"""Optional generic contract for a topic page and its nested entry pages.

The Board engine never names a consumer family such as Paper, Literature, or
Value.  A board opts into this overlay by writing ``### Q-consumer register``
on an S page and placing entry pages below a ``probes/`` directory.  Each entry
then has one neutral executor and a declared dependency on its topic page.
"""
from __future__ import annotations

import re
from pathlib import Path


TOPIC_REGISTER = re.compile(r"^### Q-consumer register\s*$", re.M | re.I)
ENTRY_HEADINGS = ("q-executor", "consumer trace", "bank binding", "a-executor")
RESOLVED_STATES = {"read", "answered-local"}
QUEUED_STATES = {"planned", "commissioned", "deferred"}
ENTRY_STATES = RESOLVED_STATES | QUEUED_STATES


def page_id(path: Path) -> str:
    """Return the stable S page id encoded at the start of a filename."""
    match = re.match(r"^(S-[A-Za-z]+-\d+[a-z]?)", path.name)
    return match.group(1) if match else ""


def subsection(text: str, heading: str) -> str:
    match = re.search(
        rf"(?ms)^#### {re.escape(heading)}\s*$\n?(.*?)(?=^#### |^### |^## |\Z)",
        text,
    )
    return match.group(1) if match else ""


def check_topic_entries(board_dir: Path, pages: dict[str, Path], report) -> None:
    """Add structural findings for every board that opts into topic entries.

    ``report`` intentionally has the tiny ``add(level, code, where, message)``
    protocol rather than importing the main checker.  This keeps the contract
    reusable by future Board entry points and avoids a circular import.
    """
    topics: dict[str, tuple[Path, str]] = {}
    for path in pages.values():
        text = path.read_text(encoding="utf-8")
        if TOPIC_REGISTER.search(text):
            ident = page_id(path)
            if not ident:
                report.add("ERROR", "topic-register-not-s-page", path.name,
                           "a Q-consumer register belongs on an S page with a stable id")
                continue
            topics[ident] = (path, text)

    if not topics:
        return

    for path in pages.values():
        relative = path.relative_to(board_dir)
        if "probes" not in relative.parts:
            continue
        text = path.read_text(encoding="utf-8")
        where = relative.as_posix()
        requires = re.search(r"^requires:\s*([^\s,]+)\s*$", text, re.M)
        topic_id = requires.group(1) if requires else ""
        if topic_id not in topics:
            report.add("ERROR", "topic-entry-requires-topic", where,
                       "an entry beneath probes/ must require one direct topic page that owns a Q-consumer register")
            continue

        for heading in ENTRY_HEADINGS:
            count = len(re.findall(rf"^#### {re.escape(heading)}\s*$", text, re.M))
            if count != 1:
                report.add("ERROR", "topic-entry-heading", where,
                           f"needs exactly one `#### {heading}`; found {count}")

        binding = subsection(text, "bank binding")
        state = re.search(r"^\*\*state\*\*:\s*([a-z-]+)\s*$", binding, re.M)
        if not state:
            report.add("ERROR", "topic-entry-bank-state", where,
                       "the bank binding needs one `**state**:` line")
        elif state.group(1) not in ENTRY_STATES:
            allowed = " · ".join(sorted(ENTRY_STATES))
            report.add("ERROR", "topic-entry-bank-state", where,
                       f"state {state.group(1)!r} is not one of {allowed}")

        trace = subsection(text, "consumer trace")
        q_ids = set(re.findall(r"\bQ-[A-Za-z0-9-]+", trace))
        if not q_ids:
            report.add("WARN", "topic-entry-no-consumer", where,
                       "the consumer trace names no Q id from its topic register")
            continue
        topic_text = topics[topic_id][1]
        missing = sorted(q_id for q_id in q_ids if q_id not in topic_text)
        if missing:
            report.add("ERROR", "topic-entry-unregistered", where,
                       "consumer trace ids missing from the parent topic register: " + ", ".join(missing))
