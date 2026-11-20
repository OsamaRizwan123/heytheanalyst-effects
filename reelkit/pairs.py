"""'Not this / But this' overlay: before/after chart cards popping over a full-screen talking head,
plus an optional hook caption and an end card ("Comment CHART for the free PDF").

Usage:
  python -m reelkit.pairs configs/not_this_but_this.json            # renders the video
  python -m reelkit.pairs configs/not_this_but_this.json --still 19.2 cover.jpg   # one frame, e.g. for a cover
Config keys: see configs/not_this_but_this.json
Times are when you SAY "not this" / "but this" (find them with reelkit.transcribe).
"""
import argparse, json, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from .style import font_path, clamp, ease, back
from . import sfx as SFX

W, H, FPS = 1080, 1920, 30
RED = (232, 57, 43, 255); GREEN = (46, 158, 91, 255)

def card(im, tw, th, radius=26):
    im = im.resize((tw, th), Image.LANCZOS).convert("RGBA")
    m = Image.new("L", (tw, th), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, tw - 1, th - 1], radius=radius, fill=255); im.putalpha(m)
    pad = 40; sh = Image.new("RGBA", (tw + 2 * pad, th + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([pad, pad + 10, pad + tw, pad + th + 10], radius=radius, fill=(0, 0, 0, 110))
    sh = sh.filter(ImageFilter.GaussianBlur(18)); sh.alpha_composite(im, (pad, pad)); return sh

def fit(path, aspect, crop_top=0.0):
    """Open an image, optionally trim a header band (fraction of height), pad to the card aspect (w/h)."""
    im = Image.open(path).convert("RGB")
    if crop_top: im = im.crop((0, int(im.height * crop_top), im.width, im.height))
    w, h = im.size; target_h = int(w / aspect)
    c = Image.new("RGB", (w, max(h, target_h) if target_h >= h else h), "white")
    if target_h > h: c = Image.new("RGB", (w, target_h), "white"); c.paste(im, (0, (target_h - h) // 2)); return c
    tw = int(h * aspect); c = Image.new("RGB", (tw, h), "white"); c.paste(im, ((tw - w) // 2, 0)); return c

def tag(text, col, kind, font):
    tw = int(ImageDraw.Draw(Image.new("RGBA", (1, 1))).textlength(text, font=font)); w, h = tw + 92, 66
    t = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(t); d.rounded_rectangle([0, 0, w - 1, h - 1], radius=h // 2, fill=col)
    x0, y = 26, h // 2
    if kind == "x": d.line([(x0, y - 11), (x0 + 22, y + 11)], fill="white", width=6); d.line([(x0, y + 11), (x0 + 22, y - 11)], fill="white", width=6)
    else: d.line([(x0, y + 1), (x0 + 8, y + 11), (x0 + 24, y - 11)], fill="white", width=6, joint="curve")
    d.text((x0 + 38, y), text, font=font, fill="white", anchor="lm"); return t

class Overlay:
    def __init__(s, cfg):
        s.c = cfg; L = cfg.get("layout", {})
        s.TW, s.TH = L.get("card_w", 820), L.get("card_h", 615)
        s.pos = [tuple(L.get("top", [130, 300])), tuple(L.get("bottom", [130, 975]))]
        aspect = s.TW / s.TH; crop = L.get("crop_top", 0.0)
        s.pairs = [(card(fit(p["before"], aspect, crop), s.TW, s.TH), card(fit(p["after"], aspect, crop), s.TW, s.TH), p["not_at"], p["but_at"]) for p in cfg["pairs"]]
        s.fb = ImageFont.truetype(font_path("Poppins-Bold.ttf"), 34); s.fc = ImageFont.truetype(font_path("Poppins-Bold.ttf"), 58)
        s.tags = [tag(L.get("not_label", "NOT THIS"), RED, "x", s.fb), tag(L.get("but_label", "BUT THIS"), GREEN, "v", s.fb)]
        e = cfg.get("end_card")
        s.end = (card(Image.open(e["image"]).convert("RGB"), e.get("w", 900), e.get("h", 600)), e) if e else None
    def caption(s, o, text, y, a, hl=()):
        d = ImageDraw.Draw(o); x = (W - d.textlength(text, font=s.fc)) / 2
        for w_ in text.split():
            col = (232, 57, 43, int(255 * a)) if w_.strip(".,!?").lower() in [h.lower() for h in hl] else (255, 255, 255, int(255 * a))
            for dx, dy in [(-3, 0), (3, 0), (0, -3), (0, 3), (-2, -2), (2, 2), (-2, 2), (2, -2)]: d.text((x + dx, y + dy), w_, font=s.fc, fill=(0, 0, 0, int(200 * a)))
            d.text((x, y), w_, font=s.fc, fill=col); x += d.textlength(w_ + " ", font=s.fc)
    def put(s, o, c, cx, cy, a, out, tg=None, th=None):
        vis = min(a, 1.0) * (1 - out); sc = (0.85 + 0.15 * min(a, 1.04)) * (1 - 0.08 * out)
        cw, ch = int(c.width * sc), int(c.height * sc); cc = c.resize((cw, ch), Image.BILINEAR)
        if vis < 0.999: cc.putalpha(cc.getchannel("A").point(lambda p: int(p * vis)))
        o.alpha_composite(cc, (int(cx - cw / 2), int(cy - ch / 2)))
        if tg is not None:
            if vis < 0.999: tg = tg.copy(); tg.putalpha(tg.getchannel("A").point(lambda p: int(p * vis)))
            o.alpha_composite(tg, (int(cx - tg.width / 2), int(cy - th * sc / 2) - 54))
    def frame(s, t):
        o = Image.new("RGBA", (W, H), (0, 0, 0, 0)); hook = s.c.get("hook")
        if hook and t < hook["until"]:
            s.caption(o, hook["text"], hook.get("y", 1450), ease(t / 0.2) * (1 - ease((t - hook["until"] + 0.15) / 0.15)), hook.get("highlight", []))
        end_at = s.end[1]["at"] if s.end else 1e9
        for i, (b, af, n_at, b_at) in enumerate(s.pairs):
            end = s.pairs[i + 1][2] - 0.33 if i + 1 < len(s.pairs) else end_at - 0.3
            if t < n_at - 0.15 or t > end + 0.2: continue
            out = ease((t - end) / 0.17)
            for j, (cimg, t1) in enumerate([(b, n_at - 0.15), (af, b_at - 0.15)]):
                a = back((t - t1) / 0.28)
                if a > 0.03: x, y = s.pos[j]; s.put(o, cimg, x + s.TW / 2, y + s.TH / 2, a, out, s.tags[j], s.TH)
        if s.end and t >= end_at - 0.1:
            c, e = s.end; s.put(o, c, W / 2, e.get("y", 620), back((t - (end_at - 0.1)) / 0.4), 0)
            for k, line in enumerate(e.get("lines", [])):
                s.caption(o, line, e.get("text_y", 1440) + k * 80, ease((t - end_at - 0.3 - 0.7 * k) / 0.3), e.get("highlight", []))
        return o

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("config"); ap.add_argument("--still", nargs=2, metavar=("T", "OUT"))
    a = ap.parse_args(); cfg = json.load(open(a.config)); ov = Overlay(cfg)
    vf = "fps=30,scale=1080:1920,setsar=1" + (",eq=brightness=0.03:contrast=1.06:saturation=1.1" if cfg.get("grade") else "")
    if a.still:
        t = float(a.still[0]); bg = "/tmp/_bg.png"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(t), "-i", cfg["video"], "-frames:v", "1", "-vf", vf, bg], check=True)
        im = Image.open(bg).convert("RGBA"); im.alpha_composite(ov.frame(t)); im.convert("RGB").save(a.still[1], quality=95); print("->", a.still[1]); return
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", cfg["video"]], capture_output=True, text=True).stdout)
    events = []
    for p in cfg["pairs"]: events += [{"t": p["not_at"] - 0.15, "type": "pop_low"}, {"t": p["but_at"] - 0.15, "type": "pop_high"}]
    if cfg.get("end_card"): events.append({"t": cfg["end_card"]["at"], "type": "ding"})
    SFX.save(SFX.render(events, dur), "/tmp/_sfx.wav")
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-i", cfg["video"], "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", "/tmp/_sfx.wav",
        "-filter_complex", f"[0:v]{vf}[bg];[bg][1:v]overlay=0:0:format=auto,format=yuv420p[v];[2:a]volume={cfg.get('sfx_volume', 0.35)},aresample=48000[s];[0:a]aresample=48000[a];[a][s]amix=inputs=2:normalize=0:duration=first[aout]",
        "-map", "[v]", "-map", "[aout]", "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-c:a", "aac", "-b:a", "192k", "-t", str(dur), "-movflags", "+faststart", cfg.get("output", "out.mp4")], stdin=subprocess.PIPE)
    for f in range(int(dur * FPS)):
        p.stdin.write(ov.frame(f / FPS).tobytes())
        if f % 150 == 0: print(f"{f / FPS:.0f}s", end=" ", flush=True)
    p.stdin.close(); p.wait(); print("\n->", cfg.get("output", "out.mp4"))

if __name__ == "__main__": main()
