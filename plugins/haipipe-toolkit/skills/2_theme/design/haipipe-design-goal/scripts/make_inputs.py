"""Freeze a Block's inputs version, or build a Job's inputs/ fence (ref/inputs.md).

    python make_inputs.py freeze <block>/inputs/iN [--new "<what changed>"] [--rules r2]
    python make_inputs.py job    <block>/jNN_<goal>_<method>

freeze writes inputs/iN/manifest.yaml: every file with the first 12 hex of its sha256, keeping a parts: list a draft
manifest already has. job writes the Job's inputs/goal.md from its pinned goal (board.md ## Goals), links every file
of the pinned inputs version whose part the method's step ① sees (inputs/method.md `sees:`), and writes
inputs/manifest.yaml. Neither ever overwrites: with a frozen manifest there, nothing is made.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import os
import re
import sys
from pathlib import Path

import yaml

PARTS = ("Goal · how much is set", "Goal · for whom", "Information · whose", "Information · form", "Examples",
         "Tools", "Reading", "From the last unit")
DEFAULT_SEES = ("Goal · how much is set",)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12] if path.is_file() else "—"


def front(md: Path) -> dict:
    if not md.is_file():
        return {}
    m = re.match(r"(?s)^---\n(.*?)\n---\n", md.read_text(encoding="utf-8"))
    return (yaml.safe_load(m.group(1)) or {}) if m else {}


def goals(board: Path) -> list:
    m = re.search(r"(?ms)^##\s+Goals\s*\n.*?```yaml\n(.*?)```", board.read_text(encoding="utf-8")) \
        if board.is_file() else None
    data = (yaml.safe_load(m.group(1)) or {}) if m else {}
    return data.get("goals", []) or []


def _dump(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def today() -> str:
    return datetime.date.today().strftime("%y%m%d")


def freeze(version: Path, new: str, rules: str, made: list) -> None:
    if not re.match(r"^i\d+$", version.name) or version.parent.name != "inputs":
        sys.exit(f"an inputs version is <block>/inputs/iN: {version}")
    man = version / "manifest.yaml"
    draft = yaml.safe_load(man.read_text(encoding="utf-8")) if man.is_file() else {}
    if draft and draft.get("frozen"):
        return                                           # frozen: never edited, a new version is i<N+1>
    files = sorted(p for p in version.rglob("*") if p.is_file() and p.name != "manifest.yaml")
    if not files:
        sys.exit(f"nothing to freeze in {version}")
    data = {"version": version.name, "frozen": today(), "new": new or (draft or {}).get("new", "<what changed>"),
            "rules": rules or (draft or {}).get("rules", ""), "parts": (draft or {}).get("parts", []),
            "files": [{"path": p.relative_to(version).as_posix(), "sha256": sha(p)} for p in files]}
    _dump(man, data)
    made.append(man)


def _goal_md(goal: dict) -> str:
    rules = "".join(f"- {r}\n" for r in goal.get("rules") or []) or "- (the shared rules only)\n"
    return (f"# {goal.get('id')} · {goal.get('aim', '?')}\n\n"
            f"aim: {goal.get('aim', '?')}\nwho: {goal.get('who', '?')}\nvenue: {goal.get('venue', '?')}\n"
            f"n: {goal.get('n', '?')}\nleave out: {goal.get('leave-out', '') or 'nothing named'}\n\n"
            f"## Rules for this goal\n\n{rules}")


def _sees(entries) -> dict:
    """A method's `sees:` as {part: kinds or None}: `<part>` sees every file of that part; `<part> [<kind>, …]` only
    the files whose manifest entry carries one of those `kind:`s (JL 261008: a method ladder where each method sees one
    more layer of the same kind of input)."""
    out = {}
    for e in entries:
        m = re.match(r"^(.*?)\s*\[(.*)\]\s*$", str(e))
        part, kinds = (m.group(1).strip(), {k.strip() for k in m.group(2).split(",") if k.strip()}) if m else (str(e).strip(), None)
        if part in out and (out[part] is None or kinds is None):
            out[part] = None
        else:
            out[part] = (out.get(part) or set()) | kinds if kinds is not None else None
    return out


def _seen(entry: dict, sees: dict) -> bool:
    part = entry.get("part")
    if part not in sees:
        return False
    return sees[part] is None or str(entry.get("kind", "")) in sees[part]


def job(jdir: Path, made: list) -> None:
    face = jdir / f"{jdir.name}.md"
    pins = front(face)
    if not pins.get("goal") or not pins.get("inputs"):
        sys.exit(f"{face.name} pins no goal: or inputs: (run-setup-goal first)")
    block = jdir.parent
    fence = jdir / "inputs"
    if (fence / "manifest.yaml").is_file():
        return                                           # built once; a rebuild removes inputs/ first
    goal = next((g for g in goals(block / "board.md") if g.get("id") == pins["goal"]), None)
    if goal is None:
        sys.exit(f"goal {pins['goal']} is not in {block.name}/board.md ## Goals")
    if not str(goal.get("signed") or "").strip():
        sys.exit(f"goal {pins['goal']} is not signed yet: a person signs it at the Block first")
    version = block / "inputs" / str(pins["inputs"])
    vman = version / "manifest.yaml"
    if not vman.is_file() or not (yaml.safe_load(vman.read_text(encoding="utf-8")) or {}).get("frozen"):
        sys.exit(f"inputs version {pins['inputs']} is not frozen (make_inputs.py freeze {version})")
    vparts = (yaml.safe_load(vman.read_text(encoding="utf-8")) or {}).get("parts", []) or []
    if not (fence / "method.md").is_file():
        sys.exit(f"{jdir.name}/inputs/method.md is missing: pin the method first (run-setup-method, pin_method.py); "
                 "step ① of the pinned version decides what the fence holds")
    method = front(fence / "method.md")
    sees = _sees(method.get("sees") or DEFAULT_SEES)
    fence.mkdir(parents=True, exist_ok=True)
    gmd = fence / "goal.md"
    if not gmd.exists():
        gmd.write_text(_goal_md(goal), encoding="utf-8")
        made.append(gmd)
    rows = [{"part": "Goal · how much is set", "choice": "aim · N · leave out", "file": "goal.md"}]
    for p in vparts:
        if not _seen(p, sees) or not p.get("file") or not (version / p["file"]).is_file():
            continue
        name = Path(p["file"]).name
        link = fence / name
        if link.exists() or link.is_symlink():
            name = p["file"].replace("/", "-")
            link = fence / name
        if not (link.exists() or link.is_symlink()):
            os.symlink(os.path.relpath(version / p["file"], fence), link)
            made.append(link)
        rows.append({"part": p["part"], "choice": p.get("says", ""), "file": name, **({"kind": p["kind"]} if p.get("kind") else {})})
    covered = {r["part"] for r in rows}
    if "Goal · for whom" not in covered:
        rows.append({"part": "Goal · for whom", "choice": "in goal.md: who", "file": ""})
    rows += [{"part": part, "choice": "nothing", "file": ""} for part in PARTS
             if part not in covered and part != "Goal · for whom"]
    rows.sort(key=lambda r: PARTS.index(r["part"]) if r["part"] in PARTS else len(PARTS))
    pinned = f"haipipe-design-method/methods/{method.get('method', '?')}-*/{method.get('version', '?')}.md"
    files = [{"path": p.name, "source": os.readlink(p) if p.is_symlink() else pinned if p.name == "method.md"
              else "written", "sha256": sha(p)}
             for p in sorted(fence.iterdir()) if p.name != "manifest.yaml"]
    man = fence / "manifest.yaml"
    _dump(man, {"inputs": str(pins["inputs"]), "frozen": today(),
                "method": "method.md", "parts": rows, "files": files})
    made.append(man)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("what", choices=("freeze", "job"))
    ap.add_argument("folder", type=Path)
    ap.add_argument("--new", default="")
    ap.add_argument("--rules", default="")
    a = ap.parse_args(argv)
    made = []
    if a.what == "freeze":
        freeze(a.folder, a.new, a.rules, made)
    else:
        job(a.folder, made)
    for p in made:
        print("made", p)
    return made


if __name__ == "__main__":
    main()
