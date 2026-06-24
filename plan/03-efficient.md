# 🎬 PLAN VIDEO MANIM — PHẦN 3: EXPERIMENTS & HIỆU QUẢ EBGM

> **Phần:** Experiments — Chứng minh hiệu quả của EBGM
> **Cấu trúc:** Databases → Matching Accuracy → Computational Efficiency → Benchmarks
> **Thời lượng dự kiến:** 6–7 phút
> **Số scenes:** 8

---

## 🎨 0. KẾ THỪA SETUP

Tái sử dụng **toàn bộ** setup từ `overview.md` và `algo_detail.md`:
- Bảng màu (navy + cool accents)
- Font latex thuần
- Helper functions (`make_subtitle`, `section_title`, `vietnamese_label`)
- **Signature color:** `ACCENT_LAVENDER (#B8B5FF)` cho EBGM

### Bổ sung cho phần này

```python
# Màu cho data visualization
BAR_PRIMARY   = "#48CAE4"   # cyan - thanh bar chính
BAR_SECONDARY = "#778DA9"   # blue-grey - thanh bar so sánh
BAR_SUCCESS   = "#95D5B2"   # mint - kết quả tốt
BAR_WARNING   = "#E29578"   # coral - kết quả kém
TROPHY_GOLD   = "#FCBF49"   # vàng ấm - chỉ dùng khi nhấn mạnh "best"

# Specific cho phần Experiments
EBGM_BRAND    = "#B8B5FF"   # luôn dùng cho EBGM trong mọi comparison
PCA_COLOR     = "#76C5BF"   # teal - cho PCA
NN_COLOR      = "#E29578"   # coral - cho Neural Network
PREV_COLOR    = "#778DA9"   # blue-grey - cho preceding system
```

### Helper bổ sung

```python
def make_bar_chart(values, labels, max_val=100, bar_color=BAR_PRIMARY, 
                   highlight_idx=None, scale=1.0):
    """
    Tạo bar chart ngang.
    values: list of float (0-100, percentage)
    labels: list of string
    highlight_idx: index của bar được nhấn mạnh (sẽ đổi màu thành EBGM_BRAND)
    """
    bars = VGroup()
    for i, (val, lbl) in enumerate(zip(values, labels)):
        color = EBGM_BRAND if i == highlight_idx else bar_color
        # Bar
        bar = Rectangle(
            width=val/max_val * 4.0,
            height=0.35,
            fill_color=color,
            fill_opacity=0.85,
            stroke_color=color,
            stroke_width=1
        )
        bar.shift(DOWN * i * 0.55 + RIGHT * (val/max_val * 2.0))
        # Label trái
        lbl_text = Text(lbl, font=SUBTITLE_FONT, color=TEXT_PRIMARY, 
                        weight=LIGHT).scale(0.35)
        lbl_text.next_to(bar, LEFT, buff=0.3).align_to(bar, LEFT).shift(LEFT*0.5)
        # Value phải
        val_text = Text(f"{val:.0f}%", font=MONO_FONT, color=color,
                        weight=MEDIUM).scale(0.4)
        val_text.next_to(bar, RIGHT, buff=0.2)
        bars.add(VGroup(bar, lbl_text, val_text))
    return bars.scale(scale)

def make_percentage_circle(value, color=BAR_PRIMARY, radius=1.0):
    """
    Donut chart: 1 con số phần trăm ở giữa, vòng tròn lấp đầy theo %.
    """
    bg_ring = Circle(radius=radius, color=GRID_LINE, stroke_width=8).set_opacity(0.3)
    progress_ring = Arc(
        radius=radius,
        start_angle=PI/2,
        angle=-2*PI * (value/100),
        stroke_width=10,
        color=color
    )
    text = Text(f"{value:.0f}%", font=TITLE_FONT, color=color,
                weight=MEDIUM).scale(0.9 * radius)
    return VGroup(bg_ring, progress_ring, text)

def trophy_icon(color=TROPHY_GOLD, scale=0.6):
    """Icon trophy vẽ bằng VMobject (không dùng emoji)."""
    cup = VGroup(
        # Cup body
        ArcPolygon([-0.4,0.5,0], [0.4,0.5,0], [0.3,-0.3,0], [-0.3,-0.3,0],
                   color=color, fill_opacity=0.8, stroke_width=2),
        # Handles
        Arc(radius=0.2, start_angle=PI/2, angle=-PI, color=color, 
            stroke_width=3).shift(LEFT*0.4),
        Arc(radius=0.2, start_angle=PI/2, angle=PI, color=color,
            stroke_width=3).shift(RIGHT*0.4),
        # Base
        Rectangle(width=0.5, height=0.1, color=color, fill_opacity=0.8
                  ).shift(DOWN*0.4),
        Rectangle(width=0.8, height=0.08, color=color, fill_opacity=0.8
                  ).shift(DOWN*0.5),
    )
    return cup.scale(scale)
```

---

## 📋 STRUCTURE TỔNG QUAN

| Scene | Tên | Thời lượng |
|---|---|---|
| 19 | Intro "EBGM tốt đến đâu?" | 20s |
| 20 | Databases — FERET & Bochum | 50s |
| 21 | Results trên FERET | 75s |
| 22 | Results trên Bochum (Cross-pose) | 60s |
| 23 | Matching Accuracy — Pha vs Không pha | 70s |
| 24 | Computational Efficiency — Speed | 55s |
| 25 | Benchmarks — So sánh với các hệ thống khác | 90s |
| 26 | Tổng kết phần 3 | 25s |

**Tổng:** ~7 phút 25 giây.

---

# 📽️ SCENE 19 — INTRO: "EBGM TỐT ĐẾN ĐÂU?" (≈ 20s)

## 🎯 Mục đích
Mở đầu phần Experiments — đặt câu hỏi lớn: thuật toán đẹp về lý thuyết, nhưng thực tế thì sao?

## 🎨 Visual storyboard

**Phase A (0s–8s):** Background navy. Giữa màn hình hiện câu hỏi lớn:

> *"Lý thuyết đã rõ — nhưng EBGM thực sự hiệu quả đến đâu?"*

- Font EB Garamond, scale 0.7, màu `TEXT_PRIMARY`, weight LIGHT.
- Phía sau có 1 grid 5×5 các "khuôn mặt mờ" (placeholder rectangles với gradient cyan) trôi nhẹ — gợi ý gallery của database.

**Phase B (8s–20s):** Câu hỏi co lại thành header. Hiện 4 "thẻ tiêu chí" xếp 2×2 — 4 khía cạnh sẽ được kiểm chứng:

```
┌──────────────┬──────────────┐
│  ① ACCURACY  │  ② MATCHING  │
│              │   PRECISION  │
│  Trên DB     │              │
│  lớn?        │  Bao chính   │
│              │  xác?        │
├──────────────┼──────────────┤
│  ③ SPEED     │  ④ BENCH-    │
│              │    MARKS     │
│  Đủ nhanh    │              │
│  thực tế?    │  Hơn các     │
│              │  hệ khác?    │
└──────────────┴──────────────┘
```

- Mỗi card pop in qua `LaggedStart(FadeIn(shift=UP*0.3))`, lag 0.35s.
- Đánh số `①②③④` to ở góc mỗi card, màu `ACCENT_LAVENDER`.
- Khi card ④ xuất hiện, một `Flash` cyan ở tâm 4 card → câu chốt fade in:
  > *"Bốn câu hỏi — bốn câu trả lời."*

## 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–7s | "Lý thuyết đã rõ — nhưng EBGM thực sự hiệu quả đến đâu?" |
| 7s–13s | "Bốn khía cạnh sẽ được kiểm chứng" |
| 13s–20s | "Độ chính xác, độ định vị, tốc độ và so sánh với các hệ thống khác" |

## 🛠️ Manim techniques
`Text`, `Rectangle`, `LaggedStart`, `Flash`.

---

# 📽️ SCENE 20 — DATABASES: FERET & BOCHUM (≈ 50s)

## 🎯 Mục đích
Giới thiệu 2 database được dùng — đặt ngữ cảnh cho mọi kết quả sau.

## 🎨 Visual storyboard

### Phase A (0s–8s): Setup câu hỏi

- Tiêu đề: **"Thử nghiệm trên cơ sở dữ liệu nào?"** (lavender).
- Hint thiết kế: *"Mỗi gallery — đúng MỘT ảnh cho mỗi người."* (highlight cyan để nhấn mạnh đây là setup khó).

### Phase B (8s–32s): FERET Database

Layout chia đôi — bên trái là logo/banner mock "FERET", bên phải là grid 5 ảnh đại diện cho các pose.

**Bên trái:**
- Box lớn navy_soft, viền cyan: 
  ```
  ┌──────────────────────────────┐
  │  ARPA/ARL FERET DATABASE     │
  │  US Army Research Lab        │
  │                              │
  │  • 250 người (gallery)       │
  │  • 1 ảnh / người             │
  │  • Resolution: 256×384       │
  │  • Background: thuần         │
  └──────────────────────────────┘
  ```
- Pop in qua `FadeIn(shift=RIGHT*0.3)`.

**Bên phải:** 4 ô poses xếp ngang, mỗi ô có placeholder face silhouette ở pose tương ứng:
- **Frontal** (chính diện) — silhouette nhìn thẳng
- **Half-profile** (nghiêng 40–70°) — silhouette nghiêng
- **Profile** (nghiêng 90°) — silhouette nhìn ngang
- **Frontal B** — kèm chữ "(biểu cảm khác)"

- Mỗi ô có nhãn nhỏ phía dưới (vietnamese_label).
- Các ô pop in lần lượt, kèm `Indicate` khi xuất hiện.
- Khi ô profile xuất hiện, có dòng chú thích: *"Sự thay đổi 40–70° rất khó cho mọi thuật toán."*

### Phase C (32s–50s): Bochum Database

Bên trái biến mất, slide sang phải. Bên trái mới là Bochum:

```
┌──────────────────────────────┐
│  BOCHUM DATABASE             │
│  Institute for Neural Comp.  │
│                              │
│  • 108 người (gallery)       │
│  • Poses: 0°, 11°, 22°       │
│  • Biểu cảm: neutral + khác  │
│  • Mục đích: test cross-pose │
└──────────────────────────────┘
```

**Bên phải:** 3 ô poses góc xoay nhỏ:
- 0° (frontal, neutral)
- 11° (lệch nhẹ)
- 22° (lệch vừa)

- Một mũi tên cong (lavender) **kết nối** 0° → 11° → 22°, kèm chú thích: *"Cross-pose challenge — match ảnh nghiêng vs gallery chính diện."*

## 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–6s | "Hai cơ sở dữ liệu lớn được sử dụng để kiểm chứng" |
| 6s–14s | "FERET — 250 người, do quân đội Mỹ cung cấp" |
| 14s–22s | "Bốn tư thế: chính diện, nghiêng 40-70°, profile, biểu cảm khác" |
| 22s–32s | "Setup khắc nghiệt: gallery chỉ có MỘT ảnh cho mỗi người" |
| 32s–42s | "Bochum — 108 người, tập trung vào kiểm tra xoay nhỏ trong không gian 3D" |
| 42s–50s | "Mục tiêu: matching ảnh xoay 11° và 22° với ảnh mẫu chính diện" |

## 🛠️ Manim techniques
`Rectangle` (cho info boxes), face silhouettes (vector fallback), `CurvedArrow`, `FadeIn(shift)`, `LaggedStart`.

---

# 📽️ SCENE 21 — RESULTS TRÊN FERET (≈ 75s)

## 🎯 Mục đích
Visualize bảng kết quả FERET (Table 1 của paper). Highlight 98% frontal & 84% profile.

## 🎨 Visual storyboard

### Phase A (0s–10s): Setup

- Tiêu đề: **"FERET — Kết quả Rank-1 Recognition"** (lavender).
- Câu dẫn: *"Mỗi gallery 250 người — bao nhiêu lần đoán đúng?"*

### Phase B (10s–35s): Bar chart chính

Hiện bar chart ngang (dùng `make_bar_chart`):

| Test case | Accuracy | Color |
|---|---|---|
| Frontal (fa) vs Frontal (fb) | **98%** | EBGM_BRAND (highlight) |
| Profile right vs left | **84%** | BAR_PRIMARY |
| Half-profile right vs left | **57%** | BAR_PRIMARY |
| Half-profile vs frontal | **18%** | BAR_WARNING |
| Half-profile vs profile | **12%** | BAR_WARNING |

**Animation:**
1. **(10s–15s)** Trục axes vẽ ra bằng `Create`.
2. **(15s–25s)** Mỗi bar "lên" từ 0 → giá trị thật, dùng `ValueTracker` + `always_redraw`. Lần lượt từng bar, lag 1s.
3. **(25s–30s)** Bar **98%** được nhấn mạnh: `Flash` cyan + scale up nhẹ + trophy_icon xuất hiện bên cạnh.
4. **(30s–35s)** Bar **84%** cũng được spotlight (nhỏ hơn): glow lavender + label "Đáng chú ý cho profile!".

### Phase C (35s–55s): Insight — Tại sao kết quả thay đổi?

Bar chart fade ra mép trái (giữ ở góc nhỏ). Bên phải hiện 3 boxes giải thích:

**Box 1 (35s–42s):** *"Frontal vs Frontal: ảnh chỉ khác nhau chút biểu cảm → DỄ."*
- Visualize: 2 silhouettes frontal cạnh nhau, edge `Indicate` ở các điểm giống nhau.

**Box 2 (42s–48s):** *"Profile (lật ngược) vs Profile: tận dụng đối xứng khuôn mặt → vẫn ổn."*
- Visualize: 1 silhouette profile bên trái + mũi tên `↔` (flip horizontal) + silhouette profile bên phải.

**Box 3 (48s–55s):** *"Half-profile vs Frontal: góc xoay 40-70° quá lớn → KHÓ."*
- Visualize: silhouette half-profile + silhouette frontal + dấu `≠` lớn coral ở giữa.

### Phase D (55s–75s): Take-away

- Tất cả fade ra, hiện 1 dòng lớn ở giữa:
  > **"Performance đỉnh khi pose tương đồng. Performance suy giảm khi rotation in depth tăng."**

- Bên dưới: 2 số liệu chính được "spotlight":
  - **98%** ở 1 vòng tròn lớn (dùng `make_percentage_circle`) — màu EBGM_BRAND
  - **84%** ở 1 vòng tròn nhỏ hơn bên cạnh — màu BAR_PRIMARY

- Cả 2 vòng tròn xuất hiện qua `GrowFromCenter` + arc filling animation (sweep từ top sang full).

## 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–6s | "Trên FERET — kết quả nhận diện rank-1" |
| 6s–14s | "Chính diện vs chính diện: 98% — gần như hoàn hảo" |
| 14s–22s | "Profile vs profile (sau khi lật): 84% — rất ấn tượng" |
| 22s–30s | "Nhưng khi pose chênh lệch nhiều, độ chính xác giảm đáng kể" |
| 30s–40s | "Frontal vs frontal dễ — chỉ khác biểu cảm nhỏ" |
| 40s–50s | "Profile lật ngược tận dụng được tính đối xứng của khuôn mặt" |
| 50s–60s | "Half-profile có góc xoay rất lớn — đây là giới hạn thật của EBGM" |
| 60s–75s | "Kết luận: EBGM xuất sắc trong cùng pose, vẫn cần cải thiện cross-pose" |

## 🛠️ Manim techniques
`make_bar_chart`, `ValueTracker`, `always_redraw`, `Flash`, `make_percentage_circle`, `GrowFromCenter`.

---

# 📽️ SCENE 22 — RESULTS TRÊN BOCHUM (CROSS-POSE) (≈ 60s)

## 🎯 Mục đích
Highlight khả năng xử lý xoay nhẹ trong không gian 3D — 94% ở 11°, 88% ở 22°.

## 🎨 Visual storyboard

### Phase A (0s–10s): Setup

- Tiêu đề: **"Bochum — Cross-Pose Recognition"** (lavender).
- Câu dẫn: *"Gallery: 108 ảnh chính diện. Probe: ảnh xoay 11° hoặc 22°. Có nhận ra không?"*

### Phase B (10s–35s): Visualize 3 góc xoay với kết quả

Layout: 3 cụm xếp ngang, mỗi cụm gồm (silhouette + percentage circle).

```
┌──────────┐   ┌──────────┐   ┌──────────┐
│  0°      │   │  11°     │   │  22°     │
│ (neutral │   │  rotated │   │  rotated │
│  vs fb)  │   │  vs front│   │  vs front│
│          │   │          │   │          │
│ [face]   │   │ [face]   │   │ [face]   │
│          │   │          │   │          │
│ ◯ 91%    │   │ ◯ 94%    │   │ ◯ 88%    │
└──────────┘   └──────────┘   └──────────┘
```

**Animation:**
1. **(10s–18s)** 3 silhouettes appear lần lượt — mỗi cái xoay tăng dần (0°, 11°, 22°).
   - Dùng `rotate` cho silhouette.
2. **(18s–28s)** Donut chart (`make_percentage_circle`) xuất hiện dưới mỗi silhouette, fill animation từ 0 → giá trị thật.
   - 91% (mint), 94% (mint, brighter), 88% (cyan)
3. **(28s–35s)** Một mũi tên nằm ngang chạy từ phải sang trái nối 3 cluster, kèm note: *"Performance giảm dần khi góc xoay tăng — nhưng vẫn cao."*

### Phase C (35s–55s): Comparison với hệ thống cũ

Bên cạnh hiện một bảng so sánh nhỏ:

| Probe pose | Preceding system | THIS system (EBGM) |
|---|---|---|
| 0° (fb) | 92% | **91%** |
| 11° rotated | 97% | **94%** |
| 22° rotated | 85% | **88%** |

- Highlight: 22° là case EBGM tốt HƠN — 88% vs 85%.
- Cột EBGM dùng màu `EBGM_BRAND`, cột preceding dùng `PREV_COLOR`.
- Khi mỗi hàng xuất hiện, dùng `Indicate` cho ô EBGM tương ứng.
- Note bên cạnh: *"EBGM dùng ít hơn 30 nodes (thay vì 70), không cần resize ảnh → hiệu suất tốt hơn với ít thông tin."*

### Phase D (55s–60s): Insight ngắn

- Câu chốt: *"EBGM xử lý xoay nhẹ trong 3D rất tốt — đặc tính Gabor wavelet phát huy."*

## 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–6s | "Bài test cross-pose — match ảnh nghiêng với gallery chính diện" |
| 6s–14s | "Xoay 11°: 94% — gần như không bị ảnh hưởng" |
| 14s–22s | "Xoay 22°: 88% — vẫn rất tốt" |
| 22s–32s | "Mức suy giảm rất nhẹ — Gabor wavelet trơ lì với biến đổi nhỏ" |
| 32s–42s | "So với hệ thống tiền nhiệm — EBGM tốt hơn ở case 22°" |
| 42s–52s | "Mà chỉ cần 30 nodes thay vì 70 — ít thông tin, hiệu quả hơn" |
| 52s–60s | "EBGM xử lý xoay 3D nhỏ rất tốt nhờ đặc tính Gabor wavelet" |

## 🛠️ Manim techniques
`rotate`, `make_percentage_circle`, table layout (`VGroup` + `arrange_in_grid`), `Indicate`.

---

# 📽️ SCENE 23 — MATCHING ACCURACY: PHA VS KHÔNG PHA (≈ 70s)

## 🎯 Mục đích
Chứng minh tầm quan trọng của pha — sai số 1.6px vs 5.2px, recognition rate 88% vs 67%.

## 🎨 Visual storyboard

### Phase A (0s–10s): Câu hỏi

- Tiêu đề: **"Tại sao pha quan trọng?"** (cyan — vì đây là về Gabor).
- Câu hỏi: *"Bỏ qua pha thì sao? Đây là thí nghiệm trực quan nhất."*

### Phase B (10s–35s): Visualize matching accuracy

**Layout chia đôi (split-screen):**

**Bên trái: "Không dùng pha"** (header coral)
- Một silhouette mặt với các nodes (~16 nodes) được "matched" lên.
- Mỗi node có 2 chấm: 
  - Chấm hồng = "Manual reference" (vị trí chuẩn do người đánh dấu)
  - Chấm cyan = "Auto matched" (vị trí thuật toán đoán)
- Các cặp chấm cách nhau **TRUNG BÌNH 5.2 pixels** — visualize bằng đường nối ngắn `coral`.
- Một vài node bị sai hẳn (ví dụ "node 5 từ trên xuống bên phải" sai hẳn — chú thích "wrong side of edge").
- Số liệu lớn bên dưới: **5.2 px** trong vòng tròn coral.

**Bên phải: "Dùng pha"** (header mint)
- Same setup, nhưng các chấm cyan **trùng khít** hoặc rất sát với chấm hồng.
- Trung bình **1.6 pixels** sai số.
- Số liệu lớn bên dưới: **1.6 px** trong vòng tròn mint.

**Animation:**
1. **(10s–15s)** Cả 2 side hiện ra cùng lúc, nodes pop in.
2. **(15s–25s)** Reference dots (hồng) xuất hiện trước. Sau đó algorithm dots (cyan) xuất hiện kèm hiệu ứng "tracing" line từ ref → algo dot.
3. **(25s–30s)** Đường nối được hiển thị với độ dài tỷ lệ thực.
4. **(30s–35s)** Số liệu lớn fade in.

### Phase C (35s–55s): Recognition rate khác biệt

Phần trên fade ra một chút (giữ làm context). Phần dưới hiện bar chart so sánh recognition rate (case test: 22° probe vs frontal gallery):

```
Manual positions:       96 / 108  (89%)  ████████████████████░
With phase matching:    95 / 108  (88%)  ████████████████████░
Without phase matching: 72 / 108  (67%)  ████████████████░░░░░
```

- Bar Manual & Phase: mint (gần như trùng nhau)
- Bar Without phase: coral
- `Indicate` ở phase bar khi xuất hiện.

**Insight:**
- Mũi tên to chỉ vào Phase bar: *"Phase ≈ Manual — đủ tốt cho recognition tốt nhất."*
- Mũi tên to chỉ vào Without phase bar: *"Mất 21% recognition rate!"*

### Phase D (55s–70s): Take-away

Câu chốt fade in:
> *"Phase không chỉ làm matching chính xác hơn — nó CỨU recognition rate."*

Số liệu cuối:
- **1.6 px** vs **5.2 px** → matching accuracy: **3.25× tốt hơn**
- **88%** vs **67%** → recognition rate: **+21 percentage points**

## 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–6s | "Pha trong Gabor wavelet quan trọng thế nào?" |
| 6s–14s | "So sánh trực tiếp: matching có phase vs không phase" |
| 14s–22s | "Không phase: trung bình 5.2 pixel sai so với người đánh dấu thủ công" |
| 22s–30s | "Có phase: chỉ 1.6 pixel — chính xác đến subpixel" |
| 30s–40s | "Khác biệt 3 lần — nhưng ảnh hưởng đến recognition thế nào?" |
| 40s–50s | "Test trên ảnh xoay 22°: dùng phase đạt 88%" |
| 50s–60s | "Bỏ phase: chỉ còn 67% — mất 21 điểm phần trăm" |
| 60s–70s | "Phase không chỉ chính xác hơn — nó cứu cả hệ thống nhận diện" |

## 🛠️ Manim techniques
Side-by-side comparison, `Dot` clusters với 2 màu, `Line` connections, `make_percentage_circle`, bar chart, `Indicate`.

---

# 📽️ SCENE 24 — COMPUTATIONAL EFFICIENCY (≈ 55s)

## 🎯 Mục đích
Visualize tốc độ — EBGM nhanh đáng kể so với hệ tiền nhiệm.

## 🎨 Visual storyboard

### Phase A (0s–10s): Câu hỏi

- Tiêu đề: **"EBGM có nhanh không?"** (lavender).
- Sub: *"Real-time application — feasible hay không?"*

### Phase B (10s–30s): Timeline visualization

Layout: 2 timeline ngang, một cho preceding system, một cho EBGM.

**Setup:** Visualize task "Compare 1 probe to gallery"

```
Preceding system (1993):
├──────────────────────────────────┤
0s                              25s
└─ Compare with 87 models = 25 seconds

EBGM (1999):
├─┤
0s 1s
└─ Compare with ~300 models = under 1 second!
```

**Animation:**
1. **(10s–15s)** Timeline preceding system: thanh dài từ 0 đến 25s. Lấp đầy dần (animation 5s) màu PREV_COLOR. Khi đầy, hiện số "87 models / 25s".
2. **(15s–22s)** Timeline EBGM: thanh ngắn xíu (1/25 chiều dài). Lấp đầy gần như tức thì (0.5s) màu EBGM_BRAND. Hiện số "~300 models / 1s".
3. **(22s–30s)** Hiện một **đồng hồ** to ở giữa, đang quay nhanh dần (`Rotate`). Bên trái: "OLD: 0.29 models/sec". Bên phải: "EBGM: 300 models/sec". Tỷ số: **~1000× nhanh hơn**.

### Phase C (30s–50s): Pipeline breakdown

Hiện diagram pipeline với thời gian:

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│ NEW IMAGE    │──────▶│ GRAPH        │──────▶│ COMPARE WITH │
│              │ ~30s  │ EXTRACTION   │ <1s   │ GALLERY      │
│              │       │ (1 time)     │       │ (every probe)│
└──────────────┘       └──────────────┘       └──────────────┘
                       Slow but one-off       Lightning fast
```

- Animation: 1 probe image "rơi" vào pipeline, kèm timer chạy.
- Khi sang phase Comparison, timer chạy CỰC NHANH (text "0.0... s" tăng siêu nhanh).
- Highlight: comparison chỉ tốn <1s với 300 models.

**Insight box:**
> *"Tách bạch: extraction (chậm 1 lần) vs comparison (nhanh nhiều lần)."*

### Phase D (50s–55s): Real-world implication

- Câu chốt: *"Đủ nhanh cho ứng dụng thực tế — kể cả với database lớn."*
- Small note italic: *"(Cùng nhóm sau này đã commercial hóa thành ZN-Face access control system.)"*

## 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–6s | "EBGM có đủ nhanh cho ứng dụng thực tế không?" |
| 6s–14s | "Hệ thống tiền nhiệm: 25 giây để so sánh với 87 models" |
| 14s–22s | "EBGM: chỉ 1 giây để so sánh với 300 models" |
| 22s–32s | "Tốc độ tăng khoảng 1000 lần" |
| 32s–42s | "Bí quyết: tách bạch extraction (chậm, 1 lần) khỏi comparison (siêu nhanh)" |
| 42s–55s | "Đủ nhanh cho database lớn — và đã được thương mại hóa thành công" |

## 🛠️ Manim techniques
Timeline bars với `ValueTracker`, `Rotate` cho đồng hồ, pipeline diagram, sequential `Transform`.

---

# 📽️ SCENE 25 — BENCHMARKS: EBGM VS CÁC HỆ THỐNG KHÁC (≈ 90s)

## 🎯 Mục đích
So sánh trực tiếp EBGM với PCA, Neural Networks, cross-correlation trên FERET.

## 🎨 Visual storyboard

### Phase A (0s–10s): Setup

- Tiêu đề: **"Blind Test — EBGM đối đầu với ai?"** (lavender).
- Sub: *"FERET blind test, US Army Research Lab"*
- 4 logo/name mock xếp ngang: 
  - PCA (Moghaddam & Pentland)
  - NN-RBF (Gutta et al.)
  - Cross-correlation (Gordon)
  - **EBGM** (highlight, glow lavender)

### Phase B (10s–40s): Big bar chart comparison

Hiện grouped bar chart — frontal recognition rate trên FERET:

```
EBGM (this work, 1995-1997)       ██████████████████ 98%
PCA (Moghaddam & Pentland)        ██████████████████ 99%
Matching Pursuit (Phillips)       ██████████████████ 97%
Cross-correlation (Gordon)        ████████████░░░░░░ 72%
RBF Neural Net (Gutta)            ████████████████░░ 83%
```

**Animation:**
1. **(10s–18s)** Trục axes + nhãn methods xuất hiện.
2. **(18s–32s)** Mỗi bar grow lên qua `ValueTracker`, lag 1.5s.
   - PCA: PCA_COLOR (teal)
   - NN: NN_COLOR (coral nhạt)
   - Cross-correlation: PREV_COLOR (blue-grey)
   - Matching Pursuit: BAR_SECONDARY
   - **EBGM: EBGM_BRAND** (lavender, viền đậm hơn)
3. **(32s–40s)** EBGM bar được nhấn mạnh: glow lavender + small trophy icon bên cạnh.

### Phase C (40s–60s): Insight — EBGM không chỉ nhanh

Bar chart shrink xuống mép trái. Bên phải hiện 3 cards về điểm mạnh CỦA EBGM SO VỚI PCA:

**Card 1 (40s–46s):** **"Không cần alignment cẩn thận"**
- Visualize: PCA cần ảnh được căn chỉnh chính xác (mắt-mắt cùng vị trí). EBGM tự xử lý qua matching.
- Icon: lưới với mũi tên căn chỉnh vs khuôn mặt với graph tự match.

**Card 2 (46s–52s):** **"Học ngoại lệ không cần lập trình lại"**
- Visualize: 1 ảnh người đeo kính được "thêm vào bunch" → graph thích nghi tự động.
- Icon: dấu `+` lavender → bunch graph có thêm 1 layer.

**Card 3 (52s–60s):** **"Robust với rotation in depth"**
- Visualize: 3 ảnh xoay 0°, 22°, 45° — EBGM stable hơn PCA.
- Mini chart: PCA giảm sharp ở 45°, EBGM giảm thoải.

### Phase D (60s–85s): Comparison table chi tiết

Hiện bảng so sánh:

| Aspect | PCA | NN | EBGM |
|---|---|---|---|
| Frontal accuracy | 99% | 83% | 98% |
| Half-profile | 38% | — | 57% |
| Profile | 32% | — | 84% |
| Cần alignment? | YES | NO | NO |
| Học ngoại lệ? | NO | retrain | ADD |
| Tốc độ | Fast | Medium | Fast |

- Cột EBGM dùng `EBGM_BRAND` background nhẹ.
- Mỗi hàng fade in tuần tự, lag 1.2s.
- Hàng "Half-profile" và "Profile": ô EBGM được `Indicate` (vì EBGM thắng).

### Phase E (85s–90s): Conclusion

Câu chốt:
> *"EBGM không phải #1 ở mọi thứ — nhưng linh hoạt, robust, và practical hơn."*

## 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–6s | "Blind test trên FERET — EBGM đối đầu với các đối thủ mạnh" |
| 6s–14s | "Trên ảnh chính diện: EBGM đạt 98%" |
| 14s–22s | "PCA đạt 99%, Matching Pursuit 97% — tất cả đều cao" |
| 22s–32s | "Neural Network RBF chỉ đạt 83% — yếu hơn đáng kể" |
| 32s–42s | "Cross-correlation chỉ 72% — không cạnh tranh nổi" |
| 42s–52s | "Nhưng EBGM còn nhiều ưu thế khác — không chỉ accuracy" |
| 52s–60s | "Không cần căn chỉnh ảnh quá cẩn thận như PCA" |
| 60s–70s | "Học ngoại lệ chỉ cần thêm ảnh — không cần huấn luyện lại" |
| 70s–80s | "Robust với rotation in depth — PCA suy giảm rất mạnh" |
| 80s–90s | "EBGM không vô địch mọi mặt — nhưng linh hoạt và thực tế nhất" |

## 🛠️ Manim techniques
Grouped bar chart, comparison cards với mini-visualizations, table layout, `Indicate`, sequential reveal.

---

# 📽️ SCENE 26 — TỔNG KẾT PHẦN 3 (≈ 25s)

## 🎯 Mục đích
Tóm lại 4 câu trả lời, dẫn vào phần Discussion.

## 🎨 Visual storyboard

### Phase A (0s–15s): Recap 4 câu hỏi với 4 câu trả lời

Hiện lại layout 4 card từ Scene 19, nhưng bây giờ mỗi card đã được fill với key number:

```
┌──────────────┬──────────────┐
│  ① ACCURACY  │  ② MATCHING  │
│              │   PRECISION  │
│   98% / 84%  │              │
│              │  1.6 px      │
│              │              │
├──────────────┼──────────────┤
│  ③ SPEED     │  ④ BENCH-    │
│              │    MARKS     │
│  ~1s         │              │
│  /300 models │  Top tier    │
│              │              │
└──────────────┴──────────────┘
```

- Mỗi card lần lượt được `Flash` + number scale up khi nhắc đến.
- Số liệu dùng MONO font, màu EBGM_BRAND.

### Phase B (15s–25s): Teaser cho phần Discussion

- Hiện text:
  > **"Tiếp theo: EBGM so với các hệ thống khác — và hướng phát triển tương lai"**
- Bên dưới: 3 keyword:
  - `vs PCA / Eigenfaces`
  - `vs Neural Networks` 
  - `Future improvements`
- Arrow lavender chỉ sang phải, `Flash`.

## 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–8s | "EBGM đã chứng minh cả bốn khía cạnh" |
| 8s–16s | "Độ chính xác cao, định vị tinh, tốc độ nhanh, benchmark top" |
| 16s–25s | "Tiếp theo: so sánh sâu hơn và hướng phát triển tương lai" |

## 🛠️ Manim techniques
Card layout recall, `Flash`, scale-up animation cho numbers, transition arrow.

---

## ✅ CHECKLIST CHO PHẦN 3

- [ ] Helper functions `make_bar_chart`, `make_percentage_circle`, `trophy_icon` đã test riêng.
- [ ] Tất cả con số khớp với paper:
  - FERET: 98%, 84%, 57%, 18%, 12%, 17%
  - Bochum: 91%, 94%, 88%
  - Matching: 1.6px vs 5.2px
  - Recognition (22°): 89% manual, 88% phase, 67% no-phase
  - Speed: 25s/87 models (old) vs <1s/~300 models (EBGM)
  - Benchmarks: EBGM 97-98%, PCA 99%, NN 83%, etc.
- [ ] Mọi bar chart có animation lên từ 0 (không pop ngay).
- [ ] EBGM brand color (`#B8B5FF`) nhất quán mọi nơi nhắc đến EBGM.
- [ ] Pacing: Scene 25 dài nhất (~90s) — đảm bảo không nhồi nhét.

---

## 🎯 GHI CHÚ ĐỊNH HƯỚNG SÁNG TẠO PHẦN 3

1. **Phần này là phần "data-heavy"** — visualize số liệu rất quan trọng. Đầu tư chất lượng bar chart, percentage circle.
2. **Đừng để khán giả "ngộp số":** Mỗi con số xuất hiện kèm context. Highlight con số chính, các con số phụ chỉ làm nền.
3. **Storytelling:** Mỗi scene là một "câu trả lời" cho 1 trong 4 câu hỏi setup ở Scene 19 — giữ liên kết này rõ ràng.
4. **Khi so sánh EBGM với hệ khác:** Không "dìm" đối thủ. EBGM không phải #1 mọi mặt (PCA frontal cao hơn) — trung thực điều này giúp video uy tín hơn.
5. **Pacing:** Sau mỗi animation lớn (bar grow, percentage fill), wait 1–1.5s cho khán giả đọc số.
6. **Music gợi ý:** Vẫn lo-fi/minimal piano, có thể thêm chút beat nhẹ ở Scene 24 (Speed) để tạo cảm giác "nhanh".

---

*End of Experiments plan. Sẵn sàng generate Manim code.*
