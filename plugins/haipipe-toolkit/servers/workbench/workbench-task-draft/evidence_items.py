"""The plan's Evidence Items as cards: the snapshot of each item, its plan and Run chips, and the card."""
from __future__ import annotations

import html
import json
import re
from src.item_table import readable_global_run, readable_paper_route, readable_task, wall_label
from live.evidence_text import _FIELD, _ITEM_HEADING, _inline_lite, _md_lite

def _evidence_snapshot(text: str) -> tuple[str, list[dict[str, object]]]:
    """Read the generated snapshot without leaking its file mechanics into UI.

    The snapshot remains the durable generated audit.  This reader keeps its
    item headings and labelled rows, while omitting its file title, regeneration
    command, and sentinel lines; they explain the file, not the Evidence view.
    """
    plan, records, current = "", [], None
    for raw in text.splitlines():
        line, stripped = raw.rstrip(), raw.strip()
        if not stripped or line.startswith("# ---") or stripped.startswith((
                "# ", "page:", "kind:", "EVIDENCE STATUS", "regenerate:", "GENERATED")):
            continue
        if stripped.startswith("plan:"):
            plan = stripped[len("plan:"):].strip()
            continue
        match = _ITEM_HEADING.match(line)
        if match:
            rest = match.group(2).split(" · ", 1)
            current = {"id": match.group(1).strip(), "address": rest[0].strip(),
                       "title": rest[1].strip() if len(rest) > 1 else rest[0].strip(),
                       "fields": {}}
            records.append(current)
            continue
        match = _FIELD.match(stripped)
        if match and current is not None:
            current["fields"][match.group(1).strip().lower()] = match.group(2).strip()
    # A stale snapshot can repeat an item at several Bullet targets. Keep one
    # addressable card per immutable identity, but expose every conflicting
    # source record instead of silently choosing a ready contract.
    unique = {}
    for record in records:
        item_id = str(record["id"])
        if item_id not in unique:
            unique[item_id] = record
        else:
            unique[item_id].setdefault("duplicate_records", []).append(record)
    return plan, list(unique.values())


def _plan_chips(plan: str) -> str:
    """Keep only the current, reader-relevant plan facts in the top summary."""
    if not plan:
        return ""
    chips = []
    version = re.search(r"\bv(\d+)\b", plan)
    cycle = re.search(r"\bcycle:\s*([A-Za-z]+)", plan)
    items = re.search(r"\bitems\s+(\d+)", plan)
    decided = re.search(r"\bdecided\s+(\d+/\d+)", plan)
    approved = re.search(r"\bapproved:\s*([^·]+)", plan)
    if version:
        chips.append("<span>plan v%s</span>" % version.group(1))
    if cycle:
        chips.append("<span class=cycle>%s</span>" % html.escape(cycle.group(1)))
    if items:
        chips.append("<span>%s items</span>" % items.group(1))
    if decided:
        chips.append("<span>%s decided</span>" % decided.group(1))
    if approved and "✅" in approved.group(1):
        chips.append("<span class=approved>approved</span>")
    for kind, count in re.findall(r"\b(VALUE|CITE|DISPLAY)\s+(\d+)", plan):
        chips.append("<span>%s %s</span>" % (html.escape(kind), count))
    return '<div class=evsummary>%s</div>' % "".join(chips) if chips else ""


def _run_chips(value: str, evidence_id: str, context: dict[str, str]) -> str:
    """Show compact family, action, and dotted address without inventing rNN."""
    from live.evidence_bindings import _lineage_chip, _with_evidence_context
    chips = []
    for raw in value.split(";"):
        parts = [part.strip() for part in raw.split(" · ") if part.strip()]
        if not parts:
            continue
        address = parts[-1]
        readable = readable_global_run(address) or readable_task(address) or address
        family, action = (parts[0] if len(parts) > 2 else ""), (parts[1] if len(parts) > 2 else "")
        key = family.lower()
        marker = "D" if key.startswith("discovery") else "X" if key.startswith("execution") else ""
        short_action = "new" if action.startswith("new-") else action.replace("-", "")
        survey_action = short_action or "unresolved"
        availability = "Planned" if survey_action == "new" else "Paths unresolved"
        next_action = "Rerun" if survey_action == "rerun" else "Allocate and run"
        state_class = "warn" if survey_action == "rerun" else "planned"
        chip_action = "rerun" if "rerun" in next_action.lower() else "plan"
        run = {"address": readable, "run": "", "result": "", "runtime": "",
               "availability": availability, "next_action": next_action,
               "chip_action": chip_action, "class": state_class}
        run = _with_evidence_context(run, context, local=False)
        chip = _lineage_chip(run, "run-detail-%s-fallback-%d" % (
            evidence_id, len(chips) + 1
        ))
        chips.append('<span class=runchip><b class="runfam %s">%s</b>%s</span>' % (
            html.escape(key, quote=True), marker, chip))
    return '<div class=runs>%s</div>' % "".join(chips) if chips else "—"


def _local_run_chip(value: str, evidence_id: str, context: dict[str, str]) -> str:
    """Show a Paper-Board-local Run as ``P jNN.tNN.rNN action``."""
    from live.evidence_bindings import _lineage_chip, _with_evidence_context
    left, _arrow, _result = value.partition("→")
    parts = [part.strip() for part in left.split("·")]
    if len(parts) < 4 or [part.lower() for part in parts[:2]] != ["page", "evidence item"]:
        return _inline_lite(value)
    action, address = parts[2], parts[3]
    readable = readable_paper_route(address) or address
    run = {"address": "P " + readable, "run": "", "result": "", "runtime": "",
           "availability": "Planned", "next_action": "Allocate and run",
           "chip_action": "plan", "class": "planned"}
    run = _with_evidence_context(run, context, local=True)
    return _lineage_chip(
        run, "run-detail-%s-local-fallback" % evidence_id, local=True
    )


def _item_card(record: dict[str, object], binding: dict[str, object] | None = None) -> str:
    """Render one Evidence Item with every Run item grouped inside it."""
    from live.evidence_bindings import _lineage_chip, _run_binding, _run_detail, _with_evidence_context
    fields = record["fields"]
    duplicates = record.get("duplicate_records", [])
    status = "conflicting records" if duplicates else str(fields.get("status", "open"))
    status_class = "ready" if any(word in status.lower() for word in ("ready", "accepted", "landed")) else "specified"
    type_ = str(fields.get("type", ""))
    evidence_id = str(record["id"])
    compact_id = wall_label(
        evidence_id, type_, str(record["title"]), str(fields.get("label", ""))
    )
    run_context = {
        "title": str(record["title"]),
        "type": type_,
        "need": str(fields.get("need", "")),
        "expected": str(fields.get("expected", "")),
        "acceptance": str(fields.get("acceptance", "")),
        "local_input": str(fields.get("local input", "")),
    }
    rows = []
    if duplicates:
        conflicting = [{key: value for key, value in record.items()
                        if key != "duplicate_records"}, *duplicates]
        rows.append(
            '<div class="evrow conflict" role="alert"><b>Duplicate identity</b>'
            '<span>This Evidence ID has %d source records. Resolve its target '
            'and contract in SHAPE before treating it as ready.'
            '<details><summary>Conflicting source records</summary><pre>%s</pre>'
            '</details></span></div>' % (
                len(conflicting), html.escape(json.dumps(conflicting, ensure_ascii=False, indent=2))
            )
        )
    for label, key in (("Needed", "expected"), ("Ready when", "acceptance")):
        value = str(fields.get(key, ""))
        if value:
            rows.append('<div class=evrow><b>%s</b><span>%s</span></div>' %
                        (label, _inline_lite(value)))

    run_details = []
    if binding is not None:
        supporting_runs = [
            _with_evidence_context(_run_binding(str(raw)), run_context, local=False)
            for raw in binding.get("supporting", [])
            if str(raw).strip() not in ("", "—", "-", "[]")
        ]
        supporting_html = "".join(
            _lineage_chip(run, "run-detail-%s-support-%d" % (evidence_id, index))
            for index, run in enumerate(supporting_runs, 1)
        ) or "—"
        run_details.extend(_run_detail(run) for run in supporting_runs)
        rows.append('<div class=evrow><b>Supporting runs</b><span class=lineage-list>%s</span></div>' %
                    supporting_html)

        local_raw = str(binding.get("local_run", ""))
        local_has_address = bool(re.match(r"^P\s+j\d+\.t\d+\.r\d+\b", local_raw))
        local_unallocated = (
            not local_has_address and (
                not local_raw
                or "not declared" in local_raw.lower()
                or "run not allocated" in local_raw.lower()
                or "ticket not allocated" in local_raw.lower()
                or local_raw.strip().lower() in (
                    "not allocated", "not surveyed yet", "not declared", "—", "-"
                )
            )
        )
        if local_unallocated:
            local_html = "not allocated"
        else:
            local = _with_evidence_context(
                _run_binding(local_raw), run_context, local=True
            )
            local_html = _lineage_chip(
                local, "run-detail-%s-local" % evidence_id, local=True
            )
            run_details.append(_run_detail(local))
        rows.append('<div class=evrow><b>Local run</b><span>%s</span></div>' % local_html)

        local_result = str(binding.get("local_result", ""))
        if not local_result or "not allocated" in local_result.lower():
            local_result = str(fields.get("has", "local Result not ready"))
        rows.append('<div class=evrow><b>Result</b><span>%s</span></div>' %
                    _inline_lite(local_result))
    else:
        supporting = str(fields.get("supporting runs", ""))
        if supporting:
            rows.append('<div class=evrow><b>Supporting runs</b><span>%s</span></div>' %
                        _run_chips(supporting, evidence_id, run_context))
        local_run = str(fields.get("local run", ""))
        if local_run:
            local_label = "not allocated" if local_run.startswith(("—", "-")) else local_run
            rows.append('<div class=evrow><b>Local run</b><span>%s</span></div>' %
                        _local_run_chip(local_label, evidence_id, run_context))
        has = str(fields.get("has", ""))
        if has:
            rows.append('<div class=evrow><b>Result</b><span>%s</span></div>' %
                        _inline_lite(has))

    paths_html = "".join(detail for detail in run_details if detail)
    paths = ('<details><summary>Run &amp; Result paths</summary>%s</details>' % paths_html
             if paths_html else "")
    details = []
    for label, key in (("Local input", "local input"),
                       ("Verified", "verified"), ("Decision", "decide")):
        value = str(fields.get(key, ""))
        if value:
            details.append('<div class=evdetail><b>%s</b><span>%s</span></div>' %
                           (label, _inline_lite(value)))
    detail_html = ('<details><summary>survey details</summary>%s</details>' % "".join(details)) if details else ""
    pills = '<span class="evpill %s">%s</span>' % (status_class, _inline_lite(status))
    if type_:
        pills += '<span class="evpill type">%s</span>' % _inline_lite(type_)
    return ('<article class=evcard id="run-%s" data-evidence-id="%s"><div class=evhead>'
            '<code class=evid title="%s">%s</code>'
            '<span class=evaddr>%s</span><span class=evtitle>%s</span><span class=evpills>%s</span>'
            '</div><div class=evrows>%s</div>%s%s</article>') % (
                html.escape(evidence_id, quote=True), html.escape(evidence_id, quote=True),
                html.escape(evidence_id, quote=True), html.escape(compact_id),
                _inline_lite(str(record["address"])), _inline_lite(str(record["title"])),
                pills, "".join(rows), paths, detail_html)


def _evidence_cards(text: str, run_text: str = "") -> str:
    from live.evidence_bindings import _run_binding_snapshot
    plan, records = _evidence_snapshot(text)
    if not records:
        return _md_lite(text)
    bindings = {
        str(record["id"]): record for record in _run_binding_snapshot(run_text)
    } if run_text else {}
    return _plan_chips(plan) + "".join(
        _item_card(record, bindings.get(str(record["id"]))) for record in records
    )
