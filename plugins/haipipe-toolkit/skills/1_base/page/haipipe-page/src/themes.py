"""The Project's Themes: one table for every reader.

A Theme is a Project-root folder holding the Blocks of one kind of work (the contract is
haipipe-project's ref/project-structure.md). Theme folders are singular and the general
Theme is `work/` (Tools/designs/b03_project_workbench, s01-D28 and s01-D29):

    work/  discovery/  cowork/  paper/  insight/  design/  labeling/

Until every Project has moved, a Theme's old folder (`tasks/`, `discoveries/`, ...) is read
as an alias, so an old and a new layout both open. A path is looked up under the new folder
first, then the old one. Drop the old names when no Project keeps one (the plan's phase 5).
"""

from __future__ import annotations

from pathlib import Path

# kind · folder · old folder, in the Space view's order. The work Theme's kind stays "task"
# (folder-kind, board-kind task-block, the kind filter) until the kind itself is renamed.
THEMES = (
    ("task", "work", "tasks"),
    ("discovery", "discovery", "discoveries"),
    ("cowork", "cowork", None),
    ("paper", "paper", "papers"),
    ("insight", "insight", "insights"),
    ("design", "design", "designs"),
    ("labeling", "labeling", "labelings"),
)
FOLDER = {kind: folder for kind, folder, _ in THEMES}
OLD_FOLDER = {kind: old for kind, _, old in THEMES if old}
KIND_OF = {folder: kind for kind, folder, _ in THEMES} | {old: kind for kind, _, old in THEMES if old}


def kind_of(name: str) -> str:
    """The kind of a Theme folder name, new or old (`work`, `tasks` -> `task`); "" if none."""
    return KIND_OF.get(name, "")


def folder_names(kind: str) -> tuple[str, ...]:
    """A kind's Theme folder names, the new one first: `task` -> ("work", "tasks")."""
    return tuple(n for n in (FOLDER.get(kind), OLD_FOLDER.get(kind)) if n)


def theme_dirs(project: Path, kind: str) -> list[Path]:
    """The kind's Theme folders that exist under `project`, the new one first."""
    return [Path(project) / n for n in folder_names(kind) if (Path(project) / n).is_dir()]


def theme_dir(project: Path, kind: str) -> Path:
    """Where the kind's Theme sits under `project`: the existing folder, or the new name."""
    found = theme_dirs(project, kind)
    return found[0] if found else Path(project) / FOLDER[kind]
