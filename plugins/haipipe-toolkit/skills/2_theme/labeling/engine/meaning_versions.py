"""A 🧭 meaning Task's loops and guideline versions, read from its own folders (b15 s58, stage 2; JL 261101: "Please
make them work"). The one place that knows the layout, so the workbench page, the skill and the scripts agree:

    runs/rNN_collect_frame*/          the frame record (collect.py record or a form): what to judge, agreed first
    runs/rNN_draw_report_mNN/         Loop NN's draw: result/draws.json, result/signals.jsonl (use case 2)
    runs/rNN_<what>_report_mNN/       Loop NN's report, written by the agent: report.json (meaning_contracts cards)
    runs/rNN_collect_report_mNN/      Loop NN's interaction report, the form you answer (collect.py)
    runs/rNN_update_mNN/              Loop NN's Update: result/labels.jsonl (reference labels lNN), result/changes.md
    meaning/mNN.mindmap.md            guideline mNN, a mind map: value → its rules, each rule citing its card
    meaning/mNN.approved.yaml         your sign on mNN; the expression Task runs only on an approved meaning

Loop NN makes mNN: every Run of the loop ends in `_mNN`. Nothing here writes except approve().

    python meaning_versions.py loops <meaning Task>
    python meaning_versions.py approve <meaning Task> m03 --by "<name>"
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path

RUN = re.compile(r"^r(\d\d)_[A-Za-z0-9_]+$")
LOOP = re.compile(r"_m(\d\d)$")
VERSION = re.compile(r"^m(\d\d)$")
CITE = re.compile(r"\b(r\d\d)\s+(Q\d+)\b")
QTAG = re.compile(r"\bQ\d+\b")
COMMENT = re.compile(r"\s*<!--.*?-->\s*")


def runs(task: Path) -> list[Path]:
    """The Task's Run folders, in order."""
    folder = Path(task) / "runs"
    return sorted((p for p in folder.iterdir() if p.is_dir() and RUN.match(p.name)), key=lambda p: p.name) \
        if folder.is_dir() else []


def _yaml_line(path: Path, key: str) -> str:
    if not path.is_file():
        return ""
    m = re.search(rf"(?m)^{key}:\s*(.+?)\s*$", path.read_text(encoding="utf-8", errors="ignore"))
    return m.group(1).strip().strip("'\"") if m else ""


def state(run: Path) -> str:
    """A Run's state: its receipt's status once it has run (result/runtime.yaml), else its card's; planned if neither."""
    return _yaml_line(run / "result" / "runtime.yaml", "status") or _yaml_line(run / "run.yaml", "status") or "planned"


def role(run: Path) -> str:
    """What a Run is to its loop: frame, draw, report (the agent's cards), collect (the form), update, or other."""
    name = run.name
    if "_collect_frame" in name or name.endswith("_frame"):
        return "frame"
    if "_collect_report_" in name:
        return "collect"
    if "_update_" in name:
        return "update"
    if "_draw_" in name:
        return "draw"
    if "_report_" in name:
        return "report"
    return "other"


def read_map(path: Path) -> dict:
    """A guideline's mind map: {title, root, branches: [{name, rules: [{text, note, tag, cite}]}]}. A branch is a top
    bullet (a value), a rule its child bullet; deeper bullets and indented lines join the rule's note. The tag is the
    card the note cites ("from r04 Q2" → Q2, cite r04 Q2)."""
    text = Path(path).read_text(encoding="utf-8", errors="ignore")
    title, root, branches = "", "", []
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":                     # front matter: its title only
        end = next((i for i, ln in enumerate(lines[1:], 1) if ln.strip() == "---"), 0)
        for ln in lines[1:end]:
            if ln.startswith("title:"):
                title = ln.split(":", 1)[1].strip()
        lines = lines[end + 1:]
    for raw in lines:
        if raw.startswith("# "):
            root = _clean(raw[2:])
            continue
        m = re.match(r"^( *)[-*] (.+)$", raw)
        if m:
            depth = len(m.group(1)) // 2
            words = _clean(m.group(2))
            if depth == 0:
                branches.append({"name": words, "rules": []})
            elif depth == 1 and branches:
                branches[-1]["rules"].append({"text": words, "note": ""})
            elif branches and branches[-1]["rules"]:
                _note(branches[-1]["rules"][-1], words)
            continue
        if raw.startswith("    ") and raw.strip() and branches and branches[-1]["rules"]:
            _note(branches[-1]["rules"][-1], _clean(raw))
    for b in branches:
        for r in b["rules"]:
            cite = CITE.search(r["note"])
            tag = QTAG.search(r["note"])
            r["cite"] = f"{cite.group(1)} {cite.group(2)}" if cite else ""
            r["tag"] = cite.group(2) if cite else tag.group(0) if tag else ""
    return {"title": title, "root": root, "branches": branches}


def _clean(words: str) -> str:
    return COMMENT.sub(" ", words).replace("**", "").strip()


def _note(rule: dict, words: str) -> None:
    rule["note"] = (rule["note"] + " " + words).strip()


def versions(task: Path) -> list[tuple[str, Path]]:
    """[(mNN, its mind map)] in order."""
    folder = Path(task) / "meaning"
    return sorted(((p.name[:3], p) for p in folder.glob("m[0-9][0-9].mindmap.md")), key=lambda v: v[0]) \
        if folder.is_dir() else []


def approval(task: Path, version: str) -> dict | None:
    """{by, at} once mNN is signed, else None."""
    path = Path(task) / "meaning" / f"{version}.approved.yaml"
    if not path.is_file():
        return None
    return {"by": _yaml_line(path, "by"), "at": _yaml_line(path, "at")}


def approve(task: Path, version: str, by: str, now: datetime | None = None) -> dict:
    """Your sign on guideline mNN: meaning/mNN.approved.yaml. Refused when the version is not made yet, or signed
    already (a sign is never rewritten); raises ValueError with the reason."""
    task = Path(task)
    by = re.sub(r"\s+", " ", str(by or "")).strip()
    if not VERSION.match(str(version or "")):
        raise ValueError("a guideline version is mNN, such as m03")
    if not by or len(by) > 80:
        raise ValueError("type your name to sign (at most 80 characters)")
    if not (task / "meaning" / f"{version}.mindmap.md").is_file():
        raise ValueError(f"{version} is not made yet: meaning/{version}.mindmap.md is missing")
    if approval(task, version):
        raise ValueError(f"{version} is approved already")
    at = (now or datetime.now()).strftime("%Y-%m-%d %H:%M")
    path = task / "meaning" / f"{version}.approved.yaml"
    path.write_text(f"version: {version}\nby: {json.dumps(by)}\nat: {at}\n"
                    "means: the meaning that expression may run on; written by the Approve sign (meaning_versions.py)\n",
                    encoding="utf-8")
    return {"version": version, "by": by, "at": at}


def frame_record(task: Path) -> dict | None:
    """The frame: {run, state, when, decisions: [{title, decision, said}]} from the first frame Run, a chat record
    (decisions.yaml) or an answered form (result/answer_collection.md); None when there is no frame Run yet."""
    run = next((r for r in runs(task) if role(r) == "frame"), None)
    if run is None:
        return None
    rows = _record_rows(run / "decisions.yaml") or _answer_rows(run / "result" / "answer_collection.md")
    when = next((r.get("when", "") for r in rows if r.get("when")), "")
    return {"run": run, "state": state(run), "when": when, "decisions": rows}


def _record_rows(path: Path) -> list[dict]:
    """collect.py record's decisions.yaml, read without a YAML library: `- title:` starts an entry, `key: value` lines
    follow (folded continuation lines join the value)."""
    if not path.is_file():
        return []
    rows, key = [], ""
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = re.match(r"^(-\s+)?(\w+):\s*(.*)$", raw.strip()) if not raw.startswith("    ") else None
        if m and (m.group(1) or rows):
            if m.group(1):
                rows.append({})
            key = m.group(2)
            rows[-1][key] = m.group(3).strip().strip("'\"")
        elif rows and key and raw.strip():
            rows[-1][key] = (rows[-1][key] + " " + raw.strip()).strip()
    return [{"title": r.get("title", ""), "decision": r.get("decision", ""), "said": r.get("said", ""),
             "when": r.get("when", "")} for r in rows if r.get("title")]


ANSWER_Q = re.compile(r"^## (Q\d+) · (.+)$")


def answers(path: Path) -> list[dict]:
    """An answered form's result/answer_collection.md: [{q, title, pick, text, note}] in order, pick the ticked key
    ("own" for my own decision, "" when nothing was picked)."""
    if not Path(path).is_file():
        return []
    out = []
    for raw in Path(path).read_text(encoding="utf-8", errors="ignore").splitlines():
        m = ANSWER_Q.match(raw)
        if m:
            out.append({"q": m.group(1), "title": m.group(2).strip(), "pick": "", "text": "", "note": ""})
            continue
        if not out:
            continue
        cur = out[-1]
        tick = re.match(r"^- \[x\] (\w) · (.+)$", raw.strip())
        if tick and not cur["pick"]:
            cur["pick"], cur["text"] = tick.group(1), tick.group(2).strip()
        elif raw.startswith("Answer: my own decision"):
            cur["pick"], cur["text"] = "own", "my own decision"
        elif raw.startswith("> decision:") or raw.startswith("> note:"):
            cur["note"] = (cur["note"] + " " + raw.split(":", 1)[1].strip()).strip()
        elif raw.startswith("Answer: none") or raw.startswith("Answer: (no option"):
            cur["pick"], cur["text"] = "", ""
    return out


def _answer_rows(path: Path) -> list[dict]:
    return [{"title": a["title"], "decision": a["note"] if a["pick"] == "own" else a["text"], "said": a["note"],
             "when": ""} for a in answers(path)]


def applied(run: Path) -> dict:
    """{QN: (state, by)} from a collect Run's applied.md (collect.py applied): what applied each answer."""
    path = Path(run) / "applied.md"
    out = {}
    if path.is_file():
        for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            m = re.match(r"^[-*]?\s*(Q\d+)\b[^A-Za-z]*(applied|in progress)?\b(.*)$", raw.strip())
            if m:
                rest = re.sub(r"^[\s·:—-]+", "", m.group(3))
                out[m.group(1)] = (m.group(2) or "applied", rest)
    return out


def questions(run: Path) -> list[tuple[str, str]]:
    """[(QN, its title)] from a form's question_collection.md."""
    path = Path(run) / "question_collection.md"
    if not path.is_file():
        return []
    return [(m.group(1), m.group(2).strip()) for m in
            (ANSWER_Q.match(ln) for ln in path.read_text(encoding="utf-8", errors="ignore").splitlines()) if m]


def report_json(loop_runs: list[Path]) -> dict | None:
    """Loop NN's report.json (the agent's cards): in the form's Run first, then in the report Run, its result/ too."""
    for run in sorted(loop_runs, key=lambda r: (role(r) != "collect", r.name)):
        for path in (run / "report.json", run / "result" / "report.json"):
            if path.is_file():
                try:
                    return json.loads(path.read_text(encoding="utf-8"))
                except ValueError:
                    return None
    return None


def cards_by_item(report: dict | None) -> dict:
    """{item_ref: QN}: which question of the form shows each item (the form keeps the report's card order)."""
    out = {}
    for i, card in enumerate((report or {}).get("cards") or [], 1):
        for ev in card.get("evidence") or []:
            if ev.get("item_ref"):
                out.setdefault(ev["item_ref"], f"Q{i}")
    return out


def loops(task: Path) -> list[dict]:
    """Every loop: {n, version, runs, frame?, draw, report, collect, update (the latest Run of each role), map,
    approved, state}. A loop exists once a Run ends in its `_mNN` or its mind map is written."""
    task = Path(task)
    by: dict[int, dict] = {}
    for run in runs(task):
        m = LOOP.search(run.name)
        if not m:
            continue
        n = int(m.group(1))
        loop = by.setdefault(n, {"n": n, "version": f"m{n:02d}", "runs": []})
        loop["runs"].append(run)
        loop[role(run)] = run                                 # the latest Run of each role
    for version, path in versions(task):
        by.setdefault(int(version[1:]), {"n": int(version[1:]), "version": version, "runs": []})["map"] = path
    out = []
    for n in sorted(by):
        loop = by[n]
        loop.setdefault("map", None)
        loop["approved"] = approval(task, loop["version"]) if loop["map"] else None
        loop["state"] = loop_state(loop)
        out.append(loop)
    return out


def loop_state(loop: dict) -> str:
    """One loop in words: approved, made, waiting for you, answered, in the making, or planned."""
    v = loop["version"]
    if loop.get("approved"):
        return f"{v} approved"
    if loop.get("map"):
        return f"made {v}"
    collect = loop.get("collect")
    if collect is not None:
        st = state(collect)
        if st == "waiting":
            return "waiting for you"
        if st == "done":
            return "answered; Update next"
        return "form planned"
    if loop.get("report") is not None:
        return "report in the making"
    draw = loop.get("draw")
    if draw is not None:
        return "draw planned" if state(draw) == "planned" else "drawn; report next"
    return "planned"


def approved_meaning(job: Path) -> tuple[Path, str, dict] | None:
    """The newest approved guideline of a Job's meaning Task: (its Task, mNN, {by, at}); None when none is signed. The
    expression Task runs only on this (b15 s58-D15, Q6)."""
    for task in sorted(p for p in Path(job).iterdir() if p.is_dir() and re.match(r"^t\d+_", p.name)):
        face = task / f"{task.name}.md"
        if face.is_file() and re.search(r"(?m)^task-type:\s*labeling-meaning\b", face.read_text(errors="ignore")[:3000]):
            signed = [(v, approval(task, v)) for v, _ in versions(task)]
            signed = [(v, a) for v, a in signed if a]
            if signed:
                return task, signed[-1][0], signed[-1][1]
    return None


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    one = sub.add_parser("loops", help="each loop's Runs, version and state")
    one.add_argument("task", type=Path)
    two = sub.add_parser("approve", help="your sign on a guideline version")
    two.add_argument("task", type=Path)
    two.add_argument("version")
    two.add_argument("--by", required=True)
    a = ap.parse_args(argv)
    if a.cmd == "loops":
        for loop in loops(a.task):
            names = ", ".join(r.name for r in loop["runs"]) or "no Run yet"
            print(f"Loop {loop['n']} · {loop['version']} · {loop['state']} · {names}")
        return 0
    try:
        print(json.dumps(approve(a.task, a.version, a.by)))
    except ValueError as err:
        print(f"not signed: {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
