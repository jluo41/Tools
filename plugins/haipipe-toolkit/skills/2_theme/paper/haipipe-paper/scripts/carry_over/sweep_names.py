#!/usr/bin/env python3
"""sweep_names.py · after the carry-over, sweep a Board's old names out of the files the other scripts skip.

    python sweep_names.py <board> --dry-run     print every file and line it would change; change nothing
    python sweep_names.py <board> --apply       do them; keep each changed file's old text for rollback
    python sweep_names.py <board> --rollback    put the newest sweep's files back exactly

migrate_paper.py, topics_paper.py and rename_tasks.py leave draft/records/, draft/previous/ and Run tickets as
written, so a receipt still resolves through their records. JL's full-sweep rule (AGENTS.md rule 7) wants the
hand-written ones to say the new names too. This script reads the three records the others wrote
(.paper-moves.yaml, .paper-topics-N.yaml, .paper-tasks.yaml) and replaces, longest first:

    A1-Story/StoryA-<desk>-<idea>/StoryA-…  -> studio/sNN-story-<desk>-<idea>/sNN-story-…   (topics record)
    Ba-<desk>-Main/ · Bb-<desk>-Appendix/   -> jNN_v<MMDD>_<desk>/                          (moves + tasks records)
    S-<desk>-Main-<N>-<Title>               -> t0N_<title>                                  (tasks record)

It edits hand-written text only (.md .yaml .yml .toml .sh .py .txt), skips generated and sealed output
(delivery/, board/, results/, passes/, payload/, _archive/, .git) and every line that names the predecessor
Board (a path through `0-paperboard/` or an `_old/` paper keeps its own old names), and leaves board.md's
## Log as written: it narrates the renames themselves. Nothing is committed.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import date
from pathlib import Path

import yaml

TEXT = {".md", ".yaml", ".yml", ".toml", ".sh", ".py", ".txt"}
SKIP = {"delivery", "board", "results", "passes", "payload", "_archive", ".git", "__pycache__", "node_modules"}
PREDECESSOR = re.compile(r"0-paperboard|/_old/|MedJournal")
RECORD = ".paper-sweep.yaml"
KEEP = ".paper-sweep"


def load(path):
    return yaml.safe_load(path.read_text(encoding="utf-8")) if path.is_file() else {}


def token_map(board):
    """old -> new, from the three carry-over records; the version rename is folded into the group renames."""
    tasks = load(board / ".paper-tasks.yaml").get("tokens", {}) or {}
    out = dict(tasks)
    topics = {}
    for rec in sorted(board.glob(".paper-topics-*.yaml")):
        for mv in load(rec).get("moves", []) or []:
            o, n = Path(mv["old"]), Path(mv["new"])
            if o.parent == n.parent and o.suffix == "" and o.name != n.name:   # a topic folder renamed
                topics[o.name] = n.name
    out.update(topics)
    for old, new in (load(board / ".paper-moves.yaml").get("renames", {}) or {}).items():
        if new != "studio":                                   # a desk group: every child moved with it
            out[old] = tasks.get(new, new)
            continue
        # the Story group: only its moved children went to studio/; a child archived before the move
        # (Story01-seed, Story04-narrative-…) is named by where it sits now, under the Board's _archive/
        for child in topics:
            out[f"{old}/{child}"] = f"studio/{topics[child]}"
        for kept in sorted(board.glob("_archive/*/Story*")):
            out.setdefault(f"{old}/{kept.name}", kept.relative_to(board).as_posix())
    return {o: n for o, n in out.items() if o and n and o != n}


def files(board):
    for p in sorted(board.rglob("*")):
        rel = p.relative_to(board)
        if (p.is_file() and p.suffix in TEXT and not p.is_symlink()
                and not any(part in SKIP or part.startswith(".paper-") for part in rel.parts)):
            yield p


def sweep(text, tokens, keep_log):
    pat = re.compile("|".join(re.escape(t) for t in sorted(tokens, key=len, reverse=True)))
    out, changed, in_log = [], [], False
    for i, line in enumerate(text.split("\n")):
        if line.startswith("## "):
            in_log = keep_log and line[3:].strip().lower().startswith("log")
        if in_log or PREDECESSOR.search(line) or not pat.search(line):
            out.append(line)
            continue
        new = pat.sub(lambda m: tokens[m.group(0)], line)
        out.append(new)
        if new != line:
            changed.append((i + 1, line, new))
    return "\n".join(out), changed


def run(board, apply):
    tokens = token_map(board)
    if not tokens:
        sys.exit("stop: no carry-over records (.paper-moves.yaml, .paper-topics-N.yaml, .paper-tasks.yaml) here")
    edits = []
    for p in files(board):
        text = p.read_text(encoding="utf-8", errors="replace")
        new, changed = sweep(text, tokens, keep_log=p == board / "board.md")
        if changed:
            edits.append((p, text, new, changed))
    for p, _, _, changed in edits:
        print(f"{p.relative_to(board)}  ({len(changed)} line(s))")
        for n, a, b in changed[:3]:
            print(f"  {n:>5} - {a.strip()[:150]}\n        + {b.strip()[:150]}")
    lines = sum(len(c) for *_, c in edits)
    if not apply:
        print(f"\n{len(edits)} file(s) · {lines} line(s) · nothing changed (dry run)")
        return
    keep = board / KEEP
    for p, old, new, _ in edits:
        backup = keep / (p.relative_to(board).as_posix() + ".orig")
        backup.parent.mkdir(parents=True, exist_ok=True)
        backup.write_text(old, encoding="utf-8")
        p.write_text(new, encoding="utf-8")
    rec = {"swept": date.today().isoformat(), "tool": "haipipe-paper/scripts/carry_over/sweep_names.py",
           "tokens": tokens, "files": [p.relative_to(board).as_posix() for p, *_ in edits]}
    (board / RECORD).write_text(yaml.safe_dump(rec, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"\n{len(edits)} file(s) · {lines} line(s) swept · record {RECORD}; nothing committed")


def rollback(board):
    rec = load(board / RECORD)
    if not rec:
        sys.exit(f"stop: no {RECORD} to roll back")
    for rel in rec.get("files", []):
        backup = board / KEEP / (rel + ".orig")
        if backup.is_file():
            (board / rel).write_text(backup.read_text(encoding="utf-8"), encoding="utf-8")
    shutil.rmtree(board / KEEP, ignore_errors=True)
    (board / RECORD).rename(board / f".paper-sweep.rolled-back-{date.today().isoformat()}.yaml")
    print(f"rolled back {len(rec.get('files', []))} file(s)")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("board", type=Path)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    g.add_argument("--rollback", action="store_true")
    a = ap.parse_args()
    board = a.board.resolve()
    if a.rollback:
        rollback(board)
    else:
        run(board, a.apply)


if __name__ == "__main__":
    main()
