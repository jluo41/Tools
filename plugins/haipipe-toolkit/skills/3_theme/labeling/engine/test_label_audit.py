from __future__ import annotations

import importlib.util
import json
import random
from pathlib import Path

import pytest


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("labeling_label_audit_test", HERE / "label_audit.py")
assert SPEC and SPEC.loader
la = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(la)


def raters(n_items=30, per_item=50, seed=7):
    """Synthetic per-rater rows: half the raters women, half men; an item-level expert field rides along on every
    row, the way an expert key would if a raw file were read whole."""
    rng = random.Random(seed)
    rows = []
    for i in range(n_items):
        item_id = f"syn-{i:02d}"
        for r in range(per_item):
            woman = r % 2 == 0
            if i < 10:
                p_yes, p_unsure = 0.9, 0.0          # clearly unsafe
            elif i < 20:
                p_yes, p_unsure = 0.1, 0.0          # clearly safe
            elif i < 25:
                p_yes, p_unsure = 0.5, 0.0          # split
            elif i < 28:
                p_yes, p_unsure = (0.95 if woman else 0.05), 0.0   # a gender gap
            else:
                p_yes, p_unsure = 0.2, 0.3          # many Unsure
            u = rng.random()
            answer = "Unsure" if u < p_unsure else ("Yes" if rng.random() < p_yes else "No")
            rows.append({"item_id": item_id, "rater_id": f"r{r}", "rater_gender": "Woman" if woman else "Man",
                         "rater_age": ["gen z", "millenial", "gen x"][r % 3], "Q_overall": answer,
                         "expert_label": f"GOLD-{'Yes' if i % 2 else 'No'}"})
    return rows


def legacy(rows=None):
    votes = la.legacy_votes(rows or raters(), groups=["rater_gender", "rater_age"])
    return [la.legacy_row(item_id, votes[item_id]) for item_id in sorted(votes)]


def test_majority_and_ties():
    assert la.majority({"Yes": 3, "No": 1, "Unsure": 0}) == "Yes"
    assert la.majority({"Yes": 2, "No": 2, "Unsure": 0}) == "Tie"
    assert la.majority({"Yes": 0, "No": 0, "Unsure": 0}) == "Tie"


def test_fence_an_item_level_field_raises():
    with pytest.raises(la.FenceError):
        la.legacy_votes(raters(), groups=["expert_label"])
    with pytest.raises(la.FenceError):
        la.legacy_votes(raters(), answer="expert_label", values=("GOLD-Yes", "GOLD-No"))


def test_fence_an_unnamed_expert_field_never_reaches_the_output():
    rows = legacy()
    text = json.dumps(rows)
    assert "expert_label" not in text and "GOLD-" not in text


def test_legacy_row_uses_t02_definitions():
    row = la.legacy_row("x", {"n": 10, "counts": {"Yes": 4, "No": 4, "Unsure": 2}, "groups": {}})
    assert row["unsafe_share"] == 0.4 and row["unsure_share"] == 0.2 and row["majority"] == "Tie"
    assert row["label"] is None


def test_signals_flag_split_gap_and_unsure():
    sigs = {s["item_id"]: s for s in (la.signals(r) for r in legacy())}
    assert "split" in sigs["syn-21"]["flags"]
    assert "gap" in sigs["syn-26"]["flags"] and sigs["syn-26"]["gap"]["field"] == "rater_gender"
    assert "unsure" in sigs["syn-29"]["flags"]
    assert not sigs["syn-03"]["flagged"] and sigs["syn-03"]["stratum"] == "unflagged"


def test_small_group_levels_never_make_a_gap():
    row = next(r for r in legacy() if r["item_id"] == "syn-26")
    assert la.signals(row, min_level=26)["gap"] is None      # 25 women and 25 men: both below 26


def test_draw_is_seeded_disjoint_train_only_with_pi():
    sigs = [la.signals(r) for r in legacy()]
    train = [s["item_id"] for s in sigs][:24] + [s["item_id"] for s in sigs][26:]
    one = la.draw(sigs, train, n_hard=5, n_blind=3, n_typical=6, seed=11)
    two = la.draw(sigs, train, n_hard=5, n_blind=3, n_typical=6, seed=11)
    assert one == two
    hard, blind, typical = (set(one["sets"][k]) for k in ("hard", "blind", "typical"))
    assert not (hard & blind or hard & typical or blind & typical)
    assert not (hard | blind | typical) & {"syn-24", "syn-25"}               # Test items are never drawn
    assert len(hard) == 5 and len(blind) == 3 and len(typical) == 6
    assert one["pi"]["blind"] == round(3 / one["unflagged"], 4)
    for stratum, pi in one["pi"]["hard"].items():
        drawn = sum(1 for i in hard if next(s for s in sigs if s["item_id"] == i)["stratum"] == stratum)
        assert pi == round(drawn / one["strata"][stratum], 4)


def test_evidence_row_is_exact_and_blind_hides_the_label():
    row = next(r for r in legacy() if r["item_id"] == "syn-03")
    item = {"item_id": "syn-03", "context_before": "User: is it safe?", "main": "Assistant: exact reply."}
    shown = la.evidence_row(item, row)
    assert shown["text"] == "Assistant: exact reply." and shown["context"] == "User: is it safe?"
    assert "unsafe (majority)" in shown["signal"]
    assert la.evidence_row(item, row, show_label=False)["signal"] == ""
    test = la.evidence_row(item, row, split="test")
    assert test["text"] == "" and test["context"] == "" and test["split"] == "test"


def test_apply_answers_maps_every_answer_kind():
    rows = legacy()
    card = lambda did, qtype, item: {"decision_id": did, "question_type": qtype,                      # noqa: E731
                                     "evidence": [{"item_ref": item, "role": "case_a"}]}
    report = {"cards": [card("b1", "diagnostic", "syn-01"), card("c1", "reference_label", "syn-02"),
                        card("c2", "reference_label", "syn-12"), card("c3", "reference_label", "syn-21"),
                        card("c4", "reference_label", "syn-22"), card("c5", "reference_label", "syn-23"),
                        card("c6", "reference_label", "syn-26"), card("r1", "define_rule", "syn-03")]}
    answers = {"b1": {"kind": "chosen", "option_id": "blind_safe"},
               "c1": {"kind": "chosen", "option_id": "keep"},
               "c2": {"kind": "chosen", "option_id": "flip", "comment": "a refusal with help"},
               "c3": {"kind": "chosen", "option_id": "change_rule"},
               "c4": {"kind": "defer"},
               "c5": {"kind": "custom", "text": "label it by its last sentence"},
               "r1": {"kind": "chosen", "option_id": "rule_change", "comment": "narrow it"}}
    out = la.apply_answers(rows, report, answers, version="l01", run="r04")
    by = {r["item_id"]: r for r in out["labels"]}
    assert by["syn-01"]["blind"] == "safe" and by["syn-01"]["status"] == "unreviewed"
    assert by["syn-02"]["status"] == "reviewed" and by["syn-02"]["label"] == "unsafe"
    assert by["syn-12"]["status"] == "corrected" and by["syn-12"]["label"] == "unsafe" and by["syn-12"]["cites"] == "r04 Q3"
    assert by["syn-21"]["status"] == "pending_rule" and by["syn-22"]["status"] == "deferred"
    assert by["syn-23"]["status"] == "custom" and by["syn-23"]["note"] == "label it by its last sentence"
    assert by["syn-26"]["status"] == "unreviewed"                              # c6 left unanswered
    assert out["changes"] == [{"item_id": "syn-12", "from": "safe", "to": "unsafe", "cites": "r04 Q3"}]
    assert out["rules"]["r1"]["option"] == "rule_change" and out["rules"]["r1"]["cites"] == "r04 Q8"


def test_profile_counts_like_t02():
    prof = la.profile(legacy())
    assert prof["items"] == 30 and sum(prof["majority"].values()) == 30
    assert prof["split_40_60"] >= 5


def test_stratified_split_mirrors_the_vote_spread_and_is_seeded():
    rows = legacy()
    one = la.stratified_split(rows, n_test=10, seed=3)
    assert one == la.stratified_split(rows, n_test=10, seed=3)
    assert one["n_test"] == 10 and one["n_train"] == 20
    assert not set(one["test"]) & set(one["train"]) and len(one["test"]) + len(one["train"]) == 30
    assert sum(s["test"] for s in one["strata"].values()) == 10


def test_clopper_pearson_matches_known_values():
    low, high = la.clopper_pearson(1, 4)
    assert 0.006 <= low <= 0.0064 and 0.805 <= high <= 0.807
    assert la.clopper_pearson(0, 4)[0] == 0.0 and la.clopper_pearson(4, 4)[1] == 1.0


def test_score_against_a_hidden_key_counts_flags_corrections_and_misses():
    rows = legacy()
    sigs = [la.signals(r) for r in rows]
    train = [r["item_id"] for r in rows]
    drawn = la.draw(sigs, train, n_hard=4, n_blind=3, n_typical=0, seed=5)
    expert = {r["item_id"]: ("unsafe" if r["item_id"] < "syn-20" and r["item_id"] < "syn-10" else "safe") for r in rows}
    expert.update({i: "unsafe" for i in drawn["sets"]["hard"]})            # the experts call every hard item unsafe
    labels = [{"item_id": r["item_id"], "label": r["label"], "status": "unreviewed", "blind": None} for r in rows]
    by = {x["item_id"]: x for x in labels}
    for i in drawn["sets"]["hard"]:
        by[i].update(status="corrected" if by[i]["label"] == "safe" else "reviewed", label="unsafe")
    for i in drawn["sets"]["blind"]:
        by[i]["blind"] = "unsafe"
    out = la.score(rows, train, sigs, drawn, labels, expert)
    assert out["raters_baseline"]["items"] == sum(1 for r in rows if r["label"])
    assert out["person"]["answered"] == len(drawn["sets"]["hard"])
    assert out["person"]["paired_agreement"]["reviewed"] == 1.0
    assert out["person"]["away_from_experts"] == 0
    assert out["missed"]["blind_judged"] == 3 and out["missed"]["estimate_ci95"][0] <= out["missed"]["estimate"]
    assert "Missed issues" in la.score_markdown(out)


def test_every_kind_of_flag_gets_a_hard_card():
    take = la._allocate(12, {"gap": 6, "split": 50, "tie": 2, "unsure": 1}, minimum=1)
    assert sum(take.values()) == 12 and all(v >= 1 for v in take.values())
    assert la._allocate(2, {"a": 5, "b": 5, "c": 5}, minimum=1) == la._allocate(2, {"a": 5, "b": 5, "c": 5})


def test_a_tie_is_set_never_flipped():
    tie = la.legacy_row("syn-tie", {"n": 10, "counts": {"Yes": 5, "No": 5, "Unsure": 0}, "groups": {}})
    card = {"decision_id": "c1", "question_type": "reference_label", "evidence": [{"item_ref": "syn-tie", "role": "case_a"}]}
    with pytest.raises(ValueError):
        la.apply_answers([tie], {"cards": [card]}, {"c1": {"kind": "chosen", "option_id": "flip"}})
    out = la.apply_answers([tie], {"cards": [card]}, {"c1": {"kind": "chosen", "option_id": "set_unsafe"}})
    assert out["labels"][0]["label"] == "unsafe" and out["labels"][0]["status"] == "corrected"
    assert out["changes"] == [{"item_id": "syn-tie", "from": None, "to": "unsafe", "cites": "r04 Q1"}]
