# 🤖 PROMPT cho CODEX — THIẾT KẾ LẠI Scene 2 (S02 "Why face recognition is hard")

> File: `release/scene_S02_why_hard.py` (class `S02_WhyHard`). Thiết kế lại **toàn bộ** phần hình. Giữ: `add_sound`, khung `beat_to`, English/LaTeX, palette, tổng thời lượng = audio (**29.21s**, |Δ|≤0.3s). Render `-qh`.

## VẤN ĐỀ HIỆN TẠI (bỏ hẳn)
- Dùng **mesh mặt 3D trừu tượng** (Surface ellipsoid + sphere mắt) → vô nghĩa, không ai hiểu.
- **`begin_ambient_camera_rotation`** xoay chậm liên tục → ì ạch, "slow motion" chán.
- → **BỎ hẳn camera rotation. BỎ ThreeDScene** (đổi sang `Scene` hoặc `MovingCameraScene`, 2D). **BỎ mesh mặt.**

## Ý NGHĨA SCENE (phải truyền tải rõ)
"Cái khó của nhận diện khuôn mặt KHÔNG phải phân biệt 2 người — mà là **cùng MỘT người trông rất khác nhau** (biểu cảm, ánh sáng, tư thế). Pixel đổi hoàn toàn = *intra-class variance*. Thuật toán phải **vừa dung thứ** (forgive biến dạng cùng người) **vừa sắc bén** (phân biệt 2 người khác nhau)."

## DÙNG ẢNH THẬT (chính) + nhịp nhanh, nhiều frame
Thay mesh bằng **ảnh thật** (xem mục "ẢNH CẦN TÌM"). Nếu ảnh chưa có → dùng helper fallback (mục "FALLBACK") để vẫn render được.

### Storyboard mới (map theo segment Jessica)
| Beat | Mốc (s) | Thoại | Hình (động, nhiều frame) |
|---|---|---|---|
| B0 | 0.00–1.38 | "What troubles AI the most?" | Nhãn lớn `What troubles AI most?` punch-in; 1 ảnh mặt người (neutral) fade vào giữa. |
| B1 | 1.88–3.80 | "Not the difference between two people" | **2 người KHÁC nhau** cạnh nhau (ảnh `s2_personA`, `s2_personB`); nhãn `Different people` + dấu `✗ not the hard part`; rồi **mờ đi** (đây KHÔNG phải vấn đề chính). |
| B2 | 4.54–8.54 | "the same person can look like two completely different people" | **TÂM ĐIỂM:** 1 identity → **montage nhanh** 4–5 ảnh CÙNG người ở các trạng thái khác nhau, kiểu **film-strip trượt ngang** hoặc cut nhanh (mỗi ảnh ~0.6s). Nhãn `Same person` (mint). Cảm giác "tưởng 2 người khác nhau". |
| B3 | 9.20–12.40 | "When you smile, frown, or light hits from below" | **Cut nhanh 3 ảnh** cùng người: `smile` → `frown` → `lit-from-below`, mỗi ảnh nhãn nhỏ tương ứng (`smile`/`frown`/`under-lit`), pop scale nhẹ. Nhịp dứt khoát. |
| B4 | 12.68–14.58 | "the pixel matrix changes entirely" | Phủ **lưới pixel** lên 2 trong số ảnh đó; bật **heatmap khác biệt màu coral bùng toàn khung** (entire matrix flares). Nhãn `Pixel matrix changes entirely`. |
| B5 | 15.42–17.40 | "intra-class variance" | Nhãn lớn `Intra-class variance` (lavender) punch-in + khung bao; ảnh nền mờ. |
| B6 | 18.08–20.62 | "must resolve this paradox" | Tách màn **2 cột** đối lập (divider dọc "quét" qua); nhãn `Paradox`. |
| B7 | 21.06–24.50 | "tolerant enough to forgive one person's deformations" | Cột trái `Tolerant` (mint): gom **các ảnh cùng người** vào 1 nhóm + dấu ✓ "forgive variation". |
| B8 | 24.72–28.72 | "sharp enough to distinguish tiniest details between two different people" | Cột phải `Sharp` (cyan): **2 người khác nhau trông giống nhau**; **zoom punch-in** vào 1 chi tiết nhỏ khác biệt (khoanh tròn), nhãn `tiniest detail`. |

### Kỹ thuật làm cho "động, nhiều frame"
- **Cut/montage nhanh** thay vì giữ tĩnh: dùng `FadeIn/FadeOut` ngắn (run_time 0.3–0.5s), `Transform` ảnh→ảnh, film-strip `shift`.
- **Pixel-diff flare:** lưới `Square` đổi sang coral đồng loạt (`LaggedStart` rất nhanh / `AnimationGroup`).
- **Punch-in nhãn:** `FadeIn(scale=0.8→1.0)` + `Indicate` 1 nhịp.
- **Camera (nếu MovingCameraScene):** đẩy nhanh vào chi tiết ở B8 (`self.camera.frame.animate.scale(0.6).move_to(detail)`), KHÔNG xoay vòng.
- Mỗi beat **một tiêu điểm**, cái cũ mờ trước khi cái mới vào (chống chồng lấp).

## ẢNH (✅ ĐÃ CÓ ĐỦ trong `assets/`)
Tất cả 7 ảnh đã sẵn sàng, dùng trực tiếp:
- Cùng người 5 trạng thái: `s2_same_neutral.jpg`, `s2_same_smile.jpg`, `s2_same_frown.jpg`, `s2_same_lowlight.jpg`, `s2_same_pose.jpg`
- Hai người khác nhau: `s2_personA.jpg`, `s2_personB.jpg`

**Lưu ý kích thước (để khung ảnh đồng nhất):**
- 6/7 ảnh là **1024×1024 (vuông 1:1)**. Riêng `s2_same_neutral.jpg` là **448×360 (1.24:1)**.
- → Khi đặt ảnh: **fix theo chiều cao cố định** (vd `img.height = 3.0`) và **crop về vuông** cho mọi ảnh để khung đồng nhất (dùng `img` rồi đặt trong một `RoundedRectangle` mask/khung viền chung). Tránh ảnh to nhỏ lệch nhau.
- ⚠️ **Kiểm tra danh tính:** 5 ảnh `s2_same_*` phải là **CÙNG một người** để montage "same person" có nghĩa. Nếu `s2_same_neutral` (đang = face.png) khác người với nhóm còn lại → ưu tiên dùng `s2_same_smile/frown/pose/lowlight` cho montage chính, hoặc bỏ neutral khỏi chuỗi "same person".

## FALLBACK (khi ảnh chưa có → vẫn render được)
Viết helper:
```python
def load_face(name, fallback_style="neutral", color=ACCENT_CYAN):
    from pathlib import Path
    base = Path(__file__).resolve().parents[1] / "assets"
    for ext in (".jpg", ".png", ".jpeg"):
        p = base / f"{name}{ext}"
        if p.exists():
            img = ImageMobject(str(p)); img.height = 3.0; return img
    # fallback: vẽ mặt cách điệu 2D (KHÔNG mesh 3D, KHÔNG xoay)
    return stylized_face_2d(style=fallback_style, color=color)
```
- `stylized_face_2d`: vẽ mặt 2D đơn giản (ellipse + mắt + mũi + miệng) theo style — để bố cục/nhịp vẫn đúng, chỉ thiếu ảnh thật. Khi người dùng thả ảnh vào, tự dùng ảnh.

## RÀNG BUỘC
- KHÔNG ThreeDScene/camera rotation/mesh. 2D, nhịp nhanh.
- English-only, nhãn qua `en_label` (LaTeX Latin Modern), KHÔNG phụ đề.
- Palette `_common.py`; tổng = 29.21s (|Δ|≤0.3s, đo ffprobe).
- Mỗi lúc 1 tiêu điểm, không chồng lấp.

## LÀM
Viết lại `release/scene_S02_why_hard.py`, render `manim -qh --disable_caching release/scene_S02_why_hard.py S02_WhyHard`, đo ffprobe, mô tả ngắn + Δ rồi dừng chờ duyệt.
