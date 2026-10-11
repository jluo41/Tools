"""A chronological Audience Report view over a report's authored event table.

The report remains the content authority. Opt in with a Markdown table headed
Date | Track | Development | Kind | Source. Kinds: recorded, observed, target.
Dates are YYYY-MM-DD, YYYY-MM (month only), or TBD; unknown dates are never placed
on a calendar. No file or browser interaction writes a report from this view.
"""
from collections import OrderedDict
import datetime as dt
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

from live.frame import esc, link, reader

COLUMNS = ("date", "track", "development", "kind", "source")
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def _cells(line):
    line = re.sub(r"<!--.*?-->", "", line).strip()
    if not line.startswith("|"):
        return []
    return [c.strip().replace(r"\|", "|") for c in re.split(r"(?<!\\)\|", line.strip("|"))]


def _date(value):
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        try:
            day = dt.date.fromisoformat(value)
            return day, day.strftime("%d %b").lstrip("0"), "day"
        except ValueError:
            return None
    if re.fullmatch(r"\d{4}-\d{2}", value):
        try:
            month = dt.date.fromisoformat(value + "-01")
            return month, month.strftime("%b %Y"), "month"
        except ValueError:
            return None
    if value.upper() == "TBD":
        return None, "TBD", "unknown"
    return None


def read_events(page):
    """Read the explicitly shaped table, outside fences; validate dates and kinds."""
    text = page.read_text(encoding="utf-8")
    lines = text.splitlines()
    events, active, fenced = [], False, False
    for line in lines:
        if line.strip().startswith("```"):
            fenced = not fenced
            active = False
            continue
        if fenced:
            continue
        cells = _cells(line)
        if tuple(c.casefold() for c in cells) == COLUMNS:
            active = True
            continue
        if active and cells and all(re.fullmatch(r":?-+:?", c) for c in cells):
            continue
        if not cells:
            active = False
            continue
        if not active or len(cells) != len(COLUMNS):
            continue
        event = dict(zip(COLUMNS, cells))
        parsed = _date(event["date"])
        if parsed is None or event["kind"] not in ("recorded", "observed", "target"):
            continue
        if not event["track"] or not event["development"]:
            continue
        if parsed[2] != "day" and event["kind"] != "target":
            continue                         # recorded history needs an exact date
        event.update(day=parsed[0], label=parsed[1], precision=parsed[2])
        events.append(event)
    asof = re.search(r"(?m)^timeline-as-of:\s*(\d{4}-\d{2}-\d{2})\s*$", text)
    parsed = _date(asof.group(1)) if asof else None
    title = re.search(r"(?m)^#\s+(.+)$", text)
    return {
        "page": page,
        "title": title.group(1).strip() if title else page.stem,
        "asof": parsed[0] if parsed else None,
        "events": sorted(events, key=lambda e: (e["day"] or dt.date.max, e["kind"] == "target")),
    }


def _sources(value, page, root):
    links = []
    for label, href in LINK.findall(value):
        parts = urlsplit(href)
        if parts.scheme in ("https", "http"):
            links.append(link(href, label))
        elif not parts.scheme and not parts.netloc and not href.startswith("/"):
            source = (page.parent / unquote(parts.path)).resolve()
            if source.is_relative_to(root.resolve()) and source.is_file():
                links.append(link(reader(source, root), label))
    return " · ".join(links) or '<span class=mut>Source unavailable</span>'


CSS = """
.tl-native{--tl-gap:22px}.tl-native h2{font-size:23px;margin:0 0 7px}.tl-intro{margin:0 0 15px;color:var(--mut)}
.tl-top{display:flex;gap:12px;justify-content:space-between;align-items:start;flex-wrap:wrap}
.tl-toolbar{display:flex;gap:6px;flex-wrap:wrap;margin:12px 0}.tl-toolbar button,.tl-jumps a{font:inherit;font-size:13px;
 border:1px solid var(--line);border-radius:6px;padding:5px 10px;background:var(--bg);color:var(--fg);cursor:pointer;text-decoration:none}
.tl-toolbar button[aria-pressed=true]{color:var(--tab-on);background:var(--tab-wash);border-color:var(--tab-on)}
.tl-jumps{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0 20px}.tl-jumps a{color:var(--acc)}
.tl-month{margin:0 0 27px}.tl-month h3{font-size:17px;margin:22px 0 14px;border-bottom:1px solid var(--line);padding-bottom:8px}
.tl-day{display:grid;grid-template-columns:78px minmax(0,1fr);gap:18px;position:relative;margin:0 0 14px}
.tl-date{font-size:14px;font-weight:600;white-space:nowrap;text-align:right;padding-top:15px}
.tl-stack{position:relative;border-left:2px solid var(--line);padding-left:20px;display:grid;gap:9px}
.tl-stack:before{content:'';position:absolute;top:20px;left:-6px;width:10px;height:10px;border-radius:50%;background:var(--fg)}
.tl-event{border:1px solid var(--line);border-radius:8px;padding:12px 15px;background:var(--bg);min-width:0}
.tl-event p{margin:6px 0 8px;overflow-wrap:anywhere}.tl-meta{display:flex;gap:8px;align-items:center;flex-wrap:wrap;font-size:12px}
.tl-track{border:1px solid var(--line);border-radius:4px;padding:1px 7px;font-weight:600}.tl-kind{color:var(--mut)}
.tl-source{font-size:12px;line-height:1.5}.tl-now{border:1px solid var(--tab-on);background:var(--tab-wash);color:var(--tab-on);
 border-radius:7px;padding:9px 13px;margin:16px 0 12px;font-weight:600;scroll-margin-top:20px}
.tl-target .tl-event,.tl-target .tl-stack{border-style:dashed}.tl-target .tl-stack:before{background:var(--bg);border:2px solid var(--acc)}
.tl-target .tl-kind{color:var(--acc)}.tl-legend{font-size:12px;color:var(--mut);margin:0 0 10px}
.tl-native [hidden]{display:none!important}.tl-native :target{scroll-margin-top:20px}
@media(max-width:760px){.tl-day{grid-template-columns:58px minmax(0,1fr);gap:12px}.tl-stack{padding-left:13px}.tl-event{padding:10px 12px}.tl-date{font-size:12px}}
"""

JS = """
(()=>{document.querySelectorAll('.tl-native').forEach(t=>{
 if(t.dataset.ready)return;t.dataset.ready='1';
 t.querySelectorAll('[data-tl-filter]').forEach(b=>b.addEventListener('click',()=>{
  const track=b.dataset.tlFilter;
  t.querySelectorAll('[data-tl-filter]').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));
  t.querySelectorAll('.tl-event').forEach(e=>e.hidden=Boolean(track&&e.dataset.track!==track));
  t.querySelectorAll('.tl-day').forEach(d=>d.hidden=!d.querySelector('.tl-event:not([hidden])'));
  t.querySelectorAll('.tl-month').forEach(m=>m.hidden=!m.querySelector('.tl-day:not([hidden])'));
 }));
});})();
"""


def render_report(data, root):
    page, events, asof = data["page"], data["events"], data["asof"]
    ident = "timeline-" + re.sub(r"[^a-zA-Z0-9_-]", "-", page.stem)
    tracks = list(dict.fromkeys(e["track"] for e in events))
    known = [e for e in events if e["kind"] != "target"]
    buttons = '<button type=button data-tl-filter="" aria-pressed=true>All tracks</button>' + ''.join(
        f'<button type=button data-tl-filter="{esc(track)}" aria-pressed=false>{esc(track)}</button>' for track in tracks)
    out = [f'<section class=tl-native id="{ident}">', '<div class=tl-top>',
           f'<div><h2>{esc(data["title"])}</h2><p class=tl-intro>Read from oldest to newest to see what changed over time.</p></div>',
           link(reader(page, root), "Report and sources ↗"), '</div>',
           f'<p class=tl-legend>{len(known)} recorded events · solid line: history · dashed line: provisional plans</p>',
           f'<div class=tl-toolbar aria-label="Filter timeline by track">{buttons}</div>',
           f'<nav class=tl-jumps aria-label="Timeline navigation"><a href="#{ident}-history">History</a>' +
           (f'<a href="#{ident}-now">Current snapshot</a>' if asof else '') +
           f'<a href="#{ident}-plans">Future targets</a></nav>', f'<div id="{ident}-history">']
    grouped = OrderedDict()
    for event in events:
        bucket = "unknown" if event["day"] is None else event["day"].strftime("%Y-%m")
        grouped.setdefault(bucket, []).append(event)
    plans_started = False
    for month, items in grouped.items():
        future = all(e["kind"] == "target" for e in items)
        name = 'Dates not set' if month == 'unknown' else items[0]["day"].strftime("%B %Y")
        if future and not plans_started:
            out.append(f'<h3 id="{ident}-plans">Future targets</h3>')
            plans_started = True
        out.append('<section class="tl-month' + (' tl-target' if future else '') + '">')
        out.append(f'<h3>{esc(name)}</h3>')
        days = OrderedDict()
        for event in items:
            days.setdefault(event['date'], []).append(event)
        for date, day_events in days.items():
            if asof and date == asof.isoformat():
                out.append(f'<div class=tl-now id="{ident}-now">Current snapshot · {asof.strftime("%d %B %Y").lstrip("0")}</div>')
            date_attr = '' if day_events[0]['precision'] == 'unknown' else f' datetime="{esc(date)}"'
            out.append(f'<div class="tl-day' + (' tl-target' if all(e['kind']=='target' for e in day_events) else '') + '">' +
                       f'<time class=tl-date{date_attr}>{esc(day_events[0]["label"])}</time><div class=tl-stack>')
            for event in day_events:
                kind = {"recorded": "Recorded", "observed": "Observed", "target": "Provisional · date pending"}[event['kind']]
                out += [f'<article class=tl-event data-track="{esc(event["track"])}">',
                        f'<div class=tl-meta><span class=tl-track>{esc(event["track"])}</span><span class=tl-kind>{kind}</span></div>',
                        f'<p>{esc(event["development"])}</p>',
                        f'<div class=tl-source>{_sources(event["source"], page, root)}</div></article>']
            out.append('</div></div>')
        out.append('</section>')
    out += ['</div></section>']
    return ''.join(out)


def group_timeline(block, root, rows, group):
    """Use an authored event table for this group, otherwise preserve the Question rows."""
    reports = []
    for row in rows:
        if str(row.get('group') or '') != group or not row.get('report'):
            continue
        page = (block / str(row['report'])).resolve()
        if not page.is_relative_to(root.resolve()) or not page.is_file():
            continue
        data = read_events(page)
        if data['events']:
            reports.append(data)
    if not reports:
        return ''
    return '<style>' + CSS + '</style>' + ''.join(render_report(d, root) for d in reports) + '<script>' + JS + '</script>'
