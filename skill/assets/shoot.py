#!/usr/bin/env python3
"""덱의 전 슬라이드를 PNG로 캡처한다 (빌드 검증용).

사용법:  python3 shoot.py deck.html out/
그 다음 out/s01.png … 를 Read 로 직접 확인할 것.
"""
import sys, os, re
from pathlib import Path
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    raise SystemExit(
        'Playwright 가 없어 자동 검증을 할 수 없습니다.\n'
        '  설치:  pip install playwright --break-system-packages && playwright install chromium\n'
        '  설치가 불가능하면 deck.html 을 브라우저에서 직접 열어 전 슬라이드를 눈으로 확인하고,\n'
        '  검증을 건너뛰었다고 사용자에게 알릴 것.')

src = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2] if len(sys.argv) > 2 else "out")
out.mkdir(parents=True, exist_ok=True)

n = len(re.findall(r"<section\b", src.read_text(encoding="utf-8")))

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1280, "height": 720}, device_scale_factor=1)
    pg.goto(f"file://{src}")
    pg.wait_for_timeout(500)
    for i in range(1, n + 1):
        if i > 1:
            pg.keyboard.press("ArrowRight")
        pg.wait_for_timeout(350)
        pg.screenshot(path=str(out / f"s{i:02d}.png"))
        # 넘침 검사
        over = pg.evaluate("""() => {
            const s=document.querySelector('section.is-active');
            const r=s.getBoundingClientRect();
            return [...s.querySelectorAll('*')].filter(e=>{
              if(e.closest('.sticker,.doodle')) return false;
              const b=e.getBoundingClientRect();
              return b.width && (b.bottom>r.bottom+2 || b.right>r.right+2 || b.left<r.left-2);
            }).map(e=>e.tagName+'.'+e.className).slice(0,5);
        }""")
        if over:
            print(f"  ⚠ s{i:02d} 넘침: {over}")
    b.close()
print(f"{n}장 저장 → {out}")
