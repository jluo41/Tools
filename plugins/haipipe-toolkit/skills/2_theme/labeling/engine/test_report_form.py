from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import pytest


HERE = Path(__file__).resolve().parent


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


rf = _load("labeling_report_form_test", HERE / "report_form.py")
la = _load("labeling_label_audit_form_test", HERE / "label_audit.py")
collect, mc = rf.collect, rf.mc
FOR = "b01.j02.t03-s01:syn @ recovered_guideline"


def item(i):
    return {"item_id": f"syn-{i:02d}", "context_before": f"Person: an earlier turn {i}\nAI: a reply\nPerson: the last turn {i}",
            "main": f"AI: the judged reply number {i}, " + "with more words to wrap " * 6}


def legacy(i, yes, no, unsure=0):
    votes = {"n": yes + no + unsure, "counts": {"Yes": yes, "No": no, "Unsure": unsure}, "groups": {}}
    return la.legacy_row(f"syn-{i:02d}", votes)


def options(*pairs):
    return [{"option_id": oid, "label": label, "effect": label, "scope": "this item"} for oid, label in pairs]


def audit_report():
    """A use-case-2 report: one blind card, two chat cards, one rule card (synthetic text only)."""
    blind = {"decision_id": "B01", "short_title": "Blind check", "question_type": "diagnostic",
             "question": "Is the AI's last reply unsafe?", "why_now": "A random unflagged item, its label hidden.",
             "current_rule": "none yet", "evidence": [la.evidence_row(item(1), legacy(1, 40, 60), show_label=False)],
             "options": options(("blind_unsafe", "Unsafe."), ("blind_safe", "Safe."), ("blind_cant_tell", "Can't tell.")),
             "none_allowed": False, "defer_allowed": False, "comments_allowed": True,
             "approval_scope": "explicit_item_set", "source_ids": ["raters"], "origin": None}
    chat = lambda did, i, yes, no: {                                                           # noqa: E731
        "decision_id": did, "short_title": f"Item syn-{i:02d}", "question_type": "reference_label",
        "question": "What should change for this item?", "why_now": "Flagged: raters split 40 to 60%. Train.",
        "current_rule": "R1: a refusal is safe", "evidence": [la.evidence_row(item(i), legacy(i, yes, no))],
        "options": options(("keep", "Keep the label safe."), ("flip", "Correct the label: this reply is unsafe."),
                           ("change_rule", "Keep the label; rule R1 needs a change.")),
        "none_allowed": False, "defer_allowed": True, "comments_allowed": True,
        "approval_scope": "explicit_item_set", "source_ids": ["raters"], "origin": None}
    rule = {"decision_id": "R01", "short_title": "Rule R1", "question_type": "define_rule",
            "question": "Does rule R1 hold?", "why_now": "Inferred from typical items; two flagged items conflict.",
            "current_rule": "R1: a refusal is safe, even a rude one.",
            "evidence": [la.evidence_row(item(4), legacy(4, 10, 90), role="case_a"),
                         la.evidence_row(item(5), legacy(5, 55, 45), role="case_b")],
            "options": options(("rule_holds", "Yes: R1 holds."), ("rule_change", "R1 needs a change.")),
            "none_allowed": False, "defer_allowed": True, "comments_allowed": True,
            "approval_scope": "exact_rule_patch", "source_ids": ["raters"], "origin": None}
    return {"schema": "labeling.decision_report", "schema_version": 1, "job_id": "j02_syn", "report_id": "report-01",
            "report_revision": 1, "round_id": "loop-1", "title": "Loop 1 report", "purpose": "audit the raters' labels",
            "base": {"task_frame_version": "f01", "meaning_version": "m00", "reference_version": "l00",
                     "split_version": "v01"},
            "sources": [{"source_id": "raters", "kind": "train_item", "label": "the raters' votes"}],
            "cards": [blind, chat("C01", 2, 45, 55), chat("C02", 3, 52, 48), rule],
            "published_at": "2026-11-01T10:00:00+00:00", "publication_actor": "agent", "synthetic": True}


def test_fixture_renders_within_the_form_limits():
    report = json.loads((HERE / "fixtures" / "decision_report_demo.json").read_text())
    text = rf.to_collection(report, title="Demo report form", for_=FOR)
    spec = collect.parse(text)
    assert collect.problems(spec, Path("r04_collect_report_m01")) == []
    assert not any(o.get("pick") for q in spec["questions"] for o in q["options"])


def test_audit_report_renders_blind_chat_and_rule_cards():
    text = rf.to_collection(audit_report(), title="Loop 1 report", for_=FOR, intro="Twelve flagged items.")
    spec = collect.parse(text)
    assert collect.problems(spec, Path("r04_collect_report_m01")) == []
    blind, chat, _chat2, rule = spec["questions"]
    assert [o["text"] for o in chat["options"]][-1] == rf.DEFER_TEXT and len(chat["options"]) == 4
    assert len(blind["options"]) == 3 and "raters" not in blind["show"][0]["sketch"]
    assert "raters" in chat["show"][0]["sketch"] and "before" in chat["show"][0]["sketch"]
    assert "fits" in rule["show"][0]["sketch"] and "conflicts" in rule["show"][0]["sketch"]
    assert all(len(q["show"][0]["sketch"].splitlines()) <= 6 for q in spec["questions"])
    assert "GENERATED" in text


@pytest.mark.parametrize("field, value", [("short_title", "A title of five words"), ("why_now", "word " * 41),
                                          ("question", "Is this a question without its mark")])
def test_a_card_over_a_limit_raises(field, value):
    report = audit_report()
    report["cards"][1][field] = value
    with pytest.raises(rf.FormError):
        rf.to_collection(report, title="Loop 1 report", for_=FOR)


def test_too_many_options_with_defer_raises():
    report = audit_report()
    report["cards"][1]["options"] += options(("other", "Another option."))
    with pytest.raises(rf.FormError):
        rf.to_collection(report, title="Loop 1 report", for_=FOR)


def test_round_trip_through_collect_save(tmp_path):
    report = audit_report()
    page = tmp_path / "t03_syn_meaning"
    page.mkdir()
    run = collect.new(page, "report_m01", "Loop 1 report", for_=FOR)
    (run / collect.QUESTIONS).write_text(rf.to_collection(report, title="Loop 1 report", for_=FOR), encoding="utf-8")
    form = collect.build(run)
    stamp = collect.form_built(form.read_text(encoding="utf-8"))
    spec = collect.parse((run / collect.QUESTIONS).read_text(encoding="utf-8"))
    q = {x["id"]: x for x in spec["questions"]}
    pasted = "\n".join([
        f"haipipe-interaction answers · {run.name} · Loop 1 report · 2026-11-01 10:05",
        f"built: {stamp}",
        f"Q1 · {q['Q1']['title']}: B · {q['Q1']['options'][1]['text']}",
        f"Q2 · {q['Q2']['title']}: my own decision",
        "   note: a refusal that names a hotline is safe",
        f"Q3 · {q['Q3']['title']}: D · {rf.DEFER_TEXT}",
        "   note: show me the whole chat",
        f"Q4 · {q['Q4']['title']}: (no option picked)",
    ]) + "\n"
    collect.save(run, pasted)
    answers = rf.answers_from(report, (run / collect.ANSWERS).read_text(encoding="utf-8"))
    assert answers["B01"] == {"kind": "chosen", "option_id": "blind_safe", "text": None, "comment": ""}
    assert answers["C01"]["kind"] == "custom" and answers["C01"]["text"] == "a refusal that names a hotline is safe"
    assert answers["C02"]["kind"] == "defer" and answers["C02"]["comment"] == "show me the whole chat"
    assert answers["R01"]["kind"] == "unanswered"
    out = la.apply_answers([legacy(1, 40, 60), legacy(2, 45, 55), legacy(3, 52, 48)], mc.validate_report(report),
                           answers, run="r04")
    by = {r["item_id"]: r for r in out["labels"]}
    assert by["syn-01"]["blind"] == "safe" and by["syn-02"]["status"] == "custom" and by["syn-03"]["status"] == "deferred"


def test_a_note_where_comments_are_off_is_refused_not_dropped():
    report = audit_report()
    report["cards"][0]["comments_allowed"] = False
    text = "haipipe-interaction answers · r04 · Loop 1 report · x\nQ1 · Blind check: A · Unsafe.\n   note: hmm\n"
    with pytest.raises(mc.ValidationError):
        rf.answers_from(report, text)
