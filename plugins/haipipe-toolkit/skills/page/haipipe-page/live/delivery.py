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

Every current lane resolves at `delivery/<lane>/`.  Readers may still inspect
an old flat Render folder during migration, but every builder and every saved
URL uses the nested category path.
"""
from __future__ import annotations

import datetime
import hashlib
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
"""


_LANES = (
    ("web", "🌐", "Web"),
    ("latex", "📜", "LaTeX"),
    ("word", "📝", "Word"),
    ("slide", "🎞", "Slides"),
    ("render", "📱", "Render"),
)


def _sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _manifest(path: pathlib.Path):
    if not path.is_file():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return value if isinstance(value, dict) else None


def _inside(base: pathlib.Path, raw):
    if not isinstance(raw, str) or not raw.strip():
        return None
    candidate = pathlib.Path(raw)
    if candidate.is_absolute():
        return None
    try:
        resolved = (base / candidate).resolve()
        resolved.relative_to(base.resolve())
    except (OSError, ValueError):
        return None
    return resolved


def _source_path_matches(base: pathlib.Path, page_src: pathlib.Path, raw) -> bool:
    if not isinstance(raw, str) or not raw.strip():
        return True
    actual = page_src.resolve().relative_to(base.resolve()).as_posix()
    expected = pathlib.PurePosixPath(raw.replace("\\", "/")).as_posix()
    return expected == actual or pathlib.PurePosixPath(expected).name == page_src.name


def _source_fields(data):
    if not isinstance(data, dict):
        return None, None
    source = data.get("source")
    if isinstance(source, dict):
        return source.get("path"), source.get("sha256")
    return data.get("source_page"), data.get("source_sha256")


def _artifact_specs(data, lane):
    """Return (label, path, expected_sha256) entries from either manifest shape."""
    if not isinstance(data, dict):
        return []
    raw = data.get("artifacts") if isinstance(data.get("artifacts"), dict) else None
    if raw is None:
        outputs = data.get("outputs")
        raw = outputs.get(lane) if isinstance(outputs, dict) else None
        if raw is None and lane == "slide" and isinstance(outputs, dict):
            raw = outputs.get("slides")
    if not isinstance(raw, dict):
        return []
    specs = []
    for key, value in raw.items():
        if key.endswith("_sha256") or key in {"sha256", "status", "build", "draft_consistency", "pdf_twin"}:
            continue
        if not isinstance(value, str) or not value.strip():
            continue
        expected = raw.get("sha256") if key == "path" else raw.get(key + "_sha256")
        specs.append((key, value, expected if isinstance(expected, str) else None))
    return specs


def _marker_source_hash(path: pathlib.Path):
    if not path.is_file():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    match = re.search(r"source_sha256[\"']?\s*[=:]\s*[\"']?([0-9a-f]{64})", text, re.I)
    return match.group(1).lower() if match else None


def _check_row(label, state, detail):
    return {"label": label, "state": state, "detail": detail}


def check_delivery(page_src: pathlib.Path):
    """Read-only consistency receipt for the current Page source and deliveries.

    The Page Markdown is the authority. This function never rebuilds, edits, or
    promotes an artifact; it only compares the current source with the saved
    delivery manifests, mirrors, hashes, and modification times.
    """
    page_src = pathlib.Path(page_src).resolve()
    base = page_src.parent
    source_hash = _sha256(page_src)
    source_mtime = page_src.stat().st_mtime
    actual_source = page_src.relative_to(base).as_posix()
    root_manifest_path = base / "delivery" / "build-manifest.json"
    root_manifest = _manifest(root_manifest_path)
    lanes = []

    for lane, icon, label in _LANES:
        lane_dir = base / "delivery" / lane
        if lane == "render" and not lane_dir.is_dir() and (base / "render").is_dir():
            lane_dir = base / "render"
        lane_manifest_path = lane_dir / "build-manifest.json"
        lane_manifest = _manifest(lane_manifest_path)
        data = lane_manifest or root_manifest
        manifest_path = lane_manifest_path if lane_manifest else root_manifest_path if root_manifest else None
        manifest_source_path, manifest_source_hash = _source_fields(data)
        if data is None:
            manifest_source_path, manifest_source_hash = None, None
        specs = _artifact_specs(data, lane)
        files = []
        artifact_rows = []
        hard_failure = False
        hash_unverified = False
        has_material = lane_dir.is_dir() and any(p.is_file() for p in lane_dir.iterdir())

        for key, raw_path, expected_hash in specs:
            path = _inside(base, raw_path)
            lane_path = _inside(lane_dir, raw_path)
            if lane_path is not None and (path is None or not path.exists()):
                path = lane_path
            if path is None:
                artifact_rows.append(_check_row(key, "stale", "manifest path is outside this Page"))
                hard_failure = True
                continue
            has_material = True
            if not path.is_file():
                artifact_rows.append(_check_row(key, "stale", "missing: %s" % raw_path))
                hard_failure = True
                continue
            files.append(path)
            if expected_hash:
                actual_hash = _sha256(path)
                if actual_hash != expected_hash:
                    artifact_rows.append(_check_row(key, "stale", "hash differs: %s" % raw_path))
                    hard_failure = True
                else:
                    artifact_rows.append(_check_row(key, "pass", raw_path))
            else:
                artifact_rows.append(_check_row(key, "unverified", "no artifact hash in manifest"))
                hash_unverified = True

        if lane == "web":
            index = lane_dir / "index.html"
            mirror = lane_dir / page_src.name
            marker = lane_dir / ".haipipe-page-export"
            if index.is_file():
                has_material = True
                if index not in files:
                    files.append(index)
            if mirror.is_file():
                has_material = True
                files.append(mirror)
                if _sha256(mirror) != source_hash:
                    artifact_rows.append(_check_row("content mirror", "stale", "web Markdown differs from Page source"))
                    hard_failure = True
                else:
                    artifact_rows.append(_check_row("content mirror", "pass", "web Markdown matches Page source"))
            elif index.is_file():
                artifact_rows.append(_check_row("content mirror", "stale", "missing: delivery/web/%s" % page_src.name))
                hard_failure = True
            marker_hash = _marker_source_hash(marker)
            if marker.is_file() and marker_hash:
                if marker_hash != source_hash:
                    artifact_rows.append(_check_row("export marker", "stale", "marker points to an older Page source"))
                    hard_failure = True
                else:
                    artifact_rows.append(_check_row("export marker", "pass", "source fingerprint recorded"))
            elif index.is_file():
                artifact_rows.append(_check_row("export marker", "unverified", "legacy marker has no source fingerprint"))
                hash_unverified = True

        source_state = "pass"
        source_detail = "current Page source"
        if data is None and has_material:
            source_state = "unverified"
            source_detail = "no build manifest"
            hash_unverified = True
        elif data is not None:
            if not _source_path_matches(base, page_src, manifest_source_path):
                source_state = "stale"
                source_detail = "manifest names %s, current source is %s" % (manifest_source_path, actual_source)
                hard_failure = True
            elif manifest_source_hash is None:
                source_state = "unverified"
                source_detail = "manifest has no source fingerprint"
                hash_unverified = True
            elif manifest_source_hash.lower() != source_hash:
                source_state = "stale"
                source_detail = "manifest fingerprint differs from current source"
                hard_failure = True
        artifact_rows.insert(0, _check_row("source fingerprint", source_state, source_detail))

        if files:
            old = [p for p in files if p.exists() and p.stat().st_mtime < source_mtime]
            if old:
                artifact_rows.append(_check_row("freshness", "stale", "%d artifact(s) predate the Page source" % len(old)))
                hard_failure = True
            else:
                artifact_rows.append(_check_row("freshness", "pass", "artifacts are at least as new as the Page source"))
        elif has_material:
            artifact_rows.append(_check_row("freshness", "unverified", "no inspectable artifact files"))
            hash_unverified = True

        if not has_material:
            state = "not-built"
        elif hard_failure:
            state = "stale"
        elif hash_unverified:
            state = "unverified"
        else:
            state = "pass"
        lanes.append({
            "lane": lane, "icon": icon, "label": label, "state": state,
            "manifest": manifest_path.relative_to(base).as_posix() if manifest_path else None,
            "rows": artifact_rows,
        })

    counts = {state: sum(1 for lane in lanes if lane["state"] == state)
              for state in ("pass", "stale", "unverified", "not-built")}
    overall = "stale" if counts["stale"] else "unverified" if counts["unverified"] else "pass"
    return {
        "schema": "page-delivery-consistency/v1",
        "source": {"path": actual_source, "sha256": source_hash, "mtime": source_mtime},
        "overall": overall,
        "counts": counts,
        "lanes": lanes,
    }


def render_workspace(page_src: pathlib.Path, path_q: str, file_q: str) -> str:
    """Render the internal read-only Delivery Workspace check."""
    receipt = check_delivery(page_src)
    state = receipt["overall"]
    state_icon = {"pass": "✅", "stale": "⚠️", "unverified": "❓"}[state]
    counts = receipt["counts"]
    summary = "%s %d current · %d stale · %d unverified · %d not built" % (
        state_icon, counts["pass"], counts["stale"], counts["unverified"], counts["not-built"])
    cards = []
    for lane in receipt["lanes"]:
        icon = {"pass": "✅", "stale": "⚠️", "unverified": "❓", "not-built": "⬜"}[lane["state"]]
        rows = "".join(
            "<li><b>%s</b> <span class=%s>%s</span><span class=mut>%s</span></li>" %
            (html.escape(row["label"]), row["state"], row["state"], html.escape(row["detail"]))
            for row in lane["rows"])
        manifest = (" · manifest: <code>%s</code>" % html.escape(lane["manifest"])
                    if lane["manifest"] else " · no manifest")
        cards.append("<section class=card><h2>%s %s <span class=state-%s>%s</span></h2>"
                     "<div class=mut>%s</div><ul>%s</ul></section>" %
                     (lane["icon"], html.escape(lane["label"]), lane["state"],
                      lane["state"], manifest, rows or "<li>no delivery files</li>"))
    source = receipt["source"]
    return f"""<!doctype html><meta charset=utf-8>
<title>📤 Delivery Workspace · {html.escape(page_src.stem)}</title>
<style>
:root{{--bg:#fff;--fg:#1c1d1f;--mut:#71727a;--line:#e4e4e7;--card:#f7f7f8;--acc:#3b6ea5;--bad:#a43d35;--warn:#996b00;--ok:#24733d}}
@media(prefers-color-scheme:dark){{--bg:#161719;--fg:#e8e8e6;--mut:#9a9a97;--line:#2c2e33;--card:#1d1f23;--acc:#7aa7d8;--bad:#f08b80;--warn:#e4bd62;--ok:#8bd49a}}
body{{margin:0;background:var(--bg);color:var(--fg);font:14px/1.55 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}
header{{padding:14px 18px 8px;border-bottom:1px solid var(--line)}}
h1{{font-size:18px;margin:0 0 3px}} h2{{font-size:14px;margin:0 0 4px}}
.mut{{color:var(--mut);font-size:12px}} code{{font:11.5px ui-monospace,Menlo,monospace}}
.source{{margin:12px 18px;padding:10px 12px;border:1px solid var(--line);border-radius:8px;background:var(--card)}}
.source div{{margin:2px 0}} .toolbar{{float:right;border:1px solid var(--line);background:var(--bg);color:var(--fg);border-radius:6px;padding:3px 8px;cursor:pointer}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px;margin:12px 18px}}
.card{{border:1px solid var(--line);border-radius:8px;padding:10px 12px;background:var(--card)}}
.card ul{{padding-left:18px;margin:7px 0 0}} .card li{{margin:2px 0}} .card li b{{display:inline-block;min-width:112px}}
.pass,.state-pass{{color:var(--ok)}} .stale,.state-stale{{color:var(--bad)}} .unverified,.state-unverified{{color:var(--warn)}} .not-built,.state-not-built{{color:var(--mut)}}
.state-pass,.state-stale,.state-unverified,.state-not-built{{font-size:12px;font-weight:600}}
</style>
<header><button class=toolbar onclick="location.reload()">Refresh check</button>
<h1>📤 Delivery Workspace · {html.escape(page_src.stem)}</h1>
<div class=mut>Read-only consistency projection · Page source is authoritative · this view never rebuilds or edits delivery files</div></header>
<div class=source><div><b>Authority</b> <code>{html.escape(source["path"])}</code></div>
<div><b>SHA-256</b> <code>{source["sha256"]}</code></div><div><b>Result</b> {html.escape(summary)}</div></div>
<main class=grid>{''.join(cards)}</main>
"""


def _stamp(p: pathlib.Path) -> str:
    t = datetime.datetime.fromtimestamp(p.stat().st_mtime)
    return t.strftime("%y%m%d %H:%M")


def render(page_src: pathlib.Path, path_q: str, file_q: str, *,
           interactive: bool = True, asset_base: str | None = None) -> str:
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
        row("📜", "LaTeX", f"delivery/latex/{stem}.pdf",
            "the delivery writer has not built it"),
        row("📝", "Word", f"delivery/word/{stem}.docx",
            "the delivery writer has not built it"),
        row("🎞", "Slides", f"delivery/slide/{stem}-deck.html",
            "authored on the 🎞 tab's ✨ bar, never auto-built here"),
        "<div class=row><b>📱 Render</b><code>delivery/render/</code>"
        "<span class=mut>%s</span></div>"
        % ("%d file(s) on disk · Folder-native writer live" % n_render if n_render
           else "empty · run the Folder-native render verb"),
    ])
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
<header><h1>📤 Delivery · {html.escape(stem)}</h1>
<div class=mut>one surface, four lanes · what leaves the page · builders and
storage stay with delivery/latex/ · delivery/word/ · delivery/slide/ · delivery/render/</div></header>
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
    if (CTX.asset_base !== null) return CTX.asset_base + '/' + plugin + '/' + name;
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
        body: JSON.stringify({{path: CTX.path, file: CTX.file}})
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
        got = self.target({"path": path_q, "file": file_q})
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
