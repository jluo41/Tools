"""The classic paper Board page's Delivery Space: the build's previews, artifacts and checks, the cover letter, the rounds,
and its Runs panel. Moved from paper_spaces.py; paper.py's `__getattr__` finds every name here, so
`from live.paper import render_delivery` keeps working."""
import json
import re
from pathlib import Path

from live.paper import (_card, _file_link, _kv, _link, _not_ready_ids, _stamp, _status_cls, _table, _tree_url, _yn,
                        esc)
from live.paper_spaces import (DELIVERY_TABS, DELIVERY_VIEWS, _bucket, _cards, _page_runs, _pane, _panel, _space,
                               _tag)


def _delivery_panel(d, kinds):
    dv, rows = d["delivery"], []
    man = dv["manifest"] or {}
    if man and dv["built"]:
        stamp = re.sub(r"\D", "", dv["built"])[2:8]
        rows.append({"run_id": "compile-" + stamp, "global_id": "compile-" + stamp, "status": "done",
                     "target": "the whole paper", "result": "delivery/build-manifest.json",
                     "result_path": dv["dir"], "goal": "%s · built %s" % (man.get("status") or "", dv["built"]),
                     "_display": "run-compile-" + stamp, "_place": "Build"})
    for r in d["rounds"]:
        fill = {"page": r["stem"], "paper": d["board"].name}
        for row in _page_runs(d, r):
            rows += [dict(x, _place="Response") for x in _tag([row], [r["stem"]], fill)]
    cover = _cover(d)
    if cover is not None:                             # the build's one fixed cover-letter run
        rows.append({"run_id": "run-delivery-coverletter", "global_id": "run-delivery-coverletter",
                     "status": "done" if cover.get("ready") else "held", "target": cover.get("round") or "the letter",
                     "result": ((cover.get("outputs") or {}).get("pdf") or ""), "result_path": dv["dir"],
                     "goal": "from " + (cover.get("from") or "?"), "_display": "run-delivery-coverletter",
                     "_place": "Cover letter", "_views": "cover"})
    rows = _tag(rows)
    fill = {"page": d["board"].name, "paper": d["board"].name}
    return _panel(d, "delivery", kinds, _bucket(kinds, rows, lambda r: r.get("_place")), fill, "the manuscript")


def _outputs(d, suffix):
    return [o for o in d["delivery"]["outputs"] if o["rel"].endswith(suffix)]


def _output_rows(d, outs):
    rows = []
    for o in outs:
        st = ("✅ built" + (" · stale" if o["stale"] else "")) if o["exists"] else "⬜ not built"
        rows.append((esc(o["what"]), _file_link(d, o["path"], o["rel"]) if o["exists"] else esc(o["rel"]),
                     '<span class="%s">%s</span>' % (_status_cls(st), esc(st)), esc(o["size"]), esc(o["stamp"])))
    return rows


def _checks_html(d):
    dv = d["delivery"]
    man = dv["manifest"] or {}
    if not man:
        return '<div class="space-empty">No build yet.</div>'
    build, sub, rd = man.get("build") or {}, man.get("submission_readiness") or {}, man.get("readiness") or {}
    facts = []
    if build:
        facts += [("main text", "%s words%s%s" % (build.get("main_text_words", "?"),
                                                  " · from %s" % build["main_text_words_from"] if build.get("main_text_words_from") else "",
                                                  (" · limit %s" % build["main_text_word_limit"])
                                                if build.get("main_text_word_limit") else "")),
                  ("citations", "%s cited · %s bib entries" % (build.get("citations", "?"), man.get("bib_entries", "?"))),
                  ("displays", "%s main table(s) · %s main figure(s)" % (build.get("main_tables", "?"), build.get("main_figures", "?"))),
                  ("pages ready", ("⬜ not ready: " + ", ".join(_not_ready_ids(rd))) if rd.get("not_ready")
                                  else "✅" if rd else ""),   # a mark and the names, never "N of M"
                  ("submission", "%s%s" % (sub.get("status", "?"), (" · " + "; ".join(sub.get("blockers") or [])) if sub.get("blockers") else ""))]
    if dv["stale"]:
        facts.append(("changed since build", ", ".join(dv["stale"])))
    g4 = next((v for g, _, v in d["gates"] if g == "G4"), "")
    if g4:
        facts.append(("G4 compile", g4))
    crs = [(esc(k.replace("_", " ")), _yn(v) if isinstance(v, bool) else '<span class="mut">%s</span>' % esc(str(v)))
           for k, v in (build.get("checks") or {}).items()]
    render = man.get("render") or {}
    if render:
        crs.append(("latexmk", _yn(render.get("latexmk_rc") == 0)))
        crs.append(("docx", _yn(render.get("docx_rc") == 0)))
    pages = []
    for i, p in enumerate(dv["pages"], 1):
        notes = list(p["reasons"]) + list(p["warnings"]) + (["changed since build"] if p["stale"] else [])
        pages.append((esc(p["id"]), _yn(p["frag"]),
                      _yn(p["ready"]) if p["ready"] is not None else '<span class="mut">—</span>', esc("; ".join(notes))))
    # engine ≥0.8 writes each unresolved \ref as {"page", "ref"}; older manifests wrote a bare string
    warns = [w if isinstance(w, str) else json.dumps(w, ensure_ascii=False) for w in (man.get("warnings") or [])] + [
        "unresolved \\ref: " + (x if isinstance(x, str) else "%s (%s)" % (x.get("ref", "?"), x.get("page", "?")))
        for x in (man.get("unresolved_refs") or [])]
    return (_kv([(k, esc(v)) for k, v in facts], "spine-row")
            + _table(["check", "result"], crs)
            + _table(["page", "fragment", "ready", "notes"], pages)
            + (('<ul class="item-bullets">%s</ul>' % "".join("<li>%s</li>" % esc(w) for w in warns)) if warns else ""))


def _preview_html(d, suffix):
    outs = [o for o in _outputs(d, suffix) if o["exists"]]
    if not outs:
        return '<div class="space-empty">Not built yet.</div>'
    main = next((o for o in outs if "main" in o["what"]), outs[0])
    if suffix == ".pdf":
        return '<iframe class="space-frame" title="%s" data-src="%s"></iframe>' % (esc(main["rel"]), esc(_tree_url(d, main["path"])))
    # JL 260929 "for the word, why we cannot preview it": the paper build draws a PDF twin of each .docx
    # beside it (<stem>.pdf, from the package itself); Preview shows it under one line naming the .docx
    twin = Path(main["path"]).with_suffix(".pdf")
    if twin.is_file():
        stale = twin.stat().st_mtime < Path(main["path"]).stat().st_mtime
        return ('<p class="mut">%s · %s · %s%s</p><iframe class="space-frame" title="%s" data-src="%s"></iframe>'
                % (_file_link(d, main["path"], main["rel"]), esc(main["size"]), esc(main["stamp"]),
                   " · the preview is older than the .docx; rebuild" if stale else "",
                   esc(main["rel"]), esc(_tree_url(d, twin))))
    return _kv([("file", _file_link(d, main["path"], main["rel"])), ("size", esc(main["size"])),
                ("written", esc(main["stamp"])),
                ("preview", '<span class="mut">none yet: the next paper build draws it</span>')], "spine-row")


def _artifacts_html(d, suffix):
    dv = d["delivery"]
    html_ = _table(["what", "file", "state", "size", "written"], _output_rows(d, _outputs(d, suffix)))
    if suffix == ".pdf":
        drs = [(esc(r[0]), esc(r[1]), '<code>%s</code>' % esc(r[2]), esc(r[3]), esc(r[4])) for r in dv["displays"]]
        html_ += _table(["printed", "declared", "label", "unit", "page"], drs)
        html_ += _table(["asset", "size"], [(_file_link(d, a["path"], a["name"]), esc(a["size"])) for a in dv["assets"]])
    else:
        html_ += _table(["returned", "size", "written"], [(_file_link(d, r["path"], r["rel"]), esc(r["size"]), esc(r["stamp"]))
                                                         for r in dv["returned"]])
    return html_ or '<div class="space-empty">Not built yet.</div>'


def _round_cards(d):
    cards = []
    for r in d["delivery"]["rounds"]:
        rows = [(k, esc(v)) for k, v in (("kind", r["kind"]), ("received", " · ".join(x for x in (r["from"], r["at"]) if x)),
                                          ("response due", r["due"]), ("base build", r["base"]),
                                          ("folders", " · ".join(r["subs"]))) if v]
        rows.append(("page", _link(d, r["rel"], "Open ↗")))
        if r["state"]:
            rows.insert(0, ("state", esc(r["state"])))
        cards.append(_card("round-" + r["stem"], r["stem"][:4], r["stem"], esc(r["kind"]), "",
                           r["state"].split("·")[0].strip(), _status_cls(r["state"]), rows, key=r["stem"]))
    venue = d["delivery"]["links"].get("venue-page", "")
    tail = _kv([("venue", _file_link(d, (d["board"] / venue).resolve(), Path(venue).stem))], "spine-row") if venue else ""
    return _cards(cards, "No round yet.") + tail


def _cover(d):
    """The cover letter as the paper build recorded it (hai-paper-assemble 0.9.0,
    run-delivery-coverletter): build-manifest.json `cover_letter`, or None."""
    man = d["delivery"]["manifest"] or {}
    return man.get("cover_letter") if isinstance(man.get("cover_letter"), dict) else None


def _cover_panes(d):
    """Cover letter tab (JL 260929: one more delivery item). The words live on the submission
    Round page's Cover letter division; the paper build writes the letter and its checks; this
    tab only reads that record."""
    cover = _cover(d)
    if cover is None:
        empty = ('<div class="space-empty">No cover letter built yet: add a <code>[coverletter]</code> '
                 'block to delivery/paper-build.toml and run the build.</div>')
        return "".join(_pane(empty, "cover", v) for v, _ in DELIVERY_VIEWS)
    base = d["delivery"]["dir"]
    outs = {k: (base / v) if v and not Path(v).is_absolute() else (Path(v) if v else None)
            for k, v in (cover.get("outputs") or {}).items()}
    src = cover.get("source") or ""
    head = '<div class="space-h">%s · %s%s</div>' % (
        esc(cover.get("round") or "letter"), "ready" if cover.get("ready") else "not ready",
        (" · " + _link(d, src.split("/draft/")[0] + "/" + Path(src.split("/draft/")[0]).name + ".md", "Open ↗",
                       lens="div")) if src else "")
    pdf = outs.get("pdf")
    preview = head + (('<iframe class="space-frame" title="cover letter" data-src="%s"></iframe>'
                       % esc(_tree_url(d, pdf))) if pdf and pdf.is_file() else '<div class="space-empty">Not built yet.</div>')
    files = [(_file_link(d, f, f.name), esc(_stamp(f))) for f in outs.values() if f and f.is_file()]
    artifacts = head + (_table(["file", "written"], files) if files else '<div class="space-empty">Not built yet.</div>')
    rows = [(esc(c.get("check", "")), '<span class="%s">%s</span>' % ("ok" if c.get("ok") else "warn", "✅" if c.get("ok") else "⚠️"),
             esc(c.get("detail", ""))) for c in cover.get("checks") or []]
    checks = head + (_table(["check", "", "detail"], rows) or '<div class="space-empty">No checks recorded.</div>')
    return (_pane(preview, "cover", "preview") + _pane(artifacts, "cover", "artifacts")
            + _pane(checks, "cover", "checks"))


def render_delivery(d, kinds):
    main = ""
    for tab, suffix in (("latex", ".pdf"), ("word", ".docx")):
        if d["delivery"]["dir"] is None:
            empty = '<div class="space-empty">No delivery/ yet.</div>'
            main += "".join(_pane(empty, tab, v) for v, _ in DELIVERY_VIEWS)
            continue
        main += (_pane(_preview_html(d, suffix), tab, "preview") + _pane(_artifacts_html(d, suffix), tab, "artifacts")
                 + _pane(_checks_html(d), tab, "checks"))
    main += _cover_panes(d)
    main += _pane(_round_cards(d), "rounds")
    return _space("delivery", main, _delivery_panel(d, kinds), DELIVERY_TABS, DELIVERY_VIEWS, noviews=("rounds",))
