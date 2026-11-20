"""Pareto-reel layout: an animated panel (1080x1000) on top, your talking head (1080x920) below.

Usage:
  python -m reelkit.stack --panel panel.mp4 --video raw.mov -o reel.mp4 [--sfx sfx.wav] [--captions captions.ass]
                         [--crop-y 520] [--grade] [--sfx-volume 0.35]
--crop-y picks which 920px band of your 1080x1920 video to keep (raise it if your head is cut off).
"""
import argparse, subprocess

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--panel", required=True); ap.add_argument("--video", required=True); ap.add_argument("-o", default="reel.mp4")
    ap.add_argument("--sfx"); ap.add_argument("--captions"); ap.add_argument("--crop-y", type=int, default=520)
    ap.add_argument("--grade", action="store_true"); ap.add_argument("--sfx-volume", type=float, default=0.35)
    a = ap.parse_args()
    grade = ",eq=brightness=0.04:contrast=1.07:saturation=1.12:gamma=1.1,colorbalance=rs=0.03:bs=-0.02" if a.grade else ""
    subs = f",subtitles={a.captions}" if a.captions else ""
    fc = (f"[1:v]fps=30,scale=1080:1920{grade},crop=1080:920:0:{a.crop_y},setsar=1[v];[0:v]setsar=1[p];"
          f"[p][v]vstack=inputs=2{subs},format=yuv420p[out]")
    cmd = ["ffmpeg", "-loglevel", "error", "-y", "-i", a.panel, "-i", a.video]
    if a.sfx:
        cmd += ["-i", a.sfx]
        fc += f";[2:a]volume={a.sfx_volume},aresample=48000[s];[1:a]aresample=48000[a];[a][s]amix=inputs=2:normalize=0:duration=first[aout]"
        amap = "[aout]"
    else: amap = "1:a"
    cmd += ["-filter_complex", fc, "-map", "[out]", "-map", amap, "-c:v", "libx264", "-preset", "slow", "-crf", "17",
            "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", a.o]
    subprocess.run(cmd, check=True); print("->", a.o)

if __name__ == "__main__": main()
