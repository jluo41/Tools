#!/usr/bin/env python3
"""Keep a Discovery Block's Board source and generated projection in sync.

The Discovery tree is the membership authority:

    bNN_<block>/board.md
      jNN_<job>/
        tNN_<task>/tNN_<task>.md

This helper owns only the small amount of Board source that Discovery can
derive safely.  It never writes Task rows into ``## Pages`` and never edits
``board/`` directly.  The Board engine remains responsible for parsing,
building, and checking the projection.

Typical calls from the Discovery lifecycle::

    python3 board_sync.py <block>
    python3 board_sync.py <block> --build --check --strict

The first call is idempotent: it creates a canonical Discovery Board head when
needed and refreshes the managed Job headings after a Job is opened.  Existing
authored Board prose is preserved.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


BOARD_KIND = "discovery-block"
MANAGED_START = "<!-- haipipe:discovery-board-jobs:start -->"
MANAGED_END = "<!-- haipipe:discovery-board-jobs:end -->"
JOB_RE = re.compile(r"^(j\d{2})_(?P<slug>[a-z0-9][a-z0-9_-]*)$", re.IGNORECASE)
BLOCK_RE = re.compile(r"^b\d{2}_[a-z0-9][a-z0-9_-]*$", re.IGNORECASE)


def _title_from_slug(value: str) -> str:
    """Turn a stable folder slug into a readable fallback label."""

    words = re.sub(r"[_-]+", " ", value).strip()
    return words[:1].upper() + words[1:] if words else value


def _block_title(block: Path) -> str:
    match = re.match(r"^b\d{2}_(?P<slug>.+)$", block.name, re.IGNORECASE)
    slug = match.group("slug") if match else block.name
    return f"{_title_from_slug(slug)} Discovery Board"


def _job_rows(block: Path) -> list[str]:
    """Return exact-folder-bound Job headings in stable numeric order."""

    jobs: list[tuple[int, str, str]] = []
    for child in block.iterdir():
        if not child.is_dir() or child.name.startswith((".", "_")):
            continue
        match = JOB_RE.fullmatch(child.name)
        if not match:
            continue
        jobs.append((int(match.group(1)[1:]), child.name.casefold(), child.name))
    rows: list[str] = [MANAGED_START]
    if not jobs:
        rows.append("No Jobs opened yet; the direct BJTR tree is the membership source.")
    else:
        for _number, _sort_name, folder in sorted(jobs):
            match = JOB_RE.fullmatch(folder)
            assert match is not None
            job_id = match.group(1).lower()
            rows.append(f"### {job_id} · {folder}")
            rows.append(
                "The folder name is the Job/Group identity; Task Pages below it "
                "are discovered from the direct tree."
            )
    rows.append(MANAGED_END)
    return rows


def _head(title: str, spine: str, close: str) -> str:
    return f"""# {title}
board-kind: {BOARD_KIND}
spine: {spine}
close: {close}

## Topic
This Board groups related Discovery Jobs. The Job and Task folders are the membership authority.

## Pipeline
SCOPE -> PREPARE? -> ACQUIRE -> SYNTHESIZE -> Page CHECK -> CLOSE

## Board Map
```text
Block / Board
└── Job / Group
    └── Task Page
        └── Paper or Source Runs
```

## Pages
{MANAGED_START}
No Jobs opened yet; the direct BJTR tree is the membership source.
{MANAGED_END}
"""


def _ensure_sections(text: str, spine: str, close: str) -> str:
    """Repair only missing Board declarations; preserve authored prose."""

    kind = re.search(r"(?m)^board-kind:\s*(\S+)(?:\s+#.*)?\s*$", text)
    if kind and kind.group(1) != BOARD_KIND:
        raise ValueError(
            f"{BOARD_KIND} sync cannot rewrite board-kind {kind.group(1)!r}"
        )
    if not kind:
        title_match = re.search(r"(?m)^#\s+.+$", text)
        insert_at = title_match.end() if title_match else 0
        prefix = "\n" if insert_at else ""
        text = text[:insert_at] + prefix + f"board-kind: {BOARD_KIND}\n" + text[insert_at:]

    additions: list[str] = []
    if not re.search(r"(?m)^spine:\s*\S", text):
        additions.append(f"spine: {spine}")
    if not re.search(r"(?m)^close:\s*\S", text):
        additions.append(f"close: {close}")
    for section, body in (
        ("Topic", "This Board groups related Discovery Jobs. The Job and Task folders are the membership authority."),
        ("Pipeline", "SCOPE -> PREPARE? -> ACQUIRE -> SYNTHESIZE -> Page CHECK -> CLOSE"),
        ("Board Map", "```text\nBlock / Board\n└── Job / Group\n    └── Task Page\n        └── Paper or Source Runs\n```"),
        ("Pages", ""),
    ):
        if not re.search(rf"(?m)^##\s+{re.escape(section)}\s*$", text):
            additions.extend([f"## {section}", body])
    if additions:
        text = text.rstrip() + "\n\n" + "\n".join(additions).rstrip() + "\n"
    return text


def _replace_managed_pages(text: str, rows: list[str]) -> str:
    """Replace the managed Job roster, creating it immediately under Pages."""

    managed = "\n".join(rows)
    pattern = re.compile(
        rf"{re.escape(MANAGED_START)}.*?{re.escape(MANAGED_END)}",
        re.DOTALL,
    )
    if pattern.search(text):
        return pattern.sub(managed, text, count=1)

    pages = re.search(r"(?m)^##\s+Pages\s*$", text)
    if not pages:
        raise ValueError("board.md has no ## Pages section after repair")
    insert_at = pages.end()
    return text[:insert_at] + "\n" + managed + text[insert_at:]


def sync_source(
    block: Path,
    *,
    title: str | None = None,
    spine: str = "Organize one bounded external-evidence program across Discovery Jobs and Task Pages.",
    close: str = "Every Task Page is checked and every admitted Paper or Source Run has a truthful terminal state.",
) -> tuple[Path, bool]:
    """Create or update ``board.md`` and return ``(path, changed)``."""

    if not block.is_dir():
        raise ValueError(f"Discovery Block is not a directory: {block}")
    if not BLOCK_RE.fullmatch(block.name):
        raise ValueError(f"Discovery Block must use bNN_<slug>: {block.name}")
    board = block / "board.md"
    before = board.read_text(encoding="utf-8") if board.exists() else ""
    text = _head(title or _block_title(block), spine, close) if not before else _ensure_sections(before, spine, close)
    text = _replace_managed_pages(text, _job_rows(block))
    changed = text != before
    if changed:
        board.write_text(text.rstrip() + "\n", encoding="utf-8")
    return board, changed


def _run_board_cli(block: Path, command: str, strict: bool = False) -> int:
    skills_root = Path(__file__).resolve().parents[3]
    engine = skills_root / "board" / "haipipe-board" / "cli" / f"{command}.py"
    if not engine.is_file():
        raise FileNotFoundError(f"Board {command} CLI not found: {engine}")
    args = [sys.executable, str(engine), str(block)]
    if command == "check" and strict:
        args.append("--strict")
    return subprocess.run(args, check=False).returncode


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("block", type=Path, help="Discovery Block folder (bNN_<slug>)")
    parser.add_argument("--title", help="title for a new Board head; existing titles are preserved")
    parser.add_argument("--spine", default="Organize one bounded external-evidence program across Discovery Jobs and Task Pages.", help="spine for a new or repaired Board head")
    parser.add_argument("--close", dest="close_condition", default="Every Task Page is checked and every admitted Paper or Source Run has a truthful terminal state.", help="close condition for a new or repaired Board head")
    parser.add_argument("--build", action="store_true", help="rebuild the derived board/ site")
    parser.add_argument("--check", action="store_true", help="run the Board checker")
    parser.add_argument("--strict", action="store_true", help="make Board checker errors fail")
    args = parser.parse_args(argv)
    if args.strict and not args.check:
        parser.error("--strict requires --check")

    try:
        board, changed = sync_source(
            args.block.resolve(),
            title=args.title,
            spine=args.spine,
            close=args.close_condition,
        )
        print(f"{'updated' if changed else 'current'} {board}")
        if args.build and _run_board_cli(args.block.resolve(), "build"):
            return 1
        if args.check:
            return _run_board_cli(args.block.resolve(), "check", strict=args.strict)
        return 0
    except (OSError, ValueError, FileNotFoundError) as exc:
        print(f"board sync: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
