#!/usr/bin/env python3
"""definition-discussion Run: the identified human settles what each label means, one label at a time.

The AI may ask, propose wording, and offer made-up edge cases.  It never picks a
meaning, and it never uses a round item as an example, so the human's first
answers stay blind.  Only the human's stated decisions are recorded as decisions.

    start    open the Run, or return the one already open      runs/<run>.yaml · results/<run>/before.yaml
    say      keep one turn of the talk, human or model          results/<run>/turns.jsonl
    decide   the human settles one label: keep it, or new words results/<run>/decisions.jsonl
    close    every label settled: write the ledger; changed
             wording becomes one meaning revision (job.py)      results/<run>/ledger.yaml · result.yaml

A changed meaning retires the G0 confirmation, so the human presses Confirm
meaning again.  Meanings change only before any item has a first answer; after
that, a change is a guideline patch for guideline-learn.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
_SPEC = importlib.util.spec_from_file_location("subjective_label_calibration_for_definition", HERE / "calibration.py")
cal = importlib.util.module_from_spec(_SPEC)
assert _SPEC.loader is not None
_SPEC.loader.exec_module(cal)
job = cal.job
LabelingRefused = cal.LabelingRefused

OPERATION = "definition-discussion"
AUTHORS = ("human", "model")
ACCEPTANCE = "every label settled by the human; changed wording is one meaning revision"


def _labels(config: dict) -> tuple[list[str], dict]:
    labels = config.get("labels") if isinstance(config.get("labels"), dict) else {}
    meanings = labels.get("meanings") if isinstance(labels.get("meanings"), dict) else {}
    return [str(v) for v in labels.get("values") or []], meanings


def _runs(job_root: Path) -> list[str]:
    base = job.runs_dir(job_root)
    if not base.is_dir():
        return []
    names = [p.stem for p in base.glob(f"rl*_{OPERATION}_*.yaml")]
    return sorted(names, key=lambda n: int(n[2:].split("_", 1)[0]))


def _runtime(job_root: Path, run: str) -> dict:
    path = job.results_dir(job_root) / run / "runtime.yaml"
    return job.load_mapping(path) if path.is_file() else {}


def _open_run(job_root: Path) -> str | None:
    return next((r for r in reversed(_runs(job_root)) if _runtime(job_root, r).get("status") == "running"), None)


def _require(job_root: Path, human_id: str) -> dict:
    state = job.status(job_root)
    if state["missing"] or state["p0_integrity_errors"]:
        raise LabelingRefused(f"P0 contract integrity must pass first: {state['p0_integrity_errors'] or state['missing']}")
    if state["hold"]:
        raise LabelingRefused(f"HOLD · {state['hold_reason']}")
    if not human_id or human_id != state.get("human_id"):
        raise LabelingRefused("caller-supplied human_id must match the configured semantic authority")
    return state


def _running(job_root: Path, run: str) -> None:
    if run not in _runs(job_root):
        raise LabelingRefused(f"no {OPERATION} Run named {run}")
    if _runtime(job_root, run).get("status") != "running":
        raise LabelingRefused(f"{run} is closed; start a new discussion")


def _read_jsonl(path: Path) -> list[dict]:
    return cal._read_jsonl(path)


def _append(path: Path, row: dict) -> dict:
    with cal._locked(path.with_name(".lock")):
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")
    return row


def start(job_root: Path, *, human_id: str, channel: str = "claude chat") -> dict:
    """Open one discussion of the label meanings, or return the one already open."""
    job_root = job_root.resolve()
    _require(job_root, human_id)
    already = _open_run(job_root)
    if already:
        return {**state(job_root, already), "resumed": True}
    judged = job._judged_items(job_root)
    if judged:
        raise LabelingRefused("items are already judged, so the meanings are fixed; "
                              "a change now is a guideline patch for guideline-learn")
    config_path = job_root / "config.yaml"
    values, meanings = _labels(job.load_mapping(config_path))
    if not values:
        raise LabelingRefused("config.yaml names no labels to discuss")
    target = f"labels-v{len(_runs(job_root)) + 1}"
    run = cal._run_name(job_root, OPERATION, target)
    before = job.yaml_bytes({"labels": values, "meanings": meanings})
    job.write_once(job.results_dir(job_root) / run / "before.yaml", before)
    cal._write_run(
        job_root, run, operation=OPERATION, phase="P0", episode="meaning", target=target,
        commission={"path": job.page_path(job_root, "config.yaml")},
        inputs=[{"path": f"results/{run}/before.yaml"}],
        worker={"kind": "human", "name": human_id, "surface": channel},
        acceptance=ACCEPTANCE, status="running", started_at=cal.now_iso(), finished_at=None,
        outcome="discussing", artifacts=[],
    )
    return {**state(job_root, run), "resumed": False}


def say(job_root: Path, run: str, *, human_id: str, author: str, text: str, label: str | None = None) -> dict:
    """Keep one turn of the talk: the human's own words, or the model's question or proposal."""
    job_root = job_root.resolve()
    _require(job_root, human_id)
    _running(job_root, run)
    if author not in AUTHORS:
        raise LabelingRefused(f"author must be one of {list(AUTHORS)}")
    values = state(job_root, run)["values"]
    if label is not None and label not in values:
        raise LabelingRefused(f"label must be one of {values}")
    text = " ".join(str(text or "").split())[:4000]
    if not text:
        raise LabelingRefused("a turn needs text")
    return _append(job.results_dir(job_root) / run / "turns.jsonl",
                   {"at": cal.now_iso(), "author": author, "label": label, "text": text})


def decide(job_root: Path, run: str, *, human_id: str, label: str, meaning: str | None = None,
           keep: bool = False, reason: str = "") -> dict:
    """The human settles one label: keep the wording, or give new wording. A later decision replaces it."""
    job_root = job_root.resolve()
    _require(job_root, human_id)
    _running(job_root, run)
    current = state(job_root, run)
    if label not in current["values"]:
        raise LabelingRefused(f"label must be one of {current['values']}")
    before = next(row["before"] for row in current["labels"] if row["label"] == label)
    wording = before if keep else " ".join(str(meaning or "").split())
    if not wording:
        raise LabelingRefused("give the new wording, or keep the current one")
    return _append(job.results_dir(job_root) / run / "decisions.jsonl", {
        "at": cal.now_iso(), "label": label, "decision": "keep" if wording == before else "change",
        "meaning": wording, "reason": " ".join(str(reason or "").split())[:2000], "human_id": human_id,
    })


def state(job_root: Path, run: str) -> dict:
    """Where one discussion stands: each label's wording before, the human's decision, and what is open."""
    job_root = job_root.resolve()
    folder = job.results_dir(job_root) / run
    before = job.load_mapping(folder / "before.yaml")
    values = [str(v) for v in before.get("labels") or []]
    meanings = before.get("meanings") or {}
    decisions: dict[str, dict] = {}
    for row in _read_jsonl(folder / "decisions.jsonl"):
        decisions[row["label"]] = row
    labels = [{"label": v, "before": meanings.get(v) or "",
               "after": (decisions.get(v) or {}).get("meaning"),
               "decision": (decisions.get(v) or {}).get("decision"),
               "reason": (decisions.get(v) or {}).get("reason") or ""} for v in values]
    ledger = folder / "ledger.yaml"
    return {
        "run": run, "status": _runtime(job_root, run).get("status"), "values": values, "labels": labels,
        "open": [row["label"] for row in labels if row["decision"] is None],
        "turns": len(_read_jsonl(folder / "turns.jsonl")),
        "open_questions": (job.load_mapping(ledger).get("open_questions") or []) if ledger.is_file() else [],
    }


def close(job_root: Path, run: str, *, human_id: str, open_questions: list[str] | tuple[str, ...] = ()) -> dict:
    """Every label settled: write the ledger and, when any wording changed, one meaning revision."""
    job_root = job_root.resolve()
    _require(job_root, human_id)
    _running(job_root, run)
    current = state(job_root, run)
    if current["open"]:
        raise LabelingRefused(f"settle every label first; still open: {', '.join(current['open'])}")
    folder = job.results_dir(job_root) / run
    config_path = job_root / "config.yaml"
    _, meanings_now = _labels(job.load_mapping(config_path))
    if meanings_now != job.load_mapping(folder / "before.yaml").get("meanings"):
        raise LabelingRefused("the meanings changed after this discussion started; start a new one")
    rows = [{"label": r["label"], "before": r["before"], "after": r["after"],
             "changed": r["after"] != r["before"], "reason": r["reason"]} for r in current["labels"]]
    questions = [" ".join(str(q).split()) for q in open_questions if str(q).strip()]
    ledger = job.yaml_bytes({"run": run, "decided_by": human_id, "labels": rows, "open_questions": questions})
    job.write_once(folder / "ledger.yaml", ledger)
    changed = [r["label"] for r in rows if r["changed"]]
    artifacts = [{"path": f"results/{run}/ledger.yaml"}]
    for name in ("turns.jsonl", "decisions.jsonl"):
        if (folder / name).is_file():
            artifacts.append({"path": f"results/{run}/{name}"})
    revision = None
    if changed:
        revision = job.revise_meanings(job_root=job_root, human_id=human_id, run=run, revised_at=cal.now_iso(),
                                       meanings={r["label"]: r["after"] for r in rows})
        artifacts.append({"path": job.page_path(job_root, revision["revision"])})
        artifacts.append({"path": job.page_path(job_root, "config.yaml")})
    runtime = _runtime(job_root, run)
    ticket = job.load_mapping(job.runs_dir(job_root) / f"{run}.yaml")
    outcome = (f"{len(changed)} of {len(rows)} meanings changed ({', '.join(changed)}); confirm the meaning again"
               if changed else f"all {len(rows)} meanings kept")
    cal._write_run(
        job_root, run, operation=OPERATION, phase="P0", episode="meaning", target=ticket["target"],
        commission=ticket["commission"], inputs=ticket["inputs"], worker=ticket["worker"], acceptance=ACCEPTANCE,
        status="complete", started_at=runtime["started_at"], finished_at=cal.now_iso(), outcome=outcome,
        artifacts=artifacts,
    )
    return {**state(job_root, run), "changed": changed, "revision": revision, "outcome": outcome}


def main() -> None:
    parser = argparse.ArgumentParser(description="subjective-label definition-discussion Run")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("start", "say", "decide", "close", "state"):
        p = sub.add_parser(name)
        p.add_argument("--job-root", type=Path, required=True)
        if name != "state":
            p.add_argument("--human-id", required=True)
        if name != "start":
            p.add_argument("--run", required=name != "state")
        if name == "say":
            p.add_argument("--author", choices=AUTHORS, required=True)
            p.add_argument("--text", required=True)
            p.add_argument("--label")
        if name == "decide":
            p.add_argument("--label", required=True)
            p.add_argument("--meaning")
            p.add_argument("--keep", action="store_true")
            p.add_argument("--reason", default="")
        if name == "close":
            p.add_argument("--open-question", action="append", default=[])
    args = parser.parse_args()
    root = args.job_root
    if args.command == "start":
        out = start(root, human_id=args.human_id)
    elif args.command == "say":
        out = say(root, args.run, human_id=args.human_id, author=args.author, text=args.text, label=args.label)
    elif args.command == "decide":
        out = decide(root, args.run, human_id=args.human_id, label=args.label, meaning=args.meaning,
                     keep=args.keep, reason=args.reason)
    elif args.command == "close":
        out = close(root, args.run, human_id=args.human_id, open_questions=args.open_question)
    else:
        out = state(root, args.run or _open_run(root.resolve()) or (_runs(root.resolve()) or [""])[-1])
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
