"""Outline's internal Evidence Workspace (JL 260903).

"We still have the subfolder for bibex, etc, but we just need one evidence
plugin, to present bibex, display, etc." So this mixin owns PRESENTATION
ONLY: a live GET composing five segments — Evidence Items (the generated
outline/<stem>-evidence.md snapshot joined to
outline/evidence/supporting-runs lineage),
📚 Citations (the bibex saved workbench), 🧮 Values (the live /_board/value
route), 🖼 Displays (the display saved view), and 🔗 PageX (the borrow view),
with pens inline; exact-file cards expose Page evidence and
whole-Folder cards expose Page/Task Face status). Storage, writers,
walls and the three human gates (verified: / read: / accepted:) stay with the
lane contracts (`haipipe-plugin-evidence` is the paper contract for this
file). Like the 🧮 tab: no storage, no writer, nothing stored, never stale.

A segment whose saved view does not exist yet is BUILT ON CLICK through the
lane's own POST route (/_board/bibex, /_board/display, /_board/pagex), which
is the same pen the old separate tabs pressed.
"""
from __future__ import annotations

import html
import json
import pathlib
import re

from src.common import evidence_run_dirs
from src.item_table import (readable_global_run, readable_paper_route,
                            readable_task, wall_label)

_CSS = """
:root{--bg:#ffffff;--fg:#1c1d1f;--mut:#71727a;--line:#e4e4e7;--card:#f7f7f8;
 --acc:#3b6ea5;--ok:#287443;--warn:#a95b12}
@media(prefers-color-scheme:dark){:root{--bg:#161719;--fg:#e8e8e6;--mut:#9a9a97;
 --line:#2c2e33;--card:#1d1f23;--acc:#7aa7d8;--ok:#74b68a;--warn:#e0a05c}}
body{margin:0;background:var(--bg);color:var(--fg);
 font:15px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
header{padding:12px 16px 7px}
.embedded header{display:none}.embedded nav{top:0;padding-top:6px;padding-bottom:6px}
h1{font-size:16px;margin:0}
.mut{color:var(--mut);font-size:12.5px}.lead{margin:2px 0 0;color:var(--mut);font-size:13px}
nav{display:flex;gap:6px;overflow-x:auto;padding:8px 16px;border-bottom:1px solid var(--line);
 position:sticky;top:0;background:var(--bg);z-index:1}
nav button{border:1px solid var(--line);background:var(--card);color:var(--fg);
 border-radius:6px;padding:4px 10px;font-size:13px;cursor:pointer;white-space:nowrap;flex:none}
nav button.on{border-color:var(--acc);color:var(--acc);font-weight:600}
#items{padding:12px 16px 20px;max-width:none}
#items pre{background:var(--card);padding:8px 10px;border-radius:6px;
 overflow-x:auto;font:12.5px ui-monospace,Menlo,monospace}
#items code{font:12.5px ui-monospace,Menlo,monospace;background:var(--card);
 padding:0 3px;border-radius:4px}
#items h2{font-size:15px;margin:14px 0 4px}
#items h3{font-size:13.5px;margin:12px 0 3px}
#items .run-focus{outline:2px solid var(--acc);outline-offset:4px;border-radius:9px}
#items ul{margin:4px 0;padding-left:22px}
.evsummary{display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin:0 0 12px}
.evsummary span{font-size:11.5px;color:var(--mut);border:1px solid var(--line);border-radius:999px;padding:1px 7px}
.evsummary .cycle{color:var(--acc);border-color:var(--acc);font-weight:650}.evsummary .approved{color:var(--ok);border-color:var(--ok)}
.evcard{border:1px solid var(--line);border-radius:9px;margin:9px 0;background:var(--bg);overflow:hidden}
.evhead{display:flex;align-items:baseline;gap:7px;flex-wrap:wrap;padding:9px 10px 7px}
.evid{font:650 11px ui-monospace,Menlo,monospace;color:var(--acc);border:1px solid var(--line);border-radius:5px;padding:0 5px;white-space:nowrap}
.evtitle{font-weight:650;line-height:1.4;flex:1;min-width:10em}.evaddr{color:var(--mut);font-size:12px;white-space:nowrap}
.evpills{display:flex;gap:5px;align-items:center}.evpill{font:650 10.5px -apple-system,sans-serif;text-transform:uppercase;letter-spacing:.035em;border-radius:999px;padding:1px 7px;border:1px solid currentColor;white-space:nowrap}
.evpill.specified{color:var(--warn)}.evpill.ready{color:var(--ok)}.evpill.type{color:var(--acc)}
.evrows{border-top:1px solid var(--line);padding:5px 10px 7px}.evrow{display:grid;grid-template-columns:5.8em minmax(0,1fr);gap:7px;padding:3px 0;font-size:13px;line-height:1.48}
.evrow b{font:600 10.5px -apple-system,sans-serif;color:var(--mut);text-transform:uppercase;letter-spacing:.025em}.evrow span{overflow-wrap:anywhere}
.runs{display:flex;gap:4px;flex-wrap:wrap}.runchip{display:inline-flex;align-items:baseline;gap:3px;border:1px solid var(--line);border-radius:5px;padding:1px 5px;font-size:11.5px;line-height:1.4}.runchip .runfam{font:750 9px ui-monospace,Menlo,monospace;color:var(--mut)}.runchip .runfam.discovery{color:#7055a5}.runchip .runfam.execution{color:var(--acc)}.runchip .runfam.paper{color:#356b5d}.runchip .runact{color:var(--mut);font:600 10px ui-monospace,Menlo,monospace}.runchip code{background:none!important;padding:0!important}
.evcard details{border-top:1px solid var(--line);padding:5px 10px 7px;color:var(--mut);font-size:12.5px}.evcard summary{cursor:pointer;color:var(--mut)}.evdetail{margin-top:5px}.evdetail b{display:inline-block;min-width:6.5em;color:var(--mut);font-size:10.5px;text-transform:uppercase;letter-spacing:.025em}
.runmap-card{border:1px solid var(--line);border-radius:9px;margin:8px 0;background:var(--bg);overflow:hidden}
.runmap-head{display:grid;grid-template-columns:auto auto minmax(8em,1fr) auto;align-items:center;gap:7px;padding:8px 10px 6px}
.runmap-eid,.runmap-addr{font:650 11px ui-monospace,Menlo,monospace;white-space:nowrap}.runmap-eid{color:var(--acc)}.runmap-addr{color:var(--mut)}
.runmap-title{font-weight:650;line-height:1.35;min-width:0}.runmap-type{font:650 9.5px -apple-system,sans-serif;color:var(--acc);border:1px solid var(--acc);border-radius:999px;padding:0 6px;letter-spacing:.03em}
.runmap-line{display:grid;grid-template-columns:5.4em minmax(0,1fr);gap:7px;align-items:start;border-top:1px solid var(--line);padding:7px 10px}
.runmap-label{font:600 10px -apple-system,sans-serif;color:var(--mut);text-transform:uppercase;letter-spacing:.035em;padding-top:3px}
.lineage-list{display:flex;flex-wrap:wrap;gap:5px;min-width:0}.lineage-chip{display:inline-flex;align-items:center;gap:5px;max-width:100%;border:1px solid var(--line);border-radius:999px;padding:2px 7px;color:var(--fg);text-decoration:none;background:var(--card);font-size:11px;line-height:1.35}.lineage-chip:hover{border-color:var(--acc)}
.lineage-chip:before{content:'';width:6px;height:6px;border-radius:50%;background:var(--mut);flex:none}.lineage-chip.ready:before{background:var(--ok)}.lineage-chip.warn:before{background:var(--warn)}.lineage-chip.planned:before{background:var(--mut)}.lineage-chip code{background:none!important;padding:0!important;font-size:11.5px!important;color:inherit}.lineage-chip small{color:var(--mut);font-size:9.5px;white-space:nowrap}
.runmap-local{display:flex;align-items:center;flex-wrap:wrap;gap:6px;border-top:1px solid var(--line);padding:4px 10px;color:var(--mut);font-size:11.5px;overflow-wrap:anywhere}.runmap-local b{font-size:9.5px;text-transform:uppercase;letter-spacing:.035em}.runmap-card details{border-top:1px solid var(--line);padding:4px 10px 6px;color:var(--mut);font-size:11.5px}.runmap-card summary{cursor:pointer;font-size:11px}.run-detail{display:grid;grid-template-columns:9.5em minmax(0,1fr);gap:6px;padding:4px 0}.run-detail>code{background:none!important;padding:0!important;color:var(--fg)}.run-detail-links{display:grid;gap:3px;min-width:0}.run-path{display:grid;grid-template-columns:3.5em minmax(0,1fr);gap:6px;align-items:start;color:var(--fg);text-decoration:none;min-width:0}.run-path b{font-size:10px;text-transform:uppercase;color:var(--mut)}.run-path code{background:none!important;padding:0!important;white-space:normal;overflow-wrap:anywhere;word-break:break-word}.run-detail .missing{color:var(--mut)}
@media(max-width:560px){#items{padding:10px 10px 18px}.runmap-head{grid-template-columns:auto minmax(0,1fr) auto}.runmap-addr{display:none}.runmap-line{grid-template-columns:1fr}.runmap-label{padding:0}.lineage-list{gap:4px}.run-detail{grid-template-columns:1fr;gap:1px}.run-path{grid-template-columns:3.2em minmax(0,1fr)}}
.ghost{color:var(--mut);padding:24px 0;font-size:13.5px}
#seg{display:none;border:0;width:100%;height:calc(100vh - 92px)}
"""


def _md_lite(text: str, heading_prefix: str = "") -> str:
    """Enough markdown for the generated evidence snapshot: headings,
    bullets, fences, bold, inline code. Never trusted with raw HTML."""
    out, in_pre, in_ul = [], False, False
    for raw in text.split("\n"):
        line = html.escape(raw, quote=False)
        if raw.strip().startswith("```"):
            if in_ul: out.append("</ul>"); in_ul = False
            out.append("<pre>" if not in_pre else "</pre>")
            in_pre = not in_pre
            continue
        if in_pre:
            out.append(line)
            continue
        line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
        line = re.sub(r"`([^`]+)`", r"<code>\1</code>", line)

        def link(match):
            label, href = match.group(1), html.unescape(match.group(2))
            # The binding map writes only repo-relative Run/Result links;
            # permit ordinary web links too, but never let a markdown field
            # inject a script/data URL into the live Board surface.
            if not (href.startswith(("../", "./", "/", "https://", "http://"))):
                return label
            return ('<a href="%s" target="_blank" rel="noopener">%s</a>' %
                    (html.escape(href, quote=True), label))

        line = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, line)
        s = raw.lstrip()
        heading_attr = ""
        if heading_prefix and s.startswith(("## ", "### ")):
            heading = s.lstrip("# ").split(" ·", 1)[0].strip()
            safe = re.sub(r"[^A-Za-z0-9_-]+", "-", heading).strip("-")
            if safe:
                heading_attr = ' id="%s"' % html.escape(
                    heading_prefix + safe, quote=True
                )
        if s.startswith("### "):
            if in_ul: out.append("</ul>"); in_ul = False
            out.append("<h3%s>%s</h3>" % (heading_attr, line.lstrip()[4:]))
        elif s.startswith("## "):
            if in_ul: out.append("</ul>"); in_ul = False
            out.append("<h2%s>%s</h2>" % (heading_attr, line.lstrip()[3:]))
        elif s.startswith("- "):
            if not in_ul: out.append("<ul>"); in_ul = True
            out.append("<li>%s</li>" % line.lstrip()[2:])
        elif not s:
            if in_ul: out.append("</ul>"); in_ul = False
        else:
            out.append("<p>%s</p>" % line)
    if in_ul: out.append("</ul>")
    if in_pre: out.append("</pre>")
    return "\n".join(out)


_ITEM_HEADING = re.compile(r"^###\s+([^·]+?)\s*·\s*(.*)$")
_FIELD = re.compile(r"^-\s+\*\*([^*]+?)\*\*\s*:\s*(.*)$")


def _inline_lite(text: str) -> str:
    """Safe inline rendering for the compact Evidence Item cards."""
    line = html.escape(text.strip(), quote=False)
    line = re.sub(r"`([^`]+)`", r"<code>\1</code>", line)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)


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
    return plan, records


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


def _run_chips(value: str) -> str:
    """Show compact family, action, and dotted address without inventing rNN."""
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
        chips.append('<span class=runchip title="%s · %s"><b class="runfam %s">%s</b><code>%s</code><span class=runact>%s</span></span>' % (
            html.escape(family or "Run", quote=True), html.escape(action or "unspecified", quote=True),
            html.escape(key, quote=True), marker, html.escape(readable), html.escape(short_action)))
    return '<div class=runs>%s</div>' % "".join(chips) if chips else "—"


def _local_run_chip(value: str) -> str:
    """Show a Paper-Board-local Run as ``P jNN.tNN.rNN action``."""
    left, _arrow, _result = value.partition("→")
    parts = [part.strip() for part in left.split("·")]
    if len(parts) < 4 or [part.lower() for part in parts[:2]] != ["page", "evidence item"]:
        return _inline_lite(value)
    action, address = parts[2], parts[3]
    readable = readable_paper_route(address) or address
    short_action = "new" if action.startswith("new-") else action.replace("-", "")
    return ('<span class=runchip title="Paper Board-local · %s"><b class="runfam paper">P</b>'
            '<code>%s</code><span class=runact>%s</span></span>') % (
                html.escape(action or "unspecified", quote=True),
                html.escape(readable), html.escape(short_action))


def _item_card(record: dict[str, object], binding: dict[str, object] | None = None) -> str:
    """Render one Evidence Item with every Run item grouped inside it."""
    fields = record["fields"]
    status = str(fields.get("status", "open"))
    status_class = "ready" if any(word in status.lower() for word in ("ready", "accepted", "landed")) else "specified"
    type_ = str(fields.get("type", ""))
    evidence_id = str(record["id"])
    compact_id = wall_label(
        evidence_id, type_, str(record["title"]), str(fields.get("label", ""))
    )
    rows = []
    for label, key in (("Needed", "expected"), ("Ready when", "acceptance")):
        value = str(fields.get(key, ""))
        if value:
            rows.append('<div class=evrow><b>%s</b><span>%s</span></div>' %
                        (label, _inline_lite(value)))

    run_details = []
    if binding is not None:
        supporting_runs = [
            _run_binding(str(raw)) for raw in binding.get("supporting", [])
            if str(raw).strip() not in ("", "—", "-", "[]")
        ]
        supporting_html = "".join(_lineage_chip(run) for run in supporting_runs) or "—"
        run_details.extend(_run_detail(run) for run in supporting_runs)
        rows.append('<div class=evrow><b>Supporting runs</b><span class=lineage-list>%s</span></div>' %
                    supporting_html)

        local_raw = str(binding.get("local_run", ""))
        local_unallocated = (
            not local_raw
            or "run not allocated" in local_raw.lower()
            or "ticket not allocated" in local_raw.lower()
            or local_raw.strip().lower() in ("not allocated", "not surveyed yet", "—", "-")
        )
        if local_unallocated:
            local_html = "not allocated"
        else:
            local = _run_binding(local_raw)
            local_html = _lineage_chip(local)
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
                        _run_chips(supporting))
        local_run = str(fields.get("local run", ""))
        if local_run:
            local_label = "not allocated" if local_run.startswith(("—", "-")) else local_run
            rows.append('<div class=evrow><b>Local run</b><span>%s</span></div>' %
                        _local_run_chip(local_label))
        has = str(fields.get("has", ""))
        if has:
            rows.append('<div class=evrow><b>Result</b><span>%s</span></div>' %
                        _inline_lite(has))

    paths_html = "".join(detail for detail in run_details if detail)
    paths = ('<details><summary>Run &amp; Result paths</summary>%s</details>' % paths_html
             if paths_html else "")
    details = []
    for label, key in (("Survey note", "local input"), ("PageX", "pagex bindings"),
                       ("Decision", "decide")):
        value = str(fields.get(key, ""))
        if value and not (key == "pagex bindings" and value in ("[]", "—", "-")):
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
    plan, records = _evidence_snapshot(text)
    if not records:
        return _md_lite(text)
    bindings = {
        str(record["id"]): record for record in _run_binding_snapshot(run_text)
    } if run_text else {}
    return _plan_chips(plan) + "".join(
        _item_card(record, bindings.get(str(record["id"]))) for record in records
    )


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
    lowered = " · ".join(parts).lower()
    if ("run not allocated" in lowered or "ticket not allocated" in lowered
            or "not allocated" in address.lower()):
        state, state_class = "new", "planned"
    elif ("result not found" in lowered or "no result" in lowered
          or "no result receipt" in lowered or "run only" in lowered):
        state, state_class = "run only", "warn"
    elif "rerun" in lowered:
        state, state_class = "rerun", "warn"
    elif links.get("result") or links.get("receipt"):
        state, state_class = "ready", "ready"
    else:
        action = parts[0].lower() if parts else "run"
        state = "new" if action in ("newrun", "new-run") else action.replace("-", " ")
        state_class = "planned"
    run_path = links.get("run", "") or links.get("ticket", "") or run_href
    result_path = links.get("result", "") or links.get("receipt", "")
    return {
        "address": address.strip(),
        "href": run_path,
        "run": run_path,
        "result": result_path,
        "state": state,
        "class": state_class,
        "title": " · ".join([address.strip()] + parts),
    }


def _lineage_chip(run: dict[str, object]) -> str:
    tag = "a" if run["href"] else "span"
    link = (' href="%s" target="_blank" rel="noopener"' %
            html.escape(str(run["href"]), quote=True)) if run["href"] else ""
    return ('<%s class="lineage-chip %s"%s title="%s"><code>%s</code><small>%s</small></%s>' % (
        tag, html.escape(str(run["class"]), quote=True), link,
        html.escape(str(run["title"]), quote=True), html.escape(str(run["address"])),
        html.escape(str(run["state"])), tag))


def _run_detail(run: dict[str, object]) -> str:
    if not run["run"] and not run["result"]:
        return ""
    links = []
    for label, key in (("Run", "run"), ("Result", "result")):
        href = str(run[key])
        if href:
            links.append('<a class=run-path href="%s" target="_blank" rel="noopener">'
                         '<b>%s</b><code>%s</code></a>' %
                         (html.escape(href, quote=True), label, html.escape(href)))
        elif label == "Result":
            links.append('<span class="run-path missing"><b>Result</b>'
                         '<span>not available</span></span>')
    return ('<div class=run-detail><code>%s</code><span class=run-detail-links>%s</span></div>' %
            (html.escape(str(run["address"])), "".join(links)))


def _run_binding_card(record: dict[str, object]) -> str:
    evidence_id = str(record["id"])
    identity = re.match(r"^(E\d+)(?:-([A-Z]+))?(?:-(.*))?$", evidence_id)
    short_id = identity.group(1) if identity else evidence_id
    type_ = identity.group(2) if identity and identity.group(2) else ""
    slug = identity.group(3) if identity and identity.group(3) else ""
    short_title = slug.replace("-", " ") if slug else str(record["title"])
    runs = [
        _run_binding(str(raw)) for raw in record["supporting"]
        if str(raw).strip() not in ("", "—", "-", "[]")
    ]
    chips = "".join(_lineage_chip(run) for run in runs) or "—"
    details = "".join(_run_detail(run) for run in runs)

    local_run, local_result = str(record["local_run"]), str(record["local_result"])
    local_unallocated = (
        not local_run
        or "run not allocated" in local_run.lower()
        or "ticket not allocated" in local_run.lower()
        or local_run.strip().lower() in ("not allocated", "not surveyed yet", "—", "-")
    )
    if local_unallocated:
        local_html = "<span>not allocated</span>"
    elif local_run:
        local = _run_binding(local_run)
        local_html = _lineage_chip(local)
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


def render(page_src: pathlib.Path, path_q: str, file_q: str) -> str:
    stem = page_src.stem
    folded = page_src.parent.name == stem
    folder = page_src.parent if folded else None
    ev = (folder / "outline" / f"{stem}-evidence.md") if folder else \
         (page_src.parent / "outline" / f"{stem}-evidence.md")
    page_home = folder or page_src.parent
    runmap = next((d / f"{stem}-run-bindings.md"
                   for d in evidence_run_dirs(page_home)
                   if (d / f"{stem}-run-bindings.md").is_file()), None)
    run_text = runmap.read_text(encoding="utf-8") if runmap else ""
    if ev.exists():
        body = _evidence_cards(ev.read_text(encoding="utf-8"), run_text)
    else:
        body = ("<div class=ghost>No evidence snapshot yet: "
                "<code>cli/evidence-status.py</code> (or an OUTLINE pass) "
                "writes <code>outline/%s-evidence.md</code>.</div>" % html.escape(stem))
    ctx = json.dumps({"path": path_q, "file": file_q, "stem": stem,
                      "folded": folded})
    return f"""<!doctype html><meta charset=utf-8>
<title>🧭 Outline · Evidence Workspace · {html.escape(stem)}</title>
<style>{_CSS}</style>
<header><h1>Evidence Workspace · {html.escape(stem)}</h1>
<p class=lead>what each bullet needs, what supports it, and what is ready</p></header>
<nav>
<button class=on data-seg=items>🧾 Evidence Items</button>
<button data-seg=bibex>📚 Citations</button>
<button data-seg=value>🧮 Values</button>
<button data-seg=display>🖼 Displays</button>
<button data-seg=pagex>🔗 PageX</button>
</nav>
<div id=items>{body}</div>
<iframe id=seg></iframe>
<script>
(function () {{
  'use strict';
  var CTX = {ctx};
  function savedUrl(plugin, ext) {{
    var p = decodeURIComponent(CTX.path || '');
    var cut = p.lastIndexOf('/board/');
    var base = cut >= 0 ? p.slice(0, cut)
             : (/\\.md$/.test(p) ? p.slice(0, p.lastIndexOf('/')) : '');
    if (!base) return '';
    var m = (CTX.file || '').match(/^(.*)\\/([^\\/]+)\\/\\2\\.md$/);
    if (m) return base + '/' + m[1] + '/' + m[2] + '/outline/evidence/' + plugin + '/' + m[2] + (ext || '-view.html');
    return base + '/outline/evidence/' + plugin + '/' + CTX.stem + (ext || '-view.html');
  }}
  var LANES = {{
    bibex:   {{ext: '-bib.html',  route: 'bibex'}},
    display: {{ext: '-view.html', route: 'display'}},
    pagex:   {{ext: '-view.html', route: 'pagex'}},
    value:   {{live: '/_board/value?path=' + encodeURIComponent(CTX.path)
                    + '&file=' + encodeURIComponent(CTX.file)}}
  }};
  var frame = document.getElementById('seg'),
      staticSegs = {{items: document.getElementById('items')}};
  function show(id, btn) {{
    var all = document.querySelectorAll('nav button');
    for (var i = 0; i < all.length; i++) all[i].className = '';
    btn.className = 'on';
    if (staticSegs[id]) {{
      frame.style.display = 'none';
      Object.keys(staticSegs).forEach(function (key) {{ staticSegs[key].style.display = key === id ? 'block' : 'none'; }});
      return;
    }}
    Object.keys(staticSegs).forEach(function (key) {{ staticSegs[key].style.display = 'none'; }});
    frame.style.display = 'block';
    var lane = LANES[id];
    if (lane.live) {{ frame.src = lane.live; return; }}
    var url = savedUrl(id, lane.ext);
    fetch(url, {{method: 'HEAD'}}).then(function (r) {{
      if (r.ok) {{ frame.src = url + '?embed'; return; }}
      /* not built yet: press the lane's own pen, then load what it names */
      fetch('/_board/' + lane.route, {{
        method: 'POST', headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{path: CTX.path, file: CTX.file}})
      }}).then(function (r2) {{ return r2.json(); }})
        .then(function (j) {{
          if (j.ok && j.url) frame.src = j.url + '?embed';
          else frame.srcdoc = '<p style="font:13px sans-serif;color:#888;padding:20px">⚠ ' +
                              ((j && j.err) || 'the ' + id + ' view failed') + '</p>';
        }});
    }});
  }}
  var btns = document.querySelectorAll('nav button');
  for (var i = 0; i < btns.length; i++) {{
    (function (b) {{
      b.addEventListener('click', function () {{ show(b.getAttribute('data-seg'), b); }});
    }})(btns[i]);
  }}
  var params = new URLSearchParams(location.search),
      requestedSeg = params.get('seg') || '',
      requestedFocus = params.get('focus') || '';
  if (params.get('embed') === '1') document.documentElement.classList.add('embedded');
  try {{
    requestedSeg = localStorage.getItem('board-outline-evidence-seg') || requestedSeg;
    requestedFocus = localStorage.getItem('board-outline-evidence-focus') || requestedFocus;
    localStorage.removeItem('board-outline-evidence-seg');
    localStorage.removeItem('board-outline-evidence-focus');
  }} catch (e) {{}}
  /* Old Outline links remain valid after By bullet and Run links merge. */
  if (requestedSeg === 'runlinks' || requestedSeg === 'bybullet') requestedSeg = 'items';
  if (requestedSeg) {{
    var requestedButton = document.querySelector('nav button[data-seg="' +
                                                   requestedSeg + '"]');
    if (requestedButton) show(requestedSeg, requestedButton);
  }}
  if (requestedFocus) {{
    setTimeout(function () {{
      var target = document.getElementById(requestedFocus);
      if (target) {{
        target.classList.add('run-focus');
        target.setAttribute('tabindex', '-1');
        target.focus({{preventScroll: true}});
        target.scrollIntoView({{block: 'start'}});
      }}
    }}, 0);
  }}
}})();
</script>"""


class EvidenceTabMixin:
    """Compatibility route for Outline's internal read-only workspace."""

    # ---- GET/HEAD /_board/evidence?path=…&file=… ------------------------
    def evidence_tab_view(self, head_only=False):
        from urllib.parse import parse_qs, urlparse
        q = parse_qs(urlparse(self.path).query)
        path_q = (q.get("path") or [""])[0]
        file_q = (q.get("file") or [""])[0]
        got = self.target({"path": path_q, "file": file_q})
        if got[0] is None:
            return self.reply(400, {"ok": False, "err": got[1]})
        body = render(got[0], path_q, file_q).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    # ---- POST /_board/evidence — the shell's write() twin, writes nothing
    def plug_evidence(self, p):
        from urllib.parse import quote
        got = self.target(p)
        if got[0] is None:
            return None, got[1]
        return {"url": "/_board/evidence?path=%s&file=%s"
                % (quote(p.get("path") or ""), quote(p.get("file") or ""))}, None
