# 🤖 PROMPT cho CODEX — THIẾT KẾ LẠI Scene 4 (S04 "Three Pillars / EBGM idea")

> File: `release/scene_S04_idea.py` (class `S04_Idea`). Thiết kế lại phần hình cho **sạch & rõ**. Giữ: `add_sound`, khung `beat_to`, English/LaTeX (`en_label`), palette, tổng = audio (**35.85s**, |Δ|≤0.3s). Render `-qh`. Đổi base sang `MovingCameraScene` (KHÔNG `ThreeDScene`, KHÔNG xoay camera).

## LỖI HIỆN TẠI (thô — phải bỏ/làm lại)
- **Intro B0 nguệch ngoạc:** `bad_pixels` (lưới pixel gạch chéo) + `pca_line` (1 đường + 3 chấm + 1 gạch coral) trôi nổi, nhãn `not raw pixels`/`not linear PCA` — nhìn rời rạc, sơ sài, không rõ nghĩa.
- **Icon 3 trụ schematic/thô:** `face_graph` (chấm trừu tượng), `jet_icon`, `bunch_icon`, `color_patch` — chưa "đọc" ra ý.

## Ý NGHĨA (5 segment Jessica)
EBGM dựng trên **3 trụ cột**, KHÁC với "nhớ pixel" hay "nén tuyến tính (PCA)":
1. **Image Graph** — nhìn mặt như đồ thị các điểm mốc.
2. **Wavelet Jet** — tại mỗi mốc trích "ADN kết cấu", không lấy màu.
3. **Face Bunch Graph** — chồng nhiều đồ thị mẫu để phủ mọi tư thế.
Kết quả: bền với ánh sáng, học từ <100 ảnh, độ chính xác cao.

## THIẾT KẾ MỚI — dùng ảnh thật + icon sạch, mỗi beat 1 tiêu điểm

| Beat | Mốc (s) | Thoại | Hình (sạch, rõ) |
|---|---|---|---|
| B0 | 0.00–7.50 | "EBGM built on three pillars, unlike memorizing pixels or compressing linearly as PCA" | **Ảnh mặt thật `face.png`** ở giữa. Hai thumbnail nhỏ 2 bên trong khung bo góc gọn: TRÁI = phiên bản **pixel hoá** của mặt (mosaic) + nhãn `raw pixels` + **✗ coral**; PHẢI = phiên bản **PCA mờ/nhoè** (blur/ghost average) + nhãn `linear PCA` + **✗ coral**. Cả hai **mờ đi** khi tiêu đề `Three Pillars` hiện. KHÔNG vẽ gạch chéo nguệch ngoạc — dùng thumbnail có khung + dấu ✗ sạch. |
| B1 | 7.50–13.36 | "1. graph connecting landmark points" | Trụ 1 `1. Image Graph`: **ảnh mặt thật nhỏ** với **các chấm mốc** (mắt/mũi/khóe miệng) + **cạnh nối** vẽ đẹp (lavender) overlay → đồ thị rõ ràng. Note `landmarks + edges`. |
| B2 | 13.36–21.96 | "2. extract a wavelet jet, texture DNA, not color" | Trụ 2 `2. Wavelet Jet`: phóng 1 mốc → **jet đẹp = bó/stack ~ nhiều đĩa nhỏ** (gợi 40 hệ số, đồng bộ style S06). Patch màu nhỏ + `not color ✗`; mũi tên gọn → jet. Note `texture DNA`. |
| B3 | 21.96–27.16 | "3. stack many sample graphs into a face-bunch graph" | Trụ 3 `3. Face Bunch Graph`: **vài đồ thị-trên-mặt xếp chồng theo chiều sâu (offset isometric)** thành "chùm"; nhãn pose `frontal / half-profile / profile`. Note `pose samples stacked`. |
| B4 | 27.16–35.32 | "result: robust to lighting, < 100 images, astonishing accuracy" | 3 trụ cùng sáng lại + khung tổng; 3 chip kết quả gọn: `Robust to light` (cyan) · `< 100 images` (teal) · `High accuracy` (mint). |

## NGUYÊN TẮC
- Dùng **ảnh thật `face.png`** cho B0 (giữa) và B1 (trụ Image Graph) → bớt "thô". Có thể tạo "pixel-hoá" bằng cách phủ lưới ô vuông lên ảnh / hạ độ phân giải; "PCA blur" bằng ảnh mờ + opacity.
- Mỗi beat **một tiêu điểm**: khi build trụ mới, **trụ trước hạ opacity** (đang làm rồi — giữ). Không để icon chồng đè/đè chữ.
- Icon phải **đọc ra ý**: graph = mặt + mốc + cạnh; jet = stack đĩa; bunch = đồ thị chồng sâu. KHÔNG dùng chấm/đường trừu tượng rời rạc.
- Mũi tên/khung gọn, đều; nhãn LaTeX (`en_label`), KHÔNG `Text()`, KHÔNG phụ đề.

## ASSETS
- ✅ Dùng sẵn `assets/face.png`. Không cần ảnh mới. Có thể tái dùng helper `load_face`/thử nhiều đuôi như S02/S03 (fallback vẽ mặt 2D nếu thiếu).

## RÀNG BUỘC
- `MovingCameraScene`, không xoay camera. English-only, palette `_common.py`. Tổng = 35.85s (|Δ|≤0.3s, ffprobe).
- Giữ ý nghĩa 3 trụ + kết quả; chỉ làm **sạch & rõ hơn**, bỏ nét nguệch ngoạc.

## LÀM
Viết lại `release/scene_S04_idea.py`, render `manim -qh --disable_caching release/scene_S04_idea.py S04_Idea`, đo ffprobe, mô tả ngắn + Δ rồi dừng chờ duyệt.
