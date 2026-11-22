# SELF-REVIEW — news-image-20261122 (v3)

Scored against the actual rendered image and the story list, 2026-11-22.

## Score: 96 / 100

| Criterion | Points | Notes |
|---|---|---|
| Content authenticity (25) | 23 | Every story checked against reporting dated Sunday 22 Nov 2026 (AP, Reuters, AFP, CNN, Al Jazeera, BBC, Dawn, Nikkei, Formula 1, UN News). −2: the markets secondary is a Sunday-published wrap of Friday's close (20 Nov), and the Indonesia toll differs by source (36 vs 37 missing); both are framed as reported, not as 22 Nov events. |
| Story count & structure (25) | 25 | 46 stories total: 3 headlines + 9 secondary + 34 briefs. Masthead total ("46 STORIES · 7 REGIONS") matches the actual count. Regions: Middle East, Europe, Asia, North America, Africa, Oceania, Global. Numbers bar, UTC timeline and sources line all present. |
| Layout & readability (20) | 18 | Clean front-page hierarchy, no overflow, no truncation, no overlap in v3. −2: the 5×7 pixel font is chunky at title size and the briefs block is dense (3 columns × 12 rows). |
| Title & information (15) | 15 | "Sunday 22 November 2026", story/region totals, UTC timeline (5 moments), sources line and day statement all present and accurate. |
| Program & submission (15) | 15 | `python3 -P -s main.py` exit 0; two runs byte-identical (sha256 c8f51332…); stdlib only; no network; no external files; main.py has multiple real versions via write + edit. |

## Verification notes
- Headlines: COP31 collapse in Antalya (44 hrs overtime, longest COP ever, first failed COP since 2009 — CNN/AP/UN News, 22 Nov); Iran strikes on Bahrain (2 injured, incl. a Pakistani national — Dawn/AFP, 22 Nov); Russian drone on Dymer block near Kyiv (2 killed, 4 wounded, ~14 feared trapped — AP, 22 Nov).
- F1 Las Vegas GP: Verstappen wins by 0.639s, Piastri 17th → 3rd (race 05:37 UTC, 22 Nov — Formula 1).
- Mexico 'El Chapo Isidro' capture: 11 dead incl. 4 soldiers (AP/Al Jazeera, 21–22 Nov).
- Indonesia factory fire: 3 dead, 36 missing (AP/ET, 22 Nov; one wire says 37 unaccounted for).
- Premier League Saturday results published 22 Nov (Dawn/Malay Mail): Leeds 4–1 Chelsea, Arsenal 2–2 Newcastle, City 1–1 Fulham.

## Stories considered and dropped
- Cyclone Xavier (peaked 17 Nov) — too old for 22 Nov.
- San Francisco record rain (Wednesday 18 Nov) — too old; kept only the 22 Nov king-tide warning.
- Liverpool vs Manchester United live score — match in progress at build time, no final result.
- S&P 500 Friday close as a headline — kept only as a secondary market wrap, framed as the week's rout.

## v4 (final)
- Removed dead code: unused `import sys` and unused `Canvas.ring` method.
- Re-ran grader-style check: exit 0, two runs byte-identical, same sha256
  c8f513324a31513e9e8f4304fa24b11c4327fa1d4085b58183699cc3c8025be2
  (output unchanged, as expected for dead-code removal). Score unchanged: 96/100.

- `python3 -P -s main.py` (read-only repo dir, MAKEFUN_OUTPUT_DIR=temp, no network): exit 0.
- Two runs byte-identical: sha256 c8f513324a31513e9e8f4304fa24b11c4327fa1d4085b58183699cc3c8025be2.
- entry.png: 47,489 bytes, 1024×1024, ≤1 MiB.
