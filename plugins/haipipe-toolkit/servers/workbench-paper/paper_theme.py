"""The paper theme on the base frame (servers/workbench/page/frame.py): only what differs from vanilla.

A paper Board climbs the ladder as Tools/blueprints/Project-Ladder/work/b16_theme_paper proposes (Q01, s11-paper-block): the
Board is one paper; its versions are Jobs and its Sections are Page Tasks once those folders exist. Today
a paper Board holds A1-Story/ (Ideation and Story Pages) and Ba-/Bb- Section groups, so this theme fills
the Block tab only, from today's folders, with paper.py's own content (JL: carry over what exists) drawn in
the base's look only (JL 261007: no theme stylesheet): wf-table, the folding .topic row, the lw-/bj- work rows.

    Description      Scope · Venue · Resources · Related     (Related: paper cards, drawing from the deep read)
    Idea Studio      the base's studio rows; the RoadMap drawings are rows   (was Story › RoadMap Draw)
    Audience Report  Ideation · Narrative · High-level logic + Low-level work · Related Questions · Related
                     Papers (by the question each bears on, JL 261009): questions
                     (JL 261007); Narrative = what the story says, how it is drawn and told, will it attract
    Work Details     Idea · Story · DataFlow · PaperFlow · Jobs   (each Operation over Result; Jobs: the versions)
    Runs             vanilla (runs/), with the paper's run types
    Delivery         LaTeX · Word · Cover letter · Rounds     (was Delivery)

A Job is a version (s12: one send, jNN_v<N>_<desk>/, or today's Ba-/Bb-/Bc-<desk>-<part> group) or the
A1-Story/ group of an older Board (the Story is studio topics and Questions on the ladder, b16 Q04); a Task is a Section (S-…), a review batch (RD<NN> · CM<NN>) or a
Story Page. Both layouts read the same (b16 g03). The old Board page (/_board/paper-board) stays, linked from
the band, until this replaces it. Read-only: nothing here writes; a run type only copies its prompt.
"""
from __future__ import annotations

import re
from pathlib import Path

from live import paper as P
from live.frame import _file_url
from live.frame import Space, Theme, esc, face, link, reader, rel, studio_cards, table, vanilla


def _kinds(group: str, views=None) -> tuple:
    """The paper's run cards of one Space key (`block › audience report`), as Runs-panel kinds; `views` keeps
    the cards meant for those views (a card with no views belongs to all of them)."""
    out = []
    for k in P.paper_run_types().get(group, []):
        if views and k["views"] and not set(k["views"].split()) & set(views):
            continue
        prompt = k["prompt"].replace("{page}", "{folder}/board.md").replace("{target}", "<target>")
        if k.get("run"):                           # named by the Run it makes, what it does under it (as the frame's)
            out.append({"label": k["run"], "doing": k["label"], "prompt": prompt, "skills": k["skills"]})
        else:
            out.append({"label": k["label"], "prompt": prompt, "skills": k["skills"]})
    return tuple(out)


def _slug(view: str) -> str:
    """A third-row view's name as a card's `views` word: Draft-Main → draft-main; the research questions'
    long name is logic-work."""
    return "logic-work" if view.startswith("High-level logic") else re.sub(r"[^a-z0-9]+", "-", view.lower()).strip("-")


def _run_cards(level: str, space: str, view: str | None = None) -> tuple:
    """The run cards of one level's Space (haipipe-paper-workflow/ref/run-cards.md, `<Level> › <Space>`, b16
    Q05), keeping those meant for `view`; a card with no views shows in every view of its Space."""
    return _kinds(f"{level} › {space}".lower(), (_slug(view),) if view else None)


def _data(block: Path, root: Path, version: Path | None = None) -> dict:
    """What paper.py's Spaces read, collected once for this Board, as its own page does; `version` reads that
    version's Section Narrative where the Story is studio topics (b16 Q04)."""
    d = P.collect(block, rel(block / "board.md", root), version=version)
    d["root"] = root
    d["sessions"] = P.session_rows(d)
    return d


# ── the old paper page's look (JL 261007: "how did we do the UI previously … that was much better"): its own
# stylesheet, read from paper.py's page, scoped to `.pv` so it styles only the paper's views on the frame
_PAGE_CHROME = (".spaces", ".space-tabs", ".space-views", ".panel", ".runs-", ".rr-", ".split", "h1")


def _scope(css: str) -> str:
    out, i = [], 0
    while i < len(css):
        j = css.find("{", i)
        if j < 0:
            break
        head = css[i:j].strip()
        if head.startswith("@media"):                       # a block of rules: scope what is inside
            depth, k = 1, j + 1
            while depth and k < len(css):
                depth += {"{": 1, "}": -1}.get(css[k], 0)
                k += 1
            out.append(head + "{" + _scope(css[j + 1:k - 1]) + "}")
            i = k
            continue
        k = css.find("}", j)
        body = css[j:k + 1]
        sels = []
        for sel in head.split(","):
            sel = sel.strip()
            if not sel or any(sel.startswith(c) for c in _PAGE_CHROME) or sel.startswith("body"):
                continue
            sels.append(".pv" if sel in (":root", "html") else ".pv " + sel)
        if sels:
            out.append(",".join(sels) + body)
        i = k + 1
    return "".join(out)


def _old_css() -> str:
    page = P._PAGE
    css = page[page.index("<style>") + 7:page.index("</style>")].replace("{{", "{").replace("}}", "}")
    return _scope(re.sub(r"(?s)/\*.*?\*/", "", css))             # a comment's commas would split a selector


PV_CSS = _old_css()


_OLD_LINK = re.compile(r'href="/_board/draft\?path=([^&"]+)&amp;file=([^&"]+)(?:&amp;[^"]*)?"')
_TASK_DIR = re.compile(r"^(t\d{2}_|S-|RD\d|CM\d)")


def _frame_links(html: str) -> str:
    """The old page's links into its Page view (/_board/draft) point at the frame instead (JL 261008: "why we
    are back to the old version now???"): a Section, Abstract or letter opens its own tab, anything else opens
    in the reader."""
    from urllib.parse import quote, unquote
    from live.frame import ROUTE

    def fix(m):
        board = Path(unquote(m.group(1))).parent
        file = Path(unquote(m.group(2)))
        target = board / file
        if _TASK_DIR.match(file.parent.name):
            return f'href="{ROUTE}?path={quote(str(target.parent), safe="")}&amp;theme=paper"'
        return f'href="/_board/page?path={quote("/" + str(target), safe="")}"'
    return _OLD_LINK.sub(fix, html)


# The old page's own script filled its frames; a view drawn by pv() in the frame needs the same two rules
# (JL 261009: a related paper's card opened on an empty box): a related paper's PDF (data-pdf) loads when its
# card opens, any other old frame (data-src: RoadMap Draw, a delivery preview) once it is shown.
PV_JS = """<script>(function(){if(window.pvFill)return;
function fill(r){r.querySelectorAll('iframe[data-src]:not([src])').forEach(function(f){
 var d=f.parentElement.closest('details');if(!d||d.open)f.setAttribute('src',f.dataset.src);});}
window.pvFill=fill;function all(){document.querySelectorAll('.pv').forEach(fill);}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',all);else all();
document.addEventListener('toggle',function(ev){var w=ev.target;if(!(w.matches&&w.open&&w.closest('.pv')))return;
 var f=w.matches('details.rp-card')&&w.querySelector('iframe[data-pdf]');
 if(f&&!f.getAttribute('src'))f.setAttribute('src',f.dataset.pdf);fill(w);},true);})();</script>"""


def pv(html: str) -> str:
    """A view in the old paper page's look, its links into the frame, its frames loading as they did there."""
    return f'<div class=pv><style>{PV_CSS}</style>{_frame_links(html)}{PV_JS}</div>'


def _pick(sub: str, options: tuple) -> str:
    return sub if sub in options else options[0]


OTHER = "Datasets and repos"        # Related's group with no research question (b16 g03 D9)
NOT_PAPERS = ("meeting", "file", "email")    # in related.md but no related work: Related Papers leaves them out (b10 s01-D34, s04-D09)


def _related_rows(d, block):
    """(group, kind, key, title, venue, why, run) per related item: related/related.md when the Board has
    it (b03 s01-D27), else the current Story's related-papers table; run = the deep read it links, or None.
    A row's `group` cell is comma-separated (b10 s04-D07): a paper bearing on two questions is one row per
    question. Its subfolder is the Studio's group (s04-D08), not a question, so it is not read here. A table
    with a `bears on` column groups by it instead (JL 261013: the Studio's groups are the kinds, "things like
    meeting, email, paper", so what a paper bears on moves out of `group`)."""
    table = block / "related" / "related.md"
    rows = []
    if table.is_file():
        heads, body = [], []
        for line in P.read(table).splitlines():
            if not line.startswith("|") or set(line.replace("|", "").strip()) <= set("-: "):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            (body.append(cells) if heads else heads.extend(c.lower() for c in cells))
        get = lambda r, *names: next((r[heads.index(n)] for n in names if n in heads and heads.index(n) < len(r)), "")
        for r in body:
            addr = next(iter(P._addresses(get(r, "read", "discovery"))), "")
            run = P._disc_run(d, addr) if addr else None
            about = get(r, "bears on") if "bears on" in heads else get(r, "group")
            for g in [g.strip() for g in about.split(",") if g.strip()] or [OTHER]:
                rows.append((g, get(r, "kind") or "paper", get(r, "key"), get(r, "paper", "item"),
                             get(r, "venue"), get(r, "why here", "why"), run))
        return rows
    for s in P.current_stories(d):
        for r in s["pp"]:
            h = s["pp_h"]
            addr = next(iter(P._addresses(P._cell(h, r, "discovery") or " ".join(r[1:]))), "")
            run = P._disc_run(d, addr) if addr else None
            m = P.paper_card_data(run) if run is not None else {}
            venue, year = P._short_venue(m.get("venue"))
            who = " ".join(x for x in (P._first_author(m.get("authors")), year) if x)
            title = (who + " · " if who else "") + (m.get("title") or P._cell(h, r, "paper") or r[0])
            rows.append((P._cell(h, r, "question") or OTHER, "paper",
                         "★" if P._cell(h, r, "key") or "key" in P._cell(h, r, "role").lower() else "",
                         title, venue or P._cell(h, r, "venue"), P._cell(h, r, "keep") or P._cell(h, r, "why"), run))
    return rows


def _related(d, block, root, skip=()):
    """Related as paper cards, grouped by `group` (RQn first, then Datasets and repos, then the rest). A card folds;
    opened, it shows the paper's drawing from its deep read, view only (JL 261007, s11-paper-block). skip: the
    kinds left out (Related Papers leaves out meetings, files and emails)."""
    rows = [r for r in _related_rows(d, block) if r[1] not in skip]
    if not rows:
        return '<p class=mut>No related item yet: related/related.md, one row each, any kind.</p>'
    order = lambda g: (0 if g.upper().startswith("RQ") else 1 if g == OTHER else 2, g)
    out = []
    for group in sorted({r[0] for r in rows}, key=order):
        out.append(f"<h3>{esc(group)}</h3>")
        for _, kind, key, title, venue, why, run in (r for r in rows if r[0] == group):
            # the Result's files carry the Run's name: runs/rNN_<slug>/result/ (one folder per Run) or the
            # old results/rNN_<slug>/
            name = (run.parent.name if run.name == "result" else run.name) if run is not None else ""
            drawing = run / f"{name}.excalidraw" if run is not None else None
            # a Result card is no Page Face, so /_board/page refuses it: open it in the Markdown reader
            card = run / f"{name}.md" if run is not None else None
            read = (link(_file_url(card, root),
                         f"read {name.split('_')[0]} ↗")
                    if card is not None and card.is_file() else "no deep read yet")
            head = (f'<span><b>{esc((key + " ") if key else "")}{esc(title)}</b>'           # line 1: who · title
                    + (f' <span class=topic-meta>{esc(venue)}</span>' if venue else "")
                    + f'<br><span class=topic-meta>{esc(kind)} · why here: {esc(why or "—")} · {read}</span></span>')
            if drawing is not None and drawing.is_file():
                url = "/_excalidraw/?" + P.urlencode({"board": rel(drawing, root)})
                head += f'<span class=topic-pop>{link(url, "↗ full size")}</span>'
                body = (f'<iframe class=st-frame title="{esc(title)}" data-src="{esc(url)}" '
                        'referrerpolicy=no-referrer></iframe>')
            elif kind != "paper":
                body = f'<p class="mut none">A {esc(kind)}: no drawing.</p>'
            else:
                body = ('<p class="mut none">⚠ No drawing yet: the paper\'s deep read draws it '
                        '(question → data · method → finding → limits). Run type: Read a paper.</p>')
            missing = kind == "paper" and not (drawing is not None and drawing.is_file())
            out.append(f'<details class="topic{" missing" if missing else ""}"><summary>{head}</summary>{body}</details>')
    return "".join(out)


def _description(d, block, root, sub):
    opts = ("Scope", "Venue", "Resources")              # Related folds inside the Studio (_related_space)
    s = _pick(sub, opts)
    if s == "Scope":
        html = (f'<p class=mut>{esc(P._shell_band(d))}</p>'
                + vanilla("Block", block, root)["Description"].html)
    elif s == "Venue":
        calls = sorted((block / "venues").glob("*/call.md"))
        rows = [(link(reader(c, root), c.parent.name), esc(rel(c, root))) for c in calls]
        html = (table(("venue", "call"), rows) if rows else
                f'<p>Target now: <b>{esc(P.venue_name(d) or "—")}</b> (from the Story).</p>'
                '<p class=mut>No venues/&lt;venue&gt;/call.md yet: one folder per venue the paper writes for '
                '(proposed, b16 Q02).</p>')
    else:
        from live.task_questions import register, words
        res, _ = register(P.read(block / "board.md"), "Related resources", "resources")
        rows = [(link(words(r.get("url")), words(r.get("title"))), esc(", ".join(r.get("questions") or [])))
                for r in res if words(r.get("title"))]
        html = table(("resource", "for"), rows)
    return Space(html=html, subspaces=opts, open=s, run_types=_run_cards("Block", "Description", s))


def _related_space(d, block, root, sub):
    """The Block's Related, folded inside the Studio (b10 s04-D05, was Description › Related): the frame's own
    view, grouped by related/ subfolder, each file previewed (JL 261011: "this is also for the whole workbench
    system"); the paper's buttons. A Board with no related/ yet shows its telling's old P-board cards. The
    cards by research question stay in Report › Related Papers."""
    if not (block / "related").is_dir():
        return Space(html=pv(P.related_html(d)), run_types=_run_cards("Block", "Related"))   # the old Story cards
    return Space(run_types=_run_cards("Block", "Related"))


# ── the paper's views in the base's look (JL 261007: base styles only, no theme stylesheet) ────────
# Same content as paper.py's old page, drawn with what the frame styles for every theme: wf-table
# (table), the folding .topic row, the lw-/bj- work rows (WORK_ITEM_CSS), .space-empty and .mut.
def _fold(title, meta="", body="", pop="", opened=False):
    """One folding row, the frame's .topic: its title and one muted line; opened, its body."""
    return (f'<details class=topic{" open" if opened else ""}><summary><span><b>{title}</b>'
            + (f'<br><span class=topic-meta>{meta}</span>' if meta else "") + "</span>"
            + (f"<span class=topic-pop>{pop}</span>" if pop else "") + f"</summary>{body}</details>")


def _st(ok, text):
    """A status word in the base's colours (.st-ok · .st-warn)."""
    return f'<span class="{"st-ok" if ok else "st-warn"}">{esc(text)}</span>'


def _empty(text):
    return f'<p class="space-empty mut">{esc(text)}</p>'


def _kv(rows):
    """Label and value rows, as the base's table (paper.py's _kv drew its own grid)."""
    return table(("", ""), [(f"<b>{esc(k)}</b>" if k else "", v) for k, v in rows])


def _studio(d, block, root):
    """Idea Studio: the base's studio rows; the Story's RoadMap drawings in studio/ are rows like any topic."""
    return Space(html=studio_cards(block, root), run_types=_run_cards("Block", "Idea Studio"))


# ── On disk (b03's Disk box, JL 261007: "add the disks as well, to show what files are associated with the
# content in the screen"): per Space and per open view, the files that view reads, relative to the open folder
def _rel_to(path, folder):
    import os
    return Path(os.path.relpath(path, folder)).as_posix()


def _section_globs(d, base, part):
    """The folders that hold this part's Sections (today's group, or a version), each as a glob."""
    homes = sorted({(d["board"] / r["page"]["rel"]).parent.parent for r in P.section_rows(d)
                    if r["page"] and r["part"] == part})
    pat = "t2[0-9]_*/" if part == "appendix" else "t[01][0-9]_*/"
    return [(_rel_to(h, base) + ("/" + pat if VERSION_RE.match(h.name) else "/S-*/"),
             f"the {part} Sections, a Page each") for h in homes]


VERSION_RE = re.compile(r"^j\d{2}_(?:writing_)?v")   # j11_writing_v<MMDD>_<desk> since 261031


def _disk_block(d, block, out):
    from dataclasses import replace
    from live.paper_theme_work import BOARD_STEP, _board_topics
    cur = P.current_stories(d)[:1]
    tell = [(str(cur[0]["rel"]), "the telling: identity · pitch · stakes · evidence · discovery · task roadmaps")] \
        if cur and cur[0].get("rel") else []
    idea = [(str(d["story00"]["rel"]), "the ideas, ranked, admitted, eliminated")] if d.get("story00") else []
    reg = [("board.md", "## Questions: the register")]
    rep_ = [("reports/q*/q*.md", "one report per question")]
    ddir = _rel_to(P.delivery_dir(block), block)
    disk = {
        ("Description", "Scope"): [("board.md", "the face: spine · close · Topic")],
        ("Description", "Venue"): [("venues/", "one folder per venue, its call.md")] + tell,
        ("Description", "Resources"): [("board.md", "## Related resources")],
        ("Related", ""): [("related/related.md", "the related items: kind · group · why here · the deep read")]
                         + [(f"related/{x}/", what) for x, what in (("meetings", "a meeting's notes"),
                                                                     ("papers", "open-licensed PDFs"),
                                                                     ("files", "what we were sent"))] + tell,
        ("Idea Studio", ""): [("s[0-9][0-9]-*/", "the topics, beside the Jobs, one row each"),
                              ("studio/", "older topics and loose drawings")],
        ("Audience Report", "Ideation"): idea + reg,
        ("Audience Report", "Narrative"): tell + reg,
        ("Audience Report", "High-level logic + Low-level work"): reg + tell + rep_,
        ("Audience Report", "Related Questions"): reg + rep_,
        ("Audience Report", "Related Papers"): [("related/related.md", "the related items, by question")] + tell + reg,
        ("Work Details", "Jobs"): [("j[0-9][0-9]_*/", "one version each")],
        **{("Work Details", n): [(f"{t.relative_to(block).as_posix()}/", "its drawing and face") for t, _x in
                                 _board_topics(block, BOARD_STEP[n][1], BOARD_STEP[n][2])]
           or [("sNN-*/", "no topic yet")] for n in BOARD_STEP},
        ("Runs", ""): [("runs/", "the Board's Runs")],
        ("Delivery", ""): [(f"{ddir}/paper-build.toml", "the build: order · venue · names"),
                           (f"{ddir}/build-manifest.json", "the checks"),
                           (f"{ddir}/latex/", "generated, never edited"), (f"{ddir}/word/", "generated, never edited")],
    }
    for name, sp in out.items():
        rows = disk.get((name, sp.open)) or disk.get((name, ""))
        if rows:
            out[name] = replace(sp, disk=tuple(rows))
    return out


def _disk_version(d, board, job, out):
    from dataclasses import replace
    face = [(f"{job.name}.md", "the face: send · venue · state · tells · from · answers")]
    disk = {
        ("Description", "Version"): face,
        ("Description", "Venue rules"): [("../venues/", "the venue's call.md")],
        ("Audience Report", "Questions"): [(f"{job.name}.md", "## Questions: the register"),
                                           ("reports/q*/q*.md", "one report per question")],
        ("Audience Report", "Draft-Main"): [(f"{job.name}.md", "## Narrative: the reading order and §8 rows")]
            + _section_globs(d, job, "main"),
        ("Audience Report", "Draft-Appendix"): [(f"{job.name}.md", "## Narrative: the reading order and §8 rows")]
            + _section_globs(d, job, "appendix"),
        ("Audience Report", "Comments"): [("reports/q*/q*.md", "comments reports (page-type: comments)")],
        ("Audience Report", "Cover letter"): [("t3[0-9]_*/", "the letter Tasks"),
                                              ("delivery/paper-build.toml", "[coverletter]")],
        ("Work Details", "Letters"): [("t3[0-9]_*/", "the letter Tasks"), ("reports/q*/q*.md", "the comments they answer")],
        ("Work Details", ""): _section_globs(d, job, "main") + _section_globs(d, job, "appendix"),
        ("Runs", ""): [("runs/", "this version's Runs")],
        ("Delivery", ""): [("delivery/paper-build.toml", "the build: order · venue · names"),
                           ("delivery/build-manifest.json", "the checks"), ("delivery/latex/", "generated, never edited"),
                           ("delivery/word/", "generated, never edited")],
    }
    for name, sp in out.items():
        rows = disk.get((name, sp.open)) or disk.get((name, ""))
        if rows:
            out[name] = replace(sp, disk=tuple(rows))
    return out


def spaces(level, folder, root, sub):
    from live.paper_theme_version import _delivery, version_spaces
    from live.paper_theme_report import _report
    from live.paper_theme_section import section_spaces
    from live.paper_theme_work import _board_work, story_spaces
    folder, root = Path(folder).resolve(), Path(root).resolve()
    if level == "Task" and P.is_section(folder.name):   # a Section is a Page Task (S-… or t00-t29): the base's Page views
        return section_spaces(folder, root, sub)    # (b16 s13), with the paper's own lines (◆) over them
    if level == "Task":                             # a review batch (RD<NN> · CM<NN>) or a Story Page: the
        from live.task_draft import draft_task_spaces      # plain Page Task views until Q03
        return draft_task_spaces(folder, root, sub)
    if level == "Job" and folder.name.startswith(("A1-", "j00_")):   # the Story Job (g03 D1)
        return story_spaces(folder, root, sub)
    if level == "Job":                              # a version (s12): today's group, or jNN_v<N>_<desk>/
        return version_spaces(folder, root, sub)
    if level != "Block" or not (folder / "board.md").is_file():
        return {}
    d = _data(folder, root)
    return _disk_block(d, folder, {"Description": _description(d, folder, root, sub),
                                   "Related": _related_space(d, folder, root, sub),
                                   "Idea Studio": _studio(d, folder, root),
                                   "Audience Report": _report(d, folder, root, sub),
                                   "Work Details": _board_work(d, folder, root, sub),
                                   "Runs": Space(run_types=_run_cards("Block", "Runs")),
                                   "Delivery": _delivery(d, sub, board=folder, root=root)})


def work_meta(folder, root):
    """A paper's words on a Work card (b10 s32-D19): a Job is a send, the rounds or the story; a Section, its state."""
    from live.paper_theme_section import _header
    folder = Path(folder)
    if P.is_section(folder.name):
        st = _header(face(folder)).get("state", "") if face(folder) else ""
        return esc(P._state_word(st) or st)
    if (folder.parent / "board.md").is_file():
        return ("story (reference)" if folder.name.startswith(("A1-", "j00_")) else
                "rounds" if folder.name.startswith("Bc-") else "send")
    return ""


# ── Delivery: each result in its Section series (JL 261014: "there should be groups for the section-task group") ──
# A version's own build (the whole paper) first, then its Sections by series, each series in reading order:
# t00 Abstract and t0N Main, t2N Appendix, t3N Letters (haipipe-paper ref/paper-ladder.md).
SERIES = (("📄 Paper", None), ("Main", ("0",)), ("Appendix", ("2",)), ("Letters", ("3",)))


def delivery_fixed(item: dict):
    """(groups, order) of one Delivery result: its version's whole build is "📄 Paper"; a Section's result goes
    under its series, ordered by its Task number."""
    parts = item.get("source", "").split(" › ")
    task = next((p for p in parts if re.match(r"^t\d{2}_", p)), None)
    if task is None:
        return ["📄 Paper"], (0, 0)
    for n, (name, leads) in enumerate(SERIES):
        if leads and task[1] in leads:
            return [name], (n, int(task[1:3]))
    return ["Sections"], (9, int(task[1:3]))


THEME = Theme(name="paper", label="Paper", icon="📄", guide="paper", work_meta=work_meta, delivery_fixed=delivery_fixed,
              level_names={"Block": "Paper Board", "Job": "Version", "Task": "Section"}, spaces=spaces,
              # today's folders on the ladder, unrenamed (b03, JL 261007: keep the names): a group
              # Ba-/Bb-/Bc-<desk>-<part> or A1-Story is a Job (jNN_ folders are Jobs by their prefix); a
              # Section S-…, a review batch RD<NN>/CM<NN> or a Story Page inside one is a Task (g03)
              level_patterns={"Job": r"^(B[a-z]|A1)-", "Task": r"^(S-|RD\d|CM\d|Story|t\d{2}_)"})


# ── moved out, still importable here ──────────────────────────────────────────────────────────────────────
_MOVED = ("paper_theme_report", "paper_theme_work", "paper_theme_section", "paper_theme_story", "paper_theme_version")


def __getattr__(name):
    """A name moved to one of the _MOVED modules still resolves here (`from live.paper_theme import _story_sections`),
    loaded on first use, so those modules can import this one's helpers at their top without an import cycle."""
    if not name.startswith("__"):
        import importlib
        for module in _MOVED:
            found = importlib.import_module("live." + module).__dict__
            if name in found:
                return found[name]
    raise AttributeError("module %r has no attribute %r" % (__name__, name))
