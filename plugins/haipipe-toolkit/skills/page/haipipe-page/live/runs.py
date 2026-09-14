"""The Run Space inside 🧭 Outline, read-only.

The Page-facing vocabulary has three lanes: Run P for human/Page interactions,
Run E for Page-owned Evidence production, and Supporting Runs for linked work
owned elsewhere. Supporting Runs remain inspectable references; they are never
copied into this Page.

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
    r"(?:^rp\d+|^rl\d+|^ri\d+|^rd\d+|^r\d+|^run[-_]|^b\d+[._]j\d+[._]t\d+[._]r\d+|^p[._]?j\d+[._]?t\d+[._]?r\d+)",
    re.I,
)
_STATE_ORDER = {"Running": 0, "Waiting": 1, "Failed": 2, "Held": 3,
                "Ready": 4, "Done": 5}
_PAGE_WRITING_OPERATIONS = {"interactive-writing", "paragraph-writing"}
_STRUCTURE_RUN = "rp00_mermaid-structure"
_PARAGRAPH_RUN = re.compile(
    r"(rp(?:0[1-9]|[1-9]\d+))_p(0[1-9]|[1-9]\d+)"
    r"(?:-p(0[1-9]|[1-9]\d+))?"
)


_CSS = """
:root{--bg:#fff;--fg:#1c1d1f;--mut:#71727a;--line:#e4e4e7;--card:#f7f7f8;
 --acc:#3b6ea5;--ok:#287443;--warn:#a95b12;--bad:#b13c3c}
@media(prefers-color-scheme:dark){:root{--bg:#161719;--fg:#e8e8e6;--mut:#9a9a97;
 --line:#2c2e33;--card:#1d1f23;--acc:#7aa7d8;--ok:#74b68a;--warn:#e0a05c;--bad:#e77b7b}}
body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.55 -apple-system,
 BlinkMacSystemFont,'Segoe UI',sans-serif}header{padding:10px 16px 7px}h1{font-size:16px;margin:0}
.embedded header{display:none}
.source-map{margin:8px 16px 6px;color:var(--mut);font:11px/1.45 ui-monospace,SFMono-Regular,Menlo,monospace}
.source-map code{color:var(--fg);font-size:11px}
.mut{color:var(--mut);font-size:12.5px}.lead{margin:3px 0 0}.summary{display:flex;gap:8px;
 padding:7px 16px;border-top:1px solid var(--line);border-bottom:1px solid var(--line);font-size:12.5px}
.wrap{padding:0 16px 16px;overflow:auto}.note{margin:9px 0;font-size:12.5px;color:var(--mut)}
table{width:100%;border-collapse:collapse;font-size:12.5px}th,td{text-align:left;vertical-align:top;
 border-bottom:1px solid var(--line);padding:8px 6px}th{font-size:11px;color:var(--mut);
 text-transform:uppercase;letter-spacing:.035em}tr.run{cursor:pointer}tr.run:hover td{background:var(--card)}
code{font:12px ui-monospace,SFMono-Regular,Menlo,monospace}.route{font-weight:650;white-space:nowrap}.state{font-weight:650;white-space:nowrap}
tr.run td:first-child::after{content:'›';display:inline-block;margin-left:7px;color:var(--mut);font:bold 16px/1 sans-serif;transition:transform .15s}tr.run[aria-expanded=true] td:first-child::after{transform:rotate(90deg)}
.state.ready{color:var(--acc)}.state.running,.state.waiting{color:var(--warn)}.state.done{color:var(--ok)}.state.failed,.state.held{color:var(--bad)}
.repo-path{white-space:normal;overflow-wrap:anywhere;word-break:break-word;user-select:text}.detail[hidden]{display:none}
.detail td{padding:0 7px 10px;background:var(--card)}.detailbox{border-left:3px solid var(--acc);padding:12px 14px;margin:3px 0;font-size:14px}
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
.detailbox h2{font-size:14px;margin:14px 0 5px}.summary{flex-wrap:wrap}
.lane{margin:16px 0 22px}.lane h2{font-size:14px;margin:0 0 2px}.lane-empty{margin:8px 0 0;
 padding:11px 12px;border:1px dashed var(--line);border-radius:7px;color:var(--mut)}
.scripts{margin:16px 0}.scripts summary{cursor:pointer;font-weight:650}.scripts ul{padding-left:20px}
@media(max-width:700px){body{font-size:15px}.wrap{padding:0 10px 14px;overflow:visible}.summary{padding:7px 10px}
 table.runs-table,table.runs-table>tbody{display:block}table.runs-table>thead{display:none}.runs-table>tbody>tr.run{display:grid;grid-template-columns:1fr auto;gap:3px 10px;padding:10px 8px;border-bottom:1px solid var(--line)}
 .runs-table>tbody>tr.run>td{display:block;padding:0;border:0}.runs-table>tbody>tr.run>td:nth-child(2){grid-column:1/-1;font-size:14px}.runs-table>tbody>tr.run>td:nth-child(3){color:var(--mut)}
 .runs-table>tbody>tr.run>td:nth-child(4){grid-column:2;grid-row:1;text-align:right}.runs-table>tbody>tr.run>td:nth-child(5){display:none}
 .task-runs>tbody>tr.run>td:nth-child(2){grid-column:1/-1;font-size:12px;color:var(--mut)}.task-runs>tbody>tr.run>td:nth-child(3){grid-column:1/-1;color:var(--fg);font-size:14px}
 .runs-table>tbody>tr.detail{display:block}.runs-table>tbody>tr.detail[hidden]{display:none}.runs-table>tbody>tr.detail>td{display:block;padding:0 4px 12px;border-bottom:1px solid var(--line)}
 .detailbox{border-left:0;border-top:3px solid var(--acc);padding:13px 10px;margin:0}.run-meta{grid-template-columns:1fr 1fr}.run-meta .wide{grid-column:1/-1}
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
             "operation", "interaction", "mode", "version", "step", "outcome", "summary")}


def _writing_operation(fields: dict[str, str]) -> bool:
    """Return whether the Run uses a writing dialect that requires a receipt."""
    return fields.get("operation", "").lower() in _PAGE_WRITING_OPERATIONS


def _is_page_run(fields: dict[str, str]) -> bool:
    """Only human-feedback interactive writing belongs to the Page Run lane."""
    return fields.get("operation", "").lower() == "interactive-writing"


def _page_run_label(run_id: str) -> str:
    """Keep the Page Run column short while preserving its canonical identity."""
    if run_id == _STRUCTURE_RUN:
        return "rp00 · Mermaid Structure"
    match = _PARAGRAPH_RUN.fullmatch(run_id)
    if not match:
        return run_id
    scope = f"P{match.group(2)}"
    if match.group(3):
        scope += f"-P{match.group(3)}"
    return f"{match.group(1).lower()} · {scope.upper()}"


def _valid_page_run_id(run_id: str) -> bool:
    """Accept only the current Page Run namespace; no aliases or fallback."""
    return run_id == _STRUCTURE_RUN or bool(_PARAGRAPH_RUN.fullmatch(run_id))


def _audit_page_run_order(rows: list[dict]) -> None:
    """Reject noncanonical ids and require the closed Mermaid Structure Run."""
    page_rows = [row for row in rows if row.get("lane") == "page"]
    structure = next((row for row in page_rows
                      if row["run_id"] == _STRUCTURE_RUN), None)
    structure_closed = bool(structure and structure.get("status") == "Done")
    for row in page_rows:
        run_id = row["run_id"]
        if not _valid_page_run_id(run_id):
            row["status"] = "Held"
            row.setdefault("audit", []).append(
                "invalid Page Run identity; expected rp00_mermaid-structure "
                "or rpNN_pNN[-pNN] from rp01"
            )
            continue
        if run_id == _STRUCTURE_RUN:
            continue
        if structure_closed:
            continue
        row["status"] = "Held"
        row.setdefault("audit", []).append(
            "paragraph Page Run requires a closed rp00_mermaid-structure"
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
    if row.get("run_id") != _STRUCTURE_RUN:
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


def _page_run_detail(row: dict, root: Path, page_src: Path) -> str:
    """Reader-first Page Run summary with history and internals on demand."""
    version_step = "/".join(filter(None, (row.get("version", ""), row.get("step", ""))))
    scope = ("Whole-page argument flow and paragraph order (P01–P06)"
             if row.get("run_id") == _STRUCTURE_RUN
             else row.get("target") or "Page")
    fields = [
        ("Goal", html.escape(row.get("goal") or "Not recorded"), True),
        ("Scope", html.escape(scope), True),
        ("Status", '<span class="state %s">%s</span>' %
         (html.escape(row["status"].lower()), html.escape(row["status"])), False),
        ("Version / Step", html.escape(version_step or "Not started"), False),
    ]
    chunks = [
        '<div class=detail-head><span class=detail-title>%s</span></div>' %
        html.escape(_page_run_label(row["run_id"])),
        _meta_grid(fields),
    ]
    earlier_steps: list[tuple[str, str, str, str]] = []
    working_text = ""
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
                    if request:
                        chunks.append("<section class=\"review-card feedback\"><h3>Latest feedback</h3>%s%s</section>" %
                                      (_markdown_fragment(request),
                                       ("<h4>What this means</h4><ul>%s</ul>" % "".join(
                                           f"<li>{_inline_markdown(item)}</li>" for item in interpretations
                                       )) if interpretations else ""))
                    if result:
                        visual = _mermaid_run_visual(page_src, row)
                        chunks.append("<section class=\"review-card result\"><h3>Current saved result</h3>%s%s</section>" %
                                      (visual, _markdown_fragment(result) + track_changes))
                else:
                    earlier_steps.append((f"{path.stem}/{step_id}", request, result,
                                          track_changes))
    else:
        chunks.append("<p class=note>This Page Run has no current lifecycle projection.</p>")

    next_action = _working_field(working_text, "Next")
    if next_action:
        chunks.append('<p class=next-action><b>Next</b><br>%s</p>' %
                      _inline_markdown(next_action))
    if earlier_steps:
        entries = []
        for label, request, result, track_changes in reversed(earlier_steps):
            body = (("<h4>Feedback</h4>%s" % _markdown_fragment(request)) if request else "")
            body += (("<h4>Saved result</h4>%s" % _markdown_fragment(result)) if result else "")
            body += track_changes
            entries.append("<details class=step-history><summary>%s</summary>%s</details>" %
                           (html.escape(label), body or "<p>No readable summary recorded.</p>"))
        chunks.append("<details class=history><summary>Earlier steps · %d</summary>%s</details>" %
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
    for finding in row.get("audit", []):
        technical_html += "<p class=note>Run audit finding: %s.</p>" % html.escape(finding)
    chunks.append("<details class=technical><summary>Technical details</summary>%s</details>" %
                  technical_html)
    return "<div class=detailbox>%s</div>" % "".join(chunks)


def _interactive_findings(runtime: Path, fields: dict[str, str]) -> list[str]:
    """Check that the current Version/Step is durable in one Markdown journal."""
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
    numbers = re.findall(r"r(?:p|l|i|d)?(\d+)", row.get("run_id", ""), re.I)
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
        for key in ("target", "family", "operation", "interaction", "mode", "version", "step"):
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
    return sorted(rows, key=lambda row: (row.get("lane") != "page",) + _sort_key(row))


def _detail(row: dict, root: Path, page_src: Path) -> str:
    if row.get("lane") == "page" and row.get("operation") == "interactive-writing":
        return _page_run_detail(row, root, page_src)
    fields = [("Run", html.escape(row["run_id"])),
              ("Purpose", html.escape(row["target"]))]
    if row.get("lane") == "page":
        fields.extend([
            ("Goal", html.escape(row.get("goal") or "not recorded")),
            ("Version / Step", html.escape("/".join(filter(None, (
                row.get("version", ""), row.get("step", "")))) or "not started")),
            ("Run record", _linked(row["ticket"], label=_shown_path(row["ticket"], root))),
            ("Writing Result", _linked(row.get("result_path"),
                                        label=_shown_path(row.get("result_path"), root))),
        ])
    else:
        # A Page consumes a delegated Result. Ticket, command and runtime are
        # deliberately not projected across the Task ownership boundary.
        fields.insert(1, ("Kind / where", html.escape(
            f"{row.get('kind', 'Task')} · {row.get('origin', 'Local')}")))
        fields.insert(3, ("What happened", html.escape(_what_happened(row))))
        result_path = row.get("result_path") or _repo_path(root, row.get("result", ""))
        fields.append(("Result", _linked(result_path,
                                           label=_shown_path(result_path, root))
                       if result_path else "not available yet"))
    chunks = ["<p class=kv><b>%s</b><span>%s</span></p>" % (label, value)
              for label, value in fields]
    for finding in row.get("audit", []):
        chunks.append("<p class=note>Run audit finding: %s.</p>" % html.escape(finding))
    if row["refs"]:
        chunks.append("<p><b>Evidence</b></p><ul class=refs>%s</ul>" % "".join(
            "<li><code>%s</code></li>" % html.escape(ref) for ref in row["refs"]
        ))
    if row.get("operation") == "paragraph-writing":
        if row["runtime"] is None:
            chunks.append("<p class=note>Missing runtime.yaml: this writing Run has no lifecycle receipt.</p>")
        previews = ([('Writing instructions / Prompt', row['ticket'], row['ticket'].parent)]
                    if row.get("ticket") else [])
        if row["runtime"]:
            directory = row["runtime"].parent
            previews.extend((label, directory / name, directory) for label, name in
                            (("Paragraph", "paragraph.md"), ("Trace / Review", "trace.md")))
        for label, path, boundary in previews:
            text = _preview_text(path, boundary)
            chunks.append("<h2>%s</h2><pre class=run-preview>%s</pre>" %
                          (label, html.escape(text or "Not available yet.")))
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


def _lane_table(rows: list[dict], lane: str, root: Path, page_src: Path,
                selected_run: str = "") -> str:
    if not rows:
        message = {
            "p": "No Run P yet.",
            "e": "No Run E yet.",
            "support": "No Supporting Run linked yet.",
        }.get(lane, "No Run yet.")
        return '<div class=lane-empty><b>%s</b></div>' % html.escape(message)
    rendered = []
    headings = ("<th>Run</th><th>Goal</th><th>Version / Step</th><th>Status</th><th>Result</th>"
                if lane == "p" else
                "<th>Run</th><th>Type / Where</th><th>What happened</th><th>Status</th><th>Result</th>")
    for index, row in enumerate(rows):
        key = f"{lane}-{index}"
        expanded = bool(selected_run and row["run_id"] == selected_run)
        expanded_text = "true" if expanded else "false"
        hidden = "" if expanded else " hidden"
        state = row["status"].lower()
        if lane == "p":
            middle = html.escape("/".join(filter(None, (row.get("version", ""),
                                                         row.get("step", "")))) or "—")
            result = "history" if row["runtime"] else "—"
            cells = (html.escape(_page_run_label(row["run_id"])),
                     html.escape(row.get("goal") or row["target"]),
                     middle, html.escape(state), html.escape(row["status"]), result)
        else:
            result = "output" if row.get("result") else "—"
            kind_origin = f"{row.get('kind', 'Task')} · {row.get('origin', 'Local')}"
            cells = (html.escape(row["run_id"]), html.escape(kind_origin),
                     html.escape(_what_happened(row)), html.escape(state),
                     html.escape(row["status"]), result)
        rendered.append(
            '<tr class="run" data-key="%s" data-run="%s" tabindex="0" aria-expanded="%s"><td><code class=route>%s</code></td>'
            '<td>%s</td><td>%s</td><td><span class="state %s">%s</span></td><td>%s</td></tr>'
            '<tr class="detail" data-key="%s"%s><td colspan=5>%s</td></tr>' %
            ((html.escape(key), html.escape(row["run_id"]), expanded_text) + cells +
             (html.escape(key), hidden, _detail(row, root, page_src))))
    return '<table class="runs-table %s-runs"><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (lane, headings, "".join(rendered))


def render(page_src: Path, _path_q: str, _file_q: str,
           selected_run: str = "") -> str:
    rows = run_inventory(page_src)
    run_p = [row for row in rows
             if row.get("lane") == "page" or row.get("operation") == "paragraph-writing"]
    run_e = [row for row in rows
             if row.get("lane") != "page"
             and row.get("origin") != "Linked"
             and row.get("operation") != "paragraph-writing"
             and (row.get("operation") == "evidence-item" or row.get("refs"))]
    supporting = [row for row in rows if row.get("origin") == "Linked"]
    root = repo_root(page_src.parent)
    sections = [
        ("Run P", run_p, "p"),
        ("Run E", run_e, "e"),
        ("Supporting Runs", supporting, "support"),
    ]
    lane_sections = "".join(
        "<section class=lane><h2>%s</h2>%s</section>" % (
            title, _lane_table(lane_rows, lane, root, page_src, selected_run))
        for title, lane_rows, lane in sections
    )
    source_map = ("<div class=source-map>Tickets <code>runs/</code> · "
                  "Results <code>results/</code> · Supporting <code>linked refs</code></div>")
    main = source_map + "<div class=wrap>%s</div>" % lane_sections
    return f"""<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width, initial-scale=1">
<title>Run Space · {html.escape(page_src.stem)}</title><style>{_CSS}</style>
<body class=embedded><header><h1>Run Space</h1></header>{main}
<script>
(function () {{
 function remember(r,open){{var u=new URL(window.location.href);if(open)u.searchParams.set('run',r.dataset.run);else u.searchParams.delete('run');history.replaceState(null,'',u);}}
 function toggle(r){{var key=r.dataset.key;var d=document.querySelector('tr.detail[data-key="'+key+'"]');if(d){{d.hidden=!d.hidden;r.setAttribute('aria-expanded',String(!d.hidden));remember(r,!d.hidden);}}}}
 document.addEventListener('click',function(e){{var r=e.target.closest('tr.run');if(r)toggle(r);}});
 document.addEventListener('keydown',function(e){{var r=e.target.closest('tr.run');if(r&&(e.key==='Enter'||e.key===' ')){{e.preventDefault();toggle(r);}}}});
 var wanted=new URLSearchParams(window.location.search).get('run');if(wanted){{var rows=document.querySelectorAll('tr.run');for(var i=0;i<rows.length;i++){{if(rows[i].dataset.run===wanted){{rows[i].scrollIntoView({{block:'start'}});break;}}}}}} }})();
</script>"""


class RunsTabMixin:
    """Read-only page-local Runs view plus the shell's no-write POST twin."""

    def runs_view(self, head_only=False):
        query = parse_qs(urlparse(self.path).query)
        path_q = (query.get("path") or [""])[0]
        file_q = (query.get("file") or [""])[0]
        run_q = (query.get("run") or [""])[0]
        page_src, error = self.target({"path": path_q, "file": file_q})
        if page_src is None:
            return self.reply(400, {"ok": False, "err": error})
        body = render(page_src, path_q, file_q, run_q).encode("utf-8")
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
