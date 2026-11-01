#!/usr/bin/env python3
"""A decision report (meaning_contracts) as a /haipipe-interaction form, and the form's answers back as a decision
record. Each meaning loop's report is one collect Run: its question_collection.md is written here, from the report,
never by hand (b15 s58-D08: "the agent using the /haipipe-labeling-interaction to call /haipipe-interaction to
generate the report").

    to_collection(report, *, title, for_, intro)   the report's cards as question_collection.md, nothing ticked
    answers_from(report, answer_text)              the pasted (or saved) answers as validate_answers' records

Card k is question Qk. A card's options become A, B, C in order; when the card allows defer, one more option asks
for more context. The form's own last choice, "My own decision", is a custom answer (slide 23: "Write another
decision"), and its note box is the comment ("Reason and intended scope"). A card that breaks the form's limits
raises FormError: it is never trimmed silently. Evidence excerpts are shortened for the card's sketch only (marked
with …); the report keeps them exact.

CLI:
    report_form.py form    <report.json> <run folder> --title T --for F [--intro I]   writes question_collection.md
    report_form.py answers <report.json> <run folder>                                 prints the decision record
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent
COLLECT = HERE.parents[2] / "1_base" / "workbench" / "haipipe-interaction" / "scripts" / "collect.py"
LETTERS = "ABCD"
DEFER_TEXT = "Defer: I need more context."
SKETCH_WIDTH = 80


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


mc = _load("labeling_meaning_contracts_form", HERE / "meaning_contracts.py")
collect = _load("haipipe_interaction_collect_form", COLLECT)


class FormError(ValueError):
    """A card breaks the form's limits (collect.py LIMITS); the message names the card and the limit."""


def _words(text: str) -> int:
    return len(str(text or "").split())


def _flat(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()


def _cut(text: str, width: int = SKETCH_WIDTH) -> str:
    text = _flat(text)
    return text if len(text) <= width else text[: width - 1].rstrip() + "…"


def _wrap(text: str, width: int = SKETCH_WIDTH, lines: int = 3) -> list[str]:
    parts = textwrap.wrap(_flat(text), width - 1) or [""]
    if len(parts) > lines:
        parts = parts[:lines]
        parts[-1] = parts[-1][: width - 2].rstrip() + "…"
    return parts


def _last_turn(context: str) -> str:
    turns = [line for line in str(context or "").splitlines() if line.strip()]
    return turns[-1] if turns else ""


def sketch(card: dict) -> list[str]:
    """At most six lines: a rule card shows its rule, the case that fits and the case that conflicts; any other
    card shows its first case's last earlier turn, the judged reply, and its signal when the card shows one."""
    rows = card["evidence"]
    if card["question_type"] == "define_rule":
        lines = [f"rule      {_cut(card['current_rule'], SKETCH_WIDTH - 10)}"]
        names = {"case_a": "fits", "case_b": "conflicts", "context": "context"}
        for row in rows[:4]:
            lines.append(f"{names[row['role']]:<10}{row['item_ref']}: {_cut(row['text'], SKETCH_WIDTH - 12 - len(row['item_ref']))}")
        return lines[:6]
    row = next((r for r in rows if r["role"] == "case_a"), rows[0] if rows else None)
    if row is None or row["split"] == "test":
        return [f"case      {row['item_ref']} (Test: read it in the workbench)"] if row else []
    lines = []
    if _last_turn(row["context"]):
        lines.append(f"before    {_cut(_last_turn(row['context']), SKETCH_WIDTH - 10)}")
    wrapped = _wrap(row["text"], SKETCH_WIDTH - 10, 3)
    lines += [f"{'reply' if k == 0 else '':<10}{part}" for k, part in enumerate(wrapped)]
    if row["signal"]:
        lines += [f"{'raters' if k == 0 else '':<10}{part}" for k, part in enumerate(_wrap(row["signal"], SKETCH_WIDTH - 10, 2))]
    return lines[:6]


def _options(card: dict) -> list[str]:
    labels = [option["label"] for option in card["options"]] + ([DEFER_TEXT] if card["defer_allowed"] else [])
    if not 2 <= len(labels) <= collect.LIMITS["options"]:
        raise FormError(f"card {card['decision_id']}: {len(labels)} options with defer; the form takes 2 to "
                        f"{collect.LIMITS['options']}")
    for label in labels:
        if _words(label) > collect.LIMITS["option"]:
            raise FormError(f"card {card['decision_id']}: option {label!r} has {_words(label)} words; at most "
                            f"{collect.LIMITS['option']}")
    return [f"- [ ] {LETTERS[k]} · {label}" for k, label in enumerate(labels)]


def to_collection(report: dict, *, title: str, for_: str, intro: str = "") -> str:
    """question_collection.md for one report: Qk is card k; nothing is ticked (options are never preselected)."""
    normalized = mc.validate_report(report)
    cards = normalized["cards"]
    if not 2 <= _words(title) <= 4:
        raise FormError(f"title {title!r}: two to four words")
    if _words(intro) > collect.LIMITS["intro"]:
        raise FormError(f"intro: at most {collect.LIMITS['intro']} words")
    if len(cards) > collect.LIMITS["questions"]:
        raise FormError(f"{len(cards)} cards; one form holds at most {collect.LIMITS['questions']}")
    out = [f"# {title}", "", f"for: {for_}", "",
           f"<!-- GENERATED by report_form.to_collection from {normalized['report_id']} revision "
           f"{normalized['report_revision']}: question Qk is card k. Change the report and write this again. -->", ""]
    if intro:
        out += [intro, ""]
    for k, card in enumerate(cards, 1):
        where = f"card {card['decision_id']}"
        if not 1 <= _words(card["short_title"]) <= 3:
            raise FormError(f"{where}: short_title {card['short_title']!r}, one to three words")
        if _words(card["why_now"]) > collect.LIMITS["why"]:
            raise FormError(f"{where}: why_now has {_words(card['why_now'])} words; at most {collect.LIMITS['why']}")
        question = card["question"].strip()
        if not question.endswith("?") or _words(question) > collect.LIMITS["ask"]:
            raise FormError(f"{where}: the question ends with ? and has at most {collect.LIMITS['ask']} words")
        out += [f"## Q{k} · {card['short_title']}", "", _flat(card["why_now"]), ""]
        lines = sketch(card)
        if lines:
            out += ["```text", *lines, "```", ""]
        out += [f"**{question}**", "", *_options(card), ""]
    return "\n".join(out).rstrip() + "\n"


def _paste(answer_text: str) -> str:
    """The copied text: the whole of a paste, or the part of a saved answer file that keeps it word for word."""
    lines = answer_text.splitlines()
    for k, line in enumerate(lines):
        if line.strip().startswith(collect.HEADS):
            return "\n".join(lines[k:])
    return answer_text


def answers_from(report: dict, answer_text: str) -> dict:
    """The person's answers as validate_answers' records: a letter is chosen (or defer, for the defer letter), the
    form's own decision is custom (its words are the note), no pick is unanswered. A note on a card that takes no
    comment is refused by validate_answers, never dropped."""
    normalized = mc.validate_report(report)
    given, _odd, twice = collect.picks(_paste(answer_text))
    if twice:
        raise FormError(f"answered twice: {', '.join(twice)}")
    answers = {}
    for k, card in enumerate(normalized["cards"], 1):
        got = given.get(f"Q{k}")
        if not got or not got["pick"]:
            continue
        note = got["note"]
        if got["pick"] == collect.OWN:
            answers[card["decision_id"]] = {"kind": "custom", "text": note}
            continue
        index = LETTERS.index(got["pick"])
        if card["defer_allowed"] and index == len(card["options"]):
            answers[card["decision_id"]] = {"kind": "defer", "comment": note}
        elif index < len(card["options"]):
            answers[card["decision_id"]] = {"kind": "chosen", "option_id": card["options"][index]["option_id"],
                                            "comment": note}
        else:
            raise FormError(f"Q{k}: pick {got['pick']} is not one of the card's options")
    return mc.validate_answers(report, answers)


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("form", help="write question_collection.md from the report")
    f.add_argument("report", type=Path)
    f.add_argument("run", type=Path)
    f.add_argument("--title", required=True)
    f.add_argument("--for", dest="for_", required=True)
    f.add_argument("--intro", default="")
    a = sub.add_parser("answers", help="the saved answers as a decision record")
    a.add_argument("report", type=Path)
    a.add_argument("run", type=Path)
    args = ap.parse_args(argv)
    report = json.loads(args.report.read_text(encoding="utf-8"))
    if args.cmd == "form":
        text = to_collection(report, title=args.title, for_=args.for_, intro=args.intro)
        (args.run / collect.QUESTIONS).write_text(text, encoding="utf-8")
        print(args.run / collect.QUESTIONS)
        return
    print(json.dumps(answers_from(report, (args.run / collect.ANSWERS).read_text(encoding="utf-8")), indent=1,
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
