# Hooks

Previews use a placeholder figure, not real footage.

```bash
python hooks/apply.py --video raw.mp4 --style red_stamp --line1 MYTH --end 2.5 -o out.mp4
```

| Style | What it does | Preview |
|---|---|---|
| `hook_caption` | Big two-line line on your chest, one red word | <img src="previews/hook_caption.gif" width="160"> |
| `headline_box` | Headline at the top, line 2 in a white box | <img src="previews/headline_box.gif" width="160"> |
| `backdrop_word` | Giant word drops in behind you (person cut-out) | <img src="previews/backdrop_word.gif" width="160"> |
| `red_stamp` | A red stamp slams onto the screen | <img src="previews/red_stamp.gif" width="160"> |
| `typed_question` | A question types itself out in a white card | <img src="previews/typed_question.gif" width="160"> |
