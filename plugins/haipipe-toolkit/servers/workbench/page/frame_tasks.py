"""A Task's type picks its layout: task_type, task_layouts and the Task's Work card lines."""

from __future__ import annotations

import re
from pathlib import Path

from live.frame_base import face


# ── a Task's type picks its layout (b32 s03, JL 261014: "for the theme, we can have different type of tasks,
# and the tasks can have different layout"; s41-D15, JL 261016: one folder per type) ──────────────────────────
# A Task's face says its type (`task-type: draft`). Each type has its own folder, `workbench-task-<type>/`, holding its layout
# `task_<type>.py` (TASK_TYPE, spaces) and every view and asset it shows: servers/workbench/workbench-task-<type>/ for a type
# every theme uses, servers/workbench-<theme>/workbench-task-<type>/ for a theme's own. The theme's own Spaces go on top.
_TASK_TYPE = re.compile(r"(?m)^\**task-type\**:\s*`?([\w-]+)")


def task_type(folder: Path) -> str:
    """The `task-type:` a Task's face declares, or "" when it names none."""
    md = face(folder) if folder else None
    if not md:
        return ""
    m = _TASK_TYPE.search(md.read_text(encoding="utf-8", errors="ignore")[:3000])
    return m.group(1) if m else ""


def task_layouts(theme: str = "") -> dict:
    """{task type: spaces(folder, root, sub)} for one theme: every `workbench-task-<type>/task_<type>.py` in
    servers/workbench/ (every theme's), then the theme's own in servers/workbench-<theme>/ (that theme's only, so
    a labeling `task-type: eval` never lays out a work Task). A layout names its TASK_TYPE, or several TASK_TYPES."""
    return {name: layout.spaces for name, layout in _task_modules(theme).items()}


def _task_modules(theme: str = "") -> dict:
    """{task type: its layout module} for one theme (task_layouts' search)."""
    import importlib
    from host_registry import task_folders, workbench_name
    found = {}
    for folder in task_folders():
        owner = folder.parent.name
        if owner != "workbench" and workbench_name(folder.parent) != theme:
            continue
        kind = folder.name[len("workbench-task-"):]
        module = f"task_{kind.replace('-', '_')}"
        if (folder / f"{module}.py").is_file():
            layout = importlib.import_module(f"live.{module}")
            for name in getattr(layout, "TASK_TYPES", None) or (layout.TASK_TYPE,):
                found[name] = layout
    return found


def task_card(task: Path, root: Path, theme: str = "") -> str:
    """A Task type's own lines on the Task's Work card in its Job (its layout's optional `work_card(task, root)`):
    a draft Task's seven steps, each a link to its tab (b32 s41); "" for a type that has none."""
    layout = _task_modules(theme).get(task_type(task))
    try:
        return layout.work_card(task, root) if layout is not None and hasattr(layout, "work_card") else ""
    except Exception:                            # a Task type's lines never break the base's tree
        return ""
