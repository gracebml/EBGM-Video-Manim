# 🤖 PROMPT — GEMINI: GENERATE MANIM CODE TỪ `discussion.md`

> **Mục đích:** Sinh code Manim Community Edition (Python) để render video phần Discussion của thuật toán EBGM, dựa trên kế hoạch chi tiết trong `discussion.md`.
>
> **Cách dùng:** Copy toàn bộ nội dung file này, paste vào Gemini, **đính kèm** `discussion.md` (hoặc paste nội dung). Yêu cầu Gemini sinh từng Scene một.

---

## 🎯 1. ROLE & CONTEXT

Bạn là **chuyên gia Manim Community Edition (CE) v0.18+**, có kinh nghiệm:
- Comparison layouts (side-by-side, vs-cards, pros/cons)
- Roadmap & timeline visualizations
- Animation typography & infographic-style
- Render văn bản tiếng Việt có dấu (Unicode) trong Manim
- Tối ưu performance & tránh lỗi LaTeX
- Thiết kế visual sang trọng tone lạnh

Nhiệm vụ: dựa trên `discussion.md` đính kèm, sinh **code Python Manim hoàn chỉnh, chạy được ngay**, cho phần Discussion (phần CUỐI) của video giải thích **Elastic Bunch Graph Matching (EBGM)** — bài báo Wiskott et al. 1999.

**Đây là phần 4 / phần cuối trong loạt video.** Nó kế thừa setup từ phần 1 (Overview), phần 2 (Algorithm Detail), phần 3 (Experiments). Code phải tương thích với `_common.py` đã sinh trước đó.

---

## 📁 2. INPUT

Bạn sẽ nhận:

1. **`discussion.md`** (file kế hoạch): chứa 9 scenes (Scene 27–35), mỗi scene có visual storyboard, phụ đề timing, Manim techniques.
2. **`_common.py`** từ trước (nếu user provide). Nếu không, giả định nó tồn tại với constants & helpers chuẩn — và redeclare trong từng file để standalone.

**Luôn ưu tiên discussion.md** — không tự ý thêm/bỏ scene, không thay đổi storyboard trừ khi user yêu cầu.

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

# === COMPARISON / BENCHMARK (kế thừa phần 3) ===
EBGM_BRAND      = "#B8B5FF"   # lavender
PCA_COLOR       = "#76C5BF"   # teal
NN_COLOR        = "#E29578"   # coral nhạt
PREV_COLOR      = "#778DA9"   # blue-grey (preceding system Lades)

# === ĐỐI THỦ MỚI (phần 4) ===
YUILLE_COLOR    = "#8896AB"   # xám lạnh (user-defined features)
LANITIS_COLOR   = "#5FA8D3"   # blue (Lanitis deformable)
WARP_COLOR      = "#A7C5EB"   # light blue (3D warping)

# === PROS / CONS / FUTURE ===
PRO_COLOR       = "#95D5B2"   # mint - điểm mạnh
CON_COLOR       = "#E29578"   # coral - điểm yếu
FUTURE_GLOW     = "#B8B5FF"   # lavender - hướng tương lai
TROPHY_GOLD     = "#FCBF49"   # vàng ấm, DÙNG ÍT
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

### 4.1. Quy tắc vàng (như các phần trước)

| Loại nội dung | Class | Lý do |
|---|---|---|
| Phụ đề tiếng Việt | **`Text(...)`** font Be Vietnam Pro | Unicode native |
| Tiêu đề tiếng Việt | **`Text(...)`** font EB Garamond | Unicode native |
| Công thức toán | `MathTex(...)` | LaTeX math mode |
| Thuật ngữ tiếng Anh / số | `Text(...)` font JetBrains Mono | Đơn giản |

### 4.2. KHÔNG dùng `Tex()` với chuỗi tiếng Việt

❌ **SAI:** `Tex("Mô hình lò xo", tex_template=vn_template)`
✅ **ĐÚNG:** `Text("Mô hình lò xo", font=SUBTITLE_FONT, color=TEXT_PRIMARY)`

### 4.3. Helpers cơ bản (tái dùng từ `_common.py`)

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
    return Text(text_str, font=SUBTITLE_FONT, color=color,
                weight=LIGHT).scale(scale)
```

### 4.4. Helpers MỚI cho phần 4 — PHẢI implement đầy đủ

Bạn PHẢI implement các helper sau (đã có trong `discussion.md`):

```python
def make_vs_card(title_left, title_right, color_left, color_right, scale=1.0):
    """
    Card so sánh 'X vs Y': 2 panel cạnh nhau với divider 'VS' ở giữa.
    Trả về VGroup(panel_l, panel_r, lbl_l, lbl_r, vs).
    Panel rỗng để caller tự thêm nội dung vào sau.
    """
    panel_l = RoundedRectangle(
        width=3.0, height=2.0, corner_radius=0.15,
        fill_color=BG_NAVY_SOFT, fill_opacity=0.6,
        stroke_color=color_left, stroke_width=2
    ).shift(LEFT*2.0)
    panel_r = RoundedRectangle(
        width=3.0, height=2.0, corner_radius=0.15,
        fill_color=BG_NAVY_SOFT, fill_opacity=0.6,
        stroke_color=color_right, stroke_width=2
    ).shift(RIGHT*2.0)
    lbl_l = Text(title_left, font=TITLE_FONT, color=color_left,
                 weight=MEDIUM).scale(0.4).move_to(panel_l.get_top()+DOWN*0.3)
    lbl_r = Text(title_right, font=TITLE_FONT, color=color_right,
                 weight=MEDIUM).scale(0.4).move_to(panel_r.get_top()+DOWN*0.3)
    vs = Text("VS", font=TITLE_FONT, color=TEXT_MUTED, weight=BOLD).scale(0.6)
    return VGroup(panel_l, panel_r, lbl_l, lbl_r, vs).scale(scale)


def pro_item(text_str, scale=0.4):
    """Dòng điểm mạnh với check icon mint (vẽ tay, KHÔNG emoji)."""
    check = VGroup(
        Line([-0.08,0,0], [-0.02,-0.06,0], color=PRO_COLOR, stroke_width=3),
        Line([-0.02,-0.06,0], [0.08,0.06,0], color=PRO_COLOR, stroke_width=3),
    )
    txt = Text(text_str, font=SUBTITLE_FONT, color=TEXT_PRIMARY,
               weight=LIGHT).scale(scale)
    return VGroup(check, txt).arrange(RIGHT, buff=0.2)


def con_item(text_str, scale=0.4):
    """Dòng điểm yếu với cross icon coral (vẽ tay, KHÔNG emoji)."""
    cross = VGroup(
        Line([-0.06,0.06,0], [0.06,-0.06,0], color=CON_COLOR, stroke_width=3),
        Line([-0.06,-0.06,0], [0.06,0.06,0], color=CON_COLOR, stroke_width=3),
    )
    txt = Text(text_str, font=SUBTITLE_FONT, color=TEXT_PRIMARY,
               weight=LIGHT).scale(scale)
    return VGroup(cross, txt).arrange(RIGHT, buff=0.2)


def future_node(text_str, icon_mob, color=FUTURE_GLOW, scale=1.0):
    """Node cho roadmap: icon + text trong rounded box."""
    box = RoundedRectangle(
        width=2.8, height=1.2, corner_radius=0.12,
        fill_color=BG_NAVY_SOFT, fill_opacity=0.7,
        stroke_color=color, stroke_width=1.5
    )
    txt = Text(text_str, font=SUBTITLE_FONT, color=TEXT_PRIMARY,
               weight=LIGHT).scale(0.32)
    icon_mob.scale(0.5).move_to(box.get_left()+RIGHT*0.5)
    txt.next_to(icon_mob, RIGHT, buff=0.25)
    return VGroup(box, icon_mob, txt).scale(scale)
```

### 4.5. Helpers từ các phần trước (nếu scene cần)

Một số scene phần 4 dùng lại bar chart, percentage circle, jet visual từ phần 2-3. Nếu scene cần, redeclare:
- `make_bar_chart(...)` (Scene 30, 32 — comparison bars)
- `make_percentage_circle(...)` (Scene 32)
- `make_jet_visual(...)` (Scene 31 — Gabor jet vs profile)
- `trophy_icon(...)` (nếu cần)

Nếu user đã có `_common.py` với các helper này, import; nếu không, paste inline.

---

## 📐 5. CODE STRUCTURE — MỖI SCENE 1 FILE

### 5.1. File naming

```
scene_27_intro_generality.py
scene_28_vs_preceding.py
scene_29_vs_userdefined.py
scene_30_vs_pca.py
scene_31_vs_lanitis.py
scene_32_rotation_depth.py
scene_33_future_roadmap.py
scene_34_speed_optimization.py
scene_35_finale.py
```

### 5.2. Template chuẩn

```python
"""
EBGM Video — Part 4: Discussion (FINAL PART)
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
# COLOR PALETTE (redeclare để standalone)
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
EBGM_BRAND      = "#B8B5FF"
PCA_COLOR       = "#76C5BF"
NN_COLOR        = "#E29578"
PREV_COLOR      = "#778DA9"
YUILLE_COLOR    = "#8896AB"
LANITIS_COLOR   = "#5FA8D3"
WARP_COLOR      = "#A7C5EB"
PRO_COLOR       = "#95D5B2"
CON_COLOR       = "#E29578"
FUTURE_GLOW     = "#B8B5FF"
TROPHY_GOLD     = "#FCBF49"

SUBTITLE_FONT = "Be Vietnam Pro"
TITLE_FONT    = "EB Garamond"
MONO_FONT     = "JetBrains Mono"

# ============================================================
# HELPERS (basic + phần 4)
# ============================================================
# ... make_subtitle, section_title, vietnamese_label
# ... make_vs_card, pro_item, con_item, future_node
# ... (+ bất kỳ helper nào scene này cần)

# ============================================================
# MAIN SCENE
# ============================================================
class Scene<N>_<ClassName>(Scene):
    def construct(self):
        self.camera.background_color = BG_NAVY

        # === Phase A: <mô tả> ===
        # ...

        # Cleanup
        self.play(FadeOut(*self.mobjects))
        self.wait(0.3)
```

### 5.3. Subtitle management

Theo bảng phụ đề trong `discussion.md`:

```python
subs = [
    ("EBGM đã hiệu quả — nhưng nó đứng ở đâu giữa các hệ thống khác?", 0, 6),
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

### 6.1. vs-card overlap nội dung
- `make_vs_card` trả về 2 panel rỗng. Khi thêm nội dung (pro_item, con_item, demo), dùng `.move_to(panel.get_center())` rồi `.shift()` để fit trong panel.
- Test với 1 panel trước, đảm bảo nội dung không tràn ra ngoài.

### 6.2. pro_item / con_item icon emoji
- Font Be Vietnam Pro KHÔNG có emoji. Check & cross icon PHẢI vẽ bằng `Line` (đã có trong helper). KHÔNG dùng "✓" "✗" ký tự Unicode trong `Text` (có thể ra ô vuông tùy font).

### 6.3. Số liệu sai
- TẤT CẢ số liệu PHẢI khớp `discussion.md`:
  - Matching: **5.2px → 1.6px**
  - Maurer transform: Bochum 22° **88% → 96%**; FERET 45° **36% → 50%**
  - Kruger learning weights: **25% → 31%** (+6%)
  - EBGM FERET 45° (no transform): **18%**
  - PCA frontal: **99%** vs EBGM **98%**
  - Warping / Linear object classes: **100%** (perfect rendered DB)
  - Speed: ~**30s/graph** extraction
  - Yuille: **9 model parameters**

### 6.4. EBGM brand color không nhất quán
- MỌI nơi nhắc EBGM → `EBGM_BRAND = #B8B5FF`.

### 6.5. Màu cảnh báo cho đối thủ
- KHÔNG dùng red gắt cho đối thủ. Mỗi đối thủ có màu lạnh riêng (PCA teal, Yuille xám, Lanitis blue, Warp light-blue). Comparison phải CÔNG BẰNG.

### 6.6. Honest notes bị bỏ
- Phần Discussion của paper RẤT trung thực. Các "honest note" trong `discussion.md` (PCA 99% > EBGM 98%, EBGM yếu ở góc xoay lớn 18%) PHẢI được giữ — đây là điểm làm video uy tín. KHÔNG bỏ qua hay làm đẹp số liệu.

### 6.7. Asset không tồn tại
- Mọi `ImageMobject` phải có try/except fallback về vector silhouette.

### 6.8. Roadmap path lỗi
- Scene 33: con đường nên dùng `VMobject` với `set_points_smoothly([...])` hoặc `CubicBezier`. Test path trước khi add milestone nodes lên.

---

## 🎨 7. STYLE & QUALITY GUIDELINES

### 7.1. Pacing

- Sau mỗi vs-card xuất hiện đầy đủ, `self.wait(1.0)`.
- Sau mỗi mini-demo so sánh, `self.wait(0.8)`.
- Transition giữa Phase: `FadeOut(...)` + `wait(0.3)`.

### 7.2. `run_time` chuẩn

- vs-card appear: 1.0s (2 panel slide in từ 2 phía)
- pro/con item reveal: 0.5s mỗi item, dùng `LaggedStart`
- roadmap path `Create`: 2.0s
- milestone node pop: 0.6s mỗi node
- merge `Transform` (Scene 31 "best of both"): 1.5s
- `Flash` / `Indicate`: 0.5s

### 7.3. Comparison fairness (RẤT QUAN TRỌNG phần 4)

- Mỗi vs-card: panel EBGM (phải) viền `EBGM_BRAND`, panel đối thủ (trái) viền màu riêng của đối thủ.
- KHÔNG làm panel đối thủ "xấu" hơn (mờ hơn, nhỏ hơn). Hai panel cân xứng.
- Khi EBGM thắng ở 1 khía cạnh → `Indicate` panel EBGM. Khi đối thủ thắng → `Indicate` panel đối thủ (vd Lanitis distortion model, PCA frontal accuracy).

### 7.4. Honest tone

- Khi show số liệu EBGM thua: dùng màu trung tính (TEXT_MUTED hoặc CON_COLOR nhẹ), KHÔNG né tránh.
- Câu chốt mỗi scene phải phản ánh đúng tinh thần paper: EBGM linh hoạt & thực tế, nhưng không vô địch mọi mặt.

### 7.5. Ending (Scene 35) đặc biệt

- Đây là cao trào cảm xúc — pacing CHẬM hơn các scene khác.
- Image graph rotation: rất chậm (`run_time=8` cho 1 vòng nhẹ, hoặc dùng `Rotating`).
- Message fade in: mỗi dòng cách nhau 2s, để khán giả "ngấm".
- Fade to navy cuối cùng: `run_time=2`.

---

## 🔁 8. CHIẾN LƯỢC SINH CODE

**KHÔNG sinh cả 9 scene trong 1 lần.** Sinh từng scene:

**Turn 1 (turn này):** Sinh **Scene 27** (intro + tính tổng quát) + verify helpers mới (`make_vs_card`, `pro_item`, `con_item`, `future_node`).

**Các turn tiếp:** User yêu cầu "tiếp Scene 28"... — sinh từng cái.

**Mỗi scene, kết thúc bằng:**
1. Lệnh render
2. Verification points
3. Câu hỏi: *"Bạn muốn tôi sinh Scene <N+1> không?"*

> **Lưu ý đặc biệt:** Scene 35 là scene CUỐI của toàn series. Khi sinh xong Scene 35, thay vì hỏi tiếp, hãy chúc mừng đã hoàn thành toàn bộ 35 scenes và gợi ý các bước tiếp theo (concatenate video, thêm music, render high-quality).

---

## ✅ 9. SELF-VALIDATION CHECKLIST

Trước khi gửi code:

- [ ] Import đúng `from manim import *`
- [ ] Mọi chuỗi tiếng Việt dùng `Text()`, KHÔNG `Tex()`/`MathTex()`
- [ ] Đã set `self.camera.background_color = BG_NAVY`
- [ ] Helpers phần 4 (`make_vs_card`, `pro_item`, `con_item`, `future_node`) đầy đủ ở đầu file
- [ ] Check/cross icon vẽ bằng `Line`, KHÔNG dùng emoji/Unicode ký tự
- [ ] Tất cả số liệu khớp `discussion.md` (đặc biệt honest notes)
- [ ] EBGM color `#B8B5FF` nhất quán
- [ ] Màu đối thủ công bằng (không red gắt)
- [ ] Honest notes được giữ nguyên (PCA 99%, EBGM 18% ở 45°)
- [ ] Mọi `ImageMobject` có try/except fallback
- [ ] Cuối scene có `FadeOut(*self.mobjects)`
- [ ] Comment đầu file: font + lệnh render
- [ ] Tổng thời lượng khớp mục tiêu trong `discussion.md` (±10%)
- [ ] Phụ đề khớp bảng timing
- [ ] (Scene 35) Pacing chậm, elegant cho ending

---

## 📤 10. OUTPUT FORMAT

````
## Scene <N>: <Tên>

**Mục tiêu:** <1 câu>
**Thời lượng dự kiến:** <X>s
**Assets cần thiết:** <liệt kê hoặc "không">
**Key data points:** <list số liệu dùng trong scene>

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
- <điểm 3: honest note nào cần giữ>

---

Bạn muốn tôi sinh **Scene <N+1>: <tên scene tiếp theo>** không?
````

---

## 🎬 11. YÊU CẦU CỤ THỂ CHO TURN ĐẦU TIÊN

Trong turn này:

1. **Đọc kỹ `discussion.md`** đính kèm.
2. **Sinh `scene_27_intro_generality.py`** đầy đủ với:
   - Phase A (0–12s): tiêu đề + câu hỏi mở "EBGM đứng ở đâu?"
   - Phase B (12–32s): "IN-CLASS RECOGNITION" trung tâm + 4 ví dụ orbit (khuôn mặt, động vật, xe, thực vật) — icon vẽ tay
   - Phase C (32–45s): 3 badge ưu thế (no training, one image, 22° robust)
   - Đầy đủ helpers ở đầu file
3. **Đừng quên fallback** cho mọi visual asset.
4. **Kết thúc bằng** câu hỏi có muốn tiếp Scene 28 không.

---

## 🚫 12. KHÔNG ĐƯỢC LÀM

- ❌ Sinh code Manim cũ (ShowCreation, GraphScene, etc.)
- ❌ Dùng `Tex()` cho tiếng Việt
- ❌ Hard-code màu hex rời rạc — luôn dùng constant
- ❌ Bỏ qua phụ đề
- ❌ Tự ý thay đổi/làm đẹp số liệu (KHÔNG được biến 98% → 100%, KHÔNG bỏ honest note)
- ❌ Tự thêm/bỏ scene
- ❌ Sinh tất cả 9 scene trong 1 turn
- ❌ Dùng emoji trong text rendered bởi Manim
- ❌ Dùng màu red gắt / cảnh báo cho đối thủ benchmark
- ❌ Làm panel đối thủ "xấu" hơn panel EBGM (phải cân xứng)
- ❌ Bỏ qua honest notes của paper

---

## 📚 13. REFERENCE — MANIM CE API CHEAT SHEET (Phần 4 focus)

**Comparison & layout:**
- `RoundedRectangle(width, height, corner_radius, fill_color, fill_opacity, stroke_color, stroke_width)`
- `VGroup(*mobs).arrange(RIGHT/DOWN, buff=0.3)`
- `VGroup(*mobs).arrange_in_grid(rows, cols, buff)`
- `mob.move_to(other.get_center())`, `mob.next_to(other, direction, buff)`

**Roadmap / path:**
- `VMobject().set_points_smoothly([p1, p2, p3, ...])` — đường cong mượt
- `CubicBezier(start, h1, h2, end)` — bezier curve
- `MoveAlongPath(mob, path)` — di chuyển dọc path
- `self.play(self.camera.frame.animate.move_to(point))` — chỉ MovingCameraScene

**Orbit animation (Scene 27):**
- `Rotate(mob, angle, about_point=ORIGIN)` — xoay quanh tâm
- `mob.animate.rotate(angle, about_point=center)`
- Hoặc dùng `Rotating(mob, radians, about_point, run_time)`

**Animations:**
- `Create`, `Write`, `FadeIn(shift=)`, `FadeOut`
- `Transform`, `ReplacementTransform`
- `Indicate(mob, color, scale_factor)`, `Flash(point, color)`
- `Wiggle(mob)` — cho glitch effect (Scene 29)
- `LaggedStart(*anims, lag_ratio)`
- `GrowFromCenter`, `GrowFromEdge`
- `Rotating(mob, radians=TAU, run_time=8)` — slow rotation (Scene 35 ending)

**Camera (cho roadmap & ending):**
- Nếu cần camera move → dùng `MovingCameraScene` thay vì `Scene`
- `self.camera.frame.animate.scale(0.8).move_to(point)`

---

## 🏁 14. BẮT ĐẦU

Sau khi đọc xong prompt này và `discussion.md`:

1. Confirm ngắn (1 câu) rằng đã hiểu task — và rằng đây là phần CUỐI của series (Scene 27–35).
2. Đề xuất bổ sung 4 helpers mới (`make_vs_card`, `pro_item`, `con_item`, `future_node`) vào `_common.py` (hoặc inline).
3. Sinh `scene_27_intro_generality.py` theo template ở mục 5.2 và storyboard Scene 27.
4. Hỏi user có muốn tiếp Scene 28 không.

**Bắt đầu nào.**