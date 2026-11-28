"""Read a plan-C insight Board and its Question Book Block from disk (b11 s00 · s11 · s12 · s13, 261007).

Plan C: the Question Book (questions + scripts) is its own work Block, `work/bNN_<topic>_prototype/`, whose
Jobs are versions `j0N_pN/` (release.yaml · partitions.md · thresholds.yaml · the questions' Tasks). The
insight Board, `insights/bNN_<topic>/`, holds one dataset with dated versions (board.md `dataset:`,
`versions:`, `prototype:`); its Jobs `jNN_question-vN-<slug>_data-vM/` pin one Question Book version and
one data version; a Job's Tasks are its questions, their hard Runs `runs/rNN_<segment>/`; the Job's
`reports/vs-<prev>.md` is written by its run-compare. Read-only: this module only reads.
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

# a Board Job's folder: jNN_question-vN-<release slug>_data-vM, read left to right; underscores part its three
# fields, hyphens join the words inside one. The older jNN_prototype-pN-<slug>_data-<D>vM and jNN_pN_<D>vM still read,
# until hai-insight ref/rename_code_data.py carries their Board over. Groups: release, dataset ('' in the new name),
# version (hai-insight ref/open_job.py writes the name).
class _Either:
    """Two patterns read as one: the first that matches (re has no branch reset, so the groups stay numbered alike)."""

    def __init__(self, *pats):
        self.pats = pats

    def match(self, s):
        return next((m for m in (p.match(s) for p in self.pats) if m), None)


JOB_NAME = _Either(re.compile(r"^j\d+_((?:question|code)-v\d+)(?:-[a-z0-9-]+)?_()(data-v\d+)$"),
                   re.compile(r"^j\d+_(?:prototype-)?(p\d+)(?:-[a-z0-9-]+)?_(?:data-)?(.+?)(v\d+)$"))
RELEASE_NAME = re.compile(r"^j\d+_(?:question-v|code-v|p)\d+(_.+)?$")     # a Question Book's Job, one question version
TASK_NAME = re.compile(r"^t\d+_([DIKWX]\d+)_")
LEVEL_OF = {"X": "executive", "D": "data", "I": "information", "K": "knowledge", "W": "wisdom"}


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
    if card["status"] == "refused" and not card.get("reason"):       # a card written before run_job.py kept the reason
        card["reason"] = str(_yaml(run_dir / "result" / "runtime.yaml").get("reason") or "")
    card["path"] = run_dir
    card["report"] = next((f for f in (run_dir / "result" / "tables.md", run_dir / "result" / "report.md")  # generated;
                           if f.is_file()), None)                                     # report.md before 261120
    card["run_report"] = run_report(run_dir)
    return card


# ── a Run's report: an agent's reading of its result, beside result/ (workbench-insight T31) ──────────
def result_hash(run_dir: Path) -> str:
    """The result's content, as hai-insight ref/run_report.py result_hash pins it (a test keeps the two equal)."""
    import hashlib
    rec = _yaml(run_dir / "result" / "runtime.yaml")
    if rec.get("tables_sha256"):
        return str(rec["tables_sha256"])
    h = hashlib.sha256(f"{rec.get('status')}\n{rec.get('reason') or ''}\n".encode())
    res = run_dir / "result"
    for f in sorted(res.rglob("*")) if res.is_dir() else []:
        if f.is_file() and f.suffix in (".csv", ".json") and "provenance" not in f.relative_to(res).parts:
            h.update(f.relative_to(res).as_posix().encode() + b"\n" + f.read_bytes())
    return h.hexdigest()


def run_report(run_dir: Path) -> dict | None:
    """runs/rNN_<segment>/report.md: {path, headline, sentences, caveat, check, carried, stale}; None when unwritten.
    A rerun keeps it (the ticket clears only result/); a result that changed since makes it stale."""
    md = run_dir / "report.md"
    fm = front(md) if md.is_file() else {}
    if not str(fm.get("headline") or "").strip():
        return None
    return {"path": md, "headline": str(fm["headline"]).strip(), "sentences": fm.get("sentences") or [],
            "caveat": str(fm.get("caveat") or ""), "check": str(fm.get("check") or ""),
            "carried": str(fm.get("carried-from") or ""), "stale": str(fm.get("result-sha256")) != result_hash(run_dir)}


def report_headline(run: dict) -> str:
    """A Run card's report headline, '' when it has none or the result changed after it was written."""
    rep = run.get("run_report")
    return rep["headline"] if rep and not rep["stale"] else ""


def runs(folder: Path) -> list:
    rdir = folder / "runs"
    return [run_card(p) for p in sorted(rdir.iterdir()) if p.is_dir() and not p.name.startswith((".", "_"))] \
        if rdir.is_dir() else []


# ── a data version on a page: shapes, counts and names, never a record value (workbench-insight T19) ──────
# No row of a data version is drawn onto a page, and a dictionary's sample column is dropped as it is read: a page is
# also what a session reads when it checks one, so a row on a page is a row in that session's context.
SAMPLE_KEYS = {"sample_value", "sample", "samples", "example", "example_value", "examples", "first_value", "top_values"}


DOC_EXT = (".md", ".txt")
TABLE_EXT = (".csv", ".tsv")
IMAGE_EXT = (".png", ".jpg", ".jpeg", ".svg", ".gif")


def version_folder(v: dict, root: Path, board: Path | None = None) -> Path | None:
    """A data version's folder (it holds everything about the version, so the page reads the
    folder): board.md `folder:`, else the folder of its `extract:` file. The path is SPACE-relative; it is
    found against the served root, else the Board's own folder, else the root with a leading `Tools/` dropped,
    so a server rooted at the Tools checkout reads a blueprint's data too (round 1, 261106)."""
    ref = str(v.get("folder") or v.get("extract") or "")
    if not ref or ref.startswith("/") or ".." in Path(ref).parts:
        return None
    tries = [Path(root) / ref]
    if board is not None:
        tries.append(Path(board) / ref)
    if ref.startswith("Tools/"):
        tries.append(Path(root) / ref[len("Tools/"):])
    for t in tries:
        hit = t.resolve() if v.get("folder") else t.resolve().parent
        if hit.is_dir():
            return hit
    return tries[0].resolve() if v.get("folder") else tries[0].resolve().parent


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
            out["dictionary"] = [{k: v for k, v in row.items() if (k or "").strip().lower() not in SAMPLE_KEYS}
                                 for row in csv.DictReader(fh)]
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



# ── the Question Book Block ─────────────────────────────────────────────────────────────────────────
def prototype(block: Path) -> dict:
    """{path, releases: [{name, job, face, questions: {qid: {...}}, segments, thresholds}], proposals}."""
    return prototype_at(_project(block) / str(front(block / "board.md").get("prototype", "")))


def prototype_at(path: Path) -> dict:
    """The Question Book Block at `path`, read as prototype() reads the one a Board names."""
    out = {"path": path, "releases": [], "proposals": []}
    if not path.is_dir():
        return out
    for job in sorted(p for p in path.iterdir() if p.is_dir() and RELEASE_NAME.match(p.name)):
        rel = _yaml(job / "release.yaml")
        qs = {}
        for qid, row in (rel.get("questions") or {}).items():
            task = (job / str(row.get("task", ""))).resolve()
            q = front(task / "question.md")
            qs[qid] = {"id": qid, "level": q.get("level") or LEVEL_OF.get(qid[0], ""), "question": q.get("question", ""),
                       "method": q.get("method") or {}, "signed": q.get("signed", ""), "agreed": q.get("agreed", ""),
                       "change": row.get("change", ""), "task": task, "file": task / "question.md",
                       "ask": q.get("ask", ""), "name": q.get("name", ""), "needs": q.get("needs") or {},
                       "asked": (q.get("partitions") or {}).get("asked") if isinstance(q.get("partitions"), dict) else ""}
        name = rel.get("release") or job.name.split("_")[1]
        slug = job.name.split("_", 2)[2] if job.name.count("_") >= 2 else ""
        face = front(job / f"{job.name}.md")                # its title (`title:`), else the folder's slug
        title = face.get("title") or slug.replace("-", " ")
        code = plan_code(name)
        out["releases"].append({"name": name, "slug": slug, "code": code, "words": title,
                                "label": f"{code} · {title}" if title else code, "job": job,
                                "face": face, "questions": qs,
                                "partitions": front(job / "partitions.md").get("partitions") or [],
                                "thresholds": _yaml(job / "thresholds.yaml")})
    pdir = path / "proposals"
    if pdir.is_dir():
        out["proposals"] = [dict(front(p), file=p, title=p.stem) for p in sorted(pdir.glob("*.md")) if p.name != "README.md"]
    return out


# ── the words a person reads: the screen, the folders and the
# files say the same id; an older Board's pN and vM read as question-vN and data-vM until it is carried over ──────────
def plan_code(release: str) -> str:
    """A question version (a release) as it is written everywhere: `question-v1` (an older `p1` reads the same)."""
    return re.sub(r"^(?:p|code-v)(\d+)$", r"question-v\1", str(release or ""))


def freeze_code(version: str) -> str:
    """A data version as it is written everywhere: `data-v1` (an older `v1` reads the same)."""
    return re.sub(r"^v(\d+)$", r"data-v\1", str(version or ""))


def freeze_words(v: dict) -> str:
    """A data version's few words: its `label:`, else the start of `new:` up to a colon."""
    words = str(v.get("label") or str(v.get("new") or "").split(":")[0]).strip()
    return "" if words.startswith("<") else words              # a scaffold placeholder is no words


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
            "hard": [r for r in rr if r["kind"] == "hard" and r.get("type") != "collect"],   # a segment's Run, never a
            "soft": [r for r in rr if r["kind"] == "soft"]}                                   # collection Run (🙋)


def vs_report(jdir: Path) -> dict:
    """reports/vs-<prev>.md: {file, face, rows: {qid: {previous, this, status, why}}}."""
    files = sorted((jdir / "reports").glob("vs-*.md")) if (jdir / "reports").is_dir() else []
    if not files:
        return {}
    text = files[0].read_text(encoding="utf-8", errors="ignore")
    rows = {}
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 5 and re.match(r"^[DIKWX]\d+$", cells[0]):
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
    handoffs = [dict(front(h), file=h) for h in sorted((block / "delivery").glob("*.md"))
                if h.name != "delivery.md"] if (block / "delivery").is_dir() else []   # delivery.md: the folder's table
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
