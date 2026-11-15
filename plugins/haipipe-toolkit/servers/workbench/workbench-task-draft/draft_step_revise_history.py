"""5 · Revise of the draft Task: a sentence's earlier wordings (the 🕘 Earlier wordings card), moved out of
draft_step_revise.py (700-line rule), which re-exports every name. Sentences are keyed as draft_step_revise_keys.Keys
keys them (M-D05: the full address when the Draft repeats a bare id)."""
from __future__ import annotations

import datetime
import difflib
import re
from pathlib import Path

from live.frame import esc
from live.draft_step_revise_cards import _by, _by_badges, _old_new
from live.draft_step_revise_keys import Keys


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
        # who made this version, as its header says it (JL 261114: "each entry should say WHO made the change"): a person,
        # or a session with the person who signed, `by: AITC-LOI-t01 session, signed JL`
        who = (re.search(r"(?m)^by:[^\S\n]*(\S.*?)\s*$", body.split("\n## ", 1)[0]) or [None, ""])[1]
        label = f"draft {ver.group(1) if ver else f.stem}" + (f" · {who}" if who else "")
        sec = body.split("## 3 ·", 1)[1] if "## 3 ·" in body else body
        for t in re.findall(r"(?m)^- B\d+[a-z]* · [Ss]\d+[a-z]* · (.+)$", sec):
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
                label = re.sub(r"\s*·\s*[Ss]\d+[a-z]*\b", "", m.group(1)).strip()
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
    now = Keys(d).words()
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
        rows = _merged(rows)
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


def _merged(rows: list) -> list:
    """Two or more wordings of one source (the same label and day, e.g. two sentences of "draft v4.0") that land on one
    sentence of today's text were merged into it: one row, their words joined in their old order, before the diff."""
    out, at = [], {}
    for when, label, text, by in rows:
        k = (when, label)
        if k in at:
            i = at[k]
            w, l, t, b = out[i]
            out[i] = (w, l, f"{t} {text}", b + [x for x in by if x not in b])
        else:
            at[k] = len(out)
            out.append((when, label, text, list(by)))
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
