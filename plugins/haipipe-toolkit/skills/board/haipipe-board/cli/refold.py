#!/usr/bin/env python3
"""Give every page on a board its own folder (JL 260815), and re-anchor the paths.

    python3 refold.py <board-dir>            # dry run, prints the plan
    python3 refold.py <board-dir> --apply    # do it (git mv when tracked)

`regroup.py` puts a page in the folder of its GROUP. This puts it in a folder of
its OWN: `2-QB-delivery/QB1-opening.md` becomes
`2-QB-delivery/QB1-opening/QB1-opening.md`, and from then on every subfolder
beside that md is one of the page's plugins. `src/common.py` has read that shape
since 260815 — `_page_home()` is `<name>/<name>.md` and `_in_plugin()` keeps
discovery out of everything else — so this command adds no capability. It only
performs the move that a person otherwise does by hand, 73 times, without
dropping a path.

WHAT COMES WITH THE PAGE. Before folding, a group folder holds the plugin
material of all its pages side by side, keyed by the page's name:
`display/QBt3-for-display/`, `QA-probe/QBt5-for-value/`, `draw/QBt2.excalidraw`.
Each of those belongs to one page, so each moves under that page:
`QBt3-for-display/display/QBt3-for-display/`. The INNER path is preserved
exactly, never flattened, because things read it — a display unit is addressed
by its own folder name, and a QA-probe record names its evidence page by the
drawer it sits in (`src/topic_entry_contract.py` reads `parts[-2]`). Re-parent,
do not rename: renaming is a different decision and belongs to whoever owns that
contract.

WHAT THE MOVE BREAKS, AND WHY IT IS FIXED HERE. A page one level deeper is a
page whose every relative path is one level short. A sibling citation
`QBv1-misq.md` has to become `../QBv1-misq/QBv1-misq.md`, and a path that
pointed out of the board needs one more `../`. So the rewrite is part of the
command rather than a follow-up: a path is re-anchored when, and only when, it
RESOLVES from where the file sits today. A path that is already dead is left
exactly as it is, because guessing at what it meant is how a dead path becomes a
plausible wrong one.

WHAT IS DELIBERATELY LEFT ALONE. `## Pages` writes bare filenames and always
did, so board.md needs no edit there. Anything under `_`, `.`, `fig/` or the
generated `board/` is not board material. A page already folded is skipped, so
the command is safe to re-run.
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent  # the engine dir (this file lives in cli/)
sys.path.insert(0, str(HERE))

from src.common import page_files  # noqa: E402

# `QBt2-for-venue` owns the scene `QBt2.excalidraw`: a scene is named for the
# page's ID, which is the token before the first hyphen.
PAGE_ID = re.compile(r"^([A-Za-z]+[0-9][0-9A-Za-z]*)(?:-|$)")

# The three ways a path is written in this repo's markdown, plus the bare
# second field of a `## Links` row, which is handled separately in `rewrite()`.
TOKEN = re.compile(r"\]\(([^)\s]+)\)|`([^`\n]+?)`|!\[\[([^\]\n]+?)\]\]")

SKIP_DIRS = ("board", "fig")


def page_id(stem):
    m = PAGE_ID.match(stem)
    return m.group(1) if m else None


def companions(page, board):
    """-> [(src, dest)] the plugin material of this page, held by its group.

    A sibling directory of the page counts when it holds a child named for the
    page, or a drawing named for the page's id. The group's own scene
    (`group.excalidraw`) and anything under `_` stay where they are: they belong
    to the group, not to any one page."""
    group, stem, out = page.parent, page.stem, []
    pid = page_id(stem)
    for sib in sorted(group.iterdir()):
        if not sib.is_dir() or sib.name.startswith(("_", ".")):
            continue
        if (sib / f"{stem}.md").is_file():        # another folded page
            continue
        keyed = sib / stem
        if keyed.exists():
            lane = Path("studio") / sib.name if sib.name in {"chat", "draw"} \
                else Path(sib.name)
            out.append((keyed, group / stem / lane / stem))
        if pid:
            for scene in sorted(sib.glob(f"{pid}.*")):
                if scene.is_file():
                    lane = Path("studio") / sib.name if sib.name in {"chat", "draw"} \
                        else Path(sib.name)
                    out.append((scene, group / stem / lane / scene.name))
    return out


def plan(board):
    """-> (moves, note). `moves` is [(src, dest)], pages first, then material."""
    pages = [p for p in page_files(board) if p.parent != board]
    todo = [p for p in pages if p.parent.name != p.stem]
    if not todo:
        return [], "every page already has its own folder"
    moves = []
    for p in sorted(todo):
        moves.append((p, p.parent / p.stem / p.name))
        moves.extend(companions(p, board))
    return moves, ""


def moved_map(moves):
    """-> {resolved old path: resolved new path}, for the rewriter."""
    return {src.resolve(): dest.resolve() for src, dest in moves}


def relocate(target, mapping):
    """Where `target` ends up: itself if moved, else under a moved ancestor."""
    if target in mapping:
        return mapping[target]
    for src, dest in mapping.items():
        if src in target.parents:
            return dest / target.relative_to(src)
    return target


def rewrite_text(text, old_dir, new_dir, mapping, board=None, links_section=False):
    """Re-anchor every path in `text` that resolves from `old_dir` or the board.

    A token is rewritten only when it points at something that exists today.
    That single test is what keeps the command honest: it cannot invent a target
    for a path that was already dead, and it cannot mistake prose in backticks
    for a path, because prose does not resolve.

    Two anchors, because both are in use and they fail differently. A path
    written from the FILE resolves against `old_dir`, and the move breaks it
    even when its target never moved, so it is re-anchored to `new_dir`. A path
    written from the BOARD ROOT survives the move and breaks only when its
    target moved, so it stays board-relative and follows the target. Trying the
    file first keeps that order of preference; a path that answers to neither
    anchor is already dead and is left exactly as it is."""
    def fix(raw):
        s = raw.split("#")[0].strip()
        if not s or "://" in s or s.startswith("/") or " " in s:
            return None
        if not (s.startswith(".") or "/" in s or s.endswith(".md")):
            return None
        try:
            target = (old_dir / s).resolve()
            anchor = new_dir
            if not target.exists() and board is not None:
                target, anchor = (board / s).resolve(), board
            if not target.exists():
                return None
        except OSError:
            return None
        new = os.path.relpath(relocate(target, mapping), anchor)
        if s.endswith("/") and not new.endswith("/"):
            new += "/"
        return None if new == s else raw.replace(s, new, 1)

    if links_section:
        out = []
        for ln in text.split("\n"):
            parts = ln.split(None, 1)
            if len(parts) == 2 and not ln.startswith(("#", " ")):
                got = fix(parts[1].strip())
                if got is not None:
                    ln = ln.replace(parts[1].strip(), got, 1)
            out.append(ln)
        return "\n".join(out)

    def sub(m):
        raw = m.group(1) or m.group(2) or m.group(3) or ""
        got = fix(raw)
        return m.group(0) if got is None else m.group(0).replace(raw, got, 1)

    return TOKEN.sub(sub, text)


def markdown_files(board):
    for p in sorted(board.rglob("*.md")):
        rel = p.relative_to(board).parts
        if rel and rel[0] in SKIP_DIRS:
            continue
        if any(s.startswith(".") for s in rel):
            continue
        yield p


def rewrites(board, moves):
    """-> {path: new text}, computed against the layout BEFORE the move."""
    mapping = moved_map(moves)
    out = {}
    for p in markdown_files(board):
        old_dir = p.parent.resolve()
        new_dir = relocate(p.resolve(), mapping).parent
        text = p.read_text(encoding="utf-8")
        if p.name == "board.md" and p.parent == board:
            head, sep, tail = text.partition("\n## Links\n")
            body = rewrite_text(head, old_dir, new_dir, mapping, board)
            if sep:
                body += sep + rewrite_text(tail, old_dir, new_dir, mapping,
                                           board, links_section=True)
            new = body
        else:
            new = rewrite_text(text, old_dir, new_dir, mapping, board)
        if new != text:
            out[p.resolve()] = new
    return out


def apply(moves, texts):
    for src, dest in moves:
        dest.parent.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(["git", "mv", str(src), str(dest)],
                           cwd=src.parent, capture_output=True)
        if r.returncode:                      # untracked, or not a repo
            src.rename(dest)
    mapping = moved_map(moves)
    for old, text in texts.items():
        relocate(old, mapping).write_text(text, encoding="utf-8")


def run(board, do_it):
    board = Path(board).resolve()
    moves, note = plan(board)
    print(f"\n📋 {board.name}")
    if note:
        print(f"   {note}")
        return 0
    texts = rewrites(board, moves)
    pages = [(s, d) for s, d in moves if s.suffix == ".md" and s.stem == d.parent.name]
    print(f"   {len(pages)} pages get their own folder")
    for src, dest in moves:
        if (src, dest) not in pages:
            print(f"   ↳ {src.relative_to(board)}  →  {dest.relative_to(board)}")
    print(f"   {len(texts)} files have paths to re-anchor")
    if do_it:
        apply(moves, texts)
        print(f"   ✅ moved {len(moves)}, rewrote {len(texts)}")
    else:
        print(f"   (dry run: pass --apply)")
    return len(moves)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("target", help="a board folder, or a root with --all")
    ap.add_argument("--all", action="store_true", help="every board.md under target")
    ap.add_argument("--apply", action="store_true", help="actually move")
    a = ap.parse_args(argv)
    root = Path(a.target).resolve()
    if not a.all:
        run(root, a.apply)
        return 0
    total = 0
    for bmd in sorted(root.rglob("board.md")):
        rel = bmd.parent.relative_to(root).as_posix()
        if any(s.startswith((".", "_")) for s in rel.split("/")):
            continue
        total += run(bmd.parent, a.apply)
    print(f"\n{total} moves {'made' if a.apply else 'planned'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
