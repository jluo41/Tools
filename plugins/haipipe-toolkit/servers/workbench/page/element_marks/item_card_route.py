"""POST /_board/item-card {page, address, act, n, card, was, text, words}: the one writer of item cards (ref/cards.md
§6). It answers with the item's new mark strip and card slot, so the page replaces them in place.

A draft Task's sentence, paragraph and Section comments and its sentence checks go to Draft Lab's own writer
(draft_step_revise_notes.note_act), the same one /_board/draft-comment calls, so Draft Lab reads and writes exactly as
before. Its edit cards keep /_board/draft-card (card_act: the pass title, the sentence rewrite). Every other page
writes through item_cards.
"""
from __future__ import annotations

from pathlib import Path

from live import item_cards as IC
from live.item_marks import card_slot, marks

COMMENT_ACTS = ("add", "reply", "done", "reopen", "delete")
CHECK_ACTS = ("check", "uncheck")
EDIT_ACTS = ("accept", "reject", "undo")

# Accept writes the item's words through the adapter of the workbench that owns the item (ref/cards.md §7): keyed by
# the address's first segment ("RQ" for a Research Question row). fn(page, address, card_head, root) -> None when the
# words were written, or the reason it refused (the item's words differ from the card's Original:). No adapter: only
# the card's State changes.
ACCEPT_ADAPTERS: dict = {}


def register_accept(prefix: str, fn) -> None:
    ACCEPT_ADAPTERS[prefix] = fn


def _draft(page: Path, root: Path, p: dict) -> tuple:
    from live.draft_step_revise_notes import NOTE_TARGET, note_act
    address = str(p.get("address") or "")
    if not NOTE_TARGET.match(address):
        return None
    if str(p.get("act")) not in COMMENT_ACTS + CHECK_ACTS:
        return 400, {"ok": False, "err": "a draft's edit cards are answered on its Revise step"}
    q = {"task": page.relative_to(root).as_posix(), "s": address, "act": p.get("act"), "n": p.get("n"),
         "was": p.get("was"), "text": p.get("text"), "quote": p.get("quote")}
    return note_act(root, q)


def item_card_act(root, p: dict, read_only: bool = False) -> tuple:
    if read_only:
        return 403, {"ok": False, "err": "this host is read-only"}
    root = Path(root).resolve()
    rel = str(p.get("page") or "").strip("/")
    page = (root / rel).resolve()
    if not (page.is_dir() and (page == root or root in page.parents)):
        return 400, {"ok": False, "err": "no such page"}
    address, act = str(p.get("address") or ""), str(p.get("act") or "")
    if not IC.ADDRESS.match(address):
        return 400, {"ok": False, "err": "no such item address"}
    address = IC.card_key(page, address)             # a draft's S8 and s8 are one sentence
    if (page / "draft").is_dir():
        res = _draft(page, root, p)
        if res is not None:
            return res
    if act in COMMENT_ACTS:
        code, res = IC.comment_act(page, p)
    elif act in CHECK_ACTS:
        code, res = IC.check_act(page, p)
    elif act in EDIT_ACTS:
        code, res = IC.edit_card_act(page, p)
        adapter = ACCEPT_ADAPTERS.get(address.split(".", 1)[0]) if act == "accept" and code == 200 else None
        if adapter is not None:                     # the card is accepted first; a refused write puts it back
            refused = adapter(page, address, str(p.get("card") or ""), root)
            if refused:
                IC.edit_card_act(page, {**p, "act": "undo", "was": "accepted"})
                return 409, {"ok": False, "err": refused}
    else:
        return 400, {"ok": False, "err": "no such act"}
    if code == 200:
        now = IC.cards(page)
        res["marks"] = marks(address, now)
        try:                                        # a table row's slot stays a full-width <tr> after a save
            cols = max(0, min(int(p.get("cols") or 0), 50))
        except (TypeError, ValueError):
            cols = 0
        res["slot"] = card_slot(address, now, rel, cols=cols, words=str(p.get("words") or ""))
    return code, res
