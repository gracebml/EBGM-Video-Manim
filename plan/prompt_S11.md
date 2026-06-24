# 🤖 PROMPT cho CODEX — THIẾT KẾ LẠI Scene 11 (S11 "Elastic Matching")

> File: `release/scene_S11_elastic.py` (class `S11_Elastic`, `ThreeDScene` góc phẳng `phi=0, theta=-90`).
> Mục tiêu: **đổi mặt vẽ tay → mặt người thật + node khớp feature**; **dọn frame cuối (B7–B9) lộn xộn**; design **sang hơn**, **chuẩn nội dung thuật toán**.
> **GIỮ:** `add_sound`, khung `beat_to`/`load_scene_timing`/`seg_end`, English/LaTeX, palette `_common.py`.
> **Audio = `scene_11`, duration = 46.39s** → render xong `ffprobe` cho `|Δ| ≤ 0.3s`.
> Env `vid`; kiểm tra `-pql`, bản cuối `-qh --disable_caching`.

---

## 1. VẤN ĐỀ HIỆN TẠI (phải sửa)

1. **Mặt vẽ tay 2D** (`face`) + `base` cố định → node không khớp feature thật. Elastic matching ("node bò về đúng landmark") **chỉ có nghĩa khi đặt trên mặt thật**.
2. **Frame cuối (B7–B9) lộn xộn:**
   - B7 thêm `phase_title` (`Two Phases`, UP*2.75) nhưng **không FadeOut `title` "Elastic Matching"** (UP*3.0) → **hai tiêu đề chồng**.
   - B8 `raw_frame` (mép trên y≈0.65) **đè lên `timeline`** (y=0.55) của Two Phases; cụm normalization + recognition + timeline + dots chen nhau.
   - Luồng "2 phases → normalization → recognition → final graph" không đọc ra mạch.

**Mục tiêu:** elastic matching trên **mặt thật** rõ ràng; phần cuối là một **pipeline 2 bước sạch** (Phase 1 Normalization → Phase 2 Recognition), không chồng tiêu đề/khung.

---

## 2. Ý NGHĨA SCENE (giữ chuẩn — nội dung lõi)

Trái tim thuật toán = **Elastic Matching**, đi từ **cứng → mềm**:
- **Rigid:** graph như khối cứng **trượt** khắp ảnh để định vị mặt (`λ=∞`).
- **Scale + aspect:** phóng to/thu nhỏ toàn cục, kéo width/height cho đúng tỉ lệ.
- **ELASTIC (bước thần kỳ):** graph **được "thả"**; **mỗi node bò tự do** nhích dần về **đúng landmark thật**; **cạnh = lò xo** giữ cấu trúc không vỡ (`λ` hữu hạn, vd 2).
- Chạy theo **2 phase**: **Normalization** (crop mặt chuẩn **128×128**) → **Recognition** (trích **final detailed graph**).

(Nội dung đúng — giữ; nâng hình + dọn bố cục cuối.)

---

## 3. SỬA CỤ THỂ

### 3.1 Mặt thật + node khớp feature (dùng lại cơ chế S08)
- Bỏ `face()` vẽ tay. Dùng **`ImageMobject` `s8_face`** + helper `L(u,v)` + **landmark `s8_landmarks.json`** (cùng người/cùng node với S08–S10).
- B5 "node bò về landmark": node bắt đầu **lệch** (offset), rồi `animate.move_to` về **đúng (u,v) feature thật** trên ảnh — thấy rõ "crawl to true landmark". B6 cạnh = lò xo dọc đúng cạnh thật.

### 3.2 Dọn frame cuối (B7–B9) — pipeline 2 bước sạch
- B7: **FadeOut `title` "Elastic Matching"** trước khi hiện `Two Phases` (chỉ một tiêu đề). Timeline đặt cao (vd y≈1.6), hai mốc `Phase 1` / `Phase 2` rõ.
- B8–B9 bố trí **2 thẻ ngang, không chồng timeline**:
  - **Phase 1 — Normalization (trái):** ảnh mặt thật + khung **crop 128×128** (Square cyan) nằm **dưới** timeline (mép trên thẻ < timeline y). Nhãn `Normalization` + `crop 128×128` trong/dưới thẻ.
  - **`thin_arrow`** nối sang phải (đầu mũi cách thẻ).
  - **Phase 2 — Recognition (phải):** thẻ chứa **final detailed graph** (trên mặt thật thu nhỏ hoặc graph thuần) + nhãn `final detailed graph` (dưới thẻ, trong khung).
  - Đảm bảo: không thẻ nào đè timeline/dots; nhãn không tràn mép; mỗi thẻ heading→nội dung→caption có spacing.

### 3.3 Đường nét "sang hơn"
- Node/edge mảnh đều; lò xo stroke đều biên độ vừa; mũi tên StealthTip dừng cách phần tử.
- `mode_bar` Rigid↔Supple: con trượt di chuyển mượt theo beat; `λ=∞ → λ=2` đặt gọn góc, không đè graph.
- Một tiêu điểm mỗi beat; dim/clear cụm cũ trước khi vào cụm mới (đặc biệt clear sạch trước B7).

---

## 4. STORYBOARD — map đúng segment `transcript.json` (scene_11)

Mốc lấy bằng `seg_end(T, k)`:

| Beat | seg | Mốc≈(s) | Thoại | Hình |
|---|---|---|---|---|
| **B0** | 0 | →6.52 | "the heart of the algorithm, elastic matching, going from rigid to supple." | Mặt thật + graph; thanh `Rigid ↔ Supple`. |
| **B1** | 1 | →12.00 | "the graph is a rigid block, sliding across the image to locate the face." | Graph như khối cứng **trượt**; `λ=∞`; `rigid scan`. |
| **B2** | 2 | →18.44 | "scales globally to match size, and stretches width and height" | `global scale` rồi `width / height` (aspect). |
| **B3** | 3 | →22.42 | "the magic is the final step, the word elastic." | `ELASTIC` punch-in; con trượt về Supple. |
| **B4** | 4 | →24.18 | "The graph is released." | Khoá mở (`released`); chuyển mint. |
| **B5** | 5 | →29.86 | "Each node crawls freely... toward its true landmark" | **Node bò về đúng feature thật**; `nodes crawl to landmarks`. |
| **B6** | 6 | →33.70 | "the edges act as springs holding the structure" | Cạnh = **lò xo**; `λ=2`; `edges act as springs`. |
| **B7** | 7 | →36.10 | "The whole thing runs in two phases." | **FadeOut title cũ**; `Two Phases` + timeline + Phase 1/2. |
| **B8** | 8 | →43.06 | "Normalization, crop the face to 128×128, then recognition." | Thẻ **Normalization** (mặt thật + crop 128×128) → arrow → thẻ **Recognition**. Không chồng. |
| **B9** | 9 | →45.50 | "Extract the final detailed graph." | Trong thẻ Recognition: **final detailed graph** + nhãn. |

**Tail:** `self.wait(max(0, T["duration"] - elapsed - 0.18))` để khớp 46.39s.

---

## 5. ẢNH CẦN CUNG CẤP (user thả vào `assets/`)

- ✅ (bắt buộc bản đẹp) **`assets/s8_face.png`** + **`assets/s8_landmarks.json`** — tái dùng cùng người/cùng node với S08–S10. Không cần ảnh mới riêng cho S11.

Fallback: thiếu ảnh → `face.png`; thiếu landmark → bộ `(u,v)` mặc định (prompt S08). **Không** quay lại mặt vẽ tay. Helper `base = Path(__file__).resolve().parents[1] / "assets"`.

---

## 6. KIỂM TRA & NGHIỆM THU

```bash
python3 -m py_compile video-2-ebgm/release/scene_S11_elastic.py
rg -n "Text\(|font=|Paragraph|make_subtitle|[À-ỹ]" video-2-ebgm/release/scene_S11_elastic.py
ffprobe -v error -show_entries format=duration -of csv=p=0 media/.../S11_Elastic.mp4   # |Δ| ≤ 0.3s vs 46.39
```

Checklist:
- [ ] Mặt thật + node khớp feature; "node crawl to landmark" rõ trên mặt thật.
- [ ] B7 **chỉ một tiêu đề** (title cũ đã fade); timeline không bị thẻ đè.
- [ ] Pipeline Normalization → Recognition sạch, nhãn không tràn/đè.
- [ ] Mọi event đúng segment; tổng khớp 46.39s (|Δ|≤0.3s); English-only; palette; `-qh` OK.
