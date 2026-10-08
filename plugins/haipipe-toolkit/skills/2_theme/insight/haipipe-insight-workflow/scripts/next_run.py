"""next_run.py <insight folder> · where it stands on the ladder and which Run is next (b11 s21 phase 2).

    python next_run.py <Prototype | release | insight Board | Job | Task>

Reads the folder's files only (faces, release.yaml, board.md, run.yaml cards) and prints its state and the next
Run, by the gates in ref/run-cards.md § Gates. It never runs or writes anything: a person or an agent presses the
button the card names. Exit 0; 1 when the folder is not an insight folder.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location(
    "insight_ladder", HERE.parents[1] / "haipipe-insight" / "scripts" / "insight_ladder.py")
IL = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(IL)
LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)   # the C loader when built: a Job has a run.yaml per cut


def _card(run_dir: Path) -> dict:
    p = run_dir / "run.yaml"
    return (yaml.load(p.read_text(encoding="utf-8"), Loader=LOADER) or {}) if p.is_file() else {}


def _done(status) -> bool:
    return str(status) in ("ok", "done", "closed", "refused")


def release_state(ver: Path) -> tuple[str, str]:
    face = IL.face(ver)
    rel = IL.VERSION.match(ver.name).group(2)
    if str(face.get("state")) == "closed":
        return f"{rel} signed {face.get('signed', '')}, frozen", "a Board runs it: run-add-j<NN> on the insight Board"
    local = {q: (ver / row["task"]).resolve() for q, row in (IL.release(ver).get("questions") or {}).items()
             if (ver / row["task"]).resolve().parent == ver.resolve()}
    if not local and not (IL.release(ver).get("questions") or {}):
        return f"{rel} open, no question yet", f"run-ask-<l><nn> (or run-triage-proposals-{rel})"
    for q, task in local.items():
        fm = IL.front(task / "question.md")[0]
        if not fm.get("needs"):
            return f"{rel} open; {q} has no evidence plan", f"run-plan-evidence-{q.lower()}"
        if not str(fm.get("agreed", "")).startswith("✅"):
            return f"{rel} open; {q}'s needs not agreed", f"run-review-plan-{q.lower()}"
        if not list((task / "scripts").glob("*.py")) and any(
                (n or {}).get("kind") == "compute" for n in (fm.get("needs") or {}).values()):
            return f"{rel} open; {q} has no script", f"run-write-script-{q.lower()}"
    parts = IL.front(ver / "partitions.md")[0].get("partitions") or []
    if not any(p.get("name") == "full" for p in parts) or any("<" in str(p.get("name")) for p in parts):
        return f"{rel} open; the cuts are not set", f"run-set-cuts-{rel}"
    return f"{rel} open; every question agreed, the cuts set", f"run-sign-release-{rel} (a person signs)"


def prototype_state(proto: Path) -> tuple[str, str]:
    vers = IL.versions(proto)
    open_props = [p for p in (proto / "proposals").glob("*.md")
                  if p.name != "README.md" and IL.front(p)[0].get("state", "open") == "open"]
    if not vers:
        return "no release yet", "run-open-version-p1"
    state, nxt = release_state(vers[-1])
    if str(IL.face(vers[-1]).get("state")) == "closed":
        n = int(IL.VERSION.match(vers[-1].name).group(2)[1:]) + 1
        taken = [p for p in (proto / "proposals").glob("*.md")
                 if str(IL.front(p)[0].get("taken-in", "")) == f"p{n}"]
        if taken:
            return f"{state}; {len(taken)} proposals taken into p{n}", f"run-open-version-p{n}, then apply them"
        if open_props:
            return f"{state}; {len(open_props)} open proposals", f"run-triage-proposals-p{n}, then run-open-version-p{n}"
    return state, nxt


def task_state(task: Path) -> tuple[str, str]:
    t = task.name.split("_", 1)[0]
    hard = [_card(r) for r in sorted((task / "runs").glob("r[0-9][0-9]_*"))] if (task / "runs").is_dir() else []
    waiting = [c.get("run") for c in hard if not _done(c.get("status"))]
    if waiting:
        return f"{len(hard) - len(waiting)} of {len(hard)} cuts run", f"{waiting[0]} (its run.sh)"
    face = IL.face(task)
    if str(face.get("answer-status", "open")) != "answered":
        return "every cut run; the page not written", f"run-write-{t}"
    if not str(face.get("check", "")).startswith("✅"):
        return "the page written, not checked", f"run-check-{t} (another agent)"
    return "answered and checked", "-"


def job_state(job: Path) -> tuple[str, str]:
    face = IL.face(job)
    jid = job.name.split("_", 1)[0]
    if str(face.get("state")) == "closed":
        return f"{jid} closed, frozen", "-"
    tasks = [t for t in sorted(job.iterdir()) if t.is_dir() and IL.TASK.match(t.name)]
    todo = [(t, task_state(t)) for t in tasks]
    todo = [(t, s) for t, s in todo if s[1] != "-"]
    if todo:
        t, (st, nxt) = todo[0]
        launched = (job / "runs").is_dir() and any((job / "runs").glob("run-launch-*"))
        if not launched and st.endswith("cuts run"):
            return f"{jid} open; {len(todo)} of {len(tasks)} questions not done, not launched", f"run-launch-{jid}"
        return f"{jid} open; {len(todo)} of {len(tasks)} questions not done ({t.name}: {st})", nxt
    prev = str(face.get("previous") or "")
    compared = (job / "reports").is_dir() and any((job / "reports").glob("vs-*.md"))
    if prev and not compared:
        return f"{jid} open; every page checked, not compared", f"run-compare-{prev.split('_', 1)[0]}"
    return f"{jid} open; every page checked" + (", compared" if prev else ""), f"run-close-{jid} (a person signs)"


def board_state(board: Path) -> tuple[str, str]:
    fm = IL.front(board / "board.md")[0]
    if not fm.get("versions"):
        return "no data version yet", "run-add-version-v1"
    jobs = IL.jobs(board)
    if not jobs:
        return f"{len(fm['versions'])} data versions, no Job yet", "run-add-j01"
    last = jobs[-1]
    st, nxt = job_state(last)
    if nxt == "-":
        proto = IL.project_of(board) / str(fm.get("prototype", ""))
        signed = [v for v in IL.versions(proto) if str(IL.face(v).get("state")) == "closed"]
        pairs = {(IL.JOB.match(j.name).group(2), IL.JOB.match(j.name).group(4)) for j in jobs}
        newest_rel = IL.VERSION.match(signed[-1].name).group(2) if signed else ""
        newest_data = str(fm["versions"][-1].get("version"))
        lrel, ldata = IL.JOB.match(last.name).group(2), IL.JOB.match(last.name).group(4)
        if newest_data != ldata and (lrel, newest_data) not in pairs:
            return f"{st}; data {newest_data} is new", f"run-add-j{len(jobs) + 1:02d} ({lrel} on {newest_data}: data moved)"
        if newest_rel and newest_rel != lrel and (newest_rel, ldata) not in pairs:
            return f"{st}; release {newest_rel} is signed", f"run-add-j{len(jobs) + 1:02d} ({newest_rel} on {ldata}: code moved)"
        return f"{st}; the newest pair has run", "run-coverage, then the Board's questions"
    return f"{last.name}: {st}", nxt


def state(folder: Path) -> tuple[str, str] | None:
    """(state, next Run) of an insight folder, or None when the folder is not one (a caller shows nothing)."""
    try:
        level = IL.level_of(folder.resolve())
    except SystemExit:
        return None
    return {"prototype": prototype_state, "version": release_state, "board": board_state, "job": job_state,
            "task": task_state}.get(level, lambda f: (f"a {level}", "its own Runs (ref/run-cards.md)"))(folder.resolve())


def main(argv=None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if len(args) != 1:
        print(__doc__)
        return 2
    found = state(Path(args[0]))
    if found is None:
        print(f"{args[0]}: not an insight Prototype, release, Board, Job or Task folder")
        return 1
    print(f"state  {found[0]}\nnext   {found[1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
