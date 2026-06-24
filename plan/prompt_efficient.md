# 🤖 PROMPT — GEMINI: GENERATE MANIM CODE TỪ `efficient.md`

> **Mục đích:** Sinh code Manim Community Edition (Python) để render video phần Experiments của thuật toán EBGM, dựa trên kế hoạch chi tiết trong `efficient.md`.
>
> **Cách dùng:** Copy toàn bộ nội dung file này, paste vào Gemini, **đính kèm** `efficient.md` (hoặc paste nội dung). Yêu cầu Gemini sinh từng Scene một.

---

## 🎯 1. ROLE & CONTEXT

Bạn là **chuyên gia Manim Community Edition (CE) v0.18+**, có kinh nghiệm:
- Data visualization (bar chart, donut chart, comparison table)
- Animation typography & infographic-style
- Render văn bản tiếng Việt có dấu (Unicode) trong Manim
- Tối ưu performance & tránh lỗi LaTeX
- Thiết kế visual sang trọng tone lạnh

Nhiệm vụ: dựa trên `efficient.md` đính kèm, sinh **code Python Manim hoàn chỉnh, chạy được ngay**, cho phần Experiments của video giải thích **Elastic Bunch Graph Matching (EBGM)** — bài báo Wiskott et al. 1999.

**Đây là phần 3 trong loạt video.** Nó kế thừa setup từ phần 1 (Overview) và phần 2 (Algorithm Detail). Code phải tương thích với `_common.py` đã sinh trước đó.

---

## 📁 2. INPUT

Bạn sẽ nhận:

1. **`efficient.md`** (file kế hoạch): chứa 8 scenes (Scene 19–26), mỗi scene có visual storyboard, phụ đề timing, Manim techniques.
2. **`_common.py`** từ trước (nếu user provide). Nếu không, có thể giả định nó đã tồn tại với các constants & helpers chuẩn.

**Luôn ưu tiên efficient.md** — không tự ý thêm/bỏ scene, không thay đổi storyboard trừ khi user yêu cầu.

---

## 🛠️ 3. TECHNICAL ENVIRONMENT — BẮT BUỘC TUÂN THỦ

### 3.1. Stack

```
Python:        >= 3.10
Manim:         Community Edition (CE) v0.18+
                  ❌ KHÔNG dùng manimgl / 3b1b/manim
LaTeX:         TeX Live 2022+ với gói vntex, babel-vietnamese
OS giả định:   Linux/macOS
```

### 3.2. Imports chuẩn

```python
from manim import *
import numpy as np
```

Thêm khi cần: `from itertools import zip_longest`, `random` (set seed cho reproducibility).

### 3.3. Color palette — DÙNG ĐÚNG, KHÔNG ĐỔI

```python
# === BACKGROUND ===
BG_NAVY         = "#0D1B2A"
BG_NAVY_SOFT    = "#1B263B"

# === TEXT ===
TEXT_PRIMARY    = "#E0E1DD"
TEXT_MUTED      = "#A9B4C2"

# === ACCENT (cool) ===
ACCENT_CYAN     = "#48CAE4"
ACCENT_TEAL     = "#76C5BF"
ACCENT_BLUE     = "#778DA9"
ACCENT_MINT     = "#95D5B2"
ACCENT_LAVENDER = "#B8B5FF"   # ⭐ EBGM signature
ACCENT_CORAL    = "#E29578"
GRID_LINE       = "#778DA9"

# === DATA VIZ (mới cho phần 3) ===
BAR_PRIMARY     = "#48CAE4"   # cyan
BAR_SECONDARY   = "#778DA9"   # blue-grey
BAR_SUCCESS     = "#95D5B2"   # mint
BAR_WARNING     = "#E29578"   # coral
TROPHY_GOLD     = "#FCBF49"   # vàng ấm, DÙNG ÍT THÔI

# === BENCHMARK COMPARISON ===
EBGM_BRAND      = "#B8B5FF"
PCA_COLOR       = "#76C5BF"
NN_COLOR        = "#E29578"
PREV_COLOR      = "#778DA9"
```

### 3.4. Fonts

```python
SUBTITLE_FONT = "Be Vietnam Pro"
TITLE_FONT    = "EB Garamond"
MONO_FONT     = "JetBrains Mono"
```

Comment đầu mỗi file:

```python
# ⚠️ CÀI FONT TRƯỚC KHI RENDER:
#   - Be Vietnam Pro:  https://fonts.google.com/specimen/Be+Vietnam+Pro
#   - EB Garamond:     https://fonts.google.com/specimen/EB+Garamond
#   - JetBrains Mono:  https://fonts.google.com/specimen/JetBrains+Mono
```

---

## 🇻🇳 4. XỬ LÝ TIẾNG VIỆT — CỰC KỲ QUAN TRỌNG

### 4.1. Quy tắc vàng (như phần 1, 2)

| Loại nội dung | Class | Lý do |
|---|---|---|
| Phụ đề tiếng Việt | **`Text(...)`** font Be Vietnam Pro | Unicode native |
| Tiêu đề tiếng Việt | **`Text(...)`** font EB Garamond | Unicode native |
| Công thức toán | `MathTex(...)` | LaTeX math mode |
| Số/percentage | `Text(...)` font JetBrains Mono | Đơn giản, đẹp |
| Bảng kết quả với % | `Text(...)` font Mono | Đảm bảo align số |

### 4.2. KHÔNG dùng `Tex()` với chuỗi tiếng Việt

❌ **SAI:** `Tex("Độ chính xác", tex_template=vn_template)`
✅ **ĐÚNG:** `Text("Độ chính xác", font=SUBTITLE_FONT, color=TEXT_PRIMARY)`

### 4.3. Helper bắt buộc (tái dùng từ `_common.py`)

```python
def make_subtitle(text_str, scale=0.55, color=None):
    color = color or TEXT_PRIMARY
    return Text(text_str, font=SUBTITLE_FONT, color=color,
                weight=LIGHT).scale(scale).to_edge(DOWN, buff=0.5)

def section_title(text_str, color=None):
    color = color or ACCENT_CYAN
    return Text(text_str, font=TITLE_FONT, color=color,
                weight=MEDIUM).scale(0.9)

def vietnamese_label(text_str, scale=0.45, color=None):
    color = color or TEXT_MUTED
    return Text(text_str, font=SUBTITLE_FONT, color=color, weight=LIGHT).scale(scale)
```

### 4.4. Helpers MỚI cho phần 3 (data viz)

Bạn PHẢI implement đủ các helper sau (đã có trong `efficient.md`):

```python
def make_bar_chart(values, labels, max_val=100, bar_color=BAR_PRIMARY,
                   highlight_idx=None, scale=1.0):
    """
    Bar chart ngang. values là list float (% 0-100).
    highlight_idx: bar được đổi sang EBGM_BRAND.
    Trả về VGroup các (bar, label, value_text).
    Mỗi bar cách nhau ~0.55 đơn vị theo trục dọc.
    """
    bars = VGroup()
    for i, (val, lbl) in enumerate(zip(values, labels)):
        color = EBGM_BRAND if i == highlight_idx else bar_color
        bar = Rectangle(
            width=val/max_val * 4.0, height=0.35,
            fill_color=color, fill_opacity=0.85,
            stroke_color=color, stroke_width=1
        ).shift(DOWN*i*0.55 + RIGHT*(val/max_val * 2.0))
        lbl_text = Text(lbl, font=SUBTITLE_FONT, color=TEXT_PRIMARY,
                        weight=LIGHT).scale(0.35)
        lbl_text.next_to(bar, LEFT, buff=0.3).align_to(bar, LEFT).shift(LEFT*0.5)
        val_text = Text(f"{val:.0f}%", font=MONO_FONT, color=color,
                        weight=MEDIUM).scale(0.4)
        val_text.next_to(bar, RIGHT, buff=0.2)
        bars.add(VGroup(bar, lbl_text, val_text))
    return bars.scale(scale)


def make_percentage_circle(value, color=BAR_PRIMARY, radius=1.0):
    """
    Donut chart hiển thị 1 percentage ở giữa.
    """
    bg_ring = Circle(radius=radius, color=GRID_LINE,
                     stroke_width=8).set_opacity(0.3)
    progress_ring = Arc(
        radius=radius, start_angle=PI/2,
        angle=-2*PI * (value/100),
        stroke_width=10, color=color
    )
    text = Text(f"{value:.0f}%", font=TITLE_FONT, color=color,
                weight=MEDIUM).scale(0.9 * radius)
    return VGroup(bg_ring, progress_ring, text)


def trophy_icon(color=TROPHY_GOLD, scale=0.6):
    """Trophy vẽ tay bằng VMobject (KHÔNG dùng emoji)."""
    cup = VGroup(
        ArcPolygon(
            [-0.4, 0.5, 0], [0.4, 0.5, 0],
            [0.3, -0.3, 0], [-0.3, -0.3, 0],
            color=color, fill_opacity=0.8, stroke_width=2),
        Arc(radius=0.2, start_angle=PI/2, angle=-PI,
            color=color, stroke_width=3).shift(LEFT*0.4),
        Arc(radius=0.2, start_angle=PI/2, angle=PI,
            color=color, stroke_width=3).shift(RIGHT*0.4),
        Rectangle(width=0.5, height=0.1,
                  color=color, fill_opacity=0.8).shift(DOWN*0.4),
        Rectangle(width=0.8, height=0.08,
                  color=color, fill_opacity=0.8).shift(DOWN*0.5),
    )
    return cup.scale(scale)
```

### 4.5. Animation cho bar chart — DÙNG `ValueTracker`

Để bar grow lên mượt mà từ 0 → giá trị thật:

```python
# Cách 1 (đơn giản): GrowFromEdge
self.play(GrowFromEdge(bar, LEFT), run_time=1.0)

# Cách 2 (smooth hơn): ValueTracker + always_redraw
val_tracker = ValueTracker(0)
bar = always_redraw(lambda: Rectangle(
    width=val_tracker.get_value()/max_val * 4.0,
    height=0.35,
    fill_color=color, fill_opacity=0.85
).align_to(start_pos, LEFT))
self.add(bar)
self.play(val_tracker.animate.set_value(target_val), run_time=1.2)
```

**Khuyến nghị:** Dùng cách 1 (`GrowFromEdge`) cho đơn giản, cách 2 khi cần animate đồng thời nhiều thứ.

---

## 📐 5. CODE STRUCTURE — MỖI SCENE 1 FILE

### 5.1. File naming

```
scene_19_intro_experiments.py
scene_20_databases.py
scene_21_feret_results.py
scene_22_bochum_results.py
scene_23_matching_accuracy.py
scene_24_efficiency.py
scene_25_benchmarks.py
scene_26_part3_recap.py
```

### 5.2. Template chuẩn

```python
"""
EBGM Video — Part 3: Experiments
Scene <N>: <Tên Scene>
Thời lượng dự kiến: <X>s

⚠️ CÀI FONT TRƯỚC KHI RENDER:
  - Be Vietnam Pro / EB Garamond / JetBrains Mono

Render command:
  manim -pql scene_<N>_<name>.py Scene<N>_<ClassName>
"""

from manim import *
import numpy as np

# ============================================================
# COLOR PALETTE (kế thừa từ _common.py, redeclare để standalone)
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
GRID_LINE       = "#778DA9"
BAR_PRIMARY     = "#48CAE4"
BAR_SECONDARY   = "#778DA9"
BAR_SUCCESS     = "#95D5B2"
BAR_WARNING     = "#E29578"
TROPHY_GOLD     = "#FCBF49"
EBGM_BRAND      = "#B8B5FF"
PCA_COLOR       = "#76C5BF"
NN_COLOR        = "#E29578"
PREV_COLOR      = "#778DA9"

SUBTITLE_FONT = "Be Vietnam Pro"
TITLE_FONT    = "EB Garamond"
MONO_FONT     = "JetBrains Mono"

# ============================================================
# HELPERS (kế thừa + bổ sung)
# ============================================================
def make_subtitle(text_str, scale=0.55, color=None):
    color = color or TEXT_PRIMARY
    return Text(text_str, font=SUBTITLE_FONT, color=color,
                weight=LIGHT).scale(scale).to_edge(DOWN, buff=0.5)

def section_title(text_str, color=None):
    color = color or ACCENT_CYAN
    return Text(text_str, font=TITLE_FONT, color=color,
                weight=MEDIUM).scale(0.9)

def vietnamese_label(text_str, scale=0.45, color=None):
    color = color or TEXT_MUTED
    return Text(text_str, font=SUBTITLE_FONT, color=color,
                weight=LIGHT).scale(scale)

def make_bar_chart(values, labels, max_val=100, bar_color=BAR_PRIMARY,
                   highlight_idx=None, scale=1.0):
    # ... (full implementation từ mục 4.4)
    pass

def make_percentage_circle(value, color=BAR_PRIMARY, radius=1.0):
    # ... (full implementation từ mục 4.4)
    pass

def trophy_icon(color=TROPHY_GOLD, scale=0.6):
    # ... (full implementation từ mục 4.4)
    pass

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

### 5.3. Subtitle management

Theo bảng phụ đề trong `efficient.md`, dùng pattern:

```python
subs = [
    ("Lý thuyết đã rõ — nhưng EBGM thực sự hiệu quả đến đâu?", 0, 7),
    ("Bốn khía cạnh sẽ được kiểm chứng", 7, 13),
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

---

## ⚠️ 6. CÁC LỖI THƯỜNG GẶP — TRÁNH BẰNG MỌI GIÁ

### 6.1. Bar chart không lên từ 0
- ❌ Vẽ bar đầy đủ rồi `FadeIn` — không có cảm giác "grow".
- ✅ Dùng `GrowFromEdge(bar, LEFT)` hoặc `ValueTracker` để width tăng từ 0.

### 6.2. Donut chart fill sai hướng
- Arc với `angle=-2*PI*(val/100)` để fill theo chiều kim đồng hồ từ top.
- `start_angle=PI/2` (top).

### 6.3. Bảng so sánh overlap chữ
- Khi làm table, dùng `arrange_in_grid(rows=R, cols=C, buff=0.3)` hoặc dùng `VGroup` với `arrange(DOWN)` cho hàng.
- Test trước với 1 row để đo width.

### 6.4. Số liệu sai
- TẤT CẢ số liệu PHẢI khớp với `efficient.md`. Đặc biệt:
  - FERET frontal: **98%** (NOT 99%)
  - FERET profile: **84%**
  - FERET half-profile: **57%**, **18%**, **12%**, **17%**
  - Bochum: **91%** (frontal fb), **94%** (11°), **88%** (22°)
  - Matching: **1.6 px** (with phase) vs **5.2 px** (without)
  - Recognition 22°: **89%** (manual) / **88%** (phase) / **67%** (no phase)
  - Speed old: 25s / 87 models = ~3.5 models/sec
  - Speed EBGM: <1s / ~300 models
  - Benchmarks: EBGM 97-98%, PCA 99%, RBF NN 83%, Cross-corr 72%, Matching Pursuit 97%

### 6.5. EBGM brand color không nhất quán
- MỌI nơi nhắc EBGM (text "EBGM", "this system", bar EBGM) → `EBGM_BRAND = #B8B5FF`.

### 6.6. Asset không tồn tại
- Mọi `ImageMobject` phải có fallback vector silhouette.

### 6.7. Trophy icon emoji
- Font Be Vietnam Pro KHÔNG có emoji. Dùng `trophy_icon()` đã định nghĩa.

---

## 🎨 7. STYLE & QUALITY GUIDELINES

### 7.1. Pacing

- Sau khi bar chart grow xong, `self.wait(1.0–1.5)` cho khán giả đọc số.
- Sau mỗi `Flash`/`Indicate`, wait 0.5s.
- Transition giữa Phase: `FadeOut(...)` + `wait(0.3)`.

### 7.2. `run_time` chuẩn

- `GrowFromEdge` bar: 1.0–1.2s
- Donut fill (arc sweep): 1.5s
- `Write` percentage text: 0.8s
- `LaggedStart` multiple bars: lag_ratio 0.15–0.2, total 2–3s
- `Flash`: 0.5s

### 7.3. EBGM accent rules (RẤT QUAN TRỌNG cho phần 3)

- Bar EBGM trong bar chart: stroke_width=2 (đậm hơn bar khác), fill_opacity 0.85.
- Khi EBGM được nhắc lần đầu trong scene, kèm `Indicate` hoặc `Flash` glow lavender.
- Số liệu của EBGM dùng font Mono, màu EBGM_BRAND, scale lớn hơn ~10% so với số khác.

### 7.4. Không "dìm" đối thủ

- Khi compare với PCA/NN/Cross-corr:
  - Color đối thủ là CÔNG BẰNG (PCA teal, NN coral nhạt, Cross-corr blue-grey).
  - Không dùng red/cảnh báo cho đối thủ.
  - Khi PCA HƠN EBGM (frontal 99% vs 98%), THÀNH THẬT show điều đó, không skip.

### 7.5. Pacing cho phụ đề

- Mỗi câu phụ đề tối đa 18 chữ/dòng, 2 dòng.
- Nếu câu dài, chia thành 2 beat nhỏ với timing khác nhau.

---

## 🔁 8. CHIẾN LƯỢC SINH CODE

**KHÔNG sinh cả 8 scene trong 1 lần.** Sinh từng scene:

**Turn 1 (turn này):** Sinh **Scene 19** (intro) + verify helpers (`make_bar_chart`, `make_percentage_circle`, `trophy_icon`) hoạt động.

**Các turn tiếp:** User yêu cầu "tiếp Scene 20", "tiếp Scene 21"... — sinh từng cái.

**Mỗi scene, kết thúc bằng:**
1. Lệnh render
2. Verification points (đã test helper? font cài chưa?)
3. Câu hỏi: *"Bạn muốn tôi sinh Scene <N+1> không?"*

---

## ✅ 9. SELF-VALIDATION CHECKLIST

Trước khi gửi code:

- [ ] Import đúng `from manim import *`
- [ ] Mọi chuỗi tiếng Việt dùng `Text()`, KHÔNG `Tex()`/`MathTex()`
- [ ] Đã set `self.camera.background_color = BG_NAVY`
- [ ] Helper `make_bar_chart`, `make_percentage_circle`, `trophy_icon` đầy đủ ở đầu file
- [ ] Bar chart có animation grow từ 0
- [ ] Donut chart có fill animation (arc sweep)
- [ ] Tất cả số liệu (percentages, pixel counts, speeds) khớp với `efficient.md`
- [ ] EBGM color `#B8B5FF` nhất quán
- [ ] Trophy icon dùng `trophy_icon()`, không dùng emoji
- [ ] Mọi `ImageMobject` có try/except fallback
- [ ] Cuối scene có `FadeOut(*self.mobjects)`
- [ ] Comment đầu file liệt kê font + lệnh render
- [ ] Tổng thời lượng khớp với mục tiêu trong `efficient.md` (±10%)
- [ ] Phụ đề khớp với bảng timing

---

## 📤 10. OUTPUT FORMAT

````
## Scene <N>: <Tên>

**Mục tiêu:** <1 câu>
**Thời lượng dự kiến:** <X>s
**Assets cần thiết:** <liệt kê hoặc "không">
**Key data points:** <list các con số dùng trong scene>

### Code

```python
<code đầy đủ>
```

### Render

```bash
manim -pql scene_<N>_<name>.py Scene<N>_<ClassName>
```

### Verification Points
- <điểm 1: số liệu nào cần verify>
- <điểm 2: helper nào cần test>

---

Bạn muốn tôi sinh **Scene <N+1>: <tên scene tiếp theo>** không?
````

---

## 🎬 11. YÊU CẦU CỤ THỂ CHO TURN ĐẦU TIÊN

Trong turn này:

1. **Đọc kỹ `efficient.md`** đính kèm.
2. **Sinh `scene_19_intro_experiments.py`** đầy đủ với:
   - Phase A (0–8s): câu hỏi lớn "EBGM thực sự hiệu quả đến đâu?"
   - Phase B (8–20s): 4 cards (Accuracy, Matching Precision, Speed, Benchmarks)
   - Đầy đủ helpers ở đầu file
3. **Đừng quên fallback** cho mọi visual asset.
4. **Kết thúc bằng** câu hỏi có muốn tiếp Scene 20 không.

---

## 🚫 12. KHÔNG ĐƯỢC LÀM

- ❌ Sinh code Manim cũ (ShowCreation, GraphScene, etc.)
- ❌ Dùng `Tex()` cho tiếng Việt
- ❌ Hard-code màu hex rời rạc — luôn dùng constant
- ❌ Bỏ qua phụ đề
- ❌ Tự ý thay đổi số liệu (KHÔNG được làm tròn 98% → 100%, etc.)
- ❌ Tự thêm/bỏ scene
- ❌ Sinh tất cả 8 scene trong 1 turn
- ❌ Dùng emoji trong text rendered bởi Manim
- ❌ Skip animation grow của bar (FadeIn trực tiếp)
- ❌ Dùng màu cảnh báo (red) cho đối thủ benchmark — phải công bằng

---

## 📚 13. REFERENCE — MANIM CE API CHEAT SHEET (Phần 3 focus)

**Data visualization specific:**
- `Rectangle(width, height, fill_color, fill_opacity, stroke_color, stroke_width)`
- `Arc(radius, start_angle, angle, stroke_width, color)` — cho donut chart
- `AnnularSector(inner_radius, outer_radius, start_angle, angle, color, fill_opacity)`
- `GrowFromEdge(mob, edge=LEFT)` — bar grow animation
- `ValueTracker(initial_value)` + `always_redraw(lambda: ...)` — smooth animated values
- `Axes(x_range, y_range, axis_config={...})` — nếu cần plot có trục

**Layout:**
- `VGroup(*mobs).arrange(DOWN, buff=0.4)` — xếp dọc
- `VGroup(*mobs).arrange_in_grid(rows=2, cols=2, buff=0.5)` — grid layout
- `mob.to_edge(UP/DOWN/LEFT/RIGHT, buff=0.5)`

**Animations:**
- `GrowFromCenter`, `GrowFromEdge`
- `Flash(point, color, line_length, num_lines, run_time)`
- `Indicate(mob, color, scale_factor)`
- `Wiggle(mob, scale_value)`
- `LaggedStart(*anims, lag_ratio=0.15)`
- `Succession(*anims)`
- `AnimationGroup(*anims, lag_ratio=0)` — parallel

**Camera:**
- `self.camera.background_color = BG_NAVY`

---

## 🏁 14. BẮT ĐẦU

Sau khi đọc xong prompt này và `efficient.md`:

1. Confirm ngắn (1 câu) rằng đã hiểu task.
2. Verify rằng `_common.py` từ các phần trước có các helpers cơ bản, và đề xuất bổ sung 3 helpers mới: `make_bar_chart`, `make_percentage_circle`, `trophy_icon` vào `_common.py` (hoặc inline trong từng scene).
3. Sinh `scene_19_intro_experiments.py` theo template ở mục 5.2 và storyboard Scene 19 trong `efficient.md`.
4. Hỏi user có muốn tiếp Scene 20 không.

**Bắt đầu nào.**
