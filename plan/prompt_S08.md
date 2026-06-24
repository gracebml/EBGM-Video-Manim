# 🤖 PROMPT cho CODEX — THIẾT KẾ LẠI Scene 8 (S08 "Image Graph")

> File: `release/scene_S08_image_graph.py` (class `S08_ImageGraph`, `ThreeDScene` góc phẳng `phi=0, theta=-90`).
> Mục tiêu: **đổi mặt vẽ tay → mặt người thật**; **đặt các node đồ thị đúng vào feature thật** (mắt/mũi/miệng…); design **sang hơn**, **chuẩn nội dung thuật toán**.
> **GIỮ:** `add_sound`, khung `beat_to`/`load_scene_timing`/`seg_end`, English/LaTeX (`en_label`, `MathTex`/`Tex` + `EN_TEX_TEMPLATE`), palette `_common.py`.
> **Audio = `scene_08`, duration = 23.64s** → render xong `ffprobe` cho `|Δ| ≤ 0.3s`.
> Env `vid`; kiểm tra `-pql`, bản cuối `-qh --disable_caching`.

---

## 1. VẤN ĐỀ HIỆN TẠI (phải sửa)

1. **Mặt vẽ tay 2D** (`face_outline`: ellipse + line mũi + arc miệng) → thô, trừu tượng. Người xem không thấy "đồ thị đặt lên một KHUÔN MẶT THẬT".
2. **Node đặt theo toạ độ `pts` cố định** (forehead/eye_l/eye_r/nose/…) → khớp với mặt vẽ, **không khớp feature thật**. Cần node **rơi đúng lên đồng tử, cánh mũi, khoé miệng, cằm, gò má** của ảnh thật.
3. Chưa "sang": tách "skin surface | bone structure" ở B5–B6 dùng lại mặt vẽ thu nhỏ → loãng.

**Mục tiêu:** một khuôn mặt thật, **graph landmark khớp chính xác**, nét sạch; rồi tách rõ **2 lớp thông tin** (texture trên node ↔ hình học trên edge) đúng tinh thần EBGM.

---

## 2. Ý NGHĨA SCENE (giữ chuẩn — nội dung lõi)

- Rải các **jet** lên **landmark** (mắt, mũi, miệng) rồi **nối lại** → **Image Graph**.
- **Node = jet = "barcode texture"** của điểm đó (thông tin **bề mặt/da**).
- **Edge = khoảng cách hình học** (`Δx`) giữa các điểm (thông tin **cấu trúc/xương**).
- **Điểm thiên tài của EBGM:** **tách hẳn** thông tin **skin surface** (texture, nằm trên node) khỏi **bone structure** (hình học, nằm trên edge) → máy **xử lý độc lập** từng phần.

(Nội dung hiện đúng — giữ; chỉ nâng chất lượng hình + độ chính xác landmark.)

---

## 3. SỬA CỤ THỂ

### 3.1 Mặt người thật + node khớp feature (quan trọng nhất)
- Bỏ `face_outline()`. Dùng **`ImageMobject`** mặt thật (mục 5), set chiều cao cố định (vd `img.set_height(4.6)`), đặt trong khung bo góc nhất quán (`RoundedRectangle` viền `ACCENT_BLUE` mảnh). Dùng `Group` khi trộn ảnh với vector.
- **Đặt landmark bằng toạ độ chuẩn hoá theo ảnh**, KHÔNG hardcode toạ độ scene. Dùng helper map từ `(u, v) ∈ [0,1]` (gốc trái-trên ảnh) → điểm scene:
  ```python
  def L(u, v):  # u: trái→phải, v: trên→dưới (0..1) theo ẢNH
      tl = img.get_corner(UL); br = img.get_corner(DR)
      return np.array([tl[0] + u*(br[0]-tl[0]), tl[1] + v*(br[1]-tl[1]), 0])
  ```
- **Bộ landmark (đặt đúng feature thật)** — tinh chỉnh `(u,v)` theo ảnh user cung cấp; gợi ý mặc định cho mặt chính diện căn giữa:
  - `eye_l ≈ (0.36, 0.40)`, `eye_r ≈ (0.64, 0.40)` (đồng tử)
  - `nose ≈ (0.50, 0.56)` (chóp mũi), `nostril_l ≈ (0.44,0.58)`, `nostril_r ≈ (0.56,0.58)` *(tuỳ chọn)*
  - `mouth_l ≈ (0.41, 0.72)`, `mouth_r ≈ (0.59, 0.72)`, `mouth_c ≈ (0.50,0.72)`
  - `brow_l ≈ (0.36,0.33)`, `brow_r ≈ (0.64,0.33)` *(tuỳ chọn)*, `chin ≈ (0.50, 0.90)`
  - `cheek_l ≈ (0.30, 0.62)`, `cheek_r ≈ (0.70, 0.62)`
  > **Bắt buộc tinh chỉnh** các `(u,v)` này cho khớp ảnh thật (render `-pql` 1 frame để soi). Nếu user cung cấp file landmark (mục 5) thì đọc trực tiếp, khỏi đoán.
- **Edges** nối theo quan hệ giải phẫu (mắt–mắt, mắt–mũi, mũi–miệng, miệng–cằm, mắt–gò má…), `thin` line đều, opacity ~0.7.
- Mỗi node có **jet_icon nhỏ** (rays + ring) đặt **đúng tâm landmark**, không lệch.

### 3.2 Tách "skin surface ↔ bone structure" (B5–B6) sang hơn
Thay vì copy mặt vẽ thu nhỏ:
- **Trái = SKIN SURFACE:** vẫn ảnh mặt thật (hoặc bản mờ/đơn sắc cyan) + **chỉ các node/jet** sáng lên → nhấn "texture nằm trên node".
- **Phải = BONE STRUCTURE:** **chỉ còn graph hình học** (node + edge, **bỏ ảnh**), tông mint, gợi "khung xương" → nhấn "hình học nằm trên edge".
- Một divider dọc mảnh `GRID_LINE` giữa hai bên. Mỗi bên một tiêu đề (`skin surface` / `bone structure`) có gap, không đè graph.

### 3.3 Đường nét "sang hơn"
- Node `Dot` `ACCENT_LAVENDER`, viền nhẹ; edge `thin` đều; jet_icon stroke ~1.6.
- Panel `node = jet` (barcode) & `edge = distance` (`Δx`): theo CLAUDE.md — đủ cao, heading→icon→note có spacing, **không đè**; mũi tên/khoanh tròn highlight dừng cách chữ.
- Mỗi beat một tiêu điểm; dim cụm cũ (kể cả nhãn) trước khi đưa cụm mới.
- Highlight node mẫu (eye_l) và edge mẫu (eye_l–nose) bằng vòng/đường đậm hơn, không phá bố cục.

---

## 4. STORYBOARD — map đúng segment `transcript.json` (scene_08)

Mốc lấy bằng `seg_end(T, k)` (đừng hardcode):

| Beat | seg | Mốc≈(s) | Thoại | Hình |
|---|---|---|---|---|
| **B0** | 0 | →2.06 | "Sprinkle these jets onto the landmarks," | Mặt thật vào; **jet_icon rải lên các landmark** (`LaggedStart`), khớp đúng feature. Nhãn `sprinkle jets onto landmarks`. |
| **B1** | 1 | →5.82 | "eyes, nose, mouth, and connect them." | Node mọc tại mắt/mũi/miệng + **edges nối** (Create lần lượt). Nhãn `eyes · nose · mouth`. |
| **B2** | 2 | →7.84 | "And you have an image graph." | Đặt tên: title `Image Graph` đổi màu lavender + `SurroundingRectangle`. |
| **B3** | 3 | →11.26 | "The nodes hold the texture barcode, the jet," | Khoanh 1 node (eye_l); panel `node = jet` + **mini-barcode** (texture). |
| **B4** | 4 | →13.66 | "the edges hold geometric distances." | Highlight 1 edge (eye_l–nose); panel `edge = distance` + `Δx`. |
| **B5** | 5 | →18.72 | "The genius key, EBGM fully separates skin surface" | Tách màn: trái **skin surface** (ảnh + node/jet sáng). Nhãn `skin surface`. |
| **B6** | 6 | →20.34 | "information from bone structure" | Phải **bone structure** (chỉ graph hình học, mint). Nhãn `bone structure`. |
| **B7** | 7 | →22.90 | "so the machine can process each independently." | Hai bên cùng sáng + nhãn `processed independently`; nhấn 2 lớp tách bạch. |

**Tail:** `self.wait(max(0, T["duration"] - elapsed - 0.18))` để khớp 23.64s.

---

## 5. ẢNH CẦN CUNG CẤP (user thả vào `assets/`)

- ✅ (bắt buộc cho bản đẹp) **`assets/s8_face.png`** — **mặt người thật, chính diện thẳng, biểu cảm trung tính, ánh sáng đều, độ phân giải cao**; **thấy rõ: 2 mắt, sống/chóp mũi, miệng, đường viền hàm + cằm, trán/chân tóc** (để đặt node forehead/chin/cheek chuẩn). Vuông hoặc dọc ~768–1024px, nền tối/đồng nhất hợp tông navy.
  - *Có thể tái dùng `s6_face.png` nếu nó là mặt chính diện sạch (lý tưởng: cùng một người xuyên S06/S08 để mạch hình nhất quán).*
- ✅ (khuyến nghị, giúp node khớp **tuyệt đối chuẩn**) **`assets/s8_landmarks.json`** — toạ độ landmark đã detect, dạng `(u,v)` chuẩn hoá `[0,1]` theo ảnh (hoặc pixel kèm kích thước ảnh). Nếu có file này, codex đọc thẳng thay vì tinh chỉnh tay. Ví dụ format:
  ```json
  {"image":"s8_face.png","w":1024,"h":1024,
   "landmarks":{"eye_l":[0.36,0.40],"eye_r":[0.64,0.40],"nose":[0.50,0.56],
                "mouth_l":[0.41,0.72],"mouth_r":[0.59,0.72],"chin":[0.50,0.90],
                "cheek_l":[0.30,0.62],"cheek_r":[0.70,0.62]}}
  ```

**Mô tả ảnh mong muốn (để user chuẩn bị):** chân dung người thật nhìn thẳng, tóc không che trán/mắt, không nghiêng đầu, miệng khép, ánh sáng phẳng — để 9–12 landmark rơi đúng feature.

Fallback: thiếu ảnh → dùng `face.png`; thiếu landmark file → dùng bộ `(u,v)` mặc định ở mục 3.1 (đã tinh chỉnh). **Không** quay lại mặt vẽ tay. Helper kiểm tra tồn tại `base = Path(__file__).resolve().parents[1] / "assets"`.

---

## 6. KIỂM TRA & NGHIỆM THU

```bash
python3 -m py_compile video-2-ebgm/release/scene_S08_image_graph.py
rg -n "Text\(|font=|Paragraph|make_subtitle|[À-ỹ]" video-2-ebgm/release/scene_S08_image_graph.py   # phải rỗng
ffprobe -v error -show_entries format=duration -of csv=p=0 media/.../S08_ImageGraph.mp4             # |Δ| ≤ 0.3s vs 23.64
```

Checklist:
- [ ] Dùng **mặt người thật** (`ImageMobject`); bỏ hẳn mặt vẽ tay.
- [ ] **Node rơi đúng feature thật** (đồng tử/mũi/khoé miệng/cằm/gò má) — đã tinh chỉnh hoặc đọc từ landmark file.
- [ ] B5–B6 tách rõ **skin surface (node/jet)** ↔ **bone structure (edge hình học)**, không loãng.
- [ ] Panel `node=jet` / `edge=distance` không chồng; highlight node/edge mẫu gọn.
- [ ] Mọi event rơi đúng segment; tổng khớp 23.64s (|Δ|≤0.3s); English-only; palette `_common.py`; render `-qh` OK.
