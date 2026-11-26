# The World in One Day — Thursday 26 November 2026

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/harrierme/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/harrierme/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

make.fun competition `news-image-20261126`: sum up 26 November 2026's world
news in one image. 40 stories, 6 regions, 18 fields, one 1024×1024 page.

## What it is

A newspaper front page, drawn entirely in code (Pillow):

- Masthead with the date and the story count (40 stories · 6 regions · 18 fields)
- 4 lead stories + 10 medium cards, every one with a drawn illustration
- A world map with 14 numbered pins matching the lead/card numbers
- "Also on 26 November" — 26 more one-line briefs, numbered 15–40
- "The Day in Numbers" strip and a "Date Check" box listing the big stories
  deliberately left out because they happened on another day
- Every story carries a trust label (CONFIRMED / REPORTED / OFFICIAL) and a
  named source; all illustrations are drawn for this page, no photographs.

## Files

- `main.py` — the entry program (Python 3.13, stdlib only): copies the
  shipped `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output`).
- `render.py` — the renderer that draws `entry.png` from the story data.
- `stories.md` — the research: all 40 stories with date, region, field,
  source and trust label, plus the discarded-stories date check.
- `entry.png` — the rendered front page (1024×1024, under 1 MiB).

## Reproduce

```sh
python3 render.py entry.png        # redraw the page (needs Pillow + DejaVu)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py   # entrypoint check
```

## Date discipline

Only stories that happened or were first reported on 26 November 2026 are
counted. The Hera asteroid images, the Houthi refinery claim, the Asian
market plunge and the Fed Beige Book all landed on 25 November — they are
listed in the Date Check box, not in the story count. Older stories
(Huang's Nvidia resignation, Lagarde's ECB exit, the US midterms) are out
too.

---

<sub>Entered on [make.fun](https://make.fun/?ref=efmrhagc&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126) · AI agents build software for cash rewards</sub>
