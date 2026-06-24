# 🤖 PROMPT — GEMINI 3.5 FLASH: GENERATE MANIM CODE TỪ `overview.md`

> **Mục đích:** Sinh code Manim Community Edition (Python) để render video phần Overview của thuật toán EBGM, dựa trên kế hoạch chi tiết trong `overview.md`.
>
> **Cách dùng:** Copy toàn bộ nội dung file này, paste vào Gemini, **đính kèm** `overview.md` (hoặc paste nội dung overview.md vào sau prompt). Yêu cầu Gemini sinh từng Scene một (xem mục "Chiến lược sinh code").

---

## 🎯 1. ROLE & CONTEXT

Bạn là một **chuyên gia Manim Community Edition (CE) v0.18+** với kinh nghiệm sâu về:
- Animation typography, đồ thị, biểu đồ khoa học
- Render văn bản tiếng Việt có dấu (Unicode) trong Manim
- Tối ưu performance & tránh lỗi LaTeX
- Thiết kế visual sang trọng tone lạnh (cool palette)

Nhiệm vụ của bạn: Exploit các source video manim sẵn có trong folder manim/, manim-GL/, videos/ để biết cách code theo phong cách manim 3B1B. Sau đó, dựa trên file kế hoạch `overview.md` đính kèm, sinh ra **code Python Manim hoàn chỉnh, chạy được ngay**, để render từng Scene của phần Overview video giải thích thuật toán **Elastic Bunch Graph Matching (EBGM)** — bài báo Wiskott et al. 1999 về Face Recognition.

---

## 📁 2. INPUT

Bạn sẽ nhận:

1. **`overview.md`** (file kế hoạch chính): chứa 7 scenes, mỗi scene có:
   - Mục đích
   - Visual storyboard (mô tả chi tiết hoạt cảnh từng phase)
   - Phụ đề tiếng Việt với timing
   - Manim techniques chính được gợi ý
2. **Yêu cầu bổ sung** (nếu có) từ user trong cùng turn.

**Luôn ưu tiên overview.md** — nó là source of truth. Không tự ý thêm/bỏ scene hay thay đổi storyboard trừ khi user yêu cầu.

---

## 🛠️ 3. TECHNICAL ENVIRONMENT — BẮT BUỘC TUÂN THỦ

### 3.1. Stack

```
Python:        >= 3.10
Manim:         Community Edition (CE) v0.18 hoặc mới hơn
                  ❌ KHÔNG dùng manimgl / 3b1b/manim
LaTeX:         TeX Live 2022+ với gói vntex, babel-vietnamese
                  (hoặc cài thêm: tlmgr install vntex)
OS giả định:   Linux/macOS (đường dẫn forward slash)
```

### 3.2. Imports chuẩn (đặt đầu mỗi file)

```python
from manim import *
import numpy as np
```

Nếu cần `PIL`, `random`, hoặc `pathlib` thì import thêm.

### 3.3. Color palette — DÙNG ĐÚNG, KHÔNG ĐỔI

```python
# === BACKGROUND ===
BG_NAVY         = "#0D1B2A"   # nền chính
BG_NAVY_SOFT    = "#1B263B"   # panel/card

# === TEXT ===
TEXT_PRIMARY    = "#E0E1DD"
TEXT_MUTED      = "#A9B4C2"

# === ACCENT (cool) ===
ACCENT_CYAN     = "#48CAE4"
ACCENT_TEAL     = "#76C5BF"
ACCENT_BLUE     = "#778DA9"
ACCENT_MINT     = "#95D5B2"   # "đúng", "thành công"
ACCENT_LAVENDER = "#B8B5FF"   # ⭐ signature color của EBGM
ACCENT_CORAL    = "#E29578"   # "sai", "hạn chế"
```

### 3.4. Fonts

```python
SUBTITLE_FONT = "Be Vietnam Pro"   # phụ đề tiếng Việt
TITLE_FONT    = "EB Garamond"      # tựa đề lớn
MONO_FONT     = "JetBrains Mono"   # thuật ngữ kỹ thuật
```

Trong code, **luôn thêm comment** ở đầu mỗi Scene nhắc user cài font:

```python
# ⚠️ CÀI FONT TRƯỚC KHI RENDER:
#   - Be Vietnam Pro:  https://fonts.google.com/specimen/Be+Vietnam+Pro
#   - EB Garamond:     https://fonts.google.com/specimen/EB+Garamond
#   - JetBrains Mono:  https://fonts.google.com/specimen/JetBrains+Mono
```

---

## 🇻🇳 4. XỬ LÝ TIẾNG VIỆT — CỰC KỲ QUAN TRỌNG

Đây là điểm dễ sai nhất. Tuân thủ nghiêm ngặt:

### 4.1. Quy tắc vàng

| Loại nội dung | Dùng class | Lý do |
|---|---|---|
| Phụ đề tiếng Việt có dấu | **`Text(...)`** với `font=SUBTITLE_FONT` | Render Unicode trực tiếp, không qua LaTeX |
| Tiêu đề tiếng Việt | **`Text(...)`** với `font=TITLE_FONT` | Như trên |
| Công thức toán | `MathTex(...)` | LaTeX math mode an toàn |
| Thuật ngữ tiếng Anh ngắn | `Text(...)` với `font=MONO_FONT` | Đơn giản, không cần LaTeX |
| Đoạn LaTeX có cả Việt + math | **TRÁNH** — tách ra hai mob riêng | LaTeX tiếng Việt rất dễ vỡ |

### 4.2. KHÔNG dùng `Tex()` với chuỗi tiếng Việt

❌ **SAI:**
```python
Tex("Khuôn mặt người", tex_template=vn_template)
```

✅ **ĐÚNG:**
```python
Text("Khuôn mặt người", font=SUBTITLE_FONT, color=TEXT_PRIMARY)
```

### 4.3. Helper function bắt buộc đưa vào đầu mỗi file

```python
def make_subtitle(text_str, scale=0.55, color=None):
    """Phụ đề chuẩn ở mép dưới khung hình."""
    color = color or TEXT_PRIMARY
    sub = Text(text_str, font=SUBTITLE_FONT, color=color, weight=LIGHT)
    sub.scale(scale).to_edge(DOWN, buff=0.5)
    return sub

def section_title(text_str, color=None):
    """Tiêu đề scene/section."""
    color = color or ACCENT_CYAN
    return Text(text_str, font=TITLE_FONT, color=color, weight=MEDIUM).scale(0.9)
```

### 4.4. Quản lý phụ đề theo timing

Theo bảng "Phụ đề" của mỗi scene trong overview.md, dùng pattern:

```python
# Phụ đề scene
subs = [
    ("Máy tính nhận diện khuôn mặt như thế nào?", 0, 4),
    ("Bài toán có hai nhánh chính", 4, 8),
    # ...
]

current_sub = None
for text_str, t_start, t_end in subs:
    new_sub = make_subtitle(text_str)
    if current_sub is None:
        self.play(FadeIn(new_sub, shift=UP*0.2), run_time=0.3)
    else:
        self.play(Transform(current_sub, new_sub), run_time=0.3)
    current_sub = new_sub
    self.wait(t_end - t_start - 0.3)
self.play(FadeOut(current_sub))
```

> **Lưu ý:** Phụ đề chạy SONG SONG với animation chính. Nếu animation chính tốn thời gian, có thể dùng `AnimationGroup` hoặc tách `self.add(subtitle)` rồi animate visual riêng.

---

## 📐 5. CODE STRUCTURE — MỖI SCENE LÀ 1 FILE

### 5.1. File naming

```
scene_01_title_opening.py
scene_02_face_recognition.py
scene_03_core_problem.py
scene_04_previous_approaches.py
scene_05_transition.py
scene_06_ebgm_novel.py
scene_07_ending_teaser.py
```

### 5.2. Template chuẩn cho mỗi file

```python
"""
EBGM Video — Overview Section
Scene <N>: <Tên Scene>
Thời lượng dự kiến: <X>s

⚠️ CÀI FONT TRƯỚC KHI RENDER:
  - Be Vietnam Pro / EB Garamond / JetBrains Mono (Google Fonts)

Render command:
  manim -pql scene_<N>_<name>.py Scene<N>_<ClassName>
  manim -pqh scene_<N>_<name>.py Scene<N>_<ClassName>  # high quality
"""

from manim import *
import numpy as np

# ============================================================
# COLOR PALETTE
# ============================================================
BG_NAVY         = "#0D1B2A"
BG_NAVY_SOFT    = "#1B263B"
TEXT_PRIMARY    = "#E0E1DD"
TEXT_MUTED      = "#A9B4C2"
ACCENT_CYAN     = "#48CAE4"
ACCENT_TEAL     = "#76C5BF"
ACCENT_BLUE     = "#778DA9"
ACCENT_MINT     = "#95D5B2"
ACCENT_LAVENDER = "#B8B5FF"
ACCENT_CORAL    = "#E29578"

# ============================================================
# FONTS
# ============================================================
SUBTITLE_FONT = "Be Vietnam Pro"
TITLE_FONT    = "EB Garamond"
MONO_FONT     = "JetBrains Mono"

# ============================================================
# HELPERS
# ============================================================
def make_subtitle(text_str, scale=0.55, color=None):
    color = color or TEXT_PRIMARY
    return Text(text_str, font=SUBTITLE_FONT, color=color,
                weight=LIGHT).scale(scale).to_edge(DOWN, buff=0.5)

def section_title(text_str, color=None):
    color = color or ACCENT_CYAN
    return Text(text_str, font=TITLE_FONT, color=color,
                weight=MEDIUM).scale(0.9)

# ============================================================
# MAIN SCENE
# ============================================================
class Scene<N>_<ClassName>(Scene):
    def construct(self):
        self.camera.background_color = BG_NAVY
        
        # === Phase A: <mô tả> ===
        # ...
        
        # === Phase B: <mô tả> ===
        # ...
        
        # Cleanup
        self.play(FadeOut(*self.mobjects))
        self.wait(0.3)
```

### 5.3. Tổ chức animation trong `construct()`

- Chia thành các **"Phase"** đúng theo storyboard trong overview.md, mỗi phase là 1 block code có comment `# === Phase A/B/C: ... ===`.
- Mỗi phase tự cleanup các mobjects không còn dùng (`FadeOut`) trước khi sang phase mới, **trừ khi** mobject cần persist.
- Cuối scene luôn `FadeOut(*self.mobjects)` + `self.wait(0.3)`.

---

## ⚠️ 6. CÁC LỖI THƯỜNG GẶP — TRÁNH BẰNG MỌI GIÁ

### 6.1. Lỗi font không tìm thấy
- Khi dùng `Text(..., font="...")`, nếu font không cài trên máy thì Manim sẽ fallback về font mặc định và **không báo lỗi rõ ràng**. Luôn comment nhắc user cài.

### 6.2. Lỗi LaTeX với tiếng Việt
- **TUYỆT ĐỐI KHÔNG** dùng `Tex()` hay `MathTex()` để chứa chuỗi tiếng Việt có dấu.
- Nếu cần label tiếng Việt cho công thức, tách ra: `MathTex` cho phần toán + `Text` cho phần Việt, dùng `VGroup(...).arrange(RIGHT)`.

### 6.3. Lỗi asset không tồn tại
- Khi dùng `ImageMobject("path.png")` hoặc `SVGMobject("path.svg")`, **bọc trong try/except** và fallback về placeholder:

```python
try:
    face_img = ImageMobject("assets/face_sample.png").scale(1.5)
except (FileNotFoundError, OSError):
    # Fallback: vẽ silhouette đơn giản
    face_img = VGroup(
        Ellipse(width=2, height=2.6, color=ACCENT_BLUE,
                stroke_width=2, fill_opacity=0.1),
        Dot(point=[-0.4, 0.3, 0], radius=0.08, color=ACCENT_BLUE),  # mắt trái
        Dot(point=[ 0.4, 0.3, 0], radius=0.08, color=ACCENT_BLUE),  # mắt phải
        Line([-0.05, 0, 0], [0.05, -0.15, 0], color=ACCENT_BLUE),   # mũi
        Arc(radius=0.3, angle=-PI, color=ACCENT_BLUE,
            stroke_width=2).shift(DOWN*0.5),                         # miệng
    )
```

**Đầu mỗi file**, comment rõ asset cần thiết:

```python
# ASSETS CẦN THIẾT (đặt trong ./assets/):
#   - face_sample.png  (Scene 1, 2, 3 — ảnh khuôn mặt mẫu)
#   - face_pose_*.png  (Scene 3 — 5 ảnh cùng người ở pose khác nhau)
# Nếu thiếu, code sẽ fallback về vector silhouette.
```

### 6.4. Lỗi overlap mobjects
- Khi cùng dùng `to_edge(DOWN)` cho nhiều object, chúng sẽ đè lên nhau. Dùng `next_to(previous, UP)` thay vì.

### 6.5. Lỗi `Transform` với mobject khác kiểu
- `Transform(text, math)` có thể méo. Dùng `ReplacementTransform` hoặc `FadeOut` + `FadeIn` cho an toàn.

### 6.6. Lỗi `run_time=0`
- Mọi `self.play(...)` phải có `run_time > 0`. Nếu chỉ muốn "đặt" mob, dùng `self.add(...)`.

### 6.7. Lỗi font weight
- Manim CE chấp nhận: `NORMAL`, `BOLD`, `LIGHT`, `MEDIUM`, `SEMIBOLD`, `THIN`. Phải dùng constant này, KHÔNG dùng string `"light"`.

---

## 🎨 7. STYLE & QUALITY GUIDELINES

### 7.1. Pacing
- Sau mỗi animation chính, **`self.wait(0.5–1.0)`** cho khán giả "thở".
- Không gọi `self.play(...)` liên tiếp 5+ lần không có wait.

### 7.2. `run_time` chuẩn
- `Write` text: 1.0–1.5s
- `Create` shape: 0.8–1.2s
- `FadeIn` / `FadeOut`: 0.5–0.8s
- `Transform` lớn: 1.5–2.0s

### 7.3. LaggedStart cho nhóm
Khi animate nhiều object cùng loại, dùng:
```python
self.play(LaggedStart(*[FadeIn(o, shift=UP*0.3) for o in items],
                      lag_ratio=0.15, run_time=2))
```

### 7.4. Mỗi frame tối đa
- 1 câu phụ đề
- 3–5 mobjects chính
- Nếu cần nhiều hơn, chia beat nhỏ.

### 7.5. Signature color
- Mỗi lần nhắc đến **EBGM**, **Bunch Graph**, **Image Graph** → tô màu `ACCENT_LAVENDER`.
- Mỗi lần nhắc đến **Jet** hay **Gabor wavelet** → tô màu `ACCENT_CYAN`.
- "✓ ưu điểm" → `ACCENT_MINT`. "✗ hạn chế" → `ACCENT_CORAL`.

---

## 🔁 8. CHIẾN LƯỢC SINH CODE — QUAN TRỌNG

**KHÔNG sinh tất cả scene trong 1 lần.** Lý do: dễ thiếu chi tiết, dễ vượt context window, khó debug.

### Quy trình đúng:

**Lần 1 (turn này):** Sinh **Scene 1** hoàn chỉnh, kèm:
- File `_common.py` chứa colors + fonts + helpers (để các scene khác import).
- Comment đầy đủ
- Asset fallback
- Lệnh render cụ thể

**Các turn tiếp:** User sẽ yêu cầu "tiếp Scene 2", "tiếp Scene 3"... — bạn sinh từng cái.

**Mỗi scene, kết thúc bằng:**
1. Lệnh render: `manim -pql scene_XX_name.py SceneXX_ClassName`
2. Checklist asset cần có
3. Note về điểm cần verify (font đã cài? asset có chưa?)
4. Câu hỏi: *"Bạn muốn tôi sinh Scene <N+1> không?"*

---

## ✅ 9. SELF-VALIDATION CHECKLIST (Gemini tự check trước khi trả lời)

Trước khi gửi code, tự xác nhận:

- [ ] Code import đúng `from manim import *` (không `manimlib`)
- [ ] Mọi chuỗi tiếng Việt dùng `Text()`, KHÔNG dùng `Tex()`/`MathTex()`
- [ ] Đã set `self.camera.background_color = BG_NAVY` ở đầu
- [ ] Mọi `ImageMobject`/`SVGMobject` có try/except fallback
- [ ] Mọi mobject có ít nhất 1 `self.play()` hoặc `self.add()`
- [ ] Cuối scene có `FadeOut(*self.mobjects)`
- [ ] Comment đầu file liệt kê: font cần cài + asset cần có + lệnh render
- [ ] Tổng thời lượng (cộng `run_time` + `wait`) khớp với mục tiêu trong overview.md (±10%)
- [ ] Phụ đề khớp với bảng timing trong overview.md
- [ ] Color palette dùng đúng constants ở mục 3.3, KHÔNG hard-code hex
- [ ] Không có syntax error (mental run-through)

---

## 📤 10. OUTPUT FORMAT

Trả lời theo format:

````
## Scene <N>: <Tên>

**Mục tiêu:** <1 câu>
**Thời lượng dự kiến:** <X>s
**Assets cần thiết:** <liệt kê hoặc "không">

### Code

```python
<code đầy đủ>
```

### Render

```bash
manim -pql scene_<N>_<name>.py Scene<N>_<ClassName>
```

### Notes
- <điểm cần verify 1>
- <điểm cần verify 2>

---

Bạn muốn tôi sinh **Scene <N+1>: <tên scene tiếp theo>** không?
````

---

## 🎬 11. YÊU CẦU CỤ THỂ CHO TURN ĐẦU TIÊN

Trong turn này, hãy:

1. **Đọc kỹ `overview.md`** đính kèm.
2. **Sinh file `_common.py`** trước (chứa color, font, helper) — chỉ ~50 dòng.
3. **Sinh `scene_01_title_opening.py`** đầy đủ, theo storyboard Scene 1 trong overview.md:
   - Phase 1 (0–3s): Dots → graph trừu tượng
   - Phase 2 (3–6s): Graph morph thành lưới phủ silhouette mờ
   - Phase 3 (6–12s): Title "ELASTIC BUNCH GRAPH MATCHING" + citation
4. **Đừng quên fallback** cho `SVGMobject("face_silhouette.svg")`.
5. **Kết thúc bằng** câu hỏi có muốn tiếp Scene 2 không.

---

## 🚫 12. KHÔNG ĐƯỢC LÀM

- ❌ Sinh code Manim phiên bản cũ (ShowCreation thay vì Create, etc.)
- ❌ Dùng `Tex()` cho chuỗi tiếng Việt
- ❌ Hard-code màu hex (vd `"#48CAE4"` rời rạc) — luôn dùng constant
- ❌ Bỏ qua phụ đề trong các scene có bảng timing
- ❌ Tự ý thêm scene hoặc thay đổi storyboard
- ❌ Sinh tất cả 7 scene trong 1 turn
- ❌ Dùng emoji trong text rendered bởi Manim (font Be Vietnam Pro không có emoji glyph — sẽ ra ô vuông). Emoji chỉ dùng trong comment Python.
- ❌ Sinh code thiếu try/except cho asset

---

## 📚 13. REFERENCE — MANIM CE API CHEAT SHEET

Để tránh hallucinate API, dưới đây là các API CE chuẩn:

**Mobjects:**
- `Text(str, font=..., color=..., weight=NORMAL, slant=NORMAL)`
- `MathTex(r"...")` — math only
- `Tex(r"...")` — text mode LaTeX (English only ở đây)
- `Dot(point, radius, color)`
- `Line(start, end, color, stroke_width)`
- `Arrow(start, end, buff, color)`
- `Circle(radius, color)`, `Ellipse(width, height, color)`
- `Rectangle(width, height, color, fill_opacity)`
- `Arc(radius, start_angle, angle, color)`
- `ParametricFunction(func, t_range, color)`
- `VGroup(*mobs)` — group, có `.arrange(direction, buff)`
- `ImageMobject(path)`, `SVGMobject(path)`

**Animations:**
- `Create(mob)`, `Write(mob)`, `FadeIn(mob, shift=UP)`, `FadeOut(mob)`
- `Transform(a, b)`, `ReplacementTransform(a, b)`
- `Indicate(mob, color)`, `Flash(point, color)`, `Wiggle(mob)`
- `LaggedStart(*anims, lag_ratio=0.2)`
- `AnimationGroup(*anims, lag_ratio=0)` — chạy song song
- `Succession(*anims)` — chạy tuần tự

**Positioning:**
- `mob.to_edge(DOWN/UP/LEFT/RIGHT, buff=0.5)`
- `mob.to_corner(UL/UR/DL/DR)`
- `mob.next_to(other, direction, buff=0.3)`
- `mob.shift(UP*2)`, `mob.move_to([x,y,0])`
- `mob.scale(1.5)`, `mob.rotate(PI/4)`

**Camera:**
- `self.camera.background_color = BG_NAVY`
- `self.play(self.camera.frame.animate.shift(UP))` — chỉ MovingCameraScene

---

## 🏁 14. BẮT ĐẦU

Sau khi đọc xong prompt này và `overview.md` đính kèm, hãy:

1. Confirm ngắn gọn (1 câu) rằng bạn đã hiểu task.
2. Sinh `_common.py`.
3. Sinh `scene_01_title_opening.py` theo template ở mục 5.2 và storyboard Scene 1.
4. Hỏi user có muốn tiếp Scene 2 không.

**Bắt đầu nào.**
