# 🤖 PROMPT cho CODEX — THIẾT KẾ LẠI Scene 14 (S14 "Rotation, Phase, Speed")

> File: `release/scene_S14_phase_speed.py` (class `S14_PhaseSpeed`, `Scene` 2D).
> Mục tiêu: **đồ thị rõ & sang hơn**; **frame cuối (pipeline) bớt đơn điệu**; dùng **mặt thật + node khớp feature** cho phần phase; **chuẩn nội dung thuật toán**.
> **GIỮ:** `add_sound`, khung `beat_to`/`load_scene_timing`/`seg_end`, English/LaTeX, palette `_common.py`.
> **Audio = `scene_14`, duration = 44.44s** → render xong `ffprobe` cho `|Δ| ≤ 0.3s`.
> Env `vid`; kiểm tra `-pql`, bản cuối `-qh --disable_caching`.

---

## 1. VẤN ĐỀ HIỆN TẠI (phải sửa — xem ảnh user gửi)

1. **Đồ thị accuracy↔rotation chưa rõ/chưa sang:** `y_range=[60,100]` nhưng đường chỉ chạy 94→88 nên **dính sát đỉnh, gần như phẳng**, không thấy được "giảm nhẹ". Nhãn trục nhỏ (0.25), mặt pose vẽ tay thô đặt dưới trục, rời rạc.
2. **Mặt vẽ tay** cho pose & phase-test → nên dùng **mặt thật**; phần "node drift 5.2px vs 1.6px" cần đặt trên **mặt thật + node khớp feature** mới thuyết phục.
3. **Frame cuối đơn điệu:** pipeline `image → Extraction → Matching → db` chỉ là hộp + mũi tên + chữ `1000x faster`; thiếu nhấn mạnh "trích 1 lần, so khớp nhiều lần" và độ nhanh.

**Mục tiêu:** đồ thị zoom đúng vùng, có gridline/vùng tô, marker rõ + thumbnail pose thật; phase-test trên mặt thật; pipeline cuối giàu hình, làm bật "1000× faster".

---

## 2. Ý NGHĨA SCENE (giữ chuẩn — nội dung lõi)

- Ở **góc xoay nhỏ** (11°, 22°), nhờ graph linh hoạt, accuracy **giữ cao**: **94% → 88%**.
- **Phase có cần không?** Thí nghiệm:
  - **Bỏ phase** → localization **lệch > 5.2 px** → recognition tụt còn **67%**.
  - **Giữ phase** → lệch chỉ **1.6 px** → recognition lên **88%**.
  - → **Phase = mỏ neo** cứu cả hệ.
- Ngoài ra: **tách Extraction (1 lần) khỏi Matching (nhiều lần)** giúp EBGM **~1000× nhanh hơn** kiến trúc trước → đủ nhanh cho database lớn.

(Nội dung đúng — giữ; nâng đồ thị + pipeline.)

---

## 3. SỬA CỤ THỂ

### 3.1 Đồ thị accuracy↔rotation — rõ & sang
- **Zoom trục y vào vùng có nghĩa**, vd `y_range=[80,100,5]` (hoặc [84,100]) để đường 94→88 **dốc xuống thấy rõ**.
- Thêm **gridline mờ**, **vùng tô dưới đường** (gradient mint→cyan, opacity thấp), marker tròn tại 0°/11°/22°.
- Nhãn trục lớn hơn (≥0.3), `accuracy (%)` dọc bên trái, `rotation angle` dưới; nhãn `94%` / `88%` gắn sát marker, không đè đường.
- **Thumbnail pose thật** đặt **dưới trục x, canh đúng tick 0°/11°/22°** (ảnh mặt xoay dần) → liên kết trực quan điểm dữ liệu ↔ độ xoay.

### 3.2 Phase-test trên mặt thật (No phase vs With phase)
- Hai mặt thật cạnh nhau (`L(u,v)` + landmark như S08).
- **No phase (trái, coral):** node **trôi lệch khỏi feature** (đường nối ref→drift), nhãn lớn `5.2 px`, `recognition 67%`.
- **With phase (phải, mint):** node **bám sát feature** (drift cực nhỏ), `1.6 px`, `recognition 88%`.
- Kết: `phase = anchor` (giữa, dưới).

### 3.3 Pipeline cuối — giàu hình, bật tốc độ
- Bước rõ: **image (mặt thật)** → **Extraction (once)** xây graph → **Matching (many)** so với **DB nhiều mặt thật** → kết quả.
- Nhấn **"1 lần vs nhiều lần"**: extraction có badge `×1`, matching có badge `×N`.
- Bật **1000× faster**: một **thanh so sánh / gauge** (old vs EBGM) hoặc số `1000×` punch-in với hiệu ứng đếm nhanh; thêm `fast enough for large databases`.
- Mũi tên StealthTip, hộp đủ cao, nhãn không tràn/đè.

### 3.4 Đường nét "sang hơn"
- Bo góc & cỡ chữ nhất quán; gradient nhẹ; một tiêu điểm mỗi beat; clear cụm cũ trước khi vào cụm mới.

---

## 4. STORYBOARD — map đúng segment `transcript.json` (scene_14)

Mốc lấy bằng `seg_end(T, k)`:

| Beat | seg | Mốc≈(s) | Thoại | Hình |
|---|---|---|---|---|
| **B0–B1** | 0–1 | →10.02 | "at small rotation angles 11°, 22°... accuracy holds 94→88%." | Đồ thị zoom rõ + marker 11°/22° + thumbnail pose thật + `94%`/`88%`. |
| **B2** | 2 | →13.12 | "is the phase of the wave really necessary?" | `Is phase necessary?` nhấn; chuẩn bị tách đôi. |
| **B3–B4** | 3–4 | →23.06 | "drop phase... drifts > 5.2 px... down to 67." | No-phase (mặt thật): node trôi, `5.2 px`, `recognition 67%`. |
| **B5–B6** | 5–6 | →33.10 | "keep phase... 1.6 px... jumps to 88. Phase is the anchor." | With-phase: node bám, `1.6 px`, `88%`, `phase = anchor`. |
| **B7–B8** | 7–8 | →43.66 | "separating extraction from matching... ~1000× faster... large databases." | Pipeline giàu hình + `1000×` + `fast enough for large databases`. |

**Tail:** `self.wait(max(0, T["duration"] - elapsed - 0.18))` để khớp 44.44s.

---

## 5. ẢNH CẦN CUNG CẤP (user thả vào `assets/`)

- ✅ **`assets/s8_face.png`** + **`assets/s8_landmarks.json`** — phase-test + image trong pipeline (tái dùng cùng người/node).
- ✅ (khuyến nghị) **3 ảnh mặt cùng người xoay dần:** **`assets/s14_rot0.png`**, **`assets/s14_rot11.png`**, **`assets/s14_rot22.png`** (~256–512px, xoay ~0°/11°/22°) cho thumbnail dưới trục. *(Nếu không có → dùng `s8_face` xoay nhẹ bằng `ImageMobject.rotate` làm fallback gần đúng.)*
- ✅ (pipeline DB) vài mặt thật khác nhau cho database — **tái dùng `s12_gallery*`/`s9_sample*`/`s2_*`**.

Fallback: thiếu ảnh → `face.png`/silhouette. Helper `base = Path(__file__).resolve().parents[1] / "assets"`.

---

## 6. KIỂM TRA & NGHIỆM THU

```bash
python3 -m py_compile video-2-ebgm/release/scene_S14_phase_speed.py
rg -n "Text\(|font=|Paragraph|make_subtitle|[À-ỹ]" video-2-ebgm/release/scene_S14_phase_speed.py
ffprobe -v error -show_entries format=duration -of csv=p=0 media/.../S14_PhaseSpeed.mp4   # |Δ| ≤ 0.3s vs 44.44
```

Checklist:
- [ ] Đồ thị zoom đúng vùng (thấy rõ 94→88), gridline + vùng tô + marker + thumbnail pose thật canh tick.
- [ ] Phase-test trên **mặt thật**, node drift rõ (5.2px vs 1.6px).
- [ ] Pipeline cuối giàu hình, bật `1000×`; nhãn không tràn/đè.
- [ ] Mọi event đúng segment; tổng khớp 44.44s (|Δ|≤0.3s); English-only; palette; `-qh` OK.
