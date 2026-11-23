"""AI-правка фрагмента кадра через OpenRouter. Ключ берётся из .env и никуда не печатается.

В модель уходит только вырезанный фрагмент (без лиц и волос, где это возможно); обратно в кадр
вклеивается только область box с растушёвкой, остальные пиксели остаются оригиналом.

python scripts/ai-edit.py <src> <out> <x0,y0,x1,y1> "<что сделать>" [--pad 140] [--model google/gemini-3-pro-image]
"""
import sys, os, io, json, base64, urllib.request
from PIL import Image, ImageDraw, ImageFilter

args = sys.argv[1:]
def opt(name, default):
    if name in args:
        i = args.index(name); v = args[i + 1]; del args[i:i + 2]; return v
    return default
model = opt('--model', 'google/gemini-3-pro-image')
pad = int(opt('--pad', 140))
feather = int(opt('--feather', 18))
src, out, box, prompt = args[0], args[1], [int(v) for v in args[2].split(',')], args[3]

root = os.path.join(os.path.dirname(__file__), '..')
key = next(l.split('=', 1)[1].strip() for l in open(os.path.join(root, '.env')) if l.startswith('OPENROUTER_API_KEY='))

im = Image.open(src).convert('RGB')
cx0, cy0 = max(0, box[0] - pad), max(0, box[1] - pad)
cx1, cy1 = min(im.width, box[2] + pad), min(im.height, box[3] + pad)
crop = im.crop((cx0, cy0, cx1, cy1))
buf = io.BytesIO(); crop.save(buf, 'PNG')
body = {
    'model': model, 'modalities': ['image', 'text'], 'usage': {'include': True},
    'messages': [{'role': 'user', 'content': [
        {'type': 'text', 'text': prompt + ' Keep everything else in the image pixel-identical: same framing, same size, same colors, same lighting. Return only the edited image.'},
        {'type': 'image_url', 'image_url': {'url': 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()}},
    ]}],
}
req = urllib.request.Request('https://openrouter.ai/api/v1/chat/completions', data=json.dumps(body).encode(),
                             headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
try:
    res = json.load(urllib.request.urlopen(req, timeout=240))
except urllib.error.HTTPError as e:
    sys.exit(f'HTTP {e.code}: {e.read().decode()[:400]}')
msg = res['choices'][0]['message']
imgs = msg.get('images') or []
if not imgs:
    sys.exit('нет картинки в ответе: ' + json.dumps(msg)[:400])
ai = Image.open(io.BytesIO(base64.b64decode(imgs[0]['image_url']['url'].split(',', 1)[1]))).convert('RGB')
print('модель', model, '| фрагмент', crop.size, '-> ответ', ai.size, '| usage', json.dumps(res.get('usage', {}))[:300])
ai = ai.resize(crop.size, Image.LANCZOS)
mask = Image.new('L', crop.size, 0)
ImageDraw.Draw(mask).rectangle((box[0] - cx0, box[1] - cy0, box[2] - cx0, box[3] - cy0), fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(feather))
res_im = im.copy()
res_im.paste(Image.composite(ai, crop, mask), (cx0, cy0))
os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
res_im.save(out, quality=94)
# лист сравнения: оригинал | результат, фрагмент при 100 %
cmp_ = Image.new('RGB', (crop.width * 2 + 8, crop.height), '#f0f')
cmp_.paste(crop, (0, 0)); cmp_.paste(res_im.crop((cx0, cy0, cx1, cy1)), (crop.width + 8, 0))
cmp_.save(os.path.splitext(out)[0] + '.cmp.jpg', quality=92)
print('сохранено', out)
