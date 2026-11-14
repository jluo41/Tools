"""The Evidence view's copy prompt and the label details of an item."""
from __future__ import annotations

import html
import pathlib
from live.evidence_results import _evidence_blockers, _evidence_run_contract, _evidence_type

def _evidence_copy_prompt(record: dict[str, object], page_src: pathlib.Path,
                          root: pathlib.Path, board_path: str, page_path: str,
                          status: str) -> str:
    """Compose a copy-only request for the exact Evidence Item on this card."""
    kind = _evidence_type(record)
    contract = _evidence_run_contract(kind)
    fields = record.get("fields", {})
    item_id = str(record.get("id", "")).strip()
    label = str(fields.get("label", record.get("title", ""))).strip()
    target = str(record.get("address", fields.get("target", ""))).strip()
    run_id = str(fields.get("run", "") or fields.get("local run", "")).strip()
    run_status = str(fields.get("run status", "")).strip() or "not recorded"
    owner_run = str(fields.get("owner run", "")).strip()
    support = str(fields.get("supporting runs", "")).strip() or "none recorded"
    matching_runs = str(fields.get("matching page runs", "")).strip()
    if not matching_runs and run_id:
        matching_runs = "%s · %s" % (run_id, run_status)
    matching_runs = matching_runs or "none recorded"
    blockers = _evidence_blockers(fields)
    no_result = bool(fields.get("no selected result"))
    decision = str(fields.get("decision", "")).strip() or "not recorded"
    item_expected = str(fields.get("item expected", "")).strip() or "not recorded"
    item_acceptance = str(fields.get("item acceptance", "")).strip() or "not recorded"
    local_input = str(fields.get("local input", "")).strip() or "not recorded"
    local_action = str(fields.get("ledger run action", "")).strip() or "not recorded"
    local_route = str(fields.get("ledger run route", "")).strip() or "not recorded"
    result_binding = str(fields.get("ledger result binding", "")).strip() or "not recorded"
    try:
        folder = page_src.parent.relative_to(root).as_posix()
    except ValueError:
        folder = page_src.parent.name
    if folder in {"", "."}:
        folder = page_src.parent.name
    board = board_path.strip()
    if board in {"", "/"}:
        board = "Standalone Page (no Board)"
    if no_result and decision != "make":
        next_action = ("Resolve the required human Decide choice and the SHAPE/SURVEY gates first. Do not allocate or run "
                       "an Evidence Run while this item is only specified.")
    elif no_result and blockers:
        next_action = ("Report these ledger blockers and ask the owner to complete SHAPE/SURVEY before any allocation: "
                       + "; ".join(blockers) + ". Do not invent a Run or treat a planned route as an allocated Run.")
    elif no_result and "; " in matching_runs:
        next_action = ("Several Page Runs map to this item. Compare their Tickets, receipts, targets, and Results, then "
                       "ask which unique lineage to resume; do not select one by ordering.")
    elif no_result and matching_runs != "none recorded":
        next_action = ("Resume only the one recorded matching Page RE after checking its Ticket, receipt, and the current "
                       "owner gates. Do not allocate a second lineage.")
    elif no_result:
        next_action = ("The human has selected make and the ledger prerequisites are present. Recheck accepted Shape/Survey "
                       "contracts, then the owner may allocate the next typed RE if no matching Run now exists.")
    elif status.lower() in {"ready", "complete", "completed", "accepted", "resolved"}:
        next_action = ("Reuse the recorded ready Result and let the Page Evidence owner decide whether EMBED is next. "
                       "Do not create a new Evidence Run unless the owner identifies a new attempt or goal.")
    elif status.lower() in {"needs review", "in progress", "planned", "specified"}:
        next_action = ("Inspect the named item, its current Run/Result, and required human verification. Resume only the "
                       "unique matching Run when its owner contract permits; otherwise name the blocker and hold.")
    else:
        next_action = ("Reconcile this item against the current Run/Result and its Acceptance. The owner must decide "
                       "whether to resume, hold, or commission a new attempt; do not silently replace a Result.")
    lines = [
        "Use haipipe-draft-workflow and haipipe-evidence for this one typed Page Evidence item.",
        "Board: " + board,
        "Folder: " + folder,
        "Page: " + page_src.stem,
        "Page source: " + (page_path.strip() or page_src.name),
        "Evidence Item: " + item_id + (" · " + label if label else ""),
        "Target: " + (target or "not recorded"),
        "Run Type: Page.evidence-item · " + contract["name"],
        "Run identity: " + {"VALUE": "run-value-<slug>", "CITE": "run-citation-<slug>",
                            "DISPLAY": "run-display-<slug>"}.get(kind, "owner-native Evidence identity"),
        "Bounded work: " + contract["work"],
        "Owner Skill(s): " + contract["owner"],
        "Worker Skill(s): " + contract["workers"],
        "Actor: " + contract["actor"],
        "Prerequisites: " + contract["prerequisites"],
        "Item Expected: " + item_expected,
        "Item Acceptance: " + item_acceptance,
        "Local Input declaration: " + local_input,
        "Ledger Local Run: " + local_action + " · " + local_route,
        "Ledger Result binding: " + result_binding,
        "Decision: " + decision,
        "Current matching Page Run/status: " + matching_runs,
        "Current Result status: " + ("no selected Result" if no_result else status),
        "Supporting Run references: " + support,
        "Owner-native worker Run: " + (owner_run or "none recorded"),
        "Next permitted action: " + next_action,
        "Space affordance: Shown here · read-only; Copy prompt to chat. This copy action is inert until pasted and sent.",
        "Re-read the current Page, selected Outline, Evidence Item ledger, matching Run ticket/receipt, and selected Result before acting. This prompt contains item metadata only: never copy protected payloads or raw rows into chat; use their owner-governed paths.",
    ]
    display_kind = str(fields.get("display_kind", "")).strip()
    if kind == "DISPLAY" and display_kind:
        lines.insert(lines.index("Actor: " + contract["actor"]),
                     "Declared display kind: " + display_kind + "; select its renderer Skill through the Outline owner contract.")
    return "\n".join(lines)


def _copy_prompt_button(prompt: str) -> str:
    """No ⧉ chip here: the Runs panel beside each Space holds every prompt (JL 260927)."""
    return ""


def _label_details(labels: object) -> str:
    """Render resolved values with their original token in disclosure.

    The visible value is intentionally short. Opening the row exposes the
    authored token, target path, Evidence Item, Page RE, and Result path so a
    resolved number never loses its evidence identity.
    """
    if not isinstance(labels, list):
        return ""
    rows = []
    for raw in labels:
        if not isinstance(raw, dict):
            continue
        token = str(raw.get("token", "")).strip()
        reference = str(raw.get("reference") or raw.get("key") or token).strip()
        if not token:
            continue
        display = str(raw.get("display", "")).strip()
        status = str(raw.get("status", "unresolved")).strip().lower()
        visible = display if display and status not in {"pending", "unresolved", "missing"} else token
        meta = [
            ("kind", raw.get("kind", "")),
            ("reference", reference),
            ("target", raw.get("target", "")),
            ("item", raw.get("item", "")),
            ("evidence run", raw.get("page_run", "")),
            ("owner run", raw.get("run", "")),
            ("result", raw.get("result", "")),
            ("provenance", raw.get("provenance", "")),
        ]
        meta_html = "".join(
            '<span><b>%s</b> <code>%s</code></span> '
            % (html.escape(key), html.escape(str(value)))
            for key, value in meta if str(value).strip()
        )
        rows.append(
            '<details class=evidence-label-binding><summary>'
            '<span class=evidence-label-visible>%s</span>'
            '<code class=evidence-label-token>%s</code>'
            '<span class=evidence-label-state>%s</span></summary>'
            '<div class=evidence-label-meta>%s</div></details>'
            % (html.escape(visible), html.escape(token), html.escape(status), meta_html)
        )
    return '<div class=evidence-label-list>%s</div>' % "".join(rows) if rows else ""


def _label_summary(labels: object) -> str:
    """Render the small, reader-facing V/C/D index for an open card."""
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
            '<span class=evidence-label-chip title="%s"><b>%s</b><span>%s</span></span>'
            % (html.escape(token, quote=True), html.escape(kind), html.escape(visible)),
        )
    if not chips:
        return ""
    return '<div class=evidence-label-summary><span class=evidence-label-summary-title>Labels</span>%s</div>' % "".join(chips)
