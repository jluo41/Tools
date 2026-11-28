"""A ready design Block for tests: run-add-job's gates met (a signed goal, an inputs version), placeholders only."""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import design_ladder as D  # noqa: E402


def ready(block: Path, n: int = 3, inputs: str = "i2", goals: list | None = None) -> Path:
    """Scaffold the Block, sign G01 (N = n) into board.md ## Goals and make inputs/<inputs>/; returns the Block."""
    D.main(["block", str(block), "--channel", "sms"])
    goals = goals or [{"id": "G01", "aim": "<the behaviour to change>", "who": "<audience>", "venue": "sms", "n": n,
                       "rules": [], "leave-out": "<what>", "signed": "✅ 261007"}]
    board = block / "board.md"
    board.write_text(board.read_text().replace("goals: []", yaml.safe_dump({"goals": goals}, allow_unicode=True)
                                               .rstrip("\n").replace("goals:\n", "goals:\n", 1)))
    rules = block / "design-goal.md"
    rules.write_text(rules.read_text().replace("signed: ''", "signed: ✅ 261007"))
    (block / "inputs" / inputs).mkdir(parents=True, exist_ok=True)
    return block
