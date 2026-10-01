"""check_evidence on a two-question fixture board: one fit answer, then each way it breaks."""

import importlib.util
import json
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location(
    "check_evidence", Path(__file__).resolve().parents[1] / "ref" / "check_evidence.py")
ce = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ce)

MT02 = """# Information register

## Content

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
**Needs agreed**: ✅ AB 261001
**Where it stands**: answered.

#### 3 · QI2 · Unplanned

**The ask**: something.
**What would answer it**: prose only.
**Where it stands**: answered.
"""

MT03 = """# Knowledge register

### 1 · Queue

```text
id   question            full
──────────────────────────────────
QK1  does group matter?  ✅ K01-full
```

#### 2 · QK1 · Group Matters

**What would answer it**: the gain and a reading.
- E1 · cite · the rates · from: QI1.E1
- E2 · compute · gain with its uncertainty · pass: an interval on the gain
- E3 · judge · is the gain material? · from: E1, E2
**Needs agreed**: ⬜
"""

TICKET = "run_b51j21t01r01_full_rates"


def page(root, folder, stem, body, answers=None, files=None, status="ok", ended="2026-10-01T10:00:00Z"):
    d = root / folder / stem
    (d / "runs").mkdir(parents=True)
    (d / f"{stem}.md").write_text(body, encoding="utf-8")
    if answers is not None:
        (d / "answers.yaml").write_text(answers, encoding="utf-8")
    for ticket, tables in (files or {}).items():
        (d / "runs" / f"{ticket}.sh").write_text("#!/bin/bash\n", encoding="utf-8")
        r = d / "results" / ticket
        r.mkdir(parents=True)
        (r / "runtime.yaml").write_text(f"status: {status}\nended: {ended}\n", encoding="utf-8")
        for name, text in tables.items():
            (r / name).write_text(text, encoding="utf-8")
    return d


@pytest.fixture
def board(tmp_path):
    b = tmp_path / "Demo-InsightBoard"
    for stem, text in (("MT02-question-information", MT02), ("MT03-question-knowledge", MT03)):
        (b / "0-MT-meta" / stem).mkdir(parents=True)
        (b / "0-MT-meta" / stem / f"{stem}.md").write_text(text, encoding="utf-8")
    page(b, "1-full", "I01-full-rates",
         "# Rates\n\nstate: ✅ · answers QI1\nresults-read: 2026-10-01T12:00:00Z\n\n## Opening\n\nGroup b leads [QI1.E1].\n",
         answers=f"QI1:\n  E1: {{ticket: {TICKET}, files: [rates.csv], fields: [ci_lo, ci_hi]}}\n",
         files={TICKET: {"rates.csv": "level,rate,ci_lo,ci_hi\na,1,0,2\n"}})
    page(b, "1-full", "I02-full-other", "# Other\n\nstate: ✅ · answers QI2\n")
    page(b, "1-full", "K01-full-group",
         "# Group\n\nresults-read: 2026-10-01T12:00:00Z\n\n## Opening\n\n"
         "Rates differ [QI1.E1]; the gain is nil [QK1.E2]; not material [QK1.E3].\n",
         answers=f"QK1:\n  E1: {{pages: [I01-full]}}\n  E2: {{ticket: {TICKET}, files: [gain.csv], fields: [ci_lo]}}\n  E3: judge\n",
         files={TICKET: {"gain.csv": "grouping,gain,ci_lo,ci_hi\nx,0,-1,1\n"}})
    return b


def verdicts(board):
    return {(r["question"], r["page"]): r for r in ce.run(board)}


def test_queue_reads_rows_not_notes(board):
    cells = ce.parse_queue(MT02)
    assert ("QI1", "✅", "I01-full") in cells
    assert all(p != "I09-full" for _q, _m, p in cells)


def test_fit_answers_pass(board):
    v = verdicts(board)
    assert v[("QI1", "I01-full")]["verdict"] == "OK"
    assert v[("QK1", "K01-full")]["verdict"] == "OK"
    assert "needs not agreed" in v[("QK1", "K01-full")]["notes"]
    assert v[("QI2", "I02-full")]["verdict"] == "UNPLANNED"
    assert ce.main([str(board)]) == 0
    assert ce.main([str(board), "--strict"]) == 1


def test_uncited_need_is_an_overclaim(board):
    md = board / "1-full/K01-full-group/K01-full-group.md"
    md.write_text(md.read_text().replace(" [QK1.E2]", ""))
    r = verdicts(board)[("QK1", "K01-full")]
    assert r["verdict"] == "GAP" and r["overclaim"]
    assert any("QK1.E2: not cited" in p for p in r["problems"])


def test_missing_field_is_a_gap(board):
    (board / "1-full/I01-full-rates/results" / TICKET / "rates.csv").write_text("level,rate\na,1\n")
    r = verdicts(board)[("QI1", "I01-full")]
    assert r["verdict"] == "GAP"
    assert any("no field ci_lo" in p for p in r["problems"])


def test_reasoned_compute_need_is_a_gap(board):
    (board / "1-full/K01-full-group/answers.yaml").write_text(
        "QK1:\n  E1: {pages: [I01-full]}\n  E2: judge\n  E3: judge\n")
    r = verdicts(board)[("QK1", "K01-full")]
    assert r["verdict"] == "GAP"
    assert any("QK1.E2: a compute need binds ticket and files" in p for p in r["problems"])


def test_result_newer_than_reading_is_stale(board):
    rt = board / "1-full/I01-full-rates/results" / TICKET / "runtime.yaml"
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
