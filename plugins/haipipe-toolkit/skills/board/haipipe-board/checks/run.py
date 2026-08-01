#!/usr/bin/env python3
"""The board's standing checklist: every hard 'Items to Finish' condition that
can be executed, executed (JL 260731: "checklist 就是 item to finish — 要时刻
保证它们永远是被 check 的").

Two tiers:

  python3 checks/run.py                  # smoke: the LIVE server, seconds,
                                         # read-only (see smoke.py)
  python3 checks/run.py --full           # + real turns on a THROWAWAY fixture
                                         # board with its own server + Chrome:
                                         #   pty_e2e.py    ⌨ engine, real CLI turn
                                         #   termnav.mjs   ⌨ follows the tree
                                         #                 router, park-not-held,
                                         #                 paste  (real browser)
                                         #   one SDK chat turn (💬 answers)

The full tier never touches a real board: a standing check must not rewrite a
real page's `session:` header or leave rows in a real registry. Fixture shape
copied from gate_live.py (QC8).

Board items each check guards:
  QD3 ⑤ park & reattach      -> termnav T9c/T9d (reused:true), pty_e2e ⑥
  QD3 own-PTY engine         -> pty_e2e ①-⑦
  QD1 one scope one window   -> termnav T9b (old PTY parked, new paints)
  QD2 chat answers a turn    -> the SDK turn below + smoke's venv check
  QD3m paste                 -> termnav T9b'
"""
import argparse
import json
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent          # checks/
SKILL = HERE.parent                             # the skill dir
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def post(base, path, payload, timeout=180):
    r = urllib.request.urlopen(urllib.request.Request(
        base + path, json.dumps(payload).encode(),
        {"Content-Type": "application/json"}), timeout=timeout)
    return json.loads(r.read())


def full_tier():
    src = SKILL.parent.parent / "diagrams" / "01-boardform-260722"
    work = Path(tempfile.mkdtemp(prefix="board-checks-"))
    fx = work / "b" / src.name
    (work / "b").mkdir(parents=True)
    shutil.copytree(src, fx, ignore=shutil.ignore_patterns(
        "_archive", "*.excalidraw", ".haipipe-board", "board", "fig"))
    # A fixture has no session identity: the copied pages carry the REAL
    # board's `session:` headers, and a fixture spawn would --resume a session
    # whose jsonl lives under the real repo's project dir (found when pty_e2e
    # booted but the turn never answered). Strip them; every spawn is fresh.
    for md in fx.rglob("*.md"):
        lines = md.read_text(encoding="utf-8").splitlines(True)
        keep = [ln for ln in lines if not ln.startswith("session: ")]
        if len(keep) != len(lines):
            md.write_text("".join(keep), encoding="utf-8")
    print(f"fixture: {fx}", flush=True)
    r = subprocess.run([sys.executable, str(SKILL / "build.py"), str(fx), "--split"],
                       capture_output=True, text=True)
    if "✅" not in (r.stdout or ""):
        print("fixture build FAILED:\n" + (r.stdout + r.stderr)[-1500:])
        return 1

    port, cdp = free_port(), free_port()
    base = f"http://127.0.0.1:{port}"
    board_url = f"/{src.name}"
    srv = subprocess.Popen(
        [sys.executable, str(SKILL / "serve.py"), "--root", str(work / "b"),
         "--port", str(port), "--host", "127.0.0.1"],
        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    chrome = None
    fails = 0
    try:
        for _ in range(80):
            try:
                urllib.request.urlopen(base + board_url + "/board/index.html",
                                       timeout=2).read()
                break
            except Exception:
                if srv.poll() is not None:
                    print("fixture server died:\n" + srv.stderr.read().decode()[:2000])
                    return 1
                time.sleep(0.25)

        env = dict(__import__("os").environ,
                   CHECK_HOST="127.0.0.1", CHECK_PORT=str(port),
                   CHECK_BOARD=src.name,
                   CHECK_HOSTPORT=f"127.0.0.1:{port}",
                   CHECK_BOARD_URL=board_url,
                   CHECK_CDP=f"127.0.0.1:{cdp}",
                   CHECK_FIGDIR=str(fx / "fig"))

        print("\n── pty_e2e (⌨ engine, real CLI turn) " + "─" * 30, flush=True)
        r = subprocess.run([sys.executable, str(HERE / "pty_e2e.py")], env=env)
        fails += r.returncode != 0

        print("\n── one SDK chat turn (💬 answers) " + "─" * 33, flush=True)
        try:
            j = post(base, "/_board/chat",
                     {"path": board_url + "/board.html", "file": "board.md",
                      "message": "reply with exactly CHATOK and nothing else",
                      "scope": "scoped"})
            ok = "CHATOK" in (j.get("text") or "")
            print(("PASS" if ok else "FAIL") + "  SDK turn answered · "
                  + (j.get("text") or str(j))[:80])
            fails += not ok
        except Exception as e:
            print(f"FAIL  SDK turn · {e}")
            fails += 1

        print("\n── termnav (⌨ follows the tree router, real browser) " + "─" * 14, flush=True)
        prof = work / "chrome"
        chrome = subprocess.Popen(
            [CHROME, "--headless=new", f"--remote-debugging-port={cdp}",
             f"--user-data-dir={prof}", "--no-first-run",
             "--no-default-browser-check", "--window-size=1500,950",
             "about:blank"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(40):
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{cdp}/json/version",
                                       timeout=2).read()
                break
            except Exception:
                time.sleep(0.25)
        r = subprocess.run(["node", str(HERE / "termnav.mjs")], env=env)
        fails += r.returncode != 0

        # belt: no orphan PTY may outlive the tier
        try:
            for t in post(base, "/_board/terms", {}).get("terms", []):
                print(f"reaping leftover PTY {t.get('key')}")
                post(base, "/_board/release",
                     {"path": board_url + "/board.html", "file": t.get("file", "board.md")})
        except Exception:
            pass
    finally:
        if chrome:
            chrome.terminate()
        srv.terminate()
        try:
            srv.wait(timeout=5)
        except Exception:
            srv.kill()
        shutil.rmtree(work, ignore_errors=True)
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true",
                    help="also run real CLI/SDK turns on a throwaway fixture")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", default="5599")
    a = ap.parse_args()

    print("── smoke (the live server) " + "─" * 40)
    rc = subprocess.run([sys.executable, str(HERE / "smoke.py"),
                         "--host", a.host, "--port", a.port]).returncode
    if not a.full:
        return rc
    rc2 = full_tier()
    print("\n" + ("ALL TIERS GREEN" if rc == 0 and rc2 == 0 else "FAILURES — see above"))
    return rc or rc2


if __name__ == "__main__":
    sys.exit(main())
