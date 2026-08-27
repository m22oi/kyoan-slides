#!/usr/bin/env python3
"""Paperlogy(또는 임의의 한글 폰트)를 한글 서브셋 woff2로 줄여 base64 @font-face 로 출력.

사용법:
    pip install fonttools brotli --break-system-packages
    python3 embed_font.py Paperlogy-7Bold.ttf Paperlogy-4Regular.ttf deck.html
    # deck.html 안에 쓰인 글자만 서브셋해서 <!-- FONT-FACE --> 자리에 삽입한다.

deck.html 을 주지 않으면 KS X 1001 상용 한글 2350자 + ASCII 로 서브셋한다.
Paperlogy 는 SIL Open Font License 이므로 임베딩/재배포가 허용된다.
"""
import base64, io, re, sys, unicodedata
from pathlib import Path

try:
    from fontTools.ttLib import TTFont
    from fontTools.subset import Subsetter, Options
except ImportError:
    sys.exit("fonttools 가 필요합니다:  pip install fonttools brotli --break-system-packages")


def chars_from_html(path: Path) -> set:
    txt = re.sub(r"<[^>]+>", " ", path.read_text(encoding="utf-8"))
    return set(txt)


def default_charset() -> set:
    cs = set(chr(c) for c in range(0x20, 0x7F))
    # 한글 음절 전체(11,172자)를 넣으면 서브셋 의미가 사라진다(수 MB).
    # deck.html 을 인자로 주는 것이 정상 경로이며, 이 기본값은 최후의 수단이다.
    print('  ⚠ deck.html 없이 실행됨 — 한글 전체를 넣어 용량이 커집니다. '
          'deck.html 을 함께 지정하세요.', file=sys.stderr)
    cs |= set(chr(c) for c in range(0xAC00, 0xD7A4))
    cs |= set("‘’“”…·–—×÷←→↑↓★☆♥♡")
    return cs


def subset(src: Path, chars: set) -> bytes:
    font = TTFont(str(src))
    opts = Options()
    opts.flavor = "woff2"
    opts.desubroutinize = True
    opts.layout_features = ["*"]
    sub = Subsetter(options=opts)
    sub.populate(text="".join(sorted(chars)))
    sub.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff2"
    font.save(buf)
    return buf.getvalue()


def main():
    args = [Path(a) for a in sys.argv[1:]]
    fonts = [a for a in args if a.suffix.lower() in (".ttf", ".otf", ".woff2")]
    html = next((a for a in args if a.suffix.lower() in (".html", ".htm")), None)
    if not fonts:
        sys.exit(__doc__)

    chars = chars_from_html(html) if html and html.exists() else default_charset()
    chars |= set(chr(c) for c in range(0x20, 0x7F))

    blocks = []
    for f in fonts:
        weight = 700 if re.search(r"(bold|7b)", f.stem, re.I) else 400
        data = subset(f, chars)
        b64 = base64.b64encode(data).decode()
        blocks.append(
            "@font-face{font-family:'Paperlogy';font-style:normal;font-weight:%d;"
            "font-display:swap;src:url(data:font/woff2;base64,%s) format('woff2');}" % (weight, b64)
        )
        print(f"  {f.name}: {len(data)/1024:.0f} KB (woff2)", file=sys.stderr)

    css = "<style>\n" + "\n".join(blocks) + "\n</style>"

    if html and html.exists():
        src = html.read_text(encoding="utf-8")
        marker = "<!-- FONT-FACE:"
        if marker in src:
            src = re.sub(r"<!-- FONT-FACE:.*?-->", css, src, count=1, flags=re.S)
        else:
            src = src.replace("</head>", css + "\n</head>", 1)
        html.write_text(src, encoding="utf-8")
        print(f"OK → {html}", file=sys.stderr)
    else:
        print(css)


if __name__ == "__main__":
    main()
