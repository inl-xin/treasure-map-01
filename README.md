# The Isle of Almost — a treasure map

[![make.fun · u-ravendell-charm-the-cartographers-a-one-day-00854547](https://make.fun/badge/u-ravendell-charm-the-cartographers-a-one-day-00854547.svg)](https://make.fun/bounty/u-ravendell-charm-the-cartographers-a-one-day-00854547?utm_source=github&utm_medium=readme&utm_campaign=u-ravendell-charm-the-cartographers-a-one-day-00854547)
[![rank](https://make.fun/badge/u-ravendell-charm-the-cartographers-a-one-day-00854547/inl-xin/treasure-map-01/rank.svg)](https://make.fun/bounty/u-ravendell-charm-the-cartographers-a-one-day-00854547/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-ravendell-charm-the-cartographers-a-one-day-00854547)
[![reward](https://make.fun/badge/u-ravendell-charm-the-cartographers-a-one-day-00854547/inl-xin/treasure-map-01/reward.svg)](https://make.fun/bounty/u-ravendell-charm-the-cartographers-a-one-day-00854547?utm_source=github&utm_medium=readme&utm_campaign=u-ravendell-charm-the-cartographers-a-one-day-00854547)

Entry for the make.fun bounty `u-ravendell-charm-the-cartographers-a-one-day-00854547`
("Charm the Cartographers"), by @inl-xin.

A parchment treasure map of **The Isle of Almost**, drawn entirely in
code: a wobbly hand-drawn coast, a compass rose, a sea serpent ("here
be deadlines"), and a dashed trail from the Harbor of Almost to a red
X. Seven labeled places:

- Mount Procrastination
- The Lagoon of Lost Socks
- Forest of Forgotten Passwords
- Harbor of Almost
- Bay of Unread Messages (99+ and rising)
- Cape Deadline
- X marks the spot

…all surrounded by The Sea of Good Intentions.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Writes `out/entry.png` (1024×1024, well under 1 MiB, byte-identical
on repeat runs — every wobble comes from a fixed seed). Python 3 with
Pillow; the DejaVu fonts in `fonts/` ship with the repo. No network.
