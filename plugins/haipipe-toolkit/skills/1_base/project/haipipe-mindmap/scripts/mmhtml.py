"""The static page of a mind map, `<stem>.mindmap.html`: the map as the workbench card draws it (mmmap.py), read
only, and the file's Markdown notes rendered. One self-contained page, no script from the network; git ignores it
(`*.mindmap.html`), since the file rebuilds it on every change.
"""
from __future__ import annotations

import html
import re

import mmtree as MT


def inline(s: str) -> str:
    """Markdown inside a line: `code`, ![pictures](url), [links](url), **bold**, *italic*; everything else escaped."""
    keep = []

    def stash(h):
        keep.append(h)
        return f"\x00{len(keep) - 1}\x00"
    s = re.sub(r"`([^`]+)`", lambda m: stash(f"<code>{html.escape(m.group(1))}</code>"), str(s))
    s = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", lambda m: stash(        # a picture shows as itself, opens full size
        f'<a class=mm-pic data-pop="{html.escape(m.group(1), quote=True)}" href="{html.escape(m.group(2), quote=True)}" '
        f'target=_blank rel=noopener><img src="{html.escape(m.group(2), quote=True)}" alt="{html.escape(m.group(1), quote=True)}" '
        f'loading=lazy></a>'), s)
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: stash(        # a link opens in the workbench's pop-out
        f'<a data-pop="{html.escape(m.group(1), quote=True)}" href="{html.escape(m.group(2), quote=True)}" target=_blank '
        f'rel=noopener>{html.escape(m.group(1))}</a>'), s)
    s = html.escape(s, quote=False)
    s = re.sub(r"(\*\*|__)(.+?)\1", r"<strong>\2</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"<em>\1</em>", s)
    s = re.sub(r"(?<![\w_])_(?!\s)(.+?)(?<!\s)_(?!\w)", r"<em>\1</em>", s)
    return re.sub("\x00(\\d+)\x00", lambda m: keep[int(m.group(1))], s)


def blocks(text: str) -> str:
    """Block Markdown: headings, paragraphs, lists (nested by indent), quotes, fenced code, tables, rules."""
    lines, out, i = str(text).split("\n"), [], 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
        elif ln.lstrip().startswith("```"):
            j = i + 1
            while j < len(lines) and not lines[j].lstrip().startswith("```"):
                j += 1
            out.append("<pre><code>" + html.escape("\n".join(lines[i + 1:j])) + "</code></pre>")
            i = j + 1
        elif re.match(r"^#{1,6} ", ln):
            k = len(ln) - len(ln.lstrip("#"))
            out.append(f"<h{min(k + 1, 6)}>{inline(ln[k:].strip())}</h{min(k + 1, 6)}>")
            i += 1
        elif re.match(r"^\s*([-*_])\s*(\1\s*){2,}$", ln):
            out.append("<hr>")
            i += 1
        elif MT.BULLET.match(ln):
            j = i
            while j < len(lines) and (MT.BULLET.match(lines[j]) or (lines[j].startswith(" ") and lines[j].strip())):
                j += 1
            out.append(_list(lines[i:j]))
            i = j
        elif ln.startswith(">"):
            j = i
            while j < len(lines) and lines[j].startswith(">"):
                j += 1
            out.append("<blockquote>" + blocks("\n".join(x[1:].lstrip() for x in lines[i:j])) + "</blockquote>")
            i = j
        elif ln.strip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?[\s:|-]+\|?\s*$", lines[i + 1]):
            j = i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                j += 1
            cells = lambda r: [c.strip() for c in r.strip().strip("|").split("|")]
            head = "".join(f"<th>{inline(c)}</th>" for c in cells(ln))
            body = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells(r)) + "</tr>" for r in lines[i + 2:j])
            out.append(f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>")
            i = j
        else:
            j = i
            while j < len(lines) and lines[j].strip() and not MT.BULLET.match(lines[j]) and \
                    not re.match(r"^(#{1,6} |```|>)", lines[j]):
                j += 1
            out.append("<p>" + inline(" ".join(x.strip() for x in lines[i:j])) + "</p>")
            i = j
    return "\n".join(out)


def _list(lines: list) -> str:
    items = []
    stack = [(-1, items)]
    for ln in lines:
        m = MT.BULLET.match(ln)
        if not m:
            if stack[-1][1]:
                stack[-1][1][-1][0].append(ln.strip())
            continue
        ind = len(m.group(1).expandtabs(4))
        while stack[-1][0] >= ind and len(stack) > 1:
            stack.pop()
        item = ([m.group(2)], [])
        stack[-1][1].append(item)
        stack.append((ind, item[1]))

    def ul(xs):
        return "<ul>" + "".join(f"<li>{inline(' '.join(t))}{ul(k) if k else ''}</li>" for t, k in xs) + "</ul>"
    return ul(items)


CSS = """
:root{--bg:#ffffff;--fg:#1e1e1e;--mut:#5c636a;--line:#ced4da;--code:#f1f3f5;--link:#1864ab;--card:#ffffff;--wash:#f1f3f5;--acc:#1864ab}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#16181b;--fg:#e9ecef;--mut:#a5abb1;
--line:#3a3f45;--code:#23272b;--link:#74c0fc;--card:#1d1f22;--wash:#23272b}}
:root[data-theme="dark"]{--bg:#16181b;--fg:#e9ecef;--mut:#a5abb1;--line:#3a3f45;--code:#23272b;--link:#74c0fc;
--card:#1d1f22;--wash:#23272b}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 -apple-system,"Segoe UI",Nunito,sans-serif}
main{padding:28px 16px 64px}
h1{font-size:28px;margin:0 0 4px}.meta{color:var(--mut);font-size:13px;margin:0 0 18px}
.map{overflow-x:auto;margin:12px 0 24px}
a{color:var(--link)}code{background:var(--code);padding:1px 5px;border-radius:4px;font-size:.92em}
pre{background:var(--code);padding:12px;border-radius:8px;overflow:auto}pre code{background:none;padding:0}
table{border-collapse:collapse;margin:10px 0}th,td{border:1px solid var(--line);padding:4px 8px}
blockquote{margin:8px 0;padding-left:12px;border-left:3px solid var(--line);color:var(--mut)}
"""


def page(mm: MT.MindMap) -> str:
    """The static page: the map read only (as the workbench card draws it), the root's note and the free notes."""
    import mmmap
    title = MT.display(mm.meta.get("title") or mm.root.text)
    meta = " · ".join(f"{k}: {v}" for k, v in mm.meta.items() if k in ("built", "source", "updated"))
    note = blocks("\n".join(mm.root.note)) if mm.root.note else ""
    return (f'<!doctype html>\n<html lang=en><head><meta charset=utf-8>'
            f'<meta name=viewport content="width=device-width, initial-scale=1">'
            f'<title>{html.escape(title)} · mind map</title><style>{CSS}</style></head><body><main>'
            f'<h1>{inline(title)}</h1>' + (f'<p class=meta>{inline(meta)}</p>' if meta else "") +
            f'{note}<div class=map>{mmmap.draw(mm, "", False)}</div>{blocks(mm.tail) if mm.tail else ""}</main></body></html>\n')
