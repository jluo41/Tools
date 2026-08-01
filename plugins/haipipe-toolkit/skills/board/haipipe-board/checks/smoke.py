#!/usr/bin/env python3
"""Smoke tier: is the LIVE board healthy, right now? Seconds, read-only.

Every check here answers a failure that actually happened on 260731 and was
invisible until someone clicked:
  - the server restarted on system python 3.9 -> SDK chat 400s while every
    page still serves 200  (the venv check)
  - a shipped board.js never reached the tree because nothing rebuilt it
    (the assets-fresh check)
  - watch.py not running -> Sync writes land in .md but the html goes stale

Run against the REAL server; spawns nothing, writes nothing.

    python3 checks/smoke.py [--host 127.0.0.1] [--port 5599] [--board <path>]

--board is the board dir relative to the server's --root; default is the
family's own design board.
"""
import argparse
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent      # the skill dir
DEFAULT_BOARD = "Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722"

results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f" · {detail}" if detail else ""))
    return ok


def get(url, timeout=5):
    return urllib.request.urlopen(url, timeout=timeout).read().decode("utf-8", "replace")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=5599)
    ap.add_argument("--board", default=DEFAULT_BOARD)
    a = ap.parse_args()
    base = f"http://{a.host}:{a.port}"

    # ① the tree serves (canonical since JL discarded board.html, 260731);
    #    board.html only matters while the file still exists on disk
    try:
        tree = get(f"{base}/{a.board}/board/index.html")
    except Exception as e:
        check("server serves board/ tree index", False, str(e)[:80])
    else:
        check("server serves board/ tree index", len(tree) > 3000)
    try:
        get(f"{base}/{a.board}/board.html")
        check("board.html serves (legacy, still on disk)", True)
    except Exception:
        print("      board.html absent — discarded per JL 260731, tree is canonical")

    # ② the RUNNING server can import claude_agent_sdk (the 3.9 trap: pages
    #    200 while every chat turn dies). Only the process itself can answer —
    #    ps shows the venv symlink RESOLVED to the bare interpreter, and
    #    re-running that binary outside the venv loses the site-packages.
    try:
        h = json.loads(get(f"{base}/_board/health"))
        check("server python imports claude_agent_sdk", bool(h.get("sdk")),
              f"python {h.get('python')}")
    except Exception as e:
        check("server answers /_board/health", False,
              f"{str(e)[:60]} — server predates 0.88.0, restart it")

    # ③ the tree's assets are the CURRENT assets (a shipped board.js that never
    #    reached board/_assets/ = every tree page runs old code)
    sys.path.insert(0, str(HERE))
    from src import assets as _a       # the parts, assembled
    src_js = _a.js()
    served_root = None
    try:
        served_root = subprocess.run(
            ["pgrep", "-fl", "serve.py --root"], capture_output=True, text=True
        ).stdout
        m = re.search(r"--root\s+(\S+)", served_root or "")
        root = Path(m.group(1)) if m else None
    except Exception:
        root = None
    tree_js = root / a.board / "board" / "_assets" / "board.js" if root else None
    if tree_js and tree_js.exists():
        check("tree _assets/board.js is current",
              tree_js.read_text(encoding="utf-8") == src_js,
              "rebuild with --split if FAIL")
    else:
        check("tree _assets/board.js exists", False, str(tree_js))

    # ④ watch.py is rebuilding on .md edits
    w = subprocess.run(["pgrep", "-f", "watch.py"], capture_output=True, text=True)
    check("watch.py running", w.returncode == 0)

    # ⑤ the claude binary the terminal spawns
    c = subprocess.run(["which", "claude"], capture_output=True, text=True)
    check("claude binary on PATH", c.returncode == 0, c.stdout.strip())

    # ⑥ node for the browser suites (full tier needs it)
    n = subprocess.run(["node", "--version"], capture_output=True, text=True)
    check("node available (full tier)", n.returncode == 0, n.stdout.strip())

    ok = all(results)
    print(f"\n{'ALL PASS' if ok else str(results.count(False)) + ' FAILURES'} · {len(results)} smoke checks")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
