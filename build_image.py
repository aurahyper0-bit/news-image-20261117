"""Draw the 17 November 2026 world-news front page (1024x1024 PNG).

One typographic front page: masthead, the date in red, five reported stories
with short headlines and one-line summaries, plus an "also" strip. All text
is drawn with PIL (crisp, legible) -- no generated art, no network.
Run: python3 build_image.py  (writes entry.png next to this script)
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024
PAPER = (248, 245, 238)
INK = (17, 17, 17)
RED = (185, 28, 28)
BLUE = (29, 78, 216)
TEAL = (13, 116, 128)
PURPLE = (107, 33, 168)
MUTED = (85, 85, 85)
RULE = (17, 17, 17)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_MAST = font("DejaVuSans-Bold.ttf", 74)
F_DATE = font("DejaVuSans-Bold.ttf", 36)
F_CHIP = font("DejaVuSans-Bold.ttf", 20)
F_LEAD_H = font("DejaVuSans-Bold.ttf", 42)
F_LEAD_S = font("DejaVuSans.ttf", 23)
F_H = font("DejaVuSans-Bold.ttf", 31)
F_S = font("DejaVuSans.ttf", 21)
F_ALSO = font("DejaVuSans.ttf", 20)
F_FOOT = font("DejaVuSans.ttf", 18)


def wrap(draw, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_chip(draw, x, y, label, color):
    pad_x, pad_y = 12, 6
    tw = draw.textlength(label, font=F_CHIP)
    th = F_CHIP.size
    draw.rectangle([x, y, x + tw + 2 * pad_x, y + th + 2 * pad_y], fill=color)
    draw.text((x + pad_x, y + pad_y), label, font=F_CHIP, fill=(255, 255, 255))
    return tw + 2 * pad_x


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 48  # margin
    cw = W - 2 * mx  # content width
    y = 30

    # Masthead
    title = "WORLD NEWS"
    d.text(((W - d.textlength(title, font=F_MAST)) / 2, y), title,
           font=F_MAST, fill=INK)
    y += 92
    d.rectangle([mx, y, W - mx, y + 6], fill=RED)
    y += 20

    # Date line
    date = "TUESDAY  •  17 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=F_DATE)) / 2, y), date,
           font=F_DATE, fill=RED)
    y += 54
    d.rectangle([mx, y, W - mx, y + 2], fill=RULE)
    y += 22

    stories = [
        # (chip, chip color, headline, subline) -- lead first
        ("MIDDLE EAST", RED,
         "Iran fires drones at U.S. radar base in Bahrain",
         "Bahrain says the attack was intercepted, with no casualties. "
         "U.S. intelligence warns Iran is plotting a \u201cdirty bomb\u201d "
         "attack on Trump officials."),
        ("UKRAINE", BLUE,
         "Crimea bridge shut after Ukrainian strike",
         "Zelenskyy hails an \u201cunprecedented operation\u201d as Russia "
         "hits two bridges in Kyiv."),
        ("ASIA", TEAL,
         "Trump flies to Asia for talks with Xi and Putin",
         "Trilateral nuclear talks set for Shenzhen on 19 November."),
        ("MIDDLE EAST", RED,
         "Third U.S. carrier reaches the Middle East",
         "Tankers struck by mines in the Strait of Hormuz."),
        ("EUROPE", PURPLE,
         "Five EU states plan migrant hub in Rwanda",
         "Germany, Denmark, Austria, Greece and the Netherlands unveil "
         "a joint return facility."),
    ]

    for i, (chip, color, head, sub) in enumerate(stories):
        lead = (i == 0)
        fh, fs = (F_LEAD_H, F_LEAD_S) if lead else (F_H, F_S)
        draw_chip(d, mx, y, chip, color)
        y += 38 if lead else 34
        for line in wrap(d, head, fh, cw):
            d.text((mx, y), line, font=fh, fill=INK)
            y += fh.size + 4
        y += 2
        for line in wrap(d, sub, fs, cw):
            d.text((mx, y), line, font=fs, fill=MUTED)
            y += fs.size + 4
        y += 12 if lead else 10
        if i < len(stories) - 1:
            d.rectangle([mx, y, W - mx, y + 1], fill=(200, 195, 185))
            y += 11 if lead else 10

    # Also strip
    also = ("ALSO:  Japan scrambles jets as Russian planes enter its airspace  •  "
            "UK sanctions Israeli settlement builders  •  Depardieu pleads guilty")
    for line in wrap(d, also, F_ALSO, cw):
        d.text((mx, y), line, font=F_ALSO, fill=MUTED)
        y += F_ALSO.size + 4
    y += 12

    # Footer
    d.rectangle([mx, y, W - mx, y + 2], fill=RULE)
    y += 12
    foot = "17 NOVEMBER 2026  —  compiled from major wire reports"
    d.text(((W - d.textlength(foot, font=F_FOOT)) / 2, y), foot,
           font=F_FOOT, fill=MUTED)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
