"""A face's ## Background: its words folded, its timeline specs drawn as SVG."""
import re

import yaml
from live import frame
from live.work_progress_records import (
    _LOADER, e, section, text_of,
)


def background_md(job):
    """A face's `## Background` as Markdown pieces and drawn timelines, in order: ("md", text) or ("html", svg)."""
    text = section(text_of(frame.face(job)), "Background")
    out = []
    for k, chunk in enumerate(re.split(r"^```[^\n]*\n(.*?)^```[ \t]*$", text, flags=re.M | re.S)):
        if k % 2 == 0:
            if chunk.strip():
                out.append(("md", chunk))
            continue
        try:
            spec = yaml.load(chunk, Loader=_LOADER)
        except yaml.YAMLError:
            spec = None
        if isinstance(spec, dict) and isinstance(spec.get("timeline"), dict):
            out.append(("html", f'<figure>{timeline_svg(spec["timeline"])}</figure>'))
        else:
            out.append(("md", f"```\n{chunk}```\n"))
    return out


def timeline_svg(spec):
    """A meal drawn down its timeline (JL 261021: a sketch of Item1..Item3 as lanes, t1..tN down the side, and
    bites that take some of several items at one moment): each food item a vertical lane, each time a row, each
    bite a band across the items it holds. `spec`: {items, times, bites: [{name, at, items}], title?}. `spans:
    [{name, item, from, to, aside?}]` draws the other shape, one lane over a stretch of time (an exercise activity,
    from its start to its end; `aside` dashed, as a device's day total; s22 j02, JL 261021). A span with
    `zoom: true` and the block's `zoom: {items, times, bites, ...}` draw one picture: the day on the left, and that
    span opened on the right into its own lanes and bites, joined by two dashed lines (j01, JL 261021: "你可以把这两个
    图融成一个图吗"). `rule: {question, branches: [{answer, title, then, example, today?}]}` draws the handling rule
    as a small decision at the top right, a question and a box per answer (j01, JL 261021: "假如没有时间 ... 只记了开始、
    没有记结束，这时候该怎么办？... 你在这个地方完全没有显示出来")."""
    parts, width, height, at = timeline_parts(spec)
    if not parts:
        return ""
    zoom, opened = spec.get("zoom"), next((s for s in spec.get("spans") or [] if s.get("zoom")), None)
    extra, dx, below = "", width + 70, 0
    if isinstance(spec.get("rule"), dict):                           # the handling rule, top right
        rparts, rw, rh = rule_parts(spec["rule"], dx - 14, 40, int(spec["rule"].get("width") or 660))
        extra, below = rparts, 40 + rh + 40
        width, height = max(width, dx - 14 + rw + 6), max(height, below)
    if isinstance(zoom, dict) and opened and opened.get("name") in at:
        zparts, zw, zh, _ = timeline_parts(zoom, arrow=False)
        if zparts:
            x0, y0, x1, y1 = at[opened["name"]]                      # the span that opens, on the day
            mid = (y0 + y1) / 2
            dy = max(below, mid - zh / 2)                            # under the rule, when there is one
            fx, fy = dx - 14, dy
            extra += (f'<g transform="translate({dx} {dy})">{zparts}</g>'
                     f'<rect x="{fx}" y="{fy}" width="{zw + 14}" height="{zh}" rx="12" fill="none" '
                     'stroke="currentColor" stroke-width="1.5"/>'
                     f'<line x1="{x1}" y1="{y0}" x2="{fx}" y2="{fy + 12}" stroke="currentColor" stroke-width="1.2" '
                     'stroke-dasharray="5 5"/>'
                     f'<line x1="{x1}" y1="{y1}" x2="{fx}" y2="{fy + zh - 12}" stroke="currentColor" '
                     'stroke-width="1.2" stroke-dasharray="5 5"/>')
            width, height = max(width, dx + zw + 6), max(height, dy + zh + 4)    # room for the frame's stroke
    return (f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" '
            f'aria-label="{e(spec.get("title") or "a meal down its timeline")}" '
            'style="max-width:100%;height:auto;color:inherit;font-family:inherit">'
            '<defs><marker id="tl-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" '
            'orient="auto"><path d="M1 1 L9 5 L1 9" fill="none" stroke="currentColor" stroke-width="1.5"/></marker></defs>'
            + parts + extra + "</svg>")


def rule_parts(rule, x, y, w=660):
    """A handling rule as a small decision: the question in a box, then one box per answer side by side, each with
    its title, what is done, and its example from the picture; the answer that holds today is filled. Returns
    (shapes, width, height)."""
    def lines(text, width_px, size=14):                          # wrap by words, about 0.53 em a letter
        out, cur, cap = [], "", max(8, int(width_px / (size * 0.53)))
        for word in str(text).split():
            if cur and len(cur) + 1 + len(word) > cap:
                out.append(cur)
                cur = word
            else:
                cur = f"{cur} {word}".strip()
        return out + [cur] if cur else out

    def block(tx, ty, rows, size=14, weight="normal"):
        return "".join(f'<text x="{tx}" y="{ty + k * size * 1.35}" font-size="{size}" font-weight="{weight}" '
                       f'fill="currentColor">{e(r)}</text>' for k, r in enumerate(rows))

    branches = rule.get("branches") or []
    qh = 44
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{qh}" rx="10" fill="none" stroke="currentColor" '
           'stroke-width="1.5"/>'
           f'<text x="{x + w / 2}" y="{y + 28}" text-anchor="middle" font-size="15" font-weight="600" '
           f'fill="currentColor">{e(rule.get("question", ""))}</text>']
    if not branches:
        return "".join(out), w, qh
    gap = 24
    bw = (w - gap * (len(branches) - 1)) / len(branches)
    by = y + qh + 46
    boxes = []
    for k, b in enumerate(branches):
        bx = x + k * (bw + gap)
        title, then = lines(b.get("title", ""), bw - 24, 14), lines(b.get("then", ""), bw - 24, 14)
        ex = lines(b.get("example", ""), bw - 24, 13)
        bh = 18 + len(title) * 19 + 6 + len(then) * 19 + (8 + len(ex) * 18 if ex else 0) + 14
        boxes.append((bx, title, then, ex, bh, b))
    bh = max(h for *_, h, _ in boxes)
    for bx, title, then, ex, _, b in boxes:
        fill = "#fff3bf" if b.get("today") else "none"
        out.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="{fill}" stroke="currentColor" '
                   'stroke-width="1.5"/>')
        side = "start" if bx + bw / 2 >= x + w / 2 else "end"      # the answer beside its arrowhead, off the line
        out.append(f'<line x1="{x + w / 2}" y1="{y + qh}" x2="{bx + bw / 2}" y2="{by - 3}" stroke="currentColor" '
                   'stroke-width="1.5" marker-end="url(#tl-arrow)"/>'
                   f'<text x="{bx + bw / 2 + (12 if side == "start" else -12)}" y="{by - 10}" text-anchor="{side}" '
                   f'font-size="14" font-weight="600" fill="currentColor">{e(b.get("answer", ""))}</text>')
        ty = by + 22
        out.append(block(bx + 12, ty, title, 14, "600"))
        ty += len(title) * 19 + 6
        out.append(block(bx + 12, ty, then, 14))
        ty += len(then) * 19 + 8
        if ex:
            out.append(f'<g opacity="0.75">{block(bx + 12, ty, ex, 13)}</g>')
    return "".join(out), w, by - y + bh


def timeline_parts(spec, arrow=True):
    """One timeline's shapes, without the <svg> around them: (shapes, width, height, {span name: its box}).
    `arrow`: the time axis ends in an arrowhead (a zoomed panel draws its axis plain)."""
    items, times, bites = spec.get("items") or [], spec.get("times") or [], spec.get("bites") or []
    clock = spec.get("clock") if isinstance(spec.get("clock"), dict) else None
    if not items or not (times or clock):
        return "", 0, 0, {}
    left, top, col, row = 200, 78, 170, 62                      # left: room for the times, clear of a bite
    width = left + col * (len(items) - 1) + 120
    x = {it: left + col * k for k, it in enumerate(items)}
    if clock:                                                    # a real clock (s22 j02, JL 261021: "默认 ... by hour"):
        def mins(t):                                             # every hour the same height, each HH:MM where its
            h, m = str(t).split(":")                             # minutes put it, labels on the whole hours only
            return int(h) * 60 + int(m)
        start, end, px = mins(clock["from"]), mins(clock["to"]), float(clock.get("hour_px", 150))
        wrap = end <= start                                      # a night: 23:00 to 07:00 runs past midnight
        end += 1440 if wrap else 0
        on = lambda v: v + 1440 if wrap and v < start else v     # a time after midnight, on the night's own line
        step = int(clock.get("mark", 60))                        # minutes between labels: 60, or 180 for a whole day
        fmt = lambda v: f"{(v // 60) % 24 if wrap else v // 60:02d}:{v % 60:02d}"   # a day ends at 24:00
        hours = [fmt(v) for v in range(-(-start // step) * step, end + 1, step)]
        marks = {s.get(k) for s in spec.get("spans") or [] for k in ("from", "to")} | {b.get("at") for b in bites}
        y = {}
        for t in (marks - {None}) | set(hours):
            try:
                y[t] = top + 36 + (on(mins(t)) - start) / 60 * px
            except (ValueError, AttributeError):
                pass
        labels = {t: y[t] for t in hours}
        height = int(top + 36 + (end - start) / 60 * px + 30)
    else:
        y = {t: top + 36 + row * k for k, t in enumerate(times)}
        labels = y
        height = top + row * len(times) + 20
    out, boxes = [], {}
    out.append(f'<text x="{left + col * (len(items) - 1) / 2}" y="22" text-anchor="middle" font-size="15" '
               f'font-weight="600" fill="currentColor">{e(spec.get("items_label") or "Food items")}</text>')
    for it, cx in x.items():                                     # a lane per food item, its name on top
        out.append(f'<text x="{cx}" y="{top - 22}" text-anchor="middle" font-size="14" fill="currentColor">{e(it)}</text>'
                   f'<line x1="{cx}" y1="{top - 10}" x2="{cx}" y2="{height - 12}" stroke="currentColor" '
                   'stroke-width="2"/>')
    out.append(f'<text x="22" y="{(top + height - 20) / 2}" font-size="14" fill="currentColor" '
               f'transform="rotate(-90 22 {(top + height - 20) / 2})" text-anchor="middle">'
               f'{e(spec.get("time_label") or "Timeline")}</text>'
               f'<line x1="40" y1="{top}" x2="40" y2="{height - 14}" stroke="currentColor" stroke-width="1.5"'
               + (' marker-end="url(#tl-arrow)"' if arrow else "") + '/>')
    for t, ty in labels.items():                                 # a row per moment (on a clock, per whole hour)
        out.append(f'<text x="{left - 90}" y="{ty + 5}" text-anchor="end" font-size="14" fill="currentColor">{e(t)}</text>')
        if clock:                                                # the hour's line across the lanes, faint
            out.append(f'<line x1="{left - 80}" y1="{ty}" x2="{left + col * (len(items) - 1) + 80}" y2="{ty}" '
                       'stroke="currentColor" stroke-width="1" stroke-dasharray="2 6" opacity="0.45"/>')
    for b in bites:                                              # a bite: a band across the items it holds
        held = [x[i] for i in b.get("items") or [] if i in x]
        if not held or b.get("at") not in y:
            continue
        x0, x1, ty = min(held) - 52, max(held) + 52, y[b["at"]]
        out.append(f'<rect x="{x0}" y="{ty - 17}" width="{x1 - x0}" height="34" rx="9" fill="#fff3bf" '
                   'stroke="currentColor" stroke-width="1.5"/>'
                   f'<text x="{(x0 + x1) / 2}" y="{ty + 5}" text-anchor="middle" font-size="14" fill="#1e1e1e">'
                   f'{e(b.get("name", ""))}</text>')
    for s in spec.get("spans") or []:                            # a span: one lane over a stretch of time
        if s.get("item") not in x or s.get("from") not in y or s.get("to") not in y:
            continue
        cx, y0, y1, aside = x[s["item"]], y[s["from"]], y[s["to"]], bool(s.get("aside"))
        y0, y1 = y0 + 3, max(y1 - 3, y0 + 33)                    # from its start to its end: back to back, never overlapping
        hw = max(58, min(col / 2 - 6, len(s.get("name", "")) * 3.8 + 9))   # wide enough for its name, within its lane
        out.append(f'<rect x="{cx - hw}" y="{y0}" width="{2 * hw}" height="{y1 - y0}" rx="9" '
                   f'fill="{"#ffffff" if aside else "#fff3bf"}" stroke="currentColor" '
                   f'stroke-width="{2.5 if s.get("zoom") else 1.5}"'
                   + (' stroke-dasharray="6 5"' if aside else "") + '/>'
                   f'<text x="{cx}" y="{(y0 + y1) / 2 + 5}" text-anchor="middle" font-size="14" fill="#1e1e1e">'
                   f'{e(s.get("name", ""))}</text>')
        boxes[s.get("name", "")] = (cx - hw, y0, cx + hw, y1)
    return "".join(out), width, height, boxes


def background_html(folder):
    """A face's `## Background`, under its goal and above the tree: what the work is for, in plain words (JL 261021:
    "可以再加一个 section，比如叫 background 啥的，介绍一下我们要实现什么"). A `- ` line is a bullet (its next lines
    continue it), anything else a paragraph; **bold** and `code` keep their look. A fenced yaml block holding
    `timeline:` is drawn as a picture (timeline_svg); another fenced block shows as it is written. The words fold
    under one "BACKGROUND · N points" line, closed by default; the pictures stay in view (JL 261021: "像这种
    background，我们可以给它 hide 一下吗"). No section, nothing drawn."""
    text = section(text_of(frame.face(folder)), "Background") if folder else ""
    if not text:
        return ""

    def inline(s):
        s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", e(s.strip()))
        return re.sub(r"`([^`]+)`", r"<code>\1</code>", s)

    def prose(chunk):
        out, bullets = [], []
        for line in chunk.splitlines():
            if line.lstrip().startswith(("- ", "* ")):
                bullets.append(line.lstrip()[2:])
            elif line.strip() and bullets and line.startswith((" ", "\t")):
                bullets[-1] += " " + line.strip()
            else:
                if bullets:
                    out.append("<ul>" + "".join(f"<li>{inline(b)}</li>" for b in bullets) + "</ul>")
                    bullets = []
                if line.strip():
                    out.append(f"<p>{inline(line)}</p>")
        if bullets:
            out.append("<ul>" + "".join(f"<li>{inline(b)}</li>" for b in bullets) + "</ul>")
        return out

    words, out, figs = [], [], []                                # the words fold away; the pictures stay in view

    def flush():                                                 # pictures in a row share one line, as a day and its
        if figs:                                                 # zoom (j01, JL 261021: "zoom in ... bite1, bite2")
            out.append('<div style="display:flex;flex-wrap:wrap;gap:8px 36px;align-items:flex-start">'
                       + "".join(figs) + "</div>" if len(figs) > 1 else figs[0])
            figs.clear()

    for k, chunk in enumerate(re.split(r"^```[^\n]*\n(.*?)^```[ \t]*$", text, flags=re.M | re.S)):
        if k % 2 == 0:                                           # the prose between fences
            if chunk.strip():
                flush()
            words += prose(chunk)
            continue
        try:
            spec = yaml.load(chunk, Loader=_LOADER)
        except yaml.YAMLError:
            spec = None
        if isinstance(spec, dict) and isinstance(spec.get("timeline"), dict):
            figs.append(f'<figure style="margin:10px 0 12px;max-width:100%">{timeline_svg(spec["timeline"])}'
                        + (f'<figcaption class=mut style="font-size:12px;max-width:900px">'
                           f'{inline(spec["timeline"]["caption"])}</figcaption>' if spec["timeline"].get("caption") else "")
                        + "</figure>")
        else:
            flush()
            out.append(f"<pre>{e(chunk.rstrip())}</pre>")
    flush()
    n = sum(w.count("<li>") for w in words) or len(words)
    folded = (f'<details data-work-key="background-{e(folder.name)}"><summary class=mut style="cursor:pointer;'
              f'font-size:12px;letter-spacing:.04em">BACKGROUND · {n} point{"s" * (n != 1)}, click to read</summary>'
              + "".join(words) + "</details>") if words else ""   # folded by default (JL 261021: "background ... hide")
    return ('<div class=goal-bg style="margin:6px 0 14px;font-size:14px;line-height:1.55">'
            + folded + "".join(out) + "</div>")
