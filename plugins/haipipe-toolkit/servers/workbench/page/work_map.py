"""🗺️ A transit map of a Block's work: one coloured line per lane (a Job, a session, a person), one station per entry
in time order, an entry two lanes share joins their lines, a shaded band per day (the method of trace-canvas,
github.com/CallSymmetryEcho/trace-canvas; JL 261114: "the Map like this could be generated to other work map").

`transit_svg` draws any entries and uses the standard library only, so a Block's own build script imports it too
(b41_agreeablerx_replay draws its decisions with it). `block_map` draws a work Block's Jobs and their Runs; a
station is a Run, and a click opens that Run's page in the workbench pop-out.

A station carries `data-card` (JSON: tm, ti, chips, blocks) and, when it has a page, `data-href`; the workbench's
click handler (work_sections.PICK_JS) opens the page, or draws the card, in the pop-out.
"""
import datetime
import html
import json
import re
from pathlib import Path

COLOURS = ["#e4002b", "#0072ce", "#00a651", "#f68b1f", "#8e3a96", "#00a0b0", "#a6192e", "#5b6b7f", "#c99700",
           "#d0006f", "#2e7d32", "#6d4c41"]


def transit_svg(lanes, entries, noun="entry", lane_noun="lane"):
    """lanes: [(key, label)] top to bottom. entries: [{"time": "YYYY-MM-DD HH:MM", "lanes": [key, ...],
    "tip": str, "card": dict, "href": str?}] in time order. Returns the SVG text."""
    entries = [e for e in entries if any(k in dict(lanes) for k in e["lanes"])]
    if not entries:
        return ""
    left, step, top, lane = 150, 9, 46, 34
    keys = [k for k, _ in lanes if any(k in e["lanes"] for e in entries)]
    label = dict(lanes)
    height = top + lane * len(keys) + 44
    y = {k: top + lane * i + lane // 2 for i, k in enumerate(keys)}
    colour = {k: COLOURS[i % len(COLOURS)] for i, k in enumerate(keys)}
    day = [e["time"][:10] for e in entries]
    x, at, start = [], left + 20, 0
    for i in range(len(entries)):                            # a day is at least 84 px, so its name never overlaps
        if i and day[i] != day[i - 1]:
            at, start = max(at + step, x[start] + 84), i
        elif i:
            at += step
        x.append(at)
    width = x[-1] + 40
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
           'font-family="-apple-system,Segoe UI,sans-serif" font-size="12">']
    k, band_end = 0, {}
    while k < len(entries):                                  # one band per day, its name on top
        j = k
        while j < len(entries) and day[j] == day[k]:
            j += 1
        try:
            dt = datetime.date.fromisoformat(day[k])
            name, even = f'{dt.strftime("%a %b")} {dt.day}', dt.day % 2 == 0
        except ValueError:
            name, even = day[k], k % 2 == 0
        x0, x1 = x[k] - step / 2, (x[j] if j < len(entries) else x[j - 1] + step) - step / 2
        band_end[day[k]] = x1
        out.append(f'<rect x="{x0:.0f}" y="24" width="{x1 - x0:.0f}" height="{height - 24}" '
                   f'fill="{"#f3f5f8" if even else "#ffffff"}"/>')
        out.append(f'<text x="{x0 + 4:.0f}" y="16" fill="#5f6368" font-weight="600">{html.escape(name)}</text>')
        k = j
    for key in keys:                                         # each lane's line, from its first station to its last
        xs = [x[t] for t, e in enumerate(entries) if key in e["lanes"]]
        out.append(f'<text x="{left - 8}" y="{y[key] + 4}" text-anchor="end" fill="{colour[key]}" font-weight="600">'
                   f'{html.escape(label[key])}</text>')
        out.append(f'<line x1="{min(xs)}" y1="{y[key]}" x2="{max(xs)}" y2="{y[key]}" stroke="{colour[key]}" '
                   'stroke-width="5" stroke-linecap="round"/>')
        seen = set()                                         # its name again at its first station each day, the
        for t, e in enumerate(entries):                      # short form when the day is too narrow for the whole
            if key in e["lanes"] and day[t] not in seen:
                seen.add(day[t])
                room = band_end[day[t]] - x[t]
                name = label[key] if len(label[key]) * 6 < room else label[key].split()[0]
                out.append(f'<text x="{x[t] - 3}" y="{y[key] - 8}" fill="{colour[key]}" font-size="10" '
                           f'font-weight="600">{html.escape(name)}</text>')
    for t, e in enumerate(entries):                          # a station per entry; a shared one is an interchange
        on = [k for k in e["lanes"] if k in y]
        tip = html.escape(e.get("tip", ""))
        attrs = f'data-card="{html.escape(json.dumps(e.get("card", {}), ensure_ascii=False), quote=True)}"'
        if e.get("href"):
            attrs += f' data-href="{html.escape(e["href"], quote=True)}"'
        if len(on) > 1:
            ys = sorted(y[k] for k in on)
            out.append(f'<rect x="{x[t] - 4}" y="{ys[0] - 5}" width="8" height="{ys[-1] - ys[0] + 10}" rx="4" '
                       f'fill="#fff" stroke="#1b1c1f" stroke-width="1.5" {attrs}><title>{tip}</title></rect>')
        for k in on:
            out.append(f'<circle cx="{x[t]}" cy="{y[k]}" r="4" fill="#fff" stroke="#1b1c1f" stroke-width="1.3" '
                       f'{attrs}><title>{tip}</title></circle>')
    ly = height - 14                                         # the legend: what a line and a station mean
    out.append(f'<g font-size="12" fill="#5f6368"><line x1="{left - 120}" y1="{ly - 4}" x2="{left - 96}" y2="{ly - 4}" '
               'stroke="#0072ce" stroke-width="5" stroke-linecap="round"/>'
               f'<text x="{left - 88}" y="{ly}">one {html.escape(lane_noun)}</text>'
               f'<circle cx="{left + 10}" cy="{ly - 4}" r="4" fill="#fff" stroke="#1b1c1f" stroke-width="1.3"/>'
               f'<text x="{left + 20}" y="{ly}">one {html.escape(noun)} (click it)</text>'
               + (f'<rect x="{left + 176}" y="{ly - 13}" width="8" height="18" rx="4" fill="#fff" stroke="#1b1c1f" '
                  f'stroke-width="1.5"/><text x="{left + 192}" y="{ly}">shared by several</text>'
                  if any(len(e["lanes"]) > 1 for e in entries) else '') + '</g>')
    out.append("</svg>")
    return "\n".join(out)


# ── a work Block's own map: its Jobs and their Runs ─────────────────────────────────────────────────────────────
def _run_time(run: Path) -> str:
    """When a Run ran: its receipt's start, else its card's, else the folder's last change."""
    for f in (run / "result" / "runtime.yaml", run / "run.yaml"):
        if f.is_file():
            m = re.search(r"(?m)^(?:started_at|started|finished_at|time_started):\s*'?\"?(\d{4}-\d\d-\d\d)[T ](\d\d:\d\d)",
                          f.read_text(encoding="utf-8", errors="ignore"))
            if m:
                return f"{m.group(1)} {m.group(2)}"
    return datetime.datetime.fromtimestamp(run.stat().st_mtime).strftime("%Y-%m-%d %H:%M")


def block_map(block: Path, root: Path) -> str:
    """The SVG of a work Block's Jobs (one line each) and their Runs (a station each, in time order), or "" when it
    has fewer than two Runs."""
    from live import frame
    from live.focus_base import inside, page_url, read_face
    from live.focus_runs import run_headline
    jobs = [j for j in frame.children(block, "Block") if inside(j, root) and re.match(r"j\d\d_", j.name)]
    lanes, entries = [], []
    for j in jobs:
        lanes.append((j.name, j.name[:3] + " " + j.name[4:].replace("_", " ")[:22]))
        for t in frame.children(j, "Job"):
            if not inside(t, root):
                continue
            for run in sorted((t / "runs").glob("r[0-9]*")) if (t / "runs").is_dir() else []:
                if not run.is_dir():
                    continue
                when = _run_time(run)
                card = run / "run.yaml"
                says = (re.search(r"(?m)^says:\s*(.+)$", card.read_text(encoding="utf-8", errors="ignore"))
                        or [None, ""])[1].strip("'\" ") if card.is_file() else ""
                head = run_headline(run)
                entries.append({"time": when, "lanes": [j.name], "href": page_url(run, root),
                                "tip": f"{when[5:]} · {t.name} › {run.name}" + (f": {head}" if head else ""),
                                "card": {"tm": when[5:], "ti": f"{t.name} › {run.name}", "chips": [j.name[:3]],
                                         "blocks": [["Says", says], ["Returned", head]]}})
    if len(entries) < 2:
        return ""
    entries.sort(key=lambda e: e["time"])
    return transit_svg(lanes, entries, noun="Run", lane_noun="Job")
