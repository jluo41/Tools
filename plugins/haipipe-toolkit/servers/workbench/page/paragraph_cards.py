"""Paragraph cards (ref/cards.md §2, §3 rule 5; JL 261116: "if they are just the paragraph, could we treat them as the
sentence cards as well"): a paragraph of a page's own sections that ends in an invisible `<!-- id: p3 -->` carries
marks at its end, and its cards open under it.

The id is written once by `/haipipe-work update` (servers/workbench-work/paragraph_ids.py), never by a click, and is
kept when the words change. A paragraph's address is `<view>.<id>` (`overview.p3`); its cards live in the page's
`records/` (item_cards). A paragraph with no id carries nothing.
"""
from __future__ import annotations

import re
from pathlib import Path

from live import item_cards as IC
from live.item_marks import ASSETS, card_slot, marks

_ID = r'\s*(?:&lt;|<)!--\s*id:\s*([A-Za-z0-9_-]+)\s*--(?:&gt;|>)\s*'
PARA = re.compile(r'(<p>)((?:(?!</?p>).)*?)' + _ID + r'</p>', re.S)
ITEM = re.compile(r'(<li[^>]*>)((?:(?!</?li[ >]).)*?)' + _ID + r'</li>', re.S)


def _plain(html: str) -> str:
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', html)).strip()


def mark_paragraphs(html: str, page: Path, root: Path, view: str) -> str:
    """The section's HTML with each id'd paragraph's marks at its end and its cards under it; unchanged when none."""
    if 'id:' not in html:
        return html
    page_cards = IC.cards(page)
    rel = page.relative_to(root).as_posix() if page != root else ""

    def para(m):
        a = f"{view}.{m[3]}"
        return f'{m[1]}{m[2]}{marks(a, page_cards)}</p>{card_slot(a, page_cards, rel, words=_plain(m[2]))}'

    def item(m):
        a = f"{view}.{m[3]}"
        return f'{m[1]}{m[2]}{marks(a, page_cards)}{card_slot(a, page_cards, rel, words=_plain(m[2]))}</li>'

    out = ITEM.sub(item, PARA.sub(para, html))
    return ASSETS + out if out != html else html
