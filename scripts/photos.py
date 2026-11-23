"""Рабочие копии кадров для сайта: content/ -> src/assets/photos/ и public/video/. Оригиналы не меняются.
Волосы, лица и кожа не правятся: только копия, кроп и уменьшение. Запуск: python scripts/photos.py
"""
import os, subprocess
from PIL import Image

ROOT = os.path.join(os.path.dirname(__file__), '..')
B = os.path.join(ROOT, 'content/photos/best')
POSTS = os.path.join(ROOT, 'content/instagram/posts')
OUT = os.path.join(ROOT, 'src/assets/photos')
VID = os.path.join(ROOT, 'public/video')
os.makedirs(OUT, exist_ok=True); os.makedirs(VID, exist_ok=True)
STORY = (0.045, 0.025, 0.955, 0.975)  # срезать скруглённые углы кадра сторис

def save(im, name, box=None, maxside=None):
    w, h = im.size
    if box: im = im.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)))
    if maxside and max(im.size) > maxside: im.thumbnail((maxside, maxside), Image.LANCZOS)
    im.save(os.path.join(OUT, name), quality=92); print(name, im.size)

def copy(src, name, box=None, maxside=None):
    """box в долях (x0, y0, x1, y1)."""
    save(Image.open(os.path.join(B, src)).convert('RGB'), name, box, maxside)

def frame(video, t, name, box=None):
    tmp = os.path.join(OUT, '_tmp.jpg')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', str(t), '-i', os.path.join(POSTS, video), '-frames:v', '1', '-q:v', '2', tmp], check=True)
    im = Image.open(tmp).convert('RGB'); im.load(); os.remove(tmp)
    save(im, name, box)

def loop(video, start, dur, name, poster_at=None):
    """Немой цикл: 720p как в исходнике и лёгкая версия 540p для телефона. Постер: кадр poster_at или первый кадр."""
    src = os.path.join(POSTS, video)
    for suffix, vf, crf in (('', 'format=yuv420p', '27'), ('-m', 'scale=540:960,format=yuv420p', '29')):
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', str(start), '-t', str(dur), '-i', src, '-an', '-vf', vf,
                        '-c:v', 'libx264', '-crf', crf, '-preset', 'slow', '-movflags', '+faststart',
                        os.path.join(VID, name + suffix + '.mp4')], check=True)
    frame(video, poster_at if poster_at is not None else start, name + '.jpg')

# Первый экран: видео в зеркале. Четыре варианта на выбор Остапа, после выбора остаётся один
loop('2026-10-27_DfAHoF7oCXH_01.mp4', 20.6, 6.0, 'hero-1')   # догляд Braé, очень длинные волосы, новый зал
loop('2026-11-18_Df5Op2CsO0y_01.mp4', 17.95, 2.5, 'hero-2')  # корекція AirTouch, блонд, стена с логотипом
loop('2026-09-15_DdUGHH_M7t2_01.mp4', 8.2, 5.0, 'hero-3')    # тёмные длинные, взмах: волосы самой колористки
loop('2026-07-29_DbXa_arB5dd_01.mp4', 12.2, 5.2, 'hero-4')   # платиновый блонд, старый зал

# Роботи: серия со спины в зале студии
frame('2026-11-13_Dfsj8hiMGny_01.mp4', 6.0, 'robota-1.jpg')  # AirTouch, кадр результата в новом зале
copy('color/2026-11-01_DfME0fUB0Be_01.jpg', 'robota-2.jpg')
copy('color/2026-10-28_DfB1CynBbcq_01.jpg', 'robota-3.jpg')
copy('color/2026-11-12_Dfo6sDTMz72_01.jpg', 'robota-4.jpg')
copy('color/2026-10-22_DezSzLlKM-M_01.jpg', 'robota-5.jpg', STORY)
copy('color/2026-10-05_DeGw3-UMB-Z_01.jpg', 'robota-6.jpg')

# До і після
# 1. AirTouch, 12.11.2026
copy('before-after/2026-11-12_Dfpir2pCN-p_03.jpg', 'do-1.jpg', (0, 0, 1, 0.9))
copy('before-after/2026-11-12_Dfpir2pCN-p_01.jpg', 'pislia-1.jpg', (0, 0, 1, 0.9))
# 2. Корекція AirTouch, 18.11.2026: «до» из рилса (субтитр лежит ниже 60 % высоты, срезан кропом), «після» с обложки
frame('2026-11-18_Df5Op2CsO0y_01.mp4', 2.6, 'do-2.jpg', (0, 0.05, 1, 0.60))
copy('interior/2026-11-18_Df5Op2CsO0y_01.jpg', 'pislia-2.jpg', (0.12, 0.25, 0.88, 0.785))
# 3. «Відмовили у блонді», 17.11.2026: субтитры рилса лежат ниже 76 % высоты кадра, срезаны кропом
frame('2026-11-17_Df2AUtxsKLA_01.mp4', 1.0, 'do-3.jpg', (0, 0, 1, 0.75))
frame('2026-11-17_Df2AUtxsKLA_01.mp4', 17.5, 'pislia-3.jpg', (0, 0, 1, 0.75))

# Власниця, сертификаты, догляд, образ, фото для страницы цен
copy('team/2026-01-16_DTkDnqQDJwX_01.jpg', 'olha.jpg')
copy('team/2026-08-02_Dbhz5d_DGJG_02.jpg', 'sertyfikaty.jpg', maxside=1600)
frame('2026-09-21_DdiZ18iu_ov_01.mp4', 7.6, 'dohliad.jpg')
copy('makeup/2026-06-22_DZ4JlJuuSzh_01.jpg', 'obraz.jpg', STORY)
copy('color/2026-09-17_DdYGrHNuG3c_01.jpg', 'tsiny.jpg', STORY)
