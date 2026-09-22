#!/usr/bin/env python3
"""📄 Paper Workbench · view audit: drive every Space view in REAL headless Chrome.

Wire green is not UI green. This opens `/_board/paper` for one or more paper
boards on a running board server, walks all twenty `#<space>/<view>` routes at
a given window width, and reports layout defects as text:

  page overflow · an element past the right edge · clipped text (ellipsis or
  hidden overflow on a leaf) · type under 11.5px · a view or panel still
  visible while another is active

It writes nothing to the board. With --shots DIR it also saves one full-height
PNG per view. Needs `websocket-client` and a local Chrome.

  python audit_paper_views.py --base http://HOST:PORT \\
      --paper examples/<Project>/papers/<Paper> [--paper …] [--width 1360] [--shots DIR]

Exit code 1 when any view is flagged, so it can gate a change.
"""
import argparse
import base64
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request

import websocket

CHROME = os.environ.get("CHROME_BIN", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
VIEWS = [("setup", "folders"), ("setup", "sessions"),
         ("ideation", "pool"), ("ideation", "evidence"), ("ideation", "admission"),
         ("story", "spine"), ("story", "questions"), ("story", "tasks"), ("story", "sections"), ("story", "evidence"),
         ("run", "page"), ("run", "evidence"), ("run", "supporting"), ("run", "gates"), ("run", "workflow"),
         ("delivery", "manuscript"), ("delivery", "sections"), ("delivery", "displays"), ("delivery", "checks"), ("delivery", "rounds")]

AUDIT = r"""
(() => {
  const S = %s, V = %s, vw = window.innerWidth;
  const vis = el => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
  const tag = el => el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).join('.') : '');
  const panel = document.querySelector('.panel[data-space="' + S + '"]');
  const view = panel && panel.querySelector('.view[data-view="' + V + '"]');
  const out = {exists: !!view, shown: !!(view && vis(view)), docOverflow: document.documentElement.scrollWidth - vw,
               height: document.documentElement.scrollHeight, leaks: 0, wide: [], clipped: [], tiny: 0, tinyEx: [], chars: 0};
  if (!view) return out;
  out.leaks = [...document.querySelectorAll('.view')].filter(v => v !== view && vis(v)).length
            + [...document.querySelectorAll('.panel')].filter(p => p !== panel && vis(p)).length;
  out.chars = view.innerText.length;
  const seenW = new Set(), seenC = new Set();
  for (const el of view.querySelectorAll('*')) {
    if (!vis(el)) continue;
    const r = el.getBoundingClientRect(), cs = getComputedStyle(el);
    if (r.right > vw + 1) { const t = tag(el); if (!seenW.has(t)) { seenW.add(t); out.wide.push(t + ' right=' + Math.round(r.right)); } }
    const leaf = el.children.length === 0 && el.textContent.trim().length > 0;
    if (leaf && !el.title && (cs.overflowX === 'hidden' || cs.textOverflow === 'ellipsis') && el.scrollWidth > el.clientWidth + 1) {
      const t = tag(el); if (!seenC.has(t)) { seenC.add(t); out.clipped.push(t + ': ' + el.textContent.trim().slice(0, 60)); }
    }
    if (leaf && parseFloat(cs.fontSize) < 11.5) { out.tiny++; if (out.tinyEx.length < 3) out.tinyEx.push(tag(el) + ' ' + cs.fontSize + ': ' + el.textContent.trim().slice(0, 30)); }
  }
  out.nClipped = seenC.size; out.clipped = out.clipped.slice(0, 5); out.wide = out.wide.slice(0, 5);
  return out;
})()
"""


class CDP:
    def __init__(self, ws_url):
        self.ws = websocket.create_connection(ws_url, timeout=30, suppress_origin=True)
        self.n = 0

    def call(self, method, **params):
        self.n += 1
        self.ws.send(json.dumps({"id": self.n, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self.n:
                return msg.get("result", {})

    def ev(self, expr):
        r = self.call("Runtime.evaluate", expression=expr, returnByValue=True, awaitPromise=True)
        return r.get("result", {}).get("value")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", required=True, help="the running board server, e.g. http://HOST:PORT")
    ap.add_argument("--paper", action="append", required=True, help="repo-relative paper board folder (repeatable)")
    ap.add_argument("--width", type=int, default=1360)
    ap.add_argument("--shots", default="", help="folder for one full-height PNG per view")
    ap.add_argument("--port", type=int, default=9347, help="Chrome remote-debugging port")
    a = ap.parse_args()
    if a.shots:
        os.makedirs(a.shots, exist_ok=True)
    prof = tempfile.mkdtemp(prefix="paper-audit-chrome-")          # its own profile: a shared one hangs headless Chrome
    proc = subprocess.Popen([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                             "--remote-debugging-port=%d" % a.port, "--user-data-dir=" + prof,
                             "--window-size=%d,1000" % a.width, "about:blank"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    flagged = 0
    try:
        targets = None
        for _ in range(40):
            try:
                targets = json.load(urllib.request.urlopen("http://127.0.0.1:%d/json" % a.port))
                break
            except Exception:
                time.sleep(0.5)
        if not targets:
            sys.exit("Chrome did not open its debugging port")
        c = CDP([t for t in targets if t["type"] == "page"][0]["webSocketDebuggerUrl"])
        c.call("Page.enable")
        c.call("Emulation.setDeviceMetricsOverride", width=a.width, height=1000, deviceScaleFactor=1, mobile=False)
        for rel in a.paper:
            rel = rel.strip("/")
            url = "%s/_board/paper?path=%s&file=board.md" % (a.base.rstrip("/"), urllib.parse.quote("/" + rel + "/board.md", safe=""))
            c.call("Page.navigate", url=url)
            for _ in range(60):
                if c.ev("document.readyState") == "complete":
                    break
                time.sleep(0.25)
            time.sleep(0.6)
            print("=== %s @ %dpx" % (rel.rsplit("/", 1)[-1], a.width))
            for space, view in VIEWS:
                c.ev("location.hash = '#%s/%s'" % (space, view))
                time.sleep(0.35)
                r = c.ev(AUDIT % (json.dumps(space), json.dumps(view)))
                if not r or not r.get("exists"):
                    print("%-9s %-11s (view not on this paper)" % (space, view))
                    continue
                flags = []
                if not r["shown"]:
                    flags.append("NOT SHOWN")
                if r["docOverflow"] > 1:
                    flags.append("page overflows by %dpx" % r["docOverflow"])
                if r["leaks"]:
                    flags.append("%d other view/panel visible" % r["leaks"])
                if r["wide"]:
                    flags.append("past right edge: " + "; ".join(r["wide"]))
                if r["nClipped"]:
                    flags.append("clipped(%d kinds): %s" % (r["nClipped"], " | ".join(r["clipped"])))
                if r["tiny"]:
                    flags.append("tiny type x%d e.g. %s" % (r["tiny"], " | ".join(r["tinyEx"])))
                flagged += bool(flags)
                print("%-9s %-11s h=%-6d chars=%-7d %s" % (space, view, r["height"], r["chars"], "OK" if not flags else "⚠ " + " ‖ ".join(flags)))
                if a.shots:
                    shot = c.call("Page.captureScreenshot", format="png", captureBeyondViewport=True,
                                  clip={"x": 0, "y": 0, "width": a.width, "height": min(int(r["height"]), 9000), "scale": 1})
                    with open(os.path.join(a.shots, "%s-%s-%s.png" % (rel.rsplit("/", 1)[-1], space, view)), "wb") as f:
                        f.write(base64.b64decode(shot["data"]))
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()
        shutil.rmtree(prof, ignore_errors=True)
    print("%d view(s) flagged" % flagged)
    sys.exit(1 if flagged else 0)


if __name__ == "__main__":
    main()
