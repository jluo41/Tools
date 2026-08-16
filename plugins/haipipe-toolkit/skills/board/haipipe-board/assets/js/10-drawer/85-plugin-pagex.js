/* 🔗 Pagex · the page's citations into the repo's OTHER PAGES (QPf11).
 *
 * WHAT THIS FILE OWNS, one thing: WHERE the borrow view lives and which door
 * writes it. The store, the minter, the two finding routes, and the pen all
 * live server-side in live/pagex.py; the view carries its own controls, so
 * this entry only names the saved view and the re-mint door — the same split
 * the skill and bibex entries hold.
 *
 * Registered with the `tab: {url, write}` spec (haipipe-plugin), so the shell
 * builds the 🔗 tab without being edited.
 */
(function () {
  'use strict';

  function pageFile(page) {
    return (page && page.getAttribute('data-file')) || '';
  }

  function board() {
    try { return boardPath(); } catch (e) { return location.pathname; }
  }

  /* folded page -> <dir>/<stem>/pagex/<stem>-view.html; a flat page falls
     back to the board-level pagex/ home, the same fork every plugin takes. */
  function savedUrl(page) {
    var f = pageFile(page);
    if (!f) return '';
    var p = decodeURIComponent(location.pathname || '');
    var cut = p.lastIndexOf('/board/');
    if (cut < 0) return '';
    var base = p.slice(0, cut);
    var m = f.match(/^(.*)\/([^\/]+)\/\2\.md$/);
    if (m) return base + '/' + m[1] + '/' + m[2] + '/pagex/' + m[2] + '-view.html';
    var stem = (f.split('/').pop() || '').replace(/\.md$/, '');
    return stem ? base + '/pagex/' + stem + '-view.html' : '';
  }

  function write(page, cb, err) {
    fetch('/_board/pagex', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: board(), file: pageFile(page) })
    }).then(function (r) { return r.json(); })
      .then(function (j) {
        if (!j.ok) { err && err(j.err || 'the borrow view did not build'); return; }
        cb(j);
      })
      .catch(function (e) { err && err(String(e)); });
  }

  if (window.boardPlugins) {
    window.boardPlugins.register({
      id: 'pagex',
      label: '🔗 Pagex',
      hint: 'files this page borrows from other pages, linked live',
      menu: 'plugin',
      applies: function (page) { return !!pageFile(page); },
      open: function (page) {
        write(page, function (j) {
          if (j.url) window.open(j.url + '?plain', '_blank', 'noopener');
        }, function (e) { alert('⚠ ' + e); });
      },
      tab: {
        url: function (page) { return savedUrl(page); },
        write: write
      }
    });
  }
})();
