#!/usr/bin/env python3
"""RA Reborn — đối chiếu chỉ số với luật gốc Red Alert 2 / Yuri's Revenge.

So sánh từng quân/công trình có trong mod với file luật INI gốc (vd rulesmd.ini của YR,
lấy từ expandmd01.mix) và báo cáo chỗ lệch. Với --apply thì ghi giá trị gốc vào YAML.

Quy đổi (rút ra từ chính OpenRA RA2 mod):
  Cost -> Valued.Cost         Strength -> Health.HP        Armor -> Armor.Type
  Sight -> RevealsShroud.Range ("Nc0")                      Speed -> Mobile.Speed (x15)
  Vũ khí: Damage -> Warhead@1Dam.Damage, ROF -> ReloadDelay, Range (ô) -> "NcM" (M = phần lẻ x1024),
          Burst -> Burst, Warhead.Verses (11 giáp) -> Versus None..Concrete, special_1 -> Drone, special_2 -> Rocket

Dùng:
  python3 tools/parity/ra2_parity.py --rules /đường/dẫn/rulesmd.ini --report AI/parity/report.md [--apply]
Cần: engine đã build (make) để chạy ./utility.sh --resolved-rules.
"""
import argparse, os, re, subprocess, sys, json

ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..'))
MOD = os.path.join(ROOT, 'mods', 'rareborn')
ARMORS = ['None', 'Flak', 'Plate', 'Light', 'Medium', 'Heavy', 'Wood', 'Steel', 'Concrete', 'Drone', 'Rocket']
ARMOR_INI = {'none': 'None', 'flak': 'Flak', 'plate': 'Plate', 'light': 'Light', 'medium': 'Medium', 'heavy': 'Heavy',
             'wood': 'Wood', 'steel': 'Steel', 'concrete': 'Concrete', 'special_1': 'Drone', 'special_2': 'Rocket'}

# Vũ khí mà OpenRA tái hiện bằng cơ chế khác (sạc điện, điều khiển tâm trí, nhảy, bom hẹn giờ, carrier…):
# chép số gốc sẽ làm hỏng cơ chế -> chỉ báo cáo, không --apply.
SPECIAL_WEAPONS = {w.lower() for w in '''CoilBolt OPCoilBolt PrismShot PrismSupport MindControl MindControlE SuperMindControl
 PsiWave SuperPsiWave DroneJump IvanBomber IvanBomberE HornetLauncher ASWLauncher Medusa MedusaE AssaultBolt AssaultBoltE
 BlimpBomb BlimpBombE VirtualScanner DefuseKit MakeupKit Sapper FakeC4 TerrorBomb DemoTruckTargeting SquidGrab SquidPunch
 DogJaw BadTeeth DolphinZap SonicZap RadEruptionWeapon ChronoBeam NeutronRifle NeutronRifleE'''.split()}

# ---------------------------------------------------------------- ghi YAML (giữ nguyên định dạng)
def set_yaml(path, block, chain, value):
    """Ghi 'leaf: value' vào block top-level `block` theo đường dẫn chain = [(key, giá trị-khi-tạo), ..., (leaf, None)].
    Node chưa có thì tạo ở cuối node cha. Giữ nguyên các dòng khác (tab, comment)."""
    lines = open(path, encoding='utf-8').read().split('\n')
    def subtree_end(i, d):
        """dòng sau cùng (exclusive) của node ở dòng i, độ sâu d; bỏ dòng trống ở cuối."""
        j = i + 1
        while j < len(lines) and (not lines[j].strip() or lines[j].startswith('\t' * (d + 1))): j += 1
        while j > i + 1 and not lines[j - 1].strip(): j -= 1
        return j
    try: node = next(i for i, l in enumerate(lines) if re.match(r'^' + re.escape(block) + r':\s*$', l))
    except StopIteration: return False
    depth = 0
    for idx, (key, create) in enumerate(chain):
        last = idx == len(chain) - 1
        d = depth + 1
        end = subtree_end(node, depth)
        pat = re.compile(r'^' + '\t' * d + re.escape(key) + r':(.*)$')
        found = next((i for i in range(node + 1, end) if pat.match(lines[i])), None)
        if found is None:
            lines.insert(end, '\t' * d + key + ':' + ((' ' + value) if last else ((' ' + create) if create else '')))
            found = end
        elif last:
            lines[found] = '\t' * d + key + ': ' + value
        node, depth = found, d
    open(path, 'w', encoding='utf-8').write('\n'.join(lines))
    return True

# ---------------------------------------------------------------- INI gốc
def read_ini(path):
    secs, cur = {}, None
    for ln in open(path, encoding='latin1'):
        s = ln.split(';')[0].strip()
        if not s: continue
        m = re.match(r'^\[([^\]]+)\]', s)
        if m:
            cur = m.group(1).strip().upper(); secs.setdefault(cur, {}); continue
        if cur and '=' in s:
            k, v = s.split('=', 1); secs[cur][k.strip().lower()] = v.strip()
    return secs

def ini_list(secs, name):
    return [v.upper() for v in secs.get(name.upper(), {}).values() if v]

# ---------------------------------------------------------------- MiniYaml (đủ dùng cho rules/weapons)
def parse_miniyaml(text):
    """Trả về list node (key, value, children). Thụt lề bằng tab."""
    root = []; stack = [(-1, root)]
    for raw in text.split('\n'):
        line = raw.rstrip('\r')
        if not line.strip() or line.lstrip().startswith('#'): continue
        depth = len(line) - len(line.lstrip('\t'))
        body = line.strip()
        body = re.sub(r'\s+#.*$', '', body)
        if ':' in body:
            k, v = body.split(':', 1); k, v = k.strip(), v.strip()
        else:
            k, v = body, ''
        node = [k, v, []]
        while stack[-1][0] >= depth: stack.pop()
        stack[-1][1].append(node); stack.append((depth, node[2]))
    return root

def node_get(nodes, key):
    for n in nodes:
        if n[0] == key: return n
    return None

def merge(base, over):
    """Gộp children kiểu MiniYaml (over đè base, '-Key' xóa)."""
    out = [list(n) for n in base]
    for n in over:
        if n[0].startswith('-'):
            out = [m for m in out if m[0] != n[0][1:]]; continue
        m = node_get(out, n[0])
        if m is None: out.append([n[0], n[1], list(n[2])])
        else:
            if n[1] != '': m[1] = n[1]
            m[2] = merge(m[2], n[2])
    return out

def load_weapons():
    defs = {}
    for f in sorted(os.listdir(os.path.join(MOD, 'weapons'))):
        if f.endswith('.yaml'):
            for n in parse_miniyaml(open(os.path.join(MOD, 'weapons', f), encoding='utf-8').read()):
                defs[n[0]] = (f, n)
    cache = {}
    def resolve(name, seen=()):
        if name in cache: return cache[name]
        if name not in defs or name in seen: return None
        _, n = defs[name]; kids = []
        for c in n[2]:
            if c[0].split('@')[0] == 'Inherits':
                p = resolve(c[1], seen + (name,))
                if p: kids = merge(kids, p)
        kids = merge(kids, [c for c in n[2] if c[0].split('@')[0] != 'Inherits'])
        cache[name] = kids; return kids
    return defs, resolve

# ---------------------------------------------------------------- OpenRA resolved rules
def resolved_rules(actor):
    env = dict(os.environ)
    out = subprocess.run([os.path.join(ROOT, 'utility.sh'), '--resolved-rules', actor], cwd=ROOT,
                         capture_output=True, text=True, env=env, timeout=300).stdout
    return parse_miniyaml(out)

def actor_ids():
    ids = {}
    for f in sorted(os.listdir(os.path.join(MOD, 'rules'))):
        if f.endswith('.yaml'):
            for ln in open(os.path.join(MOD, 'rules', f), encoding='utf-8'):
                m = re.match(r'^([A-Za-z0-9_.\-]+):\s*$', ln)
                if m and not ln.startswith('^'): ids[m.group(1).lower()] = (f, m.group(1))
    return ids

# ---------------------------------------------------------------- quy đổi
def cells_to_wdist(v):
    x = float(v); c = int(x); m = round((x - c) * 1024)
    if m == 1024: c, m = c + 1, 0
    return f'{c}c{m}'

def wdist_cells(s):
    m = re.match(r'^(-?\d+)c(\d+)$', s or '')
    return (int(m.group(1)) + int(m.group(2)) / 1024) if m else None

def pct(v):
    return int(round(float(v.strip().rstrip('%')))) if v.strip().endswith('%') else int(round(float(v) * 100))

def trait(nodes, prefix):
    """Trait theo tên (bỏ qua @tag, ưu tiên bản không tag)."""
    exact = node_get(nodes, prefix)
    if exact: return exact
    for n in nodes:
        if n[0].split('@')[0] == prefix: return n
    return None

def val(n, key):
    m = node_get(n[2], key) if n else None
    return m[1] if m else None

# ---------------------------------------------------------------- so sánh
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rules', required=True, help='rulesmd.ini (YR) hoặc rules.ini (RA2) gốc')
    ap.add_argument('--report', required=True)
    ap.add_argument('--json')
    ap.add_argument('--apply', action='store_true', help='ghi giá trị gốc vào YAML')
    a = ap.parse_args()
    ini = read_ini(a.rules)
    ids = actor_ids()
    wdefs, wres = load_weapons()
    rows, wrows, missing, done_w = [], [], [], set()
    for lst, kind in [('InfantryTypes', 'Bộ binh'), ('VehicleTypes', 'Xe & tàu'), ('AircraftTypes', 'Máy bay'), ('BuildingTypes', 'Công trình')]:
        for uid in ini_list(ini, lst):
            s = ini.get(uid, {})
            try: tl = int(s.get('techlevel', '-1'))
            except ValueError: tl = -1
            if not 1 <= tl <= 10: continue
            if uid.lower() not in ids: missing.append((kind, uid, s.get('name', ''))); continue
            r = resolved_rules(ids[uid.lower()][1])
            exp = {}
            if 'cost' in s: exp[('Valued', 'Cost')] = str(int(float(s['cost'])))
            if 'strength' in s: exp[('Health', 'HP')] = str(int(float(s['strength'])))
            if 'armor' in s: exp[('Armor', 'Type')] = ARMOR_INI.get(s['armor'].lower(), s['armor'])
            if 'sight' in s: exp[('RevealsShroud', 'Range')] = f"{int(float(s['sight']))}c0"
            if 'speed' in s and lst in ('InfantryTypes', 'VehicleTypes') and trait(r, 'Mobile'):
                exp[('Mobile', 'Speed')] = str(int(round(float(s['speed']) * 15)))
            for (t, k), e in exp.items():
                got = val(trait(r, t), k)
                ok = got is not None and (got.lower() == e.lower() if t == 'Armor' else got == e)
                if t == 'RevealsShroud' and got is not None:
                    ok = abs((wdist_cells(got) or -1) - (wdist_cells(e) or -2)) < 1e-6
                if not ok: rows.append(dict(kind=kind, id=uid, name=s.get('name', ''), trait=t, key=k, ini=e, mod=got, file=ids[uid.lower()][0], actor=ids[uid.lower()][1]))
            # vũ khí
            arms = [(n[0], val(n, 'Weapon')) for n in r if n[0].split('@')[0] == 'Armament']
            modw = {w for _, w in arms if w}
            for key in ['primary', 'secondary', 'eliteprimary', 'elitesecondary']:
                w = s.get(key)
                if not w: continue
                wu = next((x for x in modw if x.lower() == w.lower()), None)
                if not wu:
                    rows.append(dict(kind=kind, id=uid, name=s.get('name', ''), trait='Armament', key=key, ini=w, mod=', '.join(sorted(modw)) or None, file=ids[uid.lower()][0], actor=ids[uid.lower()][1]))
                    continue
                if wu in done_w: continue
                done_w.add(wu)
                ws = ini.get(w.upper(), {}); wy = wres(wu)
                if wy is None: continue
                whd = trait(wy, 'Warhead')
                whname, whtype = (whd[0], whd[1]) if whd else ('Warhead@1Dam', 'SpreadDamage')
                cmp = []
                if 'damage' in ws: cmp.append(('Damage', str(int(float(ws['damage']))), val(whd, 'Damage')))
                if 'rof' in ws: cmp.append(('ReloadDelay', str(int(float(ws['rof']))), val(wy and ['', '', wy], 'ReloadDelay')))
                if 'range' in ws: cmp.append(('Range', cells_to_wdist(ws['range']), val(['', '', wy], 'Range')))
                if 'burst' in ws: cmp.append(('Burst', str(int(float(ws['burst']))), val(['', '', wy], 'Burst') or '1'))
                wh = ini.get(ws.get('warhead', '').upper(), {})
                if 'verses' in wh:
                    vs = [pct(x) for x in wh['verses'].split(',')]
                    vy = node_get(whd[2], 'Versus') if whd else None
                    for i, arm in enumerate(ARMORS):
                        if i < len(vs):
                            got = val(vy, arm) if vy else None
                            cmp.append((f'Versus.{arm}', str(vs[i]), got if got is not None else '100'))
                for k, e, g in cmp:
                    same = (g == e) if k != 'Range' else (g is not None and abs((wdist_cells(g) or -9) - (wdist_cells(e) or -8)) < 1e-3)
                    if not same:
                        wrows.append(dict(weapon=wu, used_by=uid, key=k, ini=e, mod=g, file=wdefs[wu][0] if wu in wdefs else '?',
                                          special=wu.lower() in SPECIAL_WEAPONS, whname=whname, whtype=whtype))
    applied = 0
    if a.apply:
        for r in rows:
            if r['trait'] == 'Armament': continue
            if set_yaml(os.path.join(MOD, 'rules', r['file']), r['actor'], [(r['trait'], ''), (r['key'], None)], r['ini']):
                r['applied'] = True; applied += 1
        for r in wrows:
            if r['special'] or r['file'] == '?': continue
            f = os.path.join(MOD, 'weapons', r['file'])
            k = r['key']
            if k in ('ReloadDelay', 'Range', 'Burst'): chain = [(k, None)]
            elif k == 'Damage': chain = [(r['whname'], r['whtype']), ('Damage', None)]
            else: chain = [(r['whname'], r['whtype']), ('Versus', ''), (k.split('.', 1)[1], None)]
            if set_yaml(f, r['weapon'], chain, r['ini']): r['applied'] = True; applied += 1
        print('đã ghi', applied, 'giá trị')
    # ---- báo cáo
    os.makedirs(os.path.dirname(os.path.abspath(a.report)), exist_ok=True)
    with open(a.report, 'w', encoding='utf-8') as f:
        f.write('# Đối chiếu chỉ số RA Reborn ↔ luật gốc\n\n')
        f.write(f'Nguồn: `{os.path.basename(a.rules)}`. Chỉ xét mục xây được (TechLevel 1–10).\n\n')
        f.write(f'- Quân/công trình lệch chỉ số: **{len({r["id"] for r in rows})}** ({len(rows)} giá trị)\n')
        f.write(f'- Vũ khí lệch: **{len({r["weapon"] for r in wrows})}** ({len(wrows)} giá trị)\n')
        f.write(f'- Chưa có trong RA Reborn: **{len(missing)}**\n\n')
        f.write('## Quân / công trình\n\n| Loại | Mã | Tên | Thuộc tính | Gốc | RA Reborn |\n|---|---|---|---|---|---|\n')
        for r in rows: f.write(f"| {r['kind']} | {r['id']} | {r['name']} | {r['trait']}.{r['key']} | {r['ini']} | {r['mod']}{' → đã sửa' if r.get('applied') else ''} |\n")
        f.write('\n## Vũ khí\n\nVũ khí đánh dấu ⚙️ có cơ chế riêng trong OpenRA (sạc điện, điều khiển tâm trí, nhảy…): không tự sửa.\n\n| Vũ khí | Quân dùng | Thuộc tính | Gốc | RA Reborn |\n|---|---|---|---|---|\n')
        for r in wrows: f.write(f"| {'⚙️ ' if r['special'] else ''}{r['weapon']} | {r['used_by']} | {r['key']} | {r['ini']} | {r['mod']}{' → đã sửa' if r.get('applied') else ''} |\n")
        f.write('\n## Chưa có\n\n| Loại | Mã | Tên |\n|---|---|---|\n')
        for k, u, n in missing: f.write(f'| {k} | {u} | {n} |\n')
    if a.json: json.dump(dict(rows=rows, weapons=wrows, missing=missing), open(a.json, 'w'), ensure_ascii=False, indent=1)
    print(f'actors lệch: {len({r["id"] for r in rows})} ({len(rows)} giá trị) · vũ khí lệch: {len({r["weapon"] for r in wrows})} ({len(wrows)}) · chưa có: {len(missing)}')

if __name__ == '__main__':
    main()
