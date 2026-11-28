"""open_job.py <insight Board> --release question-vN --data data-vM [--previous jNN_…] [--moved code|data|start]

Open one plan-C Job on an insight Board (b11 s00 · s11 · s12, 261007):
`jNN_question-vN-<release slug>_data-vM/` (`job_name`), pinning one Question Book release (board.md
`prototype:`) and one data version (board.md `versions:`). It writes:

    <job>.md                              the Job's face: release, data, state open, moved, previous, and its
                                          `goal:` line, what this release × data version answers (job_goal)
    tNN_<L><NN>_<slug>/tNN_….md           one Task per question of the release: `question:`, its `goal:` (the
                                          question's ask), its answer fields empty until its page is written
    tNN_…/runs/rNN_<segment>/run.sh     one ticket per segment the question is asked on (rNN = the segment's
                                          place in the release's partitions.md), running run_job.py
    tNN_…/runs/rNN_<segment>/run.yaml   the Run's card, planned until its ticket runs

A question with no compute need gets no ticket (its page cites the answers below it). Never overwrites a
file; rerun it after a release adds a question. Prints what it made.
"""
import argparse
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_question as RQ  # noqa: E402

# A Board Job's folder name, read left to right (it reads as question version × data version without
# a lookup): j02_question-v1-example-questions_data-v2. Underscores part its three fields (the
# number, the question version, the data version) and hyphens join the words inside one, as in a Task's tNN_<L><NN>_<slug>.
# The older j01_prototype-p1-basic-questions_data-SMSR2v1 and jNN_pN_<D>vM still read, until rename_code_data.py
# carries their Board over. Groups: number, release, dataset ('' in the new name), version.
JOB_NEW = re.compile(r"^j(\d+)_((?:question|code)-v\d+)(?:-[a-z0-9-]+)?_()(data-v\d+)$")
JOB_OLD = re.compile(r"^j(\d+)_(?:prototype-)?(p\d+)(?:-[a-z0-9-]+)?_(?:data-)?([A-Za-z][A-Za-z0-9]*?)(v\d+)$")


class Either:
    """Two patterns read as one: the first that matches (re has no branch reset, so the groups stay numbered alike)."""

    def __init__(self, *pats):
        self.pats = pats

    def match(self, s):
        return next((m for m in (p.match(s) for p in self.pats) if m), None)

    fullmatch = match


JOB = Either(JOB_NEW, JOB_OLD)


def num(vid: str) -> int:
    """The number of a code or data version id: 2 from question-v2, data-v2, p2 or v2."""
    m = re.search(r"(\d+)$", str(vid or ""))
    return int(m.group(1)) if m else 0


def code_id(rid: str) -> str:
    """A question version as a person reads it: question-v1 (an older p1 reads the same)."""
    return re.sub(r"^(?:p|code-v)(\d+)$", r"question-v\1", str(rid or ""))


def data_id(vid: str) -> str:
    """A data version as a person reads it: data-v1 (an older v1 reads the same)."""
    return re.sub(r"^v(\d+)$", r"data-v\1", str(vid or ""))


def release_slug(rdir: Path) -> str:
    """A release folder's words: `basic-questions` from j01_question-v1_basic-questions ('' for a bare jNN_question-vN)."""
    return rdir.name.split("_", 2)[2] if rdir.name.count("_") >= 2 else ""


def job_name(number: int, release: str, slug: str, dataset: str, data: str) -> str:
    """j01_question-v1-basic-questions_data-v1: the Job's number, its question version and words, its data version (one
    dataset per Board, named in board.md, so the name carries none)."""
    plan = "-".join(x for x in (code_id(release), slug) if x)
    return f"j{int(number):02d}_{plan}_{data_id(data)}"

TICKET = """#!/bin/bash
# run.sh · one hard Run of a plan-C Job: this Task's question on this segment (hai-insight ref/run_job.py).
# The same lines in every ticket; the folder name is the Run (rNN_<segment>).
R="$(cd "$(dirname "$0")" && while [ ! -f env.sh ] && [ "$PWD" != / ]; do cd ..; done; pwd)"
source "$R/env.sh" >/dev/null 2>&1
HERE="$(cd "$(dirname "$0")" && pwd)"
exec "$R/.venv/bin/python" "$R/Tools/plugins/haipipe-toolkit/skills/3_theme/insight/hai-insight/ref/run_job.py" \\
  "$(cd "$HERE/../.." && pwd)" "$(basename "$HERE")"
"""


def _words(rdir: Path, release: str) -> str:
    rface, _ = RQ.front(rdir / f"{rdir.name}.md")
    return str(rface.get("title") or release_slug(rdir).replace("-", " ") or release)


def job_goal(board, jface: dict) -> str:
    """A Board Job's goal line, what its question version × data version answers: `What the example questions (question-v1)
    find on data-v2, all sixteen days`."""
    board = Path(board)
    face, _ = RQ.front(board / "board.md")
    release, data = str(jface.get("release") or ""), str(jface.get("data") or "")
    rdir = board.parent.parent / str(jface.get("prototype") or "")
    words = _words(rdir, release) if rdir.is_dir() else ""
    v = next((v for v in face.get("versions") or [] if str(v.get("version")) == data), {})
    label = str(v.get("label") or "").strip()
    plan = code_id(release)
    return (f"What the {words} ({plan})" if words else f"What {plan}") + \
        f" find{'' if words else 's'} on {data_id(data)}" + (f", {label}" if label else "")


def question_fields(board, jface: dict, qid: str) -> dict:
    """A Board Task's question as the Question Book's question.md holds it (its ask is the Task's goal line)."""
    rdir = Path(board).parent.parent / str(jface.get("prototype") or "")
    rows = (yaml.safe_load((rdir / "release.yaml").read_text()) or {}).get("questions") or {} \
        if (rdir / "release.yaml").is_file() else {}
    row = rows.get(qid)
    return RQ.front((rdir / row["task"]).resolve() / RQ.QFILE)[0] if row else {}


def _write(path, text, made, mode=None):
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    if mode:
        path.chmod(mode)
    made.append(path)


def _front(fields, body):
    return "---\n" + yaml.safe_dump(fields, sort_keys=False, allow_unicode=True) + "---\n\n" + body


def open_job(board, release, data, previous="", moved="start", number=None, name=None, extra=None, require_data=True,
             shift=0):
    board = Path(board).resolve()
    face, _ = RQ.front(board / "board.md")
    proto = board.parent.parent / str(face.get("prototype", ""))
    rdir = next((p for p in sorted(proto.glob("j*_*")) if p.is_dir()          # jNN_question-vN or jNN_question-vN_<slug>
                 and re.match(rf"^j\d+_{release}(_.+)?$", p.name)), None)
    if rdir is None:
        raise SystemExit(f"no release {release} in {proto}")
    if require_data and not any(v.get("version") == data for v in face.get("versions") or []):
        raise SystemExit(f"no data version {data} in {board.name}/board.md versions:")   # a prep Job's head Task makes it
    jobs = sorted(p for p in board.glob("j[0-9][0-9]_*") if p.is_dir() and JOB.match(p.name))
    dataset = str(face.get("dataset", ""))
    job = board / name if name else next((j for j in jobs if JOB.match(j.name).group(2, 4) == (release, data)), None) \
        or board / job_name(number or len(jobs) + 1, release, release_slug(rdir), dataset, data)
    made = []
    plan_words = _words(rdir, release)
    heading = f"{plan_words[:1].upper()}{plan_words[1:]} ({code_id(release)}) on {data_id(data)}"   # the folder, in words
    jface = {**(extra or {}), "release": release, "prototype": str(rdir.relative_to(board.parent.parent)), "data": data,
             "state": "open", "moved": moved, "previous": previous}
    jface["goal"] = job_goal(board, jface)
    _write(job / f"{job.name}.md", _front(jface,
                                          f"# {heading}\n\n{code_id(release)} on {data_id(data)}. "
                                          "Frozen once closed (run-close).\n"), made)
    rows = yaml.safe_load((rdir / "release.yaml").read_text())["questions"]
    partitions = RQ.front(rdir / "partitions.md")[0]["partitions"]
    place = {p["name"]: k for k, p in enumerate(partitions, 1)}
    for qid, row in rows.items():
        qdir = (rdir / row["task"]).resolve()
        q, _ = RQ.front(qdir / RQ.QFILE)
        tdir = job / Path(row["task"]).name
        if shift:                                       # a Job of three versions: t01 is its prep Task (insight_ladder_datajob)
            m = re.match(r"^t(\d+)_(.+)$", tdir.name)
            tdir = job / f"t{int(m.group(1)) + shift:02d}_{m.group(2)}"
        ask = str(q.get("ask") or q.get("question") or "").strip()
        _write(tdir / f"{tdir.name}.md", _front({"question": qid, **({"goal": ask} if ask and not ask.startswith("<") else {}),
                                                 "answer-status": "open", "answer": "", "how-sure": "", "check": ""},
                                                f"# {qid} · {q.get('name') or q.get('question', '')}\n\n"
                                                f"**The ask**: {q.get('ask') or q.get('question', '')}\n\n"
                                                "**Answer**: not written yet (run-write, after its runs).\n"), made)
        if not any(n.get("kind") == "compute" for n in RQ.live_needs(q).values()):
            continue
        for part in RQ.asked_partitions(q, partitions):
            rundir = tdir / "runs" / f"r{place[part]:02d}_{part}"
            _write(rundir / "run.sh", TICKET, made, 0o755)
            _write(rundir / "run.yaml", yaml.safe_dump({
                "run": rundir.name, "kind": "hard", "type": "cross" if part == "cross" else "partition",
                "partition": part, "target": tdir.name, "question": qid, "release": release, "data": data,
                "status": "planned", "passes": 0}, sort_keys=False), made)
    return job, made


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("board")
    ap.add_argument("--release", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--previous", default="")
    ap.add_argument("--moved", default="start")
    a = ap.parse_args()
    job, made = open_job(a.board, a.release, a.data, a.previous, a.moved)
    tickets = sum(p.name == "run.sh" for p in made)
    print(f"{job.name}: {len(made)} made · {tickets} tickets")


if __name__ == "__main__":
    main()
