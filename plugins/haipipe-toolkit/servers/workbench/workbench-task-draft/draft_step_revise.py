"""5 · Revise of the draft Task (draft_steps.py): the Revise passes and their cards, comments (note_act), card
actions (card_act), the logic and review cards, the sentence board, and the step (_revise); re-exported by draft_steps."""
from __future__ import annotations

import datetime
import difflib
import re
from pathlib import Path
from urllib.parse import quote

from live.frame import _notes, _rel, _table, chain, esc, face
from live.draft_steps_assets import CARDS_CSS, CARDS_JS, NOTES_CSS, NOTES_JS
from live.draft_steps_common import (
    _canvas_card, CARDS, _code, _fold, _header, INK, _inline, _kv, _marks, _md, _not_yet, _paragraphs, _parts,
    _prompt_box, _source, _step_box)
from live.draft_step_evidence import (
    _cite_names, _displays, _embed_displays, EV_STATE, _num, _s_ids, _sx_board, _sx_fill, _sx_paras)
# the passes' cards and the comments moved out (600-line rule); every name stays importable here
from live.draft_step_revise_cards import (  # noqa: F401
    _by, _by_badges,
    _before_passes, _by_sentence, _change, _chosen, _first_pass_title, _is_report, _listed, _old_new, _options,
    _paragraph_plan, _plan_cell, _proposed_cards, _review_chips, _revise_card, _revise_passes, STATE_CHIP)
from live.draft_step_revise_notes import (  # noqa: F401
    _answered_by, card_act, _comments, _comments_path, note_act, _note_card, NOTE_LABEL, NOTE_TARGET)


def _first_para(part: str, d: dict) -> str:
    """The first paragraph id of a part of the text (C2 → C2.P4), where a card on the whole part is placed."""
    body = "\n".join(b for _, b in (d or {}).get("text", []))
    return (re.search(r"(?m)^### (" + re.escape(part) + r"\.P\d+)\b", body) or [None, ""])[1]


def _reading_key(head: str, d: dict) -> tuple:
    """Where a card sits in the text: the Section first, then a paragraph's first sentence, then its own sentence, in
    the order the text reads, which an S number need not follow once a sentence has moved (S5 before S4)."""
    m = re.match(r"[^·]+·\s*(?:S(\d+)([a-z]?)|(C\d+\.P\d+)|(C\d+))\b", head)
    if not m:
        return (10 ** 6, "")
    body = "\n".join(b for _, b in (d or {}).get("text", []))
    order = {sid: i for i, sid in enumerate(re.findall(r"(?m)^- B\d+[a-z]* · (S\d+[a-z]*) · ", body))}
    if m.group(4):                                   # a card on a whole part (C2) sits at its first paragraph, first
        first = _first_para(m.group(4), d)           # among that paragraph's cards
        sec = first and re.search(r"(?ms)^### " + re.escape(first) + r"\b.*?^- B\d+[a-z]* · (S\d+[a-z]*)", body)
        return (order[sec.group(1)] - 0.6, "") if sec and sec.group(1) in order else (-1, "")
    if m.group(1):
        sid = f"S{m.group(1)}{m.group(2)}"
        return (order[sid], "") if sid in order else (int(m.group(1)) + 10 ** 5, m.group(2))
    sec = re.search(r"(?ms)^### " + re.escape(m.group(3)) + r"\b.*?^- B\d+[a-z]* · (S\d+[a-z]*)", body)
    return (order[sec.group(1)] - 0.5, "") if sec and sec.group(1) in order else (10 ** 6, "")


def _text_and_cards(d: dict, ev: dict, root: Path, path: Path, task: Path) -> str:
    """The text on the left and its Revise cards on the right, in reading order (JL 261020: "How do you think we can
    merge them together, one in the left, and one in the right? so we can link to the original text as well"). Only the
    newest pass ("always keep the latest version"); it ends with the prompt that writes the accepted cards into the
    text as the next version.

    The text is one column with no space between its sentences, the same text 2 · Write, 3 · Evidence and 4 · Display
    show (JL 261020: "我不想让句子跟句子之间有这么大的空格 ... 在 revise、evidence、display 这里都保持一样的风格"): a card
    is placed at its sentence's line and pushed down only to clear the card above it (CARDS_JS `align`), the text
    never moves for a card, and it stays in view while the cards scroll. A card on a whole part (`Section question ·
    C2 · …`) is a card like the others, on the right at its part's first paragraph heading (JL 261021, of one above
    the text: "我想知道它是不是应该也当成一个 card 之类的，放到右边去？")."""
    marks = _marks(ev)
    text = "".join((f'<h3 style="margin:14px 0 4px">{esc(t)}</h3>' if len(d["text"]) > 1 else "")
                   + _md(b, marks, _parts(d), rows=True) for t, b in d["text"])
    text = _cite_names(_embed_displays(text, d, _displays(task, d), root), d)
    # a sentence the person checked, while its words are the same (draft_step_revise_notes.checked)
    from live.draft_step_revise_notes import checked
    held = checked(path)
    now_words = {m.group(1): " ".join(m.group(2).split()) for _, b in d["text"]
                 for m in re.finditer(r"(?m)^- B\d+[a-z]* · (S\d+[a-z]*) · (.*)$", b)}
    ok = {s for s, w in held.items() if now_words.get(s) == " ".join(w.split())}
    # a ✓ on an earlier wording is shown as lapsed, so the person sees which sentences to pass again (JL 261114: "when I
    # reload, the C2.P2 is not folded")
    text = re.sub(r'<li data-s="(S\d+[a-z]*)"', lambda m: m.group(0) + (' data-checked="1"' if m.group(1) in ok else
                  ' data-checked="stale"' if m.group(1) in held else ""), text)
    passes = _revise_passes(path)[:1] if path.is_file() else []
    title, cs = passes[0] if passes else ("", [])
    t = _rel(task, root)
    whole = lambda h: re.match(r"[^·]+·\s*(C\d+)\s*·", h)      # `Section question · C1 · …`, not `· C1.P2 · …`
    cs = [(h, c) for h, c in cs if not _is_report(h)]
    cards = sorted(cs, key=lambda x: _reading_key(x[0], d))
    # the pass's review report is its own section above this one (_review_report; JL 261021: "把那些比较详细的 review
    # report 单独作为一个新的 section ... 我还要之前的那个 revised card section")
    top = ""
    # a person's comments sit among the cards, each beside its sentence and before the cards on it, so a comment reads
    # first and the change that answers it after (JL 261021: "你的 change 怎么跟我的 comments 一起来做交互、解决我的 comments")
    notes_at = _comments_path(path)
    notes, by = _comments(notes_at), _answered_by(path)
    # the newest report scores today's text: a record that keeps its rounds in order has the latest at the bottom
    rep = next((c for h, c in reversed(passes[0][1] if passes else []) if _is_report(h)), None)
    said = _sentence_lines(rep.get("body", "")) if rep else []
    # a sentence written after the newest report was made: its ★ is out of date (a card synced before it is not)
    head = rep.get("reviewer", "") or rep.get("body", "")[:600] if rep else ""
    seen = {"": _when(head)}                          # the review's date, then each sentence rescored later ("S3 and S8
    for ids, day in re.findall(r"((?:S\d+[a-z]*(?:,\s*|\s+and\s+)?)+) (?:were|was) rescored (\S+)", head):   # were rescored …")
        seen.update({sid: _when(day) for sid in re.findall(r"S\d+[a-z]*", ids)})
    later = lambda w, t: w and t and (w[:3] > t[:3] if t[3] < 0 else w > t)   # a date alone compares by day
    since = {sid for h, c in (passes[0][1] if passes else []) if seen[""] and not _is_report(h)
             and re.match(r"(written|applied|done)\b", c.get("state", ""))
             for sid in re.findall(r"\bS\d+[a-z]*\b", h.split(" · ")[1] if " · " in h else "")
             if later(_when(c.get("state", "")), seen.get(sid) or seen[""])}
    for x in said:
        x["stale"] = x["s"] in since
    paras = [pid for _, b in d["text"] for pid in re.findall(r"(?m)^### (C\d+\.P\d+)\b", b)]
    body = "\n".join(b for _, b in d["text"])
    sids = {pid: re.findall(r"(?m)^- B\d+[a-z]* · (S\d+[a-z]*) · ", (re.search(r"(?ms)^### " + re.escape(pid) + r"\b.*?(?=^### |\Z)", body)
                                                                 or [""])[0]) for pid in paras}
    flows = [(k, v, next((pid for pid in paras if pid.endswith("." + k)), "")) for k, v in
             re.findall(r"(?m)^Flow (P\d+): (.*)$", rep.get("body", "").partition("\nSentences:")[2])] if rep else []
    words = {m.group(1): m.group(2) for _, b in d["text"] for m in re.finditer(r"(?m)^- B\d+[a-z]* · (S\d+[a-z]*) · (.*)$", b)}
    # each sentence's evidence beside it, the rows 3 · Evidence shows there (JL 261021: "这里最好也加一下 evidence ...
    # 这一块对应的 paper 是什么 ... citation、values")
    evs = {}
    for c in ev.get("cards", []):
        for n, it in enumerate(c["items"], 1):
            for sid in _s_ids(it):
                if sid in words:
                    evs.setdefault(sid, []).append((c, it, n))
    right = list(html for _, html in sorted(
        [((_reading_key(h, d), 2), _revise_card(h, c, t, title)) for h, c in cards if not whole(h)]
        + [((_reading_key(h, d), 0), _revise_card(h, c, t, title, _first_para(whole(h).group(1), d))) for h, c in cards
           if whole(h)]
        + [((_reading_key(f"Comment · {c['target']}", d), 0), _note_card(c, by.get(c["n"], []))) for c in notes]
        + [((_reading_key(f"Review · {x['s']}", d), 1), _logic_card(x, words.get(x["s"], ""))) for x in said]
        + [((_reading_key(f"Ev · {sid}", d), 1.5), _ev_side_card(sid, items, root, words.get(sid, ""))) for sid, items in evs.items()]
        + [((_reading_key(f"Flow · {sids[pid][-1]}", d), 3), _flow_card(k, v, pid, sids[pid])) for k, v, pid in flows
           if pid and sids.get(pid)]
        + [((_reading_key(f"History · {sid}", d), 4), _history_card(sid, rows))
           for sid, rows in _sentence_history(d, path).items()],
        key=lambda x: x[0]))
    from live.draft_card_text import cite_text    # the cards' citations print as the sentences' do, never as LaTeX
    right = [cite_text(h, d) for h in right]
    some = any((c.get("state") or "proposed").split()[0].lower() == "proposed" for _, c in cs)
    waiting = sum(c["state"] == "open" for c in notes)
    # a card already written into the text, or a comment its person closed, is hidden until asked for (JL 261021:
    # "你的这个 editing card 如果已经结束的话，就把它 hide 掉吧")
    # revise + comments: a pass that answers the open comments first (JL 261021: "有的时候我让你 review，可能是加了一些我的
    # comments 之类的 revise + comments")
    ask = (f"/haipipe-draft {t} revise: answer my open comments in {_rel(notes_at, root)} first (each is my ruling), "
           "then review the rest as usual. For each comment: change the sentence it names as an Edit card with "
           "`Answers: Comment <n>`, or say why not; append `- Reply · <time from the clock>: <what you did, one or two "
           "lines>` and set `State: answered`; a comment, a co-author's change or a decided card that is a rule for the whole Section goes into the Revise "
           "rules as a new R#. Apply by default, as the Revise rules say.")
    # the pass on the left; no filter chips (JL 261113, of "Edits 5 · Evidence 23": "maybe we don't need this
    # anymore"): each row folds its own cards and its marks count them, so a kind filter only hid what ▸ already hides
    # no title over the text (JL 261113: "let's the layout explain themselves"); the head holds only the copy button
    head = ((f'<div class=rv-head><div class=rv-kinds>'
             + (f'<button type=button class="run-copy work-act" data-copy="{esc(ask)}">Copy: revise '
                f'with my {waiting} open comment{"s" if waiting > 1 else ""}</button>' if waiting else "") + '</div></div>')
            if cs or notes or said or evs else '<p class=space-empty>No Revise cards yet.</p>')
    tail = ""
    body = (f'<p class=space-reads>{_code(d["file"], root)}' + (f' · {_code(path, root)}' if path.is_file() else "")
            + (f' · {_code(notes_at, root)}' if notes_at.is_file() else "") + '</p>'
            f'<div class=rv-board data-task="{esc(t)}">{head}{top}'
            f'{_sx_board(_sx_fill(text, right, _sx_paras(d), "Cards on no sentence in this text") + tail)}</div>')
    proposed = sum((c.get("state") or "proposed").split()[0].lower() == "proposed" for _, c in cs)
    word = (f'{proposed} card{"s" if proposed != 1 else ""} wait for you' if proposed else
            f'{waiting} comment{"s" if waiting != 1 else ""} open' if waiting else "every card decided" if cs else "no cards yet")
    return (CARDS_CSS + NOTES_CSS + _fold(f"✍️ The text and its Revise cards · {d['version']}", body, open_=True, word=word)
            + CARDS_JS + NOTES_JS)


# ── a sentence's earlier wordings ─────────────────────────────────────────────────────────────────
# JL 261113: "How could we see this sentence's previous versions". Every wording the Section has had, from each older
# Draft in draft/previous/ (its §3 sentences, dated by its `date:` line) and every Revise card of every round
# (Original, then Expected), joined to today's sentence by its words, never by its S number: S numbers are renumbered
# when sentences move, so an old card's S may name another sentence now.

def _plain(s: str) -> str:
    """A sentence's words for matching: no citation command, no Markdown, one space between words, lowercase."""
    s = re.sub(r"\\cite[tp]?\{[^}]*\}|\[[^\]]*\]|[*_`]", "", s)
    return " ".join(s.split()).lower()


def _yymmdd(text: str, fallback: str = "") -> str:
    """The first date in a text as YYMMDD: `2026-10-24` or a bare `261024`."""
    m = re.search(r"\b20(\d\d)-(\d\d)-(\d\d)\b", text)
    if m:
        return "".join(m.groups())
    m = re.search(r"(?<!\d)(2[5-9][01]\d[0-3]\d)(?!\d)", text)
    return m.group(1) if m else fallback


def _wordings(d: dict, revise: Path) -> list:
    """[(date, order, label, text)] for every earlier wording on disk: older Drafts, then each card's Original and
    Expected."""
    out, n = [], 0
    draft = Path(d.get("file") or "")
    prev = draft.parent / "previous"
    for f in sorted(prev.glob("*.md")) if prev.is_dir() else []:
        body = f.read_text(encoding="utf-8", errors="replace")
        ver = (re.search(r"(?m)^(?:draft|outline)-version:\s*(\S+)", body) or re.search(r"-v(\d[\w.]*)\.md$", f.name))
        # its last change, not its `date:` line: a Draft is often edited in place after the day it was made
        when = datetime.date.fromtimestamp(f.stat().st_mtime).strftime("%y%m%d")
        label = f"draft {ver.group(1) if ver else f.stem}"
        sec = body.split("## 3 ·", 1)[1] if "## 3 ·" in body else body
        for t in re.findall(r"(?m)^- B\d+[a-z]* · S\d+[a-z]* · (.+)$", sec):
            if not t.startswith("["):
                n += 1
                out.append((when, 10 ** 6 + n, label, t.strip(), []))  # a Draft holds its day's last wording
    if revise.is_file():
        text = revise.read_text(encoding="utf-8", errors="replace")
        for part in re.split(r"(?m)^## ", text)[1:]:
            title, _, rest = part.partition("\n")
            rank = int((re.search(r"\br(\d+)\b", title) or [None, "0"])[1]) * 1000   # round r1 before r2 on one day
            for m in re.finditer(r"(?ms)^### ([^\n]+)\n(.*?)(?=^### |\Z)", rest):
                f = {k: v.strip() for k, v in re.findall(r"(?m)^(?:[-*]\s+)?(Original|Expected|State|Why|By):[^\S\n]*(.*)$", m.group(2))}
                if not f.get("Original") or not f.get("Expected"):
                    continue
                state = (f.get("State") or "proposed").split()[0].lower()
                when = _yymmdd(f.get("State", ""), _yymmdd(title))
                label = re.sub(r"\s*·\s*S\d+[a-z]*\b", "", m.group(1)).strip()
                n += 1
                out.append((when, rank + n, f"before: {label}", f["Original"], []))
                # only a wording the text really had: an accepted card not yet written in is not history (JL 261114,
                # of S13 showing a change and its undoing: "I feel the logic here is not good")
                if state in ("written", "applied", "done"):
                    n += 1
                    out.append((when, rank + n, label, f["Expected"],
                                _by({k.lower(): v for k, v in f.items()})))
    return out


def _sentence_history(d: dict, revise: Path) -> dict:
    """{S: [(date, label, text)]} oldest first, each earlier wording at the sentence of today's text it is closest to
    (at least 60% the same words, and not a fragment), consecutive repeats removed; the last line is today's."""
    now = {m.group(1): m.group(2).strip() for _, b in d.get("text", [])
           for m in re.finditer(r"(?m)^- B\d+[a-z]* · (S\d+[a-z]*) · (.*)$", b)}
    if not now:
        return {}
    keys = {s: _plain(t) for s, t in now.items()}
    got = {}
    for when, n, label, text, by in sorted(_wordings(d, revise), key=lambda r: r[:4]):
        p = _plain(text)
        best, score = None, 0.0
        for s, k in keys.items():
            a, b = p.split(), k.split()
            if not a or not b or min(len(a), len(b)) < 0.3 * max(len(a), len(b)):
                continue
            sm = difflib.SequenceMatcher(None, a, b)
            same = sum(x.size for x in sm.get_matching_blocks())
            # the same words, or the shorter wording almost whole inside the longer (a sentence split, or a clause added)
            r = max(sm.ratio(), 0.9 * same / min(len(a), len(b)) if same / min(len(a), len(b)) >= 0.85 else 0)
            if r > score:
                best, score = s, r
        if best and score >= 0.6:
            got.setdefault(best, []).append((when, label, text, by))
    out = {}
    for s, rows in got.items():
        seq = []
        for when, label, text, by in rows:
            if seq and _plain(seq[-1][2]) == _plain(text):
                continue
            seq.append((when, label, text, by))
        # the wording that is today's text is folded into "now", and its author goes with it (JL 261113: "why you
        # don't see this is from Ritu??"); a later card that only kept the text names no one new
        made, since = [], ""                       # everyone whose card wrote today's text (S3b: Ritu and JL)
        for when, label, text, by in rows:
            if _plain(text) == keys[s] and not label.startswith("before:"):
                made += [k for k in by if k not in made]
                since = max(since, when)           # the last time today's text was written (JL 261113: "who made
                                                   # this change? what is the date?"; 261114: a text written twice
                                                   # dates from the second time)
        if seq and _plain(seq[-1][2]) == keys[s]:
            seq.pop()
        if seq:
            out[s] = seq + [("now", f"current text, since {since}" if since else "current text", now[s], made)]
    return out


def _history_card(sid: str, rows: list) -> str:
    """A sentence's earlier wordings, oldest first, each set against the one before it (red out, green in); folded
    into the row's History with the decided cards."""
    lines, prev = [], None
    for when, label, text, by in rows:
        words = text if prev is None else None
        body = esc(re.sub(r"\\cite[tp]?\{([^}]*)\}", r"[\1]", words)) if words is not None else _old_new(
            re.sub(r"\\cite[tp]?\{([^}]*)\}", r"[\1]", prev), re.sub(r"\\cite[tp]?\{([^}]*)\}", r"[\1]", text))
        lines.append(f'<div class="sx-h{" now" if when == "now" else ""}"><span class=sx-hw>{esc(when)} · {esc(label)} {_by_badges(by)}</span>'
                     f'{body}</div>')
        prev = text
    n = len(rows) - 1
    # newest first, each with the change it made to the one below it (JL 261113: "could we put the most recent ones to
    # the top?"); the oldest, at the bottom, is shown whole
    lines.reverse()
    return (f'<div class="rv-card sx-histcard open" data-s="{esc(sid)}" data-state="history" data-n="{n}">'
            f'<div class=lg-head><b>🕘 Earlier wordings</b> <span class=mut>{n}, newest first</span></div>{"".join(lines)}</div>')


# the base rubric's four axes, then sentence-to-sentence flow and the anti-AI audit (JL 261021: "你这个 rubric 怎么没有
# 分数？... 句子连贯性、反 AI 写法"), then the venue's own rule
RUBRIC_AXES = ("Mechanics", "Function", "Evidence", "Readability", "Coherence", "Anti-AI", "Venue")
AXIS_NAME = {"Anti-AI": "Anti-AI writing"}
VERDICT_CHIP = {"MEETS": "st st-ok", "NEEDS WORK": "st st-warn", "NOT VERIFIABLE": "st st-warn", "N/A": "st"}


def _score_ink(n: float) -> str:
    return 'class="st st-ok"' if n >= 9 else 'class="st st-warn"' if n >= 8 else 'class=st style="color:#c92a2a"'


def _sentence_lines(body: str) -> list:
    """A review report's `Sentences:` lines (haipipe-draft-review ref/sentence-logic.md), `- S<n> · logic <n>/10 · read
    <n>/10 · link: <relation>, <carried | weak | broken> · <the problem> · Fix: none | <the rewritten sentence>`, as
    dicts; an older line, `- S<n> · <n>/10 · link: <state> · …`, has one score, read as its read score."""
    out = []
    for sid, rest in re.findall(r"(?m)^- (S\d+[a-z]*) · (.*)$", body.partition("\nSentences:")[2]):
        two = re.match(r"logic (\d+(?:\.\d+)?)/10 · read (\d+(?:\.\d+)?)/10 · (?:ai (\d+(?:\.\d+)?)/10 · )?", rest)
        one = None if two else re.match(r"(\d+(?:\.\d+)?)/10 · ", rest)
        if not (two or one):
            continue
        lo, rd = (two.group(1), two.group(2)) if two else ("", one.group(1))
        problem, _, fix = rest[(two or one).end():].partition(" · Fix: ")
        link = re.match(r"link: ([^·]+?) · ", problem)          # how it follows the sentence before it
        problem = problem[link.end():] if link else problem
        word = link.group(1).strip() if link else ""
        state = (re.search(r"\b(carried|weak|broken)\b", word) or [None, ""])[1]
        none = lambda t: "" if t.strip().lower() in ("", "none") else t.strip()
        out.append({"s": sid, "logic": lo, "read": rd, "ai": (two and two.group(3)) or "", "link": word, "state": state, "problem": none(problem),
                    "fix": none(fix), "pass": min(float(v) for v in (lo or 10, rd, (two and two.group(3)) or 10)) >= 8 and state != "broken"})
    return out


def _when(text: str):
    """The first date (and time, if any) in `text`, as a comparable tuple: 2026-11-14 00:13, else 261113; None if none.
    A date alone sorts before every time that day is known, so a card written later that day counts as later."""
    m = re.search(r"(20\d\d)-(\d\d)-(\d\d)(?:[ T](\d\d):(\d\d))?", text or "")
    if m:
        return (int(m[1]), int(m[2]), int(m[3]), int(m[4] or -1), int(m[5] or -1))
    m = re.search(r"\b(\d\d)(\d\d)(\d\d)\b", text or "")
    return (2000 + int(m[1]), int(m[2]), int(m[3]), -1, -1) if m else None


def _logic_card(x: dict, now: str = "") -> str:
    """The reviewer's logic comment on one sentence, beside it in the column of cards (JL 261021: "这个 sentence 应该当做一个
    新的 type ... logic comments ... 应该是放到右边的"): its logic and read scores, its link to the sentence before, the
    problem, and the smallest fix (marked when it is already in the text). Read only: an Edit card changes the text."""
    # in plain words (JL 261113: "How to understand these here, kind of hard to read"): one verdict that names the
    # weakest axis, the reviewer's problem as a sentence, and the suggested sentence with its change marked; the three
    # scores small at the end of the first line
    axes = [(k, float(v)) for k, v in (("logic", x["logic"]), ("read", x["read"]), ("ai", x.get("ai"))) if v]
    low = min(v for _, v in axes)
    worst = min(axes, key=lambda a: a[1])[0]
    what = {"logic": ("The logic needs work", "The logic is a little weak"),
            "read": ("Hard to read", "A little hard to read"),
            "ai": ("Reads like AI", "A little AI-like")}[worst]
    word, ink = ((what[0], "#c92a2a") if low <= 6 else (what[1], "#d9480f") if low < 8
                 else ("Reads well", "#2b8a3e"))
    if x["state"] == "broken":
        word, ink = "Does not follow from the sentence before", "#c92a2a"
    elif x["state"] == "weak" and low >= 8:
        word, ink = "Weak link to the sentence before", "#d9480f"
    names = {"logic": "logic", "read": "read", "ai": "human"}
    scores = " · ".join(f"{names[k]} {v:g}" for k, v in axes)
    # the sentence's length beside its scores, citations left out (JL 261113: "I want the wc just in the star")
    nw = len(re.findall(r"[A-Za-z0-9][\w'’.,%-]*", re.sub(r"\\cite[tp]?\{[^}]*\}", "", now or ""))) if now else 0
    scores += f" · {nw} words" if nw else ""
    applied = now and x["fix"] and " ".join(now.split()) == " ".join(x["fix"].split())
    fix = ""
    if x["fix"]:
        fix = ('<div class="lg-text lg-sugg"><span class=lg-lab>✓ Fixed: the suggestion is in the text now; the score above '
               'was for the old wording</span></div>' if applied else
               f'<div class="lg-text lg-sugg"><span class=lg-lab>Suggested</span> '
               f'{_old_new(now, x["fix"]) if now else _inline(x["fix"], {})}'
               # take the reviewer's sentence (JL 261113: "I think this is good, how could I accept it?")
               f' <button type=button class="work-act lg-use" data-adopt="{esc(x["s"])}" data-orig="{esc(now or "")}" '
               f'data-new="{esc(x["fix"])}">✓ Use this</button> <span class="lg-msg mut"></span></div>')
    # one line until clicked, so each card stays about as tall as its sentence and beside it
    return (f'<div class="rv-card rv-rev" data-s="{esc(x["s"])}" data-state="review" data-low="{low:g}" '
            f'data-scores="{esc(scores)}"{" data-fixed=1" if applied else " data-stale=1" if x.get("stale") else ""}>'
            f'<div class=lg-head><b class=lg-q>★{low:g} {esc(word)}</b>'
            f'<span class=lg-sc title="9-10 good · 8 passes · 7 weak · 6 or less needs work">{esc(scores)}</span></div>'
            + (f'<div class="lg-text lg-prob">{_inline(x["problem"][:1].upper() + x["problem"][1:], {})}.</div>'
               if x["problem"] else "")
            + fix + '</div>')


def _bib_ref(result) -> dict:
    """A discovery Run's one-entry .bib as a reference: who ("Ibrahim and Zaki"), year, title, venue, and a link (its DOI,
    else its URL, else its arXiv id)."""
    bib = next(Path(result).glob("*.bib"), None)
    text = bib.read_text(encoding="utf-8", errors="replace") if bib else ""
    get = lambda k: ((m := re.search(r"\b" + k + r"\s*=\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}", text)) and
                     re.sub(r"[{}]", "", m[1]).strip()) or ""
    raw = re.search(r"\bauthor\s*=\s*\{\s*\{([^{}]+)\}\s*\}", text)        # {{U.S. Congress}}: one name, kept whole
    names = [raw[1].strip()] if raw else [a.strip() for a in get("author").split(" and ") if a.strip()]
    last = lambda a: a.split(",")[0].strip() if "," in a else a.split()[-1]
    who = ((names[0] if raw else last(names[0])) + (" et al." if len(names) > 2 else f" and {last(names[1])}"
           if len(names) == 2 else "")) if names else ""
    doi, url, eprint = get("doi"), get("url") or get("howpublished").replace("\\url", "").strip(), get("eprint")
    link = (f"https://doi.org/{doi}" if doi else url if url.startswith("http") else
            f"https://arxiv.org/abs/{eprint}" if eprint else "")
    venue = get("journal") or get("booktitle") or ("arXiv" if eprint else get("howpublished") if not get("howpublished").startswith("\\url") else "")
    return {"who": who, "year": get("year"), "title": get("title"), "venue": venue, "link": link}


def _ev_item(c: dict, it: dict, n: int, root: Path | None) -> str:
    """One evidence item beside its sentence (JL 261021: "我需要 evidence 对应的是哪一个 paper ... 你得给个链接、给个 reference"):
    its label and state; for a citation, the paper (who, year, title, venue, linked), the sentences quoted from it and
    the words they back; for a value, the value and the file and key it is read from; and the Run that read it."""
    ink = INK.get(c["kind"], INK["value"])
    res, addr = it.get("result"), f'{c["source"]}.{it["run"]}' if it.get("run") else ""
    card = Path(res) / f"{Path(res).parent.name}.md" if res else None      # the Run's Result Card, result/<run>.md
    run = (f'<a href="/{esc(quote(_rel(card, root)))}" target=_blank>{esc(addr)}</a>' if card and root and card.is_file()
           else esc(addr))
    words = " · ".join(f"“{esc(a)}”" for a in it.get("anchor") or [])
    head = f'<b style="color:{ink}">{esc(c["label"])}.{n}</b> {EV_STATE[it["state"]]}'
    if c["kind"] == "cite" and res:
        r = _bib_ref(res)
        # a reference as a paper's reference list prints it, its Run small after it (JL 261113, of "CITE 2.1 ✅ Barnett
        # et al., 2017 · Title · venue / backs the sentence · Run …": "this layout is not that good")
        who = esc(f'{r["who"]} ({r["year"]})' if r["year"] else r["who"])
        title = (f'<a href="{esc(r["link"])}" target=_blank>{esc(r["title"])}</a>' if r["link"] else esc(r["title"]))
        ref = f'❝︎ {who}. {title}.' + (f' <i>{esc(r["venue"])}</i>.' if r["venue"] else "")
        ids = it.get("fact") or []
        ids = ids if isinstance(ids, list) else [ids]
        try:
            said = CARDS.facts(res, [str(x) for x in ids]) if ids and CARDS else ""
        except Exception:
            said = ""
        return (f'<div class="ev-item ev-ref">{ref} <span class=ev-run>{EV_STATE[it["state"]]} Run {run}</span></div>'
                + "".join(f'<div class=ev-quote>{esc(q)}</div>' for q in re.split(r"(?<=\([A-Z]\d{2}\))\s+", said) if q.strip()))
    if c["kind"] != "cite" and it.get("state") == "have":
        val = f'<b>= {esc(_num(it.get("value")))}</b>' if it.get("value") not in ("", None) else ""
        what = esc(it.get("what") or "")
        src = f'{run}' + (f' · {esc(it["file"])}' if it.get("file") else "") + (f' <code>{esc(it["key"])}</code>' if it.get("key") else "")
        return (f'<div class="ev-item ev-ref">📊 {words} {val}' + (f' <span class=mut>{what}</span>' if what else "")
                + f' <span class=ev-run>{EV_STATE[it["state"]]} {src}</span></div>')
    return (f'<div class="ev-item ev-ref">⏳ {words} <span class=mut>{esc(str(it.get("value") or it.get("need") or ""))}</span>'
            f' <span class=ev-run>{head}</span></div>')


def _ev_side_card(sid: str, items: list, root: Path | None = None, text: str = "") -> str:
    """A sentence's evidence beside it in 5 · Revise: one line naming its papers (who, year) or its values as the
    sentence says them ("1,983 requests", never an item id such as "VALUE 1.1 queries in fold00"), or what a pending
    one still needs; then, opened, each item with its reference, link, quoted sentences and the Run that read it."""
    names = []
    for c, it, n in items:
        if c["kind"] == "cite" and it.get("result"):
            r = _bib_ref(it["result"]); names.append(f'{r["who"]} {r["year"]}'.strip() or it.get("cite", ""))
        elif it.get("need"):
            names.append("pending: " + str(it["need"]).split(":")[0][:48])
        else:
            said = [a for a in it.get("anchor") or [] if a in text] or list(it.get("anchor") or [])
            what = str(it.get("what") or "").split(":")[0]
            names += said or [it.get("cite") or f'{c["label"]}.{n} {what[:40]}'.strip()]
    kinds = [c["kind"] for c, _, _ in items]          # the row's marks count each kind (JL 261113: "the citation?")
    return (f'<div class="rv-card rv-ev" data-s="{esc(sid)}" data-state="evidence" data-cite="{kinds.count("cite")}" '
            f'data-value="{kinds.count("value")}" data-display="{kinds.count("display")}">'
            f'<div class=lg-head><span class=rv-handle><span class=ev-k title="evidence for {esc(sid)}">❝︎</span></span>'
            f'<span class=rv-peek style="flex:1;min-width:0;margin:0">{esc(" · ".join(dict.fromkeys(names)))}</span></div>'
            + "".join(_ev_item(c, it, n, root) for c, it, n in items) + '</div>')


def _flow_card(k: str, text: str, pid: str, sids: list) -> str:
    """A paragraph's flow as the reviewer reads it, `S1 the shift → S2 … · weakest join S3 to S5`, a Logic card under
    the paragraph's last sentence (so it never pushes the first one down); pointing at it lights all its sentences."""
    steps, _, weak = text.partition(" · weakest join ")
    return (f'<div class="rv-card rv-rev rv-flow" data-s="{esc(" ".join(sids))}" data-p="{esc(pid)}" data-state="review">'
            f'<div class=lg-head><span class=rv-handle><b class=lg-k>Logic</b><span class=nt-s>{esc(k)} flow</span></span></div>'
            f'<div class="lg-text lg-clip2">{_inline(steps, {})}</div>'
            + (f'<div class="lg-text mut">weakest join {esc(weak)}</div>' if weak else "") + '</div>')


def _review_report(path: Path) -> str:
    """The newest pass's review report as its own section, above the text and its cards (JL 261021: "above the section
    of 'The text and its Revise cards' you should give me the section 'Revise Review Report' and tell me for each
    rubric, how you feel about this draft"; "把那些比较详细的 review report 单独作为一个新的 section"). One row per axis
    of haipipe-draft-review's rubric (Mechanics, Function, Evidence, Readability, and the venue's own rule), each with
    its verdict (MEETS · NEEDS WORK · NOT VERIFIABLE · N/A), how the draft reads, and the smallest fix; then the
    paragraphs now against what the cards propose. Nothing here is accepted: the cards are the changes."""
    passes = _revise_passes(path)[:1] if path.is_file() else []
    if not passes:
        return ""
    title, cs = passes[0]
    rep = next((c for h, c in cs if _is_report(h)), None)
    if rep is None:
        return ""
    body = rep.get("body", "")
    field = lambda k: (re.search(r"(?m)^" + k + r":[^\S\n]*(.*)$", body) or [None, ""])[1].strip()
    rows, scores = [], []
    for axis in RUBRIC_AXES:
        v = field(axis)
        if not v:
            continue
        verdict, _, rest = v.partition(" · ")
        sc = re.match(r"(\d+(?:\.\d+)?)/(10|5) · ", rest)     # `6/10 · …`: the reviewer's score (an older pass: /5)
        if sc:
            scores.append(float(sc.group(1)) * (2 if sc.group(2) == "5" else 1))
            rest = rest[sc.end():]
        reading, _, fix = rest.partition(" · Fix: ")
        chip = (f'<span class="{VERDICT_CHIP.get(verdict.strip().upper(), "st")}" style="white-space:nowrap">'
                f'{esc(verdict.strip())}</span>')
        rows.append((f"<b>{esc(AXIS_NAME.get(axis, axis))}</b>", chip,
                     f'<b>{sc.group(1)}</b><span class=mut>/{sc.group(2)}</span>' if sc else '<span class=mut>—</span>',
                     _inline(reading, {}), _inline(fix, {}) if fix else '<span class=mut>—</span>'))
    table = _change("Section question", field("Now"), field("Proposed")) if field("Now") and field("Proposed") else ""
    # each sentence in its context, as the reviewer reads it (JL 261021: "让 AI 也来评评每句话，作为一个 reviewer"; "每句话
    # 都要看一下上下文，review 它的逻辑关系是否通顺，并且给每句话打分"): haipipe-draft-review's ref/sentence-logic.md lines,
    # `- S<n> · logic <n>/10 · read <n>/10 · link: <relation>, <carried | weak | broken> · <the problem> · Fix: …`,
    # then `Flow P<k>: …`; an older line, `- S<n> · <n>/10 · link: <state> · …`, has one score
    lines = _sentence_lines(body)
    logic = [float(x["logic"]) for x in lines if x["logic"]]
    read = [float(x["read"]) for x in lines]
    fail = sum(not x["pass"] for x in lines)
    mean = lambda xs: f"{sum(xs) / len(xs):.1f}"
    # the lines themselves are Logic cards beside the text (_logic_card); the report keeps their sum
    sentences = ((f'<p style="margin:10px 0 0"><b>Each sentence, in its context:</b> '
                  + (f'logic {mean(logic)} · ' if logic else "") + f'read {mean(read)} of 10 · '
                  f'{len(lines) - fail} of {len(lines)} pass (8 or more{" on both" if logic else ""}, no broken link) '
                  '<span class=mut>· each sentence\'s Logic card is beside it below</span></p>') if lines else "")
    # the score and the table only (JL 261113: no Reviewer, Verdict or "cards below" prose)
    out = ((f'<p style="margin:0 0 6px"><b>Score {sum(scores) / len(scores):.1f} of 10</b> <span class=mut>· the mean '
              f'of {len(scores)} rows; a reading aid, never a pass mark</span></p>' if scores else "")
           + (_table(("rubric", "verdict", "score", "how the draft reads", "smallest fix"), rows) if rows else "")
           + sentences
           + (f'<h4 style="margin:14px 0 4px">The paragraphs, now and as the cards propose</h4>{table}' if table else ""))
    # folded until opened: the text and its cards come first (JL 261021: "我想说自动的话就把它 hide 起来")
    return _fold(f"📋 Revise Review Report · {title}", out, open_=False)


def _revise(f: dict, folder: Path, root: Path, st: str) -> tuple:
    d, ev = f["draft"], f["ev"]
    revise_n = len(re.findall(r"(?m)^#{2,4} ", f["revise"].read_text(encoding="utf-8", errors="replace"))) \
        if f["revise"].is_file() else 0
    paras = _paragraphs(d["structure"][1]) if d and d["structure"] else []
    section = (f"{f['section']} · {len(paras)} paragraphs · {sum(len(b) for _, b in paras)} Bullets" if paras else
               f"{f['section']} · " + " · ".join(t for t, _ in (d or {}).get("text", [])) if d else f["section"])
    notes = _comments(_comments_path(f["revise"]))
    rows = [("Section", esc(section)),
            ("Draft", esc(f"{d['version']} · {len(d['previous'])} older in previous/") if d else '<span class=mut>—</span>'),
            ("Cards", esc(f"{len(ev['cards'])} Evidence · {revise_n} Revise")),
            ("Comments", esc(" · ".join(f"{sum(c['state'] == s for c in notes)} {s}" for s in ("open", "answered", "done")))
             if notes else '<span class=mut>none</span>'),
            ("Mode", "quick: no full review; the rubric only on ask")]
    job = face(chain(folder, root).get("Job") or folder)      # the draft's desk, else its version's (desk: jamaim)
    desk = ((d or {}).get("head", {}).get("desk", "") or f["head"].get("desk", "")
            or (_header(job.read_text(encoding="utf-8", errors="ignore")).get("desk", "") if job else "")).split(":")[0].strip()
    who = (f"a reviewer for {desk}" if " " in desk else f"a reviewer for the {desk}" if desk.lower().endswith("desk")
           else f"a reviewer for the {desk} desk" if desk else
           "the reviewer this Section's venue would send")
    # think as the reviewer first (JL 261020: "think about yourself，就是你是一个什么样的 reviewer，你是怎么审这篇文章的")
    prompt = (f"/haipipe-draft {f['t']} revise: first think as {who}: who you are, what you look for, and how you "
              f"will review {f['section']} (the argument and its paragraphs first, then claims and evidence, then "
              "sentences); say it in three lines. Then read the Writing Rubric (the Draft view's 4 · Writing Rubric; "
              f"JL 261113): draft/records/{f['stem']}-requirement.md (venue V and Section W rules), "
              f"draft/records/{f['stem']}-revise-rules.md (my rulings), the paper Board's writing-patterns.md (the "
              "co-authors' patterns), and haipipe-draft-review ref/plain-rules.md and ref/ai-tells.md; every card "
              "follows them and names the rule it applies. Then read the Section, my notes and my open comments in "
              f"draft/records/{f['stem']}-comments.md; answer each comment (an Edit card with `Answers: Comment <n>`, "
              "or why not; then `- Reply · <time>: <one or two lines>` and `State: answered`). Then rewrite "
              f"draft/records/{f['stem']}-revise.md as one new pass (## Pass <k> · <date> · on draft {d['version'] if d else 'v<N>'}), "
              "the latest only: carry over the cards of the last pass still undecided and still true, drop the rest "
              "(git keeps them). The pass opens with `### Revise review report`, one line each: Reviewer (those three "
              "lines), Verdict, then Mechanics, Function, Evidence, Readability, Coherence (sentence to sentence), Anti-AI "
              "(run haipipe-draft-review's cli/anti_slop.py audit and read its ref/ai-tells.md) and Venue, each "
              "`<MEETS | NEEDS WORK | NOT VERIFIABLE | N/A> · <0-10>/10 · how the draft reads · Fix: the smallest fix` "
              "(haipipe-draft-review ref/evaluation-rubric.md, its score bands and its Revise review overlay), "
              "and Cards, how the cards' own text scores on that audit, then `Sentences:`, one line for every "
              "sentence read in its context, as haipipe-draft-review's ref/sentence-logic.md says (`- S<n> · logic "
              "<0-10>/10 · read <0-10>/10 · ai <0-10>/10 · link: <relation>, <carried | weak | broken> · <the specific problem> · Fix: "
              "none | the rewritten sentence`, then a `Flow P<k>:` line per paragraph); the loop of blind reviews ends "
              "only when every sentence scores 8 or more on all three, with no broken link, "
              "then Now and Proposed (the paragraphs as `P1 <job> (S1 to S4) · P2 …`); then Section questions on the "
              "structure, then Edit and Review cards, each with Why, Original, Expected and State: proposed, each changing the fewest words (a card keeping under 60% of its sentence needs a defect a small edit cannot fix, never style alone); where a "
              "sentence can be fixed more than one way (another order, emphasis or link), give 2 or 3 `Option A (<the "
              "approach>): <the sentence>` lines and `Chosen: A`, A applied by default. Rebuild "
              "the canvas.")
    # folded until opened: the text and its cards are what Revise is read for (JL 261020: "could you make this hidden
    # by default?")
    op = _step_box("🔁 Stage 5 · Revise", st, "<h4>Input</h4>" + _kv(rows) + _prompt_box(prompt, folder, root, "revise"),
                   open_=False, k=len(d["previous"]) if d else 0)
    canvas = [x for x in f["topics"] if (_notes(x[1]) and "canvas:" in _notes(x[1]).read_text(encoding="utf-8", errors="ignore"))]
    # the text, then its Revise cards by pass, then the canvas (JL 261020: "between these two, you should also add a
    # new one about the Revision card")
    cards = _text_and_cards(d, ev, root, f["revise"], folder) if d and d["text"] else ""
    if not cards:
        cards = _not_yet("No text yet.")
    cards = _review_report(f["revise"]) + cards
    if f["feedback"].is_file():
        cards += _fold("💬 Your marks from the canvas", _source(f["feedback"], root, ""))
    cards += "".join(_canvas_card(s, t, dr, root) for s, t, dr in canvas)
    # the rules every pass follows and the author's rulings, each with his words, kept across passes in their own file
    # (JL 261021: "可以在这里面再加一个 section，说明一下我们 revise 的规则是什么 ... 作者提出来的那些 revise 意见 ... 在这里也记录一下")
    rules = f["revise"].with_name(f"{f['stem']}-revise-rules.md")
    if rules.is_file():
        text = re.sub(r"\A#[^\n]*\n", "", rules.read_text(encoding="utf-8", errors="replace"))
        cards += _fold("📜 Revise rules · how a pass runs, and the author's rulings",
                       f'<p class=space-reads>{_code(rules, root)}</p>' + _md(text, {}))
    if d and d["previous"]:
        cards += _fold("🕘 Older versions", "<ul>" + "".join(f"<li>{_code(p, root)}</li>" for p in reversed(d["previous"]))
                       + "</ul>")
    return op, cards, ()
