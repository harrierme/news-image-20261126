#!/usr/bin/env python3
"""Render 'The World in One Day' - Thursday 26 November 2026 - as one 1024x1024
PNG newspaper front page. All 52 stories were researched first (see stories.md);
every illustration is drawn here with Pillow, no photos, no network, no fonts
downloaded at run time. Deterministic: same input, same bytes every run."""

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


def trunc(d, text, font, width):
    """Shorten text with an ellipsis so it fits `width` px."""
    if d.textlength(text, font=font) <= width:
        return text
    while text and d.textlength(text + "...", font=font) > width:
        text = text[:-1]
    return text + "..."


# ---------------------------------------------------------------- stories
# (num, tag, headline, summary, kind, lat, lon)
LEADS = [
    (1, "ASIA-PACIFIC · TRADE · REPORTED",
     "US proposes tariffs of up to 15% on Taiwan and 16 partners",
     "USTR releases its overcapacity-probe findings; Taipei says it sits in the "
     "lowest tier, with Japan, South Korea and the EU, and answers on Thursday.",
     "ship", 25.03, 121.56),
    (2, "NORTH AMERICA · CULTURE · OFFICIAL",
     "100th Macy's Thanksgiving Day Parade steps off in New York",
     "A record 100 inflatable elements float the 2.5-mile route; US markets, "
     "banks and post offices shut for Thanksgiving Day.",
     "parade", 40.71, -74.00),
    (3, "ASIA-PACIFIC · ECONOMY · CONFIRMED",
     "Bank of Korea raises base rate 25bp to 3.25%",
     "Tightening resumes after October's pause, as the AI export boom keeps "
     "growth brisk and inflation above target.",
     "bank", 37.56, 126.97),
    (4, "EUROPE · WAR · REPORTED",
     "Russia's own figures show nearly 500,000 military deaths in Ukraine",
     "Moscow's own data put its war dead near half a million - a rare official "
     "glimpse of the toll after almost five years of war.",
     "war", 55.75, 37.61),
]

# (num, tag, headline, summary, kind, lat, lon)
CARDS = [
    (5, "N. AMERICA · LAW", "Judge bars FCC from moves threatening ABC licence",
     "Judge: agency appears to run a retaliatory campaign driven by Trump.", "tv", 38.90, -77.03),
    (6, "EUROPE · CLIMATE", "Norway top court voids climate-disputed oil licences",
     "Supreme Court rules disputed licences invalid in a landmark case.", "oil", 59.91, 10.75),
    (7, "ASIA-PACIFIC · DIPLOMACY", "N. Korea orders Switzerland to shut Pyongyang office",
     "Swiss diplomatic presence closed in a sanctions row.", "diplomacy", 39.03, 125.75),
    (8, "ASIA-PACIFIC · SPACE", "Pakistan's first astronaut to join China's Tiangong",
     "Muhammad Zeeshan Ali flies on Shenzhou-24, first foreigner aboard.", "rocket", 33.68, 73.05),
    (9, "SOUTH ASIA · POLITICS", "Hasina asks to return to Bangladesh on 16 December",
     "Ex-PM seeks government help to arrange return from India.", "parliament", 23.81, 90.41),
    (10, "SOUTH ASIA · ECONOMY", "Bangladesh raises garment minimum wage 36%",
     "Entry-level monthly pay for garment workers jumps by a third.", "factory", 23.81, 90.41),
    (11, "S. AMERICA · CRIME", "Colombia police free 20 supermarket hostages",
     "Hostages freed after a 17-hour standoff at a supermarket.", "supermarket", 4.71, -74.07),
    (12, "MIDDLE EAST · DISASTER", "Cairo fuel-tanker crash fire kills 31",
     "Thirty-one killed as a tanker crashes and burns on a highway.", "tanker", 30.04, 31.23),
    (13, "AFRICA · HEALTH", "Kenya clears last Ebola patient; DRC toll tops 5,300",
     "Kenya discharges its final case as the DRC outbreak toll climbs.", "clinic", -1.29, 36.82),
    (14, "AFRICA · ECONOMY", "Ghana unveils Heritage Series banknotes",
     "New notes honour Nkrumah, Kofi Annan and Makola traders.", "banknotes", 5.60, -0.18),
    (15, "SOUTH ASIA · EDUCATION", "India marks Constitution Day; IITs add 6,000 seats",
     "New seats in robotics, AI and space technology from 2027.", "university", 28.61, 77.20),
    (16, "SOUTH ASIA · SPORT", "IPL 2027 auction draws 1,220 players",
     "A record 1,220 cricketers register for the IPL auction.", "cricket", 19.07, 72.87),
]

# (num, place, headline) - one line each
BRIEFS = [
    (17, "Hanoi", "Vietnam says US trade deal to finish 'as soon as possible'"),
    (18, "New Delhi", "India unveils 15,000-crore-rupee package for Nepal"),
    (19, "New Delhi", "India urges human control over AI in warfare"),
    (20, "New Delhi", "India condemns Riyadh tower attack; two Indians hurt"),
    (21, "Bengaluru", "Flipkart chief Krishnamurthy to step down in December"),
    (22, "Geneva", "Gukesh meets Sindarov in World Chess Championship"),
    (23, "Dubai", "Sooryavanshi smashes 204 off 53 balls vs UAE"),
    (24, "Tokyo", "Azur Promilia launches across East Asia"),
    (25, "New York", "Some brands sit out Black Friday discounts"),
    (26, "Punjab", "Farmers sell stubble to biomass plants, cutting fires"),
    (27, "Washington", "Attorney general dodges questions on Nvidia inquiry"),
    (28, "Shanghai", "Xi's graft probe hits Shanghai rising star"),
    (29, "Jerusalem", "Judges urge dropping gravest charges against Netanyahu"),
    (30, "Gaza", "Israeli strike kills Hamas official"),
    (31, "Luxembourg", "EU court rules on caged animals"),
    (32, "Moscow", "Russia's military budget surges"),
    (33, "Brussels", "EU Parliament advances budget proposals"),
    (34, "Brussels", "3.7m European industrial jobs at risk"),
    (35, "Kinshasa", "DRC president enacts constitutional reform law"),
    (36, "Sao Tome", "PM Americo Ramos reappointed"),
    (37, "Lagos", "Nigeria starts building naval ships at home"),
    (38, "Johannesburg", "Protest outside court; police bar anti-migrant rallies"),
    (39, "Nairobi", "Kenya secures 293,600 jobs in Saudi Arabia"),
    (40, "Philadelphia", "LeBron's first 76ers triple-double cools Heat 111-104"),
    (41, "San Diego", "Padres sign reliever Romero, 3 yrs, $21m"),
    (42, "Baton Rouge", "RJ Luis Jr sues SEC and commissioner Sankey"),
    (43, "Bahamas", "Xavier edges Texas A&M 88-83 in Battle 4 Atlantis"),
    (44, "Lincoln", "Nebraska tops 100 again; USC edges S. Carolina 71-69"),
    (45, "Bruges", "Liverpool win 3-0; Bayern lose 2-1 at Lille"),
    (46, "Paris", "PSG held 2-2 by Roma; Man Utd draw 2-2 at Sporting"),
    (47, "Baku", "Barca cruise 4-1 at Sabah; Inter beat Stuttgart 2-0"),
    (48, "Ranchi", "Police detain protesters over tree cutting"),
    (49, "Juba", "Awar Odhiang named model of the year"),
    (50, "Lagos", "Tyla, Tems and Kidjo lead Africa's Grammy hopes"),
    (51, "Bogota", "UN chief praises Colombia's decade of peace progress"),
    (52, "Brasilia", "Brazil viral infections down 68% after Wolbachia mosquitoes"),
]

REGIONS = [("NORTH AMERICA", 9), ("SOUTH AMERICA", 3), ("EUROPE", 10),
           ("AFRICA", 9), ("MIDDLE EAST", 4), ("SOUTH ASIA", 9),
           ("ASIA-PACIFIC", 8)]

NUMBERS = [("3.25%", "Bank of Korea rate"), ("15%", "top US tariff proposed"),
           ("100th", "Macy's parade"), ("500,000", "Russian war dead"),
           ("1,220", "IPL auction hopefuls"), ("293,600", "Kenya jobs in Saudi"),
           ("36%", "Bangladesh wage rise"), ("204", "runs, 53 balls")]

DATE_CHECK = [
    "Houthi claim, Ras Tanura attack; Brent $94.61 — Wed 25 Nov",
    "Hera asteroid images released — Wed 25 Nov",
    "Asian stocks plunge: Kospi -6%, Nikkei -3% — Wed 25 Nov",
    "Fed Beige Book: modest growth — Wed 25 Nov",
    "F-15EX unveiled at Kadena — Wed 25 Nov",
    "Nvidia CEO Jensen Huang resigned — Thu 12 Nov",
    "Nvidia record $115.8bn quarter — Tue 17 Nov",
    "Kerch bridge attack — 16-17 Nov",
    "An-12 crash — Tue 17 Nov",
    "Lagarde ECB resignation announced — Thu 29 Oct",
    "US midterms: Democrats take Congress — Tue 3 Nov",
    "Not yet: Black Friday — Fri 27 Nov",
]

SOURCES = ("Sources: Reuters, BBC, AP, AFP, RTHK, USTR, Bank of Korea, Taiwan Executive Yuan, "
           "C54 News, EUR Radio, Xinhua, NBC, press wires. Labels: CONFIRMED = verified by the "
           "named source; REPORTED = as reported; OFFICIAL = announced by an authority. "
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
        d.line([cx, 74, cx, 92], fill=INK, width=1)
    elif kind == "bank":
        _sky(d, (0, 0, w, h), (200, 205, 190), (150, 150, 130))
        d.polygon([(10, 46), (cx, 18), (w - 10, 46)], fill=(120, 60, 50))
        d.rectangle([16, 46, w - 16, 52], fill=(90, 84, 74))
        for i in range(4):
            d.rectangle([22 + i * 30, 52, 34 + i * 30, h - 14], fill=(240, 240, 235))
        d.rectangle([16, h - 14, w - 16, h - 8], fill=(90, 84, 74))
        d.text((cx, 56), "%", font=F(26, bold=True), fill=RED, anchor="mt")
    elif kind == "war":
        _sky(d, (0, 0, w, h), (120, 130, 140), (70, 90, 70))
        _sun(d, (0, 0, w, h), w - 26, 26, 14, (220, 200, 160))
        for (px, py) in [(20, 70), (48, 84), (76, 68), (104, 86), (128, 72), (60, 96), (100, 100)]:
            d.line([px, py, px, py - 16], fill=(40, 70, 40), width=2)
            d.ellipse([px - 5, py - 22, px + 5, py - 12], fill=(158, 26, 26))
            d.ellipse([px - 2, py - 19, px + 2, py - 15], fill=(26, 26, 26))
        d.rectangle([8, h - 8, w - 8, h - 4], fill=(60, 60, 50))
    elif kind == "tv":
        _sky(d, (0, 0, w, h), (190, 195, 205), (140, 145, 155))
        d.rectangle([18, 30, w - 18, h - 34], fill=(30, 40, 56))
        d.rectangle([26, 38, w - 26, h - 42], fill=(150, 200, 220))
        d.text((cx, 44), "ABC", font=F(22, bold=True), fill=(26, 26, 26), anchor="mt")
        d.line([cx - 20, h - 34, cx - 34, 14], fill=INK, width=2)
        d.line([cx + 20, h - 34, cx + 34, 14], fill=INK, width=2)
        d.ellipse([cx - 34, 8, cx - 28, 14], fill=RED)
        d.ellipse([cx + 28, 8, cx + 34, 14], fill=RED)
    elif kind == "oil":
        _sky(d, (0, 0, w, h), (150, 180, 205), (70, 110, 130))
        _sun(d, (0, 0, w, h), 26, 24, 13)
        d.polygon([(70, h - 10), (86, 30), (102, 30), (118, h - 10)], fill=(60, 60, 60))
        d.line([86, 30, 118, h - 10], fill=(240, 240, 235), width=2)
        d.line([102, 30, 102, 52], fill=(240, 240, 235), width=3)
        d.rectangle([w - 40, h - 30, w - 8, h - 10], fill=(40, 60, 80))
        d.ellipse([w - 46, h - 44, w - 30, h - 28], fill=(30, 40, 56))
    elif kind == "diplomacy":
        _sky(d, (0, 0, w, h), (200, 210, 220), (160, 165, 170))
        d.line([44, 16, 44, h - 12], fill=INK, width=3)
        d.line([w - 44, 16, w - 44, h - 12], fill=INK, width=3)
        d.rectangle([44, 16, 84, 44], fill=(158, 26, 26))
        d.ellipse([56, 24, 72, 36], fill=(247, 243, 234))
        d.rectangle([w - 84, 16, w - 44, 44], fill=(28, 68, 110))
        d.rectangle([w - 84, 26, w - 44, 34], fill=(247, 243, 234))
        d.ellipse([cx - 10, h - 30, cx + 10, h - 10], fill=GOLD)
    elif kind == "rocket":
        _sky(d, (0, 0, w, h), (20, 30, 60), (40, 60, 100))
        for (sx, sy) in [(20, 20), (50, 12), (110, 18), (130, 40), (14, 60), (126, 70)]:
            d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(247, 243, 234))
        d.polygon([(cx, 14), (cx + 12, 44), (cx - 12, 44)], fill=(158, 26, 26))
        d.rectangle([cx - 12, 44, cx + 12, 78], fill=(240, 240, 235))
        d.polygon([(cx - 12, 62), (cx - 24, 80), (cx - 12, 78)], fill=(158, 26, 26))
        d.polygon([(cx + 12, 62), (cx + 24, 80), (cx + 12, 78)], fill=(158, 26, 26))
        d.ellipse([cx - 5, 52, cx + 5, 62], fill=(28, 68, 110))
        d.polygon([(cx - 6, 78), (cx + 6, 78), (cx + 12, 96), (cx - 12, 96)], fill=GOLD)
        d.ellipse([w - 30, h - 30, w - 8, h - 8], fill=(200, 200, 190))
        d.ellipse([w - 26, h - 26, w - 16, h - 16], fill=(150, 150, 140))
    elif kind == "parliament":
        _sky(d, (0, 0, w, h), (190, 200, 215), (150, 155, 150))
        d.ellipse([cx - 26, 18, cx + 26, 52], fill=(120, 90, 70))
        d.rectangle([16, 52, w - 16, 58], fill=(90, 84, 74))
        for i in range(5):
            d.rectangle([22 + i * 26, 58, 32 + i * 26, h - 12], fill=(240, 240, 235))
        d.rectangle([16, h - 12, w - 16, h - 6], fill=(90, 84, 74))
        d.rectangle([cx - 8, 66, cx + 8, h - 12], fill=(120, 60, 50))
    elif kind == "factory":
        _sky(d, (0, 0, w, h), (200, 200, 190), (140, 140, 130))
        d.rectangle([16, h - 52, w - 40, h - 10], fill=(110, 100, 90))
        d.polygon([(16, h - 52), (36, h - 70), (56, h - 52)], fill=(90, 80, 70))
        d.polygon([(56, h - 52), (76, h - 70), (96, h - 52)], fill=(90, 80, 70))
        d.rectangle([w - 36, 22, w - 22, h - 10], fill=(90, 84, 74))
        for (sx, sy, r) in [(w - 29, 14, 5), (w - 33, 6, 4), (w - 25, 2, 3)]:
            d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(220, 220, 210))
        _windows(d, 22, h - 46, w - 68, 30, 2, 5)
    elif kind == "supermarket":
        _sky(d, (0, 0, w, h), (200, 210, 200), (150, 155, 145))
        d.rectangle([14, 34, w - 14, h - 12], fill=(240, 240, 235))
        d.rectangle([14, 34, w - 14, 52], fill=(158, 26, 26))
        for i in range(5):
            d.rectangle([20 + i * 26, 52, 32 + i * 26, 58], fill=(247, 243, 234))
        d.rectangle([cx - 16, 62, cx + 16, h - 12], fill=(28, 68, 110))
        d.rectangle([22, 66, 52, 84], fill=(150, 200, 220))
        d.rectangle([w - 52, 66, w - 22, 84], fill=(150, 200, 220))
    elif kind == "tanker":
        _sky(d, (0, 0, w, h), (210, 190, 170), (120, 110, 100))
        d.ellipse([cx - 34, 12, cx + 34, 66], fill=(220, 110, 30))
        d.ellipse([cx - 20, 26, cx + 20, 58], fill=(240, 160, 40))
        d.rectangle([18, h - 40, w - 18, h - 22], fill=(200, 200, 190))
        d.ellipse([34, h - 22, 52, h - 4], fill=(26, 26, 26))
        d.ellipse([w - 52, h - 22, w - 34, h - 4], fill=(26, 26, 26))
        d.rectangle([w - 30, h - 52, w - 14, h - 40], fill=(158, 26, 26))
    elif kind == "clinic":
        _sky(d, (0, 0, w, h), (200, 215, 205), (160, 170, 160))
        d.rectangle([24, 34, w - 24, h - 12], fill=(240, 240, 235))
        d.rectangle([cx - 6, 40, cx + 6, 64], fill=(158, 26, 26))
        d.rectangle([cx - 12, 46, cx + 12, 58], fill=(158, 26, 26))
        d.rectangle([32, h - 34, 62, h - 12], fill=(150, 200, 220))
        d.rectangle([w - 62, h - 34, w - 32, h - 12], fill=(150, 200, 220))
        d.rectangle([cx - 10, h - 30, cx + 10, h - 12], fill=(28, 68, 110))
    elif kind == "banknotes":
        _sky(d, (0, 0, w, h), (190, 200, 180), (140, 145, 130))
        for i, c in enumerate([(176, 132, 40), (28, 110, 80), (120, 90, 140)]):
            y = 24 + i * 26
            d.rectangle([16, y, w - 16, y + 22], fill=c)
            d.ellipse([cx - 9, y + 4, cx + 9, y + 18], fill=(247, 243, 234))
            d.text((cx, y + 6), "$", font=F(12, bold=True), fill=INK, anchor="mt")
    elif kind == "university":
        _sky(d, (0, 0, w, h), (200, 205, 190), (150, 150, 130))
        d.polygon([(14, 40), (cx, 16), (w - 14, 40)], fill=(90, 60, 50))
        for i in range(4):
            d.rectangle([24 + i * 30, 44, 36 + i * 30, h - 14], fill=(240, 240, 235))
        d.rectangle([16, h - 14, w - 16, h - 8], fill=(90, 84, 74))
        d.rectangle([cx - 8, 56, cx + 8, h - 14], fill=(120, 60, 50))
        d.ellipse([cx - 14, 22, cx + 14, 38], fill=GOLD)
    elif kind == "cricket":
        _sky(d, (0, 0, w, h), (150, 190, 140), (90, 140, 80))
        d.rectangle([cx - 30, 22, cx - 18, 84], fill=(200, 170, 120))  # bat
        d.rectangle([cx - 32, 14, cx - 16, 24], fill=(120, 90, 60))
        d.ellipse([cx + 8, 30, cx + 26, 48], fill=(158, 26, 26))  # ball
        d.ellipse([cx + 13, 34, cx + 18, 39], fill=(247, 243, 234))
        for i in range(3):
            d.rectangle([cx + 34 + i * 6, 60, cx + 38 + i * 6, h - 16], fill=(220, 190, 120))
        d.rectangle([cx + 34, 56, cx + 52, 60], fill=(200, 170, 120))
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
    d.text((W - M, 54), "52 STORIES  ·  7 REGIONS  ·  19 FIELDS",
           font=F(12, bold=True), fill=RED, anchor="ra")
    rule(d, 84, 2)
    rule(d, 88, 1)


def draw_region_strip(d):
    parts = []
    for name, n in REGIONS:
        parts.append("%s %d" % (name, n))
    txt = "   ·   ".join(parts)
    d.text((W // 2, 96), txt, font=F(11, bold=True), fill=BLUE, anchor="ma")


def draw_lead(d, x, y, w, h, item):
    num, tag, head, summ, kind, lat, lon = item
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)
    img = scene(kind, 140, 128).resize((140, h), Image.LANCZOS)
    d._image.paste(img, (x, y))
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
    cols, rows = 4, 2
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
        d.text((tx, ty), trunc(d, "✕ " + item, f, cw - 6), font=f, fill=FAINT)


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
        ty = yy + row * 15
        line = "%d. %s: %s" % (num, place, head)
        d.text((tx, ty), trunc(d, line, f, cw - 10), font=f, fill=INK)
    return yy + per_col * 15


def draw_footer(d, y):
    rule(d, y, 1)
    yy = text_block(d, M, y + 5, wrap(d, SOURCES, F(9), CW), F(9),
                    fill=FAINT, leading=11)
    d.text((W // 2, yy + 3),
           "All illustrations drawn for this page  ·  THE WORLD IN ONE DAY  ·  "
           "Thursday 26 November 2026  ·  52 stories, one day",
           font=F(9, bold=True), fill=INK, anchor="ma")


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d._image = img  # paste helper for scene images

    draw_masthead(d)
    draw_region_strip(d)

    # leads: 2 x 2 grid
    lw = (CW - 8) // 2
    lh = 124
    ly = 124
    for i, item in enumerate(LEADS):
        x = M + (i % 2) * (lw + 8)
        y = ly + (i // 2) * (lh + 8)
        draw_lead(d, x, y, lw, lh, item)

    # map (left) + numbers/date-check (right)
    my = 384
    mh = 176
    mw = (CW - 8) // 2
    d.text((M, my), "WHERE IT HAPPENED — 16 STORIES PINNED",
           font=F(11, bold=True), fill=INK)
    pins = [(num, lat, lon) for num, tag, head, summ, kind, lat, lon
            in LEADS + CARDS]
    # leader-line offsets where pins would cover each other (same city/region)
    leaders = {5: (-16, 10), 7: (16, -12), 8: (-18, -14), 10: (16, 10),
               16: (-14, 12)}
    draw_map(d, (M, my + 18, M + mw, my + mh), pins, leaders)

    rx = M + mw + 8
    draw_numbers(d, rx, my, mw, 88)
    draw_date_check(d, rx, my + 92, mw, mh - 92)

    # medium cards: 4 cols x 3 rows
    cw4 = (CW - 3 * 4) // 4
    ch4 = 64
    cy = 568
    for i, item in enumerate(CARDS):
        x = M + (i % 4) * (cw4 + 4)
        y = cy + (i // 4) * (ch4 + 4)
        draw_card(d, x, y, cw4, ch4, item)

    # briefs
    by = 776
    endy = draw_briefs(d, M, by, CW)

    draw_footer(d, 972)
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
