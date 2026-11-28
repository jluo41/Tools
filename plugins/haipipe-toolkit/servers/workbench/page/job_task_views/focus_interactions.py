"""The focus page's Interactions and Know: what asks the person, what they should know, where each was asked."""
from __future__ import annotations

import datetime as dt
import re
from pathlib import Path
from urllib.parse import urlencode

import yaml

from live import frame
from live.ui_parts import WORD_CSS
from live import interaction_section as IX
from live.focus_base import (face_title, inside, is_topic, kids, page_level, page_title, page_url, rollup,
    topic_home)
from live.focus_styles_bands import RAIL_IX_CSS


def interactions(folder: Path, root: Path) -> list:
    """Every interaction at this page or below, waiting ones first (hai-interaction; JL 261031: one record per
    interaction, shown by the Interactions view, the Work rows, the map and the Studio cards alike). A record is a
    collection Run, `runs/rNN_collect_<slug>/`; its state is its card's status (waiting, answered, planned), so no
    view keeps a state of its own. Answered is not applied: applying belongs to the Runs its `feeds:` names."""
    rows = [r for page in rollup(folder) for r in page_interactions(page, root)]
    order = {"waiting": 0, "planned": 1, "answered": 2}
    return sorted(rows, key=lambda r: order.get(r["state"], 1))


def card_interactions(folder: Path, root: Path) -> list:
    """The interactions a page's Studio cards can be about: those of its Block and below, so a question the Block asks
    about a Job's sNN still shows on that sNN's card on the Job page; above a Block, the page's own and below."""
    block = next((p for p in (folder, *folder.parents) if frame.level_of(p) == "Block"), folder)
    return interactions(block if inside(block, root) else folder, root)


INTERACTION_STATE = {"waiting": "waiting", "done": "answered", "complete": "answered", "planned": "planned"}


def interaction_topic(about: str, page: Path) -> Path | None:
    """The sNN an interaction is about, from the address its `for:` line starts with (`b35-s01:studio @ …`,
    `b17.j03-s02:…`): that Block among the page's folders, its Job or Task when named, and that level's sNN."""
    m = re.match(r"\s*(b\d+|(?:Paper|Grant|Insight|Design|InsightQuestionBook|QuestionBook|Prototype)-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*?)((?:\.[jt]\d+)*)-(s\d+)\b",
                 about or "")
    if not m:
        return None
    paper = not re.fullmatch(r"b\d+", m.group(1))       # a named Board (paper, insight, its Question Book, design) has no
    #                                                       bNN: its folder name is its address (261106)
    level = next((p for p in [page, *page.parents] if (p.name == m.group(1) if paper else p.name.split("_")[0] == m.group(1))
                  and (paper or frame.level_of(p) == "Block")), None)
    for part in [x for x in m.group(2).split(".") if x]:
        level = next((k for k in kids(level) if k.name.split("_")[0] == part), None) if level else None
    return next((t for t, _ in frame._studio_topics(level) if t.name.split("-")[0] == m.group(3) and is_topic(t)),
                None) if level else None


def known(folder: Path, root: Path, below: list | None = None) -> list:
    """What the person should know on this page (JL 261108: a right-rail section of its own, apart from Interactions, "yes,
    we should do that"): the notes (`collect.py know`, state "to know") at this page or below, and those of every page
    above it up to its Project, so a Project's lesson shows on each of its Blocks, Jobs and Tasks. Nearest page first."""
    here = [r for r in (below if below is not None else interactions(folder, root)) if r["state"] == "to know"]
    above = []
    for page in folder.parents:
        if not inside(page, root) or page_level(page) in ("SPACE", "Folder"):
            break
        above += [r for r in page_interactions(page, root) if r["state"] == "to know"]
    return here + above


def _yaml(path: Path) -> dict:
    from live.focus_runs import _yaml as cached      # here, not at the top: focus_runs is imported after this file
    return cached(path)


def page_interactions(page: Path, root: Path) -> list:
    """The interactions kept on one page: its own `runs/rNN_collect_*/`, nothing below it."""
    rows = []
    runs = page / "runs"
    if runs.is_dir() and inside(page, root):
        for run in sorted(p for p in runs.glob("r*_collect_*") if p.is_dir()):
            card = _yaml(run / "run.yaml")          # parsed once per file version (focus_runs), as every Run card
            source = run / "question_collection.md"
            text = source.read_text(encoding="utf-8", errors="ignore") if source.is_file() else ""
            about = (re.search(r"(?m)^for:\s*(.+?)\s*$", text) or [None, str(card.get("target") or "")])[1]
            answers = run / "result" / "answer_collection.md"
            answers = answers if answers.is_file() else None
            got = re.search(r"(?m)^received:\s*(.+?)\s*$", answers.read_text(encoding="utf-8", errors="ignore")) if answers else None
            status = str(card.get("status") or "")
            form = run / f"{run.name}.html"
            done_ = run / "applied.md"                 # what applied each answer (hai-interaction collect.py applied)
            marks = {m.group(1): (m.group(2), m.group(3), m.group(4)) for m in re.finditer(
                r"(?m)^(Q\d+) · (applied|in progress) · (\d{4}-\d{2}-\d{2}) \d{2}:\d{2} · (.+?)\s*$",
                done_.read_text(encoding="utf-8", errors="ignore"))} if done_.is_file() else {}
            rows.append({"run": run.name, "path": run, "page": page, "status": status,
                         "view": str(card.get('view') or ''),
                         "state": "to know" if card.get("source") == "know" else "answered" if answers else INTERACTION_STATE.get(status, status or "planned"),
                         "title": next((ln[2:].strip() for ln in text.splitlines() if ln.startswith("# ")), run.name),
                         "about": about, "topic": interaction_topic(about, page),
                         "asks": re.findall(r"(?ms)^##\s+(Q\d+)\s*·\s*(.+?)\s*$.*?^\*\*(.+?)\*\*\s*$", text),
                         "form": form if form.is_file() else None, "answers": answers,
                         "received": got.group(1) if got else "", "feeds": list(card.get("feeds") or []),
                         "applied": marks})
    return rows


def interaction_button(rows: list, holder: Path, root: Path) -> str:
    """One button, "Interaction", on a row that holds interactions: no count, no colour, no answered or questions
    tag (JL 261031, b16 t01 r04 Q3: C, "we will not have the answered & questions for you"); it pops out the list of
    the row's items, the waiting one first (Q4: A). The same button wherever an item shows (Q6: A). `holder` is what
    the row is: an sNN (the items about it), a Job or Task (the items at it or below), or one collection Run."""
    if not rows or not inside(holder, root):
        return ""
    href = frame.ROUTE + "?" + urlencode({"view": "focus-part", "part": "interactions", "path": frame.rel(holder, root)})
    # a question waiting for the person flags the button (JL 261031: "if there are some questions i need to answer,
    # cuold you flag them as well"); with nothing waiting it stays plain
    waits = any(r.get("state") == "waiting" for r in rows)
    flag = (' style="border-color:light-dark(#ffa94d,#b35c00);color:light-dark(#b35c00,#ffc078)" '
            'title="questions wait for you"') if waits else ''
    return (f'<a class="row-verb"{flag} data-pop="{frame.esc(holder.name)} · Interaction" href="{frame.esc(href)}" '
            f'target=_blank rel=noopener>{"🙋 " if waits else ""}Interaction</a>')


def answer_link(holder: Path, root: Path) -> str:
    """Answer, on a Status row whose Job or Task holds a form that waits for the person: it opens that form in the
    pop-out, the waiting one with the most questions first (round 3: "the Answer button onto Status's Task rows").
    Nothing waits, no verb."""
    rows = [r for r in interactions(holder, root) if r["state"] == "waiting"]
    # the one Interaction button, as wherever an item shows (JL 261031 Q6: A; 261109: "could we change this to the
    # interaction?"): it lists every item at this Job or Task and below, the waiting first; shown only while one waits
    return interaction_button(rows, holder, root).replace('class="row-verb"', 'class="row-verb ix-answer"', 1)


def interaction_items(holder: Path, root: Path) -> list:
    """The items an Interaction button lists: about an sNN, held by one collection Run, or at a page or below."""
    if is_topic(holder):
        return [r for r in card_interactions(frame.topic_owner(holder), root) if r["topic"] == holder]
    if holder.parent.name == "runs" and "_collect_" in holder.name:
        return [r for r in interactions(holder.parent.parent, root) if r["path"] == holder]
    return interactions(holder, root)


def interaction_item(r: dict, folder: Path, root: Path, in_pop: bool = False) -> str:
    """One item (JL 261031, b16 t01 r04 Q5: A): its title, state and date, its questions, and one button: Answer
    (its form) or See answers (its answer file). The Interactions view and the button's pop-out draw it alike; inside
    the pop-out the button opens in that same pop-out, never a second one over it."""
    opens = (lambda label: 'target=_self') if in_pop else (lambda label: f'data-pop="{frame.esc(label)}" target=_blank rel=noopener')
    form, answers = r["form"], r["answers"]
    day = r["received"].split(" ")[0] if r["received"] else (
        dt.datetime.fromtimestamp(form.stat().st_mtime).strftime("%Y-%m-%d") if form else "")
    state = {"waiting": "waiting for you", "answered": "answered", "planned": "not sent yet"}.get(r["state"], r["state"])
    where = asked_where(r, folder, root)
    def flag(q):                                         # an applied answer carries its flag (JL 261031)
        mark = r.get("applied", {}).get(q)
        return (f' <span class="ix-applied" title="{frame.esc(mark[2])}">'
                + ("✅ applied " if mark[0] == "applied" else "⏳ in progress ") + f'{frame.esc(mark[1])}</span>') if mark else ''
    asks = "".join(f'<li><b>{frame.esc(q)}</b> {frame.esc(ask)}{flag(q)}</li>' for q, _, ask in r["asks"])
    if r["state"] == "to know" and form and inside(form, root):
        button = (f'<a class="row-verb" href="{frame.esc(frame._file_url(form, root))}" {opens(r["title"])}>Read</a>')
    elif r["state"] == "to know" and (r["path"] / 'question_collection.md').is_file() and inside(r["path"], root):
        source = r["path"] / 'question_collection.md'
        button = f'<a class="row-verb" href="{frame.esc(frame.reader(source, root))}" {opens(r["title"])}>Read</a>'
    elif r["state"] == "answered" and (form or answers):   # the answered form itself, read only, not its raw Markdown
        shown = form if form and inside(form, root) else answers     # (JL 261031: "the UI here doesn't good")
        button = (f'<a class="row-verb" href="{frame.esc(frame._file_url(shown, root))}" '
                  f'{opens(r["title"] + " · answers")}>See answers</a>') if shown and inside(shown, root) else ""
    elif form and inside(form, root):
        button = (f'<a class="row-verb" href="{frame.esc(frame._file_url(form, root))}" {opens(r["title"])}>Answer</a>')
    else:
        button = ""
    applies = ("Applying it belongs to " + ", ".join(Path(str(f)).name for f in r["feeds"]) + "."
               if r["state"] == "answered" and r["feeds"] else "")   # applied is the owning Task's record, not ours
    return (f'<article class="inbox-row {frame.esc(r["state"])}"><div class="inbox-head"><b>{frame.esc(r["title"])}</b>'
            f'<span class="inbox-state {frame.esc(r["state"])}">{frame.esc(state)}{(" · " + frame.esc(day)) if day else ""}</span></div>'
            f'<p class="inbox-where">{where}</p>'
            + (f'<ol class="inbox-asks">{asks}</ol>' if asks else '')
            + (f'<p class="inbox-waits">{frame.esc(applies)}</p>' if applies else '')
            + (f'<div class="inbox-actions">{button}</div>' if button else '') + '</article>')


def asked_where(r: dict, folder: Path, root: Path) -> str:
    """Who asked and what it is about, in words only: "Asked by the main association · about How the main fit reads"
    (round 3: the footers "j02 · t01 · s03 · r02_collect_…" read as ids); each folder name stays on its link's hover."""
    page = r["page"]
    who = "Kept on" if r["state"] == "to know" else "Asked by"
    where = (f'{who} <a href="{frame.esc(page_url(page, root))}" title="{frame.esc(page.name)}">'
             f'{frame.esc(page_title(page))}</a>')
    if r["topic"] is not None:
        topic = r["topic"]
        where += (f' · about <a href="{frame.esc(topic_home(topic, root))}" title="{frame.esc(topic.name)}">'
                  f'{frame.esc(face_title(frame._notes(topic) or topic / "_") or topic.name)}</a>')
    elif r["about"]:
        about = str(r["about"])
        words = (about.split("@", 1)[1].strip().replace("_", " ") if "@" in about
                 else "" if re.match(r"\s*[\w.-]+-s\d+\b", about) else about)   # a bare address says nothing in words
        where += f' · about {frame.esc(words[:1].upper() + words[1:])}' if words else ""
    return where


def interaction_where(r: dict, folder: Path, root: Path) -> str:
    """The small line under a set's form: who asked, what it is about, when it was answered, and who applies its
    answers; no Run name (round 3)."""
    where = asked_where(r, folder, root)
    if r["received"]:
        where += f' · {frame.esc(r["received"].split(" ")[0])}'
    if r["state"] == "answered" and r["feeds"]:
        where += " · Applying it belongs to " + frame.esc(", ".join(Path(str(f)).name for f in r["feeds"])) + "."
    return where


def standard_interactions(rows: list, folder: Path, root: Path, in_pop: bool = False, title: str = "🙋 Interaction") -> str:
    """The standard Interaction for these rows; a Run with no built form or no questions keeps its plain row, so nothing
    asked goes missing. Its bar draws its state word on the right, as every bar's (round 2: "Interaction5 wait for you")."""
    sec = IX.interaction_section(rows, root, 0, lambda r: interaction_where(r, folder, root), plain=False, title=title)
    sec = (RAIL_IX_CSS + WORD_CSS + sec.replace("<section class=fd-sec>", '<section class="fd-sec ix-rail">', 1)) if sec else ""
    return sec + "".join(interaction_item(r, folder, root, in_pop) for r in rows if r.get("form") is None or not r.get("asks"))
