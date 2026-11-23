#!/usr/bin/env python3
"""ONE DAY, EVERYWHERE - a one-page newspaper of Monday, November 23, 2026.

Deterministic Pillow renderer. Every story below was checked against
reporting dated Monday, November 23, 2026; the source is named on the page.
Run: python3 draw.py  ->  writes entry.png (1024x1024) next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024

FD = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FD, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FD, "DejaVuSerif.ttf")
SANS_B = os.path.join(FD, "DejaVuSans-Bold.ttf")
SANS = os.path.join(FD, "DejaVuSans.ttf")

def F(path, size):
    return ImageFont.truetype(path, size)

BG = (246, 239, 219)
PAPER = (252, 248, 233)
INK = (27, 23, 17)
FAINT = (112, 101, 80)
RULE = (58, 50, 38)
RED = (163, 36, 27)
BLUE = (36, 72, 118)
GREEN = (46, 102, 58)
AMBER = (166, 112, 20)
SKY = (196, 216, 228)
SEA = (222, 231, 224)

TAG_COLORS = {"REPORTED": BLUE, "CLAIM": AMBER, "ONGOING": RED}

HERO = [
    ("258", "House seats clinched by the Democrats - biggest majority since 1992"),
    ("-5.06%", "Japan's Nikkei, as the AI sell-off spread across Asia"),
    ("24", "dead in the Banten candy-factory fire; about 30 still missing"),
    ("11", "killed in Russian strikes across the Kyiv region"),
    ("1,600+", "Delta flights delayed by the Atlanta hub outage"),
    ("405 t", "of rocket chemical seized on a ship off Indonesia"),
]

LEADS = [
    {
        "num": 1, "scene": "climate", "tag": "REPORTED",
        "kicker": "ANTALYA, TURKIYE - CLIMATE SUMMIT",
        "headline": "COP31 Ends Without a Deal",
        "body": ("The UN climate summit closed after two days of overtime with no overall "
                 "agreement. The EU, Panama and some 130 parties rejected a presidency draft "
                 "that left out fossil fuels; Saudi Arabia, India and China backed the text. "
                 "Ireland's climate minister, speaking for the EU, said oil states had "
                 "hijacked the talks - the longest climate summit on record."),
        "src": "BBC - The Hindu",
    },
    {
        "num": 2, "scene": "strike", "tag": "REPORTED",
        "kicker": "DYMER, UKRAINE - THE WAR",
        "headline": "Strikes Kill at Least 11 Near Kyiv",
        "body": ("A Russian strike destroyed an apartment block in Dymer, north of Kyiv; "
                 "rescuers pulled a 7-year-old boy alive from the rubble. The Associated Press "
                 "put the toll across the Kyiv region at at least 11 dead, among them a "
                 "teenager, with two more killed when a supermarket was hit in Vyshneve."),
        "src": "Associated Press",
    },
    {
        "num": 3, "scene": "markets", "tag": "REPORTED",
        "kicker": "TOKYO - WORLD MARKETS",
        "headline": "AI Sell-Off Rattles the World",
        "body": ("Fears that AI shares are wildly overpriced set off a global slide. Japan's "
                 "Nikkei fell 5.06% and the S&P 500 dropped 3.7%; London's FTSE 100 lost "
                 "1.02%. Gold jumped 2.72% as investors ran for safety, while Brent crude held "
                 "near $90 a barrel, at $89.96, as Iran-war attacks continued."),
        "src": "Market reports",
    },
]

CARDS = [
    (4, "capitol", "REPORTED", "Democrats Clinch 258 House Seats",
     "Largest majority for either party since 1992 - AP"),
    (5, "flame", "ONGOING", "Factory Fire Kills 24 in Banten",
     "About 30 still unaccounted for; search resumes - Xinhua"),
    (6, "plane", "REPORTED", "Delta Outage Delays 1,600+ Flights",
     "Weight-and-balance fault at Atlanta hub, now fixed - FAA"),
    (7, "tanker", "ONGOING", "Tankers Ablaze Near Hormuz",
     "Strikes on Bahrain as Iran-war attacks continue"),
    (8, "drone", "CLAIM", "Iran Claims US Drone Downed",
     "Tehran says an MQ-9 Reaper fell over the Strait"),
    (9, "city", "REPORTED", "Five Children Killed in Khartoum",
     "Drone attacks hit the capital and Omdurman, Sudan"),
    (10, "shield", "REPORTED", "Attack Kills 24 in South Sudan",
     "Paramilitary assault on civilians reported"),
    (11, "cross", "ONGOING", "Ebola Response Disrupted",
     "Fighting near the outbreak zone in eastern DR Congo"),
    (12, "ship", "REPORTED", "Russian Warship Sinks off Libya",
     "Kyiv says its naval drone struck the corvette Merkury"),
    (13, "tower", "REPORTED", "Belgian Airports Shut by Strike",
     "Anti-austerity walkout grounds flights in Brussels"),
    (14, "crowd", "REPORTED", "Thousands Rally in Istanbul",
     "Protest against a takeover of media outlets"),
    (15, "arch", "REPORTED", "Nepal's PM Welcomed in Delhi",
     "Balen Shah received by Modi at Rashtrapati Bhavan"),
]

ALSO = [
    (16, "Trump 'inclined' to resume Iran conflict if no deal by New Year", "Economic Times"),
    (17, "Houthis claim Saudi refinery attack; Saudi strike hits Hodeida", "One Turn"),
    (18, "Experts say Gaza war left widespread contamination", "One Turn"),
    (19, "Netanyahu, Eisenkot parties end coalition talks without a deal", "One Turn"),
    (20, "Russia-bound freighter Sparta II ablaze in the Gulf of Finland", "One Turn"),
    (21, "Five EU countries accept deportation centres in Rwanda", "One Turn"),
    (22, "Ship seized with 405 t of rocket chemical bound for Bangladesh", "Inshorts"),
    (23, "India holds No. 3 in Asia Power Index, scoring 40.5", "Lowy via Inshorts"),
    (24, "South Korea education minister quits over exam cheating", "One Turn"),
    (25, "Bolsonaro in intensive care with intestinal obstruction", "One Turn"),
    (26, "US Army to detonate unstable explosives in Iowa", "One Turn"),
    (27, "Nine shot at a concert in Strathmore, California", "One Turn"),
    (28, "Shuri Castle hall restored, seven years after the fire", "One Turn"),
    (29, "Ateez earn a fourth No. 1 on the Billboard 200", "One Turn"),
    (30, "Australia treasurer warns jobless rate will pass 5%", "One Turn"),
    (31, "Otters return to a once-polluted Kuala Lumpur river", "One Turn"),
    (32, "Robot sub finds fierce volcanic activity in Mariana Trench", "One Turn"),
    (33, "Lewis Pugh swims the length of the Strait of Hormuz", "One Turn"),
    (34, "Nigeria moves to end jail terms for attempted suicide", "One Turn"),
]

DATE_CHECK = [
    ("SUN NOV 22", "Liverpool 4-0 Man United in Pochettino's debut - played Sunday (Reuters)"),
    ("SUN NOV 22", "AP college poll: Georgia, Utah, Notre Dame stay 1-2-3 (Reuters)"),
    ("FRI NOV 20", "Common Cents Act signed - US penny production ends (White House)"),
    ("FRI NOV 20", "'El Chapo Isidro' captured in Sinaloa - arrested Friday, told Monday"),
    ("THU NOV 19", "Trump, Putin and Xi meet at the Shenzhen APEC summit (Reuters)"),
]

# story number -> (lon, lat) for the dotted map pins
PINS = {
    1: (30.7, 36.9), 2: (30.5, 50.4), 3: (139.7, 35.7), 4: (-77.0, 38.9),
    5: (106.2, -6.4), 6: (-84.4, 33.7), 7: (56.3, 26.5), 8: (51.4, 35.7),
    9: (32.5, 15.6), 10: (31.6, 4.9), 11: (29.2, -1.7), 12: (13.2, 32.9),
    13: (4.4, 50.8), 14: (28.9, 41.0), 15: (77.2, 28.6),
}

# stylised landmasses for the dotted map: (lon, lat, radius_lon, radius_lat)
BLOBS = [
    (-102, 50, 26, 9), (-88, 40, 15, 8), (-96, 31, 11, 5), (-118, 40, 9, 10),
    (-122, 48, 6, 6), (-155, 64, 11, 4), (-85, 66, 12, 5), (-78, 44, 8, 5),
    (-102, 20, 7, 5), (-99, 17, 5, 3.5), (-84, 15, 4, 2), (-41, 73, 11, 6),
    (-62, -8, 10, 7), (-52, -15, 9, 7), (-58, -25, 6, 7), (-64, -35, 4.5, 7),
    (-70, -47, 2.5, 6), (-75, 2, 6, 4), (-43, -5, 7, 4),
    (8, 46, 10, 5), (18, 50, 12, 5), (28, 52, 8, 4), (-3, 40, 5, 3),
    (14, 41, 3, 4), (-2, 53, 3, 3.5), (14, 62, 8, 6), (24, 64, 7, 5),
    (60, 62, 35, 7), (105, 64, 35, 7), (140, 63, 30, 7), (60, 55, 25, 5),
    (95, 55, 25, 5), (130, 52, 20, 5),
    (45, 30, 10, 6), (52, 25, 7, 4), (38, 35, 6, 3),
    (8, 8, 14, 8), (20, 6, 13, 8), (24, -4, 11, 8), (26, -16, 10, 8),
    (22, -27, 8, 6), (0, 22, 16, 7), (15, 24, 14, 6), (-8, 26, 8, 5),
    (47, 5, 5, 5), (47, -19, 3, 6),
    (78, 21, 6, 7), (80, 13, 4, 4), (101, 15, 5, 6), (104, 8, 3, 3),
    (97, 17, 4, 4), (108, 32, 13, 8), (115, 30, 9, 6), (122, 37, 6, 4),
    (102, -2, 6, 2.5), (113, -1, 6, 2.5), (120, -2, 5, 2.5), (131, -3, 5, 2.5),
    (95, 4, 4, 2), (107, -7, 5, 1.8), (138, 37, 4, 3), (141, 42, 3, 2.5),
    (128, 37, 2.5, 2.5), (122, 13, 2.5, 3.5),
    (134, -25, 11, 6), (146, -28, 7, 5), (122, -24, 6, 4), (148, -37, 4, 3),
    (172, -42, 2.5, 3),
]

def is_land(lon, lat):
    for clon, clat, rx, ry in BLOBS:
        if ((lon - clon) / rx) ** 2 + ((lat - clat) / ry) ** 2 <= 1.0:
            return True
    return False


# ---------------------------------------------------------------- helpers

def tw(d, s, font):
    return d.textlength(s, font=font)

def wrap(d, s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if tw(d, t, font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def lines_at(d, x, y, lines, font, fill, leading):
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y

def chip(d, x, y, text, color):
    f = F(SANS_B, 9)
    w_ = tw(d, text, f) + 10
    d.rounded_rectangle([x, y, x + w_, y + 14], 3, fill=color)
    d.text((x + 5, y + 2), text, font=f, fill=(255, 252, 240))
    return w_

def num_badge(d, cx, cy, n, r=10):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=INK)
    f = F(SANS_B, 11 if n < 10 else 10)
    s = str(n)
    d.text((cx - tw(d, s, f) / 2, cy - 7), s, font=f, fill=(255, 252, 240))

# ---------------------------------------------------------------- scenes

def scene_climate(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.ellipse([x + w - 62, y + 10, x + w - 18, y + 54], fill=(240, 178, 60))
    for dx in range(0, w, 26):  # clouds
        d.ellipse([x + dx + 6, y + 12, x + dx + 34, y + 26], fill=(244, 248, 250))
    gx, gy, gr = x + 74, y + h - 52, 40  # globe
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(88, 140, 190))
    d.ellipse([gx - 26, gy - 22, gx - 4, gy - 6], fill=GREEN)
    d.ellipse([gx + 4, gy + 2, gx + 28, gy + 20], fill=GREEN)
    d.ellipse([gx - 10, gy + 14, gx + 8, gy + 30], fill=GREEN)
    bx = x + w - 118  # factory
    d.rectangle([bx, y + h - 58, bx + 78, y + h - 18], fill=(74, 66, 58))
    d.rectangle([bx + 8, y + h - 88, bx + 20, y + h - 58], fill=(74, 66, 58))
    d.rectangle([bx + 52, y + h - 96, bx + 64, y + h - 58], fill=(74, 66, 58))
    for sx, sy in ((bx + 14, y + h - 100), (bx + 58, y + h - 108)):
        d.ellipse([sx - 8, sy - 8, sx + 10, sy + 6], fill=(200, 200, 196))
        d.ellipse([sx + 4, sy - 16, sx + 26, sy], fill=(214, 214, 210))
    for i in range(6):
        d.rectangle([bx + 10 + i * 12, y + h - 46, bx + 18 + i * 12, y + h - 34],
                    fill=(250, 214, 120))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(96, 122, 74))
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)

def scene_strike(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(216, 206, 188))
    d.rectangle([x, y, x + w, y + 30], fill=(172, 178, 186))
    bx, by, bw, bh = x + 118, y + 26, 92, h - 44  # standing block
    d.rectangle([bx, by, bx + bw, by + bh], fill=(168, 152, 128))
    for r in range(3):
        for c in range(4):
            d.rectangle([bx + 8 + c * 21, by + 7 + r * 17, bx + 20 + c * 21, by + 18 + r * 17],
                        fill=(240, 226, 170))
    dx, dy, dw, dh = x + 226, y + 40, 76, h - 58  # damaged block
    d.polygon([(dx, dy + dh), (dx, dy + 18), (dx + 26, dy + 34), (dx + 44, dy + 10),
               (dx + dw, dy + 26), (dx + dw, dy + dh)], fill=(150, 132, 110))
    for wx, wy in ((dx + 48, dy + 22), (dx + 48, dy + 38), (dx + 12, dy + 26)):
        d.rectangle([wx, wy, wx + 13, wy + 11], fill=(90, 80, 70))
    for i in range(7):  # rubble
        rx = x + 210 + i * 13
        d.polygon([(rx, y + h - 18), (rx + 8, y + h - 30 - (i % 3) * 4), (rx + 16, y + h - 18)],
                  fill=(120, 106, 88))
    cx = x + 40  # crane
    d.rectangle([cx, y + 34, cx + 6, y + h - 18], fill=(120, 90, 40))
    d.rectangle([cx, y + 34, cx + 92, y + 40], fill=(120, 90, 40))
    d.line([cx + 84, y + 40, cx + 84, y + 66], fill=(80, 70, 50), width=2)
    d.rectangle([cx + 76, y + 66, cx + 92, y + 76], fill=(150, 132, 110))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(104, 94, 78))
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)

def scene_markets(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 240, 238))
    for gx in range(x + 14, x + w - 8, 28):
        d.line([gx, y + 10, gx, y + h - 24], fill=(206, 210, 204), width=1)
    for gy in range(y + 12, y + h - 20, 22):
        d.line([x + 10, gy, x + w - 10, gy], fill=(206, 210, 204), width=1)
    pts = [(x + 18, y + 26), (x + 62, y + 40), (x + 104, y + 34), (x + 146, y + 58),
           (x + 188, y + 66), (x + 228, y + 88), (x + 262, y + 96), (x + w - 22, y + h - 34)]
    d.line(pts, fill=RED, width=4)
    for px, py in pts:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED)
    ex, ey = pts[-1]
    d.polygon([(ex + 2, ey - 2), (ex + 16, ey + 2), (ex + 2, ey + 10)], fill=RED)
    for i, (cw, chh) in enumerate(((10, 26), (10, 18), (10, 30))):  # candles
        cx = x + 36 + i * 26
        d.rectangle([cx, y + h - 44, cx + cw, y + h - 44 + chh], fill=GREEN)
    gx = x + w - 74  # gold bar
    d.polygon([(gx, y + h - 30), (gx + 52, y + h - 30), (gx + 44, y + h - 16), (gx + 8, y + h - 16)],
              fill=(226, 178, 60), outline=(150, 116, 30))
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=1)

SCENES = {"climate": scene_climate, "strike": scene_strike, "markets": scene_markets}

# ---------------------------------------------------------------- icons

def icon(d, kind, x, y, s=40):
    """Tiny scene glyphs drawn in an s x s box."""
    ink, acc = INK, RED
    if kind == "capitol":
        d.polygon([(x + 8, y + 16), (x + s - 8, y + 16), (x + s // 2, y + 5)], fill=ink)
        for i in range(4):
            d.rectangle([x + 9 + i * 8, y + 18, x + 13 + i * 8, y + 30], fill=ink)
        d.rectangle([x + 6, y + 32, x + s - 6, y + 35], fill=ink)
    elif kind == "flame":
        d.polygon([(x + s // 2, y + 3), (x + s - 9, y + 24), (x + s - 13, y + 34),
                   (x + 13, y + 34), (x + 9, y + 24)], fill=acc)
        d.polygon([(x + s // 2, y + 15), (x + s - 15, y + 27), (x + s // 2, y + 34),
                   (x + 15, y + 27)], fill=(240, 160, 50))
        d.rectangle([x + 6, y + 35, x + s - 6, y + 38], fill=ink)
    elif kind == "plane":
        d.polygon([(x + 4, y + 22), (x + s - 6, y + 10), (x + s - 12, y + 22),
                   (x + s - 6, y + 34), (x + 14, y + 27)], fill=ink)
        d.polygon([(x + 8, y + 6), (x + 16, y + 6), (x + 13, y + 16), (x + 9, y + 16)], fill=ink)
    elif kind in ("tanker", "ship"):
        d.polygon([(x + 4, y + 24), (x + s - 4, y + 24), (x + s - 9, y + 33), (x + 9, y + 33)],
                  fill=acc if kind == "tanker" else ink)
        d.rectangle([x + 14, y + 16, x + 26, y + 24], fill=ink)
        if kind == "tanker":
            d.polygon([(x + 26, y + 8), (x + 31, y + 17), (x + 21, y + 17)], fill=(240, 130, 40))
        for i in range(3):
            d.arc([x + 4 + i * 11, y + 32, x + 15 + i * 11, y + 40], 0, 180, fill=BLUE, width=2)
    elif kind == "drone":
        for cx, cy in ((x + 8, y + 8), (x + s - 8, y + 8), (x + 8, y + s - 10), (x + s - 8, y + s - 10)):
            d.ellipse([cx - 5, cy - 2, cx + 5, cy + 2], outline=ink, width=2)
            d.line([cx, cy, x + s // 2, y + s // 2], fill=ink, width=2)
        d.ellipse([x + s // 2 - 5, y + s // 2 - 5, x + s // 2 + 5, y + s // 2 + 5], fill=acc)
    elif kind == "city":
        d.rectangle([x + 6, y + 14, x + 16, y + 34], fill=ink)
        d.rectangle([x + 19, y + 8, x + 30, y + 34], fill=ink)
        d.rectangle([x + 32, y + 18, x + 38, y + 34], fill=ink)
        for wx, wy in ((9, 18), (22, 13), (22, 21), (34, 22)):
            d.rectangle([x + wx, y + wy, x + wx + 3, y + wy + 3], fill=(250, 220, 130))
    elif kind == "shield":
        d.polygon([(x + s // 2, y + 4), (x + s - 7, y + 9), (x + s - 7, y + 22),
                   (x + s // 2, y + 36), (x + 7, y + 22), (x + 7, y + 9)], outline=ink, width=3)
        d.text((x + s // 2 - 5, y + 11), "!", font=F(SANS_B, 17), fill=acc)
    elif kind == "cross":
        d.ellipse([x + 3, y + 3, x + s - 3, y + s - 3], outline=ink, width=2)
        d.rectangle([x + s // 2 - 3, y + 11, x + s // 2 + 3, y + 29], fill=acc)
        d.rectangle([x + 11, y + s // 2 - 3, x + 29, y + s // 2 + 3], fill=acc)
    elif kind == "tower":
        d.rectangle([x + s // 2 - 3, y + 14, x + s // 2 + 3, y + 36], fill=ink)
        d.polygon([(x + 10, y + 14), (x + s - 10, y + 14), (x + s // 2, y + 4)], fill=ink)
        d.line([x + 8, y + 8, x + s - 8, y + 30], fill=acc, width=3)
        d.line([x + s - 8, y + 8, x + 8, y + 30], fill=acc, width=3)
    elif kind == "crowd":
        for cx, cy, r in ((13, 16, 5), (24, 12, 6), (33, 17, 5)):
            d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r], fill=ink)
            d.pieslice([x + cx - r - 2, y + cy + r - 1, x + cx + r + 2, y + cy + r + 13], 180, 360, fill=ink)
        d.rectangle([x + 4, y + 34, x + s - 4, y + 36], fill=ink)
    elif kind == "arch":
        d.pieslice([x + 6, y + 6, x + s - 6, y + 34], 180, 360, fill=ink)
        d.rectangle([x + 6, y + 20, x + 12, y + 36], fill=ink)
        d.rectangle([x + s - 12, y + 20, x + s - 6, y + 36], fill=ink)
        d.rectangle([x + 4, y + 34, x + s - 4, y + 37], fill=ink)
    else:
        d.ellipse([x + 10, y + 10, x + s - 10, y + s - 10], fill=ink)


# ---------------------------------------------------------------- layout

def build():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    M, R = 24, 1000

    # masthead
    d.rectangle([M, 16, R, 19], fill=INK)
    d.line([M, 23, R, 23], fill=INK, width=1)
    mast = "ONE DAY, EVERYWHERE"
    fm = F(SERIF_B, 55)
    d.text(((W - tw(d, mast, fm)) / 2, 30), mast, font=fm, fill=INK)
    sub = "A ONE-PAGE NEWSPAPER OF THE WORLD'S NEWS"
    fs = F(SANS_B, 11)
    d.text(((W - tw(d, sub, fs)) / 2, 96), sub, font=fs, fill=FAINT)
    d.line([M, 116, R, 116], fill=RULE, width=1)
    dl = F(SANS_B, 11)
    d.text((M, 122), "MONDAY, NOVEMBER 23, 2026", font=dl, fill=INK)
    mid = "Vol. I - No. 23"
    d.text(((W - tw(d, mid, F(SANS, 11))) / 2, 122), mid, font=F(SANS, 11), fill=FAINT)
    rt = "34 STORIES - 7 REGIONS - 1 PAGE"
    d.text((R - tw(d, rt, dl), 122), rt, font=dl, fill=INK)
    d.line([M, 142, R, 142], fill=RULE, width=2)

    # hero number strip
    hy, hh = 150, 72
    cw = (976 - 5 * 6) / 6
    for i, (num, cap) in enumerate(HERO):
        cx = M + i * (cw + 6)
        if i:
            d.line([cx - 3, hy + 4, cx - 3, hy + hh - 4], fill=(196, 186, 158), width=1)
        fn = F(SERIF_B, 26)
        d.text((cx + (cw - tw(d, num, fn)) / 2, hy), num, font=fn, fill=RED)
        fc = F(SANS, 8.5)
        for j, ln in enumerate(wrap(d, cap, fc, cw - 6)[:3]):
            d.text((cx + (cw - tw(d, ln, fc)) / 2, hy + 34 + j * 11), ln, font=fc, fill=INK)
    d.line([M, 228, R, 228], fill=RULE, width=1)

    # leads
    ly, lh = 236, 294
    colw = (976 - 2 * 12) / 3
    for i, lead in enumerate(LEADS):
        cx = M + i * (colw + 12)
        if i:
            d.line([cx - 6, ly, cx - 6, ly + lh], fill=(196, 186, 158), width=1)
        fk = F(SANS_B, 10)
        d.text((cx, ly), lead["kicker"], font=fk, fill=RED)
        sy = ly + 16
        SCENES[lead["scene"]](d, int(cx), sy, int(colw), 100)
        yy = sy + 108
        fh = F(SERIF_B, 19)
        yy = lines_at(d, cx, yy, wrap(d, lead["headline"], fh, colw - 4)[:2], fh, INK, 23)
        fb = F(SERIF, 11)
        yy = lines_at(d, cx, yy + 2, wrap(d, lead["body"], fb, colw - 4)[:9], fb, INK, 14.5)
        fy = ly + lh - 16
        num_badge(d, cx + 10, fy + 7, lead["num"])
        chip(d, cx + 26, fy, lead["tag"], TAG_COLORS[lead["tag"]])
        fsrc = F(SANS, 9)
        d.text((cx + colw - tw(d, lead["src"], fsrc), fy + 2), lead["src"], font=fsrc, fill=FAINT)

    # map band + date check
    my, mh = 538, 156
    d.rectangle([M, my, 620, my + mh], fill=PAPER, outline=RULE, width=1)
    d.text((M + 10, my + 7), "WHERE IT HAPPENED", font=F(SANS_B, 11), fill=INK)
    d.text((M + 168, my + 8), "dots are land - pins carry the story numbers",
           font=F(SANS, 8.5), fill=FAINT)
    gx0, gy0, gw, gh = M + 8, my + 26, 580, 122
    for ci in range(110):
        lon = -180 + ci * 3.3
        for ri in range(33):
            lat = 82 - ri * 4.3
            if is_land(lon, lat):
                px = gx0 + ci * (gw / 109)
                py = gy0 + ri * (gh / 32)
                d.ellipse([px - 1.3, py - 1.3, px + 1.3, py + 1.3], fill=(158, 148, 118))
    pin_off = {1: (12, 8), 2: (5, -10), 4: (10, -3), 6: (-7, 3), 7: (9, 6),
               8: (-8, -6), 9: (-9, -4), 10: (11, 0), 11: (-3, 10), 12: (-6, 6),
               13: (-4, -6), 14: (-10, -2)}
    for n, (lon, lat) in PINS.items():
        ox, oy = pin_off.get(n, (0, 0))
        px = gx0 + (lon + 180) / 360 * gw + ox
        py = gy0 + (82 - lat) / 140 * gh + oy
        col = RED if n <= 3 else INK
        r = 8.5
        d.ellipse([px - r, py - r, px + r, py + r], fill=col, outline=(255, 252, 240), width=1)
        fp = F(SANS_B, 9)
        s = str(n)
        d.text((px - tw(d, s, fp) / 2, py - 5.5), s, font=fp, fill=(255, 252, 240))

    dx = 632
    d.rectangle([dx, my, R, my + mh], fill=(240, 230, 203), outline=RULE, width=1)
    d.text((dx + 10, my + 7), "DATE CHECK", font=F(SANS_B, 12), fill=RED)
    d.text((dx + 108, my + 9), "big stories from OTHER days - set aside on purpose",
           font=F(SANS, 8.5), fill=FAINT)
    yy = my + 28
    for when, what in DATE_CHECK:
        d.text((dx + 10, yy), when, font=F(SANS_B, 8.5), fill=INK)
        yy = lines_at(d, dx + 76, yy, wrap(d, what, F(SANS, 8.5), R - dx - 84)[:2],
                      F(SANS, 8.5), INK, 10.5)
        yy += 4.5

    # small cards: 4 cols x 3 rows
    cy0, chh, cgap = 702, 58, 4
    ccw = (976 - 3 * 8) / 4
    for idx, (num, ic, tag, head, sub) in enumerate(CARDS):
        r, c = divmod(idx, 4)
        cx = M + c * (ccw + 8)
        cy = cy0 + r * (chh + cgap)
        d.rectangle([cx, cy, cx + ccw, cy + chh], fill=PAPER, outline=(206, 196, 168), width=1)
        icon(d, ic, int(cx + 5), int(cy + 9), 40)
        tx = cx + 50
        d.text((tx, cy + 4), tag, font=F(SANS_B, 7.5), fill=TAG_COLORS[tag])
        nb = "%d." % num
        d.text((cx + ccw - tw(d, nb, F(SANS_B, 9)) - 5, cy + 3), nb, font=F(SANS_B, 9), fill=FAINT)
        fh = F(SANS_B, 10.5)
        yy = lines_at(d, tx, cy + 13, wrap(d, head, fh, ccw - 56)[:2], fh, INK, 12.5)
        fsb = F(SANS, 8.5)
        lines_at(d, tx, yy + 1, wrap(d, sub, fsb, ccw - 56)[:2], fsb, FAINT, 10.5)

    # also in the day
    ay = 890
    d.text((M, ay), "ALSO IN THE DAY", font=F(SANS_B, 12), fill=INK)
    leg = "TAGS: REPORTED = confirmed by named outlets - CLAIM = one side's claim - ONGOING = still developing"
    d.text((R - tw(d, leg, F(SANS, 8.5)), ay + 2), leg, font=F(SANS, 8.5), fill=FAINT)
    d.line([M, ay + 16, R, ay + 16], fill=RULE, width=1)
    fa = F(SANS, 9)
    fab = F(SANS_B, 9)
    col1 = ALSO[:10]
    col2 = ALSO[10:]
    for j, items in enumerate((col1, col2)):
        cx = M if j == 0 else 512
        yy = ay + 22
        for num, text, src in items:
            nb = "%d" % num
            d.text((cx, yy), nb, font=fab, fill=RED)
            d.text((cx + 20, yy), text + " - " + src, font=fa, fill=INK)
            yy += 10.0
    credit = ("All stories checked against Nov 23, 2026 reporting - sources named on the "
              "page - drawn in Pillow, no photographs")
    d.text(((W - tw(d, credit, F(SANS, 8))) / 2, 1014), credit, font=F(SANS, 8), fill=FAINT)

    out = os.path.join(HERE, "entry.png")
    img.save(out)
    return out

if __name__ == "__main__":
    p = build()
    import hashlib
    data = open(p, "rb").read()
    print(p, len(data), hashlib.sha256(data).hexdigest())
