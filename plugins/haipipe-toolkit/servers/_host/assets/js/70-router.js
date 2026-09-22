/* ── board/ tree navigation (QC9, JL 260731) ───────────────────────────────
   In the tree each page is its own document, so a normal link click is a real
   navigation and a real navigation destroys the chat drawer and the terminal,
   which is the exact failure QD4's parked-outside-the-wrap design exists to
   avoid. So in site mode we intercept internal links, fetch the target, swap
   ONLY div.wrap, and pushState. The drawer never notices it moved.

   With scripts off every link is still an ordinary href, so the tree stays
   fully navigable and the strip-scripts invariant holds. */
(function () {
  /* QD5, corrected 260802. The first cut turned the router OFF in every pane,
     reasoning that a frame is the unit that reloads. That made every click a
     full DOCUMENT boot: fetch the page, parse 400 KB of html, and execute this
     whole bundle again. The page pane instead swaps one column and keeps
     everything else alive. JL felt it immediately ("really slow to click
     and go to a new page"), and he was right: 42 ms against 49 ms on the machine
     serving it, and far worse across a tailnet.

     So the PAGE pane keeps the router and a click is a swap again. The index and
     chat panes still return here: nothing in them should swap anything. */
  if (window.__boardPane && window.__boardPane !== 'page') return;
  if (!document.body.classList.contains('split')) return;  // single-file mode
  var busy = false, pending = null;

  function samesite(a) {
    if (!a || !a.getAttribute) return false;
    var href = a.getAttribute('href') || '';
    if (!href || href[0] === '#' || /^[a-z]+:/i.test(href)) return false;
    if (a.target === '_blank') return false;
    return /\.html(\?|#|$)/.test(href);
  }

  async function go(url, push) {
    /* Dropping a navigation that arrives mid-swap loses it for good: the second
       of two quick clicks does nothing, and Back pressed during a swap moves
       the URL while the content stays put (both reproduced in headless Chrome
       260731). Hold the latest request and run it when this one lands. */
    if (busy) { pending = [url, push]; return; }
    busy = true;
    try {
      /* `no-store` re-downloaded the whole page on every visit, and 82% of a
         page's bytes are the sidebar, which this swap then throws away because the
         sidebar lives outside div.wrap. `no-cache` still REVALIDATES every time, so
         a rebuilt page is never served stale, but an unchanged one comes back as
         a 0-byte 304 instead of 136 KB (JL 260801: "why does it take a long time
         to navigate"). Correctness is unchanged; only the wire is. */
      /* A HUNG FETCH MUST NOT WEDGE THE ROUTER. `busy` guards against two
         clicks racing, and its only release is this function finishing, so a
         request that never settles left every later click queued forever and
         the sidebar simply stopped working (measured 260802, after the swap was
         put back in the page pane). Five seconds, then fall back to an ordinary
         navigation, which is slower but always arrives. */
      var ctl = new AbortController();
      var bell = setTimeout(function () { ctl.abort(); }, 5000);
      var r;
      /* The sidebar is repeated in every generated page. Navigation only replaces
         `.wrap`, so ask the live server for that fragment directly. A static
         server that ignores the query still returns the full page as fallback. */
      var fragmentUrl = new URL(url, location.href);
      fragmentUrl.searchParams.set('fragment', 'wrap');
      try { r = await fetch(fragmentUrl.href, { cache: 'no-cache', signal: ctl.signal }); }
      finally { clearTimeout(bell); }
      var doc = new DOMParser().parseFromString(await r.text(), 'text/html');
      var nw = doc.querySelector('div.wrap'), old = document.querySelector('div.wrap');
      if (!nw || !old) { location.href = url; return; }
      old.replaceWith(nw);
      /* THE POPCARDS MUST TRAVEL WITH THE WRAP. They sit OUTSIDE div.wrap and
         every page numbers its cards from pc1, so a swap that left them behind
         made `popovertarget="pc1"` on the ARRIVING page resolve to the page we
         just left: change page, click a chip, read the previous page's
         evidence. JL 260807, screenshot of QBt5 showing QBt4's broken key.
         This is the navigation path a reader actually takes; the auto-rebuild
         path in 20-live-refresh.js carries the same two lines. */
      var ncards = doc.querySelector('#popcards');
      var ocards = document.querySelector('#popcards');
      if (ncards && ocards) { ocards.replaceWith(ncards); }
      document.title = doc.title || document.title;
      if (push) history.pushState({ board: 1 }, '', url);
      /* A SWAP LEAVES THE DOCUMENT'S OWN STAMP BEHIND. The pane's refresh poll
         compares this document's `__paneStamp` against the server's ETag, and
         after a swap that stamp still describes the page we just LEFT, so the
         next tick would see a difference and reload the frame we were trying
         not to reload. Rebase it from the response we just read. */
      try {
        var et = r.headers.get('etag');
        if (et && window.__paneRebase) window.__paneRebase(et);
      } catch (e) {}
      /* and tell the shell, so the address bar and the strip follow a swap the
         same way they follow a real navigation */
      try { if (parent !== window && parent.__boardMirror) parent.__boardMirror(); } catch (e) {}
      window.scrollTo(0, 0);
      if (window.__boardRewire) window.__boardRewire();
      window.dispatchEvent(new CustomEvent('board:updated'));
    } catch (e) {
      location.href = url;          // a failed swap must still navigate
    } finally {
      busy = false;
      if (pending) { var p = pending; pending = null; go(p[0], p[1]); }
    }
  }

  document.addEventListener('click', function (e) {
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button) return;
    var a = e.target.closest && e.target.closest('a');
    if (!samesite(a)) return;
    e.preventDefault();
    go(a.href, true);
  });

  window.addEventListener('popstate', function () { go(location.href, false); });
  /* the index pane calls this instead of navigating this frame (QD5, 260802) */
  window.__boardGo = go;
})();

/* Sidebar drag-to-resize (JL 260731: "can the left panel be dragged, it feels
   fixed"). Same shape the chat drawer uses for --chatw: one CSS variable, a
   handle on the edge that sets it, and the width remembered per machine.
   Pure enhancement, so with scripts off the sidebar keeps its default width. */
(function () {
  var KEY = 'board-sidebar-width';
  function setW(px) {
    px = Math.max(150, Math.min(px, Math.round(window.innerWidth * 0.6)));
    document.documentElement.style.setProperty('--sbw', px + 'px');
    try { localStorage.setItem(KEY, String(px)); } catch (e) {}
  }
  var saved = parseInt(localStorage.getItem(KEY) || '', 10);
  if (saved) setW(saved);
  function wire() {
    var rz = document.querySelector('.sbrz');
    if (!rz || rz.dataset.wired) return;
    rz.dataset.wired = '1';
    rz.addEventListener('pointerdown', function (e) {
      e.preventDefault();
      rz.setPointerCapture(e.pointerId);
      document.body.style.userSelect = 'none';
      var move = function (ev) { setW(ev.clientX); };
      var up = function () {
        rz.removeEventListener('pointermove', move);
        rz.removeEventListener('pointerup', up);
        rz.removeEventListener('pointercancel', up);
        document.body.style.userSelect = '';
      };
      rz.addEventListener('pointermove', move);
      rz.addEventListener('pointerup', up);
      rz.addEventListener('pointercancel', up);
    });
    // double-click the handle to snap back to the default
    rz.addEventListener('dblclick', function () {
      document.documentElement.style.removeProperty('--sbw');
      try { localStorage.removeItem(KEY); } catch (e) {}
    });
  }
  wire();
  window.addEventListener('board:updated', wire);   // survives a live swap
})();
