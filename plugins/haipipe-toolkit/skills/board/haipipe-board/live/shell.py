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
  if (!href || href[0] === '#' || /^[a-z]+:/i.test(href) || !/\.html/.test(href)) return;
  var go = null;
  try { go = parent.frames.page && parent.frames.page.__boardGo; } catch (err) { return; }
  if (typeof go !== 'function') return;          // fall through to target="page"
  e.preventDefault();
  go(new URL(a.href, location.href).href.replace(/\?pane=page/, '') + '?pane=page', true);
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
  <button id="mtui" type="button" data-mode="tui"
    title="The real CLI in a terminal. Click again to put the chat away.">&gt;_ TUI Chat</button>
  <button id="mgui" type="button" data-mode="gui"
    title="The SDK chat box. Click again to put the chat away.">💬 GUI Chat</button>
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
  <iframe name="chat"  id="fc" data-src="__CHAT__"  title="chat"></iframe>
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
  var wanted = 'tui';
  try { wanted = localStorage.getItem('board-split-mode') || 'tui'; } catch (e) {}
  var btns = [document.getElementById('mtui'), document.getElementById('mgui')];

  function liveMode() {
    try { return frames.chat.__paneModeNow ? frames.chat.__paneModeNow() : wanted; }
    catch (e) { return wanted; }
  }
  function paint() {
    split.classList.toggle('hc', hidden);
    if (!hidden) load(document.getElementById('fc'));
    var on = hidden ? '' : liveMode();
    btns.forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.mode === on));
    });
  }
  function want(mode) {
    if (!hidden && liveMode() === mode) { hidden = true; }   // the lit one = put it away
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
