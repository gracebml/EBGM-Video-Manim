# EBGM Manim Rework Notes

## Global Rules
- Work at source level in `video-2-ebgm/release/*.py`; do not use timestamp cutting or the old `build_release_cut.py` pipeline.
- Keep audio embedded with `self.add_sound(T["audio_path"])`.
- Match each rendered scene to `audio/en/transcript.json` duration with `ffprobe`; target tolerance is `abs(delta) <= 0.3s`.
- Use `load_scene_timing`, `seg_end`, and `word_start` for beat timing. Important visual events should land on transcript segments or word starts.
- English-only visuals. No Vietnamese labels, no subtitles, no dialogue captions.
- Use `_common.en_label(...)` or `MathTex`/`Tex` with the shared template. Do not use `Text(...)`, custom `font=...`, `Paragraph`, or `make_subtitle`.
- Preserve the shared palette from `_common.py`: navy background, cool cyan/teal/blue, lavender EBGM accents, mint positives, coral warnings.
- Do not edit original `scene_*.py` sources unless explicitly asked. New/reworked scenes live in `release/`.

## Visual Style
- Clarity beats decoration. Every visual must explain the spoken idea, not merely look impressive.
- Avoid generic continuous motion such as ribbon-like trails, endless orbiting, or slow ambient drift.
- Prefer 3Blue1Brown-like stepped reveals: show one idea clearly, hold long enough to read, then transition cleanly.
- At any moment, keep one visual focus. Fade or dim old elements before introducing the next focus.
- Make key diagrams and images large enough to read. Avoid tiny decorative elements that compete with the main idea.
- Use fast, meaningful cuts and transforms when the narration is dense; do not leave dead waits while voiceover continues.
- Use 3D only when it materially clarifies the concept. If 3D becomes abstract or confusing, switch to direct 2D/2.5D.
- Do not use ambient camera rotation by default. Camera motion should be short, purposeful, and tied to a concept.

## Arrow & Overlap Conventions
- Arrowheads must be slim, not the clunky default filled triangle. Use the `_common.py` helpers `thin_arrow(...)` / `thin_curved_arrow(...)` (Manim `StealthTip`, stroke ~2–2.4, tip ≤16% of length). Replace `Arrow`/`Vector`/`CurvedArrow` accordingly; for `Arrow3D` shrink the cone (`height`/`base_radius` small).
- No element may overlap another at the same time/place: arrowheads must stop with a clear gap before any text (canh theo `get_left()/get_right()` + margin); labels and inner icons inside a card must be stacked with spacing (heading at top, icon below, note outside/at bottom), never colliding.
- A `Cross(...)` over a thumbnail (e.g. S04 "raw pixels" / "linear PCA") is an intentional "rejected approach" mark, not an artifact; keep it slim so it does not look like a scribble.

## Image-Based Scenes
- Prefer real images when the scene is about recognition, identity, expression, pose, or lighting.
- For S02 and similar scenes, use the real assets in the repo root `assets/`, not `video-2-ebgm/assets/`.
- Current S02 assets:
  - `assets/s2_same_neutral.jpg`
  - `assets/s2_same_smile.jpg`
  - `assets/s2_same_frown.jpg`
  - `assets/s2_same_lowlight.jpg`
  - `assets/s2_same_pose.jpg`
  - `assets/s2_personA.jpg`
  - `assets/s2_personB.jpg`
- Fix images to a common visual size, usually by setting height and placing them in a consistent rounded frame.
- If an image is missing, use a simple 2D fallback face, not a 3D mesh.
- For same-identity montages, verify the images actually look like the same person. If `s2_same_neutral.jpg` does not match the other same-person images, skip it in the main montage.

## S01 Cold Open Notes
- The street-recognition opening must be sparse and readable.
- Keep the background as a night-street hint only: few buildings, low opacity, minimal window glints, no decorative surveillance/camera/scan icons.
- Keep person A on the left and person B on the right. They may step closer but must stop with clear space between heads.
- The recognition moment should have one strong focus:
  - a bright gaze line from A to B,
  - one moving spark along that line,
  - one pulse ring on B,
  - one large `Recognized!` label or one large check, not both.
- Fade the street, people, gaze, pulse, and label cleanly before the `face.png` teaser enters.

## S02 Redesign Notes
- S02 should be fully 2D or `MovingCameraScene`; do not use `ThreeDScene`.
- Remove the abstract 3D face mesh, ellipsoid surface, sphere eyes, and ambient camera rotation.
- The scene idea is:
  - the hard part is not simply telling two different people apart,
  - the hard part is that the same person can look dramatically different under expression, light, and pose,
  - pixel matrices can change entirely,
  - this is intra-class variance,
  - the algorithm must be both `Tolerant` and `Sharp`.
- Use quick, clear image montage beats:
  - `Different people` fades/dims as "not the hard part".
  - `Same person` montage becomes the main focus.
  - Cut through `smile`, `frown`, and `under-lit`.
  - Show pixel grid and coral heatmap flare for pixel change.
  - Punch in `Intra-class variance`.
  - Split into `Tolerant` and `Sharp`.
  - For `Sharp`, zoom quickly into a tiny detail between two different people.
- No slow-motion orbit, no mesh, no visual abstraction that makes the identity problem harder to understand.

## S03 Redesign Notes ("Pre-Deep-Learning")
- `release/scene_S03_pre_deeplearning.py`, class `S03_PreDL`, `MovingCameraScene` (no `ThreeDScene`, no ambient rotation).
- Draw "3D" as isometric polygon blocks (3 shaded faces), not `Surface` meshes.
- CNN must read as real convolution volumes: blocks pop one-by-one on the spoken keyword ("CNN", "millions of images", "loss", "backpropagation") with clean forward arrows; the backprop arrow is one tidy `CurvedArrow`, label placed below it, never overlapping blocks.
- "Rewind to 1997": reverse the forward arrows, collapse/fade blocks in reverse, spin a clock backward once (not continuous), reveal `1997`.
- Draw a recognizable 3D GPU (`gpu_3d`: body + two fans + PCIe) and a dataset block; cross each out with coral on "No powerful GPUs" / "No massive datasets". No spinning.
- Later beats must be rich, not bare text: use the real paper image `assets/ebgm_paper_p1.png` (page 1 of EBGM.pdf) with an `IEEE PAMI · 1997` stamp; a glowing visual-cortex illustration; a bold `ELASTIC BUNCH GRAPH MATCHING` reveal; a `FERET top-ranked` ranking badge/podium.
- STT fixes to honor in labels: "IEE PAMI" -> `IEEE PAMI`, "ferret" -> `FERET`.

## S04 Idea Notes ("Three Pillars")
- `release/scene_S04_idea.py`, class `S04_Idea`, `MovingCameraScene` (no `ThreeDScene`/rotation).
- Three pillars, each a clean readable icon (no abstract scattered dots/lines): 1) `Image Graph` = real `face.png` with landmark dots + edges; 2) `Wavelet Jet` = a stack-of-discs bundle (match S06 style) with `texture DNA`, `not color`; 3) `Face Bunch Graph` = several face-graphs stacked in depth with pose labels.
- Intro contrast must be clean, not crude doodles: real face center, flanked by a pixel-mosaic thumbnail (`raw pixels` ✗) and a blurred thumbnail (`linear PCA` ✗); both fade as the pillars build. Use slim `Cross` marks.
- End with three strength chips: `Robust to light`, `< 100 images`, `High accuracy`.

## S06 / S07 Specific Fixes
- S06 amplitude/phase cards: give enough height; stack heading → optional icon → note with spacing so text never overlaps the inner circle; formula→card arrows stop above the card edge.
- S07: the `match?` label must have clear space; the two converging arrows stop well short of it (no arrowhead touching the word).

## Per-Scene Fix Prompts
- Iterative per-scene redesign prompts live in `video-2-ebgm/prompt_codex_S0X_*.md` (e.g. `prompt_codex_S01_fix.md`, `prompt_codex_S02_redesign.md`, `prompt_codex_S03_redesign.md`, `prompt_codex_S03_mathframe.md`, `prompt_codex_S04_redesign.md`, `prompt_codex_fix_arrows_overlap.md`). Work one scene at a time: edit `release/`, re-run `render_hd.sh` (it re-renders only stale scenes via `-nt`), then review.

## Project Context & Current State
- This is video 2 of a pattern-recognition series (video 1 = Parzen Windows in `video-1-parzen/`). The EBGM source paper is `video-2-ebgm/EBGM.pdf` (Wiskott et al., IEEE PAMI 1997 / CRC 1999).
- The release video is an English, ~9-minute, 16-scene cut condensed from 33 original `scene_*.py`. Mapping and the keep/cut/merge rationale live in `video-2-ebgm/kich_ban_ebgm.md` (Vietnamese) and `video-2-ebgm/script_ebgm_en.md` (English VO). The single operating spec for the rework is `video-2-ebgm/prompt_v2.md`; per-scene fix prompts are `prompt_codex_S0X_*.md`.
- Original `scene_*.py` (33 files, no `scene_18`) are untouched references. All reworked scenes are `release/scene_S01..S16_*.py`.
- Voice: ElevenLabs "Jessica" (`eleven_multilingual_v2`). Audio is the canonical timing master in `audio/en/scene_01..16.mp3`; old George set is backed up in `backups/audio_en_george/`. Do not re-stretch audio; build visuals to the audio.
- The deprecated ffmpeg time-slice pipeline (`build_release_cut.py`, `media/release_cut_16_scenes/`) is quarantined under `backups/deprecated/`; never reuse it.

## Audio & Timing Pipeline
- Regenerate audio: ElevenLabs TTS from the clean per-scene text in `audio/_scenes_en.json` (not from STT text). Voice id Jessica = `cgSgspJ2msm6clMCkdW9`.
- After any audio change, re-run `transcribe_audio.py` (conda env `vid`, faster-whisper `large-v3-turbo`, CPU int8) to refresh `audio/en/transcript.json` with word- and segment-level timestamps; scenes auto-resync via `load_scene_timing()`.
- `audio/en/transcript.json` is the single source of truth for `load_scene_timing` / `seg_end` / `word_start`. Segment counts differ from the old George set; never hardcode times — read them.

## Scene Map (file · class · key · audio duration s)
- S01 `scene_S01_cold_open.py` · `S01_ColdOpen` · scene_01 · 25.73
- S02 `scene_S02_why_hard.py` · `S02_WhyHard` · scene_02 · 29.21
- S03 `scene_S03_pre_deeplearning.py` · `S03_PreDL` · scene_03 · 57.21
- S04 `scene_S04_idea.py` · `S04_Idea` · scene_04 · 35.85
- S05 `scene_S05_gabor.py` · `S05_Gabor` · scene_05 · 36.55
- S06 `scene_S06_jet.py` · `S06_Jet` · scene_06 · 28.56
- S07 `scene_S07_similarity.py` · `S07_Similarity` · scene_07 · 36.55
- S08 `scene_S08_image_graph.py` · `S08_ImageGraph` · scene_08 · 23.64
- S09 `scene_S09_bunch_graph.py` · `S09_BunchGraph` · scene_09 · 25.50
- S10 `scene_S10_graph_sim.py` · `S10_GraphSim` · scene_10 · 26.15
- S11 `scene_S11_elastic.py` · `S11_Elastic` · scene_11 · 46.39
- S12 `scene_S12_recognition.py` · `S12_Recognition` · scene_12 · 22.38
- S13 `scene_S13_feret.py` · `S13_Feret` · scene_13 · 36.87
- S14 `scene_S14_phase_speed.py` · `S14_PhaseSpeed` · scene_14 · 44.44
- S15 `scene_S15_big_picture.py` · `S15_BigPicture` · scene_15 · 35.53
- S16 `scene_S16_conclusion.py` · `S16_Conclusion` · scene_16 · 24.06
- Full cut ≈ 8:54.

## Build / Render Workflow
- Run all from `video-2-ebgm/` in conda env `vid` (Manim Community v0.20.1).
- `bash render_hd.sh` renders every scene at 1080p60 and concatenates to `release/EBGM_EN_v1_HD.mp4` plus `release/durations_report.csv`.
- The script re-renders a scene only when its source `.py` is newer than the rendered mp4 (`[ "$out" -nt "$file" ]`); otherwise it skips. So after editing a scene, just re-run `render_hd.sh` and it rebuilds only what changed, then re-concats. If a player still shows the old clip, the render was stale — check source-vs-mp4 mtimes.
- Concatenation uses the ffmpeg concat demuxer over the per-scene mp4s (audio is already embedded via `add_sound`); never cut by timestamp.

## Environments & Assets
- conda envs: `vid` (Manim + faster-whisper), `f5tts` (F5-TTS + Kokoro experiments; F5-TTS is too slow on this CPU-only machine — abandoned in favor of ElevenLabs). No GPU.
- Real images live in repo-root `assets/` (one level above `video-2-ebgm/`): `face.png`, `ebgm_paper_p1.png` (EBGM.pdf p1), the `s2_*` set, plus optional `gpu.png`/`brain.png` for S03. Reference them with `Path(__file__).resolve().parents[1] / "assets"`.

## Rendering And Verification
- Quick render during iteration may use `-pql`; final requested quality may use `-qh --disable_caching`.
- Measure final mp4 with:
  - `ffprobe -v error -show_entries format=duration -of csv=p=0 <file.mp4>`
- After source edits, run checks such as:
  - `python3 -m py_compile video-2-ebgm/release/<scene>.py`
  - `rg -n "Text\\(|font=|Paragraph|make_subtitle|[À-ỹ]" video-2-ebgm/release/<scene>.py`
- GUI preview warnings like `cannot open display` do not matter if Manim reports the mp4 file is ready.
