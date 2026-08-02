#!/usr/bin/env python3
"""QD5 · the gap checks: everything checks/splitshell.mjs does NOT cover.

    python3 checks/splitgaps.py

splitshell.mjs proves the split's own mechanics against the family's real board.
These four prove the claims that suite leaves untested, and they need to WRITE —
a comment lands in a page's Markdown and the pane is expected to repaint — so
they run on a throwaway fixture with its own server, never on a real board. Same
shape as run.py's full tier: build a fixture, serve it, drive a Chrome of its
own, tear all three down.

  G1  an ORDINARY board page is unchanged     the regression surface of the
      (router still swaps, live-refresh       split: `70-router.js` and
      still refreshes in place, no reload)    `20-live-refresh.js` run on every
                                              page, and the pane guards must be
                                              no-ops outside a pane
  G2  a pane refresh keeps your place         A2.3
  G3  a pane's page reads with JS stripped    A3.3, on the SERVED pane rather
                                              than on the built file
  G4  a write through the server repaints     A3.1 · P1, through the same
      the pane, and only the pane             endpoint the drawer and the
                                              terminal both post to
"""
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

BOARD_MD = """# QD5 gap fixture: a board that exists to be written to

spine: Two pages and one sentence to comment on. Nothing here is read by a human; it exists so the split's write path can be driven end to end without touching a real board.
close: Never. This folder is rebuilt from scratch on every run.

## Topic
A fixture board for checks/splitgaps.py.
"""

Q1 = """# The page a pane shows

state: 🟡 fixture
owner: CC
method: hold one stable sentence for the write test to comment on

## Question
Does a pane repaint when this page's Markdown changes?

The quick brown fox jumps over the lazy dog.
This second sentence exists so the first one is not the only anchor.

""" + "\n".join(
    # UNDER `## Question`, which renders OPEN. Filler inside `## Content` sits in
    # a drawer that ships shut, so the page was not actually taller than the
    # frame and G2's scroll had nothing to scroll (its first two runs).
    f"Filler line {i} keeps this page tall enough that a scroll position is a real thing to lose."
    for i in range(1, 120)
) + """

## Content

### C1 · A section with a drawer in it

<details><summary>A drawer that starts shut</summary>

Its open state is what A2.3 promises to carry across a refresh.

</details>
"""

Q2 = """# A second page, so the sidebar has somewhere to go

state: 🟡 fixture
owner: CC
method: exist

## Question
Is there a second page to click to?

There is.
"""


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def main():
    work = Path(tempfile.mkdtemp(prefix="board-splitgaps-"))
    fx = work / "gapfixture"
    fx.mkdir(parents=True)
    # AT THE BOARD ROOT, not in a group folder: `target()` resolves a write as
    # `<board>/<file>` and does not walk subfolders, so a fixture page in a
    # folder is a page the write path cannot find (which is what G4 reported
    # the first time this ran).
    (fx / "board.md").write_text(BOARD_MD, encoding="utf-8")
    (fx / "QA1-thepage.md").write_text(Q1, encoding="utf-8")
    (fx / "QA2-second.md").write_text(Q2, encoding="utf-8")
    print(f"fixture: {fx}", flush=True)

    r = subprocess.run([sys.executable, str(SKILL / "cli" / "build.py"), str(fx)],
                       capture_output=True, text=True)
    if "✅" not in (r.stdout or ""):
        print("fixture build FAILED:\n" + (r.stdout + r.stderr)[-2000:])
        return 1

    port, cdp = free_port(), free_port()
    base = f"http://127.0.0.1:{port}"
    srv = subprocess.Popen(
        [sys.executable, str(SKILL / "cli" / "serve.py"), "--root", str(work),
         "--port", str(port), "--host", "127.0.0.1"],
        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    prof = work / "chrome"
    chrome = subprocess.Popen(
        [CHROME, "--headless=new", f"--remote-debugging-port={cdp}",
         f"--user-data-dir={prof}", "--window-size=1600,1000",
         "--no-first-run", "--no-default-browser-check", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(80):
            try:
                urllib.request.urlopen(
                    base + "/gapfixture/board/index.html", timeout=2).read()
                break
            except Exception:
                if srv.poll() is not None:
                    print("fixture server died:\n"
                          + srv.stderr.read().decode()[:2000])
                    return 1
                time.sleep(0.25)
        for _ in range(80):
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{cdp}/json", timeout=2).read()
                break
            except Exception:
                time.sleep(0.25)

        env = dict(os.environ,
                   CHECK_HOSTPORT=f"127.0.0.1:{port}",
                   CHECK_CDP=f"127.0.0.1:{cdp}",
                   CHECK_BOARD_URL="/gapfixture",
                   CHECK_FIXTURE=str(fx),
                   CHECK_PY=sys.executable,
                   CHECK_SKILL=str(SKILL))
        out = subprocess.run(["node", str(HERE / "splitgaps.mjs")], env=env)
        return out.returncode
    finally:
        for p in (chrome, srv):
            try:
                p.terminate()
                p.wait(timeout=5)
            except Exception:
                try:
                    p.kill()
                except Exception:
                    pass
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
