"""Render one explicitly attached source; both Page and Board call this."""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
import re
from urllib.parse import quote, unquote, urlsplit

from . import body as grammar
from .common import esc


class _SafeMarkup(HTMLParser):
    """Constrain links after Markdown interpretation, including entity URLs."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
    def handle_starttag(self, tag, attrs):
        safe = []
        for key, value in attrs:
            if key.startswith("on") or key in {"srcdoc"}:
                continue
            if key in {"href", "src", "data"} and value:
                scheme = urlsplit(value.strip()).scheme.lower()
                if scheme and scheme not in {"http", "https", "mailto"}:
                    value = "#blocked-link"
            if tag == "iframe" and key == "sandbox":
                continue
            safe.append(key if value is None else f'{key}="{escape(value, quote=True)}"')
        if tag == "iframe":
            safe.append('sandbox="allow-scripts"')
        self.parts.append('<' + tag + (' ' + ' '.join(safe) if safe else '') + '>')
    def handle_endtag(self, tag):
        self.parts.append(f'</{tag}>')
    def handle_data(self, data):
        self.parts.append(escape(data, quote=False))


def render_source_content(page):
    folder = (Path(grammar.BASE or ".") / page["file"]).resolve().parent
    relative = page.get("source_content", "")
    from .page_workspace import render_confined
    try:
        source = render_confined(folder, relative)
    except ValueError:
        return '<p class="source-error">Attached source is missing or outside this Page Folder.</p>'
    if not source.is_file():
        return '<p class="source-error">Attached source is missing.</p>'
    href = quote(grammar._rel(source), safe="/")
    title = f'<p class="source-caption">Source: <a href="{esc(href)}">{esc(source.name)}</a></p>'
    if source.suffix.lower() in {".html", ".htm"}:
        # Opaque origin: imported scripts cannot call the editor API or access
        # the host document. Assets remain relative to the imported HTML.
        content = (f'<iframe class="source-html" title="{esc(source.name)}" '
                   f'sandbox="allow-scripts" src="{esc(href)}"></iframe>')
    elif source.suffix.lower() in {".md", ".markdown"}:
        old, old_paper, old_links, old_root = grammar.PAGE_DIR, grammar.PAPER, grammar.LINKS, grammar.RENDER_ROOT
        try:
            grammar.PAGE_DIR = source.parent
            grammar.PAPER, grammar.LINKS = None, {}
            grammar.RENDER_ROOT = folder
            markdown = source.read_text(encoding="utf-8")
            # The common grammar keeps Markdown hrefs verbatim. Convert only
            # authored link destinations from the import's base to host base.
            def rebase(match):
                destination = match[2]
                parsed = urlsplit(destination)
                if parsed.scheme:
                    url = destination if parsed.scheme.lower() in {"http", "https", "mailto"} else "#blocked-link"
                elif parsed.netloc or not parsed.path:
                    url = destination
                else:
                    asset = (source.parent / unquote(parsed.path)).resolve()
                    url = quote(grammar._rel(asset), safe="/") if asset.is_relative_to(folder) else "#blocked-link"
                    if parsed.query:
                        url += "?" + parsed.query
                    if parsed.fragment:
                        url += "#" + parsed.fragment
                return match[1] + url + match[3]
            markdown = re.sub(r'(!?\[[^\]]*\]\()([^\s)]+)(\))', rebase, markdown)
            # A supplied document is not executable Page grammar. In particular,
            # ![[...]] must not invoke the repository-walking embed resolver.
            from .page_stage import render_doc
            sanitizer = _SafeMarkup()
            sanitizer.feed(render_doc(markdown))
            content = ''.join(sanitizer.parts)
        finally:
            grammar.PAGE_DIR = old
            grammar.PAPER, grammar.LINKS = old_paper, old_links
            grammar.RENDER_ROOT = old_root
    else:
        try:
            content = '<pre class="source-code"><code>' + esc(source.read_text(encoding="utf-8")) + '</code></pre>'
        except (UnicodeError, OSError):
            content = f'<p><a href="{esc(href)}" download>Download {esc(source.name)}</a> (binary source)</p>'
    return '<section class="attached-source">' + title + content + '</section>'
