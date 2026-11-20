# Data visuals

Previews use a placeholder figure, not real footage.

```bash
python -m reelkit.apply data-visuals number_chart --video raw.mp4 --params '{"start": 2, "end": 6, "value": 42, "label": "Conversion rate"}' -o out.mp4
```

| Style | What it does | Preview |
|---|---|---|
| `number_chart` | White card beside your head: bars grow, a big number counts up | <img src="previews/number_chart.gif" width="160"> |
