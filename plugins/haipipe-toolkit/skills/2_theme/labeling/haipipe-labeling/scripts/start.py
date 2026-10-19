#!/usr/bin/env python3
"""/haipipe-labeling <Job>: open the workbench on the step a labeling Job is at, and say where it stands.

A labeling Job (`jNN_<dataset>_<label>/`) holds Tasks of five types, read from each face's `task-type:` line
(b15 s13): items · ground truth · building · scanning · score. The work starts at the items Task (b15 s41: describe →
items → embed) and goes on to building, then scanning. This script reads the Job from disk, finds the first
Task with work left, opens the workbench on that Task's tab (through the workbench's own /wb, which starts or
reuses the SPACE's host), and prints the Job's ladder with the one next thing and who does it. It writes nothing.

    python start.py <Job or one of its Tasks> [--no-open] [--json]
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
import webbrowser
from pathlib import Path
from urllib.parse import quote

HERE = Path(__file__).resolve().parent
LABELING = HERE.parents[1]                                     # skills/2_theme/labeling
WB = LABELING.parents[1] / "1_base" / "workbench" / "workbench" / "cli" / "wb.py"
TYPES = (("items", "📦", ("items", "data")), ("ground_truth", "📏", ("raw",)),
         ("building", "🏗", ("labeling-building", "labeling")), ("scanning", "🔍", ("labeling-scanning", "labeling")),
         ("score", "📊", ("eval",)))


def engine():
    spec = importlib.util.spec_from_file_location("labeling_items_task", LABELING / "engine" / "items_task.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def job_of(path: Path) -> Path:
    path = path.resolve()
    for p in (path, *path.parents):
        if re.match(r"^j\d\d_", p.name):
            return p
    raise SystemExit(f"no labeling Job (jNN_<dataset>_<label>/) at or above {path}")


def tasks(job: Path) -> list:
    out = []
    for t in sorted(job.glob("t[0-9][0-9]_*/")):
        face = t / f"{t.name}.md"
        text = face.read_text(encoding="utf-8", errors="ignore")[:3000] if face.is_file() else ""
        m = re.search(r"(?m)^task-type:\s*([\w-]+)", text)
        types = [n for n, _, lines in TYPES if m and m.group(1) in lines]
        title = re.search(r"(?m)^#\s+(.+)$", text)
        out.append({"task": t, "types": types, "title": title.group(1).strip() if title else t.name,
                    "icon": " + ".join(i for n, i, _ in TYPES if n in types) or "·"})
    return out


def open_url(root: Path, task: Path, tab: str, space: str, no_open: bool) -> str:
    """The SPACE's host, started or reused by /wb, and the link to one tab of one Task."""
    rel = task.relative_to(root).as_posix()
    got = subprocess.run([sys.executable, str(WB), "--no-open", "--json", rel], cwd=root, capture_output=True,
                         text=True)
    try:
        port = json.loads(got.stdout)["port"]
    except (ValueError, KeyError):
        raise SystemExit("the workbench did not start: " + (got.stderr.strip()[-400:] or got.stdout.strip()[-400:]))
    url = (f"http://127.0.0.1:{port}/_board/workbench?path={quote(rel)}&theme=labeling"
           f"&space={quote(space)}&sub={quote(tab)}")
    if not no_open:
        webbrowser.open(url)
    return url


def start(path: Path, no_open: bool = False) -> dict:
    IT = engine()
    job = job_of(path)
    root = IT.space_root(job)
    ladder = tasks(job)
    out = {"job": job.relative_to(root).as_posix(), "tasks": [], "now": None}
    items = next((t for t in ladder if t["types"] == ["items"]), None)
    for t in ladder:
        state = ""
        if t is items:
            n = IT.next_step(t["task"], settle_runs=False)
            done = [op for op in ("describe", "items", "embed") if IT.latest(t["task"], op)]
            state = f"{len(done)} of 3 steps done" if n["step"] != "done" else "done"
        out["tasks"].append({"task": t["task"].name, "types": t["types"], "title": t["title"], "icon": t["icon"],
                             "state": state})
    if items is not None:
        n = IT.next_step(items["task"], settle_runs=False)
        if n["step"] != "done":
            out["now"] = {"task": items["task"].name, "type": "items", "step": n["step"], "tab": n["tab"],
                          "who": n["who"], "do": n["do"], "run": n.get("run"), "note": n.get("note"),
                          "data": n["data"], "files": n["files"]}
            out["url"] = open_url(root, items["task"], n["tab"], "Work Details", no_open)
            return out
    building = next((t for t in ladder if "building" in t["types"]), None)
    if building is not None:
        out["now"] = {"task": building["task"].name, "type": "building", "who": "agent",
                      "do": "the items are ready: run /haipipe-labeling with no verb on this Task; the workflow derives "
                            "its next gate (Contract first) and stops at each human gate"}
        out["url"] = open_url(root, building["task"], "Preparation", "Work Details", no_open)
        return out
    out["now"] = {"who": "person", "do": "this Job has no items Task and no building Task yet: add one "
                                         "(task-type: items, then labeling-building)"}
    return out


def words(r: dict) -> str:
    lines = [f"🏷 {r['job']}", ""]
    for t in r["tasks"]:
        here = r["now"] and t["task"] == r["now"].get("task")
        lines.append(f"{'▶' if here else ' '} {t['icon']} {t['task']} · {t['title']}" + (f" · {t['state']}" if t["state"] else ""))
    n = r["now"] or {}
    lines += ["", f"now   {n.get('task', '—')} · {n.get('step', n.get('type', ''))} · tab {n.get('tab', '—')}",
              f"who   {n.get('who')}", f"do    {n.get('do')}"]
    if n.get("note"):
        lines.append(f"note  {n['note']}")
    if r.get("url"):
        lines.append(f"open  {r['url']}")
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("path", type=Path)
    ap.add_argument("--no-open", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    r = start(a.path, a.no_open)
    print(json.dumps(r, indent=2, ensure_ascii=False, default=str) if a.json else words(r))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
