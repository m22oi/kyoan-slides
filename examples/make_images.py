"""예시 명세가 참조하는 이미지를 코드로 그려 _images.json 으로 저장한다.

    python3 make_images.py

하트 3종(5x5·16x16·32x32) · 픽셀 확대 도해 · 픽셀 그리기 앱 목업.
전부 코드로 그리므로 저작권 이슈가 없다. 실제 수업에서는 앱 스크린샷을
embed_images.py 로 넣으면 된다.
"""
from PIL import Image, ImageDraw
import base64, io, json

INK = (21, 42, 32)
PINK = (252, 61, 138)

def b64(im, scale=1):
    if scale != 1:
        im = im.resize((im.width*scale, im.height*scale), Image.NEAREST)
    buf = io.BytesIO(); im.save(buf, 'PNG')
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()

def heart(n):
    """n x n 캔버스에 하트를 그린다."""
    im = Image.new('RGB', (n, n), 'white')
    d = ImageDraw.Draw(im)
    cx, cy = (n-1)/2, (n-1)/2
    for y in range(n):
        for x in range(n):
            # 하트 방정식 (정규화 좌표)
            u = (x - cx) / (n/2) * 1.15
            v = -(y - cy) / (n/2) * 1.15 + 0.30
            f = (u*u + v*v - 1)**3 - u*u*v*v*v
            if f <= 0:
                d.point((x, y), PINK)
    return im

def pixel_zoom():
    """체커보드 + 확대 도해."""
    im = Image.new('RGB', (640, 300), 'white')
    d = ImageDraw.Draw(im)
    g = (170, 170, 170)
    for y in range(16):
        for x in range(16):
            if (x+y) % 2 == 0:
                d.rectangle([x*16, y*16+22, x*16+15, y*16+37], fill=g)
    d.rectangle([0, 22, 255, 277], outline=INK, width=2)
    # 확대판
    for y in range(4):
        for x in range(4):
            c = g if (x+y) % 2 == 0 else (255, 255, 255)
            d.rectangle([380+x*60, 40+y*60, 380+x*60+59, 40+y*60+59], fill=c, outline=(210,210,210))
    d.rectangle([380, 40, 619, 279], outline=INK, width=2)
    d.rectangle([500, 160, 559, 219], outline=INK, width=4)
    d.line([256, 100, 380, 40], fill=INK, width=2)
    d.line([256, 210, 380, 279], fill=INK, width=2)
    return im

def app_mock():
    """픽셀 그리기 앱 화면 목업 (실제 앱 스크린샷 대체)."""
    W, H = 900, 480
    im = Image.new('RGB', (W, H), (247, 247, 249))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 46], fill=(106, 62, 118))
    d.text((W//2-40, 16), 'Drawing 1', fill='white')
    # 캔버스
    for y in range(5):
        for x in range(5):
            c = (232,232,232) if (x+y) % 2 == 0 else (245,245,245)
            d.rectangle([120+x*64, 80+y*64, 120+x*64+63, 80+y*64+63], fill=c)
    d.rectangle([120, 80, 439, 399], outline=(190,190,190))
    # 우측 패널
    d.rectangle([620, 46, W, H], fill=(255,255,255), outline=(225,225,225))
    d.text((636, 60), '색상 선택', fill=(90,90,90))
    d.ellipse([660, 84, 820, 244], outline=(200,200,200), width=14)
    d.text((636, 262), 'PALETTE', fill=(140,140,140))
    cols = [(0,0,0),(220,40,40),(240,150,40),(240,220,60),(120,210,90),(60,190,150),
            (60,150,230),(140,90,220),(230,90,170),(120,120,120)]
    for r in range(4):
        for i, c in enumerate(cols):
            d.ellipse([636+i*26, 286+r*26, 636+i*26+18, 286+r*26+18], fill=c)
    d.text((636, 400), 'TOOLBOX', fill=(140,140,140))
    for i in range(4):
        d.rectangle([640+i*44, 424, 640+i*44+32, 456], outline=(150,150,150), width=2)
    return im

out = {
    'heart5':  b64(heart(5), 60),
    'heart16': b64(heart(16), 19),
    'heart32': b64(heart(32), 10),
    'zoom':    b64(pixel_zoom()),
    'app':     b64(app_mock()),
}
open('_images.json', 'w').write(json.dumps(out))
print({k: len(v)//1024 for k, v in out.items()}, 'KB')
