import sys, pickle, struct, json, re
sys.path.insert(0, sys.argv[1]); import shp
W=sys.argv[1]
s=pickle.load(open(W+'/store.pkl','rb'))
def ini(b):
    d={}; cur=None
    for line in b.decode('latin-1').splitlines():
        line=line.split(';')[0].strip()
        if not line: continue
        if line.startswith('['): cur=line[1:line.index(']')]; d.setdefault(cur,{}); continue
        if '=' in line and cur is not None:
            k,v=line.split('=',1); d[cur][k.strip()]=v.strip()
    return d
def csf(b):
    out={}; p=24; n=struct.unpack_from('<I',b,8)[0]
    for _ in range(n):
        if b[p:p+4]!=b' LBL': break
        cnt,ln=struct.unpack_from('<II',b,p+4); name=b[p+12:p+12+ln].decode('latin-1'); p+=12+ln
        val=''
        for i in range(cnt):
            t=b[p:p+4]; L=struct.unpack_from('<I',b,p+4)[0]; raw=b[p+8:p+8+L*2]; p+=8+L*2
            val=bytes((~c)&0xff for c in raw).decode('utf-16le')
            if t==b'WRTS': L2=struct.unpack_from('<I',b,p)[0]; p+=4+L2
        out[name.upper()]=val
    return out
R=ini(s[('expandmd01.mix','rulesmd.ini')]); A=ini(s[('localmd.mix','artmd.ini')])
S=csf(s[('langmd.mix','ra2md.csf')])
cams={}
for (m,f),d in s.items():
    if m in('cameo.mix','cameomd.mix') and f.endswith('.shp'): cams.setdefault(f[:-4].lower(),(m,f))
items=[]
for cat in ['InfantryTypes','VehicleTypes','AircraftTypes','BuildingTypes']:
    for k,idv in R.get(cat,{}).items():
        sec=R.get(idv,{}); 
        if not sec: continue
        tl=int(sec.get('TechLevel','-1') or -1)
        if tl<1 or tl>10: continue
        img=sec.get('Image',idv); art=A.get(img,{}) or A.get(idv,{})
        cam=(art.get('Cameo') or '').lower()
        ui=sec.get('UIName','')
        items.append(dict(id=idv,cat=cat,name=S.get(ui.upper(),sec.get('Name',idv)),owner=sec.get('Owner',''),
            cost=sec.get('Cost',''),hp=sec.get('Strength',''),speed=sec.get('Speed',''),armor=sec.get('Armor',''),
            prereq=sec.get('Prerequisite',''),tl=tl,cameo=cam,has=cam in cams,power=sec.get('Power',''),
            req=sec.get('RequiredHouses',''),forb=sec.get('ForbiddenHouses',''),
            primary=sec.get('Primary',''),elite=sec.get('ElitePrimary',''),sight=sec.get('Sight',''),
            ammo=sec.get('Ammo',''),crew=sec.get('Crewed',''),super=sec.get('SuperWeapon','')))
json.dump(items,open(W+'/items.json','w'),ensure_ascii=False,indent=0)
print(len(items))
for it in items: print(it['cat'][:3],it['id'],'|',it['name'],'|',it['owner'][:40],'|',it['cost'],it['hp'],it['speed'],'|',it['cameo'],it['has'],'| req',it['req'],'forb',it['forb'])
# sides & countries
print(R.get('Sides'))
for c in R.get('Countries',{}).values(): print(c, R.get(c,{}).get('Side'), S.get(R.get(c,{}).get('UIName','').upper()), R.get(c,{}).get('Multiplay'))
json.dump({k:R[k] for k in R if k in('General','CombatDamage','AudioVisual','SpecialWeapons') or k in [v for v in R.get('SuperWeaponTypes',{}).values()]},open(W+'/rules_misc.json','w'),indent=0)
print('SW', [(v, S.get(R.get(v,{}).get('UIName','').upper()), R.get(v,{}).get('RechargeTime')) for v in R.get('SuperWeaponTypes',{}).values()])
