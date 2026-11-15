"""A paper Board's Story parts: the story arc, Story by Section (each Section's part of the arc and its claims),
the Idea and Story side tabs, the research questions' table and the Roadmaps (board_results draws the views)."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

from live import draft_steps as ds
from live import item_cards as IC, item_marks as IM
from live.frame import esc
from live.ui_parts import _cap, _clean, _kv, _open_btn, _plain, _side_tabs
from live.board_read import (_rq_table, _after_table, _face, _field, _label_rows, _lead_sentence, _open_link, _page_url,
                             _rq_lists, _table, _undated, is_version)


def _story_arc(topic: Path, body: str, md=None) -> str:
    """The whole paper's story arc, the first tab of Story by Section (JL 261109: "at the top of the tab, to describe the
    narrative of this paper, what is the story arc of it"): the Section Narrative's `#### Story arc` (haipipe-paper-story);
    else the ```text block that opens it (identity, question, headline, boundaries); else where to write it."""
    m = re.search(r"(?ims)^#{2,5}[ \t]*(?:[\d.]+[ \t]*·[ \t]*)?(?:story|argument)[ \t]+arc\b[^\n]*\n(.*?)(?=^#{2,5}[ \t]|\Z)", body)
    if m and m[1].strip():
        arc = _drop_section_table(m[1].strip())          # the per-Section table is drawn as rows (_section_rows)
        return (md(arc, topic) if md else f'<p>{esc(_plain(arc))}</p>') if arc.strip() else ""
    pre = re.split(r"(?m)^#{2,5}[ \t]|^\|", body, maxsplit=1)[0]
    block = re.search(r"```text\n(.*?)```", pre, re.S)
    if block:
        return f'<pre style="white-space:pre-wrap;margin:0">{esc(block[1].rstrip())}</pre>'
    return ('<p class=mut>No story arc yet: the Story\'s Section Narrative opens with <code>#### Story arc</code> '
            '(haipipe-paper-story).</p>')


def _drop_section_table(text: str) -> str:
    """The text without its Markdown table whose first header is `Section` (the per-Section rows)."""
    return re.sub(r"(?ms)^\|[ \t]*Section[ \t]*\|.*?(?=^(?!\|)|\Z)", "", text, flags=re.I).strip()


def _steps_of(text: str) -> list:
    """A Section's ordered moves: split on → or ->, else on ; (a table cell cannot hold a list)."""
    said = _said(text)
    parts = re.split(r"\s*(?:→|->)\s*", said)
    if len(parts) < 2:
        parts = re.split(r"\s*;\s*", said)
    return [x.strip() for x in parts if x.strip()]


def _section_row(num: str, name: str, low: dict, claims=()) -> str:
    """One Section's part of the arc as a row, exactly the Research Questions' row (JL 261111: "they are very differnt,
    where is the 1, 2, 3, 4"): its number and name; what the reader asks, then the moves as a quieter line; then what the
    reader leaves with, its displays and claims as chips, and what it must not say, muted."""
    ask, steps = _said(low.get("reader question", "")), _steps_of(low.get("ordered moves", ""))
    exit_, refuse = _said(low.get("exit", "")), _said(low.get("must refuse", ""))
    shows = [x.strip() for x in re.split(r"\s*[;,]\s*(?![^()]*\))", _said(low.get("displays", ""))) if x.strip()]
    chips = "".join(f"<span class=pb-chip>{esc(x)}</span> " for x in shows) + "".join(
        f'<span class=pb-chip title="{esc(_plain(r.get("proposition", "")))}">{esc(r.get("claim", ""))}</span> ' for r in claims)
    left = ((f'<p class=q>{esc(ask)}</p>' if ask else "")
            # the moves as the Section's numbered flow, 1, 2, 3, 4, one per line (JL 261111: "I want the introduction to
            # have the 1, 2, 3, 4 for the narrative follow")
            + (f'<ol class=mvs>{"".join(f"<li>{esc(x)}</li>" for x in steps)}</ol>' if steps else ""))
    right = ((f'<p class=if>→ {esc(exit_)}</p>' if exit_ else "")
             + (f'<p class=st>{chips}</p>' if chips else "")
             + (f'<p class=mv>✗ {esc(refuse)}</p>' if refuse else ""))
    return (f'<li><span class=k>{esc(num)}<span class=nm>{esc(_cap(_sec_key(name)))}</span></span>'
            f'<div class=q-col>{left}</div><div class=a>{right}</div></li>')


SECTION_ROWS_CSS = ("<style>.pb-rqs.pb-secs li{grid-template-columns:96px minmax(0,1.15fr) minmax(0,1fr)}"
                    ".pb-rqs .q-col{min-width:0}.pb-rqs .mv{color:var(--muted);font-size:13px;line-height:1.5;margin-top:3px}"
                    ".pb-rqs ol.mvs{list-style:decimal;margin:4px 0 0;padding-left:1.4em;font-size:13.5px;line-height:1.5}"
                    ".pb-rqs ol.mvs li{display:list-item;padding:0 0 2px;border:0}"
                    ".pb-rqs .nm{display:block;font-weight:500;font-size:12.5px}.pb-rqs .pb-chip{margin:0 4px 2px 0}"
                    "@media(max-width:900px){.pb-rqs.pb-secs li{grid-template-columns:96px 1fr}.pb-rqs.pb-secs .a{grid-column:2}}"
                    "@media(max-width:600px){.pb-rqs.pb-secs li{grid-template-columns:62px 1fr}.pb-rqs .nm{font-size:11.5px}}</style>")


SUPPLEMENT = re.compile(r"^(?:supplement|appendix|extended data|supplementary)")


def _section_numbers(names: list) -> list:
    """Each Section's number in reading order: 1, 2, 3 for the main text, S1, S2 for a supplement or appendix."""
    out, main, sup = [], 0, 0
    for n in names:
        if SUPPLEMENT.match(_sec_key(n)):
            sup += 1
            out.append(f"S{sup}")
        else:
            main += 1
            out.append(str(main))
    return out


def _section_rows(rows: list) -> str:
    """The per-Section rows, [(name, low, claims)], numbered in reading order, across the card's width."""
    nums = _section_numbers([r[0] for r in rows])
    return (STORY_CSS + SECTION_ROWS_CSS + '<div class="pb-story pb-wide"><ol class="pb-rqs pb-secs">'
            + "".join(_section_row(k, *r) for k, r in zip(nums, rows)) + '</ol></div>') if rows else ""


NARRATIVE_ORDER = ("abstract", "summary", "introduction", "background", "theory", "data", "methods", "results",
                   "robustness", "discussion", "conclusion", "appendix", "extended data", "supplement", "cover letter",
                   "letter", "response")


def _sec_key(name: str) -> str:
    """A Section's name for matching: `t01_introduction`, `Introduction` and `introduction` alike."""
    return re.sub(r"[\s_-]+", " ", re.sub(r"^t\d+_", "", _plain(name))).strip().lower()


def _said(value: str) -> str:
    """A cell or face line as words; a `<placeholder>` or a dash says nothing."""
    v = _plain(value or "").strip()
    return "" if not v or v in ("—", "-", "none") or re.fullmatch(r"<[^>]*>", v) else v


def _section_story(board: Path, body: str) -> list:
    """[(Section key, its name, {reader question, entry, moves, must refuse, displays, exit, in, out})] in reader order:
    the per-Section rows of the Story's §8 (a table whose first header is `Section`), else of the newest writing
    version's `## Narrative`; each completed by its Section face (`reader-question`, `entry-state`, `exit-state`,
    `transition-in`, `transition-out`) in that version."""
    versions = sorted((j for j in board.glob("j[0-9]*_*") if j.is_dir() and is_version(j)), reverse=True)
    from live.board_read import md_table
    rows, version = [], None
    sources = [(None, body)] + [(v, (v / f"{v.name}.md").read_text(encoding="utf-8", errors="ignore"))
                                for v in versions if (v / f"{v.name}.md").is_file()]
    for owner, src in sources:
        rows = [r for r in md_table(src, "Section") or md_table(src, "section")       # a row still all <placeholders>
                if _said(r.get("Section", r.get("section", "")))                       # (a new Section's, haipipe-paper
                and any(_said(v) for k, v in r.items() if k.lower() != "section")]      # task) tells nothing yet
        if rows:
            version = owner
            break
    version = version or (versions[0] if versions else None)
    faces = {}
    for sec in (sorted(x for x in version.glob("t[0-9]*_*") if x.is_dir()) if version else []):
        f = sec / f"{sec.name}.md"
        faces[_sec_key(sec.name)] = f.read_text(encoding="utf-8", errors="ignore") if f.is_file() else ""
    out, seen = [], set()
    for r in rows:
        low = {k.lower(): v for k, v in r.items()}
        name = low.get("section", "")
        key = _sec_key(name)
        out.append((key, name, low))
        seen.add(key)
    for key, text in faces.items():                       # a Section with no row still tells its face's lines
        if key not in seen and any(_said(_field(text, f)) for f in ("reader-question", "exit-state", "transition-out")):
            out.append((key, key, {}))
    for key, name, low in out:
        text = faces.get(key, "")
        for col, field in (("reader question", "reader-question"), ("entry", "entry-state"), ("exit", "exit-state"),
                           ("in", "transition-in"), ("out", "transition-out"), ("must refuse", "must-refuse")):
            if not _said(low.get(col, "")) and _said(_field(text, field)):
                low[col] = _field(text, field)
    rank = lambda k: next((i for i, o in enumerate(NARRATIVE_ORDER) if k.startswith(o)), 99)
    return out if rows else sorted(out, key=lambda x: rank(x[0]))


def _narrative(topic: Path, root: Path, body: str, md=None) -> str:
    """Story by Section as side tabs, restored (JL 261111: "I want the left tab right content, git it back to me!!!!"; first JL 261109: "for this we should have the left tab and right content"; "this is not
    just the claims, it is also about the narratives, the arc, how to make it smooth"). The first tab is the whole
    paper's story arc (_story_arc). Then one tab per Section in reader order, its small line what the reader leaves
    with; on the right the Section's part of the arc first: what the reader asks, comes in with, the moves in order,
    leaves with, how it hands on to the next Section, what it must not say, its displays; its claims last (the claims
    table, `lands in`), each with the question it answers and the display that carries it. The full mind map opens by
    its button (b16 s32 B r02)."""
    claims = [r for r in _table(body) if r.get("lands in") and r.get("proposition")]
    story = _section_story(topic.parent, body)
    if not (claims or story):
        return ""
    where = {}
    for r in claims:
        for sec in (x.strip() for x in r["lands in"].split(",")):
            where.setdefault(_sec_key(sec), (sec, []))[1].append(r)
    secs = [(key, name, low) for key, name, low in story]
    known = {k for k, _, _ in secs}
    rank = lambda k: next((i for i, o in enumerate(NARRATIVE_ORDER) if k.startswith(o)), 99)
    for key in sorted(where, key=rank):                   # a Section only the claims name, after the told ones
        if not any(key.startswith(k) or k.startswith(key) for k in known):
            secs.append((key, where[key][0], {}))

    def claims_of(key):
        return [r for k, (_, rs) in where.items() if k == key or k.startswith(key) or key.startswith(k) for r in rs]

    def moves(text):                                      # numbered 1, 2, 3, one per line (JL 261111)
        steps = _steps_of(text)
        return (f'<ol style="margin:0;padding-left:1.3em">{"".join(f"<li>{esc(x)}</li>" for x in steps)}</ol>'
                if len(steps) > 1 else esc(_said(text)))

    items, panels = [], []
    for key, name, low in secs:
        mine = claims_of(key)
        told = _kv([("Reader asks", esc(_said(low.get("reader question", "")))),
                    ("Comes in with", esc(_said(low.get("entry", "")) or _said(low.get("in", "")))),
                    ("Moves", moves(low.get("ordered moves", ""))),
                    ("Leaves with", esc(_said(low.get("exit", "")))),
                    ("Hands on", esc(_said(low.get("out", "")))),
                    ("Must not say", esc(_said(low.get("must refuse", "")))),
                    ("Displays", esc(_said(low.get("displays", ""))))])
        said = _kv((r.get("claim", ""), esc(_plain(r["proposition"])) + "".join(
                   f'<br><span class=mut>{esc(k)}: {esc(_plain(r[c]))}</span>'
                   for c, k in (("answers", "Answers"), ("displays", "Shown in")) if _plain(r.get(c, "")))) for r in mine)
        if told == '<dl class=pb-kv></dl>':
            told = ""
        panels.append(told + (('<p class=pb-part>Claims</p>' if told else "") + said if mine else ""))
        exit_ = _said(low.get("exit", ""))
        items.append((_cap(_sec_key(name)), exit_[:60] if exit_ else
                      f'{len(mine)} claim{"s" if len(mine) != 1 else ""}' if mine else ""))
    page = topic / f"{topic.name}.mindmap.html"
    btn = (f'<a class=fd-btn data-pop="{esc(topic.name)} · mind map" href="/{quote(ds._rel(page, root))}">Mind map</a>'
           if page.is_file() else "")
    items, panels = [("📖 Story arc", "the whole paper")] + items, [_story_arc(topic, body, md)] + panels
    return _side_tabs("nar", items, panels) + (f'<div class=pb-verbs>{btn}</div>' if btn else "")


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


# the Story view's reading parts (Paper-CMS-AI-Usage 261110: "the display here is not well to ready"): a reading
# measure, label and value rows, a sentence a line, each question with what it lets the paper say, pending as a chip
# a capped block sits in the middle of its card, its text left-aligned (JL 261110: "at least you put the paragraph in
# the middle"); the question rows fill the card, their head capped and centred like the prose above them
STORY_CSS = ("<style>.pb-story,.pb-story.pb-wide .pb-head{max-width:92ch;margin-inline:auto}.pb-story .pb-big{margin:2px 0 12px;max-width:none}"
             ".pb-story .pb-kv{grid-template-columns:130px 1fr;margin:0 0 6px}"
             ".pb-label{font-size:11.5px;letter-spacing:.05em;text-transform:uppercase;color:var(--muted);margin:0}"
             ".pb-chip{display:inline-block;font-size:11.5px;line-height:1.6;color:var(--muted);border:1px solid var(--line);"
             "border-radius:10px;padding:0 8px;white-space:nowrap;vertical-align:1px}"
             ".pb-story ul.pb-lines,.pb-story ol.pb-rqs{padding:0;margin-left:0}.pb-lines{list-style:none;margin:0}.pb-lines li{margin:0 0 7px;line-height:1.55}"
             # a list keeps the question block's width, centred with it (JL 261111: "I want the table is the same width to the
             # Paper questions"), its columns the question, then what it lets the paper say; stacked on a narrow screen
             ""
             ".pb-rqs{list-style:none;margin:4px 0 0}.pb-rqs li{display:grid;grid-template-columns:42px minmax(0,1.15fr) minmax(0,1fr);gap:3px 22px;"
             "padding:9px 0;border-top:1px solid var(--line)}.pb-rqs .k{color:var(--accent);font-weight:600;font-size:13px;padding-top:1px}"
             ".pb-rqs p{margin:0}.pb-rqs .q{line-height:1.5}.pb-rqs .if{font-size:13.5px;line-height:1.5}"
             ".pb-rqs .st{margin-top:5px}"
             "@media(max-width:900px){.pb-rqs li{grid-template-columns:42px 1fr}.pb-rqs .a{grid-column:2}"
             ".pb-rqs .if{color:var(--muted)}}@media(max-width:600px){.pb-story .pb-kv{grid-template-columns:1fr}}</style>")


RQ_CONTEXT = (("why we ask", "Why we ask"), ("how others asked", "Asked before"), ("what is new", "New here"))


def _cards(topic: Path, root: Path) -> tuple:
    """The Story topic's item cards (it owns its questions' ids, cards.md §4) and its path for the writer."""
    try:
        rel = topic.resolve().relative_to(Path(root).resolve()).as_posix()
    except ValueError:
        rel = ""
    return IC.cards(topic), rel


def _rq_head(whole, cards: dict, rel: str) -> str:
    """The paper's question above the table, `RQ.Q`, with its marks and its cards under it."""
    if not whole:
        return ""
    words = _plain(whole[1])
    return (f'<div class=pb-rqhead data-addr="RQ.Q"><p class=pb-label>The paper\'s question {IM.marks("RQ.Q", cards)}</p>'
            f'<p class=pb-big>{_chips(words)}</p>{IM.card_slot("RQ.Q", cards, rel, words=words)}</div>')


def _rq_context(rq: str) -> dict:
    """{RQ number: (why we ask it, how others asked it, what is new here)} from §3's table whose header names them
    (Paper-CMS-AI-Usage 261111: "Why we ask each question, and how others asked it"); its first cell starts with the
    RQ number ("1 · how many physicians")."""
    lines = rq.splitlines()
    for i, line in enumerate(lines):
        head = [c.strip().lower() for c in line.strip().strip("|").split("|")]
        if not line.lstrip().startswith("|") or not any("why we ask" in h for h in head):
            continue
        cols = [next((j for j, h in enumerate(head) if key in h), None) for key, _ in RQ_CONTEXT]
        out = {}
        for row in lines[i + 2:]:
            if not row.lstrip().startswith("|"):
                break
            cells = [c.strip() for c in row.strip().strip("|").split("|")]
            num = re.match(r"\D*(\d+)", cells[0] if cells else "")
            if num:
                out[int(num[1])] = tuple(_said(cells[j]) if j is not None and j < len(cells) else "" for j in cols)
        return out
    return {}


RQ_TABLE_CSS = ("<style>.fd-body table.pb-rqtab,table.pb-rqtab{display:table;width:100%;max-width:none;overflow:visible;border-collapse:collapse;margin:10px 0 0;font-size:13.5px;line-height:1.5}"
                ".pb-rqtab th{text-align:left;font-weight:600;padding:4px 12px 4px 0;border-bottom:1px solid var(--line);vertical-align:bottom}"
                ".pb-rqtab td{vertical-align:top;padding:7px 12px 7px 0;border-bottom:1px solid var(--line)}"
                ".pb-rqtab td.k{color:var(--accent);font-weight:600;white-space:nowrap}.pb-rqtab td:first-child,.pb-rqtab th:first-child{width:40px}"
                ".pb-rqtab td[data-h=Question]{min-width:220px}"
                ".pb-rqhead .pb-big{margin:2px 0 8px;max-width:none}"  # the paper's question on the table's left edge (JL 261111)
                "@media(max-width:700px){.pb-rqtab,.pb-rqtab tbody,.pb-rqtab tr,.pb-rqtab td{display:block;width:auto}.pb-rqtab thead{display:none}"
                ".pb-rqtab tr{border-bottom:1px solid var(--line);padding:6px 0}.pb-rqtab td{border:0;padding:1px 0;min-width:0!important;white-space:normal!important}"
                ".pb-rqtab td[data-h]::before{content:attr(data-h) \": \";color:var(--muted)}}</style>")


def _chips(text: str) -> str:
    """Escaped text with each `⟦pending ...⟧` mark as a muted chip, not raw brackets."""
    return re.sub(r"⟦([^⟧]*)⟧", lambda m: f"<span class=pb-chip>{m[1]}</span>", esc(text))


def _sentences(text: str) -> list:
    """A paragraph a sentence a line: split after . ? ! before a capital, a <placeholder> or a pending mark (which then
    leads the anticipated sentence it marks)."""
    return [x.strip() for x in re.split(r"(?<=[.?!])\s+(?=[A-Z<⟦])", text.strip()) if x.strip()]


def _bold_rows(body: str) -> tuple:
    """([(label, value)], the rest): each paragraph that opens `**Label**: value`, as a label and value row."""
    rows = []

    def take(m):
        rows.append((m[1].strip(), _plain(" ".join(m[2].split()))))
        return ""
    rest = re.sub(r"(?m)^\*\*([^*\n]+)\*\*:\s*(.+(?:\n(?![ \t]*\n).+)*)\n?", take, body)
    return rows, rest


def idea_tabs(topic: Path, md) -> list:
    """Idea's parts (b16 s32 A): Direction large, then the directions considered. The
    Hand-off is no tab: only a question it holds for the person stays, under the Direction (s32-D35).
    Returns [(tab name, its small line, its panel)]."""
    text, parts = _face(topic)
    chosen = ""
    if "direction" in parts:
        lead, rest = _lead_sentence(parts["direction"])
        _, rest = _label_rows(re.sub(r"(?m)^\*\*Direction\*\*:.*\n?", "", rest))   # no stage, no START, SETTING, CONTRAST rows (JL 261104: "could we just remve this?")
        rows, rest = _bold_rows(rest)
        if not lead and rows:                    # a face of **Label**: paragraphs (Paper-CMS-AI-Usage 261110: "not well to
            at = next((i for i, (k, _) in enumerate(rows) if "question" in k.lower()), 0)   # read"): its question large,
            lead = rows.pop(at)[1]               # the rest (Why now, Admission rule) as label and value rows
        chosen = (f'<p class=pb-big>{_chips(_cap(lead))}</p>' + _kv((k, _chips(_cap(v))) for k, v in rows)
                  + (md(rest, topic) if rest.strip() else ""))
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
    chosen = STORY_CSS + f'<div class=pb-story>{chosen}</div>' if chosen else ""
    theories = []
    if rows:
        theories = [(short(_plain(r.get("direction", ""))), _undated(r.get("verdict", "")), "", _direction_theory(r)) for r in tiles]
    theory = (_side_cards("th", [x[:3] for x in theories], [f'<p>{esc(x[3]) or "No theory written for this direction yet."}</p>' for x in theories])
              if any(x[3] for x in theories) else "")
    return ([("Direction", "the direction chosen", chosen)] if chosen else []) + \
        ([("Directions considered", "what else was weighed", considered)] if considered else []) + \
        ([("Theory", "each direction's theory", theory)] if theory else [])



def story_tabs(board: Path, topic: Path, root: Path, md) -> list:
    """Story's parts (b16 s32 B; s32-D44): Pitch large, the Research Questions, Stakes,
    Evidence basis, Venues, Story by Section (its mind map). The Roadmaps are the Plan's.
    Returns [(tab name, its small line, its panel)]."""
    text, parts = _face(topic)
    rel = lambda p: "/" + quote(ds._rel(p, root))
    tabs = []
    if "pitch" in parts:
        one = _field(parts.get("identity", ""), "One-sentence identity")
        pitch = _plain(parts["pitch"])
        lead = _clean(one) or _clean(re.split(r"(?<=[.;])\s", pitch, maxsplit=1)[0])
        rest = pitch if one else (re.split(r"(?<=[.;])\s", pitch, maxsplit=1) + [""])[1]
        # the stage is the bar's word, so not again under the sentence; the rest a sentence a line, the Pitch's moves
        # (tension, what we do, the answer, who cares), a pending answer a muted chip (Paper-CMS-AI-Usage 261110)
        tabs.append(("Pitch", "the paper in short", STORY_CSS + f'<div class=pb-story><p class=pb-big>{_chips(_cap(lead))}</p>'
                     + (f'<ul class=pb-lines>{"".join(f"<li>{_chips(x)}</li>" for x in _sentences(rest))}</ul>' if rest else "")
                     + '</div>'))
    rq = parts.get("research questions", "")
    qs, said = _rq_lists(rq)
    if qs:                                       # each question with what it lets the paper say, one story (261110)
        reports = dict(re.findall(r"Q0*(\d+)\s*(\[[^\]]+\]\([^)]+\))", rq))
        whole = re.search(r"\*\*The paper's question\*\*:?\s*(.+)", rq)
        context = _rq_context(rq)
        cols = [name for i, (_, name) in enumerate(RQ_CONTEXT) if any(v[i] for v in context.values())]
        heads = ["", "Question"] + cols + ["Expected", ""]        # the last column: each row's card marks (cards.md §7)
        cards, owner = _cards(topic, root)
        body = ""
        for k, q in qs:                              # k: the item's own number (a story may start at RQ0)
            m = re.match(r"(.+?\?)\s*(.*)$", q)
            ask, state = (m.group(1), m.group(2)) if m else (q, "")
            link = _open_link(reports.get(str(k), ""), topic, root)
            ctx = dict(zip([n for _, n in RQ_CONTEXT], context.get(k, ("", "", ""))))
            cells = ([f'<td class=k>RQ{k}</td>', f'<td data-h="Question">{_chips(ask)}</td>']
                     + [f'<td data-h="{esc(c)}">{esc(ctx.get(c, ""))}</td>' for c in cols]
                     + [f'<td data-h="Expected">{_chips(_plain(said.get(k, "")))}{" " + link if link else ""}</td>'])
            # no State column: every question reads "nothing yet" until a Run returns (JL 261111: "no need for this, drop it")
            body += (f'<tr data-addr="RQ.RQ{k}">' + "".join(cells) + f'<td class=im-c>{IM.marks(f"RQ.RQ{k}", cards)}</td></tr>'
                     + IM.card_slot(f"RQ.RQ{k}", cards, owner, cols=len(heads), words=_plain(ask)))   # its address (cards.md §2)
        table = (f'<table class=pb-rqtab><thead><tr>{"".join(f"<th>{esc(h)}</th>" for h in heads)}</tr></thead>'
                 f'<tbody>{body}</tbody></table>')
        # one row per question, every field side by side (JL 261111: "why you don't just add more columns????? so hard
        # to review and read"); a compared table takes the card's width, the paper's question keeps the reading measure
        tabs.append(("Research Questions", "what it asks", STORY_CSS + RQ_TABLE_CSS + IM.ASSETS + _rq_head(whole, cards, owner) + table))
    elif (keyed := _rq_table(rq))[1]:               # §3 as one keyed table (H1, "H2 check", RQ1): the same table, its rows
        heads, rows = keyed                          # its own columns, each row addressed by its key (cards.md §2)
        whole = re.search(r"\*\*The paper's question\*\*:?\s*(.+)", rq)
        cards, owner = _cards(topic, root)
        span = len(heads) + 2                        # the key, its columns, the marks
        ask = lambda cells: _plain(next((c for h, c in zip(heads, cells) if "question" in h.lower()), ""))
        body = "".join(f'<tr data-addr="RQ.{esc(key)}"><td class=k>{esc(label)}</td>'
                       + "".join(f'<td data-h="{esc(h)}">{_chips(_plain(c))}</td>' for h, c in zip(heads, cells))
                       + f'<td class=im-c>{IM.marks("RQ." + key, cards)}</td></tr>'
                       + IM.card_slot("RQ." + key, cards, owner, cols=span, words=ask(cells))
                       for key, label, cells in rows)
        table = (f'<table class=pb-rqtab><thead><tr><th></th>{"".join(f"<th>{esc(h[:1].upper() + h[1:])}</th>" for h in heads)}'
                 f'<th></th></tr></thead><tbody>{body}</tbody></table>')
        tabs.append(("Research Questions", "what it asks", STORY_CSS + RQ_TABLE_CSS + IM.ASSETS + _rq_head(whole, cards, owner) + table))
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
            # the desk editor's question for this topic, answered (JL 261111: "why the editor want to consider this?")
            # the editor's test report, a fresh-context desk screen (reports/qNN_editor_test_<venue>/), opens by its button
            # (JL 261111: "I might want to see the details about it")
            et = next((f for f in sorted(board.glob(f"reports/q*_editor_test_{slug.replace('-', '')}*/q*_editor_test_*.md"))), None)
            et_btn = (" " + _open_btn("Open the editor's test", _page_url(et, root), "editor's test")) if et else ""
            # how to pass the desk: the report's "To raise the odds" list, each change's first sentence (JL 261111: "the
            # suggestions about how could I improve to pass the desk rejection")
            fixes = []
            if et:
                m = re.search(r"\*\*To raise the odds\*\*\s*\n+((?:\s*\d+\..+\n?)+)", et.read_text(encoding="utf-8"))
                fixes = [re.split(r"(?<=[.?!])\s", _plain(x).strip(), maxsplit=1)[0]
                         for x in re.findall(r"(?m)^\s*\d+\.\s*(.+)$", m[1])] if m else []
            panels.append(_kv((("Editor's test", esc(_plain(v.get("editor's test", "") or v.get("editor test", "")))
                                + (f"<br>{et_btn}" if et_btn else "")),
                               ("To pass the desk", f'<ol style="margin:0;padding-left:1.3em">{"".join(f"<li>{esc(x)}</li>" for x in fixes)}</ol>'
                                if fixes else ""),
                               ("Why it fits", esc(_plain(v.get("why it fits", "")))), ("Leads with", esc(_plain(v.get("leads with", "")))),
                               ("Still needs", esc(_plain(v.get("still needs", "")))),
                               ("Desk rules", f'<a class=fd-btn data-pop="{esc(slug)}" href="/_board/page?path={rel(call)}">Open call.md</a>'
                                if call.is_file() else esc(_plain(v.get("desk record", ""))) or "none yet"),
                               ("Related papers", rp),
                               ("All journals", _open_btn("Compare all journals", _page_url(topic / "delivery" / "venue-comparison.md", root), "venue comparison")
                                if (topic / "delivery" / "venue-comparison.md").is_file() else ""))))
        full = topic / "delivery" / "venue-comparison.md"
        tabs.append(("Venues", "where it is sent", _side_cards("ve", tiles, panels) + ("" if full.is_file() else md(_after_table(parts["venues"]), topic))))
    if "section narrative" in parts:                 # the narrative IS the mind map (JL 261031)
        tabs.append(("Story by Section", "what each Section says", _narrative(topic, root, parts["section narrative"], md) or md(parts["section narrative"], topic)))
    return tabs


