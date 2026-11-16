"""The pieces every insight view shares: the level and status words, the run cards behind each button, the links
to a page, a Run and a Job, and the small labels (release, data version, segment, written or not)."""

from __future__ import annotations

import re
import sys
import traceback
from pathlib import Path

from live import insight_plan_c as P
from live.frame import esc, pop, reader, rel, table
from live.ui_parts import _pill as _bar_pill, _section as _bar_section, _side_tabs as _bar_side_tabs, waits_on_you
from host_paths import skill_dir


# X, the Executive level: a few plain questions a leader asks, each answered from the questions below, no run of its own.
# They are read together as the Overall Report, the Audience Report's first button, before Full (the reader
# meets the summary before the full tables); no segment's table lists them.
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
          "Run the Job": ("haipipe-insight-workflow",), "Propose a segment": ("haipipe-insight-question",),
          "Propose questions": ("haipipe-insight-question",), "Update the coverage": ("haipipe-insight-check",),
          "Draw a track": ("haipipe-insight-check",), "Check consistency": ("haipipe-insight-knowledge",),
          "Pool or split": ("haipipe-insight-knowledge",), "Ask a Block question": ("haipipe-report",),
          "Write the report": ("haipipe-report",), "Check a report": ("haipipe-report",),
          "Write the counsel": ("haipipe-insight-wisdom",), "Draft the handoff": ("haipipe-insight-wisdom",),
          "Draw the question map": ("haipipe-insight",), "Run a segment": ("haipipe-insight",),
          "Check alignment": ("haipipe-insight-check",), "Add a topic": ("haipipe-studio",),
          "Open the release ↗": ("haipipe-insight",), "Open the Question Book Block ↗": ("haipipe-insight",),
          "Write a report": ("haipipe-insight-data", "haipipe-insight-information", "haipipe-insight-knowledge"),
          "Write the overall report": ("haipipe-insight",), "Write the Data report": ("haipipe-insight-data",), "Write the Information report": ("haipipe-insight-information",),
          "Write the Knowledge report": ("haipipe-insight-knowledge",), "Write the Wisdom report": ("haipipe-insight-wisdom",),
          "Compare with jNN": ("haipipe-insight-knowledge",)}


# each button named by the Run it makes (haipipe-run ref/run-types-by-space.md rule 6; b11 s21's names);
# a hard Run keeps its rNN_ name. Its words stay as what it does, the small line under the button.
RUNS = {"Add a data version": "run-add-version-data-v<M>", "Add a Job": "run-add-<jNN>", "Close a Job": "run-close-<jNN>",
        "Close the Job": "run-close-<jNN>", "Run the Job": "run-launch-<jNN>", "Propose a segment": "run-propose-cut-<slug>",
        "Propose questions": "run-propose-<jNN>", "Update the coverage": "run-coverage", "Draw a track": "run-track-<q>",
        "Check consistency": "run-consistency-<jA>-<jB>", "Pool or split": "run-pool-<tNN>",
        "Ask a Block question": "run-ask-<qNN>", "Write the report": "run-report-<qNN>",
        "Write the counsel": "run-write-counsel", "Draft the handoff": "run-draft-handoff",
        "Draw the question map": "run-map-questions", "Run a segment": "rNN_<segment>",
        "Check alignment": "run-check-alignment-<tNN>", "Add a topic": "sNN-<topic>/passes/pNN-<MMDD>", "Write a report": "run-write-<tNN>",
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
        got = NR.state(Path(folder))                 # None: not an insight Question Book, release, Board, Job or Task
        if not got:
            return ""
        st, nxt = got
        card = RC.card_for(nxt) if nxt.startswith(("run-", "r")) else None
    except ImportError:                              # the workflow skill is not installed: no next line
        return ""
    except Exception:  # noqa: BLE001 · a failing helper leaves the screen as it was; the server log names it
        traceback.print_exc()
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


# A page shows a state as a mark beside the thing, never as a word or a sentence about state. A word that asks the
# person to act, a verdict (held, changed), a name or a reason is not a state: it stays as written.
_NOT_YET = ("no ", "not ", "none", "nothing", "to ", "planned", "draft", "ready", "still ", "—", "open point")
_DONE = ("done", "ok", "closed", "answered", "written", "checked", "signed", "agreed", "pool", "ran", "all ", "pinned",
         "scripted", "aligned", "page checked", "complete", "locked", "✅", "✓", "by segment")
_UNDER_WAY = ("running", "drafted", "partly", "open", "in progress", "next", "asked", "being written", "partial")
_BAD = ("refused", "failed", "returned", "↩", "void", "error")
_ORDER = "🙋❗🏃⬜✅"


def _mark1(piece: str) -> str:
    low = piece.strip().lower()
    if not low or low in STATUS or low.startswith("waits on"):     # a verdict, or the reason a step cannot start
        return ""
    if low == "nothing to do":
        return "✅"
    if low.startswith(_NOT_YET) or low == "ready":
        return "⬜"
    if low.startswith(_BAD):
        return "❗"
    if low.startswith(_DONE):
        return "✅"
    if "sign" in low:
        return "🙋"
    return "🏃" if low.startswith(_UNDER_WAY) else ""


def mark(word) -> str:
    """A state word as its mark: ✅ there, 🏃 under way, ⬜ not yet, ❗ refused or sent back, 🙋 waits on a sign. Several
    states joined by " · " become the one mark that most needs a look; whatever is not a state stays in words."""
    word = str(word or "").strip()
    if not word or waits_on_you(word):
        return word
    pieces = [p for p in word.split(" · ") if p.strip()]
    marks = [_mark1(p) for p in pieces]
    kept = [p for p, m in zip(pieces, marks) if not m]
    got = sorted({m for m in marks if m}, key=_ORDER.index)
    return " ".join(got[:1] + ([" · ".join(kept)] if kept else []))


def _section(title: str, body: str, word: str = "", waits: str = "") -> str:
    """The shared section bar, its state as a mark."""
    return _bar_section(title, body, mark(word), waits)


def _pill(state: str) -> str:
    """The shared pill, its state as a mark (its colour still read from the state)."""
    m = mark(state)
    return _bar_pill(state).replace(">" + esc(state) + "<", ">" + esc(m) + "<") if state and m != state else _bar_pill(state)


def _side_tabs(eid: str, items: list, panels: list) -> str:
    """The shared side tabs, each item's state as a mark."""
    return _bar_side_tabs(eid, [(h, mark(w)) for h, w in items], panels)


def _st(state: str) -> str:
    s = str(state or "—")
    low = s.lower()
    cls = ("st-ok" if low in OK or low.split(" ")[0] in OK or s.startswith("✅") else
           "mut" if low in QUIET else "st-warn")
    return f"<span class={cls}>{esc(mark(s))}</span>"


def _fold(title: str, meta: str, body: str, opened: bool = False) -> str:
    return (f'<details class=topic{" open" if opened else ""}><summary><b>{esc(title)}</b>'
            f'<span class=topic-meta>{esc(mark(meta))}</span></summary><div style="padding:8px 14px">{body}</div></details>')


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
    """A page's focus view (a Question Book release, a Task): the frame's own route."""
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
    board laid them: "Data questions 5", its 'may say' line, and on the right a link to where
    that level's questions are kept (`links`: {letter: html}). A level opens to its question rows.
    With `tabs` (the focus page's id for them): side tabs instead, a level's name on the left with its state word
    (`words`: {letter: word}), no count in a label (haipipe-ui: one kind of tabs, labels carry no counts; 261106)."""
    if tabs:
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
    """Each DIKW level's link to where its questions are kept: the Question Book release, in the workbench."""
    if not rel_dir or not Path(rel_dir).is_dir():
        return {}
    url = "/_board/workbench?path=" + rel(Path(rel_dir), root)
    name = label or Path(rel_dir).name
    return {lv: pop(url, f"{name} · {word.lower()} questions", f"{name} · {word.lower()} questions ↗")
            for lv, word, _ in LEVELS}


OPS = {"eq": "=", "ne": "≠", "lt": "<", "lte": "≤", "gt": ">", "gte": "≥", "isin": "in", "notin": "not in"}


def _where(p: dict) -> str:
    """A segment's filter in words: `patient_gender = M · age ≤ 35`; a list of conditions or a plain string."""
    w = p.get("where")
    if isinstance(w, list):
        conds = [" ".join([str(c.get("column", ""))] + [f"{OPS.get(k, k)} {v:g}" if isinstance(v, float) else f"{OPS.get(k, k)} {v}"
                                                         for k, v in c.items() if k != "column"])
                 if isinstance(c, dict) else str(c) for c in w]
        return " · ".join(conds) or "every row"
    return str(w or "") or ("across " + ", ".join(p.get("of") or []) if p.get("of") else "every row")


WORDS = {"young", "old", "older", "midlife", "middle", "adult", "senior", "teen", "elder"}   # a segment's prefix word


def _label(name: str) -> str:
    """A segment's button: `youngmale` -> `Young male`, `full` -> `Full`; a name with other characters stays."""
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


LEVEL_WORD = {"X": "Executive", "D": "Data", "I": "Information", "K": "Knowledge", "W": "Wisdom"}
MARK = {"ok": "✅", "refused": "🚫", "failed": "❌", "planned": "⏳", "running": "⏳"}


def _job_link(href, j: dict, short: bool = False) -> str:
    """A Job by its folder name, or (short, where its row and column already say the plan and the data) by `j01`."""
    text = j["name"].split("_", 1)[0] if short else j["name"]
    return f'<a href="{esc(href("", "", j["path"]))}" title="{esc(j["name"])}">{esc(text)}</a>'


def _rlabel(b: dict, name: str) -> str:
    """A question version (a release) by its id and words, `question-v1 · first ladder`, from the Question Book's release folder."""
    return next((r.get("label") or r["name"] for r in b["prototype"]["releases"] if r["name"] == name), P.plan_code(name))


def _vlabel(b: dict, version: str) -> str:
    """A data version by its id and words, `data-v1 · first 5 days`, from board.md versions:."""
    v = next((v for v in b["versions"] if str(v.get("version")) == str(version)), {})
    words = P.freeze_words(v)
    return f"{P.freeze_code(version)} · {words}" if words else P.freeze_code(version)


WRITTEN = ("written", "answered", "checked")     # a page is written once any of these (the matrix counts the same)


def _runs_table(runs: list, root: Path) -> str:
    rows = [(_run_link(r, root), esc(r.get("kind", "")), esc(r.get("type", "")),
             esc(r.get("target", "")), _st(r.get("status")), esc(r.get("passes", ""))) for r in runs]
    return table(("Run", "kind", "type", "target", "status", "passes"), rows)


def _band(j: dict, b: dict) -> str:
    moved = {"code": "the code", "data": "the data", "start": "the first Job"}.get(j["moved"], j["moved"] or "—")
    prev = f' · moved from {esc(j["previous"][:3])}: {esc(moved)}' if j["previous"] else f" · {esc(moved)}"
    frozen = ", frozen" if j["state"] == "closed" else ""
    return (f'<p class=mut><code>{esc(_rlabel(b, j["release"]))} × {esc(_vlabel(b, j["data"]))}</code> · '
            f'{esc(j["state"])}{frozen}{prev}</p>')


RUN_LEVELS = "DIK"                        # a question with Runs of its own; W and X cite the answers below them


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
    """A page's state as a mark: ❗ returned (a CHECK sent it back), else its answer-status's mark."""
    f = t.get("face") or {}
    if str(f.get("check") or "").startswith("↩"):
        return "❗"
    return mark(str(f.get("answer-status") or "to write"))


def far(done: int, total: int, word: str, none: str = "") -> str:
    """How far a set of items is, as a mark and never a count or a word (each item shows its own state where it sits):
    ✅ all of them, 🏃 some, ⬜ none. `word` and `none` name what is counted, for the reader of the code."""
    return "✅" if total and done >= total else "🏃" if done else "⬜"


def _task_link(t: dict, root: Path) -> str:
    """↗ a Task's answer page in the pop-out: its answer once written, else 'not written yet'."""
    f = t.get("face") or {}
    text = "the page, all segments" if f.get("answer") else "not written yet"
    return pop("/_board/insight-run?answer=" + rel(Path(t["path"]), root), f'{t["name"]} · the page', text + " ↗")
