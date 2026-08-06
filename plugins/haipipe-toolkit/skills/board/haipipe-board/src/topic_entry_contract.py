"""Optional generic contract for an evidence page and its nested QA-probes.

The Board engine never names a consumer family such as Paper, Literature, or
Value.  A board opts into this overlay by writing ``route: outward`` or
``route: inward`` in an S page's metadata head and placing QA-probe records
below a ``probes/`` directory.  The evidence page organizes its Content BY
EXECUTOR (JL, 260806): one ``### E<n> · <question>`` division per Q-executor
conversation, each pointing at exactly one QA-probe, plus the standing
``### E0 · incoming`` queue.  Since JL's ruling B (260806) a QA-probe is a
hidden SOURCE RECORD named ``<n>-<slug>.md``, the consumer's copy that points
at the QA-bank it is answered by: the digit-first name keeps it out of
``page_files``'s prefix sweep, so this module finds records with its own
``probes/`` glob rather than through the page registry.
"""
from __future__ import annotations

import re
from pathlib import Path


# The head key that makes an S page an evidence page (the type key, JL 260806:
# it moved from the retired `### Q-consumer register` marker to the page head).
HEAD_ROUTE = re.compile(r"^route:\s*(outward|inward)\s*$", re.M)
# One Content division per Q-executor conversation; E0 is the incoming queue.
E_DIVISION = re.compile(r"^### E(\d+)\s*·\s*(.*)$", re.M)
# The slot words are the four capitals (JL 260806): Q-consumer / A-consumer /
# Q-executor / A-executor. `consumer trace` and `bank binding` are not among
# the four words and stay lowercase.
ENTRY_HEADINGS = ("Q-executor", "consumer trace", "bank binding", "A-executor")
RESOLVED_STATES = {"read", "answered-local"}
QUEUED_STATES = {"planned", "commissioned", "deferred"}
ENTRY_STATES = RESOLVED_STATES | QUEUED_STATES


def page_id(path: Path) -> str:
    """Return the stable S page id encoded at the start of a filename."""
    match = re.match(r"^(S-[A-Za-z]+-\d+[a-z]?)", path.name)
    return match.group(1) if match else ""


def head(text: str) -> str:
    """The metadata head: everything before the first ``## `` section."""
    match = re.search(r"(?m)^## ", text)
    return text[: match.start()] if match else text


def subsection(text: str, heading: str) -> str:
    match = re.search(
        rf"(?msi)^#### {re.escape(heading)}\s*$\n?(.*?)(?=^#### |^### |^## |\Z)",
        text,
    )
    return match.group(1) if match else ""


def e_divisions(text: str) -> list[tuple[int, str, str]]:
    """-> [(n, question, body)] for every ``### E<n> ·`` Content division."""
    out = []
    matches = list(E_DIVISION.finditer(text))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[m.end():end]
        stop = re.search(r"(?m)^#{1,3} ", body)
        if stop:
            body = body[: stop.start()]
        out.append((int(m.group(1)), m.group(2).strip(), body))
    return out


def check_topic_entries(board_dir: Path, pages: dict[str, Path], report) -> None:
    """Add structural findings for every board that opts into evidence pages.

    ``report`` intentionally has the tiny ``add(level, code, where, message)``
    protocol rather than importing the main checker.  This keeps the contract
    reusable by future Board entry points and avoids a circular import.
    """
    topics: dict[str, tuple[Path, str]] = {}
    for path in pages.values():
        text = path.read_text(encoding="utf-8")
        if HEAD_ROUTE.search(head(text)):
            ident = page_id(path)
            if not ident:
                report.add("ERROR", "topic-route-not-s-page", path.name,
                           "a route: head key belongs on an S page with a stable id")
                continue
            topics[ident] = (path, text)

    if not topics:
        return

    entries: dict[Path, None] = {}
    for path in pages.values():
        if "probes" in path.relative_to(board_dir).parts:
            entries[path] = None
    for path in sorted(board_dir.rglob("probes/*/*.md")):
        parts = path.relative_to(board_dir).parts
        if any(s.startswith(("_", ".")) for s in parts[:-1]):
            continue
        entries[path] = None

    for path in entries:
        relative = path.relative_to(board_dir)
        text = path.read_text(encoding="utf-8")
        where = relative.as_posix()
        requires = re.search(r"^requires:\s*([^\s,]+)\s*$", text, re.M)
        topic_id = requires.group(1) if requires else ""
        if topic_id not in topics:
            report.add("ERROR", "topic-entry-requires-topic", where,
                       "a QA-probe beneath probes/ must require one direct evidence page carrying a route: head key")
            continue

        for heading in ENTRY_HEADINGS:
            hits = re.findall(rf"(?i)^#### ({re.escape(heading)})\s*$", text, re.M)
            if len(hits) != 1:
                report.add("ERROR", "topic-entry-heading", where,
                           f"needs exactly one `#### {heading}`; found {len(hits)}")
            elif hits[0] != heading:
                report.add("WARN", "topic-entry-heading-case", where,
                           f"`#### {hits[0]}` should wear the canonical casing `#### {heading}`")

        binding = subsection(text, "bank binding")
        state = re.search(r"^\*\*state\*\*:\s*([a-z-]+)\s*$", binding, re.M)
        if not state:
            report.add("ERROR", "topic-entry-bank-state", where,
                       "the bank binding needs one `**state**:` line")
        elif state.group(1) not in ENTRY_STATES:
            allowed = " · ".join(sorted(ENTRY_STATES))
            report.add("ERROR", "topic-entry-bank-state", where,
                       f"state {state.group(1)!r} is not one of {allowed}")

        # One E<n> division ↔ one QA-probe (JL 260806): the owning evidence
        # page must point at this record from exactly one executor division.
        # E0 never points at a record; it queues Q-consumers not yet translated.
        topic_path, topic_text = topics[topic_id]
        rel_from_topic = ""
        try:
            rel_from_topic = path.relative_to(topic_path.parent).as_posix()
        except ValueError:
            pass
        owners = [n for n, _q, body in e_divisions(topic_text)
                  if n > 0 and rel_from_topic and rel_from_topic in body]
        if len(owners) != 1:
            report.add("ERROR", "topic-probe-division", where,
                       f"a QA-probe belongs to exactly one `### E<n>` division of "
                       f"{topic_id}; {len(owners)} division(s) point at it")

        trace = subsection(text, "consumer trace")
        q_ids = set(re.findall(r"\bQ-[A-Za-z0-9-]+", trace))
        if not q_ids:
            report.add("WARN", "topic-entry-no-consumer", where,
                       "the consumer trace names no Q id from its evidence page")
            continue
        missing = sorted(q_id for q_id in q_ids if q_id not in topic_text)
        if missing:
            report.add("ERROR", "topic-entry-unregistered", where,
                       "consumer trace ids missing from the parent evidence page: " + ", ".join(missing))
