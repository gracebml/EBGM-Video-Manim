# 🎬 PLAN VIDEO MANIM — PHẦN OVERVIEW

> **Thuật toán:** Face Recognition by Elastic Bunch Graph Matching (EBGM)
> **Phần:** Overview (bài toán → cách tiếp cận trước đây → cách tiếp cận novel của EBGM)
> **Thời lượng dự kiến:** 5–6 phút
> **Số scenes:** 7

---

## 🎨 0. SETUP CHUNG (định nghĩa một lần, dùng lại toàn video)
Môi trường: conda (vid) đã tạo
### 0.1. Bảng màu (cool, sang trọng trên nền navy)

```python
# Background
BG_NAVY        = "#0D1B2A"   # nền chính - navy đậm
BG_NAVY_SOFT   = "#1B263B"   # nền phụ cho card/panel

# Text
TEXT_PRIMARY   = "#E0E1DD"   # chữ chính, trắng ngà
TEXT_MUTED     = "#A9B4C2"   # chữ phụ, xám lạnh

# Accent (lạnh, sang)
ACCENT_CYAN    = "#48CAE4"   # cyan - highlight chính
ACCENT_TEAL    = "#76C5BF"   # teal - phụ
ACCENT_BLUE    = "#778DA9"   # blue-grey - secondary
ACCENT_MINT    = "#95D5B2"   # mint - dùng cho "đúng"/"thành công"
ACCENT_LAVENDER= "#B8B5FF"   # lavender - dùng cho EBGM (signature color)

# Warning/Negative (vẫn lạnh)
ACCENT_CORAL   = "#E29578"   # coral muted - dùng cho "hạn chế"/"sai"
```

### 0.2. Font / LaTeX template hỗ trợ tiếng Việt

```python
from manim import *

# Template LaTeX hỗ trợ tiếng Việt + ký hiệu toán
vn_template = TexTemplate()
vn_template.add_to_preamble(r"""
\usepackage[utf8]{inputenc}
\usepackage[T5]{fontenc}
\usepackage[vietnamese]{babel}
\usepackage{amsmath, amssymb}
\usepackage{mathpazo}   % font Palatino - sang trọng
""")

# Font Text cho phụ đề (Manim Text)
SUBTITLE_FONT = "Be Vietnam Pro"   # hoặc "Inter", "Source Sans Pro"
TITLE_FONT    = "EB Garamond"      # serif elegant cho tiêu đề lớn
MONO_FONT     = "JetBrains Mono"   # cho code/term kỹ thuật
```

### 0.3. Helper functions tái sử dụng

```python
def make_subtitle(text, scale=0.55):
    """Phụ đề ở dưới khung hình - luôn cùng vị trí, cùng style."""
    sub = Text(text, font=SUBTITLE_FONT, color=TEXT_PRIMARY, weight="LIGHT")
    sub.scale(scale).to_edge(DOWN, buff=0.5)
    return sub

def section_title(text):
    """Tiêu đề mỗi section."""
    return Text(text, font=TITLE_FONT, color=ACCENT_CYAN, weight="MEDIUM").scale(0.9)

def cool_glow(mob, color=ACCENT_CYAN):
    """Hiệu ứng glow nhẹ quanh đối tượng."""
    return mob.copy().set_stroke(color, width=8, opacity=0.3)
```

### 0.4. Convention global

- **Background:** luôn `BG_NAVY` (set 1 lần ở đầu mỗi Scene bằng `self.camera.background_color = BG_NAVY`).
- **Phụ đề tiếng Việt:** dùng `Text` với font Be Vietnam Pro, KHÔNG dùng `Tex` (LaTeX render tiếng Việt dấu phức tạp & dễ lỗi).
- **Công thức toán + thuật ngữ Anh:** dùng `MathTex` / `Tex` với `tex_template=vn_template`.
- **Mỗi phụ đề** không quá 2 dòng, không quá 18 chữ/dòng.
- **Transition giữa scene:** `FadeOut(*self.mobjects)` rồi `Wait(0.5)`.

---

## 📽️ SCENE 1 — TITLE OPENING (≈ 12s)

### 🎯 Mục đích
Mở đầu sang trọng, gây ấn tượng, giới thiệu tên thuật toán.

### 🎨 Visual storyboard

**Frame 1 (0s–3s):** Nền navy đen tuyền. Từ giữa màn hình, các **chấm sáng nhỏ** (Dots, cyan/lavender) xuất hiện ngẫu nhiên rồi **tự động kết nối** thành một đồ thị (graph) trừu tượng — gợi ý về "image graph" sắp xuất hiện. Dùng `Create` + `Flash` nhẹ tại mỗi node.

**Frame 2 (3s–6s):** Đồ thị từ từ **biến hình** (`Transform`) thành lưới các điểm phủ lên một silhouette khuôn mặt mờ (chỉ đường viền, opacity 0.4, màu `ACCENT_BLUE`).

**Frame 3 (6s–12s):** Silhouette mờ đi, **tên thuật toán** trượt vào từ dưới lên:

```
        FACE RECOGNITION
              BY
   ELASTIC BUNCH GRAPH MATCHING
```

- Dòng 1 & 2: `Text` font EB Garamond, màu `TEXT_PRIMARY`, scale 0.7.
- Dòng 3: `Text` font EB Garamond, màu `ACCENT_LAVENDER`, scale 1.0, **chữ "ELASTIC"** và **"BUNCH GRAPH"** highlight bằng underline mảnh (cyan).
- Dưới cùng (xuất hiện sau 1s): `Wiskott, Fellous, Krüger, von der Malsburg · 1999` — italic, scale 0.35, màu `TEXT_MUTED`.

### 📝 Code skeleton

```python
class Scene1_TitleOpening(Scene):
    def construct(self):
        self.camera.background_color = BG_NAVY

        # Phase 1: dots → graph
        dots = VGroup(*[Dot(point=np.random.uniform(-3,3,3)*[1,1,0],
                            color=ACCENT_CYAN, radius=0.05) for _ in range(12)])
        edges = VGroup(*[Line(dots[i].get_center(), dots[j].get_center(),
                              stroke_width=1, color=ACCENT_BLUE)
                         for i, j in [(0,1),(1,2),(2,3),(3,4),(4,0),
                                      (5,6),(6,7),(0,5),(2,7),(3,8)]])
        self.play(LaggedStart(*[GrowFromCenter(d) for d in dots], lag_ratio=0.1))
        self.play(Create(edges, run_time=1.5))

        # Phase 2: morph into face outline grid
        face_outline = SVGMobject("face_silhouette.svg").set_color(ACCENT_BLUE).set_opacity(0.4)
        # ... (transform dots to land on fiducial positions of face_outline)

        # Phase 3: Title in
        title_main = Text("ELASTIC BUNCH GRAPH MATCHING",
                          font=TITLE_FONT, color=ACCENT_LAVENDER).scale(0.85)
        title_top  = Text("FACE RECOGNITION BY",
                          font=TITLE_FONT, color=TEXT_PRIMARY).scale(0.55)
        title_top.next_to(title_main, UP, buff=0.3)
        citation = Text("Wiskott · Fellous · Krüger · von der Malsburg  —  1999",
                        font=SUBTITLE_FONT, slant=ITALIC,
                        color=TEXT_MUTED).scale(0.35)
        citation.next_to(title_main, DOWN, buff=0.6)

        self.play(FadeOut(face_outline, edges, dots))
        self.play(Write(title_top), Write(title_main), run_time=2)
        self.play(FadeIn(citation, shift=UP*0.2))
        self.wait(2)
        self.play(FadeOut(*self.mobjects))
```

### 💬 Phụ đề
*(không có phụ đề ở scene mở đầu — chỉ để hình ảnh & tựa đề "lên tiếng")*

---

## 📽️ SCENE 2 — BÀI TOÁN FACE RECOGNITION (≈ 50s)

### 🎯 Mục đích
Trình bày bài toán face recognition và **chia làm 2 nhánh** rõ ràng: Verification (1:1) vs Identification (1:N).

### 🎨 Visual storyboard

**Phần A (0s–8s): Câu hỏi mở**

- Giữa màn hình hiện câu hỏi lớn: *"Máy tính nhận diện khuôn mặt như thế nào?"*
  - `Text`, font Be Vietnam Pro, weight LIGHT, scale 0.7, màu `TEXT_PRIMARY`.
- Phía sau câu hỏi: 4–5 hình khuôn mặt nhỏ mờ trôi chậm từ phải sang trái (parallax).
- Câu hỏi **biến hình** thành tiêu đề scene: *"Face Recognition — Hai nhánh"*.

**Phần B (8s–50s): Split-screen 2 nhánh**

Màn hình chia đôi bằng đường thẳng đứng mảnh (`Line` stroke 0.5, cyan, opacity 0.4).

```
┌─────────────────────┬─────────────────────┐
│   VERIFICATION 1:1  │  IDENTIFICATION 1:N │
│   (Xác thực)        │  (Nhận dạng)        │
│                     │                     │
│   [icon: 1 ảnh +    │   [icon: 1 ảnh →    │
│    1 ID card →      │    quét N ảnh]      │
│    ✓ / ✗]           │                     │
│                     │                     │
│   "Đúng là họ       │   "Là ai trong      │
│    không?"          │    N người?"        │
│                     │                     │
│   Ví dụ:            │   Ví dụ:            │
│   • FaceID iPhone   │   • Camera an ninh  │
│   • Hộ chiếu        │   • Auto-tag FB     │
└─────────────────────┴─────────────────────┘
```

**Animation chi tiết:**

1. Tiêu đề từng nhánh **slide in** từ hai phía (left từ trái, right từ phải) — `FadeIn(shift=RIGHT)`.
2. **Bên trái (Verification):**
   - Một `Rectangle` đại diện cho ảnh khuôn mặt (chứa 1 silhouette).
   - Bên cạnh: icon `ID card` (Rectangle có chữ "ID" bên trong).
   - Một dấu `=?` lớn ở giữa.
   - Sau 1.5s: dấu `=?` biến thành `✓` (mint) hoặc `✗` (coral) — thử cả 2 luân phiên.
3. **Bên phải (Identification):**
   - Một `Rectangle` chứa silhouette (probe image).
   - Một `Arrow` chỉ sang phải.
   - Một **grid 5×3 = 15 ô** nhỏ (gallery DB), một ô được highlight bằng glow lavender.
   - Hiệu ứng "scan": một thanh ngang sáng quét qua grid từ trên xuống (1.5s).
   - Ô khớp **giật nhẹ** (`Indicate`) và phóng to nhẹ.

**Phần C (cuối scene, 45s–50s):** Hai panel cùng zoom out → ghi chú dưới chân: *"Bài báo EBGM tập trung vào nhánh 1:N (Identification)."*

### 💬 Phụ đề (timing tương đối)

| Thời điểm | Phụ đề |
|---|---|
| 0s–4s | "Máy tính nhận diện khuôn mặt như thế nào?" |
| 4s–8s | "Bài toán có hai nhánh chính" |
| 8s–14s | "Verification — Xác thực 1:1 — Người này có đúng là họ không?" |
| 14s–20s | "So sánh một ảnh với một mẫu duy nhất → Đúng / Sai" |
| 20s–24s | "Ví dụ: mở khóa FaceID, quẹt hộ chiếu điện tử" |
| 24s–30s | "Identification — Nhận dạng 1:N — Người này là ai trong N người?" |
| 30s–36s | "So sánh một ảnh với toàn bộ N mẫu → trả về top giống nhất" |
| 36s–42s | "Ví dụ: tìm tội phạm qua camera, auto-tag Facebook" |
| 42s–50s | "EBGM tập trung giải quyết bài toán 1:N" |

### 🛠️ Manim techniques chính
`Text`, `Rectangle`, `SVGMobject` (cho icon ID/card), `Arrow`, `VGroup` (cho grid), `Indicate`, `Flash`, `Transform`, custom `ValueTracker` cho thanh scan.

---

## 📽️ SCENE 3 — VẤN ĐỀ CỐT LÕI (≈ 55s)

### 🎯 Mục đích
Làm nổi bật **hai cấp độ thách thức**: (1) variance trong cùng một người, (2) cấu trúc chung của lớp khuôn mặt → in-class discrimination.

### 🎨 Visual storyboard

**Phần A (0s–8s): Tiêu đề & dẫn dắt**
- Tiêu đề: *"Vấn đề cốt lõi"* (section_title, slide từ trên xuống).
- Câu dẫn: *"Tại sao bài toán này lại khó?"*

**Phần B (8s–30s): Variance — cùng một người, rất nhiều biến đổi**

- Ở giữa hiện **5 ảnh** của cùng một người, xếp thành vòng cung:
  - Ảnh 1: chính diện, trung tính.
  - Ảnh 2: nghiêng 30°.
  - Ảnh 3: cười tươi.
  - Ảnh 4: thiếu sáng / chụp gần.
  - Ảnh 5: đeo kính.
- Mỗi ảnh xuất hiện kèm 1 nhãn nhỏ: *biểu cảm*, *tư thế*, *ánh sáng*, *vị trí*, *kích thước*.
- Sau khi đủ 5 ảnh, một **vòng tròn lớn** bao quanh + chữ giữa: **"CÙNG MỘT NGƯỜI"** (mint).
- Mũi tên cong ↔ giữa các ảnh, ngụ ý "máy phải hiểu đây đều là cùng một người".
- Thuật ngữ tiếng Anh hiện ra (góc dưới): `discrimination-in-the-presence-of-variance`, font MONO, scale 0.4, cyan.

**Phần C (30s–50s): In-class discrimination — cấu trúc chung của khuôn mặt**

- Tất cả ảnh trên fade out, hiện một **face template** đơn giản (vector): hình bầu dục + 2 mắt + mũi + miệng — line art mảnh, cyan.
- Phụ đề chỉ rõ: *"Mọi khuôn mặt đều có cấu trúc cơ bản giống nhau"*.
- Lần lượt 3 khuôn mặt khác nhau (3 người) **slide qua template** — template trùng khớp ở các điểm cơ bản.
- Sau đó **zoom vào vùng mắt và miệng**, highlight chi tiết riêng → chữ hiện ra: *"Phân biệt cá nhân = nhìn vào những chi tiết tinh tế hơn"*.
- Thuật ngữ: `in-class discrimination` (góc dưới, MONO, cyan).

**Phần D (50s–55s): Kết luận**

- Hiện 2 cụm từ song song, lớn:
  - **"Collapse the variance"** (mint) ← nén bỏ biến đổi
  - **"Emphasize discriminating features"** (lavender) ← nhấn mạnh đặc trưng phân biệt
- Hai cụm từ này sẽ là "promise" của EBGM ở scene sau.

### 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–4s | "Tại sao nhận diện khuôn mặt lại khó?" |
| 4s–12s | "Một người có thể trông rất khác nhau giữa các bức ảnh" |
| 12s–20s | "Biểu cảm, tư thế, ánh sáng, vị trí, kích thước — tất cả đều thay đổi" |
| 20s–28s | "Đây là bài toán: phân biệt trong môi trường có nhiều biến đổi" |
| 28s–36s | "Nhưng mọi khuôn mặt đều có cấu trúc chung — hai mắt, một mũi, một miệng" |
| 36s–44s | "Máy phải biết cấu trúc chung trước, rồi mới tìm chi tiết phân biệt từng người" |
| 44s–55s | "Mục tiêu: triệt tiêu biến đổi & làm nổi đặc trưng nhận dạng" |

### 🛠️ Manim techniques chính
`ImageMobject` (cho 5 ảnh), `Circle`, `CurvedArrow`, `Transform` (template ↔ face), `ZoomedScene` hoặc `MoveCamera` cho phần zoom mắt/miệng, `LaggedStart`.

---

## 📽️ SCENE 4 — CÁCH TIẾP CẬN TRƯỚC ĐÂY (≈ 90s)

### 🎯 Mục đích
Trình bày 3 cách tiếp cận truyền thống, **mỗi cách 1 panel riêng**, có pros & cons rõ ràng → đặt nền cho EBGM "novel" ở scene tiếp.

### 🎨 Cấu trúc tổng

- Mỗi cách 1 panel = **~28 giây**.
- Layout panel chuẩn:

```
┌──────────────────────────────────────────┐
│   [Số: 01]   TÊN CÁCH TIẾP CẬN           │
│   ─────────                              │
│                                          │
│   [Visual illustration ở giữa, ~5s anim] │
│                                          │
│   ✓ Ưu điểm:    ...                      │
│   ✗ Hạn chế:    ...                      │
└──────────────────────────────────────────┘
```

- Header `01` `02` `03` lớn, font EB Garamond, màu `ACCENT_BLUE`, scale 1.2.
- Tên cách: font EB Garamond, màu `TEXT_PRIMARY`, scale 0.75.
- Visual: chiếm 50% chiều cao giữa.
- Ưu điểm: icon ✓ mint, text muted.
- Hạn chế: icon ✗ coral, text muted (sẽ là phần được nhấn mạnh).

### Panel 01 — DESIGNER-PROVIDED STRUCTURES (0s–28s)

**Visual:** 
- Vẽ tay (line-by-line, `Create`) một mô hình mắt: **vòng tròn bên trong hình quả hạnh**, kèm các thông số `r=15px`, `α=40°` chú thích bằng `MathTex`.
- Bên cạnh: 3 mô hình tương tự cho mũi, miệng, lông mày — line art.
- Tất cả nối với "code block giả" hiện ra ở bên: 
  ```
  if eye_open():
      detect_iris()
  elif sunglasses_detected():
      ???
  ```
- Khi gặp dòng `???`, đèn đỏ nhấp nháy + một ảnh người đeo kính râm xuất hiện, mô hình mắt "không khớp" → hiệu ứng shake & glitch.

**Pros/Cons:**
- ✓ "Mô hình rõ ràng, dễ hiểu"
- ✗ "Đắt đỏ, thiếu linh hoạt — gặp ngoại lệ phải lập trình lại"

### Panel 02 — NEURAL NETWORKS (28s–56s)

**Visual:**
- Vẽ một mạng nơ-ron 4 lớp (input layer = pixels → hidden → hidden → output = "person ID").
- Dùng `Dot` + `Line` cho neurons/connections, màu cyan/lavender, glow nhẹ.
- Hàng ngàn ảnh **bay từ trái** vào input layer (dùng `LaggedStart` của `ImageMobject` nhỏ), kèm chữ chạy nhanh: `epoch 1`, `epoch 2`, …, `epoch 1000`.
- Hiệu ứng "ánh sáng pulse" chạy dọc theo các connection mỗi khi có ảnh mới được nạp.
- Một đồng hồ nhỏ ở góc kêu tích tắc & một biểu tượng `$` đếm tăng (chi phí compute).

**Pros/Cons:**
- ✓ "Tự học cấu trúc từ dữ liệu"
- ✗ "Cần khối lượng huấn luyện khổng lồ và chuyên sâu"

### Panel 03 — PCA / EIGENFACES (56s–90s)

**Visual:**
- Hiện 1 khuôn mặt → công thức `MathTex`:
  $$\mathbf{f} \approx \bar{\mathbf{f}} + \sum_{i=1}^{k} \alpha_i \mathbf{u}_i$$
- 4–5 "eigenfaces" (ảnh giả mặt nạ trừu tượng, tone xám-cyan) xếp ngang, mỗi ảnh nhân hệ số $\alpha_i$ rồi cộng dồn → tái tạo khuôn mặt gốc.
- **Demo hạn chế:** hiện 2 ảnh khuôn mặt cùng người, **một có miệng cao, một có miệng thấp**.
  - Dùng `Transform` để "trộn tuyến tính" — kết quả là **2 cái miệng mờ chồng lên nhau** (làm thật bằng cách overlay 2 image với opacity 0.5).
  - Mũi tên đỏ chỉ vào → chữ: *"Không nội suy ra được vị trí trung gian!"*
- **Demo hạn chế 2:** một ảnh khuôn mặt bị che một phần (tóc che mắt) — vector đại diện trong eigenspace bị lệch hoàn toàn so với gốc → 2 chấm trong không gian 2D xa nhau.

**Pros/Cons:**
- ✓ "Biểu diễn nén, gọn gàng (~30 hệ số)"
- ✗ "Tuyến tính → không xử lý được biến đổi hình học & che khuất"

### 💬 Phụ đề (highlights)

| Thời điểm | Phụ đề |
|---|---|
| 0s–6s | "Trước EBGM, có ba hướng tiếp cận phổ biến" |
| 6s–14s | "Một: thiết kế thủ công các đặc trưng khuôn mặt" |
| 14s–22s | "Ví dụ: mô hình mắt là vòng tròn bên trong quả hạnh" |
| 22s–28s | "Hạn chế: gặp ngoại lệ là phải lập trình lại từ đầu" |
| 28s–36s | "Hai: dùng mạng nơ-ron học từ dữ liệu" |
| 36s–44s | "Mạng tự hấp thụ cấu trúc qua quá trình huấn luyện" |
| 44s–56s | "Hạn chế: cần dữ liệu khổng lồ và huấn luyện rất tốn kém" |
| 56s–64s | "Ba: PCA — phân tách khuôn mặt thành các vector riêng" |
| 64s–72s | "Toàn bộ khuôn mặt được biểu diễn bằng vài chục hệ số" |
| 72s–82s | "Nhưng PCA tuyến tính — kết hợp hai khuôn mặt cho ra ảnh mờ" |
| 82s–90s | "Và rất nhạy cảm với che khuất hoặc biến dạng cục bộ" |

### 🛠️ Manim techniques chính
`Create` (vẽ line-by-line), `LaggedStart`, mạng nơ-ron tự build bằng `VGroup` của `Dot` + `Line`, công thức `MathTex` với `vn_template`, demo overlay bằng `ImageMobject` + `set_opacity`.

---

## 📽️ SCENE 5 — CHUYỂN TIẾP: VẤN ĐỀ CÒN BỎ NGỎ (≈ 15s)

### 🎯 Mục đích
Cầu nối ngắn — tổng kết hạn chế của 3 cách trên, gợi mở "có cách nào tốt hơn không?".

### 🎨 Visual storyboard

- Background tối hẳn xuống (opacity 0.3 cho mọi thứ trước đó).
- 3 box mờ của 3 cách trước xếp ngang, mỗi box có 1 dấu ✗ coral.
- Câu hỏi lớn fade in giữa màn hình: 
  > *"Liệu có cách nào tích hợp được thông tin cấu trúc — mà KHÔNG cần huấn luyện khổng lồ, KHÔNG cần lập trình lại, KHÔNG bị tuyến tính giới hạn?"*
- Sau 3s, câu hỏi co lại thành tiêu đề nhỏ → trượt lên top, mở đường cho Scene 6.

### 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–8s | "Cả ba cách tiếp cận đều có điểm nghẽn riêng" |
| 8s–15s | "Liệu có giải pháp nào trung gian, gần với cách con người nhận thức?" |

### 🛠️ Manim techniques chính
`set_opacity` để làm mờ, `Transform`, `Write`.

---

## 📽️ SCENE 6 — CÁCH TIẾP CẬN NOVEL CỦA EBGM (≈ 75s)

### 🎯 Mục đích
Giới thiệu **trực giác** của EBGM (chưa đi vào chi tiết kỹ thuật), nhấn 4 ưu điểm chính.

### 🎨 Visual storyboard

**Phần A (0s–10s): Reveal tên EBGM**

- Tiêu đề lớn fade in: *"EBGM — Elastic Bunch Graph Matching"*.
- Dưới: subtitle "Một cách tiếp cận mới mẻ" (font EB Garamond italic, muted).
- Background: các "graph nodes" lavender lấp lánh trôi nhẹ.

**Phần B (10s–35s): Tóm tắt 3 khái niệm cốt lõi**

Hiện 3 box xếp ngang, từng box xuất hiện kèm icon minh họa:

| # | Khái niệm | Visual icon |
|---|---|---|
| 1 | **Image graph** | Một mạng các node phủ lên khuôn mặt (mắt, mũi, miệng, viền) — line art. |
| 2 | **Jet (Gabor wavelets)** | Một node phóng to → bên trong là 40 vạch sóng (5 tần số × 8 hướng) xếp như "nan quạt". |
| 3 | **Bunch graph** | Nhiều image graph (~5 cái) xếp chồng lên nhau như cọc thẻ bài, mỗi node là 1 "bunch" jet. |

- Mỗi box xuất hiện với `FadeIn(shift=UP)`, sau 1s thì icon bên trong animate (vẽ graph, tạo jet, stack các graph).
- Lưu ý: ở đây chỉ **giới thiệu khái niệm**, các scene sau sẽ đi sâu.

**Phần C (35s–70s): 4 ưu điểm chính của EBGM**

Layout: 4 card xếp 2×2, mỗi card có:
- Icon ở top
- Tiêu đề ngắn (bold)
- Mô tả 1–2 dòng

| # | Card | Tiêu đề | Mô tả |
|---|---|---|---|
| 1 | 🌊 Gabor waves icon | Tích hợp đặc tính vật lý | Trơ lì trước ánh sáng, dịch chuyển nhỏ, biến dạng cục bộ |
| 2 | 📚 Stack of graphs | Linh hoạt nhờ Bunch Graph | Chỉ vài chục mẫu, nhưng tổ hợp được vô số biến thể |
| 3 | 🎯 Few examples | Hiệu quả với ít dữ liệu | ~70 ảnh là đủ cho toàn bộ tác vụ |
| 4 | ➕ Plus icon | Dễ mở rộng | Gặp ngoại lệ chỉ cần thêm ảnh vào bunch, không lập trình lại |

- Mỗi card pop in lần lượt (LaggedStart, 0.4s mỗi card), highlight viền lavender khi xuất hiện.
- Sau khi đủ 4 card, một **đường tròn cyan** bao quanh cả 4 + chữ giữa: *"Cân bằng giữa thiết kế thủ công & học máy"*.

**Phần D (70s–75s): Câu chốt**

> *"EBGM gần với cách hệ thống nhận thức tự nhiên hoạt động — chỉ vài chục ví dụ là đủ."*

### 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–6s | "EBGM — Elastic Bunch Graph Matching" |
| 6s–14s | "Một cách tiếp cận trung gian, linh hoạt hơn" |
| 14s–22s | "Image Graph — biểu diễn khuôn mặt bằng đồ thị các điểm mốc" |
| 22s–30s | "Jet — đặc trưng cục bộ tại mỗi điểm, dùng Gabor wavelets" |
| 30s–38s | "Bunch Graph — chồng nhiều đồ thị mẫu thành một thực thể tổ hợp" |
| 38s–46s | "Trơ lì với ánh sáng và biến dạng nhờ Gabor wavelets" |
| 46s–54s | "Linh hoạt: mỗi điểm có thể chọn 'expert' tốt nhất từ bunch" |
| 54s–62s | "Chỉ cần ~70 mẫu cho toàn bộ tác vụ nhận diện" |
| 62s–70s | "Gặp ngoại lệ ư? Chỉ cần thêm ảnh vào bunch — không cần lập trình lại" |
| 70s–75s | "Cân bằng giữa thiết kế thủ công và học máy" |

### 🛠️ Manim techniques chính
`FadeIn(shift=)`, `LaggedStart`, custom Gabor jet visualization (dùng `ParametricFunction` + `VGroup` cho 40 sóng), stack hiệu ứng bằng `VGroup` với `arrange(IN, buff=0.1)` rồi xoay góc 3D nhẹ.

> 💡 **Gabor jet visualization gợi ý:**
> ```python
> def make_jet_icon(scale=1.0):
>     wedges = VGroup()
>     for nu in range(5):       # 5 tần số
>         for mu in range(8):   # 8 hướng
>             freq = 0.5 + nu * 0.3
>             angle = mu * PI / 8
>             curve = ParametricFunction(
>                 lambda t: np.array([t*np.cos(angle), 
>                                     0.3*np.sin(freq*t*5)*np.cos(angle), 0]),
>                 t_range=[0, 0.6], color=ACCENT_CYAN, stroke_width=1
>             )
>             wedges.add(curve)
>     return wedges.scale(scale)
> ```

---

## 📽️ SCENE 7 — KẾT THÚC OVERVIEW & TEASER (≈ 15s)

### 🎯 Mục đích
Tóm lại "promise" của EBGM trong 1 câu, dẫn vào phần tiếp theo (chi tiết hệ thống).

### 🎨 Visual storyboard

- Quay lại background navy thuần.
- Hiện 1 image graph hoàn chỉnh (đầy đủ node + edge, jet ở mỗi node lấp lánh) — đẹp, slow rotation nhẹ.
- Dưới: text 2 dòng (đại diện cho 2 promise của Scene 3):
  > **"Collapse the variance · Emphasize discriminating features"**
- Sau 4s, image graph fade out, hiện text teaser:
  > **"Tiếp theo: Khám phá chi tiết hệ thống EBGM"**
  > **"→ Gabor Wavelets · Face Representation · Matching · Recognition"**
- Một arrow lớn (lavender) chỉ sang phải, kèm hiệu ứng `Flash` ở mũi tên.

### 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–8s | "EBGM — nén biến đổi, làm nổi đặc trưng phân biệt" |
| 8s–15s | "Tiếp theo: đi sâu vào từng thành phần của hệ thống" |

---

## 📊 TỔNG HỢP TIMING

| Scene | Tên | Thời lượng | Cumulative |
|---|---|---|---|
| 1 | Title Opening | 12s | 0:12 |
| 2 | Bài toán Face Recognition | 50s | 1:02 |
| 3 | Vấn đề cốt lõi | 55s | 1:57 |
| 4 | Cách tiếp cận trước đây | 90s | 3:27 |
| 5 | Chuyển tiếp | 15s | 3:42 |
| 6 | Cách tiếp cận novel của EBGM | 75s | 4:57 |
| 7 | Kết thúc Overview | 15s | 5:12 |

**Tổng:** ~5 phút 12 giây.

---

## ✅ CHECKLIST TRƯỚC KHI RENDER

- [ ] Đã cài font `Be Vietnam Pro`, `EB Garamond` trên máy.
- [ ] LaTeX template tiếng Việt đã test với 1 chuỗi có dấu (vd: "Khuôn mặt người").
- [ ] Đã chuẩn bị assets:
  - [ ] SVG silhouette khuôn mặt (cho Scene 1).
  - [ ] 5 ảnh cùng một người ở các tư thế/biểu cảm khác nhau (Scene 3).
  - [ ] 3 ảnh khuôn mặt khác nhau (Scene 3, demo template).
  - [ ] Icon ID card, gallery grid (có thể vẽ bằng `Rectangle`).
  - [ ] (Tùy chọn) Eigenface mock images cho Scene 4 panel 3.
- [ ] Đã verify rằng phụ đề không bị tràn ra ngoài frame ở mọi scene.
- [ ] Đã chọn quality phù hợp: `-pql` cho draft, `-pqh` cho final.

---

## 🎯 GHI CHÚ ĐỊNH HƯỚNG SÁNG TẠO

1. **Tone tổng:** Sang trọng, "academic but cinematic". Tránh hoạt hình quá sôi động — EBGM là một bài báo kinh điển, nên giữ phong thái "trang sách trí thức".
2. **Đừng nhồi chữ:** Mỗi frame tối đa 1 câu phụ đề + tối đa 3–4 mobjects chính. Khi cần nhiều text, hãy chia thành nhiều beat nhỏ.
3. **Music gợi ý (nếu cần):** Lo-fi/ambient/neo-classical instrumental, ~60 BPM. Volume thấp, không lấn phụ đề.
4. **Pacing:** Sau mỗi animation lớn, để `self.wait(0.8)` cho khán giả "thở".
5. **Signature visual:** Mỗi lần nhắc đến EBGM, dùng **lavender (#B8B5FF)** — nhất quán xuyên suốt, tạo brand identity cho thuật toán.

---

*End of Overview plan. Sẵn sàng để bắt đầu code Scene 1 hoặc tiếp tục plan cho phần "Chi tiết EBGM".*
