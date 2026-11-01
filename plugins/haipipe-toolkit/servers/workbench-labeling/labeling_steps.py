"""A 🧭 meaning or 🛠 expression Task's focus page (b15 j01 t03 s58, stage 2; JL 261101: "how will you update the
skills ... and update the workbench here ... Please make them work").

The Task's steps are the view-button-list; each view is ⚙️ Process (the step's flow In → who works → Out, its prompt
box, your sign or the interaction that waits on you) then 📊 Results (what the step made), each numbered from 1, then
the next step. Report shows the Results only. Everything is read from the Task's own folders, in the layout
haipipe-labeling-interaction (meaning) and haipipe-labeling-expression (expression) write; the meaning layout is
engine/meaning_versions.py's, so the page and the skill read the same files:

    meaning     Frame · Report · Preferences · Update     Loop NN makes guideline mNN (a mind map) and labels lNN;
                                                           its Runs end in _mNN; only this Task asks you
    expression  Rewrite · Run · Evaluate · Release         round eNN under one approved meaning; its Runs end in
                                                           _mNN_eNN; it never asks you

Nothing here writes. The one write a page makes is your sign on a guideline (POST /_board/labeling/approve, labeling.py),
and the Preferences prompt, which copies the embedded form's answers with your notes (focus-assets/steps.js).
"""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path
from urllib.parse import quote

from live import focus_page as F, frame, labeling_theme as T
from live.ui_parts import (GROUP_CSS, PB_CSS, PB_JS, PROCESS, PROMPT_CSS, PROMPT_JS, RESULTS, _band, _kv, _numbered, _pill,
                           _section, _todo, prompt_box)

ASSETS = Path(__file__).parent / "focus-assets"
APPROVE = "/_board/labeling/approve"
SHOW = 12                                    # rows a case table shows; the rest are named in one line


def _engine():
    """haipipe-labeling's engine/meaning_versions.py, found from this file; None when the skill is absent."""
    for base in Path(__file__).resolve().parents:
        path = base / "skills" / "2_theme" / "labeling" / "engine" / "meaning_versions.py"
        if path.is_file():
            spec = importlib.util.spec_from_file_location("labeling_meaning_versions", path)
            mod = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(mod)
            except Exception:
                return None
            return mod
    return None


MV = _engine()

STEPS = {
    "meaning": (("frame", "Frame", "what we judge, agreed before any rule"),
                ("prepare", "Report", "the rules now, then this loop's report and the cases it asks about"),
                ("preferences", "Preferences", "this loop's interaction report: your answers"),
                ("update", "Update", "the rules your answers made, what changed, and where the loop goes")),
    "expression": (("rewrite", "Rewrite", "the wording, rewritten under a fixed meaning"),
                   ("run", "Run", "the models labeling Train and Test"),
                   ("evaluate", "Evaluate", "how the models did, and where the round report sends it"),
                   ("release", "Release", "whether the frozen version is ready")),
}
NEXT = {"frame": ("prepare", "🔍 Report"), "prepare": ("preferences", "🙋 Preferences"), "preferences": ("update", "🔁 Update"),
        "rewrite": ("run", "▶️ Run"), "run": ("evaluate", "📊 Evaluate"), "evaluate": ("release", "🔒 Release")}
OWN = ("report", "work")                     # the sections this page draws; the rest are the base page's


def kind(folder) -> str:
    """meaning or expression, for a Task this page draws; "" for every other folder."""
    folder = Path(folder)
    if MV is None or frame.level_of(folder) != "Task":
        return ""
    types = T.types_of(folder)
    return types[0] if types in (("meaning",), ("expression",)) else ""


# ── small parts ──────────────────────────────────────────────────────────────────────────────────────────────────
def esc(x) -> str:
    return frame.esc(str(x))


def _session(task: Path) -> str:
    """The Claude session a step's prompt runs in: the Task face's `session:`, else its Job's, else the Task's name."""
    for face in (task / f"{task.name}.md", task.parent / f"{task.parent.name}.md"):
        if face.is_file():
            m = re.search(r"(?m)^session:\s*`?([\w.-]+)`?", face.read_text(encoding="utf-8", errors="ignore")[:4000])
            if m:
                return m.group(1)
    return task.name


def _flow(inn: tuple, who: tuple, out: tuple) -> str:
    """The step slide's flow: In → who works → Out, each a box with its lines (s58 views, the deck's pages 8 to 15)."""
    boxes = []
    for word, (head, *lines) in (("In", inn), ("Who works", who), ("Out", out)):
        boxes.append(f'<div class=ls-box><small>{word}</small><b>{esc(head)}</b>'
                     + "".join(f"<span>{esc(x)}</span>" for x in lines if x) + "</div>")
    return '<div class=ls-flow>' + '<span class=ls-arrow aria-hidden=true>→</span>'.join(boxes) + "</div>"


def _turns(label: str, turns: list) -> str:
    """The loop's iterations as a strip: [(name, word, now)]; the one waiting on you orange, the current one in the
    workbench's blue (a built page keeps the workbench's colours; review D3 and C2 r01)."""
    def cell(n, w, now, href=""):
        tag, attr = ("a", f' href="{esc(href)}"') if href else ("span", "")
        return (f'<{tag} class="ls-turn{" you" if "waiting for you" in w else " now" if now else ""}"{attr}><b>{esc(n)}</b>'
                f'<small>{esc(w)}</small></{tag}>')
    cells = '<span class=ls-arrow aria-hidden=true>→</span>'.join(cell(*t) for t in turns)
    return f'<div class=ls-turns><span class=ls-tl>{esc(label)}</span>{cells}</div>' if turns else ""


def _bar(words: str, verbs: str = "", mode: str = "you") -> str:
    """Your part, one line: the interaction that waits on you or your sign (orange); done, or waiting on a condition
    (grey)."""
    return f'<div class="ls-bar {mode}"><span>{esc(words)}</span>{verbs}</div>'


def _step(title: str, body: str, state: tuple = ("", "")) -> str:
    """A step's first section, its state word at the right of its heading bar (review C1 and C2 r01)."""
    word, cls = state
    pill = f'<span class=fd-verb><span class="pb-pill {cls}">{esc(word)}</span></span>' if word else ""
    return f'<section class=fd-sec><h3 class=fd-h>{esc(title)}{pill}</h3>{body}</section>'


def _rerun(task: Path, step: str, asks: str, template: str) -> str:
    """A step whose prompt reruns it alone (Run, Evaluate; s58-D15, Q7): the prompt as one row, its words copied by
    Copy prompt and shown on hover, so the step's results come first (review D3 r01)."""
    tail = f'Run this in the Claude session "{_session(task)}"; start it if it is not running.'
    head = " · ".join(x for x in ("✍️ Prompt", step, asks) if x)
    return (PROMPT_CSS + f'<div class="pb-prompt ls-rerun" title="{esc(template)}"><div class=pb-ph><span>{esc(head)}</span>'
            f'<button type=button class="fd-btn pb-copy" data-copy="{esc(template)}" data-tail="{esc(tail)}">Copy prompt</button>'
            "</div></div>" + PROMPT_JS)


def _rows(rows: list) -> str:
    """Rows like ui_parts._todo, each state with its own colour: [(words, sub, (state, ok | you | run | ""))]."""
    return '<div class=pb-todos>' + "".join(
        f'<div class=pb-todo><span class=w>{esc(w)}' + (f"<small>{esc(sub)}</small>" if sub else "") + "</span>"
        + (f'<span class="pb-pill {cls}">{esc(state)}</span>' if state else "") + "</div>"
        for w, sub, (state, cls) in rows) + "</div>"


def _link_tile(head: str, words: str, href: str, verb: str) -> str:
    """A tile whose verb opens where the work goes next (review C4 r01: a mark with no verb)."""
    go = f'<a class=fd-btn href="{esc(href)}">{esc(verb)}</a>' if href else ""
    return f'<div class=pb-tile><b>{esc(head)}</b><span>{esc(words)}</span>{go}</div>'


def _empty(words: str) -> str:
    return f'<p class=ls-empty>{esc(words)}</p>'


def _table(head: tuple, rows: list, more: str = "") -> str:
    """A small table; cells are HTML already escaped."""
    return ('<div class=ls-tw><table class=ls-table><thead><tr>' + "".join(f"<th>{esc(h)}</th>" for h in head)
            + "</tr></thead><tbody>" + "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
            + "</tbody></table></div>" + (f'<p class=ls-foot>{more}</p>' if more else ""))


def _open(path: Path, root: Path, label: str = "Open") -> str:
    return (f'<a class=fd-btn data-pop="{esc(path.name)}" href="{esc(frame._file_url(path, root))}">{esc(label)}</a>'
            if path.is_file() and F.inside(path, root) else "")


def _view_url(task: Path, root: Path, key: str, section: str = "work") -> str:
    return F.page_url(task, root, section, key)


def _when(path: Path) -> str:
    import datetime
    return datetime.datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M") if path.exists() else ""


def _chain(steps: list) -> str:
    """A sequence as boxes with arrows, each with its role word above: [(role, words)]."""
    return ('<div class=ls-chain>' + '<span class=ls-arrow aria-hidden=true>→</span>'.join(
        f'<div class=ls-box><small>{esc(r)}</small><span>{esc(w)}</span></div>' for r, w in steps) + "</div>")


def _tiles(tiles: list) -> str:
    return '<div class=pb-tiles>' + "".join(f'<div class=pb-tile><b>{esc(h)}</b><span>{esc(w)}</span></div>'
                                            for h, w in tiles) + "</div>"


def _prompt(task: Path, root: Path, key: str, step: str, asks: str, template: str, fields=None, cls: str = "") -> str:
    box = prompt_box(template, fields, _session(task), step=step, asks=asks, key=f"notes:{frame.rel(task, root)}#{key}",
                     upload=(frame.rel(task, root), "/_board/labeling/notes"))
    return f'<div class="{cls}">{box}</div>' if cls else box


# ── 🧭 meaning ───────────────────────────────────────────────────────────────────────────────────────────────────
def _map_html(m: dict, mark: dict | None = None) -> str:
    """One guideline version as a tree (s58 C2, C4): the question, its values, each value's rules. A rule's tag means
    one thing per view: in Report (`mark` given) the card of this loop's report that asks about it; in Update the card
    that set it (its note's "from rNN QN")."""
    branches = []
    for b in m["branches"]:
        leaves = []
        for r in b["rules"]:
            if mark is not None:
                tag, why = mark.get(r["text"].strip().lower(), ("", ""))
                tag = f"{tag} asks" if tag else ""
            else:
                tag, why = (f"from {r['tag']}" if r["tag"] else ""), r.get("cite") or r["note"]
            pill = f'<span class=ls-q title="{esc(why)}">{esc(tag)}</span>' if tag else ""
            leaves.append(f'<div class=ls-lf title="{esc(r["note"])}"><span>{esc(r["text"])}</span>{pill}</div>')
        branches.append(f'<div class=ls-br><div class=ls-bn>{esc(b["name"])}</div><div class=ls-lvs>'
                        + ("".join(leaves) or '<div class=ls-lf><span class=mut>no rule yet</span></div>') + "</div></div>")
    return (f'<div class=ls-map><div class=ls-root>{esc(m["root"] or "the question")}</div>'
            f'<div class=ls-brs>{"".join(branches)}</div></div>')


def _maps(task: Path, root: Path, on: str = "", mark: dict | None = None, sign: bool = True) -> str:
    """Every guideline version, one button each, the newest (or `on`) open: its tree, then its sign. `mark`: Report's
    {rule words: (QN, why)} for the open version; None in Update (each rule's own card)."""
    vs = MV.versions(task)
    if not vs:
        return ""
    on = on if on in dict(vs) else vs[-1][0]
    buttons = "".join(f'<button type=button class="ls-v{" on" if v == on else ""}" data-pbtab="lsmm{v}">{esc(v)}</button>'
                      for v, _ in vs)
    panels = []
    for v, path in vs:
        signed = MV.approval(task, v)
        foot = (f"{v} · approved by {signed['by']} · {signed['at']}" if signed else f"{v} · not approved yet") if sign else ""
        drawn = f"/_board/workbench?path={quote(frame.rel(path, root))}&view=focus-map"     # the drawn map, not its Markdown
        panels.append(f'<div class="pb-panel ls-mp" data-pbpanel="lsmm{v}"{"" if v == on else " hidden"}>'
                      + _map_html(MV.read_map(path), (mark if v == on else {}) if mark is not None else None)
                      + f'<p class=ls-foot>{esc(foot)} <a class=fd-btn data-pop="{esc(v)}" href="{esc(drawn)}">'
                      'Open the mind map</a></p></div>')
    return (f'<div class="pb-tabset ls-maps"><div class=ls-vrow><span>version</span>{buttons}</div>'
            + "".join(panels) + "</div>")


def _meaning_turns(loops: list, now_n: int, now_word: str = "", task: Path | None = None, root: Path | None = None) -> str:
    go = {"waiting for you": "preferences", "answered; Update next": "update"}
    turns = [(f"Loop {lp['n']}", lp["state"], lp["n"] == now_n,
              _view_url(task, root, go[lp["state"]]) if task is not None and lp["state"] in go else
              _view_url(task, root, "update") if task is not None and lp["state"].startswith("made ") else "")
             for lp in loops]
    if now_n and all(lp["n"] != now_n for lp in loops):
        turns.append((f"Loop {now_n}", now_word or "next", True, ""))
    return _turns("🧭 meaning loops", turns)


def _current(loops: list) -> int:
    """The loop Report works on: the newest loop with no guideline yet, else the next one."""
    if loops and not loops[-1]["map"]:
        return loops[-1]["n"]
    return (loops[-1]["n"] + 1) if loops else 1


def _form_loop(loops: list) -> dict | None:
    """The loop Preferences shows: the form that waits for you, else the newest form."""
    forms = [lp for lp in loops if lp.get("collect") is not None]
    waiting = [lp for lp in forms if MV.state(lp["collect"]) == "waiting"]
    return (waiting or forms or [None])[-1]


def _update_loop(loops: list) -> dict | None:
    """The loop Update shows: the newest loop whose form is answered or whose guideline is written."""
    done = [lp for lp in loops if lp["map"] or (lp.get("collect") is not None and MV.state(lp["collect"]) == "done")]
    return done[-1] if done else None


def _report_rows(task: Path, root: Path, loops: list) -> str:
    rows = []
    for lp in reversed(loops):
        run = lp.get("collect")
        if run is None:
            continue
        form, st = run / f"{run.name}.html", MV.state(run)
        sub = run.name
        word = {"waiting": "waiting for you", "done": "answered"}.get(st, "form not built yet")
        verb = ("Answer" if st == "waiting" else "Open") if form.is_file() else ""
        rows.append((f"Loop {lp['n']} · report-{lp['n']:02d}", sub, word, verb,
                     frame._file_url(form, root) if form.is_file() else "", True))
    return _todo(rows) if rows else ""


def _cases(task: Path, root: Path, lp: dict | None) -> tuple[str, str, str]:
    """This loop's typical, hard and random cases (use case 2: the draw Run's draws.json and signals.jsonl), each a
    table: item, why it was drawn, its current label, the card that shows it."""
    if lp is None or lp.get("draw") is None:
        return "", "", ""
    out = lp["draw"] / "result"
    path = out / "draws.json"
    if not path.is_file():
        return "", "", ""
    try:
        sets = json.loads(path.read_text(encoding="utf-8")).get("sets") or {}
    except ValueError:
        return "", "", ""
    sig = {}
    if (out / "signals.jsonl").is_file():
        for raw in (out / "signals.jsonl").read_text(encoding="utf-8").splitlines():
            try:
                row = json.loads(raw)
            except ValueError:
                continue
            sig[row.get("item_id")] = row
    cards = MV.cards_by_item(MV.report_json(lp["runs"]))
    now = _labels_now(task)

    def table(key: str, why: bool, hide: bool) -> str:
        ids = sets.get(key) or []
        if not ids:
            return ""
        rows = []
        for i in ids[:SHOW]:
            s = sig.get(i, {})
            label = "hidden until you judge it" if hide else (now.get(i) or s.get("label") or s.get("majority") or "no majority")
            card = cards.get(i)
            cells = [f"<span class=nw>{esc(i)}</span>"] + ([esc(", ".join(s.get("flags") or []) or "flagged")] if why else [])
            rows.append(tuple(cells + [esc(label), f"<span class=nw>{esc(card)}</span>" if card else "<span class=mut>no card</span>"]))
        more = esc(f"{len(ids) - SHOW} more in {lp['draw'].name}'s draws.json") if len(ids) > SHOW else ""
        head = ("item", "why flagged", "current label", "card") if why else ("item", "current label", "card")
        return _table(head, rows, more)

    return table("typical", False, False), table("hard", True, False), table("blind", False, True)


def _labels_now(task: Path) -> dict:
    """{item: label} from the newest Update's labels.jsonl (lNN), so a case shows what the last loop decided."""
    for run in reversed(MV.runs(task)):
        path = run / "result" / "labels.jsonl"
        if MV.role(run) == "update" and path.is_file():
            out = {}
            for raw in path.read_text(encoding="utf-8").splitlines():
                try:
                    row = json.loads(raw)
                except ValueError:
                    continue
                if row.get("item_id"):
                    out[row["item_id"]] = row.get("label") or "no majority"
            return out
    return {}


def _mark(lp: dict | None) -> dict:
    """{rule words: (QN, why)} for the rules this loop's report asks about: a card whose current_rule quotes a rule."""
    report = MV.report_json(lp["runs"]) if lp else None
    out = {}
    for i, card in enumerate((report or {}).get("cards") or [], 1):
        rule = re.sub(r"^R\d+:\s*", "", str(card.get("current_rule") or "")).strip().rstrip(".").lower()
        if rule and rule not in ("none yet", "none"):
            out.setdefault(rule, (f"Q{i}", f"asked in report-{lp['n']:02d}, Q{i}"))
    return out


def m_frame(task: Path, root: Path) -> tuple[str, str]:
    rec = MV.frame_record(task)
    process = _step("🎯 Frame the labeling task", _flow(
        ("Rough idea + prepared items", "goals · use cases · constraints", "items, context, old labels"),
        ("🤖 Agent", "inspect items; surface assumptions", rec["run"].name if rec else "a frame Run, rNN_collect_frame"),
        ("Initial task agreement", "purpose · target population", "provisional labels")), states(task)["frame"])
    process += _prompt(task, root, "frame", "Frame", "your rough idea", (
        f"Use /haipipe-labeling-interaction on {task.name}, step Frame: read the items and the old labels' sources this "
        "Job names, surface the assumptions in my idea below, then ask me the three frame questions (what to judge, "
        "which standard, who decides) as a frame form; record my answers as the frame."),
        (("Goal", "what the labels are for"), ("Use cases", "where they will be used"), ("Constraints", "data, time, who decides")))
    if not rec or not rec["decisions"]:
        word = "waiting for you" if rec and rec["state"] == "waiting" else "not framed yet"
        results = _section("📜 Initial task agreement", _empty(f"Nothing to show yet ({word}): this view will show what "
                                                               "we judge, agreed before any rule."))
        if rec and rec["state"] == "waiting":
            form = rec["run"] / f"{rec['run'].name}.html"
            process += _bar(f"🙋 Interaction · the frame questions wait for your answers", _open(form, root, "Answer"))
        return process, results
    first, rest = rec["decisions"][0], rec["decisions"][1:]
    results = _section("📜 Initial task agreement",
                       f'<p class=pb-big>{esc(first["decision"])}</p><p class=pb-state>agreed as frame f01</p>')
    if rest:
        results += _section("❓ What you confirmed", _kv([(d["title"], esc(d["decision"])) for d in rest]))
    return process, results


def m_report(task: Path, root: Path, loops: list) -> tuple[str, str]:
    n = _current(loops)
    lp = next((x for x in loops if x["n"] == n), None)
    collect = lp.get("collect") if lp else None
    process = _step(f"🔍 Prepare interaction report-{n:02d}", _flow(
        ("Human sources + reports", "ideas · notes · decisions", "earlier round reports · cases"),
        ("🤖 Alignment Agent", "/haipipe-labeling-interaction", collect.name if collect else f"rNN_collect_report_m{n:02d}"),
        (f"Interaction report-{n:02d}", "cards with evidence", "for you to decide")), states(task)["prepare"])
    process += _prompt(task, root, "prepare", "Report", f"Loop {n}'s interaction report", (
        f"Use /haipipe-labeling-interaction on {task.name}, Loop {n}: prepare interaction report-{n:02d} from my sources, "
        "earlier decisions and any round report, its cases grouped typical, hard and random. Flags are hypotheses: no "
        "rule or label changes until I answer."))
    maps = _maps(task, root, mark=_mark(lp))
    results = _section("🧠 Guideline rules, as a mind map", maps or _empty(
        "No guideline yet: Loop 1's Update writes m01, the rules as a mind map."))
    results += _section("🙋 Interaction report", _report_rows(task, root, loops) or _empty(
        f"No report yet: Loop {n}'s report shows here once its form is built."))
    typical, hard, blind = _cases(task, root, lp)
    results += _section("📌 Typical cases", typical or _empty("No cases drawn yet for this loop."))
    results += _section("⚠️ Hard cases", hard or _empty("No flagged cases drawn yet for this loop."))
    results += _section("🎲 Random cases", blind or _empty("No random cases drawn yet for this loop."))
    return process, results


def m_preferences(task: Path, root: Path, loops: list) -> tuple[str, str]:
    lp = _form_loop(loops)
    if lp is None:
        n = _current(loops)
        process = _section("🙋 Collect preferences", _flow(
            (f"Interaction report-{n:02d}", "earlier decisions", "evidence beside each card"),
            ("🙋 You", "confirm · clarify · revise · defer", f"rNN_collect_report_m{n:02d}"),
            ("Decision record", "preference · reason", "scope · version")))
        process += _bar(f"No report waits for you: Report prepares Loop {n}'s.", "", "wait")
        return process, _section("🗒 Cards", _empty("Nothing to show yet: this view will show the report's cards and "
                                                     "your answers."))
    n, run = lp["n"], lp["collect"]
    st, form = MV.state(run), run / f"{run.name}.html"
    process = _step("🙋 Collect preferences", _flow(
        (f"Interaction report-{n:02d}", "earlier decisions", "evidence beside each card"),
        ("🙋 You", "confirm · clarify · revise · defer", run.name),
        ("Decision record", "preference · reason", "scope · version")), states(task)["preferences"])
    if st == "waiting" and form.is_file():
        process += _section(f"📝 Interaction report-{n:02d}",
                            f'<iframe class=ls-form id=ls-form src="{esc(frame._file_url(form, root))}" '
                            f'title="Interaction report-{n:02d}" data-ls-form></iframe>')
        process += _prompt(task, root, "preferences", "Preferences", "send my answers", (
            f"Use /haipipe-labeling-interaction on {task.name}, Loop {n}: save my answers to report-{n:02d} ({run.name}: "
            "the block at the end, from its 'haipipe-interaction answers' line) with my notes, then start Update."),
            (("your notes", "optional: context for the decision record"),), cls="ls-send")
    elif st == "done":
        saved = run / "result" / "answer_collection.md"
        process += _bar(f"✅ Loop {n} · report-{n:02d} answered {_when(saved)}", _open(form, root, "See answers"), "done")
    else:
        process += _bar(f"Loop {n} · report-{n:02d}'s form is not built yet: Report builds it.", "", "wait")
    if st != "done":                                   # the step's Out: the decision record, once saved
        return process, _section("📦 Decision record", _empty(
            f"Not saved yet: Copy prompt sends your answers to report-{n:02d}, and the chat saves them here."))
    picks, flags = {a["q"]: a for a in MV.answers(run / "result" / "answer_collection.md")}, MV.applied(run)
    rows = []
    for q, title in MV.questions(run):
        a, flag = picks.get(q), flags.get(q)
        said = ""
        if a:
            said = (f"{a['pick']} · {a['text']}" if a["pick"] and a["pick"] != "own" else a["text"] or "no option picked")
            said += f" · note: {a['note']}" if a["note"] else ""
        rows.append((f"{q} · {title}", said, flag[0] if flag else "saved", "", "", False))
    return process, _section("📦 Decision record", _todo(rows))


def _label_changes(task: Path, lp: dict) -> list:
    """Reference label changes lNN: the Update Run's result/changes.md (or gold/versions/lNN/changes.md), one row per
    `- ` line or table row."""
    paths = ([lp["update"] / "result" / "changes.md"] if lp.get("update") is not None else [])
    paths.append(task / "gold" / "versions" / f"l{lp['n']:02d}" / "changes.md")
    for path in paths:
        if path.is_file():
            rows = []
            for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
                ln = raw.strip()
                if ln.startswith("- "):
                    rows.append(ln[2:])
                elif ln.startswith("|") and not re.match(r"^\|[\s:|-]+\|$", ln) and "item" not in ln.lower()[:12]:
                    rows.append(" · ".join(c.strip() for c in ln.strip("|").split("|") if c.strip()))
            return [(path, r) for r in rows]
    return []


def m_update(task: Path, root: Path, loops: list) -> tuple[str, str]:
    lp = _update_loop(loops)
    n = lp["n"] if lp else _current(loops)
    v, run = f"m{n:02d}", (lp or {}).get("collect")
    upd = (lp or {}).get("update")
    process = _step("🔁 Integrate feedback and check alignment", _flow(
        ("Your answers", f"{run.name}'s answer_collection.md" if run else "the answered form", "+ earlier decisions and rules"),
        ("🤖 Alignment Agent", "reconcile; apply approved changes", upd.name if upd else f"rNN_update_{v}"),
        (f"Guideline {v}", "rules as a mind map", f"+ reference labels l{n:02d}")),
        states(task)["update"] if states(task)["update"][1] == "you" else ("", ""))
    made = bool(lp and lp["map"])
    signed = MV.approval(task, v) if made else None
    if signed:
        process += _bar(f"✅ {v} approved by {signed['by']} · {signed['at']}: expression may run on it", "", "done big")
    elif made:
        process += _bar(f"✍️ Your sign: approve {v} and l{n:02d}; expression starts only after it",
                        f'<input class=ls-by name=by maxlength=80 placeholder="your name" aria-label="Your name">'
                        f'<button type=button class=fd-btn data-approve="{esc(v)}" data-task="{esc(frame.rel(task, root))}">'
                        f'Approve {esc(v)}</button><span class=ls-msg role=status></span>')
    else:
        process += _bar(f"✍️ Your sign: approve {v} once Update has written it", f'<button type=button class=fd-btn disabled>'
                        f'Approve {esc(v)}</button>', "wait")
    process += _prompt(task, root, "update", "Update", "apply my answers", (
        f"Use /haipipe-labeling-interaction on {task.name}, step Update, Loop {n}: read "
        f"{run.name if run else 'the form'}'s answer_collection.md; write meaning {v} and labels l{n:02d}, each rule "
        f"naming its card; recheck affected items; anything unclear becomes a card for Loop {n + 1}, never a guess. "
        "Then wait for my sign."))
    if not lp:
        return process, _section("🧠 Guideline rules, as a mind map", _empty(
            "Nothing to show yet: Update runs after you answer a report."))
    results = _section("🧠 Guideline rules, as a mind map", _maps(task, root, on=v, sign=False) or _empty(
        f"{v} is not written yet: the Update prompt above writes it."))
    flags = MV.applied(run) if run else {}
    titles = dict(MV.questions(run)) if run else {}
    cite = (run.name.split("_", 1)[0] + " ") if run else ""
    changes = [w for _, w in _label_changes(task, lp)]
    rows, used = [], set()
    for q, (st, what) in flags.items():
        mine = [w for w in changes if f"({cite}{q})" in w or f"({cite}{q}," in w]
        used.update(mine)
        rows.append((f"{q} · {titles.get(q, '')}".strip(" ·"), " · ".join([what] + [f"label {w}" for w in mine]),
                     ("done", "ok") if st == "applied" else ("in progress", "run")))
    rows += [(f"label {w}", "", ("done", "ok")) for w in changes if w not in used and not w.startswith("no label")]
    results += _section("📜 What your answers changed", _rows(rows) if rows else _empty(
        "No answer applied yet: Update flags each answer it applies."))
    deferred = [q for q, (st, _) in flags.items() if st == "in progress"]
    expression = next((t for t in sorted(task.parent.iterdir()) if t.is_dir() and kind(t) == "expression"), None)
    results += _section("➡️ Where it goes", '<div class=pb-tiles>' + _link_tile(
        "🛠 expression", f"{v} + l{n:02d}" + ("" if signed else ", after your sign"),
        _view_url(expression, root, "rewrite") if expression and signed else "", "Open expression") + _link_tile(
        f"🔍 Loop {n + 1}'s report", (f"{len(deferred)} open card{'s' if len(deferred) != 1 else ''} asked again"
                                      if deferred else "new cases"), _view_url(task, root, "prepare"), "Open Report")
        + "</div>")
    hist = []
    rec = MV.frame_record(task)
    if rec:
        hist.append(("frame", f"f01 ← {rec['run'].name}"))
    for x in loops:
        if x["map"]:
            src = x.get("collect")
            hist.append((f"Loop {x['n']}", f"{x['version']} ← {src.name if src is not None else 'its answers'}"))
    if hist:
        results += _section("🧾 Meaning history", _chain(hist))
    return process, results


# ── 🛠 expression ────────────────────────────────────────────────────────────────────────────────────────────────
XROLE = (("_rewrite_", "rewrite"), ("_run_", "run"), ("_evaluate_", "evaluate"), ("_release", "release"))


def _xruns(task: Path) -> dict:
    """{role: [Runs]} for an expression Task: rewrite, run, evaluate, release."""
    out = {r: [] for _, r in XROLE}
    for run in MV.runs(task):
        role = next((r for key, r in XROLE if key in run.name), "")
        if role:
            out[role].append(run)
    return out


def _round(run: Path | None) -> str:
    m = re.search(r"_e(\d\d)$", run.name) if run is not None else None
    return f"e{m.group(1)}" if m else ""


def _json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None
    except ValueError:
        return None


def _meaning_strip(task: Path, root: Path) -> tuple[str, str]:
    """(the strip, the approved version or "") from the Job's meaning Task: expression runs only on a signed meaning."""
    got = MV.approved_meaning(task.parent)
    if got:
        mt, v, signed = got
        return (f'<div class=ls-strip>🔒 approved meaning {esc(v)} · fixed during rewriting · signed by '
                f'{esc(signed["by"])} {esc(signed["at"])}</div>', v)
    meaning = next((t for t in sorted(task.parent.iterdir()) if t.is_dir() and kind(t) == "meaning"), None)
    link = (f'<a class=fd-btn href="{esc(_view_url(meaning, root, "update"))}">Open meaning\'s Update</a>' if meaning else "")
    return _bar("⏳ No approved meaning yet: expression waits for your sign in 🧭 meaning's Update", link, "wait"), ""


def x_view(task: Path, root: Path, key: str) -> tuple[str, str, str]:
    """(lead, process, results) for one expression step."""
    xr = _xruns(task)
    strip, v = _meaning_strip(task, root)
    rounds = sorted({_round(r) for r in xr["rewrite"] if _round(r)})
    now = rounds[-1] if rounds else "e01"
    last = {r: (runs[-1] if runs else None) for r, runs in xr.items()}
    reached = ("report sent" if last["evaluate"] is not None and MV.state(last["evaluate"]) == "done"
               else "in progress")
    turns = _turns(f"🛠 rounds under {v or 'the approved meaning'}",
                   [(e, reached if e == now else "done", e == now) for e in rounds] or [("e01", "next", True)])
    st = states(task)
    if key == "rewrite":
        process = _step("✏️ Rewrite expression", _flow(
            (f"Approved rules {v or 'mNN'}", "Train error analysis only", ""),
            ("🤖 Execution & Audit Agent", "wording · order · examples", last["rewrite"].name if last["rewrite"] else f"rNN_rewrite_{v or 'mNN'}_{now}"),
            (f"Expression {now}", "", "")), st["rewrite"])
        process += _prompt(task, root, "rewrite", "Rewrite", f"the whole round {now}", (
            f"Use /haipipe-labeling-expression on {task.name}, round {now}: rewrite the wording under meaning "
            f"{v or '<the approved mNN>'} from Train errors only, run the executors, evaluate, and stop at round report "
            f"{now}. Change no rule and ask me nothing: rule or label questions go to the round report."))
        changes = last["rewrite"] / "result" / "changes.md" if last["rewrite"] else None
        body = (F.markdown(changes.read_text(encoding="utf-8"), task, root) if changes and changes.is_file() else "")
        return strip + turns, process, _section("✏️ What the wording changed", body or _empty(
            "Nothing to show yet: this view will show what the round's rewrite changed."))
    if key == "run":
        process = _step("▶️ Run label executors", _flow(
            (f"{v or 'mNN'} + expression {now}", "Train + Test items", ""),
            ("🤖 Label executors", "the models this Job names", last["run"].name if last["run"] else "rNN_run_…"),
            ("Labels on Train and Test", "", "")), st["run"])
        process += _rerun(task, "Run", "rerun the executors", (
            f"To rerun this step alone (Rewrite's prompt runs the whole round): use /haipipe-labeling-expression on "
            f"{task.name}, step Run, round {now}: label Train and Test with {v or 'the approved meaning'} + {now} on the "
            "Job's executors; keep the reference labels hidden."))
        data = _json(last["run"] / "result" / "runs.json") if last["run"] else None
        rows = [(esc(r.get("model", "")), esc(r.get("train", "")), esc(r.get("test", "")), _pill(str(r.get("state", ""))))
                for r in (data or []) if isinstance(r, dict)]
        return strip + turns, process, _section("▶️ Executor runs", _table(("model", "Train", "Test", "state"), rows)
                                                if rows else _empty("Nothing to show yet: this view will show each model's run."))
    if key == "evaluate":
        process = _step("🧮 Evaluate and analyze errors", _flow(
            ("Labels + reference labels", "hidden from the executors", ""),
            ("🤖 Execution & Audit Agent", "score by set; sort errors", last["evaluate"].name if last["evaluate"] else "rNN_evaluate_…"),
            (f"Round report {now}", "errors by kind", "and where the round goes")), st["evaluate"])
        process += _rerun(task, "Evaluate", f"rerun round report {now}", (
            f"To rerun this step alone (Rewrite's prompt runs the whole round): use /haipipe-labeling-expression on "
            f"{task.name}, step Evaluate, round {now}: score by set and model, sort errors into the four kinds, and "
            f"write round report {now} with its route."))
        out = last["evaluate"] / "result" if last["evaluate"] else None
        report = out / "round_report.md" if out else None
        results = ""
        if report and report.is_file():
            head = next((ln.strip("# ").strip() for ln in report.read_text(encoding="utf-8").splitlines()
                         if ln.strip() and not ln.startswith("#")), report.name)
            meaning = next((t for t in sorted(task.parent.iterdir()) if t.is_dir() and kind(t) == "meaning"), None)
            href = _view_url(meaning, root, "prepare") if meaning else ""
            results += _section(f"📋 Round report {now}", f'<p class=pb-big>{esc(head)}</p><div class=ls-verbs>'
                                f'<span class="pb-pill ok">sent to meaning</span>{_open(report, root, "Open the round report")}'
                                + (f'<a class=fd-btn href="{esc(href)}">Open in meaning</a>' if href else "") + "</div>")
        errors = _json(out / "errors.json") if out else None
        if isinstance(errors, dict) and errors:
            results += _section("🔍 Errors, by kind", '<div class="pb-tiles ls-tiles4">' + "".join(
                f'<div class=pb-tile><span class=ls-num>{esc(val if not isinstance(val, dict) else val.get("count", ""))}</span>'
                f'<small>{esc(k)}</small></div>' for k, val in errors.items()) + "</div>")
        perf = _json(out / "performance.json") if out else None
        rows = [(esc(r.get("model", "")), esc(r.get("train", "")), esc(r.get("test", "")), esc(r.get("coverage", "")))
                for r in (perf or []) if isinstance(r, dict)]
        if rows:
            results += _section("📈 Labeling performance", _table(("model", "Train quality", "Test quality", "coverage"), rows))
        return strip + turns, process, results or _section(f"📋 Round report {now}", _empty(
            "Nothing to show yet: this view will show the round report, its errors by kind and each model's quality."))
    # release
    process = _step("🔒 Freeze a version and check release readiness", _flow(
        ("Frozen package", f"rules {v or 'mNN'} · expression {now}", "+ labels + model settings"),
        ("🤖 Agent + evaluation tools", "review staging evidence", "and acceptance criteria"),
        ("Pass or fail", "pass: release a qualified version", "fail: back to expression or meaning")), st["release"])
    process += _prompt(task, root, "release", "Release", "check readiness", (
        f"Use /haipipe-labeling-expression on {task.name}, step Release: freeze {v or 'the approved meaning'} · {now} · "
        "its reference labels · the model settings, check the floors, non-regression and cost, and report pass or fail."))
    crit = _json(last["release"] / "result" / "criteria.json") if last["release"] else None
    rows = [(str(c.get("name", "")), "", str(c.get("state", "not yet")), "", "", False) for c in (crit or []) if isinstance(c, dict)]
    rows = rows or [("Quality + coverage floors", "", "not yet", "", "", False), ("Strong-model non-regression", "", "not yet", "", "", False),
                    ("Cost per accepted item", "", "not yet", "", "", False)]
    met = all(r[2] in ("met", "passed", "pass", "done") for r in rows)
    process += _bar("✍️ Your sign: the release, once every criterion below is met",
                    '<button type=button class=fd-btn disabled>Sign release</button>', "you" if met else "wait")
    results = _section("✅ Release criteria", _todo(rows))
    results += _section("🧾 Fresh data for claims", '<p class=ls-line>claims about unseen items need data beyond the '
                                                    'audited staging set</p>')
    return strip + turns, process, results


def states(task: Path) -> dict:
    """{step: (state word, ok | you | run | "")}: where each step stands, on its button and its first heading bar."""
    out = {}
    if kind(task) == "expression":
        xr = _xruns(task)
        for key in ("rewrite", "run", "evaluate"):
            run = xr[key][-1] if xr[key] else None
            out[key] = ("done", "ok") if run is not None and MV.state(run) == "done" else \
                ("running", "run") if run is not None and MV.state(run) in ("running", "waiting") else ("", "")
        run = xr["release"][-1] if xr["release"] else None
        out["release"] = ("ready", "ok") if run is not None and MV.state(run) == "done" else ("not yet", "")
        return out
    loops, rec = MV.loops(task), MV.frame_record(task)
    out["frame"] = (("agreed", "ok") if rec and rec["decisions"] else ("waiting for you", "you")
                    if rec and rec["state"] == "waiting" else ("next", ""))
    n = _current(loops)
    lp = next((x for x in loops if x["n"] == n), None)
    collect = lp.get("collect") if lp else None
    if collect is not None and MV.state(collect) in ("waiting", "done"):
        out["prepare"] = (f"report-{n:02d} ready", "ok")
    elif lp and (lp.get("report") is not None or lp.get("draw") is not None):
        out["prepare"] = (lp["state"], "you" if lp["state"] == "draw planned" else "run")   # a planned draw: you press it
    else:
        out["prepare"] = ("next", "")
    form = _form_loop(loops)
    out["preferences"] = (("waiting for you", "you") if form and MV.state(form["collect"]) == "waiting"
                          else ("answered", "ok") if form else ("", ""))
    up = _update_loop(loops)
    out["update"] = ((f"{up['version']} approved", "ok") if up and up["approved"] else
                     (f"sign {up['version']}", "you") if up and up["map"] else ("next", "") if up else ("", ""))
    return out


# ── the page ─────────────────────────────────────────────────────────────────────────────────────────────────────
def default_view(task: Path) -> str:
    """Where Work opens: the step that needs you or comes next."""
    if kind(task) == "expression":
        xr = _xruns(task)
        return next((k for k in ("rewrite", "run", "evaluate", "release") if not xr[k]), "evaluate")
    loops = MV.loops(task)
    if any(lp.get("collect") is not None and MV.state(lp["collect"]) == "waiting" for lp in loops):
        return "preferences"
    rec = MV.frame_record(task)
    if not rec or not rec["decisions"]:
        return "frame"
    if loops and (not loops[-1]["map"] and loops[-1].get("collect") is not None
                  and MV.state(loops[-1]["collect"]) == "done"):
        return "update"
    if loops and loops[-1]["map"] and not loops[-1]["approved"]:
        return "update"
    return "prepare"


def view_html(task: Path, root: Path, section: str, key: str) -> str:
    """One step: its strip, ⚙️ Process, 📊 Results, the next step (Report: the Results only)."""
    steps = {k: (name, cap) for k, name, cap in STEPS[kind(task)]}
    name, caption = steps[key]
    if kind(task) == "meaning":
        loops = MV.loops(task)
        at = {"preferences": _form_loop(loops), "update": _update_loop(loops)}.get(key)
        lead = "" if key == "frame" else _meaning_turns(loops, at["n"] if at else _current(loops), "report next", task, root)
        process, results = {"frame": lambda: m_frame(task, root), "prepare": lambda: m_report(task, root, loops),
                            "preferences": lambda: m_preferences(task, root, loops),
                            "update": lambda: m_update(task, root, loops)}[key]()
    else:
        lead, process, results = x_view(task, root, key)
    body = lead + ("" if section == "report" else _band(PROCESS, _numbered(process))) + _band(RESULTS, _numbered(results))
    if section != "report" and key in NEXT:
        nxt, words = NEXT[key]
        body += f'<p class=ls-next><a href="{esc(_view_url(task, root, nxt))}">next: {esc(words)} →</a></p>'
    return (f'<p class="view-caption">{esc(caption[:1].upper() + caption[1:])}.</p>'
            f'<div class=ls-view>{body}</div>')


def page(theme, root, folder, section: str = "", group: str = ""):
    """The Task's focus page: the base page's shell and rails (labeling_focus.task_shell); Report and Work hold the
    steps."""
    from live import labeling_focus as LF
    root, folder = Path(root).resolve(), Path(folder).resolve()
    views = {k: name for k, name, _ in STEPS[kind(folder)]}
    keys = [k for k, _, _ in LF.base_rail(folder, root)]
    if section in views and section not in keys:               # a step named as a section: that step, in Work
        section, group = "work", section
    if section in keys and section not in OWN:
        return F.render(theme, root, folder, section, group)
    section = section if section in OWN else "work"
    view = group if group in views else default_view(folder)
    from live import focus_draft as FD                         # the same section bars, folding by their heading
    css = "<style>" + (ASSETS / "steps.css").read_text(encoding="utf-8") + "</style>"
    js = "<script>" + (ASSETS / "steps.js").read_text(encoding="utf-8") + "</script>"
    return LF.task_shell(root, folder, section, views, view, view_html(folder, root, section, view),
                         PB_CSS + GROUP_CSS + FD.CSS + css, PB_JS + FD.JS + js, states(folder))
