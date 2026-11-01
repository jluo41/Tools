"""Update, the last step of a 🧭 meaning loop (b15 s58 C4): the person's saved answers to the loop's interaction report
become the next reference labels and the list of what changed, deterministically. The guideline's words (meaning/mNN.
mindmap.md) are the agent's to write, each rule citing its card; this writes the labels and names the rule answers it
must write.

    python meaning_update.py labels --report <report.json> --form <the collect Run> --previous <labels.jsonl>
                                    --version l02 --out <the update Run>/result

Writes, into --out:
    labels.jsonl          every item: label, from, status, cites, note, blind
    changes.md            one line per changed label, then the rule answers the guideline must take
    decision_record.json  the validated answers, keyed by decision_id

--previous is the existing labels (l00, legacy_labels.jsonl) in Loop 1, else the last Update's labels.jsonl. A card
over its options, or an answer the report never offered, is refused (meaning_contracts), never guessed.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _load(name: str):
    spec = importlib.util.spec_from_file_location(f"labeling_{name}_for_update", HERE / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


la = _load("label_audit")
rf = _load("report_form")


def update(report: dict, answer_text: str, previous: list, *, version: str, run: str) -> dict:
    """{version, labels, changes, rules, answers}: the answers read from the saved form (report_form.answers_from,
    validated), applied to the previous labels (label_audit.apply_answers). An item this loop's report does not show
    keeps its previous record whole (its status, cites, note and blind judgment), so Loop N never undoes Loop N-1's
    review (found by the skill's run-through, 261101)."""
    report = rf.mc.validate_report(report)
    answers = rf.answers_from(report, answer_text)
    out = la.apply_answers(previous, report, answers, version=version, run=run)
    shown = {ev["item_ref"] for card in report["cards"] for ev in card["evidence"] if ev.get("item_ref")}
    before = {r["item_id"]: r for r in previous if "status" in r}       # an earlier Update's record, not l00's votes
    out["labels"] = [dict(before[r["item_id"]]) if r["item_id"] in before and r["item_id"] not in shown else r
                     for r in out["labels"]]
    out["answers"] = answers
    return out


def changes_md(out: dict, form: str, notes: str = "") -> str:
    """What the answers changed: each relabelled item, then each rule answer the guideline must take; the person's
    notes from the Preferences prompt first, when they sent any."""
    lines = [f"# Reference labels {out['version']} · what changed", "",
             f"From the answers saved in {form}. Each line cites its card.", ""]
    if notes.strip():
        lines += [f"Your notes with the answers: {notes.strip()}", ""]
    lines += [f"- {c['item_id']}: {c['from'] or 'no majority'} → {c['to']} ({c['cites']})" for c in out["changes"]] \
        or ["- no label changed"]
    pending = [r for r in out["labels"] if r["status"] in ("pending_rule", "deferred", "custom")]
    if pending:
        lines += ["", "## Kept, waiting on a rule or more evidence", ""]
        lines += [f"- {r['item_id']}: {r['status'].replace('_', ' ')} ({r['cites']})" + (f": {r['note']}" if r["note"] else "")
                  for r in pending]
    if out["rules"]:
        lines += ["", "## Rule answers the guideline must take", ""]
        for did, r in out["rules"].items():
            words = r["text"] or r["option"] or r["answer"]
            lines.append(f"- {did}: {words} ({r['cites']})" + (f": {r['comment']}" if r["comment"] else ""))
    return "\n".join(lines) + "\n"


def write(out: dict, dest: Path, form: str, notes: str = "", now=None) -> list[Path]:
    """The three files into `dest`; when `dest` is a Run's result/, also that Run's card (run.yaml, if it has none)
    and its receipt (result/runtime.yaml), so the Update Run reads as done (meaning_versions.state)."""
    from datetime import datetime
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    la._write_jsonl(dest / "labels.jsonl", out["labels"])
    (dest / "changes.md").write_text(changes_md(out, form, notes), encoding="utf-8")
    (dest / "decision_record.json").write_text(json.dumps(out["answers"], indent=1, ensure_ascii=False) + "\n",
                                               encoding="utf-8")
    paths = [dest / "labels.jsonl", dest / "changes.md", dest / "decision_record.json"]
    run = dest.parent
    if dest.name == "result" and run.name.startswith("r"):
        at = (now or datetime.now()).strftime("%Y-%m-%d %H:%M")
        if not (run / "run.yaml").is_file():
            (run / "run.yaml").write_text(f"run: {run.name}\nkind: soft\ntype: update\nstatus: done\n"
                                          f"reads: {form}/result/answer_collection.md\n", encoding="utf-8")
            paths.append(run / "run.yaml")
        (dest / "runtime.yaml").write_text(f"run: {run.name}\nstatus: done\nended: '{at}'\n", encoding="utf-8")
        paths.append(dest / "runtime.yaml")
    return paths


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    one = sub.add_parser("labels", help="the next reference labels and what changed, from a saved form")
    one.add_argument("--report", type=Path, required=True)
    one.add_argument("--form", type=Path, required=True, help="the collect Run whose result/answer_collection.md is saved")
    one.add_argument("--previous", type=Path, required=True)
    one.add_argument("--version", required=True, help="lNN, the labels this Update makes")
    one.add_argument("--out", type=Path, required=True)
    one.add_argument("--notes", default="", help="the person's notes from the Preferences prompt, kept in changes.md")
    a = ap.parse_args(argv)
    saved = a.form / "result" / "answer_collection.md"
    if not saved.is_file():
        print(f"not updated: {saved} is missing; save the answers first (collect.py save)", file=sys.stderr)
        return 1
    report = json.loads(a.report.read_text(encoding="utf-8"))
    out = update(report, saved.read_text(encoding="utf-8"), list(la._read_jsonl(a.previous)),
                 version=a.version, run=a.form.name.split("_", 1)[0])
    for path in write(out, a.out, a.form.name, a.notes):
        print(path)
    print(f"{len(out['changes'])} label(s) changed; {len(out['rules'])} rule answer(s) for the guideline")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
