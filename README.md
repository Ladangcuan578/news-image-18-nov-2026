# 18 November 2026 — World News in One Image

[![news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Ladangcuan578/news-image-18-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/Ladangcuan578/news-image-18-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261118)

Entry for make.fun's [Sum up 18 November's world news in one image](https://make.fun/bounty/news-image-20261118) bounty.

## What it is

One 1024×1024 front-page infographic (`entry.png`, 145 KB) that sums up
Wednesday 18 November 2026, drawn as a newspaper front page: a masthead,
the Gulf strikes as the hero story, six more stories in panels, and a
bottom strip with two more items. Every story is self-explanatory — headline
plus a one-line summary — because the judge reads the image with no news
feed. All facts come from the verified briefing in
`news-18nov-facts.md` (kept beside the repo, not part of the entry).

**Stories on the page**

1. **Gulf escalation (hero):** U.S. jets strike a Revolutionary Guard
   missile site on Qeshm Island; Iran fires drones at Ali Al Salem Air Base
   in Kuwait and targets in Bahrain.
2. **Xi and Putin meet** in Shenzhen at APEC, a day before the first-ever
   trilateral summit with Trump.
3. **Kerch Bridge hit again** — part of its road span falls into the strait.
4. **Peltola wins Alaska** — Democrats take the Senate 56–44.
5. **U.S. loses measles-free status** — 5,412 cases in 2026, 10 deaths.
6. **Ebola in DR Congo passes 11,000 cases** — 5,400+ deaths.
7. **Voyager 1 reaches one light-day** from Earth.
8. **Also:** Nvidia revenue $115.84B (+103%), board rules out bringing back
   Jensen Huang; Category 5 Cyclone Xavier hits the Northern Cook Islands.

## How it is built

- `gen.py` draws the image with PIL and the DejaVu fonts (build machine
  only). Run `python3 gen.py` to re-render `entry.png`.
- `main.ts` (Node 22, standard library only) copies `entry.png` to
  `/output/entry.png` and verifies it is a whole 1024×1024 PNG of at most
  1 MiB. A plain copy is deterministic: two runs write identical bytes.

## Run it locally

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
