"""Recognize a new Idea Job without relabeling a legacy Task portfolio."""

from pathlib import Path
import re

import yaml


def mapping(path: Path) -> dict:
    """Return only readable YAML mappings; callers report missing/invalid data."""
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError, yaml.YAMLError):
        return {}


# An Idea Block is a named Board in the Project's paper/ world, Idea-<Slug>/, beside Paper- and Grant- (JL 261124:
# "No more ideation theme"); an older bNN_<direction>/ Block still reads.
BLOCK_NAME = r"Idea-[A-Za-z0-9][A-Za-z0-9-]*|b\d{2,}_.+"


def block_key(name: str) -> str:
    """The Block's part of a Job address: the whole Idea-<Slug> name, or an older Block's bNN."""
    return name if name.startswith("Idea-") else name.split("_", 1)[0]


def is_idea_job(root: Path) -> bool:
    """A layout marker alone cannot bypass a legacy Paper projection gate."""
    root = root.resolve()
    manifest = mapping(root / "ideation.yaml")
    if (manifest.get("kind") != "ideation-unit"
            or manifest.get("layout") != "idea-job"
            or not re.fullmatch(r"j\d{2,}_.+", root.name)
            or not re.fullmatch(BLOCK_NAME, root.parent.name)):
        return False
    block_ref = manifest.get("block")
    if not isinstance(block_ref, str) or (root / block_ref).resolve() != root.parent / "ideation.yaml":
        return False
    block = mapping(root.parent / "ideation.yaml")
    rows = block.get("ideas")
    if block.get("kind") != "ideation-block" or block.get("version") != 1 or not isinstance(rows, list):
        return False
    matches = [row for row in rows if isinstance(row, dict)
               and row.get("job") == root.name]
    idea_id = manifest.get("idea_id")
    if (not isinstance(idea_id, str) or not re.fullmatch(r"i\d+", idea_id)
            or len(matches) != 1 or matches[0].get("idea_id") != idea_id
            or sum(isinstance(row, dict) and row.get("idea_id") == idea_id for row in rows) != 1):
        return False
    cards = [mapping(path) for path in (root / "cards").glob("i*.yaml")]
    return (len(cards) == 1 and cards[0].get("kind") == "idea-card"
            and cards[0].get("id") == idea_id
            and cards[0].get("canonical_id") == idea_id)
