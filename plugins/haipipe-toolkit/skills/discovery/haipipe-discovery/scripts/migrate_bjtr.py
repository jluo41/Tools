#!/usr/bin/env python3
"""Migrate legacy two-level Discovery banks to explicit BJTR Task Pages."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


LEGACY_BLOCK_RE = re.compile(r"^[A-Z][0-9]{2}_(.+)$")
LEGACY_TASK_RE = re.compile(r"^([0-9]{2})_(.+)$")
CANONICAL_BLOCK_RE = re.compile(r"^b[0-9]{2}_.+_.+$")
TOP_LEVEL_RE = re.compile(r"(?m)^([A-Za-z_][A-Za-z0-9_-]*):")
SCALAR_RE = r"(?m)^{name}:\s*([^\n#]+)"
LEGACY_TYPE_MAP = {
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
TEXT_SUFFIXES = {
    ".bib",
    ".csv",
    ".do",
    ".html",
    ".htm",
    ".json",
    ".md",
    ".ps1",
    ".py",
    ".sh",
    ".tex",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
RECORD_NAMES = ("summary.md", "verdict.md", "landscape.md", "ideas.md")
READABLE_NAMES = RECORD_NAMES + ("notes.md", "sources.md")
DISPLAY_WORDS = {
    "ai": "AI",
    "cms": "CMS",
    "cpt": "CPT",
    "did": "DiD",
    "healthit": "HealthIT",
    "is": "IS",
    "llm": "LLM",
    "llms": "LLMs",
    "misq": "MISQ",
    "rx": "Rx",
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
MIGRATION_METHOD = (
    "method: Read the current records and admit new evidence through numbered Paper Runs."
)


@dataclass(frozen=True)
class Unit:
    bank: Path
    project: Path
    old_block: str
    old_task: str
    block_name: str
    job_name: str
    task_name: str
    block_title: str
    job_title: str

    @property
    def old_path(self) -> Path:
        return self.bank / self.old_block / self.old_task

    @property
    def new_path(self) -> Path:
        return self.bank / self.block_name / self.job_name / self.task_name

    @property
    def address(self) -> str:
        return ".".join(
            (self.block_name[:3], self.job_name[:3], self.task_name[:3])
        )

    @property
    def address_compact(self) -> str:
        return self.address.replace(".", "")


def slugify(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    value = re.sub(r"_+", "_", value)
    if "_" not in value:
        value = f"{value}_inquiry"
    return value


def humanize(value: str) -> str:
    return value.replace("_", " ").replace("-", " ").strip()


def default_board_slug(project: Path) -> str:
    stem = re.sub(r"(?i)^project[-_]*", "", project.name).strip("-_")
    stem = re.sub(r"[^a-z0-9]+", "_", stem.lower()).strip("_")
    return f"{stem or 'project'}_evidence_board"


def default_board_title(project: Path) -> str:
    stem = re.sub(r"(?i)^project[-_]*", "", project.name).strip("-_")
    return f"{humanize(stem or 'project').capitalize()} evidence board"


def scalar(text: str, name: str, default: str = "") -> str:
    match = re.search(SCALAR_RE.format(name=re.escape(name)), text)
    if not match:
        return default
    return match.group(1).strip().strip("'\"")


def nested_scalar(text: str, section: str, name: str, default: str = "") -> str:
    match = re.search(
        rf"(?ms)^{re.escape(section)}:\s*\n"
        rf"(?P<body>(?:^[ \t]+.*(?:\n|$))*)",
        text,
    )
    if not match:
        return default
    child = re.search(
        rf"(?m)^[ \t]+{re.escape(name)}:\s*([^\n#]+)", match.group("body")
    )
    return child.group(1).strip().strip("'\"") if child else default


def top_level_sections(text: str) -> list[tuple[str, str]]:
    matches = list(TOP_LEVEL_RE.finditer(text))
    return [
        (
            match.group(1),
            text[match.start() : matches[index + 1].start()]
            if index + 1 < len(matches)
            else text[match.start() :],
        )
        for index, match in enumerate(matches)
    ]


def yaml_block_text(text: str, name: str) -> str:
    section = next((body for key, body in top_level_sections(text) if key == name), "")
    if not section:
        return ""
    first, *rest = section.splitlines()
    inline = first.split(":", 1)[1].strip()
    if inline and inline not in {"|", ">", "|-", ">-"}:
        return inline.strip("'\"")
    lines = []
    for line in rest:
        if line.startswith("  "):
            lines.append(line[2:])
        elif line.strip():
            break
        else:
            lines.append("")
    return "\n".join(lines).strip()


def discover_type(text: str, task_path: Path) -> str:
    legacy_type = scalar(text, "type").lower()
    legacy_role = scalar(text, "role").lower()
    canonical = LEGACY_TYPE_MAP.get((legacy_type, legacy_role))
    if canonical:
        return canonical
    if legacy_type == "search" and legacy_role.startswith("source_gather"):
        return "source-reading" if (task_path / "notes.md").is_file() else "source-map"
    raise ValueError(
        f"unsupported legacy Discovery type/role in {task_path}: "
        f"{legacy_type!r}/{legacy_role!r}"
    )


def typed_record(task_path: Path, discovery_type: str) -> str | None:
    preferred = {
        "topic-summary": "summary.md",
        "prior-art-verdict": "verdict.md",
        "counterevidence-review": "verdict.md",
        "landscape-review": "landscape.md",
        "benchmark-landscape": "landscape.md",
        "ideation": "ideas.md",
        "novelty-verdict": "verdict.md",
    }.get(discovery_type)
    if preferred and (task_path / preferred).is_file():
        return preferred
    return next((name for name in RECORD_NAMES if (task_path / name).is_file()), None)


def normalized_task_status(text: str) -> str:
    """Translate a legacy status without claiming a Report that is absent."""
    raw = scalar(text, "status", "planned").lower()
    has_report = any(key == "report" for key, _ in top_level_sections(text))
    if raw in {"review", "reported", "ok", "inconclusive"}:
        raw = "reported" if has_report else "executing"
    elif raw not in TASK_STATUSES:
        raw = "planned"
    return raw


def manifest_text(unit: Unit, source: str | None) -> tuple[str, str, str]:
    block_id, job_id, task_id = unit.address.split(".")
    block_slug = unit.block_name[4:]
    job_slug = unit.job_name[4:]
    task_slug = unit.task_name[4:]
    if source is None:
        title = humanize(task_slug).capitalize()
        question = f"What do the collected sources establish about {humanize(task_slug)}?"
        body = (
            "status: planned\n"
            'created_at: "2026-09-01T00:00:00-04:00"\n'
            'updated_at: "2026-09-01T00:00:00-04:00"\n\n'
            "question: |\n"
            f"  {question}\n"
            "sources:\n"
            "  local_first: true\n"
            "  verification_required: true\n"
            "  candidate_rule: >-\n"
            "    Existing source files remain migration inputs; future admitted sources\n"
            "    become Paper Runs only after canonical identity is resolved.\n"
        )
        discovery_type = "source-reading"
    else:
        title = scalar(source, "title", humanize(task_slug).capitalize())
        question = yaml_block_text(source, "question") or title
        discovery_type = discover_type(
            source, unit.new_path if unit.new_path.is_dir() else unit.old_path
        )
        normalized_status = normalized_task_status(source)
        kept: list[str] = []
        for key, section in top_level_sections(source):
            if key in {
                "version",
                "kind",
                "address",
                "address_compact",
                "discovery_type",
                "block",
                "job",
                "task",
                "page",
                "id",
                "type",
                "role",
                "group",
                "slug",
                "title",
                "expected_outputs",
            }:
                continue
            if key == "build":
                section = re.sub(r"(?m)^build:", "instrument:", section, count=1)
                section = re.sub(r"(?m)^(\s+)artifact:", r"\1path:", section)
            elif key == "status":
                section = f"status: {normalized_status}\n"
            kept.append(section.rstrip())
        record = typed_record(
            unit.new_path if unit.new_path.is_dir() else unit.old_path,
            discovery_type,
        )
        report_index = next(
            (index for index, section in enumerate(kept) if section.startswith("report:")),
            len(kept),
        )
        if record:
            kept.insert(report_index, f"typed_record: {record}")
        body = "\n\n".join(section for section in kept if section).strip() + "\n"

    header = (
        "version: 6\n"
        "kind: discovery\n"
        f"address: {unit.address}\n"
        f"address_compact: {unit.address_compact}\n"
        f"discovery_type: {discovery_type}\n"
        "block:\n"
        f"  id: {block_id}\n"
        f"  slug: {block_slug}\n"
        f"  title: {json.dumps(unit.block_title, ensure_ascii=False)}\n"
        "job:\n"
        f"  id: {job_id}\n"
        f"  slug: {job_slug}\n"
        f"  title: {json.dumps(unit.job_title, ensure_ascii=False)}\n"
        "task:\n"
        f"  id: {task_id}\n"
        f"  slug: {task_slug}\n"
        f"  title: {json.dumps(title, ensure_ascii=False)}\n"
        f"page: {unit.task_name}.md\n"
    )
    return header + body, discovery_type, question


def display_phrase(task_slug: str, limit: int | None = None) -> str:
    words = humanize(task_slug).split()
    if limit is not None:
        words = words[:limit]
    displayed = [DISPLAY_WORDS.get(word.lower(), word.lower()) for word in words]
    if displayed and displayed[0] not in DISPLAY_WORDS.values():
        displayed[0] = displayed[0].capitalize()
    return " ".join(displayed)


def page_title(task_slug: str) -> str:
    words = humanize(task_slug).split()
    if len(words) < 3:
        words.extend(("evidence", "review")[: 3 - len(words)])
    return display_phrase("_".join(words), limit=6)


def opening_lead(question: str) -> str:
    prompt = re.sub(r"[.!?]+", "", re.sub(r"\s+", " ", question)).strip()
    if len(prompt) > 125:
        shortened = prompt[:122].rsplit(" ", 1)[0].rstrip(" ,;:-")
        prompt = f"{shortened}…"
    if prompt:
        prompt = prompt[0].upper() + prompt[1:]
    return f"{prompt}?" if prompt else "What does the available evidence establish?"


def page_text(
    task_path: Path,
    task_name: str,
    question: str,
    status: str,
    discovery_type: str,
    heading: str | None = None,
) -> str:
    links = [name for name in READABLE_NAMES if (task_path / name).is_file()]
    link_rows = "\n".join(
        f"- [{humanize(Path(name).stem).capitalize()}]({name})" for name in links
    ) or "- No synthesis record has been written yet."
    state = {
        "planned": "🔴 OPEN",
        "reported": "🟡 REPORTED",
        "ok": "✅ REPORTED",
        "inconclusive": "⏸️ INCONCLUSIVE",
        "blocked": "⏸️ BLOCKED",
    }.get(status, "🟡 ACTIVE")
    records_tick = {
        "ok": "✅",
        "inconclusive": "❄️",
        "blocked": "❄️",
    }.get(status, "🔨")
    has_runs = any((task_path / "runs").glob("r*.sh"))
    evidence_tick = (
        "✅"
        if has_runs and status == "ok"
        else "🔨"
        if has_runs and status not in {"inconclusive", "blocked"}
        else "❄️"
    )
    normalized_question = re.sub(r"\s+", " ", question).strip()
    subject = display_phrase(task_name[4:], limit=6)
    page_heading = heading or page_title(task_name[4:])
    record_hint = (
        "the preserved "
        + " and ".join(humanize(Path(name).stem) for name in links[:2])
        + " records"
        if links
        else "the current empty record set"
    )
    payload_name = humanize(discovery_type)
    division_names = (
        f"Question and boundary · {subject}",
        f"Type payload · {subject} {payload_name}",
        f"Evidence map · {subject} sources",
        f"Limits and next move · {subject} decision",
    )
    return f"""# {page_heading}
state: {state}
owner: CC
folder-kind: discovery
{MIGRATION_METHOD}

## Opening
{opening_lead(normalized_question)}
This `{discovery_type}` Page tests the {subject} question against {record_hint}.
A source counts only after its canonical identity is resolved and its claim traces to a Result.
Next, admit a {subject} source, revise the synthesis, or hold the boundary.

**Current question**: {normalized_question}

**Scope and admission**: `discovery.yaml` records the source boundary; only a resolved canonical Subject that is relevant enough to analyze may enter as a new Run.

**Migration state**: Existing records remain linked below, while historical Paper Runs are deliberately not inferred from those files.

## Writing Style
**Audience and purpose**: Write for a reader who needs the answer, its evidence boundary, and the next decision without reading the execution history first.

**Language and voice**: Use plain English, active voice, and domain terms only after defining them in the sentence that first needs them.

**Sentence shape**: Put one claim on each source line; keep labels as short noun phrases and move explanatory clauses into prose.

**Evidence rule**: Separate legacy indexes from new Result-backed claims, and attach every newly admitted factual source to its Run, Result Card, facts, and cite key.

**Required sections**: Keep Opening, Writing Style, all four Content roles, and matching Aims; a migration Page may keep unfinished payload work visibly active.

**Optional sections**: Add a top-level Diagram only when it clarifies the whole inquiry; keep typed records, PDFs, and other supporting files linked rather than copied.

**Question and boundary**: State the exact inquiry, evidence population, and canonical-Subject admission rule.

**Type payload**: Synthesize the selected `{discovery_type}` promise in the root Page rather than leaving the reader at a legacy file link.

**Evidence map**: Bind factual support to Result Cards and cite keys, and keep disagreements and unresolved gaps visible.

**Limits and next move**: Say what the evidence does not establish and choose one lawful route: admit, revise, extend, hold, or close.

**Section rules**: Aims mirror the complete subject-specific division names and report current facts rather than future plans.

**Revision rule**: Keep Content and Aim names aligned, and update synthesis prose only when its evidence route is visible.

## Content
### 1 · {division_names[0]}
**{subject} inquiry boundary**: how this question becomes a bounded evidence admission rule.
```text
❓ Question  discovery.yaml
🧭 Scope     source boundary
🚪 Admit     canonical Subject → rNN
```

The current question is: {normalized_question}
The manifest owns the candidate boundary, while relevance and canonical identity decide whether a source becomes a Run.

### 2 · {division_names[1]}
**{subject} reader payload**: where the `{discovery_type}` synthesis lives during migration.
```text
📄 Page      active synthesis surface
🗂 Records   preserved typed record · notes · sources
```

{link_rows}

These records preserve the earlier synthesis and source boundary without pretending that a link alone is the finished root article.

### 3 · {division_names[2]}
**{subject} evidence lineage**: how preserved indexes differ from newly admitted evidence.
```text
🗃 Legacy    readable migration input
🧾 New       rNN ticket ↔ Result · facts · Bib
```

The linked source and note files remain readable indexes.
They do not become Paper Run receipts unless a canonical Subject is admitted and analyzed through `runs/rNN_*.sh`.

### 4 · {division_names[3]}
**{subject} handoff**: what structural migration establishes and what evidence work remains.
```text
⚠️ Limit     no historical Run inferred
➡️ Next      admit source · revise synthesis · hold
```

Structural migration establishes the BJTR address and preserves existing records, but it does not verify or backfill their source lineage.
The next evidence action is to admit a canonical Subject as a Run, revise the Page from completed Results, or explicitly hold the unresolved boundary.

## Aims
### A1 · 🔎 {division_names[0]}
- ✅ A1.1 · The Task Page states one bounded external-evidence question and its admission rule.
  **Done when:** The question, source boundary, and canonical-Subject gate can be found from this Page.
  **Now:** The question and admission rule are visible here; `discovery.yaml` owns the detailed source boundary.

### A2 · 📚 {division_names[1]}
- {records_tick} A2.1 · The root Page realizes the `{discovery_type}` reader promise from the preserved records.
  **Done when:** The Page carries the type-specific synthesis rather than only pointing at a legacy record.
  **Now:** Existing records are preserved and linked; synthesis into the root Page remains explicit migration work unless this Aim is met.

### A3 · 🔗 {division_names[2]}
- {evidence_tick} A3.1 · New evidence is traceable to one canonical Subject per Run.
  **Done when:** Every newly admitted source has a same-stem Run, Result, runtime receipt, facts, and authoritative Bib entry.
  **Now:** Existing indexes are preserved; historical Paper Runs were not inferred during structural migration.

### A4 · 🧭 {division_names[3]}
- ✅ A4.1 · The Page states what migration does not establish and the lawful next evidence action.
  **Done when:** A reader can distinguish preserved legacy material from verified Result-backed evidence and choose the next route.
  **Now:** The limitation and the admit, revise, or hold routes are stated in Content.
"""


def plan_bank(
    bank: Path,
    board_slug: str | None = None,
    board_title: str | None = None,
) -> list[Unit]:
    bank = bank.resolve()
    if bank.name != "discoveries" or not bank.is_dir():
        raise ValueError(f"not a Discovery bank: {bank}")
    legacy_blocks = sorted(
        path
        for path in bank.iterdir()
        if path.is_dir() and LEGACY_BLOCK_RE.fullmatch(path.name)
    )
    occupied = {
        int(path.name[1:3])
        for path in bank.iterdir()
        if path.is_dir() and CANONICAL_BLOCK_RE.fullmatch(path.name)
    }
    available = (number for number in range(1, 100) if number not in occupied)
    block_number = next(available)
    block_slug = slugify(board_slug or default_board_slug(bank.parent))
    block_name = f"b{block_number:02d}_{block_slug}"
    block_title = board_title or default_board_title(bank.parent)
    units: list[Unit] = []
    for job_number, old_block_path in enumerate(legacy_blocks, start=1):
        group_slug = slugify(LEGACY_BLOCK_RE.fullmatch(old_block_path.name).group(1))
        job_name = f"j{job_number:02d}_{group_slug}_inquiry"
        candidates = sorted(
            path
            for path in old_block_path.iterdir()
            if path.is_dir() and LEGACY_TASK_RE.fullmatch(path.name)
        )
        job_title = f"{humanize(group_slug).capitalize()} inquiry"
        for candidate in candidates:
            manifest = candidate / "discovery.yaml"
            if manifest.is_file():
                source = manifest.read_text(encoding="utf-8")
                group_title = nested_scalar(source, "group", "title", "")
                if group_title:
                    job_title = (
                        group_title
                        if group_title.lower().endswith(" inquiry")
                        else f"{group_title} inquiry"
                    )
                break
        for candidate in candidates:
            task_match = LEGACY_TASK_RE.fullmatch(candidate.name)
            task_slug = slugify(task_match.group(2))
            units.append(
                Unit(
                    bank=bank,
                    project=bank.parent,
                    old_block=old_block_path.name,
                    old_task=candidate.name,
                    block_name=block_name,
                    job_name=job_name,
                    task_name=f"t{task_match.group(1)}_{task_slug}",
                    block_title=block_title,
                    job_title=job_title,
                )
            )
    return units


def replacements(units: list[Unit]) -> list[tuple[str, str]]:
    pairs: set[tuple[str, str]] = set()
    for unit in units:
        old_pair = f"{unit.old_block}/{unit.old_task}"
        new_pair = f"{unit.block_name}/{unit.job_name}/{unit.task_name}"
        pairs.add((f"discoveries/{old_pair}", f"discoveries/{new_pair}"))
        pairs.add((old_pair, new_pair))
        pairs.add((unit.old_task, unit.task_name))
        new_group = f"{unit.block_name}/{unit.job_name}"
        pairs.add((f"discoveries/{unit.old_block}", f"discoveries/{new_group}"))
        pairs.add((unit.old_block, new_group))
    return sorted(pairs, key=lambda pair: len(pair[0]), reverse=True)


def replace_project_references(project: Path, pairs: list[tuple[str, str]]) -> int:
    changed = 0
    for path in project.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and ".pre-" not in path.name:
            continue
        if ".git" in path.parts:
            continue
        try:
            original = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        updated = original
        for old, new in pairs:
            if old[0].isdigit():
                updated = re.sub(
                    rf"(?<![A-Za-z0-9]){re.escape(old)}(?![A-Za-z0-9])",
                    new,
                    updated,
                )
            else:
                updated = updated.replace(old, new)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    return changed


def apply_bank(units: list[Unit]) -> tuple[int, int]:
    if not units:
        return 0, 0
    bank = units[0].bank
    for unit in units:
        if unit.new_path.exists():
            raise FileExistsError(unit.new_path)
    block_names = {unit.block_name for unit in units}
    if len(block_names) != 1:
        raise ValueError("one legacy bank migration must resolve to one Board Block")
    block_path = bank / units[0].block_name
    if block_path.exists():
        raise FileExistsError(block_path)
    block_path.mkdir()
    grouped: dict[str, list[Unit]] = {}
    for unit in units:
        grouped.setdefault(unit.old_block, []).append(unit)
    for old_block, block_units in grouped.items():
        job_path = block_path / block_units[0].job_name
        job_path.mkdir()
        old_group_path = bank / old_block
        for unit in block_units:
            (old_group_path / unit.old_task).rename(job_path / unit.task_name)
        for group_item in sorted(old_group_path.iterdir()):
            destination = job_path / group_item.name
            if destination.exists():
                raise FileExistsError(destination)
            group_item.rename(destination)
        old_group_path.rmdir()

    for unit in units:
        manifest = unit.new_path / "discovery.yaml"
        source = manifest.read_text(encoding="utf-8") if manifest.is_file() else None
        migrated, discovery_type, question = manifest_text(unit, source)
        manifest.write_text(migrated, encoding="utf-8")
        status = scalar(migrated, "status", "reported")
        (unit.new_path / f"{unit.task_name}.md").write_text(
            page_text(
                unit.new_path,
                unit.task_name,
                question,
                status,
                discovery_type,
            ),
            encoding="utf-8",
        )

    changed_refs = replace_project_references(
        units[0].project, replacements(units)
    )
    return len(block_names), changed_refs


def repair_canonical_pages(bank: Path, write: bool) -> tuple[int, int]:
    """Refresh only Pages carrying the deterministic migration signature."""
    bank = bank.resolve()
    if bank.name != "discoveries" or not bank.is_dir():
        raise ValueError(f"not a Discovery bank: {bank}")
    found = changed = 0
    for manifest in sorted(bank.glob("b[0-9][0-9]_*/j[0-9][0-9]_*/t[0-9][0-9]_*/discovery.yaml")):
        task_path = manifest.parent
        page = task_path / f"{task_path.name}.md"
        if not page.is_file():
            continue
        page_source = page.read_text(encoding="utf-8")
        if MIGRATION_METHOD not in page_source:
            continue
        found += 1
        manifest_source = manifest.read_text(encoding="utf-8")
        status = normalized_task_status(manifest_source)
        updated_manifest = re.sub(
            r"(?m)^status:\s*[^\n#]+$",
            f"status: {status}",
            manifest_source,
            count=1,
        )
        question = yaml_block_text(updated_manifest, "question")
        discovery_type = scalar(updated_manifest, "discovery_type")
        heading_match = re.search(r"(?m)^#\s+(.+?)\s*$", page_source)
        heading = (
            heading_match.group(1)
            if heading_match
            else page_title(task_path.name[4:])
        )
        updated_page = page_text(
            task_path,
            task_path.name,
            question,
            status,
            discovery_type,
            heading=heading,
        )
        print(
            f"REPAIR {page.relative_to(bank.parent)} "
            f"status={scalar(manifest_source, 'status')}->{status}"
        )
        if write:
            manifest.write_text(updated_manifest, encoding="utf-8")
            page.write_text(updated_page, encoding="utf-8")
            changed += 1
    return found, changed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="migrate legacy Discovery banks to explicit b/j/t addresses"
    )
    parser.add_argument("banks", nargs="+", type=Path)
    parser.add_argument("--write", action="store_true")
    parser.add_argument(
        "--board-slug",
        help="optional noun-rich slug for the one Board created from this bank",
    )
    parser.add_argument(
        "--board-title",
        help="optional human title for the one Board created from this bank",
    )
    parser.add_argument(
        "--repair-pages",
        action="store_true",
        help="refresh only canonical Pages carrying the migration signature",
    )
    args = parser.parse_args()
    if (args.board_slug or args.board_title) and len(args.banks) != 1:
        parser.error("--board-slug/--board-title require exactly one bank")
    total_blocks = total_tasks = total_refs = 0
    if args.repair_pages:
        total_found = total_changed = 0
        for bank in args.banks:
            found, changed = repair_canonical_pages(bank, args.write)
            total_found += found
            total_changed += changed
        mode = "WROTE" if args.write else "DRY-RUN"
        print(
            f"{mode} migration_pages={total_found} "
            f"changed={total_changed if args.write else '-'}"
        )
        return 0
    for bank in args.banks:
        units = plan_bank(bank, args.board_slug, args.board_title)
        if not units:
            print(f"SKIP {bank}: no legacy Discovery folders")
            continue
        print(f"BANK {bank.resolve()}")
        for unit in units:
            print(f"  {unit.old_path.relative_to(unit.project)}")
            print(f"    -> {unit.new_path.relative_to(unit.project)} [{unit.address}]")
        if args.write:
            blocks, refs = apply_bank(units)
            total_blocks += blocks
            total_tasks += len(units)
            total_refs += refs
    mode = "WROTE" if args.write else "DRY-RUN"
    print(
        f"{mode} blocks={total_blocks if args.write else '-'} "
        f"tasks={total_tasks if args.write else '-'} "
        f"reference_files={total_refs if args.write else '-'}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
