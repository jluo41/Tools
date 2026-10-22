"""The normalizer APIs, passed through this host behind its login (JL 261021: "那我这个怎么打开这个 set 呢？... 没有给我链接？").

The haipipe-utils API host (plugins/haipipe-utils/servers/_host/serve.py) has no login of its own and listens on
localhost only; its page notes say to put a gate in front before it listens on a network. This host is that gate:
`/_api/<rest>` goes to `$HAIPIPE_UTILS_ORIGIN/<rest>` (default http://127.0.0.1:8070), so its try page opens at
`/_api/try/food` wherever this host is opened, after this host's own login. Requests and answers pass through as they
are (GET and POST, a JSON body or a photo's multipart body); nothing is rewritten.
"""

import os


class ApiProxyMixin:
    API_PREFIX = "/_api"

    def is_api_request(self):
        path = self.path.split("?", 1)[0]
        return path == self.API_PREFIX or path.startswith(self.API_PREFIX + "/")

    def proxy_api(self):
        import urllib.error
        import urllib.request
        origin = os.environ.get("HAIPIPE_UTILS_ORIGIN", "http://127.0.0.1:8070").rstrip("/")
        path = self.path[len(self.API_PREFIX):] or "/"
        body = None
        if self.command == "POST":
            n = int(self.headers.get("Content-Length") or 0)
            body = self.rfile.read(n) if n else b""
        req = urllib.request.Request(origin + path, data=body, method=self.command)
        if self.headers.get("Content-Type"):
            req.add_header("Content-Type", self.headers["Content-Type"])
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                data, status, ctype = r.read(), r.status, r.headers.get("Content-Type", "")
        except urllib.error.HTTPError as e:
            data, status, ctype = e.read(), e.code, e.headers.get("Content-Type", "text/plain")
        except Exception as e:
            data = (f"The API host is not answering at {origin} ({type(e).__name__}). Start it with:  "
                    ".venv/bin/python Tools/plugins/haipipe-utils/servers/_host/serve.py "
                    "--store _WorkSpace/ExternalStore --only food").encode()
            status, ctype = 502, "text/plain; charset=utf-8"
        self.send_response(status)
        if ctype:
            self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)
