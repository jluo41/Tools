"""Explicit, non-destructive migrations for Page-owned authoring records."""
from __future__ import annotations

from pathlib import Path

from src.outline_version import latest_outline
from src.plan_shape import iter_plan_bullets
from src.plan_shape import global_paragraph_mapping, rewrite_paragraph_addresses
from live.outline_preview import (
    page_lock,
    read_legacy_opening,
    read_legacy_previews,
    write_opening_draft,
    write_drafts,
)


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


def migrate_embedded_drafts(page, *, archive_legacy: bool = True) -> dict:
    """Move one Page's standalone preview into its current Outline Markdown.

    The migration is deliberately content-preserving: every legacy Bullet
    record must map to a current Bullet before the old file is archived.  The
    selected Outline keeps its existing version and shape; only its embedded
    Draft fields are added.
    """
    plan = latest_outline(page.folder / "outline", page.source.stem)
    if plan is None:
        raise ValueError("Page has no current Outline Markdown")
    legacy = page.folder / "outline" / (page.source.stem + "-preview.md")
    records = read_legacy_previews(page.source)
    opening = read_legacy_opening(page.source)
    if not records and not opening:
        return {"plan": plan.relative_to(page.folder).as_posix(),
                "migrated": 0, "archived": None, "status": "nothing-to-migrate"}
    blocks = list(iter_plan_bullets(plan.read_text(encoding="utf-8", errors="replace")))
    addresses = {block["address"] for block in blocks}
    missing = sorted(set(records) - addresses)
    if missing:
        raise ValueError("Legacy Draft has Bullet addresses absent from current Outline: "
                         + ", ".join(missing))
    with page_lock(page.source):
        write_drafts(page.source, records)
        if opening:
            write_opening_draft(page.source, opening)
        archived = None
        if archive_legacy and legacy.is_file():
            archive_dir = page.folder / "outline" / "_archive" / "legacy-outline-preview"
            archive_dir.mkdir(parents=True, exist_ok=True)
            target = archive_dir / legacy.name
            if target.exists():
                raise FileExistsError(f"Legacy Draft archive already exists: {target}")
            legacy.replace(target)
            archived = target.relative_to(page.folder).as_posix()
    return {"plan": plan.relative_to(page.folder).as_posix(),
            "migrated": len(records), "opening": bool(opening),
            "archived": archived, "status": "migrated"}
