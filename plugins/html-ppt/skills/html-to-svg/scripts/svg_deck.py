#!/usr/bin/env python3
"""svg_deck — tiny helper library for slide-per-file SVG deck generation.

Copy this file next to your deck's generate_svgs.py (keep decks self-contained)
or import it directly from the skill folder.

Style contract (the html-to-svg skill):
  - canvas 1280x720 (= PowerPoint 13.33in x 7.5in @ 96dpi, imports 1:1)
  - pure white background
  - Times New Roman everywhere
  - body text via bullets(): ONE SENTENCE PER LINE, hanging indent on wrap
  - NO emoji in <text> — use color, the todo() pill, or vector shapes instead
    (rasterizers without an emoji font draw tofu boxes; PowerPoint importers
    vary). Safe glyphs: • → ← ▶ · ± ≥ ∨ — – “ ”
"""
import html
from pathlib import Path

W, H = 1280, 720
M = 60  # side margin

BG, SURF, SURF2 = "#ffffff", "#ffffff", "#f2f2f0"
INK, SUB, MUT = "#1c1c1c", "#3f3f46", "#8a8a8a"
ACC, WARN, GOOD, BORDER = "#1f5aa8", "#b45309", "#15803d", "#d4d4d0"
FONT = "'Times New Roman', Times, serif"


def esc(s):
    return html.escape(str(s), quote=True)


def wrap(s, max_px, fs):
    """Greedy wrap by estimated glyph width (~0.48*fs for Times)."""
    cw = fs * 0.48
    max_chars = max(8, int(max_px / cw))
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        cand = (cur + " " + w_).strip()
        if len(cand) <= max_chars:
            cur = cand
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


class Svg:
    """Element buffer with primitive draw calls; render() wraps in <svg>."""

    def __init__(self):
        self.el = []

    def add(self, s):
        self.el.append(s)

    def rect(self, x, y, w, h, fill=SURF, stroke=BORDER, rx=10, dash=None, sw=1):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def line(self, x1, y1, x2, y2, stroke=BORDER, sw=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                 f'stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def circle(self, cx, cy, r, fill=INK, stroke=SURF, sw=2):
        self.add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" '
                 f'stroke="{stroke}" stroke-width="{sw}"/>')

    def text(self, x, y, s, fs=14, fill=INK, weight="normal", anchor="start", style=""):
        self.add(f'<text x="{x}" y="{y}" font-size="{fs}" fill="{fill}" '
                 f'font-weight="{weight}" font-family="{FONT}" '
                 f'text-anchor="{anchor}" {style}>{esc(s)}</text>')

    def bullets(self, x, y, items, max_px, fs=13, fill=SUB, lh=None, gap=5, indent=16):
        """Each item = one sentence = one bullet, as ONE <text> with <tspan>
        lines — PowerPoint's Convert-to-Shape then yields one text box per
        bullet (loose per-line <text> elements become colliding boxes)."""
        lh = lh or fs * 1.4
        yy = y
        for it in items:
            color, weight, txt = fill, "normal", it
            if isinstance(it, tuple):  # (text, color) or (text, color, weight)
                txt, color = it[0], it[1]
                weight = it[2] if len(it) > 2 else "normal"
            lines = wrap(txt, max_px - indent, fs)
            spans = [f'<tspan x="{x}" y="{yy}" font-weight="bold">•</tspan>']
            for k, ln in enumerate(lines):
                dy = f' dy="{lh}"' if k else ""
                w_attr = "" if weight == "normal" else f' font-weight="{weight}"'
                first_y = "" if k else f' y="{yy}"'
                spans.append(f'<tspan x="{x + indent}"{first_y}{dy}{w_attr}>{esc(ln)}</tspan>')
            self.add(f'<text font-size="{fs}" fill="{color}" font-family="{FONT}">'
                     + "".join(spans) + "</text>")
            yy += lh * len(lines) + gap
        return yy  # next baseline

    def render(self, title):
        body = "\n".join(self.el)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
                f'viewBox="0 0 {W} {H}">\n<title>{esc(title)}</title>\n'
                f'<rect width="{W}" height="{H}" fill="{BG}"/>\n{body}\n</svg>\n')


def header(s, kicker, title, n, total, footer=""):
    """Standard slide chrome: kicker, serif title, rule, page number, footer."""
    s.text(M, 62, kicker.upper(), fs=13, fill=ACC, weight="bold",
           style='letter-spacing="2"')
    s.text(M, 104, title, fs=31, fill=INK, weight="bold")
    s.line(M, 122, W - M, 122, stroke=BORDER)
    s.text(W - M, 62, f"{n} / {total}", fs=12, fill=MUT, anchor="end")
    if footer:
        s.text(M, H - 26, footer, fs=11, fill=MUT)


def card(s, x, y, w, h, title, items, accent=False, fs=12.5):
    """Bordered card whose body is a bullet list (one sentence per line)."""
    s.rect(x, y, w, h, fill=SURF, stroke=ACC if accent else BORDER,
           sw=1.6 if accent else 1)
    s.text(x + 16, y + 28, title, fs=15, weight="bold")
    return s.bullets(x + 16, y + 52, items, w - 32, fs=fs)


def todo(s, x, y, label):
    """Dashed amber placeholder pill for not-yet-available content.

    Returns the x just past the pill so pills can be chained on one line.
    """
    wpx = len(label) * 6.6 + 20
    s.rect(x, y - 13, wpx, 19, fill=SURF2, stroke=WARN, rx=9, dash="4,3")
    s.text(x + wpx / 2, y + 1, label, fs=11, fill=WARN, weight="bold", anchor="middle")
    return x + wpx + 8


def minibar(s, x, y, w, label, frac, value, bar_h=13):
    """One row of a small horizontal bar chart: label | bar | value."""
    s.text(x, y + 10, label, fs=12, fill=SUB)
    bw = max(3, (w - 105 - 80) * frac)
    s.rect(x + 105, y, bw, bar_h, fill=ACC, stroke="none", rx=4)
    s.text(x + w - 4, y + 10, value, fs=12, fill=INK, weight="bold", anchor="end")
    return y + bar_h + 8


def write_deck(slides, out_dir):
    """slides: list of (name, fn) where fn() returns an SVG string."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for name, fn in slides:
        p = out / f"{name}.svg"
        p.write_text(fn(), encoding="utf-8")
        print(f"wrote {p.name}")
