"""Cut a labeling step page into the parts the tests read. A step's 📋 Review Content is one numbered list of closed
sections: the step itself first (its flow, your part, its prompt), then what it made, then 🙋 Interaction."""
from __future__ import annotations

import re

SEC = "<section class=fd-sec>"
# where 📋 Review Content ends: the view's shared 🙋 Interactions fold, or the page card's end (the side pane holds
# the rest, hai-block A01)
END = re.compile(r'<details class=band-sec><summary><span class=bt>🙋 Interactions|</section><footer>')


def review(page: str) -> str:
    """The open view's 📋 Review Content, without the shared 🙋 Interactions fold under it."""
    return END.split(page.split("📋 Review Content", 1)[-1], 1)[0]


def asks(page: str) -> str:
    """The view's shared 🙋 Interactions fold, empty when nothing is asked there."""
    after = page.split("📋 Review Content", 1)[-1]
    found = re.search(r'<details class=band-sec><summary><span class=bt>🙋 Interactions', after)
    return after[found.start():].split("</section><footer>", 1)[0] if found else ""


def step(page: str) -> str:
    """Section 1 of the list: the step itself."""
    parts = review(page).split(SEC)
    return parts[1] if len(parts) > 1 else ""


def made(page: str) -> str:
    """Sections 2 onward: what the step made, then 🙋 Interaction."""
    return SEC.join(review(page).split(SEC)[2:])


def outside_sections(html: str) -> str:
    """What sits between the closed sections (nothing should: every part lives inside one)."""
    return re.sub(r"<section class=fd-sec>.*?</section>", "", html, flags=re.S)
