"""A paper Board's Audience Report: its questions as rows (Logic │ Work │ Report), the ideas, the audiences it must attract.
Moved from paper_theme.py, which re-exports every name here so `from live.paper_theme import _report` keeps working."""
from __future__ import annotations

import re

from live import paper as P
from live.frame import Space, esc, pop, reader, rel, topic_drawings
from live.paper_theme import NOT_PAPERS, _empty, _pick, _related, _run_cards, pv


# JL 261007: the Audience Report is questions; Spine, Design and the telling are one view, Narrative: how we
# tell the story, and whether it will attract an editor, a reviewer and the public
AUDIENCE = ("Ideation", "Narrative", "High-level logic + Low-level work", "Related Questions", "Related Papers")
# who the story must attract, what each looks for, and the Story division that answers it (by its heading)
ATTRACT = (("editor", "fit, and a contribution worth the pages, in one sentence", ("Identity", "Pitch")),
           ("reviewer", "claims backed by evidence, honest about their limits", ("Research Questions", "Evidence")),
           ("public", "why it matters, and what to take away", ("Stakes", "Pitch")))


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
    for t in P.board_topics(block, topic_glob):
        face_md = t / f"{t.name}.md"
        drawing = next(iter(topic_drawings(t)), None)      # its own drawing first, never its mNN mind map
        url = ("/_excalidraw/?" + P.urlencode({"board": rel(drawing, root)})) if drawing else reader(face_md, root)
        out.append(f'<li>{pop(url, t.name + " · from the Idea Studio", t.name + " ↗")}</li>')
    return "".join(out)


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
