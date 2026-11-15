"""The focus page's Studio, Timeline, Files and Related sections."""
from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import urlencode

from live import frame
from live.ui_parts import COPY_JS, copy_verb
from live.focus_base import in_group, inside, is_topic, markdown, origin, page_level, page_url, read_face, rollup
from live.focus_interactions import interaction_button
from live.focus_tree import work_root


def topic_rows(folder: Path, root: Path, inventory: list | None = None) -> list:
    """The page's own Studio topics, then its children's (frame.studio_inventory), each with where it lives; or the
    (source, topic, drawings) a page type hands in (a draft Task: the Block topics that name it)."""
    rows = []
    sources = rollup(folder) if page_level(folder) in ("SPACE", "Folder", "Project", "Theme") else None
    if inventory is None:
        inventory = ([(s, t, d) for s in sources for t, d in frame._studio_topics(s)] if sources
                     else frame.studio_inventory(folder, root))
    for source, topic, drawings in inventory:
        if not inside(topic, root):
            continue
        notes = frame._notes(topic)
        facts = frame._note_facts(notes) if notes and inside(notes, root) else {"tags": []}
        rows.append((topic, [p for p in drawings if inside(p, root)], {**facts, "origin": origin(source, folder)}))
    return rows


def studio_none(folder: Path, root: Path) -> str:
    """A page's Studio with no topic yet (b11 form, JL 261106: "Studio says none yet, with Add a topic"): one line, and a
    verb that copies the prompt for haipipe-studio's new_topic.py at this page."""
    prompt = (f"/haipipe-studio add a Studio topic at {frame.rel(folder, root)}: name it after the one question it "
              "thinks about, make it with scripts/new_topic.py, then draw it.")
    return (COPY_JS + '<p class="mut">No Studio topic here yet.</p><div class="focus-actions">'
            + copy_verb("Add a topic", prompt) + '</div>')


def studio_html(rows, root, group, asks=(), *, tabs=False):
    """One row per topic, four things only (JL 261029: "the information here is a bit overwhelmed"): its picture
    (the lead idea slide, else the drawing's preview), its name (address @ topic), the one line it asks, its stage
    as a word; then Slides, Draw, Mind map. The name opens the face. Rounds, ideas and tags live behind it. `asks` are
    the interactions in reach (card_interactions): each one about a topic shows on its card, the same badge as Work's."""
    if tabs:
        from live import studio_tabs
        return studio_tabs.render(rows, root, group, asks)
    out = []
    for topic, drawings, facts in rows:
        if not in_group(facts, group):
            continue
        title = topic.name if topic.is_dir() else topic.stem
        notes = frame._notes(topic)
        face_url = frame.reader(notes, root) if notes and inside(notes, root) else ""
        draw_url = frame._draw_url(drawings[0], root) if drawings else ""
        url = face_url or draw_url                  # no topic page (JL 261031): the name opens the face, popped out
        lead_slide = None
        record = topic / f"{topic.name}.slides.json" if topic.is_dir() else None
        if record and record.is_file():
            try:
                first = json.loads(record.read_text(encoding="utf-8"))["slides"][0]["image"]
                lead_slide = topic / first if (topic / first).is_file() and inside(topic / first, root) else None
            except (ValueError, KeyError, IndexError, TypeError):
                lead_slide = None
        previews = [d.with_suffix(".png") for d in drawings] + ([topic / (topic.name + ".png")] if topic.is_dir() else [])
        preview = lead_slide or next((p for p in previews if p.is_file() and inside(p, root)), None)
        deck = topic / f"{topic.name}.slides.html" if topic.is_dir() else None
        deck_url = "/" + frame.rel(deck, root) if deck and deck.is_file() and inside(deck, root) else ""
        mind = topic / f"{topic.name}.mindmap.md" if topic.is_dir() else None
        verbs = []
        # everything on a row pops out over the page, so a reader previews a topic without leaving it (JL 261029: "I
        # want to make things here to be pop out")
        if deck_url:
            verbs.append(f'<a class="row-verb main" data-pop="{frame.esc(title)} · slide" href="{frame.esc(deck_url)}" target=_blank rel=noopener>'
                         f'{"Slide" if is_topic(topic) else "Slides"}</a>')   # JL 261031: "we might just call it Slide"
        if draw_url:
            verbs.append(f'<a class="row-verb" data-pop="{frame.esc(title)}" href="{frame.esc(draw_url)}" target=_blank rel=noopener>Draw</a>')
        if mind and mind.is_file() and inside(mind, root):
            verbs.append(f'<a class="row-verb" data-pop="{frame.esc(title)} · mind map" href="{frame.esc(frame.ROUTE + "?" + urlencode({"view": "focus-map", "path": frame.rel(mind, root)}))}" target=_blank rel=noopener>Mind map</a>')
        if topic.is_dir() and is_topic(topic) and work_root(topic) is not None:   # the work that makes it (JL 261030)
            verbs.append(f'<a class="row-verb" data-pop="{frame.esc(title)} · work" href="{frame.esc(frame.ROUTE + "?" + urlencode({"view": "focus-part", "part": "work", "path": frame.rel(topic, root)}))}" target=_blank rel=noopener>Work</a>')
        if topic.is_dir() and is_topic(topic) and (topic / "delivery").is_dir():   # what it hands over, popped out (JL 261030)
            verbs.append(f'<a class="row-verb" data-pop="{frame.esc(title)} · delivery" href="{frame.esc(frame.ROUTE + "?" + urlencode({"view": "focus-delivery", "path": frame.rel(topic, root)}))}" target=_blank rel=noopener>Delivery</a>')
        # an interaction about this topic, beside its drawing and mind map (JL 261031: one record, many entries)
        verbs.append(interaction_button([r for r in asks if r["topic"] == topic], topic, root))
        lead, shown = frame.topic_label(topic, facts.get("at", "")) if topic.is_dir() else ("", title)
        name = (f'<a class="row-name" data-pop="{frame.esc(title)}" href="{frame.esc(url)}" target=_blank rel=noopener>'
                f'{frame.esc(shown)}</a>') if url else f'<span class="row-name">{frame.esc(shown)}</span>'
        if lead:                                             # b17.j01-s07:theme_work.tables @ one_table (s01-D03)
            name = f'<span class="row-address">{frame.esc(lead)}</span>' + name
        stage = facts.get("stage") or ""
        if stage:                                            # one word, never the four-step line
            name += f'<span class="row-stage">{frame.esc(stage)}</span>'
        if facts.get("dtype"):                               # what it hands over, beside how far it is
            name += f'<span class="row-type" title="delivery type">{frame.esc(facts["dtype"])}</span>'
        pic_url = deck_url if lead_slide and deck_url else (draw_url or url)   # the picture opens its slide
        picture = (f'<a class="row-thumb" data-pop="{frame.esc(title)}" href="{frame.esc(pic_url)}" target=_blank rel=noopener>'
                   f'<img src="{frame.esc(frame._file_url(preview, root))}" alt="{frame.esc(title)}" loading="lazy"></a>'
                   if preview and pic_url else '<span class="row-thumb none">no picture yet</span>')
        topic_line = facts.get("topic", "")                 # one line: its first sentence
        first = re.match(r"(.+?[.;])(?:\s|$)", topic_line)
        topic_line = first.group(1) if first else topic_line[:200]
        line = (f'<a data-pop="{frame.esc(title)}" href="{frame.esc(url)}" target=_blank rel=noopener>{frame.esc(topic_line)}</a>'
                if url else frame.esc(topic_line))
        out.append(f'<article class="status-row studio-row" id="{frame.esc(topic.name)}"><div><p class="row-title">{name}</p>'
                   + (f'<p class="row-line">{line}</p>' if topic_line else '')
                   + (f'<p class="row-verbs">{"".join(verbs)}</p>' if verbs else '') + f'</div>{picture}</article>')
    return "".join(out) or '<p class="mut">No Studio topics in this section.</p>'


def log_events(text: str) -> list:
    """Only dates written in the current face's Log, never file modification times."""
    events = []
    for line in text.splitlines():
        match = re.match(r"^\s*(?:[-*]\s+)?(\d{4}-\d{2}-\d{2}|\d{6})(?:\s+(\d{4}))?\s*[·:–-]\s*(.+)", line)
        if not match:
            continue
        raw, time, message = match.groups()
        day = f"20{raw[:2]}-{raw[2:4]}-{raw[4:]}" if len(raw) == 6 else raw
        try:
            dt.date.fromisoformat(day)
        except ValueError:
            continue
        events.append((day, time or "", message))
    return sorted(events, key=lambda e: (e[0], e[1]))


TIMELINE_MAX = 120


def timeline_events(folder: Path, root: Path, git: bool = True) -> list:
    """What happened when, newest first, from records that already carry a date (JL 261028: a view, never a
    timeline folder): the git commits that touched this folder, each Run's passes and receipt below it, and any
    dated `## Log` line of a face. Each event: (day, kind, words, origin)."""
    events = []
    try:
        if not git:                                  # the caller reads git once for many folders (project_branches)
            raise OSError
        out = subprocess.run(["git", "-C", str(folder), "log", f"-{TIMELINE_MAX}", "--format=%cs%x09%s", "--", "."],
                             capture_output=True, text=True, timeout=5)
        for line in out.stdout.splitlines() if out.returncode == 0 else []:
            day, _, words = line.partition("\t")
            events.append((day, "commit", words, ""))
    except (OSError, subprocess.TimeoutExpired):
        pass
    for source in rollup(folder):
        where = origin(source, folder)
        for day, _, message in log_events(read_face(source, root)["sections"].get("log", "")):
            events.append((day, "log", message, where))
        for run in frame.runs_of(source) if (source / "runs").is_dir() else []:
            path = run["path"]
            if not path.is_dir() or not inside(path, root):
                continue
            receipt = path / "result" / "runtime.yaml"
            text = receipt.read_text(encoding="utf-8", errors="ignore") if receipt.is_file() else ""
            done = re.search(r"(?m)^finished_at:\s*'?(\d{4}-\d{2}-\d{2})", text)
            status = re.search(r"(?m)^status:\s*(\S+)", text)
            if done:
                events.append((done.group(1), "run", f"{run['run']} {status.group(1) if status else 'finished'}", where))
            for pdir in sorted((path / "passes").glob("p[0-9]*-[0-9][0-9][0-9][0-9]")) if (path / "passes").is_dir() else []:
                mmdd = pdir.name.split("-")[-1]
                year = (done.group(1)[:4] if done else str(dt.date.today().year))
                note = pdir / "pass.md"                  # what the pass did: its own title line
                title = next((l[2:].strip() for l in note.read_text(encoding="utf-8", errors="ignore").splitlines()
                              if l.startswith("# ")), "") if note.is_file() else ""
                events.append((f"{year}-{mmdd[:2]}-{mmdd[2:]}", "pass",
                               (f"{title} ({run['run']}, {pdir.name.split('-')[0]})" if title else f"{run['run']} · {pdir.name}"), where))
    events.sort(key=lambda e: e[0], reverse=True)
    return events[:TIMELINE_MAX]


KIND_WORDS = {"commit": ("change", "changes"), "run": ("Run finished", "Runs finished"), "pass": ("work session", "work sessions"),
              "log": ("log note", "log notes")}


def kind_count(kinds) -> str:
    """`commit, commit, run` -> `2 changes · 1 Run finished`."""
    from collections import Counter as _C
    c = _C(kinds)
    return " · ".join(f"{n} {KIND_WORDS.get(k, (k, k))[0 if n == 1 else 1]}" for k, n in c.most_common())


def timeline_html(events: list, folder: Path, root: Path) -> str:
    """What was done, newest day first (JL 261029: "there should be something to describe what we have done"): a
    summary of the whole span, then one block per day that says what that day did, then its events in words."""
    if not events:
        return '<p class="mut">Nothing dated below this page yet.</p>'
    days = {}
    for e in events:
        days.setdefault(e[0], []).append(e)
    busiest = sorted(days.items(), key=lambda kv: -len(kv[1]))[:3]
    summary = ('<div class="tl-summary"><p><b>' + frame.esc(kind_count(e[1] for e in events)) + '</b> between '
               + frame.esc(min(days)) + ' and ' + frame.esc(max(days)) + ', on ' + str(len(days)) + ' days.</p>'
               '<p class="mut">Busiest: ' + " · ".join(f"{frame.esc(d)} ({len(es)})" for d, es in busiest) + '</p></div>')
    blocks = []
    for day in sorted(days, reverse=True):
        items = days[day]
        commits = [w for _, k, w, _ in items if k == "commit"]
        lead = commits[0] if commits else items[0][2]          # the day's headline: its first change, else its first event
        rows = "".join(f'<li><span class="tl-kind">{frame.esc(KIND_WORDS.get(k, (k, k))[0])}</span> {frame.esc(w)}'
                       + (f' <span class="tl-where">· {frame.esc(where)}</span>' if where else '') + '</li>'
                       for _, k, w, where in items)
        blocks.append(f'<section class="tl-day" data-day="{frame.esc(day)}"><header><time>{frame.esc(day)}</time>'
                      f'<span class="tl-lead">{frame.esc(lead)}</span><span class="tl-n">{frame.esc(kind_count(k for _, k, _, _ in items))}</span>'
                      f'</header><ul>{rows}</ul></section>')
    return (summary + '<div class="date-range"><label>From <input type="date" data-from></label>'
            '<label>To <input type="date" data-to></label></div><p data-date-message role="status"></p>'
            '<div class="tl-days">' + "".join(blocks) + '</div>')


def folder_html(folder, root, seen=(), depth=0):
    """Show two levels directly; deeper folders link to their own folder page."""
    if not inside(folder, root) or folder.resolve() in seen:
        return ""
    children = sorted(p for p in folder.iterdir() if p.is_dir() and not p.name.startswith(".") and inside(p, root))
    rows = []
    for child in children:
        if depth < 1:
            rows.append(f'<li><span>{frame.esc(child.name)}/</span>'
                        f'{folder_html(child, root, (*seen, folder.resolve()), depth + 1)}</li>')
        else:
            rows.append(f'<li><a href="{frame.esc(page_url(child, root, "folders"))}">{frame.esc(child.name)}/</a></li>')
    return '<ul class="focus-folders">' + "".join(rows) + '</ul>' if rows else '<p class="mut">No subfolders.</p>'


def related_html(folder: Path, root: Path) -> str:
    """What came in from outside (haipipe-related): the folder's related/related.md table, or its files."""
    rel = folder / "related"
    if not rel.is_dir() or not inside(rel, root):
        return ""
    table = rel / "related.md"
    if table.is_file():
        return markdown(table.read_text(encoding="utf-8", errors="replace"), rel, root)
    files = sorted(q for q in rel.rglob("*") if q.is_file() and not q.name.startswith("."))
    return "<ul>" + "".join(f'<li><a href="{frame.esc(frame._file_url(q, root))}" target=_blank rel=noopener>'
                            f'{frame.esc(q.relative_to(rel).as_posix())}</a></li>' for q in files) + "</ul>" if files else ""
