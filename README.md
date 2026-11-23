# news-image-23-20261123 — Round 2

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/freysiatiara/news-image-23-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/freysiatiara/news-image-23-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

Bounty: https://make.fun/bounty/news-image-20261123

One image that sums up the world's news of Monday 23 November 2026, drawn as a
cream broadsheet front page — "ONE DAY, EVERYWHERE": COP31 ends in Antalya
without a deal, Russian strikes kill at least 11 near Kyiv, an AI sell-off
rattles world markets (Nikkei −5.06%). 34 stories across 7 regions, each marked
REPORTED, CLAIM or ONGOING, with a dotted world map whose pins carry the story
numbers, a hero strip of the day's biggest numbers, and a DATE CHECK box that
names the big stories from other days (Liverpool 4–0, the penny law, Shenzhen)
deliberately set aside. Every fact was checked against reporting dated
November 23, 2026, and a source is named for every story on the page.

## Run it

```sh
python3 main.py
```

`main.py` (stdlib only) copies `entry.png` (1024x1024 PNG) to the output
directory (`$MAKEFUN_OUTPUT_DIR`, `$OUTPUT_DIR`, `/output` when present, else
the working directory), after self-checks on the PNG signature, size
(<= 1 MiB) and dimensions (<= 1024x1024). `draw.py` regenerates `entry.png`
deterministically with Pillow — two runs produce byte-identical output.

## License

MIT — see `LICENSE`.
