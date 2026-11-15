"""Where a two-loop labeling Job stands, read from its Task folders: the step a 🧭 meaning or 🛠 expression Task is at,
and which Task the person or the agent works on next. One place, so the workbench page and /haipipe-labeling <Job>
(haipipe-labeling/scripts/start.py) always agree. Nothing here writes.

    meaning     Frame · Prepare · Preferences · Update, loop by loop, until a guideline mNN is signed
    expression  Rewrite · Run · Evaluate · Release, round by round, under the newest signed mNN

A round's report (rNN_evaluate_mNN_eNN/result/round_report.md) says on its first line where the work goes next:
`… → meaning, Loop N` sends wrong labels and rule gaps back to the meaning Task; anything else stays in expression.

    python two_loops.py <Job>
"""
from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
XROLE = (("_rewrite_", "rewrite"), ("_run_", "run"), ("_evaluate_", "evaluate"), ("_release", "release"))
TYPE = re.compile(r"(?m)^task-type:\s*(labeling-meaning|labeling-expression)\b")


def _load_versions():
    spec = importlib.util.spec_from_file_location("labeling_meaning_versions_for_two_loops", HERE / "meaning_versions.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


MV = _load_versions()


def kind(task: Path) -> str:
    """meaning or expression, from the Task face's task-type: line; "" for any other Task."""
    face = Path(task) / f"{Path(task).name}.md"
    m = TYPE.search(face.read_text(encoding="utf-8", errors="ignore")[:3000]) if face.is_file() else None
    return m.group(1).split("-", 1)[1] if m else ""


def expression_runs(task: Path) -> dict:
    """{role: [Runs]} for an expression Task: rewrite, run, evaluate, release. A 🙋 form beside the steps
    (r08_collect_release_…) is never one of them."""
    out = {r: [] for _, r in XROLE}
    for run in MV.runs(task):
        if "_collect_" in run.name:
            continue
        role = next((r for key, r in XROLE if key in run.name), "")
        if role:
            out[role].append(run)
    return out


def task_step(task: Path) -> str:
    """The step a meaning or expression Task opens on: the one that needs the person, else the one that comes next."""
    if kind(task) == "expression":
        xr = expression_runs(task)
        return next((k for k in ("rewrite", "run", "evaluate", "release") if not xr[k]), "release")
    loops = MV.loops(task)
    if any(lp.get("collect") is not None and MV.state(lp["collect"]) == "waiting" for lp in loops):
        return "preferences"
    rec = MV.frame_record(task)
    if not rec or not rec["decisions"]:
        return "frame"
    if loops and (not loops[-1]["map"] and loops[-1].get("collect") is not None
                  and MV.state(loops[-1]["collect"]) == "done"):
        return "update"
    if loops and loops[-1]["map"] and not loops[-1]["approved"]:
        return "update"
    return "prepare"


def waiting(task: Path) -> list[Path]:
    """The Task's Runs that wait for the person (a form to answer)."""
    return [r for r in MV.runs(task) if MV.state(r) == "waiting"]


def sends_back(evaluate: Path | None) -> int:
    """The meaning loop a round's report sends its cards to (its first line `… → meaning, Loop N`), else 0."""
    report = Path(evaluate) / "result" / "round_report.md" if evaluate else None
    if not report or not report.is_file():
        return 0
    route = next((ln for ln in report.read_text(encoding="utf-8", errors="ignore").splitlines()
                  if ln.strip() and not ln.startswith("#")), "")
    m = re.search(r"→\s*meaning(?:,\s*Loop\s*(\d+))?", route)
    if not m:
        return 0
    loop = re.search(r"_m(\d\d)_e\d\d$", Path(evaluate).name)
    return int(m.group(1)) if m.group(1) else (int(loop.group(1)) + 1 if loop else 1)


def _now(task: Path, who: str, do: str) -> dict:
    return {"task": task, "kind": kind(task), "step": task_step(task), "who": who, "do": do}


def job_now(job: Path) -> dict | None:
    """The one next thing in a two-loop Job: {task, kind, step, who, do}, task None once its release is signed.
    None when the Job has no meaning or expression Task (an older building Job)."""
    tasks = sorted(p for p in Path(job).iterdir() if p.is_dir() and re.match(r"^t\d\d_", p.name))
    meaning = next((t for t in tasks if kind(t) == "meaning"), None)
    expression = next((t for t in tasks if kind(t) == "expression"), None)
    if meaning is None and expression is None:
        return None
    if meaning is not None:
        loops = MV.loops(meaning)
        last = loops[-1] if loops else None
        if waiting(meaning):
            return _now(meaning, "person", "answer the form that waits for you; the step opens on it")
        if last and last["map"] and not last["approved"]:
            return _now(meaning, "person", f"read guideline {last['version']} in Update and sign it")
        if MV.approved_meaning(Path(job)) is None or (last and not last["approved"]):
            return _now(meaning, "agent", f"run the meaning Task's next step: /haipipe-labeling interaction {meaning.name}")
    if expression is not None:
        if waiting(expression):
            return _now(expression, "person", "answer the form that waits for you; the step opens on it")
        xr = expression_runs(expression)
        back = sends_back(xr["evaluate"][-1] if xr["evaluate"] else None)
        if meaning is not None and back and not any(lp["n"] >= back for lp in MV.loops(meaning)):
            return _now(meaning, "agent", f"round {xr['evaluate'][-1].name[-3:]} sent cards back: open Loop {back} with "
                                          f"/haipipe-labeling interaction {meaning.name}")
        release = xr["release"][-1] if xr["release"] else None
        if release is not None and MV.state(release) == "done":
            if MV.release_sign(release):
                return {"task": None, "kind": "", "step": "delivery", "who": "person",
                        "do": f"{release.name[-3:]} is released and signed: its final labels are in the Job's Delivery"}
            return _now(expression, "person", f"read release {release.name[-3:]} in Release and sign it")
        return _now(expression, "agent", f"run the next round: /haipipe-labeling expression {expression.name}")
    return _now(meaning, "agent", "the meaning is signed; add an expression Task (task-type: labeling-expression)")


def main(argv: list[str] | None = None) -> int:
    job = Path((argv or sys.argv[1:])[0])
    now = job_now(job)
    print(json.dumps(now and dict(now, task=now["task"] and now["task"].name), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
