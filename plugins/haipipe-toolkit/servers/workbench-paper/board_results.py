"""A paper Board's RESULTS band: the views from Idea and Story to Writing in the shape settled in b16 s32 (numbered bars,
the main point large, side tabs, the flow map, folder trees), the same on Report and Work."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

from live import draft_steps as ds
from live.frame import _file_url, esc, related_items, related_rows
from live.ui_parts import _bar, _cap, _clean, _kv, _open_btn, _plain, _section, _side_tabs, _when, plural_word
from live.focus_draft import paragraphs
from live.board_read import display_plan, view_topics, _after_table, _face, _field, _first_para, _folder_line, _label_rows, _lead_sentence, _mark, _num, _open_link, _page_url, _rq_lists, _section_state, _state_words, _table, _task_url, _undated, _version_url, explore_tree, is_version
from live.paper_version import build_running
from live.board_evidence import EVIDENCE_KINDS, VALUES_CSS, VALUES_DIALOG, VALUES_JS, empty_job, evidence_body, evidence_word, value_tabs, values_word


def _helpers(topic: Path, root: Path, items, mind: bool = True, drawing: bool = True, label: str = "") -> str:
    """The helpers at the bottom: the drawing (Slides · Draw), the mind map (Idea only). `label` names the part, as a
    view can hold two (JL 261104). The dashed rule above them is the view's (_after_rule)."""
    from live import frame
    rel = lambda p: "/" + quote(ds._rel(p, root))
    of = f" · {label}" if label else ""
    out = ""                                            # Interactions moved into the Process band (JL 261101)
    show, (drawing, png, deck) = drawing, (topic / f"{topic.name}.excalidraw", topic / f"{topic.name}.png", topic / f"{topic.name}.slides.html")
    if show and png.is_file():
        href = frame._draw_url(drawing, root) if drawing.is_file() else rel(png)
        verbs = ([f'<a class=fd-btn data-pop="{esc(topic.name)} · slide" href="{esc(rel(deck))}">Slides</a>'] if deck.is_file() else []) + \
            [f'<a class=fd-btn data-pop="{esc(topic.name)}" href="{esc(href)}">Draw</a>']
        out += _section("🖼️ The drawing" + of, f'<div class=pb-pic><a data-pop="{esc(topic.name)}" href="{esc(href)}"><img src="{esc(rel(png))}" '
                                         f'alt="{esc(topic.name)}"></a><div class=pb-verbs>{"".join(verbs)}</div></div>',
                        "drawn " + _when(png)[:10])
    page = topic / f"{topic.name}.mindmap.html"
    if mind and page.is_file():
        out += _section("🧠 The mind map" + of, f'<div class=pb-verbs><a class=fd-btn data-pop="{esc(topic.name)} · mind map" '
                                          f'href="{esc(rel(page))}">Open the mind map</a></div>', "built " + _when(page)[:10])
    return out


def _studio_panel(topic: Path, root: Path) -> str:
    """A topic's Studio (JL 261104: "why the mind map is not at the top and should be embedded, and where are the studios
    here?"): its mind map drawn in place, its drawing, and the way to its card and canvas. A drawing with no picture yet
    still gets its Draw button."""
    from live import frame
    from live.focus_page import topic_home
    rel = lambda p: "/" + quote(ds._rel(p, root))
    drawing, png, deck = topic / f"{topic.name}.excalidraw", topic / f"{topic.name}.png", topic / f"{topic.name}.slides.html"
    draw = frame._draw_url(drawing, root) if drawing.is_file() else rel(png) if png.is_file() else ""
    verbs = f'<a class=fd-btn href="{esc(topic_home(topic, root))}">Open in Studio</a>' + \
        (f'<a class=fd-btn data-pop="{esc(topic.name)} · slide" href="{esc(rel(deck))}">Slides</a>' if deck.is_file() else "") + \
        (f'<a class=fd-btn data-pop="{esc(topic.name)}" href="{esc(draw)}">Draw</a>' if draw else "")
    pic = (f'<div class=pb-pic><a data-pop="{esc(topic.name)}" href="{esc(draw)}"><img src="{esc(rel(png))}" alt="{esc(topic.name)}"></a></div>'
           if png.is_file() else "")
    return f'<div class=pb-verbs>{verbs}</div>{_canvas(topic, root)}{pic}'


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


def _side_cards(eid: str, tiles: list, panels: list) -> str:
    """Idea's and Story's choices as a left tab and right content (JL 261104: "for each of this, could you make it like the
    style of [Values], we have the left tab and right content"): a card's head and line become the tab's two lines."""
    return _side_tabs(eid, [(t[0], t[1]) for t in tiles], panels)


def _direction_theory(row: dict) -> str:
    """A direction's theory: its `theory` cell, else the `Theory: ...` sentence that opens its reason."""
    said = _plain(row.get("theory", ""))
    if said:
        return said
    m = re.match(r"Theory:\s*(.+?)(?:\.(?:\s|$)|$)", _plain(row.get("reason", "")))
    return m[1] if m else ""


IS_VENUE = re.compile(r"\b(?:MISQ|MIS Quarterly|ISR|Information Systems Research|JMIS|JAIS)\b")


def _no_theory(board: Path, where: str) -> str:
    """What an empty Theory says; an information systems journal expects one, so there it is flagged (JL 261105: "we should
    have the section named theory as well"; "espeically for the IS")."""
    md_file = board / "board.md"
    target = _field(md_file.read_text(encoding="utf-8", errors="ignore"), "venue") if md_file.is_file() else ""
    named = IS_VENUE.search(target or "")
    head = (f'<p class=pb-state style="color:light-dark(#b35c00,#ffc078)">🙋 {esc(named[0])} is an information systems journal: it '
            'expects the theory this paper speaks to, and what the paper says back to it.</p>' if named else "")
    return head + f'<p class=mut>No theory written yet: {where}</p>'


def idea_tabs(topic: Path, md) -> list:
    """Idea's parts (b16 s32 A): Direction large, then the directions considered. The
    Hand-off is no tab: only a question it holds for the person stays, under the Direction (s32-D35).
    Returns [(tab name, its small line, its panel)]."""
    text, parts = _face(topic)
    chosen = ""
    if "direction" in parts:
        lead, rest = _lead_sentence(parts["direction"])
        _, rest = _label_rows(re.sub(r"(?m)^\*\*Direction\*\*:.*\n?", "", rest))   # no stage, no START, SETTING, CONTRAST rows (JL 261104: "could we just remve this?")
        chosen = f'<p class=pb-big>{esc(_cap(lead))}</p>' + md(rest, topic)
    rows = _table(parts.get("directions considered", ""))
    if rows:
        rank = lambda r: next((i for i, w in enumerate(("✅", "fallback", "second", "considered", "lost", "replaced"))
                               if w in r.get("verdict", "")), 9)
        tiles = sorted(rows, key=rank)
        kind = lambda r: " pb-chosen" if rank(r) == 0 else (" pb-gone" if rank(r) >= 4 else "")
        short = lambda t: t if len(t) <= 60 else t[:58].rsplit(" ", 1)[0] + " …"
        when = lambda r: (re.search(r"\b(\d{6})\b", r.get("verdict", "")) or [None, ""])[1]
        considered = _side_cards("dc", [
            (short(_plain(r.get("direction", ""))), _undated(r.get("verdict", "")), "", kind(r).replace(" pb-chosen", " pb-chosen1"))   # the name large, its status small (JL 261104)
            for r in tiles], [_kv((("Direction", esc(_plain(r.get("direction", "")))), ("Verdict", esc(_undated(r.get("verdict", "")))),
                                   ("Reason", esc(_plain(r.get("reason", "")))), ("Decided", esc(when(r)))))
                              for r in tiles])
    else:
        considered = ""
    asks = "\n\n".join(ln.strip() for ln in parts.get("hand-off", "").splitlines() if "🙋" in ln)
    if asks:
        chosen += md(asks, topic)
    theories = []
    if rows:
        theories = [(short(_plain(r.get("direction", ""))), _undated(r.get("verdict", "")), "", _direction_theory(r)) for r in tiles]
    theory = (_side_cards("th", [x[:3] for x in theories], [f'<p>{esc(x[3]) or "No theory written for this direction yet."}</p>' for x in theories])
              if any(x[3] for x in theories) else "")
    return ([("Direction", "the direction chosen", chosen)] if chosen else []) + \
        ([("Directions considered", "what else was weighed", considered)] if considered else []) + \
        ([("Theory", "each direction's theory", theory)] if theory else [])


def _named(n: int, emoji: str, name: str, body: str, word: str = "", waits: str = "") -> str:
    """A numbered section whose name is this theme's own, so the shared EMOJI list is left alone."""
    return _section(f"{n} · {emoji} {name}", body, word, waits)


# ── each bar's state word, read from the part it shows (JL 261106: "every closed bar shows a state word on its right") ──
def _stage(topic: Path | None) -> str:
    """A topic's own **Stage:** (explore, shaping, chosen, agreed), the state of the part its sections show."""
    if topic is None:
        return ""
    text, _ = _face(topic)
    return _plain(_field(text, "Stage")).lower()


def _written(text: str) -> str:
    return "written" if (text or "").strip() else "not written yet"


def _rq_word(rq: str) -> str:
    """The Research Questions' word: how many are still open, from each question's own state after its question mark."""
    qs, _ = _rq_lists(rq)
    states = [(re.match(r".+?\?\s*(.*)$", q) or [None, ""])[1].strip().lower() for _, q in qs]
    if not states:
        return "written" if rq.strip() else "none yet"
    still = sum(not st or st.startswith(("open", "⬜", "not")) for st in states)
    return f"{still} of {len(states)} open" if still else "none open"


def _rows_done(rows: list) -> str:
    """A roadmap table's word: how many of its rows are done (✅), from its `state` column, else its `folder` column."""
    def done(r):
        cell = _plain(r.get("state") or r.get("folder") or "")
        return cell.startswith("✅") or cell.lower().startswith("done")
    return f"{sum(done(r) for r in rows)} of {len(rows)} done" if rows else "nothing yet"


def story_tabs(board: Path, topic: Path, root: Path, md) -> list:
    """Story's parts (b16 s32 B; s32-D44): Pitch large, the Research Questions, Stakes,
    Evidence basis, Venues, Story by Section (its mind map). The Roadmaps are the Plan's (roadmap_section).
    Returns [(tab name, its small line, its panel)]."""
    text, parts = _face(topic)
    rel = lambda p: "/" + quote(ds._rel(p, root))
    tabs = []
    if "pitch" in parts:
        one = _field(parts.get("identity", ""), "One-sentence identity")
        pitch = _plain(parts["pitch"])
        lead = _clean(one) or _clean(re.split(r"(?<=[.;])\s", pitch, 1)[0])
        rest = pitch if one else (re.split(r"(?<=[.;])\s", pitch, 1) + [""])[1]
        tabs.append(("Pitch", "the paper in short", f'<p class=pb-big>{esc(_cap(lead))}</p><p class=pb-state>{esc(_field(text, "Stage"))}</p>'
                     + (f'<p>{esc(rest)}</p>' if rest else "")))
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
        tabs.append(("Research Questions", "what it asks", _side_cards("rq", tiles, panels)))
    elif rq.strip():                                 # a Story that draws its questions its own way still shows them
        tabs.append(("Research Questions", "what it asks", md(rq, topic)))
    if "stakes" in parts:
        tabs.append(("Stakes", "why it matters, and to whom", md(parts["stakes"], topic)))
    if "evidence basis and boundaries" in parts:
        tabs.append(("Evidence basis", "what it can claim, and what it cannot", md(parts["evidence basis and boundaries"], topic)))
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
        full = topic / "delivery" / "venue-comparison.md"
        tabs.append(("Venues", "where it is sent", _side_cards("ve", tiles, panels) + ("" if full.is_file() else md(_after_table(parts["venues"]), topic))))
    if "section narrative" in parts:                 # the narrative IS the mind map (JL 261031)
        tabs.append(("Story by Section", "what each Section says", _narrative(topic, root, parts["section narrative"]) or md(parts["section narrative"], topic)))
    return tabs


def roadmap_section(board: Path, md, n: int) -> str:
    """The Story's Discovery and Task Roadmaps, what is still to read and to run: the Plan's last section (s32-D35)."""
    topic = next((t for k, _, t in view_topics(board, "story") if k != "idea"), None)
    parts = _face(topic)[1] if topic is not None else {}
    road = [(k, parts[k]) for k in ("discovery roadmap", "task roadmap") if k in parts]
    rows = [r for _, b in road for r in _table(b)]
    # each row by its words, not its id (r03: D1, T0 to T2 led every row); the id stays in the face
    no_id = lambda b: re.sub(r"(?m)^\|\s*(?:[A-Z]\d*|[A-Z])\s*\|", "|", b)
    return _bar(n, "Roadmaps", _side_cards("rm", [(k.capitalize(), "the literature still to read" if k.startswith("discovery")
                                                   else "the Runs still to make", "") for k, _ in road],
                                           [md(no_id(b), topic) for _, b in road]), _rows_done(rows)) if road else ""


def _after_rule(helpers: str) -> str:
    """The helpers after the view's one dashed rule (board_views.banded splits the view there)."""
    return "<hr class=pb-rule>" + helpers


RELATED_CSS = ("<style>.pb-relhead{margin:0 0 4px;font-weight:600}.pb-relsaid{margin:0 0 8px;font-size:12.5px;color:var(--muted)}"
               ".pb-relpdf{display:block;width:100%;height:62vh;border:1px solid var(--line);border-radius:6px;background:var(--paper)}</style>"
               # a PDF loads only once its tab and section are on screen; the browser's loading=lazy fetched all 22 on page open
               "<script>document.addEventListener('DOMContentLoaded',function(){var o=new IntersectionObserver(function(es){es.forEach(function(e){"
               "if(e.isIntersecting){e.target.src=e.target.dataset.src;o.unobserve(e.target);}});});"
               "document.querySelectorAll('iframe.pb-relpdf[data-src]').forEach(function(f){o.observe(f);});});</script>")


ARXIV = re.compile(r"https?://(?:www\.)?arxiv\.org/(?:abs|pdf)/([^\s?#]+?)(?:\.pdf)?$")


def _related_tab(item: dict, row: dict, board: Path, root: Path) -> tuple:
    """One related paper as a left tab and its right side: ((short name, author and venue), the panel). A kept PDF or an
    arXiv paper shows its PDF embedded, loaded only when its tab opens (JL 261104: "I want to embed the pdf here as
    well"), with Pop out beside it ("I want it can pop out and read"); arXiv's PDF may be framed though its abstract page
    may not. Any other web address links out, since a publisher's page refuses to be framed."""
    target, title = item["target"] or "", item["title"]
    star = "★ " if row.get("key") else ""
    who = re.search(r"\(([^()]*\d{4}[a-z]?)\)\s*$", title)
    bare = title[:who.start()].strip() if who else title
    tab = (star + bare.split(": ", 1)[0], " · ".join(x for x in (who[1] if who else "", _plain(row.get("venue", ""))) if x))
    said = _plain(row.get("why here", ""))
    head = f'<p class=pb-relhead>{esc(star + title)}</p>' + (f'<p class=pb-relsaid>{esc(said)}</p>' if said else "")
    path = board / "related" / target if target else None
    arxiv = ARXIV.match(target)
    url = f"https://arxiv.org/pdf/{arxiv[1]}" if arxiv else (_file_url(path, root) if path is not None and not re.match(r"https?://", target) and path.is_file() else "")
    if url:
        pop = f'<div class=pb-verbs><a class=fd-btn data-pop="{esc(title)}" href="{esc(url)}" target=_blank rel=noopener>Pop out</a></div>'
        if arxiv or path.suffix.lower() == ".pdf":
            return tab, head + pop + f'<iframe class=pb-relpdf title="{esc(title)}" data-src="{esc(url)}"></iframe>'
        return tab, head + pop
    if re.match(r"https?://", target):
        return tab, head + f'<p class=pb-state>No PDF to show here: this site opens only in its own tab.</p><div class=pb-verbs><a class=fd-btn href="{esc(target)}" target=_blank rel=noopener>Open the paper ↗</a></div>'
    return tab, head + '<p class=pb-state>No PDF or link yet.</p>'


def related_section(board: Path, root: Path, n: int) -> tuple:
    """Story, the Board's related/related.md rows (JL 261104: "could you put the related section to be here?").
    Left tabs, one per paper, under a small name per `bears on`; the open paper's PDF on the right (JL 261104: "please
    change all type of these into this style"). Returns (html, the last section number)."""
    items = related_items(board)
    if not items:
        return "", n
    rows = related_rows(board)[1]
    groups = {}
    for item in items:
        row = rows[item["row"]] if item["row"] is not None else {}
        bears = _plain(row.get("bears on", "")) or ("Not in the table yet" if item["row"] is None else (item["groups"] or ["Other"])[0].capitalize())
        groups.setdefault(bears, []).append(_related_tab(item, row, board, root))
    kept = sum("pb-relpdf" in body or "Pop out" in body for papers in groups.values() for _, body in papers)
    word = "every paper to read here" if kept == len(items) else f"{kept} of {len(items)} to read here"
    return _section(f"{n + 1} · 📚 Related", RELATED_CSS + _grouped_tabs("rl", [(_cap(bears), tab, body) for bears, papers in groups.items() for tab, body in papers]),
                    word), n + 1


# a mind map draws its curves only when on screen, so a section opening redraws them
REDRAW = ("<script>document.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('.fd-h')"
          "&&window.pmDraw)setTimeout(window.pmDraw,30);});</script>")


def idea_view(board: Path, root: Path, md, items=()) -> str:
    """A · Idea, its own button, for the many directions (JL 261105: "I mean seperate this!!!"; "idea for multiple direction,
    story for one direction"; s32-D44): its Studio, every direction weighed, left tabs, then each one's Theory. The chosen one's words are the
    Story's, unless there is no Story yet. The page adds 🙋 Interaction."""
    out, n = "", 0
    has_story = bool(view_topics(board, "story"))
    for _, _, topic in view_topics(board, "idea"):
        stage = _stage(topic)
        out += _bar(None, "🎨 Studio", _studio_panel(topic, root) + REDRAW, stage)
        tabs = dict((h, p) for h, _, p in idea_tabs(topic, md))
        if "Direction" in tabs and not has_story:
            n += 1
            out += _bar(n, "Direction", tabs["Direction"], stage or "written")
        if "Directions considered" in tabs:
            n += 1
            rows = _table(_face(topic)[1].get("directions considered", ""))
            out += _named(n, "🔀", "Directions", tabs["Directions considered"],
                          "one chosen" if any("✅" in r.get("verdict", "") for r in rows) else "none chosen yet")
        n += 1
        out += _named(n, "🎓", "Theory", tabs.get("Theory") or _no_theory(
            board, "each direction names its theory, a <code>theory</code> column in Directions considered (haipipe-paper-ideation)."),
            _written(tabs.get("Theory", "")))
    if not has_story:                                                   # no Story yet: Related follows the idea
        out += related_section(board, root, n)[0]
    return out


def story_view(board: Path, root: Path, md, items=()) -> str:
    """B · Story, its own button, for the one direction chosen (JL 261105: "story for one direction"; s32-D44): its Studio,
    Direction, Pitch, Theory, Research Questions, Stakes and evidence, Related, Venues, Story by Section. The page adds 🙋 Interaction."""
    out, n = "", 0
    for _, _, topic in view_topics(board, "story"):
        stage = _stage(topic) or "written"
        out += _bar(None, "🎨 Studio", _studio_panel(topic, root) + REDRAW, stage)
        tabs = {h: (w, p) for h, w, p in story_tabs(board, topic, root, md)}
        parts = _face(topic)[1]
        def bar(emoji, name, body, word):
            nonlocal n, out
            n += 1
            out += _named(n, emoji, name, body, word)
        for _, _, idea in view_topics(board, "idea"):                   # the chosen direction's words live on the idea topic
            chosen = dict((h, p) for h, _, p in idea_tabs(idea, md)).get("Direction")
            if chosen:
                bar("🧭", "Direction", chosen, _stage(idea) or "chosen")
        if "Pitch" in tabs:
            bar("💡", "Pitch", tabs["Pitch"][1], stage)
        said = _field(parts.get("identity", ""), "Theory")
        whole = parts.get("theory", "")
        bar("🎓", "Theory", md(whole or said, topic) if whole or said else _no_theory(
            board, "a <code>**Theory**:</code> line in the Story's Identity (haipipe-paper-story)."), _written(whole or said))
        if "Research Questions" in tabs:
            bar("❓", "Research Questions", tabs["Research Questions"][1], _rq_word(parts.get("research questions", "")))
        duo = [k for k in ("Stakes", "Evidence basis") if k in tabs]
        if duo:
            bar("⚖️", "Stakes and evidence", _side_cards("se", [(k, tabs[k][0], "") for k in duo], [tabs[k][1] for k in duo]),
                "both written" if len(duo) == 2 else f"{duo[0].lower()} only")
        related, n = related_section(board, root, n)
        out += related
        if "Venues" in tabs:
            venues = _table(parts.get("venues", ""))
            bar("🏛️", "Venues", tabs["Venues"][1], f'target {_plain(venues[0].get("venue", ""))}' if venues else "written")
        if "Story by Section" in tabs:
            bar("🧠", "Story by Section", tabs["Story by Section"][1], stage)
    return out


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


def _canvas(topic: Path, root: Path) -> str:
    """The topic's mind map as the canvas to work on, edited in place where it is read (JL 261102: "I think we should
    have the mindmap canvas to work on"): the same map and endpoint as the topic card's Structured side."""
    from live import frame
    mind = topic / f"{topic.name}.mindmap.md"
    if not mind.is_file():
        return (f'<p class=pb-state>No mind map yet: <code>mindmap.py from-topic {esc(topic.name)}</code> '
                f'(haipipe-mindmap) makes {esc(mind.name)}.</p>')
    try:
        html = frame.mindmap_module().fragment(mind, ds._rel(mind, root), editable=not frame.READ_ONLY_MAPS,
                                               url_of=lambda q: "/" + quote(ds._rel(q, root)))
        # a map not written yet says so by its state word, never by a grey instruction on its root (r03: "Not written
        # yet: ask in the Studio chat…" on Idea's and Story's roots); its root line stays there to type into
        html = re.sub(r'(<p data-edit=arc data-raw=")Not written yet[^"]*("[^>]*>)Not written yet[^<]*(</p>)', r"\1\2\3", html)
        return '<div class=pb-map>' + html + '</div>'
    except Exception as e:                          # a map that fails to read says so, never a blank view
        return f'<p class=pb-state>The mind map did not read: {esc(str(e))}</p>'


def _written_map(topic: Path) -> bool:
    """A topic's mind map a person wrote (its front matter's `written:`), not the one `mindmap.py from-topic` built."""
    mind = topic / f"{topic.name}.mindmap.md"
    return mind.is_file() and re.search(r"(?m)^written:", mind.read_text(encoding="utf-8", errors="ignore")) is not None


def _stub_map(topic: Path) -> bool:
    """A topic's mind map is still the stub `mindmap.py from-topic` writes before anyone fills it: its root's line asks
    for it to be written, and it holds no branch but Files."""
    mind = topic / f"{topic.name}.mindmap.md"
    if not mind.is_file():
        return True
    text = mind.read_text(encoding="utf-8", errors="ignore")
    heads = re.findall(r"(?m)^- (.+?)(?:\s*<!--.*)?$", text)
    return "Not written yet" in text and all(h.strip() == "Files" for h in heads)


def _face_tables(text: str) -> dict:
    """{heading words, lowercased and without its number: [row dicts]} of a face's `### N · <name>` tables."""
    from live.focus_draft import md_tables
    out = {}
    for m in re.finditer(r"(?ms)^###\s+(?:\d+\s*·\s*)?(.+?)\s*$(.*?)(?=^#{2,3}\s|^\S.*\n-{3,}\s*$|\Z)", text):
        tables = md_tables(m.group(2))
        if tables:
            out[m.group(1).strip().lower()] = tables[0]
    return out


def paperflow_map(topic: Path, root: Path) -> str:
    """Paper flow's map, from its face (r03: the map showed only Send and a cut Topic line, while the face held the
    Sections): the send, each Section in reader order with what it answers, its displays, its evidence and its words,
    then the dated steps to the send. Drawn on every open from the face, the one source; "" when it has no Sections."""
    face = topic / f"{topic.name}.md"
    text = face.read_text(encoding="utf-8", errors="ignore") if face.is_file() else ""
    tables = _face_tables(text)
    secs = tables.get("sections") or []
    if not secs:
        return ""
    from live import frame
    from live.paper_version import paper_map
    frame.mindmap_module()
    import mmbuild
    label = lambda k: (re.search(rf"(?m)^\*\*{k}:\*\*\s*`?([^`\n]+?)`?\s*$", text) or [None, ""])[1]
    t = topic.name
    kids = []
    send = label("Send")
    if send:
        kids.append(mmbuild.built(f"{t}/send", f"Send · {send}"))
    for i, r in enumerate(secs, 1):
        name = r.get("section") or r.get("S") or f"Section {i}"
        words = r.get("words", "")
        leaves = [mmbuild.built(f"{t}/s{i}/{k}", f"[{k}] {v}") for k, v in
                  (("answers", r.get("answers", "")), ("displays", r.get("displays", "")), ("evidence", r.get("evidence", "")),
                   ("words", "" if re.match(r"^\d", words or "") else words), ("job", r.get("job", ""))) if v and v not in ("—", "-")]
        kids.append(mmbuild.built(f"{t}/s{i}", f"{i} · {name}" + (f" · {words} words" if re.match(r"^\d", words or "") else ""),
                                  leaves))
    steps = tables.get("timeline") or []
    if steps:
        kids.append(mmbuild.built(f"{t}/steps", "Steps to the send", [
            mmbuild.built(f"{t}/steps/{j}", f"[{r.get('when', '')}] {r.get('step', '')}"
                          + (f" · {re.sub(r'^[^A-Za-z<]+', '', r.get('state', ''))}" if r.get("state") else ""))
            for j, r in enumerate(steps)]))
    note = " · ".join(x for x in (label("Tags"), label("Stage")) if x)
    return paper_map("Paper flow", kids, [note] if note else [], key=t)


def _plan_part(board: Path, topic: Path, root: Path) -> tuple:
    """(body, word) of a Plan part (r02: Data flow drew a stub map and a grey "Not written yet: ask in the Studio chat"
    line, while its -drawing.yaml held the data → linking → tables flow): the flow from the drawing's words when the
    topic has them, its mind map when one is written, else the topic's drawing, else a short state."""
    flow = dataflow_map(board, topic) or paperflow_map(topic, root)
    stub = _stub_map(topic)
    canvas = "" if stub or (flow and not _written_map(topic)) else _canvas(topic, root)   # a built map says what the
                                                                                          # flow above already draws
    if flow or canvas:
        return flow + canvas, (_stage(topic) or "drawn")
    drawing = _topic_canvas(board, root, re.sub(r"^s\d+-", "", topic.name))
    return (drawing or '<p class=mut>No map drawn yet.</p>'), ("drawn" if drawing else "no map yet")


def plan_view(board: Path, root: Path, md, items=()) -> str:
    """B · Data + Paper Plan, one view (JL 261104: "Data flow and Paper flow to be one view of Plan"): 1 · Data flow, how the data
    become each answer, then 2 · Paper flow, the Sections in reader order and the steps to the send, each worked on as
    its topic's mind map, the window's full width (b16 s32; JL 261102: "the data flow and paper flow are not what we
    want"); then their drawings. The cards they had (the flow map from -drawing.yaml, Questions to Runs, Send, Sections,
    Displays, Timeline) left; the Questions and the displays have their own views, Story and Displays."""
    parts = view_topics(board, "plan")
    icon = {"Data flow": "🗄️", "Paper flow": "📝"}                       # every section has its emoji (JL 261105)
    maps = "".join(_named(n, icon.get(name, "📌"), name, *_plan_part(board, topic, root))
                   for n, (_, name, topic) in enumerate(parts, 1))
    return (f'<div class=pb-canvas>{maps}</div>' + roadmap_section(board, md, len(parts) + 1)
            + _after_rule("".join(_helpers(topic, root, items, mind=False, label=name) for _, name, topic in parts)))


def explore_view(board: Path, root: Path, md, items=()) -> str:
    """C · Support blocks as folder trees (JL 261101: "more like the folder tree, only show the related folder tree";
    "we will have both the work and discovery, as two sections"; "the works from multiple projects"): 1 · Work and
    2 · Discovery, each one tree per Project, its Blocks, Jobs and Tasks this paper names, one line each, each a link."""
    tree = explore_tree(board)
    named = tree.get("named", {})
    main = max(named, key=named.get) if named else None       # the Job the pages name most: the paper's main analysis
    url = lambda d: "/_board/workbench?" + "&".join(f"{a}={quote(b)}" for a, b in (("path", ds._rel(d, root)), ("layout", "focus")))

    def apart(lines: list) -> list:
        """Sibling Tasks' lines without the words they all share (s32 E r03: five lines read "Tables of whether…")."""
        if len(lines) < 2 or not all(lines):
            return lines
        ws = [ln.split() for ln in lines]
        a = next((i for i in range(min(map(len, ws))) if len({w[i] for w in ws}) > 1), 0)
        z = next((i for i in range(1, min(map(len, ws)) - a) if len({w[-i] for w in ws}) > 1), 1) - 1
        return [_cap(" ".join(w[a:len(w) - z]).strip(" ,.;*`()")) for w in ws]

    def node(d: Path, kids: str = "", line: str = None, open_: bool = False) -> str:
        """One folder's line. A folder with children folds (JL 261102: "I want it can be collapsed"): its row is the
        fold's summary, ▸ shut, ▾ open; its name opens the folder in the pop-out, not a new page ("when we click it,
        I don't want to switch but to have the pop out window first"); the pop-out keeps "Open in its own tab"."""
        line = _folder_line(d) if line is None else line
        if re.match(r"t\d", d.name) and line and line == _folder_line(d.parent):
            line = ""
        name = esc(d.name).replace("_", "_<wbr>")                # a phone breaks a long name only after "_"
        big = d == main
        row = (f'<a href="{esc(url(d))}" data-pop="{esc(d.name)}" title="{esc(line)}"{" class=pb-main" if big else ""}>{name}/</a>'
               + ('<em class=pb-mainw>main analysis</em>' if big else "")
               + (f'<small>{esc(line)}</small>' if line else ""))
        if not kids:
            return f'<li><div class="pb-frow pb-leaf">{row}</div></li>'
        return (f'<li><details{" open" if open_ else ""}><summary class=pb-frow>{row}</summary>'
                f'<ul>{kids}</ul></details></li>')

    MARK = {"complete": "✅", "done": "✅", "failed": "❌", "blocked": "🔶", "running": "⏳"}

    def runs(task: Path) -> str:
        """A Task's Runs, one leaf each (JL 261102: "we also want to see what are the runs under each task"): its
        receipt's mark (⬜ no receipt yet) and its headline; the name opens the Run in the pop-out."""
        out = ""
        for r in sorted(d for d in (task / "runs").glob("r[0-9]*") if d.is_dir()):
            rt = r / "result" / "runtime.yaml"
            text = rt.read_text(encoding="utf-8", errors="ignore") if rt.is_file() else ""
            st = (re.search(r"(?m)^status:\s*(\S+)", text) or [None, ""])[1]
            head = (re.search(r'(?m)^headline:\s*"?(.*?)"?\s*$', text) or [None, ""])[1]
            out += (f'<li><div class="pb-frow pb-leaf pb-run"><a href="{esc(url(r))}" data-pop="{esc(task.name)} · {esc(r.name)}" '
                    f'title="{esc(head)}">{MARK.get(st, "⬜")} {esc(r.name)}</a>' + (f'<small>{esc(head)}</small>' if head else "")
                    + '</div></li>')
        return out

    def tasks(job: Path, ts) -> str:
        """Every Task of a Job (JL 261102: a Job the pages name without its Tasks showed no fold), each folding to
        its Runs; the Tasks the pages name come first only by their number, like the rest."""
        ts = sorted(set(ts) | {t for t in job.glob("t[0-9]*_*") if t.is_dir()})
        return "".join(node(t, runs(t), line=ln) for t, ln in zip(ts, apart([_folder_line(t) for t in ts])))
    out = ""
    for n, (kind, name, none) in enumerate((("work", "Work", "No work folder named yet."),
                                            ("discovery", "Discovery", "No discovery folder named yet.")), 1):
        trees = ""
        for proj, blocks in sorted(tree.get(kind, {}).items(), key=lambda x: (x[0] != board.parents[1], x[0].name)):
            inner = "".join(node(b, "".join(node(j, tasks(j, ts)) for j, ts in sorted(jobs.items())), open_=True)
                            for b, jobs in sorted(blocks.items()))   # Blocks open, Jobs shut: the tree starts short
            trees += (f'<ul class=pb-ftree><li><details open><summary class=pb-frow><a href="{esc(url(proj))}" '
                      f'data-pop="{esc(proj.name)}">{esc(proj.name)}/</a></summary>'
                      f'<ul><li><details open><summary class=pb-frow><span>{kind}/</span></summary><ul>{inner}</ul></details></li></ul>'
                      f'</details></li></ul>')
        venues = "/_board/workbench?" + "&".join(f"{a}={quote(b)}" for a, b in (("path", ds._rel(board, root)), ("layout", "focus"),
                                                                                 ("section", "report"), ("group", "story")))
        papers = (board / "related").is_dir() and any((board / "related").iterdir())
        empty = f'<p class=mut>{esc(none)}</p>' if kind == "work" or not papers else (   # the venue's papers, one click
            f'<p class=mut>No discovery folder named yet: the venue\'s papers sit in '            # away, only when there
            f'<a href="{esc(venues)}">Story › Venues</a>, the related-work map.</p>')              # are some (r03)
        blocks = sum(len(b) for b in tree.get(kind, {}).values())
        out += _bar(n, name, trees or empty, plural_word(blocks, "Block", "Blocks") if blocks else "none named yet")
    return out


def evidence_view(board: Path, root: Path, md, items=()) -> str:
    """D · Evidence: 1 values, 2 citations, each a side tab per Task whose panel shows the thing itself. The displays
    are a view of their own, E · Displays, after this one (JL 261101: "put the display outside of the Evidence, and put
    it after the Evidence and before the Writing, to highlight it")."""
    return _evidence_kinds(board, root, ("Values", "Citations"))[0] or '<p class=mut>No values or citations Job yet.</p>'


def displays_view(board: Path, root: Path, md, items=()) -> str:
    """E · Displays (JL 261101, its own view between Evidence and Writing): 1 · the plan, each display against the
    venue's display rules (haipipe-paper-plan's display plan, when the Board has one); 2 · the displays, one side tab
    per pool Task (Figure 1 (Display A), its type and name), its panel the newest preview.pdf, the display as the paper
    prints it, then how it was made; and all of them as one PDF (build_displays_pdf.py). The plan is the s06
    display-plan topic's drawing only; its venue check lines live in that drawing and in display_plan.py check."""
    out, n = "", 0
    plan = _topic_canvas(board, root, "paper-displays")   # JL 261102: "we might want to have this to be a excalidraw
    if plan:                                              # only. No need to put others" (the venue check stays in s06)
        n += 1
        out += _bar(n, "Plan", plan, _stage(next((t for t in sorted(board.glob("s[0-9]*-paper-displays")) if t.is_dir()), None)) or "drawn")
    body, n = _evidence_kinds(board, root, ("Displays",), n)
    if not (out or body):
        return '<p class=mut>No display Job or display plan yet.</p>'
    # JL 261102: "after the display, could you add a new section named 3. Examples"; JL 261103: "we can add the things
    # like 3-Examples": it always shows, saying how to fill it while it is empty. Its questions are the page's 🙋 Interaction.
    n += 1
    examples = _display_examples(board, root)
    body += _named(n, "🔍", "Examples", examples or (
        '<p class=mut>No examples yet. The target venue\'s published displays go on one canvas, the Board topic '
        '<code>sNN-paper-display-examples</code> (haipipe-paper-display, Examples).</p>'), "drawn" if examples else "nothing yet")
    return out + body


def _topic_canvas(board: Path, root: Path, slug: str) -> str:
    """A Board topic `sNN-<slug>` shown as its drawing only: the picture, opening the Excalidraw editor, and a Draw
    button; nothing else (JL 261102). Empty when the topic or its picture is missing."""
    from live import frame
    topic = next((t for t in sorted(board.glob(f"s[0-9]*-{slug}")) if t.is_dir()), None)
    if topic is None:
        return ""
    png, drw = topic / f"{topic.name}.png", topic / f"{topic.name}.excalidraw"
    if not png.is_file():
        return ""
    href = frame._draw_url(drw, root) if drw.is_file() else "/" + quote(ds._rel(png, root))
    return (f'<div class=pb-verbs>{_open_btn("Draw", href, topic.name)}</div>'
            f'<a data-pop="{esc(topic.name)}" href="{esc(href)}"><img src="/{esc(quote(ds._rel(png, root)))}" '
            f'alt="{esc(topic.name)}" loading=lazy style="display:block;max-width:100%;border:1px solid var(--line);'
            'border-radius:6px"></a>')


def _display_examples(board: Path, root: Path) -> str:
    """3 · Examples: the displays of the target venue's papers on one canvas, to compare with ours (JL 261102: "what I
    want is just one excalidraw and put all other papers's displays only ... no more text here"): the Board's
    `sNN-paper-display-examples` drawing only."""
    return _topic_canvas(board, root, "paper-display-examples")


def _check_href(job: Path, root: Path, kind: str) -> str:
    """The evidence Job's Check view, where the whole-paper check is read in full."""
    return _version_url(job, root, "report") + "&group=" + ("value-check" if kind == "Values" else "cite-check")


def _evidence_kinds(board: Path, root: Path, kinds: tuple, n: int = 0, only: tuple | None = None,
                    check: bool = True, since=None) -> tuple[str, int]:
    """The numbered sections of these evidence kinds (Values, Citations, Displays), in that order, each a side tab per
    Task; the displays also as one PDF (`delivery/<job>/<job>-all-displays.pdf`). The Board's Evidence, a version's
    Values, Citations and Display views and the evidence Jobs draw these same sections, so their words agree (261106,
    review round 2). A Job's whole-paper check (t99) is never a tab: it shows once, a verdict line above the tabs
    (`check`; off in the Check view itself). Its state word comes from that check, each citation key counted once;
    what differs or is missing waits under the closed bar. `only`: only these display groups (main, supplement,
    unplanned), as a version's Display-Main and Display-Appendix. `since(task or None, tab name)`: a revision's word for
    a tab, what this send did to it ("same as j11_…", "new in this send", "asked by Reviewer 2"), or None."""
    from live import evidence_read as er
    since = since or (lambda task, head: None)
    jobs = [d for d in sorted(board.glob("j[0-9]*_*")) if d.is_dir() and not is_version(d)]
    out = ""
    for kind, pat in sorted((k for k in EVIDENCE_KINDS if k[0] in kinds), key=lambda k: ("Values", "Citations", "Displays").index(k[0])):
        job = next((j for j in jobs if re.search(pat, j.name, re.I)), None)
        if job is None:
            continue
        top = er.verdict(job, root, kind, _check_href(job, root, kind)) if check and kind != "Displays" else ""
        vtabs = value_tabs(job, root) if kind == "Values" else None
        if vtabs:                                # side tabs, each a readable topic with its raw table (JL 261104)
            n += 1
            # the word agrees with the check (r02: "all current" stood beside "1 differs"): what differs first, then a
            # raw table whose source moved, then how many printed numbers match
            word, waits = er.value_state(er.job_values(job))
            fresh = values_word(job, root)
            if not waits and (word == "nothing yet" or fresh.endswith("need a look")):
                word = fresh or word
            out += _bar(n, kind, f'<div class=pb-verbs>{_open_btn(f"Open {job.name}", _task_url(job, root))}</div>' + top + VALUES_CSS
                        + _side_tabs("evV", [(h, since(None, h) or w) for h, w, _ in vtabs], [p for _, _, p in vtabs]) + VALUES_DIALOG + VALUES_JS,
                        word, waits)
            continue
        tasks = sorted((x for x in job.glob("t[0-9]*_*") if x.is_dir() and not er.is_check(x)), key=_num)
        tiles, panels = [], []
        dp = display_plan() if kind == "Displays" else None
        paper_as = {r.get("display", ""): dp.title(r) for r in (dp.rows(board) if dp else [])}
        plan_of = {r.get("display", ""): r for r in (dp.rows(board) if dp else [])}
        groups = []                              # (group, plan order) per tile, for the Displays' Main / Appendix lists
        statuses = []                            # each Task's status, for the section's state word
        for t in tasks:                          # each item to read: its list on the left, the thing itself on the right
            label, status, body = evidence_body(t, root)
            if kind == "Citations" and er.cite_rows(t):   # its claim, then one line per key; the cards are the Check
                body = er.cite_lines(t, root)               # view's (r02: the same three cards in both views)
                status = er.cite_state(er.cite_rows(t))[0]
            if kind == "Values" and er.value_data(t).get("rows"):   # each printed number drawn, no framed page
                data = er.value_data(t)
                body = er.value_check_html(data, t, root) + f'<p><a class=fd-btn href="{esc(_task_url(t, root))}">Open {esc(t.name)} ↗</a></p>'
                status = er.value_state(data)[0]
            statuses.append(status)
            words = re.sub(r"^t\d+_", "", t.name).replace("-", " ")
            words = re.sub(r"^(?:e?figure|e?table|values|cite)\d*\s*", "", words, flags=re.I)
            head = label if label and label.lower() not in ("values", "citations") else _cap(words)
            line = words if head == label else re.sub(r"^\d+\s+", "", status or "")
            line = "waiting" if line.startswith("waits") else line
            if kind in ("Citations", "Values") and (er.cite_rows(t) or er.value_data(t).get("rows")):
                line = status                    # its tab says how many keys are verified, or what differs
            if kind == "Displays":               # JL 261101: "for each display, we might also want to have the name and type"
                line = _display_line(t, words)
                group, order, head = _display_place(t, label, head, dp, paper_as, plan_of)
                groups.append((group, order))
            tiles.append((head, since(t, head) or line or status, ""))
            panels.append(body)
        if kind == "Displays" and only is not None:   # a version's Display-Main or Display-Appendix: those groups only
            keep = [k for k, (g, _) in enumerate(groups) if g in only]
            tiles, panels, groups, statuses = ([x[k] for k in keep] for x in (tiles, panels, groups, statuses))
            if not tiles:
                continue
        book = board / "delivery" / job.name / f"{job.name}-all-displays.pdf"   # build_displays_pdf.py writes it
        whole = (_open_btn("Open all displays as one PDF", "/" + quote(ds._rel(book, root)), book.name)
                 + f'<span class=pb-state>built {_when(book)}</span>') if kind == "Displays" and book.is_file() else ""
        n += 1
        if kind == "Displays" and tiles:         # grouped, Main then Appendix (JL 261101: "groups them in different groups,
            sup = _supplement_word(list(paper_as.values()) + [h for h, _w, _x in tiles])   # like the main"), each card thinner
            name = {"main": "Main", "supplement": sup, "method": "Method", "unplanned": "Others"}   # JL 261102: candidates not in the plan, "a new section here as Others"
            keyed = sorted(zip(groups, tiles, panels), key=lambda x: (("main", "supplement", "method", "unplanned").index(x[0][0]), x[0][1]))
            tabs = _grouped_tabs("evD", [(name[g], (h, w), b) for (g, _), (h, w, _), b in keyed])
        else:
            tabs = _side_tabs("ev" + kind[0], [(h, w) for h, w, _ in tiles], panels) if tiles else empty_job(job)
        keys = er.job_cites(job) if kind == "Citations" else []
        checked = er.job_values(job) if kind == "Values" else {}
        if keys:                                 # each key once, from the whole-paper check (a key in two groups, or in
            word, waits = er.cite_state(keys)    # a group and the check, was counted twice: "0 of 6")
        elif checked.get("rows"):                # the Values word is the check's: what differs waits under the bar
            word, waits = er.value_state(checked)
        else:
            word, waits = evidence_word(kind, statuses), ""
        out += _bar(n, kind, f'<div class=pb-verbs>{whole}{_open_btn(f"Open {job.name}", _task_url(job, root))}</div>' + top + tabs,
                    word, waits)
    return out, n


def _display_place(t: Path, label: str, head: str, dp, paper_as: dict, plan_of: dict) -> tuple:
    """(group, order, head) of one display Task: where it goes (main, supplement, method, unplanned), its place in the plan, and
    what the paper calls it (Figure 1 (Display A)), from the display plan, by any key its face answers to."""
    face = t / f"{t.name}.md"
    ks = dp.keys(face.read_text(encoding="utf-8", errors="ignore")) if dp and face.is_file() else []
    head = next((paper_as[k] for k in ks if k in paper_as), head)
    r = next((plan_of[k] for k in ks if k in plan_of), None)
    order = list(plan_of).index(r.get("display", "")) if r is not None else 999
    fgroup = _field(face.read_text(encoding="utf-8", errors="ignore"), "group").lower() if face.is_file() else ""
    if fgroup in ("method", "methods"):
        group = "method"             # a display that explains how the study is done, for a reader such as an
                                     # advisor (JL 261106: "we might have a section named Method")
    elif fgroup == "others":
        group = "unplanned"          # a draft shown apart until it is placed (JL 261104: "先放到 other 里面去")
    elif r is not None:              # the plan says where it goes
        group = r["where"]
    elif plan_of:                    # a plan that does not name it
        group = "unplanned"
    else:                            # no plan: the face's label says where it goes and its number (JL 261103:
        lab = re.match(r"(Extended Data |Supplementary )?(Figure|Table) (\d+)", label or "")   # "I didn't see
        if lab:                      # the fairness figure": label "Extended Data Figure 1" on t53 sat under Main's
            group = "supplement" if lab.group(1) else "main"   # t07 and Figure 4 (t06) after Figure 5 (t04))
            order = (lab.group(2) == "Table") * 100 + int(lab.group(3))
        else:                        # t51 and on, or an eTable / Appendix label, is outside the main text
            group = "supplement" if _num(t) >= 50 or re.match(r"(?i)(e(?=fig|tab)|appendix|supp)", label or "") else "main"
    return group, order, head


def display_groups(board: Path, tasks: list) -> dict:
    """{display Task: its group}, as the Displays tabs place it (a version's Display-Main and its Process list the same
    displays)."""
    dp = display_plan()
    rows = dp.rows(board) if dp else []
    paper_as = {r.get("display", ""): dp.title(r) for r in rows}
    plan_of = {r.get("display", ""): r for r in rows}
    out = {}
    for t in tasks:
        face = t / f"{t.name}.md"
        label = _field(face.read_text(encoding="utf-8", errors="ignore"), "label") if face.is_file() else ""
        out[t] = _display_place(t, label, label, dp, paper_as, plan_of)[0]
    return out


def _supplement_word(labels: list) -> str:
    """What the venue calls the displays outside the main text: Extended Data (Nature journals), Supplement (eFigure,
    Supplementary Table), else Appendix."""
    if any(x.startswith("Extended Data") for x in labels):
        return "Extended Data"
    return "Supplement" if any(re.match(r"(?:e(?:Figure|Table)|Supplementary)", x) for x in labels) else "Appendix"


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
    """E · Displays' plan, from the display plan (haipipe-paper-plan; JL 261101: "we should also have the plan for the
    displays"; "the display ... should also follow the venue"): the venue check first, then each display as a side tab
    (Figure 1 (Display A), its type and name), its panel what it shows, where it goes, its Run and its sketch."""
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
    labs = [dp.title(r) for r in plan]
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


def _section_read(task: Path, root: Path | None = None) -> str:
    """A Section's text to read: its paragraphs in order, each under its name, each sentence on its own numbered line
    (JL 261101: "the content here is not readable? could you still make each sentence to be a line"); a citation
    command reads as its keys. One owner, focus_draft.content_read, so the Section's own Text reads the same (r02)."""
    from live.focus_draft import content_read
    return content_read(task, root) or '<p class=mut>No text yet: 2 · Write writes it.</p>'


# the Section's sentences, one per line with a small number, citations in grey (this theme's own look)
WRITING_CSS = ("<style>.pb-sents{margin:2px 0 10px;padding-left:2.1em;line-height:1.5}"
               ".pb-sents li{margin:0 0 3px;padding-left:2px}.pb-sents li::marker{color:var(--muted);font-size:11.5px}"
               ".pb-cite{color:var(--muted);font-size:.88em}"
               # JL 261104: the Section's button in the panel's top right corner, staying there while you read down
               ".pb-corner{float:right;position:sticky;top:8px;z-index:2;margin:0 0 8px 12px}"
               ".pb-corner .fd-btn{background:var(--bg)}</style>")


def _pdf_facts(pdf: Path | None) -> tuple[str, str]:
    """A PDF's page count and the program that drew it, read from the file on every open."""
    import subprocess
    if pdf is None or pdf.suffix != ".pdf":
        return "", ""
    try:
        info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, timeout=5).stdout
    except (OSError, subprocess.SubprocessError):
        return "", ""
    field = lambda k: (re.search(rf"^{k}:\s*(.+)$", info, re.M) or [None, ""])[1].strip()
    return field("Pages"), field("Producer")


def _tab_flag(kind: str, man: dict, pdf: Path | None, running: bool, stand_in: bool = False) -> str:
    """Each tab's state, one short line on the tab (JL 261104: "could you flag each tab' status?"): can it be read now,
    and what is not final yet. Everything comes from the manifest and the file itself; nobody types it."""
    pages, producer = _pdf_facts(pdf)
    count = f" · {pages} pages" if pages else ""
    draft = " · draft" if man.get("status") != "READY" else ""
    if kind == "latex":
        if running and not man.get("pdf_only"):
            return "⏳ Rebuilding: last build shown"
        return f"✅ Read now{draft}{count}"
    if kind == "word":
        if running:
            return "⏳ Rebuilding: do not open"
        if stand_in or "LibreOffice" in producer:
            return "❗ Word stuck: layout not final"
        return f"✅ Read now{draft}{count}"
    if kind == "letter":
        cover = man.get("cover_letter") or {}
        off = [c for c in cover.get("checks", []) if not c.get("ok")]
        return f"❗ {len(off)} checks open" if off else f"✅ Read now{draft}"
    if kind == "portal":
        portal = man.get("portal") or {}
        uploads = portal.get("uploads") or []
        ready = sum(u.get("state") == "ready" for u in uploads)
        return f"⬜ {ready} of {len(uploads)} uploads ready" if uploads else "⬜ Not ready"
    return ""


def _paper_files(vdir: Path, root: Path, eid: str = "pp") -> str:
    """The assembled paper to read (JL 261101: "should we show it as well? like different versions of the output with the
    left panel?"): side tabs, each output on the left (the paper as LaTeX builds it, as Word prints it, the Word
    supplement, then earlier rounds), the open one shown on the right as its PDF, with its Open buttons."""
    import json
    try:
        man = json.loads((vdir / "build-manifest.json").read_text(encoding="utf-8"))
    except Exception:
        return ""
    out = man.get("outputs") or {}
    if not isinstance(out, dict):      # the Word step ran alone, with no build before it (see paper_version.built_outputs)
        return ""
    f = lambda r: vdir / r if r and (vdir / r).is_file() else None
    sup_pdf = f(out.get("supplement_docx_pdf"))
    sup_docx = f(out.get("supplement_docx_pdf", "")[:-4] + ".docx") if out.get("supplement_docx_pdf") else None
    letter = (man.get("cover_letter") or {}).get("outputs") or {}
    if not letter.get("pdf"):                    # JL 261103: "where is the cover letter?": a letter Task exported on its
        for own in sorted(vdir.glob("t3[0-9]_*letter*")):   # own, before the build has [coverletter], still shows
            letter = {"pdf": f"{own.name}/word/{own.name}.pdf", "docx": f"{own.name}/word/{own.name}.docx"}
            break
    by = man.get("word_pdf_printed_by") or {}      # b16.j02-s22 261104: Word stuck, and these tabs showed LibreOffice's print
    running_now = build_running(vdir)
    word_how = lambda key, pdf: _tab_flag("word", man, pdf, running_now, by.get(key) == "stand-in")
    # JL 261102: "we should say the results here as well": every document the build makes, the letter too
    pieces = [("The paper", _tab_flag("latex", man, f(out.get("pdf")), running_now), f(out.get("pdf")), None),
              ("The paper · Word", word_how("main_docx", f(out.get("docx_pdf"))), f(out.get("docx_pdf")), f(out.get("docx"))),
              ("The supplement", _tab_flag("latex", man, f(out.get("supplement")), running_now), f(out.get("supplement")), None),
              ("The supplement · Word", word_how("supplement_docx", sup_pdf), sup_pdf, sup_docx),
              ("The combined copy", "paper and supplement in one PDF", f(out.get("combined")), None),
              ("The cover letter", _tab_flag("letter", man, f(letter.get("pdf")), running_now), f(letter.get("pdf")), f(letter.get("docx")))]
    # JL 261102: "add the new tab for the submission portal": the send's submission Job (jNN_submission_…, its face
    # `for: <this version>`) writes delivery/<that Job>/portal-fill.html, every portal field with its value to paste
    for sj in sorted(vdir.parent.parent.glob("j[0-9]*_submission_*")):
        face = sj / f"{sj.name}.md"
        if face.is_file() and re.search(rf"(?m)^for:\s*{re.escape(vdir.name)}\s*$", face.read_text(encoding="utf-8", errors="ignore")):
            fill = vdir.parent / sj.name / "portal-fill.html"
            pieces.append(("The submission portal", _tab_flag("portal", man, None, running_now), fill if fill.is_file() else None, None))
    pieces = [_or_adopted(vdir, p) if p[0].endswith("· Word") else p for p in pieces]
    shown = {p.name for _, _, a, b in pieces for p in (a, b) if p}
    word = vdir / "word"
    older = sorted((x for x in word.glob("*.docx") if x.name not in shown and "supplement" not in x.name),
                   key=lambda x: x.stat().st_mtime, reverse=True) if word.is_dir() else []
    earlier = [p for p in pieces if p[2] or p[3]]            # how many stand above the fold (below: JL 261103)
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
                f'<iframe class=pb-pdf src="{esc(href(pdf))}{"" if pdf.suffix == ".html" else "#view=FitH"}" title="{esc(name)}"></iframe>') if pdf \
            else f'<p class=mut>{esc(how)}: no PDF beside it to show here.</p>'
        verbs = ((_open_btn("Open the page" if pdf.suffix == ".html" else "Open the PDF", href(pdf), pdf.name) if pdf else "")
                 + (_open_btn("Open the Word file", href(doc), doc.name) if doc else ""))
        panels.append(view + f'<div class=pb-verbs>{verbs}</div>')
    running = '<p class=pb-state>⏳ A build is running: these are the last built files.</p>' if build_running(vdir) else ""
    draft = ('<p class=pb-state>📝 Word draft: displays float to page tops, not placed by measuring. Run a full build before sending.</p>'
             if man.get("word_draft") else "")
    return running + draft + _fold_earlier(_side_tabs(eid, items, panels), eid, len(earlier), len(items))


def _or_adopted(vdir: Path, row: tuple) -> tuple:
    """A Word row with no file: `word_round.py adopt` renames the build's -draft files to -v<n> (Paper-PhyAbsence 261104:
    "the panel's Word rows have no file until the next full build"), so the newest adopted copy shows until then."""
    name, how, pdf, doc = row
    if pdf or doc:
        return row
    supplement = "supplement" in name.lower()
    kept = sorted((x for x in (vdir / "word").glob("*-v[0-9]*.docx") if ("supplement" in x.name) == supplement),
                  key=lambda x: x.stat().st_mtime, reverse=True)
    if not kept:
        return row
    twin = kept[0].with_suffix(".pdf")
    return name, "the copy adopted for the round", twin if twin.is_file() else None, kept[0]


def _fold_earlier(tabs: str, eid: str, start: int, total: int) -> str:
    """The older rounds' side tabs behind one closed fold at the list's end (JL 261103: "for the early round, could you
    just first to hide them?"), no count; they open as before once it is unfolded. A build with nothing current yet
    leaves the fold open, so the panel on show has its tab in sight."""
    if start >= total:
        return tabs
    first = tabs.index(f'data-pbtab="{eid}{start}"')
    at, end = tabs.rindex("<button", 0, first), tabs.index("</div><div class=pb-read>", first)
    return (tabs[:at] + f'<details class=pb-earlier style="flex-basis:100%"{" open" if start == 0 else ""}>'
            '<summary style="cursor:pointer;font-size:13px;color:var(--muted);padding:6px 9px">Earlier rounds</summary>'
            + tabs[at:end] + "</details>" + tabs[end:])


PORTAL_WORDS = {"ready": "✅ ready", "draft": "🔶 built, not approved", "stale": "❗ stale", "missing": "⬜ missing"}


def _portal(vdir: Path, root: Path) -> str:
    """What goes into the venue's portal as it is (JL 261102: "the final delivery content that are ready to submit
    directly in the portal"): the build's portal packet, delivery/<job>/portal/, one row per upload slot with its
    file and its state, each file opening in the pop-out (haipipe-paper-assemble § The portal packet)."""
    import json
    try:
        portal = json.loads((vdir / "build-manifest.json").read_text(encoding="utf-8")).get("portal") or {}
    except Exception:
        return ""
    ups = portal.get("uploads") or []
    if not ups:
        return ""
    folder = vdir / str(portal.get("folder", "portal"))
    href = lambda x: "/" + quote(ds._rel(x, root))
    rows = []
    for i, u in enumerate(ups, 1):
        files = [folder / n for n in u.get("files") or [] if (folder / n).is_file()]
        links = " ".join(_open_btn(x.name, href(x), x.name) for x in files) or '<span class=mut>no file yet</span>'
        note = "; ".join(x for x in (u.get("detail", ""), u.get("note", "")) if x)
        rows.append(f'<tr><td>{i}</td><td>{esc(u.get("slot", ""))}</td><td>{links}</td>'
                    f'<td>{esc(PORTAL_WORDS.get(u.get("state"), u.get("state", "")))}</td><td class=mut>{esc(note)}</td></tr>')
    table = folder / "portal.md"
    head = (f'<p class=pb-state>{portal.get("ready", 0)} of {len(ups)} slots ready · upload these files as they are, '
            f'each into its slot · {_open_btn("Open portal.md", href(table), table.name) if table.is_file() else ""}</p>')
    return (head + '<table class=pb-portal><tr><th>#</th><th>slot</th><th>file</th><th>state</th><th>note</th></tr>'
            + "".join(rows) + '</table>'
            + '<style>.pb-portal{border-collapse:collapse;width:100%;font-size:13px}.pb-portal td,.pb-portal th'
              '{border-top:1px solid var(--line);padding:5px 6px;text-align:left;vertical-align:top}</style>')


def writing_view(board: Path, root: Path, md, items=()) -> str:
    """F · Writing: a numbered section per version; its Sections as card tabs (each panel its step words), then the
    assembled paper."""
    out, n = "", 0
    for job in sorted(d for d in board.glob("j[0-9]*_*") if d.is_dir() and is_version(d)):
        tasks = sorted(d for d in job.glob("t[0-9]*_*") if d.is_dir())
        paper = _paper_files(board / "delivery" / job.name, root, f"pp{n}")
        n += 1
        word, waits = sections_word(tasks, root)
        out += _section(f"{n} · ✍️ {job.name}", f'<div class=pb-verbs>{_open_btn("Open the version", _version_url(job, root, "report"))}</div>'
                        + (section_tabs(tasks, root, f"wr{n}") if tasks else '<p class=mut>No Sections yet.</p>'), word, waits)
        if paper:
            n += 1
            out += _section(f"{n} · 📄 The assembled paper", paper, paper_word(board / "delivery" / job.name))
        portal = _portal(board / "delivery" / job.name, root)
        if portal:
            n += 1
            out += _section(f"{n} · 📮 Ready for the portal", portal, portal_word(board / "delivery" / job.name))
    # every section starts closed (JL 261104: "this should be closed at the begining"); focus_draft's fold reads the mark
    return '<i data-fd-closed hidden></i>' + out if out else '<p class=mut>No version yet.</p>'


def section_tabs(tasks: list, root: Path, eid: str, words: dict | None = None) -> str:
    """Each Section's text to read, one side tab per Section (its name, its next step), its sentences on the right with
    its Open button in the corner: the Board's Writing and a version's Draft views draw the same tabs (JL 261106).
    `words` {Section: its word} names each tab's word instead (a revision: what this send did to it; a Report: how
    much text it has); a tab is never left without one (r03: the Cover letter tab had none)."""
    from live.focus_draft import text_count
    secs = [(_cap(re.sub(r"^t\d+_", "", t.name).replace("-", " ")), _state_words(_section_state(t, root))) for t in tasks]
    if words is not None:
        secs = [(h, words.get(t) or w) for (h, w), t in zip(secs, tasks)]
    elif len({w for _, w in secs}) == 1:        # the same step on every tab says nothing: how much text each has
        secs = [(h, text_count(t)) for (h, _), t in zip(secs, tasks)]
    panels = [f'<div class=pb-corner>{_open_btn("Open the Section", _task_url(t, root), t.name)}</div>' + _section_read(t, root) for t in tasks]
    return _side_tabs(eid, secs, panels)


def text_word(tasks: list) -> str:
    """How many of these Sections have text to read (their adopted Content)."""
    if not tasks:
        return "nothing yet"
    have = sum(any(t for _, _, t in paragraphs(x)) for x in tasks)
    return f"{have} of {len(tasks)} with text"          # adopted text, not the Write step's word (r02: "4 of 4 written"
                                                        # stood beside Write: later)


def sections_word(tasks: list, root: Path) -> tuple:
    """(state word, waiting line) of a version's Sections: how many wait for you and the first of them, else how many
    are done (each Section's own next step, board_read._section_state)."""
    if not tasks:
        return "nothing yet", ""
    states = [(t, _state_words(_section_state(t, root))) for t in tasks]
    you = [(t, w) for t, w in states if "your" in w]
    signs = _waiting_steps(tasks, root)          # every step that waits on you, as many as the sign chips (r02: "1
    if you or signs:                              # waits for you" stood beside two "sign" chips)
        name = _cap(re.sub(r"^t\d+_", "", (you or signs)[0][0].name).replace("-", " "))
        n = max(len(signs), len(you))
        return f'{n} wait{"s" if n == 1 else ""} for you', f"🙋 {name}: {(you or signs)[0][1]}"
    done = sum(w == "done" for _, w in states)
    return f"{done} of {len(states)} done", ""


def _waiting_steps(tasks: list, root: Path) -> list:
    """[(Section, "<step>: waits for …")] of every step of these Sections that waits on the person (sign, asked, send,
    pass), in Section order."""
    from live.focus_draft import STATUS_WHAT, WAITS, WORK, _facts
    out = []
    for t in tasks:
        try:
            f, st, k = _facts(t, root)
        except Exception:
            continue
        out += [(t, f'{step.split(" · ")[1]}: {STATUS_WHAT[st[step]].format(k=k)}') for _, step in WORK if st.get(step) in WAITS]
    return out


def paper_word(vdir: Path) -> str:
    """The assembled paper's word: rebuilding while a build runs, else built (the manifest READY) or a draft."""
    import json
    if build_running(vdir):
        return "rebuilding"
    try:
        man = json.loads((vdir / "build-manifest.json").read_text(encoding="utf-8"))
    except Exception:
        return "not built yet"
    return "built" if man.get("status") == "READY" else "draft"


def portal_word(vdir: Path) -> str:
    """The portal packet's word: how many of its upload slots are ready."""
    import json
    try:
        ups = (json.loads((vdir / "build-manifest.json").read_text(encoding="utf-8")).get("portal") or {}).get("uploads") or []
    except Exception:
        return "not built yet"
    return f'{sum(u.get("state") == "ready" for u in ups)} of {len(ups)} ready' if ups else "not built yet"


SHAPED = {"idea": idea_view, "story": story_view, "plan": plan_view}
