# 🤖 PROMPT cho CODEX — CẢI TIẾN Scene 16 (S16 "Conclusion")

> File: `release/scene_S16_conclusion.py` (class `S16_Conclusion`, `Scene` 2D).
> Mục tiêu: kết bài **sang hơn**, bớt đơn điệu; dùng **mặt thật + node khớp feature** cho final grid; **chuẩn nội dung**.
> **GIỮ:** `add_sound`, khung `beat_to`/`load_scene_timing`/`seg_end`, English/LaTeX, palette `_common.py`.
> **Audio = `scene_16`, duration = 24.06s** → render xong `ffprobe` cho `|Δ| ≤ 0.3s`.
> Env `vid`; kiểm tra `-pql`, bản cuối `-qh --disable_caching`.

---

## 1. VẤN ĐỀ HIỆN TẠI (cải thiện)

1. **Final grid mặt vẽ tay** (Ellipse + node rời) → nên là **mặt thật + node khớp feature** để chốt hình ảnh thương hiệu EBGM.
2. Hiệu ứng chủ yếu `FadeIn` → có thể thêm nhịp (cards build, crown nhường chỗ, grid sáng, từ khoá hiện) cho sang.
3. Giữ mạch: 3 ý → vương miện deep learning → "elastic landmarks lives on" → LOCAL/ELASTIC/GENERAL → thanks.

**Mục tiêu:** một kết bài gọn, đẹp, đầy đặn; final face-grid trên mặt thật.

---

## 2. Ý NGHĨA SCENE (giữ chuẩn — nội dung lõi)

EBGM là **bản giao hưởng 3 ý tưởng**: **local signal processing** + **wavelets** + **spatial geometry (graphs)**.
Tuy **deep learning đang đội vương miện**, **triết lý elastic landmarks vẫn sống** trong các kiến trúc face detection hiện đại — **local · elastic · general**. Cảm ơn đã xem.

(Nội dung đúng — giữ; nâng hình + nhịp.)

---

## 3. SỬA CỤ THỂ

- **3 idea cards** (local signal / wavelets / geometry): icon sạch, build có nhịp (`LaggedStart` + pop), gradient nhẹ.
- **Crown "deep learning":** vương miện gọn, sang; câu `elastic landmarks still live on` nổi bật; chuyển cảnh mượt (crown mờ → grid lên).
- **Final face-grid = mặt thật + node khớp feature** (dùng `L(u,v)` + landmark `s8_landmarks.json`), node lavender sáng dần; 3 từ khoá `LOCAL · ELASTIC · GENERAL` hiện theo nhịp, có dấu chấm phân tách, không tràn/đè.
- **Thanks:** `Thank you for watching` + `See you in the next algorithm video`; grid mờ nền phía sau (đầy đặn, không trống), nhãn rõ.
- Đường nét: bo góc & cỡ chữ nhất quán; một tiêu điểm mỗi beat; clear cụm cũ trước khi vào cụm mới.

---

## 4. STORYBOARD — map đúng segment `transcript.json` (scene_16)

Mốc lấy bằng `seg_end(T, k)`:

| Beat | seg | Mốc≈(s) | Thoại | Hình |
|---|---|---|---|---|
| **B0–B2** | 0–2 | →7.42 | "a symphony of local signal processing, wavelets, and spatial geometry / graphs." | Title + `symphony of three ideas` + 3 idea cards build có nhịp. |
| **B3–B5** | 3–5 | →16.62 | "deep learning wears the crown, but EBGM's elastic landmarks still live on..." | Crown `deep learning` → `elastic landmarks still live on`. |
| **B6** | 6 | →19.16 | "local, elastic, general." | Final face-grid (mặt thật) + `LOCAL · ELASTIC · GENERAL`. |
| **B7–B8** | 7–8 | →23.46 | "Thank you for watching. See you in the next algorithm video." | `Thank you for watching` + `See you in the next algorithm video`; grid mờ nền. |

**Tail:** `self.wait(max(0, T["duration"] - elapsed - 0.18))` để khớp 24.06s.

---

## 5. ẢNH CẦN CUNG CẤP (user thả vào `assets/`)

- ✅ **`assets/s8_face.png`** + **`assets/s8_landmarks.json`** — final face-grid (tái dùng cùng người/node, chốt nhất quán toàn video). Không cần ảnh mới.

Fallback: thiếu ảnh → grid mặt vẽ tay cũ. Helper `base = Path(__file__).resolve().parents[1] / "assets"`.

---

## 6. KIỂM TRA & NGHIỆM THU

```bash
python3 -m py_compile video-2-ebgm/release/scene_S16_conclusion.py
rg -n "Text\(|font=|Paragraph|make_subtitle|[À-ỹ]" video-2-ebgm/release/scene_S16_conclusion.py
ffprobe -v error -show_entries format=duration -of csv=p=0 media/.../S16_Conclusion.mp4   # |Δ| ≤ 0.3s vs 24.06
```

Checklist:
- [ ] Final face-grid trên **mặt thật + node khớp feature**.
- [ ] 3 idea cards / crown / từ khoá build có nhịp, sang; không tràn/đè.
- [ ] Kết bài đầy đặn (grid nền + thanks), không trống.
- [ ] Mọi event đúng segment; tổng khớp 24.06s (|Δ|≤0.3s); English-only; palette; `-qh` OK.
