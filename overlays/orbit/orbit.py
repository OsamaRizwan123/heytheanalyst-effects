"""Orbit: image cards circle your head, passing BEHIND you at the top and IN FRONT of you at the bottom.

Usage:
  python overlays/orbit/orbit.py --video raw.mp4 --start 3 --end 6 --images "assets/charts/*b_after.png" -o out.mp4
Options:
  --center 590 950   head-ring centre in px (x y) on a 1080x1920 frame. Put y around chin level.
  --radius 450 330   ring size (x y). The bottom of the ring should pass below your chin.
  --masks DIR        use existing person masks m_000.png... instead of computing them with rembg.
Needs: ffmpeg, pillow, numpy, and `pip install rembg` (person cut-out) unless --masks is given.
"""
import argparse, glob, math, os, subprocess, tempfile, sys
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from reelkit import sfx as SFX

def ease(x): x = max(0, min(1, x)); return x * x * (3 - 2 * x)

def make_card(path, cw=165, ch=293):
    im = Image.open(path).convert("RGB"); w, h = im.size; t = cw / ch
    if w / h > t: nw = int(h * t); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else: nh = int(w / t); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    im = im.resize((cw, ch), Image.LANCZOS).convert("RGBA")
    m = Image.new("L", (cw, ch), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, cw - 1, ch - 1], radius=16, fill=255); im.putalpha(m)
    pad = 24; sh = Image.new("RGBA", (cw + 2 * pad, ch + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([pad, pad + 6, pad + cw, pad + ch + 6], radius=16, fill=(0, 0, 0, 120))
    sh = sh.filter(ImageFilter.GaussianBlur(10)); sh.alpha_composite(im, (pad, pad))
    ImageDraw.Draw(sh).rounded_rectangle([pad, pad, pad + cw - 1, pad + ch - 1], radius=16, outline=(255, 255, 255, 230), width=4)
    return sh

def render_frame(fr, mask, t, dur, cards, cx, cy, rx, ry, spin=2.8):
    person = fr.copy(); person.putalpha(mask)
    a = ease(t / 0.45) * (1 - ease((t - (dur - 0.45)) / 0.45)); items = []
    for k, c in enumerate(cards):
        th = 2 * math.pi * k / len(cards) + 2 * math.pi * t / spin; r = 0.55 + 0.45 * a
        x = cx + rx * math.cos(th) * r; y = cy + ry * math.sin(th) * r; depth = math.sin(th)
        sc = (0.8 + 0.25 * (depth + 1) / 2) * (0.4 + 0.6 * a); items.append((depth, x, y, sc, c))
    out = fr.copy()
    for front in (False, True):
        for depth, x, y, sc, c in sorted(items, key=lambda z: z[0]):
            if (depth > 0.15) != front: continue
            cc = c.resize((int(c.width * sc), int(c.height * sc)), Image.BILINEAR)
            if a < 0.999: cc.putalpha(cc.getchannel("A").point(lambda p: int(p * a)))
            out.alpha_composite(cc, (int(x - cc.width / 2), int(y - cc.height / 2)))
        if not front: out.alpha_composite(person)
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--video", required=True); ap.add_argument("-o", default="orbit.mp4")
    ap.add_argument("--start", type=float, required=True); ap.add_argument("--end", type=float, required=True)
    ap.add_argument("--images", required=True); ap.add_argument("--center", type=int, nargs=2, default=[590, 950])
    ap.add_argument("--radius", type=int, nargs=2, default=[450, 330]); ap.add_argument("--masks")
    a = ap.parse_args(); dur = a.end - a.start
    cards = [make_card(p) for p in sorted(glob.glob(a.images))[:8]]
    tmp = tempfile.mkdtemp()
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(a.start), "-t", str(dur), "-i", a.video,
                    "-vf", "fps=30,scale=1080:1920", os.path.join(tmp, "f_%03d.png")], check=True)
    frames = sorted(glob.glob(os.path.join(tmp, "f_*.png")))
    if not a.masks:
        from rembg import remove, new_session
        sess = new_session("u2net_human_seg")
    for i, f in enumerate(frames):
        fr = Image.open(f).convert("RGBA")
        if a.masks: mask = Image.open(os.path.join(a.masks, f"m_{i:03d}.png")).convert("L")
        else: mask = remove(fr.convert("RGB"), session=sess, only_mask=True).convert("L")
        render_frame(fr, mask, i / 30, dur, cards, *a.center, *a.radius).convert("RGB").save(f.replace("f_", "o_"))
    seg = os.path.join(tmp, "seg.mp4")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-framerate", "30", "-i", os.path.join(tmp, "o_%03d.png"),
                    "-c:v", "libx264", "-crf", "14", "-pix_fmt", "yuv420p", seg], check=True)
    total = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.video], capture_output=True, text=True).stdout)
    SFX.save(SFX.render([{"t": a.start, "type": "whoosh", "dur": 0.6}, {"t": a.end - 0.45, "type": "whoosh", "dur": 0.5}], total), os.path.join(tmp, "s.wav"))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", a.video, "-i", seg, "-i", os.path.join(tmp, "s.wav"), "-filter_complex",
        f"[0:v]fps=30,scale=1080:1920[b];[1:v]setpts=PTS-STARTPTS+{a.start}/TB[o];[b][o]overlay=0:0:enable='between(t,{a.start},{a.end - 0.01})':eof_action=pass,format=yuv420p[v];"
        "[2:a]volume=0.35,aresample=48000[s];[0:a]aresample=48000[a];[a][s]amix=inputs=2:normalize=0:duration=first[aout]",
        "-map", "[v]", "-map", "[aout]", "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-c:a", "aac", "-movflags", "+faststart", a.o], check=True)
    print("->", a.o)

if __name__ == "__main__": main()
