from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import pytest


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("labeling_meaning_contracts_test", HERE / "meaning_contracts.py")
assert SPEC and SPEC.loader
mc = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mc)

DEMO = HERE / "fixtures" / "decision_report_demo.json"


def demo() -> dict:
    return json.loads(DEMO.read_text(encoding="utf-8"))


def card(report: dict, index: int = 0) -> dict:
    return report["cards"][index]


def audit_card(question_type: str = "inconsistency") -> dict:
    """The demo report with card D01 turned into an audit card that cites one Test case."""
    report = demo()
    first = card(report)
    first["question_type"] = question_type
    first["origin"] = {"round_report_ref": "round-03", "partition": "test"}
    first["evidence"].append({"item_ref": "T17", "split": "test", "role": "context", "context": "", "text": "",
                              "signal": "Executors agree against the reference label"})
    return report


# ── the fixture ──────────────────────────────────────────────────────────────


def test_the_demo_fixture_is_a_valid_report_in_normalized_form() -> None:
    report = demo()
    assert mc.validate_report(report) == report
    assert (report["job_id"], report["report_id"], report["round_id"]) == ("demo_job", "report-01", "round-01")
    assert report["base"] == {"task_frame_version": "f01", "meaning_version": "m01", "reference_version": "l01",
                              "split_version": "s01"}
    assert report["synthetic"] is True
    assert [c["decision_id"] for c in report["cards"]] == ["D01", "D02", "D03", "D04", "D05", "D06"]
    assert {row["split"] for c in report["cards"] for row in c["evidence"]} == {"train"}
    assert all(set(option) == set(mc.OPTION_FIELDS) for c in report["cards"] for option in c["options"])
    assert "sha256" not in DEMO.read_text(encoding="utf-8") and "checksum" not in DEMO.read_text(encoding="utf-8")


def test_validation_is_deterministic_and_leaves_its_input_unchanged() -> None:
    report = demo()
    before = copy.deepcopy(report)
    first = mc.validate_report(report)
    assert mc.validate_report(first) == first
    assert report == before
    assert first is not report and first["cards"][0] is not report["cards"][0]


def test_a_card_without_origin_is_normalized_with_origin_none() -> None:
    report = demo()
    del card(report)["origin"]
    assert mc.validate_report(report)["cards"][0]["origin"] is None


# ── report and card rejections ───────────────────────────────────────────────


def _set(path: tuple, value):
    def mutate(report: dict) -> None:
        target = report
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
    return mutate


def _delete(path: tuple):
    def mutate(report: dict) -> None:
        target = report
        for key in path[:-1]:
            target = target[key]
        del target[path[-1]]
    return mutate


def _duplicate_card(report: dict) -> None:
    report["cards"].append(copy.deepcopy(card(report)))


def _duplicate_source(report: dict) -> None:
    report["sources"].append(dict(report["sources"][0]))


def _duplicate_option(report: dict) -> None:
    card(report)["options"][1]["option_id"] = card(report)["options"][0]["option_id"]


def _duplicate_item(report: dict) -> None:
    card(report)["evidence"][1]["item_ref"] = card(report)["evidence"][0]["item_ref"]


def _test_case_on(question_type: str):
    def mutate(report: dict) -> None:
        fresh = audit_card()
        card(fresh)["question_type"] = question_type
        report.clear()
        report.update(fresh)
    return mutate


def _test_case_without_origin(report: dict) -> None:
    fresh = audit_card()
    card(fresh)["origin"] = None
    report.clear()
    report.update(fresh)


def _test_case_with(field: str, value: str):
    def mutate(report: dict) -> None:
        fresh = audit_card()
        card(fresh)["evidence"][-1][field] = value
        report.clear()
        report.update(fresh)
    return mutate


def _test_item_source_on_a_boundary_card(report: dict) -> None:
    report["sources"].append({"source_id": "S09", "kind": "test_item", "label": "Test case named by round-03"})
    card(report)["source_ids"].append("S09")


REJECTIONS = [
    ("nearly empty report", lambda r: r.clear() or r.update({"cards": []}), "missing field 'schema'"),
    ("unknown report field", _set(("approved",), True), "unknown field 'approved'"),
    ("status smuggled in", _set(("publication_status",), "published"), "unknown field"),
    ("missing purpose", _delete(("purpose",)), "missing field 'purpose'"),
    ("wrong schema", _set(("schema",), "labeling.round_report"), "report.schema"),
    ("newer schema_version", _set(("schema_version",), 2), "unsupported schema_version"),
    ("bool schema_version", _set(("schema_version",), True), "unsupported schema_version"),
    ("unsafe job_id", _set(("job_id",), "../demo_job"), "job_id must match"),
    ("unsafe report_id", _set(("report_id",), "reports/report-01"), "report_id must match"),
    ("empty round_id", _set(("round_id",), ""), "round_id must match"),
    ("revision zero", _set(("report_revision",), 0), "report_revision"),
    ("revision text", _set(("report_revision",), "1"), "report_revision"),
    ("revision bool", _set(("report_revision",), True), "report_revision"),
    ("blank title", _set(("title",), "   "), "report.title: must not be empty"),
    ("overlong purpose", _set(("purpose",), "x" * (mc.MAX_TEXT + 1)), "longer than"),
    ("base missing split", _delete(("base", "split_version")), "missing field 'split_version'"),
    ("base unknown key", _set(("base", "confidence"), "high"), "unknown field 'confidence'"),
    ("base unsafe version", _set(("base", "meaning_version"), "m 01"), "base.meaning_version"),
    ("no sources", _set(("sources",), []), "sources: needs at least 1 entry"),
    ("duplicate source", _duplicate_source, "duplicate source_id 'S01'"),
    ("old learning kind", _set(("sources", 2, "kind"), "learning_item"), "sources[2].kind"),
    ("source unknown key", _set(("sources", 0, "text"), "copied"), "unknown field 'text'"),
    ("no cards", _set(("cards",), []), "cards: needs at least 1 entry"),
    ("too many cards", lambda r: r.update(cards=[card(r)] * (mc.MAX_ENTRIES + 1)), "more than"),
    ("duplicate decision", _duplicate_card, "duplicate decision_id 'D01'"),
    ("no timezone", _set(("published_at",), "2026-11-01T10:00:00"), "needs a timezone"),
    ("not a timestamp", _set(("published_at",), "yesterday"), "ISO 8601"),
    ("unsafe publisher", _set(("publication_actor",), "JL Luo"), "publication_actor must match"),
    ("synthetic text", _set(("synthetic",), "yes"), "report.synthetic"),
    ("card not an object", _set(("cards", 0), "D01"), "cards[0]: must be an object"),
    ("card unknown key", _set(("cards", 0, "recommended_option"), "A"), "unknown field 'recommended_option'"),
    ("card missing why_now", _delete(("cards", 0, "why_now")), "missing field 'why_now'"),
    ("unsafe decision_id", _set(("cards", 0, "decision_id"), "D01/../x"), "decision_id must match"),
    ("label-error type name", _set(("cards", 0, "question_type"), "label_error"), "question_type"),
    ("prototype scope word", _set(("cards", 0, "approval_scope"), "rule_preference_only"), "approval_scope"),
    ("flag as text", _set(("cards", 0, "none_allowed"), "true"), "none_allowed: must be true or false"),
    ("blank question", _set(("cards", 0, "question"), ""), "question: must not be empty"),
    ("no source_ids", _set(("cards", 0, "source_ids"), []), "source_ids: needs at least 1 entry"),
    ("missing source", _set(("cards", 0, "source_ids"), ["S01", "S99"]), "'S99' is not one of the report"),
    ("repeated source", _set(("cards", 0, "source_ids"), ["S01", "S01"]), "duplicate source_id 'S01'"),
    ("unsafe source ref", _set(("cards", 0, "source_ids"), ["../S01"]), "source_ids[0] must match"),
    ("no options", _set(("cards", 0, "options"), []), "options: needs at least 1 entry"),
    ("preselected option", _set(("cards", 0, "options", 0, "selected"), True), "never preselected"),
    ("default option", _set(("cards", 0, "options", 1, "default"), True), "never preselected"),
    ("preselected key", _set(("cards", 0, "options", 1, "preselected"), False), "never preselected"),
    ("duplicate option", _duplicate_option, "duplicate option_id 'A'"),
    ("option without effect", _delete(("cards", 0, "options", 0, "effect")), "missing field 'effect'"),
    ("option unknown key", _set(("cards", 0, "options", 0, "patch"), "x"), "unknown field 'patch'"),
    ("unsafe option_id", _set(("cards", 0, "options", 0, "option_id"), "A/B"), "option_id must match"),
    ("blank option label", _set(("cards", 0, "options", 0, "label"), " "), "label: must not be empty"),
    ("learning split", _set(("cards", 0, "evidence", 0, "split"), "learning"), "split: must be one of train"),
    ("validation split", _set(("cards", 0, "evidence", 0, "split"), "validation"), "split: must be one of"),
    ("confirmation split", _set(("cards", 0, "evidence", 0, "split"), "confirmation"), "confirmation set never"),
    ("unknown role", _set(("cards", 0, "evidence", 0, "role"), "case_c"), "role"),
    ("train without text", _set(("cards", 0, "evidence", 0, "text"), "  "), "exact excerpt"),
    ("evidence label smuggled", _set(("cards", 0, "evidence", 0, "label"), "high"), "unknown field 'label'"),
    ("evidence missing signal", _delete(("cards", 0, "evidence", 0, "signal")), "missing field 'signal'"),
    ("unsafe item_ref", _set(("cards", 0, "evidence", 0, "item_ref"), "../L01"), "item_ref must match"),
    ("duplicate item", _duplicate_item, "duplicate item_ref 'L01'"),
    ("Test case on a boundary card", _test_case_on("boundary"), "only on an audit card"),
    ("Test case on a diagnostic card", _test_case_on("diagnostic"), "only on an audit card"),
    ("Test case without origin", _test_case_without_origin, "names its audit issue in origin"),
    ("Test text copied", _test_case_with("text", "the Test reply, copied"), "custody reference"),
    ("Test context copied", _test_case_with("context", "the Test context"), "custody reference"),
    ("Test item source off an audit card", _test_item_source_on_a_boundary_card, "only on an audit card"),
    ("origin confirmation", _set(("cards", 0, "origin"), {"round_report_ref": "round-03",
                                                        "partition": "confirmation"}), "confirmation set never"),
    ("origin unknown key", _set(("cards", 0, "origin"), {"round_report_ref": "round-03", "partition": "test",
                                                       "issue": "x"}), "unknown field 'issue'"),
    ("origin unsafe ref", _set(("cards", 0, "origin"), {"round_report_ref": "../round-03",
                                                      "partition": "train"}), "round_report_ref must match"),
]


@pytest.mark.parametrize(("name", "mutate", "message"), REJECTIONS, ids=[row[0] for row in REJECTIONS])
def test_validate_report_refuses(name: str, mutate, message: str) -> None:
    report = demo()
    mutate(report)
    with pytest.raises(mc.ValidationError, match=message.replace("(", r"\(").replace("[", r"\[")):
        mc.validate_report(report)


@pytest.mark.parametrize("value", [None, [], "report", 7])
def test_validate_report_refuses_a_non_object(value) -> None:
    with pytest.raises(mc.ValidationError, match="report: must be an object"):
        mc.validate_report(value)


@pytest.mark.parametrize("question_type", mc.AUDIT_QUESTION_TYPES)
def test_an_audit_card_cites_a_test_case_by_custody_reference(question_type: str) -> None:
    report = audit_card(question_type)
    normalized = mc.validate_report(report)
    test_row = normalized["cards"][0]["evidence"][-1]
    assert test_row == {"item_ref": "T17", "split": "test", "role": "context", "context": "", "text": "",
                        "signal": "Executors agree against the reference label"}
    assert normalized["cards"][0]["origin"] == {"round_report_ref": "round-03", "partition": "test"}


def test_a_train_origin_and_empty_evidence_are_allowed() -> None:
    report = demo()
    card(report)["origin"] = {"round_report_ref": "round-02", "partition": "train"}
    card(report, 5)["evidence"] = []
    normalized = mc.validate_report(report)
    assert normalized["cards"][0]["origin"]["partition"] == "train"
    assert normalized["cards"][5]["evidence"] == []


def test_the_error_classes_share_one_base() -> None:
    for error in (mc.ValidationError, mc.StaleRevision, mc.DuplicateRequest):
        assert issubclass(error, mc.MeaningError)
    assert not issubclass(mc.StaleRevision, mc.ValidationError)


# ── identifiers ──────────────────────────────────────────────────────────────


@pytest.mark.parametrize("value", ["a", "A1", "report-01", "sub_000001", "x" * 64])
def test_safe_identifiers_pass(value: str) -> None:
    assert mc.validate_identifier(value, "id") == value and mc.is_identifier(value)


@pytest.mark.parametrize("value", ["", "-a", "_a", ".a", "..", "../a", "a/b", "a\\b", "a b", "a.b", "x" * 65,
                                   "a\n", "%2e%2e", "café", "a\x00", 7, None])
def test_unsafe_identifiers_are_refused(value) -> None:
    assert not mc.is_identifier(value)
    with pytest.raises(mc.ValidationError, match="id must match"):
        mc.validate_identifier(value, "id")


# ── answers ──────────────────────────────────────────────────────────────────


def test_answers_cover_every_card_in_order_and_keep_each_kind() -> None:
    report = demo()
    answers = {
        "D02": {"kind": "reject_options", "comment": "none of these fit"},
        "D01": {"kind": "chosen", "option_id": "B"},
        "D03": {"kind": "custom", "text": "Ask for context, then decide."},
        "D04": {"kind": "defer"},
        "D05": {"kind": "unanswered"},
        "D06": None,
    }
    before = copy.deepcopy(answers)
    normalized = mc.validate_answers(report, answers)
    assert list(normalized) == ["D01", "D02", "D03", "D04", "D05", "D06"]
    assert normalized["D01"] == {"kind": "chosen", "option_id": "B", "text": None, "comment": ""}
    assert normalized["D02"] == {"kind": "reject_options", "option_id": None, "text": None,
                                 "comment": "none of these fit"}
    assert normalized["D03"] == {"kind": "custom", "option_id": None, "text": "Ask for context, then decide.",
                                 "comment": ""}
    assert normalized["D04"]["kind"] == "defer" and normalized["D05"]["kind"] == "unanswered"
    assert normalized["D06"] == {"kind": "unanswered", "option_id": None, "text": None, "comment": ""}
    assert answers == before
    assert mc.validate_answers(report, {}) == {d: normalized["D06"] for d in normalized}


def test_comments_and_custom_text_are_kept_exactly_as_written() -> None:
    comment = "  only for adults \n\t(and not in chats)  "
    custom = "\n  Count practical help\tonly when it is relevant.  "
    normalized = mc.validate_answers(demo(), {"D01": {"kind": "chosen", "option_id": "A", "comment": comment},
                                              "D02": {"kind": "custom", "text": custom, "comment": " "}})
    assert normalized["D01"]["comment"] == comment
    assert normalized["D02"]["text"] == custom and normalized["D02"]["comment"] == " "


def _no(field: str):
    def change(report: dict) -> None:
        card(report)[field] = False
    return change


ANSWER_REJECTIONS = [
    ("not an object", None, ["D01"], "answers must be an object"),
    ("unknown decision", None, {"D99": {"kind": "defer"}}, "unknown decision_id 'D99'"),
    ("answer not an object", None, {"D01": "A"}, "answer to D01: must be an object"),
    ("missing kind", None, {"D01": {"option_id": "A"}}, "missing field 'kind'"),
    ("unknown kind", None, {"D01": {"kind": "approve"}}, "kind: must be one of"),
    ("unknown answer key", None, {"D01": {"kind": "chosen", "option_id": "A", "selected_option_id": "A"}},
     "unknown field 'selected_option_id'"),
    ("chosen without option", None, {"D01": {"kind": "chosen"}}, "names one option of this card"),
    ("chosen foreign option", None, {"D01": {"kind": "chosen", "option_id": "Z"}}, "names one option"),
    ("option on defer", None, {"D01": {"kind": "defer", "option_id": "A"}}, "only for a chosen answer"),
    ("option on reject", None, {"D01": {"kind": "reject_options", "option_id": "A"}}, "only for a chosen"),
    ("custom without text", None, {"D01": {"kind": "custom"}}, "needs the person's own text"),
    ("custom blank text", None, {"D01": {"kind": "custom", "text": "  \n"}}, "needs the person's own text"),
    ("text on chosen", None, {"D01": {"kind": "chosen", "option_id": "A", "text": "also this"}},
     "text is only for a custom answer"),
    ("defer not allowed", _no("defer_allowed"), {"D01": {"kind": "defer"}}, "does not allow defer"),
    ("reject not allowed", _no("none_allowed"), {"D01": {"kind": "reject_options"}}, "none_allowed is false"),
    ("comment not allowed", _no("comments_allowed"), {"D01": {"kind": "defer", "comment": "x"}},
     "does not take comments"),
    ("comment not text", None, {"D01": {"kind": "defer", "comment": 5}}, "comment: must be text"),
    ("overlong comment", None, {"D01": {"kind": "defer", "comment": "x" * (mc.MAX_TEXT + 1)}}, "longer than"),
]


@pytest.mark.parametrize(("name", "change", "answers", "message"), ANSWER_REJECTIONS,
                         ids=[row[0] for row in ANSWER_REJECTIONS])
def test_validate_answers_refuses(name: str, change, answers, message: str) -> None:
    report = demo()
    if change:
        change(report)
    with pytest.raises(mc.ValidationError, match=message):
        mc.validate_answers(report, answers)


def test_an_empty_comment_is_allowed_where_comments_are_not() -> None:
    report = demo()
    card(report)["comments_allowed"] = False
    assert mc.validate_answers(report, {"D01": {"kind": "defer", "comment": ""}})["D01"]["comment"] == ""


def test_validate_answers_checks_the_report_too() -> None:
    report = demo()
    report["cards"][0]["options"][0]["selected"] = True
    with pytest.raises(mc.ValidationError, match="never preselected"):
        mc.validate_answers(report, {})
