"""Accept on a Research Question's edit card writes the question's new words into the Story topic's own face
(workbench/ref/cards.md §7: the words belong to the owner, so the adapter is the paper's). The shared route accepts the
card, calls this, and puts the card back when it refuses. It replaces the question of row <key> (`RQ.<key>`) only while
that question still reads exactly as the card's `Original:`; a changed row, a cut, or a row it cannot find refuses.
Two forms of §3: one keyed table (a first cell H1, "H2 check", RQ1, "1 · …", its question in the column named
"question"), or the numbered list under **The paper's question** (RQn is item n)."""
from __future__ import annotations

import re
from pathlib import Path

from live import item_cards as IC
from live.board_read import rq_key
from live.item_card_route import register_accept

_SECTION = re.compile(r"(?ms)^(#{2,4})[^\n]*Research Questions[^\n]*\n(.*?)(?=^\1 |\Z)")


def _card(page: Path, head: str) -> dict | None:
    return next((e for e in IC.parse_edits(IC.files(page)["revise"]) if e["head"] == head), None)


def _in_table(body: str, key: str, old: str, new: str) -> str | None:
    """The section with row <key>'s question cell changed, or None when no keyed row holds `old`."""
    lines = body.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if not line.lstrip().startswith("|") or i + 1 >= len(lines) or not re.match(r"\s*\|[\s:|-]+\|?\s*$", lines[i + 1]):
            continue
        head = [c.strip().lower() for c in line.strip().strip("|").split("|")]
        q = next((j for j, h in enumerate(head) if j and "question" in h), None)
        if q is None:
            continue
        for k in range(i + 2, len(lines)):
            row = lines[k]
            if not row.lstrip().startswith("|"):
                break
            cells = row.rstrip("\n").strip().strip("|").split("|")
            if cells and rq_key(cells[0].strip()) == key and q < len(cells):
                if cells[q].strip() != old:
                    return None
                cells[q] = f" {new} "
                lines[k] = row[:len(row) - len(row.lstrip())] + "|" + "|".join(cells) + "|" + ("\n" if row.endswith("\n") else "")
                return "".join(lines)
    return None


def _in_list(body: str, key: str, old: str, new: str) -> str | None:
    """The numbered list form: item n of RQn, its question (up to its question mark) replaced."""
    m = re.fullmatch(r"RQ(\d+)", key)
    if not m:
        return None
    item = re.search(rf"(?m)^(\s*{m[1]}\.\s+)(.*)$", body)
    if not item or not item[2].startswith(old):
        return None
    return body[:item.start(2)] + new + item[2][len(old):] + body[item.end(2):]


def accept_rq(page: Path, address: str, card_head: str, root: Path) -> str | None:
    key = address.split(".", 1)[1] if "." in address else ""
    card = _card(page, card_head)
    if not card or not key:
        return "the card is not on this page; reload"
    old, new = card["original"].strip(), card["expected"].strip()
    if not old or not new or new == "(cut)":
        return "this card has no new words for the question"
    face = IC.page_face(page)
    if face is None:
        return "the Story has no face to write"
    with IC.locked(face):
        text = face.read_text(encoding="utf-8")
        sec = _SECTION.search(text)
        if not sec:
            return "the Story has no Research Questions section"
        body = sec.group(2)
        done = _in_table(body, key, old, new) or _in_list(body, key, old, new)
        if done is None:
            return f"{address} no longer reads as the card's Original; reload"
        IC.write_text(face, text[:sec.start(2)] + done + text[sec.end(2):])
    return None


register_accept("RQ", accept_rq)
