# Implementation Plan - Redesign S10 Graph Similarity

Redesign `release/scene_S10_graph_sim.py` to replace the 2D hand-drawn face outline with a real face image (`s8_face.png` framed in a card), map landmarks using the exact same coordinates and helper `L(u, v)` as S08/S09, clean up formula and badge positions, and resolve overlaps in B6-B8.

## Proposed Changes

### [S10 Graph Similarity Scene Component]

#### [MODIFY] [scene_S10_graph_sim.py](file:///media/mlinh/Kingston/projects/pattern-recog/video-manim/video-2-ebgm/release/scene_S10_graph_sim.py)
- Import PIL `Image`, `ImageOps` and `Path` from `pathlib` for squared face caching/loading.
- Define directory constants `ASSET_DIR` and `TMP_IMG_DIR`.
- Define `square_cache`, `load_face`, and `make_face_card` helpers (identical to S08/S09).
- Replace the hand-drawn `face` outline with a framed `face_card` of `s8_face.png` scaled to height `4.4`.
- Set up coordinates using the `L(u, v)` mapping helper to match the real features of the face image.
- Reposition formula, rope, knot, and reward/penalty cards to avoid overlaps.
- For B6, B7, B8 (mismatch & penalty):
  - Load the face image and render the normal graph correctly fitted to landmarks.
  - Draw the distorted graph (nose pushed way up to forehead) with a clean arrow, and show the stretched edge using a nice spring visualization.
  - Reposition all labels (`force nose onto forehead`, `edge stretches`, `ENORMOUS PENALTY`, `S_B \downarrow`) to ensure they do not collide with elements or panels.
- Group all elements containing `ImageMobject` with `Group` instead of `VGroup`.

## Verification Plan

### Automated Tests
- Run low-quality preview rendering:
  ```bash
  conda run -n vid manim -ql release/scene_S10_graph_sim.py S10_GraphSim
  ```
- Run `ffprobe` to verify duration is exactly `26.15s` (within $\pm 0.3$s):
  ```bash
  ffprobe -v error -show_entries format=duration -of csv=p=0 video-2-ebgm/media/videos/scene_S10_graph_sim/480p15/S10_GraphSim.mp4
  ```
- Check for forbidden keywords and Vietnamese text using `rg`:
  ```bash
  rg -n "Text\(|font=|Paragraph|make_subtitle|[À-ỹ]" video-2-ebgm/release/scene_S10_graph_sim.py
  ```
- Compile the final high-quality video:
  ```bash
  conda run -n vid manim -qh --disable_caching release/scene_S10_graph_sim.py S10_GraphSim
  ```
