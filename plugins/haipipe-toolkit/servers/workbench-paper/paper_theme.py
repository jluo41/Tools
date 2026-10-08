"""The paper theme on the base frame (servers/workbench/frame.py): only what differs from vanilla.

A paper Board climbs the ladder as Tools/designs/b16_theme_paper proposes (Q01, s11-paper-block): the
Board is one paper; its versions are Jobs and its Sections are Page Tasks once those folders exist. Today
a paper Board holds A1-Story/ (Ideation and Story Pages) and Ba-/Bb- Section groups, so this theme fills
the Block tab only, from today's folders, with paper.py's own content (JL: carry over what exists) drawn in
the base's look only (JL 261007: no theme stylesheet): wf-table, the folding .topic row, the lw-/bj- work rows.

    Description      Scope · Venue · Resources · Related     (Related: paper cards, drawing from the deep read)
    Idea Studio      the base's studio rows; the RoadMap drawings are rows   (was Story › RoadMap Draw)
    Audience Report  Ideation · Narrative · High-level logic + Low-level work · Related Questions: questions
                     (JL 261007); Narrative = what the story says, how it is drawn and told, will it attract
    Work Details     Main · Appendix · Evidence               (was Sections; a row opens its Page)
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
from live.frame import Space, Theme, esc, face, link, page_task_spaces, pop, reader, rel, studio_cards, table, vanilla


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


def pv(html: str) -> str:
    """A view in the old paper page's look, its links into the frame."""
    return f'<div class=pv><style>{PV_CSS}</style>{_frame_links(html)}</div>'


def _pick(sub: str, options: tuple) -> str:
    return sub if sub in options else options[0]


OTHER = "Datasets and repos"        # Related's group with no research question (b16 g03 D9)


def _related_rows(d, block):
    """(group, kind, key, title, venue, why, run) per related item: related/related.md when the Board has
    it (b03 s01-D27), else the current Story's related-papers table; run = the deep read it links, or None."""
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
            rows.append((get(r, "group") or OTHER, get(r, "kind") or "paper", get(r, "key"),
                         get(r, "paper", "item"), get(r, "venue"), get(r, "why here", "why"),
                         P._disc_run(d, addr) if addr else None))
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


def _related(d, block, root):
    """Related as paper cards, grouped by `group` (RQn first, then Datasets and repos, then the rest). A card folds;
    opened, it shows the paper's drawing from its deep read, view only (JL 261007, s11-paper-block)."""
    rows = _related_rows(d, block)
    if not rows:
        return '<p class=mut>No related item yet: related/related.md, one row each, any kind.</p>'
    order = lambda g: (0 if g.upper().startswith("RQ") else 1 if g == OTHER else 2, g)
    out = []
    for group in sorted({r[0] for r in rows}, key=order):
        out.append(f"<h3>{esc(group)}</h3>")
        for _, kind, key, title, venue, why, run in (r for r in rows if r[0] == group):
            drawing = run / f"{run.name}.excalidraw" if run is not None else None
            read = (link(reader(run / f"{run.name}.md", root), f"read {run.name.split('_')[0]} ↗")
                    if run is not None and (run / f"{run.name}.md").is_file() else "no deep read yet")
            head = (f'<span><b>{esc((key + " ") if key else "")}{esc(title)}</b>'           # line 1: who · title
                    + (f' <span class=topic-meta>{esc(venue)}</span>' if venue else "")
                    + f'<br><span class=topic-meta>{esc(kind)} · why here: {esc(why or "—")} · {read}</span></span>')
            if drawing is not None and drawing.is_file():
                url = "/_excalidraw/?" + P.urlencode({"board": rel(drawing, root)})
                head += f'<span class=topic-pop>{link(url, "↗ full size")}</span>'
                body = (f'<iframe class=st-frame title="{esc(title)}" data-src="{esc(url)}" '
                        'referrerpolicy=no-referrer></iframe>')
            elif kind != "paper":
                body = '<p class="mut none">A dataset or repo: no drawing.</p>'
            else:
                body = ('<p class="mut none">⚠ No drawing yet: the paper\'s deep read draws it '
                        '(question → data · method → finding → limits). Run type: Read a paper.</p>')
            missing = kind == "paper" and not (drawing is not None and drawing.is_file())
            out.append(f'<details class="topic{" missing" if missing else ""}"><summary>{head}</summary>{body}</details>')
    return "".join(out)


def _description(d, block, root, sub):
    opts = ("Scope", "Venue", "Resources", "Related")
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
    elif s == "Resources":
        from live.task_questions import register, words
        res, _ = register(P.read(block / "board.md"), "Related resources", "resources")
        rows = [(link(words(r.get("url")), words(r.get("title"))), esc(", ".join(r.get("questions") or [])))
                for r in res if words(r.get("title"))]
        html = table(("resource", "for"), rows)
    else:
        html = (_related(d, block, root) if (block / "related" / "related.md").is_file()
                else pv(P.related_html(d)))                     # the old Related Papers cards (JL 261007)
    return Space(html=html, subspaces=opts, open=s, run_types=_run_cards("Block", "Description", s))


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
AUDIENCE = ("Ideation", "Narrative", "High-level logic + Low-level work", "Related Questions")
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
        drawing = next(iter(sorted(t.glob("*.excalidraw"))), None)
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
    else:                                           # the current telling's research questions
        html = pv(P.logic_work_html(d))             # its original structure (JL 261007): question blocks,
        if 'class="qc lw-q"' not in html:           # logic beside work and report; a Board with no Story text
            html = "".join(_base_rows(block, root, g) for g in _fed_groups(d, block, root)) or html   # yet
    return Space(html=html, subspaces=AUDIENCE, open=s, run_types=_run_cards("Block", "Audience Report", s))


def _sections(d, sub):
    opts = ("Jobs", "Main", "Appendix", "Evidence")
    s = _pick(sub, opts)
    rows = P.section_rows(d)
    if s == "Jobs":                                 # s11: the Board's Work Details are its Jobs
        html = _jobs(d, d["board"], d["root"])
    elif s in ("Main", "Appendix"):
        html = pv(P._section_table(d, [r for r in rows if r["part"] == s.lower()]))
    else:
        html = table(("item", "type", "Section", "need", "state", ""),
                     [(esc(it["id"]), esc(it["type"]), esc(it["page"]), esc(it["desc"]), esc(it["status"]),
                       P._link(d, it["rel"], "Open ↗", lens="evidence", focus=it["id"])) for it in d["hero"]])
    return Space(html=html, subspaces=opts, open=s, run_types=_run_cards("Block", "Work Details") + (
        _run_cards("Job", "Work Details", "Main") if s != "Jobs" else ()))


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


def _version_delivery(d, board, job, root):
    """A version's Delivery as folding item cards, no third row (JL 261007: "item card based", s12): Manuscript
    (the PDF, the Word file), Letters (the cover letter), Checks (submission readiness), Sent (each frozen send)."""
    dv = d["delivery"]
    if dv["dir"] is None:
        return Space(html=_empty("No delivery/ yet: Build writes it."), run_types=_delivery_runs())
    out = []
    for suffix, kind in ((".pdf", "LaTeX"), (".docx", "Word")):
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
    cover = P._cover(d)
    if cover is not None:
        pdf = (cover.get("outputs") or {}).get("pdf")
        pdf = (dv["dir"] / pdf) if pdf and not Path(pdf).is_absolute() else (Path(pdf) if pdf else None)
        body = _frame(d, pdf, "cover letter") if pdf and pdf.is_file() else _empty("Not built yet.")
        out.append(("Letters", _fold("cover letter", esc(("built" if pdf and pdf.is_file() else "not built") + " · "
                                                         + ("ready" if cover.get("ready") else "not ready")), body)))
    else:
        out.append(("Letters", _fold("cover letter", "not built", _empty(
            "No cover letter built yet: add a [coverletter] block to delivery/paper-build.toml and run the build."))))
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
    html, last = "", ""
    for group, card in out:
        html += (f"<h3>{esc(group)}</h3>" if group != last else "") + card
        last = group
    return Space(html=html, run_types=_delivery_runs())


def _delivery_runs():
    """Build · Check (Send stays a proposal, s12)."""
    return _run_cards("Job", "Delivery")


def _delivery(d, sub, opts=("LaTeX", "Word", "Cover letter", "Rounds")):
    s = _pick(sub, opts)
    if s in ("LaTeX", "Word"):
        html = (_empty("No delivery/ yet.") if d["delivery"]["dir"] is None else
                _built(d, ".pdf" if s == "LaTeX" else ".docx", checks="Checks" not in opts))
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
    web = folder / "delivery" / "web" / "index.html"
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
ASSEMBLE = Path(__file__).resolve().parents[2] / "skills/2_theme/paper/haipipe-paper-assemble/scripts"
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
    else:
        html = pv(P._section_table(d, [r for r in rows if s == "All" or r["part"] == s.lower()]))
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
    if (job / "delivery").is_dir():                 # on the ladder each version builds its own (g03 D4)
        d = dict(d, delivery=P.delivery_info(d, job / "delivery"))
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


SECTION_SKILL = Path(__file__).resolve().parents[2] / "skills/2_theme/paper/haipipe-paper-section"
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
    """◆ Scope: the reader contract, read from the face's header (haipipe-paper-section's fields)."""
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
    pdf = (folder / "delivery" / "latex" / f"{stem}.pdf").is_file()
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
    out = page_task_spaces(folder, root, sub)
    md = face(folder)
    d, a, w = out["Description"], out["Audience Report"], out["Delivery"]
    if d.open == "Scope":
        base = vanilla("Task", folder, root, sub).get("Description")
        out["Description"] = replace(d, html=_contract(md) + (base.html if base else ""))
    elif d.open == "Requirement":
        out["Description"] = replace(d, html=d.html + _sub_rows(md))
    if sub == "Comments":                         # ◆ the paper's own view, after the Page's three
        a = Space(html=_reviews(folder, root), open="Comments", run_types=())
    out["Audience Report"] = replace(a, subspaces=tuple(page_task_spaces(folder, root, "")["Audience Report"].subspaces)
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
        ("Description", "Related"): [("related/related.md", "the related items")] + tell,
        ("Idea Studio", ""): [("studio/", "one row per topic"), ("studio/s*/", "the topics")],
        ("Audience Report", "Ideation"): idea + reg,
        ("Audience Report", "Narrative"): tell + reg,
        ("Audience Report", "High-level logic + Low-level work"): reg + tell + rep_,
        ("Audience Report", "Related Questions"): reg + rep_,
        ("Work Details", "Jobs"): [("j[0-9][0-9]_*/", "one version each")],
        ("Work Details", "Main"): _section_globs(d, block, "main"),
        ("Work Details", "Appendix"): _section_globs(d, block, "appendix"),
        ("Work Details", "Evidence"): [("*/t[0-2][0-9]_*/draft/*-evidence-items.md", "each Section's evidence items")],
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
        from live.frame import page_task_spaces      # plain Page Task views until Q03
        return page_task_spaces(folder, root, sub)
    if level == "Job" and folder.name.startswith(("A1-", "j00_")):   # the Story Job (g03 D1)
        return story_spaces(folder, root, sub)
    if level == "Job":                              # a version (s12): today's group, or jNN_v<N>_<desk>/
        return version_spaces(folder, root, sub)
    if level != "Block" or not (folder / "board.md").is_file():
        return {}
    d = _data(folder, root)
    return _disk_block(d, folder, {"Description": _description(d, folder, root, sub),
                                   "Idea Studio": _studio(d, folder, root),
                                   "Audience Report": _report(d, folder, root, sub),
                                   "Work Details": _sections(d, sub),
                                   "Runs": Space(run_types=_run_cards("Block", "Runs")),
                                   "Delivery": _delivery(d, sub)})


THEME = Theme(name="paper", label="Paper", icon="📄", guide="paper",
              level_names={"Block": "Paper Board", "Job": "Version", "Task": "Section"}, spaces=spaces,
              # today's folders on the ladder, unrenamed (b03, JL 261007: keep the names): a group
              # Ba-/Bb-/Bc-<desk>-<part> or A1-Story is a Job (jNN_ folders are Jobs by their prefix); a
              # Section S-…, a review batch RD<NN>/CM<NN> or a Story Page inside one is a Task (g03)
              level_patterns={"Job": r"^(B[a-z]|A1)-", "Task": r"^(S-|RD\d|CM\d|Story|t\d{2}_)"})
