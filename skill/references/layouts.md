# 레이아웃 카탈로그 v2

`assets/template.html` 의 `<!-- SLIDES -->` 자리에 `<section>` 들을 순서대로 붙인다.

## section 공통 속성

```html
<section
  style="--accent:var(--orange)"   <!-- 이 슬라이드의 포인트색 (pink/orange/purple/mint/yellow) -->
  data-chapter="1. 픽셀이란"        <!-- 하단 HUD·목차에 표시되는 챕터 이름 -->
  data-title="픽셀이 뭘까요?"       <!-- 목차에 쓸 짧은 제목 (없으면 h1에서 자동 추출) -->
  data-notes="교사용 메모"          <!-- N 키로만 보임 -->
  data-timer="10">                 <!-- 활동 슬라이드에서 타이머 분 -->
```

공통 부품(스티커·낙서·신호등)은 문서 맨 아래 "부품" 절 참조.

---

## L1. 표지 — **3단 구조 고정**

상단 = 사업명 / 중간 = 과정명 / 하단 = 차시번호 + 차시명.

```html
<section style="--accent:var(--pink)" data-chapter="표지" data-title="표지"
         data-notes="인사, 지난 차시 한 줄 복습">
  <div class="win" style="border:none;background:none">
    <div class="win__bar" style="border:var(--bw) solid var(--ink);border-radius:var(--radius);padding-right:20px">
      <h2 style="font-size:30px;text-align:right">2026년 디지털 교육 프로그램</h2>
      <div class="dots"><i></i><i></i><i></i></div>
    </div>
    <div style="flex:1;min-height:0;margin-top:16px;background:var(--pink);
                border:var(--bw) solid var(--ink);border-radius:var(--radius);
                display:flex;flex-direction:column;align-items:center;justify-content:center;gap:44px;padding:40px">
      <div class="shadowbox"><div class="big sm">드로잉 게임메이커<br>: 내가 만드는 디지털게임</div></div>
      <div class="lesson"><em>1.</em>네모로 그리는 픽셀아트</div>
    </div>
  </div>
  <!-- 스티커 2개 -->
</section>
```

> 과정명이 한 줄이면 `.big`, 두 줄이면 `.big.sm`, 아주 길면 `.big.xs`.

## L2. 학습 목표 — **가로 알약 바** (기본형)

목표는 2~3개. 문장은 `~해요.` 로 끝내고 한 줄에 담는다.

```html
<section data-chapter="학습 목표" data-notes="다 함께 소리 내어 읽기">
  <div class="win">
    <div class="win__bar"><h1>학습 목표</h1><div class="dots"><i></i><i></i><i></i></div></div>
    <div class="win__body">
      <div class="goals">
        <div class="goal">디지털 그림이 작은 네모(픽셀)로 이루어진 것을 알아요.</div>
        <div class="goal">픽셀과 캔버스 크기에 따라 그림이 달라지는 걸 체험해요.</div>
      </div>
    </div>
  </div>
</section>
```

> 목표를 짧은 명사구로 쓰고 싶을 때만 카드 3장(L9)을 쓴다.

## L3. 간지 — 챕터마다 색을 바꾼다

```html
<section style="--accent:var(--orange)" data-chapter="1. 픽셀이란" data-title="디지털 그림의 비밀">
  <div class="win win--fill">
    <div class="win__bar"><h1></h1><div class="dots"><i></i><i></i><i></i></div></div>
    <div class="win__body center" style="gap:56px">
      <div class="big">디지털 그림의 비밀을 찾아서</div>
      <div class="caption" style="width:64%">픽셀에 대해 함께 알아봐요</div>
    </div>
  </div>
</section>
```

## L4. 용어 정의 — **좌상단 알약 태그 + 한 줄 정의 + 그림**

새 낱말을 소개하는 슬라이드는 항상 이 형태로.

```html
<section style="--accent:var(--orange)" data-chapter="1. 픽셀이란">
  <div class="win">
    <div class="win__bar"><h1>픽셀이 뭘까요?</h1><div class="dots"><i></i><i></i><i></i></div></div>
    <div class="win__body" style="gap:14px;align-items:flex-start">
      <span class="pill lg">픽셀 Pixel</span>
      <p class="lead">디지털 이미지의 가장 작은 단위로 네모 한 칸</p>
      <div class="media"><img src="data:image/png;base64,..." alt="픽셀 확대 도해"></div>
    </div>
  </div>
</section>
```

## L5. 스크린샷 + 콜아웃 — **실습 교안의 주력 레이아웃**

앱 화면을 보여주고 눌러야 할 곳을 분홍 링과 라벨로 짚는다.
`ring`/`tag` 좌표는 `%` 로 넣어 스케일에 안전하게.

```html
<section style="--accent:var(--pink)" data-chapter="2. 앱 익히기" data-title="캔버스 크기 바꾸기"
         data-notes="교사가 먼저 시연 → 학생 따라 하기">
  <div class="win">
    <div class="win__bar"><h1>캔버스 크기 바꾸기</h1><div class="dots"><i></i><i></i><i></i></div></div>
    <div class="win__body" style="padding:18px 24px">
      <div class="media">
        <span class="shot">
          <img class="framed" src="data:image/png;base64,..." alt="캔버스 크기 설정 화면">
          <span class="ring" style="left:44%;top:22%;width:20%;height:14%"></span>
          <span class="tag"  style="left:66%;top:24%">폭 · 높이에 5</span>
        </span>
      </div>
    </div>
  </div>
</section>
```

**필수**: `ring`/`tag` 는 반드시 `.shot` 안에 넣는다. `.media` 바로 아래에 두면 이미지가 아니라 빈 여백을 가리킨다.

**규칙**: 한 슬라이드에 링 1~2개까지. 3개 넘으면 슬라이드를 나눈다 (아래 "한 슬라이드 한 동작").

## L6. 결과 비교 3열 — 하단에 결론 알약

```html
<section style="--accent:var(--pink)" data-chapter="1. 픽셀이란" data-title="다른 점을 발견했나요?">
  <div class="win">
    <div class="win__bar"><h1>다른 점을 발견했나요?</h1><div class="dots"><i></i><i></i><i></i></div></div>
    <div class="win__body">
      <div class="compare" style="--n:3">
        <figure><img src="..." alt="5x5 하트"><span class="pill pink sm">5 X 5</span></figure>
        <figure><img src="..." alt="16x16 하트"><span class="pill pink sm">16 X 16</span></figure>
        <figure><img src="..." alt="32x32 하트"><span class="pill pink sm">32 X 32</span></figure>
      </div>
      <div class="pillrow"><span class="pill pink on-dark">픽셀이 많을수록 더 부드럽고 잘 보여요</span></div>
    </div>
  </div>
</section>
```

## L7. 갤러리 + 발문 알약

```html
<section style="--accent:var(--orange)" data-chapter="1. 픽셀이란" data-title="게임 속 그림 살펴보기">
  <div class="win">
    <div class="win__bar"><h1>게임 속 그림을 살펴봐요</h1><div class="dots"><i></i><i></i><i></i></div></div>
    <div class="win__body" style="padding:20px 28px">
      <div class="gallery" style="--n:5">
        <img src="..." alt=""><img src="..." alt=""><img src="..." alt="">
        <img src="..." alt=""><img src="..." alt="">
      </div>
      <div class="pillrow"><span class="pill">이 그림, 어디서 봤어요?</span></div>
    </div>
  </div>
</section>
```

## L8. 본문 글머리표

```html
<section style="--accent:var(--orange)" data-chapter="1. 픽셀이란">
  <div class="win">
    <div class="win__bar"><h1>코딩은 &lsquo;순서&rsquo;예요</h1><div class="dots"><i></i><i></i><i></i></div></div>
    <div class="win__body">
      <ul class="bullets">
        <li>한 줄로 끝나는 짧은 문장</li>
        <li>최대 5개까지만</li>
      </ul>
    </div>
  </div>
</section>
```

## L9. 카드 (2~4장)

```html
<div class="cards" style="--n:3">
  <div class="card"><h3>블록클리</h3><p>화면 속 캐릭터에게<br>길을 알려 주기</p></div>
  ...
</div>
```
카드 제목은 **한 줄 8자 이내**로 끊어 `<br>` 를 직접 넣는다.

## L10. 발문

```html
<section style="--accent:var(--mint)" data-chapter="1. 픽셀이란" data-title="생각해 봐요"
         data-notes="예상 답변: …">
  <div class="win win--fill">
    <div class="win__bar"><h1>생각해 봐요</h1><div class="dots"><i></i><i></i><i></i></div></div>
    <div class="win__body center"><div class="mid">게임에 규칙이 없으면<br>어떤 일이 벌어질까요?</div></div>
  </div>
</section>
```

## L11. 활동 (타이머 필수)

```html
<section style="--accent:var(--yellow)" data-chapter="3. 만들기" data-timer="12"
         data-title="활동 1. 미로 빠져나가기" data-notes="순회하며 지원">
  <div class="win">
    <div class="win__bar"><h1 class="sm">활동 1. 미로를 빠져나가자</h1><div class="dots"><i></i><i></i><i></i></div></div>
    <div class="win__body">
      <ol class="steps">
        <li>미로 1단계를 연다</li>
        <li>블록을 순서대로 놓는다</li>
        <li>실행을 눌러 확인하고 고친다</li>
      </ol>
      <div class="timer"><div class="timer__face">12:00</div><button type="button">시작</button></div>
    </div>
  </div>
</section>
```

## L12. 발표 · 공유 (빈칸 채우기)

```html
<section style="--accent:var(--orange)" data-chapter="4. 공유" data-title="내 작품 자랑하기">
  <div class="win">
    <div class="win__bar"><h1>내 캐릭터를 자랑해요!</h1><div class="dots"><i></i><i></i><i></i></div></div>
    <div class="win__body">
      <div class="media"><img src="..." alt="학생 작품 예시"></div>
      <div class="pillrow"><span class="pill">내 캐릭터는 ______ 이에요!</span></div>
    </div>
  </div>
</section>
```

## L13. 마무리

```html
<section style="--accent:var(--mint)" data-chapter="마무리" data-title="마무리">
  <div class="win win--fill">
    <div class="win__bar"><h1></h1><div class="dots"><i></i><i></i><i></i></div></div>
    <div class="win__body center" style="gap:40px">
      <div class="big">참 잘했어요</div>
      <div class="caption" style="width:72%;font-size:32px">다음 시간: 픽셀아트로 캐릭터 만들기</div>
    </div>
  </div>
</section>
```

---

# 부품

## 신호등
```html
<div class="dots"><i></i><i></i><i></i></div>
```

## 스티커 — 창 테두리에 걸치게

하트
```html
<span class="sticker" style="top:8px;left:110px;color:var(--mint)">
  <svg width="72" height="66" viewBox="0 0 24 22"><path fill="currentColor"
   d="M12 21S2 14.4 2 7.9A5.6 5.6 0 0 1 12 4.6 5.6 5.6 0 0 1 22 7.9C22 14.4 12 21 12 21z"/></svg>
</span>
```

별
```html
<span class="sticker" style="top:6px;left:120px;color:var(--orange)">
  <svg width="74" height="70" viewBox="0 0 24 23"><polygon fill="currentColor"
   points="12,1 15.2,8.2 23,9 17.2,14.2 18.9,22 12,18 5.1,22 6.8,14.2 1,9 8.8,8.2"/></svg>
</span>
```

스마일
```html
<span class="sticker" style="bottom:140px;right:-16px;color:var(--purple)">
  <svg width="78" height="78" viewBox="0 0 24 24">
    <circle cx="12" cy="12" r="10.5" fill="currentColor"/>
    <path d="M8.4 9.6v1.2M15.6 9.6v1.2" stroke-linecap="round"/>
    <path d="M8.6 14.4a4.4 4.4 0 0 0 6.8 0" fill="none" stroke-linecap="round"/>
  </svg>
</span>
```

## 낙서 선 (좌 / 우)
```html
<span class="doodle" style="left:-4px;top:300px"><svg width="120" height="210" viewBox="0 0 130 230">
  <path d="M118 4C70 26 6 40 22 74s76 6 66 44-64 26-58 62 60 30 82 46"/></svg></span>

<span class="doodle" style="right:-6px;top:230px"><svg width="120" height="200" viewBox="0 0 130 230">
  <path d="M12 4c48 22 112 36 96 70s-76 6-66 44 64 26 58 62-60 30-82 46"/></svg></span>
```

## 색 이름
`var(--pink)` `var(--orange)` `var(--purple)` `var(--mint)` `var(--yellow)` `var(--green)`
