#!/usr/bin/env python3
"""Read-only audit for Paper Pages against the current Page contract.

This deliberately reports migration work; it never edits a Paper folder,
renames a Run, or regenerates delivery.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable


SKIP_DIRS = {
    ".git",
    ".codex",
    "_archive",
    "board",
    "delivery",
    "released",
    "sent",
    "__pycache__",
}
PAGE_GROUP_RE = re.compile(r"^B[a-d]-")
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
VALUE_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):\s*(.*?)\s*$", re.MULTILINE)
LEGACY_RUN_RE = re.compile(
    r"(?:^|/)(?:pj\d+t\d+r\d+|r\d+_page-"
    r"(?:writing|division-writing|evidence-item|display))(?:[_./-]|$)"
)
CURRENT_PAGE_RUN_RE = re.compile(
    r"^(?:rp00_mermaid-structure|rp\d+_p\d+(?:-p\d+)?)(?:\.[^.]+)?$"
)
OLD_ADDRESS_RE = re.compile(r"\bC(\d+)\.P1\b")

PROHIBITED_SECTIONS = {
    "outline",
    "diagram",
    "files",
    "log",
    "discussion",
}


def _excluded(path: Path, root: Path) -> bool:
    try:
        parts = path.relative_to(root).parts
    except ValueError:
        return True
    return any(part in SKIP_DIRS for part in parts)


def _page_sources(root: Path) -> Iterable[Path]:
    for path in root.rglob("*.md"):
        if _excluded(path, root) or path.stem != path.parent.name:
            continue
        parent_group = path.parent.parent.name
        if parent_group == "A1-Story" or PAGE_GROUP_RE.match(parent_group):
            yield path


def _frontmatter(text: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*(.*?)\s*$", text, re.MULTILINE)
    if not match:
        return None
    value = match.group(1).strip().strip("'\"")
    return value or None


def _finding(
    findings: list[dict[str, str]],
    severity: str,
    code: str,
    page: Path,
    root: Path,
    detail: str,
) -> None:
    findings.append(
        {
            "severity": severity,
            "code": code,
            "page": page.stem,
            "path": str(page.parent.relative_to(root)),
            "detail": detail,
        }
    )


def audit(root: Path) -> dict[str, object]:
    root = root.resolve()
    findings: list[dict[str, str]] = []
    pages: list[dict[str, object]] = []

    for source in sorted(_page_sources(root)):
        page_dir = source.parent
        text = source.read_text(encoding="utf-8", errors="replace")
        page_record: dict[str, object] = {
            "page": source.stem,
            "path": str(page_dir.relative_to(root)),
            "owner": _frontmatter(text, "owner"),
            "page_type": _frontmatter(text, "page-type"),
            "folder_kind": _frontmatter(text, "folder-kind"),
            "page_runs": [],
        }
        pages.append(page_record)

        if not any(
            page_record[key] for key in ("owner", "page_type", "folder_kind")
        ):
            _finding(
                findings,
                "error",
                "missing-page-owner",
                source,
                root,
                "no owner:, page-type:, or folder-kind: declaration",
            )

        if not (page_dir / "outline").is_dir():
            _finding(
                findings,
                "error",
                "missing-outline",
                source,
                root,
                "Page source has no outline/ record folder",
            )

        if not (page_dir / "workflow").is_dir():
            _finding(
                findings,
                "warning",
                "missing-workflow",
                source,
                root,
                "no workflow/ receipt folder; create it when the Page re-enters the lifecycle",
            )

        if page_record["page_type"] == "section":
            story_row = _frontmatter(text, "story-row")
            if not story_row:
                _finding(
                    findings,
                    "error",
                    "missing-story-row",
                    source,
                    root,
                    "Section Page has no story-row: binding",
                )
            elif "+" not in story_row and "sha256:" not in story_row:
                _finding(
                    findings,
                    "warning",
                    "missing-story-version-binding",
                    source,
                    root,
                    "story-row: names a row but does not record the bound Story outline/version",
                )

        if (page_dir / "evidence").exists():
            _finding(
                findings,
                "error",
                "legacy-evidence-root",
                source,
                root,
                "evidence/ is at Page root; current records belong under outline/evidence/",
            )

        for heading in HEADING_RE.findall(text):
            normalized = re.sub(r"\s+", " ", heading).strip().lower()
            if normalized in PROHIBITED_SECTIONS or normalized.startswith(
                "historical content"
            ):
                _finding(
                    findings,
                    "error",
                    "retired-page-section",
                    source,
                    root,
                    f"authored top-level heading '## {heading}'",
                )

        page_runs: list[str] = []
        legacy_paths: set[str] = set()
        for candidate in page_dir.rglob("*"):
            if _excluded(candidate, root):
                continue
            relative = candidate.relative_to(page_dir).as_posix()
            name = candidate.name
            if CURRENT_PAGE_RUN_RE.match(name):
                page_runs.append(relative)
            if LEGACY_RUN_RE.search("/" + relative):
                legacy_paths.add(relative)

        page_record["page_runs"] = sorted(page_runs)
        if legacy_paths:
            _finding(
                findings,
                "warning",
                "legacy-run-reference",
                source,
                root,
                f"{len(legacy_paths)} historical pj/rNN_page* path(s); preserve read-only and classify",
            )

        if page_runs and not any(
            Path(run).name.startswith("rp00_mermaid-structure") for run in page_runs
        ):
            _finding(
                findings,
                "error",
                "missing-rp00-baseline",
                source,
                root,
                "Page has current-looking rpNN interaction but no rp00_mermaid-structure",
            )
        elif legacy_paths and not page_runs:
            _finding(
                findings,
                "warning",
                "page-run-baseline-needed",
                source,
                root,
                "historical interaction records exist; create rp00 only when new Page interaction begins",
            )

        address_spaces = sorted({int(value) for value in OLD_ADDRESS_RE.findall(text)})
        if len(address_spaces) > 1:
            _finding(
                findings,
                "error",
                "page-global-address-reset",
                source,
                root,
                f"multiple C<n>.P1 starts found ({', '.join(f'C{n}' for n in address_spaces)}); migrate to Page-global P addresses",
            )

    errors = sum(item["severity"] == "error" for item in findings)
    warnings = sum(item["severity"] == "warning" for item in findings)
    return {
        "paper_root": str(root),
        "page_count": len(pages),
        "pages": pages,
        "summary": {"errors": errors, "warnings": warnings},
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paper_root", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="return exit code 1 when compatibility errors are found",
    )
    args = parser.parse_args()

    if not args.paper_root.is_dir():
        parser.error(f"not a Paper directory: {args.paper_root}")

    report = audit(args.paper_root)
    if args.as_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        summary = report["summary"]
        print(
            f"Page compatibility audit: {report['page_count']} Page(s), "
            f"{summary['errors']} error(s), {summary['warnings']} warning(s)"
        )
        for item in report["findings"]:
            print(
                f"[{item['severity']}] {item['code']}: "
                f"{item['path']} — {item['detail']}"
            )
    if args.strict and report["summary"]["errors"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
