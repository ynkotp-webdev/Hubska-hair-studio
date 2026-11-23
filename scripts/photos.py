"""Рабочие копии кадров для сайта: content/ -> src/assets/photos/. Оригиналы не меняются.
Волосы, лица и кожа не правятся: только копия, кроп и уменьшение. Запуск: python scripts/photos.py
"""
import os, subprocess, shutil
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), '..')
B = os.path.join(ROOT, 'content/photos/best')
POSTS = os.path.join(ROOT, 'content/instagram/posts')
OUT = os.path.join(ROOT, 'src/assets/photos')
VID = os.path.join(ROOT, 'public/video')
os.makedirs(OUT, exist_ok=True); os.makedirs(VID, exist_ok=True)

def copy(src, name, box=None, maxside=None):
    """box в долях (x0, y0, x1, y1)."""
    im = Image.open(os.path.join(B, src)).convert('RGB'); w, h = im.size
    if box: im = im.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)))
    if maxside and max(im.size) > maxside: im.thumbnail((maxside, maxside), Image.LANCZOS)
    im.save(os.path.join(OUT, name), quality=92); print(name, im.size)

def frame(video, t, name, box=None):
    tmp = os.path.join(OUT, '_tmp.jpg')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', str(t), '-i', os.path.join(POSTS, video), '-frames:v', '1', '-q:v', '2', tmp], check=True)
    im = Image.open(tmp).convert('RGB'); w, h = im.size
    if box: im = im.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)))
    im.save(os.path.join(OUT, name), quality=92); os.remove(tmp); print(name, im.size)

def loop(video, start, dur, name):
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', str(start), '-t', str(dur), '-i', os.path.join(POSTS, video), '-an',
                    '-vf', 'format=yuv420p', '-c:v', 'libx264', '-crf', '27', '-preset', 'slow', '-movflags', '+faststart',
                    os.path.join(VID, name + '.mp4')], check=True)
    # лёгкая версия для телефона
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', str(start), '-t', str(dur), '-i', os.path.join(POSTS, video), '-an',
                    '-vf', 'scale=540:960,format=yuv420p', '-c:v', 'libx264', '-crf', '29', '-preset', 'slow', '-movflags', '+faststart',
                    os.path.join(VID, name + '-m.mp4')], check=True)
    frame(video, start, name + '.jpg')

import sys
if '--video' in sys.argv:
  loop('2026-09-15_DdUGHH_M7t2_01.mp4', 8.2, 5.0, 'hero-1')
  loop('2026-07-29_DbXa_arB5dd_01.mp4', 12.2, 5.2, 'hero-2')
  loop('2026-07-31_DbclHnRhwVy_01.mp4', 9.3, 4.5, 'hero-3')
  loop('2026-08-14_DcAqj4lBxAl_01.mp4', 9.0, 5.0, 'hero-4')

# Роботи: серия со спины на одной стене зала
copy('interior/2026-11-18_Df5Op2CsO0y_01.jpg', 'robota-1.jpg')
copy('color/2026-11-01_DfME0fUB0Be_01.jpg', 'robota-2.jpg')
copy('color/2026-10-28_DfB1CynBbcq_01.jpg', 'robota-3.jpg')
copy('color/2026-11-12_Dfo6sDTMz72_01.jpg', 'robota-4.jpg')
copy('color/2026-10-22_DezSzLlKM-M_01.jpg', 'robota-5.jpg', (0.045, 0.025, 0.955, 0.975))  # срезаны скруглённые углы сторис
copy('color/2026-10-05_DeGw3-UMB-Z_01.jpg', 'robota-6.jpg')

# До і після
copy('before-after/2026-11-12_Dfpir2pCN-p_03.jpg', 'do-1.jpg', (0, 0, 1, 0.9))
copy('before-after/2026-11-12_Dfpir2pCN-p_01.jpg', 'pislia-1.jpg', (0, 0, 1, 0.9))
# Случай «відмовили у блонді»: субтитры рилса лежат ниже 76 % высоты кадра, срезаны кропом
frame('2026-11-17_Df2AUtxsKLA_01.mp4', 1.0, 'do-2.jpg', (0, 0, 1, 0.75))
frame('2026-11-17_Df2AUtxsKLA_01.mp4', 17.5, 'pislia-2.jpg', (0, 0, 1, 0.75))

# Власниця, сертификаты, образ, стена с логотипом, фото для страницы цен
copy('team/2026-01-16_DTkDnqQDJwX_01.jpg', 'olha.jpg')
copy('team/2026-08-02_Dbhz5d_DGJG_02.jpg', 'sertyfikaty.jpg', maxside=1600)
copy('makeup/2026-06-22_DZ4JlJuuSzh_01.jpg', 'obraz.jpg', (0.045, 0.025, 0.955, 0.975))
copy('brand/2026-11-03_DfSSXb4s4Xt_01.jpg', 'stina.jpg')
copy('color/2026-09-17_DdYGrHNuG3c_01.jpg', 'tsiny.jpg', (0.045, 0.025, 0.955, 0.975))
