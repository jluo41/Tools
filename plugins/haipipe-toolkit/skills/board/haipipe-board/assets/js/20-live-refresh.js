
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
            /* SURGICAL UPDATES (JL 260801: "只更新这个配置的一小部分",
               "我一旦改了之后，我想看到这个变化是 immediate 的变化").

               A full reload is the only thing that can destroy a running
               terminal, so it is now the last resort rather than the first
               move, and the two assets are handled apart:

                 CSS changed  → swap the <link>. Instant, and nothing in the
                                page even notices; no reload, ever.
                 JS  changed  → cannot be hot-swapped safely, so reload, but
                                NEVER while a terminal or a turn is live. The
                                badge then says so and reloads the moment that
                                work ends, or immediately if you click it.

               The old code used one stamp for both, so a CSS tweak reloaded the
               page and took the terminal with it, and a 90-second hard cap
               reloaded even with a terminal open. Both are gone. */
            var newCss = (doc.querySelector('meta[name="board-css"]') || {}).content;
            var myCss = (document.querySelector('meta[name="board-css"]') || {}).content;
            if (newCss && myCss && newCss !== myCss) {
              var link = document.querySelector('link[rel="stylesheet"][href*="board.css"]');
              if (link) {
                var href = link.getAttribute('href').split('?')[0] + '?v=' + newCss;
                var fresh = link.cloneNode();
                fresh.setAttribute('href', href);
                /* load the new sheet BEFORE dropping the old one, or the page
                   flashes unstyled for a frame */
                fresh.onload = function () { if (link.parentNode) link.remove(); };
                link.parentNode.insertBefore(fresh, link.nextSibling);
                var m = document.querySelector('meta[name="board-css"]');
                if (m) m.content = newCss;
              }
            }

            var newJs = (doc.querySelector('meta[name="board-js"]') || {}).content;
            var myJs = (document.querySelector('meta[name="board-js"]') || {}).content;
            if (newJs && myJs && newJs !== myJs) {
              /* RELOAD, even with a terminal open (JL 260801: "你能够把这个
                 reload 变成自动 reload 吗... 哪怕我打开 terminal TUI 的时候").

                 This was deferred for a while because a reload used to destroy
                 the terminal. It no longer does, and each part of that is now
                 held up by its own check:
                   · the PTY is PARKED, not killed, so the process survives
                   · the drawer comes back in TUI mode and reattaches to it
                   · the ring replay repaints at THIS browser's size, so the
                     screen is not shredded
                   · a half-typed prompt lives in the CLI process, not in the
                     page, so it is still there afterwards
                 The badge stays for the moment it takes, so the reload is
                 explained rather than mysterious. */
              var bar = document.getElementById('lrf-hold');
              if (!bar) {
                bar = document.createElement('div');
                bar.id = 'lrf-hold'; bar.className = 'lrf';
                document.body.appendChild(bar);
              }
              bar.textContent = '↻ new board code · reloading…';
              /* remember the caret so the reattached terminal gets it back */
              try {
                sessionStorage.setItem('board-refocus',
                  (window.__boardTermFocused && window.__boardTermFocused()) ? 'term' : '');
              } catch (e) {}
              location.reload();
              return;
            }

            var nw = doc.querySelector('div.wrap');
            var old = document.querySelector('div.wrap');
            if (!nw || !old) return;
            var y = window.scrollY;
            /* Remember the caret BEFORE anything moves it. The hash re-bind
               below focuses the fragment's element, and a reader mid-sentence
               in the terminal or the composer should not pay for a board
               update they did not ask for (JL 260801). */
            var hadTerm = !!(window.__boardTermFocused && window.__boardTermFocused());
            var hadEl = document.activeElement;
            var hadChat = !hadTerm && hadEl && hadEl.closest && hadEl.closest('#chat');
            var selStart = hadChat && 'selectionStart' in hadEl ? hadEl.selectionStart : null;
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
            /* ...and put it back, after every one of those has had its turn. */
            if (hadTerm && window.__boardTermFocus) {
              window.__boardTermFocus();
            } else if (hadChat && hadEl && document.contains(hadEl)) {
              try {
                hadEl.focus({ preventScroll: true });
                if (selStart !== null && 'setSelectionRange' in hadEl)
                  hadEl.setSelectionRange(selStart, selStart);
              } catch (e) {}
            }
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
  /* QD5 · IN A PANE, A FRAME REFRESHES ITSELF.
     The swap above exists to keep a drawer and a terminal alive inside the one
     document that held everything. A pane holds one of those things and nothing
     else, so the honest update is a real reload of this frame — the browser
     rebuilds the document correctly instead of us patching it, and no other pane
     can even observe it.

     It asks about ITSELF, which is the whole difference from the 4000 ms poll
     this replaces: that one ran in a document carrying the rail, the page and
     the chat, so its answer had to be surgery. Here a HEAD on our own URL is the
     complete question, so it can be asked often and answered by reloading.

     The chat pane never asks. It is the one frame whose whole value is that it
     is NOT interrupted, and a terminal mid-command is exactly what a reload
     would take. Everything the shell knows about refreshing is now this. */
  if (window.__boardPane) {
    window.__boardRefresh = function () { location.reload(); };
    if (window.__boardPane === 'chat') return;
    /* THE BASELINE IS THIS DOCUMENT, not the first answer we happen to get.
       Asking once and keeping that as "current" looks equivalent and is not:
       an edit that lands between this document loading and the first tick is
       then adopted as the baseline, and the frame sits on the old page forever
       while believing it is fresh. `document.lastModified` is the timestamp of
       the response this frame is ACTUALLY showing, so it cannot drift. */
    /* Compare the ETag, which the server sets from the file's mtime in
       NANOSECONDS. `Last-Modified` is whole seconds, so an edit landing in the
       same second as this document was served looks identical to it and the
       frame sits stale forever believing it is current — narrow, but this board
       is rebuilt in bursts and it was hit (260802). The timestamp stays as the
       fallback for anything that does not send a tag. */
    var tag = window.__paneStamp || '';
    var mine = Date.parse(document.lastModified);
    setInterval(function () {
      if (document.hidden) return;
      fetch(location.href, { method: 'HEAD', cache: 'no-store' })
        .then(function (h) {
          var t = h.headers.get('etag');
          if (tag && t) { if (t !== tag) location.reload(); return; }
          var lm = Date.parse(h.headers.get('last-modified') || '');
          if (!lm || !mine) return;
          if (lm !== mine) location.reload();   // nothing is remembered, so a
        })                                      // dropped reload just retries
        .catch(function () {});
    }, 800);
    return;
  }
  setInterval(tick, 4000);
})();