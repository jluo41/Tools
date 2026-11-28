#!/usr/bin/env python3
"""/hai-labeling <Job>: open the workbench on the step a labeling Job is at, and say where it stands.

A labeling Job (`jNN_<dataset>_<label>/`) holds Tasks typed by each face's `task-type:` line: items, then either
the two loops (🧭 meaning ⇄ 🛠 expression, up to a signed release) or an older building Task, then scanning. The
work starts at the items Task (describe → items → embed). This script reads the Job from disk, finds the one next
thing (engine/two_loops.py for the two loops, the same rule the page opens on), opens that Task's page on the
workbench's focus layout (through /wb, which starts or reuses the SPACE's host; the page opens on the step that
needs you), and prints the Job's ladder with the next thing and who does it. It writes nothing.

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
LABELING = HERE.parents[1]                                     # skills/3_theme/labeling
WB = LABELING.parents[1] / "1_base" / "workbench" / "hai-workbench" / "cli" / "wb.py"
TYPES = (("items", "📦", ("items", "data")), ("ground_truth", "📏", ("raw",)),
         ("meaning", "🧭", ("labeling-meaning",)), ("expression", "🛠", ("labeling-expression",)),
         ("building", "🏗", ("labeling-building", "labeling")), ("scanning", "🔍", ("labeling-scanning", "labeling")),
         ("score", "📊", ("eval",)))


def engine(name: str = "items_task"):
    spec = importlib.util.spec_from_file_location(f"labeling_{name}_for_start", LABELING / "engine" / f"{name}.py")
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


def open_url(root: Path, folder: Path, no_open: bool, group: str = "") -> str:
    """The SPACE's host, started or reused by /wb, and the link to one Task's (or the Job's) focus page. With no
    group the page opens on the step that needs you; the Job's Delivery is group=delivery."""
    rel = folder.relative_to(root).as_posix()
    got = subprocess.run([sys.executable, str(WB), "--no-open", "--json", rel], cwd=root, capture_output=True,
                         text=True)
    try:
        port = json.loads(got.stdout)["port"]
    except (ValueError, KeyError):
        raise SystemExit("the workbench did not start: " + (got.stderr.strip()[-400:] or got.stdout.strip()[-400:]))
    url = (f"http://127.0.0.1:{port}/_board/workbench?path={quote(rel)}&layout=focus"
           + (f"&section=report&group={quote(group)}" if group else ""))
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
            out["url"] = open_url(root, items["task"], no_open)
            return out
    loop = engine("two_loops").job_now(job)
    if loop is not None:
        task = loop["task"]
        out["now"] = {"task": task.name if task else None, "type": loop["kind"] or "release", "step": loop["step"],
                      "who": loop["who"], "do": loop["do"]}
        out["url"] = open_url(root, task or job, no_open, "" if task else "delivery")
        return out
    building = next((t for t in ladder if "building" in t["types"]), None)
    if building is not None:
        out["now"] = {"task": building["task"].name, "type": "building", "who": "agent",
                      "do": "the items are ready: run /hai-labeling with no verb on this Task; the workflow derives "
                            "its next gate (Contract first) and stops at each human gate"}
        out["url"] = open_url(root, building["task"], no_open)
        return out
    out["now"] = {"who": "person", "do": "this Job has no items Task and no labeling Task yet: add one "
                                         "(task-type: items, then labeling-meaning and labeling-expression)"}
    return out


def words(r: dict) -> str:
    lines = [f"🏷 {r['job']}", ""]
    for t in r["tasks"]:
        here = r["now"] and t["task"] == r["now"].get("task")
        lines.append(f"{'▶' if here else ' '} {t['icon']} {t['task']} · {t['title']}" + (f" · {t['state']}" if t["state"] else ""))
    n = r["now"] or {}
    lines += ["", f"now   {n.get('task') or r['job']} · {n.get('type', '')} · step {n.get('step', '—')}",
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
