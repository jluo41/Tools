"""📂 Folder · the page-folder's own status, the tab rail's FIRST surface.

WHAT THIS ANSWERS (JL 260815: "a first item in the plugin to show the content
of the page-folder status"): the tab rail shows the surfaces someone built;
nothing showed what the page's folder actually HOLDS. So a reader could not
tell "no deck" from "deck built, tab unopened", and nothing said the compiled
latex/ now predates the .md it was compiled from.

WHY A LIVE GET AND NOT A WRITTEN VIEW: every other plugin's view page is
derived bytes beside derived bytes, and that is right for them — the artifact
IS a file. A status has no artifact: written to disk it starts aging the
moment it lands, and a stale page ABOUT staleness would be the board's best
joke at its own expense. So `GET /_board/folderstat` renders from the live
tree on every open, and the POST twin exists only so the shell's
`tab: {url, write}` contract holds.

STALENESS IS THE POINT, and it is claimed narrowly: only a DERIVED plugin
(latex, word, bibex, slide, display) can be stale, and it is stale when its
newest file predates the page's .md. Source material (draw, chat, meeting,
skill) is often older than the prose and that is healthy, so it gets an age,
never a warning.
"""
import html
import time
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ICON = {"draw": "🖌", "slide": "🎬", "chat": "💬", "latex": "📜",
        "word": "📝", "bibex": "📚", "display": "🖼", "skill": "⚙️",
        "meeting": "🗣", "probe": "🧪", "_runs": "🧾", "_fixture": "📦"}
DERIVED = {"latex", "word", "bibex", "slide", "display"}

_PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>
:root{{--bg:#fbfbf9;--fg:#1c1c1c;--mut:#7c7c78;--line:#e4e4df;--card:#fff;
 --warn:#b3541e;--ok:#3a7d44}}
@media(prefers-color-scheme:dark){{:root{{--bg:#161719;--fg:#e8e8e6;--mut:#9a9a97;
 --line:#2c2e33;--card:#1d1f23;--warn:#e0955a;--ok:#7dbb87}}}}
body{{margin:0;padding:16px;background:var(--bg);color:var(--fg);
 font:14px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}
h1{{font-size:15px;margin:0 0 2px}} .mut{{color:var(--mut);font-size:12px}}
table{{border-collapse:collapse;width:100%;margin-top:10px}}
td,th{{padding:6px 8px;border-bottom:1px solid var(--line);text-align:left;
 font-size:13px;vertical-align:top}}
th{{color:var(--mut);font-weight:500;font-size:11px;text-transform:uppercase}}
.stale{{color:var(--warn);font-weight:600}} .fresh{{color:var(--ok)}}
.absent{{color:var(--mut)}} code{{font:12px ui-monospace,Menlo,monospace}}
</style></head><body>
<h1>📂 {title}</h1>
<div class="mut">the page's own folder · rendered live, never stored ·
source .md edited {md_age}</div>
<table><tr><th></th><th>plugin</th><th>holds</th><th>newest</th><th>state</th></tr>
{rows}</table>
<div class="mut" style="margin-top:10px">{absent}</div>
</body></html>"""


def _age(ts, now):
    if not ts:
        return "—"
    d = max(0, int(now - ts))
    for unit, size in (("d", 86400), ("h", 3600), ("m", 60)):
        if d >= size:
            return f"{d // size}{unit} ago"
    return f"{d}s ago"


def folder_status(page_src):
    """-> (title, md_mtime, [ {name, icon, files, bytes, newest, derived,
    stale} ]). Pure filesystem walk, no engine imports, so serve stays thin."""
    page_dir = page_src.parent
    md_mtime = page_src.stat().st_mtime
    rows = []
    for d in sorted(page_dir.iterdir()):
        if not d.is_dir():
            continue
        files = [f for f in d.rglob("*") if f.is_file()]
        newest = max((f.stat().st_mtime for f in files), default=0)
        rows.append({
            "name": d.name,
            "icon": ICON.get(d.name.lstrip("_"), ICON.get(d.name, "📁")),
            "files": len(files),
            "bytes": sum(f.stat().st_size for f in files),
            "newest": newest,
            "derived": d.name in DERIVED,
            "stale": d.name in DERIVED and bool(files) and newest < md_mtime,
        })
    return page_dir.name, md_mtime, rows


def _fmt_bytes(n):
    for unit in ("B", "KB", "MB"):
        if n < 1024:
            return f"{n:.0f}{unit}"
        n /= 1024
    return f"{n:.1f}GB"


class FolderStatMixin:

    # ---- GET/HEAD /_board/folderstat?path=…&file=… ---------------------
    def folderstat_view(self, head_only=False):
        q = parse_qs(urlparse(self.path).query)
        p = {"path": (q.get("path") or [""])[0], "file": (q.get("file") or [""])[0]}
        got = self.target(p)
        if got[0] is None:
            body = f"<h1>📂 folder status</h1><p>{html.escape(got[1])}</p>".encode()
            return self._folderstat_send(body, 404, head_only)
        f, board = got
        page_src = Path(board) / f
        now = time.time()
        title, md_mtime, rows = folder_status(page_src)
        present, absent = [], []
        for r in rows:
            state = ('<span class="stale">⚠️ STALE · older than the .md</span>'
                     if r["stale"] else
                     ('<span class="fresh">✅ fresh</span>' if r["derived"]
                      else '<span class="mut">source material</span>'))
            present.append(
                "<tr><td>%s</td><td><code>%s/</code></td><td>%d file%s · %s</td>"
                "<td>%s</td><td>%s</td></tr>" % (
                    r["icon"], html.escape(r["name"]), r["files"],
                    "s"[:r["files"] != 1], _fmt_bytes(r["bytes"]),
                    _age(r["newest"], now), state))
        known = {r["name"] for r in rows}
        gaps = [n for n in ("draw", "slide", "chat", "latex", "word", "bibex",
                            "display", "skill", "meeting")
                if n not in known]
        if gaps:
            absent.append("⬜ not present: " + " · ".join(gaps))
        page = _PAGE.format(title=html.escape(title),
                            md_age=_age(md_mtime, now),
                            rows="".join(present) or
                                 "<tr><td colspan=5 class=mut>no plugin folders yet</td></tr>",
                            absent=" ".join(absent))
        return self._folderstat_send(page.encode("utf-8"), 200, head_only)

    def _folderstat_send(self, body, code, head_only):
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    # ---- POST /_board/folderstat — the shell's write() twin -----------
    def plug_folderstat(self, p):
        """{path, file} -> {ok, url}. Nothing is written: the GET renders
        live. This exists so the tab spec's write() has something to call."""
        got = self.target(p)
        if got[0] is None:
            return None, got[1]
        from urllib.parse import quote
        url = ("/_board/folderstat?path=%s&file=%s"
               % (quote(p.get("path") or ""), quote(p.get("file") or "")))
        return {"url": url}, None
