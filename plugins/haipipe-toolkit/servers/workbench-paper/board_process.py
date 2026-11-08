"""A paper Board's PROCESS band (b16 s33-D06, D07): step by step, one row per thing to do with its state pill and
its verb, the decisions waiting for you, Plan's plan center (Open, the skill, Copy prompt), and the skills."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote

from live import draft_steps as ds
from live.frame import esc
from live.ui_parts import _cap, _plain, _plan_html, _section, _todo, plural_word, todo_section
from live.focus_draft import WORK
from live.board_read import BOARD_PARTS, DOT_REF, view_topics, _face, _field, _num, _open_list, _page_url, _section_state, _state_words, _table, _task_url, _waits, board_topic, explore_tree, is_version, md_table, part_topics
from live.board_interactions import answers_of
from live.board_evidence import EVIDENCE_KINDS, evidence_body


# ── every Board view in two bands, PROCESS and RESULTS, each numbered from 1 (JL 261101: "the index for each section
# should be 1, 2, ... 1, 2, 3"; "the results should be consistent to the report"): RESULTS is the Report view itself,
# the same on Report and Work; PROCESS is how this layer is being made: 1 Interactions (Report: what was decided;
# Work: what waits on you), 2 its open points or where each item stands, 3 the skills that do it (Work; JL 261101:
# "show what is the skills related to each UI"). PROCESS is Work's only (s32-D27) ─────────────────────
VIEW_SKILLS = {
    "idea": (("haipipe-paper-ideation", "picks the direction and the target, through your gate"),
             ("haipipe-ideation", "finds candidate ideas and tests their novelty and fit")),
    "story": (("haipipe-paper-story", "writes the questions, hypotheses, claims and Section narrative"),
              ("haipipe-paper-venue", "keeps each journal's desk rules, venues/<venue>/call.md"),
              ("haipipe-paper-related", "maps the closest related papers, beside ours")),
    "plan": (("haipipe-paper-plan", "draws how the data becomes each answer, then the Sections and dated steps to the send"),
             ("haipipe-report", "keeps each Board Question and its report"),
             ("haipipe-task", "runs each Task's Runs and keeps their Results"),
             ("haipipe-paper", "routes the paper's work to the skill that owns it")),
    "explore": (("haipipe-work", "the work Blocks, Jobs, Tasks and Runs"),
                ("haipipe-discovery", "the discovery Blocks: each paper read by a Run")),
    "evidence": (("haipipe-paper-evidence", "checks the values and citations as one ledger"),
                 ("haipipe-evidence", "lands each Evidence Item from its Results")),
    "displays": (("haipipe-paper-plan", "plans each display against the venue's rules (the display plan)"),
                 ("haipipe-display", "draws each table and figure, then its review loop"),
                 ("haipipe-paper-evidence", "each version's preview.pdf, as the paper prints it")),
    "draft": (("haipipe-paper-draft", "drafts one Section through its steps"),
              ("haipipe-draft-writing", "writes and revises the prose"),
              ("haipipe-paper-assemble", "builds the whole paper: the PDF and the Word files")),
}


def _state_of(raw: str) -> str:
    """A table's state cell as one pill word: ✅ done, ⏳ running, ⬜ waiting for you or not started."""
    raw = _plain(raw or "")
    if raw.startswith("✅"):
        return "done"
    if raw.startswith("⏳"):
        return "running"
    if re.search(r"waiting for (JL|you)|waits on you|your (sign|call)", raw, re.I):
        return "waiting for you"
    return "not started" if raw.startswith(("⬜", "○")) or not raw else _cap(re.split(r"[;:(,.]", raw.lstrip("⬜✕ "))[0].strip())[:28]


def _steps(board: Path, key: str, topic, text: str, root: Path, md):
    """(title, rows): this view's things to do, in order, each (words, under, state, verb, href, pop)."""
    wb = lambda d: "/_board/workbench?" + "&".join(f"{a}={quote(b)}" for a, b in (("path", ds._rel(d, root)), ("layout", "focus")))
    if key == "dataflow":                      # the Story's T table: each Run to do, T0 first
        story = board_topic(board, "story", r"s\d+-story")
        f = story / f"{story.name}.md" if story is not None else None
        rows = []
        for r in (md_table(f.read_text(encoding="utf-8", errors="ignore"), "T") if f and f.is_file() else []):
            if r.get("state", "").lstrip().startswith("✕"):
                continue
            m = DOT_REF.search(r.get("where", ""))
            own = next((d for d in board.parents if (d / "work").is_dir()), None)
            hit = None
            if m and own is not None:
                hit = next(iter(sorted((own / "work").glob(f"b{m.group(1)}_*/j{m.group(2)}_*" + (f"/t{m.group(3)}_*" if m.group(3) else "")))), None)
            rows.append((f'{r.get("T", "")} · {_plain(r.get("work", ""))}', _plain(r.get("what it gives", ""))[:90],
                         _state_of(r.get("state", "")), "Open", wb(hit) if hit else "", False))
        rows.sort(key=lambda x: int(re.sub(r"\D", "", x[0].split(" · ")[0]) or 0))
        return ("Runs to do", rows) if rows else ("", [])
    if key == "paperflow":                     # the dated steps not done yet, by date
        _, parts = _face(topic) if topic is not None else ("", {})
        steps = sorted(_table(parts.get("timeline", "")), key=lambda r: _plain(r.get("when", "")))
        rows = [(f'{_plain(r.get("when", ""))} · {_plain(r.get("step", ""))}', _plain(r.get("who", "")), _state_of(r.get("state", "")), "", "", False)
                for r in steps if not _plain(r.get("state", "")).startswith("✅")]
        return ("Next steps to the send", rows) if rows else ("", [])
    if key in ("evidence", "displays"):        # each item, in RESULTS' order, its state
        jobs = [d for d in sorted(board.glob("j[0-9]*_*")) if d.is_dir() and not is_version(d)]
        rows = []
        mine = ("Displays",) if key == "displays" else ("Values", "Citations")
        for kind, pat in sorted((k for k in EVIDENCE_KINDS if k[0] in mine), key=lambda k: ("Values", "Citations", "Displays").index(k[0])):
            job = next((j for j in jobs if re.search(pat, j.name, re.I)), None)
            for t in (sorted((x for x in job.glob("t[0-9]*_*") if x.is_dir()), key=_num) if job else []):
                label, status, _ = evidence_body(t, root)
                words = re.sub(r"^(?:e?figure|e?table|values|cite)\d*\s*", "", re.sub(r"^t\d+_", "", t.name).replace("-", " "), flags=re.I)
                head = label if label and label.lower() not in ("values", "citations") else _cap(words)
                st = (status or "").lower()
                pill = ("not started" if re.search(r"\b(?:not|un)[\s-]*(?:yet\s+)?(?:checked|drawn|filled|done)", st)   # "not drawn" is not done
                        else "done" if re.search(r"checked|drawn|filled|done", st)
                        else "waiting" if st.startswith("wait") else _cap(status or "not started")[:28])
                name = f"{kind} · {head}"
                if kind == "Displays":           # its plan name, as RESULTS shows it: Figure 1 (Display A) · 📈 Figure · <name>
                    from live.board_results import _display_line, display_plan
                    dp = display_plan()
                    plan = {r.get("display", ""): r for r in (dp.rows(board) if dp else [])}
                    face = t / f"{t.name}.md"
                    ks = dp.keys(face.read_text(encoding="utf-8", errors="ignore")) if dp and face.is_file() else []
                    r = next((plan[k] for k in ks if k in plan), None)
                    lab = dp.title(r) if r else head
                    name = f"{lab} · {_display_line(t, words)}"
                line = ""
                if kind != "Displays":           # what its Run returned, in the version's and the Job's words (r03:
                    from live.evidence_read import task_state   # a pill cut a coded headline, "0 card-o")
                    line, pill = task_state(t, status)
                rows.append((name, line, pill, "Open", _task_url(t, root), False))
        return ("Where each display stands" if key == "displays" else "Where each stands", rows) if rows else ("", [])
    if key == "draft":                         # each Section's next step, a verb that opens it
        rows = []
        for job in sorted(d for d in board.glob("j[0-9]*_*") if d.is_dir() and is_version(d)):
            for t in sorted((x for x in job.glob("t[0-9]*_*") if x.is_dir()), key=_num):
                say = _state_words(_section_state(t, root))
                step, _, st = say.partition(": ")
                name = _cap(re.sub(r"^t\d+_", "", t.name).replace("-", " "))
                pill = "done" if say == "done" else "waiting for you" if "your" in st else st or "not started"
                gk = next((k for k, s_ in WORK if step and s_.endswith(step)), "")
                rows.append((name, f"{job.name} · next: {step}" if step and say != "done" else job.name, pill,
                             f"Open {step}" if step and say != "done" else "Open", _task_url(t, root, gk), False))
        return ("Sections to finish", rows) if rows else ("", [])
    waits = _open_list(text)                   # idea, story, explore: the topic's open points
    rows = [(_plain(w)[:140], "", "open", "", "", False) for w in waits]
    return ("Open", rows) if rows else ("", [])


def read_board(board: Path) -> str:
    return (board / "board.md").read_text(encoding="utf-8", errors="ignore")


def _plan_steps(board: Path, root: Path) -> list:
    """Plan's plan center (JL 261101: "the design of the dataset, the design of the regression, and how to make them
    run ... the plan center for the work and discovery"; "just open it, and just say use this skill, and copy it"): each
    step (title, what it covers, the skill, Open's href, the prompt to copy). The prompt sends a session to the thing,
    has it screenshot the mind map, and asks for a plan before any change."""
    rel = lambda p: ds._rel(p, root)
    url = lambda p: "/" + quote(rel(p))
    wb = lambda d: "/_board/workbench?" + "&".join(f"{a}={quote(b)}" for a, b in (("path", rel(d)), ("layout", "focus")))
    flow = board_topic(board, "dataflow", dict((k, pat) for k, _, pat in BOARD_PARTS)["dataflow"])
    story = board_topic(board, "story", r"s\d+-story")
    smd = story / f"{story.name}.md" if story is not None else None
    mind = flow / f"{flow.name}.mindmap.html" if flow is not None else None
    yaml_ = next(iter(sorted(flow.glob("*-drawing.yaml"))), None) if flow is not None else None
    named = explore_tree(board).get("named", {})
    main = max(named, key=named.get) if named else None
    ask = "Show me the plan first; change nothing until I say yes."
    steps = []
    if flow is not None:
        steps.append(("🗂️ Design the dataset", "the data, the linking and the tables each question reads", "haipipe-paper-plan",
                      url(mind) if mind and mind.is_file() else wb(flow),
                      f"Use /haipipe-paper-plan. Open the data-flow mind map {rel(mind) if mind and mind.is_file() else rel(flow)} "
                      f"and take a screenshot of it" + (f"; read {rel(yaml_)}" if yaml_ else "") + ". Check the dataset design: "
                      "the data, the linking and the tables each question reads. Propose how to update the plan, and which work "
                      f"Block, Job and Task builds each table (/haipipe-work). {ask}"))
    if main is not None:
        steps.append(("📈 Design the regressions", f"{main.parent.name} · {main.name}: outcome, treatment, estimator, windows",
                      "haipipe-task", wb(main),
                      f"Use /haipipe-task. Open {rel(main)}, its src/ design files, and the research questions (§3) of "
                      f"{rel(smd) if smd else 'the Story'}. For each question, check the regression design: outcome, treatment, "
                      f"estimator, windows, and which Task and Run test it. Propose the changes as Tasks and Runs in the work theme. {ask}"))
    if smd is not None and smd.is_file():
        steps.append(("⚙️ Make them run", "the Task Roadmap: each Run, its ticket, its state", "haipipe-run", _page_url(smd, root),
                      f"Use /haipipe-run. Read the Task Roadmap (§7, the T table) of {rel(smd)}. For each row not done, check that "
                      "its Run ticket exists and is ready, and build what is missing. Never start a Run: I press Run. Tell me what "
                      "to press, in order."))
        plan = next(iter(sorted(board.glob("s??-paper-displays"))), None)
        pface = plan / f"{plan.name}.md" if plan is not None else None
        steps.append(("🖼️ Plan the displays", "each display, its Run, and the venue's display rules", "haipipe-paper-plan",
                      _page_url(pface, root) if pface and pface.is_file() else _page_url(smd, root),
                      (f"Use /haipipe-paper-plan. Open {rel(pface)} and run display_plan.py check on the Board. "
                       if pface and pface.is_file() else
                       f"Use /haipipe-paper-plan. Make s06-paper-displays for this Board from the questions of {rel(smd)}. ")
                      + "For each research question, check which display carries its answer, what it shows, where it goes "
                        "(main or supplement) and the Run that makes it, against the venue's display rules (venues/<venue>/"
                        f"call.md, its Displays table). {ask}"))
        steps.append(("🔎 Plan the reading", "the Discovery Roadmap: what each question must read", "haipipe-discovery",
                      _page_url(smd, root),
                      f"Use /haipipe-discovery. Read the Discovery Roadmap (§6, the D table) of {rel(smd)}. For each row with no "
                      f"folder yet, propose its discovery Block and Job: the question and the first papers to read. {ask}"))
    return steps


PTD_CSS = ("<style>.pb-ptd{margin:0 0 6px}.pb-ptd>summary{cursor:pointer;font-size:12.5px;color:var(--muted);padding:2px 0}"
           ".pb-ptd[open]>summary{margin-bottom:4px}</style>")


def behind_copy(html: str) -> str:
    """Prompt boxes with their prompt behind Copy prompt (r02: Work › Plan showed five prompts open): each prompt's text
    in a closed "Show the prompt" fold, its session line off the page (Copy prompt still copies both)."""
    html = re.sub(r"<p class=pb-sess>.*?</p>", "", html, flags=re.S)
    return PTD_CSS + re.sub(r"(<pre class=pb-pt>.*?</pre>)", r"<details class=pb-ptd><summary>Show the prompt</summary>\1</details>",
                            html, flags=re.S)


def process_html(board: Path, key: str, root: Path, md, items, work: bool, item_html=None) -> str:
    """The PROCESS band, step by step (b15 s58); a title names the step, never a count (JL's rule: labels carry no
    counts; the pills say each row's state): 1 the decisions waiting for you (Report: decided), one row per
    question; 2 this view's things to do, one row each with its state and its verb; 3 in Work, the skills that do it."""
    from live import frame
    parts = []                                 # (part, its topic, its face's text); a view of two parts reads both
    for part, _, topic in view_topics(board, key):
        face_md = frame._notes(topic)
        parts.append((part, topic, face_md.read_text(encoding="utf-8", errors="ignore") if face_md else ""))
    topics = [t for _, t, _ in parts]
    mine = [r for r in items if r.get("topic") in topics] if topics else \
        [r for r in items if r.get("topic") not in part_topics(board)] if key == "draft" else []
    href = lambda r: f'/{quote(ds._rel(Path(r["form"]), root))}' if r.get("form") else ""
    out, n = "", 0
    if work:                                   # 1 · the open points the parts' faces mark as waiting for you; the open
        # forms' questions are the view's last section, 🙋 Interaction, so they show once (JL 261105: "keep only the
        # bottom"; as Writing's own question row went, 261105); with no open point there is no step
        waits = [(re.sub(r"\s*[⬜✅⏳○]\s*", " ", _plain(ln.lstrip("- ")))[:140].strip(), "", "waiting for you", "", "", False)
                 for _, _, text in parts for ln in _waits(text)]                # the mark is the pill now; shown with the
                                                                                # parts' own Open list, one "📌 Open points"
    else:                                      # 1 · what was decided: each answered question, its pick
        rows = [(f"{q} · {pick}", (f"note: {note}" if note else r["title"]), "Answered", "See answers", href(r), True)
                for r in sorted((x for x in mine if x.get("state") == "answered" and x.get("answers")),
                                key=lambda x: x.get("received", ""), reverse=True)
                for q, pick, note in answers_of(r["answers"])]
        title = "Decisions made" if rows else "No form answered yet"
        n += 1
        out += _section(f"{n} · 🙋 {_cap(title)}", _todo(rows) if rows else "<span hidden></span>",
                        plural_word(len(rows), "decided", "decided") if rows else "nothing yet")
    if key == "plan":                          # 2 · the plan center: design the data, the regressions, run, read
        plan = _plan_steps(board, root)
        if plan:
            n += 1
            session = _field(read_board(board), "session") if (board / "board.md").is_file() else ""   # the Board's own
            out += _section(f"{n} · 🧭 Plan", behind_copy(_plan_html(plan, session, key=f"plan:{ds._rel(board, root)}")),
                            f"runs in {session}" if session else plural_word(len(plan), "prompt", "prompts"))
    # each part's things to do; two parts with the same kind of list (Idea's and Story's Open) read as one
    lists: dict = {}
    for part, topic, text in parts or [(key, None, "")]:
        head, rows = _steps(board, part, topic, text, root, md)
        if rows:
            lists.setdefault((head, part if head != "Open" else ""), []).extend(rows)
    if work and waits:                         # the waiting lines join the Open list, or stand as it (261105: Idea read
        lists[("Open", "")] = waits + lists.get(("Open", ""), [])   # "🚧 Open", Story "📌 Open points")
    for (head, part), rows in sorted(lists.items(), key=lambda kv: kv[0][0] != "Open"):
        n += 1
        if head == "Open":                     # each step's word and waiting line read from its rows' pills (261106)
            out += todo_section(f"{n} · 📌 Open points", rows)
            continue
        emoji = {"dataflow": "⚙️", "paperflow": "🗓️", "evidence": "📋", "displays": "🖼️", "draft": "🪜"}.get(part, "🚧")
        out += todo_section(f"{n} · {emoji} {head}", rows)
    # who does it: the rail's Skills section, once per page (JL 261105); VIEW_SKILLS feeds it
    return out
