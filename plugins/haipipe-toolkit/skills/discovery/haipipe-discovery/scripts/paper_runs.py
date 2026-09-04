#!/usr/bin/env python3
"""Validate a Discovery Page Folder and build its derived Evidence Bib."""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


RUN_RE = re.compile(r"^r[0-9]{2}_[a-z0-9]+[0-9]{4}_[a-z0-9_]+$")
SEGMENT_RE = {
    "block": re.compile(r"^(b[0-9]{2})_([a-z0-9][a-z0-9-]*_[a-z0-9][a-z0-9_-]*)$"),
    "job": re.compile(r"^(j[0-9]{2})_([a-z0-9][a-z0-9-]*_[a-z0-9][a-z0-9_-]*)$"),
    "task": re.compile(r"^(t[0-9]{2})_([a-z0-9][a-z0-9-]*_[a-z0-9][a-z0-9_-]*)$"),
}
BIB_START_RE = re.compile(
    r"(?im)^[ \t]*@([a-z]+)\s*([({])\s*([^,\s]+)\s*,"
)
CITE_RE = re.compile(
    r"(?im)^\s*(?:[-*]\s*)?cite:\s*@([A-Za-z0-9_:.+/-]+)\s*$"
)
STATUS_RE = re.compile(r"(?m)^status:\s*['\"]?([a-z_-]+)['\"]?\s*$")
RUN_FIELD_RE = re.compile(r"(?m)^run:\s*['\"]?([^'\"\s]+)['\"]?\s*$")
PAGE_FIELD_RE = re.compile(r"(?m)^page:\s*['\"]?([^'\"\s]+)['\"]?\s*$")
ADDRESS_FIELD_RE = re.compile(r"(?m)^address:\s*['\"]?([^'\"\s]+)['\"]?\s*$")
ADDRESS_COMPACT_FIELD_RE = re.compile(
    r"(?m)^address_compact:\s*['\"]?([^'\"\s]+)['\"]?\s*$"
)
KIND_FIELD_RE = re.compile(r"(?m)^kind:\s*['\"]?([^'\"\s]+)['\"]?\s*$")
VERSION_FIELD_RE = re.compile(r"(?m)^version:\s*['\"]?([^'\"\s]+)['\"]?\s*$")
DISCOVERY_TYPE_RE = re.compile(
    r"(?m)^discovery_type:\s*['\"]?([^'\"\s]+)['\"]?\s*$"
)
LEGACY_TYPE_RE = re.compile(r"(?m)^type:\s*['\"]?([^'\"\s]+)['\"]?\s*$")
LEGACY_ROLE_RE = re.compile(r"(?m)^role:\s*['\"]?([^'\"\s]+)['\"]?\s*$")
FAMILY_FIELD_RE = re.compile(r"(?m)^family:\s*['\"]?([^'\"\s]+)['\"]?\s*$")
OPERATION_FIELD_RE = re.compile(
    r"(?m)^operation:\s*['\"]?([^'\"\s]+)['\"]?\s*$"
)
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
TASK_STATUSES = {
    "planned",
    "building",
    "executing",
    "reported",
    "ok",
    "inconclusive",
    "blocked",
}
REPORT_REQUIRED_TASK_STATUSES = {"reported", "ok", "inconclusive"}
TERMINAL_TASK_STATUSES = {"ok", "inconclusive"}
REPORT_COMMON_FIELDS = (
    "outcome",
    "summary",
    "confidence",
    "completed_runs",
    "unresolved_runs",
    "evidence_bib",
)
VERIFICATION_STATUSES = {"pending", "verified"}
NON_ENTRY_TYPES = {"comment", "preamble", "string"}
DISCOVERY_TYPES = {
    "source-map",
    "source-reading",
    "topic-summary",
    "prior-art-verdict",
    "counterevidence-review",
    "landscape-review",
    "benchmark-landscape",
    "ideation",
    "novelty-verdict",
}
LEGACY_DISCOVERY_TYPES = {
    ("search", "source_gather"): "source-map",
    ("search", "source_read"): "source-reading",
    ("search", "search_and_read"): "source-reading",
    ("review", "topic_summary"): "topic-summary",
    ("review", "prior_art_check"): "prior-art-verdict",
    ("review", "counterevidence"): "counterevidence-review",
    ("review", "landscape_review"): "landscape-review",
    ("review", "benchmark_landscape"): "benchmark-landscape",
    ("idea", "idea_generation"): "ideation",
    ("idea", "novelty_check"): "novelty-verdict",
}
ALLOWED_OPERATIONS = {"paper-analysis", "source-analysis"}
DISCOVERY_PAGE_ROLES = (
    "Question and boundary",
    "Type payload",
    "Evidence map",
    "Limits and next move",
)
WRITING_STYLE_LABELS = (
    "Language and voice",
    "Sentence shape",
    "Evidence rule",
    "Required sections",
    "Optional sections",
    "Question and boundary",
    "Type payload",
    "Evidence map",
    "Limits and next move",
    "Section rules",
)


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


def _bib_verification(runtime_text: str) -> tuple[str, str | None, str | None]:
    """Return citation verification state; an absent receipt is pending."""
    bib_block = _yaml_block(runtime_text, "bib")
    if bib_block is None:
        return "pending", None, None
    verification = _yaml_block(textwrap.dedent(bib_block), "verification")
    if verification is None:
        return "pending", None, None
    return (
        _block_field(verification, "status") or "pending",
        _block_field(verification, "by"),
        _block_field(verification, "at"),
    )


def verification_counts(topic: Path) -> dict[str, int]:
    """Count complete Results by citation-verification state."""
    counts = {"pending": 0, "verified": 0, "invalid": 0}
    runs, results = _pair_maps(topic)
    for stem in sorted(runs.keys() & results.keys()):
        runtime_path = results[stem] / "runtime.yaml"
        if not runtime_path.is_file():
            continue
        status, _, runtime_text = _runtime(runtime_path)
        if status != "complete":
            continue
        verification, _, _ = _bib_verification(runtime_text)
        key = verification if verification in VERIFICATION_STATUSES else "invalid"
        counts[key] += 1
    return counts


def _topic_identity(topic: Path) -> tuple[str | None, str | None, list[str]]:
    """Return readable/compact b.j.t identity derived only from the path."""
    errors: list[str] = []
    task = topic
    job = task.parent
    block = job.parent
    bank = block.parent
    parts: list[str] = []
    for level, path in (("block", block), ("job", job), ("task", task)):
        match = SEGMENT_RE[level].fullmatch(path.name)
        if match is None:
            errors.append(f"address-{level}-name-invalid: {path}")
        else:
            parts.append(match.group(1))
    if bank.name != "discoveries":
        errors.append(f"address-bank-invalid: {bank}: expected discoveries/")
    if errors:
        return None, None, errors
    return ".".join(parts), "".join(parts), errors


def _page_errors(page: Path, question: str = "") -> list[str]:
    text = page.read_text(encoding="utf-8")
    errors: list[str] = []
    if not re.search(r"(?m)^folder-kind:\s*discovery\s*$", text):
        errors.append(f"page-folder-kind-invalid: {page}: expected discovery")
    if re.search(r"(?m)^page-type:\s*task\s*$", text):
        errors.append(f"page-task-type-forbidden: {page}")
    opening = re.search(
        r"(?ms)^## (?:Opening|Question)\s*\n(?P<body>.*?)(?=\n\s*\n|\Z)",
        text,
    )
    if not opening:
        errors.append(f"page-opening-missing: {page}")
    else:
        visible = re.sub(r"\s+", " ", opening.group("body")).strip()
        sentence_count = len(re.findall(r"[.!?](?=\s|$)", visible))
        if sentence_count not in {4, 5}:
            errors.append(
                f"page-opening-sentence-count: {page}: {sentence_count}"
            )
        if len(visible) > 520:
            errors.append(f"page-opening-too-long: {page}: {len(visible)}")
        question_words = re.findall(r"[a-z0-9]+", question.casefold())[:5]
        visible_words = re.findall(r"[a-z0-9]+", visible.casefold())[:5]
        if question_words and visible_words != question_words:
            errors.append(f"page-opening-question-drift: {page}")
    writing_style = re.search(
        r"(?ms)^## Writing Style\s*\n(.*?)(?=^## Content\s*$)", text
    )
    if not writing_style:
        errors.append(f"page-writing-style-missing: {page}")
    else:
        for label in WRITING_STYLE_LABELS:
            if not re.search(
                rf"(?m)^\*\*{re.escape(label)}\*\*:\s+\S", writing_style.group(1)
            ):
                errors.append(f"page-writing-style-label-missing: {page}: {label}")
    if not re.search(r"(?m)^## Content\s*$", text):
        errors.append(f"page-content-missing: {page}")
    if not re.search(r"(?m)^## Aims\s*$", text):
        errors.append(f"page-aims-missing: {page}")

    division_pairs = re.findall(r"(?m)^### ([0-9]+) · (.+?)\s*$", text)
    divisions = {number: name.strip() for number, name in division_pairs}
    aim_pairs = re.findall(r"(?m)^### A([0-9]+) · (.+?)\s*$", text)
    aim_groups = {
        number: re.sub(r"^[^A-Za-z0-9]+", "", name).strip()
        for number, name in aim_pairs
    }
    if len(division_pairs) != 4 or set(divisions) != {"1", "2", "3", "4"}:
        errors.append(f"page-discovery-division-set-invalid: {page}")
    if len(aim_pairs) != 4 or set(aim_groups) != {"1", "2", "3", "4"}:
        errors.append(f"page-discovery-aim-set-invalid: {page}")
    for index, role in enumerate(DISCOVERY_PAGE_ROLES, start=1):
        name = divisions.get(str(index), "")
        if not name.startswith(f"{role} · ") or not name[len(role) + 3 :].strip():
            errors.append(
                f"page-discovery-role-invalid: {page}: {index} expected {role!r}"
            )
    for number, aim_name in aim_groups.items():
        division_name = divisions.get(number)
        if division_name is None:
            errors.append(f"page-aim-division-missing: {page}: A{number}")
        elif aim_name != division_name:
            errors.append(
                f"page-aim-name-drift: {page}: A{number} "
                f"{aim_name!r} != {division_name!r}"
            )

    content = re.search(r"(?ms)^## Content\s*\n(.*?)(?=^## Aims\s*$)", text)
    if content:
        body = content.group(1)
        headings = list(re.finditer(r"(?m)^### [0-9]+ · .+?\s*$", body))
        for index, heading in enumerate(headings):
            end = headings[index + 1].start() if index + 1 < len(headings) else len(body)
            division = body[heading.end() : end]
            if not re.match(
                r"\s*\*\*[^*\n]+\*\*: [^\n]+\n```(?:text)?\s*\n",
                division,
            ):
                errors.append(
                    f"page-content-division-diagram-missing: {page}: "
                    f"{heading.group(0)}"
                )

    state = re.search(r"(?m)^state:\s*(.+?)\s*$", text)
    if state and state.group(1).startswith("✅"):
        ticks = re.findall(r"(?m)^- ([^\s]+)\s+A[0-9]+\.[0-9]+\s+·", text)
        if any(tick not in {"✅", "❄️"} for tick in ticks):
            errors.append(f"page-done-with-open-aim: {page}")
    return errors


def _manifest_errors(topic: Path) -> list[str]:
    manifest = topic / "discovery.yaml"
    if not manifest.is_file():
        return [f"manifest-missing: {manifest}"]

    text = manifest.read_text(encoding="utf-8")
    errors: list[str] = []
    readable, compact, identity_errors = _topic_identity(topic)
    errors.extend(identity_errors)
    if _field(text, VERSION_FIELD_RE) != "6":
        errors.append(f"manifest-version-invalid: {manifest}")
    if _field(text, KIND_FIELD_RE) != "discovery":
        errors.append(f"manifest-kind-invalid: {manifest}")
    task_status = _field(text, STATUS_RE)
    if task_status not in TASK_STATUSES:
        errors.append(f"manifest-status-invalid: {manifest}: {task_status!r}")
    elif (
        task_status in REPORT_REQUIRED_TASK_STATUSES
        and _yaml_block(text, "report") is None
    ):
        errors.append(f"manifest-report-missing: {manifest}: status={task_status}")

    if readable is not None:
        manifest_address = _field(text, ADDRESS_FIELD_RE)
        if manifest_address != readable:
            errors.append(
                f"manifest-address-mismatch: {manifest}: "
                f"{manifest_address!r} != {readable!r}"
            )
        manifest_compact = _field(text, ADDRESS_COMPACT_FIELD_RE)
        if manifest_compact != compact:
            errors.append(
                f"manifest-address-compact-mismatch: {manifest}: "
                f"{manifest_compact!r} != {compact!r}"
            )
        section_paths = (topic.parent.parent, topic.parent, topic)
        for section, expected, section_path in zip(
            ("block", "job", "task"), readable.split("."), section_paths
        ):
            block_text = _yaml_block(text, section)
            actual = _block_field(block_text, "id") if block_text else None
            if actual != expected:
                errors.append(
                    f"manifest-{section}-id-mismatch: {manifest}: "
                    f"{actual!r} != {expected!r}"
                )
            actual_slug = _block_field(block_text, "slug") if block_text else None
            expected_slug = section_path.name[4:]
            if actual_slug != expected_slug:
                errors.append(
                    f"manifest-{section}-slug-mismatch: {manifest}: "
                    f"{actual_slug!r} != {expected_slug!r}"
                )

    page = _field(text, PAGE_FIELD_RE)
    expected_page = f"{topic.name}.md"
    if page is None:
        errors.append(f"manifest-page-missing: {manifest}")
    elif Path(page).is_absolute() or Path(page).name != page:
        errors.append(f"manifest-page-invalid: {manifest}: {page!r}")
    elif page != expected_page:
        errors.append(
            f"manifest-page-stem-mismatch: {manifest}: {page!r} != {expected_page!r}"
        )
    elif not (topic / page).is_file():
        errors.append(f"page-missing: {topic / page}")
    else:
        page_text = (topic / page).read_text(encoding="utf-8")
        errors.extend(
            _page_errors(topic / page, question=_yaml_block(text, "question") or "")
        )
        page_state = re.search(r"(?m)^state:\s*(.+?)\s*$", page_text)
        if task_status in TERMINAL_TASK_STATUSES and (
            page_state is None or not page_state.group(1).startswith("✅")
        ):
            errors.append(
                f"manifest-terminal-page-open: {manifest}: "
                f"page_state={page_state.group(1)!r}"
                if page_state
                else f"manifest-terminal-page-open: {manifest}: page_state=None"
            )

    canonical = _field(text, DISCOVERY_TYPE_RE)
    legacy_type = _field(text, LEGACY_TYPE_RE)
    legacy_role = _field(text, LEGACY_ROLE_RE)
    legacy = None
    if legacy_type or legacy_role:
        legacy = LEGACY_DISCOVERY_TYPES.get(
            ((legacy_type or "").casefold(), (legacy_role or "").casefold())
        )
        if legacy is None:
            errors.append(
                f"manifest-legacy-type-invalid: {manifest}: "
                f"{legacy_type!r}/{legacy_role!r}"
            )

    if canonical is None and legacy is None:
        errors.append(f"manifest-discovery-type-missing: {manifest}")
    elif canonical is not None and canonical not in DISCOVERY_TYPES:
        errors.append(
            f"manifest-discovery-type-invalid: {manifest}: {canonical!r}"
        )
    elif canonical is not None and legacy is not None and canonical != legacy:
        errors.append(
            f"manifest-discovery-type-conflict: {manifest}: "
            f"{canonical!r} != legacy {legacy!r}"
        )
    return errors


def _report_errors(
    topic: Path,
    counts: dict[str, int],
    verification: dict[str, int],
) -> list[str]:
    manifest = topic / "discovery.yaml"
    if not manifest.is_file():
        return []
    text = manifest.read_text(encoding="utf-8")
    task_status = _field(text, STATUS_RE)
    report = _yaml_block(text, "report")
    errors: list[str] = []
    if report is None:
        return errors

    if task_status in TERMINAL_TASK_STATUSES:
        for field in REPORT_COMMON_FIELDS:
            if _block_field(report, field) is None:
                errors.append(f"manifest-report-field-missing: {manifest}: {field}")

    for field, expected in (
        ("completed_runs", counts["complete"]),
        ("unresolved_runs", counts["unresolved"]),
    ):
        raw = _block_field(report, field)
        if raw is None:
            continue
        try:
            actual = int(raw)
        except ValueError:
            errors.append(f"manifest-report-count-invalid: {manifest}: {field}={raw!r}")
            continue
        if actual != expected:
            errors.append(
                f"manifest-report-count-mismatch: {manifest}: "
                f"{field}={actual} != {expected}"
            )

    evidence_bib = _block_field(report, "evidence_bib")
    if evidence_bib is not None:
        canonical_path = default_bib_path(topic)
        canonical = canonical_path.relative_to(topic).as_posix()
        if evidence_bib != canonical:
            errors.append(
                f"manifest-report-evidence-bib-invalid: {manifest}: "
                f"{evidence_bib!r} != {canonical!r}"
            )
        elif not canonical_path.is_file():
            errors.append(f"manifest-report-evidence-bib-missing: {canonical_path}")

    pending = verification["pending"] + verification["invalid"]
    if task_status in TERMINAL_TASK_STATUSES and pending:
        errors.append(
            f"manifest-terminal-with-unverified-citation: {manifest}: "
            f"pending={pending}"
        )
    return errors


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

    if (topic / "evidence").exists():
        errors.append(
            f"legacy-root-evidence-forbidden: {topic / 'evidence'}: "
            "use outline/evidence/"
        )
    errors.extend(_manifest_errors(topic))
    topic_readable, topic_compact, _ = _topic_identity(topic)

    runs, results = _pair_maps(topic)
    for stem in sorted(runs.keys() | results.keys()):
        if not RUN_RE.fullmatch(stem):
            errors.append(f"runname-invalid: {stem}")
    for stem in sorted(runs.keys() - results.keys()):
        errors.append(f"missing-result: runs/{stem}.sh has no results/{stem}/")
    for stem in sorted(results.keys() - runs.keys()):
        errors.append(f"orphan-result: results/{stem}/ has no runs/{stem}.sh")

    for stem in sorted(runs.keys() & results.keys()):
        run_path = runs[stem]
        result_dir = results[stem]
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
        if topic_readable is not None and RUN_RE.fullmatch(stem):
            run_id = stem[:3]
            expected_address = f"{topic_readable}.{run_id}"
            expected_compact = f"{topic_compact}{run_id}"
            runtime_address = _field(runtime_text, ADDRESS_FIELD_RE)
            runtime_compact = _field(runtime_text, ADDRESS_COMPACT_FIELD_RE)
            if runtime_address != expected_address:
                errors.append(
                    f"runtime-address-mismatch: {runtime_path}: "
                    f"{runtime_address!r} != {expected_address!r}"
                )
            if runtime_compact != expected_compact:
                errors.append(
                    f"runtime-address-compact-mismatch: {runtime_path}: "
                    f"{runtime_compact!r} != {expected_compact!r}"
                )
        family = _field(runtime_text, FAMILY_FIELD_RE)
        if family != "discovery":
            errors.append(f"runtime-family-invalid: {runtime_path}: {family!r}")
        operation = _field(runtime_text, OPERATION_FIELD_RE)
        if operation not in ALLOWED_OPERATIONS:
            errors.append(
                f"runtime-operation-invalid: {runtime_path}: {operation!r}"
            )
        if not re.search(r"(?m)^trigger:\s*$", runtime_text):
            errors.append(f"runtime-trigger-missing: {runtime_path}")
        subject_block = _yaml_block(runtime_text, "subject")
        if subject_block is None:
            errors.append(f"runtime-subject-missing: {runtime_path}")
        elif subject_block is not None and operation in ALLOWED_OPERATIONS:
            subject_kind = _block_field(subject_block, "kind")
            expected_operation = (
                "paper-analysis" if subject_kind == "paper" else "source-analysis"
            )
            if operation != expected_operation:
                errors.append(
                    f"runtime-operation-subject-mismatch: {runtime_path}: "
                    f"{operation!r} != {expected_operation!r}"
                )

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
        verification_status, verified_by, verified_at = _bib_verification(runtime_text)
        if verification_status not in VERIFICATION_STATUSES:
            errors.append(
                f"runtime-bib-verification-status-invalid: {runtime_path}: "
                f"{verification_status!r}"
            )
        elif verification_status == "verified":
            if verified_by is None or not verified_by.startswith("person:"):
                errors.append(f"runtime-bib-verifier-missing: {runtime_path}")
            if verified_at is None:
                errors.append(f"runtime-bib-verified-at-missing: {runtime_path}")

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
    errors.extend(_report_errors(topic, counts, verification_counts(topic)))
    return errors, counts, complete_entries


def aggregate_bib(entries: Iterable[BibEntry]) -> str:
    unique: dict[str, BibEntry] = {}
    for entry in entries:
        key_id = entry.key.casefold()
        unique.setdefault(key_id, entry)
    ordered = sorted(unique.values(), key=lambda item: (item.key.casefold(), item.key))
    return ("\n\n".join(entry.text for entry in ordered) + "\n") if ordered else ""


def default_bib_path(topic: Path) -> Path:
    """Return the Outline-owned derived Discovery Bib path for ``topic``."""
    manifest = topic / "discovery.yaml"
    stem = topic.name
    if manifest.is_file():
        page = _field(manifest.read_text(encoding="utf-8"), PAGE_FIELD_RE)
        if page:
            stem = Path(page).stem
    return topic / "outline" / "evidence" / "bibex" / f"{stem}.bib"


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
    verification = verification_counts(topic)
    print(
        "citation-verification: "
        + " ".join(f"{key}={verification[key]}" for key in sorted(verification))
    )
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 1
    pending = verification["pending"] + verification["invalid"]
    if pending:
        print(
            "STRUCTURE_OK discovery-page-and-run contract · "
            f"CLOSURE_HELD citation-verification={pending}"
        )
    else:
        print("OK discovery-page-and-run contract")
    return 0


def command_build_bib(topic: Path, output: Path | None, write: bool) -> int:
    canonical = default_bib_path(topic.resolve())
    if write and output is not None and output.resolve() != canonical.resolve():
        print(
            f"ERROR bib-output-noncanonical: {output}: expected {canonical}",
            file=sys.stderr,
        )
        return 1
    errors, counts, entries = check_topic(topic)
    if write:
        errors = [
            error
            for error in errors
            if not error.startswith("manifest-report-evidence-bib-missing:")
        ]
    _print_summary(counts)
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 1
    text = aggregate_bib(entries)
    output_path = output or canonical
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
    check = subparsers.add_parser(
        "check", help="validate the Discovery Page plus Run/Result pairs"
    )
    check.add_argument("topic", type=Path)
    bib = subparsers.add_parser("build-bib", help="build derived Task Page Evidence Bib")
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
