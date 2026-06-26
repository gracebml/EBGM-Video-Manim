# 🤖 PROMPT cho CODEX — Thêm INTRO + sửa S15 (Big Picture) + S16 (Conclusion)

> Ba việc độc lập. Giữ quy ước chung: English/LaTeX (`en_label`, `EN_TEX_TEMPLATE`), palette `_common.py`, `thin_arrow`/StealthTip, không `Text(...)`/`font=`/tiếng Việt. Render kiểm tra `-pql`, bản cuối `-qk` (4K, theo bộ hiện tại).

---

## VIỆC 1 — THÊM SCENE INTRO (chào hỏi + tiêu đề video)

**Tạo file mới:** `release/scene_S00_intro.py`, class `S00_Intro(Scene)` (2D).

- **KHÔNG có audio** (đây là intro im lặng) → **không gọi `add_sound`**. Thời lượng cố định bằng `self.wait`, tổng scene **≈ 6.0s**.
- Không dùng `load_scene_timing`/transcript (scene này không có trong `transcript.json`).

### Nội dung & hiệu ứng (sang, dứt khoát)
1. **Mở màn (0.0–1.2s):** nền navy; một **face-graph motif** nhỏ (mặt thật `s8_face` mờ + vài node lavender nối, dùng `L(u,v)` + `s8_landmarks.json` như các scene khác) **hiện nhanh** ở giữa, hơi glow.
2. **Tiêu đề (1.2–3.2s):** **`ELASTIC BUNCH GRAPH MATCHING`** punch-in (FadeIn + scale 0.8→1.0 + `Indicate` 1 nhịp), chữ lớn (scale ~0.8, bold), lavender/`TEXT_PRIMARY`. Một đường kẻ mảnh cyan chạy ngang dưới tiêu đề (Create).
3. **Phụ đề/chào (3.2–4.6s):** dòng nhỏ `Pattern Recognition Series · Video 2` (TEXT_MUTED, scale 0.34) và/hoặc `How a 1997 algorithm taught machines to see faces`.
   - *(Text tiêu đề/phụ đề user có thể đổi — để hằng số `TITLE`, `SUBTITLE` ở đầu construct cho dễ sửa.)*
4. **Giữ & chuyển (4.6–6.0s):** giữ ~1s rồi **fade sạch toàn bộ** (FadeOut) để nối liền mạch sang S01 (kết thúc trên nền navy trống).
- Motif mặt + node: nhẹ nhàng, không che tiêu đề; canh tiêu đề ở trên, motif phía sau mờ (opacity ≤ 0.5).

### Tích hợp pipeline (QUAN TRỌNG)
- Thêm `S00_Intro` **đầu danh sách** trong cả `render_hd.sh` và `render_uhd.sh`:
  `"scene_S00_intro.py:S00_Intro"` (hoặc `"scene_S00_intro.py S00_Intro"` đúng định dạng từng script) đặt **trước** `S01_ColdOpen`.
- Concat order: intro đứng đầu, rồi S01…S16.

---

## VIỆC 2 — SỬA S15 (`scene_S15_big_picture.py`, class `S15_BigPicture`)

Vấn đề: frame cuối **"Limits & Strengths"** vào bằng **một cú `FadeOut(old) + FadeIn(tất cả)`** ở `beat_to(seg_end(T,9), ...)` (dòng ~273–290) → mềm, khó theo dõi; **chữ heading nhỏ**.

### 2.1 Chuyển cảnh dứt khoát (thay fade mềm)
- Tách làm 2 nhịp trong ngân sách của beat cuối (giữ tổng khớp audio 35.53s — **đo lại ffprobe**):
  1. **Clear nhanh, dứt khoát** cụm PCA/EBGM cũ (`old`): `play_t(0.4, FadeOut(old, shift=DOWN*0.2))` hoặc `FadeOut` nhanh — cảm giác "gạt sạch" trước khi vào tổng kết.
  2. **Panel + tiêu đề vào dứt khoát:** `GrowFromCenter(limits_panel)` (thay FadeIn), `cons_title` `Write`/`FadeIn(scale=0.8→1.0)` + `Indicate` 1 nhịp.
  3. Hai cột reveal có nhịp: `LaggedStart` cho (`limits_lbl` → X + lim_lbl1 → X + lim_lbl2) và (`strengths_lbl` → ✓ + str_lbl1 → ✓ + str_lbl2), `lag_ratio ~0.12`.
  4. `no_training` dải mint vào cuối (`GrowFromEdge`/`FadeIn(scale)`), có `Indicate`/glow nhẹ để chốt.
- Dùng `play_t` (helper cập nhật `elapsed`) cho các nhịp tuần tự, **kết bằng `beat_to(seg_end(T,9))`** để hấp thụ phần dư. **Tổng Σ run_time ≤ ngân sách** (seg8→seg9), tránh overrun.

### 2.2 Phóng to chữ heading
- `cons_title` "Limits & Strengths": scale **0.52 → 0.66** (bold).
- `limits_lbl` "Limits" & `strengths_lbl` "Strengths": scale **0.38 → 0.52** (bold).
- Item labels giữ ~0.28–0.30 (đủ đọc, không tràn panel). Nếu phóng heading làm chật, nới `limits_panel` height một chút và canh lại y các hàng cho cân, **không đè**.

---

## VIỆC 3 — SỬA S16 (`scene_S16_conclusion.py`, class `S16_Conclusion`)

Vấn đề: frame cuối "Thank you for watching" **còn sót gương mặt** vì beat cuối chỉ `final_face_card.animate.set_opacity(0.18)` (dòng ~202–210) — `ImageMobject` ở 0.18 **vẫn hiện mờ khuôn mặt** sau chữ.

### Sửa
- Ở beat thanks (`beat_to(seg_end(T,8), ...)`): **FadeOut hẳn** mặt + graph thay vì dim:
  - `FadeOut(final_face_card)`, `FadeOut(final_graph)` (đưa về opacity 0, biến mất hẳn).
  - Với `words`/`dots`: có thể `FadeOut` hoặc dim xuống ~0.25 làm nền chữ — nhưng **khuôn mặt phải biến mất hoàn toàn**.
- Đảm bảo `thanks` + `next_video` nằm trên nền **sạch** (navy), không có ảnh mặt phía sau. Nếu muốn nền đỡ trống, để **face-graph motif rất mờ (≤0.12) KHÔNG phải ảnh mặt** — nhưng đơn giản nhất là nền navy trơn.
- Giữ tổng khớp audio 24.06s (đo lại ffprobe).

---

## RENDER LẠI & NGHIỆM THU

```bash
# compile
python3 -m py_compile release/scene_S00_intro.py release/scene_S15_big_picture.py release/scene_S16_conclusion.py
rg -n "Text\(|font=|Paragraph|make_subtitle|[À-ỹ]" release/scene_S00_intro.py release/scene_S15_big_picture.py release/scene_S16_conclusion.py

# render 4K từng scene đã đổi
manim -qk --disable_caching release/scene_S00_intro.py S00_Intro
manim -qk --disable_caching release/scene_S15_big_picture.py S15_BigPicture
manim -qk --disable_caching release/scene_S16_conclusion.py S16_Conclusion

# đo (S15 ≈ 35.53, S16 ≈ 24.06; intro ≈ 6.0 cố định)
ffprobe -v error -show_entries format=duration -of csv=p=0 <mp4>
```

Checklist:
- [ ] `S00_Intro`: intro im lặng ~6s, tiêu đề `ELASTIC BUNCH GRAPH MATCHING` + phụ đề, hiệu ứng dứt khoát, fade sạch cuối; đã thêm vào đầu `render_hd.sh` & `render_uhd.sh`.
- [ ] S15: chuyển vào "Limits & Strengths" **dứt khoát** (clear nhanh + GrowFromCenter + LaggedStart), **heading to hơn** (title 0.66, Limits/Strengths 0.52), không tràn/đè; `|Δ|≤0.3s` vs 35.53.
- [ ] S16: frame thanks **không còn khuôn mặt** (FadeOut hẳn face+graph); nền sạch; `|Δ|≤0.3s` vs 24.06.
- [ ] English-only; palette; render 4K OK.
