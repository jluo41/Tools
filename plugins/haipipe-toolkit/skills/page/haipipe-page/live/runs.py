"""The Run Space inside 🧭 Outline, read-only.

The Page-facing vocabulary has three areas: local Page Runs for human/Page
interactions and Page-owned Evidence, plus Supporting Runs for linked work
owned elsewhere. Page Writing includes a small human-first Scratch Run for
rough thinking at Section or whole paragraph-group scope in the current
Outline grammar. There is no separate subsection node, and B/symbol rows are
not Scratch targets. Supporting
Runs remain inspectable references; they are never copied into this Page. The
reader-facing projection is result-first: a closed card shows only what the
Run is called and what it is doing, while its real Result appears when the
card is opened.

Native families remain intact below this projection, so Board and standalone
Page resolve the same records. ``new-*`` remains a plan rather than a Run.
Nothing in this module executes or edits a Run, Result, or feedback record.
"""
from __future__ import annotations

import difflib
import html
import re
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse

from src.item_table import (compact_global_run, compact_paper_run, read_items,
                            readable_global_run, readable_paper_route, repo_root,
                            run_registry)
try:
    # Board contributes the job-backed Task adapter through its ``src``
    # namespace. A standalone Page has no Board package and therefore keeps
    # the Folder-local Runs dialect only.
    from src.dialect_task_block import page_info as task_page_info
except ImportError:
    def task_page_info(_block, _page_src):
        return None


_TICKET_SUFFIXES = {".sh", ".ps1", ".py", ".do", ".r", ".R", ".yaml", ".yml", ".md"}
_TICKET_NAME = re.compile(
    r"(?:^rp-(?:struct|sec|para)-\d{2}(?:_P\d{2}(?:-P\d{2})?)?"
    r"|^rp-scratch-\d{2}_[A-Za-z0-9._-]+"
    r"|^re-(?:value|display|cite)-\d{2}(?:_[a-z0-9][a-z0-9_-]*)?"
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


def _is_structure_run(run_id: str) -> bool:
    """Recognize the current structure Run and readable legacy records."""
    return run_id in _STRUCTURE_RUNS or _STRUCTURE_RUN_RE.fullmatch(run_id) is not None


_CSS = """
:root{--bg:#fff;--fg:#1c1d1f;--mut:#71727a;--line:#e4e4e7;--card:#f7f7f8;
 --acc:#3b6ea5;--ok:#287443;--warn:#a95b12;--bad:#b13c3c}
@media(prefers-color-scheme:dark){:root{--bg:#161719;--fg:#e8e8e6;--mut:#9a9a97;
 --line:#2c2e33;--card:#1d1f23;--acc:#7aa7d8;--ok:#74b68a;--warn:#e0a05c;--bad:#e77b7b}}
body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.55 -apple-system,
 BlinkMacSystemFont,'Segoe UI',sans-serif}header{padding:10px 16px 7px}h1{font-size:16px;margin:0}
.embedded header{display:none}
.mut{color:var(--mut);font-size:12.5px}.lead{margin:3px 0 0}.summary{display:flex;gap:8px;
 padding:7px 16px;border-top:1px solid var(--line);border-bottom:1px solid var(--line);font-size:12.5px}
.wrap{padding:0 16px 16px;overflow:auto}.note{margin:9px 0;font-size:12.5px;color:var(--mut)}
code{font:12px ui-monospace,SFMono-Regular,Menlo,monospace}.route{font-weight:650;white-space:nowrap}.state{font-weight:650;white-space:nowrap}
.state.ready{color:var(--acc)}.state.running,.state.waiting{color:var(--warn)}.state.done{color:var(--ok)}.state.failed,.state.held{color:var(--bad)}
.repo-path{white-space:normal;overflow-wrap:anywhere;word-break:break-word;user-select:text}
.run-space-switcher{display:flex;gap:6px;overflow-x:auto;padding:0 0 9px;margin:0 0 11px;border-bottom:1px solid var(--line);scrollbar-width:none}.run-space-switcher::-webkit-scrollbar{display:none}.run-space-tab{appearance:none;border:1px solid var(--line);background:var(--card);color:var(--fg);border-radius:7px;padding:5px 10px;font-size:13px;line-height:1.35;cursor:pointer;white-space:nowrap;flex:none}.run-space-tab:hover{border-color:var(--acc)}.run-space-tab.on{border-color:var(--acc);color:var(--acc);font-weight:650;background:var(--bg)}.run-space-panels{min-width:0}.run-space-panel[hidden]{display:none}.run-space-overview{display:flex;gap:6px;flex-wrap:wrap;margin:0 0 12px}.run-space-overview span{border:1px solid var(--line);border-radius:999px;padding:2px 8px;color:var(--mut);font-size:11.5px;line-height:1.4;white-space:nowrap}.run-space-overview .total{color:var(--fg);font-weight:650}.run-subspace{margin:13px 0 18px}.run-subspace>h3{font-size:13px;margin:0 0 6px;color:var(--mut);font-weight:700;letter-spacing:.02em}
.run-cards{display:grid;gap:7px}.run-card{border:1px solid var(--line);border-radius:9px;background:var(--bg);overflow:hidden}.run-card-summary{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:2px 10px;padding:10px 12px;cursor:pointer}.run-card-summary:hover{background:var(--card)}.run-card-summary.bound-focus{outline:2px solid var(--acc);outline-offset:3px}
.run-card-summary::after{content:'›';grid-column:2;grid-row:1 / span 2;align-self:center;color:var(--mut);font:bold 18px/1 sans-serif;transition:transform .15s}.run-card-summary[aria-expanded=true]::after{transform:rotate(90deg)}
.run-card-name{font-weight:700;min-width:0;overflow-wrap:anywhere}.run-card-action{grid-column:1;color:var(--mut);font-size:13px;overflow-wrap:anywhere}.run-state-dot{grid-column:2;grid-row:1;align-self:start;margin-right:18px;font-size:11px;line-height:1;color:var(--mut)}.run-state-dot.done{color:var(--ok)}.run-state-dot.running,.run-state-dot.waiting{color:var(--warn)}.run-state-dot.failed,.run-state-dot.held{color:var(--bad)}.run-state-dot.ready{color:var(--acc)}
.run-card-detail[hidden]{display:none}.run-card-detail{border-top:1px solid var(--line);padding:12px;background:var(--card)}.detailbox{font-size:14px}
.detailbox p{margin:7px 0}.detailbox .kv{display:grid;grid-template-columns:118px minmax(0,1fr);gap:8px}.detailbox h3{font-size:15px;margin:0}.detailbox h4{font-size:13px;margin:13px 0 5px;color:var(--mut)}
.detail-head{display:flex;align-items:center;gap:10px;justify-content:space-between;margin-bottom:10px}.detail-title{font-size:16px;font-weight:700}
.run-meta{display:grid;grid-template-columns:minmax(0,2fr) minmax(110px,1fr);gap:8px;margin:0 0 14px}
.run-meta div{padding:8px 10px;border:1px solid var(--line);border-radius:7px;background:var(--bg)}
.run-meta .wide{grid-column:1/-1}.run-meta dt{color:var(--mut);font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.04em}
.run-meta dd{margin:2px 0 0;font-size:13.5px}.review-card{margin:10px 0;padding:10px 12px;border-radius:8px;background:var(--bg);border:1px solid var(--line)}
.review-card.feedback{border-left:3px solid var(--warn)}.review-card.result{border-left:3px solid var(--ok)}
.review-card h3{margin-bottom:6px}.review-card blockquote{margin:6px 0;padding-left:10px;border-left:2px solid var(--line);color:var(--fg)}
.review-card ul,.review-card ol{margin:6px 0;padding-left:22px}.review-card pre,.step-history pre{white-space:pre-wrap;overflow-wrap:anywhere;word-break:break-word;margin:7px 0;padding:9px;border-radius:6px;background:var(--card);font-size:12px}
.track-card{margin:14px 0 4px;padding:11px 12px;border:1px solid var(--line);border-radius:8px;background:var(--card)}
.track-card h4{margin:0 0 8px;color:var(--fg)}.track-kind,.track-status{color:var(--mut);font-size:12px}.track-diff{margin:8px 0;padding:11px 12px;border-radius:7px;background:var(--bg);font-family:Georgia,'Times New Roman',serif;font-size:16px;line-height:1.75;overflow-wrap:anywhere}
.track-diff del{color:#b42318;background:#fee4e2;text-decoration:line-through;text-decoration-thickness:1.5px}.track-diff ins{color:#16733c;background:#dcfae6;text-decoration:underline;text-decoration-thickness:1.5px;text-underline-offset:2px}.track-card .why,.track-card .preference{margin:7px 0}.track-legend{display:flex;gap:12px;margin:4px 0 8px;color:var(--mut);font-size:11px}.track-legend .removed{color:#b42318}.track-legend .added{color:#16733c}
.md-table{width:100%;margin:8px 0;font-size:12px}.md-table th,.md-table td{padding:6px;border:1px solid var(--line)}
.run-logic{margin:8px 0 12px}.run-logic h4{margin-top:0}.run-logic-viewport{max-width:100%;overflow:auto;background:#fff;border:1px solid var(--line);border-radius:8px;padding:6px;box-sizing:border-box}
.run-logic-canvas{min-width:0}.logic-svg{display:block;width:100%;height:auto;overflow:visible}.logic-edge{fill:none;stroke:var(--acc);stroke-width:1.7;opacity:.82}
.logic-edge-label{fill:var(--mut);font:500 14px -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}.logic-group{fill:color-mix(in srgb,var(--acc) 2%,var(--card));stroke:var(--line);stroke-width:1.2}
.logic-group-label{fill:var(--acc);font:650 15px -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}.logic-node{fill:color-mix(in srgb,var(--acc) 5%,var(--card));stroke:var(--acc);stroke-width:1.4}
.logic-node-label{fill:var(--fg);font:600 18px -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
.logic-steps{display:none;margin:4px 0;padding:0;list-style:none}.logic-steps li{padding:8px 0;border-bottom:1px solid var(--line)}
.logic-steps li:last-child{border-bottom:0}.logic-steps b{display:block}.logic-steps span{display:block;margin-top:3px;color:var(--acc);font-size:13px}
.next-action{margin:10px 0;padding:9px 11px;border-radius:7px;background:color-mix(in srgb,var(--acc) 10%,var(--bg));border-left:3px solid var(--acc)}
.history,.technical{margin-top:10px;border-top:1px solid var(--line);padding-top:9px}.history>summary,.technical>summary,.step-history>summary{cursor:pointer;font-weight:650}
.step-history{min-width:0;overflow-wrap:anywhere;margin:8px 0;padding:8px 10px;border:1px solid var(--line);border-radius:7px;background:var(--bg)}
.technical dl{margin:8px 0}.technical dt{margin-top:7px;color:var(--mut);font-size:11px;font-weight:700;text-transform:uppercase}.technical dd{margin:1px 0}
.refs{margin:5px 0 0;padding-left:18px}.run-preview{overflow-wrap:anywhere;font-size:13px;line-height:1.6;margin:8px 0}
.detailbox h2{font-size:14px;margin:14px 0 5px}.summary{flex-wrap:wrap}.run-result{margin:0 0 10px;padding:11px 12px;border-left:3px solid var(--ok);border-radius:7px;background:var(--bg)}.run-result h3{margin:0 0 7px;font-size:13px;color:var(--mut);text-transform:uppercase;letter-spacing:.04em}.run-output{overflow-wrap:anywhere;word-break:break-word}.run-output pre{white-space:pre-wrap;overflow-wrap:anywhere;margin:0;padding:9px;border-radius:6px;background:var(--card);font-size:12.5px}.run-result-empty{color:var(--mut);font-size:13px}.run-context,.support-member{margin-top:9px;border-top:1px solid var(--line);padding-top:8px}.run-context summary,.support-member>summary{cursor:pointer;font-weight:650;color:var(--mut)}.support-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.support-column{min-width:0}.support-column>h3{font-size:13px;margin:0 0 6px}.support-group-detail{margin:0}.support-member{padding:0 0 8px}.support-member:last-child{border-bottom:0}.support-member>summary code{font-weight:650}.lane-empty{margin:8px 0 0;padding:10px 12px;border:1px dashed var(--line);border-radius:7px;color:var(--mut)}
.run-label-summary{display:flex;align-items:center;gap:5px;flex-wrap:wrap;margin:0 0 9px;padding:5px 7px;border:1px solid var(--line);border-radius:6px;background:var(--bg)}.run-label-summary-title{color:var(--mut);font:650 10px -apple-system,sans-serif;text-transform:uppercase;letter-spacing:.04em}.run-label-chip{display:inline-flex;gap:4px;align-items:baseline;padding:2px 6px;border:1px solid var(--line);border-radius:999px;color:var(--mut);font-size:11.5px;max-width:100%;overflow:hidden}.run-label-chip b{color:var(--acc);font-size:9.5px}.run-label-chip span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.workflow-map-note{margin:0 0 12px;color:var(--mut);font-size:12.5px;line-height:1.5}.workflow-map-viewport{max-width:100%;overflow-x:auto;border:1px solid var(--line);border-radius:9px;background:var(--bg);-webkit-overflow-scrolling:touch}.workflow-map-grid{display:grid;grid-template-columns:138px repeat(4,minmax(190px,1fr));min-width:898px}.workflow-map-row{display:contents}.workflow-map-cell{min-width:0;padding:9px 10px;border-right:1px solid var(--line);border-bottom:1px solid var(--line);overflow-wrap:anywhere}.workflow-map-cell:nth-child(5n){border-right:0}.workflow-map-row:last-child .workflow-map-cell{border-bottom:0}.workflow-map-head{background:var(--card);color:var(--mut);font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:uppercase}.workflow-map-spec{font-weight:700;color:var(--fg);font-size:12.5px}.workflow-map-spec code{display:block;margin-top:2px;color:var(--acc);font-size:11px}.workflow-map-cell code{font-size:11px;white-space:normal}.workflow-map-mode{display:inline-block;margin-bottom:3px;color:var(--acc);font-size:10px;font-weight:700;letter-spacing:.04em;text-transform:uppercase}.workflow-map-schema{display:block;font-weight:650;font-size:12px}.workflow-map-path{display:block;margin-top:3px;color:var(--mut);font-size:11px;line-height:1.4}.workflow-map-empty{color:var(--mut);font-size:12px}
.scripts{margin:16px 0}.scripts summary{cursor:pointer;font-weight:650}.scripts ul{padding-left:20px}
@media(max-width:700px){body{font-size:15px}.wrap{padding:0 10px 14px;overflow:visible}.summary{padding:7px 10px}.run-space-switcher{margin-bottom:9px}.run-space-tab{font-size:13px;padding:5px 9px}.run-space-overview{gap:5px}.run-space-overview span{font-size:11px;padding:2px 7px}.support-grid{grid-template-columns:1fr}
 .run-card-summary{padding:10px}.run-card-detail{padding:10px}.detailbox{padding:0}.run-meta{grid-template-columns:1fr 1fr}.run-meta .wide{grid-column:1/-1}
 .detailbox .kv{grid-template-columns:96px minmax(0,1fr)}
 .detail-head{display:none}.review-card{padding:10px}.md-table{display:table}.run-logic-viewport{display:none}.logic-steps{display:block}.detail-title{font-size:17px}}
"""


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
             "target_scope", "participants", "coordinator", "contributors")}


def _writing_operation(fields: dict[str, str]) -> bool:
    """Return whether the Run uses a writing dialect that requires a receipt."""
    return fields.get("operation", "").lower() in _PAGE_WRITING_OPERATIONS


def _is_page_run(fields: dict[str, str]) -> bool:
    """Only human-feedback interactive writing belongs to the Page Run lane."""
    return fields.get("operation", "").lower() == "interactive-writing"


def _page_run_label(run_id: str) -> str:
    """Keep the Page Run column short while preserving its canonical identity."""
    if run_id in _LEGACY_STRUCTURE_RUNS:
        return "rp00 · Mermaid Structure (legacy)"
    if _is_structure_run(run_id):
        return f"{run_id.lower()} · Mermaid Structure"
    if _SECTION_RUN.fullmatch(run_id):
        return f"{run_id.lower()} · Section"
    scratch = _SCRATCH_RUN.fullmatch(run_id)
    if scratch:
        return f"{run_id.lower()} · Scratch · {scratch.group(1)}"
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
            or _PARAGRAPH_RUN.fullmatch(run_id) is not None
            or _LEGACY_PARAGRAPH_RUN.fullmatch(run_id) is not None)


def _audit_page_run_order(rows: list[dict]) -> None:
    """Reject noncanonical ids and require the closed Mermaid Structure Run."""
    page_rows = [row for row in rows if row.get("lane") == "page"]
    structure = next((row for row in page_rows
                      if _is_structure_run(row["run_id"])), None)
    structure_closed = bool(structure and structure.get("status") == "Done")
    for row in page_rows:
        run_id = row["run_id"]
        if not _valid_page_run_id(run_id):
            row["status"] = "Held"
            row.setdefault("audit", []).append(
            "invalid Page Run identity; expected rp-struct-NN, rp-sec-NN, "
                "rp-scratch-NN_<target>, or rp-para-NN_Pxx[-Pyy]"
            )
            continue
        if _is_structure_run(run_id):
            continue
        if row.get("mode") == "scratch":
            # Scratch is the person's pre-writing thinking lane. It may be
            # opened from Draft while the fused Structure Run is still being
            # settled; Section/Paragraph writing remains gated on Structure.
            continue
        if structure_closed:
            continue
        row["status"] = "Held"
        row.setdefault("audit", []).append(
            "Page Section/Paragraph Run requires a closed rp-struct-01"
        )


def _ticket_note(ticket: Path, label: str) -> str:
    """Read one Markdown list field from an owned Page Run ticket."""
    if ticket.suffix.lower() != ".md":
        return ""
    text = _preview_text(ticket, ticket.parent)
    hit = re.search(rf"^-\s+{re.escape(label)}:\s*(.+?)\s*$", text, re.M | re.I)
    return hit.group(1).strip() if hit else ""


def _preview_text(path: Path, boundary: Path) -> str:
    """Bounded plain-text preview of an owned file, never a referenced external path."""
    try:
        if not path.resolve().is_relative_to(boundary.resolve()) or not path.is_file():
            return ""
        with path.open("rb") as stream:
            data = stream.read(65537)
        text = data[:65536].decode("utf-8", errors="replace")
        return text + ("\n[Preview truncated at 64 KiB]" if len(data) > 65536 else "")
    except OSError:
        return ""


def _plain_inline_markdown(value: str) -> str:
    """Reduce one trusted local summary line to compact reader-facing text."""
    value = re.sub(r"[`*_]", "", value).strip()
    return re.sub(r"\s+", " ", value).rstrip(".")


def _result_outcome(runtime: Path | None, fields: dict[str, str]) -> str:
    """Read one bounded outcome from a local receipt or its summary report."""
    declared = fields.get("outcome") or fields.get("summary")
    if declared:
        return _plain_inline_markdown(declared)
    if runtime is None:
        return ""
    report = _preview_text(runtime.parent / "report.md", runtime.parent)
    if not report:
        return ""
    action = {"create-semantic-records": "Created semantic records",
              "resume-and-build": "Resumed and rebuilt Page"}.get(
                  fields.get("mode", ""), "")

    def with_action(value: str) -> str:
        value = _plain_inline_markdown(value)
        return f"{action} — {value}" if action else value

    for label in ("Outcome", "Summary"):
        hit = re.search(rf"^-\s+{label}:\s*(.+?)\s*$", report, re.M | re.I)
        if hit:
            return with_action(hit.group(1))
    coverage = re.search(r"^-\s+Coverage:\s*(.+?)\s*$", report, re.M | re.I)
    gate = re.search(r"^-\s+Mechanical gate:\s*(.+?)\s*$", report, re.M | re.I)
    if coverage or gate:
        parts = []
        if coverage:
            parts.append(_plain_inline_markdown(coverage.group(1)))
        if gate:
            parts.append("Mechanical gate " + _plain_inline_markdown(gate.group(1)))
        return with_action(" · ".join(parts))
    summary = re.search(r"^##\s+Summary\s*$\n(.*?)(?=^##\s+|\Z)", report,
                        re.M | re.S | re.I)
    if summary:
        first = next((line.strip().lstrip("-* ")
                      for line in summary.group(1).splitlines() if line.strip()), "")
        return with_action(first)
    return ""


def _evidence_type(row: dict) -> str:
    """Return the reader-facing Page Evidence subspace for one Run."""
    candidates = [row.get("target", ""), *row.get("refs", [])]
    for value in candidates:
        match = re.search(
            r"E\d+-(VALUE|TABLE|DISPLAY|CITE)(?:-|$)",
            str(value or ""),
            re.I,
        )
        if match:
            return _EVIDENCE_TYPES[match.group(1).upper()]
    return ""


def _evidence_item_label(row: dict) -> str:
    """Turn an Evidence Item id into a short card label."""
    candidates = [row.get("target", ""), *row.get("refs", [])]
    for value in candidates:
        match = re.search(r"(E\d+)-(?:VALUE|TABLE|DISPLAY|CITE)(?:-|$)",
                          str(value or ""), re.I)
        if match:
            return match.group(1).upper()
    return "Evidence"


def _evidence_records(page_src: Path) -> dict[str, dict]:
    """Load the same Result-backed Evidence records used by Evidence Space."""
    try:
        from live.evidence import _result_records
        records = _result_records(page_src.parent)
    except (ImportError, OSError, ValueError, TypeError, AttributeError):
        return {}
    return {str(record.get("id", "")).strip(): record for record in records
            if str(record.get("id", "")).strip()}


def _attach_evidence_bindings(page_src: Path, rows: list[dict]) -> None:
    """Attach readable Evidence Item records to every bound Run."""
    records = _evidence_records(page_src)
    if not records:
        return
    for row in rows:
        bindings = [records[ref] for ref in row.get("refs", []) if ref in records]
        if not bindings:
            continue
        labels = []
        for binding in bindings:
            fields = binding.get("fields", {})
            for label in fields.get("labels", []):
                if isinstance(label, dict) and label not in labels:
                    labels.append(label)
        if labels:
            row["evidence_labels"] = labels
        row["evidence_bindings"] = bindings
        primary = bindings[0]
        item_id = str(primary.get("id", "")).strip()
        match = re.match(r"(E\d+)-", item_id, re.I)
        row["evidence_item_id"] = match.group(1).upper() if match else item_id
        row["evidence_title"] = str(primary.get("title", "")).strip()


def _page_writing_subspace(row: dict) -> str:
    """Map one local interactive Run to its minimal writing subspace."""
    if _is_structure_run(str(row.get("run_id", ""))):
        return "Structure"
    if row.get("mode") == "scratch" or _SCRATCH_RUN.fullmatch(str(row.get("run_id", ""))):
        return "Scratch"
    if _SECTION_RUN.fullmatch(str(row.get("run_id", ""))):
        return "Section"
    target = str(row.get("target", ""))
    if re.search(r"(?:^|-)P\d+", target, re.I) or "_p" in row.get("run_id", "").lower():
        return "Paragraph"
    return "Section"


def _run_pills(items: list[tuple[str, int]]) -> str:
    """Render the compact, non-interactive count pills used by each space."""
    return "".join(
        '<span class="run-pill%s">%d %s</span>' % (
            " total" if index == 0 else "", count, html.escape(label)
        )
        for index, (label, count) in enumerate(items)
    )


def _fallback_evidence_counts(rows: list[dict]) -> tuple[int, dict[str, int]]:
    """Count unique Evidence Item ids when no Result snapshot is available."""
    items: dict[str, str] = {}
    for row in rows:
        for value in [row.get("target", ""), *row.get("refs", [])]:
            for match in re.finditer(
                    r"\b(E\d+)-(VALUE|TABLE|DISPLAY|CITE)(?:-[a-z0-9-]+)?\b",
                    str(value or ""), re.I):
                items.setdefault(match.group(1).upper(),
                                 _EVIDENCE_TYPES[match.group(2).upper()])
    counts = {label: 0 for label in _EVIDENCE_TYPE_ORDER}
    for kind in items.values():
        if kind in counts:
            counts[kind] += 1
    return len(items), counts


def _evidence_summary_counts(page_src: Path, rows: list[dict]) -> tuple[int, dict[str, int]]:
    """Use the same current Result records as Evidence Space for its pills."""
    try:
        from live.evidence import _evidence_type as result_evidence_type
        from live.evidence import _result_records
        records = _result_records(page_src.parent)
    except (ImportError, OSError, ValueError, TypeError, AttributeError):
        records = []
        result_evidence_type = None
    if records and result_evidence_type is not None:
        counts = {label: 0 for label in _EVIDENCE_TYPE_ORDER}
        for record in records:
            kind = result_evidence_type(record)
            if kind == "DISPLAY":
                counts["Display"] += 1
            elif kind == "CITE":
                counts["Citation"] += 1
            elif kind == "VALUE":
                counts["Value"] += 1
        return len(records), counts
    return _fallback_evidence_counts(rows)


def _short_text(value: str, limit: int = 150) -> str:
    """Keep a reader-facing action short without inventing a summary."""
    clean = _plain_inline_markdown(value)
    if len(clean) <= limit:
        return clean
    return clean[: limit - 1].rstrip() + "…"


def _run_label_summary(row: dict) -> str:
    """Render the compact V/C/D provenance index for an Evidence Run."""
    labels = row.get("evidence_labels", [])
    if not isinstance(labels, list):
        return ""
    chips = []
    for raw in labels:
        if not isinstance(raw, dict):
            continue
        token = str(raw.get("token") or raw.get("reference") or raw.get("key") or "").strip()
        if not token:
            continue
        kind = str(raw.get("kind", "")).strip().upper() or "LABEL"
        display = str(raw.get("display", "")).strip()
        status = str(raw.get("status", "unresolved")).strip().lower()
        visible = display if display and status not in {"pending", "unresolved", "missing"} else token
        chips.append(
            '<span class=run-label-chip title="%s"><b>%s</b><span>%s</span></span>'
            % (html.escape(token, quote=True), html.escape(kind), html.escape(visible)),
        )
    if not chips:
        return ""
    return '<div class=run-label-summary><span class=run-label-summary-title>Labels</span>%s</div>' % "".join(chips)
def _run_name(row: dict) -> str:
    """Return the semantic name shown on a closed Run card."""
    if row.get("lane") == "page" and row.get("operation") == "interactive-writing":
        run_id = str(row.get("run_id", ""))
        if row.get("mode") == "scratch" or _SCRATCH_RUN.fullmatch(run_id):
            scope = str(row.get("target_scope", "target")).capitalize()
            target = str(row.get("target", "")).strip()
            return "Scratch · %s%s" % (scope, (" · " + target) if target else "")
        if _is_structure_run(run_id):
            return "Structure"
        target = str(row.get("target", "")).strip()
        if _SECTION_RUN.fullmatch(run_id):
            return "Section · " + target if target else "Section"
        legacy_paragraph = ("_p" in run_id.lower() or
                            bool(re.fullmatch(r"rp\d+", run_id, re.I)))
        if (_PARAGRAPH_RUN.fullmatch(run_id) or legacy_paragraph) and target:
            return "Paragraph · " + target.replace("-", "–")
        return "Section" if legacy_paragraph else _page_run_label(run_id)
    if row.get("operation") == "paragraph-writing":
        target = str(row.get("target", "")).strip()
        return "Paragraph · " + (target or "Writing")
    evidence_type = _evidence_type(row)
    if evidence_type:
        item_id = str(row.get("evidence_item_id", "")).strip() or _evidence_item_label(row)
        title = str(row.get("evidence_title", "")).strip()
        label = " · ".join(part for part in (item_id, title) if part)
        bindings = row.get("evidence_bindings", [])
        if isinstance(bindings, list) and len(bindings) > 1:
            label += " · +%d more" % (len(bindings) - 1)
        return f"{evidence_type} · {label}"
    # Insight and other task dialects already provide the useful semantic
    # name in ``kind``. Keep that name on the closed card; the full address
    # remains available inside the opened Run details.
    kind = str(row.get("kind", "")).strip()
    if kind and str(row.get("operation", "")).lower() in {"item", "insight"}:
        return _short_text(kind, 100)
    operation = str(row.get("operation", "")).strip()
    if operation:
        return operation.replace("-", " ").title()
    return str(row.get("run_id", "Run"))


def _run_action(row: dict) -> str:
    """Return the one-line activity shown before a card is opened."""
    if row.get("lane") == "page" and row.get("operation") == "interactive-writing":
        if row.get("mode") == "scratch":
            scope = str(row.get("target_scope", "target"))
            target = str(row.get("target", "the Page"))
            return "Capture rough thinking for %s %s" % (scope, target)
        if _is_structure_run(str(row.get("run_id", ""))):
            return "Agree the Page structure and evidence routes"
        target = str(row.get("target", "")).strip()
        return "Review and modify " + (target or "the Page")
    evidence_type = _evidence_type(row)
    if evidence_type:
        run_id = str(row.get("global_id") or row.get("run_id", "")).strip()
        if run_id.startswith("P "):
            run_id = run_id[2:]
        bindings = row.get("evidence_bindings", [])
        suffix = " · %d Evidence Items" % len(bindings) if isinstance(bindings, list) and len(bindings) > 1 else ""
        return "Run %s → Result%s" % (run_id or "not allocated", suffix)
    return _short_text(row.get("outcome") or row.get("target") or _what_happened(row))


def _result_source_files(row: dict, root: Path) -> list[Path]:
    """Resolve only safe, conventional Result payload files for preview."""
    result_path = row.get("result_path") or _repo_path(root, row.get("result", ""))
    if not result_path:
        return []
    if result_path.is_file():
        return [result_path]
    if not result_path.is_dir() or result_path.is_symlink():
        return []
    preferred = []
    if row.get("operation") == "paragraph-writing":
        preferred.extend(("paragraph.md", "result.md"))
    evidence_type = _evidence_type(row)
    if evidence_type == "Display":
        preferred.extend(("display.md", "table.md"))
    elif evidence_type == "Citation":
        preferred.extend(("citation.md", "source.md"))
    preferred.extend(("result.md", "facts.md", "summary.md", "report.md", "result.yaml",
                      "value.yaml", "result.json", "result.csv"))
    files = []
    for name in preferred:
        candidate = result_path / name
        if candidate not in files and _confined_file(candidate, result_path):
            files.append(candidate)
    return files


def _yaml_result_payload(text: str) -> str:
    """Extract the substantive payload from a Result envelope, not its metadata."""
    lines = text.splitlines()
    start = next((index for index, line in enumerate(lines)
                  if re.match(r"^payload:\s*$", line)), None)
    if start is not None:
        payload = []
        for line in lines[start + 1:]:
            if line and not line[0].isspace():
                break
            payload.append(line[2:] if line.startswith("  ") else line)
        value = "\n".join(payload).strip()
        if value:
            return value
    values = []
    for key in ("reader_takeaway", "interpretation", "outcome", "summary"):
        match = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", text, re.M)
        if match:
            values.append(match.group(1).strip().strip("'\""))
    if values:
        return "\n\n".join(values)

    # Small domain Result files such as ``value.yaml`` often contain only
    # substantive fields and therefore have no explicit ``payload`` key.
    # Keep those values visible while filtering the lifecycle envelope.
    metadata = {
        "schema", "run", "global_id", "status", "target", "ticket",
        "result", "runtime", "family", "operation", "interaction",
        "version", "step", "item", "supporting_results",
    }
    fields = []
    for line in lines:
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.+?)\s*$", line)
        if match and match.group(1).lower() not in metadata:
            fields.append(line.strip())
    return "\n".join(fields)


def _render_result_file(path: Path) -> str:
    """Render one safe Result payload as readable HTML."""
    boundary = path.parent
    text = _preview_text(path, boundary)
    if not text:
        return ""
    suffix = path.suffix.lower()
    if suffix == ".md":
        return _markdown_fragment(text)
    if suffix in {".yaml", ".yml"}:
        payload = _yaml_result_payload(text)
        return "<pre>%s</pre>" % html.escape(payload) if payload else ""
    return "<pre>%s</pre>" % html.escape(text.strip())


def _result_preview(row: dict, root: Path) -> str:
    """Show the actual safe Result payload before any Run metadata."""
    for path in _result_source_files(row, root):
        rendered = _render_result_file(path)
        if rendered:
            return '<section class=run-result><h3>Result</h3><div class=run-output>%s</div></section>' % rendered
    if row.get("outcome"):
        return '<section class=run-result><h3>Result</h3><p class=run-output>%s</p></section>' % _inline_markdown(row["outcome"])
    return '<section class="run-result run-result-empty"><h3>Result</h3><p>No Result available yet.</p></section>'


def _what_happened(row: dict) -> str:
    """Give every overview row an honest result-or-state sentence."""
    if row.get("outcome"):
        return row["outcome"]
    prefix = {"Done": "Completed", "Running": "Working on", "Ready": "Planned",
              "Failed": "Failed", "Held": "Needs attention"}.get(row["status"], "Target")
    return f"{prefix} — {row['target']}"


def _version_path(runtime: Path, version: str) -> Path | None:
    """Resolve only the declared single-Markdown Version journal."""
    if not re.fullmatch(r"v[0-9][0-9][0-9]", version):
        return None
    return runtime.parent / f"{version}.md"


def _section_body(text: str, heading: str) -> str:
    hit = re.search(
        rf"^###[ \t]+{re.escape(heading)}[ \t]*$\n(.*?)(?=^###[ \t]+|^##[ \t]+|\Z)",
        text,
        re.M | re.S,
    )
    return hit.group(1).strip() if hit else ""


def _step_section(text: str, step: str) -> str:
    """Return one Step block from a Version journal, without crossing Steps."""
    if not re.fullmatch(r"s[0-9][0-9][0-9]", step):
        return ""
    hit = re.search(
        rf"^##[ \t]+Step[ \t]+{re.escape(step)}(?:[ \t].*)?$\n(.*?)"
        rf"(?=^##[ \t]+(?:Step[ \t]+s[0-9]{{3}}|Version closure)\b|\Z)",
        text,
        re.M | re.S,
    )
    return hit.group(1) if hit else ""


def _inline_markdown(text: str) -> str:
    """Escape inline text while retaining small, readable code spans."""
    parts = text.split("`")
    rendered = []
    for index, part in enumerate(parts):
        escaped = html.escape(part)
        rendered.append(f"<code>{escaped}</code>" if index % 2 else escaped)
    return "".join(rendered)


def _markdown_fragment(text: str) -> str:
    """Render the small Markdown subset used by Page Run journals safely."""
    lines = text.strip().splitlines()
    rendered: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if line.strip().startswith("```"):
            index += 1
            code_lines = []
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code_lines.append(lines[index])
                index += 1
            index += index < len(lines)
            rendered.append("<pre><code>%s</code></pre>" %
                            html.escape("\n".join(code_lines).strip()))
            continue
        if (index + 1 < len(lines) and "|" in line and
                re.fullmatch(r"\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*",
                             lines[index + 1])):
            headers = [cell.strip() for cell in line.strip().strip("|").split("|")]
            index += 2
            rows = []
            while index < len(lines) and "|" in lines[index] and lines[index].strip():
                rows.append([cell.strip() for cell in
                             lines[index].strip().strip("|").split("|")])
                index += 1
            head = "".join(f"<th>{_inline_markdown(cell)}</th>" for cell in headers)
            body = "".join("<tr>%s</tr>" % "".join(
                f"<td>{_inline_markdown(cell)}</td>" for cell in row
            ) for row in rows)
            rendered.append(f"<table class=md-table><thead><tr>{head}</tr></thead>"
                            f"<tbody>{body}</tbody></table>")
            continue
        list_match = re.match(r"^\s*[-*]\s+(.+)$", line)
        if list_match:
            items = []
            while index < len(lines):
                match = re.match(r"^\s*[-*]\s+(.+)$", lines[index])
                if not match:
                    break
                items.append(f"<li>{_inline_markdown(match.group(1))}</li>")
                index += 1
            rendered.append("<ul>%s</ul>" % "".join(items))
            continue
        ordered_match = re.match(r"^\s*\d+[.)]\s+(.+)$", line)
        if ordered_match:
            items = []
            while index < len(lines):
                match = re.match(r"^\s*\d+[.)]\s+(.+)$", lines[index])
                if not match:
                    break
                items.append(f"<li>{_inline_markdown(match.group(1))}</li>")
                index += 1
            rendered.append("<ol>%s</ol>" % "".join(items))
            continue
        heading = re.match(r"^#{1,6}\s+(.+)$", line)
        if heading:
            rendered.append(f"<h4>{_inline_markdown(heading.group(1))}</h4>")
            index += 1
            continue
        if line.lstrip().startswith(">"):
            quote_lines = []
            while index < len(lines) and lines[index].lstrip().startswith(">"):
                quote_lines.append(lines[index].lstrip()[1:].lstrip())
                index += 1
            rendered.append("<blockquote>%s</blockquote>" %
                            _inline_markdown(" ".join(quote_lines)))
            continue
        paragraph = [line.strip()]
        index += 1
        while index < len(lines) and lines[index].strip():
            candidate = lines[index]
            if (candidate.strip().startswith("```") or
                    re.match(r"^\s*(?:[-*]|\d+[.)])\s+", candidate) or
                    re.match(r"^#{1,6}\s+", candidate) or
                    candidate.lstrip().startswith(">") or
                    (index + 1 < len(lines) and "|" in candidate and
                     re.fullmatch(r"\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*",
                                  lines[index + 1]))):
                break
            paragraph.append(candidate.strip())
            index += 1
        rendered.append("<p>%s</p>" % _inline_markdown(" ".join(paragraph)))
    return "".join(rendered)


def _subsection_body(text: str, heading: str) -> str:
    hit = re.search(
        rf"^####[ \t]+{re.escape(heading)}[ \t]*$\n(.*?)(?=^####[ \t]+|^###[ \t]+|^##[ \t]+|\Z)",
        text,
        re.M | re.S,
    )
    return hit.group(1).strip() if hit else ""


def _step_feedback_summary(section: str) -> tuple[str, list[str]]:
    feedback = _section_body(section, "Human feedback")
    request = _subsection_body(feedback, "Original request") or feedback
    interpretations = re.findall(r"^-\s+Agent interpretation:\s*(.+)$", feedback, re.M)
    return request.strip(), [item.strip() for item in interpretations]


def _saved_result_focus(section: str) -> str:
    """Keep the substantive result; omit hashes, checks, and audit bookkeeping."""
    saved = _section_body(section, "Saved result")
    if not saved:
        return ""
    sections = list(re.finditer(r"^####[ \t]+(.+?)[ \t]*$", saved, re.M))
    ignored = {"changes", "checks", "planning snapshot", "track changes",
               "feedback classification"}
    focused = []
    for index, match in enumerate(sections):
        title = match.group(1).strip()
        if title.lower() in ignored:
            continue
        end = sections[index + 1].start() if index + 1 < len(sections) else len(saved)
        body = saved[match.end():end].strip()
        if body:
            focused.append(f"#### {title}\n\n{body}")
    if focused:
        return "\n\n".join(focused)
    # Simple journals may store prose directly beneath Saved result.
    cleaned = re.sub(r"```(?:text)?\s*.*?```", "", saved, flags=re.S)
    cleaned = re.sub(r"^(?:Source after save|State):.*$", "", cleaned,
                     flags=re.M | re.I)
    return cleaned.strip()


def _level_heading_body(text: str, level: int, heading: str) -> str:
    marks = "#" * level
    hit = re.search(
        rf"^{re.escape(marks)}[ \t]+{re.escape(heading)}[ \t]*$\n"
        rf"(.*?)(?=^{re.escape(marks)}[ \t]+|\Z)",
        text,
        re.M | re.S,
    )
    return hit.group(1).strip() if hit else ""


def _token_track_changes(before: str, after: str) -> str:
    """Render one paired span with document-like lexical replacements."""
    # Bind leading space to its lexical token. Treating whitespace as an
    # independent match makes a replaced phrase alternate old/new word by word,
    # which is technically granular but visually unlike document Track Changes.
    token = re.compile(r"\s*(?:[\w]+(?:['’\-][\w]+)*|[^\w\s])", re.UNICODE)
    old = token.findall(before.strip())
    new = token.findall(after.strip())
    output = []
    for operation, a1, a2, b1, b2 in difflib.SequenceMatcher(
            None, old, new, autojunk=False).get_opcodes():
        old_text = html.escape("".join(old[a1:a2]))
        new_text = html.escape("".join(new[b1:b2]))
        if operation == "equal":
            output.append(old_text)
        elif operation == "delete":
            output.append(f"<del>{old_text}</del>")
        elif operation == "insert":
            output.append(f"<ins>{new_text}</ins>")
        else:
            output.append(f"<del>{old_text}</del><ins>{new_text}</ins>")
    return "".join(output)


def _track_sentences(value: str) -> list[str]:
    """Keep sentence whitespace so inserted/deleted sentences read naturally."""
    return [match.group(0) for match in re.finditer(
        r".*?(?:[。！？]+|[.!?]+(?=\s|$))(?:\s+|$)|.+$", value.strip(), re.S
    ) if match.group(0)]


def _sentence_similarity(left: str, right: str) -> float:
    token = re.compile(r"[\w]+(?:['’\-][\w]+)*|[^\w\s]", re.UNICODE)
    matcher = difflib.SequenceMatcher(
        None, token.findall(left.lower()), token.findall(right.lower()),
        autojunk=False,
    )
    longest_anchor = max((block.size for block in matcher.get_matching_blocks()),
                         default=0)
    return longest_anchor + matcher.ratio()


def _word_track_changes(before: str, after: str) -> str:
    """Render safe Track Changes: whole sentences, then word-level edits."""
    old_sentences = _track_sentences(before)
    new_sentences = _track_sentences(after)
    if len(old_sentences) == 1 and len(new_sentences) > 1:
        paired = max(range(len(new_sentences)),
                     key=lambda index: _sentence_similarity(
                         old_sentences[0], new_sentences[index]))
        if _sentence_similarity(old_sentences[0], new_sentences[paired]) >= 1.3:
            return "".join(
                _token_track_changes(old_sentences[0], sentence)
                if index == paired else f"<ins>{html.escape(sentence)}</ins>"
                for index, sentence in enumerate(new_sentences)
            )
    if len(new_sentences) == 1 and len(old_sentences) > 1:
        paired = max(range(len(old_sentences)),
                     key=lambda index: _sentence_similarity(
                         old_sentences[index], new_sentences[0]))
        if _sentence_similarity(old_sentences[paired], new_sentences[0]) >= 1.3:
            return "".join(
                _token_track_changes(sentence, new_sentences[0])
                if index == paired else f"<del>{html.escape(sentence)}</del>"
                for index, sentence in enumerate(old_sentences)
            )
    return _token_track_changes(before, after)


def _track_change_html(section: str) -> str:
    saved = _section_body(section, "Saved result")
    track_section = _subsection_body(saved, "Track changes")
    matches = list(re.finditer(r"^#####[ \t]+(.+?)[ \t]*$", track_section, re.M))
    cards = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(track_section)
        body = track_section[match.end():end].strip()
        before = _level_heading_body(body, 6, "Before")
        after = _level_heading_body(body, 6, "After")
        # A Track Changes card represents an actual text transition. Lifecycle,
        # navigation, and presenter-only feedback belongs in the ordinary
        # Changes record and must not create an empty visual diff.
        if not before or not after or before == after:
            continue
        why = _level_heading_body(body, 6, "Why")
        preference = _level_heading_body(body, 6, "Inferred preference")
        analysis = _level_heading_body(body, 6, "Analysis status")
        status = _level_heading_body(body, 6, "Preference status")
        title = match.group(1).strip()
        title_parts = [part.strip() for part in title.split("·", 1)]
        identifier = title_parts[0]
        feedback_match = re.fullmatch(r"F0*(\d+)", identifier, re.I)
        display_identifier = (
            f"Feedback {int(feedback_match.group(1))}"
            if feedback_match else identifier
        )
        kind = title_parts[1] if len(title_parts) > 1 else "Unclassified change"
        cards.append(
            '<section class=track-card><h4>%s</h4><p class=track-kind>%s</p>'
            '<div class=track-legend><span class=removed>Deleted</span>'
            '<span class=added>Added</span></div><div class=track-diff>%s</div>%s%s%s%s</section>' % (
                html.escape(display_identifier), html.escape(kind),
                _word_track_changes(before, after),
                ('<p class=why><b>Why</b><br>%s</p>' % _inline_markdown(why)) if why else "",
                ('<p class=preference><b>Inferred preference</b><br>%s</p>' %
                 _inline_markdown(preference)) if preference else "",
                ('<p class=track-status>%s</p>' % _inline_markdown(status)) if status else "",
                ('<p class=track-status><b>Analysis</b><br>%s</p>' %
                 _inline_markdown(analysis)) if analysis else "",
            )
        )
    return "".join(cards)


def _working_field(text: str, label: str) -> str:
    hit = re.search(rf"^{re.escape(label)}:[ \t]*(.+)$", text, re.M | re.I)
    return hit.group(1).strip() if hit else ""


def _meta_grid(fields: list[tuple[str, str, bool]]) -> str:
    return "<dl class=run-meta>%s</dl>" % "".join(
        '<div%s><dt>%s</dt><dd>%s</dd></div>' %
        (' class=wide' if wide else "", html.escape(label), value)
        for label, value, wide in fields
    )


def _mermaid_run_visual(page_src: Path, row: dict) -> str:
    """Reuse the Page's deterministic Mermaid renderer for the structure Run."""
    if not _is_structure_run(str(row.get("run_id", ""))):
        return ""
    logic = page_src.parent / "outline" / f"{page_src.stem}-logic.mmd"
    source = _preview_text(logic, logic.parent)
    if not source:
        return '<p class=note>The Mermaid Structure source is not available.</p>'
    try:
        from live.outline import _logic_svg
        figure = _logic_svg(source, min_width=420)
    except (ImportError, ValueError) as exc:
        return '<p class=note>The Mermaid Structure cannot be rendered: %s.</p>' % html.escape(str(exc))
    nodes: dict[str, str] = {}
    order: list[str] = []
    outgoing: dict[str, list[str]] = {}
    for raw in source.splitlines():
        line = raw.strip()
        node = re.fullmatch(
            r'([A-Za-z][A-Za-z0-9_-]*)\s*\[\s*"((?:\\.|[^"])*)"\s*\]', line
        )
        if node:
            key, label = node.groups()
            if key not in nodes:
                order.append(key)
            nodes[key] = re.sub(r"<br\s*/?>", " — ", label).replace(r"\n", " ")
            continue
        edge = re.fullmatch(
            r'([A-Za-z][A-Za-z0-9_-]*)\s*-->\s*'
            r'(?:\|"((?:\\.|[^"])*)"\|\s*)?([A-Za-z][A-Za-z0-9_-]*)', line
        )
        if edge:
            start, label, _end = edge.groups()
            outgoing.setdefault(start, []).append(label or "continues to the next point")
    flow = "<ol class=logic-steps>%s</ol>" % "".join(
        "<li><b>%s</b>%s</li>" %
        (_inline_markdown(nodes[key]), "".join(
            "<span>↓ %s</span>" % _inline_markdown(label)
            for label in outgoing.get(key, [])
        )) for key in order
    )
    return (
        '<div class=run-logic><h4>Argument flow</h4>'
        '<div class=run-logic-viewport tabindex=0 aria-label="Scrollable Mermaid Structure">'
        '<div class=run-logic-canvas>%s</div></div>%s</div>' % (figure, flow)
    )


def _scratch_run_detail(row: dict, root: Path, page_src: Path) -> str:
    """Show a Scratch Result as summary first, raw notes second."""
    chunks = [
        '<div class=detail-head><span class=detail-title>%s</span></div>' %
        html.escape(_run_name(row)),
    ]
    summary = str(row.get("summary", "")).strip()
    raw = ""
    if row.get("runtime"):
        version = row.get("version", "") or "v001"
        journal = _version_path(row["runtime"], version)
        text = _preview_text(journal, row["runtime"].parent) if journal else ""
        summary = (_level_heading_body(text, 4, "Summary") or summary).strip()
        raw = _level_heading_body(text, 4, "Raw scratch").strip()
    result = _markdown_fragment(summary) if summary else "<p>No Summary yet.</p>"
    chunks.append('<section class=run-result><h3>Summary</h3><div class=run-output>%s</div></section>' % result)
    if raw:
        chunks.append('<details class=run-context><summary>Raw Scratch</summary><div class=run-output>%s</div></details>' %
                      _markdown_fragment(raw))
    technical = [
        ("Target", html.escape("%s · %s" % (
            row.get("target_scope", "target"), row.get("target", "")))),
        ("Run record", _linked(row.get("ticket"), label=_shown_path(row.get("ticket"), root))),
        ("Result folder", _linked(row.get("result_path"), label=_shown_path(row.get("result_path"), root))),
    ]
    chunks.append('<details class=technical><summary>Technical details</summary><dl>%s</dl></details>' %
                  "".join("<dt>%s</dt><dd>%s</dd>" % (html.escape(label), value)
                          for label, value in technical))
    return "<div class=detailbox>%s</div>" % "".join(chunks)


def _page_run_detail(row: dict, root: Path, page_src: Path) -> str:
    """Reader-first Page Run detail: Result first, history and metadata later."""
    chunks = [
        '<div class=detail-head><span class=detail-title>%s</span></div>' %
        html.escape(_run_name(row)),
    ]
    earlier_steps: list[tuple[str, str, str, str]] = []
    working_text = ""
    current_request = ""
    current_interpretations: list[str] = []
    current_result = ""
    current_track_changes = ""
    if row.get("runtime"):
        directory = row["runtime"].parent
        findings = _interactive_findings(row["runtime"], row)
        if findings:
            chunks.append("<p class=note>History integrity finding: missing %s.</p>" %
                          html.escape(", ".join(findings)))
        working_text = _preview_text(directory / "working.md", directory)
        current_key = (row.get("version", ""), row.get("step", ""))
        for path in sorted(directory.glob("v[0-9][0-9][0-9].md")):
            if not _confined_file(path, directory):
                continue
            version_text = _preview_text(path, directory)
            for step_id in re.findall(r"^##[ \t]+Step[ \t]+(s[0-9]{3})", version_text, re.M):
                section = _step_section(version_text, step_id)
                request, interpretations = _step_feedback_summary(section)
                result = _saved_result_focus(section)
                track_changes = _track_change_html(section)
                if (path.stem, step_id) == current_key:
                    current_request = request
                    current_interpretations = interpretations
                    current_result = result
                    current_track_changes = track_changes
                else:
                    earlier_steps.append((f"{path.stem}/{step_id}", request, result,
                                          track_changes))
    else:
        chunks.append("<p class=note>This Page Run has no current lifecycle projection.</p>")

    visual = _mermaid_run_visual(page_src, row)
    result_body = (visual + _markdown_fragment(current_result) + current_track_changes
                   if current_result else "")
    if result_body:
        chunks.append('<section class=run-result><h3>Result</h3><div class=run-output>%s</div></section>' % result_body)
    else:
        chunks.append('<section class="run-result run-result-empty"><h3>Result</h3><p>No Result available yet.</p></section>')

    next_action = _working_field(working_text, "Next")
    if current_request or next_action:
        context = []
        if current_request:
            context.append("<h4>Review input</h4>%s" % _markdown_fragment(current_request))
        if current_interpretations:
            context.append("<h4>Interpretation</h4><ul>%s</ul>" % "".join(
                f"<li>{_inline_markdown(item)}</li>" for item in current_interpretations
            ))
        if next_action:
            context.append("<h4>Next</h4>%s" % _inline_markdown(next_action))
        chunks.append("<details class=run-context><summary>Review context</summary>%s</details>" %
                      "".join(context))
    if earlier_steps:
        entries = []
        for label, request, result, track_changes in reversed(earlier_steps):
            body = (("<h4>Review input</h4>%s" % _markdown_fragment(request)) if request else "")
            body += (("<h4>Result</h4>%s" % _markdown_fragment(result)) if result else "")
            body += track_changes
            entries.append("<details class=step-history><summary>%s</summary>%s</details>" %
                           (html.escape(label), body or "<p>No readable summary recorded.</p>"))
        chunks.append("<details class=history><summary>Earlier results · %d</summary>%s</details>" %
                      (len(entries), "".join(entries)))

    technical = [
        ("Run record", _linked(row.get("ticket"),
                                label=_shown_path(row.get("ticket"), root))),
        ("Result folder", _linked(row.get("result_path"),
                                   label=_shown_path(row.get("result_path"), root))),
    ]
    technical_html = "<dl>%s</dl>" % "".join(
        "<dt>%s</dt><dd>%s</dd>" % (html.escape(label), value)
        for label, value in technical
    )
    if row.get("refs"):
        technical_html += "<h4>Evidence bindings</h4><ul class=refs>%s</ul>" % "".join(
            "<li><code>%s</code></li>" % html.escape(ref) for ref in row["refs"]
        )
    if _is_structure_run(str(row.get("run_id", ""))):
        collaboration = (
            row.get("participants") or "not supplied",
            row.get("coordinator") or "not supplied",
            row.get("contributors") or "current Step not supplied",
        )
        technical_html += (
            "<h4>Collaboration</h4><dl>"
            "<dt>Participants</dt><dd><code>%s</code></dd>"
            "<dt>Coordinator</dt><dd><code>%s</code></dd>"
            "<dt>Step contributors</dt><dd><code>%s</code></dd>"
            "</dl>" % tuple(html.escape(value) for value in collaboration)
        )
    for finding in row.get("audit", []):
        technical_html += "<p class=note>Run audit finding: %s.</p>" % html.escape(finding)
    chunks.append("<details class=technical><summary>Technical details</summary>%s</details>" %
                  technical_html)
    return "<div class=detailbox>%s</div>" % "".join(chunks)


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


def _status(runtime: Path | None, fields: dict[str, str]) -> str:
    if runtime is None:
        return "Held" if _writing_operation(fields) else "Ready"
    status = fields.get("status", "").lower()
    if status in {"planned", "ticket", "queued"}:
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
    if status in {"complete", "completed", "done"}:
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
        return "Done" if has_output else "Held"
    return "Held"


def _ticket_files(runs_dir: Path) -> list[Path]:
    if not runs_dir.is_dir():
        return []
    return [path for path in sorted(runs_dir.rglob("*"))
            if _confined_file(path, runs_dir) and path.suffix in _TICKET_SUFFIXES
            and _TICKET_NAME.match(path.name) and not path.name.startswith(".")]


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
        if not _confined_file(candidate, results_dir):
            continue
        fields = _fields(candidate)
        if fields.get("ticket") in {rel_text, ticket.name, str(ticket)}:
            return candidate
    return None


def _task_context(page_src: Path):
    """Return the Task adapter record and containing Job for a Task Page."""
    if len(page_src.parents) < 3:
        return None, None
    block = page_src.parents[2]
    info = task_page_info(block, page_src)
    return (info, page_src.parents[1]) if info else (None, None)


def _fallback_result(runtime: Path | None, base: Path) -> str:
    if runtime is None:
        return ""
    try:
        return str(runtime.parent.relative_to(base))
    except ValueError:
        return str(runtime.parent)


def _evidence_refs(page_src: Path, *, run_id: str, ticket: Path) -> list[str]:
    """Return Evidence Items only when their ledger has named this local run."""
    compact = compact_paper_run(run_id) or compact_global_run(run_id)
    needles = {run_id, ticket.name, str(ticket.relative_to(page_src.parent))}
    if compact:
        needles.update({compact, readable_paper_route(compact), readable_global_run(compact)})
    refs = []
    for item in read_items(page_src).values():
        declared = " ".join((item.get("local_run", ""), item.get("result", "")))
        if any(needle and needle in declared for needle in needles):
            refs.append(item["item"])
    return refs


def _sort_key(row: dict) -> tuple:
    """Order active/recovery work first, then newer Run numbers."""
    numbers = re.findall(
        r"(?:r(?:p|l|i|d)?|rp-(?:struct|sec|para)-|re-(?:value|display|cite)-|rd)(\d+)",
        row.get("run_id", ""),
        re.I,
    )
    newest = -int(numbers[-1]) if numbers else 0
    return _STATE_ORDER.get(row["status"], 9), newest, row["run_id"]


def local_runs(page_src: Path) -> list[dict]:
    """Read allocated Folder-local or Job-backed Task Run pairs."""
    page_dir = page_src.parent
    instance_rows = (_insight_runs(page_src) if (page_dir / "workflow/insight.yaml").is_file() else [])
    item_tickets = {row["ticket"] for row in instance_rows}
    task_info, job_dir = _task_context(page_src)
    runs_dir = page_dir / "runs"
    if task_info:
        results_dir = job_dir / "results" / page_dir.name
        result_base = job_dir
    else:
        results_dir = page_dir / "results"
        result_base = page_dir
    rows = list(instance_rows)
    paired_runtimes = {row["runtime"] for row in rows if row.get("runtime")}
    for ticket in _ticket_files(runs_dir):
        if ticket in item_tickets:
            continue
        runtime = _runtime_for(ticket, runs_dir, results_dir)
        if runtime:
            paired_runtimes.add(runtime)
        fields = _fields(runtime)
        ticket_fields = _fields(ticket) if ticket.suffix.lower() in {".md", ".yaml", ".yml"} else {}
        for key in ("target", "family", "operation", "interaction", "mode", "version", "step",
                    "participants", "coordinator", "contributors"):
            fields[key] = fields.get(key) or ticket_fields.get(key, "")
        if not fields.get("operation") and re.fullmatch(r"r\d+_page-writing_c\d+-p\d+", ticket.stem):
            fields["operation"] = "paragraph-writing"
        if not fields.get("operation") and _valid_page_run_id(ticket.stem):
            fields.update({"family": fields.get("family") or "page",
                           "operation": "interactive-writing",
                           "interaction": fields.get("interaction") or "human-feedback"})
        is_page_run = _is_page_run(fields)
        audit = []
        retired_design = bool(re.fullmatch(
            r"r[0-9]{2,}_design_(?:generate|verify)_[a-z0-9][a-z0-9_-]*",
            ticket.stem,
        ))
        if retired_design:
            audit.append("retired Design Run identity is unsupported")
        if is_page_run and fields.get("run") and fields["run"] != ticket.stem:
            audit.append("runtime Run identity does not match the authored Run record")
        kind = ("Interactive writing" if fields.get("operation") == "interactive-writing"
                else "Paragraph writing" if fields.get("operation") == "paragraph-writing"
                else fields.get("operation") or fields.get("family") or "Task")
        if task_info:
            compact = (compact_global_run(fields.get("global_id", ""))
                       or compact_global_run(ticket.stem))
            local_run = re.match(r"^(r\d{2})(?:_|$)", ticket.stem, re.I)
            if not compact and local_run:
                compact = f"{task_info['id']}{local_run.group(1).lower()}"
            global_id = readable_global_run(compact) if compact else ticket.stem
            run_id = global_id
        elif (fields.get("family") == "design" or
              re.fullmatch(r"rd[0-9]{2,}_(?:generate|verify)_[a-z0-9][a-z0-9_-]*",
                           ticket.stem)):
            # Design uses its stable Folder address, never a fabricated Paper
            # or b/j/t identity. Its YAML Ticket is already a supported suffix.
            compact = ""
            global_id = fields.get("global_id") or f"{page_dir.as_posix()}#{ticket.stem}"
            run_id = ticket.stem
            if fields.get("family") == "design" and not re.fullmatch(
                    r"rd[0-9]{2,}_(?:generate|verify)_[a-z0-9][a-z0-9_-]*",
                    ticket.stem):
                audit.append("invalid current Design Run identity")
        elif retired_design:
            compact = ""
            global_id = ticket.stem
            run_id = ticket.stem
        else:
            paper_id = (compact_paper_run(fields.get("global_id", ""))
                        or compact_paper_run(ticket.stem))
            compact = (paper_id or compact_global_run(fields.get("global_id", ""))
                       or compact_global_run(ticket.stem))
            # The Paper Board is the local block. This view omits an inherited
            # ``bNN`` prefix, while ledger and receipt retain it for global lookup.
            global_id = (paper_id or readable_global_run(compact)) if compact else ticket.stem
            relative_id = readable_paper_route(compact) if compact else ""
            if ((page_dir / "page.toml").is_file()
                    or (page_dir / "workflow/insight.yaml").is_file()) and not compact:
                run_id = ticket.stem
            else:
                run_id = "P " + (relative_id or ticket.stem)
        if is_page_run:
            run_id = ticket.stem
        rows.append({
            "run_id": run_id,
            "global_id": global_id,
            "compact_id": compact,
            "ticket": ticket,
            "runtime": runtime,
            "result_path": runtime.parent if runtime else None,
            "result": fields.get("result", "") or _fallback_result(runtime, result_base),
            "target": fields.get("target", "") or "page-local work",
            "outcome": _result_outcome(runtime, fields),
            "kind": kind,
            "origin": "Task Job" if task_info else "Local",
            "lane": "page" if is_page_run else "task",
            "family": fields.get("family", "") or "Task",
            "operation": fields.get("operation", ""),
            "version": fields.get("version", ""),
            "step": fields.get("step", ""),
            "mode": fields.get("mode", ""),
            "target_scope": fields.get("target_scope", ""),
            "participants": fields.get("participants", ""),
            "coordinator": fields.get("coordinator", ""),
            "contributors": fields.get("contributors", ""),
            "goal": _ticket_note(ticket, "Goal"),
            "status": "Held" if audit else _status(runtime, fields),
            "audit": audit,
            "refs": _evidence_refs(
                page_src,
                run_id=global_id,
                ticket=ticket,
            ),
        })
    for runtime in (sorted(results_dir.rglob("runtime.yaml"))
                    if results_dir.is_dir() else []):
        if runtime in paired_runtimes or not _confined_file(runtime, results_dir):
            continue
        fields = _fields(runtime)
        is_page_run = _is_page_run(fields)
        stem = runtime.parent.name
        rows.append({
            "run_id": stem if is_page_run else f"P {stem}",
            "global_id": fields.get("global_id") or stem,
            "compact_id": compact_global_run(fields.get("global_id", "")),
            "ticket": None,
            "runtime": runtime,
            "result_path": runtime.parent,
            "result": fields.get("result", "") or _fallback_result(runtime, result_base),
            "target": fields.get("target", "") or "orphan Result",
            "outcome": _result_outcome(runtime, fields),
            "kind": ("Interactive writing" if fields.get("operation") == "interactive-writing"
                     else fields.get("operation") or fields.get("family") or "Task"),
            "lane": "page" if is_page_run else "task",
            "origin": "Task Job" if task_info else "Local",
            "family": fields.get("family", "") or "Task",
            "operation": fields.get("operation", ""),
            "version": fields.get("version", ""),
            "step": fields.get("step", ""),
            "mode": fields.get("mode", ""),
            "target_scope": fields.get("target_scope", ""),
            "participants": fields.get("participants", ""),
            "coordinator": fields.get("coordinator", ""),
            "contributors": fields.get("contributors", ""),
            "goal": "",
            "status": "Held",
            "refs": [],
            "orphan": True,
            "audit": ["Result exists without its authored Run record"],
        })
    base_children = {}
    for relation in instance_rows:
        base = relation.get("base_run", "")
        if base:
            base_children.setdefault(base, []).append(relation["run_id"])
    for row in rows:
        children = base_children.get(row.get("global_id", ""), [])
        if children:
            row["kind"] = "Base Task Run"
            row["outcome"] = "Reusable method for " + ", ".join(children)
    _audit_page_run_order(rows)
    rows.extend(_labeling_runs(page_src))
    return sorted(rows, key=_sort_key)


def _labeling_runs(page_src: Path) -> list[dict]:
    """Project the page-local Labeling dialect into the Task Run lane.

    Labeling keeps its Ticket and Result beneath ``labeling/``.  The generic
    presenter reads only the safe envelope; domain artifacts remain owned by
    the Labeling plugin and never become previews here.
    """
    job = page_src.parent / "labeling"
    runs_dir = job / "runs"
    results_dir = job / "results"
    if not runs_dir.is_dir() and not results_dir.is_dir():
        return []
    rows = []
    paired = set()
    for ticket in _ticket_files(runs_dir):
        runtime = _runtime_for(ticket, runs_dir, results_dir)
        if runtime:
            paired.add(runtime)
        fields = _fields(runtime)
        ticket_fields = _fields(ticket)
        for key in ("run", "status", "target", "result", "family", "operation",
                    "outcome", "summary"):
            fields[key] = fields.get(key) or ticket_fields.get(key, "")
        audit = []
        declared = fields.get("run")
        if declared and declared != ticket.stem:
            audit.append("runtime Run identity does not match the authored Run record")
        rows.append({
            "run_id": ticket.stem,
            "global_id": ticket.stem,
            "compact_id": ticket.stem,
            "ticket": ticket,
            "runtime": runtime,
            "result_path": runtime.parent if runtime else None,
            "result": fields.get("result", "") or _fallback_result(runtime, job),
            "target": fields.get("target", "") or "labeling operation",
            "outcome": fields.get("outcome", "") or fields.get("summary", ""),
            "kind": fields.get("operation", "") or "Labeling",
            "origin": "Local",
            "lane": "task",
            "family": "Labeling",
            "operation": fields.get("operation", ""),
            "version": "", "step": "", "goal": "", "refs": [],
            "status": "Held" if audit else _status(runtime, fields),
            "audit": audit,
        })
    for runtime in sorted(results_dir.glob("*/runtime.yaml")) if results_dir.is_dir() else []:
        if runtime in paired or not _confined_file(runtime, results_dir):
            continue
        fields = _fields(runtime)
        rows.append({
            "run_id": runtime.parent.name, "global_id": runtime.parent.name,
            "compact_id": runtime.parent.name, "ticket": None, "runtime": runtime,
            "result_path": runtime.parent,
            "result": fields.get("result", "") or _fallback_result(runtime, job),
            "target": fields.get("target", "") or "orphan Labeling Result",
            "outcome": fields.get("outcome", "") or fields.get("summary", ""),
            "kind": fields.get("operation", "") or "Labeling",
            "origin": "Local", "lane": "task", "family": "Labeling",
            "operation": fields.get("operation", ""), "version": "", "step": "",
            "goal": "", "refs": [], "status": "Held", "orphan": True,
            "audit": ["Result exists without its authored Run record"],
        })
    return rows


def _insight_runs(page_src: Path) -> list[dict]:
    """The instance dialect has one ticket and several explicit executions."""
    from src.insight_instances import contract
    api = contract()
    try:
        manifest, items, errors = api.inspect(page_src.parent)
    except (OSError, ValueError, TypeError, KeyError, AttributeError, api.yaml.YAMLError):
        return []  # the Outline item table displays the validation failure
    rows = []
    for item in items:
        if not item["ticket"]:
            continue  # proposed items are not allocated Runs
        run = item["item"]["run"]
        base_run = item["item"].get("base_run", {}).get("id", "")
        datasets = ", ".join(item["item"].get("datasets", []))
        target_rung = item["item"].get("target", "")
        ticket = api.item_ticket(page_src.parent, item["item"])
        for info in item["versions"] or [None]:
            ident = info["execution"] if info else f"{manifest['instance']}#{run}"
            directory = page_src.parent / "results" / run / info["version"] if info else None
            status = "Ready"
            if info:
                status = {"planned": "Ready", "running": "Running", "complete": "Done",
                          "failed": "Failed", "blocked": "Held"}.get(info["status"], "Held")
                if not info["valid"] or info["stale"]:
                    status = "Held"
            result_file = directory / "result.yaml" if directory else None
            has_result = bool(result_file and result_file.is_file())
            binding_state = ((info.get("status", "").capitalize() + " binding · ")
                             if info else "Binding · ")
            rows.append({"run_id": ident, "global_id": ident, "compact_id": ident if info else "",
                         "ticket": ticket, "runtime": directory / "runtime.yaml" if directory else None,
                         "result_path": result_file if has_result else None,
                         "result": str(result_file) if has_result else "",
                         "target": item["item"].get("question", ""), "status": status,
                         "outcome": (f"{binding_state}binds {base_run} to {datasets}" if base_run else ""),
                         "origin": "Local", "lane": "task", "family": "Insight",
                         "kind": (f"Insight · RI · {target_rung.title()}"
                                  if base_run else "Insight"),
                         "operation": "item", "version": info["version"] if info else "",
                         "step": "", "goal": "", "base_run": base_run,
                         "refs": _evidence_refs(page_src, run_id=ident, ticket=ticket)})
    return sorted(rows, key=_sort_key)


def _linked(path: Path | None, *, label: str) -> str:
    """Show an exact selectable path without opening or downloading it."""
    if path is None:
        return "—"
    return '<code class=repo-path>%s</code>' % html.escape(label)


def _shown_path(path: Path | None, root: Path) -> str:
    if path is None:
        return "—"
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path.resolve())


def _repo_path(root: Path, value: str) -> Path | None:
    """Resolve a registry pointer only for display; never follow it for preview."""
    if not value:
        return None
    path = Path(value)
    return path if path.is_absolute() else root / path


def _registry_status(record: dict[str, str]) -> str:
    status = record.get("status", "").lower()
    if status in {"complete", "completed", "done", "historical"}:
        return "Done"
    if status in {"running", "started"}:
        return "Running"
    if status in {"failed", "error"}:
        return "Failed"
    if status in {"blocked", "held", "rerun", "incomplete"}:
        return "Held"
    return "Ready"


def _result_supporting_refs(page_src: Path) -> list[dict[str, str]]:
    """Read external Supporting Runs from local Evidence Result manifests."""
    result_root = page_src.parent / "results"
    if not result_root.is_dir() or result_root.is_symlink():
        return []
    rows = []
    for manifest in sorted(result_root.rglob("result.yaml")):
        if manifest.is_symlink():
            continue
        try:
            manifest.resolve().relative_to(result_root.resolve())
            text = manifest.read_text(encoding="utf-8", errors="replace")
        except (OSError, ValueError):
            continue
        item_match = re.search(r"(?mi)^item:\s*([^#\n]+)", text)
        item_id = item_match.group(1).strip().strip("'\"") if item_match else ""
        if not re.fullmatch(
            r"E\d+-(?:VALUE|TABLE|CITE|DISPLAY)-[a-z0-9-]+", item_id, re.I
        ):
            continue
        in_supporting = False
        current = None
        for raw in text.splitlines():
            if raw.strip() == "supporting_results:":
                in_supporting = True
                continue
            if (in_supporting and raw and not raw[0].isspace()
                    and not re.match(r"^-\s+run:\s*", raw)):
                break
            if not in_supporting:
                continue
            run_match = re.match(r"^\s*-\s+run:\s*([^#\n]+)", raw)
            if run_match:
                if current:
                    rows.append(current)
                current = {"run": run_match.group(1).strip().strip("'\""),
                           "item": item_id, "kind": "Task", "result": "",
                           "runtime": ""}
                continue
            field_match = re.match(r"^\s+(kind|result|runtime):\s*([^#\n]+)", raw)
            if current and field_match:
                current[field_match.group(1)] = field_match.group(2).strip().strip("'\"")
        if current:
            rows.append(current)
    return rows


def supporting_task_runs(page_src: Path) -> list[dict]:
    """Project allocated Supporting Runs as Task Runs without execution internals."""
    root = repo_root(page_src.parent)
    registry = run_registry(str(root))
    by_id: dict[str, dict] = {}
    for item in read_items(page_src).values():
        declared = item.get("supporting_runs", "")
        if declared == "[]":
            continue
        for entry in (part.strip() for part in declared.split(";") if part.strip()):
            parts = [part.strip() for part in entry.split("·")]
            if len(parts) < 3 or parts[1].lower() not in {"reuse", "rerun", "registered"}:
                continue
            compact = compact_global_run(parts[2])
            if not compact:
                continue
            record = registry.get(compact, {})
            declared_result = _repo_path(root, record.get("result", ""))
            result_path = declared_result if _existing_path(declared_result) else None
            status = _registry_status(record) if record else "Held"
            if status == "Done" and result_path is None:
                status = "Held"
            row = by_id.setdefault(compact, {
                "run_id": readable_global_run(compact) or parts[2],
                "global_id": readable_global_run(compact) or parts[2],
                "compact_id": compact,
                "ticket": _repo_path(root, record.get("ticket", "")),
                "runtime": _repo_path(root, record.get("runtime", "")),
                "result_path": result_path,
                "result": record.get("result", "") if result_path else "",
                "target": record.get("target", "") or item.get("target", "")
                          or "unresolved supporting run",
                "outcome": record.get("outcome", "") or record.get("summary", ""),
                "kind": record.get("family", "") or parts[0] or "Task",
                "origin": "Linked",
                "family": record.get("family", "") or parts[0] or "Task",
                "lane": "task",
                "operation": "",
                "version": "",
                "step": "",
                "goal": "",
                "status": status,
                "refs": [],
            })
            if item["item"] not in row["refs"]:
                row["refs"].append(item["item"])
    for source in _result_supporting_refs(page_src):
        compact = compact_global_run(source["run"])
        if not compact:
            continue
        record = registry.get(compact, {})
        declared_result = _repo_path(root, source.get("result", "") or record.get("result", ""))
        result_path = declared_result if _existing_path(declared_result) else None
        runtime = _repo_path(root, source.get("runtime", "") or record.get("runtime", ""))
        ticket = _repo_path(root, record.get("ticket", ""))
        row = by_id.setdefault(compact, {
            "run_id": readable_global_run(compact) or source["run"],
            "global_id": readable_global_run(compact) or source["run"],
            "compact_id": compact,
            "ticket": ticket,
            "runtime": runtime,
            "result_path": result_path,
            "result": source.get("result", "") if result_path else "",
            "target": record.get("target", "") or "Supporting Evidence Result",
            "outcome": record.get("outcome", "") or record.get("summary", ""),
            "kind": source.get("kind", "") or record.get("family", "") or "Task",
            "origin": "Linked",
            "family": source.get("kind", "") or record.get("family", "") or "Task",
            "lane": "task", "operation": "", "version": "", "step": "",
            "goal": "", "status": "Done" if result_path else "Held", "refs": [],
        })
        if source["item"] not in row["refs"]:
            row["refs"].append(source["item"])
        if result_path and not row.get("result_path"):
            row["result_path"] = result_path
            row["result"] = source.get("result", "")
            row["status"] = "Done"
    return sorted(by_id.values(), key=_sort_key)


def run_inventory(page_src: Path) -> list[dict]:
    """Return the two-lane Page projection, deduplicated by native Run identity."""
    rows = local_runs(page_src)
    by_id = {}
    for row in rows:
        key = row.get("compact_id") or row["global_id"]
        if key in by_id:
            finding = "duplicate native Run identity"
            for duplicate in (by_id[key], row):
                duplicate["status"] = "Held"
                duplicate.setdefault("audit", []).append(finding)
        else:
            by_id[key] = row
    for row in supporting_task_runs(page_src):
        key = row.get("compact_id") or row["global_id"]
        if key in by_id:
            for ref in row["refs"]:
                if ref not in by_id[key]["refs"]:
                    by_id[key]["refs"].append(ref)
            continue
        rows.append(row)
        by_id[key] = row
    _attach_evidence_bindings(page_src, rows)
    return sorted(rows, key=lambda row: (row.get("lane") != "page",) + _sort_key(row))


def _detail(row: dict, root: Path, page_src: Path) -> str:
    if row.get("lane") == "page" and row.get("operation") == "interactive-writing":
        if row.get("mode") == "scratch":
            return _scratch_run_detail(row, root, page_src)
        return _page_run_detail(row, root, page_src)
    # The first thing in every non-interactive detail is the actual Result.
    # Ownership and record metadata remain available below the fold.
    chunks = [
        '<div class=detail-head><span class=detail-title>%s</span></div>' %
        html.escape(_run_name(row)),
        _result_preview(row, root),
        _run_label_summary(row),
    ]
    for finding in row.get("audit", []):
        chunks.append("<p class=note>Run audit finding: %s.</p>" % html.escape(finding))
    if row.get("operation") == "paragraph-writing":
        if row["runtime"] is None:
            chunks.append("<p class=note>Missing runtime.yaml: this writing Run has no lifecycle receipt.</p>")
        if row.get("ticket"):
            prompt = _preview_text(row["ticket"], row["ticket"].parent)
            if prompt:
                chunks.append("<details class=run-context><summary>Prompt</summary><pre class=run-preview>%s</pre></details>" %
                              html.escape(prompt))
        if row.get("runtime"):
            trace = _preview_text(row["runtime"].parent / "trace.md", row["runtime"].parent)
            if trace:
                chunks.append("<details class=run-context><summary>Trace</summary><pre class=run-preview>%s</pre></details>" %
                              html.escape(trace))
    context = []
    if row.get("refs"):
        context.append("<h4>Evidence bindings</h4><ul class=refs>%s</ul>" % "".join(
            "<li><code>%s</code></li>" % html.escape(ref) for ref in row["refs"]
        ))
    result_path = row.get("result_path") or _repo_path(root, row.get("result", ""))
    if result_path:
        context.append("<h4>Result source</h4><code class=repo-path>%s</code>" %
                       html.escape(_shown_path(result_path, root)))
    if context:
        chunks.append("<details class=technical><summary>Run details</summary>%s</details>" %
                      "".join(context))
    return "<div class=detailbox>%s</div>" % "".join(chunks)


def _scripts(page_src: Path, root: Path) -> str:
    """Render a collapsed inventory of Page-owned supporting code."""
    directory = page_src.parent / "scripts"
    files = ([path for path in sorted(directory.rglob("*"))
              if _confined_file(path, directory) and not path.name.startswith(".")]
             if directory.is_dir() else [])
    if not files:
        return ""
    items = "".join("<li><code class=repo-path>%s</code></li>" %
                    html.escape(_shown_path(path, root)) for path in files)
    return ("<details class=scripts><summary>Scripts ▸ %d files</summary>"
            "<p class=mut>Read-only supporting code; not another Run lane.</p>"
            "<ul>%s</ul></details>" % (len(files), items))


def _run_card(row: dict, key: str, root: Path, page_src: Path,
              selected_run: str = "") -> str:
    """Render one semantic Run card with its Result behind the disclosure."""
    expanded = bool(selected_run and row.get("run_id") == selected_run)
    state = str(row.get("status", "Held"))
    return (
        '<article class=run-card>'
        '<div class=run-card-summary data-key="%s" data-run="%s" tabindex="0" '
        'role="button" aria-expanded="%s">'
        '<div class=run-card-name>%s</div>'
        '<span class="run-state-dot %s" title="%s" aria-label="Status: %s">●</span>'
        '<div class=run-card-action>%s</div></div>'
        '<div class=run-card-detail data-key="%s"%s>%s</div>'
        '</article>' % (
            html.escape(key), html.escape(str(row.get("run_id", ""))),
            "true" if expanded else "false", html.escape(_run_name(row)),
            html.escape(state.lower()), html.escape(state), html.escape(state),
            html.escape(_run_action(row)), html.escape(key),
            "" if expanded else " hidden", _detail(row, root, page_src),
        )
    )


def _run_subspace(title: str, rows: list[dict], prefix: str, root: Path,
                  page_src: Path, selected_run: str = "") -> str:
    """Render one stable Page Run or Evidence subspace."""
    if not rows:
        return '<section class=run-subspace><h3>%s</h3><div class=lane-empty>No %s Run yet.</div></section>' % (
            html.escape(title), html.escape(title))
    cards = "".join(_run_card(row, f"{prefix}-{index}", root, page_src, selected_run)
                     for index, row in enumerate(rows))
    return '<section class=run-subspace><h3>%s</h3><div class=run-cards>%s</div></section>' % (
        html.escape(title), cards)


def _support_group(row: dict) -> tuple[str, str]:
    """Return a stable Task-level grouping key and short reader label."""
    value = str(row.get("compact_id") or row.get("global_id") or row.get("run_id", ""))
    match = re.search(r"b(\d+)j(\d+)t(\d+)(?:r\d+)?", value.replace(".", ""), re.I)
    if not match:
        return "unassigned", "Unassigned"
    block, job, task = match.groups()
    return f"b{block}j{job}t{task}", f"T{int(task):02d}"


def _support_group_detail(group: dict, root: Path, page_src: Path,
                          selected_run: str = "") -> str:
    """Keep the Task card compact while retaining every child Result on demand."""
    members = []
    for row in group["rows"]:
        member_label = "%s · %s" % (row.get("run_id", "Run"), _run_action(row))
        opened = " open" if row.get("run_id") == selected_run else ""
        members.append(
            '<details class=support-member%s><summary><code>%s</code></summary>%s</details>' %
            (opened, html.escape(member_label), _detail(row, root, page_src))
        )
    return '<div class=support-group-detail>%s</div>' % "".join(members)


def _support_groups(rows: list[dict]) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = {}
    for row in rows:
        key, _label = _support_group(row)
        groups.setdefault(key, []).append(row)
    return groups


def _support_column(title: str, rows: list[dict], root: Path, page_src: Path,
                   selected_run: str = "") -> str:
    groups = _support_groups(rows)
    if not groups:
        return '<section class=support-column><h3>%s</h3><div class=lane-empty>No %s Run yet.</div></section>' % (
            html.escape(title), html.escape(title))
    cards = []
    for index, (key, members) in enumerate(sorted(groups.items())):
        _group_key, label = _support_group(members[0])
        group_id = f"support-{title.lower()}-{index}"
        expanded = bool(selected_run and any(row.get("run_id") == selected_run for row in members))
        status = min((row.get("status", "Held") for row in members),
                     key=lambda value: _STATE_ORDER.get(value, 9))
        action = _short_text(members[0].get("outcome") or members[0].get("target") or
                             "%d supporting results" % len(members))
        count_label = "Run" if len(members) == 1 else "Runs"
        cards.append(
            '<article class=run-card><div class=run-card-summary data-key="%s" data-run="%s" '
            'tabindex="0" role="button" aria-expanded="%s">'
            '<div class=run-card-name>%s · %d %s</div>'
            '<span class="run-state-dot %s" title="%s" aria-label="Status: %s">●</span>'
            '<div class=run-card-action>%s</div></div>'
            '<div class=run-card-detail data-key="%s"%s>%s</div></article>' % (
                html.escape(group_id), html.escape(members[0].get("run_id", "")),
                "true" if expanded else "false", html.escape(label), len(members), count_label,
                html.escape(status.lower()), html.escape(status), html.escape(status),
                html.escape(action), html.escape(group_id), "" if expanded else " hidden",
                _support_group_detail({"rows": members}, root, page_src, selected_run),
            )
        )
    return '<section class=support-column><h3>%s</h3><div class=run-cards>%s</div></section>' % (
        html.escape(title), "".join(cards))


def _run_space_tab(key: str, title: str, active: bool) -> str:
    """Render one compact Evidence-style selector for a Run Space lane."""
    selected = "true" if active else "false"
    selected_class = " on" if active else ""
    return (
        '<button type=button class="run-space-tab%s" id="run-space-tab-%s" '
        'role=tab data-space="%s" aria-selected="%s" '
        'aria-controls="run-space-panel-%s">%s</button>' % (
            selected_class, html.escape(key, quote=True), html.escape(key, quote=True),
            selected, html.escape(key, quote=True), html.escape(title)
        )
    )


def _run_space_panel(key: str, body: str, pills: str, active: bool) -> str:
    """Render only the selected lane while retaining accessible tab semantics."""
    hidden = "" if active else " hidden"
    return (
        '<section class="run-space-panel%s" id="run-space-panel-%s" role=tabpanel '
        'data-space-panel="%s" aria-labelledby="run-space-tab-%s"%s>'
        '<div class=run-space-overview>%s</div>%s</section>' % (
            " on" if active else "", html.escape(key, quote=True),
            html.escape(key, quote=True), html.escape(key, quote=True), hidden,
            pills, body
        )
    )


def _workflow_map_rows(page_src: Path) -> list[tuple[str, str, list[tuple[str, str, str]]]]:
    """Return the small Page Run Spec × Space definition map.

    This is deliberately a definition projection, not a second Run inventory.
    Run Spec rows are stable; the paths are parameterized by the current Page
    stem so the same view works for every file-backed Page.
    """
    stem = page_src.stem
    outline = f"outline/{stem}-outline-v*.md"
    context = f"outline/{stem}-context.md"
    logic = f"outline/{stem}-logic.mmd"
    evidence_items = f"outline/{stem}-evidence-items.md"
    product = f"{stem}.md"
    return [
        (
            "context",
            "Page.context",
            [
                ("read", "PageContext", context),
                ("—", "—", "—"),
                ("read-only", "ContextReceipt", "workflow/receipts/context-*.yaml"),
                ("—", "—", "—"),
            ],
        ),
        (
            "structure",
            "Page.interactive-writing.structure",
            [
                ("action", "OutlinePlan + Mermaid", f"{outline} · {logic}"),
                ("review", "EvidenceItemPlan", evidence_items),
                ("run", "StructureRun", "runs/rp-struct-*.md + results/rp-struct-*/"),
                ("—", "—", "—"),
            ],
        ),
        (
            "scratch",
            "Page.interactive-writing.scratch",
            [
                ("input", "ScratchNote", f"{outline}#Scratch"),
                ("—", "—", "—"),
                ("run", "ScratchResult", "runs/rp-scratch-* + results/rp-scratch-*/"),
                ("—", "—", "—"),
            ],
        ),
        (
            "section-writing",
            "Page.interactive-writing.section",
            [
                ("review", "WritingResult", outline),
                ("review", "EvidenceBinding", "results/re-*/result.yaml"),
                ("run", "SectionWritingRun", "runs/rp-sec-*.md + results/rp-sec-*/"),
                ("read", "PageDraft", product),
            ],
        ),
        (
            "paragraph-writing",
            "Page.interactive-writing.paragraph",
            [
                ("review", "WritingResult", outline),
                ("review", "EvidenceBinding", "results/re-*/result.yaml"),
                ("run", "ParagraphWritingRun", "runs/rp-para-*.md + results/rp-para-*/"),
                ("read", "PageDraft", product),
            ],
        ),
        (
            "evidence-item",
            "Page.evidence-item",
            [
                ("review", "EvidenceBinding", evidence_items),
                ("action", "EvidenceResult", "results/re-{value,display,cite}-*/result.yaml"),
                ("run", "EvidenceRun", "runs/re-*.md + results/re-*/"),
                ("review", "ArtifactDependency", "delivery/**/build-manifest.json"),
            ],
        ),
        (
            "delivery",
            "Page.delivery",
            [
                ("read", "PageSource", product),
                ("read", "EvidenceResult", "results/re-*/result.yaml"),
                ("run", "DeliveryRun", "runs/rd*.md + results/rd*/"),
                ("write", "DeliveryArtifact", "delivery/{web,latex,word,render}/"),
            ],
        ),
        (
            "check",
            "Page.check",
            [
                ("review", "OutlineCheck", f"{outline} + {product}"),
                ("review", "EvidenceCheck", "results/re-*/result.yaml"),
                ("read-only", "CheckReceipt", "workflow/receipts/"),
                ("review", "DeliveryCheck", "delivery/**/build-manifest.json"),
            ],
        ),
    ]


def _workflow_map_cell(mode: str, schema: str, path: str) -> str:
    """Render one compact, copy-friendly cell in the map grid."""
    if mode == "—":
        return '<div class="workflow-map-cell workflow-map-empty" role=cell>—</div>'
    return (
        '<div class=workflow-map-cell role=cell>'
        '<span class=workflow-map-mode>%s</span>'
        '<span class=workflow-map-schema>%s</span>'
        '<code class=workflow-map-path>%s</code></div>' % (
            html.escape(mode), html.escape(schema), html.escape(path)
        )
    )


def _workflow_map_html(page_src: Path) -> str:
    """Render the reader-facing Workflow × Space specification."""
    headers = (
        ("Run Spec", ""),
        ("Draft", "draft"),
        ("Evidence", "evidence"),
        ("Run", "runtime"),
        ("Delivery", "delivery"),
    )
    header_html = []
    for label, internal in headers:
        suffix = f" <code>{internal}</code>" if internal and internal != label.lower() else ""
        header_html.append(
            '<div class="workflow-map-cell workflow-map-head" role=columnheader>%s%s</div>' %
            (html.escape(label), suffix)
        )
    rows_html = []
    for spec_id, run_type, cells in _workflow_map_rows(page_src):
        cells_html = [
            '<div class="workflow-map-cell workflow-map-spec" role=rowheader>%s<code>%s</code></div>' %
            (html.escape(spec_id), html.escape(run_type))
        ]
        cells_html.extend(_workflow_map_cell(*cell) for cell in cells)
        rows_html.append('<div class=workflow-map-row role=row>%s</div>' % "".join(cells_html))
    return (
        '<p class=workflow-map-note>Rows are planned Run Specs; columns are Spaces. '
        'Each cell shows <code>mode · schema · path</code>. This map is read-only; '
        'the concrete Runs remain in the other Run Space tabs.</p>'
        '<div class=workflow-map-viewport><div class=workflow-map-grid role=table '
        'aria-label="Workflow by Space specification">%s%s</div></div>' %
        ("".join(header_html), "".join(rows_html))
    )


def render(page_src: Path, _path_q: str, _file_q: str,
           selected_run: str = "", selected_space: str = "") -> str:
    rows = run_inventory(page_src)
    run_p = [row for row in rows
             if row.get("lane") == "page" or row.get("operation") == "paragraph-writing"]
    run_e = [row for row in rows
             if row.get("lane") != "page"
             and row.get("origin") != "Linked"
             and row.get("operation") != "paragraph-writing"
             and (row.get("operation") == "evidence-item" or row.get("refs"))]
    # Supporting Runs are references to work owned outside this Page. Local
    # delivery, setup, design, and other Task/Insight records stay off-stage
    # in Folder; they are not a catch-all lane. Page-integrated plugin records
    # such as Labeling are also supporting work, even when stored locally.
    # External Results are still inspected by reference; this list never
    # copies them.
    supporting = [row for row in rows
                  if row.get("lane") != "page"
                  and row not in run_e
                  and (row.get("origin") == "Linked"
                       or row.get("family") == "Labeling")]
    root = repo_root(page_src.parent)
    writing = {name: [] for name in ("Structure", "Scratch", "Section", "Paragraph")}
    for row in run_p:
        writing[_page_writing_subspace(row)].append(row)
    evidence = {name: [] for name in _EVIDENCE_TYPE_ORDER}
    for row in run_e:
        evidence[_evidence_type(row) or "Value"].append(row)
    writing_sections = "".join(
        _run_subspace(name, writing[name], "writing-%s" % name.lower(), root, page_src, selected_run)
        for name in ("Structure", "Scratch", "Section", "Paragraph")
    )
    evidence_sections = "".join(
        _run_subspace(name, evidence[name], "evidence-%s" % name.lower(), root, page_src, selected_run)
        for name in _EVIDENCE_TYPE_ORDER
    )
    task_support = [row for row in supporting if str(row.get("kind", "")).lower() != "discovery"]
    discovery_support = [row for row in supporting if str(row.get("kind", "")).lower() == "discovery"]
    evidence_total, evidence_counts = _evidence_summary_counts(page_src, run_e)
    support_sections = '<div class=support-grid>%s%s</div>' % (
        _support_column("Task", task_support, root, page_src, selected_run),
        _support_column("Discovery", discovery_support, root, page_src, selected_run),
    )
    workflow_map = _workflow_map_html(page_src)
    selected_by_run = {
        "map": False,
        "writing": any(row.get("run_id") == selected_run for row in run_p),
        "evidence": any(row.get("run_id") == selected_run for row in run_e),
        "supporting": any(row.get("run_id") == selected_run for row in supporting),
    }
    active_space = selected_space if selected_space in selected_by_run else "writing"
    for key in ("evidence", "supporting"):
        if selected_by_run[key]:
            active_space = key
            break
    space_specs = (
        ("map", "Workflow map", workflow_map, _run_pills([
            ("Run Specs", len(_workflow_map_rows(page_src))),
            ("Spaces", 4),
        ])),
        ("writing", "Paper Writing", writing_sections, _run_pills([
            ("Writing Runs", len(run_p)),
            ("Structure", len(writing["Structure"])),
            ("Scratch", len(writing["Scratch"])),
            ("Sections", len(writing["Section"])),
            ("Paragraphs", len(writing["Paragraph"])),
        ])),
        ("evidence", "Evidence", evidence_sections, _run_pills([
            ("Evidence Items", evidence_total),
            ("Displays", evidence_counts["Display"]),
            ("Citations", evidence_counts["Citation"]),
            ("Values", evidence_counts["Value"]),
        ])),
        ("supporting", "Supporting Runs", support_sections, _run_pills([
            ("Supporting Runs", len(supporting)),
            ("Tasks", len(_support_groups(task_support))),
            ("Discoveries", len(_support_groups(discovery_support))),
        ])),
    )
    tabs = "".join(_run_space_tab(key, title, key == active_space)
                    for key, title, _body, _pills in space_specs)
    panels = "".join(_run_space_panel(key, body, pills, key == active_space)
                      for key, _title, body, pills in space_specs)
    main = (
        '<div class=wrap><div class=run-space-switcher role=tablist '
        'aria-label="Run Space sections">%s</div><div class=run-space-panels>%s</div></div>' %
        (tabs, panels)
    )
    return f"""<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width, initial-scale=1">
<title>Run Space · {html.escape(page_src.stem)}</title><style>{_CSS}</style>
<body class=embedded><header><h1>Run Space</h1></header>{main}
<script>
(function () {{
 function remember(r,open){{var u=new URL(window.location.href);if(open)u.searchParams.set('run',r.dataset.run);else u.searchParams.delete('run');history.replaceState(null,'',u);}}
 function selectSpace(key,rememberUrl){{var tabs=document.querySelectorAll('.run-space-tab');var panels=document.querySelectorAll('.run-space-panel');for(var i=0;i<tabs.length;i++){{var on=tabs[i].dataset.space===key;tabs[i].classList.toggle('on',on);tabs[i].setAttribute('aria-selected',String(on));}}for(var j=0;j<panels.length;j++){{var show=panels[j].dataset.spacePanel===key;panels[j].hidden=!show;panels[j].classList.toggle('on',show);}}if(rememberUrl){{var u=new URL(window.location.href);u.searchParams.set('space',key);history.replaceState(null,'',u);}}}}
 function normalizeRun(value){{return String(value || "").replace(/^P /, "");}}
 function toggle(r){{var key=r.dataset.key;var d=document.querySelector('.run-card-detail[data-key="'+key+'"]');if(d){{d.hidden=!d.hidden;r.setAttribute('aria-expanded',String(!d.hidden));remember(r,!d.hidden);}}}}
 document.addEventListener('click',function(e){{var tab=e.target.closest('.run-space-tab');if(tab)selectSpace(tab.dataset.space,true);}});
 document.addEventListener('click',function(e){{var r=e.target.closest('.run-card-summary');if(r)toggle(r);}});
 document.addEventListener('keydown',function(e){{var r=e.target.closest('.run-card-summary');if(r&&(e.key==='Enter'||e.key===' ')){{e.preventDefault();toggle(r);}}}});
 var initial=new URLSearchParams(window.location.search).get('space');var active=document.querySelector('.run-space-tab.on');selectSpace(initial||((active&&active.dataset.space)||'writing'),false);var wanted=new URLSearchParams(window.location.search).get('run');if(wanted){{var rows=document.querySelectorAll('.run-card-summary');for(var i=0;i<rows.length;i++){{if(normalizeRun(rows[i].dataset.run)===normalizeRun(wanted)){{var panel=rows[i].closest('.run-space-panel');if(panel)selectSpace(panel.dataset.spacePanel,false);rows[i].classList.add("bound-focus");rows[i].scrollIntoView({{block:'start'}});break;}}}}}} }})();
</script>"""


class RunsTabMixin:
    """Read-only page-local Runs view plus the shell's no-write POST twin."""

    def runs_view(self, head_only=False):
        query = parse_qs(urlparse(self.path).query)
        path_q = (query.get("path") or [""])[0]
        file_q = (query.get("file") or [""])[0]
        run_q = (query.get("run") or [""])[0]
        space_q = (query.get("space") or [""])[0]
        page_src, error = self.target({"path": path_q, "file": file_q})
        if page_src is None:
            return self.reply(400, {"ok": False, "err": error})
        body = render(page_src, path_q, file_q, run_q, space_q).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    def plug_runs(self, payload):
        page_src, error = self.target(payload)
        if page_src is None:
            return None, error
        return {"url": "/_board/runs?path=%s&file=%s" %
                (quote(payload.get("path") or ""), quote(payload.get("file") or ""))}, None
