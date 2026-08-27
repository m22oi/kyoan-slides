# 예시 명세

| 파일 | 내용 |
|---|---|
| `01-pixelart.json` | 픽셀아트 1차시 · 80분 블록 · 15장. 그림이 들어가는 레이아웃(term·compare·screenshot) 예시 |
| `02-coding-grade3.json` | 초3 코딩 1차시 · 80분 블록 · 16장. 그림 없이 텍스트만으로 만든 예시 |

## 빌드

```bash
# 그림 없는 예시 — 바로 됩니다
python3 ../skill/assets/build.py 02-coding-grade3.json deck.html

# 그림이 있는 예시 — 이미지를 먼저 만들어 넣습니다
python3 make_images.py                 # 하트·도해·앱 목업을 코드로 그림
python3 ../skill/assets/build.py 01-pixelart.json deck.html --images _images.json
```

`01-pixelart.json` 이 참조하는 `zoom` · `app` · `heart5` · `heart16` · `heart32` 는
`make_images.py` 가 코드로 그려 만듭니다. 저작권 걱정이 없는 이미지입니다.

실제 수업에서는 앱 스크린샷 폴더를 넣으세요.

```bash
python3 ../skill/assets/embed_images.py shots/ _images.json
```
