#!/usr/bin/env python3
"""스크린샷 폴더 → 리사이즈·압축·base64 → images.json

    python3 embed_images.py shots/ images.json [--max 1400] [--quality 82]

- 긴 변을 --max 로 줄이고 WebP 로 압축한다(스크린샷 기준 원본의 3~8%).
- 키는 파일 이름(확장자 제외). 명세에서 "image": "canvas-size" 처럼 참조한다.
- 총 용량과 파일별 용량을 출력한다. 합계 12MB 를 넘으면 경고한다.
- WebP 를 못 쓰는 환경이면 --format png 로 바꾼다(용량은 커진다).
"""
import base64, io, json, sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    raise SystemExit('Pillow 가 필요합니다:  pip install pillow --break-system-packages')

EXT = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp'}

def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default

def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    mx = int(arg('--max', 1400))
    q = int(arg('--quality', 82))
    fmt = arg('--format', 'webp').lower()

    files = sorted(p for p in src.rglob('*') if p.suffix.lower() in EXT)
    if not files:
        raise SystemExit(f'{src} 에 이미지가 없습니다')

    data, total, before = {}, 0, 0
    for p in files:
        before += p.stat().st_size
        im = Image.open(p)
        if im.mode not in ('RGB', 'RGBA'):
            im = im.convert('RGBA' if 'A' in im.mode else 'RGB')
        if max(im.size) > mx:
            r = mx / max(im.size)
            im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
        buf = io.BytesIO()
        if fmt == 'webp':
            im.save(buf, 'WEBP', quality=q, method=6)
            mime = 'image/webp'
        else:
            im.convert('RGB' if im.mode == 'RGB' else 'RGBA').save(buf, 'PNG', optimize=True)
            mime = 'image/png'
        b = buf.getvalue()
        total += len(b)
        data[p.stem] = f'data:{mime};base64,' + base64.b64encode(b).decode()
        print(f'  {p.name:38s} {p.stat().st_size/1024:7.0f} KB → {len(b)/1024:6.0f} KB '
              f'({im.width}x{im.height})', file=sys.stderr)

    out.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
    mb = total * 4 / 3 / 1024 / 1024      # base64 팽창 반영
    print(f'\n{len(data)}장  원본 {before/1024/1024:.1f} MB → 내장 약 {mb:.1f} MB  → {out}',
          file=sys.stderr)
    if mb > 12:
        print('  ⚠ 12MB 초과. --max 1100 또는 --quality 70 으로 다시 돌리거나 '
              '스크린샷 수를 줄일 것 (아티팩트 한도 16MB)', file=sys.stderr)

if __name__ == '__main__':
    main()
