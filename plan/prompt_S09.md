# 🤖 PROMPT cho CODEX — THIẾT KẾ LẠI Scene 9 (S09 "Face Bunch Graph")

> File: `release/scene_S09_bunch_graph.py` (class `S09_BunchGraph`, `ThreeDScene` góc phẳng `phi=0, theta=-90`).
> Mục tiêu: **đổi mặt vẽ tay → mặt người thật**, **node khớp feature thật**; dọn **lộn xộn chỗ bunch graph**; design **sang hơn**, **chuẩn nội dung thuật toán**.
> **GIỮ:** `add_sound`, khung `beat_to`/`load_scene_timing`/`seg_end`, English/LaTeX, palette `_common.py`.
> **Audio = `scene_09`, duration = 25.50s** → render xong `ffprobe` cho `|Δ| ≤ 0.3s`.
> Env `vid`; kiểm tra `-pql`, bản cuối `-qh --disable_caching`.

---

## 1. VẤN ĐỀ HIỆN TẠI (phải sửa — xem ảnh user gửi)

1. **Mặt vẽ tay 2D** (`face_outline`) + `base_pts` cố định → thô, không khớp feature thật.
2. **Bunch graph lộn xộn:** B3 `stack` chồng 6 graph warp lệch nhau tạo **mớ đường cyan rối** ở giữa; B4–B9 nhồi `bunch_card` + 3 eye icon + search beam + Local Expert + fit arrows + `combo_lines` (opacity 0.18) → **rối, đè nhau** (đúng ảnh user gửi: vùng giữa be bét, nhãn chồng).
3. Eye icon vẽ tay (`narrow/round/glasses`) kém thuyết phục cho ý "narrow/round/spectacled eyes".

**Mục tiêu:** một stack mẫu **gọn, đọc được**; "eye node = a bunch" dùng **ảnh mắt thật**; luồng search → local expert → coverage rõ ràng, không chồng.

---

## 2. Ý NGHĨA SCENE (giữ chuẩn — nội dung lõi)

- **Một graph không khớp mọi khuôn mặt** → giải pháp: **Face Bunch Graph (FBG)**.
- **Chồng nhiều graph mẫu** (nhiều người/biểu cảm) → mỗi **node** không còn giữ 1 mắt mà là **cả một "bunch"** các phiên bản (narrow / round / spectacled…).
- Gặp người lạ: hệ **dò trong bunch** và **bầu ra "local expert"** = phiên bản khớp nhất **cho từng landmark**.
- **Tổ hợp chéo** các local expert → **độ phủ gần như vô hạn** từ ít ảnh mẫu.

(Nội dung đúng — giữ; chỉ nâng hình + dọn bố cục.)

---

## 3. SỬA CỤ THỂ

### 3.1 Mặt thật + node khớp feature (dùng lại cơ chế S08)
- Bỏ `face_outline`. Dùng **`ImageMobject`** + helper `L(u,v)` map toạ độ chuẩn hoá `[0,1]` theo ảnh → scene (giống S08), và **dùng chung bộ landmark / file `s8_landmarks.json`** để node rơi đúng mắt/mũi/miệng/cằm.
- B0: hai **khuôn mặt thật khác nhau** (model vs "my face") — graph khớp người này **không** khớp người kia (node lệch khỏi feature) → nhãn `one graph cannot fit every face`.

### 3.2 Dọn "stack many sample graphs" (B3) — hết rối
Thay vì chồng 6 graph warp đè nhau:
- Vẽ **stack theo chiều sâu kiểu film/thẻ**: 4–6 **thumbnail mặt thật khác nhau** (mỗi cái có graph riêng màu khác), **offset đều**, các lớp sau **mờ dần + nhỏ dần**, lớp trước rõ. Có khoảng cách → đọc ra "nhiều graph mẫu xếp chồng", không thành mớ đường.
- Nhãn `stack many sample graphs` đặt dưới, có gap.

### 3.3 "eye node = a bunch" (B4–B5) — dùng ẢNH MẮT THẬT
- Khoanh node mắt trên graph → bung ra một **`bunch_card` ngang** chứa **3 crop mắt thật**: `narrow` / `round` / `spectacled`, mỗi crop trong khung nhỏ bo góc, **cách đều, không đè**; nhãn từng loại **bên dưới từng crop** (trong card, có spacing).
- Tiêu đề `eye node = a bunch` trên card (gap rõ). Bỏ eye icon vẽ tay.

### 3.4 Search → Local Expert → Coverage (B6–B9) — luồng rõ, không chồng
- B6 `search the bunch`: một **mặt người lạ** (thật, mờ) bên trái + **một `thin_arrow`** quét vào card (đầu mũi cách card). Nhãn `search the bunch` đặt **trên**, không đè arrow.
- B7 `Local Expert`: `SurroundingRectangle` quanh **đúng 1 crop** được chọn + nhãn `Local Expert` (gap rõ, không tràn mép).
- B8 `best fit for each landmark`: thay vì 3 fit_arrows xuống dãy dot rời, gom thành **hàng "selected" gọn** dưới card, mũi tên ngắn, đầu mũi cách dot.
- B9 `almost limitless coverage`: **bỏ combo_lines mờ 0.18 rối**. Thay bằng **lưới tổ hợp gọn**: vài đường nối tiêu biểu (opacity ~0.35, stroke đều) hoặc một grid nhỏ "expert₁ × expert₂ × …" → nhấn "tổ hợp chéo". Nhãn lớn `almost limitless coverage` trên cùng.
- Một tiêu điểm mỗi beat; dim cụm cũ (kể cả nhãn) trước khi vào cụm mới.

### 3.5 Đường nét "sang hơn"
- Node `Dot` lavender, edge `thin` đều; khung crop nhất quán; mũi tên StealthTip dừng cách phần tử.
- Gradient nhẹ phân biệt các lớp stack; tránh mọi thứ cùng độ đậm.

---

## 4. STORYBOARD — map đúng segment `transcript.json` (scene_09)

Mốc lấy bằng `seg_end(T, k)`:

| Beat | seg | Mốc≈(s) | Thoại | Hình |
|---|---|---|---|---|
| **B0** | 0 | →2.00 | "But your graph can't perfectly fit my face." | 2 mặt thật khác nhau; graph khớp người A nhưng **lệch feature** ở người B. Nhãn `one graph cannot fit every face`. |
| **B1** | 1 | →3.12 | "The solution?" | Dọn sạch; `The solution:` hiện. |
| **B2** | 2 | →4.82 | "The Face Bunch Graph." | `FACE BUNCH GRAPH` + box, đổi màu nhấn. |
| **B3** | 3 | →8.16 | "By stacking dozens of different graphs," | **Stack thumbnail mặt thật** theo chiều sâu (gọn, mờ dần). Nhãn `stack many sample graphs`. |
| **B4** | 4 | →11.28 | "the eye node no longer holds one eye, but a whole bunch." | Khoanh node mắt → `bunch_card` với **3 crop mắt thật**. Tiêu đề `eye node = a bunch`. |
| **B5** | 5 | →14.64 | "Narrow eyes, round eyes, spectacled eyes." | Nhãn `narrow / round / spectacled` dưới từng crop (không đè). |
| **B6** | 6 | →18.02 | "Facing a stranger, the system searches the bunch" | Mặt lạ (mờ) + `thin_arrow` quét vào card. Nhãn `search the bunch`. |
| **B7** | 7 | →19.26 | "and elects a local expert," | Box quanh 1 crop khớp nhất + nhãn `Local Expert`. |
| **B8** | 8 | →21.40 | "the best fit for each landmark." | Hàng selected gọn + mũi tên ngắn. Nhãn `best fit for each landmark`. |
| **B9** | 9 | →24.86 | "This cross-combination yields almost limitless coverage." | Lưới tổ hợp gọn + nhãn lớn `almost limitless coverage`. |

**Tail:** `self.wait(max(0, T["duration"] - elapsed - 0.18))` để khớp 25.50s.

---

## 5. ẢNH CẦN CUNG CẤP (user thả vào `assets/`)

- ✅ (bắt buộc bản đẹp) **`assets/s8_face.png`** — mặt model chính diện (tái dùng từ S08, **cùng một người xuyên S06/S08/S09/S10** để mạch hình nhất quán). Kèm **`assets/s8_landmarks.json`** để node khớp chuẩn.
- ✅ (B0 "my face") **`assets/s9_face_other.png`** — **một người KHÁC**, chính diện, để minh hoạ "graph không khớp mọi mặt". *(Có thể tái dùng `s2_personB.jpg`.)*
- ✅ (B3 stack) **3–5 ảnh mặt người khác nhau** cho stack mẫu: **`assets/s9_sample1.png` … `s9_sample5.png`** (chính diện, ~512px). *(Có thể tái dùng bộ `s2_*`: personA/B + same_smile/frown/pose.)*
- ✅ (B4–B5, rất nên có) **3 crop MẮT thật:** **`assets/s9_eye_narrow.png`**, **`assets/s9_eye_round.png`**, **`assets/s9_eye_glasses.png`** (~256px, crop quanh 1 mắt; cái "glasses" có gọng kính). Để "bunch" trực quan đúng nghĩa narrow/round/spectacled.

**Mô tả để user chuẩn bị:** ảnh chính diện rõ; 3 crop mắt nên khác nhau rõ rệt (mắt hẹp, mắt tròn to, mắt đeo kính) để người xem thấy ngay sự đa dạng trong bunch.

Fallback: thiếu ảnh nào → dùng `face.png`/crop tạm; thiếu crop mắt → vẽ eye icon cũ. **Không** quay lại mặt vẽ tay cho graph chính. Helper kiểm tra tồn tại `base = Path(__file__).resolve().parents[1] / "assets"`.

---

## 6. KIỂM TRA & NGHIỆM THU

```bash
python3 -m py_compile video-2-ebgm/release/scene_S09_bunch_graph.py
rg -n "Text\(|font=|Paragraph|make_subtitle|[À-ỹ]" video-2-ebgm/release/scene_S09_bunch_graph.py
ffprobe -v error -show_entries format=duration -of csv=p=0 media/.../S09_BunchGraph.mp4   # |Δ| ≤ 0.3s vs 25.50
```

Checklist:
- [ ] Mặt thật + node khớp feature; bỏ mặt vẽ tay.
- [ ] Stack mẫu **gọn, đọc được** (không còn mớ đường rối).
- [ ] `eye node = a bunch` dùng **crop mắt thật**, 3 loại cách đều, nhãn không đè.
- [ ] Search → Local Expert → coverage rõ ràng, nhãn không tràn/đè; bỏ combo_lines rối.
- [ ] Mọi event đúng segment; tổng khớp 25.50s (|Δ|≤0.3s); English-only; palette `_common.py`; `-qh` OK.
