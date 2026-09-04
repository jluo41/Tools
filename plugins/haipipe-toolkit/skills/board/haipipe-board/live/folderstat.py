"""📂 Folder · the page-folder's own live status surface.

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
import json
import os
import time
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse

ICON = {"draw": "🖌", "slide": "🎬", "chat": "💬", "latex": "📜",
        "word": "📝", "bibex": "📚", "display": "🖼", "skill": "⚙️",
        "meeting": "🗣", "_runs": "🧾", "_fixture": "📦",
        "outline": "🧭", "workflow": "🪜", "pagex": "🔗", "materials": "📥",
        "evidence": "🧾", "delivery": "📤", "studio": "🎨", "task": "🗂",
        "render": "📱", "design": "🎨", "scripts": "📜", "runs": "🎫",
        "results": "📦", "outline/evidence/supporting-runs": "🧷"}

# The two-part unit grammar (haipipe-plugin §🗂/🔌, JL 260831): which category
# owns each lane, so the table can say it and the gaps line can speak the
# grammar instead of the pre-260831 flat roster. A flat lane name counts for
# its category until the sweep folds it in (a stub keeps it resolving after).
# Evidence is not a top-level category: it is the material workspace owned by
# Outline.  The old flat lanes remain named here only so Folder can explain
# their migration destination.
CATEGORY = {"bibex": "outline/evidence", "display": "outline/evidence",
            "pagex": "outline/evidence", "materials": "outline/evidence",
            "skill": "outline",
            "latex": "delivery", "word": "delivery", "slide": "delivery",
            "render": "delivery",
            "chat": "studio", "draw": "studio",
            "scripts": "code", "runs": "code", "results": "code"}
DERIVED = {"latex", "word", "bibex", "slide", "display", "render"}
DERIVED_LABELS = {"outline/evidence/supporting-runs"}
# STALE rows a click may cure IN PLACE (JL 260816: "could we update them
# along the time?"): only the MECHANICAL writers — one POST, seconds, no
# judgment. display joined the same day (JL: "I want to add the rebuild
# button"): its POST recompiles each unit's DERIVED preview.tex ▶ pdf and
# touches no intake, recipe, or accepted: tick. slide stays a pointer —
# AUTHORED by claude -p (minutes, money), never a button reflex.
MECHANICAL = {"latex": "/_board/latex", "word": "/_board/word",
              "bibex": "/_board/bibex", "display": "/_board/display"}
POINTER = {"slide": "✨ regenerate in the 🎞 Slides tab"}

_PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>
:root{{--bg:#ffffff;--fg:#1c1c1c;--mut:#7c7c78;--line:#e4e4e7;--card:#fff;
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
tr.plug{{cursor:pointer}} tr.plug:hover td{{background:var(--card)}}
.caret{{display:inline-block;width:1em;color:var(--mut);
 transition:transform .12s}} tr.open .caret{{transform:rotate(90deg)}}
tr.files{{display:none}} tr.files.show{{display:table-row}}
tr.files>td{{padding:6px 8px 12px 30px;border-bottom:1px solid var(--line)}}
.f{{display:flex;gap:10px;padding:3px 0;align-items:baseline;
 font:13px/1.6 ui-monospace,Menlo,monospace}}
.f a{{color:var(--fg);text-decoration:none;flex:1;min-width:0;
 overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.f a:hover{{text-decoration:underline}}
.f .mut{{flex:none;font-size:12px;font-variant-numeric:tabular-nums}}
.f.dir{{color:var(--mut);margin-top:5px;font-weight:600}}
.f.dir .mut{{font-weight:400}}
.lnk{{color:var(--mut);font-size:12px;flex:none;white-space:nowrap;
 overflow:hidden;text-overflow:ellipsis;max-width:44%}}
.rb{{margin-left:8px;padding:1px 8px;font:11px -apple-system,sans-serif;
 color:var(--warn);background:none;border:1px solid var(--warn);
 border-radius:9px;cursor:pointer}}
.rb:hover{{background:var(--warn);color:var(--card)}}
.rb[disabled]{{opacity:.5;cursor:default}}
.rball{{float:right;margin-top:2px;padding:4px 12px;cursor:pointer;
 font:500 12px -apple-system,sans-serif;color:var(--fg);
 background:var(--card);border:1px solid var(--line);border-radius:10px}}
.rball:hover{{border-color:var(--warn);color:var(--warn)}}
.rball[disabled]{{opacity:.5;cursor:default}}
</style></head><body>
{allbtn}<h1>📂 {title}</h1>
<div class="mut">the page's own folder · rendered live, never stored ·
source .md edited {md_age}</div>
<table><tr><th></th><th>path</th><th>holds</th><th>newest</th><th>state</th></tr>
{rows}</table>
<div class="mut" style="margin-top:10px">{absent}</div>
<script>
var TARGET={target};
document.querySelectorAll('tr.plug').forEach(function(tr){{
  tr.addEventListener('click',function(){{
    tr.classList.toggle('open');
    var d=tr.nextElementSibling;
    if(d&&d.classList.contains('files'))d.classList.toggle('show');
  }});
}});
/* ♻ cure a MECHANICAL stale row in place: the same POST the tab's writer
   uses, then re-render this live view. The click stays on the button. */
function fire(route){{
  return fetch(route,{{method:'POST',
    headers:{{'Content-Type':'application/json'}},
    body:JSON.stringify(TARGET)}}).then(function(r){{return r.json();}});
}}
/* 🔄 the header pill, the Word/LaTeX views' own affordance (JL 260816:
   "add the button like rebuild like this"): one click walks every stale
   MECHANICAL row in turn, then re-renders. Sequential on purpose — the
   writers share the page's folder and xelatex is not a thing to race. */
var all=document.querySelector('.rball');
if(all)all.addEventListener('click',function(){{
  var routes=all.dataset.routes.split(',').filter(Boolean);
  all.disabled=true;
  var i=0;
  (function step(){{
    if(i>=routes.length){{location.reload();return;}}
    all.textContent='⏳ '+(i+1)+'/'+routes.length;
    fire(routes[i]).then(function(j){{
      if(!j.ok){{all.textContent='✋ '+(j.err||'refused');
                 all.disabled=false;return;}}
      i++;step();
    }}).catch(function(){{all.textContent='✋ server?';all.disabled=false;}});
  }})();
}});
document.querySelectorAll('.rb').forEach(function(b){{
  b.addEventListener('click',function(ev){{
    ev.stopPropagation();
    b.disabled=true; b.textContent='⏳';
    fetch(b.dataset.route,{{method:'POST',
      headers:{{'Content-Type':'application/json'}},
      body:JSON.stringify(TARGET)}})
      .then(function(r){{return r.json();}})
      .then(function(j){{
        if(j.ok){{location.reload();return;}}
        b.disabled=false; b.textContent='✋ '+(j.err||'refused');
      }})
      .catch(function(){{b.disabled=false;b.textContent='✋ server?';}});
  }});
}});
</script>
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
    stubs = []

    def row_for(d, label, recursive=True):
        candidates = d.rglob("*") if recursive else d.iterdir()
        files = sorted((f for f in candidates if f.is_file()),
                       key=lambda f: str(f.relative_to(d)))
        newest = max((f.stat().st_mtime for f in files), default=0)
        return {
            "name": d.name,
            "label": label,
            "icon": ICON.get(label, ICON.get(d.name.lstrip("_"), ICON.get(d.name, "📁"))),
            "files": len(files),
            "bytes": sum(f.stat().st_size for f in files),
            "newest": newest,
            "derived": d.name in DERIVED or label in DERIVED_LABELS,
            "stale": (d.name in DERIVED or label in DERIVED_LABELS) and bool(files) and newest < md_mtime,
            "list": [(str(f.relative_to(d)), f) for f in files],
        }

    for d in sorted(page_dir.iterdir()):
        if not d.is_dir():
            continue
        # a migration STUB (flat name -> its category home) is a compatibility
        # NAME, not a folder: listing it would double-count the lane and keep
        # the flat-lanes callout firing on already-migrated pages
        if d.is_symlink():
            stubs.append(d.name)
            continue
        # Category folders show their lanes as first-class rows. Outline keeps
        # one direct-files row for its authored process records, while each
        # evidence lane gets its own explicit path. This prevents the plan's
        # eight records from being visually merged with bibex/display/PageX
        # material and avoids counting the same files twice.
        if d.name == "outline":
            rows.append(row_for(d, "outline", recursive=False))
            skill = d / "skill"
            if skill.is_dir() and not skill.is_symlink():
                rows.append(row_for(skill, "outline/skill"))
            evidence = d / "evidence"
            if evidence.is_dir():
                for lane in sorted(evidence.iterdir()):
                    if lane.is_dir() and not lane.is_symlink():
                        rows.append(row_for(
                            lane, "outline/evidence/%s" % lane.name))
            continue
        if d.name in ("delivery", "studio"):
            for lane in sorted(d.iterdir()):
                if lane.is_dir() and not lane.is_symlink():
                    rows.append(row_for(lane, f"{d.name}/{lane.name}"))
            continue
        rows.append(row_for(d, d.name))
    rows.sort(key=lambda r: r["label"])
    return page_dir.name, md_mtime, rows, stubs


def _as_tree(pairs):
    """[(rel, path)] -> [(depth, kind, label, payload)] in reading order.

    Files a level OWNS come before the folders under it, so the eye meets the
    thing itself before its parts; a folder carries its own file count, which
    is what makes a collapsed branch still worth reading."""
    tree = {}
    for rel, f in pairs:
        *dirs, name = rel.split("/")
        node = tree
        for seg in dirs:
            node = node.setdefault(seg, {})
        node.setdefault("\0", []).append((name, f))

    def walk(node, depth):
        out = []
        for name, f in sorted(node.get("\0", [])):
            out.append((depth, "file", name, f))
        for seg in sorted(k for k in node if k != "\0"):
            sub = walk(node[seg], depth + 1)
            n = sum(1 for r in sub if r[1] == "file")
            out.append((depth, "dir", seg, "%d file%s" % (n, "s"[:n != 1])))
            out.extend(sub)
        return out

    return walk(tree, 0)


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
        title, md_mtime, rows, stubs = folder_status(page_src)
        root = self.root.resolve()
        present, absent = [], []
        for r in rows:
            if r["stale"]:
                state = '<span class="stale">⚠️ STALE · older than the .md</span>'
                if r["name"] in MECHANICAL:
                    state += ('<button class=rb type=button data-route="%s">'
                              '♻ rebuild</button>' % MECHANICAL[r["name"]])
                elif r["name"] in POINTER:
                    state += ' <span class="mut">· %s</span>' % POINTER[r["name"]]
            elif r["derived"]:
                state = '<span class="fresh">✅ fresh</span>'
            else:
                state = '<span class="mut">source material</span>'
            # a nested lane already SAYS its category in the path; only a
            # flat, pre-sweep lane still needs the chip naming where it goes
            cat = CATEGORY.get(r["name"].lstrip("_"), "")
            flat_here = cat and r["label"] == r["name"]
            cat_chip = (' <span class=mut title="this lane\'s category folder'
                        ' in the two-part unit grammar">· %s (flat)</span>' % cat
                        if flat_here else "")
            present.append(
                "<tr class=plug><td><span class=caret>▸</span>%s</td>"
                "<td><code>%s/</code>%s</td><td>%d file%s · %s</td>"
                "<td>%s</td><td>%s</td></tr>" % (
                    r["icon"], html.escape(r["label"]), cat_chip, r["files"],
                    "s"[:r["files"] != 1], _fmt_bytes(r["bytes"]),
                    _age(r["newest"], now), state))
            # A FOLDER IS A TREE, not a sorted list of path strings (JL
            # 260816: "是不是应该加一个 folder structure … 这个排版不是非常
            # 按照我们的思路来排的"). Flat, `pagex/` read as six unrelated
            # rows with its own store and view wedged alphabetically between
            # four borrowed pages; nested, the same six say what the folder IS
            # — two files it owns, then one folder per page it borrows from.
            items = []
            for depth, kind, label, f in _as_tree(r["list"]):
                pad = "style='padding-left:%dpx'" % (depth * 18)
                if kind == "dir":
                    items.append("<div class='f dir' %s>📁 %s<span class=mut>"
                                 "%s</span></div>"
                                 % (pad, html.escape(label + "/"), f))
                    continue
                try:
                    href = "/" + quote(str(f.resolve().relative_to(root)))
                except ValueError:
                    continue
                rel = label
                # A SYMLINK MUST NOT READ AS A COPY (JL 260816: "are they
                # copied or are they the symlink?"). The row reports the
                # RESOLVED file, so a borrowed 13KB page md looked exactly
                # like 13KB of duplicated bytes; pagex's whole claim is that
                # it copies nothing, and the one surface that shows the folder
                # was quietly denying it.
                #
                # The first fix said so with the whole repo path inline, which
                # crushed the filename out of the flex row and wrapped over
                # three lines ("very ugly", same day). A link needs ONE mark
                # and a SHORT target: the source page plus the file, which is
                # what a person is actually identifying it by.
                mark = ""
                if f.is_symlink():
                    try:
                        t = f.resolve().relative_to(root)
                        short = "/".join(t.parts[-2:])
                    except ValueError:
                        short = os.readlink(f).split("/")[-1]
                    # pagex mints links whose place MIRRORS the source, so the
                    # short target usually repeats the row's own name. Saying
                    # it twice is the noise the first fix was trying to cure;
                    # the bare mark carries the whole point, and the full
                    # target lives on hover.
                    mark = ('<span class=lnk title="%s">🔗%s</span>'
                            % (html.escape(str(f.resolve())),
                               "" if short == rel else " " + html.escape(short)))
                items.append(
                    '<div class=f %s><a href="%s" target="_blank" '
                    'rel="noopener">%s</a>%s<span class=mut>%s · %s</span>'
                    '</div>' % (
                        pad, href, html.escape(rel), mark,
                        _fmt_bytes(f.stat().st_size),
                        _age(f.stat().st_mtime, now)))
            present.append(
                "<tr class=files><td colspan=5>%s</td></tr>"
                % ("".join(items) or '<span class="mut f">empty</span>'))
        known = {r["name"] for r in rows}
        # The gaps line speaks the two-part grammar (260831), not lane names:
        # a category counts as present when its folder exists OR any of its
        # flat pre-sweep lanes does.
        have_cat = {c for c in ("delivery", "studio") if c in known}
        have_cat |= {c for n, c in CATEGORY.items() if n in known}
        gaps = [n for n in ("outline", "workflow") if n not in known]
        gaps += [c + "/" for c in ("delivery", "studio")
                 if c not in have_cat]
        if gaps:
            absent.append("⬜ not present: " + " · ".join(gaps))
        flat = sorted(r["name"] for r in rows
                      if r["name"] in CATEGORY and r["label"] == r["name"])
        if flat:
            absent.append("📦 pre-migration flat lanes: " + " · ".join(flat)
                          + " — the sweep folds them under their category")
        if stubs:
            absent.append("🔗 %d compatibility stub%s (flat name → category), "
                          "dropped when the engine de-symlinks"
                          % (len(stubs), "s"[:len(stubs) != 1]))
        cures = [MECHANICAL[r["name"]] for r in rows
                 if r["stale"] and r["name"] in MECHANICAL]
        allbtn = ('<button class=rball type=button data-routes="%s">'
                  '🔄 rebuild stale (%d)</button>' % (",".join(cures), len(cures))
                  if cures else "")
        page = _PAGE.format(title=html.escape(title),
                            allbtn=allbtn,
                            target=json.dumps({"path": p["path"],
                                               "file": p["file"]}),
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
