# Text overlays

Previews use a placeholder figure, not real footage.

```bash
python -m reelkit.apply text-overlays glass_type --video raw.mp4 --params '{"start": 1, "end": 5, "text": "AI does the analysis.\nYou tell the story.", "highlight": ["story."]}' -o out.mp4
```

| Style | What it does | Preview |
|---|---|---|
| `glass_type` | Frosted-glass card where your line types out | <img src="previews/glass_type.gif" width="160"> |
