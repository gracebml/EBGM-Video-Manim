# 🤖 PROMPT cho CODEX — THIẾT KẾ LẠI Scene 15 (S15 "The Big Picture")

> File: `release/scene_S15_big_picture.py` (class `S15_BigPicture`, `Scene` 2D).
> Mục tiêu: **hiệu ứng bớt đơn điệu**, **frame cuối giàu hơn**; dùng **ảnh thật** (mặt/động vật/xe, mặt + kính thật); design **sang hơn**, **chuẩn nội dung**.
> **GIỮ:** `add_sound`, khung `beat_to`/`load_scene_timing`/`seg_end`, English/LaTeX, palette `_common.py`.
> **Audio = `scene_15`, duration = 35.53s** → render xong `ffprobe` cho `|Δ| ≤ 0.3s`.
> Env `vid`; kiểm tra `-pql`, bản cuối `-qh --disable_caching`.

---

## 1. VẤN ĐỀ HIỆN TẠI (phải sửa)

1. **Icon vẽ tay đơn điệu:** faces/animals/vehicles/variants là icon line thô; PCA↔EBGM dùng mặt vẽ + kính vẽ → kém thuyết phục.
2. **Hiệu ứng đơn điệu:** hầu hết chỉ `FadeIn`. Thiếu nhịp tương phản cho ý "PCA vỡ toàn cục vì 1 cặp kính" vs "EBGM khoanh vùng rủi ro".
3. **Frame cuối sơ sài:** `Limits` (2 dấu X + chữ) + 1 hộp `no massive training` → trống trải, chưa chốt mạnh.

**Mục tiêu:** dùng **ảnh thật** cho in-class examples & demo kính; tương phản PCA(toàn cục đỏ) ↔ EBGM(chỉ node mắt) bằng hiệu ứng rõ; frame cuối là một **bảng tổng kết cân đối, sang**.

---

## 2. Ý NGHĨA SCENE (giữ chuẩn — nội dung lõi)

- **Zoom out:** EBGM giải **lớp bài toán rộng** — *in-class recognition under variants*: **người, động vật, xe…**.
- **Khác PCA:** một cặp **kính râm** làm **vector toàn cục của PCA hỏng cả ảnh**; còn **EBGM khoanh vùng rủi ro** — **chỉ các jet ở mắt bị nhiễu**, phần còn lại an toàn.
- **Giới hạn:** yếu khi xoay **> 22°**, dễ vỡ khi **landmark bị che**.
- Nhưng là thuật toán **không cần training khổng lồ**, EBGM **làm rất tốt**.

(Nội dung đúng — giữ; nâng hình + hiệu ứng + frame cuối.)

---

## 3. SỬA CỤ THỂ

### 3.1 In-class examples = ảnh thật
- 4 card: **mặt người thật** / **động vật thật** / **xe thật** / **variants** (graph). Khung bo góc nhất quán; xuất hiện `LaggedStart` có scale-pop nhẹ (bớt đơn điệu).

### 3.2 PCA ↔ EBGM với ảnh + kính thật, tương phản mạnh
- Hai panel: **PCA** (trái) vs **EBGM** (phải), mỗi bên một **mặt thật** (cùng người).
- Đeo **kính râm thật** (overlay `s15_sunglasses.png` hoặc ảnh `s15_face_glasses.png`).
- **PCA:** khi kính xuất hiện → **heat đỏ lan TOÀN ảnh** (vector toàn cục hỏng) — hiệu ứng đỏ loang. Nhãn `global vector disturbed`.
- **EBGM:** chỉ **2 node mắt** chuyển coral + ring cảnh báo; các node còn lại **mint, an toàn**. Nhãn `only eye jets disturbed · the rest stay safe`.
- Dùng `Indicate`/đổi màu/loang để tạo tương phản, không chỉ `FadeIn`.

### 3.3 Frame cuối — bảng tổng kết sang
- Hai **chip Limits** rõ (X coral): `weak beyond 22°` · `fragile with occluded landmarks`.
- **Điểm mạnh chốt:** một dải/hero `no massive training required` (mint) nổi bật, kèm vài chip phụ (`few samples`, `compartmentalized risk`) hoặc một mini face-grid sáng lên → cảm giác kết luận đầy đặn, không trống.

### 3.4 Đường nét "sang hơn"
- Bo góc & cỡ chữ nhất quán; gradient nhẹ; mỗi beat một tiêu điểm; clear cụm cũ trước khi vào cụm mới; nhãn không tràn/đè.

---

## 4. STORYBOARD — map đúng segment `transcript.json` (scene_15)

Mốc lấy bằng `seg_end(T, k)`:

| Beat | seg | Mốc≈(s) | Thoại | Hình |
|---|---|---|---|---|
| **B0–B1** | 0–1 | →9.98 | "EBGM solves a broad class... human faces, animals, or vehicles." | 4 card ảnh thật (face/animal/vehicle/variants), pop nhẹ. |
| **B2** | 2 | →15.10 | "Unlike PCA, wrecked across the whole image by a single pair of sunglasses," | PCA panel: mặt thật + kính → **heat đỏ loang toàn ảnh**; `global vector disturbed`. |
| **B3–B5** | 3–5 | →23.20 | "EBGM compartmentalizes risk. Glasses? Only the eye jets disturbed. The rest stay safe." | EBGM panel: chỉ 2 node mắt coral + ring; node khác mint; `only eye jets disturbed`. |
| **B6–B8** | 6–8 | →29.74 | "it has limits. Weak beyond 22°. Fragile when landmarks occluded." | `Limits` + 2 chip X. |
| **B9** | 9 | →35.12 | "needs no massive training, EBGM did exceptionally well." | Hero `no massive training required` + chip phụ → bảng tổng kết đầy đặn. |

**Tail:** `self.wait(max(0, T["duration"] - elapsed - 0.18))` để khớp 35.53s.

---

## 5. ẢNH CẦN CUNG CẤP (user thả vào `assets/`)

- ✅ **`assets/s15_face.png`** — mặt người thật (có thể tái dùng `s8_face.png`).
- ✅ **`assets/s15_animal.png`** — một con vật rõ (mèo/chó), chính diện.
- ✅ **`assets/s15_vehicle.png`** — một chiếc xe rõ (ô tô), góc 3/4 hoặc bên.
- ✅ (demo kính) **`assets/s15_sunglasses.png`** (PNG nền trong, để overlay lên mặt) **hoặc** **`assets/s15_face_glasses.png`** (mặt thật đã đeo kính râm).

**Mô tả:** ảnh chính diện rõ nét, nền gọn; ảnh động vật/xe đủ "đại diện lớp" để minh hoạ in-class recognition; kính râm che đúng vùng mắt.

Fallback: thiếu ảnh nào → icon vẽ tay cũ cho item đó (vẫn render được). Helper `base = Path(__file__).resolve().parents[1] / "assets"`.

---

## 6. KIỂM TRA & NGHIỆM THU

```bash
python3 -m py_compile video-2-ebgm/release/scene_S15_big_picture.py
rg -n "Text\(|font=|Paragraph|make_subtitle|[À-ỹ]" video-2-ebgm/release/scene_S15_big_picture.py
ffprobe -v error -show_entries format=duration -of csv=p=0 media/.../S15_BigPicture.mp4   # |Δ| ≤ 0.3s vs 35.53
```

Checklist:
- [ ] In-class examples + PCA/EBGM dùng **ảnh thật**; kính râm thật.
- [ ] Tương phản PCA(đỏ toàn cục) ↔ EBGM(chỉ node mắt) rõ bằng hiệu ứng, không chỉ FadeIn.
- [ ] Frame cuối đầy đặn (limits + hero no-training + chip phụ), không trống.
- [ ] Mọi event đúng segment; tổng khớp 35.53s (|Δ|≤0.3s); English-only; palette; `-qh` OK.
