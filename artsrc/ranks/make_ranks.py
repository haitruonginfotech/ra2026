"""Vẽ huy hiệu 4 bậc của RA Reborn (16x16, PNG 8-bit dùng chung 1 bảng màu).
Bậc 1 Tân binh: không huy hiệu. Bậc 2 Đồng, bậc 3 Vàng, bậc 4 Kim cương.
Chạy: python make_ranks.py <thư mục ra>"""
import sys, os
from PIL import Image, ImageDraw
out = sys.argv[1] if len(sys.argv) > 1 else '.'
S = 16
# bảng màu: 0 trong suốt, 1 viền tối, sau đó các tông đồng / vàng / kim cương
PAL = [(0,0,0),(20,16,12),
       (110,58,28),(166,94,48),(214,140,82),(245,196,140),      # đồng: tối -> sáng (2..5)
       (128,92,10),(196,150,20),(244,204,52),(255,244,170),     # vàng (6..9)
       (20,70,120),(40,140,200),(110,210,245),(210,245,255),(255,255,255)]  # kim cương (10..14)
flat = [c for rgb in PAL for c in rgb] + [0]*(768-3*len(PAL))

def chevron(d, y, dark, mid, light):
    # chữ V dày 3 px, rộng 14 px, có viền
    pts = [(1,y),(8,y+5),(15,y),(15,y+3),(8,y+8),(1,y+3)]
    d.polygon(pts, fill=1)                                      # viền
    d.polygon([(2,y+1),(8,y+5),(14,y+1),(14,y+2),(8,y+6),(2,y+2)], fill=mid)
    d.line([(2,y+1),(8,y+5)], fill=light); d.line([(8,y+5),(14,y+1)], fill=dark)

def img():
    im = Image.new('P', (S, S), 0); im.putpalette(flat); im.info['transparency'] = 0
    return im, ImageDraw.Draw(im)

bronze, d = img(); chevron(d, 4, 2, 3, 5)
gold, d = img(); chevron(d, 1, 6, 7, 9); chevron(d, 7, 6, 8, 9)
diamond, d = img()
d.polygon([(4,2),(11,2),(15,6),(7.5,14),(0,6)], fill=1)                 # viền viên đá
d.polygon([(4,3),(11,3),(14,6),(7.5,13),(1,6)], fill=11)
d.polygon([(4,3),(7.5,3),(5,6),(1,6)], fill=12); d.polygon([(7.5,3),(11,3),(14,6),(10,6)], fill=10)
d.polygon([(5,6),(10,6),(7.5,13)], fill=12); d.polygon([(1,6),(5,6),(7.5,13)], fill=13); d.polygon([(10,6),(14,6),(7.5,13)], fill=10)
d.line([(5,4),(6,4)], fill=14); d.point((12,1), fill=14); d.point((13,2), fill=13)   # lấp lánh
for name, im in [('rank-bronze', bronze), ('rank-gold', gold), ('rank-diamond', diamond)]:
    im.save(os.path.join(out, name + '.png'), transparency=0)
# ảnh xem trước x8 trên nền giống bản đồ
prev = Image.new('RGB', (3*(S*8+24)+24, S*8+48), (74,84,64))
for i, im in enumerate([bronze, gold, diamond]):
    big = im.convert('RGBA').resize((S*8, S*8), Image.NEAREST); prev.paste(big, (24+i*(S*8+24), 24), big)
prev.save(os.path.join(out, 'preview.png'))
