"""Write a soft Run and its passes: `runs/run-<type>-<target>/` with its card and ticket (haipipe-run,
b03 s21, 261007). The tool that writes `run.yaml` for a soft Run, so no person types the card.

    python soft_run.py new  <scope> --type <type> --target <target> [--skill S] [--agent A]
                            [--signs a,b] [--ask '…'] [--close '…'] [--feeds a,b] [--writes a,b]
    python soft_run.py pass <scope>/runs/run-<type>-<target> --title '…' [--ask '…'] [--summary '…']
                            [--changed a,b] [--date MMDD] [--status done]

A type may be hyphenated (`add-venue`, `freeze-predictions`): the name is `run-<type>-<target>` and
the target is always given, so the name never has to be split. `new` makes the Run once per target (a second `new` for the same type and target is refused: a new
round is a pass). Its name carries no date (JL 261006): a target that looks like a date is refused.
`pass` adds `passes/pNN-<MMDD>/pass.md` (title, ask, summary, what it changed) and updates the card:
`passes`, `status`, `writes`. The scope is any Block, Job or Task folder; `scope:` in the card is
SPACE-relative (the nearest folder above holding env.sh), else null.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

import yaml

TYPE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")      # one word, or hyphenated (add-venue)
TARGET = re.compile(r"^[a-z0-9][a-z0-9_.-]*$")
DATED = re.compile(r"(^|-)(\d{4}|\d{6})(-|$)")      # MMDD or YYMMDD inside the name
STATES = ("planned", "running", "waiting", "done", "failed", "held", "superseded")
FIELDS = ("run", "kind", "type", "scope", "target", "ticket", "skill", "agent", "signs", "status", "passes",
          "writes", "feeds")


def space_root(folder: Path) -> Path | None:
    for p in [folder, *folder.parents]:
        if (p / "env.sh").is_file():
            return p
    return None


def _list(value: str) -> list[str]:
    return [v.strip() for v in (value or "").split(",") if v.strip()]


def read_card(run: Path) -> dict:
    return yaml.safe_load((run / "run.yaml").read_text(encoding="utf-8")) or {}


def write_card(run: Path, card: dict) -> None:
    ordered = {k: card.get(k) for k in FIELDS}
    ordered.update({k: v for k, v in card.items() if k not in ordered})
    (run / "run.yaml").write_text(yaml.safe_dump(ordered, sort_keys=False, allow_unicode=True), encoding="utf-8")


def new(scope: Path, rtype: str, target: str, skill: str = "", agent: str = "", ask: str = "", close: str = "",
        feeds: list[str] | None = None, writes: list[str] | None = None, signs: list[str] | None = None) -> Path:
    if not scope.is_dir():
        raise ValueError(f"{scope}: no such folder")
    if not TYPE.match(rtype):
        raise ValueError(f"type {rtype!r}: lower-case letters and digits, words joined by -")
    if not TARGET.match(target):
        raise ValueError(f"target {target!r}: lower-case letters, digits, _ . -")
    if DATED.search(target):
        raise ValueError(f"target {target!r} looks like a date: a soft Run's name has none, its passes do")
    name = f"run-{rtype}-{target}"
    run = scope / "runs" / name
    if run.exists():
        raise ValueError(f"{name} exists: a new round on the same target is a pass")
    root = space_root(scope.resolve())
    run.mkdir(parents=True)
    ticket = run / f"{name}.md"
    ticket.write_text("\n".join([f"# {name}", "", f"target: {target}", f"ask: {ask or '<what this Run is asked to do>'}",
                                 f"close: {close or '<what settles it>'}", ""]), encoding="utf-8")
    write_card(run, {"run": name, "kind": "soft", "type": rtype,
                     "scope": scope.resolve().relative_to(root).as_posix() if root else None,
                     "target": target, "ticket": ticket.name, "skill": skill or None, "agent": agent or None,
                     "signs": signs or None, "status": "planned", "passes": [], "writes": writes or [], "feeds": feeds or []})
    return run


def add_pass(run: Path, title: str, ask: str = "", summary: str = "", changed: list[str] | None = None,
             date: str = "", status: str = "done") -> Path:
    if not (run / "run.yaml").is_file():
        raise ValueError(f"{run}: no run.yaml; make the Run with `new` first")
    if status not in STATES:
        raise ValueError(f"status {status!r}: one of {' · '.join(STATES)}")
    date = date or dt.date.today().strftime("%m%d")
    if not re.fullmatch(r"\d{4}", date):
        raise ValueError(f"date {date!r}: MMDD")
    passes = run / "passes"
    nums = [int(m.group(1)) for p in passes.iterdir() for m in [re.match(r"^p(\d+)-", p.name)] if m] \
        if passes.is_dir() else []
    folder = passes / f"p{(max(nums) + 1 if nums else 1):02d}-{date}"
    folder.mkdir(parents=True)
    changed = changed or []
    body = [f"# {title}", "", "## Ask", "", ask or "<the session's ask>", "", "## Summary", "",
            summary or "<what it did>", "", "## Changed", ""] + [f"- `{c}`" for c in changed] + \
           ([] if changed else ["<nothing>"]) + [""]
    (folder / "pass.md").write_text("\n".join(body), encoding="utf-8")
    card = read_card(run)
    card["passes"] = list(card.get("passes") or []) + [folder.name]
    card["status"] = status
    card["writes"] = list(dict.fromkeys(list(card.get("writes") or []) + changed))
    write_card(run, card)
    return folder


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("new")
    p.add_argument("scope", type=Path)
    p.add_argument("--type", required=True)
    p.add_argument("--target", required=True)
    for k in ("skill", "agent", "signs", "ask", "close", "feeds", "writes"):
        p.add_argument(f"--{k}", default="")
    p = sub.add_parser("pass")
    p.add_argument("run", type=Path)
    p.add_argument("--title", required=True)
    for k in ("ask", "summary", "changed", "date"):
        p.add_argument(f"--{k}", default="")
    p.add_argument("--status", default="done")
    a = ap.parse_args()
    try:
        if a.cmd == "new":
            out = new(a.scope, a.type, a.target, a.skill, a.agent, a.ask, a.close, _list(a.feeds), _list(a.writes),
                      _list(a.signs))
        else:
            out = add_pass(a.run, a.title, a.ask, a.summary, _list(a.changed), a.date, a.status)
    except ValueError as err:
        print(f"refused: {err}", file=sys.stderr)
        return 2
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
