# 🤖 PROMPT cho CODEX — THIẾT KẾ LẠI Scene 4 (S04 "Three Pillars / The Idea")

> File: `release/scene_S04_idea.py` (class `S04_Idea`, `MovingCameraScene`).
> Thiết kế lại bố cục cho **sạch – không chồng lấp – đường nét uyển chuyển, sang hơn**.
> **GIỮ:** `add_sound`, khung `beat_to`/`load_scene_timing`/`seg_end`, English/LaTeX (`en_label`, `MathTex`/`Tex` + `EN_TEX_TEMPLATE`), palette `_common.py`.
> **Audio = `scene_04`, duration = 35.85s** → render xong `ffprobe` cho `|Δ| ≤ 0.3s`.
> Env `vid`; kiểm tra `-pql`, bản cuối `-qh --disable_caching`.

---

## 1. VẤN ĐỀ HIỆN TẠI (phải sửa — xem ảnh user gửi)

1. **Pillar 2 ("2. Wavelet Jet") chồng lấp nặng:** nhồi quá nhiều thứ trong panel hẹp (width 2.9): `input_patch` + `patch_lbl` + `color_badge` + `color_cross` + `color_lbl` + `psi` + `psi_note` + `jet` + `jet_note` + `arrow_to_jet`.
   - Nhãn **`texture DNA` đè lên heading `2. Wavelet Jet`**.
   - Sóng `ψ` (`make_wavelet_psi`, span ±1.26 quanh x=0.55) **tràn khỏi mép panel**, lấn sang khoảng giữa pillar 2–3.
   - Patch + badge + jet xếp lộn xộn, không có luồng đọc rõ.
2. **Chữ chú thích dưới 3 pillar đè lên khung:** các note đặt ở `frame.get_bottom() + DOWN*0.26` (`landmarks + edges`, `wavelet jet`, `pose samples stacked`) **nằm chồng lên viền panel / lẫn vào chip strengths**.
3. Đường nét chưa "sang": mũi tên thẳng cứng, sóng/stack stroke không đồng đều, nhiều phần tử cùng độ đậm cạnh tranh tiêu điểm.

**Mục tiêu:** mỗi pillar là một thẻ gọn, **mọi phần tử nằm trong panel** (heading trên cùng – icon ở giữa – caption hàng đáy, có khoảng cách); luồng đọc rõ; nét cong mềm (`thin_curved_arrow`), gradient nhẹ nhàng, tương phản tiêu điểm rõ.

---

## 2. Ý NGHĨA SCENE (giữ nguyên, làm rõ hơn)

EBGM dựng trên **3 trụ cột**, khác với "nhớ pixel thô" hay "nén tuyến tính kiểu PCA":
1. **Image Graph** — không coi mặt là mặt phẳng pixel, mà là **đồ thị nối các điểm landmark**.
2. **Wavelet Jet** — tại mỗi landmark, không lấy **màu**, mà trích **wavelet jet** = "**texture DNA**" của mảng da đó.
3. **Face Bunch Graph** — để chịu mọi **pose**, **chồng nhiều graph mẫu** thành một bunch graph.

Kết quả: **robust ánh sáng · học từ <100 ảnh · độ chính xác cao**.

---

## 3. BỐ CỤC MỚI (số đo cụ thể — chống chồng lấp triệt để)

### 3.1 Khung lưới 3 pillar (cân đối, có gap)
- 3 panel **rộng hơn**: `width≈3.55, height≈4.5, corner_radius 0.16`, tâm tại `x = -4.6, 0, +4.6`, `y = -0.15`.
  - → mỗi panel span ngang ~3.55, gap giữa các panel ~1.05, chừa lề mép khung. **Sóng/jet/graph phải nằm trong `width*0.84`** (≈ ±1.49 quanh tâm panel) — không phần tử nào vượt mép.
- **Mỗi pillar có 3 hàng cố định** (đặt theo tâm panel `cx, cy`):
  - **Heading row** (trên cùng trong panel): `y = cy + height/2 - 0.42`. Đánh số + tên: `1. Image Graph` / `2. Wavelet Jet` / `3. Face Bunch Graph`. **Cùng `scale`** (vd 0.30) cho cả 3 — nếu tên dài quá thì xuống 2 dòng hoặc rút gọn (`3. Bunch Graph`), **không thu nhỏ lệch** như hiện tại (0.23 vs 0.29).
  - **Icon zone** (giữa): `y ≈ cy + 0.15`, cao tối đa ~2.4, rộng ≤ `width*0.84`. Đây là vùng vẽ chính.
  - **Caption row** (đáy **trong** panel): `y = cy - height/2 + 0.40`. Caption ngắn, 1 dòng, `scale 0.24`, **không bao giờ đặt bằng `frame.get_bottom()+DOWN`** (đó là lỗi cũ khiến đè viền). Nếu cần 2 ý → ghép `caption · sub-note` trên cùng một dòng hoặc 2 dòng sát nhau vẫn trong panel.

### 3.2 Pillar 1 — Image Graph (giữ ý, dọn nét)
- `face.png` set_height vừa vùng icon, **landmark dots + edges** màu `ACCENT_CYAN` (đồng bộ màu pillar 1), stroke đều ~2.0, dots `radius 0.045`.
- Caption đáy trong panel: `landmarks + edges`.

### 3.3 Pillar 2 — Wavelet Jet (VIẾT LẠI HẲN — đây là chỗ lỗi nặng)
Bỏ kiểu nhồi ngang. Dùng **luồng dọc 1 chiều, gọn**, tất cả trong panel:
1. **Trên (trong icon zone):** một **image patch nhỏ** (`face_frame` ~0.9×0.9, crop má/da) đặt lệch trái-trên; cạnh nó một **swatch màu nhỏ + `thin` Cross coral** = ý "**not color**" (gọn, 1 cụm).
2. **`thin_curved_arrow`** mềm từ patch **đi xuống** tới jet (không mũi tên thẳng cứng; nét cong).
3. **Hero = jet stack** (stack-of-discs giống S06, hoặc `make_jet_stack` đã có nhưng canh giữa, fit `width*0.8`), tông `ACCENT_TEAL`, gradient mượt, glow nhẹ. Ký hiệu `$\psi$` nhỏ gắn cạnh jet (không phải sóng to tràn panel).
   - *(Tuỳ chọn)* sóng `ψ` chỉ làm **inset rất nhỏ** trong patch, **không** vẽ sóng span ±1.26 tràn ra ngoài như hiện tại.
4. **Caption đáy trong panel:** `wavelet jet — texture DNA` (một dòng). **Bỏ** `texture DNA` đặt ngang heading.
> Nguyên tắc: pillar 2 chỉ còn **≤ 4 cụm thị giác** (patch+not-color / arrow / jet / caption). Không cụm nào chạm cụm khác hay mép panel.

### 3.4 Pillar 3 — Face Bunch Graph (chống chồng + pose rõ)
- **3 face-graph chồng lớp theo chiều sâu** (offset nhỏ, mờ dần ra sau), màu cyan→teal→lavender. Offset vừa phải để **không che nhãn pose**.
- **Pose labels** đặt **gọn cạnh từng lớp, không tràn**: `frontal / half-profile / profile`. Nếu dùng 3 ảnh pose thật (mục 5) thì mỗi lớp là một pose khác nhau → trực quan hơn nhiều.
- Caption đáy trong panel: `pose samples stacked`.

### 3.5 Đường nét "sang hơn" (toàn scene)
- Mũi tên: **`thin_curved_arrow`/`thin_arrow` (StealthTip)** nét cong mềm, stroke 2.0–2.2, đầu mũi cách phần tử kế tiếp một khoảng rõ.
- Gradient nhẹ trên jet/graph/bunch (set_color_by_gradient hoặc fill_opacity tăng dần), tránh mọi phần tử cùng độ đậm.
- **Một tiêu điểm mỗi beat:** khi build pillar mới, **dim pillar cũ về ~0.3** (đã làm) nhưng đảm bảo dim cả caption/nhãn của nó. Cuối scene mới sáng đều cả 3.
- Chip strengths cuối đặt **dưới cùng**, có gap với panel (vd `y = -3.15`), không đụng caption đáy panel.

---

## 4. STORYBOARD — map đúng segment `transcript.json` (scene_04)

Mốc lấy bằng `seg_end(T, k)` (đừng hardcode):

| Beat | seg | Mốc≈(s) | Thoại | Hình |
|---|---|---|---|---|
| **B0** | 0 | →6.58 | "EBGM is built on three pillars, unlike memorizing pixels or compressing them linearly as PCA does." | Title `Three Pillars` + intro `not pixels, not PCA`. Mặt thật `face.png` ở giữa, **2 thumbnail bị loại** hai bên: `raw pixels` (pixel-mosaic + slim Cross) và `linear PCA` (blur + slim Cross). Cả hai **fade đi** khi pillar bắt đầu. |
| **B1** | 1 | →12.84 | "1. Don't see the face as a plane of pixels, but as a graph connecting landmark points." | Dựng **Pillar 1 — Image Graph**: face + landmark dots mọc dần (`LaggedStart`) + edges vẽ mượt. Caption `landmarks + edges`. |
| **B2** | 2 | →21.52 | "2. At each landmark, don't take color, but extract a wavelet jet, the textured DNA of that patch of skin." | Dim pillar 1. Dựng **Pillar 2 — Wavelet Jet** theo luồng dọc mới: patch + `not color` (swatch+slim cross) → `thin_curved_arrow` → jet stack (hero) + `$\psi$`. Caption `wavelet jet — texture DNA`. **Không chồng lấp.** |
| **B3** | 3 | →27.16 | "3. To handle every pose, stack many sample graphs into a face-bunch graph." | Dim pillar 2. Dựng **Pillar 3 — Face Bunch Graph**: 3 face-graph chồng lớp theo chiều sâu + pose labels `frontal/half-profile/profile`. Caption `pose samples stacked`. |
| **B4** | 4 | →35.32 | "The result? Highly robust to lighting, learns from fewer than 100 sample images, achieves astonishing accuracy." | Sáng đều cả 3 pillar; `SurroundingRectangle` bao cụm. 3 chip ở hàng đáy (có gap): `Robust to light` · `< 100 images` · `High accuracy` (xuất hiện `LaggedStart`). |

**Tail:** `self.wait(max(0, T["duration"] - elapsed - 0.18))` để khớp 35.85s.

---

## 5. ẢNH CẦN CUNG CẤP (user thả vào `assets/`)

Đã có & dùng được: `assets/face.png` (pillar 1, patch pillar 2, fallback pillar 3).

**Khuyến nghị để pillar 3 trực quan hơn** (hiện đang lặp 1 mặt 3 lần → kém thuyết phục):
- ✅ (khuyến nghị) **3 ảnh cùng một người, 3 pose:** `assets/s4_pose_frontal.png`, `assets/s4_pose_half.png`, `assets/s4_pose_profile.png` (vuông ~512px, nền tối/đồng nhất). Để bunch graph thật sự là "nhiều pose chồng lại".
- ✅ (tuỳ chọn) **`assets/s4_skin_patch.png`** — crop một mảng **da/má có texture** (~256px) cho "image patch" của pillar 2, nhấn ý "texture DNA, not color".

Nếu thiếu bất kỳ ảnh nào → **fallback**: dùng `face.png`/`load_face(...)` đã có, vẫn render được (giữ helper kiểm tra tồn tại `base = Path(__file__).resolve().parents[1] / "assets"`).

---

## 6. KIỂM TRA & NGHIỆM THU

```bash
python3 -m py_compile video-2-ebgm/release/scene_S04_idea.py
rg -n "Text\(|font=|Paragraph|make_subtitle|[À-ỹ]" video-2-ebgm/release/scene_S04_idea.py   # phải rỗng
ffprobe -v error -show_entries format=duration -of csv=p=0 media/.../S04_Idea.mp4           # |Δ| ≤ 0.3s vs 35.85
```

Checklist:
- [ ] Pillar 2 **không còn chồng lấp**; `texture DNA` không đè heading; sóng/jet nằm trong mép panel.
- [ ] 3 caption nằm **trong panel** (hàng đáy có gap), không đè viền/chip.
- [ ] Heading 3 pillar cùng cỡ chữ, cân đối; chip strengths có gap với panel.
- [ ] Mũi tên cong mềm (StealthTip), gradient nhẹ, mỗi beat một tiêu điểm (pillar cũ dim cả nhãn).
- [ ] Mọi event rơi đúng segment; tổng khớp 35.85s (|Δ|≤0.3s); English-only; palette `_common.py`; render `-qh` OK.
