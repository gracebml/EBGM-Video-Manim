# 🤖 PROMPT cho CODEX — Fix overlap S06/S07 + mũi tên đầu mảnh (toàn bộ scene)

> 3 việc: (A) fix overlap S06 (amplitude/phase), (B) fix mũi tên đè chữ "match?" S07, (C) đổi **mọi đầu mũi tên tam giác thô** thành **đầu mảnh** trên TẤT CẢ scene. Sau khi sửa file nào, render lại `-qh` file đó (|Δ|≤0.3s so audio). English/LaTeX/palette giữ nguyên.

---

## (C) MŨI TÊN ĐẦU MẢNH — GLOBAL (làm trước, dùng chung)
Đầu mũi tên mặc định của Manim là tam giác đặc, nhìn **thô kệch**. Đổi sang **đầu mảnh** (`StealthTip`) cho toàn bộ.

1. Thêm helper vào CUỐI `_common.py`:
```python
from manim import StealthTip

def thin_arrow(start, end, color=TEXT_PRIMARY, stroke_width=2.2, buff=0.08,
               tip_ratio=0.16, **kw):
    """Mũi tên đầu mảnh (StealthTip), nét gọn — dùng thay Arrow mặc định."""
    a = Arrow(start, end, color=color, stroke_width=stroke_width, buff=buff,
              tip_shape=StealthTip, max_tip_length_to_length_ratio=tip_ratio,
              **kw)
    return a

def thin_curved_arrow(start, end, color=TEXT_PRIMARY, stroke_width=2.2, **kw):
    a = CurvedArrow(start, end, color=color, stroke_width=stroke_width,
                    tip_shape=StealthTip, **kw)
    a.tip.scale(0.7)
    return a
```
2. Trong **mọi** `release/scene_S*.py`: thay
   - `Arrow(...)` → `thin_arrow(...)` (giữ nguyên tham số start/end/color/stroke_width).
   - `Vector(...)` → dùng `thin_arrow(ORIGIN, vec, ...)` hoặc thêm `tip_shape=StealthTip, max_tip_length_to_length_ratio=0.16`.
   - `CurvedArrow(...)` → thêm `tip_shape=StealthTip` rồi `.tip.scale(0.7)` (hoặc `thin_curved_arrow`).
   - `GrowArrow(arrow)` giữ nguyên (chỉ cần `arrow` đã là thin_arrow).
   - **`Arrow3D(...)`** (vd S07 `disp`, các scene 3D): làm đầu nhọn nhỏ lại — `Arrow3D(..., thickness=0.02, height=0.16, base_radius=0.045)` (giảm cone), hoặc thay bằng `Line3D` mảnh + 1 cone nhỏ.
3. Đầu mũi tên nên nhỏ, thanh; nét (`stroke_width`) ~2–2.4. Không để đầu mũi tên to hơn ~16% chiều dài.

> Các scene có mũi tên cần đổi: S01, S02, S03, S04, S05, S06, S07, S09, S10, S11, S13, S14 (theo grep). Sửa hết.

---

## (A) FIX OVERLAP S06 — `release/scene_S06_jet.py` (beat B7/B8 amplitude·phase)
**Vấn đề:** trong 2 thẻ nhỏ (`amp_card`/`phase_card`, height chỉ 1.15), **chữ `Amplitude`/`Phase` đè lên vòng tròn trang trí bên trong**, và note `what shape?`/`which coordinate?` quá sát. (dòng ~201–248)

**Sửa:**
- Tăng chiều cao thẻ (vd height ~1.6) HOẶC bỏ hẳn vòng tròn trang trí bên trong thẻ.
- Sắp xếp **dọc, có khoảng cách rõ**: tiêu đề (`Amplitude`/`Phase`) ở **đỉnh thẻ**; nếu giữ icon (vòng tròn/chấm) thì đặt **giữa thẻ, dưới tiêu đề, không chạm chữ**; note (`what shape?`/`which coordinate?`) đặt **dưới đáy thẻ, cách ra ngoài**, không đè viền.
- Mũi tên từ công thức `z_j=a_j e^{iφ_j}` xuống 2 thẻ: dùng `thin_arrow`, kết thúc **phía trên mép thẻ** (buff đủ), không cắm vào chữ.
- Kết quả: trong mỗi thẻ, chữ và icon **tách bạch**, đọc rõ; note nằm ngoài/đáy thẻ.

---

## (B) FIX MŨI TÊN ĐÈ CHỮ "match?" S07 — `release/scene_S07_similarity.py` (dòng ~81–85)
**Vấn đề:** `arrow_l`/`arrow_r` kết thúc ở `±0.32` quá gần tâm nên **đầu mũi tên cắm vào chữ `match?`**.

**Sửa:**
- Để chừa khoảng trống quanh chữ: cho 2 mũi tên kết thúc xa tâm hơn (vd từ `±1.25` → `±0.78`, để hở ~0.45 mỗi bên quanh `match?`), hoặc tăng `buff`.
- Dùng `thin_arrow`. Đảm bảo **không phần nào của mũi tên chạm bounding box của `match?`** (có thể canh theo `q.get_left()/get_right()` + margin).

---

## RÀNG BUỘC
- Chỉ đổi mũi tên + fix overlap; KHÔNG đổi nội dung/nhịp/timing scene. Tổng mỗi scene vẫn = audio (|Δ|≤0.3s).
- English-only, `en_label`/LaTeX, palette `_common.py`.
- `py_compile` sạch; render `-qh` các scene đã sửa.

## LÀM
1. Thêm helper vào `_common.py`. 2. Sửa S06 (A) + S07 (B). 3. Đổi mũi tên tất cả scene còn lại (C). 4. Render `-qh` từng scene đã đổi, đo ffprobe, báo Δ rồi dừng chờ duyệt.
