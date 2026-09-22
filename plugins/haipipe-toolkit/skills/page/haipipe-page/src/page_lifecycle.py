"""Deterministic audit of one Page lifecycle Workflow receipt."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


# The Page lifecycle is its Run list: context → structure ⇄ evidence → writing →
# check. Receipts written before 2026-09-22 carry uppercase tokens (CONTEXT,
# OUTLINE, PROBE, DRAFT, REVISE, COMPILE, CONTENT, CHECK); `run_token()` maps them
# so immutable historical receipts stay auditable. Steps keep their names.
LEGACY_RUN = {
    "CONTEXT": "context", "OUTLINE": "structure", "PROBE": "evidence",
    "EVIDENCE": "evidence", "DRAFT": "writing", "REVISE": "writing",
    "COMPILE": "writing", "CONTENT": "writing", "CHECK": "check",
}
RUNS = {"context", "structure", "evidence", "writing", "check"}
TERMINAL_ROUTES = {"CLOSE", "HOLD"}
CURRENT_RUN_CYCLES = {
    "context": {"PREPARE"},
    "structure": {"SHAPE", "SURVEY"},
    "evidence": {"LAND", "EMBED"},
    "writing": {"WRITE"},
    "check": {"CHECK"},
}
PAGE_RULINGS = {"none", "domain-gate", "local", "legacy-default"}
# Legal routes by Run key. Historical DRAFT/REVISE/COMPILE receipts normalise to
# `writing`, whose row is the union of their old edges, so they still audit.
LEGAL_ROUTES = {
    "context": {"context", "structure", "HOLD"},
    "structure": {"context", "structure", "evidence", "writing", "HOLD"},
    "evidence": {"context", "evidence", "structure", "writing", "HOLD"},
    "writing": {"context", "writing", "structure", "evidence", "check", "HOLD"},
    "check": {"CLOSE", "context", "structure", "evidence", "writing", "HOLD"},
}


def run_token(value: Any) -> Any:
    """Normalize one Run or route token: legacy uppercase words map to Run keys,
    CLOSE/HOLD stay uppercase, anything else lowercases and audits as unknown."""
    if isinstance(value, str):
        raw = value.strip()
        if raw.upper() in TERMINAL_ROUTES:
            return raw.upper()
        if raw.lower() in RUNS:
            return raw.lower()
        return LEGACY_RUN.get(raw.upper(), raw.lower())
    return value


def _raw(value: Any) -> str:
    """The receipt's own token, uppercased and untranslated, for DRAFT-era rules."""
    return str(value or "").strip().upper()


def receipt_run(receipt: dict) -> Any:
    """The receipt's Run: `run` (current) or `phase` (receipts before 2026-09-22)."""
    return receipt.get("run", receipt.get("phase", ""))


def _legacy_probe(receipts: list[Any]) -> bool:
    """Detect the short-lived PROBE-as-EVIDENCE receipt shape."""
    return any(
        isinstance(r, dict)
        and str(receipt_run(r)).strip().upper() == "PROBE"
        and str(r.get("route", "")).strip().upper() == "REVISE"
        for r in receipts
    )


def _trace_token(value: Any, legacy_probe: bool = False) -> Any:
    token = run_token(value)
    return "evidence" if legacy_probe and str(token).upper() == "PROBE" else token


SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class Finding:
    code: str
    where: str
    message: str


def _finding(code: str, index: int | str, message: str) -> Finding:
    where = f"receipt[{index}]" if isinstance(index, int) else index
    return Finding(code=code, where=where, message=message)


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _gate(receipt: dict[str, Any]) -> dict[str, Any]:
    value = receipt.get("human_gate")
    return value if isinstance(value, dict) else {}


def _version_parts(value: str) -> tuple[str, str] | None:
    parts = value.split(":")
    if len(parts) != 2 or not all(SHA256_RE.fullmatch(part) for part in parts):
        return None
    return parts[0], parts[1]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def audit_artifacts(run: dict[str, Any], base_dir: Path | None = None) -> list[Finding]:
    """Recompute the final Page identity from source and rendered files."""

    board_raw = str(run.get("board", "")).strip()
    page_raw = str(run.get("page", "")).strip()
    if not board_raw or not page_raw:
        return [
            _finding(
                "missing-artifact-context",
                "run",
                "board and page are required for independent artifact verification",
            )
        ]

    base = (base_dir or Path.cwd()).resolve()
    board = Path(board_raw).expanduser()
    if not board.is_absolute():
        board = base / board
    board = board.resolve()
    page = Path(page_raw).expanduser()
    if not page.is_absolute():
        page = board / page
    page = page.resolve()

    findings: list[Finding] = []
    try:
        page.relative_to(board)
    except ValueError:
        return [
            _finding(
                "page-outside-board",
                "run",
                f"page {page} is outside board {board}",
            )
        ]
    if not page.is_file():
        # A recorded path that no longer resolves is usually a MOVED page, not a
        # missing one: run 260805-0216-QB8e stored an ABSOLUTE path and the
        # 260816 regroup added a `<N>-` prefix to every group folder, so a page
        # that had not changed at all audited as "source does not exist". Fall
        # back to the file name under `board`, and REPORT the fallback: the
        # receipt is still defective, and saying so precisely beats saying
        # something false. A fallback is refused when it is not unique, because
        # guessing between two candidates is worse than stopping.
        candidates = sorted(board.rglob(page.name))
        candidates = [c for c in candidates if c.is_file() and "/board/" not in c.as_posix()]
        if len(candidates) != 1:
            return [
                _finding(
                    "source-artifact-missing",
                    "run",
                    f"Page source does not exist: {page}"
                    + (
                        f"; {len(candidates)} files named {page.name} under the board, so no unique fallback"
                        if candidates
                        else ""
                    ),
                )
            ]
        resolved = candidates[0]
        findings.append(
            _finding(
                "page-path-stale",
                "run",
                f"`page` records {page_raw} which does not resolve; the same file name "
                f"resolves uniquely to {resolved.relative_to(board).as_posix()}. Audited "
                f"against that. Store `page` BOARD-RELATIVE so a group rename cannot "
                f"break a receipt for a page that did not change.",
            )
        )
        page = resolved

    rendered_root = board / "board"
    rendered = sorted(rendered_root.rglob(f"{page.stem}.html")) if rendered_root.is_dir() else []
    if not rendered:
        return [
            _finding(
                "render-artifact-missing",
                "run",
                f"rendered HTML for {page.name} does not exist under {rendered_root}",
            )
        ]
    if len(rendered) > 1:
        return [
            _finding(
                "render-artifact-ambiguous",
                "run",
                f"multiple rendered HTML files match {page.stem}: "
                + ", ".join(str(path) for path in rendered),
            )
        ]

    actual = f"{_sha256(page)}:{_sha256(rendered[0])}"
    declared = str(run.get("final_version", "")).strip()
    if actual != declared:
        findings.append(
            _finding(
                "artifact-version-mismatch",
                "run",
                f"current source/render identity {actual} differs from final_version {declared}",
            )
        )
    return findings


def audit_run(run: dict[str, Any]) -> list[Finding]:
    """Return every process violation in a serialized Page RUN."""

    findings: list[Finding] = []
    packet = run.get("packet")
    if not isinstance(packet, dict):
        packet = {}
        findings.append(
            _finding("missing-packet", "run", "the original raw-material packet is required")
        )
    else:
        for field in ("run_id", "board", "page", "start_run", "intent"):
            value = packet.get(field, "") if field != "start_run" else (packet.get("start_run") or packet.get("start_phase", ""))
            if not str(value).strip():
                findings.append(
                    _finding("missing-packet-field", "run", f"packet.{field} is required")
                )
        for field in ("run_id", "board", "page"):
            if str(packet.get(field, "")).strip() != str(run.get(field, "")).strip():
                findings.append(
                    _finding(
                        "packet-run-mismatch",
                        "run",
                        f"packet.{field} must equal run.{field}",
                    )
                )
        packet_runtime_id = str(packet.get("workflow_runtime_id", "")).strip()
        run_runtime_id = str(run.get("workflow_runtime_id", "")).strip()
        if packet_runtime_id and packet_runtime_id != str(packet.get("run_id", "")).strip():
            findings.append(
                _finding(
                    "runtime-run-mismatch",
                    "run",
                    "packet.workflow_runtime_id must equal packet.run_id",
                )
            )
        if packet_runtime_id and "workflow_runtime_id" in run and packet_runtime_id != run_runtime_id:
            findings.append(
                _finding(
                    "packet-runtime-mismatch",
                    "run",
                    "packet.workflow_runtime_id must equal run.workflow_runtime_id",
                )
            )
        for field in ("sources", "constraints"):
            if field in packet and not isinstance(packet.get(field), list):
                findings.append(
                    _finding("invalid-packet-field", "run", f"packet.{field} must be a list")
                )

    receipts = run.get("receipts")
    if not isinstance(receipts, list) or not receipts:
        findings.append(
            _finding("missing-receipts", "run", "receipts must be a non-empty list")
        )
        return findings
    legacy_probe = _legacy_probe(receipts)

    limits = run.get("limits") if isinstance(run.get("limits"), dict) else {}
    max_steps = limits.get("max_steps")
    max_rounds = limits.get("max_rounds")
    for field, value in (("max_steps", max_steps), ("max_rounds", max_rounds)):
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            findings.append(
                _finding("invalid-limit", "run", f"limits.{field} must be a positive integer")
            )
    if isinstance(max_steps, int) and max_steps > 0 and len(receipts) > max_steps:
        findings.append(
            _finding(
                "max-steps-exceeded",
                "run",
                f"{len(receipts)} receipts exceed max_steps={max_steps}",
            )
        )
    packet_limits = packet.get("limits") if isinstance(packet.get("limits"), dict) else {}
    for field in ("max_steps", "max_rounds"):
        if field in packet_limits and packet_limits.get(field) != limits.get(field):
            findings.append(
                _finding(
                    "packet-limit-mismatch",
                    "run",
                    f"packet.limits.{field} must equal limits.{field}",
                )
            )

    start_run = _trace_token(str(packet.get("start_run") or packet.get("start_phase", "")), legacy_probe)
    if start_run and start_run not in RUNS:
        findings.append(
            _finding("unknown-start-run", "run", f"unknown packet start_run {start_run}")
        )
    if start_run and isinstance(receipts[0], dict):
        first_run = _trace_token(str(receipt_run(receipts[0])), legacy_probe)
        if first_run != start_run:
            findings.append(
                _finding(
                    "start-run-mismatch",
                    0,
                    f"packet start_run {start_run} does not match first Run {first_run}",
                )
            )
    packet_gate = packet.get("human_gate")
    declared_gate_required = (
        packet_gate.get("required") is True if isinstance(packet_gate, dict) else False
    )
    page_ruling_value = packet.get("page_ruling", "legacy-default")
    page_ruling = (
        page_ruling_value.strip().lower()
        if isinstance(page_ruling_value, str)
        else ""
    )
    if page_ruling not in PAGE_RULINGS:
        findings.append(
            _finding(
                "unknown-page-ruling",
                "run",
                "packet.page_ruling must be none, domain-gate, local, or "
                "legacy-default for an older packet",
            )
        )
    elif page_ruling in {"domain-gate", "local"} and not declared_gate_required:
        findings.append(
            _finding(
                "owner-gate-not-required",
                "run",
                f"packet.page_ruling={page_ruling} requires human_gate.required=true",
            )
        )

    producers: dict[str, str] = {}
    previous: dict[str, Any] | None = None

    for index, raw in enumerate(receipts):
        if not isinstance(raw, dict):
            findings.append(_finding("receipt-not-object", index, "receipt must be an object"))
            continue
        receipt = raw
        step_run = _trace_token(str(receipt_run(receipt)), legacy_probe)
        route = _trace_token(str(receipt.get("route", "")), legacy_probe)
        cycle = str(receipt.get("cycle", "")).strip().upper()
        next_cycle = str(receipt.get("next_cycle", "")).strip().upper()
        role = str(receipt.get("role", "")).lower()
        status = str(receipt.get("status", "")).lower()
        actor = str(receipt.get("actor", "")).strip()
        builder = str(receipt.get("builder_actor", "")).strip()
        before = str(receipt.get("version_before", "")).strip()
        after = str(receipt.get("version_after", "")).strip()
        checked = str(receipt.get("checked_version", "")).strip()
        source_sha256 = str(receipt.get("source_sha256", "")).strip()
        render_sha256 = str(receipt.get("render_sha256", "")).strip()
        reopens = receipt.get("reopens_promise") is True

        if receipt.get("step") != index + 1:
            findings.append(
                _finding("step-sequence", index, f"step must be {index + 1}")
            )
        if step_run not in RUNS:
            findings.append(_finding("unknown-run", index, f"unknown Run {step_run!r}"))
        elif route not in LEGAL_ROUTES[step_run]:
            findings.append(
                _finding("illegal-route", index, f"{step_run} cannot route to {route or '<missing>'}")
            )
        if step_run == "evidence" and route == "writing" and cycle != "EMBED":
            findings.append(_finding(
                "evidence-writing-without-embed", index,
                "Only the evidence Run's EMBED step may hand an approved evidence fold to writing",
            ))
        if route in TERMINAL_ROUTES and "next_cycle" in receipt:
            findings.append(
                _finding(
                    "terminal-next-cycle",
                    index,
                    f"{route} must omit next_cycle, not serialize an empty or stale value",
                )
            )
        elif next_cycle:
            allowed_cycles = CURRENT_RUN_CYCLES.get(route, set())
            if allowed_cycles and next_cycle not in allowed_cycles:
                findings.append(
                    _finding(
                        "route-cycle-mismatch",
                        index,
                        f"route {route} requires next_cycle in {sorted(allowed_cycles)}, got {next_cycle}",
                    )
                )
        if cycle:
            run_cycles = CURRENT_RUN_CYCLES.get(step_run, set())
            if run_cycles and cycle not in run_cycles:
                findings.append(
                    _finding(
                        "run-cycle-mismatch",
                        index,
                        f"Run {step_run} requires cycle in {sorted(run_cycles)}, got {cycle}",
                    )
                )
            if route not in TERMINAL_ROUTES and not next_cycle:
                findings.append(
                    _finding(
                        "missing-next-cycle",
                        index,
                        f"current {step_run}/{cycle} receipt routing to {route} requires next_cycle",
                    )
                )
        if not actor:
            findings.append(_finding("missing-actor", index, "actor identity is required"))
        if not builder:
            findings.append(
                _finding("missing-builder-actor", index, "builder actor identity is required")
            )
        if not before or not after:
            findings.append(
                _finding("missing-version", index, "version_before and version_after are required")
            )
        else:
            if _version_parts(before) is None:
                findings.append(
                    _finding(
                        "invalid-version-format",
                        index,
                        "version_before must be <source_sha256>:<render_sha256>",
                    )
                )
            after_parts = _version_parts(after)
            if after_parts is None:
                findings.append(
                    _finding(
                        "invalid-version-format",
                        index,
                        "version_after must be <source_sha256>:<render_sha256>",
                    )
                )
            elif after_parts != (source_sha256, render_sha256):
                findings.append(
                    _finding(
                        "snapshot-version-mismatch",
                        index,
                        "version_after must equal source_sha256:render_sha256",
                    )
                )
        for field in ("mechanical_errors", "mechanical_warnings"):
            value = receipt.get(field)
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                findings.append(
                    _finding(
                        "invalid-mechanical-count",
                        index,
                        f"{field} must be a non-negative integer",
                    )
                )
        if not str(receipt.get("reason", "")).strip():
            findings.append(_finding("missing-reason", index, "route reason is required"))
        if not isinstance(receipt.get("evidence"), list):
            findings.append(_finding("missing-evidence-list", index, "evidence must be a list"))
        if not isinstance(receipt.get("artifacts"), list):
            findings.append(_finding("missing-artifacts-list", index, "artifacts must be a list"))

        if status in {"blocked", "failed"} and route != "HOLD":
            findings.append(
                _finding("failed-work-not-held", index, f"status {status} must route to HOLD")
            )

        if step_run == "check":
            if role not in {"judge", "controller"}:
                findings.append(
                    _finding("check-role", index, "CHECK must be performed by a judge")
                )
            if role == "controller" and not (status in {"blocked", "failed"} and route == "HOLD"):
                findings.append(
                    _finding(
                        "controller-judged",
                        index,
                        "a controller may record CHECK failure but may not judge or close",
                    )
                )
            if not checked or before != after or checked != before:
                findings.append(
                    _finding(
                        "checked-version-mismatch",
                        index,
                        "CHECK must leave one identical "
                        "version_before/version_after/checked_version",
                    )
                )
            elif _version_parts(checked) is None:
                findings.append(
                    _finding(
                        "invalid-version-format",
                        index,
                        "checked_version must be <source_sha256>:<render_sha256>",
                    )
                )
            if role == "judge" and actor and builder and actor == builder:
                findings.append(
                    _finding(
                        "judge-is-builder",
                        index,
                        f"{actor} built and judged version {checked or after}",
                    )
                )
            producer = producers.get(checked)
            if role == "judge" and producer and producer == actor:
                findings.append(
                    _finding(
                        "self-approval",
                        index,
                        f"{actor} produced and judged version {checked}",
                    )
                )
            verdict = str(receipt.get("verdict", "")).lower()
            if route == "CLOSE" and verdict != "pass":
                findings.append(
                    _finding("close-without-pass", index, "CLOSE requires verdict=pass")
                )
            if route == "CLOSE" and receipt.get("mechanical_errors") != 0:
                findings.append(
                    _finding(
                        "close-with-mechanical-errors",
                        index,
                        "CLOSE requires mechanical_errors=0",
                    )
                )
            if verdict == "pass" and route not in {"CLOSE", "HOLD"}:
                findings.append(
                    _finding(
                        "pass-routed-to-work",
                        index,
                        "a pass may only CLOSE or HOLD for a gate",
                    )
                )
            if verdict == "revise" and route not in {"context", "structure", "evidence", "writing"}:
                findings.append(
                    _finding(
                        "revise-without-worker",
                        index,
                        "verdict=revise must name a producing Run",
                    )
                )
            if verdict == "blocked" and route != "HOLD":
                findings.append(
                    _finding("blocked-not-held", index, "verdict=blocked must route to HOLD")
                )
        else:
            if role != "producer":
                findings.append(
                    _finding("producer-role", index, f"{step_run} must be performed by a producer")
                )
            if route == "CLOSE":
                findings.append(_finding("producer-closed", index, "only CHECK may CLOSE"))
            if actor and builder and actor == builder:
                findings.append(
                    _finding(
                        "producer-is-builder",
                        index,
                        f"{actor} both produced and built version {after}",
                    )
                )
            if actor and after and status == "ok" and after != before:
                producers[after] = actor

        gate = _gate(receipt)
        if (gate.get("required") is True) != declared_gate_required:
            findings.append(
                _finding(
                    "human-gate-contract-mismatch",
                    index,
                    "receipt human_gate.required must match the raw-material packet",
                )
            )
        if route == "CLOSE" and gate.get("required") is True:
            if gate.get("status") != "passed" or not _list(gate.get("evidence")):
                findings.append(
                    _finding(
                        "human-gate-fabricated",
                        index,
                        "required human gate needs status=passed and durable evidence",
                    )
                )

        if reopens and _raw(receipt.get("route")) != "DRAFT":
            findings.append(
                _finding("reopen-without-draft", index, "reopens_promise requires route=DRAFT")
            )
        if _raw(receipt_run(receipt)) not in {"DRAFT", "OUTLINE"} and _raw(receipt.get("route")) == "DRAFT" and not reopens:
            findings.append(
                _finding(
                    "draft-without-reopen",
                    index,
                    "a non-DRAFT run may route to DRAFT only when purpose or Aims reopen",
                )
            )

        if previous is not None:
            previous_route = _trace_token(str(previous.get("route", "")), legacy_probe)
            previous_run = _trace_token(str(receipt_run(previous)), legacy_probe)
            # Compatibility only: old planning/evidence receipts represented
            # an open-gate HOLD as an in-run pause. Current receipts carry a
            # cycle and the controller always returns on HOLD, so only the
            # pre-cycle shape retains this historical audit exception.
            legacy_prepare_pause = (
                previous_route == "HOLD"
                and previous_run in {"context", "structure", "evidence"}
                and declared_gate_required
                and str(_gate(previous).get("status", "")) in {"pending", "waiting"}
                and "cycle" not in previous
                and "next_cycle" not in previous
            )
            if previous_route in TERMINAL_ROUTES and not legacy_prepare_pause:
                findings.append(
                    _finding("receipt-after-terminal", index, f"receipt follows {previous_route}")
                )
            elif legacy_prepare_pause:
                # A cold CHECK is legal on ANY version, pauses included: the
                # judge reads and routes, it does not produce (found by the
                # first real check-agent dispatch, 260819 step 14).
                if step_run != "check" and step_run not in LEGAL_ROUTES.get(previous_run, set()):
                    findings.append(
                        _finding(
                            "route-run-mismatch",
                            index,
                            f"paused at {previous_run}; Run {step_run} is not legal from it",
                        )
                    )
            elif step_run != previous_route:
                findings.append(
                    _finding(
                        "route-run-mismatch",
                        index,
                        f"previous route {previous_route} requires next run "
                        f"{previous_route}, got {step_run}",
                    )
                )

            previous_after = str(previous.get("version_after", "")).strip()
            if before != previous_after:
                findings.append(
                    _finding(
                        "version-continuity",
                        index,
                        "version_before must equal the preceding receipt's version_after",
                    )
                )

            previous_round = previous.get("round")
            current_round = receipt.get("round")
            should_increment = (
                _raw(previous.get("route")) == "DRAFT"
                and _raw(receipt_run(previous)) not in {"DRAFT", "OUTLINE"}
                and previous.get("reopens_promise") is True
            )
            expected_round = (
                previous_round + 1
                if isinstance(previous_round, int) and should_increment
                else previous_round
            )
            if current_round != expected_round:
                findings.append(
                    _finding(
                        "round-sequence",
                        index,
                        f"round must be {expected_round!r} after the previous route",
                    )
                )
        elif not isinstance(receipt.get("round"), int) or receipt.get("round") < 1:
            findings.append(
                _finding("round-start", index, "first round must be a positive integer")
            )

        current_round = receipt.get("round")
        if (
            isinstance(max_rounds, int)
            and max_rounds > 0
            and isinstance(current_round, int)
            and current_round > max_rounds
        ):
            findings.append(
                _finding(
                    "max-rounds-exceeded",
                    index,
                    f"round {current_round} exceeds max_rounds={max_rounds}",
                )
            )

        previous = receipt

    final = receipts[-1] if isinstance(receipts[-1], dict) else {}
    final_route = _trace_token(str(final.get("route", "")), legacy_probe)
    if final_route not in TERMINAL_ROUTES:
        findings.append(
            _finding("trace-not-terminal", "run", "final receipt must route to CLOSE or HOLD")
        )
    final_version = str(run.get("final_version", "")).strip()
    if not final_version:
        findings.append(_finding("missing-final-version", "run", "final_version is required"))
    elif _version_parts(final_version) is None:
        findings.append(
            _finding(
                "invalid-final-version-format",
                "run",
                "final_version must be <source_sha256>:<render_sha256>",
            )
        )
    if final_route == "CLOSE" and final_version:
        checked = str(final.get("checked_version", "")).strip()
        if final_version != checked:
            findings.append(
                _finding(
                    "changed-after-check",
                    "run",
                    "final_version differs from the version approved by terminal CHECK",
                )
            )

    run_status = str(run.get("status", "")).lower()
    if final_route == "CLOSE" and run_status and run_status != "closed":
        findings.append(_finding("status-route-mismatch", "run", "CLOSE requires status=closed"))
    if final_route == "HOLD" and run_status == "closed":
        findings.append(
            _finding("status-route-mismatch", "run", "HOLD cannot report status=closed")
        )

    return findings


def traversed_edges(receipts: Iterable[dict[str, Any]]) -> list[str]:
    """Return run-to-route edges in execution order for audit summaries."""
    receipts = list(receipts)
    legacy_probe = _legacy_probe(receipts)
    return [
        f"{_trace_token(str(receipt_run(r)), legacy_probe)}->"
        f"{_trace_token(str(r.get('route', '')), legacy_probe)}"
        for r in receipts
    ]
