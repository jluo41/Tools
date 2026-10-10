"""Project Tasks — the work linked to a console scope, read off the project ladder.

A project's work is a ladder (the haipipe project skill): Blocks hold Jobs, Jobs hold Tasks.

    <root>/examples-*/Project-*/tasks/bNN_<block>/jNN_<job>/tNN_<task>/tNN_<task>.md     the Task's face

The individual/group split is per TASK: the face's `scope: individual|group` header line says it; with no
such line, a `task-type:` naming individual work counts as individual, and anything else as group (most
data, fit and eval work is cohort-level). The older flat layout (`examples/Project-*/tasks/<A01_*>`, a
letter series) is still read as a fallback, for projects not yet on the ladder (j02 Q03, decided 261009).

Configuration, by environment like the rest of the service:

    INLAB_PROJECTS_ROOT   the SPACE root, or any folder holding examples-*/ (or Project-* folders).
                          Unset ⇒ walk up from this file looking for one.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/api")

_SERIES_RE = re.compile(r"^([A-Z])(\d{1,3})_(.+)$")


# ── project discovery ────────────────────────────────────────────────────────

def _projects_root() -> Path | None:
    env = os.environ.get("INLAB_PROJECTS_ROOT")
    if env:
        p = Path(env).expanduser().resolve()
        return p if p.is_dir() else None
    # walk up looking for a dir that holds projects, on the ladder or flat
    for base in Path(__file__).resolve().parents:
        if any(base.glob("examples-*/Project-*/tasks")):
            return base
        cand = base / "examples"
        if cand.is_dir() and any(cand.glob("Project-*")):
            return cand
        if any(base.glob("Project-*/tasks")):
            return base
    return None


def _projects() -> list[Path]:
    root = _projects_root()
    if not root:
        return []
    found = list(root.glob("examples-*/Project-*")) + list(root.glob("Project-*")) + \
        list(root.glob("examples/Project-*"))
    return sorted({p for p in found if (p / "tasks").is_dir()}, key=lambda p: (p.parent.name, p.name))


_BLOCK = re.compile(r"^b\d{2}_")
_JOB = re.compile(r"^j\d{2}_")
_TASK = re.compile(r"^t\d{2}_")
_HEAD = re.compile(r"^([a-z][a-z-]*):\s*(.+?)\s*$")


def _face(folder: Path) -> tuple[str | None, dict[str, str]]:
    """A face's title (its first `# ` line) and its `key: value` header lines, read up to its first section."""
    for name in (f"{folder.name}.md", "board.md"):
        f = folder / name
        if not f.is_file():
            continue
        title, head = None, {}
        for line in f.read_text(encoding="utf-8", errors="replace").splitlines()[:40]:
            if line.startswith("## "):
                break
            if line.startswith("# ") and title is None:
                title = line[2:].strip()
                continue
            m = _HEAD.match(line)
            if m:
                head[m.group(1)] = m.group(2)
        return title, head
    return None, {}


# ── per-task read ────────────────────────────────────────────────────────────

def _marker_scope(task_dir: Path) -> str | None:
    """An explicit override, if the task carries one."""
    m = task_dir / ".inlab-scope"
    if m.exists():
        v = m.read_text().strip().lower()
        if v in ("individual", "group"):
            return v
    for name in ("config.yaml", "plan.yaml", "task.yaml"):
        p = task_dir / name
        if not p.exists():
            continue
        hit = re.search(r"^\s*(?:scope|kind)\s*:\s*(individual|group)\b",
                        p.read_text(), re.M | re.I)
        if hit:
            return hit.group(1).lower()
    return None


def _classify(task_dir: Path, series: str | None, head: dict[str, str] | None = None) -> str:
    """individual iff the face's scope: line (or a marker) says so, or its task-type names individual work;
    the flat layout also keeps its old reading (E-series / a name mentioning individual|subject)."""
    head = head or {}
    if head.get("scope", "").lower() in ("individual", "group"):
        return head["scope"].lower()
    marked = _marker_scope(task_dir)
    if marked:
        return marked
    if "individual" in head.get("task-type", "").lower():
        return "individual"
    name = task_dir.name.lower()
    if series == "E" or "individual" in name or "subject" in name or "for-individual" in name:
        return "individual"
    return "group"


def _status(task_dir: Path) -> str:
    """A coarse lifecycle label from what's on disk — enough for a badge."""
    results = task_dir / "results"
    if results.is_dir() and any(results.iterdir()):
        return "has-results"
    if any((task_dir / f).exists() for f in ("report.yaml", ".state.json")):
        return "reported"
    if any((task_dir / f).exists() for f in ("plan.yaml", "config.yaml", "INDEX.md")):
        return "planned"
    return "scaffolded"


def _title(rest: str) -> str:
    return rest.replace("-", " ").replace("_", " ").strip()


def _scan(scope: str | None) -> list[dict]:
    out: list[dict] = []
    for proj in _projects():
        tdir = proj / "tasks"
        world = proj.parent.name if proj.parent.name.startswith("examples") else None
        blocks = [b for b in sorted(tdir.iterdir()) if b.is_dir() and _BLOCK.match(b.name)]
        for blk in blocks:                                   # the ladder
            btitle, _ = _face(blk)
            for job in sorted(j for j in blk.iterdir() if j.is_dir() and _JOB.match(j.name)):
                jtitle, _ = _face(job)
                for t in sorted(t for t in job.iterdir() if t.is_dir() and _TASK.match(t.name)):
                    ttitle, head = _face(t)
                    kind = _classify(t, None, head)
                    if scope and kind != scope:
                        continue
                    out.append({
                        "world": world, "project": proj.name,
                        "block": blk.name, "block_title": btitle or _title(blk.name[4:]),
                        "job": job.name, "job_title": jtitle or _title(job.name[4:]),
                        "task": t.name, "series": None,
                        "title": ttitle or _title(t.name[4:]),
                        "task_type": head.get("task-type"),
                        "kind": kind, "status": _status(t),
                    })
        if blocks:
            continue
        for t in sorted(tdir.iterdir()):                     # the flat layout, a fallback
            if not t.is_dir() or t.name.startswith(("_", ".")):
                continue
            m = _SERIES_RE.match(t.name)
            series = m.group(1) if m else None
            kind = _classify(t, series)
            if scope and kind != scope:
                continue
            out.append({
                "world": world, "project": proj.name, "block": None, "block_title": None,
                "job": None, "job_title": None,
                "task": t.name,
                "series": series,
                "title": _title(m.group(3)) if m else _title(t.name),
                "task_type": None,
                "kind": kind,
                "status": _status(t),
            })
    return out


# ── routes ───────────────────────────────────────────────────────────────────

@router.get("/tasks")
def tasks(scope: str | None = None):
    """Tasks across all projects, under their Block and Job, classified individual/group.
    `?scope=group` (or `individual`) filters to that side. The root is named, never its path."""
    root = _projects_root()
    if not root:
        return JSONResponse({
            "root": None,
            "tasks": [],
            "reason": "no projects root — set INLAB_PROJECTS_ROOT to the SPACE root (the folder holding "
                      "examples-*/Project-*/tasks).",
        })
    scope = scope if scope in ("individual", "group") else None
    items = _scan(scope)
    projects: dict[str, dict] = {}
    for it in items:
        p = projects.setdefault(it["project"], {"project": it["project"], "world": it["world"], "blocks": {}})
        bkey = it["block"] or ""
        b = p["blocks"].setdefault(bkey, {"block": it["block"], "title": it["block_title"], "jobs": {}})
        j = b["jobs"].setdefault(it["job"] or "", {"job": it["job"], "title": it["job_title"], "tasks": []})
        j["tasks"].append(it)
    return JSONResponse({
        "root": root.name,
        "scope": scope,
        "n": len(items),
        "projects": [
            {"project": p["project"], "world": p["world"],
             "blocks": [{"block": b["block"], "title": b["title"],
                         "jobs": [{"job": j["job"], "title": j["title"], "tasks": j["tasks"]}
                                  for j in b["jobs"].values()]}
                        for b in p["blocks"].values()]}
            for _, p in sorted(projects.items())
        ],
    })
