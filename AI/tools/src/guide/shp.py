import struct
from PIL import Image
def pal(b): return [min(255,c*4) for c in b[:768]]
def decode(data, palb, frame=0, transparent=True):
    _,W,H,N=struct.unpack_from('<4H',data,0)
    o=8+frame*24
    x,y,w,h,flags=struct.unpack_from('<4HI',data,o)
    off=struct.unpack_from('<I',data,o+20)[0]
    buf=bytearray(W*H)
    if w and h and off:
        comp=flags&0xff
        p=off
        for r in range(h):
            if comp in (1,2) and not (flags & 2):
                line=data[p:p+w]; p+=w
            elif comp==3 or (flags & 2):
                ln=struct.unpack_from('<H',data,p)[0]; q=p+2; end=p+ln; line=bytearray()
                while q<end and len(line)<w:
                    c=data[q]; q+=1
                    if c==0: line+=bytes(data[q]); q+=1
                    else: line.append(c)
                p=end; line=bytes(line[:w]).ljust(w,b'\0')
            else:
                line=data[p:p+w]; p+=w
            buf[(y+r)*W+x:(y+r)*W+x+w]=line
    im=Image.frombytes('P',(W,H),bytes(buf)); im.putpalette(pal(palb))
    im=im.convert('RGBA') if transparent else im.convert('RGB')
    if transparent:
        px=[ (0,0,0,0) if i==0 else None for i in buf]
        d=im.getdata(); im.putdata([ (0,0,0,0) if buf[i]==0 else d[i] for i in range(len(buf))])
    return im
