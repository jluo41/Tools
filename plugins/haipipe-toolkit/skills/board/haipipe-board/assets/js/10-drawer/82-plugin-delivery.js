/* 📤 Delivery · ONE tab presents the four delivery lanes (JL 260831).
 *
 * The evidence fold's twin: the delivery/ category (latex · word · slide ·
 * render, the roster's "what leaves the page") gets ONE registry row; the
 * live segmented surface is live/delivery.py (/_board/delivery), whose
 * LaTeX and Word segments press the lanes' own deterministic pens
 * (/_board/latex, /_board/word) on demand. Slides is never auto-built there
 * — its pen is claude -p authoring, reached on the native 🎞 tab's ✨ bar,
 * which STAYS in the shell strip the way Draw does: an authoring tool keeps
 * its surface, a projection folds into its category tab.
 *
 * WHAT THIS FILE OWNS, and it is one thing: the one registry row. This file
 * replaced 82-plugin-exports.js (git mv, 260831): the separate 📜 LaTeX and
 * 📝 Word rows folded in here the way 📚 bibex folded into 🧾 Evidence.
 *
 * Uses the standard plugin tab spec: register with {tab: {url, write}}
 * and the shell builds the right-pane tab — plugin N+1 ships by registering.
 */
(function () {
  'use strict';

  function pageFile(page) {
    return (page && page.getAttribute('data-file')) || '';
  }

  function board() {
    try { return boardPath(); } catch (e) { return location.pathname; }
  }

  function deliveryUrl(page) {
    var f = pageFile(page);
    if (!f) return '';
    return '/_board/delivery?path=' + encodeURIComponent(board())
         + '&file=' + encodeURIComponent(f);
  }

  function deliveryWrite(page, cb, err) {
    fetch('/_board/delivery', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: board(), file: pageFile(page) })
    }).then(function (r) { return r.json(); })
      .then(function (j) {
        if (!j.ok) { err && err(j.err || 'delivery failed'); return; }
        cb(j);
      })
      .catch(function (e) { err && err(String(e)); });
  }

  if (window.boardPlugins) {
    window.boardPlugins.register({
      id: 'delivery',
      label: '📤 Delivery',
      hint: 'latex, word, slides and renders · what leaves the page, one surface',
      menu: 'plugin',
      order: 40,
      /* Any page with a source file: an unbuilt lane still opens, and the
         🏠 segment says what exists before anything is compiled. */
      applies: function (page) { return !!pageFile(page); },
      open: function (page) {
        var u = deliveryUrl(page);
        if (u) window.open(u, '_blank', 'noopener');
      },
      tab: { url: deliveryUrl, write: deliveryWrite }
    });
  }
})();
