"""The focus page's Findings sections: findings, values, displays, maps and design drawings."""
from __future__ import annotations

import datetime as dt
import json
import re
import traceback
from pathlib import Path
from urllib.parse import urlencode

from live import frame, task_questions
from live.ui_parts import PB_CSS, PB_JS, _side_tabs
from live.focus_base import (band_title, inside, page_level, page_module, page_title, page_url, read_face,
    report_path, state_label, state_words)
from live.focus_styles_bands import BAND_CSS, DESIGN_JS, FINDINGS_CSS, FIT_FRAME_JS, band_sec, numbered, side_css
from live.focus_runs import headline_section, mark_word, output_run, run_files, run_headline, table_section
from live.focus_reports import first_answer
from live.focus_delivery import own_delivery_tabs, service_section


FOUND_STAGE = {"agreed": "answered", "partial": "partly answered", "proposed": "proposed, waiting for you", "draft": "draft", "": "no answer yet"}


def task_reading(folder: Path, root: Path) -> str:
    """The first thing a Task's or Job's own reading of its results says: the first line of its `## Content` that holds
    a result, without the line naming the Run; empty when it has written none."""
    body = re.sub(r"<!--.*?-->", "", read_face(folder, root)["sections"].get("content", ""), flags=re.S)
    for raw in body.splitlines():
        line = re.sub(r"\s+", " ", re.sub(r"\*\*|`|^\s*(?:[-*]|\d+\.)\s+|^#+\s+", "", raw)).strip()
        if line and not line.startswith(("|", "[", "!", "Reading of run")):
            return line
    return ""


def work_paths(row: dict, folder: Path, root: Path) -> list:
    """The folders a Question names under `work:`."""
    out = []
    for item in row.get("work") if isinstance(row.get("work"), list) else []:
        ref = item if isinstance(item, str) else task_questions.words(item.get("path")) if isinstance(item, dict) else ""
        path = (folder / ref).resolve() if ref else None
        if path and path.is_file():                  # a file names its folder's work (hai-cowork: `work:` names files)
            path = path.parent
        if path and inside(path, root) and path.is_dir() and path not in out:
            out.append(path)
    return out


def answer_state(path, qid: str = "") -> tuple:
    """(stage, sentence) of a report's answer: its own lead first (agreed, proposed), else its `answer-status:` field,
    so an answer with no lead reads "answered" or "partly answered" and not "draft"."""
    stage, answer = first_answer(path, qid) if path else ("", "")
    if stage == "draft":
        status = (task_questions.field(path.read_text(encoding="utf-8", errors="replace"), "answer-status") or "").lower()
        stage = "agreed" if status == "answered" else "partial" if status.startswith("partial") else stage
    return stage, answer


def finding_item(row: dict, folder: Path, root: Path) -> tuple:
    """(tab name, its line, its panel, stage) of one Question: on the left its name and answer state; on the right what
    it asks, its answer's words, then what its work has found."""
    path = report_path(row, folder, root)
    stage, answer = answer_state(path, str(row.get("id") or ""))
    title = task_questions.words(row.get("title")) or task_questions.words(row.get("question"))
    asked = task_questions.words(row.get("question"))
    results = []
    for w in work_paths(row, folder, root):
        said = task_reading(w, root)
        if said:
            where = f"{w.parent.name}/{w.name}" if page_level(w) == "Task" else w.name   # on hover, no "j02 · t01" (round 3)
            results.append(f'<li><a href="{frame.esc(page_url(w, root))}" data-pop="{frame.esc(w.name)}" title="{frame.esc(where)}">'
                           f'{frame.esc(page_title(w))}</a>: {frame.esc(said)}</li>')   # its title first
    word = FOUND_STAGE.get(stage, stage)
    html = (f'<div class=find-h><b>{frame.esc(title)}</b><span class="find-pill {stage}">{frame.esc(word)}</span>'
            + (f'<span class=find-open>{frame.pop(frame.reader(path, root), title, "Read full report ↗")}</span>' if path else '') + '</div>')
    if asked and asked != title:
        html += f'<p class=find-ask>{frame.esc(asked)}</p>'
    if answer:
        html += f'<p class=find-a>{frame.esc(answer)}</p>'
    if results:
        html += '<h4 class=find-sub>What its work found</h4><ul class=find-r>' + "".join(results[:8]) + '</ul>'
    if results[8:]:
        html += (f'<details class=find-more><summary>{len(results) - 8} more</summary><ul class=find-r>' + "".join(results[8:]) + '</ul></details>')
    if not answer and not results:
        html += '<p class="find-a mut">Nothing read from its work yet.</p>'
    return title, word, html, stage


def value_sections(folder: Path, root: Path) -> list:
    """[(title, html, state word)] of the raw tables of a Block's Jobs that hold a tables.json: the paper's Values tabs, the same code."""
    try:
        from live import board_evidence as be
    except Exception:
        traceback.print_exc()   # in the server log, not hidden (code review 261113)
        return []
    out = []
    level = page_level(folder)                       # a Block's Jobs, or the one Job (its own page or a Task's)
    jobs = [j for j in frame.children(folder, "Block") if inside(j, root)] if level == "Block" else [folder] if level == "Job" else []
    for k, job in enumerate(j for j in jobs if next(j.glob("t[0-9]*_*/runs/r[0-9]*/result/tables.json"), None)):
        try:
            tabs = be.value_tabs(job, root)
        except Exception:
            continue
        if tabs:
            opens = f'<div class=find-verbs>{frame._link(page_url(job, root), "Open " + job.name)}</div>' if level == "Block" else ""
            out.append(("🗂️ Data", opens + be.VALUES_CSS
                        + _side_tabs(f"fV{k}x", [(h, w) for h, w, _ in tabs], [p for _, _, p in tabs],
                                     cards=(job, root, "findings.values")) + be.VALUES_DIALOG + be.VALUES_JS,
                        be.values_word(job, root)))
    return out


def display_sections(folder: Path, root: Path) -> list:
    """[(title, html, state word)] of the display Tasks at this page or below (face `task-type: display`; JL 261109:
    "where is the displays???"), drawn by the paper's own Displays code (workbench-paper board_results.display_tabs; JL
    261109: "consistent with the paper theme"): the same side tabs in groups, the same shown version (the face's
    `printed:` Run, else the newest preview.pdf), the same facts and Open button. A work Block prints nowhere, so the
    paper's Main reads Results and its Method reads Methods. Shown after the Values, before the Questions."""
    try:
        from live.board_results import display_tabs
    except Exception:
        traceback.print_exc()   # in the server log, not hidden (code review 261113)
        return []
    level = page_level(folder)
    tasks = ([t for j in frame.children(folder, "Block") if inside(j, root) for t in frame.children(j, "Job") if inside(t, root)]
             if level == "Block" else [t for t in frame.children(folder, "Job") if inside(t, root)] if level == "Job"
             else [folder] if level == "Task" else [])
    shown = []
    for t in tasks:
        face = t / f"{t.name}.md"
        if face.is_file() and re.search(r"(?m)^task-type:\s*display\b", face.read_text(encoding="utf-8", errors="replace")):
            shown.append(t)
    try:
        html, word = display_tabs(shown, root, eid="fDisp" + folder.name[:3] + "x", names={"main": "Results", "method": "Methods"})
    except Exception:
        traceback.print_exc()   # in the server log, not hidden (code review 261113)
        return []
    return [("🖼️ Displays", html, word)] if html else []


def design_sections(folder: Path, root: Path) -> list:
    """[(title, html, state word)] of a Block's Jobs that have a design to read (JL 261109: "for each of the event type,
    it should show the section, and each section should be left tab right content about the workflow and the structure
    ... for each event, we should have the two studio and one website"): one section a Job, a side tab per Studio topic
    hung at it (its face's **At:**), the topic's drawing on the right, then a side tab per live page of the Job (a
    deliverable with a `url:`), the site itself, working, loaded when its tab first shows."""
    if page_level(folder) != "Block":
        return []
    out = []
    pages = frame._live_pages(folder)
    for k, job in enumerate(j for j in frame.children(folder, "Block") if inside(j, root)):
        topics = [(t, d) for _, t, d in frame._hung_here(job, root, set()) if t.is_dir() and inside(t, root)]
        sites = [i for i in pages if i["folder"] == job or job in Path(i["folder"]).parents]
        if not topics:                               # a Job with a website only is 🌐 Service's
            continue
        tabs, panels = [], []
        for topic, drawings in sorted(topics, key=lambda x: x[0].name):
            notes = frame._notes(topic)
            head = notes.read_text(encoding="utf-8", errors="replace").splitlines()[0] if notes else topic.name
            name, _, words_ = head.partition(" · ")
            png = topic / f"{topic.name}.png"
            mind = topic / f"{topic.name}.mindmap.md"
            open_ = frame.ROUTE + "?" + urlencode({"path": frame.rel(folder, root), "layout": "focus", "section": "studio"}) \
                + "#" + frame.studio_anchor(topic, folder, folder)
            verbs = [f'<a href="{frame.esc(open_)}">Open the topic</a>']
            if png.is_file():
                verbs.append(frame.pop("/" + frame.rel(png, root), words_ or topic.name, "Enlarge drawing ↗"))
            if mind.is_file():
                verbs.append(frame.pop(frame.ROUTE + "?" + urlencode({"view": "focus-map", "path": frame.rel(mind, root)}),
                                       (words_ or topic.name) + " · mind map", "Mind map ↗"))
            # the whole drawing, live, every frame of it (JL 261109: "make the preview here to be the full preview"): the
            # topic's .png is only its row's small picture, cut to its first part
            main = next((d for d in drawings if d.name == topic.name + ".excalidraw"), drawings[0] if drawings else None)
            if main is not None and inside(main, root):
                verbs.insert(1, frame.pop(frame._draw_url(main, root), words_ or topic.name, "Enlarge drawing ↗"))
                verbs = [v for v in verbs if "/" + frame.rel(png, root) not in v]
                picture = (f'<iframe class=find-draw title="{frame.esc(words_ or topic.name)}" data-src="{frame.esc(frame._draw_url(main, root))}" '
                           f'style="width:100%;height:80vh;border:1px solid var(--line,#ddd);border-radius:6px"></iframe>')
            else:
                picture = (f'<img class=find-drawing loading=lazy alt="{frame.esc(words_ or topic.name)}" '
                           f'src="/{frame.esc(frame.rel(png, root))}">' if png.is_file() else "<p class=mute>No drawing yet.</p>")
            tabs.append((name.strip() or topic.name[:3], words_.strip()))
            panels.append(f'<div class=find-verbs>{" · ".join(verbs)}</div>{picture}')
        for i in sites:
            href = frame.live_url(i, root)
            url, name = frame.esc(href), frame.esc(i["service"])
            site = (f'<iframe title="{name}" data-src="{url}" referrerpolicy=no-referrer '
                    f'style="width:100%;height:80vh;border:1px solid var(--line,#ddd);border-radius:6px"></iframe>'
                    if href.startswith("/") else "")
            tabs.append(("🌐 Website", i["title"]))
            panels.append(f'<div class=find-verbs><a href="{url}" target=_blank rel=noopener>Own tab ↗</a></div>{site}')
        jface = job / f"{job.name}.md"
        emoji = (re.search(r"(?m)^emoji:\s*(\S+)", jface.read_text(encoding="utf-8", errors="ignore")) or [None, "🧩"])[1] if jface.is_file() else "🧩"
        word = f'{len(topics)} topic{"s" * (len(topics) != 1)}' + (" · website" if sites else " · no website")
        # the Job's name as its face's title says it (j01's folder is still j01_ext_food, its title "ext meal": JL
        # 261110, "this should be meal"); the folder's words when the face has no title
        head = jface.read_text(encoding="utf-8", errors="ignore").splitlines()[0] if jface.is_file() else ""
        shown = head.partition(" · ")[2].strip() if head.startswith("# ") else ""
        out.append((f'{emoji} {shown or job.name.split("_", 1)[-1].replace("_", " ")}',
                    f'<div class=find-design>{_side_tabs(f"fE{k}x", tabs, panels, cards=(job, root, "findings.design"))}</div>', word))
    if out:
        out[-1] = (out[-1][0], out[-1][1] + DESIGN_JS, out[-1][2])
    return out


def map_sections(folder: Path, root: Path) -> list:
    """[(title, html, state word)] of the mind maps a Task's newest Run built in result/maps/ (JL 261104: "for each type of Source Table
    Name, we should have the mindmap of them"), one side tab per map, in the order of the Task's Values tabs when it has
    them. Each map is its own framed page, loaded when its tab first shows, its nodes closed."""
    out = []
    level = page_level(folder)                       # a Block's Tasks, a Job's, or the one Task
    tasks = ([t for j in frame.children(folder, "Block") if inside(j, root) for t in frame.children(j, "Job") if inside(t, root)]
             if level == "Block" else [t for t in frame.children(folder, "Job") if inside(t, root)] if level == "Job"
             else [folder] if level == "Task" else [])
    for k, task in enumerate(tasks):
        found = sorted(task.glob("runs/*/result/maps"))
        maps = sorted(found[-1].glob("*.mindmap.md")) if found else []
        if not maps:
            continue
        order = []
        for tables in reversed(sorted(task.glob("runs/*/result/tables.json"))):
            try:
                order = [t.get("title") for t in json.loads(tables.read_text(encoding="utf-8"))["tabs"]]
            except (ValueError, KeyError, AttributeError):
                continue
            break
        name = lambda m: m.name[: -len(".mindmap.md")]
        maps.sort(key=lambda m: order.index(name(m)) if name(m) in order else len(order))
        tabs, panels = [], []
        for m in maps:
            href = frame.ROUTE + "?" + urlencode({"path": frame.rel(m, root), "view": "focus-map"})
            # no cut grey line under its tab: the map's root says it whole (round 3); the frame is as tall as the map
            # in it, and grows as a card opens (round 3: "~350 px blank")
            tabs.append((name(m), ""))
            panels.append(f'<div class=find-verbs>{frame.pop(href, name(m) + " · mind map", "Enlarge map ↗")}</div>'
                          + f'<iframe class=find-map loading=lazy title="{frame.esc(name(m))} mind map" src="{frame.esc(href)}&amp;fit=1" '
                          'onload="window.fitMap&&fitMap(this)"></iframe>')
        built = dt.datetime.fromtimestamp(max(m.stat().st_mtime for m in maps)).strftime("%Y-%m-%d")
        out.append(("🧠 Maps", _side_tabs(f"fM{k}x", tabs, panels, cards=(task, root, "findings.maps")) + FIT_FRAME_JS, f"built {built}"))
    return out


def findings_board(rows: list, folder: Path, root: Path, lead: str = "", extra=(), include_delivery=True, questions=True) -> str:
    """A Block's Findings: a quick overview of the results it got and what it hands over (JL 261104: "the quick overview
    of the results we get from that block"; "we want things like this, left tab panel right content"; Delivery folded
    in), shaped like a paper Board's Evidence: numbered closed sections, each a side tab per item. Values first, then the
    Questions by their `group:` (one section when they have fewer than two groups), then 🌐 Service when it has a live
    page, then 🧠 Maps, then 📦 Delivery."""
    groups = {}
    for row in rows:
        groups.setdefault(task_questions.words(row.get("group")) or "Other", []).append(row)
    if len(groups) < 2:
        groups = {"Answers": rows} if rows else {}
    # Data, then Displays, then Maps (JL 261109: "we must first to have the Data, and the have the display, and then
    # Maps"); anything else after them, each its own numbered section, as Plan + Results adds a Job type
    secs = [(title, word, body, "") for title, body, word in value_sections(folder, root)]
    secs += [(title, word, body, "") for title, body, word in display_sections(folder, root)]
    secs += [(title, word, body, "") for title, body, word in map_sections(folder, root)]
    secs += [(title, word, body, "") for title, body, word in design_sections(folder, root)]   # a Job's design: its topics, its website
    if not questions:                            # a work Block's Findings has no ❓ question sections (JL 261109)
        groups = {}
    for g, (name, members) in enumerate(groups.items()):
        items = [finding_item(r, folder, root) for r in members]
        stages = [x[3] for x in items]
        word = ("answered" if all(x == "agreed" for x in stages) else "no answer yet" if not any(stages)
                else "waits for you" if "proposed" in stages else "partly")
        # the question whose answer waits for your agreement, under the closed bar (JL 261106)
        waits = next((f"🙋 {x[0]}: its answer waits for your agreement" for x in items if x[3] == "proposed"), "")
        title = band_title(name) if not name[:1].isalnum() else "❓ " + band_title(name)   # every bar its emoji (round 2)
        secs.append((title, word, _side_tabs(f"fQ{g}x", [(x[0], x[1]) for x in items], [x[2] for x in items],
                                                cards=(folder, root, "findings.questions")), waits))
    service = service_section(folder, root)
    if service and include_delivery:
        secs.append(("🌐 Service", "live", service, ""))
    secs += list(extra)                          # a work-shaped theme's own parts (theme_parts), before 📦 Delivery
    if include_delivery:
        tabs = own_delivery_tabs(frame.theme_of(folder, root), folder, root, "Block")
        secs.append(("📦 Delivery", "ready" if any(t[1] == "ready" for t in tabs) else "nothing yet" if all(
                     t[1] == "nothing yet" for t in tabs) else tabs[0][1], _side_tabs("fDx", [(t[0], t[1]) for t in tabs], [t[2] for t in tabs]), ""))
    try:
        from live.board_views import SIDE_CSS
    except Exception:
        SIDE_CSS = ""
    return (BAND_CSS + FINDINGS_CSS + PB_CSS + SIDE_CSS + lead + "".join(
        band_sec(n, frame.esc(title), word, body, waits) for n, (title, word, body, waits) in enumerate(secs, 1)) + PB_JS)


def task_values(task: Path, root: Path) -> list:
    """[(title, html, word)] of the Values tabs a Task's own newest Run built (its tables.json), the Block's code."""
    found = sorted(task.parent.glob("t[0-9]*_*/runs/r[0-9]*/result/tables.json"))
    if not found or task not in found[-1].parents:
        return []
    return value_sections(task.parent, root)


def output_sections(task: Path, root: Path) -> list:
    """[(title, word, body, waits)] of what a Task's newest Run returned: its headline, its Values (a tables.json) or
    else its tables (result/*.csv), its maps (result/maps/)."""
    secs = []                                    # Data, Displays, Maps, as the Block and the Job (JL 261109), then
    values = task_values(task, root)             # its headline after them
    run = output_run(task)
    if values:
        secs += [(t, w, h, "") for t, h, w in values]
    elif run is not None and (tables := table_section(run, root)):
        secs.append(("🗂️ Data", tables[2], tables[1], ""))
    secs += [(t, w, h, "") for t, h, w in display_sections(task, root)]
    secs += [(t, w, h, "") for t, h, w in map_sections(task, root)]
    head = headline_section(task, root)
    return secs + ([head + ("",)] if head else [])


def display_rows(block: Path, root: Path) -> list:
    """[(Task, its display name, its state)] of a Block's display Tasks, named as its Findings' Displays tabs name them
    (workbench-paper board_results: `label:` M1, Table 1, Figure 1 …)."""
    try:
        from live.board_results import evidence_body, _display_head, _cap, GROUP_ORDER
    except Exception:
        traceback.print_exc()   # in the server log, not hidden (code review 261113)
        return []
    out = []
    for j in (frame.children(block, "Block") if page_level(block) == "Block" else [block]):
        for t in frame.children(j, "Job") if inside(j, root) else []:
            face = t / f"{t.name}.md"
            if not (inside(t, root) and face.is_file() and re.search(r"(?m)^task-type:\s*display\b",
                                                                     face.read_text(encoding="utf-8", errors="replace"))):
                continue
            try:
                label, status, _ = evidence_body(t, root)
                words = re.sub(r"^t\d+_", "", t.name).replace("-", " ").replace("_", " ")
                words = re.sub(r"^(?:e?figure|e?table|values|cite)\d*\s*", "", words, flags=re.I)
                group, order, head, line = _display_head(t, label, label or _cap(words), words)
                key = (GROUP_ORDER.index(group) if group in GROUP_ORDER else len(GROUP_ORDER), order)
            except Exception:
                head, status, line, key = t.name, "", "", (99, 999)
            out.append((key, t, re.sub(r"<[^>]+>", "", str(head)), re.sub(r"<[^>]+>", "", str(status or line or ""))))
    # the same groups and order as the Block's own Displays tabs (display_tabs: Results, then Methods)
    return [(t, head, word) for _, t, head, word in sorted(out, key=lambda x: x[0])]


def job_findings(job: Path, root: Path, extra=(), include_delivery=True) -> str:
    """A work Job's Findings (round 2, 261106: "move the Block's Findings view down to the Job"): each Task's newest Run
    headline as a side tab, the Values its Tasks built, their maps, and what it hands over."""
    tasks = [t for t in frame.children(job, "Job") if inside(t, root)]
    secs = []
    proto = page_module(frame.theme_of(job, root), job, root)[1] == "prototype_"   # a release returns no Run headline
    if tasks and not proto:
        items, panels, returned = [], [], 0
        mod, prefix = page_module(frame.theme_of(job, root), job, root)   # a theme's own Task headline (a discovery
        own_head = getattr(mod, prefix + "headline", None) if mod is not None else None   # Task leads with its synthesis)
        for t in tasks:
            run = output_run(t)
            try:
                head = (own_head(t, root) if own_head else "") or (run_headline(run) if run else "")
            except Exception:
                head = run_headline(run) if run else ""
            label = state_label(read_face(t, root)["state"])
            returned += run is not None
            items.append((page_title(t), mark_word(state_words(label)) if label else ""))
            panels.append((f'<p class=pb-big>{frame.esc(head)}</p>' if head else '')
                          + f'<div class=find-verbs>{frame.pop(page_url(t, root), t.name, "Open " + t.name + " ↗")}</div>'
                          + (run_files(run, root) if run else ""))
        heads = [("📌 Headlines", "returned" if returned == len(tasks) else "partly returned" if returned else "nothing returned yet", _side_tabs("fH" + job.name[:3] + "x", items, panels), "")]
    else:
        heads = []
    # Data, Displays, Maps first, as the Block's (JL 261109); the Tasks' headlines after them
    secs += [(t, w, h, "") for t, h, w in value_sections(job, root)]
    secs += [(t, w, h, "") for t, h, w in display_sections(job, root)]
    secs += [(t, w, h, "") for t, h, w in map_sections(job, root)]
    secs += heads
    secs += list(extra)                          # a work-shaped theme's own parts (theme_parts), before 📦 Delivery
    if include_delivery:
        tabs = own_delivery_tabs(frame.theme_of(job, root), job, root, "Job")
        secs.append(("📦 Delivery", "ready" if any(t[1] == "ready" for t in tabs) else "nothing yet" if all(
                     t[1] == "nothing yet" for t in tabs) else tabs[0][1],
                     _side_tabs("fDx", [(t[0], t[1]) for t in tabs], [t[2] for t in tabs]), ""))
    return side_css() + numbered([(frame.esc(s[0]),) + tuple(s[1:]) for s in secs]) + PB_JS
