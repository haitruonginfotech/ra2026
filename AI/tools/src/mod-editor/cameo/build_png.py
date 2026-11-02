
import sys, pickle, json, io, base64, struct
from PIL import Image, ImageChops, ImageStat
found,pals=pickle.load(open('cameos.pkl','rb'))
palb=pals['cameo.pal'][0][1]; P=[min(255,c*4) for c in palb[:768]]
old=json.load(open('old_icons.json'))
def idx(data):
    _,W,H,N=struct.unpack_from('<4H',data,0)
    x,y,w,h,flags=struct.unpack_from('<4HI',data,8); off=struct.unpack_from('<I',data,28)[0]
    buf=bytearray(W*H)
    if w and h and off:
        comp=flags&0xff; p=off
        for r in range(h):
            if comp==3 or (flags & 2):
                ln=struct.unpack_from('<H',data,p)[0]; q=p+2; end=p+ln; line=bytearray()
                while q<end and len(line)<w:
                    c=data[q]; q+=1
                    if c==0: line+=bytes(data[q]); q+=1
                    else: line.append(c)
                p=end; line=bytes(line[:w]).ljust(w,b'\0')
            else:
                line=data[p:p+w]; p+=w
            buf[(y+r)*W+x:(y+r)*W+x+w]=line
    im=Image.frombytes('P',(W,H),bytes(buf)); im.putpalette(P); return im
out={}; tot=0; diffs=[]
for k,cands in found.items():
    oim=Image.open(io.BytesIO(base64.b64decode(old[k]))).convert('RGB'); best=None
    for s,d in cands:
        try: im=idx(d)
        except Exception: continue
        c=im.convert('RGB'); c=c.resize(oim.size) if c.size!=oim.size else c
        df=sum(ImageStat.Stat(ImageChops.difference(c,oim)).mean)/3
        if best is None or df<best[0]: best=(df,s,im)
    df,s,im=best; diffs.append(df)
    buf=io.BytesIO(); im.save(buf,'PNG',optimize=True,transparency=0); out[k]=base64.b64encode(buf.getvalue()).decode(); tot+=len(out[k])
print('icons',len(out),'b64 total',tot,'max diff',round(max(diffs),1),'median',round(sorted(diffs)[len(diffs)//2],1))
json.dump(out,open('new_icons.json','w'))
