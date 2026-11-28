"""The Runs related to an Evidence Item (supporting and authored), and their cards."""
from __future__ import annotations

import html
import re
from src.item_table import readable_global_run, readable_paper_route, readable_task, wall_label
from live.evidence_items import _evidence_snapshot
from live.evidence_bindings import _human_run_name, _run_binding, _run_binding_snapshot, _with_evidence_context

def _run_key(address: str, *, local: bool) -> str:
    """Return a stable identity key without conflating Paper and global Runs."""
    compact = re.sub(r"[^A-Za-z0-9]", "", address).lower()
    return ("local:" if local else "supporting:") + compact


def _record_context(record: dict[str, object]) -> dict[str, str]:
    fields = record.get("fields", {})
    return {
        "title": str(record.get("title", "")),
        "type": str(fields.get("type", "")),
        "need": str(fields.get("need", "")),
        "expected": str(fields.get("expected", "")),
        "acceptance": str(fields.get("acceptance", "")),
        "local_input": str(fields.get("local input", "")),
    }


def _support_family(fields: dict[str, object], address: str) -> str:
    wanted = re.sub(r"[^A-Za-z0-9]", "", address).lower()
    for raw in str(fields.get("supporting runs", "")).split(";"):
        parts = [part.strip() for part in raw.split(" · ") if part.strip()]
        if len(parts) >= 3 and re.sub(r"[^A-Za-z0-9]", "", parts[-1]).lower() == wanted:
            return parts[0]
    return "Supporting"


def _authored_support(raw: str, context: dict[str, str]) -> tuple[dict[str, object], str] | None:
    """Build an honest planned/unresolved pointer when the derived map is absent."""
    parts = [part.strip() for part in raw.split(" · ") if part.strip()]
    if len(parts) < 3:
        return None
    family, action, address = parts[0], parts[1].lower(), parts[-1]
    readable = readable_global_run(address) or readable_task(address) or address
    planned = action.startswith("new-")
    next_action = (
        "Rerun" if action == "rerun" else
        "Reuse Result" if action == "reuse" else
        "Run" if action == "registered" else
        "Allocate and run" if planned else "Resolve path"
    )
    run = {
        "address": readable, "run": "", "result": "", "runtime": "",
        "availability": "Planned" if planned else "Paths unresolved",
        "next_action": next_action,
        "chip_action": "plan" if planned else action,
        "class": "planned" if planned else "warn",
    }
    return _with_evidence_context(run, context, local=False), family


def _related_runs(evidence_text: str, run_text: str) -> list[dict[str, object]]:
    """Reverse the item-centric binding map into unique Run-centric records."""
    _plan, evidence_records = _evidence_snapshot(evidence_text)
    bindings = {
        str(record["id"]): record for record in _run_binding_snapshot(run_text)
    }
    related: dict[str, dict[str, object]] = {}

    def add(run: dict[str, object], record: dict[str, object], *, local: bool,
            family: str) -> None:
        key = _run_key(str(run.get("address", "")), local=local)
        if key.endswith(":"):
            return
        entry = related.setdefault(key, {
            **run, "local": local, "family": family, "evidence": [],
        })
        fields = record.get("fields", {})
        item_id = str(record["id"])
        compact = wall_label(
            item_id, str(fields.get("type", "")), str(record.get("title", "")),
            str(fields.get("label", "")),
        )
        if not any(ref["id"] == item_id for ref in entry["evidence"]):
            entry["evidence"].append({
                "id": item_id, "label": compact,
                "title": str(record.get("title", "")),
            })

    for record in evidence_records:
        item_id = str(record["id"])
        fields = record.get("fields", {})
        context = _record_context(record)
        binding = bindings.get(item_id)
        if binding:
            for raw in binding.get("supporting", []):
                if str(raw).strip() in ("", "—", "-", "[]"):
                    continue
                run = _with_evidence_context(_run_binding(str(raw)), context, local=False)
                add(run, record, local=False,
                    family=_support_family(fields, str(run["address"])))
            local_raw = str(binding.get("local_run", "")).strip()
            if local_raw and local_raw.lower() not in (
                "—", "-", "not allocated", "not surveyed yet", "not declared"
            ) and "not declared" not in local_raw.lower():
                local = _with_evidence_context(_run_binding(local_raw), context, local=True)
                add(local, record, local=True, family="Page")
        else:
            for raw in str(fields.get("supporting runs", "")).split(";"):
                authored = _authored_support(raw.strip(), context)
                if authored:
                    add(authored[0], record, local=False, family=authored[1])
            local_raw = str(fields.get("local run", "")).strip()
            match = re.search(r"(pj\d+t\d+r\d+)", local_raw, re.IGNORECASE)
            if match:
                readable = "P " + (readable_paper_route(match.group(1)) or match.group(1))
                local = _with_evidence_context({
                    "address": readable, "run": "", "result": "", "runtime": "",
                    "availability": "Planned", "next_action": "Allocate and run",
                    "chip_action": "plan", "class": "planned",
                }, context, local=True)
                add(local, record, local=True, family="Page")
    return sorted(
        related.values(),
        key=lambda run: (bool(run["local"]), str(run["address"]).lower()),
    )


def _related_run_card(run: dict[str, object], evidence_ref: dict[str, str]) -> str:
    refs = [evidence_ref]
    if run.get("run"):
        purpose = _human_run_name(str(run["run"])) or "Existing Run"
        purpose = "%s; supports “%s”." % (purpose, evidence_ref["title"])
        purpose_label = "Purpose"
    else:
        purpose = str(run.get("description", "Planned evidence Run."))
        purpose_label = "Plan"
    ref_html = "".join(
        '<button type=button class=related-evidence data-evidence-target="run-%s" '
        'title="%s">%s</button>' % (
            html.escape(str(ref["id"]), quote=True),
            html.escape(str(ref["title"]), quote=True),
            html.escape(str(ref["label"])),
        ) for ref in refs
    )
    path_rows = []
    for label, key in (("Run", "run"), ("Result", "result"), ("Runtime", "runtime")):
        path = str(run.get(key, ""))
        value = ('<code class=repo-path>%s</code>' % html.escape(path)) if path else (
            '<span class=missing>%s</span>' % (
                "not allocated" if run.get("availability") == "Planned" else "not available"
            )
        )
        path_rows.append('<div class=run-popover-path><b>%s</b>%s</div>' % (label, value))
    safe_id = re.sub(r"[^A-Za-z0-9_-]+", "-", "%s-%s" % (
        evidence_ref["id"], _run_key(str(run["address"]), local=bool(run["local"]))
    )).strip("-")
    layer = "Local · Page" if run["local"] else "Supporting · %s" % run["family"]
    return ('<article class=related-run-card id="related-run-%s" '
            'data-evidence-id="%s" data-run-address="%s" data-run-kind="%s">'
            '<div class=related-run-head><span class=related-run-layer>%s</span>'
            '<code>%s</code><span class=run-availability><b>Availability</b>%s</span>'
            '<span class=related-run-action><b>Next</b>%s</span></div>'
            '<div class=related-run-body>'
            '<div class="run-fact primary"><b>%s</b><span>%s</span></div>'
            '<div class=run-fact><b>Evidence Items</b><span class=related-evidence-list>%s</span></div>'
            '</div><details><summary>Run &amp; Result paths</summary>%s</details></article>') % (
                html.escape(safe_id, quote=True),
                html.escape(str(evidence_ref["id"]), quote=True),
                html.escape(str(run["address"]), quote=True),
                "local" if run["local"] else "supporting",
                html.escape(layer),
                html.escape(str(run["address"])), html.escape(str(run["availability"])),
                html.escape(str(run["next_action"])), purpose_label,
                html.escape(purpose), ref_html, "".join(path_rows),
            )


def _related_run_cards(evidence_text: str, run_text: str) -> tuple[str, int]:
    runs = _related_runs(evidence_text, run_text)
    if not runs:
        return ('<div class=ghost>No Supporting or Local Runs are mapped to these '
                'Evidence Items yet.</div>', 0)
    _plan, records = _evidence_snapshot(evidence_text)
    groups, mapping_count = [], 0
    for record in records:
        item_id = str(record["id"])
        fields = record.get("fields", {})
        compact = wall_label(
            item_id, str(fields.get("type", "")), str(record.get("title", "")),
            str(fields.get("label", "")),
        )
        evidence_ref = {
            "id": item_id, "label": compact,
            "title": str(record.get("title", "")),
        }
        item_runs = [
            run for run in runs
            if any(str(ref["id"]) == item_id for ref in run["evidence"])
        ]
        if not item_runs:
            continue
        mapping_count += len(item_runs)
        groups.append(
            '<section class=related-evidence-group><div class=related-group-head>'
            '<button type=button class="evid related-evidence" data-evidence-target="run-%s">%s</button>'
            '<span class=related-group-title>%s</span><span class=related-group-count>%d Run%s</span>'
            '</div>%s</section>' % (
                html.escape(item_id, quote=True), html.escape(compact),
                html.escape(str(record.get("title", ""))), len(item_runs),
                "" if len(item_runs) == 1 else "s",
                "".join(_related_run_card(run, evidence_ref) for run in item_runs),
            )
        )
    summary = ('<div class=related-summary><span class=all>%d Run mappings</span>'
               '<span>%d unique Runs</span><span>%d Evidences</span></div>') % (
                   mapping_count, len(runs), len(groups)
               )
    return summary + "".join(groups), mapping_count
