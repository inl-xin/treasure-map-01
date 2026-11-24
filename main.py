#!/usr/bin/env python3
"""The Isle of Almost — a treasure map, drawn in code.

make.fun bounty u-ravendell-charm-the-cartographers-a-one-day-00854547
("Charm the Cartographers"). The program draws a parchment treasure
map of an island that does not exist: a hand-drawn-feel coast, a
compass rose, a dashed trail from the harbor to a red X, and seven
labeled places:

  - Mount Procrastination        (the peak that can wait until tomorrow)
  - The Lagoon of Lost Socks     (they went in pairs, they left single)
  - Forest of Forgotten Passwords (every tree a reset link)
  - Harbor of Almost             (every ship nearly sails)
  - Bay of Unread Messages       (99+ and rising)
  - Cape Deadline                (the easternmost point, always looming)
  - X marks the spot

Deterministic: every "random" wobble comes from random.Random with a
fixed seed, so repeat runs write byte-identical PNGs. No network.
Fonts ship in fonts/ so the chart renders the same everywhere.
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024

INK = (74, 52, 32)          # dark brown ink
FAINT_INK = (122, 96, 62)
SEA = (203, 196, 152)       # aged parchment sea
SAND = (233, 214, 158)      # island sand
GRASS = (172, 186, 122)     # island green
COAST = (146, 116, 70)
WATER = (128, 178, 186)     # lagoon blue
RED = (178, 34, 34)

rng = random.Random(20261124)


def font(size, bold=True):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(HERE, "fonts", name), size)


def island_outline(cx, cy, r):
    """A wobbly closed coast from fixed harmonics plus seeded jitter."""
    pts = []
    for i in range(140):
        a = 2 * math.pi * i / 140
        wob = (0.16 * math.sin(3 * a + 1.2) + 0.10 * math.sin(5 * a + 4.0)
               + 0.06 * math.sin(8 * a + 2.1) + rng.uniform(-0.02, 0.02))
        rr = r * (1 + wob)
        pts.append((cx + rr * math.cos(a), cy + 0.88 * rr * math.sin(a)))
    return pts


def label(d, xy, text, size=27, fill=INK, anchor="mm"):
    d.text(xy, text, font=font(size), fill=fill, anchor=anchor,
           stroke_width=2, stroke_fill=(238, 226, 188))


def draw_tree(d, x, y, s):
    d.polygon([(x, y - s), (x - s * 0.55, y + s * 0.4), (x + s * 0.55, y + s * 0.4)],
              fill=(96, 128, 74), outline=INK)
    d.line([(x, y + s * 0.4), (x, y + s * 0.8)], fill=INK, width=3)


def draw_mountain(d, x, y, s):
    d.polygon([(x, y - s), (x - s * 0.8, y + s * 0.6), (x + s * 0.8, y + s * 0.6)],
              fill=(168, 152, 128), outline=INK, width=3)
    d.polygon([(x, y - s), (x - s * 0.28, y - s * 0.35), (x + s * 0.05, y - s * 0.15),
               (x + s * 0.28, y - s * 0.35)], fill=(246, 242, 230), outline=INK)


def dashed_path(d, pts, fill=(120, 72, 40), width=5, dash=16, gap=11):
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        dist = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / dist, (y2 - y1) / dist
        t = 0.0
        while t < dist:
            e = min(t + dash, dist)
            d.line([(x1 + ux * t, y1 + uy * t), (x1 + ux * e, y1 + uy * e)],
                   fill=fill, width=width)
            t += dash + gap


def main():
    img = Image.new("RGB", (W, H), SEA)
    d = ImageDraw.Draw(img)

    # parchment speckle (seeded, so identical every run)
    for _ in range(2600):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        tone = rng.choice([(196, 188, 142), (212, 205, 164), (188, 178, 132)])
        d.point((x, y), fill=tone)

    # gentle wave marks in the sea
    for _ in range(46):
        x, y = rng.uniform(30, W - 70), rng.uniform(30, H - 40)
        d.arc([x, y, x + 34, y + 14], start=200, end=340, fill=FAINT_INK, width=2)

    # island, with a darker offset copy as its "shadow" coast
    coast = island_outline(505, 545, 322)
    d.polygon([(x + 7, y + 9) for x, y in coast], fill=COAST)
    d.polygon(coast, fill=SAND)
    d.line(coast + [coast[0]], fill=INK, width=4)
    inner = island_outline(505, 545, 268)
    d.polygon(inner, fill=GRASS)

    # --- the places -------------------------------------------------
    # The Lagoon of Lost Socks: a blue pond in the north-east
    d.ellipse([612, 318, 726, 392], fill=WATER, outline=INK, width=3)
    d.arc([636, 336, 700, 374], start=20, end=300, fill=(240, 246, 246), width=3)
    label(d, (669, 428), "The Lagoon of Lost Socks", 25)

    # Mount Procrastination: three peaks, north centre
    draw_mountain(d, 470, 320, 58)
    draw_mountain(d, 545, 338, 44)
    draw_mountain(d, 408, 344, 38)
    label(d, (482, 238), "Mount Procrastination", 27)

    # Forest of Forgotten Passwords: a stand of trees, west centre
    for dx, dy, s in [(-38, -22, 30), (0, -38, 36), (40, -18, 30), (-20, 14, 32),
                      (24, 18, 28), (58, 16, 24), (-56, 16, 24)]:
        draw_tree(d, 318 + dx, 486 + dy, s)
    label(d, (318, 566), "Forest of", 25)
    label(d, (318, 594), "Forgotten Passwords", 25)

    # Harbor of Almost: an anchor on the south-west shore
    hx, hy = 268, 706
    d.ellipse([hx - 9, hy - 46, hx + 9, hy - 28], outline=INK, width=4)
    d.line([(hx, hy - 28), (hx, hy + 22)], fill=INK, width=5)
    d.line([(hx - 20, hy - 12), (hx + 20, hy - 12)], fill=INK, width=5)
    d.arc([hx - 30, hy - 6, hx + 30, hy + 44], start=0, end=180, fill=INK, width=5)
    label(d, (268, 790), "Harbor of Almost", 26)

    # Bay of Unread Messages: little envelopes bobbing in the south-east bay
    for ex, ey in [(700, 700), (742, 724), (668, 730)]:
        d.rectangle([ex, ey, ex + 30, ey + 20], fill=(240, 234, 210), outline=INK, width=2)
        d.line([(ex, ey), (ex + 15, ey + 11), (ex + 30, ey)], fill=INK, width=2)
    d.ellipse([742, 690, 762, 710], fill=RED, outline=INK, width=2)
    label(d, (706, 668), "99+", 20, fill=(246, 242, 230))
    label(d, (712, 792), "Bay of Unread Messages", 26)

    # Cape Deadline: the eastern point, with a little clock tower
    cxp, cyp = 806, 512
    d.rectangle([cxp - 12, cyp - 6, cxp + 12, cyp + 34], fill=(196, 164, 110), outline=INK, width=3)
    d.ellipse([cxp - 15, cyp - 36, cxp + 15, cyp - 6], fill=(246, 242, 230), outline=INK, width=3)
    d.line([(cxp, cyp - 21), (cxp, cyp - 30)], fill=INK, width=3)
    d.line([(cxp, cyp - 21), (cxp + 8, cyp - 17)], fill=INK, width=3)
    label(d, (806, 586), "Cape Deadline", 26)

    # --- the trail and the X ---------------------------------------
    dashed_path(d, [(282, 690), (386, 664), (428, 600), (520, 622),
                    (566, 574), (618, 596)])
    xx, yy = 640, 606
    d.line([(xx - 20, yy - 20), (xx + 20, yy + 20)], fill=RED, width=9)
    d.line([(xx - 20, yy + 20), (xx + 20, yy - 20)], fill=RED, width=9)
    label(d, (640, 560), "X marks the spot", 24, fill=RED)

    # a sea serpent for company, north-west sea
    sx, sy = 150, 218
    for i in range(3):
        d.arc([sx + i * 36, sy - (i % 2) * 10, sx + i * 36 + 44, sy + 30 - (i % 2) * 10],
              start=180, end=350, fill=INK, width=4)
    d.ellipse([sx + 112, sy - 26, sx + 130, sy - 8], outline=INK, width=4)
    label(d, (196, 292), "here be deadlines", 20, fill=FAINT_INK)

    # --- compass rose ----------------------------------------------
    px, py = 884, 176
    d.ellipse([px - 56, py - 56, px + 56, py + 56], outline=INK, width=3)
    for ang, ln in [(0, 62), (90, 62), (180, 62), (270, 62),
                    (45, 40), (135, 40), (225, 40), (315, 40)]:
        a = math.radians(ang - 90)
        d.polygon([(px, py),
                   (px + 10 * math.cos(a + 1.35), py + 10 * math.sin(a + 1.35)),
                   (px + ln * math.cos(a), py + ln * math.sin(a)),
                   (px + 10 * math.cos(a - 1.35), py + 10 * math.sin(a - 1.35))],
                  fill=INK if ln == 62 else FAINT_INK)
    label(d, (px, py - 82), "N", 30)

    # --- title, sea name, frame ------------------------------------
    label(d, (400, 66), "The Isle of Almost", 56)
    label(d, (400, 112), "a true & faithful chart of ye land of good intentions",
          21, fill=FAINT_INK)
    label(d, (512, 962), "T H E   S E A   O F   G O O D   I N T E N T I O N S",
          24, fill=FAINT_INK)
    d.rectangle([18, 18, W - 18, H - 18], outline=INK, width=5)
    d.rectangle([30, 30, W - 30, H - 30], outline=FAINT_INK, width=2)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    img.save(path)
    print(f"wrote {path} ({os.path.getsize(path)} bytes)")


if __name__ == "__main__":
    main()
