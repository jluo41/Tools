"""An Evidence Item's Run binding: read from the plan, said in words, and drawn as a card."""
from __future__ import annotations

import html
import pathlib
import re
from src.item_table import short_name
from live.evidence_text import _md_lite

_RUN_BINDING_HEADING = re.compile(
    r"^##\s+([^·]+?)\s*·\s*([^·]+?)(?:\s*·\s*(.*))?$"
)
_MARKDOWN_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


def _safe_run_href(href: str) -> str:
    href = html.unescape(href.strip())
    if href.startswith(("../", "./", "/", "https://", "http://")):
        return href
    return ""


def _run_binding_snapshot(text: str) -> list[dict[str, object]]:
    """Parse the generated pointer map into compact Evidence Item records."""
    records, current, supporting = [], None, False
    for raw in text.splitlines():
        match = _RUN_BINDING_HEADING.match(raw.strip())
        if match:
            current = {
                "id": match.group(1).strip(),
                "address": match.group(2).strip(),
                "title": (match.group(3) or "").strip(),
                "supporting": [],
                "local_run": "",
                "local_result": "",
            }
            records.append(current)
            supporting = False
            continue
        if current is None:
            continue
        stripped = raw.strip()
        if stripped == "- **Supporting Runs**:":
            supporting = True
        elif raw.startswith("  - ") and supporting:
            current["supporting"].append(stripped[2:].strip())
        elif stripped.startswith("- **Local Run**:"):
            current["local_run"] = stripped.split(":", 1)[1].strip()
            supporting = False
        elif stripped.startswith("- **Local Result**:"):
            current["local_result"] = stripped.split(":", 1)[1].strip()
            supporting = False
    return records


def _run_binding(raw: str) -> dict[str, object]:
    """Read one Run pointer; accept legacy Ticket/Receipt labels silently."""
    text = raw.strip()
    first_link = _MARKDOWN_LINK.match(text)
    first_code = re.match(r"`([^`]+)`", text)
    if first_link:
        address, run_href = first_link.group(1), _safe_run_href(first_link.group(2))
        tail = text[first_link.end():].strip().lstrip("·").strip()
    elif first_code:
        address, run_href = first_code.group(1), ""
        tail = text[first_code.end():].strip().lstrip("·").strip()
    else:
        address, _sep, tail = text.partition(" · ")
        run_href = ""
    links = {
        label.lower(): _safe_run_href(href)
        for label, href in _MARKDOWN_LINK.findall(tail)
    }
    parts = [
        _MARKDOWN_LINK.sub(lambda match: match.group(1), part).strip()
        for part in tail.split(" · ") if part.strip()
    ]
    run_path = links.get("run", "") or links.get("ticket", "") or run_href
    result_path = links.get("result", "")
    lowered = " · ".join(parts).lower()
    explicitly_unallocated = (
        "run not allocated" in lowered
        or "ticket not allocated" in lowered
        or "not allocated" in address.lower()
    )
    if run_path and result_path:
        availability = "Run + Result"
    elif run_path:
        availability = "Run exists · Result missing"
    elif explicitly_unallocated or any(
        token in lowered for token in ("newrun", "new-run", " · new ·")
    ):
        availability = "Planned"
    else:
        availability = "Paths unresolved"

    if "rerun" in lowered:
        next_action = "Rerun" if run_path else "Resolve path, then rerun"
    elif result_path:
        next_action = "Reuse Result"
    elif run_path:
        next_action = "Run"
    elif availability == "Planned":
        next_action = "Allocate and run"
    else:
        next_action = "Resolve path"

    if result_path:
        state_class = "ready"
    elif "rerun" in lowered or run_path or availability == "Paths unresolved":
        state_class = "warn"
    else:
        state_class = "planned"
    if "rerun" in next_action.lower():
        chip_action = "rerun"
    elif next_action == "Reuse Result":
        chip_action = "reuse"
    elif availability == "Planned":
        chip_action = "plan"
    elif next_action == "Run":
        chip_action = "run"
    else:
        chip_action = "resolve"
    return {
        "address": address.strip(),
        "href": run_path,
        "run": run_path,
        "result": result_path,
        "runtime": links.get("runtime", "") or links.get("receipt", ""),
        "availability": availability,
        "next_action": next_action,
        "chip_action": chip_action,
        "class": state_class,
        "title": " · ".join([address.strip()] + parts),
    }


def _human_run_name(path: str) -> str:
    """Turn a Ticket filename into a short reader-facing purpose phrase."""
    stem = pathlib.PurePosixPath(path).stem
    stem = re.sub(r"^r\d+[_-]?", "", stem, flags=re.IGNORECASE)
    stem = re.sub(r"[_-]+", " ", stem)
    stem = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", stem)
    return re.sub(r"\s+", " ", stem).strip()


def _survey_sentence(note: str, address: str) -> str:
    """Pick the authored SURVEY sentence about one Supporting Run, if any."""
    if not note:
        return ""
    compact = re.sub(r"[^A-Za-z0-9]", "", address).lower()
    for sentence in re.split(r"(?<=[.!?])\s+", note.strip()):
        if compact and compact in re.sub(r"[^A-Za-z0-9]", "", sentence).lower():
            return sentence.strip()
    return ""


def _with_evidence_context(
    run: dict[str, object], context: dict[str, str], *, local: bool
) -> dict[str, object]:
    """Attach a useful purpose/plan without creating another stored authority."""
    enriched = dict(run)
    title = context.get("title", "this Evidence Item")
    expected = context.get("expected", "").strip()
    payload = expected.split("·", 1)[-1].strip() if expected else "the required evidence"
    if run.get("run"):
        ticket_name = _human_run_name(str(run["run"]))
        description = "%s; supports “%s”." % (
            ticket_name or "Existing Supporting Run", title
        )
        description_label = "Purpose"
    elif local:
        description = "Produce the page-local %s Result for “%s”: %s." % (
            context.get("type", "evidence") or "evidence", title, payload
        )
        description_label = "Plan"
    else:
        description = "Design a Supporting Run for “%s” to provide %s." % (
            title, payload
        )
        description_label = "Plan"
    note = context.get("local_input", "").strip()
    enriched["description"] = description
    enriched["description_label"] = description_label
    enriched["survey_note"] = note if local else _survey_sentence(
        note, str(run.get("address", ""))
    )
    return enriched


def _run_popover(run: dict[str, object], popover_id: str) -> str:
    """Render one calm Run detail card with non-navigating path text."""
    facts = [
        '<div class="run-fact primary"><b>%s</b><span>%s</span></div>' % (
            html.escape(str(run.get("description_label", "Purpose"))),
            html.escape(str(run.get("description", "Surveyed Run for this Evidence Item."))),
        )
    ]
    if run.get("survey_note"):
        facts.append('<div class=run-fact><b>Survey note</b><span>%s</span></div>' %
                     html.escape(str(run["survey_note"])))
    facts.extend([
        '<div class=run-fact><b>Availability</b><span>%s</span></div>' %
        html.escape(str(run["availability"])),
        '<div class=run-fact><b>Next action</b><span>%s</span></div>' %
        html.escape(str(run["next_action"])),
    ])
    paths = []
    path_rows = [("Run", "run"), ("Result", "result")]
    if run.get("runtime"):
        path_rows.append(("Runtime", "runtime"))
    for label, key in path_rows:
        href = str(run[key])
        if href:
            # Raw scripts and receipts are commonly served as downloads. The
            # Run chip already opens this detail, so paths remain selectable
            # text rather than becoming a second navigation door.
            value = '<code class=repo-path>%s</code>' % html.escape(href)
        else:
            value = '<span class=missing>%s</span>' % (
                "not allocated" if str(run["class"]) == "planned" else "not available"
            )
        paths.append('<div class=run-popover-path><b>%s</b>%s</div>' % (label, value))
    return ('<div id="%s" popover class=run-popover><div class=run-popover-head>'
            '<div class=run-popover-title><code>%s</code><span class=run-availability>%s</span></div>'
            '<button type=button class=run-close popovertarget="%s" '
            'popovertargetaction=hide aria-label="Close Run detail">×</button></div>'
            '<div class=run-popover-body>%s%s</div></div>') % (
                html.escape(popover_id, quote=True), html.escape(str(run["address"])),
                html.escape(str(run["availability"])), html.escape(popover_id, quote=True),
                "".join(facts), "".join(paths))


def _lineage_chip(run: dict[str, object], popover_id: str, *, local: bool = False) -> str:
    """Open Run detail in place instead of sending a chip to a raw script."""
    return ('<button type=button class="lineage-chip %s" popovertarget="%s" '
            'data-run-address="%s" data-run-kind="%s" title="Inspect %s">'
            '<code>%s</code><small>%s</small>'
            '</button>%s' % (
                html.escape(str(run["class"]), quote=True),
                html.escape(popover_id, quote=True),
                html.escape(str(run["address"]), quote=True),
                "local" if local else "supporting",
                html.escape(str(run["address"]), quote=True),
                html.escape(str(run["address"])), html.escape(str(run["chip_action"])),
                _run_popover(run, popover_id)))


def _run_detail(run: dict[str, object]) -> str:
    if not run["run"] and not run["result"] and not run.get("runtime"):
        return ""
    links = []
    path_rows = [("Run", "run"), ("Result", "result")]
    if run.get("runtime"):
        path_rows.append(("Runtime", "runtime"))
    for label, key in path_rows:
        href = str(run[key])
        if href:
            links.append('<span class=run-path><b>%s</b><code>%s</code></span>' %
                         (label, html.escape(href)))
        elif label == "Result":
            links.append('<span class="run-path missing"><b>Result</b>'
                         '<span>not available</span></span>')
    return ('<div class=run-detail><code>%s</code><span class=run-detail-links>%s</span></div>' %
            (html.escape(str(run["address"])), "".join(links)))


def _run_binding_card(record: dict[str, object]) -> str:
    evidence_id = str(record["id"])
    identity = re.match(r"^(E\d+)(?:-([A-Z]+))?(?:-(.*))?$", evidence_id)
    short_id = short_name(evidence_id) if identity else evidence_id
    type_ = identity.group(2) if identity and identity.group(2) else ""
    slug = identity.group(3) if identity and identity.group(3) else ""
    short_title = slug.replace("-", " ") if slug else str(record["title"])
    run_context = {
        "title": str(record["title"]) or short_title,
        "type": type_,
        "need": "",
        "expected": "",
        "acceptance": "",
        "local_input": "",
    }
    runs = [
        _with_evidence_context(_run_binding(str(raw)), run_context, local=False)
        for raw in record["supporting"]
        if str(raw).strip() not in ("", "—", "-", "[]")
    ]
    chips = "".join(
        _lineage_chip(run, "run-detail-%s-support-%d" % (evidence_id, index))
        for index, run in enumerate(runs, 1)
    ) or "—"
    details = "".join(_run_detail(run) for run in runs)

    local_run, local_result = str(record["local_run"]), str(record["local_result"])
    local_has_address = bool(re.match(r"^P\s+j\d+\.t\d+\.r\d+\b", local_run))
    local_unallocated = (
        not local_has_address and (
            not local_run
            or "not declared" in local_run.lower()
            or "run not allocated" in local_run.lower()
            or "ticket not allocated" in local_run.lower()
            or local_run.strip().lower() in (
                "not allocated", "not surveyed yet", "not declared", "—", "-"
            )
        )
    )
    if local_unallocated:
        local_html = "<span>not allocated</span>"
    elif local_run:
        local = _with_evidence_context(
            _run_binding(local_run), run_context, local=True
        )
        local_html = _lineage_chip(
            local, "run-detail-%s-local" % evidence_id, local=True
        )
        details += _run_detail(local)
        if not local_result or "not allocated" in local_result.lower():
            local_html += "<span>no result</span>"
        else:
            local_html += "<span>Result · %s</span>" % html.escape(local_result)
    else:
        local_html = "<span>—</span>"
    detail_html = ('<details><summary>Run &amp; Result paths</summary>%s</details>' % details) if details else ""
    type_html = '<span class=runmap-type>%s</span>' % html.escape(type_) if type_ else ""
    return ('<article class=runmap-card id="run-%s"><div class=runmap-head title="%s">'
            '<code class=runmap-eid>%s</code><code class=runmap-addr>%s</code>'
            '<span class=runmap-title>%s</span>%s</div>'
            '<div class=runmap-line><span class=runmap-label>Supporting</span>'
            '<div class=lineage-list>%s</div></div>'
            '<div class=runmap-local><b>Local</b>%s</div>%s</article>') % (
                html.escape(evidence_id, quote=True), html.escape(str(record["title"]), quote=True),
                html.escape(short_id), html.escape(str(record["address"])),
                html.escape(short_title), type_html, chips, local_html, detail_html)


def _run_binding_cards(text: str) -> str:
    records = _run_binding_snapshot(text)
    if not records:
        return _md_lite(text, heading_prefix="run-")
    return "".join(_run_binding_card(record) for record in records)
