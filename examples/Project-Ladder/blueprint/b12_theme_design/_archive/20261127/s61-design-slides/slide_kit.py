"""s61 · the slide layout, drawn once for two pens.

draw_slide(pen, slide) lays one slide out on a 1280 × 720 canvas: the title (the claim), the bullets
(one sentence each), then its picture (flow · ladder · grid · cards) in the room left below. A pen only
knows rect · text · arrow, in slide units with y at the top of a text; the drawing's pen sketches it into
the storyboard (build_s61_design_slides.py), the deck's pen writes it as SVG (build_deck.py). So a slide
on the storyboard and in the deck is the same layout.

Colour roles, mapped by each pen: ink · sub · mut · acc · border · warn.
"""

W, H, M = 1280, 720, 60
CW = [0.56]          # width of one character per point of size, for wrapping; draw_slide takes the pen's


def wrap(s, max_px, fs):
    """Greedy word wrap by estimated glyph width."""
    limit = max(6, int(max_px / (fs * CW[0])))
    lines, cur = [], ""
    for w in s.split():
        cand = (cur + " " + w).strip()
        if len(cand) <= limit or not cur:
            cur = cand
        else:
            lines.append(cur)
            cur = w
    return lines + ([cur] if cur else [])


def para(pen, x, y, s, max_px, fs, role="sub", bold=False, anchor="start", lh=1.3):
    """Wrapped text; returns the y below it."""
    for ln in wrap(s, max_px, fs):
        pen.text(x, y, ln, fs, role, bold, anchor)
        y += fs * lh
    return y


def bullets(pen, x, y, items, max_px, fs, role="sub", gap=8):
    for it in items:
        pen.text(x, y, "•", fs, role, True)
        y = para(pen, x + fs * 1.0, y, it, max_px - fs * 1.0, fs, role) + gap
    return y


# ── pictures, each in its box (x, y, w, h) ───────────────────────────────────────────────────
def flow(pen, x, y, w, h, nodes, loop=None):
    """Boxes left to right joined by arrows; `loop` draws a return arrow under them, with its label."""
    n, gap = len(nodes), 34
    bw = (w - gap * (n - 1)) / n
    fl, fs = 22, 18
    heads = [wrap(nd[0], bw - 20, fl) for nd in nodes]
    subs = [wrap(nd[1], bw - 20, fs) for nd in nodes]
    bh = max(len(a) * fl * 1.3 + 12 + len(b) * fs * 1.3 for a, b in zip(heads, subs)) + 44
    top = y + max(0, (h - bh - (90 if loop else 0)) / 2)
    for k, nd in enumerate(nodes):
        bx = x + k * (bw + gap)
        edge = len(nd) > 2                                # an input or an output: dashed
        pen.rect(bx, top, bw, bh, "acc" if not edge else "mut", dashed=edge, sw=1.5)
        ty = top + 22
        for ln in heads[k]:
            pen.text(bx + bw / 2, ty, ln, fl, "ink", True, "middle")
            ty += fl * 1.3
        ty += 12
        for ln in subs[k]:
            pen.text(bx + bw / 2, ty, ln, fs, "sub", False, "middle")
            ty += fs * 1.3
        if k < n - 1:
            pen.arrow([(bx + bw + 4, top + bh / 2), (bx + bw + gap - 4, top + bh / 2)], "ink")
    if loop:
        ly = top + bh + 46
        x_last, x_first = x + (n - 1) * (bw + gap) + bw / 2, x + bw / 2
        pen.arrow([(x_last, top + bh + 4), (x_last, ly), (x_first, ly), (x_first, top + bh + 6)], "acc")
        pen.text(x + w / 2, ly + 12, loop, 19, "acc", False, "middle")


def ladder(pen, x, y, w, h, rows):
    """A staircase, Block down to Run: each level a box, its folder and what it holds beside it."""
    step, lw, lh = 72, 140, 54
    rh = min(118, h / len(rows))
    for k, (level, folder, holds) in enumerate(rows):
        lx, ly = x + k * step, y + k * rh
        pen.rect(lx, ly, lw, lh, "acc", sw=1.5)
        pen.text(lx + lw / 2, ly + 13, level, 25, "ink", True, "middle")
        tx = lx + lw + 24
        pen.text(tx, ly + 1, folder, 21, "acc")
        para(pen, tx, ly + 30, holds, x + w - tx, 19, "sub")
        if k < len(rows) - 1:
            pen.arrow([(lx + 26, ly + lh + 2), (lx + 26, ly + rh + lh / 2), (lx + step - 4, ly + rh + lh / 2)], "ink")


def grid(pen, x, y, w, h, head, rows, note=None):
    """A table: the header row, then one row per line; the first column is the row's name."""
    n = len(head)
    first = w * 0.2
    cw = (w - first) / (n - 1)
    xs = [x] + [x + first + c * cw for c in range(n - 1)]
    widths = [first] + [cw] * (n - 1)
    fh, fc = 20, 19
    pen.rect(x, y, w, 46, "border", fill="fill2")
    for c, s in enumerate(head):
        pen.text(xs[c] + 14, y + 12, s, fh, "ink", True)
    ry = y + 46
    for row in rows:
        cells = [wrap(s, widths[c] - 28, fc) for c, s in enumerate(row)]
        rh = max(len(c) for c in cells) * fc * 1.3 + 26
        for c, lines in enumerate(cells):
            ty = ry + 13
            for ln in lines:
                pen.text(xs[c] + 14, ty, ln, fc, "ink" if c == 0 else "sub", c == 0)
                ty += fc * 1.3
        ry += rh
        pen.line(x, ry, x + w, ry, "border")
    for c in range(1, n):
        pen.line(xs[c], y, xs[c], ry, "border")
    pen.rect(x, y, w, ry - y, "border", sw=1)
    if note:
        para(pen, x, ry + 26, note, w, 21, "acc")


def cards(pen, x, y, w, h, cards, arrow=False):
    """Cards side by side, each a title over its bullets; `arrow` joins them left to right (before → after)."""
    n = len(cards)
    gap = 70 if arrow else 28
    cw = (w - gap * (n - 1)) / n
    ft, fb = 25, 21
    need = []
    for title, items in cards:
        yy = bullets(_Dry(), 0, 0, items, cw - 40, fb)
        need.append(yy + 84)
    ch = min(h, max(need))
    for k, (title, items) in enumerate(cards):
        cx = x + k * (cw + gap)
        pen.rect(cx, y, cw, ch, "acc" if k == n - 1 and arrow else "border", sw=1.5)
        pen.text(cx + 20, y + 22, title, ft, "ink", True)
        bullets(pen, cx + 20, y + 68, items, cw - 40, fb)
        if arrow and k < n - 1:
            pen.arrow([(cx + cw + 10, y + ch / 2), (cx + cw + gap - 10, y + ch / 2)], "ink")


class _Dry:
    """A pen that draws nothing: measures a layout before it is drawn."""
    def text(self, *a, **k):
        pass


PICTURES = {"flow": flow, "ladder": ladder, "grid": grid, "cards": cards}


# ── one slide ───────────────────────────────────────────────────────────────────────────────
def draw_slide(pen, s):
    CW[0] = pen.cw
    if s["slug"] == "cover":
        y = para(pen, W / 2, 230, s["title"], W - 2 * M, 62, "ink", True, "middle")
        y = para(pen, W / 2, y + 24, s["sub"], W - 4 * M, 28, "sub", False, "middle")
        pen.line(W / 2 - 80, y + 30, W / 2 + 80, y + 30, "acc")
        pen.text(W / 2, H - 80, s["foot"], 18, "mut", False, "middle")
        return
    y = para(pen, M, 44, s["title"], W - 2 * M, 42, "ink", True, lh=1.2)
    y = bullets(pen, M, y + 20, s.get("bullets", []), W - 2 * M, 23, "sub", gap=10)
    if s.get("picture"):
        kind, data = s["picture"]
        top = y + 26
        PICTURES[kind](pen, M, top, W - 2 * M, H - 40 - top, **data)
