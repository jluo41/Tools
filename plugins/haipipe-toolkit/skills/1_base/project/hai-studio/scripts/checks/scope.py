"""Select only named Studio scopes, never implicitly sweep the checkout."""
import json
import re
from pathlib import Path


def sources(topic: Path) -> tuple[Path, ...]:
    return (topic / f"{topic.name}.md", topic / "studio-views.json", topic / "elements.md",
            topic / "delivery", topic / "delivery/requirements")


def kind(topic: Path, data: dict | None = None, root: Path | None = None) -> str | None:
    if root is not None and any(not p.resolve().is_relative_to(root) for p in sources(topic)):
        return "invalid"  # Select it for an explicit error without reading outside the SPACE.
    face = topic / f"{topic.name}.md"
    if face.is_file() and re.search(r"\*\*Delivery type:\*\*\s*skill\b", face.read_text()):
        return "skills"
    if data is None:
        try:
            data = json.loads((topic / "studio-views.json").read_text())
        except (OSError, ValueError):
            data = {}
    if not isinstance(data, dict):
        return None
    if "-studio-type-" in topic.name and (
        (topic / 'delivery/requirements').is_dir()
        or str(data.get('check_type', '')).rstrip('/').endswith('/' + topic.name)
        or data.get('check_type') == topic.name.split('-studio-type-', 1)[-1]
    ):
        return "type"
    if data.get("check_type"):
        return "bound"
    views = data.get("views")
    if isinstance(views, list) and views:
        for view in views:
            if not isinstance(view, dict):
                return None
            items = view.get("items")
            if not isinstance(items, list) or not items or not isinstance(items[0], dict):
                return None
            if view.get("name") == "Evaluation" and "view=skill-eval" in str(items[0].get("url", "")):
                continue                                   # each skill measured live, after the skills
            if view.get("name") == "Draw" and str(items[0].get("path", "")).endswith(".excalidraw"):
                continue                                   # a Skills topic's own drawing, its last button
            if not str(items[0].get("path", "")).endswith("/SKILL.md"):
                return None
        return "skills"
    return None


def select(target: Path, root: Path) -> list[Path]:
    if not target.exists():
        raise ValueError("target does not exist")
    current = target if target.is_dir() else target.parent
    for parent in (current, *current.parents):
        if not parent.is_relative_to(root):
            break
        if re.match(r"s\d{2}-", parent.name):
            return [parent]
        if (parent / "board.md").is_file():
            if parent != current:
                return []  # An unrelated file inside a Block is not a Studio target.
            return [p for p in sorted(parent.glob("s[0-9][0-9]-*")) if p.is_dir()
                    and (not p.resolve().is_relative_to(parent.resolve()) or kind(p, root=root))]
    return []
