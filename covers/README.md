# Covers

Previews use a placeholder figure, not real footage.

```bash
python covers/make.py big_text --video raw.mp4 --time 1 --line1 "12 charts" --line2 "like a consultant" --highlight consultant -o cover.jpg
```

| Style | What it does | Preview |
|---|---|---|
| `handdrawn_pareto` | Hand-drawn chart cover (covers/handdrawn_pareto.py) | <img src="previews/handdrawn_pareto.jpg" width="160"> |
| `handdrawn_pie_waffle` | Hand-drawn 'not this / but this' cover (covers/handdrawn_pie_waffle.py) | <img src="previews/handdrawn_pie_waffle.jpg" width="160"> |
| `big_text` | Frame of you + dark fade + huge title | <img src="previews/big_text.jpg" width="160"> |
| `card_over_face` | Image card above your head + caption on your chest | <img src="previews/card_over_face.jpg" width="160"> |
| `drawing_plus_face` | Drawing on top, you below, title pill above your head | <img src="previews/drawing_plus_face.jpg" width="160"> |
