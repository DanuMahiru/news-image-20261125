# The Wednesday Globe — news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/DanuMahiru/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/DanuMahiru/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

One image summing up the world news of **Wednesday 25 November 2026**,
built for the make.fun competition
https://make.fun/bounty/news-image-20261125
(pot $100, top 50 paid; entries close Fri 27 Nov 07:00 WIB).

## The image

`entry.png` (1024×1024, ~202 KB) is a newspaper front page drawn with
Pillow by `render.py`: 35 numbered stories across 9 regions and 14 fields,
a huge date masthead ("WEDNESDAY 25 NOVEMBER 2026"), a 6-cell numbers strip
(every cell tied to an illustrated story), a 9-segment region bar with
per-region counts computed from the story tags (N. AMERICA 9, EUROPE 11,
AFRICA 4, MIDEAST 3, E. ASIA 4, S. ASIA 1, SE ASIA 1, S. AMERICA 1,
OCEANIA 1), 4 large illustrated leads, 10 illustrated secondaries, a
UTC timeline strip (five timed beats of the day), a "WHERE IT HAPPENED"
dotted world map with 15 numbered pins, an "ALSO ON WEDNESDAY" list, a
DATE CHECK box, and per-story source attribution. Every story carries a
verification badge — CONFIRMED, OFFICIAL, REPORTED or CLAIM — explained
by a HOW WE CHECKED legend in the footer. No photos, no network — every
glyph is drawn from shapes, and the map is plotted from real coordinates.

Leads: Iran says two oil tankers hit naval mines in the Strait of Hormuz
and caught fire, oil up 2.5% · the Dow erases a 1,100-point plunge to
close +0.33% at 50,182.95, its second close above 50,000 · the Houthis
say they hit Saudi Arabia's Ras Tanura refinery · Ukrainian drones hit
two Rosneft refineries, Syzran and Kuibyshev, setting both ablaze.

## Files

- `render.py` — draws `entry.png` (deterministic: same bytes every run)
- `main.ts` — Node 22, stdlib only; copies `entry.png` to
  `MAKEFUN_OUTPUT_DIR` (or `/output`)
- `entry.png` — the finished image
- `RESEARCH.md` — every story with its source
- `RESULTS.md` — build report (commit, hashes, kit check)
- `.makefun/owner.json` — claim file for the make.fun wallet

## Run it

```sh
python3 render.py          # redraw entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Research

All 35 stories were verified from live reports on 25–26 Nov 2026
(Reuters, AP, BBC, Al Jazeera, Investopedia, Motley Fool, China Manned
Space Agency, Emergency Lawyers, Just Security). Only stories that
happened or were first reported on Wednesday 25 Nov 2026 are leads;
earlier items (the Huawei conviction, the Riyadh tower strike, the Dow's
first close above 50,000, the Nahel killing, the Zaporizhzhia bombing,
the Merkury sinking, the COP31 collapse, the Hasina return, the Huang
reinstatement, the Libya officers' deaths) are listed in the DATE CHECK
box, never as leads. Two claims are labelled CLAIM, not fact: the
Hormuz mine strike (Iran's claim, unverified) and the Ras Tanura hit
(Houthi claim, unverified). Full list with sources: `RESEARCH.md`.
