import tempfile
import unittest
from pathlib import Path

from src.topic_entry_contract import check_topic_entries


class _Report:
    def __init__(self):
        self.rows = []

    def add(self, level, code, where, message):
        self.rows.append((level, code, where, message))


# An evidence page (JL 260806): the type key is the head `route:` line, and
# Content is organized BY EXECUTOR: one `### E<n> ·` division per Q-executor
# conversation pointing at its QA-probe, plus the standing E0 incoming queue.
TOPIC = """# S Literature 1 · Topic
state: 🟡 PARTIAL
owner: JL
route: outward
requires: S-Literature-Dash

## Opening
What question does this topic own?

## Stage Contract

## Content

### E0 · incoming

<empty>

### E1 · What neutral answer does the bank owe?

🔗 QA-probe: `probes/L01-topic/1-entry.md` · state: deferred

#### consumers
- ⬜ `Q-Topic-1` · from `S-Literature-Dash` · the paper stake that this topic owns.

#### answer digest
No answer has returned yet.

## Aims

- A1 · Register is available
  - [x] The canonical consumer is on this topic page.

## States

- A1 · Register is available
  ✅ Written here.
"""

# Ruling B (JL 260806): a QA-probe is a hidden SOURCE RECORD named
# <n>-<slug>.md, not a board page. It carries no page frame; the digit-first
# name keeps it out of page_files, so the checker finds it with its own
# probes/ glob. The slot words wear the four capitals.
ENTRY = """# Entry
requires: S-Literature-1

#### Q-executor
What neutral answer does the bank owe?

#### consumer trace
* **Q-Topic-1**: this is the paper stake retained for audit.

#### bank binding
**state**: deferred

#### A-executor
No answer has returned yet.
"""


def _write(board: Path, topic_text: str = TOPIC, entry_text: str = ENTRY):
    topic = board / "S-Literature-1-topic.md"
    entry = board / "probes" / "L01-topic" / "1-entry.md"
    entry.parent.mkdir(parents=True)
    topic.write_text(topic_text, encoding="utf-8")
    entry.write_text(entry_text, encoding="utf-8")
    return topic, entry


class TopicEntryContractTest(unittest.TestCase):
    def test_complete_entry_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            board = Path(tmp)
            topic, _entry = _write(board)
            report = _Report()

            # the QA-probe record is NOT in pages: the checker's own glob finds it
            check_topic_entries(board, {topic.name: topic}, report)

            self.assertEqual([], report.rows)

    def test_entry_must_require_the_direct_topic(self):
        with tempfile.TemporaryDirectory() as tmp:
            board = Path(tmp)
            topic, entry = _write(board)
            entry.write_text(ENTRY.replace("requires: S-Literature-1",
                                           "requires: S-Literature-Dash"),
                             encoding="utf-8")
            report = _Report()

            check_topic_entries(board, {topic.name: topic}, report)

            self.assertEqual(["topic-entry-requires-topic"], [row[1] for row in report.rows])

    def test_lowercase_slot_heading_warns_but_still_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            board = Path(tmp)
            topic, entry = _write(board)
            # exercise the deprecated lowercase casing without carrying the
            # literal string that repo-wide casing sweeps grep for
            entry.write_text(ENTRY.replace("#### Q-executor",
                                           "#### Q-executor".lower()),
                             encoding="utf-8")
            report = _Report()

            check_topic_entries(board, {topic.name: topic}, report)

            self.assertEqual([("WARN", "topic-entry-heading-case")],
                             [(row[0], row[1]) for row in report.rows])

    def test_probe_unlinked_from_any_e_division_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            board = Path(tmp)
            topic, _entry = _write(
                board, TOPIC.replace("`probes/L01-topic/1-entry.md`", "`nothing`"))
            report = _Report()

            check_topic_entries(board, {topic.name: topic}, report)

            self.assertEqual(["topic-probe-division"], [row[1] for row in report.rows])

    def test_page_without_route_head_key_is_not_a_topic(self):
        with tempfile.TemporaryDirectory() as tmp:
            board = Path(tmp)
            topic, _entry = _write(board, TOPIC.replace("route: outward\n", ""))
            report = _Report()

            check_topic_entries(board, {topic.name: topic}, report)

            # no topic detected, so the overlay stays silent
            self.assertEqual([], report.rows)


if __name__ == "__main__":
    unittest.main()
