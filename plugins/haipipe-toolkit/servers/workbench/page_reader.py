"""One Page, as every workbench shows it: the Page engine's own reader.

A Page `.md` is read through `render_page` (haipipe-page `src/page_workspace.py`), the same
renderer that writes the web delivery, so what a workbench pop-out shows is what is delivered
(JL 261004: the workbench is the one reader; the Board's static site is retired). Relative
links are re-based on the Page folder so the document works from any route, and the Content
starts open.
"""
import html
import re
from pathlib import Path
from urllib.parse import quote, urlencode, urljoin, urlsplit

ROUTE = "/_board/page"


def page_url(page, root):
    """`/_board/page?path=<page .md or folder>`: the live reader for one Page; '' outside root."""
    try:
        rel = Path(page).resolve().relative_to(Path(root).resolve()).as_posix()
    except ValueError:
        return ""
    return ROUTE + "?path=" + quote("/" + rel, safe="/")


def page_document(page, root, controls=""):
    """The reader document for one Page (its `.md` or its folder); `controls` replace the
    toolbar's lone Page link (a back link, a workbench link)."""
    from src.page_workspace import load_page, render_page
    page = Path(page)
    folder = page.parent if page.suffix == ".md" else page
    document = render_page(load_page(page))
    base = "/" + quote(folder.resolve().relative_to(Path(root).resolve()).as_posix(), safe="/") + "/"
    markup, separator, scripts = document.partition("<script")

    def rebase(match):
        value = html.unescape(match.group(2))
        if not value or value.startswith(("#", "/")) or urlsplit(value).scheme:
            return match.group(0)
        return match.group(1) + '="' + html.escape(urljoin(base, value), quote=True) + '"'
    markup = re.sub(r'\b(href|src|poster)="([^"]*)"', rebase, markup)
    document = markup + separator + scripts
    document = document.replace('<details class="sect content">', '<details class="sect content" open>')
    if controls:
        document = document.replace('<nav><a href="#reading">Page</a>', "<nav>" + controls, 1)
    return document


class PageReaderMixin:
    """GET /_board/page?path=<page .md or Page folder>: one Page, live, in the reader."""

    def page_reader_view(self, head_only=False):
        from urllib.parse import parse_qs, urlparse
        root = Path(self.root).resolve()
        raw = (parse_qs(urlparse(self.path).query).get("path") or [""])[0].lstrip("/")
        target = (root / raw).resolve()
        status, body = 200, ""
        if not raw or not target.is_relative_to(root) or any(p.startswith(".") for p in target.relative_to(root).parts):
            status, body = 404, "<h1>No such Page</h1>"
        else:
            try:
                body = page_document(target, root)
            except Exception as exc:  # noqa: BLE001  (an unreadable Page says why, never 500s)
                status, body = 404, f"<h1>Not a Page</h1><p>{html.escape(str(exc))}</p>"
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        if not head_only:
            self.wfile.write(data)
