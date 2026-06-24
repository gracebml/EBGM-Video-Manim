# 🎬 PLAN VIDEO MANIM — PHẦN 4: DISCUSSION

> **Phần:** Discussion — So sánh & Hướng phát triển
> **Cấu trúc:** Tính tổng quát → So sánh các hệ thống → Rotation in depth → Future Developments
> **Thời lượng dự kiến:** 7–8 phút
> **Số scenes:** 9

---

## 🎨 0. KẾ THỪA SETUP

Tái sử dụng **toàn bộ** setup từ `overview.md`, `algo_detail.md`, `efficient.md`:
- Bảng màu (navy + cool accents)
- Font (Be Vietnam Pro / EB Garamond / JetBrains Mono)
- LaTeX template tiếng Việt
- Helper functions (`make_subtitle`, `section_title`, `vietnamese_label`, `make_bar_chart`, `make_percentage_circle`, `trophy_icon`)
- **Signature color:** `ACCENT_LAVENDER (#B8B5FF)` cho EBGM

### Bổ sung cho phần này

```python
# Màu cho so sánh đối thủ (tái dùng từ phần 3, nhất quán)
EBGM_BRAND    = "#B8B5FF"   # lavender
PCA_COLOR     = "#76C5BF"   # teal
NN_COLOR      = "#E29578"   # coral nhạt
PREV_COLOR    = "#778DA9"   # blue-grey (preceding system)
YUILLE_COLOR  = "#8896AB"   # xám lạnh (user-defined features)
LANITIS_COLOR = "#5FA8D3"   # blue (Lanitis deformable)
WARP_COLOR    = "#A7C5EB"   # light blue (3D warping)

# Màu cho "vs" comparison
PRO_COLOR     = "#95D5B2"   # mint - điểm mạnh
CON_COLOR     = "#E29578"   # coral - điểm yếu
FUTURE_GLOW   = "#B8B5FF"   # lavender - hướng tương lai
```

### Helper bổ sung

```python
def make_vs_card(title_left, title_right, color_left, color_right, scale=1.0):
    """
    Card so sánh 'X vs Y': 2 panel cạnh nhau với divider 'VS' ở giữa.
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
    
    vs = Text("VS", font=TITLE_FONT, color=TEXT_MUTED,
              weight=BOLD).scale(0.6)
    
    return VGroup(panel_l, panel_r, lbl_l, lbl_r, vs).scale(scale)

def pro_item(text_str, scale=0.4):
    """Dòng điểm mạnh với check icon mint."""
    check = VGroup(
        Line([-0.08,0,0], [-0.02,-0.06,0], color=PRO_COLOR, stroke_width=3),
        Line([-0.02,-0.06,0], [0.08,0.06,0], color=PRO_COLOR, stroke_width=3),
    )
    txt = Text(text_str, font=SUBTITLE_FONT, color=TEXT_PRIMARY,
               weight=LIGHT).scale(scale)
    return VGroup(check, txt).arrange(RIGHT, buff=0.2)

def con_item(text_str, scale=0.4):
    """Dòng điểm yếu với cross icon coral."""
    cross = VGroup(
        Line([-0.06,0.06,0], [0.06,-0.06,0], color=CON_COLOR, stroke_width=3),
        Line([-0.06,-0.06,0], [0.06,0.06,0], color=CON_COLOR, stroke_width=3),
    )
    txt = Text(text_str, font=SUBTITLE_FONT, color=TEXT_PRIMARY,
               weight=LIGHT).scale(scale)
    return VGroup(cross, txt).arrange(RIGHT, buff=0.2)

def future_node(text_str, icon_mob, color=FUTURE_GLOW, scale=1.0):
    """Node cho roadmap tương lai: icon + text trong rounded box."""
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

---

## 📋 STRUCTURE TỔNG QUAN

| Scene | Tên | Thời lượng |
|---|---|---|
| 27 | Intro Discussion + Tính tổng quát | 45s |
| 28 | EBGM vs Preceding System (Lades 1993) | 70s |
| 29 | EBGM vs User-defined Features (Yuille) | 55s |
| 30 | EBGM vs PCA / Eigenfaces | 75s |
| 31 | EBGM vs Deformable Models (Lanitis) | 60s |
| 32 | Rotation in Depth — Các hướng tiếp cận | 80s |
| 33 | Future Developments — Roadmap | 90s |
| 34 | Speed Optimization (Future) | 40s |
| 35 | Kết thúc toàn video | 35s |

**Tổng:** ~9 phút 10 giây.

---

# 📽️ SCENE 27 — INTRO DISCUSSION + TÍNH TỔNG QUÁT (≈ 45s)

## 🎯 Mục đích
Mở đầu phần Discussion, khẳng định EBGM là hệ thống tổng quát cho in-class recognition, không chỉ riêng khuôn mặt.

## 🎨 Visual storyboard

### Phase A (0s–12s): Tiêu đề & câu hỏi mở

- Tiêu đề: **"Discussion — Đặt EBGM vào bức tranh lớn"** (lavender).
- Câu dẫn: *"EBGM đã hiệu quả. Nhưng nó đứng ở đâu giữa các hệ thống khác?"*
- Background: các "graph nodes" lavender lấp lánh trôi nhẹ.

### Phase B (12s–32s): Tính tổng quát — Không chỉ riêng khuôn mặt

Trung tâm hiện chữ lớn: **"IN-CLASS RECOGNITION"** (lavender).

- Xung quanh chữ, 4 ví dụ về "lớp đối tượng" xuất hiện theo vòng tròn (orbit animation):
  - 👤 **Khuôn mặt người** (đang demo) — icon face silhouette
  - 🐕 **Loài động vật** (vd chó) — icon paw/animal silhouette
  - 🚗 **Phương tiện** — icon car silhouette
  - 🌸 **Thực vật** — icon flower silhouette
- (Icon vẽ bằng VMobject, KHÔNG emoji.)
- Mỗi icon kết nối với chữ trung tâm bằng đường nét đứt lavender.
- Animation: các icon "quay" quanh chữ trung tâm như vệ tinh (orbit), kèm chú thích: *"Cùng cấu trúc → cùng phương pháp."*

### Phase C (32s–45s): 3 ưu thế cốt lõi

Hiện 3 ưu thế ngắn (3 badge xếp ngang), pop in tuần tự:

| # | Badge | Mô tả |
|---|---|---|
| 1 | 🚫 No training | Không cần huấn luyện khổng lồ như Neural Net |
| 2 | 📷 One image | Nhận diện người mới chỉ từ 1 ảnh |
| 3 | 🔄 22° robust | Chịu được xoay đến 22° (giảm mạnh khi lớn hơn) |

- Mỗi badge dùng RoundedRectangle viền lavender + icon vẽ tay + text.
- Khi badge 3 xuất hiện, một gauge nhỏ show "performance giảm dần khi góc xoay tăng".

## 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–6s | "EBGM đã hiệu quả — nhưng nó đứng ở đâu giữa các hệ thống khác?" |
| 6s–14s | "Trước hết: EBGM không chỉ dành cho khuôn mặt" |
| 14s–22s | "Nó giải quyết bài toán nhận diện trong cùng một lớp đối tượng" |
| 22s–32s | "Cùng cấu trúc — có thể áp dụng cho động vật, xe cộ, thực vật" |
| 32s–40s | "Ba ưu thế: không cần huấn luyện, chỉ một ảnh, robust đến 22°" |
| 40s–45s | "Nhưng hiệu năng giảm đáng kể ở các góc xoay lớn hơn" |

## 🛠️ Manim techniques
Orbit animation (`Rotate` quanh tâm), `DashedLine`, badge với RoundedRectangle, custom VMobject icons, `LaggedStart`.

---

# 📽️ SCENE 28 — EBGM VS PRECEDING SYSTEM (Lades 1993) (≈ 70s)

## 🎯 Mục đích
Trình bày 3 cải tiến lớn của EBGM so với hệ tiền nhiệm.

## 🎨 Visual storyboard

### Phase A (0s–10s): Setup

- Tiêu đề: **"EBGM vs Hệ tiền nhiệm (Lades, 1993)"**.
- Hiện vs-card: bên trái "LADES 1993" (PREV_COLOR), bên phải "EBGM" (EBGM_BRAND).
- Câu dẫn: *"EBGM kế thừa và cải tiến 3 điều cốt lõi."*

### Phase B (10s–60s): 3 cải tiến — mỗi cải tiến 1 mini-demo

**Cải tiến 1 (10s–27s): Phase information cho định vị chính xác**

- Bên trái (Lades): node được match nhưng lệch (~5px), không dùng phase. Visualize: chấm lệch khỏi vị trí đúng.
- Bên phải (EBGM): node match chính xác (~1.6px) nhờ phase. Visualize: chấm trùng khít.
- Mũi tên & label: *"① Dùng phase wavelet → định vị chính xác hơn"*
- Số liệu nhỏ: "5.2px → 1.6px"

**Cải tiến 2 (27s–44s): Object-adapted grids cho nhiều pose**

- Bên trái (Lades): chỉ 1 grid cứng cho mọi ảnh. Visualize: 1 grid áp lên nhiều pose → mismatch ở pose nghiêng.
- Bên phải (EBGM): 3 grids khác nhau cho frontal/half-profile/profile. Visualize: mỗi pose có grid riêng khớp đẹp.
- Label: *"② Object-adapted grids → xử lý nhiều góc chụp"*

**Cải tiến 3 (44s–60s): FBG cho single-pass matching**

- Bên trái (Lades): với mỗi gallery image, phải search lại node positions → chậm. Visualize: 1 probe phải match nhiều lần (lặp lại animation match nhiều lần).
- Bên phải (EBGM): FBG cho phép tìm node positions 1 LẦN duy nhất cho probe mới → nhanh. Visualize: 1 lần match → image graph → so sánh trực tiếp.
- Label: *"③ FBG → tìm điểm mốc 1 lần duy nhất → tăng tốc"*

### Phase C (60s–70s): Tổng kết

- Hiện bảng tóm tắt 3 cải tiến với check marks.
- Câu chốt: *"Cùng accuracy trên cùng pose — nhưng nhanh hơn, linh hoạt hơn, mở rộng tốt hơn."*
- Note nhỏ honest: *"(Accuracy trên cùng pose KHÔNG cải thiện đáng kể — cải tiến nằm ở tốc độ & khả năng mở rộng.)"*

## 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–8s | "EBGM được xây dựng dựa trên hệ thống Lades 1993, với 3 cải tiến" |
| 8s–18s | "Một: dùng thông tin phase để định vị điểm mốc chính xác hơn" |
| 18s–28s | "Sai số giảm từ 5.2 xuống 1.6 pixel" |
| 28s–38s | "Hai: object-adapted grids — mỗi tư thế đầu có một grid riêng" |
| 38s–48s | "Xử lý được nhiều góc chụp khác nhau" |
| 48s–58s | "Ba: FBG cho phép tìm điểm mốc của người mới chỉ trong một lần quét" |
| 58s–66s | "Điều này tăng tốc độ tính toán đáng kể với database lớn" |
| 66s–70s | "Cùng độ chính xác — nhưng nhanh hơn và linh hoạt hơn nhiều" |

## 🛠️ Manim techniques
`make_vs_card`, side-by-side mini-demos, `Transform`, repeated match animation, summary table.

---

# 📽️ SCENE 29 — EBGM VS USER-DEFINED FEATURES (Yuille) (≈ 55s)

## 🎯 Mục đích
So sánh với phương pháp thiết kế đặc trưng thủ công — nhấn mạnh khả năng "học ngoại lệ" của EBGM.

## 🎨 Visual storyboard

### Phase A (0s–10s): Setup

- Tiêu đề: **"EBGM vs Đặc trưng thủ công (Yuille, 1991)"**.
- Hiện vs-card: bên trái "HAND-CRAFTED" (YUILLE_COLOR), bên phải "EBGM" (EBGM_BRAND).

### Phase B (10s–32s): Cách Yuille hoạt động & điểm yếu

- Bên trái: visualize mô hình mắt của Yuille — **vòng tròn (iris) trong hình quả hạnh (eye outline)** + 9 tham số được điều chỉnh.
  - Vẽ tay (`Create`): almond shape + circle inside + các tham số `p1...p9`.
- **Demo thất bại:** một ảnh người đeo kính râm xuất hiện → mô hình mắt "không khớp" → glitch/shake effect → dấu ✗ coral lớn.
- Hiện code giả:
  ```
  if eyes_visible():
      fit_almond_model()
  elif sunglasses():
      # ??? phải lập trình lại từ đầu
  ```
- Label: *"Gặp ngoại lệ → phải lập trình lại thủ công."*

### Phase C (32s–50s): EBGM học ngoại lệ

- Bên phải: visualize FBG. Một ảnh người đeo kính râm xuất hiện.
- Animation: ảnh kính râm được **"thêm vào bunch"** (1 layer mới slide vào stack FBG) → graph tự động thích nghi.
- KHÔNG có code thay đổi — chỉ thêm data.
- Label: *"Chỉ cần thêm mẫu vào FBG — không động vào mã nguồn."*
- Sau khi thêm, demo: ảnh kính râm khác giờ được match thành công → dấu ✓ mint.

### Phase D (50s–55s): Chốt

- Câu chốt: *"Yuille: ngoại lệ = lập trình lại. EBGM: ngoại lệ = thêm một bức ảnh."*

## 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–8s | "Một số hệ thống dùng đặc trưng thiết kế thủ công" |
| 8s–16s | "Yuille mô hình hóa mắt bằng vòng tròn trong hình quả hạnh, 9 tham số" |
| 16s–26s | "Nhưng gặp người đeo kính râm hay nhắm mắt — mô hình thất bại" |
| 26s–34s | "Lúc đó người dùng phải lập trình lại toàn bộ thuật toán" |
| 34s–44s | "EBGM thì khác: chỉ cần thêm ảnh ngoại lệ vào Đồ thị chùm" |
| 44s–50s | "Hệ thống tự động học, không cần can thiệp mã nguồn" |
| 50s–55s | "Ngoại lệ với Yuille là lập trình lại — với EBGM chỉ là một bức ảnh" |

## 🛠️ Manim techniques
Almond+circle eye model drawing (`Create`), glitch effect (`Wiggle` + rapid position shift), FBG stack add animation, code block fake, `Transform`.

---

# 📽️ SCENE 30 — EBGM VS PCA / EIGENFACES (≈ 75s)

## 🎯 Mục đích
So sánh sâu với PCA — 2 điểm yếu của PCA (biến đổi hình học & che khuất), EBGM xử lý tốt hơn.

## 🎨 Visual storyboard

### Phase A (0s–10s): Setup

- Tiêu đề: **"EBGM vs PCA / Eigenfaces"**.
- Hiện vs-card: "PCA" (PCA_COLOR) vs "EBGM" (EBGM_BRAND).
- Note nhỏ: *"PCA: toàn bộ khuôn mặt = 1 vector. EBGM: tập hợp đặc trưng cục bộ."*

### Phase B (10s–35s): Điểm yếu 1 của PCA — Biến đổi hình học

**Recreate luận điểm "two mouths" của paper:**

- Bên trái (PCA): 
  - 2 khuôn mặt cùng người, một có miệng cao, một có miệng thấp.
  - Animation "linear combination": 2 ảnh trộn tuyến tính (`Transform` với opacity blend) → kết quả là **2 cái miệng mờ chồng lên nhau** (overlay 2 mouth shapes).
  - Mũi tên đỏ + label: *"Không nội suy ra miệng ở vị trí trung gian!"*
  - Chú thích: *"PCA tuyến tính → cần căn chỉnh ảnh chuẩn xác trước."*
  - Visualize alignment requirement: ảnh phải scale/rotate/shift để align mắt-mắt.

- Bên phải (EBGM):
  - Graph co giãn tự nhiên — node miệng tự di chuyển đến đúng vị trí.
  - Animation: graph "elastic" stretch để bám theo miệng ở các vị trí khác nhau.
  - Label: *"Cấu trúc đồ thị co giãn → tự xử lý biến đổi hình học."*

### Phase C (35s–58s): Điểm yếu 2 của PCA — Che khuất cục bộ

**Recreate luận điểm "occlusion":**

- Bên trái (PCA): 
  - 1 khuôn mặt bị tóc che một phần (hoặc có râu).
  - Vì PCA holistic, che 1 vùng → **TẤT CẢ** expansion coefficients bị ảnh hưởng.
  - Visualize: 1 thanh các hệ số `α1...α30` — khi che 1 vùng nhỏ, TẤT CẢ thanh đều "rung lệch" (đỏ).
  - Label: *"Một che khuất nhỏ làm hỏng toàn bộ biểu diễn."*

- Bên phải (EBGM):
  - Cùng khuôn mặt bị che. Nhưng EBGM dùng jets cục bộ.
  - Visualize: graph với các nodes — node ở vùng bị che (đỏ, bỏ qua), các node khác (xanh, vẫn hoạt động bình thường).
  - Label: *"Vùng bị che bỏ qua — các vùng còn lại vẫn nhận diện tốt."*

### Phase D (58s–75s): Điểm chung & honest note

- Bảng so sánh nhỏ:

| | PCA | EBGM |
|---|---|---|
| Frontal accuracy | **99%** | 98% |
| Biến đổi hình học | ✗ cần align | ✓ elastic |
| Che khuất cục bộ | ✗ holistic | ✓ local jets |
| Feature type | Eigenfaces (class-specific) | Gabor (general) |

- **Honest note (quan trọng):** *"PCA frontal HƠI cao hơn EBGM (99% vs 98%). Hai cách tiếp cận đang dần hội tụ — PCA hiện đại cũng dùng matching + local features."*
- Câu chốt: *"Khác biệt cốt lõi: Eigenfaces vs Gabor wavelets. Chưa rõ cái nào có tiềm năng phát triển hơn."*

## 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–8s | "PCA xem toàn bộ khuôn mặt như một vector lớn" |
| 8s–18s | "Điểm yếu 1: không xử lý tốt biến đổi hình học" |
| 18s–26s | "Trộn hai khuôn mặt miệng khác vị trí — chỉ ra hai miệng mờ chồng nhau" |
| 26s–34s | "PCA đòi hỏi ảnh phải được căn chỉnh chuẩn xác trước" |
| 34s–42s | "EBGM thì khác: đồ thị co giãn tự xử lý biến đổi hình học" |
| 42s–50s | "Điểm yếu 2: PCA nhạy cảm với che khuất cục bộ" |
| 50s–58s | "Một vùng bị che làm lệch toàn bộ hệ số biểu diễn" |
| 58s–66s | "EBGM dùng jets cục bộ — bỏ qua vùng che, giữ vùng còn lại" |
| 66s–75s | "PCA frontal hơi cao hơn, nhưng hai cách đang dần hội tụ" |

## 🛠️ Manim techniques
"Two mouths" overlay (ImageMobject blend / shape overlay), coefficient bar array với rung lệch, occlusion visualization, elastic graph stretch, comparison table.

---

# 📽️ SCENE 31 — EBGM VS DEFORMABLE MODELS (Lanitis) (≈ 60s)

## 🎯 Mục đích
So sánh với Lanitis 1995 — mỗi hệ có điểm mạnh riêng, tác giả đề xuất kết hợp.

## 🎨 Visual storyboard

### Phase A (0s–10s): Setup

- Tiêu đề: **"EBGM vs Deformable Models (Lanitis, 1995)"**.
- Hiện vs-card: "LANITIS" (LANITIS_COLOR) vs "EBGM" (EBGM_BRAND).
- Note: *"Hai hệ rất giống nhau — đều dùng graph matching. Khác ở 2 điểm."*

### Phase B (10s–30s): Khác biệt 1 — Mô hình biến dạng

**Distortion model:**

- Bên EBGM: **mô hình lò xo (spring model)** — nhiều bậc tự do.
  - Visualize: graph với các edges như lò xo, mỗi node tự do di chuyển → có thể tạo distortion **phi thực tế** (recreate mismatch của Figure 4: bearded man chin sai).
  - Label: *"Spring model — linh hoạt nhưng có distortion phi lý."*
  - Mini icon: cho thấy 1 graph bị méo kỳ quặc.

- Bên Lanitis: **PCA trên distortion patterns** — ít bậc tự do.
  - Visualize: chỉ một số ít "kiểu biến dạng hợp lý" được học từ PCA → matching ổn định hơn.
  - Label: *"PCA giới hạn distortion → chỉ những biến dạng hợp lý."*
  - ✓ Ưu điểm của Lanitis ở đây.

### Phase C (30s–48s): Khác biệt 2 — Local features

- Bên Lanitis: **grey-value profiles đơn giản** dọc theo đường.
  - Visualize: 1 đường thẳng với profile cường độ xám đơn giản (1D plot).
  - Label: *"Đặc trưng đơn giản — vài tham số."*

- Bên EBGM: **bunches of Gabor jets** — phức tạp, mạnh mẽ.
  - Visualize: jet stacked-disk (40 hệ số).
  - Label: *"Gabor jets — đặc trưng phong phú hơn nhiều."*
  - ✓ Ưu điểm của EBGM ở đây.

### Phase D (48s–60s): Đề xuất kết hợp

- 2 panel "merge" vào giữa với hiệu ứng `Transform`:
  - Lấy **distortion model của Lanitis** (PCA-constrained) + **Gabor jets của EBGM**.
- Hiện chữ lớn: **"Best of Both Worlds"** (lavender + glow).
- Câu chốt: *"Tác giả đề xuất: kết hợp distortion ít bậc tự do của Lanitis với Gabor jets của EBGM = hệ tối ưu."*

## 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–8s | "Lanitis 1995 rất giống EBGM — đều dùng graph matching" |
| 8s–16s | "Khác biệt 1: cách xử lý biến dạng" |
| 16s–24s | "EBGM dùng mô hình lò xo — linh hoạt nhưng có thể méo phi lý" |
| 24s–32s | "Lanitis dùng PCA giới hạn biến dạng — ổn định hơn ở điểm này" |
| 32s–40s | "Khác biệt 2: loại đặc trưng cục bộ" |
| 40s–48s | "Lanitis dùng profile xám đơn giản — EBGM dùng Gabor jets mạnh hơn" |
| 48s–56s | "Tác giả đề xuất: kết hợp cả hai điểm mạnh" |
| 56s–60s | "Distortion của Lanitis cộng Gabor jets của EBGM = hệ tối ưu" |

## 🛠️ Manim techniques
Spring model visualization (edges như lò xo), distorted graph (mismatch demo), grey-value profile plot, jet visual, merge `Transform`, glow effect.

---

# 📽️ SCENE 32 — ROTATION IN DEPTH: CÁC HƯỚNG TIẾP CẬN (≈ 80s)

## 🎯 Mục đích
Tổng quan 3 cách xử lý rotation in depth, vị trí của EBGM, và các hệ đạt 100%.

## 🎨 Visual storyboard

### Phase A (0s–12s): Đặt vấn đề

- Tiêu đề: **"Thách thức lớn nhất: Rotation in Depth"** (lavender).
- Visualize: 1 khuôn mặt xoay từ frontal → 45° → 90° (rotate animation).
- Câu hỏi: *"Làm sao nhận diện khi đầu xoay sâu trong không gian 3D?"*
- EBGM hiện tại: chỉ dùng FBG riêng cho từng góc + correspondences thủ công → kết quả chưa hoàn hảo ở góc lớn.

### Phase B (12s–62s): 3 hướng tiếp cận

Hiện 3 cards lớn, mỗi card 1 approach + kết quả:

**Approach 1 (12s–28s): Transforming Feature Vectors (Maurer & von der Malsburg)**
- Visualize: jet được "biến đổi" bằng phép biến đổi tuyến tính để compensate rotation.
- Giả định: bề mặt mặt phẳng cục bộ, texture biến đổi theo.
- Kết quả: Bochum 22°: 88% → **96%** (sau transform).
- Hạn chế: kernel có support cố định → circular region thành elliptic khi tilt → mất thông tin.
- Color: WARP_COLOR.

**Approach 2 (28s–45s): Warping Images (Vetter, Beymer & Poggio)**
- Visualize: ảnh được "warp" pixel-by-pixel từ pose này sang pose khác qua 3D-model.
- Kết quả: lên tới **100%** (trên database hoàn hảo, rendered từ 3D).
- Hạn chế: cần ảnh chất lượng cao, kém robust với che khuất/kính.
- Color: WARP_COLOR sáng hơn.

**Approach 3 (45s–62s): Linear Object Classes (Vetter & Poggio)**
- Visualize: 1 khuôn mặt được phân rã tuyến tính theo set prototype, rồi tổng hợp lại ở pose mới.
- Kết quả: **100%** (database rendered hoàn hảo).
- Hạn chế: không extrapolate tốt với loại mặt mới.
- Color: LANITIS_COLOR.

### Phase C (62s–75s): Vị trí của EBGM

- Hiện bar chart so sánh recognition rate ở góc xoay lớn (FERET 45°):
  - EBGM (no transform): **18%** (coral — thành thật về điểm yếu)
  - Maurer transform 45°→0°: **50%**
  - (Warping/Linear không test trên cùng database)
- **Honest note:** *"EBGM xử lý rotation 'cơ bản' — dùng FBG riêng + correspondences thủ công. Chưa cạnh tranh được ở góc lớn."*

### Phase D (75s–80s): Trade-off của mỗi approach

- Hiện bảng nhỏ: mỗi approach có ưu/nhược:
  - Transform features: linh hoạt nhiều biến đổi, nhưng kernel cố định giới hạn.
  - Warping: tốt với mặt mới, nhưng không xử lý illumination.
  - Linear classes: nhiều biến đổi, nhưng kém extrapolate.
- Câu chốt: *"Không hướng nào vượt trội tuyệt đối — tùy bài toán mà chọn."*

## 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–8s | "Thách thức lớn nhất: đầu xoay sâu trong không gian 3D" |
| 8s–14s | "EBGM cơ bản dùng FBG riêng cho từng góc — chưa hoàn hảo ở góc lớn" |
| 14s–24s | "Hướng 1: biến đổi feature vector để bù trừ góc xoay" |
| 24s–32s | "Maurer cải thiện Bochum 22° từ 88% lên 96%" |
| 32s–42s | "Hướng 2: warping ảnh pixel-by-pixel qua mô hình 3D" |
| 42s–50s | "Đạt tới 100% trên database hoàn hảo, nhưng cần ảnh chất lượng cao" |
| 50s–60s | "Hướng 3: phân rã tuyến tính theo các prototype" |
| 60s–70s | "Cũng đạt 100% — nhưng kém extrapolate với loại mặt mới" |
| 70s–80s | "Không hướng nào vượt trội tuyệt đối — tùy bài toán mà chọn" |

## 🛠️ Manim techniques
Face rotation animation, 3 approach cards, jet transform visualization, warping effect (mesh deform), bar chart honest comparison.

---

# 📽️ SCENE 33 — FUTURE DEVELOPMENTS: ROADMAP (≈ 90s)

## 🎯 Mục đích
Trình bày 5 hướng phát triển tương lai như một roadmap sinh động.

## 🎨 Visual storyboard

### Phase A (0s–12s): Setup roadmap

- Tiêu đề: **"Hướng phát triển tương lai"** (lavender + glow).
- Hiện một "con đường" (path/road) cong từ dưới lên, với 5 milestone nodes dọc theo — animation `Create` cho con đường.
- Câu dẫn: *"Tác giả đã vạch ra 5 hướng cải tiến."*

### Phase B (12s–80s): 5 hướng — mỗi hướng 1 milestone node

Mỗi node trên roadmap pop in tuần tự với icon + mini-demo (dùng `future_node` helper).

**Hướng 1 (12s–26s): Tối ưu mô hình biến dạng**
- Icon: lò xo → PCA constraint.
- Demo: spring model nhiều bậc tự do → giảm xuống vài "distortion pattern" hợp lý (PCA).
- Label: *"Dùng PCA giới hạn distortion → tăng độ chính xác matching."*
- Improvement note: "(Lanitis-style)"

**Hướng 2 (26s–40s): Học trọng số cho nodes**
- Icon: graph với nodes có size khác nhau.
- Demo: các nodes "quan trọng" (mang tính phân biệt cao) phình to + sáng hơn; nodes ít quan trọng mờ đi.
- Label: *"Learning weights → tập trung vào điểm mốc phân biệt cá nhân."*
- Số liệu: "Kruger 1997: rank-1 tăng từ 25% lên 31% (+6%)"

**Hướng 3 (40s–54s): Trích xuất thuộc tính**
- Icon: tag labels (sex/age/race).
- Demo: 1 khuôn mặt → các tag tự động hiện ra: "Nam", "~30 tuổi", "đeo kính".
- Label: *"Nhận diện giới tính, tuổi, chủng tộc → lọc & thu hẹp tìm kiếm."*
- Demo lọc: database lớn → chỉ search sector tương ứng → nhanh hơn.

**Hướng 4 (54s–68s): Xử lý nền phức tạp**
- Icon: face trên nền lộn xộn.
- Demo: ảnh có background phức tạp → chỉ dùng Gabor kernels nằm trong khuôn mặt (suppress background).
- Label: *"Nhận diện tốt trong môi trường nền phức tạp."*

**Hướng 5 (68s–80s): Tự động hóa 100%**
- Icon: video frames → graph tự động.
- Demo: thay vì đánh dấu fiducial points bằng tay → trích xuất FBG tự động từ chuỗi video (motion cues).
- Label: *"Loại bỏ hoàn toàn can thiệp thủ công — từ video sequences."*

### Phase C (80s–90s): Đích đến

- Camera zoom theo con đường lên đỉnh, nơi có 1 "ngôi sao/đích" lavender sáng.
- Câu chốt: *"Đích đến: một hệ thống hoàn toàn tự động, real-time, robust."*

## 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–8s | "Tác giả đã vạch ra năm hướng phát triển" |
| 8s–18s | "Một: tối ưu mô hình biến dạng bằng PCA thay vì lò xo tự do" |
| 18s–28s | "Giúp tăng độ chính xác khi khớp điểm mốc" |
| 28s–38s | "Hai: học trọng số — tập trung vào các điểm phân biệt cá nhân" |
| 38s–46s | "Đã giúp tăng recognition rate từ 25% lên 31%" |
| 46s–54s | "Ba: trích xuất thuộc tính như giới tính, tuổi, chủng tộc" |
| 54s–62s | "Để lọc và thu hẹp không gian tìm kiếm trong database lớn" |
| 62s–70s | "Bốn: nhận diện tốt trong môi trường có nền phức tạp" |
| 70s–80s | "Năm: tự động hóa hoàn toàn — trích xuất FBG từ chuỗi video" |
| 80s–90s | "Đích đến: hệ thống hoàn toàn tự động, real-time, robust" |

## 🛠️ Manim techniques
Roadmap path (`Create` curve), milestone nodes với `future_node`, node weight animation (size/glow change), attribute tags, background suppression demo, camera move along path.

---

# 📽️ SCENE 34 — SPEED OPTIMIZATION (FUTURE) (≈ 40s)

## 🎯 Mục đích
Hướng tối ưu tốc độ — 30s/graph vẫn quá chậm cho real-time.

## 🎨 Visual storyboard

### Phase A (0s–10s): Vấn đề hiện tại

- Tiêu đề: **"Vẫn còn quá chậm cho real-time"**.
- Hiện đồng hồ: "Trích xuất 1 graph = ~30 giây".
- Một icon "real-time app" (camera/video) với dấu ⏱️ → chú thích: *"30s/ảnh — không đủ cho ứng dụng thời gian thực."*

### Phase B (10s–32s): 3 cách tăng tốc

Hiện 3 giải pháp (3 mini cards):

**Cách 1 (10s–17s):** Giảm số Gabor kernels
- Visualize: jet 40 hệ số → cắt còn ít hơn (vd 20).
- Label: *"Ít kernels → tính toán nhanh hơn."*

**Cách 2 (17s–24s):** Giảm số nodes
- Visualize: graph nhiều nodes → graph ít nodes hơn.
- Label: *"Ít nodes → ít phép tính (trade-off với accuracy)."*

**Cách 3 (24s–32s):** Hardware song song
- Visualize: 1 processor → nhiều processors chạy song song (parallel architecture).
- Label: *"Kiến trúc phần cứng song song hiệu năng cao."*
- Note: *"Hệ tiền nhiệm đã được tối ưu thành công → ZN-Face commercial product chạy trên PC thường."*

### Phase C (32s–40s): Triển vọng

- Câu chốt: *"Real-time face tracking đang được phát triển — EBGM hướng tới ứng dụng thực tế."*

## 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–6s | "Một hạn chế: trích xuất một đồ thị vẫn mất khoảng 30 giây" |
| 6s–14s | "Quá chậm cho các ứng dụng thời gian thực" |
| 14s–22s | "Cách 1 và 2: giảm số Gabor kernels và số nodes" |
| 22s–32s | "Cách 3: dùng kiến trúc phần cứng song song hiệu năng cao" |
| 32s–40s | "Hệ tiền nhiệm đã thương mại hóa thành công — EBGM cũng hướng tới đó" |

## 🛠️ Manim techniques
Clock animation, jet/node reduction `Transform`, parallel processor visualization, 3 mini cards.

---

# 📽️ SCENE 35 — KẾT THÚC TOÀN VIDEO (≈ 35s)

## 🎯 Mục đích
Tổng kết toàn bộ hành trình EBGM, để lại ấn tượng cuối.

## 🎨 Visual storyboard

### Phase A (0s–15s): Recap toàn bộ hành trình

Hiện lại 4 phần của video như 4 chương, mỗi chương 1 thumbnail:

```
┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐
│ OVERVIEW   │  │ HOW IT     │  │ EXPERIMENTS│  │ DISCUSSION │
│            │  │ WORKS      │  │            │  │            │
│ [problem]  │  │ [pipeline] │  │ [98% bar]  │  │ [roadmap]  │
└────────────┘  └────────────┘  └────────────┘  └────────────┘
```

- 4 chương lần lượt lóe sáng (`Flash`) khi nhắc đến.
- Một đường nối liên kết 4 chương — "hành trình hoàn chỉnh".

### Phase B (15s–28s): Thông điệp cốt lõi

- 4 chương fade ra. Hiện 1 image graph đẹp (full, nodes với jets lấp lánh, slow rotation).
- Bên cạnh, 3 dòng thông điệp lần lượt fade in:
  > **"Cân bằng giữa thiết kế thủ công và học máy."**
  > **"Vài chục mẫu — đủ cho cả tác vụ phức tạp."**
  > **"Gần với cách con người nhận thức khuôn mặt."**

### Phase C (28s–35s): Credit & đóng

- Image graph fade ra. Hiện:
  > **ELASTIC BUNCH GRAPH MATCHING**
  > *Wiskott · Fellous · Krüger · von der Malsburg · 1999*
- Câu cuối nhỏ italic: *"Một thuật toán kinh điển — vẫn truyền cảm hứng cho face recognition hiện đại."*
- Fade to navy. Kết thúc.

## 💬 Phụ đề

| Thời điểm | Phụ đề |
|---|---|
| 0s–8s | "Chúng ta đã đi qua bốn phần: bài toán, cách hoạt động, thực nghiệm, thảo luận" |
| 8s–15s | "Từ pixel thô đến danh tính người" |
| 15s–22s | "EBGM cân bằng giữa thiết kế thủ công và học máy" |
| 22s–28s | "Chỉ vài chục mẫu — gần với cách con người nhận thức" |
| 28s–35s | "Một thuật toán kinh điển — vẫn truyền cảm hứng đến hôm nay" |

## 🛠️ Manim techniques
4-chapter recap, `Flash`, image graph slow rotation, message fade in, credits, fade to black.

---

## ✅ CHECKLIST CHO PHẦN 4

- [ ] Helper mới `make_vs_card`, `pro_item`, `con_item`, `future_node` đã test riêng.
- [ ] Tất cả con số khớp paper:
  - Matching: 5.2px → 1.6px
  - Maurer transform: 88% → 96% (Bochum 22°), 36% → 50% (FERET 45°)
  - Kruger weights: 25% → 31% (+6%)
  - EBGM FERET 45°: 18%
  - PCA frontal: 99% vs EBGM 98%
  - Warping/Linear: 100% (perfect DB)
  - Speed: ~30s/graph extraction
- [ ] Mọi mention EBGM dùng `EBGM_BRAND (#B8B5FF)`.
- [ ] Màu đối thủ công bằng (không dùng red cảnh báo).
- [ ] Honest notes được giữ (PCA hơi cao hơn, EBGM yếu ở góc xoay lớn).
- [ ] Pacing: Scene 33 (roadmap) dài nhất ~90s — đảm bảo không nhồi nhét.

---

## 🎯 GHI CHÚ ĐỊNH HƯỚNG SÁNG TẠO PHẦN 4

1. **Phần này là "phần trí tuệ"** — nhiều so sánh khái niệm. Dùng nhiều `make_vs_card`, side-by-side để khán giả thấy rõ tương phản.
2. **Trung thực là chìa khóa:** Phần Discussion của paper RẤT honest về điểm yếu của EBGM. Giữ nguyên tinh thần này — show cả chỗ EBGM thua (PCA frontal 99%, EBGM yếu góc xoay lớn). Điều này làm video uy tín.
3. **Không "dìm" đối thủ:** Mỗi hệ thống khác (Lades, Yuille, PCA, Lanitis, Vetter) đều có điểm mạnh riêng. Trình bày công bằng.
4. **Scene 31 (Lanitis) và Scene 33 (Roadmap) là 2 scene "đắt" nhất** — đầu tư effort.
5. **Roadmap (Scene 33)** nên có cảm giác "tiến về phía trước" — camera move, milestones sáng dần.
6. **Ending (Scene 35)** là cao trào cảm xúc — slow, elegant, để lại dư âm. Music swell nhẹ.
7. **Music gợi ý:** Phần này quay lại tone reflective/neo-classical như overview. Ending có thể có 1 đoạn piano swell nhẹ.

---

## 🎬 TỔNG KẾT TOÀN BỘ SERIES

| Phần | File | Scenes | Thời lượng |
|---|---|---|---|
| 1. Overview | overview.md | 1–7 | ~5:12 |
| 2. How it works | algo_detail.md | 8–18 | ~10:50 |
| 3. Experiments | efficient.md | 19–26 | ~7:25 |
| 4. Discussion | discussion.md | 27–35 | ~9:10 |

**Tổng toàn video:** ~32 phút 37 giây (có thể cắt gọn xuống 25–28 phút khi edit).

---

*End of Discussion plan. Hoàn tất plan toàn bộ video EBGM.*
