#!/usr/bin/env python3
"""Watch a board folder and rebuild board.html whenever a .md changes.

    python3 watch.py <board-dir>

Why this exists: the browser's "Sync to md" button writes your comments straight
into the Q files, but it cannot run Python — so board.html stays stale until
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
    return {p: p.stat().st_mtime for p in sorted(d.glob("*.md"))}


def build(d):
    r = subprocess.run([sys.executable, str(HERE / "build.py"), str(d)],
                       capture_output=True, text=True)
    print((r.stdout or r.stderr).strip(), flush=True)


if __name__ == "__main__":
    d = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not d.is_dir():
        sys.exit(f"不是文件夹：{d}")
    print(f"👀 盯着 {d}  —— 改任何 .md 都会自动重新生成 board.html（Ctrl-C 停）",
          flush=True)
    build(d)
    prev = stamp(d)
    try:
        while True:
            time.sleep(1)
            cur = stamp(d)
            if cur != prev:
                changed = [p.name for p in cur
                           if p not in prev or prev[p] != cur[p]]
                print(f"\n📝 {', '.join(changed) or '有文件被删'}", flush=True)
                build(d)
                prev = cur
    except KeyboardInterrupt:
        print("\n停了。")
