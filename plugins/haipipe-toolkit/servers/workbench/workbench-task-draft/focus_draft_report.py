"""The draft Task's Report views: the text as it reads, its references, a response letter's replies, and its status."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import quote
from live import draft_steps as ds
from live.frame import esc, face
from live.ui_parts import _section
from live.focus_draft_words import WAITS, WORK
from live.focus_draft_assets import CSS
from live.focus_draft_steps import _facts, flatten, word

# ── Report: check ───────────────────────────────────────────────────────────────────────────────────
def paragraphs(folder: Path) -> list:
    """[(paragraph id, its name, its text)] of the face's adopted `## Content` (`#### C1.P1 · Background · s1 to s2`)."""
    md = face(folder)
    text = md.read_text(encoding="utf-8", errors="ignore") if md else ""
    text = text.split("\n## Content", 1)[1] if "\n## Content" in text else ""
    text = re.split(r"(?m)^## ", text, maxsplit=1)[0]
    out = []
    for head, body in re.findall(r"(?ms)^#### (.+?)\n(.*?)(?=^#{2,4} |\Z)", text):
        pid, _, rest = head.partition(" · ")
        body = "\n".join(line for line in re.sub(r"<!--.*?-->", "", body, flags=re.S).splitlines()
                          if not line.lstrip().startswith(">"))   # a working note (> Value:, > Note:) is not the text
        words = " ".join(body.split())
        out.append((pid.strip(), rest.split(" · ")[0].strip(), words))
    return out


CONTENT_CSS = ("<style>.fd-sents{margin:2px 0 12px;padding-left:2.1em;line-height:1.55;font-size:15px}"
               ".fd-sents li{margin:0 0 4px;padding-left:2px}.fd-sents li::marker{color:var(--muted);font-size:11.5px}"
               ".fd-cite{color:var(--muted);font-size:.88em}.fd-content h4{margin:12px 0 4px;font-size:14px}</style>")


def bib_entries(folder: Path) -> dict:
    """{key: {title, year, doi, author, file}} of a Section's own bib (draft/evidence/bibex/*.bib, the one its build
    prints from), in file order."""
    out = {}
    for f in sorted((folder / "draft" / "evidence").glob("**/*.bib")) if (folder / "draft" / "evidence").is_dir() else []:
        text = f.read_text(encoding="utf-8", errors="ignore")
        for m in re.finditer(r"@\w+\s*\{\s*([^,\s]+)\s*,(.*?)(?=^@|\Z)", text, re.S | re.M):
            field = lambda k: re.sub(r"[{}]", "", (re.search(rf"(?im)^\s*{k}\s*=\s*[{{\"](.*?)[}}\"]\s*,?\s*$", m.group(2)) or [None, ""])[1])
            out.setdefault(m.group(1), {"title": field("title"), "year": field("year"), "doi": field("doi"),
                                        "author": field("author"), "file": f})
    return out


def bib_href(folder: Path, root: Path | None, key: str) -> str:
    """Where a [key] in the text opens: its row under Work › 3 · Evidence (r03: the keys linked nowhere)."""
    if root is None:
        return ""
    from live.board_read import _task_url
    return _task_url(folder, root, "evidence") + f"#bib-{quote(key)}"


def content_read(folder: Path, root: Path | None = None) -> str:
    """A Section's adopted Content to read (its `## Content` paragraphs), each under its name, a sentence a numbered
    line, a citation command as its keys: the one way a Section's text is drawn on its own page and on its version's
    Draft views (r02: Text showed raw \\citep keys while Draft-Main showed [keys]). With `root`, each key links to its
    bib entry under Work › Evidence; a key not in the Section's bib says so on hover."""
    paras = [(name or pid, t) for pid, name, t in paragraphs(folder) if t]
    if not paras:
        return ""
    try:
        from live.outline_revise import split_sentences
    except ImportError:
        split_sentences = lambda t: [t]
    bib = bib_entries(folder) if root is not None else {}

    def key(k: str) -> str:
        k = k.strip()
        if root is None:
            return esc(k)
        if k in bib:
            return f'<a href="{esc(bib_href(folder, root, k))}" title="{esc(bib[k]["title"])}">{esc(k)}</a>'
        return f'<span title="not in this Section\'s bib">{esc(k)} ⚠</span>'
    cite = lambda h: re.sub(r"\\cite[pt]?\{([^}]*)\}", lambda m: '<span class=fd-cite>[' + ", ".join(key(k) for k in m.group(1).split(",")) + ']</span>', h)
    return CONTENT_CSS + '<div class=fd-content>' + "".join(
        f'<h4>{esc(h)}</h4><ol class=fd-sents>' + "".join(f'<li>{cite(esc(x))}</li>' for x in split_sentences(t)) + '</ol>'
        for h, t in paras) + '</div>'


def text_count(folder: Path) -> str:
    n = sum(1 for _, _, t in paragraphs(folder) if t)
    return "adopted" if n else ""                # no paragraph count on a bar or tab (AGENTS § Page words)


READ_ONLY = ("<style>.fd-read .rv-acts,.fd-read .nt-acts,.fd-read .nt-box,.fd-read .nt-plus,.fd-read .nt-gut,"
             ".fd-read .rv-accept-all{display:none!important}</style>")


def text_html(folder: Path, root: Path) -> str:
    """The Section at sentence level (JL 261031: "why there are no things like sentence level, and the tracking, and
    the evidence etc. left and right panel"): the newest draft, one sentence a row with its S number, and on the right
    each sentence's cards, in reading order: its evidence, its changes (old to new, the tracking), the review's logic
    and the comments, each kind switched on or off above. Report checks, so the cards are read here, never decided:
    Accept, Reject and comments are Work › 5 · Revise's. A draft not yet written shows the adopted Content."""
    board = reply_board(folder, root)            # a response letter: each reply beside its point (r02: six identical
    if board:                                    # "no evidence" cards beside the replies)
        return answers_line(folder, root) + CSS + board
    f = ds.facts(folder, root)
    d = f["draft"]
    if d and d["text"]:
        token = ds.FLAT.set(True)
        try:
            board = ds._text_and_cards(d, f["ev"], root, f["revise"], folder)
            if "No Revise cards yet" in board:          # no pass yet: each sentence beside its evidence and open points
                board = ds._text_and_evidence(d, f["ev"], root, ds._open_points(d), f["displays"])
        finally:
            ds.FLAT.reset(token)
        if board:                                # the text is what the view is for: it starts open (261106)
            return (answers_line(folder, root) + CSS + READ_ONLY
                    + f'<div class=fd-read>{flatten(board).replace("<section class=fd-sec>", "<section class=fd-sec data-open>", 1)}</div>')
    if paragraphs(folder):
        return answers_line(folder, root) + CSS + _section_open("📝 The text", content_read(folder, root), text_count(folder))
    return '<p class=mut>No text yet: 2 · Write writes it.</p>'


def _section_open(title: str, body: str, word: str = "") -> str:
    return _section(title, body, word).replace("<section class=fd-sec>", "<section class=fd-sec data-open>", 1)


# ── a letter that answers comments (a response letter's `responds-to:`): the comments report linked, and each of its
# Review Items beside the reply that answers it (r01: "open the reviewers' comments it answers: could not") ─────────
def md_tables(text: str) -> list:
    """Every Markdown table of a text, each a list of dicts by its header."""
    out, rows, head = [], None, None
    for line in text.splitlines() + [""]:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not line.lstrip().startswith("|"):
            if rows is not None:
                out.append(rows)
            rows, head = None, None
        elif head is None:
            head, rows = cells, []
        elif not set("".join(cells)) <= set("-: "):
            rows.append(dict(zip(head, cells + [""] * (len(head) - len(cells)))))
    return out


def responds_to(folder: Path) -> Path | None:
    """The comments report a page answers (its face's `responds-to:`), else None."""
    md = face(folder)
    m = re.search(r"(?m)^responds-to:\s*(\S+)", md.read_text(encoding="utf-8", errors="ignore")) if md else None
    hit = (folder / m.group(1)).resolve() if m else None
    return hit if hit is not None and hit.is_file() else None


def review_items(report: Path) -> list:
    """[(the point, who raised it, the Section it lands on, its reply paragraph, its state)] from a comments report's
    Feedback Concern Table and Review Items."""
    tables = md_tables(report.read_text(encoding="utf-8", errors="ignore"))
    concerns = {r.get("item", ""): r for t in tables for r in t if r.get("concern")}
    items = next((t for t in tables if t and "lands on" in t[0]), [])
    out = []
    for r in items:
        c = concerns.get(r.get("cites", ""), {})
        out.append((c.get("concern") or r.get("item", ""), c.get("source", ""), r.get("lands on", ""), r.get("reply", ""),
                    r.get("state", "") or c.get("state", "")))
    return out


def review_points(report: Path, letter: Path | None) -> list:
    """review_items, each reply read from the letter when the report names none: the one paragraph whose name names who
    raised the point ("Reply to Reviewer 1 on …"), its state answered (r02: the report said "routed" for two points
    while the letter held a reply to each, so the Answers line said "1 of 3" beside three replies)."""
    items = review_items(report)
    if letter is None:
        return items
    paras = [(pid.split(".")[-1], name) for pid, name, t in paragraphs(letter) if t]
    taken = {reply for _, _, _, reply, _ in items if reply}
    out = []
    for point, who, lands, reply, state in items:
        if not reply and who:
            hits = [p for p, name in paras if p not in taken and re.search(rf"\b{re.escape(who)}\b", name, re.I)]
            if len(hits) == 1:
                reply, state = hits[0], "answered"
                taken.add(reply)
        out.append((point, who, lands, reply, state))
    return out


REPLY_CSS = ("<style>.fd-reply{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:8px 18px;padding:10px 0;"
             "border-bottom:1px solid var(--line)}.fd-reply h4{margin:0 0 4px;font-size:14px}"
             ".fd-point{border:1px solid var(--line);border-left:3px solid light-dark(#2b8a3e,#8bd49a);border-radius:8px;"
             "padding:7px 11px;font-size:13.5px}.fd-point.open{border-left-color:light-dark(#b35c00,#ffc078)}"
             ".fd-point b{display:block;margin:0 0 4px}.fd-point small{display:block;color:var(--muted)}"
             "@media(max-width:700px){.fd-reply{grid-template-columns:minmax(0,1fr)}}</style>")


def reply_board(folder: Path, root: Path) -> str:
    """A response letter's text, each reply paragraph beside the reviewer's point it answers (who raised it, where it
    lands, its state); a point with no reply yet listed after them. "" for any other Section."""
    report = responds_to(folder)
    paras = [p for p in paragraphs(folder) if p[2]]
    if report is None or not paras:
        return ""
    try:
        from live.outline_revise import split_sentences
    except ImportError:
        split_sentences = lambda t: [t]
    points = review_points(report, folder)
    by_reply = {reply: (point, who, lands, state) for point, who, lands, reply, state in points if reply}

    def card(point, who, lands, state):
        done = state in ("answered", "applied")
        return (f'<div class="fd-point{"" if done else " open"}"><b>{esc(point)}</b>'
                + "".join(f'<small>{esc(k)}: {esc(v)}</small>' for k, v in (("raised by", who), ("lands on", lands),
                                                                           ("state", state or "open")) if v) + '</div>')
    rows = ""
    for pid, name, text in paras:
        hit = by_reply.get(pid.split(".")[-1])
        rows += (f'<div class=fd-reply><div><h4>{esc(pid)} · {esc(name)}</h4><ol class=fd-sents>'
                 + "".join(f"<li>{esc(x)}</li>" for x in split_sentences(text)) + '</ol></div><div>'
                 + (card(*hit) if hit else '<p class=mut>No Review Item names this reply.</p>') + '</div></div>')
    left = [(point, who, lands, state) for point, who, lands, reply, state in points if not reply]
    rows += "".join(f'<div class=fd-reply><div><p class=mut>No reply yet.</p></div><div>{card(*x)}</div></div>' for x in left)
    return CONTENT_CSS + REPLY_CSS + _section_open("✉️ Each reply beside the point it answers", rows)   # each row its state


def answers_line(folder: Path, root: Path) -> str:
    """One line above a response letter's text: the comments it answers, opening the report (no answered tally)."""
    report = responds_to(folder)
    if report is None:
        return ""
    from live.frame import reader
    return (CSS + f'<div class=fd-ask role=status><span class=n>Answers</span><span class=d>{esc(report.parent.name)}'
            f'</span><a class=fd-btn data-pop="{esc(report.parent.name)}" href="{esc(reader(report, root))}">Open the comments</a></div>')


STATUS_WHAT = {"done": "done", "next": "comes next", "sign": "waits for your sign", "asked": "waits for your ticks",
               "send": "built, waits for your send", "optional": "optional", "pass": "pass {k}: cards wait for you",
               "todo": "later", "early": "written before the plan was signed: back to 1 · Plan"}


def status_html(folder: Path, root: Path, url) -> str:
    """The Section's aims and opening (what it must do, when it is done, where it is now), then each step, one row: its
    name, what it waits for in its state's colour, Go (into Work, or the rail's section)."""
    f, st, k = _facts(folder, root)
    now = now_line(st, k)                        # "Now" from the steps, never the face's typed word (r03: "not started"
    rows = [f'<div class=fd-row><span class=n>{esc(n)}</span><span class=d>{esc(now if n == "Now" else v)}</span></div>'
            for n, v in aims(folder)]            # stood over "2 paragraphs, adopted")
    if not any(n == "Now" for n, _ in aims(folder)):
        rows.insert(0, f'<div class=fd-row><span class=n>Now</span><span class=d>{esc(now)}</span></div>')
    for step in ds.STEPS:
        key = dict((s, kk) for kk, s in WORK).get(step)
        if key == "display" and not f["displays"]:   # Work shows no Display then, so its row would open Plan (261105)
            continue
        href = url("report", key) if key else url(step.lower(), "")
        w, cls = word(st[step], k)
        rows.append(f'<div class=fd-row><span class=n>{esc(step)}</span><span class="d {cls}">{esc(STATUS_WHAT[st[step]].format(k=k))}'
                    f'</span><a class=fd-btn href="{esc(href)}">Go</a></div>')
    return CSS + "".join(rows)


def now_line(st: dict, k: int = 1) -> str:
    """Where the Section stands, from its steps: the steps done, then the one that waits for the person or comes next."""
    steps = [step for _, step in WORK if step in st]
    done = [step.split(" · ")[1] for step in steps if st[step] == "done"]
    wait = next((step for step in steps if st[step] in WAITS), None)
    nxt = next((step for step in steps if st[step] == "next"), None)
    bits = ([f"{', '.join(done)} done"] if done else []) + \
           ([f"{wait.split(' · ')[1]} {STATUS_WHAT[st[wait]].format(k=k)}"] if wait else
            [f"{nxt.split(' · ')[1]} comes next"] if nxt else [])
    return "; ".join(bits) or "not started"


def aims(folder: Path) -> list:
    """[(name, words)] of the face's `## Aims` (Target · Done when · Now) and the first line of its `## Opening`
    (r02: they showed nowhere on the Section's page)."""
    md = face(folder)
    text = md.read_text(encoding="utf-8", errors="ignore") if md else ""
    sec = lambda name: (re.search(rf"(?ms)^## {name}\s*\n(.*?)(?=^## |\Z)", text) or [None, ""])[1].strip()
    out = []
    for line in sec("Aims").splitlines():
        for part in line.lstrip("- ").split(" · "):
            k, _, v = part.partition(":")
            if v.strip() and k.strip() in ("Target", "Done when", "Now"):
                out.append((k.strip(), v.strip()))   # "Target", as the face says (r03: two "Aim"s on one page)
    opening = " ".join(sec("Opening").split())
    if opening:
        out.append(("Opening", opening[:280] + ("…" if len(opening) > 280 else "")))
    return out


def report_views(folder: Path, root: Path, url) -> dict:
    """Report's views after MindMap: Text, Status (the base adds MindMap first and Questions last). The review report
    is Work › 5 · Revise's, beside the cards it judges (JL 261031: "the revise should be in the Work Section")."""
    return {"text": ("Text", lambda: text_html(folder, root)),
            "status": ("Plan + Results", lambda: status_html(folder, root, url))}
