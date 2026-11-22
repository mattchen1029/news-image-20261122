#!/usr/bin/env python3
"""news-image-20261122: one-day world news front page, Sunday 22 November 2026.

Pure standard library. Draws a 1024x1024 newspaper front page and writes it
to $MAKEFUN_OUTPUT_DIR/entry.png (default out/). Deterministic: no random,
no timestamps, no network, no external files.
"""
import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
PAPER = (247, 243, 232)
INK = (26, 26, 26)
NAVY = (18, 30, 58)
NAVY2 = (30, 46, 84)
RED = (178, 34, 34)
GOLD = (201, 162, 39)
GREY = (110, 108, 100)
LIGHT = (232, 226, 210)
TEAL = (31, 94, 94)
SKY = (214, 230, 238)
SEA = (46, 80, 110)

# ---------------------------------------------------------------- 5x7 font
# Each glyph: 7 rows of 5 bits. Classic public-domain style 5x7 set.
F = {}
def _g(ch, rows):
    F[ch] = rows

_g("A", ("01110","10001","10001","11111","10001","10001","10001"))
_g("B", ("11110","10001","10001","11110","10001","10001","11110"))
_g("C", ("01110","10001","10000","10000","10000","10001","01110"))
_g("D", ("11110","10001","10001","10001","10001","10001","11110"))
_g("E", ("11111","10000","10000","11110","10000","10000","11111"))
_g("F", ("11111","10000","10000","11110","10000","10000","10000"))
_g("G", ("01110","10001","10000","10111","10001","10001","01111"))
_g("H", ("10001","10001","10001","11111","10001","10001","10001"))
_g("I", ("01110","00100","00100","00100","00100","00100","01110"))
_g("J", ("00111","00010","00010","00010","00010","10010","01100"))
_g("K", ("10001","10010","10100","11000","10100","10010","10001"))
_g("L", ("10000","10000","10000","10000","10000","10000","11111"))
_g("M", ("10001","11011","10101","10101","10001","10001","10001"))
_g("N", ("10001","11001","10101","10011","10001","10001","10001"))
_g("O", ("01110","10001","10001","10001","10001","10001","01110"))
_g("P", ("11110","10001","10001","11110","10000","10000","10000"))
_g("Q", ("01110","10001","10001","10001","10101","10010","01101"))
_g("R", ("11110","10001","10001","11110","10100","10010","10001"))
_g("S", ("01111","10000","10000","01110","00001","00001","11110"))
_g("T", ("11111","00100","00100","00100","00100","00100","00100"))
_g("U", ("10001","10001","10001","10001","10001","10001","01110"))
_g("V", ("10001","10001","10001","10001","10001","01010","00100"))
_g("W", ("10001","10001","10001","10101","10101","10101","01010"))
_g("X", ("10001","10001","01010","00100","01010","10001","10001"))
_g("Y", ("10001","10001","01010","00100","00100","00100","00100"))
_g("Z", ("11111","00001","00010","00100","01000","10000","11111"))
_g("a", ("00000","00000","01110","00001","01111","10001","01111"))
_g("b", ("10000","10000","11110","10001","10001","10001","11110"))
_g("c", ("00000","00000","01110","10001","10000","10001","01110"))
_g("d", ("00001","00001","01111","10001","10001","10001","01111"))
_g("e", ("00000","00000","01110","10001","11111","10000","01110"))
_g("f", ("00110","01001","01000","11110","01000","01000","01000"))
_g("g", ("00000","01111","10001","10001","01111","00001","01110"))
_g("h", ("10000","10000","11110","10001","10001","10001","10001"))
_g("i", ("00100","00000","01100","00100","00100","00100","01110"))
_g("j", ("00010","00000","00110","00010","00010","00010","01100"))
_g("k", ("10000","10000","10010","10100","11000","10100","10010"))
_g("l", ("01100","00100","00100","00100","00100","00100","01110"))
_g("m", ("00000","00000","11010","10101","10101","10101","10101"))
_g("n", ("00000","00000","11110","10001","10001","10001","10001"))
_g("o", ("00000","00000","01110","10001","10001","10001","01110"))
_g("p", ("00000","00000","11110","10001","10001","11110","10000"))
_g("q", ("00000","00000","01111","10001","10001","01111","00001"))
_g("r", ("00000","00000","10110","11001","10000","10000","10000"))
_g("s", ("00000","00000","01111","10000","01110","00001","11110"))
_g("t", ("01000","01000","11110","01000","01000","01001","00110"))
_g("u", ("00000","00000","10001","10001","10001","10011","01101"))
_g("v", ("00000","00000","10001","10001","10001","01010","00100"))
_g("w", ("00000","00000","10001","10101","10101","10101","01010"))
_g("x", ("00000","00000","10001","01010","00100","01010","10001"))
_g("y", ("00000","00000","10001","10001","01111","00001","01110"))
_g("z", ("00000","00000","11111","00010","00100","01000","11111"))
_g("0", ("01110","10001","10011","10101","11001","10001","01110"))
_g("1", ("00100","01100","00100","00100","00100","00100","01110"))
_g("2", ("01110","10001","00001","00110","01000","10000","11111"))
_g("3", ("11111","00010","00100","00010","00001","10001","01110"))
_g("4", ("00010","00110","01010","10010","11111","00010","00010"))
_g("5", ("11111","10000","11110","00001","00001","10001","01110"))
_g("6", ("00110","01000","10000","11110","10001","10001","01110"))
_g("7", ("11111","00001","00010","00100","01000","01000","01000"))
_g("8", ("01110","10001","10001","01110","10001","10001","01110"))
_g("9", ("01110","10001","10001","01111","00001","00010","01100"))
_g(" ", ("00000","00000","00000","00000","00000","00000","00000"))
_g(".", ("00000","00000","00000","00000","00000","01100","01100"))
_g(",", ("00000","00000","00000","00000","01100","00100","01000"))
_g("!", ("00100","00100","00100","00100","00100","00000","00100"))
_g("?", ("01110","10001","00001","00110","00100","00000","00100"))
_g("-", ("00000","00000","00000","01110","00000","00000","00000"))
_g("\u2013", ("00000","00000","00000","01110","00000","00000","00000"))
_g("\u2014", ("00000","00000","00000","11111","00000","00000","00000"))
_g("'", ("00100","00100","01000","00000","00000","00000","00000"))
_g("\u2019", ("00100","00100","01000","00000","00000","00000","00000"))
_g("\u201c", ("01010","01010","00000","00000","00000","00000","00000"))
_g("\u201d", ("01010","01010","00000","00000","00000","00000","00000"))
_g('"', ("01010","01010","00000","00000","00000","00000","00000"))
_g("(", ("00010","00100","01000","01000","01000","00100","00010"))
_g(")", ("01000","00100","00010","00010","00010","00100","01000"))
_g("/", ("00001","00010","00010","00100","01000","01000","10000"))
_g("%", ("11001","11010","00010","00100","01000","01011","10011"))
_g("$", ("00100","01111","10100","01110","00101","11110","00100"))
_g("&", ("01100","10010","10100","01000","10101","10010","01101"))
_g("+", ("00000","00100","00100","11111","00100","00100","00000"))
_g("=", ("00000","00000","11111","00000","11111","00000","00000"))
_g(";", ("00000","01100","00000","01100","00100","01000","00000"))
_g(":", ("00000","01100","00000","01100","00000","00000","00000"))
_g("*", ("00000","10101","01110","11111","01110","10101","00000"))
_g("#", ("01010","01010","11111","01010","11111","01010","01010"))
_g("\u00b7", ("00000","00000","00000","01100","01100","00000","00000"))
_g("\u2022", ("00000","00100","01110","01110","01110","00100","00000"))
_g("~", ("00000","00000","00000","01001","10110","00000","00000"))
_g("<", ("00010","00100","01000","10000","01000","00100","00010"))
_g(">", ("01000","00100","00010","00001","00010","00100","01000"))
_g("_", ("00000","00000","00000","00000","00000","00000","11111"))
_g("[", ("01110","01000","01000","01000","01000","01000","01110"))
_g("]", ("01110","00010","00010","00010","00010","00010","01110"))

def text_w(s, sc):
    return len(s) * 6 * sc - sc if s else 0

# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg) * (w * h)

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = c

    def rect(self, x, y, w, h, c):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            for xx in range(x0, x1):
                i = base + (xx - x0) * 3
                self.px[i], self.px[i + 1], self.px[i + 2] = c

    def hline(self, x, y, w, c, t=1):
        self.rect(x, y, w, t, c)

    def vline(self, x, y, h, c, t=1):
        self.rect(x, y, t, h, c)

    def line(self, x0, y0, x1, y1, c, t=1):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.rect(x0 - t // 2, y0 - t // 2, t, t, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, c):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, c)

    def poly(self, pts, c):
        # scanline fill
        ys = [p[1] for p in pts]
        for y in range(min(ys), max(ys) + 1):
            xs = []
            n = len(pts)
            for i in range(n):
                x0, y0 = pts[i]
                x1, y1 = pts[(i + 1) % n]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    x = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
                    xs.append(x)
            xs.sort()
            for k in range(0, len(xs) - 1, 2):
                for x in range(int(xs[k]), int(xs[k + 1]) + 1):
                    self.set(x, y, c)

    def text(self, s, x, y, sc=1, c=INK, bold=False):
        cx = x
        for ch in s:
            g = F.get(ch, F["?"])
            for r in range(7):
                row = g[r]
                for col in range(5):
                    if row[col] == "1":
                        self.rect(cx + col * sc, y + r * sc, sc, sc, c)
                        if bold:
                            self.rect(cx + col * sc + 1, y + r * sc, sc, sc, c)
            cx += 6 * sc
        return cx

    def text_c(self, s, cx, y, sc=1, c=INK, bold=False):
        self.text(s, cx - text_w(s, sc) // 2, y, sc, c, bold)

def wrap(s, maxw, sc):
    words = s.split(" ")
    lines, cur = [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if text_w(t, sc) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines

# ---------------------------------------------------------------- PNG
def write_png(cv, path):
    raw = bytearray()
    for y in range(cv.h):
        raw.append(0)
        raw += cv.px[y * cv.w * 3:(y + 1) * cv.w * 3]
    comp = zlib.compress(bytes(raw), 9)

    def chunk(typ, data):
        c = struct.pack(">I", len(data)) + typ + data
        return c + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", comp)
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)

# ---------------------------------------------------------------- story data
# All stories verified against reporting dated Sunday 22 November 2026
# (AP, Reuters, AFP, CNN, Al Jazeera, BBC, Dawn, Nikkei, Formula 1, UN News).
HEADLINES = [
    {
        "num": "1", "tag": "TURKIYE \u00b7 CLIMATE", "art": "cop",
        "title": "COP31 collapses with no deal on fossil fuels",
        "body": "UN climate talks in Antalya end in failure after 44 hours of overtime, the longest COP ever. The EU rejects a draft that never mentions fossil fuels.",
    },
    {
        "num": "2", "tag": "MIDDLE EAST \u00b7 CONFLICT", "art": "gulf",
        "title": "Iran strikes Bahrain as Gulf tensions boil over",
        "body": "Missiles and drones hit US bases and a civilian site in Bahrain; two people are hurt. Saudi Arabia intercepts a missile aimed at Makkah.",
    },
    {
        "num": "3", "tag": "EUROPE \u00b7 WAR IN UKRAINE", "art": "kyiv",
        "title": "Drone flattens a block near Kyiv; 14 feared trapped",
        "body": "A Russian drone destroys a five-storey building in Dymer overnight; two are killed. A Russian ship burns in the Baltic after a drone strike.",
    },
]
SECONDARY = [
    ("4", "NORTH AMERICA \u00b7 SECURITY", "star",
     "Mexico captures cartel boss 'El Chapo Isidro'",
     "Eleven die in the Sinaloa raid, four of them soldiers; he was FBI most-wanted."),
    ("5", "ASIA \u00b7 DISASTER", "flame",
     "Factory fire near Jakarta leaves dozens missing",
     "Three workers are dead and 36 missing after a blaze at a candy factory in Cikande."),
    ("6", "NORTH AMERICA \u00b7 SPORT", "flag",
     "Verstappen wins a Las Vegas thriller by 0.639s",
     "The Red Bull driver holds off Norris after 50 laps; Piastri storms from 17th to third."),
    ("7", "EUROPE \u00b7 SPORT", "ball",
     "Leeds thrash Chelsea 4-1; Arsenal held 2-2",
     "Leeds stun Chelsea at Stamford Bridge; Arsenal stay top after a 2-2 draw at Newcastle."),
    ("8", "GLOBAL \u00b7 MARKETS", "chart",
     "AI rout goes global as stocks slide into correction",
     "The S&P 500 falls 3.7% and the Nasdaq 5.3% in the worst week since 2020."),
    ("9", "MIDDLE EAST \u00b7 GAZA", "box",
     "Strike on Gaza food vehicle kills three",
     "Israel says it hit militants; hospital staff say the dead were carrying food."),
    ("10", "AFRICA \u00b7 DISASTER", "boat",
     "Boat capsizes in Nigeria; at least 24 dead",
     "The boat was carrying people to a funeral when it overturned."),
    ("11", "ASIA \u00b7 CULTURE", "castle",
     "Okinawa celebrates Shuri Castle, rebuilt at last",
     "Seven years after fire destroyed it, the restored main hall reopens to crowds."),
    ("12", "NORTH AMERICA \u00b7 CYBER", "shield",
     "FBI crime database hacked, Trump confirms",
     "The FBI's National Crime Information Center was breached, the president confirms."),
]
NUMBERS = [
    ("44 HRS", "COP31 ran 44 hours past its official end \u2014 the longest climate talks ever"),
    ("0.639 SEC", "Verstappen's winning margin over Norris in the Las Vegas Grand Prix"),
    ("11 DEAD", "Killed in the raid that captured cartel boss 'El Chapo Isidro' in Sinaloa"),
    ("98.5%", "Of tariffs on EU goods scrapped under the new EU\u2013Indonesia trade deal"),
]
TIMELINE = [
    ("OVERNIGHT", "A Russian drone hits a five-storey block in Dymer, near Kyiv; 14 are feared trapped."),
    ("05:37 UTC", "Verstappen takes the chequered flag in Las Vegas, 0.639 seconds ahead of Norris."),
    ("MORNING", "Rescuers search the ruins of a candy factory fire near Jakarta; 3 dead, dozens missing."),
    ("AFTERNOON", "COP31 collapses in Antalya as the EU rejects a draft with no mention of fossil fuels."),
    ("EVENING", "UN chief Guterres calls the outcome 'deeply disappointing'; next summit: Addis Ababa."),
]
BRIEFS = [
    "EU\u2013Indonesia deal \u2014 The EU and Indonesia sign a trade deal after almost 10 years of talks.",
    "Saudi shield \u2014 Saudi air defences intercept a ballistic missile allegedly aimed at Makkah.",
    "Houthi fire \u2014 Houthis fire on Saudi Arabia as Yemen exchanges fire with the kingdom.",
    "Iran pressure \u2014 Qatar and Germany call on Iran to end Houthi support and open up on nuclear.",
    "Poland alert \u2014 Russian missiles land in Poland; NATO calls it a violation.",
    "Peace talks \u2014 Kushner says Russia is 'comfortable' with NATO-like guarantees.",
    "UK\u2013EU reset \u2014 Britain and the EU strike trade and travel deals after Brexit.",
    "Lisbon march \u2014 Thousands march in Lisbon as living costs fuel anger.",
    "France protests \u2014 Protesters rally for a sixth weekend in France.",
    "Spain votes soon \u2014 Spain heads to a snap election on 29 November.",
    "Village votes out \u2014 An English village votes to 'leave the UK' over plans for a migrant camp.",
    "Big Tech tax \u2014 The EU proposes a tax on Big Tech.",
    "Killer robots \u2014 Countries open a path to an accord on 'killer robots'.",
    "Caravan north \u2014 An America-bound migrant caravan reaches Mexico.",
    "Italy loss \u2014 A former Italian police chief dies by suicide.",
    "Bundesliga \u2014 Nmecha helps Dortmund beat Gladbach and go top of the Bundesliga.",
    "Hull win \u2014 Hull City beat Brighton 2\u20130; Pochettino takes charge at Liverpool.",
    "Europe's leagues \u2014 Real Madrid beat Celta Vigo 2\u20131; Roma thrash Parma 5\u20131; Leipzig hit five.",
    "Card cap \u2014 Trump vows to work with Democrats to cap credit card interest rates at 10%.",
    "Musk warning \u2014 Elon Musk warns the AI race may hit a 'nuts' cash crunch in 2027.",
    "Anthropic IPO \u2014 Anthropic shares, which opened near $112, fall to about $85 on day two.",
    "Gold slide \u2014 Gold falls about 9.4% in the week; Goldman Sachs sees $4,650 an ounce by 2027.",
    "Cyclone Akvan \u2014 Akvan weakens over Odisha; India warns of a new Andaman Sea system.",
    "King tides \u2014 California braces for king tides from Sunday to 27 November after record rains.",
    "Sri Lanka rain \u2014 Sri Lanka forecasts fairly heavy rain, about 75mm, on Sunday.",
    "Rohingya hope \u2014 Rohingya welcome the World Court's genocide verdict but want to go home.",
    "Israel politics \u2014 Eisenkot invites Netanyahu's party to join Israeli coalition talks.",
    "AUKUS row \u2014 Australia criticises the US budget office over AUKUS comments.",
    "China rebuke \u2014 China opposes a US ban on telecom firms' phone access.",
    "Singapore fraud \u2014 Chinese national Li Ming is charged in a fraud case linked to Megaspeed.",
    "India startups \u2014 Indian startups raise about $290m in a week, up from $31m the week before.",
    "Thanksgiving travel \u2014 81 million Americans face disruption as a possible tropical storm brews.",
    "COP32 next \u2014 The next climate summit is set for Addis Ababa, Ethiopia, in November 2027.",
    "Air Astana \u2014 Kazakhstan's Air Astana seeks a bigger India play amid the Gulf crisis.",
]
TOTAL_STORIES = 3 + 9 + len(BRIEFS)  # 46
REGIONS = 7  # Middle East, Europe, Asia, North America, Africa, Oceania, Global

# ---------------------------------------------------------------- illustrations
def art_cop(cv, x, y, w, h):
    cv.rect(x, y, w, h, (222, 232, 226))
    cv.circle(x + w - 42, y + 30, 18, GOLD)
    # globe, left
    cv.circle(x + 78, y + 52, 38, (70, 130, 160))
    for dx in (-19, 0, 19):
        cv.line(x + 78 + dx, y + 18, x + 78 + dx, y + 86, (120, 180, 200), 2)
    cv.hline(x + 44, y + 52, 68, (120, 180, 200), 2)
    # cracked pact document, right
    cv.text("NO DEAL", x + 168, y + 22, 2, RED, bold=True)
    cv.rect(x + 168, y + 46, 128, 52, (250, 248, 240))
    cv.hline(x + 178, y + 58, 90, GREY, 1)
    cv.hline(x + 178, y + 68, 90, GREY, 1)
    cv.hline(x + 178, y + 78, 60, GREY, 1)
    cv.line(x + 232, y + 46, x + 244, y + 64, RED, 3)
    cv.line(x + 244, y + 64, x + 234, y + 80, RED, 3)
    cv.line(x + 234, y + 80, x + 248, y + 98, RED, 3)

def art_gulf(cv, x, y, w, h):
    cv.rect(x, y, w, h, (24, 38, 66))
    cv.circle(x + w - 46, y + 30, 14, (240, 220, 160))
    cv.rect(x, y + h - 46, w, 46, SEA)
    # tanker
    cv.rect(x + 40, y + h - 78, 150, 26, (30, 30, 30))
    cv.rect(x + 55, y + h - 104, 90, 26, (120, 40, 40))
    cv.rect(x + 150, y + h - 96, 26, 18, (200, 200, 200))
    cv.rect(x + 40, y + h - 52, 150, 6, (180, 60, 50))
    # missile arcs
    cv.line(x + 230, y + 20, x + 250, y + 60, (240, 200, 80), 3)
    cv.line(x + 250, y + 60, x + 262, y + 96, (240, 200, 80), 3)
    cv.circle(x + 262, y + 100, 6, (240, 120, 40))
    cv.line(x + 40, y + 30, x + 70, y + 70, (240, 200, 80), 2)
    # radar dome
    cv.circle(x + 30, y + h - 46, 16, (200, 200, 200))
    cv.rect(x + 14, y + h - 46, 32, 4, (200, 200, 200))
    cv.text("GULF", x + 210, y + h - 30, 2, (220, 220, 220), bold=True)

def art_kyiv(cv, x, y, w, h):
    cv.rect(x, y, w, h, (206, 214, 222))
    # smoke
    cv.circle(x + 90, y + 26, 14, (140, 140, 140))
    cv.circle(x + 112, y + 18, 18, (160, 160, 160))
    cv.circle(x + 136, y + 28, 12, (140, 140, 140))
    # building, damaged corner
    cv.rect(x + 60, y + 46, 130, h - 46, (150, 120, 100))
    cv.poly([(x + 150, y + 46), (x + 190, y + 46), (x + 190, y + 92),
             (x + 172, y + 78), (x + 162, y + 96), (x + 150, y + 84)], (60, 50, 45))
    for r in range(3):
        for c in range(4):
            cv.rect(x + 72 + c * 28, y + 58 + r * 26, 16, 14, (240, 230, 200))
    cv.rect(x + 210, y + 60, 60, h - 60, (120, 100, 85))
    for r in range(3):
        cv.rect(x + 222, y + 72 + r * 26, 14, 14, (240, 230, 200))
    cv.rect(x + 60, y + h - 4, 210, 4, (90, 80, 70))
    cv.text("KYIV", x + 226, y + 12, 2, INK, bold=True)

ARTS = {"cop": art_cop, "gulf": art_gulf, "kyiv": art_kyiv}

def icon(cv, kind, x, y, s=34):
    cv.rect(x, y, s, s, NAVY2)
    cx, cy = x + s // 2, y + s // 2
    if kind == "star":
        cv.poly([(cx, cy - 11), (cx + 4, cy - 3), (cx + 12, cy - 2), (cx + 6, cy + 4),
                 (cx + 8, cy + 12), (cx, cy + 7), (cx - 8, cy + 12), (cx - 6, cy + 4),
                 (cx - 12, cy - 2), (cx - 4, cy - 3)], GOLD)
    elif kind == "flame":
        cv.poly([(cx, cy - 12), (cx + 8, cy + 2), (cx + 4, cy + 10), (cx - 4, cy + 10),
                 (cx - 8, cy + 2)], (240, 120, 40))
        cv.circle(cx, cy + 4, 4, GOLD)
    elif kind == "flag":
        cv.rect(x + 8, y + 7, 18, 12, (240, 240, 240))
        cv.rect(x + 8, y + 7, 9, 6, RED)
        cv.rect(x + 17, y + 13, 9, 6, INK)
        cv.line(x + 8, y + 7, x + 8, y + 28, (240, 240, 240), 2)
    elif kind == "ball":
        cv.circle(cx, cy, 11, (240, 240, 240))
        cv.poly([(cx, cy - 5), (cx + 5, cy - 1), (cx + 3, cy + 5), (cx - 3, cy + 5),
                 (cx - 5, cy - 1)], INK)
    elif kind == "chart":
        cv.line(x + 7, y + 26, x + 13, y + 18, (120, 220, 120), 3)
        cv.line(x + 13, y + 18, x + 19, y + 22, (120, 220, 120), 3)
        cv.line(x + 19, y + 22, x + 27, y + 9, (240, 90, 90), 3)
    elif kind == "box":
        cv.rect(x + 8, y + 10, 18, 14, (200, 170, 120))
        cv.rect(cx - 2, y + 12, 4, 10, RED)
        cv.rect(x + 11, y + 15, 12, 4, RED)
    elif kind == "boat":
        cv.poly([(x + 7, y + 18), (x + 27, y + 18), (x + 23, y + 26), (x + 11, y + 26)], (200, 170, 120))
        cv.line(cx, y + 8, cx, y + 18, (240, 240, 240), 2)
        cv.poly([(cx, y + 8), (cx + 8, y + 17), (cx, y + 17)], (240, 240, 240))
    elif kind == "castle":
        cv.rect(x + 9, y + 14, 16, 12, (200, 170, 120))
        cv.poly([(x + 6, y + 14), (cx, y + 6), (x + 28, y + 14)], RED)
        cv.rect(cx - 2, y + 18, 4, 8, INK)
    elif kind == "shield":
        cv.poly([(cx, y + 7), (x + 26, y + 11), (x + 26, y + 19), (cx, y + 28),
                 (x + 8, y + 19), (x + 8, y + 11)], (180, 180, 180))
        cv.rect(cx - 1, y + 14, 3, 6, NAVY2)
        cv.circle(cx, y + 12, 2, NAVY2)

# ---------------------------------------------------------------- layout
def build():
    cv = Canvas(W, H, PAPER)
    # masthead
    cv.rect(0, 0, W, 122, NAVY)
    cv.rect(0, 122, W, 3, GOLD)
    cv.text("THE DAY IN WORLD NEWS", 28, 14, 2, GOLD, bold=True)
    cv.text("%d STORIES \u00b7 %d REGIONS \u00b7 ONE PAGE" % (TOTAL_STORIES, REGIONS),
            W - 28 - text_w("%d STORIES \u00b7 %d REGIONS \u00b7 ONE PAGE" % (TOTAL_STORIES, REGIONS), 2),
            14, 2, GOLD, bold=True)
    cv.text("Sunday 22 November 2026", 28, 36, 5, (250, 248, 240), bold=True)
    cv.text("Every story on this page happened, or was first reported, on this day.",
            28, 100, 1, (200, 205, 220))
    # headlines: 3 columns
    colw, gap, x0, y0 = 318, 15, 28, 136
    art_h = 110
    for i, hd in enumerate(HEADLINES):
        x = x0 + i * (colw + gap)
        ARTS[hd["art"]](cv, x, y0, colw, art_h)
        cv.rect(x, y0 + art_h, colw, 1, INK)
        yy = y0 + art_h + 10
        cv.circle(x + 9, yy + 5, 9, RED)
        cv.text(hd["num"], x + 5, yy - 2, 1, (255, 255, 255), bold=True)
        cv.text(hd["tag"], x + 24, yy, 1, RED, bold=True)
        yy += 20
        for ln in wrap(hd["title"], colw, 2):
            cv.text(ln, x, yy, 2, INK, bold=True)
            yy += 16
        yy += 4
        for ln in wrap(hd["body"], colw, 1):
            cv.text(ln, x, yy, 1, INK)
            yy += 9
    cv.hline(28, 358, W - 56, INK, 2)
    # secondary: 3 cols x 3 rows
    sy = 370
    row_h = 58
    for i, (num, tag, ic, title, body) in enumerate(SECONDARY):
        col, row = i % 3, i // 3
        x = x0 + col * (colw + gap)
        y = sy + row * row_h
        icon(cv, ic, x, y + 2)
        tx = x + 44
        cv.text(num + "  " + tag, tx, y + 1, 1, RED, bold=True)
        tlines = wrap(title, colw - 44, 1)
        yy = y + 12
        for ln in tlines[:2]:
            cv.text(ln, tx, yy, 1, INK, bold=True)
            yy += 10
        for ln in wrap(body, colw - 44, 1)[:2]:
            cv.text(ln, tx, yy, 1, (60, 60, 60))
            yy += 9
    cv.hline(28, 552, W - 56, INK, 2)
    # by the numbers
    ny = 564
    cv.text("BY THE NUMBERS", 28, ny + 4, 2, RED, bold=True)
    for i, (big, small) in enumerate(NUMBERS):
        x = 240 + i * 192
        cv.text(big, x, ny, 3, NAVY, bold=True)
        yy = ny + 26
        for ln in wrap(small, 175, 1):
            cv.text(ln, x, yy, 1, (60, 60, 60))
            yy += 9
    cv.hline(28, 616, W - 56, INK, 2)
    # timeline
    ty = 628
    cv.text("THE DAY IN UTC", 28, ty, 2, RED, bold=True)
    yy = ty + 22
    for t, ev in TIMELINE:
        cv.text(t, 28, yy, 1, NAVY, bold=True)
        for ln in wrap(ev, W - 56 - 130, 1):
            cv.text(ln, 150, yy, 1, INK)
            yy += 10
        yy += 1
    cv.hline(28, yy + 4, W - 56, INK, 2)
    # briefs: 3 columns, up to 2 lines each
    by = yy + 14
    cv.text("ALSO ON SUNDAY 22 NOVEMBER \u2014 %d MORE STORIES" % len(BRIEFS),
            28, by, 2, NAVY, bold=True)
    by += 24
    cv.hline(28, by - 4, W - 56, RED, 2)
    per = 12
    for j, b in enumerate(BRIEFS):
        col, row = j // per, j % per
        x = 28 + col * 325
        y = by + row * 17
        cv.text("%d." % (13 + j), x, y, 1, RED, bold=True)
        ly = y
        for ln in wrap(b, 285, 1)[:2]:
            cv.text(ln, x + 30, ly, 1, INK)
            ly += 8
    fy = by + per * 17 + 6
    cv.hline(28, fy, W - 56, INK, 1)
    cv.text("All stories happened or were first reported on Sunday 22 November 2026. "
            "Disputed claims are attributed.", 28, fy + 8, 1, GREY)
    cv.text("Sources: Reuters, AP, AFP, Al Jazeera, BBC, CNN, FT, UN News, Dawn, Nikkei, "
            "Formula 1. Original drawings.", 28, fy + 18, 1, GREY)
    return cv

def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(outdir, exist_ok=True)
    cv = build()
    path = os.path.join(outdir, "entry.png")
    n = write_png(cv, path)
    print("wrote %s (%d bytes)" % (path, n))

if __name__ == "__main__":
    main()
