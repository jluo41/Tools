"""The 📤 Delivery tab · ONE surface presenting what leaves the page (JL 260831).

The delivery/ category (roster: latex · word · slide · render) gets the same
treatment the evidence/ category got in servers/workbench/task-page/evidence.py: one tab, one segment
per lane, PRESENTATION ONLY. Storage, builders and their routes stay with the
lane contracts (`workbench-page/ref/delivery.md` is the paper contract for this file).

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

Every current lane resolves at `delivery/<lane>/`.  Readers may still inspect
an old flat Render folder during migration, but every builder and every saved
URL uses the nested category path.
"""
from __future__ import annotations

import datetime
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
.run-contract{margin:-2px 16px 10px;color:var(--mut);font-size:11.5px;line-height:1.5}
.run-contract summary{cursor:pointer}.run-contract .facts{padding:5px 8px;border:1px solid var(--line);border-radius:6px;background:var(--card)}
.run-contract b{color:var(--fg)}
"""


_LANES = (
    ("web", "🌐", "Web"),
    ("latex", "📜", "LaTeX"),
    ("word", "📝", "Word"),
    ("slide", "🎞", "Slides"),
    ("render", "📱", "Render"),
)

# One fixed Delivery Run per lane (JL 260928: "we just need one run ... run_delivery_webpage, no need for
# rd01_web, rd02_web"), named in the readable grammar (run_names.delivery_name): run-delivery-webpage.
# A rebuild reruns the same Run; the lane's built files are its result. Slides and render are pressed,
# never rebuilt by `page.py export`, so run_names does not mint them; their names here are for display.
FIXED_RUNS = {"web": "run-delivery-webpage", "latex": "run-delivery-latex", "word": "run-delivery-word",
              "slide": "run-delivery-slides", "render": "run-delivery-render"}
LANE_OF_RUN = {name: lane for lane, name in FIXED_RUNS.items()}
# Older numbered Delivery Runs (rdNN_<lane>) still show as history.
_DELIVERY_RUN_TARGET = re.compile(r"rd\d{2,}_(web|latex|word|slide|render)(?:_|$)", re.I)


def _delivery_run_instances(page_src: pathlib.Path) -> dict[str, list[tuple[str, str]]]:
    """Project recorded Page Delivery Runs without copying the Run catalogue."""
    from live.runs import local_runs

    found = {lane: [] for lane in ("web", "latex", "word", "slide", "render")}
    for row in local_runs(page_src):
        ticket = row.get("ticket")
        identity = ticket.stem if isinstance(ticket, pathlib.Path) else str(row.get("run_id", ""))
        match = _DELIVERY_RUN_TARGET.match(identity)
        if not match and identity not in LANE_OF_RUN:
            continue
        lane = LANE_OF_RUN.get(identity) or match.group(1).lower()
        run_id = ticket.stem if isinstance(ticket, pathlib.Path) else identity.removeprefix("P ")
        found[lane].append((run_id, str(row.get("status") or "unknown")))
    for lane in found:
        found[lane].sort(key=lambda item: (item[0] in LANE_OF_RUN,
                                           int((re.search(r"rd(\d+)", item[0], re.I) or [0, 0])[1]), item[0]))
    return found


def _delivery_run_contract(lane: str, recorded: list[tuple[str, str]],
                           page_src: pathlib.Path | None = None,
                           board_path: str = "", page_path: str = "",
                           read_only: bool = False) -> str:
    """One line under each lane: the lane's fixed Run, which a rebuild reruns."""
    return '<div class=run-contract><b>Run</b> <code>%s</code></div>' % html.escape(FIXED_RUNS[lane])


def _manifest(path: pathlib.Path):
    if not path.is_file():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return value if isinstance(value, dict) else None


def _check_row(label, state, detail):
    return {"label": label, "state": state, "detail": detail}


# The files a lane's build writes, by Page stem. `render` has no fixed name: any file counts.
_MAIN = {"web": ("index.html",), "latex": ("{stem}.pdf", "{stem}.tex"), "word": ("{stem}.docx",),
         "slide": ("{stem}-deck.html",), "render": ()}


def _when(path: pathlib.Path) -> str:
    return datetime.datetime.fromtimestamp(path.stat().st_mtime).strftime("%y%m%d %H:%M")


def check_delivery(page_src: pathlib.Path):
    """Is each delivery lane built from the current Page? Read-only; never rebuilds.

    By file time alone (JL 260928: no content hashes, no build record needed): a lane is
    current when its built files are at least as new as the Page source, stale when one is
    older, not built when it has none. The web lane's copy of the Page must also read the
    same as the Page.
    """
    page_src = pathlib.Path(page_src).resolve()
    base = page_src.parent
    source_mtime = page_src.stat().st_mtime
    lanes = []
    for lane, icon, label in _LANES:
        lane_dir = base / "delivery" / lane
        if lane == "render" and not lane_dir.is_dir() and (base / "render").is_dir():
            lane_dir = base / "render"
        names = [name.format(stem=page_src.stem) for name in _MAIN.get(lane, ())]
        files = [lane_dir / name for name in names if (lane_dir / name).is_file()]
        if not names and lane_dir.is_dir():
            files = sorted(p for p in lane_dir.iterdir() if p.is_file() and not p.name.startswith("."))
        rows, stale = [], False
        for path in files:
            old = path.stat().st_mtime < source_mtime
            stale = stale or old
            rows.append(_check_row(path.name, "stale" if old else "pass",
                                   ("built %s, before the Page last changed" if old else "built %s") % _when(path)))
        mirror = lane_dir / page_src.name
        if lane == "web" and files and mirror.is_file():
            same = mirror.read_text(encoding="utf-8", errors="replace") == page_src.read_text(encoding="utf-8", errors="replace")
            stale = stale or not same
            rows.append(_check_row("Page copy", "pass" if same else "stale",
                                   "reads the same as the Page" if same else "differs from the Page"))
        state = "not-built" if not files else "stale" if stale else "pass"
        lanes.append({"lane": lane, "icon": icon, "label": label, "state": state, "rows": rows})
    counts = {state: sum(1 for lane in lanes if lane["state"] == state) for state in ("pass", "stale", "not-built")}
    return {
        "schema": "page-delivery-consistency/v2",
        "source": {"path": page_src.relative_to(base).as_posix(), "mtime": source_mtime,
                   "saved": _when(page_src)},
        "overall": "stale" if counts["stale"] else "pass",
        "counts": counts,
        "lanes": lanes,
    }


def render_workspace(page_src: pathlib.Path, path_q: str, file_q: str) -> str:
    """Render the internal read-only Delivery Workspace check."""
    receipt = check_delivery(page_src)
    delivery_runs = _delivery_run_instances(page_src)
    state = receipt["overall"]
    state_icon = {"pass": "✅", "stale": "⚠️"}[state]
    counts = receipt["counts"]
    summary = "%s %d current · %d stale · %d not built" % (
        state_icon, counts["pass"], counts["stale"], counts["not-built"])
    cards = []
    for lane in receipt["lanes"]:
        icon = {"pass": "✅", "stale": "⚠️", "not-built": "⬜"}[lane["state"]]
        rows = "".join(
            "<li><b>%s</b> <span class=%s>%s</span><span class=mut>%s</span></li>" %
            (html.escape(row["label"]), row["state"], row["state"], html.escape(row["detail"]))
            for row in lane["rows"])
        run_contract = _delivery_run_contract(
            lane["lane"], delivery_runs[lane["lane"]], page_src,
            path_q, file_q, read_only=True)
        cards.append("<section class=card><h2>%s %s <span class=state-%s>%s</span></h2>"
                     "<ul>%s</ul>%s</section>" %
                     (lane["icon"], html.escape(lane["label"]), lane["state"],
                      lane["state"], rows or "<li>no delivery files</li>",
                      run_contract))
    source = receipt["source"]
    return f"""<!doctype html><meta charset=utf-8>
<title>📤 Delivery Space · {html.escape(page_src.stem)}</title>
<style>
:root{{--bg:#fff;--fg:#1c1d1f;--mut:#71727a;--line:#e4e4e7;--card:#f7f7f8;--acc:#3b6ea5;--bad:#a43d35;--warn:#996b00;--ok:#24733d}}
@media(prefers-color-scheme:dark){{--bg:#161719;--fg:#e8e8e6;--mut:#9a9a97;--line:#2c2e33;--card:#1d1f23;--acc:#7aa7d8;--bad:#f08b80;--warn:#e4bd62;--ok:#8bd49a}}
body{{margin:0;background:var(--bg);color:var(--fg);font:14px/1.55 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}
header{{padding:14px 18px 8px;border-bottom:1px solid var(--line)}}
h1{{font-size:18px;margin:0 0 3px}} h2{{font-size:14px;margin:0 0 4px}}
.mut{{color:var(--mut);font-size:12px}} code{{font:11.5px ui-monospace,Menlo,monospace}}
.source{{margin:12px 18px;padding:10px 12px;border:1px solid var(--line);border-radius:8px;background:var(--card)}}
.source div{{margin:2px 0}} .toolbar{{float:right;border:1px solid var(--line);background:var(--bg);color:var(--fg);border-radius:6px;padding:3px 8px;cursor:pointer}}
.grid{{display:grid;grid-template-columns:1fr;gap:10px;margin:12px 18px}}
.card{{border:1px solid var(--line);border-radius:8px;padding:10px 12px;background:var(--card)}}
.card ul{{padding-left:18px;margin:7px 0 0}} .card li{{margin:2px 0}} .card li b{{display:inline-block;min-width:112px}}
.pass,.state-pass{{color:var(--ok)}} .stale,.state-stale{{color:var(--bad)}} .unverified,.state-unverified{{color:var(--warn)}} .not-built,.state-not-built{{color:var(--mut)}}
.state-pass,.state-stale,.state-unverified,.state-not-built{{font-size:12px;font-weight:600}}
</style>
<header><button class=toolbar onclick="location.reload()">Refresh check</button>
<h1>📤 Delivery Space · {html.escape(page_src.stem)}</h1>
<div class=mut>Read-only consistency projection · Page source is authoritative · this view never rebuilds or edits delivery files</div></header>
<div class=source><div><b>Authority</b> <code>{html.escape(source["path"])}</code></div>
<div><b>Board / Folder</b> {html.escape(path_q or 'standalone Page')} · {html.escape(page_src.parent.name)}</div>
<div><b>Page saved</b> {html.escape(source["saved"])}</div><div><b>Result</b> {html.escape(summary)}</div></div>
<main class=grid>{''.join(cards)}</main>
"""


def _stamp(p: pathlib.Path) -> str:
    t = datetime.datetime.fromtimestamp(p.stat().st_mtime)
    return t.strftime("%y%m%d %H:%M")


def render(page_src: pathlib.Path, path_q: str, file_q: str, *,
           interactive: bool = True, asset_base: str | None = None) -> str:
    stem = page_src.stem
    base = page_src.parent
    delivery_runs = _delivery_run_instances(page_src)

    def row(icon, name, rel, hint, lane):
        p = base / rel
        if p.exists():
            state = "✅ built · %s" % _stamp(p)
        else:
            state = "⬜ not built — %s" % hint
        return ("<div class=row><b>%s %s</b><code>%s</code>"
                "<span class=mut>%s</span></div>%s"
                % (icon, name, html.escape(rel), html.escape(state),
                   _delivery_run_contract(lane, delivery_runs[lane], page_src,
                                          path_q, file_q)))

    rn = base / "delivery" / "render"
    if not rn.is_dir() and (base / "render").is_dir():
        rn = base / "render"
    render_files = sorted(f.name for f in rn.iterdir() if f.is_file()) if rn.is_dir() else []
    n_render = len(render_files)
    home = "\n".join([
        row("🌐", "Web", f"delivery/web/index.html",
            "no current web artifact exists", "web"),
        row("📜", "LaTeX", f"delivery/latex/{stem}.pdf",
            "the delivery writer has not built it", "latex"),
        row("📝", "Word", f"delivery/word/{stem}.docx",
            "the delivery writer has not built it", "word"),
        row("🎞", "Slides", f"delivery/slide/{stem}-deck.html",
            "authored on the 🎞 tab's ✨ bar, never auto-built here", "slide"),
        "<div class=row><b>📱 Render</b><code>delivery/render/</code>"
        "<span class=mut>%s</span></div>"
        % ("%d file(s) on disk · Folder-native writer live" % n_render if n_render
           else "empty · run the Folder-native render verb"),
        _delivery_run_contract("render", delivery_runs["render"], page_src,
                               path_q, file_q),
    ])
    from live.outline_prompts import assets_html as prompt_assets_html
    ctx = json.dumps({
        "path": path_q, "file": file_q, "stem": stem,
        "render_files": render_files,
        "render_legacy_flat": rn == base / "render",
        "interactive": interactive,
        "asset_base": asset_base.rstrip("/") if asset_base is not None else None,
    })
    return f"""<!doctype html><meta charset=utf-8>
<title>📤 Delivery · {html.escape(stem)}</title>
<style>{_CSS}</style>
{prompt_assets_html()}
<header><h1>📤 Delivery · {html.escape(stem)}</h1>
<div class=mut>one surface · four interactive lanes plus Web status · what leaves the page · builders and
storage stay with delivery/latex/ · delivery/word/ · delivery/slide/ · delivery/render/</div></header>
<div class=mut style="padding:0 16px 5px">Board: {html.escape(path_q or 'standalone Page')} · Folder: {html.escape(base.name)} · Page: {html.escape(file_q or page_src.name)}</div>
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
  function savedUrl(workbench, name) {{
    if (CTX.asset_base !== null) return CTX.asset_base + '/' + workbench + '/' + name;
    var p = decodeURIComponent(CTX.path || '');
    var cut = p.lastIndexOf('/board/');
    var base = cut >= 0 ? p.slice(0, cut)
             : (/\\.md$/.test(p) ? p.slice(0, p.lastIndexOf('/')) : '');
    if (!base) return '';
    var m = (CTX.file || '').match(/^(.*)\\/([^\\/]+)\\/\\2\\.md$/);
    if (m) return base + '/' + m[1] + '/' + m[2] + '/' + workbench + '/' + name;
    return base + '/' + workbench + '/' + name;
  }}
  /* build: a deterministic route safe to press on click; slides has an
     AUTHORING pen (claude -p) so it gets a ghost, never an auto-press. */
  var LANES = {{
    latex:  {{url: savedUrl('delivery/latex', CTX.stem + '-view.html'), route: CTX.interactive ? 'latex' : ''}},
    word:   {{url: savedUrl('delivery/word',  CTX.stem + '-view.html'), route: CTX.interactive ? 'word' : ''}},
    slides: {{url: savedUrl('delivery/slide', CTX.stem + '-deck.html'),
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
    sbar.style.display = id === 'slides' && CTX.interactive ? 'flex' : 'none';
    if (id === 'home') {{
      frame.style.display = 'none'; home.style.display = 'block'; return;
    }}
    home.style.display = 'none'; frame.style.display = 'block';
    var lane = LANES[id];
    if (id === 'render') {{ showRenders(lane.files); return; }}
    if (!lane.url) {{ ghost(lane.ghost || 'no saved view for ' + id); return; }}
    fetch(lane.url, {{method: 'HEAD'}}).then(function (r) {{
      if (r.ok) {{ frame.src = lane.url + '?embed'; return; }}
      if (!lane.route) {{ ghost(lane.ghost); return; }}
      fetch('/_board/' + lane.route, {{
        method: 'POST', headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{path: CTX.path, file: CTX.file,
          author: (function () {{ try {{ return localStorage.getItem('haipipe-word-author') || undefined; }}
                                 catch (e) {{ return undefined; }} }})()}})
      }}).then(function (r2) {{ return r2.json(); }})
        .then(function (j) {{
          if (j.ok && j.url) frame.src = j.url + '?embed';
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
    if (!CTX.interactive) return;
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
          if (u) {{ frame.src = ''; setTimeout(function () {{ frame.src = u + '?embed'; }}, 300); }}
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
        workspace = (q.get("workspace") or [""])[0].lower() in {"1", "true", "yes"}
        _p = {"path": path_q, "file": file_q}
        got = self.target(_p)
        file_q = _p["file"]      # a derived file= feeds the lane links too
        if got[0] is None:
            return self.reply(400, {"ok": False, "err": got[1]})
        if workspace:
            body = render_workspace(got[0], path_q, file_q).encode("utf-8")
        else:
            body = render(
                got[0], path_q, file_q,
                interactive=getattr(self, "delivery_interactive", True),
                asset_base=getattr(self, "delivery_asset_base", ""),
            ).encode("utf-8")
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
