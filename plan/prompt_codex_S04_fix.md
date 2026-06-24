# 🤖 PROMPT cho CODEX — SỬA cảnh "Three Pillars" trong S04

> File: `release/scene_S04_idea.py` (class `S04_Idea`, `ThreeDScene` phẳng phi=0). **Chỉ sửa layout + cách dọn phần tử trong phần 3 pillars**; GIỮ NGUYÊN ý tưởng kịch bản, thứ tự beat theo `seg_end(T, k)`, và tổng thời lượng = audio (**35.85s, |Δ|≤0.3s**, kiểm bằng `ffprobe`). Có 5 segment → 5 beat (0: setup "không phải pixel/PCA", 1: Image Graph, 2: Wavelet Jet, 3: Face Bunch Graph, 4: gom 3 cột + strengths + khung tổng).

## VẤN ĐỀ HIỆN TẠI (phải khắc phục)

### 1. Khung (frame) bị chồng lấp
- Ở beat cuối, `system_box = SurroundingRectangle(pillars, buff=0.18)` bao cả 3 panel. **Cạnh dưới của khung (~y −2.38) cắt ngang qua hàng `strengths` cards** (3 thẻ ở `y=-2.35`, cao 0.78 → trải `y −2.74…−1.96`). Đường viền khung xuyên qua thẻ → trông như chồng/đè.
- 3 panel (`width=3.35` tại `xs=[-3.65, 0, 3.65]`) chỉ cách nhau **gutter ~0.3** → quá sát; các `heads` ("3. Face Bunch Graph"), `pose_labs` ("half-profile", "profile") và note dễ **tràn mép panel / chạm cột bên cạnh**.
- `title` (UP*2.35) và `balance` (UP*2.9) nằm sát mép trên của `system_box` (~y 2.18) → chật.

### 2. Vài chi tiết bị **fade mà chưa mất hẳn** (bóng ma)
Các phần tử "phản ví dụ" (reject) chỉ bị `.set_opacity(0.2–0.25)` rồi **không bao giờ xoá**, để lại bóng mờ lảng vảng trong khung:
- `note_pixels` ("not raw pixels") và `note_pca` ("not linear PCA"): beat 1 dim xuống **0.25** rồi treo luôn tới hết cảnh.
- `patch` (color_patch), `patch_lbl` ("not color"), `arrow_to_jet`: beat 3 dim xuống **0.2** rồi treo luôn — nằm mờ mờ chồng lên vùng cột 2.

## MỤC TIÊU
Phần 3 pillars phải **sạch, thoáng, các cột tách bạch**; phần tử "phản ví dụ" sau khi làm xong nhiệm vụ phải **biến mất hẳn (FadeOut)**, không để bóng mờ; khung tổng ở cuối **ôm gọn 3 cột mà KHÔNG cắt vào tiêu đề cột hay hàng strengths**.

## YÊU CẦU CỤ THỂ

### A. Xoá hẳn phần tử "phản ví dụ" thay vì dim
- **Beat 1** (reveal Image Graph): thay `note_pixels.animate.set_opacity(0.25)` và `note_pca.animate.set_opacity(0.25)` bằng **`FadeOut(note_pixels)`, `FadeOut(note_pca)`** (chúng đã được minh hoạ xong cùng `bad_pixels`/`pca_line` vốn đã FadeOut). Sau beat 1 vùng trên giữa phải trống.
- **Beat 3** (reveal Face Bunch Graph): thay 3 dòng `patch.animate.set_opacity(0.2)`, `patch_lbl.animate.set_opacity(0.2)`, `arrow_to_jet.animate.set_opacity(0.2)` bằng **`FadeOut(patch)`, `FadeOut(patch_lbl)`, `FadeOut(arrow_to_jet)`**. Không để bóng "not color" còn lại.
- Việc dim cột đã hoàn tất (p1/graph/jet… về 0.28–0.36 rồi cuối beat 4 kéo lại 0.72/0.78) **giữ nguyên** — đó là chủ ý "làm mờ cột cũ, nổi cột đang nói, cuối gom lại cả ba". Chỉ xử lý các phần tử reject ở trên.

### B. Giãn 3 cột cho tách bạch, không tràn mép
- Tăng khoảng cách cột và thu nhẹ panel: ví dụ `xs = [-3.95, 0.0, 3.95]`, `panel(width=3.05, height=3.95)` → gutter ≈ 0.85, vẫn nằm trong khung hình (mép ngoài ~±5.5 < 7.1). Tinh chỉnh để **không phần tử nào của một cột chạm cột kế bên**.
- `heads`, `*_note`, `pose_labs`: đảm bảo nằm **trong bề ngang panel của cột đó**. Nếu "3. Face Bunch Graph" còn rộng, giảm `scale` xuống ~0.28 hoặc rút gọn; `pose_labs` giữ `scale ~0.20` và kéo `x` về trong panel 3.
- Đẩy nhẹ tâm các pillar lên (ví dụ panel center `y ≈ 0.05`) để chừa chỗ cho hàng `strengths` bên dưới.

### C. Khung tổng + strengths không cắt nhau
- Hạ hàng `strengths` xuống rõ ràng dưới khung: ví dụ `y = -2.95` (3 thẻ tại `x ≈ [-3.85, 0, 3.85]`), và để `system_box` (SurroundingRectangle các pillar, `buff≈0.2`) có **cạnh dưới cao hơn mép trên thẻ ≥ 0.25**. Kiểm tra số học: `panel_bottom = panel_center_y − height/2`; `box_bottom = panel_bottom − buff`; `card_top = card_y + 0.39`; phải có `box_bottom − card_top ≥ 0.25`.
- Nếu cần, có thể **chỉ bao 3 panel (không bao heads/strengths)** và đặt strengths như một hàng độc lập bên dưới khung, có khoảng hở rõ. `balance` giữ ở trên (UP*2.9) nhưng đảm bảo **không chạm mép trên `system_box`** (hạ box hoặc nâng balance để hở ≥ 0.2).
- `title` ("Three Pillars") phải nằm **trên** `system_box`, không bị viền khung đè.

### D. Tự kiểm tra bằng frame
Render `-ql` rồi trích vài frame để soi chồng lấp:
- t ≈ 8.5s (sau beat1: đã sạch note_pixels/note_pca?)
- t ≈ 22s (sau beat3: đã sạch patch/"not color"/arrow?)
- t ≈ 30s (beat4: khung tổng KHÔNG cắt strengths, 3 cột đều, không bóng ma)

## RÀNG BUỘC
- Chỉ chỉnh layout/dọn phần tử trong S04; **không đổi** thông điệp, nhãn tiếng Anh, palette `_common.py`, hay cơ chế `beat_to(seg_end(T,k))`.
- Mọi text qua `en_label`/`label(...)` (LaTeX Latin Modern) — KHÔNG `Text(...)`, `font=...`, `Paragraph`, không phụ đề, English-only.
- Giữ `add_sound`, giữ `ThreeDScene` phi=0 hiện tại (không cần đổi sang MovingCameraScene).
- Tổng thời lượng khớp audio **35.85s (|Δ|≤0.3s)** — đo `ffprobe -v error -show_entries format=duration -of csv=p=0 <mp4>`.
- Sau khi sửa: `python3 -m py_compile release/scene_S04_idea.py` và
  `rg -n "Text\(|font=|Paragraph|make_subtitle|[À-ỹ]" release/scene_S04_idea.py` (không được khớp).
