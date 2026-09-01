#!/usr/bin/env python3
"""Validate Discovery Paper Runs and build the derived Topic Evidence Bib."""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


RUN_RE = re.compile(r"^r[0-9]{2}_[a-z0-9]+[0-9]{4}_[a-z0-9_]+$")
BIB_START_RE = re.compile(
    r"(?im)^[ \t]*@([a-z]+)\s*([({])\s*([^,\s]+)\s*,"
)
CITE_RE = re.compile(
    r"(?im)^\s*(?:[-*]\s*)?cite:\s*@([A-Za-z0-9_:.+/-]+)\s*$"
)
STATUS_RE = re.compile(r"(?m)^status:\s*['\"]?([a-z_-]+)['\"]?\s*$")
RUN_FIELD_RE = re.compile(r"(?m)^run:\s*['\"]?([^'\"\s]+)['\"]?\s*$")
PAGE_FIELD_RE = re.compile(r"(?m)^page:\s*['\"]?([^'\"\s]+)['\"]?\s*$")
EXECUTED_AT_RE = re.compile(r"(?m)^executed_at:\s*['\"]?([^'\"\n]+)['\"]?\s*$")
DOI_RE = re.compile(r'(?im)\bdoi\s*=\s*[{"]\s*([^}"]+?)\s*[}"]')
ALLOWED_STATUSES = {
    "planned",
    "running",
    "complete",
    "blocked",
    "unresolved",
    "superseded",
}
NON_ENTRY_TYPES = {"comment", "preamble", "string"}


@dataclass(frozen=True)
class BibEntry:
    key: str
    text: str
    normalized: str
    doi: str | None
    source: Path


def _field(text: str, pattern: re.Pattern[str]) -> str | None:
    match = pattern.search(text)
    return match.group(1).strip() if match else None


def _balanced_entry(text: str, start: re.Match[str]) -> str:
    opener = start.group(2)
    closer = "}" if opener == "{" else ")"
    open_at = text.find(opener, start.start())
    depth = 0
    in_quote = False
    escaped = False
    for index in range(open_at, len(text)):
        char = text[index]
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == '"':
            in_quote = not in_quote
            continue
        if in_quote:
            continue
        if char == opener:
            depth += 1
        elif char == closer:
            depth -= 1
            if depth == 0:
                return text[start.start() : index + 1].strip()
    raise ValueError(f"unbalanced BibTeX entry beginning at byte {start.start()}")


def parse_bib(path: Path) -> list[BibEntry]:
    text = path.read_text(encoding="utf-8")
    entries: list[BibEntry] = []
    for match in BIB_START_RE.finditer(text):
        if match.group(1).lower() in NON_ENTRY_TYPES:
            continue
        entry_text = _balanced_entry(text, match)
        key = match.group(3)
        normalized = re.sub(r"\s+", " ", entry_text).strip()
        doi_match = DOI_RE.search(entry_text)
        doi = doi_match.group(1).strip().lower() if doi_match else None
        entries.append(BibEntry(key, entry_text, normalized, doi, path))
    return entries


def _runtime(path: Path) -> tuple[str | None, str | None, str]:
    text = path.read_text(encoding="utf-8")
    return _field(text, STATUS_RE), _field(text, RUN_FIELD_RE), text


def _yaml_block(text: str, name: str) -> str | None:
    match = re.search(
        rf"(?m)^{re.escape(name)}:\s*\n((?:^[ \t]+.*(?:\n|$))*)",
        text,
    )
    return match.group(1) if match else None


def _block_field(block: str, name: str) -> str | None:
    match = re.search(
        rf"(?m)^[ \t]+{re.escape(name)}:\s*['\"]?([^'\"\n]+?)['\"]?\s*$",
        block,
    )
    return match.group(1).strip() if match else None


def _pair_maps(topic: Path) -> tuple[dict[str, Path], dict[str, Path]]:
    runs_dir = topic / "runs"
    results_dir = topic / "results"
    runs = (
        {path.stem: path for path in runs_dir.glob("*.sh") if path.is_file()}
        if runs_dir.is_dir()
        else {}
    )
    results = (
        {path.name: path for path in results_dir.iterdir() if path.is_dir()}
        if results_dir.is_dir()
        else {}
    )
    return runs, results


def _bib_conflicts(entries: Iterable[BibEntry]) -> list[str]:
    errors: list[str] = []
    by_key: dict[str, BibEntry] = {}
    by_doi: dict[str, BibEntry] = {}
    for entry in entries:
        key_id = entry.key.casefold()
        previous = by_key.get(key_id)
        if previous and previous.normalized != entry.normalized:
            errors.append(
                f"bib-key-conflict: @{entry.key} differs between "
                f"{previous.source} and {entry.source}"
            )
        else:
            by_key.setdefault(key_id, entry)
        if entry.doi:
            previous_doi = by_doi.get(entry.doi)
            if previous_doi and (
                previous_doi.key.casefold() != entry.key.casefold()
                or previous_doi.normalized != entry.normalized
            ):
                errors.append(
                    f"bib-doi-conflict: {entry.doi} differs between "
                    f"{previous_doi.source} and {entry.source}"
                )
            else:
                by_doi.setdefault(entry.doi, entry)
    return errors


def check_topic(topic: Path) -> tuple[list[str], dict[str, int], list[BibEntry]]:
    topic = topic.resolve()
    errors: list[str] = []
    counts = {status: 0 for status in sorted(ALLOWED_STATUSES)}
    complete_entries: list[BibEntry] = []
    if not topic.is_dir():
        return [f"topic-missing: {topic}"], counts, complete_entries

    runs, results = _pair_maps(topic)
    for stem in sorted(runs.keys() - results.keys()):
        errors.append(f"missing-result: runs/{stem}.sh has no results/{stem}/")
    for stem in sorted(results.keys() - runs.keys()):
        errors.append(f"orphan-result: results/{stem}/ has no runs/{stem}.sh")

    for stem in sorted(runs.keys() & results.keys()):
        run_path = runs[stem]
        result_dir = results[stem]
        if not RUN_RE.fullmatch(stem):
            errors.append(f"runname-invalid: {stem}")
        if not os.access(run_path, os.X_OK):
            errors.append(f"run-not-executable: {run_path}")

        runtime_path = result_dir / "runtime.yaml"
        if not runtime_path.is_file():
            errors.append(f"runtime-missing: {runtime_path}")
            continue
        status, runtime_run, runtime_text = _runtime(runtime_path)
        if status not in ALLOWED_STATUSES:
            errors.append(f"runtime-status-invalid: {runtime_path}: {status!r}")
            continue
        counts[status] += 1
        if runtime_run != stem:
            errors.append(
                f"runtime-run-mismatch: {runtime_path}: {runtime_run!r} != {stem!r}"
            )
        if not re.search(r"(?m)^trigger:\s*$", runtime_text):
            errors.append(f"runtime-trigger-missing: {runtime_path}")
        if status != "unresolved" and not re.search(
            r"(?m)^subject:\s*$", runtime_text
        ):
            errors.append(f"runtime-subject-missing: {runtime_path}")

        if status != "complete":
            continue
        if _field(runtime_text, EXECUTED_AT_RE) is None:
            errors.append(f"runtime-executed-at-missing: {runtime_path}")
        bib_receipt = _yaml_block(runtime_text, "bib")
        if bib_receipt is None:
            errors.append(f"runtime-bib-provenance-missing: {runtime_path}")
        else:
            if _block_field(bib_receipt, "source") is None:
                errors.append(f"runtime-bib-source-missing: {runtime_path}")
            mode = _block_field(bib_receipt, "mode")
            if mode != "verbatim_copy":
                errors.append(
                    f"runtime-bib-mode-invalid: {runtime_path}: {mode!r}"
                )

        card_path = result_dir / f"{stem}.md"
        facts_path = result_dir / "facts.md"
        bib_path = result_dir / f"{stem}.bib"
        for required in (card_path, facts_path, bib_path):
            if not required.is_file():
                errors.append(f"complete-artifact-missing: {required}")
        if not all(path.is_file() for path in (card_path, facts_path, bib_path)):
            continue

        try:
            entries = parse_bib(bib_path)
        except ValueError as exc:
            errors.append(f"bib-parse-error: {bib_path}: {exc}")
            continue
        if len(entries) != 1:
            errors.append(f"bib-entry-count: {bib_path}: expected 1, found {len(entries)}")
            continue
        entry = entries[0]
        complete_entries.append(entry)
        card_text = card_path.read_text(encoding="utf-8")
        cite_key = _field(card_text, CITE_RE)
        if cite_key is None:
            errors.append(f"card-cite-missing: {card_path}")
        elif cite_key != entry.key:
            errors.append(
                f"card-cite-mismatch: {card_path}: @{cite_key} != @{entry.key}"
            )

    errors.extend(_bib_conflicts(complete_entries))
    return errors, counts, complete_entries


def aggregate_bib(entries: Iterable[BibEntry]) -> str:
    unique: dict[str, BibEntry] = {}
    for entry in entries:
        key_id = entry.key.casefold()
        unique.setdefault(key_id, entry)
    ordered = sorted(unique.values(), key=lambda item: (item.key.casefold(), item.key))
    return ("\n\n".join(entry.text for entry in ordered) + "\n") if ordered else ""


def default_bib_path(topic: Path) -> Path:
    manifest = topic / "discovery.yaml"
    stem = topic.name
    if manifest.is_file():
        page = _field(manifest.read_text(encoding="utf-8"), PAGE_FIELD_RE)
        if page:
            stem = Path(page).stem
    return topic / "evidence" / "bibex" / f"{stem}.bib"


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        handle.write(text)
        temp_path = Path(handle.name)
    os.replace(temp_path, path)


def _print_summary(counts: dict[str, int]) -> None:
    rendered = " ".join(f"{key}={counts[key]}" for key in sorted(counts))
    print(f"runs: {rendered}")


def command_check(topic: Path) -> int:
    errors, counts, _ = check_topic(topic)
    _print_summary(counts)
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 1
    print("OK paper-run contract")
    return 0


def command_build_bib(topic: Path, output: Path | None, write: bool) -> int:
    errors, counts, entries = check_topic(topic)
    _print_summary(counts)
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 1
    text = aggregate_bib(entries)
    output_path = output or default_bib_path(topic)
    if write:
        atomic_write(output_path, text)
        print(f"WROTE {output_path} entries={len(parse_aggregate(text))}")
    else:
        sys.stdout.write(text)
    return 0


def parse_aggregate(text: str) -> list[str]:
    """Return aggregate keys for reporting without creating a temporary file."""
    return [
        match.group(3)
        for match in BIB_START_RE.finditer(text)
        if match.group(1).lower() not in NON_ENTRY_TYPES
    ]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    check = subparsers.add_parser("check", help="validate Run/Result pairs")
    check.add_argument("topic", type=Path)
    bib = subparsers.add_parser("build-bib", help="build derived Topic Evidence Bib")
    bib.add_argument("topic", type=Path)
    bib.add_argument("--output", type=Path)
    bib.add_argument("--write", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "check":
        return command_check(args.topic)
    return command_build_bib(args.topic, args.output, args.write)


if __name__ == "__main__":
    raise SystemExit(main())
