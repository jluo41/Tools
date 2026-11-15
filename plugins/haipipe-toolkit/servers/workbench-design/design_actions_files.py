"""The refusal and the file helpers every Design action writes with: ActionError, the UTC clock, YAML dump and
load, a path reference and a slug (split out of design_actions.py)."""
from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

import yaml


class ActionError(ValueError):
    """A refused action; the message is shown to the person unchanged."""


# ------------------------------------------------------------------ files --

def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _dump(path: Path, obj) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(obj, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return path


def _load(path: Path) -> dict:
    if not path.is_file():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _ref(folder: Path, path: Path) -> dict:
    rel = path.resolve().relative_to(folder.resolve()) if folder.resolve() in path.resolve().parents \
        else Path(_relative(folder, path))
    return {"path": rel.as_posix()}  # a path, never a content hash


def _relative(folder: Path, path: Path) -> str:
    import os
    return os.path.relpath(path.resolve(), folder.resolve())


def _slug(text: str) -> str:
    slug = re.sub(r"[^a-z0-9_-]+", "-", text.lower()).strip("-_")
    return slug or "item"
