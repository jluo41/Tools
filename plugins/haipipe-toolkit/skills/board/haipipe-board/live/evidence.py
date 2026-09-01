"""The 🧾 Evidence tab · ONE surface presenting four lanes (JL 260831).

"We still have the subfolder for bibex, etc, but we just need one evidence
plugin, to present bibex, display, etc." So this mixin owns PRESENTATION
ONLY: a live GET composing six segments — ⧉ By bullet (the generated
outline/<stem>-evidence.md snapshot, the join), 📚 Citations (the bibex
saved workbench), 🚪 Cards (the probe saved view), 🧮 Values (the live
/_board/value route), 🖼 Displays (the display saved view), 🔗 Pagex (the
borrow view, pens inline — its standalone 🔗 registry row folded in here
260831, the task lane's read follows when a pagex card learns a task
unit's status). Storage, writers,
walls and the three human gates (verified: / read: / accepted:) stay with the
lane contracts (`haipipe-plugin-evidence` is the paper contract for this
file). Like the 🧮 tab: no storage, no writer, nothing stored, never stale.

A segment whose saved view does not exist yet is BUILT ON CLICK through the
lane's own POST route (/_board/bibex, /_board/probe, /_board/display, /_board/pagex), which
is the same pen the old separate tabs pressed.
"""
from __future__ import annotations

import html
import json
import pathlib
import re

_CSS = """
:root{--bg:#ffffff;--fg:#1c1d1f;--mut:#71727a;--line:#e4e4e7;--card:#f7f7f8;--acc:#3b6ea5}
@media(prefers-color-scheme:dark){:root{--bg:#161719;--fg:#e8e8e6;--mut:#9a9a97;
 --line:#2c2e33;--card:#1d1f23;--acc:#7aa7d8}}
body{margin:0;background:var(--bg);color:var(--fg);
 font:15px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
header{padding:10px 16px 0}
h1{font-size:16px;margin:0}
.mut{color:var(--mut);font-size:12.5px}
nav{display:flex;gap:6px;padding:8px 16px;border-bottom:1px solid var(--line);
 position:sticky;top:0;background:var(--bg)}
nav button{border:1px solid var(--line);background:var(--card);color:var(--fg);
 border-radius:6px;padding:3px 10px;font-size:13px;cursor:pointer}
nav button.on{border-color:var(--acc);color:var(--acc);font-weight:600}
#bybullet{padding:12px 16px;max-width:880px}
#bybullet pre{background:var(--card);padding:8px 10px;border-radius:6px;
 overflow-x:auto;font:12.5px ui-monospace,Menlo,monospace}
#bybullet code{font:12.5px ui-monospace,Menlo,monospace;background:var(--card);
 padding:0 3px;border-radius:4px}
#bybullet h2{font-size:15px;margin:14px 0 4px}
#bybullet h3{font-size:13.5px;margin:12px 0 3px}
#bybullet ul{margin:4px 0;padding-left:22px}
#seg{display:none;border:0;width:100%;height:calc(100vh - 92px)}
.ghost{color:var(--mut);padding:24px 16px;font-size:13.5px}
"""


def _md_lite(text: str) -> str:
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
        s = raw.lstrip()
        if s.startswith("### "):
            if in_ul: out.append("</ul>"); in_ul = False
            out.append("<h3>%s</h3>" % line.lstrip()[4:])
        elif s.startswith("## "):
            if in_ul: out.append("</ul>"); in_ul = False
            out.append("<h2>%s</h2>" % line.lstrip()[3:])
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


def render(page_src: pathlib.Path, path_q: str, file_q: str) -> str:
    stem = page_src.stem
    folded = page_src.parent.name == stem
    folder = page_src.parent if folded else None
    ev = (folder / "outline" / f"{stem}-evidence.md") if folder else \
         (page_src.parent / "outline" / f"{stem}-evidence.md")
    if ev.exists():
        body = _md_lite(ev.read_text(encoding="utf-8"))
        note = str(ev.name)
    else:
        body = ("<div class=ghost>No evidence snapshot yet: "
                "<code>cli/evidence-status.py</code> (or an OUTLINE pass) "
                "writes <code>outline/%s-evidence.md</code>.</div>" % html.escape(stem))
        note = "no snapshot on disk"
    ctx = json.dumps({"path": path_q, "file": file_q, "stem": stem,
                      "folded": folded})
    return f"""<!doctype html><meta charset=utf-8>
<title>🧾 Evidence · {html.escape(stem)}</title>
<style>{_CSS}</style>
<header><h1>🧾 Evidence · {html.escape(stem)}</h1>
<div class=mut>one surface, five lanes · storage and gates stay with
bibex/ · probe/ · display/ · pagex/ · the cards' value rows ({html.escape(note)})</div></header>
<nav>
<button class=on data-seg=bybullet>⧉ By bullet</button>
<button data-seg=bibex>📚 Citations</button>
<button data-seg=probe>🚪 Cards</button>
<button data-seg=value>🧮 Values</button>
<button data-seg=display>🖼 Displays</button>
<button data-seg=pagex>🔗 Pagex</button>
</nav>
<div id=bybullet>{body}</div>
<iframe id=seg></iframe>
<script>
(function () {{
  'use strict';
  var CTX = {ctx};
  function savedUrl(plugin, ext) {{
    var p = decodeURIComponent(CTX.path || '');
    var cut = p.lastIndexOf('/board/');
    var base = cut >= 0 ? p.slice(0, cut)
             : (/\\.md$/.test(p) ? p.slice(0, p.lastIndexOf('/')) : '');
    if (!base) return '';
    var m = (CTX.file || '').match(/^(.*)\\/([^\\/]+)\\/\\2\\.md$/);
    if (m) return base + '/' + m[1] + '/' + m[2] + '/' + plugin + '/' + m[2] + (ext || '-view.html');
    return base + '/' + plugin + '/' + CTX.stem + (ext || '-view.html');
  }}
  var LANES = {{
    bibex:   {{ext: '-bib.html',  route: 'bibex'}},
    probe:   {{ext: '-view.html', route: 'probe'}},
    display: {{ext: '-view.html', route: 'display'}},
    pagex:   {{ext: '-view.html', route: 'pagex'}},
    value:   {{live: '/_board/value?path=' + encodeURIComponent(CTX.path)
                    + '&file=' + encodeURIComponent(CTX.file)}}
  }};
  var frame = document.getElementById('seg'),
      bybullet = document.getElementById('bybullet');
  function show(id, btn) {{
    var all = document.querySelectorAll('nav button');
    for (var i = 0; i < all.length; i++) all[i].className = '';
    btn.className = 'on';
    if (id === 'bybullet') {{
      frame.style.display = 'none'; bybullet.style.display = 'block'; return;
    }}
    bybullet.style.display = 'none'; frame.style.display = 'block';
    var lane = LANES[id];
    if (lane.live) {{ frame.src = lane.live; return; }}
    var url = savedUrl(id, lane.ext);
    fetch(url, {{method: 'HEAD'}}).then(function (r) {{
      if (r.ok) {{ frame.src = url + '?plain'; return; }}
      /* not built yet: press the lane's own pen, then load what it names */
      fetch('/_board/' + lane.route, {{
        method: 'POST', headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{path: CTX.path, file: CTX.file}})
      }}).then(function (r2) {{ return r2.json(); }})
        .then(function (j) {{
          if (j.ok && j.url) frame.src = j.url + '?plain';
          else frame.srcdoc = '<p style="font:13px sans-serif;color:#888;padding:20px">⚠ ' +
                              ((j && j.err) || 'the ' + id + ' view failed') + '</p>';
        }});
    }});
  }}
  var btns = document.querySelectorAll('nav button');
  for (var i = 0; i < btns.length; i++) {{
    (function (b) {{
      b.addEventListener('click', function () {{ show(b.getAttribute('data-seg'), b); }});
    }})(btns[i]);
  }}
}})();
</script>"""


class EvidenceTabMixin:
    """The 🧾 tab. Presentation only: no storage, no writer, no gate."""

    # ---- GET/HEAD /_board/evidence?path=…&file=… ------------------------
    def evidence_tab_view(self, head_only=False):
        from urllib.parse import parse_qs, urlparse
        q = parse_qs(urlparse(self.path).query)
        path_q = (q.get("path") or [""])[0]
        file_q = (q.get("file") or [""])[0]
        got = self.target({"path": path_q, "file": file_q})
        if got[0] is None:
            return self.reply(400, {"ok": False, "err": got[1]})
        body = render(got[0], path_q, file_q).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    # ---- POST /_board/evidence — the shell's write() twin, writes nothing
    def plug_evidence(self, p):
        from urllib.parse import quote
        got = self.target(p)
        if got[0] is None:
            return None, got[1]
        return {"url": "/_board/evidence?path=%s&file=%s"
                % (quote(p.get("path") or ""), quote(p.get("file") or ""))}, None
