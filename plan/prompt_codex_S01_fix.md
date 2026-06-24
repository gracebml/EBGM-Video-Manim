# 🤖 PROMPT cho CODEX — SỬA cảnh "2 người nhận ra nhau" trong S01

> File: `release/scene_S01_cold_open.py` (class `S01_ColdOpen`). **CHỈ sửa đoạn mở đầu (B0): cảnh phố + khoảnh khắc nhận ra** (hiện ở dòng ~65–134). **GIỮ NGUYÊN** phần sau (ảnh `face.png`, landmark teaser, two branches, card Verification/Identification). Render lại `-qh`, giữ đúng tổng thời lượng (~25.73s, |Δ|≤0.3s).

## VẤN ĐỀ HIỆN TẠI (phải khắc phục)
1. **Chồng lấp & rối:** quá nhiều phần tử nhỏ cùng lúc ở vùng giữa — `halo` trên A, `friend_lock` (2 vòng) trên B, `recognition_badge` (checkmark) ở giữa, cộng `city_icons` (camera/scan/vòng đồng tâm), `buildings`, `window_glints`. Mắt không biết nhìn đâu.
2. **Hai người dịch sát vào nhau** (A shift phải tổng +2.45, B shift trái tổng −2.05) → gần đụng nhau, lộn xộn.
3. **Không có điểm nhấn:** khoảnh khắc "nhận ra" không nổi bật, không "wow".

## MỤC TIÊU
Khoảnh khắc **A nhận ra B** phải **RÕ RÀNG, NỔI BẬT, sạch sẽ** — một tiêu điểm duy nhất, không chồng lấp.

## YÊU CẦU CỤ THỂ

### 1. Dọn nền cho thoáng
- **XOÁ hẳn `city_icons`** (camera_icon, scan_icon, vòng đồng tâm) — không liên quan, gây nhiễu. Bỏ luôn 2 helper `camera_icon`/`scan_icon` nếu không dùng chỗ khác.
- `buildings`: giảm còn ~5 khối, opacity **0.10** (mờ hơn). `window_glints`: giảm còn 3–4 đốm, opacity 0.10. `horizon` opacity 0.25.
- Nền chỉ là gợi ý "đường phố ban đêm", KHÔNG cạnh tranh tiêu điểm.

### 2. Bố trí 2 người — KHÔNG để đụng/đè nhau
- `person_a` (ACCENT_CYAN) ở **trái**, `person_b` (ACCENT_LAVENDER) ở **phải**, kích thước to hơn chút (scale ~1.15) cho dễ thấy.
- Họ bước **lại gần nhau nhưng DỪNG với khoảng cách rõ ràng** giữa hai đầu (tối thiểu ~2.8 đơn vị giữa 2 tâm đầu). Ví dụ: A dừng ở khoảng `LEFT*2.0`, B ở `RIGHT*2.0`. **Tổng quãng đi vừa phải**, không dồn vào tâm.
- Khoảng giữa 2 người để TRỐNG cho hiệu ứng nhận ra (xem mục 3) — không đặt người/nhà ở đó.

### 3. Khoảnh khắc "NHẬN RA" — một tiêu điểm mạnh (đặt đúng lúc đọc từ "recognises")
Dùng `recog_t = word_start(T, "recogn") or 3.5`. Tại mốc này, làm **một chuỗi hiệu ứng hội tụ về 1 ý**, theo thứ tự nhanh:
- **(a) Tia nhận ra A → B:** vẽ một **đường sáng cong/thẳng nối từ đầu A sang đầu B** (ACCENT_LAVENDER, stroke ~4, có glow), bằng `Create` nhanh (~0.4s); kèm **một chấm sáng chạy dọc** đường đó từ A tới B (`MoveAlongPath`) — như "ánh nhìn" bắn sang.
- **(b) B bừng sáng:** khi chấm tới B, **đầu B phát một vòng xung sáng** (1 `Circle` nở ra rồi mờ — `GrowFromCenter` + fade, ACCENT_MINT/lavender), và đầu B **scale 1.0→1.18→1.0** (nhấn). CHỈ 1 vòng, không phải 2–3 vòng chồng.
- **(c) Nhãn nổi bật:** **một** nhãn lớn `en_label("Recognized!", color=ACCENT_MINT, scale=0.6, bold=True)` (hoặc dấu ✓ to) hiện **phía trên khoảng trống giữa 2 người**, `FadeIn(scale=0.8→1.0)` + nhấp nháy nhẹ 1 lần. KHÔNG đặt badge nhỏ + nhãn cùng lúc — chỉ 1 phần tử chốt.
- **(d) Camera:** đẩy nhẹ về phía B (`self.camera.frame.animate.scale(0.92).move_to(person_b)`) để dồn sự chú ý — rồi ở beat sau zoom tiếp vào mặt B (đã có sẵn cho phần `face.png`).

> Nguyên tắc: tại một thời điểm **chỉ 1 hành động chính sáng nhất** (tia → xung → nhãn), các thứ khác phải mờ/đứng yên. Không bật đồng thời nhiều ring/badge.

### 4. Chuyển sang phần sau (giữ nguyên logic cũ)
- Hết B0, **fade gọn** tia/xung/nhãn + 2 người + nền, rồi mới `FadeIn(face_image)` như code hiện tại. Đảm bảo **không sót phần tử nào** của cảnh phố chồng lên ảnh mặt.

## RÀNG BUỘC
- Chỉ sửa vùng B0 (cảnh phố + nhận ra). Phần `face.png` teaser, two branches, Verification/Identification, final badge **giữ nguyên**.
- Mọi text qua `en_label` (LaTeX Latin Modern) — KHÔNG `Text(font=...)`. English-only, không phụ đề.
- Giữ palette `_common.py`. Tổng thời lượng = audio (~25.73s), |Δ|≤0.3s — kiểm bằng ffprobe.
- Không để bất kỳ 2 nhóm phần tử nào đè chồng tại cùng vùng cùng lúc.

## LÀM
Sửa `release/scene_S01_cold_open.py`, render `manim -qh --disable_caching release/scene_S01_cold_open.py S01_ColdOpen`, đo ffprobe, mô tả ngắn thay đổi + Δ rồi dừng chờ duyệt.
