"""Đóng gói ảnh cameo đã phóng bằng Real-ESRGAN (thư mục up4b/*.png, 240×192) thành WebP base64
và thay khóa `icons` trong data.js của Mod Editor.
Dùng: python pack_webp.py <thư mục ảnh> <data.js vào> <data.js ra>"""
import sys, os, io, json, base64
from PIL import Image

src, din, dout = sys.argv[1:4]
pre = 'window.RA2DATA='
text = open(din, encoding='utf-8').read()
assert text.startswith(pre)
data = json.loads(text[len(pre):].rstrip().rstrip(';'))
icons = {}
for k in data['icons']:
    im = Image.open(os.path.join(src, k + '.png')).convert('RGBA')
    b = io.BytesIO()
    im.save(b, 'WEBP', quality=80, method=6)
    icons[k] = base64.b64encode(b.getvalue()).decode()
assert set(icons) == set(data['icons'])
data['icons'] = icons
open(dout, 'w', encoding='utf-8').write(pre + json.dumps(data, separators=(',', ':'), ensure_ascii=False) + ';')
print('icons', len(icons), 'b64 MB', round(sum(map(len, icons.values())) / 1e6, 2))
