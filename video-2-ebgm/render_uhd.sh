#!/usr/bin/env bash
set -u
cd "$(dirname "$0")"
source ~/miniconda3/etc/profile.d/conda.sh
conda activate vid

declare -a SCENES=(
  "release/scene_S01_cold_open.py S01_ColdOpen"
  "release/scene_S02_why_hard.py S02_WhyHard"
  "release/scene_S03_pre_deeplearning.py S03_PreDL"
  "release/scene_S04_idea.py S04_Idea"
  "release/scene_S05_gabor.py S05_Gabor"
  "release/scene_S06_jet.py S06_Jet"
  "release/scene_S07_similarity.py S07_Similarity"
  "release/scene_S08_image_graph.py S08_ImageGraph"
  "release/scene_S09_bunch_graph.py S09_BunchGraph"
  "release/scene_S10_graph_sim.py S10_GraphSim"
  "release/scene_S11_elastic.py S11_Elastic"
  "release/scene_S12_recognition.py S12_Recognition"
  "release/scene_S13_feret.py S13_Feret"
  "release/scene_S14_phase_speed.py S14_PhaseSpeed"
  "release/scene_S15_big_picture.py S15_BigPicture"
  "release/scene_S16_conclusion.py S16_Conclusion"
)

OUT="release/uhd_4k"
mkdir -p "$OUT"
REPORT="$OUT/uhd_report.csv"
echo "scene,status,duration_s" > "$REPORT"

i=0
for entry in "${SCENES[@]}"; do
  i=$((i+1))
  set -- $entry
  file="$1"; cls="$2"
  echo "=================================================="
  echo "[$i/16] RENDER $cls @ 2160p60 ($(date +%H:%M:%S))"
  echo "=================================================="
  if manim -qk --disable_caching "$file" "$cls"; then
    src=$(find media/videos -path "*2160p60/$cls.mp4" | head -1)
    if [ -n "$src" ]; then
      cp -f "$src" "$OUT/$cls.mp4"
      dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT/$cls.mp4")
      echo "$cls,OK,$dur" >> "$REPORT"
      echo "[$i/16] DONE $cls  dur=$dur  -> $OUT/$cls.mp4"
    else
      echo "$cls,NO_OUTPUT," >> "$REPORT"
      echo "[$i/16] WARN $cls rendered but mp4 not found"
    fi
  else
    echo "$cls,FAIL," >> "$REPORT"
    echo "[$i/16] FAIL $cls"
  fi
done
echo "ALL DONE -> $OUT  (report: $REPORT)"
