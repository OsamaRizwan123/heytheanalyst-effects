"""Add a call-to-action near the end of a video.

  python cta/apply.py --video raw.mp4 --style comment_box --keyword CHART --start 16 --end 19.3 -o out.mp4
  python cta/apply.py --video raw.mp4 --style end_card --image assets/pdf_cover.png --line2 "for the free PDF" --start 16 --end 19.3
"""
import argparse, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from reelkit.fx import run
from styles import STYLES

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--video", required=True); ap.add_argument("--style", default="end_card", choices=list(STYLES))
    ap.add_argument("--start", type=float, required=True); ap.add_argument("--end", type=float, required=True)
    ap.add_argument("--keyword", default="CHART"); ap.add_argument("--handle", default="@heytheanalyst"); ap.add_argument("--image")
    ap.add_argument("--line1", default=""); ap.add_argument("--line2", default=""); ap.add_argument("-o", default="cta.mp4"); a = ap.parse_args()
    run(a.video, STYLES[a.style](a.start, a.end, a.keyword, a.handle, a.image, a.line1, a.line2), a.o); print("->", a.o)
