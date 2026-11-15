"""A paper Board's RESULTS band, the same on Report and Work: the Idea, Story, Plan, Explore, Evidence and Displays
views in the shape settled in b16 s32 (numbered bars, the main point large, side tabs, the flow map, folder trees),
and the drawing and mind-map helpers under them. Writing is board_writing's; the Story, Related, canvas and display
parts live in board_story, board_related, board_canvas and board_displays, and the names callers still import from
here are re-exported below."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

from live import draft_steps as ds
from live.frame import esc
from live.ui_parts import _bar, _cap, _plain, _section, _when, plural_word
from live.board_read import view_topics, _face, _field, _folder_line, _rq_lists, _table, explore_tree
from live.board_evidence import evidence_body  # noqa: F401  (callers import it from here)
# moved out by part of the page; the names callers still import from here
from live.board_story import (RQ_TABLE_CSS, _story_arc, _section_rows, _narrative, _direction_theory, _no_theory,  # noqa: F401
                              idea_tabs, story_tabs)
from live.board_related import related_section  # noqa: F401
from live.board_canvas import _canvas, _topic_canvas, _display_examples  # noqa: F401
from live.board_displays import _evidence_kinds, _display_head, GROUP_ORDER, display_tabs, display_groups  # noqa: F401
from live.board_writing import (_section_read, _tab_flag, _paper_files, _fold_earlier, _portal, writing_view,  # noqa: F401
                                section_tabs, text_word, sections_word, portal_word)


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
    return "written" if (text or "").strip() else ""   # an empty bar shows no word (AGENTS § Page words)


def _rq_word(rq: str) -> str:
    """The Research Questions' bar word: none. Each question shows its own state after its question mark; a count of
    the open ones is a progress tally, which a page never carries (AGENTS § Page words)."""
    return ""


def _after_rule(helpers: str) -> str:
    """The helpers after the view's one dashed rule (board_views.banded splits the view there)."""
    return "<hr class=pb-rule>" + helpers


# a mind map draws its curves only when on screen, so a section opening redraws them
REDRAW = ("<script>document.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('.fd-h')"
          "&&window.pmDraw)setTimeout(window.pmDraw,30);});</script>")


def idea_view(board: Path, root: Path, md, items=(), *, studio=True) -> str:
    """A · Idea, its own button, for the many directions (JL 261105: "I mean seperate this!!!"; "idea for multiple direction,
    story for one direction"; s32-D44): its Studio, every direction weighed, left tabs, then each one's Theory. The chosen one's words are the
    Story's, unless there is no Story yet. The page adds 🙋 Interaction."""
    out, n = "", 0
    has_story = bool(view_topics(board, "story"))
    for _, _, topic in view_topics(board, "idea"):
        stage = _stage(topic)
        if studio:
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
    out += related_section(board, root, n)[0]            # the same references inform both candidate ideas and the Story
    return out


def story_view(board: Path, root: Path, md, items=(), *, studio=True) -> str:
    """B · Story, its own button, for the one direction chosen (JL 261105: "story for one direction"; s32-D44): its Studio,
    Direction, Pitch, Theory, Research Questions, Related, Venues, Story by Section. The page adds 🙋 Interaction."""
    out, n = "", 0
    for _, _, topic in view_topics(board, "story"):
        stage = _stage(topic) or "written"
        if studio:
            out += _bar(None, "🎨 Studio", _studio_panel(topic, root) + REDRAW, stage)
        tabs = {h: (w, p) for h, w, p in story_tabs(board, topic, root, md)}
        parts = _face(topic)[1]
        def flush(html):
            """A Story part written as Markdown starts at the bar's left edge, as the Research Questions do, its words
            at the reading measure and a compared table the card's full width, styled as the RQ table (Paper-CMS-AI-Usage
            261114: "one page has two left edges and two widths")."""
            return (RQ_TABLE_CSS + "<style>.pb-prose>p,.pb-prose>ul,.pb-prose>ol{max-width:880px;margin:0 0 10px}.pb-prose .pb-rqtab td:first-child,.pb-prose .pb-rqtab th:first-child{width:auto}</style>"
                    + '<div class=pb-prose>' + re.sub(r"<table(?=[\s>])(?![^>]*class=)", "<table class=pb-rqtab", html) + '</div>')

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
        bar("🎓", "Theory", flush(md(whole or said, topic)) if whole or said else _no_theory(
            board, "a <code>**Theory**:</code> line in the Story's Identity (haipipe-paper-story)."), _written(whole or said))
        if "Research Questions" in tabs:
            bar("❓", "Research Questions", tabs["Research Questions"][1], _rq_word(parts.get("research questions", "")))
        # no Stakes and evidence section: the RQ table's Why we ask column says why each question matters, and the
        # Story's §4 and §5 stay in its file (JL 261111: "should we delete the Stakes and Evidence, no information from it")
        related, n = related_section(board, root, n)
        out += related
        from live.paper_reading import reading_list      # § 6 is the Story's: what the paper must read (JL 261111)
        reading, rword = reading_list(board)
        if reading:
            n += 1
            out += with_prompts(_named(n, "📚", "Reading", reading, rword), _prompts_for(board, root, "Reading")) + HP_CSS + HP_JS
        if "Venues" in tabs:
            venues = _table(parts.get("venues", ""))
            bar("🏛️", "Venues", tabs["Venues"][1], f'target {_plain(venues[0].get("venue", ""))}' if venues else "written")
        if "Story by Section" in tabs:
            bar("🧠", "Story by Section", tabs["Story by Section"][1], stage)
    return out


def _plan_part(board: Path, topic: Path, root: Path) -> tuple:
    """(body, word) of a Plan part: its topic's Excalidraw drawing, the way Displays › Plan shows s06 (JL 261111: "for
    the dataflow, it should have a draw as well, right?"; JL 261102: "excalidraw only"). The HTML flow map and the
    s04 mind map left: the drawings carry the same content, read in board.md's order and names."""
    drawing = _topic_canvas(board, root, re.sub(r"^s\d+-", "", topic.name))
    return (drawing or '<p class=mut>No drawing yet.</p>'), ((_stage(topic) or "drawn") if drawing else "no drawing yet")


# Which plan prompts sit on which section's bar (JL 261111, Paper-CMS-AI-Usage r03_collect_plan_view_decisions: "each
# section's prompts become a small button in THAT section's header bar"): the data become each answer on Data flow,
# each answer becomes the page on Paper flow, the reading on the Story's Reading
PROMPT_HOME = {"Design the dataset": "Data flow", "Design the regressions": "Data flow", "Make them run": "Data flow",
               "Plan the displays": "Paper flow", "Plan the reading": "Reading"}


HP_CSS = ("<style>.pb-hbtn{margin-left:10px;font-size:12px;font-weight:500;border:1px solid var(--line);border-radius:12px;"
          "padding:1px 10px;background:var(--paper);color:var(--ink);cursor:pointer;vertical-align:1px}"
          ".pb-hbtn:hover{border-color:var(--accent)}.pb-hp{margin:0 0 12px}</style>")


HP_JS = ("<script>document.addEventListener('click',function(e){var b=e.target.closest('.pb-hbtn');if(!b)return;"
         "e.preventDefault();e.stopPropagation();var s=b.closest('section');var hp=s&&s.querySelector('.pb-hp');if(!hp)return;"
         "hp.hidden=!hp.hidden;var d=b.closest('details');if(d&&!d.open)d.open=true;"
         "if(!hp.hidden&&!hp.offsetParent){var h=s.querySelector('h3.fd-h');if(h)h.click();}},true);</script>")


def _prompts_for(board: Path, root: Path, home: str) -> str:
    """The plan prompts whose home is this section, as the Copy-prompt boxes the Plan center drew (board_process)."""
    from live.board_process import _plan_steps, behind_copy
    from live.ui_parts import _plan_html
    steps = [st for st in _plan_steps(board, root) if PROMPT_HOME.get(re.sub(r"^\W+\s*", "", st[0])) == home]
    if not steps:
        return ""
    session = _field((board / "board.md").read_text(encoding="utf-8", errors="ignore"), "session") if (board / "board.md").is_file() else ""
    return behind_copy(_plan_html(steps, session, key=f"plan:{home}:{ds._rel(board, root)}"))


def with_prompts(section: str, prompts: str) -> str:
    """A section whose bar carries a small Prompts button; the prompts open under the bar, the section stays as it is."""
    if not section or not prompts:
        return section
    section = re.sub(r"(<h3 class=fd-h>.*?)(<span class=\"?word|</h3>)", lambda m: m.group(1)
                     + '<button type=button class=pb-hbtn aria-label="Prompts for this section">Prompts</button>' + m.group(2),
                     section, count=1, flags=re.S)
    return section.replace("</h3>", f"</h3><div class=pb-hp hidden>{prompts}</div>", 1)


def plan_view(board: Path, root: Path, md, items=()) -> str:
    """B · Data + Paper Plan, two sections (JL 261111, after re-reading haipipe-paper-plan, Paper-CMS-AI-Usage
    r03_collect_plan_view_decisions: "okay, go ahead and do it"): 1 · 🗄️ Data flow, the s03 topic (how the data become
    each answer), 2 · 📝 Paper flow, the s04 topic (how each answer becomes the page), each with its own plan prompts on
    its bar. Every fact once: the Story's § 7 Runs show in the Data flow drawing, § 6 reading in the Story view, the
    displays in Displays; no "The plan" summary, no Runs to do, no separate Plan prompts."""
    from live.paper_reading import drop_slots
    parts = view_topics(board, "plan")
    icon = {"Data flow": "🗄️", "Paper flow": "📝"}                       # every section has its emoji (JL 261105)
    maps = "".join(with_prompts(_named(n, icon.get(name, "📌"), name, *_plan_part(board, topic, root)),
                                _prompts_for(board, root, name))
                   for n, (_, name, topic) in enumerate(parts, 1))
    return drop_slots(HP_CSS + f'<div class=pb-canvas>{maps}</div>' + HP_JS
                      + _after_rule("".join(_helpers(topic, root, items, mind=False, label=name) for _, name, topic in parts)))


BIB_TITLE = re.compile(r'(?i)(?<![a-z])title\s*=\s*(?:\{((?:[^{}]|\{[^{}]*\})*)\}|"([^"]*)")')   # a .bib entry's title, braces kept inside


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
            if not head:                             # a discovery paper Run: its paper's title, from its .bib
                bib = next(iter(sorted((r / "result").glob("*.bib"))), None)
                bt = bib.read_text(encoding="utf-8", errors="ignore") if bib else ""
                m = BIB_TITLE.search(bt)
                head = re.sub(r"[{}]", "", (m.group(1) or m.group(2) or "") if m else "").strip()
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
            if kind == "discovery":   # a discovery Block named alone shows every Job, Task and paper Run (JL 261108:
                blocks = {b: jobs or {j: set() for j in sorted(b.glob("j[0-9]*_*")) if j.is_dir()}   # "make the discovery
                          for b, jobs in blocks.items()}                                              # runs as complete")
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
    """E · Displays: the plan against the venue's display rules
    (haipipe-paper-plan's display plan, when the Board has one), followed by the displays, one side tab
    per pool Task (Figure 1 (Display A), its type and name), its panel the newest preview.pdf, the display as the paper
    prints it, then how it was made; and all of them as one PDF (build_displays_pdf.py); then Examples; last the
    shared Story by Section, the same section the Story view shows (JL 261109: "this Story by Section should be at the
    bottom"). The plan is the s06 display-plan topic's drawing only; its venue check lines live in that drawing and
    in display_plan.py check. Each display's state is its tab's (the section word counts them), so no separate
    "Where each display stands" list (JL 261109: "maybe we don't need to use it")."""
    out, n = "", 0
    plan = _topic_canvas(board, root, "paper-displays")   # JL 261102: "we might want to have this to be a excalidraw
    if plan:                                              # only. No need to put others" (the venue check stays in s06)
        n += 1
        out += _bar(n, "Plan", plan, _stage(next((t for t in sorted(board.glob("s[0-9]*-paper-displays")) if t.is_dir()), None)) or "drawn")
    body, n = _evidence_kinds(board, root, ("Displays",), n)
    story = ""                                            # last: the Story view's own section, the same panel
    for _, _, topic in view_topics(board, "story"):
        for name, _, panel in story_tabs(board, topic, root, md):
            if name == "Story by Section":
                story += _named(n + (2 if plan or body else 1), "🧠", name, panel, _stage(topic) or "written")
    if not (plan or body):
        return story or '<p class=mut>No display Job or display plan yet.</p>'
    # JL 261102: "after the display, could you add a new section named 3. Examples"; JL 261103: "we can add the things
    # like 3-Examples": it always shows, saying how to fill it while it is empty. Its questions are the page's 🙋 Interaction.
    n += 1
    examples = _display_examples(board, root)
    body += _named(n, "🔍", "Examples", examples or (
        '<p class=mut>No examples yet. The target venue\'s published displays go on one canvas, the Board topic '
        '<code>sNN-paper-display-examples</code> (haipipe-paper-display, Examples).</p>'), "drawn" if examples else "")
    return out + body + story


SHAPED = {"idea": idea_view, "story": story_view, "plan": plan_view}
