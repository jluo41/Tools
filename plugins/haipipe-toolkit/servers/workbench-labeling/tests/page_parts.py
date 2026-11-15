"""Cut a labeling step page into the parts the tests read. A step's 📋 Review Content is one numbered list of closed
sections: the step itself first (its flow, your part, its prompt), then what it made, then 🙋 Interaction."""
from __future__ import annotations

import re

SEC = "<section class=fd-sec>"


def review(page: str) -> str:
    """The open view's 📋 Review Content, without 🧭 Around the Work under it."""
    return page.split("📋 Review Content", 1)[-1].split("🧭 Around the Work", 1)[0]


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
