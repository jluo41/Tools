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


# ── a data version's sample rows ────────────────────────────────────────────────────────────────
# a column that names a person, a place or a record, or holds free text, is never shown (JL 261008: "preview
# some data examples ... randomly a few lines"); a version's `preview:` list picks the readable ones first
HIDDEN = re.compile(r"(^|_)(id|ids|encoded|npi|zip\w*|phone|email|address|ssn|mrn|dob)($|_)|_id$|_encoded$|zip|npi",
                    re.I)
_SAMPLES: dict = {}                                            # {(path, mtime, n, seed): sample}


def _cell(v) -> str:
    """One value as the page shows it: a date to the day, a whole float without .0, a missing one as —."""
    import datetime as dt
    import math
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return "—"
    if isinstance(v, dt.datetime):
        return v.strftime("%Y-%m-%d")
    if isinstance(v, float):
        return f"{v:g}"
    return str(v)


DOC_EXT = (".md", ".txt")
TABLE_EXT = (".csv", ".tsv")
IMAGE_EXT = (".png", ".jpg", ".jpeg", ".svg", ".gif")


def version_folder(v: dict, root: Path) -> Path | None:
    """A data version's folder (JL 261008: "I give you the folder of the data, and you can see all the
    things"): board.md `folder:`, else the folder of its `extract:` file."""
    if v.get("folder"):
        return (Path(root) / str(v["folder"])).resolve()
    if v.get("extract"):
        return (Path(root) / str(v["extract"])).resolve().parent
    return None


def data_folder(folder: Path, extract: str = "") -> dict:
    """What a data version's folder holds, by role: {path, data (the extract), manifest, dictionary (rows of
    data_dictionary.csv), summary (cohort_summary.txt), figures, docs, tables, other}. The extract is the
    version's `extract:`, else the manifest's `output_file`, else the one data file on top. A folder or file
    whose name starts with `_` or `.` is someone's work beside the version: listed under other, never read."""
    import csv
    import json
    folder = Path(folder)
    out = {"path": folder, "data": None, "manifest": {}, "dictionary": [], "summary": "", "figures": [],
           "docs": [], "tables": [], "other": []}
    if not folder.is_dir():
        return out
    try:
        out["manifest"] = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        pass
    if (folder / "data_dictionary.csv").is_file():
        with (folder / "data_dictionary.csv").open(encoding="utf-8", errors="replace", newline="") as fh:
            out["dictionary"] = list(csv.DictReader(fh))
    if (folder / "cohort_summary.txt").is_file():
        out["summary"] = (folder / "cohort_summary.txt").read_text(encoding="utf-8", errors="replace")
    named = Path(extract).name if extract else str(out["manifest"].get("output_file") or "")
    tops = sorted(folder.iterdir(), key=lambda p: p.name.lower())
    data = [p for p in tops if p.is_file() and p.suffix.lower() in (".parquet", ".feather")]
    out["data"] = next((p for p in data if p.name == named), data[0] if len(data) == 1 else None)
    known = {"manifest.json", "data_dictionary.csv", "cohort_summary.txt"}
    for p in tops:
        if p.name.startswith((".", "_")):
            out["other"].append(p)
        elif p.is_dir() and any(f.suffix.lower() in IMAGE_EXT for f in p.iterdir() if f.is_file()):
            out["figures"] += sorted(f for f in p.iterdir() if f.suffix.lower() in IMAGE_EXT)
        elif p.is_dir():
            files = sorted(f for f in p.rglob("*") if f.is_file() and not f.name.startswith("."))
            out["docs"] += [f for f in files if f.suffix.lower() in DOC_EXT]
            out["other"] += [f for f in files if f.suffix.lower() not in DOC_EXT]
        elif p.name in known or p == out["data"]:
            continue
        elif p.suffix.lower() in DOC_EXT:
            out["docs"].append(p)
        elif p.suffix.lower() in TABLE_EXT:
            out["tables"].append(p)
        elif p.suffix.lower() in IMAGE_EXT:
            out["figures"].append(p)
        else:
            out["other"].append(p)
    seen = set()                                               # the same document twice (a copy in raw_docs/): once
    out["docs"] = [d for d in out["docs"] if not ((d.name, d.stat().st_size) in seen or seen.add((d.name, d.stat().st_size)))]
    return out


def sample_rows(extract: Path, n: int = 5, seed: int = 0, hide: tuple = ()) -> dict:
    """`n` rows of a version's extract, drawn at random with a fixed seed (the same rows on every load):
    {columns, rows, hidden, total} or {} when the file cannot be read. Columns that identify (ids, NPI, zip,
    contact), that `hide` names (the data dictionary's identity group) or that hold free text are left out
    and counted in `hidden`. Read once per file change."""
    path = Path(extract)
    try:
        st = path.stat()
    except OSError:
        return {}
    key = (str(path), st.st_mtime_ns, n, seed, tuple(hide))
    if key in _SAMPLES:
        return _SAMPLES[key]
    try:
        import numpy as np
        import pyarrow.parquet as pq
        f = pq.ParquetFile(path)
        total = f.metadata.num_rows
        names = f.schema_arrow.names
        keep = [c for c in names if not HIDDEN.search(c) and c not in hide]
        idx = np.sort(np.random.RandomState(seed).choice(total, min(n, total), replace=False))
        tab = f.read(columns=keep).take(idx).to_pylist()
    except Exception:                                          # not parquet, unreadable, no pyarrow: no sample
        _SAMPLES[key] = {}
        return {}
    free = {c for c in keep if any(isinstance(r[c], str) and len(r[c]) > 100 for r in tab)}  # free text
    cols = [c for c in keep if c not in free]
    out = {"columns": cols, "rows": [[_cell(r[c]) for c in cols] for r in tab],
           "hidden": [c for c in names if c not in cols], "total": total}
    _SAMPLES[key] = out
    return out


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
        name = rel.get("release") or job.name.split("_")[1]
        slug = job.name.split("_", 2)[2] if job.name.count("_") >= 2 else ""
        face = front(job / f"{job.name}.md")                # its title (`title:`), else the folder's slug
        title = face.get("title") or slug
        out["releases"].append({"name": name, "slug": slug, "label": f"{name} - {title}" if title else name, "job": job,
                                "face": face, "questions": qs,
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
