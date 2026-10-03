"""Read-only Excalidraw transport shared by Board and standalone Page hosts.

Scene writers remain in xcal.py. This module imports no Board grammar.
"""

import os
import re
from pathlib import Path


class ExcalidrawProxyMixin:
    def proxy_excalidraw(self, head_only=False):
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
            # The boot script lives beside this module in the studio workbench's
            # own assets/ (servers/workbench-studio/assets/xcal-boot.js).
            js = (Path(__file__).resolve().parent / "assets" / "xcal-boot.js").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "application/javascript; charset=utf-8")
            self.send_header("Content-Length", str(len(js)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            if not head_only:
                self.wfile.write(js)
            return
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
            if not head_only:
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
        if not head_only:
            self.wfile.write(body)
