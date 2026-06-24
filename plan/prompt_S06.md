# 🤖 PROMPT cho CODEX — CHỈNH/THIẾT KẾ LẠI Scene 6 (S06 "The Jet")

> File: `release/scene_S06_jet.py` (class `S06_Jet`, `ThreeDScene` góc phẳng `phi=0, theta=-90`).
> Mục tiêu: **đổi mặt vẽ tay → mặt người thật**, **sửa overlap nhãn/khung**, design **sang hơn** nhưng **chuẩn nội dung thuật toán**.
> **GIỮ:** `add_sound`, khung `beat_to`/`load_scene_timing`/`seg_end`, English/LaTeX (`en_label`, `MathTex`/`Tex` + `EN_TEX_TEMPLATE`), palette `_common.py`.
> **Audio = `scene_06`, duration = 28.56s** → render xong `ffprobe` cho `|Δ| ≤ 0.3s`.
> Env `vid`; kiểm tra `-pql`, bản cuối `-qh --disable_caching`.

---

## 1. VẤN ĐỀ HIỆN TẠI (phải sửa — xem ảnh user gửi)

1. **Overlap nhãn ↔ khung:** `bank_lbl` = `whole bank of Gabor wavelets` đặt ở `UP*1.95`, nhưng `wavelet_bank()` scale 1.25 nên **cạnh trên của `SurroundingRectangle` đè ngay lên dòng chữ**. Trông dính, không sạch.
2. **Khuôn mặt vẽ tay 2D** (`face_eye`: ellipse + 2 circle mắt + line mũi + arc miệng) ở B2 ("one eye corner") **thô và lạc tông** so với phần còn lại. → **Thay bằng mặt người thật** trong `assets/` (hoặc user cung cấp ảnh phù hợp hơn — xem mục 5).
3. Đường nét chưa thật "sang": mũi tên hội tụ mảnh nhưng rối, bố cục các beat chưa chừa khoảng thở.

**Mục tiêu:** mỗi beat một tiêu điểm, **mọi nhãn cách khung một khoảng rõ**, mặt người thật + zoom vào **đuôi mắt (eye corner)** đúng tinh thần "lấy jet tại một điểm".

---

## 2. Ý NGHĨA SCENE (giữ chuẩn — đây là nội dung lõi)

Đặt **cả bank 40 Gabor wavelets** (5 tần số × 8 hướng) tại **một điểm** (vd đuôi mắt) → thu được **40 số phức**. Bó 40 số đó gọi là **Jet**.
- Mỗi phần tử: **`z_j = a_j · e^{i φ_j}`**.
- Jet = "**mã vạch (barcode) độc nhất**" của điểm đó.
- Vì là số phức → mỗi phần tử mang **2 vũ khí**:
  - **Amplitude `a_j`** → *biến thiên chậm*, cho biết **hình dạng/kết cấu** vùng đó (`what shape?`).
  - **Phase `φ_j`** → *biến thiên nhanh*, định vị **toạ độ chính xác** của đặc trưng (`which coordinate?`).
- Kết: **Amplitude → shape · Phase → coordinate**.

(Nội dung hiện đã đúng — giữ nguyên, chỉ nâng chất lượng hình.)

---

## 3. SỬA CỤ THỂ

### 3.1 Chống overlap nhãn ↔ khung bank (B0–B1)
Đặt **ngân sách dọc** rõ ràng (frame ±4):
- `title` (`Jet = 40 complex responses at one point`): `y ≈ 3.25`.
- `bank_lbl` (`whole bank of Gabor wavelets`): `y ≈ 2.6`.
- **Khung bank:** scale lại sao cho **cạnh trên `SurroundingRectangle` ≤ y≈2.15** (gap ≥ 0.35 dưới `bank_lbl`). Tức giảm scale bank (vd 1.05–1.15 thay vì 1.25) hoặc dịch bank xuống; `buff` của box ~0.2.
- `mult` (`5 frequencies x 8 orientations = 40`): `y ≈ -2.75`, có gap dưới cạnh dưới box.
- **Bỏ `row_braces`** mờ chạy ngang nếu chúng cắt qua khung (gây rối) — hoặc giữ nhưng để **bên trong** box, opacity rất thấp.

### 3.2 Đổi mặt vẽ tay → MẶT NGƯỜI THẬT (B2 — quan trọng)
- Bỏ helper `face_eye()` (mặt 2D thô). Dùng **`ImageMobject`** mặt thật từ `assets/` (mục 5), đặt khung bo góc nhất quán (`RoundedRectangle` viền `ACCENT_BLUE` mảnh, ảnh `set_height` vừa khung, đặt trong VGroup/Group).
- **Zoom vào đuôi mắt:** chọn 1 điểm = **eye corner** trên ảnh (toạ độ tương đối khung). Vẽ:
  - một **vòng tròn focus mint** (`ACCENT_MINT`, stroke ~2.5) + dot mint tại eye corner,
  - một **inset phóng to** (magnifier): một `RoundedRectangle` nhỏ nối tới eye corner bằng `thin` connector, bên trong là **patch crop quanh eye corner** (copy ảnh, scale lớn, mask trong khung) — để thấy rõ "một điểm cụ thể".
- **Wavelets hội tụ về eye corner:** vài (không phải tất cả) wavelet thu nhỏ bay/`thin_arrow` hội tụ về đúng điểm focus, nét mảnh đều, đầu mũi dừng cách điểm một chút. Nhãn `one eye corner` (mint) đặt dưới mặt, không đè ảnh.
- Lưu ý `ThreeDScene` góc `phi=0`: `ImageMobject` hướng thẳng camera nên render bình thường; nếu cần dùng `Group` (không `VGroup`) khi trộn `ImageMobject` với mobject vector.

### 3.3 Đường nét "sang hơn" (toàn scene)
- Mũi tên: `thin_arrow`/`thin_curved_arrow` (StealthTip), stroke đều ~1.8–2.2, đầu mũi cách phần tử kế tiếp một khoảng rõ. Hội tụ wavelet: dùng **ít mũi tên hơn** (vd 6–8 cái tiêu biểu) để không rối.
- Jet stack (B4): giữ stack-of-discs nhưng **gradient mượt**, glow nhẹ, `JET` label đặt dưới có gap; `SurroundingRectangle` buff đủ.
- Cards số phức (B3) `z_0..z_7 ... x40`: canh lưới đều, không tràn; công thức `z_j=a_j e^{iφ_j}` đặt trên cụm card, có gap.
- B6 hai card **Amplitude / Phase**: theo CLAUDE.md — **đủ chiều cao**, xếp heading (trên) → icon (giữa) → note (đáy, trong card) có spacing, **không đè vòng tròn/inner icon**; mũi tên `element → card` **dừng trên mép card** (buff đủ), không chạm chữ.
- Một tiêu điểm mỗi beat: fade/dim cụm cũ trước khi đưa cụm mới.

---

## 4. STORYBOARD — map đúng segment `transcript.json` (scene_06)

Mốc lấy bằng `seg_end(T, k)` (đừng hardcode):

| Beat | seg | Mốc≈(s) | Thoại | Hình |
|---|---|---|---|---|
| **B0** | 0 | →2.62 | "throw the whole bank of 40 Gabor wavelets" | Title + `whole bank of Gabor wavelets` (gap rõ). Bank 5×8 wavelet hiện dần (`LaggedStart`), khung box **không đè nhãn**. |
| **B1** | 1 | →5.56 | "five frequencies times eight orientations" | Nhấn cấu trúc `5 frequencies x 8 orientations = 40` (đáy). Có thể highlight 1 hàng (freq) + 1 cột (orientation) để thấy 5×8. |
| **B2** | 2 | →8.12 | "at a single point like the corner of an eye" | **Mặt người thật** vào (trái); zoom/magnifier vào **eye corner** (focus mint); vài wavelet hội tụ về điểm đó. `mult` thu nhỏ lên góc. Nhãn `one eye corner`. |
| **B3** | 3 | →10.12 | "and you get 40 complex numbers" | Hội tụ → **40 số phức**: lưới card `z_0..z_7 … x40` + công thức `z_j=a_j e^{iφ_j}`. |
| **B4** | 4 | →12.20 | "That bundle is called a jet." | Bó lại thành **JET**: jet stack-of-discs + `SurroundingRectangle` + label `JET`. |
| **B5** | 5 | →15.80 | "Think of a jet as a unique barcode of that eye corner." | Morph jet → **barcode**; nhãn `unique barcode of that eye corner`. |
| **B6** | 6 | →19.86 | "since they're complex, each element carries two weapons" | `two weapons`; `z_j=a_j e^{iφ_j}` tách 2 nhánh → card **Amplitude** (mint) & **Phase** (lavender), mũi tên dừng trên mép card. |
| **B7** | 7 | →23.46 | "Amplitude, telling us what shape the region has" | Sáng card Amplitude (icon "shape"), dim Phase; note `what shape?` (đáy card). |
| **B8** | 8 | →27.64 | "phase, telling us exactly which coordinate the feature sits at" | Sáng card Phase (crosshair toạ độ), note `which coordinate?`; kết `Amplitude -> shape | Phase -> coordinate`. |

**Tail:** `self.wait(max(0, T["duration"] - elapsed - 0.18))` để khớp 28.56s.

---

## 5. ẢNH CẦN CUNG CẤP (user thả vào `assets/`)

Có sẵn: `assets/face.png` — dùng được **nhưng** nếu muốn zoom đuôi mắt nét đẹp thì nên có ảnh chất hơn:

- ✅ (khuyến nghị) **`assets/s6_face.png`** — **mặt người thật, chính diện, biểu cảm trung tính, ánh sáng đều, độ phân giải cao, hai mắt rõ** (vuông ~768–1024px, nền tối/đồng nhất hợp tông navy). Để zoom vào **đuôi mắt (eye corner)** đọc rõ.
- ✅ (tuỳ chọn) **`assets/s6_eye_corner.png`** — crop sẵn vùng **đuôi mắt** (~256px) cho inset magnifier sắc nét (nếu không có → tự crop từ `s6_face.png`/`face.png` lúc runtime).

**Mô tả ảnh mong muốn (để user chuẩn bị):** một gương mặt người thật rõ ràng, nhìn thẳng, da/đuôi mắt có chi tiết texture (để hợp ý "jet = barcode của một điểm"); tránh ảnh quá tối, quá nghiêng, hay bị che mắt.

Fallback: nếu thiếu ảnh → dùng `face.png` đã có; **không** quay lại mặt vẽ tay 2D. Giữ helper kiểm tra tồn tại `base = Path(__file__).resolve().parents[1] / "assets"`.

---

## 6. KIỂM TRA & NGHIỆM THU

```bash
python3 -m py_compile video-2-ebgm/release/scene_S06_jet.py
rg -n "Text\(|font=|Paragraph|make_subtitle|[À-ỹ]" video-2-ebgm/release/scene_S06_jet.py   # phải rỗng
ffprobe -v error -show_entries format=duration -of csv=p=0 media/.../S06_Jet.mp4            # |Δ| ≤ 0.3s vs 28.56
```

Checklist:
- [ ] `whole bank of Gabor wavelets` **không còn đè khung box** (gap ≥ 0.35); `mult` có gap dưới box.
- [ ] B2 dùng **mặt người thật** (`ImageMobject`), zoom rõ vào **eye corner**; bỏ hẳn mặt vẽ tay.
- [ ] Wavelet hội tụ gọn (ít mũi tên), StealthTip, đầu mũi cách điểm focus.
- [ ] Card Amplitude/Phase đủ cao, heading→icon→note không chồng, mũi tên dừng trên mép card.
- [ ] Mọi event rơi đúng segment; tổng khớp 28.56s (|Δ|≤0.3s); English-only; palette `_common.py`; render `-qh` OK.
