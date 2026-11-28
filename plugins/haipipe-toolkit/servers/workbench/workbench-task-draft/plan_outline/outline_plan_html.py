"""📃 Page · the Draft table's small HTML parts: evidence chips, reader prose, Opening card, cycle strip.

Moved out of outline.py (the 600-line rule); outline re-exports every name here.
"""
import html
import re
from urllib.parse import quote

from src.item_table import wall_label
from src.evidence_labels import resolve_inline_labels
from live.outline_preview import draft_path, reader_prose, read_opening_draft


def _e(s):
    return html.escape(s)


def _scratch_run_meta(record):
    if not record:
        return ""
    run_id = str(record.get("run", "")).strip()
    status = str(record.get("status", "unknown")).strip().lower()
    if not run_id:
        return ""
    return '<span class=scratch-run-meta>· %s · %s</span>' % (_e(run_id), _e(status))


def _opening_preview_card(page_src, path_q="", file_q="", evidence_bindings=None):
    """Project an accepted Page Opening candidate into Draft Space.

    C0.P1 is page-level Opening prose rather than a C.P.B plan bullet. Keep its
    candidate in the selected Outline Markdown and render it as the first
    read-only paragraph group, using the same two-column shape as the planned
    paragraphs below; do not turn it into a synthetic Bullet or change Page
    Content.
    """
    if page_src is None:
        return ""
    path = draft_path(page_src)
    prose = read_opening_draft(page_src)
    if path is None or not prose:
        return ""
    if not prose:
        return ""

    outline_url = ("/_board/draft?path=%s&file=%s" %
                   (quote(path_q), quote(file_q))) if path_q and file_q else ""
    permalink = _e(("%s&lens=div&focus=c0-p1-opening" % outline_url)
                   if outline_url else "#c0-p1-opening")
    return (
        '<details class="paragraph-group opening-preview" id="c0-p1-opening" '
        'open data-paragraph="C0.P1">'
        '<summary class="prow"><span class=addr>C0.P1</span>'
        '<span class=mut>Opening overview</span></summary>'
        '<div class=paragraph-bullets><div class=preview-columns>'
        '<span>Bullet</span><span>Draft</span></div>'
        '<div class=point-group data-point="C0.P1">'
        '<div class=point-plan><div class=point-head>'
        '<a class=point-address href="%s" title="Open C0.P1">C0.P1</a>'
        '<span class=point-label>[Opening]</span>'
        '<span class=point-statement>Overview of the literature stream</span>'
        '</div></div>'
        '<div class=point-preview><div class=preview-copy>%s</div></div>'
        '</div></div>'
        '<div class=paragraph-reading><div class="reading-line opening-reading">'
        '<span class=reading-address>C0.P1</span><div class=reading-copy>%s</div>'
        '</div></div>'
        '</details>' %
        (permalink, _preview_reader_html(prose, {}, evidence_bindings),
         _preview_reader_html(prose, {}, evidence_bindings))
    )


def _outline_cycle_strip(cycle):
    """Render the same SHAPE → SURVEY → LAND → EMBED status used on the Page."""
    stages = ("SHAPE", "SURVEY", "LAND", "EMBED")
    current = stages.index(cycle) if cycle in stages else len(stages)
    cells = []
    for index, stage in enumerate(stages):
        cls = "done" if index < current else "current" if index == current else "future"
        aria = ' aria-current="step"' if index == current else ""
        cells.append('<span class="%s"%s><b>%d</b> %s</span>' % (
            cls, aria, index + 1, stage
        ))
    return '<div class=cyclebar aria-label="Outline evidence workflow">%s</div>' % "".join(cells)


def _typed_item_chip(item, outline_url=""):
    """One compact status tag that routes to its Evidence Space item row.

    Same law as the compact Page table: the chip is a route, not a card.  The
    item's whole Survey graph (Target, Expected, Acceptance, Supporting Runs,
    Local Input, Local Run, Result, Decide) lives once, on the Evidence
    Space row, so the Draft Space only names and colours the item and
    hands the reader to that exact card.  The native popover this replaced
    duplicated every field and trapped a phone reader behind a panel that was
    hard to close (JL 260907: the Page chip was fixed, this one still popped).
    """
    status = item["status"]
    cls = "ok" if status in {"ready", "folded", "accepted"} else (
        "mut" if status in {"deferred", "dropped"} else "warn"
    )
    # The wall identity is deliberately short but semantic: readers see the
    # item number, evidence kind, and readable preview name. The immutable id,
    # full type, and status ride on the title; everything else is on the card.
    label = wall_label(
        item["id"], item["type"], item["name"], item.get("label", "")
    )
    focus = "run-" + re.sub(r"[^A-Za-z0-9_-]", "-", item["id"])
    # One URL names the destination exactly like a Page chip does
    # (workspace + focus). Without a known Board route (a checker or test
    # rendering the card alone) the href is the bare focus; the document's
    # click delegate switches lens in place either way.
    href = ("%s&lens=evidence&focus=%s" % (outline_url, focus)
            if outline_url else "#" + focus)
    return (
        '<a class="evchip %s typed-ev" href="%s" data-outline-lens="evidence" '
        'data-outline-focus="%s" title="%s · %s · %s">%s</a>'
        % (cls, _e(href), _e(focus), _e(item["id"]), _e(item["type"]),
           _e(status), _e(label))
    )


_PREVIEW_EVIDENCE_RE = re.compile(
    r"\[(E\d+-(VALUE|CITE|DISPLAY)-[a-z0-9]+(?:-[a-z0-9]+)*)(?:(?::|\s+)[^\]]*)?\]"
)


def _resolved_evidence_html(token, binding):
    """Render a resolved Page token with its authored identity folded below it."""
    if not binding:
        return '<span class=missing-evidence-token>%s</span>' % _e(token)
    display = str(binding.get("display", "")).strip()
    status = str(binding.get("status", "resolved")).strip().lower()
    visible = display if display and status not in {"pending", "unresolved", "missing"} else token
    meta = [
        ("token", token),
        ("kind", binding.get("kind", "")),
        ("item", binding.get("item", "")),
        ("evidence run", binding.get("page_run", "") or binding.get("run", "")),
        ("owner run", binding.get("run", "")),
        ("result", binding.get("result", "")),
        ("target", binding.get("target", "")),
        ("provenance", binding.get("provenance", "")),
    ]
    detail = " ".join(
        '<span><b>%s</b> <code>%s</code></span>'
        % (_e(key), _e(str(value)))
        for key, value in meta if str(value).strip()
    )
    return (
        '<details class=resolved-evidence><summary>%s</summary>'
        '<span class=resolved-evidence-detail>%s</span></details>'
        % (_e(visible), detail)
    )


def _preview_token_html(text, bindings):
    """Render Page VALUE/DISPLAY/CITE tokens in one authored text segment."""
    return "".join(
        _resolved_evidence_html(str(span.get("token")), span.get("binding"))
        if span.get("token") else _e(str(span.get("text", "")))
        for span in resolve_inline_labels(text, bindings)
    )


def _preview_reader_html(text, item_by_id, evidence_bindings=None):
    """Render the reader projection without changing authored evidence tokens.

    Legacy bracket evidence references keep their compact wall label. New
    LaTeX-like tokens use the Result manifest binding: a resolved display is
    visible in the sentence and the original token/provenance is expandable;
    an unresolved token remains visible and is marked as missing.
    """
    prose = reader_prose(text)
    bindings = evidence_bindings or {}
    chunks, cursor = [], 0
    for match in _PREVIEW_EVIDENCE_RE.finditer(prose):
        chunks.append(_preview_token_html(prose[cursor:match.start()], bindings))
        item_id, item_type = match.group(1), match.group(2)
        item = item_by_id.get(item_id) or {
            "id": item_id,
            "type": item_type,
            "name": item_id.split("-", 2)[-1].replace("-", " "),
            "label": "",
            "status": "specified",
        }
        label = wall_label(
            item["id"], item["type"], item["name"], item.get("label", "")
        )
        chunks.append("(%s)" % _e(label))
        cursor = match.end()
    chunks.append(_preview_token_html(prose[cursor:], bindings))
    return "".join(chunks)


def _bundle_row_html(full_addr, kind, bundle):
    """One Evidence Bundle row of the plan card: the Point, its kind, what landed, its state."""
    labels = []
    if bundle["sentences"]:
        labels.append("sentence " + ", ".join(bundle["sentences"]))
    if bundle["probes"]:
        labels.append("probe " + ", ".join(bundle["probes"]))
    if bundle["citations"]:
        labels.append("cite " + ", ".join(bundle["citations"]))
    if bundle["displays"]:
        labels.append("display " + ", ".join(bundle["displays"]))
    if bundle["feedback"]:
        labels.append("feedback " + ", ".join(bundle["feedback"]))
    if not labels:
        labels.append("no landed resource")
    state_cls = "ok" if bundle["summary"] == "complete" else "warn"
    return ('<div class="bundle-row"><span class=addr>%s</span>'
            '<span class=bundle-kind>%s</span><span class=bundle-items>%s</span>'
            '<span class="bundle-state %s">%s</span></div>'
            % (full_addr, kind, _e(" · ".join(labels)), state_cls,
               _e(bundle["summary"])))
