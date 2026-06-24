# 🤖 PROMPT cho CODEX — THIẾT KẾ LẠI Scene 5 (S05 "Gabor wavelets")

> File: `release/scene_S05_gabor.py` (class `S05_Gabor`, `ThreeDScene` góc phẳng `phi=0, theta=-90`).
> Mục tiêu: **hiệu ứng bớt đơn điệu** (đang gần như chỉ `FadeIn`); dùng **mặt thật + patch thật + node khớp feature**; design **sang hơn**, **chuẩn nội dung thuật toán**.
> **GIỮ:** `add_sound`, khung `beat_to`/`load_scene_timing`/`seg_end`, English/LaTeX, palette `_common.py`. **GIỮ hàm `gabor_array(...)`** (ảnh filter Gabor thật, rất tốt — tái dùng).
> **Audio = `scene_05`, duration = 36.55s** → render xong `ffprobe` cho `|Δ| ≤ 0.3s`.
> Env `vid`; kiểm tra `-pql`, bản cuối `-qh --disable_caching`.

---

## 1. VẤN ĐỀ HIỆN TẠI (phải sửa)

1. **Hiệu ứng đơn điệu:** hầu hết là `FadeIn/Create` tĩnh. Các ý động lõi của Gabor **chưa được "diễn"**: (a) sine × Gaussian **hợp thành** wavelet, (b) filter **quét** qua patch và **bật response** ở cạnh, (c) DC-free = đổi sáng nền nhưng response **không đổi**.
2. **Mặt vẽ tay** (`simple_face`) + **patch giả** (`pixel_grid` màu ngẫu nhiên) → nên dùng **mặt thật** + **patch thật** (crop da/đuôi mắt có vân/cạnh) để Gabor có ý nghĩa.
3. Bố cục/nét chưa thật sang; transition cụm này sang cụm khác hơi khô.

**Mục tiêu:** giữ mạch 6 ý nhưng **diễn hoạt** (build wavelet, quét filter, DC-free), trên **mặt + patch thật**, nét sang.

---

## 2. Ý NGHĨA SCENE (giữ chuẩn — nội dung lõi)

- **Micro:** AI "nhìn" **một điểm** trên mặt thế nào?
- **Pixel** rất nhạy sáng → **mượn từ sinh học**.
- **Gabor wavelet** = **sine wave** bị "nhốt" trong **Gaussian envelope**: `ψ(x) = e^{-x²/2σ²} · cos(kx)`.
- Hoạt động như **filter**: chỉ bắt **nếp nhăn/cạnh** ở **một hướng + một tần số** cụ thể.
- **DC-free:** **khử thành phần ánh sáng nền** → đổi độ sáng, response **vẫn ổn định**.
- **Lớp filter đầu của CNN bắt cạnh** ≈ **đúng cách visual cortex** hoạt động.

(Nội dung đúng — giữ; nâng hình + diễn hoạt.)

---

## 3. SỬA CỤ THỂ (trọng tâm: diễn hoạt + ảnh thật)

### 3.1 B0 — mặt thật + patch thật, "trích" một điểm
- Mặt thật `s8_face` (`L(u,v)` + landmark như S08). Focus **đuôi mắt** (ring mint).
- **Patch thật bay ra:** crop quanh điểm focus (`s5_patch` hoặc crop runtime), **phóng to** với 2 đường nối khung (magnifier) — chuyển động "lift & zoom", không chỉ FadeIn. Nhãn `local patch`.

### 3.2 B1 — pixel nhạy sáng (diễn fragility) → sinh học
- Patch pixel **nhấp nháy** khi đổi sáng (Indicate/đổi opacity) → cho thấy "rất nhạy sáng". Gạch `raw pixels` (coral). Sang **borrow from biology** (icon receptive field/cortex gọn).

### 3.3 B2 — BUILD wavelet bằng animation (không FadeIn rời)
- Vẽ **sine wave** trước → **Gaussian envelope** trượt vào ôm lấy nó → **nhân**: sine **bị tắt dần hai biên** **biến hình** thành **Gabor wavelet** (dùng `Transform`/`ReplacementTransform` hoặc animate hàm). Hiển thị `sine × Gaussian = Gabor` + công thức `ψ(x)=e^{-x²/2σ²}cos(kx)`.
- Đây là điểm "sang" nhất: thấy rõ wavelet **được tạo ra**.

### 3.4 B3 — filter QUÉT patch, response bật ở cạnh
- Đặt `mini_filter` (Gabor thật) **trượt ngang** qua **patch thật**; khi filter **trùng hướng cạnh** → **thanh response sáng/cao lên** (animate độ dài/độ sáng theo vị trí). 
- **Xoay qua các hướng** 0°/45°/90° (`Rotate`/ReplacementTransform) → response thay đổi → nhấn "one orientation · one frequency".

### 3.5 B4 — DC-free, diễn rõ
- Cùng một **patch thật** ở **2 mức sáng** (tối/sáng). Animate **trừ mean light** (`− mean`) → **hai response hội tụ về giống nhau** (hai thanh nhập làm một / cùng chiều dài). Nhãn lớn `DC-free` + `same edge response`.

### 3.6 B5 — CNN first-layer ≈ visual cortex
- Lưới **filter Gabor thật** (dùng `gabor_array` nhiều hướng) như "CNN first-layer filters"; cạnh đó **minh hoạ visual cortex** (ảnh `s5_cortex.png` nếu có, hoặc receptive-field gọn). Nhãn `CNN first-layer filters` `≈ visual cortex`. Có thể nhấp nháy nhẹ để liên hệ.

### 3.7 Đường nét "sang hơn"
- Bo góc/khung patch nhất quán; mũi tên StealthTip; gradient nhẹ; một tiêu điểm mỗi beat; clear cụm cũ trước khi vào cụm mới; nhãn không tràn/đè.

---

## 4. STORYBOARD — map đúng segment `transcript.json` (scene_05)

Mốc lấy bằng `seg_end(T, k)`:

| Beat | seg | Mốc≈(s) | Thoại | Hình |
|---|---|---|---|---|
| **B0** | 0 | →4.22 | "How does the AI see a single point on a face?" | Mặt thật + focus đuôi mắt → patch thật lift & zoom; `How does AI see one point?` |
| **B1** | 1 | →9.84 | "Instead of pixels, which are very light-sensitive, scientists borrowed from biology." | Patch pixel nhấp nháy theo sáng (`raw pixels` ✗) → `borrow from biology`. |
| **B2** | 2 | →15.88 | "Gabor wavelets... a sine wave trapped inside a Gaussian envelope." | **Build**: sine → Gaussian ôm vào → Gabor wavelet + công thức. |
| **B3** | 3 | →22.30 | "a filter, capturing only wrinkles and edges at one orientation and frequency." | Filter **quét** patch thật, response bật ở cạnh; xoay 0/45/90°. |
| **B4** | 4 | →28.24 | "It cancels out the background light component. It's DC-free." | Patch 2 mức sáng → `− mean` → response **giống nhau**; `DC-free`. |
| **B5** | 5 | →36.06 | "the first layers of a CNN detect edges... mirrors the visual cortex." | Lưới Gabor (CNN first-layer) `≈ visual cortex`. |

**Tail:** `self.wait(max(0, T["duration"] - elapsed - 0.18))` để khớp 36.55s.

---

## 5. ẢNH CẦN CUNG CẤP (user thả vào `assets/`)

- ✅ **`assets/s8_face.png`** + **`assets/s8_landmarks.json`** — mặt thật + focus điểm (tái dùng cùng người/node với S06/S08…).
- ✅ (khuyến nghị) **`assets/s5_patch.png`** — **crop một mảng da/đuôi mắt có vân & cạnh rõ** (~256px), để demo filter Gabor & DC-free trực quan. *(Không có → crop runtime quanh điểm focus từ `s8_face`.)*
- ✅ (tuỳ chọn, B5) **`assets/s5_cortex.png`** — minh hoạ **visual cortex / receptive field** (hoặc ảnh CNN first-layer filters thật). Không có → vẽ receptive-field gọn.

**Mô tả:** patch nên có **cạnh/nếp nhăn rõ** (đuôi mắt, mí, vân da) để thấy Gabor "bắt cạnh"; ảnh cortex chỉ cần gợi ý sinh học, tông hợp navy.

Fallback: thiếu ảnh → `face.png`/patch tự sinh. **Filter Gabor giữ `gabor_array`** (đã là ảnh thật). Helper `base = Path(__file__).resolve().parents[1] / "assets"`.

---

## 6. KIỂM TRA & NGHIỆM THU

```bash
python3 -m py_compile video-2-ebgm/release/scene_S05_gabor.py
rg -n "Text\(|font=|Paragraph|make_subtitle|[À-ỹ]" video-2-ebgm/release/scene_S05_gabor.py
ffprobe -v error -show_entries format=duration -of csv=p=0 media/.../S05_Gabor.mp4   # |Δ| ≤ 0.3s vs 36.55
```

Checklist:
- [ ] Hết đơn điệu: **build wavelet** (sine×Gaussian), **filter quét** patch, **DC-free** đều có animation thật.
- [ ] Mặt thật + patch thật + focus điểm khớp feature; filter Gabor giữ `gabor_array`.
- [ ] Mỗi beat một tiêu điểm; nhãn không tràn/đè; nét sang, nhất quán.
- [ ] Mọi event đúng segment; tổng khớp 36.55s (|Δ|≤0.3s); English-only; palette; `-qh` OK.
