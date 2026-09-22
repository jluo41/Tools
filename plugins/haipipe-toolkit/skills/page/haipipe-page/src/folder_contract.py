"""Discovery and structural validation for Folder owner contracts.

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
    "Workbenches",
    "Gate and Closure",
    "Handoff",
    "Files",
)
PRIMARY_FACES = {"page", "task"}
PAGE_RULINGS = {"none", "domain-gate", "local"}
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
class FolderContract:
    path: Path
    name: str
    workflow: str
    folder_kind: str
    primary_face: str
    page_ruling: str
    legacy_page_type: str = ""


def read_contract(path: Path) -> FolderContract | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    front = _frontmatter(text)
    workflow = _metadata_row(front, "workflow")
    if not workflow:
        return None
    return FolderContract(
        path=path,
        name=_top_row(front, "name"),
        workflow=workflow,
        folder_kind=_metadata_row(front, "folder_kind"),
        primary_face=_metadata_row(front, "primary_face"),
        page_ruling=_metadata_row(front, "page_ruling"),
        legacy_page_type=_metadata_row(front, "legacy_page_type"),
    )


def discover(skills_root: Path) -> list[FolderContract]:
    contracts: list[FolderContract] = []
    # Sibling families may use different paths; only owner metadata determines
    # resource semantics. A directory name creates no lifecycle.
    paths = set(skills_root.glob("*/folder-kinds/*/SKILL.md"))
    # Workflow controllers sit flat at their family root (no workflow-phases/ folder).
    paths.update(skills_root.glob("*/haipipe-*-inquiry/SKILL.md"))
    paths.update(skills_root.glob("*/haipipe-*-workflow/SKILL.md"))
    paths.update(skills_root.glob("*/haipipe-paper-*/SKILL.md"))
    for path in sorted(paths):
        if any(part.startswith("_") for part in path.relative_to(skills_root).parts):
            continue
        contract = read_contract(path)
        if contract is not None:
            contracts.append(contract)
    return contracts


def resolve(
    skills_root: Path, *, folder_kind: str = "", legacy_page_type: str = ""
) -> FolderContract | None:
    """Resolve one Folder owner, raising on an ambiguous declaration."""
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


def folder_identity_path(folder: Path) -> Path | None:
    """Select canonical identity, or the read-only legacy import fallback."""
    for name in ("folder.yaml", "phase.yaml"):
        candidate = Path(folder) / "workflow" / name
        if candidate.exists() or candidate.is_symlink():
            return candidate
    return None


def current_folder_kind(folder: Path) -> str:
    """Read resource identity from ``workflow/folder.yaml``.

    An absent file means the Folder has a fixed identity and may use its Page
    frontmatter. A present file is authoritative: malformed current state is a
    routing error, never permission to fall back to a stale Markdown key.
    Without a canonical file, import only folder-kind from the legacy file;
    its phase field and transition history have no execution semantics.
    """
    identity_file = folder_identity_path(folder)
    if identity_file is None:
        return ""
    try:
        import yaml
    except ImportError as exc:
        raise ValueError(f"{identity_file}: PyYAML is required to read Folder identity") from exc

    class IdentityLoader(yaml.SafeLoader):
        pass

    def unique_mapping(loader, node, deep=False):
        loader.flatten_mapping(node)
        mapping = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in mapping:
                raise ValueError(f"duplicate identity key {key!r}")
            mapping[key] = loader.construct_object(value_node, deep=deep)
        return mapping

    IdentityLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)
    try:
        record = yaml.load(identity_file.read_text(encoding="utf-8"), Loader=IdentityLoader)
    except (OSError, UnicodeError, yaml.YAMLError, ValueError, TypeError) as exc:
        raise ValueError(f"{identity_file}: invalid Folder identity: {exc}") from exc
    if not isinstance(record, dict) or not isinstance(record.get("current"), dict):
        raise ValueError(f"{identity_file}: missing top-level current mapping")
    folder_kind = record["current"].get("folder-kind")
    if not isinstance(folder_kind, str) or not _KIND.fullmatch(folder_kind):
        raise ValueError(f"{identity_file}: current.folder-kind is missing or invalid")
    return folder_kind


def resolved_folder_kind(folder: Path, *, declared: str = "", legacy: str = "") -> str:
    """Return resolved kind, '' when absent, or raise a visible routing error."""
    current = current_folder_kind(folder)
    if declared and not _KIND.fullmatch(declared):
        raise ValueError(f"{folder}: invalid Page frontmatter folder-kind {declared!r}")
    if current and declared and declared != current:
        raise ValueError(
            f"{folder_identity_path(folder)} current.folder-kind {current!r} "
            f"conflicts with Page frontmatter folder-kind {declared!r}"
        )
    return current or declared or legacy


def validate_contract(contract: FolderContract) -> list[str]:
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
    if "folder-kinds" in contract.path.parts and _metadata_row(_frontmatter(text), "phase"):
        problems.append(f"{rel}: current Folder owners must not declare metadata.phase")
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


def validate_tree(skills_root: Path) -> tuple[list[FolderContract], list[str]]:
    contracts = discover(skills_root)
    problems: list[str] = []
    for contract in contracts:
        problems.extend(validate_contract(contract))

    def duplicate(field: str, values: list[tuple[str, FolderContract]]) -> None:
        seen: dict[str, FolderContract] = {}
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

    duplicate("folder_kind", [(item.folder_kind, item) for item in contracts])
    duplicate(
        "legacy_page_type", [(item.legacy_page_type, item) for item in contracts]
    )
    return contracts, problems
