"""The Plugview page shell: the HTML page template, the strip-nav script, the
ghost scaffolds an empty tab shows, and the Probe state badges (moved verbatim from plugview.py).
"""


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

_GHOST_EVIDENCE = """<div class="card ghost"><b>E01-&lt;slug&gt; · Evidence Item</b>
<pre>specification   the page's evidence need
state:          planned → commissioned → landed → embedded
supporting:     execution/discovery Run ids
local:          consumer-owned Run id → immutable Result</pre>
<div class="mut">nothing landed yet · this is the Evidence Item shape the contract expects</div></div>"""

# The historical Probe protocol's own ladder,
# plus the three retired words so an old card still reads. `planned` and
# `commissioned` used to fall through to ⬜ here, which is how two ANSWERED
# cards on QC1-visitlbp read as untouched (fixed 260817).
_STATE_BADGE = {
    "planned": "⬜", "commissioned": "🔨", "answered": "✅",
    "answered-local": "✅", "read": "🧑✅",
    "deferred": "⏸", "failed": "🚨", "concern": "⚠️",
    "raised": "⬜", "working": "🔨", "bound": "✅",      # retired 260817
}
