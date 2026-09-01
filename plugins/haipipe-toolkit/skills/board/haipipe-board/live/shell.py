"""QD5 · the operating shell: index · page · chat, three frames that ignore each other.

One board page is one document, and today the browser shows the page list, the
page and the chat as ONE of them, so showing an edit means rebuilding all three.
This module is the other half of QD5's ruling: three same-origin iframes inside
one shell page, so a refresh is a frame re-fetch and no pane's reload can reach
another.

Four routes, and nothing else:

    GET <any board page>?split      the SAME path as the page, operated as
                                    three panes. One url per page, one query
                                    to choose how it is shown.
    GET /_shell?p=<page url>        the same thing by another name, kept
                                    because links to it exist
    GET <any board page>?pane=index the sidebar alone, links retargeted at `page`
    GET <any board page>?pane=chat  the drawer alone, opened on this page
    GET /_events?poll=1&p=<page url>  when did this board's pages last move

WHY A QUERY AND NOT A NEW PATH (QB2's invariant): a pane loads the SAME static
file that already ships at that URL. Strip the query and you have the page a
reader can open on its own, with every script stripped, exactly as before. The
panes add a `<style>` and one `window.__boardPane` line at serve time; nothing
is written to disk and no new artifact exists to go stale.

WHY ONE ASK EVERY 400 ms AND NOT A HELD STREAM: a server push was ruled and was
built first, and building it is what found the cost that ruled it back out. A
stream holds one of the browser's six connections per origin for as long as it
lives, and a replaced document's connections come back on the browser's
schedule, not ours — so opening the split twice inside a few seconds wanted
seven connections in six slots, and the second shell's panes simply never
loaded while its frames' `reload()` did nothing at all, silently, because a
queued request is indistinguishable from a slow one. The shell asks instead, on
a pooled connection it gives straight back. What C2 P1 objected to survives
intact: that was a 4000 ms poll inside ALL THREE panes ending in a `div.wrap`
swap; this is one small question from the shell, and the panes ask nothing.
"""

import base64
import json
import re
import urllib.parse
from pathlib import Path


# THE SAME MARK EVERY BOARD PAGE WEARS. The shell declared no icon at all, so a
# split tab showed the browser's default globe while every other board tab showed
# the mark — the one tab you operate from was the one you could not find (JL
# 260802). Read from the same `assets/board-mark.svg` the renderer embeds, so
# there is one file to change and no copy to drift.
_MARK = (Path(__file__).resolve().parent.parent / "assets" / "board-mark.svg")
FAVICON = ("data:image/svg+xml;base64,"
           + base64.b64encode(_MARK.read_bytes().strip()).decode("ascii")
           ) if _MARK.is_file() else ""


# An internal link to another board page: relative, ends `.html`, may carry a
# fragment. Absolute URLs and bare fragments are left exactly as they are.
_LINK = re.compile(r'href="(?!https?:|#|/)([^"#?]+\.html)(#[^"]*)?"')


# The pane stylesheets. Each hides everything the pane is not, and grows the one
# thing it is to fill its frame. They key on `body.pane-*`, which is added by
# the same injection that sets `window.__boardPane`.
PANE_CSS = {
    "index": """
/* QD5 index pane: the sidebar, alone, permanently open. */
body.pane-index{padding:0 !important;overflow:hidden}
body.pane-index .wrap,body.pane-index #chat,body.pane-index #chatfab,
body.pane-index .sbtoggle,body.pane-index .sbrz,body.pane-index #cbtn,
body.pane-index #cdock,body.pane-index #cpanel,body.pane-index .lrf{display:none !important}
body.pane-index .sidebar{transform:none !important;width:100% !important;
 padding:10px 8px 20px;z-index:1}   /* keeps its own border-right hairline */
""",
    "chat": """
/* QD5 chat pane: the drawer, alone, filling the frame. */
body.pane-chat{padding:0 !important;overflow:hidden}
body.pane-chat .wrap,body.pane-chat .sidebar,body.pane-chat .sbtoggle,
body.pane-chat .sbrz,body.pane-chat #chatfab,body.pane-chat #cbtn,
body.pane-chat #cdock,body.pane-chat #cpanel,body.pane-chat .lrf{display:none !important}
body.pane-chat #chat{position:fixed;inset:0;width:100% !important;max-width:none;
 box-shadow:none;display:flex}      /* keeps its own border-left hairline */
body.pane-chat #chat .rz,body.pane-chat #chat .back{display:none !important}
/* The drawer's own ✕ closed a drawer that sat over a page. Here the pane IS the
   drawer, so closing it would leave an empty frame; the strip's 💬 puts the
   whole pane away instead. `.term` (>_ / ←) STAYS — switching GUI chat to the
   TUI and back is exactly the choice JL asked to keep (260802). */
body.pane-chat #chat .hd .x{display:none !important}
/* `.term` flips its own glyph between `>_` and `←`, so it tells you what it
   will DO and never where you ARE. The choice belongs at the chat button in the
   shell's strip, which is where a reader asks it; the button stays in the DOM
   and keeps doing the work, hidden, because the switch hands a session back and
   forth under QD1's one-window Law and should have one implementation. */
body.pane-chat #chat .hd .term{display:none !important}
""",
    "page": """
/* QD5 page pane: the page, alone. The sidebar is the index pane's job now, and the
   chat is the chat pane's, so neither is drawn here even though both still ship
   in the file (A2.2 is what deletes the bytes; this only stops drawing them). */
body.pane-page{padding:0 !important}
body.pane-page .sidebar,body.pane-page .sbtoggle,body.pane-page .sbrz,
body.pane-page #chat,body.pane-page #chatfab{display:none !important}
""",
}

# What each pane runs once its own scripts have loaded. Only the chat pane needs
# anything: the drawer is opened for whatever page this frame is showing, which
# is the one gesture a reader would otherwise have to make on every navigation.
# What each pane runs once its own scripts have loaded. Only the chat pane needs
# anything: the drawer is opened for whatever page this frame is showing, and it
# exposes the mode switch so the SHELL can offer the choice at the chat button —
# which is where a reader asks the question (JL 260802: "what I want for the chat
# is choose the GUI or TUI when I click the chat button").
PANE_BOOT = {
    "index": """
/* A SIDEBAR CLICK IS A SWAP, NOT A NAVIGATION (JL 260802: "really slow to click and
   go to a new page"). `target="page"` loads a whole new document into the page
   frame, which parses 400 KB of html and re-executes the bundle every time. The
   page pane still owns a router that can replace one column instead, so ask it.
   The `target` stays on every link as the fallback: with scripts off, or if the
   page pane has not booted yet, the browser does the ordinary thing. */
document.addEventListener('click', function (e) {
  if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button) return;
  var a = e.target.closest && e.target.closest('a');
  if (!a) return;
  var href = a.getAttribute('href') || '';
  if (!href || href[0] === '#' || /^[a-z]+:/i.test(href) || !/\\.html/.test(href)) return;
  var go = null;
  try { go = parent.frames.page && parent.frames.page.__boardGo; } catch (err) { return; }
  if (typeof go !== 'function') return;          // fall through to target="page"
  e.preventDefault();
  go(new URL(a.href, location.href).href.replace(/\\?pane=page/, '') + '?pane=page', true);
});
""",
    "chat": """
window.addEventListener('load', function () {
  /* HONOUR THE BUTTON THAT OPENED THIS PANE (JL 260802: "when I click the GUI,
     but it is the TUI selected and opened, why?").
     The shell asks for a mode by calling `frames.chat.__paneMode(mode)` — but
     on the FIRST click the frame has not loaded yet, because the shell loads it
     lazily inside its own paint() which runs after that call. The request was
     therefore made to a window with no such function, swallowed by the try, and
     the pane then booted with the DRAWER's own preference, which defaults to
     the TUI. Reproduced from a cleared localStorage: `board-split-mode` read
     `gui`, `board-tui-default` was null, the pane opened `termon`, and the
     shell repainted `>_ TUI Chat` as the lit one.
     So the shell's radio is the source of truth and the drawer's own key is
     DERIVED from it, here, before the drawer is told to open. */
  try {
    var m = localStorage.getItem('board-split-mode');
    if (m === 'gui' || m === 'tui') {
      localStorage.setItem('board-tui-default', m === 'gui' ? '0' : '1');
    }
  } catch (e) {}
  if (window.__boardDrawerReopen) { try { window.__boardDrawerReopen(); } catch (e) {} }
  /* Belt and braces for the race the other way: if the drawer had already
     opened in the other mode before this ran, switch it with the one control
     that owns the handover. */
  /* LATE, AND ONLY IF NOTHING ELSE DID IT. This used to fire at 300ms and it
     RACED the drawer's own default-view opener: `chatOpen` schedules
     `__boardOpenDefaultView()` which opens the terminal when the TUI is the
     default, that involves a fetch and takes longer than 300ms, so this saw
     mode still `gui` and clicked `.term` a second time — and `.term` is a
     TOGGLE, so the second click closed what the first was opening. Measured
     260802: the terminal failed to come back after a reload in one run out of
     three, non-deterministically, which is exactly what a race looks like.
     Now the derived `board-tui-default` above makes path one correct on its
     own, and this is a fallback that waits for things to settle and stands
     down if a terminal is already up or on its way. */
  var settle = 0;
  var settleT = setInterval(function () {
    settle += 1;
    /* BOUNDED. Two of the branches below `return` without clearing, so a pane
       that never boots, or one holding a terminal, left this polling every
       500 ms for the life of the shell. A fallback that never gives up is a
       leak, and this one had two ways to reach it (found by re-reading the
       diff, 260803). Thirty ticks is fifteen seconds, far past any boot. */
    if (settle > 30) { clearInterval(settleT); return; }
    try {
      var m = localStorage.getItem('board-split-mode');
      if (m !== 'gui' && m !== 'tui') { clearInterval(settleT); return; }
      if (!window.__paneModeNow) return;                 // not booted yet
      if (window.__paneModeNow() === m) { clearInterval(settleT); return; }
      /* Stand down while a terminal is coming up: `__paneMode` toggles, and
         toggling against an in-flight open just fights it. Removing this guard
         was tried on 260802 and made the switch WORSE, from one failure in four
         to two in four and deterministic, because the fallback then clicked
         repeatedly against the drawer's own opener. */
      if (window.__boardTermOn && window.__boardTermOn()) return;
      if (settle < 6) return;                            // ~3s of quiet first
      clearInterval(settleT);
      window.__paneMode(m);
    } catch (e) { clearInterval(settleT); }
  }, 500);
  /* The drawer's own `.term` button still DOES the switch: handing a session
     between the chat box and the CLI is QD1's one-window Law and keeps exactly
     one implementation. This only gives the shell a handle on it. */
  window.__paneModeNow = function () {
    return (window.__boardTermOn && window.__boardTermOn()) ? 'tui' : 'gui';
  };
  window.__paneMode = function (want) {
    var b = document.querySelector('#chat .hd .term');
    if (!b || want === window.__paneModeNow()) return false;
    b.click();
    return true;
  };
});
""",
}


def _shell_doc(page_url, index_url):
    """The shell. Three frames, two drag handles, and the smallest script that
    can keep an address bar honest and listen for one event."""
    return r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="icon" type="image/svg+xml" href="__FAVICON__">
<title>board · split</title>
<style>
  /* THE SAME SURFACE AS THE BOARD. The shell shipped in its own dark chrome and
     read as three windows in a black frame (JL 260802: "I don't want the black
     boundary for the three split... make it the same style like the old
     version"). The one-document board separates its sidebar, page and drawer with
     a single hairline on a shared background, so the split does the same: these
     are the board's own variables, values and dark query copied, because the
     shell is a separate document and cannot inherit them. */
  :root{--bg:#fbfbf9;--fg:#1c1c1c;--mut:#7c7c78;--line:#e4e4df;--card:#fff;
    --accent:#1f5aa8}
  @media(prefers-color-scheme:dark){:root{--bg:#161719;--fg:#e8e8e6;--mut:#9a9a97;
    --line:#2c2e33;--card:#1d1f23;--accent:#6ea8f0}}
  html,body{margin:0;height:100%;background:var(--bg);color:var(--fg);overflow:hidden}
  /* The strip that answers "which board am I looking at". The address bar shows
     the shell rather than the page, so this is the only place that can say it. */
  .mhide{display:none !important}
/* One rule for BOTH bar menus (JL 260808: Plugin and Workflow). `left` is set from the
   button's own position when it opens, because a hardcoded offset was already only
   right for one button and would be wrong for every one added after it. */
.pmenu{position:absolute;top:38px;left:150px;z-index:90;
  min-width:260px;max-width:320px;
  max-height:calc(100vh - 96px);overflow-y:auto;overscroll-behavior:contain;
  background:#fff;border:1px solid #d8d8d8;border-radius:9px;padding:4px;
  box-shadow:0 10px 30px rgba(0,0,0,.16)}
.pmenu[hidden]{display:none}
/* `#bar button` above paints every button in the bar as a blue pill, and these rows
   ARE buttons inside the bar. The old `#mplugmenu .mrow` outranked it by an id; the
   class-only `.pmenu .mrow` did not, and the menu came back blue-on-blue. So the id
   stays in the selector: it is load-bearing, not decoration (measured 260808). */
#bar .pmenu .mrow{display:block;width:100%;text-align:left;border:0;background:none;
  padding:7px 10px;border-radius:6px;cursor:pointer;
  font:500 13px/1.35 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
  color:#1e1e1e !important}
#bar .pmenu .mrow:hover{background:#f1f3f5}
#bar .pmenu .mrow b{display:block;font-size:13px;font-weight:600;color:#1e1e1e !important}
#bar .pmenu .mrow i{display:block;font-size:11.5px;font-style:normal;
  color:#6b7280 !important;font-weight:400}
#bar{height:30px;display:flex;align-items:center;gap:9px;padding:0 12px;
    background:var(--card);color:var(--mut);border-bottom:1px solid var(--line);
    font:12px/1 ui-monospace,Menlo,monospace;white-space:nowrap;overflow:hidden}
  #bar a{color:var(--accent);text-decoration:none;flex:0 0 auto}
  #bar a:hover{text-decoration:underline}
  #where{font-weight:700;color:var(--fg);flex:0 0 auto}
  #what{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis}
  #bar .sep{color:var(--line);flex:0 0 auto}
  /* LABELLED, not bare glyphs. The old board could afford a wordless 💬 because
     it was a big accent pill with nowhere else to be; a 12px glyph in a strip is
     not the same thing to find. The word costs 34 pixels and buys the pill's
     recognisability without a FAB sitting on top of the prose forever — which is
     what a TOGGLE would have to do, since it can never hide itself the way the
     old fab did once the drawer was open. */
  #bar button{flex:0 0 auto;border:1px solid transparent;background:var(--accent);
    color:#fff;border-radius:999px;padding:4px 11px;cursor:pointer;
    font:600 12px/1 ui-monospace,Menlo,monospace;letter-spacing:.02em}
  #bar button:hover{filter:brightness(1.08)}
  #bar button[aria-pressed="false"]{background:transparent;color:var(--mut);
    border-color:var(--line)}
  /* TWO TOGGLES, NOT A MENU (JL 260802). Which chat you want and whether you
     want one are the same question, so they are the same control: the lit
     button IS the mode, neither lit means the pane is away, and clicking the
     lit one puts it away. Nothing to open, nothing to dismiss, and the state
     is readable without clicking anything. */
  #split{display:grid;height:calc(100% - 30px);overflow:hidden;
    grid-template-columns:var(--iw,250px) 5px 1fr 5px var(--cw,520px)}
  #split.hi{grid-template-columns:0 0 1fr 5px var(--cw,520px)}
  #rp{display:flex;flex-direction:column;min-width:0;overflow:hidden;
  border-left:1px solid var(--line,#e4e4df);background:var(--bg,#fff)}
#rptabs{flex:0 0 auto;display:flex;align-items:stretch;gap:2px;padding:5px 6px 0 6px;
  border-bottom:1px solid var(--line,#e4e4df);background:var(--card,#fff)}
.rpt{border:1px solid var(--line,#e4e4df);border-bottom:0;background:transparent;
  color:var(--mut,#7c7c78);cursor:pointer;border-radius:7px 7px 0 0;padding:5px 11px;
  font:600 12px/1 ui-monospace,Menlo,monospace}
.rpt:hover{background:var(--bg,#f1f3f5)}
/* the OPEN tab is the one that looks attached to the pane below it */
.rpt[aria-selected="true"]{background:var(--bg,#fff);color:var(--fg,#1c1c1c);
  border-color:var(--line,#e4e4df);margin-bottom:-1px;padding-bottom:6px}
.rpt[hidden]{display:none}
.rp-sp{flex:1}
/* the OPEN SET machinery (haipipe-plugin): the active tab's own ✕, the ＋
   that lists what this page could open, and the ＋ menu with its ● material dot */
#rp{position:relative}
#rptset{display:flex;align-items:stretch;gap:2px}
.rptx{margin-left:8px;color:var(--mut,#7c7c78);font-weight:700}
.rptx:hover{color:#c94a4a}
#rpplus{border:1px solid transparent;background:transparent;color:var(--mut,#7c7c78);
  cursor:pointer;border-radius:7px 7px 0 0;padding:5px 9px;
  font:700 13px/1 ui-monospace,Menlo,monospace}
#rpplus:hover{background:var(--bg,#f1f3f5)}
#rpmenu{position:absolute;top:32px;left:8px;z-index:95;min-width:240px;
  background:var(--card,#fff);border:1px solid var(--line,#d8d8d8);border-radius:9px;
  padding:4px;box-shadow:0 10px 30px rgba(0,0,0,.16)}
#rpmenu[hidden]{display:none}
#rpmenu .xrow{display:block;width:100%;text-align:left;border:0;background:none;
  padding:7px 10px;border-radius:6px;cursor:pointer;color:var(--fg,#1c1c1c);
  font:500 13px/1.35 ui-monospace,Menlo,monospace}
#rpmenu button.xrow:hover{background:var(--bg,#f1f3f5)}
#rpmenu .xrow .dot{float:right;color:#2a8a2a}
/* the FORM segment: subordinate to the Chat tab, never a tab itself */
#rpmode{display:flex;align-items:center;gap:2px;padding-bottom:4px}
#rpmode[hidden]{display:none}
.rpm{border:1px solid var(--line,#e4e4df);background:transparent;cursor:pointer;
  color:var(--mut,#7c7c78);border-radius:6px;padding:3px 8px;
  font:600 11px/1 ui-monospace,Menlo,monospace}
.rpm:hover{background:var(--bg,#f1f3f5)}
.rpm[aria-checked="true"]{background:var(--bg,#fff);color:var(--fg,#1c1c1c)}
#rp iframe{flex:1 1 auto;min-height:0}
/* 🎨 Studio (JL 260831): the drawing above, the chat below — zero-basis flex
   so the ratio, not the content, sets the split; the ✨ bar leads. */
#rp.studio #rptabs{order:-3}
#rp.studio #drawbar{order:-2}
#rp.studio #fd{order:-1;flex:1.15 1 0;min-height:0}
#rp.studio #fc{flex:1 1 0;min-height:0}
#rp iframe[hidden]{display:none}
/* ✨ the Draw and Slides tabs' control bars: one ask, one button, one status word */
#drawbar,#slidebar{flex:0 0 auto;display:flex;gap:6px;align-items:center;padding:6px 8px;
  border-bottom:1px solid var(--line,#e4e4df);background:var(--card,#fff)}
#drawbar[hidden],#slidebar[hidden]{display:none}
#adask,#sdask{flex:1 1 auto;min-width:0;font:12px ui-monospace,Menlo,monospace;
  padding:5px 8px;border:1px solid var(--line,#e4e4df);border-radius:7px;
  background:var(--bg,#fff);color:var(--fg,#1c1c1c)}
#adgo,#sdgo{flex:0 0 auto;font:600 12px/1 ui-monospace,Menlo,monospace;cursor:pointer;
  padding:6px 10px;border:1px solid var(--line,#e4e4df);border-radius:7px;
  background:var(--bg,#fff);color:var(--fg,#1c1c1c)}
#adgo:hover,#sdgo:hover{background:var(--bg,#f1f3f5)}
#adgo:disabled,#sdgo:disabled{opacity:.5;cursor:default}
#adstat,#sdstat{flex:0 1 auto;font:11px ui-monospace,Menlo,monospace;color:var(--mut,#7c7c78);
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#split.hc #rp{display:none}
#split{position:relative}
#split.hc{grid-template-columns:var(--iw,250px) 5px 1fr 0 0}
  #split.hi.hc{grid-template-columns:0 0 1fr 0 0}
  /* NARROW: THE SAME FIVE CHILDREN, STACKED. Three panes side by side stop
     being readable somewhere around a phone, so below 820px they become rows —
     and every rule here has to carry `#split.hi` and `#split.hc` in its
     selector, because those are id+class and would otherwise outrank a bare
     `#split` inside a media query and keep the column layout (which is what JL
     saw: one pane filling the top and white below it). */
  @media(max-width:820px){
    #split,#split.hi,#split.hc,#split.hi.hc{
      grid-template-columns:1fr;
      grid-template-rows:var(--ih,32%) 5px 1fr 5px var(--ch,42%)}
    #split.hi{grid-template-rows:0 0 1fr 5px var(--ch,42%)}
    #split.hc{grid-template-rows:var(--ih,32%) 5px 1fr 0 0}
    #split.hi.hc{grid-template-rows:0 0 1fr 0 0}
    .gr{cursor:row-resize;border-left:0;border-top:1px solid var(--line)}
    .gr:hover,.gr.on{border-top-color:var(--accent);
      box-shadow:inset 0 1px 0 var(--accent)}
    #bar{gap:6px;padding:0 8px}
    #what{display:none}          /* the page title is in the pane's own header */
  }
  iframe{border:0;width:100%;height:100%;display:block;background:var(--bg)}
  /* A HAIRLINE, not a bar. The 5px is the grab area a drag needs; what the eye
     sees is one 1px line in the board's own --line, the same separator the sidebar
     and the drawer draw on the one-document board. */
  .gr{background:var(--bg);border-left:1px solid var(--line);
    cursor:col-resize;touch-action:none}
  .gr:hover,.gr.on{border-left-color:var(--accent);
    box-shadow:inset 1px 0 0 var(--accent)}
</style>
</head>
<body>
<div id="bar">
  <a href="/boards" target="_top" title="every board in this SPACE">🏠</a>
  <button id="ti" type="button" title="Show or hide the page list (☰ on the old board)">☰ Pages</button>
  <button id="mplugbtn" type="button" aria-haspopup="menu" aria-expanded="false"
    title="Surfaces this page can open, to the right">🔌 Plugin ▾</button>
  <div id="mplugmenu" class="pmenu" hidden role="menu"></div>
  <button id="mwfbtn" type="button" aria-haspopup="menu" aria-expanded="false"
    title="Steppers for this page, along the bottom">🪜 Workflow ▾</button>
  <div id="mwfmenu" class="pmenu" hidden role="menu"></div>
  <button id="mtui" class="mhide" type="button" data-mode="tui"
    title="The real CLI in a terminal. Click again to put the chat away.">&gt;_ TUI Chat</button>
  <button id="mgui" class="mhide" type="button" data-mode="gui"
    title="The SDK chat box. Click again to put the chat away.">💬 GUI Chat</button>
  <!-- 🔌 A plugin surface the OPEN PAGE contributes. The shell hides the page's own
       FAB (see pane-page CSS), so without this row a registered plugin is unreachable
       inside the viewer: it worked on a bare page and nowhere a person actually looks.
       Drawn only when the page registers something that applies to it. -->

  <span class="sep">·</span>
  <span id="where">board</span>
  <span class="sep">·</span>
  <span id="what">loading…</span>
  <a id="plain" href="__PAGEPATH__?plain" target="_top" title="open this page on its own, without the split">↗ plain</a>
</div>
<div id="split">
  <iframe name="index" id="fi" data-src="__INDEX__" title="pages"></iframe>
  <div class="gr" data-var="iw" data-min="140" data-max="520"></div>
  <iframe name="page"  id="fp" src="__PAGE__"  title="page"></iframe>
  <div class="gr" data-var="cw" data-min="280" data-max="900" data-rev="1"></div>
  <!-- 🗂 THE RIGHT PANE IS TABBED (JL 260810). It used to be one iframe that the
       chat owned, while Draw painted its own overlay inside the PAGE column, so
       "opens to the right" meant two different mechanisms and opening both left
       405px of actual page. One column, three tabs, and the frames are HIDDEN
       rather than destroyed, because two of them hold state nothing can rebuild:
       a live SDK session and a live PTY. -->
  <div id="rp">
    <!-- 💬 ONE CHAT (JL 260815: "just have one Chat in the plugin, not more
         ChatGUI or Chat TUI"). The tab strip stopped selling the form: Chat is
         one tab, and the GUI/TUI choice appears INSIDE it, as the small mode
         segment on the right of the strip, visible only while Chat is open.
         The hidden #mtui/#mgui radio stays the single mode writer, so every
         check that drives it and every localStorage key is untouched. -->
    <!-- 🧩 TABS ARE AN OPEN SET, PER PAGE (haipipe-plugin, JL 260815): the
         strip shows what this page has OPEN, ＋ lists what it COULD open (● =
         material already on disk), the active tab carries its own ✕, and the
         pane's "✕ close" keeps meaning the whole pane. Buttons are rendered
         into #rptset from the set, so a new plugin never edits this markup. -->
    <div id="rptabs" role="tablist">
      <span id="rptset"></span>
      <button id="rpplus" type="button" title="open a plugin of this page">＋</button>
      <span class="rp-sp"></span>
      <span id="rpmode" role="radiogroup" aria-label="Chat form" hidden>
        <button class="rpm" data-mode="gui" type="button"
          title="The SDK chat box: gated edits, diffs, tool cards">🖥 GUI</button>
        <button class="rpm" data-mode="tui" type="button"
          title="The real CLI in a terminal: long jobs, skills">⌨️ TUI</button>
      </span>
    </div>
    <!-- ✨ THE DRAW TAB'S ONE CONTROL (JL 260815: "what I want is like a button,
         and it can generate what we want"). Ask is optional: empty means draw
         this page's ## Diagram. Claude authors the scene server-side
         (/_board/autodraw) and the watcher below repaints the canvas. -->
    <div id="drawbar" hidden>
      <input id="adask" type="text" spellcheck="false"
        placeholder="what to draw · empty = this page's ## Diagram">
      <button id="adgo" type="button">✨ Draw it</button>
      <span id="adstat"></span>
      <!-- 🎨 fold the canvas away (JL 260831: "make the draw collapsable");
           the bar stays as the handle, the choice is the reader's, remembered. -->
      <button id="adfold" type="button" hidden
        title="fold the drawing away · bring it back">⌄</button>
    </div>
    <!-- ✨ THE SLIDES TAB'S ONE CONTROL (JL 260815: "add a new button to it so
         we can regenerate the slide"). Ask is optional: empty means present the
         page's argument. Claude authors the deck server-side (/_board/autodeck)
         and the frame reloads onto the fresh file. -->
    <div id="slidebar" hidden>
      <input id="sdask" type="text" spellcheck="false"
        placeholder="what the talk should emphasize · empty = the page's argument">
      <button id="sdgo" type="button">✨ Regenerate</button>
      <span id="sdstat"></span>
    </div>
    <iframe name="chat"  id="fc" data-src="__CHAT__"  title="chat"></iframe>
    <iframe name="draw"  id="fd" title="drawing" referrerpolicy="no-referrer" hidden></iframe>
    <iframe name="slides" id="fs" title="slides" referrerpolicy="no-referrer" hidden></iframe>
    <!-- registry tabs get their frames on demand, appended here as fx-<id> -->
    <div id="rpmenu" hidden role="menu"></div>
  </div>
  <!-- No pane-level ✕ (JL 260815): each tab carries its own, and closing the
       last tab closes the pane. Esc keeps closing the whole pane. -->
</div>
<script>
(function () {
  var fp = document.getElementById('fp'), fi = document.getElementById('fi');
  var root = document.documentElement, shown = null;
  var INDEX = '__INDEXPATH__', OPENED = '__PAGEPATH__';

  /* ① THE ADDRESS BAR. An iframe's URL never reaches it, so without these lines
     the shell would read as one address forever and no page could be linked or
     bookmarked. Mirror the page frame's path into our own query string, and the
     `p=` we were opened with is what puts a shared link back on that page. This
     is the one real cost option A pays, and this is the whole of it. */
  function mirror() {
    var p;
    try { p = fp.contentWindow.location.pathname; } catch (e) { return; }
    /* ONLY EVER MIRROR A REAL PAGE. A frame that has not loaded yet reports
       `about:blank`, whose pathname is the word `blank`, and writing that into
       the address bar produced `/_shell?p=blank` — an address that names no
       board, cannot be shared, and 404s on reload. JL hit it within a minute
       of opening the split (260802: "this URL doesn't make sense... how do we
       know which board it is?"). */
    if (!p || !/\.html$/.test(p) || p === shown) return;
    shown = p;
    /* the page's own url, bare: the split is what that address opens as now */
    history.replaceState(null, '', p);
    /* THE CHAT FOLLOWS THE PAGE (JL 260802: "in different webpages, I open the
       TUI or GUI for each of them, things are mixed... TUI in Page 1 and Page 2
       are the same"). He is right and it was worse than mixed: the chat frame
       bound to whatever page the shell was OPENED on and never moved again, so
       browsing to a second page and opening its chat handed you the FIRST
       page's session — same drawer, same terminal key, same transcript.
       Measured: page frame QD2 → QD6 → QB4 while the chat stayed on QD2
       throughout. One chat per page is the rule; a page keeps its own sessions
       and may have several, which is QD1's Law and needs the chat to be bound
       to the page a reader is actually looking at.
       Never mid-turn: a running conversation is not something to navigate out
       from under, so a busy chat keeps its page until the turn ends. */
    (function () {
      var fc = document.getElementById('fc');
      if (!fc) return;
      var wantSrc = p + '?pane=chat';
      if ((fc.getAttribute('src') || '') === wantSrc) return;
      /* AN UNLOADED FRAME STILL HAS A STALE PLAN. `load()` lazily assigns
         `fr.dataset.src`, which was baked when the SHELL was rendered — the
         page it was first opened on. So navigating the page pane and only THEN
         clicking 💬 GUI opened the chat on the ORIGINAL page: JL's screenshot
         shows the page pane on QA2 and the chat header on QB0 (260803). This
         morning's fix skipped an unloaded frame on the assumption that the
         lazy load would use the current page. It does not. Re-aim the PLAN as
         well as the live src. */
      if (!fc.getAttribute('src')) { fc.dataset.src = wantSrc; return; }
      try {
        var w = fc.contentWindow;
        if (w && w.__chatProbe && w.__chatProbe.inflight()) return;   // a turn is running
        if (w && w.__boardTermOn && w.__boardTermOn()) {
          /* a live terminal is a running process, not a view: park it politely
             by letting the pane reload, which the PTY grace window covers */
        }
      } catch (e) {}
      fc.setAttribute('src', wantSrc);
    })();
    /* THE DRAW FOLLOWS THE PAGE, for the chat's exact reason one block up
       (JL 260815: "the split is not attached to the page, why?"): the canvas
       was aimed when the tab opened and a router swap fires no load event, so
       browsing QPf3 → QPf6 kept QPf3's scene on stage — and the ✨ button
       would have redrawn the WRONG page's scene. Re-aim on the same mirror
       the address bar and the chat already trust. A page with no drawing
       yields no url; paintTabs prunes the tab and the stage moves on. */
    (function () {
      var fdEl = document.getElementById('fd');
      if (!fdEl || fdEl.hidden) return;          // Draw not on stage: nothing aimed
      var url = '';
      try { url = drawURL(); } catch (e) {}
      if (url && (fdEl.getAttribute('src') || '') !== url) {
        fdEl.setAttribute('src', url);
      }
    })();
    /* ...AND SO DOES EVERY OTHER TAB (JL 260816: "when I change the page, the
       plugin is not changed accordingly — it is not attached to the focal
       page"). Chat and draw each earned a follow block above, one incident at
       a time; slides, the skill viewer, and every registry tab (folder, latex,
       word, bibex, skill, display, probe) were aimed only when SHOWN, and a
       router swap fires no load event, so navigating QPf1 → QPf6 kept QPf1's
       folder view on stage. One shared re-aim instead of a fourth incident. */
    try { reaimTabs(); } catch (e) {}
    var t = '';
    try { t = fp.contentDocument.title || ''; } catch (e) {}
    document.title = t || 'board · split';
    /* ...AND SAY IT ON SCREEN. The address bar shows the shell, so without a
       strip of its own the split is three frames with no answer to "which board
       am I in". Board name from the path, page title from the frame. */
    var name = (OPENED.split('/board/')[0] || '').split('/').filter(Boolean).pop() || 'board';
    document.getElementById('where').textContent = name;
    document.getElementById('what').textContent = t.replace(/\s+/g, ' ').trim();
    document.getElementById('plain').href = p + '?plain';   // the way OUT
  }

  /* ② THE REFRESH IS NOT HERE. Each pane asks about its own URL and reloads
     itself (`assets/js/20-live-refresh.js`, guarded by `window.__boardPane`),
     and the chat pane never asks at all. The shell knowing which frame to
     reload was the design's assumption and it cost two rewrites: a held stream
     spent one of the browser's six connections per origin and wedged the second
     open, and a shell-side poll had to remember what it had already told a
     frame to do, so a dropped reload was never retried. A frame asking about
     itself has neither problem: the question is one HEAD, the answer is its own
     reload, and being still stale next tick IS the retry.

     ONE ASK, FROM THE SHELL, EVERY 400 ms. The design ruled a server push and
     it was built first; building it is what found the cost that ruled it back
     out (C4 P6). A stream HOLDS one of the browser's six connections per origin
     for as long as it lives, and the ones belonging to a replaced document come
     back on the browser's schedule, so opening the split twice inside a few
     seconds put seven wanted connections into six slots: the second shell's
     panes never loaded and its frames' reload() silently did nothing, with no
     error anywhere because a queued request is indistinguishable from a slow
     one. This asks instead, on a pooled connection that is given straight back,
     and it asks the SHELL's question only — which is the part C2 P1 objected
     to, a 4000 ms poll inside all three panes that ended in a swap. One small
     request, 400 ms, no socket held, and the whole class of failure gone. */
  window.__EV = [];                       // kept as a debug handle
  function shownNow() {
    try { return fp.contentWindow.location.pathname; } catch (e) { return shown || ''; }
  }
  fp.addEventListener('load', mirror);
  /* the page pane calls this after a router SWAP, which fires no load event */
  window.__boardMirror = mirror;
  mirror();

  /* ④ THE TOGGLES. Same two gestures as the one-document board — ☰ hides the
     sidebar, 💬 hides the chat — and each remembers itself per machine, the way
     `--iw` and `--cw` already do. Hiding is a zero-width COLUMN, never an
     unloaded frame: a terminal mid-command must survive being put away. */
  var split = document.getElementById('split');
  /* LAZY, AND HIDDEN BY DEFAULT (JL 260802). A pane that is not on screen should
     not be paid for: the chat frame alone is a 30 KB document, 118 KB of xterm
     and a `claude` process that takes over a second to boot, and the index frame
     is the largest page on the board. Opening a page now loads ONE document and
     the other two arrive when they are first asked for. Once loaded they STAY
     loaded — hiding is still only a zero-width column, so a terminal mid-command
     survives being put away. */
  function load(fr) {
    if (fr && !fr.src && fr.dataset.src) fr.src = fr.dataset.src;
  }
  function pane(cls, key, btn) {
    var off = true;                       // hidden until asked for
    try { off = localStorage.getItem(key) !== '1'; } catch (e) {}
    function paint() {
      split.classList.toggle(cls, off);
      btn.setAttribute('aria-pressed', off ? 'false' : 'true');
      if (!off) load(document.getElementById(cls === 'hi' ? 'fi' : 'fc'));
    }
    paint();
    return {
      hidden: function () { return off; },
      set: function (v) {
        off = !v; paint();
        try { localStorage.setItem(key, off ? '0' : '1'); } catch (e) {}
      }
    };
  }
  var sidebarBtn = document.getElementById('ti');
  var sidebar = pane('hi', 'board-split-index', sidebarBtn);
  sidebarBtn.addEventListener('click', function () { sidebar.set(sidebar.hidden()); });

  /* THE CHAT IS TWO BUTTONS. `>_ TUI Chat` and `💬 GUI Chat` are one radio with an off
     position: the lit one is the mode you are in, clicking the other switches,
     clicking the lit one hides the pane, and neither lit means there is no chat
     on screen. The pane is only ever COLLAPSED, never unloaded, so a terminal
     mid-command is still running when you bring it back. */
  var hidden = true;                     // hidden until asked for
  try { hidden = localStorage.getItem('board-split-chat') !== '1'; } catch (e) {}
  /* GUI is the form a fresh reader gets (JL 260831: "if choose the Chat
     Plugin, make the GUI the default"); a stored choice still wins. */
  var wanted = 'gui';
  try { wanted = localStorage.getItem('board-split-mode') || 'gui'; } catch (e) {}
  var btns = [document.getElementById('mtui'), document.getElementById('mgui')];

  /* The registry lives in the PAGE frame, which is same-origin, so the shell reads it
     rather than keeping a second list that would drift. A page with nothing applicable
     keeps the button hidden, which is the same "never offer refused work" rule the
     surfaces use one level down. */
  function pageWin() {
    try { return frames.page || document.getElementById('fp').contentWindow; }
    catch (e) { return null; }
  }
  /* Entries registered by the OPEN PAGE, for one menu. The shell holds no list of its
     own beyond the two chats below, so a surface the engine has never heard of shows up
     here the moment its page registers it. */
  function pageEntries(menu) {
    var w = pageWin(), rows = [];
    try {
      if (w && w.boardPlugins) {
        w.boardPlugins.applicable(w.boardPlugins.livePage(), menu).forEach(function (e) {
          /* The shell owns these three. GUI and TUI always were; Draw joined them
             when the right pane gained tabs, because otherwise the same drawing has
             two doors inside the viewer, one of them the old overlay that eats the
             page column. On a BARE page there is no shell and no tab strip, so the
             menu entry is still the only door and still works. */
          if (e.id === 'gui' || e.id === 'tui' || e.id === 'chat'
              || e.id === 'draw' || e.id === 'slides' || e.id === 'studio'
              || e.tab) return;
          rows.push({ id: e.id, label: e.label, hint: e.hint || '',
                      run: function () { e.open(w.boardPlugins.livePage()); } });
        });
      }
    } catch (err) {}
    return rows;
  }

  /* 🔌 PLUGIN · surfaces, which open to the RIGHT. The two chats are the SHELL's and
     everything else is the open page's. The chat rows click the hidden radio buttons,
     so the lit-state and pane logic that was already written keeps working and is not
     reimplemented here. */
  function plugEntries() {
    /* ONE row for the one Chat (JL 260815): it opens in the last-used form and
       the strip's segment is where the form is chosen, so the menu stops
       selling GUI and TUI as two surfaces. */
    /* ONE ROOM (JL 260831: "put both of them into the studio, as one page"):
       the 💬 Chat and 🖌 Draw rows folded into 🎨 Studio — drawing above,
       chat below, both live at once, so the scene the chat redraws changes in
       front of the person talking. The 260815 refusal ("full chat under the
       canvas") was about the DRAW tab carrying a chat; the studio/ category
       is the room both tools share. 🎞 Slides lives in the 📤 Delivery tab. */
    var rows = [
      { id: 'studio', label: '🎨 Studio', hint: 'the human’s room · drawing above, chat below',
        run: function () { showTab('studio'); } }
    ];
    /* Registry tabs (haipipe-plugin): each row opens its right-pane tab
       through the same showTab the strip uses — one opener, one owner. */
    xdefs().forEach(function (e) {
      rows.push({ id: e.id, label: e.label, hint: e.hint || '',
                  run: function () { showTab(e.id); } });
    });
    var all = rows.concat(pageEntries('plugin'));
    /* THE DEFAULT LEADS THE MENU (JL 260831: "make the outline the first
       plugin and the default plugin"). rankDefault() has put it first in the
       STRIP since 260830, but this menu still opened on 💬 with 🧭 fifth. */
    var def = defaultTab();
    for (var i = 1; i < all.length; i++) {
      if (all[i].id === def) { all.unshift(all.splice(i, 1)[0]); break; }
    }
    return all;
  }
  /* 🪜 WORKFLOW · steppers over THIS page, which open along the BOTTOM. The shell owns
     none of these: a workflow is gated on the page's declared type, so the page is the
     only thing that can know whether one applies (JL 260808). */
  function wfEntries() { return pageEntries('workflow'); }

  /* One implementation, two buttons. A second copy of open/close/dismiss is how the two
     would drift, and the drift a person sees is a menu that will not shut. */
  function wireMenu(btn, menu, entries) {
    if (!btn || !menu) return function () {};
    function close() {
      menu.hidden = true;
      btn.setAttribute('aria-expanded', 'false');
      document.removeEventListener('pointerdown', away, true);
    }
    function away(ev) {
      if (!menu.contains(ev.target) && ev.target !== btn) close();
    }
    btn.onclick = function () {
      if (!menu.hidden) return close();
      var rows = entries();
      menu.innerHTML = rows.map(function (r, i) {
        return '<button class="mrow" type="button" role="menuitem" data-i="' + i + '">'
          + '<b>' + r.label + '</b><i>' + r.hint + '</i></button>';
      }).join('');
      menu.querySelectorAll('.mrow').forEach(function (b) {
        b.onclick = function () { close(); rows[+b.dataset.i].run(); };
      });
      menu.style.left = Math.round(btn.getBoundingClientRect().left) + 'px';
      menu.hidden = false;
      btn.setAttribute('aria-expanded', 'true');
      document.addEventListener('pointerdown', away, true);
    };
    /* An EMPTY menu hides its button rather than opening onto nothing. Most pages have
       no workflow, and a button that opens an empty box reads as broken rather than as
       not-applicable. The Plugin button always has the two chats, so it never hides. */
    return function () {
      var n = entries().length;
      btn.style.display = n ? '' : 'none';
      if (!n) close();
    };
  }
  var syncPlug = wireMenu(document.getElementById('mplugbtn'),
                          document.getElementById('mplugmenu'), plugEntries);
  var syncWf   = wireMenu(document.getElementById('mwfbtn'),
                          document.getElementById('mwfmenu'), wfEntries);
  function syncMenus() { try { syncPlug(); syncWf(); } catch (e) {} }
  /* The page registers its entries as it loads, and which ones apply changes with every
     navigation, so the buttons are synced on the page frame's load and once more a beat
     later: an entry contributed by a deferred script would otherwise stay missing until
     the NEXT navigation, which reads as the feature being broken on the page you opened. */
  fp.addEventListener('load', function () { syncMenus(); setTimeout(syncMenus, 150); });
  syncMenus();

  function liveMode() {
    try { return frames.chat.__paneModeNow ? frames.chat.__paneModeNow() : wanted; }
    catch (e) { return wanted; }
  }
  /* Closing is "click the lit one", which is a path that already exists and already
     writes both localStorage keys. Reusing it means the ✕ can never drift from what the
     buttons do, which is the drift that produced the 260802 lit-strip bug. */
  function closePane() {
    if (hidden) return;
    /* On a non-chat tab, closing the PANE must not detour through want()'s
       switch-to-chat normalization: put the pane away directly, state kept. */
    if (tab !== 'chat') {
      hidden = true;
      try { localStorage.setItem('board-split-chat', '0'); } catch (e) {}
      paint();
      return;
    }
    want(liveMode());
  }
  /* The pane-level ✕ button is gone (JL 260815): each tab closes itself and
     the last one takes the pane with it. Esc stays as the whole-pane close. */
  document.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape') closePane();
  });

  function paint() {
    split.classList.toggle('hc', hidden);
    if (!hidden) load(document.getElementById('fc'));
    var on = hidden ? '' : liveMode();
    btns.forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.mode === on));
    });
  }
  function want(mode) {
    /* Another tab may be on stage; a chat ask means "switch to chat", never a
       toggle-away of a pane that is showing something else. */
    var away = tab !== 'chat' && tab !== 'studio';
    if (away) {
      tab = 'studio'; ensureOpen('studio');
      var du = drawURL();
      if (du && fd.getAttribute('src') !== du) fd.setAttribute('src', du);
      stage('studio');
    }
    if (!hidden && !away && liveMode() === mode) { hidden = true; }   // the lit one = put it away
    else { hidden = false; wanted = mode;
           try { if (frames.chat.__paneMode) frames.chat.__paneMode(mode); } catch (e) {} }
    try {
      localStorage.setItem('board-split-chat', hidden ? '0' : '1');
      localStorage.setItem('board-split-mode', wanted);
      /* THE SHELL OWNS THE MODE, so it writes the drawer's key ITSELF rather
         than hoping the pane derives it. `__paneMode` above only lands when the
         frame is already loaded, and the pane's boot-time derivation only lands
         when the frame is COLD — between them sat the case that kept failing
         (JL 260802: clicking 💬 GUI left the strip lit on >_ TUI). One writer,
         here, on every click, covers both. */
      localStorage.setItem('board-tui-default', wanted === 'tui' ? '1' : '0');
    } catch (e) {}
    paint();
    setTimeout(paint, 1400);        // the switch releases a session; re-read after
  }
  btns.forEach(function (b) {
    b.addEventListener('click', function () { want(b.dataset.mode); });
  });
  /* the mode also changes from inside the pane (a restore reattaches a parked
     PTY), so the buttons follow the truth rather than what they last asked for */
  setInterval(paint, 1200);
  paint();

  /* ③ THE HANDLES. Fifteen lines and no dependency, which is the whole reason
     option B (a split-pane library) was dropped: a resize handle is not worth
     vendoring, and a library would still have left the panes in one document. */
  ['iw', 'cw'].forEach(function (k) {
    var v = null;
    try { v = localStorage.getItem('board-split-' + k); } catch (e) {}
    if (v) root.style.setProperty('--' + k, v + 'px');
  });
  document.querySelectorAll('.gr').forEach(function (g) {
    g.addEventListener('pointerdown', function (e) {
      g.setPointerCapture(e.pointerId); g.classList.add('on');
      var rev = g.dataset.rev, key = g.dataset.var;
      var lo = +g.dataset.min, hi = +g.dataset.max;
      /* stacked below 820px, so the drag follows the axis the grid is on */
      var rows = window.matchMedia('(max-width:820px)').matches;
      if (rows) key = (key === 'iw') ? 'ih' : 'ch';
      function move(ev) {
        var px = rows
          ? (rev ? window.innerHeight - ev.clientY : ev.clientY - 30)
          : (rev ? window.innerWidth - ev.clientX : ev.clientX);
        px = Math.max(lo, Math.min(hi, px));
        root.style.setProperty('--' + key, px + 'px');
      }
      function up(ev) {
        g.releasePointerCapture(e.pointerId); g.classList.remove('on');
        g.removeEventListener('pointermove', move);
        g.removeEventListener('pointerup', up);
        try {
          localStorage.setItem('board-split-' + key,
            parseInt(root.style.getPropertyValue('--' + key), 10));
        } catch (err) {}
      }
      g.addEventListener('pointermove', move);
      g.addEventListener('pointerup', up);
    });
  });

  /* ── 🗂 the tab strip ────────────────────────────────────────────────────────
     TABS ARE AN OPEN SET, PER PAGE (haipipe-plugin, JL 260815): the strip
     shows what this page has OPEN, ＋ lists what it COULD open, the active tab
     carries its own ✕, and the pane's "✕ close" keeps meaning the whole pane.
     Chat is NOT reimplemented: its tab clicks the same `want()` the bar buttons
     use. Draw and Slides keep their window hooks; every OTHER tab comes from a
     registry entry carrying `tab: {url, write}`, so plugin N+1 ships by
     registering and this shell is not edited for it. */
  var rp = document.getElementById('rp'), fd = document.getElementById('fd');
  var fs = document.getElementById('fs');
  var tab = 'studio';               // 🎨 studio (chat gui|tui + draw) · any open tab id

  /* 🎨 whether the studio's draw half is unfolded — per reader, remembered */
  function drawOpen() {
    try { return localStorage.getItem('board-studio-draw') !== '0'; }
    catch (e) { return true; }
  }
  function drawURL() {
    try {
      var w = frames.page;
      if (!w || !w.boardDrawOwner || !w.boardPlugins) return '';
      var o = w.boardDrawOwner(w.boardPlugins.livePage());
      return (o && o.url) || '';
    } catch (e) { return ''; }
  }

  /* THE SCENE FILE IS THE ONE TRUTH the dual stage watches. Chat's Claude (or
     anything else) writes <page>/draw/<id>.excalidraw; the canvas here refetches
     when the file's stamp moves, so a drawing asked for in the chat appears
     without a gesture. It stays quiet while the canvas itself holds focus — a
     person mid-stroke is the one writer a refetch could hurt. */
  /* ✨ THE BUTTON. One POST; Claude authors the scene server-side; the watcher
     below repaints the canvas when the file lands. The server refuses a
     hand-drawn scene and the group view, and the refusal is shown, not eaten. */
  (function () {
    var go = document.getElementById('adgo'), askEl = document.getElementById('adask'),
        st = document.getElementById('adstat');
    if (!go) return;
    function sceneRelNow() {
      var m = /board=([^&]+)/.exec(fd.getAttribute('src') || '');
      return m ? decodeURIComponent(m[1]) : '';
    }
    function run(isRetry) {
      var rel = sceneRelNow();
      if (!rel) { st.textContent = 'no scene under this view'; return; }
      go.disabled = true;
      st.textContent = '🖌 Claude is drawing… (a minute or two)';
      fetch('/_board/autodraw', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scene: rel, prompt: askEl.value.trim() })
      }).then(function (r) { return r.json(); }).then(function (j) {
        go.disabled = false;
        st.textContent = j.ok ? '✅ drawn (' + j.elements + ' elements) — refreshing'
                              : '✋ ' + (j.err || 'refused');
      }).catch(function () {
        /* A dropped CONNECTION is usually a serve.py restart mid-flight, and
           the drawing may still have landed (the file writes server-side; the
           watcher will show it). Retry once; after that, tell the truth. */
        if (!isRetry) {
          st.textContent = '⏳ server hiccuped (a restart?) — retrying…';
          setTimeout(function () { run(true); }, 3000);
          return;
        }
        go.disabled = false;
        st.textContent = '✋ server unreachable — is serve.py running?';
      });
    }
    go.addEventListener('click', run);
    askEl.addEventListener('keydown', function (e) { if (e.key === 'Enter') run(); });
    /* 🎨 the fold: one click hides the canvas (chat takes the whole room),
       one click brings it back; stage() re-reads the choice. The chat pane's
       composer 🖌 presses the same switch through window.__studioToggleDraw. */
    window.__studioToggleDraw = function () {
      try {
        localStorage.setItem('board-studio-draw', drawOpen() ? '0' : '1');
      } catch (e) {}
      if (tab === 'studio') stage('studio');
    };
    var fold = document.getElementById('adfold');
    if (fold) fold.addEventListener('click', window.__studioToggleDraw);
  })();

  var sceneStamp = '';
  var sceneDown = false;      // the server was unreachable on the last look
  function reloadCanvas() {
    var src = fd.getAttribute('src');
    fd.setAttribute('src', '');
    requestAnimationFrame(function () { fd.setAttribute('src', src); });
  }
  setInterval(function () {
    if (hidden || (tab !== 'draw' && tab !== 'studio') || fd.hidden) return;
    /* ATTACHMENT IS RE-CHECKED EVERY TICK, not only at open and at mirror():
       every stale path found so far (router swap with the tab hidden, a shell
       loaded before a fix, a restored tab strip) ends the same way — the
       staged scene is not this page's scene (JL 260816: "still it s not well
       attached"). The watcher already knows both addresses; comparing them
       here makes the mismatch impossible to keep for more than one tick. */
    var want = '';
    try { want = drawURL(); } catch (e) {}
    if (want && (fd.getAttribute('src') || '') !== want) {
      sceneStamp = '';
      fd.setAttribute('src', want);
      return;
    }
    var m = /board=([^&]+)/.exec(fd.getAttribute('src') || '');
    if (!m) return;
    var rel = decodeURIComponent(m[1]);
    try { if (fd.contentWindow && fd.contentWindow.document.hasFocus()) return; }
    catch (e) {}
    fetch('/' + rel, { method: 'HEAD', cache: 'no-store' }).then(function (r) {
      /* Coming back from a dead server, reload regardless of the stamp: a
         canvas that booted while serve.py was restarting is an EMPTY canvas
         over a scene that exists, and the stamp alone cannot tell it apart. */
      var wasDown = sceneDown;
      sceneDown = false;
      if (!r.ok) return;
      var s = rel + '·' + (r.headers.get('last-modified') || '')
                  + '·' + (r.headers.get('content-length') || '');
      if (wasDown) { sceneStamp = s; return reloadCanvas(); }
      if (!sceneStamp || sceneStamp.indexOf(rel + '·') !== 0) { sceneStamp = s; return; }
      if (s === sceneStamp) return;
      sceneStamp = s;
      reloadCanvas();
    }).catch(function () { sceneDown = true; });
  }, 2500);

  /* Slides joins the strip the way Draw did (JL 260815: "why not together with
     them"): the URL comes from the page's own plugin; the deck itself is
     AUTHORED (JL 260815: "We will just have the AI deck"), so the shell only
     locates, loads, and — through the ✨ bar — asks for a regeneration. */
  function slidesURL() {
    try {
      var w = frames.page;
      if (!w || !w.boardSlidesURL) return '';
      return w.boardSlidesURL(w.boardPlugins && w.boardPlugins.livePage()) || '';
    } catch (e) { return ''; }
  }

  /* ALWAYS RELOAD, cache-busted. Twice bitten on 260815: the iframe held a
     deck loaded before its file was fixed, and "same src" meant reopening the
     tab showed the stale document forever. Every open refetches. */
  function loadDeck(surl) {
    surl = surl || slidesURL();
    if (!surl) return;
    var noDeck = function () {
      fs.removeAttribute('src');
      fs.setAttribute('srcdoc',
        '<body style="margin:0;display:flex;align-items:center;'
        + 'justify-content:center;height:100vh;font:15px/1.7 ui-serif,'
        + 'Georgia,serif;color:#444;background:#fff">'
        + '<div style="max-width:34em;padding:2em;text-align:center">'
        + '<div style="font-size:2.4em">🎞</div>'
        + '<p>This page has no deck yet.</p>'
        + '<p style="color:#888">Press ✨ Regenerate above and Claude will '
        + 'author one from the page into its slide/ plugin.</p></div></body>');
    };
    fetch(surl, { method: 'HEAD', cache: 'no-store' }).then(function (r) {
      if (r.ok) {
        fs.removeAttribute('srcdoc');
        fs.setAttribute('src', surl + '?plain&v=' + Date.now());
        return;
      }
      noDeck();
    }).catch(noDeck);
  }

  /* ✨ THE REGENERATE BUTTON (JL 260815: "add a new button to it so we can
     regenerate the slide"). One POST; Claude authors the deck server-side
     (/_board/autodeck); the frame reloads onto the fresh file. The page's .md
     path is derived from the deck URL, so the shell still holds no list. */
  (function () {
    var go = document.getElementById('sdgo'), askEl = document.getElementById('sdask'),
        st = document.getElementById('sdstat');
    if (!go) return;
    function run(isRetry) {
      var surl = slidesURL();
      if (!surl) { st.textContent = 'no page under this view'; return; }
      var md = surl.replace(/\/slide\/([^\/]+)-deck\.html$/, '/$1.md');
      if (md === surl) { st.textContent = 'cannot derive the page from ' + surl; return; }
      go.disabled = true;
      st.textContent = '🎞 Claude is authoring the deck… (a few minutes)';
      fetch('/_board/autodeck', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ file: md, prompt: askEl.value.trim() })
      }).then(function (r) { return r.json(); }).then(function (j) {
        go.disabled = false;
        if (j.ok) {
          st.textContent = '✅ ' + j.slides + ' slides — loading';
          loadDeck(surl);
        } else {
          st.textContent = '✋ ' + (j.err || 'refused');
        }
      }).catch(function () {
        /* A dropped connection is usually a serve.py restart mid-flight; the
           deck may still land server-side. Retry the LOOK, not the write. */
        if (!isRetry) {
          st.textContent = '⏳ connection dropped — checking for the deck…';
          setTimeout(function () { go.disabled = false; loadDeck(surl); }, 5000);
          return;
        }
        go.disabled = false;
        st.textContent = '✋ server unreachable — is serve.py running?';
      });
    }
    go.addEventListener('click', function () { run(false); });
    askEl.addEventListener('keydown', function (e) { if (e.key === 'Enter') run(false); });
  })();

  /* Registry entries carrying a `tab` spec — the plugin contract's whole
     interface to this shell. The registry lives in the page frame, so the
     shell holds no list that could drift. */
  function xdefs() {
    var out = [];
    try {
      var w = pageWin();
      if (w && w.boardPlugins) {
        w.boardPlugins.all().forEach(function (e) {
          if (e.tab && ['chat', 'gui', 'tui', 'draw', 'slides', 'studio'].indexOf(e.id) < 0)
            out.push(e);
        });
      }
    } catch (e) {}
    return out;
  }
  function defOf(id) {
    var ds = xdefs();
    for (var i = 0; i < ds.length; i++) if (ds[i].id === id) return ds[i];
    return null;
  }
  function tabLabel(id) {
    if (id === 'studio') return '🎨 Studio';
    if (id === 'chat') return '💬 Chat';
    if (id === 'draw') return '🖌 Draw';
    if (id === 'slides') return '🎞 Slides';
    var d = defOf(id);
    return d ? d.label : id;
  }
  /* Never offer work that would be refused: draw needs a scene, slides needs a
     namable deck (a folded page always can), a registry tab needs its entry.
     (The second 🔍 Skill staging tab retired 260816 — JL: "maybe just one":
     the 🛠 tab opens on the skill INDEX, a name opens the skill in the same
     frame, and the viewer's ☰ walks back to the index.) */
  function offerable(id) {
    /* 260831: chat + draw live inside 🎨 Studio (a sceneless page still
       offers it — the chat half is always there); the strip no longer sells
       their old ids, and 🎞 rides in 📤 Delivery. */
    if (id === 'studio') return true;
    if (id === 'chat' || id === 'draw' || id === 'slides') return false;
    return !!defOf(id);
  }

  /* THE OPEN SET, per page: a reader returns to the pane the way they left it. */
  var openSet = null;
  function tabsKey() { return 'board-split-tabs:' + (shownNow() || OPENED); }
  /* 🧭 THE DEFAULT TAB IS THE REGISTRY'S, NOT CHAT (JL 260830: "the outline
     will be shown as the default and be ranked to be the first, not the Chat.
     This is very important"). The page frame has carried
     `boardPlugins.setDefault('outline')` since 260818, but only the FAB read
     it: this shell seeded `['chat']` and `tab = 'chat'` on its own, so every
     split pane opened on 💬 with 🧭 second or absent. The shell now asks the
     registry, and the default goes FIRST in the strip whenever the page can
     offer it. A stored set keeps the reader's other choices; only the rank of
     the default is corrected. */
  function defaultTab() {
    try {
      var w = pageWin();
      var d = w && w.boardPlugins && w.boardPlugins.getDefault(w.boardPlugins.livePage());
      return (d && d.tab && d.id && offerable(d.id)) ? d.id : '';
    } catch (e) { return ''; }
  }
  function rankDefault() {
    var id = defaultTab();
    if (!id || openSet === null) return id;
    var i = openSet.indexOf(id);
    if (i > 0) openSet.splice(i, 1);
    if (i !== 0) openSet.unshift(id);
    return id;
  }
  function loadSet() {
    openSet = ['studio'];
    try {
      var v = JSON.parse(localStorage.getItem(tabsKey()) || 'null');
      if (Array.isArray(v) && v.length) openSet = v;
    } catch (e) {}
    /* Stored sets predating the 260831 fold speak the old ids: chat and
       draw became the one 🎨 Studio room, slides moved into 📤 Delivery. */
    var seen = {};
    openSet = openSet.map(function (id) {
      if (id === 'chat' || id === 'draw') return 'studio';
      if (id === 'slides') return 'delivery';
      return id;
    }).filter(function (id) {
      if (seen[id]) return false; seen[id] = 1; return true;
    });
    rankDefault();
  }
  function saveSet() {
    try { localStorage.setItem(tabsKey(), JSON.stringify(openSet)); } catch (e) {}
  }
  function ensureOpen(id) {
    if (openSet === null) loadSet();
    if (openSet.indexOf(id) < 0) { openSet.push(id); saveSet(); }
  }
  loadSet();

  /* Registry tabs get a frame on demand; like fc/fd/fs it is then HIDDEN on a
     switch, never destroyed. */
  function xframe(id) {
    var f = document.getElementById('fx-' + id);
    if (!f) {
      f = document.createElement('iframe');
      f.id = 'fx-' + id;
      f.title = id;
      f.referrerPolicy = 'no-referrer';
      f.hidden = true;
      rp.appendChild(f);
    }
    return f;
  }
  function extraFrames() {
    return [].slice.call(rp.querySelectorAll('iframe[id^="fx-"]'));
  }
  function stage(id) {                       // one frame on stage — or the 🎨 pair
    /* 🎨 Studio (JL 260831) shows BOTH: the drawing above, the chat below —
       #rp is a flex column and every visible frame flexes, so the split is
       the layout's own. A page with no scene staged yet keeps the chat full
       height. (The 260815 refusal of "full chat under the canvas" was about
       the DRAW tab; the studio room is both tools', by JL's ask.) */
    var duo = id === 'studio';
    var hasScene = !!(fd.getAttribute('src') || '');
    var showDraw = duo && hasScene && drawOpen();
    document.getElementById('fc').hidden = id !== 'chat' && !duo;
    fd.hidden = id !== 'draw' && !showDraw;
    fs.hidden = id !== 'slides';
    /* ✨ Draw's control bar rides above the canvas, wherever the canvas is —
       and in the studio it STAYS while the canvas is folded: it is the handle
       that brings the drawing back. */
    var bar = document.getElementById('drawbar');
    if (bar) bar.hidden = !(id === 'draw' || (duo && hasScene));
    var fold = document.getElementById('adfold');
    if (fold) {
      fold.hidden = !duo;
      fold.textContent = drawOpen() ? '⌄' : '⌃';
      fold.title = drawOpen() ? 'fold the drawing away — chat takes the room'
                              : 'bring the drawing back';
    }
    rp.classList.toggle('studio', showDraw);
    var sbar = document.getElementById('slidebar');
    if (sbar) sbar.hidden = id !== 'slides';
    extraFrames().forEach(function (f) { f.hidden = ('fx-' + id) !== f.id; });
  }
  function noteDoc(msg) {
    return 'data:text/html;charset=utf-8,' + encodeURIComponent(
      '<body style="margin:0;display:grid;place-items:center;height:100vh;'
      + 'font:13px ui-monospace,Menlo,monospace;color:#7c7c78;background:#fbfbf9">'
      + '<div style="max-width:80%;white-space:pre-wrap">' + msg + '</div></body>');
  }

  var firstPaint = true;
  function paintTabs() {
    if (openSet === null) loadSet();
    /* The registry may not have existed when loadSet ran at boot; rank again
       now, and if the pane has never shown anything but the seed, aim it at
       the default so the first open lands on 🧭 rather than 💬. */
    var def = rankDefault();
    /* Boot lands on the default even when the pane comes up VISIBLE (JL
       260831): the `hidden` guard alone left a pane restored open on 💬,
       because nothing had chosen 'chat' but the seed. Once the registry has
       answered, the first paint is the only one allowed to re-aim. */
    if (def && tab === 'studio' && (hidden || firstPaint)) {
      tab = def;
      if (!hidden) { xframe(def); stage(def); aimTab(def); }
    }
    if (def) firstPaint = false;
    /* Prune what this page cannot offer, without persisting the prune: the
       stored set is the reader's choice and the next page may honour it. */
    var set = openSet.filter(offerable);
    if (!hidden && set.indexOf(tab) < 0) {
      if (set.length) { showTab(set[set.length - 1]); return; }
      hidden = true;
      try { localStorage.setItem('board-split-chat', '0'); } catch (e) {}
      split.classList.add('hc');
    }
    var live = hidden ? '' : tab;
    var host = document.getElementById('rptset');
    if (host) {
      host.innerHTML = set.map(function (id) {
        var on = id === live;
        return '<button class="rpt" data-tab="' + id + '" type="button" role="tab"'
          + ' aria-selected="' + on + '">' + tabLabel(id)
          + (on ? '<span class="rptx" title="close this tab">✕</span>' : '')
          + '</button>';
      }).join('');
      [].forEach.call(host.querySelectorAll('.rpt'), function (b) {
        b.addEventListener('click', function (ev) {
          if (ev.target && ev.target.classList
              && ev.target.classList.contains('rptx')) closeTab(b.dataset.tab);
          else showTab(b.dataset.tab);
        });
      });
    }
    /* The FORM segment shows only while Chat is the open tab (JL 260815: the
       choice is made AFTER opening the Chat, inside it), and the lit half is
       whatever mode is actually live, which want() alone decides. */
    var seg = document.getElementById('rpmode');
    if (seg) {
      seg.hidden = hidden || (tab !== 'chat' && tab !== 'studio');
      [].forEach.call(seg.querySelectorAll('.rpm'), function (m) {
        m.setAttribute('aria-checked', String(m.dataset.mode === liveMode()));
      });
    }
  }

  /* RE-AIM the staged tab at the page now in the frame, WITHOUT the lit-click
     rebuild: navigation is a look, never a request to recompile. An existing
     artifact lands; a missing one shows an invitation, the way the deck's own
     "no deck yet" body already does — auto-building here would fire a latex
     compile or a claude run as a side effect of browsing. */
  function aimTab(which) {
    if (which === 'slides') { loadDeck(); return; }
    var d = defOf(which);
    if (!d) return;
    var f = xframe(which);
    var w = pageWin(), page = null;
    try { page = w && w.boardPlugins && w.boardPlugins.livePage(); } catch (e) {}
    var u = '';
    try { u = d.tab.url(page) || ''; } catch (e) {}
    function invite() {
      f.setAttribute('src', noteDoc('⬜ nothing built for this page yet — click the '
        + tabLabel(which) + ' tab to build it'));
    }
    if (!u) { invite(); return; }
    fetch(u, { method: 'HEAD' }).then(function (r) {
      if (!r.ok) { invite(); return; }
      landFrame(f, u);
    }).catch(function () {});
  }

  /* LANDING IS FRESH BY CONTRACT (JL 260816: "make sure the folder plugin
     refreshes every time"). "Same src, do nothing" was the rule here, and for
     a LIVE view it is exactly wrong: /_board/folderstat keeps one URL per
     page, so coming back to a page — or clicking the lit 📂 tab — kept the
     snapshot from before, while latex compiled and files landed unseen. The
     server already says no-store; the frame was the stale half. Same src now
     means RELOAD; a changed src navigates as before. */
  function landFrame(f, u) {
    var src = u + (/\.html$/.test(u) ? '?plain' : '');
    if (f.getAttribute('src') !== src) { f.setAttribute('src', src); return; }
    try { f.contentWindow.location.reload(); }
    catch (e) { f.setAttribute('src', src); }
  }

  /* The one follow-the-page entry: re-read this page's own tab set, let
     paintTabs prune and possibly switch, then re-aim whatever survived on
     stage. Guarded until the tab machinery below has finished booting,
     because mirror() runs once before it has. */
  var reaimOK = false;
  function reaimTabs() {
    if (!reaimOK) return;
    loadSet();
    var prev = tab;
    paintTabs();                 // may switch via showTab, which aims itself
    if (!hidden && tab === prev && tab !== 'chat' && tab !== 'draw'
        && tab !== 'studio' && offerable(tab)) aimTab(tab);
  }

  function showTab(which) {
    ensureOpen(which);
    if (which === 'studio') {
      var duurl = drawURL();
      tab = 'studio';
      hidden = false;
      split.classList.remove('hc');
      if (duurl && fd.getAttribute('src') !== duurl) fd.setAttribute('src', duurl);
      stage('studio');
      try { localStorage.setItem('board-split-chat', '1'); } catch (e) {}
      paint(); paintTabs();
      return;
    }
    if (which === 'draw') {
      var url = drawURL();
      if (!url) return;
      tab = 'draw';
      hidden = false;
      split.classList.remove('hc');
      if (fd.getAttribute('src') !== url) fd.setAttribute('src', url);
      stage('draw');
      try { localStorage.setItem('board-split-chat', '1'); } catch (e) {}
      paint(); paintTabs();
      return;
    }
    if (which === 'slides') {
      var surl = slidesURL();
      if (!surl) return;
      tab = 'slides';
      hidden = false;
      split.classList.remove('hc');
      stage('slides');
      try { localStorage.setItem('board-split-chat', '1'); } catch (e) {}
      paint(); paintTabs();
      loadDeck(surl);
      return;
    }
    if (which === 'chat') {
      /* ONE CHAT TAB (JL 260815). Opening it resumes the LAST-USED form; the
         segment beside it switches forms; clicking the lit tab puts the pane
         away, which is the radio's own off position. Coming back from another
         tab must not toggle the chat away, so reveal the frame first and only
         call want() when something actually changes. */
      var wasAway = tab !== 'chat';
      tab = 'chat';
      stage('chat');
      if (wasAway) { hidden = false; paint(); paintTabs(); return; }
      want(wanted);
      paintTabs();
      return;
    }
    /* A REGISTRY TAB (haipipe-plugin): frame the saved artifact, or ask
       the page's own writer to build one. Clicking the lit tab REBUILDS — a
       derived view's refresh — where chat's lit-click means "put away". */
    var d = defOf(which);
    if (!d) return;
    var rebuild = tab === which && !hidden;
    tab = which;
    hidden = false;
    split.classList.remove('hc');
    var f = xframe(which);
    stage(which);
    try { localStorage.setItem('board-split-chat', '1'); } catch (e) {}
    paint(); paintTabs();
    var w = pageWin(), page = null;
    try { page = w && w.boardPlugins && w.boardPlugins.livePage(); } catch (e) {}
    function land(u) { landFrame(f, u); }   // fresh-by-contract, one rule
    function build() {
      f.setAttribute('src', noteDoc('⏳ building ' + tabLabel(which) + '…'));
      try {
        d.tab.write(page, function (j) {
          if (j.url) land(j.url);
          else f.setAttribute('src', noteDoc('⚠ the writer returned no url'));
        }, function (e) { f.setAttribute('src', noteDoc('⚠ ' + e)); });
      } catch (e) { f.setAttribute('src', noteDoc('⚠ ' + e)); }
    }
    var u = '';
    try { u = d.tab.url(page) || ''; } catch (e) {}
    if (rebuild || !u) { build(); return; }
    fetch(u, { method: 'HEAD' })
      .then(function (r) { r.ok ? land(u) : build(); })
      .catch(build);
  }

  /* ✕ ON THE ACTIVE TAB closes THAT TAB: out of the set, focus to its left
     neighbour, and closing the last one closes the pane. Always visible and
     only on the lit tab, because the phone has no hover (QPf4d) and a strip of
     permanent close targets is a strip of accidents. Closing is safe by
     construction: a derived view has nothing to lose, Draw saves on edit, and
     a chat turn survives its reader through the ring. */
  function closeTab(id) {
    if (openSet === null) loadSet();
    var i = openSet.indexOf(id);
    if (i < 0) return;
    openSet.splice(i, 1);
    saveSet();
    if (tab === id) {
      var next = openSet[i - 1] || openSet[i] || openSet[0];
      if (next) { showTab(next); return; }
      hidden = true;                       // the last tab: the pane goes with it
      try { localStorage.setItem('board-split-chat', '0'); } catch (e) {}
      paint();
    }
    paintTabs();
  }

  /* ＋ · WHAT THIS PAGE COULD OPEN (JL 260815: a tab appears on an explicit
     click). One row per offerable-but-closed plugin; ● marks the ones whose
     material is already on disk, and the offer stands either way. */
  var plus = document.getElementById('rpplus');
  var pmenu = document.getElementById('rpmenu');
  function closePlus() {
    if (!pmenu) return;
    pmenu.hidden = true;
    document.removeEventListener('pointerdown', plusAway, true);
  }
  function plusAway(ev) {
    if (pmenu && !pmenu.contains(ev.target) && ev.target !== plus) closePlus();
  }
  if (plus && pmenu) plus.onclick = function () {
    if (!pmenu.hidden) return closePlus();
    if (openSet === null) loadSet();
    var rows = [];
    ['chat', 'draw', 'slides'].forEach(function (id) {
      if (openSet.indexOf(id) < 0 && offerable(id)) rows.push({ id: id });
    });
    xdefs().forEach(function (e) {
      if (openSet.indexOf(e.id) < 0) rows.push({ id: e.id, def: e });
    });
    if (!rows.length) {
      pmenu.innerHTML = '<div class="xrow" style="cursor:default;color:var(--mut)">'
        + 'every plugin of this page is open</div>';
    } else {
      pmenu.innerHTML = rows.map(function (r, i) {
        return '<button class="xrow" type="button" data-i="' + i + '" data-id="'
          + r.id + '">' + tabLabel(r.id) + '<span class="dot" hidden>●</span></button>';
      }).join('');
      [].forEach.call(pmenu.querySelectorAll('button.xrow'), function (b) {
        b.onclick = function () { closePlus(); showTab(b.dataset.id); };
        var r = rows[+b.dataset.i], u = '';
        try {
          if (r.id === 'draw') u = drawURL();
          else if (r.id === 'slides') u = slidesURL();
          else if (r.def) {
            var w = pageWin();
            u = r.def.tab.url(w && w.boardPlugins && w.boardPlugins.livePage()) || '';
          }
        } catch (e) {}
        if (r.id === 'chat' || !u) return;
        if (r.id === 'draw') { b.querySelector('.dot').hidden = false; return; }
        fetch(u, { method: 'HEAD' }).then(function (resp) {
          if (resp.ok) b.querySelector('.dot').hidden = false;
        }).catch(function () {});
      });
    }
    pmenu.hidden = false;
    document.addEventListener('pointerdown', plusAway, true);
  };

  /* The segment's click is a MODE SWITCH, never a toggle-away: want() treats a
     click on the live mode as "put it away", so a same-mode click is dropped
     here rather than surprising the reader with a vanished pane. */
  [].forEach.call(document.querySelectorAll('#rpmode .rpm'), function (m) {
    m.addEventListener('click', function () {
      if (hidden || liveMode() !== m.dataset.mode) want(m.dataset.mode);
      paintTabs();
    });
  });
  /* The page frame decides what applies AND which set is this page's, so both
     are re-read when a new page lands in it, not only at boot — and an open
     non-chat tab is re-aimed at the new page's own artifact. Through
     reaimTabs, the same path router swaps take via mirror(): the old
     showTab(tab) here hit the lit-click branch, whose meaning is REBUILD, so
     every full page load recompiled whatever derived tab was open. */
  var fpEl = document.getElementById('fp');
  if (fpEl) fpEl.addEventListener('load', function () {
    setTimeout(reaimTabs, 300);
  });
  reaimOK = true;
  setTimeout(paintTabs, 900);
  var _paint = paint;
  paint = function () { _paint(); paintTabs(); };
})();
</script>
</body>
</html>
""".replace("__INDEX__", index_url + "?pane=index") \
   .replace("__CHAT__", page_url + "?pane=chat") \
   .replace("__PAGE__", page_url + "?pane=page") \
   .replace("__INDEXPATH__", index_url) \
   .replace("__FAVICON__", FAVICON) \
   .replace("__PAGEPATH__", page_url)


class ShellMixin:
    # ---- helpers -----------------------------------------------------
    def split_of(self, path):
        """Should this request be answered with the SHELL? Returns the page path.

        THE SPLIT IS THE DEFAULT (JL 260802). Opening a board page in a browser
        gives the three panes; `?plain` gives the one document it always was.

        Telling a tab navigation from everything else, over plain HTTP:

          `?pane=` / `?plain`   a frame, or the opt-out          -> the FILE
          Sec-Fetch-Dest        exact, and USELESS HERE: browsers
                                send it only to trustworthy
                                origins, meaning https or
                                localhost, and this board is
                                http on a tailnet address, so it
                                never arrives (260802, and the
                                reason the first cut of this
                                silently did nothing)
          Accept: text/html     what a NAVIGATION asks for; every
                                fetch() in this codebase sends
                                */* and so does curl             -> the SHELL

        So a pane, `70-router.js`, `20-live-refresh.js`, `curl`, a scraper and
        anything else programmatic all still receive the file. That is what
        keeps QB2 true: the page a reader can open and read with scripts
        stripped is still one GET away, and is what every non-browser gets.

        ONE URL PER PAGE (JL, 260802: "why don't they share the same URL? It is
        very weird"). It was weird: the split lived at `/_shell?p=<escaped path>`
        while the page lived at its own address, so the same page had two names
        and neither address bar told you it was the same thing. Now the path IS
        the page and the query says how to show it — nothing, `?split`, or
        `?pane=…` for a frame inside the split."""
        head, _, query = path.partition("?")
        if not head.endswith(".html"):
            return None
        q = urllib.parse.parse_qs(query, keep_blank_values=True)
        if "pane" in q or "plain" in q:
            return None                      # a frame, or the opt-out
        if "split" in q:
            return head                      # asked for it by name
        dest = (self.headers.get("Sec-Fetch-Dest") or "").lower()
        if dest:
            return head if dest == "document" else None
        accept = (self.headers.get("Accept") or "")
        return head if "text/html" in accept else None

    @staticmethod
    def pane_of(path):
        """`…/QD5-x.html?pane=chat` -> `"chat"`, and anything else -> None.

        Only a real board page can be a pane, so the `.html` test is part of the
        recognition rather than a guard bolted on after it: `?pane=` on any other
        URL is meaningless and falls straight through to the static handler."""
        head, _, query = path.partition("?")
        if not head.endswith(".html") or not query:
            return None
        kind = (urllib.parse.parse_qs(query).get("pane") or [""])[0]
        return kind if kind in PANE_CSS else None

    @staticmethod
    def fragment_of(path):
        """Recognize the small body fragment used by in-place navigation."""
        head, _, query = path.partition("?")
        if not head.endswith(".html") or not query:
            return None
        fragment = (urllib.parse.parse_qs(query).get("fragment") or [""])[0]
        return fragment if fragment == "wrap" else None

    def _shell_file(self, url):
        """A board URL -> the file on disk, or None if it leaves --root."""
        rel = urllib.parse.unquote((url or "").split("?", 1)[0]).lstrip("/")
        if not rel:
            return None
        f = (self.root / rel).resolve()
        try:
            f.relative_to(self.root.resolve())
        except ValueError:
            return None
        return f

    @staticmethod
    def _index_of(page_url):
        """`…/board/QD/QD5-x.html` -> `…/board/index.html`. Every page in the
        tree lives under the board's own `board/` folder, so the index is found
        by the same cut `boardPath()` already makes on the client."""
        i = page_url.rfind("/board/")
        if i == -1:
            return page_url.rsplit("/", 1)[0] + "/index.html"
        return page_url[:i] + "/board/index.html"

    def _send_html(self, html, mtime=None, etag=None):
        raw = html.encode("utf-8")
        enc = None
        # A pane carries the whole page, sidebar included, so it is the biggest
        # single thing this server hands out and it does not come from the
        # static handler that `try_gzip` covers (QD5 C2 P5).
        if len(raw) > 1024 and "gzip" in (self.headers.get("Accept-Encoding") or "").lower():
            import gzip as _gzip
            raw, enc = _gzip.compress(raw, 6), "gzip"
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        if enc:
            self.send_header("Content-Encoding", enc)
            self.send_header("Vary", "Accept-Encoding")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-cache, must-revalidate")
        if etag:
            # NANOSECONDS, because `Last-Modified` is whole seconds and an edit
            # that lands in the SAME second as the page load is then invisible
            # to a pane comparing timestamps — it sits stale believing it is
            # current. That window is narrow and this board is rebuilt in
            # bursts, so it is hit often enough to matter (260802).
            self.send_header("ETag", etag)
        if mtime is not None:
            # A PANE MUST BE ABLE TO ASK WHEN IT LAST CHANGED. The static handler
            # sends `Last-Modified` for free and the panes are served from here
            # instead, so without this line a pane's HEAD of its own URL comes
            # back with nothing to compare and it never refreshes at all — which
            # is exactly how it behaved for one silent round (260801).
            self.send_header("Last-Modified", self.date_time_string(mtime))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(raw)

    # ---- GET <page>?split  ·  GET /_shell?p=… -------------------------
    def serve_shell(self, page=None):
        if page is None:
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            page = (q.get("p") or [""])[0].split("?", 1)[0]
        page = urllib.parse.unquote(page)
        f = self._shell_file(page)
        if f is not None and f.is_dir():
            # A BOARD FOLDER IS A FAIR ANSWER TO "which page". Typing a board's
            # path is what a reader has in hand; making them find a page url
            # first would be the shell asking for the thing it can work out.
            for cand in (f / "board" / "index.html", f / "index.html"):
                if cand.is_file():
                    page = "/" + str(cand.relative_to(self.root.resolve()))
                    f = cand
                    break
        if not page or f is None or not f.is_file():
            return self.send_error(404, "give ?p=<a board page url, or a board folder>")
        return self._send_html(_shell_doc(page, self._index_of(page)))

    # ---- GET <board page>?pane=… -------------------------------------
    def serve_pane(self, kind):
        """The page as it ships, plus a body class, a stylesheet, and one line
        that tells the page's own scripts they are in a pane. Nothing is written
        to disk: strip the query and the byte-identical file is still there."""
        u = urllib.parse.urlparse(self.path)
        f = self._shell_file(u.path)
        if f is None or not f.exists():
            return self.send_error(404)
        html = f.read_text(encoding="utf-8")
        head = ("<script>window.__boardPane=" + json.dumps(kind) + ";</script>"
                "<style>" + PANE_CSS.get(kind, "") + "</style>")
        if kind in ("index", "page"):
            # A LINK OUT OF A PANE MUST LAND IN A PANE. `target="page"` sends the
            # href as written, so a sidebar click used to load the plain page into
            # the page frame: sidebar inside sidebar, drawer inside drawer, and the
            # router switched back on because nothing told that document it was
            # in a frame. Carrying `?pane=page` on the way out is what keeps the
            # frame a frame, and it is the same query a reader can delete to get
            # the standalone page back.
            html = _LINK.sub(r'href="\1?pane=page\2"', html)
        if kind == "index":
            # A4.2 · NAVIGATION COSTS NO JAVASCRIPT. `<base target="page">` makes
            # every link in this frame load the sibling frame named `page`, which
            # is ordinary HTML that browsers have done since before JavaScript
            # existed. It carries no `href`, so nothing else about how this
            # document resolves its own assets changes. This one tag is what
            # `70-router.js` spent a hundred lines imitating.
            head = '<base target="page">' + head
        boot = PANE_BOOT.get(kind, "")
        if boot:
            head += "<script>" + boot + "</script>"
        # `</head>` and `<body` are both emitted by the one template in
        # src/page_board.py, so this is a substitution and never a search.
        html = html.replace("</head>", head + "</head>", 1)
        st = f.stat()
        tag = '"%d"' % st.st_mtime_ns
        # the document carries its own stamp, so its poll compares like with like
        html = html.replace("</head>",
                            "<script>window.__paneStamp=" + json.dumps(tag)
                            + ";</script></head>", 1)
        html = html.replace("<body class=\"", "<body class=\"pane-" + kind + " ", 1)
        return self._send_html(html, st.st_mtime, tag)

    def serve_fragment(self):
        """Serve only the generated page body used by in-place navigation."""
        u = urllib.parse.urlparse(self.path)
        f = self._shell_file(u.path)
        if f is None or not f.is_file():
            return self.send_error(404)
        html = f.read_text(encoding="utf-8")
        start = html.find('<div class="wrap"')
        end = html.rfind("</div>")
        if start < 0 or end < start:
            return self.send_error(404, "page has no wrap fragment")
        fragment = html[start:end + len("</div>")]
        st = f.stat()
        tag = '"%d"' % st.st_mtime_ns
        return self._send_html(fragment, st.st_mtime, tag)

    # ---- HEAD <board page>?pane=… ------------------------------------
    def head_pane(self):
        """Answer a pane's own poll without building the page: it only reads the
        stamp. Cheap on purpose — three panes ask every 800 ms."""
        u = urllib.parse.urlparse(self.path)
        f = self._shell_file(u.path)
        if f is None or not f.is_file():
            return self.send_error(404)
        st = f.stat()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("ETag", '"%d"' % st.st_mtime_ns)
        self.send_header("Last-Modified", self.date_time_string(st.st_mtime))
        self.send_header("Cache-Control", "no-cache, must-revalidate")
        self.send_header("Content-Length", "0")
        self.end_headers()

    # ---- GET /_events?poll=1&p=… -------------------------------------
    def serve_events(self):
        """When did this board's pages last move? One small answer, no stream.

        Watching MTIMES rather than hooking the writers is deliberate: a board is
        rebuilt by `rebuild()` after a chat write, by `watch.py` when JL saves a
        .md in an editor, and by anyone running `build.py` by hand. Only the
        filesystem sees all three, and it needs no cooperation from any of them.

        The answer is scoped to the BOARD's own `board/` tree, and refusing to
        widen past it is the point: without the `/board/` cut a stray `p=` would
        set the walk loose on --root, and --root is a repo.
        """
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        page = (q.get("p") or [""])[0]
        pf = self._shell_file(page)
        if pf is None or not pf.is_file():
            return self.send_error(404, "give ?p=<a board page url that exists>")
        i = page.rfind("/board/")
        tree = self._shell_file(page[:i] + "/board") if i != -1 else None
        if tree is None or not tree.is_dir():
            tree = pf.parent
        root = self.root.resolve()
        at = {}
        try:
            for f in tree.rglob("*.html"):
                try:
                    at["/" + str(f.relative_to(root))] = f.stat().st_mtime_ns
                except (OSError, ValueError):
                    pass
        except OSError:
            pass
        raw = json.dumps({"at": at}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(raw)
