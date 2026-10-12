"""One Page, as every workbench shows it: the Page engine's own reader.

A Page `.md` is read through `render_page` (haipipe-draft `src/page_workspace.py`), the same
renderer that writes the web delivery, so what a workbench pop-out shows is what is delivered
(JL 261004: the workbench is the one reader; the Board's static site is retired). Relative
links are re-based on the Page folder so the document works from any route, and the Content
starts open.

Any other `.md` (a meeting's notes in `related/`, `related/related.md`, a studio face) is no Page and
reads as plain Markdown, escaped, its links re-based the same way (`markdown_document`; JL 261011, a
related meeting opened on "Not a Page"). Obsidian's own marks read too: a `> [!quote]-` callout
folds, a `![[file]]` embed names its file.
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


_TABLE_RULE = re.compile(r"\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)*\|?\s*")
_LIST_ITEM = re.compile(r"(\s*)([-*+]|\d+[.)])\s+(.*)")
_CALLOUT = re.compile(r"\[!(\w+)\]([+-]?)\s*(.*)")
_HR = re.compile(r"\s*(?:(?:\*\s*){3,}|(?:-\s*){3,}|(?:_\s*){3,})")
MARKDOWN_CSS = (
    "body{font:15px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#1e1e1e;background:#fff;"
    "max-width:880px;margin:0 auto;padding:18px 28px 48px}"
    "h1,h2,h3,h4{line-height:1.3;margin:1.3em 0 .45em}h1{font-size:1.6em}h2{font-size:1.3em;border-bottom:1px solid #ddd;"
    "padding-bottom:.2em}h3{font-size:1.1em}code{font:.9em ui-monospace,Menlo,monospace;background:#f3f3f3;"
    "padding:0 .25em;border-radius:3px}pre{background:#f6f6f6;padding:10px 12px;overflow:auto;line-height:1.35}"
    "pre code{background:none;padding:0}table{border-collapse:collapse;margin:.6em 0}td,th{border:1px solid #ccc;"
    "padding:4px 8px;vertical-align:top}th{background:#f6f6f6}blockquote{margin:.6em 0;padding:.1em 1em;"
    "border-left:3px solid #ccc;color:#444}.callout{margin:.6em 0;border:1px solid #ccc;border-left:3px solid #888;"
    "padding:.3em .9em;border-radius:4px}.callout>summary,.callout-title{font-weight:600;cursor:pointer}"
    ".front,.md-file{font-size:13px;color:#666}.embed{color:#666}img{max-width:100%}"
    "@media (prefers-color-scheme:dark){body{background:#1d1d1f;color:#e6e6e6}code,pre,th{background:#2a2a2c}"
    "td,th,.callout{border-color:#444}h2{border-color:#444}blockquote{color:#bbb;border-color:#555}"
    ".front,.md-file,.embed{color:#999}a{color:#7ab7ff}}")


def _md_href(value: str, base: str) -> str:
    """A link's target: a web address or a root path as written, a relative one re-based on the file's
    folder; any other scheme (javascript:, data:) is dropped."""
    value = value.strip()
    if re.match(r"(?:https?://|#|/(?!/))", value):
        return value
    if urlsplit(value).scheme or value.startswith("//"):
        return ""
    return urljoin(base, quote(value, safe="/#?=&%"))


def _md_inline(text: str, base: str) -> str:
    """One line's inline marks: `code`, **bold**, *italic*, [links](…), ![pictures](…), Obsidian's
    [[note]] and ![[embed]]; everything else escaped."""
    out = []
    for n, part in enumerate(re.split(r"(`[^`]+`)", text)):
        if n % 2:
            out.append(f"<code>{html.escape(part[1:-1])}</code>")
            continue
        s = html.escape(part, quote=False)
        s = re.sub(r"!\[\[([^\]]+)\]\]", lambda m: f"<span class=embed>⤷ {m.group(1)}</span>", s)
        s = re.sub(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", lambda m: m.group(2) or m.group(1), s)

        def picture(m):
            src = _md_href(html.unescape(m.group(2)), base)
            alt = html.escape(html.unescape(m.group(1)), quote=True)
            return f'<img alt="{alt}" src="{html.escape(src, quote=True)}">' if src else m.group(1)

        def link(m):
            href = _md_href(html.unescape(m.group(2)), base)
            return f'<a href="{html.escape(href, quote=True)}">{m.group(1)}</a>' if href else m.group(1)
        s = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", picture, s)
        s = re.sub(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)\)", link, s)
        s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
        s = re.sub(r"(?<![\w*])\*(?![\s*])(.+?)(?<![\s*])\*(?![\w*])", r"<i>\1</i>", s)
        out.append(s)
    return "".join(out)


def markdown_html(text: str, base: str = "", breaks: bool = False) -> str:
    """Plain Markdown as HTML: front matter, headings (# and underlined), code, tables, lists, quotes,
    Obsidian callouts (`> [!kind]- title` folds), rules and paragraphs. `breaks` keeps each line's own
    break, as Obsidian shows a quote's lines (a transcript is one line per turn)."""
    lines, out, i = text.splitlines(), [], 0
    if lines and lines[0].strip() == "---":
        end = next((k for k in range(1, len(lines)) if lines[k].strip() == "---"), 0)
        if end:
            out.append(f'<pre class=front>{html.escape(chr(10).join(lines[1:end]))}</pre>')
            i = end + 1
    starts_block = lambda k: (lines[k].lstrip().startswith(("```", "~~~", ">", "#")) or _LIST_ITEM.fullmatch(lines[k])
                              or (k + 1 < len(lines) and "|" in lines[k] and _TABLE_RULE.fullmatch(lines[k + 1])))
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        fence = line.lstrip()[:3]
        if fence in ("```", "~~~"):
            body, i = [], i + 1
            while i < len(lines) and not lines[i].lstrip().startswith(fence):
                body.append(lines[i])
                i += 1
            out.append(f"<pre><code>{html.escape(chr(10).join(body))}</code></pre>")
            i += 1
            continue
        heading = re.match(r"(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if heading:
            n = len(heading.group(1))
            out.append(f"<h{n}>{_md_inline(heading.group(2), base)}</h{n}>")
            i += 1
            continue
        if _HR.fullmatch(line):
            out.append("<hr>")
            i += 1
            continue
        if i + 1 < len(lines) and "|" in line and _TABLE_RULE.fullmatch(lines[i + 1]):
            cells = lambda row: [c.strip() for c in row.strip().strip("|").split("|")]
            head = "".join(f"<th>{_md_inline(c, base)}</th>" for c in cells(line))
            rows, i = [], i + 2
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                rows.append("<tr>" + "".join(f"<td>{_md_inline(c, base)}</td>" for c in cells(lines[i])) + "</tr>")
                i += 1
            out.append(f"<table><thead><tr>{head}</tr></thead><tbody>{''.join(rows)}</tbody></table>")
            continue
        if line.lstrip().startswith(">"):
            inner = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                inner.append(re.sub(r"^\s*> ?", "", lines[i]))
                i += 1
            callout = _CALLOUT.match(inner[0].strip())
            if callout:
                kind, fold, title = callout.groups()
                body = markdown_html("\n".join(inner[1:]), base, breaks=True)
                title = _md_inline(title or kind.title(), base)
                out.append(f'<details class="callout {kind.lower()}"{"" if fold == "-" else " open"}>'
                           f"<summary>{title}</summary>{body}</details>")
            else:
                out.append(f"<blockquote>{markdown_html(chr(10).join(inner), base, breaks=True)}</blockquote>")
            continue
        item = _LIST_ITEM.fullmatch(line)
        if item:
            ordered, items = item.group(2)[0].isdigit(), []
            while i < len(lines) and (match := _LIST_ITEM.fullmatch(lines[i])):
                words = re.sub(r"^\[ \]\s*", "☐ ", re.sub(r"^\[[xX]\]\s*", "☑ ", match.group(3)))
                i += 1
                while i < len(lines) and lines[i].startswith("  ") and lines[i].strip() and not _LIST_ITEM.fullmatch(lines[i]):
                    words += " " + lines[i].strip()
                    i += 1
                depth = len(match.group(1).expandtabs(4)) // 2
                indent = f' style="margin-left:{depth * 1.4:g}em"' if depth else ""
                items.append(f"<li{indent}>{_md_inline(words, base)}</li>")
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>{''.join(items)}</{tag}>")
            continue
        if i + 1 < len(lines) and re.fullmatch(r"\s*(=+|-+)\s*", lines[i + 1]) and line.strip():
            n = 1 if lines[i + 1].strip()[0] == "=" else 2          # an underlined heading (ASCII style)
            out.append(f"<h{n}>{_md_inline(line.strip(), base)}</h{n}>")
            i += 2
            continue
        para, i = [line.strip()], i + 1
        while i < len(lines) and lines[i].strip() and not starts_block(i) and not _HR.fullmatch(lines[i]):
            para.append(lines[i].strip())
            i += 1
        out.append("<p>" + ("<br>" if breaks else " ").join(_md_inline(p, base) for p in para) + "</p>")
    return "".join(out)


def markdown_document(path, root, reason=""):
    """Any other `.md`, read as plain Markdown: a line naming the file, then its text (see the module's
    note). `reason` says why it is no Page when that is not simply its missing Opening."""
    path, root = Path(path), Path(root).resolve()
    base = "/" + quote(path.parent.resolve().relative_to(root).as_posix(), safe="/") + "/"
    why = f" · not read as a Page: {html.escape(reason)}" if reason else ""
    return (f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,'
            f'initial-scale=1"><title>{html.escape(path.name)}</title><style>{MARKDOWN_CSS}</style></head><body>'
            f'<p class=md-file>{html.escape(path.name)} · Markdown{why}</p>'
            f'{markdown_html(path.read_text(encoding="utf-8"), base)}</body></html>')


class PageReaderMixin:
    """GET /_board/page?path=<page .md or Page folder>: one Page, live, in the reader; any other .md as
    plain Markdown."""

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
                if target.suffix == ".md" and target.is_file():         # a meeting's notes, related.md: no Page
                    reason = "" if "not a Page Face" in str(exc) else str(exc)
                    body = markdown_document(target, root, reason)
                else:
                    status, body = 404, f"<h1>Not a Page</h1><p>{html.escape(str(exc))}</p>"
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        if not head_only:
            self.wfile.write(data)
