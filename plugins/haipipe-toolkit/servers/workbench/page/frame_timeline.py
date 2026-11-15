"""Studio > Timeline: what moved when, read from decisions, sessions and drawing notes already on disk."""

from __future__ import annotations

import datetime
import json
import re
from pathlib import Path

from live.frame_base import _e, _reader, pop
from live.frame_studio import _draw_url, _note_facts, _notes, _sessions, studio_anchor, studio_inventory
from live.frame_groups import group_emoji, studio_group_order


# ── Studio › Timeline: what moved when, the fifth folding part (JL 261011; fourth until Runs came, 261019) ─────────────────
# Read from what is already on disk, nothing new to write: each topic's dated decisions (sNN-DNN …
# (JL 261011)), its sessions (runs/run-draw-<sNN>/passes/pNN-<MMDD>/) and the green change notes in
# its drawing (✎ <YYMMDD> <what>, haipipe-studio's change notes). Newest day first; the page script
# hides a topic's lines when the group bar hides its row.
_YYMMDD = re.compile(r"(?<!\d)(2[4-9])(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])(?!\d)")
_NOTES_SEEN: dict = {}


def _yymmdd(m) -> str:
    return f"20{m.group(1)}-{m.group(2)}-{m.group(3)}"


def _drawing_notes(d: Path) -> list:
    """(day, what) for each green change note in a drawing, read once per version of the file."""
    try:
        stat = d.stat()
    except OSError:
        return []
    key = (str(d), stat.st_mtime_ns, stat.st_size)
    if key not in _NOTES_SEEN:
        try:
            elements = json.loads(d.read_text(encoding="utf-8")).get("elements") or []
        except (OSError, ValueError, AttributeError):
            elements = []
        notes = []
        for el in elements:
            if not isinstance(el, dict) or el.get("type") != "text" or el.get("isDeleted"):
                continue
            text = re.sub(r"\s+", " ", str(el.get("text") or "")).strip()
            m = _YYMMDD.match(text[1:].strip()) if text.startswith("✎") else None
            if m:
                notes.append((_yymmdd(m), text[1:].strip()[m.end():].strip()))
        if len(_NOTES_SEEN) > 2000:
            _NOTES_SEEN.clear()
        _NOTES_SEEN[key] = notes
    return _NOTES_SEEN[key]


def _decisions(md: Path | None) -> list:
    """(day or "", id, what) for each `sNN-DNN · <what>` line of a topic's notes, its indented lines
    included; the day is the first YYMMDD in it, when it was decided."""
    if not md:
        return []
    out, cur = [], None
    for line in md.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = re.match(r"(s\d+-D\d+)\b[ \t]*[·:\-–]?[ \t]*(.*)", line)
        if m:
            cur = [m.group(1), m.group(2)]
            out.append(cur)
        elif cur and line[:1] in (" ", "\t") and line.strip():
            cur[1] += " " + line.strip()
        else:
            cur = None
    found = []
    for did, what in out:
        day = _YYMMDD.search(what)
        found.append((_yymmdd(day) if day else "", did, re.sub(r"\s+", " ", what.replace(chr(96), "")).strip()))
    return found


def _session_day(name: str, md: Path | None) -> str:
    """A session's day: pNN-<MMDD> with the year its notes give it, else the latest year not ahead of today;
    an older chat/ session by the date in its name."""
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", name)
    if m:
        return "-".join(m.groups())
    m = re.match(r"p\d+-(\d{2})(\d{2})$", name)
    if not m:
        return ""
    text = md.read_text(encoding="utf-8", errors="ignore") if md and md.is_file() else ""
    years = [y.group(1) for y in _YYMMDD.finditer(text) if (y.group(2), y.group(3)) == m.groups()]
    if years:
        return f"20{years[0]}-{m.group(1)}-{m.group(2)}"
    today = datetime.date.today()
    try:
        day = datetime.date(today.year, int(m.group(1)), int(m.group(2)))
    except ValueError:
        return ""
    return (day if day <= today else day.replace(year=today.year - 1)).isoformat()


def timeline_events(block: Path, root: Path) -> tuple:
    """(events, undated): every dated thing of the Block's Studio topics, newest first. An event is a dict
    of day, key (the topic's row key under the group bar), name, anchor, tags (its groups), kind (decided ·
    session · drawing) and its html."""
    block, root = block.resolve(), root.resolve()
    events, undated = [], []
    for source, topic, drawings in studio_inventory(block, root):
        name = topic.name if topic.is_dir() else topic.stem
        base = {"key": topic.relative_to(block).as_posix(), "name": name, "anchor": studio_anchor(topic, source, block),
                "tags": _note_facts(_notes(topic))["tags"]}
        for day, did, what in _decisions(_notes(topic)):
            if not day:
                undated.append(did)
                continue
            short = what if len(what) <= 150 else what[:149].rsplit(" ", 1)[0] + " …"
            events.append(dict(base, day=day, kind="decided",
                               html=f'<b>{_e(did)}</b> <span title="{_e(what)}">{_e(short)}</span>'))
        for s in _sessions(topic, source):
            md = s["path"] if s["path"].is_file() else None
            day = _session_day(s["name"], md)
            if day:
                events.append(dict(base, day=day, kind="session",
                                   html=pop(_reader(s["path"], root), f'{name} · {s["name"]}', f'{s["name"]} · {s["title"]}')
                                   if md else _e(f'{s["name"]} · {s["title"]}')))
        for d in drawings:
            by_day = {}
            for day, what in _drawing_notes(d):
                by_day.setdefault(day, []).append(what)
            for day, whats in by_day.items():
                events.append(dict(base, day=day, kind="drawing", n=len(whats),
                                   html=f'{pop(_draw_url(d, root), d.stem, d.stem + " ↗")} '
                                        f'{_e(" · ".join(dict.fromkeys(w for w in whats if w)))}'))
    order = {"decided": 0, "session": 1, "drawing": 2}
    events.sort(key=lambda e: (e["name"], order[e["kind"]]))
    events.sort(key=lambda e: e["day"], reverse=True)          # newest day first, topics in sNN order
    return events, undated


TIMELINE_LEVELS = ("Days", "Topics", "Everything")
TIMELINE_KINDS = (("decided", "decided", "decided"), ("session", "session", "sessions"), ("drawing", "note", "notes"))


def studio_timeline(block: Path, root: Path) -> str:
    """The Studio's fifth folding part, Timeline, under Runs (b10 s08; JL 261011: "add another section of
    the Timeline", "a real timelne ... very concise ... with a axis down", "up to down", "different level of
    details", then "it is not that beautiful ... like using the visualization tools"): time runs down one
    axis, the oldest day at the top. Days, the default, is a chart: a row per day, a column per topic, a
    bubble sized by how much that topic moved that day, and the day's total as a bar. Topics turns each day
    into a line per topic with a stacked bar of its kinds; Everything adds each decision, session and note.
    The chart's columns are the topic groups (the group bar's, in its order, Untagged last) or the topics
    (JL 261011: "the columns can also be the topic groups"); a group's bubble adds up its topics, so a
    topic in two groups counts in both, and the day's bar still counts each change once."""
    events, _ = timeline_events(block, root)
    days, topics = {}, {}
    for e in sorted(events, key=lambda e: e["day"]):          # oldest first; topics stay in sNN order
        days.setdefault(e["day"], {}).setdefault(e["key"], []).append(e)
    try:                       # every day from the first to the last, the quiet ones too: a real axis (JL 261012:
        first, last = (datetime.date.fromisoformat(d) for d in (min(days), max(days)))   # "show the days between them")
        span = [(first + datetime.timedelta(i)).isoformat() for i in range((last - first).days + 1)]
        days = {day: days.get(day, {}) for day in span}
    except ValueError:
        pass
    for e in sorted(events, key=lambda e: e["name"]):
        topics.setdefault(e["key"], (e["name"], e["anchor"]))
    years = {day[:4] for day in days}
    tags = {}
    for e in events:
        tags.setdefault(e["key"], e.get("tags") or [])
    groups, loose = {}, [k for k in topics if not tags.get(k)]
    for name in studio_group_order(block) + sorted({g for gs in tags.values() for g in gs}, key=str.casefold):
        groups.setdefault(name.casefold(), (name, []))
    for k in topics:
        for g in tags.get(k) or []:
            groups[g.casefold()][1].append(k)
    groups = {g: v for g, v in groups.items() if v[1]}
    if loose:
        groups["__untagged__"] = ("Untagged", loose)

    def size(items: list) -> int:
        return sum(e.get("n", 1) for e in items)

    def tally(items: list) -> dict:
        return {k: sum(e.get("n", 1) for e in items if e["kind"] == k) for k, _, _ in TIMELINE_KINDS}

    def says(items: list) -> str:
        t = tally(items)
        return " · ".join(f"{t[k]} {one if t[k] == 1 else many}" for k, one, many in TIMELINE_KINDS if t[k])

    def label(day: str) -> str:
        try:
            return datetime.date.fromisoformat(day).strftime("%a %d %b" + (" %Y" if len(years) > 1 else ""))
        except ValueError:
            return day

    def sid(name: str) -> str:
        m = re.match(r"s\d+", name)
        return m.group(0) if m else name

    cell_peak = max((size(items) for ts in days.values() for items in ts.values()), default=1)
    day_peak = max((size([e for items in ts.values() for e in items]) for ts in days.values()), default=1)
    group_peak = max((sum(size(ts[k]) for k in ks if k in ts) for ts in days.values() for _, ks in groups.values()),
                     default=1) or 1
    cols = "groups" if any(g != "__untagged__" for g in groups) else "topics"
    ghead = "".join(f'<button type=button class=tl-gcol data-tl-group="{_e(g)}" title="{_e(n)}: '
                    f'{_e(" · ".join(sid(topics[k][0]) for k in ks))}">'
                    f'{"" if g == "__untagged__" else _e(group_emoji(n)) + " "}{_e(n)}</button>'
                    for g, (n, ks) in groups.items())
    # Days: the chart, a row per day down the axis and a column per topic
    # a topic's column carries its full name (JL 261012: "for the sNN, here could you give it the full name?"):
    # the sNN straight and bold over the column, the rest slanted up above it; columns 60 px wide (JL 261012:
    # "make the columns width wider, and make the sNN to be more readable"). The header fits the longest name
    head = "".join(f'<a class=tl-col data-tl-key="{_e(k)}" href="#{_e(a)}" title="{_e(n)}"><b>{_e(sid(n))}</b>'
                   f'<span>{_e(n[len(sid(n)):].lstrip("-_ "))}</span></a>' for k, (n, a) in topics.items())
    slant = min(round(max((len(n) - 4 for n, _ in topics.values()), default=0) * 7.2 * 0.71) + 40, 200)
    chart = []
    for day, ts in days.items():
        cells, n_day = [], 0
        for k, (n, a) in topics.items():
            items = ts.get(k)
            if not items:
                cells.append(f'<span class=tl-cell data-tl-key="{_e(k)}"></span>')
                continue
            n_day += size(items)
            px = round(8 + 18 * (size(items) / cell_peak) ** 0.5)
            cells.append(f'<span class=tl-cell data-tl-key="{_e(k)}" data-tl-count={size(items)}>'
                         f'<a class=tl-b href="#{_e(a)}" style="--s:{px}px" '
                         f'title="{_e(n)} · {_e(label(day))} · {_e(says(items))}"></a></span>')
        for g, (gname, ks) in groups.items():
            parts = {k: size(ts[k]) for k in ks if k in ts}
            n_g = sum(parts.values())
            ball = (f'<button type=button class=tl-gb style="--s:{round(8 + 22 * (n_g / group_peak) ** 0.5)}px" '
                    f'title="{_e(gname)} · {_e(label(day))} · {n_g} changes: '
                    f'{_e(" · ".join(f"{sid(topics[k][0])} {v}" for k, v in parts.items()))}"></button>' if n_g else "")
            cells.append(f'<span class=tl-gcell data-tl-group="{_e(g)}" data-tl-parts="{_e(json.dumps(parts))}">{ball}</span>')
        chart.append(f'<div class="tl-mrow{"" if ts else " tl-quiet"}" data-day="{_e(day)}"><time datetime="{_e(day)}">{_e(label(day))}</time>'
                     f'<span class=tl-dot></span>{"".join(cells)}<span class=tl-bar><span class=tl-track>'
                     f'<i style="width:{round(n_day / day_peak * 100)}%"></i></span><b>{n_day}</b></span></div>')
    # Topics and Everything: a line per topic under its day, a stacked bar of its kinds, then its items
    days_html = []
    for day, ts in days.items():
        lines = []
        for k, items in ts.items():
            n, a = topics[k]
            t = tally(items)
            stack = "".join(f'<i class=k-{kind} style="flex:{t[kind]}"></i>' for kind, _, _ in TIMELINE_KINDS if t[kind])
            lis = "".join(f'<li><i class="tl-kd k-{e["kind"]}" title="{dict((k_, o) for k_, o, _ in TIMELINE_KINDS)[e["kind"]]}">'
                          f'</i>{e["html"]}</li>' for e in items)
            lines.append(f'<div class=tl-topic data-tl-key="{_e(k)}" data-tl-count={size(items)}>'
                         f'<a class=tl-name href="#{_e(a)}" title="{_e(n)}"><b>{_e(sid(n))}</b>'
                         f'<span>{_e(n[len(sid(n)):].lstrip("-_ "))}</span></a>'
                         f'<span class=tl-meter title="{_e(says(items))}"><span class=tl-stack style="width:'
                         f'{max(round(size(items) / cell_peak * 240), 6)}px">{stack}</span><span class=tl-n>{size(items)}</span>'
                         f'</span><ul class=tl-items>{lis}</ul></div>')
        days_html.append(f'<li class="tl-day{"" if ts else " tl-quiet"}" data-day="{_e(day)}"><time datetime="{_e(day)}">{_e(label(day))}</time>'
                         f'<div class=tl-body>{"".join(lines)}</div></li>')
    levels = "".join(f'<button type=button data-tl-level={lv.lower()} aria-pressed={"true" if lv == "Days" else "false"}>'
                     f'{lv}</button>' for lv in TIMELINE_LEVELS)
    keys = "".join(f'<i class="tl-kd k-{kind}"></i>{one}' for kind, one, _ in TIMELINE_KINDS)
    # undated decisions are not listed (JL 261012: "I don't want this"); timeline_events still returns them
    body = (f'<div class=tl-wrap data-level=days><nav class=tl-levels aria-label="How much the Timeline shows">{levels}'
            f'<span class="tl-cols tl-legend-b">columns <button type=button data-tl-cols=groups aria-pressed='
            f'{"true" if cols == "groups" else "false"}>by group</button><button type=button data-tl-cols=topics '
            f'aria-pressed={"true" if cols == "topics" else "false"}>by topic</button></span>'
            f'<span class="tl-help tl-legend-b">a bubble: how much moved that day · click a group for its topics, '
            f'a topic to read it</span><span class="tl-help tl-legend-k">{keys}</span></nav>'
            # the group bar's groups again, here, so a group is picked without scrolling up (JL 261012:
            # "我这怎么选其他的？比如说 group 呢，或者说 topic 呢？"); the page script fills it from the bar
            f'<nav class=tl-groups aria-label="Pick a topic group"></nav>'
            f'<div class=tl-map data-cols={cols} style="--tl-slant:{slant}px"><div class=tl-mhead><span></span><span></span>{head}{ghead}'
            f'<span class=tl-bar-h>changes</span>'
            f'</div>{"".join(chart)}</div><div class=tl-picked></div>'
            f'<ol class="tl-axis tl-list">{"".join(days_html)}</ol></div>' if days else
            '<p class=mut>Nothing dated yet: a decision gets its date in brackets, (JL 261011).</p>')
    return (f'<details class="studio-related studio-timeline" id=studio-timeline>'
            f'<summary><b>Timeline</b></summary>'                # no counts (JL 261011: "I don't need this")
            f'<div class=related-in>{body}</div></details>')
