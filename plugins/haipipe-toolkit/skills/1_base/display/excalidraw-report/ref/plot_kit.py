"""plot_kit: the /excalidraw-report drawing engine plus plots made of native Excalidraw shapes.

Copy this file into `<Block or report>/studio/_build/` and import it from the builder; a builder
reads its numbers from the Result files the report cites and hands them to these functions, so
no value on a drawing is typed. Every plot is rectangles, lines and text: it stays editable in
Excalidraw, renders in the workbench, and carries its values as text (a bar without its number is
not read). Plot kinds (SKILL.md § Plots says which number takes which plot):

    hbar        sizes of several things, largest first          tables by rows, Runs by minutes
    compare     two to four big bars side by side, A vs B       schema vs schema, before vs after
    share_bar   one 100% bar: how a whole splits               rows by table, patients by route
    columns     a count over time, one column per period        rows per year
    spans       when each thing starts and ends, on one axis    table date coverage
    gauge       done out of total                               Runs complete, gates settled
    trend       a line over ordered points                       a metric across versions

Engine: Doc().frame(...), text, rect, line, dot, pill, then Doc.save(path).
"""
from __future__ import annotations

import json
import math
import random

EM = 0.6                                   # average glyph width / font size, for layout only
INK, GRAY, LGRAY, BLUE, ORANGE, GREEN, RED, PURPLE = (
    "#1e1e1e", "#495057", "#adb5bd", "#1864ab", "#e8590c", "#2b8a3e", "#c92a2a", "#7048e8")
FILL = {GRAY: "#dee2e6", LGRAY: "#f1f3f5", BLUE: "#a5d8ff", ORANGE: "#ffd8a8", GREEN: "#b2f2bb",
        RED: "#ffc9c9", PURPLE: "#d0bfff", INK: "#868e96"}


def fmt_n(v: float) -> str:
    """22667470420 -> '22.7B'; 4003 -> '4,003'; 0.452 stays as given by the caller."""
    v = float(v)
    for unit, d in (("B", 1e9), ("M", 1e6)):
        if abs(v) >= d:
            return f"{v / d:.1f}{unit}" if abs(v) < 100 * d else f"{v / d:.0f}{unit}"
    return f"{int(round(v)):,}"


def pct(v: float, total: float, digits: int = 1) -> str:
    return f"{100 * v / total:.{digits}f}%" if total else "0%"


class Doc:
    """One drawing file; every element drawn after frame() belongs to that frame."""

    def __init__(self, seed: int = 7):
        self.els, self.n, self.frame_id = [], 0, None
        random.seed(seed)

    # ------------------------------------------------------------------ primitives
    def base(self, kind, x, y, w, h, **kw):
        self.n += 1
        e = {"id": f"{kind}-{self.n}", "type": kind, "x": x, "y": y, "width": w, "height": h, "angle": 0,
             "strokeColor": INK, "backgroundColor": "transparent", "fillStyle": "solid", "strokeWidth": 2,
             "strokeStyle": "solid", "roughness": 0, "opacity": 100, "groupIds": [], "frameId": self.frame_id,
             "roundness": None, "seed": random.randint(1, 2**31 - 1), "version": 1,
             "versionNonce": random.randint(1, 2**31 - 1), "isDeleted": False, "boundElements": [],
             "updated": 1790900000000, "link": None, "locked": False}
        e.update(kw)
        self.els.append(e)
        return e

    def frame(self, fid, name, x, y, w, h):
        self.frame_id = None
        f = self.base("frame", x, y, w, h, id=fid, name=name, strokeColor="#bbbbbb")
        self.frame_id = fid
        return f

    def text(self, x, y, t, size=20, color=INK, align="left", link=None):
        lines = str(t).split("\n")
        w = max(len(l) for l in lines) * size * EM
        h = len(lines) * size * 1.25
        if align == "center":
            x -= w / 2
        elif align == "right":
            x -= w
        return self.base("text", x, y, w, h, strokeColor=color, text=str(t), originalText=str(t), fontSize=size,
                         fontFamily=6, textAlign=align, verticalAlign="top", containerId=None,
                         autoResize=True, lineHeight=1.25, link=link)

    def rect(self, x, y, w, h, stroke=INK, fill="transparent", width=2, dashed=False, round_=True):
        return self.base("rectangle", x, y, w, h, strokeColor=stroke, backgroundColor=fill, strokeWidth=width,
                         strokeStyle="dashed" if dashed else "solid",
                         roundness={"type": 3} if round_ else None)

    def line(self, x, y, points, color=GRAY, width=2, dashed=False):
        ox, oy = points[0]                 # Excalidraw expects the first point at the origin
        x, y = x + ox, y + oy
        points = [[px - ox, py - oy] for px, py in points]
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        return self.base("line", x, y, max(xs) - min(xs), max(ys) - min(ys), strokeColor=color,
                         strokeWidth=width, strokeStyle="dashed" if dashed else "solid",
                         points=[list(p) for p in points], lastCommittedPoint=None,
                         startBinding=None, endBinding=None, startArrowhead=None, endArrowhead=None)

    def dot(self, x, y, color, d=16):
        return self.base("ellipse", x, y, d, d, strokeColor=color, backgroundColor=color, strokeWidth=1)

    def pill(self, x_right, y, label, color, size=16):
        w = len(label) * size * EM + 24
        self.rect(x_right - w, y - 4, w, size * 1.25 + 8, stroke=color, fill="#ffffff", width=2)
        self.text(x_right - w / 2, y, label, size, color, align="center")

    def headline(self, x, y, answer, subtitle="", size=46):
        """Rule 0: the headline IS the answer; one gray subtitle under it."""
        self.text(x, y, answer, size, INK)
        if subtitle:
            self.text(x, y + size * 1.35, subtitle, 20, GRAY)

    def key(self, x, y, items, size=18):
        """Only the colours this frame uses: [(color, 'meaning'), ...]."""
        for color, meaning in items:
            self.dot(x, y + 3, color, 14)
            self.text(x + 22, y, meaning, size, GRAY)
            x += 22 + (len(meaning) + 3) * size * EM

    def source(self, x, y, label, link=None, size=16):
        """Rule 7: where the numbers came from, at the bottom, clickable when a link is given."""
        self.text(x, y, "Source · " + label, size, GRAY, link=link)

    def save(self, path, name="report"):
        doc = {"type": "excalidraw", "version": 2, "source": "excalidraw-report/plot_kit",
               "elements": self.els, "appState": {"viewBackgroundColor": "#ffffff", "gridSize": None},
               "files": {}}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(doc, f, indent=1)
        return path

    # ------------------------------------------------------------------ plots
    def title(self, x, y, t, size=24):
        """A plot's own 2-4 word title, above it."""
        return self.text(x, y, t, size, INK)

    def hbar(self, x, y, rows, width=820, label_w=300, row_h=46, color=GRAY, highlight=None,
             size=20, fmt=fmt_n, log=False, total=None):
        """Horizontal bars, largest first. rows = [(label, value), ...]; values become text.

        highlight: {label: color} for the one or two bars the headline is about; the rest stay
        `color`. log=True when values span more than two orders of magnitude (say so in the
        subtitle). total adds a share after each value. Returns the y below the last row."""
        rows = sorted(rows, key=lambda r: -float(r[1]))
        top = max(float(v) for _, v in rows) or 1.0
        lo = min((float(v) for _, v in rows if float(v) > 0), default=1.0)

        def length(v):
            v = float(v)
            if v <= 0:
                return 0
            if log:
                span = math.log10(top) - math.log10(lo) or 1.0
                return width * (0.08 + 0.92 * (math.log10(v) - math.log10(lo)) / span)
            return width * v / top

        for i, (label, v) in enumerate(rows):
            yy = y + i * row_h
            c = (highlight or {}).get(label, color)
            self.text(x, yy + (row_h - 8 - size * 1.25) / 2, label, size, INK)
            L = max(length(v), 4)
            self.rect(x + label_w, yy, L, row_h - 12, stroke=c, fill=FILL.get(c, c), width=1, round_=False)
            value = fmt(v) + (f"  ·  {pct(float(v), total)}" if total else "")
            self.text(x + label_w + L + 12, yy + (row_h - 8 - size * 1.25) / 2, value, size, c if c != GRAY else INK)
        base = x + label_w
        self.line(base, y - 6, [[0, 0], [0, len(rows) * row_h]], LGRAY, 2)
        return y + len(rows) * row_h

    def compare(self, x, y, items, height=320, bar_w=170, gap=120, size=22, fmt=fmt_n, note=""):
        """Two to four big vertical bars side by side. items = [(label, value, color), ...].
        The value sits on top of each bar; note (e.g. '12.7×') goes between the first two."""
        top = max(float(v) for _, v, _ in items) or 1.0
        for i, (label, v, c) in enumerate(items):
            bx = x + i * (bar_w + gap)
            h = max(height * float(v) / top, 4)
            self.rect(bx, y + height - h, bar_w, h, stroke=c, fill=FILL.get(c, c), width=2, round_=False)
            self.text(bx + bar_w / 2, y + height - h - size * 1.6, fmt(v), size + 4, c, align="center")
            self.text(bx + bar_w / 2, y + height + 12, label, size, INK, align="center")
        self.line(x - 20, y + height, [[0, 0], [len(items) * (bar_w + gap) - gap + 40, 0]], GRAY, 2)
        if note and len(items) >= 2:
            self.text(x + bar_w + gap / 2, y + height * 0.45, note, size + 6, ORANGE, align="center")
        return y + height + 12 + size * 1.4

    def share_bar(self, x, y, parts, width=1400, height=70, size=20, min_inside=110):
        """One 100% bar. parts = [(label, value, color), ...] in the order to show; the share
        goes inside a wide segment, and every part is listed under the bar with its share."""
        total = sum(float(v) for _, v, _ in parts) or 1.0
        cx = x
        for label, v, c in parts:
            w = width * float(v) / total
            self.rect(cx, y, max(w, 2), height, stroke="#ffffff", fill=FILL.get(c, c), width=2, round_=False)
            if w >= min_inside:
                self.text(cx + w / 2, y + (height - size * 1.25) / 2, pct(float(v), total), size, INK, align="center")
            cx += w
        self.rect(x, y, width, height, stroke=GRAY, fill="transparent", width=2, round_=False)
        ly, lx = y + height + 16, x
        for label, v, c in parts:
            item = f"{label} {pct(float(v), total)}"
            step = 22 + (len(item) + 3) * (size - 2) * EM
            if lx + step > x + width:
                lx, ly = x, ly + (size - 2) * 1.6
            self.dot(lx, ly + 3, c, 14)
            self.text(lx + 22, ly, item, size - 2, GRAY)
            lx += step
        return ly + (size - 2) * 1.6

    def columns(self, x, y, series, width=1200, height=260, color=BLUE, size=16, label_every=1,
                fmt=fmt_n, highlight=None):
        """A count over time: series = [(period_label, value), ...] in time order. The peak
        column carries its value; highlight={label: color} marks one period."""
        top = max(float(v) for _, v in series) or 1.0
        n = len(series)
        slot = width / max(n, 1)
        peak = max(range(n), key=lambda i: float(series[i][1]))
        for i, (lab, v) in enumerate(series):
            c = (highlight or {}).get(lab, color)
            h = max(height * float(v) / top, 1)
            bx = x + i * slot + slot * 0.12
            self.rect(bx, y + height - h, slot * 0.76, h, stroke=c, fill=FILL.get(c, c), width=1, round_=False)
            if i % label_every == 0 or i == n - 1:
                self.text(bx + slot * 0.38, y + height + 8, str(lab), size, GRAY, align="center")
            if i == peak:
                self.text(bx + slot * 0.38, y + height - h - size * 1.5, fmt(v), size + 2, c, align="center")
        self.line(x, y + height, [[0, 0], [width, 0]], GRAY, 2)
        return y + height + 8 + size * 1.4

    def spans(self, x, y, rows, start, end, width=1100, label_w=280, row_h=42, color=BLUE, size=18,
              tick_every=10):
        """When each thing starts and ends. rows = [(label, first, last, mark_or_None), ...];
        mark draws a dot (e.g. the peak year). The axis runs start..end with ticks."""
        def px(t):
            return x + label_w + width * (float(t) - start) / ((end - start) or 1)

        for i, (label, a, b, mark) in enumerate(rows):
            yy = y + i * row_h
            self.text(x, yy + 4, label, size, INK)
            a0, b0 = max(float(a), start), min(float(b), end)     # clamp to the axis; the label keeps the truth
            self.rect(px(a0), yy + 6, max(px(b0) - px(a0), 3), row_h - 18, stroke=color,
                      fill=FILL.get(color, color), width=1, round_=False)
            if float(a) < start:
                self.text(px(start) - 4, yy + 3, "◀", size - 2, GRAY, align="right")
            self.text(px(b0) + 10, yy + 4, f"{a}–{b}", size - 2, GRAY)
            if mark is not None and start <= float(mark) <= end:
                self.dot(px(mark) - 7, yy + 9, ORANGE, 14)
        ay = y + len(rows) * row_h + 6
        self.line(x + label_w, ay, [[0, 0], [width, 0]], GRAY, 2)
        t = start - start % tick_every + (tick_every if start % tick_every else 0)
        while t <= end:
            self.line(px(t), ay, [[0, 0], [0, 8]], GRAY, 2)
            self.text(px(t), ay + 12, str(t), size - 2, GRAY, align="center")
            t += tick_every
        return ay + 12 + size * 1.3

    def gauge(self, x, y, done, total, label, width=700, height=40, color=GREEN, size=22):
        """Done out of total, e.g. Runs complete or gates settled: one bar and 'N of M'."""
        frac = (float(done) / float(total)) if total else 0.0
        self.rect(x, y, width, height, stroke=LGRAY, fill="#f8f9fa", width=2, round_=False)
        if frac > 0:
            self.rect(x, y, max(width * frac, 3), height, stroke=color, fill=FILL.get(color, color), width=2,
                      round_=False)
        self.text(x + width + 18, y + (height - size * 1.25) / 2, f"{done:,} of {total:,}  {label}", size, INK)
        return y + height

    def trend(self, x, y, points, width=900, height=260, color=BLUE, size=16, fmt=fmt_n):
        """A line over ordered points = [(x_label, value), ...]; first and last values written."""
        vals = [float(v) for _, v in points]
        lo, hi = min(vals), max(vals)
        span = (hi - lo) or 1.0
        n = len(points)
        pts = [[width * i / max(n - 1, 1), height - height * (v - lo) / span] for i, v in enumerate(vals)]
        self.line(x, y, pts, color, 3)
        for i in (0, n - 1):
            self.dot(x + pts[i][0] - 7, y + pts[i][1] - 7, color, 14)
            # end labels sit beside their point, outside the line: left of the first, right of the last
            side = "right" if i == 0 else "left"
            lx = x + pts[i][0] + (-14 if i == 0 else 14)
            self.text(lx, y + pts[i][1] - (size + 2) * 0.65, fmt(vals[i]), size + 2, color, align=side)
            self.text(x + pts[i][0], y + height + 10, str(points[i][0]), size, GRAY, align="center")
        self.line(x, y + height, [[0, 0], [width, 0]], LGRAY, 2)
        return y + height + 10 + size * 1.3
