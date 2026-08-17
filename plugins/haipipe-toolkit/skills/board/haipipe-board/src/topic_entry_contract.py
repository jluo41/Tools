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
DISPLAY_STATES = {"candidate", "selected", "paper-bound", "parked", "not-displayable"}
DISPLAY_POINTER = re.compile(
    r"🖼 Display:\s*`?([^`\s·]+)`?\s*·\s*state:\s*([a-z-]+)"
)


# The paper's drawer of bound records. `QA-probe` is the name ruled on 260806 so
# the twin law reads off the filesystem rather than only out of this contract;
# `probes` is the pre-rename name and stays readable while each paper migrates.
# Both are globbed; new work writes the first.
EVIDENCE_DIRS = ("QA-probe", "probes")


def page_id(path: Path) -> str:
    """The stable id a QA-probe may bind to.

    The S form (`S-Value-1`) is the one a probe writes in its `requires:` line,
    so it stays first. Any other page falls back to its own stem, which is what
    the drawer is named after under the 260806 rule: a page's companion folder
    is `<type-plural>/<page name>/`, exactly. Requiring an S prefix here was a
    consequence of pairing through a hand-typed id; pairing through the folder
    name needs no prefix, and refusing an evidence page for its filename alone
    would have blocked every board that is not a paper.
    """
    match = re.match(r"^(S-[A-Za-z]+-\d+[a-z]?)", path.name)
    return match.group(1) if match else path.stem


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


LEAN_SECTIONS = ("Question", "Answer")
LEAN_ROUTES = {"task", "discovery", "local"}


def head_key(text: str, name: str) -> str:
    """A head key in either style: `route: task` or `- route: task`."""
    m = re.search(rf"^-?\s*{name}:\s*(\S.*?)\s*$", head(text), re.M)
    return m.group(1) if m else ""


def check_four_slot_record(text: str, where: str, report) -> None:
    """The pre-260806 record: four `#### ` slots, state inside the binding."""
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


def check_lean_record(text: str, where: str, report) -> None:
    """The 260806 record: head keys, and the three sections a QA-bank wears.

    A record and the bank it answers to are deliberately the same shape, so a
    reader who has read one can read the other. What a record adds is `route:`,
    and on any route but `local` the `bank:` path that says where the original
    lives. It is never a copy of that original: the Answer here is a digest,
    and only the Caveats travel whole, because a digest of a LIMIT is how a
    paper ends up claiming more than its design supports.
    """
    for section in LEAN_SECTIONS:
        if not re.search(rf"(?m)^## {section}\s*$", text):
            report.add("ERROR", "topic-record-section", where,
                       f"a QA record needs one `## {section}` section")

    state = head_key(text, "state").split("·")[0].strip().lower()
    if not state:
        report.add("ERROR", "topic-record-state", where,
                   "a QA record needs one `state:` head key")
    elif state not in ENTRY_STATES:
        allowed = " · ".join(sorted(ENTRY_STATES))
        report.add("ERROR", "topic-record-state", where,
                   f"state {state!r} is not one of {allowed}")

    route = head_key(text, "route").lower()
    bank = head_key(text, "bank")
    if route not in LEAN_ROUTES:
        allowed = " · ".join(sorted(LEAN_ROUTES))
        report.add("ERROR", "topic-record-route", where,
                   f"a QA record needs one `route:` head key from {allowed}"
                   + (f"; found {route!r}" if route else ""))
    elif route == "local" and bank:
        report.add("ERROR", "topic-record-route", where,
                   "route is `local`, meaning the answer was produced here, "
                   "so there is no bank to name")
    elif route != "local" and not bank:
        report.add("ERROR", "topic-record-route", where,
                   f"route `{route}` means the answer lives in an executor "
                   "tree, so the record must name it with a `bank:` key")


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
            topics[page_id(path)] = (path, text)

    if not topics:
        return

    entries: dict[Path, None] = {}
    for path in pages.values():
        if set(EVIDENCE_DIRS) & set(path.relative_to(board_dir).parts):
            entries[path] = None
    found = [p for d in EVIDENCE_DIRS for p in board_dir.rglob(f"{d}/*/*.md")]
    for path in sorted(found):
        parts = path.relative_to(board_dir).parts
        if any(s.startswith(("_", ".")) for s in parts[:-1]):
            continue
        entries[path] = None

    for path in entries:
        relative = path.relative_to(board_dir)
        text = path.read_text(encoding="utf-8")
        where = relative.as_posix()
        # Two ways a record names the evidence page it answers to, and both are
        # live. The DECLARED way is a `requires:` line naming the page id, which
        # every pre-260806 probe uses. The IMPLIED way is the drawer it sits in:
        # under the 260806 naming rule a page's companion folder carries the
        # page's own name, so `QA-probe/QBt5-for-value/2-x.md` needs no line at
        # all. Prefer the declared one where it exists, because a page can only
        # be in one folder but may be renamed, and a stale `requires:` should be
        # caught rather than silently overridden by the folder.
        requires = re.search(r"^-?\s*requires:\s*([^\s,]+)\s*$", text, re.M)
        topic_id = requires.group(1) if requires else relative.parts[-2]
        if topic_id not in topics:
            how = ("its `requires:` line names" if requires
                   else "the drawer it sits in is named for")
            report.add("ERROR", "topic-entry-requires-topic", where,
                       f"a QA record must answer to one evidence page carrying a "
                       f"route: head key, and {how} `{topic_id}`, which is not one")
            continue

        # Two record shapes are live, and the file itself says which it is.
        # FOUR-SLOT is the shape written before 260806: `#### Q-executor`,
        # `#### consumer trace`, `#### bank binding`, `#### A-executor`, with
        # the state inside the binding block. LEAN is the shape ruled on
        # 260806, after JL observed that three of those four slots were copies
        # of something that already existed elsewhere: the bank's question, the
        # evidence page's consumers, and the bank's answer. What survives is
        # the head keys and the same three sections a QA-bank wears.
        lean = not any(re.search(rf"(?im)^#### {re.escape(h)}\s*$", text)
                       for h in ENTRY_HEADINGS)
        if lean:
            check_lean_record(text, where, report)
        else:
            check_four_slot_record(text, where, report)

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

        # A topic page may opt into the paired EVIDENCE -> DISPLAY workflow with
        # `display: companion` in its metadata head.  New Value and Literature
        # pages do this.  Old pages remain readable while they migrate.
        if head_key(topic_text, "display") == "companion":
            divisions = [body for n, _q, body in e_divisions(topic_text)
                         if n > 0 and rel_from_topic and rel_from_topic in body]
            if len(divisions) == 1:
                pointers = DISPLAY_POINTER.findall(divisions[0])
                if len(pointers) != 1:
                    report.add("ERROR", "topic-display-pointer", where,
                               "a companion-enabled E division needs exactly one "
                               "`🖼 Display:` pointer")
                else:
                    display_rel, display_state = pointers[0]
                    if display_state not in DISPLAY_STATES:
                        allowed = " · ".join(sorted(DISPLAY_STATES))
                        report.add("ERROR", "topic-display-state", where,
                                   f"display state {display_state!r} is not one of {allowed}")
                    display_path = topic_path.parent / display_rel
                    if not display_path.is_file():
                        report.add("ERROR", "topic-display-missing", where,
                                   f"display companion `{display_rel}` does not exist")
                    else:
                        card_state = head_key(
                            display_path.read_text(encoding="utf-8"), "state"
                        ).split("·")[0].strip().lower()
                        if card_state != display_state:
                            report.add("ERROR", "topic-display-state", where,
                                       f"display pointer says `{display_state}` but companion "
                                       f"says `{card_state or 'missing'}`")

        if lean:
            # A lean record carries no consumer trace, on purpose: who is
            # waiting is the evidence page's `#### consumers`, and holding it
            # in two files is how the two drift. The division check above has
            # already proven this record is pointed at from exactly one E
            # division, which is the same binding read from the other end.
            continue

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
