
# PHẦN I — LUẬT CHUNG

## 0. MỤC TIÊU
Làm lại 16 scene **ở mức source `.py`** sao cho:
1. **Khớp audio:** mỗi scene dài đúng `audio/en/scene_NN.mp3` (|Δ| ≤ 0.3s), nhúng `self.add_sound(...)`.
2. **Chỉ cắt wait/khoảng trống**, GIỮ NGUYÊN mọi ảnh minh họa.
3. **Enhance 3D + chuyển động liên tục mượt.**
4. **English-only**, KHÔNG phụ đề; nhãn/chú thích trên hình bằng tiếng Anh.
5. **Kiểu chữ LaTeX thuần** (xem mục 4) — mọi text hiển thị render qua LaTeX (Latin Modern), KHÔNG dùng `Text(font=...)`.
6. **Mỗi hiệu ứng phải CÓ Ý NGHĨA, bám câu thoại đang đọc. KHÔNG dày đặc/chồng lấp** — mỗi beat một tiêu điểm; cái cũ mờ/đẩy đi trước khi cái mới vào.

⚠️ TUYỆT ĐỐI KHÔNG cắt video bằng ffmpeg time-slice (`build_release_cut.py` cũ). Sửa source → render → đo ffprobe.

## 1. MÔI TRƯỜNG & LỆNH
```bash
source /home/mlinh/miniconda3/etc/profile.d/conda.sh && conda activate vid
cd /media/mlinh/Kingston/projects/pattern-recog/video-manim/video-2-ebgm
manim -pql release/scene_SNN_*.py <Class>      # render thử
manim -pqh release/scene_SNN_*.py <Class>      # render cuối
ffprobe -v error -show_entries format=duration -of csv=p=0 <file.mp4>   # đo
```
- Timing: `audio/en/transcript.json`. Audio: `audio/en/scene_NN.mp3`.
- `Surface` 3D nặng CPU → `resolution=(16,16)` khi `-pql`, `(32,32)` khi `-pqh`.

## 2. PHASE 0 — BACKUP & REVERT (chạy 1 lần)
```bash
D=$(date +%Y%m%d); mkdir -p backups/source_pre_rework_$D backups/deprecated release
cp scene_*.py _common.py backups/source_pre_rework_$D/
mv build_release_cut.py backups/deprecated/ 2>/dev/null
mv media/release_cut_16_scenes backups/deprecated/ 2>/dev/null
# GIỮ media/videos_backup_20260623_213811/. KHÔNG sửa scene_*.py gốc; làm bản mới trong release/.
```

## 3. HELPER CHUNG — thêm vào CUỐI `_common.py`
```python
import json
from pathlib import Path

# ---- audio timing ----
_TRANSCRIPT = None
def load_scene_timing(scene_key):           # scene_key vd 'scene_01'
    global _TRANSCRIPT
    if _TRANSCRIPT is None:
        p = Path(__file__).resolve().parent / "audio" / "en" / "transcript.json"
        _TRANSCRIPT = json.load(open(p))
    sc = dict(next(s for s in _TRANSCRIPT["scenes"] if s["scene"] == scene_key))
    sc["audio_path"] = str(Path(__file__).resolve().parent / "audio" / "en" / f"{scene_key}.mp3")
    return sc

def seg_end(timing, k):
    segs = timing["segments"]
    return segs[k]["end"] if k < len(segs) else timing["duration"]

def word_start(timing, substr):
    """Mốc bắt đầu của từ chứa substr (lowercase match) — để bật hiệu ứng đúng lúc đọc."""
    for w in timing["words"]:
        if substr.lower() in w["word"].lower():
            return w["start"]
    return None

# ---- ảnh mặt thật ----
FACE_PATH = str(Path(__file__).resolve().parent.parent / "assets" / "face.png")  # video-manim/assets/face.png
```

## 4. ⭐ QUY TẮC KIỂU CHỮ LATEX THUẦN (BẮT BUỘC)
Mọi text hiển thị **render qua LaTeX, font Latin Modern** — KHÔNG dùng `Text(...)`/`SUBTITLE_FONT`/`MONO_FONT`/`Paragraph`.
- Dùng helper có sẵn trong `_common.py`: `vn_tex(...)` / `vn_tex_bold(...)` / `vn_tex_italic(...)` / `vn_tex_mono(...)` cho chữ; `vn_math(...)`/`MathTex(...)` cho công thức.
- Thêm template English (để default language = english) và helper nhãn vào CUỐI `_common.py`:
```python
EN_TEX_TEMPLATE = TexTemplate(
    tex_compiler="xelatex", output_format=".xdv",
    documentclass=r"\documentclass[preview]{standalone}",
    preamble=r"""
\usepackage{fontspec}
\usepackage{amsmath}\usepackage{amssymb}\usepackage{amsfonts}\usepackage{mathtools}
\usepackage{unicode-math}
\setmainfont{Latin Modern Roman}\setsansfont{Latin Modern Sans}\setmonofont{Latin Modern Mono}
\setmathfont{Latin Modern Math}
""")

def en_label(text_str, color=None, scale=0.5, bold=False):
    """Nhãn/chú thích NGẮN tiếng Anh trên sơ đồ — LaTeX Latin Modern. KHÔNG phải phụ đề."""
    color = color or TEXT_PRIMARY
    body = (r"\textbf{%s}" % text_str) if bold else text_str
    return Tex(body, tex_template=EN_TEX_TEMPLATE, color=color).scale(scale)
```
- Trong `ThreeDScene`, nhãn dùng `en_label(...)` rồi `self.add_fixed_in_frame_mobjects(lbl)` để chữ không méo theo camera.
- Ký tự đặc biệt LaTeX: escape đúng (`%`→`\%`, `×`→`$\times$` hoặc `\(\times\)`, `→`→`$\to$`, `°`→`$^\circ$`, `&`→`\&`, `λ`→`$\lambda$`).
- **Quét bỏ** mọi `Text(`, `font=SUBTITLE_FONT/MONO_FONT/TITLE_FONT` còn sót trong scene đang làm; thay bằng LaTeX helper.

## 5. SKELETON BẮT BUỘC (mỗi scene)
```python
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from manim import *
import numpy as np
from _common import *

class SNN_Name(ThreeDScene):      # hoặc Scene / MovingCameraScene
    SCENE_KEY = "scene_NN"
    def construct(self):
        T = load_scene_timing(self.SCENE_KEY)
        self.add_sound(T["audio_path"])
        self.camera.background_color = BG_NAVY
        elapsed = 0.0
        def beat_to(t, *anims, **kw):
            nonlocal elapsed
            rt = max(0.2, t - elapsed)
            (self.play(*anims, run_time=rt, **kw) if anims else self.wait(rt))
            elapsed = t
        # ... beat_to(seg_end(T,k), <anim>) theo bảng storyboard ...
        if T["duration"] - elapsed > 0.05:
            self.wait(T["duration"] - elapsed)   # chốt đúng tổng audio
```
Quy tắc beat: map mỗi nhóm câu (segment) → 1 beat; từ khóa → bật bằng `word_start`; KHÔNG `wait` chết khi đang có thoại (thay bằng orbit/pulse liên tục); hình hết sớm → ambient motion phủ tới `T["duration"]`.

## 6. ENHANCE 3D (kho dùng chung)
- Mặt/landmark trên mặt cong/plane 3D; camera `set_camera_orientation` + `begin_ambient_camera_rotation(rate≈0.08)` → `stop_ambient_camera_rotation()` cuối.
- Graph 3D: node=`Sphere`/`Dot3D`+glow, cạnh=`Line3D`. Bunch = nhiều graph lệch trục Z (`shift(OUT*k*0.4)`).
- Landscape (S07,S10): `Surface(...)` basin trơn vs đỉnh nhọn; thả `Sphere` lăn.
- Gabor (S05): `Surface` dao động theo `ValueTracker` (always_redraw).
- Hiệu ứng (chọn 2–3/scene, đa dạng): glow pulsing (lavender cho "thắng"), flow-lines dọc cạnh, `LaggedStart`, `TransformMatchingTex`, dolly/orbit chậm, depth-fade theo z. GIỮ palette `_common.py`.

## 7. ENGLISH-ONLY
- Xoá mọi phụ đề/câu thoại VN; KHÔNG thêm phụ đề EN.
- Nhãn/tiêu đề/tên cột/nhãn trục → tiếng Anh qua `en_label`. Bảng dịch:
  Verification 1:1 / Identification 1:N · Same person · Amplitude→recognition / Phase→localization · Coarse / Fine · Local Expert · Image Graph · Phase 1: Normalization / Phase 2: Recognition · Reward (jet match) / Penalty (distortion) · Frontal / Half-profile / Profile · With phase / No phase · Extraction (once) / Matching (×many).

## 8. WORKFLOW (một scene một lần)
Phase 0 + helper (mục 3,4) trước. Rồi S01→S16: tạo `release/scene_SNN_*.py` → `-pql` → ffprobe đo Δ → soát checklist → **báo cáo (render_dur, Δ, ghi chú) rồi DỪNG** chờ duyệt. Cuối: `release/build_full.py` concat 16 mp4 (KHÔNG time-slice) → `release/EBGM_EN_full.mp4` + `release/durations_report.csv`.

## 9. CHECKLIST (mỗi scene)
- [ ] Render OK; `add_sound` đúng; |render_dur − target| ≤ 0.3s.
- [ ] Beat khớp segment; từ khóa bật đúng lúc; không `wait` chết.
- [ ] Mọi ảnh minh họa gốc còn đủ (chỉ cắt wait).
- [ ] 3D + chuyển động liên tục; ≥2 loại hiệu ứng; KHÔNG chồng lấp.
- [ ] **0 phụ đề; 0 chữ VN; mọi text qua LaTeX Latin Modern (không `Text()`).**
- [ ] Palette giữ nguyên.

## 10. DO / DON'T
DO: sửa ở `release/`; backup trước; render+ffprobe; một scene/lần; báo cáo.
DON'T: ❌ ffmpeg time-slice · ❌ xén animation minh họa · ❌ thêm phụ đề · ❌ text VN · ❌ `Text(font=...)` (phải LaTeX) · ❌ đổi màu/phong cách · ❌ sửa source gốc.

---

# PHẦN II — STORYBOARD 16 SCENE

> ⚠️ **GIỌNG ĐÃ CHỐT: Jessica (ElevenLabs).** `audio/en/scene_NN.mp3` + `audio/en/transcript.json` đã là bản Jessica (tổng **8:54**).
> Các con số **mốc giây / target_dur trong bảng storyboard dưới đây là CHỈ DẪN (theo bản trước)** — KHÔNG hardcode. CODE **bắt buộc** đọc mốc thật từ `transcript.json` qua `load_scene_timing()` / `seg_end()` / `word_start()`. Số segment một số scene đã đổi, nên map beat theo segment THỰC của Jessica.
>
> **Target_dur thực tế (Jessica) — dùng để kiểm tra |Δ|≤0.3s:**
> S01 25.73 · S02 29.21 · S03 57.21 · S04 35.85 · S05 36.55 · S06 28.56 · S07 36.55 · S08 23.64 · S09 25.50 · S10 26.15 · S11 46.39 · S12 22.38 · S13 36.87 · S14 44.44 · S15 35.53 · S16 24.06

> Mỗi scene: **target_dur**, base class, bảng beat (mốc giây từ transcript), ghi chú chống chồng lấp. Hiệu ứng phải minh họa đúng câu.

---

## 🎬 S01 — COLD OPEN & PROBLEM · 25.22s · MovingCameraScene
| Beat | Mốc | Thoại | Hình (ý nghĩa) |
|---|---|---|---|
| B0 | 0.00–4.78 | "glance at someone... brain recognises them in a tenth of a second" | Cảnh phố (chân trời + nhà mờ); **2 người** lướt qua nhau; tại từ *recognises* (~3.5s) đầu người A bật **vòng sáng nhận ra** + tia nhìn A→B. Tối giản 2D. |
| B1 | 5.32–7.82 | "how does a computer recognise a face?" | **Zoom** vào mặt B → **cross-dissolve sang `face.png` thật** (mượt, không pop). |
| B2 | (trong 5.3–8.3) | (teaser) | Vài **landmark dot thưa/mờ** (mắt/mũi/khóe miệng) + cạnh mảnh trên mặt thật. **Tan trước B3.** |
| B3 | 8.32–10.16 | "two branches" | Mặt thu nhỏ giữa-trên; tách 2 nhánh. |
| B4 | 11.02–14.92 | "Verification 1:1 — owner of this phone?" | Nhánh trái: thẻ `Verification 1:1` + icon điện thoại mở khoá. |
| B5 | 15.42–20.54 | "Identification 1:N — who among millions?" | Nhánh phải: thẻ `Identification 1:N` + gallery nhiều mặt nhỏ. |
| B6 | 20.84–24.70 | "tackle the harder branch. 1:N" | Thẻ `1:N` sáng lavender + glow; thẻ `1:1` mờ. Chốt. |
*Chống chồng lấp:* teaser tan trước B3; B4 giữ tĩnh/mờ khi B5 vào.

## 🎬 S02 — WHY IT'S HARD · 28.28s · ThreeDScene
| Beat | Mốc | Thoại | Hình |
|---|---|---|---|
| B0 | 0.00–1.84 | "What troubles AI the most?" | Dấu `?` + mặt 3D mờ. |
| B1 | 1.84–3.92 | "Not the difference between two people" | 2 mặt KHÁC người cạnh nhau → mờ đi (không phải vấn đề). |
| B2 | 3.92–8.30 | "same person can look like two different people" | **1 mặt 3D** xoay/biến đổi → trông như 2 người; nhãn `Same person`. |
| B3 | 8.30–11.62 | "smile, frown, light from below" | Áp biểu cảm + ánh sáng dưới lên mặt 3D. |
| B4 | 11.62–14.06 | "pixel matrix changes entirely" | Lưới pixel dưới mặt **đổi giá trị toàn bộ** (coral). |
| B5 | 14.06–16.82 | "intra-class variance" | Nhãn `Intra-class variance`. |
| B6 | 16.82–19.90 | "resolve this paradox" | Cán cân/scale (paradox). |
| B7 | 19.90–23.44 | "tolerant enough to forgive deformations" | Panel `Tolerant` (mint). |
| B8 | 23.44–27.84 | "sharp enough to distinguish tiniest details" | Panel `Sharp` (cyan). Chốt. |
*Chống chồng lấp:* 2 mặt khác người (B1) mờ trước khi vào "same person" (B2).

## 🎬 S03 — PRE-DEEP-LEARNING ⭐ · 54.52s · ThreeDScene (DỰNG MỚI)
| Beat | Mốc | Thoại | Hình |
|---|---|---|---|
| B0 | 0.00–4.08 | "facing... what's our first instinct?" | Câu hỏi `Modern instinct?` |
| B1 | 4.08–11.06 | "Build a CNN... millions of images... backprop" | **CNN 3D layers** + mũi tên `Backprop` ngược + `millions of images` + `Loss ↓` (coral/teal). |
| B2 | 11.06–17.48 | "rewind to 1997, no GPUs, no datasets" | Đồng hồ **quay ngược**; CNN mờ/co; thẻ `No GPU`, `No big data`, dấu `1997`. |
| B3 | 17.48–23.08 | "recognizing a face... impossible if you compared pixels" | Mặt đổi sáng/biểu cảm → so pixel **thất bại** (✗ coral). |
| B4 | 23.08–27.10 | "solve this geometric variance problem?" | Nhãn câu hỏi `Geometric variance?` |
| B5 | 27.10–32.06 | "pure mathematics and signal processing" | `Pure math + signal processing` (không deep learning). |
| B6 | 32.06–40.56 | "1997, published in IEEE PAMI... unusual idea" | **Bìa paper** đóng dấu `IEEE PAMI · 1997`. |
| B7 | 40.56–44.36 | "see a face the way our visual cortex does" | **Vỏ não thị giác** glow (não + tia). |
| B8 | 44.36–47.70 | "Elastic Bunch Graph Matching" | Tên `ELASTIC BUNCH GRAPH MATCHING` lớn (lavender glow). |
| B9 | 47.70–52.56 | "ranked among the very best in FERET blind tests 1990s" | Badge `FERET · top-ranked (1990s)`. |
| B10 | 52.56–54.16 | "Today, we dissect it." | Chuyển tiếp. |
*Lưu ý:* STT "ferret"→**FERET**. KHÔNG dùng nội dung sc04. *Chống chồng lấp:* CNN (B1) phải mờ trước khi vào 1997 (B2).

## 🎬 S04 — THREE PILLARS · 35.11s · ThreeDScene
| Beat | Mốc | Thoại | Hình |
|---|---|---|---|
| B0 | 0.00–7.32 | "three pillars, unlike pixels or PCA" | Tiêu đề `Three Pillars`; note nhỏ `unlike pixels / PCA`. |
| B1 | 7.32–12.68 | "graph connecting landmark points" | **Trụ 1** dựng đứng: `Image Graph` (đồ thị landmark). |
| B2 | 12.68–20.96 | "wavelet jet, texture DNA of that patch" | **Trụ 2**: `Wavelet Jet`; nhãn `texture DNA`. |
| B3 | 20.96–26.00 | "stack many sample graphs into a face-bunch graph" | **Trụ 3**: `Face Bunch Graph` (xếp chồng). |
| B4 | 26.00–34.54 | "robust to lighting, < 100 images, astonishing accuracy" | 3 strengths: `Robust to light`, `< 100 images`, `High accuracy`. |
*Chống chồng lấp:* 3 trụ dựng lần lượt, không hiện cùng lúc khi đang giải thích từng cái.

## 🎬 S05 — GABOR WAVELETS · 34.04s · ThreeDScene
| Beat | Mốc | Thoại | Hình |
|---|---|---|---|
| B0 | 0.00–4.22 | "how does the AI see a single point?" | Mặt nhỏ góc; **zoom 1 điểm** (khóe mắt) + patch nhỏ. |
| B1 | 4.22–9.50 | "instead of pixels... borrowed from biology" | Lưới pixel **nhấp nháy** (coral) → gạch bỏ; icon sinh học mờ. |
| B2 | 9.50–15.48 | "sine wave trapped inside a Gaussian envelope" | **Dựng kernel:** sine (cyan) × Gaussian (teal) = Gabor (`Surface` 3D); `MathTex` ψ rút gọn. |
| B3 | 15.48–21.68 | "filter... one orientation and frequency" | Kernel **xoay hướng** + đổi tần số (ValueTracker); áp lên patch. |
| B4 | 21.68–26.22 | "cancels background light. DC-free" | Đổi sáng nền → đáp ứng **không đổi**; nhãn `DC-free` (mint). |
| B5 | 26.22–33.64 | "like first layers of a CNN... visual cortex" | 3 ô `CNN first-layer filter` song song; vỏ não glow. Chốt. |
*Chống chồng lấp:* lưới pixel tan trước khi dựng kernel; CNN filters chỉ ở cuối.

## 🎬 S06 — JET (40 COEFFICIENTS) · 27.73s · ThreeDScene
| Beat | Mốc | Thoại | Hình |
|---|---|---|---|
| B0 | 0.00–5.42 | "bank of 40 Gabor wavelets, 5 freq × 8 orient" | Lưới **5×8 = 40** wavelet (3D); nhãn `5 freq × 8 orient = 40`. |
| B1 | 5.42–10.40 | "at a single point → 40 complex numbers" | 40 wavelet **hội tụ** vào 1 điểm (khóe mắt) → 40 số phức. |
| B2 | 10.40–12.50 | "that bundle is called a jet" | Gộp thành **stack-of-discs** = `Jet`. |
| B3 | 12.50–16.36 | "unique barcode of that eye corner" | Ẩn dụ `barcode`. |
| B4 | 16.36–20.40 | "two weapons" | Tách mỗi phần tử → 2 nhánh. |
| B5 | 20.40–23.36 | "amplitude → what shape" | `Amplitude → shape`. |
| B6 | 23.36–27.32 | "phase → which coordinate" | `Phase → coordinate`. Chốt. |

## 🎬 S07 — TWO SIMILARITY FUNCTIONS · 35.34s · ThreeDScene
| Beat | Mốc | Thoại | Hình |
|---|---|---|---|
| B0 | 0.00–2.80 | "how does the machine know they match?" | 2 jet + `?`. |
| B1 | 2.80–7.04 | "pairs two similarity functions" | 2 panel: trái `Sₐ`, phải `S_φ` (mới tiêu đề). |
| B2 | 7.04–11.06 | "first compares only amplitude" | Panel trái sáng; `MathTex` Sₐ; pha gạch bỏ. |
| B3 | 11.06–14.54 | "smooth basin, a wide attractor" | **Surface basin** trơn rộng. |
| B4 | 14.54–19.18 | "catch signal from afar and slide toward the eye" | Thả `Sphere` lăn từ rìa xuống đáy. |
| B5 | 19.18–20.88 | "coarse step" | Nhãn `Coarse`. |
| B6 | 20.88–24.20 | "second function with phase kicks in" | Sang panel phải; `MathTex` S_φ. |
| B7 | 24.20–30.72 | "razor sharp... sub-pixel accuracy" | **Surface đỉnh nhọn**; zoom đỉnh; nhãn `sub-pixel`. |
| B8 | 30.72–34.94 | "points the way... how far to move the jet" | Mũi tên displacement (lavender) + `focus 1→5`. Chốt. |
*Chống chồng lấp:* chỉ 1 Surface hiển thị tại 1 thời điểm (basin mờ trước khi surface pha lên).

## 🎬 S08 — IMAGE GRAPH · 21.32s · ThreeDScene
| Beat | Mốc | Thoại | Hình |
|---|---|---|---|
| B0 | 0.00–6.92 | "sprinkle jets onto landmarks... image graph" | Jet đặt lên mắt/mũi/miệng → nối thành graph 3D (xoay); nhãn `Image Graph`. |
| B1 | 6.92–12.82 | "nodes hold the jet, edges hold geometric distances" | Highlight `node = jet`, `edge = Δx (distance)`. |
| B2 | 12.82–20.56 | "separates skin surface from bone structure" | Tách `skin surface` (jet) vs `bone structure` (cạnh) xử lý độc lập. |

## 🎬 S09 — FACE BUNCH GRAPH · 25.91s · ThreeDScene
| Beat | Mốc | Thoại | Hình |
|---|---|---|---|
| B0 | 0.00–2.54 | "your graph can't perfectly fit my face" | Graph 1 người dán lệch lên mặt khác (coral). |
| B1 | 2.54–5.26 | "the face bunch graph" | Nhãn `Face Bunch Graph`. |
| B2 | 5.26–11.06 | "stacking dozens... eye node → a whole bunch" | Nhiều graph **xếp chồng trục Z**; phóng vào nút mắt → bunch. |
| B3 | 11.06–14.96 | "narrow, round, bespectacled eyes" | Ví dụ chùm mắt. |
| B4 | 14.96–19.54 | "searches the bunch and elects a local expert" | Jet thắng **bừng sáng lavender** `Local Expert`. |
| B5 | 19.54–22.02 | "best fit for each landmark" | Mỗi nút rút 1 expert. |
| B6 | 22.02–25.32 | "limitless coverage" | Nhãn `Limitless coverage`. Chốt. |

## 🎬 S10 — GRAPH SIMILARITY · 24.33s · ThreeDScene (hoặc Scene)
| Beat | Mốc | Thoại | Hình |
|---|---|---|---|
| B0 | 0.00–2.50 | "graph correctly fitted?" | Câu hỏi + graph trên mặt. |
| B1 | 2.50–7.60 | "optimization... a tug-of-war" | Ẩn dụ **kéo co**; `MathTex` S_B (2 số hạng). |
| B2 | 7.60–10.52 | "rewards jet similarity" | Bên trái `Reward (jet match)` (mint). |
| B3 | 10.52–15.70 | "penalizes distortion, scaled by λ" | Bên phải `Penalty (distortion) × λ` (coral). |
| B4 | 15.70–19.34 | "force nose up onto the forehead" | Nút mũi bị kéo lên trán. |
| B5 | 19.34–23.80 | "edge stretches... enormous penalty" | Cạnh **lò xo** giãn → vùng phạt coral bùng. Chốt. |

## 🎬 S11 — ELASTIC MATCHING 4 BƯỚC ⭐ · 44.63s · ThreeDScene
| Beat | Mốc | Thoại | Hình |
|---|---|---|---|
| B0 | 0.00–2.80 | "heart of the algorithm" | Mặt + lưới mờ phía trên; nhãn `Elastic Matching`. |
| B1 | 2.80–5.98 | "rigid to supple" | Thanh `Rigid → Supple`. |
| B2 | 5.98–10.92 | "rigid block sliding to locate the face" | Lưới CỨNG **trượt** quét + heatmap; dừng tại mặt; `λ = ∞`. |
| B3 | 10.92–17.02 | "scales globally... stretches width/height" | Lưới co giãn size rồi kéo x/y (aspect). |
| B4 | 17.02–21.20 | "the magic... the word elastic" | Chữ `ELASTIC` sáng lavender; lưới "thở". |
| B5 | 21.20–22.88 | "the graph is released" | Nút mở khoá chế độ cứng. |
| B6 | 22.88–28.24 | "each node crawls toward its true landmark" | Từng nút **bò** về mốc (LaggedStart) → glow. |
| B7 | 28.24–32.72 | "edges act as springs" | Cạnh **lò xo**; `λ = 2`. |
| B8 | 32.72–35.72 | "two phases" | Tách timeline 2 phase. |
| B9 | 35.72–40.56 | "Normalization, crop to 128×128" | `Phase 1: Normalization` (crop `128×128`). |
| B10 | 40.56–44.16 | "recognition, extract final detailed graph" | `Phase 2: Recognition` (lưới chi tiết). Chốt. |
*Lưu ý:* STT "120x128" → đúng `128×128`. Nút bò LaggedStart, không nhảy loạn.

## 🎬 S12 — RECOGNITION & RANK · 21.87s · ThreeDScene
| Beat | Mốc | Thoại | Hình |
|---|---|---|---|
| B0 | 0.00–5.12 | "elastic grid locked onto the new face (probe)" | Lưới khoá chặt mặt; nhãn `Probe`. |
| B1 | 5.12–9.08 | "compare against each person in the gallery" | `Gallery` 3D dạng kệ; tia so khớp. |
| B2 | 9.08–12.20 | "drop phase, use amplitude only" | `MathTex` S_G; nhãn `amplitude only`. |
| B3 | 12.20–16.72 | "amplitude robust to expression/smiles" | Mặt cười vẫn khớp. |
| B4 | 16.72–21.44 | "score, rank... rank 1 is the identity" | Bảng rank; `Rank 1 [WINNER]` trượt lên (vàng). Chốt. |

## 🎬 S13 — DATA & FERET RESULTS · 35.43s · ThreeDScene
| Beat | Mốc | Thoại | Hình |
|---|---|---|---|
| B0 | 0.00–2.50 | "how about reality?" | Câu hỏi. |
| B1 | 2.50–5.68 | "US government's tough FERET test" | Nhãn `FERET (US gov)`. |
| B2 | 5.68–9.68 | "exactly one image per person" | `1 image / person`. |
| B3 | 9.68–13.06 | "same frontal pose, 98%" | Bar `Frontal 98\%` (mint). |
| B4 | 13.06–17.48 | "same profile, mirrored L/R, 84%" | Bar `Profile (mirrored) 84\%` (cyan). |
| B5 | 17.48–20.34 | "same half-profile angle, 57%" | Bar `Half-profile R/L 57\%` (teal). |
| B6 | 20.34–26.24 | "gallery frontal, probe angled → 18%" | Bar `Frontal→angled 18\%` (coral). |
| B7 | 26.24–31.72 | "king at expression/lighting changes" | Nhãn `King: expression / lighting`. |
| B8 | 31.72–34.98 | "3D rotation = Achilles heel" | Nhãn `3D rotation = Achilles heel`. Chốt. |
*Sửa lỗi cũ:* nhãn ĐÚNG cặp pose 98/84/57/18 (57% là half-profile R/L, KHÔNG phải cross-pose).

## 🎬 S14 — CROSS-POSE · PHASE · SPEED · 42.17s · ThreeDScene
| Beat | Mốc | Thoại | Hình |
|---|---|---|---|
| B0 | 0.00–6.36 | "small angles 11°, 22°, graph flexibility" | Đường cong góc xoay 3D; mốc `11°`,`22°`. |
| B1 | 6.36–9.46 | "accuracy holds 94 → 88%" | Nhãn `94\% → 88\%`. |
| B2 | 9.46–13.26 | "is phase really necessary?" | Câu hỏi `Phase necessary?`. |
| B3 | 13.26–19.78 | "drop phase → drift over 5.2 pixels" | Cột `No phase: 5.2 px` (coral). |
| B4 | 19.78–22.38 | "recognition down to 67" | `67\%`. |
| B5 | 22.38–27.60 | "keep phase → 1.6 px, recognition 88" | Cột `With phase: 1.6 px / 88\%` (mint). |
| B6 | 27.60–31.26 | "phase is the anchor" | Nhãn `Phase = anchor`. |
| B7 | 31.26–39.42 | "separating extraction from matching → ~1000× faster" | Tách `Extraction (once)` vs `Matching (×many)`; `~1000× faster`. |
| B8 | 39.42–41.44 | "fast enough for large databases" | Nhãn `Large DB ready`. Chốt. |

## 🎬 S15 — BIG PICTURE · 33.99s · ThreeDScene
| Beat | Mốc | Thoại | Hình |
|---|---|---|---|
| B0 | 0.00–5.98 | "zoom out... in-class recognition under variance" | `In-class recognition under variance`. |
| B1 | 5.98–12.78 | "faces, animals, vehicles... PCA wrecked by sunglasses" | 4 icon in-class; PCA bị **phá toàn ảnh** vì kính (coral). |
| B2 | 12.78–20.68 | "EBGM compartmentalizes risk — glasses only disturb eye jets" | Kính → chỉ jet mắt nhiễu, phần khác an toàn (mint). |
| B3 | 20.68–27.76 | "limits: weak >22°, fragile when landmarks occluded" | Nhãn `>22° weak`, `occlusion fragile` (coral). |
| B4 | 27.76–33.52 | "no massive training → did exceptionally well" | Nhãn `No massive training` (mint). Chốt. |
*Chống chồng lấp:* PCA-fail (B1) tách rõ với EBGM-compartmentalize (B2), không đè.

## 🎬 S16 — CONCLUSION · 20.99s · ThreeDScene (hoặc Scene)
| Beat | Mốc | Thoại | Hình |
|---|---|---|---|
| B0 | 0.00–3.94 | "symphony of local signal processing (wavelets)" | Wavelet glow; nhãn `Local signal (wavelets)`. |
| B1 | 3.94–9.52 | "+ spatial geometry (graphs)... deep learning wears crown" | Graph + nhãn `Spatial geometry (graphs)`. |
| B2 | 9.52–15.32 | "elastic landmarks live on in modern face detection" | Lưới landmark mờ dần vào hiện đại. |
| B3 | 15.32–20.44 | "Local, Elastic, General. Thank you." | 3 keyword `LOCAL · ELASTIC · GENERAL` (cyan/lavender/mint) + lời cảm ơn. Chốt. |

---

# BẮT ĐẦU
Chạy Phase 0 (mục 2) + thêm helper LaTeX/timing (mục 3,4). Rồi làm **S01**, render `-pql`, đo ffprobe, báo cáo, chờ duyệt → tiếp S02 … S16 → build full + report.
