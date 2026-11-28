"""insight_ladder's `run` command: the level a folder is, a soft Run's card (runs/run-<type>-<target>/) and a Task's
hard Runs, one per segment (runs/rNN_<segment>/)."""

from __future__ import annotations

import sys
from pathlib import Path

from insight_ladder_base import (
    SOFT, VERSION, JOB, TASK, PREP, STEP, JOB3, PREPTASK, LEVEL, TYPES, ALONE, DEFAULT_TARGET, RUN_TYPES, Plan, front,
    dump_yaml,
    project_of, face, face_kind)
import open_job as OJ  # noqa: E402  (ref/, put on the path by insight_ladder_base)


# ── a Run ───────────────────────────────────────────────────────────────────────────────────────
def level_of(folder: Path) -> str:
    name = folder.name
    if (folder / "board.md").is_file():
        kind = face_kind(folder)
        if kind:
            return kind
    if VERSION.match(name) and face_kind(folder.parent) == "prototype":
        return "version"
    if (JOB.match(name) or JOB3.match(name)) and face_kind(folder.parent) == "board":
        return "job"
    if PREPTASK.match(name) and JOB3.match(folder.parent.name) and face_kind(folder.parent.parent) == "board":
        return "preptask"
    if PREP.match(name) and face_kind(folder.parent) == "dataprep":
        return "prep"
    if STEP.match(name) and PREP.match(folder.parent.name) and face_kind(folder.parent.parent) == "dataprep":
        return "step"
    if TASK.match(name):                       # an older Board Job's name (j01_p1_<D>v1) fits VERSION: ask the face above
        above = face_kind(folder.parent.parent)
        if VERSION.match(folder.parent.name) and above == "prototype":
            return "question"
        if (JOB.match(folder.parent.name) or JOB3.match(folder.parent.name)) and above == "board":
            return "task"
    sys.exit(f"not an insight Block, version, Job, Task, prep version or step folder: {folder}")


def _default_target(folder: Path, level: str, rtype: str) -> str:
    if (level, rtype) in DEFAULT_TARGET:
        return DEFAULT_TARGET[(level, rtype)]
    name = folder.name
    if level == "version":
        return VERSION.match(name).group(2)                        # question-v2
    if level == "dataprep":                                        # the next prep version: prep-v3
        return f"prep-v{sum(1 for p in folder.iterdir() if p.is_dir() and PREP.match(p.name)) + 1}"
    if level == "prep":
        return PREP.match(name).group(2)                           # prep-v2
    if level == "step":
        return name.split("_", 1)[0]                               # t01
    if level == "question":
        return TASK.match(name).group(2).lower()                   # k01
    if level == "job":
        return name.split("_", 1)[0]                               # j03
    if level in ("task", "preptask"):
        return name.split("_", 1)[0]                               # t03
    sys.exit(f"a {level} Run needs its target: run {name} {rtype} <target>")


def _partitions(task: Path) -> list[dict]:
    jf = face(task.parent)
    ver = project_of(task.parent.parent) / str(jf.get("prototype", ""))
    parts = front(ver / "partitions.md")[0].get("partitions") or []
    return parts                                      # rNN = the segment's place in partitions.md (open_job.py)


def hard_run(task: Path, which: str, plan: Plan) -> list[Path]:
    parts = _partitions(task)
    names = [p["name"] for p in parts]
    if not names:
        sys.exit(f"{task.parent.name}'s release has no segments (partitions.md)")
    pick = names if which == "all" else [which]
    for p in pick:
        if p not in names:
            sys.exit(f"{p} is not a segment of this release: {', '.join(names)}")
    jf, qid = face(task.parent), TASK.match(task.name).group(2)
    out = []
    for p in pick:
        k = names.index(p) + 1
        path = task / "runs" / f"r{k:02d}_{p}"
        cross = "of" in parts[k - 1]
        plan.write(path / "run.sh", OJ.TICKET)               # the same lines in every ticket (ref/open_job.py)
        if not plan.dry and (path / "run.sh").exists():
            (path / "run.sh").chmod(0o755)
        plan.write(path / "run.yaml", dump_yaml(
            {"run": path.name, "kind": "hard", "type": "cross" if cross else "partition", "partition": p,
             "target": task.name, "question": qid, "script": jf.get("hash", ""), "release": jf.get("release", ""),
             "data": jf.get("data", ""), "status": "planned", "passes": 0}))
        out.append(path)
    return out


def run(folder: Path, rtype: str, target: str, plan: Plan, again: bool = False) -> list[Path]:
    level = level_of(folder)
    if (level, rtype) not in TYPES:
        sys.exit(f"run-{rtype} does not run at the {level} level; its run types: {RUN_TYPES[level]}")
    skill, agent, signs, hard = TYPES[(level, rtype)]
    if hard and level == "preptask":                           # its one Run, made with the Job (insight_ladder.py job --prep)
        return sorted(r for r in (folder / "runs").glob("r[0-9][0-9]_*") if r.is_dir())
    if hard:
        return hard_run(folder, target or "all", plan)
    if level == "task" and rtype == "write":
        letter = TASK.match(folder.name).group(2)[0]          # an Executive page is the door's own: no level skill
        skill = "hai-insight" if letter == "X" else f"hai-insight-{LEVEL[letter]}"
    if (level, rtype) in ALONE:
        path = folder / "runs" / f"run-{rtype}"
        if not path.exists() and not plan.dry:
            path.mkdir(parents=True)
            SOFT.write_card(path, {"run": path.name, "kind": "soft", "type": rtype, "scope": None, "target": "every Job",
                                   "ticket": None, "skill": skill, "agent": agent, "signs": [signs], "status": "planned",
                                   "passes": [], "writes": [], "feeds": []})
        plan.made.append(path / "run.yaml")
        return [path]
    target = (target or _default_target(folder, level, rtype)).lower()
    path = folder / "runs" / f"run-{rtype}-{target}"
    if path.exists():
        return [path]
    plan.made.append(path / "run.yaml")
    if not plan.dry:
        SOFT.new(folder, rtype, target, skill=skill, agent=agent, signs=[signs])
    return [path]
