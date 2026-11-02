# -*- coding: utf-8 -*-
import json, os, sys, base64, io, html
from PIL import Image
W = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, W)
from content import *

items = json.load(open(W + '/items.json'))
sw = {s['id']: s for s in json.load(open(W + '/sw.json'))}
byid = {i['id']: i for i in items}

def b64(path, fmt=None, width=None, q=82):
    im = Image.open(path)
    if width and im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    if fmt == 'jpg':
        im.convert('RGB').save(buf, 'JPEG', quality=q); mime = 'image/jpeg'
    else:
        im.save(buf, 'PNG'); mime = 'image/png'
    return f'data:{mime};base64,' + base64.b64encode(buf.getvalue()).decode()

def cameo(id_):
    p = f'{W}/img/{id_}.png'
    if not os.path.exists(p): return ''
    im = Image.open(p).resize((120, 96), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, 'PNG')
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()

def side_of(it):
    if it['id'] in SIDE_OF: return SIDE_OF[it['id']]
    if it['cat'] == 'BuildingTypes':
        pre = it['prereq']
        if 'YACNST' in pre or it['id'] in ('GAFWLL',): return 'Y'
        if 'NACNST' in pre or it['id'] in ('NAWALL',): return 'S'
        if 'GACNST' in pre or it['id'] in ('GAWALL',): return 'A'
    s = it['sides']
    return s if len(s) == 1 else s[0]

GENERIC = {'POWER': 'Power Plant', 'PROC': 'Refinery', 'RADAR': 'Radar', 'TECH': 'Battle Lab', 'BARRACKS': 'Barracks'}
SHORT = {'GAPILE': 'Barracks', 'NAHAND': 'Barracks', 'YABRCK': 'Barracks', 'GAWEAP': 'War Factory', 'NAWEAP': 'War Factory',
         'YAWEAP': 'War Factory', 'GATECH': 'Battle Lab', 'NATECH': 'Battle Lab', 'YATECH': 'Battle Lab', 'NARADR': 'Radar Tower',
         'GAYARD': 'Shipyard', 'NAYARD': 'Shipyard', 'YAYARD': 'Naval Yard', 'GADEPT': 'Repair Depot', 'NADEPT': 'Repair Depot',
         'NAREFN': 'Refinery', 'GAREFN': 'Refinery', 'GAROBO': 'Robot Control', 'NAPSIS': 'Psychic Radar', 'YAGRND': 'Grinder'}
def prereq_txt(it):
    out = []
    for p in [x.strip() for x in it['prereq'].split(',') if x.strip()]:
        P = p.upper()
        if P.endswith('CNST'): continue
        out.append(GENERIC.get(P) or SHORT.get(P) or (byid[P]['name'] if P in byid else p))
    return ', '.join(out) or 'Construction Yard'

def card(it, color):
    role, desc = D.get(it['id'], ('', ''))
    stats = []
    if it['cost']: stats.append(f"<span><b>${int(it['cost']):,}</b></span>")
    if it['hp']: stats.append(f"<span>Máu <b>{it['hp']}</b></span>")
    if it['cat'] != 'BuildingTypes' and it['speed']: stats.append(f"<span>Tốc độ <b>{it['speed']}</b></span>")
    if it['cat'] == 'BuildingTypes' and it['power'] not in ('', '0'):
        pw = int(it['power']); stats.append(f"<span>Điện <b class='{'pos' if pw > 0 else 'neg'}'>{pw:+d}</b></span>")
    img = cameo(it['id'])
    return f"""<div class="card">
  <img class="cam" src="{img}">
  <div class="cb">
    <div class="nm">{html.escape(it['name'])}</div>
    <div class="role" style="color:{color}">{role}</div>
    <div class="st">{''.join(stats)}</div>
    <div class="ds">{desc}</div>
    <div class="pr">Cần: {html.escape(prereq_txt(it))}</div>
  </div>
</div>"""

CAT_ORDER = [('InfantryTypes', 'Bộ binh'), ('VehicleTypes', 'Xe, tàu & khí cầu'), ('AircraftTypes', 'Máy bay'), ('BuildingTypes', 'Công trình')]

def side_section(key):
    S = SIDES[key]; c = S['color']
    countries = [x for x in COUNTRIES if x[0] == key]
    h = [f'<section class="side" style="--c:{c};--l:{S["light"]}">']
    h.append(f'<div class="sidehead"><div class="kicker">{S["num"]} · PHE</div><h1>{S["name"]}</h1></div>')
    h.append(f'<p class="lead">{S["intro"]}</p>')
    h.append('<div class="two"><div class="box pros"><h4>Điểm mạnh</h4><ul>' + ''.join(f'<li>{x}</li>' for x in S['pros']) +
             '</ul></div><div class="box cons"><h4>Điểm yếu</h4><ul>' + ''.join(f'<li>{x}</li>' for x in S['cons']) + '</ul></div></div>')
    h.append('<h3>Thứ tự xây gợi ý khi mới vào trận</h3><ol class="bo">' + ''.join(f'<li>{x}</li>' for x in S['build']) + '</ol>')
    h.append('<h3>Quốc gia & quân đặc trưng</h3><div class="countries">')
    for _, cid, nm, uniq, txt in countries:
        h.append(f'''<div class="ctry"><img src="{b64(SIG[cid])}">
          <div><div class="cn">{nm}{f' <span class="cu">{uniq}</span>' if uniq else ''}</div><div class="ct">{txt}</div></div></div>''')
    h.append('</div>')
    for cat, label in CAT_ORDER:
        lst = [i for i in items if i['cat'] == cat and i['id'] not in SKIP and side_of(i) == key]
        if not lst: continue
        lst.sort(key=lambda i: (int(i['cost'] or 0)))
        h.append(f'<h2 class="cat">{label} <small>{len(lst)}</small></h2><div class="grid">')
        h.extend(card(i, c) for i in lst)
        h.append('</div>')
    h.append('</section>')
    return '\n'.join(h)

SWROWS = [
 ('NukeSpecial', 'NAMISL', 'Liên Xô', 'Nuclear Missile Silo', 'Tên lửa hạt nhân: phá hủy một vùng rộng, để lại phóng xạ.'),
 ('IronCurtainSpecial', 'NAIRON', 'Liên Xô', 'Iron Curtain Device', 'Làm một nhóm xe hoặc công trình bất tử trong thời gian ngắn. Bộ binh dính vào sẽ chết.'),
 ('SpyPlaneSpecial', 'NARADR', 'Liên Xô', 'Radar Tower', 'Máy bay trinh sát bay qua, soi một vùng.'),
 ('LightningStormSpecial', 'GAWEAT', 'Đồng Minh', 'Weather Controller', 'Bão sét đánh liên tục xuống một khu vực.'),
 ('ChronoSphereSpecial', 'GACSPH', 'Đồng Minh', 'Chronosphere', 'Dịch chuyển tức thời một nhóm xe đến bất kỳ đâu (bộ binh đi theo sẽ chết).'),
 ('AmericanParaDropSpecial', 'AMRADR', 'Mỹ', 'Air Force Command', 'Thả một tiểu đội lính dù GI.'),
 ('PsychicDominatorSpecial', 'YAPPET', 'Yuri', 'Psychic Dominator', 'Chiếm quyền điều khiển vĩnh viễn mọi đơn vị trong vùng, gây sát thương công trình.'),
 ('GeneticConverterSpecial', 'YAGNTC', 'Yuri', 'Genetic Mutator', 'Biến toàn bộ bộ binh trong vùng thành Brute của Yuri.'),
 ('PsychicRevealSpecial', 'NAPSIS', 'Yuri', 'Psychic Radar', 'Soi một vùng trên bản đồ.'),
 ('ParaDropSpecial', None, 'Mọi phe', 'Tech Airport (chiếm được)', 'Thả lính dù của phe bạn.'),
]
def sw_table():
    rows = []
    for sid, bid, side, bname, txt in SWROWS:
        icon = f'{W}/img/sw_{sid}.png'
        if sid == 'LightningStormSpecial' or not os.path.exists(icon): icon = f'{W}/img/{bid}.png'
        rows.append(f'<tr><td><img class="swi" src="{b64(icon)}"></td><td><b>{html.escape(sw[sid]["name"])}</b><br><small>{side} · {bname}</small></td>'
                    f'<td class="num">{sw[sid]["recharge"]} phút</td><td>{txt}</td></tr>')
    return '<table class="t sw"><tr><th></th><th>Siêu vũ khí</th><th>Hồi chiêu</th><th>Tác dụng</th></tr>' + ''.join(rows) + '</table>'

def table(rows, h1, h2, cls=''):
    return f'<table class="t {cls}"><tr><th>{h1}</th><th>{h2}</th></tr>' + ''.join(f'<tr><td><b>{a}</b></td><td>{b}</td></tr>' for a, b in rows) + '</table>'

def small(id_):
    im = Image.open(f'{W}/img/{id_}.png').resize((60, 48), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, 'JPEG', quality=80)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()

SIG = {'ustates': f'{W}/img/sw_AmericanParaDropSpecial.png', 'korea': f'{W}/img/BEAG.png', 'france': f'{W}/img/GTGCAN.png',
       'germany': f'{W}/img/TNKD.png', 'ukingdom': f'{W}/img/SNIPE.png', 'russia': f'{W}/img/TTNK.png', 'iraq': f'{W}/img/DESO.png',
       'cuba': f'{W}/img/TERROR.png', 'libya': f'{W}/img/DTRUCK.png', 'yuri': f'{W}/img/YURIPR.png'}

def quickref():
    out = ['<table class="t qr"><tr><th></th><th>Tên</th><th>Mã</th><th>Phe</th><th>Loại</th><th class="num">Giá</th><th class="num">Máu</th><th class="num">Tốc độ</th></tr>']
    lab = {'InfantryTypes': 'Bộ binh', 'VehicleTypes': 'Xe/tàu', 'AircraftTypes': 'Máy bay', 'BuildingTypes': 'Công trình'}
    sn = {'A': 'Đồng Minh', 'S': 'Liên Xô', 'Y': 'Yuri'}
    for i in sorted([i for i in items if i['id'] not in SKIP], key=lambda i: ('ASY'.index(side_of(i)), list(lab).index(i['cat']), int(i['cost'] or 0))):
        sp = i['speed'] if i['cat'] != 'BuildingTypes' else '–'
        out.append(f"<tr class='s{side_of(i)}'><td class='qi'><img src='{small(i['id'])}'></td><td>{html.escape(i['name'])}</td><td style='color:#666;font-size:7.4pt'>{i['id']}</td><td>{sn[side_of(i)]}</td><td>{lab[i['cat']]}</td><td class='num'>{int(i['cost']):,}</td><td class='num'>{i['hp']}</td><td class='num'>{sp}</td></tr>")
    out.append('</table>')
    return ''.join(out)

TIPS = [
 ('Kinh tế là trên hết', 'Xây 2 nhà máy lọc thật sớm, sau đó thêm xe khai thác. Ai nhiều tiền hơn thường thắng. Bãi <b>đá quý</b> (tinh thể nhiều màu) đáng giá hơn quặng vàng.'),
 ('Đừng để thiếu điện', 'Thanh điện nằm cạnh thanh xây. Khi điện tụt xuống đỏ, mọi thứ xây chậm lại, radar tắt và nhiều tháp phòng thủ ngừng bắn. Luôn dư một nhà máy điện.'),
 ('Nhiều nhà máy = nhanh hơn', 'Có 2–3 doanh trại hoặc xưởng xe cùng loại thì sản xuất nhanh hơn hẳn.'),
 ('Bán và sửa', 'Bán công trình (phím L) được hoàn 50% giá. Sửa công trình (phím K) tốn tiền; cho Kỹ sư vào công trình phe mình thì sửa đầy máu ngay.'),
 ('Chiếm công nghệ phe khác', 'Dùng Kỹ sư chiếm Construction Yard, Barracks hoặc War Factory của địch là xây được quân của phe đó. Ví dụ Đồng Minh có thể sở hữu Rhino hay Kirov.'),
 ('Hộ tống xe khai thác', 'Địch thường đánh vào xe khai thác. Đặt vài quân hoặc tháp phòng thủ gần bãi quặng.'),
 ('Gom quân vào nhóm', 'Ctrl+1 cho nhóm tăng, Ctrl+2 cho phòng không, Ctrl+3 cho bộ binh... Đánh theo nhóm có vai trò rõ ràng thắng chắc hơn đánh dồn một cục.'),
 ('Chiếm nhà cao tầng', 'Cho bộ binh vào nhà dân để có công sự: bắn ra an toàn và tầm xa hơn. Muốn đuổi lính ra thì phá nhà bằng xe tăng hoặc pháo.'),
 ('Phòng Yuri', 'Đánh với Yuri thì luôn để vài con chó trong căn cứ và đi cùng đội quân. Dùng Robot Tank hoặc Terror Drone (miễn nhiễm điều khiển tâm trí). Tiêu diệt Yuri hoặc Master Mind thì quân bị điều khiển được trả lại.'),
 ('Rải căn cứ ra', 'Đừng xây dồn mọi thứ một chỗ: một quả hạt nhân hay một trận bão sét có thể xóa sổ cả cụm.'),
 ('Lên cấp quân', 'Quân lên <b>Cựu binh</b> khi tiêu diệt kẻ địch có tổng giá trị gấp 3 lần giá của chính nó: bền hơn, nhanh hơn, bắn nhanh hơn. <b>Tinh nhuệ</b> thì mạnh hơn nữa và tự hồi máu. Giữ quân lâu năm sống sót!'),
 ('Tận dụng IFV', 'IFV là xe rẻ mà linh hoạt nhất game. Một nhóm IFV chở Kỹ sư sẽ tự sửa cho nhau.'),
 ('Lộ trình (Z)', 'Bấm Z rồi click nhiều điểm để đặt đường đi vòng, tránh tháp phòng thủ và đánh úp từ phía sau.'),
 ('Dời căn cứ', 'Khi bật MCV Repacks, chọn Construction Yard rồi bấm D để thu về thành xe MCV và dời sang chỗ mới.'),
]


TRICKS = [
 ('Dìm xe địch xuống biển', 'Đồng Minh', 'Dùng <b>Chronosphere</b> chọn một cụm xe tăng <i>của địch</i> rồi thả chúng xuống mặt nước. Xe mặt đất không bơi được nên chìm ngay lập tức.'),
 ('Diệt bộ binh bằng siêu vũ khí "phòng thủ"', 'Đồng Minh / Liên Xô', 'Bộ binh dính <b>Iron Curtain</b> hoặc bị <b>Chronosphere</b> dịch chuyển sẽ chết. Bắn hai siêu vũ khí này vào cụm lính địch đông là xóa sổ cả đám.'),
 ('Kirov bất tử', 'Liên Xô', 'Đợi đoàn Kirov hoặc Apocalypse vừa tới căn cứ địch rồi phủ <b>Iron Curtain</b> lên: chúng phá sạch mà không ai bắn hạ được.'),
 ('Bom Ivan "di động"', 'Liên Xô', 'Cho <b>Crazy Ivan</b> gắn bom lên chó, lính rẻ hoặc cả con bò trên bản đồ, rồi cho chạy vào giữa cụm quân hay công trình địch.'),
 ('Bắn lò hạt nhân của địch', 'Mọi phe', 'Gặp Liên Xô có <b>Nuclear Reactor</b> thì dồn hỏa lực phá nó: lò sẽ nổ to và gây thiệt hại nặng cho chính căn cứ của họ.'),
 ('Cắt điện trước khi tổng tấn công', 'Đồng Minh', 'Đưa <b>Gián điệp</b> vào nhà máy điện địch ngay trước đợt tấn công: tháp Prism, Tesla, Patriot đều tắt trong một lúc.'),
 ('Kỹ sư "nhảy dù"', 'Mọi phe', 'Chở 5 Kỹ sư bằng NightHawk hoặc xe đổ bộ, đổ thẳng vào căn cứ địch và chiếm Construction Yard, Battle Lab hoặc War Factory. Bạn có công nghệ của phe đó; công trình chiếm được cũng có thể bán ngay lấy tiền.'),
 ('Bán trước khi mất', 'Mọi phe', 'Công trình sắp bị phá thì bấm <kbd>L</kbd> và click vào nó để bán: lấy lại 50% tiền thay vì mất trắng, thường còn có vài lính chạy ra.'),
 ('Nghiền tù binh ra tiền', 'Yuri', 'Dùng Yuri Clone hoặc Master Mind chiếm quân địch, sau đó đưa vào <b>Grinder</b> để đổi thành tiền. Vừa mất quân vừa nuôi kinh tế của bạn.'),
 ('Cướp cả căn cứ', 'Yuri', '<b>Yuri Prime</b> điều khiển được công trình. Chiếm Construction Yard của địch là có luôn công nghệ của phe đó.'),
 ('Quấy rối bằng Rocketeer', 'Đồng Minh', 'Đầu trận, Conscript và GI không bắn lên trời được. Vài <b>Rocketeer</b> bay vào bắn lính và chặn xe khai thác làm đối phương rất khó chịu.'),
 ('Phục kích bằng Mirage', 'Đồng Minh', 'Đặt 3–4 <b>Mirage Tank</b> đứng yên ở bãi quặng giữa bản đồ: chúng ngụy trang thành cây và bắn tan xe khai thác hoặc đoàn quân đi qua.'),
 ('Phá cầu chặn đường', 'Mọi phe', 'Bấm <kbd>Ctrl</kbd> + click vào cây cầu để bắn sập, buộc địch đi đường vòng. Muốn sửa cầu thì cho Kỹ sư vào chòi gác ở đầu cầu.'),
 ('Tesla Coil chạy không cần điện', 'Liên Xô', 'Lính <b>Tesla Trooper</b> đứng cạnh Tesla Coil sẽ sạc cho nó: tháp vẫn bắn khi căn cứ mất điện và bắn mạnh hơn bình thường.'),
 ('Pháo đài bắn tỉa', 'Anh / Đồng Minh', 'Nhồi 5 <b>Sniper</b> (Anh) hoặc 5 Guardian GI vào <b>Battle Fortress</b>: một pháo đài di động diệt bộ binh hoặc xe tăng cực mạnh.'),
 ('Lính nhân đôi', 'Yuri', 'Có <b>Cloning Vats</b> thì mỗi bộ binh bạn mua được tặng một bản sao: Initiate, Brute, Virus… đều thành gấp đôi với cùng số tiền.'),
 ('Tù binh làm điện', 'Yuri', 'Cho lính (kể cả lính địch bị điều khiển) vào <b>Bio Reactor</b> để tăng sản lượng điện.'),
 ('Mở khóa quân bí mật', 'Mọi phe', 'Gián điệp lọt vào Battle Lab của từng phe sẽ mở khóa Chrono Commando, Chrono Ivan hoặc Psi Commando: những quân không thể có bằng cách thông thường.'),
]

SYSTRICKS = [
 ('Không có mã cheat', 'Red Alert 2 và Yuri\'s Revenge bản phát hành <b>không có mã cheat gõ phím</b>. Đừng tải các "trainer" hay tool hack lạ trên mạng: chúng rất hay chứa virus, và Ra2026 chỉ bảo vệ chính game chứ không chặn được chương trình khác bạn tự chạy.'),
 ('Tiền khởi đầu nhiều hơn menu cho phép', 'Mở file <b>RA2MD.INI</b> trong thư mục Ra2026 bằng Notepad, tìm mục <code>[Skirmish]</code> rồi sửa dòng <code>Credits=</code> (file của bạn đang để 20000). Lưu lại rồi vào Skirmish và đừng chạm vào ô Credits trong menu. Nếu game tự đặt lại giá trị, chọn mức cao nhất có sẵn trong menu.'),
 ('Tự chỉnh chỉ số quân (mod)', 'Cách dễ nhất: mở <b>E:\\games\\Ra2\\AI\\tools\\RA2_Mod_Editor.html</b> bằng Chrome/Edge để sửa trực quan. Muốn sửa tay: bản luật chính thức nằm ở <b>AI\\mod\\rulesmd-official-yr.ini</b>; chép vào Ra2026, đổi tên thành <b>rulesmd.ini</b> rồi sửa các dòng của từng quân, ví dụ <code>[HTNK]</code> (Rhino): <code>Cost=900</code> là giá, <code>Strength=400</code> là máu. Game ưu tiên file rulesmd.ini rời hơn luật trong .mix.'),
 ('Lưu ý khi mod', 'Chơi LAN thì <b>mọi máy phải dùng cùng một file</b>, nếu không trận đấu sẽ lỗi đồng bộ. Luôn giữ lại bản gốc. Mã nhận diện của từng quân (HTNK, MTNK, E1…) được ghi trong bảng tra cứu ở cuối sổ tay này.'),
 ('Cả hai game trong thư mục này đã bị mod', '<b>Play_RA2</b> dùng file <b>rules.ini</b> rời đã chỉnh (thêm hơn 30 bộ binh và gần 40 xe). <b>Play_YR</b> dùng luật mod trong <b>expandmd03.mix</b>: xây nhanh gần gấp 3, bán công trình hoàn 100%, thêm 51 quân mới (F-16, M1A2, Medic, Titan...), bỏ Harrier, đổi một số chỉ số. Sổ tay này mô tả luật <b>chính thức</b>; muốn chơi đúng như sổ tay, dùng nút Khôi phục → “bản chính thức” trong RA2 Mod Editor.'),
 ('Cửa sổ hay toàn màn hình', 'Bấm <kbd>Alt</kbd> + <kbd>Enter</kbd> khi đang chơi để chuyển qua lại giữa cửa sổ và toàn màn hình. Các tùy chọn đồ họa khác nằm trong file <b>ddraw.ini</b>.'),
 ('Lưu và tải trận', 'Bấm <kbd>Esc</kbd> → <b>Save Game</b> để lưu cả trận Skirmish lẫn chiến dịch. Nên lưu trước khi tổng tấn công.'),
]

CSS = """
@page { size: A4; margin: 13mm 13mm 15mm 13mm; }
* { box-sizing: border-box; }
body { font-family: Inter, 'DejaVu Sans', sans-serif; font-size: 9.6pt; color: #222; line-height: 1.45; margin: 0; }
h1,h2,h3,h4 { font-family: 'Inter Display', Inter, sans-serif; margin: 0; }
.title { border-bottom: 1.5pt solid #222; padding-bottom: 3mm; margin-bottom: 4mm; }
.title .k { font-size: 8.5pt; letter-spacing: .25em; color: #666; font-weight: 600; }
.title h1 { font-size: 26pt; font-weight: 900; line-height: 1.05; margin: 1mm 0 1.5mm; letter-spacing: -.01em; }
.title .sub { font-size: 10.5pt; color: #444; }
.title .tags span { font-weight: 800; margin-right: 4mm; }
h2.sec { font-size: 17pt; font-weight: 800; margin: 0 0 3mm; padding-bottom: 1.5mm; border-bottom: 1pt solid #222; }
h3 { font-size: 11.5pt; font-weight: 700; margin: 4mm 0 1.8mm; }
p { margin: 0 0 2.2mm; }
.pb { break-before: page; }
.toc ol { columns: 2; column-gap: 10mm; padding-left: 5mm; font-size: 10.5pt; margin: 0 0 3mm; }
.toc li { margin: 0 0 1.4mm; }
.note { border: .7pt solid #bbb; border-left: 2.2pt solid #888; padding: 2.2mm 3.5mm; margin: 2.5mm 0; border-radius: 1.5mm; }
.note.warn { border-left-color: #c77d00; }
code { font-family: 'DejaVu Sans Mono', monospace; font-size: 8.4pt; border: .5pt solid #ccc; border-radius: .8mm; padding: 0 1mm; }
table.t { width: 100%; border-collapse: collapse; margin: 1.5mm 0 3.5mm; font-size: 9pt; }
table.t th { text-align: left; color: #222; padding: 1.2mm 2mm; font-weight: 700; border-bottom: 1.2pt solid #222; }
table.t td { padding: .95mm 2mm; border-bottom: .5pt solid #d6d6d6; vertical-align: top; }
table.t tr { break-inside: avoid; }
td.num, th.num { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
table.sw td, table.tech td { vertical-align: middle; }
img.swi { width: 14mm; display: block; border-radius: .8mm; }
img.tch { width: 17mm; display: block; }
table.qr { font-size: 8pt; } table.qr td { padding: .5mm 1.6mm; vertical-align: middle; }
td.qi { width: 9mm; padding: .4mm 1mm !important; } td.qi img { width: 8mm; height: 6.4mm; display: block; border-radius: .5mm; }
tr.sA td:nth-child(2) { border-left: 1.5pt solid #1f5fae; } tr.sS td:nth-child(2) { border-left: 1.5pt solid #b3261e; } tr.sY td:nth-child(2) { border-left: 1.5pt solid #6a35a8; }
.side { break-before: page; }
.sidehead { border-bottom: 2pt solid var(--c); padding-bottom: 1.5mm; margin-bottom: 3mm; }
.sidehead .kicker { font-size: 8.5pt; letter-spacing: .25em; color: var(--c); font-weight: 700; }
.sidehead h1 { font-size: 24pt; font-weight: 900; color: var(--c); }
.lead { font-size: 10.5pt; }
.two { display: grid; grid-template-columns: 1fr 1fr; gap: 3mm; }
.box { border: .7pt solid #ccc; border-radius: 1.5mm; padding: 2.2mm 3.5mm; }
.box h4 { font-size: 10pt; margin-bottom: .8mm; color: var(--c); }
.box ul { margin: 0; padding-left: 4.5mm; } .box li { margin-bottom: .8mm; }
.cons h4 { color: #555; }
ol.bo { padding-left: 5mm; margin: 0; columns: 2; column-gap: 8mm; } ol.bo li { margin-bottom: .6mm; font-weight: 600; }
ol.bo li::marker { color: var(--c); font-weight: 800; }
.countries { display: grid; grid-template-columns: 1fr 1fr; gap: 2mm; }
.ctry { display: grid; grid-template-columns: 15mm 1fr; gap: 2.5mm; align-items: start; border: .5pt solid #d0d0d0; border-radius: 1.5mm; padding: 1.8mm; break-inside: avoid; }
.ctry img { width: 15mm; border-radius: .8mm; display: block; }
.cn { font-weight: 800; font-size: 10pt; } .cu { font-size: 7.6pt; font-weight: 700; color: var(--c); border: .6pt solid var(--c); padding: 0 1.4mm; border-radius: 1mm; margin-left: 1mm; }
.ct { font-size: 8.6pt; margin-top: .6mm; }
h2.cat { font-size: 13.5pt; font-weight: 800; color: var(--c); margin: 5mm 0 2.5mm; padding-bottom: 1mm; border-bottom: 1pt solid var(--c); break-after: avoid; }
h2.cat small { font-size: 9pt; color: #888; font-weight: 600; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 2mm; }
.card { display: grid; grid-template-columns: 17mm 1fr; gap: 2.5mm; border: .5pt solid #d0d0d0; border-radius: 1.5mm; padding: 1.8mm; break-inside: avoid; }
.card .cam { width: 17mm; height: 13.6mm; border-radius: .8mm; display: block; }
.nm { font-weight: 800; font-size: 10pt; line-height: 1.2; }
.role { font-size: 7.8pt; font-weight: 700; text-transform: uppercase; letter-spacing: .03em; margin: .3mm 0 .8mm; }
.st { display: flex; flex-wrap: wrap; gap: .6mm 2.5mm; font-size: 8pt; color: #444; margin-bottom: .8mm; }
.st b.pos { color: #1b7f3b; } .st b.neg { color: #b3261e; }
.ds { font-size: 8.5pt; line-height: 1.36; }
.pr { font-size: 7.4pt; color: #777; margin-top: .8mm; }
.tips { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5mm 2.5mm; }
.tip { border: .5pt solid #d0d0d0; border-radius: 1.5mm; padding: 1.6mm 2.6mm; break-inside: avoid; }
.tip .n { display: inline-block; min-width: 5.5mm; height: 5.5mm; line-height: 4.9mm; text-align: center; border-radius: 50%; border: .8pt solid #222; font-weight: 800; font-size: 8pt; margin-right: 1.6mm; }
.tip b.h { font-size: 9.8pt; }
.tip .who { font-size: 7.6pt; color: #777; font-weight: 600; margin-left: 1mm; }
.tip p { margin: .6mm 0 0; font-size: 8.4pt; line-height: 1.34; }
.keys td:first-child { white-space: nowrap; width: 42mm; } .keys td { padding: .5mm 2mm; }
kbd { font-family: inherit; font-weight: 700; border: .6pt solid #999; border-bottom-width: 1.2pt; border-radius: .9mm; padding: 0 1.3mm; font-size: 8.4pt; }
.steps { counter-reset: s; padding: 0; list-style: none; margin: 0 0 2mm; }
.steps li { counter-increment: s; position: relative; padding-left: 7.5mm; margin-bottom: 1.3mm; }
.steps li::before { content: counter(s); position: absolute; left: 0; top: -.2mm; width: 5mm; height: 5mm; line-height: 4.4mm; text-align: center; border-radius: 50%; border: .8pt solid #222; font-weight: 800; font-size: 8pt; }
.foot { font-size: 8pt; color: #777; margin-top: 4mm; }
"""

TECHIMG = ['tech_caoild', 'tech_cahosp', 'tech_camach', 'tech_caairp', 'tech_capowr', 'tech_caslab', None]

def tech_table():
    rows = []
    for (a, b), im in zip(TECH, TECHIMG):
        cell = f'<img class="tch" src="{b64(f"{W}/img/{im}.png", "jpg", 160, 82)}">' if im else ''
        rows.append(f'<tr><td>{cell}</td><td><b>{a}</b></td><td>{b}</td></tr>')
    return '<table class="t tech"><tr><th></th><th>Công trình</th><th>Lợi ích</th></tr>' + ''.join(rows) + '</table>'

def kbd(s):
    s = s.replace('chuột trái', 'chuột\u00a0trái')
    return ' '.join(f'<kbd>{p}</kbd>' if p not in ('+', '/', '…', '–') else p for p in s.replace('+', ' + ').split(' ') if p)

def tipgrid(rows, with_who=False):
    out = []
    for i, r in enumerate(rows):
        if with_who: a, who, b = r
        else: (a, b), who = r, ''
        out.append(f'<div class="tip"><span class="n">{i+1}</span><b class="h">{a}</b>{f"<span class=who>· {who}</span>" if who else ""}<p>{b}</p></div>')
    return '<div class="tips">' + ''.join(out) + '</div>'

def quickref_ids():
    return quickref()

def build():
    keys = '<table class="t keys"><tr><th>Phím / thao tác</th><th>Tác dụng</th></tr>' + ''.join(
        f'<tr><td>{kbd(a) if not a.startswith(("Chuột","Kéo")) else "<b>"+a+"</b>"}</td><td>{b}</td></tr>' for a, b in HOTKEYS) + '</table>'
    n_items = len([i for i in items if i['id'] not in SKIP])
    doc = f"""<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>Red Alert 2: Yuri's Revenge – Sổ tay người chơi</title><style>{CSS}</style></head><body>
<div class="title"><div class="k">SỔ TAY NGƯỜI CHƠI · RA2026</div>
<h1>Red Alert 2: Yuri's Revenge</h1>
<div class="sub">Hướng dẫn chơi từ A đến Z: 3 phe, 10 quốc gia, {n_items} loại quân &amp; công trình, siêu vũ khí, phím tắt, thủ thuật và mẹo chiến thuật.<br>
<span class="tags"><span style="color:#1f5fae">Đồng Minh</span><span style="color:#b3261e">Liên Xô</span><span style="color:#6a35a8">Yuri</span></span>
<span style="color:#888;font-size:8.5pt">Ảnh và chỉ số trích từ luật chính thức của game (rulesmd.ini trong expandmd01.mix) · Bản cập nhật 02/11/2026 · Bố cục tiết kiệm mực in</span></div></div>

<section class="toc"><h2 class="sec">Mục lục</h2><ol>
<li>Bắt đầu chơi với Ra2026</li><li>Màn hình & điều khiển</li><li>Phím tắt</li><li>Kinh tế, điện & lên cấp</li>
<li>Đồng Minh (Allies)</li><li>Liên Xô (Soviets)</li><li>Yuri</li><li>Siêu vũ khí</li>
<li>Gián điệp, IFV & công trình trung lập</li><li><b>Thủ thuật</b> (trong trận & chỉnh game)</li><li>Khắc chế & 14 mẹo chiến thuật</li><li>Bảng tra cứu nhanh có hình</li></ol>
<div class="note"><b>Ba phe trong game:</b> <b style="color:#1f5fae">Đồng Minh</b> (Mỹ và châu Âu, công nghệ cao), <b style="color:#b3261e">Liên Xô</b> (xe tăng nặng, đông quân; đây là phe cộng sản, không phải phát xít) và <b style="color:#6a35a8">Yuri</b> (điều khiển tâm trí, chỉ có trong Yuri's Revenge).</div>
<div class="note warn"><b>Lưu ý:</b> game trong Ra2026 có sẵn mod (chương 10). Sổ tay theo <b>luật chính thức</b>; bản mod xây nhanh hơn, bán hoàn 100%, bỏ Harrier, thêm 51 quân. Chỉ số: <b>$</b> giá, <b>Máu</b> độ bền, <b>Tốc độ</b> theo thang game (bộ binh ~4, máy bay ~14).</div></section>

<h2 class="sec" style="margin-top:5mm">1. Bắt đầu chơi với Ra2026</h2>
<ol class="steps">
<li>Mở thư mục <b>E:\\games\\Ra2\\Ra2026</b>.</li>
<li>Bấm đúp <b>Play_YR.exe</b> để chơi <b>Yuri's Revenge</b> (có phe Yuri, khuyên dùng), hoặc <b>Play_RA2.exe</b> để chơi Red Alert 2 gốc (2 phe).</li>
<li>Ở menu chính chọn <b>Skirmish</b> để đánh với máy, <b>Campaign</b> để chơi cốt truyện, <b>LAN</b> để chơi mạng nội bộ.</li>
<li>Không mở trực tiếp game.exe hay gamemd.exe: game sẽ tự tắt.</li></ol>
<h3>Thiết lập trận Skirmish</h3>
<table class="t"><tr><th>Tùy chọn</th><th>Ý nghĩa</th></tr>
<tr><td><b>Credits</b></td><td>Tiền khởi đầu. Mới chơi nên để 10.000 (muốn nhiều hơn: xem chương Thủ thuật).</td></tr>
<tr><td><b>Unit Count</b></td><td>Số quân được tặng lúc bắt đầu.</td></tr>
<tr><td><b>Game Speed</b></td><td>Tốc độ trận đấu; mới chơi nên chọn chậm.</td></tr>
<tr><td><b>Short Game</b></td><td>Phá hết công trình của đối phương là thắng, không cần diệt sạch quân.</td></tr>
<tr><td><b>Superweapons</b></td><td>Bật hoặc tắt siêu vũ khí.</td></tr>
<tr><td><b>MCV Repacks</b></td><td>Cho phép thu Construction Yard về thành xe MCV để dời căn cứ.</td></tr>
<tr><td><b>Crates</b></td><td>Hộp quà ngẫu nhiên trên bản đồ.</td></tr>
<tr><td><b>Build off Ally</b></td><td>Được xây sát căn cứ đồng minh.</td></tr>
<tr><td><b>AI: Easy / Medium / Brutal</b></td><td>Độ khó của máy. Tập với 1 máy Easy trước rồi tăng dần.</td></tr></table>

<section class="pb"><h2 class="sec">2. Màn hình & điều khiển</h2>
<p><b>Bản đồ chính</b> chiếm phần lớn màn hình. Bên phải là <b>thanh bên (sidebar)</b> gồm radar mini, số tiền, thanh điện và các tab xây dựng: <b>Công trình · Phòng thủ · Bộ binh · Xe</b>.</p>
<ol class="steps">
<li><b>Xây công trình:</b> click biểu tượng ở tab Công trình. Đợi đếm ngược xong ("Construction complete"), click lần nữa rồi đặt lên bản đồ ở chỗ hiện ô xanh.</li>
<li><b>Huấn luyện quân:</b> click biểu tượng ở tab Bộ binh hoặc Xe. Click nhiều lần để xếp hàng; <b>Shift + click</b> để thêm 5 một lúc. Chuột phải vào biểu tượng để tạm dừng hoặc hủy.</li>
<li><b>Ra lệnh:</b> chọn quân rồi click vào đất để di chuyển, click vào địch để tấn công.</li>
<li><b>Radar mini</b> chỉ hoạt động khi có công trình radar và đủ điện.</li>
<li>Icon tối màu nghĩa là thiếu điều kiện (chưa có công trình cần thiết); con số trên icon là số lượng đang chờ.</li></ol>
<h3>3. Phím tắt</h3>{keys}
</section>

<section class="pb"><h2 class="sec">4. Kinh tế, điện & lên cấp</h2>
<h3>Tiền đến từ quặng</h3>
<p>Xe khai thác đào <b>quặng</b> (vàng) hoặc <b>đá quý</b> (tinh thể nhiều màu, giá trị cao hơn) rồi đổ về nhà máy lọc để thành tiền. Mỏ quặng mọc lại chậm quanh các giếng quặng.</p>
<table class="t"><tr><th>Phe</th><th>Cách khai thác</th></tr>
<tr><td><b style="color:#1f5fae">Đồng Minh</b></td><td>Chrono Miner tự dịch chuyển về nhà máy lọc. Ore Purifier thêm <b>+25%</b> mỗi lượt giao quặng.</td></tr>
<tr><td><b style="color:#b3261e">Liên Xô</b></td><td>War Miner giáp dày, có súng máy tự vệ. Industrial Plant giảm giá xe.</td></tr>
<tr><td><b style="color:#6a35a8">Yuri</b></td><td>Slave Miner triển khai thành nhà máy lọc ngay tại bãi quặng, nô lệ ra đào. Grinder nghiền lính thành tiền.</td></tr></table>
<p>Ngoài ra: chiếm <b>Oil Derrick</b> (giếng dầu) để có thêm thu nhập; bán công trình được hoàn <b>50%</b> giá.</p>
<h3>Điện</h3>
<p>Khi điện sinh ra ít hơn điện dùng, thanh điện chuyển đỏ: xây chậm lại, radar tắt, các tháp cần điện (Prism, Tesla Coil, Patriot...) ngừng hoạt động.</p>
<table class="t"><tr><th>Nhà máy điện</th><th class="num">Điện</th><th class="num">Giá</th></tr>
<tr><td>Power Plant (Đồng Minh)</td><td class="num">+200</td><td class="num">$800</td></tr>
<tr><td>Tesla Reactor (Liên Xô)</td><td class="num">+150</td><td class="num">$600</td></tr>
<tr><td>Nuclear Reactor (Liên Xô, cần Battle Lab)</td><td class="num">+2000</td><td class="num">$1,000</td></tr>
<tr><td>Bio Reactor (Yuri; tăng điện khi có bộ binh bên trong)</td><td class="num">+150</td><td class="num">$600</td></tr>
<tr><td>Tech Power Plant (công trình trung lập, phải chiếm)</td><td class="num">+200</td><td class="num">–</td></tr></table>
<h3>Lên cấp (Veterancy)</h3>
<p>Quân lên cấp khi tiêu diệt kẻ địch có tổng giá trị gấp <b>3 lần</b> giá của chính nó.</p>
<table class="t"><tr><th>Cấp</th><th>Hiệu ứng (theo rulesmd.ini)</th></tr>
<tr><td><b>Cựu binh</b> (1 vạch)</td><td>Giáp ×1.5, tốc độ ×1.2, bắn nhanh hơn (ROF ×0.6).</td></tr>
<tr><td><b>Tinh nhuệ</b> (ngôi sao)</td><td>Thêm sát thương ×1.1 và tự hồi máu; nhiều quân được đổi sang vũ khí tinh nhuệ mạnh hơn.</td></tr></table>
<h3>Hộp quà (crate)</h3><p>Khi bật Crates, hộp gỗ rơi ngẫu nhiên trên bản đồ. Cho quân chạm vào để nhận một trong các phần thưởng: <b>+$2000</b>, giáp ×1.5, hỏa lực ×2, tốc độ ×1.2, lên một cấp, hồi máu toàn bộ quân, lộ bản đồ hoặc được tặng quân.</p>
</section>

{side_section('A')}
{side_section('S')}
{side_section('Y')}

<section class="pb"><h2 class="sec">8. Siêu vũ khí</h2>
<p>Công trình siêu vũ khí cần Battle Lab và tốn rất nhiều điện. Khi xây xong, đồng hồ đếm ngược hiện ở góc màn hình <b>cho tất cả người chơi</b> thấy. Thời gian hồi chiêu lấy từ rulesmd.ini.</p>
{sw_table()}
<div class="note warn">Phòng thủ trước siêu vũ khí: rải căn cứ ra, đừng dồn quân một chỗ khi đồng hồ địch sắp về 0, và dùng Gián điệp đặt lại đồng hồ của địch.</div>

<h2 class="sec" style="margin-top:5mm">9. Gián điệp, IFV & công trình trung lập</h2>
<h3>Gián điệp (Spy) xâm nhập vào...</h3>{table(SPY, 'Công trình địch', 'Hiệu quả')}
<h3>IFV: ai ngồi trong thì đổi vũ khí</h3>{table(IFV, 'Bộ binh trong IFV', 'IFV trở thành')}
<h3>Công trình trung lập (dùng Kỹ sư chiếm)</h3>{tech_table()}
</section>

<section class="pb"><h2 class="sec">10. Thủ thuật</h2>
<h3>Thủ thuật trong trận</h3>
{tipgrid(TRICKS, True)}
<h3 style="margin-top:5mm">Thủ thuật với game & chỉnh sửa</h3>
{tipgrid(SYSTRICKS)}
</section>

<section class="pb"><h2 class="sec">11. Bảng khắc chế</h2>{table(COUNTER, 'Đối phương dùng...', 'Hãy đáp trả bằng')}
<h3 style="margin-top:4mm">14 mẹo chiến thuật</h3>{tipgrid(TIPS)}</section>

<section class="pb"><h2 class="sec">12. Bảng tra cứu nhanh</h2>
<p>Toàn bộ {n_items} đơn vị và công trình xây được trong Skirmish/LAN của Yuri's Revenge, xếp theo phe, loại và giá. Cột <b>Mã</b> là tên dùng trong rulesmd.ini (cần khi tự mod).</p>
{quickref()}
<p class="foot">Ngoài ra còn 3 quân chỉ mở được bằng Gián điệp: Chrono Commando (Battle Lab Đồng Minh, $2,000), Chrono Ivan (Battle Lab Liên Xô, $1,750), Psi Commando (Battle Lab Yuri, $1,000).</p>
</section>
</body></html>"""
    open(W + '/guide.html', 'w').write(doc)
    print('html', len(doc) // 1024, 'KB')

build()
