"""Workflow gate checks for engine entry points (deterministic; no model calls).

A v2 job root (`config.yaml` with `schema_version: subjective-label/v2`) may not
send corpus text to a model, embed it, or sample it until the named gate passed.
Only G0 is implemented: the job has left P0 and its G0 receipt is valid, as
reported by `job.status`. Legacy v1 project dirs keep working with a warning.

Usage (from another engine module):
    from gates import GateHold, guard_job_root
    guard_job_root(project_dir, "G0")      # raises GateHold on a v2 job before G0
"""
from __future__ import annotations

import sys
from pathlib import Path

ENGINE_DIR = Path(__file__).resolve().parent
V2_SCHEMA = "subjective-label/v2"
_WARNED: set[str] = set()


class GateHold(RuntimeError):
    """The job has not passed the gate required for this operation."""


def is_v2_job_root(root: Path | None) -> bool:
    if root is None:
        return False
    cfg = Path(root) / "config.yaml"
    if not cfg.is_file():
        return False
    import yaml  # noqa: PLC0415
    try:
        data = yaml.safe_load(cfg.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as error:
        raise GateHold(f"HOLD · cannot read {cfg} to check its schema: "
                       f"{type(error).__name__}") from None
    return isinstance(data, dict) and data.get("schema_version") == V2_SCHEMA


def require_gate(job_root: Path, gate: str) -> None:
    """Raise GateHold unless `job_root` has passed `gate`. Only G0 is implemented."""
    if gate != "G0":
        raise GateHold(f"HOLD · gate {gate!r} has no engine check yet; refusing to proceed")
    if str(ENGINE_DIR) not in sys.path:
        sys.path.insert(0, str(ENGINE_DIR))
    from job import status  # noqa: PLC0415

    state = status(Path(job_root))
    phase = state.get("phase")
    if phase == "P0" or not state.get("g0_receipt_valid"):
        frontier = state.get("first_blocked_frontier") or "G0"
        raise GateHold(
            f"HOLD · {gate} not passed for {job_root} (phase {phase}, "
            f"g0_receipt_valid={bool(state.get('g0_receipt_valid'))}, blocked at {frontier}); "
            "no item was sent to a model, embedded, or sampled")


def guard_job_root(project_dir: Path | None, gate: str = "G0") -> bool:
    """Gate a v2 job root; warn once for a legacy dir. Returns True for a v2 job."""
    if is_v2_job_root(project_dir):
        require_gate(Path(project_dir), gate)
        return True
    key = str(Path(project_dir).resolve()) if project_dir is not None else "<none>"
    if key not in _WARNED:
        _WARNED.add(key)
        print(f"WARNING · legacy project dir (no schema_version {V2_SCHEMA}): {key}; "
              f"{gate} is not enforced", file=sys.stderr)
    return False
