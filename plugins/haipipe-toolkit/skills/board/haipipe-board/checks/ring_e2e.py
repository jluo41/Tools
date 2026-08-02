#!/usr/bin/env python3
"""QD2 §9 R1 · prove the turn outlives the socket that started it.

The defect this pins down was reported for a month in one shape or another and
never had a test: JL would navigate away, switch a setting, or let a long job
run, and the turn's trace was gone — because the trace WAS the HTTP response.
"只有我发一个新的 message 之后，你的 response 才能显现出来" (260801).

The check is deliberately shaped like the complaint rather than like the code:

    1. start a streaming turn on a THROWAWAY fixture
    2. read a few seconds of it, remember the last cursor
    3. HANG UP — close the socket the way a navigation does
    4. POST /_board/attach with that cursor
    5. the rest of the turn must arrive, ending in `done`

Before R1 step 5 returned nothing at all, because there was no ring to rejoin.
Run it with the repo venv (the SDK needs 3.10+):

    .venv/bin/python Tools/.../haipipe-board/checks/ring_e2e.py
"""

import http.client
import json
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
CLI = SKILL / "cli"

# Long enough to still be running when we hang up, cheap enough to run often.
# The whole test depends on the turn being UNFINISHED at step ②, so this asks
# for far more output than the watch window can consume.
PROMPT = ("Count from 1 to 300. Put each number on its own line, and after each "
          "one add a short note of three or four words. Do not use any tools, "
          "and do not stop early or summarise.")
WATCH_S = 4


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def fixture():
    src = SKILL.parent.parent / "diagrams" / "01-boardform-260722"
    work = Path(tempfile.mkdtemp(prefix="board-ring-"))
    fx = work / "b" / src.name
    (work / "b").mkdir(parents=True)
    shutil.copytree(src, fx, ignore=shutil.ignore_patterns(
        "_archive", "*.excalidraw", ".haipipe-board", "board", "fig"))
    # Same reason as checks/run.py: a copied `session:` header would --resume a
    # conversation whose jsonl lives under the REAL repo's project dir.
    for md in fx.rglob("*.md"):
        lines = md.read_text(encoding="utf-8").splitlines(True)
        keep = [ln for ln in lines if not ln.startswith("session: ")]
        if len(keep) != len(lines):
            md.write_text("".join(keep), encoding="utf-8")
    r = subprocess.run([sys.executable, str(CLI / "build.py"), str(fx)],
                       capture_output=True, text=True)
    if "✅" not in (r.stdout or ""):
        print("fixture build FAILED:\n" + (r.stdout + r.stderr)[-1200:])
        sys.exit(1)
    return work / "b", src.name


def post_stream(port, path, payload):
    """Open a streaming POST and hand back the raw connection, unread."""
    c = http.client.HTTPConnection("127.0.0.1", port, timeout=180)
    c.request("POST", path, json.dumps(payload),
              {"Content-Type": "application/json"})
    return c, c.getresponse()


def read_events(resp, seconds=None, until_done=False):
    """Pull NDJSON events off a live response. Returns (events, raw_tail)."""
    evs, buf, t0 = [], b"", time.time()
    while True:
        if seconds and time.time() - t0 > seconds:
            break
        chunk = resp.read(1)
        if not chunk:
            break
        buf += chunk
        if not buf.endswith(b"\n"):
            continue
        for ln in buf.decode("utf-8", "replace").splitlines():
            if not ln.strip():
                continue
            try:
                evs.append(json.loads(ln))
            except ValueError:
                pass
        buf = b""
        if until_done and evs and evs[-1].get("t") == "done":
            break
    return evs


def main():
    root, boardname = fixture()
    port = free_port()
    srv = subprocess.Popen(
        [sys.executable, str(CLI / "serve.py"), "--root", str(root),
         "--port", str(port), "--host", "127.0.0.1"],
        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    board_url = f"/{boardname}/board/index.html"
    fails = []
    try:
        for _ in range(80):
            try:
                urllib.request.urlopen(
                    f"http://127.0.0.1:{port}{board_url}", timeout=2).read()
                break
            except Exception:
                if srv.poll() is not None:
                    print("server died:\n" + srv.stderr.read().decode()[:1500])
                    return 1
                time.sleep(0.25)

        target = {"path": board_url, "file": "board.md"}

        # ── 1-2 · start the turn, watch a little of it ──────────────────
        print("① starting a turn…", flush=True)
        conn, resp = post_stream(port, "/_board/chat", dict(
            target, message=PROMPT, stream=True, scope="scoped",
            model="haiku", effort="low", session="new"))
        if resp.status != 200:
            print(f"   chat refused: HTTP {resp.status} {resp.read()[:300]}")
            return 1
        seen = read_events(resp, seconds=WATCH_S)
        cursor = max([e.get("n", -1) for e in seen] + [-1]) + 1
        kinds = sorted({e.get("t") for e in seen})
        print(f"   saw {len(seen)} events {kinds}, cursor now {cursor}")
        if cursor == 0:
            fails.append("no events carried a cursor `n` — the ring never filled")
        if any(e.get("t") == "done" for e in seen):
            fails.append(f"the turn finished inside the {WATCH_S}s watch window, "
                         "so nothing was left to rejoin — lengthen PROMPT")
            return report(fails, srv)

        # ── 3 · hang up, the way navigating away does ───────────────────
        print("② hanging up mid-turn (socket closed, no ⏹)…", flush=True)
        conn.close()
        time.sleep(2)

        # ── 4-5 · rejoin and demand the rest ───────────────────────────
        print(f"③ re-attaching at cursor {cursor}…", flush=True)
        c2, r2 = post_stream(port, "/_board/attach",
                             dict(target, cursor=cursor))
        if r2.status != 200:
            fails.append(f"attach returned HTTP {r2.status}")
            return report(fails, srv)
        ctype = r2.getheader("Content-Type") or ""
        if "ndjson" not in ctype:
            body = json.loads(r2.read() or b"{}")
            fails.append("attach found no live turn to rejoin "
                         f"(live={body.get('live')}) — the turn died with its socket")
            return report(fails, srv)
        rest = read_events(r2, seconds=180, until_done=True)
        c2.close()
        got = sorted({e.get("t") for e in rest})
        print(f"   rejoined and read {len(rest)} more events {got}")

        done = next((e for e in rest if e.get("t") == "done"), None)
        if done is None:
            fails.append("the rejoined stream never reached `done`")
        else:
            txt = (done.get("text") or "").strip()
            print(f"   done · {len(txt)} chars · session {(done.get('session') or '')[:8]}")
            if len(txt) < 40:
                fails.append(f"`done` carried almost no text ({len(txt)} chars)")
            if not done.get("session"):
                fails.append("`done` carried no session id, so nothing resumes")
        low = [e for e in rest if e.get("n", 0) < cursor and e.get("t") != "gap"]
        if low:
            fails.append(f"attach replayed {len(low)} events the reader already had")
        if not any(e.get("n", -1) >= cursor for e in rest):
            fails.append("attach delivered nothing at or past the cursor")

        # ── 6 · a FINISHED turn must NOT be re-streamed ────────────────
        # Found by driving a real browser: the drawer rejoins on open, on focus
        # and on a 25s heartbeat, so a finished-but-still-buffered ring was
        # re-attached over and over and its `done` re-rendered each time — one
        # duplicate answer bubble per heartbeat. Once a turn has ended the
        # transcript is the right source; the ring only covers the live window.
        print("④ re-attaching AFTER the turn ended (must decline)…", flush=True)
        c3, r3 = post_stream(port, "/_board/attach", dict(target, cursor=0))
        ctype3 = r3.getheader("Content-Type") or ""
        body3 = {}
        if "ndjson" not in ctype3:
            try:
                body3 = json.loads(r3.read() or b"{}")
            except ValueError:
                pass
        c3.close()
        print(f"   answered live={body3.get('live')} ended={body3.get('ended')}")
        if "ndjson" in ctype3:
            fails.append("a finished turn was streamed again — every heartbeat "
                         "would repaint its answer")
        elif body3.get("live") is not False or body3.get("ended") is not True:
            fails.append(f"expected live:false ended:true, got {body3}")
    finally:
        srv.terminate()
        shutil.rmtree(root.parent, ignore_errors=True)
    return report(fails, srv)


def report(fails, srv):
    print()
    if fails:
        for f in fails:
            print(f"❌ {f}")
        return 1
    print("✅ R1: the turn outlived the socket, and a rejoin got the rest of it")
    return 0


if __name__ == "__main__":
    sys.exit(main())
