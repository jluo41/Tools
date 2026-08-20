"""🧮 Value · every number the page owes or uses, joined both ways (QPw4v).

A probe card is ONE question whose answer holds SEVERAL numbers, and a sentence
uses one of them (JL 260819). Until the `PP<NN>.v<n>` id existed, both sentences
could only cite `PP01`, so nobody could tell which number each used and a value
nobody used looked exactly like one everybody did.

NO STORAGE and NO WRITER, by contract (`haipipe-plugin-value` §🧊): the number
lives in `probe/PP<NN>/proof/` with its source, run and sha256. This module reads
`card.md`'s `## Values` block and the page's own prose, and joins them.
"""
from __future__ import annotations

import html
import pathlib
import re

_ROW = re.compile(r"^-\s*(v\d+)\s*·\s*(.+?)\s*·\s*(.+?)\s*(?:·\s*(.+?))?\s*$", re.M)
_CITE = re.compile(r"\b(PP\d+)\.(v\d+)\b")
_DIV = re.compile(r"(?m)^###\s+(\d+)\s*·")


def _e(s) -> str:
    return html.escape(str(s), quote=True)


def read_values(page_src: pathlib.Path):
    """-> {(PP id, v id): (what it is, the number, where from)}, from every card."""
    out = {}
    d = page_src.parent / "probe"
    if not d.is_dir():
        return out
    for card in sorted(d.glob("PP*/card.md")):
        pid = card.parent.name.split("-")[0]
        txt = card.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"(?ms)^##\s+Values\s*$(.*?)(?=^##\s|\Z)", txt)
        if not m:
            continue
        for vid, what, num, frm in _ROW.findall(m.group(1)):
            out[(pid, vid)] = (what, num, frm or "")
    return out


def read_citations(page_src: pathlib.Path):
    """-> {(PP id, v id): [division numbers]}, from the page's own prose.

    The division is by POSITION, the same way the outline surface counts them, so
    a value cited in §1 reports §1 and not the nearest heading text."""
    txt = page_src.read_text(encoding="utf-8", errors="replace")
    marks = [(m.start(), m.group(1)) for m in _DIV.finditer(txt)]
    out = {}
    for m in _CITE.finditer(txt):
        sec = ""
        for pos, num in marks:
            if pos < m.start():
                sec = num
            else:
                break
        out.setdefault((m.group(1), m.group(2)), [])
        if sec and sec not in out[(m.group(1), m.group(2))]:
            out[(m.group(1), m.group(2))].append(sec)
    return out


def rows(page_src: pathlib.Path):
    """-> [(state, id, what, number, from, used-by)], every value and every cite.

    THREE states, and an empty cell is a status rather than a blank:
      ✅ bound      both sides agree
      🎈 unused     a card holds it, no sentence cites it
      🚨 unsourced  a sentence cites it, no card declares it
    """
    have, used = read_values(page_src), read_citations(page_src)
    out = []
    for key in sorted(set(have) | set(used)):
        pid, vid = key
        what, num, frm = have.get(key, ("", "", ""))
        secs = used.get(key, [])
        if key not in have:
            st = "unsourced"
        elif not secs:
            st = "unused"
        else:
            st = "bound"
        out.append((st, "%s.%s" % (pid, vid), what, num, frm,
                    " · ".join("§" + s for s in secs)))
    return out


def render(page_src: pathlib.Path) -> str:
    r = rows(page_src)
    n = {"bound": 0, "unused": 0, "unsourced": 0}
    for st, *_ in r:
        n[st] += 1
    head = ('<h1>🧮 Values</h1><p class=mut>%d bound · %d used by nobody · '
            '%d cited with no card</p>' % (n["bound"], n["unused"], n["unsourced"]))
    if not r:
        return ("<style>%s</style>%s<p class=mut>No <code>## Values</code> block on "
                "any card, and no <code>PP&lt;NN&gt;.v&lt;n&gt;</code> in the prose. "
                "A value is written at EVIDENCE, stage ② BIND.</p>" % (_CSS, head))
    body = []
    for st, vid, what, num, frm, secs in r:
        icon = {"bound": "✅", "unused": "🎈", "unsourced": "🚨"}[st]
        note = {"bound": "", "unused": "answered for nobody",
                "unsourced": "no card declares it"}[st]
        body.append(
            '<tr class=%s><td>%s <code>%s</code></td><td>%s</td><td class=num>%s</td>'
            '<td class=frm>%s</td><td>%s</td></tr>'
            % (st, icon, _e(vid), _e(what or note), _e(num),
               _e(frm) or '<span class=warn>names no file</span>',
               _e(secs) or '<span class=mut>%s</span>' % note))
    return ("<style>%s</style>%s<table><tr><th>id</th><th>what it is</th>"
            "<th>number</th><th>read from</th><th>used by</th></tr>%s</table>"
            % (_CSS, head, "".join(body)))


_CSS = """
:root{--bg:#fff;--fg:#1a1a19;--mut:#6b6b68;--line:#e3e3e0;--card:#fafaf8;
 --warn:#b06a2c;--ok:#3f7a4d}
@media(prefers-color-scheme:dark){:root{--bg:#161719;--fg:#e8e8e6;--mut:#9a9a97;
 --line:#2c2e33;--card:#1d1f23;--warn:#e0955a;--ok:#7dbb87}}
body{margin:0;padding:16px;background:var(--bg);color:var(--fg);
 font:15px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
h1{font-size:17px;margin:0 0 2px}.mut{color:var(--mut);font-size:13px}
table{border-collapse:collapse;width:100%;margin-top:12px;font-size:14px}
th{text-align:left;font-size:12px;text-transform:uppercase;letter-spacing:.03em;
 color:var(--mut);border-bottom:1px solid var(--line);padding:4px 8px 4px 0}
td{padding:5px 8px 5px 0;border-bottom:1px solid var(--line);vertical-align:top}
td.num{font:600 14px ui-monospace,Menlo,monospace}
td.frm{font:12px ui-monospace,Menlo,monospace;color:var(--mut)}
code{font:12.5px ui-monospace,Menlo,monospace}
tr.unused td{background:var(--card)}
tr.unsourced td{background:var(--card)}
.warn{color:var(--warn);font-weight:600}
"""


class ValueMixin:
    """The 🧮 tab. No storage, no writer: the numbers live in probe cards."""

    # ---- GET/HEAD /_board/value?path=…&file=… ---------------------------
    def value_view(self, head_only=False):
        from urllib.parse import parse_qs, urlparse
        q = parse_qs(urlparse(self.path).query)
        got = self.target({"path": (q.get("path") or [""])[0],
                           "file": (q.get("file") or [""])[0]})
        if got[0] is None:
            return self.reply(400, {"ok": False, "err": got[1]})
        body = render(got[0]).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    # ---- POST /_board/value — the shell's write() twin, writes nothing ---
    def plug_value(self, p):
        from urllib.parse import quote
        got = self.target(p)
        if got[0] is None:
            return None, got[1]
        return {"url": "/_board/value?path=%s&file=%s"
                % (quote(p.get("path") or ""), quote(p.get("file") or ""))}, None
