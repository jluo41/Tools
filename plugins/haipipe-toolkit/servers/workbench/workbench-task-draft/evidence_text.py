"""Small Markdown-to-HTML helpers the Evidence view's cards share."""
from __future__ import annotations

import html
import re

def _md_lite(text: str, heading_prefix: str = "") -> str:
    """Enough markdown for the generated evidence snapshot: headings,
    bullets, fences, bold, inline code. Never trusted with raw HTML."""
    out, in_pre, in_ul = [], False, False
    for raw in text.split("\n"):
        line = html.escape(raw, quote=False)
        if raw.strip().startswith("```"):
            if in_ul: out.append("</ul>"); in_ul = False
            out.append("<pre>" if not in_pre else "</pre>")
            in_pre = not in_pre
            continue
        if in_pre:
            out.append(line)
            continue
        line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
        line = re.sub(r"`([^`]+)`", r"<code>\1</code>", line)

        def link(match):
            label, href = match.group(1), html.unescape(match.group(2))
            # The binding map writes only repo-relative Run/Result links;
            # permit ordinary web links too, but never let a markdown field
            # inject a script/data URL into the live Board surface.
            if not (href.startswith(("../", "./", "/", "https://", "http://"))):
                return label
            return ('<a href="%s" target="_blank" rel="noopener">%s</a>' %
                    (html.escape(href, quote=True), label))

        line = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, line)
        s = raw.lstrip()
        heading_attr = ""
        if heading_prefix and s.startswith(("## ", "### ")):
            heading = s.lstrip("# ").split(" ·", 1)[0].strip()
            safe = re.sub(r"[^A-Za-z0-9_-]+", "-", heading).strip("-")
            if safe:
                heading_attr = ' id="%s"' % html.escape(
                    heading_prefix + safe, quote=True
                )
        if s.startswith("### "):
            if in_ul: out.append("</ul>"); in_ul = False
            out.append("<h3%s>%s</h3>" % (heading_attr, line.lstrip()[4:]))
        elif s.startswith("## "):
            if in_ul: out.append("</ul>"); in_ul = False
            out.append("<h2%s>%s</h2>" % (heading_attr, line.lstrip()[3:]))
        elif s.startswith("- "):
            if not in_ul: out.append("<ul>"); in_ul = True
            out.append("<li>%s</li>" % line.lstrip()[2:])
        elif not s:
            if in_ul: out.append("</ul>"); in_ul = False
        else:
            out.append("<p>%s</p>" % line)
    if in_ul: out.append("</ul>")
    if in_pre: out.append("</pre>")
    return "\n".join(out)


_ITEM_HEADING = re.compile(r"^###\s+([^·]+?)\s*·\s*(.*)$")
_FIELD = re.compile(r"^-\s+\*\*([^*]+?)\*\*\s*:\s*(.*)$")


def _inline_lite(text: str) -> str:
    """Safe inline rendering for the compact Evidence Item cards."""
    line = html.escape(text.strip(), quote=False)
    line = re.sub(r"`([^`]+)`", r"<code>\1</code>", line)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
