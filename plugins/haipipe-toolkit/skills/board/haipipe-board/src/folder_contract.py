"""Discovery and structural validation for phase-owned Folder contracts.

The contract intentionally uses a small frontmatter reader instead of loading
the skills as YAML documents. Skill descriptions may contain punctuation that
is legal Markdown but awkward for a broad YAML round-trip; the rows we need are
simple scalars indented directly under ``metadata:``.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


REQUIRED_SECTIONS = (
    "Position",
    "Folder Kind",
    "Input",
    "Page Face",
    "Task Face",
    "Plugins",
    "Gate and Closure",
    "Handoff",
    "Files",
)
PRIMARY_FACES = {"page", "task"}
PAGE_RULINGS = {"none", "domain-gate", "local"}
_PHASE = re.compile(r"^[A-Z][0-9]+$")
_KIND = re.compile(r"^[a-z][a-z0-9-]*$")


def _frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    parts = text.split("---", 2)
    return parts[1] if len(parts) == 3 else ""


def _top_row(front: str, key: str) -> str:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*(.*?)\s*$", front)
    return _clean(match.group(1)) if match else ""


def _metadata_row(front: str, key: str) -> str:
    match = re.search(rf"(?m)^  {re.escape(key)}:\s*(.*?)\s*$", front)
    return _clean(match.group(1)) if match else ""


def _clean(value: str) -> str:
    value = re.sub(r"\s+#.*$", "", value).strip()
    return value.strip("\"'")


@dataclass(frozen=True)
class PhaseContract:
    path: Path
    name: str
    workflow: str
    phase: str
    folder_kind: str
    primary_face: str
    page_ruling: str
    legacy_page_type: str = ""


def read_contract(path: Path) -> PhaseContract | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    front = _frontmatter(text)
    workflow = _metadata_row(front, "workflow")
    if not workflow:
        return None
    return PhaseContract(
        path=path,
        name=_top_row(front, "name"),
        workflow=workflow,
        phase=_metadata_row(front, "phase"),
        folder_kind=_metadata_row(front, "folder_kind"),
        primary_face=_metadata_row(front, "primary_face"),
        page_ruling=_metadata_row(front, "page_ruling"),
        legacy_page_type=_metadata_row(front, "legacy_page_type"),
    )


def discover(skills_root: Path) -> list[PhaseContract]:
    contracts: list[PhaseContract] = []
    for path in sorted(skills_root.glob("*/workflow-phases/*/SKILL.md")):
        if any(part.startswith("_") for part in path.relative_to(skills_root).parts):
            continue
        contract = read_contract(path)
        if contract is not None:
            contracts.append(contract)
    return contracts


def resolve(
    skills_root: Path, *, folder_kind: str = "", legacy_page_type: str = ""
) -> PhaseContract | None:
    """Resolve one phase contract, raising on an ambiguous declaration."""
    if not folder_kind and not legacy_page_type:
        return None
    matches = [
        contract
        for contract in discover(skills_root)
        if (folder_kind and contract.folder_kind == folder_kind)
        or (legacy_page_type and contract.legacy_page_type == legacy_page_type)
    ]
    if len(matches) > 1:
        key = folder_kind or legacy_page_type
        raise ValueError(
            "Folder contract %r is ambiguous: %s"
            % (key, ", ".join(str(item.path) for item in matches))
        )
    return matches[0] if matches else None


def current_folder_kind(folder: Path) -> str:
    """Read the authoritative current kind from ``workflow/phase.yaml``.

    An absent file means the Folder has a fixed identity and may use its Page
    frontmatter. A present file is authoritative: malformed current state is a
    routing error, never permission to fall back to a stale Markdown key.
    """
    phase_file = Path(folder) / "workflow" / "phase.yaml"
    if not phase_file.is_file():
        return ""
    lines = phase_file.read_text(encoding="utf-8", errors="replace").splitlines()
    try:
        start = next(
            index for index, line in enumerate(lines)
            if re.fullmatch(r"current:\s*(?:#.*)?", line)
        )
    except StopIteration as exc:
        raise ValueError(f"{phase_file}: missing top-level current block") from exc

    rows: dict[str, str] = {}
    for line in lines[start + 1:]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line[:1].isspace():
            break
        match = re.match(r"\s+([A-Za-z][A-Za-z0-9-]*):\s*(.*?)\s*$", line)
        if match:
            rows[match.group(1)] = _clean(match.group(2))

    phase = rows.get("phase", "")
    folder_kind = rows.get("folder-kind", "")
    if not _PHASE.fullmatch(phase):
        raise ValueError(f"{phase_file}: current.phase is missing or invalid")
    if not _KIND.fullmatch(folder_kind):
        raise ValueError(f"{phase_file}: current.folder-kind is missing or invalid")
    return folder_kind


def validate_contract(contract: PhaseContract) -> list[str]:
    problems: list[str] = []
    text = contract.path.read_text(encoding="utf-8", errors="replace")
    rel = contract.path.as_posix()
    if not contract.name:
        problems.append(f"{rel}: missing frontmatter name")
    elif contract.name != contract.path.parent.name:
        problems.append(
            f"{rel}: name {contract.name!r} differs from folder {contract.path.parent.name!r}"
        )
    if not contract.workflow.endswith("-workflow"):
        problems.append(f"{rel}: workflow must name a *-workflow skill")
    if not _PHASE.fullmatch(contract.phase):
        problems.append(f"{rel}: phase {contract.phase!r} is not <LETTER><number>")
    if not _KIND.fullmatch(contract.folder_kind):
        problems.append(f"{rel}: folder_kind {contract.folder_kind!r} is not kebab-case")
    if contract.primary_face not in PRIMARY_FACES:
        problems.append(
            f"{rel}: primary_face must be page or task, got {contract.primary_face!r}"
        )
    if contract.page_ruling not in PAGE_RULINGS:
        problems.append(
            f"{rel}: page_ruling must be none, domain-gate, or local, "
            f"got {contract.page_ruling!r}"
        )
    if contract.legacy_page_type and not _KIND.fullmatch(contract.legacy_page_type):
        problems.append(
            f"{rel}: legacy_page_type {contract.legacy_page_type!r} is not kebab-case"
        )
    positions = []
    for heading in REQUIRED_SECTIONS:
        hits = list(re.finditer(rf"(?m)^## {re.escape(heading)}\s*$", text))
        if len(hits) != 1:
            problems.append(f"{rel}: requires exactly one `## {heading}` section")
        else:
            positions.append(hits[0].start())
    if len(positions) == len(REQUIRED_SECTIONS) and positions != sorted(positions):
        problems.append(f"{rel}: required sections are out of contract order")
    if contract.legacy_page_type and not re.search(r"(?m)^  outline:\s*$", _frontmatter(text)):
        problems.append(
            f"{rel}: legacy_page_type requires metadata.outline for plan-shape compatibility"
        )
    return problems


def validate_tree(skills_root: Path) -> tuple[list[PhaseContract], list[str]]:
    contracts = discover(skills_root)
    problems: list[str] = []
    for contract in contracts:
        problems.extend(validate_contract(contract))

    def duplicate(field: str, values: list[tuple[str, PhaseContract]]) -> None:
        seen: dict[str, PhaseContract] = {}
        for value, contract in values:
            if not value:
                continue
            prior = seen.get(value)
            if prior is not None:
                problems.append(
                    f"duplicate {field} {value!r}: {prior.path} and {contract.path}"
                )
            else:
                seen[value] = contract

    duplicate(
        "workflow phase",
        [(f"{item.workflow}:{item.phase}", item) for item in contracts],
    )
    duplicate("folder_kind", [(item.folder_kind, item) for item in contracts])
    duplicate(
        "legacy_page_type", [(item.legacy_page_type, item) for item in contracts]
    )
    return contracts, problems
