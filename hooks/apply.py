"""Add a hook to the start of a video.

  python hooks/apply.py --video raw.mp4 --style headline_box --line1 "Most charts lie." --line2 "Here's how" --highlight lie --end 2.5 -o out.mp4
backdrop_word puts the word behind you (needs `pip install rembg`, or --masks with m_000.png...).
"""
import argparse, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from reelkit.fx import run
from styles import STYLES

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--video", required=True); ap.add_argument("--style", default="hook_caption", choices=list(STYLES))
    ap.add_argument("--line1", required=True); ap.add_argument("--line2", default=""); ap.add_argument("--highlight", nargs="*", default=[])
    ap.add_argument("--start", type=float, default=0.0); ap.add_argument("--end", type=float, default=2.5); ap.add_argument("--y", type=int)
    ap.add_argument("--masks"); ap.add_argument("-o", default="hooked.mp4"); a = ap.parse_args()
    run(a.video, STYLES[a.style](a.line1, a.line2, a.highlight, a.start, a.end, a.y), a.o, masks=a.masks); print("->", a.o)
