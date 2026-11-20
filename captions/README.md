# Captions

Previews use a placeholder figure, not real footage.

```bash
python captions/apply.py --video raw.mp4 --segs segs.json --style karaoke --keywords consultant -o out.mp4
```

| Style | What it does | Preview |
|---|---|---|
| `keyword_red` | 3–4 word chunks on your chest, keywords in red (Poppins) | <img src="previews/keyword_red.gif" width="160"> |
| `word_pop` | One big word at a time, pops in | <img src="previews/word_pop.gif" width="160"> |
| `karaoke` | Full line, the spoken word sits on a red pill (Inter Black) | <img src="previews/karaoke.gif" width="160"> |
| `boxed` | Dark text on a white rounded box | <img src="previews/boxed.gif" width="160"> |
| `handwritten` | Marker-style handwriting with a slight tilt (Caveat) | <img src="previews/handwritten.gif" width="160"> |
