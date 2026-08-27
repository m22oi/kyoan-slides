#!/usr/bin/env python3
"""슬라이드 명세(JSON) → 교안 HTML 한 파일.

    python3 build.py deck.json deck.html [--images images.json]

명세만 고치면 마크업은 이 스크립트가 찍는다. 스티커·낙서 배치, 챕터 색 순환,
초등 가독성 규칙 검사는 전부 자동이다. 규칙 위반은 stderr 에 경고로 나온다.
스펙 형식은 references/spec.md 참고.
"""
import json, re, sys
from pathlib import Path

HERE = Path(__file__).parent
PALETTE = ['pink', 'orange', 'purple', 'mint', 'yellow', 'green']

# ---------- 장식 ----------
SVG = {
 'heart': '<svg width="72" height="66" viewBox="0 0 24 22"><path fill="currentColor"'
          ' d="M12 20.4C12 20.4 2.6 14.2 2.6 8.2A5.2 5.2 0 0 1 12 5.1 5.2 5.2 0 0 1 21.4 8.2'
          'C21.4 14.2 12 20.4 12 20.4Z"/></svg>',
 'star': '<svg width="72" height="68" viewBox="0 0 24 23"><path fill="currentColor"'
         ' d="M12 1.8 15 8.4 22.1 9.2 16.8 14 18.3 21 12 17.6 5.7 21 7.2 14 1.9 9.2 9 8.4Z"/></svg>',
 'smile': '<svg width="74" height="74" viewBox="0 0 24 24">'
          '<circle cx="12" cy="12" r="10.2" fill="currentColor"/>'
          '<path d="M8.6 9.8v1.3M15.4 9.8v1.3" fill="none"/>'
          '<path d="M8.8 14.2a4.2 4.2 0 0 0 6.4 0" fill="none"/></svg>',
}
DOODLE = {
 'left':  '<span class="doodle" style="left:-4px;top:330px"><svg width="116" height="196" viewBox="0 0 130 230"><path d="M118 4C70 26 6 40 22 74s76 6 66 44-64 26-58 62 60 30 82 46"/></svg></span>',
 'right': '<span class="doodle" style="right:-6px;top:262px"><svg width="116" height="186" viewBox="0 0 130 230"><path d="M12 4c48 22 112 36 96 70s-76 6-66 44 64 26 58 62-60 30-82 46"/></svg></span>',
}
# 레이아웃별로 콘텐츠와 절대 겹치지 않는 슬롯만 허용한다.
SLOTS = {
    'bar_left':   'top:2px;left:118px',
    'bar_midl':   'top:2px;left:236px',
    'bar_right':  'top:2px;right:206px',
    'edge_right': 'bottom:150px;right:-16px',
    'gut_right':  'top:206px;right:22px',
    'cov_right':  'top:330px;right:2px',
    'edge_left':  'bottom:172px;left:-12px',
}
# fill(색면) 레이아웃은 사방이 비어 안전, 그리드 레이아웃은 타이틀바 슬롯만.
# 눈썹 라벨이 좌상단을 차지하는 레이아웃에는 스티커를 붙이지 않는다(라벨이 그 역할을 한다).
LAYOUT_SLOTS = {
    'cover':   ['bar_midl', 'cov_right'],
    'divider': ['bar_left', 'edge_right'],
    'ask':     ['bar_left', 'edge_right'],
    'outro':   ['bar_left', 'edge_left'],
    'goals':   ['bar_left'],
}
DOODLE_LAYOUTS = {'divider', 'ask', 'outro'}

# ---------- 표지 전용 오브젝트 일러스트 (원본 교안의 연필·마우스·키보드) ----------
OBJECTS = (
 # 연필 — 좌상단
 '<span class="obj" style="top:34px;left:34px;transform:rotate(-20deg)">'
 '<svg width="76" height="214" viewBox="0 0 40 112">'
 '<rect x="9" y="2" width="22" height="14" rx="7" fill="#FFD4A8"/>'
 '<rect x="9" y="15" width="22" height="7" fill="#EDE2FF"/>'
 '<rect x="9" y="21" width="22" height="61" rx="3" fill="#D6BDF7"/>'
 '<path d="M9 82h22l-8.5 22a2.6 2.6 0 0 1-5 0Z" fill="#FAE5A8"/>'
 '<path d="M16.4 101.5h7.2l-2.1 5.5a1.6 1.6 0 0 1-3 0Z" fill="#152A20"/>'
 '</svg></span>'
 # 마우스 — 좌하단
 '<span class="obj" style="bottom:34px;left:32px">'
 '<svg width="88" height="129" viewBox="0 0 56 82">'
 '<rect x="3" y="3" width="50" height="76" rx="25" fill="#9CF0E5"/>'
 '<path d="M28 5v26" fill="none"/>'
 '<rect x="22.5" y="14" width="11" height="18" rx="5.5" fill="#D2FABB"/>'
 '</svg></span>'
 # 키보드 — 우하단
 '<span class="obj" style="bottom:24px;right:6px;transform:rotate(-8deg)">'
 '<svg width="196" height="106" viewBox="0 0 140 76">'
 '<rect x="3" y="3" width="134" height="70" rx="12" fill="#FFD4A8"/>'
 + ''.join(f'<rect x="{11+i*15}" y="12" width="11" height="10" rx="3" fill="#FFF8F7"/>' for i in range(8))
 + ''.join(f'<rect x="{11+i*15}" y="28" width="11" height="10" rx="3" fill="#FFF8F7"/>' for i in range(8))
 + '<rect x="34" y="52" width="72" height="12" rx="5" fill="#FFF8F7"/>'
 '</svg></span>'
)

DOTS = '<div class="dots"><i></i><i></i><i></i></div>'

warnings = []
def warn(i, msg):
    warnings.append(f'  슬라이드 {i:>2}: {msg}')

def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            .replace('"', '&quot;'))

def br(s):
    return esc(s).replace('\n', '<br>')

def width(line):
    """한글=1.0em, 영숫자=0.55em, 공백=0.32em 로 줄 폭을 em 단위로 추정."""
    w = 0.0
    for ch in re.sub('<[^>]+>', '', str(line)):
        if ch == ' ': w += 0.32
        elif '\uac00' <= ch <= '\ud7a3': w += 1.0
        else: w += 0.55
    return w


def fit_class(lines, px_avail, sizes):
    """가장 긴 줄이 px_avail 안에 들어가는 가장 큰 크기를 고른다."""
    mx = max(width(l) for l in lines) or 1
    for cls, px in sizes:
        if mx * px <= px_avail:
            return cls
    return sizes[-1][0]


def plain(s):
    return re.sub(r'\s+', '', re.sub('<[^>]+>', '', str(s)))

# ---------- 초등 중저학년 가독성 검사 ----------
MAX_LINE = 20        # 한 줄 한글 글자 수 (글자를 키웠으므로 줄었다)
MAX_BULLETS = 4
MAX_CHARS = 100      # 슬라이드 전체 본문 글자 수
HARD_WORDS = ['활용', '수행', '구현', '적용', '인지', '산출', '도출', '기입',
              '입력하시오', '설정하여', '~에 대하여', '요구된다']

def check_text(idx, s, label):
    t = str(s)
    for line in t.split('\n'):
        if len(plain(line)) > MAX_LINE:
            warn(idx, f'{label} 한 줄이 {len(plain(line))}자 (권장 {MAX_LINE}자): "{line[:24]}…"')
    for w in HARD_WORDS:
        if w in t:
            warn(idx, f'{label}에 어려운 낱말 "{w}" — 쉬운 말로 바꿀 것')

# ---------- 슬라이드 렌더러 ----------
def win(inner, fill=False, bar='', bar_cls='', body_cls='', eb=''):
    h = f'<h1 class="{bar_cls}">{bar}</h1>'
    return (f'<div class="win{" win--fill" if fill else ""}">'
            f'<div class="win__bar"><span class="barleft">{eb}</span>{h}{DOTS}</div>'
            f'<div class="win__body {body_cls}">{inner}</div></div>')

def bar_cls_for(title, eb_text):
    """타이틀바에 눈썹 라벨과 신호등을 두고 남는 폭에 맞춰 제목 크기를 고른다."""
    eb_w = width(eb_text) * 25 + 44 if eb_text else 0     # 라벨 실제 폭
    avail = 1152 - 77 - 24 - eb_w - 40                    # 바 안폭 - 신호등 - 간격 - 라벨 - 여유
    side = max(avail, 300)
    return fit_class([title], side, [('', 52), ('sm', 44), ('xs', 36)])


def eyebrow(sl):
    ch = sl.get('chapter')
    return f'<span class="eyebrow">{esc(ch)}</span>' if ch and sl['type'] not in (
        'cover', 'divider', 'outro') else ''

def render(sl, idx, meta, images):
    t = sl['type']
    img = lambda k: images.get(k, k)
    px = ' px' if sl.get('pixel') else ''
    eb = eyebrow(sl)

    if t == 'cover':
        lines = str(meta['course']).split('\n')
        ccls = fit_class(lines, 1000, [('big', 96), ('big sm', 76), ('big xs', 62), ('big xxs', 50)])
        if ccls == 'big xxs':
            warn(idx, '과정명이 길다 — \\n 으로 끊으면 훨씬 크게 나온다')
        return (f'<div class="win" style="border:none;background:none">'
                f'<div class="win__bar" style="border:var(--bw) solid var(--ink);'
                f'border-radius:var(--r-lg);padding-right:20px;margin:0 26px;display:flex">'
                f'<h2 style="font-size:30px;text-align:right;flex:1">{esc(meta["program"])}</h2>{DOTS}</div>'
                f'<div style="flex:1;min-height:0;margin:var(--s-md) 26px 0;background:var(--pink);'
                f'border:var(--bw) solid var(--ink);border-radius:var(--r-lg);display:flex;'
                f'flex-direction:column;align-items:center;justify-content:center;gap:36px;padding:28px">'
                f'<div class="shadowbox"><div class="{ccls}">{br(meta["course"])}</div></div>'
                f'<div class="lesson"><em>{esc(meta["lessonNo"])}.</em>{esc(meta["lessonTitle"])}</div>'
                f'</div></div>' + OBJECTS)

    if t == 'goals':
        items = ''.join(f'<div class="goal">{br(g)}</div>' for g in sl['items'])
        if len(sl['items']) > 3:
            warn(idx, f'학습목표가 {len(sl["items"])}개 — 3개 이하로')
        for g in sl['items']:
            check_text(idx, g, '학습목표')
        return win(f'<div class="goals">{items}</div>', bar=esc(sl.get('title', '학습 목표')),
                   bar_cls=bar_cls_for(sl.get('title', '학습 목표'), ''))

    if t == 'divider':
        cap = f'<div class="caption" style="width:64%">{br(sl["sub"])}</div>' if sl.get('sub') else ''
        cls = fit_class(str(sl['title']).split('\n'), 960,
                        [('big', 96), ('big sm', 76), ('big xs', 62), ('big xxs', 50)])
        return win(f'<div class="divider-title"><div class="{cls}">{br(sl["title"])}</div></div>{cap}',
                   fill=True, body_cls='divider')

    if t == 'term':
        check_text(idx, sl['def'], '용어 정의')
        if sl.get('image'):
            body = (f'<span class="pill lg">{esc(sl["term"])}</span>'
                    f'<p class="lead" style="margin-top:var(--s-xs)">{br(sl["def"])}</p>'
                    f'<div class="media" style="margin-top:var(--s-md)">'
                    f'<img class="{px.strip()}" src="{img(sl["image"])}" alt="{esc(sl.get("alt",""))}"></div>')
            return win(body, bar=esc(sl['title']),
                       bar_cls=bar_cls_for(sl['title'], sl.get('chapter', '')), eb=eb)
        # 그림이 없으면 가운데로 모아 허전하지 않게
        return win(f'<div class="termblock"><span class="pill lg">{esc(sl["term"])}</span>'
                   f'<p class="mid" style="font-size:48px">{br(sl["def"])}</p></div>',
                   bar=esc(sl['title']), bar_cls=bar_cls_for(sl['title'], sl.get('chapter', '')), eb=eb)

    if t in ('bullets', 'quiz'):
        for b in sl['items']:
            check_text(idx, b, '글머리표')
        if len(sl['items']) > MAX_BULLETS:
            warn(idx, f'글머리표 {len(sl["items"])}개 — {MAX_BULLETS}개 이하로 쪼갤 것')
        lis = ''.join(f'<li>{br(b)}</li>' for b in sl['items'])
        pill = (f'<div class="pillrow"><span class="pill">{br(sl["pill"])}</span></div>'
                if sl.get('pill') else '')
        return win(f'<ul class="bullets">{lis}</ul>{pill}', bar=esc(sl['title']),
                   bar_cls=bar_cls_for(sl['title'], sl.get('chapter','')), eb=eb)

    if t in ('steps', 'activity'):
        for s in sl['steps']:
            check_text(idx, s, '활동 단계')
        if len(sl['steps']) > 3:
            warn(idx, f'활동 단계 {len(sl["steps"])}개 — 3단계 이하로')
        lis = ''.join(f'<li>{br(s)}</li>' for s in sl['steps'])
        timer = ''
        if t == 'activity':
            if not sl.get('timer'):
                warn(idx, '활동 슬라이드에 timer 가 없다')
            m = sl.get('timer', 10)
            timer = (f'<div class="timer"><div class="timer__face">{m:02d}:00</div>'
                     f'<button type="button">시작</button></div>')
        return win(f'<ol class="steps">{lis}</ol>{timer}', bar=esc(sl['title']),
                   bar_cls=bar_cls_for(sl['title'], sl.get('chapter', '')), eb=eb)

    if t == 'cards':
        if len(sl['items']) > 4:
            warn(idx, '카드는 4장까지')
        cs = ''
        for c in sl['items']:
            if len(plain(c['h'].split('\n')[0])) > 8:
                warn(idx, f'카드 제목 첫 줄이 길다 (\\n 으로 끊을 것): "{c["h"]}"')
            style = f' style="background:var(--{c["color"]})"' if c.get('color') else ''
            p = f'<p>{br(c["p"])}</p>' if c.get('p') else ''
            cs += f'<div class="card"{style}><h3>{br(c["h"])}</h3>{p}</div>'
        pill = (f'<div class="pillrow"><span class="pill">{br(sl["pill"])}</span></div>'
                if sl.get('pill') else '')
        return win(f'<div class="cards" style="--n:{len(sl["items"])}">{cs}</div>{pill}',
                   bar=esc(sl['title']), bar_cls=bar_cls_for(sl['title'], sl.get('chapter', '')), eb=eb)

    if t == 'screenshot':
        rings = ''
        n_ring = len(sl.get('rings', []))
        if n_ring > 2:
            warn(idx, f'강조 링 {n_ring}개 — 2개까지. 슬라이드를 나눌 것 (한 슬라이드 한 동작)')
        for r in sl.get('rings', []):
            rings += (f'<span class="ring" style="left:{r["x"]}%;top:{r["y"]}%;'
                      f'width:{r["w"]}%;height:{r["h"]}%"></span>')
            if r.get('label'):
                lx = r.get('lx', r['x'] + r['w'] / 2)
                ly = r.get('ly', r['y'] + r['h'] + 6)
                rings += f'<span class="tag" style="left:{lx}%;top:{ly}%">{esc(r["label"])}</span>'
        return win(f'<div class="media"><span class="shot">'
                   f'<img class="framed" src="{img(sl["image"])}" alt="{esc(sl.get("alt",""))}">'
                   f'{rings}</span></div>', bar=esc(sl['title']),
                   bar_cls=bar_cls_for(sl['title'], sl.get('chapter', '')), body_cls='tight', eb=eb)

    if t == 'compare':
        fs = ''.join(f'<figure><img class="{px.strip()}" src="{img(c["image"])}" alt="{esc(c.get("alt",""))}">'
                     f'<span class="pill pink sm">{esc(c["label"])}</span></figure>'
                     for c in sl['items'])
        pill = (f'<div class="pillrow"><span class="pill pink">{br(sl["pill"])}</span></div>'
                if sl.get('pill') else '')
        return win(f'<div class="compare" style="--n:{len(sl["items"])}">{fs}</div>{pill}',
                   bar=esc(sl['title']), bar_cls=bar_cls_for(sl['title'], sl.get('chapter', '')), eb=eb)

    if t == 'gallery':
        gs = ''.join(f'<img class="{px.strip()}" src="{img(g)}" alt="">' for g in sl['images'])
        pill = (f'<div class="pillrow"><span class="pill">{br(sl["pill"])}</span></div>'
                if sl.get('pill') else '')
        return win(f'<div class="gallery" style="--n:{sl.get("cols",len(sl["images"]))}">{gs}</div>{pill}',
                   bar=esc(sl['title']), bar_cls=bar_cls_for(sl['title'], sl.get('chapter', '')),
                   body_cls='tight', eb=eb)

    if t == 'ask':
        check_text(idx, sl['q'], '발문')
        if not sl.get('notes'):
            warn(idx, '발문 슬라이드에 예상 답변(notes)이 없다')
        return win(f'<div class="mid">{br(sl["q"])}</div>',
                   fill=True, bar=esc(sl.get('title', '생각해 봐요')),
                   bar_cls=bar_cls_for(sl.get('title', '생각해 봐요'), ''), body_cls='center')

    if t == 'share':
        media = (f'<div class="media"><img class="{px.strip()}" src="{img(sl["image"])}" alt="{esc(sl.get("alt",""))}"></div>'
                 if sl.get('image') else f'<div class="mid" style="flex:1;display:grid;place-items:center">{br(sl.get("q",""))}</div>')
        return win(f'{media}<div class="pillrow"><span class="pill">{br(sl["pill"])}</span></div>',
                   bar=esc(sl['title']), bar_cls=bar_cls_for(sl['title'], sl.get('chapter', '')), eb=eb)

    if t == 'outro':
        return win(f'<div class="divider-title"><div class="big">{br(sl.get("title", "참 잘했어요"))}</div></div>'
                   f'<div class="caption">{br(meta.get("next",""))}</div>',
                   fill=True, body_cls='divider')

    raise SystemExit(f'알 수 없는 슬라이드 type: {t}')


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    spec = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    outp = Path(sys.argv[2])
    images = {}
    if '--images' in sys.argv:
        images = json.loads(Path(sys.argv[sys.argv.index('--images') + 1]).read_text())

    meta = spec['meta']
    chapters = {c['name']: c.get('color') for c in spec.get('chapters', [])}
    # 색이 지정 안 된 챕터는 orange → pink → purple → mint 순환
    cycle = ['orange', 'pink', 'purple', 'mint']
    ci = 0
    for name in chapters:
        if not chapters[name]:
            chapters[name] = cycle[ci % len(cycle)]; ci += 1

    out, cur_ch = [], None
    sticker_i, prev_combo = 0, None
    fill_streak = 0

    for k, sl in enumerate(spec['slides'], 1):
        cur_ch = sl.get('chapter', cur_ch)
        if sl['type'] in ('cover', 'goals'):
            cur_ch = sl.get('chapter', {'cover': '표지', 'goals': '학습 목표'}[sl['type']])
        sl['chapter'] = cur_ch

        # 색: 활동은 항상 노랑, 그 외는 챕터 색
        accent = 'yellow' if sl['type'] == 'activity' else (
            sl.get('color') or chapters.get(cur_ch) or 'pink')

        # 색면 연속 방지 (Figma: 색 블록 사이에는 흰 캔버스를 둔다)
        is_fill = sl['type'] in ('divider', 'ask', 'outro', 'cover')
        if is_fill:
            fill_streak += 1
            if fill_streak >= 3:
                warn(k, '색면 슬라이드가 3장 연속 — 사이에 흰 배경 슬라이드를 넣을 것')
        else:
            fill_streak = 0

        body = render(sl, k, meta, images)

        # 스티커 자동 배치: 레이아웃이 허용한 슬롯에서, 악센트와 다른 색으로, 조합 반복 없이
        deco = ''
        slots = LAYOUT_SLOTS.get(sl['type'], [])
        n_st = min(len(slots), 2 if k % 2 == 1 else 1)
        shapes = ['heart', 'star', 'smile']
        combo = []
        for j in range(n_st):
            shape = shapes[(sticker_i + j) % 3]
            col = [c for c in PALETTE if c != accent][(sticker_i * 2 + j) % (len(PALETTE) - 1)]
            combo.append((shape, col))
            deco += (f'<span class="sticker" style="{SLOTS[slots[j]]};color:var(--{col})">'
                     f'{SVG[shape]}</span>')
        if combo and combo == prev_combo:
            warn(k, '앞 슬라이드와 스티커 조합이 같다')
        if combo:
            prev_combo, sticker_i = combo, sticker_i + 1

        if sl['type'] in DOODLE_LAYOUTS:
            deco += DOODLE['left' if k % 2 else 'right']

        # 본문 글자 수 (렌더된 화면 글자만)
        total = len(plain(re.sub(r'<(script|style)[^>]*>.*?</\1>', '', body, flags=re.S)))
        if total > MAX_CHARS:
            warn(k, f'글자가 많다(약 {total}자) — 슬라이드를 나눌 것')

        attrs = (f'style="--accent:var(--{accent})" data-chapter="{esc(cur_ch or "")}" '
                 f'data-title="{esc(sl.get("title") or sl.get("q") or meta.get("lessonTitle",""))}" '
                 f'data-notes="{esc(sl.get("notes",""))}"')
        if sl['type'] == 'activity':
            attrs += f' data-timer="{sl.get("timer",10)}"'
        out.append(f'<section {attrs}>{body}{deco}</section>')

    tpl = (HERE / 'template.html').read_text(encoding='utf-8')
    html = tpl.replace('<!-- SLIDES -->', '\n'.join(out)).replace(
        '{{DECK_TITLE}}', esc(f'{meta["lessonNo"]}. {meta["lessonTitle"]}'))
    outp.write_text(html, encoding='utf-8')

    size = len(html.encode()) / 1024 / 1024
    print(f'{len(out)}장 → {outp}  ({size:.1f} MB)', file=sys.stderr)
    if size > 15:
        print('  ⚠ 15MB 초과 — embed_images.py 로 이미지를 더 줄일 것', file=sys.stderr)
    if warnings:
        print(f'\n규칙 경고 {len(warnings)}건:', file=sys.stderr)
        print('\n'.join(warnings), file=sys.stderr)
    else:
        print('규칙 경고 없음', file=sys.stderr)


if __name__ == '__main__':
    main()
