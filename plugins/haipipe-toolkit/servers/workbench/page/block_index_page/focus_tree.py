"""The focus page's Progress tree: a page's kids, Task families folded, Runs under their Task."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlencode

import yaml

from live import frame
from live import focus_interactions
from live.ui_parts import state_mark
from live.focus_base import (inside, kids, one_line, page_level, page_url, read_face, state_label,
    state_words, task_tally, topic_home)
from live.focus_styles_bands import FOLD_CSS
from live.ladder_cards import row_cards
from live.focus_runs import run_rows, run_url
from live.focus_interactions import interaction_button
from live.focus_reports import question_cards


def output_of(holder: Path, root: Path) -> str:
    """The newest Run's figure with its question and headline, shown in place. `holder` is a Task (its
    runs/*/result) or one Run folder (its result)."""
    results = [holder / "result"] if (holder / "result").is_dir() else sorted(holder.glob("runs/*/result"))
    for result in reversed(results):
        picture = next((p for p in (result / "figure.png", result / "preview.png") if p.is_file()), None)
        if not picture or not inside(picture, root):
            continue
        display = {}
        if (result / "display.yaml").is_file():
            try:
                display = yaml.safe_load((result / "display.yaml").read_text(encoding="utf-8")) or {}
            except yaml.YAMLError:
                display = {}
        head = (result / "headline.txt").read_text(encoding="utf-8").strip() if (result / "headline.txt").is_file() else ""
        url = frame._file_url(picture, root)
        question = display.get("question") if isinstance(display, dict) else ""
        return (f'<figure class="row-output"><a data-pop="{frame.esc(result.parent.name)}" href="{frame.esc(url)}"'
                f' target=_blank rel=noopener><img src="{frame.esc(url)}" alt="{frame.esc(result.parent.name)}"'
                ' loading="lazy"></a><figcaption>'
                + (f'<p>{frame.esc(question)}</p>' if question else '')
                + (f'<p class="mut">{frame.esc(head[:400])}</p>' if head else '')
                + f'<p class="mut">Run {frame.esc(result.parent.name)}</p></figcaption></figure>')
    return ""


def picture_of(folder: Path, root: Path) -> Path | None:
    """The page's own picture: the first topic preview it has (s00-overview retired 261029: the Report MindMap
    shows the Block). A Block whose topics sit beside its Jobs (b35-s01-D12) shows its first Job topic's."""
    for _, topic, _ in frame.studio_inventory(folder, root):
        for png in (topic / f"{topic.name}.png",):
            if png.is_file() and inside(png, root):
                return png
    return None


def kid_row(child: Path, root: Path) -> str:
    """One child as one scannable row (hai-ui, JL 261029: "make it the award level UI"): its real name, one line
    of what it is, its buttons and its picture; no count pills (JL 261030: "why we have this? I don't think we need
    these?": labels carry no counts, and where a child stands is on its own page)."""
    data = read_face(child, root)
    face = data.get("face")
    line = one_line(data["goal"]) or (frame._title(face) if face and inside(face, root) else "")
    pic = picture_of(child, root)
    picture = (f'<img class="kid-pic" src="{frame.esc(frame._file_url(pic, root))}" alt="" loading="lazy">'
               if pic else '<span class="kid-pic none" aria-hidden="true"></span>')
    url = frame.esc(page_url(child, root))
    return (f'<div class="kid-row"><span class="kid-text"><a class="kid-name" href="{url}">{frame.esc(child.name)}</a>'
            + (f'<a class="kid-line" href="{url}">{frame.esc(line)}</a>' if line else '')
            + f'<span class="row-verbs">{"".join(part_verbs(child, root, pic))}</span>'
            + f'</span><a href="{url}" aria-hidden="true" tabindex="-1">{picture}</a></div>')


# A row's buttons, each popped out over the page like an sNN card's (JL 261030: "please create the draw, mind map and
# delivery for them"; "we can also add the job-task-run to it, to show the structure content"): its drawing, its
# mind map, its structure down to the Runs, and its delivery.
PARTS = (("map", "Mind map"), ("work", "Work"), ("delivery", "Delivery"))   # Work: its Jobs, Tasks and Runs


def part_verbs(folder: Path, root: Path, pic: Path | None = None) -> list:
    out = []
    drawing = pic.with_suffix(".excalidraw") if pic else None
    if drawing and drawing.is_file() and inside(drawing, root):
        out.append(f'<a class="row-verb" data-pop="{frame.esc(folder.name)} · drawing" '
                   f'href="{frame.esc(frame._draw_url(drawing, root))}" target=_blank rel=noopener>Draw</a>')
    for key, name in PARTS:
        if key == "work" and work_root(folder) is None:
            continue
        href = frame.ROUTE + "?" + urlencode({"view": "focus-part", "part": key, "path": frame.rel(folder, root)})
        out.append(f'<a class="row-verb" data-pop="{frame.esc(folder.name)} · {frame.esc(name)}" '
                   f'href="{frame.esc(href)}" target=_blank rel=noopener>{frame.esc(name)}</a>')
    return out


def work_root(folder: Path) -> Path | None:
    """What its Work tree (Jobs, Tasks, Runs) starts from: a Block or a Job itself, a Project's work/ world; an sNN's,
    the work that makes its delivery (JL 261030: "could we add the work, (which are the jobs-task)"): the Job its
    render.yaml names as a builder (`by:`), else the Job it sits in; none yet for a Block's sNN that names none."""
    level = page_level(folder)
    if level == "Topic":
        owner = frame.topic_owner(folder)
        card = folder / "delivery" / "render.yaml"
        named = re.findall(r"(?m)^\s*by:\s*['\"]?(j\d+_[^/\s'\"]+)", card.read_text(encoding="utf-8", errors="ignore")) \
            if card.is_file() else []
        for name in named:
            if (owner / name).is_dir():
                return owner / name
        if frame.level_of(owner) == "Task":
            return owner.parent
        return owner if frame.level_of(owner) == "Job" else None   # a Block's sNN with no Job of its own: no Job yet
    if level in ("Block", "Job"):
        return folder
    if level == "Project" and (folder / "work").is_dir():
        return folder / "work"
    if level == "Theme" and folder.name == "work":
        return folder
    return None


def kid_group(name: str, href: str, rows: list) -> str:
    return (f'<section class="kid-group"><h3 class="kid-head"><a href="{frame.esc(href)}">{frame.esc(name)}</a>'
            '</h3>' + "".join(rows) + '</section>')        # no count: the rows show how many (AGENTS.md Page words)


FAMILY_MIN = 4                                       # four or more same-shaped Tasks fold into one line


def task_families(tasks: list) -> list:
    """A Job's Tasks in families (JL 261103: "walk this block, I still feel it is very hard to read"): Tasks named
    alike but for a last value (t11_train_numeric_1m … t22_train_numeric_1b) are one family, keyed by the shared middle
    ("train_numeric") with its values ("1m" … "1b"); others stand alone. Returns [(key or None, [tasks], [values])],
    in folder order."""
    keyed = []
    for t in tasks:
        m = re.match(r"t\d+_(.+)_([0-9][0-9.]*[a-z]*)$", t.name)
        keyed.append((m.group(1), m.group(2)) if m else (None, None))
    count = {}
    for k, _ in keyed:
        if k:
            count[k] = count.get(k, 0) + 1
    out, seen = [], {}
    for t, (k, v) in zip(tasks, keyed):
        if k and count[k] >= FAMILY_MIN:
            if k not in seen:
                seen[k] = len(out)
                out.append((k, [], []))
            out[seen[k]][1].append(t)
            out[seen[k]][2].append(v)
        else:
            out.append((None, [t], []))
    return out


def family_words(key: str, tasks: list, values: list) -> tuple:
    """A family's name and its line: "t11–t22 train numeric", "12 Tasks, 1m to 1b"."""
    first, last = tasks[0].name.split("_")[0], tasks[-1].name.split("_")[0]
    return f"{first}–{last} {key.replace('_', ' ')}", f"{len(tasks)} Tasks, {values[0]} to {values[-1]}"


def fold_tree(folder: Path, root: Path, level: str, outputs: bool = True, only: list | None = None) -> str:
    """A Block's Jobs, or a Job's Tasks, as one folding tree down to each Task's Runs (JL 261102: "could we make it
    looks like this to be collapsable"; "we also want to see what are the runs under each task"). Each line: its
    name (opens in the pop-out, JL: "I don't want to switch but to have the pop out window first"), its state, its
    goal or, for a Run, its receipt's headline. Everything starts folded. `only` keeps the Jobs and Tasks it names (and
    what holds them), the same rows for a part of the work (a Status Topic)."""
    def kept(p: Path) -> bool:
        return only is None or any(p == o or o in p.parents or p in o.parents for o in only)

    def line(href, name, label, state, note, kids="", extra="", short_note=False, slot=""):
        row = (f'<a href="{frame.esc(href)}" data-pop="{frame.esc(label)}">{frame.esc(name)}</a>'
               + state_mark(state) + extra
               + (f'<small title="{frame.esc(note)}">{frame.esc(note)}</small>' if note and short_note else ""))
        if note and not short_note:                       # a goal sentence waits behind a hover (JL 261103: "too many words")
            row = row.replace(f'data-pop="{frame.esc(label)}"', f'data-pop="{frame.esc(label)}" title="{frame.esc(note)}"', 1)
        if not kids:
            return f'<li><div class="fold-row leaf">{row}</div>{slot}</li>'
        return f'<li><details><summary class=fold-row>{row}</summary><ul>{kids}</ul></details>{slot}</li>'

    def runs(task: Path) -> str:
        out = ""
        for r, mark, head in run_rows(task):
            strip, slot = row_cards(r, root, head or r.name)      # its marks and cards (JL 261116); its 🙋 says
            mark = "" if "~ask" in strip and "wait" in (mark or "").lower() else mark   # it waits, no words beside it
            out += line(run_url(r, root), r.name, f"{task.name} · {r.name}", mark, head, extra=strip,
                        short_note=True, slot=slot)
        return out

    def task_line(t: Path) -> str:
        d = read_face(t, root)
        out = output_of(t, root) if outputs else ""   # the Task's output, in place, first inside its fold
        kids = (f'<li class=fold-out>{out}</li>' if out else "") + runs(t)
        st = state_label(d["state"])                   # "✅ DONE" as the Jobs' "✅ done" (JL 261103)
        strip, slot = row_cards(t, root, t.name)
        return line(page_url(t, root), t.name, t.name, state_words(st) if st else "", d["goal"].split("\n")[0], kids,
                    strip, slot=slot)

    def family_lines(ts: list) -> str:
        """Same-shaped Tasks as one folded line each family (its state tally, its values), the Tasks inside it."""
        out = ""
        for key, members, values in task_families(ts):
            if key is None:
                out += task_line(members[0])
                continue
            name, words = family_words(key, members, values)
            tally = task_tally([s for s in (state_label(read_face(t, root)["state"]) for t in members) if s])
            out += (f'<li><details><summary class=fold-row><b class=fam>{frame.esc(name)}</b>'
                    + state_mark(tally)
                    + f'<small>{frame.esc(words)}</small></summary><ul>{"".join(task_line(t) for t in members)}</ul></details></li>')
        return out

    items = ""
    for child in (frame.children(folder, level) if level == "Block" else []):
        if not inside(child, root):
            continue
        d = read_face(child, root)
        if level == "Block":
            if not kept(child):
                continue
            ts = [t for t in frame.children(child, "Job") if inside(t, root) and kept(t)]
            tally = task_tally([s for s in (state_label(read_face(t, root)["state"]) for t in ts) if s])
            strip, slot = row_cards(child, root, child.name)
            items += line(page_url(child, root), child.name, child.name, tally, d["goal"].split("\n")[0],
                          family_lines(ts), strip, slot=slot)
    if level != "Block":
        items += family_lines([c for c in frame.children(folder, level) if inside(c, root) and kept(c)])
    return FOLD_CSS + f'<ul class=fold-tree>{items}</ul>' if items else ""


def status_html(folder: Path, root: Path, level: str, questions: list) -> str:
    """Goal & status: one full-width row per child (Jobs, Tasks or Runs) with its goal, its status and, for
    a Task or a Run, its output in place; then the Questions."""
    rows = []
    if level in {"SPACE", "Folder"}:              # its Projects, under each folder of Projects
        groups = [(None, kids(folder))] if level == "Folder" else [(g, kids(g) if page_level(g) == "Folder" else [g]) for g in kids(folder)]
        for group, projects in groups:
            items = [kid_row(q, root) for q in projects if inside(q, root)]
            rows.append(kid_group(group.name, page_url(group, root), items) if group is not None and page_level(group) == "Folder"
                        else "".join(items))
    elif level in {"Project", "Theme"}:          # a Project lists its Blocks under each Theme; a Theme, its Blocks
        groups = [(th, kids(th)) for th in kids(folder)] if level == "Project" else [(None, kids(folder))]
        for theme, blocks in groups:
            items = [kid_row(b, root) for b in blocks if inside(b, root)]
            rows.append(kid_group(theme.name, page_url(theme, root), items) if theme is not None else "".join(items))
    elif level in {"Block", "Job"}:
        # what this Block or Job asks itself (its own runs/rNN_collect_*), waiting or answered, first: no Job or Task row
        # holds it, so without this line Work would not show it (JL 261031: one record, an entry wherever its work is)
        for r in (r for r in focus_interactions.interactions(folder, root) if r["page"] == folder):
            about = (f' · about <a href="{frame.esc(topic_home(r["topic"], root))}">{frame.esc(r["topic"].name)}</a>'
                     if r["topic"] is not None else '')
            rows.append(f'<article class="status-row ix-row"><span class="row-name">{frame.esc(r["title"])}</span>'
                        + (f'<p class="row-line">{about[3:]}</p>' if about else '')
                        + f'<p class="row-meta">{frame.esc(r["run"])}{interaction_button([r], r["path"], root)}</p></article>')
        rows.append(fold_tree(folder, root, level))       # its Jobs, Tasks and Runs as one folding tree (JL 261102)
    elif level == "Task":
        records = {r["path"]: r for r in focus_interactions.interactions(folder, root)}
        for run in frame.runs_of(folder):
            path = run["path"]
            if not inside(path, root):
                continue
            badge = interaction_button([records[path]], path, root) if path in records else ""   # a collection Run
            name = (f'<a class="row-name" data-pop="{frame.esc(folder.name)} · {frame.esc(run["run"])}" '
                    f'href="{frame.esc(run_url(path, root))}" target=_blank rel=noopener>{frame.esc(run["run"])}</a>'
                    if path.is_dir() else f'<span class="row-name">{frame.esc(run["run"])}</span>')
            rows.append(f'<article class="status-row">{name}'
                        f'<p class="row-meta">{frame.esc(run["status"])}{badge}</p>'
                        + (output_of(path, root) if path.is_dir() else '') + '</article>')
    body = "".join(rows)
    if questions:
        body += '<h3 class="focus-sub">Questions</h3>' + question_cards(questions, folder, root)
    below = {"SPACE": "Projects", "Folder": "Projects", "Project": "Themes", "Theme": "Blocks", "Block": "Jobs", "Job": "Tasks",
             "Task": "Runs"}.get(level, "pages")
    return body or f'<p class="mut">No {below} yet.</p>'
