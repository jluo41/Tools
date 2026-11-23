"""A part line with no label is still its part; an untagged Page line after a Draft is named (AgreeableJama 261122)."""
import pytest

from src.folder_health import FAIL, WARN, folder_health
from src.plan_shape import iter_plan_bullets
from tests.test_folder_health import BULLET, FACE, HEADER, make, levels

SECTIONED = """# Sample-Page · draft v1.1
draft-version: v1.1
approved: ⬜

## 1 · Structure · Bullet Point Table

### Structure Overview

{part}
- C1.P1 · State the answer · S1 to S1
- C2.P2 · Say more · S2 to S2

### C1.P1 · State the answer · S1 to S1
- B1 · S1 · [Claim] First claim
  Evidence: none · a definition

### C2.P2 · Say more · S2 to S2
- B2 · S2 · [Claim] Second claim
  Evidence: none · a definition

## 3 · Draft · Reading and Revise

### C1.P1 · State the answer · S1 to S1
- B1 · S1 · The first sentence.

### C2.P2 · Say more · S2 to S2
- B2 · S2 · The second sentence.
"""


@pytest.mark.parametrize("form", ["- C{n} · Answer", "- C{n}", "- C{n} ·", "- **C{n}**", "- **C{n}** · Answer"])
def test_a_bare_part_line_still_addresses_its_part(form):
    parts = "\n".join(form.format(n=n) for n in (1, 2))
    text = SECTIONED.replace("{part}", parts)
    assert [b["address"] for b in iter_plan_bullets(text)] == ["C1.P1.B1", "C2.P2.B2"]


def test_a_bullet_under_no_part_says_the_part_line_needs_a_label(tmp_path):
    plan = HEADER + BULLET.replace("## C1 · Answer\n", "")
    found = [f for f in folder_health(make(tmp_path, plan=plan))["findings"] if f["check"] == "structure"]
    assert any(f["level"] == FAIL and "part line needs a label" in f["message"] for f in found)


def test_an_untagged_page_line_after_the_draft_is_named(tmp_path):
    face = FACE + "An untagged sentence the Draft lacks.\n"
    report = folder_health(make(tmp_path, face=face))
    named = [f["message"] for f in report["findings"] if f["check"] == "sync" and "C1.P1.B2:" in f["message"]]
    assert named and "untagged text" in named[0] and "An untagged sentence" in named[0]
    assert WARN in levels(report, "sync")
