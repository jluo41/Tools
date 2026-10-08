"""Workflow gate checks for engine entry points (deterministic; no model calls).

A v2 job root (`config.yaml` with `schema_version: subjective-label/v2`) may not
send corpus text to a model, embed it, or sample it until the named gate passed.
Only G0 is implemented: the P0 contract integrity, human meaning receipt, and
G0 receipt predicates must all be valid, as reported by `job.status`. P0/P1
phase values are compatibility projections and never authorize an operation.
Missing, malformed, or unknown schemas fail closed before any such operation.

Usage (from another engine module):
    from gates import GateHold, guard_job_root
    guard_job_root(project_dir, "G0")      # raises GateHold unless schema and G0 pass
"""
from __future__ import annotations

import sys
from pathlib import Path

ENGINE_DIR = Path(__file__).resolve().parent
V2_SCHEMA = "subjective-label/v2"


class GateHold(RuntimeError):
    """The job has not passed the gate required for this operation."""


def is_v2_job_root(root: Path | None) -> bool:
    """Validate that a job root has the only currently supported schema.

    This intentionally raises for missing or unknown schemas instead of
    treating them as legacy: doing so would let a damaged v2 config bypass G0.
    """
    if root is None:
        raise GateHold(
            "HOLD · a job root is required to check its schema; "
            "no item was sent to a model, embedded, or sampled"
        )
    cfg = Path(root) / "config.yaml"
    if not cfg.is_file():
        raise GateHold(
            f"HOLD · missing job config {cfg}; no item was sent to a model, "
            "embedded, or sampled"
        )
    import yaml  # noqa: PLC0415
    try:
        data = yaml.safe_load(cfg.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise GateHold(f"HOLD · cannot read {cfg} to check its schema: "
                       f"{type(error).__name__}; no item was sent to a model, "
                       "embedded, or sampled") from None
    if not isinstance(data, dict):
        raise GateHold(
            f"HOLD · {cfg} must contain a YAML mapping with schema_version; "
            "no item was sent to a model, embedded, or sampled"
        )
    schema_version = data.get("schema_version")
    if schema_version != V2_SCHEMA:
        detail = "missing" if schema_version is None else repr(schema_version)
        raise GateHold(
            f"HOLD · unsupported schema_version {detail} in {cfg}; expected "
            f"{V2_SCHEMA!r}; no item was sent to a model, embedded, or sampled"
        )
    return True


def require_gate(job_root: Path, gate: str) -> None:
    """Raise GateHold unless `job_root` has passed `gate`. Only G0 is implemented."""
    if gate != "G0":
        raise GateHold(f"HOLD · gate {gate!r} has no engine check yet; refusing to proceed")
    if str(ENGINE_DIR) not in sys.path:
        sys.path.insert(0, str(ENGINE_DIR))
    from job import status  # noqa: PLC0415

    state = status(Path(job_root))
    g0_ready = bool(
        state.get("p0_contract_integrity_valid")
        and not state.get("hold")
        and state.get("meaning_receipt_valid")
        and state.get("g0_receipt_valid")
    )
    if g0_ready:
        return

    frontier = state.get("first_blocked_frontier") or "G0"
    if state.get("missing") or not state.get("p0_contract_integrity_valid"):
        raise GateHold(
            f"HOLD · {gate} blocked by P0 contract integrity for {job_root} "
            f"(blocked at {frontier}; errors={state.get('p0_integrity_errors') or state.get('missing')}); "
            "no item was sent to a model, embedded, or sampled"
        )
    if state.get("hold"):
        raise GateHold(
            f"HOLD · {gate} blocked by human-authority policy for {job_root}: "
            f"{state.get('hold_reason') or 'authority is not valid'}; "
            "no item was sent to a model, embedded, or sampled"
        )
    if not state.get("meaning_receipt_valid"):
        raise GateHold(
            f"{gate} pending · explicit caller attestation for the configured "
            f"human semantic authority is required for {job_root}; caller identity "
            "is not authenticated; no item was sent to a model, embedded, or sampled"
        )
    if not state.get("g0_receipt_valid"):
        raise GateHold(
            f"HOLD · {gate} receipt integrity is invalid for {job_root} "
            f"(blocked at {frontier}; errors={state.get('g0_integrity_errors')}); "
            "no item was sent to a model, embedded, or sampled"
        )
    raise GateHold(
        f"HOLD · {gate} predicates are incomplete for {job_root} "
        f"(blocked at {frontier}); no item was sent to a model, embedded, or sampled"
    )


def guard_job_root(project_dir: Path | None, gate: str = "G0") -> bool:
    """Require a supported schema and its gate before model, embed, or sample work."""
    is_v2_job_root(project_dir)
    require_gate(Path(project_dir), gate)
    return True
