#!/usr/bin/env python3
"""The ANCHOR PARITY sweep: can every sentence on this board still be written to?

    python3 sentencerun.py <board-dir> [--port 9222] [--url http://127.0.0.1:5599]

QF5 rules this. A sentence operation (edit, add a lane, comment) is an EXACT
string match between three components that are written in three languages and
have no reason to agree:

    ①  build.py            renders a source line into HTML
    ②  __boardSentenceText reads that HTML back into a string, in the browser
    ③  _sentence_line      finds that string among the source lines, in Python

Every failure this family has shipped in this area was ① changing and ② not
following: the ⚑ badge moved inside the <p> and every write on a sentence
carrying apparatus began failing silently (260801). Nothing caught it, because
the markdown was valid, the page built, and the checker reads ① alone.

This run asks the REAL page, in a REAL browser, what it WOULD post for every
writable sentence, and resolves each answer with the server's OWN matcher. It
posts nothing and writes nothing: it needs no fixture, no undo, and it can be
run against a live board at any time.

A third implementation of "what does this sentence say" would defeat the whole
point, so there is none here: ② is called in the page and ③ is imported.

Exit 1 if any sentence cannot be resolved.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent  # the engine dir (this file lives in cli/)
sys.path.insert(0, str(HERE))

from live.write import WriteMixin        # noqa: E402  — ③, imported not copied
from src.common import page_files        # noqa: E402

# Ask the page itself what it would send. `.sentence-target` is what the
# address pass marks as writable, and a summary's <p> is the same thing once a
# sentence has gained apparatus (that shape is exactly what broke).
PROBE = """
(() => {
  const read = window.__boardSentenceText;
  if (!read) return {err: 'this page has no __boardSentenceText'};
  const out = [];
  document.querySelectorAll('section.slide.q').forEach(q => {
    const file = q.getAttribute('data-file') || '';
    const seen = new Set();
    q.querySelectorAll('p').forEach(p => {
      if (p.closest('.sapp,.cmt,.cmb,.change,.lane,.dadd,.sadd,.sedit,.nav,.idx')) return;
      const shape = p.closest('details.sent') ? 'apparatus' : 'plain';
      const text = read(p);
      if (!text || text.length < 12) return;
      const key = shape + '\\u0000' + text;
      if (seen.has(key)) return;
      seen.add(key);
      out.push({file, shape, text});
    });
  });
  return {rows: out};
})()
"""


def new_tab(port):
    """A tab of OUR OWN. Attaching to whatever tab happens to be first drives
    the tab a person is reading, and a run that navigates 57 pages under
    someone's cursor is both rude and unreliable: their tab can be mid-dialog
    or busy, and the socket simply times out (260801)."""
    req = urllib.request.Request(f"http://127.0.0.1:{port}/json/new?about:blank",
                                 method="PUT")
    try:
        return json.load(urllib.request.urlopen(req, timeout=10))
    except urllib.error.HTTPError:                        # older Chrome: GET
        return json.load(urllib.request.urlopen(
            f"http://127.0.0.1:{port}/json/new?about:blank", timeout=10))


class Browser:
    def __init__(self, port):
        import websocket                 # noqa: PLC0415 — optional dependency
        self.port = port
        self.tab = new_tab(port)
        self.ws = websocket.create_connection(self.tab["webSocketDebuggerUrl"],
                                              suppress_origin=True, timeout=30)
        self.i = 0

    def close(self):
        try:
            urllib.request.urlopen(
                f"http://127.0.0.1:{self.port}/json/close/{self.tab['id']}", timeout=5)
        except Exception:                                  # noqa: BLE001
            pass

    def cmd(self, method, **params):
        self.i += 1
        self.ws.send(json.dumps({"id": self.i, "method": method, "params": params}))
        while True:
            m = json.loads(self.ws.recv())
            if m.get("id") == self.i:
                if "error" in m:
                    raise RuntimeError(m["error"])
                return m.get("result", {})

    def open(self, url, settle=1.6):
        # No `Page.enable`: on a freshly created tab it never answers on this
        # Chrome build and the socket simply times out (260801). Nothing here
        # needs page events; navigate and settle is enough.
        import time
        self.cmd("Page.navigate", url=url)
        time.sleep(settle)

    def js(self, expr):
        r = self.cmd("Runtime.evaluate", expression=expr, returnByValue=True,
                     awaitPromise=True)
        if "exceptionDetails" in r:
            raise RuntimeError(json.dumps(r["exceptionDetails"])[:300])
        return r.get("result", {}).get("value")


def tree_url(base, board, root, page):
    """The built page for one source file, in the board/ tree.

    `?pane=page` asks for the PAGE, not the shell around it. Without it the
    server answers with the three-pane frame and the real document loads in an
    iframe, so `Runtime.evaluate` reads the shell's window, finds no reader and
    reports every page unreadable. That is what it did on 260802: 55 of 55
    pages SKIPPED, which looks exactly like a run nobody bothered to read.
    """
    rel = page.relative_to(board)
    group = rel.parts[0].split("-", 1)[0] if len(rel.parts) > 1 else ""
    name = rel.stem + ".html?pane=page"
    stem = board.resolve().relative_to(root.resolve()).as_posix()
    return f"{base}/{stem}/board/{group}/{name}" if group else f"{base}/{stem}/board/{name}"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("board")
    ap.add_argument("--port", type=int, default=9222, help="Chrome CDP port")
    ap.add_argument("--url", default="http://127.0.0.1:5599", help="serve.py origin")
    ap.add_argument("--root", default="", help="repo root serve.py was started with")
    ap.add_argument("--only", default="", help="substring filter on page filenames")
    a = ap.parse_args()

    board = Path(a.board).resolve()
    root = Path(a.root).resolve() if a.root else board.parents[4]
    pages = [p for p in page_files(board) if a.only in p.name]
    if not pages:
        print("no pages", file=sys.stderr)
        return 1

    try:
        br = Browser(a.port)
    except Exception as e:                        # noqa: BLE001
        print(f"⚠️  no browser on CDP port {a.port}: {e}\n"
              "    start Chrome with --remote-debugging-port and install "
              "websocket-client; SKIPPED rather than passed.", file=sys.stderr)
        return 2

    checked = shapes = 0
    bad, unreadable = [], []
    per_shape = {}
    for p in pages:
        # One wedged page must not end the sweep: a run that dies at page 12
        # reports nothing about pages 13 to 60, which is indistinguishable from
        # a clean board (260801, a socket timeout on the sixth page).
        try:
            br.open(tree_url(a.url, board, root, p))
            r = br.js(PROBE)
        except Exception as e:                    # noqa: BLE001
            unreadable.append((p.name, f"{type(e).__name__}: {e}"))
            try:
                br = Browser(a.port)              # a fresh tab, and carry on
            except Exception:                     # noqa: BLE001
                break
            continue
        if not r or "rows" not in r:
            unreadable.append((p.name, (r or {}).get("err", "no answer")))
            continue
        for row in r["rows"]:
            src = board / row["file"] if row["file"] else p
            if not src.is_file():
                bad.append((p.name, row["shape"], row["text"], f"no source file {row['file']}"))
                continue
            lines = src.read_text(encoding="utf-8").split("\n")
            hit, err = WriteMixin._sentence_line(lines, row["text"])
            checked += 1
            per_shape[row["shape"]] = per_shape.get(row["shape"], 0) + 1
            if hit is None:
                bad.append((p.name, row["shape"], row["text"], err))

    br.close()
    shapes = len(per_shape)
    for name, why in unreadable:
        print(f"SKIP  {name:<44} {why}")
    for name, shape, text, err in bad:
        print(f"FAIL  {name:<40} [{shape}] {text[:56]!r}\n      {err}")
    tally = " · ".join(f"{k} {v}" for k, v in sorted(per_shape.items()))
    print(f"\n{len(pages)} pages · {checked} writable sentences · {shapes} shapes ({tally})"
          f" · {len(bad)} unanchored · {len(unreadable)} unreadable")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
