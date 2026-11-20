---
name: reel
description: Edit an @heytheanalyst reel from a raw talking-head recording - transcribe, cut, captions, sound effects, chart overlays, stacked panel and cover. Use when the user drops a .mov/.mp4 and asks to edit, add effects, sync charts, or make a cover.
---

# Making a reel with reelkit

Style rules (always):
- Brand: white grid panels, navy #0b3d91 / #0b1f4b, red #e8392b, Poppins. Natural, non-hype wording.
- Keep the top ~250px free (Instagram top bar / "Preview") and nothing important below ~1530px (username + caption).
- Never zoom or move the camera on the person's face. Keep the talking head stable.
- Sound effects are quiet (volume 0.35). Keywords in captions are red.
- Data in charts is illustrative; never use employer/confidential data. Blur strangers' faces.

Steps:
1. Transcribe: `python -m reelkit.transcribe raw.mov -o segs.json --models models/` and read the timings.
2. Optional jump cuts: `python -m reelkit.cut raw.mov -o edit.mp4 --keep a-b c-d ...` (it prints the new start times).
3. Pick the format:
   - **Not this / But this** (charts over a full-screen talking head): fill `configs/not_this_but_this.json`
     with the spoken times of "not this" and "but this", then `python -m reelkit.pairs config.json`.
     Cover: `python -m reelkit.pairs config.json --still <t> cover.jpg`.
   - **Panel on top** (animated explainer above the talking head): write a panel script like
     `examples/panels/pareto_panel.py` (1080x1000, steps synced to segs.json), render panel.mp4, then
     `python -m reelkit.captions captions.json -o captions.ass --keywords ...`,
     `python -m reelkit.sfx events.json --duration D -o sfx.wav`,
     `python -m reelkit.stack --panel panel.mp4 --video raw.mov --sfx sfx.wav --captions captions.ass -o reel.mp4`.
4. Check stills at key moments before sending (label overlaps, top-bar area, cut-off text).
