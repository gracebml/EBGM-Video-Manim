# 🤖 PROMPT cho CODEX — LÀM LẠI Scene 1 (S01)

> Đọc kèm `prompt_codex.md` (luật chung: skeleton `beat_to`, helper `load_scene_timing`, English-only, palette `_common.py`, đo bằng ffprobe). File này **ghi đè storyboard cho riêng S01** — bản 3D cũ KHÔNG ăn nhập script, làm lại theo đúng nội dung thoại dưới đây.

---

## 1. NGUYÊN TẮC (đọc trước khi code)
- **Mỗi hiệu ứng phải CÓ Ý NGHĨA, minh họa đúng câu thoại đang đọc.** Không thêm 3D/hiệu ứng trang trí vô nghĩa.
- **Không để hiệu ứng dày đặc, chồng lấp nhau.** Mỗi beat **một tiêu điểm rõ ràng**; cái cũ mờ/đẩy đi trước khi cái mới vào.
- Khớp audio `audio/en/scene_01.mp3` (tổng **25.22s**), nhúng `self.add_sound(...)`, canh beat theo mốc câu bên dưới (lấy từ `transcript.json`).
- **English-only**, KHÔNG phụ đề. Nhãn ngắn trên hình bằng `en_label(...)`.
- Class này có thể là `MovingCameraScene` (cần zoom mượt vào mặt) — KHÔNG cần `ThreeDScene` cho S01.

## 2. ẢNH MẶT THẬT
```python
from pathlib import Path
FACE_PATH = str(Path(__file__).resolve().parents[2] / "assets" / "face.png")  # video-manim/assets/face.png
face_img = ImageMobject(FACE_PATH)
```

## 3. STORYBOARD THEO TỪNG MỐC THOẠI (bám sát)

| Beat | Mốc (s) | Câu thoại | Hình minh họa (ý nghĩa) |
|---|---|---|---|
| B0 | 0.00–4.78 | "You glance at someone you know on the street, and your brain recognises them in a tenth of a second." | **Cảnh phố:** đường chân trời + vài khối nhà đơn giản (silhouette mờ). **Hai người** (figure cách điệu) đi ngược chiều/lướt qua nhau. Tại từ "recognises" (~3.5s) → đầu nhân vật A phát **vòng sáng nhận ra** + 1 tia/ánh nhìn nối A→B (hoặc dấu "!" nhỏ). Giữ tối giản, 2D. |
| B1 | 5.32–7.82 | "But how does a computer recognise a face?" | **Phóng to** (camera zoom mượt) vào MẶT của người B. **Cross-dissolve** từ đầu cách điệu → **ảnh mặt thật `face.png`** (FadeIn/cross-fade, không "pop"). |
| B2 (teaser) | trong 5.32–8.32 | (vẫn câu trên, chuyển ý "computer") | Trên ảnh mặt thật, **vài landmark dot** (2 mắt, mũi, 2 khóe miệng — ~5–6 chấm lavender) **fade in nhẹ** + vài cạnh mảnh nối chúng. **MỜ, thưa, low-opacity** — chỉ gợi ý "máy nhìn mặt thành đồ thị", KHÔNG vẽ lưới dày. |
| B3 | 8.32–10.16 | "The problem has two branches." | Từ ảnh mặt, **tách thành 2 nhánh** (2 đường rẽ sang trái/phải). Ảnh mặt thu nhỏ về giữa-trên. |
| B4 | 11.02–14.92 | "Verification 1:1 — Am I really the owner of this phone?" | Nhánh trái: thẻ **`Verification 1:1`** + icon **điện thoại mở khoá** (1 mặt ↔ 1 mặt). |
| B5 | 15.42–20.54 | "And identification 1:N — Who is this person among millions of records?" | Nhánh phải: thẻ **`Identification 1:N`** + **lưới nhiều mặt nhỏ** (gallery) để 1 mặt dò trong N. |
| B6 | 20.84–24.70 | "Today, we tackle the harder branch. 1:N Identification." | Thẻ **`1:N` sáng lavender** (`ACCENT_LAVENDER`) + nhấn nhẹ (glow/scale 1.05); thẻ `1:1` **mờ đi**. Chốt scene. |

> **Lưu ý chồng lấp:** B4 và B5 KHÔNG hiện cùng lúc đè nhau — B4 hiện ở nhánh trái xong, khi sang B5 nhánh phải vào (nhánh trái có thể giữ tĩnh, giảm opacity). Landmark teaser (B2) phải **mờ/tan đi** trước khi vào B3 để không rối.

## 4. SKELETON (bám khung `beat_to`)
```python
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manim import *
import numpy as np
from pathlib import Path
from _common import *   # palette, en_label, load_scene_timing, seg_end

class S01_ColdOpen(MovingCameraScene):
    SCENE_KEY = "scene_01"
    def construct(self):
        T = load_scene_timing(self.SCENE_KEY)
        self.add_sound(T["audio_path"])
        self.camera.background_color = BG_NAVY
        elapsed = 0.0
        def beat_to(t, *anims, **kw):
            nonlocal elapsed
            rt = max(0.2, t - elapsed)
            (self.play(*anims, run_time=rt, **kw) if anims else self.wait(rt))
            elapsed = t

        # B0 street + recognition  (kết thúc seg 0 = 4.78)
        # ... vẽ phố + 2 figure; tại ~3.5s thêm vòng nhận ra (có thể tách beat phụ) ...
        # B1 zoom + ghép face.png  (đến ~7.82)
        # B2 landmark teaser (mờ, thưa)  rồi tan trước B3
        # B3 two branches (đến 10.16)
        # B4 Verification 1:1 (đến 14.92)
        # B5 Identification 1:N + gallery (đến 20.54)
        # B6 1:N sáng lavender, 1:1 mờ (đến 24.70)

        if T["duration"] - elapsed > 0.05:
            self.wait(T["duration"] - elapsed)   # chốt = 25.22s
```

## 5. CHECKLIST S01
- [ ] B0 có cảnh phố + 2 người + khoảnh khắc "nhận ra" đúng lúc đọc "recognises".
- [ ] B1 zoom vào mặt + ghép `face.png` thật (cross-fade mượt, không pop).
- [ ] B2 teaser landmark **thưa/mờ**, tan trước B3 (không lưới dày).
- [ ] B4/B5 hai nhánh KHÔNG đè chồng; B6 `1:N` sáng lavender, `1:1` mờ.
- [ ] `add_sound` đúng; |render_dur − 25.22| ≤ 0.3s (đo ffprobe).
- [ ] English-only, 0 phụ đề, palette giữ nguyên.
- [ ] Không hiệu ứng vô nghĩa / không chồng lấp.

## 6. LÀM
Sửa lại file `release/scene_S01_*.py` theo storyboard trên (giữ nguyên file source gốc). `manim -pql`, đo ffprobe, báo `render_dur` + Δ rồi dừng chờ duyệt.
