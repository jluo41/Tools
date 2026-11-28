"""The Run Space inside 📃 Page, read-only.

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

from src.common import delivery_dir, delivery_read_lane_dir, delivery_relative  # noqa: F401  (kept importable)
import html
import re
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse

from live.outline_structure import STRUCTURE_CSS
from src.outline_version import plan_dir  # noqa: F401  (kept importable)
from src import run_names as _names  # noqa: F401  (kept importable)
from src.item_table import (compact_global_run, compact_paper_run, read_items,  # noqa: F401  (kept importable)
                            readable_global_run, readable_paper_route, repo_root,
                            run_registry)

# Moved parts, imported in this order (result_view before runs_track_changes and runs_cards,
# which read its names back through live.runs); names kept importable here.
from live.runs_ids import (  # noqa: F401
    _TICKET_SUFFIXES, _TICKET_NAME, _STATE_ORDER, _PAGE_WRITING_OPERATIONS, _STRUCTURE_RUN,
    _LEGACY_STRUCTURE_RUNS, _STRUCTURE_RUNS, _STRUCTURE_RUN_RE, _EVIDENCE_TYPES, _EVIDENCE_TYPE_ORDER,
    _SECTION_RUN, _SCRATCH_RUN, _REVISE_RUN, _AUTO_EMBED_RUN, _PARAGRAPH_RUN, _LEGACY_PARAGRAPH_RUN,
    _WRITING_KINDS, _new_kind, _is_structure_run, _writing_operation, _is_page_run, _page_run_label,
    _valid_page_run_id, _audit_page_run_order, _page_writing_subspace)
from live.runs_receipts import (  # noqa: F401
    _confined_file, _existing_path, _fields, _version_path, _interactive_findings, _version_closed,
    _declares_outputs, _status, _ticket_files, _is_ticket_place, _run_folder_receipt, _runtime_for,
    _fallback_result, _repo_path)
from live.runs_result_view import (  # noqa: F401
    _ticket_note, _preview_text, _plain_inline_markdown, _result_outcome, _short_text,
    _run_label_summary, _run_name, _run_action, _result_source_files, _yaml_result_payload,
    _render_result_file, _result_preview, _what_happened, _section_body, _step_section,
    _inline_markdown, _markdown_fragment, _subsection_body, _step_feedback_summary,
    _saved_result_focus, _level_heading_body)
from live.runs_evidence import (  # noqa: F401
    _evidence_type, _evidence_item_label, _evidence_records, _attach_evidence_bindings, _run_pills,
    _fallback_evidence_counts, _evidence_summary_counts, _evidence_refs)
from live.runs_cards import (  # noqa: F401
    _working_field, _meta_grid, _structure_run_visual, _scratch_run_detail, _page_run_detail,
    _linked, _shown_path, _detail, _scripts, _run_card, _run_subspace)
from live.runs_local import (  # noqa: F401
    task_page_info, _task_context, _sort_key, _task_result_locations, _fixed_delivery_run, local_runs)


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
.run-structure{margin:8px 0 12px}.run-structure h4{margin-top:0}.run-structure-source{margin:0 0 6px;color:var(--mut);font-size:11px}
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
 .detail-head{display:none}.review-card{padding:10px}.md-table{display:table}.detail-title{font-size:17px}}
"""


from live.runs_track_changes import (  # noqa: F401  (moved; names kept importable here)
    _token_track_changes, _track_sentences, _sentence_similarity, _word_track_changes,
    _track_change_html)


from live.runs_themes import (  # noqa: F401  (moved; names kept importable here)
    _labeling_runs, _insight_runs)


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
    from src.run_folders import result_roots, under_page_results
    if (page_src.parent / "results").is_symlink():
        return []
    rows = []
    manifests = [m for root in result_roots(page_src.parent) for m in sorted(root.rglob("result.yaml"))]
    for manifest in manifests:
        if manifest.is_symlink() or not under_page_results(page_src.parent, manifest):
            continue
        try:
            text = manifest.read_text(encoding="utf-8", errors="replace")
        except OSError:
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


from live.runs_support_column import (  # noqa: F401  (moved; names kept importable here)
    _support_group, _support_group_detail, _support_groups, _support_column)


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


from live.runs_workflow_map import (  # noqa: F401  (moved; names kept importable here)
    _workflow_map_rows, _workflow_map_cell, _workflow_map_html)


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
    # in Folder; they are not a catch-all lane. Page-integrated workbench records
    # such as Labeling are also supporting work, even when stored locally.
    # External Results are still inspected by reference; this list never
    # copies them.
    supporting = [row for row in rows
                  if row.get("lane") != "page"
                  and row not in run_e
                  and (row.get("origin") == "Linked"
                       or row.get("family") == "Labeling")]
    root = repo_root(page_src.parent)
    writing = {name: [] for name in ("Structure", "Scratch", "Section", "Paragraph", "Revise")}
    for row in run_p:
        writing[_page_writing_subspace(row)].append(row)
    evidence = {name: [] for name in _EVIDENCE_TYPE_ORDER}
    for row in run_e:
        evidence[_evidence_type(row) or "Value"].append(row)
    writing_sections = "".join(
        _run_subspace(name, writing[name], "writing-%s" % name.lower(), root, page_src, selected_run)
        for name in ("Structure", "Scratch", "Section", "Paragraph", "Revise")
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
        ("writing", "Page Writing", writing_sections, _run_pills([
            ("Writing Runs", len(run_p)),
            ("Structure", len(writing["Structure"])),
            ("Scratch", len(writing["Scratch"])),
            ("Sections", len(writing["Section"])),
            ("Paragraphs", len(writing["Paragraph"])),
            ("Revisions", len(writing["Revise"])),
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
<title>Run Space · {html.escape(page_src.stem)}</title><style>{_CSS}{STRUCTURE_CSS}</style>
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
        _p = {"path": path_q, "file": file_q}
        page_src, error = self.target(_p)
        file_q = _p["file"]
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
