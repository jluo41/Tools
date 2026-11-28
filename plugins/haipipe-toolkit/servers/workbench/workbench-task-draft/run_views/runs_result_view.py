"""How a Run reads on its card: its name, action, outcome and Result preview,
plus the small Markdown readers they share (moved verbatim from runs.py).
"""
from __future__ import annotations

import html
import re
from pathlib import Path

from live.runs_ids import (_PARAGRAPH_RUN, _REVISE_RUN, _SCRATCH_RUN, _SECTION_RUN, _is_structure_run,
                          _new_kind, _page_run_label)


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
        kind = _new_kind(run_id)
        if kind and kind not in {"scratch", "revise", "structure"}:
            target = str(row.get("target", "")).strip()
            word = kind.replace("-", " ").capitalize()
            return "%s · %s" % (word, target) if target else word
        if row.get("mode") == "scratch" or _SCRATCH_RUN.fullmatch(run_id) or kind == "scratch":
            scope = str(row.get("target_scope", "target")).capitalize()
            target = str(row.get("target", "")).strip()
            return "Scratch · %s%s" % (scope, (" · " + target) if target else "")
        if _REVISE_RUN.fullmatch(run_id) or kind == "revise":
            target = str(row.get("target", "")).strip()
            return "Revise · " + target if target else "Revise"
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
        if _REVISE_RUN.fullmatch(str(row.get("run_id", ""))) or _new_kind(row.get("run_id", "")) == "revise":
            return "Compare before and after for %s and settle each change" % (
                str(row.get("target", "")).strip() or "the target")
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


# at the end, not the top: these parts import one another, so each can be imported first
from live.runs_evidence import _evidence_item_label, _evidence_type
from live.runs_receipts import _confined_file, _repo_path
