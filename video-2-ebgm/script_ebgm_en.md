# 🎬 EBGM Video Script (10-minute cut — FINAL) — Elastic Bunch Graph Matching

> **Basis:** 33 pre-built scenes (`scene_01..scene_33.py`, `scene_18` missing) in 4 parts: Overview (1–7), Algorithm Detail (8–17), Experiments (19–26), Discussion (27–33). Planned runtime of all 33 ≈ **29 min** → trimmed to **~10 min / 16 scenes**.
> **This version** = the 16-scene cut + a "tech-storytelling" voiceover (intuition, deep-learning analogies), with all reviewed errors fixed (the 57% figure, terminology, publication year, the cut-off line…), plus a **new storyboard for S3** ("pre-deep-learning era" idea).
> **Style & color:** keep the series' `_common.py` (deep navy background, lavender `#B8B5FF` = EBGM signature). Subtitles rendered as `Text`; formulas as `MathTex`.
> **VO delivery:** Explanatory / Tech-Storytelling (3Blue1Brown · Veritasium). Stress the opposing pairs (Reward/Penalty, Rigid/Elastic, Tolerant/Sharp). Slow down one beat on the basin/sharp-peak passage (S7).
> **Note:** This is the English companion to `kich_ban_ebgm.md`. Same timing, structure, and source-scene mapping; only the voiceover/labels are in English.

---

## 📊 PART A — 33-SCENE ANALYSIS: KEEP / CUT / MERGE

| Source scene | Content | Planned | Decision | Reason |
|---|---|---|---|---|
| 01 Title | EBGM title | 12s | **MERGE→ S1** | Short cold open, fold into the problem |
| 02 Face Recognition | Verification 1:1 vs Identification 1:N | 50s | **MERGE→ S1** | Keep only "EBGM solves 1:N" |
| 03 Core Problem | In-class variance, collapse + emphasize | 55s | **KEEP→ S2** | Core "why it's hard" |
| 04 Prior Approaches | Hand-crafted / NN / PCA | 90s | **❌ replaced by new S3** | Per user: pre-DL framing |
| 05 Bridge Problem | Need a middle-ground solution | 15s | **MERGE→ S3 (1 line)** | Closing line into EBGM |
| 06 EBGM Novel | Image Graph + Jet + Bunch + strengths | 75s | **KEEP→ S4** | Idea manifesto |
| 07 Teaser | Overview wrap-up | 15s | **❌ CUT** | Redundant transition |
| 08 Intro | "How does EBGM work?" | 20s | **❌ CUT** | Redundant transition |
| 09 Gabor Basics | Gabor wavelet, DC-free, biology | 80s | **KEEP→ S5** | Technical foundation |
| 10 Jet Basics | 40 complex coefficients/point | 60s | **KEEP→ S6** | The jet concept |
| 11 Similarity | Sₐ (coarse) vs S_φ (fine, phase) | 75s | **KEEP→ S7** | Important: phase → localization |
| 12 Individual Graph | Nodes=jet, edges=Δx | 65s | **KEEP→ S8** | Image graph definition |
| 13 Bunch Graph | FBG, stacked graphs | 70s | **KEEP→ S9** | The breakthrough idea |
| 14 Graph Similarity | Feature match − λ·distortion | 55s | **KEEP→ S10** | Matching objective |
| 15 Matching Procedure | Elastic matching, 4 steps | 110s | **KEEP→ S11** ⭐ | Heart of the algorithm |
| 16 Two-Stage | Normalization → Recognition | 50s | **MERGE→ S11 (1 line)** | Secondary detail |
| 17 Recognition Stage | Probe/gallery compare, ranking | 60s | **KEEP→ S12** | Recognition step |
| 19 Intro Experiments | 4 questions | 20s | **❌ CUT** | Redundant transition |
| 20 Databases | FERET + Bochum, poses | 50s | **MERGE→ S13** | Fold into FERET results |
| 21 FERET Results | 98% / 84% / 57% | 75s | **KEEP→ S13** | Key figures |
| 22 Bochum Results | Cross-pose 94%/88%, 30 nodes | 60s | **MERGE→ S14** | Fold into phase |
| 23 Phase Importance | 1.6px vs 5.2px; 88% vs 67% | 70s | **KEEP→ S14** | Evidence of phase's role |
| 24 Efficiency | ~1000× faster; ZN-Face | 55s | **MERGE→ S14 (1 line)** | Fold at end of S14 |
| 25 Benchmarks | Blind test vs Gordon/Gutta/Phillips | 90s | **❌ CUT** | Overlaps comparison; heavy |
| 26 Summary | Part-3 recap | 25s | **❌ CUT** | Redundant |
| 27 Generality | In-class: faces/animals/vehicles | 45s | **KEEP→ S15** | Broader meaning |
| 28 Vs Preceding | vs Lades 1993 | 70s | **❌ CUT** | Phase/FBG already covered |
| 29 Vs Template | Feature-based vs PCA | 45s | **MERGE→ S15** | Representative comparison |
| 30 Vs 3D | 2D grid vs 3D morphable | 50s | **❌ CUT** | Off the main thread |
| 31 Pros/Cons | 3 pros / 3 cons | 60s | **MERGE→ S15** | Wrapped into "big picture" |
| 32 Legacy/Future | Legacy, bridge to deep learning | 55s | **MERGE→ S16 (1 line)** | Fold into conclusion |
| 33 Conclusion | Closing | 30s | **KEEP→ S16** | Closes the video |

**Fully cut:** 07, 08, 19, 25, 26, 28, 30. **New replacement:** 04→S3. **Result:** 16 scenes, target ~10:48 (see Part C for how to reach 10:00).

---

## 🎯 PART B — COMPLETE SCRIPT (16 SCENES · VO + VISUAL + TIMING + SOURCE)

> Each scene: **timing · source scene**, then **🎤 Voiceover (VO)** and **🎨 Visual**. VO paced at ~150 wpm.

---

### 🎬 S1 — COLD OPEN & THE PROBLEM
**⏱ 0:00 → 0:24 (24s) · source: sc01 + sc02**

**🎤 Voiceover**
> "You glance at someone you know on the street, and your brain recognizes them in a tenth of a second. But how does a computer recognize a face?
>
> The problem has two branches: *Verification 1:1* — 'Am I really the owner of this phone?'; and *Identification 1:N* — 'Who is this person among millions of records?'
>
> Today, we tackle the harder branch: **1:N identification**."

**🎨 Visual**
- 0:00–0:09: Title `EBGM — Elastic Bunch Graph Matching` (lavender) appears, then shrinks to a corner (sc01).
- 0:09–0:24: Two cards `VERIFICATION 1:1` and `IDENTIFICATION 1:N` (sc02); the **1:N card glows lavender**, the 1:1 card dims.
- *Cut:* drop the long FaceID/passport examples from sc02.

---

### 🎬 S2 — WHY FACE RECOGNITION IS HARD
**⏱ 0:24 → 1:02 (38s) · source: sc03**

**🎤 Voiceover**
> "What troubles AI the most? Not the difference between two people — but the fact that *the same person* can look like two completely different people.
>
> When you smile, frown, or light hits from below, the pixel matrix changes entirely. This is called *intra-class variance*.
>
> A good algorithm must resolve this paradox: be **tolerant enough to forgive** one person's deformations, yet **sharp enough to distinguish** the tiniest details between two different people."

**🎨 Visual**
- 0:24–0:48: One person through 5 states (frontal / pose / expression / lighting / occlusion) tagged `SAME PERSON` (sc03).
- 0:48–1:02: Two opposing goals light up: `Tolerant — forgive deformation` / `Sharp — distinguish features` (sc03, relabeled to match the pair).
- *Cut:* drop the "wide face vs long face" part.

---

### 🎬 S3 — THE PRE-DEEP-LEARNING ERA (NEW storyboard) ⭐
**⏱ 1:02 → 1:52 (50s) · source: BUILD NEW (replaces sc04) + closing line from sc05**

> **Note:** This scene's content fully changes from sc04 (the 3 prior approaches) → it **must be built fresh**; sc04/05 cannot be reused. The idea (per the user): place EBGM in the context before neural networks took over.

**🎤 Voiceover**
> "Today, facing a face-recognition problem, what's our first instinct? Build a CNN, gather millions of images, define a loss function, and let backpropagation do the rest.
>
> But rewind to 1997. No powerful GPUs. No massive datasets. Recognizing a face under changing light or expression was nearly impossible if you only compared pixels.
>
> So how did scientists back then solve this *geometric-variance* problem? Not with deep learning — but with pure mathematics and signal processing. In 1997, a group published in IEEE PAMI — one of the most rigorous AI journals — an unusual idea: teach the computer to *see* a face the way our **visual cortex** does.
>
> That algorithm is **Elastic Bunch Graph Matching**. It once ranked among the very best in the FERET blind tests of the 1990s. Today, we dissect it."

**🎨 Visual (new storyboard)**
- 1:02–1:18 — *Modern instinct:* on the left, a multi-layer CNN diagram (stacked blocks) + a `Backpropagation` arrow running backwards + labels `millions of images` and `Loss ↓`. Coral/teal tones (deep-learning feel). `LaggedStart` the layers.
- 1:18–1:30 — *Rewind time:* a clock/reel spins backwards; the CNN fades and shrinks. Three "scarcity of 1997" cards appear: `No GPU`, `No big data`, `Pixel-by-pixel fails` (coral ✗ icons). A face shifts light/expression, making the pixel grid flicker chaotically.
- 1:30–1:42 — *The paper:* zoom into a stylized "paper cover," stamped **`IEEE PAMI · 1997`** (lavender), with a small note `(expanded into CRC book chapter, 1999)`. A *visual cortex* icon (brain outline + rays) lights up — foreshadowing Gabor in S5.
- 1:42–1:52 — The name `ELASTIC BUNCH GRAPH MATCHING (EBGM)` appears large center-screen (lavender, glow); a small badge `FERET · top-ranked`. Closing line from sc05 as subtitle: `A middle ground: structure + signal, no massive training`.

---

### 🎬 S4 — THE EBGM IDEA: THREE PILLARS
**⏱ 1:52 → 2:36 (44s) · source: sc06**

**🎤 Voiceover**
> "EBGM is built on three pillars — unlike memorizing pixels or compressing them linearly as PCA does:
>
> One — don't see the face as a plane of pixels, but as a **graph** connecting landmark points. Two — at each landmark, don't take color, but extract a **wavelet jet**, loosely the *texture DNA* of that patch of skin. Three — to handle every pose, stack many sample graphs into a **Face Bunch Graph**.
>
> The result? A system that's highly robust to lighting, learns from fewer than a hundred sample images, and achieves astonishing accuracy."

**🎨 Visual**
- 1:52–2:18: Three concepts appear in sequence: `1. Image Graph` (landmark grid on a face), `2. Wavelet Jet` (8-direction Gabor bundle), `3. Bunch Graph` (stacked graphs) (sc06).
- 2:18–2:36: Four strengths, compact: `Robust to light · Flexible recombination · Little data · Easy to extend`; closing tag `BALANCE: DESIGN ↔ MACHINE LEARNING`.
- *Cut:* the long "human cognition" analogy from sc06; drop sc07.

---

### 🎬 S5 — GABOR WAVELETS: THE EYES OF EBGM
**⏱ 2:36 → 3:22 (46s) · source: sc09 · 💡 analogy: CNN filters**

**🎤 Voiceover**
> "Let's start micro: how does the AI *see* a single point on a face? Instead of pixels — which are very light-sensitive — scientists borrowed from biology.
>
> They use **Gabor wavelets**: mathematically, a sine wave *trapped* inside a Gaussian envelope. It acts as a filter, capturing only wrinkles and edges at one specific orientation and frequency.
>
> The beauty: it cancels out the background-light component — it's DC-free. Just like the first layers of a CNN detect edges, the Gabor wavelet mirrors exactly how the visual cortex works."

**🎨 Visual**
- 2:36–3:02: Plane wave × Gaussian envelope = Gabor kernel (real/imaginary/magnitude) (sc09); label `DC-free`.
- 3:02–3:22: Four properties light up in turn: `Light-robust · Tolerates deformation/rotation · Mimics visual cortex · Optimal for natural images`.
- *Add small caption:* `≈ first-layer CNN filter` (to match the VO analogy).

---

### 🎬 S6 — JET: 40 COMPLEX COEFFICIENTS AT A POINT
**⏱ 3:22 → 3:58 (36s) · source: sc10 · 💡 analogy: "barcode"**

**🎤 Voiceover**
> "Now throw the whole bank of forty Gabor wavelets — five frequencies times eight orientations — at a single point like the corner of an eye, and you get **forty complex numbers**. That bundle is called a **jet**.
>
> Think of a jet as a unique *barcode* of that eye corner. And since they're complex, each element carries two weapons: **amplitude** — telling us what *shape* the region has; and **phase** — telling us *exactly which coordinate* the feature sits at."

**🎨 Visual**
- 3:22–3:42: A point on the face radiates 40 rays to 40 Gabor patches → bundled into a "stack of discs" jet (sc10).
- 3:42–3:58: Formula `𝒥ⱼ = aⱼ·exp(i·φⱼ)`; opposing labels `amplitude → recognition (shape)` / `phase → localization (coordinate)`.

---

### 🎬 S7 — COMPARING JETS: TWO SIMILARITY FUNCTIONS
**⏱ 3:58 → 4:46 (48s) · source: sc11 · 💡 analogy: loss landscape / attractor basin**

**🎤 Voiceover — *slow down one beat on the basin/sharp-peak passage***
> "With two jets, how does the machine know they match? The algorithm pairs two similarity functions in beautiful harmony.
>
> The first compares only *amplitude*, ignoring phase. Picture it forming a smooth *basin* — a wide attractor — that lets the algorithm catch a signal from afar and slide toward the eye. This is the **coarse** step.
>
> Once very close, the second function *with phase* kicks in. It's razor-sharp, sensitive to the tiniest shift, pinning the exact position with **sub-pixel** accuracy. Better still, it *points the way*: it tells you how far to move the jet."

**🎨 Visual**
- 3:58–4:24: Two panels: `Sₐ` smooth wide basin ("large attractor basin · coarse") vs `S_φ` many sharp peaks ("sub-pixel · fine") (sc11).
- 4:24–4:46: *(matching the "points the way" line)* a lavender displacement arrow guides an off-center jet onto the eye; a `focus 1→5` bar (coarse-to-fine).

---

### 🎬 S8 — IMAGE GRAPH: THE FACE AS A GRAPH
**⏱ 4:46 → 5:16 (30s) · source: sc12**

**🎤 Voiceover**
> "Sprinkle these jets onto the landmarks — eyes, nose, mouth — and connect them… and you have an **image graph**.
>
> The *nodes* hold the texture barcode (the jet); the *edges* hold geometric distances. The genius key: EBGM fully separates *skin surface* information from *bone structure*, so the machine can process each independently."

**🎨 Visual**
- 4:46–5:16: A lavender graph grid over the face; highlight `node = jet 𝒥ₙ [40 complex]` and `edge = Δxₑ = xₙ − xₙ'` (sc12).

---

### 🎬 S9 — FACE BUNCH GRAPH
**⏱ 5:16 → 6:00 (44s) · source: sc13 · 💡 analogy: Local Expert**

**🎤 Voiceover**
> "But *your* graph can't perfectly fit *my* face. The solution: the **Face Bunch Graph**.
>
> By stacking dozens of different graphs, the *eye* node no longer holds one eye but a whole *bunch*: narrow eyes, round eyes, bespectacled eyes.
>
> Facing a stranger, the system searches the bunch and elects a **local expert** — the best fit for each landmark. This cross-combination yields almost limitless coverage."

**🎨 Visual**
- 5:16–5:38: Several `single graphs` fly in and stack in alignment into the FBG (sc13).
- 5:38–6:00: Zoom into the eye node: a bunch of jets; the winning jet **flares lavender** (`local expert`).

---

### 🎬 S10 — THE GRAPH SIMILARITY FUNCTION
**⏱ 6:00 → 6:32 (32s) · source: sc14 · 💡 analogy: loss + regularization**

**🎤 Voiceover — *stress the Reward/Penalty pair***
> "How do we know the graph is correctly fitted? EBGM solves an optimization with a very familiar objective — a *tug of war*.
>
> On one side it **rewards** jet similarity. On the other it **penalizes** geometric distortion of the edges, scaled by lambda.
>
> If you force the *nose* point up onto the *forehead* to match texture, the connecting edge stretches — and the algorithm hits you with an enormous penalty."

**🎨 Visual**
- 6:00–6:32: Formula `S_B = (1/N)Σ max S_φ − (λ/E)Σ (Δx distortion)²`; three balance examples: high feature + huge penalty / low feature + zero penalty / **good feature + small penalty** (sc14). A stretched-spring edge → coral penalty region.

---

### 🎬 S11 — ELASTIC MATCHING: 4 STEPS ⭐
**⏱ 6:32 → 7:42 (70s) · source: sc15 (+ 1 line from sc16) · 💡 analogy: coarse→fine like annealing**

**🎤 Voiceover — *stress the Rigid/Elastic pair***
> "And here it is — the heart of the algorithm: elastic matching, going from *rigid* to *supple*.
>
> First, the graph is a **rigid** block, sliding across the image to locate the face. Then it scales globally to match size, and stretches width and height for the right aspect ratio.
>
> But the magic is the final step — the word **Elastic**: the graph is *released*. Each node crawls freely, nudging bit by bit toward its true landmark on the image, while the edges act as *springs* holding the structure from breaking apart.
>
> The whole thing runs in two phases: *normalization* — crop the face to a standard 128×128; then *recognition* — extract the final detailed graph."

**🎨 Visual**
- 6:32–6:58: Steps 1–2: the rigid graph scans for the face, then scales to fit (sc15).
- 6:58–7:24: Step 3: stretch aspect, `focus 1→5`. Step 4 ⭐: each node crawls to its landmark, edges shown as **springs**, `λ=2` (sc15).
- 7:24–7:42: One line folding sc16: two blocks `Phase 1: Normalize (128×128)` → `Phase 2: Detailed recognition`.
- *Cut:* drop the 30/70-model parameter table of sc16; keep only the two-phase labels.

---

### 🎬 S12 — RECOGNITION: MATCH & RANK
**⏱ 7:42 → 8:16 (34s) · source: sc17**

**🎤 Voiceover**
> "Once the *elastic grid* is locked onto the new face — the *probe* — recognition is featherlight.
>
> Carry this grid and compare it against each person in the *gallery*. Now we drop phase and **use amplitude only**, because amplitude is more robust to changes in expression and smiles.
>
> Score, rank — and whoever lands at **rank 1** is the identity you're looking for."

**🎨 Visual**
- 7:42–8:02: `PROBE` compared to `GALLERY`, rays linking corresponding nodes; formula `S_G = (1/N')Σ Sₐ` (sc17).
- 8:02–8:16: Ranking table; `Rank 1: M3 — 0.89 [WINNER]` slides to the top, gold border.

---

### 🎬 S13 — EXPERIMENTS: DATA & FERET RESULTS
**⏱ 8:16 → 8:56 (40s) · source: sc20 + sc21**

**🎤 Voiceover — *(57% figure corrected)***
> "Beautiful theory, but how about reality? In the US government's tough FERET test, EBGM was given exactly *one image* per person in the database.
>
> The results? Same frontal pose: **ninety-eight percent**. Same profile pose — mirrored left–right: **eighty-four**. Same half-profile angle: fifty-seven. But if the gallery is frontal while the probe is turned at an angle, it drops sharply to just **eighteen percent**.
>
> Clearly: EBGM is *king* at handling changes in expression or lighting, but large 3D rotation remains its Achilles' heel."

**🎨 Visual**
- 8:16–8:30: Two DB cards `FERET (250 people)` / `Bochum (108)`, the pose strip, label `ONE image/person` (sc20).
- 8:30–8:56: FERET rank-1 bar chart (sc21): `Frontal fa/fb 98%` (mint) · `Profile R/L 84%` (cyan) · `Half-profile R/L 57%` (teal) · `Half-profile vs Frontal 18%` (coral, the "Achilles' heel" beat).
- *Build note:* labels must match the correct pose pairs as in scene_21 (98/84/57/18/12); do not misattribute 57% to cross-pose.

---

### 🎬 S14 — CROSS-POSE, THE ROLE OF PHASE & SPEED
**⏱ 8:56 → 9:46 (50s) · source: sc22 + sc23 + sc24**

**🎤 Voiceover**
> "However, at *small* rotation angles — eleven degrees, twenty-two degrees — thanks to the graph's flexibility, accuracy holds from ninety-four down to eighty-eight percent.
>
> And is the *phase* of the wave really necessary? Experiments show: drop phase, and landmark localization drifts by over *5.2 pixels*, dragging recognition down to sixty-seven. Keep phase: error is only *1.6 pixels*, and recognition jumps to eighty-eight. Phase is the anchor that saves the whole system!
>
> On top of that, separating *extraction* from *matching* makes EBGM about *a thousand times faster* than its predecessor architectures — fast enough even for large databases."

**🎨 Visual**
- 8:56–9:13: Bochum: `11° → 94%`, `22° → 88%`, label `very slight degradation` (sc22).
- 9:13–9:33: Phase comparison: `1.6 px / 88%` (mint) vs `5.2 px / 67%` (coral) (sc23).
- 9:33–9:46: Split diagram `EXTRACTION (once)` ⟶ `MATCHING (×many)`, label `~1000× faster` (sc24).

---

### 🎬 S15 — EBGM IN THE BIG PICTURE
**⏱ 9:46 → 10:26 (40s) · source: sc27 + sc29 + sc31**

**🎤 Voiceover**
> "Zoom out, and EBGM solves a broad class of problems: **in-class recognition under variance** — whether human faces, animals, or vehicles.
>
> Unlike PCA, which is wrecked across the whole image by a single pair of sunglasses, EBGM *compartmentalizes risk*: glasses? Only the eye jets are disturbed; the rest stay safe.
>
> True, it has limits — weak beyond 22 degrees of rotation, fragile when landmarks are occluded. But as an algorithm that needs *no massive training*, EBGM did exceptionally well."

**🎨 Visual**
- 9:46–10:02: `IN-CLASS RECOGNITION` with four icons: faces/animals/vehicles/plants (sc27).
- 10:02–10:14: Mini comparison `EBGM (feature-based)` vs `PCA (template-based)`: glasses/beard only shift locally in EBGM (sc29).
- 10:14–10:26: 3 pros (mint ✓) / 3 cons (coral ✗), compact (sc27 + sc31).

---

### 🎬 S16 — CONCLUSION
**⏱ 10:26 → 10:48 (22s) · source: sc33 (+ 1 line from sc32)**

**🎤 Voiceover**
> "Elastic Bunch Graph Matching is a symphony of *local signal processing* — wavelets — and *spatial geometry* — graphs.
>
> Although deep learning now wears the crown, EBGM's philosophy of *elastic landmarks* still lives on in modern face-detection architectures.
>
> Local. Elastic. General. Thank you for watching — see you in the next algorithm video!"

**🎨 Visual**
- 10:26–10:40: The graph grid over the face fades; three keywords `LOCAL · ELASTIC · GENERAL` (cyan/lavender/mint) (sc33 + 1 line from sc32).
- 10:40–10:48: Reference list (Wiskott 1997/1999 · Lades 1993 · Daugman 1988 · Turk & Pentland 1991) scrolls gently, fade to black.

---

## ⏱️ PART C — RUNTIME BUDGET

| S | Title | Δ (s) | Cumulative |
|---|---|---|---|
| 1 | Cold open & problem | 24 | 0:24 |
| 2 | Why it's hard | 38 | 1:02 |
| 3 | Pre-deep-learning era ⭐(new) | 50 | 1:52 |
| 4 | The EBGM idea | 44 | 2:36 |
| 5 | Gabor wavelets | 46 | 3:22 |
| 6 | Jet, 40 coefficients | 36 | 3:58 |
| 7 | Comparing jets (Sₐ/S_φ) | 48 | 4:46 |
| 8 | Image graph | 30 | 5:16 |
| 9 | Face Bunch Graph | 44 | 6:00 |
| 10 | Graph similarity function | 32 | 6:32 |
| 11 | Elastic matching, 4 steps ⭐ | 70 | 7:42 |
| 12 | Recognition & ranking | 34 | 8:16 |
| 13 | Data & FERET | 40 | 8:56 |
| 14 | Cross-pose · phase · speed | 50 | 9:46 |
| 15 | Big picture | 40 | 10:26 |
| 16 | Conclusion | 22 | 10:48 |

**Total ≈ 10:48.** To hit exactly **10:00**, trim ~48s: shorten S3 to ~40s (drop one minor point), S11 to ~60s, S2 to ~33s, S14 to ~45s.

---

## 🛠️ PART D — TO PRODUCE THE 10-MINUTE CUT
1. **Build NEW scene S3** (`scene_03b_pre_deeplearning.py`): per the new storyboard (CNN → rewind → IEEE PAMI 1997 paper → EBGM name). Do not reuse sc04/05.
2. **Keep & trim:** for the 15 remaining source scenes, cut `self.wait()`/`run_time` to match the Δ column. In particular sc20/21/22 currently carry 35–37s of total `wait` — cut to ~10–14s.
3. **Merge:** S1 (sc01+02), S13 (sc20+21), S14 (sc22+23+24), S15 (sc27+29+31) — combine classes or build scenes taking only the core.
4. **Remove from the render pipeline:** sc04, sc05, sc07, sc08, sc19, sc25, sc26, sc28, sc30, sc32 (keep the files; just exclude from the final cut).
5. **Fix the S13 figure labels** to the correct pose pairs (98/84/57/18) — avoid misattributing 57% to cross-pose.
6. **Add analogy captions** (`≈ CNN filter` in S5) to match the VO.
7. **Record VO** per Part B (~150 wpm, tech-storytelling delivery); sync animation to VO.
8. **Stitch** via `scene_full_video.py` in S1→S16 order.

---
# END — EBGM SCRIPT (10-MINUTE CUT — FINAL) 🚀
