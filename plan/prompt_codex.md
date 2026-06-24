# 🤖 PROMPT cho CODEX — Rework 16 scene EBGM (3D · audio-synced · English-only)

> **Đọc kèm:** `plan_rework.md` (kế hoạch tổng). File này = lệnh thực thi **từng scene**, có skeleton code. Tuân thủ **đúng** ràng buộc; không tự ý đổi phong cách/màu/nội dung minh họa.

---

## 0. ROLE & MỤC TIÊU

Bạn là chuyên gia **Manim Community Edition v0.18+**. Nhiệm vụ: làm lại 16 scene video EBGM **ở mức source `.py`**, sao cho:
1. **Khớp audio:** mỗi scene render dài **đúng** file `audio/en/scene_NN.mp3` (sai số ≤ 0.3s), nhúng sẵn tiếng.
2. **Chỉ cắt wait/khoảng trống**, GIỮ NGUYÊN mọi ảnh minh họa chi tiết.
3. **Enhance 3D + chuyển động liên tục mượt** (mặt người, đồ thị, surface).
4. **English-only:** xoá hết phụ đề (VN & EN); nhãn/chú thích trên hình dịch sang tiếng Anh và giữ.

⚠️ TUYỆT ĐỐI KHÔNG dùng lại cách cắt ffmpeg theo timestamp (`build_release_cut.py`). Mọi chỉnh sửa ở source, render lại, đo bằng ffprobe.

---

## 1. MÔI TRƯỜNG & LỆNH

```bash
# env có manim CE
source /home/mlinh/miniconda3/etc/profile.d/conda.sh && conda activate vid
cd /media/mlinh/Kingston/projects/pattern-recog/video-manim/video-2-ebgm

# render thử (nhanh) / render cuối (đẹp)
manim -pql release/scene_S01_cold_open.py S01_ColdOpen
manim -pqh release/scene_S01_cold_open.py S01_ColdOpen

# đo thời lượng mp4 vừa render
ffprobe -v error -show_entries format=duration -of csv=p=0 <file.mp4>
```
- Source timing: `audio/en/transcript.json`. Audio: `audio/en/scene_NN.mp3`.
- 3D `Surface` nặng trên CPU → khi `-pql` đặt `resolution=(16,16)`; `-pqh` thì `(32,32)`.

---

## 2. PHASE 0 — BACKUP & REVERT (chạy 1 lần, trước mọi thứ)

```bash
D=$(date +%Y%m%d)
mkdir -p backups/source_pre_rework_$D backups/deprecated release
cp scene_*.py _common.py backups/source_pre_rework_$D/
git rev-parse 2>/dev/null || echo "(no git — backup thủ công ở trên)"
# cô lập pipeline cắt ffmpeg cũ (KHÔNG xoá)
mv build_release_cut.py backups/deprecated/ 2>/dev/null
mv media/release_cut_16_scenes backups/deprecated/ 2>/dev/null
# GIỮ media/videos_backup_20260623_213811/ làm phao cứu hộ
```
- KHÔNG sửa file `scene_*.py` gốc. Mọi scene mới đặt trong `release/`.
- KHÔNG bật lại phụ đề trong `_common.py` (giữ `make_subtitle` vô hiệu).

---

## 3. HELPER CHUNG — thêm vào CUỐI `_common.py`

```python
# ============================================================
# REWORK HELPERS — audio timing + English labels + 3D utils
# ============================================================
import json, os
from pathlib import Path

_TRANSCRIPT = None
def load_scene_timing(scene_key):
    """scene_key vd 'scene_01'. Trả dict {duration, segments[], words[], audio_path}."""
    global _TRANSCRIPT
    if _TRANSCRIPT is None:
        p = Path(__file__).resolve().parent / "audio" / "en" / "transcript.json"
        _TRANSCRIPT = json.load(open(p))
    sc = next(s for s in _TRANSCRIPT["scenes"] if s["scene"] == scene_key)
    sc = dict(sc)
    sc["audio_path"] = str(Path(__file__).resolve().parent / "audio" / "en" / f"{scene_key}.mp3")
    return sc

def seg_end(timing, k):
    """Mốc kết thúc câu thứ k (0-indexed); k>=len → duration."""
    segs = timing["segments"]
    return segs[k]["end"] if k < len(segs) else timing["duration"]

def en_label(text_str, color=None, scale=0.5):
    """Nhãn/chú thích NGẮN tiếng Anh trên sơ đồ (KHÔNG phải phụ đề)."""
    from manim import Text
    color = color or TEXT_PRIMARY
    return Text(text_str, font=TITLE_FONT, color=color).scale(scale)

def label3d(text_str, color=None, scale=0.5):
    """Nhãn dùng trong ThreeDScene — luôn quay mặt về camera."""
    lbl = en_label(text_str, color, scale)
    return lbl  # gọi self.add_fixed_in_frame_mobjects(lbl) trong scene 3D
```

---

## 4. SKELETON BẮT BUỘC CHO MỖI SCENE

> Mỗi scene là 1 file `release/scene_SNN_<slug>.py`, 1 class `SNN_<Name>`. Bắt buộc theo cấu trúc beat-timing dưới đây.

```python
# release/scene_S07_similarity.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manim import *
import numpy as np
from _common import *   # palette, helpers, load_scene_timing, en_label

class S07_Similarity(ThreeDScene):   # hoặc Scene/MovingCameraScene nếu không cần 3D
    SCENE_KEY = "scene_07"

    def construct(self):
        T = load_scene_timing(self.SCENE_KEY)
        self.add_sound(T["audio_path"])      # nhúng VO → mp4 có tiếng
        self.camera.background_color = BG_NAVY

        elapsed = 0.0
        def beat_to(t_target, *anims, **kw):
            """Chạy anims sao cho KẾT THÚC tại mốc t_target (giây) so với đầu scene."""
            nonlocal elapsed
            rt = max(0.2, t_target - elapsed)
            if anims:
                self.play(*anims, run_time=rt, **kw)
            else:
                self.wait(rt)
            elapsed = t_target

        # ----- Beat theo segments của transcript -----
        # seg_end(T,0) = hết câu 1, ... Canh visual đổi đúng nhịp thoại.
        beat_to(seg_end(T, 0), Create(axes3d))          # ví dụ
        beat_to(seg_end(T, 3), Create(basin_surface))   # ...
        # ... thêm beat ...

        # ----- CHỐT đúng tổng thời lượng audio -----
        if T["duration"] - elapsed > 0.05:
            self.wait(T["duration"] - elapsed)
```

**Quy tắc vàng khi đặt beat:**
- Map mỗi nhóm câu (segment) → một beat hình. Dùng `seg_end(T,k)` làm mốc.
- Từ khóa quan trọng → bật hiệu ứng đúng lúc bằng `words[]` (tra `start` của từ đó, dùng `beat_to(word_start, Indicate(...))`).
- **Không bao giờ** để `self.wait()` "chết" giữa scene khi VO vẫn đang nói — thay bằng chuyển động liên tục (orbit, pulse).
- Nếu hình hết sớm mà audio còn → thêm ambient motion (camera orbit / drift) phủ kín tới `T["duration"]`.

---

## 5. ENHANCE 3D — CÔNG THỨC CHUNG

- **Mặt người / landmark:** đặt các node lên mặt cong 3D hoặc plane 3D; `self.set_camera_orientation(phi=70*DEGREES, theta=-45*DEGREES)`, `self.begin_ambient_camera_rotation(rate=0.08)`; cuối scene `self.stop_ambient_camera_rotation()`.
- **Image/Bunch graph 3D:** node = `Sphere(radius=0.08)` hoặc `Dot3D` + glow; cạnh = `Line3D`/`ParametricFunction`. Bunch = nhiều graph lệch theo trục Z (`shift(OUT*k*0.4)`), camera lia thấy chiều sâu.
- **Similarity / energy landscape (S07, S10):** `Surface(lambda u,v: [...], resolution=(16,16))` — basin trơn vs nhiều đỉnh nhọn; thả 1 `Sphere` lăn xuống đáy.
- **Gabor (S05):** `Surface` dao động theo `ValueTracker` pha (always_redraw) để sóng "sống".
- **Hiệu ứng đa dạng (chọn 2–3/scene):** glow pulsing (lavender cho phần "thắng"), flow-lines chạy dọc cạnh, `LaggedStart`, `TransformMatchingTex` cho công thức, dolly/orbit chậm, depth fade theo z.
- **Nhãn trong 3D:** tạo bằng `en_label(...)`, gọi `self.add_fixed_in_frame_mobjects(lbl)` để nhãn không méo theo camera.

---

## 6. ENGLISH-ONLY

- Xoá mọi gọi hiển thị phụ đề/câu thoại tiếng Việt. KHÔNG thêm phụ đề tiếng Anh.
- Mọi nhãn/tiêu đề/tên cột/nhãn trục **dịch sang tiếng Anh** bằng `en_label(...)`.
- Bảng dịch dùng chung (áp nhất quán):

| VN (cũ) | EN (mới) |
|---|---|
| Xác thực 1:1 / Nhận dạng 1:N | `Verification 1:1` / `Identification 1:N` |
| Cùng một người | `Same person` |
| Biên độ → nhận dạng / Pha → định vị | `Amplitude → recognition` / `Phase → localization` |
| Khớp thô / Khớp tinh | `Coarse match` / `Fine match` |
| Chuyên gia cục bộ | `Local Expert` |
| Đồ thị khuôn mặt | `Image Graph` |
| Giai đoạn 1: Chuẩn hóa / Giai đoạn 2: Nhận diện | `Phase 1: Normalization` / `Phase 2: Recognition` |
| Thưởng (feature) / Phạt (biến dạng) | `Reward (jet match)` / `Penalty (distortion)` |
| Chính diện / Nghiêng vừa / Nghiêng hẳn | `Frontal` / `Half-profile` / `Profile` |
| Có pha / Không pha | `With phase` / `No phase` |
| Trích xuất (1 lần) / So khớp (×nhiều) | `Extraction (once)` / `Matching (×many)` |

- Công thức `MathTex` giữ nguyên (đã là ký hiệu quốc tế).

---

## 7. BẢNG LÀM VIỆC 16 SCENE (target_dur = giây, audio chuẩn)

| File mới (release/) | Class | SCENE_KEY | target_dur | Source nội dung | Trọng tâm rework |
|---|---|---|---|---|---|
| scene_S01_cold_open.py | S01_ColdOpen | scene_01 | **25.22** | sc01+sc02 | Title 3D depth; thẻ 1:1 vs **1:N** (1:N sáng lavender); rút wait |
| scene_S02_why_hard.py | S02_WhyHard | scene_02 | **28.28** | sc03 | Mặt 3D xoay qua 5 trạng thái (`Same person`); cặp `Tolerant`/`Sharp` |
| scene_S03_pre_deeplearning.py | S03_PreDL | scene_03 | **54.52** | **DỰNG MỚI** | CNN 3D layers + backprop → clock rewind → "IEEE PAMI 1997" paper → visual-cortex glow → tên EBGM. KHÔNG dùng sc04 |
| scene_S04_idea.py | S04_Idea | scene_04 | **35.11** | sc06 | 3 trụ cột 3D (Image Graph / Wavelet Jet / Bunch); 4 strengths EN |
| scene_S05_gabor.py | S05_Gabor | scene_05 | **34.04** | sc09 | Gabor kernel `Surface` dao động; `DC-free`; caption `≈ CNN first-layer filter` |
| scene_S06_jet.py | S06_Jet | scene_06 | **27.73** | sc10 | 40 wavelet lưới 3D; stack-of-discs xoay; `Amplitude`/`Phase` |
| scene_S07_similarity.py | S07_Similarity | scene_07 | **35.34** | sc11 | **Surface 3D**: basin trơn vs đỉnh nhọn; bi lăn; mũi tên displacement; `focus 1→5` |
| scene_S08_image_graph.py | S08_ImageGraph | scene_08 | **21.32** | sc12 | Graph 3D xoay; Sphere nodes; cạnh phát sáng; `node=jet`/`edge=Δx` |
| scene_S09_bunch_graph.py | S09_BunchGraph | scene_09 | **25.91** | sc13 | Đồ thị xếp chồng trục Z; `Local Expert` bừng sáng |
| scene_S10_graph_sim.py | S10_GraphSim | scene_10 | **24.33** | sc14 | Lò xo cạnh 3D; vùng `Penalty` coral; công thức 2 số hạng |
| scene_S11_elastic.py | S11_Elastic | scene_11 | **44.63** | sc15(+nhãn sc16) | Lưới 3D đáp lên mặt; 4 bước; nút bò về mốc; cạnh lò xo; orbit; `Phase 1/2` |
| scene_S12_recognition.py | S12_Recognition | scene_12 | **21.87** | sc17 | Gallery 3D kệ; tia so khớp; bảng rank trượt; `[WINNER]` |
| scene_S13_feret.py | S13_Feret | scene_13 | **35.43** | sc20+sc21 | Bar chart 3D; rút wait DÀI; nhãn ĐÚNG cặp pose (98/84/57/18) |
| scene_S14_phase_speed.py | S14_PhaseSpeed | scene_14 | **42.17** | sc22+23+24 | Đường cong góc xoay 3D; `1.6px` vs `5.2px`; tách `Extraction`/`Matching` `~1000×` |
| scene_S15_big_picture.py | S15_BigPicture | scene_15 | **33.99** | sc27+29+31 | 4 icon in-class 3D; EBGM vs PCA; pros/cons |
| scene_S16_conclusion.py | S16_Conclusion | scene_16 | **20.99** | sc33(+nhãn sc32) | Lưới mặt mờ dần; `LOCAL · ELASTIC · GENERAL` |

> **S13 — sửa lỗi số liệu:** nhãn đúng cặp pose: `Frontal 98%`, `Profile 84%`, `Half-profile R/L 57%`, `Half-profile vs Frontal 18%`. KHÔNG gán 57% cho cross-pose.
> **S03 — dựng mới hoàn toàn** theo storyboard pre-deep-learning (xem `kich_ban_ebgm.md`/`script_ebgm_en.md` S3 để bám VO 54.5s).

---

## 8. QUY TRÌNH (một scene một lần — KHÔNG nhảy bước)

Lặp cho S01 → S16:
1. Mở source `.py` tương ứng + đọc `transcript.json` đoạn scene đó.
2. Tạo `release/scene_SNN_*.py` theo skeleton mục 4: áp 3D (mục 5) + English (mục 6) + giữ đủ ảnh minh họa.
3. `manim -pql ...` render thử.
4. `ffprobe` đo duration; so `target_dur`. Lệch >0.3s → chỉnh beat/run_time → render lại tới khi đạt.
5. Soát checklist mục 9. Đạt hết → sang scene kế. **Báo cáo ngắn** (duration đo được, Δ, ghi chú) rồi mới tiếp.
6. Sau S16: tạo `release/build_full.py` nối 16 mp4 (concat ffmpeg, KHÔNG cắt timestamp) → `release/EBGM_EN_full.mp4`; và `release/durations_report.csv` (scene, target_dur, render_dur, Δ).

`build_full.py` (concat đơn giản):
```python
# duyệt release/*.mp4 theo thứ tự S01..S16, ghi concat list, gọi:
# ffmpeg -f concat -safe 0 -i list.txt -c copy release/EBGM_EN_full.mp4
```

---

## 9. CHECKLIST NGHIỆM THU (mỗi scene)
- [ ] Render OK (`-pql` và `-pqh`), không lỗi LaTeX/3D.
- [ ] `add_sound` đúng file; |render_dur − target_dur| ≤ 0.3s.
- [ ] Beat hình canh theo segments; từ khóa bật theo words.
- [ ] Không còn `self.wait()` chết / màn hình đứng im khi đang có thoại.
- [ ] Mọi ảnh minh họa gốc còn đủ (chỉ cắt wait, không cắt nội dung).
- [ ] Có 3D + chuyển động liên tục mượt; ≥2 loại hiệu ứng.
- [ ] 0 phụ đề (VN & EN); 0 chữ tiếng Việt; nhãn đều tiếng Anh.
- [ ] Palette `_common.py` giữ nguyên (navy + cool + lavender).

---

## 10. DO / DON'T
**DO:** sửa ở `release/`; backup trước; render+ffprobe mỗi scene; một scene một lần; báo cáo từng scene.
**DON'T:** ❌ ffmpeg time-slice · ❌ xén animation minh họa · ❌ thêm phụ đề · ❌ để text tiếng Việt · ❌ đổi màu/phong cách · ❌ sửa file source gốc.

---
## 11. BẮT ĐẦU
Thực hiện **Phase 0** (mục 2) + thêm helper (mục 3) trước. Sau đó làm **S01**, render, đo, báo cáo, chờ pass rồi tiếp S02… đến S16, cuối cùng dựng full + report.
