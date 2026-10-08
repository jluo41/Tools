"""Where the toolkit's skills sit, found by name rather than by depth.

Skills sit in three layers: ``skills/0_utils/<skill>``, ``skills/1_base/<family>/<skill>`` and
``skills/2_theme/<family>/<skill>`` (a family may nest one more level, e.g. ``task/1_data``).
Code finds the skills root by its folder name and a skill or family by its folder name, so
moving a family to another layer breaks no path.
"""
from __future__ import annotations

import functools
import re
from pathlib import Path

SKILLS = next(p for p in Path(__file__).resolve().parents if p.name == "skills")
TOOLKIT = SKILLS.parent
LAYERS = ("0_utils", "1_base", "2_theme")


@functools.lru_cache(maxsize=None)
def skill_dir(name: str) -> Path:
    """The folder named ``name`` under ``skills/``: a skill (``haipipe-page``) or a family
    (``design``), nearest first. Folders starting with ``.`` or ``_`` are skipped. When none
    exists ``skills/<name>`` is returned, so a missing skill fails where it is read."""
    level = [SKILLS]
    for _ in range(4):                     # layer / family / skill / sub-skill
        below = []
        for folder in level:
            try:
                children = sorted(folder.iterdir())
            except OSError:
                continue
            for child in children:
                if child.name.startswith((".", "_")) or not child.is_dir():
                    continue
                if child.name == name:
                    return child
                below.append(child)
        level = below
    return SKILLS / name


def in_skills(relative: str) -> Path:
    """A path written relative to ``skills/``, with or without its layer: ``paper/venue/x.md``
    (written before the layers) and ``2_theme/paper/venue/x.md`` both give the file."""
    path = SKILLS / relative
    if path.exists() or relative.split("/", 1)[0] in LAYERS:
        return path
    for layer in LAYERS:
        if (SKILLS / layer / relative).exists():
            return SKILLS / layer / relative
    return path


_WRITTEN = re.compile(r"(haipipe-toolkit/skills/)(?!(?:%s)/)([^/]+/)" % "|".join(LAYERS))


def relayer(value: str) -> str:
    """A ``…/haipipe-toolkit/skills/<family>/…`` path written before the layers, with its layer
    put back in when that family now sits in one; any other value is returned unchanged."""
    def put(match):
        family = match.group(2).rstrip("/")
        for layer in LAYERS:
            if (SKILLS / layer / family).is_dir():
                return f"{match.group(1)}{layer}/{match.group(2)}"
        return match.group(0)
    return _WRITTEN.sub(put, value)
