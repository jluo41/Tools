"""Reading one Run's receipt: its runtime fields, Version journal and status, and
where its ticket and Result live (moved verbatim from runs.py).
"""
from __future__ import annotations

import re
from pathlib import Path

from live.runs_ids import _TICKET_NAME, _TICKET_SUFFIXES


def _confined_file(path: Path, boundary: Path) -> bool:
    try:
        return path.is_file() and path.resolve().is_relative_to(boundary.resolve())
    except OSError:
        return False


def _existing_path(path: Path | None) -> bool:
    try:
        return bool(path and path.exists() and (path.is_file() or path.is_dir()))
    except OSError:
        return False


def _fields(runtime: Path | None) -> dict[str, str]:
    """Read portable receipt keys without declaring a new receipt dialect."""
    if runtime is None or not runtime.is_file():
        return {}
    text = runtime.read_text(encoding="utf-8", errors="replace")
    if runtime.suffix == ".md":
        front = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
        text = front.group(1) if front else ""

    def field(name: str) -> str:
        hit = re.search(rf"^{re.escape(name)}:[ \t]*(.*?)[ \t]*$", text, re.M)
        return hit.group(1).strip().strip("\"'") if hit else ""

    return {name: field(name) for name in
            ("run", "global_id", "status", "target", "result", "ticket", "family",
             "operation", "interaction", "mode", "version", "step", "outcome", "summary",
             "target_scope", "participants", "coordinator", "contributors", "store", "host")}


def _version_path(runtime: Path, version: str) -> Path | None:
    """Resolve only the declared single-Markdown Version journal."""
    if not re.fullmatch(r"v[0-9][0-9][0-9]", version):
        return None
    return runtime.parent / f"{version}.md"


def _interactive_findings(runtime: Path, fields: dict[str, str]) -> list[str]:
    """Check that the current Version/Step is durable in one Markdown journal."""
    if fields.get("mode", "").lower() == "scratch" or fields.get("interaction", "").lower() == "human-scratch":
        findings = []
        if not _preview_text(runtime.parent / "working.md", runtime.parent).strip():
            findings.append("working.md")
        version, step = fields.get("version", ""), fields.get("step", "")
        path = _version_path(runtime, version)
        if path is None:
            findings.append("valid version pointer")
        if not re.fullmatch(r"s[0-9][0-9][0-9]", step):
            findings.append("valid step pointer")
        text = _preview_text(path, runtime.parent).strip() if path else ""
        if path and not text:
            findings.append(f"{version}.md")
        if text and not _section_body(text, "Human scratch"):
            findings.append("Step s001 · Human scratch")
        return findings
    findings = []
    if not _preview_text(runtime.parent / "working.md", runtime.parent).strip():
        findings.append("working.md")
    version, step = fields.get("version", ""), fields.get("step", "")
    path = _version_path(runtime, version)
    if path is None:
        findings.append("valid version pointer")
    valid_step = bool(re.fullmatch(r"s[0-9][0-9][0-9]", step))
    if not valid_step:
        findings.append("valid step pointer")
    text = _preview_text(path, runtime.parent).strip() if path else ""
    if path and not text:
        findings.append(f"{version}.md")
    step_ids = re.findall(r"^##[ \t]+Step[ \t]+(s[0-9]{3})(?:[ \t].*)?$", text, re.M)
    if text and valid_step:
        expected = [f"s{number:03d}" for number in range(1, int(step[1:]) + 1)]
        if step_ids != expected:
            findings.append(f"ordered Steps s001–{step}")
        for step_id in expected:
            section = _step_section(text, step_id)
            if not section:
                findings.append(f"Step {step_id}")
                continue
            if not _section_body(section, "Human feedback"):
                findings.append(f"Step {step_id} · Human feedback")
            if not _section_body(section, "Saved result"):
                findings.append(f"Step {step_id} · Saved result")
    return findings


def _version_closed(runtime: Path, version: str) -> bool:
    path = _version_path(runtime, version)
    text = _preview_text(path, runtime.parent) if path else ""
    hit = re.search(r"^##[ \t]+Version closure[ \t]*$\n(.*?)(?=^##[ \t]+|\Z)",
                    text, re.M | re.S)
    return bool(hit and _section_body(hit.group(1), "Human close"))


def _declares_outputs(runtime: Path) -> bool:
    """True when a receipt lists a non-empty `outputs:` (inline list or YAML block)."""
    try:
        text = runtime.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    return bool(re.search(r"^outputs:[ \t]*(?:\[[ \t]*[^\]\s]|\r?\n[ \t]*- )", text, re.M))


def _status(runtime: Path | None, fields: dict[str, str]) -> str:
    if runtime is None:
        # An open run (ticket only) is running; anything else without a receipt is held.
        return "Running" if fields.get("status", "").lower() in {"open", "running"} else "Held"
    status = fields.get("status", "").lower()
    # A receipt a laptop selftest seeded (host: laptop-selftest) proves the code path,
    # not an execution: the Run is still planned until its real receipt replaces it.
    if "selftest" in fields.get("host", "").lower():
        return "Ready"
    if status in {"ready", "planned", "ticket", "queued"}:
        return "Ready"
    if status in {"running", "started"}:
        return "Running"
    if status == "waiting-for-feedback":
        if fields.get("operation") == "interactive-writing":
            if _interactive_findings(runtime, fields):
                return "Held"
        return "Waiting"
    if status in {"failed", "error"}:
        return "Failed"
    if status in {"blocked", "held", "rerun", "incomplete"}:
        return "Held"
    if status in {"complete", "completed", "done", "ok"}:  # ok: the Databricks runner's word
        if fields.get("family", "").lower() == "paper" and fields.get("operation") == "judgment":
            return "Done" if _version_closed(runtime, fields.get("version", "")) else "Held"
        if fields.get("operation") == "paragraph-writing":
            # Structural availability only; the writer owns semantic acceptance.
            return "Done" if all(_preview_text(runtime.parent / name, runtime.parent).strip()
                                 for name in ("paragraph.md", "trace.md")) else "Held"
        if fields.get("operation") == "interactive-writing":
            if fields.get("mode", "").lower() == "scratch" or fields.get("interaction", "").lower() == "human-scratch":
                version = fields.get("version", "")
                text = _preview_text(_version_path(runtime, version), runtime.parent) if _version_path(runtime, version) else ""
                closed = "AI generated the Scratch Summary and the person closed the Run." in text
                return "Done" if not _interactive_findings(runtime, fields) and closed else "Held"
            version = fields.get("version", "")
            return ("Done" if not _interactive_findings(runtime, fields)
                    and _version_closed(runtime, version) else "Held")
        has_output = any(child.is_file() and child.name not in {"runtime.yaml", "receipt.yaml"}
                         for child in runtime.parent.iterdir())
        # A server-only Run keeps its output where it was written (row-level data never
        # leaves the server); a receipt that lists those `outputs:` is its Result.
        has_output = has_output or _declares_outputs(runtime)
        return "Done" if has_output else "Held"
    return "Held"


def _ticket_files(runs_dir: Path) -> list[Path]:
    if not runs_dir.is_dir():
        return []
    return [path for path in sorted(runs_dir.rglob("*"))
            if _confined_file(path, runs_dir) and path.suffix in _TICKET_SUFFIXES
            and _TICKET_NAME.match(path.name) and not path.name.startswith(".")
            and _is_ticket_place(path, runs_dir)]


def _is_ticket_place(path: Path, runs_dir: Path) -> bool:
    """One folder per Run (haipipe-run 0.31.0): `runs/<run>/<run>.<ext>` is the ticket, and nothing
    under a Run's `result/` or `passes/` is one; the older flat `runs/<run>.<ext>` still reads."""
    parts = path.relative_to(runs_dir).parts
    if any(part in {"result", "passes"} for part in parts[:-1]):
        return False
    if len(parts) == 2 and _TICKET_NAME.match(parts[0]) and parts[0] != path.stem:
        return False                       # a file beside the ticket inside a Run folder
    return True


def _run_folder_receipt(ticket: Path) -> Path | None:
    """The receipt of a Run in its own folder: a hard Run's `runs/<run>/result/runtime.yaml`, or a
    soft Run's latest pass `runs/<run>/passes/pNN-<MMDD>/runtime.yaml` (a Page Run, 0.125)."""
    if ticket.parent.name != ticket.stem:
        return None
    receipt = ticket.parent / "result" / "runtime.yaml"
    if _confined_file(receipt, ticket.parent):
        return receipt
    from src.run_folders import passes
    for folder in reversed(passes(ticket.parent.parent.parent, ticket.stem)):
        if _confined_file(folder / "runtime.yaml", ticket.parent):
            return folder / "runtime.yaml"
    return None


def _runtime_for(ticket: Path, runs_dir: Path, results_dir: Path) -> Path | None:
    """Pair by logical ticket address, then accept a receipt naming that ticket."""
    relative = ticket.relative_to(runs_dir).with_suffix("")
    candidates = (
        results_dir / relative / "runtime.yaml",
        results_dir / ticket.stem / "runtime.yaml",
        results_dir / (str(relative) + ".yaml"),
    )
    for candidate in candidates:
        if _confined_file(candidate, results_dir):
            return candidate
    rel_text = str(ticket.relative_to(runs_dir))
    for candidate in sorted(results_dir.rglob("runtime.yaml")) if results_dir.is_dir() else []:
        if ("attempts" in candidate.relative_to(results_dir).parts
                or not _confined_file(candidate, results_dir)):
            continue
        fields = _fields(candidate)
        if fields.get("ticket") in {rel_text, ticket.name, str(ticket)}:
            return candidate
    return None


def _fallback_result(runtime: Path | None, base: Path) -> str:
    if runtime is None:
        return ""
    try:
        return str(runtime.parent.relative_to(base))
    except ValueError:
        return str(runtime.parent)


def _repo_path(root: Path, value: str) -> Path | None:
    """Resolve a registry pointer only for display; never follow it for preview."""
    if not value:
        return None
    path = Path(value)
    return path if path.is_absolute() else root / path


# at the end, not the top: these parts import one another, so each can be imported first
from live.runs_result_view import _preview_text, _section_body, _step_section
