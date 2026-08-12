#!/usr/bin/env python3
"""Watch a Board source folder and rebuild its generated board/ site.

    python3 watch.py <board-dir>

Why this exists: the browser's "Sync to md" button writes your comments straight
into the Q files, but it cannot run Python, so board/ stays stale until
someone rebuilds. Run this once in a terminal and that gap closes: press Sync,
refresh the page, your comment is rendered. No Claude Code in the loop.

Stdlib only, polls mtimes every second. Ctrl-C to stop.
"""
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent  # the engine dir (this file lives in cli/)


def stamp(d):
    # QC3: Q files may sit in subfolders, so watch the whole tree; skip
    # `_`/`.` segments (archives, previews) and fig/ same as build.py.
    return {p: p.stat().st_mtime
            for p in sorted(d.rglob("*.md"))
            if not any(s.startswith(("_", ".")) or s == "fig"
                       for s in p.relative_to(d).parts[:-1])}


def build(d, only=None):
    """Rebuild the board.

    `only` names the .md files that actually changed. When the board/ tree
    exists, that lets the rebuild rewrite JUST those pages instead of all of
    them, which is JL's 260731 rule: changing one page must not disturb a
    reader sitting on another (QC9).
    """
    cmd = [sys.executable, str(HERE / "cli" / "build.py"), str(d)]
    if (d / "board").is_dir():
        if only:
            cmd += ["--only", ",".join(sorted(only))]
    r = subprocess.run(cmd, capture_output=True, text=True)
    print((r.stdout or r.stderr).strip(), flush=True)
    project_sections(d, only)


MD2TEX = (HERE.parent.parent / "paper" / "haipipe-paper"
          / "scripts" / "to-word" / "md2tex.py")


def project_sections(d, only=None):
    """A SECTION page that changed also regenerates its .tex, and says where.

    JL 260807: "section 一改它就生成", and the path has to be printed or the
    output may as well not exist. Only pages that DECLARE `section_title:` are
    projected, so this never fires on a board that has no manuscript behind it.

    It writes `3-dist/tex/`, which is md2tex's own default, and never
    `sections/`. Overwriting the tree a human hand-carries stays a separate
    deliberate act, and a watcher is the last place that should happen by
    itself.
    """
    if not MD2TEX.is_file():
        return
    pages = [p for p in sorted(d.rglob("*.md"))
             if not any(s.startswith(("_", ".")) for s in p.relative_to(d).parts)
             and (only is None or p.name in only)
             and "section_title:" in p.read_text(errors="ignore")[:1500]]
    if not pages:
        return
    root = next((c for c in (d / "_fixture", d.parent.parent) if c.is_dir()), None)
    if root is None:
        return
    r = subprocess.run([sys.executable, str(MD2TEX), *map(str, pages),
                        "--paper-root", str(root)],
                       capture_output=True, text=True)
    out = (r.stdout or r.stderr).strip()
    if out:
        print(out, flush=True)
    for p in pages:
        made = root / "3-dist" / "tex" / (p.stem + ".tex")
        if made.is_file():
            print(f"   📄 {made}", flush=True)


if __name__ == "__main__":
    d = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not d.is_dir():
        sys.exit(f"不是文件夹：{d}")
    print(f"👀 盯着 {d}  —— 改任何 .md 都会自动重新生成 board/（Ctrl-C 停）",
          flush=True)
    build(d)
    prev = stamp(d)
    try:
        while True:
            time.sleep(1)
            cur = stamp(d)
            if cur != prev:
                changed_paths = [p for p in cur
                                 if p not in prev or prev[p] != cur[p]]
                changed = [p.name for p in changed_paths]
                print(f"\n📝 {', '.join(changed) or 'a file was deleted'}", flush=True)
                build(d, only=changed)
                prev = cur
    except KeyboardInterrupt:
        print("\n停了。")
