"""The HTML pieces the paper Spaces share: tables, label/value rows, the collapsed card, Idea and hero
Evidence cards, links, and the Story row ids a cell names.
Moved from paper.py, which re-exports the names its callers import from there (`from live.paper import ...`)."""
import re

from live.paper_text import _LINK_RE, esc, outline_url
from live.paper_evidence_items import item_name
from live.paper_work_homes import _tree_url


def _table(headers, rows):
    if not rows:
        return ""
    h = "".join("<th>%s</th>" % esc(x) for x in headers)
    body = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % c for c in r) for r in rows)
    return '<table class="grid"><tr>%s</tr>%s</table>' % (h, body)


def _empty(msg):
    return '<div class="mut">%s</div>' % esc(msg)


def _link(d, rel, label, **extra):
    if not rel:
        return esc(label)
    return '<a href="%s">%s</a>' % (esc(outline_url(d["path"], rel, **extra)), esc(label))


def _kv(rows, cls=""):
    """Label/value rows as a table with cell edges. A row with no label, or
    whose value is itself a table or a tree, spans the full width instead of
    nesting a grid inside a narrow cell."""
    out = []
    for l, v in rows:
        wide = (not l) or "<table" in v or 'class="tree-' in v
        if wide:
            cap = ('<div class="kv-cap">%s</div>' % esc(l)) if l and "<table" not in v and 'class="tree-' not in v else ""
            out.append('<div class="item-row %s nolabel">%s<span>%s</span></div>' % (cls, cap, v))
        else:
            out.append('<div class="item-row %s"><b>%s</b><span>%s</span></div>' % (cls, esc(l), v))
    return '<div class="kv">%s</div>' % "".join(out) if out else ""


def _card(cid, kind, label, sub, where, status, status_cls, rows, key="", attrs="", body="", fold=False):
    """One collapsed card, the Evidence-card shape: chevron · kind pill · label
    with a muted subline · where · status; open = label/value rows. `key` is what
    opening the card selects in its Space's Runs panel."""
    # `body` leads the opened card; `fold` tucks the label/value rows under a closed Details line
    detail = body + (('<details class="row-details"><summary>Details</summary>%s</details>' % _kv(rows))
                     if fold and rows else _kv(rows))
    # say a thing once: a subline that is empty, a dash, or the same words as `where` is dropped
    plain = lambda h: re.sub(r"<[^>]+>", "", h or "").strip()
    subline = "" if plain(sub) in ("", "—") or plain(sub) == plain(where) else '<span class="item-title">%s</span>' % sub
    return ('<details class="item-card" id="%s"%s%s><summary><div class="item-summary">'
            '<span class="item-chevron">›</span><span class="item-kind">%s</span>'
            '<div class="item-main"><span class="item-label">%s</span>%s</div>'
            '<span class="item-where">%s</span><span class="item-status %s">%s</span>'
            '</div></summary><div class="item-detail">%s</div></details>'
            % (esc(cid), (' data-key="%s"' % esc(key)) if key else "", attrs, esc(kind), esc(label), subline,
               where, status_cls, esc(status), detail))


def _status_cls(text):
    t = (text or "").upper()
    if t.startswith("NOT ") or t.startswith("NO ") or "ABSENT" in t or "MISSING" in t:
        return "mut"
    if "✅" in t or "PROCEED" in t or "ESTABLISHED" in t or "ALLOCATED" in t or "READY" in t or "ACCEPTED" in t:
        return "ok"
    if "⚠" in t or "🔨" in t or "PROVISIONAL" in t or "PARTIAL" in t or "WAITING" in t:
        return "warn"
    return "mut"


def _fields(headers, cells, skip):
    return [(headers[i] if i < len(headers) else "col %d" % (i + 1), esc(cells[i]))
            for i in range(len(cells)) if i not in skip and cells[i] and cells[i] not in ("—", "-")]


def _field_html(paras):
    """A **Field** block: bullet lines become a list, other lines a paragraph."""
    items = [l for l in paras if l.lstrip().startswith("- ")]
    text = [l for l in paras if not l.lstrip().startswith("- ")]
    html_ = esc(" ".join(text))
    if items:
        html_ += '<ul class="item-bullets">%s</ul>' % "".join(
            "<li>%s</li>" % esc(l.lstrip()[2:]) for l in items)
    return html_


def _idea_card(d, i, x):
    substance = x.get("substance") or []
    def _first(*starts):
        return next((" ".join(v) for k, v in substance if k.lower().startswith(starts)), "")
    # The card leads with the question the Idea asks (JL 260922: "the ideation should be the
    # research question, which can trigger the reader to think"); the title drops to the subline.
    rq = _first("research question", "question")
    hyp = _first("hypothesis", "one-sentence")
    label, sub = (rq, esc(x["title"])) if rq else (x["title"], esc(hyp))
    if rq and " ".join(x["title"].split()).rstrip("?").lower() == " ".join(rq.split()).rstrip("?").lower():
        sub = esc(hyp)        # the table's idea cell is the question itself: say the guess, not the question twice
    verdict = x.get("verdict") or "⬜ open"
    went = x.get("went") if x.get("went") not in (None, "", "—", "-") else ""
    rows = [(k, _field_html(v)) for k, v in substance]
    if x["bullets"]:
        blist = []
        for bl in x["bullets"]:
            note = " ".join(bl["notes"])
            blist.append('<li><b>%s</b> %s%s%s</li>' % (
                esc(bl["bullet"]), esc(bl["head"]),
                ('<div class="item-note">%s</div>' % esc(note)) if note else "",
                ('<div class="item-note">Evidence: %s</div>' % esc(bl["evidence"])) if bl["evidence"] else ""))
        rows.append(("", '<details class="item-plan"><summary>Writing plan</summary><ul class="item-bullets">%s</ul></details>'
                     % "".join(blist)))
    if x["items"]:
        rows.append(("Evidence items", "".join(
            '<div><span class="idtag">%s</span> %s <span class="%s">%s</span></div>' % (
                esc(it["id"]), esc(it["desc"]), "ok" if "✅" in it["verified"] else "mut", esc(it["verified"]))
            for it in x["items"])))
    fields = [(l, esc(v)) for l, v in x.get("fields", []) if l.lower() not in ("verdict", "went to")]
    if fields:
        rows.append(("Comparison", "".join('<div><b class="item-sub">%s</b> %s</div>' % (esc(l), v) for l, v in fields)))
    if " · " in verdict:
        rows.append(("Verdict", esc(verdict)))
    if went:
        rows.append(("Went to", esc(went)))       # G0: where the admitted idea went
    short = verdict.split(" · ")[0].strip()       # the closed line keeps the title readable
    return _card("idea-" + x["id"], x["id"], label, sub, esc(went), short, _status_cls(verdict), rows,
                 key=_norm_key("i", x["id"]))


def _col(headers, needles, default):
    """Index of the first header naming one of `needles` (case-insensitive), else `default`."""
    for i, h in enumerate(headers):
        if any(n in h.lower() for n in needles):
            return i
    return default


_ROW_ID = re.compile(r"(?<![\w.])(RQ|[ETBDQHC])-?0*(\d+)(?:\s*[–-]\s*(?:\1-?)?0*(\d+))?(?![\w-]|\.\w)")


def _row_ids(text):
    """The Story row ids a cell names (`RQ2`, `E4`, `T1`, `B3`, `D5`, `Q2`, and the §3
    question blocks' `H1` hypotheses and `C1` claims); a range (`E1-E4`, `RQ1–RQ7`) names
    each one. An Evidence Item id (`E01-CITE-…`) and a Bullet address (`C1.P1.B1`) are
    not row ids."""
    out = []
    for m in _ROW_ID.finditer(text or ""):
        lo = int(m.group(2))
        hi = int(m.group(3)) if m.group(3) and int(m.group(3)) >= lo else lo
        for n in range(lo, min(hi, lo + 50) + 1):
            if "%s%d" % (m.group(1), n) not in out:
                out.append("%s%d" % (m.group(1), n))
    return out


def _row_key(cell):
    """`E2 (C1)` → `E2`, `T01` → `T1`: the id a row's first cell carries."""
    ids = _row_ids(cell)
    return ids[0] if ids else (cell or "").strip()


def _plain(text):
    """A field value → plain text: links to their label, no bold or code marks. Unlike
    clean(), a file name keeps its underscores."""
    text = _LINK_RE.sub(r"\1", text or "")
    return re.sub(r"\s+", " ", re.sub(r"\*\*|`", "", text)).strip()


def _hero_cards(d):
    cards = []
    for it in d["hero"]:
        short = it["id"].split("-")[0]
        rows = [("Need", esc(it["desc"])), ("Expected", esc(it["expected"] or "—")),
                ("Bullet", esc(it["target"]))]
        if it["supporting"]:
            rows.append(("Supporting", "<br>".join(
                "%s · <code>%s</code>" % (esc(s["owner"]), esc(s["addr"] or s["raw"])) for s in it["supporting"])))
        rows.append(("Page", _link(d, it["rel"], "Open ↗", lens="evidence", focus=it["id"])))
        cards.append(_card("hero-" + it["id"], it["type"], it["label"] or it["id"],
                           esc(item_name(it["id"]) + " · " + it["page"]), "", it["status"], _status_cls(it["status"]), rows,
                           key="%s:%s" % (it["page"], short), attrs=' data-part="%s"' % it["part"]))
    return cards


def _file_link(d, path, label):
    url = _tree_url(d, path) if path else ""
    return ('<a href="%s">%s</a>' % (esc(url), esc(label))) if url else esc(label)


def _yn(v):
    return '<span class="ok">✓</span>' if v else '<span class="warn">✗</span>'


def _norm_key(kind, value):
    """`i01` → `i1`, `E-05` → `E5`: selection keys compare by number."""
    m = re.match(r"^%s-?0*(\d+)$" % kind, (value or "").strip())
    return "%s%s" % (kind, m.group(1)) if m else (value or "").strip()
