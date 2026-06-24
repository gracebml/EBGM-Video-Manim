# 🤖 Prompt cho Gemini Pro: Sản xuất Video Manim "Parzen Windows"

> **Mục đích file này:** Đây là **bộ prompt** được chia thành nhiều **batch nhỏ** để bạn (người dùng) copy-paste lần lượt vào Gemini Pro. Mỗi batch là một bước sản xuất video Manim hoàn chỉnh. Đừng đưa toàn bộ file này cho Gemini cùng lúc — agent sẽ bị quá tải. Hãy đưa **từng batch một**, đợi output, kiểm tra, rồi mới chuyển sang batch tiếp theo.

---

## 📑 Mục lục

- [Hướng dẫn sử dụng](#-hướng-dẫn-sử-dụng)
- [Tài liệu tham khảo bắt buộc](#-tài-liệu-tham-khảo-bắt-buộc-đưa-cho-gemini-trước-batch-0)
- [BATCH 0 — Setup & Infrastructure](#-batch-0--setup--infrastructure)
- [BATCH 1 — Scene 1+2: Hook & Bridge](#-batch-1--scene-12-hook--bridge)
- [BATCH 2 — Scene 3+4: Parametric fail & Histogram](#-batch-2--scene-34-parametric-fail--histogram)
- [BATCH 3 — Scene 5: Trái tim của Parzen](#-batch-3--scene-5-trái-tim-của-parzen)
- [BATCH 4 — Scene 6: Bandwidth h](#-batch-4--scene-6-bandwidth-h)
- [BATCH 5 — Scene 7: Công thức & hội tụ](#-batch-5--scene-7-công-thức--hội-tụ)
- [BATCH 6 — Scene 8+9: Ứng dụng & Mở rộng](#-batch-6--scene-89-ứng-dụng--mở-rộng)
- [BATCH 7 — Scene 10 & Tích hợp](#-batch-7--scene-10--tích-hợp)
- [BATCH FINAL — Render & QA](#-batch-final--render--qa)

---

## 📖 Hướng dẫn sử dụng

1. **Lần đầu:** Copy phần **"Tài liệu tham khảo bắt buộc"** vào Gemini Pro để khởi tạo context. Đây là phần "system prompt" để Gemini biết phong cách & quy ước.
2. **Mỗi batch sau đó:** Copy nguyên block `## BATCH X` (từ tiêu đề đến hết block code cuối của batch đó). Đợi Gemini sinh code, lưu vào file `.py`, test bằng `manim -pql` (preview low quality).
3. **Nếu có lỗi:** Quote lại lỗi cho Gemini, yêu cầu fix. Đừng nhảy batch.
4. **Cuối cùng:** Chạy `BATCH FINAL` để render full quality và làm checklist.

> 💡 **Lưu ý:** Mọi batch giả định bạn đã đưa **file kịch bản gốc** (`kich_ban_parzen_windows.md`) cho Gemini. Nếu bạn dùng phiên Gemini mới, hãy đưa lại kịch bản đó **trước batch đầu**.

---

## 📚 Tài liệu tham khảo bắt buộc (đưa cho Gemini TRƯỚC Batch 0)

```
Bạn là một chuyên gia sản xuất video giáo dục bằng Manim Community Edition (ManimCE) v0.18+. Bạn sẽ giúp tôi sản xuất một video 9 phút về thuật toán Parzen Windows theo phong cách 3Blue1Brown (Grant Sanderson).

## Tài liệu tham khảo BẮT BUỘC nghiên cứu trước khi viết code:

### 1. Source code chính thức của 3Blue1Brown
- Repo videos thật: https://github.com/3b1b/videos
  → Đặc biệt nghiên cứu các thư mục: `_2024/`, `_2025/`, `_2026/ ` (style mới nhất) (folder `videos/`)
  → Các video gợi ý đọc kỹ: "neural networks", "convolutions", "bayes theorem"
- Repo Manim của Grant: https://github.com/3b1b/manim (ManimGL — chỉ tham khảo style, KHÔNG copy import) (folder `manim-GL/`)
- Manim Community (cái ta dùng): https://github.com/ManimCommunity/manim (folder `manim/`)
- Docs ManimCE: https://docs.manim.community/

### 2. Đặc trưng phong cách 3Blue1Brown cần bắt chước
- Nền tối: dark navy `#0F1419` (KHÔNG dùng đen tuyền)
- Bảng màu hạn chế: BLUE_C, BLUE_D, YELLOW, RED_C, GREEN, GREY_BROWN
- Mọi text giải thích đứng riêng, KHÔNG đè lên animation chính
- Mọi đối tượng xuất hiện qua `FadeIn`, `Write`, `Create` — KHÔNG bao giờ "pop" đột ngột
- Dùng `LaggedStart` thay vì `AnimationGroup` khi muốn các phần tử xuất hiện tuần tự
- Công thức LaTeX dùng `MathTex` với từng phần được tô màu riêng bằng `set_color_by_tex`
- Camera đôi khi zoom/pan bằng `MovingCameraScene` — KHÔNG lạm dụng
- Transition giữa concept dùng `TransformMatchingTex` hoặc `ReplacementTransform`
- Khoảng nghỉ giữa các bước animation: `self.wait(0.5)` đến `self.wait(1.5)` — không bao giờ 0

### 3. Quy ước project CỦA TÔI
- Tên file: `scene_XX_<short_name>.py` (vd: `scene_05_kernel_sum.py`)
- Mỗi scene là 1 class kế thừa `Scene` hoặc `MovingCameraScene`
- File `config.py` chung chứa: màu sắc, font, helper functions
- File `assets/` chứa SVG chữ ký, ảnh khuôn mặt nếu cần
- Khi sinh code, LUÔN bao gồm: docstring, comment tiếng Việt cho mỗi đoạn animation lớn, type hints cho helper
- Sau mỗi scene, ĐOÁN thời gian chạy (`self.wait()` cộng dồn) và in ra console comment

### 4. Khi nào KHÔNG dùng cái gì
- KHÔNG dùng `ManimGL` (cái của Grant) — chỉ ManimCE
- KHÔNG dùng `manim_voiceover` trong giai đoạn đầu (sẽ thêm sau)
- KHÔNG generate hình ảnh bằng AI — dùng SVG/PNG có sẵn hoặc tạo bằng VMobject
- KHÔNG hardcode đường dẫn tuyệt đối — dùng `Path(__file__).parent / "assets"`

### 5. Ngôn ngữ output
- Comment trong code: tiếng Việt
- Tên biến/hàm: English (snake_case)
- Text hiển thị trên video: tiếng Việt (dùng font "Be Vietnam Pro" hoặc "Inter")
- Câu hỏi/đề xuất với tôi: tiếng Việt

Bạn ĐÃ HIỂU và sẵn sàng? Trả lời "Sẵn sàng nhận Batch 0" để tôi gửi batch đầu tiên.
```

---

## 🔧 BATCH 0 — Setup & Infrastructure

> **Mục tiêu:** Tạo bộ khung project, file config chung, helper functions tái sử dụng cho mọi scene.

```
BATCH 0: Tạo infrastructure cho project Manim "Parzen Windows Video"

## Yêu cầu
Sinh ra các file sau (trả về dưới dạng code block riêng cho từng file):

### File 1: `requirements.txt`
- manim>=0.18.0
- numpy
- scipy (cho hàm scipy.stats.norm)
- (KHÔNG cần thêm gì khác)

### File 2: `config.py`
Chứa:
1. Bảng màu — đặt biến giống convention 3B1B nhưng custom cho project:
   - `BG_COLOR = "#0F1419"`
   - `TEXT_PRIMARY = "#ECECEC"`
   - `ACCENT_BLUE = "#5DADE2"` (cho khái niệm/data)
   - `ACCENT_YELLOW = "#F1C40F"` (cho highlight chính)
   - `ACCENT_RED = "#E74C3C"` (cho cảnh báo, GIẢ MẠO)
   - `ACCENT_GREEN = "#2ECC71"` (cho đúng/THẬT)
   - `ACCENT_PURPLE = "#9B59B6"` (cho công thức)
   - `MUTED = "#7F8C8D"` (cho citation, text phụ)

2. Font setup:
   - `FONT_VIET = "Be Vietnam Pro"` (fallback: "Inter", "Arial")
   - `FONT_MATH = "CMU Serif"` (mặc định của MathTex)

3. Sizes chuẩn:
   - `SIZE_TITLE = 56`
   - `SIZE_HEADER = 40`
   - `SIZE_BODY = 28`
   - `SIZE_CAPTION = 20`
   - `SIZE_CITE = 16`

4. Setup mặc định cho Scene:
   ```python
   from manim import config
   config.background_color = BG_COLOR
   config.frame_rate = 60
   ```

### File 3: `helpers.py`
Chứa các hàm tiện ích:

1. `gaussian_kernel(x, mu, h)` — kernel Gaussian 1D có normalize.
   - Type hints đầy đủ
   - Docstring giải thích vai trò trong Parzen

2. `parzen_density(x, data_points, h)` — tính ước lượng Parzen tại điểm x cho list điểm dữ liệu.

3. `get_parzen_curve(axes, data_points, h, color)` → trả về `axes.plot(...)` của đường mật độ Parzen.

4. `create_data_dots(axes, data_points, color=WHITE, radius=0.06)` → trả về `VGroup` các `Dot` đặt trên trục x.

5. `create_method_card(short_name, full_name, color, highlight=False)` → trả về `VGroup` (Rectangle + 2 Text) — dùng cho Scene 2.

6. `make_callout(text, color, size=24)` → Text với background mờ nhẹ phía sau (kiểu callout của 3B1B).

### File 4: `README.md` (cho project)
Tóm tắt cấu trúc, cách chạy:
```
manim -pql scene_01_hook.py HookScene
manim -pqh scene_01_hook.py HookScene  # high quality
```

### Validation cho Batch 0
- [ ] 4 files được tạo
- [ ] `config.py` import được từ scene file mẫu
- [ ] Helper `gaussian_kernel(0, 0, 1)` cho ra ≈ 0.3989 (test mental math)
- [ ] Mọi hàm có docstring tiếng Việt
- [ ] KHÔNG có import dư thừa

Sau khi sinh xong, hãy:
1. Hỏi tôi có muốn điều chỉnh màu/font không
2. Đề xuất 1 file `scene_00_test.py` tối thiểu để verify setup hoạt động (chỉ hiện chữ "Hello Parzen" với đúng màu/font)
```

---

## 🎬 BATCH 1 — Scene 1+2: Hook & Bridge

> **Mục tiêu:** Hai scene đầu tiên — chữ ký thật/giả + chuyển tiếp vào Parzen.

```
BATCH 1: Sinh code Manim cho Scene 1 (Hook) và Scene 2 (Bridge)

## Bối cảnh
- Đã hoàn thành Batch 0: có config.py, helpers.py
- Tham khảo lại file kịch bản: Scene 1 (0:00-0:45) và Scene 2 (0:45-1:30)

## Yêu cầu

### File: `scene_01_hook.py`
Class `HookScene(Scene)`:

1. Frame 1 (0-3s): nền đen, vẽ chữ ký 1 từ trái sang phải bằng `Create` với run_time=2.
   - Vì ta CHƯA có SVG thật, dùng `VMobject` mô phỏng chữ ký bằng đường cong Bezier ngẫu nhiên
   - Hoặc dùng `Text("Nguyễn Văn A", font="Brush Script MT", slant=ITALIC)` để giả lập
   - Caption "của bạn" bên dưới (font size SIZE_CAPTION)

2. Frame 2 (3-6s): dịch chữ ký 1 sang trái (LEFT*3), vẽ chữ ký 2 bên phải tương tự.
   - Hai chữ ký phải hơi khác nhau (ví dụ rotate 5 độ hoặc scale 0.95)

3. Frame 3 (6-9s): chữ ký 2 chuyển dần sang ACCENT_RED, hiện label "GIẢ MẠO" với hiệu ứng `FadeIn(scale=1.5)`.

4. Frame 4 (9-12s): mọi thứ collapse về 1 dấu `?` lớn (font_size=200, ACCENT_YELLOW) ở giữa.
   - Dùng `Transform(VGroup(...), question_mark)`

5. KẾT THÚC scene: fade out toàn bộ, để lại nền đen 0.5s

### File: `scene_02_bridge.py`
Class `BridgeScene(Scene)`:

1. Frame 1 (0-3s): 4 method cards xếp ngang ở giữa màn hình.
   - Card 1: "DTW" / "Dynamic Time Warping" — BLUE
   - Card 2: "HMM" / "Hidden Markov Model" — BLUE
   - Card 3: "NN" / "Neural Network" — BLUE
   - Card 4: "Parzen" / "Parzen Windows" — YELLOW + highlight=True
   - Dùng `LaggedStartMap(FadeIn, cards, lag_ratio=0.3)`

2. Frame 2 (3-7s):
   - 3 card đầu opacity → 0.2 đồng thời card 4 phóng to 1.8x và di chuyển về ORIGIN
   - Dùng `AnimationGroup(*[c.animate.set_opacity(0.2) for c in cards[:3]], cards[3].animate.scale(1.8).move_to(ORIGIN))`

3. Frame 3 (7-10s): hiện subtitle dưới card Parzen
   - Text: "không cần giả định phân phối"
   - Color: ACCENT_BLUE
   - Animation: `FadeIn(subtitle, shift=UP*0.3)`
   - Đợi 2s rồi fade out

## Yêu cầu chung
- Tổng thời lượng Scene 1: ~12s (gần với target 45s — sẽ pad bằng narration sau)
- Tổng thời lượng Scene 2: ~10s
- Đảm bảo có `self.wait(...)` hợp lý giữa các frame
- Comment tiếng Việt mô tả từng frame

## 3B1B Style Notes cho batch này
- Trong các video về proof/math, Grant thường mở đầu bằng 1 dấu hỏi lớn ở giữa — hãy bắt chước đoạn Frame 4 Scene 1
- Card layout giống video "Why π is in the normal distribution" — nghiên cứu code repo `_2023/clt/main.py` nếu có thể

## Validation
- [ ] Cả 2 file chạy được với `manim -pql`
- [ ] Không có warning về font (nếu Be Vietnam Pro không có, fallback sang Inter)
- [ ] Transition giữa 4 frame mượt, không nhảy
- [ ] In ra console: tổng thời lượng dự kiến của mỗi scene

Sau khi xong, đề xuất với tôi: nên dùng SVG chữ ký thật (tôi cung cấp file) hay tiếp tục với mock?
```

---

## 🎬 BATCH 2 — Scene 3+4: Parametric fail & Histogram

> **Mục tiêu:** Hai scene về vấn đề của parametric và histogram ngây thơ.

```
BATCH 2: Sinh code Manim cho Scene 3 (Parametric fails) và Scene 4 (Histogram)

## Bối cảnh
- Hoàn thành Batch 0, 1
- Scene 3 (1:30-2:30) và Scene 4 (2:30-3:15) trong kịch bản

## Yêu cầu

### File: `scene_03_parametric_fails.py`
Class `ParametricFailsScene(Scene)`:

1. Frame 1: tạo `Axes` x_range=[-4,4], y_range=[0, 0.6] đặt giữa màn hình.
   - Vẽ Gaussian chuẩn (mean=0, std=1) màu ACCENT_BLUE
   - Label trên trái: "Mô hình tham số: Gaussian"
   - Đợi 1.5s

2. Frame 2: scatter 150 điểm dữ liệu "thật" rút từ phân phối bimodal:
   ```python
   true_pdf = lambda x: 0.4*norm.pdf(x,-1.5,0.4) + 0.5*norm.pdf(x,1,0.7) + 0.1*norm.pdf(x,2.5,0.3)
   ```
   - Mỗi điểm là 1 `Dot` nhỏ (radius=0.04), đặt trên trục x với y=0
   - Hiện scatter dần với `LaggedStartMap(FadeIn, dots, lag_ratio=0.005)` (xuất hiện trong ~1.5s)

3. Frame 3: vẽ đường mật độ THẬT (true_pdf) màu ACCENT_YELLOW, đè lên Gaussian giả định
   - Dùng `axes.plot(true_pdf)` với `stroke_width=4`
   - Khán giả thấy ngay: Gaussian không khớp data

4. Frame 4: tô vùng "lệch" giữa 2 đường cong màu ACCENT_RED, opacity 0.4
   - Dùng `axes.get_area(curve1, [x_min, x_max], bounded_graph=curve2, color=RED)`
   - Đây là khoảnh khắc "model sai" — đợi 2s để khán giả ngấm

5. Frame 5: ở góc dưới, hiện text trích dẫn:
   ```
   "Classical parametric densities are unimodal,
   but many practical problems involve
   multimodal densities."
                — Duda, Hart & Stork (2001)
   ```
   - Italic, font_size=22, ACCENT_BLUE
   - Citation dưới cùng, ACCENT_MUTED, size 16
   - Dùng `Write` cho text, `FadeIn` cho citation

### File: `scene_04_histogram.py`
Class `HistogramScene(Scene)`:

1. Frame 1: tạo trục số 1D (chỉ x-axis, từ -3 đến 3), scatter 40 điểm có distribution bimodal (cùng bộ với Scene 3 nhưng ít hơn).

2. Frame 2: dần dần dựng histogram lên:
   - bin_width = 0.5
   - Mỗi bin là một `Rectangle` mọc lên từ y=0
   - Sequential animation: bin trái trước → bin phải sau (`LaggedStartMap`)
   - Tổng thời lượng dựng histogram: 2s

3. Frame 3: highlight đường viền histogram bằng `ACCENT_RED` để nhấn mạnh sự gồ ghề
   - Dùng `VMobject` với path là đường gấp khúc nối các đỉnh bin
   - `ShowCreation` đường viền này trong 1s

4. Frame 4 (QUAN TRỌNG): animate slider bin_width thay đổi
   - Tạo `ValueTracker(bin_width)`
   - Histogram tự cập nhật theo `bin_width` qua `.add_updater(...)`
   - Animate: `self.play(bin_width_tracker.animate.set_value(0.2), run_time=1.5)`
   - Rồi: `set_value(1.2)`, `set_value(0.4)` — tổng 3 lần thay đổi
   - Hiện text bên trên: "Cùng dữ liệu — nhiều histogram khác nhau!"

5. Frame 5: fade out histogram, để lại chỉ scatter, đợi 0.5s rồi chuyển scene

## Yêu cầu kỹ thuật
- Scene 3: tổng ~15s
- Scene 4: tổng ~12s
- Phải dùng `ValueTracker` + `add_updater` cho slider — đây là kỹ thuật quan trọng của 3B1B (xem `_2022/learning/main.py` repo 3b1b/videos để có inspiration)

## 3B1B Style Notes
- Vùng đỏ giữa 2 curves: làm opacity 0.4, KHÔNG quá đậm
- Citation cuối Scene 3 giống Grant để credit Tao Te Ching trong video chaos theory
- Histogram bins nên có border `WHITE` mỏng (stroke_width=1) để tách bin với nhau

## Validation
- [ ] Slider trong Scene 4 thay đổi mượt mà
- [ ] Vùng đỏ trong Scene 3 hiển thị đúng (không overflow ra ngoài curves)
- [ ] Text trích dẫn không bị wrap xấu
- [ ] Đảm bảo dùng cùng RNG seed cho data points để consistency giữa Scene 3 và 4

Sau khi xong, hỏi tôi: có muốn render Scene 1-4 cùng nhau preview trước khi sang Scene 5 không?
```

---

## 🎬 BATCH 3 — Scene 5: Trái tim của Parzen

> **Mục tiêu:** Scene quan trọng nhất — đặt kernel ở mỗi điểm rồi cộng dồn.

```
BATCH 3: Sinh code Manim cho Scene 5 — "Trái tim của Parzen"

## CẢNH BÁO ĐẶC BIỆT
Đây là scene CỐT LÕI của video — quyết định tính "viral" và educational value. Hãy đầu tư thời gian. Animation phải mượt mà, từ tốn, có nhịp điệu rõ ràng.

## Tham khảo
- Kịch bản: Scene 5 (3:15 - 4:30)
- Style reference: video 3B1B "But what is the Central Limit Theorem?" — đoạn cộng các phân phối thành Gaussian. Tải về repo 3b1b/videos `_2023/clt/` để học cách Grant animate sum of distributions.
- Cũng tham khảo: video "Convolutions" của 3B1B — animation "trượt + nhân + cộng" rất giống Parzen

## Yêu cầu

### File: `scene_05_kernel_sum.py`
Class `KernelSumScene(Scene)`:

#### Phần 1 (0-5s): Data points xuất hiện
- Tạo `Axes` x_range=[-3, 3], y_range=[0, 0.8]
- 5 data points cố định: `x_data = [-1.5, -0.5, 0.2, 1.3, 2.1]`
- Mỗi điểm là `Dot` (color=WHITE, radius=0.08) tại y=0 trên axes
- Cùng xuất hiện với một `Cross` tick nhỏ trên trục x ngay dưới mỗi dot
- Dùng `LaggedStartMap(GrowFromCenter, dots, lag_ratio=0.15)`

#### Phần 2 (5-15s): Đặt kernel TỪNG ĐIỂM một
Đây là phần CHẬM RÃI nhất. Mỗi kernel:
1. Pulse vào dot tương ứng (highlight nó 0.3s)
2. Vẽ một Gaussian nhỏ trên đó với `Create`, run_time=1.5s
3. Kernel có: mu=x_data[i], h=0.4, color tăng dần qua color wheel:
   - Kernel 1: BLUE_C
   - Kernel 2: TEAL
   - Kernel 3: GREEN
   - Kernel 4: YELLOW
   - Kernel 5: ORANGE

Lời thoại đồng bộ (commented in code):
- Kernel 1: "Một quả chuông tại điểm thứ nhất..."
- Kernel 2: "Thêm một cái nữa tại điểm thứ hai..."
- Kernel 3-5: "...và tiếp tục..."

```python
# Pseudocode mong muốn:
kernels = []
for i, x_i in enumerate(x_data):
    self.play(Indicate(dots[i], color=YELLOW), run_time=0.3)
    kernel_i = axes.plot(
        lambda x, mu=x_i: gaussian_kernel(x, mu, h=0.4) / len(x_data),
        color=color_palette[i],
        stroke_width=2.5
    )
    self.play(Create(kernel_i), run_time=1.5)
    kernels.append(kernel_i)
    self.wait(0.3)
```

#### Phần 3 (15-22s): KHOẢNH KHẮC WOW — cộng dồn
1. Đợi 1s sau khi kernel cuối xuất hiện
2. Vẽ đường tổng (sum_curve) MỜ trước (opacity 0.3, BLUE_D, stroke_width=5):
   ```python
   sum_curve = get_parzen_curve(axes, x_data, h=0.4, color=BLUE_D).set_opacity(0.3)
   self.add(sum_curve)
   ```
3. Animate 5 kernels "tan chảy" vào sum_curve:
   - Dùng `Transform(VGroup(*kernels), sum_curve)` với run_time=2.5
4. Sau khi transform xong: tăng opacity sum_curve lên 1.0 + tô màu sáng ACCENT_YELLOW
   - `self.play(sum_curve.animate.set_opacity(1).set_color(ACCENT_YELLOW).set_stroke(width=6))`

#### Phần 4 (22-30s): Công thức xuất hiện
- Đẩy axes sang trái 2 đơn vị
- Bên phải hiện công thức:
  ```python
  formula = MathTex(
      r"\hat{p}_n(x) = \frac{1}{n}\sum_{i=1}^{n} \frac{1}{h_n}\,\varphi\!\left(\frac{x - x_i}{h_n}\right)"
  ).scale(0.9)
  ```
- Tô màu từng phần bằng `set_color_by_tex`:
  - `\frac{1}{n}` → BLUE_C (caption: "trung bình")
  - `\varphi` → ACCENT_YELLOW (caption: "kernel")
  - `\frac{x - x_i}{h_n}` → ORANGE (caption: "chuẩn hóa khoảng cách")
- Highlight từng phần lần lượt với `Indicate` + caption pop lên dưới công thức 1.5s, rồi biến mất

## Yêu cầu chuyên sâu
- Mọi animation trong Phần 3 phải dùng `rate_func=smooth` hoặc `there_and_back_with_pause`
- Sau Phần 3, để khán giả "ngấm" — đợi `self.wait(2)` trước khi sang Phần 4
- Tổng độ dài scene: ~30-35s

## 3B1B Style Notes
- Trong video "Convolutions", Grant dùng kỹ thuật MỘT kernel "trượt" để minh họa convolution. Ở đây ta KHÔNG trượt — ta đặt CỐ ĐỊNH ở mỗi điểm. Hãy chắc chắn agent hiểu sự khác biệt.
- Khi 5 kernels "tan" thành 1 đường tổng: nên có hiệu ứng "ánh sáng" — có thể thêm `Flash` ở đỉnh đường tổng sau khi transform xong.
- Công thức cuối: dùng cùng template formula của 3B1B trong video "What is backpropagation really doing?" — các phần được tô màu riêng biệt.

## Validation NGHIÊM NGẶT
- [ ] Đoạn cộng dồn 5 kernels mượt — không jerky
- [ ] Mỗi kernel có MÀU RIÊNG biệt rõ rệt (không phải các tone xanh gần giống nhau)
- [ ] Công thức LaTeX render đúng (`\varphi`, không phải `\phi`)
- [ ] Caption tiếng Việt nằm trong vùng an toàn (không cắt vào axes)
- [ ] Test bằng `manim -pqm scene_05_kernel_sum.py KernelSumScene` (medium quality)

Sau khi sinh code, đề xuất với tôi 2 phương án khác nhau cho đoạn "cộng dồn" (Phần 3) và để tôi chọn:
1. Phương án A: 5 kernels Transform thẳng vào sum_curve
2. Phương án B: 5 kernels "rơi" xuống và tích lũy thành sum_curve qua từng bước
```

---

## 🎬 BATCH 4 — Scene 6: Bandwidth h

> **Mục tiêu:** 3-cột so sánh h khác nhau + slider tương tác.

```
BATCH 4: Sinh code Manim cho Scene 6 — Bandwidth h và Bias-Variance Trade-off

## Bối cảnh
- Hoàn thành Batch 0-3
- Scene 6 (4:30-5:45) trong kịch bản

## Yêu cầu

### File: `scene_06_bandwidth.py`

Class `BandwidthCompareScene(Scene)`:

#### Phần 1 (0-12s): 3 cột so sánh
Tạo 3 axes nhỏ xếp ngang, cùng dùng 5 data points như Scene 5 (giữ consistency!):
- Cột trái: h=2.0 (under-fit) — đường cong gần phẳng
- Cột giữa: h=0.4 (vừa) — đường cong 2-3 đỉnh đẹp
- Cột phải: h=0.1 (over-fit) — đường cong gai góc

Mỗi cột có:
- Axes cá nhân (scale ~0.4)
- Data points (cùng 5 điểm)
- Đường mật độ Parzen tương ứng
- Title trên đầu mỗi cột:
  - Cột trái: "h = 2.0" (color ACCENT_RED, caption "QUÁ MƯỢT")
  - Cột giữa: "h = 0.4" (color ACCENT_GREEN, caption "VỪA ĐẸP")
  - Cột phải: "h = 0.1" (color ACCENT_RED, caption "QUÁ GAI")
- Cột giữa thêm khung viền `SurroundingRectangle(color=GREEN, buff=0.2)`
- Cột trái + phải có khung viền RED mờ

Animation order:
1. Tạo 3 axes cùng lúc (FadeIn lag 0.2)
2. Data dots xuất hiện ở cả 3 cột đồng thời
3. Vẽ 3 đường Parzen TỪ TRÁI sang PHẢI bằng `LaggedStartMap(Create, curves, lag_ratio=0.5)`
4. Titles + frames xuất hiện cùng lúc cuối

#### Phần 2 (12-20s): Slider INTERACTIVE
Đây là phần đỉnh cao của scene. Phải bám sát kỹ thuật `ValueTracker`:

```python
# Pseudocode
self.play(*[FadeOut(c) for c in three_columns])  # clear 3 cột

# Một axes duy nhất ở giữa, lớn
big_axes = Axes(x_range=[-3,3], y_range=[0, 1.0])
big_dots = create_data_dots(big_axes, x_data)
self.play(Create(big_axes), FadeIn(big_dots))

# ValueTracker cho h
h_tracker = ValueTracker(0.4)

# Đường Parzen tự cập nhật
parzen_curve = always_redraw(
    lambda: get_parzen_curve(big_axes, x_data, h=h_tracker.get_value(), color=ACCENT_YELLOW)
)
self.add(parzen_curve)

# Slider visual ở dưới
h_slider_track = NumberLine(x_range=[0.05, 2.0, 0.1], length=8).to_edge(DOWN, buff=1)
h_slider_dot = always_redraw(
    lambda: Dot(h_slider_track.n2p(h_tracker.get_value()), color=ACCENT_YELLOW, radius=0.15)
)
self.add(h_slider_track, h_slider_dot)

# Label "h = X.XX" cập nhật theo tracker
h_label = always_redraw(
    lambda: MathTex(f"h = {h_tracker.get_value():.2f}").next_to(h_slider_dot, UP)
)
self.add(h_label)

# Animate slider: 0.4 → 1.5 → 0.1 → 0.4
self.play(h_tracker.animate.set_value(1.5), run_time=2.5, rate_func=smooth)
self.wait(0.5)
self.play(h_tracker.animate.set_value(0.1), run_time=2.5, rate_func=smooth)
self.wait(0.5)
self.play(h_tracker.animate.set_value(0.4), run_time=1.5, rate_func=smooth)
```

#### Phần 3 (20-25s): Cross-validation note
- Bên phải màn hình, hiện một sơ đồ nhỏ:
  - Rectangle dài "Train (80%)" — BLUE
  - Rectangle nhỏ "Val (20%)" — ORANGE
  - Mũi tên: "→ chọn h tối ưu"
- Caption: "Trong thực tế: dùng cross-validation"
- Reference (font nhỏ, MUTED): "Duda et al., §4.3.6"

## 3B1B Style Notes
- Slider animation = signature của 3B1B (xem video "What is a Fourier series?" về phần slider tham số)
- Khi slider chạy, đường Parzen biến đổi LIÊN TỤC — đây là `always_redraw` magic
- KHÔNG thêm âm thanh "ting" khi tracker thay đổi (Manim không hỗ trợ tốt việc này)
- Slider track dùng style "minimalist": NumberLine với tick mark rất nhẹ

## Yêu cầu Kỹ thuật
- `always_redraw` PHẢI được dùng cho parzen_curve, slider dot, và label — KHÔNG dùng `add_updater` riêng lẻ
- Cẩn thận với `lambda` capture: dùng default argument trick để tránh closure bug
- Sau scene, fade out toàn bộ trừ data points (để Scene 7 dùng tiếp)

## Validation
- [ ] Slider mượt mà, không có frame nhảy
- [ ] Đường Parzen biến đổi đúng khi h thay đổi (test với h=0.1 phải thấy nhiều đỉnh nhọn)
- [ ] Label `h = X.XX` cập nhật real-time
- [ ] 3 cột so sánh ở Phần 1 cùng scale, không cái nào "to" hơn cái khác
- [ ] Tổng thời lượng ~25s

Sau khi xong, đề xuất: có nên thêm âm thanh slider (whoosh) qua external editing không?
```

---

## 🎬 BATCH 5 — Scene 7: Công thức & hội tụ

> **Mục tiêu:** Phương trình tổng quát, 3 điều kiện hội tụ, animation hội tụ.

```
BATCH 5: Sinh code Manim cho Scene 7 — Công thức tổng quát & Tính nhất quán

## Bối cảnh
- Hoàn thành Batch 0-4
- Scene 7 (5:45-6:30) trong kịch bản

## Yêu cầu

### File: `scene_07_convergence.py`

Class `ConvergenceScene(Scene)`:

#### Phần 1 (0-8s): Phương trình lớn ở giữa

```python
formula = MathTex(
    r"\hat{p}_n(\mathbf{x}) = ",
    r"\frac{1}{n}",
    r"\sum_{i=1}^{n}",
    r"\frac{1}{V_n}\,",
    r"\varphi\!\left(",
    r"\frac{\mathbf{x} - \mathbf{x}_i}{h_n}",
    r"\right)"
).scale(1.3)
```

Tô màu từng phần bằng index:
- `formula[1]` (1/n): BLUE_C
- `formula[3]` (1/V): PURPLE
- `formula[4]` (φ): YELLOW
- `formula[5]` ((x-xi)/h): ORANGE

Animation:
1. Write formula từng phần (chậm) — dùng `Write` với run_time=3
2. Sau khi đầy đủ: `Indicate` từng phần theo thứ tự, kèm caption pop dưới:
   - 1/n → "trung bình của n cửa sổ"
   - 1/V → "chuẩn hóa theo thể tích"
   - φ → "hàm cửa sổ (kernel)"
   - (x-xi)/h → "khoảng cách chuẩn hóa"
3. Mỗi caption hiển thị 1.2s, ẩn đi, mới tới phần tiếp theo

#### Phần 2 (8-15s): Ba điều kiện hội tụ

Đẩy formula lên đỉnh, scale 0.7.

Hiện title: "Khi nào ước lượng HỘI TỤ về phân phối thật?"

Hiện 3 điều kiện xếp dọc dưới title:

```python
cond1 = MathTex(r"\lim_{n \to \infty} V_n = 0")  # Volume → 0
cond2 = MathTex(r"\lim_{n \to \infty} k_n = \infty")  # Số sample trong vùng → ∞
cond3 = MathTex(r"\lim_{n \to \infty} \frac{k_n}{n} = 0")  # Nhưng tỉ lệ → 0
```

Bên phải mỗi điều kiện, có caption nhỏ giải thích trực giác (font size 20, MUTED):
- Cond 1: "Vùng cửa sổ co lại"
- Cond 2: "Đủ mẫu trong cửa sổ"
- Cond 3: "Nhưng vẫn là phần nhỏ của tổng"

Animation: `LaggedStartMap(FadeIn, conditions, lag_ratio=0.5)`

Reference dưới cùng (font size 14, MUTED):
```
"Duda, Hart & Stork — Pattern Classification, §4.2 (trang 163)"
```

#### Phần 3 (15-22s): Hội tụ visualization

Đây là phần WOW của scene. Xóa hết, tạo một axes mới.

True density:
```python
true_pdf = lambda x: 0.5*norm.pdf(x, -1, 0.5) + 0.5*norm.pdf(x, 1, 0.5)
true_curve = axes.plot(true_pdf, color=WHITE, stroke_opacity=0.4, stroke_width=2)
self.add(true_curve)
```

Title: "n = ?" ở góc trên trái (sẽ thay đổi)

Loop 4 lần với n = [1, 10, 100, 1000]:
1. Sample n điểm từ true_pdf (dùng `np.random.choice` với weights)
2. Tạo đường Parzen với h = h_n = 1/sqrt(n) (như sách Duda)
3. `Transform` đường Parzen cũ thành mới (run_time=1.5)
4. Cập nhật label "n = X"
5. Wait 1s

Sau vòng lặp:
- Đường Parzen overlap gần như hoàn toàn với true_curve
- Hiện text "n = ∞" và caption: "Hội tụ về MỌI phân phối liên tục" (color GREEN, large)

## 3B1B Style Notes
- Phần highlight công thức bằng `Indicate` + caption là kỹ thuật chuẩn của Grant (xem "What is backpropagation really doing?")
- Đoạn convergence visualization (n tăng dần) tham khảo trực tiếp Figure 4.5 trang 169 và Figure 4.7 trang 171 của Duda — bạn nên đọc lại để hiểu mong đợi
- Khi text "n = ∞" xuất hiện, dùng hiệu ứng `FadeIn(scale=2)` cho dramatic effect

## Validation
- [ ] LaTeX render đẹp, không có lỗi compile (test với `manim --renderer=cairo`)
- [ ] Reference Duda hiển thị đúng định dạng học thuật
- [ ] Đường Parzen tại n=1000 khớp tốt với true_pdf
- [ ] Tổng thời lượng ~22s
- [ ] RNG seed cố định cho phần sample n điểm — để consistency giữa các run

Sau scene này, kiểm tra tổng thời lượng Scene 1-7: phải đạt ~5:30 (gần với target 6:30 trừ phần overhead voice-over)
```

---

## 🎬 BATCH 6 — Scene 8+9: Ứng dụng & Mở rộng

> **Mục tiêu:** Đóng vòng với chữ ký + mở rộng sang biometric khác + PNN.

```
BATCH 6: Sinh code Manim cho Scene 8 (Ứng dụng chữ ký) và Scene 9 (Vượt khỏi chữ ký)

## Bối cảnh
- Hoàn thành Batch 0-5
- Scene 8 (6:30-7:30) và Scene 9 (7:30-8:30) trong kịch bản

## Yêu cầu

### File: `scene_08_signature_app.py`

Class `SignatureApplicationScene(Scene)`:

#### Phần 1 (0-6s): Trích đặc trưng từ chữ ký
- Hiện lại chữ ký từ Scene 1 ở bên trái màn hình (nhỏ hơn, scale 0.6)
- Bên phải: hiện các đường cong đặc trưng x(t), y(t), pressure(t)
  - Mỗi đường là một `axes.plot` với data ngẫu nhiên nhưng trông như chữ ký thật
  - Label: "x(t)", "y(t)", "pressure(t)"
  - Color: BLUE_C, GREEN, ORANGE
  - `LaggedStartMap(Create, curves, lag_ratio=0.3)`

#### Phần 2 (6-12s): Vector 100-D → điểm trong không gian
- 3 đường cong "co rúm" thành một cột số (vector 100 phần tử)
- Vector này biến thành 1 điểm tròn (Dot, YELLOW) trong một plane 2D giả lập
  - Animation: `Transform(vector_column, single_dot)`
- Caption: "Vector đặc trưng (100 chiều, hiển thị 2D)"

#### Phần 3 (12-22s): Mật độ Parzen của 25 chữ ký mẫu
- Hiện 25 điểm xanh (chữ ký thật của user) rải rác trên plane 2D
  - Tập trung quanh một vùng nhỏ (giả lập "manifold của chữ ký X")
- Quanh mỗi điểm vẽ một kernel mờ (như Scene 5)
- Đường contour mật độ Parzen 2D xuất hiện — sử dụng `ImplicitFunction` hoặc đường viền tô gradient
- Highlight vùng mật độ cao bằng glow blue nhẹ

#### Phần 4 (22-30s): Test với chữ ký mới
Animate TWO test cases:

Case A — Chữ ký thật:
- Một điểm vàng xuất hiện trong vùng mật độ cao
- Vùng quanh nó tỏa sáng GREEN
- Caption lớn: "✓ THẬT" + score: `s_PWC = 0.87`

Case B — Chữ ký giả:
- Một điểm vàng xuất hiện XA vùng mật độ
- Đỏ rực, có dấu X trên đầu
- Caption lớn: "✗ GIẢ MẠO" + score: `s_PWC = 0.03`

Cuối scene hiện công thức:
```python
score_eq = MathTex(
    r"s_{\text{PWC}} = p(\mathbf{o}_T \mid \lambda_C^{\text{PWC}})"
).to_edge(DOWN)
```
- Caption: "Score càng cao = càng giống thật"
- Reference: "Handbook of Biometrics, Ch. 10"

---

### File: `scene_09_beyond_signature.py`

Class `BeyondSignatureScene(Scene)`:

#### Phần 1 (0-12s): 4 ô lưới 2x2 — các bài toán khác nhau
Tạo 4 panel:

**Panel 1 (góc trên trái) — Khuôn mặt:**
- 3 hình tròn nhỏ tượng trưng cho 3 người (dùng `Circle` với màu khác nhau, có "icon mặt" đơn giản: 2 mắt + 1 miệng)
- Quanh mỗi người: contour Parzen mờ
- Một khuôn mặt mới (Dot vàng) xuất hiện → rơi vào contour người thứ 2 → flash green

**Panel 2 (góc trên phải) — Vân tay:**
- Hình vân tay đơn giản (dùng `ParametricFunction` với hàm xoắn ốc)
- Một vài minutiae điểm (chấm đỏ nhỏ)
- Tương tự, có contour Parzen và 1 sample test

**Panel 3 (góc dưới trái) — Mống mắt (Iris):**
- IrisCode dưới dạng grid 8x16 với các ô đen/trắng ngẫu nhiên
- Caption: "IrisCode (Daugman) → Parzen trong không gian Hamming"

**Panel 4 (góc dưới phải) — Anomaly Detection:**
- Scatter plot lưu lượng mạng: 50 chấm xanh tập trung 1 cụm
- 1 chấm đỏ outlier xa
- Caption: "Phát hiện bất thường mạng"

Animation:
- 4 panel xuất hiện đồng thời với `LaggedStart(FadeIn(...), lag_ratio=0.15)`
- Mỗi panel tự chạy animation con (test sample được phân loại) — async via `AnimationGroup`

#### Phần 2 (12-20s): Probabilistic Neural Network (PNN)

Clear 4 panel, hiện sơ đồ PNN:

```
        [ω₁]    [ω₂]    [ω₃]      ← category units (c)
         |       |       |
       /   \   /   \   /   \
     [P₁][P₂][P₃][P₄][P₅][P₆]      ← pattern units (n)
        \  |   |   |   |  /
         [x₁] [x₂] [x₃]              ← input units (d)
```

- 3 layer node được tạo bằng `Circle` với label bên trong
- Connections: dùng `Line` mỏng
- Highlight 1 đường zigzag từ input → pattern unit → category unit để show flow

Caption bên cạnh:
- "Huấn luyện: chỉ 1 lần duyệt qua data"
- "Phân loại: O(1) (parallel)"
- Reference: "Duda et al., §4.3.5"

#### Phần 3 (20-25s): Punch line
Clear hết. Hiện text lớn ở giữa:

```
Một công thức.
Mọi bài toán nhận dạng.
```

- Font size 56, color ACCENT_YELLOW
- `Write` với run_time=2
- Đợi 2s

## 3B1B Style Notes
- Phần 2 (PNN) tham khảo style sơ đồ neural network của 3B1B trong series "Neural Networks" — các node đều có viền trắng mỏng và glow nhẹ khi active
- 4 panel ở Phần 1 dùng `VGroup` đặt trong `MovingCameraScene` để có thể zoom vào từng panel nếu cần
- Punch line cuối: dùng style "big text reveal" như video "But what is a neural network?"

## Validation
- [ ] 4 panel ở Scene 9 layout đều, không panel nào lệch
- [ ] Sơ đồ PNN dễ đọc, label rõ ràng
- [ ] Scene 8 nối liền với Scene 1 (chữ ký) — đóng vòng tròn câu chuyện
- [ ] Tổng thời lượng Scene 8: ~30s, Scene 9: ~25s

Hỏi tôi: có muốn thêm logo Apple Face ID, Windows Hello, etc. ở Panel 1 Scene 9 để tăng tính thực tế? (cần có file logo .svg)
```

---

## 🎬 BATCH 7 — Scene 10 & Tích hợp

> **Mục tiêu:** Scene cuối + ghép tất cả thành 1 video.

```
BATCH 7: Sinh code Manim cho Scene 10 (Outro) và file tích hợp toàn bộ

## Bối cảnh
- Hoàn thành Batch 0-6 (10 scene files)
- Scene 10 (8:30-8:50) trong kịch bản

## Yêu cầu

### File: `scene_10_outro.py`

Class `OutroScene(Scene)`:

#### Phần 1 (0-5s): Phương trình quay lại
- Hiện phương trình Parzen rút gọn:
  ```python
  final_eq = MathTex(
      r"\hat{p}(\mathbf{x}) = \frac{1}{n}\sum_{i=1}^{n} K_h(\mathbf{x} - \mathbf{x}_i)"
  ).scale(1.5)
  ```
- `Write` chậm rãi (run_time=3)
- Đợi 1.5s

#### Phần 2 (5-12s): 3 từ khóa
Dưới phương trình, hiện 3 từ khóa xếp ngang:

```python
keywords = VGroup(
    Text("Đơn giản", color=ACCENT_BLUE),
    Text("Không giả định", color=ACCENT_YELLOW),
    Text("Phổ quát", color=ACCENT_GREEN),
).arrange(RIGHT, buff=1.5).scale(0.9)
```

Mỗi từ khóa xuất hiện cách nhau 0.6s (`LaggedStartMap(FadeIn, ..., lag_ratio=0.3)`)
Mỗi từ có hiệu ứng glow nhẹ khi xuất hiện

#### Phần 3 (12-18s): Credits cuộn
Move phương trình + keywords lên TOP, ở DOWN hiện credits cuộn:

```python
credits = VGroup(
    Text("Tham khảo:", font_size=22, color=MUTED, weight=BOLD),
    Text("• Duda, Hart & Stork — Pattern Classification (2001), §4.3", font_size=18),
    Text("• Handbook of Biometrics — Chương 10: Signature Verification", font_size=18),
    Text("• Parzen, E. (1962) — On estimation of a probability density function", font_size=18),
    Text("• Phong cách Manim: 3Blue1Brown (Grant Sanderson)", font_size=18),
).arrange(DOWN, buff=0.25, aligned_edge=LEFT)

credits.to_edge(DOWN, buff=0.5)
```

Animation: `FadeIn(credits, shift=UP*0.3)` (không cuộn — chỉ fade)

#### Phần 4 (18-20s): Logo/Signature
- Dưới cùng: text "Đồ án Nhận dạng Mẫu — 2025" (font_size=16, MUTED)
- Fade out toàn bộ trong 1.5s

---

### File: `main_compile.py`

Tạo một file để compile và preview TOÀN BỘ video. Có 2 chế độ:

#### Mode 1: Render từng scene riêng
```python
# main_compile.py
"""
Render từng scene độc lập để preview.
Chạy: python main_compile.py --scene 5
"""
import subprocess
import sys

SCENES = [
    ("scene_01_hook.py", "HookScene"),
    ("scene_02_bridge.py", "BridgeScene"),
    ("scene_03_parametric_fails.py", "ParametricFailsScene"),
    ("scene_04_histogram.py", "HistogramScene"),
    ("scene_05_kernel_sum.py", "KernelSumScene"),
    ("scene_06_bandwidth.py", "BandwidthCompareScene"),
    ("scene_07_convergence.py", "ConvergenceScene"),
    ("scene_08_signature_app.py", "SignatureApplicationScene"),
    ("scene_09_beyond_signature.py", "BeyondSignatureScene"),
    ("scene_10_outro.py", "OutroScene"),
]

def render_scene(idx, quality="m"):
    """Render scene theo index (1-10)."""
    file, cls = SCENES[idx-1]
    cmd = ["manim", f"-pq{quality}", file, cls]
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        for i in range(1, 11):
            render_scene(i, quality="l")  # low quality cho preview nhanh
    elif len(sys.argv) > 2 and sys.argv[1] == "--scene":
        render_scene(int(sys.argv[2]))
    else:
        print("Usage: python main_compile.py [--all | --scene N]")
```

#### Mode 2: One big scene ghép tất cả
Tạo file `scene_full_video.py` với class `FullVideo(Scene)`:

```python
class FullVideo(Scene):
    """Ghép toàn bộ 10 scene thành 1 video duy nhất."""

    def construct(self):
        # Import construct method từ các scene
        from scene_01_hook import HookScene
        from scene_02_bridge import BridgeScene
        # ... etc

        # Chạy lần lượt
        HookScene.construct(self)
        self.clear()
        self.wait(0.3)  # transition pause

        BridgeScene.construct(self)
        self.clear()
        self.wait(0.3)

        # ... lặp lại cho 10 scenes
```

**LƯU Ý kỹ thuật:** Manim không hỗ trợ tốt việc gọi `construct` của class khác. Phương án thay thế: refactor mỗi scene thành 1 hàm `construct_scene_XX(self)` ngoài class, rồi `FullVideo.construct` gọi tuần tự.

Hãy sinh phương án refactor này, kèm hướng dẫn migration ngắn.

## Validation cuối cùng
Sau khi sinh xong:
- [ ] `main_compile.py --scene 1` render được scene 1
- [ ] `main_compile.py --all` render tất cả 10 scene ở low quality (~5 phút build)
- [ ] `scene_full_video.py` chạy được, output file MP4 duy nhất ~9 phút
- [ ] Khoảng nghỉ giữa các scene ~0.3-0.5s (không quá dài)
- [ ] Không có scene nào bị "cắt" giữa chừng do exception

Đề xuất với tôi:
1. Nên thêm transition wipe/fade giữa các scene không?
2. Nên có intro logo (3s) ở đầu video không?
3. Có cần thêm background music (qua external editor) không?
```

---

## 🎬 BATCH FINAL — Render & QA

> **Mục tiêu:** Render full quality + chạy checklist chất lượng cuối.

```
BATCH FINAL: Render production-quality video và chạy QA checklist

## Yêu cầu

### Bước 1: Render high quality
Chạy:
```bash
manim -pqh scene_full_video.py FullVideo
```
- `-pqh` = preview + quality high (1080p, 60fps)
- Output: `media/videos/scene_full_video/1080p60/FullVideo.mp4`
- Thời gian build dự kiến: 15-30 phút (tùy GPU)

Nếu có GPU mạnh, dùng:
```bash
manim -pqk scene_full_video.py FullVideo  # 4K
```

### Bước 2: QA Checklist (cho Gemini chạy + báo cáo)

Hãy nhìn vào video output và xác nhận TỪNG mục:

#### 🎯 Cấu trúc nội dung
- [ ] Có đủ 10 scene theo đúng thứ tự
- [ ] Tổng thời lượng nằm trong khoảng 7:30 - 10:00
- [ ] Mỗi scene có ít nhất 1 visual chính (axes, equation, hoặc diagram)
- [ ] Scene 5 (cốt lõi) có thời lượng > 25s
- [ ] Outro có credits đủ 5 nguồn

#### 🎨 Visual quality
- [ ] Background đồng nhất `#0F1419` (kiểm tra bằng cách pause giữa scene)
- [ ] KHÔNG có text bị tràn ra ngoài frame
- [ ] KHÔNG có element bị overlap không cố ý
- [ ] Font tiếng Việt hiển thị đúng (kiểm tra dấu)
- [ ] Tất cả LaTeX công thức render rõ nét
- [ ] Màu của các element nhất quán giữa các scene (vd: chữ ký luôn dùng cùng màu)

#### 🎬 Animation quality
- [ ] Mọi transition mượt, không jerky
- [ ] `LaggedStart` được dùng cho các xuất hiện liên tiếp
- [ ] `always_redraw` slider ở Scene 6 chạy real-time
- [ ] Đoạn cộng dồn kernels ở Scene 5 (KEY moment) đặc biệt mượt
- [ ] Khoảng wait() giữa các động tác >= 0.3s (không gấp gáp)

#### 📚 Tính đúng đắn học thuật
- [ ] Công thức Parzen đúng (có 1/n, 1/V, φ, h)
- [ ] 3 điều kiện hội tụ ở Scene 7 chính xác (V→0, k→∞, k/n→0)
- [ ] Citation Duda-Hart-Stork chính xác (trang 161, 163, 168 đều có nhắc đúng chỗ)
- [ ] Phần PNN ở Scene 9 có đúng 3 layer (input, pattern, category)

#### 🔧 Kỹ thuật
- [ ] File MP4 chạy được trên trình duyệt (test bằng Chrome)
- [ ] Audio track: TRỐNG (sẽ thêm voiceover sau)
- [ ] Resolution: tối thiểu 1920x1080
- [ ] Bitrate: >= 5 Mbps (kiểm tra bằng `ffprobe`)

### Bước 3: Export deliverables

Tạo folder `deliverables/`:
- `parzen_windows_silent.mp4` — video không tiếng (cho voiceover bên ngoài)
- `parzen_windows_with_subs.mp4` — version có subtitle nhúng (nếu Manim hỗ trợ qua `manim_voiceover`)
- `scenes_individual/` — folder chứa 10 mp4 riêng lẻ
- `thumbnails/` — folder chứa 10 ảnh PNG từ frame ấn tượng nhất của mỗi scene (tự chọn)

### Bước 4: Report

Sinh ra file `RENDER_REPORT.md` chứa:
- Tổng thời lượng video (đo từ ffprobe)
- Thời lượng từng scene
- Bugs phát hiện được (nếu có)
- Đề xuất cải thiện cho lần render tiếp

## Sau khi xong
Hỏi tôi:
1. Có muốn rerender với 4K không?
2. Có cần xuất GIF cho social media (cắt từ Scene 5 - kernel sum) không?
3. Bước tiếp theo: thêm voiceover (manim_voiceover) hay edit ngoài (Premiere/DaVinci)?
```

---

## 📌 Phụ lục: Tips khi làm việc với Gemini Pro

### 1. Khi Gemini sinh code có lỗi
- Quote NGUYÊN VĂN error trace
- Nói: "Lỗi này ở dòng X. Hãy xem lại logic và fix, không cần sinh lại toàn bộ file."
- KHÔNG accept "fix bằng cách bỏ feature đó đi" — bắt Gemini giải quyết gốc rễ

### 2. Khi Gemini hiểu sai style
- Đưa lại link tham khảo cụ thể: "Hãy xem video [X] của 3B1B tại phút Y:ZZ"
- Yêu cầu Gemini diễn giải lại style theo cách hiểu của nó trước khi sinh code

### 3. Khi Gemini lười (sinh stub code)
- Nói rõ: "Tôi cần production-ready code, KHÔNG phải skeleton."
- Yêu cầu: "Hãy điền đầy đủ mọi animation, không placeholder."

### 4. Quản lý context limit
- Mỗi 2-3 batch, **reset session** Gemini và đưa lại "Tài liệu tham khảo bắt buộc" + kịch bản + tóm tắt những batch đã hoàn thành
- Lưu code Gemini sinh ra ngay lập tức vào local — đừng dựa vào memory của Gemini

### 5. Iterate nhanh
- Render bằng `-pql` (low quality) để preview trong < 1 phút
- Chỉ render `-pqh` ở batch cuối
- Dùng `-s` flag để render frame cuối (kiểm tra composition nhanh)

---

## 🎯 Kết

File này thiết kế để bạn sản xuất video Manim hoàn chỉnh trong **5-7 ngày**, làm việc 2-3 giờ/ngày với Gemini Pro. Tổng số batch: **9** (Batch 0 → Batch FINAL).

Chúc bạn render thành công 🚀

> 💡 **Pro tip cuối:** Sau khi có video silent, đừng quên thêm **voiceover** — đây là phần làm video thực sự "thấm". Có thể dùng:
> - `manim_voiceover` plugin (tự động sync)
> - ElevenLabs TTS với giọng tiếng Việt
> - Tự thu âm với microphone trong DaVinci Resolve
