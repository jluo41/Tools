"""workflow_drawing.py: make writes a forwarding builder and a words yaml; draw reads the telling, the Board Questions'
reports and the newest version's Review Items, and marks what the reviewers hit (red) and what fixes it (green)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import workflow_drawing as wd  # noqa: E402

FACE = """s02 · The telling
=================

**Topic:** Can lessons from one experiment design the next?

| E | RQ | proposition | support state | basis |
|---|---|---|---|---|
| E1 | RQ1 | lessons predict | absent | needs T4 |

| D | name | question | folder |
|---|---|---|---|
| D1 | Has anyone done this? | we look | none yet |

| T | name | question | feeds |
|---|---|---|---|
| T1 | The data | we pull the data | none |
| T4 | Predict | we predict the held-out round | none |
"""

REPORT = """# Do they hold?

#### 3.1 · Question 1 · RQ1
- **Name**: Getting reliable insights
- **Question**: Do the lessons hold on outcomes they never saw?
- **Section**: Results

**Tasks**
- Inputs · One ladder: three inputs of rising richness

**Hypotheses**
- **1a** · Do the lessons hold?: lessons predict the held-out round · tested by E1

**Potential claims**
- **1a** · C1 · from 1a · Insights that predict: lessons predict outcomes they never saw
  - **Role**: headline

**Potential contributions**
- rests on 1a · A reliability test: a way to check lessons

**Potential work**
- **T4** · for 1a
- **D1** · for 1a

### 2 · Evidence
"""

COMMENTS = """# q01_review-0916

page-type: comments

## Review Items

| item | cites | lands on | hits | fixed by | work | reply | state |
|---|---|---|---|---|---|---|---|
| Review-more-shots | R1.1 · E1.2 | t03_research-design | data | T4 · D1 | | | open |
| Review-scope | R2.1 | t01_introduction | — | t01_introduction | | | open |
| Review-orphan | R2.2 | t04_results | data | | | | open |

## Aims
"""


def board(tmp_path):
    (tmp_path / "env.sh").write_text("", encoding="utf-8")
    (tmp_path / "Tools").symlink_to(wd.SKILLS.parents[2])                 # a SPACE reaches Tools by its link
    proj = tmp_path / "Proj"
    (proj / "work").mkdir(parents=True)
    (proj / "project.yaml").write_text("profile: research\n", encoding="utf-8")
    b = proj / "paper" / "Paper-X"
    (b / "studio" / "s02-story").mkdir(parents=True)
    (b / "board.md").write_text("# Paper-X\n\nstory-current: s02-story\n\n## Questions\n\n```yaml\nquestions:\n"
                                "- id: Q01\n  report: reports/q01_hold/q01_hold.md\n```\n", encoding="utf-8")
    (b / "studio" / "s02-story" / "s02-story.md").write_text(FACE, encoding="utf-8")
    (b / "reports" / "q01_hold").mkdir(parents=True)
    (b / "reports" / "q01_hold" / "q01_hold.md").write_text(REPORT, encoding="utf-8")
    c = b / "j02_v0916_desk" / "reports" / "q01_review-0916"
    c.mkdir(parents=True)
    (c / "q01_review-0916.md").write_text(COMMENTS, encoding="utf-8")
    topic = b / "studio" / "s04-paper-workflow"
    topic.mkdir()
    return b, topic


def texts(path):
    els = json.loads(path.read_text(encoding="utf-8"))["elements"]
    return [(e.get("text", ""), e.get("strokeColor")) for e in els if e.get("type") == "text"]


def test_make_then_draw_with_the_overlay(tmp_path):
    b, topic = board(tmp_path)
    builder = wd.make(topic)
    assert builder.name == "build_s04_paper_workflow.py"
    assert "/Users/" not in builder.read_text(encoding="utf-8")              # a relative path through the SPACE
    assert (topic / "s04-paper-workflow-drawing.yaml").is_file()
    out = wd.draw(topic)
    assert out.name == "s04-paper-workflow.excalidraw"
    tx = texts(out)
    words = " ".join(t for t, _ in tx)
    assert "Question 1 · Getting reliable insights" in words                # the question row, from its report
    assert "T4 Predict" in words and "D1 Has anyone done this?" in words      # the analysis, from the face
    red = [t for t, c in tx if c == wd.RED]
    green = [t for t, c in tx if c == wd.GREEN]
    assert any("reviewers: more shots, orphan" in t for t in red)            # the data card was hit
    assert sum("fixes: more shots" in t for t in green) == 2                 # by T4 and by D1
    assert any("fixed in the writing" in t and "scope → t01_introduction" in t for t in green)
    assert any("nothing fixes yet: orphan" in t for t in red)


def test_no_comments_no_overlay(tmp_path):
    b, topic = board(tmp_path)
    for p in sorted(b.glob("j02_*/reports/*/*.md")):
        p.unlink()
    wd.make(topic)
    tx = texts(wd.draw(topic))
    assert not [t for t, c in tx if c in (wd.RED, wd.GREEN) and ("reviewers" in t or "fixes" in t)]


def test_count_reads_a_json_on_disk(tmp_path):
    root = tmp_path
    (root / "d.json").write_text(json.dumps({"designs": [{"job": "j01", "released": "261012"}] * 3}), encoding="utf-8")
    spec = {"json": "d.json", "list": "designs", "where": {"job": "j01"}, "say": "{n} released {released}"}
    assert wd.count_line(spec, root) == "3 released 261012"
    assert wd.count_line({**spec, "where": {"job": "j05"}, "none": "held"}, root) == "held"
