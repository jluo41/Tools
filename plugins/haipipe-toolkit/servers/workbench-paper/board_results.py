"""A paper Board's RESULTS band: the eight views A Idea to H Writing in the shape settled in b16 s32 (numbered bars,
the main point large, card tabs, side tabs, the flow map, folder trees), the same on Report and Work."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

from live import draft_steps as ds
from live.frame import esc
from live.ui_parts import _bar, _cap, _card_tabs, _clean, _kv, _open_btn, _plain, _section, _side_tabs, _when
from live.focus_draft import paragraphs
from live.board_read import display_plan, _after_table, _face, _field, _first_para, _folder_line, _label_rows, _lead_sentence, _mark, _num, _open_link, _page_url, _rq_lists, _section_state, _state_words, _table, _task_url, _undated, _version_url, explore_tree, face_sections, is_version
from live.board_interactions import ix_answered, ix_item
from live.board_evidence import EVIDENCE_KINDS, evidence_body


def _topic_view(topic: Path, root: Path, md, items=(), answer_first: bool = False) -> str:
    """A topic as a view. `answer_first` (b16 s32-D10, view A · Idea, JL 261031: "do you think we should put the
    Direction to the top?"): the face's first section, then 🙋 what waits on you, then the drawing and the mind
    map, then the rest of the face, then the answered forms; else the pictures first."""
    from live import frame
    face_md = frame._notes(topic)
    text = face_md.read_text(encoding="utf-8", errors="ignore") if face_md else ""
    line = _field(text, "Topic")
    line = (re.match(r"(.+?[.;])(?:\s|$)", line) or [None, line])[1] if line else ""
    rel = lambda p: "/" + quote(ds._rel(p, root))
    verbs = [f'<a class=fd-btn data-pop="{esc(topic.name)}" href="/_board/page?path={rel(face_md)}">Open the topic ↗</a>'] if face_md else []
    deck = topic / f"{topic.name}.slides.html"
    if deck.is_file():
        verbs.append(f'<a class=fd-btn data-pop="{esc(topic.name)} · slide" href="{esc(rel(deck))}">Slide</a>')
    mind = topic / f"{topic.name}.mindmap.md"
    drawing, png = topic / f"{topic.name}.excalidraw", topic / f"{topic.name}.png"
    pic = ""
    if png.is_file():
        href = frame._draw_url(drawing, root) if drawing.is_file() else rel(png)
        pic = _section("The drawing", f'<a class=pb-draw data-pop="{esc(topic.name)}" href="{esc(href)}">'
                                      f'<img src="{esc(rel(png))}" alt="{esc(topic.name)}" loading=lazy></a>')
    if mind.is_file():                          # the mind map is a section too, in place (JL 261031: "the mind map
        try:                                    # here should be a section as well")
            tree = frame.mindmap_module().fragment(mind, ds._rel(mind, root), editable=False,
                                                   url_of=lambda q: "/" + quote(ds._rel(q, root)))
            pic += _section("The mind map", f'<div class=pb-map>{tree}</div>')
        except Exception:
            pass
    answered = ix_answered([r for r in items if r.get("topic") == topic], root)   # what was decided here, by form (JL 261031)
    parts = [f'<section class=fd-sec><h3 class=fd-h>{esc(n)}</h3>{md(b, topic)}</section>' for n, b in face_sections(text)]
    head = (f'<p class=pb-topic><b>{esc(topic.name)}</b>' + (f' · {esc(line)}' if line else '') + '</p>'
            + f'<div class=pb-verbs>{"".join(verbs)}</div>')
    if not answer_first:
        return head + pic + answered + "".join(parts)
    waiting = "".join(ix_item(r, root) for r in items if r.get("topic") == topic and r.get("state") == "waiting")
    return (head + "".join(parts[:1]) + (_section("🙋 Interactions", waiting) if waiting else "")
            + pic + "".join(parts[1:]) + answered)


# the Board Report's views settled one by one, A to H (b16 s32-D09, JL 261031: "we might want to update them one by one");
# a view here opens answer first (s32-D10)
ANSWER_FIRST = {"idea"}


def _helpers(topic: Path, root: Path, items, mind: bool = True, drawing: bool = True) -> str:
    """The helpers at the bottom: what waits on you, the drawing (Slides · Draw), the mind map (A only)."""
    from live import frame
    rel = lambda p: "/" + quote(ds._rel(p, root))
    out = '<hr class=pb-rule>'                          # Interactions moved into the Process band (JL 261101)
    show, (drawing, png, deck) = drawing, (topic / f"{topic.name}.excalidraw", topic / f"{topic.name}.png", topic / f"{topic.name}.slides.html")
    if show and png.is_file():
        href = frame._draw_url(drawing, root) if drawing.is_file() else rel(png)
        verbs = ([f'<a class=fd-btn data-pop="{esc(topic.name)} · slide" href="{esc(rel(deck))}">Slides</a>'] if deck.is_file() else []) + \
            [f'<a class=fd-btn data-pop="{esc(topic.name)}" href="{esc(href)}">Draw</a>']
        out += _bar(None, "The drawing", f'<div class=pb-pic><a data-pop="{esc(topic.name)}" href="{esc(href)}"><img src="{esc(rel(png))}" '
                                         f'alt="{esc(topic.name)}"></a><div class=pb-verbs>{"".join(verbs)}</div></div>')
    page = topic / f"{topic.name}.mindmap.html"
    if mind and page.is_file():
        out += _bar(None, "The mind map", f'<div class=pb-verbs><a class=fd-btn data-pop="{esc(topic.name)} · mind map" '
                                          f'href="{esc(rel(page))}">Open the mind map</a></div>')
    return out


def _narrative(topic: Path, root: Path, body: str) -> str:
    """The Section narrative drawn as a small map: the paper, then each Section in reader order, then the claims that
    land in it (the face's claims table, `lands in`); the full mind map opens by its button (b16 s32 B r02)."""
    rows = [r for r in _table(body) if r.get("lands in") and r.get("proposition")]
    if not rows:
        return ""
    order = ("abstract", "introduction", "data", "methods", "results", "robustness", "discussion", "cover letter")
    where = {}
    for r in rows:
        for sec in (x.strip() for x in r["lands in"].split(",")):
            where.setdefault(sec, []).append(r)
    secs = sorted(where, key=lambda x: next((i for i, o in enumerate(order) if x.lower().startswith(o)), 99))
    tree = "".join(f'<div class=pb-nrow><span class=pb-sbox>{esc(_cap(sec))}</span><div class=pb-chips>' + "".join(
        f'<span class=pb-chip><b>{esc(r.get("claim", ""))}</b> {esc(_plain(r["proposition"]))}</span>' for r in where[sec])
        + '</div></div>' for sec in secs)
    page = topic / f"{topic.name}.mindmap.html"
    btn = (f'<a class=fd-btn data-pop="{esc(topic.name)} · mind map" href="/{quote(ds._rel(page, root))}">Mind map</a>'
           if page.is_file() else "")
    return f'<div class=pb-tree><span class=pb-root>{esc(topic.name.split("-", 2)[-1].replace("-", " "))}</span><div class=pb-nar>{tree}</div></div>' + \
        (f'<div class=pb-verbs>{btn}</div>' if btn else "")


def idea_view(topic: Path, root: Path, md, items=()) -> str:
    """A · Idea (b16 s32 A): 1 · 🧭 Direction large, 2 · 🔀 Directions considered as tiles, 3 · 🤝 Hand-off as a chain."""
    text, parts = _face(topic)
    out, n = "", 0
    if "direction" in parts:
        lead, rest = _lead_sentence(parts["direction"])
        rows, rest = _label_rows(re.sub(r"(?m)^\*\*Direction\*\*:.*\n?", "", rest))
        n += 1
        out += _bar(n, "Direction", f'<p class=pb-big>{esc(_cap(lead))}</p><p class=pb-state>{esc(_field(text, "Stage"))}</p>'
                    + rows + md(rest, topic))
    rows = _table(parts.get("directions considered", ""))
    if rows:
        rank = lambda r: next((i for i, w in enumerate(("✅", "fallback", "second", "considered", "lost", "replaced"))
                               if w in r.get("verdict", "")), 9)
        tiles = sorted(rows, key=rank)
        kind = lambda r: " pb-chosen" if rank(r) == 0 else (" pb-gone" if rank(r) >= 4 else "")
        short = lambda t: t if len(t) <= 90 else t[:88].rsplit(" ", 1)[0] + " …"
        when = lambda r: (re.search(r"\b(\d{6})\b", r.get("verdict", "")) or [None, ""])[1]
        n += 1
        out += _bar(n, "Directions considered", _card_tabs("dc", [
            (_undated(r.get("verdict", "")), short(_plain(r.get("direction", ""))), "", kind(r).replace(" pb-chosen", " pb-chosen1"))
            for r in tiles], [_kv((("Direction", esc(_plain(r.get("direction", "")))), ("Verdict", esc(_undated(r.get("verdict", "")))),
                                   ("Reason", esc(_plain(r.get("reason", "")))), ("Decided", esc(when(r)))))
                              for r in tiles]))
    if "hand-off" in parts:
        body = parts["hand-off"]
        to = (re.search(r"\bs\d+-[a-z0-9-]+", body) or [""])[0]
        first, _, rest = body.strip().partition("\n")
        chain = ('<div class=pb-chain>' + "".join(
            f'<div class=pb-hop>{"<span class=pb-arrow>→</span>" if k else ""}<div class=pb-step><span class=pb-role>{r}</span>'
            f'<div class=pb-tile><span>{esc(v)}</span></div></div></div>'
            for k, (r, v) in enumerate((("from", topic.name), ("hands", "the selected idea"), ("to", to or "the Story")))) + '</div>')
        n += 1
        out += _bar(n, "Hand-off", chain + md(rest, topic))
    return out + _helpers(topic, root, items, mind=True)


def story_view(board: Path, topic: Path, root: Path, md, items=()) -> str:
    """B · Story (b16 s32 B): Pitch large; the RQs and the journals as tabs; the narrative as its mind map."""
    text, parts = _face(topic)
    rel = lambda p: "/" + quote(ds._rel(p, root))
    out, n = "", 0
    if "pitch" in parts:
        one = _field(parts.get("identity", ""), "One-sentence identity")
        pitch = _plain(parts["pitch"])
        lead = _clean(one) or _clean(re.split(r"(?<=[.;])\s", pitch, 1)[0])
        rest = pitch if one else (re.split(r"(?<=[.;])\s", pitch, 1) + [""])[1]
        n += 1
        out += _bar(n, "Pitch", f'<p class=pb-big>{esc(_cap(lead))}</p><p class=pb-state>{esc(_field(text, "Stage"))}</p>'
                    + (f'<p>{esc(rest)}</p>' if rest else ""))
    rq = parts.get("research questions", "")
    qs, said = _rq_lists(rq)
    if qs:
        reports = dict(re.findall(r"Q0*(\d+)\s*(\[[^\]]+\]\([^)]+\))", rq))
        tiles, panels = [], []
        for k, q in qs:                              # k: the item's own number (a story may start at RQ0)
            m = re.match(r"(.+?\?)\s*(.*)$", q)
            ask, state = (m.group(1), m.group(2)) if m else (q, "")
            tiles.append((f"RQ{k}", _plain(ask), ""))
            panels.append(_kv((("Question", esc(_plain(ask))), ("Answer so far", esc(_plain(state))),
                               ("Claim if answered", esc(_plain(said.get(k, "")))),
                               ("Report", _open_link(reports.get(str(k), ""), topic, root)))))
        n += 1
        out += _bar(n, "Questions", _card_tabs("rq", tiles, panels))
    duo = [(k, parts[k]) for k in ("stakes", "evidence basis and boundaries") if k in parts]
    if duo:
        n += 1
        out += _bar(n, "Stakes and evidence basis", _card_tabs("se", [(("Stakes" if k == "stakes" else "Evidence basis"),
                                                                 ("why it matters, and to whom" if k == "stakes" else "what it can claim, and what it cannot"), "")
                                                                for k, _ in duo], [md(b, topic) for _, b in duo]))
    venues = _table(parts.get("venues", ""))
    if venues:
        tiles, panels = [], []
        for k, v in enumerate(venues):
            name = _plain(v.get("venue", ""))
            slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
            call = board / "venues" / slug / "call.md"
            related = next(iter(sorted(board.glob(f"s[0-9]*-related-work-{slug}"))), None)
            rp = ""
            if related is not None and (related / f"{related.name}.png").is_file():
                rp = (f'<a data-pop="{esc(related.name)}" href="{esc(rel(related / (related.name + ".png")))}"><img src="{esc(rel(related / (related.name + ".png")))}" '
                      f'alt="{esc(related.name)}" style="max-width:min(320px,100%);border:1px solid var(--line);border-radius:6px"></a>'
                      f'<br><a class=fd-btn data-pop="{esc(related.name)}" href="{esc(rel(related / (related.name + ".png")))}">Open the related-work map</a>')
            tiles.append((name, _plain(v.get("kind", "")), "target" if k == 0 else f"fallback {k}"))
            panels.append(_kv((("Why it fits", esc(_plain(v.get("why it fits", "")))), ("Leads with", esc(_plain(v.get("leads with", "")))),
                               ("Still needs", esc(_plain(v.get("still needs", "")))),
                               ("Desk rules", f'<a class=fd-btn data-pop="{esc(slug)}" href="/_board/page?path={rel(call)}">Open call.md</a>'
                                if call.is_file() else esc(_plain(v.get("desk record", ""))) or "none yet"),
                               ("Related papers", rp),
                               ("All journals", _open_btn("Compare all journals", _page_url(topic / "delivery" / "venue-comparison.md", root), "venue comparison")
                                if (topic / "delivery" / "venue-comparison.md").is_file() else ""))))
        n += 1
        full = topic / "delivery" / "venue-comparison.md"
        out += _bar(n, "Venues", _card_tabs("ve", tiles, panels, chain=True) + ("" if full.is_file() else md(_after_table(parts["venues"]), topic)))
    road = [(k, parts[k]) for k in ("discovery roadmap", "task roadmap") if k in parts]
    if road:
        n += 1
        out += _bar(n, "Roadmaps", _card_tabs("rm", [(k.capitalize(), "the literature still to read" if k.startswith("discovery")
                                                 else "the Runs still to make", "") for k, _ in road], [md(b, topic) for _, b in road]))
    if "section narrative" in parts:                 # the narrative IS the mind map (JL 261031)
        n += 1
        out += _bar(n, "Section narrative", _narrative(topic, root, parts["section narrative"]) or md(parts["section narrative"], topic))
    return out + _helpers(topic, root, items, mind=False)


def dataflow_map(board: Path, topic: Path) -> str:
    """How the data come together, as a map (JL 261101: "for the data flow, we should focus on the mindmap, show the
    mind map of how these data are collected together"): four columns joined by lines, the data, the linking, the
    tables, then the questions each table feeds; read from the topic's `<topic>-drawing.yaml` (excalidraw-workflow's
    words), the Board Questions from reports/."""
    import json
    import yaml
    f = topic / f"{topic.name}-drawing.yaml"
    if not f.is_file():
        return ""
    try:
        spec = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
    except Exception:
        return ""
    found, cols = spec.get("foundation") or {}, spec.get("columns") or {}
    qs = [d for d in sorted((board / "reports").glob("q[0-9]*_*")) if d.is_dir()]
    title = lambda q: next((ln[2:].strip() for ln in (q / f"{q.name}.md").read_text(encoding="utf-8", errors="ignore").splitlines()
                            if ln.startswith("# ")), q.name) if (q / f"{q.name}.md").is_file() else q.name
    links = [(x["from"], x["to"]) for x in spec.get("links") or [] if isinstance(x, dict)]
    links += [(str(t), f"q{int(k):02d}") for k, t in (spec.get("feeds") or {}).items()]      # a table feeds a question

    def box(key, head, line="", gray=""):
        return (f'<div class=pb-node data-key="{esc(key)}"><b>{esc(head)}</b>' + (f'<span>{esc(line)}</span>' if line else "")
                + (f'<small>{esc(gray)}</small>' if gray else "") + '</div>')
    out = ""
    for c in ("D", "S", "T"):
        head = (cols.get(c) or [c, ""])
        out += (f'<div class=pb-col><p class=pb-colh>{esc(head[0].capitalize())}<small>{esc(head[1] if len(head) > 1 else "")}</small></p>'
                + "".join(box(n.get("key", ""), n.get("map") or n.get("title", ""), (n.get("lines") or [""])[0], n.get("gray", ""))
                          for n in found.get(c) or []) + '</div>')
    out += ('<div class=pb-col><p class=pb-colh>The questions<small>what each table answers</small></p>'
            + "".join(box(q.name.split("_", 1)[0], q.name.split("_", 1)[0].upper() + " · " + title(q)) for q in qs) + '</div>')
    return f'<div class=pb-flow data-links="{esc(json.dumps(links))}">{out}<svg class=pb-wires aria-hidden=true></svg></div>'


def dataflow_view(board: Path, topic: Path, root: Path, md, items=()) -> str:
    """C · Data flow: 1 the flow in one sentence, then its map (dataflow_map), which is the view's mind map, so no
    mind-map helper; 2 each Board Question as a card tab, its
    answer and the work it waits on; 3 what it waits on."""
    text, parts = _face(topic)
    out, n = "", 0
    n += 1
    out += _bar(n, "Flow", f'<p class=pb-big>{esc(_field(text, "Topic"))}</p>'      # the topic's stage word said nothing (D r02)
                + dataflow_map(board, topic))
    qs = sorted(d for d in (board / "reports").glob("q[0-9]*_*") if d.is_dir())
    tiles, panels = [], []
    for q in qs:
        f = q / f"{q.name}.md"
        if not f.is_file():
            continue
        qt = f.read_text(encoding="utf-8", errors="ignore")
        title = next((ln[2:].strip() for ln in qt.splitlines() if ln.startswith("# ")), q.name)
        qp = {re.sub(r"^\d+\s*·\s*", "", a).strip().lower(): b for a, b in face_sections(qt)}
        body = qp.get("the question", "")
        bullet = lambda name: _plain((re.search(rf"(?m)^\s*-\s*\*\*{name}\*\*:?\s*(.+)$", body) or [None, ""])[1])
        first_under = lambda head: _plain(re.sub(r"^\*\*[^*]+\*\*\s*·\s*", "", (re.search(
            rf"\*\*{head}\*\*\s*\n\s*-\s*(.+)", body) or [None, ""])[1]))
        state = bullet("Answer state")
        tiles.append((q.name.split("_", 1)[0].upper(), f"{title} · {state}" if state else title, ""))
        panels.append(_kv((("Question", esc(bullet("Question"))), ("Hypothesis", esc(first_under("Hypotheses"))),
                           ("Claim if it holds", esc(first_under("Potential claims"))), ("Now", esc(re.split(r"(?<=[.;])\s", bullet("Now"), 1)[0])),
                           ("Answer so far", esc(_first_para(qp.get("answer", ""))) or "not answered yet"),
                           ("Report", _open_btn(f"Open: {title}", _page_url(f, root), title)))))
    if tiles:
        n += 1
        out += _bar(n, "Questions to Runs", _card_tabs("qr", tiles, panels))
    return out + _helpers(topic, root, items, mind=False)       # the Flow IS the mind map (JL 261101); its open points: Process


def paperflow_view(board: Path, topic: Path, root: Path, md, items=()) -> str:
    """D · Paper flow: 1 the send in one sentence; 2 the Sections and 3 the displays as card tabs; 4 the timeline as
    dated steps, each with its state."""
    text, parts = _face(topic)
    out, n = "", 0
    send = re.sub(r"\s*\(.*?\)\.?$", "", _field(text, "Send"))
    venue = _field((board / "board.md").read_text(encoding="utf-8", errors="ignore"), "venue") if (board / "board.md").is_file() else ""
    lead = f"Send {send}" + (f" to {venue}" if venue else "") if send else _field(text, "Topic")
    shows = _table(parts.get("displays", ""))
    done = sum(1 for r in shows if _mark(r.get("state", "")) == "✅")
    n += 1
    out += _bar(n, "Send", f'<p class=pb-big>{esc(lead)}</p>'
                + (f'<p class=pb-state>{done} of {len(shows)} displays done</p>' if shows else ''))
    secs = _table(parts.get("sections", ""))
    if secs:
        n += 1
        out += _bar(n, "Sections", _card_tabs("ps", [(_plain(r.get("section", "")), "answers " + _plain(r.get("answers", "")), "")
                                                 for r in secs],
                                         [_kv((("Its job", esc(_plain(r.get("job", "")))), ("Displays", esc(_plain(r.get("displays", "")).strip("—–- ") or "none")),
                                               ("Evidence", esc(_plain(r.get("evidence", "")))), ("Words", esc(_plain(r.get("words", ""))))))
                                          for r in secs]))
    dp = display_plan()
    plan = dp.rows(board) if dp else []
    if plan:                                     # the display plan lives in G · Displays (JL 261101); here one line
        n += 1
        out += _bar(n, "Displays", f'<p class=pb-state>{len(plan)} displays planned, '
                    f'{sum(1 for r in plan if r["where"] == "main")} in the paper: see the Displays view.</p>')
    elif shows:
        n += 1
        out += _bar(n, "Displays", _card_tabs("pd", [(_plain(r.get("display", "")), _mark(r.get("state", "")) + " " + _plain(r.get("state", "")), "")
                                                 for r in shows],
                                         [_kv((("Title", esc(_plain(r.get("title", "")))), ("Kind", esc(_plain(r.get("kind", "")))),
                                               ("Answers", esc(_plain(r.get("answers", "")))), ("Made by", esc(_plain(r.get("made by", ""))))))
                                          for r in shows]))
    steps = sorted(_table(parts.get("timeline", "")), key=lambda r: _plain(r.get("when", "")))
    if steps:
        n += 1
        out += _bar(n, "Timeline", '<div class=pb-steps>' + "".join(
            f'<div class=pb-srow><span class=pb-when>{esc(_plain(r.get("when", "")))}</span><span class=pb-what>{esc(_plain(r.get("step", "")))}'
            f'<small>{esc(_plain(r.get("who", "")))}</small></span><span class=pb-st>{_mark(r.get("state", ""))} {esc(_plain(r.get("state", "")))}</span></div>'
            for r in steps) + '</div>')
    return out + _helpers(topic, root, items, mind=True)


def explore_view(board: Path, root: Path, md, items=()) -> str:
    """E · Support blocks as folder trees (JL 261101: "more like the folder tree, only show the related folder tree";
    "we will have both the work and discovery, as two sections"; "the works from multiple projects"): 1 · Work and
    2 · Discovery, each one tree per Project, its Blocks, Jobs and Tasks this paper names, one line each, each a link."""
    tree = explore_tree(board)
    named = tree.get("named", {})
    main = max(named, key=named.get) if named else None       # the Job the pages name most: the paper's main analysis
    url = lambda d: "/_board/workbench?" + "&".join(f"{a}={quote(b)}" for a, b in (("path", ds._rel(d, root)), ("layout", "focus")))

    def apart(lines: list) -> list:
        """Sibling Tasks' lines without the words they all share (E r03: five lines read "Tables of whether…")."""
        if len(lines) < 2 or not all(lines):
            return lines
        ws = [ln.split() for ln in lines]
        a = next((i for i in range(min(map(len, ws))) if len({w[i] for w in ws}) > 1), 0)
        z = next((i for i in range(1, min(map(len, ws)) - a) if len({w[-i] for w in ws}) > 1), 1) - 1
        return [_cap(" ".join(w[a:len(w) - z]).strip(" ,.;*`()")) for w in ws]

    def node(d: Path, kids: str = "", line: str = None) -> str:
        line = _folder_line(d) if line is None else line
        if re.match(r"t\d", d.name) and line and line == _folder_line(d.parent):
            line = ""
        name = esc(d.name).replace("_", "_<wbr>")                # a phone breaks a long name only after "_"
        big = d == main
        return (f'<li><div class=pb-frow><a href="{esc(url(d))}" title="{esc(line)}"{" class=pb-main" if big else ""}>{name}/</a>'
                + ('<em class=pb-mainw>main analysis</em>' if big else "")
                + (f'<small>{esc(line)}</small>' if line else "") + '</div>' + (f'<ul>{kids}</ul>' if kids else "") + '</li>')

    def tasks(ts) -> str:
        ts = sorted(ts)
        return "".join(node(t, line=ln) for t, ln in zip(ts, apart([_folder_line(t) for t in ts])))
    out = ""
    for n, (kind, name, none) in enumerate((("work", "Work", "No work folder named yet."),
                                            ("discovery", "Discovery", "No discovery folder named yet: the venue's papers sit in the related-work map.")), 1):
        trees = ""
        for proj, blocks in sorted(tree.get(kind, {}).items(), key=lambda x: (x[0] != board.parents[1], x[0].name)):
            inner = "".join(node(b, "".join(node(j, tasks(ts)) for j, ts in sorted(jobs.items())))
                            for b, jobs in sorted(blocks.items()))
            trees += (f'<ul class=pb-ftree><li><div class=pb-frow><a href="{esc(url(proj))}">{esc(proj.name)}/</a></div>'
                      f'<ul><li><span>{kind}/</span><ul>{inner}</ul></li></ul></li></ul>')
        venues = "/_board/workbench?" + "&".join(f"{a}={quote(b)}" for a, b in (("path", ds._rel(board, root)), ("layout", "focus"),
                                                                                 ("section", "report"), ("group", "story")))
        empty = f'<p class=mut>{esc(none)}</p>' if kind == "work" else (     # E r04 fix 2: the venue's papers, one click away
            f'<p class=mut>No discovery folder named yet: the venue\'s papers sit in '
            f'<a href="{esc(venues)}">Story › 4 · Venues</a>, the related-work map.</p>')
        out += _bar(n, name, trees or empty)
    return out


def evidence_view(board: Path, root: Path, md, items=()) -> str:
    """F · Evidence: 1 values, 2 citations, each a side tab per Task whose panel shows the thing itself. The displays
    are a view of their own, G · Displays, after this one (JL 261101: "put the display outside of the Evidence, and put
    it after the Evidence and before the Writing, to highlight it")."""
    return _evidence_kinds(board, root, ("Values", "Citations"))[0] or '<p class=mut>No values or citations Job yet.</p>'


def displays_view(board: Path, root: Path, md, items=()) -> str:
    """G · Displays (JL 261101, its own view between Evidence and Writing): 1 · the plan, each display against the
    venue's display rules (haipipe-paper-plan's display plan, when the Board has one); 2 · the displays, one side tab
    per pool Task (Display A → Figure 1, its type and name), its panel the newest preview.pdf, the display as the paper
    prints it, then how it was made; and all of them as one PDF (build_displays_pdf.py)."""
    out, n = "", 0
    dp = display_plan()
    plan = dp.rows(board) if dp else []
    if plan:
        n += 1
        out += _bar(n, "Plan", _display_plan(board, root, dp, plan))
    body, _ = _evidence_kinds(board, root, ("Displays",), n)
    return (out + body) or '<p class=mut>No display Job or display plan yet.</p>'


def _evidence_kinds(board: Path, root: Path, kinds: tuple, n: int = 0) -> tuple[str, int]:
    """The numbered sections of these evidence kinds (Values, Citations, Displays), in that order, each a side tab per
    Task; the displays also as one PDF (`delivery/<job>/<job>-all-displays.pdf`)."""
    jobs = [d for d in sorted(board.glob("j[0-9]*_*")) if d.is_dir() and not is_version(d)]
    out = ""
    for kind, pat in sorted((k for k in EVIDENCE_KINDS if k[0] in kinds), key=lambda k: ("Values", "Citations", "Displays").index(k[0])):
        job = next((j for j in jobs if re.search(pat, j.name, re.I)), None)
        if job is None:
            continue
        tasks = sorted((x for x in job.glob("t[0-9]*_*") if x.is_dir()), key=_num)
        tiles, panels = [], []
        dp = display_plan() if kind == "Displays" else None
        paper_as = {r.get("display", ""): (r["as"] if r["as"] == r.get("display") else f"{r.get('display', '')} → {r['as']}")
                    for r in (dp.rows(board) if dp else [])}
        plan_of = {r.get("display", ""): r for r in (dp.rows(board) if dp else [])}
        groups = []                              # (group, plan order) per tile, for the Displays' Main / Appendix lists
        for t in tasks:                          # each item to read: its list on the left, the thing itself on the right
            label, status, body = evidence_body(t, root)
            words = re.sub(r"^t\d+_", "", t.name).replace("-", " ")
            words = re.sub(r"^(?:e?figure|e?table|values|cite)\d*\s*", "", words, flags=re.I)
            head = label if label and label.lower() not in ("values", "citations") else _cap(words)
            line = words if head == label else re.sub(r"^\d+\s+", "", status or "")
            line = "waiting" if line.startswith("waits") else line
            if kind == "Displays":               # JL 261101: "for each display, we might also want to have the name and type"
                line = _display_line(t, words)
                face = t / f"{t.name}.md"         # Display A → Figure 1, from the display plan, by any key the face answers to
                ks = dp.keys(face.read_text(encoding="utf-8", errors="ignore")) if dp and face.is_file() else []
                head = next((paper_as[k] for k in ks if k in paper_as), head)
                r = next((plan_of[k] for k in ks if k in plan_of), None)
                order = list(plan_of).index(r.get("display", "")) if r is not None else 999
                if r is not None:                # the plan says where it goes
                    group = r["where"]
                elif plan_of:                    # a plan that does not name it
                    group = "unplanned"
                else:                            # no plan: t51 and on, or an eTable / Appendix label, is outside the main text
                    group = "supplement" if _num(t) >= 50 or re.match(r"(?i)(e(?=fig|tab)|appendix|supp)", label or "") else "main"
                groups.append((group, order))
            tiles.append((head, line or status, ""))
            panels.append(body)
        book = board / "delivery" / job.name / f"{job.name}-all-displays.pdf"   # build_displays_pdf.py writes it
        whole = (_open_btn("Open all displays as one PDF", "/" + quote(ds._rel(book, root)), book.name)
                 + f'<span class=pb-state>built {_when(book)}</span>') if kind == "Displays" and book.is_file() else ""
        n += 1
        if kind == "Displays" and tiles:         # grouped, Main then Appendix (JL 261101: "groups them in different groups,
            sup = _supplement_word(list(paper_as.values()))   # like the main"), each card thinner
            name = {"main": "Main", "supplement": sup, "unplanned": "Not in the plan"}
            keyed = sorted(zip(groups, tiles, panels), key=lambda x: (("main", "supplement", "unplanned").index(x[0][0]), x[0][1]))
            tabs = _grouped_tabs("evD", [(name[g], (h, w), b) for (g, _), (h, w, _), b in keyed])
        else:
            tabs = _side_tabs("ev" + kind[0], [(h, w) for h, w, _ in tiles], panels) if tiles else '<p class=mut>No Tasks yet.</p>'
        out += _bar(n, kind, f'<div class=pb-verbs>{whole}{_open_btn(f"Open {job.name}", _task_url(job, root))}</div>' + tabs)
    return out, n


def _supplement_word(labels: list) -> str:
    """What the venue calls the displays outside the main text: Supplement (eFigure, Supplementary Table), else Appendix."""
    return "Supplement" if any(re.search(r"→ (?:e(?:Figure|Table)|Supplementary)", x) for x in labels) else "Appendix"


def _grouped_tabs(eid: str, items: list) -> str:
    """Side tabs in groups (Main, Appendix): the shared side-tab markup (ui_parts._side_tabs, so its clicks work), a
    small group name above each group's cards, each card thinner (this theme's own style, DISPLAY_CSS)."""
    rows, panels, last = "", "", None
    for k, (group, (h, w), body) in enumerate(items):
        if group != last:
            rows += f'<div class=pb-lgroup>{esc(group)}</div>'
            last = group
        rows += (f'<button type=button class="pb-item{" on" if k == 0 else ""}" data-pbtab="{eid}{k}"><b>{esc(h)}</b>'
                 f'<span title="{esc(w)}">{esc(w)}</span></button>')
        panels += f'<div class=pb-panel data-pbpanel="{eid}{k}"{"" if k == 0 else " hidden"}>{body}</div>'
    return (DISPLAY_CSS + f'<div class="pb-tabset pb-side pb-thin"><div class=pb-list>{rows}</div>'
            f'<div class=pb-read>{panels}</div></div>')


# the Displays' side lists: thinner cards, a group name above each group (this theme's own look; ui_parts stays shared)
DISPLAY_CSS = ("<style>.pb-thin .pb-item{padding:3px 9px;margin:0 0 1px}.pb-thin .pb-item b{font-size:13px;line-height:1.3}"
               ".pb-thin .pb-item span{font-size:11.5px;line-height:1.3}"
               ".pb-lgroup{font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);"
               "margin:10px 0 3px 2px}.pb-lgroup:first-child{margin-top:0}"
               "@media(max-width:600px){.pb-lgroup{flex-basis:100%;margin:6px 0 2px}}</style>")


DISPLAY_TYPES = (("figure", "📈 Figure"), ("table", "📊 Table"))


def _display_plan(board: Path, root: Path, dp, plan: list) -> str:
    """G · Displays' plan, from the display plan (haipipe-paper-plan; JL 261101: "we should also have the plan for the
    displays"; "the display ... should also follow the venue"): the venue check first, then each display as a side tab
    (Display A → Figure 1, its type and name), its panel what it shows, where it goes, its Run and its sketch."""
    face = dp.plan_face(board)
    text = face.read_text(encoding="utf-8", errors="ignore")
    checks = dp.check(board)
    call = dp.venue_call(board)
    bad = [t for m, t in checks if m == "❗"]
    head = (f'<p class=pb-state>{"❗ " + str(len(bad)) + " against the venue" if bad else "✅ within the venue" + chr(39) + "s rules"}'
            + (f' · {esc(call.parent.name)}' if call else '') + '</p>'
            + '<ul class=pb-checks>' + "".join(f'<li>{esc(m)} {esc(t)}</li>' for m, t in checks) + '</ul>'
            + f'<div class=pb-verbs>{_open_btn("Open the display plan", _page_url(face, root), face.name)}'
            + (_open_btn("Open the venue rules", _page_url(call, root), "call.md") if call else "") + '</div>')
    labs = [f"{r.get('display', '')} → {r['as']}" if r["as"] != r.get("display") else r["as"] for r in plan]
    sup = _supplement_word(labs)
    items = [("Main" if r["where"] == "main" else sup, (lab, f"{dp.TYPES[r['type']]} · {_plain(r.get('name', ''))}"), None)
             for r, lab in zip(plan, labs)]
    panels = [_kv((("Shows", esc(_plain(r.get("shows", "")))), ("Answers", esc(_plain(r.get("answers", "")))),
                   ("Section", esc(_plain(r.get("section", "")))), ("Where", esc(r["where"])),
                   ("Made by", esc(_plain(r.get("made by", "")))), ("State", esc(_plain(r.get("state", ""))))))
              + (f'<pre class=pb-sketch>{esc(dp.sketch(text, r.get("display", "")))}</pre>' if dp.sketch(text, r.get("display", "")) else "")
              for r in plan]
    keyed = sorted(zip(items, panels), key=lambda x: x[0][0] != "Main")          # Main first, the plan's order kept
    return PLAN_CSS + head + _grouped_tabs("dpl", [(g, t, b) for (g, t, _), b in keyed])


# the plan's check list and sketches, this theme's own look (shared ui_parts stays its owners')
PLAN_CSS = ("<style>.pb-checks{list-style:none;margin:4px 0 8px;padding:0;font-size:13.5px;line-height:1.6}"
            ".pb-sketch{margin:8px 0 0;padding:8px 10px;border-radius:6px;background:var(--wash);"
            "font:12.5px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;white-space:pre;overflow-x:auto}</style>")


def _display_line(task: Path, slug: str) -> str:
    """A Display tab's second line: its type, then its name. The name is the face's `name:` line, else the title after
    "<label>," in its first line, else the folder's words; the type is the face's `type:` (or `kind:`) line, else what
    its newest float.tex begins (a figure or a table environment)."""
    face = task / f"{task.name}.md"
    text = face.read_text(encoding="utf-8", errors="ignore") if face.is_file() else ""
    field = lambda k: (re.search(rf"^{k}:\s*(.+?)\s*$", text, re.M) or [None, ""])[1]
    name = field("name")
    if not name:
        m = re.match(r"#\s*[^,\n]*?\b(?:Display|e?Figure|e?Table)\s+\w+\s*[,:·]\s*(.+)", text.strip())
        name = m.group(1).strip() if m else _cap(slug)
    kind = (field("type") or field("kind")).lower()
    if not kind:
        floats = sorted([*task.glob("runs/*/result/float.tex"), *task.glob("display/*/float.tex")],
                        key=lambda f: f.stat().st_mtime)
        body = floats[-1].read_text(encoding="utf-8", errors="ignore") if floats else ""
        kind = next((k for k in ("table", "figure") if f"\\begin{{{k}" in body), "")
    word = next((w for k, w in DISPLAY_TYPES if k in kind), kind.capitalize())
    return f"{word} · {name}" if word else name


def _section_read(task: Path) -> str:
    """A Section's text to read: its paragraphs in order, each under its name (the version page's reader)."""
    paras = [(name or pid, t) for pid, name, t in paragraphs(task) if t]
    return ('<div class=pb-text>' + "".join(f'<h4>{esc(h)}</h4><p>{esc(t)}</p>' for h, t in paras) + '</div>') if paras \
        else '<p class=mut>No text yet: 2 · Write writes it.</p>'


def _paper_files(vdir: Path, root: Path, eid: str = "pp") -> str:
    """The assembled paper to read (JL 261101: "should we show it as well? like different versions of the output with the
    left panel?"): side tabs, each output on the left (the paper as LaTeX builds it, as Word prints it, the Word
    supplement, then earlier rounds), the open one shown on the right as its PDF, with its Open buttons."""
    import json
    try:
        out = json.loads((vdir / "build-manifest.json").read_text(encoding="utf-8")).get("outputs", {})
    except Exception:
        return ""
    f = lambda r: vdir / r if r and (vdir / r).is_file() else None
    sup_pdf = f(out.get("supplement_docx_pdf"))
    sup_docx = f(out.get("supplement_docx_pdf", "")[:-4] + ".docx") if out.get("supplement_docx_pdf") else None
    pieces = [("The paper", "as LaTeX builds it", f(out.get("pdf")), None),
              ("The paper · Word", "as Word prints it", f(out.get("docx_pdf")), f(out.get("docx"))),
              ("The supplement · Word", "as Word prints it", sup_pdf, sup_docx)]
    shown = {p.name for _, _, a, b in pieces for p in (a, b) if p}
    word = vdir / "word"
    older = sorted((x for x in word.glob("*.docx") if x.name not in shown and "supplement" not in x.name),
                   key=lambda x: x.stat().st_mtime, reverse=True) if word.is_dir() else []
    pieces += [(f"Earlier round · {_when(x)}", x.stem, x.with_suffix(".pdf") if x.with_suffix(".pdf").is_file() else None, x) for x in older]
    pieces = [p for p in pieces if p[2] or p[3]]
    if not pieces:
        return ""
    href = lambda x: "/" + quote(ds._rel(x, root))
    items, panels = [], []
    for name, how, pdf, doc in pieces:
        newest = max((x for x in (pdf, doc) if x), key=lambda x: x.stat().st_mtime)
        items.append((name, how))
        made = f'<span class=pb-state>{"draft" if "-draft" in newest.stem else "built"} {_when(newest)}</span>'
        view = (f'<div class=pb-ptop>{made}{_open_btn("⤢ Pop out", href(pdf), f"{name} · {pdf.name}")}</div>'   # a large view pops out
                f'<iframe class=pb-pdf src="{esc(href(pdf))}#view=FitH" title="{esc(name)}"></iframe>') if pdf \
            else f'<p class=mut>{esc(how)}: no PDF beside it to show here.</p>'
        verbs = ((_open_btn("Open the PDF", href(pdf), pdf.name) if pdf else "")
                 + (_open_btn("Open the Word file", href(doc), doc.name) if doc else ""))
        panels.append(view + f'<div class=pb-verbs>{verbs}</div>')
    return _side_tabs(eid, items, panels)


def writing_view(board: Path, root: Path, md, items=()) -> str:
    """H · Writing: a numbered section per version; its Sections as card tabs (each panel its step words), then the
    assembled paper."""
    out, n = "", 0
    for job in sorted(d for d in board.glob("j[0-9]*_*") if d.is_dir() and is_version(d)):
        tasks = sorted(d for d in job.glob("t[0-9]*_*") if d.is_dir())
        secs = [(_cap(re.sub(r"^t\d+_", "", t.name).replace("-", " ")), _state_words(_section_state(t, root))) for t in tasks]
        if len({w for _, w in secs}) == 1:          # the same state on every tab says nothing: drop it
            secs = [(h, "") for h, _ in secs]
        panels = [_section_read(t) + f'<div class=pb-verbs>{_open_btn("Open the Section", _task_url(t, root), t.name)}</div>' for t in tasks]
        paper = _paper_files(board / "delivery" / job.name, root, f"pp{n}")
        n += 1
        out += _section(f"{n} · ✍️ {job.name}", f'<div class=pb-verbs>{_open_btn("Open the version", _version_url(job, root, "report"))}</div>'
                        + (_side_tabs(f"wr{n}", secs, panels) if secs else '<p class=mut>No Sections yet.</p>'))
        if paper:
            n += 1
            out += _section(f"{n} · 📄 The assembled paper", paper)
    return out or '<p class=mut>No version yet.</p>'


SHAPED = {"idea": lambda board, t, root, md, items: idea_view(t, root, md, items),
          "story": lambda board, t, root, md, items: story_view(board, t, root, md, items),
          "dataflow": lambda board, t, root, md, items: dataflow_view(board, t, root, md, items),
          "paperflow": lambda board, t, root, md, items: paperflow_view(board, t, root, md, items)}
