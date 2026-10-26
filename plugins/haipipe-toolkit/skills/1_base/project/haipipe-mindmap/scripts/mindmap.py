#!/usr/bin/env python3
"""haipipe-mindmap: one `.mindmap.md` file, shown as the draft's §1 Structure map is: HTML, edited in place.

    mindmap.py new        <x.mindmap.md> [--title T]          a new map: its root, nothing under it yet
    mindmap.py from-work  <world|Block|Job> [--out F]          Block → Job → Task → Run with run counts
    mindmap.py from-topic <studio/sNN-topic> [--out F]         the topic's structured side, mNN-<topic>
    mindmap.py refresh    <x.mindmap.md>                       rebuild from disk; a person's nodes and words kept
    mindmap.py render     <x.mindmap.md>                       the static page <x>.mindmap.html from the file
    mindmap.py check      <x.mindmap.md | folder> ...          grammar and ids

The workbench draws the map live from the file on every open (a Studio topic's Structured side) and writes each
change a person makes there back into the file (mmmap.act, POST /_board/mindmap). Exit 0 done, 1 a check failed.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import mmbuild as MB  # noqa: E402
import mmhtml as MH  # noqa: E402
import mmtree as MT  # noqa: E402


def _load(md: Path) -> MT.MindMap:
    """The file, every node given an id (a bullet a person typed gets the next free nNN, written back)."""
    mm = MT.load(md)
    if MT.ensure_ids(mm):
        MT.save(mm, md)
    return mm


def render(md: Path, mm: MT.MindMap | None = None) -> None:
    """The static page beside the file; the workbench needs none, it draws the map from the file."""
    v = MT.views(md)
    mm = mm or _load(md)
    with open(v["html"], "w", encoding="utf-8", newline="\n") as f:
        f.write(MH.page(mm))
    print(f"{v['stem']}: {sum(1 for _ in MT.walk(mm.root))} nodes, {MB.words(mm)} words · {v['html'].name}")


def build(kind: str, src: Path, out: Path | None) -> int:
    src = Path(src).resolve()
    if kind == "from-topic":
        new = MB.from_topic(src)
        out = out or src / MB.mnn_name(src)
    else:
        new = MB.from_work(src)
        out = out or src / "studio" / f"mind-map{MT.SUFFIX}"
    out = Path(out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    new.meta["built"] = f"{kind} {Path(os.path.relpath(src, out.parent)).as_posix()}"
    if out.is_file():
        mm = _load(out)
        done = MB.refresh(mm, new)
        mm.meta["built"] = new.meta["built"]
        print(f"{out.name}: refreshed: {done['updated']} words updated, {done['added']} added, "
              f"{done['dropped']} gone from disk; a person's nodes and words kept")
    else:
        mm = new
    MT.save(mm, out)
    render(out, mm)
    return 0


def refresh(md: Path) -> int:
    md = Path(md).resolve()
    kind, _, where = (MT.load(md).meta.get("built") or "").partition(" ")
    if kind not in ("from-work", "from-topic"):
        sys.exit(f"{md.name}: its front matter says no `built: from-work <path>` or `built: from-topic <path>`")
    return build(kind, (md.parent / (where or ".")).resolve(), md)


def stale(md: Path, mm: MT.MindMap) -> list:
    """A topic's map older than what it is made from: the topic's page or its drawing changed after the map was last
    written, so the map may say something they no longer do. A warning, not a failure: a person decides."""
    md = Path(md)
    kind, _, where = (mm.meta.get("built") or "").partition(" ")
    if kind != "from-topic":
        return []
    topic = (md.parent / (where or ".")).resolve()
    sources = [topic / f"{topic.name}.md"] + [d for d in topic.glob("*.excalidraw") if not re.match(r"m\d{2}[-_]", d.name)]
    newer = [f for f in sources if f.is_file() and f.stat().st_mtime > md.stat().st_mtime + 1]
    return [f"{f.name} changed after this map: update the map (ask in the Studio chat, or `refresh`)" for f in newer]


def skeleton(topic: Path) -> Path:
    """A new topic's map, honest about being unwritten: its root and its Files only, and a note saying so. A map
    built from a fresh face's template reads as finished and empty; this one asks to be written."""
    topic = Path(topic).resolve()
    out = topic / MB.mnn_name(topic)
    if out.exists():
        return out
    mm = MB.from_topic(topic)
    mm.root.children = [c for c in mm.root.children if c.id == "@files"]
    mm.root.note = ["Not written yet: ask in the Studio chat to write this map from the topic's page and drawing."]
    mm.meta["built"] = "from-topic ."
    MT.save(mm, out)
    render(out, mm)
    return out


def check(paths) -> int:
    files = []
    for p in map(Path, paths):
        files += sorted(p.rglob("*" + MT.SUFFIX)) if p.is_dir() else [p]
    bad = 0
    for md in files:
        problems = []
        try:
            mm = MT.load(md)
        except MT.GrammarError as e:
            problems.append(str(e))
            mm = None
        if mm:
            ids = [n.id for n, p, *_ in MT.walk(mm.root) if p is not None]
            if "" in ids:
                problems.append(f"{ids.count('')} bullet(s) without an id: the workbench or render gives them one")
            dup = sorted({i for i in ids if i and ids.count(i) > 1})
            if dup:
                problems.append(f"an id used twice: {', '.join(dup)}")
        notes = stale(md, mm) if mm else []
        bad += bool(problems)
        print(f"{'✗' if problems else '✓'} {md}" + "".join(f"\n    ✗ {p}" for p in problems)
              + "".join(f"\n    · {n}" for n in notes))
    return 1 if bad else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("new")
    s.add_argument("file")
    s.add_argument("--title")
    for name in ("from-work", "from-topic"):
        s = sub.add_parser(name)
        s.add_argument("path")
        s.add_argument("--out")
    for name in ("refresh", "render"):
        sub.add_parser(name).add_argument("file")
    sub.add_parser("check").add_argument("paths", nargs="+")
    a = ap.parse_args(argv)
    if a.cmd == "new":
        md = Path(a.file)
        MT.views(md)
        if md.exists():
            sys.exit(f"{md} exists: edit it, or render it")
        title = a.title or md.name[: -len(MT.SUFFIX)].replace("-", " ")
        md.parent.mkdir(parents=True, exist_ok=True)
        mm = MT.MindMap({"mindmap": "1", "title": title}, MT.Node("root", title))
        MT.save(mm, md)
        render(md, mm)
        return 0
    if a.cmd in ("from-work", "from-topic"):
        return build(a.cmd, Path(a.path), Path(a.out) if a.out else None)
    if a.cmd == "refresh":
        return refresh(Path(a.file))
    if a.cmd == "render":
        render(Path(a.file))
        return 0
    return check(a.paths)


if __name__ == "__main__":
    sys.exit(main())
