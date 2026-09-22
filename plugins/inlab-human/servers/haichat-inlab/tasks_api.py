"""Project task-folders — the work linked to a console scope.

The individual/group split is per-TASK, not per-project: one research project
(examples/Project-*) holds both group-level tasks (cohort data/case/eval
pipelines, the A–D series) and, when they exist, individual-level tasks (query
one subject's data — the haipipe `for-individual` E-series). This router scans
those task-folders and classifies each, so the group console lists the group
tasks and the individual console lists the individual ones.

There is no per-task scope marker in the wild yet, so classification is a
best-effort heuristic (documented in `_classify`), overridable by a one-line
marker (`.inlab-scope` = individual|group, or `scope:`/`kind:` in a task yaml).

Configuration, by environment like the rest of the service:

    INLAB_PROJECTS_ROOT   dir that holds Project-* folders (an examples/ dir).
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
    # walk up looking for a dir that actually contains Project-* folders
    for base in Path(__file__).resolve().parents:
        cand = base / "examples"
        if cand.is_dir() and any(cand.glob("Project-*")):
            return cand
        if any(base.glob("Project-*")):
            return base
    return None


def _projects() -> list[Path]:
    root = _projects_root()
    if not root:
        return []
    return sorted(p for p in root.glob("Project-*") if (p / "tasks").is_dir())


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


def _classify(task_dir: Path, series: str | None) -> str:
    """individual iff an explicit marker says so, or it looks like a haipipe
    per-individual task (E-series / name mentions individual|subject). Otherwise
    group — most pipeline/case/data/eval tasks are cohort-level."""
    marked = _marker_scope(task_dir)
    if marked:
        return marked
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
        for t in sorted(tdir.iterdir()):
            if not t.is_dir() or t.name.startswith(("_", ".")):
                continue
            m = _SERIES_RE.match(t.name)
            series = m.group(1) if m else None
            kind = _classify(t, series)
            if scope and kind != scope:
                continue
            out.append({
                "project": proj.name,
                "task": t.name,
                "series": series,
                "title": _title(m.group(3)) if m else _title(t.name),
                "kind": kind,
                "status": _status(t),
            })
    return out


# ── routes ───────────────────────────────────────────────────────────────────

@router.get("/tasks")
def tasks(scope: str | None = None):
    """Task-folders across all projects, classified individual/group.
    `?scope=group` (or `individual`) filters to that side."""
    root = _projects_root()
    if not root:
        return JSONResponse({
            "root": None,
            "tasks": [],
            "reason": "no projects root — set INLAB_PROJECTS_ROOT to an examples/ dir "
                      "(the one holding Project-* folders).",
        })
    scope = scope if scope in ("individual", "group") else None
    items = _scan(scope)
    by_project: dict[str, list[dict]] = {}
    for it in items:
        by_project.setdefault(it["project"], []).append(it)
    return JSONResponse({
        "root": str(root),
        "scope": scope,
        "n": len(items),
        "projects": [
            {"project": p, "tasks": ts} for p, ts in sorted(by_project.items())
        ],
    })
