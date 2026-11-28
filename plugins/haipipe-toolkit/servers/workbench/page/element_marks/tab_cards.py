"""Tab cards (ref/cards.md §2, JL 261116): a left tab that holds content (a store, a value table, a map, a question)
carries marks after its name, and its cards open at the top of its content on the right, where there is room.

A tab's address is `<prefix>.<its name>` (`findings.maps.cohort`), the name it already has on disk made safe for an
address; its cards live in the page's own `records/` (item_cards). `ui_parts._side_tabs(..., cards=(page, root, prefix))`
calls this; a tabset without `cards` (structure: views, file lists, Skills) carries none.
"""
from __future__ import annotations

import re
from pathlib import Path

from live import item_cards as IC
from live.item_marks import ASSETS as IM_ASSETS, card_slot, marks


def slug(name: str) -> str:
    """A tab's name as an address segment: letters, digits, `_` and `-` only; "" when nothing is left."""
    return re.sub(r"[^A-Za-z0-9_-]+", "-", re.sub(r"<[^>]+>", "", name)).strip("-")[:60]


def tab_marks(page: Path, root: Path, prefix: str, names: list) -> tuple[list, list]:
    """([the marks after each tab's name], [the cards at the top of each tab's content]); "" for a tab with no name."""
    page_cards = IC.cards(page)
    rel = page.relative_to(root).as_posix() if page != root else ""
    strips, slots = [], []
    for name in names:
        s = slug(str(name))
        a = f"{prefix}.{s}" if s else ""
        strips.append(marks(a, page_cards) if a else "")
        slots.append(card_slot(a, page_cards, rel, words=str(name)) if a else "")
    if slots:
        slots[0] = ASSETS + slots[0]
    return strips, slots


ASSETS = IM_ASSETS + """<style>.pb-trow{display:flex;align-items:flex-start;gap:2px}.pb-trow>.pb-item{flex:1 1 auto;min-width:0}
.pb-trow>.im-marks{margin:7px 0 0;flex-direction:column;align-items:flex-end}</style><script>
(function(){if(window.__tcCards)return;window.__tcCards=1;
document.addEventListener('click',function(e){var o=e.target.closest&&e.target.closest('.pb-trow [data-im-open]');if(!o)return;
 var t=o.closest('.pb-trow').querySelector('[data-pbtab]');if(t&&!t.classList.contains('on'))t.click();},true);
})();</script>"""
