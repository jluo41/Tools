"""The classic paper Board page: its four Spaces (Ideation, Story, Sections, Delivery), their Runs panels, and render_paper.
Moved from paper.py, which re-exports every name here so `from live.paper import render_paper` keeps working."""
import re
from pathlib import Path

from host_paths import skill_dir
from src.outline_version import latest_outline, plan_dir, version_tag

from live.paper import (TASK_STEM, _addresses, _card, _col, _fields, _hero_cards, _idea_card, _kv, _link, _norm_key,
                        _row_ids, _row_key, _status_cls, clean, collect, current_stories, esc, inline, outline_url,
                        paper_desk, part_of, prose, read, scalar, session_rows, task_num)
from live.paper_pages import _PAGE
from live.paper_related import logic_work_html, related_html, roadmap_html
from live.paper_run_view import run_result_url
from live.paper_story_tree import story_tree


# ---------------------------------------------------------------- render
# The Page workbench's grammar (JL 260927; the drawing is
# Tools/blueprints/Project-Ladder/work/b16_theme_paper/_archive/20261010/s02-paper-workbench/paper-workbench-design.excalidraw): four Spaces,
# each with its tabs and views, the content on the left and its own Runs panel on
# the right. Nothing on screen explains itself: no source lines, counts or hints.
SPACES = (("ideation", "Ideation"), ("story", "Story"),               # plain names, as every
          ("sections", "Sections"), ("delivery", "Delivery"))          # workbench's (JL 261003)
STORY_TABS = (("spine", "Spine"), ("roadmap-draw", "RoadMap Draw"),                           # JL 260930
              ("logic-work", "High-level logic + Low-level work"),                        # JL 260929
              ("related", "Related Papers"))                                             # JL 260930
SECTION_TABS = (("main", "Main"), ("appendix", "Appendix"))
SECTION_VIEWS = (("table", "Table"), ("narrative", "Narrative"), ("evidence", "Evidence"))
DELIVERY_TABS = (("latex", "LaTeX"), ("word", "Word"), ("cover", "Cover letter"), ("rounds", "Rounds"))
DELIVERY_VIEWS = (("preview", "Preview"), ("artifacts", "Artifacts"), ("checks", "Checks"))

_CARDS = skill_dir("haipipe-paper-workflow") / "ref" / "run-cards.md"
_BUTTON = re.compile(r"^🔘 BUTTON\s+(?P<label>.+?)\s+·\s+(?P<space>[A-Z][^·]*?)\s+·\s+"
                     r"(?P<pattern>\S.*?)(?:\s+·\s+views\s+(?P<views>[\w -]+?))?\s*$")
_PROMPT = re.compile(r"^💬 PROMPT\s+(?P<prompt>.+?)\s*$")


def paper_run_types(path=_CARDS):
    """The paper's Run cards → {space: [{label, run, pattern, views, prompt, skills}]} in
    card order. Each button takes the first `💬 PROMPT` after it and the `🧩 SKILL`
    line before that prompt, and its `🏷 RUN` line, the Run it makes (b16 Q05); pattern `-`
    means the button only copies a prompt (its runs live with another owner)."""
    out, pending = {}, []
    for line in read(path).splitlines():
        m = _BUTTON.match(line)
        if m:
            t = {"label": m["label"], "space": m["space"].lower(), "pattern": m["pattern"].strip(),
                 "views": " ".join((m["views"] or "").split()), "prompt": "", "skills": [], "run": ""}
            out.setdefault(t["space"], []).append(t)
            pending.append(t)
            continue
        m = re.match(r"^🏷 RUN\s+(.+?)\s*$", line)
        if m and pending:
            pending[-1]["run"] = m.group(1)
            continue
        m = re.match(r"^🧩 SKILL\s+(.+?)\s*$", line)
        if m:
            for t in pending:
                t["skills"] = [s.strip() for s in m.group(1).split("·") if s.strip()]
            continue
        m = _PROMPT.match(line)
        if m:
            for t in pending:
                t["prompt"] = m["prompt"]
            pending = []
    return out


def _page_runs(d, page):
    """One Page's runs as the Page workbench reads them (live.runs.local_runs)."""
    if not page or not page.get("rel"):
        return []
    from live.runs import local_runs
    try:
        return local_runs(d["board"] / page["rel"])
    except Exception:  # noqa: BLE001  a broken ticket must not blank a Space
        return []


def _bucket(kinds, rows, place):
    """rows → one list per run type. A row goes to the type whose ticket pattern
    matches; `place(row)` names a type for rows no pattern takes (or None)."""
    from live.runs_panel import _number, _ticket_name
    buckets = [[] for _ in kinds]
    for row in sorted(rows, key=_number, reverse=True):
        name = _ticket_name(row)
        hit = next((i for i, k in enumerate(kinds)
                    if k["pattern"] != "-" and re.search(k["pattern"], name)), None)
        if hit is None:
            label = place(row)
            hit = next((i for i, k in enumerate(kinds) if k["label"] == label), None)
        if hit is not None:
            buckets[hit].append(row)
    return buckets


def _panel(d, space, kinds, buckets, fill, whole):
    from live.runs_panel import panel_markup
    return panel_markup(space, kinds, buckets, base=Path(d["root"]),
                        fill=lambda row: row.get("_fill") or fill, whole=whole, folded=True)


def _tag(rows, keys=(), fill=None):
    """Mark rows for the paper's panels: selection keys, no format filter, prompt fill."""
    out = []
    for row in rows:
        row = dict(row)
        row["_keys"] = " ".join(k for k in list(keys) + row.get("_keys", "").split() if k)
        row["_views"] = ""
        if fill:
            row["_fill"] = fill
        out.append(row)
    return out


def _ideation_panel(d, kinds):
    page = d["story00"]
    fill = {"page": page["stem"] if page else "Story00", "paper": d["board"].name}
    rows = []
    for row in _page_runs(d, page):
        rows += _tag([row], [_norm_key("i", row.get("target"))], fill)
    return _panel(d, "ideation", kinds, _bucket(kinds, rows, lambda r: None), fill, "every idea")


def _claim_rq(s):
    """Claim number → the RQs its row names."""
    irq = _col(s["e_h"], ("rq", "question"), 1)
    out = {}
    for c in s["e"]:
        m = re.match(r"E-?\d+", c[0])
        if m:
            out[_norm_key("E", m.group(0))] = [x for x in _row_ids(c[irq] if len(c) > irq else "") if x.startswith("RQ")]
    return out


def _supporting_rows(d, s, fill, T):
    """The Task and Discovery runs this paper's Evidence Items cite, as run rows
    keyed by the Task and Discovery Roadmap rows whose addresses cover them, and by every claim and
    RQ above those rows, so selecting a question shows the runs behind it."""
    q_of = {_row_key(c[0]): _q_of(s["tt_h"], c) for c in s["tt"]}
    q_of.update({_row_key(c[0]): _q_of(s["dd_h"], c) for c in s["dd"]})
    covers = [(_row_key(c[0]), _addresses(" ".join(c))) for c in s["tt"] + s["dd"]]
    rows = []
    for owner in ("Execution", "Discovery"):
        for node in d["supporting"][owner].values():
            for jnode in node["jobs"].values():
                for tnode in jnode["tasks"].values():
                    for r in tnode["runs"]:
                        dotted = ".".join(re.findall(r"[bjtr]\d{2}", r["addr"]))
                        ticket = r["tickets"][0][1] if r["tickets"] else None
                        keys = [row for row, addrs in covers if any(r["addr"].startswith(a) for a in addrs)]
                        keys += sorted({q_of[k] for k in keys if q_of.get(k)}) + [u for k in keys for u in T["up"].get(k, [])]
                        users = sorted({u["page"] + " " + u["item"].split("-")[0] for u in r["users"]})
                        st = (r["status"] or "").lower()
                        task = tnode.get("task")
                        home = Path(task["dir"]) if task and task.get("dir") else None
                        stem = r["tickets"][0][0] if r["tickets"] else ""
                        # its card opens the run's results in the pop-out (JL 260930)
                        opens = home is not None and ((home / "results").is_dir() or (home / "runs" / stem / "result").is_dir()) \
                            and d.get("root") is not None
                        rows.append({"run_id": dotted, "global_id": dotted, "ticket": ticket,
                                     "status": "done" if st in ("complete", "completed", "done") else (st or "unknown"),
                                     "target": owner + " · " + dotted, "goal": "used by " + ", ".join(users),
                                     "result": "", "_display": dotted, "_keys": " ".join(keys),
                                     "result_path": (home / "runs" / stem / "result" if stem and (home / "runs" / stem / "result").is_dir()
                                                     else home / "results" / stem if stem and (home / "results" / stem).is_dir()
                                                     else home / "results") if opens else "",
                                     "_open": run_result_url(d["root"], home, stem) if opens else "",
                                     "_open_name": stem or dotted})
    return _tag(rows, (), fill)


def _story_panel(d, kinds):
    rows = []
    for s in d["story"]:
        fill = {"page": s["stem"], "paper": d["board"].name}
        rq, T = _claim_rq(s), story_tree(s)
        hyp_of = {}                                  # §5 row → the hypotheses it tests
        for q in T["questions"]:
            for h in q["hyps"]:
                for x in h["tests"]:
                    hyp_of.setdefault(x, []).append(h["id"])
        for row in _page_runs(d, s):
            name = str(row.get("run_id") or row.get("global_id") or "")
            target = str(row.get("target") or "")
            if re.search(r"(^|\s)run-paper-claim-", name):
                e = _norm_key("E", target)
                rows += _tag([row], [e] + rq.get(e, []) + hyp_of.get(e, []), fill)
            elif re.search(r"(^|\s)run-paper-task-", name):
                t = _row_key(target)
                rows += _tag([row], [t] + T["up"].get(t, []), fill)
            elif not re.search(r"(^|\s)run-paper-(idea|narrative)-", name):
                rows += _tag([row], [], fill)
        rows += _supporting_rows(d, s, fill, T)
    first = d["story"][0]["stem"] if d["story"] else "the Story"
    fill = {"page": first, "paper": d["board"].name}
    # a supporting run goes under its owner: a Task folder's run or a Discovery folder's run
    buckets = _bucket(kinds, rows, lambda r: "Discovery runs" if str(r.get("target", "")).startswith("Discovery · ")
                      else "Task runs" if str(r.get("target", "")).startswith("Execution · ") else None)
    return _panel(d, "story", kinds, buckets, fill, "the Story")


def _sections_panel(d, kinds, sections):
    from live.runs_panel import _name_by_item, _paper_run_key, _ticket_item, row_space
    from live.space_views import run_tabs
    rows = []
    part = {sec["id"]: sec["part"] for sec in sections}
    for s in d["story"]:
        fill = {"page": s["stem"], "paper": d["board"].name}
        for row in _page_runs(d, s):
            if re.search(r"(^|\s)run-paper-narrative-", str(row.get("run_id") or "")):
                sid = str(row.get("target") or "").strip()
                rows += [dict(x, _views=part.get(sid, "")) for x in _tag([row], [sid], fill)]
    for sec in sections:
        if not sec["page"]:
            continue
        fill = {"page": sec["id"], "paper": d["board"].name}
        page_src = d["board"] / sec["page"]["rel"]
        try:
            served_by = run_tabs(page_src)
        except Exception:  # noqa: BLE001
            served_by = {}
        evidence = []
        for row in _page_runs(d, sec["page"]):
            where = row_space(row)
            keys = [sec["id"]]
            if where == "evidence":
                served = served_by.get(_paper_run_key(str(row.get("run_id") or "")))
                if served:
                    row = dict(row, _served=served)
                item = (served or {}).get("item") or _ticket_item(row)
                if item:
                    keys.append("%s:%s" % (sec["id"], item))
            tagged = _tag([row], keys, fill)[0]
            tagged["target"] = ("%s %s" % (sec["id"], row.get("target") or "")).strip()
            tagged["_views"] = sec["part"]
            tagged["_place"] = {"evidence": "Evidence runs", "delivery": "Delivery runs"}.get(where, "Draft runs")
            (evidence if where == "evidence" else rows).append(tagged)
        _name_by_item(evidence)
        rows += evidence
    fill = {"page": "{target}", "paper": d["board"].name}
    buckets = _bucket(kinds, rows, lambda r: r.get("_place"))
    return _panel(d, "sections", kinds, buckets, fill, "each Section")


# ---- the Spaces --------------------------------------------------------------
def _space(space, main, panel, tabs=(), views=(), noviews=()):
    """One Space: its tabs and views over the content, its Runs panel beside it."""
    tab_row = ('<div class="space-tabs">%s</div>' % "".join(
        '<button type=button class="space-tab%s" data-tab="%s" data-label="%s"%s>%s</button>'
        % (" on" if i == 0 else "", k, esc(label), " data-noviews" if k in noviews else "", esc(label))
        for i, (k, label) in enumerate(tabs))) if tabs else ""
    view_row = ('<div class="space-views"><span class="space-views-label">View</span>%s</div>' % "".join(
        '<button type=button class="space-view%s" data-view="%s">%s</button>' % (" on" if i == 0 else "", k, esc(label))
        for i, (k, label) in enumerate(views))) if views else ""
    return ('<div class="panel space-split" data-space="%s"><div class="space-main">%s%s%s</div>%s</div>'
            % (space, tab_row, view_row, main, panel))


def _pane(html_, tab="", view=""):
    return '<div class="space-pane"%s%s>%s</div>' % (
        (' data-tab="%s"' % tab) if tab else "", (' data-view="%s"' % view) if view else "", html_)


def _cards(cards, empty):
    return '<div class="item-cards">%s</div>' % "".join(cards) if cards else '<div class="space-empty">%s</div>' % esc(empty)


def render_ideation(d, kinds):
    i = d["ideation"]
    if not i["present"]:
        main = _pane('<div class="space-empty">No Story00-ideation page yet.</div>')
    else:
        main = _pane(_cards([_idea_card(d, i, x) for x in i["ideas"]], "No idea yet."))
    return _space("ideation", main, _ideation_panel(d, kinds))


def _spine_html(d):
    out = []
    many = sum(1 for s in d["story"] if re.match(r"^Story[A-Z]", s["stem"])) > 1
    for s in d["story"]:
        if many:
            out.append('<h3 class="story-name">%s</h3>' % esc(s["stem"]))
        for n, title, (face, subs, paras) in s["spine"]:
            rows = [(k, inline(v)) for k, v in face]
            if paras:
                rows.append(("", prose(paras)))
            rows += [(sub, prose(pg)) for sub, pg in subs if pg]
            out.append('<div class="card spine-card" data-key="C%d"><h2>%s<span class="tally">%s</span></h2>%s</div>'
                       % (n, esc(title), _link(d, s["rel"], "Open ↗", focus="C%d" % n),
                          _kv(rows, "spine-row") or '<div class="space-empty">Empty.</div>'))
    return "".join(out) or '<div class="space-empty">No Story yet.</div>'


def _q_of(headers, row):
    """The general question a T or D row names in its `Q` column ('' when none)."""
    i = next((k for k, h in enumerate(headers) if h.strip().upper() == "Q"), None)
    return row[i].strip() if i is not None and i < len(row) else ""


def render_story(d, kinds):
    if not d["story"]:
        empty = '<div class="space-empty">No Story yet.</div>'
        return _space("story", "".join(_pane(empty, k) for k, _ in STORY_TABS), _story_panel(d, kinds), STORY_TABS)
    main = (_pane(_spine_html(d), "spine") + _pane(roadmap_html(d), "roadmap-draw")
            + _pane(logic_work_html(d), "logic-work") + _pane(related_html(d), "related"))
    return _space("story", main, _story_panel(d, kinds), STORY_TABS)


def section_rows(d):
    """Every Section of the paper in compile order: the current Story's §8 rows joined to
    their Section Pages, then any Section Page no §8 row names."""
    by_id, heads = {}, {}
    stories = current_stories(d)
    for s in stories:
        for r in s["sections"]:
            by_id.setdefault(r["id"], r)
            heads.setdefault(r["id"], r.get("heads") or s["sec_h"])
    order = next((s["order"] for s in stories if s["order"]), [])
    ids = [x for x in order] + [x for x in by_id if x not in order]
    ids += [p["stem"] for p in d["sections"] if p["stem"] not in ids]
    pages = {p["stem"]: p for p in d["sections"]}
    sessions = {r["stem"]: r for r in d.get("sessions", [])}
    out = []
    for sid in ids:
        page = pages.get(sid)
        page = page if page and page["rel"] else None
        # S-<desk>-<Main|Appendix>-[<N>-]<Title>; a desk may carry a hyphen (JAMA-IM)
        m = re.match(r"^S-.+?-(?:Main|Appendix)-(?:([0-9]+|[A-Z])-)?(.+)$", sid)
        tm = TASK_STEM.match(sid)
        num, name = (((m.group(1) or ""), m.group(2).replace("-", " ")) if m else
                     (task_num(sid), tm.group(2).replace("-", " ").title()) if tm else ("", sid))
        c8_num = (by_id.get(sid) or {}).get("target", "")
        if not num and re.fullmatch(r"[0-9]+|[A-Z]", c8_num):
            num = c8_num                    # a record's `(0)`: the Abstract's place in the order
        version = ""
        if page:
            plan = latest_outline(plan_dir((d["board"] / page["rel"]).parent), sid)
            version = version_tag(plan) if plan else ""
        state = clean(scalar(page["text"], "state", "")).split("·")[0].strip() if page else "not set up"
        out.append({"id": sid, "part": part_of(sid), "num": num,
                    "name": name, "page": page, "version": version, "state": state,
                    "row": by_id.get(sid), "heads": heads.get(sid, []), "session": sessions.get(sid)})
    return out


def _state_word(state):
    """`🟡 PARTIAL - prose inherited, evidence items not landed` → `🟡 Partial`: the state
    word only (JL 261003: "this is too detailed, could we make it light?"); the whole
    line stays in the cell's tooltip."""
    head = re.split(r"\s+[-–—·]\s+|[:,(]", state or "", maxsplit=1)[0].strip()
    m = re.match(r"^(\W*?)\s*([A-Za-z][\w ]*)$", head)
    return ("%s %s" % (m.group(1), m.group(2).strip().capitalize())).strip() if m else head


def _section_table(d, rows):
    out = []
    for r in rows:
        opener = ('<a class="sec-open" href="%s">Open ↗</a>' % esc(outline_url(d["path"], r["page"]["rel"]))
                  if r["page"] else "")
        out.append('<div class="sec-row" data-key="%s" tabindex="0" title="%s"><span class="sec-num">%s</span>'
                   '<span class="sec-name">%s</span><span class="sec-ver">%s</span>'
                   '<span class="sec-state %s" title="%s">%s</span>%s</div>'
                   % (esc(r["id"]), esc(r["id"]), esc(r["num"]), esc(r["name"]), esc(r["version"]),
                      _status_cls(r["state"]) if r["page"] else "warn", esc(r["state"]),
                      esc(_state_word(r["state"])), opener))
    return '<div class="sec-list">%s</div>' % "".join(out) if out else '<div class="space-empty">No Section yet.</div>'


def _narrative_cards(d, rows):
    cards = []
    for r in rows:
        c8 = r["row"]
        fields = _fields(r["heads"], c8["cells"], {0, 1}) if c8 else []
        if r["session"]:
            sess = r["session"]
            if not sess["pair"]:                # a Claude session with no Codex pair yet
                fields.append(("Session", esc(sess["state"])))
            else:
                fields.append(("Session", '<code>%s</code>%s' % (esc(sess["pair"]), "" if sess["state"].startswith("no ")
                                                                  else " · " + esc(sess["state"]))))
        label = (c8["question"] if c8 and c8["question"] else r["name"])
        cards.append(_card("section-" + r["id"], r["num"] or "·", label, esc("%s %s" % (r["num"], r["name"])).strip(),
                           "", r["state"], _status_cls(r["state"]) if r["page"] else "warn", fields, key=r["id"]))
    return cards


def render_sections(d, kinds):
    rows = section_rows(d)
    main = ""
    for tab, _ in SECTION_TABS:
        mine = [r for r in rows if r["part"] == tab]
        hero = [c for c in _hero_cards(d) if ('data-part="%s"' % tab) in c]
        main += (_pane(_section_table(d, mine), tab, "table")
                 + _pane(_cards(_narrative_cards(d, mine), "No Section yet."), tab, "narrative")
                 + _pane(_cards(hero, "No Display or Value yet."), tab, "evidence"))
    return _space("sections", main, _sections_panel(d, kinds, rows), SECTION_TABS, SECTION_VIEWS)


def _shell_band(d):
    """The band under the title: what this paper is and where it stands, read from its files."""
    cur = current_stories(d)
    texts = {x["stem"]: x["text"] for x in d["stories"]}
    s = texts.get(cur[0]["stem"], "") if cur else (d["stories"][0]["text"] if d["stories"] else "")
    desk = scalar(s, "desk") or paper_desk(d)
    version = scalar(s, "story-version") or scalar(s, "version")
    questions = len(cur[0]["qb"]) if cur else 0
    sections = section_rows(d)
    built = (d.get("delivery") or {}).get("built") or ""
    parts = [desk, "Story %s" % version if version else "no Story yet" if not d["story"] else "",
             "%d questions" % questions if questions else "",
             "%d Sections" % len(sections) if sections else "",
             "built %s" % built if built else ""]
    return " · ".join(x for x in parts if x)


def render_paper(board, root, path_param):
    from live.runs_panel import PANEL_CSS, PANEL_JS
    from live.space_views import SPACE_CSS
    from live.work_items import WORK_ITEM_CSS
    from live.paper_spaces_delivery import render_delivery      # at call time: that module imports this one at its top
    d = collect(board, path_param)
    d["root"] = Path(root).resolve()
    d["sessions"] = session_rows(d)          # needs root for the pair lookup
    kinds = paper_run_types()
    chips = "".join('<button type=button class="space" data-space="%s">%s</button>' % (k, l) for k, l in SPACES)
    panels = (render_ideation(d, kinds.get("ideation", [])) + render_story(d, kinds.get("story", []))
              + render_sections(d, kinds.get("sections", [])) + render_delivery(d, kinds.get("delivery", [])))
    default = "story" if d["story"] else "ideation"
    document = _PAGE.format(title=esc(d["title"]), space_chips=chips, panels=panels, default_space=default,
                        band=esc(_shell_band(d)),
                        space_css=SPACE_CSS, panel_css=PANEL_CSS, panel_js=PANEL_JS, work_item_css=WORK_ITEM_CSS,
                        paper_id=esc(d["board"].name))
    from live.workbench_guide import mount_guide
    return mount_guide(document, "paper", {"path": path_param, "file": "board.md"},
                       ".spaces", ".panel[data-space]")
