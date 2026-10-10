"""The labeling theme on the base frame (servers/workbench/frame.py): only what differs from vanilla.

A labeling Block holds one schema (`schema.yaml`) and its Jobs; a labeling job is a Task Page whose
`labeling/` lane the subjective-label engine owns (Tools/blueprints/b01_haipipe-toolkit/j15_theme_labeling, Q01 open). Today's
Labeling workbench (labeling.py: Data · Labeling · Quality · Delivery, three views each) stays the one
place a person labels: it is the write door, gated by the engine. This theme is read only. It shows each
job's status and opens that workbench at the right view; it never renders item text and never writes.

    Block  Description: Scope · Schema (schema.yaml)
           Work Details: Jobs (vanilla) · Labeling (one status row per labeling job, labeling.board_jobs)
    Job    vanilla (its Tasks)
    Task   (a labeling job's Page)
           Description: Scope (vanilla) · Contract (the job's status facts)
           Work Details: Preparation · Embedding · Definition · Rounds · Guideline · Test · Evaluation · Audit
           Delivery: Files (vanilla) · Handoff · Scan · Final labels
           each view: the job's status, and "open in the Labeling workbench ↗" at that view; its skill
           as a run type (the panel copies a prompt and starts nothing)

Drawn in the base's look only (JL 261007: no theme stylesheet): wf-table, .chip, .mut, .space-source,
.st-ok/.st-warn. The labeling package is optional: without it this theme loads and shows vanilla.
"""
from __future__ import annotations

from pathlib import Path
from urllib.parse import quote

from live.frame import Space, Theme, esc, face, rel, table

try:                                            # the optional haipipe-labeling package (labeling.py)
    from live import labeling as L
except Exception:                               # absent or broken: the frame shows vanilla
    L = None

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
WORK = tuple(v for v in VIEWS if v[0] in ("data", "labeling", "quality") and v[1] != "contract")
DELIVER = tuple(v for v in VIEWS if v[0] == "delivery")
BY_SUB = {v[2]: v for v in VIEWS}


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


def _block_spaces(folder: Path, root: Path, sub: str) -> dict:
    out = {}
    d_sub = sub if sub in ("Scope", "Schema") else "Scope"
    if d_sub == "Schema":
        schema = folder / "schema.yaml"
        html = (f'<p class=space-reads>{esc(rel(schema, root))}</p>'
                f'<pre class=space-source>{esc(schema.read_text(encoding="utf-8", errors="replace"))}</pre>'
                if schema.is_file() else '<p class=space-empty>No schema.yaml in this Block yet.</p>')
    else:
        html = ""                                   # Scope: the vanilla face and its fields
    out["Description"] = Space(html=html, subspaces=("Scope", "Schema"), open=d_sub)
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


def _task_spaces(folder: Path, root: Path, sub: str) -> dict:
    md, block = face(folder), _block_of(folder)
    job = _job_for(md, block, root) if md and block else None
    if job is None:
        return {}                                   # not a labeling job's Page: vanilla
    out = {}
    d_sub = sub if sub in ("Scope", "Contract") else "Scope"
    contract = BY_SUB["Contract"]
    out["Description"] = Space(
        html="" if d_sub == "Scope" else (_facts(job) + f'<p>{_open(_view_url(job, contract))}</p>'),
        subspaces=("Scope", "Contract"), open=d_sub,
        run_types=(_skill_run(contract),) if d_sub == "Contract" else ())
    names = tuple(v[2] for v in WORK)
    w = BY_SUB[sub] if sub in names else WORK[0]
    out["Work Details"] = Space(
        html=(f'<p class=mut>{esc(w[3])}.</p>{_facts(job)}<p>{_open(_view_url(job, w))}</p>'),
        subspaces=names, open=w[2], run_types=(_skill_run(w),))
    dnames = ("Files",) + tuple(v[2] for v in DELIVER)
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
    if level == "Task":
        return _task_spaces(folder, root, sub)
    return {}                                       # a Job: vanilla, its Tasks


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
             "Scan": "run-labeling-scan-<job>", "Final labels": "run-labeling-final-<job>"}

THEME = Theme(name="labeling", label="Labeling", icon="🏷", guide="labeling", spaces=spaces, claims=claims,
              run_names=RUN_NAMES)
