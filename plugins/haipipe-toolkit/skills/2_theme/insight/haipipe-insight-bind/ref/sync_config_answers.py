#!/usr/bin/env python3
"""sync_config_answers — each called task config lists the evidence needs it serves.

Reads every answering page of one InsightBoard: its `answers.yaml` (need →
ticket) and the page tickets in `runs/`, follows each ticket to the task
ticket it execs, and so to that run's config (`scripts/config/<run>.yaml`).
Then it rewrites the config's `answers:` line to the need ids bound to it,
`answers: [QI4.E1, QK2.E1]`, keeping any trailing comment. While a board is
being backfilled, a bare question id already on the line (`QI4`) is kept until
some need of that question is bound anywhere on the board; from then on only
need ids are listed. Configs no ticket calls are left alone. (haipipe-insight
ref/evidence-needs.md § 2)

    sync_config_answers.py <board> [--check]

--check writes nothing and exits 1 when any config would change.
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

EXEC = re.compile(r'exec\s+"\$\{PAGE\}/([^"]+?\.sh)"')
ANSWERS = re.compile(r"(?m)^answers:\s*\[[^\]\n]*\](.*)$")
NEED = re.compile(r"^Q[DIKW]\d+\.E\d+$")
LEVEL_ORDER = {"D": 0, "I": 1, "K": 2, "W": 3}


def task_config(page_dir: Path, ticket: Path):
    m = EXEC.search(ticket.read_text(encoding="utf-8"))
    if not m:
        return None
    task_ticket = (page_dir / m.group(1)).resolve()
    config = task_ticket.parent.parent / "scripts" / "config" / f"{task_ticket.stem}.yaml"
    return config if config.is_file() else None


def collect(board: Path):
    called, bound = {}, {}
    for page_dir in sorted(p for p in board.glob("*/*/") if (p / "runs").is_dir()):
        tickets = {t.stem: task_config(page_dir, t) for t in sorted((page_dir / "runs").glob("run_*.sh"))}
        for cfg in tickets.values():
            if cfg is not None:
                called.setdefault(cfg, set())
        amap = page_dir / "answers.yaml"
        data = (yaml.safe_load(amap.read_text(encoding="utf-8")) or {}) if amap.is_file() else {}
        for qid, needs in data.items():
            for eid, b in (needs or {}).items():
                if not isinstance(b, dict) or "refused" in b:
                    continue
                for t in ([b["ticket"]] if b.get("ticket") else []) + list(b.get("tickets") or []):
                    if tickets.get(t) is not None:
                        bound.setdefault(tickets[t], set()).add(f"{qid}.{eid}")
    for cfg, ids in bound.items():
        called.setdefault(cfg, set()).update(ids)
    return called


def order(need):
    q, e = need.split(".")
    return (LEVEL_ORDER[q[1]], int(q[2:]), int(e[1:]))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("board", type=Path)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    if not (a.board / "0-MT-meta").is_dir():
        print(f"{a.board}: not an InsightBoard", file=sys.stderr)
        return 2
    changed = 0
    calls = collect(a.board)
    bound_q = {n.split(".")[0] for ids in calls.values() for n in ids}   # questions bound anywhere
    for cfg, ids in sorted(calls.items()):
        text = cfg.read_text(encoding="utf-8")
        m = ANSWERS.search(text)
        old = re.findall(r"Q[DIKW]\d+(?:\.E\d+)?", m.group(0).split("#", 1)[0]) if m else []
        legacy = {q for q in old if "." not in q and q not in bound_q}        # not yet backfilled
        keep = sorted(ids, key=order) + sorted(legacy, key=lambda q: (LEVEL_ORDER[q[1]], int(q[2:])))
        line = "answers: [" + ", ".join(keep) + "]"
        new = (text[:m.start()] + line + m.group(1) + text[m.end():]) if m else line + "\n" + text
        if new != text:
            changed += 1
            print(f"{'would update' if a.check else 'updated'} {cfg.parent.parent.parent.name}/{cfg.name}: {line}")
            if not a.check:
                cfg.write_text(new, encoding="utf-8")
    print(f"{changed} config(s) {'out of sync' if a.check else 'updated'}")
    return 1 if (a.check and changed) else 0


if __name__ == "__main__":
    sys.exit(main())
