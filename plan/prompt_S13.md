# 🤖 PROMPT cho CODEX — CẢI TIẾN Scene 13 (S13 "FERET Reality Check")

> File: `release/scene_S13_feret.py` (class `S13_Feret`, `Scene` 2D).
> Mục tiêu: design **sang hơn**, **chuẩn nội dung**; (tuỳ chọn) dùng **thumbnail pose thật** thay silhouette vẽ tay; đảm bảo **không tràn/đè nhãn**.
> **GIỮ:** `add_sound`, khung `beat_to`/`load_scene_timing`/`seg_end`, English/LaTeX, palette `_common.py`.
> **Audio = `scene_13`, duration = 36.87s** → render xong `ffprobe` cho `|Δ| ≤ 0.3s`.
> Env `vid`; kiểm tra `-pql`, bản cuối `-qh --disable_caching`.

---

## 1. VẤN ĐỀ HIỆN TẠI (cải thiện)

1. **Pose icon vẽ tay** (`silhouette` frontal/half/profile) hơi thô; có thể nâng bằng **thumbnail pose thật** (đồng bộ với S04/S09).
2. Cần soát **không tràn mép / không đè**: hàng kết quả (icon + name + sub + bar + value), `warning "large pose gap"` + `cliff` quanh row 4, và 2 hộp tổng kết `king/achilles` ở đáy.
3. STT cần sửa nhãn: **"Ferret" → `FERET`** (giữ đúng `FERET` trong mọi label).

**Mục tiêu:** bảng kết quả Rank-1 sạch, dễ đọc; cú "rơi vực" ở cross-pose 18% gây ấn tượng; kết luận King ↔ Achilles rõ.

---

## 2. Ý NGHĨA SCENE (giữ chuẩn — nội dung lõi)

- Lý thuyết đẹp, nhưng **thực tế thế nào?** → bài test **U.S. Tough FERET**, mỗi người **đúng 1 ảnh** trong gallery.
- Kết quả **Rank-1**:
  - Same **frontal**: **98%**
  - Same **profile** (mirror trái–phải): **84%**
  - Same **half-profile**: **57%**
  - Gallery **frontal** vs probe **xoay góc** (cross-pose): **rơi mạnh xuống 18%**
- Kết luận: EBGM **vua** xử lý **biểu cảm + ánh sáng**, nhưng **xoay 3D lớn là gót chân Achilles**.

(Nội dung đúng — giữ; nâng hình + soát overlap.)

---

## 3. SỬA CỤ THỂ

### 3.1 (Tuỳ chọn, khuyến nghị) Pose icon = thumbnail thật
- Thay `silhouette` bằng **crop pose thật** nhỏ trong khung bo góc: `frontal / half-profile / profile`. Mỗi hàng kết quả minh hoạ cặp pose (gallery vs probe) bằng 2 thumbnail nhỏ → trực quan "same frontal", "cross-pose mismatch".
- Nếu không có ảnh pose → giữ silhouette nhưng nét mảnh, đồng bộ tông.

### 3.2 Bảng Rank-1 sạch, không tràn
- 4 hàng cách đều; mỗi hàng: **[pose icon(s)] · name+sub · thanh bar · value%** canh cột thẳng hàng, không đè.
- Bar nền + bar giá trị cùng baseline; `value%` đặt **sau bar, trong khung** (đừng để x quá lớn tràn mép).
- `warning "large pose gap"` + `cliff` (đường gãy + mũi tên xuống) đặt **gọn cạnh row 4**, không tràn mép phải, không đè value.

### 3.3 Cú "rơi vực" cross-pose
- Row 4 (18%, coral) nhấn mạnh: bar ngắn + vùng cảnh báo + mũi tên `cliff` rơi xuống → cảm giác tụt mạnh từ 57% xuống 18%.

### 3.4 Kết luận King ↔ Achilles
- 2 hộp đáy cân đối, có gap: `strong: expression + lighting` (mint) ↔ `weak: large 3D rotation` (coral). Không đè hàng kết quả phía trên.

### 3.5 Đường nét "sang hơn"
- Bo góc nhất quán, bar gradient nhẹ, nhãn cùng hệ cỡ chữ; mũi tên StealthTip; một tiêu điểm mỗi beat (các hàng hiện lần lượt theo số liệu được đọc).

---

## 4. STORYBOARD — map đúng segment `transcript.json` (scene_13)

Mốc lấy bằng `seg_end(T, k)`:

| Beat | seg | Mốc≈(s) | Thoại | Hình |
|---|---|---|---|---|
| **B0** | 0 | →2.10 | "Beautiful theory, but how about reality?" | Title `FERET Reality Check` + câu hỏi. |
| **B1–B2** | 1–2 | →9.72 | "U.S. Tough FERET... exactly one image per person." | Thẻ `U.S. Tough FERET` + `one stored image per person` + dãy gallery 1-ảnh. |
| **B3** | 3 | →11.16 | "The results?" | `Rank-1 results` + trục. |
| **B4** | 4 | →14.24 | "Same frontal pose, 98%." | Row Frontal **98%** (mint). |
| **B5** | 5 | →19.60 | "Same profile pose, mirrored, 84%." | Row Profile **84%** (cyan). |
| **B6** | 6 | →22.48 | "Same half-profile angle, 57%." | Row Half-profile **57%** (lavender). |
| **B7–B8** | 7–8 | →28.10 | "frontal gallery vs angled probe... drops to 18%." | Row cross-pose **18%** (coral) + `cliff` + `large pose gap`. |
| **B9–B10** | 9–10 | →36.38 | "king at expression/lighting, but large 3D rotation is its Achilles heel." | 2 hộp `strong: expression + lighting` ↔ `weak: large 3D rotation`. |

**Tail:** `self.wait(max(0, T["duration"] - elapsed - 0.18))` để khớp 36.87s.

---

## 5. ẢNH CẦN CUNG CẤP (user thả vào `assets/`) — TUỲ CHỌN

- (tuỳ chọn) **3 pose thật của cùng một người:** **`assets/s13_frontal.png`**, **`assets/s13_half.png`**, **`assets/s13_profile.png`** (~256–512px). *(Có thể tái dùng `s4_pose_frontal/half/profile` nếu đã cấp cho S04.)*
- Nếu không cấp → giữ silhouette vẽ tay (đã đủ rõ cho scene dạng biểu đồ).

**Mô tả:** ảnh cùng người ở 3 góc (chính diện / nghiêng 3/4 / nghiêng hẳn) để minh hoạ rõ "same pose vs cross-pose".

Fallback: thiếu ảnh → silhouette. Helper `base = Path(__file__).resolve().parents[1] / "assets"`.

---

## 6. KIỂM TRA & NGHIỆM THU

```bash
python3 -m py_compile video-2-ebgm/release/scene_S13_feret.py
rg -n "Text\(|font=|Paragraph|make_subtitle|[À-ỹ]" video-2-ebgm/release/scene_S13_feret.py
rg -n "[Ff]erret" video-2-ebgm/release/scene_S13_feret.py    # phải rỗng (chỉ dùng FERET)
ffprobe -v error -show_entries format=duration -of csv=p=0 media/.../S13_Feret.mp4   # |Δ| ≤ 0.3s vs 36.87
```

Checklist:
- [ ] Bảng Rank-1 thẳng cột, **không tràn/đè**; `cliff`/`warning` gọn cạnh row 4.
- [ ] Cú rơi 57%→18% gây ấn tượng; King ↔ Achilles rõ, có gap.
- [ ] (nếu có ảnh) pose icon = thumbnail thật; nhãn `FERET` đúng (không "Ferret").
- [ ] Mọi event đúng segment; tổng khớp 36.87s (|Δ|≤0.3s); English-only; palette; `-qh` OK.
