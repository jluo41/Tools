"""Explicit, non-destructive migrations for Page-owned authoring records."""
from __future__ import annotations

from pathlib import Path

from src.outline_version import latest_outline
from src.plan_shape import global_paragraph_mapping, rewrite_paragraph_addresses


def migrate_global_paragraphs(page) -> dict:
    """Make active Page paragraph addresses global while preserving their text.

    The migration changes references only in Page-owned source and working
    records. Static delivery is rebuilt separately; delegated Task histories
    are deliberately outside this address authority.
    """
    plan = latest_outline(page.folder / "outline", page.source.stem)
    if plan is None:
        raise ValueError("Page has no current Shape to migrate")
    mapping = global_paragraph_mapping(plan.read_text(encoding="utf-8"))
    changed_mapping = {old: new for old, new in mapping.items() if old != new}
    if not changed_mapping:
        return {"paragraphs": len(mapping), "changed_addresses": 0, "files": []}

    candidates = {page.source, plan}
    for directory in (page.folder / "outline", page.folder / "runs"):
        if directory.is_dir():
            candidates.update(path for path in directory.rglob("*") if path.is_file())
    results = page.folder / "results"
    if results.is_dir():
        for runtime in results.glob("*/runtime.yaml"):
            body = runtime.read_text(encoding="utf-8", errors="replace")
            if "operation: interactive-writing" in body:
                candidates.update(
                    path for path in runtime.parent.rglob("*") if path.is_file()
                )

    changed_files = []
    for path in sorted(candidates):
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        rewritten = rewrite_paragraph_addresses(text, changed_mapping)
        if rewritten == text:
            continue
        path.write_text(rewritten, encoding="utf-8")
        changed_files.append(path.relative_to(page.folder).as_posix())
    return {
        "paragraphs": len(mapping),
        "changed_addresses": len(changed_mapping),
        "files": changed_files,
    }
