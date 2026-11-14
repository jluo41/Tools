"""Run names and identities in the Run Space: ticket patterns, Page Run kinds,
labels and writing subspaces, and the Page Run order audit (moved verbatim from runs.py).
"""
from __future__ import annotations

import re

from src import run_names as _names


_TICKET_SUFFIXES = {".sh", ".ps1", ".cmd", ".py", ".do", ".r", ".R", ".yaml", ".yml", ".md"}
_TICKET_NAME = re.compile(
    r"(?:^rp-(?:struct|sec|para)-\d{2}(?:_P\d{2}(?:-P\d{2})?)?"
    r"|^rp-scratch-\d{2}_[A-Za-z0-9._-]+"
    r"|^rp-revise-\d{2}_[A-Za-z0-9._-]+"
    r"|^rp-(?:embed|auto)-\d{2}(?:_[A-Za-z0-9._-]+)?"
    r"|^re-(?:value|display|cite)-\d{2}(?:_[a-z0-9][a-z0-9_-]*)?"
    r"|^r(?:idea|claim|task|narra|response)-\d+"
    r"|^rp\d+|^rl\d+|^ri\d+|^rd\d+|^r\d+|^run[-_]"
    r"|^b\d+[._]j\d+[._]t\d+[._]r\d+|^p[._]?j\d+[._]?t\d+[._]?r\d+)",
    re.I,
)
_STATE_ORDER = {"Running": 0, "Waiting": 1, "Failed": 2, "Held": 3,
                "Ready": 4, "Done": 5}
_PAGE_WRITING_OPERATIONS = {"interactive-writing", "paragraph-writing"}
_STRUCTURE_RUN = "rp-struct-01"
_LEGACY_STRUCTURE_RUNS = {"rp00_mermaid-structure"}
_STRUCTURE_RUNS = {_STRUCTURE_RUN, *_LEGACY_STRUCTURE_RUNS}
_STRUCTURE_RUN_RE = re.compile(r"rp-struct-(?:0[1-9]|[1-9]\d+)", re.I)
_EVIDENCE_TYPES = {
    "VALUE": "Value",
    "TABLE": "Display",  # legacy alias retained for old Result manifests
    "DISPLAY": "Display",
    "CITE": "Citation",
}
_EVIDENCE_TYPE_ORDER = ("Value", "Display", "Citation")
_SECTION_RUN = re.compile(r"rp-sec-(?:0[1-9]|[1-9]\d+)", re.I)
_SCRATCH_RUN = re.compile(r"rp-scratch-(?:0[1-9]|[1-9]\d+)_([A-Za-z0-9._-]+)", re.I)
# Revise: compare two frozen texts of one target and settle each change. Its
# Result is the change ledger; the accepted text returns to the writing Run
# as a Version (haipipe-draft-writing (ref/revise.md)).
_REVISE_RUN = re.compile(r"rp-revise-(?:0[1-9]|[1-9]\d+)_([A-Za-z0-9._-]+)", re.I)
# Auto write and Evidence embed: an agent writes the Draft sentences, or folds
# accepted evidence into the plan, for one target (page-run-families.md).
_AUTO_EMBED_RUN = re.compile(r"rp-(auto|embed)-(?:0[1-9]|[1-9]\d+)(?:_([A-Za-z0-9._-]+))?", re.I)
_PARAGRAPH_RUN = re.compile(
    r"(rp-para-(?:0[1-9]|[1-9]\d+))_P((?:0[1-9]|[1-9]\d+))"
    r"(?:-P((?:0[1-9]|[1-9]\d+)))?",
    re.I,
)
_LEGACY_PARAGRAPH_RUN = re.compile(
    r"(rp(?:0[1-9]|[1-9]\d+))_p(0[1-9]|[1-9]\d+)"
    r"(?:-p(0[1-9]|[1-9]\d+))?",
    re.I,
)


_WRITING_KINDS = ("structure", "section", "paragraph", "scratch", "revise", "auto-write",
                  "evidence-embed", "context")


def _new_kind(run_id: str) -> str | None:
    """The kind of a readable run name (`run-section-0927-cleanup` → `section`), else None."""
    found = _names.NAME.match(str(run_id or ""))
    return found.group("kind") if found else None


def _is_structure_run(run_id: str) -> bool:
    """Recognize the current structure Run and readable legacy records."""
    return (run_id in _STRUCTURE_RUNS or _STRUCTURE_RUN_RE.fullmatch(run_id) is not None
            or _new_kind(run_id) == "structure")


def _writing_operation(fields: dict[str, str]) -> bool:
    """Return whether the Run uses a writing dialect that requires a receipt."""
    return fields.get("operation", "").lower() in _PAGE_WRITING_OPERATIONS


def _is_page_run(fields: dict[str, str]) -> bool:
    """Only human-feedback interactive writing belongs to the Page Run lane."""
    return fields.get("operation", "").lower() == "interactive-writing"


def _page_run_label(run_id: str) -> str:
    """Keep the Page Run column short while preserving its canonical identity."""
    if _names.is_run_name(run_id):
        return run_id                     # already readable
    if run_id in _LEGACY_STRUCTURE_RUNS:
        return "rp00 · Structure (legacy)"
    if _is_structure_run(run_id):
        return f"{run_id.lower()} · Structure"
    if _SECTION_RUN.fullmatch(run_id):
        return f"{run_id.lower()} · Section"
    scratch = _SCRATCH_RUN.fullmatch(run_id)
    if scratch:
        return f"{run_id.lower()} · Scratch · {scratch.group(1)}"
    revise = _REVISE_RUN.fullmatch(run_id)
    if revise:
        return f"{run_id.lower()} · Revise · {revise.group(1)}"
    auto_embed = _AUTO_EMBED_RUN.fullmatch(run_id)
    if auto_embed:
        kind = "Auto write" if auto_embed.group(1).lower() == "auto" else "Evidence embed"
        return " · ".join(x for x in (run_id.lower(), kind, auto_embed.group(2) or "") if x)
    match = _PARAGRAPH_RUN.fullmatch(run_id) or _LEGACY_PARAGRAPH_RUN.fullmatch(run_id)
    if not match:
        return run_id
    scope = f"P{match.group(2)}"
    if match.group(3):
        scope += f"-P{match.group(3)}"
    return f"{match.group(1).lower()} · {scope.upper()}"


def _valid_page_run_id(run_id: str) -> bool:
    """Accept typed Page Run ids, while keeping old records readable."""
    return (_is_structure_run(run_id) or _SECTION_RUN.fullmatch(run_id) is not None
            or _SCRATCH_RUN.fullmatch(run_id) is not None
            or _REVISE_RUN.fullmatch(run_id) is not None
            or _AUTO_EMBED_RUN.fullmatch(run_id) is not None
            or _names.is_run_name(run_id)
            or _PARAGRAPH_RUN.fullmatch(run_id) is not None
            or _LEGACY_PARAGRAPH_RUN.fullmatch(run_id) is not None)


def _audit_page_run_order(rows: list[dict]) -> None:
    """Reject noncanonical ids and require the closed Structure Run."""
    # A fixed Delivery Run (run-delivery-<lane>) builds files; it is not a writing Run.
    page_rows = [row for row in rows if row.get("lane") == "page" and row.get("operation") != "delivery"]
    structure = next((row for row in page_rows
                      if _is_structure_run(row["run_id"])), None)
    structure_closed = bool(structure and structure.get("status") == "Done")
    for row in page_rows:
        run_id = row["run_id"]
        if not _valid_page_run_id(run_id):
            row["status"] = "Held"
            row.setdefault("audit", []).append(
            "invalid Page Run identity; expected a full name run-<kind>-<slug> "
                "(kind: structure, section, paragraph, scratch, revise, auto-write, evidence-embed)"
            )
            continue
        if _is_structure_run(run_id):
            continue
        if row.get("mode") in {"scratch", "revise"}:
            # Scratch and Revise are the person's direct lanes in Draft Space.
            # They may be opened while the fused Structure Run is still being
            # settled; Section/Paragraph writing remains gated on Structure.
            continue
        if structure_closed:
            continue
        row["status"] = "Held"
        row.setdefault("audit", []).append(
            "Page Section/Paragraph Run requires a closed structure Run"
        )


def _page_writing_subspace(row: dict) -> str:
    """Map one local interactive Run to its minimal writing subspace."""
    new = {"structure": "Structure", "scratch": "Scratch", "revise": "Revise",
           "section": "Section", "paragraph": "Paragraph"}.get(_new_kind(row.get("run_id", "")))
    if new:
        return new
    if _is_structure_run(str(row.get("run_id", ""))):
        return "Structure"
    if row.get("mode") == "scratch" or _SCRATCH_RUN.fullmatch(str(row.get("run_id", ""))):
        return "Scratch"
    if _REVISE_RUN.fullmatch(str(row.get("run_id", ""))):
        return "Revise"
    if _SECTION_RUN.fullmatch(str(row.get("run_id", ""))):
        return "Section"
    target = str(row.get("target", ""))
    if re.search(r"(?:^|-)P\d+", target, re.I) or "_p" in row.get("run_id", "").lower():
        return "Paragraph"
    return "Section"
