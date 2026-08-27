---
name: kyoan-slides
description: 초등 중저학년용 교안 슬라이드를 만든다 — 파스텔 브라우저 창 스타일(모눈 배경·검정 외곽선·알약 강조)의 단일 HTML 파일로, 교실 화면에 띄워 넘기며 수업한다. 목차 점프·발표자 노트·활동 타이머가 들어 있다. Use when 초등 교안, 차시 슬라이드, 학습목표 슬라이드, 앱 실습 매뉴얼 슬라이드, 픽셀아트/코딩 수업 자료 같은 요청이 있을 때. 코드 하이라이팅이 필요한 개발 강의 자료는 test-class-slides, 지도안·기획안 문서는 lesson-plan, .pptx 파일 자체는 pptx 스킬로 간다.
---

# 교안 슬라이드 (kyoan-slides)

초등 중저학년(3~4학년) 대상 수업용 HTML 덱을 만든다.
결과물은 **의존성 없는 단일 HTML 파일** 하나. 교실 프로젝터에 띄워 키보드로 넘긴다.

## 0. 처음 한 번: 도구 파일 만들기

이 스킬은 파이썬 스크립트로 동작한다. **작업 시작 전에 아래 부록의 코드를 그대로
작업 폴더에 저장한다.** 이미 있으면 다시 만들지 않는다.

| 만들 파일 | 내용 | 필요 시점 |
|---|---|---|
| `kyo_template.html` | 부록 A — 덱 엔진(CSS·네비·목차·타이머) | 항상 |
| `kyo_build.py` | 부록 B — 명세 → HTML + 규칙 검사 | 항상 |
| `kyo_shoot.py` | 부록 C — 전 슬라이드 캡처(검증) | 항상 |
| `kyo_images.py` | 부록 D — 스크린샷 압축·내장 | 스크린샷이 있을 때 |
| `kyo_font.py` · `kyo_topdf.py` | 부록 F — 폰트 내장 · PDF 내보내기 | 선택 |

`kyo_build.py` 는 같은 폴더의 `kyo_template.html` 을 읽는다. **두 파일은 항상 같은 폴더에 둔다.**

## 작업 순서

1. **골든 샘플 확인** — 이 문서 아래 **부록 E 골든 샘플 명세**. 밀도·색 리듬의 기준.
2. **재료 확보** — 아래 "물어볼 것".
3. **명세 작성** — `deck.json` 을 쓴다. **HTML을 손으로 쓰지 않는다.** 형식은 아래 **명세(deck.json) 레퍼런스** 절.
4. **이미지 처리** — 스크린샷이 있으면 `kyo_images.py` 로 먼저 압축·내장.
5. **빌드** — `kyo_build.py`. **규칙 경고가 0건이 될 때까지 명세를 고친다.**
6. **검증** — `kyo_shoot.py` 로 캡처해 **직접 Read 로 눈으로 본다.**
7. **폰트** — 아래 "폰트".
8. **전달** — 파일 전달. 아티팩트 게시 여부는 확인.

```bash
python3 kyo_images.py shots/ images.json          # 스크린샷 있을 때
python3 kyo_build.py deck.json deck.html --images images.json
python3 kyo_shoot.py deck.html out/                     # 검증
python3 kyo_topdf.py deck.html deck.pdf                 # 배포용(선택)
```

## 물어볼 것 (모르면 한 번만 묶어서 질문)

- **사업명 / 과정명 / 차시번호·차시명** — 표지 3단이 이걸로 채워진다
- 학습 목표 2~3개
- 학년 (기본 가정: 초등 3~4학년)
- 수업 시간 (40분 / 80분 블록)
- 실습 앱이 있으면 이름과 **화면 캡처 이미지를 줄 수 있는지**
- 다음 차시명

"알아서 해줘"면 묻지 말고 채운 뒤 가정을 한 줄로 알린다.

---

## 디자인 원칙

원본 교안의 키치한 얼굴은 그대로 두고, 시스템 규율만 지킨다.

### 1. 토큰 밖으로 나가지 않는다

색은 `--pink --orange --purple --mint --yellow --green` + `--ink --bg --white` 가 전부다.
**새 색을 만들지 않는다.** 여백은 8px 배수(`--s-*`), 모서리는 `--r-*` 스케일만 쓴다.

### 2. 파스텔 위 글자는 언제나 잉크색

| 조합 | 대비 |
|---|---|
| 핑크 위 흰 글씨 | 2.06 : 1 ❌ **금지** |
| 핑크 위 잉크 | 7.37 : 1 ✅ |
| 오렌지·퍼플·민트 위 잉크 | 9~11 : 1 ✅ |

교실 뒷자리와 밝은 프로젝터에서 실제로 안 보인다. 흰 글씨는 쓰지 않는다.

### 3. 색면 사이에는 흰 캔버스를 둔다

간지·발문·마무리는 창 전체가 색으로 차는 **색면 슬라이드**다.
색면이 연속되면 리듬이 죽는다. **3장 연속 금지** (kyo_build.py가 경고한다).
그리고 **한 슬라이드에 포인트색은 1개.**

### 4. 크기가 아니라 굵기로 위계를 만든다

본문은 **42px** 아래로 내리지 않는다(1280×720 무대 기준). 교실 뒷자리에서 읽히는 하한이다. 강조는 폰트 크기를 키우는 대신
`<b>` (제목 폰트) 또는 알약으로 감싼다.

### 5. 선 굵기는 화면 전체에서 하나다

아이콘·스티커·일러스트의 외곽선은 **어떤 크기로 확대되든 2.5px**로 고정한다
(`vector-effect:non-scaling-stroke`). SVG 안에 stroke-width 를 직접 적으면 확대 배율만큼
굵어져서 어떤 아이콘은 8px로 찍힌다 — 이게 "아이콘이 두껍다"의 원인이다.
창 테두리도 2.5px이라, 화면 위 모든 선이 같은 무게로 읽힌다.

### 6. 그림자를 쓰지 않는다

색면이 깊이 장치다. 그라데이션·드롭섀도우·블러 금지.
예외는 표지 제목의 오프셋 그림자 하나뿐이다.

### 7. 표지·간지는 원본 구성을 지킨다

- **표지 3단**: 상단 사업명(작은 창) / 중간 과정명(노란 상자, 최대 96px) / 하단 차시명(54px).
  핑크 패널을 좌우로 들이고 그 여백에 **연필·마우스·키보드 일러스트**를 놓는다(build.py 자동).
- **간지**: 타이틀바는 비우고, 큰 제목을 위쪽에·목표 캡션을 아래쪽에 둔다. 마무리도 같은 구성.

### 8. 알약이 서명이다

| 위치 | 색 | 용도 |
|---|---|---|
| 좌상단 | orange | 용어 이름 (`픽셀 Pixel`) |
| 하단 중앙 | orange / pink | 발문 · 결론 · 빈칸 채우기 |
| 스크린샷 위 | pink | 화면 요소 이름표 |
| 타이틀바 왼쪽 | 챕터색 | 챕터 눈썹 라벨(자동) |

한 슬라이드에 알약 **최대 3개**.

**챕터 라벨은 타이틀바 왼쪽**에 산다. 본문이 아니라 제목 줄에 있어야
학생 눈이 "라벨 → 제목 → 내용" 한 방향으로 흐른다. 라벨은 그 챕터의 색으로 칠해져
색만 봐도 지금 어느 단원인지 안다. 제목은 라벨과 신호등을 뺀 남은 폭에 맞춰
**52 / 44 / 36px 중 자동으로** 골라진다.

라벨이 있는 슬라이드에는 **스티커를 붙이지 않는다.** 좌상단을 라벨이 이미 쓰고 있고,
장식이 겹치면 지저분해진다. 스티커는 라벨이 없는 표지·목표·간지·발문·마무리에만.

---

## 구성 규칙

### 전체 흐름

```
표지 → 학습목표 → [간지 → 개념 1~3장 → 활동] × 챕터 → 정리 → 공유 → 마무리
```

40분 = 12~16장, 80분 블록 = 24~34장. 챕터는 2~4개.

### 한 슬라이드 한 동작

앱 조작을 가르칠 때 **한 슬라이드에 한 동작만**.
"앱 찾기 → 화면 구성 → 캔버스 크기 → 도구 → 색 → 그리기 → 저장 → 내보내기"처럼
누르는 곳이 바뀌면 슬라이드도 바뀐다. 강조 링은 **1~2개까지**.

### 개념 구간

- 새 낱말은 반드시 `term` 슬라이드. 정의는 **한 문장 20자 이내**.
- 개념 뒤에 **"우리 주변에서 찾기"**(`bullets` + 발문 알약)를 붙여 학생 경험에 연결한다.
- 실험 결과는 `compare` 3열 + 하단 결론 알약.

### 초등 중저학년 글쓰기

- 한 줄 **20자**, 글머리표 **4개**, 활동 **3단계**, 슬라이드 전체 **100자** 이내
- **한자어·수동태를 쓰지 않는다** — "활용하여" → "써서", "수행한다" → "한다"
- 지시문은 동사로 끝낸다: "칸을 하나씩 칠한다"
- 상세 지도 내용은 슬라이드가 아니라 `notes` 로

이 수치들은 `kyo_build.py` 가 자동으로 검사한다. **경고 0건이 목표다.**

### 하지 말 것

- 이모지를 본문에 뿌리기 — 스티커 도형이 그 역할이다
- 외부 CDN 이미지·스크립트 — 단일 파일 원칙이 깨진다. 이미지는 base64만
- 저작권 불명 캐릭터 이미지 — 사용자가 준 자료만, 없으면 도형으로 대체
- 스티커·낙서를 손으로 배치 — `kyo_build.py` 가 안전 슬롯에 자동 배치한다

---

## 이미지

실제 교안은 절반 이상이 앱 스크린샷이다. 그냥 넣으면 파일이 20MB를 넘는다.

```bash
python3 kyo_images.py shots/ images.json --max 1400 --quality 82
```

긴 변 1400px + WebP로 원본의 3~8%까지 줄인다. 총합 12MB를 넘으면 경고가 뜬다
(아티팩트 한도 16MB). 넘으면 `--max 1100` 또는 스크린샷 수를 줄인다.

명세에서는 파일 이름(확장자 제외)으로 참조한다: `"image": "canvas-size"`.

**링 좌표는 이미지를 Read 로 직접 본 뒤 정한다.** 감으로 찍지 않는다.

작은 픽셀아트·도트 그림은 명세에 `"pixel": true` 를 넣는다. 확대해도 뭉개지지 않고
네모가 또렷하게 보인다. 스크린샷(`screenshot` 타입)은 원본 크기를 넘겨 확대하지 않는다.

---

## 폰트

**Paperlogy** (SIL Open Font License — 상업적 이용·수정·재배포·웹폰트 임베딩 허용,
폰트 단독 판매와 라이선스 변경만 금지).

1. 작업 환경에 `Paperlogy-7Bold.ttf` / `-4Regular.ttf` 가 있는지 찾는다.
2. 있으면 `python3 kyo_font.py Paperlogy-7Bold.ttf Paperlogy-4Regular.ttf deck.html`
   — **반드시 deck.html 을 함께 넘긴다.** 그 덱에 쓰인 글자만 서브셋한다.
3. 없으면 폴백 스택을 그대로 둔다(Black Han Sans / Jua / Gowun Dodum / Noto Sans KR).
4. **내장하지 못했으면 완성 보고에 한 줄로 알린다.**

> 아티팩트 게시 시 Google Fonts 외 폰트 호스트는 차단된다. jsDelivr·눈누 CDN 링크 금지.

---

## 검증 (건너뛰지 말 것)

1. `kyo_build.py` 규칙 경고 **0건**
2. `kyo_shoot.py` 로 전 슬라이드 캡처 → **PNG를 Read 로 직접 본다**
   - 텍스트가 넘치거나 3줄로 터지지 않았나
   - 스티커가 글자를 가리지 않나
   - 링이 스크린샷의 엉뚱한 곳을 가리키지 않나
   - 파스텔 위에 흰 글씨가 없나
3. Playwright가 없으면 브라우저로 직접 확인하고, **검증을 건너뛰었다고 사용자에게 알린다**

넘침이 나오면 **폰트를 줄이지 말고 내용을 줄인다.**

---

---

## 명세(deck.json) 레퍼런스


`kyo_build.py` 가 읽는 형식. **HTML을 손으로 쓰지 말고 이 명세를 쓴다.**
색 순환·스티커 배치·눈썹 라벨·타이머·가독성 검사는 전부 build.py가 처리한다.

```bash
python3 kyo_images.py shots/ images.json      # 스크린샷이 있을 때만
python3 kyo_build.py deck.json deck.html --images images.json
```

### 최상위

```jsonc
{
  "meta": {
    "program":     "2026년 디지털 교육 프로그램",  // 표지 상단(사업명)
    "course":      "드로잉 게임메이커\n: 내가 만드는 디지털게임", // 표지 중간(과정명), \n 로 줄바꿈
    "lessonNo":    "1",
    "lessonTitle": "네모로 그리는 픽셀아트",                  // 표지 하단(차시명)
    "next":        "2. 픽셀아트로 캐릭터 만들기",             // 마무리 슬라이드
    "grade":       "초등 3~4학년",
    "minutes":     80
  },
  "chapters": [                       // color 를 비우면 orange→pink→purple→mint 자동 순환
    {"name":"1. 픽셀이란", "color":"orange"},
    {"name":"2. 앱 익히기"}
  ],
  "slides": [ ... ]
}
```

> **차시 시리즈**: `meta` 와 `chapters` 를 `deck.meta.json` 하나로 빼고 차시별 JSON에서 합치면
> 12차시 내내 사업명·과정명·색 순서가 자동으로 일치한다.

### 슬라이드 공통 키

| 키 | 설명 |
|---|---|
| `type` | 필수. 아래 표 참조 |
| `chapter` | 이 슬라이드부터 챕터가 바뀔 때만. 안 쓰면 앞 슬라이드 챕터를 이어받는다 |
| `title` | 창 제목 |
| `notes` | 발표자 노트(`N` 키). 상세 지도 내용은 전부 여기로 |
| `color` | 챕터 색을 무시하고 강제할 때만 (거의 쓸 일 없음) |
| `pixel` | `true` 면 그 슬라이드의 이미지를 픽셀 그대로 또렷하게 확대 (도트·픽셀아트용) |

### type 목록

| type | 필수 키 | 선택 키 | 쓰임 |
|---|---|---|---|
| `cover` | — | — | 표지. meta 3단이 자동으로 들어간다 |
| `goals` | `items[]` (2~3) | `title` | 학습 목표 알약 바 |
| `divider` | `title` | `sub`, `chapter` | 챕터 간지(색면) |
| `term` | `title`,`term`,`def` | `image`,`alt` | 용어 정의 — 새 낱말은 무조건 이것 |
| `bullets` | `title`,`items[]` (≤4) | `pill` | 본문 글머리표 |
| `cards` | `title`,`items[{h,p,color}]` (2~4) | `pill` | 카드 비교 |
| `screenshot` | `title`,`image`,`rings[]` | `alt` | 앱 화면 + 강조 링 (링 ≤2) |
| `compare` | `title`,`items[{image,label}]` | `pill` | 결과물 3열 비교 |
| `gallery` | `title`,`images[]` | `cols`,`pill` | 사진 모음 + 발문 |
| `ask` | `q` | `title`,`notes`(예상답변) | 발문(색면) |
| `activity` | `title`,`steps[]` (≤3),`timer` | — | 활동. 색은 항상 노랑 |
| `quiz` | `title`,`items[]` | `pill` | O·X 형성평가 |
| `share` | `title`,`pill` | `image`,`q` | 발표·공유(빈칸 채우기) |
| `outro` | — | `title` | 마무리. `meta.next` 가 들어간다 |

### `rings` (screenshot)

좌표는 **이미지 기준 %**. 라벨 위치 `lx`/`ly` 는 라벨 중심점이다.

```jsonc
"rings": [
  {"x":12, "y":15, "w":37, "h":68, "label":"캔버스", "lx":30, "ly":92}
]
```

> 좌표는 눈으로 정한다: **이미지를 Read 로 먼저 본 뒤** 값을 넣고, 빌드 후 캡처로 확인한다.

### kyo_build.py 가 자동으로 하는 일

- 챕터 색 순환, 활동 슬라이드 노랑 고정
- 눈썹 라벨(챕터명 칩)을 **타이틀바 왼쪽**에 챕터 색으로 삽입 — 표지·목표·간지·발문·마무리 제외
- 제목 크기를 라벨·신호등을 뺀 남은 폭에 맞춰 52/44/36px 중 자동 선택
- 스티커 자동 배치 — **눈썹 라벨이 있는 슬라이드에는 붙이지 않는다.** 라벨 없는 레이아웃에서만,
  악센트와 다른 색으로, 앞 슬라이드와 조합이 겹치지 않게
- 낙서 선: 여백이 넉넉한 레이아웃(표지·간지·발문·마무리·목표)에만 좌우 번갈아
- 색면 3연속 경고 (사이에 흰 배경 슬라이드를 넣게)
- **제목·과정명 글자 크기 자동 맞춤** — 줄 폭을 한글 1.0em / 영숫자 0.55em / 공백 0.32em 로 계산해
  들어가는 가장 큰 크기를 고른다. 표지 과정명은 `\n` 으로 끊을수록 크게 나온다
- **표지 오브젝트 일러스트**(연필·마우스·키보드) 자동 배치 — 핑크 패널을 좌우로 들여 그 자리를 만든다
- 간지·마무리는 제목을 위쪽, 캡션을 아래쪽에 배치 (원본 교안 구성)
- 아이콘·일러스트 외곽선을 확대 배율과 무관하게 **항상 2.5px** 로 고정
- 그림(스크린샷 제외)을 남는 공간에 맞춰 키움 — `term` 에 그림이 없으면 가운데로 모음

### kyo_build.py 가 경고하는 것 (초등 중저학년 기준)

| 검사 | 기준 |
|---|---|
| 한 줄 글자 수 | 20자 (한글 기준 폭으로 계산) |
| 글머리표 개수 | 4개 |
| 활동 단계 | 3단계 |
| 학습 목표 | 3개 |
| 카드 제목 첫 줄 | 8자 (`\n` 으로 끊기) |
| 슬라이드 전체 글자 수 | 100자 |
| 강조 링 | 2개 |
| 어려운 낱말 | 활용·수행·구현·적용·인지·산출·도출·기입 등 |
| 활동에 타이머 없음 / 발문에 예상답변 없음 | — |

**경고가 0건이 될 때까지 명세를 고친다.** 폰트를 줄여서 해결하지 않는다.


---

# 부록 A — `kyo_template.html`

덱 엔진. **직접 수정하지 않는다.** 크기·색을 바꿔야 하면 `:root` 토큰만 손댄다.

````html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{DECK_TITLE}}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Jua&family=Gowun+Dodum&family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
<!-- FONT-FACE -->
<style>
/* ========== 디자인 토큰 ==========
   색은 팔레트 밖으로 나가지 않는다. 새 색을 추가하지 말 것.
   본문 글자색은 항상 --ink. 파스텔 위 흰 글씨는 금지(대비 2.06:1). */
:root{
  /* surface */
  --bg:#FFF8F7; --grid:#F5DBDC; --white:#FFFFFF; --soft:#FDF2F1;
  /* ink */
  --ink:#152A20;
  /* color blocks */
  --pink:#FC999F; --purple:#D6BDF7; --orange:#FFD4A8;
  --yellow:#FAE5A8; --mint:#9CF0E5; --green:#D2FABB;
  --accent:var(--pink);

  /* spacing — 8px 기반 */
  --s-xxs:4px; --s-xs:8px; --s-sm:12px; --s-md:16px;
  --s-lg:24px; --s-xl:32px; --s-xxl:48px;

  /* radius */
  --r-sm:8px; --r-md:16px; --r-lg:24px; --r-xl:32px; --r-pill:999px;

  --bw:2.5px;
  --font-title:"Paperlogy","Black Han Sans","Jua","Pretendard","Noto Sans KR",sans-serif;
  --font-body:"Paperlogy","Gowun Dodum","Pretendard","Noto Sans KR",sans-serif;
  --font-label:"Paperlogy","Jua","Pretendard","Noto Sans KR",sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;overflow:hidden;background:#241d1b}
body{font-family:var(--font-body);color:var(--ink);display:grid;place-items:center}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}

/* ========== 무대 ========== */
#stage{width:1280px;height:720px;position:relative;transform-origin:center center;
  background-color:var(--bg);
  background-image:linear-gradient(var(--grid) 1px,transparent 1px),
                   linear-gradient(90deg,var(--grid) 1px,transparent 1px);
  background-size:72px 72px;overflow:hidden}
section{position:absolute;inset:0;padding:var(--s-xl) 40px;display:none;flex-direction:column}
section.is-active{display:flex;animation:pop .22s ease-out}
@keyframes pop{from{opacity:0;transform:scale(.99)}to{opacity:1;transform:none}}
#bar{position:absolute;left:0;top:0;height:6px;background:var(--ink);z-index:30;
  transition:width .25s ease;opacity:.85}

/* ========== 브라우저 창 ========== */
.win{flex:1;min-height:0;display:flex;flex-direction:column;border:var(--bw) solid var(--ink);
  border-radius:var(--r-lg);background:var(--white);position:relative}
.win__bar{display:grid;grid-template-columns:minmax(0,1fr) auto minmax(0,1fr);
  align-items:center;gap:var(--s-sm);padding:10px var(--s-lg);
  background:var(--bg);border-bottom:var(--bw) solid var(--ink);
  border-radius:calc(var(--r-lg) - 2px) calc(var(--r-lg) - 2px) 0 0;min-height:70px;flex:none}
.win__bar h1,.win__bar h2{justify-self:center;min-width:0;text-align:center;
  font-family:var(--font-title);font-size:52px;line-height:1.1;letter-spacing:-.025em;white-space:nowrap}
.win__bar h1.sm{font-size:44px}
.win__bar h1.xs{font-size:36px;white-space:normal;line-height:1.15}
.barleft{justify-self:start;min-width:0;display:flex}
.dots{display:flex;gap:10px;justify-self:end;flex:none}
.dots i{width:19px;height:19px;border-radius:50%;border:var(--bw) solid var(--ink);display:block}
.dots i:nth-child(1){background:var(--yellow)}
.dots i:nth-child(2){background:var(--pink)}
.dots i:nth-child(3){background:var(--mint)}
.win__body{flex:1;min-height:0;display:flex;flex-direction:column;padding:var(--s-lg) var(--s-xxl);
  overflow:hidden;border-radius:0 0 calc(var(--r-lg) - 2px) calc(var(--r-lg) - 2px)}
.win--fill .win__body{background:var(--accent)}
.win__body.center{align-items:center;justify-content:center}
.divider-title{flex:1;min-height:0;display:grid;place-items:center;width:100%}
.win__body.divider{align-items:center;padding-bottom:var(--s-xxl)}
.win__body.divider .caption{width:68%;font-size:46px}
.win__body.tight{padding:var(--s-md) var(--s-lg)}
.termblock{flex:1;min-height:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:var(--s-xl);text-align:center}

/* 눈썹 라벨 — 타이틀바 왼쪽. 지금 어느 챕터인지 늘 보인다 */
.eyebrow{font-family:var(--font-label);font-size:25px;line-height:1.2;white-space:nowrap;
  letter-spacing:.02em;background:var(--accent);border:2px solid var(--ink);color:var(--ink);
  border-radius:var(--r-pill);padding:5px 20px;overflow:hidden;text-overflow:ellipsis}

/* ========== 타이포 ==========
   크기가 아니라 굵기로 위계를 만든다. 본문은 34px 아래로 내리지 않는다. */
.big{font-family:var(--font-title);font-size:104px;line-height:1.05;text-align:center;letter-spacing:-.035em}
.big.sm{font-size:84px} .big.xs{font-size:68px} .big.xxs{font-size:56px}
.mid{font-family:var(--font-title);font-size:66px;line-height:1.3;text-align:center}
.lead{font-size:42px;line-height:1.45;font-weight:500}
.lead.center{text-align:center}
b,strong{font-family:var(--font-title);font-weight:700}

/* 알약 — 이 스타일의 서명. 글자색은 언제나 잉크. */
.pill{display:inline-block;background:var(--orange);color:var(--ink);border-radius:var(--r-pill);
  padding:12px var(--s-xl);font-family:var(--font-title);font-size:44px;line-height:1.25}
.pill.lg{font-size:58px;padding:16px 40px}
.pill.sm{font-size:34px;padding:8px 24px}
.pill.pink{background:var(--pink)} .pill.mint{background:var(--mint)}
.pill.yellow{background:var(--yellow)} .pill.purple{background:var(--purple)}
.win__body>.pill{align-self:flex-start}
.pillrow{display:flex;justify-content:center;margin-top:auto;padding-top:var(--s-md);flex:none}

.goals{flex:1;min-height:0;display:flex;flex-direction:column;justify-content:center;gap:var(--s-xxl)}
.goal{border-radius:var(--r-pill);padding:32px 48px;font-family:var(--font-title);font-size:46px;
  line-height:1.3;text-align:center;color:var(--ink)}
.goal:nth-child(1){background:var(--orange)}
.goal:nth-child(2){background:var(--pink)}
.goal:nth-child(3){background:var(--purple)}

ul.bullets{list-style:none;display:flex;flex-direction:column;gap:var(--s-lg);justify-content:center;flex:1;min-height:0}
ul.bullets li{font-size:42px;line-height:1.4;padding-left:52px;position:relative}
ul.bullets li::before{content:"";position:absolute;left:0;top:.30em;width:28px;height:28px;
  border:var(--bw) solid var(--ink);border-radius:var(--r-sm);background:var(--accent)}
ol.steps{list-style:none;counter-reset:s;display:flex;flex-direction:column;gap:var(--s-lg);flex:1;min-height:0;justify-content:center}
ol.steps li{counter-increment:s;font-size:42px;line-height:1.4;padding-left:80px;position:relative}
ol.steps li::before{content:counter(s);position:absolute;left:0;top:-4px;width:56px;height:56px;
  display:grid;place-items:center;font-family:var(--font-title);font-size:32px;
  border:var(--bw) solid var(--ink);border-radius:50%;background:var(--accent)}
.caption{background:var(--bg);border:var(--bw) solid var(--ink);border-radius:var(--r-md);
  padding:20px var(--s-xl);font-size:42px;font-family:var(--font-body);text-align:center;flex:none}

/* ========== 카드 ========== */
.cards{flex:1;min-height:0;display:grid;grid-template-columns:repeat(var(--n,3),1fr);gap:var(--s-lg);align-items:stretch}
.card{border:var(--bw) solid var(--ink);border-radius:var(--r-lg);padding:var(--s-lg);display:flex;
  flex-direction:column;justify-content:center;align-items:center;text-align:center;gap:10px}
.card h3{font-family:var(--font-title);font-size:40px;line-height:1.25}
.card p{font-size:30px;line-height:1.45}
.card:nth-child(1){background:var(--pink)}
.card:nth-child(2){background:var(--orange)}
.card:nth-child(3){background:var(--purple)}
.card:nth-child(4){background:var(--mint)}

/* ========== 미디어 / 콜아웃 ========== */
.media{flex:1;min-height:0;position:relative;display:flex;align-items:center;justify-content:center}
.media img{max-width:100%;max-height:100%;object-fit:contain;display:block}
.media img:not(.framed){width:100%;height:100%}
.media img.framed{border:var(--bw) solid var(--ink);border-radius:var(--r-md)}
img.px{image-rendering:pixelated}
.shot{position:relative;display:inline-block;max-width:100%;max-height:100%;line-height:0}
.shot img{max-width:100%;max-height:100%;object-fit:contain;display:block}
.gallery{flex:1;min-height:0;display:grid;gap:var(--s-md);align-items:center;justify-items:center;
  grid-template-columns:repeat(var(--n,4),1fr)}
.gallery img{width:100%;height:100%;object-fit:contain}
.ring{position:absolute;border:5px solid var(--pink);border-radius:var(--r-lg);pointer-events:none}
.tag{position:absolute;background:var(--pink);color:var(--ink);border-radius:var(--r-md);
  padding:8px 24px;font-family:var(--font-title);font-size:34px;line-height:1.2;
  text-align:center;pointer-events:none;white-space:nowrap;transform:translate(-50%,-50%)}
.compare{flex:1;min-height:0;display:grid;grid-template-columns:repeat(var(--n,3),1fr);
  gap:20px;align-items:end;justify-items:center}
.compare figure{display:flex;flex-direction:column;align-items:center;gap:var(--s-sm);height:100%;min-height:0;justify-content:flex-end}
.compare img{width:100%;height:100%;object-fit:contain;min-height:0}

/* ========== 표지 ========== */
.shadowbox{position:relative;display:inline-block;max-width:100%}
.shadowbox::before{content:"";position:absolute;inset:20px -10px -18px 10px;background:var(--green);
  border:var(--bw) solid var(--ink);border-radius:var(--r-lg)}
.shadowbox>*{position:relative;background:var(--yellow);border:var(--bw) solid var(--ink);
  border-radius:var(--r-lg);padding:var(--s-xl) 40px}
.lesson{font-family:var(--font-title);font-size:58px;line-height:1.2;text-align:center;color:var(--ink);
  background:var(--white);border:var(--bw) solid var(--ink);border-radius:var(--r-pill);padding:12px 52px}
.lesson em{font-style:normal;opacity:.55;margin-right:var(--s-sm)}

/* ========== 장식 ========== */
.sticker{position:absolute;z-index:5;pointer-events:none}
.sticker svg{display:block;overflow:visible}
.sticker path,.sticker circle,.sticker polygon,.sticker rect,.sticker ellipse{
  stroke:var(--ink);stroke-width:2.5;stroke-linejoin:round;stroke-linecap:round;
  vector-effect:non-scaling-stroke}
.obj{position:absolute;z-index:4;pointer-events:none}
.obj svg{display:block;overflow:visible}
.obj path,.obj rect,.obj circle,.obj ellipse,.obj line{
  stroke:var(--ink);stroke-width:2.5;stroke-linejoin:round;stroke-linecap:round;
  vector-effect:non-scaling-stroke}
.doodle{position:absolute;z-index:0;pointer-events:none}
.doodle path{fill:none;stroke:var(--ink);stroke-width:2;stroke-linecap:round}

/* ========== 타이머 ========== */
.timer{display:flex;align-items:center;gap:var(--s-md);justify-content:center;margin-top:auto;padding-top:var(--s-md);flex:none}
.timer__face{font-family:var(--font-title);font-size:78px;min-width:220px;text-align:center;
  background:var(--white);border:var(--bw) solid var(--ink);border-radius:var(--r-md);padding:4px 18px;
  font-variant-numeric:tabular-nums}
.timer button{font-family:var(--font-title);font-size:30px;min-height:48px;padding:10px var(--s-lg);cursor:pointer;
  background:var(--yellow);border:var(--bw) solid var(--ink);border-radius:var(--r-pill);color:var(--ink)}
.timer button:active{transform:translateY(2px)}
.timer.is-done .timer__face{background:var(--pink);animation:blink 1s steps(2) infinite}
@keyframes blink{50%{background:var(--white)}}

/* ========== 화면 밖 조작 UI ========== */
#hud{position:fixed;left:0;right:0;bottom:0;display:flex;align-items:center;gap:var(--s-sm);
  padding:var(--s-xs) var(--s-md);color:#fff;font-size:14px;font-family:var(--font-label);
  background:linear-gradient(transparent,rgba(0,0,0,.45));pointer-events:none;z-index:20}
#hud .chapter{opacity:.75} #hud .count{margin-left:auto;opacity:.75}
.navbtn{position:fixed;top:50%;transform:translateY(-50%);z-index:25;width:64px;height:96px;
  border:none;border-radius:var(--r-md);background:rgba(255,255,255,.10);color:#fff;font-size:34px;
  cursor:pointer;opacity:0;transition:opacity .2s}
body:hover .navbtn{opacity:.5}
.navbtn:hover{opacity:1!important;background:rgba(255,255,255,.22)}
.navbtn:focus-visible{opacity:1;outline:3px solid #fff}
#prev{left:10px} #next{right:10px}
#notes{position:fixed;left:0;right:0;bottom:0;max-height:36vh;overflow:auto;padding:18px var(--s-lg) 34px;
  background:#1c1714;color:#f6efe9;font-size:17px;line-height:1.65;display:none;z-index:22;border-top:2px solid #4a403a}
body.show-notes #notes{display:block}
#toc{position:fixed;inset:0;background:rgba(20,16,14,.96);display:none;z-index:40;padding:40px;overflow:auto}
body.show-toc #toc{display:block}
#toc h2{color:#fff;font-family:var(--font-label);font-size:26px;margin-bottom:20px;text-align:center}
#toc ol{list-style:none;display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:10px;max-width:1100px;margin:0 auto}
#toc button{width:100%;text-align:left;display:flex;gap:var(--s-sm);align-items:baseline;cursor:pointer;
  background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.14);border-radius:var(--r-sm);
  color:#f6efe9;font:inherit;font-size:16px;padding:12px 14px;min-height:44px}
#toc button:hover,#toc button:focus-visible{background:rgba(255,255,255,.2);outline:none}
#toc button .n{font-family:var(--font-label);opacity:.6;min-width:26px}
#toc button .c{margin-left:auto;font-size:12px;opacity:.55}
#help{position:fixed;inset:0;background:rgba(20,16,14,.95);color:#fff;display:none;
  place-items:center;font-size:20px;line-height:2.1;z-index:45;text-align:center}
body.show-help #help{display:grid}
kbd{background:#3a322d;border-radius:6px;padding:3px 11px;font-family:inherit;font-size:.9em}

@media print{
  html,body{overflow:visible;background:#fff}
  #hud,#notes,#help,#toc,#bar,.navbtn{display:none!important}
  #stage{transform:none!important}
  section{display:flex!important;position:relative;page-break-after:always;width:1280px;height:720px}
}
</style>
</head>
<body>

<div id="stage">
  <div id="bar"></div>
<!-- SLIDES -->
</div>

<button class="navbtn" id="prev" aria-label="이전 슬라이드">‹</button>
<button class="navbtn" id="next" aria-label="다음 슬라이드">›</button>

<div id="hud"><span class="chapter"></span><span class="count"></span></div>
<div id="notes"></div>
<div id="toc"><h2>목차 — 눌러서 이동 (O 키로 닫기)</h2><ol></ol></div>
<div id="help"><div>
  <kbd>→</kbd> <kbd>Space</kbd> 다음 &nbsp; <kbd>←</kbd> 이전<br>
  <kbd>O</kbd> 목차 &nbsp; <kbd>N</kbd> 발표자 노트 &nbsp; <kbd>F</kbd> 전체화면<br>
  <kbd>B</kbd> 화면 가리기 &nbsp; <kbd>Home</kbd> 처음으로<br>
  <kbd>?</kbd> 또는 <kbd>Esc</kbd> 닫기
</div></div>

<script>
(function(){
  const stage=document.getElementById('stage');
  const slides=[...stage.querySelectorAll('section')];
  const hudC=document.querySelector('#hud .chapter'), hudN=document.querySelector('#hud .count');
  const notes=document.getElementById('notes'), bar=document.getElementById('bar');
  let i=0, blank=false;

  function fit(){ stage.style.transform='scale('+Math.min(innerWidth/1280,innerHeight/720)+')'; }
  addEventListener('resize',fit); fit();

  const tocList=document.querySelector('#toc ol');
  slides.forEach((s,k)=>{
    const t=s.dataset.title||s.querySelector('h1,h2,.big,.mid')?.textContent.trim()||'슬라이드';
    const li=document.createElement('li');
    li.innerHTML='<button><span class="n">'+(k+1)+'</span><span>'+t+'</span>'+
      (s.dataset.chapter?'<span class="c">'+s.dataset.chapter+'</span>':'')+'</button>';
    li.querySelector('button').onclick=()=>{show(k);document.body.classList.remove('show-toc')};
    tocList.appendChild(li);
  });

  function show(n){
    i=Math.max(0,Math.min(slides.length-1,n));
    slides.forEach((s,k)=>s.classList.toggle('is-active',k===i));
    const s=slides[i];
    hudC.textContent=s.dataset.chapter||'';
    hudN.textContent=(i+1)+' / '+slides.length;
    notes.textContent=s.dataset.notes||'(발표자 노트 없음)';
    bar.style.width=((i+1)/slides.length*100)+'%';
    bar.style.background=getComputedStyle(s).getPropertyValue('--accent')||'#152A20';
    history.replaceState(null,'','#s'+(i+1));
    resetTimer(s);
  }
  const go=d=>show(i+d);

  addEventListener('keydown',e=>{
    const k=e.key;
    if(k==='ArrowRight'||k===' '||k==='PageDown'){go(1);e.preventDefault();}
    else if(k==='ArrowLeft'||k==='PageUp'){go(-1);e.preventDefault();}
    else if(k==='Home'){show(0);} else if(k==='End'){show(slides.length-1);}
    else if(k==='f'||k==='F'){document.documentElement.requestFullscreen?.();}
    else if(k==='n'||k==='N'){document.body.classList.toggle('show-notes');}
    else if(k==='o'||k==='O'){document.body.classList.toggle('show-toc');}
    else if(k==='b'||k==='B'){blank=!blank;stage.style.visibility=blank?'hidden':'visible';}
    else if(k==='?'){document.body.classList.toggle('show-help');}
    else if(k==='Escape'){document.body.classList.remove('show-help','show-toc');}
  });
  document.getElementById('prev').onclick=()=>go(-1);
  document.getElementById('next').onclick=()=>go(1);
  stage.addEventListener('click',e=>{ if(!e.target.closest('button')) go(1); });

  let x0=null;
  addEventListener('touchstart',e=>{x0=e.changedTouches[0].clientX},{passive:true});
  addEventListener('touchend',e=>{
    if(x0===null)return; const dx=e.changedTouches[0].clientX-x0; x0=null;
    if(Math.abs(dx)>60) go(dx<0?1:-1);
  },{passive:true});

  let tick=null;
  function resetTimer(sec){
    clearInterval(tick);
    const box=sec.querySelector('.timer'); if(!box) return;
    const mins=+sec.dataset.timer||5;
    const face=box.querySelector('.timer__face'), btn=box.querySelector('button');
    let left=mins*60, running=false;
    box.classList.remove('is-done');
    const paint=()=>face.textContent=String(Math.floor(left/60)).padStart(2,'0')+':'+String(left%60).padStart(2,'0');
    paint(); btn.textContent='시작';
    btn.onclick=ev=>{
      ev.stopPropagation();
      if(running){clearInterval(tick);running=false;btn.textContent='계속';return;}
      running=true;btn.textContent='멈춤';
      tick=setInterval(()=>{ left--; paint();
        if(left<=0){clearInterval(tick);running=false;box.classList.add('is-done');btn.textContent='다시';left=mins*60;}
      },1000);
    };
  }

  const start=parseInt((location.hash||'').replace('#s',''),10);
  show(Number.isFinite(start)&&start>0?start-1:0);
})();
</script>
</body>
</html>

````

---

# 부록 B — `kyo_build.py`

명세를 HTML로 찍고 초등 가독성 규칙을 검사한다. `kyo_template.html` 과 같은 폴더에 둔다.

````python
#!/usr/bin/env python3
"""슬라이드 명세(JSON) → 교안 HTML 한 파일.

    python3 kyo_build.py deck.json deck.html [--images images.json]

명세만 고치면 마크업은 이 스크립트가 찍는다. 스티커·낙서 배치, 챕터 색 순환,
초등 가독성 규칙 검사는 전부 자동이다. 규칙 위반은 stderr 에 경고로 나온다.
스펙 형식은 스킬 문서의 "명세 레퍼런스" 절 참고.
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

    tpl = (HERE / 'kyo_template.html').read_text(encoding='utf-8')
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

````

---

# 부록 C — `kyo_shoot.py`

전 슬라이드를 PNG로 캡처하고 넘침을 자동 검사한다. **캡처한 PNG는 반드시 Read 로 눈으로 본다.**

````python
#!/usr/bin/env python3
"""덱의 전 슬라이드를 PNG로 캡처한다 (빌드 검증용).

사용법:  python3 kyo_shoot.py deck.html out/
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

````

---

# 부록 D — `kyo_images.py`

스크린샷 폴더를 리사이즈·WebP 압축해 base64 로 만든다. 스크린샷이 있을 때만 쓴다.

````python
#!/usr/bin/env python3
"""스크린샷 폴더 → 리사이즈·압축·base64 → images.json

    python3 kyo_images.py shots/ images.json [--max 1400] [--quality 82]

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

````

---

# 부록 E — 골든 샘플 명세

새 덱을 쓰기 전에 이 명세를 읽고 **밀도·문장 길이·챕터 리듬**의 기준을 잡는다.
(픽셀아트 1차시 · 80분 블록 · 15장. `zoom`/`app`/`heart5`… 는 이미지 키 예시)

````json
{
 "meta": {
  "program": "2026년 디지털 교육 프로그램",
  "course": "드로잉 게임메이커\n: 내가 만드는 디지털게임",
  "lessonNo": "1",
  "lessonTitle": "네모로 그리는 픽셀아트",
  "next": "2. 픽셀아트로 캐릭터 만들기",
  "grade": "초등 3~4학년",
  "minutes": 80
 },
 "chapters": [
  {
   "name": "1. 픽셀이란",
   "color": "orange"
  },
  {
   "name": "2. 앱 익히기",
   "color": "pink"
  },
  {
   "name": "3. 칸 늘리기",
   "color": "purple"
  },
  {
   "name": "4. 공유",
   "color": "mint"
  }
 ],
 "slides": [
  {
   "type": "cover",
   "notes": "인사 → 오늘은 작은 네모로 그림을 그려 본다고 예고한다."
  },
  {
   "type": "goals",
   "items": [
    "디지털 그림은 작은 네모로 되어 있어요.",
    "칸 수에 따라 그림이 달라져요."
   ],
   "notes": "두 문장을 다 함께 소리 내어 읽는다."
  },
  {
   "type": "divider",
   "chapter": "1. 픽셀이란",
   "title": "디지털 그림의 비밀",
   "sub": "픽셀에 대해 알아봐요"
  },
  {
   "type": "term",
   "title": "픽셀이 뭘까요?",
   "term": "픽셀 Pixel",
   "def": "그림을 이루는 작은 네모 한 칸",
   "image": "zoom",
   "alt": "체커보드를 확대해 네모 한 칸을 보여 주는 도해",
   "notes": "화면에 눈을 가까이 대면 네모가 보인다고 이야기해 준다.",
   "pixel": true
  },
  {
   "type": "bullets",
   "title": "어디에 픽셀이 있을까?",
   "items": [
    "교실 TV 화면",
    "태블릿과 휴대폰 화면",
    "사진기로 찍은 사진"
   ],
   "pill": "또 어디에서 봤어요?",
   "notes": "교실에 있는 화면을 직접 가리키게 한다."
  },
  {
   "type": "divider",
   "chapter": "2. 앱 익히기",
   "title": "직접 그려 봐요",
   "sub": "픽셀 그리기 앱을 열어요"
  },
  {
   "type": "screenshot",
   "title": "화면 살펴보기",
   "image": "app",
   "alt": "픽셀 그리기 앱 화면",
   "rings": [
    {
     "x": 12,
     "y": 15,
     "w": 37,
     "h": 68,
     "label": "캔버스",
     "lx": 30,
     "ly": 92
    },
    {
     "x": 67,
     "y": 11,
     "w": 31,
     "h": 80,
     "label": "색과 도구",
     "lx": 82,
     "ly": 4
    }
   ],
   "notes": "학생 태블릿도 같은 화면인지 확인한 뒤 넘어간다."
  },
  {
   "type": "screenshot",
   "title": "칸을 5칸으로",
   "image": "app",
   "alt": "캔버스 크기를 정하는 화면",
   "rings": [
    {
     "x": 12,
     "y": 15,
     "w": 37,
     "h": 68,
     "label": "여기가 5칸 X 5칸",
     "lx": 30,
     "ly": 92
    }
   ],
   "notes": "숫자를 잘못 넣으면 뒤로 갔다 다시 오면 된다."
  },
  {
   "type": "activity",
   "title": "5칸에 하트 그리기",
   "timer": 12,
   "steps": [
    "색깔을 하나 고른다",
    "칸을 하나씩 칠한다",
    "하트가 되면 손을 든다"
   ],
   "notes": "색이 안 칠해지는 학생을 먼저 돕는다. 다 한 학생은 색을 바꿔 보게 한다."
  },
  {
   "type": "divider",
   "chapter": "3. 칸 늘리기",
   "title": "칸을 늘려 볼까?",
   "sub": "16칸, 32칸으로 다시 그려요"
  },
  {
   "type": "ask",
   "q": "칸이 많아지면\n하트가 어떻게 달라질까요?",
   "notes": "예상 답변: 더 예뻐진다 / 더 오래 걸린다 / 더 진짜 같다"
  },
  {
   "type": "activity",
   "title": "32칸으로 다시 그리기",
   "timer": 10,
   "steps": [
    "새 그림을 32칸으로 만든다",
    "같은 하트를 다시 그린다",
    "갤러리에 저장한다"
   ],
   "notes": "저장까지 마친 학생만 다음으로 넘어가게 한다."
  },
  {
   "type": "compare",
   "title": "무엇이 달라졌나요?",
   "items": [
    {
     "image": "heart5",
     "label": "5 X 5",
     "alt": "5칸 하트"
    },
    {
     "image": "heart16",
     "label": "16 X 16",
     "alt": "16칸 하트"
    },
    {
     "image": "heart32",
     "label": "32 X 32",
     "alt": "32칸 하트"
    }
   ],
   "pill": "칸이 많을수록 더 부드러워요",
   "notes": "학생 작품 세 개를 실제로 띄워 비교하면 더 좋다.",
   "pixel": true
  },
  {
   "type": "share",
   "chapter": "4. 공유",
   "title": "내 그림을 자랑해요",
   "image": "heart32",
   "alt": "학생 작품 예시",
   "pill": "내 그림은 ______ 칸이에요!",
   "notes": "두세 명만 앞에 나와 빈칸을 채워 발표한다.",
   "pixel": true
  },
  {
   "type": "outro",
   "notes": "태블릿 정리 안내 후 다음 차시 예고."
  }
 ]
}
````

---

# 부록 F — 선택 도구

## `kyo_font.py`

Paperlogy 를 덱에 쓰인 글자만 서브셋해 base64 로 내장한다.

````python
#!/usr/bin/env python3
"""Paperlogy(또는 임의의 한글 폰트)를 한글 서브셋 woff2로 줄여 base64 @font-face 로 출력.

사용법:
    pip install fonttools brotli --break-system-packages
    python3 kyo_font.py Paperlogy-7Bold.ttf Paperlogy-4Regular.ttf deck.html
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

````

## `kyo_topdf.py`

덱을 PDF로 내보낸다(배포·인쇄용).

````python
#!/usr/bin/env python3
"""덱 → PDF (배포·인쇄용).   python3 kyo_topdf.py deck.html deck.pdf"""
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

````
