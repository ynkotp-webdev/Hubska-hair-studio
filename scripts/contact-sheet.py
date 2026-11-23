"""Контактные листы: python scripts/contact-sheet.py <out_prefix> <file-or-dir>... [--cols 5 --rows 3]"""
import sys, os, glob
from PIL import Image, ImageDraw, ImageOps

args = sys.argv[1:]
cols, rows = 5, 3
if '--cols' in args: i = args.index('--cols'); cols = int(args[i+1]); del args[i:i+2]
if '--rows' in args: i = args.index('--rows'); rows = int(args[i+1]); del args[i:i+2]
out, srcs = args[0], args[1:]
files = []
for s in srcs:
    files += sorted(glob.glob(os.path.join(s, '*.jpg'))) if os.path.isdir(s) else [s]
TW, TH, LAB = 300, 533, 22
per = cols * rows
for n in range(0, len(files), per):
    sheet = Image.new('RGB', (cols * TW, rows * (TH + LAB)), '#222')
    d = ImageDraw.Draw(sheet)
    for k, f in enumerate(files[n:n + per]):
        im = ImageOps.exif_transpose(Image.open(f)).convert('RGB')
        w, h = im.size
        im.thumbnail((TW - 4, TH - 4))
        x, y = (k % cols) * TW, (k // cols) * (TH + LAB)
        sheet.paste(im, (x + (TW - im.width) // 2, y + (TH - im.height) // 2))
        d.text((x + 4, y + TH + 4), f"{n + k + 1} {os.path.basename(f)[:34]} {w}x{h}", fill='#fff')
    p = f"{out}-{n // per + 1:02d}.jpg"
    sheet.save(p, quality=82)
    print(p)
