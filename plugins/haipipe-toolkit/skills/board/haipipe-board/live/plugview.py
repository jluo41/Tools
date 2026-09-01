"""🖼🚪 Plugview · read-only evidence/display/ and evidence/probe/ surfaces.

THE DIVISION OF LABOUR, the same one export.py drew for latex/word/bibex:

  the writers (renderer skills · the probe orchestrator)   HOW material is made
  this file                                                WHERE the tab looks, read-only

Nothing here writes MATERIAL. A display unit is written by its renderer and
accepted by a person (QPf5); a probe card is raised by its consumer and bound
by the collector (QPf9). This surface SHOWS both and writes neither, which is
each contract's own rule: "the pane shows everything · writes NOTHING".
One carve-out, ruled JL 260816 ("I want to add the rebuild button, so that we
can have a new list"): display's 🔄 recompiles each unit's DERIVED preview
(preview.tex ▶ preview.pdf, the unit README's own rebuild contract) before
re-rendering the list. intake/, recipe/, and the accepted: tick stay a
person's and are never touched — a preview is a projection, not material.

THE VIEW IS DERIVED, like every export view: `<plugin>/<stem>-view.html` is
regenerated on each open and never hand-edited. An EMPTY plugin renders the
contract's ghost scaffold instead of a blank, so an empty tab teaches what
belongs there (JL 260815).
"""
import json
import os
import re
from pathlib import Path

_PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>
:root{{--bg:#ffffff;--fg:#1c1c1c;--mut:#7c7c78;--line:#e4e4e7;--card:#fff}}
@media(prefers-color-scheme:dark){{:root{{--bg:#161719;--fg:#e8e8e6;--mut:#9a9a97;
 --line:#2c2e33;--card:#1d1f23}}}}
body{{margin:0;padding:18px;background:var(--bg);color:var(--fg);
 font:14px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}
h1{{font-size:16px;margin:0 0 4px}} .mut{{color:var(--mut);font-size:12px}}
a.summary{{color:inherit}} h2{{font-size:14px;margin:14px 0 5px}}
p{{margin:7px 0}} ul{{margin:6px 0 8px 20px;padding:0}}
code{{font:12px ui-monospace,Menlo,monospace;background:var(--bg);padding:1px 4px;
 border-radius:4px}} .summary{{display:flex;gap:7px;flex-wrap:wrap;margin:0 0 10px}}
.metric{{border:1px solid var(--line);border-radius:999px;padding:3px 9px;
 background:var(--card);font-size:12px}} .ready{{color:#267247}} .pending{{color:#9a6115}}
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
.chead{{display:flex;align-items:baseline;gap:9px;padding:0 0 9px;
 border-bottom:1px solid var(--line);margin-bottom:11px}}
.pid{{font:700 11px ui-monospace,Menlo,monospace;color:var(--mut);
 border:1px solid var(--line);border-radius:5px;padding:1px 6px;letter-spacing:.04em}}
.ptitle{{font:600 15.5px/1.3 -apple-system,BlinkMacSystemFont,sans-serif}}
.q{{font-size:15px;line-height:1.55;margin:0 0 11px;max-width:60em}}
dl.fields{{display:grid;grid-template-columns:auto 1fr;gap:3px 14px;margin:0 0 12px;
 font-size:12.5px}}
dl.fields dt{{color:var(--mut);font:600 11px ui-monospace,Menlo,monospace;
 text-transform:uppercase;letter-spacing:.05em;padding-top:2px}}
dl.fields dd{{margin:0;word-break:break-all}}
.next{{font-size:12.5px;border-radius:7px;padding:7px 11px;margin:0 0 4px;
 border:1px solid var(--line);background:var(--card)}}
.next.owed{{color:#9a6115;border-color:#e5cfa8}}
.next.ok{{color:#267247;border-color:#bcdcc7}}
.step{{border:1px solid var(--line);border-radius:10px;margin:13px 0;
 overflow:hidden;background:var(--bg)}}
.step.lead{{border-color:var(--fg);border-width:1.5px}}
.step .sh{{display:flex;align-items:baseline;gap:8px;padding:7px 12px;
 background:var(--card);border-bottom:1px solid var(--line)}}
.step .sh b{{font:700 11.5px -apple-system,sans-serif;letter-spacing:.09em;
 text-transform:uppercase}}
.step .sh .sn{{color:var(--mut);font-size:11.5px;font-family:ui-monospace,Menlo,monospace}}
.step .sb{{padding:11px 13px}}
.step .sb p:first-child{{margin-top:0}} .step .sb p:last-child{{margin-bottom:0}}
details.fold>summary{{cursor:pointer}}
details.fold[open]>summary{{border-bottom:1px solid var(--line)}}
.hole{{border:1px dashed var(--line);border-radius:8px;padding:10px 12px;
 color:var(--mut);font-size:12.5px}}
figure.pf{{margin:0 0 12px;border:1px solid var(--line);border-radius:9px;
 overflow:hidden;background:var(--card)}}
figure.pf+.why{{margin:-6px 0 14px}}
.pfh{{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap;padding:8px 11px;
 border-bottom:1px solid var(--line)}}
.pfn{{font:600 12.5px ui-monospace,Menlo,monospace;word-break:break-all}}
.facts{{display:flex;gap:5px;flex-wrap:wrap}}
.fact{{font-size:10.5px;color:var(--mut);border:1px solid var(--line);
 border-radius:999px;padding:1px 8px;white-space:nowrap;background:var(--bg)}}
.exhibit{{display:block;width:100%;height:290px;border:0;background:var(--bg)}}
object.exhibit{{aspect-ratio:4/3;height:auto}}
.pfp{{border-top:1px solid var(--line);padding:6px 11px;font-size:11.5px;
 color:var(--mut)}}
.pfp>summary{{cursor:pointer}} .pfp div{{word-break:break-all;margin:3px 0}}
.why{{font-size:13px;line-height:1.55;margin:0 0 13px;max-width:60em}}
details>summary{{list-style:none}}
details>summary::-webkit-details-marker{{display:none}}
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

_GHOST_EVIDENCE = """<div class="card ghost"><b>PP01-&lt;slug&gt;/card.md</b>
<pre>question    in the page's own words, stake included
state:      planned → commissioned → answered → read
bank:       reuse | run | code | new
target:     &lt;task-folder&gt;/QA/&lt;n&gt;-&lt;slug&gt;.md</pre>
<div class="mut">nothing asked yet · this is the card shape the contract expects (QPf9 §1)</div></div>"""

# The protocol's own ladder (haipipe-probe, via haipipe-plugin-probe 0.7.0),
# plus the three retired words so an old card still reads. `planned` and
# `commissioned` used to fall through to ⬜ here, which is how two ANSWERED
# cards on QC1-visitlbp read as untouched (fixed 260817).
_STATE_BADGE = {
    "planned": "⬜", "commissioned": "🔨", "answered": "✅",
    "answered-local": "✅", "read": "🧑✅",
    "deferred": "⏸", "failed": "🚨", "concern": "⚠️",
    "raised": "⬜", "working": "🔨", "bound": "✅",      # retired 260817
}


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


def _inline_md(text):
    """The small, safe Markdown subset a probe card needs in its read-only tab.

    Card bodies are authored evidence summaries, not executable HTML.  Escape
    first, then restore only code and bold spans so a path or result can remain
    legible without allowing a card to inject markup into the Board shell.
    """
    text = _esc(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)


def _read(path):
    return path.read_text(errors="replace") if path.is_file() else ""


def _head_fields(text):
    """`key: value` lines above the first `##` — haipipe-plugin-probe §🪪."""
    out = {}
    for ln in text.splitlines():
        if ln.startswith("## "):
            break
        m = re.match(r"^([a-z_-]+):\s*(.*)$", ln)
        if m:
            out.setdefault(m.group(1), m.group(2).strip())
    return out


def _proof_rows(manifest):
    """-> ([{name,kind,rows,run,source,why}], note) from proof/manifest.yaml.

    A deliberately small reader: the surface must not gain a yaml dependency,
    and the manifest is authored to a fixed shape (§🧾).
    """
    if not manifest.is_file():
        return [], "no proof/manifest.yaml"
    text = manifest.read_text(errors="replace")
    rows, cur, in_files = [], None, False
    lines = text.splitlines()
    # A folded scalar (`why: >-`) keeps its text on the following indented
    # lines. Without this the surface printed the literal `>-` (found 260817
    # by looking at the rendered tab, not at the parser).
    for i, ln in enumerate(lines):
        m = re.match(r"^(\s*)([a-z_0-9]+):\s*[>|]-?\s*$", ln)
        if m:
            pad, tail = len(m.group(1)), []
            for nxt in lines[i + 1:]:
                if nxt.strip() and len(nxt) - len(nxt.lstrip()) > pad:
                    tail.append(nxt.strip())
                else:
                    break
            lines[i] = "%s%s: %s" % (m.group(1), m.group(2), " ".join(tail))
    for ln in lines:
        if re.match(r"^files:\s*\[\s*\]\s*$", ln):
            in_files = False
            continue
        if re.match(r"^files:\s*$", ln):
            in_files = True
            continue
        if re.match(r"^(why_empty|pending|card):", ln):
            in_files = False
        if in_files and re.match(r"^\s*-\s+\w+:", ln):
            cur = {}
            rows.append(cur)
        if in_files and cur is not None:
            m = re.match(r"^\s*-?\s*([a-z_0-9]+):\s*(.*)$", ln)
            if m:
                cur[m.group(1)] = m.group(2).strip()
    note = ""
    m = re.search(r"^(why_empty|pending):\s*(.*)$", text, re.M)
    if m and not rows:
        tail = []
        for ln in text.split(m.group(0), 1)[1].splitlines():
            if re.match(r"^\s+\S", ln):
                tail.append(ln.strip())
            elif tail:
                break
        note = "%s: %s" % (m.group(1), " ".join([m.group(2)] + tail).strip(" >-"))
    return rows, note


def _missing_step(head, qx, ax, proof, pnote):
    """The FIRST step that is not done — never a claim that one exists merely
    because the folder does (§🚪)."""
    if not qx.strip():
        return "no q-executor written yet: nothing can be dispatched"
    if not head.get("target"):
        return "q-executor written, target empty: nobody has been asked yet"
    if not ax.strip():
        return "dispatched, no answer copied back into a-executor.md"
    if not proof and not pnote:
        return "answered, but proof/ is empty and says nothing about why"
    return "answered · nobody has read it and written the A-consumer"


def _embed_proof(href, path):
    """EMBED the file, never re-render it as HTML (JL 260817).

    Display frames `preview.pdf` with <object>; a proof file is framed the same
    way. This is not only a look: every proof bug so far came from PARSING —
    `15.3332***` lost its stars to the bold rule, a folded yaml scalar printed
    `>-`, and esttab's `="..."` armour needed its own splitter. An embedded file
    is the file, so there is nothing left to get wrong.
    """
    if path.suffix == ".pdf":
        return ("<object class='exhibit' data='%s' type='application/pdf'>"
                "<a href='%s'>%s</a></object>" % (href, href, _esc(path.name)))
    return ("<iframe class='exhibit' src='%s' title='%s' loading='lazy'></iframe>"
            % (href, _esc(path.name)))


def _step(icon, label, note, inner, tone=""):
    """One wall step as its OWN panel: a header strip naming it, then its body.

    JL 260817 read the previous card as "乱糟糟" — five steps ran together in
    one column with only a hairline between them, so the eye could not tell
    where the dispatched question ended and the answer began.
    """
    return ("<section class='step %s'><header class='sh'><span>%s</span>"
            "<b>%s</b><span class='sn'>%s</span></header>"
            "<div class='sb'>%s</div></section>"
            % (tone, icon, _esc(label), _esc(note), inner))


def _proof_block(rows, note, folder, rel):
    """Wall step 4: ONE PANEL PER FILE — a header bar carrying the filename and
    its facts, the framed file flush underneath, provenance folded below."""
    if not rows:
        return ("<div class='hole'>🕳 %s</div>"
                % _esc(note or "empty, and the manifest says nothing about why"))
    out = []
    for r in rows:
        nm = r.get("name", "?")
        path = folder / nm
        facts = "".join("<span class='fact'>%s</span>" % _esc(x) for x in (
            r.get("kind", "?"), "%s rows" % r.get("rows", "?"),
            "%s bytes" % r.get("bytes", "?"),
            r.get("run", "")) if x)
        body = (_embed_proof(_esc("%s/proof/%s" % (rel, nm)), path)
                if path.is_file()
                else "<div class='hole'>🕳 named in the manifest, not on disk</div>")
        out.append(
            "<figure class='pf'>"
            "<figcaption class='pfh'><span class='pfn'>%s</span>"
            "<span class='facts'>%s</span></figcaption>"
            "%s"
            "<details class='pfp'><summary>provenance</summary>"
            "<div>source: <code>%s</code></div>"
            "<div>pulled: %s</div><div>sha256: <code>%s</code></div>"
            "</details></figure>"
            % (_esc(nm), facts, body, _esc(r.get("source", "?")),
               _esc(r.get("pulled", "?")), _esc(r.get("sha256", "?"))))
        if r.get("why"):
            out.append("<div class='why'>%s</div>" % _esc(r["why"]))
    return "".join(out)


def _probe_body_html(text):
    """Render the material below a probe card's header metadata.

    The previous surface silently discarded this body, leaving a bound Probe
    looking like a question plus a file tree.  This intentionally small reader
    supports the structures used by card.md (paragraphs, headings and lists)
    while keeping the plugin read-only and dependency-free.
    """
    kept = []
    for ln in text.splitlines():
        if ln.startswith("# ") or re.match(
                r"^(?:state|question|binding)\s*:", ln, re.I):
            continue
        kept.append(ln.rstrip())
    out, para, items = [], [], []

    def flush_para():
        if para:
            out.append("<p>%s</p>" % _inline_md(" ".join(x.strip() for x in para)))
            para.clear()

    def flush_items():
        if items:
            out.append("<ul>%s</ul>" % "".join(
                "<li>%s</li>" % _inline_md(x) for x in items))
            items.clear()

    fence = None
    for ln in kept:
        s = ln.strip()
        # A ``` block is VERBATIM. Without this the inline reader ate the
        # significance stars: `15.3332***` rendered as `15.3332*`, because
        # `**` is bold everywhere else (found 260817 by reading the tab).
        if s.startswith("```"):
            if fence is None:
                flush_para()
                flush_items()
                fence = []
            else:
                out.append("<pre>%s</pre>" % _esc("\n".join(fence)))
                fence = None
            continue
        if fence is not None:
            fence.append(ln)
            continue
        if not s:
            flush_para()
            flush_items()
        elif s.startswith("##"):
            flush_para()
            flush_items()
            out.append("<h2>%s</h2>" % _inline_md(s.lstrip("#").strip()))
        elif re.match(r"^[-*]\s+", s):
            flush_para()
            items.append(re.sub(r"^[-*]\s+", "", s))
        else:
            flush_items()
            para.append(s)
    if fence:
        out.append("<pre>%s</pre>" % _esc("\n".join(fence)))
    flush_para()
    flush_items()
    return "".join(out)


def _display_state(unit, rows):
    """Compute declared/rendered/accepted from files, never from folder count."""
    row = {k.lower(): v for k, v in rows}
    inputs = unit / "intake" / "inputs"
    has_intake = (unit / "intake" / "manifest.yaml").is_file() and \
        inputs.is_dir() and any(p.is_file() for p in inputs.rglob("*"))
    has_recipe = (unit / "recipe").is_dir() and \
        any(p.is_file() for p in (unit / "recipe").rglob("*"))
    assets = unit / "assets"
    has_asset = assets.is_dir() and any(
        p.is_file() and p.name in ("table-body.tex", "figure.pdf", "figure.png", "figure.svg")
        for p in assets.rglob("*"))
    has_preview = (unit / "preview.pdf").is_file()
    accepted_text = row.get("accepted", "").strip().lower()
    accepted = accepted_text.startswith(("✅", "yes", "true", "accepted"))
    rendered = has_asset and has_preview
    if not has_intake:
        next_step = "① INTAKE missing · add an approved frozen snapshot"
    elif not has_recipe:
        next_step = "② RENDER missing · add the renderer-owned recipe"
    elif not has_asset:
        next_step = "② RENDER has not produced a winning asset"
    elif not has_preview:
        next_step = "④ BUILD missing · compile preview.pdf"
    elif not accepted:
        next_step = "⑤ ACCEPT pending · rendered candidate awaits human review"
    else:
        next_step = "complete · rendered and human-accepted"
    return {"rendered": rendered, "accepted": accepted, "next": next_step}


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
        # 🔄 the rebuild recompiles every unit's derived preview first
        # (JL 260816): preview.tex ▶ preview.pdf in the unit's own dir, the
        # contract line each unit README already states. A unit without a
        # preview.tex is skipped whole — nothing is invented for it.
        fails = []
        env = dict(os.environ,
                   PATH="/Library/TeX/texbin:" + os.environ.get("PATH", ""))
        for unit in sorted(d for d in out_dir.iterdir() if d.is_dir()):
            if not (unit / "preview.tex").is_file():
                continue
            code, log = self._run(
                ["xelatex", "-interaction=nonstopmode", "preview.tex"],
                timeout=120, cwd=unit, env=env)
            if code != 0 or not (unit / "preview.pdf").is_file():
                fails.append(unit.name)
        cards, states = [], []
        for unit in sorted(d for d in out_dir.iterdir() if d.is_dir()):
            rows = _readme_rows(unit / "README.md")
            state = _display_state(unit, rows)
            states.append(state)
            # THE RENDER LEADS (JL 260819: "display the pdf at the very top,
            # and then show information" — clicking a unit showed him its
            # description rows first and the drawn thing below the fold).
            pdf = unit / "preview.pdf"
            if pdf.is_file():
                href = _esc(unit.name + "/preview.pdf")
                body = ("<object class='pdf' data='%s' type='application/pdf'>"
                        "<a href='%s'>preview.pdf</a></object>" % (href, href))
                body += ("<div class='%s' style='margin:7px 0'>%s</div>"
                         % ("ready" if state["accepted"] else "pending",
                            _esc(state["next"])))
            else:
                body = ("<div class='card ghost' style='margin:8px 0'>"
                        "🕳 no render yet · %s</div>" % _esc(state["next"]))
            body += "".join("<div class='mut'><b style='color:var(--fg)'>%s</b>: %s</div>"
                            % (_esc(k), _esc(v)) for k, v in rows)
            body += "<pre>%s</pre>" % _esc(_tree(unit))
            cards.append("<div class='card' id='%s'><b>%s</b>%s</div>"
                         % (_esc(unit.name), _esc(unit.name), body))
        # The NAME LIST: every unit as a chip, clicking one shifts the deck
        # there (JL 260815: "where is the name list for all the displays?").
        stem = out_dir.parent.name
        units = [d.name for d in sorted(out_dir.iterdir()) if d.is_dir()]
        summary = ("<div class='summary'><span class='metric'>%d declared</span>"
                   "<span class='metric ready'>%d rendered</span>"
                   "<span class='metric'>%d accepted</span></div>"
                   % (len(units), sum(s["rendered"] for s in states),
                      sum(s["accepted"] for s in states)))
        chips = ""
        if len(units) > 1:
            chips = "<div class='chips'>%s</div>" % "".join(
                "<a class='chip' href='#%s'>%s</a>"
                % (_esc(u), _esc(u[len(stem) + 1:] if u.startswith(stem + "-") else u))
                for u in units)
        footer = ("read-only · renderers write recipe/ and assets/; "
                  "a person rules intake/ and ticks accepted: (QPf5 §3) · "
                  "🔄 recompiles each unit's preview")
        if fails:
            footer += " · ⚠️ preview failed: " + ", ".join(fails)
        return self._plug_page(p, out_dir, "display", "🖼 Display",
                               cards or [_GHOST_DISPLAY], footer,
                               strip=True, head=summary + chips)

    # ---- POST /_board/probe ------------------------------------------
    def plug_probe(self, p):
        """One card per FOLDER, read in WALL ORDER so the reader sees the
        crossing: head, what was asked, what came back, the proof files, and
        the stake-bearing audit copy folded away (haipipe-plugin-probe §🚪).

        The four counts and the `read` verdict are computed from DISK, never
        from the `state:` word — a folder count is not an answered question.
        """
        page_src, out_dir, _, err = self._export_target(p, "probe")
        if err:
            return None, err
        dirs = sorted(d for d in out_dir.iterdir()
                      if d.is_dir() and d.name.startswith("PP"))
        flat = sorted(f for f in out_dir.glob("PP*.md"))
        cards, names, tally = [], [], {"planned": 0, "commissioned": 0,
                                       "answered": 0, "read": 0}
        for d in dirs + flat:
            card = d / "card.md" if d.is_dir() else d
            if not card.is_file():
                continue
            head = _head_fields(card.read_text(errors="replace"))
            name = d.name if d.is_dir() else d.stem
            names.append(name)
            state = head.get("state", "")
            badge = _STATE_BADGE.get(state.lower(), "⬜")

            qx = _read(d / "executor" / "q-executor.md")
            ax = _read(d / "executor" / "a-executor.md")
            qc = _read(d / "consumer" / "q-consumer.md")
            proof, pnote = _proof_rows(d / "proof" / "manifest.yaml")

            # the counts, from disk
            tally["planned"] += 1
            if head.get("target"):
                tally["commissioned"] += 1
            if ax.strip() and head.get("target"):
                tally["answered"] += 1
            is_read = head.get("read", "").startswith("✅")
            tally["read"] += 1 if is_read else 0

            # DISPLAY'S SHAPE, filled with probe's material, and every
            # step in its OWN PANEL (JL 260817: "每一个 file 是不是应该分开
            # 一些？现在看着乱糟糟的").
            rows = []
            if head.get("question"):
                rows.append("<div class='q'>%s</div>" % _inline_md(head["question"]))
            rows.append("<dl class='fields'>%s</dl>" % "".join(
                "<dt>%s</dt><dd>%s</dd>" % (_esc(k), _esc(head[k]))
                for k in ("state", "route", "bank", "serves", "target")
                if head.get(k)))
            rows.append("<div class='next %s'>%s</div>"
                        % ("ok" if is_read else "owed",
                           _esc(("✅ read · " + head.get("read", "").lstrip("✅ "))
                                if is_read
                                else "🕳 " + _missing_step(head, qx, ax, proof, pnote))))
            rows.append(_step("🔢", "proof", "the files behind the answer",
                              _proof_block(proof, pnote, d / "proof", d.name),
                              tone="lead"))
            rows.append(_step("🧱", "asked", "executor/q-executor.md · the only "
                              "thing dispatched", _probe_body_html(qx)))
            if ax.strip():
                rows.append(_step("📥", "came back", "executor/a-executor.md · "
                                  "the bank's own words", _probe_body_html(ax)))
            if qc.strip():
                rows.append("<details class='step fold'><summary class='sh'>"
                            "<span>🗂</span><b>audit</b><span class='sn'>"
                            "consumer/q-consumer.md · who wanted it, and why"
                            "</span></summary><div class='sb'>%s</div></details>"
                            % _probe_body_html(qc))
            rows.append("<details class='step fold'><summary class='sh'>"
                        "<span>📂</span><b>files</b><span class='sn'>%s</span>"
                        "</summary><div class='sb'><pre>%s</pre></div></details>"
                        % (_esc(d.name), _esc(_tree(d))))
            pp, _, words = name.partition("-")
            cards.append("<div class='card' id='%s'>"
                         "<div class='chead'><span class='badge'>%s</span>"
                         "<span class='pid'>%s</span>"
                         "<span class='ptitle'>%s</span></div>%s</div>"
                         % (_esc(name), badge, _esc(pp),
                            _esc(words.replace("-", " ")), "".join(rows)))

        n = len(names)
        verdict = "ready" if n and tally["read"] == n else ""
        summary = ("<div class='summary'>"
                   "<span class='metric'>%d planned</span>"
                   "<span class='metric'>%d commissioned</span>"
                   "<span class='metric'>%d answered</span>"
                   "<span class='metric %s'>%d / %d read</span></div>"
                   % (tally["planned"], tally["commissioned"], tally["answered"],
                      verdict, tally["read"], n))
        chips = ""
        if n > 1:
            chips = "<div class='chips'>%s</div>" % "".join(
                "<a class='chip' href='#%s'>%s</a>"
                % (_esc(x), _esc(x.split("-", 1)[0] if x.startswith("PP") else x))
                for x in names)
        return self._plug_page(p, out_dir, "probe", "🚪 Probe",
                               cards or [_GHOST_EVIDENCE],
                               "read-only · consumer/ never crosses · executor/ is "
                               "the only thing dispatched · a person ticks read:",
                               strip=True, head=summary + chips)

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
