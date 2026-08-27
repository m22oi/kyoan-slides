#!/usr/bin/env python3
"""덱 → PDF (배포·인쇄용).   python3 topdf.py deck.html deck.pdf"""
import sys, re
from pathlib import Path
src = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2] if len(sys.argv) > 2 else src.with_suffix('.pdf'))
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    raise SystemExit(
        'Playwright 가 없습니다. 대안: 브라우저에서 deck.html 을 열고 Ctrl+P →\n'
        '  대상 "PDF로 저장", 용지 가로, 배율 100%, 배경 그래픽 켜기.\n'
        '  (템플릿에 인쇄 CSS가 들어 있어 슬라이드가 한 장씩 나뉩니다.)')
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto(f'file://{src}'); pg.wait_for_timeout(800)
    pg.pdf(path=str(out), width='1280px', height='720px', print_background=True, margin={'top':'0','bottom':'0','left':'0','right':'0'})
    b.close()
print(f'→ {out}')
