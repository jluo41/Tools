"""Run folders by Space (0.118): a Page keeps each run beside the Space it changes.

    runs/draft-manual-run/   Structure revise · Scratch · Section and Paragraph revise
    runs/draft-auto-run/     Auto write · Evidence embed · scripted drafting
    runs/evidence-run/       Citation · Value · Display
    runs/supporting-run/     generated index of the Block > Job > Task runs elsewhere
    runs/delivery-run/       Web · LaTeX · Word · Slides builds

A Page with none of these folders keeps the flat `runs/`. `results/` stays
flat either way: the Run Space pairs `runs/<folder>/<run>` with `results/<run>/`.
"""
from __future__ import annotations

from pathlib import Path
import re

FOLDERS = ("draft-manual-run", "draft-auto-run", "evidence-run", "supporting-run", "delivery-run")
SPACE = {"draft-manual-run": "draft", "draft-auto-run": "draft", "evidence-run": "evidence",
         "supporting-run": "evidence", "delivery-run": "delivery"}
_KINDS = (
    (re.compile(r"^rp-(?:struct|sec|para|scratch|revise)-\d", re.I), "draft-manual-run"),
    (re.compile(r"^rp-(?:auto|embed)-\d", re.I), "draft-auto-run"),
    (re.compile(r"^(?:re-(?:cite|value|display)-\d|p[._]?j\d+[._]?t\d+[._]?r\d+)", re.I), "evidence-run"),
    (re.compile(r"^rd\d", re.I), "delivery-run"),
)


def uses_space_folders(page_folder) -> bool:
    runs = Path(page_folder) / "runs"
    return any((runs / name).is_dir() for name in FOLDERS)


def folder_for(run_id: str) -> str | None:
    """The Space folder a run id belongs in, or None for other families."""
    return next((folder for pattern, folder in _KINDS if pattern.match(run_id or "")), None)


def ticket_dir(page_folder, run_id: str) -> Path:
    """Where a new run's ticket goes: its Space folder, or flat `runs/` on older Pages."""
    runs = Path(page_folder) / "runs"
    folder = folder_for(run_id) if uses_space_folders(page_folder) else None
    return runs / folder if folder else runs


def ticket_rel(page_folder, run_id: str, suffix: str = ".md") -> str:
    """The ticket path as a Page-relative string, e.g. `runs/draft-manual-run/rp-para-15_P02.md`."""
    return (ticket_dir(page_folder, run_id) / (run_id + suffix)).relative_to(Path(page_folder)).as_posix()


def space_of(ticket) -> str:
    """draft · evidence · delivery · other, from the ticket's folder, else its id."""
    path = Path(str(ticket))
    for part in path.parts:
        if part in SPACE:
            return SPACE[part]
    folder = folder_for(path.stem)
    return SPACE.get(folder, "other") if folder else "other"
