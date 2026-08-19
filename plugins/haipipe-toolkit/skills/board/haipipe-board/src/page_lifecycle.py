"""Deterministic audit of one Page lifecycle Workflow receipt."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


# PROBE is a live phase again: it raises and dispatches the card, while
# EVIDENCE lands what comes back. Receipts written during the short 260816
# rename used `phase: PROBE` for the widened EVIDENCE phase; `_legacy_probe`
# below recognizes that old shape (PROBE → REVISE) without sacrificing the new
# phase for current runs.
PHASE_ALIASES = {}
PHASES = {"OUTLINE", "DRAFT", "PROBE", "EVIDENCE", "REVISE", "COMPILE", "CHECK"}
TERMINAL_ROUTES = {"CLOSE", "HOLD"}
LEGAL_ROUTES = {
    "OUTLINE": {"OUTLINE", "DRAFT", "HOLD"},
    "DRAFT": {"DRAFT", "PROBE", "EVIDENCE", "REVISE", "CHECK", "HOLD"},
    "PROBE": {"PROBE", "EVIDENCE", "REVISE", "HOLD"},
    "EVIDENCE": {"EVIDENCE", "REVISE", "DRAFT", "CHECK", "HOLD"},
    "REVISE": {"REVISE", "COMPILE", "EVIDENCE", "DRAFT", "CHECK", "HOLD"},
    "COMPILE": {"COMPILE", "CHECK", "REVISE", "HOLD"},
    "CHECK": {"CLOSE", "OUTLINE", "REVISE", "PROBE", "EVIDENCE", "DRAFT", "HOLD"},
}


def phase_token(value: Any) -> Any:
    """Normalize one phase or route token without collapsing live PROBE."""
    if isinstance(value, str):
        return PHASE_ALIASES.get(value.strip().upper(), value.strip().upper())
    return value


def _legacy_probe(receipts: list[Any]) -> bool:
    """Detect the short-lived PROBE-as-EVIDENCE receipt shape."""
    return any(
        isinstance(r, dict)
        and str(r.get("phase", "")).strip().upper() == "PROBE"
        and str(r.get("route", "")).strip().upper() == "REVISE"
        for r in receipts
    )


def _trace_token(value: Any, legacy_probe: bool = False) -> Any:
    token = phase_token(value)
    return "EVIDENCE" if legacy_probe and token == "PROBE" else token


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
        for field in ("run_id", "board", "page", "start_phase", "intent"):
            if not str(packet.get(field, "")).strip():
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

    start_phase = _trace_token(str(packet.get("start_phase", "")), legacy_probe)
    if start_phase and start_phase not in PHASES:
        findings.append(
            _finding("unknown-start-phase", "run", f"unknown packet start_phase {start_phase}")
        )
    if start_phase and isinstance(receipts[0], dict):
        first_phase = _trace_token(str(receipts[0].get("phase", "")), legacy_probe)
        if first_phase != start_phase:
            findings.append(
                _finding(
                    "start-phase-mismatch",
                    0,
                    f"packet start_phase {start_phase} does not match first phase {first_phase}",
                )
            )
    packet_gate = packet.get("human_gate")
    declared_gate_required = (
        packet_gate.get("required") is True if isinstance(packet_gate, dict) else False
    )

    producers: dict[str, str] = {}
    previous: dict[str, Any] | None = None

    for index, raw in enumerate(receipts):
        if not isinstance(raw, dict):
            findings.append(_finding("receipt-not-object", index, "receipt must be an object"))
            continue
        receipt = raw
        phase = _trace_token(str(receipt.get("phase", "")), legacy_probe)
        route = _trace_token(str(receipt.get("route", "")), legacy_probe)
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
        if phase not in PHASES:
            findings.append(_finding("unknown-phase", index, f"unknown phase {phase!r}"))
        elif route not in LEGAL_ROUTES[phase]:
            findings.append(
                _finding("illegal-route", index, f"{phase} cannot route to {route or '<missing>'}")
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

        if phase == "CHECK":
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
            if verdict == "revise" and route not in {
                "OUTLINE", "DRAFT", "PROBE", "EVIDENCE", "REVISE", "COMPILE"
            }:
                findings.append(
                    _finding(
                        "revise-without-worker",
                        index,
                        "verdict=revise must name a producing phase",
                    )
                )
            if verdict == "blocked" and route != "HOLD":
                findings.append(
                    _finding("blocked-not-held", index, "verdict=blocked must route to HOLD")
                )
        else:
            if role != "producer":
                findings.append(
                    _finding("producer-role", index, f"{phase} must be performed by a producer")
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

        if reopens and route != "DRAFT":
            findings.append(
                _finding("reopen-without-draft", index, "reopens_promise requires route=DRAFT")
            )
        if phase not in {"DRAFT", "OUTLINE"} and route == "DRAFT" and not reopens:
            findings.append(
                _finding(
                    "draft-without-reopen",
                    index,
                    "a non-DRAFT phase may route to DRAFT only when purpose or Aims reopen",
                )
            )

        if previous is not None:
            previous_route = _trace_token(str(previous.get("route", "")), legacy_probe)
            previous_phase = _trace_token(str(previous.get("phase", "")), legacy_probe)
            if previous_route in TERMINAL_ROUTES:
                findings.append(
                    _finding("receipt-after-terminal", index, f"receipt follows {previous_route}")
                )
            elif phase != previous_route:
                findings.append(
                    _finding(
                        "route-phase-mismatch",
                        index,
                        f"previous route {previous_route} requires next phase "
                        f"{previous_route}, got {phase}",
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
                previous_route == "DRAFT"
                and previous_phase not in {"DRAFT", "OUTLINE"}
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
    """Return phase-to-route edges in execution order for audit summaries."""
    receipts = list(receipts)
    legacy_probe = _legacy_probe(receipts)
    return [
        f"{_trace_token(str(r.get('phase', '')), legacy_probe)}->"
        f"{_trace_token(str(r.get('route', '')), legacy_probe)}"
        for r in receipts
    ]
