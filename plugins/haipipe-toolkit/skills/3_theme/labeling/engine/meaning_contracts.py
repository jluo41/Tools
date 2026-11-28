#!/usr/bin/env python3
"""Decision-report records for one labeling job: pure validators, no file writes, no model calls.

A decision report asks the job's human a few rule-level questions at once (s03 implementation-plan
CONTRACTS.md version 2, sections 5 and 6).  This module owns what such a report, and one person's answers to
it, may contain:

    validate_report(report)            a published report, returned normalized, or ValidationError
    validate_answers(report, answers)  answers keyed by decision_id, returned normalized, or ValidationError

meaning_store.py is the only writer of these records.

Partitions are Train and Test only.  A card's evidence cites Train items with their exact excerpt.  It cites
Test cases only on an audit card (question_type ``inconsistency``, or ``reference_label`` for a suspected
label error) whose ``origin`` names the round report that raised it, and then by custody reference alone: the
row's text and context stay empty and resolve at read time.  The fresh confirmation set never appears in a
report.  No option is ever preselected.  A comment is kept exactly as written.

No record carries a content hash: versions are explicit numbers, and equality is exact JSON-value comparison.
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any, NoReturn


REPORT_SCHEMA = "labeling.decision_report"
SCHEMA_VERSION = 1
IDENTIFIER_PATTERN = r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}"
VERSION_PATTERN = r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}"
MAX_TEXT = 20_000    # characters in one text field
MAX_ENTRIES = 500    # entries in one list: sources, cards, evidence rows, options

QUESTION_TYPES = (
    "define_rule",
    "boundary",
    "exception",
    "precedence",
    "inconsistency",
    "reference_label",
    "diagnostic",
    "acceptance_policy",
)
AUDIT_QUESTION_TYPES = ("inconsistency", "reference_label")  # the only cards that may cite Test cases
APPROVAL_SCOPES = (
    "exact_rule_patch",
    "preference_only",
    "diagnostic_definition",
    "explicit_item_set",
    "explicit_audit_policy",
)
PARTITIONS = ("train", "test")
EVIDENCE_ROLES = ("case_a", "case_b", "context")
SOURCE_KINDS = (
    "human_idea",
    "human_comment",
    "chat_excerpt",
    "prior_decision",
    "train_item",
    "test_item",
    "supplied_document",
)
ANSWER_KINDS = ("chosen", "reject_options", "custom", "defer", "unanswered")
DISPOSITIONS = {
    "chosen": "chosen",
    "reject_options": "rejected_options",
    "custom": "custom_proposal",
    "defer": "deferred",
    "unanswered": "unanswered",
}
PRESELECTION_KEYS = ("selected", "default", "preselected")

REPORT_FIELDS = (
    "schema",
    "schema_version",
    "job_id",
    "report_id",
    "report_revision",
    "round_id",
    "title",
    "purpose",
    "base",
    "sources",
    "cards",
    "published_at",
    "publication_actor",
    "synthetic",
)
BASE_FIELDS = ("task_frame_version", "meaning_version", "reference_version", "split_version")
SOURCE_FIELDS = ("source_id", "kind", "label")
CARD_FIELDS = (
    "decision_id",
    "short_title",
    "question_type",
    "question",
    "why_now",
    "current_rule",
    "evidence",
    "options",
    "none_allowed",
    "defer_allowed",
    "comments_allowed",
    "approval_scope",
    "source_ids",
    "origin",
)
CARD_REQUIRED = tuple(field for field in CARD_FIELDS if field != "origin")
EVIDENCE_FIELDS = ("item_ref", "split", "role", "context", "text", "signal")
OPTION_FIELDS = ("option_id", "label", "effect", "scope")
ORIGIN_FIELDS = ("round_report_ref", "partition")
ANSWER_FIELDS = ("kind", "option_id", "text", "comment")

_IDENTIFIER = re.compile(IDENTIFIER_PATTERN)
_VERSION = re.compile(VERSION_PATTERN)


class MeaningError(Exception):
    """A decision-report record is missing, unreadable or refused; the message names why."""


class ValidationError(MeaningError):
    """A record or a request breaks the contract: a field, a choice or an identifier."""


class StaleRevision(MeaningError):
    """A write named a revision that is no longer current: a published report or a draft."""


class DuplicateRequest(MeaningError):
    """A request_id already committed a different submission."""


# ── small checks ─────────────────────────────────────────────────────────────


def _show(value: Any) -> str:
    text = repr(value)
    return text if len(text) <= 60 else text[:57] + "..."


def _fail(where: str, message: str) -> NoReturn:
    raise ValidationError(f"{where}: {message}")


def _fields(value: Any, where: str, allowed: tuple[str, ...], required: tuple[str, ...]) -> dict:
    if not isinstance(value, dict):
        _fail(where, "must be an object")
    for key in value:
        if key not in allowed:
            _fail(where, f"unknown field {_show(key)}")
    for key in required:
        if key not in value:
            _fail(where, f"missing field {key!r}")
    return value


def _text(value: Any, where: str, *, blank_ok: bool = False) -> str:
    if not isinstance(value, str):
        _fail(where, "must be text")
    if not blank_ok and not value.strip():
        _fail(where, "must not be empty")
    if len(value) > MAX_TEXT:
        _fail(where, f"is longer than {MAX_TEXT} characters")
    return value


def _flag(value: Any, where: str) -> bool:
    if not isinstance(value, bool):
        _fail(where, "must be true or false")
    return value


def _whole(value: Any, where: str, minimum: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        _fail(where, f"must be a whole number >= {minimum}, not {_show(value)}")
    return value


def _entries(value: Any, where: str, *, minimum: int = 0) -> list:
    if not isinstance(value, list):
        _fail(where, "must be a list")
    if len(value) < minimum:
        _fail(where, f"needs at least {minimum} entry" if minimum == 1 else f"needs at least {minimum} entries")
    if len(value) > MAX_ENTRIES:
        _fail(where, f"holds more than {MAX_ENTRIES} entries")
    return value


def _choice(value: Any, where: str, allowed: tuple[str, ...]) -> str:
    if not isinstance(value, str) or value not in allowed:
        _fail(where, f"must be one of {', '.join(allowed)}, not {_show(value)}")
    return value


def _partition(value: Any, where: str) -> str:
    if value == "confirmation":
        _fail(where, "the fresh confirmation set never appears in a report")
    return _choice(value, where, PARTITIONS)


def _version(value: Any, where: str) -> str:
    if not isinstance(value, str) or _VERSION.fullmatch(value) is None:
        _fail(where, f"must be a version string ({VERSION_PATTERN}), not {_show(value)}")
    return value


def _timestamp(value: Any, where: str) -> str:
    _text(value, where)
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        _fail(where, f"must be an ISO 8601 timestamp, not {_show(value)}")
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        _fail(where, "needs a timezone")
    return value


def is_identifier(value: Any) -> bool:
    """True for a safe record identifier: ^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$ (no path separator, no dot)."""
    return isinstance(value, str) and _IDENTIFIER.fullmatch(value) is not None


def validate_identifier(value: Any, field: str = "identifier") -> str:
    """Return ``value`` if it is a safe identifier, else raise ValidationError naming ``field``."""
    if not is_identifier(value):
        raise ValidationError(
            f"{field} must match ^{IDENTIFIER_PATTERN}$ (letters, digits, '_' and '-', at most 64), "
            f"not {_show(value)}"
        )
    return value


# ── the report ───────────────────────────────────────────────────────────────


def _sources(value: Any) -> list[dict]:
    rows, seen = [], set()
    for index, raw in enumerate(_entries(value, "sources", minimum=1)):
        where = f"sources[{index}]"
        _fields(raw, where, SOURCE_FIELDS, SOURCE_FIELDS)
        source_id = validate_identifier(raw["source_id"], f"{where}.source_id")
        if source_id in seen:
            _fail(where, f"duplicate source_id {source_id!r}")
        seen.add(source_id)
        rows.append({
            "source_id": source_id,
            "kind": _choice(raw["kind"], f"{where}.kind", SOURCE_KINDS),
            "label": _text(raw["label"], f"{where}.label"),
        })
    return rows


def _origin(value: Any, where: str) -> dict | None:
    if value is None:
        return None
    _fields(value, where, ORIGIN_FIELDS, ORIGIN_FIELDS)
    return {
        "round_report_ref": validate_identifier(value["round_report_ref"], f"{where}.round_report_ref"),
        "partition": _partition(value["partition"], f"{where}.partition"),
    }


def _evidence(value: Any, where: str) -> dict:
    _fields(value, where, EVIDENCE_FIELDS, EVIDENCE_FIELDS)
    row = {
        "item_ref": validate_identifier(value["item_ref"], f"{where}.item_ref"),
        "split": _partition(value["split"], f"{where}.split"),
        "role": _choice(value["role"], f"{where}.role", EVIDENCE_ROLES),
        "context": _text(value["context"], f"{where}.context", blank_ok=True),
        "text": _text(value["text"], f"{where}.text", blank_ok=True),
        "signal": _text(value["signal"], f"{where}.signal", blank_ok=True),
    }
    if row["split"] == "train" and not row["text"].strip():
        _fail(f"{where}.text", "a Train case shows its exact excerpt")
    if row["split"] == "test" and (row["text"] or row["context"]):
        _fail(where, "a Test case is cited by custody reference (item_ref) only; "
                     "its text and context stay empty and resolve at read time")
    return row


def _option(value: Any, where: str) -> dict:
    if isinstance(value, dict):
        for key in PRESELECTION_KEYS:
            if key in value:
                _fail(where, f"options are never preselected; remove {key!r}")
    _fields(value, where, OPTION_FIELDS, OPTION_FIELDS)
    return {
        "option_id": validate_identifier(value["option_id"], f"{where}.option_id"),
        "label": _text(value["label"], f"{where}.label"),
        "effect": _text(value["effect"], f"{where}.effect"),
        "scope": _text(value["scope"], f"{where}.scope"),
    }


def _card(value: Any, where: str, source_kinds: dict[str, str]) -> dict:
    _fields(value, where, CARD_FIELDS, CARD_REQUIRED)
    decision_id = validate_identifier(value["decision_id"], f"{where}.decision_id")
    where = f"card {decision_id}"
    question_type = _choice(value["question_type"], f"{where}.question_type", QUESTION_TYPES)
    origin = _origin(value.get("origin"), f"{where}.origin")

    source_ids = []
    for index, source_id in enumerate(_entries(value["source_ids"], f"{where}.source_ids", minimum=1)):
        validate_identifier(source_id, f"{where}.source_ids[{index}]")
        if source_id not in source_kinds:
            _fail(f"{where}.source_ids", f"{source_id!r} is not one of the report's sources")
        if source_id in source_ids:
            _fail(f"{where}.source_ids", f"duplicate source_id {source_id!r}")
        source_ids.append(source_id)

    evidence = []
    for index, raw in enumerate(_entries(value["evidence"], f"{where}.evidence")):
        row = _evidence(raw, f"{where}.evidence[{index}]")
        if any(row["item_ref"] == other["item_ref"] for other in evidence):
            _fail(f"{where}.evidence", f"duplicate item_ref {row['item_ref']!r}")
        evidence.append(row)

    options = []
    for index, raw in enumerate(_entries(value["options"], f"{where}.options", minimum=1)):
        option = _option(raw, f"{where}.options[{index}]")
        if any(option["option_id"] == other["option_id"] for other in options):
            _fail(f"{where}.options", f"duplicate option_id {option['option_id']!r}")
        options.append(option)

    cites_test = any(row["split"] == "test" for row in evidence) or any(
        source_kinds[source_id] == "test_item" for source_id in source_ids
    )
    if cites_test and question_type not in AUDIT_QUESTION_TYPES:
        _fail(where, "Test cases appear only on an audit card (question_type inconsistency or "
                     f"reference_label), not on {question_type}")
    if cites_test and origin is None:
        _fail(where, "a card citing Test cases names its audit issue in origin "
                     "(round_report_ref and partition)")

    return {
        "decision_id": decision_id,
        "short_title": _text(value["short_title"], f"{where}.short_title"),
        "question_type": question_type,
        "question": _text(value["question"], f"{where}.question"),
        "why_now": _text(value["why_now"], f"{where}.why_now"),
        "current_rule": _text(value["current_rule"], f"{where}.current_rule"),
        "evidence": evidence,
        "options": options,
        "none_allowed": _flag(value["none_allowed"], f"{where}.none_allowed"),
        "defer_allowed": _flag(value["defer_allowed"], f"{where}.defer_allowed"),
        "comments_allowed": _flag(value["comments_allowed"], f"{where}.comments_allowed"),
        "approval_scope": _choice(value["approval_scope"], f"{where}.approval_scope", APPROVAL_SCOPES),
        "source_ids": source_ids,
        "origin": origin,
    }


def validate_report(report: dict) -> dict:
    """Return the normalized published report, or raise ValidationError naming the first broken field.

    Every field is required except a card's ``origin`` (None unless a round report raised the card).  An
    unknown field anywhere is refused, so nothing rides along unchecked: a preselected option, a reference
    label on an evidence row, a status.  The result is a new dict whose fields follow the contract's order;
    validating it again returns an equal dict, and the input is never changed.
    """
    _fields(report, "report", REPORT_FIELDS, REPORT_FIELDS)
    if report["schema"] != REPORT_SCHEMA:
        _fail("report.schema", f"must be {REPORT_SCHEMA!r}, not {_show(report['schema'])}")
    schema_version = report["schema_version"]
    if isinstance(schema_version, bool) or schema_version != SCHEMA_VERSION:
        _fail("report.schema_version", f"unsupported schema_version {_show(schema_version)}; "
                                       f"this reader knows {SCHEMA_VERSION}")

    job_id = validate_identifier(report["job_id"], "job_id")
    report_id = validate_identifier(report["report_id"], "report_id")
    report_revision = _whole(report["report_revision"], "report.report_revision", 1)
    round_id = validate_identifier(report["round_id"], "round_id")
    title = _text(report["title"], "report.title")
    purpose = _text(report["purpose"], "report.purpose")
    raw_base = _fields(report["base"], "base", BASE_FIELDS, BASE_FIELDS)
    base = {key: _version(raw_base[key], f"base.{key}") for key in BASE_FIELDS}
    sources = _sources(report["sources"])
    source_kinds = {row["source_id"]: row["kind"] for row in sources}
    cards = []
    for index, raw in enumerate(_entries(report["cards"], "cards", minimum=1)):
        card = _card(raw, f"cards[{index}]", source_kinds)
        if any(card["decision_id"] == other["decision_id"] for other in cards):
            _fail("cards", f"duplicate decision_id {card['decision_id']!r}")
        cards.append(card)

    return {
        "schema": REPORT_SCHEMA,
        "schema_version": SCHEMA_VERSION,
        "job_id": job_id,
        "report_id": report_id,
        "report_revision": report_revision,
        "round_id": round_id,
        "title": title,
        "purpose": purpose,
        "base": base,
        "sources": sources,
        "cards": cards,
        "published_at": _timestamp(report["published_at"], "report.published_at"),
        "publication_actor": validate_identifier(report["publication_actor"], "publication_actor"),
        "synthetic": _flag(report["synthetic"], "report.synthetic"),
    }


# ── the answers ──────────────────────────────────────────────────────────────


def _answer(card: dict, value: Any) -> dict:
    where = f"answer to {card['decision_id']}"
    if value is None:
        return {"kind": "unanswered", "option_id": None, "text": None, "comment": ""}
    _fields(value, where, ANSWER_FIELDS, ("kind",))
    kind = _choice(value["kind"], f"{where}.kind", ANSWER_KINDS)
    option_id, text, comment = value.get("option_id"), value.get("text"), value.get("comment")

    if kind == "chosen":
        if option_id not in [option["option_id"] for option in card["options"]]:
            _fail(where, f"a chosen answer names one option of this card, not {_show(option_id)}")
    elif option_id is not None:
        _fail(where, f"option_id is only for a chosen answer, not for {kind}")

    if kind == "custom":
        if not isinstance(text, str) or not text.strip():
            _fail(where, "a custom answer needs the person's own text")
        _text(text, f"{where}.text")
    elif text not in (None, ""):
        _fail(where, f"text is only for a custom answer, not for {kind}")
    else:
        text = None

    if kind == "defer" and not card["defer_allowed"]:
        _fail(where, "this card does not allow defer")
    if kind == "reject_options" and not card["none_allowed"]:
        _fail(where, "this card does not allow rejecting every option (none_allowed is false)")

    if comment is None:
        comment = ""
    _text(comment, f"{where}.comment", blank_ok=True)
    if comment and not card["comments_allowed"]:
        _fail(where, "this card does not take comments")
    return {"kind": kind, "option_id": option_id if kind == "chosen" else None, "text": text,
            "comment": comment}


def validate_answers(report: dict, answers: dict) -> dict:
    """Return one normalized answer per card of ``report``, in card order, or raise ValidationError.

    ``answers`` is keyed by decision_id; a card left out (or given None) is ``unanswered``, and an unknown
    decision_id is refused.  Each answer is ``{kind, option_id?, text?, comment?}``:

        chosen          option_id names one option of that card
        reject_options  none of the options fits (needs none_allowed)
        custom          the person's own answer, in non-empty text
        defer           decide later (needs defer_allowed)
        unanswered      no answer yet

    The answered states are never converted into one another.  A comment needs comments_allowed and is kept
    exactly as written, spaces and line breaks included; an absent comment is "".  The result is
    ``{decision_id: {kind, option_id, text, comment}}``.
    """
    normalized = validate_report(report)
    if not isinstance(answers, dict):
        raise ValidationError("answers must be an object keyed by decision_id")
    cards = {card["decision_id"]: card for card in normalized["cards"]}
    for decision_id in answers:
        if decision_id not in cards:
            raise ValidationError(f"answers: unknown decision_id {_show(decision_id)}")
    return {decision_id: _answer(card, answers.get(decision_id)) for decision_id, card in cards.items()}
