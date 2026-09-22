#!/usr/bin/env python3
"""Response-identical gate for a serve.py refactor.

Drives a real server against a THROWAWAY copy of one Board and records, per run:
  · every response (status, length, sha256 of the normalized body, a short head)
    for a fixed script of GET / HEAD / POST requests over the reader routes,
    the static asset bundle, and every workbench route;
  · the normalized bytes of every .md / .html / .css / .js in the fixture afterwards.

    python3 servers/_host/tests/gate_live.py --fixture <board-folder> \
        --file <page-rel> --save before.json
    ... refactor ...
    python3 servers/_host/tests/gate_live.py --fixture <same> \
        --file <same> --save after.json --diff before.json

`--serve` defaults to the sibling `../serve.py`; pass the old entry point to
record a baseline before a move. Requires a Python with PyYAML for the build.

A clean diff means the move was mechanical. Normalization blanks only what is
allowed to differ between two runs (clocks, uuids, terminal keys, filesystem
timestamps); each rule is narrow and named so a real change cannot hide behind one.
"""
import argparse
import hashlib
import json
import re
import shutil
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def norm(text):
    rules = [
        (r'"session":\s*"[0-9a-f-]{36}"', '"session":"<uuid>"'),
        (r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b', '<uuid>'),
        (r'\b\d{6}-\d{6}\b', '<stamp>'),
        (r'\b\d{6} \d{4}\b', '<stamp>'),
        (r'"(mtime|size|ts|started_at|ended_at|seconds|generated|built)":\s*[0-9.]+', r'"\1":<num>'),
        (r'\b\d{2}:\d{2}(:\d{2})?\b', '<time>'),
        (r'/_term/[0-9a-f]{12}/', '/_term/<key>/'),
        (r'"key":\s*"[0-9a-f]{12}"', '"key":"<key>"'),
        (r'\b20\d{2}-\d{2}-\d{2}T[0-9:.+-]+', '<iso>'),
        (r'"python":\s*"[0-9.]+"', '"python":"<py>"'),
    ]
    for pat, rep in rules:
        text = re.sub(pat, rep, text)
    return text


def call(base, path, payload=None, method=None):
    url = base + path
    try:
        req = urllib.request.Request(url, method=method) if payload is None else urllib.request.Request(
            url, data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"})
        r = urllib.request.urlopen(req, timeout=30)
        body, code = r.read(), r.status
    except urllib.error.HTTPError as e:
        body, code = e.read(), e.code
    except Exception as e:
        return {"code": -1, "err": type(e).__name__ + ": " + str(e)[:120]}
    txt = norm(body.decode("utf-8", "replace"))
    return {"code": code, "len": len(txt), "sha": hashlib.sha256(txt.encode()).hexdigest(),
            "head": txt[:300]}


def script(base, fx_name, page_rel):
    board_url = f"/{fx_name}/board/index.html"
    page_url = f"/{fx_name}/board/index.html"        # browser location for workbench routes
    q = f"path={page_url}&file={page_rel}"
    out = {}
    g = lambda k, p: out.__setitem__("GET " + k, call(base, p))
    h = lambda k, p: out.__setitem__("HEAD " + k, call(base, p, method="HEAD"))
    post = lambda k, p, payload: out.__setitem__("POST " + k, call(base, p, payload))

    g("home", "/")
    g("boards", "/boards")
    g("board index", board_url)
    g("page html", f"/{fx_name}/board/1/" + Path(page_rel).stem + ".html")
    g("board.js", f"/{fx_name}/board/_assets/board.js")
    g("board.css", f"/{fx_name}/board/_assets/board.css")
    g("asset xterm.css", "/_board/asset/xterm.css")
    g("asset xterm.min.js", "/_board/asset/xterm.min.js")
    g("asset missing", "/_board/asset/nope.js")
    g("health", "/_board/health")
    g("shell", "/_shell")
    g("source md", f"/{fx_name}/{page_rel}")
    for route in ("folderstat", "outline", "value", "evidence", "delivery", "runs", "pageruns",
                  "paper", "design", "design-board", "design-bundle", "insight-board", "insight",
                  "labeling-board", "labeling"):
        g(route, f"/_board/{route}?{q}")
    g("outline no file", f"/_board/outline?path={page_url}")
    g("outline derived file", f"/_board/outline?path=/{fx_name}/{page_rel}")
    # `/w/` · the short workbench address (302 → the long route; urllib follows)
    slug = fx_name.split("-", 1)[1].rsplit("-", 1)[0] if fx_name.count("-") >= 2 else fx_name
    stem = Path(page_rel).stem.split("-")[0]
    g("w board", f"/w/{slug}")
    g("w page", f"/w/{slug}/{stem}")
    g("w page runs", f"/w/{slug}/{stem}/runs")
    g("w page folder", f"/w/{slug}/{stem}/folder")
    g("w page bad tab", f"/w/{slug}/{stem}/studio")
    g("w page labeling", f"/w/{slug}/{stem}/labeling")
    g("w missing", "/w/nosuchboard")
    g("pagexview", "/_board/pagexview")
    for route in ("folderstat", "outline", "value", "evidence", "delivery", "runs", "paper",
                  "design", "insight-board", "labeling"):
        h(route, f"/_board/{route}?{q}")
    h("board index", board_url)
    post("terms", "/_board/terms", {})
    post("activity stats", "/_board/activity", {"path": page_url, "op": "stats"})
    for route in ("folderstat", "outline", "value", "evidence", "delivery", "runs"):
        post(route, f"/_board/{route}", {"path": page_url, "file": page_rel})
    post("design", "/_board/design", {"path": page_url, "file": page_rel})
    post("insight-board", "/_board/insight-board", {"path": page_url})
    post("labeling-board", "/_board/labeling-board", {"path": page_url})
    post("design-board", "/_board/design-board", {"path": page_url})
    post("display", "/_board/display", {"path": page_url, "file": page_rel})
    post("probe", "/_board/probe", {"path": page_url, "file": page_rel})
    post("retired comment", "/_board/comment", {"path": page_url, "file": page_rel, "text": "x"})
    post("bad route", "/_board/nosuchthing", {"path": page_url})
    post("bad file", "/_board/outline", {"path": page_url, "file": "../../etc/passwd"})
    post("structure addgroup", "/_board/structure",
         {"path": page_url, "op": "add_group", "title": "Gate probe group"})
    g("board index after", board_url)
    return out


def fixture_state(root):
    st = {}
    for p in sorted(root.rglob("*")):
        if p.is_file() and p.suffix in (".md", ".html", ".css", ".js") and "__pycache__" not in p.parts:
            txt = norm(p.read_text(encoding="utf-8", errors="replace"))
            st[str(p.relative_to(root))] = hashlib.sha256(txt.encode()).hexdigest()
    return st


def run(serve, fixture, page_rel, save, diff_against, workdir):
    fixture = Path(fixture).resolve()
    work = Path(workdir).resolve()
    frozen = work / "frozen" / fixture.name
    if not frozen.exists():
        shutil.copytree(fixture, frozen,
                        ignore=shutil.ignore_patterns("_archive", "fig", "*.excalidraw", "__pycache__"))
    live = work / "live"
    if live.exists():
        shutil.rmtree(live)
    (live / "b").mkdir(parents=True)
    fx = live / "b" / fixture.name
    shutil.copytree(frozen, fx)
    port = free_port()
    proc = subprocess.Popen(
        [sys.executable, str(Path(serve).resolve()), "--root", str(live / "b"),
         "--port", str(port), "--host", "127.0.0.1"],
        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    base = f"http://127.0.0.1:{port}"
    try:
        for _ in range(120):
            try:
                urllib.request.urlopen(base + "/_board/health", timeout=2).read()
                break
            except Exception:
                if proc.poll() is not None:
                    print("server died:\n" + proc.stderr.read().decode()[:4000])
                    return 2
                time.sleep(0.25)
        res = {"responses": script(base, fixture.name, page_rel)}
        time.sleep(0.5)
        res["files"] = fixture_state(fx)
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()
    Path(save).write_text(json.dumps(res, indent=1, sort_keys=True))
    print(f"saved {save}: {len(res['responses'])} responses, {len(res['files'])} files")
    for k, v in res["responses"].items():
        flag = "  " if v.get("code", 0) in (200, 400, 403, 404, 405) else "!!"
        print(f"{flag} {v.get('code'):>4}  {k}")
    if diff_against:
        old = json.loads(Path(diff_against).read_text())
        bad = 0
        for k in sorted(set(old["responses"]) | set(res["responses"])):
            a, b = old["responses"].get(k), res["responses"].get(k)
            if a != b:
                bad += 1
                print(f"\nDIFF response [{k}]\n  before: {json.dumps(a)[:500]}\n  after:  {json.dumps(b)[:500]}")
        for k in sorted(set(old["files"]) | set(res["files"])):
            if old["files"].get(k) != res["files"].get(k):
                bad += 1
                print(f"DIFF file [{k}]")
        print(("\n❌ %d difference(s)" % bad) if bad else "\n✅ gate green: responses and files identical")
        return 1 if bad else 0
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--serve", default=str(Path(__file__).resolve().parents[1] / "serve.py"),
                    help="path to the serve.py under test (default: the host's own)")
    ap.add_argument("--fixture", required=True, help="a Board folder to copy and drive")
    ap.add_argument("--file", required=True, help="one Page Face relative to the Board root")
    ap.add_argument("--save", required=True)
    ap.add_argument("--diff", dest="diff_against")
    ap.add_argument("--workdir", default="/tmp/haipipe-gate")
    a = ap.parse_args()
    sys.exit(run(a.serve, a.fixture, a.file, a.save, a.diff_against, a.workdir))
