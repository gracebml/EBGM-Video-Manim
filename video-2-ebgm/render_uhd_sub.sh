#!/usr/bin/env bash
set -u
cd "$(dirname "$0")"
source ~/miniconda3/etc/profile.d/conda.sh
conda activate vid
OUT="release/uhd_4k_sub"; mkdir -p "$OUT"
REP="$OUT/report.csv"; echo "scene,status,dur" > "$REP"
SCENES=(
 "scene_S01_cold_open.py:S01_ColdOpen" "scene_S02_why_hard.py:S02_WhyHard"
 "scene_S03_pre_deeplearning.py:S03_PreDL" "scene_S04_idea.py:S04_Idea"
 "scene_S05_gabor.py:S05_Gabor" "scene_S06_jet.py:S06_Jet"
 "scene_S07_similarity.py:S07_Similarity" "scene_S08_image_graph.py:S08_ImageGraph"
 "scene_S09_bunch_graph.py:S09_BunchGraph" "scene_S10_graph_sim.py:S10_GraphSim"
 "scene_S11_elastic.py:S11_Elastic" "scene_S12_recognition.py:S12_Recognition"
 "scene_S13_feret.py:S13_Feret" "scene_S14_phase_speed.py:S14_PhaseSpeed"
 "scene_S15_big_picture.py:S15_BigPicture" "scene_S16_conclusion.py:S16_Conclusion"
)
i=0
for e in "${SCENES[@]}"; do
  i=$((i+1)); f="release/${e%%:*}"; cls="${e##*:}"
  echo "===== [$i/16] $cls @2160p60 $(date +%H:%M:%S) ====="
  if manim -qk --disable_caching "$f" "$cls"; then
    src=$(find media/videos -path "*2160p60/$cls.mp4"|head -1)
    cp -f "$src" "$OUT/$cls.mp4"
    echo "$cls,OK,$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT/$cls.mp4")" >> "$REP"
    echo "[$i/16] DONE $cls"
  else
    echo "$cls,FAIL," >> "$REP"; echo "[$i/16] FAIL $cls"
  fi
done
echo "ALLDONE -> $OUT"
