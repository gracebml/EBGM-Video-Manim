# 🎬 Kịch bản Video EBGM (bản 10 phút — HOÀN CHỈNH) — Elastic Bunch Graph Matching

> **Cơ sở:** 33 scene đã dựng (`scene_01..scene_33.py`, thiếu `scene_18`) chia 4 phần: Overview (1–7), Algorithm Detail (8–17), Experiments (19–26), Discussion (27–33). Tổng thời lượng dự kiến của 33 scene ≈ **29 phút** → gọt còn **~10 phút / 16 scene**.
> **Bản này** = bản gọt 16 scene + lời thoại "tech-storytelling" (intuition, ẩn dụ Deep Learning) đã **sửa các lỗi** đã review (con số 57%, thuật ngữ, năm công bố, câu cụt…), kèm **storyboard mới cho S3** theo ý tưởng "thời kỳ tiền Deep Learning".
> **Phong cách & màu:** giữ `_common.py` của series (nền navy, lavender `#B8B5FF` = thương hiệu EBGM). Phụ đề tiếng Việt `Text` (Be Vietnam Pro), công thức `MathTex`/`vn_tex`.
> **Lối đọc VO:** Explanatory / Tech-Storytelling (3Blue1Brown · Veritasium). Nhấn các cặp đối lập (Thưởng/Phạt, Cứng/Mềm, Linh hoạt/Sắc bén). Đoạn Lòng chảo/Đỉnh nhọn (S7) đọc chậm 1 nhịp.

---

## 📊 PHẦN A — PHÂN TÍCH 33 SCENE: GIỮ / CẮT / GỘP

| Scene gốc | Nội dung | Dự kiến | Quyết định | Lý do |
|---|---|---|---|---|
| 01 Title | Tiêu đề EBGM | 12s | **GỘP→ S1** | Mở màn ngắn, nhập chung bài toán |
| 02 Face Recognition | Verification 1:1 vs Identification 1:N | 50s | **GỘP→ S1** | Chỉ giữ ý EBGM giải 1:N |
| 03 Core Problem | In-class variance, collapse + emphasize | 55s | **GIỮ→ S2** | Cốt lõi "vì sao khó" |
| 04 Prior Approaches | Hình học thủ công / NN / PCA | 90s | **❌ thay bằng S3 mới** | Theo ý người dùng: framing tiền-DL |
| 05 Bridge Problem | Cần giải pháp trung gian | 15s | **GỘP→ S3 (1 câu)** | Câu chốt dẫn vào EBGM |
| 06 EBGM Novel | Image Graph + Jet + Bunch + ưu điểm | 75s | **GIỮ→ S4** | Tuyên ngôn ý tưởng |
| 07 Teaser | Chốt overview | 15s | **❌ CẮT** | Chuyển tiếp thừa |
| 08 Intro | "How does EBGM work?" | 20s | **❌ CẮT** | Chuyển tiếp thừa |
| 09 Gabor Basics | Gabor wavelet, DC-free, sinh học | 80s | **GIỮ→ S5** | Nền tảng kỹ thuật |
| 10 Jet Basics | 40 hệ số phức/điểm | 60s | **GIỮ→ S6** | Khái niệm jet |
| 11 Similarity | Sₐ (thô) vs S_φ (tinh, pha) | 75s | **GIỮ→ S7** | Quan trọng: pha → định vị |
| 12 Individual Graph | Nút=jet, cạnh=Δx | 65s | **GIỮ→ S8** | Định nghĩa image graph |
| 13 Bunch Graph | FBG, chồng đồ thị | 70s | **GIỮ→ S9** | Ý tưởng đột phá FBG |
| 14 Graph Similarity | Feature match − λ·distortion | 55s | **GIỮ→ S10** | Hàm mục tiêu matching |
| 15 Matching Procedure | Elastic matching 4 bước | 110s | **GIỮ→ S11** ⭐ | Trái tim thuật toán |
| 16 Two-Stage | Normalization → Recognition | 50s | **GỘP→ S11 (1 câu)** | Chi tiết phụ |
| 17 Recognition Stage | So probe/gallery, ranking | 60s | **GIỮ→ S12** | Bước nhận dạng |
| 19 Intro Experiments | 4 câu hỏi | 20s | **❌ CẮT** | Chuyển tiếp thừa |
| 20 Databases | FERET + Bochum, poses | 50s | **GỘP→ S13** | Nhập với kết quả FERET |
| 21 FERET Results | 98% / 84% / 57% | 75s | **GIỮ→ S13** | Số liệu chủ chốt |
| 22 Bochum Results | Cross-pose 94%/88%, 30 nodes | 60s | **GỘP→ S14** | Nhập với pha |
| 23 Phase Importance | 1.6px vs 5.2px; 88% vs 67% | 70s | **GIỮ→ S14** | Bằng chứng vai trò pha |
| 24 Efficiency | 1000× nhanh hơn; ZN-Face | 55s | **GỘP→ S14 (1 câu)** | Fold cuối S14 |
| 25 Benchmarks | Blind test vs Gordon/Gutta/Phillips | 90s | **❌ CẮT** | Trùng so sánh; nặng |
| 26 Summary | Tổng kết phần 3 | 25s | **❌ CẮT** | Trùng lặp |
| 27 Generality | In-class: faces/animals/vehicles | 45s | **GIỮ→ S15** | Mở rộng ý nghĩa |
| 28 Vs Preceding | vs Lades 1993 | 70s | **❌ CẮT** | Pha/FBG đã nói ở trên |
| 29 Vs Template | Feature-based vs PCA | 45s | **GỘP→ S15** | So sánh đại diện |
| 30 Vs 3D | 2D grid vs 3D morphable | 50s | **❌ CẮT** | Ngoài lề mạch chính |
| 31 Pros/Cons | 3 ưu / 3 nhược | 60s | **GỘP→ S15** | Gói trong "bức tranh lớn" |
| 32 Legacy/Future | Di sản, cầu nối deep learning | 55s | **GỘP→ S16 (1 câu)** | Fold vào kết luận |
| 33 Conclusion | Kết | 30s | **GIỮ→ S16** | Đóng video |

**CẮT hẳn:** 07, 08, 19, 25, 26, 28, 30. **Thay mới:** 04→S3. **Kết quả:** 16 scene, mục tiêu ~10:48 (cách rút về 10:00 ở Phần C).

---

## 🎯 PHẦN B — KỊCH BẢN HOÀN CHỈNH (16 SCENE · VO + VISUAL + MỐC + NGUỒN)

> Mỗi scene: **mốc thời gian · nguồn scene gốc**, rồi **🎤 Lời thoại (VO)** và **🎨 Visual**. VO canh ~150 từ/phút.

---

### 🎬 S1 — MỞ ĐẦU & BÀI TOÁN
**⏱ 0:00 → 0:24 (24s) · nguồn: sc01 + sc02**

**🎤 Lời thoại (VO)**
> "Bạn lướt qua một người quen trên phố, và bộ não nhận ra họ chỉ trong một phần mười giây. Nhưng máy tính nhận dạng khuôn mặt như thế nào?
>
> Bài toán có hai nhánh: *Xác thực 1:1* — 'Tôi có đúng là chủ nhân chiếc điện thoại này không?'; và *Nhận dạng 1:N* — 'Người này là ai trong hàng triệu hồ sơ?'.
>
> Hôm nay, ta đi vào nhánh khó hơn: **nhận dạng 1:N**."

**🎨 Visual**
- 0:00–0:09: Tiêu đề `EBGM — Elastic Bunch Graph Matching` (lavender) hiện ra rồi thu nhỏ lên góc (sc01).
- 0:09–0:24: Hai thẻ `VERIFICATION 1:1` và `IDENTIFICATION 1:N` (sc02); thẻ **1:N sáng lavender**, thẻ 1:1 mờ đi.
- *Cắt:* bỏ ví dụ FaceID/hộ chiếu dài của sc02.

---

### 🎬 S2 — VÌ SAO NHẬN DẠNG KHUÔN MẶT LẠI KHÓ
**⏱ 0:24 → 1:02 (38s) · nguồn: sc03**

**🎤 Lời thoại (VO)**
> "Điều gì làm AI đau đầu nhất? Không phải sự khác biệt giữa hai người — mà là thực tế: *cùng một người* có thể trông như hai người hoàn toàn khác nhau.
>
> Khi bạn cười, nhăn mặt, hay ánh sáng hắt từ dưới lên, ma trận điểm ảnh thay đổi hoàn toàn. Đó gọi là *phương sai nội lớp* — intra-class variance.
>
> Một thuật toán tốt phải giải nghịch lý này: đủ **linh hoạt để dung thứ** cho biến dạng của cùng một người, nhưng đủ **sắc bén để phân biệt** chi tiết cực nhỏ giữa hai người khác nhau."

**🎨 Visual**
- 0:24–0:48: Một người qua 5 trạng thái (chính diện / tư thế / biểu cảm / ánh sáng / vật cản) gắn nhãn `CÙNG MỘT NGƯỜI` (sc03).
- 0:48–1:02: Hai mục tiêu đối lập sáng lên: `Linh hoạt — dung thứ biến dạng` / `Sắc bén — phân biệt đặc trưng` (sc03, đổi nhãn cho khớp cặp đối lập).
- *Cắt:* bỏ phần "wide face vs long face".

---

### 🎬 S3 — THỜI KỲ TIỀN DEEP LEARNING (storyboard MỚI) ⭐
**⏱ 1:02 → 1:52 (50s) · nguồn: DỰNG MỚI (thay sc04) + chốt sc05**

> **Ghi chú:** Scene này nội dung đổi hoàn toàn so với sc04 (3 cách tiếp cận cũ) → **phải dựng scene mới**, không tái dùng sc04/05. Ý tưởng theo yêu cầu của người dùng: đặt EBGM vào bối cảnh trước khi neural network thống trị.

**🎤 Lời thoại (VO)**
> "Ngày nay, gặp bài toán nhận diện khuôn mặt, phản xạ đầu tiên của ta là gì? Dựng một mạng CNN, thu hàng triệu ảnh, định nghĩa một hàm Loss, rồi để Backpropagation lo phần còn lại.
>
> Nhưng hãy tua về năm 1997. Không có GPU mạnh. Không tập dữ liệu khổng lồ. Nhận diện một khuôn mặt khi đổi ánh sáng hay biểu cảm gần như bất khả thi nếu chỉ so từng pixel.
>
> Vậy các nhà khoa học thời đó giải bài toán *biến thiên hình học* này ra sao? Họ không dùng học sâu — họ dùng toán học thuần và xử lý tín hiệu. Năm 1997, một nhóm công bố trên IEEE PAMI — một trong những tạp chí AI khắt khe nhất — một ý tưởng khác thường: dạy máy tính *nhìn* khuôn mặt theo đúng cách **vỏ não thị giác** của chúng ta hoạt động.
>
> Thuật toán đó tên là **Elastic Bunch Graph Matching**. Nó từng đạt thứ hạng hàng đầu trong blind test FERET những năm 90. Hôm nay, ta sẽ mổ xẻ nó."

**🎨 Visual (storyboard mới)**
- 1:02–1:18 — *Phản xạ hiện đại:* bên trái màn hiện một sơ đồ CNN nhiều lớp (các khối chồng nhau) + mũi tên `Backpropagation` chạy ngược + nhãn `hàng triệu ảnh` + `Loss ↓`. Tông màu coral/teal (gợi "deep learning"). `LaggedStart` các lớp.
- 1:18–1:30 — *Tua ngược thời gian:* hiệu ứng đồng hồ/ră bobbin quay ngược; sơ đồ CNN mờ và co lại. Hiện 3 thẻ "thiếu thốn 1997": `Không GPU`, `Không big data`, `Pixel-by-pixel thất bại` (icon ✗ coral). Một khuôn mặt đổi sáng/biểu cảm khiến lưới pixel nhấp nháy hỗn loạn.
- 1:30–1:42 — *Bài báo:* phóng to một "bìa paper" cách điệu, **đóng dấu `IEEE PAMI · 1997`** (lavender), dưới ghi nhỏ `(mở rộng thành chương sách CRC 1999)`. Một biểu tượng *vỏ não thị giác* (đường viền não + tia) sáng lên — báo trước Gabor ở S5.
- 1:42–1:52 — Tên `ELASTIC BUNCH GRAPH MATCHING (EBGM)` hiện lớn giữa màn (lavender, glow); badge nhỏ `FERET · top-ranked`. Chốt 1 câu của sc05: phụ đề `Giải pháp trung gian: cấu trúc + tín hiệu, không cần training khổng lồ`.

---

### 🎬 S4 — Ý TƯỞNG EBGM: BA TRỤ CỘT
**⏱ 1:52 → 2:36 (44s) · nguồn: sc06**

**🎤 Lời thoại (VO)**
> "EBGM xây trên ba trụ cột. Khác với việc nhớ pixel hay nén tuyến tính như PCA:
>
> Một — không nhìn mặt như mặt phẳng pixel, mà như một **Đồ thị** nối các điểm mốc. Hai — tại mỗi mốc, không lấy màu, mà trích một **Wavelet Jet**, hiểu nôm na là *ADN kết cấu* của vùng da đó. Ba — để đối phó mọi tư thế, xếp chồng hàng loạt đồ thị mẫu thành một **Face Bunch Graph**.
>
> Kết quả? Một hệ thống rất bền với ánh sáng, học được với chưa tới một trăm ảnh mẫu, và đạt độ chính xác đáng kinh ngạc."

**🎨 Visual**
- 1:52–2:18: Ba khái niệm hiện tuần tự: `1. Image Graph` (lưới mốc trên mặt), `2. Wavelet Jet` (bó sóng Gabor 8 hướng), `3. Bunch Graph` (chồng đồ thị) (sc06).
- 2:18–2:36: Bốn ưu điểm gọn: `Bền với ánh sáng · Tổ hợp linh hoạt · Ít dữ liệu · Dễ mở rộng`; chốt `CÂN BẰNG THIẾT KẾ ↔ HỌC MÁY`.
- *Cắt:* đoạn loại suy "nhận thức con người" dài của sc06; bỏ sc07.

---

### 🎬 S5 — GABOR WAVELETS: MẮT CỦA EBGM
**⏱ 2:36 → 3:22 (46s) · nguồn: sc09 · 💡 ẩn dụ: CNN filters**

**🎤 Lời thoại (VO)**
> "Bắt đầu từ mức vi mô: làm sao AI *nhìn* một điểm trên mặt? Thay vì dùng pixel — vốn rất nhạy với ánh sáng — các nhà khoa học vay mượn từ sinh học.
>
> Họ dùng **Sóng Gabor**: về toán học là một sóng hình sin bị *nhốt* trong một bao Gaussian. Nó như một bộ lọc, chỉ bắt các nếp nhăn, góc cạnh ở một hướng và một tần số nhất định.
>
> Tuyệt ở chỗ: nó triệt tiêu thành phần ánh sáng nền — DC-free. Giống hệt cách các lớp đầu của một mạng CNN dò đường nét, sóng Gabor mô phỏng đúng cách vỏ não thị giác hoạt động."

**🎨 Visual**
- 2:36–3:02: Sóng phẳng × bao Gaussian = kernel Gabor (phần thực/ảo/magnitude) (sc09); nhãn `DC-free`.
- 3:02–3:22: 4 thuộc tính sáng lần lượt: `Trơ lì ánh sáng · Chịu biến dạng/xoay · Mô phỏng vỏ não · Tối ưu ảnh tự nhiên`.
- *Thêm caption nhỏ:* `≈ filter lớp đầu của CNN` (để khớp ẩn dụ trong VO).

---

### 🎬 S6 — JET: 40 HỆ SỐ PHỨC TẠI MỘT ĐIỂM
**⏱ 3:22 → 3:58 (36s) · nguồn: sc10 · 💡 ẩn dụ: "mã vạch"**

**🎤 Lời thoại (VO)**
> "Giờ ném cả bộ lọc bốn mươi sóng Gabor — năm tần số nhân tám hướng — vào đúng một điểm như khóe mắt, ta thu về **bốn mươi số phức**. Khối dữ liệu ấy gọi là một **Jet**.
>
> Hãy coi Jet như một *mã vạch* độc bản của khóe mắt đó. Và vì là số phức, mỗi phần tử có hai vũ khí: **Biên độ** — cho biết vùng này có *hình dáng* gì; và **Pha** — cho biết đặc trưng nằm *chính xác ở tọa độ nào*."

**🎨 Visual**
- 3:22–3:42: Một điểm trên mặt tỏa 40 tia tới 40 patch Gabor → gộp thành "cọc đĩa" jet (sc10).
- 3:42–3:58: Công thức `𝒥ⱼ = aⱼ·exp(i·φⱼ)`; nhãn đối lập `biên độ → nhận dạng (hình dáng)` / `pha → định vị (tọa độ)`.

---

### 🎬 S7 — SO KHỚP JET: HAI HÀM SIMILARITY
**⏱ 3:58 → 4:46 (48s) · nguồn: sc11 · 💡 ẩn dụ: Loss landscape / attractor basin**

**🎤 Lời thoại (VO) — *đọc chậm 1 nhịp ở đoạn lòng chảo/đỉnh nhọn***
> "Có hai Jet rồi, làm sao máy biết chúng giống nhau? Thuật toán phối hợp hai hàm tương đồng cực nhịp nhàng.
>
> Hàm thứ nhất chỉ so *Biên độ*, bỏ pha. Hãy hình dung nó tạo ra một *lòng chảo* trơn tru — vùng thu hút rộng — giúp thuật toán bắt tín hiệu từ xa và trượt dần về phía con mắt. Đây là bước **khớp thô**.
>
> Khi đã ở rất gần, hàm thứ hai có *Pha* kích hoạt. Nó nhọn hoắt, nhạy với từng dịch chuyển nhỏ, ghim chặt vào đúng vị trí với độ chính xác **dưới một pixel**. Hơn thế, nó còn *chỉ đường*: cho biết phải dịch jet đi bao nhiêu là vừa."

**🎨 Visual**
- 3:58–4:24: Hai panel: `Sₐ` lòng chảo trơn rộng ("large attractor basin · tìm thô") vs `S_φ` nhiều đỉnh nhọn ("subpixel · khớp tinh") (sc11).
- 4:24–4:46: *(bám VO "chỉ đường")* mũi tên displacement lavender dẫn jet lệch trượt về đúng con mắt; thanh `focus 1→5` (coarse-to-fine).

---

### 🎬 S8 — IMAGE GRAPH: ĐỒ THỊ KHUÔN MẶT
**⏱ 4:46 → 5:16 (30s) · nguồn: sc12**

**🎤 Lời thoại (VO)**
> "Rải các Jet này lên các điểm mốc — mắt, mũi, miệng — rồi nối lại… ta có một **Đồ thị khuôn mặt**.
>
> Các *Nút* chứa mã vạch kết cấu là Jet; các *Cạnh* chứa khoảng cách hình học. Chìa khóa thiên tài: EBGM tách hẳn thông tin *bề mặt da* khỏi *cấu trúc xương*, nên máy có thể xử lý từng phần độc lập."

**🎨 Visual**
- 4:46–5:16: Lưới đồ thị lavender trên mặt; highlight `nút = Jet 𝒥ₙ [40 số phức]` và `cạnh = Δxₑ = xₙ − xₙ'` (sc12).

---

### 🎬 S9 — FACE BUNCH GRAPH
**⏱ 5:16 → 6:00 (44s) · nguồn: sc13 · 💡 ẩn dụ: Local Expert**

**🎤 Lời thoại (VO)**
> "Nhưng đồ thị của *bạn* không thể khớp hoàn hảo lên mặt *tôi*. Giải pháp: **Face Bunch Graph**.
>
> Xếp chồng hàng chục đồ thị khác nhau, giờ tại nút *Mắt* ta không chỉ có một con mắt, mà cả một *chùm*: mắt ti hí, mắt to tròn, mắt đeo kính.
>
> Gặp người lạ, hệ thống tự lục trong chùm để bầu ra một **Chuyên gia cục bộ** — local expert — hợp nhất cho từng mốc. Sự kết hợp chéo ấy tạo khả năng phủ quát gần như vô tận."

**🎨 Visual**
- 5:16–5:38: Nhiều `Đồ thị đơn lẻ` bay tới, chồng thẳng hàng thành FBG (sc13).
- 5:38–6:00: Phóng vào nút mắt: chùm jet; jet thắng **bừng sáng lavender** (`local expert`).

---

### 🎬 S10 — HÀM TƯƠNG ĐỒNG ĐỒ THỊ
**⏱ 6:00 → 6:32 (32s) · nguồn: sc14 · 💡 ẩn dụ: Loss + Regularization**

**🎤 Lời thoại (VO) — *nhấn cặp Thưởng/Phạt***
> "Biết đồ thị đã áp đúng mặt chưa? EBGM giải một bài toán tối ưu với hàm mục tiêu rất quen thuộc — một sự *giằng co*.
>
> Một mặt, nó **Thưởng** bằng điểm tương đồng của các Jet. Mặt khác, nó **Phạt** sự biến dạng hình học của các cạnh, nhân hệ số Lambda.
>
> Nếu bạn ép điểm *mũi* lệch lên tận *trán* để khớp bề mặt, cạnh nối bị kéo giãn — và thuật toán ném cho bạn một án phạt khổng lồ."

**🎨 Visual**
- 6:00–6:32: Công thức `S_B = (1/N)Σ max S_φ − (λ/E)Σ (Δx méo)²`; ba ví dụ cân bằng: feature cao+phạt khổng lồ / feature thấp+phạt 0 / **feature tốt+phạt nhỏ** (sc14). Lò xo cạnh kéo căng → vùng phạt coral.

---

### 🎬 S11 — ELASTIC MATCHING: 4 BƯỚC ⭐
**⏱ 6:32 → 7:42 (70s) · nguồn: sc15 (+ sc16 1 câu) · 💡 ẩn dụ: coarse→fine như giảm nhiệt**

**🎤 Lời thoại (VO) — *nhấn cặp Cứng/Mềm***
> "Và đây — trái tim thuật toán: Elastic Matching, đi từ *cứng nhắc* đến *mềm dẻo*.
>
> Đầu tiên, đồ thị là một khối **cứng**, trượt khắp ảnh để định vị khuôn mặt. Rồi nó co giãn toàn cục để khớp kích thước, và nới ngang–dọc cho đúng tỉ lệ.
>
> Nhưng kỳ diệu nằm ở bước cuối — chữ **Elastic**: đồ thị được *thả lỏng*. Từng nút tự do bò trườn, nhích từng chút về đúng điểm mốc thật trên ảnh, trong khi các cạnh như những chiếc *lò xo* níu giữ cấu trúc khỏi vỡ.
>
> Toàn bộ chạy hai pha: *chuẩn hóa* — cắt mặt về kích thước chuẩn 128×128; rồi mới *nhận diện* — trích đồ thị chi tiết cuối cùng."

**🎨 Visual**
- 6:32–6:58: Bước 1–2: khuôn cứng quét tìm mặt, rồi co/giãn khớp kích thước (sc15).
- 6:58–7:24: Bước 3: nới aspect, `focus 1→5`. Bước 4 ⭐: từng nút bò về mốc, cạnh hiện dạng **lò xo**, `λ=2` (sc15).
- 7:24–7:42: Một câu gộp sc16: hai khối `Pha 1: Chuẩn hóa (128×128)` → `Pha 2: Nhận diện chi tiết`.
- *Cắt:* bỏ bảng thông số 30/70 models của sc16; chỉ giữ nhãn 2 pha.

---

### 🎬 S12 — NHẬN DẠNG: SO KHỚP & XẾP HẠNG
**⏱ 7:42 → 8:16 (34s) · nguồn: sc17**

**🎤 Lời thoại (VO)**
> "Một khi *lưới đàn hồi* đã chốt chặt vào khuôn mặt mới — ảnh *probe* — phần nhận dạng diễn ra cực nhẹ nhàng.
>
> Mang lưới này so với từng người trong *gallery*. Lúc này ta bỏ pha, **chỉ dùng biên độ**, vì biên độ bền hơn trước thay đổi nét mặt, nụ cười.
>
> Tính điểm, xếp hạng — người đứng **Top-1** chính là danh tính cần tìm."

**🎨 Visual**
- 7:42–8:02: `PROBE` so với `GALLERY`, các tia nối nút tương ứng; công thức `S_G = (1/N')Σ Sₐ` (sc17).
- 8:02–8:16: Bảng xếp hạng; `Hạng 1: M3 — 0.89 [WINNER]` trượt lên đầu, viền vàng.

---

### 🎬 S13 — THỰC NGHIỆM: DỮ LIỆU & KẾT QUẢ FERET
**⏱ 8:16 → 8:56 (40s) · nguồn: sc20 + sc21**

**🎤 Lời thoại (VO) — *(đã sửa con số 57%)***
> "Lý thuyết rất đẹp, nhưng thực tế thì sao? Trong bài kiểm tra khắt khe của chính phủ Mỹ — FERET — EBGM chỉ được cho đúng *một bức ảnh* mỗi người trong cơ sở dữ liệu.
>
> Kết quả? Cùng chụp thẳng: **chín mươi tám phần trăm**. Cùng chụp nghiêng — lật trái–phải: **tám mươi tư**. Cùng góc nghiêng vừa: năm mươi bảy. Nhưng nếu gallery thẳng mà probe lại nghiêng chéo, nó rớt thê thảm xuống chỉ còn **mười tám phần trăm**.
>
> Rõ ràng: EBGM là *vua* khi xử lý biến đổi nét mặt hay ánh sáng, nhưng góc xoay 3D lớn vẫn là gót chân Achilles."

**🎨 Visual**
- 8:16–8:30: Hai thẻ DB `FERET (250 người)` / `Bochum (108)`, dải pose, nhãn `MỘT ảnh/người` (sc20).
- 8:30–8:56: Bảng FERET rank-1 (sc21): `Frontal fa/fb 98%` (mint) · `Profile R/L 84%` (cyan) · `Half-profile R/L 57%` (teal) · `Half-profile vs Frontal 18%` (coral, nhấn "gót chân Achilles").
- *Lưu ý dựng:* nhãn phải đúng cặp pose như scene_21 (98/84/57/18/12), tránh gán nhầm 57% cho cross-pose.

---

### 🎬 S14 — CROSS-POSE, VAI TRÒ CỦA PHA & TỐC ĐỘ
**⏱ 8:56 → 9:46 (50s) · nguồn: sc22 + sc23 + sc24**

**🎤 Lời thoại (VO)**
> "Tuy nhiên ở các góc xoay *nhỏ* — mười một độ, hai mươi hai độ — nhờ độ dẻo của đồ thị, độ chính xác vẫn giữ ở chín mươi tư xuống tám mươi tám phần trăm.
>
> Còn phần *Pha* của sóng có thực sự cần không? Thực nghiệm cho thấy: bỏ pha, định vị mốc trượt tới hơn *năm phẩy hai pixel*, kéo nhận dạng tụt còn sáu mươi bảy. Giữ pha: sai chỉ *một phẩy sáu pixel*, nhận dạng vọt lên tám mươi tám. Pha chính là mỏ neo cứu cả hệ thống!
>
> Thêm nữa, tách bước *trích xuất* khỏi bước *so khớp* giúp EBGM nhanh gấp khoảng *một nghìn lần* các kiến trúc tiền nhiệm — đủ cho cả database lớn."

**🎨 Visual**
- 8:56–9:13: Bochum: `11° → 94%`, `22° → 88%`, nhãn `suy giảm rất nhẹ` (sc22).
- 9:13–9:33: So sánh pha: `1.6 px / 88%` (mint) vs `5.2 px / 67%` (coral) (sc23).
- 9:33–9:46: Sơ đồ tách `TRÍCH XUẤT (1 lần)` ⟶ `SO KHỚP (×nhiều)`, nhãn `~1000× nhanh hơn` (sc24).

---

### 🎬 S15 — EBGM TRONG BỨC TRANH LỚN
**⏱ 9:46 → 10:26 (40s) · nguồn: sc27 + sc29 + sc31**

**🎤 Lời thoại (VO)**
> "Nhìn rộng ra, EBGM giải một nhóm bài toán lớn: **nhận dạng biến thiên trong cùng một lớp** — dù là mặt người, động vật, hay xe cộ.
>
> Khác với PCA bị phá hỏng cả bức ảnh chỉ vì một cặp kính râm, EBGM *phân mảnh rủi ro*: đeo kính ư? Chỉ các Jet ở mắt bị nhiễu, các vùng khác vẫn an toàn.
>
> Đúng là nó có giới hạn — yếu khi xoay quá 22 độ, dễ lỗi khi mốc bị che. Nhưng với vị thế một thuật toán *không cần training khổng lồ*, EBGM đã làm quá xuất sắc."

**🎨 Visual**
- 9:46–10:02: `IN-CLASS RECOGNITION` với 4 biểu tượng faces/animals/vehicles/plants (sc27).
- 10:02–10:14: Mini so sánh `EBGM (feature-based)` vs `PCA (template-based)`: kính/râu chỉ lệch cục bộ ở EBGM (sc29).
- 10:14–10:26: 3 ưu (mint ✓) / 3 nhược (coral ✗) gọn (sc27 + sc31).

---

### 🎬 S16 — KẾT LUẬN
**⏱ 10:26 → 10:48 (22s) · nguồn: sc33 (+ 1 câu sc32)**

**🎤 Lời thoại (VO)**
> "Elastic Bunch Graph Matching là bản giao hưởng giữa *xử lý tín hiệu cục bộ* — Wavelets — và *hình học không gian* — Graphs.
>
> Dù Deep Learning nay đã tiếp quản ngôi vương, triết lý *điểm mốc đàn hồi* của EBGM vẫn sống trong các kiến trúc phát hiện khuôn mặt hiện đại.
>
> Cục bộ. Đàn hồi. Tổng quát. Cảm ơn các bạn — hẹn gặp lại ở video thuật toán tiếp theo!"

**🎨 Visual**
- 10:26–10:40: Lưới đồ thị trên mặt mờ dần; ba từ khóa `CỤC BỘ · ĐÀN HỒI · TỔNG QUÁT` (cyan/lavender/mint) (sc33 + 1 câu sc32).
- 10:40–10:48: Danh mục tham khảo (Wiskott 1997/1999 · Lades 1993 · Daugman 1988 · Turk & Pentland 1991) cuộn nhẹ, kết về đen.

---

## ⏱️ PHẦN C — NGÂN SÁCH THỜI LƯỢNG

| S | Tên | Δ (s) | Cộng dồn |
|---|---|---|---|
| 1 | Mở đầu & bài toán | 24 | 0:24 |
| 2 | Vì sao khó | 38 | 1:02 |
| 3 | Thời kỳ tiền Deep Learning ⭐(mới) | 50 | 1:52 |
| 4 | Ý tưởng EBGM | 44 | 2:36 |
| 5 | Gabor wavelets | 46 | 3:22 |
| 6 | Jet 40 hệ số | 36 | 3:58 |
| 7 | So khớp jet (Sₐ/S_φ) | 48 | 4:46 |
| 8 | Image graph | 30 | 5:16 |
| 9 | Face Bunch Graph | 44 | 6:00 |
| 10 | Hàm tương đồng đồ thị | 32 | 6:32 |
| 11 | Elastic matching 4 bước ⭐ | 70 | 7:42 |
| 12 | Nhận dạng & xếp hạng | 34 | 8:16 |
| 13 | Dữ liệu & FERET | 40 | 8:56 |
| 14 | Cross-pose · pha · tốc độ | 50 | 9:46 |
| 15 | Bức tranh lớn | 40 | 10:26 |
| 16 | Kết luận | 22 | 10:48 |

**Tổng ≈ 10:48.** Muốn về đúng **10:00**, cắt ~48s: rút S3 còn ~40s (bỏ 1 ý phụ), S11 còn ~60s, S2 còn ~33s, S14 còn ~45s.

---

## 🛠️ PHẦN D — VIỆC CẦN LÀM ĐỂ DỰNG BẢN 10 PHÚT
1. **Dựng MỚI scene S3** (`scene_03b_pre_deeplearning.py`): theo storyboard mới (CNN→tua ngược→paper IEEE PAMI 1997→tên EBGM). Không tái dùng sc04/05.
2. **Giữ & rút:** với 15 scene gốc còn lại, giảm `self.wait()`/`run_time` khớp cột Δ. Đặc biệt sc20/21/22 hiện có tổng `wait` 35–37s — cắt xuống ~10–14s.
3. **Gộp:** S1 (sc01+02), S13 (sc20+21), S14 (sc22+23+24), S15 (sc27+29+31) — ghép class hoặc dựng scene lấy phần lõi.
4. **Cắt khỏi pipeline render:** sc04, sc05, sc07, sc08, sc19, sc25, sc26, sc28, sc30, sc32 (giữ file, không đưa vào bản final).
5. **Sửa nhãn số liệu S13** đúng cặp pose (98/84/57/18) — tránh lỗi 57% bị gán cross-pose.
6. **Thêm caption ẩn dụ** (`≈ CNN filter` ở S5) để khớp VO.
7. **Lồng tiếng** theo VO Phần B (~150 từ/phút, lối tech-storytelling); căn animation theo VO.
8. **Ghép** qua `scene_full_video.py` theo thứ tự S1→S16.

---
# HẾT KỊCH BẢN EBGM (BẢN 10 PHÚT — HOÀN CHỈNH) 🚀
