import sys, ra2mix, io, contextlib, os, json, pickle
U='/mnt/user-data/uploads/Ra2/Ra2026/'
keys=set(json.load(open('keys.json')))
found={}   # name -> list of (mix, data)
pals={}
def read(data):
    with contextlib.redirect_stdout(io.StringIO()):
        return ra2mix.read(mix_data=data)
def walk(name, data, chain):
    try: fm=read(data)
    except Exception as e: return
    for fn,d in fm.items():
        l=fn.lower()
        if l.endswith('.mix'): walk(l,d,chain+[l])
        elif l.endswith('.shp') and l[:-4] in keys: found.setdefault(l[:-4],[]).append(('/'.join(chain+[l]),d))
        elif l in ('cameo.pal','cameomd.pal'): pals.setdefault(l,[]).append(('/'.join(chain),d))
for top in sorted(os.listdir(U)):
    if top.lower().endswith('.mix'): walk(top.lower(), open(U+top,'rb').read(), [top.lower()])
print('found', len(found), 'of', len(keys)); print('missing', sorted(keys-set(found))[:20])
print({k:[c for c,_ in v] for k,v in pals.items()})
import collections; print(collections.Counter(v[-1][0].split('/')[0] for v in found.values()))
pickle.dump((found,pals), open('cameos.pkl','wb'))
