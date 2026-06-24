# 🎬 PLAN VIDEO MANIM — PHẦN 2: HOW EBGM WORKS

> **Phần:** Algorithm Detail
> **Cấu trúc:** Preprocessing (Gabor Wavelets) → Face Representation → Elastic Bunch Graph Matching → Recognition
> **Thời lượng dự kiến:** 9–10 phút
> **Số scenes:** 11

---

## 🎨 0. KẾ THỪA SETUP TỪ OVERVIEW

Phần này **tái sử dụng toàn bộ** từ `overview.md`nhưng font chữ đã đổi lại thành latex thuần (check code)
- Bảng màu (navy + cool accents)
- LaTeX tiếng Việt
- Helper functions (`make_subtitle`, `section_title`, `cool_glow`)
- **Signature color:** `ACCENT_LAVENDER (#B8B5FF)` cho mọi đối tượng EBGM-related

### Bổ sung cho phần này

```python
# Màu thêm cho phần kỹ thuật
GABOR_REAL    = "#48CAE4"   # cyan cho phần real của Gabor wavelet
GABOR_IMAG    = "#B8B5FF"   # lavender cho phần imaginary
JET_GLOW      = "#76C5BF"   # teal glow cho jet
GRID_LINE     = "#778DA9"   # blue-grey cho lưới grid mờ
HIGHLIGHT_HOT = "#FCBF49"   # vàng ấm RẤT THƯA THỚT, chỉ dùng nhấn mạnh focus điểm

# Math constants
FONT_MATH_SCALE = 0.8
```

### Helper bổ sung cho phần này

```python
def make_jet_visual(n_freq=5, n_orient=8, scale=1.0, color=GABOR_REAL):
    """
    Visualize jet: 40 wavelets xếp theo lưới (n_freq hàng x n_orient cột).
    Mỗi ô là 1 mini Gabor wavelet pattern.
    """
    grid = VGroup()
    for nu in range(n_freq):
        for mu in range(n_orient):
            kx = np.cos(mu * PI / n_orient)
            ky = np.sin(mu * PI / n_orient)
            freq = 0.5 + nu * 0.3
            wavelet = ParametricFunction(
                lambda t, kx=kx, freq=freq: np.array([
                    t * 0.3,
                    0.15 * np.sin(freq * t * 8) * np.exp(-(t**2)/0.5),
                    0
                ]),
                t_range=[-0.8, 0.8],
                color=color, stroke_width=1.2
            ).rotate(mu * PI / n_orient)
            wavelet.move_to([mu * 0.4 - 1.5, nu * 0.4 - 0.8, 0])
            grid.add(wavelet)
    return grid.scale(scale)

def make_face_graph_node(pos, jet_size=0.15, color=ACCENT_LAVENDER):
    """Một node trên image graph: chấm trung tâm + ring + mini jet."""
    return VGroup(
        Dot(pos, radius=0.06, color=color),
        Circle(radius=jet_size, color=color, stroke_width=1.5).move_to(pos),
    )

def vietnamese_label(text_str, scale=0.45, color=None):
    """Nhãn tiếng Việt nhỏ, dùng cho chú thích."""
    color = color or TEXT_MUTED
    return Text(text_str, font=SUBTITLE_FONT, color=color, weight=LIGHT).scale(scale)
```

---

## 📋 STRUCTURE TỔNG QUAN

| Scene | Tên | Thời lượng |
|---|---|---|
| 8 | Intro "How does EBGM work?" | 20s |
| 9 | Gabor Wavelets — Khái niệm cơ bản (Fig. 1) | 80s |
| 10 | Jet — 40 hệ số phức (Fig. 1 jet) | 60s |
| 11 | So sánh Jet — Similarity functions (Fig. 2) | 75s |
| 12 | Face Representation — Individual Graph | 65s |
| 13 | Face Bunch Graph — FBG (Fig. 3) | 70s |
| 14 | Graph Similarity Function | 55s |
| 15 | Matching Procedure — 4 bước (Fig. 4) | 110s |
| 16 | Two-stage Schedule | 50s |
| 17 | Recognition — So sánh & xếp hạng | 60s |
| 18 | Tổng kết phần 2 | 25s |

**Tổng:** ~10 phút 50 giây.

---

# 📽️ SCENE 8 — INTRO: "EBGM HOẠT ĐỘNG NHƯ THẾ NÀO?" (≈ 20s)

## 🎯 Mục đích
Mở đầu phần 2 — đặt câu hỏi lớn dẫn dắt vào toàn bộ phần kỹ thuật.

## 🎨 Visual storyboard

**Phase A (0s–8s):** Background navy. Một câu hỏi lớn ở giữa màn hình:

> *"Vậy EBGM thực sự hoạt động như thế nào?"*

- `Text` font EB Garamond, scale 0.75, màu `TEXT_PRIMARY`, weight LIGHT.
- Bên dưới câu hỏi: một dòng nhỏ italic `ACCENT_CYAN`: *"Đi từ pixel thô đến danh tính"*.

**Phase B (8s–20s):** Câu hỏi co lại thành header phía trên. Hiện ra **roadmap 4 bước** dưới dạng pipeline ngang với mũi tên kết nối:

```
┌─────────────┐   ┌─────────────┐   ┌──────────────┐   ┌─────────────┐
│  1. GABOR   │──▶│  2. FACE    │──▶│  3. ELASTIC  │──▶│  4. RECOG-  │
│   WAVELETS  │   │   REPRESEN- │   │     BUNCH    │   │    NITION   │
│ (Tiền xử lý)│   │   TATION    │   │   GRAPH      │   │  (Nhận diện)│
│             │   │ (Biểu diễn) │   │   MATCHING   │   │             │
└─────────────┘   └─────────────┘   └──────────────┘   └─────────────┘
   §2.1             §2.2             §2.3                §2.4
```

- 4 card pop in tuần tự bằng `LaggedStart(FadeIn(shift=UP*0.3))`, mỗi card cách nhau 0.4s.
- Khi từng card xuất hiện, mũi tên giữa chúng vẽ ra bằng `Create`.
- Card hiện tại được "spotlight" bằng `Flash` + glow `ACCENT_LAVENDER`.
- Sau khi đủ 4 card, một thanh tiến trình mảnh ở phía dưới: 4 ô — ô đầu tiên (Gabor) sáng lên, 3 ô còn lại mờ.

## 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–6s | "Vậy EBGM thực sự hoạt động như thế nào?" |
| 6s–12s | "Bốn bước, đi từ pixel thô đến danh tính người" |
| 12s–20s | "Bắt đầu với bước đầu tiên: trích xuất đặc trưng bằng Gabor Wavelets" |

## 🛠️ Manim techniques
`Text`, `Rectangle` (cho card), `Arrow`, `LaggedStart`, `Flash`, `Create`.

---

# 📽️ SCENE 9 — GABOR WAVELETS: KHÁI NIỆM CƠ BẢN (≈ 80s)

> **Reference Figure 1** trong paper: bức ảnh khuôn mặt gốc → Gabor wavelets (imaginary part và magnitude) → jet → image graph.

## 🎯 Mục đích
Giải thích Gabor wavelet là gì, công thức, vì sao chọn nó (DC-free, robust, gần với neuron thị giác).

## 🎨 Visual storyboard

### Phase A (0s–15s): Câu hỏi & motivation

- Tiêu đề scene fade in (top): **"Gabor Wavelets — Mắt của EBGM"** (section_title, lavender).
- Câu hỏi giữa màn hình: *"Làm sao trích xuất đặc trưng tại MỘT điểm ảnh?"*
- Một ảnh khuôn mặt (placeholder hoặc ImageMobject) xuất hiện bên trái. Một mũi tên cyan **chỉ vào MỘT điểm cụ thể** (ví dụ: đuôi mắt). Một `Circle` nhỏ highlight điểm đó, kèm chú thích: *"Điểm này nói lên điều gì?"*

### Phase B (15s–35s): Recreate Figure 1 — Convolution với Gabor kernels

Layout (theo đúng tinh thần Fig. 1 của paper):

```
┌──────────┬──────────────────────────────────┬──────┬──────────┐
│          │       CONVOLUTION RESULT         │      │          │
│ ORIGINAL │   ┌────────┬─────────┬─────────┐ │ JET  │  IMAGE   │
│  IMAGE   │   │ GABOR  │  IMAG.  │ MAGNI-  │ │      │  GRAPH   │
│          │   │WAVELETS│  PART   │  TUDE   │ │      │          │
│  [face]  │   │   ║║   │  ░▓░░   │  ▓▓▓▓▓  │ │[jet] │ [graph]  │
│          │   │   ╫╫   │  ░░▓░   │  ░▓▓▓░  │ │      │ on face  │
│          │   │   ║║   │  ▓░░░   │  ▓▓░░▓  │ │      │          │
│          │   └────────┴─────────┴─────────┘ │      │          │
└──────────┴──────────────────────────────────┴──────┴──────────┘
```

**Animation chi tiết:**

1. **(15s–20s)** Ảnh khuôn mặt giữ ở bên trái (scale ~0.4, ~1.5×2 đơn vị).
2. **(20s–25s)** Bên cạnh xuất hiện **3 Gabor kernels** xếp dọc (3 hướng khác nhau: ngang, dọc, chéo 45°). Mỗi kernel vẽ như "vạch sóng có envelope Gaussian":
   - Background của kernel: ô vuông xám đậm (`BG_NAVY_SOFT`).
   - Plot bằng `ImageMobject` hoặc tự generate bằng `Surface`/`heatmap` style: 
     ```python
     # Gabor kernel visualization (2D)
     def gabor_kernel_2d(orientation, freq=1.5, sigma=0.4, size=40):
         arr = np.zeros((size, size))
         for i in range(size):
             for j in range(size):
                 x = (i - size/2) / size * 2
                 y = (j - size/2) / size * 2
                 # rotate
                 xr = x*np.cos(orientation) + y*np.sin(orientation)
                 yr = -x*np.sin(orientation) + y*np.cos(orientation)
                 gauss = np.exp(-(xr**2 + yr**2) / (2*sigma**2))
                 wave = np.cos(2*PI*freq*xr)
                 arr[i,j] = gauss * wave
         return arr
     ```
     Sau đó dùng `ImageMobject` từ numpy array (chuẩn hóa về [0,255]).
   - Mỗi kernel kèm nhãn nhỏ: `μ=0`, `μ=2`, `μ=5`.

3. **(25s–32s)** **Convolution animation:** Mỗi kernel "trượt" qua ảnh khuôn mặt (sliding window). Dùng `MoveAlongPath` cho một `Square` highlight nhỏ di chuyển trên ảnh, đồng thời bên cạnh "vẽ ra dần" kết quả convolution (heatmap 2D):
   - **Imaginary part:** dạng plot có dấu (đỏ-xanh xen kẽ), nhiều dao động.
   - **Magnitude:** mờ và mượt hơn, các vùng sáng/tối liên tục.

4. **(32s–35s)** Toàn bộ panel đã render xong, hiện text bên dưới: 
   > *"Mỗi kernel = một plane wave bị giới hạn bởi envelope Gaussian"*

### Phase C (35s–55s): Công thức toán

Layout: bên trái là 1 Gabor kernel lớn được phóng to (visualization 3D-ish, có thể dùng `Surface` hoặc just 2D imshow). Bên phải là công thức:

$$\psi_j(\vec{x}) = \frac{k_j^2}{\sigma^2}\exp\!\left(-\frac{k_j^2 x^2}{2\sigma^2}\right)\left[\exp(i\vec{k}_j\vec{x}) - \exp\!\left(-\frac{\sigma^2}{2}\right)\right]$$

- Dùng `MathTex`, scale 0.75, màu `TEXT_PRIMARY`.
- Sau khi viết xong, từng phần được highlight (qua `SurroundingRectangle` cyan):
  - **Phần `exp(-k²x²/2σ²)`** → label: *"Envelope Gaussian"* (mũi tên chỉ vào hình bao của kernel)
  - **Phần `exp(i k·x)`** → label: *"Plane wave"*
  - **Phần `-exp(-σ²/2)`** → label: *"DC-free correction"* — kèm chú thích: *"⇒ Trơ lì với độ sáng nền"*.

- Thông số dùng:
  $$k_\nu = 2^{-\frac{\nu+2}{2}}\pi, \quad \varphi_\mu = \mu \frac{\pi}{8}, \quad \sigma = 2\pi$$
- Hiện ra trong khung nhỏ bên dưới: *"5 tần số × 8 hướng = 40 hệ số / điểm"*.

### Phase D (55s–80s): Vì sao Gabor?

Hiện 4 lý do (4 card mini, layout 2×2), mỗi card có icon:

| # | Lý do | Icon | Note |
|---|---|---|---|
| 1 | **DC-free** | ⚡ độ sáng | Tích phân kernel = 0 → không bị độ sáng nền làm lệch |
| 2 | **Robust** | 🛡️ | Trơ với dịch chuyển nhỏ, biến dạng, rotation |
| 3 | **Sinh học** | 🧠 | Giống receptive field của simple cells trong vỏ não thị giác |
| 4 | **Tự nhiên** | 📐 | Có thể derived từ thống kê ảnh tự nhiên |

- Mỗi card pop in qua `FadeIn(shift=UP*0.4)`, lag 0.4s.
- Icon được vẽ tay bằng VMobject thay vì emoji (vì font không có emoji).

## 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–6s | "Bước 1: Trích xuất đặc trưng bằng Gabor Wavelets" |
| 6s–12s | "Câu hỏi: làm sao mô tả 'cái gì' xảy ra tại MỘT điểm ảnh?" |
| 12s–20s | "Câu trả lời: convolve điểm đó với một bộ lọc đặc biệt" |
| 20s–28s | "Gabor wavelet — sóng phẳng bị giới hạn bởi envelope Gaussian" |
| 28s–36s | "Mỗi điểm được mô tả bởi 5 tần số × 8 hướng = 40 hệ số" |
| 36s–46s | "Thành phần DC-free giúp trơ lì với thay đổi độ sáng nền" |
| 46s–56s | "Envelope Gaussian khoanh vùng cục bộ, chống dịch chuyển nhỏ" |
| 56s–66s | "Gabor wavelet có hình dạng giống tế bào thần kinh thị giác" |
| 66s–80s | "Đây là lý do EBGM 'nhìn' giống cách bộ não chúng ta nhìn" |

## 🛠️ Manim techniques chính
`ImageMobject` (từ numpy array của Gabor kernel), `MathTex` (công thức), `SurroundingRectangle`, `MoveAlongPath` (cho convolution slide), `LaggedStart`.

---

# 📽️ SCENE 10 — JET: 40 HỆ SỐ PHỨC TẠI MỘT ĐIỂM (≈ 60s)

> **Reference Figure 1, panel "jet"** trong paper: hình chiếc jet được vẽ như "chồng đĩa stacked" (5 disks, mỗi disk có 8 phần).

## 🎯 Mục đích
Định nghĩa jet, visualize cấu trúc 5×8 = 40, giải thích phase và magnitude.

## 🎨 Visual storyboard

### Phase A (0s–10s): Định nghĩa jet

- Tiêu đề: **"Jet — 40 hệ số phức tại một điểm"** (lavender).
- Hiện công thức:
  $$\mathcal{J}_j = a_j \exp(i\phi_j), \quad j = \mu + 8\nu, \quad \nu=0..4, \mu=0..7$$
- Bên dưới: chú thích nhỏ — *"40 phép tích chập tại 1 điểm = 1 jet"*.

### Phase B (10s–35s): Visualize jet — Recreate Figure 1 "jet" panel

Dùng đúng motif **stacked disks** của paper:

```
            ┌─ ν=4 (highest freq)    [thin disk, 8 sectors]
            │
       ┌────┴─ ν=3
       │
   ┌───┴────── ν=2
   │
┌──┴───────── ν=1
│
└─────────── ν=0 (lowest freq)        [thick disk, 8 sectors]
```

**Cách vẽ:**

1. **(10s–15s)** Từ một điểm (Dot lavender) trên khuôn mặt, một mũi tên chỉ "phóng to ra" thành cấu trúc jet (effect zoom-in).

2. **(15s–25s)** Vẽ 5 disks chồng lên nhau, với perspective 3D nhẹ (rotate `(60°, 0, 0)` để tạo depth):
   ```python
   jets_disks = VGroup()
   for nu in range(5):
       disk = VGroup()
       # 8 sectors
       for mu in range(8):
           sector = AnnularSector(
               inner_radius=0.4 + nu*0.05,
               outer_radius=0.8 + nu*0.05,
               start_angle=mu * PI/4,
               angle=PI/4,
               color=interpolate_color(GABOR_REAL, GABOR_IMAG, mu/7),
               fill_opacity=0.6
           )
           disk.add(sector)
       disk.shift(UP * nu * 0.3)  # stack lên trên
       jets_disks.add(disk)
   jets_disks.rotate(PI/6, axis=RIGHT)  # tilt perspective
   ```
3. **(25s–30s)** Mỗi disk được label `ν=0`, `ν=1`, ..., `ν=4` ở bên phải. Mỗi sector trong cùng 1 disk có hue khác nhau (gradient cyan→lavender) → biểu thị 8 hướng `μ=0..7`.
4. **(30s–35s)** Một sector ở disk thấp nhất nhấp nháy + zoom in (Indicate), kèm label: `j = 0 + 8·0 = 0` (μ=0, ν=0).

### Phase C (35s–55s): Phase vs Magnitude — 2 components

Layout chia đôi:

**Bên trái: Magnitude a_j**
- Plot biểu đồ trục thời gian / dịch chuyển ngang:
  - Y axis: giá trị magnitude (0 → 1)
  - X axis: dịch chuyển ngang (pixel)
  - Curve: trơn, slow-varying — dạng "đồi mịn" — màu `ACCENT_MINT`
- Label: *"Magnitude — biến đổi CHẬM"*
- Chú thích: *"⇒ Robust, dùng để tìm thô"*

**Bên phải: Phase φ_j**
- Plot tương tự:
  - Curve: nhanh, dao động sin tần số cao — màu `ACCENT_LAVENDER`
- Label: *"Phase — biến đổi NHANH"*
- Chú thích: *"⇒ Chính xác, dùng để tìm tinh (subpixel)"*

(Dùng `Axes` + `plot` của Manim cho 2 biểu đồ này.)

### Phase D (55s–60s): Chốt

- Magnitude và Phase merge lại thành biểu thức `J_j = a_j · exp(i·φ_j)` ở giữa.
- Câu chốt: *"Mỗi điểm ảnh = 1 jet = 40 con số phức, đủ để mô tả 'cái gì xảy ra ở đây'."*

## 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–6s | "Một jet là gì?" |
| 6s–14s | "Jet = bộ 40 hệ số phức tại MỘT điểm ảnh" |
| 14s–22s | "Cấu trúc: 5 tần số × 8 hướng, xếp như 5 chiếc đĩa chồng lên nhau" |
| 22s–30s | "Mỗi sector trong đĩa = 1 hướng cụ thể" |
| 30s–38s | "Mỗi hệ số phức tách thành hai phần: magnitude và phase" |
| 38s–46s | "Magnitude biến đổi chậm theo không gian — dùng để tìm thô" |
| 46s–54s | "Phase biến đổi nhanh — dùng để định vị chính xác đến subpixel" |
| 54s–60s | "40 con số — đủ để mô tả 'cái gì xảy ra tại điểm này'" |

## 🛠️ Manim techniques chính
`AnnularSector`, `VGroup`, `rotate(axis=RIGHT)` cho 3D-ish, `Axes` + `plot`, `MathTex`.

---

# 📽️ SCENE 11 — SO SÁNH JET: HAI HÀM SIMILARITY (≈ 75s)

> **Reference Figure 2** trong paper: plot của Sa (không pha), Sφ (có pha), và estimated displacement / 8.

## 🎯 Mục đích
Giải thích 2 hàm similarity, vì sao cần cả 2, và cách Sφ ước lượng displacement.

## 🎨 Visual storyboard

### Phase A (0s–15s): Đặt vấn đề

- Tiêu đề: **"Làm sao so sánh hai jet?"**
- Hiện 2 jets (đại diện bằng 2 mini stacked-disks) — gọi là `J` và `J'`. Khoảng cách giữa chúng có thể là 0, vài pixel, hay rất xa.
- Câu hỏi: *"Chúng có giống nhau không? Cách nhau bao xa?"*

### Phase B (15s–35s): Hàm similarity KHÔNG dùng phase — S_a

Layout chia đôi.

**Bên trái:** Công thức:
$$\mathcal{S}_a(\mathcal{J}, \mathcal{J}') = \frac{\sum_j a_j a'_j}{\sqrt{\sum_j a_j^2 \sum_j a'_j^2}}$$

- Highlight: chỉ dùng magnitude `a_j`, KHÔNG có phase.

**Bên phải:** Recreate **Fig 2(a)** — Plot Sa vs horizontal displacement:
- `Axes`: x ∈ [-50, 50] pixels, y ∈ [-1, 1]
- Curve dạng "đường cong dài, mượt như đồi" — màu `ACCENT_CYAN`, có 1 đỉnh lớn ở x=0 (mượt, đáy rộng).
- Highlight vùng đỉnh: rectangle nhạt + label *"Large attractor basin"* (basin hút lớn).
- Chú thích: *"⇒ Dễ hội tụ, dùng cho tìm thô ban đầu"*

### Phase C (35s–55s): Hàm similarity DÙNG phase — S_φ

Bên trái fade ra, hiện công thức mới:
$$\mathcal{S}_\phi(\mathcal{J}, \mathcal{J}') = \frac{\sum_j a_j a'_j \cos(\phi_j - \phi'_j - \vec{d}\cdot\vec{k}_j)}{\sqrt{\sum_j a_j^2 \sum_j a'_j^2}}$$

- Highlight: thêm phần `cos(φ_j - φ'_j - d·k_j)` — màu `ACCENT_LAVENDER`.
- Note: `d` là vector dịch chuyển cần ước lượng.

Bên phải:
- **Plot Sφ** (replicate Fig 2b): curve có **NHIỀU đỉnh nhọn** (oscillate mạnh), đỉnh chính ở x=0 vẫn rất nhọn, các đỉnh phụ ở các vị trí khác. Màu `ACCENT_LAVENDER`.
- Note ở đỉnh phụ tại x ≈ -24: *"Mắt còn lại — đỉnh giả!"* (vì 2 mắt cách nhau ~24 pixel).
- Chú thích: *"⇒ Chính xác cao, nhưng nhiều cực trị địa phương → cần khởi tạo gần đúng"*

### Phase D (55s–70s): Ước lượng displacement — Estimated d

Hiện công thức (compact):
$$\vec{d}(\mathcal{J}, \mathcal{J}') = \frac{1}{\Gamma_{xx}\Gamma_{yy} - \Gamma_{xy}\Gamma_{yx}}\begin{pmatrix}\Gamma_{yy} & -\Gamma_{yx}\\ -\Gamma_{xy} & \Gamma_{xx}\end{pmatrix}\begin{pmatrix}\Phi_x \\ \Phi_y\end{pmatrix}$$

- Comment ngắn (chỉ chỉ tay vào): "Maximize Sφ qua khai triển Taylor → giải tuyến tính cho d"

Recreate **Fig 2(c)**: estimated displacement curve
- Dạng sawtooth (răng cưa): đúng & dốc ở quanh x=0 (slope = -1, scale by 1/8), nhảy bậc ở các đỉnh phụ.
- Vẽ đường dotted ở y=0 và mũi tên chú thích: *"Quanh 0: ước lượng chính xác đến subpixel"*

### Phase E (70s–75s): Trade-off summary

Bảng 2 cột nhỏ:

| `S_a` (no phase) | `S_φ` (with phase) |
|---|---|
| Mượt, basin lớn | Nhọn, nhiều cực trị |
| ✓ Tìm thô | ✓ Tìm tinh |
| Init position | Refine subpixel |

→ Câu chốt: *"EBGM dùng cả hai — coarse-to-fine."*

## 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–8s | "Hai jet — chúng giống nhau không? Cách nhau bao xa?" |
| 8s–16s | "Cách 1: chỉ so sánh magnitude — bỏ qua phase" |
| 16s–24s | "Đường cong mượt, có vùng thu hút lớn — dễ hội tụ" |
| 24s–32s | "Phù hợp cho bước tìm thô vị trí ban đầu" |
| 32s–42s | "Cách 2: so sánh có dùng phase — chính xác hơn nhiều" |
| 42s–50s | "Đường cong nhiều đỉnh — nhưng đỉnh chính rất nhọn" |
| 50s–58s | "Phase còn cho phép ước lượng độ dịch chuyển d" |
| 58s–66s | "Quanh vị trí đúng, ước lượng chính xác đến subpixel" |
| 66s–75s | "EBGM kết hợp cả hai: thô trước, tinh sau" |

## 🛠️ Manim techniques chính
`Axes`, `plot` với hàm tùy chỉnh (giả lập Sa và Sφ curves), `SurroundingRectangle`, `MathTex` cho ma trận.

---

# 📽️ SCENE 12 — FACE REPRESENTATION: INDIVIDUAL GRAPH (≈ 65s)

## 🎯 Mục đích
Định nghĩa "image graph" / "model graph" — đồ thị biểu diễn một khuôn mặt: nodes ở fiducial points, edges với label khoảng cách.

## 🎨 Visual storyboard

### Phase A (0s–10s): Câu hỏi mở

- Tiêu đề: **"Biểu diễn một khuôn mặt = một đồ thị có nhãn"**
- Câu hỏi: *"Nhưng làm sao TỔ CHỨC 40 hệ số × nhiều điểm thành một biểu diễn mạch lạc?"*

### Phase B (10s–35s): Xây dựng graph từng bước

Bắt đầu với 1 bức ảnh khuôn mặt (placeholder), sau đó:

1. **(10s–18s)** Lần lượt "đặt" các fiducial points lên ảnh:
   - Pupil trái → `Dot` lavender + label "L. pupil"
   - Pupil phải → label "R. pupil"
   - Tip of nose, mouth corners (L/R), chin tip, ear top/bottom, forehead, cheeks...
   - Tổng ~16–20 nodes, xuất hiện lần lượt qua `LaggedStart(GrowFromCenter)`.

2. **(18s–25s)** Vẽ các **cạnh** nối các nodes — màu `GRID_LINE`, stroke_width=1.2. Vẽ qua `Create`.
   - Nhấn mạnh đây là "geometric structure".

3. **(25s–30s)** **Highlight 1 node:** Một node (vd: pupil trái) được phóng to lên → cạnh nó hiện ra 1 jet visualization nhỏ (mini stacked disk).
   - Chú thích bằng `MathTex`: $\mathcal{J}_n$ — *"jet tại node n"*

4. **(30s–35s)** **Highlight 1 edge:** Một cạnh được làm dày lên, hiện vector chú thích:
   - $\Delta\vec{x}_e = \vec{x}_n - \vec{x}_{n'}$
   - Một mũi tên đỏ vẽ thực sự vector này trên ảnh (từ node `n'` đến node `n`).

### Phase C (35s–55s): Tổng kết cấu trúc dữ liệu

Hiện một schema bên cạnh ảnh (như infographic):

```
GRAPH G = (V, E)
│
├─ V = {nodes} (N điểm)
│   └─ Each node n: label = Jet J_n   [40 complex coefs]
│
└─ E = {edges}
    └─ Each edge e: label = Δx_e = x_n - x_n'  [2D vector]
```

Dùng `Tree` hoặc `VGroup` xếp theo cây. Mỗi dòng fade in tuần tự.

Chú thích phía dưới: *"Khi graph adapt theo các fiducial points → 'object-adapted graph'"*

### Phase D (55s–65s): Pose-specific graphs

- Hiện 3 graph nhỏ song song: **frontal**, **half-profile**, **profile**.
- Cấu trúc khác nhau ở từng pose (số nodes, vị trí).
- Mũi tên kết nối các nodes "tương ứng" giữa các pose (vd: tip of nose → tip of nose) — dotted lines lavender.
- Chú thích: *"Mỗi pose có một graph riêng. Designer-provided correspondences giữa các pose."*

## 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–6s | "Bước 2: Biểu diễn khuôn mặt bằng một đồ thị" |
| 6s–14s | "Các nút đặt ở những điểm mốc đặc trưng — mắt, mũi, miệng" |
| 14s–22s | "Mỗi nút được gán một jet — 40 hệ số mô tả cục bộ" |
| 22s–32s | "Các cạnh nối các nút, mang nhãn là vector khoảng cách giữa chúng" |
| 32s–42s | "Đây là cấu trúc 'object-adapted graph'" |
| 42s–50s | "Tóm tắt: V = các điểm mốc, E = các kết nối hình học" |
| 50s–58s | "Mỗi tư thế đầu (frontal, nghiêng, profile) có graph riêng" |
| 58s–65s | "Tương ứng giữa các pose được người thiết kế chỉ định" |

## 🛠️ Manim techniques chính
`Dot`, `Line` (cho edges), `GrowFromCenter`, `LaggedStart`, `MathTex`, `Tree` (hoặc `VGroup`).

---

# 📽️ SCENE 13 — FACE BUNCH GRAPH (FBG) (≈ 70s)

> **Reference Figure 3** trong paper: hình "stacked face graphs" với chú thích "face bunch graph", các nodes có "bunches of jets", một số jet được highlight bằng grey shading (= "best fitting").

## 🎯 Mục đích
Giải thích Bunch Graph — sao chồng 70 graphs cho phép tổ hợp đa dạng.

## 🎨 Visual storyboard

### Phase A (0s–12s): Câu hỏi & motivation

- Tiêu đề: **"Face Bunch Graph — Trí tuệ tổ hợp"** (lavender).
- Câu hỏi: *"Làm sao 1 graph biểu diễn được... mọi loại mắt, mọi loại mũi?"*
- Hint: 1 graph mẫu fade ra, kèm chữ "❌ chưa đủ".

### Phase B (12s–35s): Build FBG by stacking — Recreate Figure 3

Đây là **scene quan trọng nhất** của phần 2 — recreate Figure 3 của paper.

**Animation steps:**

1. **(12s–18s)** Hiện 1 graph (graph G^{B_1}), nodes cách đều, jet visualization (mini stacked disks) ở mỗi node. Màu `ACCENT_BLUE`.

2. **(18s–28s)** **Stack thêm các graph bên trên** (theo perspective 3D): G^{B_2}, G^{B_3}, ..., (visualize 5–6 layers, label "M=70 models" ở góc).
   - Dùng `rotate(axis=RIGHT, angle=PI/6)` để có perspective.
   - Mỗi layer shift up nhẹ (UP*0.4).
   - Các layers semi-transparent, để có thể thấy stack.
   - Code skeleton:
     ```python
     fbg = VGroup()
     for m in range(6):
         single_graph = make_face_graph()  # function tự định nghĩa
         single_graph.set_opacity(0.6)
         single_graph.shift(UP * m * 0.35 + RIGHT * m * 0.05)
         fbg.add(single_graph)
     fbg.rotate(PI/6, axis=RIGHT)
     ```

3. **(28s–32s)** Edges nối các nodes — averaged distance (paper: $\Delta\vec{x}_e^B = \sum_m \Delta\vec{x}_e^{B_m}/M$).
   - Edges chỉ vẽ giữa các "trung điểm" (average positions) — màu `ACCENT_LAVENDER` đậm.

4. **(32s–35s)** Chú thích bên dưới: **"Face Bunch Graph (FBG)"**, font EB Garamond, scale 0.7, lavender.

### Phase C (35s–55s): Khái niệm "Bunch" tại 1 node

Zoom vào MỘT node (ví dụ: node mắt trái).

- Camera focus zoom vào, các node khác mờ đi.
- Tại node này, hiện ra **một stack ngang** gồm ~6 mini-jets (mỗi jet đại diện cho 1 model graph khác nhau).
- Bên cạnh mỗi mini-jet, label nhỏ italic: "mắt nam", "mắt nữ", "mắt nhắm", "mắt mở", "mắt đeo kính", "mắt có nếp gấp"...
- Câu chú thích: *"Tại MỖI node, ta có một 'bunch' — chùm các jets từ các khuôn mặt mẫu khác nhau."*

**Highlight "best fitting jet":** Sau 3s, một trong các mini-jet được spotlight bằng glow `HIGHLIGHT_HOT` + `Indicate`. Label: *"Local expert — chuyên gia cục bộ"*.

### Phase D (55s–70s): Tính tổ hợp (Combinatorial Power)

- Zoom out trở lại FBG đầy đủ.
- Tại nhiều nodes khác nhau, từng "best jet" tự động được pick ra từ bunch (hiện 1 vài node với grey shading style như paper).
- Câu chú thích chốt:
  > *"Mỗi node tự CHỌN jet phù hợp nhất → FBG tổ hợp ra **vô số khuôn mặt mới**, dù chỉ có 70 mẫu gốc."*
- Hiện một con số lớn: $6^{16} \approx 2.8 \times 10^{12}$ tổ hợp khả thi (với ~16 nodes và ~6 jet/bunch).

## 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–6s | "Một graph mẫu không thể đại diện cho mọi khuôn mặt" |
| 6s–14s | "Giải pháp: chồng ~70 graphs lên thành một thực thể chung" |
| 14s–22s | "Đó là Face Bunch Graph — FBG" |
| 22s–30s | "Tất cả có cùng cấu trúc, các nodes ở cùng vị trí mốc" |
| 30s–38s | "Tại mỗi node: không phải 1 jet, mà là một CHÙM jets" |
| 38s–46s | "Mỗi jet trong chùm đến từ một khuôn mặt mẫu khác nhau" |
| 46s–54s | "Khi quét ảnh mới, mỗi node tự CHỌN jet phù hợp nhất" |
| 54s–62s | "Jet được chọn được gọi là 'local expert' — chuyên gia cục bộ" |
| 62s–70s | "FBG tổ hợp ra vô số khuôn mặt mới — sức mạnh từ tính tổ hợp" |

## 🛠️ Manim techniques chính
`VGroup` stacking với `rotate(axis=RIGHT)`, `set_opacity`, `Indicate`, `Flash`, `MoveToTarget`, camera zoom.

---

# 📽️ SCENE 14 — GRAPH SIMILARITY FUNCTION (≈ 55s)

## 🎯 Mục đích
Trình bày công thức similarity giữa image graph và FBG — cốt lõi của matching.

## 🎨 Visual storyboard

### Phase A (0s–10s): Setup

- Tiêu đề: **"Hàm tương đồng đồ thị"**.
- Bên trái: một **image graph** (G^I) đang được khớp lên ảnh khuôn mặt.
- Bên phải: **FBG** (B) — stack of graphs.
- Mũi tên ở giữa: *"So sánh thế nào?"*

### Phase B (10s–30s): Công thức từng phần

Hiện công thức ở giữa màn hình:

$$\mathcal{S}_B(\mathcal{G}^I, \mathcal{B}) = \underbrace{\frac{1}{N}\sum_n \max_m\left(\mathcal{S}_\phi(\mathcal{J}_n^I, \mathcal{J}_n^{B_m})\right)}_{\text{Jet similarity}} - \underbrace{\frac{\lambda}{E}\sum_e \frac{(\Delta\vec{x}_e^I - \Delta\vec{x}_e^B)^2}{(\Delta\vec{x}_e^B)^2}}_{\text{Distortion penalty}}$$

**Animation từng phần:**

1. **(10s–18s)** Phần Jet similarity được vẽ ra trước. Highlight `max_m`: 
   - Trên FBG hiện ra animation: tại mỗi node, "quay" qua các jets trong bunch, dừng ở jet có score cao nhất.
   - Label: *"Chọn 'local expert' tại mỗi node"*.

2. **(18s–25s)** Phần Distortion penalty được vẽ ra sau (màu coral, vì là penalty).
   - Hiện minh họa: 2 edges, một edge "đúng" (giữ nguyên), một edge "bị méo" (kéo dài 1.5×) → penalty tăng.
   - Visualize: dùng `Line` với stroke_width khác nhau, kèm `MathTex` cho phần khoảng cách.

3. **(25s–30s)** Tham số `λ` được giải thích: *"Trade-off — feature similarity vs cấu trúc hình học"*.

### Phase C (30s–55s): Visualize objective

Layout cuối: graph đang được "kéo dãn" qua nhiều configurations:
- Config 1: méo nhiều → jet match cao nhưng penalty cao → score thấp
- Config 2: cứng (không méo) → penalty 0 nhưng jet match thấp → score thấp
- Config 3: cân bằng → score cao nhất ✓

Mỗi config hiện ra trong ~6s, có chú thích & gauge score (cyan bar) bên cạnh.

Câu chốt: *"Tối đa hóa = vừa khớp đặc trưng, vừa giữ cấu trúc"*

## 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–6s | "Làm sao đo lường: image graph khớp với FBG đến đâu?" |
| 6s–14s | "Công thức gồm hai phần đối lập nhau" |
| 14s–22s | "Phần thứ nhất: trung bình độ tương đồng jet — chọn expert tốt nhất" |
| 22s–30s | "Phần thứ hai: hình phạt cho biến dạng cấu trúc" |
| 30s–38s | "Quá méo? Score giảm. Quá cứng? Cũng không khớp đặc trưng" |
| 38s–46s | "Tham số λ điều chỉnh sự cân bằng giữa hai phần" |
| 46s–55s | "Tối đa hóa hàm này = tìm đồ thị khớp ảnh nhất" |

## 🛠️ Manim techniques chính
`MathTex` với `\underbrace`, `SurroundingRectangle`, `Transform` cho graph configurations, custom gauge bar.

---

# 📽️ SCENE 15 — MATCHING PROCEDURE: 4 BƯỚC (≈ 110s)

> **Reference Figure 4** trong paper: object-adapted grids — bên trái là grids cho face finding (outline-heavy), bên phải là grids cho face recognition (interior-heavy).

## 🎯 Mục đích
Trình bày 4 bước matching coarse-to-fine — đây là **trái tim** của EBGM.

## 🎨 Visual storyboard

### Phase A (0s–15s): Setup và roadmap

- Tiêu đề: **"Elastic Bunch Graph Matching — Bốn bước"** (lavender).
- Hiện một thanh tiến trình ngang 4 ô bên dưới:
  ```
  [1. Approximate pos]  [2. Position + Size]  [3. Aspect ratio]  [4. Local distortion]
       Rigid model           Phase focus 1        Focus 1→5         Per-node
  ```
- Một probe image (khuôn mặt mới chưa biết) hiện ở bên trái — graph chưa có.
- Câu hỏi: *"FBG → ảnh mới. Đặt graph ở đâu? Đặt thế nào?"*

### Phase B — STEP 1 (15s–35s): Approximate Position

**Visual:**
1. **(15s–20s)** FBG ở góc trên phải. Animation: FBG **co lại** (Transform) thành 1 graph trung bình (rigid model), bằng cách "average magnitudes of jets in each bunch".
2. **(20s–32s)** Rigid model được **trượt** trên ảnh theo lưới 4×4 pixel (scan grid 4 pixels). 
   - Highlight visualization: một `Square` đại diện cho rigid model di chuyển qua các vị trí (LaggedStart of Transform).
   - Tại mỗi vị trí, hiện score (mini bar, cyan) ở bên cạnh.
   - Score cao nhất → vị trí highlight bằng `Flash`.
3. **(32s–35s)** Refine: spacing giảm xuống 1 pixel quanh vị trí tốt nhất → fine tune.

**Note bên dưới:** *"Step 1: λ=∞ (no flex), dùng S_a (no phase)"*

### Phase C — STEP 2 (35s–55s): Position + Size

**Visual:**
1. **(35s–40s)** Vị trí tốt nhất từ Step 1 được giữ. Bây giờ FBG đầy đủ (không trung bình nữa) được thử ở **8 cấu hình**:
   - 4 displacements: `(±3, ±3)` pixels
   - 2 sizes: 1× và 1.18× (lớn) hoặc 1/1.18× (nhỏ)
   - = 4 × 2 = 8 configs
2. **(40s–50s)** Visualize 8 configs cùng lúc trên grid 2×4 mini panels. Cấu hình tốt nhất được highlight.
3. **(50s–55s)** Sau khi chọn config tốt, **mỗi node** được cho phép displacement nhỏ (focus 1, up to 8 pixels) → grid được "kéo dãn" nhẹ. Rồi rescale & reposition để minimize sum of displacements.

**Note:** *"Step 2: λ=∞, BẮT ĐẦU dùng phase (S_φ), focus 1 (low freq only)"*

### Phase D — STEP 3 (55s–75s): Aspect Ratio

**Visual:**
1. Tương tự Step 2, nhưng **x-axis và y-axis được scale ĐỘC LẬP**:
   - 4 configs: (1.0, 1.0), (1.18, 1.0), (1.0, 1.18), (1.18, 1.18)
   - Visualize bằng grids "stretched" theo x hoặc y.
2. Focus tăng dần từ 1 → 2 → 3 → 4 → 5.
   - Visualize focus như "kính phóng đại" càng lúc càng zoom vào (radius indicator giảm dần).
   - Mỗi step focus, các nodes "nhúc nhích" nhẹ đến vị trí chính xác hơn.

**Note:** *"Step 3: focus 1→5, x/y scale độc lập"*

### Phase E — STEP 4 (75s–100s): Local Distortion

Đây là phần thú vị nhất — graph "thực sự" trở nên **đàn hồi**.

**Visual:**
1. **(75s–82s)** Từng node được di chuyển độc lập theo thứ tự ngẫu nhiên (pseudo-random sequence).
   - Hiện mũi tên nhỏ ở mỗi node — chiều di chuyển.
   - Mỗi lần 1 node di chuyển, các edges nối nó bị stretched/compressed.
2. **(82s–92s)** **Quan trọng:** Bây giờ `λ=2` (không còn ∞), nên distortion gây penalty. Hiện gauge bar bên cạnh:
   - Khi node di chuyển vừa phải → score tăng (cyan bar lên)
   - Khi node di chuyển quá → penalty tăng (coral bar lên), score giảm.
3. **(92s–100s)** Chỉ những displacements `d < 1` được chấp nhận. Focus lại tăng 1→5.

**Note:** *"Step 4: λ=2, focus 1→5, per-node displacement"*

### Phase F (100s–110s): Kết quả

- Cuối cùng: graph đã "khớp" hoàn hảo vào ảnh khuôn mặt — recreate visual đẹp như **Figure 4** của paper (object-adapted grid trên face).
- Show 2–3 examples nhỏ (như Fig. 4): face finding grid (outline-heavy) vs face recognition grid (interior-heavy).
- Câu chốt: *"Đây là 'Image Graph' — biểu diễn cuối cùng cho khuôn mặt này."*

## 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–8s | "Bốn bước, từ thô đến tinh" |
| 8s–18s | "Bước 1: Tìm vị trí xấp xỉ — quét toàn ảnh bằng mô hình cứng" |
| 18s–28s | "Mô hình cứng = trung bình hóa FBG, λ vô hạn, chưa dùng phase" |
| 28s–38s | "Bước 2: Tinh chỉnh vị trí và kích thước" |
| 38s–48s | "Thử 8 cấu hình: 4 dịch chuyển × 2 kích thước" |
| 48s–58s | "Bắt đầu dùng phase ở tần số thấp — focus 1" |
| 58s–66s | "Bước 3: Điều chỉnh tỷ lệ khung hình x và y độc lập" |
| 66s–74s | "Focus tăng dần từ 1 lên 5 — chính xác đến subpixel" |
| 74s–84s | "Bước 4: Biến dạng cục bộ — từng node tự do xê dịch" |
| 84s–94s | "Lúc này λ=2 — có hình phạt nếu cấu trúc bị méo" |
| 94s–104s | "Chỉ chấp nhận dịch chuyển nhỏ, focus lại tăng từ 1 lên 5" |
| 104s–110s | "Kết quả: Image Graph khớp hoàn hảo lên khuôn mặt" |

## 🛠️ Manim techniques chính
`Transform` (lots of), `MoveAlongPath`, grid scanning với `LaggedStart`, custom gauge bars (`Rectangle` với `width=ValueTracker`), `Flash`.

---

# 📽️ SCENE 16 — TWO-STAGE SCHEDULE (≈ 50s)

## 🎯 Mục đích
Giải thích lộ trình 2 giai đoạn: normalization stage (face finding) và recognition stage.

## 🎨 Visual storyboard

### Phase A (0s–10s): Setup

- Tiêu đề: **"Hai giai đoạn: Chuẩn hóa & Trích xuất"**.
- Hiện sơ đồ flowchart:
  ```
  [Original Image]
        │
        ▼
  ┌─────────────────────┐
  │ Stage 1:            │
  │ NORMALIZATION       │
  │ (FBG nhẹ, outline)  │
  └────────┬────────────┘
        │
        ▼
  [Cropped & Resized 128×128]
        │
        ▼
  ┌─────────────────────┐
  │ Stage 2:            │
  │ RECOGNITION         │
  │ (FBG dày, interior) │
  └────────┬────────────┘
        │
        ▼
  [Image Graph]
  ```

### Phase B (10s–30s): Stage 1 — Normalization

- Hiện 1 ảnh gốc (256×384 paper-style) — face có thể to nhỏ vị trí khác nhau.
- FBG dùng ở đây: **30 models, outline-heavy** (recreate left side of Fig. 4).
- Animation: graph được khớp → bounding box xuất hiện → "cut & resize" effect → ảnh được crop và scale về 128×128.
- Note bên cạnh: 
  - "M=30 models"
  - "Nodes tập trung ở viền mặt"
  - "Mục tiêu: tìm + crop, không cần chính xác từng điểm"
  - "~99% accuracy, ~20s/image trên SPARCstation 10-512"

### Phase C (30s–50s): Stage 2 — Recognition

- Hiện ảnh 128×128 đã chuẩn hóa.
- FBG dùng ở đây: **70 models, interior-heavy** (recreate right side of Fig. 4).
- Animation: matching procedure 4 bước (rút gọn) → image graph cuối cùng (nhiều nodes trong khuôn mặt).
- Note bên cạnh:
  - "M=70 models"
  - "Nodes tập trung ở giữa mặt"
  - "Mục tiêu: trích xuất feature chi tiết"
  - "~10s/image"

## 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–6s | "Trong thực tế, matching chạy hai lần" |
| 6s–14s | "Giai đoạn 1: Chuẩn hóa — FBG thưa, tập trung viền mặt" |
| 14s–22s | "Mục tiêu: tìm khuôn mặt, crop, resize về 128×128 pixel" |
| 22s–30s | "Khoảng 30 models là đủ, độ chính xác ~99%" |
| 30s–38s | "Giai đoạn 2: Nhận diện — FBG dày, tập trung giữa mặt" |
| 38s–46s | "Khoảng 70 models, trích xuất feature chi tiết để phân biệt cá nhân" |
| 46s–50s | "Đầu ra: Image Graph cuối cùng — sẵn sàng cho nhận diện" |

## 🛠️ Manim techniques chính
`Arrow`, sequential `Transform`, `ImageMobject` resize animation, side-by-side comparison.

---

# 📽️ SCENE 17 — RECOGNITION: SO SÁNH & XẾP HẠNG (≈ 60s)

## 🎯 Mục đích
Bước cuối: so sánh image graph với gallery, xếp hạng, trả về danh tính.

## 🎨 Visual storyboard

### Phase A (0s–12s): Setup

- Tiêu đề: **"Nhận diện — Hạng 1 chiến thắng"** (lavender).
- Hiện image graph của **probe image** (ảnh cần nhận diện) ở bên trái.
- Bên phải: **gallery** — một grid 5×5 = 25 model graphs (đại diện cho 250 người, paper test FERET với 250 models).
- Mũi tên từ probe → gallery: *"So sánh probe với từng model"*.

### Phase B (12s–35s): Công thức & process

Hiện công thức:
$$\mathcal{S}_G(\mathcal{G}^I, \mathcal{G}^M) = \frac{1}{N'}\sum_{n'} \mathcal{S}_a(\mathcal{J}_{n'}^I, \mathcal{J}_{n_{n'}}^M)$$

- Nhấn mạnh: 
  - $\mathcal{S}_a$ — KHÔNG dùng phase! 
  - Lý do (highlight box): *"Không-phase robust hơn với thay đổi biểu cảm"*
- Animation: probe graph trượt qua từng model trong gallery (LaggedStart), mỗi lần so sánh hiện ra 1 score bên cạnh:
  - Model 1: 0.42
  - Model 2: 0.38
  - Model 3: 0.91 ← cao nhất
  - ...

### Phase C (35s–50s): Ranking visualization

- Sau khi tính xong, tất cả scores được **sort xuống** thành bảng xếp hạng:
  ```
  Rank 1: ████████████ 0.91  [Person ID: 042]  ← MATCH ✓
  Rank 2: █████████    0.74
  Rank 3: ████████     0.69
  Rank 4: ███████      0.61
  ...
  Rank 250: █          0.12
  ```
- Top-1 được highlight bằng box `ACCENT_MINT` + checkmark.
- Phía bên cạnh: 
  - Mặt trên cùng (rank 1) = probe person? → **YES** → recognition CORRECT.
  - Hoặc → **NO** → recognition INCORRECT (color coral).

### Phase D (50s–60s): Kết quả & speed

- Câu chốt: *"So sánh với 250 models chỉ mất < 1 giây."*
- Hiện một số liệu nhỏ: 
  - "FERET 250 fa vs 250 fb: **98% rank-1 accuracy**"
  - "Bochum 108 frontal: **91%**"

## 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–8s | "Cuối cùng: image graph được so sánh với cả gallery" |
| 8s–16s | "Mỗi cặp jet tương ứng cho ra một độ tương đồng" |
| 16s–24s | "Lưu ý: ở đây dùng hàm KHÔNG-phase" |
| 24s–32s | "Vì không-phase robust hơn với thay đổi biểu cảm" |
| 32s–40s | "Trung bình cộng các điểm jet = điểm tương đồng đồ thị" |
| 40s–48s | "Xếp hạng tất cả gallery — model điểm cao nhất là rank 1" |
| 48s–56s | "Nếu rank 1 đúng người → nhận diện thành công" |
| 56s–60s | "Một probe vs 250 models — chỉ chưa đầy 1 giây" |

## 🛠️ Manim techniques chính
`LaggedStart`, sort animation (`Transform` rearrange), `Rectangle` cho bar chart ranking, `MathTex`.

---

# 📽️ SCENE 18 — TỔNG KẾT PHẦN 2 (≈ 25s)

## 🎯 Mục đích
Tóm lại pipeline đầy đủ trong 1 frame, dẫn vào Experiments.

## 🎨 Visual storyboard

### Phase A (0s–15s): Recap pipeline

Hiện lại sơ đồ 4 ô như Scene 8, nhưng giờ mỗi ô đã được **fill** với 1 thumbnail thu nhỏ của những gì đã giải thích:

```
┌─────────────┐   ┌─────────────┐   ┌──────────────┐   ┌─────────────┐
│  1. GABOR   │──▶│  2. FACE    │──▶│  3. ELASTIC  │──▶│  4. RECOG-  │
│             │   │   GRAPH     │   │     BUNCH    │   │    NITION   │
│ [jet icon]  │   │ [graph on   │   │  [stacked    │   │ [ranking    │
│             │   │   face]     │   │   FBG]       │   │   list]     │
└─────────────┘   └─────────────┘   └──────────────┘   └─────────────┘
```

- Mỗi ô lần lượt lóe sáng (`Flash` + glow) khi nhắc đến trong subtitle.

### Phase B (15s–25s): Teaser cho phần tiếp

- Hiện text:
  > **"Tiếp theo: Experiments — EBGM hoạt động tốt đến đâu?"**
- Bên dưới: 3 keyword chạy ngang:
  - `FERET` (250 faces)
  - `Bochum Database`
  - `Cross-pose recognition`
- Arrow `→` lavender chỉ sang phải, `Flash`.

## 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–8s | "Đó là toàn bộ EBGM: Gabor → Graph → Bunch → Recognition" |
| 8s–16s | "Từ pixel thô đến danh tính người — chỉ trong vài chục giây" |
| 16s–25s | "Tiếp theo: Đánh giá EBGM trên các bộ dữ liệu thực tế" |

## 🛠️ Manim techniques chính
`Flash`, recap composition, `FadeIn(shift)`.

---

## ✅ CHECKLIST CHO PHẦN 2

- [ ] Tất cả công thức LaTeX đã test render được không lỗi.
- [ ] Gabor kernel visualization (Scene 9) đã pre-generate hoặc compute on-the-fly.
- [ ] Hàm `make_jet_visual()` và `make_face_graph_node()` đã được test riêng.
- [ ] Asset cần chuẩn bị:
  - [ ] Face image ít nhất 3 ảnh (frontal, half-profile, profile) cho Scene 12, 13, 15.
  - [ ] (Tùy chọn) Pre-rendered convolution result heatmaps cho Scene 9.
- [ ] Pacing: Scene 15 dài nhất (~110s) — cân nhắc cắt nhỏ thành 2 scene nếu cần.
- [ ] Mọi mention "EBGM" dùng màu `ACCENT_LAVENDER`.
- [ ] Mọi mention "Jet" dùng màu `ACCENT_CYAN`.

---

## 🎯 GHI CHÚ ĐỊNH HƯỚNG SÁNG TẠO PHẦN 2

1. **Tone:** Vẫn academic, nhưng phần này có nhiều **math + technical detail** — nên dùng nhiều `MathTex` đẹp, animations từng bước (highlight từng term).
2. **Đừng làm khán giả "ngộp công thức":** Mỗi công thức xuất hiện kèm visual minh họa. Highlight từng term, đừng vứt cả công thức lên rồi đọc.
3. **Scene 13 (FBG) và Scene 15 (Matching) là 2 scene "đắt" nhất** — đầu tư nhiều effort vào.
4. **Recreate đúng tinh thần Figure 1, 2, 3, 4 của paper** — đây là những hình kinh điển, khán giả có thể đã thấy trong nhiều slide khác.
5. **Music gợi ý cho phần này:** Lo-fi nhẹ hơn phần overview (vì cần tập trung), tempo 50–55 BPM. Có thể chuyển sang piano minimal.
6. **Pacing trick:** Sau mỗi công thức, để `self.wait(1.5)` cho khán giả đọc.
