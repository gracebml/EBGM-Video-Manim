from __future__ import annotations

import csv
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "media" / "videos"
OUT_DIR = ROOT / "release"
FULL_OUT = OUT_DIR / "EBGM_EN_full.mp4"
CONCAT_LIST = OUT_DIR / "concat_list.txt"
REPORT = OUT_DIR / "durations_report.csv"
TRANSCRIPT = ROOT / "audio" / "en" / "transcript.json"


SCENES = [
    ("S01", "scene_01", MEDIA / "scene_S01_cold_open" / "480p15" / "S01_ColdOpen.mp4"),
    ("S02", "scene_02", MEDIA / "scene_S02_why_hard" / "480p15" / "S02_WhyHard.mp4"),
    ("S03", "scene_03", MEDIA / "scene_S03_pre_deeplearning" / "480p15" / "S03_PreDL.mp4"),
    ("S04", "scene_04", MEDIA / "scene_S04_idea" / "480p15" / "S04_Idea.mp4"),
    ("S05", "scene_05", MEDIA / "scene_S05_gabor" / "480p15" / "S05_Gabor.mp4"),
    ("S06", "scene_06", MEDIA / "scene_S06_jet" / "480p15" / "S06_Jet.mp4"),
    ("S07", "scene_07", MEDIA / "scene_S07_similarity" / "480p15" / "S07_Similarity.mp4"),
    ("S08", "scene_08", MEDIA / "scene_S08_image_graph" / "480p15" / "S08_ImageGraph.mp4"),
    ("S09", "scene_09", MEDIA / "scene_S09_bunch_graph" / "480p15" / "S09_BunchGraph.mp4"),
    ("S10", "scene_10", MEDIA / "scene_S10_graph_sim" / "480p15" / "S10_GraphSim.mp4"),
    ("S11", "scene_11", MEDIA / "scene_S11_elastic" / "480p15" / "S11_Elastic.mp4"),
    ("S12", "scene_12", MEDIA / "scene_S12_recognition" / "480p15" / "S12_Recognition.mp4"),
    ("S13", "scene_13", MEDIA / "scene_S13_feret" / "480p15" / "S13_Feret.mp4"),
    ("S14", "scene_14", MEDIA / "scene_S14_phase_speed" / "480p15" / "S14_PhaseSpeed.mp4"),
    ("S15", "scene_15", MEDIA / "scene_S15_big_picture" / "480p15" / "S15_BigPicture.mp4"),
    ("S16", "scene_16", MEDIA / "scene_S16_conclusion" / "480p15" / "S16_Conclusion.mp4"),
]


def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True).strip()


def ffprobe_duration(path: Path) -> float:
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]))


def main() -> None:
    timing = {s["scene"]: float(s["duration"]) for s in json.loads(TRANSCRIPT.read_text(encoding="utf-8"))["scenes"]}

    missing = [str(path) for _, _, path in SCENES if not path.exists()]
    if missing:
        raise SystemExit("Missing rendered mp4 files:\n" + "\n".join(missing))

    rows = []
    for scene_id, scene_key, path in SCENES:
        target = timing[scene_key]
        rendered = ffprobe_duration(path)
        rows.append({
            "scene": scene_id,
            "target_dur": f"{target:.3f}",
            "render_dur": f"{rendered:.6f}",
            "delta": f"{rendered - target:+.6f}",
            "path": str(path.relative_to(ROOT)),
        })

    with REPORT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["scene", "target_dur", "render_dur", "delta", "path"])
        writer.writeheader()
        writer.writerows(rows)

    with CONCAT_LIST.open("w", encoding="utf-8") as f:
        for _, _, path in SCENES:
            f.write(f"file '{path.resolve()}'\n")

    subprocess.check_call([
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(CONCAT_LIST),
        "-c",
        "copy",
        str(FULL_OUT),
    ])

    full_duration = ffprobe_duration(FULL_OUT)
    print(f"wrote {REPORT.relative_to(ROOT)}")
    print(f"wrote {FULL_OUT.relative_to(ROOT)}")
    print(f"full_duration={full_duration:.6f}")


if __name__ == "__main__":
    main()
