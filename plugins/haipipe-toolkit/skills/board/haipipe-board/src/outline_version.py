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


def version_tag(path: Path) -> str:
    """Return the filename's outline version tag, or an empty string."""
    match = re.search(r"-outline-(v\d+(?:\.\d+){0,2})\.md$", Path(path).name)
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
    legacy_tag = Path(path).stem.split("-outline-")[-1]
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
    pattern = f"{stem}-outline-*.md" if stem else "*-outline-*.md"
    plans = list(outline_dir.glob(pattern))
    return max(plans, key=version_key) if plans else None
