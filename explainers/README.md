# Explainers

Previews use a placeholder figure, not real footage.

```bash
python -m reelkit.apply explainers checklist --video raw.mp4 --params '{"start": 1, "end": 8, "items": ["Remove clutter", "Sort", "Highlight", "Title"], "ticks": [2, 3.5, 5, 6.5]}' -o out.mp4
```

| Style | What it does | Preview |
|---|---|---|
| `checklist` | Card next to your head; items appear and tick green on cue | <img src="previews/checklist.gif" width="160"> |
