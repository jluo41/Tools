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


DRAWN = """s02 · Story: does it hold

**G0:** ⬜ not marked.

**The paper's question**: Do the lessons hold on
outcomes they never saw?

#### 3.1 · Question 1 · RQ1
- **Name**: Do they hold?
- **Research question**: Do the lessons hold on the held-out round? (RQ1a: on every arm?)
- **Section**: Results

**Hypotheses**
- **1a** · Hold: lessons predict the held-out round · tested by E1
- **1b** · Every arm: they predict on every arm · tested by E1

**Potential claims**
- **1a** · C1 · from 1a, 1b · Insights that predict: lessons predict outcomes they never saw
  - **Role**: primary

**Potential work**
- **T1** · for 1a
- **T2** · for 1b

| E | evidence | source | support state |
|---|---|---|---|
| E1 | they predict | b01.j01.t01.r01 | established |

| T | work | where | state | starts |
|---|---|---|---|---|
| T1 | Predict | b01.j01.t01 | done | done |
| T2 | Every arm, a new Run | b01.j01.t01 | ticket next | a person presses Run |
"""

PLAN = """s04 · Paper workflow: a demo

| Display | title | kind | answers | made by | state |
|---|---|---|---|---|---|
| Figure 1 | Predicted against seen | figure | RQ1 | b01.j01.t01.r02 | not started |
"""


def test_a_drawn_telling(tmp_path):
    """A 0.23 face: its question line, a claim on two hypotheses drawn once, a new Run in a Task that ran is not done,
    the analysis card's number read from its Result, and the display named on s04."""
    b, topic = board(tmp_path)
    (b / "board.md").write_text("# Paper-X\n\nstory-current: s02-story\n", encoding="utf-8")
    (b / "studio" / "s02-story" / "s02-story.md").write_text(DRAWN, encoding="utf-8")
    run = tmp_path / "Proj" / "work" / "b01_data" / "j01_tests" / "t01_predict" / "runs" / "r01_main" / "result"
    run.mkdir(parents=True)
    (run / "metrics.json").write_text(json.dumps({"r2": {"held_out": 0.61}}), encoding="utf-8")
    (b / "studio" / "s04-paper-workflow" / "s04-paper-workflow.md").write_text(PLAN, encoding="utf-8")
    flow = b / "studio" / "s03-paper-dataflow"
    flow.mkdir()
    wd.make(flow)
    words = flow / "s03-paper-dataflow-drawing.yaml"
    rel = run.relative_to(tmp_path) / "metrics.json"
    words.write_text(words.read_text(encoding="utf-8") +
                     f'numbers: {{T1: {{json: "{rel}", say: "R² {{r2_held_out:.2f}} on the held-out round"}}}}\n',
                     encoding="utf-8")
    out = wd.draw(flow)
    tx = " ".join(t for t, _ in texts(out))
    assert "Do the lessons hold on outcomes they never saw?" in tx            # the paper's question, wrapped
    assert "C1 · Insights that predict" in tx and "with Q1a → C1" in tx      # one claim, two hypotheses
    assert "no claim of its own" not in tx
    assert "R² 0.61 on the held-out round" in tx                              # an analysis card's number
    assert "Figure 1" in tx                                                    # from s04, named once
    assert "T2 Every arm, a new Run" in tx and "not run" in tx                 # its Task ran; this Run did not
    assert out.with_suffix(".png").is_file()


def test_count_reads_an_object(tmp_path):
    (tmp_path / "m.json").write_text(json.dumps({"rows": 1200, "share": {"none": 0.717}}), encoding="utf-8")
    assert wd.count_line({"json": "m.json", "say": "{rows:,} rows · {share_none:.1%} none"}, tmp_path) == \
        "1,200 rows · 71.7% none"
