"""A paper Board's Work Details (Idea · Story · DataFlow · PaperFlow, then its Jobs), the card helpers its steps draw with,
and an older Board's Story Job. Moved from paper_theme.py, which re-exports every name here so
`from live.paper_theme import _board_work` keeps working."""
from __future__ import annotations

import re

from live import paper as P
from live.frame import Space, esc, link, pop, reader, rel, table, work_tree
from live.paper_theme import THEME, _data, _empty, _kv, _pick, _run_cards, _studio
from live.paper_theme_report import _report


# The Board's Work (JL 261020: "Like in the work, we might also have Studio (studio is already in the top), and then
# the Idea, and then the Story, and DataFlow, and PaperFlow ... and later we can have many Jobs"): the paper's own
# steps before its versions, each Operation over Result as a Section's seven steps are (draft_steps), then its Jobs.
BOARD_STEPS = ("Idea", "Story", "DataFlow", "PaperFlow", "Jobs")
OLD_BOARD_SUBS = {"Main": "Jobs", "Appendix": "Jobs", "Evidence": "Jobs"}     # the old Work Details tabs still open
# step → (emoji, the Studio group whose topics it reads, a word the topic's name must hold, its prompt)
BOARD_STEP = {
    "Idea": ("💡", "Ideation", "", "/hai-paper ideate {b}: read {t} and the related work (s10 to s14) and my "
             "notes; add or test ideas, each with its question, its novelty against the closest work and a verdict; "
             "then redraw the topic."),
    "Story": ("📖", "Story", "", "/hai-paper story {b}: read the ideas that went to a story and my notes; tell the paper "
              "in {t} (the tension, what we do, the answer so far, who cares) and its research questions, one "
              "Board Question each; then redraw the topic."),
    "DataFlow": ("🔀", "Plan", "dataflow", "/hai-paper-plan {b} dataflow: read the Story's research questions and the "
                 "Runs on disk; draw in {t} how the data becomes each answer (inputs, the Runs, what each feeds), "
                 "with what is still to run; then redraw."),
    "PaperFlow": ("🗺", "Plan", "workflow", "/hai-paper-plan {b} paperflow: read the Story, the DataFlow and my notes; "
                  "draw in {t} how the answers become the paper (the Sections, the displays and the Run behind "
                  "each, the dates to the send); then redraw."),
}


def _board_topics(block, group, word=""):
    """The Board's sNN topics of one group (their **Tags:** line), whose name holds `word`: beside the Jobs, then studio/."""
    out = []
    for topic in P.board_topics(block):
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


def _board_step(name, topics, state, block, root, d=None):
    """One step: its Operation (Input, Prompt) over its Result (each topic's drawing, opened, then what is open and
    what was decided)."""
    from live.draft_steps import _part, _prompt_box, _step_box
    from live.frame import _draw_url
    from live.paper_theme_story import _flow_sections, _idea_cards, _story_sections, _sub
    emoji, group, word, prompt = BOARD_STEP[name]
    first = topics[0][0].name if topics else f"sNN-{(word or group).lower()}"
    rows = [("Topics", ", ".join(esc(t.name) for t, _x in topics) or f'<span class=mut>none yet in the {esc(group)} group</span>')]
    for topic, text in topics[:1]:
        stage = re.search(r"(?m)^\*\*Stage:\*\*\s*(.*)$", text)
        rows += [("What", esc(_topic_what(text)) or "—"), ("Stage", esc(stage.group(1).strip()) if stage else "—")]
    ask = prompt.format(b=rel(block, root), t=topics[0][0].relative_to(block).as_posix() if topics else first)
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
                 + (_folded("✅ Decided", "", "<ul>" + "".join(f"<li>{P.inline(x)}</li>" for x in decided) + "</ul>")
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


# ── an older Board's Story group (A1-Story/, an earlier j00_story/) read as a Job; on the ladder the Story is
# studio topics and Questions (b16 Q04) and this view is not reached ─────────────────────────────────────
STORY_AR = ("Ideation", "Narrative")


def _story_pages(d, board, job):
    from live.paper_theme_version import _mine
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
