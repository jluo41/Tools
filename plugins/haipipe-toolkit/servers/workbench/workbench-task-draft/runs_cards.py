"""One Run card and its opened detail: Page Run, structure and Scratch detail,
the scripts list, and the card and subspace HTML (moved verbatim from runs.py).
"""
from __future__ import annotations

import html
import re
from pathlib import Path

from live.runs_ids import _is_structure_run
from src.outline_version import plan_dir


def _working_field(text: str, label: str) -> str:
    hit = re.search(rf"^{re.escape(label)}:[ \t]*(.+)$", text, re.M | re.I)
    return hit.group(1).strip() if hit else ""


def _meta_grid(fields: list[tuple[str, str, bool]]) -> str:
    return "<dl class=run-meta>%s</dl>" % "".join(
        '<div%s><dt>%s</dt><dd>%s</dd></div>' %
        (' class=wide' if wide else "", html.escape(label), value)
        for label, value, wide in fields
    )


def _structure_run_visual(page_src: Path, row: dict) -> str:
    """The Structure Run's Result opens with the Outline as a text list.

    Same list Draft Space shows at its top (`live.outline_structure`), read
    from the selected Outline on every open. No Mermaid map (JL 260922).
    """
    if not _is_structure_run(str(row.get("run_id", ""))):
        return ""
    from src.outline_version import latest_outline
    from live.outline_structure import structure_text
    plan = latest_outline(plan_dir(page_src.parent), page_src.stem)
    if plan is None or not plan.is_file():
        return '<p class=note>No Outline exists yet; the Structure Run has nothing to show.</p>'
    text = structure_text(_preview_text(plan, plan.parent))
    if not text:
        return '<p class=note>The Outline declares no C<n> divisions yet.</p>'
    return ('<div class=run-structure><h4>Structure</h4>'
            '<div class=run-structure-source><code>%s</code></div>'
            '<pre class="structure-text">%s</pre></div>'
            % (html.escape(plan.parent.name + "/" + plan.name), html.escape(text)))


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

    visual = _structure_run_visual(page_src, row)
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


# at the end, not the top: these parts import one another, so each can be imported first
from live.runs_receipts import _confined_file, _interactive_findings, _repo_path, _version_path
from live.runs_result_view import (_inline_markdown, _level_heading_body, _markdown_fragment, _preview_text,
                                   _result_preview, _run_action, _run_label_summary, _run_name,
                                   _saved_result_focus, _step_feedback_summary, _step_section)
from live.runs_track_changes import _track_change_html
