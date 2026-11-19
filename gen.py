#!/usr/bin/env python3
"""Generate the 18 November 2026 world-news front page (1024x1024 PNG).

Run: python3 gen.py  -> writes entry.png beside this file.
All facts are from the verified briefing (news-18nov-facts.md). PIL + DejaVu
fonts are only used here, on the build machine; the shipped program (main.ts)
is stdlib-only and just copies the finished image.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
W, H = 1024, 1024
PAPER = (251, 248, 241)
INK = (20, 20, 20)
NAVY = (22, 35, 61)
RED = (166, 27, 27)
GREY = (52, 50, 46)
RULE = (200, 194, 182)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_MAST = font("DejaVuSans-Bold.ttf", 62)
F_DATE = font("DejaVuSans.ttf", 23)
F_KICK = font("DejaVuSans-Bold.ttf", 22)
F_HERO = font("DejaVuSans-Bold.ttf", 50)
F_BODY = font("DejaVuSans.ttf", 24)
F_HEAD = font("DejaVuSans-Bold.ttf", 30)
F_SUM = font("DejaVuSans.ttf", 21)
F_FOOT = font("DejaVuSans.ttf", 20)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, color=INK):
    """Draw wrapped paragraph; returns y after the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def para_h(draw, text, fnt, max_w, leading):
    """Height a wrapped paragraph would take."""
    return len(wrap(draw, text, fnt, max_w)) * leading


def rule(draw, x0, x1, y, w=2, color=RULE):
    draw.line([(x0, y), (x1, y)], fill=color, width=w)


def panel_h(draw, w, headline, summary):
    """Height of one grid panel: kicker + headline + summary."""
    return 28 + para_h(draw, headline, F_HEAD, w, 34) + 4 + \
        para_h(draw, summary, F_SUM, w, 26)


def panel(draw, x, y, w, kicker, headline, summary):
    draw.text((x, y), kicker, font=F_KICK, fill=RED)
    y += 28
    y = para(draw, x, y, headline, F_HEAD, w, 34)
    y += 4
    y = para(draw, x, y, summary, F_SUM, w, 26, color=GREY)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ---
    d.rectangle([0, 0, W, 112], fill=NAVY)
    d.text((W // 2, 10), "WORLD NEWS", font=F_MAST, fill=(255, 255, 255),
           anchor="ma")
    d.text((W // 2, 82), "WEDNESDAY  ·  18 NOVEMBER 2026", font=F_DATE,
           fill=(214, 210, 198), anchor="ma")
    d.rectangle([0, 112, W, 118], fill=RED)

    # --- hero: Gulf escalation ---
    x, y = 40, 136
    d.text((x, y), "GULF ESCALATION", font=F_KICK, fill=RED)
    y += 30
    y = para(d, x, y, "U.S. STRIKES IRAN — IRAN HITS BACK", F_HERO, W - 80, 56)
    y += 6
    y = para(d, x, y,
             "U.S. jets hit a Revolutionary Guard missile site on Qeshm Island "
             "in the Strait of Hormuz. Iran fired drones at Ali Al Salem Air "
             "Base in Kuwait and targets in Bahrain; Bahrain intercepted "
             "attacks before dawn.", F_BODY, W - 80, 30)
    rule(d, 40, W - 40, y + 10, 2)

    # --- grid: 6 stories, 2 cols x 3 rows, rows sized to fit content ---
    col_w = 472
    gx0, gx1 = 40, 512
    stories = [
        ("APEC  ·  SHENZHEN",
         "XI AND PUTIN MEET AHEAD OF TRUMP SUMMIT",
         "Xi and Putin open talks in Shenzhen at APEC, a day before the "
         "first-ever trilateral summit with Trump."),
        ("UKRAINE",
         "KERCH BRIDGE HIT AGAIN",
         "Ukraine hit the Kerch Bridge a second day; part of its road span "
         "fell into the strait."),
        ("U.S. SENATE",
         "PELTOLA WINS ALASKA",
         "Peltola beats Sullivan; Democrats take the Senate 56–44, their "
         "largest majority since 2009."),
        ("HEALTH",
         "U.S. LOSES MEASLES-FREE STATUS",
         "Measles-free status held since 2000 is gone: 5,412 cases in "
         "2026, the most since 1991; 10 deaths."),
        ("HEALTH  ·  DR CONGO",
         "EBOLA PASSES 11,000 CASES",
         "Outbreak more than doubled in three months: 11,000+ cases, "
         "5,400+ deaths across 67 health zones."),
        ("SPACE",
         "VOYAGER 1: ONE LIGHT-DAY",
         "NASA's Voyager 1 reaches one light-day from Earth — about 16 "
         "billion miles — a first for any human-made object."),
    ]
    gy = y + 24
    for r in range(3):
        pair = stories[r * 2:(r + 1) * 2]
        rh = max(panel_h(d, col_w, s[1], s[2]) for s in pair)
        for i, (kick, head, summ) in enumerate(pair):
            px = gx0 if i == 0 else gx1
            panel(d, px, gy, col_w, kick, head, summ)
        d.line([(504, gy + 4), (504, gy + rh - 6)], fill=RULE, width=1)
        gy += rh + 10
        if r < 2:
            rule(d, 40, W - 40, gy - 2, 1)

    # --- bottom strip: also in the news (two centred lines) ---
    by = gy + 2
    d.rectangle([0, by, W, by + 60], fill=(235, 230, 220))
    d.text((W // 2, by + 8),
           "ALSO: Nvidia revenue $115.84B, up 103% — board rules out bringing "
           "back Jensen Huang",
           font=F_FOOT, fill=GREY, anchor="ma")
    d.text((W // 2, by + 32),
           "Category 5 Cyclone Xavier hits the Northern Cook Islands",
           font=F_FOOT, fill=GREY, anchor="ma")

    img.save(os.path.join(HERE, "entry.png"), "PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
