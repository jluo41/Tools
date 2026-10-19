"""The labeling theme on the base frame (servers/workbench/frame.py): only what differs from vanilla.

A labeling Job is one dataset × one label (`jNN_<dataset>_<label>/`, its `schema.yaml`); each of its Tasks
is one of five types, read from the face's `task-type:` line (Tools/blueprints/b15_theme_labeling,
s13-labeling-task): items · ground truth · building · scanning · score. Today's one labeling Page
(`task-type: labeling`) is building and scanning at once; the engine's own Labeling workbench (labeling.py:
Data · Labeling · Quality · Delivery) stays the one place a person labels: it is the write door, gated by
the engine. This theme shows each Task's type and state, the types a Job still lacks, and opens that workbench
at the right view. An items Task is the exception (b15 s41): its tabs show the real rows and items (s41-D07), and
a person's Sign, Agree and Draw again go through LabelingMixin's two narrow routes (/_board/labeling/items and
/_board/labeling/sample), which call haipipe-labeling-preparation's engine (items_task.py).

    Block  Description: Scope · Schema (schema.yaml)
           Work Details: Jobs (vanilla) · Labeling (one status row per labeling job, labeling.board_jobs)
    Job    Description: Scope · Schema (the Job's schema.yaml)
           Work Details: its Tasks, each with its type and state, then a dashed card per type still to make
    Task   by its type, drawn by workbench-task-labeling/task_labeling.py (b32 s41-D15):
           items     three steps, each a tab in Work and Report (b15 s41): 1 · Data · 2 · Items · 3 · Embedding;
                     Work: the step (what we have · the recipe or build to sign · the prompt with notes), folded once
                     done, then one card per topic; Report: the cards only
           ground_truth  vanilla; a note that building and scanning never read it
           building  four Stages, each a tab in Work and Report (b15 s42): 1 · Contract · 2 · Initial Labeling
                     Definition · 3 · Rounds · 4 · Handoff; Work: the Stage (its Input with each 👁 reading budget,
                     the prompt with notes), then its Result cards; a Sign or a ruling opens the Labeling
                     workbench; Description: Scope · Contract; Delivery: Files · Handoff
           scanning  Description: Scope · Handoff; Work Details: Test · Evaluation · Scan · Audit;
                     Delivery: Files · Final labels
           score     vanilla; a note that it reads the final labels and the ground truth
           each engine view: the job's status, and "open in the Labeling workbench ↗" at that view; its skill
           as a run type (the panel copies a prompt and starts nothing)

Drawn in the base's look only (JL 261007: no theme stylesheet): wf-table, .chip, .mut, .space-source,
.st-ok/.st-warn, .topic.missing. The labeling package is optional: without it this theme loads and shows vanilla.
"""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

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
# line, never from the number: ground truth and score are optional, so the numbers shift ("keys" until JL 261014:
# "could we do not use the term of key").
# (type, icon, what it does, the `task-type:` lines that make it, the skill that runs it)
TYPES = (
    ("items", "📦", "the corpus as items, the sealed test held back by the labeling job", ("data", "items"),
     "haipipe-labeling-preparation"),                       # its one main skill (b15 s41-D11)
    ("ground_truth", "📏", "the dataset's own labels, never read by building or scanning", ("raw",),
     "haipipe-task-for-raw"),
    ("building", "🏗", "Contract → Rounds → G0 → Freeze → the signed Label Handoff", ("labeling-building", "labeling"),
     "haipipe-labeling-building"),
    ("scanning", "🔍", "the Handoff carried out: Test → Scan → Audit → final labels", ("labeling-scanning", "labeling"),
     "haipipe-labeling-scanning"),
    ("score", "📊", "the final labels against the experts' gold and the raters' spread", ("eval",), "haipipe-task-for-eval"),
)
TYPE = {t[0]: t for t in TYPES}
NOTES = {"items": "📦 items: it makes the items; the labeling job holds back the sealed test from them.",
         "ground_truth": "📏 ground truth: building and scanning never read this Task; only the score Task opens it.",
         "score": "📊 score: it reads the final labels and the ground truth Task, and labels nothing."}
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
    return " + ".join(f"{TYPE[t][1]} {t.replace('_', ' ')}" for t in types)


def _needed(made: set) -> tuple:
    """The types a Job still lacks to close: items, building and scanning; score too once it has ground truth."""
    need = ("items", "building", "scanning") + (("score",) if "ground_truth" in made else ())
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
            f'<span class=topic-meta>{icon} {esc(t.replace("_", " "))} · {why} · {esc(what)}</span></span></summary>'
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
    optional = tuple(t for t in ("ground_truth", "score") if t not in made and t not in need)
    top = max([int(m.group(1)) for k in tasks if (m := re.match(r"^t(\d+)_", k.name))] or [0])
    cards = "".join(_missing_card(folder, t, top + i + 1) for i, t in enumerate(need))
    cards += "".join(_missing_card(folder, t, top + len(need) + i + 1, optional=True) for i, t in enumerate(optional))
    adds = tuple({"label": f"Add {t.replace('_', ' ')}", "prompt": f"Add a {t.replace('_', ' ')} Task to {{folder}}: a tNN_ folder whose face says "
                  f"`task-type: {TYPE[t][3][0]}` ({TYPE[t][2]}); {TYPE[t][4]} runs it.", "skills": ["haipipe-job"]}
                 for t in need + optional)
    out["Work Details"] = Space(html=work_tree("Job", folder, root, THEME) + cards, run_types=adds + (
        {"label": "Add a Task", "prompt": "Add a Task to {folder}.", "skills": ["haipipe-job"]},))
    return out


# ── Task: the items Task's results and steps (JL 261014: "show the description of the data, like the item, the raw
# data, the method of the item, and embedding") ──────────────────────────────────────────────────────────────
def spaces(level, folder, root, sub):
    folder, root = Path(folder).resolve(), Path(root).resolve()
    if L is None:
        return {}
    if level == "Block":
        return _block_spaces(folder, root, sub)
    if level == "Job":
        return _job_spaces(folder, root, sub)
    return {}                                   # a Task: workbench-task-labeling/task_labeling.py (s41-D15)


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
