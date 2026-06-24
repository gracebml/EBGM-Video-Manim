# 🤖 PROMPT cho CODEX — THIẾT KẾ LẠI Scene 12 (S12 "Recognition")

> File: `release/scene_S12_recognition.py` (class `S12_Recognition`, `Scene` 2D).
> Mục tiêu: **sửa overlap frame gần cuối (gallery ↔ rank panel)**; **dùng mặt người thật cho probe & gallery**; design **sang hơn**, **chuẩn nội dung thuật toán**.
> **GIỮ:** `add_sound`, khung `beat_to`/`load_scene_timing`/`seg_end`, English/LaTeX, palette `_common.py`.
> **Audio = `scene_12`, duration = 22.38s** → render xong `ffprobe` cho `|Δ| ≤ 0.3s`.
> Env `vid`; kiểm tra `-pql`, bản cuối `-qh --disable_caching`.

---

## 1. VẤN ĐỀ HIỆN TẠI (phải sửa — xem ảnh user gửi)

1. **Overlap cuối scene:** `gallery_frame` (tâm x=2.05, rộng 5.55 → mép phải ≈ **4.82**) **đè lên** `rank_panel` (tâm x=5.02, rộng 2.7 → mép trái ≈ **3.67**). Cột phải gallery (M3/M6 ở x=3.6) và **vòng winner** (bán kính 0.72 quanh M3) **nằm dưới panel RANK** → đúng chỗ chồng trong ảnh.
2. **Công thức `S_G` (UP*2.45) gần chạm `GALLERY` (UP*2.18)** → chật phía trên.
3. **Mặt vẽ tay** (`graph_at` chỉ là graph trừu tượng, không có khuôn mặt) → probe & gallery nên là **mặt người thật** để "so khớp danh tính" trực quan.

**Mục tiêu:** 3 vùng **probe | gallery | rank** **tách bạch, có gap**; winner highlight nằm gọn trong gallery; mặt thật cho probe + gallery; mạch score→rank→winner rõ.

---

## 2. Ý NGHĨA SCENE (giữ chuẩn — nội dung lõi)

- Khi elastic grid đã **khoá** lên mặt mới (**probe**) → nhận dạng **rất nhẹ**.
- Mang grid đó **so với từng người trong gallery**.
- **Bỏ phase, chỉ dùng amplitude** (`S_a`) vì amplitude **robust hơn** với biểu cảm/nụ cười.
  - `S_G = (1/N) Σ_i S_a(J_i^{probe}, J_i^{gallery})`.
- **Score → rank → ai đứng rank-1 chính là danh tính** cần tìm (winner).

(Nội dung đúng — giữ; nâng hình + dọn overlap.)

---

## 3. SỬA CỤ THỂ

### 3.1 Bố cục 3 vùng không chồng (số đo cụ thể)
Chia ngang rõ ràng (frame ±7.1):
- **PROBE (trái):** thẻ mặt thật ở **x ≈ −5.2**, rộng ~2.3.
- **GALLERY (giữa):** khung ở **tâm x ≈ 0.4, rộng ≤ 5.0** → mép phải ≤ **2.9**. Lưới 2×3 card mặt thật, gọn trong khung.
- **RANK (phải):** panel ở **tâm x ≈ 5.3, rộng ~2.6** → mép trái ≥ **4.0**. **Gap ≥ 1.0** với gallery.
- **Winner ring** quanh card thắng (M3) **nằm trong gallery**, không chạm panel RANK.
- Beam probe→gallery: ít đường, gọn, đầu cách card.

### 3.2 Công thức & nhãn phía trên
- `S_G = (1/N) Σ S_a(...)` đặt **UP*2.85** (gap với title), scale vừa.
- `GALLERY` label đặt **bên trong** mép trên khung gallery (không trôi lên đụng công thức).

### 3.3 Mặt người thật cho probe + gallery
- **Probe** = mặt thật (vd `s8_face`) + elastic grid khoá (graph khớp feature, dùng `L(u,v)`/landmark như S08).
- **Gallery 6 card** = 6 mặt thật khác nhau; **một trong số đó cùng danh tính probe → là winner (M3, score cao nhất)**. Mỗi card: ảnh + tên `M1..M6` (trên) + score (dưới), không đè.
- `drop phase / amplitude only`: hai chip nhỏ gọn dưới công thức, không tràn.

### 3.4 Đường nét "sang hơn"
- Card đồng cỡ, khung bo góc nhất quán; score tag canh dưới card có gap.
- Rank rows: `1. M3  0.92` (winner mint), `2. M5 0.73`, `3. M1 0.64` — đều, trong panel; `[WINNER]` dưới panel có gap.
- Một tiêu điểm mỗi beat.

---

## 4. STORYBOARD — map đúng segment `transcript.json` (scene_12)

Mốc lấy bằng `seg_end(T, k)`:

| Beat | seg | Mốc≈(s) | Thoại | Hình |
|---|---|---|---|---|
| **B0** | 0 | →3.56 | "Once the elastic grid is locked onto the new face, the probe," | PROBE: mặt thật + grid khoá; nhãn `elastic grid locked` + khoá. |
| **B1** | 1 | →5.46 | "recognition is featherlight." | Icon lông vũ `featherlight` (nhẹ). |
| **B2** | 2 | →9.34 | "compare it against each person in the gallery." | GALLERY 2×3 mặt thật + beam probe→gallery. |
| **B3** | 3 | →12.82 | "Now we drop phase and use amplitude only" | Công thức `S_G` + chip `drop phase` / `amplitude only`. |
| **B4** | 4 | →16.66 | "because amplitude is more robust to changes in expression and smiles." | Nhấn `robust to smiles`; sáng chip amplitude. |
| **B5** | 5 | →21.96 | "Score, rank, and whoever lands at rank 1 is the identity." | Score tags → panel RANK (1/2/3) → **winner ring** quanh M3 (trong gallery) + `[WINNER]`. |

**Tail:** `self.wait(max(0, T["duration"] - elapsed - 0.18))` để khớp 22.38s.

---

## 5. ẢNH CẦN CUNG CẤP (user thả vào `assets/`)

- ✅ **`assets/s8_face.png`** + **`assets/s8_landmarks.json`** — probe (tái dùng cùng người/node với S08–S11).
- ✅ **Gallery 6 mặt thật khác nhau:** **`assets/s12_gallery1.png` … `s12_gallery6.png`** (chính diện, ~512px). **Một card phải là cùng người với probe** (winner). *(Có thể tái dùng: probe `s8_face` cho card winner + `s9_sample1..5`/bộ `s2_*` cho 5 card còn lại.)*

**Mô tả:** ảnh gallery chính diện, rõ, đa dạng người; card winner nên là **cùng danh tính với probe** (có thể khác biểu cảm/ánh sáng để minh hoạ "amplitude robust to smiles").

Fallback: thiếu ảnh → tái dùng `s2_*`/`face.png`; thiếu winner cùng danh tính → vẫn highlight M3. Helper `base = Path(__file__).resolve().parents[1] / "assets"`.

---

## 6. KIỂM TRA & NGHIỆM THU

```bash
python3 -m py_compile video-2-ebgm/release/scene_S12_recognition.py
rg -n "Text\(|font=|Paragraph|make_subtitle|[À-ỹ]" video-2-ebgm/release/scene_S12_recognition.py
ffprobe -v error -show_entries format=duration -of csv=p=0 media/.../S12_Recognition.mp4   # |Δ| ≤ 0.3s vs 22.38
```

Checklist:
- [ ] **Gallery & RANK không chồng** (gap ≥ 1.0); winner ring nằm trong gallery.
- [ ] Công thức `S_G` không đụng `GALLERY`.
- [ ] Probe + gallery dùng **mặt thật**; winner = cùng danh tính probe.
- [ ] Score → rank → winner đọc rõ; nhãn không tràn.
- [ ] Mọi event đúng segment; tổng khớp 22.38s (|Δ|≤0.3s); English-only; palette; `-qh` OK.
