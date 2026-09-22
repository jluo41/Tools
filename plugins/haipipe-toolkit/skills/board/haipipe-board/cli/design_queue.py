#!/usr/bin/env python3
"""🎨 design_queue · run the Design agent queue of one DesignBoard from a terminal.

    python3 design_queue.py <board dir> --list
    python3 design_queue.py <board dir> --run [--limit N] [--dry-run]

--list  prints every planned Generate / Verify run record across the board's
        Design Folders, and every open draft request (a task whose register is
        short of the designs the Brief asks for).
--run   for each planned run record, in order: names the worker on the record
        (designer-cli-NN / reviewer-cli-NN), dispatches `claude -p` with the
        haipipe-designer-agent brief, then closes the run with the records
        check (`design_actions.complete_run`): complete with the next route, or
        failed carrying the check's own words. A verify never runs in the same
        dispatch as the generate it judges.

A planned run whose pinned files changed after it was queued (an insight page
edited since) is skipped with the names of the files; the person clicks
"Queue again" on the Page level, which replaces it with a fresh run.

Human steps (Release, Adopt, Queue again) are never taken here; a person clicks
them on the Page level. Draft requests are listed, not fulfilled: a Claude
session drafts the register from the request file, through
`design_actions.add_item`.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parents[3] / "servers" / "_host"))  # the `live` namespace

from live import design_actions as acts  # noqa: E402
from live.designboard import DESIGN_GROUP, is_design_board  # noqa: E402
from live.design import design_snapshot  # noqa: E402

AGENT_DOC = HERE.parents[2] / "design" / "haipipe-design" / "agents" / "haipipe-designer-agent.md"
UNIT_SKILL = HERE.parents[2] / "design" / "haipipe-design-unit" / "SKILL.md"


def folders(board: Path) -> list[Path]:
    group = board / DESIGN_GROUP
    return sorted(p for p in group.iterdir() if p.is_dir() and (p / f"{p.name}.md").is_file()) if group.is_dir() else []


def planned(board: Path) -> list[dict]:
    rows = []
    for folder in folders(board):
        rows += acts.planned_runs(folder)
    return rows


def drafts(board: Path) -> list[dict]:
    out = []
    for folder in folders(board):
        req = acts.open_draft_request(folder, folder.name)
        if req:
            out.append({"folder": folder.as_posix(), "items": req["items"], "asked_by": req["asked_by"]})
    return out


def brief_for(row: dict, actor: str) -> str:
    op = row["operation"]
    role = "designer" if op == "generate" else "independent reviewer"
    return (
        f"You are the {role} `{actor}` for one Design Run record.\n"
        f"Read the agent contract at {AGENT_DOC} and load {UNIT_SKILL} completely.\n"
        f"Run record: {row['ticket']}\nDesign Folder: {row['folder']}\n"
        f"Operation: {op}. Write only results/{row['run']}/ (content, checks.yaml, result.yaml) with the v2 "
        "result schema, pinning the run record's sha256 and the config's sha256. "
        + ("Do not read any generate discussion; judge the draft only against the frozen criteria.\n" if op == "verify"
           else "Read the frozen design_intent first; never back-fill the bet after seeing the draft.\n")
        + "Do not touch runtime.yaml, the register, or any other file. Return the verdict and the checks in text."
    )


def dispatch(row: dict, actor: str, dry_run: bool) -> tuple[int, str]:
    cmd = ["claude", "-p", brief_for(row, actor), "--permission-mode", "acceptEdits",
           "--add-dir", row["folder"], "--output-format", "text"]
    if dry_run:
        return 0, "dry-run: " + " ".join(c if " " not in c else "'…'" for c in cmd)
    if shutil.which("claude") is None:
        return 127, "claude CLI not on PATH; dispatch the run record from a Claude session instead"
    done = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
    return done.returncode, (done.stdout or "") + (done.stderr or "")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("board")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    board = Path(args.board).resolve()
    if not is_design_board(board):
        print(f"not a DesignBoard: {board}")
        return 2
    rows = planned(board)
    reqs = drafts(board)
    if args.list or not args.run:
        print(f"{len(rows)} planned run(s) · {len(reqs)} open draft request(s)")
        for r in rows:
            print(f"  {r['operation']:9s} {Path(r['folder']).name}/{r['run']}  item {r['item']}")
        for q in reqs:
            print(f"  draft     {Path(q['folder']).name}  {q['items']} item(s) asked by {q['asked_by']}")
        return 0
    n = 0
    for i, row in enumerate(rows, 1):
        if args.limit and n >= args.limit:
            break
        actor = f"{'designer' if row['operation'] == 'generate' else 'reviewer'}-cli-{i:02d}"
        folder = Path(row["folder"])
        changed = acts.stale_inputs(folder, row["run"])
        if changed:
            print(f"⏭ {row['run']} · changed since it was queued: {', '.join(changed)} · "
                  "click Queue again on the page")
            continue
        if not args.dry_run:
            acts.name_worker(folder, row["run"], actor)
        code, text = dispatch(row, actor, args.dry_run)
        print(f"▶ {row['run']} · {actor} · exit {code}")
        if args.dry_run:
            print("  " + text[:200])
            continue
        try:
            receipt = acts.complete_run(folder, row["run"])
            print(f"  {receipt['status']} · verdict {receipt['verdict'] or '—'} · route {receipt['route']}"
                  + (f" · {'; '.join(receipt['problems'])}" if receipt["problems"] else ""))
            n += 1
        except acts.ActionError as exc:
            print(f"  not closed: {exc}")
            if not (folder / "results" / row["run"] / "result.yaml").is_file():
                back = acts.release_worker(folder, row["run"])
                print(f"  put back in the queue · lost worker {back['lost']}")
                if text.strip():
                    print("  worker said: " + text.strip().splitlines()[-1][:160])
                break          # a dead worker usually means no capacity: stop instead of burning the queue
    snap_items = sum(len(design_snapshot(f / f"{f.name}.md", board)["items"]) for f in folders(board))
    print(f"done · {n} run(s) closed · {snap_items} item(s) on the board")
    return 0


if __name__ == "__main__":
    sys.exit(main())
