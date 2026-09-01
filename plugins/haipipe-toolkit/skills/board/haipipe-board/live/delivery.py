"""The 📤 Delivery tab · ONE surface presenting what leaves the page (JL 260831).

The delivery/ category (roster: latex · word · slide · render) gets the same
treatment the evidence/ category got in live/evidence.py: one tab, one segment
per lane, PRESENTATION ONLY. Storage, builders and their routes stay with the
lane contracts (`haipipe-plugin-delivery` is the paper contract for this file).

Segments: 🏠 What's built (a server-side stat of the four lanes) · 📜 LaTeX ·
📝 Word · 🎞 Slides · 📱 Render. LaTeX and Word are BUILT ON CLICK through
their own deterministic routes (/_board/latex, /_board/word) when the saved
view is missing — the same pens the old separate tabs pressed. Slides is
NEVER auto-built: its pen is `claude -p` authoring (/_board/autodeck), so
the segment carries the ✨ bar the shell's native 🎞 tab used to hold (that
tab folded 260831 with the studio fold) — one explicit press authors, a
missing deck is a ghost until then. Render is built by the Folder-native
Application render verb; this presenter lists and opens whatever that live
lane holds. A served render POST remains optional.

Render resolves canonical `delivery/render/` first and keeps flat `render/`
readable. The older LaTeX/Word/Slide views still resolve through their flat
symlink stubs (`latex -> delivery/latex`, QPf1) during category migration.
"""
from __future__ import annotations

import datetime
import html
import json
import pathlib

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
#home{padding:12px 16px;max-width:880px}
#home .row{display:flex;gap:10px;align-items:baseline;padding:7px 10px;
 border:1px solid var(--line);border-radius:8px;margin:8px 0;background:var(--card)}
#home .row b{min-width:110px}
#home .row code{font:12.5px ui-monospace,Menlo,monospace}
#seg{display:none;border:0;width:100%;height:calc(100vh - 92px)}
#sbar{display:none;gap:6px;padding:6px 16px;border-bottom:1px solid var(--line);
 align-items:center}
#sbar input{flex:1;border:1px solid var(--line);background:var(--bg);
 color:var(--fg);border-radius:6px;padding:3px 8px;font-size:13px}
#sbar button{border:1px solid var(--line);background:var(--card);color:var(--fg);
 border-radius:6px;padding:3px 10px;font-size:13px;cursor:pointer}
#sbar .st{color:var(--mut);font-size:12px;max-width:40%}
.ghost{color:var(--mut);padding:24px 16px;font-size:13.5px}
"""


def _stamp(p: pathlib.Path) -> str:
    t = datetime.datetime.fromtimestamp(p.stat().st_mtime)
    return t.strftime("%y%m%d %H:%M")


def render(page_src: pathlib.Path, path_q: str, file_q: str) -> str:
    stem = page_src.stem
    base = page_src.parent

    def row(icon, name, rel, hint):
        p = base / rel
        if p.exists():
            state = "✅ built · %s" % _stamp(p)
        else:
            state = "⬜ not built — %s" % hint
        return ("<div class=row><b>%s %s</b><code>%s</code>"
                "<span class=mut>%s</span></div>"
                % (icon, name, html.escape(rel), html.escape(state)))

    rn = base / "delivery" / "render"
    if not rn.is_dir() and (base / "render").is_dir():
        rn = base / "render"
    render_files = sorted(f.name for f in rn.iterdir() if f.is_file()) if rn.is_dir() else []
    n_render = len(render_files)
    home = "\n".join([
        row("📜", "LaTeX", f"latex/{stem}.pdf", "the segment compiles it on first open"),
        row("📝", "Word", f"word/{stem}.docx", "the segment builds it on first open"),
        row("🎞", "Slides", f"slide/{stem}-deck.html",
            "authored on the 🎞 tab's ✨ bar, never auto-built here"),
        "<div class=row><b>📱 Render</b><code>render/</code>"
        "<span class=mut>%s</span></div>"
        % ("%d file(s) on disk · Folder-native writer live" % n_render if n_render
           else "empty · run the Folder-native render verb"),
    ])
    ctx = json.dumps({
        "path": path_q, "file": file_q, "stem": stem,
        "render_files": render_files,
        "render_legacy_flat": rn == base / "render",
    })
    return f"""<!doctype html><meta charset=utf-8>
<title>📤 Delivery · {html.escape(stem)}</title>
<style>{_CSS}</style>
<header><h1>📤 Delivery · {html.escape(stem)}</h1>
<div class=mut>one surface, four lanes · what leaves the page · builders and
storage stay with latex/ · word/ · slide/ · render/</div></header>
<nav>
<button class=on data-seg=home>🏠 What's built</button>
<button data-seg=latex>📜 LaTeX</button>
<button data-seg=word>📝 Word</button>
<button data-seg=slides>🎞 Slides</button>
<button data-seg=render>📱 Render</button>
</nav>
<div id=home>{home}</div>
<div id=sbar><input id=sask placeholder="the ask, optional — ✨ authors the deck from this page's .md">
<button id=sgo>✨ Author</button><span class=st id=sst></span></div>
<iframe id=seg></iframe>
<script>
(function () {{
  'use strict';
  var CTX = {ctx};
  function savedUrl(plugin, name) {{
    var p = decodeURIComponent(CTX.path || '');
    var cut = p.lastIndexOf('/board/');
    var base = cut >= 0 ? p.slice(0, cut)
             : (/\\.md$/.test(p) ? p.slice(0, p.lastIndexOf('/')) : '');
    if (!base) return '';
    var m = (CTX.file || '').match(/^(.*)\\/([^\\/]+)\\/\\2\\.md$/);
    if (m) return base + '/' + m[1] + '/' + m[2] + '/' + plugin + '/' + name;
    return base + '/' + plugin + '/' + name;
  }}
  /* build: a deterministic route safe to press on click; slides has an
     AUTHORING pen (claude -p) so it gets a ghost, never an auto-press. */
  var LANES = {{
    latex:  {{url: savedUrl('latex', CTX.stem + '-view.html'), route: 'latex'}},
    word:   {{url: savedUrl('word',  CTX.stem + '-view.html'), route: 'word'}},
    slides: {{url: savedUrl('slide', CTX.stem + '-deck.html'),
              ghost: 'No deck yet \\u2014 the \\u2728 bar above authors one from ' +
                     'this page\\u2019s .md (claude -p, a minute or two).'}},
    render: {{files: CTX.render_files || []}}
  }};
  var frame = document.getElementById('seg'),
      home = document.getElementById('home'),
      sbar = document.getElementById('sbar');
  function ghost(msg) {{
    frame.srcdoc = '<p style="font:13.5px sans-serif;color:#888;padding:24px">' +
                   msg + '</p>';
  }}
  function esc(s) {{
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }}
  function showRenders(files) {{
    if (!files.length) {{
      ghost('No recipient preview yet \\u2014 run the Folder-native Application render verb.');
      return;
    }}
    var lane = CTX.render_legacy_flat ? 'render' : 'delivery/render';
    var items = files.map(function (name) {{
      var url = savedUrl(lane, name);
      return '<li><a target="_blank" href="' + esc(url) + '">' + esc(name) + '</a></li>';
    }}).join('');
    frame.srcdoc = '<div style="font:13.5px sans-serif;padding:18px">' +
      '<b>Recipient previews</b><ul>' + items + '</ul>' +
      '<p style="color:#777">Derived files; edit the owning D4 division, then re-render.</p></div>';
  }}
  function show(id, btn) {{
    var all = document.querySelectorAll('nav button');
    for (var i = 0; i < all.length; i++) all[i].className = '';
    btn.className = 'on';
    sbar.style.display = id === 'slides' ? 'flex' : 'none';
    if (id === 'home') {{
      frame.style.display = 'none'; home.style.display = 'block'; return;
    }}
    home.style.display = 'none'; frame.style.display = 'block';
    var lane = LANES[id];
    if (id === 'render') {{ showRenders(lane.files); return; }}
    if (!lane.url) {{ ghost(lane.ghost || 'no saved view for ' + id); return; }}
    fetch(lane.url, {{method: 'HEAD'}}).then(function (r) {{
      if (r.ok) {{ frame.src = lane.url + '?plain'; return; }}
      if (!lane.route) {{ ghost(lane.ghost); return; }}
      fetch('/_board/' + lane.route, {{
        method: 'POST', headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{path: CTX.path, file: CTX.file}})
      }}).then(function (r2) {{ return r2.json(); }})
        .then(function (j) {{
          if (j.ok && j.url) frame.src = j.url + '?plain';
          else ghost('⚠ ' + ((j && j.err) || 'the ' + id + ' build failed'));
        }});
    }});
  }}
  var btns = document.querySelectorAll('nav button');
  for (var i = 0; i < btns.length; i++) {{
    (function (b) {{
      b.addEventListener('click', function () {{ show(b.getAttribute('data-seg'), b); }});
    }})(btns[i]);
  }}
  /* ✨ the deck's AUTHORING pen, moved here from the shell's native 🎞 tab
     (260831): one explicit press, claude -p server-side, then frame what
     landed. Never pressed by a mere view. */
  (function () {{
    var go = document.getElementById('sgo'), ask = document.getElementById('sask'),
        st = document.getElementById('sst');
    function run() {{
      go.disabled = true;
      st.textContent = '🎞 Claude is authoring… (a minute or two)';
      fetch('/_board/autodeck', {{
        method: 'POST', headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{path: CTX.path, file: CTX.file,
                               prompt: ask.value.trim()}})
      }}).then(function (r) {{ return r.json(); }})
        .then(function (j) {{
          go.disabled = false;
          if (!j.ok) {{ st.textContent = '✋ ' + (j.err || 'refused'); return; }}
          st.textContent = '✅ ' + (j.slides || '') + ' slides — loading';
          var u = LANES.slides.url;
          if (u) {{ frame.src = ''; setTimeout(function () {{ frame.src = u + '?plain'; }}, 300); }}
        }})
        .catch(function () {{ go.disabled = false; st.textContent = '✋ server unreachable'; }});
    }}
    go.addEventListener('click', run);
    ask.addEventListener('keydown', function (e) {{ if (e.key === 'Enter') run(); }});
  }})();
}})();
</script>"""


class DeliveryTabMixin:
    """The 📤 tab. Presentation only: no storage, no writer, no gate."""

    # ---- GET/HEAD /_board/delivery?path=…&file=… ------------------------
    def delivery_tab_view(self, head_only=False):
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

    # ---- POST /_board/delivery — the shell's write() twin, writes nothing
    def plug_delivery(self, p):
        from urllib.parse import quote
        got = self.target(p)
        if got[0] is None:
            return None, got[1]
        return {"url": "/_board/delivery?path=%s&file=%s"
                % (quote(p.get("path") or ""), quote(p.get("file") or ""))}, None
