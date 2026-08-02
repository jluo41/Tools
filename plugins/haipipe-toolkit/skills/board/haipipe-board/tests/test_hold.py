#!/usr/bin/env python3
"""QD2 M1 proof: does holding the client actually remove the per-message boot?

The QC8 gate deliberately never calls /_board/chat (it costs money and needs a
login), so it can only prove M1 broke nothing else. This one drives two real
turns at the cheapest tier and reports first-token latency for each. The claim
under test is narrow: turn two should not pay a boot.

Run it with the SPACE's own venv, which is where claude_agent_sdk lives; system
python3 is 3.9 and the SDK needs 3.10+, so the endpoint just answers 400.

    .venv/bin/python test_hold.py                      # held (M1)
    HAIBOARD_NO_HOLD=1 .venv/bin/python test_hold.py    # the pre-M1 path
    M1_SCOPE=full .venv/bin/python test_hold.py         # the tier that boots skills
"""
import json
import os
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent  # the engine dir
# the SDK needs 3.10+; the repo venv is where claude_agent_sdk lives (QD2)
VENV = HERE.parents[5] / ".venv" / "bin" / "python"
PY_EXE = str(VENV) if VENV.exists() else sys.executable


def turn(base, board_url, page, msg):
    """One streamed turn; returns (seconds to first text, total seconds, reply)."""
    body = json.dumps({
        "path": board_url, "file": page, "message": msg, "stream": True,
        "model": os.environ.get("M1_MODEL", "haiku"),
        "effort": "low",
        "scope": os.environ.get("M1_SCOPE", "scoped"),
    }).encode()
    t0 = time.time()
    first, text, sid = None, [], None
    r = urllib.request.urlopen(urllib.request.Request(
        base + "/_board/chat", data=body,
        headers={"Content-Type": "application/json"}), timeout=300)
    for raw in r:
        line = raw.decode("utf-8", "replace").strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except Exception:
            continue
        if ev.get("t") in ("delta", "text") and first is None:
            first = time.time() - t0
        if ev.get("t") == "delta":
            text.append(ev.get("text", ""))
        if ev.get("t") == "done":
            sid = ev.get("session")
            if not text:
                text.append(ev.get("text", ""))
    return first, time.time() - t0, "".join(text).strip()[:60], sid


def main():
    frozen = Path("/tmp/qc8-fixture")
    work = Path("/tmp/m1-test")
    if work.exists():
        shutil.rmtree(work)
    (work / "b").mkdir(parents=True)
    shutil.copytree(frozen, work / "b" / "01-boardform-260722")
    s = socket.socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
    proc = subprocess.Popen(
        [PY_EXE, str(HERE / "cli" / "serve.py"), "--root", str(work / "b"),
         "--port", str(port), "--host", "127.0.0.1"],
        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    base, board_url = f"http://127.0.0.1:{port}", "/01-boardform-260722/board.html"
    page = "QA-design/QA0-three-folders.md"
    try:
        for _ in range(80):
            try:
                urllib.request.urlopen(base + board_url, timeout=2).read()
                break
            except Exception:
                if proc.poll() is not None:
                    print(proc.stderr.read().decode()[:2000]); return 2
                time.sleep(0.25)
        mode = ("PRE-M1 (a client per POST)" if os.environ.get("HAIBOARD_NO_HOLD")
                else "M1 (one held client)") + \
               f"  ·  tier={os.environ.get(chr(77)+chr(49)+chr(95)+chr(83)+chr(67)+chr(79)+chr(80)+chr(69), chr(115)+chr(99)+chr(111)+chr(112)+chr(101)+chr(100))}"
        print(f"mode: {mode}\n")
        rows = []
        for i, m in enumerate(["Reply with exactly: ONE", "Reply with exactly: TWO"], 1):
            f, tot, txt, sid = turn(base, board_url, page, m)
            rows.append((i, f, tot, txt, sid))
            print(f"  turn {i}: first token {f if f is None else round(f,2)}s · "
                  f"total {round(tot,2)}s · reply {txt!r} · session {str(sid)[:8]}")
        if len(rows) == 2 and rows[0][1] and rows[1][1]:
            saved = rows[0][1] - rows[1][1]
            print(f"\n  turn 2 was {round(saved,2)}s faster to first token "
                  f"({round(100*saved/rows[0][1])}% less wait)")
        if rows[0][4] and rows[0][4] == rows[1][4]:
            print(f"  same session across both turns: {rows[0][4][:8]} ✅")
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=8)
        except Exception:
            proc.kill()
    return 0


if __name__ == "__main__":
    sys.exit(main())
