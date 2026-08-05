import tempfile
import unittest
from pathlib import Path

from src.topic_entry_contract import check_topic_entries


class _Report:
    def __init__(self):
        self.rows = []

    def add(self, level, code, where, message):
        self.rows.append((level, code, where, message))


TOPIC = """# S Literature 1 · Topic
state: 🟡 PARTIAL
owner: JL
requires: S-Literature-Dash

## Opening
What question does this topic own?

## Stage Contract

## Content

### Q-consumer register

- **Q-Topic-1**: the paper stake that this topic owns.

## Aims

- A1 · Register is available
  - [x] The canonical consumer is on this topic page.

## States

- A1 · Register is available
  ✅ Written here.
"""

# Ruling B (JL 260806): an entry is a hidden SOURCE RECORD named <n>-<slug>.md,
# not a board page. It carries no page frame; the digit-first name keeps it out
# of page_files, so the checker finds it with its own probes/ glob.
ENTRY = """# Entry
requires: S-Literature-1

#### q-executor
What neutral answer does the bank owe?

#### consumer trace
* **Q-Topic-1**: this is the paper stake retained for audit.

#### bank binding
**state**: deferred

#### a-executor
No answer has returned yet.
"""


class TopicEntryContractTest(unittest.TestCase):
    def test_complete_entry_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            board = Path(tmp)
            topic = board / "S-Literature-1-topic.md"
            entry = board / "probes" / "L01-topic" / "1-entry.md"
            entry.parent.mkdir(parents=True)
            topic.write_text(TOPIC, encoding="utf-8")
            entry.write_text(ENTRY, encoding="utf-8")
            report = _Report()

            # the entry record is NOT in pages: the checker's own glob finds it
            check_topic_entries(board, {topic.name: topic}, report)

            self.assertEqual([], report.rows)

    def test_entry_must_require_the_direct_topic(self):
        with tempfile.TemporaryDirectory() as tmp:
            board = Path(tmp)
            topic = board / "S-Literature-1-topic.md"
            entry = board / "probes" / "L01-topic" / "1-entry.md"
            entry.parent.mkdir(parents=True)
            topic.write_text(TOPIC, encoding="utf-8")
            entry.write_text(ENTRY.replace("requires: S-Literature-1", "requires: S-Literature-Dash"), encoding="utf-8")
            report = _Report()

            check_topic_entries(board, {topic.name: topic}, report)

            self.assertEqual(["topic-entry-requires-topic"], [row[1] for row in report.rows])
