#!/usr/bin/env python3
"""haipipe-mindmap: one `.mindmap.md` file, drawn left to right on an Excalidraw canvas and shown as a web page.

    mindmap.py new        <x.mindmap.md> [--title T]          a new map: its root, nothing under it yet
    mindmap.py from-work  <world|Block|Job> [--out F] [--all]  Block → Job → Task → Run with run counts
    mindmap.py from-topic <studio/sNN-topic> [--out F] [--all] the topic's structured side, mNN-<topic>
    mindmap.py refresh    <x.mindmap.md> [--all]               rebuild from disk; a person's nodes and words kept
    mindmap.py render     <x.mindmap.md> [--force]             the canvas, its .png and the web page from the file
    mindmap.py sync       <x.mindmap.md> [--take file|canvas|ID=file|ID=canvas ...]
                                                              the canvas's edits into the file, then render
    mindmap.py html       <x.mindmap.md>                       the web page only
    mindmap.py check      <x.mindmap.md | folder> ...          grammar, ids, the views, nothing left unsynced

Exit 0 when done, 1 when a check fails, 2 when an edit made on both sides waits for a person to pick a side.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import mmbuild as MB  # noqa: E402
import mmcanvas as MC  # noqa: E402  (puts excalidraw-studio's and haipipe-studio's scripts on the path)
import mmhtml as MH  # noqa: E402
import mmtree as MT  # noqa: E402
import render_png  # noqa: E402  (haipipe-studio's offline preview)


def _taken(v: dict) -> set:
    base = MC.base_of(MC.load_doc(v["canvas"])) if v["canvas"].is_file() else None
    return set(base or {})


def _load(md: Path) -> MT.MindMap:
    """The file, every node given an id (a bullet a person typed gets the next free nNN, written back)."""
    v = MT.views(md)
    mm = MT.load(md)
    if MT.ensure_ids(mm, _taken(v)):
        MT.save(mm, md)
    return mm


def pending(md: Path) -> tuple:
    """(the canvas's edits not yet in the file, what `read` saw), or (None, None) with no canvas or no base."""
    v = MT.views(md)
    if not v["canvas"].is_file():
        return None, None
    doc = MC.load_doc(v["canvas"])
    seen = MC.read(doc)
    if seen is None:
        return None, None
    return MC.changes(MC.base_of(doc), seen["flat"]), seen


def render(md: Path, mm: MT.MindMap | None = None, absorbed: set = frozenset(), html: bool = True, quiet=False) -> None:
    v = MT.views(md)
    mm = mm or _load(md)
    MC.write(v["canvas"], MC.draw(mm), absorbed)
    render_png.render(v["canvas"], v["png"])
    if html:
        write_html(md, mm)
    if not quiet:
        print(f"{v['stem']}: {sum(1 for _ in MT.walk(mm.root))} nodes, {MB.words(mm)} words · "
              f"{v['canvas'].name} · {v['png'].name}" + (f" · {v['html'].name}" if html else ""))


def write_html(md: Path, mm: MT.MindMap) -> None:
    v = MT.views(md)
    with open(v["html"], "w", encoding="utf-8", newline="\n") as f:
        f.write(MH.page(mm, v["png"].name))


def parse_take(items) -> dict:
    out = {}
    for t in items or []:
        k, _, side = t.rpartition("=")
        side = {"md": "file"}.get(side, side)
        if side not in ("file", "canvas"):
            sys.exit(f"--take {t}: a side is file or canvas")
        out[k or "*"] = side
    return out


def sync(md: Path, take: dict | None = None) -> int:
    v = MT.views(md)
    mm = _load(md)
    if not v["canvas"].is_file():
        render(md, mm)
        return 0
    doc = MC.load_doc(v["canvas"])
    seen, base = MC.read(doc), MC.base_of(doc)
    if seen is None:
        print(f"{v['canvas'].name}: no mind map frame (mm:frame) on the canvas, so nothing to read back; "
              "drawing from the file, the person's own elements kept")
        render(md, mm)
        return 0
    try:
        done = MC.merge(mm, base, seen, take)
    except MC.Conflict as c:
        print(f"{md.name}: {len(c.items)} edit(s) made on both sides; nothing written. Pick a side:")
        for i, what, file_side, canvas_side in c.items:
            print(f"  {i:<14} {what}\n  {'':<14} file:   {file_side}\n  {'':<14} canvas: {canvas_side}")
        print(f"then: mindmap.py sync {md} --take file | --take canvas | --take <id>=file ...")
        return 2
    MT.ensure_ids(mm, set(base))
    MT.save(mm, md)
    render(md, mm, seen["absorbed"])
    said = ", ".join(f"{k} {n}" for k, n in done.items() if n)
    print(f"{md.name}: from the canvas: {said or 'nothing changed'}")
    return 0


def build(kind: str, src: Path, out: Path | None, everything: bool) -> int:
    src = Path(src).resolve()
    if kind == "from-topic":
        new = MB.from_topic(src)
        out = out or src / MB.mnn_name(src)
        rel_src = "."
    else:
        new = MB.from_work(src)
        out = out or src / "studio" / f"mind-map{MT.SUFFIX}"
        rel_src = None
    out = Path(out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    rel_src = rel_src or Path(_relpath(src, out.parent)).as_posix()
    new.meta["built"] = f"{kind} {rel_src}"
    if not everything:
        MB.fit(new)
    if out.is_file():
        rc = sync(out)                                  # the canvas's edits first, so a refresh loses none
        if rc:
            return rc
        mm = _load(out)
        done = MB.refresh(mm, new)
        mm.meta["built"] = new.meta["built"]
        MT.save(mm, out)
        print(f"{out.name}: refreshed: {done['updated']} words updated, {done['added']} added, "
              f"{done['dropped']} gone from disk; a person's nodes and words kept")
    else:
        mm = new
        MT.save(mm, out)
    render(out, mm)
    return 0


def _relpath(a: Path, b: Path) -> str:
    import os
    return os.path.relpath(a, b)


def refresh(md: Path, everything: bool) -> int:
    md = Path(md).resolve()
    meta = MT.load(md).meta
    kind, _, where = (meta.get("built") or "").partition(" ")
    if kind not in ("from-work", "from-topic"):
        sys.exit(f"{md.name}: its front matter says no `built: from-work <path>` or `built: from-topic <path>`")
    return build(kind, (md.parent / (where or ".")).resolve(), md, everything)


def check(paths) -> int:
    files = []
    for p in map(Path, paths):
        files += sorted(p.rglob("*" + MT.SUFFIX)) if p.is_dir() else [p]
    bad = 0
    for md in files:
        v, problems, notes = MT.views(md), [], []
        try:
            mm = MT.load(md)
        except MT.GrammarError as e:
            print(f"✗ {md}: {e}")
            bad += 1
            continue
        ids = [n.id for n, p, *_ in MT.walk(mm.root) if p is not None]
        if "" in ids:
            problems.append(f"{ids.count('')} bullet(s) without an id: run render or sync")
        dup = sorted({i for i in ids if i and ids.count(i) > 1})
        if dup:
            problems.append(f"an id used twice: {', '.join(dup)}")
        if not v["canvas"].is_file():
            problems.append(f"no canvas {v['canvas'].name}: run render")
        else:
            doc = MC.load_doc(v["canvas"])
            base = MC.base_of(doc)
            if base is None:
                problems.append("the canvas has no mind map frame: run render")
            else:
                cv, _seen = pending(md)
                if cv and MC.any_change(cv):
                    problems.append("the canvas has edits not in the file: run sync")
                if MC.any_change(MC.changes(base, MT.flat(mm))):
                    problems.append("the file has edits not drawn: run sync (or render)")
        if not v["png"].is_file():
            problems.append(f"no preview {v['png'].name}: run render")
        if not v["html"].is_file():
            notes.append(f"no web page {v['html'].name} (git ignores it): run html")
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
        s.add_argument("--all", action="store_true", help="keep every node, past principle 7's 200 words")
    s = sub.add_parser("refresh")
    s.add_argument("file")
    s.add_argument("--all", action="store_true")
    s = sub.add_parser("render")
    s.add_argument("file")
    s.add_argument("--force", action="store_true", help="draw over edits the canvas holds that are not in the file")
    s = sub.add_parser("sync")
    s.add_argument("file")
    s.add_argument("--take", action="append", help="file | canvas | <id>=file | <id>=canvas")
    s = sub.add_parser("html")
    s.add_argument("file")
    s = sub.add_parser("check")
    s.add_argument("paths", nargs="+")
    a = ap.parse_args(argv)
    if a.cmd == "new":
        md = Path(a.file)
        MT.views(md)
        if md.exists():
            sys.exit(f"{md} exists: edit it, or render it")
        title = a.title or md.name[: -len(MT.SUFFIX)].replace("-", " ")
        md.parent.mkdir(parents=True, exist_ok=True)
        MT.save(MT.MindMap({"mindmap": "1", "title": title}, MT.Node("root", title)), md)
        render(md)
        return 0
    if a.cmd in ("from-work", "from-topic"):
        return build(a.cmd, Path(a.path), Path(a.out) if a.out else None, a.all)
    if a.cmd == "refresh":
        return refresh(Path(a.file), a.all)
    if a.cmd == "render":
        md = Path(a.file)
        cv, _ = pending(md)
        if cv and MC.any_change(cv) and not a.force:
            print(f"{md.name}: the canvas holds edits not in the file; run `sync` first (or render --force to drop them)")
            return 2
        render(md)
        return 0
    if a.cmd == "sync":
        return sync(Path(a.file), parse_take(a.take))
    if a.cmd == "html":
        write_html(Path(a.file), _load(Path(a.file)))
        print(MT.views(Path(a.file))["html"].name)
        return 0
    return check(a.paths)


if __name__ == "__main__":
    sys.exit(main())
