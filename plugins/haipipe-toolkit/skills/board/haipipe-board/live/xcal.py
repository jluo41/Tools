"""QC8 · the canvas round-trip (QB4b, QD5): frames, scenes, embedded files.

Moved out of serve.py on 2026-07-31 under the gate_live.py response-identical gate.
QC3's Law: a refactor moves code, features never ride along.
"""

import base64
import datetime as dt
import difflib
import hashlib
import itertools
import json
import os
import re
import shutil
import signal
import socket
import sqlite3
import struct
import subprocess
import sys
import threading
import time
import urllib.parse
from pathlib import Path
from urllib.parse import unquote

from . import base




class XcalMixin:
    def excalidraw_key(self):
        """The Excalidraw+ key, from the environment or from env.sh at the root.

        env.sh is gitignored and per-machine (QE6), and serve.py is often started
        from a shell that never sourced it, so falling back to reading the file is
        the difference between "works" and "works only if you remembered".
        """
        k = os.environ.get("EXCALIDRAW_API_KEY", "").strip()
        if k:
            return k, "environment"
        env = self.root / "env.sh"
        if env.exists():
            m = re.search(r'^\s*export\s+EXCALIDRAW_API_KEY\s*=\s*["\']?([^"\'\s#]+)',
                          env.read_text(encoding="utf-8", errors="ignore"), re.M)
            if m:
                return m.group(1), "env.sh"
        return "", ""

    def new_excalidraw(self, f, p):
        """✨ Mint an Excalidraw+ scene for this page and write its link into ## Diagram.

        The point is that nobody should have to leave the board, create a drawing
        by hand, and paste a URL back: the page asks for one and gets one.

        The response shape is DISCOVERED rather than assumed. Excalidraw+'s API is
        public beta and its docs list the endpoints without showing the bodies, so
        this asks, then REPORTS what came back, including the raw keys when no link
        is found. A wrong guess that fails loudly beats a wrong guess that writes
        a plausible dead URL into twenty-eight pages.
        """
        import urllib.error
        import urllib.request

        key, src = self.excalidraw_key()
        if not key:
            return None, ("no EXCALIDRAW_API_KEY. Add `export EXCALIDRAW_API_KEY=…` to "
                          "env.sh at the repo root (it is gitignored), or export it in the "
                          "shell that runs serve.py. The key comes from your Excalidraw+ "
                          "workspace settings.")
        base = os.environ.get("EXCALIDRAW_API_BASE", "https://api.excalidraw.com/api/v1")

        def call(method, path, body=None):
            req = urllib.request.Request(
                base + path, method=method,
                data=json.dumps(body).encode() if body is not None else None,
                headers={"Authorization": f"Bearer {key}",
                         "Content-Type": "application/json",
                         "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=20) as r:
                raw = r.read().decode("utf-8", "replace")
            return json.loads(raw) if raw.strip() else {}

        try:
            coll = os.environ.get("EXCALIDRAW_COLLECTION_ID", "").strip()
            if not coll:
                got = call("GET", "/collections")
                items = got if isinstance(got, list) else (got.get("data") or got.get("collections") or [])
                if not items:
                    return None, f"no collections came back from {base}/collections: {str(got)[:200]}"
                coll = str(items[0].get("id") or items[0].get("collectionId") or "")
                if not coll:
                    return None, f"a collection came back with no id: {str(items[0])[:200]}"
            title = f.stem
            scene = call("POST", f"/collections/{coll}/scenes", {"name": title})
        except urllib.error.HTTPError as e:
            return None, f"excalidraw API {e.code} on {e.url}: {e.read()[:200].decode('utf-8','replace')}"
        except Exception as e:
            return None, f"{type(e).__name__} talking to {base}: {e}"

        # Find a link in whatever came back, without inventing one.
        def find_url(o):
            if isinstance(o, str) and o.startswith("http"):
                return o
            if isinstance(o, dict):
                for k2 in ("url", "link", "shareLink", "publicLink", "editLink", "href"):
                    u = find_url(o.get(k2))
                    if u:
                        return u
                for v in o.values():
                    u = find_url(v)
                    if u:
                        return u
            if isinstance(o, list):
                for v in o:
                    u = find_url(v)
                    if u:
                        return u
            return None

        url = find_url(scene)
        if not url:
            keys = ", ".join(sorted(scene)) if isinstance(scene, dict) else type(scene).__name__
            return None, ("the scene was created but no link field was found in the response. "
                          f"Keys: {keys}. Open it in the Excalidraw+ workspace, copy the URL, and "
                          "paste it here; then tell CC which field holds it so this can stop guessing.")
        res, err = self.add_diagram(f, {"url": url})
        if err:
            return None, f"created {url} but could not write it: {err}"
        return {"url": url, "key_from": src, **(res or {})}, None

    def add_diagram(self, f, p):
        """➕ Excalidraw in 🖼 Diagram (JL 260726): paste a share URL on the page and it
        lands on its own line inside `## Diagram` — the same line an author types by hand,
        so the md stays the single source and the canvas comes back through build.py.
        One canvas per page: pasting again replaces the old URL instead of stacking a
        second iframe onto the section."""
        url = (p.get("url") or "").strip()
        drop = bool(p.get("remove"))
        # The hosted app, OR this board's own Excalidraw. A self-hosted URL is not
        # guessable, so board.md declares the host once (`excalidraw:`) and this
        # accepts anything under it; without that the ➕ control could not take the
        # very URL the board tells every page to use.
        host = ""
        bmd = f.parent / "board.md"
        if bmd.exists():
            m = re.search(r"^excalidraw:\s*(\S+)", bmd.read_text(encoding="utf-8"), re.M)
            if m:
                host = m.group(1).rstrip("/")
        okay = re.fullmatch(r"https?://(?:app\.)?excalidraw\.com/\S+", url) or (
            host and url.startswith(host + "/"))
        if not drop and not okay:
            hint = f" or this board's own {host}/…" if host else ""
            return None, f"not an excalidraw link (https://app.excalidraw.com/s/…{hint})"
        lines = f.read_text(encoding="utf-8").split("\n")
        def is_xcal(s):
            """A line that is ALREADY an excalidraw embed, hosted or ours.

            It must know about the board's own host too, or a second paste on a
            self-hosted page appends a second iframe instead of replacing the
            first, which is the stacking this endpoint exists to prevent.
            """
            s = s.strip()
            if re.fullmatch(r"https?://(?:app\.)?excalidraw\.com/\S+", s):
                return True
            return bool(host) and s.startswith(host + "/")

        # ## Diagram 的范围。找的时候要跳 ``` 围栏：QA4 正文里就摆着 md 段落的示例，
        # 不跳的话会写进示例里（评论层 260723 真踩过这个坑）。
        fence, start, end = False, None, None
        for i, ln in enumerate(lines):
            if ln.lstrip().startswith("```"):
                fence = not fence
                continue
            if fence:
                continue
            if start is None:
                if re.match(r"^## (?:Diagram|图)\s*$", ln):
                    start = i
                continue
            if re.match(r"^## ", ln):
                end = i
                break

        if start is None and drop:
            return None, "this page has no ## Diagram section"
        if start is None:
            # 没有 Diagram 这一节就现开一节，位置按固定层次：Diagram 在 Content 之前。
            fence, anchor = False, None
            for i, ln in enumerate(lines):
                if ln.lstrip().startswith("```"):
                    fence = not fence
                    continue
                if fence:
                    continue
                if re.match(r"^## (?:Content|Items to Finish|Done when|完成条件|清单)\b", ln):
                    anchor = i
                    break
            block = ["## Diagram", url, ""]
            if anchor is None:
                lines += [""] + block
            else:
                lines[anchor:anchor] = block
            f.write_text("\n".join(lines), encoding="utf-8")
            return {"warn": "created ## Diagram holding only a canvas; the ascii figure is "
                            "the part that survives being copied, so add one"}, None

        end = end if end is not None else len(lines)
        if drop:
            # 🗑 QD7 (JL 260726): attaching used to be reversible only by hand, so
            # a wrong paste sent the reader to the editor the button exists to
            # avoid. Removal takes out the URL LINE and one blank line above it,
            # and touches nothing else: the ascii figure, the heading, and the
            # section all stay, because deleting a section is a different act
            # with a different blast radius.
            gone = [j for j in range(start + 1, end) if is_xcal(lines[j])]
            if not gone:
                return None, "this Diagram has no excalidraw to remove"
            for j in reversed(gone):
                if j - 1 > start and not lines[j - 1].strip():
                    del lines[j - 1:j + 1]
                else:
                    del lines[j]
            f.write_text("\n".join(lines), encoding="utf-8")
            return {"removed": len(gone)}, None
        for j in range(start + 1, end):
            if is_xcal(lines[j]):
                lines[j] = url
                f.write_text("\n".join(lines), encoding="utf-8")
                return {"replaced": True}, None
        k = end
        while k - 1 > start and not lines[k - 1].strip():
            k -= 1
        lines[k:k] = ["", url]
        f.write_text("\n".join(lines), encoding="utf-8")
        has_ascii = any(lines[j].lstrip().startswith("```") for j in range(start + 1, end))
        return ({} if has_ascii else
                {"warn": "this Diagram has no ascii figure; the canvas is the half that "
                         "disappears when it cannot load"}), None

    def proxy_excalidraw(self):
        import urllib.error
        import urllib.request
        origin = os.environ.get("EXCALIDRAW_ORIGIN", "http://127.0.0.1:5610")
        path = self.path
        if path.startswith("/_excalidraw"):
            path = path[len("/_excalidraw"):] or "/"
        # The app's own storage is the whole reason a drawing never reached the
        # repo, so we hand it ours. Served from under the proxy prefix so it is
        # same-origin with the app it is patching.
        if path.split("?")[0] == "/_haipipe-xcal.js":
            # base.HERE 是技能根（live/ 的上一层）：__file__ 搬进 live/ 之后，
            # parent/"assets" 会指到不存在的 live/assets/（260731 拆分回归，
            # 每次从浏览器开 excalidraw 场景都 500）。
            js = (base.HERE / "assets" / "xcal-boot.js").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "application/javascript; charset=utf-8")
            self.send_header("Content-Length", str(len(js)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            return self.wfile.write(js)
        try:
            with urllib.request.urlopen(origin + path, timeout=20) as r:
                body, status, ctype = r.read(), r.status, r.headers.get("Content-Type", "")
        except urllib.error.HTTPError as e:
            body, status, ctype = e.read(), e.code, e.headers.get("Content-Type", "text/plain")
        except Exception as e:
            msg = (f"Excalidraw is not answering at {origin}: {type(e).__name__}. "
                   f"Start it with:  docker run --rm -d -p 5610:80 excalidraw/excalidraw"
                   ).encode()
            self.send_response(502)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(msg)))
            self.end_headers()
            self.wfile.write(msg)
            return
        # Two rewrites, and the second is what makes images work. A classic
        # script in <head> runs before the app's deferred module, which is
        # enough to replace localStorage; it is NOT enough for IndexedDB, where
        # the images live, because that API is async and the app would read the
        # store before our seed landed. So the app's own module is HELD: it is
        # turned into a variable, and the boot script appends it once seeding
        # has actually finished.
        if "text/html" in ctype:
            tag = b'<script src="/_excalidraw/_haipipe-xcal.js"></script>'
            # The boot script must come AFTER the variable it reads. Injecting it
            # at <head> put it first, so it ran with __haipipeApp still undefined,
            # returned quietly, and the app never started at all: a blank page
            # with a correct badge on it (found 260726 in headless Chrome).
            body, n = re.subn(
                rb'<script type="module"([^>]*?)src="([^"]+)"([^>]*)></script>',
                rb'<script>window.__haipipeApp="\2"</script>' + tag, body, count=1)
            if not n:                       # no module to hold; seed anyway
                body = (body.replace(b"<head>", b"<head>" + tag, 1)
                        if b"<head>" in body else tag + body)
        self.send_response(status)
        if ctype:
            self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def hydrate_files(self, scene, els, base):
        """scene pointers -> the dataURLs the editor expects, for these elements."""
        want = {e.get("fileId") for e in els
                if e.get("type") == "image" and e.get("fileId")}
        out = {}
        for fid in sorted(want):
            rec = (scene.get("files") or {}).get(fid)
            if not isinstance(rec, dict):
                continue
            if rec.get("dataURL"):          # an older scene with the bytes inline
                out[fid] = rec
                continue
            p = (base / rec.get("path", "")).resolve()
            try:
                p.relative_to(base.resolve())
            except ValueError:
                continue
            if not p.exists():
                continue
            mime = rec.get("mimeType") or "image/png"
            b64 = base64.b64encode(p.read_bytes()).decode()
            out[fid] = {"id": fid, "mimeType": mime, "created": rec.get("created", 0),
                        "dataURL": f"data:{mime};base64,{b64}"}
        return out

    def stash_files(self, scene, files, base):
        """the editor's dataURLs -> files on disk + pointers in the scene."""
        keep = dict(scene.get("files") or {})
        wrote = []
        for fid, rec in (files or {}).items():
            if not isinstance(rec, dict):
                continue
            m = re.match(r"^data:([^;,]+);base64,(.+)$", rec.get("dataURL") or "", re.S)
            if not m:
                continue
            mime, b64 = m.group(1), m.group(2)
            name = re.sub(r"[^A-Za-z0-9_.-]", "_", fid) + self.XMIME.get(mime, ".bin")
            base.mkdir(parents=True, exist_ok=True)
            try:
                (base / name).write_bytes(base64.b64decode(b64))
            except Exception:
                continue
            keep[fid] = {"id": fid, "mimeType": mime, "path": f"{base.name}/{name}",
                         "created": rec.get("created", 0)}
            wrote.append(name)
        scene["files"] = keep
        return wrote

    def save_excalidraw(self, d):
        """POST /_board/excalidraw-save {board, frame, elements} -> the scene file.

        The half `#url=` never had. With `frame`, this MERGES: that frame's slice
        is replaced and every other page's frame is left exactly as it was, which
        is what lets one file be edited from any page without the pages fighting.
        Without `frame`, the whole scene is replaced, because that edit was made
        with the whole scene on screen.
        """
        rel = (d.get("board") or "").lstrip("/")
        frame = (d.get("frame") or "").strip()
        els = d.get("elements")
        if not isinstance(els, list):
            return {"ok": False, "err": "elements must be a list"}
        f = (self.root / rel).resolve()
        try:
            f.relative_to(self.root.resolve())
        except ValueError:
            return {"ok": False, "err": "outside --root"}
        if f.suffix != ".excalidraw" or not f.exists():
            return {"ok": False, "err": f"no scene at {rel!r}"}
        try:
            scene = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            return {"ok": False, "err": f"{f.name} is not a scene: {e}"}
        old = scene.get("elements", [])
        els = [e for e in els if isinstance(e, dict) and not e.get("isDeleted")]
        if not frame:
            scene["elements"] = els
        else:
            fid = next((e.get("id") for e in old
                        if e.get("type") == "frame" and e.get("name") == frame), None)
            if fid is None:
                names = [e.get("name") for e in old if e.get("type") == "frame"]
                return {"ok": False, "err": f"no frame named {frame!r}. Frames: {names}"}
            rest = [e for e in old if e.get("id") != fid and e.get("frameId") != fid]
            slice_ = []
            for e in els:
                if e.get("type") == "frame":
                    # keep the frame's identity whatever the editor renamed it to:
                    # the name IS the page's link, so losing it breaks that page
                    e["id"], e["name"] = fid, frame
                else:
                    e["frameId"] = fid
                slice_.append(e)
            if not any(e.get("id") == fid for e in slice_):
                orig = next(e for e in old if e.get("id") == fid)
                slice_.insert(0, orig)      # the frame was deleted; put it back
            scene["elements"] = rest + slice_
        imgs = self.stash_files(scene, d.get("files"), f.parent / "assets")
        tmp = f.with_name(f.name + ".tmp")
        tmp.write_text(json.dumps(scene, indent=1), encoding="utf-8")
        tmp.replace(f)
        return {"ok": True, "wrote": len(els), "total": len(scene["elements"]),
                "images": imgs, "frame": frame or "(whole board)"}

    def serve_frame(self):
        """`…/board.excalidraw?frame=QA4a` -> the SAME scene, that frame only.

        ONE excalidraw per board, one FRAME per page (JL 260726). The frame is not
        a separate file and must never become one: the whole point of a single
        scene is that it can say how the pages relate, which is the thing a
        per-page drawing can never express.

        A per-frame URL is needed anyway, because a page's Diagram should open at
        ITS frame rather than at the whole board. The hosted `?element=<id>` anchor
        is an Excalidraw+ feature; the open-source app reads only `id`,
        `resourcekey`, `start` and `t` from the query string, so the anchor has to
        come from this side. It is a projection, computed per request:

            …/fig/board.excalidraw                 the whole board, for drawing
            …/fig/board.excalidraw?frame=QA4a      that frame, for the page

        Both are the same file on disk. Editing happens on the first.
        """
        path, _, qs = self.path.partition("?")
        want = urllib.parse.parse_qs(qs).get("frame", [""])[0]
        # `?frame=` narrows to one page; no frame means the whole board, and
        # BOTH need their images turned back into dataURLs on the way out.
        f = (self.root / path.lstrip("/")).resolve()
        try:
            f.relative_to(self.root.resolve())
        except ValueError:
            return self.reply(403, {"ok": False, "err": "outside --root"})
        if not f.exists():
            return self.reply(404, {"ok": False, "err": f"no {path}"})
        try:
            scene = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            return self.reply(400, {"ok": False, "err": f"{f.name} is not a scene: {e}"})

        els = scene.get("elements", [])
        if not want:
            scene["files"] = self.hydrate_files(scene, els, f.parent)
            return self.reply_scene(scene)
        frame = next((e for e in els
                      if e.get("type") == "frame" and e.get("name") == want), None)
        if frame is None:
            names = [e.get("name") for e in els if e.get("type") == "frame"]
            return self.reply(404, {"ok": False,
                                    "err": f"no frame named {want!r}. Frames: {names}"})
        fid = frame.get("id")
        keep = [e for e in els if e.get("frameId") == fid or e.get("id") == fid]
        scene["elements"] = keep
        scene["files"] = self.hydrate_files(scene, keep, f.parent)
        return self.reply_scene(scene)

    def reply_scene(self, scene):
        body = json.dumps(scene).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)
