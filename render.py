#!/usr/bin/env python3
"""Render 'The World in One Day' - Thursday 26 November 2026 - as one 1024x1024
PNG newspaper front page. All 40 stories were researched first (see stories.md);
every illustration is drawn here with Pillow, no photos, no network, no fonts
downloaded at run time. Deterministic: same input, same bytes every run.

Round 3 (26 Nov 2026): 22 briefs replaced with individually verified
26 Nov news (old briefs' dates were 4-25 Nov), region count 7 -> 6
(no verified Middle East story on 26 Nov), map pins spread with
leader-lines, numbers label "15% Taiwan tariff rate kept" corrected
to "confident", README updated to final counts."""

import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (26, 26, 26)
FAINT = (90, 84, 74)
RED = (158, 26, 26)
BLUE = (28, 68, 110)
GOLD = (176, 132, 40)
RULE = (120, 110, 96)

FD = "/usr/share/fonts/truetype/dejavu"


def F(size, serif=False, bold=False):
    if serif:
        name = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
    else:
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FD, name), size)


def wrap(d, text, font, width):
    """Greedy word wrap; returns list of lines that fit `width` px."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, font, fill=INK, leading=None, max_lines=None):
    """Draw lines of text; returns y just below the last line drawn."""
    if leading is None:
        leading = font.size + 2
    if max_lines is not None:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- stories
# (num, tag, headline, summary, kind, lat, lon, label)
LEADS = [
    (1, "ASIA-PACIFIC · TRADE · REPORTED",
     "Taiwan confident of keeping 15% US tariff",
     "Taipei says trade deals cap the new US tariff salvo; USTR proposes "
     "20-40% ceilings on 14 economies.",
     "ship", 25.03, 121.56, "15%"),
    (2, "NORTH AMERICA · CULTURE · CONFIRMED",
     "Macy's postpones 100th parade to Saturday",
     "First postponement in the parade's history as a nor'easter bears down; "
     "NBC airs last year's march instead.",
     "parade", 40.71, -74.00, "100th"),
    (3, "ASIA-PACIFIC · ECONOMY · CONFIRMED",
     "Bank of Korea raises base rate 25bp to 3.25%",
     "Tightening resumes after October's pause, as the AI export boom keeps "
     "growth brisk and inflation above target.",
     "bank", 37.56, 126.97, "3.25%"),
    (4, "NORTH AMERICA · LAW · REPORTED",
     "Judge bars FCC from moves threatening ABC licence",
     "Judge says the agency appears to run a retaliatory campaign driven by "
     "President Trump.",
     "tv", 38.90, -77.03, "ABC"),
]

# (num, tag, headline, summary, kind, lat, lon)
CARDS = [
    (5, "ASIA-PACIFIC · TRADE", "Chinese firms gain on Japanese rivals",
     "JETRO survey finds more rivals abroad.", "factory", 35.68, 139.69),
    (6, "ASIA-PACIFIC · MARKETS", "Asia shares bounce as AI rout eases",
     "Nikkei +1.6%, Kospi +1.9% on Thursday.", "bank", 22.32, 114.17),
    (7, "ASIA-PACIFIC · TECH", "Azur Promilia launches in East Asia",
     "Fantasy RPG live in 4 regions today.", "game", 31.23, 121.47),
    (8, "ASIA-PACIFIC · FINANCE", "ANZ dropped from NY Fed FX list",
     "CBA now the only Australian bank on list.", "banknotes", -33.87, 151.21),
    (9, "SOUTH ASIA · CULTURE", "India marks Constitution Day",
     "Constitution adopted on this day in 1949.", "parliament", 28.61, 77.20),
    (10, "EUROPE · SPORT", "Chess: Game 3 today, level 1-1",
     "Gukesh-Sindarov drew twice in Geneva.", "chess", 46.20, 6.14),
    (11, "ASIA-PACIFIC · TRANSPORT", "PIA shifts UK flights to own fleet",
     "Own 777s take over UK routes from today.", "plane", 51.50, -0.12),
    (12, "NORTH AMERICA · CULTURE", "Thanksgiving; markets shut",
     "Banks and post offices close for holiday.", "feast", 41.88, -87.63),
    (13, "EUROPE · SPORT", "Europa League night kicks off",
     "Matchday 5 games start across Europe.", "football", 50.85, 4.35),
    (14, "NORTH AMERICA · MEDIA", "NBC airs 2025 parade rerun",
     "Dog Show at noon; 2026 march on Saturday.", "parade", 40.71, -74.00),
]

# (num, place, headline) - one line each; every line pre-shortened to fit
BRIEFS = [
    (15, "Hanoi", "Vietnam to finish US trade deal soon"),
    (16, "Bogor", "Indonesia mine rescue resumes"),
    (17, "New Delhi", "Uber names Ranjan India chief"),
    (18, "Brussels", "EU leaders open two-day summit"),
    (19, "Detroit", "NFL triple-header on Thanksgiving"),
    (20, "New York", "Some brands sit out Black Friday deals"),
    (21, "Punjab", "Farmers sell stubble, cutting fires"),
    (22, "Charlotte", "Bulls edge Hornets 107-105"),
    (23, "Raleigh", "NC State beats Norfolk St 80-49"),
    (24, "Pyongyang", "Kim hails tactical nuclear push"),
    (25, "London", "BBC-Met Office weather deal live"),
    (26, "London", "UK to publish EU treaties today"),
    (27, "Washington", "Capitals rout Flyers 7-3"),
    (28, "Buffalo", "Sabres top Rangers 5-1"),
    (29, "Boston", "Jets beat Bruins 4-2"),
    (30, "London", "UK to create stalking offence"),
    (31, "Detroit", "Detroit's 100th parade steps off"),
    (32, "Moscow, Idaho", "Pastor wants women's vote repealed"),
    (33, "Bavaria", "Guitar wars over Stratocaster"),
    (34, "Las Vegas", "Players Era semis tip off today"),
    (35, "Paris", "France mainstream faces vote wipeout"),
    (36, "London", "Parents feel pressure to be perfect"),
    (37, "Mogadishu", "Jihadism 'changing shape', BBC finds"),
    (38, "Philadelphia", "LeBron's first 76ers triple-double"),
    (39, "Buenos Aires", "Argentina Senate votes on PASO reform"),
    (40, "New York", "Knicks beat Cavaliers 121-102"),
]

REGIONS = [("NORTH AMERICA", 16), ("SOUTH AMERICA", 1), ("EUROPE", 9),
           ("AFRICA", 1), ("SOUTH ASIA", 3), ("ASIA-PACIFIC", 10)]

# (time UTC, event) - 7 slots, all 26 Nov 2026
UTC_STRIP = [
    ("00:55", "Judge bars FCC moves vs ABC"),
    ("01:00", "Bank of Korea hikes to 3.25%"),
    ("01:16", "Macy's postpones 100th parade"),
    ("02:00", "Azur Promilia launches"),
    ("02:00", "JETRO: Chinese firms gain"),
    ("14:00", "Chess Game 3 starts"),
    ("17:45", "Europa League kicks off"),
]

# 6 big-number cells, all verified 26 Nov 2026
NUMBERS = [("3.25%", "Bank of Korea rate"), ("20%", "top US tariff proposed"),
           ("100th", "Macy's parade (postponed)"),
           ("510", "free pulls, Azur Promilia launch"),
           ("$2.5m", "chess title prize fund"),
           ("15%", "Taiwan confident of keeping 15%")]

# 15 discarded (wrong date) + 2 not yet; every line pre-shortened to fit
DATE_CHECK = [
    "Norway oil licences voided — Thu 13 Nov",
    "Ghana banknotes unveiled — Thu 12 Nov",
    "Kenya last Ebola patient out — Wed 11 Nov",
    "Russia 500k dead, leaked Rosstat — Mon 23 Nov",
    "Hasina plans return 16 Dec — Tue 24 Nov",
    "Sooryavanshi 204 off 53 — Tue 24 Nov",
    "Democrats reach 259 House seats — Tue 24 Nov",
    "UK nuclear veterans win inquiry — Tue 24 Nov",
    "Chen Jining graft probe — Tue 24 Nov",
    "Shenzhou-24 + Pakistan crew — Wed 25 Nov",
    "Colombia hostages freed — Wed 25 Nov",
    "N. Korea expels Swiss envoy — Wed 25 Nov",
    "Bangladesh wage +36% — Wed 25 Nov",
    "Cairo tanker fire kills 31 — Wed 25 Nov",
    "IPL auction: 1,220 players — Wed 25 Nov",
    "Not yet: Black Friday — Fri 27 Nov",
    "Not yet: Macy's 100th parade — Sat 28 Nov",
]

MAP_LEGEND = [
    "1 Taipei · 2 New York · 3 Seoul · 4 Washington · 5 Tokyo · 6 Hong Kong · 7 Shanghai",
    "8 Sydney · 9 New Delhi · 10 Geneva · 11 London · 12 Chicago · 13 Brussels · 14 New York",
]

SOURCES = ("Sources: Reuters, BBC, AP, AFP, FIDE, UEFA, NBC, Nexon, Yostar, "
           "Bank of Korea, USTR, JETRO, NY Fed, Govt of India, PIA, KCNA, NHL, "
           "NCAA.com, USA Today, Bloomberg, Guardian, PA, Independent, "
           "Detroit Free Press, Sportradar. Labels: "
           "CONFIRMED = verified by the named source; REPORTED = as reported; "
           "OFFICIAL = announced by an authority; FORECAST = scheduled. "
           "All illustrations drawn for this page — no photographs.")


# ---------------------------------------------------------------- scenes
# Every illustration is flat vector-style art drawn with Pillow primitives.

def _sky(d, box, top, bottom):
    d.rectangle(box, fill=top)
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0 + (y1 - y0) * 2 // 3, x1, y1], fill=bottom)


def _sun(d, box, cx, cy, r, col=GOLD):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)


def _building(d, x, y, w, h, col, roof=None):
    d.rectangle([x, y, x + w, y + h], fill=col)
    if roof:
        d.polygon([(x - 3, y), (x + w // 2, y - 12), (x + w + 3, y)], fill=roof)


def _windows(d, x, y, w, h, rows=3, cols=4, col=(247, 243, 234)):
    cw, ch = w // cols, h // rows
    for r in range(rows):
        for c in range(cols):
            d.rectangle([x + c * cw + 2, y + r * ch + 2,
                         x + (c + 1) * cw - 2, y + (r + 1) * ch - 2], fill=col)


def scene(kind, w, h):
    """Draw one small flat illustration; returns an Image."""
    img = Image.new("RGB", (w, h), (232, 226, 210))
    d = ImageDraw.Draw(img)
    cx, cy = w // 2, h // 2
    if kind == "ship":
        _sky(d, (0, 0, w, h), (168, 200, 220), (58, 110, 150))
        d.rectangle([8, h - 26, w - 8, h - 12], fill=(30, 40, 56))  # hull
        for i, c in enumerate([(158, 26, 26), (28, 68, 110), (176, 132, 40)]):
            d.rectangle([16 + i * 34, h - 52, 44 + i * 34, h - 26], fill=c)
        # tariff ceilings on the containers: 20% / 15% / 40% (USTR proposal)
        for i, lab in enumerate(["20%", "15%", "40%"]):
            d.text((30 + i * 34, h - 39), lab, font=F(8, bold=True),
                   fill=(255, 255, 255), anchor="mm")
        d.rectangle([w - 34, h - 66, w - 18, h - 52], fill=(240, 240, 235))  # bridge
        d.line([8, h - 12, w - 8, h - 12], fill=(247, 243, 234), width=2)
    elif kind == "parade":
        _sky(d, (0, 0, w, h), (150, 190, 220), (120, 140, 160))
        for bx in (6, 34, 62, 90, 118):
            _building(d, bx, h - 46, 22, 46, (90, 96, 110))
            _windows(d, bx + 2, h - 42, 18, 40, 3, 2)
        for (bx, by, c) in [(30, 26, (158, 26, 26)), (76, 18, (28, 68, 110)),
                            (118, 30, (176, 132, 40))]:
            d.ellipse([bx - 15, by - 12, bx + 15, by + 12], fill=c)
            d.line([bx, by + 12, bx, by + 30], fill=INK, width=1)
        d.ellipse([cx - 12, 52, cx + 12, 74], fill=(240, 240, 235))  # balloon
        d.text((cx, 63), "100", font=F(9, bold=True), fill=RED, anchor="mm")
        d.line([cx, 74, cx, 92], fill=INK, width=1)
    elif kind == "bank":
        _sky(d, (0, 0, w, h), (200, 205, 190), (150, 150, 130))
        d.polygon([(10, 46), (cx, 18), (w - 10, 46)], fill=(120, 60, 50))
        d.rectangle([16, 46, w - 16, 52], fill=(90, 84, 74))
        for i in range(4):
            d.rectangle([22 + i * 30, 52, 34 + i * 30, h - 14], fill=(240, 240, 235))
        d.rectangle([16, h - 14, w - 16, h - 8], fill=(90, 84, 74))
        d.text((cx, 56), "%", font=F(26, bold=True), fill=RED, anchor="mt")
        # rising rate line above the roof (hike to 3.25%)
        d.line([(8, 18), (18, 14), (28, 10), (38, 6)], fill=RED, width=2)
        d.line([(38, 6), (32, 5)], fill=RED, width=2)
        d.line([(38, 6), (36, 12)], fill=RED, width=2)
    elif kind == "tv":
        _sky(d, (0, 0, w, h), (190, 195, 205), (140, 145, 155))
        d.rectangle([18, 30, w - 18, h - 34], fill=(30, 40, 56))
        d.rectangle([26, 38, w - 26, h - 42], fill=(150, 200, 220))
        d.text((cx, 44), "ABC", font=F(22, bold=True), fill=(26, 26, 26), anchor="mt")
        d.line([cx - 20, h - 34, cx - 34, 14], fill=INK, width=2)
        d.line([cx + 20, h - 34, cx + 34, 14], fill=INK, width=2)
        d.ellipse([cx - 34, 8, cx - 28, 14], fill=RED)
        d.ellipse([cx + 28, 8, cx + 34, 14], fill=RED)
    elif kind == "factory":
        _sky(d, (0, 0, w, h), (200, 200, 190), (140, 140, 130))
        d.rectangle([16, h - 52, w - 40, h - 10], fill=(110, 100, 90))
        d.polygon([(16, h - 52), (36, h - 70), (56, h - 52)], fill=(90, 80, 70))
        d.polygon([(56, h - 52), (76, h - 70), (96, h - 52)], fill=(90, 80, 70))
        d.rectangle([w - 36, 22, w - 22, h - 10], fill=(90, 84, 74))
        for (sx, sy, r) in [(w - 29, 14, 5), (w - 33, 6, 4), (w - 25, 2, 3)]:
            d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(220, 220, 210))
        _windows(d, 22, h - 46, w - 68, 30, 2, 5)
    elif kind == "banknotes":
        _sky(d, (0, 0, w, h), (190, 200, 180), (140, 145, 130))
        for i, c in enumerate([(176, 132, 40), (28, 110, 80), (120, 90, 140)]):
            y = 24 + i * 26
            d.rectangle([16, y, w - 16, y + 22], fill=c)
            d.ellipse([cx - 9, y + 4, cx + 9, y + 18], fill=(247, 243, 234))
            d.text((cx, y + 6), "$", font=F(12, bold=True), fill=INK, anchor="mt")
    elif kind == "parliament":
        _sky(d, (0, 0, w, h), (190, 200, 215), (150, 155, 150))
        d.ellipse([cx - 26, 18, cx + 26, 52], fill=(120, 90, 70))
        d.rectangle([16, 52, w - 16, 58], fill=(90, 84, 74))
        for i in range(5):
            d.rectangle([22 + i * 26, 58, 32 + i * 26, h - 12], fill=(240, 240, 235))
        d.rectangle([16, h - 12, w - 16, h - 6], fill=(90, 84, 74))
        d.rectangle([cx - 8, 66, cx + 8, h - 12], fill=(120, 60, 50))
    elif kind == "game":
        # Kibo creature companion (Azur Promilia): round body, ears, stars
        _sky(d, (0, 0, w, h), (140, 170, 220), (90, 120, 170))
        for (sx, sy) in [(18, 18), (120, 14), (128, 52), (12, 58), (70, 10)]:
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(247, 243, 234))
        d.polygon([(cx - 26, 52), (cx - 34, 22), (cx - 12, 40)], fill=(176, 132, 40))
        d.polygon([(cx + 26, 52), (cx + 34, 22), (cx + 12, 40)], fill=(176, 132, 40))
        d.ellipse([cx - 30, 40, cx + 30, 100], fill=(240, 235, 220))
        d.ellipse([cx - 18, 56, cx - 8, 66], fill=(26, 26, 26))
        d.ellipse([cx + 8, 56, cx + 18, 66], fill=(26, 26, 26))
        d.arc([cx - 10, 68, cx + 10, 84], 20, 160, fill=(158, 26, 26), width=2)
        d.ellipse([cx - 4, 92, cx + 4, 100], fill=(28, 110, 80))
    elif kind == "chess":
        _sky(d, (0, 0, w, h), (200, 200, 190), (150, 150, 130))
        sq = 18
        ox, oy = cx - 2 * sq, 20
        for r in range(4):
            for c in range(4):
                col = (240, 240, 235) if (r + c) % 2 == 0 else (60, 60, 60)
                d.rectangle([ox + c * sq, oy + r * sq,
                             ox + (c + 1) * sq, oy + (r + 1) * sq], fill=col)
        d.ellipse([ox + 6, oy + 6, ox + 30, oy + 30], fill=(247, 243, 234),
                  outline=(26, 26, 26), width=2)
        d.text((ox + 18, oy + 8), "K", font=F(13, bold=True), fill=INK, anchor="mt")
        d.ellipse([ox + 42, oy + 42, ox + 66, oy + 66], fill=(26, 26, 26),
                  outline=(247, 243, 234), width=2)
        d.text((ox + 54, oy + 44), "Q", font=F(13, bold=True),
               fill=(247, 243, 234), anchor="mt")
        d.rectangle([ox, oy + 4 * sq, ox + 4 * sq, oy + 4 * sq + 6], fill=(120, 90, 60))
    elif kind == "plane":
        _sky(d, (0, 0, w, h), (150, 190, 220), (120, 140, 160))
        _sun(d, (0, 0, w, h), w - 24, 22, 12)
        d.ellipse([18, 48, w - 18, 78], fill=(240, 240, 235))  # fuselage
        d.polygon([(cx - 10, 62), (cx + 30, 96), (cx + 44, 96), (cx + 14, 62)],
                  fill=(28, 68, 110))  # wing
        d.polygon([(w - 34, 50), (w - 14, 34), (w - 10, 50)], fill=(158, 26, 26))
        for wx in (34, 52, 70):
            d.ellipse([wx, 58, wx + 8, 66], fill=(28, 68, 110))
        d.line([18, 66, w - 18, 66], fill=(158, 26, 26), width=2)
    elif kind == "feast":
        _sky(d, (0, 0, w, h), (210, 190, 160), (150, 130, 110))
        d.rectangle([10, h - 34, w - 10, h - 12], fill=(120, 80, 50))  # table
        d.ellipse([cx - 26, 52, cx + 26, 84], fill=(150, 90, 40))  # turkey
        d.line([cx - 26, 56, cx - 38, 44], fill=(120, 70, 30), width=4)
        d.line([cx + 26, 56, cx + 38, 44], fill=(120, 70, 30), width=4)
        d.ellipse([cx - 8, 46, cx + 8, 58], fill=(200, 150, 80))
        d.ellipse([22, h - 52, 44, h - 34], fill=(240, 240, 235))
        d.ellipse([w - 44, h - 52, w - 22, h - 34], fill=(240, 240, 235))
        d.rectangle([cx - 2, 30, cx + 2, 48], fill=(247, 243, 234))
        d.ellipse([cx - 4, 22, cx + 4, 30], fill=GOLD)
    elif kind == "football":
        _sky(d, (0, 0, w, h), (150, 190, 140), (90, 140, 80))
        d.rectangle([10, 60, w - 10, h - 10], fill=(80, 140, 70))  # pitch
        d.line([cx, 60, cx, h - 10], fill=(247, 243, 234), width=2)
        d.ellipse([cx - 14, 74, cx + 14, 102], outline=(247, 243, 234), width=2)
        d.rectangle([14, 66, 34, 96], outline=(247, 243, 234), width=2)
        d.rectangle([w - 34, 66, w - 14, 96], outline=(247, 243, 234), width=2)
        d.ellipse([cx - 10, 30, cx + 10, 50], fill=(247, 243, 234),
                  outline=(26, 26, 26), width=1)
        d.ellipse([cx - 3, 36, cx + 3, 42], fill=(26, 26, 26))
    else:  # generic globe
        _sky(d, (0, 0, w, h), (150, 190, 220), (60, 110, 150))
        d.ellipse([cx - 34, 14, cx + 34, 82], fill=(90, 160, 110))
        d.ellipse([cx - 34, 14, cx + 34, 82], outline=(240, 240, 235), width=2)
        d.arc([cx - 34, 14, cx + 34, 82], 200, 340, fill=(240, 240, 235), width=2)
        d.line([cx, 14, cx, 82], fill=(240, 240, 235), width=2)
    return img


# ---------------------------------------------------------------- world map
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 80),
     (-75, 72), (-65, 60), (-55, 52), (-60, 47), (-70, 42), (-75, 35),
     (-80, 25), (-85, 30), (-90, 20), (-95, 18), (-100, 16), (-105, 20),
     (-110, 23), (-115, 30), (-125, 40), (-125, 48), (-135, 58), (-150, 60),
     (-165, 60)],
    [(-80, 10), (-75, 5), (-70, 0), (-60, -5), (-50, -5), (-40, -10),
     (-35, -15), (-40, -25), (-50, -30), (-60, -35), (-65, -45), (-70, -52),
     (-73, -40), (-75, -30), (-78, -18), (-80, -8), (-81, 0), (-80, 8)],
    [(-10, 35), (-5, 35), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
     (40, 15), (48, 11), (51, 10), (48, 0), (42, -5), (40, -15), (35, -25),
     (30, -32), (20, -35), (15, -30), (12, -18), (9, -5), (5, 4), (-8, 4),
     (-15, 10), (-17, 20), (-15, 30)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 55), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 59), (28, 60), (30, 62), (32, 60), (30, 55),
     (28, 50), (24, 45), (20, 42), (18, 40), (15, 38), (12, 44), (8, 44),
     (3, 43), (-1, 38), (-6, 36)],
    [(30, 62), (40, 68), (55, 72), (70, 73), (90, 75), (110, 76), (130, 72),
     (150, 70), (170, 66), (178, 65), (170, 60), (162, 55), (158, 50),
     (150, 45), (142, 42), (135, 35), (130, 33), (127, 35), (122, 30),
     (120, 25), (110, 20), (105, 10), (100, 8), (98, 15), (95, 20),
     (90, 22), (85, 20), (80, 15), (77, 8), (75, 15), (70, 22), (65, 25),
     (60, 25), (55, 26), (50, 28), (48, 30), (45, 35), (40, 38), (35, 40),
     (30, 45), (30, 55), (30, 60)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32), (130, -32),
     (135, -35), (140, -38), (145, -38), (150, -37), (153, -32), (150, -25),
     (146, -20), (142, -15), (140, -12), (135, -12), (132, -11), (130, -13),
     (126, -14), (122, -17), (118, -20), (114, -21)],
]


def project(lon, lat, box):
    x0, y0, x1, y1 = box
    px = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
    py = y0 + (90.0 - lat) / 150.0 * (y1 - y0)
    return px, py


def draw_map(d, box, pins, leaders=None):
    """pins: list of (num, lat, lon). leaders: {num: (dx, dy)} px offset with a
    thin leader line, used where two pins would otherwise cover each other."""
    leaders = leaders or {}
    d.rectangle(box, fill=(215, 228, 232))
    d.rectangle(box, outline=RULE, width=1)
    for poly in CONTINENTS:
        pts = [project(lon, lat, box) for lon, lat in poly]
        d.polygon(pts, fill=(226, 216, 190), outline=(140, 128, 104))
    fnum = F(8, bold=True)
    for num, lat, lon in pins:
        px, py = project(lon, lat, box)
        if num in leaders:
            dx, dy = leaders[num]
            d.line([px, py, px + dx, py + dy], fill=RED, width=1)
            px, py = px + dx, py + dy
        r = 7
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=(247, 243, 234), width=1)
        d.text((px, py), str(num), font=fnum, fill=(255, 255, 255),
               anchor="mm")


# ---------------------------------------------------------------- layout
M = 14                      # outer margin
CW = W - 2 * M              # 996 content width


def section_title(d, x, y, text, size=12):
    d.text((x, y), text, font=F(size, bold=True), fill=INK)
    return y + size + 4


def rule(d, y, width=1):
    d.line([(M, y), (W - M, y)], fill=RULE, width=width)


def draw_masthead(d):
    d.text((M, 8), "MAKE.FUN  ·  THURSDAY EDITION  ·  ONE DAY, ONE PAGE",
           font=F(10, bold=True), fill=RED)
    d.text((W - M, 8), "PRICE: ONE DAY'S NEWS", font=F(10, bold=True),
           fill=FAINT, anchor="ra")
    d.text((M, 22), "The World in One Day", font=F(40, serif=True, bold=True),
           fill=INK)
    d.text((W - M, 30), "Thursday, 26 November 2026",
           font=F(19, serif=True, bold=True), fill=INK, anchor="ra")
    d.text((W - M, 54), "40 STORIES  ·  6 REGIONS  ·  18 FIELDS",
           font=F(12, bold=True), fill=RED, anchor="ra")
    rule(d, 84, 2)
    rule(d, 88, 1)


def draw_region_strip(d):
    parts = []
    for name, n in REGIONS:
        parts.append("%s %d" % (name, n))
    txt = "   ·   ".join(parts)
    d.text((W // 2, 94), txt, font=F(11, bold=True), fill=BLUE, anchor="ma")


def draw_utc(d, x, y, w):
    """THE DAY IN UTC: 7 slots, time + event. No box; rules above/below."""
    rule(d, y - 2, 1)
    d.text((x, y + 4), "THE DAY IN UTC", font=F(10, bold=True), fill=INK)
    sw = w // len(UTC_STRIP)
    for i, (t, ev) in enumerate(UTC_STRIP):
        sx = x + i * sw
        d.text((sx + 2, y + 18), t, font=F(9, bold=True), fill=RED)
        text_block(d, sx + 2, y + 29, wrap(d, ev, F(8), sw - 6), F(8),
                   fill=INK, leading=10, max_lines=2)
    rule(d, y + 44, 1)


def draw_lead(d, x, y, w, h, item):
    num, tag, head, summ, kind, lat, lon, label = item
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    img = scene(kind, 140, 128).resize((140, h), Image.LANCZOS)
    d._image.paste(img, (x, y))
    # data label inside the illustration (bottom-left of the image area)
    flab = F(12, bold=True)
    lw = d.textlength(label, font=flab) + 10
    d.rectangle([x + 4, y + h - 22, x + 4 + lw, y + h - 6],
                fill=(247, 243, 234), outline=RED, width=1)
    d.text((x + 9, y + h - 20), label, font=flab, fill=RED)
    tx = x + 148
    tw = w - 156
    d.text((tx, y + 6), "%d  ·  %s" % (num, tag), font=F(9, bold=True), fill=RED)
    yy = text_block(d, tx, y + 20, wrap(d, head, F(16, serif=True, bold=True), tw),
                    F(16, serif=True, bold=True), leading=18, max_lines=3)
    text_block(d, tx, yy + 2, wrap(d, summ, F(11), tw), F(11),
               fill=(60, 56, 48), leading=13, max_lines=3)


def draw_card(d, x, y, w, h, item):
    num, tag, head, summ, kind, lat, lon = item
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    img = scene(kind, 140, 128).resize((58, h), Image.LANCZOS)
    d._image.paste(img, (x, y))
    tx = x + 64
    tw = w - 70
    d.text((tx, y + 3), "%d · %s" % (num, tag), font=F(8, bold=True), fill=RED)
    yy = text_block(d, tx, y + 14, wrap(d, head, F(10, bold=True), tw),
                    F(10, bold=True), leading=11, max_lines=2)
    text_block(d, tx, yy + 1, wrap(d, summ, F(9), tw), F(9),
               fill=(60, 56, 48), leading=10, max_lines=2)


def draw_numbers(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    d.text((x + 8, y + 5), "THE DAY IN NUMBERS", font=F(11, bold=True), fill=INK)
    cols, rows = 3, 2
    cw, ch = w // cols, (h - 24) // rows
    for i, (num, label) in enumerate(NUMBERS):
        cx0 = x + (i % cols) * cw
        cy0 = y + 24 + (i // cols) * ch
        d.text((cx0 + 8, cy0), num, font=F(14, bold=True), fill=RED)
        d.text((cx0 + 8, cy0 + 17), label, font=F(8), fill=FAINT)


def draw_date_check(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    d.text((x + 8, y + 5), "DATE CHECK — LEFT OUT ON PURPOSE (WRONG DATE)",
           font=F(10, bold=True), fill=RED)
    cols = 2
    cw = (w - 16) // cols
    f = F(9)
    per_col = (len(DATE_CHECK) + 1) // 2
    for i, item in enumerate(DATE_CHECK):
        col = i // per_col
        row = i % per_col
        tx = x + 8 + col * cw
        ty = y + 20 + row * 10
        d.text((tx, ty), "✕ " + item, font=f, fill=FAINT)


def draw_briefs(d, x, y, w):
    yy = section_title(d, x, y, "ALSO ON 26 NOVEMBER — THE REST OF THE DAY")
    cols = 3
    cw = w // cols
    f = F(10)
    per_col = (len(BRIEFS) + cols - 1) // cols
    for i, (num, place, head) in enumerate(BRIEFS):
        col = i // per_col
        row = i % per_col
        tx = x + col * cw
        ty = yy + row * 16
        line = "%d. %s: %s" % (num, place, head)
        d.text((tx, ty), line, font=f, fill=INK)
    return yy + per_col * 16


def draw_footer(d, y):
    rule(d, y, 1)
    yy = text_block(d, M, y + 5, wrap(d, SOURCES, F(9), CW), F(9),
                    fill=FAINT, leading=11)
    d.text((W // 2, yy + 3),
           "All illustrations drawn for this page  ·  THE WORLD IN ONE DAY  ·  "
           "Thursday 26 November 2026  ·  40 stories, one day",
           font=F(9, bold=True), fill=INK, anchor="ma")


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d._image = img  # paste helper for scene images

    draw_masthead(d)
    draw_region_strip(d)
    draw_utc(d, M, 108, CW)

    # leads: 2 x 2 grid
    lw = (CW - 8) // 2
    lh = 124
    ly = 160
    for i, item in enumerate(LEADS):
        x = M + (i % 2) * (lw + 8)
        y = ly + (i // 2) * (lh + 8)
        draw_lead(d, x, y, lw, lh, item)

    # map (left) + numbers/date-check (right)
    my = 424
    mh = 202
    mw = (CW - 8) // 2
    d.text((M, my), "WHERE IT HAPPENED — 14 STORIES PINNED",
           font=F(11, bold=True), fill=INK)
    pins = [(num, lat, lon) for num, tag, head, summ, kind, lat, lon, *rest
            in LEADS] + [(num, lat, lon) for num, tag, head, summ, kind, lat, lon
                         in CARDS]
    # leader-line offsets where pins would cover each other (same city,
    # or clusters: Geneva/London/Brussels within ~9px, Washington/New York/
    # Chicago within ~15px, Taipei/Shanghai/Hong Kong/Seoul within ~13px)
    leaders = {2: (-16, 10), 14: (16, -12), 4: (-20, -14),
               10: (-22, 16), 11: (2, -20), 13: (22, 10),
               1: (0, 18), 6: (-16, 10), 7: (2, -20), 12: (6, -22)}
    draw_map(d, (M, my + 18, M + mw, my + 158), pins, leaders)
    ly0 = my + 162
    for ln in MAP_LEGEND:
        d.text((M, ly0), ln, font=F(8), fill=FAINT)
        ly0 += 11

    rx = M + mw + 8
    draw_numbers(d, rx, my, mw, 88)
    draw_date_check(d, rx, my + 92, mw, mh - 92)

    # medium cards: 5 cols x 2 rows
    cw5 = (CW - 4 * 4) // 5
    ch5 = 68
    cy = 634
    for i, item in enumerate(CARDS):
        x = M + (i % 5) * (cw5 + 4)
        y = cy + (i // 5) * (ch5 + 4)
        draw_card(d, x, y, cw5, ch5, item)

    # briefs
    by = 782
    endy = draw_briefs(d, M, by, CW)

    draw_footer(d, 952)
    return img


def main():
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = build()
    img.save(out, "PNG", optimize=True)
    print("wrote %s %dx%d %d bytes" % (out, img.width, img.height,
                                       os.path.getsize(out)))


if __name__ == "__main__":
    main()
