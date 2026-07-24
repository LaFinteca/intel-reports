#!/usr/bin/env python3
"""Generates the branded 1200x630 Open Graph image for one digest issue.

Requires: pip install pillow numpy

Usage:
  python3 scripts/generate-og-image.py \
    --week "Week 31" \
    --intro "Fintech, payments & LatAm intelligence — curated weekly by LaFinteca MRO." \
    --out assets/og-digest-week-31.png

Uses the shared background/scheme approved for the digest OG image
(assets/og/backgrounds/lf-deckv2-digest-bg.png). Only --week, --intro and
--out change from issue to issue.
"""
import argparse
import re
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / "assets" / "og" / "fonts"
BG_DEFAULT = ROOT / "assets" / "og" / "backgrounds" / "lf-deckv2-digest-bg.jpg"

W, H = 1200, 630

# Path data for the LaFinteca wordmark (viewBox 0 0 545 64). Every path uses
# only M/L/H/V/Z (straight-line) commands, so it can be rasterized as plain
# evenodd-combined polygons instead of needing a real SVG renderer.
LOGO_PATHS = [
    ("chevron", "M0 35.3406V27.9089L35.483 13.241V21.7158L10.5666 31.4292V31.8203L35.483 42.0553V50.5301L0 35.3406Z"),
    ("chevron", "M545 28.6585L545 36.0902L509.517 50.7582L509.517 42.2834L534.433 32.5699L534.433 32.1788L509.517 21.9438L509.517 13.469L545 28.6585Z"),
    ("word", "M99.9159 42.1908V55.4107L108.51 64H126.468L133.837 56.9549V64H142.926V23.1124L133.363 13.5544H109.867L100.304 23.1124V30.6785H109.684V26.0672L113.876 21.9607H129.451L133.643 26.0672V33.7023H108.514L99.9159 42.1908ZM124.126 55.5938L133.643 46.4442V42.1086H112.518L109.296 45.2481V52.4542L112.518 55.5938H124.126Z"),
    ("word", "M201.268 0.056688H156.222V64H165.796V33.7782H196.616V24.9845H165.796V8.8504H201.268V0.056688Z"),
    ("word", "M208.246 3.60855V8.78473L211.8 12.3371H216.979L220.533 8.78473V3.60855L216.979 0.0562165H211.8L208.246 3.60855Z"),
    ("word", "M219.13 24.984H209.75V63.9995H219.13V24.984Z"),
    ("word", "M241.588 13.5544H232.402V38.7772V64H241.782V33.5192L253.153 22.1544H262.033L266.226 26.2609V64H275.606V23.1124L266.043 13.5544H250.3L241.588 22.2616V13.5544Z"),
    ("word", "M294.384 22.0575L288.71 54.1024L296.927 64H311.462L312.902 55.4969H301.941L298.621 51.4493L303.799 22.0575H318.828L320.268 13.5544H305.297L308.107 0.0692076H298.874L296.063 13.5544H287.112L285.672 22.0575H294.384Z"),
    ("word", "M326.245 23.1119V54.4416L335.809 63.9995H361.049L370.613 54.4416V46.9723H361.233V51.293L357.04 55.3996H339.818L335.625 51.293V42.0112H370.709V23.1084L361.046 13.5539H335.809L326.245 23.1119ZM357.137 22.1539L361.329 26.2605V33.605H335.625V26.2604L339.818 22.1539H357.137Z"),
    ("word", "M383.656 23.1119V54.4416L393.219 63.9995H417.394L426.957 54.4416V46.9723H417.577V51.293L413.384 55.3996H397.228L393.036 51.293V26.2604L397.228 22.1539H413.384L417.577 26.2604V30.5812H426.957V23.1119L417.394 13.5539H393.219L383.656 23.1119Z"),
    ("word", "M439.962 42.1903V55.4102L448.556 63.9995H466.514L473.883 56.9544V63.9995H482.972V23.1119L473.409 13.5539H449.913L440.35 23.1119V30.678H449.73V26.0667L453.922 21.9602H469.497L473.689 26.0667V33.7018H448.56L439.962 42.1903ZM464.172 55.5933L473.689 46.4437V42.1081H452.564L449.342 45.2476V52.4538L452.564 55.5933H464.172Z"),
    ("word", "M71.4869 0H61.9131V63.9433H86.6686V55.2465H71.4869V0Z"),
]
VBW, VBH = 545, 64
TOKEN_RE = re.compile(r"[MLHVZ]|-?\d*\.?\d+(?:[eE]-?\d+)?")

SCHEME = dict(
    scrim_color=(8, 7, 12),
    scrim_max_alpha=232,
    scrim_end=800,
    kicker=(191, 254, 67),
    title1=(255, 255, 255),
    title2=(195, 171, 255),
    intro=(201, 201, 201),
    footer=(122, 118, 130),
    logo_chevron=(195, 171, 255, 255),
    logo_word=(255, 255, 255, 255),
)


def parse_subpaths(d):
    tokens = TOKEN_RE.findall(d)
    subpaths, cur = [], []
    cmd = None
    x = y = 0.0
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok in "MLHVZ":
            cmd = tok
            i += 1
            if cmd == "Z":
                if cur:
                    subpaths.append(cur)
                    cur = []
                continue
        if cmd == "M":
            x, y = float(tokens[i]), float(tokens[i + 1])
            i += 2
            if cur:
                subpaths.append(cur)
            cur = [(x, y)]
            cmd = "L"
        elif cmd == "L":
            x, y = float(tokens[i]), float(tokens[i + 1])
            i += 2
            cur.append((x, y))
        elif cmd == "H":
            x = float(tokens[i])
            i += 1
            cur.append((x, y))
        elif cmd == "V":
            y = float(tokens[i])
            i += 1
            cur.append((x, y))
        else:
            i += 1
    if cur:
        subpaths.append(cur)
    return subpaths


def render_logo(height_px, colors, supersample=4):
    scale = height_px / VBH
    ss = supersample
    w = round(VBW * scale)
    h = round(VBH * scale)
    Wp, Hp = w * ss, h * ss
    out = np.zeros((Hp, Wp, 4), dtype=np.uint8)
    for kind, d in LOGO_PATHS:
        acc = np.zeros((Hp, Wp), dtype=bool)
        for sp in parse_subpaths(d):
            pts = [(px * scale * ss, py * scale * ss) for px, py in sp]
            layer = Image.new("1", (Wp, Hp), 0)
            ImageDraw.Draw(layer).polygon(pts, fill=1)
            acc ^= np.array(layer, dtype=bool)
        out[acc] = colors.get(kind, (255, 255, 255, 255))
    return Image.fromarray(out).resize((w, h), Image.LANCZOS)


def font(name, size, weight=None):
    f = ImageFont.truetype(str(FONT_DIR / name), size)
    if weight is not None:
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
    return f


def cover_crop(im, w, h):
    sw, sh = im.size
    scale = max(w / sw, h / sh)
    nw, nh = round(sw * scale), round(sh * scale)
    im = im.resize((nw, nh), Image.LANCZOS)
    x, y = (nw - w) // 2, (nh - h) // 2
    return im.crop((x, y, x + w, y + h))


def draw_tracked_text(draw, xy, text, fnt, fill, tracking=0):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking


def wrap_text(draw, text, fnt, max_width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def compose(bg_path, week_label, intro_text, out_path, site_label="lafinteca.github.io/intel-reports"):
    bg = Image.open(bg_path).convert("RGB")
    canvas = cover_crop(bg, W, H).convert("RGBA")

    grad = np.zeros((H, W), dtype=np.uint8)
    end = SCHEME["scrim_end"]
    for x in range(W):
        a = 0 if x >= end else SCHEME["scrim_max_alpha"] * (1 - (x / end) ** 1.4)
        grad[:, x] = int(max(0, min(255, a)))
    scrim = Image.new("RGBA", (W, H), SCHEME["scrim_color"] + (0,))
    scrim.putalpha(Image.fromarray(grad))
    canvas = Image.alpha_composite(canvas, scrim)

    draw = ImageDraw.Draw(canvas)
    left = 64

    logo = render_logo(24, {"chevron": SCHEME["logo_chevron"], "word": SCHEME["logo_word"]})
    canvas.paste(logo, (left, 54), logo)
    draw = ImageDraw.Draw(canvas)

    kicker_y = 132
    kicker_font = font("JetBrainsMono-Medium.ttf", 15, weight=560)
    draw_tracked_text(draw, (left, kicker_y), "MARKETING & RESEARCH OFFICE", kicker_font, SCHEME["kicker"], tracking=2.6)

    t1_font = font("InstrumentSerif-Regular.ttf", 66)
    t2_font = font("InstrumentSerif-Italic.ttf", 66)
    title_y = 188
    draw.text((left, title_y), "Weekly Industry Digest", font=t1_font, fill=SCHEME["title1"])
    draw.text((left, title_y + 74), week_label, font=t2_font, fill=SCHEME["title2"])

    intro_font = font("InterTight-Regular.ttf", 21, weight=340)
    ly = title_y + 74 + 92
    for line in wrap_text(draw, intro_text, intro_font, 640)[:2]:
        draw.text((left, ly), line, font=intro_font, fill=SCHEME["intro"])
        ly += 30

    footer_font = font("JetBrainsMono-Medium.ttf", 13, weight=460)
    draw.text((left, H - 56), site_label, font=footer_font, fill=SCHEME["footer"])

    rgb = canvas.convert("RGB")
    if str(out_path).lower().endswith((".jpg", ".jpeg")):
        rgb.save(out_path, "JPEG", quality=88, optimize=True)
    else:
        rgb.save(out_path, "PNG", optimize=True)
    print(f"wrote {out_path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", required=True, help='e.g. "Week 31"')
    ap.add_argument("--intro", required=True, help="Short subtitle line under the title")
    ap.add_argument("--out", required=True, help="Output PNG path")
    ap.add_argument("--bg", default=str(BG_DEFAULT), help="Background image (defaults to the approved digest background)")
    args = ap.parse_args()
    compose(args.bg, args.week, args.intro, args.out)
