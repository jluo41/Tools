"""Outline plan version parsing and ordering.

Current plans use an explicit frozen baseline (``v5.0``) and unapproved
working revisions (``v5.1``, ``v5.2``). Before a first approval, plans are
``v0.1``, ``v0.2``. A channel approval alone promotes the selected working
plan to the next frozen baseline (``v6.0``). Integer-only ``v5`` files remain
readable legacy input; no new current plan may use that form.
"""
import re
from pathlib import Path


VERSION_RE = re.compile(r"^v(?P<major>\d+)(?:\.(?P<minor>\d+))?$")


def version_tag(path: Path) -> str:
    """Return the filename's outline version tag, or an empty string."""
    match = re.search(r"-outline-(v\d+(?:\.\d+)?)\.md$", Path(path).name)
    return match.group(1) if match else ""


def version_key(path: Path) -> tuple[int, int, int, int]:
    """Sort standard versions numerically while retaining legacy plans."""
    tag = version_tag(path)
    match = VERSION_RE.fullmatch(tag)
    if match:
        # Prefer an explicit .0 baseline over an otherwise equal legacy vN.
        return (
            2,
            int(match.group("major")),
            int(match.group("minor") or 0),
            1 if match.group("minor") is not None else 0,
        )

    # Legacy ``*-outline-v_0707.md`` files remain readable. Any standard
    # approved/revision lineage outranks this migration-only shape.
    legacy_tag = Path(path).stem.split("-outline-")[-1]
    digits = re.sub(r"\D", "", legacy_tag)
    return (1, int(digits or 0), 0, 0)


def version_policy_issues(path: Path, text: str) -> list[str]:
    """Return approval/version contract violations for one standard plan."""
    tag = version_tag(path)
    match = VERSION_RE.fullmatch(tag)
    if not match:
        return []

    major = int(match.group("major"))
    minor_text = match.group("minor")
    minor = int(minor_text) if minor_text is not None else None
    approved = bool(re.search(r"(?m)^approved:\s*✅", text))
    issues = []

    if major == 0:
        if minor is None or minor < 1:
            issues.append(f"{tag}: pre-approval plans must use v0.<revision>")
        if approved:
            issues.append(f"{tag}: a pre-approval revision cannot be approved; promote it to v1.0")
    elif minor is None:
        if not approved:
            issues.append(f"{tag}: an integer major requires explicit channel approval")
    elif minor == 0:
        if not approved:
            issues.append(f"{tag}: a frozen .0 baseline requires explicit channel approval")
    elif approved:
        issues.append(
            f"{tag}: a working minor cannot be approved; promote it to v{major + 1}.0"
        )

    return issues


def legacy_integer_issue(path: Path) -> str:
    """Name the migration owed when the current plan is an integer-only ``vN`` file.

    A legacy chain ``v1 … vN`` renumbers one to one to ``v0.1 … v0.N``; no
    legacy tick mints ``v1.0`` (plan-grammar §6, JL 260905).
    """
    tag = version_tag(path)
    match = VERSION_RE.fullmatch(tag)
    if not match or match.group("minor") is not None:
        return ""
    major = int(match.group("major"))
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
