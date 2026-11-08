"""The insight theme's plan-C views: what each Space shows at the Board, a Job and a Task (b11 s11 · s12 · s13).

Drawn from the folders (insight_plan_c.py) in the base's look only: .topic folds, .wf-table, the q-row
Question │ Work │ Report rows, .chip, .st-ok / .st-warn, and the frame's own tab row (.row.subs .tab) for a
Space's second row of buttons. A Space with two dimensions (Partition × Reading at the Board, Partition ×
Period at a Job) keeps the first in the frame's third row and draws the second as a row of the same tabs
under it; `sub` carries both as "<first>/<second>". Read-only: a run type only copies its prompt.

The design's open points (b11 goal spec, "still open") are drawn as nothing: no rule for "held" (the
compare report is shown as its run wrote it), no backfill Job, no stale handoff, Findings the same on
every partition, no automatic re-run, no Board Run pop-out of its own, no Prototype steps in the Guide.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from live import insight_plan_c as P
from live.frame import Space, delivery_view, esc, pop, reader, rel, table, themes

# X, the Executive level (JL 261012: "based on the whole bottom level question, what are the high level question
# we should have?"): a few plain questions a leader asks, each answered from the questions below, no run of its own.
# They are read together as the Overall Report, the Audience Report's first button, before Full (JL 261012: "before
# the Full, we should have a Overall Report ... we can click and read it"); no cut's table lists them.
LEVELS = (("X", "Executive", "may say: the plain answer a leader asks for, each resting on the questions below"),
          ("D", "Data", "may say: counts, what was seen"),
          ("I", "Information", 'may say: rates and contrasts, never "because"'),
          ("K", "Knowledge", "may say: one claim, how sure, its rivals, its limits"),
          ("W", "Wisdom", "may say: advice, signed by a person, for Design"))
READINGS = ("Coverage", "Tracks", "Consistency", "Findings")
PERIODS = ("Current", "vs previous")
STATUS = ("new question", "new finding", "held", "changed", "dropped", "not comparable")
OK = ("ok", "closed", "answered", "✅", "held", "new finding", "new question", "pool", "signed")
QUIET = ("—", "", "planned", "not comparable", "none")


# each button's owner skill (b11 s21-insight-run-skill, frame 1; 261007)
SKILLS = {"Add a data version": ("haipipe-insight-meta",), "Add a Job": ("haipipe-insight",),
          "Close a Job": ("haipipe-insight-workflow",), "Close the Job": ("haipipe-insight-workflow",),
          "Run the Job": ("haipipe-insight-workflow",), "Propose a cut": ("haipipe-insight-question",),
          "Propose questions": ("haipipe-insight-question",), "Update the coverage": ("haipipe-insight-check",),
          "Draw a track": ("haipipe-insight-check",), "Check consistency": ("haipipe-insight-knowledge",),
          "Pool or split": ("haipipe-insight-knowledge",), "Ask a Block question": ("haipipe-report",),
          "Write the report": ("haipipe-report",), "Check a report": ("haipipe-report",),
          "Write the counsel": ("haipipe-insight-wisdom",), "Draft the handoff": ("haipipe-insight-wisdom",),
          "Draw the question map": ("haipipe-insight",), "Run a partition": ("haipipe-insight",),
          "Check alignment": ("haipipe-insight-check",), "Add a topic": ("haipipe-studio",),
          "Open the release ↗": ("haipipe-insight",), "Open the Prototype Block ↗": ("haipipe-insight",),
          "Write a report": ("haipipe-insight-data", "haipipe-insight-information", "haipipe-insight-knowledge"),
          "Write the overall report": ("haipipe-insight",), "Write the Data report": ("haipipe-insight-data",), "Write the Information report": ("haipipe-insight-information",),
          "Write the Knowledge report": ("haipipe-insight-knowledge",), "Write the Wisdom report": ("haipipe-insight-wisdom",),
          "Compare with jNN": ("haipipe-insight-knowledge",)}


# each button named by the Run it makes (haipipe-run ref/run-types-by-space.md rule 6; b11 s21's names);
# a hard Run keeps its rNN_ name. Its words stay as what it does, the small line under the button.
RUNS = {"Add a data version": "run-add-version-<d>vM", "Add a Job": "run-add-<jNN>", "Close a Job": "run-close-<jNN>",
        "Close the Job": "run-close-<jNN>", "Run the Job": "run-launch-<jNN>", "Propose a cut": "run-propose-cut-<slug>",
        "Propose questions": "run-propose-<jNN>", "Update the coverage": "run-coverage", "Draw a track": "run-track-<q>",
        "Check consistency": "run-consistency-<jA>-<jB>", "Pool or split": "run-pool-<tNN>",
        "Ask a Block question": "run-ask-<qNN>", "Write the report": "run-report-<qNN>",
        "Write the counsel": "run-write-counsel", "Draft the handoff": "run-draft-handoff",
        "Draw the question map": "run-map-questions", "Run a partition": "rNN_<partition>",
        "Check alignment": "run-check-alignment-<tNN>", "Add a topic": "run-draw-<sNN>", "Write a report": "run-write-<tNN>",
        "Write the Data report": "run-write-<tNN>", "Write the Information report": "run-write-<tNN>",
        "Write the Knowledge report": "run-write-<tNN>", "Write the Wisdom report": "run-write-<tNN>",
        "Write the overall report": "run-overall-<jNN>"}


def _kind(label: str, prompt: str, *skills: str, rows=(), run: str = "") -> dict:
    """A Runs-panel kind; `rows` are its past runs (run_id, status, target, result), newest last; its
    skills default to the button's owner (SKILLS). The button shows the Run it makes (`run`, else RUNS),
    its words kept as `doing`; a link that opens a file (… ↗) makes no Run and keeps its words."""
    owner = skills or SKILLS.get(label) or (SKILLS["Compare with jNN"] if label.startswith("Compare with ") else ())
    name = run or RUNS.get(label) or ("run-compare-" + label.split()[-1] if label.startswith("Compare with ") else "")
    return {"label": name or label, "doing": label if name else "", "prompt": prompt, "skills": list(owner),
            "rows": list(rows)}


# the run cards are the one source of each button's Run, skill, agent, sign and prompt (b11 s21 step 2,
# 261008): haipipe-insight-workflow/ref/run-cards.md, read through its own reader run_cards.py
from host_paths import skill_dir  # noqa: E402
_CARDS_DIR = skill_dir("haipipe-insight-workflow") / "scripts"   # wherever it lives: a skill, or a part of its door
_CARDS: dict = {}
ALIAS = {"Write a report": ("Write the Data report", "Write the Information report", "Write the Knowledge report",
                            "Write the Wisdom report")}


def run_cards() -> list:
    """Every insight run card, read again only when run-cards.md changes; [] when the skill is absent."""
    try:
        if str(_CARDS_DIR) not in sys.path:
            sys.path.insert(0, str(_CARDS_DIR))
        import run_cards as RC
        st = RC.CARDS.stat()
    except (ImportError, OSError):
        return []
    key = (st.st_mtime_ns, st.st_size)
    if _CARDS.get("key") != key:
        _CARDS.update(key=key, cards=RC.cards(), run_name=RC.run_name)
    return _CARDS["cards"]


def _card_kind(card: dict, fill: dict, rows=()) -> dict:
    """A Runs-panel kind from its card: the button shows the Run (its `<NN>` filled where the screen knows
    it), its words as `doing`; the prompt names the agent and what a person signs, as design's do."""
    name, prompt = _CARDS["run_name"](card) or card["label"], card["prompt"]
    for k, v in fill.items():
        name, prompt = name.replace(k, v), prompt.replace(k, v)
    if card["agent"] and card["agent"] != "none":
        prompt = f'Run with {card["agent"]}. {prompt}'
    if card["signs"] and card["signs"] != "none" and f'I sign {card["signs"]}' not in prompt:   # once, not twice
        prompt += f' I sign {card["signs"]}.'
    return {"label": name, "doing": card["label"], "prompt": prompt, "skills": [card["skill"]] if card["skill"] else [],
            "rows": list(rows)}


_NEXT: dict = {}  # {folder: (time, line)} · next_run reads every run card of a Job, so a minute's reuse


def _next_line(folder: Path) -> str:
    """One quiet line at the top of a level's Runs Space: where it stands and the Run to press next, from
    haipipe-insight-workflow's next_run.py (reads files only); its owner skill from the card. '' if absent."""
    import time
    hit = _NEXT.get(str(folder))
    if hit and time.time() - hit[0] < 60:
        return hit[1]
    line = _next_now(folder)
    _NEXT[str(folder)] = (time.time(), line)
    return line


def _next_now(folder: Path) -> str:
    try:
        if str(_CARDS_DIR) not in sys.path:
            sys.path.insert(0, str(_CARDS_DIR))
        import next_run as NR
        import run_cards as RC
        got = NR.state(Path(folder))                 # None: not an insight Prototype, release, Board, Job or Task
        if not got:
            return ""
        st, nxt = got
        card = RC.card_for(nxt) if nxt.startswith(("run-", "r")) else None
    except Exception:  # noqa: BLE001 · a missing or failing helper leaves the screen as it was
        return ""
    skill = f' · {esc(card["skill"])}' if card and card.get("skill") else ""
    return f'<p class=mut>next: <code>{esc(nxt)}</code>{skill} · {esc(st)}</p>'


def _carded(spaces: dict, level: str, views: dict, fill: dict | None = None, keep=None) -> dict:
    """Each Space's buttons from the run cards of (level, Space) shown on the open view (a card with no views
    shows on every view, and every card on "All"); a button the screen drew keeps its past runs, and one no
    card names (a ↗ link, Add a topic) stays after the cards. `keep(card)` drops a card the screen hides."""
    cards = run_cards()
    if not cards:
        return spaces
    for sname, sp in spaces.items():
        own = [c for c in cards if c["level"] == level and c["space"] == sname and (keep is None or keep(c))]
        if not own:
            continue
        view = str(views.get(sname, "")).lower().replace(" ", "-")
        shown = [c for c in own if not c["views"] or view in ("", "all") or view in c["views"]]
        drawn = {}
        for k in sp.run_types:
            words = k.get("doing") or k["label"]
            if words.startswith("Compare with "):
                words = "Compare with the Job before"
            for w in ALIAS.get(words, (words,)):
                drawn.setdefault(w, k)
        out = [_card_kind(c, fill or {}, (drawn.get(c["label"]) or {}).get("rows", ())) for c in shown]
        named = {c["label"] for c in own} | {"Write a report"}
        out += [k for k in sp.run_types
                if (k.get("doing") or k["label"]) not in named and not (k.get("doing") or "").startswith("Compare with ")]
        sp.run_types = tuple(out)
    return spaces


def _rows(runs: list, root: Path, *types: str) -> list:
    """The panel rows of these runs: by type (a soft run's), or by kind (hard)."""
    out = []
    for r in runs:
        if types and r.get("type") not in types and r.get("kind") not in types:
            continue
        res = r["report"] or (r["path"] / "run.yaml")
        out.append({"run_id": r["run"], "status": r.get("status", ""), "target": r.get("target", ""),
                    "result": rel(res, root) if Path(res).exists() else ""})
    return out


def _st(state: str) -> str:
    s = str(state or "—")
    low = s.lower()
    cls = ("st-ok" if low in OK or low.split(" ")[0] in OK or s.startswith("✅") else
           "mut" if low in QUIET else "st-warn")
    return f"<span class={cls}>{esc(s)}</span>"


def _fold(title: str, meta: str, body: str, opened: bool = False) -> str:
    return (f'<details class=topic{" open" if opened else ""}><summary><b>{esc(title)}</b>'
            f'<span class=topic-meta>{esc(meta)}</span></summary><div style="padding:8px 14px">{body}</div></details>')


def _chip(text: str, cls: str = "chip") -> str:
    return f"<span class={cls}>{esc(text)}</span>"


def run_url(rundir: Path, root: Path) -> str:
    return "/_board/insight-run?run=" + rel(Path(rundir), root)


def _run_link(run: dict, root: Path, text: str = "") -> str:
    """↗ a hard Run in the pop-out, as a run page (its report, figures, tables, receipt); any other
    run opens its file in the page reader."""
    path = Path(run.get("path") or "")
    if run.get("kind") == "hard" and (path / "run.yaml").is_file():
        return pop(run_url(path, root), run["run"], (text or run["run"]) + " ↗")
    return _open(run.get("report") or (path / "run.yaml"), root, run["run"], text or run["run"])


def page_link(folder: Path, root: Path) -> str:
    """A page's focus view (a Prototype release, a Task): the frame's own route."""
    from urllib.parse import urlencode
    return "/_board/workbench?" + urlencode({"path": rel(Path(folder), root), "layout": "focus"})


def open_url(path: Path, root: Path) -> str:
    """Where a file or folder opens in the pop-out (round 2 walk, 261108: a .txt, .py, .yaml or a folder sent to the
    Markdown reader showed a 404): Markdown in the page reader; any other file as itself; a page folder (it has a
    face) as its focus page; another folder as its first file."""
    from live import frame as F
    path = Path(path)
    if path.is_dir():
        if F.face(path) is not None:
            return page_link(path, root)
        first = next((q for q in sorted(path.iterdir()) if q.is_file() and not q.name.startswith((".", "_"))), None)
        return open_url(first, root) if first is not None else page_link(path.parent, root)
    return reader(path, root) if path.suffix.lower() in (".md", ".markdown") else F._file_url(path, root)


def _open(path: Path | None, root: Path, label: str, text: str = "") -> str:
    """↗ a file in the frame's pop-out: Markdown in the page reader, any other file as itself (open_url)."""
    if not path or not Path(path).exists():
        return esc(text or label)
    return pop(open_url(Path(path), root), label, (text or label) + " ↗")


def second_row(href, space: str, first: str, options: tuple, current: str, label: str) -> str:
    """A Space's second row of buttons, in the frame's own tab row look; each keeps the first choice."""
    tabs = "".join(f'<a class="tab{" on" if o == current else ""}" href="{esc(href(space, f"{first}/{o}"))}">{esc(o)}</a>'
                   for o in options)
    return f'<nav class="row subs"><span class=mut style="margin-right:8px">{esc(label)}:</span>{tabs}</nav>'


def split(sub: str, firsts: tuple, seconds: tuple) -> tuple:
    a, _, b = (sub or "").partition("/")
    return (a if a in firsts else firsts[0]), (b if b in seconds else seconds[0])


def _qwr_head(work: str, report: str = "Report · its page") -> str:
    return (f'<div class="q-row q-head-row"><div>Logic · the question</div><div>{esc(work)}</div>'
            f'<div>{esc(report)}</div></div>')


def _qwr(logic: str, work: str, report: str, rid: str = "") -> str:
    return (f'<div class=q-row{(" id=" + esc(rid)) if rid else ""}><div class=q-l>{logic}</div>'
            f'<div class=q-w>{work}</div><div class=q-r>{report}</div></div>')


def _by_level(rows: dict, head: str, empty: str = "No question at this DIKW level.", links: dict | None = None,
              tabs: str = "", words: dict | None = None) -> str:
    """rows: {level letter: [row html]} -> one header row, then a closed row per DIKW level, as the old
    board laid them (JL 261008): "Data questions 5", its 'may say' line, and on the right a link to where
    that level's questions are kept (`links`: {letter: html}). A level opens to its question rows.
    With `tabs` (the focus page's id for them): side tabs instead, a level's name on the left with its state word
    (`words`: {letter: word}), no count in a label (haipipe-ui: one kind of tabs, labels carry no counts; 261106)."""
    if tabs:
        from live.ui_parts import _side_tabs
        lvs = [(lv, name, says) for lv, name, says in LEVELS if rows.get(lv)]
        if not lvs:
            return f"<p class=mut>{esc(empty)}</p>"
        return _side_tabs(tabs, [(f"{name}", (words or {}).get(lv, "")) for lv, name, _ in lvs],   # no grey "may say"
                          [f'<div class=q-table>{"".join(rows[lv])}</div>' for lv, _, says in lvs])   # line (round 1)
    out = []
    for lv, name, says in LEVELS:
        if not rows.get(lv):
            continue
        right = (links or {}).get(lv, "")
        out.append(f'<details class=topic><summary><b>{esc(name)} questions</b> '
                   f'<span class=topic-meta>{len(rows[lv])}</span>'
                   + (f'<span class=lv-link>{right}</span>' if right else "")
                   + f'</summary><div class=q-table>{head}{"".join(rows[lv])}</div></details>')
    return f'<div class=dikw>{"".join(out)}</div>' if out else f"<p class=mut>{esc(empty)}</p>"


def _release_links(rel_dir, root: Path, label: str = "") -> dict:
    """Each DIKW level's link to where its questions are kept: the Prototype release, in the workbench."""
    if not rel_dir or not Path(rel_dir).is_dir():
        return {}
    url = "/_board/workbench?path=" + rel(Path(rel_dir), root)
    name = label or Path(rel_dir).name
    return {lv: pop(url, f"{name} · {word.lower()} questions", f"{name} · {word.lower()} questions ↗")
            for lv, word, _ in LEVELS}


OPS = {"eq": "=", "ne": "≠", "lt": "<", "lte": "≤", "gt": ">", "gte": "≥", "isin": "in", "notin": "not in"}


def _where(p: dict) -> str:
    """A cut's filter in words: `patient_gender = M · age ≤ 35`; a list of conditions or a plain string."""
    w = p.get("where")
    if isinstance(w, list):
        conds = [" ".join([str(c.get("column", ""))] + [f"{OPS.get(k, k)} {v:g}" if isinstance(v, float) else f"{OPS.get(k, k)} {v}"
                                                         for k, v in c.items() if k != "column"])
                 if isinstance(c, dict) else str(c) for c in w]
        return " · ".join(conds) or "every row"
    return str(w or "") or ("across " + ", ".join(p.get("of") or []) if p.get("of") else "every row")


WORDS = {"young", "old", "older", "midlife", "middle", "adult", "senior", "teen", "elder"}   # a cut's prefix word


def _label(name: str) -> str:
    """A cut's button: `youngmale` -> `Young male`, `full` -> `Full`; a name with other characters stays."""
    if not re.fullmatch(r"[a-z]+", name or ""):
        return name
    splits = [(name[:-len(sex)], sex) for sex in ("female", "male") if name.endswith(sex) and len(name) > len(sex)]
    known = [x for x in splits if x[0] in WORDS]
    pre, sex = (known or splits or [(name, "")])[0]
    return f"{pre.capitalize()} {sex}".strip()


def _part_names(parts: list) -> tuple:
    return tuple(_label(p["name"]) for p in parts if p.get("name")) or ("Full", "Cross")


def _part_key(label: str) -> str:
    return label.lower().replace(" ", "") if re.fullmatch(r"[A-Za-z ]+", label or "") else label


# ── a question's row, Question │ Work │ Report, in the old board's richer style (JL 261008) ─────
STEP = {"compute": "🧮 Compute", "cite": "📎 Reuse", "reuse": "📎 Reuse", "answer": "⚓ Answer", "judge": "⚓ Answer"}
LEVEL_WORD = {"X": "Executive", "D": "Data", "I": "Information", "K": "Knowledge", "W": "Wisdom"}
MARK = {"ok": "✅", "refused": "🚫", "failed": "❌", "planned": "⏳", "running": "⏳"}
_SPEC: dict = {}


def _spec(q: dict) -> dict:
    """The question's question.md front matter (name, ask, needs, ...), read once per change."""
    f = q.get("file")
    if not f or not Path(f).is_file():
        return {}
    key = (str(f), Path(f).stat().st_mtime)
    if key not in _SPEC:
        _SPEC[key] = P.front(Path(f))
    return _SPEC[key]


def _leads(report, k: int = 3) -> list:
    """A generated run report's lead lines (each need's point, first), without their table names."""
    if not report or not Path(report).is_file():
        return []
    lines = Path(report).read_text(encoding="utf-8", errors="ignore").splitlines()
    return [re.sub(r"\s*\(`[^`]+`\)$", "", x[2:]) for x in lines if x.startswith("- ")][:k]


def _cap(text: str) -> str:
    return (text[:1].upper() + text[1:]) if text else ""


def _q_logic(qid: str, q: dict, mark: str, root: Path, word: str = "") -> str:
    s = _spec(q)
    more = [(k, s.get(k)) for k in ("ask", "why", "answer") if isinstance(s.get(k), str) and s.get(k)]
    asked = (s.get("partitions") or {}).get("asked") if isinstance(s.get("partitions"), dict) else ""
    more += [("asked on", asked if isinstance(asked, str) else ", ".join(asked))] if asked else []
    body = "".join(f'<p><span class=mut>{esc(k)}:</span> {esc(v)}</p>' for k, v in more)
    cited = sorted({str(n["from"]).split(".")[0] for n in _needs(q) if isinstance(n.get("from"), str)
                    and re.match(r"^[DIKWX]\d+", str(n["from"]))})
    builds = ""
    if cited:
        by = {}
        for c in cited:
            by.setdefault(c[0], []).append(str(int(c[1:])))
        builds = ("<p class=mut>builds on " + "; ".join(f"{LEVEL_WORD[k]} questions {', '.join(v)}" for k, v in by.items())
                  + "</p>")
    from live.ui_parts import _pill
    return (f'<p class=q-head><span class=chip>Question {int(qid[1:])}</span> '
            + (_pill(word) if word else esc(mark)) + '</p>'
            + (f'<p><b>{esc(s.get("name"))}</b></p>' if s.get("name") else "")
            + f'<p>{esc(_cap(s.get("question") or q.get("question") or ""))}</p>' + builds
            + f'<details><summary class=mut>More</summary>{body}<p>{_open(q.get("file"), root, qid, "question.md")}</p></details>')


def _needs(q: dict) -> list:
    """The question's live needs (a retired or superseded one left out), in order."""
    return [n for n in (_spec(q).get("needs") or {}).values() if isinstance(n, dict) and not n.get("retired")]


def _goes(n: dict) -> str:
    """Where a step's result goes, or comes from: its tables, the need it reuses, or the page."""
    if n.get("output"):
        return " · ".join(n["output"])
    if isinstance(n.get("from"), str):
        return f"from {n['from']}"
    if n.get("kind") in ("judge", "answer"):
        return "made on the page"
    return ""


def _q_work(q: dict, trail: list) -> str:
    steps = "".join(f'<li><b>{esc(STEP.get(n.get("kind"), _cap(str(n.get("kind") or "step"))))}</b> · {esc(n.get("what", ""))}'
                    + (f' → <span class=mut>{esc(_goes(n))}</span>' if _goes(n) else "") + "</li>" for n in _needs(q))
    return (f'<details><summary><span class=chip>Task Work</span> <span class=mut>its steps</span></summary>'   # no count
            f'<ol>{steps}</ol></details>'
            + "".join(f'<p class=mut>{line}</p>' for line in trail))


def _takeaway(run: dict) -> str:
    """The takeaway of a question on one cut: its Task face's `takeaways: {<partition>: …}`, written by
    run-write-<tNN> with the Task's page (a part per cut); '' until then."""
    path = Path(run.get("path") or "")
    task = path.parent.parent if path.parent.name == "runs" else None
    if task is None:
        return ""
    got = (P.front(task / f"{task.name}.md").get("takeaways") or {})
    return str(got.get(run.get("partition"), "") or "") if isinstance(got, dict) else ""


def _q_report(name: str, run, root: Path, cut: str, extra: str = "") -> str:
    """The Report cell: the takeaway on this cut (JL 261008: not the numbers, what they add up to); the
    numbers stay one click away, in a fold and on the run page."""
    if not run:
        return f'<p class=mut>Not asked on this cut</p>{extra}'
    state = str(run.get("status") or "—")
    if "answer" in run:                                    # a carried board: the cut's answering page
        title = _open(run["report"], root, run["run"], run["answer"] or "the page") if run["report"] else esc(state)
        return f'<p class=q-head><b>{title}</b></p><p class=mut>{esc(run.get("how-sure") or "")}</p>{extra}'
    n = run.get("n")
    rows = f"{n:,} rows" if isinstance(n, int) else f"{n or '—'} rows"
    if state != "ok":
        word = {"refused": "Refused", "failed": "Failed", "planned": "Not run yet"}.get(state, _cap(state))
        return (f'<p>{_st(word)} · {_run_link(run, root)}</p>'
                + (f'<p class=mut>{esc(run.get("reason") or "")}</p>' if run.get("reason") else "") + extra)
    take = _takeaway(run)
    lead = (f'<p class=q-head>{esc(take)}</p>' if take else
            f'<p class=mut>Takeaway not written yet (run-write-{esc(Path(run["path"]).parent.parent.name[:3])})</p>')
    leads = _leads(run.get("report"))
    nums = (f'<details class=q-more><summary class=mut>the numbers · {_run_link(run, root)} · {esc(rows)}</summary>'
            + "".join(f"<p>{esc(_cap(x))}</p>" for x in leads) + "</details>")
    return lead + nums + extra


# ── the Overall Report: a Job's Executive answers as one document to read (JL 261012) ─────────────
OVERALL = "Overall Report"
CITE = re.compile(r"\(([DIKWX]\d\d) · (t\d+)\)")


def _executive(j: dict) -> list:
    """The Job's Executive Tasks (X01, X02, ...), in question order; [] when its release asks none."""
    return sorted((t for t in j["tasks"] if t["qid"][:1] == "X"), key=lambda t: t["qid"])


def _sections(page) -> list:
    """A Task page's body as [(heading, markdown)]: its `# ` title and its **The ask** line left out, since the
    report shows the question itself."""
    text = Path(page).read_text(encoding="utf-8") if page and Path(page).is_file() else ""
    text = text.split("---", 2)[2] if text.startswith("---") else text
    out, head, buf = [], "", []
    for line in text.splitlines() + ["## "]:
        if line.startswith("## "):
            if "\n".join(buf).strip():
                out.append((head, "\n".join(buf)))
            head, buf = line[3:].strip(), []
        elif not line.startswith(("# ", "**The ask**")):
            buf.append(line)
    return out


def _cites(body: str, j: dict, root: Path) -> str:
    """Each `(K01 · t30)` in a rendered page a link to that Task's page, in the pop-out."""
    tasks = {t["name"].split("_", 1)[0]: t for t in j["tasks"]}

    def link(m):
        t = tasks.get(m.group(2))
        return m.group(0) if not t else "(" + pop("/_board/insight-run?answer=" + rel(Path(t["path"]), root),
                                                  f'{t["name"]} · the page', f"{m.group(1)} · {m.group(2)}") + ")"
    return CITE.sub(link, body)


def _fig_png(part: Path, j: dict, qid: str, name) -> Path:
    """An Executive figure as ref/overall_report.py draws it: under its Task's part of the Job's delivery
    (delivery/<job>/<tNN_X..>/), else the older delivery/<job>/figures/."""
    t = next((t for t in j["tasks"] if t["qid"] == qid), None)
    here = part / t["name"] / f"{qid}-{name}.png" if t else None
    return here if here and here.is_file() else part / "figures" / f"{qid}-{name}.png"


def _figure(qid: str, spec: dict, part: Path, j: dict, root: Path) -> str:
    """One figure an Executive page names (`figures:`), as ref/overall_report.py drew it into the Board's
    delivery/<job>/figures/ (JL 261013: "figures to show it to quickly get the outcome"): its outcome as a
    heading, the picture (a click opens it full size), and the answer it reads as a link."""
    title = esc(spec.get("title") or spec.get("name") or "")
    png = _fig_png(part, j, qid, spec.get("name"))
    tables = [x.get("table", "") for x in spec["rows"]] if isinstance(spec.get("rows"), list) else [spec.get("table", "")]
    src = ", ".join(dict.fromkeys(f"({m.group(2)} · {m.group(1)})" for t in tables
                                  if (m := re.match(r"^(t\d+)_([DIKWX]\d\d)_", str(t)))))
    if not png.is_file():
        return (f'<p class=rep-lead>{title}</p><p class=mut>Figure not drawn yet: ref/overall_report.py draws it '
                f'from {esc(src) or "its table"}.</p>')
    url = "/" + rel(png, root)
    return (f'<figure class=rep-fig><figcaption>{title}</figcaption><a href="{esc(url)}" target=_blank '
            f'rel=noopener><img src="{esc(url)}" alt="{title}" loading=lazy></a>'
            + (f'<p class=mut>from {_cites(esc(src), j, root)}</p>' if src else "") + "</figure>")


def _overall(j: dict, b: dict, r: dict, root: Path) -> str:
    """The Job's Overall Report (JL 261012: "before the Full, we should have a Overall Report ... we can click and
    read it"): its Executive answers as one document, a section per question from its Task page, each `(K01 · t30)`
    a link to the Task it rests on, its figure under its answer (JL 261013), and the print beside it. Read-only: an
    answer changes on its page, a figure by its page's `figures:` and ref/overall_report.py."""
    from live.page_reader import markdown_html
    xs = _executive(j)
    face = j["path"] / f'{j["name"]}.md'
    title = next((x[2:].strip() for x in face.read_text(encoding="utf-8").splitlines() if x.startswith("# ")),
                 j["name"]) if face.is_file() else j["name"]
    done = sum(bool(t["face"].get("answer")) for t in xs)
    checked = sum(bool(t["face"].get("check")) for t in xs)
    part = b["path"] / "delivery" / j["name"]
    prints = sorted(f for f in part.glob("overall-report.*") if f.is_file()) if part.is_dir() else []
    one = (" · the print: " + " · ".join(f'<a href="/{esc(rel(f, root))}" target=_blank rel=noopener>'
                                            f'{esc(f.suffix[1:].upper())} ↗</a>' for f in prints)) if prints else \
        " · no print yet (ref/overall_report.py)"
    toc, body = [], []
    for n, t in enumerate(xs, 1):
        q = _spec(r["questions"].get(t["qid"], {}))
        name = str(q.get("name") or t["qid"])
        f = t["face"]
        first = next((x for x in f.get("figures") or [] if isinstance(x, dict)), None)
        png = _fig_png(part, j, t["qid"], first.get("name")) if first else None
        toc.append(f'<a href="#overall-{esc(t["qid"])}"><span>{n} · {esc(name)}</span>'
                   + (f'<b>{esc(first.get("title") or "")}</b><img src="/{esc(rel(png, root))}" alt="" loading=lazy>'
                      if png and png.is_file() else f'<b>{esc(f.get("answer") or "not written yet")}</b>') + "</a>")
        parts = []
        for head, md in _sections(t["page"]):
            html_ = _cites(markdown_html(md), j, root)
            parts.append(f'<details><summary>{esc(head)}</summary>{html_}</details>' if head.lower().startswith("what it rests")
                         else (f"<h4>{esc(head)}</h4>" if head and head.lower() != "answer" else "") + html_)
        body.append(f'<section id="overall-{esc(t["qid"])}"><h3>{n}. {esc(name)}</h3>'
                    f'<p class=rep-ask>{esc(_cap(str(q.get("question") or "")))}</p>'
                    + (f'<p class=rep-lead>{esc(f["answer"])}</p>' if f.get("answer") else
                       '<p class=mut>Not written yet: its page answers from the questions below it.</p>')
                    + (f'<p class=mut>How sure: {esc(f["how-sure"])}</p>' if f.get("how-sure") else "")
                    + "".join(_figure(t["qid"], spec, part, j, root) for spec in f.get("figures") or [] if isinstance(spec, dict))
                    + "".join(parts)
                    + f'<p class=mut>{_task_link(t, root)} · {esc(t["qid"])} · {_st(f.get("answer-status") or "open")}'
                      f' · CHECK {esc(f.get("check") or "not yet")}</p></section>')
    return (f'<article class=report-doc><h2>{esc(title)}</h2>'
            f'<p class=mut>{esc(_rlabel(b, j["release"]))} × {esc(_vlabel(b, j["data"]))} · <code>{esc(j["name"])}</code></p>'
            f'<p class=mut>{done} of {len(xs)} answers written · {checked} checked{one}</p>'
            f'<p class=rep-glance-head>At a glance</p><nav class=rep-glance>{"".join(toc)}</nav>{"".join(body)}'
            '<p class=mut>Each answer rests on the Data, Information, Knowledge and Wisdom questions below it; a '
            '(K01 · t30) opens that Task\'s page.</p></article>')


def _overall_tabs(j: dict, b: dict, r: dict, root: Path, eid: str = "ov") -> str:
    """The Job's Overall Report as side tabs (JL 261106, b11 j01 forms: "one Executive question open, its figure
    beside"): each Executive question a tab, its state word on it; the open one's answer, its first figure, the
    other figures small, its page's sections, what it rests on folded; the print one click away above the tabs."""
    from live.page_reader import markdown_html
    from live.ui_parts import _side_tabs
    xs = _executive(j)
    if not xs:
        return ""
    part = b["path"] / "delivery" / j["name"]
    prints = sorted(f for f in part.glob("overall-report.*") if f.is_file()) if part.is_dir() else []
    head = ('<p class=ov-print>The print: ' + " · ".join(              # the pair is the view's; its counts the bar's word
        f'<a href="/{esc(rel(f, root))}" target=_blank rel=noopener>{esc(f.suffix[1:].upper())} ↗</a>' for f in prints)
            + "</p>") if prints else ""
    items, panels = [], []
    for t in xs:
        q = _spec(r["questions"].get(t["qid"], {}))
        f = t["face"]
        figs = [x for x in f.get("figures") or [] if isinstance(x, dict)]
        first = _figure(t["qid"], figs[0], part, j, root) if figs else ""
        small = "".join(f'<a class=ov-thumb data-pop="{esc(x.get("title") or x.get("name") or "")}" href="/{esc(rel(p, root))}" '
                        f'target=_blank rel=noopener><img src="/{esc(rel(p, root))}" alt="" loading=lazy>'
                        f'<span>{esc(x.get("title") or x.get("name") or "")}</span></a>'
                        for x in figs[1:] for p in [_fig_png(part, j, t["qid"], x.get("name"))] if p.is_file())
        parts = []
        for h, md in _sections(t["page"]):
            html_ = _cites(markdown_html(md), j, root)
            parts.append(f'<details><summary>{esc(h)}</summary>{html_}</details>' if h.lower().startswith("what it rests")
                         else (f"<h4>{esc(h)}</h4>" if h and h.lower() != "answer" else "") + html_)
        items.append((f'{t["qid"]} · {q.get("name") or t["name"].split("_", 2)[-1].replace("-", " ")}', page_word(t)))
        panels.append('<div class="report-doc ov-one">'
                      f'<p class=rep-ask>{esc(_cap(str(q.get("question") or "")))}</p>'
                      + (f'<p class=rep-lead>{esc(f["answer"])}</p>' if f.get("answer") else
                         '<p class=mut>Its page answers from the questions below it; it is still to write.</p>')
                      + (f'<p class=mut>How sure: {esc(f["how-sure"])}</p>' if f.get("how-sure") else "")
                      + first + (f'<div class=ov-thumbs>{small}</div>' if small else "") + "".join(parts)
                      + f'<p class=mut>{_task_link(t, root)} · CHECK {esc(f.get("check") or "not yet")}</p></div>')
    return OV_CSS + head + _side_tabs(eid, items, panels)


OV_CSS = ("<style>.ov-print{font-size:13.5px;margin:0 0 8px}.ov-one{font-size:14.5px;max-width:none}.ov-one>*{max-width:none}.ov-one .rep-fig{max-width:620px}"
          ".ov-thumbs{display:flex;flex-wrap:wrap;align-items:flex-start;gap:10px;margin:4px 0 10px}.ov-thumb{display:block;width:150px;"
          "text-decoration:none;color:var(--mut);font-size:12px}.ov-thumb img{display:block;width:150px;border:1px solid "
          "var(--line);border-radius:6px;background:#fff}</style>")


def _board_overall(b: dict, root: Path, href) -> str:
    """The Board's Overall Report: its latest Job's, with the earlier Jobs' a click away."""
    jobs = [j for j in b["jobs"] if _executive(j)]
    j = jobs[-1]
    earlier = (" · earlier Jobs: " + ", ".join(_job_link(href, o) for o in jobs[:-1])) if jobs[1:] else ""
    return (f'<p class=mut>The latest Job\'s report, {_job_link(href, j)}{earlier}.</p>'
            + _overall(j, b, P.release(b["prototype"], j["release"]), root))


# ── the Board ───────────────────────────────────────────────────────────────────────────────────
def board_spaces(block: Path, root: Path, sub: str, href) -> dict:
    b = P.board(block)
    proto = b["prototype"]
    latest = proto["releases"][-1] if proto["releases"] else {"partitions": [], "name": "", "questions": {}}
    parts = _part_names(latest["partitions"])
    prel = rel(proto["path"], root) if proto["path"].exists() else str(b["face"].get("prototype", ""))
    desc = ("Map", "Prototype", "Dataset", "Partitions")
    d_open = sub if sub in desc else "Map"
    d_html = {"Map": _map, "Prototype": _prototype, "Dataset": _dataset, "Partitions": _partitions}[d_open](b, root, href)
    d_runs = {"Map": (_kind("Add a data version", "Add a data version to the Board {folder}: register the extract, frozen, "
                            "its rows counted per cut (run-add-version-<d>vM)."),
                      _kind("Add a Job", "Add a Job to {folder}: pair a Prototype release with a data version, one clock "
                                         "moved from its neighbour (run-add-<jNN>; the Job folder jNN_prototype-pN-<slug>_data-<d>vM carries the pair).", rows=_rows(b["runs"], root, "add"))),
              "Prototype": (_kind("Open the Prototype Block ↗", f"Open the Prototype Block {prel}: releases are cut there."),),
              "Dataset": (_kind("Add a data version", "Add a data version to the Board {folder} (run-add-version-<d>vM)."),),
              "Partitions": (_kind("Propose a cut", f"Propose a cut for {prel}/proposals/ (run-propose-cut-<slug>): a cut is plan, so it lands "
                                                    "in the next release."),)}[d_open]
    told = [j for j in b["jobs"] if _executive(j)]          # Jobs whose release asks Executive questions
    a_subs = ((OVERALL,) if told else ()) + parts
    a_part, a_read = split(sub, a_subs, READINGS)
    a_html = _board_overall(b, root, href) if a_part == OVERALL else (
        second_row(href, "Audience Report", a_part, READINGS, a_read, "Reading")
        + {"Coverage": _coverage, "Tracks": _tracks, "Consistency": _consistency, "Findings": _findings}[a_read](
            b, root, _part_key(a_part), href))
    a_runs = {"Coverage": (_kind("Update the coverage", "Update the coverage of {folder}: what each Job asked and answered "
                                 "(run-coverage, reads the Jobs' receipts, never data).", rows=_rows(b["runs"], root, "coverage")),),
              "Tracks": (_kind("Draw a track", "Draw a question's track across the Jobs of {folder} (run-track-<q>).", rows=_rows(b["runs"], root, "track")),),
              "Consistency": (_kind("Check consistency", "Check consistency between two Jobs one clock apart in {folder} "
                                    "(run-consistency-<jA>-<jB>).", rows=_rows(b["runs"], root, "consistency")),),
              "Findings": (_kind("Ask a Block question", "Ask a Block question of {folder} (run-ask-<qNN>): a row in board.md ## Questions "
                                 "and reports/qNN_<topic>/."),
                           _kind("Write the report", "Write a Block question's report in {folder}/reports/qNN_<topic>/ "
                                 "(run-report-<qNN>), citing the reading it rests on.", rows=_rows(b["runs"], root, "report")),
                           _kind("Check a report", "Check a Block question's report in {folder} (run-check-<qNN>): every claim cites a Job.", run="run-check-<qNN>"))}[a_read]
    if a_part == OVERALL:                                    # written in the Job; the Board shows the latest one
        a_runs = (_kind("Open the latest Job ↗", f"Open the latest Job {rel(told[-1]['path'], root)}: its Overall Report "
                        f"is written there (run-overall-{told[-1]['name'][:3]})."),)
    rels = tuple(r["name"] for r in proto["releases"])
    w_open = sub if sub in rels else "All"
    r_views = ("All", "soft", "from below")
    r_open = sub if sub in r_views else "All"
    return _carded({
        "Description": Space(html=d_html, subspaces=desc, open=d_open, run_types=d_runs),
        "Audience Report": Space(html=a_html, subspaces=a_subs, open=a_part, run_types=a_runs,
                                 note="The latest Job's report: it is written and checked in that Job." if a_part == OVERALL else ""),
        "Idea Studio": Space(run_types=(_kind("Draw the question map", "Draw the question map of {folder} into studio/ (run-map-questions) "
                                              "(generated from the question files; view only)."),
                                        _kind("Add a topic", "Add or redraw a studio topic of {folder} (run-draw-<sNN>): sNN-<topic>/, a pass per session."))),
        "Work Details": Space(html=_jobs(b, root, href, w_open), subspaces=("All",) + rels, open=w_open,
                              run_types=(_kind("Add a Job", "Add a Job to {folder} (run-add-<jNN>).",
                                               rows=_rows(b["runs"], root, "add")),
                                         _kind("Close a Job", "Close a Job of {folder} after its checks and its comparison "
                                                              "(run-close-<jNN>): frozen.",
                                               rows=_rows([r for j in b["jobs"] for r in j["runs"]], root, "close")))),
        "Runs": Space(html=_next_line(block) + _board_runs(b, root, r_open), subspaces=r_views, open=r_open,
                      run_types=(_kind("Add a Job", "Add a Job to {folder} (run-add-<jNN>).", rows=_rows(b["runs"], root, "add")),
                                 _kind("Update the coverage", "Update the coverage of {folder} (run-coverage).",
                                       rows=_rows(b["runs"], root, "coverage")),
                                 _kind("Check consistency", "Check consistency between two Jobs of {folder}.",
                                       rows=_rows(b["runs"], root, "consistency")))),
        "Delivery": Space(html=delivery_view(block, root, themes()["insight"]) + _handoff(b, root),   # cards (b10 s32-D18)
                          subspaces=("Handoff",), open="Handoff",
                          run_types=(_kind("Write the counsel", "Write the Wisdom counsel of {folder} from the latest Job."),
                                     _kind("Draft the handoff", "Draft the handoff of {folder} for a person to sign."))),
    }, "Block", {"Description": d_open, "Audience Report": "overall-report" if a_part == OVERALL else a_read, "Runs": r_open,
                 "Delivery": "handoff"})


def _job_link(href, j: dict, short: bool = False) -> str:
    """A Job by its folder name, or (short, where its row and column already say the plan and the data) by `j01`."""
    text = j["name"].split("_", 1)[0] if short else j["name"]
    return f'<a href="{esc(href("", "", j["path"]))}" title="{esc(j["name"])}">{esc(text)}</a>'


def _rlabel(b: dict, name: str) -> str:
    """An analysis plan (a release) by its code and words, `AP1 · first ladder`, from the Prototype's release folder."""
    return next((r.get("label") or r["name"] for r in b["prototype"]["releases"] if r["name"] == name), P.plan_code(name))


def _vlabel(b: dict, version: str) -> str:
    """A data freeze (a data version) by its code and words, `F1 · first 5 days`, from board.md versions:."""
    v = next((v for v in b["versions"] if str(v.get("version")) == str(version)), {})
    words = P.freeze_words(v)
    return f"{P.freeze_code(version)} · {words}" if words else P.freeze_code(version)


def _map(b: dict, root: Path, href) -> str:
    """The two clocks crossed: a row per release (its name and slug, its questions, cuts and signature), a
    column per data version (frozen date, rows), a Job in each cell with how far it has got."""
    versions = b["versions"]
    rels = b["prototype"]["releases"] or [{"name": n, "label": n, "questions": {}, "partitions": [], "face": {}}
                                          for n in sorted({j["release"] for j in b["jobs"]})]
    cell = {(j["release"], j["data"]): j for j in b["jobs"]}
    head = "".join(f'<th><b>{esc(_vlabel(b, v.get("version", "")))}</b><br><span class=mut>'
                   + esc(" · ".join(x for x in (f'frozen {v["frozen"]}' if v.get("frozen") else "",
                                                f'{v["rows"]} rows' if v.get("rows") else "") if x))
                   + "</span></th>" for v in versions)
    body = []
    for r in rels:
        signed = r["face"].get("signed") or ""
        facts = (f'{len(r["questions"])} questions · {len(r["partitions"])} cuts<br>'
                 + (f"signed {esc(signed)}" if signed else "not signed yet"))
        cells = [f'<td><b>{esc(r.get("label") or r["name"])}</b><br><span class=mut>{facts}</span></td>']
        for v in versions:
            j = cell.get((r["name"], v.get("version")))
            if not j:
                cells.append('<td>—</td>')                # a new Job is Work's (Jobs › ➕ A new Job), never Report's
                continue
            hard = [x for t in j["tasks"] for x in t["hard"]]
            count = {}
            for x in hard:
                count[x.get("status") or "planned"] = count.get(x.get("status") or "planned", 0) + 1
            runs = ", ".join(f"{n} {s}" for s, n in sorted(count.items(), key=lambda kv: -kv[1]))
            done, asked = written_of(j["tasks"])
            checked = sum(is_written(t) and str(t["face"].get("check") or "").startswith("✅") for t in j["tasks"])
            cells.append(f'<td>{_job_link(href, j, short=True)} · {_st(j["state"])}<br><span class=mut>{len(hard)} runs: '
                         f'{esc(runs) or "none"}<br>{done} of {asked} answered · {checked} checked</span></td>')
        body.append("<tr>" + "".join(cells) + "</tr>")
    return (f'<table class=wf-table style="width:auto"><tr><th>analysis plan \\ data freeze</th>{head}</tr>'
            f'{"".join(body)}</table>')


def _prototype_tabs(b: dict, root: Path, eid: str) -> str:
    """The questions, plan by plan, as side tabs (the focus page; haipipe-ui: one kind of tabs, no count in a label):
    each analysis plan a tab, its state word (signed or not), its questions by DIKW level as tables; the open
    proposals last, their word how many are open."""
    from live.ui_parts import _side_tabs
    proto = b["prototype"]
    items, panels = [], []
    for r in reversed(proto["releases"]):                       # the newest plan first, open
        parts = []
        for lv, name, says in LEVELS:
            qs = [q for q in r["questions"].values() if q["id"][:1] == lv]
            if qs:
                rows = [(f'<b>{esc(q["id"])}</b>', _open(q["file"], root, q["id"], q["question"] or "<question>"),
                         esc(q["change"] or "—")) for q in qs]
                parts.append(f'<p class=pb-lv><b>{esc(name)}</b></p>'
                             + table(("#", "question", "in this plan"), rows))
        signed = str(r["face"].get("signed") or "")
        items.append((r.get("label") or r["name"], f"signed {signed.lstrip('✅ ').strip()}" if signed.startswith("✅")
                      else "not signed yet"))
        panels.append("".join(parts) or "<p class=mut>This plan asks no question yet.</p>")
    open_ = [p for p in proto["proposals"] if str(p.get("state") or "open").lower() in ("open", "proposed", "")]
    if proto["proposals"]:
        items.append(("proposals", f"{len(open_)} open" if open_ else "all triaged"))
        panels.append(table(("proposal", "kind", "from", "state"),
                            [(_open(p["file"], root, p["title"]), esc(p.get("kind", "")), esc(p.get("from", "")),
                              _st(p.get("state", ""))) for p in proto["proposals"]]))
    return _side_tabs(eid, items, panels) if items else ""


def _prototype(b: dict, root: Path, href) -> str:
    proto = b["prototype"]
    out = [f'<p class=mut>The questions live in the Prototype Block: {esc(rel(proto["path"], root)) if proto["path"].exists() else "—"}'
           ' (read only here; releases are cut there).</p>']
    jobs_on = {}
    for j in b["jobs"]:
        jobs_on.setdefault(j["release"], []).append(j["name"])
    for k, r in enumerate(proto["releases"]):
        groups = []                     # one closed fold per DIKW level (JL 261102: "group them by topics ... open and close")
        for lv, name, says in LEVELS:
            qs = [q for q in r["questions"].values() if q["id"][:1] == lv]
            if not qs:
                continue
            rows = [(f'<b>{esc(q["id"])}</b>', _open(q["file"], root, q["id"], q["question"] or "<question>"),
                     esc(q["change"] or "—"), _st(q["signed"] or "—")) for q in qs]
            new = sum((q["change"] or "") == "new" for q in qs)
            signed = sum(bool(q["signed"]) and q["signed"] != "—" for q in qs)
            meta = f'{len(qs)} questions' + (f' · {new} new' if new else "") + (f' · {signed} signed' if signed else "")
            groups.append(f'<details class=topic><summary><b>{esc(name)} questions</b> <span class=topic-meta>{esc(meta)}</span>'
                          f'<span class=lv-link>{esc(says)}</span></summary>'
                          f'<div style="padding:4px 14px 10px">{table(("#", "question", "in this release", "signed"), rows)}</div></details>')
        meta = " · ".join(x for x in (str(r["face"].get("state") or ""), str(r["face"].get("signed") or "not signed yet"),
                                      f'{len(jobs_on.get(r["name"], []))} Job(s)') if x)
        out.append(_fold(f'release {r.get("label") or r["name"]}', meta, f'<div class=dikw>{"".join(groups)}</div>',
                         opened=k == len(proto["releases"]) - 1))
    props = [(_open(p["file"], root, p["title"]), esc(p.get("kind", "")), esc(p.get("from", "")), _st(p.get("state", "")))
             for p in proto["proposals"]]
    out.append(_fold("proposals/", f"{len(props)} open", table(("proposal", "kind", "from", "state"), props)))
    return "".join(out)


def _dataset(b: dict, root: Path, href) -> str:
    on = {}
    for j in b["jobs"]:
        on.setdefault(j["data"], []).append(j)
    rows = []
    for v in b["versions"]:
        f = P.version_folder(v, root)
        man = P.data_folder(f, str(v.get("extract", "")))["manifest"] if f else {}
        rows.append((f'<b>{esc(v.get("version", ""))}</b>', f'<code>{esc(rel(f, root) + "/") if f else "—"}</code>',
                     esc(v.get("frozen") or man.get("end_date") or ""), esc(v.get("rows") or f'{man.get("n_rows", ""):,}'
                                                                           if man.get("n_rows") else v.get("rows", "")),
                     esc(v.get("new", "")), " ".join(_job_link(href, j) for j in on.get(v.get("version"), []))))
    return (f'<p class=mut>One dataset, <b>{esc(b["dataset"])}</b>, its versions frozen outside the Project, one folder each; '
            f'a new version is a new column of the Map. accumulates: {esc(b["accumulates"] or "—")}</p>'
            + table(("version", "folder", "frozen", "rows", "what is new", "Jobs on it"), rows)
            + "".join(_version(v, root, opened=k == len(b["versions"]) - 1) for k, v in enumerate(b["versions"])))


SAMPLE_N, SAMPLE_COLS = 5, 20          # rows drawn; columns shown first when a version names no preview:


def _raw(path: Path, root: Path) -> str:
    """A file under the SPACE as the host serves it (an image, a text file)."""
    from urllib.parse import quote
    return "/" + quote(rel(Path(path), root), safe="/")


def _version(v: dict, root: Path, opened: bool = True) -> str:
    """One data version, read from its folder (JL 261008: "I give you the folder of the data, and you can see
    all the things"): its facts (manifest.json over board.md), then what the folder holds, each in a fold:
    the summary, the columns by group (data_dictionary.csv), a few rows, the figures, the documents, and the
    rest beside it. Read-only; a folder or file whose name starts with `_` is listed, never read."""
    name = str(v.get("version", ""))
    folder = P.version_folder(v, root)
    if not folder or not folder.is_dir():
        return _fold(f"{name} · its folder", "not on this machine",
                     f'<p class=mut>{esc(v.get("folder") or v.get("extract") or "no folder: or extract: in board.md")} '
                     'is not here.</p>', opened)
    d = P.data_folder(folder, str(v.get("extract", "")))
    m = d["manifest"]
    span = (" to ".join(str(x) for x in (m.get("start_date"), m.get("end_date")) if x)
            if m.get("start_date") else (f'to {m["end_date"]}' if m.get("end_date") else ""))
    facts = [(k, val) for k, val in (
        ("folder", f'<code>{esc(rel(folder, root))}/</code>'),
        ("the data", f'<code>{esc(d["data"].name)}</code>' if d["data"] else '<span class=st-warn>no single data file</span>'),
        ("rows · columns", esc(f'{m["n_rows"]:,} · {m.get("n_cols", "—")}' if m.get("n_rows") else v.get("rows", ""))),
        ("dates", esc(span)), ("frozen", esc(v.get("frozen", ""))), ("what is new", esc(v.get("new", ""))),
        ("made from", esc(" · ".join(str(x) for x in (m.get("source_set"), m.get("external_version")) if x))),
        ("built", esc(str(m.get("build_date") or "")[:10]))) if val]
    parts = [table(("fact", "value"), facts)]
    if d["summary"]:
        parts.append(_fold("summary", "cohort_summary.txt", f'<pre style="margin:0">{esc(d["summary"].strip())}</pre>', True))
    if d["dictionary"]:
        groups = {}
        for c in d["dictionary"]:
            groups.setdefault(c.get("group") or "—", []).append(c)
        rows = [(f'<b>{esc(g)}</b>' if i == 0 else "", f'<code>{esc(c.get("name", ""))}</code>', esc(c.get("dtype", "")),
                 esc(c.get("null_pct", "")), esc(c.get("n_unique", "")), esc(c.get("notes", "")))
                for g, cs in groups.items() for i, c in enumerate(cs)]
        parts.append(_fold("columns", f'{len(d["dictionary"])} in {len(groups)} groups · data_dictionary.csv',
                           table(("group", "column", "type", "null %", "distinct", "notes"), rows)))
    hide = tuple((m.get("groups") or {}).get("identity") or ())
    parts.append(_sample(v, d["data"], hide))
    if d["figures"]:
        thumbs = "".join(f'<a data-pop="{esc(f.name)}" href="{esc(_raw(f, root))}" target=_blank rel=noopener '
                         f'style="display:inline-block;width:220px;margin:0 10px 12px 0;vertical-align:top;text-decoration:none">'
                         f'<img src="{esc(_raw(f, root))}" alt="{esc(f.stem)}" loading=lazy '
                         f'style="width:220px;border:1px solid var(--line)"><br><span class=mut>{esc(f.stem)}</span></a>'
                         for f in d["figures"])
        parts.append(_fold("figures", f'{len(d["figures"])}', thumbs))
    for doc in d["docs"]:
        text = doc.read_text(encoding="utf-8", errors="replace")
        if doc.suffix.lower() == ".md":
            from live.paper import _md_view
            body = _md_view(text)
        else:
            body = f'<pre style="margin:0;white-space:pre-wrap">{esc(text[:20000])}</pre>'
        parts.append(_fold(doc.name, f"{esc(rel(doc, folder))} · a document of the version", body))
    if d["tables"]:
        parts.append(_fold("other tables", f'{len(d["tables"])}', "".join(
            f'<p><a data-pop="{esc(t.name)}" href="{esc(_raw(t, root))}" target=_blank rel=noopener>{esc(t.name)} ↗</a></p>'
            for t in d["tables"])))
    if d["other"]:
        parts.append(_fold("beside it", "listed, not read", "<p class=mut>In the folder but not part of the version "
                           "(a name that starts with _ is someone's work beside it).</p>"
                           + "".join(f'<p><code>{esc(rel(o, folder))}{"/" if o.is_dir() else ""}</code></p>' for o in d["other"])))
    return _fold(f"{name} · what its folder holds", f'{rel(folder, root)}/', "".join(parts), opened)


def _sample(v: dict, data, hide: tuple = ()) -> str:
    """A few rows of a version's data, to show what it looks like (JL 261008): drawn at random with a seed fixed
    per version, so the same rows on every load. One column a row, one sample row a column; the version's
    `preview:` columns (else up to SAMPLE_COLS that differ across the sample) first, the rest folded.
    Identifying columns (the dictionary's identity group, ids, zips, NPI) and free text are never shown."""
    import zlib
    name = str(v.get("version", ""))
    s = P.sample_rows(data, SAMPLE_N, zlib.crc32(name.encode()), hide) if data else {}
    if not s:
        return _fold("a few rows", "not readable here", "<p class=mut>No parquet data file in the folder.</p>")
    vals = dict(zip(s["columns"], zip(*s["rows"]))) if s["rows"] else {}
    picked = [c for c in (v.get("preview") or []) if c in vals]
    first = picked or [c for c in s["columns"] if len(set(vals[c])) > 1][:SAMPLE_COLS]
    rest = [c for c in s["columns"] if c not in first]
    heads = ("column",) + tuple(f"row {i + 1}" for i in range(len(s["rows"])))

    def grid(cols):
        return table(heads, [(f"<code>{esc(c)}</code>",) + tuple(esc(x) for x in vals[c]) for c in cols])
    why = ("the version's preview: columns" if picked else f"up to {SAMPLE_COLS} columns that differ across these rows")
    body = (f'<p class=mut>{len(s["rows"])} of {s["total"]:,} rows, drawn at random (the same {len(s["rows"])} on every load). '
            f'First {esc(why)}; dates to the day. Left out, as identifying or free text: '
            f'{esc(", ".join(s["hidden"])) or "none"}.</p>' + grid(first)
            + (_fold(f"the other {len(rest)} columns", "" if picked else "the same in these rows, or empty", grid(rest)) if rest else ""))
    return _fold("a few rows", f'{len(s["columns"])} columns shown', body)


def _partitions(b: dict, root: Path, href) -> str:
    proto = b["prototype"]
    if not proto["releases"]:
        return "<p class=mut>No release yet: the cuts are defined in the Prototype's release.</p>"
    r = proto["releases"][-1]
    defs = [(f'<b>{esc(p.get("name", ""))}</b>', f'<code>{esc(_where(p))}</code>',
             esc(p.get("why", ""))) for p in r["partitions"]]
    power = (r["thresholds"].get("power") or {})
    names = [p.get("name") for p in r["partitions"] if p.get("name") != "cross"]
    counts = []
    for v in b["versions"]:
        cells = {}
        for j in (j for j in b["jobs"] if j["data"] == v.get("version")):
            for t in j["tasks"]:
                for run in t["hard"]:
                    cells.setdefault(run.get("partition"), run.get("n", "—"))
        counts.append([f'<b>{esc(v.get("version", ""))}</b>'] + [esc(cells.get(n, "—")) for n in names])
    return (f'<p class=mut>Defined in release {esc(r.get("label") or r["name"])} ({esc(rel(r["job"], root))}/partitions.md), part of the plan, '
            f'fixed before any outcome; a new or changed cut is a new release. Power floor: '
            f'{esc(power.get("smallest_effect_pp", "—"))} pp.</p>'
            + table(("partition", "where", "why"), defs)
            + '<p class=mut>Rows per data version (a row per version, a column per partition):</p>'
            + table(["version"] + names, counts))


def _questions(b: dict) -> dict:
    """Every question any release asks on a cut, by id, with the release that asks it last; the Executive ones
    are read in the Overall Report instead."""
    out = {}
    for r in b["prototype"]["releases"]:
        for qid, q in r["questions"].items():
            if qid[:1] != "X":
                out[qid] = dict(q, release=r["name"])
    return out


def newest_task(b: dict, qid: str) -> dict | None:
    """A question's Task in the newest Job that asks it: what the Board's counts read (one count, round 1)."""
    return next((t for j in reversed(b["jobs"]) for t in j["tasks"] if t["qid"] == qid), None)


def _cell(j: dict, qid: str, part: str) -> tuple:
    t = next((t for t in j["tasks"] if t["qid"] == qid), None)
    if not t:
        return None, None
    run = next((r for r in t["hard"] if r.get("partition") == part), None)
    return t, run


def _newest_word(b: dict, qid: str) -> str:
    """A question's mark on the Board, its newest Job's page in its tab's word (round 2: "rename each ✅/· to its
    tab's word"): page written, else page and its state (partial, returned, open), else not asked yet."""
    t = newest_task(b, qid)
    if not t:
        return "not asked yet"
    if is_written(t):
        return "page written"
    if any(_rtype(r) == "write" and str(r.get("status") or "").lower() in ("running", "started") for r in t.get("soft") or []):
        return "page being written"
    return "page " + page_word(t).replace(" · checked", "")


def _coverage(b: dict, root: Path, part: str, href, tabs: str = "", work: bool = False) -> str:
    """What each question found on one cut, Job by Job. With `tabs` (the focus page): side tabs, one per DIKW
    level with its state word, each question a two-part row (the question; what it found); with `work` (the focus
    page's Work) also its steps and its trail through the Jobs (round 2: "the path lines leave Report")."""
    rows, said_n, all_n = {}, {}, {}
    for qid, q in _questions(b).items():
        trail, n, last, said, has_runs, asked = [], 0, None, None, False, 0
        for j in b["jobs"]:
            t, run = _cell(j, qid, part)
            if not t:
                trail.append(f'<span title="{esc(j["name"])}">{esc(j["name"][:3])}</span> · not in its release')
                continue
            asked += 1
            state = run.get("status", "—") if run else t["face"].get("answer-status", "—")
            n += is_written(t)
            last = run or last
            has_runs = has_runs or bool(t["hard"])
            said = t if str(t["face"].get("answer") or "").strip() else said
            ran = (_run_link(run, root) if run
                   else "no run on this cut")
            trail.append(f'<span title="{esc(j["name"])} › {esc(t["name"])}">{esc(j["name"][:3])}</span> ▸ {ran} · '
                         f'{_st(state)} · page {esc(page_word(t))}')
        mark = MARK.get(str((last or {}).get("status")), "·")
        tally = f'<p class=mut>page written in {n} of {asked} Jobs</p>' if asked else ""
        if last is None and said:         # no Run on this cut: what it found where it is asked (a cross test), or
            cuts = ", ".join(dict.fromkeys(str(h.get("partition") or "") for h in said["hard"]))   # from the answers below
            found = (f'<p class=q-head>{esc(str(said["face"]["answer"]))}</p><p class=mut>'
                     + (f"asked on {esc(cuts)}" if cuts else "it cites the answers below it")
                     + f' · {_task_link(said, root)}</p>' + tally)
        elif not has_runs:
            found = '<p class=mut>It cites the answers below it; its page is still to write</p>' + tally
        else:
            found = _q_report(_spec(q).get("name") or qid, last, root, _label(part), tally)
        all_n[qid[:1]] = all_n.get(qid[:1], 0) + 1
        said_n[qid[:1]] = said_n.get(qid[:1], 0) + bool(newest_task(b, qid) and is_written(newest_task(b, qid)))
        if tabs:
            rows.setdefault(qid[:1], []).append(f'<div class="q-row q-two" id=question-{esc(qid)}><div class=q-l>'
                                                f'{_q_logic(qid, q, mark, root, _newest_word(b, qid))}</div><div class=q-r>{found}'
                                                + (_q_work(q, trail) if work else "") + '</div></div>')
        else:
            rows.setdefault(qid[:1], []).append(_qwr(_q_logic(qid, q, mark, root), _q_work(q, trail), found, f"question-{qid}"))
    last = b["prototype"]["releases"][-1] if b["prototype"]["releases"] else {}
    latest = last.get("job")
    if tabs:
        return _by_level(rows, "", links=_release_links(latest, root, last.get("label", "")), tabs=tabs,
                         words={lv: f"{said_n.get(lv, 0)} of {n} written" for lv, n in all_n.items()})
    return _by_level(rows, _qwr_head("Task Work · each Job on this cut", "Report · what it found"),
                     links=_release_links(latest, root, last.get("label", "")))


def _tracks(b: dict, root: Path, part: str, href) -> str:
    rows = {}
    for qid, q in _questions(b).items():
        steps, verdicts = [], []
        for j in b["jobs"]:
            t, run = _cell(j, qid, part)
            if t:
                steps.append(f'{esc(j["name"][:3])} {_st(run.get("status") if run else t["face"].get("answer-status", "—"))}')
            v = (j["vs"].get("rows") or {}).get(qid)
            if v:
                verdicts.append(f'{esc(j["name"][:3])}: {_st(v["status"])}')
        logic = f'<p class=q-head><b>{esc(qid)}</b> {_open(q["file"], root, qid, q["question"] or "<question>")}</p>'
        rows.setdefault(qid[:1], []).append(_qwr(logic, " → ".join(steps) or "<span class=mut>—</span>",
                                                 " · ".join(verdicts) or "<span class=mut>no comparison yet</span>"))
    return ('<p class=mut>Each question Job by Job; along one release the data versions make a trend.</p>'
            + _by_level(rows, _qwr_head("Work · Job by Job", "Report · what each comparison found")))


def _consistency(b: dict, root: Path, part: str, href) -> str:
    rows = {}
    pairs = [j for j in b["jobs"] if j["vs"]]
    for qid, q in _questions(b).items():
        work, tally = [], {}
        for j in pairs:
            v = j["vs"]["rows"].get(qid)
            if not v:
                continue
            tally[v["status"]] = tally.get(v["status"], 0) + 1
            work.append(f'{esc(j["previous"][:3])} → {esc(j["name"][:3])} {_st(v["status"])} <span class=mut>{esc(v["why"])}</span>')
        logic = f'<p class=q-head><b>{esc(qid)}</b> {_open(q["file"], root, qid, q["question"] or "<question>")}</p>'
        rows.setdefault(qid[:1], []).append(_qwr(logic, "<br>".join(work) or "<span class=mut>—</span>",
                                                 " · ".join(f"{esc(k)} {n}" for k, n in tally.items()) or "<span class=mut>—</span>"))
    return ('<p class=mut>Only Jobs one clock apart are compared, so each change has one cause. Each verdict is as the '
            "Job's run-compare wrote it (reports/vs-&lt;prev&gt;.md); the rule for 'held' is still open.</p>"
            + _by_level(rows, _qwr_head("Work · each step between Jobs", "Report · the verdicts")))


def _findings(b: dict, root: Path, part: str, href, tabs: str = "") -> str:
    runs = {r["run"]: r for r in b["runs"]}
    rows = {}
    for rp in b["reports"]:
        num = rp["slug"].split("_")[0]
        level = str(rp.get("level", ""))[:1].upper() or "D"
        run = runs.get(f"run-report-{num}")
        work = (f'{esc(run["run"])} {_st(run.get("status"))}' if run else '<span class=mut>no run yet</span>') \
            + '<p class=mut>reads: the Jobs\' answers</p>'
        logic = f'<p class=q-head><b>{esc(num.upper())}</b> {_open(rp["file"], root, num.upper(), P.front(rp["file"]).get("title") or rp["slug"])}</p>'
        report = f'{_st(rp.get("answer-status", "—"))} · {_open(rp["file"], root, rp["slug"], "the report")}'
        rows.setdefault(level, []).append(_qwr(logic, work, report))
    return (("" if tabs else "<p class=mut>The Block's own questions, a second D · I · K · W over the Jobs' answers; they "
             "live on the Board (board.md, reports/qNN_&lt;topic&gt;/).</p>")
            + _by_level(rows, _qwr_head("Work · the Board's soft run", "Report · what it says"), "No Block question yet.",
                        tabs=tabs, words={lv: f"{len(v)} asked" for lv, v in rows.items()}))


WRITTEN = ("written", "answered", "checked")     # a page is written once any of these (the matrix counts the same)


def _answered(j: dict) -> str:
    out = []
    for lv, _, _ in LEVELS:
        ts = [t for t in j["tasks"] if t["qid"][:1] == lv]
        if ts:
            done = sum(str(t["face"].get("answer-status") or "").lower() in WRITTEN for t in ts)
            out.append(f"{lv} {done}/{len(ts)}")
    return " · ".join(out)


def _jobs(b: dict, root: Path, href, only: str) -> str:
    rows = []
    for j in b["jobs"]:
        if only != "All" and j["release"] != only:
            continue
        rows.append((_job_link(href, j), esc(f'{_rlabel(b, j["release"])} × {_vlabel(b, j["data"])}'),
                     esc(j["moved"] or "—"), esc(_answered(j)), _st(j["state"])))
    out = [table(("Job", "pins", "the clock that moved", "pages written, by DIKW level", "state"), rows)]
    for j in (j for j in b["jobs"] if j["state"] != "closed" and (only == "All" or j["release"] == only)):
        groups = []                     # a closed fold per DIKW level, one short line per Task (JL 261102: "very hard to use")
        for lv, name, _ in LEVELS:
            ts = [t for t in j["tasks"] if t["qid"][:1] == lv]
            if not ts:
                continue
            quick, ran_all = [], 0
            wrote = sum(str(t["face"].get("answer-status") or "").lower() in WRITTEN for t in ts)
            for t in ts:
                tally = {}
                for r in t["hard"]:
                    tally[str(r.get("status") or "—")] = tally.get(str(r.get("status") or "—"), 0) + 1
                cuts = ", ".join(str(r.get("partition")) for r in t["hard"])
                said = (" · ".join(f"{n} {st}" for st, n in tally.items()) + f' <span class=mut title="{esc(cuts)}">'
                        f'({len(t["hard"])} cut{"s" if len(t["hard"]) != 1 else ""})</span>') if t["hard"] else (
                    "<span class=mut>not run</span>" if t["qid"][:1] in RUN_LEVELS else
                    "<span class=mut>cites the answers below it</span>")      # W and X have no Run of their own
                ran_all += bool(t["hard"])
                words = t["name"].split("_", 2)[-1].replace("-", " ")
                quick.append((f'<b>{esc(t["qid"])}</b>', f'<a href="{esc(href("", "", t["path"]))}">{esc(words)}</a>',
                              said, _st(t["face"].get("answer-status") or "—")))
            groups.append(f'<details class=topic><summary><b>{esc(name)} questions</b> '
                          f'<span class=topic-meta>{wrote} of {len(ts)} pages written · {ran_all} with Runs</span></summary>'
                          f'<div style="padding:4px 14px 10px">{table(("#", "question", "runs", "page"), quick)}</div></details>')
        out.append(_fold(f'{j["name"]} · its Tasks', f'{len(j["tasks"])} Tasks', f'<div class=dikw>{"".join(groups)}</div>', opened=True))
    return "".join(out)


def _runs_table(runs: list, root: Path) -> str:
    rows = [(_run_link(r, root), esc(r.get("kind", "")), esc(r.get("type", "")),
             esc(r.get("target", "")), _st(r.get("status")), esc(r.get("passes", ""))) for r in runs]
    return table(("Run", "kind", "type", "target", "status", "passes"), rows)


def _board_runs(b: dict, root: Path, view: str) -> str:
    out = []
    if view in ("All", "soft"):
        out.append(_fold("the Board's own · soft", f"{len(b['runs'])} runs", _runs_table(b["runs"], root), opened=True))
    if view in ("All", "from below"):
        below = [(esc(j["name"]), esc(len(j["runs"])), esc(sum(len(t["hard"]) for t in j["tasks"])),
                  esc(sum(len(t["soft"]) for t in j["tasks"]))) for j in b["jobs"]]
        out.append(_fold("from below · each Job", f"{len(b['jobs'])} Jobs",
                         table(("Job", "its own soft", "its Tasks' hard", "its Tasks' soft"), below), opened=True))
    return "".join(out)


def _handoff(b: dict, root: Path) -> str:
    rows = [(_open(h["file"], root, h.get("counsel", h["file"].stem)), esc(h.get("job", "")), _st(h.get("signed", "—")))
            for h in b["handoffs"]]
    return ('<p class=mut>The signed Wisdom counsel, naming the Job (its analysis plan and data freeze) it came from. '
            'Only a signed counsel leaves this Board.</p>' + (table(("counsel", "from Job", "signed"), rows) if rows else
                                 '<p class=mut>No signed counsel yet.</p>'))


# ── a Job ───────────────────────────────────────────────────────────────────────────────────────
def _band(j: dict, b: dict) -> str:
    moved = {"code": "the code", "data": "the data", "start": "the first Job"}.get(j["moved"], j["moved"] or "—")
    prev = f' · moved from {esc(j["previous"][:3])}: {esc(moved)}' if j["previous"] else f" · {esc(moved)}"
    frozen = ", frozen" if j["state"] == "closed" else ""
    return (f'<p class=mut><code>{esc(_rlabel(b, j["release"]))} × {esc(_vlabel(b, j["data"]))}</code> · '
            f'{esc(j["state"])}{frozen}{prev}</p>')


def job_spaces(jdir: Path, root: Path, sub: str, href) -> dict:
    block = P.job_board(jdir)
    b = P.board(block)
    j = P.job(jdir)
    proto = b["prototype"]
    r = P.release(proto, j["release"])
    band = _band(j, b)
    desc = ("Prototype", "Dataset")
    d_open = sub if sub in desc else "Prototype"
    # no band beside the tab (s12, 261007): the Job's line opens Description › Prototype only
    d_html = (band + _job_prototype(j, r, root)) if d_open == "Prototype" else _job_dataset(j, b, r, root)
    parts = ((OVERALL,) if _executive(j) else ()) + _part_names(r["partitions"])
    a_part, a_period = split(sub, parts, PERIODS)
    prev = j["previous"][:3]
    a_html = _overall(j, b, r, root) if a_part == OVERALL else second_row(
        href, "Audience Report", a_part, PERIODS, a_period, "Period") + (
        _job_current(j, b, r, root, _part_key(a_part)) if a_period == "Current" else _vs_previous(j, root))
    me = j["name"][:3]
    propose = _kind("Propose questions", f"Propose questions from {me} (run-propose-{me}): file each new or changed "
                    "question, and each gap this Job could not answer, to the Prototype's proposals/<slug>.md (kind · "
                    f"DIKW level · from {me} · why). It writes nothing else.", rows=_rows(j["runs"], root, "propose"))
    a_runs = ((_kind("Write the overall report", "Write the Overall Report of {folder} (run-overall-<jNN>): each Executive "
                     "question's page from the answers below it, then its one page (ref/overall_report.py)."),
               _kind("Check a report", "Check an Executive question's page in {folder} (run-check-<tNN>).", run="run-check-<tNN>"))
              if a_part == OVERALL else
              (_kind("Compare with " + prev, f"Compare this Job with {prev} (run-compare-{prev}): it writes "
                     f"reports/vs-{prev}.md, after every check.", rows=_rows(j["runs"], root, "compare")), propose)
              if a_period == "vs previous" and prev else (propose,) if a_period == "vs previous" else
              (_kind("Pool or split", "Run the Cross test of a question in {folder} (rNN_cross): one test of the "
                     "difference."),) if _part_key(a_part) == "cross" else
              (_kind("Write a report", "Write a question's page in {folder}: a part per partition."),
               _kind("Check a report", "Check a question's page in {folder} (run-check-<tNN>).", run="run-check-<tNN>")))
    wf = _work_facts(j)
    w_open = _work_step(sub, j, wf)
    r_views = ("All", "hard", "soft", "launch", "power", "compare", "propose", "close")
    r_open = sub if sub in r_views else "All"
    hard = [x for t in j["tasks"] for x in t["hard"]]
    own = (_kind("Run the Job", "Run the Job {folder} (run-launch): start every Task's hard Runs, one per partition.",
                 rows=_rows(j["runs"], root, "launch")),
           _kind("Run a partition", "Run one question on one partition in {folder} (rNN_<partition>).",
                 rows=_rows(hard, root, "hard")))
    return _carded({
        "Description": Space(html=d_html, subspaces=desc, open=d_open, page=True,   # Dataset: no run, as s12 draws it
                             run_types=(_kind("Open the release ↗", f"Open the release {rel(r['job'], root) if r['job'] else j['release']}: "
                                              "read only here; it is changed in the Prototype Block."),) if d_open == "Prototype" else ()),
        "Audience Report": Space(html=a_html, subspaces=parts, open=a_part, run_types=a_runs),
        "Work Details": Space(html=_work_view(j, b, r, wf, w_open, jdir, root, href), subspaces=WORK_STEPS, open=w_open,
                              run_types=_work_kinds(j, wf, root)),
        "Runs": Space(html=_next_line(jdir) + _job_runs(j, root, r_open), subspaces=r_views, open=r_open,
                      run_types=own + ((_kind("Compare with " + prev, f"Compare this Job with {prev} (run-compare-{prev}).",
                                              rows=_rows(j["runs"], root, "compare")),) if prev else ())
                      + (propose, _kind("Close the Job", "Close the Job {folder} after its checks and the comparison (run-close): frozen.",
                               rows=_rows(j["runs"], root, "close")),)),
        "Idea Studio": Space(run_types=(_kind("Add a topic", "Add or redraw a studio topic of {folder} (run-draw-<sNN>): sNN-<topic>/, a pass per session."),)),
        # page=True: the frame takes this Space's runs and third row as set, even none (frame.lays_out_page)
        "Delivery": Space(html=delivery_view(jdir, root, themes()["insight"]) + _job_delivery(j, b, root),
                          run_types=(), page=True,
                          note="Nothing to run here: the Board's Delivery holds the handoff; the Overall Report's one "
                               "page is printed by haipipe-insight ref/overall_report.py."),
    }, "Job", {"Audience Report": "overall-report" if a_part == OVERALL else "cross" if _part_key(a_part) == "cross" else a_period,
               "Work Details": STEP_KEY[w_open],
               "Runs": r_open},
        {"j<NN>": me, "j<prev>": prev or "j<prev>"},
        keep=lambda c: c["label"] != "Compare with the Job before" or bool(prev))


def _job_prototype(j: dict, r: dict, root: Path) -> str:
    rows = {}
    for t in j["tasks"]:
        q = r["questions"].get(t["qid"], {})
        rows.setdefault(t["qid"][:1], []).append(
            (f'<b>{esc(t["qid"])}</b>', _open(q.get("file"), root, t["qid"], q.get("question") or "<question>"),
             esc(q.get("change") or "—"), " ".join(_chip(f"{k}: {v}") for k, v in (q.get("method") or {}).items())))
    body = "".join(_fold(f"{lv} · {name}", f"{len(rows[lv])}", table(("#", "question", "in this release", "methods"), rows[lv]),
                         opened=True) for lv, name, _ in LEVELS if rows.get(lv))
    defs = [(f'<b>{esc(p.get("name", ""))}</b>', f'<code>{esc(_where(p))}</code>',
             esc(p.get("why", ""))) for p in r["partitions"]]
    power = (r["thresholds"].get("power") or {})
    compare = r["thresholds"].get("compare")
    code = [d for d in ("src", "configs") if r["job"] and (r["job"] / d).is_dir()]
    return (f'<p class=mut>Analysis plan {esc(r.get("label") or r["name"])}: {esc(rel(r["job"], root)) if r["job"] else "—"} (read only).</p>' + body
            + _fold("the cuts, as defined in the release", f"{len(defs)}", table(("partition", "where", "why"), defs))
            + f'<p class=mut>Power floor: {esc(power.get("smallest_effect_pp", "—"))} pp · compare rule: '
              f'{esc(compare) if compare else "not set (still open)"} · shared code: {esc(", ".join(code) or "none")}</p>')


def _job_dataset(j: dict, b: dict, r: dict, root: Path | None = None) -> str:
    v = next((v for v in b["versions"] if v.get("version") == j["data"]), {"version": j["data"]})
    return ((_version(v, root) if root else "")
            + "<p class=mut>Each cut on this version, checked before any outcome (run-power):</p>" + _cut_table(j))


def _cut_table(j: dict) -> str:
    """Each cut's n, power and the questions it refused, from the Job's hard Runs' cards."""
    cuts = {}
    for t in j["tasks"]:
        for run in t["hard"]:
            c = cuts.setdefault(run.get("partition"), {"n": run.get("n", "—"), "power": set(), "refused": []})
            c["power"].add(str(run.get("power", "—")))
            if run.get("status") == "refused":
                c["refused"].append(t["qid"])
    rows = [(f'<b>{esc(p)}</b>', "<span class=mut>— (a test across the cuts)</span>" if p == "cross" else esc(c["n"]),
             esc(" · ".join(sorted(c["power"]))),
             f'<span class=st-warn>{esc(", ".join(c["refused"]))}</span>' if c["refused"] else "<span class=mut>—</span>")
            for p, c in cuts.items()]
    return table(("partition", "n", "power", "refused"), rows)


def _method_chips(q: dict, which: str) -> str:
    m = (q.get("method") or {}).get(which)
    return _chip(f"{which}: {m} ↗") if m else ""


def _job_current(j: dict, b: dict, r: dict, root: Path, part: str) -> str:
    rows = {}
    for t in j["tasks"]:
        if t["qid"][:1] == "X":                              # the Executive answers: the Overall Report's
            continue
        q = r["questions"].get(t["qid"], {})
        run = next((x for x in t["hard"] if x.get("partition") == part), None)
        f = t["face"]
        cites = t["qid"][:1] == "W" and not t["hard"]        # Wisdom reads the answers below
        if cites:
            trail = ['cites the answers below; no run of its own']
        elif run:
            trail = [f'<code>{esc(j["name"])}</code> › <code>{esc(t["name"])}</code> ▸ '
                     f'{_run_link(run, root)} · {_st(run.get("status"))}']
        else:
            trail = ["not asked on this cut"]
        mark = MARK.get(str((run or {}).get("status")), "·") if run else ("retired" if _spec(q).get("retired") else "·")
        page = (f'<p class=mut>{_task_link(t, root)}'
                + (f' · CHECK {esc(f["check"])}' if f.get("check") else "") + "</p>"
                if t.get("page") and f.get("answer") and "answer" not in (run or {}) else "")
        if cites:
            report = (f'<p><span class=chip>Report</span> {_st(f.get("answer-status") or "open")}</p>'
                      f'<p>{esc(f.get("answer") or "the counsel is written on its page, signed by a person")}</p>{page}')
        else:
            report = _q_report(_spec(q).get("name") or t["qid"], run, root, _label(part), page)
        rows.setdefault(t["qid"][:1], []).append(_qwr(_q_logic(t["qid"], q, mark, root), _q_work(q, trail), report,
                                                      f'question-{t["qid"]}'))
    work_head = "Task Work · the difference test" if part == "cross" else f"Task Work · its run on {_label(part)}"
    n = next((x.get("n") for t in j["tasks"] for x in t["hard"] if x.get("partition") == part and x.get("status") == "ok"), None)
    size = "compares the cuts" if part == "cross" else (f"{n:,} rows" if isinstance(n, int) else "")
    head = f'<h3>{esc(_label(part))}{(" · " + esc(size)) if size else ""}</h3>'
    return head + _by_level(rows, _qwr_head(work_head, "Report · what it found"), links=_release_links(r.get("job"), root, r.get("label", "")))


def _vs_previous(j: dict, root: Path, tabs: str = "") -> str:
    """Each answer against the Job before, as its run-compare wrote it. With `tabs` (the focus page): a side tab per
    DIKW level, its word what changed there, each row's status a plain word."""
    vs = j["vs"]
    if not vs:
        return (f'<p class=mut>No comparison yet: run-compare-{esc(j["previous"][:3]) or "&lt;prev&gt;"} writes '
                'reports/vs-&lt;prev&gt;.md after every check.</p>' if j["previous"] else
                '<p class=mut>The first Job: nothing before it to compare with.</p>')
    tally = {s: 0 for s in STATUS}
    for row in vs["rows"].values():
        tally[row["status"]] = tally.get(row["status"], 0) + 1
    summary = " · ".join(f"{n} {s}" for s, n in tally.items())
    chips = " ".join(_chip(f"{s} {tally.get(s, 0)}") for s in STATUS)
    rows, moved = {}, {}
    full = _full_answers(j) if tabs else {}
    for qid, row in vs["rows"].items():
        status = f'<b>{esc(row["status"])}</b>' if tabs else _st(row["status"])
        if str(row["status"]).lower() != "held":
            moved.setdefault(qid[:1], []).append(row["status"])
        if tabs:                                    # each answer whole, from the two Jobs' pages (round 1: never "…")
            before, now = full.get(qid, ("", ""))
            rows.setdefault(qid[:1], []).append(
                f'<div class=vs-q><p class=vs-h><b>{esc(qid)}</b> {status}</p><dl class=vs-ab>'
                f'<dt>{esc(j["previous"][:3])}</dt><dd>{esc(before or row["previous"])}</dd>'
                f'<dt>{esc(j["name"][:3])}</dt><dd>{esc(now or row["this"])}</dd><dt>why</dt><dd>{esc(row["why"])}</dd></dl></div>')
            continue
        rows.setdefault(qid[:1], []).append(_qwr(f'<p class=q-head><b>{esc(qid)}</b></p>',
                                                 f'previous: {esc(row["previous"])}<br>this: {esc(row["this"])}',
                                                 f'{status} <span class=mut>{esc(row["why"])}</span>'))
    said = lambda xs: (f'{xs.count("changed")} changed' if "changed" in xs else xs[0]) if xs else "all held"
    words = {lv: said([str(x).lower() for x in moved.get(lv, [])]) for lv in rows}
    if tabs:                                        # no tally line, no chips, no grey sentence (round 1)
        return VS_CSS + _by_level(rows, "", tabs=tabs, words=words) + f'<p class=vs-file>{_open(vs["file"], root, vs["file"].name)}</p>'
    return (f'<p><b>{esc(summary)}</b> · {_open(vs["file"], root, vs["file"].name)}</p><p>{chips}</p>'
            '<p class=mut>As the Job\'s run-compare wrote it; one clock moved, so "why" names its cause.</p>'
            + _by_level(rows, _qwr_head("Work · the two answers", "Report · status · why"), words=words))


VS_CSS = ("<style>.vs-q{padding:8px 2px;border-bottom:1px solid var(--line)}.vs-q:last-child{border-bottom:0}"
          ".vs-h{margin:0 0 4px;display:flex;gap:10px;align-items:baseline}.vs-ab{display:grid;grid-template-columns:44px minmax(0,1fr);"
          "gap:3px 10px;margin:0;font-size:14px;line-height:1.45}.vs-ab dt{color:var(--muted);font-size:12.5px}.vs-ab dd{margin:0;"
          "overflow-wrap:anywhere}.vs-file{font-size:13px;margin:8px 0 0}</style>")


def _full_answers(j: dict) -> dict:
    """{qid: (the previous Job's answer, this Job's answer)}, whole, from the two Jobs' Task faces; a page not
    written says so."""
    prev = j["path"].parent / j["previous"] if j.get("previous") else None
    before = {t["qid"]: t for t in (P.job(prev)["tasks"] if prev and prev.is_dir() else [])}
    now = {t["qid"]: t for t in j["tasks"]}
    said = lambda t: (str(t["face"].get("answer") or "").strip() if t else "") or ("page to write" if t else "")
    return {q: (said(before.get(q)), said(now.get(q))) for q in set(before) | set(now)}


def _tree(j: dict, root: Path, view: str, href) -> str:
    rows = {}
    for t in j["tasks"]:
        runs = [x for x in t["hard"] + t["soft"] if view == "All" or x.get("kind") == view]
        body = _runs_table(runs, root)
        rows.setdefault(t["qid"][:1], []).append(
            _fold(t["name"], f'{t["face"].get("answer-status", "")} · {len(t["hard"])} hard · {len(t["soft"])} soft',
                  f'<p><a href="{esc(href("", "", t["path"]))}">open its Task tab ↗</a></p>' + body))
    return ''.join(_fold(f"{lv} · {name}", f"{len(rows[lv])}", "".join(rows[lv]), opened=True)
                   for lv, name, _ in LEVELS if rows.get(lv)) or "<p class=mut>No Task yet.</p>"


def _job_runs(j: dict, root: Path, view: str) -> str:
    own = [r for r in j["runs"] if view in ("All", "soft") or r.get("type") == view]
    below = [r for t in j["tasks"] for r in t["hard"] + t["soft"] if view in ("All",) or r.get("kind") == view]
    order = ("Add a Job (Board) → run-launch → run-power → per Task: rNN_&lt;partition&gt; → rNN_cross → run-write → "
             "run-check → run-compare-&lt;prev&gt; (after the checks) → run-propose-&lt;job&gt; (reads the compare) → "
             "run-close (frozen)")
    out = [f"<p class=mut>{order}</p>"]
    if own:
        out.append(_fold("the Job's own · soft", f"{len(own)}", _runs_table(own, root), opened=True))
    if below and view in ("All", "hard", "soft"):
        out.append(_fold("its Tasks'", f"{len(below)}", _runs_table(below, root), opened=view != "All"))
    return "".join(out)


def _job_delivery(j: dict, b: dict, root: Path | None = None) -> str:
    """The Job's part of the Board's delivery/ (its Overall Report on one page, JL 261012), then where its counsel goes."""
    part = b["path"] / "delivery" / j["name"]
    files = sorted(f for f in part.iterdir() if f.is_file()) if part.is_dir() else []
    links = "".join(f'<li><a href="/{esc(rel(f, root))}" target=_blank rel=noopener>{esc(f.name)} ↗</a></li>'
                    for f in files) if root else ""
    out = (f'<p><b>Overall Report</b>: its {len(_executive(j))} Executive answers on one page.</p>'
           f'<ul class=files>{links}</ul>' if files else
           '<p class=mut>No one-page Overall Report yet: ref/overall_report.py prints it from the Executive answers.</p>'
           if _executive(j) else "")
    latest = b["jobs"][-1]["name"] if b["jobs"] else ""
    if any(t["qid"][:1] == "W" for t in j["tasks"]) and j["name"] == latest:
        return out + "<p>This is the latest Job: its Wisdom counsel goes to Board › Delivery › Handoff, naming this Job.</p>"
    return out or "<p class=mut>None of its own: a Job's answers are read by the Board.</p>"


# ── a Job's Work: its steps, each a work panel over its result (b11 s12, 261022) ────────────────
# JL 261022: "how to make it that when the user want, they can open this work panel and work on it". The Job's Work is
# its steps in the order a Job runs, a tab each; a tab's work panel (what the step has, the first card's prompt with
# your notes, what is running, what a person signs) stays folded until opened, its result under it. It copies
# prompts only; nothing here writes.
WORK_STEPS = ("1 · Launch", "2 · Run", "3 · Write", "4 · Check", "5 · Compare", "6 · Close")
STEP_KEY = {s: s.split(" · ")[1].lower() for s in WORK_STEPS}         # a run card's `views` word
OLD_WORK = {"All": "2 · Run", "hard": "2 · Run", "soft": "4 · Check"}    # the Job → Task → Run tree's views
STEP_EMOJI = {"launch": "🚀", "run": "🧮", "write": "✍", "check": "🔍", "compare": "🔁", "close": "🔒"}
WRITTEN = ("written", "answered", "checked")
FINAL = ("ok", "refused")                 # a hard Run's answer; a refusal is an answer
RUN_LEVELS = "DIK"                        # a question with Runs of its own; W and X cite the answers below them
WRITE_ORDER = "DIKWX"                     # pages are written up the DIKW levels, the Executive answers last
WRITE_CARD = {"D": "Write the Data report", "I": "Write the Information report", "K": "Write the Knowledge report",
              "W": "Write the Wisdom report", "X": "Write the overall report"}


def _rtype(x: dict) -> str:
    """A Run's type: a soft Run's from its name (run-check-alignment-t30 → check-alignment), a hard one's card."""
    m = re.match(r"run-(.+?)-[jt]\d+", x["run"])
    return m.group(1) if m and x.get("kind") == "soft" else str(x.get("type") or ("partition" if x.get("kind") == "hard" else ""))


def _closed(x: dict) -> bool:
    s = str(x.get("status") or "").lower()
    return s in ("closed", "ok", "done", "signed") or s.startswith("✅")


def is_written(t: dict) -> bool:
    """A question's page is written, the one count every "N of M answered" reads (round 1, 261106: the counts must
    agree): its answer-status says so, it has its answer, and no CHECK returned it (`check: ↩ …`)."""
    f = t.get("face") or {}
    return (str(f.get("answer-status") or "").lower() in WRITTEN and bool(str(f.get("answer") or "").strip())
            and not str(f.get("check") or "").startswith("↩"))


def written_of(tasks: list) -> tuple:
    """(written, asked) over the live Tasks (a retired question is not asked), by is_written."""
    live = [t for t in tasks if str((t.get("face") or {}).get("answer-status") or "").lower() != "retired"]
    return sum(is_written(t) for t in live), len(live)


def page_word(t: dict) -> str:
    """A page's state in a word or two: returned (a CHECK sent it back), else its answer-status, checked when so."""
    f = t.get("face") or {}
    if str(f.get("check") or "").startswith("↩"):
        return "returned"
    return str(f.get("answer-status") or "to write") + (" · checked" if str(f.get("check") or "").startswith("✅") else "")


def _work_facts(j: dict) -> dict:
    """What the Job's steps stand on, from its Tasks' faces and its Runs' cards: the questions still to run, write
    and check, the Job's own Runs by type, and what is running now."""
    live = [t for t in j["tasks"] if str(t["face"].get("answer-status", "")).lower() != "retired"]
    asked = [t for t in live if t["qid"][:1] in RUN_LEVELS]
    ran = [t for t in asked if t["hard"] and all(str(x.get("status")).lower() in FINAL for x in t["hard"])]
    # a page a CHECK returned (its check: line starts ↩) is not written: 3 · Write takes it back with the reason
    returned = [t for t in live if str(t["face"].get("check") or "").startswith("↩")]
    written = [t for t in live if is_written(t)]
    checked = [t for t in written if str(t["face"].get("check") or "").startswith("✅")]
    name = lambda ts: {t["name"] for t in ts}
    own = {}
    for x in j["runs"]:
        own.setdefault(_rtype(x), []).append(x)
    every = [x for t in j["tasks"] for x in t["hard"] + t["soft"]] + j["runs"]
    running = [x for x in every if str(x.get("status")).lower() in ("running", "started")
               or (x.get("kind") == "soft" and str(x.get("status")).lower() == "open")]
    return {"live": live, "asked": asked, "ran": ran, "unrun": [t for t in asked if t["name"] not in name(ran)],
            "failed": [t for t in asked if any(str(x.get("status")).lower() == "failed" for x in t["hard"])],
            "written": written, "unwritten": [t for t in live if t["name"] not in name(written)], "returned": returned,
            "checked": checked, "unchecked": [t for t in written if t["name"] not in name(checked)],
            "own": own, "running": running, "hard": [x for t in j["tasks"] for x in t["hard"]],
            "soft": [x for t in j["tasks"] for x in t["soft"]]}


def _work_states(j: dict, f: dict) -> dict:
    """Each step's chip, from disk: done, or the first step not done is next; the close is a person's, so it reads
    sign once every step before it is done."""
    has = lambda kind: any(_closed(x) for x in f["own"].get(kind, []))
    first = not j["previous"]
    compare = (has("propose") or (not first and (bool(j["vs"]) or has("compare"))))
    st = {"1 · Launch": "done" if has("launch") or f["ran"] else "todo",
          "2 · Run": "done" if not f["unrun"] and not f["failed"] else "todo",
          "3 · Write": "done" if f["live"] and not f["unwritten"] else "todo",
          "4 · Check": "done" if f["written"] and not f["unchecked"] and not f["unwritten"] else "todo",
          "5 · Compare": "done" if compare else "optional" if first else "todo",
          "6 · Close": "done" if j["state"] == "closed" or has("close") else "todo"}
    nxt = next((s for s in WORK_STEPS if st[s] == "todo"), "")
    if nxt:
        st[nxt] = "sign" if nxt == WORK_STEPS[-1] else "next"
    return st


def _work_step(sub: str, j: dict, f: dict) -> str:
    """The tab a link opens: the one it names (an older tree view opens its step), else the step that comes next."""
    sub = OLD_WORK.get(sub, sub)
    if sub in WORK_STEPS:
        return sub
    st = _work_states(j, f)
    return next((s for s in WORK_STEPS if st[s] in ("next", "sign")), WORK_STEPS[-1])


def _card_prompt(label: str, folder: str, me: str, prev: str) -> str:
    """The prompt of the Job › Work Details card named `label`, the Job filled in; '' without the cards."""
    card = next((c for c in run_cards() if c["level"] == "Job" and c["space"] == "Work Details" and c["label"] == label), None)
    if not card:
        return ""
    return _card_kind(card, {"j<NN>": me, "j<prev>": prev or "j<prev>"})["prompt"].replace("{folder}", folder)


def _still(tasks: list, what: str) -> str:
    """The Tasks a prompt names, six at most: a longer list is the step's own Input, which the agent reads too."""
    names = [t["name"] for t in tasks]
    more = f" and {len(names) - 6} more (the step's Input lists them)" if len(names) > 6 else ""
    return f" {what}: {', '.join(names[:6])}{more}." if names else ""


def _names(tasks: list) -> str:
    names = [t["name"] for t in tasks]
    more = f" · and {len(names) - 8} more" if len(names) > 8 else ""
    return (esc(" · ".join(names[:8])) + more) if names else "<span class=mut>none</span>"


def _level_card(title: str, done: int, total: int, body: str, open_: bool = False, chip: str = "") -> str:
    """A result card: its title and how many of its questions are done (or its own `chip`), folded until opened."""
    cls = "st-ok" if total and done == total else "st-warn"
    return (f'<details class="topic work-task"{" open" if open_ else ""}><summary><span class=related-head>'
            f'<b>{esc(title)}</b> <span class="st {cls}">{esc(chip or f"{done} of {total}")}</span></span></summary>'
            f'<div class=work-body>{body}</div></details>')


def _page_link(t: dict, root: Path) -> str:
    return pop("/_board/insight-run?answer=" + rel(Path(t["path"]), root), f'{t["name"]} · the page', t["name"] + " ↗")


def _launch_step(j, b, r, f, root, href, ask):
    launch, power = f["own"].get("launch", []), f["own"].get("power", [])
    record = (", ".join(f'{x["run"]} · {x.get("status", "—")}' for x in launch) if launch else
              "none on disk; its Runs show the Job ran" if f["ran"] else "none yet")
    powered = sum(1 for x in f["hard"] if x.get("power") not in (None, "", "—"))
    rows = [("Pins", esc(f'{_rlabel(b, j["release"])} × {_vlabel(b, j["data"])}')),
            ("Hash", esc(j["face"].get("hash")) if j["face"].get("hash") else "<span class=st-warn>not recorded</span>"),
            ("Launch", esc(record)),
            ("Power", esc(", ".join(f'{x["run"]} · {x.get("status", "—")}' for x in power)) if power else
             esc(f"read inside each Run ({powered} of {len(f['hard'])} carry it)") if f["hard"] else "not measured yet")]
    parts = {x.get("partition") for x in f["hard"]}
    result = (_level_card("The pins", 1 if j["face"].get("hash") else 0, 1, _band(j, b) + _job_prototype_line(r, root), True,
                          "pinned" if j["face"].get("hash") else "no hash")
              + _level_card("Each cut: n, power, refused", 1, 1, _cut_table(j), True, f"{len(parts)} cuts"))
    return rows, [("Prompt", ask("Run the Job"))], result


def _job_prototype_line(r: dict, root: Path) -> str:
    return f'<p class=mut>Analysis plan {esc(r.get("label") or r["name"])}: {esc(rel(r["job"], root)) if r["job"] else "—"} (read only).</p>'


def _run_step(j, b, r, f, root, href, ask):
    ok = sum(1 for x in f["hard"] if str(x.get("status")).lower() == "ok")
    refused = sum(1 for x in f["hard"] if str(x.get("status")).lower() == "refused")
    rows = [("Questions run", f'{len(f["ran"])} of {len(f["asked"])} (the Data, Information and Knowledge questions)'),
            ("Runs on disk", f'{len(f["hard"])} · {ok} ok · {refused} refused'),
            ("Still to run", _names(f["unrun"]))]
    parts = []
    for x in f["hard"]:
        p = x.get("partition") or x["run"].split("_", 1)[-1]
        if p not in parts:
            parts.append(p)
    cards = []
    for lv in RUN_LEVELS:
        ts = [t for t in f["asked"] if t["qid"][:1] == lv]
        if not ts:
            continue
        grid = []
        for t in ts:
            by = {(x.get("partition") or x["run"].split("_", 1)[-1]): x for x in t["hard"]}
            grid.append((f'<a href="{esc(href("", "", t["path"]))}">{esc(t["name"])}</a>',) + tuple(
                pop(run_url(by[p]["path"], root), by[p]["run"], MARK.get(str(by[p].get("status")), "·")) if p in by
                else "<span class=mut>·</span>" for p in parts))
        done = sum(1 for t in ts if t["name"] in {x["name"] for x in f["ran"]})
        cards.append(_level_card(f"{lv} · {LEVEL_WORD[lv]}", done, len(ts), table(("Task",) + tuple(_label(p) for p in parts), grid)))
    cards.append(_level_card("Every Run, by Task", len(f["ran"]), len(f["asked"]), _tree(j, root, "All", href)))
    return rows, [("Prompt", ask("Run a partition") + _still(f["unrun"], "Still to run, or to retire"))], "".join(cards)


def _write_step(j, b, r, f, root, href, ask):
    # a page is ready to write once its own Runs answered (W and X cite the answers below them); the rest wait on 2 · Run
    ran = {t["name"] for t in f["ran"]}
    ready = [t for t in f["unwritten"] if t["qid"][:1] not in RUN_LEVELS or t["name"] in ran]
    waiting = [t for t in f["unwritten"] if t not in ready]
    lv = next((t["qid"][:1] for t in sorted(ready, key=lambda t: WRITE_ORDER.find(t["qid"][:1]))), "")
    rows = [("Pages written", f'{len(f["written"])} of {len(f["live"])}'),
            ("Next DIKW level", esc(f"{lv} · {LEVEL_WORD[lv]}") if lv else "<span class=mut>none ready to write</span>"),
            ("Still to write", _names(ready))] + ([("Returned by CHECK", _names(f["returned"]))] if f["returned"] else []) \
        + ([("Waiting on 2 · Run", _names(waiting))] if waiting else [])
    back = [t for t in f["returned"] if t["qid"][:1] == lv]
    prompts = [("Prompt", ask(WRITE_CARD[lv]) + _still([t for t in ready if t["qid"][:1] == lv], "Still to write")
                + (_still(back, "Returned by CHECK") + " Rewrite each from the reason on its check: line, then empty that "
                   "line." if back else ""))] if lv else []
    done = {t["name"] for t in f["written"]}
    cards = []
    for level in WRITE_ORDER:
        ts = [t for t in f["live"] if t["qid"][:1] == level]
        if ts:
            rows_ = [(_page_link(t, root), _st("↩ returned" if t in f["returned"] else t["face"].get("answer-status") or "open"),
                      esc(t["face"].get("answer") or "—")) for t in ts]
            cards.append(_level_card(f"{level} · {LEVEL_WORD[level]}", sum(t["name"] in done for t in ts), len(ts),
                                     table(("Task", "page", "its answer"), rows_)))
    return rows, prompts, "".join(cards)


def _check_step(j, b, r, f, root, href, ask):
    soft = lambda t, kind: next((x for x in t["soft"] if _rtype(x) == kind), None)
    aligned = sum(1 for t in f["written"] if soft(t, "check-alignment"))
    rows = [("Pages checked", f'{len(f["checked"])} of {len(f["written"])} written'),
            ("Alignment Runs", f'{aligned} of {len(f["written"])}'),
            ("Still to check", _names(f["unchecked"]))]
    prompts = [("Prompt · alignment", ask("Check alignment") + _still(f["unchecked"], "Still to check")),
               ("Prompt · CHECK", ask("Check a report") + _still(f["unchecked"], "Still to check"))]
    done = {t["name"] for t in f["checked"]}
    cards = []
    for level in WRITE_ORDER:
        ts = [t for t in f["written"] if t["qid"][:1] == level]
        if ts:
            cell = lambda x: _run_link(x, root, x["run"]) + " " + _st(x.get("status")) if x else "<span class=mut>—</span>"
            rows_ = [(_page_link(t, root), _st(t["face"]["check"]) if t["name"] in done else _check_form(t, root),
                      cell(soft(t, "check-alignment")), cell(soft(t, "check"))) for t in ts]
            cards.append(_level_card(f"{level} · {LEVEL_WORD[level]}", sum(t["name"] in done for t in ts), len(ts),
                                     table(("Task", "CHECK", "alignment", "its check Run"), rows_)))
    return rows, prompts, "".join(cards) or "<p class=mut>No page is written yet: 3 · Write comes first.</p>"


def _check_form(t: dict, root: Path) -> str:
    """A person's CHECK of one page, folded in its row (JL 261023: "design the work in a way that we human can operate
    this system as well"): read the page ↗ and its Runs, tick that you did, then ✅ Pass or ↩ Return with a reason.
    POST /_board/insight-act writes the page's check: line and a pass of run-check-tNN (insight_act.py)."""
    import json
    body = lambda verdict: esc(json.dumps({"action": "check", "task": rel(Path(t["path"]), root), "verdict": verdict}))
    btn = lambda verdict, word: (f'<button type=button class=work-act data-post="/_board/insight-act" '
                                 f'data-body="{body(verdict)}" data-fields="attest why">{word}</button>')
    return (f'<details class=check-it><summary>not yet · check it</summary><p class=sign-row style="margin:6px 0">'
            f'<label><input type=checkbox name=attest> I read the page and its Runs\' results</label> '
            f'<input name=why placeholder="why, if it goes back" size=24> {btn("pass", "✅ Pass")} {btn("return", "↩ Return")}'
            f'</p></details>')


def _compare_step(j, b, r, f, root, href, ask):
    prev = j["previous"]
    propose = f["own"].get("propose", [])
    rows = [("Job before", esc(prev) if prev else "<span class=mut>none: the first Job</span>"),
            ("Comparison", _open(j["vs"]["file"], root, j["vs"]["file"].name) if j["vs"] else "<span class=mut>not written</span>"),
            ("Proposals filed", esc(", ".join(f'{x["run"]} · {x.get("status", "—")}' for x in propose)) if propose else
             "<span class=mut>none</span>")]
    prompts = ([("Prompt · compare", ask("Compare with the Job before"))] if prev else []) + [
        ("Prompt · propose", ask("Propose questions"))]
    result = _vs_previous(j, root) + (_level_card("Proposals filed", sum(_closed(x) for x in propose), len(propose),
                                                  _runs_table(propose, root), True) if propose else "")
    return rows, prompts, result


def _close_step(j, b, r, f, root, href, ask):
    st = _work_states(j, f)
    waits = [s for s in WORK_STEPS[:-1] if st[s] not in ("done", "optional")]
    close = f["own"].get("close", [])
    rows = [("State", _st(j["state"])), ("Waits on", esc(" · ".join(waits)) if waits else "<span class=st-ok>nothing</span>"),
            ("The close", esc(", ".join(f'{x["run"]} · {x.get("status", "—")}' for x in close)) if close else
             "<span class=mut>not yet: a person signs it</span>")]
    frozen = [("Pages", f'{len(f["checked"])} checked · {len(f["written"])} written · {len(f["live"])} asked'),
              ("Runs", f'{len(f["hard"])} hard · {len(f["soft"]) + len(j["runs"])} soft'),
              ("Comparison", _open(j["vs"]["file"], root, j["vs"]["file"].name) if j["vs"] else "<span class=mut>none</span>")]
    return rows, [("Prompt", ask("Close the Job"))], _level_card("What the close freezes", len(WORK_STEPS) - 1 - len(waits),
                                                                 len(WORK_STEPS) - 1, _kv_table(frozen), True)


def _close_sign(j: dict, st: dict, folder: str) -> str:
    """🙋 Sign the close: a person's own sign once every step before it is done (POST /_board/insight-act, close)."""
    import json
    if j["state"] == "closed":
        return f'<p><span class="st st-ok">✓ closed</span> {esc(j["face"].get("signed") or "")}</p>'
    waits = [s for s in WORK_STEPS[:-1] if st[s] not in ("done", "optional")]
    if waits:
        return (f'<p><b>🙋 Sign the close</b> <button type=button class=work-act disabled>Sign the close</button> '
                f'<span class=mut>it waits on {esc(" · ".join(waits))}</span></p>')
    body = esc(json.dumps({"action": "close", "job": folder}))
    return (f'<p class=sign-row><b>🙋 Sign the close</b> <label><input type=checkbox name=attest> I read what the close '
            f'freezes</label> <button type=button class=work-act data-post="/_board/insight-act" data-body="{body}" '
            f'data-fields="attest">Sign the close</button></p>')


def _kv_table(rows: list) -> str:
    from live.draft_steps import _kv
    return _kv(rows)


WORK_PARTS = {"launch": _launch_step, "run": _run_step, "write": _write_step, "check": _check_step,
              "compare": _compare_step, "close": _close_step}
WORK_RUNNING = {"launch": ("launch", "power"), "run": ("partition", "cross", "pool"), "write": ("write", "overall"),
                "check": ("check", "check-alignment"), "compare": ("compare", "propose"), "close": ("close",)}


def _work_view(j: dict, b: dict, r: dict, f: dict, step: str, jdir: Path, root: Path, href) -> str:
    """One step tab: its work panel (Input, what is running, the prompt with your notes, the sign), folded until
    opened, then its Result."""
    from live.draft_steps import _kv, _part, _prompt_box, _step_box
    key = STEP_KEY[step]
    st = _work_states(j, f)
    folder, me, prev = rel(jdir, root), j["name"][:3], j["previous"][:3]
    rows, prompts, result = WORK_PARTS[key](j, b, r, f, root, href, lambda label: _card_prompt(label, folder, me, prev))
    now = "".join(f'<p class=run-now style="margin:0 0 8px;padding:6px 10px;border:1px solid var(--line);border-radius:3px">'
                  f'⏳ <b>Running now</b> · {_run_link(x, root, x["run"])} <span class=mut>· {esc(x.get("status", ""))}'
                  f'{(" since " + esc(x["started_at"])) if x.get("started_at") else ""}</span></p>'
                  for x in f["running"] if _rtype(x) in WORK_RUNNING[key])
    sign = (_close_sign(j, st, folder) if key == "close" else
            '<p><b>🙋 Or check a page yourself</b>: open its row in the Result below, read the page and its Runs, '
            'then ✅ Pass or ↩ Return with the reason.</p>' if key == "check" else "")
    body = ("<h4>Input</h4>" + _kv(rows) + now
            + "".join(_prompt_box(p, jdir, root, f"job-{key}-{k}", title) for k, (title, p) in enumerate(prompts) if p) + sign)
    return (_part("Operation") + _step_box(f"{STEP_EMOJI[key]} {step}", st[step], body)
            + _part("Result") + (result or "<p class=mut>Nothing here yet.</p>"))


def _work_kinds(j: dict, f: dict, root: Path) -> tuple:
    """The Work Space's buttons before the cards pick them (each keeps its past Runs): the cards of the open step."""
    pick = lambda xs, *kinds: [x for x in xs if _rtype(x) in kinds]
    return (_kind("Run the Job", "", rows=_rows(pick(j["runs"], "launch"), root)),
            _kind("Measure the power", "", rows=_rows(pick(j["runs"], "power"), root)),
            _kind("Run a partition", "", rows=_rows(f["hard"], root)),
            _kind("Pool or split", "", rows=_rows(pick(f["soft"], "pool"), root)),
            _kind("Write a report", "", rows=_rows(pick(f["soft"], "write"), root)),
            _kind("Write the overall report", "", rows=_rows(pick(j["runs"], "overall"), root)),
            _kind("Check alignment", "", rows=_rows(pick(f["soft"], "check-alignment"), root)),
            _kind("Check a report", "", rows=_rows(pick(f["soft"], "check"), root)),
            _kind("Compare with the Job before", "", rows=_rows(pick(j["runs"], "compare"), root)),
            _kind("Propose questions", "", rows=_rows(pick(j["runs"], "propose"), root)),
            _kind("Close the Job", "", rows=_rows(pick(j["runs"], "close"), root)))


# ── a Task ──────────────────────────────────────────────────────────────────────────────────────
def task_spaces(tdir: Path, root: Path, sub: str, href) -> dict:
    jdir = P.task_job(tdir)
    b = P.board(P.job_board(jdir))
    j = P.job(jdir)
    t = P.task(tdir)
    q = P.question_of(b["prototype"], j["release"], t["qid"])
    level = LEVEL_WORD.get(t["qid"][:1], "")
    head = f'<p class=mut><code>{esc(t["qid"])}</code> on {esc(j["name"])} · {esc(level)} · {_st(t["face"].get("answer-status", "—"))}</p>'
    d_views = ("Question", "Records")
    d_open = sub if sub in d_views else "Question"
    a_views = ("Table", "Reading")
    a_open = sub if sub in a_views else "Table"
    r_views = ("All", "hard", "soft")
    r_open = sub if sub in r_views else "All"
    # page=True on each: the frame takes the subspaces and runs as set, so s13's views stand alone
    return _carded({
        "Description": Space(html=head + (_question(q, root) if d_open == "Question" else _records(t, root)),
                             subspaces=d_views, open=d_open, run_types=(), page=True,
                             note="Read only: a change to the question is made in the Prototype."),
        "Idea Studio": Space(run_types=(_kind("Add a topic", "Add or redraw a studio topic of {folder} (run-draw-<sNN>): sNN-<topic>/, a pass per session."),)),
        "Audience Report": Space(html=head + (_task_table(t, q, root) if a_open == "Table" else _task_reading(t, q, root)),
                                 subspaces=a_views, open=a_open, page=True,
                                 run_types=(_kind(f"Write the {level} report", "Write the page of {folder}: a part per partition."),
                                            _kind("Check a report", "Check the page of {folder} (run-check-<tNN>).", run="run-check-<tNN>"))),
        "Work Details": Space(html=head + _task_parts(t, root), subspaces=("Partitions",), open="Partitions", page=True,
                              run_types=(_kind("Run a partition", "Run {folder} on one partition (rNN_<partition>).",
                                               rows=_rows(t["hard"], root, "hard")),
                                         _kind("Check alignment", "Check a run of {folder} against its plan (run-check).",
                                               rows=_rows(t["soft"], root, "check")))),
        "Runs": Space(html=_next_line(tdir) + head + _runs_table([x for x in t["hard"] + t["soft"] if r_open == "All" or x.get("kind") == r_open], root),
                      subspaces=r_views, open=r_open, page=True,
                      run_types=(_kind("Run a partition", "Run {folder} on one partition (rNN_<partition>)."),
                                 _kind("Check alignment", "Check a run of {folder} against its plan (run-check)."))),
        "Delivery": Space(html=head + "<p class=mut>None of its own: its answer goes up as a cite need.</p>",
                          page=True, note="Nothing to run here."),
    }, "Task", {"Audience Report": a_open, "Runs": r_open}, {"t<NN>": t["name"][:3]},
        keep=lambda c: not c["label"].startswith("Write the ") or c["label"] == f"Write the {level} report")


def _question(q: dict, root: Path) -> str:
    fm = q.get("fields") or (P.front(q["file"]) if q.get("file") else {})
    rows = [(esc(k), esc(v if not isinstance(v, dict) else " · ".join(f"{a}: {b}" for a, b in v.items())))
            for k, v in fm.items() if v]
    name = q["file"].name if q.get("fields") and q.get("file") else "question.md"
    return (f'<p><b>{esc(q["id"])}</b> {esc(q.get("question") or "")}</p>'
            f'<p>{_open(q.get("file"), root, q["id"], name)} · read only: a change is a proposal to the Prototype.</p>'
            + table(("field", "value"), rows))


def _records(t: dict, root: Path) -> str:
    rec = sorted((t["path"] / "draft" / "records").glob("*.md")) if (t["path"] / "draft" / "records").is_dir() else []
    rows = [(_open(r, root, r.stem), "") for r in rec] + [(esc(x["run"]), _st(x.get("status"))) for x in t["soft"]]
    return "<p class=mut>Its records: the page's draft records and its soft runs.</p>" + table(("record", "state"), rows)


def _task_table(t: dict, q: dict, root: Path) -> str:
    f = t["face"]
    rows = [(f'<b>{esc(r.get("partition"))}</b>', _st(r.get("status")), esc(r.get("answer") or f.get("answer") or "—"),
             esc(r.get("how-sure") or f.get("how-sure") or "—"),
             _run_link(r, root)) for r in t["hard"]]
    head = f'<p>{_open(t["page"], root, t["name"], "the page")} · CHECK {esc(f.get("check") or "—")}</p>'
    if not rows:                                  # Wisdom and Executive: no run, the answer cites the ones below
        return (head + f'<p><b>Answer</b>: {esc(f.get("answer") or "not written yet")}</p>'
                f'<p class=mut>How sure: {esc(f.get("how-sure") or "—")} · no runs: it cites the answers below it.</p>')
    return head + table(("partition", "run", "answer", "how sure", "its run"), rows)


def _task_reading(t: dict, q: dict, root: Path) -> str:
    m = (q.get("method") or {}).get("read")
    return (f'<p>Read by: {_chip((m or "—") + " ↗")}</p><p>{_open(t["page"], root, t["name"], "the page")}: '
            f'Answer: {esc(t["face"].get("answer") or "—")}</p>')


def _task_parts(t: dict, root: Path) -> str:
    rows = [(f'<b>{esc(r.get("partition"))}</b>', _run_link(r, root),
             _st(r.get("status")), esc(r.get("n", "—")), esc(r.get("power", "—"))) for r in t["hard"]]
    return table(("partition", "run", "status", "n", "power"), rows) if rows else \
        "<p class=mut>No partition runs: this question cites the answers below it.</p>"


# ── a hard Run's own page, for the pop-out (/_board/insight-run?run=<its folder>) ──────────────
def _task_link(t: dict, root: Path) -> str:
    """↗ a Task's answer page in the pop-out: its answer once written, else 'not written yet'."""
    f = t.get("face") or {}
    text = "the page, all cuts" if f.get("answer") else "not written yet"
    return pop("/_board/insight-run?answer=" + rel(Path(t["path"]), root), f'{t["name"]} · the page', text + " ↗")


def render_task_page(tdir: Path, root: Path) -> str:
    """One Task of a plan-C Job as a page: its answer (the face's fields and body), then each of its hard
    Runs with its lead lines, each opening its run page. Read-only."""
    from live.paper import _RESULT_PAGE, _md_view
    tdir, root = Path(tdir).resolve(), Path(root).resolve()
    t = P.task(tdir)
    f = t["face"]
    md = t["page"].read_text(encoding="utf-8")
    text = md.split("---", 2)[2] if md.startswith("---") else md
    fields = " · ".join(f"{k} {f[k]}" for k in ("question", "answer-status", "how-sure", "check") if f.get(k) not in (None, ""))
    body = [f'<p class="where mut"><code>{esc(rel(tdir, root))}</code></p><p>{esc(fields)}</p>',
            '<div class=doc>' + _md_view(text, base="/" + rel(tdir, root) + "/") + '</div>']   # its figures, by path
    if not f.get("answer"):
        body.append('<p class=mut>The answer is not written yet: run-write writes it here from the runs below.</p>')
    rows = []
    for run in t["hard"]:
        leads = _leads(run.get("report"))
        rows.append((_run_link(run, root, run["run"]), _st(run.get("status")), esc(run.get("n", "—")),
                     esc(_cap(leads[0])) if leads else ""))
    if rows:
        body.append(f'<h2>Runs · {len(rows)}</h2>' + table(("run", "status", "rows", "what it found"), rows))
    return _RESULT_PAGE.format(title=esc(tdir.name), body="\n".join(body))


def render_run_page(rundir: Path, root: Path) -> str:
    """One hard Run as a page: where it is, its card, its generated report (the point, its figures, its
    tables) first, then every table it wrote, its receipt and its other files. Read-only."""
    from live.paper import _RESULT_PAGE, _csv_view, _md_view
    from urllib.parse import quote
    rundir, root = Path(rundir).resolve(), Path(root).resolve()
    from host_registry import static_path_allowed  # sealed labels, *.private.*, dot folders stay hidden (review 261031)
    if not static_path_allowed(root, rundir):
        return '<p class="mut">This Run is not shown here.</p>'
    res = rundir / "result"
    raw = lambda f: "/" + quote(f.resolve().relative_to(root).as_posix(), safe="/")
    card = P._yaml(rundir / "run.yaml")
    facts = " · ".join(f"{k} {card[k]}" for k in ("question", "partition", "release", "data", "n", "power", "status")
                       if card.get(k) not in (None, ""))
    links = [f'<a href="{esc(raw(f))}" target=_blank rel=noopener>{label} ↗</a>'
             for f, label in ((rundir / "run.sh", "Ticket"), (rundir / "run.yaml", "Run card"),
                              (res / "runtime.yaml", "Receipt")) if f.is_file()]
    body = [f'<h1>{esc(card.get("target", rundir.parent.parent.name))} · {esc(rundir.name)}</h1>'
            f'<p class="where mut"><code>{esc(rel(rundir, root))}</code></p><p>{esc(facts)}</p>',
            f'<div class=links>{" · ".join(links)}</div>']
    report = res / "report.md"
    if report.is_file():
        body.append('<h2>Report</h2><div class=doc>'
                    + _md_view(report.read_text(encoding="utf-8", errors="replace"), base=raw(report).rsplit("/", 1)[0] + "/") + "</div>")
    else:
        body.append('<p class=mut>Not run yet: no report.</p>')
    receipt = res / "runtime.yaml"
    if receipt.is_file():
        body.append(f'<details><summary><b>Receipt</b></summary><pre>{esc(receipt.read_text(encoding="utf-8", errors="replace")[:4000])}</pre></details>')
    files = sorted(f for f in res.rglob("*") if f.is_file() and static_path_allowed(root, f)) if res.is_dir() else []
    tabs = [f for f in files if f.suffix.lower() in (".csv", ".tsv")]
    if tabs:
        body.append(f'<details><summary><b>Tables · {len(tabs)}</b></summary>'
                    + "".join(f'<h3>{esc(f.name)}</h3>{_csv_view(f)}' for f in tabs) + "</details>")
    rest = [f for f in files if f not in tabs and f not in (receipt, report) and not f.name.startswith("fig_")]
    if rest:
        body.append(f'<details><summary><b>Other files · {len(rest)}</b></summary><ul class=files>' + "".join(
            f'<li><a href="{esc(raw(f))}" target=_blank rel=noopener>{esc(f.relative_to(res).as_posix())}</a></li>'
            for f in rest) + "</ul></details>")
    return _RESULT_PAGE.format(title=esc(rundir.name), body="\n".join(body))
