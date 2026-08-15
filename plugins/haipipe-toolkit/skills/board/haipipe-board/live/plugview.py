"""🖼🚪 Plugview · the EVIDENCE plugins' read-only surfaces: display/ and probe/.

THE DIVISION OF LABOUR, the same one export.py drew for latex/word/bibex:

  the writers (renderer skills · the probe orchestrator)   HOW material is made
  this file                                                WHERE the tab looks, read-only

Nothing here writes material. A display unit is written by its renderer and
accepted by a person (QPf5); a probe card is raised by its consumer and bound
by the collector (QPf9). This surface SHOWS both and writes neither, which is
each contract's own rule: "the pane shows everything · writes NOTHING".

THE VIEW IS DERIVED, like every export view: `<plugin>/<stem>-view.html` is
regenerated on each open and never hand-edited. An EMPTY plugin renders the
contract's ghost scaffold instead of a blank, so an empty tab teaches what
belongs there (JL 260815).
"""
import json
import re
from pathlib import Path

_PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>
:root{{--bg:#fbfbf9;--fg:#1c1c1c;--mut:#7c7c78;--line:#e4e4df;--card:#fff}}
@media(prefers-color-scheme:dark){{:root{{--bg:#161719;--fg:#e8e8e6;--mut:#9a9a97;
 --line:#2c2e33;--card:#1d1f23}}}}
body{{margin:0;padding:18px;background:var(--bg);color:var(--fg);
 font:14px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}
h1{{font-size:16px;margin:0 0 4px}} .mut{{color:var(--mut);font-size:12px}}
a{{color:#1f5aa8}} pre{{background:var(--card);border:1px solid var(--line);
 border-radius:8px;padding:12px;overflow:auto;font:12px/1.45 ui-monospace,Menlo,monospace;
 white-space:pre-wrap}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:8px;
 padding:10px 12px;margin:0 0 10px}}
.card b{{font:600 13px/1.3 ui-monospace,Menlo,monospace}}
.ghost{{opacity:.55;border-style:dashed}}
.badge{{font-size:13px;margin-right:6px}}
object.pdf{{width:100%;aspect-ratio:4/3;border:1px solid var(--line);border-radius:8px}}
.strip{{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:14px;
 scroll-behavior:smooth;padding:2px}}
.strip>.card{{flex:0 0 100%;scroll-snap-align:start;margin:0;box-sizing:border-box}}
.nav{{display:flex;align-items:center;gap:8px;float:right}}
.nav button{{cursor:pointer;border:1px solid var(--line);background:var(--card);
 color:var(--fg);border-radius:6px;padding:3px 10px;font:600 13px -apple-system,sans-serif}}
.nav .pos{{color:var(--mut);font-size:12px;min-width:38px;text-align:center}}
.chips{{display:flex;gap:6px;flex-wrap:wrap;margin:0 0 10px}}
.chip{{font:500 12px ui-monospace,Menlo,monospace;border:1px solid var(--line);
 border-radius:999px;padding:3px 10px;text-decoration:none;color:var(--fg);
 background:var(--card)}}
.chip.on{{border-color:#3e5c84;color:#3e5c84;font-weight:700}}
</style></head><body>{body}</body></html>
"""

_STRIP_NAV = """<script>
(function () {
  var s = document.getElementById('strip');
  if (!s) return;
  var cards = s.children.length;
  var pos = document.getElementById('pos');
  function at() { return Math.round(s.scrollLeft / s.clientWidth); }
  function paint() { pos.textContent = (at() + 1) + ' / ' + cards; }
  function go(d) { s.scrollTo({left: (at() + d) * s.clientWidth, behavior: 'smooth'}); }
  document.getElementById('prev').onclick = function () { go(-1); };
  document.getElementById('next').onclick = function () { go(1); };
  var chips = [].slice.call(document.querySelectorAll('.chip'));
  function paintChips() {
    var i = at();
    chips.forEach(function (c, k) { c.className = 'chip' + (k === i ? ' on' : ''); });
  }
  s.addEventListener('scroll', function () {
    requestAnimationFrame(function () { paint(); paintChips(); });
  });
  /* A CITATION or a chip lands here as #<unit-id>: shift the deck to that
     unit, so a sentence citing a display arrives at the render it cites. */
  function toHash() {
    var h = decodeURIComponent((location.hash || '').slice(1));
    var el = h && document.getElementById(h);
    if (el && el.parentNode === s) s.scrollLeft = el.offsetLeft - s.offsetLeft;
  }
  window.addEventListener('hashchange', toHash);
  toHash();
  paint(); paintChips();
})();
</script>"""

_GHOST_DISPLAY = """<div class="card ghost"><b>&lt;PageID&gt;-Display1-&lt;slug&gt;/</b>
<pre>README.md      claim · kind · caption-job · fragility · status
intake/        🧑 manifest.yaml + small approved extracts
recipe/        🎨 renderer-owned script, spec, receipts
float.tex · preview.tex ▶ preview.pdf   ⚙️ derived
assets/        ⚙️ the WINNING render
candidates/ · versions/</pre>
<div class="mut">nothing here yet · this is the unit shape the contract expects (QPf5 §1)</div></div>"""

_GHOST_PROBE = """<div class="card ghost"><b>PP01-&lt;slug&gt;/card.md</b>
<pre>question    in the page's own words, stake included
state:      raised → working → bound
binding:    → &lt;task-folder&gt;/QA/&lt;n&gt;-&lt;slug&gt;.md</pre>
<div class="mut">nothing asked yet · this is the card shape the contract expects (QPf9 §1)</div></div>"""

_STATE_BADGE = {"raised": "⬜", "working": "🔨", "bound": "✅", "answered": "✅"}


def _esc(s):
    import html
    return html.escape(str(s or ""), quote=False)


def _readme_rows(readme):
    """`- key: value` bullets from a unit README, in file order."""
    rows = []
    if readme.is_file():
        for ln in readme.read_text(errors="replace").splitlines():
            m = re.match(r"^\s*-\s+([\w-]+):\s*(.+)$", ln)
            if m:
                rows.append((m.group(1), m.group(2)))
    return rows


def _tree(root, keep=60):
    """An indented folder tree (JL 260815: "I want it to be like the folder
    structure"), derived halves marked ⚙️; capped, and the cap is said."""
    lines = []

    def walk(d, prefix):
        entries = sorted(
            (e for e in d.iterdir()
             if not e.name.startswith(".") and not e.name.endswith("-view.html")),
            key=lambda e: (e.is_file(), e.name))
        for i, e in enumerate(entries):
            if len(lines) >= keep:
                return
            last = i == len(entries) - 1
            rel = e.relative_to(root).as_posix() + ("/" if e.is_dir() else "")
            mark = "⚙️ " if re.match(
                r"(assets|candidates|versions)(/|$)|preview\.pdf$", rel) else ""
            lines.append(prefix + ("└── " if last else "├── ")
                         + mark + e.name + ("/" if e.is_dir() else ""))
            if e.is_dir():
                walk(e, prefix + ("    " if last else "│   "))

    walk(root, "")
    if len(lines) >= keep:
        lines.append("… (capped at %d entries)" % keep)
    return "\n".join(lines)


class PlugViewMixin:

    # ---- POST /_board/display ----------------------------------------
    def plug_display(self, p):
        page_src, out_dir, _, err = self._export_target(p, "display")
        if err:
            return None, err
        cards = []
        for unit in sorted(d for d in out_dir.iterdir() if d.is_dir()):
            rows = _readme_rows(unit / "README.md")
            body = "".join("<div class='mut'><b style='color:var(--fg)'>%s</b>: %s</div>"
                           % (_esc(k), _esc(v)) for k, v in rows)
            pdf = unit / "preview.pdf"
            if pdf.is_file():
                href = _esc(unit.name + "/preview.pdf")
                body += ("<object class='pdf' data='%s' type='application/pdf'>"
                         "<a href='%s'>preview.pdf</a></object>" % (href, href))
            else:
                body += ("<div class='card ghost' style='margin:8px 0'>"
                         "🕳 no render yet · this unit has an intake and a recipe "
                         "but ② RENDER has not run; the figure appears here when "
                         "preview.pdf exists</div>")
            body += "<pre>%s</pre>" % _esc(_tree(unit))
            cards.append("<div class='card' id='%s'><b>%s</b>%s</div>"
                         % (_esc(unit.name), _esc(unit.name), body))
        # The NAME LIST: every unit as a chip, clicking one shifts the deck
        # there (JL 260815: "where is the name list for all the displays?").
        stem = out_dir.parent.name
        units = [d.name for d in sorted(out_dir.iterdir()) if d.is_dir()]
        chips = ""
        if len(units) > 1:
            chips = "<div class='chips'>%s</div>" % "".join(
                "<a class='chip' href='#%s'>%s</a>"
                % (_esc(u), _esc(u[len(stem) + 1:] if u.startswith(stem + "-") else u))
                for u in units)
        return self._plug_page(p, out_dir, "display", "🖼 Display",
                               cards or [_GHOST_DISPLAY],
                               "read-only · renderers write recipe/ and assets/; "
                               "a person rules intake/ and ticks accepted: (QPf5 §3)",
                               strip=True, head=chips)

    # ---- POST /_board/probe ------------------------------------------
    def plug_probe(self, p):
        page_src, out_dir, _, err = self._export_target(p, "probe")
        if err:
            return None, err
        cards = []
        srcs = sorted(d / "card.md" for d in out_dir.iterdir() if d.is_dir())
        srcs += sorted(f for f in out_dir.glob("PP*.md"))
        for card in srcs:
            if not card.is_file():
                continue
            text = card.read_text(errors="replace")
            state = (re.search(r"^state:\s*(\w+)", text, re.M) or [None, ""])[1]
            badge = _STATE_BADGE.get(state.lower(), "⬜")
            binding = (re.search(r"^binding:\s*(.+)$", text, re.M) or [None, ""])[1]
            q = (re.search(r"^question\s*:?\s*(.+)$", text, re.M) or [None, ""])[1]
            if not q:
                for ln in text.splitlines():
                    if ln.strip() and not ln.startswith(("#", "state:", "binding:", "-")):
                        q = ln.strip()
                        break
            name = card.parent.name if card.name == "card.md" else card.stem
            cards.append(
                "<div class='card'><span class='badge'>%s</span><b>%s</b>"
                "<div>%s</div><div class='mut'>%s</div></div>"
                % (badge, _esc(name), _esc(q),
                   _esc("binding: " + binding if binding else "no binding yet")))
        return self._plug_page(p, out_dir, "probe", "🚪 Probe",
                               cards or [_GHOST_PROBE],
                               "read-only · the consumer raises, the orchestrator claims, "
                               "the collector binds (QPf9 §3)")

    # ---- shared page writer ------------------------------------------
    def _plug_page(self, p, out_dir, route, label, cards, footer, strip=False, head=""):
        """strip=True lays the cards as a horizontal deck, one unit filling
        the pane, snap-shifted right to the next (JL 260815: "shift to the
        new one to the right") — the slide deck's scroll-snap move, sideways."""
        stem = out_dir.parent.name
        btn, script = self._rebuild_ui(route, p)
        if strip and len(cards) > 1:
            nav = ("<span class='nav'><button id='prev'>◀</button>"
                   "<span class='pos' id='pos'></span>"
                   "<button id='next'>▶</button></span>")
            deck = "<div class='strip' id='strip'>%s</div>" % "".join(cards)
            script += _STRIP_NAV
        else:
            nav = ""
            deck = "".join(cards)
        body = ("%s%s<h1>%s · %s</h1>"
                "<div class='mut' style='margin:0 0 12px'>%s</div>%s%s%s"
                % (btn, nav, label, _esc(stem), _esc(footer), head, deck, script))
        view = out_dir / ("%s-view.html" % stem)
        view.write_text(_PAGE.format(title="%s · %s" % (label, stem), body=body),
                        encoding="utf-8")
        url = self._url_of(view)
        return {"url": url, "count": len(cards)}, None
