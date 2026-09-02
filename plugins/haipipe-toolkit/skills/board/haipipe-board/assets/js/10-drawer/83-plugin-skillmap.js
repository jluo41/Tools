/* 🛠 Skill map · the page's citations into the SKILL tree (bibex's twin).
 *
 * WHAT THIS FILE OWNS, one thing: WHERE the map's view lives and which door
 * writes it. The store, the seed-scan, the drag-rank, and the pen all live
 * server-side in live/skillmap.py; the view carries its own controls, so
 * this entry only names the saved view and the refresh door — the same
 * split the bibex entry holds.
 *
 * Registered with the `tab: {url, write}` spec (haipipe-plugin), so the
 * shell builds the 🛠 tab without being edited.
 */
(function () {
  'use strict';

  function pageFile(page) {
    return (page && page.getAttribute('data-file')) || '';
  }

  function board() {
    try { return boardPath(); } catch (e) { return location.pathname; }
  }

  /* folded page -> <dir>/<stem>/skill/<stem>-skill.html; a flat page falls
     back to the board-level skill/ home, the same fork every plugin takes. */
  function savedUrl(page) {
    var f = pageFile(page);
    if (!f) return '';
    var p = decodeURIComponent(location.pathname || '');
    var cut = p.lastIndexOf('/board/');
    if (cut < 0) return '';
    var base = p.slice(0, cut);
    var m = f.match(/^(.*)\/([^\/]+)\/\2\.md$/);
    if (m) return base + '/' + m[1] + '/' + m[2] + '/skill/' + m[2] + '-skill.html';
    var stem = (f.split('/').pop() || '').replace(/\.md$/, '');
    return stem ? base + '/skill/' + stem + '-skill.html' : '';
  }

  function write(page, cb, err) {
    fetch('/_board/skill', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: board(), file: pageFile(page) })
    }).then(function (r) { return r.json(); })
      .then(function (j) {
        if (!j.ok) { err && err(j.err || 'the skill map did not build'); return; }
        cb(j);
      })
      .catch(function (e) { err && err(String(e)); });
  }

  if (window.boardPlugins) {
    window.boardPlugins.register({
      id: 'skill',
      label: '🛠 Skill',
      hint: 'the skills related to this page, ranked by you',
      menu: 'plugin',
      order: 60,
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
