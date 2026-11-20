# Calls to action

Previews use a placeholder figure, not real footage.

```bash
python cta/apply.py --video raw.mp4 --style comment_box --keyword CHART --start 16 --end 19.3 -o out.mp4
```

| Style | What it does | Preview |
|---|---|---|
| `end_card` | Your PDF/cover card + 'Comment CHART' | <img src="previews/end_card.gif" width="160"> |
| `comment_box` | Instagram comment field types the keyword and posts it | <img src="previews/comment_box.gif" width="160"> |
| `follow_button` | Profile card, Follow flips to Following | <img src="previews/follow_button.gif" width="160"> |
| `save_prompt` | Bookmark fills in with 'Save this for later' | <img src="previews/save_prompt.gif" width="160"> |
