"""A card's Evaluation column: each acceptance rule with the review's mark, the
reviewer's notes, and the expected effect.

Split out of design_page.py; design_page.py re-exports every name here."""
from __future__ import annotations

import re

from live.design import _escape, _read, shown_design
from live.design_page_runs import _criterion_words, run_short


def _rule_checks(item: dict) -> tuple[str, str]:
    """Each acceptance rule with the mark the review of the SHOWN draft gave it.

    The review is the Verify whose target is the draft on the card, else that
    draft's own self-check, else nothing (audit N2).  Rule N is criterion rNN,
    plus rNNb, rNNc when the rule quoted several phrases; a hand-written config
    with its own criterion names is matched by order when the counts agree."""
    shown = shown_design(item)
    source, word = None, ""
    if shown:
        for r in reversed(item["runs"]):
            if (r["kind"] == "verify" and r["status"] == "complete" and r["checks"]
                    and any(str(t.get("path", "")).startswith(f'results/{shown["run"]}/') for t in r["targets"])):
                source, word = r, "independent review"
                break
        if source is None:
            own = next((r for r in item["runs"] if r["id"] == shown["run"] and r["checks"]), None)
            source, word = (own, "self-check") if own else (None, "")
    checks = source["checks"] if source else []
    by_id: dict[str, list[str]] = {}
    for c in checks:
        hit = re.match(r"^(r\d{2})[a-z]?$", str(c.get("criterion")))
        if hit:
            by_id.setdefault(hit.group(1), []).append(str(c.get("status")))
    if checks and not by_id and source["criteria"]:
        # a hand-written config names its own criteria (length, optout): show those, by name
        status = {str(c.get("criterion")): str(c.get("status")) for c in checks}
        lines = [(_criterion_words(c), [status.get(str(c.get("id")), "")]) for c in source["criteria"]]
    else:
        lines = [(rule, by_id.get(f"r{i:02d}", [])) for i, rule in enumerate(item["acceptance"], start=1)]
    rows = []
    for rule, marks in lines:
        s_ = ("fail" if "fail" in marks else "pass" if marks and all(m == "pass" for m in marks)
              else "unresolved" if any(marks) else "")
        glyph = ('<span class="g ok">✓</span>' if s_ == "pass" else '<span class="g bad">✗</span>' if s_ == "fail"
                 else '<span class="g mut">·</span>')
        rows.append(f"<li>{glyph}{_escape(rule)}</li>")
    head = (f'<span class=mut>{word} '
            f'{_escape(run_short(source["id"]))}</span>') if source else '<span class=mut>not checked yet</span>'
    released = next((r for r in item["runs"] if r["kind"] == "commission" and r["outcome"] == "release"), None)
    if released and _bet_changed(item, released):
        head += (f' <span class=bad>· the register changed after release ({_escape(run_short(released["id"]))}); '
                 'drafts still follow the released goal and rules</span>')
    return head, "".join(rows) or "<li class=mut>none</li>"


def _bet_changed(item: dict, released: dict) -> bool:
    """Whether the register's goal, bet or rules differ from what the Commission froze."""
    intent = released["intent"] or {}
    frozen_rules = released.get("acceptance")
    return bool(
        (intent.get("move") and intent["move"] not in (item["goal"], item["title"]))
        or (intent.get("move") and (intent.get("expected_effect") or "") != (item["expected"] or "")
            and released["design_mode"] != "brainstorm")
        or (frozen_rules is not None and list(frozen_rules) != list(item["acceptance"])))


def _review_notes(item: dict) -> str:
    """The independent reviewer's own words on the shown draft (its `review.md`), one per line."""
    shown = shown_design(item)
    if not shown:
        return ""
    for r in reversed(item["runs"]):
        if (r["kind"] == "verify" and r["status"] == "complete"
                and any(str(t.get("path", "")).startswith(f'results/{shown["run"]}/') for t in r["targets"])):
            path = r["result_dir"] / "review.md"
            if not path.is_file():
                return ""
            lines = [re.sub(r"^[-*]\s+|^\d+[.)]\s+", "", ln.strip()) for ln in _read(path).splitlines()
                     if ln.strip() and not ln.lstrip().startswith("#")]
            return "".join(f"<li>{_escape(ln)}</li>" for ln in lines[:8])
    return ""


def _evaluation_col(item: dict, aim: dict | None = None) -> str:
    """The open card's right column: Evaluation, of two kinds. Acceptance is
    judged now, by the independent Verify; the expected effect is judged later, by the send."""
    aim = aim or {}
    head, rules = _rule_checks(item)
    notes = _review_notes(item)
    out = (f'<details class=sub><summary>Acceptance · {head}</summary><ul class=checks>{rules}</ul></details>')
    if notes:
        out += f'<details class=sub><summary>Review notes</summary><ul class=notes>{notes}</ul></details>'
    effect = ""
    for label, value in (("Expected", item["expected"]), ("Wrong if", item["falsified"]),
                         ("Against", aim.get("baseline", "")), ("Measured by", aim.get("success metrics", ""))):
        if value:
            tone = {"Expected": "ok", "Wrong if": "bad"}.get(label, "mut")
            effect += f'<div class=betl><span class="k {tone}">{label}</span>{_escape(value)}</div>'
    out += ('<details class=sub><summary>Expected effect · <span class=mut>not tested yet, judged at the send</span></summary>'
            + (effect or '<div class=mut>No expected effect recorded.</div>') + '</details>')
    return out
