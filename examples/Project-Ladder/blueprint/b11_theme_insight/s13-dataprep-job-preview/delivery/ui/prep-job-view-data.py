"""Run: python3 prep-job-view-data.py <a DataPrep Block folder> > prep-job-view-data.js  (needs PyYAML).
Print the s13 preview's data, read from the DataPrep Block and the Boards it serves: its Jobs (one prep version
each), each version's steps (step.md: goal, reads, writes, checks, agreed), and every Board Job that pins the version
(its data version, its t01 Run's line per step, each step's metrics.json, the ready folder it made). Nothing is typed
here; a field the Block lacks stays empty."""
import json
import re
import sys
from pathlib import Path

import yaml

B = Path(sys.argv[1])
INSIGHT = B.parent                                       # <Project>/insight/: the Boards a serves: line names
RUN = {"done": "✅", "ok": "✅", "running": "🏃", "failed": "❗", "refused": "❗"}


def front(f):
    m = re.match(r"(?s)---\n(.*?)\n---", f.read_text(errors="ignore")) if f.is_file() else None
    return (yaml.safe_load(m.group(1)) or {}) if m else {}


def body_line(f):
    t = re.sub(r"(?s)^---\n.*?\n---\n", "", f.read_text(errors="ignore")) if f.is_file() else ""
    paras = [p for p in re.split(r"\n\s*\n", t) if p.strip() and not p.lstrip().startswith("#")]
    return " ".join(paras[0].split()) if paras else ""


board = front(B / "board.md")
boards = [INSIGHT / Path(s).name for s in board.get("serves") or []]


def runs_of(prep: str):
    """Every Board Job that pins this prep version, with its t01 Run's runtime and each step's metrics."""
    out = []
    for b in boards:
        for j in sorted(b.glob("j[0-9][0-9]_*")):
            face = front(j / f"{j.name}.md")
            if face.get("prep") != prep or Path(str(face.get("dataprep", ""))).name != B.name:
                continue
            run = next(iter(sorted(j.glob("t01_*/runs/r*/result/runtime.yaml"))), None)
            rt = yaml.safe_load(run.read_text()) if run else {}
            steps = {}
            for s in rt.get("steps") or []:
                light = run.parent / "steps" / s["step"]                # the first step's light folder holds its card
                m = next((light / f for f in ("metrics.json", "experiment_card.json") if (light / f).is_file()), None)
                steps[s["step"]] = {"mark": RUN.get(s.get("status"), "⬜"), "seconds": s.get("seconds"),
                                    "file": m.name if m else "", "metrics": json.loads(m.read_text()) if m else {}}
            out.append({"board": b.name, "job": j.name[:3], "folder": j.name, "data": face.get("data", ""),
                        "release": face.get("release", ""), "mark": RUN.get(rt.get("status"), "⬜"),
                        "run": run.parent.parent.name if run else "", "ready": face.get("ready", ""), "steps": steps})
    return out


jobs = []
for j in sorted(B.glob("j[0-9][0-9]_*"), reverse=True):
    face = front(j / f"{j.name}.md")
    steps = []
    for t in sorted(j.glob("t[0-9][0-9]_*")):
        s = front(t / "step.md")
        steps.append({"id": t.name[:3], "name": s.get("step", t.name[4:]), "folder": t.name, "goal": s.get("goal", ""),
                      "reads": s.get("reads", ""), "writes": s.get("writes", ""), "checks": s.get("checks") or [],
                      "agreed": str(s.get("agreed") or ""), "about": body_line(t / "step.md")})
    jobs.append({"id": j.name[:3], "prep": face.get("prep", ""), "folder": j.name, "closed": face.get("state") == "closed",
                 "signed": str(face.get("signed") or ""), "hash": face.get("hash", ""), "from": face.get("from") or "",
                 "goal": face.get("goal", ""), "about": body_line(j / f"{j.name}.md"), "steps": steps,
                 "used": runs_of(face.get("prep", ""))})

print("window.PREP = " + json.dumps({"block": B.name, "set": board.get("set", ""), "store": board.get("store", ""),
                                     "serves": [b.name for b in boards], "jobs": jobs},
                                    ensure_ascii=False, indent=0) + ";")
