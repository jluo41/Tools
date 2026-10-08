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
from pathlib import Path

from live import insight_plan_c as P
from live.frame import Space, esc, pop, reader, rel, table

LEVELS = (("D", "Data", "may say: counts, what was seen"),
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
          "Pool or split": ("haipipe-insight-knowledge",), "Ask a Block question": ("haipipe-question",),
          "Write the report": ("haipipe-report",), "Check a report": ("haipipe-report",),
          "Write the counsel": ("haipipe-insight-wisdom",), "Draft the handoff": ("haipipe-insight-wisdom",),
          "Draw the question map": ("haipipe-insight",), "Run a partition": ("haipipe-insight",),
          "Check alignment": ("haipipe-insight-check",), "Add a topic": ("haipipe-studio",),
          "Open the release ↗": ("haipipe-insight",), "Open the Prototype Block ↗": ("haipipe-insight",),
          "Write a report": ("haipipe-insight-data", "haipipe-insight-information", "haipipe-insight-knowledge"),
          "Write the Data report": ("haipipe-insight-data",), "Write the Information report": ("haipipe-insight-information",),
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
        "Write the Knowledge report": "run-write-<tNN>", "Write the Wisdom report": "run-write-<tNN>"}


def _kind(label: str, prompt: str, *skills: str, rows=(), run: str = "") -> dict:
    """A Runs-panel kind; `rows` are its past runs (run_id, status, target, result), newest last; its
    skills default to the button's owner (SKILLS). The button shows the Run it makes (`run`, else RUNS),
    its words kept as `doing`; a link that opens a file (… ↗) makes no Run and keeps its words."""
    owner = skills or SKILLS.get(label) or (SKILLS["Compare with jNN"] if label.startswith("Compare with ") else ())
    name = run or RUNS.get(label) or ("run-compare-" + label.split()[-1] if label.startswith("Compare with ") else "")
    return {"label": name or label, "doing": label if name else "", "prompt": prompt, "skills": list(owner),
            "rows": list(rows)}


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


def _open(path: Path | None, root: Path, label: str, text: str = "") -> str:
    """↗ a file in the frame's pop-out (the page reader)."""
    if not path or not Path(path).exists():
        return esc(text or label)
    return pop(reader(Path(path), root), label, (text or label) + " ↗")


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


def _by_level(rows: dict, head: str, empty: str = "No question at this DIKW level.") -> str:
    """rows: {level letter: [row html]} -> D · I · K · W sections, each with its 'may say' line."""
    out = []
    for lv, name, says in LEVELS:
        if not rows.get(lv):
            continue
        out.append(_fold(f"{name} questions", f"{len(rows[lv])} · {says}",
                         head + "".join(rows[lv]), opened=True))
    return "".join(out) or f"<p class=mut>{esc(empty)}</p>"


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
LEVEL_WORD = {"D": "Data", "I": "Information", "K": "Knowledge", "W": "Wisdom"}
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


def _q_logic(qid: str, q: dict, mark: str, root: Path) -> str:
    s = _spec(q)
    more = [(k, s.get(k)) for k in ("ask", "why", "answer") if isinstance(s.get(k), str) and s.get(k)]
    asked = (s.get("partitions") or {}).get("asked") if isinstance(s.get("partitions"), dict) else ""
    more += [("asked on", asked if isinstance(asked, str) else ", ".join(asked))] if asked else []
    body = "".join(f'<p><span class=mut>{esc(k)}:</span> {esc(v)}</p>' for k, v in more)
    cited = sorted({str(n["from"]).split(".")[0] for n in _needs(q) if isinstance(n.get("from"), str)
                    and re.match(r"^[DIKW]\d+", str(n["from"]))})
    builds = ""
    if cited:
        by = {}
        for c in cited:
            by.setdefault(c[0], []).append(str(int(c[1:])))
        builds = ("<p class=mut>builds on " + "; ".join(f"{LEVEL_WORD[k]} questions {', '.join(v)}" for k, v in by.items())
                  + "</p>")
    return (f'<p class=q-head><span class=chip>Question {int(qid[1:])}</span> {esc(mark)}</p>'
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
    return (f'<details open><summary><span class=chip>Task Work</span></summary><ol>{steps}</ol></details>'
            + "".join(f'<p class=mut>{line}</p>' for line in trail))


def _q_report(name: str, run, root: Path, cut: str, extra: str = "") -> str:
    if not run:
        return f'<p class=mut>Not asked on this cut</p>{extra}'
    state = str(run.get("status") or "—")
    word = {"ok": "Ran on this cut", "refused": "Refused", "failed": "Failed", "planned": "Not run yet"}.get(state, _cap(state))
    head = f'<p><span class=chip>Report</span> {_st(word) if state != "ok" else esc(word)}</p>'
    if "answer" in run:                                    # a carried board: the cut's answering page
        title = _open(run["report"], root, run["run"], run["answer"] or "the page") if run["report"] else esc(state)
        return head + f'<p class=q-head><b>{title}</b></p><p class=mut>{esc(run.get("how-sure") or "")}</p>{extra}'
    report = run.get("report")
    leads = _leads(report)
    title = _open(report, root, run["run"], f"{name or run['run']} · {cut}") if report else esc(f"{name} · {cut}")
    why = run.get("reason") or ""
    return (head + f'<p class=q-head><b>{title}</b></p>'
            + "".join(f"<p>{esc(_cap(x))}</p>" for x in leads)
            + (f'<p class=mut>{esc(why)}</p>' if why else "")
            + f'<p class=mut>run {esc(run["run"])} · {esc(run.get("n", "—"))} rows · the page: not written yet</p>{extra}')


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
                                         "moved from its neighbour (run-add-<jNN>; the Job folder j0N_pN_<d>vM carries the pair).", rows=_rows(b["runs"], root, "add"))),
              "Prototype": (_kind("Open the Prototype Block ↗", f"Open the Prototype Block {prel}: releases are cut there."),),
              "Dataset": (_kind("Add a data version", "Add a data version to the Board {folder} (run-add-version-<d>vM)."),),
              "Partitions": (_kind("Propose a cut", f"Propose a cut for {prel}/proposals/ (run-propose-cut-<slug>): a cut is plan, so it lands "
                                                    "in the next release."),)}[d_open]
    a_part, a_read = split(sub, parts, READINGS)
    a_html = (second_row(href, "Audience Report", a_part, READINGS, a_read, "Reading")
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
    rels = tuple(r["name"] for r in proto["releases"])
    w_open = sub if sub in rels else "All"
    r_views = ("All", "soft", "from below")
    r_open = sub if sub in r_views else "All"
    return {
        "Description": Space(html=d_html, subspaces=desc, open=d_open, run_types=d_runs),
        "Audience Report": Space(html=a_html, subspaces=parts, open=a_part, run_types=a_runs),
        "Idea Studio": Space(run_types=(_kind("Draw the question map", "Draw the question map of {folder} into studio/ (run-map-questions) "
                                              "(generated from the question files; view only)."),
                                        _kind("Add a topic", "Add or redraw a studio topic of {folder} (run-draw-<sNN>): studio/sNN-<topic>/, a pass per session."))),
        "Work Details": Space(html=_jobs(b, root, href, w_open), subspaces=("All",) + rels, open=w_open,
                              run_types=(_kind("Add a Job", "Add a Job to {folder} (run-add-<jNN>).",
                                               rows=_rows(b["runs"], root, "add")),
                                         _kind("Close a Job", "Close a Job of {folder} after its checks and its comparison "
                                                              "(run-close-<jNN>): frozen.",
                                               rows=_rows([r for j in b["jobs"] for r in j["runs"]], root, "close")))),
        "Runs": Space(html=_board_runs(b, root, r_open), subspaces=r_views, open=r_open,
                      run_types=(_kind("Add a Job", "Add a Job to {folder} (run-add-<jNN>).", rows=_rows(b["runs"], root, "add")),
                                 _kind("Update the coverage", "Update the coverage of {folder} (run-coverage).",
                                       rows=_rows(b["runs"], root, "coverage")),
                                 _kind("Check consistency", "Check consistency between two Jobs of {folder}.",
                                       rows=_rows(b["runs"], root, "consistency")))),
        "Delivery": Space(html=_handoff(b, root), subspaces=("Handoff",), open="Handoff",
                          run_types=(_kind("Write the counsel", "Write the Wisdom counsel of {folder} from the latest Job."),
                                     _kind("Draft the handoff", "Draft the handoff of {folder} for a person to sign."))),
    }


def _job_link(href, j: dict) -> str:
    return f'<a href="{esc(href("", "", j["path"]))}">{esc(j["name"])}</a>'


def _map(b: dict, root: Path, href) -> str:
    versions = [v.get("version", "") for v in b["versions"]]
    rels = [r["name"] for r in b["prototype"]["releases"]] or sorted({j["release"] for j in b["jobs"]})
    cell = {(j["release"], j["data"]): j for j in b["jobs"]}
    rows = []
    for r in rels:
        row = [f"<b>{esc(r)}</b>"]
        for v in versions:
            j = cell.get((r, v))
            row.append(f'{_job_link(href, j)} {_st(j["state"])}' if j else '<span class=mut>· Add a Job</span>')
        rows.append(row)
    return ('<p class=mut>The two clocks crossed: the Prototype releases as rows, the data versions as columns, '
            'a Job in each cell (one Prototype version × one data version).</p>'
            + table(["release \\ data"] + versions, rows))


def _prototype(b: dict, root: Path, href) -> str:
    proto = b["prototype"]
    out = [f'<p class=mut>The questions live in the Prototype Block: {esc(rel(proto["path"], root)) if proto["path"].exists() else "—"}'
           ' (read only here; releases are cut there).</p>']
    jobs_on = {}
    for j in b["jobs"]:
        jobs_on.setdefault(j["release"], []).append(j["name"])
    for k, r in enumerate(proto["releases"]):
        rows = []
        for lv, name, _ in LEVELS:
            for q in (q for q in r["questions"].values() if q["id"][:1] == lv):
                rows.append((f'<b>{esc(q["id"])}</b>', esc(name), _open(q["file"], root, q["id"], q["question"] or "<question>"),
                             esc(q["change"] or "—"), _st(q["signed"] or "—")))
        meta = f'{r["face"].get("state", "")} · {r["face"].get("signed", "")} · Jobs: {", ".join(jobs_on.get(r["name"], [])) or "none yet"}'
        out.append(_fold(f'release {r["name"]}', meta, table(("#", "DIKW level", "question", "in this release", "signed"), rows),
                         opened=k == len(proto["releases"]) - 1))
    props = [(_open(p["file"], root, p["title"]), esc(p.get("kind", "")), esc(p.get("from", "")), _st(p.get("state", "")))
             for p in proto["proposals"]]
    out.append(_fold("proposals/", f"{len(props)} open", table(("proposal", "kind", "from", "state"), props)))
    return "".join(out)


def _dataset(b: dict, root: Path, href) -> str:
    on = {}
    for j in b["jobs"]:
        on.setdefault(j["data"], []).append(j)
    rows = [(f'<b>{esc(v.get("version", ""))}</b>', f'<code>{esc(v.get("extract", ""))}</code>', esc(v.get("frozen", "")),
             esc(v.get("rows", "")), esc(v.get("new", "")), " ".join(_job_link(href, j) for j in on.get(v.get("version"), [])))
            for v in b["versions"]]
    return (f'<p class=mut>One dataset, <b>{esc(b["dataset"])}</b>, its versions frozen outside the Project; a new version '
            f'is a new column of the Map. accumulates: {esc(b["accumulates"] or "—")}</p>'
            + table(("version", "extract", "frozen", "rows", "what is new", "Jobs on it"), rows))


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
    return (f'<p class=mut>Defined in release {esc(r["name"])} ({esc(rel(r["job"], root))}/partitions.md), part of the plan, '
            f'fixed before any outcome; a new or changed cut is a new release. Power floor: '
            f'{esc(power.get("smallest_effect_pp", "—"))} pp.</p>'
            + table(("partition", "where", "why"), defs)
            + '<p class=mut>Rows per data version (a row per version, a column per partition):</p>'
            + table(["version"] + names, counts))


def _questions(b: dict) -> dict:
    """Every question any release asks, by id, with the release that asks it last."""
    out = {}
    for r in b["prototype"]["releases"]:
        for qid, q in r["questions"].items():
            out[qid] = dict(q, release=r["name"])
    return out


def _cell(j: dict, qid: str, part: str) -> tuple:
    t = next((t for t in j["tasks"] if t["qid"] == qid), None)
    if not t:
        return None, None
    run = next((r for r in t["hard"] if r.get("partition") == part), None)
    return t, run


def _coverage(b: dict, root: Path, part: str, href) -> str:
    rows = {}
    for qid, q in _questions(b).items():
        trail, n, last = [], 0, None
        for j in b["jobs"]:
            t, run = _cell(j, qid, part)
            if not t:
                trail.append(f'<code>{esc(j["name"])}</code> · not in its release')
                continue
            state = run.get("status", "—") if run else t["face"].get("answer-status", "—")
            n += state in OK
            last = run or last
            ran = (_open(run["report"] or (run["path"] / "run.yaml"), root, run["run"], run["run"]) if run
                   else "no run on this cut")
            trail.append(f'<code>{esc(j["name"])}</code> › <code>{esc(t["name"])}</code> ▸ {ran} · {_st(state)}')
        mark = MARK.get(str((last or {}).get("status")), "·")
        rows.setdefault(qid[:1], []).append(_qwr(
            _q_logic(qid, q, mark, root), _q_work(q, trail),
            _q_report(_spec(q).get("name") or qid, last, root, _label(part),
                      f'<p class=mut>answered on {n} of {len(b["jobs"])} Jobs</p>'), f"question-{qid}"))
    return _by_level(rows, _qwr_head("Task Work · each Job on this cut", "Report · what it found"))


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


def _findings(b: dict, root: Path, part: str, href) -> str:
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
    return ("<p class=mut>The Block's own questions, a second D · I · K · W over the Jobs' answers; they live on the "
            "Board (board.md, reports/qNN_&lt;topic&gt;/).</p>"
            + _by_level(rows, _qwr_head("Work · the Board's soft run", "Report · what it says"), "No Block question yet."))


def _answered(j: dict) -> str:
    out = []
    for lv, _, _ in LEVELS:
        ts = [t for t in j["tasks"] if t["qid"][:1] == lv]
        if ts:
            done = sum(t["face"].get("answer-status") == "answered" for t in ts)
            out.append(f"{lv} {done}/{len(ts)}")
    return " · ".join(out)


def _jobs(b: dict, root: Path, href, only: str) -> str:
    rows = []
    for j in b["jobs"]:
        if only != "All" and j["release"] != only:
            continue
        rows.append((_job_link(href, j), esc(f'{j["release"]} × {b["dataset"]} {j["data"]}'),
                     esc(j["moved"] or "—"), esc(_answered(j)), _st(j["state"])))
    out = [table(("Job", "pins", "the clock that moved", "answered by DIKW level", "state"), rows)]
    for j in (j for j in b["jobs"] if j["state"] != "closed" and (only == "All" or j["release"] == only)):
        quick = []
        for t in j["tasks"]:
            quick.append((f'<a href="{esc(href("", "", t["path"]))}">{esc(t["name"])}</a>',
                          " · ".join(f'{esc(r.get("partition"))} {_st(r.get("status"))}' for r in t["hard"]) or "<span class=mut>—</span>"))
        out.append(_fold(f'{j["name"]} · its Tasks\' quick results', "open", table(("Task", "each partition"), quick), opened=True))
    return "".join(out)


def _runs_table(runs: list, root: Path) -> str:
    rows = [(_open(r["report"] or (r["path"] / "run.yaml"), root, r["run"]), esc(r.get("kind", "")), esc(r.get("type", "")),
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
    return ('<p class=mut>The signed Wisdom counsel, naming the Job (pN × vM) it came from. Only a signed counsel leaves '
            'this Board.</p>' + (table(("counsel", "from Job", "signed"), rows) if rows else
                                 '<p class=mut>No signed counsel yet.</p>'))


# ── a Job ───────────────────────────────────────────────────────────────────────────────────────
def _band(j: dict, b: dict) -> str:
    moved = {"code": "the code", "data": "the data", "start": "the first Job"}.get(j["moved"], j["moved"] or "—")
    prev = f' · moved from {esc(j["previous"][:3])}: {esc(moved)}' if j["previous"] else f" · {esc(moved)}"
    frozen = ", frozen" if j["state"] == "closed" else ""
    return (f'<p class=mut><code>{esc(j["release"])} × {esc(b["dataset"])} {esc(j["data"])}</code> · '
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
    d_html = (band + _job_prototype(j, r, root)) if d_open == "Prototype" else _job_dataset(j, b, r)
    parts = _part_names(r["partitions"])
    a_part, a_period = split(sub, parts, PERIODS)
    prev = j["previous"][:3]
    a_html = second_row(href, "Audience Report", a_part, PERIODS, a_period, "Period") + (
        _job_current(j, b, r, root, _part_key(a_part)) if a_period == "Current" else _vs_previous(j, root))
    me = j["name"][:3]
    propose = _kind("Propose questions", f"Propose questions from {me} (run-propose-{me}): file each new or changed "
                    "question, and each gap this Job could not answer, to the Prototype's proposals/<slug>.md (kind · "
                    f"DIKW level · from {me} · why). It writes nothing else.", rows=_rows(j["runs"], root, "propose"))
    a_runs = ((_kind("Compare with " + prev, f"Compare this Job with {prev} (run-compare-{prev}): it writes "
                     f"reports/vs-{prev}.md, after every check.", rows=_rows(j["runs"], root, "compare")), propose)
              if a_period == "vs previous" and prev else (propose,) if a_period == "vs previous" else
              (_kind("Pool or split", "Run the Cross test of a question in {folder} (rNN_cross): one test of the "
                     "difference."),) if _part_key(a_part) == "cross" else
              (_kind("Write a report", "Write a question's page in {folder}: a part per partition."),
               _kind("Check a report", "Check a question's page in {folder} (run-check-<tNN>).", run="run-check-<tNN>")))
    w_views = ("All", "hard", "soft")
    w_open = sub if sub in w_views else "All"
    r_views = ("All", "hard", "soft", "launch", "power", "compare", "propose", "close")
    r_open = sub if sub in r_views else "All"
    hard = [x for t in j["tasks"] for x in t["hard"]]
    soft = [x for t in j["tasks"] for x in t["soft"]]
    own = (_kind("Run the Job", "Run the Job {folder} (run-launch): start every Task's hard Runs, one per partition.",
                 rows=_rows(j["runs"], root, "launch")),
           _kind("Run a partition", "Run one question on one partition in {folder} (rNN_<partition>).",
                 rows=_rows(hard, root, "hard")))
    return {
        "Description": Space(html=d_html, subspaces=desc, open=d_open, page=True,   # Dataset: no run, as s12 draws it
                             run_types=(_kind("Open the release ↗", f"Open the release {rel(r['job'], root) if r['job'] else j['release']}: "
                                              "read only here; it is changed in the Prototype Block."),) if d_open == "Prototype" else ()),
        "Audience Report": Space(html=a_html, subspaces=parts, open=a_part, run_types=a_runs),
        "Work Details": Space(html=_tree(j, root, w_open, href), subspaces=w_views, open=w_open,
                              run_types=own[1:] + (_kind("Check alignment", "Check a run against its plan in {folder} (run-check).",
                                                         rows=_rows(soft, root, "check")), own[0])),
        "Runs": Space(html=_job_runs(j, root, r_open), subspaces=r_views, open=r_open,
                      run_types=own + ((_kind("Compare with " + prev, f"Compare this Job with {prev} (run-compare-{prev}).",
                                              rows=_rows(j["runs"], root, "compare")),) if prev else ())
                      + (propose, _kind("Close the Job", "Close the Job {folder} after its checks and the comparison (run-close): frozen.",
                               rows=_rows(j["runs"], root, "close")),)),
        "Idea Studio": Space(run_types=(_kind("Add a topic", "Add or redraw a studio topic of {folder} (run-draw-<sNN>): studio/sNN-<topic>/, a pass per session."),)),
        # page=True: the frame takes this Space's runs and third row as set, even none (frame.lays_out_page)
        "Delivery": Space(html=_job_delivery(j, b), run_types=(), page=True,
                          note="Nothing to run here: the Board's Delivery holds the handoff."),
    }


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
    return (f'<p class=mut>Release {esc(r["name"])}: {esc(rel(r["job"], root)) if r["job"] else "—"} (read only).</p>' + body
            + _fold("the cuts, as defined in the release", f"{len(defs)}", table(("partition", "where", "why"), defs))
            + f'<p class=mut>Power floor: {esc(power.get("smallest_effect_pp", "—"))} pp · compare rule: '
              f'{esc(compare) if compare else "not set (still open)"} · shared code: {esc(", ".join(code) or "none")}</p>')


def _job_dataset(j: dict, b: dict, r: dict) -> str:
    v = next((v for v in b["versions"] if v.get("version") == j["data"]), {})
    facts = table(("fact", "value"), [("version", esc(v.get("version", j["data"]))), ("extract", f'<code>{esc(v.get("extract", ""))}</code>'),
                                      ("frozen", esc(v.get("frozen", ""))), ("rows", esc(v.get("rows", ""))),
                                      ("what is new", esc(v.get("new", "")))])
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
    return facts + "<p class=mut>Each cut on this version, checked before any outcome (run-power):</p>" + \
        table(("partition", "n", "power", "refused"), rows)


def _method_chips(q: dict, which: str) -> str:
    m = (q.get("method") or {}).get(which)
    return _chip(f"{which}: {m} ↗") if m else ""


def _job_current(j: dict, b: dict, r: dict, root: Path, part: str) -> str:
    rows = {}
    for t in j["tasks"]:
        q = r["questions"].get(t["qid"], {})
        run = next((x for x in t["hard"] if x.get("partition") == part), None)
        f = t["face"]
        if t["qid"][:1] == "W" and not t["hard"]:
            trail = ['cites the K and I answers; no run of its own']
        elif run:
            trail = [f'<code>{esc(j["name"])}</code> › <code>{esc(t["name"])}</code> ▸ '
                     f'{_open(run["report"] or (run["path"] / "run.yaml"), root, run["run"], run["run"])} · {_st(run.get("status"))}']
        else:
            trail = ["not asked on this cut"]
        mark = MARK.get(str((run or {}).get("status")), "·") if run else ("retired" if _spec(q).get("retired") else "·")
        page = (f'<p class=mut>the page: {_open(t["page"], root, t["name"], f.get("answer") or "open ↗")} · '
                f'CHECK {esc(f.get("check") or "—")}</p>' if t.get("page") and "answer" not in (run or {}) else "")
        if t["qid"][:1] == "W" and not t["hard"]:
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
    return head + _by_level(rows, _qwr_head(work_head, "Report · what it found"))


def _vs_previous(j: dict, root: Path) -> str:
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
    rows = {}
    for qid, row in vs["rows"].items():
        rows.setdefault(qid[:1], []).append(_qwr(f'<p class=q-head><b>{esc(qid)}</b></p>',
                                                 f'previous: {esc(row["previous"])}<br>this: {esc(row["this"])}',
                                                 f'{_st(row["status"])} <span class=mut>{esc(row["why"])}</span>'))
    return (f'<p><b>{esc(summary)}</b> · {_open(vs["file"], root, vs["file"].name)}</p><p>{chips}</p>'
            '<p class=mut>As the Job\'s run-compare wrote it; one clock moved, so "why" names its cause.</p>'
            + _by_level(rows, _qwr_head("Work · the two answers", "Report · status · why")))


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


def _job_delivery(j: dict, b: dict) -> str:
    latest = b["jobs"][-1]["name"] if b["jobs"] else ""
    if any(t["qid"][:1] == "W" for t in j["tasks"]) and j["name"] == latest:
        return "<p>This is the latest Job: its Wisdom counsel goes to Board › Delivery › Handoff, naming this Job.</p>"
    return "<p class=mut>None of its own: a Job's answers are read by the Board.</p>"


# ── a Task ──────────────────────────────────────────────────────────────────────────────────────
def task_spaces(tdir: Path, root: Path, sub: str, href) -> dict:
    jdir = P.task_job(tdir)
    b = P.board(P.job_board(jdir))
    j = P.job(jdir)
    t = P.task(tdir)
    q = P.question_of(b["prototype"], j["release"], t["qid"])
    level = {"D": "Data", "I": "Information", "K": "Knowledge", "W": "Wisdom"}.get(t["qid"][:1], "")
    head = f'<p class=mut><code>{esc(t["qid"])}</code> on {esc(j["name"])} · {esc(level)} · {_st(t["face"].get("answer-status", "—"))}</p>'
    d_views = ("Question", "Records")
    d_open = sub if sub in d_views else "Question"
    a_views = ("Table", "Reading")
    a_open = sub if sub in a_views else "Table"
    r_views = ("All", "hard", "soft")
    r_open = sub if sub in r_views else "All"
    # page=True on each: the frame takes the subspaces and runs as set, so s13's views stand alone
    return {
        "Description": Space(html=head + (_question(q, root) if d_open == "Question" else _records(t, root)),
                             subspaces=d_views, open=d_open, run_types=(), page=True,
                             note="Read only: a change to the question is made in the Prototype."),
        "Idea Studio": Space(run_types=(_kind("Add a topic", "Add or redraw a studio topic of {folder} (run-draw-<sNN>): studio/sNN-<topic>/, a pass per session."),)),
        "Audience Report": Space(html=head + (_task_table(t, q, root) if a_open == "Table" else _task_reading(t, q, root)),
                                 subspaces=a_views, open=a_open, page=True,
                                 run_types=(_kind(f"Write the {level} report", "Write the page of {folder}: a part per partition."),
                                            _kind("Check a report", "Check the page of {folder} (run-check-<tNN>).", run="run-check-<tNN>"))),
        "Work Details": Space(html=head + _task_parts(t, root), subspaces=("Partitions",), open="Partitions", page=True,
                              run_types=(_kind("Run a partition", "Run {folder} on one partition (rNN_<partition>).",
                                               rows=_rows(t["hard"], root, "hard")),
                                         _kind("Check alignment", "Check a run of {folder} against its plan (run-check).",
                                               rows=_rows(t["soft"], root, "check")))),
        "Runs": Space(html=head + _runs_table([x for x in t["hard"] + t["soft"] if r_open == "All" or x.get("kind") == r_open], root),
                      subspaces=r_views, open=r_open, page=True,
                      run_types=(_kind("Run a partition", "Run {folder} on one partition (rNN_<partition>)."),
                                 _kind("Check alignment", "Check a run of {folder} against its plan (run-check)."))),
        "Delivery": Space(html=head + "<p class=mut>None of its own: its answer goes up as a cite need.</p>",
                          page=True, note="Nothing to run here."),
    }


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
             _open(r["report"] or (r["path"] / "run.yaml"), root, r["run"])) for r in t["hard"]]
    return (f'<p>{_open(t["page"], root, t["name"], "the page")} · CHECK {esc(f.get("check") or "—")}</p>'
            + table(("partition", "run", "answer", "how sure", "its run"), rows))


def _task_reading(t: dict, q: dict, root: Path) -> str:
    m = (q.get("method") or {}).get("read")
    return (f'<p>Read by: {_chip((m or "—") + " ↗")}</p><p>{_open(t["page"], root, t["name"], "the page")}: '
            f'Answer: {esc(t["face"].get("answer") or "—")}</p>')


def _task_parts(t: dict, root: Path) -> str:
    rows = [(f'<b>{esc(r.get("partition"))}</b>', _open(r["report"] or (r["path"] / "run.yaml"), root, r["run"]),
             _st(r.get("status")), esc(r.get("n", "—")), esc(r.get("power", "—"))) for r in t["hard"]]
    return table(("partition", "run", "status", "n", "power"), rows) if rows else \
        "<p class=mut>No partition runs: this question cites the answers below it.</p>"
