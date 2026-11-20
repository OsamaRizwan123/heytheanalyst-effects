"""Jump-cut a recording: keep only the listed time ranges and join them.

Usage:
  python -m reelkit.cut raw.mov -o edit.mp4 --keep 0.3-2.35 5.57-6.66 7.71-9.12
Prints where each kept clip starts in the new timeline (use those times for overlays).
"""
import argparse, subprocess

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("video"); ap.add_argument("-o", default="edit.mp4")
    ap.add_argument("--keep", nargs="+", required=True); ap.add_argument("--size", default="1080:1920")
    a = ap.parse_args()
    parts = [tuple(map(float, k.split("-"))) for k in a.keep]; f = []; lab = []; t = 0
    for i, (s, e) in enumerate(parts):
        f.append(f"[0:v]trim={s}:{e},setpts=PTS-STARTPTS,scale={a.size},fps=30[v{i}];"
                 f"[0:a]atrim={s}:{e},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={e - s - 0.03:.3f}:d=0.03[a{i}]")
        lab.append(f"[v{i}][a{i}]"); print(f"clip {i}: {s}-{e}  ->  new start {t:.2f}s"); t += e - s
    fc = ";".join(f) + ";" + "".join(lab) + f"concat=n={len(parts)}:v=1:a=1[v][a]"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", a.video, "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "14", "-c:a", "aac", "-b:a", "192k", a.o], check=True)
    print(f"total {t:.2f}s -> {a.o}")

if __name__ == "__main__": main()
