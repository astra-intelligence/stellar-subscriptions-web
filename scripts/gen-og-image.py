#!/usr/bin/env python3
"""Generate the 1200x630 Open Graph image for Stellar Subscriptions using the
project's exact brand colors (from app/globals.css) and the recurring ↻ mark
used in the site header. Reproducible: run from the repo root."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
BG = (9, 11, 16)          # --bg dark
BRAND = (34, 211, 238)    # --brand dark (#22D3EE)
FG = (236, 239, 244)      # --fg dark
MUTED = (148, 157, 175)   # --muted dark

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# Subtle brand glow in the top-right corner (radial-ish via concentric alpha).
for i in range(60, 0, -1):
    a = int(14 * (i / 60))
    d.ellipse([W - 320 - i * 3, -120 - i * 3, W - 320 + i * 3, -120 + i * 3],
              fill=(BRAND[0], BRAND[1], BRAND[2], a))
img = img.convert("RGBA")
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
for i in range(60, 0, -1):
    a = int(10 * (i / 60))
    od.ellipse([W - 300 - i * 3, -100 - i * 3, W - 300 + i * 3, -100 + i * 3],
               fill=(BRAND[0], BRAND[1], BRAND[2], a))
img = Image.alpha_composite(img, overlay).convert("RGB")
d = ImageDraw.Draw(img)

# Brand mark: rounded square with ↻, top-left.
def rounded_rect(draw, box, radius, fill):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=radius, fill=fill)

rounded_rect(d, (80, 80, 200, 200), 28, BRAND)

# Find a font for the ↻ glyph.
def find_font(sizes):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, sizes)
    return ImageFont.load_default()

font_mark = find_font(90)
# Draw ↻ centered in the brand square.
mark_bbox = d.textbbox((0, 0), "↻", font=font_mark)
mw, mh = mark_bbox[2] - mark_bbox[0], mark_bbox[3] - mark_bbox[1]
d.text((140 - mw / 2, 140 - mh / 2 - mark_bbox[1]), "↻", font=font_mark, fill=(255, 255, 255))

# Title.
font_title = find_font(72)
d.text((80, 250), "Stellar Subscriptions", font=font_title, fill=FG)

# Tagline.
font_tag = find_font(40)
d.text((80, 360), "Recurring payments on Stellar, on your terms.", font=font_tag, fill=MUTED)

# Sub-line.
font_sub = find_font(34)
d.text((80, 440), "Authorize a spending cap once, cancel anytime.", font=font_sub, fill=MUTED)

# Bottom brand bar.
d.rectangle([0, H - 12, W, H], fill=BRAND)

out = os.path.join(os.path.dirname(__file__), "..", "app", "opengraph-image.png")
img.save(out, "PNG")
print("wrote", os.path.abspath(out), img.size)
