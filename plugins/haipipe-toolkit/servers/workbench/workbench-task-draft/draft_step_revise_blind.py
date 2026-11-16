"""5 · Revise of the draft Task: the blind A/B readers' verdicts a rewrite must pass before it is written (must-check
M-D07: adopt a rewrite only when its blind pair says easier AND same meaning; "meaning: no" anywhere blocks it).

A readability Run (haipipe-paper-draft § the easier-to-read check) keeps, in its `result/`: `key.json` (pair id → which
side, A or B, is the rewrite), the pairs (`pairs*.md` or `pairs/*.md`: `### <pair id>`, `A: …`, `B: …`) and the
unblinded verdicts (`unblinded*.md` lines `… | meaning: no | … | <pair id>`, or `unblinded.json`). Every rewrite a
pair judged `meaning: no` is blocked, and so is a later pair, card or suggestion whose words carry that rewrite.
draft_step_revise_notes `_adopt` (✓ Use this) and `_card_act` (accept) call `blind_refusal` before writing.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

NO = re.compile(r"(?i)\bmeaning:\s*no\b")


def _norm(s: str) -> str:
    return " ".join((s or "").replace("“", '"').replace("”", '"').replace("’", "'").split()).strip().lower()


def _results(task: Path) -> list:
    """The readability Runs' result folders this Task's rewrites are judged in: its own and its Board's review Jobs'."""
    roots = [task] + ([task.parents[1]] if len(task.parents) > 1 else [])
    out = []
    for r in roots:
        pat = "runs/*/result/key.json" if r == task else "*/*/runs/*/result/key.json"
        out += [k.parent for k in sorted(r.glob(pat)) if k.parent not in out]
    return out


def _pairs(res: Path) -> dict:
    """{pair id: {"A": text, "B": text}} from a result folder's pairs files."""
    out = {}
    for f in sorted(res.glob("pairs*.md")) + sorted((res / "pairs").glob("*.md")):
        for m in re.finditer(r"(?ms)^### (\S+)[^\n]*\n(.*?)(?=^### |\Z)", f.read_text(encoding="utf-8", errors="replace")):
            out[m.group(1)] = dict(re.findall(r"(?m)^([AB]):[^\S\n]*(.*)$", m.group(2)))
    return out


def _no_pairs(res: Path) -> set:
    """The pair ids a reader judged `meaning: no`."""
    out = set()
    for f in sorted(res.glob("unblinded*.md")):
        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            if "|" in line and NO.search(line):
                out.add(line.rsplit("|", 1)[1].strip())
    for f in sorted(res.glob("unblinded*.json")):
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        out |= {k for k, v in (data.items() if isinstance(data, dict) else ()) if isinstance(v, dict)
                and str(v.get("meaning", "")).strip().lower().startswith("no")}
    return out


def blocked(task: Path) -> list:
    """[(pair id, its result folder, the rewrite's words)] for every rewrite a blind pair judged `meaning: no`."""
    out = []
    for res in _results(task):
        try:
            key = json.loads((res / "key.json").read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        pairs = _pairs(res)
        for pid in sorted(_no_pairs(res)):
            side = "A" if str((key.get(pid) or {}).get("A", "")).lower() == "rewrite" else "B"
            words = (pairs.get(pid) or {}).get(side, "")
            if words.strip():
                out.append((pid, res, words))
    return out


def blind_refusal(revise: Path, words: str, card_body: str = "") -> str:
    """Why `words` may not be written into the Draft, or "": the card's own blind verdict says `meaning: no`, or a blind
    pair judged these words (or words they carry) `meaning: no`."""
    if card_body and any(NO.search(line) for line in card_body.splitlines()
                         if re.match(r"(?i)\s*(?:[-*]\s+)?(Readable|Blind|Meaning|Verdict|Readers?)\b", line)):
        return "not written: the blind A/B readers said this rewrite changes the meaning (meaning: no)"
    new = _norm(words)
    if not new:
        return ""
    task = Path(revise).parents[2]
    for pid, res, said in blocked(task):
        old = _norm(said)
        if old and (old == new or old.rstrip(".!?;:") in new):
            return (f"not written: the blind A/B readers said this rewrite changes the meaning (pair {pid}, "
                    f"meaning: no, in {res.parent.name}/result)")
    return ""


POINTER = re.compile(r"(?i)\s*(see|as)\b|\s*(split|keep|merge|cut|drop|none|n/?a|tbd|same)\b\W*$")


def not_a_sentence(new: str, orig: str = "") -> str:
    """Why a review line's `Fix:` is not a sentence that may replace `orig`, or "" (JL 261115: "the editing card is very
    bad": "Fix: see the card" was offered as the new sentence). A sentence ends in . ? or ! (a closing quote, bracket or
    citation after it is fine), is not a pointer ("see the card", "split", "keep", "as above"), is at least 40 percent
    of the original's length, and shares at least one word of four letters or more with it."""
    t = " ".join((new or "").split())
    if not t or POINTER.match(t):
        return "the suggestion is a note, not a sentence"
    if not re.search(r"[.?!][\"'”’)\]]*(?:\s*\\cite[tp]?\{[^}]*\}[.?!]?)?\s*$", t):
        return "the suggestion is not a whole sentence"
    o = " ".join((orig or "").split())
    if o and len(t) < 0.4 * len(o):
        return "the suggestion is much shorter than the sentence"
    words = lambda s: {w.lower() for w in re.findall(r"[A-Za-z]{4,}", s)}
    if o and len(o.split()) >= 8 and not (words(t) & words(o)):
        return "the suggestion shares no words with the sentence"
    return ""
