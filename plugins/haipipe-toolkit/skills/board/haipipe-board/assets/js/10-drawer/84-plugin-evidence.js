/* 🧾 Evidence · ONE tab presents the four evidence lanes (JL 260831).
 *
 * "We still have the subfolder for bibex, etc, but we just need one evidence
 * plugin, to present bibex, display, etc." So this file registers ONE row;
 * the live segmented surface is live/evidence.py (/_board/evidence), whose
 * segments press the lanes' own pens (/_board/bibex·probe·display) on demand.
 * Storage, writers and the three human gates stay with the lane contracts.
 *
 * WHAT THIS FILE OWNS, and it is one thing: the one registry row. The
 * surfaces are read-only views built by live/plugview.py (one /_board/<plugin>
 * route each), because both contracts forbid the pane a pen: a display is
 * accepted by a person (QPf5 §3) and a probe is moved by its three hands
 * (QPf9 §3). The view shows units with previews, or cards with states, and an
 * EMPTY plugin shows the contract's ghost scaffold instead of a blank.
 *
 * Same `tab` spec as 82-plugin-exports.js: register with {tab: {url, write}}
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

  /* The saved view, by the plugin contract's one naming rule (see 82's note):
     folded page -> <dir>/<stem>/<plugin>/<stem>-view.html; a flat page falls
     back to the board-level <board>/<plugin>/ home. */
  function savedUrl(page, plugin) {
    var f = pageFile(page);
    if (!f) return '';
    var p = decodeURIComponent(location.pathname || '');
    var cut = p.lastIndexOf('/board/');
    if (cut < 0) return '';
    var base = p.slice(0, cut);
    var m = f.match(/^(.*)\/([^\/]+)\/\2\.md$/);
    if (m) return base + '/' + m[1] + '/' + m[2] + '/' + plugin + '/' + m[2] + '-view.html';
    var stem = (f.split('/').pop() || '').replace(/\.md$/, '');
    return stem ? base + '/' + plugin + '/' + stem + '-view.html' : '';
  }

  function writer(route) {
    return function (page, cb, err) {
      fetch('/_board/' + route, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: board(), file: pageFile(page) })
      }).then(function (r) { return r.json(); })
        .then(function (j) {
          if (!j.ok) { err && err(j.err || 'the ' + route + ' view failed'); return; }
          cb(j);
        })
        .catch(function (e) { err && err(String(e)); });
    };
  }

  function opener(write) {
    return function (page) {
      write(page, function (j) {
        if (j.url) window.open(j.url, '_blank', 'noopener');
      }, function (e) { alert('⚠ ' + e); });
    };
  }

  function evidenceUrl(page) {
    var f = pageFile(page);
    if (!f) return '';
    return '/_board/evidence?path=' + encodeURIComponent(board())
         + '&file=' + encodeURIComponent(f);
  }

  function evidenceWrite(page, cb, err) {
    fetch('/_board/evidence', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: board(), file: pageFile(page) })
    }).then(function (r) { return r.json(); })
      .then(function (j) {
        if (!j.ok) { err && err(j.err || 'evidence failed'); return; }
        cb(j);
      })
      .catch(function (e) { err && err(String(e)); });
  }

  if (window.boardPlugins) {
    window.boardPlugins.register({
      id: 'evidence',
      label: '🧾 Evidence',
      hint: 'citations, cards, values and displays · one surface, four lanes',
      menu: 'plugin',
      /* Any page with a source file: an empty lane still opens, and the
         ghost scaffold it shows is the contract teaching itself. */
      applies: function (page) { return !!pageFile(page); },
      open: function (page) {
        var u = evidenceUrl(page);
        if (u) window.open(u, '_blank', 'noopener');
      },
      tab: { url: evidenceUrl, write: evidenceWrite }
    });
  }
})();
