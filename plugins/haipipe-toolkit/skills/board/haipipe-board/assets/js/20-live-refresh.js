
/* ── live refresh (QD6, JL 260724) ─────────────────────────────────────────
   "when the chat changed something, refresh automatically — and my chat
   interface is still there." So: NEVER reload. Poll our own Last-Modified
   (both servers send it); when the file changes, fetch the new page and swap
   ONLY div.wrap. Everything the scripts appended to <body> — comment dock,
   chat drawer (mid-stream included), terminal, fab — stays alive. No Node,
   no framework: the drawer survives because it was never inside the content. */
(function () {
  var last = null, busy = false;
  function tick() {
    if (busy || document.hidden) return;
    fetch(location.pathname, { method: 'HEAD', cache: 'no-store' })
      .then(function (h) {
        var lm = h.headers.get('last-modified');
        if (!lm) return;
        if (last === null) { last = lm; return; }
        if (lm === last) return;
        // mid-selection = probably writing a comment on that text; hold the swap
        if (window.getSelection && String(window.getSelection())) return;
        // mid-TYPING（JL 260731「add discussion 打到一半，板一刷，字没了」）：
        // 换掉整个 .wrap 会把正在打的讨论/评论框连字带框一起扔掉。
        // 光标在 .wrap 里的输入框上，或任何框里有没保存的草稿 → 这一轮不换，
        // 4 秒后的下一轮再看。抽屉在 .wrap 外面，不受这条影响。
        var wrapEl = document.querySelector('div.wrap');
        if (wrapEl) {
          var ae = document.activeElement;
          if (ae && /^(TEXTAREA|INPUT)$/.test(ae.tagName) && wrapEl.contains(ae)) return;
          var drafts = wrapEl.querySelectorAll('textarea');
          for (var di = 0; di < drafts.length; di++) {
            if (drafts[di].value && drafts[di].value.trim()) return;
          }
        }
        busy = true;
        return fetch(location.pathname, { cache: 'no-store' })
          .then(function (r) { return r.text(); })
          .then(function (t) {
            var doc = new DOMParser().parseFromString(t, 'text/html');
            // The swap keeps THIS tab's scripts alive forever, so when the
            // BUILD's assets changed (three sessions shipped JS today while a
            // tab sat open, JL 260731), old JS would rewire new markup and die
            // silently — dead ➕ buttons. Different stamp = the one full reload.
            var theirs = doc.querySelector('meta[name="board-assets"]');
            var mine = document.querySelector('meta[name="board-assets"]');
            if (theirs && (!mine || mine.content !== theirs.content)) {
              // ⌨ 开着时不整页 reload（JL 260731「开一会儿它自己退了」的另一半）：
              // 挂个角标等着，终端一关（termView(false)）再 reload。
              // park 让 reload 后也能秒接，但正打着字被刷掉仍然是打断。
              var termOpen = document.body.classList.contains('termon');
              var chatRunning = document.body.classList.contains('chatbusy');
              if (!window.__pendingSince) window.__pendingSince = Date.now();
              // HARD CAP: holding the reload is a courtesy, not a promise. A
              // wedged turn must not pin the tab on stale JS indefinitely.
              var heldTooLong = Date.now() - window.__pendingSince > 90000;
              if ((termOpen || chatRunning) && !heldTooLong) {
                window.__pendingReload = 1;
                if (!document.getElementById('lrf-hold')) {
                  var b = document.createElement('div');
                  b.id = 'lrf-hold'; b.className = 'lrf';
                  b.textContent = termOpen
                    ? '↻ board updated — will reload when the terminal closes'
                    : '↻ board updated — will reload when this turn finishes';
                  document.body.appendChild(b);
                }
                return;
              }
              location.reload();
              return;
            }
            var nw = doc.querySelector('div.wrap');
            var old = document.querySelector('div.wrap');
            if (!nw || !old) return;
            var y = window.scrollY;
            // Carry the OPEN/CLOSED state of every drawer across the swap
            // (JL 260731: "even when a section is open, the change should be
            // smooth"). Without this, replacing div.wrap silently re-collapses
            // whatever the reader had opened, which reads as the page resetting
            // itself under them. Keyed by the drawer's own heading text, so it
            // survives a section moving up or down the page.
            var oldD = old.querySelectorAll('details');
            var openAt = [], openKey = {};
            oldD.forEach(function (d, i) {
              if (!d.open) return;
              openAt.push(i);
              var s = d.querySelector('summary');
              if (s) openKey[s.textContent.replace(/\s+/g, ' ').trim()] = 1;
            });
            old.replaceWith(nw);
            var newD = nw.querySelectorAll('details');
            if (newD.length === oldD.length) {
              // Same shape, so position is the exact identity: editing a
              // sentence does not add or remove drawers.
              openAt.forEach(function (i) { newD[i].open = true; });
            } else {
              // The page gained or lost a drawer, so fall back to the summary
              // text, which survives a section moving.
              newD.forEach(function (d) {
                var s = d.querySelector('summary');
                if (s && openKey[s.textContent.replace(/\s+/g, ' ').trim()]) d.open = true;
              });
            }
            if (window.__boardRewire) window.__boardRewire();
            // RE-BIND :target, or the swap silently returns you to the index.
            // The page router is pure CSS (`body:has(.q:target) .q:target`), and
            // :target binds to an ELEMENT, not to an id. Replacing div.wrap
            // destroys the section the hash pointed at; the fresh one carries the
            // same id but the browser never re-resolves the fragment, so nothing
            // matches, `.q{display:none}` hides every page and the index comes
            // back — with the hash still in the URL, which is why it reads as
            // "the refresh threw me out" rather than as a bug. Only a real
            // navigation re-resolves it; history.replaceState does not.
            // Verified in headless Chrome 260727 (JL).
            var h = location.hash;
            if (h) { location.hash = ''; location.hash = h; }
            window.scrollTo(0, y);
            last = lm;
            var n = document.createElement('div');
            n.className = 'lrf';
            n.textContent = '↻ board updated';
            document.body.appendChild(n);
            window.dispatchEvent(new CustomEvent('board:updated'));
            setTimeout(function () { n.remove(); }, 2200);
          });
      })
      .catch(function () {})
      .then(function () { busy = false; });
  }
  // instant, drawer-preserving refresh — what every former location.reload() now calls
  window.__boardRefresh = function () { if (last === null) last = '0'; tick(); };
  setInterval(tick, 4000);
})();