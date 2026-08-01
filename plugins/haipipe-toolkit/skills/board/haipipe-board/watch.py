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

HERE = Path(__file__).resolve().parent


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
    cmd = [sys.executable, str(HERE / "build.py"), str(d)]
    if (d / "board").is_dir():
        if only:
            cmd += ["--only", ",".join(sorted(only))]
    r = subprocess.run(cmd, capture_output=True, text=True)
    print((r.stdout or r.stderr).strip(), flush=True)


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
