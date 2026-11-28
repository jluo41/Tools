"""Ladder rows as cards (ref/cards.md §2, §3): a Job, Task or Run row in Plan + Results carries marks after its state
mark, the way a Draft Lab sentence does, and a click on a mark opens its cards under the row.

  🙋 N   the questions waiting for the person at that row or below (its collection Runs); the card is the question
         form itself, answered in place (hai-interaction's built form, the 🙋 Interaction section's frame)
  ℹ️ N   things the person should know there (`collect.py know`)
  💬 📝 ✓ the row's own comments, edit cards and the person's check (item_marks)

A row's address is its place on the ladder from its Block, `j02`, `j02.t01`, `j02.t01.r05` (the number prefix only,
never the slug), so the same row shows the same thread on the Block, Job and Task pages. Its cards live in the Block's
`records/` (item_cards), the page where the ladder is kept.
"""
from __future__ import annotations

import re
from pathlib import Path

from live import item_cards as IC
from live.frame import esc
from live.item_marks import ASSETS as IM_ASSETS, card_slot, marks

PREFIX = re.compile(r"^([a-z]\d\d)_")


def block_of(folder: Path) -> Path | None:
    """The Block holding a Job, Task or Run: the nearest folder with a board.md."""
    for p in (folder, *folder.parents):
        if (p / "board.md").is_file():
            return p
    return None


def short(folder: Path) -> str:
    """A ladder folder's segment: `j02` for j02_census, `r05` for r05_first; a soft Run keeps its whole name."""
    m = PREFIX.match(folder.name)
    if m:
        return m[1]
    return folder.name if IC.ADDRESS.match(folder.name) else ""


def address(folder: Path, block: Path) -> str:
    """`j02.t01.r05` from the Block down, skipping the runs/ folder; "" when the folder is not under the Block."""
    try:
        parts = folder.relative_to(block).parts
    except ValueError:
        return ""
    segs = [short(Path(p)) for p in parts if p != "runs"]
    return ".".join(segs) if segs and all(segs) else ""


def _ask_slot(a: str, rows: list, root: Path) -> str:
    """The 🙋 card: the waiting forms at this row, one frame each, loaded when the card first opens."""
    from live.interaction_section import interaction_section
    body = interaction_section(rows, root, body_only=True)
    body = body.replace('class=pb-ixframe title=', 'class=pb-ixframe loading=lazy title=').replace('" src="', '" data-src="')
    return f'<div class="im-slot lc-ask" data-im-slot="{esc(a)}~ask" hidden><div class=im-slot-in>{body}</div></div>'


def row_cards(folder: Path, root: Path, words: str = "") -> tuple[str, str]:
    """(the marks after the row, the cards under it) for one Job, Task or Run folder; ("", "") off the ladder."""
    block = block_of(folder.parent)
    a = address(folder, block) if block else ""
    if not a:
        return "", ""
    from live.focus_interactions import interaction_items
    rows = interaction_items(folder, root)          # a Job or Task: its forms and below; a collection Run: its own
    waiting = [r for r in rows if r["state"] == "waiting"]
    know = [r for r in rows if r["state"] == "to know"]
    page_cards = IC.cards(block)
    ask = ((f'<button type="button" class="im-mk im-w" data-im-open="{esc(a)}~ask">🙋 {len(waiting)}</button>'
            if waiting else "")
           + (f'<button type="button" class="im-mk" data-im-open="{esc(a)}~ask">ℹ️ {len(know)}</button>' if know else ""))
    strip = f'<span class=lc-marks>{ask}{marks(a, page_cards)}</span>'
    slot = card_slot(a, page_cards, block.relative_to(root).as_posix(), words=words)
    return strip, slot + (_ask_slot(a, waiting + know, root) if waiting or know else "")


ASSETS = IM_ASSETS + """<style>.lc-marks{display:inline-flex;align-items:center}.lc-marks .im-marks{margin-left:2px}
.lc-ask .pb-ixframe{height:auto;min-height:220px}</style><script>
(function(){if(window.__lcCards)return;window.__lcCards=1;
document.addEventListener('click',function(e){var o=e.target.closest&&e.target.closest('[data-im-open$="~ask"]');if(!o)return;
 setTimeout(function(){var s=document.querySelector('[data-im-slot="'+CSS.escape(o.dataset.imOpen)+'"]');
  if(!s||s.hidden)return;var q=s.querySelector('.pb-ixset [data-ixq]');if(q&&!s.dataset.lcOn){s.dataset.lcOn=1;q.click();}},0);});
})();</script>"""
