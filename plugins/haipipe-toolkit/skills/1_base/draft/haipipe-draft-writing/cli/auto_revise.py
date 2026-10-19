"""Auto revise: the record and the stop rule of a loop of revise rounds (s41-D13, JL 261016).

A round is the writer (this skill) revising a candidate copy, then a FRESH reviewer (haipipe-draft-review, another
agent) judging it against the shared rubric. This script does not write or judge: it keeps the rounds, applies the
stop rule, and gathers the big decisions for the person.

    python auto_revise.py start  <run dir> --source <text.md>        copy the text in as round 0's candidate
    python auto_revise.py record <run dir> <round.yaml>              file one round (the writer's and reviewer's output)
    python auto_revise.py check  <run dir> [--max-rounds 3]          STOP or CONTINUE, and why
    python auto_revise.py cards  <run dir>                           the decision cards and the folded small fixes

A run dir holds `candidate.md` (the text as it stands now, never the Draft), `rounds/rNN.yaml` and `decisions.yaml`.
A round file:

    round: 1
    rubric: {Mechanics: MEETS, Function: NEEDS WORK, Evidence: NOT VERIFIABLE, Readability: MEETS}   # the reviewer's
    anti_slop: 34                       # anti_slop.py audit --format json → score, on the candidate after the round
    small:  [{where: S5, before: "…", after: "…", why: "…"}]          # applied to candidate.md by the writer
    big:    [{where: S5, what: "…", options: ["…", "…"], lean: "…", why: "…"}]   # held for the person, never applied

Small vs big: big is anything that changes a claim, a number, a citation, the order of the argument or the plan
(`## 1 · Structure`); everything else is small. The stop rule follows the rubric ("no detector score establishes
acceptance"): STOP when no axis says NEEDS WORK, or a round did not reduce the NEEDS WORK count, or the round limit is
reached. anti_slop is a guard: a round that raises it by more than 5 points does not count as an improvement.
NOT VERIFIABLE is never a pass: it becomes a decision card (the evidence or authority is missing).
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

import yaml

VERDICTS = {"MEETS", "NEEDS WORK", "N/A", "NOT VERIFIABLE"}
AXES = ("Mechanics", "Function", "Evidence", "Readability")


def rounds(run: Path) -> list:
    return [yaml.safe_load(p.read_text(encoding="utf-8")) for p in sorted((run / "rounds").glob("r*.yaml"))]


def needs_work(r: dict) -> int:
    return sum(1 for v in r.get("rubric", {}).values() if v == "NEEDS WORK")


def check(rs: list, max_rounds: int = 3) -> tuple:
    """(STOP | CONTINUE, why)."""
    if not rs:
        return "CONTINUE", "no round yet"
    last = rs[-1]
    if needs_work(last) == 0:
        return "STOP", f"round {last['round']}: no axis needs work (the reviewer's verdict)"
    if len(rs) >= 2:
        prev = rs[-2]
        better = needs_work(last) < needs_work(prev)
        worse_slop = (last.get("anti_slop") or 0) > (prev.get("anti_slop") or 0) + 5
        if not better or worse_slop:
            why = "the NEEDS WORK count did not fall" if not better else "anti_slop rose by more than 5"
            return "STOP", f"round {last['round']}: no improvement ({why})"
    if len(rs) >= max_rounds:
        return "STOP", f"round limit {max_rounds} reached"
    return "CONTINUE", f"round {last['round']}: {needs_work(last)} axis needs work"


def validate(r: dict) -> list:
    out = []
    if not isinstance(r.get("round"), int):
        out.append("round must be a number")
    for axis, v in r.get("rubric", {}).items():
        if axis not in AXES or v not in VERDICTS:
            out.append(f"rubric {axis}: {v!r} is not one of the four verdicts on the four axes")
    for b in r.get("big", []):
        if not b.get("options"):
            out.append(f"big {b.get('where')}: a decision needs options")
    return out


def cards(rs: list) -> dict:
    """Every big item, plus each NOT VERIFIABLE axis of the last round, as a decision card; the small fixes folded."""
    decisions, seen = [], set()
    for r in rs:                                                # a decision held in several rounds is one decision
        for b in r.get("big", []):
            if (b.get("where"), b.get("what")) not in seen:
                seen.add((b.get("where"), b.get("what")))
                decisions.append(dict(b, round=r["round"], kind="decision"))
    if rs:
        for axis, v in rs[-1].get("rubric", {}).items():
            if v == "NOT VERIFIABLE":
                decisions.append({"where": "Evidence", "kind": "decision", "round": rs[-1]["round"],
                                  "what": f"{axis} cannot be verified: the evidence or authority is missing",
                                  "options": ["add the source", "narrow the claim", "accept as open"],
                                  "lean": "add the source", "why": "NOT VERIFIABLE is never a pass"})
    small = [dict(s, round=r["round"]) for r in rs for s in r.get("small", [])]
    grouped = {}                                                # one card per place: every concern about it together
    for dcn in decisions:
        where = str(dcn.get("where", "Section")).split(",")[0].strip()   # "S2, S3" goes on S2's card
        g = grouped.setdefault(where, {"where": where, "kind": "decision",
                                                              "concerns": [], "options": [], "lean": None})
        g["concerns"].append(dcn.get("what"))
        g["options"] += [o for o in dcn.get("options", []) if o not in g["options"]]
        g["lean"] = g["lean"] or dcn.get("lean")                # the first lean given stays the card's lean
    num = lambda w: int(re.sub(r"\D", "", w) or 0)              # S2 before S10; the Section last
    cards_ = sorted(grouped.values(), key=lambda g: (g["where"] in ("Section", "Evidence"), g["where"][:1], num(g["where"])))
    return {"decisions": cards_, "small_fixes": small,
            "summary": f"{len(cards_)} decisions for you ({len(decisions)} concerns); {len(small)} small fixes in {len(rs)} rounds"}


def main():
    ap = argparse.ArgumentParser(description="Auto revise: rounds, stop rule, decision cards.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("start"); s.add_argument("run"); s.add_argument("--source", required=True)
    r = sub.add_parser("record"); r.add_argument("run"); r.add_argument("round_file")
    c = sub.add_parser("check"); c.add_argument("run"); c.add_argument("--max-rounds", type=int, default=3)
    k = sub.add_parser("cards"); k.add_argument("run")
    a = ap.parse_args()
    run = Path(a.run)
    if a.cmd == "start":
        (run / "rounds").mkdir(parents=True, exist_ok=True)
        shutil.copyfile(a.source, run / "candidate.md")
        print(f"started: {run / 'candidate.md'} (a copy; the Draft is never written here)")
    elif a.cmd == "record":
        data = yaml.safe_load(Path(a.round_file).read_text(encoding="utf-8"))
        problems = validate(data)
        if problems:
            sys.exit("not recorded: " + "; ".join(problems))
        out = run / "rounds" / f"r{data['round']:02d}.yaml"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")
        print(f"recorded {out.name}")
    elif a.cmd == "check":
        verdict, why = check(rounds(run), a.max_rounds)
        print(f"{verdict}: {why}")
    else:
        out = cards(rounds(run))
        (run / "decisions.yaml").write_text(yaml.safe_dump(out, sort_keys=False, allow_unicode=True), encoding="utf-8")
        print(out["summary"])


if __name__ == "__main__":
    main()
