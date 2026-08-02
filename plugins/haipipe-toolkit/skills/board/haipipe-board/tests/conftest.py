"""Make the engine folder importable from tests/ (JL 260801: the top level had
25 loose .py files, 11 of them tests).

Moving the suite down one folder broke two things, and this fixes the first:
`from src.parse import ...` and `from stage import ...` resolve against the
ENGINE dir, not against tests/. The second fix lives in each test file, where
`HERE` is re-pointed at the parent so `HERE / "serve.py"` still means the same
file it always did.
"""
import sys
from pathlib import Path

_ENGINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_ENGINE))
sys.path.insert(0, str(_ENGINE / "cli"))  # the runnable scripts moved here 260801
