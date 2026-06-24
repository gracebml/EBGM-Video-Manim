#!/usr/bin/env python3
"""Build the 16-scene EBGM release cut from rendered scene videos.

This script is intentionally non-destructive: it reads the current rendered
1080p60 MP4 files in media/videos and writes release outputs into
media/release_cut_16_scenes.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MEDIA_VIDEOS = ROOT / "media" / "videos"
OUT_DIR = ROOT / "media" / "release_cut_16_scenes"


SCENES = {
    "01": ("scene_01_title_opening", "Scene1_TitleOpening.mp4"),
    "02": ("scene_02_face_recognition", "Scene2_FaceRecognition.mp4"),
    "03": ("scene_03_core_problem", "Scene3_CoreProblem.mp4"),
    "04": ("scene_04_prior_approaches", "Scene4_PriorApproaches.mp4"),
    "05": ("scene_05_bridge_problem", "Scene5_BridgeProblem.mp4"),
    "06": ("scene_06_ebgm_novel", "Scene6_EBGM_Novel.mp4"),
    "09": ("scene_09_gabor_basics", "Scene9_GaborBasics.mp4"),
    "10": ("scene_10_jet_basics", "Scene10_JetBasics.mp4"),
    "11": ("scene_11_similarity", "Scene11_Similarity.mp4"),
    "12": ("scene_12_individual_graph", "Scene12_IndividualGraph.mp4"),
    "13": ("scene_13_bunch_graph", "Scene13_BunchGraph.mp4"),
    "14": ("scene_14_graph_similarity", "Scene14_GraphSimilarity.mp4"),
    "15": ("scene_15_matching_procedure", "Scene15_MatchingProcedure.mp4"),
    "16": ("scene_16_two_stage_schedule", "Scene16_TwoStageSchedule.mp4"),
    "17": ("scene_17_recognition_stage", "Scene17_RecognitionStage.mp4"),
    "20": ("scene_20_databases", "Scene20_Databases.mp4"),
    "21": ("scene_21_feret_results", "Scene21_FeretResults.mp4"),
    "22": ("scene_22_bochum_results", "Scene22_BochumResults.mp4"),
    "23": ("scene_23_phase_importance", "Scene23_PhaseImportance.mp4"),
    "24": ("scene_24_computational_efficiency", "Scene24_ComputationalEfficiency.mp4"),
    "27": ("scene_27_intro_generality", "Scene27_IntroGenerality.mp4"),
    "28": ("scene_28_vs_preceding", "Scene28_VsPreceding.mp4"),
    "29": ("scene_29_vs_template", "Scene29_VsTemplate.mp4"),
    "31": ("scene_31_pros_cons", "Scene31_ProsCons.mp4"),
    "32": ("scene_32_legacy_future", "Scene32_LegacyFuture.mp4"),
    "33": ("scene_33_conclusion", "Scene33_Conclusion.mp4"),
}


# Durations target a 10:10 release cut. Gop/cat decisions follow
# plan/kich_ban_enhance.md and the table from the production note.
RELEASE_PLAN = [
    {
        "id": "S01",
        "title": "Mo dau va bai toan",
        "target_duration": 22.0,
        "segments": [("01", 0, 8.0), ("02", 0, 14.0)],
    },
    {
        "id": "S02",
        "title": "Vi sao nhan dang khuon mat kho",
        "target_duration": 38.0,
        "segments": [("03", 0, 38.0)],
    },
    {
        "id": "S03",
        "title": "Tien deep learning va cau hoi trung gian",
        "target_duration": 30.0,
        "segments": [("04", 0, 26.0), ("05", 0, 4.0)],
    },
    {
        "id": "S04",
        "title": "Y tuong EBGM",
        "target_duration": 42.0,
        "segments": [("06", 0, 42.0)],
    },
    {
        "id": "S05",
        "title": "Gabor wavelets",
        "target_duration": 45.0,
        "segments": [("09", 0, 45.0)],
    },
    {
        "id": "S06",
        "title": "Jet",
        "target_duration": 35.0,
        "segments": [("10", 0, 35.0)],
    },
    {
        "id": "S07",
        "title": "Similarity va displacement",
        "target_duration": 44.0,
        "segments": [("11", 0, 44.0)],
    },
    {
        "id": "S08",
        "title": "Image graph",
        "target_duration": 30.0,
        "segments": [("12", 0, 30.0)],
    },
    {
        "id": "S09",
        "title": "Face bunch graph",
        "target_duration": 44.0,
        "segments": [("13", 0, 44.0)],
    },
    {
        "id": "S10",
        "title": "Graph similarity",
        "target_duration": 32.0,
        "segments": [("14", 0, 32.0)],
    },
    {
        "id": "S11",
        "title": "Elastic matching",
        "target_duration": 68.0,
        "segments": [("15", 0, 63.0), ("16", 0, 5.0)],
    },
    {
        "id": "S12",
        "title": "Recognition va ranking",
        "target_duration": 34.0,
        "segments": [("17", 0, 34.0)],
    },
    {
        "id": "S13",
        "title": "FERET",
        "target_duration": 40.0,
        "segments": [("20", 0, 8.0), ("21", 0, 32.0)],
    },
    {
        "id": "S14",
        "title": "Cross pose, phase va toc do",
        "target_duration": 48.0,
        "segments": [("22", 0, 10.0), ("23", 0, 33.0), ("24", 0, 5.0)],
    },
    {
        "id": "S15",
        "title": "Buc tranh lon",
        "target_duration": 38.0,
        "segments": [("27", 0, 16.0), ("28", 0, 3.0), ("29", 0, 12.0), ("31", 0, 7.0)],
    },
    {
        "id": "S16",
        "title": "Ket luan",
        "target_duration": 20.0,
        "segments": [("32", 0, 4.0), ("33", 0, 16.0)],
    },
]


def scene_path(scene_id: str) -> Path:
    folder, filename = SCENES[scene_id]
    return MEDIA_VIDEOS / folder / "1080p60" / filename


def run(command: list[str]) -> None:
    subprocess.run(command, check=True)


def render_release_scene(item: dict) -> Path:
    output = OUT_DIR / f"{item['id']}_{slug(item['title'])}.mp4"
    inputs = []
    filters = []
    streams = []

    for index, (scene_id, start, duration) in enumerate(item["segments"]):
        path = scene_path(scene_id)
        if not path.exists():
            raise FileNotFoundError(path)
        inputs.extend(["-i", str(path)])
        filters.append(
            f"[{index}:v]trim=start={start}:duration={duration},"
            f"setpts=PTS-STARTPTS,fps=60,format=yuv420p[v{index}]"
        )
        streams.append(f"[v{index}]")

    filters.append("".join(streams) + f"concat=n={len(streams)}:v=1:a=0[outv]")

    run(
        [
            "ffmpeg",
            "-y",
            *inputs,
            "-filter_complex",
            ";".join(filters),
            "-map",
            "[outv]",
            "-an",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "18",
            "-movflags",
            "+faststart",
            str(output),
        ]
    )
    return output


def slug(text: str) -> str:
    return (
        text.lower()
        .replace(",", "")
        .replace(" ", "_")
        .replace("va", "va")
    )


def probe_duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def write_manifest(outputs: list[Path], full_output: Path) -> None:
    details = []
    for item, output in zip(RELEASE_PLAN, outputs):
        details.append(
            {
                "id": item["id"],
                "title": item["title"],
                "target_duration": item["target_duration"],
                "actual_duration": round(probe_duration(output), 3),
                "output": str(output.relative_to(ROOT)),
                "segments": [
                    {
                        "source_scene": scene_id,
                        "source_file": str(scene_path(scene_id).relative_to(ROOT)),
                        "start": start,
                        "duration": duration,
                    }
                    for scene_id, start, duration in item["segments"]
                ],
            }
        )

    total = round(sum(item["actual_duration"] for item in details), 3)
    manifest = {
        "description": "16-scene EBGM release cut built from 1080p60 renders.",
        "total_duration_seconds": total,
        "total_duration_timecode": seconds_to_timecode(total),
        "full_output": str(full_output.relative_to(ROOT)),
        "full_output_duration_seconds": round(probe_duration(full_output), 3),
        "cut_scenes": ["07", "08", "19", "25", "26", "30"],
        "partial_scene_28_policy": "Only the opening 3 seconds are folded into S15.",
        "scenes": details,
    }
    (OUT_DIR / "release_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def seconds_to_timecode(seconds: float) -> str:
    whole = int(round(seconds))
    minutes, sec = divmod(whole, 60)
    return f"{minutes:02d}:{sec:02d}"


def concat_full_video(outputs: list[Path]) -> Path:
    concat_list = OUT_DIR / "full_release_concat.txt"
    concat_list.write_text(
        "".join(f"file '{output.name}'\n" for output in outputs),
        encoding="utf-8",
    )
    full_output = OUT_DIR / "EBGM_release_16_scenes_full.mp4"
    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_list),
            "-c",
            "copy",
            str(full_output),
        ]
    )
    return full_output


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    outputs = [render_release_scene(item) for item in RELEASE_PLAN]
    full_output = concat_full_video(outputs)
    write_manifest(outputs, full_output)
    print(f"Built {len(outputs)} release scenes")
    print(f"Full output: {full_output}")


if __name__ == "__main__":
    main()
