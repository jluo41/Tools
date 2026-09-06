"""Read-only bridge for opening historical PageX links.

Current Page work uses Context source addresses and Evidence Item Run bindings.
The server keeps this one GET view so an already-rendered historical card does
not become a dead link. No PageX store or symlink is created or changed here.
"""

import re
from pathlib import Path
from urllib.parse import parse_qs, quote as _q, urlparse

from live.export import _esc


_ROW = re.compile(
    r"^- (?P<path>\S+)(?P<removed> · removed)?"
    r"(?: · note: (?P<note>.*))?\s*$"
)


class LegacyPagexViewMixin:
    """Serve the navigation shell for historical PageX card links only."""

    @staticmethod
    def _page_home_of(target, root):
        directory, parts = target.parent, [target.name]
        while True:
            if (directory / f"{directory.name}.md").is_file():
                return directory, "/".join(reversed(parts))
            if directory == root or directory.parent == directory:
                return None, target.name
            parts.append(directory.name)
            directory = directory.parent

    def _rendered_url(self, page_md):
        directory = page_md.resolve().parent
        root = Path(self.root).resolve()
        while directory != root and directory.parent != directory:
            if (directory / "board.md").is_file():
                matches = sorted(
                    (directory / "board").glob(f"*/{page_md.stem}.html")
                )
                return self._url_of(matches[0]) if matches else None
            directory = directory.parent
        return None

    def serve_pagexview(self):
        query = parse_qs(urlparse(self.path).query)
        page = (query.get("p") or [""])[0]
        store = (query.get("from") or [""])[0]
        if not page:
            return self.reply(400, {"ok": False, "err": "no page"})

        siblings, current = [], -1
        root = Path(self.root).resolve()
        store_path = root / store if store else None
        if store_path and store_path.is_file():
            for line in store_path.read_text(encoding="utf-8").splitlines():
                match = _ROW.match(line.strip())
                if not match or match.group("removed"):
                    continue
                target = (root / match.group("path")).resolve()
                home, _inner = self._page_home_of(target, root)
                if not home or target.name != f"{home.name}.md":
                    continue
                url = self._rendered_url(target)
                if url and all(url != sibling[1] for sibling in siblings):
                    siblings.append((home.name, url))

        for index, (_name, url) in enumerate(siblings):
            if url.lstrip("/") == page.lstrip("/"):
                current = index
                break

        def door(index, glyph, label):
            if not 0 <= index < len(siblings):
                return f"<span class='off'>{glyph}</span>"
            return (
                "<a href='/_board/pagexview?p=%s&from=%s' title='%s'>%s</a>"
                % (
                    _q(siblings[index][1].lstrip("/")),
                    _q(store),
                    _esc(siblings[index][0]),
                    glyph,
                )
            )

        name = siblings[current][0] if current >= 0 else Path(page).stem
        index_url = (
            "/" + store.rsplit("/", 1)[0] + "/" + Path(store).stem + "-view.html"
            if store
            else "#"
        )
        bar = (
            "<div class=bar>%s<a class=idx href='%s'>☰ historical links</a>%s"
            "<b>%s</b><span class=sp></span>"
            "<a href='/%s' target=_blank>open on its own</a></div>"
            % (
                door(current - 1, "←", "previous"),
                _esc(index_url),
                door(current + 1, "→", "next"),
                _esc(name),
                _q(page),
            )
        )
        html = (
            "<!doctype html><meta charset=utf-8><title>%s</title><style>"
            "html,body{height:100%%;margin:0}"
            ".bar{display:flex;gap:12px;align-items:center;height:34px;"
            "padding:0 12px;border-bottom:1px solid #dedeb8;"
            "font:13px -apple-system,sans-serif;background:#fff}"
            "@media(prefers-color-scheme:dark){.bar{background:#161719;"
            "border-color:#2c2e33;color:#e8e8e6}.bar a{color:#7fb2ea}}"
            ".bar a{color:#1f5aa8;text-decoration:none}"
            ".bar a:hover{text-decoration:underline}"
            ".bar .off{color:#b6b6b0}.bar .sp{flex:1}"
            "iframe{width:100%%;height:calc(100%% - 35px);border:0}"
            "</style>%s<iframe src='/%s'></iframe>"
            % (_esc(name), bar, _q(page))
        )
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)
