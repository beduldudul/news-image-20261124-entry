#!/usr/bin/env python3
"""Draw the 24 November 2026 front page: THE WORLD IN ONE PAGE.

Programmatically drawn with PIL (no generated imagery, no AI text):
every glyph is rendered from DejaVu so the page stays crisp and
legible at ~300 px across. Output: entry.png, 1024x1024, <= 1 MiB.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
NAVY = (14, 34, 64)
NAVY_DARK = (10, 26, 50)
AMBER = (232, 163, 61)
INK = (24, 32, 48)
GREY = (86, 92, 104)
TEAL = (0, 110, 110)
RUST = (176, 74, 28)
RED = (178, 34, 34)
BLUE = (30, 80, 180)
PURPLE = (110, 60, 170)
GREEN = (28, 120, 70)
WHITE = (255, 255, 255)
CARD = (255, 255, 255)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width; returns list of lines."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for w in words[1:]:
            trial = cur + " " + w
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, fill, width, leading=None):
    lines = wrap(draw, text, fnt, width)
    lh = leading or int(fnt.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def centred(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + int(fnt.size * 1.25)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- Header band -------------------------------------------------------
d.rectangle([0, 0, W, 118], fill=NAVY)
centred(d, W // 2, 20, "THE WORLD IN ONE PAGE", font(BOLD, 58), WHITE)
centred(d, W // 2, 76, "TUESDAY, 24 NOVEMBER 2026", font(BOLD, 27), AMBER)
d.rectangle([0, 118, W, 122], fill=AMBER)

# ---- Sub-header --------------------------------------------------------
y = 136
_sub = "THE DAY'S WORLD NEWS  ·  TUESDAY 24 NOVEMBER 2026"
_subf = font(BOLD, 19)
_subw = d.textlength(_sub, font=_subf)
d.line([36, y + 12, W // 2 - _subw // 2 - 24, y + 12], fill=NAVY, width=2)
d.line([W // 2 + _subw // 2 + 24, y + 12, 988, y + 12], fill=NAVY, width=2)
centred(d, W // 2, y, _sub, _subf, NAVY)

# ---- Hero (left column) ------------------------------------------------
hx, hw = 36, 574
y = 178
d.text((hx, y), "RUSSIA  ·  TALLINN", font=font(BOLD, 22), fill=TEAL)
y += 34
y = draw_wrapped(d, hx, y, "RUSSIA WARNS ESTONIA\nOF 'OPEN WAR'",
                 font(BOLD, 54), INK, hw, leading=60)
y += 10
y = draw_wrapped(d, hx, y,
                 "Moscow says Tallinn's plan to close the border risks "
                 "outright conflict, after Estonia accused Russia of "
                 "hostile acts.",
                 font(REG, 21), GREY, hw, leading=27)

# ---- Hero panel: two flags, one warning --------------------------------
py = y + 16
ph = 168
d.rounded_rectangle([hx, py, hx + hw, py + ph], radius=10, fill=NAVY)
# Estonian flag (blue / black / white) on the left
fx, fy, fw, fh = hx + 46, py + 26, 150, 84
d.rectangle([fx, fy, fx + fw, fy + 28], fill=(0, 114, 206))
d.rectangle([fx, fy + 28, fx + fw, fy + 56], fill=(20, 20, 20))
d.rectangle([fx, fy + 56, fx + fw, fy + 84], fill=WHITE)
# Russian flag (white / blue / red) on the right
gx = hx + hw - 46 - 150
d.rectangle([gx, fy, gx + fw, fy + 28], fill=WHITE)
d.rectangle([gx, fy + 28, gx + fw, fy + 56], fill=(0, 57, 166))
d.rectangle([gx, fy + 56, gx + fw, fy + 84], fill=(213, 0, 50))
# Warning mark between the flags
mx = hx + hw // 2
d.ellipse([mx - 26, fy + 14, mx + 26, fy + 66], fill=AMBER)
d.text((mx - 7, fy + 18), "!", font=font(BOLD, 40), fill=NAVY)
d.line([hx + 46, py + ph - 34, hx + hw - 46, py + ph - 34],
       fill=AMBER, width=3)
centred(d, hx + hw // 2, py + ph - 26,
        "Russia warns Tallinn over border closure",
        font(BOLD, 17), WHITE)

# ---- Right rail: two stacked cards -------------------------------------
rx, rw = 634, 354
card_h = 252
gap = 18
top = 178


def rail_card(y0, bar, kicker, kicker_fill, headline, sub):
    d.rounded_rectangle([rx, y0, rx + rw, y0 + card_h], radius=8,
                        fill=CARD, outline=NAVY, width=2)
    d.rectangle([rx, y0 + 8, rx + 9, y0 + card_h - 8], fill=bar)
    x = rx + 26
    d.text((x, y0 + 18), kicker, font=font(BOLD, 18), fill=kicker_fill)
    yy = draw_wrapped(d, x, y0 + 48, headline, font(BOLD, 30), INK,
                      rw - 46, leading=35)
    draw_wrapped(d, x, yy + 10, sub, font(REG, 19), GREY, rw - 46,
                 leading=25)
    return y0 + card_h


rail_card(top, AMBER, "INDIA  ·  NEW DELHI", RUST,
          "INDIA PLEDGES $1.6BN TO NEPAL",
          "Modi offers flood rebuild aid as Nepal's PM visits Delhi.")
rail_card(top + card_h + gap, RED, "TAJIKISTAN  ·  DUSHANBE", RED,
          "TAJIKISTAN TO QUIT ICC",
          "Fourth country to start leaving the court since July.")

# ---- Around the world: three cards -------------------------------------
ay = 706
d.text((36, ay), "AROUND THE WORLD", font=font(BOLD, 24), fill=NAVY)
d.line([292, ay + 14, 988, ay + 14], fill=NAVY, width=2)
cy = ay + 40
cw, chh = 300, 150
cx0 = 36


def world_card(x0, bar, kicker, kicker_fill, headline, sub):
    d.rounded_rectangle([x0, cy, x0 + cw, cy + chh], radius=8,
                        fill=CARD, outline=NAVY, width=2)
    d.rectangle([x0 + 8, cy, x0 + cw - 8, cy + 6], fill=bar)
    x = x0 + 16
    d.text((x, cy + 16), kicker, font=font(BOLD, 16), fill=kicker_fill)
    yy = draw_wrapped(d, x, cy + 40, headline, font(BOLD, 22), INK,
                      cw - 32, leading=26)
    draw_wrapped(d, x, yy + 6, sub, font(REG, 15), GREY, cw - 32,
                 leading=19)


world_card(cx0, BLUE, "GAZA  ·  JABALIA", BLUE,
           "GAZA STRIKES KILL UN WORKER",
           "UNRWA worker Adel al-Helo among the dead.")
world_card(cx0 + cw + 12, PURPLE, "CLIMATE  ·  ANTALYA", PURPLE,
           "COP31: WORLD SPLIT",
           "No deal in Antalya; fossil-fuel row ends talks.")
world_card(cx0 + 2 * (cw + 12), GREEN, "EUROPE  ·  BERLIN", GREEN,
           "BOMB THREATS HIT SCHOOLS",
           "Hundreds of schools emailed; police say not serious.")

# ---- Ticker -------------------------------------------------------------
ty = 912
th = 80
d.rounded_rectangle([36, ty, 988, ty + th], radius=10, fill=NAVY)
d.text((56, ty + 28), "ALSO IN BRIEF", font=font(BOLD, 20), fill=AMBER)
ticker = ("Danish court upholds 'ghetto law' evictions  ·  France protests "
          "enter sixth weekend  ·  AFCON title awaits court ruling  ·  UN "
          "counts 25 seafarers killed off Hormuz  ·  Iranian singer flogged "
          "over concert  ·  New Yorkers stock up as tech outages mount")
draw_wrapped(d, 252, ty + 8, ticker, font(REG, 17), WHITE, 988 - 252 - 20,
             leading=21)

# ---- Footer -------------------------------------------------------------
centred(d, W // 2, 999, "Tuesday 24 November 2026  ·  as reported by the wires",
        font(REG, 15), GREY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
