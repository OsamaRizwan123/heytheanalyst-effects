# Looks

Previews use a placeholder figure, not real footage.

```bash
python -m reelkit.apply looks spotlight --video raw.mp4 --params '{"start": 1, "end": 4, "word": "DATA"}' -o out.mp4
```

| Style | What it does | Preview |
|---|---|---|
| `spotlight` | Room goes dark, you stay lit, a glowing word appears behind you (person cut-out) | <img src="previews/spotlight.gif" width="160"> |
