"""Revise view, the sentence half: a paragraph's text cut into sentences and matched back to its Bullets.

Moved out of outline_revise.py (the 600-line rule); outline_revise re-exports every name here.
"""
from __future__ import annotations

import difflib
import re


_PROTECT_RE = re.compile(r"\b(?:e\.g\.|i\.e\.|et al\.|cf\.|vs\.|Dr\.|Mr\.|Ms\.|Prof\.|Fig\.|Eq\.|No\.|St\.|Jr\.|Inc\.|Ltd\.|[A-Z]\.)", re.I)
# a sentence may also open on a ⟦pending⟧ or ⟦check⟧ mark, or on a LaTeX command (JL 261020: a mark alone is its own
# sentence, and must stay its own point when the paragraph is saved as prose)
_END_RE = re.compile(r"[.!?]['\"”’)\]⟧]*\s+(?=[\"“'(\[A-Z0-9⟦\\])|[。！？]['\"”’)\]]*\s*")


def split_sentences(text: str) -> list[str]:
    """One sentence per line for the box (JL: "each sentence separated with a new line").

    Abbreviations, initials, decimals and citation braces are protected so a
    split lands only after a real sentence end. A wrong split is harmless: on
    Save the lines of one point are joined back with spaces.
    """
    text = " ".join(text.split())
    if not text:
        return []
    guarded = re.sub(r"(?<=\d)\.(?=\d)", "\u0000", text)
    guarded = _PROTECT_RE.sub(lambda m: m.group(0).replace(".", "\u0000"), guarded)
    guarded = re.sub(r"\{[^}]*\}", lambda m: m.group(0).replace(".", "\u0000").replace(" ", "\u0001"), guarded)
    parts, start = [], 0
    for match in _END_RE.finditer(guarded):
        parts.append(guarded[start:match.end()])
        start = match.end()
    parts.append(guarded[start:])
    cleaned = [p.replace("\u0000", ".").replace("\u0001", " ").strip() for p in parts]
    return [p for p in cleaned if p]


def box_text(texts: list[str]) -> str:
    """The box: each sentence a row (JL 261020: "we want to make it each sentence a row"), with no blank lines; a Save
    matches the rows back to the points by likeness (`_text_to_bullets`), so the editing stays free ("more easier and
    free style")."""
    return "\n".join(s for t in texts if t and t.strip() for s in split_sentences(t))


_SID_RE = re.compile(r"^(S\d+[a-z]*(?:\s*(?:-|–|to)\s*S\d+[a-z]*)?)\s*·")


def sentence_id(head: str) -> str:
    """A Bullet's sentence id, `S2` or `S2a`, from its head (`S2 · [Role] point`); empty on a plan without them."""
    match = _SID_RE.match(head or "")
    return match.group(1) if match else ""


def screen_rows(bullets: list[dict]) -> list[dict]:
    """The rows the editor shows: each sentence of each Bullet a row, `b` its Bullet, `s` its sentence id on the
    Bullet's first row (JL 261020: "could we make each sentences to be auto generate the sentence id as well?").
    `bullets` carry address, bullet_id, sid and text."""
    rows = []
    for bullet in bullets:
        for k, sentence in enumerate(split_sentences(bullet.get("text") or "")):
            rows.append({"b": bullet["address"], "text": sentence,
                         "s": (bullet.get("sid") or bullet.get("bullet_id") or "") if k == 0 else ""})
    return rows



def _words(text: str) -> list[str]:
    """A sentence's words for matching: lower case, the punctuation at either end of each word taken off."""
    return [w for w in (x.strip(".,;:!?()[]\"'“”‘’") for x in text.lower().split()) if w]


def _text_to_bullets(text: str, addresses: list[str], before: list[str]) -> dict[str, str]:
    """The paragraph as typed → its Bullets, by likeness: the text is cut into sentences, and each Bullet takes the
    run of sentences, in order, that reads most like the sentence it held before (word overlap). Every sentence
    lands somewhere and the order never changes: a sentence typed in between joins the neighbour it fits best, a
    deleted one leaves its Bullet empty, and with nothing to match (a first draft) Bullet k takes sentence k and the
    last takes the rest. A row ends a sentence (a line typed without its full stop stays its own sentence); blank
    lines carry no meaning."""
    sents = [s for line in text.splitlines() for s in split_sentences(line)]     # a row ends a sentence too
    n, m = len(addresses), len(sents)
    if not m:
        return {a: "" for a in addresses}
    old = [_words(b) for b in before] + [[]] * (n - len(before))

    def score(i: int, k: int, j: int) -> int:
        if k == j:
            return 0
        got = _words(" ".join(sents[k:j]))
        like = difflib.SequenceMatcher(None, old[i], got).ratio() if old[i] and got else 0.0
        # a filled Bullet gains a little, an earlier one a little more (with nothing to match, fill from B1);
        # a long run costs a little
        return round(like * 1000) + 20 + (n - i) - (j - k - 1)

    worst = -10 ** 9
    best = [[worst] * (m + 1) for _ in range(n + 1)]
    cut = [[0] * (m + 1) for _ in range(n + 1)]
    best[0][0] = 0
    for i in range(1, n + 1):
        for j in range(m + 1):
            for k in range(j + 1):
                if best[i - 1][k] == worst:
                    continue
                total = best[i - 1][k] + score(i - 1, k, j)
                if total > best[i][j]:
                    best[i][j], cut[i][j] = total, k
    mapped, j = {}, m
    for i in range(n, 0, -1):
        k = cut[i][j]
        mapped[addresses[i - 1]] = " ".join(sents[k:j])
        j = k
    return mapped


def _like(a: str, b: str) -> float:
    wa, wb = _words(a), _words(b)
    return difflib.SequenceMatcher(None, wa, wb).ratio() if wa and wb else 0.0


def _rows_to_bullets(rows: list[dict], addresses: list[str], before: list[str]) -> tuple[dict, list]:
    """The rows as typed, each naming the Bullet it was drawn from (`b`, empty on a new row) → (the paragraph's
    Bullets: their new text, [(the Bullet a run of new sentences follows, or None for the paragraph's start,
    [sentence, ...])]).

    A row keeps its Bullet, so typing inside a row edits that sentence; a row the person made (Enter, paste) is a new
    sentence (JL 261020: "auto generate the sentence id"). Inside a row, the sentences that read like the Bullet's own
    keep it and a sentence typed before or after them is new. A new sentence word for word a sentence of a Bullet no
    row names is that Bullet (two rows joined, a row retyped); an empty planned point takes the next new sentence
    before any new Bullet is made. Bullets never change order: a row naming one out of order is new."""
    index = {a: i for i, a in enumerate(addresses)}
    named = {str(r.get("b") or "") for r in rows} & set(addresses)
    olds = [split_sentences(b) for b in before]
    groups: list[list] = []          # [address or None, [sentences]] in the order typed
    last = -1

    def put(address, sentence):
        if address is not None and groups and groups[-1][0] == address:
            groups[-1][1].append(sentence)
        else:
            groups.append([address, [sentence]])

    def loose(sentence, upto):
        nonlocal last
        start = last if last >= 0 and groups and groups[-1][0] == addresses[last] else last + 1
        for k in range(start, upto):
            if addresses[k] not in named and any(" ".join(_words(o)) == " ".join(_words(sentence)) for o in olds[k]):
                put(addresses[k], sentence)
                last = k
                return
        put(None, sentence)

    for row in rows:
        sents = split_sentences(" ".join(str(row.get("text") or "").split()))
        if not sents:
            continue
        i = index.get(str(row.get("b") or ""), -1)
        if i >= 0 and (i < last or (i == last and not (groups and groups[-1][0] == addresses[i]))):
            i = -1
        if i < 0:
            for sentence in sents:
                loose(sentence, len(addresses))
            continue
        keep = [k for k, s in enumerate(sents) if any(_like(s, o) >= 0.5 for o in olds[i])]
        first, end = (keep[0], keep[-1] + 1) if len(sents) > 1 and keep else (0, len(sents))
        for sentence in sents[:first]:
            loose(sentence, i)
        for sentence in sents[first:end]:
            put(addresses[i], sentence)
        last = i
        for sentence in sents[end:]:
            loose(sentence, len(addresses))

    mapped = {a: "" for a in addresses}
    inserts, waiting, placed = [], [], -1

    def flush(upto):
        free = [k for k in range(placed + 1, upto) if not before[k].strip()]
        for k, sentence in zip(free, waiting):
            mapped[addresses[k]] = sentence
        rest = waiting[len(free):]
        if rest:
            after = free[-1] if free else placed
            inserts.append((addresses[after] if after >= 0 else None, list(rest)))
        waiting.clear()

    for address, sents in groups:
        if address is None:
            waiting.extend(sents)
            continue
        flush(index[address])
        mapped[address] = " ".join(sents)
        placed = index[address]
    flush(len(addresses))
    return mapped, inserts

