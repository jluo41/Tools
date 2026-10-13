"""open_job.py <insight Board> --release pN --data vM [--previous jNN_…] [--moved code|data|start]

Open one plan-C Job on an insight Board (b11 s00 · s11 · s12, 261007):
`jNN_prototype-pN-<release slug>_data-<dataset>vM/` (`job_name`), pinning one Prototype release (board.md
`prototype:`) and one data version (board.md `versions:`). It writes:

    <job>.md                              the Job's face: release, data, state open, moved, previous
    tNN_<L><NN>_<slug>/tNN_….md           one Task per question of the release: `question:`, its answer
                                          fields empty until its page is written (run-write)
    tNN_…/runs/rNN_<partition>/run.sh     one ticket per cut the question is asked on (rNN = the cut's
                                          place in the release's partitions.md), running run_job.py
    tNN_…/runs/rNN_<partition>/run.yaml   the Run's card, planned until its ticket runs

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

# A Board Job's folder name, read left to right (JL 261012: "make the job folder name to be human readable"):
# j01_prototype-p1-basic-questions_data-SMSR2v1. Underscores part its three fields (the number, the Prototype
# release, the data version) and hyphens join the words inside one, as in a Task's tNN_<L><NN>_<slug>. The
# older jNN_pN_<D>vM still reads. Groups: number, release, dataset, version.
JOB = re.compile(r"^j(\d+)_(?:prototype-)?(p\d+)(?:-[a-z0-9-]+)?_(?:data-)?([A-Za-z][A-Za-z0-9]*?)(v\d+)$")


def release_slug(rdir: Path) -> str:
    """A release folder's words: `basic-questions` from j01_p1_basic-questions ('' for a bare jNN_pN)."""
    return rdir.name.split("_", 2)[2] if rdir.name.count("_") >= 2 else ""


def job_name(number: int, release: str, slug: str, dataset: str, data: str) -> str:
    """j01_prototype-p1-basic-questions_data-SMSR2v1: the Job's number, its release and words, its data."""
    plan = "-".join(x for x in (release, slug) if x)
    return f"j{int(number):02d}_prototype-{plan}_data-{dataset}{data}"

TICKET = """#!/bin/bash
# run.sh · one hard Run of a plan-C Job: this Task's question on this cut (haipipe-insight ref/run_job.py).
# The same lines in every ticket; the folder name is the Run (rNN_<partition>).
R="$(cd "$(dirname "$0")" && while [ ! -f env.sh ] && [ "$PWD" != / ]; do cd ..; done; pwd)"
source "$R/env.sh" >/dev/null 2>&1
HERE="$(cd "$(dirname "$0")" && pwd)"
exec "$R/.venv/bin/python" "$R/Tools/plugins/haipipe-toolkit/skills/2_theme/insight/haipipe-insight/ref/run_job.py" \\
  "$(cd "$HERE/../.." && pwd)" "$(basename "$HERE")"
"""


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


def open_job(board, release, data, previous="", moved="start", number=None):
    board = Path(board).resolve()
    face, _ = RQ.front(board / "board.md")
    proto = board.parent.parent / str(face.get("prototype", ""))
    rdir = next((p for p in sorted(proto.glob("j*_*")) if p.is_dir()          # jNN_pN or jNN_pN_<slug>
                 and re.match(rf"^j\d+_{release}(_.+)?$", p.name)), None)
    if rdir is None:
        raise SystemExit(f"no release {release} in {proto}")
    if not any(v.get("version") == data for v in face.get("versions") or []):
        raise SystemExit(f"no data version {data} in {board.name}/board.md versions:")
    jobs = sorted(p for p in board.glob("j[0-9][0-9]_*") if p.is_dir() and JOB.match(p.name))
    dataset = str(face.get("dataset", ""))
    job = next((j for j in jobs if JOB.match(j.name).group(2, 3, 4) == (release, dataset, data)), None) \
        or board / job_name(number or len(jobs) + 1, release, release_slug(rdir), dataset, data)
    made = []
    rface, _ = RQ.front(rdir / f"{rdir.name}.md")
    plan_words = str(rface.get("title") or release_slug(rdir).replace("-", " ") or release)
    heading = f"{plan_words[:1].upper()}{plan_words[1:]} ({release}) on data {dataset}{data}"   # the folder, in words
    _write(job / f"{job.name}.md", _front({"release": release, "prototype": str(rdir.relative_to(board.parent.parent)),
                                           "data": data, "state": "open", "moved": moved, "previous": previous},
                                          f"# {heading}\n\nAnalysis plan {release.replace('p', 'AP', 1)} (release {release}) on data freeze "
                                          f"{data.replace('v', 'F', 1)} (data version {data}). "
                                          "Frozen once closed (run-close).\n"), made)
    rows = yaml.safe_load((rdir / "release.yaml").read_text())["questions"]
    partitions = RQ.front(rdir / "partitions.md")[0]["partitions"]
    place = {p["name"]: k for k, p in enumerate(partitions, 1)}
    for qid, row in rows.items():
        qdir = (rdir / row["task"]).resolve()
        q, _ = RQ.front(qdir / RQ.QFILE)
        tdir = job / Path(row["task"]).name
        _write(tdir / f"{tdir.name}.md", _front({"question": qid, "answer-status": "open", "answer": "", "how-sure": "",
                                                 "check": ""},
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
