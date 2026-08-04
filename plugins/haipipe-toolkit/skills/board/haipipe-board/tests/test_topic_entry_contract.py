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

ENTRY = """# S Literature 5 · Entry
state: 🟡 PARTIAL
owner: JL
requires: S-Literature-1

## Opening
What answer does this entry request?

## Stage Contract

## Content

#### q-executor
What neutral answer does the bank owe?

#### consumer trace
* **Q-Topic-1**: this is the paper stake retained for audit.

#### bank binding
**state**: deferred

#### a-executor
No answer has returned yet.

## Aims

- A1 · Entry contract is complete
  - [x] The entry has its four parts.

## States

- A1 · Entry contract is complete
  ✅ Written here.
"""


class TopicEntryContractTest(unittest.TestCase):
    def test_complete_entry_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            board = Path(tmp)
            topic = board / "S-Literature-1-topic.md"
            entry = board / "probes" / "L01-topic" / "S-Literature-5-entry.md"
            entry.parent.mkdir(parents=True)
            topic.write_text(TOPIC, encoding="utf-8")
            entry.write_text(ENTRY, encoding="utf-8")
            report = _Report()

            check_topic_entries(board, {topic.name: topic, entry.name: entry}, report)

            self.assertEqual([], report.rows)

    def test_entry_must_require_the_direct_topic(self):
        with tempfile.TemporaryDirectory() as tmp:
            board = Path(tmp)
            topic = board / "S-Literature-1-topic.md"
            entry = board / "probes" / "L01-topic" / "S-Literature-5-entry.md"
            entry.parent.mkdir(parents=True)
            topic.write_text(TOPIC, encoding="utf-8")
            entry.write_text(ENTRY.replace("requires: S-Literature-1", "requires: S-Literature-Dash"), encoding="utf-8")
            report = _Report()

            check_topic_entries(board, {topic.name: topic, entry.name: entry}, report)

            self.assertEqual(["topic-entry-requires-topic"], [row[1] for row in report.rows])
