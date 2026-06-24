# 🤖 PROMPT cho CODEX — Thiết kế LẠI HOÀN TOÀN frame "Pure math + signal processing" (S03, beat B7)

> File: `release/scene_S03_pre_deeplearning.py`. **CHỈ thay beat B7** (hiện ở dòng ~484–512: `math_title`, `math_panel`, `dl_icon`, `Sigma`, `integral`, `kernel` "filter", `wave_in`, `env`, `wave_out`, `flow1/2/3`) và cập nhật lại nhóm `FadeOut(...)` ở cuối scene (dòng ~589) cho khớp mobject mới. **GIỮ NGUYÊN** mọi beat khác (B0–B6, B8–B12) và tổng thời lượng (57.21s). Beat này nằm trong segment 7, kết thúc tại `seg_end(T, 7)` (~34.7s).

## VẤN ĐỀ (bỏ hẳn)
Frame hiện tại là một **dãy ký hiệu rời rạc vô nghĩa**: hộp net gạch chéo + `Σ` + `∫` + vòng tròn "filter" + ellipse + 2 sóng + flow lines — bày ngang trong 1 panel. Nhìn rối, không truyền tải ý gì. **Xoá toàn bộ các phần tử này.**

## Ý NGHĨA CẦN TRUYỀN TẢI (lời thoại seg 7)
> "Not with deep learning, but with **pure mathematics and signal processing**."
- Một phép **tương phản 2 vế rõ ràng**: **Deep learning (KHÔNG dùng)** ❌ → **Toán học & Xử lý tín hiệu (cách họ chọn)** ✅.
- Vế phải phải **CÓ NGHĨA và báo trước Gabor** (S05): ý "phân tích ảnh bằng *bộ lọc sóng* (convolution), không cần học từ dữ liệu".

## THIẾT KẾ MỚI — tương phản trái→phải, MỖI VẾ MỘT Ý DUY NHẤT
Chia màn 2 nửa, có **divider dọc mảnh + mũi tên `→`** ở giữa (trái sang phải = "thay vì… ta dùng…").

### Nửa TRÁI — "Deep learning" (mờ dần, bị loại)
- Tiêu đề nhỏ `Deep learning` (màu `TEXT_MUTED`).
- MỘT cụm gọn: mạng nơ-ron nhỏ (2–3 lớp chấm nối cạnh) + icon nhỏ `data + GPU`.
- Khi đọc "Not with deep learning" → cụm này **hiện rồi mờ xuống opacity ~0.25 + một dấu ✗ coral** đè lên. Ý: "KHÔNG đi đường này".

### Nửa PHẢI — "Mathematics + Signal processing" (sáng, đường được chọn) ⭐
Tiêu đề `Mathematics + Signal processing` (teal/mint, bold). Bên dưới là **MỘT animation sạch, liền mạch** (KHÔNG bày nhiều ký hiệu):
1. **Tín hiệu vào:** một hàng tín hiệu/đường sóng ngang lấy từ ảnh (gợi "1 lát ảnh"). Có thể đặt 1 patch ảnh nhỏ (`face.png` crop) ở đầu để rõ "đây là ảnh".
2. **Bộ lọc sóng (wavelet):** dựng nhanh `ψ` = **sóng sin nằm dưới một bao Gaussian** (sin × bell) — vẽ gọn, đẹp (đây chính là Gabor, báo trước S05).
3. **Convolution sweep:** cho wavelet `ψ` **trượt dọc** tín hiệu trái→phải (MoveAlongPath/animate shift), để lại **một đường đáp ứng** (response) mượt phía dưới. Đây là "signal processing = quét ảnh bằng bộ lọc sóng".
4. **MỘT công thức duy nhất, đặt sạch sẽ:** `\mathcal{I} * \psi` (convolution) hoặc `\int \mathcal{I}(x)\,\psi(x)\,dx` — MathTex, 1 dòng, KHÔNG rải Σ/∫ lung tung.
5. Nhãn nhỏ dưới: `convolve with wave filters` (mint).

> Nguyên tắc: vế trái **mờ trước**, rồi vế phải **build lên thành tiêu điểm**. Không để 2 vế cùng nổi. Không còn ký hiệu rời rạc — chỉ 1 mạch "ảnh → lọc sóng → đáp ứng" + 1 công thức.

### Nhịp (trong seg 7, ~29.16→34.7)
- ~29.16–30.6: "Not with deep learning" → cụm net trái hiện → mờ + ✗.
- ~30.6–33.2: "pure mathematics and signal processing" → vế phải build: patch ảnh → dựng wavelet `ψ` → trượt convolution → đường đáp ứng + công thức.
- ~33.2–34.7: chốt: tiêu đề phải sáng mint, `Indicate` công thức 1 nhịp (báo trước "đây là Gabor — sẽ gặp lại").

## RÀNG BUỘC
- Chỉ sửa B7 + nhóm FadeOut cuối. Không đụng beat khác; tổng vẫn 57.21s (|Δ|≤0.3s, ffprobe).
- English-only, text qua `en_label`/`MathTex` (LaTeX Latin Modern), KHÔNG phụ đề. Palette `_common.py` (teal/mint cho vế "được chọn", coral cho ✗, lavender cho `ψ`/highlight).
- Một tiêu điểm tại một thời điểm; KHÔNG bày ký hiệu rời rạc; mũi tên/divider gọn, không đè chữ.
- Wavelet phải đẹp & rõ (sin dưới bao Gaussian) — đây là điểm nối sang S05 Gabor.

## ASSETS
- Dùng sẵn `assets/face.png` cho patch ảnh đầu vào (tùy chọn, có fallback vẽ 1 ô lưới pixel nếu không muốn ảnh). Không cần ảnh mới.

## LÀM
Sửa `release/scene_S03_pre_deeplearning.py` (chỉ B7), render `manim -qh --disable_caching release/scene_S03_pre_deeplearning.py S03_PreDL`, đo ffprobe, mô tả ngắn + Δ rồi dừng chờ duyệt.
