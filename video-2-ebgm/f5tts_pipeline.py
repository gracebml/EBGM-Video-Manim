"""F5-TTS → giọng mới cho 16 scene, STRETCH về ĐÚNG độ dài George (giữ cao độ).

Ý tưởng (chống khoá giọng):
  - "Khung thời lượng" = độ dài từng scene của George (audio/en/scene_NN.mp3),
    đọc từ audio/en/transcript.json.
  - Sinh giọng mới bằng F5-TTS (clone từ file mẫu của bạn).
  - rubberband-stretch mỗi file về ĐÚNG target (không đổi cao độ) → visual không vỡ.

Chuẩn bị:
  - audio/ref/voice_ref.wav   (5–15s, giọng muốn clone, sạch, không nhạc nền)
  - audio/ref/voice_ref.txt   (chép ĐÚNG câu nói trong file mẫu)

Chạy:  conda run -n f5tts python f5tts_pipeline.py
Output: audio/en_v2/scene_NN.mp3  (đã khớp độ dài George)
        audio/en_v2/_report.csv
"""
import json, subprocess, os, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EN   = ROOT / "audio" / "en"
OUT  = ROOT / "audio" / "en_v2"; OUT.mkdir(parents=True, exist_ok=True)
REF_WAV = ROOT / "audio" / "ref" / "voice_ref.wav"
REF_TXT = ROOT / "audio" / "ref" / "voice_ref.txt"
TOL = 0.05  # sai số giây cho phép

def dur(p):
    return float(subprocess.run(
        ["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)],
        capture_output=True, text=True).stdout.strip() or 0)

def stretch_to(src, target_dur, dst):
    """Rubberband-stretch src về target_dur (giữ pitch). 2 pass cho khít."""
    cur = dur(src)
    tempo = cur / target_dur               # >1 = đọc nhanh hơn (ngắn lại)
    tmp = dst.with_suffix(".tmp.wav")
    subprocess.run(["ffmpeg","-y","-i",str(src),
                    "-filter:a", f"rubberband=tempo={tempo:.6f}",
                    str(tmp)], capture_output=True)
    # fine-tune pass nếu còn lệch
    d2 = dur(tmp)
    if abs(d2 - target_dur) > TOL and d2 > 0:
        t2 = d2 / target_dur
        subprocess.run(["ffmpeg","-y","-i",str(tmp),
                        "-filter:a", f"atempo={t2:.6f}",
                        "-codec:a","libmp3lame","-q:a","2", str(dst)], capture_output=True)
        tmp.unlink(missing_ok=True)
    else:
        subprocess.run(["ffmpeg","-y","-i",str(tmp),
                        "-codec:a","libmp3lame","-q:a","2", str(dst)], capture_output=True)
        tmp.unlink(missing_ok=True)
    return dur(dst), tempo

def main():
    if not REF_WAV.exists() or not REF_TXT.exists():
        sys.exit(f"❌ Thiếu file mẫu:\n  {REF_WAV}\n  {REF_TXT}\nĐặt file rồi chạy lại.")
    ref_text = REF_TXT.read_text().strip()

    import torch
    torch.set_num_threads(int(os.environ.get("NTHREADS", "8")))
    NFE = int(os.environ.get("NFE", "16"))   # 32=chất lượng đầy đủ, 16=nhanh ~2x, 10=draft
    print(f"[config] nfe_step={NFE}  torch_threads={torch.get_num_threads()}")

    from f5_tts.api import F5TTS
    tts = F5TTS()   # mặc định F5TTS_v1_Base; CPU tự fallback

    T = json.load(open(EN / "transcript.json"))
    rows = [("scene","target_dur","raw_dur","final_dur","tempo")]
    for sc in T["scenes"]:
        key = sc["scene"]                      # scene_01
        target = round(sc["duration"], 3)
        gen_text = sc["text"]                  # lời thoại scene (đã đúng nội dung)
        raw = OUT / f"{key}.raw.wav"
        # F5-TTS infer
        tts.infer(ref_file=str(REF_WAV), ref_text=ref_text,
                  gen_text=gen_text, file_wave=str(raw),
                  nfe_step=NFE, cross_fade_duration=0.10)
        raw_d = dur(raw)
        final = OUT / f"{key}.mp3"
        fin_d, tempo = stretch_to(raw, target, final)
        raw.unlink(missing_ok=True)
        rows.append((key, f"{target:.3f}", f"{raw_d:.3f}", f"{fin_d:.3f}", f"{tempo:.3f}"))
        print(f"{key}: target={target:6.2f}  raw={raw_d:6.2f}  final={fin_d:6.2f}  tempo={tempo:.3f}")

    with open(OUT / "_report.csv","w") as f:
        for r in rows: f.write(",".join(map(str,r))+"\n")
    print("\n✅ Xong. Output: audio/en_v2/  (đã khớp độ dài George)")
    print("→ Khuyến nghị: chạy lại whisper trên audio/en_v2 để có transcript_v2.json")
    print("  (độ dài đã khớp George, re-transcribe giúp beat word-level đúng giọng mới)")

if __name__ == "__main__":
    main()
