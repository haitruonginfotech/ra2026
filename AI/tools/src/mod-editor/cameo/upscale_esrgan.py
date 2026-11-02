import sys, json, io, base64, torch, numpy as np
from PIL import Image
from spandrel import ModelLoader

# Phóng to cameo x4 bằng Real-ESRGAN (spandrel nạp trọng số với weights_only).
torch.set_num_threads(2)
model = ModelLoader().load_from_file(sys.argv[1]).eval()
icons = json.load(open('new_icons.json'))
names = sys.argv[3].split(',') if len(sys.argv) > 3 and sys.argv[3] else list(icons)
for i, n in enumerate(names):
    im = Image.open(io.BytesIO(base64.b64decode(icons[n]))).convert('RGBA')
    rgb = np.asarray(im.convert('RGB'), dtype=np.float32) / 255
    # tô vùng trong suốt (màu nền xanh của palette) bằng màu điểm kề bên để AI không loang màu xanh vào mép
    a = np.asarray(im.getchannel('A')) > 0
    if (~a).any() and a.any():
        rgb = rgb.copy(); filled = a.copy()
        for _ in range(8):
            if filled.all(): break
            acc = np.zeros_like(rgb); cnt = np.zeros(filled.shape, np.float32)
            for dy, dx in ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)):
                m = np.roll(filled, (dy, dx), (0, 1)); v = np.roll(rgb, (dy, dx), (0, 1))
                acc += v * m[..., None]; cnt += m
            new = (~filled) & (cnt > 0)
            rgb[new] = acc[new] / cnt[new][:, None]; filled |= new
    x = torch.from_numpy(rgb).permute(2, 0, 1)[None]
    with torch.no_grad():
        y = model(x)[0].clamp(0, 1).permute(1, 2, 0).numpy()
    up = Image.fromarray((y * 255).round().astype(np.uint8))
    up.putalpha(im.getchannel('A').resize(up.size, Image.NEAREST))
    up.save(f'{sys.argv[2]}/{n}.png')
    if i % 50 == 0:
        print(i, n, up.size, flush=True)
