"""Read a plan-C insight Board and its Prototype Block from disk (b11 s00 · s11 · s12 · s13, 261007).

Plan C: the Prototype (questions + scripts) is its own work Block, `work/bNN_<topic>_prototype/`, whose
Jobs are versions `j0N_pN/` (release.yaml · partitions.md · thresholds.yaml · the questions' Tasks). The
insight Board, `insights/bNN_<topic>/`, holds one dataset with dated versions (board.md `dataset:`,
`versions:`, `prototype:`); its Jobs `j0N_pN_<d>vM/` pin one Prototype version and one data version; a
Job's Tasks are its questions, their hard Runs `runs/rNN_<partition>/`; the Job's `reports/vs-<prev>.md`
is written by its run-compare. Read-only: this module only reads.
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

JOB_NAME = re.compile(r"^j\d+_(p\d+)_(.+?)(v\d+)$")
TASK_NAME = re.compile(r"^t\d+_([DIKW]\d+)_")
LEVEL_OF = {"D": "data", "I": "information", "K": "knowledge", "W": "wisdom"}


Loader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)      # the C parser when PyYAML has it
_PARSED: dict = {}                                             # {path: (mtime, size, parsed)}: a file is parsed once per change


def _parsed(path: Path, fm: bool):
    """A file's YAML (or a Markdown file's front matter), parsed once until the file changes."""
    try:
        st = path.stat()
    except OSError:
        return {}
    key = (str(path), fm)
    hit = _PARSED.get(key)
    if hit and hit[0] == st.st_mtime_ns and hit[1] == st.st_size:
        return hit[2]
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
        if fm:
            m = re.match(r"(?s)^---\n(.*?)\n---\n", text)
            text = m.group(1) if m else ""
        out = (yaml.load(text, Loader=Loader) or {}) if text else {}
    except (OSError, yaml.YAMLError):
        out = {}
    _PARSED[key] = (st.st_mtime_ns, st.st_size, out)
    return out


def front(md: Path) -> dict:
    """The YAML front matter of a Markdown file ({} without one)."""
    out = _parsed(Path(md), True)
    return dict(out) if isinstance(out, dict) else {}


def _yaml(path: Path) -> dict:
    out = _parsed(Path(path), False)
    return dict(out) if isinstance(out, dict) else {}


def _project(block: Path) -> Path:
    return block.parent.parent


def is_plan_c(block: Path) -> bool:
    """A Board laid out by plan C: board.md names its prototype, or a Job pairs a release and a version."""
    if not (block / "board.md").is_file():
        return False
    if front(block / "board.md").get("prototype"):
        return True
    return any(p.is_dir() and JOB_NAME.match(p.name) for p in block.iterdir())


def run_card(run_dir: Path) -> dict:
    card = _yaml(run_dir / "run.yaml") if run_dir.is_dir() else {}
    name = run_dir.name
    card.setdefault("run", name)
    card.setdefault("kind", "soft" if name.startswith("run-") else "hard")
    card.setdefault("status", "—")
    card["path"] = run_dir
    card["report"] = run_dir / "result" / "report.md" if (run_dir / "result" / "report.md").is_file() else None
    return card


def runs(folder: Path) -> list:
    rdir = folder / "runs"
    return [run_card(p) for p in sorted(rdir.iterdir()) if p.is_dir() and not p.name.startswith((".", "_"))] \
        if rdir.is_dir() else []


# ── the Prototype Block ─────────────────────────────────────────────────────────────────────────
def prototype(block: Path) -> dict:
    """{path, releases: [{name, job, face, questions: {qid: {...}}, partitions, thresholds}], proposals}."""
    path = _project(block) / str(front(block / "board.md").get("prototype", ""))
    out = {"path": path, "releases": [], "proposals": []}
    if not path.is_dir():
        return out
    for job in sorted(p for p in path.iterdir() if p.is_dir() and re.match(r"^j\d+_p\d+(_.+)?$", p.name)):
        rel = _yaml(job / "release.yaml")
        qs = {}
        for qid, row in (rel.get("questions") or {}).items():
            task = (job / str(row.get("task", ""))).resolve()
            q = front(task / "question.md")
            qs[qid] = {"id": qid, "level": q.get("level") or LEVEL_OF.get(qid[0], ""), "question": q.get("question", ""),
                       "method": q.get("method") or {}, "signed": q.get("signed", ""), "agreed": q.get("agreed", ""),
                       "change": row.get("change", ""), "task": task, "file": task / "question.md"}
        out["releases"].append({"name": rel.get("release") or job.name.split("_")[1], "job": job,
                                "face": front(job / f"{job.name}.md"), "questions": qs,
                                "partitions": front(job / "partitions.md").get("partitions") or [],
                                "thresholds": _yaml(job / "thresholds.yaml")})
    pdir = path / "proposals"
    if pdir.is_dir():
        out["proposals"] = [dict(front(p), file=p, title=p.stem) for p in sorted(pdir.glob("*.md")) if p.name != "README.md"]
    return out


def release(proto: dict, name: str) -> dict:
    return next((r for r in proto["releases"] if r["name"] == name), {"name": name, "questions": {}, "partitions": [],
                                                                     "thresholds": {}, "face": {}, "job": None})


# ── the Board and its Jobs ──────────────────────────────────────────────────────────────────────
def _carried(folder: Path) -> bool:
    """A Job or Task carried over from today's register board (insight_carry.py): pointers only."""
    return bool(front(folder / f"{folder.name}.md").get("carried"))


def task(tdir: Path) -> dict:
    if _carried(tdir):
        from live import insight_carry
        return insight_carry.task(tdir)
    page = tdir / f"{tdir.name}.md"
    m = TASK_NAME.match(tdir.name)
    fm = front(page)
    rr = runs(tdir)
    return {"name": tdir.name, "path": tdir, "qid": (m.group(1) if m else fm.get("question", "")),
            "page": page if page.is_file() else None, "face": fm,
            "hard": [r for r in rr if r["kind"] == "hard"], "soft": [r for r in rr if r["kind"] == "soft"]}


def vs_report(jdir: Path) -> dict:
    """reports/vs-<prev>.md: {file, face, rows: {qid: {previous, this, status, why}}}."""
    files = sorted((jdir / "reports").glob("vs-*.md")) if (jdir / "reports").is_dir() else []
    if not files:
        return {}
    text = files[0].read_text(encoding="utf-8", errors="ignore")
    rows = {}
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 5 and re.match(r"^[DIKW]\d+$", cells[0]):
            rows[cells[0]] = {"previous": cells[1], "this": cells[2], "status": cells[3], "why": cells[4]}
    return {"file": files[0], "face": front(files[0]), "rows": rows}


def job(jdir: Path) -> dict:
    if _carried(jdir):
        from live import insight_carry
        return insight_carry.job(jdir)
    m = JOB_NAME.match(jdir.name)
    fm = front(jdir / f"{jdir.name}.md")
    tasks = [task(t) for t in sorted(jdir.iterdir()) if t.is_dir() and TASK_NAME.match(t.name)]
    return {"name": jdir.name, "path": jdir, "face": fm, "release": fm.get("release") or (m.group(1) if m else ""),
            "data": fm.get("data") or (m.group(3) if m else ""), "state": fm.get("state", "open"),
            "moved": fm.get("moved", ""), "previous": fm.get("previous", ""), "tasks": tasks,
            "runs": runs(jdir), "vs": vs_report(jdir)}


def board(block: Path) -> dict:
    if any(_carried(p) for p in block.iterdir() if p.is_dir() and JOB_NAME.match(p.name)):
        from live import insight_carry
        return insight_carry.board(block)
    fm = front(block / "board.md")
    jobs = [job(p) for p in sorted(block.iterdir()) if p.is_dir() and JOB_NAME.match(p.name)]
    reports = sorted((block / "reports").glob("q*/q*.md")) if (block / "reports").is_dir() else []
    handoffs = [dict(front(h), file=h) for h in sorted((block / "delivery").glob("*.md"))] \
        if (block / "delivery").is_dir() else []
    return {"path": block, "face": fm, "dataset": fm.get("dataset", ""), "versions": fm.get("versions") or [],
            "accumulates": fm.get("accumulates", ""), "jobs": jobs, "runs": runs(block),
            "reports": [dict(front(r), file=r, slug=r.parent.name) for r in reports], "handoffs": handoffs,
            "prototype": prototype(block)}


def job_board(jdir: Path) -> Path:
    return jdir.parent


def task_job(tdir: Path) -> Path:
    return tdir.parent


def question_of(proto: dict, rel: str, qid: str) -> dict:
    return release(proto, rel)["questions"].get(qid, {"id": qid, "level": LEVEL_OF.get(qid[:1], ""), "question": "",
                                                          "method": {}, "change": "", "file": None})
