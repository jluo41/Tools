"""M-D09 and M-D19 (JL 261115 "now it is jumping, disturb things a lot"): while a version drafts, a Section's plan
that differs from its Narrative row, or a Story row that moved, never fails the Section; the version Job carries one
quiet note, and `page.py sync-narrative` rebuilds the rows as a diff, leaving the Narrative to sign once."""
import subprocess
import sys
from pathlib import Path

from src import narrative_sync
from src.folder_health import FAIL, INFO, WARN, folder_health
from src.page_sign import sign, sign_narrative

SKILL = Path(__file__).resolve().parents[1]
STORY = """# s02-story

### 8 · Section Narrative

| id | claim | number |
|---|---|---|
| C1 | The gain fades. | 8% |
| C2 | Reuse does not replace new readings. | 4% |

### 9 · Venue

x
"""
JOB = """# j11_writing_v1
state: drafting

## Narrative

Claims to displays: C1 Figure 2 · C2 Figure 3

| Section | reader question | ordered moves | displays | claims |
|---|---|---|---|---|
| t02_results | What did scale do? | the study → the gain fades | Figures 1 to 3 | C1, C2 |

## Questions
"""
PLAN = """# t02_results · draft v1.1
draft-version: v1.1
approved: ⬜
status: working
arc: the study, then what scale did

## 1 · Structure · Bullet Point Table

### Structure Overview

- C1 · The study
- C1.P1 · Data and models
  → s1 to s2
- C2 · The forecast gain fades with the horizon
- C2.P2 · Short forecasts gain most
  → s3 to s4

### C1.P1 · Data and models · s1 to s2
- B1 · s1 · [Data] Patients.
  Evidence: E01-DISPLAY-fig1
- B2 · s2 · [Models] Sizes.
  Evidence: none · design

### C2.P2 · Short forecasts gain most · s3 to s4
- B1 · s3 · [Finding] Short gains most.
  Evidence: E02-DISPLAY-fig2
- B2 · s4 · [Evidence] 8%.
  Evidence: E03-VALUE-gain
"""
FACE = """# t02_results
task-type: draft
claim-ids: C1 the gain fades · C2 reuse does not replace new readings

## 📚 Content

Patients. <!-- realizes: C1.P1.B1 -->
"""


def make(tmp_path: Path) -> Path:
    (tmp_path / "board.md").write_text("# Paper-X\nboard-kind: paper-board\nstory-current: s02-story\n", encoding="utf-8")
    (tmp_path / "s02-story").mkdir()
    (tmp_path / "s02-story" / "s02-story.md").write_text(STORY, encoding="utf-8")
    job = tmp_path / "j11_writing_v1"
    sec = job / "t02_results"
    (sec / "draft" / "records").mkdir(parents=True)
    (job / "j11_writing_v1.md").write_text(JOB, encoding="utf-8")
    (sec / "t02_results.md").write_text(FACE, encoding="utf-8")
    (sec / "draft" / "t02_results-draft-v1.1.md").write_text(PLAN, encoding="utf-8")
    return job


def checks(report, name):
    return [f for f in report["findings"] if f["check"] == name]


def test_a_section_plan_that_differs_from_its_row_never_fails_the_section(tmp_path):
    job = make(tmp_path)
    sec = job / "t02_results"
    assert sign_narrative(job, "this order")["ok"]
    assert sign(sec, "go with B")["ok"]
    face = job / "j11_writing_v1.md"
    face.write_text(face.read_text().replace("What did scale do?", "What did scale change?"), encoding="utf-8")
    for final in (False, True):
        report = folder_health(sec, final=final)
        assert checks(report, "row") == [] and checks(report, "narrative") == []
        assert not any("re-sign" in f["message"] or f["level"] == FAIL and "narrative" in f["message"]
                       for f in report["findings"])
    notes = checks(folder_health(job), "narrative")
    assert [n["level"] for n in notes] == [INFO]
    assert notes[0]["message"] == ("the Narrative differs from 1 Section plans; rebuild it with page.py "
                                   "sync-narrative when the Sections are good")
    final = checks(folder_health(job, final=True), "narrative")
    assert [n["level"] for n in final] == [WARN] and "not rebuilt" in final[0]["message"]


def test_a_changed_story_row_never_fails_the_section(tmp_path):
    job = make(tmp_path)
    sec = job / "t02_results"
    assert sign_narrative(job, "this order")["ok"]
    assert sign(sec, "go with B")["ok"]
    story = tmp_path / "s02-story" / "s02-story.md"
    story.write_text(story.read_text().replace("The gain fades.", "The gain fades with the horizon."), encoding="utf-8")
    for final in (False, True):
        report = folder_health(sec, final=final)
        assert checks(report, "narrative") == [] and checks(report, "row") == []


def test_sync_narrative_prints_a_diff_and_apply_leaves_it_unsigned(tmp_path):
    job = make(tmp_path)
    assert sign_narrative(job, "this order")["ok"]
    out = subprocess.run([sys.executable, "-B", str(SKILL / "cli" / "page.py"), "sync-narrative", str(job)],
                         capture_output=True, text=True, cwd=SKILL)
    assert out.returncode == 0, out.stderr
    new = ("+| t02_results | What did scale do? | The study (Figure 1) → The forecast gain fades with the horizon "
           "(Figure 2) | Figure 1, Figure 2 | C1, C2 |")
    assert "-| t02_results | What did scale do? | the study → the gain fades | Figures 1 to 3 | C1, C2 |" in out.stdout
    assert new in out.stdout
    assert "+ C1 | The forecast gain fades with the horizon  (t02_results C2)" in out.stdout   # Story, for review
    face = job / "j11_writing_v1.md"
    assert "narrative-approved: ✅" in face.read_text()                     # the default only reads
    r = narrative_sync.apply(job)
    assert r["changed"] == ["t02_results"]
    text = face.read_text()
    assert new[1:] in text and "narrative-approved" not in text and "story-at-sign" not in text
    assert "Claims to displays: C1 Figure 2" in text and "## Questions" in text
    assert "The gain fades." in (tmp_path / "s02-story" / "s02-story.md").read_text()   # the Story is untouched
    assert "approved: ⬜" in (job / "t02_results" / "draft" / "t02_results-draft-v1.1.md").read_text()
    assert narrative_sync.differing(job) == []
    notes = checks(folder_health(job), "narrative")
    assert [n["level"] for n in notes] == [WARN] and "page.py sign-narrative" in notes[0]["message"]
    assert [n["level"] for n in checks(folder_health(job, final=True), "narrative")] == [WARN]
    assert sign_narrative(job, "the rebuilt rows")["ok"]                    # the person signs once
    assert checks(folder_health(job), "narrative") == []
