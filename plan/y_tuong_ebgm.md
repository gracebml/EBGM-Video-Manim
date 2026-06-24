# 💡 Ý TƯỞNG VIDEO — Elastic Bunch Graph Matching (EBGM)

> **Nguồn gốc:** Wiskott, Fellous, Krüger & von der Malsburg (1999), *"Face Recognition by Elastic Bunch Graph Matching"*, in *Intelligent Biometric Techniques in Fingerprint and Face Recognition*, CRC Press, Ch. 11, pp. 355–396. (Bản rút gọn đã đăng IEEE TPAMI 19(7):775–779, 1997.)
>
> **Phong cách:** 3Blue1Brown / Manim — nền navy sâu, palette lạnh, màu chữ ký lavender `#B8B5FF`, chữ LaTeX thanh lịch, nhịp chậm có chiều sâu học thuật.
>
> **Vai trò trong series:** Đây là **Video 2** của loạt "Nhận dạng mẫu" (Video 1 = Parzen Windows). Video EBGM này được kể trọn vẹn trong **33 scenes** (~13–14 phút), đi từ bài toán → Gabor jets → so khớp displacement → đồ thị khuôn mặt → Face Bunch Graph → thuật toán đàn hồi → nhận dạng → thực nghiệm → thảo luận.

---

## 🎯 1. THÔNG ĐIỆP CỐT LÕI (One-sentence pitch)

> **EBGM nhận dạng khuôn mặt chỉ từ MỘT ảnh/người bằng cách mô tả khuôn mặt thành một ĐỒ THỊ ĐÀN HỒI: các nút là "jet" (đáp ứng sóng Gabor cục bộ) đặt tại các điểm mốc trên mặt, các cạnh là khoảng cách hình học. Một "đồ thị chùm" (Face Bunch Graph) tổng quát giúp tìm chính xác các điểm mốc trên khuôn mặt chưa từng thấy, rồi nhận dạng bằng so sánh độ tương đồng giữa các đồ thị.**

Ba từ khóa kết video: **CỤC BỘ — ĐÀN HỒI — TỔNG QUÁT**.

---

## 🧩 2. BÀI TOÁN & VÌ SAO KHÓ (Introduction của paper)

- Nhiệm vụ: nhận dạng người từ **một ảnh duy nhất**, đối chiếu với gallery cũng **chỉ một ảnh/người**.
- Đây là bài toán **"phân biệt trong điều kiện có biến thiên"** (discrimination-in-the-presence-of-variance):
  - biến thiên do **biểu cảm** (expression),
  - **tư thế đầu** (head pose),
  - **vị trí** (position) và **kích thước** (size).
- Hai cực đoan cổ điển đều đắt đỏ:
  - AI/Computer Vision: mô hình 3D do người thiết kế thủ công.
  - Neural network: học hấp thụ biến thiên từ rất nhiều ví dụ.
  - Cả hai đều thua xa khả năng của hệ thị giác tự nhiên — học bản chất chỉ từ vài ví dụ.
- **Giải pháp EBGM:** dùng cấu trúc tổng quát (đồ thị gắn nhãn đáp ứng wavelet) + tính chất biến đổi tổng quát (ảnh vật thể có xu hướng tịnh tiến, co giãn, xoay, biến dạng trong mặt phẳng ảnh). Cấu trúc này do người thiết kế cung cấp nhưng *rất ít công sức* vì nó tổng quát.

**Visual metaphor:** lưới điểm mốc co giãn "đàn hồi" như mạng nhện dán lên khuôn mặt — đây là hình ảnh thương hiệu của cả video.

---

## 🌊 3. TIỀN XỬ LÝ: GABOR WAVELETS & JETS (Section 2.1)

### 3.1. Vì sao Gabor
- Gabor wavelet = sóng phẳng (plane wave) bị giới hạn bởi một bao Gaussian → "kernel" cục bộ trong cả không gian lẫn tần số.
- **Động cơ sinh học:** giống *receptive field* của tế bào đơn giản trong vỏ thị giác động vật (Pollen & Ronner, Jones & Palmer, DeValois). Có thể suy ra thống kê từ ảnh tự nhiên.
- **DC-free** → bền với thay đổi độ sáng; chuẩn hóa jet → bền với tương phản; định vị giới hạn → bền (vừa phải) với tịnh tiến/biến dạng/xoay/co giãn.

### 3.2. Công thức (cần lên hình)
- Phép biến đổi tại điểm $\vec{x}$:
$$\mathcal{J}_j(\vec{x}) = \int \mathcal{I}(\vec{x}')\,\psi_j(\vec{x}-\vec{x}')\,d^2\vec{x}'$$
- Họ kernel Gabor:
$$\psi_j(\vec{x}) = \frac{k_j^2}{\sigma^2}\exp\!\left(-\frac{k_j^2 x^2}{2\sigma^2}\right)\left[\exp(i\,\vec{k}_j\vec{x}) - \exp\!\left(-\frac{\sigma^2}{2}\right)\right]$$
- Lấy mẫu **5 tần số** ($\nu = 0,\dots,4$) × **8 hướng** ($\mu = 0,\dots,7$) = **40 kernels**:
$$\vec{k}_j = \begin{pmatrix} k_\nu\cos\varphi_\mu \\ k_\nu\sin\varphi_\mu \end{pmatrix},\quad k_\nu = 2^{-\frac{\nu+2}{2}}\pi,\quad \varphi_\mu = \mu\frac{\pi}{8}$$
  với $j = \mu + 8\nu$, $\sigma = 2\pi$. Số hạng thứ hai trong ngoặc làm kernel DC-free.

### 3.3. Jet
- **Jet** $\mathcal{J} = \{\mathcal{J}_j\}$ = tập **40 hệ số phức** tại MỘT điểm ảnh:
$$\mathcal{J}_j = a_j \exp(i\phi_j)$$
  - **Biên độ** $a_j(\vec{x})$: biến thiên *chậm* theo vị trí → ổn định, dùng cho nhận dạng.
  - **Pha** $\phi_j(\vec{x})$: *quay nhanh* theo tần số không gian → nhạy, dùng để định vị chính xác (đo displacement).
- **Visual:** "đĩa xếp chồng" (stack of discs) như trong Figure 1 của paper — 40 đĩa = 40 hệ số. Hoặc "vân tay tần số" tại một điểm.

---

## 🔍 4. SO SÁNH JETS & ƯỚC LƯỢNG DỊCH CHUYỂN (Section 2.1.2–2.1.3)

### 4.1. Vấn đề pha
Hai jet cách nhau vài pixel → pha rất khác dù biểu diễn gần như cùng một đặc trưng → gây nhiễu khi so khớp.

### 4.2. Hai hàm tương đồng
- **Bỏ pha** (mượt, lòng chảo hấp dẫn rộng → hội tụ dễ):
$$\mathcal{S}_a(\mathcal{J},\mathcal{J}') = \frac{\sum_j a_j a_j'}{\sqrt{\sum_j a_j^2 \sum_j a_j'^2}}$$
- **Có pha** (sắc, nhiều cực trị địa phương, nhưng cho định vị chính xác + thông tin dịch chuyển):
$$\mathcal{S}_\phi(\mathcal{J},\mathcal{J}') = \frac{\sum_j a_j a_j' \cos(\phi_j - \phi_j' - \vec{d}\,\vec{k}_j)}{\sqrt{\sum_j a_j^2 \sum_j a_j'^2}}$$

**Visual quan trọng (Figure 2 của paper):** đồ thị độ tương đồng theo dịch chuyển ngang — đường "không pha" trơn & rộng, đường "có pha" gai góc nhưng đỉnh sắc tại 0.

### 4.3. Ước lượng dịch chuyển $\vec{d}$
Khai triển Taylor $\mathcal{S}_\phi$, đặt đạo hàm = 0, giải ra:
$$\vec{d}(\mathcal{J},\mathcal{J}') = \frac{1}{\Gamma_{xx}\Gamma_{yy}-\Gamma_{xy}\Gamma_{yx}}\begin{pmatrix}\Gamma_{yy} & -\Gamma_{yx}\\ -\Gamma_{xy} & \Gamma_{xx}\end{pmatrix}\begin{pmatrix}\Phi_x\\ \Phi_y\end{pmatrix}$$
- **Focus**: số mức tần số dùng để ước lượng ban đầu. Focus 1 → chỉ tần số thấp, dịch chuyển tới 8 pixel; Focus 5 → cả 5 mức, độ chính xác tới ~2 pixel. **Coarse-to-fine**: lặp, mỗi vòng dời jet về gần đích hơn rồi ước lượng lại với focus cao hơn → hội tụ độ chính xác *dưới pixel*.

**Visual metaphor:** la bàn/mũi tên displacement chỉ "phải dịch jet đi đâu để khớp" — như GPS dẫn đường về đúng con mắt.

---

## 🕸️ 5. BIỂU DIỄN KHUÔN MẶT (Section 2.2)

### 5.1. Đồ thị khuôn mặt cá nhân (Individual face graph)
- **Fiducial points** (điểm mốc): đồng tử, khóe miệng, đỉnh mũi, đỉnh/đáy tai... 
- **Labeled graph** $\mathcal{G}$: $N$ nút trên các điểm mốc (gắn jet $\mathcal{J}_n$) + $E$ cạnh gắn **vector khoảng cách** $\Delta\vec{x}_e = \vec{x}_n - \vec{x}_{n'}$.
- Đồ thị **object-adapted** (bám theo đặc trưng), khác với "grid" lưới đều.
- **Image graph**: đồ thị trích từ ảnh, đã loại biến thiên do kích thước/vị trí/xoay trong mặt phẳng.

### 5.2. Face Bunch Graph (FBG) — ý tưởng "đột phá" của paper
- Để tìm điểm mốc trên khuôn mặt **mới**, cần biểu diễn **tổng quát**, không phải mô hình từng người.
- **FBG** = chồng (stack) nhiều đồ thị mẫu lên nhau, **cùng cấu trúc**:
  - mỗi nút mang một **bunch** (chùm) jet — ví dụ "bunch mắt" gồm jet của mắt nhắm/mở, nam/nữ...
  - mỗi cạnh mang khoảng cách **trung bình** $\Delta\vec{x}_e^{\mathcal{B}} = \sum_m \Delta\vec{x}_e^{\mathcal{B}m}/M$.
- Khi khớp với ảnh mới, mỗi nút chọn jet khớp nhất trong bunch — gọi là **local expert**. Tổ hợp các local expert phủ được dải biến thiên **lớn hơn nhiều** so với từng đồ thị mẫu riêng lẻ.
- Kích thước FBG: ~30 mẫu cho normalization, ~70 mẫu cho trích xuất cuối. Không phụ thuộc kích thước gallery.

**Visual metaphor (Figure 3):** mỗi nút là một "cọc đĩa" (stack) nhiều jet; con mắt khớp sẽ "kéo" đúng jet tốt nhất từ chùm ra — như rút quân bài đúng nhất từ một bộ bài tại mỗi điểm mốc.

---

## 🧬 6. ELASTIC BUNCH GRAPH MATCHING (Section 2.3) — TRÁI TIM CỦA THUẬT TOÁN

### 6.1. Hàm tương đồng đồ thị (graph similarity) — dùng khi MATCHING
$$\mathcal{S}_{\mathcal{B}}(\mathcal{G}^{\mathcal{I}},\mathcal{B}) = \frac{1}{N}\sum_n \max_m\big(\mathcal{S}_\phi(\mathcal{J}_n^{\mathcal{I}},\mathcal{J}_n^{\mathcal{B}m})\big) - \frac{\lambda}{E}\sum_e \frac{(\Delta\vec{x}_e^{\mathcal{I}} - \Delta\vec{x}_e^{\mathcal{B}})^2}{(\Delta\vec{x}_e^{\mathcal{B}})^2}$$
- Số hạng 1: trung bình độ tương đồng jet (chọn local expert tốt nhất ở mỗi nút).
- Số hạng 2: phạt biến dạng hình học (metric distortion); $\lambda$ cân bằng "khớp đặc trưng" vs "giữ hình dạng".

### 6.2. Thủ tục khớp (coarse-to-fine, 4 bước) — đây là phần "WOW" của video
- **Step 1 — Tìm vị trí gần đúng:** dồn FBG thành *average graph*, mô hình **cứng** ($\lambda=\infty$), quét lưới (spacing 4 px → 1 px), dùng $\mathcal{S}_a$ (không pha). → Khuôn cứng trượt khắp ảnh tìm khuôn mặt.
- **Step 2 — Tinh chỉnh vị trí & kích thước:** thử dịch $\pm3$ px và 2 kích thước (hệ số 1.18), tính displacement bằng Eq.(8), rescale/reposition lưới. Vẫn $\lambda=\infty$.
- **Step 3 — Tinh chỉnh kích thước & tỉ lệ khung (aspect ratio):** nới x, y độc lập; tăng focus 1→5.
- **Step 4 — Biến dạng cục bộ (Local distortion):** đây là chữ **"Elastic"** — di chuyển TỪNG nút độc lập để tăng tương đồng, đặt $\lambda=2$ (bật phạt hình học), focus 1→5. Chỉ chấp nhận dịch chuyển nhỏ ($d<1$).
- Kết quả: **image graph** chính xác, lưu lại làm biểu diễn khuôn mặt.

**Visual:** lưới cứng đáp xuống mặt (Step1) → căn chỉnh khung (Step2-3) → từng nút "bò" về đúng điểm mốc như nam châm hút, lò xo cạnh giữ lưới khỏi méo (Step4).

### 6.3. Lịch trình 2 giai đoạn (Section 2.3.4)
- **Giai đoạn 1 — Normalization:** ước lượng vị trí + kích thước, cắt & co ảnh về chuẩn 128×128. Dùng 3 FBG theo pose, ~30 ảnh/FBG, ít nút. (~99% định vị đúng, ~20s/ảnh thời đó.)
- **Giai đoạn 2 — Extraction:** khớp chính xác trên ảnh đã chuẩn hóa, FBG ~70 ảnh, nhiều nút nhấn vào nội tâm khuôn mặt. (~10s/ảnh.)

---

## 🏆 7. NHẬN DẠNG (Section 2.4)

- Sau khi có model graphs (từ gallery) và image graphs (từ probe): nhận dạng = so từng image graph với mọi model graph, chọn **độ tương đồng cao nhất**.
- Hàm tương đồng nhận dạng (dùng **không pha** $\mathcal{S}_a$ — bền hơn với biểu cảm):
$$\mathcal{S}_{\mathcal{G}}(\mathcal{G}^{\mathcal{I}},\mathcal{G}^{\mathcal{M}}) = \frac{1}{N'}\sum_{n'} \mathcal{S}_a(\mathcal{J}_{n'}^{\mathcal{I}},\mathcal{J}_{n_{n'}}^{\mathcal{M}})$$
- Tạo **xếp hạng** (ranking); đúng nếu model đúng đứng **hạng 1** (rank one). Rất nhanh: ~300 model graphs/giây, so 1 probe với gallery 250 người < 1 giây.

---

## 📊 8. THỰC NGHIỆM & KẾT QUẢ (Section 3)

### 8.1. Cơ sở dữ liệu
- **FERET** (ARPA/ARL): poses frontal, quarter, half-profile (40–70°), profile; 256×384; ~250 người/gallery, 1 ảnh/người.
- **Bochum**: frontal, 11°, 22°; 108 ảnh gallery.

### 8.2. Kết quả chính (Table 1 & 2) — số liệu cần lên hình
| Model → Probe | Rank 1 |
|---|---|
| frontal fa → fb (FERET) | **98%** (245/250) |
| profile pr → pl | **84%** |
| half-profile hr → hl | **57%** |
| frontal fa → 11° (Bochum) | **94%** |
| frontal fa → 22° (Bochum) | **88%** |

- Frontal–frontal rất cao (98–99%). Profile–profile vẫn tốt (84%). Cross-pose & half-profile khó hơn nhiều (góc xoay không kiểm soát tốt + nhạy với xoay sâu).
- **Bền vững** với xoay sâu **đến ~22°**, sau đó giảm mạnh.
- **Vai trò của pha** (Section 3.2.3, thí nghiệm Maurer): khớp **có pha** → sai số định vị ~1 px (so 5+ px khi không pha); nhận dạng 88% (có pha) vs 67% (không pha) cho ảnh 22°. → Pha cần cho định vị, biên độ cần cho nhận dạng.
- **Tốc độ:** nhanh hơn hệ trước (Lades et al. 1993) rất nhiều cho gallery lớn — vì image graph chỉ trích MỘT lần rồi so nhanh.

---

## 🗣️ 9. THẢO LUẬN & SO SÁNH (Section 4) — phần cuối video

- Hệ **tổng quát**, cho bài toán **in-class recognition** bất kỳ (không chỉ mặt), không cần huấn luyện lớn — chỉ cần vài ví dụ điển hình để dựng bunch graph.
- So với **PCA / Eigenfaces** (Turk & Pentland, Moghaddam & Pentland): PCA tuyến tính trong không gian ảnh → kém với biến thiên hình học, nhạy với che khuất & xoay sâu (frontal cao nhưng profile/half-profile thấp). EBGM tách biểu diễn hình học (cạnh) khỏi đặc trưng cục bộ (jet) → mạnh hơn ở biến dạng/pose.
- So với **Lanitis et al. / deformable models**: cũng dùng graph-matching + warp về hình dạng trung bình, nhưng EBGM dùng bunch của jet (đặc trưng giàu hơn) và mô hình lò xo đơn giản.
- So với **Yuille (user-defined features)**: phải lập trình lại đặc trưng cho mỗi loại vật thể; EBGM học bằng ví dụ.
- So với **hệ trước (Lades et al. 1993)**: thêm thông tin **pha** để định vị chính xác, thêm **object-adapted grid** & **FBG** để khớp người chưa từng thấy trong 1 lần → tăng tốc nhận dạng từ database lớn.
- **Hạn chế:** xoay sâu lớn (đổi pose nhiều) vẫn khó; chưa khảo sát robust với ánh sáng/nền phức tạp.

---

## 🎬 10. KIẾN TRÚC KỂ CHUYỆN — 33 SCENES (mapping)

| Act | Scenes | Nội dung |
|---|---|---|
| **0. Mở đầu** | 1–3 | Hook (1 ảnh/người) · Bài toán biến thiên · Bridge giới thiệu EBGM |
| **1. Gabor & Jet** | 4–8 | Vì sao cục bộ · Gabor kernel · 5×8=40 · Jet · Biên độ vs pha |
| **2. So jet & displacement** | 9–13 | Vấn đề pha · $\mathcal{S}_a$ · $\mathcal{S}_\phi$ · Ước lượng $\vec{d}$ · Focus coarse-to-fine |
| **3. Biểu diễn mặt** | 14–18 | Fiducial points · Image graph · Cần model tổng quát · FBG/bunch · Local expert |
| **4. Elastic matching** | 19–25 | $\mathcal{S}_\mathcal{B}$ · Mục tiêu · Step1 · Step2 · Step3 · Step4 (elastic) · 2-stage schedule |
| **5. Nhận dạng** | 26–28 | Lưu model graph · $\mathcal{S}_\mathcal{G}$ recognition · Ranking rank-1 |
| **6. Thực nghiệm** | 29–32 | Databases & poses · Bảng kết quả · Cross-pose/robust ~22° · So PCA/Lades |
| **7. Kết** | 33 | Outro: CỤC BỘ–ĐÀN HỒI–TỔNG QUÁT + credits |

### Nguyên tắc visual xuyên suốt
- Màu **lavender `#B8B5FF`** = thương hiệu EBGM (đồ thị, lưới đàn hồi, jet "thắng").
- Mọi đối tượng xuất hiện bằng `Write`/`Create`/`FadeIn`, không "pop"; `LaggedStart` cho chuỗi.
- Công thức `MathTex` tô màu từng phần; phụ đề tiếng Việt `Text` font Be Vietnam Pro; thuật ngữ Anh dùng JetBrains Mono.
- 3 "Wow moments" lớn: (a) Gabor jet phân rã ra 40 đĩa, (b) đồ thị lưới co giãn đàn hồi bò về điểm mốc, (c) FBG chọn local expert sáng bừng.
- Tái dùng motif **chữ ký lavender** & nền navy để đồng bộ với Video 1 (Parzen).

---

## 📚 11. TÀI LIỆU THAM KHẢO (cho scene credits)

1. Wiskott, L., Fellous, J.-M., Krüger, N., & von der Malsburg, C. (1999). *Face Recognition by Elastic Bunch Graph Matching.* CRC Press, Ch. 11.
2. Wiskott, L., et al. (1997). IEEE TPAMI 19(7):775–779.
3. Lades, M., et al. (1993). *Distortion invariant object recognition in the dynamic link architecture.* IEEE Trans. Computers.
4. Daugman, J. (1988). Complete discrete 2-D Gabor transforms.
5. Turk, M., & Pentland, A. (1991). *Eigenfaces for recognition.*

---
# HẾT FILE Ý TƯỞNG 💡
