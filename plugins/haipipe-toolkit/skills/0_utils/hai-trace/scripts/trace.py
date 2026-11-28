"""hai-trace: write, update and check trace files (`<Block>/trace/<YYMMDD>/<HHMM>_<slug>.md`).

    trace.py new <Block> --slug S --title T --aim A --plan "do|path|what" ... [--prompt P] [--topic sNN-x]
    trace.py prompt <trace.md> "words" [--at HH:MM]
    trace.py changed <trace.md> [--also path ...]
    trace.py close <trace.md> --check "line" ... --summary "text"
    trace.py check [glob]

Run from the SPACE root. The front matter is written with a YAML writer, so no value can break it.
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys
from pathlib import Path

import yaml

DOS = ("add", "edit", "move", "delete")
PARTS = ("Prompts", "Check", "Summary")


def split(text: str) -> tuple[dict, str]:
    """(front matter, body) of a trace; ({}, text) when it has none or it does not parse."""
    if not text.startswith("---"):
        return {}, text
    try:
        _, head, body = text.split("---", 2)
        meta = yaml.safe_load(head) or {}
    except (ValueError, yaml.YAMLError):
        return {}, text
    return (meta if isinstance(meta, dict) else {}), body


def join(meta: dict, body: str) -> str:
    head = yaml.safe_dump(meta, sort_keys=False, allow_unicode=True, width=10_000)
    return "---\n" + head + "---\n\n" + body.lstrip("\n")


def section(body: str, name: str) -> str:
    m = re.search(rf"^## {name}\n(.*?)(?=^## |\Z)", body, re.M | re.S)
    return m.group(1).strip() if m else ""


def put(body: str, name: str, text: str, append: bool = False) -> str:
    """Body with one `## name` part set (or a line appended to it)."""
    old = section(body, name)
    new = (old + "\n" + text).strip() if append and old else text.strip()
    if re.search(rf"^## {name}\n", body, re.M):
        return re.sub(rf"(^## {name}\n)(.*?)(?=^## |\Z)", lambda m: m.group(1) + "\n" + new + "\n\n", body, count=1,
                      flags=re.M | re.S)
    return body.rstrip() + f"\n\n## {name}\n\n{new}\n"


def rel(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def new(a, root: Path, now: dt.datetime) -> Path:
    block = (root / a.block).resolve()
    face = block / "trace" / now.strftime("%y%m%d") / f"{now.strftime('%H%M')}_{a.slug}.md"
    if face.exists():
        sys.exit(f"❗ {rel(face, root)} exists")
    face.parent.mkdir(parents=True, exist_ok=True)
    plan = [{"do": "add", "path": rel(face, root), "what": "this trace's own record, written first"}]
    for line in a.plan or []:
        do, path, what = (line.split("|", 2) + ["", ""])[:3]
        if do not in DOS or not path or not what:
            sys.exit(f"❗ a plan line is do|path|what with do one of {', '.join(DOS)}: {line}")
        plan.append({"do": do, "path": path, "what": what})
    meta = {"title": a.title, "date": now.strftime("%Y-%m-%d %H:%M")}
    if a.topic:
        meta["topic"] = a.topic
    meta.update({"aim": a.aim, "closed": False, "plan": plan, "changed": [rel(face, root)]})
    prompts = f"- **{now.strftime('%H:%M')}** {a.prompt}" if a.prompt else ""
    body = f"# {a.title}\n\n## Prompts\n\n{prompts}\n\n## Check\n\n## Summary\n"
    face.write_text(join(meta, body), encoding="utf-8")
    return face


def dirty(root: Path, paths) -> set[str]:
    out = subprocess.run(["git", "-C", str(root), "status", "--porcelain", "-uall", "--", *paths],
                         capture_output=True, text=True).stdout
    return {line[3:].split(" -> ")[-1].strip('"') for line in out.splitlines() if len(line) > 3}


def changed(face: Path, root: Path, also) -> list[str]:
    meta, body = split(face.read_text(encoding="utf-8"))
    plan = [str(i["path"]) for i in meta.get("plan") or [] if isinstance(i, dict) and i.get("path")]
    hit = dirty(root, plan) if plan else set()
    keep = list(dict.fromkeys([*(meta.get("changed") or []), *[p for p in plan if p in hit], *(also or [])]))
    meta["changed"] = keep
    face.write_text(join(meta, body), encoding="utf-8")
    return keep


def problems(face: Path) -> list[str]:
    meta, body = split(face.read_text(encoding="utf-8"))
    if not meta:
        return ["no front matter (or it does not parse)"]
    bad = [] if meta.get("aim") else ["no aim"]
    plan = meta.get("plan") or []
    bad += [] if plan else ["no plan"]
    bad += [f"a plan line without do, path and what: {i}" for i in plan
            if not (isinstance(i, dict) and i.get("do") in DOS and i.get("path") and i.get("what"))]
    if meta.get("closed"):
        bad += [f"closed with an empty ## {p}" for p in ("Check", "Summary") if not section(body, p)]
    return bad


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("new"); n.add_argument("block"); n.add_argument("--slug", required=True)
    n.add_argument("--title", required=True); n.add_argument("--aim", required=True)
    n.add_argument("--plan", action="append"); n.add_argument("--prompt"); n.add_argument("--topic")
    p = sub.add_parser("prompt"); p.add_argument("trace"); p.add_argument("words"); p.add_argument("--at")
    c = sub.add_parser("changed"); c.add_argument("trace"); c.add_argument("--also", nargs="*")
    z = sub.add_parser("close"); z.add_argument("trace"); z.add_argument("--check", action="append", required=True)
    z.add_argument("--summary", required=True)
    k = sub.add_parser("check"); k.add_argument("glob", nargs="?", default="examples/**/trace/[0-9]*/[0-9]*_*.md")
    a = ap.parse_args(argv)
    root, now = Path.cwd(), dt.datetime.now()
    if a.cmd == "new":
        print(rel(new(a, root, now), root))
    elif a.cmd == "prompt":
        face = root / a.trace
        meta, body = split(face.read_text(encoding="utf-8"))
        face.write_text(join(meta, put(body, "Prompts", f"- **{a.at or now.strftime('%H:%M')}** {a.words}", append=True)),
                        encoding="utf-8")
    elif a.cmd == "changed":
        print("\n".join(changed(root / a.trace, root, a.also)))
    elif a.cmd == "close":
        face = root / a.trace
        meta, body = split(face.read_text(encoding="utf-8"))
        body = put(put(body, "Check", "\n".join(f"- {x}" for x in a.check)), "Summary", a.summary)
        meta["closed"] = True
        face.write_text(join(meta, body), encoding="utf-8")
        bad = problems(face)
        for b in bad:
            print("❗", b)
        return 1 if bad else 0
    else:
        faces = sorted(root.glob(a.glob))
        bad = [(f, b) for f in faces for b in problems(f)]
        # a file beside the traces whose name has no time: the Files pane and this check would never see it
        loose = sorted(f for f in root.glob("examples/**/trace/[0-9]*/*.md") if not re.match(r"\d{4}_", f.name))
        bad += [(f, "its name has no HHMM_ prefix (trace.py new names a trace for the time of its first prompt)")
                for f in loose]
        for f, b in bad:
            print(f"❗ {rel(f, root)}: {b}")
        print(f"{'❗' if bad else '✅'} traces: {len(faces)} files, {len(bad)} problems")
        return 1 if bad else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
