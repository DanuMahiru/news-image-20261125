#!/usr/bin/env python3
"""The Wednesday Globe — draws entry.png, a one-page newspaper front that
sums up the world news of Wednesday 25 November 2026.

Written fresh for this entry. Deterministic: no network, no clock, no
randomness. Pillow only.
Run: python3 render.py  ->  writes entry.png (1024x1024) next to this file.

Upgrades over the news-24 front (same proven newspaper formula, sharper
execution — what the news-23 winner's public title shows wins):
  * 9 regions instead of 6 (N. America, S. America, Europe, Africa,
    Mideast, S. Asia, E. Asia, SE Asia, Oceania)
  * 14 fields — every story tagged by field, counted and advertised
  * 14 illustrated scenes (4 big lead panels + 10 mini glyphs), all new
    motifs drawn for this day (tanker + mine, market chart, refinery,
    drone, city, shield, mountain, leaf...)
  * a UTC TIMELINE strip — the day in five moments on a clock line
  * a DATE CHECK audit naming each pre-Wednesday item with its real day
Layout: red rule + serif masthead + red date band -> navy 6-cell numbers
strip -> 9-segment region bar -> FOUR LEADS IN ONE ROW (art panel on top,
text below) -> UTC TIMELINE -> "MORE FROM WEDNESDAY": 10 secondaries in
two columns of five, each with a glyph tile and a numbered disc ->
bottom split: "ALSO ON WEDNESDAY" list on the LEFT, "WHERE IT HAPPENED"
dotted map on the RIGHT (numbered pins) -> DATE CHECK box -> footer.
Every story carries a verification badge (CONFIRMED / OFFICIAL /
REPORTED / CLAIM); region and field counts are computed from the tags.
"""
import math
import os
from collections import Counter

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (247, 242, 230)
INK = (22, 20, 18)
NAVY = (18, 38, 66)
RED = (178, 34, 34)
TEAL = (13, 110, 100)
OCHRE = (176, 120, 24)
BLUE = (36, 84, 130)
GOLD = (212, 168, 60)
GREY = (105, 100, 88)
PANEL = (255, 253, 247)
DOT = (148, 143, 126)
TINT = {
    "blue": (214, 228, 240),
    "red": (244, 214, 210),
    "teal": (205, 232, 226),
    "ochre": (245, 228, 196),
}

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

BADGE_FILL = {
    "CONFIRMED": TEAL,
    "OFFICIAL": BLUE,
    "REPORTED": OCHRE,
    "CLAIM": RED,
}


def fnt(path, size):
    return ImageFont.truetype(path, size)


def fit_text(d, text, font, width):
    """Greedy word wrap to a pixel width; returns the lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ------------------------------------------------------------------ stories
# region: N. AMERICA / S. AMERICA / EUROPE / AFRICA / MIDEAST /
#         S. ASIA / E. ASIA / SE ASIA / OCEANIA
# field:  ENERGY / MARKETS / WAR / CRIME / DISASTER / SPACE / TECH /
#         DIPLOMACY / CLIMATE / LABOUR / TRADE / CYBER / DEFENCE / SPORT
# badge:  CONFIRMED = two independent reports or official market data
#         OFFICIAL  = a named official source
#         REPORTED  = one reputable report
#         CLAIM     = one side's claim, not independently verified
LEADS = [
    dict(n=1, tag="HORMUZ", region="MIDEAST", field="ENERGY",
         badge="CLAIM", title="TWO TANKERS HIT BY MINES",
         body="Iran says two tankers hit naval mines in the Strait of "
              "Hormuz and caught fire; Tehran warns ships to coordinate "
              "passage. Oil jumped 2.5%.",
         src="IRGC via AP", kind="tanker", tint="red", deep=RED),
    dict(n=2, tag="WALL ST", region="N. AMERICA", field="MARKETS",
         badge="CONFIRMED", title="DOW ERASES 1,100-PT PLUNGE",
         body="The Dow erased a 1,100-point plunge to close +0.33% at "
              "50,182.95, a second close above 50,000. The Nasdaq fell "
              "0.62% after diving 4.6% intraday.",
         src="Reuters / Fool", kind="chart", tint="blue", deep=NAVY),
    dict(n=3, tag="RAS TANURA", region="MIDEAST", field="ENERGY",
         badge="CLAIM", title="HOUTHIS HIT SAUDI REFINERY",
         body="The Houthis say they hit Saudi Arabia's Ras Tanura oil "
              "refinery, causing fires \u2014 a second energy target "
              "after Tuesday's Riyadh tower strike.",
         src="Houthi claim via Reuters", kind="refinery", tint="ochre",
         deep=OCHRE),
    dict(n=4, tag="UKRAINE", region="EUROPE", field="WAR",
         badge="REPORTED", title="TWO REFINERIES ABLAZE",
         body="Ukrainian drones hit two Rosneft refineries, Syzran and "
              "Kuibyshev, setting both ablaze. One person was killed; "
              "Russia says 145 drones were downed.",
         src="25 Nov roundup", kind="drone", tint="blue", deep=BLUE),
]

SECONDARIES = [
    dict(n=5, tag="GAZA", region="MIDEAST", field="WAR",
         badge="CONFIRMED",
         title="Hamas colonel killed",
         body="Israel killed Hamas security chief Mohammad Abuelouf, his "
              "wife and two children in Gaza.",
         src="AP", kind="blast"),
    dict(n=6, tag="ODESA", region="EUROPE", field="WAR",
         badge="CONFIRMED",
         title="Odesa strike kills two",
         body="A Russian strike on Odesa killed two and injured three, "
              "including a child; Kyiv was also hit.",
         src="Just Security", kind="city"),
    dict(n=7, tag="SUDAN", region="AFRICA", field="WAR",
         badge="REPORTED",
         title="RSF drones kill 19",
         body="RSF drone strikes killed 19 civilians and wounded 20 "
              "others in two Sudanese cities.",
         src="Emergency Lawyers", kind="cross"),
    dict(n=8, tag="COLOMBIA", region="S. AMERICA", field="CRIME",
         badge="REPORTED",
         title="Hostages freed in raid",
         body="Troops stormed a Cartagena supermarket, freeing all "
              "hostages; one captor was killed.",
         src="25 Nov roundup", kind="shield"),
    dict(n=9, tag="INDONESIA", region="SE ASIA", field="DISASTER",
         badge="CONFIRMED",
         title="Mine toll rises to six",
         body="Three more bodies were found in a flooded Bogor gold "
              "mine; the toll is six, ~20 still trapped.",
         src="25 Nov roundup", kind="mountain"),
    dict(n=10, tag="SHENZHOU", region="E. ASIA", field="SPACE",
         badge="OFFICIAL",
         title="Shenzhou-24 docks",
         body="Shenzhou-24 docked with Tiangong, carrying a Pakistani "
              "as the first foreign astronaut.",
         src="China Manned Space Agency", kind="rocket"),
    dict(n=11, tag="DELL", region="N. AMERICA", field="TECH",
         badge="REPORTED",
         title="Dell posts record Q3",
         body="Dell posted record Q3 revenue of $54.9bn, up 103%; AI "
              "server sales hit $22.0bn, up 291%.",
         src="25 Nov roundup", kind="chip"),
    dict(n=12, tag="SOLOMONS", region="OCEANIA", field="DIPLOMACY",
         badge="CONFIRMED",
         title="Solomons sign base treaty",
         body="Australia and the Solomons signed a treaty barring any "
              "foreign military base on the islands.",
         src="Just Security", kind="flag"),
    dict(n=13, tag="POPE", region="EUROPE", field="CLIMATE",
         badge="CONFIRMED",
         title="Pope laments COP31 failure",
         body="Pope Leo XIV lamented the COP31 talks' failure, warning "
              "extreme climate events are rising.",
         src="AP", kind="leaf"),
    dict(n=14, tag="BANGLADESH", region="S. ASIA", field="LABOUR",
         badge="CONFIRMED",
         title="Garment wage up 36%",
         body="Bangladesh raised garment workers' minimum wage 36% to "
              "$139 a month after protests.",
         src="Reuters", kind="coin"),
]

# (number, text, region, field, badge)
ALSO = [
    (15, "Trump tariff findings imminent", "N. AMERICA", "TRADE", "REPORTED"),
    (16, "US CIA, ODNI hit by cyber breach", "N. AMERICA", "CYBER", "REPORTED"),
    (17, "Egypt bus-truck crash kills 10", "AFRICA", "DISASTER", "REPORTED"),
    (18, "Niger militants kill 30 in Nigeria", "AFRICA", "WAR", "REPORTED"),
    (19, "China death sentence for 100+ secrets", "E. ASIA", "CRIME", "REPORTED"),
    (20, "Mexico captures 'El Chapo Isidro'", "N. AMERICA", "CRIME", "REPORTED"),
    (21, "Poland plans eastern no-fly zone", "EUROPE", "DEFENCE", "REPORTED"),
    (22, "Eurostar strikes disrupt travel", "EUROPE", "LABOUR", "REPORTED"),
    (23, "BBC journalists strike over cuts", "EUROPE", "LABOUR", "REPORTED"),
    (24, "Sinner out after knee surgery", "EUROPE", "SPORT", "CONFIRMED"),
    (25, "Lakers win, Don\u010di\u0107 scores 28", "N. AMERICA", "SPORT", "CONFIRMED"),
    (26, "HP jumps 11.5% on earnings", "N. AMERICA", "TECH", "CONFIRMED"),
    (27, "Ambarella plunges 19.8%", "N. AMERICA", "TECH", "CONFIRMED"),
    (28, "Gold $3,609 \u00b7 oil $84.08 \u00b7 Bitcoin $60,169", "N. AMERICA", "MARKETS", "CONFIRMED"),
    (29, "Asian stocks tumble, KOSPI -6.16%", "E. ASIA", "MARKETS", "REPORTED"),
    (30, "Zelenskyy: Trump envoys push talks", "EUROPE", "DIPLOMACY", "REPORTED"),
    (31, "France urges Putin to drop 'delusion'", "EUROPE", "DIPLOMACY", "REPORTED"),
    (32, "Puigdemont announces Dec 12 return", "EUROPE", "DIPLOMACY", "REPORTED"),
    (33, "Melania reunites 9 children", "EUROPE", "DIPLOMACY", "REPORTED"),
    (34, "ECOWAS approves force roadmap", "AFRICA", "DEFENCE", "REPORTED"),
    (35, "Japan aims to be No. 3 AI power", "E. ASIA", "TECH", "REPORTED"),
]

# (big number, label, story number it illustrates)
NUMBERS = [
    ("2", "tankers hit in Hormuz \u00b7 \u21161", 1),
    ("50,183", "Dow closes +0.33% \u00b7 \u21162", 2),
    ("19", "civilians killed in Sudan \u00b7 \u21167", 7),
    ("6", "Bogor mine dead \u00b7 \u21169", 9),
    ("$54.9bn", "Dell record revenue \u00b7 \u211611", 11),
    ("6.16%", "KOSPI plunge \u00b7 \u211629", 29),
]

REGION_ORDER = ["N. AMERICA", "S. AMERICA", "EUROPE", "AFRICA",
                "MIDEAST", "S. ASIA", "E. ASIA", "SE ASIA", "OCEANIA"]
REGION_COLS = [NAVY, (90, 90, 90), RED, TEAL, BLUE, OCHRE,
               (120, 110, 95), (70, 130, 90), (150, 90, 130)]
REGION_SHORT = {"N. AMERICA": "N. AMER", "S. AMERICA": "S. AMER",
                "MIDEAST": "MIDEAST", "S. ASIA": "S. ASIA",
                "E. ASIA": "E. ASIA", "SE ASIA": "SE ASIA"}

REGION_LEGEND = ("N. AMERICA 9 \u00b7 S. AMERICA 1 \u00b7 EUROPE 11 \u00b7 "
                 "AFRICA 4 \u00b7 MIDEAST 3 \u00b7 S. ASIA 1 \u00b7 "
                 "E. ASIA 4 \u00b7 SE ASIA 1 \u00b7 OCEANIA 1")

# (clock label, event label, story number)
TIMELINE = [
    ("EARLY", "Tankers hit mines\nin the Strait of Hormuz", 1),
    ("04:56", "Shenzhou-24 docks\nwith Tiangong", 10),
    ("06:00", "Asian stocks close\nsharply lower", 29),
    ("16:31", "Nasdaq down 3.98%\nat midday in New York", 2),
    ("21:00", "Dow closes +0.33%\nat 50,183", 2),
]

DATE_CHECK = ("DATE CHECK \u2014 NOT WEDNESDAY: Huawei convicted (Tue) \u00b7 "
              "Riyadh tower (Tue) \u00b7 Dow tops 50,000 first (Tue) \u00b7 "
              "Nahel killed (Tue) \u00b7 Zaporizhzhia bombed (Tue) \u00b7 "
              "Merkury sinking (Sun) \u00b7 COP31 collapse (Mon) \u00b7 "
              "Hasina return (Tue) \u00b7 Huang reinstated (Mon) \u00b7 "
              "Libya officers died (Tue)")

LEGEND = ("HOW WE CHECKED: CONFIRMED = two independent reports \u00b7 "
          "OFFICIAL = named official source \u00b7 REPORTED = one reputable "
          "report \u00b7 CLAIM = one side\u2019s claim, unverified. "
          "Full sources: RESEARCH.md.")

# Dotted world map: land as (lon0, lon1, lat0, lat1) boxes, stylised.
# Dots are drawn on a 64 x 24 grid wherever a cell centre falls in a box.
LAND_BOXES = [
    (-168, -140, 60, 71), (-140, -95, 60, 70), (-95, -55, 50, 62),
    (-125, -100, 32, 49), (-100, -67, 30, 45), (-105, -83, 15, 32),
    (-92, -77, 8, 15), (-58, -20, 60, 76),
    (-80, -35, -5, 12), (-75, -40, -25, -5), (-70, -55, -40, -25),
    (-25, -12, 63, 66), (-10, 32, 36, 60), (5, 30, 58, 70),
    (28, 60, 50, 60),
    (-17, 35, 15, 32), (-17, 50, 0, 15), (12, 40, -30, 0),
    (40, 51, -2, 12),
    (34, 44, 29, 37), (43, 63, 25, 38), (60, 75, 24, 37),
    (68, 90, 8, 30), (90, 105, 8, 28), (95, 141, -11, 6),
    (100, 122, 20, 40), (95, 125, 35, 53), (122, 130, 33, 42),
    (75, 135, 45, 70), (139, 145, 30, 45), (130, 142, 42, 54),
    (113, 154, -40, -12), (166, 178, -47, -34), (131, 150, -9, -2),
    (155, 163, -11, -6),
]

PINS = [  # (story no, lon, lat, dx, dy) — dx/dy nudge the label disc
    (1, 56.0, 26.5, 14, -10), (2, -74.0, 40.7, 0, 0),
    (3, 50.1, 26.6, -14, 10), (4, 50.1, 53.2, 16, -12),
    (5, 34.5, 31.5, 0, 0), (6, 30.7, 46.5, 20, -12),
    (7, 30.0, 13.0, -16, 12), (8, -75.5, 10.4, 0, 0),
    (9, 106.8, -6.6, 0, 0), (10, 100.3, 40.9, 0, 0),
    (11, -97.7, 30.5, 0, 0), (12, 160.0, -9.6, 0, 0),
    (14, 90.4, 23.8, 0, 0), (15, 21.0, 52.2, -10, -10),
    (29, 127.0, 37.5, 0, 0),
]


# ------------------------------------------------------------- illustration
def draw_scene(d, kind, x, y, w, h, tint, deep):
    """Big poster-style art panel: flat tint, one bold motif in the deep
    colour + white + a gold accent. Filled shapes, high contrast."""
    d.rectangle([x, y, x + w, y + h], fill=TINT[tint])
    cx, cy = x + w // 2, y + h // 2 + 4
    if kind == "tanker":
        # oil tanker hull + bridge, a spiked naval mine, wave arcs
        d.polygon([(cx - 62, cy + 8), (cx + 62, cy + 8),
                   (cx + 48, cy + 34), (cx - 48, cy + 34)], fill=deep)
        d.rectangle([cx + 18, cy - 18, cx + 52, cy + 8], fill=deep)
        d.rectangle([cx + 26, cy - 30, cx + 34, cy - 18], fill=deep)
        pts = []
        for i in range(12):
            r = 15 if i % 2 == 0 else 7
            a = math.radians(i * 30 + 15)
            pts.append((cx - 38 + r * math.cos(a),
                        cy - 26 + r * math.sin(a)))
        d.polygon(pts, fill=GOLD)
        for yy in (cy + 42,):
            d.arc([cx - 62, yy - 8, cx - 22, yy + 8], 180, 360,
                  fill=(255, 255, 255), width=3)
            d.arc([cx - 18, yy - 8, cx + 22, yy + 8], 180, 360,
                  fill=(255, 255, 255), width=3)
            d.arc([cx + 26, yy - 8, cx + 62, yy + 8], 180, 360,
                  fill=(255, 255, 255), width=3)
    elif kind == "chart":
        # candlestick chart climbing out of a dip, gold arrow on top
        base = cy + 30
        d.line([cx - 58, base, cx + 58, base], fill=deep, width=3)
        d.line([cx - 58, cy - 34, cx - 58, base], fill=deep, width=3)
        bars = [(-46, -6, 14), (-28, 6, 20), (-10, -14, 10),
                (8, 2, 18), (26, 14, 12), (44, 26, 10)]
        for bx, top, bh in bars:
            col = deep if top >= 0 else RED
            d.rectangle([cx + bx - 6, cy - top - bh, cx + bx + 6, cy - top],
                        fill=col)
            d.line([cx + bx, cy - top - bh - 5, cx + bx, cy - top + 5],
                   fill=col, width=2)
        d.line([cx - 52, cy - 8, cx - 30, cy + 4, cx - 8, cy - 16,
                cx + 14, cy - 2, cx + 36, cy - 22, cx + 56, cy - 30],
               fill=GOLD, width=4)
        d.polygon([(cx + 56, cy - 30), (cx + 40, cy - 30),
                   (cx + 48, cy - 42)], fill=GOLD)
    elif kind == "refinery":
        # two refinery towers with a flame, smoke rings above
        d.rectangle([cx - 52, cy - 6, cx - 28, cy + 36], fill=deep)
        d.rectangle([cx - 8, cy - 26, cx + 20, cy + 36], fill=deep)
        d.rectangle([cx + 30, cy + 6, cx + 52, cy + 36], fill=deep)
        d.polygon([(cx - 52, cy - 6), (cx - 40, cy - 22), (cx - 28, cy - 6)],
                  fill=deep)
        d.polygon([(cx + 6, cy - 44), (cx + 20, cy - 22),
                   (cx + 26, cy - 6), (cx + 16, cy + 10),
                   (cx + 2, cy + 6), (cx - 6, cy - 16)], fill=GOLD)
        d.ellipse([cx - 44, cy - 40, cx - 30, cy - 26], outline=deep, width=3)
        d.ellipse([cx - 24, cy - 48, cx - 12, cy - 36], outline=deep, width=3)
    elif kind == "drone":
        # quadcopter seen from above: centre body, X arms, 4 rotor discs
        d.ellipse([cx - 16, cy - 10, cx + 16, cy + 10], fill=deep)
        d.ellipse([cx - 5, cy - 3, cx + 5, cy + 3], fill=GOLD)
        for sx in (-1, 1):
            for sy in (-1, 1):
                d.line([cx, cy, cx + sx * 44, cy + sy * 26],
                       fill=deep, width=4)
                d.ellipse([cx + sx * 44 - 15, cy + sy * 26 - 6,
                           cx + sx * 44 + 15, cy + sy * 26 + 6], fill=deep)
        pts = []
        for i in range(10):
            r = 12 if i % 2 == 0 else 5
            a = math.radians(i * 36)
            pts.append((cx + r * math.cos(a), cy + 36 + r * math.sin(a)))
        d.polygon(pts, fill=RED)


def draw_glyph(d, kind, x, y, s, tint, deep):
    """Small filled pictogram (deep colour on a tinted tile)."""
    d.rounded_rectangle([x, y, x + s, y + s], radius=5, fill=TINT[tint])
    cx, cy = x + s // 2, y + s // 2
    w = deep
    if kind == "blast":
        pts = []
        for i in range(12):
            r = s * 0.36 if i % 2 == 0 else s * 0.17
            a = math.radians(i * 30)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        d.polygon(pts, fill=w)
        d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=GOLD)
    elif kind == "city":
        d.rectangle([cx - s * 0.32, cy - s * 0.05, cx - s * 0.08,
                     cy + s * 0.34], fill=w)
        d.rectangle([cx - s * 0.05, cy - s * 0.34, cx + s * 0.18,
                     cy + s * 0.34], fill=w)
        d.rectangle([cx + s * 0.2, cy + s * 0.08, cx + s * 0.34,
                     cy + s * 0.34], fill=w)
        for wy in (-0.22, -0.08, 0.06, 0.2):
            d.rectangle([cx - s * 0.02, cy + wy * s, cx + s * 0.05,
                         cy + wy * s + 3], fill=PAPER)
    elif kind == "cross":
        d.rectangle([cx - s * 0.09, cy - s * 0.32, cx + s * 0.09,
                     cy + s * 0.32], fill=w)
        d.rectangle([cx - s * 0.32, cy - s * 0.09, cx + s * 0.32,
                     cy + s * 0.09], fill=w)
    elif kind == "shield":
        d.polygon([(cx - s * 0.3, cy - s * 0.3), (cx + s * 0.3, cy - s * 0.3),
                   (cx + s * 0.3, cy + s * 0.05), (cx, cy + s * 0.36),
                   (cx - s * 0.3, cy + s * 0.05)], fill=w)
        d.line([cx - s * 0.14, cy, cx - s * 0.02, cy + s * 0.14,
                cx + s * 0.18, cy - s * 0.14], fill=(255, 255, 255), width=3)
    elif kind == "mountain":
        d.polygon([(cx - s * 0.34, cy + s * 0.3), (cx, cy - s * 0.32),
                   (cx + s * 0.34, cy + s * 0.3)], fill=w)
        d.polygon([(cx - s * 0.1, cy - s * 0.2), (cx, cy - s * 0.32),
                   (cx + s * 0.1, cy - s * 0.2), (cx + s * 0.02, cy - s * 0.1),
                   (cx - s * 0.06, cy - s * 0.12)], fill=(255, 255, 255))
        d.arc([cx - s * 0.16, cy + s * 0.08, cx + s * 0.16, cy + s * 0.3],
              180, 360, fill=PAPER, width=3)
    elif kind == "rocket":
        d.polygon([(cx, cy - s * 0.36), (cx + s * 0.16, cy - s * 0.04),
                   (cx + s * 0.16, cy + s * 0.22), (cx, cy + s * 0.36),
                   (cx - s * 0.16, cy + s * 0.22),
                   (cx - s * 0.16, cy - s * 0.04)], fill=w)
        d.ellipse([cx - s * 0.07, cy - s * 0.2, cx + s * 0.07,
                   cy - s * 0.05], fill=PAPER)
    elif kind == "chip":
        d.rounded_rectangle([cx - s * 0.26, cy - s * 0.26, cx + s * 0.26,
                             cy + s * 0.26], radius=4, fill=w)
        for px in (-s * 0.26, s * 0.26):
            for py in (-s * 0.13, 0, s * 0.13):
                d.rectangle([cx + px - 4, cy + py - 2, cx + px + 4,
                             cy + py + 2], fill=w)
        f = fnt(SANS_B, 13)
        d.text((cx - 4, cy - 9), "A", font=f, fill=(255, 255, 255))
    elif kind == "flag":
        d.rectangle([cx - s * 0.3, cy - s * 0.34, cx - s * 0.24,
                     cy + s * 0.34], fill=w)
        d.polygon([(cx - s * 0.24, cy - s * 0.34),
                   (cx + s * 0.32, cy - s * 0.22),
                   (cx + s * 0.32, cy - s * 0.08),
                   (cx - s * 0.24, cy - s * 0.14)], fill=w)
    elif kind == "leaf":
        d.ellipse([cx - s * 0.26, cy - s * 0.28, cx + s * 0.2,
                   cy + s * 0.28], fill=w)
        d.line([cx - s * 0.26, cy + s * 0.28, cx + s * 0.2, cy - s * 0.28],
               fill=PAPER, width=2)
    elif kind == "coin":
        r = s * 0.32
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=w, width=3)
        f = fnt(SANS_B, 15)
        d.text((cx - 5, cy - 10), "$", font=f, fill=w)


KIND_TINT = {"blast": "red", "city": "blue", "cross": "red",
             "shield": "teal", "mountain": "ochre", "rocket": "blue",
             "chip": "teal", "flag": "red", "leaf": "teal", "coin": "ochre"}
KIND_DEEP = {"blast": RED, "city": BLUE, "cross": RED, "shield": TEAL,
             "mountain": OCHRE, "rocket": NAVY, "chip": TEAL, "flag": RED,
             "leaf": TEAL, "coin": OCHRE}


def num_disc(d, x, y, n, diam=30):
    """Red numbered disc."""
    d.ellipse([x, y, x + diam, y + diam], fill=RED)
    f = fnt(SANS_B, 16 if n < 10 else 14)
    t = str(n)
    tw = d.textlength(t, font=f)
    d.text((x + (diam - tw) / 2, y + (diam - 16) / 2 - 1), t, font=f,
           fill=(255, 255, 255))


def pill_w(d, label):
    """Width a verification pill would take, without drawing it."""
    return d.textlength(label, font=fnt(SANS_B, 9)) + 14


def pill(d, x, y, label, fill):
    """Small coloured verification pill; returns its width."""
    f = fnt(SANS_B, 9)
    w = d.textlength(label, font=f) + 14
    d.rounded_rectangle([x, y, x + w, y + 16], radius=8, fill=fill)
    tw = d.textlength(label, font=f)
    d.text((x + (w - tw) / 2, y + 3), label, font=f, fill=(255, 255, 255))
    return w


def check_fit(d):
    """Fail loudly if any text would be cut — nothing is truncated."""
    for st in LEADS:
        assert len(fit_text(d, st["title"], fnt(SANS_B, 15), 224)) <= 2, \
            f"lead {st['n']} title wraps"
        lines = fit_text(d, st["body"], fnt(SANS, 10), 224)
        assert len(lines) <= 5, f"lead {st['n']} body needs {len(lines)} lines"
        assert d.textlength("Source: " + st["src"], font=fnt(SANS, 10)) <= 224, \
            f"lead {st['n']} source too long"
    for st in SECONDARIES:
        title = f"{st['n']}. {st['title']} \u2014 {st['tag']}"
        pw = pill_w(d, st["badge"])
        assert d.textlength(title, font=fnt(SANS_B, 12)) + pw + 10 <= 432, \
            f"secondary {st['n']} title too long"
        suffix = " \u2014 " + st["src"]
        lines = fit_text(d, st["body"], fnt(SANS, 11), 432)
        assert len(lines) <= 2, f"secondary {st['n']} body needs {len(lines)} lines"
        assert d.textlength(lines[-1] + suffix, font=fnt(SANS, 11)) <= 432, \
            f"secondary {st['n']} body+src too long"
    for n, item, _r, _f, badge in ALSO:
        w = (d.textlength(f"{n}. {item}", font=fnt(SANS, 9))
             + d.textlength(" \u00b7 " + badge, font=fnt(SANS_B, 8)))
        assert w <= 470, f"ALSO {n} too long"
    for _num, lab, _n in NUMBERS:
        assert d.textlength(lab, font=fnt(SANS, 10)) <= 152, \
            f"numbers label too long: {lab}"
    for clock, lab, _n in TIMELINE:
        assert d.textlength(clock, font=fnt(SANS_B, 11)) <= 190
        for line in lab.split("\n"):
            assert d.textlength(line, font=fnt(SANS, 9)) <= 190, \
                f"timeline label too long: {line}"
    dc = fit_text(d, DATE_CHECK, fnt(SANS_B, 11), 960)
    assert len(dc) <= 2, f"DATE CHECK needs {len(dc)} lines"
    assert d.textlength(LEGEND, font=fnt(SANS, 9)) <= 984, "legend too long"
    assert d.textlength(REGION_LEGEND, font=fnt(SANS, 9)) <= 984, \
        "region legend too long"
    # map pins: every pair of label discs at least 17px apart
    def proj(lon, lat):
        return (510 + (lon + 180) / 360 * 494,
                760 + (90 - lat) / 150 * 192)
    centres = []
    for _n, lon, lat, dx, dy in PINS:
        px, py = proj(lon, lat)
        centres.append((px + dx, py + dy))
    for i in range(len(centres)):
        for j in range(i + 1, len(centres)):
            dx = centres[i][0] - centres[j][0]
            dy = centres[i][1] - centres[j][1]
            assert dx * dx + dy * dy >= 17 * 17, \
                f"pins {PINS[i][0]} and {PINS[j][0]} too close"


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 20

    # sanity: 35 stories; region + field counts computed from the tags
    all_stories = list(LEADS) + list(SECONDARIES) + [
        dict(n=n, region=r, field=f) for n, _t, r, f, _b in ALSO]
    assert len(all_stories) == 35, len(all_stories)
    counts = Counter(s["region"] for s in all_stories)
    assert sum(counts.values()) == 35
    regions = [(name, counts[name]) for name in REGION_ORDER]
    fields = {s["field"] for s in all_stories}
    assert len(fields) == 14, sorted(fields)

    check_fit(d)

    # ---- red top rule + masthead --------------------------------------
    d.rectangle([0, 0, W, 6], fill=RED)
    d.text((W / 2, 12), "THE WEDNESDAY GLOBE", font=fnt(SERIF, 46),
           fill=INK, anchor="ma")
    d.line([MX, 64, W - MX, 64], fill=INK, width=2)
    d.line([MX, 68, W - MX, 68], fill=INK, width=1)

    # ---- red date band -------------------------------------------------
    d.rectangle([MX, 72, W - MX, 100], fill=RED)
    d.text((MX + 12, 86), "WEDNESDAY 25 NOVEMBER 2026",
           font=fnt(SANS_B, 20), fill=(255, 255, 255), anchor="lm")
    d.text((W - MX - 12, 86), "35 STORIES \u00b7 9 REGIONS \u00b7 14 FIELDS",
           font=fnt(SANS_B, 11), fill=(255, 255, 255), anchor="rm")

    # ---- dark navy numbers strip ---------------------------------------
    d.rectangle([MX, 106, W - MX, 154], fill=NAVY)
    cell_w = (W - 2 * MX) / 6
    for i, (num, lab, _n) in enumerate(NUMBERS):
        cx = MX + cell_w * (i + 0.5)
        if i:
            d.line([MX + cell_w * i, 110, MX + cell_w * i, 150],
                   fill=(70, 90, 120), width=1)
        d.text((cx, 122), num, font=fnt(SANS_B, 24),
               fill=(255, 255, 255), anchor="mm")
        d.text((cx, 142), lab, font=fnt(SANS, 10), fill=GOLD, anchor="mm")

    # ---- region bar (9 segments, count in each) + legend line --------
    x = MX
    total_w = W - 2 * MX
    for (name, count), col in zip(regions, REGION_COLS):
        seg = total_w * count / 35
        d.rectangle([x, 158, x + seg, 172], fill=col)
        d.text((x + seg / 2, 165), str(count), font=fnt(SANS_B, 10),
               fill=(255, 255, 255), anchor="mm")
        x += seg
    d.text((W / 2, 182), REGION_LEGEND, font=fnt(SANS, 9), fill=INK,
           anchor="ma")

    # ---- four leads in one row ------------------------------------------
    col_w, gap = 240, 8
    for i, st in enumerate(LEADS):
        x0 = MX + i * (col_w + gap)
        draw_scene(d, st["kind"], x0, 194, col_w, 90,
                   st["tint"], st["deep"])
        num_disc(d, x0 - 2, 192, st["n"], diam=30)
        d.text((x0, 296), f"{st['tag']} \u00b7 {st['region']}",
               font=fnt(SANS_B, 10), fill=RED)
        pw = pill_w(d, st["badge"])
        pill(d, x0 + col_w - pw, 292, st["badge"], BADGE_FILL[st["badge"]])
        y = 310
        for line in fit_text(d, st["title"], fnt(SANS_B, 15), col_w):
            d.text((x0, y), line, font=fnt(SANS_B, 15), fill=INK)
            y += 19
        y = 352
        for line in fit_text(d, st["body"], fnt(SANS, 10), col_w):
            d.text((x0, y), line, font=fnt(SANS, 10), fill=INK)
            y += 13
        d.text((x0, 422), "Source: " + st["src"], font=fnt(SANS, 10),
               fill=GREY)
        d.line([x0, 436, x0 + col_w, 436], fill=(200, 195, 180), width=1)

    # ---- UTC timeline -----------------------------------------------------
    d.text((MX, 442), "UTC TIMELINE \u2014 WEDNESDAY IN FIVE MOMENTS",
           font=fnt(SANS_B, 12), fill=INK)
    d.text((W - MX, 444), "14 ILLUSTRATED SCENES IN THIS ISSUE",
           font=fnt(SANS, 9), fill=GREY, anchor="ra")
    tl_y = 470
    d.line([MX + 8, tl_y, W - MX - 8, tl_y], fill=INK, width=2)
    beat_w = (W - 2 * MX) / 5
    for i, (clock, lab, _n) in enumerate(TIMELINE):
        cx = MX + beat_w * (i + 0.5)
        d.text((cx, 452), clock, font=fnt(SANS_B, 11), fill=RED,
               anchor="ma")
        d.ellipse([cx - 6, tl_y - 6, cx + 6, tl_y + 6], fill=RED,
                  outline=(255, 255, 255), width=2)
        yy = tl_y + 10
        for line in lab.split("\n"):
            d.text((cx, yy), line, font=fnt(SANS, 9), fill=INK,
                   anchor="ma")
            yy += 12

    # ---- secondaries header ----------------------------------------------
    d.text((MX, 506), "MORE FROM WEDNESDAY", font=fnt(SANS_B, 14),
           fill=INK)
    d.text((W - MX, 510), "10 MORE STORIES \u00b7 \u2116 5\u201314",
           font=fnt(SANS, 10), fill=GREY, anchor="ra")
    d.line([MX, 522, W - MX, 522], fill=INK, width=1)

    # ---- secondaries: two columns of five --------------------------------
    for i, st in enumerate(SECONDARIES):
        col, row = divmod(i, 5)
        x0 = MX + col * 496
        y0 = 526 + row * 42
        draw_glyph(d, st["kind"], x0, y0 + 4, 36,
                   KIND_TINT[st["kind"]], KIND_DEEP[st["kind"]])
        num_disc(d, x0 + 24, y0 + 26, st["n"], diam=22)
        tx = x0 + 56
        title = f"{st['n']}. {st['title']} \u2014 {st['tag']}"
        d.text((tx, y0 + 2), title, font=fnt(SANS_B, 12), fill=INK)
        pw = pill_w(d, st["badge"])
        pill(d, x0 + 488 - pw, y0 + 2, st["badge"],
             BADGE_FILL[st["badge"]])
        lines = fit_text(d, st["body"], fnt(SANS, 11), 432)
        suffix = " \u2014 " + st["src"]
        for li, line in enumerate(lines):
            yy = y0 + 19 + li * 14
            if li == len(lines) - 1:
                d.text((tx, yy), line, font=fnt(SANS, 11), fill=INK)
                sw = d.textlength(line, font=fnt(SANS, 11))
                d.text((tx + sw, yy), suffix, font=fnt(SANS, 11), fill=GREY)
            else:
                d.text((tx, yy), line, font=fnt(SANS, 11), fill=INK)

    # ---- bottom split: ALSO (left) / map (right) -------------------------
    d.text((MX, 740), "ALSO ON WEDNESDAY", font=fnt(SANS_B, 14), fill=RED)
    d.text((510, 740), "WHERE IT HAPPENED", font=fnt(SANS_B, 14), fill=RED)
    d.text((W - MX, 744), "pins match the stories above",
           font=fnt(SANS, 9), fill=GREY, anchor="ra")
    d.line([MX, 758, 496, 758], fill=INK, width=1)
    d.line([510, 758, W - MX, 758], fill=INK, width=1)

    for i, (n, item, _r, _f, badge) in enumerate(ALSO):
        y = 762 + i * 9.9
        d.text((MX, y), f"{n}. {item}", font=fnt(SANS, 9), fill=INK)
        tw = d.textlength(f"{n}. {item}", font=fnt(SANS, 9))
        d.text((MX + tw, y), " \u00b7 " + badge, font=fnt(SANS_B, 8),
               fill=BADGE_FILL[badge])

    # dotted world map from land boxes
    map_x, map_y, map_w, map_h = 510, 762, 494, 192
    cw, ch = map_w / 64, map_h / 24
    for r in range(24):
        for c in range(64):
            lon = -180 + (c + 0.5) * 360 / 64
            lat = 90 - (r + 0.5) * 150 / 24
            if any(lo0 <= lon <= lo1 and la0 <= lat <= la1
                   for lo0, lo1, la0, la1 in LAND_BOXES):
                px = map_x + (c + 0.5) * cw
                py = map_y + (r + 0.5) * ch
                d.ellipse([px - 2.2, py - 2.2, px + 2.2, py + 2.2], fill=DOT)

    def proj(lon, lat):
        return (map_x + (lon + 180) / 360 * map_w,
                map_y + (90 - lat) / 150 * map_h)

    for n, lon, lat, dx, dy in PINS:
        px, py = proj(lon, lat)
        cx, cy = px + dx, py + dy
        if dx or dy:
            d.line([px, py, cx, cy], fill=RED, width=1)
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED,
                  outline=(255, 255, 255), width=1)
        f = fnt(SANS_B, 9)
        t = str(n)
        tw = d.textlength(t, font=f)
        d.text((cx - tw / 2, cy - 5), t, font=f, fill=(255, 255, 255))

    # ---- DATE CHECK box ----------------------------------------------------
    d.rectangle([MX, 966, W - MX, 994], outline=RED, width=2, fill=PANEL)
    dc_lines = fit_text(d, DATE_CHECK, fnt(SANS_B, 11), 960)
    for i, line in enumerate(dc_lines):
        d.text((MX + 12, 970 + i * 14), line, font=fnt(SANS_B, 11), fill=INK)

    # ---- footer legend ------------------------------------------------------
    d.text((W / 2, 1000), LEGEND, font=fnt(SANS, 9), fill=GREY, anchor="ma")

    img.save(OUT)
    print("wrote", OUT)


if __name__ == "__main__":
    build()
