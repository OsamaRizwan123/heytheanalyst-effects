"""Shared engine for overlay effects.

An effect is any object with:
  .frame(t) -> (back_rgba or None, front_rgba or None)   # 1080x1920 layers
  .needs_mask (bool)   # True if 'back' should sit BEHIND the person (cut-out)
  .sfx(duration) -> list of sfx events (optional)
run(video, effect, out) composites: video -> back layer -> person cut-out -> front layer, adds quiet SFX.
"""
import os, subprocess, tempfile, glob, json
from PIL import Image, ImageDraw, ImageFont
from .style import ease, back, clamp
from . import sfx as SFX

W, H, FPS = 1080, 1920, 30
FONTS = os.path.join(os.path.dirname(__file__), "..", "fonts")
RED = (232, 57, 43); NAVY = (11, 61, 145); INK = (28, 36, 51); WHITE = (255, 255, 255); GREEN = (46, 158, 91)

def font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)

def blank(): return Image.new("RGBA", (W, H), (0, 0, 0, 0))

def fade(img, a):
    if a >= 0.999: return img
    img = img.copy(); img.putalpha(img.getchannel("A").point(lambda p: int(p * max(0, a)))); return img

def outlined(d, xy, text, f, fill, outline=(0, 0, 0), w=4, alpha=255, anchor="la"):
    x, y = xy
    for dx in range(-w, w + 1, 2):
        for dy in range(-w, w + 1, 2):
            if dx or dy: d.text((x + dx, y + dy), text, font=f, fill=outline + (int(alpha * 0.85),), anchor=anchor)
    d.text((x, y), text, font=f, fill=fill + (alpha,), anchor=anchor)

def words_from_segments(segs):
    """[[start,end,'some words'],...] -> [[start,end,'word'],...] spread by word length."""
    out = []
    for a, b, text in segs:
        ws = text.split(); tot = sum(len(w) + 1 for w in ws) or 1; t = a
        for w in ws: d = (b - a) * (len(w) + 1) / tot; out.append([round(t, 3), round(t + d, 3), w]); t += d
    return out

def duration(video):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video], capture_output=True, text=True).stdout)

def run(video, effect, out, masks=None, sfx_volume=0.35, dur=None):
    dur = dur or duration(video); tmp = tempfile.mkdtemp()
    mask_at = None
    if getattr(effect, "needs_mask", False):
        if masks:
            mask_at = lambda i: Image.open(os.path.join(masks, f"m_{i:03d}.png")).convert("L")
        else:
            from rembg import remove, new_session
            sess = new_session("u2net_human_seg")
            mask_at = lambda i, fr=None: None  # replaced below per frame
    frames_dir = os.path.join(tmp, "f"); os.makedirs(frames_dir)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", video, "-t", str(dur), "-vf", f"fps={FPS},scale={W}:{H}", os.path.join(frames_dir, "%04d.png")], check=True)
    files = sorted(glob.glob(os.path.join(frames_dir, "*.png")))
    SFX.save(SFX.render(effect.sfx(dur) if hasattr(effect, "sfx") else [], dur), os.path.join(tmp, "s.wav"))
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-i", video, "-i", os.path.join(tmp, "s.wav"), "-filter_complex",
                          f"[2:a]volume={sfx_volume},aresample=48000[s];[1:a]aresample=48000[a];[a][s]amix=inputs=2:normalize=0:duration=first[aout]",
                          "-map", "0:v", "-map", "[aout]", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                          "-c:a", "aac", "-t", str(dur), "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for i, f in enumerate(files):
        t = i / FPS; fr = Image.open(f).convert("RGBA"); bk, fg = effect.frame(t); img = fr
        if bk is not None:
            img = fr.copy(); img.alpha_composite(bk)
            if getattr(effect, "needs_mask", False):
                m = Image.open(os.path.join(masks, f"m_{i:03d}.png")).convert("L") if masks else remove(fr.convert("RGB"), session=sess, only_mask=True).convert("L")
                person = fr.copy(); person.putalpha(m); img.alpha_composite(person)
        if fg is not None: img = img.copy(); img.alpha_composite(fg)
        p.stdin.write(img.convert("RGB").tobytes())
    p.stdin.close(); p.wait(); return out

def preview_gif(video, out_gif, start=0, dur=None, width=360, fps=12):
    """Small looping GIF for READMEs."""
    args = ["ffmpeg", "-loglevel", "error", "-y", "-ss", str(start)] + (["-t", str(dur)] if dur else []) + ["-i", video, "-vf",
            f"fps={fps},scale={width}:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=bayer", out_gif]
    subprocess.run(args, check=True); return out_gif
