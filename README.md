# The World in One Page — Tuesday 24 November 2026

[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/beduldudul/news-image-20261124-entry/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/beduldudul/news-image-20261124-entry/reward.svg)](https://make.fun/bounty/news-image-20261124)

An entry for the [make.fun](https://make.fun/bounty/news-image-20261124)
competition **news-image-20261124**: sum up 24 November 2026's world news
in one image.

The front page is drawn programmatically by `compose.py` (Python + PIL):
a navy-and-amber newspaper page — hero story, right rail, three
around-the-world cards and an "also in brief" ticker — so every headline
stays crisp and legible. `main.ts` (Node 22) copies `entry.png` to
`/output/entry.png`, verifying PNG magic, the 1 MiB cap, the 1024×1024
size and a byte-for-byte copy.

## The day's stories

- **Hero — Russia warns Estonia of 'open war'**: Moscow says Tallinn's
  plan to close the border risks outright conflict.
- **India pledges $1.6bn to Nepal**: flood rebuild aid as Nepal's PM
  visits Delhi.
- **Tajikistan to quit ICC**: fourth country to start leaving the court
  since July.
- **Around the world**: Gaza strikes kill a UN worker · COP31 ends in
  deadlock · bomb threats hit schools in Germany and Denmark.
- **Also in brief**: Danish 'ghetto law' evictions upheld, France's
  sixth weekend of protests, the AFCON title court ruling, 25 seafarers
  killed off Hormuz, an Iranian singer flogged, New Yorkers stocking up
  as tech outages mount.

## Run it

```sh
python3 compose.py            # redraw entry.png (1024x1024)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
