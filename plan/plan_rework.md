# 🛠️ PLAN — Làm lại 16 scene EBGM ở mức SOURCE (cho Codex)

> **Mục tiêu tổng:** Bỏ cách cắt ffmpeg sai (mất frame, wait dài). Làm lại **ở mức source Manim (.py)**: chỉ cắt wait/khoảng trống, **giữ nguyên mọi ảnh minh họa**; **enhance 3D + chuyển động liên tục mượt**; **khớp thời lượng mỗi scene đúng audio tương ứng** (dựa `audio/en/transcript.json` word-level); **xoá hết phụ đề tiếng Việt, mọi nhãn/chú thích chuyển sang tiếng Anh** (KHÔNG cần phụ đề tiếng Anh — VO lo lời).

---

## 0. BỐI CẢNH & CHẨN ĐOÁN

**Codex đã làm gì (cần hiểu để revert):**
- `build_release_cut.py` cắt ở **mức video**: đọc mp4 đã render trong `media/videos/`, cắt theo mốc thời gian cứng (vd `("01", 0, 8.0)`), ghép lại bằng ffmpeg → ghi ra `media/release_cut_16_scenes/`.
- ⚠️ Cắt mù theo timestamp → **xén luôn frame minh họa đang hiển thị**, và **không thể loại riêng `self.wait()`**. Đây là nguyên nhân lỗi.
- File source `scene_*.py` **không bị sửa** (vẫn bản gốc 27–28/05). ✅
- `_common.py::make_subtitle` đã bị sửa thành trả mobject vô hình (tắt phụ đề). **Giữ nguyên trạng thái tắt này** (đúng ý: không phụ đề).
- Đã có backup renders cũ: `media/videos_backup_20260623_213811/`.
- **Không có git** trong repo.

**Nguyên tắc mới:** mọi thay đổi làm ở **source `.py`**, render lại, KHÔNG đụng ffmpeg time-slice nữa.

---

## 1. PHASE 0 — AN TOÀN & REVERT (làm trước tiên)

1. **Backup source hiện tại** (vì không có git):
   - Tạo thư mục `backups/source_pre_rework_<YYYYMMDD>/` và copy toàn bộ `scene_*.py` + `_common.py` vào đó.
2. **Cô lập (revert) cơ chế cắt ffmpeg sai** — KHÔNG xoá vĩnh viễn, chỉ chuyển vào quarantine:
   - Di chuyển `build_release_cut.py` → `backups/deprecated/build_release_cut.py`.
   - Di chuyển `media/release_cut_16_scenes/` → `backups/deprecated/release_cut_16_scenes/`.
   - Giữ nguyên `media/videos_backup_20260623_213811/` (là phao cứu hộ).
3. **Kiểm tra render gốc còn nguyên:** so `media/videos/` với `videos_backup_20260623_213811/`. Nếu khác (Codex từng re-render hỏng), khôi phục từ backup.
4. **Không revert** phần tắt phụ đề trong `_common.py` (ta muốn không phụ đề).

✅ *Hết Phase 0:* source nguyên vẹn + đã backup; pipeline cắt ffmpeg đã gỡ khỏi đường chạy.

---

## 2. PHASE 1 — QUY TẮC THỜI LƯỢNG & CẮT (cốt lõi)

### 2.1. Audio là "nhạc trưởng"
- Mỗi scene cuối **phải dài đúng bằng** file audio tương ứng trong `audio/en/scene_NN.mp3`.
- Lấy mốc chuẩn từ `audio/en/transcript.json`:
  - `scenes[i].duration` = tổng thời lượng audio scene đó (giây).
  - `scenes[i].segments[]` = mốc **câu** (`start`,`end`,`text`) → đổi beat hình theo câu.
  - `scenes[i].words[]` = mốc **từ** (`start`,`end`,`word`) → "bật" hiệu ứng đúng lúc đọc từ khóa.
- **Nhúng audio vào scene:** đầu `construct()` gọi `self.add_sound("audio/en/scene_NN.mp3")` để mp4 render ra đã có tiếng và tự đồng bộ.

### 2.2. Khớp thời lượng thế nào (KHÔNG cắt ảnh)
- **Nếu source dài hơn audio:** chỉ rút `self.wait(...)` và xoá khoảng trống chết (đoạn màn hình đứng yên không thoại). **Tuyệt đối không** xoá/rút ngắn animation đang vẽ ảnh minh họa chi tiết.
- **Nếu source ngắn hơn audio:** KHÔNG để màn hình đứng chờ. Thay vào đó **kéo dài bằng chuyển động liên tục**: camera orbit chậm, ambient rotation, drift/pulse nhẹ, vẽ chi tiết kỹ hơn — đúng tinh thần "mượt, đa dạng hiệu ứng".
- **Mục tiêu sai số:** `|render_duration − audio_duration| ≤ 0.3s`.

### 2.3. Khung dựng beat theo transcript (mẫu cho mọi scene)
```python
import json
T = json.load(open("audio/en/transcript.json"))
SC = next(s for s in T["scenes"] if s["scene"] == "scene_NN")
DUR = SC["duration"]            # tổng audio
SEG = SC["segments"]            # [{start,end,text}]
# self.add_sound("audio/en/scene_NN.mp3")
# Mỗi beat hình bắt đầu/kết thúc canh theo SEG[k].start / SEG[k].end
# run_time của animation = (mốc kết thúc beat) - (thời điểm hiện tại)
# Beat cuối: thêm self.wait(DUR - elapsed) để chốt đúng tổng.
```
> Codex nên viết 1 helper chung (vd trong `_common.py`: `load_scene_timing("scene_NN")`) để mọi scene tái dùng.

---

## 3. PHASE 2 — ENHANCE CHẤT LƯỢNG (3D + chuyển động + hiệu ứng)

### 3.1. Chuyển sang 3D
- Đổi base class các scene phù hợp: `class SceneX(ThreeDScene)` (hoặc `MovingCameraScene` khi chỉ cần pan/zoom 2D).
- **Mặt người minh họa:** hiện là silhouette 2D (VMobject). Nâng thành 3D:
  - Mặt phẳng/mặt cong 3D nhẹ, hoặc đặt landmark lên một bề mặt 3D (`Surface`) có thể xoay.
  - Cho camera `set_camera_orientation(phi=…, theta=…)` + `begin_ambient_camera_rotation(rate=…)` để xoay quanh khuôn mặt.
- **Đồ thị (image graph / bunch graph):** nâng nút + cạnh thành 3D:
  - Nút = `Sphere`/`Dot3D` phát sáng; cạnh = đường 3D; cả graph **xoay liên tục** quanh trục Y.
  - Bunch graph: các đồ thị xếp **chồng theo trục Z** (depth thật), camera lia để thấy chiều sâu chùm.
- **Bề mặt mật độ / năng lượng** (similarity landscape S7, graph similarity S10): vẽ `Surface` 3D (lòng chảo trơn vs đỉnh nhọn) — đây là điểm "wow".

### 3.2. Chuyển động liên tục & hiệu ứng "ảo ma xịn"
- Ưu tiên `always_redraw`/`ValueTracker` cho chuyển động mượt liên tục (không "pop").
- Kho hiệu ứng nên dùng đa dạng (mỗi scene chọn vài cái, tránh lặp đơn điệu):
  - Glow/halo pulsing (lavender `ACCENT_LAVENDER` cho điểm "thắng").
  - Particle/flow lines chạy dọc cạnh đồ thị; trace sáng theo đường.
  - Camera orbit / dolly chậm; depth-of-field giả bằng opacity theo z.
  - `LaggedStart` cho chuỗi xuất hiện; `TransformMatchingTex` cho công thức.
  - Wavelet/Gabor: sóng dao động thật theo thời gian (ValueTracker pha).
- **Giữ phong cách & palette `_common.py`** (nền navy, cool tone, lavender = thương hiệu EBGM). Không đổi bảng màu.

### 3.3. GIỮ NGUYÊN nội dung minh họa
- Mọi ảnh/đồ thị/công thức minh họa **phải còn đủ** (enhance, không lược). Chỉ wait/khoảng trống mới được cắt.

---

## 4. PHASE 3 — NGÔN NGỮ (English-only, không phụ đề)

1. **Xoá toàn bộ phụ đề tiếng Việt** (câu thoại dưới màn hình): giữ `make_subtitle` ở trạng thái vô hiệu; gỡ mọi block hiển thị câu thoại tiếng Việt còn sót.
2. **KHÔNG thêm phụ đề tiếng Anh** (VO đã lo lời).
3. **Nhãn/chú thích/tiêu đề trên hình → dịch sang tiếng Anh** và GIỮ (vì là phần đồ họa, không phải phụ đề):
   - Ví dụ: "Biên độ→nhận dạng" → `Amplitude → recognition`; "Chuyên gia cục bộ" → `Local Expert`; "Giai đoạn 1: Chuẩn hóa" → `Phase 1: Normalization`; nhãn trục, tên cột bảng, badge.
   - Phân biệt rõ: **subtitle (câu thoại đầy đủ) = XOÁ** · **annotation (thuật ngữ ngắn trên sơ đồ) = DỊCH SANG ANH, GIỮ**.
4. Thay `vn_tex/Text` tiếng Việt bằng text tiếng Anh; công thức `MathTex` giữ nguyên. Có thể bỏ template tiếng Việt cho text Anh (dùng font Latin Modern/`Text` thường) để render nhẹ hơn.

---

## 5. BẢNG ÁNH XẠ 16 SCENE (final ↔ source ↔ audio ↔ việc cần làm)

> `audio_dur` lấy từ `transcript.json` (giây). "Source" = file `.py` gốc cung cấp nội dung.

| Final | audio_dur | Source scene | Hành động chính | Gợi ý 3D / hiệu ứng |
|---|---|---|---|---|
| **S01** Cold open & problem | 25.2 | sc01 + sc02 | Gộp; rút wait | Title 3D depth; 2 thẻ 1:1 vs 1:N trôi trong không gian z |
| **S02** Why it's hard | 28.3 | sc03 | Rút wait | Mặt 3D xoay qua 5 trạng thái; nhãn EN |
| **S03** Pre-deep-learning ⭐ | 54.5 | **DỰNG MỚI** | Tạo scene mới khớp audio (CNN→tua ngược→IEEE PAMI 1997→tên EBGM). KHÔNG dùng sc04 | CNN 3D layers + backprop arrows; clock rewind; "paper" 3D; brain/visual-cortex glow |
| **S04** EBGM idea (3 pillars) | 35.1 | sc06 | Rút/kéo khớp | 3 trụ cột 3D dựng đứng; jet bundle xoay |
| **S05** Gabor wavelets | 34.0 | sc09 | Rút wait | Gabor kernel 3D `Surface` dao động; caption `≈ CNN first-layer filter` |
| **S06** Jet (40 coeff) | 27.7 | sc10 | Kéo dài bằng motion | 40 wavelet trên lưới 3D; "stack of discs" xoay |
| **S07** Two similarity fns | 35.3 | sc11 | Rút wait | **Surface 3D**: basin trơn vs nhiều đỉnh nhọn; bi lăn; mũi tên displacement |
| **S08** Image graph | 21.3 | sc12 | Khớp | Graph 3D xoay; nút=Sphere, cạnh phát sáng |
| **S09** Face Bunch Graph | 25.9 | sc13 | Khớp | Đồ thị xếp chồng theo trục Z; local expert bừng sáng |
| **S10** Graph similarity | 24.3 | sc14 | Khớp | Lò xo cạnh 3D; vùng phạt coral; công thức tô màu 2 số hạng |
| **S11** Elastic matching 4 bước ⭐ | 44.6 | sc15 (+sc16 1 nhãn) | Rút wait; giữ đủ 4 bước | Lưới 3D đáp lên mặt; từng nút bò về mốc; cạnh = lò xo; camera orbit |
| **S12** Recognition & rank | 21.9 | sc17 | Khớp | Gallery 3D dạng kệ; tia so khớp; bảng rank trượt |
| **S13** Data & FERET | 35.4 | sc20 + sc21 | Gộp; rút wait DÀI (sc20/21 wait ~35s) | Bar chart 3D; nhãn đúng cặp pose (98/84/57/18) |
| **S14** Cross-pose · phase · speed | 42.2 | sc22 + sc23 + sc24 | Gộp; rút wait | Đường cong góc xoay 3D; cột 1.6px vs 5.2px; sơ đồ tách extraction/matching |
| **S15** Big picture | 34.0 | sc27 + sc29 + sc31 | Gộp | 4 icon in-class 3D; mini so PCA vs EBGM; pros/cons |
| **S16** Conclusion | 21.0 | sc33 (+sc32 1 nhãn) | Khớp | Lưới mặt mờ dần; 3 keyword `LOCAL · ELASTIC · GENERAL` |

> **Lưu ý S03:** audio (54.5s) đã thu theo nội dung "pre-deep-learning" MỚI → **bắt buộc dựng scene mới** đúng nội dung đó; sc04 (3 cách tiếp cận cũ) bị loại, KHÔNG tái dùng.

---

## 6. QUY TRÌNH LÀM TỪNG SCENE (Codex tuân thủ tuần tự)

Với mỗi scene S01…S16, làm **một scene một lần**, theo vòng:
1. Đọc source `.py` tương ứng + đoạn `transcript.json` của scene đó (segments/words).
2. Áp Phase 1 (timing), Phase 2 (3D+motion), Phase 3 (English) lên source → file mới: `release/scene_SNN_<slug>.py` (giữ source gốc không đụng).
3. `self.add_sound("audio/en/scene_NN.mp3")` ở đầu.
4. Render kiểm tra nhanh: `manim -pql release/scene_SNN_*.py <Class>`.
5. **Đo thời lượng** mp4 vừa render bằng ffprobe; so với `audio_dur`. Lệch >0.3s → chỉnh run_time/wait rồi render lại.
6. Tick checklist (mục 7). Đạt mới sang scene kế.
7. Cuối cùng: dựng `release/build_full.py` nối 16 mp4 theo thứ tự S01→S16 (concat ffmpeg đơn giản, KHÔNG cắt theo timestamp).

---

## 7. CHECKLIST NGHIỆM THU (mỗi scene phải đạt hết)
- [ ] Render chạy không lỗi (`-pql` và `-pqh`).
- [ ] Thời lượng khớp audio (|Δ| ≤ 0.3s); đã `add_sound` đúng file.
- [ ] Beat hình canh theo `segments`/`words` (từ khóa bật đúng lúc đọc).
- [ ] **Không còn `self.wait()` chết** / màn hình đứng yên im lặng.
- [ ] **Mọi ảnh minh họa gốc còn đủ** (không xén nội dung).
- [ ] Có yếu tố **3D** (mặt/đồ thị/surface) + **chuyển động liên tục** mượt.
- [ ] **0 phụ đề** (cả VN & EN).
- [ ] **0 chữ tiếng Việt**; mọi nhãn/chú thích là tiếng Anh.
- [ ] Giữ palette `_common.py` (navy + cool + lavender).

---

## 8. RÀNG BUỘC (DO / DON'T)
**DO**
- Sửa ở source `.py`; render lại; đo bằng ffprobe.
- Backup trước khi sửa (không có git).
- Một scene một lần; xác nhận đạt rồi mới tiếp.

**DON'T**
- ❌ KHÔNG cắt video bằng ffmpeg time-slice (cơ chế cũ).
- ❌ KHÔNG xoá/rút animation vẽ ảnh minh họa để tiết kiệm thời gian.
- ❌ KHÔNG thêm bất kỳ phụ đề nào.
- ❌ KHÔNG để text tiếng Việt còn sót.
- ❌ KHÔNG đổi bảng màu / phong cách series.
- ❌ KHÔNG sửa file source gốc (làm bản mới trong `release/`).

---

## 9. DELIVERABLES
- `backups/source_pre_rework_<date>/` (bản gốc) + `backups/deprecated/` (pipeline cũ).
- `release/scene_S01_*.py … scene_S16_*.py` (16 scene đã rework, có audio).
- `release/scene_S03_pre_deeplearning.py` (scene mới).
- `_common.py` thêm helper `load_scene_timing()` (+ giữ subtitle tắt).
- `release/build_full.py` + `release/EBGM_EN_full.mp4` (~8:30, đã có VO).
- `release/durations_report.csv` (audio_dur vs render_dur từng scene, cột Δ).

---

## 10. MÔI TRƯỜNG
- Conda env: **`vid`** (đã có manim CE; faster-whisper đã cài).
- Audio: `audio/en/scene_01..16.mp3`; timing: `audio/en/transcript.json`.
- Render thử `-pql`, render cuối `-pqh`. Lưu ý: `Surface` 3D nặng trên CPU → giữ `resolution` vừa phải khi `-pql`.

---
*Sau khi bạn duyệt plan này, mình sẽ viết `prompt_codex.md` — hướng dẫn Codex chỉnh **từng scene** theo đúng các ràng buộc trên (kèm skeleton code timing/3D mẫu).*
