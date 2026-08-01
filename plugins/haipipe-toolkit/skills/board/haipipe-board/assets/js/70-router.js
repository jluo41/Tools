/* ── board/ tree navigation (QC9, JL 260731) ───────────────────────────────
   In the tree each page is its own document, so a plain link click is a real
   navigation and a real navigation destroys the chat drawer and the terminal,
   which is the exact failure QD4's parked-outside-the-wrap design exists to
   avoid. So in site mode we intercept internal links, fetch the target, swap
   ONLY div.wrap, and pushState. The drawer never notices it moved.

   With scripts off every link is still an ordinary href, so the tree stays
   fully navigable and the strip-scripts invariant holds. */
(function () {
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
      var r = await fetch(url, { cache: 'no-store' });
      var doc = new DOMParser().parseFromString(await r.text(), 'text/html');
      var nw = doc.querySelector('div.wrap'), old = document.querySelector('div.wrap');
      if (!nw || !old) { location.href = url; return; }
      old.replaceWith(nw);
      document.title = doc.title || document.title;
      if (push) history.pushState({ board: 1 }, '', url);
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
})();

/* Rail drag-to-resize (JL 260731: "can the left panel be dragged, it feels
   fixed"). Same shape the chat drawer uses for --chatw: one CSS variable, a
   handle on the edge that sets it, and the width remembered per machine.
   Pure enhancement, so with scripts off the rail keeps its default width. */
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
