#!/usr/bin/env python3
"""QC8 gate: prove a serve.py refactor changed no RESPONSE and no file on disk.

QC3's gate compared the generated html because build.py's whole output IS a file.
The live layer's output is HTTP, so this one drives a real server against a
THROWAWAY copy of a board and records two things per run:

  · every response (status + normalized body) for a fixed script of requests
  · the bytes of every .md and generated board/ page in the fixture afterwards

Run it before the refactor (`--save before.json`), then after (`--save after.json
--diff before.json`). A clean diff means the move was mechanical.

Normalization exists because some fields are legitimately time- or uuid-shaped;
each rule is narrow and named, so a real change cannot hide behind one.
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

HERE = Path(__file__).resolve().parent.parent  # the engine dir (this file lives in cli/)


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def norm(text):
    """Blank out what is allowed to differ between two runs, and nothing else."""
    rules = [
        (r'"session":\s*"[0-9a-f-]{36}"', '"session":"<uuid>"'),
        (r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b', '<uuid>'),
        (r'\b\d{6}-\d{6}\b', '<stamp>'),          # image filenames: 260731-140233
        (r'"(mtime|size|ts|started_at|ended_at|seconds)":\s*[0-9.]+', r'"\1":<num>'),
        (r'\b\d{2}:\d{2}(:\d{2})?\b', '<time>'),
        (r'/_term/[0-9a-f]{12}/', '/_term/<key>/'),
        (r'"key":\s*"[0-9a-f]{12}"', '"key":"<key>"'),
    ]
    for pat, rep in rules:
        text = re.sub(pat, rep, text)
    return text


def call(base, path, payload=None):
    url = base + path
    try:
        if payload is None:
            r = urllib.request.urlopen(url, timeout=20)
        else:
            r = urllib.request.urlopen(
                urllib.request.Request(
                    url, data=json.dumps(payload).encode(),
                    headers={"Content-Type": "application/json"}), timeout=20)
        body, code = r.read(), r.status
    except urllib.error.HTTPError as e:
        body, code = e.read(), e.code
    except Exception as e:                       # connection refused, timeout
        return {"code": -1, "err": type(e).__name__ + ": " + str(e)[:120]}
    txt = body.decode("utf-8", "replace")
    # Generated pages are large and regenerated; hash them rather than store them.
    if path.endswith(".html"):
        return {"code": code, "len": len(body),
                "sha": hashlib.sha256(norm(txt).encode()).hexdigest()}
    return {"code": code, "body": norm(txt)[:4000]}


def script(base, page, board_url):
    """One fixed sequence, ordered so writes land on known anchors."""
    out = {}
    S = "The three folders are named and the movements are drawn, but nothing has been confirmed by JL and no checker enforces either forbidden direction."

    out["GET board index"] = call(base, board_url)
    out["GET asset xterm.css"] = call(base, "/_board/asset/xterm.css")
    out["GET asset missing"] = call(base, "/_board/asset/nope.js")
    out["POST terms"] = call(base, "/_board/terms", {})
    out["POST sessions"] = call(base, "/_board/sessions", {"path": board_url, "file": page})
    out["POST activity"] = call(base, "/_board/activity",
                                {"path": board_url, "op": "stats"})
    out["POST comment"] = call(base, "/_board/comment",
                               {"path": board_url, "file": page, "who": "GATE",
                                "sentence": S, "text": "gate probe", "when": "260731"})
    out["POST discuss"] = call(base, "/_board/discuss",
                               {"path": board_url, "file": page, "who": "GATE",
                                "text": "gate discussion probe"})
    out["POST sentence"] = call(base, "/_board/sentence",
                                {"path": board_url, "file": page, "sentence": S,
                                 "lane": "Note", "text": "gate lane probe"})
    out["POST edit-sentence"] = call(base, "/_board/edit-sentence",
                                     {"path": board_url, "file": page, "sentence": S,
                                      "replacement": S + " Gate edit.", "who": "GATE"})
    out["POST image bad"] = call(base, "/_board/image",
                                 {"path": board_url, "file": page,
                                  "name": "x", "data": "not-a-data-url"})
    out["POST image ok"] = call(base, "/_board/image",
                                {"path": board_url, "file": page, "name": "gate",
                                 "data": "data:image/png;base64,"
                                         "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ"
                                         "AAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="})
    out["POST structure addq"] = call(base, "/_board/structure",
                                      {"path": board_url, "op": "add_question",
                                       "group": "QA", "title": "Gate probe page"})
    out["POST structure addgroup"] = call(base, "/_board/structure",
                                          {"path": board_url, "op": "add_group",
                                           "title": "Gate probe group"})
    out["POST resolve"] = call(base, "/_board/resolve",
                               {"path": board_url, "file": page,
                                "sentence": S + " Gate edit.", "who": "GATE"})
    out["POST bad route"] = call(base, "/_board/nosuchthing", {"path": board_url})
    out["POST bad file"] = call(base, "/_board/comment",
                                {"path": board_url, "file": "../../etc/passwd",
                                 "sentence": "x", "text": "y"})
    out["GET board index after"] = call(base, board_url)
    return out


def fixture_state(root):
    """Every written file, so a write that lands in the wrong place is caught.

    Hashed through the same norm() as the responses: a generated page's Log line
    carries `260731 1354`, so two runs minutes apart differ for a reason that has
    nothing to do with the code. Normalizing before hashing keeps the clock out
    without letting a real content change hide.
    """
    st = {}
    for pat in ("*.md", "*.html"):
        for p in sorted(root.rglob(pat)):
            txt = norm(p.read_text(encoding="utf-8", errors="replace"))
            st[str(p.relative_to(root))] = hashlib.sha256(txt.encode()).hexdigest()
    return st


def run(save, diff_against):
    # FREEZE the fixture: the source board keeps being edited between runs, and
    # a gate whose input moves cannot prove anything about the code.
    frozen = Path("/tmp/qc8-fixture")
    if not frozen.exists():
        src = HERE.parent.parent / "diagrams" / "01-boardform-260722"
        shutil.copytree(src, frozen,
                        ignore=shutil.ignore_patterns("_archive", "fig", "*.excalidraw"))
    work = Path("/tmp/qc8-gate")
    if work.exists():
        shutil.rmtree(work)
    (work / "b").mkdir(parents=True)
    fx = work / "b" / "01-boardform-260722"
    shutil.copytree(frozen, fx)
    port = free_port()
    proc = subprocess.Popen(
        [sys.executable, str(HERE / "cli" / "serve.py"), "--root", str(work / "b"),
         "--port", str(port), "--host", "127.0.0.1"],
        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    base = f"http://127.0.0.1:{port}"
    board_url = "/01-boardform-260722/board/index.html"
    try:
        for _ in range(80):                      # wait for listen
            try:
                urllib.request.urlopen(base + board_url, timeout=2).read()
                break
            except Exception:
                if proc.poll() is not None:
                    print("server died:\n" + proc.stderr.read().decode()[:3000])
                    return 2
                time.sleep(0.25)
        res = {"responses": script(base, "QA-design/QA0-three-folders.md", board_url)}
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
        flag = "  " if v.get("code", 0) in (200, 400, 403, 404) else "!!"
        print(f"{flag} {v.get('code')}  {k}")

    if diff_against:
        old = json.loads(Path(diff_against).read_text())
        bad = 0
        for k in sorted(set(old["responses"]) | set(res["responses"])):
            a, b = old["responses"].get(k), res["responses"].get(k)
            if a != b:
                bad += 1
                print(f"\nDIFF response [{k}]\n  before: {json.dumps(a)[:600]}\n  after:  {json.dumps(b)[:600]}")
        for k in sorted(set(old["files"]) | set(res["files"])):
            if old["files"].get(k) != res["files"].get(k):
                bad += 1
                print(f"DIFF file [{k}]")
        print(("\n❌ %d difference(s)" % bad) if bad else "\n✅ gate green: responses and files identical")
        return 1 if bad else 0
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--save", required=True)
    ap.add_argument("--diff", dest="diff_against")
    a = ap.parse_args()
    sys.exit(run(a.save, a.diff_against))
