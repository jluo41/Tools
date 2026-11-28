"""Contained source paths and access to the existing Studio rule owners."""
from contextlib import contextmanager
from importlib import import_module
from pathlib import Path
import sys

SCRIPTS = Path(__file__).resolve().parents[1]                       # hai-studio/scripts, where these checks live
PLUGIN = next(p for p in SCRIPTS.parents if (p / ".claude-plugin").is_dir())
ROOT = PLUGIN.parents[1]


def contained(root: Path, value: str) -> Path:
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise ValueError("expected a nonempty SPACE-relative path")
    path = (root / value).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("path leaves the SPACE")
    return path


def owner(name: str):
    own = sorted(SCRIPTS.parent.glob("gallery/*/scripts"))             # each Studio Type's own scripts
    for folder in (SCRIPTS, *own, PLUGIN / "servers/_host"):
        if str(folder) not in sys.path:
            sys.path.insert(0, str(folder))
    return import_module(name)


@contextmanager
def using_root(module, root: Path):
    """Existing generators have a SPACE constant; checks run sequentially."""
    previous = module.SPACE
    module.SPACE = root
    try:
        yield module
    finally:
        module.SPACE = previous
