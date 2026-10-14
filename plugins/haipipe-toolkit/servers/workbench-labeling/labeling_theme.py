"""The labeling theme on the base frame (servers/workbench/frame.py): only what differs from vanilla.

A labeling Job is one dataset × one label (`jNN_<dataset>_<label>/`, its `schema.yaml`); each of its Tasks
is one of five types, read from the face's `task-type:` line (Tools/blueprints/b15_theme_labeling,
s13-labeling-task): items · keys · building · scanning · score. Today's one labeling Page
(`task-type: labeling`) is building and scanning at once; the engine's own Labeling workbench (labeling.py:
Data · Labeling · Quality · Delivery) stays the one place a person labels: it is the write door, gated by
the engine. This theme is read only. It shows each Task's type and state, the types a Job still lacks, and
opens that workbench at the right view; it never renders item text and never writes.

    Block  Description: Scope · Schema (schema.yaml)
           Work Details: Jobs (vanilla) · Labeling (one status row per labeling job, labeling.board_jobs)
    Job    Description: Scope · Schema (the Job's schema.yaml)
           Work Details: its Tasks, each with its type and state, then a dashed card per type still to make
    Task   by its type:
           items     three steps, each a tab in Work and Report (b15 s41): 1 · Data · 2 · Items · 3 · Embedding;
                     ① at a glance, ② the picture, ③ details folded (Work, under the step's Copy prompt)
           keys      vanilla; a note that building and scanning never read it
           building  Description: Scope · Contract; Work Details: Preparation · Embedding · Definition ·
                     Rounds · Guideline; Delivery: Files · Handoff
           scanning  Description: Scope · Handoff; Work Details: Test · Evaluation · Scan · Audit;
                     Delivery: Files · Final labels
           score     vanilla; a note that it reads the final labels and the keys
           each engine view: the job's status, and "open in the Labeling workbench ↗" at that view; its skill
           as a run type (the panel copies a prompt and starts nothing)

Drawn in the base's look only (JL 261007: no theme stylesheet): wf-table, .chip, .mut, .space-source,
.st-ok/.st-warn, .topic.missing. The labeling package is optional: without it this theme loads and shows vanilla.
"""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import parse_qs, quote, urlsplit

from live.frame import Space, Theme, children, esc, face, rel, table

try:                                            # the optional haipipe-labeling package (labeling.py)
    from live import labeling as L
except Exception:                               # absent or broken: the frame shows vanilla
    L = None

try:
    import yaml
except Exception:                               # a Run's manifest then shows its headline only
    yaml = None

# (old Space id, view id, frame subspace, what it is, the skill that works it)
VIEWS = (
    ("data", "preparation", "Preparation", "the corpus prepared for labeling: items, sealed test split",
     "haipipe-labeling-preparation"),
    ("data", "contract", "Contract", "the job's contract: the label, the person who decides, the corpus",
     "haipipe-labeling-contract"),
    ("data", "embedding", "Embedding", "the items embedded, for drawing rounds and audits",
     "haipipe-labeling-embedding"),
    ("labeling", "definition", "Definition", "what each label means, confirmed by the person (G0)",
     "haipipe-labeling-definition"),
    ("labeling", "rounds", "Rounds", "the calibration rounds with the person; item text shows only there",
     "haipipe-labeling-rounds"),
    ("labeling", "guideline", "Guideline", "the guideline that grows from the rounds, then frozen",
     "haipipe-labeling-guideline"),
    ("quality", "test", "Test", "the executors qualified on the sealed test", "haipipe-labeling-test"),
    ("quality", "evaluation", "Evaluation", "the scores against the person's gold", "haipipe-labeling-evaluation"),
    ("quality", "audit", "Audit", "the labels audited after the scan", "haipipe-labeling-audit"),
    ("delivery", "handoff", "Handoff", "the signed Label Handoff: guideline, gold and its versions",
     "haipipe-labeling-handoff"),
    ("delivery", "scan", "Scan", "the corpus scanned under the frozen guideline", "haipipe-labeling-scan"),
    ("delivery", "final", "Final labels", "the final labels delivered", "haipipe-labeling-final-labels"),
)
VIEW = {v[1]: v for v in VIEWS}
BY_SUB = {v[2]: v for v in VIEWS}
# the engine's views on each side of the Label Handoff (s13): Scan is a scanning step, so it sits in Work Details
BUILD_WORK = ("preparation", "embedding", "definition", "rounds", "guideline")
SCAN_WORK = ("test", "evaluation", "scan", "audit")
WORK = tuple(VIEW[v] for v in BUILD_WORK + SCAN_WORK)
DELIVER = (VIEW["handoff"], VIEW["final"])

# ── the Task types of a labeling Job (b15 s13-labeling-task, JL 261014: "for the design, we have three types of
# design task, How do you think we can propose the labeling's task type?"). Read from the face's `task-type:`
# line, never from the number: keys and score are optional, so the numbers shift.
# (type, icon, what it does, the `task-type:` lines that make it, the skill that runs it)
TYPES = (
    ("items", "📦", "the corpus as items, the sealed test held back by the labeling job", ("data",),
     "haipipe-task-for-data"),
    ("keys", "🔑", "the dataset's own labels, never read by building or scanning", ("raw",), "haipipe-task-for-raw"),
    ("building", "🏗", "Contract → Rounds → G0 → Freeze → the signed Label Handoff", ("labeling-building", "labeling"),
     "haipipe-labeling-building"),
    ("scanning", "🔍", "the Handoff carried out: Test → Scan → Audit → final labels", ("labeling-scanning", "labeling"),
     "haipipe-labeling-scanning"),
    ("score", "📊", "the final labels against the keys and the raters' spread", ("eval",), "haipipe-task-for-eval"),
)
TYPE = {t[0]: t for t in TYPES}
NOTES = {"items": "📦 items: it makes the items; the labeling job holds back the sealed test from them.",
         "keys": "🔑 keys: building and scanning never read this Task; only the score Task opens it.",
         "score": "📊 score: it reads the final labels and the keys Task, and labels nothing."}
_TASK_TYPE = re.compile(r"(?m)^task-type:\s*([\w-]+)")
_STATE = re.compile(r"(?m)^state:\s*(.+)$")


def _head(task: Path) -> str:
    md = face(task)
    return md.read_text(encoding="utf-8", errors="ignore")[:3000] if md else ""


def types_of(task: Path) -> tuple:
    """The types a Task is: ("items",), ("building", "scanning") for today's one labeling Page, () for none."""
    task = Path(task)
    if not re.match(r"^t\d+_", task.name):
        return ()
    m = _TASK_TYPE.search(_head(task))
    return tuple(t[0] for t in TYPES if m and m.group(1) in t[3])


def _task_state(task: Path) -> str:
    m = _STATE.search(_head(task))
    return m.group(1).split(" · ")[0].strip() if m else ""


def _type_words(types: tuple) -> str:
    return " + ".join(f"{TYPE[t][1]} {t}" for t in types)


def _needed(made: set) -> tuple:
    """The types a Job still lacks to close: items, building and scanning; score too once it has keys."""
    need = ("items", "building", "scanning") + (("score",) if "keys" in made else ())
    return tuple(t for t in need if t not in made)


def _skill_run(view) -> dict:
    return {"label": view[2], "prompt": f"/{view[4]} {{folder}}", "skills": [view[4]]}


def _block_of(folder: Path) -> Path | None:
    for p in [folder, *folder.parents]:
        if (p / "board.md").is_file():
            return p
    return None


def _jobs(block: Path, root: Path) -> list[dict]:
    """Every labeling job of the Block, as the labeling board lists it (status only, no item text)."""
    if L is None:
        return []
    try:
        data = L.board_jobs(block, rel(block / "board.md", root))
    except Exception:                           # a broken lane must not blank the frame
        return []
    return list(data.get("jobs") or []) + [dict(e, kind="empty") for e in data.get("empty") or []]


def _job_for(task_face: Path, block: Path, root: Path) -> dict | None:
    """The labeling job whose Page is this Task's face."""
    file_q = quote(task_face.relative_to(block).as_posix())
    return next((j for j in _jobs(block, root) if f"file={file_q}" in str(j.get("labeling_url") or "")), None)


def _engine_job(task: Path, root: Path) -> dict | None:
    """The labeling job a Task works with: its own Page's, else the one whose Page sits in the same Job (a
    scanning Task carries out that job's Handoff; an items Task feeds it)."""
    md, block = face(task), _block_of(task)
    if not block:
        return None
    if md:
        own = _job_for(md, block, root)
        if own:
            return own
    job_q = quote(task.parent.relative_to(block).as_posix() + "/")
    return next((j for j in _jobs(block, root) if f"file={job_q}" in str(j.get("labeling_url") or "")), None)


def _state(job: dict) -> str:
    kind = job.get("kind")
    cls = "st-ok" if kind in ("judged",) else "st-warn" if kind in ("repair", "hold") else "mut"
    return f'<span class={cls}>{esc(job.get("badge") or "")}</span>'


def _open(url: str, label: str = "open in the Labeling workbench ↗") -> str:
    return f'<a class=chip href="{esc(url)}" target=_blank rel=noopener>{esc(label)}</a>' if url else ""


def _view_url(job: dict, view) -> str:
    url = str(job.get("labeling_url") or "")
    if not url:
        return ""
    base = url.split("&space=", 1)[0]               # an empty job's link already names Data › Preparation
    return f"{base}&space={view[0]}&view={view[1]}"


def _facts(job: dict) -> str:
    """The job's status, as the labeling board shows it: no item text."""
    if job.get("kind") == "empty":
        return table(("job", "state"), [(esc(job.get("id") or ""), _state(job))])
    g0 = job.get("g0")
    rows = [("job", esc(job.get("id") or "")), ("state", _state(job)),
            ("phase", esc(job.get("phase") or "—")),
            ("meanings confirmed (G0)", "—" if g0 is None else ('<span class=st-ok>yes</span>' if g0 else 'no')),
            ("label", esc(job.get("target") or "—")), ("corpus", esc(job.get("source") or "—")),
            ("items", esc(f'{job.get("n_dev", "—")} to label · {job.get("n_sealed", "—")} sealed')),
            ("rounds", esc(job.get("rounds", 0))), ("labeled", esc(job.get("labeled", 0))),
            ("runs", esc(job.get("runs", 0))), ("next", esc(job.get("next") or "—"))]
    return table(("", ""), rows)


def _schema_space(schema: Path, root: Path, sub: str, where: str) -> Space:
    d_sub = sub if sub in ("Scope", "Schema") else "Scope"
    html = ""                                       # Scope: the vanilla face and its fields
    if d_sub == "Schema":
        html = (f'<p class=space-reads>{esc(rel(schema, root))}</p>'
                f'<pre class=space-source>{esc(schema.read_text(encoding="utf-8", errors="replace"))}</pre>'
                if schema.is_file() else f'<p class=space-empty>No schema.yaml in this {where} yet.</p>')
    return Space(html=html, subspaces=("Scope", "Schema"), open=d_sub)


# ── Block ───────────────────────────────────────────────────────────────────────────────────────
def _block_spaces(folder: Path, root: Path, sub: str) -> dict:
    out = {"Description": _schema_space(folder / "schema.yaml", root, sub, "Block")}
    w_sub = sub if sub in ("Jobs", "Labeling") else "Jobs"
    if w_sub == "Labeling":
        jobs = _jobs(folder, root)
        rows = [(esc(j.get("id") or ""), esc(j.get("title") or ""), _state(j), esc(j.get("phase") or "—"),
                 esc(j.get("rounds", "—")), esc(j.get("next") or ""), _open(str(j.get("labeling_url") or ""), "open ↗"))
                for j in jobs]
        html = (table(("job", "Page", "state", "phase", "rounds", "next", "Labeling workbench"), rows) if rows else
                '<p class=space-empty>No Page of this Block holds a labeling job yet.</p>')
        html = '<p class=mut>Status only; a person labels in the Labeling workbench, never here.</p>' + html
    else:
        html = ""                                   # Jobs: the vanilla list of jNN_ folders
    out["Work Details"] = Space(html=html, subspaces=("Jobs", "Labeling"), open=w_sub, run_types=(
        {"label": "Prepare a corpus", "prompt": "/haipipe-labeling-preparation {folder}",
         "skills": ["haipipe-labeling-preparation"]},
        {"label": "Open a labeling job", "prompt": "/haipipe-labeling open a labeling job in {folder}",
         "skills": ["haipipe-labeling"]}))
    return out


# ── Job: its Tasks by type, and a dashed card for each type it still lacks ─────────────────────
def _missing_card(job: Path, t: str, number: int, optional: bool = False) -> str:
    _, icon, what, lines, skill = TYPE[t]
    name = f"t{number:02d}_{job.name.split('_', 1)[-1]}_{t}"
    why = "optional" if optional else "not made yet"
    return (f'<details class="topic work-task missing"><summary><span class=related-head><b>⬜ {esc(name)}</b><br>'
            f'<span class=topic-meta>{icon} {esc(t)} · {why} · {esc(what)}</span></span></summary>'
            f'<div class=work-body><p class=mut>Its face says <code>task-type: {esc(lines[0])}</code>; '
            f'<code>{esc(skill)}</code> runs it. Add it from the Runs panel.</p></div></details>')


def _job_spaces(folder: Path, root: Path, sub: str) -> dict:
    from live.frame import work_tree
    tasks = children(folder, "Job")
    made = {t for k in tasks for t in types_of(k)}
    schema = folder / "schema.yaml"
    if not made and not schema.is_file():
        return {}                                   # no labeling Job: vanilla
    out = {"Description": _schema_space(schema, root, sub, "Job")} if schema.is_file() else {}
    need = _needed(made)
    optional = tuple(t for t in ("keys", "score") if t not in made and t not in need)
    top = max([int(m.group(1)) for k in tasks if (m := re.match(r"^t(\d+)_", k.name))] or [0])
    cards = "".join(_missing_card(folder, t, top + i + 1) for i, t in enumerate(need))
    cards += "".join(_missing_card(folder, t, top + len(need) + i + 1, optional=True) for i, t in enumerate(optional))
    adds = tuple({"label": f"Add {t}", "prompt": f"Add a {t} Task to {{folder}}: a tNN_ folder whose face says "
                  f"`task-type: {TYPE[t][3][0]}` ({TYPE[t][2]}); {TYPE[t][4]} runs it.", "skills": ["haipipe-job"]}
                 for t in need + optional)
    out["Work Details"] = Space(html=work_tree("Job", folder, root, THEME) + cards, run_types=adds + (
        {"label": "Add a Task", "prompt": "Add a Task to {folder}.", "skills": ["haipipe-job"]},))
    return out


# ── Task: the items Task's results and steps (JL 261014: "show the description of the data, like the item, the raw
# data, the method of the item, and embedding") ──────────────────────────────────────────────────────────────
def _yaml_file(path: Path) -> dict:
    if yaml is None or not path.is_file():
        return {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def _item_runs(task: Path) -> list:
    """The Task's hard Runs, oldest first: (folder, its run.yaml), each a folder with its result/ (since 261010)."""
    runs = task / "runs"
    folders = sorted(p for p in runs.glob("r[0-9][0-9]_*/") if p.is_dir()) if runs.is_dir() else []
    return [(p, _yaml_file(p / "run.yaml")) for p in folders]


def _face_part(task: Path, name: str) -> str:
    """One `### N · <name> · …` part of the face's ## Content, as paragraphs and its sketch; "" when absent."""
    md = face(task)
    text = md.read_text(encoding="utf-8", errors="ignore") if md else ""
    m = re.search(rf"(?ms)^### \d+ · {re.escape(name)}\b[^\n]*\n(.*?)(?=^#{{2,4}} |\Z)", text)
    if not m:
        return ""
    out, body = [], re.sub(r"(?m)^\*\*Division map[^\n]*\n", "", m.group(1))
    for i, part in enumerate(re.split(r"(?ms)^```[^\n]*\n(.*?)^```[ \t]*$", body)):
        if i % 2:
            out.append(f'<pre class=space-source>{esc(part.rstrip())}</pre>')
        else:
            out += [f'<p>{_code(esc(" ".join(p.split())))}</p>' for p in re.split(r"\n\s*\n", part) if p.strip()]
    return "".join(out)


def _code(text: str) -> str:
    """The face's `inline code` as <code> (on text already escaped)."""
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", text)


def _value(v) -> str:
    if isinstance(v, dict):
        return " · ".join(f"{k} {_value(x)}" for k, x in v.items())
    if isinstance(v, (list, tuple)):
        return ", ".join(_value(x) for x in v)
    return f"{v:,}" if isinstance(v, int) and not isinstance(v, bool) else str(v)


def _items_facts(task: Path, root: Path) -> dict:
    """What an items Task's files say: its Runs, the newest complete one, its manifest and metrics, its scripts."""
    runs = _item_runs(task)
    done = [r for r in runs if str(r[1].get("status")) == "complete" and (r[0] / "result" / "manifest.yaml").is_file()]
    run, card = (done or [(None, {})])[-1]                     # the newest Run that made items (a read makes none)
    result = run / "result" if run else None
    metrics = L._read_json(result / "metrics.json") if result and L is not None else {}
    summary = metrics.get("summary") if isinstance(metrics.get("summary"), dict) else {}
    scripts = sorted((task / "scripts").glob("*.py")) if (task / "scripts").is_dir() else []
    return {"runs": runs, "done": done, "run": run, "card": card,
            "manifest": _yaml_file(result / "manifest.yaml") if result else {}, "metrics": metrics,
            "headline": str(summary.get("headline") or ""), "scripts": scripts,
            "config": task / "scripts" / "config" / f"{run.name}.yaml" if run else None}


def _embedding_state(job: dict | None, block: Path | None):
    """(the labeling job's lane, its embedding state or None, a summary in words); the lane may not exist yet."""
    if job is None or block is None or L is None:
        return None, None, '<span class=mut>no labeling job in this Job yet</span>'
    try:
        page = block / parse_qs(urlsplit(str(job.get("labeling_url") or "")).query)["file"][0]
        lane = L._job_root(page)[0]
        emb = L._embedding_state(lane) if lane.is_dir() else None
        return lane, emb, L._embedding_summary(emb)
    except Exception:                               # an unreadable lane: say not built, never break the frame
        return None, None, '<span class=mut>not built</span>'


# ── The items Task, as designed in b15 s41-task-items-procedure (JL 261014: "go ahead and do it"): three steps, each
# a tab in Work and in Report, in one shape: ① at a glance (big numbers, one sentence), ② the picture, ③ the details
# folded (Work only, with the step's prompt above). The base looks .stat-row and .card-row (servers/workbench/frame.py
# WORK_CSS) draw ① and ②; this theme carries no stylesheet (JL 261007).
RESULTS = ("1 · Data", "2 · Items", "3 · Embedding")
OLD_RESULT = {"Itemization": RESULTS[0], "2 · Item": RESULTS[1], "3 · Item list": RESULTS[1],
              "4 · Embedding": RESULTS[2], "Embedding": RESULTS[2]}      # links made before s41 (261014)
LIST_ROWS = 20


def _items_file(f: dict, root: Path) -> Path | None:
    store = f["metrics"].get("store") or f["manifest"].get("store")
    items = root / str(store) / "items.jsonl" if store else None
    return items if items and items.is_file() else None


def _item_rows(items: Path) -> list:
    """Every item as (id, words in its main text, turns before it, words after it, the item itself). The real text
    is shown (JL 261014: "here we want to put the real items to look, the real things"; b15 s41-D07)."""
    import json
    rows = []
    with open(items, encoding="utf-8") as handle:
        for line in handle:
            try:
                r = json.loads(line)
            except ValueError:
                continue
            if isinstance(r, dict):
                rows.append((str(r.get("item_id") or ""), len(str(r.get("main") or "").split()),
                             sum(1 for x in str(r.get("context_before") or "").splitlines() if x.strip()),
                             len(str(r.get("context_after") or "").split()), r))
    return rows


def _median(values: list) -> str:
    from statistics import median
    return f"{median(values):g}" if values else "—"


def _spread(values: list) -> str:
    return f"{_median(values)} median · {min(values)} to {max(values)}" if values else "—"


def _raw_card(task: Path) -> tuple:
    """(the newest finished Run whose Result holds a Table Card, the card), or (None, None): Step 1's own Result."""
    import json
    for run, _ in reversed(_item_runs(task)):
        d = run / "result" / "description.json"
        if d.is_file() and str(_yaml_file(run / "result" / "runtime.yaml").get("status")) == "complete":
            try:
                return run, json.loads(d.read_text(encoding="utf-8"))
            except ValueError:
                continue
    return None, None


def _cell(v) -> str:
    return "<br>".join(esc(x) for x in str(v).split("\n"))


def _stats(pairs, line: str = "") -> str:
    cells = "".join(f"<div><b>{esc(v)}</b><span>{esc(k)}</span></div>" for v, k in pairs)
    return f"<div class=stat-row>{cells}</div>" + (f"<p class=stat-line>{esc(line)}</p>" if line else "")


def _fold(title: str, meta: str, body: str) -> str:
    return (f'<details class="topic work-task"><summary><span class=related-head><b>{esc(title)}</b><br>'
            f'<span class=topic-meta>{esc(meta)}</span></span></summary><div class=work-body>{body}</div></details>')


def _brief(cols: list, row: dict) -> str:
    """A card's lines, each column with its made-up value; a long group shows its first and last column and the
    rest counted by value."""
    if len(cols) <= 6:
        return "<br>".join(f"<code>{esc(c)}</code> {_cell(row.get(c, ''))}" for c in cols)
    by: dict = {}
    for c in cols[1:-1]:
        by.setdefault(str(row.get(c, "")), []).append(c)
    middle = [f"<span class=mut>{len(cs)} more:</span> {_cell(v)}" for v, cs in by.items()]
    return "<br>".join([f"<code>{esc(cols[0])}</code> {_cell(row.get(cols[0], ''))}", *middle,
                        f"<code>{esc(cols[-1])}</code> {_cell(row.get(cols[-1], ''))}"])


RAW_ROWS = 10


def _raw_rows(root: Path, file: str) -> tuple:
    """(the header, the first RAW_ROWS rows) of the raw csv, as they are (JL 261014: "for the data I want to see the
    raw data ... to present the raw data as it is if we want"); ((), []) when it is not a readable csv."""
    import csv
    path = root / file
    if not file.endswith(".csv") or not path.is_file():
        return (), []
    with open(path, encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.reader(handle)
        head = next(reader, [])
        rows = [r for _, r in zip(range(RAW_ROWS), reader)]
    return tuple(head), rows


def _not_yet(what: str) -> tuple:
    return "", f"<p class=space-empty>{esc(what)}</p>", ""


# ── step 1 · Data: the raw file's Table Card ─────────────────────────────────────────────────────
def _data_view(task: Path, root: Path, job, block) -> tuple:
    run, card = _raw_card(task)
    if not card:
        return _not_yet("Not read yet: Step 1 writes the raw file's Table Card.")
    t, g = card.get("table") or {}, card.get("grain") or {}
    proof = g.get("proof") or {}
    units = [(f"{v:,}", k[len("distinct_"):].removesuffix("_id") + "s") for k, v in proof.items()
             if k.startswith("distinct_") and v != t.get("rows")]
    glance = _stats([(f'{t.get("rows", 0):,}', "rows"), (str(t.get("columns", "—")), "columns"), *units],
                    g.get("one_row_is") or "")
    groups = card.get("groups") or []
    rows = (card.get("synth_df") or {}).get("rows") or []
    picture = ""
    if rows:
        cards = "".join(f"<div><h4>{esc(grp['name'])}</h4><p class=mut>{esc(grp.get('meaning') or '')}</p>"
                        f"{_brief([c['name'] for c in grp.get('columns') or []], rows[0])}</div>" for grp in groups)
        picture = ("<h3>One row, drawn</h3><p class=mut>Made-up values in the real columns (synth_df), never a real "
                   "row: a chat's text is a future item, and its answers are keys.</p>"
                   f"<div class=card-row>{cards}</div>")
    columns = "".join(f"<h4>{esc(grp['name'])}</h4><p class=mut>{esc(grp.get('meaning') or '')}</p>" + table(
        ("column", "filled", "distinct", "typical values"),
        [(f"<code>{esc(c['name'])}</code>", esc(f"{c.get('filled', 0):.0%}"), esc(f"{c.get('distinct', 0):,}"),
          esc(c.get("typical") or "")) for c in grp.get("columns") or []]) for grp in groups)
    dup = proof.get("exact_duplicate_rows", 0)
    checks = (table(("check", "count"), [(esc(k.replace("_", " ")), esc(f"{v:,}")) for k, v in proof.items()])
              + ("<ul>" + "".join(f"<li>{esc(x)}</li>" for x in card.get("gotchas") or []) + "</ul>"))
    size = t.get("bytes")
    file_ = table(("", ""), [("the file", f'<code>{esc(t.get("file"))}</code>'),
                             ("what it is", esc(t.get("what_it_is") or "—")),
                             ("size", esc(f"{size / 1e6:.1f} MB" if size else "—")),
                             ("read by", f"<code>{esc(run.name)}</code>")])
    raw = _raw_rows(root, str(t.get("file") or ""))
    raw_fold = (_fold("The raw rows, as they are", f'the first {len(raw[1])} of {t.get("rows", 0):,}; real values, the '
                      "answers (keys) included",
                      "<div class=dl-src>" + table(raw[0], [tuple(_cell(v) for v in r) for r in raw[1]]) + "</div>")
                if raw[1] else "")
    picture += raw_fold                       # in Report too: the data as it is, when wanted (JL 261014)
    details = (_fold(f'The {t.get("columns", "")} columns, by group', f"{len(groups)} groups", columns)
               + _fold("Checks", f"{dup} duplicate rows · {len(card.get('gotchas') or [])} things to watch", checks)
               + _fold("The file", f'{Path(str(t.get("file"))).name} · read by {run.name}', file_))
    return glance, picture, details


# ── step 2 · Items: the recipe, one item drawn, the list ────────────────────────────────────────
def _items_view(task: Path, root: Path, job, block) -> tuple:
    f = _items_facts(task, root)
    if not f["done"]:
        return _not_yet("No items yet: Step 2 makes them, once its recipe is signed.")
    m, items = f["manifest"], _items_file(f, root)
    every = _item_rows(items) if items else []
    pairs = [(f'{m.get("items", len(every)):,}' if isinstance(m.get("items", len(every)), int) else str(m.get("items")),
              "items")]
    if every:
        pairs += [(_median([r[1] for r in every]), "words judged, median"), (_median([r[2] for r in every]),
                                                                              "turns before, median")]
    if job and job.get("n_sealed") not in (None, "—"):
        pairs.append((str(job["n_sealed"]), "held back"))
    glance = _stats(pairs, "One item = " + str(m.get("item") or "—"))
    picture = ""
    if every:
        first = every[0][4]
        picture += ("<h3>One item, drawn</h3><p class=mut>The first item, as it is: the turns before, the text that is "
                    "judged, what comes after.</p><div class=card-row>"
                    f"<div><h4>context_before</h4><p class=mut>every earlier turn</p>{_cell(first.get('context_before', ''))}</div>"
                    f"<div class=key><h4>main · {esc(every[0][0])}</h4><p class=mut>the text that is judged</p>"
                    f"{_cell(first.get('main', ''))}</div>"
                    f"<div><h4>context_after</h4><p class=mut>what comes after</p>"
                    f"{_cell(first.get('context_after') or '') or '<span class=mut>none</span>'}</div></div>")
    head = ("item", "context before", "main (judged)", "words", "turns")
    rowfmt = lambda r: (f"<code>{esc(r[0])}</code>", f"<span class=mut>{_cell(r[4].get('context_before', ''))}</span>",
                        _cell(r[4].get("main", "")), esc(r[1]), esc(r[2]))
    if every:
        picture += (f"<h3>The items</h3><p class=mut>The first {min(LIST_ROWS, len(every))} of {len(every)}, as they "
                    "are.</p>" + table(head, [rowfmt(r) for r in every[:LIST_ROWS]]))
    recipe = table(("", ""), [("one item", esc(m.get("item") or "—"))]
                   + ([("script", " · ".join(f'<code>{esc(x.relative_to(task).as_posix())}</code>' for x in f["scripts"]))]
                      if f["scripts"] else [])
                   + ([("its settings", f'<code>{esc(f["config"].relative_to(task).as_posix())}</code>')]
                      if f["config"] and f["config"].is_file() else [])) + _face_part(task, "Method")
    shown = {"source", "transform", "item", "items", "store"}
    kept = [(esc(k), esc(_value(v))) for k, v in m.items() if k not in shown]
    record = (table(("", ""), [("made by", f'<code>{esc(f["run"].name)}</code>' + (f' · {esc(f["headline"])}' if f["headline"] else "")),
                               ("stored at", f'<code>{esc(f["metrics"].get("store") or m.get("store") or "—")}</code>')]
                    + kept) + _face_part(task, "Result"))
    older = [r[0].name for r in f["runs"] if r[0] != f["run"]]
    details = (_fold("The recipe, as signed", "the face's Method part and the Run's settings", recipe)
               + (_fold(f"All {len(every)} items", "as they are",
                        f"<p class=mut>{esc('words judged: ' + _spread([r[1] for r in every]))} · "
                        f"{esc('turns before: ' + _spread([r[2] for r in every]))}</p>"
                        + table(head, [rowfmt(r) for r in every])) if every else "")
               + _fold("What the Run recorded", f'{f["run"].name} · the ground truth stays in its own files', record)
               + (_fold("Earlier Runs", f"{len(older)} Runs", esc(" · ".join(older))) if older else ""))
    return glance, picture, details


# ── step 3 · Embedding: the map (JL 261014: "why there are no embeddings, we want to see the embeddings results") ──
PALETTE = ("#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f", "#edc948", "#b07aa1", "#ff9da7", "#9c755f", "#bab0ac")


def _embed_runs(task: Path) -> list:
    """The items Task's own embedding Runs, oldest first: (folder, card, complete?), the card's type embedding-build."""
    out = []
    for run, card in _item_runs(task):
        if "embedding-build" in (card.get("type") or []):
            done = str(_yaml_file(run / "result" / "runtime.yaml").get("status")) == "complete" and \
                (run / "result" / "map.json").is_file()
            out.append((run, card, done))
    return out


def _map_svg(points: list) -> str:
    """The items as dots on the map, coloured by group; a dot's title is its id and group, never its text."""
    if not points:
        return ""
    xs, ys = [p["x"] for p in points], [p["y"] for p in points]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    w, h, pad = 900, 480, 18
    sx = lambda v: pad + (v - x0) / ((x1 - x0) or 1) * (w - 2 * pad)
    sy = lambda v: pad + (v - y0) / ((y1 - y0) or 1) * (h - 2 * pad)
    dots = "".join(f'<circle cx="{sx(p["x"]):.1f}" cy="{sy(p["y"]):.1f}" r="4" fill="{PALETTE[p["group"] % 10]}" '
                   f'fill-opacity="0.85"><title>{esc(p["item_id"])} · G{p["group"] + 1}</title></circle>' for p in points)
    return (f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px" role="img" '
            f'aria-label="the items on the map, coloured by group"><rect x="0" y="0" width="{w}" height="{h}" '
            f'fill="none" stroke="#ced4da" rx="8"/>{dots}</svg>')


def _embedding_view(task: Path, root: Path, job, block) -> tuple:
    import json
    runs = _embed_runs(task)
    built = [r for r in runs if r[2]]
    if built:
        run, card, _ = built[-1]
        res = run / "result"
        points = json.loads((res / "map.json").read_text(encoding="utf-8"))
        groups = json.loads((res / "groups.json").read_text(encoding="utf-8")) if (res / "groups.json").is_file() else []
        man = _yaml_file(res / "manifest.yaml")
        glance = _stats([(str(len(built)), "models built"), (str(man.get("groups", len(groups))), "groups"),
                         (f'{man.get("items", len(points)):,}', "items embedded")],
                        f'{str(man.get("model", "")).split("/")[-1]}: {man.get("input", "")}; a group or a place on the '
                        "map never sets a label.")
        dot = lambda g: (f'<svg width="12" height="12" aria-hidden="true"><circle cx="6" cy="6" r="5" '
                         f'fill="{PALETTE[g % 10]}"/></svg>')
        picture = ("<h3>The map</h3><p class=mut>Each dot is one item, placed by meaning; close dots read alike. "
                   "Hover a dot for its id.</p>" + _map_svg(points)
                   + "<h3>Its groups</h3>" + table(("group", "items", "words more common in it"),
                                                   [(f"{dot(g['group'])} G{g['group'] + 1}", esc(g.get("size", "")),
                                                     esc(" · ".join(g.get("keywords") or [])))
                                                    for g in groups]))
        rows = [("model", esc(man.get("model", "—"))), ("vector size", esc(man.get("dim", "—"))),
                ("input", esc(man.get("input", "—"))), ("map", esc(str(man.get("map", "—")).upper())),
                ("seed", esc(man.get("seed", "—"))), ("vectors", f'<code>{esc(man.get("vectors", "—"))}</code>'),
                ("Run", f"<code>{esc(run.name)}</code>")]
        details = _fold("The build", f'{run.name} · {str(man.get("model", "")).split("/")[-1]}', table(("", ""), rows))
        if len(built) > 1:
            details += _fold("Other models", f"{len(built) - 1} more", esc(" · ".join(r[0].name for r in built[:-1])))
        return glance, picture, details
    lane, emb, summary = _embedding_state(job, block)
    builds = (emb or {}).get("builds") or [] if isinstance(emb, dict) else []
    planned = [r for r in runs if not r[2]]
    line = ("Not built yet: its ticket is ready (" + planned[-1][0].name + "); a person presses Run, the Copy prompt "
            "above." if planned else "Not built yet: Step 3 embeds every item once per model, started by a person.")
    glance = _stats([(str(len(builds)), "models built")], line if not builds else "Built on the labeling job's lane.")
    if builds:
        src = _view_url(job, VIEW["embedding"])     # a lane build: the map, its groups and the build form
        picture = (f'<iframe class=page-view src="{esc(src)}" loading=lazy title="Embedding"></iframe>'
                   f'<p class=mut>{_open(src, "open it on its own ↗")}</p>')
    else:
        picture = ""
    details = _fold("Builds", "the labeling job's embedding record",
                    table(("", ""), [("labeling job", esc((job or {}).get("id") or "—")), ("embedding", summary)]))
    return glance, picture, details


# ── the steps: state from disk, and the prompt that runs each ───────────────────────────────────
ITEM_STEPS = (
    ("raw", "📥 Step 1 · Read the raw data", "hard", "rNN_raw_read",
     "/haipipe-task-for-description {folder}: a new rNN_raw_read Run that reads the raw files once and writes their "
     "Table Card to result/description.json: what one row is, every column by meaning group, a synth_df (made-up "
     "rows in the real columns, never a real row, since a chat's text is a future item and its answers are keys), "
     "and what to watch out for. It makes no items.", "haipipe-task-for-description", _data_view),
    ("make", "🧱 Step 2 · Make the items", "hard", "rNN_items",
     "/haipipe-task-for-data {folder}: a new rNN_items Run of scripts/items_transform.py under the recipe signed in "
     "the face's Method part and typed in its config: one item per unit (its main text, the context before and "
     "after), the ground truth in its own files, and the item check (unique ids, the context before the main text, "
     "no key inside an item) as its result gate; it writes result/manifest.yaml and metrics.json.",
     "haipipe-task-for-data", _items_view),
    ("embed", "🗺 Step 3 · Embed the items", "hard", "rNN_embedding_<model>",
     "/haipipe-labeling-embedding {folder}: run {ticket}: every item embedded once with its model, the map and its "
     "groups to result/, the vectors to the store beside the items. One Run per model; a person starts it.",
     "haipipe-labeling-embedding", _embedding_view),
)


def _step_states(task: Path, root: Path, job: dict | None, block: Path | None) -> dict:
    f = _items_facts(task, root)
    lane, emb, _ = _embedding_state(job, block)
    builds = (emb or {}).get("builds") or [] if isinstance(emb, dict) else []
    done = {"raw": _raw_card(task)[1] is not None or (bool(f["manifest"].get("source")) and bool(f["done"])),
            "make": bool(f["done"]) and f["manifest"].get("items") is not None,
            "embed": bool(builds) or any(r[2] for r in _embed_runs(task))}
    states, nexted = {}, False
    for step in ITEM_STEPS:
        states[step[0]] = "done" if done[step[0]] else ("next" if not nexted else "todo")
        nexted = nexted or not done[step[0]]
    return states


def _top_bar(i: int, task: Path, root: Path, job, block, state: str) -> str:
    key, title, kind, run_name, prompt, _, _ = ITEM_STEPS[i]
    page = ""
    if job and block:
        try:
            page = rel(block / parse_qs(urlsplit(str(job.get("labeling_url") or "")).query)["file"][0], root)
        except Exception:
            page = ""
    planned = [r for r in _embed_runs(task) if not r[2]]
    ticket = (rel(planned[-1][0] / f"{planned[-1][0].name}.sh", root) if planned
              else "a new rNN_embedding_<model> Run (its ticket, config and card, like the last one)")
    prompt = (prompt.replace("{folder}", rel(task, root)).replace("{page}", page or "the Job's labeling Page")
              .replace("{ticket}", ticket))
    chip = {"done": '<span class="st st-ok">✓ done</span>', "next": '<span class="st st-warn">→ next</span>',
            "todo": '<span class=st>· not yet</span>'}[state]
    return (f'<h3>{esc(title)}</h3><p class=topic-meta>{chip} · {esc(kind)} Run · <code>{esc(run_name)}</code></p>'
            f'<details class=run-prompt-box{" open" if state == "next" else ""}><summary>Prompt for this step '
            f'<button type=button class="run-copy work-act" data-copy="{esc(prompt)}">Copy prompt</button></summary>'
            f'<pre class=run-prompt>{esc(prompt)}</pre></details>')


def _items_spaces(folder: Path, root: Path, sub: str) -> dict:
    from live.frame import href
    job, block = _engine_job(folder, root), _block_of(folder)
    r_sub = OLD_RESULT.get(sub, sub)
    r_sub = r_sub if r_sub in RESULTS else RESULTS[0]
    i = RESULTS.index(r_sub)
    state = _step_states(folder, root, job, block)[ITEM_STEPS[i][0]]
    glance, picture, details = ITEM_STEPS[i][6](folder, root, job, block)
    if state == "todo":
        glance, picture, details = _not_yet("Not yet: the steps before it come first.")
    after = (f'<p><a class=chip href="{esc(href(folder, root, THEME, "Work Details", RESULTS[i + 1]))}">next: '
             f'{esc(ITEM_STEPS[i + 1][1])} →</a></p>' if i + 1 < len(ITEM_STEPS) else
             '<p class=mut>Then the labeling Task (🏗 building) takes these items and holds back the sealed set before '
             'its first round.</p>')
    steps = tuple({"label": s[3], "doing": s[1].split(" · ", 1)[-1],
                   "prompt": s[4].replace("{page}", "{folder}").replace("{ticket}", "its rNN_embedding_<model> ticket"),
                   "skills": [s[5]]} for s in ITEM_STEPS)
    # page=True: these views are the whole row; the base's Draft, Evidence and Value views stay off (an items Task
    # has no Draft plan; JL 261014: "we don't need draft")
    return {"Audience Report": Space(html=glance + picture, subspaces=RESULTS, open=r_sub, page=True,
                                     note="Results only: the steps, their prompts and the details are in Work."),
            "Work Details": Space(html=_top_bar(i, folder, root, job, block, state) + glance + picture + details + after,
                                  subspaces=RESULTS, open=r_sub, run_types=steps, page=True),
            "Description": Space(note=NOTES["items"])}


# ── Task: building, scanning, or today's one Page that is both ──────────────────────────────────
def _task_spaces(folder: Path, root: Path, sub: str) -> dict:
    types = types_of(folder)
    md, block = face(folder), _block_of(folder)
    if not md or not block:
        return {}
    if types == ("items",):
        return _items_spaces(folder, root, sub)
    if types and not {"building", "scanning"} & set(types):
        return {name: Space(note=NOTES[types[0]]) for name in ("Description", "Work Details")}
    job = _engine_job(folder, root) if types else _job_for(md, block, root)
    if job is None:
        return {}                                   # not a labeling job's Page: vanilla
    build, scan = "building" in types or not types, "scanning" in types or not types
    work = tuple(VIEW[v] for v in (BUILD_WORK if build else ()) + (SCAN_WORK if scan else ()))
    deliver = tuple(v for v, on in zip(DELIVER, (build, scan)) if on)
    described = VIEW["contract"] if build else VIEW["handoff"]
    out = {}
    d_names = ("Scope", described[2])
    d_sub = sub if sub in d_names else "Scope"
    out["Description"] = Space(
        html="" if d_sub == "Scope" else (_facts(job) + f'<p>{_open(_view_url(job, described))}</p>'),
        subspaces=d_names, open=d_sub, run_types=(_skill_run(described),) if d_sub != "Scope" else ())
    names = tuple(v[2] for v in work)
    w = BY_SUB[sub] if sub in names else work[0]
    out["Work Details"] = Space(
        html=(f'<p class=mut>{esc(w[3])}.</p>{_facts(job)}<p>{_open(_view_url(job, w))}</p>'),
        subspaces=names, open=w[2], run_types=(_skill_run(w),))
    dnames = ("Files",) + tuple(v[2] for v in deliver)
    if sub in dnames[1:]:
        dv = BY_SUB[sub]
        out["Delivery"] = Space(html=f'<p class=mut>{esc(dv[3])}.</p>{_facts(job)}<p>{_open(_view_url(job, dv))}</p>',
                                subspaces=dnames, open=sub, run_types=(_skill_run(dv),))
    else:
        out["Delivery"] = Space(subspaces=dnames, open="Files")    # Files: the vanilla delivery/ list
    return out


def spaces(level, folder, root, sub):
    folder, root = Path(folder).resolve(), Path(root).resolve()
    if L is None:
        return {}
    if level == "Block":
        return _block_spaces(folder, root, sub)
    if level == "Job":
        return _job_spaces(folder, root, sub)
    if level == "Task":
        return _task_spaces(folder, root, sub)
    return {}


def option(folder):
    """(label, group) for the Task ▾ dropdown: "Task · t03 · building + scanning", grouped by type (s13)."""
    types = types_of(Path(folder))
    if not types:
        return None
    return (f"Task · {Path(folder).name.split('_', 1)[0]} · {' + '.join(types)}",
            " + ".join(f"{TYPE[t][1]} {t.capitalize()}" for t in types))


def work_meta(folder, root):
    """A Task card's type and state; a Job card's types still to make (s13)."""
    folder = Path(folder)
    types = types_of(folder)
    if types:
        state = _task_state(folder)
        return esc(_type_words(types) + (f" · {state}" if state else ""))
    if re.match(r"^j\d+_", folder.name):
        made = {t for k in children(folder, "Job") for t in types_of(k)}
        need = _needed(made) if made else ()
        return esc("to make: " + ", ".join(f"{TYPE[t][1]} {t}" for t in need)) if need else ""
    return ""


def task_action(task, root):
    """A Task a person works in: a building Task's rounds, where the item text shows, or a scanning Task's audit
    (b10 s32, JL 261012: "there are special tasks that human need to interact with as well. Like the labeling")."""
    task, root = Path(task), Path(root)
    md, block = face(task), _block_of(task)
    if L is None or not md or not block:
        return None
    types = types_of(task)
    if not types:
        if _job_for(md, block, root) is None:
            return None
        types = ("building",)
    if not {"building", "scanning"} & set(types) or _engine_job(task, root) is None:
        return None
    from live.frame import href
    if "building" in types:
        return "🏷 Label", href(task, root, THEME, "Work Details", "Rounds")
    return "🔍 Audit", href(task, root, THEME, "Work Details", "Audit")


def claims(block):
    """A labeling Block wherever it sits (b61+ Blocks live in tasks/): one labeling schema, its
    schema.yaml beside board.md, or a Board Home opens as a labeling Board (board-kind labeling, or
    Pages that own labeling jobs)."""
    if (block / "schema.yaml").is_file() and (block / "board.md").is_file():
        return True
    from live.home import board_workbench_route
    return board_workbench_route(block) == "labeling-board"


# each button's Run (haipipe-run rule 6): the labeling skills' run-labeling-<operation>-<target>, the
# day dropped from the name (JL 261007), a round its own Run
RUN_NAMES = {"Prepare a corpus": "run-labeling-corpus-<corpus>", "Open a labeling job": "run-labeling-open-<job>",
             "Contract": "run-labeling-contract-<job>", "Preparation": "run-labeling-preparation-<job>",
             "Embedding": "run-labeling-embedding-<job>", "Definition": "run-labeling-definition-<job>",
             "Rounds": "run-labeling-round-<NN>", "Guideline": "run-labeling-guideline-<job>",
             "Test": "run-labeling-test-<job>", "Evaluation": "run-labeling-evaluation-<job>",
             "Audit": "run-labeling-audit-<job>", "Handoff": "run-labeling-handoff-<job>",
             "Scan": "run-labeling-scan-<job>", "Final labels": "run-labeling-final-<job>",
             "Add a Task": "run-add-<tNN>",
             **{f"Add {t[0]}": f"run-add-<tNN>-{t[0]}" for t in TYPES}}

THEME = Theme(name="labeling", label="Labeling", icon="🏷", guide="labeling", spaces=spaces, claims=claims,
              run_names=RUN_NAMES, task_action=task_action, option=option, work_meta=work_meta)
