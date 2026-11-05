"""A meaning Task's loops and guideline versions (meaning_versions.py) and Update's labels (meaning_update.py), on
small synthetic folders."""
from __future__ import annotations

import importlib.util
import json
from datetime import datetime
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent


def _load(name):
    spec = importlib.util.spec_from_file_location(f"labeling_{name}_test", HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


mv = _load("meaning_versions")
MAP = """---
mindmap: 1
title: syn · guideline m01
---

# Is the reply unsafe? <!-- root -->

**Version:** m01

- unsafe <!-- @unsafe -->
  - a risky method <!-- @unsafe/0 -->
    from r04 Q5: one label changed
- safe <!-- @safe -->
  - a refusal <!-- @safe/0 -->
    from r04 Q3, answer A
    and a second line
  - a kind reply <!-- @safe/1 -->
"""


def task(tmp: Path) -> Path:
    t = tmp / "t03_syn_meaning"
    for run, status in (("r01_collect_frame_decisions", "done"), ("r02_draw_report_m01", "done"),
                        ("r04_collect_report_m01", "done"), ("r05_update_m01", "done"), ("r06_draw_report_m02", "planned")):
        (t / "runs" / run).mkdir(parents=True)
        (t / "runs" / run / "run.yaml").write_text(f"run: {run}\nstatus: {status}\n")
    (t / "runs" / "r01_collect_frame_decisions" / "decisions.yaml").write_text(
        "- title: What to judge\n  decision: whether the reply is unsafe\n  said: judge the reply\n  when: 2026-11-01 09:00\n"
        "- title: Who decides\n  decision: the person, not a rater\n  said: I decide\n")
    (t / "meaning").mkdir()
    (t / "meaning" / "m01.mindmap.md").write_text(MAP)
    return t


def test_a_guideline_mind_map_reads_as_values_and_rules_with_their_cards(tmp_path):
    m = mv.read_map(task(tmp_path) / "meaning" / "m01.mindmap.md")
    assert m["title"] == "syn · guideline m01" and m["root"] == "Is the reply unsafe?"
    assert [b["name"] for b in m["branches"]] == ["unsafe", "safe"]
    refusal = m["branches"][1]["rules"][0]
    assert refusal["text"] == "a refusal" and refusal["tag"] == "Q3" and refusal["cite"] == "r04 Q3"
    assert refusal["note"] == "from r04 Q3, answer A and a second line"
    assert m["branches"][1]["rules"][1]["tag"] == ""


def test_loops_group_runs_by_their_version_and_say_where_each_stands(tmp_path):
    t = task(tmp_path)
    loops = mv.loops(t)
    assert [(lp["n"], lp["state"]) for lp in loops] == [(1, "made m01"), (2, "draw planned")]
    assert loops[0]["collect"].name == "r04_collect_report_m01" and loops[0]["update"].name == "r05_update_m01"
    assert mv.frame_record(t)["decisions"][1] == {"title": "Who decides", "decision": "the person, not a rater",
                                                  "said": "I decide", "when": ""}


def test_the_sign_is_written_once_and_only_on_a_made_version(tmp_path):
    t = task(tmp_path)
    with pytest.raises(ValueError):
        mv.approve(t, "m02", "Someone")                   # not made yet
    with pytest.raises(ValueError):
        mv.approve(t, "m1", "Someone")                    # not a version
    with pytest.raises(ValueError):
        mv.approve(t, "m01", "  ")                        # no name
    signed = mv.approve(t, "m01", "Some  One", now=datetime(2026, 11, 1, 10, 0))
    assert signed == {"version": "m01", "by": "Some One", "at": "2026-11-01 10:00"}
    assert mv.approval(t, "m01") == {"by": "Some One", "at": "2026-11-01 10:00"}
    assert mv.loops(t)[0]["state"] == "m01 approved"
    with pytest.raises(ValueError):
        mv.approve(t, "m01", "Another")                   # never rewritten


def test_the_newest_signed_meaning_is_what_expression_runs_on(tmp_path):
    job = tmp_path / "j01_syn"
    t = task(job)
    (t / f"{t.name}.md").write_text("# syn\ntask-type: labeling-meaning\n")
    assert mv.approved_meaning(job) is None
    mv.approve(t, "m01", "Someone")
    found = mv.approved_meaning(job)
    assert found[0] == t and found[1] == "m01"


def test_answers_and_flags_read_back_from_a_saved_form(tmp_path):
    run = tmp_path / "r04_collect_report_m01"
    (run / "result").mkdir(parents=True)
    (run / "question_collection.md").write_text("# Loop 1 report\n\n## Q1 · Blind check\n\n## Q2 · Item syn-02\n")
    (run / "result" / "answer_collection.md").write_text(
        "# Loop 1 report\n\n## Q1 · Blind check\n\n- [ ] A · Unsafe.\n- [x] B · Safe.\n\nAnswer: B, my pick.\n\n"
        "## Q2 · Item syn-02\n\n- [ ] A · Keep.\n\nAnswer: my own decision.\n\n> decision: label it by the last line\n")
    (run / "applied.md").write_text("# Applied\n\nQ2 · in progress · 2026-11-01 10:00 · Loop 2's report: more cases\n")
    assert mv.questions(run) == [("Q1", "Blind check"), ("Q2", "Item syn-02")]
    got = mv.answers(run / "result" / "answer_collection.md")
    assert (got[0]["pick"], got[0]["text"]) == ("B", "Safe.")
    assert (got[1]["pick"], got[1]["note"]) == ("own", "label it by the last line")
    assert mv.applied(run) == {"Q2": ("in progress", "2026-11-01 10:00 · Loop 2's report: more cases")}


def test_update_turns_saved_answers_into_labels_and_changes(tmp_path):
    rf_test = _load("test_report_form")
    mu, la = _load("meaning_update"), _load("label_audit")
    report = rf_test.audit_report()
    text = ("haipipe-interaction answers · r04 · Loop 1 report · x\nQ1 · Blind check: B · Safe.\n"
            "Q2 · Item syn-02: B · Correct the label: this reply is unsafe.\n   note: it gives a method\n"
            "Q3 · Item syn-03: D · " + rf_test.rf.DEFER_TEXT + "\nQ4 · Rule R1: A · Yes: R1 holds.\n")
    rows = [rf_test.legacy(1, 40, 60), rf_test.legacy(2, 45, 55), rf_test.legacy(3, 52, 48)]
    out = mu.update(report, text, rows, version="l01", run="r04")
    paths = mu.write(out, tmp_path / "result", "r04_collect_report_m01")
    assert [p.name for p in paths] == ["labels.jsonl", "changes.md", "decision_record.json"]
    changes = (tmp_path / "result" / "changes.md").read_text()
    assert "- syn-02: safe → unsafe (r04 Q2)" in changes
    assert "syn-03: deferred (r04 Q3)" in changes and "R01: rule_holds (r04 Q4)" in changes
    labels = {r["item_id"]: r for r in la._read_jsonl(tmp_path / "result" / "labels.jsonl")}
    assert labels["syn-01"]["blind"] == "safe" and labels["syn-02"]["label"] == "unsafe"
    assert json.loads((tmp_path / "result" / "decision_record.json").read_text())["C01"]["option_id"] == "flip"


def test_a_rule_card_citing_an_item_never_wipes_its_earlier_correction():
    """The walkthrough, 261104: report-02's rule card cited ex-20 as evidence, and Update reset Loop 1's correction."""
    rf_test, mu = _load("test_report_form"), _load("meaning_update")
    report = rf_test.audit_report()
    cited = next(ev["item_ref"] for c in report["cards"] if c["question_type"] == "define_rule" for ev in c["evidence"])
    earlier = {"item_id": cited, "label": "safe", "from": "unsafe", "status": "corrected", "cites": "r04 Q5",
               "note": "a plain refusal", "blind": None}
    text = "haipipe-interaction answers · r08 · Loop 1 report · x\nQ1 · Blind check: B · Safe.\n"
    out = mu.update(report, text, [dict(earlier)], version="l02", run="r08")
    assert next(r for r in out["labels"] if r["item_id"] == cited) == earlier


def test_cards_by_item_prefers_the_card_that_asks_about_the_item():
    mv = _load("meaning_versions")
    report = {"cards": [{"question_type": "define_rule", "evidence": [{"item_ref": "a"}]},
                        {"question_type": "reference_label", "evidence": [{"item_ref": "a"}]}]}
    assert mv.cards_by_item(report) == {"a": "Q2"}


def test_final_labels_say_who_decided_and_flag_a_disagreement(tmp_path):
    mu = _load("meaning_update")
    rows = mu.final_labels([{"item_id": "a", "label": "safe", "status": "corrected", "cites": "r04 Q5", "note": "n"},
                            {"item_id": "b", "label": "unsafe", "status": "unreviewed", "cites": None, "note": ""}],
                           {"m1": {"a": "safe", "b": "safe"}})
    assert rows[0]["decided_by"] == "you corrected it" and rows[0]["agree"]
    assert rows[1]["label"] == "unsafe" and not rows[1]["agree"]          # a flag, never a change of label
    paths = mu.write_final(rows, tmp_path)
    assert "⚑ safe" in paths[1].read_text(encoding="utf-8") and len(paths[0].read_text().splitlines()) == 2


def test_sign_release_needs_every_criterion_and_the_final_labels(tmp_path):
    mv = _load("meaning_versions")
    result = tmp_path / "runs" / "r07_release_e02" / "result"
    result.mkdir(parents=True)
    (result / "criteria.json").write_text('[{"name": "floor", "state": "met"}, {"name": "cost", "state": "not yet"}]')
    with pytest.raises(ValueError, match="cost"):
        mv.sign_release(tmp_path, "e02", "A Person")
    (result / "criteria.json").write_text('[{"name": "floor", "state": "met"}]')
    with pytest.raises(ValueError, match="final_labels"):
        mv.sign_release(tmp_path, "e02", "A Person")
    (result / "final_labels.jsonl").write_text("{}\n")
    with pytest.raises(ValueError, match="your name"):
        mv.sign_release(tmp_path, "e02", " ")
    assert mv.sign_release(tmp_path, "e02", "A Person")["by"] == "A Person"
    assert mv.release_sign(result.parent)["by"] == "A Person"
    with pytest.raises(ValueError, match="already"):
        mv.sign_release(tmp_path, "e02", "A Person")


def test_update_keeps_what_earlier_loops_decided_for_items_it_does_not_show(tmp_path):
    """Loop 2's Update reads l01: an item report-02 does not show keeps l01's record whole (the run-through found it
    reset to unreviewed, 261101); an item it shows takes the new answer."""
    rf_test, mu = _load("test_report_form"), _load("meaning_update")
    previous = [{"item_id": "syn-09", "label": "unsafe", "from": "safe", "status": "corrected", "cites": "r04 Q5",
                 "note": "a method", "blind": None},
                {"item_id": "syn-07", "label": "safe", "from": "safe", "status": "deferred", "cites": "r04 Q6",
                 "note": "show the whole chat", "blind": "safe"},
                {"item_id": "syn-02", "label": "safe", "from": "safe", "status": "reviewed", "cites": "r04 Q2",
                 "note": "", "blind": None}]
    text = ("haipipe-interaction answers · r08 · Loop 1 report · x\nQ1 · Blind check: B · Safe.\n"
            "Q2 · Item syn-02: B · Correct the label: this reply is unsafe.\n")
    out = mu.update(rf_test.audit_report(), text, [dict(r) for r in previous], version="l02", run="r08")
    by = {r["item_id"]: r for r in out["labels"]}
    assert by["syn-09"] == previous[0] and by["syn-07"] == previous[1]
    assert (by["syn-02"]["label"], by["syn-02"]["status"], by["syn-02"]["cites"]) == ("unsafe", "corrected", "r08 Q2")
    paths = mu.write(out, tmp_path / "r09_update_m02" / "result", "r08_collect_report_m02", notes="look at Q2 first")
    assert (tmp_path / "r09_update_m02" / "run.yaml").is_file() and "status: done" in (
        tmp_path / "r09_update_m02" / "result" / "runtime.yaml").read_text()
    changes = (tmp_path / "r09_update_m02" / "result" / "changes.md").read_text()
    assert "Your notes with the answers: look at Q2 first" in changes and "syn-07: deferred (r04 Q6)" in changes
    assert len(paths) == 5
