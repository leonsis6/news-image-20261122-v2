#!/usr/bin/env python3
"""Render the news-image-20261122 v2 front page: 1024x1024 PNG, code-drawn text only.

Content comes ONLY from STORIES.md (36 verified stories, UTC timeline, numbers
strip, map counts, DATE CHECK, source footer). No invented numbers or claims.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
CREAM = (248, 244, 231)
PANEL = (240, 235, 218)
MAP_BG = (233, 238, 240)
LAND = (216, 203, 172)
LAND_EDGE = (120, 110, 88)
INK = (18, 18, 18)
GREY = (90, 86, 76)
RED = (172, 32, 28)
RED_DK = (140, 24, 22)
BLUE = (38, 70, 110)

F = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = F + "DejaVuSerif-Bold.ttf"
SERIF = F + "DejaVuSerif.ttf"
SANS = F + "DejaVuSans.ttf"
SANS_B = F + "DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, width):
    """Greedy word wrap; returns list of lines that fit `width` px."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if fnt.getlength(t) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, x, y, text, fnt, width, fill=INK, spacing=3, align="left"):
    lines = wrap(text, fnt, width)
    for ln in lines:
        if align == "center":
            lx = x + (width - fnt.getlength(ln)) / 2
        else:
            lx = x
        d.text((lx, y), ln, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def text_h(fnt, lines=1, spacing=3):
    return lines * (fnt.size + spacing) - spacing


img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)
MX = 14                      # side margin
CW = W - 2 * MX               # content width = 996
y = 8

# ---------- 1. kicker ----------
f_kick = font(SANS_B, 15)
d.text(((W - f_kick.getlength("ONE DAY OF WORLD NEWS, ONE PICTURE")) / 2, y),
       "ONE DAY OF WORLD NEWS, ONE PICTURE", font=f_kick, fill=RED)
y += 18

# ---------- 2. count line ----------
f_count = font(SANS, 12)
s = "36 STORIES  ·  7 REGIONS  ·  EVERY ONE DATED SUNDAY 22 NOVEMBER 2026"
d.text(((W - f_count.getlength(s)) / 2, y), s, font=f_count, fill=INK)
y += 15

# ---------- 3. masthead ----------
f_mast = font(SERIF_B, 38)
mast = "SUNDAY 22 NOVEMBER 2026"
while f_mast.getlength(mast) > CW and f_mast.size > 30:
    f_mast = font(SERIF_B, f_mast.size - 1)
d.text(((W - f_mast.getlength(mast)) / 2, y), mast, font=f_mast, fill=INK)
y += f_mast.size + 5
d.line([(MX, y), (W - MX, y)], fill=INK, width=2)
y += 5

# ---------- section header helper ----------
def section_header(title):
    global y
    f = font(SANS_B, 13)
    d.text((MX, y), title, font=f, fill=INK)
    y += 15
    d.line([(MX, y), (W - MX, y)], fill=INK, width=1)
    y += 4
    return y

# ---------- 4. THE DAY IN UTC ----------
section_header("THE DAY IN UTC")
f_time = font(SANS_B, 10)
f_t = font(SANS, 10)
utc = [
    ("01:00 UTC", "Hong Kong polls open (09:00 local)"),
    ("03:00 UTC", "Drone hits a block in Dymer, near Kyiv (05:00 Kyiv time)"),
    ("06:00 UTC", "Verstappen wins the Las Vegas Grand Prix (Saturday night, local)"),
    ("08:00 UTC", "Ukraine air force reports 186 drones launched overnight, 161 downed"),
    ("16:30 UTC", "Liverpool v Man Utd kicks off at Anfield (17:30 CET)"),
    ("EVENING", "COP31 talks collapse in Antalya; no final deal"),
]
col_w = (CW - 2 * 12) // 3
for row in range(2):
    row_h = 0
    for col in range(3):
        t, txt = utc[row * 3 + col]
        x0 = MX + col * (col_w + 12)
        lines = wrap(txt, f_t, col_w - 78)
        hh = max(text_h(f_t, len(lines), 2), 12)
        row_h = max(row_h, hh)
        d.text((x0, y), t, font=f_time, fill=RED)
        draw_wrapped(d, x0 + 78, y, txt, f_t, col_w - 78, spacing=2)
    y += row_h + 2
y += 1

# ---------- 5. THE DAY IN NUMBERS ----------
section_header("THE DAY IN NUMBERS")
nums = [
    ("186", "drones Russia launched at Ukraine overnight"),
    ("161", "downed or jammed by Ukrainian air defences"),
    ("258", "House seats for the Democrats, largest since 1992"),
    ("720/9", "India's declared total in Wellington, a record on NZ soil"),
    ("24", "body bags recovered from the Banten factory fire"),
    ("50", "points for Wembanyama (19 rebounds, 5 blocks, 4 steals)"),
]
f_num = font(SERIF_B, 24)
f_lab = font(SANS, 8)
ncol = CW // 6
for i, (n, lab) in enumerate(nums):
    x0 = MX + i * ncol
    d.text((x0 + (ncol - f_num.getlength(n)) / 2, y), n, font=f_num, fill=RED)
    ly = y + 28
    draw_wrapped(d, x0 + 4, ly, lab, f_lab, ncol - 8, spacing=1, align="center")
    if i < 5:
        d.line([(x0 + ncol - 1, y + 2), (x0 + ncol - 1, y + 50)], fill=GREY, width=1)
y += 52
d.line([(MX, y), (W - MX, y)], fill=INK, width=1)
y += 6

# ---------- vector-art helpers ----------
def art_globe(d, x, y, w, h):
    cx, cy, r = x + w // 2, y + h // 2 + 2, h // 2 - 4
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=BLUE, width=2)
    d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=BLUE, width=1)
    d.line([(cx - r, cy), (cx + r, cy)], fill=BLUE, width=1)
    d.line([(cx - r + 6, cy - r + 8), (cx + 2, cy - 4), (cx - 6, cy + 6),
            (cx + r - 8, cy + r - 6)], fill=RED, width=3)

def art_drones(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(226, 232, 238), outline=GREY)
    for dx, dy, s in [(18, 10, 5), (w // 2, 6, 4), (w - 22, 14, 5)]:
        d.line([(x + dx - s, y + dy - s), (x + dx + s, y + dy + s)], fill=INK, width=1)
        d.line([(x + dx - s, y + dy + s), (x + dx + s, y + dy - s)], fill=INK, width=1)
        for ox, oy in [(-s, -s), (s, -s), (-s, s), (s, s)]:
            d.ellipse([x + dx + ox - 2, y + dy + oy - 2, x + dx + ox + 2, y + dy + oy + 2],
                      outline=INK, width=1)
        d.ellipse([x + dx - 2, y + dy - 2, x + dx + 2, y + dy + 2], fill=RED)
    bx, by, bw, bh = x + w // 2 - 26, y + h - 22, 52, 22
    d.rectangle([bx, by, bx + bw, by + bh], outline=INK, width=2)
    d.line([(bx, by), (bx + 14, by - 8), (bx + 26, by)], fill=INK, width=2)
    for wy in (by + 6, by + 13):
        for wx in (bx + 6, bx + 18, bx + 30, bx + 42):
            d.rectangle([wx, wy, wx + 5, wy + 4], fill=INK)

def art_ship(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(226, 232, 238), outline=GREY)
    for wy in (y + h - 12, y + h - 7):
        for wx in range(x + 4, x + w - 4, 16):
            d.arc([wx, wy, wx + 14, wy + 8], 180, 360, fill=BLUE, width=2)
    d.polygon([(x + w // 2 - 34, y + 16), (x + w // 2 + 34, y + 24),
               (x + w // 2 + 24, y + 34), (x + w // 2 - 26, y + 28)], fill=INK)
    d.rectangle([x + w // 2 - 8, y + 6, x + w // 2 + 2, y + 18], fill=INK)
    d.line([(x + w // 2 - 30, y + 20), (x + w // 2 - 12, y + 12)], fill=RED, width=2)

def art_icon(d, x, y, kind):
    """Small 24x20 icon for a card, drawn at (x, y)."""
    if kind == "blast":
        d.rectangle([x + 2, y + 10, x + 13, y + 19], outline=INK, width=2)
        d.rectangle([x + 4, y + 5, x + 7, y + 10], outline=INK, width=1)
        d.line([(x + 16, y + 2), (x + 19, y + 6)], fill=RED, width=2)
        d.line([(x + 21, y + 5), (x + 22, y + 9)], fill=RED, width=2)
        d.line([(x + 15, y + 9), (x + 19, y + 11)], fill=RED, width=2)
    elif kind == "flame":
        d.polygon([(x + 12, y + 1), (x + 19, y + 10), (x + 16, y + 19),
                   (x + 8, y + 19), (x + 5, y + 10)], outline=RED, width=2)
        d.polygon([(x + 12, y + 9), (x + 15, y + 14), (x + 9, y + 14)], fill=RED)
    elif kind == "capitol":
        d.polygon([(x + 4, y + 9), (x + 12, y + 2), (x + 20, y + 9)], outline=INK, width=2)
        d.rectangle([x + 4, y + 10, x + 20, y + 13], outline=INK, width=1)
        d.rectangle([x + 3, y + 14, x + 21, y + 19], outline=INK, width=2)
    elif kind == "tow":
        d.polygon([(x + 1, y + 8), (x + 14, y + 8), (x + 12, y + 15), (x + 3, y + 15)],
                  outline=INK, width=2)
        d.line([(x + 14, y + 11), (x + 22, y + 11)], fill=INK, width=2)
        d.ellipse([x + 19, y + 14, x + 23, y + 18], outline=INK, width=2)
    elif kind == "cricket":
        d.line([(x + 5, y + 18), (x + 16, y + 4)], fill=INK, width=3)
        d.ellipse([x + 17, y + 12, x + 23, y + 18], fill=RED)
    elif kind == "race":
        d.polygon([(x + 2, y + 5), (x + 12, y + 5), (x + 9, y + 14), (x + 1, y + 14)],
                  outline=INK, width=2)
        d.ellipse([x + 4, y + 14, x + 8, y + 18], outline=INK, width=2)
        d.ellipse([x + 14, y + 14, x + 18, y + 18], outline=INK, width=2)
        d.rectangle([x + 19, y + 3, x + 23, y + 7], fill=INK)
        d.rectangle([x + 19, y + 8, x + 23, y + 12], outline=INK, width=1)
    elif kind == "hoop":
        d.ellipse([x + 4, y + 3, x + 20, y + 19], outline=RED, width=2)
        d.arc([x + 4, y + 3, x + 20, y + 19], 0, 180, fill=INK, width=1)
        d.line([(x + 4, y + 11), (x + 20, y + 11)], fill=INK, width=1)
    elif kind == "soccer":
        d.ellipse([x + 4, y + 2, x + 20, y + 18], outline=INK, width=2)
        d.polygon([(x + 10, y + 7), (x + 14, y + 7), (x + 15, y + 11),
                   (x + 12, y + 14), (x + 9, y + 11)], fill=INK)
    elif kind == "ballot":
        d.rectangle([x + 5, y + 8, x + 19, y + 19], outline=INK, width=2)
        d.line([(x + 5, y + 8), (x + 12, y + 2), (x + 19, y + 8)], fill=INK, width=2)
        d.line([(x + 9, y + 13), (x + 11, y + 16), (x + 16, y + 10)], fill=RED, width=2)
    elif kind == "chart":
        d.line([(x + 3, y + 4), (x + 9, y + 10), (x + 14, y + 7), (x + 21, y + 16)],
               fill=RED, width=2)
        d.polygon([(x + 21, y + 16), (x + 16, y + 16), (x + 21, y + 11)], fill=RED)

# ---------- 6. LEADS ----------
leads = [
    ("1", "COP31 COLLAPSES", "UN climate talks end Sunday with no deal; the EU and island states reject a draft that never mentions fossil fuels. First COP failure since Copenhagen 2009; longest summit on record.",
     "CONFIRMED (Bloomberg / NYT / Irish Times)", "ANTALYA, TURKEY", art_globe),
    ("2", "186 DRONES OVER UKRAINE", "Russia launches 186 drones overnight, 72 of them jet-powered; air defences down or jam 161; strikes at 18 sites. In Dymer a drone partly collapses a five-storey block; 14 missing.",
     "CONFIRMED (Ukraine Air Force)", "DYMER, UKRAINE", art_drones),
    ("3", "CORVETTE HIT AT BENGHAZI", "Sea drones strike the Russian corvette Merkury at Libya's Benghazi naval base; the ship is severely damaged and capsized at its berth; 10 hurt. Kyiv and Moscow say nothing on Sunday.",
     "REPORTED (AP / Libyan officials)", "BENGHAZI, LIBYA", art_ship),
]
LEAD_H = 146
lead_w = (CW - 2 * 10) // 3
f_lead_h = font(SERIF_B, 16)
f_lead_b = font(SANS, 10)
f_lead_t = font(SANS_B, 8)
lead_top = y
for i, (num, head, body, tag, place, art) in enumerate(leads):
    x0 = MX + i * (lead_w + 10)
    d.rectangle([x0, y, x0 + lead_w - 1, y + LEAD_H - 1], outline=GREY, width=1)
    art(d, x0 + 6, y + 5, lead_w - 12, 42)
    hy = y + 50
    d.text((x0 + 6, hy), num + ".", font=f_lead_h, fill=RED)
    hl = wrap(head, f_lead_h, lead_w - 12 - f_lead_h.getlength(num + ". "))
    yy = hy
    for ln in hl:
        d.text((x0 + 6 + (f_lead_h.getlength(num + ". ") if ln == hl[0] else 0), yy),
               ln, font=f_lead_h, fill=INK)
        yy += 18
    by = yy + 1
    by = draw_wrapped(d, x0 + 6, by, body, f_lead_b, lead_w - 12, spacing=1)
    d.text((x0 + 6, y + LEAD_H - 13), place, font=f_lead_t, fill=GREY)
    tw = f_lead_t.getlength(tag)
    d.text((x0 + lead_w - 6 - tw, y + LEAD_H - 13), tag, font=f_lead_t, fill=RED)
y = lead_top + LEAD_H + 6

# ---------- 7. CARDS 4-13 ----------
cards = [
    ("4", "BAHRAIN", "An Iranian strike hits a civilian industrial site, 2 hurt, 1 critical; Tehran claims 2 US Patriot radars destroyed.",
     "OFFICIAL (Bahrain) + REPORTED (Iran claim)", "blast"),
    ("5", "BANTEN FIRE", "24 body bags recovered from the Cikande candy factory; 34 workers missing; the death toll is not yet confirmed.",
     "CONFIRMED (AP / Reuters)", "flame"),
    ("6", "DEMOCRATS 258", "At least 258 House seats, the largest majority since 1992; Hubbard beats Foxx by 330 votes in N. Carolina.",
     "CONFIRMED (AP)", "capitol"),
    ("7", "SPARTA II TOWED OUT", "The drone-hit Russian cargo ship leaves Finnish waters Sunday after a multinational rescue; 16 crew evacuated.",
     "CONFIRMED (Yle / Reuters)", "tow"),
    ("8", "INDIA 720/9", "India declares on a record 720 for 9, the highest Test total on New Zealand soil.",
     "CONFIRMED", "cricket"),
    ("9", "VERSTAPPEN WINS VEGAS", "From pole, beats Norris and Piastri after 35 lead changes; his 75th career win.",
     "CONFIRMED (AP / ESPN)", "race"),
    ("10", "WEMBANYAMA 50", "50 points, 19 rebounds, 5 blocks, 4 steals; Spurs beat Pelicans 114-91; the first ever 50/15/5/4 line.",
     "CONFIRMED (AP)", "hoop"),
    ("11", "LIVERPOOL 4-0 MAN UTD", "Pochettino's first game as United boss ends in a rout at Anfield; Yoro sent off after 8 minutes.",
     "CONFIRMED", "soccer"),
    ("12", "HONG KONG VOTES", "Election Committee poll: 856 candidates for 723 seats; turnout near 99%, a record.",
     "CONFIRMED (SCMP)", "ballot"),
    ("13", "MARKETS SLIDE", "S&P 500 -8.6% on the week, Nasdaq -10%; gold -8.9% to $3,538 as the AI sell-off deepens.",
     "CONFIRMED", "chart"),
]
CARD_H = 90
card_w = (CW - 4 * 8) // 5
f_card_h = font(SANS_B, 11)
f_card_b = font(SANS, 9)
f_card_t = font(SANS_B, 7)
card_top = y
for idx, (num, head, body, tag, kind) in enumerate(cards):
    r, c = divmod(idx, 5)
    x0 = MX + c * (card_w + 8)
    y0 = card_top + r * (CARD_H + 5)
    d.rectangle([x0, y0, x0 + card_w - 1, y0 + CARD_H - 1], outline=GREY, width=1)
    art_icon(d, x0 + 5, y0 + 4, kind)
    fh = f_card_h
    title = num + ". " + head
    while fh.getlength(title) > card_w - 34 and fh.size > 8:
        fh = font(SANS_B, fh.size - 1)
    d.text((x0 + 32, y0 + 6), title, font=fh, fill=INK)
    by = draw_wrapped(d, x0 + 6, y0 + 28, body, f_card_b, card_w - 12, spacing=2)
    tw = f_card_t.getlength(tag)
    d.text((x0 + card_w - 6 - tw, y0 + CARD_H - 11), tag, font=f_card_t, fill=RED)
y = card_top + 2 * CARD_H + 5 + 4

# ---------- 8. WHERE IT HAPPENED — world map ----------
section_header("WHERE IT HAPPENED")
map_x0, map_y0 = MX, y
map_w, map_h = CW, 118
d.rectangle([map_x0, map_y0, map_x0 + map_w - 1, map_y0 + map_h - 1],
            fill=MAP_BG, outline=GREY, width=1)
LON0, LON1, LAT0, LAT1 = -170.0, 190.0, 80.0, -52.0
def proj(lon, lat):
    return (map_x0 + (lon - LON0) / (LON1 - LON0) * map_w,
            map_y0 + (LAT0 - lat) / (LAT0 - LAT1) * map_h)
for glon in range(-150, 181, 30):
    x = proj(glon, 0)[0]
    d.line([(x, map_y0), (x, map_y0 + map_h)], fill=(210, 218, 222), width=1)
for glat in (60, 30, 0, -30):
    yy = proj(0, glat)[1]
    d.line([(map_x0, yy), (map_x0 + map_w, yy)], fill=(210, 218, 222), width=1)
NA = [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 60), (-55, 47),
      (-70, 42), (-75, 35), (-80, 26), (-85, 20), (-90, 15), (-97, 16), (-105, 20),
      (-110, 24), (-117, 33), (-125, 40), (-125, 49), (-140, 60), (-155, 58), (-165, 60)]
SA = [(-80, 10), (-75, 5), (-60, 0), (-50, 0), (-40, -5), (-35, -10), (-40, -20),
      (-48, -28), (-58, -35), (-65, -45), (-70, -55), (-73, -40), (-72, -20),
      (-77, -12), (-80, -5)]
AF = [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
      (43, 12), (51, 11), (48, 0), (40, -10), (35, -20), (30, -30), (20, -35),
      (15, -28), (12, -18), (9, -1), (9, 4), (-8, 5), (-15, 11)]
EU = [(-9, 37), (-9, 43), (-2, 48), (0, 50), (3, 53), (7, 55), (8, 57), (12, 55),
      (18, 56), (21, 55), (24, 58), (28, 60), (30, 63), (32, 68), (40, 68),
      (55, 69), (68, 70), (80, 73), (100, 77), (120, 73), (140, 72),
      (160, 70), (178, 65), (170, 60), (162, 56), (158, 52), (150, 59), (142, 55),
      (140, 45), (135, 43), (130, 42), (127, 40), (126, 38), (122, 31), (120, 28),
      (115, 23), (110, 20), (108, 18), (105, 10), (103, 8), (100, 8), (98, 10),
      (95, 16), (92, 21), (90, 22), (88, 22), (86, 20), (83, 18), (80, 15),
      (77, 8), (76, 10), (73, 16), (72, 20), (70, 22), (67, 24), (64, 25),
      (61, 25), (58, 25), (56, 26), (54, 26), (52, 27), (50, 29), (48, 30),
      (52, 26), (54, 24), (56, 23), (58, 22), (59, 22), (57, 19),
      (55, 17), (52, 16), (48, 14), (44, 13), (43, 12), (42, 15), (41, 18),
      (39, 21), (38, 24), (37, 27), (36, 29), (35, 29), (36, 36), (33, 36),
      (30, 36), (27, 37), (23, 36), (22, 37), (19, 40), (16, 38), (15, 40),
      (12, 44), (8, 44), (3, 43), (0, 40), (-2, 37), (-6, 36)]
AU = [(114, -22), (114, -30), (115, -35), (120, -34), (124, -33), (129, -32),
      (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
      (153, -32), (153, -27), (150, -23), (146, -19), (142, -15), (142, -11),
      (140, -17), (136, -15), (135, -12), (132, -11), (130, -13), (126, -14),
      (122, -17), (118, -20)]
for poly in (NA, SA, AF, EU, AU):
    d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND, outline=LAND_EDGE)
for lon, lat, rx, ry in [(140, 38, 5, 8), (-1, 54, 4, 6), (172, -41, 4, 8), (-18, 65, 4, 3)]:
    cx, cy = proj(lon, lat)
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=LAND, outline=LAND_EDGE)
# pins: (num, lat, lon, dx, dy) — dx/dy nudge crowded pins; leader line from true spot
pins = [
    (1, 36.9, 30.7, 16, 4), (2, 50.8, 30.3, 4, -13), (3, 32.1, 20.1, -11, 8),
    (4, 26.2, 50.6, -7, 13), (5, -6.3, 106.3, 0, 0), (6, 38.9, -77.0, -13, 9),
    (7, 59.8, 25.0, -6, -6), (8, -41.3, 174.8, 0, -2), (9, 36.2, -115.1, 0, 0),
    (10, 29.4, -98.5, 0, 6), (11, 53.4, -3.0, -12, -4), (12, 22.3, 114.2, 0, 0),
    (13, 40.7, -74.0, 10, 8), (14, 28.6, 77.2, 6, 9), (15, 23.7, 121.0, 0, 0),
    (16, 15.6, 32.5, 2, 11), (17, 31.9, 35.2, -12, 10), (18, 31.5, 74.3, -9, -7),
    (19, 26.2, 127.7, 0, 0), (20, 30.5, 47.8, -16, 6), (21, 47.9, 106.9, 0, 0),
    (22, 35.7, 51.4, 3, -13), (23, 50.8, 4.4, -6, 9), (24, 23.8, 90.4, -9, -7),
    (25, 21.9, 96.0, 10, -6), (26, 38.9, -77.0, 14, -12), (27, 24.0, 54.0, 15, 10),
    (28, 26.2, 56.2, 13, -3), (29, 39.0, -98.0, -2, -9), (30, 51.0, 10.0, 7, -10),
    (31, 35.7, 139.7, 0, 0), (32, 23.8, 90.4, 9, 7), (33, 32.2, 34.8, 16, -12),
    (34, 46.5, 30.7, -16, 8), (35, 47.0, 28.9, 8, 2), (36, -33.9, 151.2, 0, 0),
]
f_pin = font(SANS_B, 7)
for num, lat, lon, dx, dy in pins:
    tx, ty = proj(lon, lat)
    px, py = tx + dx, ty + dy
    if dx or dy:
        d.line([(tx, ty), (px, py)], fill=GREY, width=1)
        d.ellipse([tx - 1.5, ty - 1.5, tx + 1.5, ty + 1.5], fill=INK)
    r = 7
    d.ellipse([px - r, py - r, px + r, py + r], fill=(255, 255, 255),
              outline=RED, width=1)
    s = str(num)
    d.text((px - f_pin.getlength(s) / 2, py - 5), s, font=f_pin, fill=RED_DK)
y = map_y0 + map_h + 4
f_reg = font(SANS_B, 10)
regs = "Europe 8  ·  Middle East 7  ·  Asia 11  ·  Africa 2  ·  Americas 5  ·  Oceania 2  ·  World 1"
d.text(((W - f_reg.getlength(regs)) / 2, y), regs, font=f_reg, fill=INK)
y += 13

# ---------- 9. ALSO ON SUNDAY — briefs 14-36 ----------
section_header("ALSO ON SUNDAY")
briefs = [
    ("14", "Nepal PM Shah arrives in Delhi for a two-day state visit; talks with Modi on Monday.", "CONFIRMED"),
    ("15", "Taiwan tracks 24 Chinese sorties, 17 median-line crossings, 11 ships, 2 balloons.", "CONFIRMED (Taiwan MND)"),
    ("16", "Drone strikes hit Khartoum early Sunday, damaging a UN facility; 3 killed in Omdurman.", "REPORTED"),
    ("17", "Settlers torch 12 Palestinian vehicles in 4 villages near Ramallah overnight.", "REPORTED (Reuters / AP)"),
    ("18", "Lahore is the world's most polluted major city again, AQI 538 on Sunday morning.", "CONFIRMED (Dawn / IQAir)"),
    ("19", "Shuri Castle's main hall reopens, 7 years after the 2019 fire.", "CONFIRMED"),
    ("20", "Fire at the Hartha power station kills 4, injures about 30.", "REPORTED"),
    ("21", "Parliament approves President Khurelsukh's resignation; a snap vote is ahead.", "REPORTED"),
    ("22", "Iran resumes scheduled power cuts from Sunday as the cold season starts.", "REPORTED (Tavanir)"),
    ("23", "Air traffic controllers join Monday's national strike; flights to be grounded.", "CONFIRMED"),
    ("24", "773 arrested in Dhaka operations, incl. 181 Awami League members.", "REPORTED"),
    ("25", "Army-backed government calls ASEAN exclusion unfair after the ICJ genocide ruling.", "REPORTED (Reuters)"),
    ("26", "Trump tells European leaders ending the Ukraine war would free resources for home needs.", "CONFIRMED (Reuters)"),
    ("27", "US-Iran contacts continue through mediators; positions still far apart.", "CONFIRMED (Reuters)"),
    ("28", "Tankers near Khasab: UKMTO investigates a reported stern strike.", "REPORTED"),
    ("29", "Delta: 1,000+ flights delayed on 22 Nov after an automation glitch.", "REPORTED"),
    ("30", "Lufthansa to cut up to 1,000 jobs over fuel costs.", "REPORTED"),
    ("31", "Japan's economy shrinks in Q3, -0.02% on the quarter.", "REPORTED"),
    ("32", "Garment factories shut as workers strike over pay.", "REPORTED"),
    ("33", "Likud and Yashar meet 4 hours, still split on the next government.", "REPORTED (Al Jazeera)"),
    ("34", "Strikes cripple power lines; the city is short of electricity, water and heating.", "REPORTED (Ukrenergo)"),
    ("35", "A Russian jet drone crossed into Moldova twice.", "REPORTED"),
    ("36", "AUKUS: Australia's Marles calls a US report on submarine numbers wrong.", "CONFIRMED (Reuters)"),
]
f_br = font(SANS, 8)
f_brb = font(SANS_B, 8)
brief_col_w = (CW - 16) // 2
brief_top = y
for i, (num, txt, tag) in enumerate(briefs):
    col = 0 if i < 12 else 1
    row = i if i < 12 else i - 12
    x0 = MX + col * (brief_col_w + 16)
    yy = brief_top + row * 11.5
    d.text((x0, yy), num + ".", font=f_brb, fill=RED)
    full = txt + " " + tag
    lines = wrap(full, f_br, brief_col_w - 26)
    ly = yy
    for ln in lines:
        d.text((x0 + 26, ly), ln, font=f_br, fill=INK)
        ly += 10
    if len(lines) > 1:
        print("WARN brief", num, "wrapped to", len(lines), "lines")
y = brief_top + 12 * 11.5 + 1

# ---------- 10. DATE CHECK ----------
section_header("DATE CHECK — LEFT OUT ON PURPOSE")
dc = [
    "El Chapo Isidro captured — raid Fri 20 Nov, reported Sat 21 Nov.",
    "Kryvyi Rih strike — Fri 20 Nov evening.",
    "Peru Junin quake — Fri 20 Nov, 19:09 local.",
    "Bolsonaro to ICU — Sat 21 Nov.",
    "FBI crime-database hack — reported Fri 20 Nov.",
    "Estonia border closure — announced 15-16 Nov.",
    "Denmark expels Russian attache — Fri 20 Nov.",
    "Somalia expels UAE envoy — Thu 19 Nov.",
    "Kenya's last Ebola patient — discharged Wed 11 Nov.",
    "H-6 bomber near Manila — Fri 21 Nov.",
    "BepiColombo enters Mercury orbit — Sat 21 Nov.",
    "EU-Indonesia trade deal — signed Sat 21 Nov.",
]
f_dc = font(SANS, 8)
dc_top = y
for i, item in enumerate(dc):
    col = 0 if i < 7 else 1
    row = i if i < 7 else i - 7
    x0 = MX + col * (brief_col_w + 16)
    d.text((x0, dc_top + row * 10), "·  " + item, font=f_dc, fill=GREY)
y = dc_top + 7 * 10 + 1
f_ny = font(SANS_B, 8)
ny = ("Not yet:  Merkury attribution (Kyiv/Moscow silent on 22 Nov)  ·  "
      "Banten death toll (DNA checks pending)  ·  COP31 final text (none agreed)")
ny_lines = wrap(ny, f_ny, CW)
for ln in ny_lines:
    d.text((MX, y), ln, font=f_ny, fill=INK)
    y += 10

# ---------- 11. source footer ----------
y += 1
d.line([(MX, y), (W - MX, y)], fill=INK, width=1)
y += 4
f_ft = font(SANS, 8)
f_ftb = font(SANS_B, 8)
src = "Sources: Reuters · AP · AFP · BBC · Al Jazeera · Yle · SCMP · Taiwan MND · Ukraine Air Force"
d.text((MX, y), src, font=f_ft, fill=INK)
y += 10
leg = ("CONFIRMED = wire/official confirmation   ·   OFFICIAL = on-the-record statement   ·   "
       "REPORTED = single outlet / attribution not yet confirmed")
d.text((MX, y), leg, font=f_ft, fill=GREY)
y += 10
print("final y =", y, "of", H, "-> overflow!" if y > H else "-> fits")
img.save("entry.png", optimize=True)
print("saved entry.png")
