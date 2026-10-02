"""check_evidence on a fixture board: one fit answer per kind of citation, then each way it breaks."""

import importlib.util
import json
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location(
    "check_evidence", Path(__file__).resolve().parents[1] / "ref" / "check_evidence.py")
ce = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ce)

MT02 = """# Information register

### 1 · Queue

**Queue**: this rung's questions.

```text
id   question              full         alpha
─────────────────────────────────────────────────
QI1  how fast do rates     ✅ I01-full  🚫 full-only
     move by group?
QI2  unplanned question    ✅ I02-full  ·

🚫 a note with a token ✅ I09-full that is not a cell
```

#### 2 · QI1 · Rates By Group

**The ask**: rate by group, with an interval.
**What would answer it**: per-group rates with intervals.
- E1 · compute · rate per group with a 95% interval · pass: an interval per group
    cut: full
    unit: one sent message
    measure: click rate · ask: "rate"
    by: group · ask: "by group"
    uncertainty: Wilson 95% interval
    rivals: none
    output: rates.csv [level, rate, ci_lo, ci_hi]
**Ask covered**: "rate by group" → E1 · "with an interval" → E1
**Needs agreed**: ✅ 261001

#### 3 · QI2 · Unplanned

**What would answer it**: prose only.
"""

MT03 = """# Knowledge register

### 1 · Queue

```text
id   question            full
──────────────────────────────────
QK1  does group matter?  ✅ K01-full
```

#### 2 · QK1 · Group Matters

**The ask**: does the group gain matter, with its uncertainty?
**What would answer it**: the gain and a reading.
- E1 · cite · the rates · from: QI1.E1
- E2 · compute · gain with its uncertainty · pass: an interval on the gain
    cut: the cell's partition
    unit: one sent message
    measure: click-rate gain of a per-group message over the pooled best · ask: "group gain"
    by: grouping · ask: "group"
    uncertainty: cross-fitted standard error
    rivals: none
    output: gain.csv [grouping, gain, ci_lo]
- E3 · judge · is the gain material? · from: E1, E2
**Ask covered**: "does the group gain matter" → E1, E2, E3 · "with its uncertainty" → E2
**Needs agreed**: ⬜
"""

RATES = "run_b51j21t01r01_full_rates"
GAIN = "run_b51j31t01r01_full_gain"


def task(root, job, name, run, answers):
    t = root / "tasks" / "b51_x" / job / name
    (t / "runs").mkdir(parents=True)
    (t / "scripts" / "config").mkdir(parents=True)
    (t / "runs" / f"{run}.sh").write_text("#!/bin/bash\n", encoding="utf-8")
    (t / "scripts" / "config" / f"{run}.yaml").write_text(f"answers: [{answers}]\n", encoding="utf-8")
    return t


def page(board, folder, stem, body, answers=None, tickets=None, ended="2026-10-01T10:00:00Z"):
    d = board / folder / stem
    (d / "runs").mkdir(parents=True)
    (d / f"{stem}.md").write_text(body, encoding="utf-8")
    if answers is not None:
        (d / "answers.yaml").write_text(answers, encoding="utf-8")
    for ticket, (job, name, run, tables) in (tickets or {}).items():
        (d / "runs" / f"{ticket}.sh").write_text(
            f'#!/bin/bash\nexec "${{PAGE}}/../../../../tasks/b51_x/{job}/{name}/runs/{run}.sh"\n', encoding="utf-8")
        r = d / "results" / ticket
        r.mkdir(parents=True)
        (r / "runtime.yaml").write_text(f"status: ok\nended: {ended}\n", encoding="utf-8")
        for fname, text in tables.items():
            (r / fname).write_text(text, encoding="utf-8")
    return d


@pytest.fixture
def board(tmp_path):
    project = tmp_path / "Project-Demo"
    b = project / "insights" / "Demo-InsightBoard"
    for stem, text in (("MT02-question-information", MT02), ("MT03-question-knowledge", MT03)):
        (b / "0-MT-meta" / stem).mkdir(parents=True)
        (b / "0-MT-meta" / stem / f"{stem}.md").write_text(text, encoding="utf-8")
    task(project, "j21_information_x", "t01_rates", "r01_full", "QI1.E1")
    task(project, "j31_knowledge_x", "t01_gain", "r01_full", "QK1.E2")
    # an old-style page that cites by inline tag
    page(b, "1-full", "I01-full-rates",
         "# Rates\n\nresults-read: 2026-10-01T12:00:00Z\n\n## Opening\n\nGroup b leads [QI1.E1].\n",
         answers=f"QI1:\n  E1: {{ticket: {RATES}, files: [rates.csv]}}\n",
         tickets={RATES: ("j21_information_x", "t01_rates", "r01_full",
                          {"rates.csv": "level,rate,ci_lo,ci_hi\na,1,0,2\n"})})
    page(b, "1-full", "I02-full-other", "# Other\n\nanswers: QI2\n")
    # a Page Face page that cites through its plan and Evidence Items
    k = page(b, "1-full", "K01-full-group",
             "# Group gain: click effect\n\nresults-read: 2026-10-01T12:00:00Z\n\n## Opening\n\nDoes it matter?\n\n"
             "## Content\n\n### 1 · Rates\n\n#### 1.1 · Rates\nRates differ. <!-- realizes: C1.P1.B1 -->\n\n"
             "### 2 · Gain\n\n#### 2.1 · Gain\nThe gain is nil. <!-- realizes: C2.P2.B1 -->\n\n"
             "### 3 · Claim\n\n#### 3.1 · Claim\nNot material. <!-- realizes: C3.P3.B1 -->\n",
             answers=f"QK1:\n  E1: {{pages: [I01-full]}}\n  E2: {{ticket: {GAIN}, files: [gain.csv]}}\n  E3: judge\n",
             tickets={GAIN: ("j31_knowledge_x", "t01_gain", "r01_full",
                             {"gain.csv": "grouping,gain,ci_lo,ci_hi\nx,0,-1,1\n"})})
    (k / "draft").mkdir()
    (k / "draft" / "K01-full-group-evidence-items.md").write_text(
        "# Items\n\n### E01-VALUE-rates · C1.P1.B1 · the rates\n\n- **Need**: QK1.E1 ← QI1.E1\n"
        "- **Artifact**: `../I01-full-rates/results/run_b51j21t01r01_full_rates/rates.csv`\n\n"
        f"### E02-VALUE-gain · C2.P2.B1 · the gain\n\n- **Need**: QK1.E2\n- **Artifact**: `results/{GAIN}/gain.csv`\n",
        encoding="utf-8")
    (k / "draft" / "K01-full-group-draft-v0.1.md").write_text(
        "# plan\n\n## 1 · Structure · Bullet Point Table\n\n### C1.P1 · Rates\n- B1 · [Rates] The rates differ.\n"
        "  Evidence: E01-VALUE-rates · the rates\n\n### C2.P2 · Gain\n- B1 · [Gain] The gain is nil.\n"
        "  Evidence: E02-VALUE-gain · the gain\n\n### C3.P3 · Claim\n- B1 · [Claim] Not material.\n"
        "  Evidence: none · judge QK1.E3 from E1, E2\n\n## 2 · Scratch\n", encoding="utf-8")
    return b


def verdicts(board):
    return {(r["question"], r["page"]): r for r in ce.run(board)}


def test_queue_reads_rows_not_notes():
    cells = ce.parse_queue(MT02)
    assert ("QI1", "✅", "I01-full") in cells
    assert all(p != "I09-full" for _q, _m, p in cells)


def test_spec_lines_are_read():
    need = ce.parse_needs("QI1", MT02.split("#### 2 · QI1")[1])[0]
    assert need.spec["cut"] == "full" and need.outputs() == {"rates.csv": ["level", "rate", "ci_lo", "ci_hi"]}


def test_fit_answers_pass(board):
    v = verdicts(board)
    assert v[("QI1", "I01-full")]["verdict"] == "OK"
    assert v[("QK1", "K01-full")]["verdict"] == "OK", v[("QK1", "K01-full")]["problems"]
    assert "needs not agreed" in v[("QK1", "K01-full")]["notes"]
    assert v[("QI2", "I02-full")]["verdict"] == "UNPLANNED"
    assert ce.main([str(board)]) == 0
    assert ce.main([str(board), "--strict"]) == 1


def test_unrealized_item_is_an_overclaim(board):
    md = board / "1-full/K01-full-group/K01-full-group.md"
    md.write_text(md.read_text().replace(" <!-- realizes: C2.P2.B1 -->", ""))
    r = verdicts(board)[("QK1", "K01-full")]
    assert r["verdict"] == "GAP" and r["overclaim"]
    assert any("QK1.E2: not cited" in p for p in r["problems"])


def test_missing_spec_column_is_a_gap(board):
    (board / "1-full/I01-full-rates/results" / RATES / "rates.csv").write_text("level,rate\na,1\n")
    r = verdicts(board)[("QI1", "I01-full")]
    assert r["verdict"] == "GAP"
    assert any("rates.csv has no column ci_lo" in p for p in r["problems"])


def test_config_must_list_the_need(board):
    cfg = board.parents[1] / "tasks/b51_x/j21_information_x/t01_rates/scripts/config/r01_full.yaml"
    cfg.write_text("answers: [QI1]\n")
    r = verdicts(board)[("QI1", "I01-full")]
    assert any("does not list QI1.E1" in p for p in r["problems"])


def test_reasoned_compute_need_and_bare_refusal_are_gaps(board):
    (board / "1-full/K01-full-group/answers.yaml").write_text(
        "QK1:\n  E1: {pages: [I01-full]}\n  E2: judge\n  E3: judge\n")
    r = verdicts(board)[("QK1", "K01-full")]
    assert any("QK1.E2: a compute need binds ticket and files" in p for p in r["problems"])
    (board / "1-full/K01-full-group/answers.yaml").write_text(
        "QK1:\n  E1: {pages: [I01-full]}\n  E2: {refused: no field}\n  E3: judge\n")
    r = verdicts(board)[("QK1", "K01-full")]
    assert any("a refusal needs its probe run" in p for p in r["problems"])


def test_missing_spec_is_unplanned_and_wrong_cut_is_a_gap(board):
    mt02 = board / "0-MT-meta/MT02-question-information/MT02-question-information.md"
    mt02.write_text(mt02.read_text().replace("    cut: full\n", "    cut: alpha\n"))
    assert any("spec cut is alpha" in p for p in verdicts(board)[("QI1", "I01-full")]["problems"])
    text = mt02.read_text()
    spec = text[text.index("    cut:"):text.index("**Needs agreed**")]
    mt02.write_text(text.replace(spec, ""))
    assert verdicts(board)[("QI1", "I01-full")]["verdict"] == "UNPLANNED"


def test_result_newer_than_reading_is_stale(board):
    rt = board / "1-full/I01-full-rates/results" / RATES / "runtime.yaml"
    rt.write_text("status: ok\nended: 2026-10-02T09:00:00Z\n")
    r = verdicts(board)[("QI1", "I01-full")]
    assert r["verdict"] == "STALE" and r["overclaim"]


def test_no_entry_is_unbound_and_kind_rules_hold(board):
    (board / "1-full/I01-full-rates/answers.yaml").write_text("{}\n")
    assert verdicts(board)[("QI1", "I01-full")]["verdict"] == "UNBOUND"
    mt02 = board / "0-MT-meta/MT02-question-information/MT02-question-information.md"
    mt02.write_text(mt02.read_text().replace("· compute · rate per group", "· judge · rate per group"))
    r = verdicts(board)[("QI1", "I01-full")]
    assert any("judge need is not legal at rung I" in p for p in r["problems"])


def test_json_output(board, capsys):
    assert ce.main([str(board), "--format", "json"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["failed"] == 0 and len(out["cells"]) == 3


def test_cite_of_a_retired_or_unknown_need_is_a_gap(board):
    mt02 = board / "0-MT-meta/MT02-question-information/MT02-question-information.md"
    mt02.write_text(mt02.read_text().replace("pass: an interval per group\n",
                                             "pass: an interval per group · retired: test\n", 1))
    r = verdicts(board)[("QK1", "K01-full")]
    assert any("cites QI1.E1, which is retired" in p for p in r["problems"])
    mt03 = board / "0-MT-meta/MT03-question-knowledge/MT03-question-knowledge.md"
    mt03.write_text(mt03.read_text().replace("from: QI1.E1", "from: QI1.E9"))
    r = verdicts(board)[("QK1", "K01-full")]
    assert any("cites QI1.E9, which QI1 does not list" in p for p in r["problems"])


def test_bound_run_must_be_on_the_cut_the_spec_names(board):
    cfg = board.parents[1] / "tasks/b51_x/j21_information_x/t01_rates/scripts/config/r01_full.yaml"
    cfg.write_text(cfg.read_text() + "population: {name: alpha}\n")
    r = verdicts(board)[("QI1", "I01-full")]
    assert any("runs on population alpha; the spec's cut asks for full" in p for p in r["problems"])


def test_plan_must_answer_its_own_ask(board):
    mt02 = board / "0-MT-meta/MT02-question-information/MT02-question-information.md"
    base = mt02.read_text()
    # a causal ask at the Information rung
    mt02.write_text(base.replace("**The ask**: rate by group, with an interval.",
                                 "**The ask**: does group move the rate, with an interval?"))
    probs = verdicts(board)[("QI1", "I01-full")]["problems"]
    assert any("the ask claims a cause ('move')" in p for p in probs)
    # an ask word no need answers
    mt02.write_text(base.replace("**The ask**: rate by group, with an interval.",
                                 "**The ask**: rate by group and its missingness, with an interval."))
    assert any("ask words no need answers: missingness" in p for p in verdicts(board)[("QI1", "I01-full")]["problems"])
    # a spec line that names no part of the ask
    mt02.write_text(base.replace('    measure: click rate · ask: "rate"\n', "    measure: click rate beside its share\n"))
    assert any('spec measure: carries no ask:' in p for p in verdicts(board)[("QI1", "I01-full")]["problems"])


def test_a_run_answers_one_question(board):
    cfg = board.parents[1] / "tasks/b51_x/j21_information_x/t01_rates/scripts/config/r01_full.yaml"
    cfg.write_text(cfg.read_text().replace("answers: [QI1.E1]", "answers: [QI1.E1, QI5.E2]"))
    r = verdicts(board)[("QI1", "I01-full")]
    assert any("also serves QI5; a run answers one question" in p for p in r["problems"])
