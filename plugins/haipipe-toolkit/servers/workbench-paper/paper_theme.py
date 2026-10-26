"""The paper theme on the base frame (servers/workbench/frame.py): only what differs from vanilla.

A paper Board climbs the ladder as Tools/blueprints/b16_theme_paper proposes (Q01, s11-paper-block): the
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

from src.common import delivery_dir, delivery_read_lane_dir, delivery_relative
import re
from pathlib import Path

from live import paper as P
from live.discoveryboard import file_url as disc_file_url
from live.frame import (Space, Theme, delivery_view, esc, face, link, pop, reader, rel, studio_cards,
                        table, topic_drawings, vanilla, work_tree)
from live.task_draft import draft_task_spaces


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
            # a Result card is no Page Face, so /_board/page refuses it: open it in the Discovery reader
            # (<block>/jNN/tNN/runs/rNN/result → the Block is five folders up; results/rNN → four)
            card = run / f"{name}.md" if run is not None else None
            read = (link(disc_file_url(run.parents[4 if run.name == "result" else 3], card, root),
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


def _spine(d):
    out = []
    stems = {x["stem"] for x in P.current_stories(d)}            # the Story the Board tells now (story-current)
    shown = [s for s in d["story"] if s["stem"] in stems] or d["story"]
    many = len(shown) > 1
    for s in shown:
        if many:
            out.append(f"<h3>{esc(s['stem'])}</h3>")
        for n, title, (face, subs, paras) in s["spine"]:
            rows = [(k, P.inline(v)) for k, v in face] + ([("", P.prose(paras))] if paras else [])
            rows += [(sub, P.prose(pg)) for sub, pg in subs if pg]
            out.append(_fold(esc(title), "", _kv(rows) if rows else _empty("Empty."),
                             P._link(d, s["rel"], "Open ↗", focus="C%d" % n), opened=True))
    return "".join(out) or _empty("No Story yet.")


def _ideas(d):
    i = d["ideation"]
    if not i["present"]:
        return _empty("No Story00-ideation page yet.")
    out = []
    for x in i["ideas"]:
        sub = dict((k.lower(), " ".join(v)) for k, v in x.get("substance") or [])
        rq = next((v for k, v in sub.items() if k.startswith(("research question", "question"))), "")
        verdict = (x.get("verdict") or "⬜ open")
        went = x.get("went") if x.get("went") not in (None, "", "—", "-") else ""
        rows = [(k, P._field_html(v)) for k, v in x.get("substance") or []]
        rows += [(l, esc(v)) for l, v in x.get("fields", []) if l.lower() not in ("verdict", "went to")]
        rows += [("Verdict", esc(verdict))] + ([("Went to", esc(went))] if went else [])
        out.append(_fold(f"{esc(x['id'])} · {esc(rq or x['title'])}",
                         esc(verdict.split(" · ")[0]) + (f" · went to {esc(went)}" if went else ""), _kv(rows)))
    return "".join(out) or _empty("No idea yet.")


# JL 261007: the Audience Report is questions; Spine, Design and the telling are one view, Narrative: how we
# tell the story, and whether it will attract an editor, a reviewer and the public
AUDIENCE = ("Ideation", "Narrative", "High-level logic + Low-level work", "Related Questions", "Related Papers")
# who the story must attract, what each looks for, and the Story division that answers it (by its heading)
ATTRACT = (("editor", "fit, and a contribution worth the pages, in one sentence", ("Identity", "Pitch")),
           ("reviewer", "claims backed by evidence, honest about their limits", ("Research Questions", "Evidence")),
           ("public", "why it matters, and what to take away", ("Stakes", "Pitch")))
ASKERS = ("reviewer", "coauthor", "editor", "reader")   # who asks a Board question (JL 261007), its `group:`

def _design(d, block, root):
    """The Story's design drawing, presented view only (its working copy is edited in Idea Studio)."""
    studio = block / "studio"
    stems = [x["stem"] for x in P.current_stories(d)]
    files = sorted(studio.glob("*.excalidraw"), key=lambda f: (f.stem not in stems, f.name)) if studio.is_dir() else []
    out = []
    for k, f in enumerate(files):
        url = "/_excalidraw/?" + P.urlencode({"board": rel(f, root)})
        out.append(_fold(esc(f.stem), "view only · edited in Idea Studio",
                         f'<iframe class=st-frame title="{esc(f.stem)}" data-src="{esc(url)}" referrerpolicy=no-referrer></iframe>',
                         link(url, "↗ full size"), opened=k == 0))
    return "".join(out) or _empty("No design drawing yet: draw the Story in Idea Studio, studio/<Story>.excalidraw.")


def _narrative(d):
    rows = P.section_rows(d)
    return "".join(_fold(f"{esc(r['num'])} {esc(r['name'])}".strip(),
                         esc(P._state_word(r["state"])) + " · " + esc(r["id"]),
                         _kv(P._fields(r["heads"], r["row"]["cells"], {0, 1})) if r["row"] else
                         _empty("No Narrative row for this Section."))
                   for r in rows) or _empty("No Section yet.")


_STATUS = {"answered": ("✅ answered", "ok"), "partial": ("🟡 partial", "warn"), "open": ("⬜ open", "")}


def _questions(folder, root):
    """The folder's register (its face's ## Questions), each with its report: [(row, report page or None)]."""
    from live.frame import _register, face
    out = []
    for r in _register(face(folder)):
        page = folder / r["report"] if r.get("report") else None
        if page is None or not page.is_file():
            qid = str(r.get("id", ""))[1:].zfill(2)
            found = sorted(folder.glob(f"reports/q{qid}_*/q{qid}_*.md"))
            page = found[0] if found else None
        out.append((r, page))
    return out


def _question_card(r, page, root):
    """One Question as the old card (JL 261007: "All the things to be the card"): id · title · its question
    under it · group · its answer status; opened, the question, the answer line, its work and its report."""
    head = page.read_text(encoding="utf-8", errors="replace") if page else ""
    status = re.search(r"(?m)^answer-status:\s*(\w+)", head)
    word, cls = _STATUS.get(status.group(1) if status else "open", ("⬜ open", ""))
    if re.search(r"(?m)^page-type:\s*comments", head):
        word, cls = "💬 comments", ""
    opening = re.search(r"(?ms)^## Opening\s*\n+(.*?)(?:\n\n|\Z)", head)
    work = r.get("work") or []
    work = ", ".join(str(w.get("task") or w.get("path") or w) if isinstance(w, dict) else str(w) for w in work)
    rows = [("question", esc(str(r.get("question") or r.get("title") or "")))]
    if opening:
        rows.append(("answer", esc(opening.group(1).strip())))
    rows.append(("work", esc(work) if work else '<span class="mut">no work named yet</span>'))
    rows.append(("report", pop(reader(page, root), page.stem, page.name + " ↗") if page else
                 '<span class="mut">no report yet</span>'))
    return P._card(str(r.get("id")), str(r.get("id")), str(r.get("title") or r.get("id")),
                   esc(str(r.get("question") or "")) if r.get("question") != r.get("title") else "",
                   esc(str(r.get("group") or "")), word, cls, rows)


def _question_cards(folder, root, group=None, skip=()):
    rows = [(r, pg) for r, pg in _questions(folder, root)
            if (group is None or r.get("group") == group) and r.get("group") not in skip]
    cards = [_question_card(r, pg, root) for r, pg in rows]
    if group is not None:                           # the group is the heading above: not again on each card
        cards = [c.replace(f'<span class="item-where">{esc(group)}</span>', '<span class="item-where"></span>') for c in cards]
    return P._cards(cards, "No question yet.") if rows else ""


# ── a question as a row (JL 261007: "put things here in the question format", the Insight rows):
# Question (pill, mark, its name, the question, More) │ Task Work (numbered) │ Report (pill, status, title, answer)
_MARK = {"answered": "✅", "partial": "🟡", "open": "⬜"}
_WORD = {"answered": "Answered", "partial": "Partly answered", "open": "Not answered yet"}


def _pill(text):
    return f'<span class="item-kind">{esc(text)}</span>'


def _qrow(left, work, report, key=""):
    return (f'<div class="q-row"{(" id=" + chr(34) + "question-" + esc(key) + chr(34)) if key else ""}>'
            f'<div class=q-l>{left}</div><div class=q-w>{work}</div><div class=q-r>{report}</div></div>')


def _status_of(page):
    head = page.read_text(encoding="utf-8", errors="replace") if page else ""
    m = re.search(r"(?m)^answer-status:\s*(\w+)", head)
    return (m.group(1) if m and m.group(1) in _MARK else "open"), head


def _report_side(page, root, question=""):
    """Report: its pill and status, its title (the Page, in the pop-out), its answer line, its tag."""
    if page is None:
        return f'<p>{_pill("Report")}</p><p class=mut>No report yet</p>'
    status, head = _status_of(page)
    title = re.search(r"(?m)^# +(.*)$", head)
    title = title.group(1).strip() if title else page.stem
    opening = re.search(r"(?ms)^## Opening\s*\n+(.*?)(?:\n\n|\Z)", head)
    return (f'<p>{_pill("Report")} <span class=mut>{_WORD[status]}</span></p>'
            f'<p class=rp-title><b>{pop(reader(page, root), title, title + " ↗")}</b></p>'
            + (f'<p class=rp-text>{esc(opening.group(1).strip())}</p>'          # its answer, not the question again
               if opening and opening.group(1).strip() != question.strip() else "")
            + f'<p class=mut>report {esc(page.stem.split("_")[0])}</p>')


def _story_question(T, page):
    """The Story question a report answers (its block's `· RQk`), or None."""
    head = page.read_text(encoding="utf-8", errors="replace") if page else ""
    m = re.search(r"(?m)^####\s+[\d.]+\s*·\s*Question\s+\d+\s*·\s*(RQ\d+)", head)
    return next((q for q in (T or {}).get("questions", []) if m and q["id"] == m.group(1)), None)


def _task_work(T, sq, work=()):
    """Task Work: the question's Task Roadmap rows, numbered (each its id, name and what it does)."""
    items = [T["work"][i["w"]] for i in (sq or {}).get("items", []) if i["w"] in (T or {}).get("work", {})]
    lines = [f'<li><b>{esc(w["id"])} · {esc(w["name"])}</b> · {esc(w["text"])}</li>' for w in items]
    lines += [f"<li>{esc(str(w))}</li>" for w in work]
    return (f'<p>{_pill("Task Work")} <span class=mut>{len(lines)} item{"" if len(lines) == 1 else "s"}</span></p>'
            + (f'<ol class=qw-list>{"".join(lines)}</ol>' if lines else '<p class=mut>No Task linked yet</p>'))


def _question_row(n, r, page, T, root):
    status, _ = _status_of(page)
    sq = _story_question(T, page)
    more = []
    for h in (sq or {}).get("hyps", []):
        more.append(f'<li><b>Hypothesis {esc(h["id"])}</b> · {esc(h["phrase"])}</li>')
    for c in (sq or {}).get("claims", []):
        more.append(f'<li><b>Claim {esc(c["id"])}</b> · {esc(c["text"])}</li>')
    why = next((v for k, v in (sq or {}).get("fields", []) if k.lower().startswith("why")), "")
    if why:
        more.insert(0, f'<li><b>Why the paper needs it</b> · {esc(why)}</li>')
    left = (f'<p>{_pill(f"Question {n}")} {_MARK[status]}</p><p><b>{esc(str(r.get("title") or ""))}</b></p>'
            f'<p>{esc(str(r.get("question") or ""))}</p>'
            + (f'<details class=qmore><summary>More</summary><ul>{"".join(more)}</ul></details>' if more else ""))
    work = [w.get("task") or w.get("path") or w if isinstance(w, dict) else w for w in (r.get("work") or [])]
    return _qrow(left, _task_work(T, sq, work), _report_side(page, root, str(r.get("question") or "")),
                 str(r.get("id", "")))


def _idea_row(x):
    """An idea as a question row: the question it asks │ how it was tested │ its verdict and where it went."""
    verdict = x.get("verdict") or "⬜ open"
    mark = "✅" if verdict.startswith("✅") else "🔴" if verdict.startswith(("❌", "🔴")) else "⬜"
    sub = dict((k.lower(), " ".join(v) if isinstance(v, list) else str(v)) for k, v in x.get("substance") or [])
    rq = next((v for k, v in sub.items() if k.startswith(("research question", "question"))), "")
    fields = [(l, v) for l, v in x.get("fields", []) if l.lower() not in ("verdict", "went to")]
    more = [f'<li><b>{esc(k)}</b> · {esc(v)}</li>' for k, v in sub.items() if v and not k.startswith(("research question", "question"))]
    left = (f'<p>{_pill("Idea " + str(x.get("id", "")))} {mark}</p><p><b>{esc(x.get("title", ""))}</b></p>'
            + (f'<p>{esc(rq)}</p>' if rq and rq != x.get("title") else "")
            + (f'<details class=qmore><summary>More</summary><ul>{"".join(more)}</ul></details>' if more else ""))
    work = (f'<p>{_pill("Tests")} <span class=mut>{len(fields)}</span></p>'
            + (f'<ol class=qw-list>{"".join(f"<li><b>{esc(l)}</b> · {esc(v)}</li>" for l, v in fields)}</ol>'
               if fields else '<p class=mut>Not tested yet</p>'))
    went = x.get("went") if x.get("went") not in (None, "", "—", "-") else ""
    report = (f'<p>{_pill("Verdict")}</p><p><b>{esc(verdict.split(" · ")[0])}</b></p>'
              + (f'<p class=rp-text>{esc(" · ".join(verdict.split(" · ")[1:]))}</p>' if " · " in verdict else "")
              + (f'<p class=mut>went to {esc(went)}</p>' if went else ""))
    return _qrow(left, work, report, str(x.get("id", "")))


def _question_rows(d, block, root, rows):
    """Rows for (register row, report page) pairs, the Story's tree giving each its Task Work and More."""
    stories = P.current_stories(d)
    T = P.story_tree(stories[0]) if stories else None
    return "".join(_question_row(int(str(r.get("id", "Q0"))[1:] or 0) if str(r.get("id", ""))[1:].isdigit() else k + 1,
                                 r, pg, T, root) for k, (r, pg) in enumerate(rows))


# ── b03's question row, the base frame's own (JL 261007: "I want it to be the format like this"): Logic
# (tag · title, status, the Idea Studio topics that feed it) │ Work │ Report (title ↗, answer, drawing, tag)
_HEAD = ('<div class="q-row q-head-row"><div>Logic · the question</div><div>Work · the Jobs, Tasks and Runs</div>'
         '<div>Report · what it says</div></div>')


def _base_rows(folder, root, group=""):
    """The base frame's Question │ Work │ Report rows for one register group (all when "")."""
    from live.frame import question_rows
    html, _ = question_rows("Block" if (folder / "board.md").is_file() else "Job", folder, root, group)
    return html if "q-row" in html and "No Questions at this level" not in html else ""


def _with_story_work(html, d, block, root):
    """Fill each research question's Work with its Task Roadmap rows, numbered (the Story's planned work),
    where the register names none."""
    stories = P.current_stories(d)
    T = P.story_tree(stories[0]) if stories else None
    for r, page in _questions(block, root):
        sq = _story_question(T, page)
        items = [T["work"][i["w"]] for i in (sq or {}).get("items", []) if i["w"] in (T or {}).get("work", {})]
        if not items:
            continue
        work = ('<ol class=qw-list>' + "".join(f'<li><b>{esc(w["id"])} · {esc(w["name"])}</b> · {esc(w["text"])}</li>'
                                               for w in items) + "</ol>")
        pat = re.compile(r'(<div class=q-row id="question-%s"><div class=q-l>.*?</div><div class=q-w>)'
                         r'<span class=mut>no work yet</span>(</div>)' % re.escape(str(r.get("id"))), re.S)
        html = pat.sub(lambda m: m.group(1) + work + m.group(2), html, count=1)
    return html


def _brow(tag, title, status, feeds, work, report):
    """A row in the same markup, for what is not a registered Question (an idea, an audience)."""
    logic = (f'<p class=q-head><span class=kind>{esc(tag)}</span> <b>{esc(title)}</b></p>'
             + (f'<p class=mut>{esc(status)}</p>' if status else "")
             + (f'<p class=from>from the Idea Studio</p><ul class=from-list>{feeds}</ul>' if feeds else ""))
    return (f'<div class=q-row><div class=q-l>{logic}</div><div class=q-w>{work or "<span class=mut>no work yet</span>"}'
            f'</div><div class=q-r>{report}</div></div>')


def _feed(block, root, topic_glob):
    """The Idea Studio topics matching a glob, as the base's "from the Idea Studio" list items."""
    out = []
    for t in sorted((block / "studio").glob(topic_glob)) if (block / "studio").is_dir() else []:
        face_md = t / f"{t.name}.md"
        drawing = next(iter(topic_drawings(t)), None)      # its own drawing first, never its mNN mind map
        url = ("/_excalidraw/?" + P.urlencode({"board": rel(drawing, root)})) if drawing else reader(face_md, root)
        out.append(f'<li>{pop(url, t.name + " · from the Idea Studio", t.name + " ↗")}</li>')
    return "".join(out)


def _group_questions(block, root, group):
    """The Board's questions of one group (board.md ## Questions, group: <group>), as the old cards."""
    html = _question_cards(block, root, group)
    return pv(html) if html else ""


def _attract(d):
    """Will the story attract them? One row per audience: what it looks for, where the Story answers it."""
    cards = []                                        # one card per audience, the old Evidence-card shape
    for s in [x for x in d["story"] if x["stem"] in {c["stem"] for c in P.current_stories(d)}][:1]:
        for who, wants, heads in ATTRACT:
            found = [(n, t) for n, t, _ in s["spine"] if any(h.lower() in t.lower() for h in heads)]
            where = " · ".join(P._link(d, s["rel"], t, focus="C%d" % n) for n, t in found) or "—"
            cards.append(P._card("attract-" + who, who, wants, "", where, "⬜ not judged yet", "warn",
                                 [("looks for", esc(wants)), ("where the Story answers it", where)]))
    return P._cards(cards, "No Story yet.") if cards else ""


def _says(d):
    """What it says: the current telling's Identity, Pitch and Stakes, one old spine card each, its words as
    written (bullets stay bullets), each with Open ↗ to that division."""
    out = []
    for s in P.current_stories(d)[:1]:
        for n, title, _ in s["spine"]:
            body = P.division_body(P.read(d["board"] / s["rel"]), n).strip()
            out.append('<div class="card spine-card"><h2>%s<span class="tally">%s</span></h2>%s</div>'
                       % (esc(title), P._link(d, s["rel"], "Open ↗", focus="C%d" % n),
                          P._md_view(body) if body else '<div class="space-empty">Empty.</div>'))
    return "".join(out) or '<div class="space-empty">No Story yet.</div>'


def _narrative_view(d, block, root):
    """Narrative (JL 261007): how the paper tells its story, in four parts: what it says (the Spine), how it is
    drawn (the design), how it is told (the Sections in order), and whether it will attract its audience."""
    qs = _group_questions(block, root, "narrative")
    parts = [("Will it attract?", pv(_attract(d) or '<div class="space-empty">No Story yet.</div>')),
             ("What it says", pv(_says(d))),
             ("How it is drawn", _design(d, block, root))]
    return ((f"<h3>Narrative questions</h3>{qs}" if qs else "")
            + "".join(f"<h3>{esc(h)}</h3>{body}" for h, body in parts))


def _related_questions(block, root, d=None):
    """The Board's own questions, the ones its audience asks (b03 s01-D19: Related Questions), grouped by who
    asks: reviewer · coauthor · editor · reader; each a Question │ Work │ Report row, its report in reports/."""
    rows = [r for r, _ in _questions(block, root) if r.get("group") not in ("narrative", "ideation")]
    if not rows:
        return _empty("No questions yet. Ask one a reviewer, a coauthor, an editor or a reader will ask; "
                      "board.md ## Questions, group: reviewer · coauthor · editor · reader.")
    groups = sorted({str(r.get("group") or "other") for r in rows},
                    key=lambda g: (ASKERS.index(g) if g in ASKERS else len(ASKERS), g))
    pairs = _questions(block, root)
    return pv("".join(f'<h3 class="space-h">{esc(g)}</h3>'
                      + _question_rows(d, block, root, [(r, pg) for r, pg in pairs if str(r.get("group") or "other") == g])
                      for g in groups))


def _ideation_rows(d, block, root):
    """Ideation, b03's rows: each idea a question (tag i1 · the question it asks, its verdict, from the
    Ideation topic) │ how it was tested │ the verdict and where it went."""
    i = d["ideation"]
    feeds = _feed(block, root, "s[0-9][0-9]-ideation")
    rows = []
    for x in i["ideas"] if i["present"] else []:
        verdict = x.get("verdict") or "⬜ open"
        tests = [(l, v) for l, v in x.get("fields", []) if l.lower() not in ("verdict", "went to")]
        work = "".join(f'<p><b>{esc(l)}</b> · {esc(v)}</p>' for l, v in tests)
        went = x.get("went") if x.get("went") not in (None, "", "—", "-") else ""
        report = (f'<p class=rp-title><b>{esc(verdict.split(" · ")[0])}</b></p>'
                  + (f'<p class=rp-text>{esc(" · ".join(verdict.split(" · ")[1:]))}</p>' if " · " in verdict else "")
                  + f'<p class=rp-tags>idea {esc(x.get("id", ""))}' + (f' · went to {esc(went)}' if went else "") + "</p>")
        rows.append(_brow(x.get("id", ""), x.get("title", ""), verdict.split(" · ")[0], feeds, work, report))
    return (_HEAD + "".join(rows)) if rows else _empty("No idea yet.")


def _narrative_rows(d, block, root):
    """Narrative, b03's rows: will it attract each audience, a question each, from the current telling's topic
    (JL 261007: the telling's Identity · Pitch · Stakes are not shown here)."""
    cur = P.current_stories(d)[:1]
    feeds = _feed(block, root, (cur[0]["stem"] if cur else "s[0-9][0-9]-story-*"))
    rows = []
    for s in cur:
        for who, wants, heads in ATTRACT:
            found = [(n, t) for n, t, _ in s["spine"] if any(h.lower() in t.lower() for h in heads)]
            where = " · ".join(P._link(d, s["rel"], t, focus="C%d" % n) for n, t in found)
            rows.append(_brow(who, f"Will it attract the {who}?", "not judged yet", feeds,
                              f'<p>looks for: {esc(wants)}</p>' + (f'<p class=mut>where the Story answers it: {where}</p>'
                                                                   if where else ""),
                              '<p class=mut>No report yet: run Review for an audience</p>'))
    qs = _base_rows(block, root, "narrative")
    return (qs + (_HEAD + "".join(rows) if rows else "")) or _empty("No Story yet.")


def _fed_groups(d, block, root):
    """The register groups of the questions the current telling feeds (its face's **Feeds:** reports)."""
    cur = P.current_stories(d)
    text = P.read(block / cur[0]["rel"]) if cur and cur[0].get("rel") else ""
    feeds = re.search(r"\*\*Feeds:\*\*(.+?)(?:\n\s*\n|\Z)", text, re.S)
    fed = {"Q" + n for n in re.findall(r"\bq(\d\d)_", feeds.group(1) if feeds else "")}
    return list(dict.fromkeys(str(r.get("group") or "") for r, _ in _questions(block, root) if r.get("id") in fed))


def _report(d, block, root, sub):
    """The Audience Report in b03's own rows (JL 261007): every view a list of questions, Logic │ Work │ Report."""
    s = _pick(sub, AUDIENCE) if sub in AUDIENCE else ("Narrative" if d["story"] else "Ideation")
    if s == "Ideation":
        html = _base_rows(block, root, "ideation") + _ideation_rows(d, block, root)
    elif s == "Narrative":
        html = _narrative_rows(d, block, root)
    elif s == "Related Questions":
        told = set(_fed_groups(d, block, root))     # the telling's own questions are High-level logic's (s11)
        groups = [g for g in dict.fromkeys(str(r.get("group") or "") for r, _ in _questions(block, root))
                  if g not in ("ideation", "narrative") and g not in told]
        html = "".join(f'<h3>{esc(g)}</h3>' + _with_story_work(_base_rows(block, root, g), d, block, root)
                       for g in groups) or \
            _empty("No questions yet. Ask one a reviewer, a coauthor, an editor or a reader will ask; "
                   "board.md ## Questions, group: reviewer · coauthor · editor · reader.")
    elif s == "Related Papers":                     # the related work under the question each bears on (JL 261009);
        html = (_related(d, block, root, NOT_PAPERS) if (block / "related" / "related.md").is_file()   # groups by it
                else pv(P.related_by_question_html(d, [(str(r.get("id") or ""), str(r.get("title") or ""))
                                                       for r, _ in _questions(block, root)])))
    else:                                           # the current telling's research questions
        html = pv(P.logic_work_html(d))             # its original structure (JL 261007): question blocks,
        if 'class="qc lw-q"' not in html:           # logic beside work and report; a Board with no Story text
            html = "".join(_base_rows(block, root, g) for g in _fed_groups(d, block, root)) or html   # yet
    return Space(html=html, subspaces=AUDIENCE, open=s, run_types=_run_cards("Block", "Audience Report", s))


# The Board's Work (JL 261020: "Like in the work, we might also have Studio (studio is already in the top), and then
# the Idea, and then the Story, and DataFlow, and PaperFlow ... and later we can have many Jobs"): the paper's own
# steps before its versions, each Operation over Result as a Section's seven steps are (draft_steps), then its Jobs.
BOARD_STEPS = ("Idea", "Story", "DataFlow", "PaperFlow", "Jobs")
OLD_BOARD_SUBS = {"Main": "Jobs", "Appendix": "Jobs", "Evidence": "Jobs"}     # the old Work Details tabs still open
# step → (emoji, the Studio group whose topics it reads, a word the topic's name must hold, its prompt)
BOARD_STEP = {
    "Idea": ("💡", "Ideation", "", "/haipipe-paper ideate {b}: read studio/{t} and the related work (s10 to s14) and my "
             "notes; add or test ideas, each with its question, its novelty against the closest work and a verdict; "
             "then redraw the topic."),
    "Story": ("📖", "Story", "", "/haipipe-paper story {b}: read the ideas that went to a story and my notes; tell the paper "
              "in studio/{t} (the tension, what we do, the answer so far, who cares) and its research questions, one "
              "Board Question each; then redraw the topic."),
    "DataFlow": ("🔀", "Plan", "dataflow", "/haipipe-paper-plan {b} dataflow: read the Story's research questions and the "
                 "Runs on disk; draw in studio/{t} how the data becomes each answer (inputs, the Runs, what each feeds), "
                 "with what is still to run; then redraw."),
    "PaperFlow": ("🗺", "Plan", "workflow", "/haipipe-paper-plan {b} paperflow: read the Story, the DataFlow and my notes; "
                  "draw in studio/{t} how the answers become the paper (the Sections, the displays and the Run behind "
                  "each, the dates to the send); then redraw."),
}


def _board_topics(block, group, word=""):
    """The Board's studio topics of one group (their **Tags:** line), whose name holds `word`, in name order."""
    out = []
    for topic in sorted((block / "studio").glob("s[0-9][0-9]-*/")):
        md = topic / f"{topic.name}.md"
        text = md.read_text(encoding="utf-8", errors="replace") if md.is_file() else ""
        tags = re.search(r"(?m)^\*\*Tags:\*\*\s*(.*)$", text)
        names = [x.strip().strip("`").strip().casefold() for x in re.split(r"[,·|]", tags.group(1))] if tags else []
        if group.casefold() in names and word in topic.name:
            out.append((topic, text))
    return out


def _topic_lists(text, head):
    """The items under a face's `Decided` or `Open` heading (setext or `## `): its list items, each with its wrapped
    lines, or its `sNN-D01 · …` paragraphs; none-yet lines left out."""
    m = re.search(r"(?ms)^(?:## )?%s\s*\n(?:-{3,}\n)?(.*?)(?=^\S[^\n]*\n-{3,}\n|^## |\Z)" % head, text)
    body = m.group(1) if m else ""
    items = _items(body) or [" ".join(par.split()) for par in re.split(r"\n\s*\n", body)
                             if re.match(r"\s*s\d+-D\d+", par)]
    return [i for i in items if not i.startswith("(none")]


def _items(body):
    """The top-level list items of a Markdown body (`- ` or `1. `), each joined with its wrapped lines; a nested item
    and the text after the list are left out."""
    out, inside = [], False
    for line in (body or "").splitlines():
        if re.match(r"^(?:- |\d+\. )", line):
            out.append(re.sub(r"^(?:- |\d+\. )", "", line).strip())
            inside = True
        elif inside and line.startswith("  ") and line.strip() and not re.match(r"^\s+(?:- |\d+\. )", line):
            out[-1] += " " + line.strip()
        elif inside and line.strip() and not line.startswith(" "):
            inside = False
    return out


def _topic_what(text):
    """What the topic is, in its own first words: its **Topic:** line, else its Opening's first paragraph."""
    m = re.search(r"(?ms)^\*\*Topic:\*\*\s*(.*?)(?:\n\s*\n)", text) or re.search(r"(?ms)^## Opening\s*\n+(.*?)(?:\n\s*\n)", text)
    words = " ".join(m.group(1).split()) if m else ""
    first = re.split(r"(?<=[.?!])\s", words, maxsplit=1)[0]
    return first if len(first.split()) <= 40 else " ".join(first.split()[:40]) + " …"


def _board_state(steps):
    """Each step's chip: no topic yet → next (the first) or later; open points → asked; else done."""
    out, first = {}, True
    for name, topics in steps.items():
        if not topics:
            out[name], first = ("next" if first else "todo"), False
        elif any(_topic_lists(text, "Open") for _t, text in topics):
            out[name] = "asked"
        else:
            out[name] = "done"
    return out


# an idea card's lines, the label it reads under and the field it comes from (the Ideation contract's names)
IDEA_LINES = (("Question", "Research Question"), ("Hypothesis", "Hypothesis"), ("Test", "Minimum Experiment"),
              ("Closest work", "Discovery Basis"), ("Risk", "Risk"), ("Next", "Next Evidence Action"))


def _first_sentence(text, words=45):
    """A field's first sentence, as read (its Markdown marks kept for P.inline), cut at `words`."""
    text = " ".join(text.split())
    m = re.search(r"(?<=[.?!])\s+(?=[A-Z0-9(\"“])", text)
    first = text[:m.start()] if m else text
    ws = first.split()
    return first if len(ws) <= words else " ".join(ws[:words]) + " …"


def _idea_groups(text):
    """[(mark, name, note, [ids])] from the ranked list's sketch (`🔥 first   i13 i14   the roster batch: …`)."""
    m = re.search(r"(?ms)^### \d+ · Ideas \(ranked\).*?```text\n(.*?)```", text or "")
    out = []
    for line in (m.group(1).splitlines() if m else []):
        g = re.match(r"^(\S+)\s+(.+?)\s{2,}((?:i\d+\s*)+?)\s{2,}(.*)$", line.strip())
        if g:
            out.append((g.group(1), g.group(2).strip(), g.group(4).strip(), g.group(3).split()))
    return out


def _line(label, html):
    """One labelled line of a card: the label small and grey in its own column, the words beside it."""
    return (f'<div style="display:grid;grid-template-columns:7.2em 1fr;gap:10px;margin:3px 0">'
            f'<span style="color:var(--mut);font:11.5px/1.9 ui-monospace,Menlo,monospace">{esc(label)}</span>'
            f'<span style="line-height:1.55">{html}</span></div>')


def _card(head, rows, foot="", anchor=""):
    """A light card: its head in bold, then its labelled lines (JL 261020: "I still want each of them to have a card")."""
    return (f'<div class=topic style="padding:10px 16px 8px;margin:0 0 10px"{f" id={chr(34)}{esc(anchor)}{chr(34)}" if anchor else ""}>'
            f'<div style="margin-bottom:4px">{head}</div>' + "".join(_line(k, v) for k, v in rows if v)
            + (f'<div class=mut style="font-size:12.5px;margin-top:6px">{foot}</div>' if foot else "") + "</div>")


def _key(html):
    """The line to read first, as plain text (JL 261020, of yellow boxes and big numbers: "看起来太咋咋呼呼了，就没有重点")."""
    return f'<p style="margin:2px 0 8px;line-height:1.55">{html}</p>'


def _folded(head, meta, body, anchor=""):
    """A row folded closed, its emoji and bold title only, as 1 · Plan's rows (JL 261020: "可以把它们也都变成闭合的吗";
    "我还是喜欢这种模式的"); opened, its state first, then its body."""
    head = re.sub(r"</?b>", "", head).strip()
    return (f'<details class="topic work-task"{f" id={chr(34)}{esc(anchor)}{chr(34)}" if anchor else ""}><summary>'
            f'<span class=related-head><b>{head}</b></span></summary><div class=work-body style="padding:4px 16px 12px">'
            + (f'<p class=mut style="font-size:13px;margin:2px 0 8px">{meta}</p>' if meta else "") + f"{body}</div></details>")


def _cols(cols):
    """Columns read left to right, an arrow between them, as a drawing's row of frames; they stack on a narrow screen."""
    return ('<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:22px;margin-top:6px">'
            + "".join(f'<div><div style="font:600 12.5px system-ui,sans-serif;color:var(--mut);margin-bottom:4px">'
                      f'{esc(title)}{" →" if k < len(cols) - 1 else ""}</div>{body}</div>' for k, (title, body) in enumerate(cols))
            + "</div>")


def _mini(head, text, foot=""):
    """One entry in a column (a hypothesis, a claim, a step): its name in bold, its sentence, a grey note; no box."""
    return (f'<div style="margin:0 0 9px;line-height:1.45"><b>{head}</b>' + (f'<br>{text}' if text else "")
            + (f'<br><span class=mut style="font-size:12.5px">{foot}</span>' if foot else "") + "</div>")


def _section(title, note, body):
    """A quiet label over a run of rows (the ideas' groups), then the rows."""
    return (f'<div class=mut style="font-size:12.5px;margin:14px 0 5px">{esc(title)}' + (f' · {esc(note)}' if note else "")
            + f"</div>{body}")


def _idea_card(x, words=None, mark=""):
    """One idea, folded to its one line (its short question, verdict and state), opened as its drawing card is: why it
    matters in the key box, its data beside its method, what each finding would mean, now and next; then the face's
    full question, closest work and risk (JL 261020: "让它的 layout 跟我们 draw 里面长得比较相似一些")."""
    w = words or {}
    sub = {k.lower(): " ".join(v) for k, v in x.get("substance") or []}
    status = {k.lower(): re.sub(r"\s*\(.*?\)", "", v) for k, v in x.get("fields") or []}
    call = _first_sentence(sub.get("recommendation", ""), 12)
    short = w.get("short") or _first_sentence(sub.get("research question") or x.get("title", ""), 18)
    meta = " · ".join(esc(v) for v in ([x.get("verdict") or "⬜ open"] + [f"{k} {status[k]}" for k in ("novelty", "pilot")
                                                                         if status.get(k)] + ([call] if call else [])))
    why = w.get("why") or _first_sentence(sub.get("hypothesis", ""))
    results = "<br>".join(f'{P.inline(r.get("find", ""))} <span class=mut>→</span> {P.inline(r.get("means", ""))}'
                          for r in w.get("results") or [])
    rows = [("Question", P.inline(sub.get("research question") or x.get("title", ""))),
            ("Why it matters" if w.get("why") else "Hypothesis", P.inline(why)),
            ("Data", " · ".join(P.inline(i) for i in w.get("data") or [])),
            ("Method", "<br>".join(f"{k}. {P.inline(i)}" for k, i in enumerate(w.get("method") or [], 1))
             or P.inline(_first_sentence(sub.get("method", "")))),
            ("If we find", results + (' <span class=mut>(drafted)</span>' if results and w.get("drafted") else "")),
            ("Now", P.inline(w.get("now", ""))), ("Next", P.inline(w.get("next") or _first_sentence(sub.get("next evidence action", "")))),
            ("Closest work", P.inline(_first_sentence(sub.get("discovery basis", "")))), ("Risk", P.inline(_first_sentence(sub.get("risk", ""))))]
    body = ["".join(_line(k, v) for k, v in rows if v)]
    return _folded(f'{esc(mark)} <b>{esc(x["id"])} · {P.inline(short)}</b>', meta, "".join(body), f"idea-{x['id']}")


def _drawing_words(page):
    """The topic's drawing words (`<topic>-drawing.yaml`), {} when it has none."""
    import yaml
    if not page:
        return {}
    f = Path(page.get("path") or "")
    try:
        return yaml.safe_load(f.read_text(encoding="utf-8")) or {} if f.is_file() else {}
    except Exception:
        return {}


def _idea_map(ideas, direction, shorts=None):
    """The ideas as a map: the direction in the root, each idea a branch (its verdict mark and its question), and a leaf
    for each of its hypothesis, method, smallest experiment, novelty and recommendation, cut to their first sentence."""
    labels = (("Hypothesis", "hypothesis"), ("Method", "method"), ("Minimum Experiment", "experiment"),
              ("novelty", "novelty"), ("Recommendation", "verdict"))
    branches = []
    for x in ideas:
        sub = {k.lower(): v for k, v in x.get("substance") or []}
        sub["novelty"] = [v for k, v in x.get("fields") or [] if k.lower() == "novelty"]   # its short mark, not the table
        leaves = []
        for label, tag in labels:
            said = " ".join(sub.get(label.lower()) or [])
            if said and not said.lstrip().startswith("|"):
                first = _first_sentence(said)
                leaves.append(_leaf("", tag, P.inline(first if len(first) <= 110 else first[:107].rsplit(" ", 1)[0] + " …"), note=said))
        mark = (x.get("verdict") or "").split()[0] if (x.get("verdict") or "")[:1] in "✅🔶⬜❗🟡❌" else ""
        # the drawing's short title when it has one (the full question shows on the card below and on hover)
        branches.append((f"{esc(mark)} {esc(x['id'])}", P.inline((shorts or {}).get(x["id"]) or x.get("title", "")), leaves, "",
                         f"idea-{x['id']}"))
    return _map("💡 The direction", P.inline(direction), branches) if branches else ""


def _idea_cards(d):
    """The Ideation topic as its drawing reads: the question in the key box, the setting folded, then each group of
    ideas (a card each, folded), then the path to G0."""
    i = d.get("ideation") or {}
    ideas = {x["id"]: x for x in i.get("ideas") or []} if i.get("present") else {}
    if not ideas:
        return ""
    page = P.ideation_topic(d["board"])
    text = page["text"] if page else ""
    words = _drawing_words({"path": str(d["board"] / "studio" / page["stem"] / f'{page["stem"]}-drawing.yaml')} if page else None)
    asked = re.search(r"(?ms)^## Opening\s*\n+(.*?)\n", text)
    index = words.get("index") or {}
    out = []
    roster = words.get("roster") or {}
    if roster:
        flow = " → ".join(P.inline(x) for x in [roster.get("start", ""), roster.get("roster", ""),
                                                 " / ".join(roster.get("google", [])), " / ".join(roster.get("agent", [])), roster.get("end", "")] if x)
        rows = ([("Question", P.inline(asked.group(1).strip()))] if asked else []) + \
               [("Pool", P.inline(index.get("key", ""))), ("Flow", flow), ("Reading", P.inline(roster.get("reading", "")))] + \
               [(n.get("big", ""), P.inline(n.get("tag", ""))) for n in roster.get("numbers") or []]
        out.append(_folded(f'🔑 {P.inline(roster.get("title", "The setting")).lstrip("①").strip()}', P.inline(roster.get("key", "")),
                           "".join(_line(k, v) for k, v in rows if v)))
    groups = [(g.get("name", ""), g.get("line", ""), g.get("ideas") or []) for g in words.get("groups") or []] or \
             [(f"{m} {n}", note, ids) for m, n, note, ids in _idea_groups(text)]
    sketch = {k: m for m, _n, _note, ids in _idea_groups(text) for k in ids}
    shown = set()
    for name, line, ids in groups:
        cards = [_idea_card(ideas[k], (words.get("ideas") or {}).get(k), sketch.get(k, "")) for k in ids if k in ideas and k not in shown]
        shown.update(ids)
        if cards:
            out.append(_section(name, line, "".join(cards)))
    rest = [_idea_card(x, (words.get("ideas") or {}).get(k)) for k, x in ideas.items() if k not in shown]
    if rest:
        out.append(_section("Other ideas", "", "".join(rest)))
    # the ideas also drawn as the draft's §1 mind map (JL 261022: "for the idea and for the story ... I want something
    # like this"): the direction in the root, each idea a branch in the drawing's order, its hypothesis, method,
    # experiment, novelty and recommendation the leaves; the cards follow under their own subsection
    order = [k for _n, _l, ids in groups for k in ids if k in ideas] + [k for k in ideas if k not in shown]
    direction = re.search(r"(?m)^\*\*The direction\*\*:\s*(.*)$", text)
    shorts = {k: v.get("short") for k, v in (words.get("ideas") or {}).items() if isinstance(v, dict) and v.get("short")}
    tree = _idea_map([ideas[k] for k in dict.fromkeys(order)], direction.group(1) if direction else (asked.group(1).strip() if asked else ""),
                     shorts)
    if tree:
        out = [_sub("The ideas"), tree, _sub("Each idea")] + out
    path = words.get("path") or {}
    if path.get("steps"):
        rows = [(st.get("title", ""), "<br>".join(P.inline(l) for l in st.get("lines") or [])) for st in path["steps"]]
        rows += [("Also", P.inline(path.get("also", "")))] + [("Open", P.inline(q)) for q in path.get("open") or []]
        out.append(_folded(f'🧭 {P.inline(path.get("title", "From here to G0")).lstrip("⑲").strip()}', P.inline(path.get("key", "")),
                           "".join(_line(k, v) for k, v in rows if v)))
    return "".join(out)


def _division(text, title):
    """The body of a face's `### N · <title>` division, up to the next division or setext heading."""
    m = re.search(r"(?ms)^### \d+ · %s[^\n]*\n(.*?)(?=^### \d+ · |^\S[^\n]*\n-{3,}\n|\Z)" % re.escape(title), text or "")
    return m.group(1) if m else ""


def _fields(body):
    """`**Label**: words` paragraphs and `- **Label**: words` or `1. **Label**: words` items → [(label, words)]."""
    out = []
    for par in re.split(r"\n\s*\n", body or ""):
        for item in (_items(par) or [" ".join(par.split())]):
            m = re.match(r"^\*\*(.+?)\*\*\s*:?\s*(.*)$", item.strip())
            if m:
                out.append((m.group(1).strip().rstrip(":"), m.group(2).strip()))
    return out


def _table(body, first):
    """The rows of a division's Markdown table whose first cell matches `first`, each a list of cells."""
    rows = [[c.strip() for c in line.strip().strip("|").split("|")] for line in (body or "").splitlines() if line.startswith("|")]
    return [r for r in rows if re.fullmatch(first, r[0])]


def _rq_blocks(body):
    """§3's `#### 3.N · Question N · RQn` blocks: (id, fields, {group: [item]}), an item a dict of its code, its
    `Name: sentence`, its other ` · ` parts and its indented `- **Label**: words` lines (a claim's Now, If it fails)."""
    out = []
    for m in re.finditer(r"(?ms)^#### [\d.]+ · Question \d+ · (RQ\d+)\s*\n(.*?)(?=^#### |\Z)", body or ""):
        fields, groups, group, last = [], {}, None, None
        for line in m.group(2).splitlines():
            g = re.match(r"^\*\*(Theories|Hypotheses|Potential claims|Potential contributions|Potential work|Tasks)\*\*\s*$", line.strip())
            if g:
                group, last = g.group(1), None
                groups[group] = []
                continue
            nested = re.match(r"^\s+- \*\*(.+?)\*\*\s*:\s*(.*)$", line)
            if nested and last is not None:
                last["more"][nested.group(1).strip().lower()] = nested.group(2).strip()
                continue
            item = re.match(r"^- \*\*(.+?)\*\*\s*(?::|·)\s*(.*)$", line)
            if not item:
                continue
            if group is None:
                fields.append((item.group(1), item.group(2).strip()))
                continue
            parts = [x.strip() for x in item.group(2).strip().split(" · ")]
            code = next((x for x in parts if re.fullmatch(r"C\d+", x)), item.group(1))
            said = next((x for x in parts if ":" in x), parts[-1] if parts else "")
            last = {"code": code, "said": said, "parts": parts, "more": {}}
            groups[group].append(last)
        out.append((m.group(1), fields, groups))
    return out


def _sub(title):
    """A subsection of a step's Result: a small grey heading over its folded cards (JL 261022: "for the results, should
    we also have the subsection as well? ... venue will be on subsection of the results")."""
    return (f'<h4 style="margin:20px 0 6px;font:600 12.5px system-ui,sans-serif;color:var(--mut);'
            f'letter-spacing:.04em;text-transform:uppercase">{esc(title)}</h4>')


def _map(root_title, root_text, branches):
    """A tree drawn as the draft's §1 mind map (JL 261022, of the Story and the Idea: "I want something like this"): the
    root box, each branch box with the line it hands to the next on the arrow below it, each leaf a code, a grey tag,
    its words and its evidence chips. Read-only, but it answers a click (JL 261023: "我点击这个 button 的时候，它就会 show
    more information"): a leaf opens its whole sentence under it, a branch opens its card below and scrolls to it. A
    branch is (id, title, [leaf html], hand-on) or (id, title, [leaf html], hand-on, the id of its card)."""
    from live.draft_steps import _mapview          # §1's look, shared by haipipe-mindmap's mapview.py
    PLAN_CSS, PLAN_JS = _mapview().CSS, _mapview().JS
    paras = []
    for k, b in enumerate(branches):
        bid, title, leaves, handon = b[:4]
        opens = f' data-open="{esc(b[4])}" title="open its card"' if len(b) > 4 and b[4] else ""
        paras.append(f'<div class=pm-para><div class="pm-node pm-pnode"{opens}><span class=pm-id>{bid}</span><b>{title}</b></div>'
                     f'<ul class=pm-leaves>{"".join(leaves)}</ul></div>'
                     + (f'<div class=pm-q>↓ {handon}</div>' if handon and k < len(branches) - 1 else ""))
    return (PLAN_CSS + MAP_RO + '<div style="overflow-x:auto;margin:4px 0 10px"><div class="pm pm-ro"><svg class=pm-wires aria-hidden=true></svg>'
            f'<div class="pm-node pm-root"><b>{root_title}</b>' + (f'<p>{root_text}</p>' if root_text else "")
            + f'</div><div>{"".join(paras)}</div></div></div>' + PLAN_JS)


# a read-only map's clicks: a leaf shows its whole text under it (click again to close), a branch opens its card
MAP_RO = """<style>.pm-ro .pm-leaves li[title]{cursor:pointer}.pm-ro .pm-leaves li[title]:hover .pm-t{color:var(--acc)}
.pm-ro .pm-pnode[data-open]{cursor:pointer}.pm-ro .pm-pnode[data-open]:hover{border-color:var(--acc)}
.pm-more{white-space:normal;max-width:680px;margin:3px 0 7px 38px;padding:6px 10px;border-left:2px solid var(--acc);
 background:var(--wash);color:var(--fg);font-size:13px;line-height:1.55;border-radius:0 6px 6px 0;cursor:auto}</style>
<script>(function(){if(window.__pmRo)return;window.__pmRo=1;
 document.addEventListener('click',function(e){var t=e.target;if(!t.closest)return;
  var n=t.closest('.pm-ro .pm-pnode[data-open]');
  if(n){var d=document.getElementById(n.dataset.open);if(d){d.open=true;d.scrollIntoView({behavior:'smooth',block:'start'});}return;}
  if(t.closest('.pm-more'))return;
  var li=t.closest('.pm-ro .pm-leaves li[title]');if(!li)return;
  var m=li.querySelector(':scope>.pm-more');
  if(m)m.remove();else{m=document.createElement('div');m.className='pm-more';m.textContent=li.getAttribute('title');li.appendChild(m);}
  if(window.pmDraw)window.pmDraw();});})();</script>"""


def _leaf(code, tag, words, chips="", note=""):
    """One leaf of a map: its code, a grey tag, its words, its chips; the whole sentence on hover."""
    return (f'<li{(" title=" + chr(34) + esc(note) + chr(34)) if note else ""}><span class=pm-s>{esc(code)}</span>'
            + (f'<span class=pm-role>{esc(tag)}</span>' if tag else "")      # no empty tag box (JL 261023: "干净一些")
            + f'<span class=pm-w><span class=pm-t>{words}</span>{chips}</span></li>')


VENUE_BRANCHES = (("The call", ("call", "editors", "window", "scope")),
                  ("What it asks", ("what it asks", "topics", "methods", "read first")),
                  ("The format", ("length", "words", "our budget", "submission", "same as")))


def _venue_map(venue_div, venues, held):
    """The target venue as a map: the venue in the root; its first frame split into the call, what it asks and the
    format (by each point's label), and each further frame (how the paper meets the call, why it is doable) a branch of
    its own; each point a leaf, its label the tag, its evidence rows as chips, the whole point on hover."""
    from live.draft_steps import INK

    def chip(e):
        state = held.get(e, "absent")
        ink = INK["need"] if state == "absent" else INK["cite"] if e.lower().startswith("ecite") else INK["value"]
        return f' <span class=pm-card style="color:{ink};border-color:{ink}66">{esc(e)}</span>'

    def leaf(point):
        label, _, words = point.partition(":") if re.match(r"^[^:]{1,80}:", point) else ("", "", point)
        words = re.sub(r"\s*\((?:E\w*\d+(?:, )?)+\)", "", words).strip()
        tag = " ".join(re.sub(r"\([^)]*\)|[\"“”]", "", label).replace(",", " ").split()[:2])
        return _leaf("", _clip(tag, 18), P.inline(_clip(words, 64)), _chips(re.findall(r"E(?:work|cite)\d+", point), chip), point)

    frames = list(re.finditer(r"(?ms)^#### (V\d+) · ([^\n]+)\n(.*?)(?=^#### |\Z)", venue_div))
    branches = []
    for k, m in enumerate(frames):
        points = _items(m.group(3))
        if k == 0:
            left = list(points)
            for name, keys in VENUE_BRANCHES:
                mine = [x for x in left if x.split(":", 1)[0].strip().lower().startswith(keys)]
                left = [x for x in left if x not in mine]
                if mine:
                    branches.append((esc(m.group(1)), esc(name), [leaf(x) for x in mine], ""))
            if left:
                branches.append((esc(m.group(1)), "More", [leaf(x) for x in left], ""))
        elif points:
            branches.append((esc(m.group(1)), P.inline(m.group(2).strip()[:1].upper() + m.group(2).strip()[1:]), [leaf(x) for x in points], ""))
    v = venues[0]
    root = f"🧭 {P.inline(v[1])}" if len(v) > 1 else "🧭 The venue"
    return _map(root, P.inline(v[3]) if len(v) > 3 else "", branches) if branches else ""


def _clip(text, n):
    """At most n characters, cut at a word; the whole text stays on the leaf's hover."""
    text = re.sub(r"\s+", " ", text or "").strip()
    return text if len(text) <= n else text[:n - 1].rsplit(" ", 1)[0].rstrip(",;:") + " …"


# a hypothesis's theory said in one short word on its tag, as the draft map's roles are (JL 261023, of the draft's map:
# "为什么别人的就是看起来那么的干净 ... 你能够做得干净一些吗？")
SHORT_THEORY = (("consideration", "consideration"), ("institutional", "logics"), ("bias in", "bias in/out"),
                ("copy of", "bias in/out"), ("cumulative", "cumulative"), ("safety", "safety"), ("long tail", "long tail"),
                ("superstar", "superstars"), ("four ways", "regulation"), ("oversight", "oversight"),
                ("many hands", "many hands"), ("remedial", "remedial"), ("equality", "fairness"), ("availability", "availability"))


def _short_tag(text):
    low = (text or "").lower()
    found = sorted((low.find(key), short) for key, short in SHORT_THEORY if key in low)   # the theory named first wins
    hit = found[0][1] if found else ""
    return hit or _clip(re.sub(r"[\"()]", "", text or "").split(";")[0], 16)


def _chips(codes, chip, keep=3):
    """At most `keep` evidence chips on a leaf, then a grey +n."""
    codes = list(dict.fromkeys(codes))
    more = f' <span class=mut style="font-size:11px">+{len(codes) - keep}</span>' if len(codes) > keep else ""
    return "".join(chip(e) for e in codes[:keep]) + more


def _outline(body):
    """A nested Markdown list as a tree: [(text, [children])], two spaces of indent a level."""
    root, stack = [], [(-1, None)]
    for line in (body or "").splitlines():
        m = re.match(r"^(\s*)- (.*\S)", line)
        if not m:
            continue
        depth, node = len(m.group(1)) // 2, (m.group(2), [])
        while stack and stack[-1][0] >= depth:
            stack.pop()
        (stack[-1][1][1] if stack[-1][1] else root).append(node)
        stack.append((depth, node))
    return root


def _tree_map(root_title, root_text, nodes):
    """A mind map of any depth (JL 261023, of the data flow: "You can make more layers of the mindmap tree"): a node
    with children is a box wired to them, a node without is a leaf; a line `title · note` puts its note grey beside it,
    `code · title · note` adds a code, and a leading ✅ 🔶 ⬜ 🙋 ❗ marks its state. A click opens a leaf's whole line."""
    from live.draft_steps import _mapview          # §1's look, shared by haipipe-mindmap's mapview.py
    PLAN_CSS = _mapview().CSS

    def split(text):
        parts = [x.strip() for x in text.split(" · ")]
        code = parts.pop(0) if len(parts) > 2 and len(parts[0]) <= 14 else ""
        return code, parts[0], " · ".join(parts[1:])

    def leaf(text):
        code, title, note = split(text)
        mark = note[:1] if note[:1] in "✅🔶⬜🙋❗" else ""          # its state first, as the story's RQ boxes show theirs
        note = note[1:].strip() if mark else note
        # "n of m folds" as a badge beside the name (JL 261023: "能把这个 n of n folds 变得显眼一些？")
        # and "n of m runs" the same way (JL 261024, the ScalingGlucose data flow: "I want you to make things like this")
        folds = re.search(r"(\d+) of (\d+) (folds|runs)[;:,]?\s*", note)
        badge = ""
        if folds:
            n, m = int(folds.group(1)), int(folds.group(2))
            ink = "#2b8a3e" if n == m else "#e8590c" if n else "#adb5bd"
            badge = (f' <span style="display:inline-block;margin:0 4px;padding:0 8px;border-radius:10px;background:{ink};'
                     f'color:#fff;font:700 12px/1.6 system-ui,sans-serif">{n} / {m} {folds.group(3)}</span>')
            note = (note[:folds.start()] + note[folds.end():]).strip(" ;,:")
        return _leaf(code, "", (f"{mark} " if mark else "") + f"{P.inline(_clip(title, 48))}" + badge + (f' <span class=mut style="font-size:12px">{P.inline(_clip(note, 70))}</span>' if note else ""),
                     note=text)

    def row(text, kids):
        code, title, note = split(text)
        boxes = "".join(row(t, k) for t, k in kids if k)
        leaves = "".join(leaf(t) for t, k in kids if not k)
        return (f'<div class=tr-row><div class="pm-node tr-box"{(" title=" + chr(34) + esc(note) + chr(34)) if note else ""}>'
                + (f'<span class=pm-id>{esc(code)}</span>' if code else "") + f'<b>{P.inline(title)}</b>'
                + (f'<span class=tr-note>{P.inline(_clip(note, 60))}</span>' if note else "")
                + f'</div><div class=tr-kids>{boxes}' + (f'<ul class=pm-leaves>{leaves}</ul>' if leaves else "") + '</div></div>')

    body = "".join(row(t, k) for t, k in nodes)
    return (PLAN_CSS + MAP_RO + TREE_CSS + '<div style="overflow-x:auto;margin:4px 0 10px"><div class="tr pm-ro"><svg class=tr-wires aria-hidden=true></svg>'
            f'<div class=tr-row><div class="pm-node pm-root tr-box"><b>{root_title}</b>' + (f'<p>{root_text}</p>' if root_text else "")
            + f'</div><div class=tr-kids>{body}</div></div></div></div>' + TREE_JS)


TREE_CSS = """<style>.tr{position:relative;width:max-content;min-width:100%;padding:8px 4px;box-sizing:border-box}
.tr-wires{position:absolute;left:0;top:0;pointer-events:none;overflow:visible}.tr-wires path{fill:none;stroke:var(--mut);stroke-opacity:.45;stroke-width:1.4}
.tr-row{display:grid;grid-template-columns:auto auto;gap:0 44px;align-items:center;margin:5px 0}
.tr-kids{display:flex;flex-direction:column;justify-content:center}
.tr-box{padding:8px 12px;font-size:14px;line-height:1.35;max-width:230px}.tr-box.pm-root{max-width:250px}
.tr-note{display:block;font-size:11.5px;color:var(--mut);margin-top:2px}
@media(max-width:1000px){.tr,.tr-row{display:block;width:auto}.tr-wires{display:none}.tr-kids{padding-left:14px;border-left:2px solid var(--line);margin:4px 0}}</style>"""
TREE_JS = """<script>(function(){if(window.__trMap)return;window.__trMap=1;
 function wire(a,b,o,leaf){var p=a.getBoundingClientRect(),q=b.getBoundingClientRect();
  var x1=p.right-o.left,y1=p.top+p.height/2-o.top,x2=q.left-o.left-6,y2=(leaf?q.top+12:q.top+q.height/2)-o.top,m=(x1+x2)/2;
  return '<path d="M'+x1+','+y1+' C'+m+','+y1+' '+m+','+y2+' '+x2+','+y2+'"/>';}
 function draw(){document.querySelectorAll('.tr').forEach(function(t){var svg=t.querySelector('.tr-wires');
  if(!t.offsetParent||getComputedStyle(svg).display==='none')return;var o=t.getBoundingClientRect(),d='';
  svg.setAttribute('width',o.width);svg.setAttribute('height',o.height);
  t.querySelectorAll('.tr-row').forEach(function(r){var box=r.querySelector(':scope>.tr-box'),k=r.querySelector(':scope>.tr-kids');
   k.querySelectorAll(':scope>.tr-row>.tr-box').forEach(function(c){d+=wire(box,c,o);});
   k.querySelectorAll(':scope>ul>li').forEach(function(l){d+=wire(box,l,o,true);});});
  svg.innerHTML=d;});}
 window.addEventListener('resize',draw);window.addEventListener('load',draw);setTimeout(draw,60);
 document.addEventListener('toggle',function(){setTimeout(draw,0);},true);document.addEventListener('click',function(){setTimeout(draw,0);});
 window.trDraw=draw;})();</script>"""


def _expand_csv(nodes, root):
    """A tree line `@csv <path from the SPACE root> · <column>=<value> · <label column> · <value column>` becomes one leaf
    per matching row, `label · value`, read now, so a count in the tree is never typed (JL 261023: "我们 fold00 到 fold09
    到底跑了几个了，你也要说明一下")."""
    import csv as _csv
    out = []
    for text, kids in nodes:
        if not text.startswith("@csv "):
            out.append((text, _expand_csv(kids, root)))
            continue
        parts = [x.strip() for x in text[5:].split(" · ")]
        path = (Path(root) / parts[0]) if root else Path(parts[0])
        if len(parts) < 4 or not path.is_file():
            out.append((f"❗ {path.name} · not on disk", []))
            continue
        key, _, want = parts[1].partition("=")
        for r in _csv.DictReader(path.open(encoding="utf-8")):
            if r.get(key.strip()) == want.strip():
                out.append((f"{r.get(parts[2], '')} · {r.get(parts[3], '')}", []))
    return out


def _flow_sections(text, root=None, division="Data tree", head="The data, as a tree"):
    """A Plan topic's tree division drawn as a many-layered mind map: the DataFlow topic's "Data tree", or the
    PaperFlow topic's "Paper tree" (JL 261024: the paper flow drawn as the data flow is)."""
    tree = _expand_csv(_outline(_division(text, division)), root)
    if not tree:
        return ""
    (root, kids), rest = tree[0], tree[1:]
    title, _, note = root.partition(" · ")
    return _sub(head) + _tree_map(P.inline(title), P.inline(note), kids + rest)


def _story_map(text):
    """§3 drawn as a mind map: the paper's question in the root, each research question a branch (its state and name),
    its hypotheses and claims the leaves (a hypothesis tagged with its theory and chipped with the evidence rows that
    test it: violet a row from our own Runs, blue a cited paper, red a row still absent), and on the arrow between two
    questions what the paper can say once the first is answered (the narrative)."""
    from live.draft_steps import INK
    rqs = _division(text, "Research Questions")
    asked = next((v for k, v in _fields(rqs.split("####")[0]) if k.lower().startswith("the paper's question")), "")
    held = {r[0]: r[-1].lower() for r in _table(_division(text, "Evidence Basis and Boundaries"), r"E\w*\d+")}
    story = re.search(r"(?ms)^\*\*The narrative, if the questions are answered\*\*.*?\n\n(.*?)(?:\n\s*\n(?=\S)(?!\d+\. )|\Z)", rqs)
    said = {}
    for line in _items(story.group(1)) if story else []:
        for rq in re.findall(r"\((RQ\d+)", line):
            said.setdefault(rq, re.split(r"(?<=\w)[:;]|, yet |, but ", line, maxsplit=1)[0].strip())

    def chip(e):
        state = held.get(e, "absent")
        ink = INK["need"] if state == "absent" else INK["cite"] if e.lower().startswith("ecite") else INK["value"]
        return f' <span class=pm-card style="color:{ink};border-color:{ink}66">{esc(e)}</span>'

    branches = []
    for rq, fields, groups in _rq_blocks(rqs):
        f = {k.lower(): v for k, v in fields}
        state = f.get("answer state", "")
        mark = state.split()[0] if state[:1] in "✅🔶⬜❗🟡" else ""
        leaves = []
        # its theories first (JL 261023: "You have C, I think you also need the Theory as well"): code, role, name;
        # short, as the draft map is, with the whole sentence and its test on hover
        for t in groups.get("Theories", []):
            # tagged "theory", as a claim is tagged "claim" (JL 261023: "is the mechanism you mean the theory? could you
            # name it to 'theory'?"); its role for this question (core, rival, ...) opens with its sentence on a click
            role = t["parts"][0] if len(t["parts"]) > 1 and ":" not in t["parts"][0] else ""
            name = re.sub(r"\s*\([^()]*\d{4}[^()]*\)", "", t["said"].split(":", 1)[0]).split(", with ")[0].strip()
            note = (f"Role here: {role} · " if role else "") + " · ".join(x for x in t["parts"] if x != role)
            leaves.append(_leaf(t["code"], "theory", f"<i>{P.inline(_clip(name, 44))}</i>", note=note))
        for h in groups.get("Hypotheses", []):
            name = h["said"].split(":", 1)[0]
            theory = re.search(r"\(([^()]*)\)\s*$", h["said"].split(" · tested by")[0])
            tested = next((x for x in h["parts"] if x.startswith("tested by")), "")
            leaves.append(_leaf(h["code"], _short_tag(theory.group(1)) if theory else "", P.inline(_clip(name, 44)),
                                _chips(re.findall(r"E\w*\d+", tested), chip), " · ".join(x for x in (h["said"], tested) if x)))
        for c in groups.get("Potential claims", []):
            leaves.append(_leaf(c["code"], "claim", f'<b>{P.inline(_clip(c["said"].split(":", 1)[0], 44))}</b>', note=c["said"]))
        branches.append((f"{esc(mark)} {esc(rq)}", P.inline(f.get("name", "")), leaves, "", f"story-{rq.lower()}"))
    # on the arrow, the question the next research question asks, short, as the draft's "why should physicians care?"
    branches = [(b, n, l, (branches[k + 1][1][:1].lower() + branches[k + 1][1][1:]) if k + 1 < len(branches) else "", a)
                for k, (b, n, l, _h, a) in enumerate(branches)]
    return _map("📖 The paper's question", P.inline(asked), branches) if branches else ""


def _story_sections(text):
    """A Story topic's face laid out as its drawing (JL 261020: "让它的 layout 跟我们 draw 里面长得比较相似一些"): the
    paper's question in the key box, then a folded card per research question, opened as the drawing's row (the question
    → what we expect, and why → what the paper can say), then the narrative, stakes, what we will not claim, the evidence,
    the work and where it could go, each folded (haipipe-paper-story §1 to §9)."""
    out = []
    ident, pitch, rqs = _fields(_division(text, "Identity")), _fields(_division(text, "Pitch")), _division(text, "Research Questions")
    asked = next((v for k, v in _fields(rqs.split("####")[0]) if k.lower().startswith("the paper's question")), "")
    one = next((v for k, v in ident if k.lower() == "one sentence"), "")
    bounds = _division(text, "Evidence Basis and Boundaries")
    ev = _table(bounds, r"E\w*\d+")
    held = {r[0]: r[-1].lower() for r in ev}
    if asked or one or pitch:
        out.append(_folded("📖 The paper's question", P.inline(asked), "".join(_line(k, P.inline(v)) for k, v in
                                                                         [("In a sentence", one)] + pitch if v)))
    cards = []
    for rq, fields, groups in _rq_blocks(rqs):
        f = {k.lower(): v for k, v in fields}
        state = f.get("answer state", "")
        chip = state.split()[0] if state[:1] in "✅🔶⬜❗🟡" else ""
        asked_rq = re.sub(r"\s*\(RQ\d+[a-z]:.*$", "", f.get("research question", ""))
        col1 = (_key(f"<b>Why it matters</b> · {P.inline(_first_sentence(f.get('why it matters', '')))}")
                + "".join(_key(f"<b>{k}</b> · {P.inline(_first_sentence(v))}") for k, v in (("How", f.get("question", "")),
                          ("Now", re.sub(r"^\S+\s+", "", state) if chip else state)) if v))
        hyps, in_hand = [], 0
        for h in groups.get("Hypotheses", []):
            tested = next((x for x in h["parts"] if x.startswith("tested by")), "")
            rows = [held.get(e.strip()) for e in re.findall(r"E\w*\d+", tested)]
            mark = "✅" if rows and all(r == "established" for r in rows) else "🔶" if any(r in ("established", "provisional") for r in rows) else "⬜"
            in_hand += mark == "✅"
            hyps.append(_mini(f"{mark} {esc(h['code'])} · {P.inline(h['said'].split(':', 1)[0])}",
                              P.inline(h["said"].split(":", 1)[1].strip() if ":" in h["said"] else ""), esc(tested)))
        n = len(hyps)
        theories = [_mini(f"{esc(t['code'])} · {P.inline(t['said'].split(':', 1)[0])}",
                          P.inline(t["said"].split(":", 1)[1].strip() if ":" in t["said"] else ""),
                          " · ".join(esc(x) for x in t["parts"] if x != t["said"]))
                    for t in groups.get("Theories", [])]
        col2 = ((_key(f"{len(theories)} theor{'y' if len(theories) == 1 else 'ies'}") + "".join(theories) if theories else "")
                + ((_key(f"{n} hypothes{'is' if n == 1 else 'es'}: {in_hand} with evidence in hand, {n - in_hand} waiting for a Run")
                    + "".join(hyps)) if hyps else "")) or '<span class=mut>none yet</span>'
        claims = [_mini(f"{esc(c['code'])} · {P.inline(c['said'].split(':', 1)[0])}",
                        P.inline(c["said"].split(":", 1)[1].strip() if ":" in c["said"] else ""),
                        " · ".join(f"{esc(k.capitalize())}: {P.inline(v)}" for k, v in c["more"].items() if k in ("now", "if it fails")))
                  for c in groups.get("Potential claims", [])]
        col3 = (_key(P.inline(_first_sentence(f.get("if answered", "")))) if f.get("if answered") else "") + "".join(claims)
        work = " · ".join(esc(w["code"]) for w in groups.get("Potential work", []))
        body = (_cols([("❓ The question", col1), ("🔮 Theory, and what we expect", col2), ("📣 What the paper can say", col3 or "—")])
                + (f'<p class=mut style="font-size:12.5px;margin:8px 0 0">Work: {work}</p>' if work else ""))
        cards.append(_folded(f'{esc(chip)} <b>{esc(rq)} · {esc(f.get("name", ""))}</b>', P.inline(asked_rq), body, f"story-{rq.lower()}"))
    out = [_sub("The questions"), _story_map(text)] + out + cards
    story = re.search(r"(?ms)^\*\*The narrative, if the questions are answered\*\*.*?\n\n(.*?)(?:\n\s*\n(?=\S)(?!\d+\. )|\Z)", rqs)
    lines = _items(story.group(1)) if story else []
    more = []
    if lines:
        more.append(_folded("<b>📜 The narrative, if the questions are answered</b>", f"{len(lines)} steps",
                            "".join(_line(str(k), P.inline(x)) for k, x in enumerate(lines, 1))))
    stakes = _fields(_division(text, "Stakes"))
    if stakes:
        more.append(_folded("<b>🎯 Stakes</b>", " · ".join(esc(k) for k, _v in stakes), "".join(_line(k, P.inline(v)) for k, v in stakes)))
    nots = _items(bounds.split("**We will not claim**", 1)[1]) if "**We will not claim**" in bounds else []
    if nots:
        more.append(_folded("<b>🚫 What we will not claim</b>", f"{len(nots)} boundaries",
                            '<ul style="margin:0;padding-left:18px">' + "".join(f"<li>{P.inline(x)}</li>" for x in nots) + "</ul>"))
    if ev:
        done = sum(r[-1].lower() == "established" for r in ev)
        more.append(_folded("<b>🧾 The evidence</b>", f"{len(ev)} rows · {done} established",
                            "".join(_line(r[0], f"{P.inline(r[1])} <span class=mut>· {esc(r[-1])}</span>") for r in ev)))
    work = _table(_division(text, "Task Roadmap"), r"T\d+")
    if work:
        done = sum((r[3] if len(r) > 3 else "").lower() == "done" for r in work)
        more.append(_folded("<b>🛠 The work</b>", f"{len(work)} tasks · {done} done",
                            "".join(_line(r[0], f"{P.inline(r[1])} <span class=mut>· {esc(r[3] if len(r) > 3 else '')}</span>") for r in work)))
    venue_div = _division(text, "Venues")
    venues = _table(venue_div, r"V\d+")
    if venues:
        # the venue drawn as the questions' map (JL 261023: "could you make this to be the layout like this as well?"),
        # inside its own card, under the venue list ("this should be within the section, not out of the section")
        more.append(_folded("<b>🧭 Where the story could go</b>", f"{len(venues)} venues · {esc(venues[0][1])} first",
                            "".join(_line(r[0], f"<b>{P.inline(r[1])}</b> <span class=mut>· {esc(r[2])} · leads with "
                                               f"{esc(r[4] if len(r) > 4 else '')}</span>") for r in venues)
                            + _venue_map(venue_div, venues, held)))
    # each venue's frames (the call, how the paper meets it, why it is doable) are read in the map only; their bullet
    # cards were dropped (JL 261023: "I don't need this ... otherwise, this is very hard to read")
    # the Result in subsections (JL 261022): the questions, the narrative, why it matters, the evidence, the venue
    groups = [("The narrative", ("📜",)), ("Why it matters, and its limits", ("🎯", "🚫")),
              ("The evidence and the work", ("🧾", "🛠")), ("The venue", ("🧭",))]
    for title, marks in groups:
        mine = [c for c in more if any(f"<b>{mk}" in c for mk in marks)]
        if mine:
            out += [_sub(title)] + mine
    return "".join(out)


def _board_step(name, topics, state, block, root, d=None):
    """One step: its Operation (Input, Prompt) over its Result (each topic's drawing, opened, then what is open and
    what was decided)."""
    from live.draft_steps import _part, _prompt_box, _step_box
    from live.frame import _draw_url
    emoji, group, word, prompt = BOARD_STEP[name]
    first = topics[0][0].name if topics else f"sNN-{(word or group).lower()}"
    rows = [("Topics", ", ".join(esc(t.name) for t, _x in topics) or f'<span class=mut>none yet in the {esc(group)} group</span>')]
    for topic, text in topics[:1]:
        stage = re.search(r"(?m)^\*\*Stage:\*\*\s*(.*)$", text)
        rows += [("What", esc(_topic_what(text)) or "—"), ("Stage", esc(stage.group(1).strip()) if stage else "—"),
                 ("Decided · Open", f'{len(_topic_lists(text, "Decided"))} · {len(_topic_lists(text, "Open"))}')]
    ask = prompt.format(b=rel(block, root), t=first)
    op = _step_box(f"{emoji} {name}", state, "<h4>Input</h4>" + _kv(rows) + _prompt_box(ask, block, root, f"board-{name.lower()}"))
    # Idea: the ideas themselves, a card each; Story: its parts as sections; to read and review, the drawing folded under
    cards = (_idea_cards(d) if name == "Idea" and d else
             "".join(_story_sections(text) for _t, text in topics) if name == "Story" else
             "".join(_flow_sections(text, root) for _t, text in topics[:1]) if name == "DataFlow" else
             "".join(_flow_sections(text, root, "Paper tree", "The paper, as a tree") for _t, text in topics[:1])
             if name == "PaperFlow" else "")
    result = [cards] if cards else []
    for k, (topic, text) in enumerate(topics):
        k += bool(cards)
        drawing = topic / f"{topic.name}.excalidraw"
        url = _draw_url(drawing, root) if drawing.is_file() else ""
        # the first one starts open, so it loads at once (the frame's loader fills a fold's frame only when it opens)
        frame = (f'<iframe class=st-frame title="{esc(topic.name)}" data-src="{esc(url)}"'
                 + (f' src="{esc(url)}"' if k == 0 else "") + ' referrerpolicy=no-referrer></iframe>'
                 if url else _empty("No drawing yet."))
        # opened straight onto its drawing, no box in a box (JL 261020); under written sections it comes last, after
        # the points open for the person and the decisions
        draw = (f'<details class="topic work-task"{" open" if k == 0 else ""}><summary><span class=related-head>'
                f'<b>🎨 {esc(topic.name)}</b></span>' + (f'<span class=topic-pop>{pop(url, topic.name, "↗")}</span>' if url else "")
                + f'</summary>{frame}</details>')
        opened, decided = _topic_lists(text, "Open"), _topic_lists(text, "Decided")
        lists = ((_folded(f"🙋 Open · {len(opened)}", "", "<ol>" + "".join(f"<li>{P.inline(x)}</li>" for x in opened) + "</ol>")
                  if opened else "")
                 + (_folded(f"✅ Decided · {len(decided)}", "", "<ul>" + "".join(f"<li>{P.inline(x)}</li>" for x in decided) + "</ul>")
                    if decided else ""))
        result.append((_sub("Open, decided, and the drawing") if name == "Story" else "") + (lists + draw if cards else draw + lists))
    return _part("Operation") + op + _part("Result") + ("".join(result) or _empty(f"No {group} topic yet: the prompt above makes {first}."))


def _board_work(d, block, root, sub):
    """Work Details: Idea · Story · DataFlow · PaperFlow, then Jobs, the versions (one send each)."""
    sub = OLD_BOARD_SUBS.get(sub, sub)
    steps = {name: _board_topics(block, BOARD_STEP[name][1], BOARD_STEP[name][2]) for name in BOARD_STEP}
    state = _board_state(steps)
    # an idea still waiting for the person's G0 choice keeps Idea asked, as an open point does
    if state["Idea"] == "done" and any((x.get("verdict") or "⬜").startswith("⬜")
                                      for x in (d.get("ideation") or {}).get("ideas") or []):
        state["Idea"] = "asked"
    s = sub if sub in BOARD_STEPS else next((n for n, v in state.items() if v == "next"), "Jobs")
    if s == "Jobs":                                 # s11: the Board's Jobs, as the base's tree:
        html = (work_tree("Block", d["board"], d["root"], THEME)   # Job → Section → Run → result (b10 s32-D19)
                or _jobs(d, d["board"], d["root"]))
    else:
        html = _board_step(s, steps[s], state[s], block, root, d)
    return Space(html=html, subspaces=BOARD_STEPS, open=s, run_types=_run_cards("Block", "Work Details"))


def _checks(d):
    """The build's checks, as paper.py's Checks view reads them from build-manifest.json."""
    man = d["delivery"]["manifest"] or {}
    if not man:
        return _empty("No build yet.")
    build, sub, rd = man.get("build") or {}, man.get("submission_readiness") or {}, man.get("readiness") or {}
    facts = [("main text", f'{build.get("main_text_words", "?")} words'
                           + (f' · limit {build["main_text_word_limit"]}' if build.get("main_text_word_limit") else "")),
             ("citations", f'{build.get("citations", "?")} cited · {man.get("bib_entries", "?")} bib entries'),
             ("displays", f'{build.get("main_tables", "?")} main table(s) · {build.get("main_figures", "?")} main figure(s)'),
             ("pages ready", f'{rd.get("ready", "?")} of {rd.get("total", "?")}'
                             + (" · not ready: " + ", ".join(P._not_ready_ids(rd)) if rd.get("not_ready") else "")),
             ("submission", str(sub.get("status", "?")) + (" · " + "; ".join(sub.get("blockers") or []) if sub.get("blockers") else ""))]
    if d["delivery"]["stale"]:
        facts.append(("changed since build", ", ".join(d["delivery"]["stale"])))
    g4 = next((v for g, _, v in d.get("gates") or [] if g == "G4"), "")
    if g4:
        facts.append(("G4 compile", g4))
    mark = lambda v: _st(v, "✓" if v else "✗")
    checks = [(esc(k.replace("_", " ")), mark(v) if isinstance(v, bool) else esc(str(v)))
              for k, v in (build.get("checks") or {}).items()]
    render = man.get("render") or {}
    if render:
        checks += [("latexmk", mark(render.get("latexmk_rc") == 0)), ("docx", mark(render.get("docx_rc") == 0))]
    pages = [(esc(p["id"]), mark(p["frag"]), "—" if p["ready"] is None else mark(p["ready"]),
              esc("; ".join(list(p["reasons"]) + list(p["warnings"]) + (["changed since build"] if p["stale"] else []))))
             for p in d["delivery"]["pages"]]
    # engine ≥0.8 writes each unresolved \ref as {"page", "ref"}; older manifests wrote a bare string
    warns = [w if isinstance(w, str) else str(w) for w in man.get("warnings") or []] + [
        "unresolved \\ref: " + (x if isinstance(x, str) else f'{x.get("ref", "?")} ({x.get("page", "?")})')
        for x in man.get("unresolved_refs") or []]
    return (_kv([(k, esc(v)) for k, v in facts]) + table(("check", "result"), checks)
            + "<h3>Pages</h3>" + table(("page", "fragment", "ready", "notes"), pages)
            + ("<h3>Warnings</h3><ul>" + "".join(f"<li>{esc(w)}</li>" for w in warns) + "</ul>" if warns else ""))


def _frame(d, path, title):
    # src with loading=lazy: the frame's loader fills only a .topic row's first iframe, on open
    return f'<iframe class=st-frame title="{esc(title)}" src="{esc(P._tree_url(d, path))}" loading=lazy></iframe>'


def _preview(d, suffix):
    """The paper as built, embedded: the PDF, or for Word its PDF twin under one line naming the .docx
    (the old page's Preview, paper.py _preview_html)."""
    outs = [o for o in P._outputs(d, suffix) if o["exists"]]
    if not outs:
        return _empty("Not built yet.")
    main = next((o for o in outs if "main" in o["what"]), outs[0])
    if suffix == ".pdf":
        return _frame(d, main["path"], main["rel"])
    twin = Path(main["path"]).with_suffix(".pdf")
    line = (f'<p class=mut>{P._file_link(d, main["path"], main["rel"])} · {esc(main["size"])} · {esc(main["stamp"])}'
            + (" · the preview is older than the .docx; rebuild" if twin.is_file() and twin.stat().st_mtime
               < Path(main["path"]).stat().st_mtime else "") + "</p>")
    return line + (_frame(d, twin, main["rel"]) if twin.is_file() else _empty("No preview yet: the next paper build draws it."))


def _artifacts(d, suffix):
    """What the build wrote (the old page's Artifacts): outputs; for LaTeX the printed displays and the
    submission assets, for Word the returned files."""
    dv = d["delivery"]
    rows = [(esc(o["what"]), P._file_link(d, o["path"], o["rel"]) if o["exists"] else esc(o["rel"]),
             _st(o["exists"] and not o["stale"], ("built" + (" · stale" if o["stale"] else "")) if o["exists"] else "not built"),
             esc(o["size"]), esc(o["stamp"])) for o in P._outputs(d, suffix)]
    html = table(("what", "file", "state", "size", "written"), rows)
    if suffix == ".pdf":
        if dv["displays"]:
            html += table(("printed", "declared", "label", "unit", "page"),
                          [(esc(r[0]), esc(r[1]), f"<code>{esc(r[2])}</code>", esc(r[3]), esc(r[4])) for r in dv["displays"]])
        if dv["assets"]:
            html += table(("asset", "size"), [(P._file_link(d, a["path"], a["name"]), esc(a["size"])) for a in dv["assets"]])
    elif dv["returned"]:
        html += table(("returned", "size", "written"),
                      [(P._file_link(d, r["path"], r["rel"]), esc(r["size"]), esc(r["stamp"])) for r in dv["returned"]])
    return html


def _built(d, suffix, checks=True):
    """LaTeX and Word: Preview, then Artifacts (JL 261007: "our previous style", s12); then Checks, unless
    the tab has a Checks view of its own (a version's)."""
    return pv('<h3 class="space-h">Preview</h3>' + _preview(d, suffix)          # the old page's Artifacts, Checks
              + '<h3 class="space-h">Artifacts</h3>' + P._artifacts_html(d, suffix)
              + ('<h3 class="space-h">Checks</h3>' + P._checks_html(d) if checks else ""))


def _cover(d):
    cover = P._cover(d)
    if cover is None:
        return _empty("No cover letter built yet: add a [coverletter] block to delivery/paper-build.toml and run the build.")
    base = d["delivery"]["dir"]
    pdf = (cover.get("outputs") or {}).get("pdf")
    pdf = (base / pdf) if pdf and not Path(pdf).is_absolute() else (Path(pdf) if pdf else None)
    head = (f'<p><b>{esc(cover.get("round") or "letter")}</b> · {"ready" if cover.get("ready") else "not ready"}'
            + (f' · {pop(P._tree_url(d, pdf), "cover letter", "Open the letter ↗")}' if pdf and pdf.is_file() else "") + "</p>")
    rows = [(esc(c.get("check", "")), _st(c.get("ok"), "✓" if c.get("ok") else "⚠"), esc(c.get("detail", "")))
            for c in cover.get("checks") or []]
    return head + table(("check", "", "detail"), rows)


def _rounds(d):
    return pv(P._round_cards(d))                                   # the old Round cards (JL 261007)


def _rounds_table(d):
    rows = [(esc(r["stem"]), esc(r["kind"]), esc(" · ".join(x for x in (r["from"], r["at"]) if x)), esc(r["due"] or "—"),
             esc(r["state"] or "—"), P._link(d, r["rel"], "Open ↗")) for r in d["delivery"]["rounds"]]
    return table(("round", "kind", "received", "response due", "state", ""), rows) if rows else _empty("No round yet.")


VERSION_DELIVERY = ("LaTeX", "Word", "Cover letter", "Checks")      # the Board's; a version's is cards


def section_states(board: Path, version: Path) -> list:
    """Each Section of one version's build, from its build-manifest.json (JL 261011: "how could the delivery from
    the section level link back to the block level delivery"): (Section folder, ready, why not, fragment, state),
    state ✅ when the fragment is older than the build, ❗ when it changed after it, ⬜ when it was never exported."""
    import json
    from datetime import datetime
    man_path = delivery_dir(version) / "build-manifest.json"
    try:
        man = json.loads(man_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    try:
        built = datetime.fromisoformat(str(man.get("built") or "")).timestamp()
    except ValueError:
        built = None
    out = []
    for page in man.get("pages") or []:
        sid = str(page.get("id") or "")
        frag = board / str(page.get("fragment") or "") if page.get("fragment") else None
        if frag is None or not frag.is_file():
            state = "⬜ not exported"
        elif built is not None and frag.stat().st_mtime > built:
            state = "❗ changed after the build: rebuild"
        else:
            state = "✅ in the build"
        out.append((version / sid, bool(page.get("ready")), "; ".join(page.get("reasons") or []), frag, state,
                    str(man.get("built") or "")[:16].replace("T", " ")))
    return out


def _section_rows(board: Path, versions, root: Path) -> str:
    """The Sections of each version's build as one table: Section (its part of the Delivery), ready, in the build."""
    from live.frame import ROUTE, href
    from urllib.parse import urlencode
    rows = []
    for v in versions:
        for sec, ready, why, frag, state, built in section_states(board, v):
            rows.append((link(href(sec, root, THEME, "Delivery"), f"{v.name.split('_', 1)[0]} › {sec.name}"),
                         esc("✅ ready" if ready else "✗ " + (why or "not ready")),
                         esc(f"{state} · built {built}" if built else state),
                         link(ROUTE + "?" + urlencode({"path": rel(sec, root)}), "folder ↗")))
    return table(("Section", "ready at the build", "in the build", "back to"), rows) if rows else ""


def _version_delivery(d, board, job, root):
    """A version's Delivery as folding item cards, no third row (JL 261007: "item card based", s12): Manuscript
    (the PDF, the Word file), Letters (the cover letter), Checks (submission readiness), Sent (each frozen send)."""
    dv = d["delivery"]
    if dv["dir"] is None:
        return Space(html=_empty("No delivery/ yet: Build writes it."), run_types=_delivery_runs())
    cards = delivery_view(job, root, THEME)         # the manuscript, the letters: one card per result (b10 s32-D18)
    out = []
    for suffix, kind in ((".pdf", "LaTeX"), (".docx", "Word")) if not cards else ():
        main = next((o for o in P._outputs(d, suffix) if "main" in o["what"]), None) or \
            next(iter(P._outputs(d, suffix)), None)
        if main is None:
            continue
        meta = " · ".join(x for x in (("built" if main["exists"] else "not built"), "stale" if main["stale"] else "",
                                      main["size"], main["stamp"]) if x)
        body = _preview(d, suffix)
        if suffix == ".pdf" and dv["displays"]:
            body += table(("printed", "label", "from the Section"),
                          [(esc(r[0]), f"<code>{esc(r[2])}</code>", esc(r[4])) for r in dv["displays"]])
        out.append(("Manuscript", _fold(f"{esc(Path(main['rel']).name)} · {kind}", esc(meta), body,
                                        P._file_link(d, main["path"], "↗") if main["exists"] else "")))
    if cards and dv["displays"]:                    # what the PDF prints, kept beside the cards
        out.append(("Manuscript", _fold("displays in the build", esc(f'{len(dv["displays"])} printed'),
                                        table(("printed", "label", "from the Section"),
                                              [(esc(r[0]), f"<code>{esc(r[2])}</code>", esc(r[4])) for r in dv["displays"]]))))
    cover = P._cover(d)                             # with cards, a built cover letter is one of them
    if not cards and cover is not None:
        pdf = (cover.get("outputs") or {}).get("pdf")
        pdf = (dv["dir"] / pdf) if pdf and not Path(pdf).is_absolute() else (Path(pdf) if pdf else None)
        body = _frame(d, pdf, "cover letter") if pdf and pdf.is_file() else _empty("Not built yet.")
        out.append(("Letters", _fold("cover letter", esc(("built" if pdf and pdf.is_file() else "not built") + " · "
                                                         + ("ready" if cover.get("ready") else "not ready")), body)))
    elif not cards:
        out.append(("Letters", _fold("cover letter", "not built", _empty(
            "No cover letter built yet: add a [coverletter] block to delivery/paper-build.toml and run the build."))))
    sections = _section_rows(board, [job], root)
    if sections:
        out.append(("Sections", sections))
    man = dv["manifest"] or {}
    rd = man.get("readiness") or {}
    g4 = next((v for g, _, v in d.get("gates") or [] if g == "G4"), "")
    meta = " · ".join(x for x in (str(man.get("status", "no build")), f'{rd.get("ready", "?")} of {rd.get("total", "?")} '
                                  "Sections ready" if rd else "", f"G4 {g4.split(' · ')[0]}" if g4 else "") if x)
    out.append(("Checks", _fold("submission readiness", esc(meta), _checks(d))))
    for frozen in sorted(x for b in _version_round_pages(board, job) for kind in ("sent", "released")
                         for x in (b.parent / kind).glob("*/") if x.is_dir()):
        files = sorted(f for f in frozen.rglob("*") if f.is_file() and not f.name.startswith("."))
        body = table(("file", "size"), [(P._file_link(d, f, f.relative_to(frozen).as_posix()), esc(P._size(f)))
                                        for f in files[:40]]) + (f"<p class=mut>and {len(files) - 40} more</p>"
                                                                if len(files) > 40 else "")
        out.append(("Sent", _fold(f"{frozen.parent.name}/{frozen.name}", f"frozen · {frozen.parent.parent.name} · "
                                  f"{len(files)} files", body)))
    html, last = cards, ""
    for group, card in out:
        html += (f"<h3>{esc(group)}</h3>" if group != last else "") + card
        last = group
    return Space(html=html, run_types=_delivery_runs())


def _delivery_runs():
    """Build · Check (Send stays a proposal, s12)."""
    return _run_cards("Job", "Delivery")


def _delivery(d, sub, opts=("delivery/", "LaTeX", "Word", "Cover letter", "Rounds"), board=None, root=None):
    s = _pick(sub, opts)
    if s == "delivery/":                            # every result of the Board, as the base's cards (b10 s32-D18)
        html = (delivery_view(board, root, THEME) if board is not None and root is not None else "") or \
            _empty("No delivery/ yet.")
    elif s in ("LaTeX", "Word"):
        html = (_empty("No delivery/ yet.") if d["delivery"]["dir"] is None else
                _built(d, ".pdf" if s == "LaTeX" else ".docx", checks="Checks" not in opts))
        if board is not None and root is not None:      # each version's Sections, in the build or not
            versions = [v for v in sorted(board.glob("j[0-9][0-9]_*/")) if (delivery_dir(v) / "build-manifest.json").is_file()]
            rows = _section_rows(board, versions, root)
            html += ('<h3 class="space-h">Sections in the build</h3>' + rows) if rows else ""
    elif s == "Cover letter":
        html = _cover(d)
    elif s == "Checks":
        html = _empty("No delivery/ yet.") if d["delivery"]["dir"] is None else _checks(d)
    else:
        html = _rounds(d)
    return Space(html=html, subspaces=opts, open=s, run_types=_delivery_runs())


# ── a Section: the base's Page Task, and the paper's four lines over it (◆, b16 s13, JL 261007) ──
# ── a version (Job), from s12: one send of the paper ────────────────────────────────────────────────
# Today a Job is one group folder (Ba-/Bb-/Bc-<desk>-<part>, level_patterns); on the ladder it is one
# version folder (jNN_v<N>_<desk>/) holding every Section and Round of one send. Either way its Pages are
# the Board's ## Pages entries under it, read through paper.collect() of the Board.
VERSION_AR = ("Questions", "Draft-Main", "Draft-Appendix", "Comments", "Cover letter")
VERSION_WD = ("All", "Main", "Appendix", "Letters")
# the five standing questions of a send (s12, the Job session): the question, what answers it
STANDING = (("J1", "What is the one-minute story?", "the telling's face, studio/sNN-story-… · this version's Abstract and Introduction"),
            ("J2", "Why this venue?", "venues/<venue>/call.md · the venue's playbook"),
            ("J3", "Which writing principles does it follow?", "the playbook's style · By reader expectations"),
            ("J4", "Is it ready to send?", "every Section's CHECK · Delivery › Checks (G4)"),
            ("J5", "What changed since the last send?", "a revision only: the comments report's Review Items"))


def _mine(board, job, rel_):
    """Whether a Page (its path relative to the Board) sits under this Job's folder."""
    return bool(rel_) and Path(rel_).parts[0] == job.relative_to(board).parts[0]


def _version_rows(d, board, job):
    return [r for r in P.section_rows(d) if r["page"] and _mine(board, job, r["page"]["rel"])]


def _version_round_pages(board, job):
    """The review batches of this send: today the Board's Bc-<desk>-Round/RD<NN>-…/, on the ladder the version's
    own RD<NN>-…/ and CM<NN>-…/ (haipipe-paper-comments)."""
    found = (list(board.glob("B[a-z]-*-Round/RD*/RD*.md")) + list(job.glob("RD*/RD*.md"))
             + [q for q in job.glob("reports/q[0-9][0-9]_*/q[0-9][0-9]_*.md")      # a comments report (JL 261007)
                if re.search(r"(?m)^page-type:\s*(comments|round)\b", q.read_text(encoding="utf-8", errors="replace"))]
             + list(job.glob("CM*/CM*.md")))                     # t3N_ is Letters (a cover letter), never comments
    return sorted({q.resolve() for q in found if q.stem == q.parent.name})


def _letter_pages(job):
    """The send's letters, its t3N_ Page Tasks (t31 cover letter, t32 response), in number order (s12)."""
    return sorted(q for q in job.glob("t3[0-9]_*/t3[0-9]_*.md") if q.stem == q.parent.name)


def _md_table(text, heading):
    """The first table under the first heading that names `heading`: (head, rows), lowercase head."""
    m = re.search(rf"(?ms)^#+[^\n]*{re.escape(heading)}[^\n]*\n(.*?)(?=^#+ |\Z)", text)
    lines = [l for l in (m.group(1).splitlines() if m else []) if l.startswith("|")]
    rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in lines]
    rows = [r for r in rows if not all(set(c) <= set("-: ") for c in r)]
    return ([h.lower() for h in rows[0]], rows[1:]) if rows else ([], [])


def _comments(board, job, root):
    """Comments (s12) as the old page's item cards (JL 261007: "All the things to be the card"): one card per
    Review Item (cites · lands on · its state; opened, its work and reply), or, until a batch lists them, one per
    concern of its Feedback Concern Table."""
    cards = []
    for page in _version_round_pages(board, job):
        text = page.read_text(encoding="utf-8", errors="replace")
        opener = pop(reader(page, root), page.stem, page.stem + " ↗")
        head, body = _md_table(text, "Review Items")
        if body:
            for r in body:
                x = dict(zip(head, r))
                state = x.get("state", "") or "open"
                cards.append(P._card("item-" + x.get("item", ""), "Review", x.get("item", ""),
                                     esc("cites " + x.get("cites", "")), esc(x.get("lands on", "")), state,
                                     P._status_cls("✅" if state in ("answered", "applied") else state),
                                     [("work", esc(x.get("work", "") or "—")), ("reply", esc(x.get("reply", "") or "no reply yet")),
                                      ("comments", opener)], key=x.get("item", "")))
            continue
        head, body = _md_table(text, "Concern Table")
        for r in body:
            x = dict(zip(head, r))
            # one line on top (JL 261008: "this is the disaster"): the concern in full, its source under it, its
            # state; the route and the rest go inside, links rendered, so nothing squeezes the concern
            src = next((x[k] for k in ("source", "from", "raised by") if x.get(k)), "")
            cards.append(P._card("concern-" + x.get("item", ""), x.get("item", "") or "point",
                                 x.get("concern", ""), esc(src), "",
                                 x.get("state", "") or "open", P._status_cls(x.get("state", "")),
                                 [(k, P.inline(v)) for k, v in x.items() if v and k not in ("item", "concern")]
                                 + [("comments", opener)]))
    return pv(P._cards(cards, "No Review Items yet: a comments report's points land here, each with where it goes "
                              "and its reply."))


def _version_description(d, board, job, root, sub):
    opts = ("Version", "Venue rules")
    s = _pick(sub, opts)
    rows = _version_rows(d, board, job)
    if s == "Version":
        face = job / f"{job.name}.md"
        head = _header(face) if face.is_file() else {}       # the version's face (g03 D6): send · desk · venue …
        states = {}
        for r in rows:
            states[P._state_word(r["state"])] = states.get(P._state_word(r["state"]), 0) + 1
        html = _kv([("send", esc(head.get("send") or job.name)), ("desk", esc(head.get("desk") or P.paper_desk(d) or "—")),
                    ("venue", esc(head.get("venue") or P.venue_name(d) or "—"))]
                   + [(k, esc(head[k])) for k in ("state", "tells", "from", "responds-to", "answers") if head.get(k)] + [
                    ("Sections", esc(f"{len(rows)}: " + " · ".join(f"{n} {w}" for w, n in states.items()) if rows else "none")),
                    ("review batches", esc(str(len(_version_round_pages(board, job))))),
                    ("face", link(reader(face, root), face.name) if face.is_file()
                     else '<span class=mut>none yet: a version gets its own face on the ladder (jNN_v&lt;N&gt;_&lt;desk&gt;.md)</span>')])
    else:
        calls = sorted((board / "venues").glob("*/call.md"))
        html = (table(("venue", "call"), [(link(reader(c, root), c.parent.name), esc(rel(c, root))) for c in calls])
                if calls else f'<p>Venue: <b>{esc(P.venue_name(d) or "—")}</b> (from the Story).</p>'
                              + _empty("No venues/<venue>/call.md yet: its rules are read from there (b16 Q02)."))
    return Space(html=html, subspaces=opts, open=s, run_types=_run_cards("Job", "Description", s))


def _standing(d, job, root):
    """The send's questions as b03's own question row (JL 261007: the base frame's question_rows, "Q03 … │ no work
    yet │ report title ↗, answer, drawing thumbnail, report q03 · open"): the version's register (its ## Questions,
    a comments report among them), then the standing J1-J5 not asked there yet (J5 only for a revision), drawn in
    the same markup."""
    face = job / f"{job.name}.md"
    text = face.read_text(encoding="utf-8", errors="replace") if face.is_file() else ""
    rows = [_brow(qid, t, "not asked yet", "", f'<p class=mut>{esc(w)}</p>',
                  '<p class=mut>no report yet · Ask a Question writes it into ## Questions with its report</p>')
            for qid, t, w in STANDING
            if not re.search(rf"\b{qid}\b", text) and (qid != "J5" or re.search(r"(?m)^from:\s*j\d", text))]
    base = _base_rows(job, root)                    # the standing rows continue under the base's own head
    html = base + (("" if "q-head-row" in base else _HEAD) + "".join(rows) if rows else "")
    return html or _empty("No question yet: Ask a Question.")


# ── Draft-Main · Draft-Appendix (s12, JL 261007): one Question │ Work │ Report row per Section, in reading
# order; opened, the rendered draft and the Section's logic + narrative drawing side by side, both view only
WRITING_RUN = re.compile(r"^run-(section|write|writing|content|structure|revise)")


def _cell(heads, cells, *names):
    """The first §8 cell whose header holds one of `names`, or ""."""
    for n in names:
        for i, h in enumerate(heads):
            if n in h.lower() and i < len(cells) and cells[i].strip() not in ("", "—", "-"):
                return cells[i].strip()
    return ""


PARA = re.compile(r"(?m)^#{3,4} +((?:C\d+\.)?P\d+)\b.*$")      # ### C1.P1 · … (a draft) · #### P1. … (a face)


def _paragraphs(folder, stem):
    """(planned, written) paragraphs: planned from the newest draft's Structure part, written = those with
    prose under its Draft part; a face that keeps its words in ## Content counts there."""
    def version(f):
        m = re.search(r"-draft-v([\d.]+)\.md$", f.name)
        return tuple(int(x) for x in m.group(1).split(".") if x) if m else ()
    drafts = sorted(folder.glob(f"draft/{stem}-draft-v*.md"), key=version)
    text = drafts[-1].read_text(encoding="utf-8", errors="replace") if drafts else ""
    parts = dict((m.group(1).lower(), m.start()) for m in re.finditer(r"(?m)^## +\d+ · (\w+)", text))
    cut = lambda a: text[parts[a]:min([v for v in parts.values() if v > parts[a]] or [len(text)])] if a in parts else ""
    planned = list(dict.fromkeys(PARA.findall(cut("structure") or text)))
    prose = lambda body: [i for i, b in zip(PARA.findall(body), PARA.split(body)[2::2]) if b.strip()]
    written = set(prose(cut("draft")))
    face = folder / f"{stem}.md"
    if not written and face.is_file():
        body = face.read_text(encoding="utf-8", errors="replace").partition("\n## Content")[2].split("\n## ", 1)[0]
        written = set(prose(body))
        planned = planned or list(dict.fromkeys(PARA.findall(body)))
    return len(planned), len(written)


def _section_name(r):
    """A Section's reader-facing name: 'Literature review' from t02_literature-review or S-…-2-Literature-Review."""
    m = P.TASK_STEM.match(r["id"]) if hasattr(P, "TASK_STEM") else None
    name = m.group(2) if m else (r["name"] or r["id"])
    name = name.replace("-", " ").replace("_", " ").strip()
    return name[:1].upper() + name[1:]


def _draft_work(folder, stem):
    """Work, one line: the evidence it binds, and how much of its plan is written."""
    items = [i for i in P._page_items(folder, stem) if not i["retired"]]
    count = lambda *t: sum(1 for i in items if i["type"] in t)
    planned, written = _paragraphs(folder, stem)
    ev = " · ".join(f"{n} {w}" for n, w in ((count("CITE"), "cite"), (count("VALUE"), "value"),
                                             (count("DISPLAY", "TABLE"), "display")) if n) or "no evidence yet"
    return f'{esc(ev)}<br><span class=mut>{written} of {planned or "?"} ¶ written</span>'


def _draft_links(d, folder, stem, root):
    """The rendered draft and the logic drawing, each a pop-out link, only when it exists."""
    out = []
    web = delivery_read_lane_dir(folder, "web") / "index.html"
    if web.is_file():
        out.append(pop(P._tree_url(d, web), f"{stem} · draft", "draft ↗"))
    drawing = next((x for x in [folder / "studio" / f"{stem}-sections.excalidraw"]
                    + sorted(folder.glob("studio/*.excalidraw")) if x.is_file()), None)
    if drawing is not None:
        out.append(pop("/_excalidraw/?" + P.urlencode({"board": rel(drawing, root)}), f"{stem} · drawing", "drawing ↗"))
    return " · ".join(out)


def _draft_rows(d, board, root, rows):
    """Draft-Main / Draft-Appendix (s12, JL 261007): the paper as read, one line per Section in reading order,
    Question │ Work │ Report in one plain table (as the old Sections list: no nested boxes, no filler)."""
    from live.frame import ROUTE
    out = []
    for r in rows:
        folder = (board / r["page"]["rel"]).parent
        heads, cells = r["heads"], (r["row"] or {}).get("cells") or []
        ask = _cell(heads, cells, "reader question", "question", "job")
        claims = _cell(heads, cells, "must establish", "claim")
        tab = ROUTE + "?" + P.urlencode({"path": rel(folder, root)})
        question = (f'<b>{link(tab, _section_name(r))}</b>'
                    + (f'<br><span class=mut title="{esc(("carries: " + claims) if claims else "")}">{esc(ask)}</span>'
                       if ask else ""))
        checks = sorted(folder.glob("runs/run-check-*.md"))
        links = _draft_links(d, folder, r["id"], root)
        report = (esc(P._state_word(r["state"]) or "—") + (" · " + _st(True, "checked") if checks else "")
                  + (f'<br><span class=mut>{links}</span>' if links else ""))
        out.append((esc(r["num"] or "·"), question, _draft_work(folder, r["id"]), report))
    return table(("#", "Section · what it must answer", "Work", "Report"), out) if out else ""


# ── Cover letter (JL 261007, s12): the letter as the editor reads it, one row per paragraph ───────────────
from host_paths import skill_dir  # noqa: E402
ASSEMBLE = skill_dir("haipipe-paper-assemble") / "scripts"      # a skill, or a part of haipipe-paper
LETTER = (("¶1 · what we submit", "the version's face: title · article type · venue", ("submit", "what we", "manuscript")),
          ("¶2 · the one-minute story", "J1 · the one-minute story", ("story", "one-minute", "contribution", "finding")),
          ("¶3 · why this venue", "J2 · why this venue", ("venue", "fit", "journal", "why")),
          ("¶4 · declarations", "venues/<venue>/call.md: originality · conflicts · data · funding",
           ("declar", "conflict", "original", "funding", "data")),
          ("¶5 · suggested reviewers", "only when the venue asks", ("reviewer",)))

def _letter_words(board, job):
    """(paragraphs as [(heading, text)], the page that holds them, content | draft): from the version's cover
    letter Task (t3N_), else its batches, through haipipe-paper-assemble's own reader (cover_letter.py)."""
    import importlib.util
    try:
        spec = importlib.util.spec_from_file_location("cover_letter", ASSEMBLE / "cover_letter.py")
        C = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(C)
    except Exception:
        return [], None, ""
    pages = ([q for q in _letter_pages(job) if "cover" in q.stem] + _version_round_pages(board, job)
             + sorted(job.glob("t*_cover_letter*/t*_cover_letter*.md")))
    for page in pages:                              # the page's Content first, then its drafts, newest first
        drafts = sorted(page.parent.glob("draft/*-draft-v*.md"), key=C._draft_version, reverse=True)
        for src, where in [(page, "content")] + [(x, "draft") for x in drafts]:
            text = src.read_text(encoding="utf-8", errors="replace")
            heads = list(C.HEAD.finditer(text))
            top = next((i for i, h in enumerate(heads) if "cover letter" in h.group(2).lower()), None)
            if top is None:
                continue
            level, end, subs = len(heads[top].group(1)), len(text), []
            for h in heads[top + 1:]:
                if len(h.group(1)) <= level:
                    end = h.start()
                    break
                subs.append(h)
            named = []                              # each paragraph with the sub-heading above it, if any
            for k, cut in enumerate([heads[top]] + subs):
                stop = subs[k].start() if k < len(subs) else end
                body = text[cut.end():stop]
                named += [("" if k == 0 else cut.group(2).strip(), w) for w in (C.division("## x\n" + body, "x") or [])]
            if named:
                return named, src, where
    return [], None, ""


def _cover_letter(d, board, job, root):
    """One card per paragraph (what it says · the question or rule it answers; opened, its text), then the built
    letter embedded (Delivery › Cover letter keeps its files
    and checks)."""
    paras, src, where = _letter_words(board, job)
    cover = P._cover(d) or {}
    state = ("ready" if cover.get("ready") else "not ready") if cover else "not built"
    headed = any(h for h, _ in paras)
    used, rows = set(), []
    for n, (slot, work, keys) in enumerate(LETTER):
        if headed:                                  # a paragraph answers the row its sub-heading names
            i = next((k for k, (h, _) in enumerate(paras) if k not in used and any(x in h.lower() for x in keys)), None)
            if i is not None:
                used.add(i)
            rows.append((slot, work, paras[i][1] if i is not None else ""))
        else:                                       # no sub-headings: the paragraphs in order, unmapped
            rows.append((slot, "—" if n < len(paras) else work, paras[n][1] if n < len(paras) else ""))
            used.add(n)
    rows += [(f"¶{k + 1} · {h or '—'}", "—", t) for k, (h, t) in enumerate(paras) if k not in used]
    body = pv(P._cards([P._card(f"para-{k}", slot.split(" · ")[0], slot.split(" · ", 1)[-1], esc(work), "",
                                "written" if text else "not written yet", "ok" if text else "mut", [],
                                body=f"<p>{esc(text)}</p>" if text else "") for k, (slot, work, text) in enumerate(rows)],
                       "No paragraph yet."))                # one card per paragraph (JL 261007: cards)
    source = (f'<p class=mut>words from {pop(reader(src, root), src.stem, src.name + " ↗")}'
              f' ({"its Content" if where == "content" else "its latest draft"}) · the letter: {esc(state)}</p>'
              if src else '<p class=mut>No letter yet: its words go in the cover letter Task (t31_cover-letter) '
                          'or the submission batch\'s <b>### Cover letter</b> division. The letter: ' + esc(state) + '</p>')
    pdf = (cover.get("outputs") or {}).get("pdf")
    base = d["delivery"]["dir"]
    pdf = (base / pdf) if pdf and base is not None and not Path(pdf).is_absolute() else (Path(pdf) if pdf else None)
    built = ("<h3>The letter as built</h3>" + _frame(d, pdf, "cover letter") if pdf and pdf.is_file()
             else "<h3>The letter as built</h3>" + _empty("Not built yet: Delivery › Cover letter builds it."))
    return source + body + built


def _version_report(d, board, job, root, sub):
    s = _pick(sub, VERSION_AR)
    if s == "Questions":
        html = _standing(d, job, root)
    elif s in ("Draft-Main", "Draft-Appendix"):
        part = "main" if s == "Draft-Main" else "appendix"
        rows = [r for r in _version_rows(d, board, job) if r["part"] == part]
        html = pv(P._cards(P._narrative_cards(d, rows), f"No {part} Section in this send."))
    elif s == "Cover letter":
        html = _cover_letter(d, board, job, root)
    else:
        html = _comments(board, job, root)
    return Space(html=html, subspaces=VERSION_AR, open=s, run_types=_run_cards("Job", "Audience Report", s))


def _version_work(d, board, job, root, sub):
    s = _pick(sub, VERSION_WD)
    rows = _version_rows(d, board, job)
    if s == "Letters":                              # the letters are t3N_ Page Tasks; the comments are reports
        from live.frame import ROUTE
        cards = []
        for q in _letter_pages(job):
            h = _header(q)
            tab = ROUTE + "?" + P.urlencode({"path": rel(q.parent, root)})
            cards.append(P._card("letter-" + q.stem, "Letter", q.stem,
                                 "to the editor" if "cover" in q.stem else "to the reviewers" if "respon" in q.stem else "",
                                 "", P._state_word(h.get("state", "")) or h.get("state", "") or "—", "mut",
                                 [("open", link(tab, "the Task tab ↗")), ("face", pop(reader(q, root), q.stem, q.name + " ↗"))]))
        for q in _version_round_pages(board, job):
            h = _header(q)
            cards.append(P._card("comments-" + q.stem, "Comments", q.stem, "the comments a response answers", "",
                                 h.get("state", "") or "open", "mut", [("report", pop(reader(q, root), q.stem, q.name + " ↗"))]))
        html = pv(P._cards(cards, "No letter Task yet: t31_cover-letter (to the editor) and, in a revision, "
                                  "t32_response (to the reviewers), each a Page Task like a Section."))
    elif s == "All":                                # every Section, ✎ Write on each, its Runs and what they found (b10 s32-D19)
        html = work_tree("Job", job, root, THEME) or pv(P._section_table(d, rows))
    else:
        html = pv(P._section_table(d, [r for r in rows if r["part"] == s.lower()]))
    return Space(html=html, subspaces=VERSION_WD, open=s,
                 run_types=_run_cards("Job", "Work Details", None if s == "All" else s))


def version_spaces(job, root, sub):
    """The version tab (s12): a send's Description, Audience Report, Work Details, Runs and Delivery."""
    board = next((q for q in job.parents if (q / "board.md").is_file()), None)
    if board is None:
        return {}
    d = _data(board, root, job)
    # two versions may hold the same Section names (j02 starts as a copy of j01): this tab reads its own
    d = dict(d, sections=[p for p in d["sections"] if p["rel"] and _mine(board, job, p["rel"])])
    if delivery_dir(job).is_dir():                 # on the ladder each version builds its own (g03 D4)
        d = dict(d, delivery=P.delivery_info(d, delivery_dir(job)))
    return _disk_version(d, board, job, {"Description": _version_description(d, board, job, root, sub),
                                         "Audience Report": _version_report(d, board, job, root, sub),
                                         "Work Details": _version_work(d, board, job, root, sub),
                                         "Runs": Space(run_types=_run_cards("Job", "Runs")),
                                         "Delivery": _version_delivery(d, board, job, root)})


# ── an older Board's Story group (A1-Story/, an earlier j00_story/) read as a Job; on the ladder the Story is
# studio topics and Questions (b16 Q04) and this view is not reached ─────────────────────────────────────
STORY_AR = ("Ideation", "Narrative")


def _story_pages(d, board, job):
    return [p for p in d["pages"] if p["rel"] and _mine(board, job, p["rel"]) and p["stem"].startswith("Story")]


def story_spaces(job, root, sub):
    """The Story Job: its Ideation and Story Pages as Tasks; the Board's Ideation and Narrative views read here
    too, since the Story is what every version tells. It builds nothing."""
    from dataclasses import replace
    board = next((q for q in job.parents if (q / "board.md").is_file()), None)
    if board is None:
        return {}
    d = _data(board, root)
    pages = _story_pages(d, board, job)
    current = {x["stem"] for x in P.current_stories(d)}
    kind = lambda stem: "ideation" if stem.startswith("Story00") else "current Story" if stem in current else "Story"
    desc = _kv([("Job", esc(job.name)), ("kind", "the Story (a reference Job: every version tells it)"),
                ("story-current", esc(", ".join(sorted(current)) or "—")), ("Pages", esc(str(len(pages))))])
    work = table(("Page", "kind", "state", ""),
                 [(esc(p["stem"]), esc(kind(p["stem"])), esc(P._state_word(P.scalar(p["text"], "state", "")) or "—"),
                   pop(reader(board / p["rel"], root), p["stem"], "Open ↗")) for p in pages])         if pages else _empty("No Story Page in this Job.")
    report = _report(d, board, root, _pick(sub, STORY_AR))
    return {"Description": Space(html=desc, subspaces=("Story",), open="Story"),
            "Idea Studio": _studio(d, board, root),
            "Audience Report": replace(report, subspaces=STORY_AR),
            "Work Details": Space(html=work, subspaces=("Pages",), open="Pages",
                                  run_types=_run_cards("Block", "Audience Report", "Ideation")),
            "Runs": Space(run_types=_run_cards("Block", "Runs")),
            "Delivery": Space(html=_empty("A Story builds nothing: a version Job tells it and builds the paper."))}


def _jobs(d, board, root):
    """The Board's Jobs: today's groups or the ladder's versions, each with its Pages and a link to its tab."""
    from live.frame import ROUTE
    from urllib.parse import urlencode
    rows = []
    for g in d["groups"]:
        folder = board / g["folder"] if g["folder"] else None
        if not folder or not folder.is_dir():
            continue
        kind = ("story (reference)" if g["folder"].startswith(("A1-", "j00_")) else
                "rounds" if g["folder"].startswith("Bc-") else "send")
        rows.append((link(ROUTE + "?" + urlencode({"path": rel(folder, root)}), g["folder"]), esc(kind),
                     esc(len(g["stems"]))))
    return table(("Job", "kind", "Pages"), rows) if rows else _empty("No Job yet.")


SECTION_SKILL = skill_dir("haipipe-paper-draft")
READINESS = Path(__file__).resolve().parents[2] / "skills/2_theme/paper/haipipe-paper/ref/submission-readiness.md"
CONTRACT = ("reader-question", "entry-state", "exit-state", "must-establish", "must-refuse", "transition-in",
            "transition-out", "story-row", "section_kind", "structure-source", "structure-division")
SUB_PREFIX = {"introduction": "SUB-INTRO", "methods": "SUB-METHOD", "results": "SUB-RESULT", "discussion": "SUB-DISC"}


def _header(md):
    """The face's `key: value` lines above its first `## ` heading."""
    out = {}
    for line in (md.read_text(encoding="utf-8", errors="replace").splitlines() if md else []):
        if line.startswith("## "):
            break
        key, sep, value = line.partition(":")
        if sep and key.strip() and " " not in key.strip():
            out[key.strip()] = value.strip()
    return out


def _contract(md):
    """◆ Scope: the reader contract, read from the face's header (haipipe-paper-draft's fields)."""
    head = _header(md)
    rows = [(esc(k), esc(head[k]) if head.get(k) else '<span class=mut>—</span>') for k in CONTRACT]
    return ('<h3>◆ The reader contract</h3><p class=mut>read from the face\'s header; a stale story-row sends '
            'the Section back to its Story</p>' + table(("field", "value"), rows))


def _sub_rows(md):
    """◆ Requirement: the Section's SUB-* rows (submission-readiness.md), by its section_kind, folded."""
    prefix = SUB_PREFIX.get(_header(md).get("section_kind", "").strip().lower())
    if not prefix or not READINESS.is_file():
        return ""
    rows = [[c.strip().strip("`") for c in line.strip().strip("|").split("|")]
            for line in READINESS.read_text(encoding="utf-8", errors="replace").splitlines()
            if line.startswith(f"| `{prefix}-")]
    body = table(("id", "criterion", "axes"), [(esc(r[0]), esc(r[1]), esc(r[2])) for r in rows if len(r) > 2])
    return (f'<details class=topic><summary><b>◆ {esc(prefix)}-* · this Section at submission</b>'
            f'<span class=topic-meta>{len(rows)} rows, judged on the four axes at G4</span></summary>'
            f'<div style="padding:8px 14px">{body}</div></details>')


def _ready(folder, md):
    """◆ Delivery: ready for the build (outline approved · every display has preview.pdf · its PDF
    compiles), shown apart from done (the Page CHECK)."""
    stem = md.stem if md else folder.name
    try:
        from src.outline_version import latest_outline, plan_dir
        plan = latest_outline(plan_dir(folder), stem)
    except Exception:
        plan = None
    approved = _header(plan).get("approved", "") if plan else ""
    units = sorted(d for d in folder.glob("results/run-display-*/payload/Display*") if d.is_dir())
    previews = sum((d / "preview.pdf").is_file() for d in units)
    pdf = (delivery_read_lane_dir(folder, "latex") / f"{stem}.pdf").is_file()
    checks = sorted(folder.glob("runs/run-check-*.md"))
    lights = [_st(bool(approved) and not approved.startswith("⬜"), "outline approved"),
              _st(previews == len(units), f"displays with preview.pdf: {previews} of {len(units)}"),
              _st(pdf, f"{stem}.pdf compiles")]
    done = (f"the Page CHECK {esc(checks[-1].stem)}, its verdict in Runs" if checks
            else "no Page CHECK yet")
    # a card group, as the base's Delivery cards (div.topic > .st-bar), before its lanes (JL 261007)
    return ('<h2>◆ Ready</h2>'
            f'<div class=topic><div class=st-bar><span><b>ready for the build</b> {" · ".join(lights)}</span></div></div>'
            f'<div class=topic><div class=st-bar><span><b>done</b> <span class=mut>{done}; the version\'s '
            f'submit (G4) is the Job\'s</span></span></div></div>')


def _round_pages(folder):
    """The comments of this Section's version (haipipe-paper-comments): a report of type comments in the
    version's reports/qNN_<kind>-<MMDD>/ (JL 261007: "a special type of report … in the reports/"), and
    the older layouts still read: RD<NN>-… and CM<NN>-… in the Board's B<x>-<desk>-Round/ or the version."""
    board, version = folder.parent.parent, folder.parent
    found = [p for kind in ("RD", "CM") for p in list(board.glob(f"B[a-z]-*-Round/{kind}*/{kind}*.md"))
             + list(version.glob(f"{kind}*/{kind}*.md"))]
    found += [q for q in version.glob("reports/q[0-9][0-9]_*/q[0-9][0-9]_*.md")   # a comments report (JL 261007)
              if re.search(r"(?m)^page-type:\s*(comments|round)\b", q.read_text(encoding="utf-8", errors="replace"))]
    return sorted({p.resolve() for p in found if p.stem == p.parent.name})


def _review_items(folder):
    """[(round page, row)]: the rows of each Round page's `## Review Items` table whose `lands on` starts
    with this Section's stem (the Round's table, agreed by JL 261007; haipipe-paper-comments)."""
    out = []
    for page in _round_pages(folder):
        text = page.read_text(encoding="utf-8", errors="replace")
        if "## Review Items" not in text:
            continue
        lines = [l for l in text.split("## Review Items", 1)[1].split("\n## ", 1)[0].splitlines() if l.startswith("|")]
        rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in lines]
        rows = [r for r in rows if not all(set(c) <= set("-: ") for c in r)]
        if not rows:
            continue
        head = [h.lower() for h in rows[0]]
        for r in rows[1:]:
            row = dict(zip(head, r))
            if row.get("lands on", "").startswith(folder.name):
                out.append((page, row))
    return out


def _reviews(folder, root):
    """◆ Comments: the Review Items of the version's comments Pages that land on this Section (Review-<slug>, citing the
    points it answers: R1.1 · E1.2 · A1.2), Review Item │ Work │ Report."""
    items = _review_items(folder)
    if not items:
        return ('<p class=space-empty>No Review Items yet. A comments Page\'s Review Items (Review-&lt;slug&gt;, citing '
                'R1.1 · E1.2 · A1.2) show here once its comments Page lists them.</p>')
    rows = [(f'<b>{esc(r.get("item", ""))}</b> <span class=mut>cites {esc(r.get("cites", ""))} · '
             f'{esc(r.get("lands on", ""))}</span>',
             f'{esc(r.get("work", "") or "—")} <span class=mut>· {esc(r.get("state", ""))}</span>',
             pop(reader(page, root), page.stem, f'{page.stem} › {r.get("reply", "") or "no reply yet"} ↗'))
            for page, r in items]
    return table(("Review Item", "Work", "Report"), rows)


def section_spaces(folder, root, sub):
    """A Section's six Spaces: the base's Page Task, each paper line added to the Space it belongs to;
    the subspaces stay the base's."""
    from dataclasses import replace
    out = draft_task_spaces(folder, root, sub)
    md = face(folder)
    d, a, w, plan = out["Description"], out["Audience Report"], out["Delivery"], out["Work Details"]
    if d.open == "Scope":
        base = vanilla("Task", folder, root, sub).get("Description")
        out["Description"] = replace(d, html=_contract(md) + (base.html if base else ""))
    if plan.open == "1 · Plan":                   # the Requirement is a card of 1 · Plan (b32 s41 Ⓐ)
        out["Work Details"] = replace(plan, html=plan.html + _sub_rows(md))
    elif plan.open == "3 · Evidence":             # a Section's evidence follows the paper's rules (haipipe-paper 1.15)
        out["Work Details"] = replace(plan, html=plan.html.replace("/haipipe-evidence ", "/haipipe-paper-evidence "))
    if sub == "Comments":                         # ◆ the paper's own view, after the Page's three
        a = Space(html=_reviews(folder, root), open="Comments", run_types=())
    out["Audience Report"] = replace(a, subspaces=tuple(draft_task_spaces(folder, root, "")["Audience Report"].subspaces)
                                     + ("Comments",), note="")   # no read-only note in the Runs panel (JL 261008)
    out["Delivery"] = replace(w, html=_ready(folder, md) + w.html)   # ◆ Ready over the base's cards
    return out


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


VERSION_RE = re.compile(r"^j\d{2}_v")


def _disk_block(d, block, out):
    from dataclasses import replace
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
        ("Idea Studio", ""): [("studio/", "one row per topic"), ("studio/s*/", "the topics")],
        ("Audience Report", "Ideation"): idea + reg,
        ("Audience Report", "Narrative"): tell + reg,
        ("Audience Report", "High-level logic + Low-level work"): reg + tell + rep_,
        ("Audience Report", "Related Questions"): reg + rep_,
        ("Audience Report", "Related Papers"): [("related/related.md", "the related items, by question")] + tell + reg,
        ("Work Details", "Jobs"): [("j[0-9][0-9]_*/", "one version each")],
        **{("Work Details", n): [(f"studio/{t.name}/", "its drawing and face") for t, _x in
                                 _board_topics(block, BOARD_STEP[n][1], BOARD_STEP[n][2])]
           or [("studio/", "no topic yet")] for n in BOARD_STEP},
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
