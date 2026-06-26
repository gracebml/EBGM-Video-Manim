#!/usr/bin/env bash
# Render 16 release scene ở HD 1080p60 rồi ghép thành video v1 (audio Jessica đã nhúng qua add_sound).
set -e
cd "$(dirname "$0")"
source /home/mlinh/miniconda3/etc/profile.d/conda.sh; conda activate vid

declare -a SC=(
 "scene_S00_intro.py:S00_Intro"
 "scene_S01_cold_open.py:S01_ColdOpen"
 "scene_S02_why_hard.py:S02_WhyHard"
 "scene_S03_pre_deeplearning.py:S03_PreDL"
 "scene_S04_idea.py:S04_Idea"
 "scene_S05_gabor.py:S05_Gabor"
 "scene_S06_jet.py:S06_Jet"
 "scene_S07_similarity.py:S07_Similarity"
 "scene_S08_image_graph.py:S08_ImageGraph"
 "scene_S09_bunch_graph.py:S09_BunchGraph"
 "scene_S10_graph_sim.py:S10_GraphSim"
 "scene_S11_elastic.py:S11_Elastic"
 "scene_S12_recognition.py:S12_Recognition"
 "scene_S13_feret.py:S13_Feret"
 "scene_S14_phase_speed.py:S14_PhaseSpeed"
 "scene_S15_big_picture.py:S15_BigPicture"
 "scene_S16_conclusion.py:S16_Conclusion"
)

CONCAT="release/concat_hd.txt"; : > "$CONCAT"
for item in "${SC[@]}"; do
  file="release/${item%%:*}"; cls="${item##*:}"
  base="${item%%:*}"; dir="media/videos/${base%.py}/1080p60"
  out="$dir/${cls}.mp4"
  if [ -f "$out" ] && [ "$out" -nt "$file" ]; then
    echo "[skip] $cls (render mới hơn source)"
  else
    echo "[render] $cls ... (source mới / chưa có)"
    manim -qh --disable_caching "$file" "$cls" >/dev/null 2>&1
  fi
  echo "file '$(pwd)/$out'" >> "$CONCAT"
done

echo "=== concat → release/EBGM_EN_v1_HD.mp4 ==="
ffmpeg -y -f concat -safe 0 -i "$CONCAT" -c copy release/EBGM_EN_v1_HD.mp4 2>/dev/null \
  || ffmpeg -y -f concat -safe 0 -i "$CONCAT" -c:v libx264 -preset medium -crf 18 -c:a aac -b:a 192k release/EBGM_EN_v1_HD.mp4 2>/dev/null
echo "DONE: release/EBGM_EN_v1_HD.mp4"
ffprobe -v error -show_entries format=duration:stream=width,height -of default=noprint_wrappers=1 release/EBGM_EN_v1_HD.mp4 2>/dev/null
