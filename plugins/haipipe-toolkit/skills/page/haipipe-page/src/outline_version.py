"""Outline plan version parsing and ordering.

Plans use ``v<generation>.<shape>[.<evidence>]``. The omitted evidence
component is zero, so ``v1.2`` and ``v1.2.0`` have the same meaning. Generation
zero is outline-only. From generation one onward, a released shape or evidence
change requires Content reconciliation through its gates; unapproved working
edits do not publish Content. Integer-only ``v5`` files remain readable legacy input;
no new current plan may use that form.
"""
import re
from pathlib import Path


VERSION_RE = re.compile(
    r"^v(?P<generation>\d+)(?:\.(?P<shape>\d+))?(?:\.(?P<evidence>\d+))?$"
)


PLAN_KINDS = ("outline", "draft")


def plan_dir(page_folder) -> Path:
    """The folder that holds a Page's plan: ``draft/`` since 0.118, else ``outline/``.

    A real ``draft/`` wins; an ``outline`` link that points at it is only kept
    for older readers.
    """
    page_folder = Path(page_folder)
    draft = page_folder / "draft"
    if draft.is_dir() and not draft.is_symlink():
        return draft
    return page_folder / "outline"


def version_tag(path: Path) -> str:
    """Return the filename's plan version tag (``-outline-`` or ``-draft-``), or ''."""
    match = re.search(r"-(?:outline|draft)-(v\d+(?:\.\d+){0,2})\.md$", Path(path).name)
    return match.group(1) if match else ""


def version_key(path: Path) -> tuple[int, int, int, int, int]:
    """Sort standard versions numerically while retaining legacy plans."""
    tag = version_tag(path)
    match = VERSION_RE.fullmatch(tag)
    if match:
        shape_text = match.group("shape")
        evidence_text = match.group("evidence")
        # Prefer an explicit shape component over an otherwise equal legacy
        # integer. An explicit evidence zero may coexist during migration and
        # sorts after its shorter semantic alias.
        return (
            2,
            int(match.group("generation")),
            int(shape_text or 0),
            int(evidence_text or 0),
            (1 if shape_text is not None else 0) + (1 if evidence_text is not None else 0),
        )

    # Legacy ``*-outline-v_0707.md`` files remain readable. Any standard
    # approved/revision lineage outranks this migration-only shape.
    legacy_tag = re.split(r"-(?:outline|draft)-", Path(path).stem)[-1]
    digits = re.sub(r"\D", "", legacy_tag)
    return (1, int(digits or 0), 0, 0, 0)


def version_policy_issues(path: Path, text: str) -> list[str]:
    """Return approval/version contract violations for one standard plan."""
    tag = version_tag(path)
    match = VERSION_RE.fullmatch(tag)
    if not match:
        return []

    generation = int(match.group("generation"))
    shape_text = match.group("shape")
    evidence_text = match.group("evidence")
    shape = int(shape_text) if shape_text is not None else None
    evidence = int(evidence_text or 0)
    approved = bool(re.search(r"(?m)^approved:\s*✅", text))
    issues = []

    if generation == 0:
        if shape is None or shape < 1:
            issues.append(f"{tag}: pre-content plans must use v0.<shape>[.<evidence>]")
        if approved:
            issues.append(f"{tag}: a v0 plan cannot be approved; promote the selected state to v1.0")
    elif shape is None:
        if not approved:
            issues.append(f"{tag}: an integer generation requires explicit channel approval")
    elif shape == 0 and evidence == 0:
        if not approved:
            issues.append(f"{tag}: a generation baseline requires explicit channel approval")
    elif evidence > 0:
        expected_base = f"v{generation}.{shape}"
        if not approved:
            issues.append(f"{tag}: an evidence revision must inherit the approved {expected_base} Shape")
        if not re.search(rf"(?m)^shape-base:\s*{re.escape(expected_base)}\s*$", text):
            issues.append(f"{tag}: evidence revision must declare shape-base: {expected_base}")
        if approved and not re.search(
            rf"(?m)^approved:\s*✅.*inherited from {re.escape(expected_base)}\b", text
        ):
            issues.append(f"{tag}: evidence revision approval must say inherited from {expected_base}")

    return issues


def legacy_integer_issue(path: Path) -> str:
    """Name the migration owed when the current plan is an integer-only ``vN`` file.

    A legacy chain ``v1 … vN`` renumbers one to one to ``v0.1 … v0.N``; no
    legacy tick mints ``v1.0`` (plan-grammar §6, JL 260905).
    """
    tag = version_tag(path)
    match = VERSION_RE.fullmatch(tag)
    if not match or match.group("shape") is not None:
        return ""
    major = int(match.group("generation"))
    return (
        f"{tag}: integer-only plan version is legacy; renumber the chain "
        f"v1…v{major} to v0.1…v0.{major} (no v1.0 until a person promotes one)"
    )


def latest_outline(outline_dir: Path, stem=None):
    """Return the newest standard or legacy outline plan in one folder."""
    outline_dir = Path(outline_dir)
    if not outline_dir.is_dir():
        return None
    plans = plan_files(outline_dir, stem)
    if not plans and (outline_dir / PREVIOUS).is_dir():
        # Only superseded versions left: the newest of them is still current.
        plans = plan_files(outline_dir / PREVIOUS, stem)
    return max(plans, key=version_key) if plans else None


def plan_files(folder: Path, stem=None) -> list[Path]:
    """Every plan version in one folder: `<stem>-outline-*.md` and `<stem>-draft-v*.md`."""
    prefix = stem or "*"
    return sorted(set(Path(folder).glob(f"{prefix}-outline-*.md"))
                  | set(Path(folder).glob(f"{prefix}-draft-v*.md")))


# Superseded Outline versions live in `outline/previous/`, so `outline/`
# holds exactly one plan: the current one. Every reader globs `outline/`
# only, and a named older version is still found under `previous/`.
PREVIOUS = "previous"


def retire_superseded(outline_dir: Path, stem=None) -> list[Path]:
    """Move every Outline version except the newest into `outline/previous/`.

    Returns the moved files' new paths. Never overwrites a file already in
    `previous/`; a name clash is left in place and reported by the caller.
    """
    outline_dir = Path(outline_dir)
    stems = {}
    for plan in plan_files(outline_dir, stem):
        stems.setdefault(re.split(r"-(?:outline|draft)-", plan.name)[0], []).append(plan)
    moved = []
    for plans in stems.values():
        newest = max(plans, key=version_key)
        for plan in sorted(plans, key=version_key):
            if plan == newest:
                continue
            target = outline_dir / PREVIOUS / plan.name
            if target.exists():
                continue
            target.parent.mkdir(exist_ok=True)
            plan.rename(target)
            moved.append(target)
    return moved


# The six process records sit in `outline/records/`, so `outline/` opens on the
# two authored files: the current plan and the Evidence Item contract.
RECORDS = "records"
RECORD_KINDS = ("context", "requirement", "discussion", "feedback", "files", "log")


def record_path(outline_dir: Path, stem: str, kind: str) -> Path:
    """Return `outline/records/<stem>-<kind>.md`, or the old flat file while it exists.

    New records are always created under `records/`; a caller that writes must
    create the parent folder.
    """
    outline_dir = Path(outline_dir)
    new = outline_dir / RECORDS / f"{stem}-{kind}.md"
    old = outline_dir / f"{stem}-{kind}.md"
    return old if old.is_file() and not new.is_file() else new


def retire_records(outline_dir: Path) -> list[Path]:
    """Move flat `<stem>-<kind>.md` process records into `outline/records/`."""
    outline_dir = Path(outline_dir)
    moved = []
    for kind in RECORD_KINDS:
        for old in sorted(outline_dir.glob(f"*-{kind}.md")):
            target = outline_dir / RECORDS / old.name
            if "-outline-" in old.name or target.exists():
                continue
            target.parent.mkdir(exist_ok=True)
            old.rename(target)
            moved.append(target)
    return moved


def find_version(outline_dir: Path, name: str) -> Path | None:
    """Return a named Outline version from `outline/` or `outline/previous/`."""
    for folder in (Path(outline_dir), Path(outline_dir) / PREVIOUS):
        if (folder / name).is_file():
            return folder / name
    return None
