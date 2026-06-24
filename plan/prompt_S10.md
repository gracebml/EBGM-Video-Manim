# 🤖 PROMPT cho CODEX — THIẾT KẾ LẠI Scene 10 (S10 "Graph Similarity")

> File: `release/scene_S10_graph_sim.py` (class `S10_GraphSim`, `ThreeDScene` góc phẳng `phi=0, theta=-90`).
> Mục tiêu: **đổi mặt vẽ tay → mặt người thật**, **node khớp feature thật**; sửa **chồng chéo chỗ similarity / "force nose"**; design **sang hơn**, **chuẩn nội dung thuật toán**.
> **GIỮ:** `add_sound`, khung `beat_to`/`load_scene_timing`/`seg_end`, English/LaTeX, palette `_common.py`.
> **Audio = `scene_10`, duration = 26.15s** → render xong `ffprobe` cho `|Δ| ≤ 0.3s`.
> Env `vid`; kiểm tra `-pql`, bản cuối `-qh --disable_caching`.

---

## 1. VẤN ĐỀ HIỆN TẠI (phải sửa — xem ảnh user gửi)

1. **Mặt vẽ tay 2D** (`face`) + `pts` cố định → thô, node không khớp feature thật.
2. **Chồng chéo chỗ "force nose onto forehead" (B6–B8):** vẽ **`normal_g` + `bad_g` (warp nose lên) + `nose_arrow` + `stretched` + `spring_edge`** đè lên nhau → **lò xo rối quanh mắt-mũi**, hai graph chồng (ảnh user gửi: cụm cam rối).
3. **Nhãn tràn mép:** `edge stretches` ở `RIGHT*3.25 + UP*1.3` **bị cắt mép phải**; `force nose onto forehead` đáy ổn nhưng cụm trên rối.

**Mục tiêu:** chỉ **một graph trên mặt thật**, kéo **đúng node mũi** lên trán, **một cạnh** căng ra (lò xo gọn), penalty bùng rõ — không hai graph chồng, không nhãn tràn.

---

## 2. Ý NGHĨA SCENE (giữ chuẩn — nội dung lõi)

- Làm sao biết graph **khớp đúng**? EBGM giải một **bài toán tối ưu** = **kéo co (tug of war)**:
  - **Reward** = độ giống jet (`jet similarity`) — kéo về phía khớp texture.
  - **Penalty** = méo hình học của cạnh (`geometric distortion`), **nhân hệ số λ**.
  - **`S_B = Reward − λ · Penalty`**.
- Nếu **ép node mũi lên trán** để khớp texture → **cạnh nối căng ra** → **penalty khổng lồ** → `S_B` tụt → bị loại. (Cân bằng texture ↔ hình học.)

(Nội dung đúng — giữ; chỉ nâng hình + dọn chồng chéo.)

---

## 3. SỬA CỤ THỂ

### 3.1 Mặt thật + node khớp feature (dùng lại cơ chế S08)
- Bỏ `face()` vẽ tay. Dùng **`ImageMobject`** + helper `L(u,v)` + **dùng chung landmark/`s8_landmarks.json`** (cùng người, cùng node với S08/S09) → node rơi đúng mắt/mũi/miệng/trán/cằm.

### 3.2 Dọn "force nose onto forehead" (B6–B8) — hết chồng chéo
- Giữ **một graph duy nhất** trên mặt thật (không vẽ `normal_g` + `bad_g` chồng).
- **Kéo đúng node mũi** từ vị trí đúng → lên **trán** bằng `MoveAlongPath`/`.animate.move_to(forehead)`; node mũi đổi sang coral khi sai vị trí. Một `thin_arrow` ngắn chỉ hướng kéo (đầu mũi cách node).
- **Một cạnh bị căng**: cạnh `eye–nose` (hoặc `nose–mouth`) **kéo dài theo node mũi**; vẽ **một lò xo gọn** dọc đúng cạnh đó (rotate khớp góc cạnh, biên độ nhỏ), **không** thêm lò xo thứ hai chồng.
- Nhãn `force nose onto forehead` (đáy) và `edge stretches` đặt **trong khung, có gap** (đừng để `x>~5.6`); canh theo `get_*()` + margin.

### 3.3 Tug-of-war & công thức (B1–B5) — gọn, không đè
- Công thức `S_B = Reward − λ·Penalty` trên cùng (gap với title).
- Hai card **Reward (mint)** / **Penalty (coral)** hai bên, dây thừng + knot ở giữa; knot dịch theo bên thắng.
- Sub-note trong card (`jet similarity` / `geometric distortion` + bars/spring) **xếp dọc có spacing**, không tràn card; `λ` + `scales the penalty` đặt gần Penalty, không đè card.

### 3.4 Đường nét "sang hơn"
- Node/edge mảnh đều; mũi tên StealthTip dừng cách phần tử; lò xo stroke đều, biên độ vừa.
- `ENORMOUS PENALTY` + vùng đỏ + `S_B ↓`: nhấn mạnh nhưng đặt có gap, không phủ kín graph.
- Một tiêu điểm mỗi beat; dim cụm cũ trước khi vào cụm mới.

---

## 4. STORYBOARD — map đúng segment `transcript.json` (scene_10)

Mốc lấy bằng `seg_end(T, k)`:

| Beat | seg | Mốc≈(s) | Thoại | Hình |
|---|---|---|---|---|
| **B0** | 0 | →1.80 | "How do we know the graph is correctly fitted?" | Mặt thật + graph khớp; nhãn `correctly fitted?`. |
| **B1** | 1 | →6.48 | "EBGM solves an optimization with a very familiar objective," | Công thức `S_B = Reward − λ·Penalty`; dây kéo co + 2 card Reward/Penalty + knot. |
| **B2** | 2 | →7.92 | "a tug of war." | Knot lệch về một bên; nhãn `optimization = tug of war`. |
| **B3** | 3 | →11.16 | "On one side, it rewards jet similarity." | Sáng Reward (mint) + `jet similarity` + bars; knot kéo về mint. |
| **B4** | 4 | →14.56 | "On the other, it penalizes geometric distortion" | Sáng Penalty (coral) + `geometric distortion` + spring; knot về giữa. |
| **B5** | 5 | →16.52 | "of the edges, scaled by lambda." | `λ` + `scales the penalty` (gần Penalty, không đè). |
| **B6** | 6 | →19.88 | "If you force the nose point up onto the forehead" | Mặt thật + graph; **kéo node mũi lên trán** (1 graph, node coral). Nhãn `force nose onto forehead`. |
| **B7** | 7 | →22.36 | "to match texture, the connecting edge stretches," | **Một cạnh căng** + lò xo gọn dọc cạnh; nhãn `edge stretches` (trong khung). |
| **B8** | 8 | →25.62 | "and the algorithm hits you with an enormous penalty." | Vùng đỏ + `ENORMOUS PENALTY` + `S_B ↓`. |

**Tail:** `self.wait(max(0, T["duration"] - elapsed - 0.18))` để khớp 26.15s.

---

## 5. ẢNH CẦN CUNG CẤP (user thả vào `assets/`)

- ✅ (bắt buộc bản đẹp) **`assets/s8_face.png`** + **`assets/s8_landmarks.json`** — **tái dùng cùng người & cùng landmark** với S08/S09 (mạch hình nhất quán, node khớp chuẩn). Không cần ảnh mới riêng cho S10.

**Mô tả:** chỉ cần khuôn mặt chính diện chuẩn đã dùng ở S08; toàn bộ S10 là thao tác trên graph của khuôn mặt đó (kéo node mũi, căng cạnh).

Fallback: thiếu ảnh → dùng `face.png`; thiếu landmark file → bộ `(u,v)` mặc định (mục 3.1 của prompt S08). **Không** quay lại mặt vẽ tay. Helper `base = Path(__file__).resolve().parents[1] / "assets"`.

---

## 6. KIỂM TRA & NGHIỆM THU

```bash
python3 -m py_compile video-2-ebgm/release/scene_S10_graph_sim.py
rg -n "Text\(|font=|Paragraph|make_subtitle|[À-ỹ]" video-2-ebgm/release/scene_S10_graph_sim.py
ffprobe -v error -show_entries format=duration -of csv=p=0 media/.../S10_GraphSim.mp4   # |Δ| ≤ 0.3s vs 26.15
```

Checklist:
- [ ] Mặt thật + node khớp feature; bỏ mặt vẽ tay.
- [ ] B6–B8 chỉ **một graph**, kéo đúng node mũi, **một cạnh căng + một lò xo** — hết chồng chéo.
- [ ] `edge stretches` và mọi nhãn **không tràn mép**, có gap; card Reward/Penalty không đè sub-note.
- [ ] Tug-of-war đọc rõ; penalty bùng rõ nhưng không phủ kín graph.
- [ ] Mọi event đúng segment; tổng khớp 26.15s (|Δ|≤0.3s); English-only; palette `_common.py`; `-qh` OK.
