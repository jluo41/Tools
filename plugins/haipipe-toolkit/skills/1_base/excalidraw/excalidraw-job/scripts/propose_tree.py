"""Propose the Tasks and Runs a Job is missing, each Run numbered by its type's band (asked 261019: "一定要把这些
run 也 propose 好，然后每一个 run 都要排序排好"). See ../ref/propose-tree.md.

    python propose_tree.py <job folder> --plan <plan.yaml>            # dry run: what it would make
    python propose_tree.py <job folder> --plan <plan.yaml> --apply    # make the proposed Tasks and Runs

A proposal is a Run folder with `run.yaml` (`status: proposed`, `run_type`, `says`, `after`) and a stub ticket that
exits with what it still needs; it never has a `result/`. Existing Tasks and Runs are never changed.
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

import yaml

# type: (first number of its band, what it waits for)
BANDS = {"smoke": (1, None), "main": (11, "smoke"), "sweep": (21, "main"), "repeat": (31, "main"),
         "score": (41, "main"), "ablation": (51, "main")}
RUN = re.compile(r"^r(\d+)_")
STATES = {"completed": "✅", "failed": "❌", "running": "🔶", "ready": "⬜", "proposed": "◌"}


def run_type(name: str) -> str:
    """A Run's type from its band (r0x smoke, r1x main, …); older names outside the bands read as their band too."""
    m = RUN.match(name)
    if not m:
        return ""
    n = int(m.group(1))
    return {0: "smoke", 1: "main", 2: "sweep", 3: "repeat", 4: "score", 5: "ablation"}.get(n // 10, "")


def next_number(taken: set[int], kind: str) -> int:
    start = BANDS[kind][0]
    n = start
    while n in taken:
        n += 1
    if n >= start + 9 and kind != "ablation":
        if max(taken, default=0) >= start + 9:                          # older Runs, numbered before the bands, fill
            return max(taken) + 1                                       #   it (b01 j02 t02: r01-r57): after the last;
        raise SystemExit(f"band of {kind} (r{start:02d} to r{start + 8:02d}) is full")   # run.yaml keeps run_type
    return n


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", str(s).lower()).strip("_")


def ticket_stub(task: str, run: str, says: str, needs: str) -> str:
    return (f"#!/usr/bin/env bash\n"
            f"# PROPOSED Run of {task}: {says}\n"
            f"# Not ready: {needs}\n"
            f"# Make it real by writing this ticket and its config, then clear `status: proposed` in run.yaml.\n"
            f"echo \"{run} is proposed, not ready: {needs}\" >&2\nexit 3\n")


def task_face(name: str, t: dict) -> str:
    title = t.get("title") or t.get("asks") or name
    lines = [name, "=" * len(name), "", str(title), "",
             f"develops: {t.get('develops', '')}".rstrip(),
             f"input: {t.get('input', '')}".rstrip(),
             f"output: {t.get('output', '')}".rstrip(),
             "state: ◌ proposed",
             f"proposed: {date.today().isoformat()}", ""]
    if t.get("reuse"):
        lines += [f"Reuse: `{t['reuse']}`, copied in before its first Run can start.", ""]
    lines += ["Proposed by excalidraw-job's propose_tree.py; its Runs are stubs until written.", ""]
    return "\n".join(l for l in lines if l is not None)


def plan_job(job: Path, plan: dict) -> list[tuple[str, Path, str]]:
    """What a plan would make: (kind, path, text) for each new file; existing Tasks and Runs are left alone."""
    out = []
    tasks = {p.name: p for p in job.iterdir() if p.is_dir() and re.match(r"^t\d+_", p.name)}
    for t in plan.get("tasks") or []:
        name = t["name"]
        tdir = tasks.get(name, job / name)
        if name not in tasks:
            out.append(("task", tdir / f"{name}.md", task_face(name, t)))
        rdir = tdir / "runs"
        have = {p.name for p in rdir.iterdir() if p.is_dir()} if rdir.is_dir() else set()
        taken = {int(RUN.match(n).group(1)) for n in have if RUN.match(n)}
        made: dict[str, str] = {}                                       # type -> first Run named in this plan
        for n in sorted(have):                                         # the existing main/smoke a Run waits for
            k = run_type(n)
            made.setdefault(k, n)
        for r in t.get("runs") or []:
            kind = r["type"]
            if kind not in BANDS:
                raise SystemExit(f"{name}: unknown run type {kind!r}; one of {', '.join(BANDS)}")
            if r.get("name") and r["name"] in have:
                continue
            n = next_number(taken, kind)
            taken.add(n)
            run = r.get("name") or f"r{n:02d}_{kind}" + (f"_{slugify(r['slug'])}" if r.get("slug") else "")
            if run in have:
                continue
            after = r.get("after") or made.get(BANDS[kind][1] or "", "")
            made.setdefault(kind, run)
            needs = r.get("needs") or t.get("needs") or (f"copy the worker from {t['reuse']} and write its config"
                                                         if t.get("reuse") else "its worker and config")
            card = {"run": run, "kind": "hard", "type": None, "run_type": kind, "status": "proposed",
                    "says": r.get("says", ""), "after": after or None, "needs": needs,
                    **{k: r[k] for k in ("aim", "why", "settings", "host", "time") if r.get(k)},   # what a yes rests on
                    "scope": None, "ticket": f"{run}.sh", "writes": ["result/"],
                    "proposed": date.today().isoformat()}
            out.append(("run", rdir / run / "run.yaml", yaml.safe_dump(card, sort_keys=False, allow_unicode=True)))
            out.append(("ticket", rdir / run / f"{run}.sh", ticket_stub(name, run, r.get("says", ""), needs)))
    return out


def scope_of(path: Path) -> str:
    """The Task path from the SPACE root (the folder holding Tools/), as run.yaml's scope: is written elsewhere."""
    p = path
    while p != p.parent and not (p / "Tools").exists():
        p = p.parent
    task = path.parents[2]
    return task.relative_to(p).as_posix() if (p / "Tools").exists() else task.as_posix()


def apply(items: list[tuple[str, Path, str]]) -> None:
    for kind, path, text in items:
        path.parent.mkdir(parents=True, exist_ok=True)
        if kind == "run":
            card = yaml.safe_load(text)
            card["scope"] = scope_of(path)
            text = yaml.safe_dump(card, sort_keys=False, allow_unicode=True)
        path.write_text(text)
        if kind == "ticket":
            path.chmod(0o755)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("job", type=Path)
    ap.add_argument("--plan", type=Path, required=True)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    plan = yaml.safe_load(a.plan.read_text()) or {}
    items = plan_job(a.job, plan.get("propose", plan))
    for kind, path, _ in items:
        print(f"{'make' if a.apply else 'would make'} {kind:6s} {path.relative_to(a.job)}")
    if a.apply:
        apply(items)
    print(f"{len(items)} files {'made' if a.apply else 'planned'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
