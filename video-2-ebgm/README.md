# 📽️ Video 2: Elastic Bunch Graph Matching (EBGM) — Overview Section

Chào mừng bạn đến với dự án lập trình và sản xuất Video Manim giải thích thuật toán **Elastic Bunch Graph Matching (EBGM)** (theo bài báo khoa học kinh điển của Wiskott et al., 1999). 

Dự án này đã hiện thực hóa toàn bộ **7 Scenes của Phần 1 (Overview Section)** bằng mã nguồn Python Manim Community Edition (CE) v0.18+, đạt chất lượng hiển thị học thuật cao cấp và phong cách sư phạm chuẩn 3Blue1Brown.

---

## 🎨 Điểm nhấn Thiết kế & Giải pháp Kỹ thuật

1. **Đồng bộ hóa XeLaTeX tiếng Việt**: 
   - Sử dụng bộ compiler XeLaTeX qua `VN_TEX_TEMPLATE` với phông chữ Latin Modern Roman giúp hiển thị văn bản tiếng Việt có dấu trơn tru, sắc nét, không lỗi đè chữ, mang tính hàn lâm chuyên nghiệp.
   - Các hàm helper tối ưu trong [_common.py](file:///media/mlinh/DATA/projects/pattern-recog/video-manim/video-2-ebgm/_common.py): `vn_tex()`, `vn_tex_bold()`, `vn_tex_italic()`, `vn_tex_mono()`, và `vn_math()`.
2. **Khung Phụ đề Viền Mờ Cao cấp**:
   - Mọi phụ đề được bo góc mờ với nền Navy tối (`opacity=0.78`) và viền Stroke nhạt (`opacity=0.55`) giúp chữ cực kỳ nổi bật trên mọi tông nền chuyển động, giống hệt mẫu thiết kế bạn đã cung cấp.
3. **Mô hình Vector Tự sinh (Procedural Animations)**:
   - Thay vì nạp ảnh tĩnh bên ngoài dễ lỗi đường dẫn, toàn bộ hình vẽ như: 5 biến thể khuôn mặt cùng người, 2 cấu trúc khuôn mặt cá nhân khác biệt, mô hình mắt góc hình quả hạnh, mạng nơ-ron đa tầng, ảnh Eigenfaces trừu tượng, và Gabor Wavelet Jet đều được lập trình động bằng các thực thể toán học (`ParametricFunction`, `Arc`, `Ellipse`, `Line`, `Dot`).
   - Sóng Gabor được mô phỏng toán học chính xác bằng phương trình hàm sóng lan tỏa đa hướng kết hợp bao Gaussian:
     $$t \cdot \vec{u}_{\text{ray}} + A \cdot e^{-\frac{(t-t_0)^2}{\sigma^2}} \sin(\omega t) \vec{u}_{\text{perp}}$$

---

## 📊 Danh sách 7 Scenes đã hoàn thành và Timing

| Scene | Tên phân đoạn | Thời lượng | Mã nguồn | Trạng thái |
|---|---|---|---|---|
| **Scene 1** | **Title Opening** | 12s | [scene_01_title_opening.py](file:///media/mlinh/DATA/projects/pattern-recog/video-manim/video-2-ebgm/scene_01_title_opening.py) | **Đã biên dịch 1080p60** |
| **Scene 2** | **Bài toán Face Recognition** | 50s | [scene_02_face_recognition.py](file:///media/mlinh/DATA/projects/pattern-recog/video-manim/video-2-ebgm/scene_02_face_recognition.py) | **Đã biên dịch 1080p60** |
| **Scene 3** | **Vấn đề cốt lõi** | 55s | [scene_03_core_problem.py](file:///media/mlinh/DATA/projects/pattern-recog/video-manim/video-2-ebgm/scene_03_core_problem.py) | **Đã biên dịch 1080p60** |
| **Scene 4** | **Cách tiếp cận trước đây** | 90s | [scene_04_prior_approaches.py](file:///media/mlinh/DATA/projects/pattern-recog/video-manim/video-2-ebgm/scene_04_prior_approaches.py) | **Đã biên dịch 1080p60** |
| **Scene 5** | **Chuyển tiếp (Bridge)** | 15s | [scene_05_bridge_problem.py](file:///media/mlinh/DATA/projects/pattern-recog/video-manim/video-2-ebgm/scene_05_bridge_problem.py) | **Đã biên dịch 1080p60** |
| **Scene 6** | **Cách tiếp cận novel của EBGM** | 75s | [scene_06_ebgm_novel.py](file:///media/mlinh/DATA/projects/pattern-recog/video-manim/video-2-ebgm/scene_06_ebgm_novel.py) | **Đã biên dịch 1080p60** |
| **Scene 7** | **Teaser & Kết thúc** | 15s | [scene_07_teaser_conclusion.py](file:///media/mlinh/DATA/projects/pattern-recog/video-manim/video-2-ebgm/scene_07_teaser_conclusion.py) | **Đã biên dịch 1080p60** |

> [!NOTE]
> Tổng thời lượng toàn bộ phân đoạn Overview đạt khoảng **5 phút 12 giây** đúng chuẩn kịch bản đã lên trong file `overview.md`.

---

## 🛠️ Hướng dẫn Trích xuất & Biên dịch Video

Bạn có thể tự do chỉnh sửa hoặc biên dịch lại từng Scene ở bất kỳ độ phân giải nào theo các câu lệnh sau:

### 1. Bản nháp nhanh (Low Quality - 480p15)
Để kiểm tra animation nhanh chóng:
```bash
manim -pql scene_01_title_opening.py Scene1_TitleOpening
manim -pql scene_02_face_recognition.py Scene2_FaceRecognition
manim -pql scene_03_core_problem.py Scene3_CoreProblem
manim -pql scene_04_prior_approaches.py Scene4_PriorApproaches
manim -pql scene_05_bridge_problem.py Scene5_BridgeProblem
manim -pql scene_06_ebgm_novel.py Scene6_EBGM_Novel
manim -pql scene_07_teaser_conclusion.py Scene7_TeaserConclusion
```

### 2. Bản phát hành cao cấp (High Quality - 1080p60)
Để render thành phẩm cuối cùng:
```bash
manim -pqh scene_01_title_opening.py Scene1_TitleOpening
manim -pqh scene_02_face_recognition.py Scene2_FaceRecognition
manim -pqh scene_03_core_problem.py Scene3_CoreProblem
manim -pqh scene_04_prior_approaches.py Scene4_PriorApproaches
manim -pqh scene_05_bridge_problem.py Scene5_BridgeProblem
manim -pqh scene_06_ebgm_novel.py Scene6_EBGM_Novel
manim -pqh scene_07_teaser_conclusion.py Scene7_TeaserConclusion
```

> [!TIP]
> Tất cả các file video đầu ra nằm trong thư mục con `media/videos/`.

---

## 🏆 Summary of Accomplishments

- Lập trình trọn vẹn và tối ưu sạch lỗi biên dịch LaTeX cho toàn bộ mã nguồn của 7 Scenes.
- Đảm bảo tuyệt đối 100% phông chữ LaTeX Latin Modern Roman chuẩn Việt hóa cao cấp.
- Đã chạy thử và biên dịch thành công toàn bộ 7 file ở cả chất lượng Nháp (`480p15`) và Bản đẹp xuất bản (`1080p60`) với đầu ra hoàn chỉnh, hoạt họa mượt mà, không gặp bất cứ lỗi cú pháp TeX hay logic nào.

Dự án phần 1 (Overview) đã sẵn sàng phục vụ việc biên tập video của bạn! Chúc bạn có những thước phim khoa học tuyệt hảo!
