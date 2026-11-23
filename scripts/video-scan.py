"""Обзор видео: по 10 кадров из каждого ролика строкой. python scripts/video-scan.py <out_prefix> <mp4>..."""
import sys, os, subprocess, tempfile
from PIL import Image, ImageDraw
out, vids = sys.argv[1], sys.argv[2:]
N, W, H, LAB, PER = 10, 150, 267, 16, 6
tmp = tempfile.mkdtemp()
rows = []
for v in vids:
    try:
        dur = float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',v],capture_output=True,text=True).stdout.strip())
    except ValueError:
        continue
    p = os.path.join(tmp, 'r.jpg')
    subprocess.run(['ffmpeg','-y','-v','error','-i',v,'-vf',f'fps={N/dur:.5f},scale={W}:{H},tile={N}x1','-frames:v','1',p])
    if os.path.exists(p):
        rows.append((os.path.basename(v), dur, Image.open(p).copy())); os.remove(p)
for n in range(0, len(rows), PER):
    chunk = rows[n:n+PER]
    sheet = Image.new('RGB', (N*W, len(chunk)*(H+LAB)), '#222'); d = ImageDraw.Draw(sheet)
    for k,(name,dur,im) in enumerate(chunk):
        sheet.paste(im, (0, k*(H+LAB)+LAB)); d.text((4, k*(H+LAB)+2), f"{name}  {dur:.1f}s  (кадр i ≈ {dur/N:.1f}s·(i+0.5))", fill='#fff')
    p = f"{out}-{n//PER+1:02d}.jpg"; sheet.save(p, quality=80); print(p)
