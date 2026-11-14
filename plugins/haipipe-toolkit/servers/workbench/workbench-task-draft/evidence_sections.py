"""The Evidence view's sections, assembled from the item, binding, Run and Result cards."""
from __future__ import annotations

import html
import pathlib
import re
from urllib.parse import quote
from live.evidence_preview import (  # noqa: F401  (moved; names kept importable here)
    _PREVIEW_IMAGE_SUFFIXES, _PREVIEW_PATH_KEYS, _PREVIEW_COPY_KEYS,
    _PREVIEW_SUFFIX_ORDER, _payload, _preview_scalar, _find_preview_scalar,
    _preview_label, _value_preview_label, _value_preview_rows, _value_preview_table,
    _preview_facts, _preview_table, _payload_table, _preview_texts,
    _preview_path_hints, _safe_preview_file, _preview_artifact, _render_delimited,
    _preview_asset_data, _render_preview_artifact, _result_preview)
from live.evidence_results import _detail_row, _evidence_run_contract, _evidence_type, _status_parts
from live.evidence_prompt import _copy_prompt_button, _evidence_copy_prompt, _label_details, _label_summary

def _workspace_actions(path_q: str, file_q: str, run_id: str = "") -> str:
    if not path_q and not file_q:
        return ""
    path = quote(path_q or "", safe="")
    file = quote(file_q or "", safe="")
    runs_href = "/_board/runs?path=%s&file=%s" % (path, file)
    if run_id:
        runs_href += "&space=evidence&run=%s" % quote(run_id, safe="")
    folder_href = "/_board/folderstat?path=%s&file=%s" % (path, file)
    return ('<div class=evidence-actions aria-label="Evidence navigation">'
            '<a class=evidence-action href="%s" target="_blank" rel="noopener">Run Space</a>'
            '<a class=evidence-action href="%s" target="_blank" rel="noopener">'
            'Browse Run + Result folders</a></div>' %
            (html.escape(runs_href, quote=True), html.escape(folder_href, quote=True)))


def _evidence_sections(records: list[dict[str, object]],
                       page_home: pathlib.Path | None = None,
                       root: pathlib.Path | None = None,
                       path_q: str = "", file_q: str = "",
                       page_src: pathlib.Path | None = None) -> str:
    """Render compact typed sections with collapsed, progressive-disclosure cards."""
    if not records:
        return '<div class=ghost>No current Evidence Item or Result.</div>'

    if page_home is None:
        for record in records:
            result_file = record.get("result_file")
            if isinstance(result_file, pathlib.Path):
                page_home = result_file.parent.parent.parent
                break
    page_home = page_home or pathlib.Path.cwd()
    root = root or page_home

    groups: dict[str, list[dict[str, object]]] = {
        "DISPLAY": [], "CITE": [], "VALUE": [], "OTHER": [],
    }
    for record in records:
        groups[_evidence_type(record)].append(record)

    headings = {
        "DISPLAY": ("Displays", "figures · tables · algorithms"),
        "CITE": ("Citations", "verified source claims"),
        "VALUE": ("Values", "scalars · intervals · comparisons"),
        "OTHER": ("Other", "migration items"),
    }
    sections = []
    for kind in ("DISPLAY", "CITE", "VALUE", "OTHER"):
        items = groups[kind]
        if not items:
            continue
        title, hint = headings[kind]
        cards = []
        for record in items:
            item_id = str(record.get("id", "")).strip()
            fields = record.get("fields", {})
            status, status_token = _status_parts(record)
            title_text = str(record.get("title", "")).strip()
            label = str(fields.get("label", "")).strip()
            if not label:
                label = title_text or item_id.split("-", 2)[-1].replace("-", " ")
            address = str(record.get("address", fields.get("target", ""))).strip()
            run_id = str(fields.get("run", "") or fields.get("local run", "")).strip()
            result_path = str(fields.get("result", "")).strip()
            result_note = str(fields.get("has", "")).strip()
            supporting = str(fields.get("supporting runs", "")).strip()
            focus = "run-" + re.sub(r"[^A-Za-z0-9_-]", "-", item_id)
            safe_kind = html.escape(kind, quote=True)
            safe_item = html.escape(item_id, quote=True)
            display_title = title_text if title_text and title_text.lower() != label.lower() else ""
            label_html = _label_details(fields.get("labels", []))
            label_summary = _label_summary(fields.get("labels", []))
            copy_prompt = (_copy_prompt_button(_evidence_copy_prompt(
                record, page_src, root, path_q, file_q, status))
                if (page_src is not None and kind in {"VALUE", "CITE", "DISPLAY"}
                    and str(record.get("address", fields.get("target", ""))).strip()
                    and not (fields.get("no selected result")
                             and str(fields.get("decision", "")).strip() in {"drop", "defer"})) else "")
            contract = _evidence_run_contract(kind) if kind in {"VALUE", "CITE", "DISPLAY"} else None
            run_pattern = {
                "VALUE": "run-value-<slug>",
                "CITE": "run-citation-<slug>",
                "DISPLAY": "run-display-<slug>",
            }.get(kind, "")
            contract_details = ""
            if contract:
                matching = str(fields.get("matching page runs", "")).strip()
                if not matching:
                    matching = ("%s · %s" % (run_id, str(fields.get("run status", "")).strip() or "status not recorded")
                                if run_id else "none recorded")
                matching += " · Result status: " + ("no selected Result" if fields.get("no selected result") else status)
                contract_rows = "".join((
                    _detail_row("Run Type", "Page.evidence-item · " + contract["name"]),
                    _detail_row("Run identity", run_pattern, code=True),
                    _detail_row("Bounded work", contract["work"]),
                    _detail_row("Owner Skill", contract["owner"]),
                    _detail_row("Worker Skill(s)", contract["workers"]),
                    _detail_row("Actor", contract["actor"]),
                    _detail_row("Prerequisites", contract["prerequisites"]),
                    _detail_row("Space affordance", "Shown here · read-only"),
                    _detail_row("Matching Run / status", matching),
                ))
                contract_details = (
                    '<details class=evidence-trace><summary>%s Run · Run Type and ownership</summary>'
                    '<div class=evidence-trace-body>%s</div></details>' % (
                        html.escape(contract["name"]), contract_rows))
            trace = "".join((
                ('<div class=evidence-detail-row><span class=evidence-detail-label>'
                 'Evidence Labels</span><span class=evidence-detail-value>%s</span></div>'
                 % label_html) if label_html else "",
                _detail_row("Evidence Label", label),
                _detail_row("Evidence Item", item_id, code=True),
                _detail_row("Type", kind),
                _detail_row("Bullet", address, code=True),
                _detail_row("Status", status),
                _detail_row("Evidence Run", run_id or "not allocated", code=bool(run_id)),
                _detail_row("Owner Run", str(fields.get("owner run", "")).strip(), code=True),
                _detail_row("Supporting Runs", supporting or "none"),
                _detail_row("Result", result_path or (result_note or "not ready"), code=bool(result_path)),
                _detail_row("Item Expected", str(fields.get("item expected", "")).strip()),
                _detail_row("Item Acceptance", str(fields.get("item acceptance", "")).strip()),
                _detail_row("Local Input", str(fields.get("local input", "")).strip()),
                _detail_row("Ledger Local Run", str(fields.get("ledger local run", "")).strip()),
                _detail_row("Ledger Run action", str(fields.get("ledger run action", "")).strip()),
                _detail_row("Ledger Run route", str(fields.get("ledger run route", "")).strip(), code=True),
                _detail_row("Ledger Result binding", str(fields.get("ledger result binding", "")).strip(), code=True),
                _detail_row("Decision", str(fields.get("decision", "")).strip()),
                _detail_row("Expected", str(fields.get("expected", "")).strip()),
                _detail_row("Acceptance", str(fields.get("acceptance", "")).strip()),
            ))
            detail = "".join((
                label_summary,
                contract_details,
                _result_preview(record, page_home, root),
                '<div class=evidence-prompt-actions>%s</div>' % copy_prompt if copy_prompt else "",
                _workspace_actions(path_q, file_q, run_id),
                '<details class=evidence-trace><summary>Traceability</summary>'
                '<div class=evidence-trace-body>%s</div></details>' % trace,
            ))
            cards.append(
                '<details class=evidence-card id="%s" data-evidence-id="%s" data-evidence-type="%s">'
                '<summary class=evidence-summary><span class=evidence-chevron aria-hidden=true>›</span>'
                '<span class=evidence-kind>%s</span>'
                '<span class=evidence-summary-main><span class=evidence-summary-line>'
                '<span class=evidence-label>%s</span><span class=evidence-title>%s</span></span></span>'
                '%s'
                '<span class="evidence-status %s">%s</span></summary>'
                '<div class=evidence-detail>%s</div></details>' % (
                    html.escape(focus, quote=True), safe_item, safe_kind,
                    safe_kind, html.escape(label), html.escape(display_title),
                    ('<code class=evidence-bullet>%s</code>' % html.escape(address)) if address else "",
                    html.escape(status_token, quote=True),
                    html.escape(status), detail,
                )
            )
        sections.append(
            '<section id="evidence-%s" class=evidence-type-section data-evidence-type="%s">'
            '<header class=evidence-type-head><h2 class=evidence-type-title>%s</h2>'
            '<span class=evidence-type-count>%d</span><span class=evidence-type-hint>%s</span></header>'
            '<div class=evidence-cards>%s</div></section>' % (
                html.escape(kind, quote=True), html.escape(kind, quote=True),
                html.escape(title), len(items),
                html.escape(hint), "".join(cards)
            )
        )
    return "".join(sections)
