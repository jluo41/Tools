/* 🛠 Skill map · the page's citations into the SKILL tree (bibex's twin).
 *
 * WHAT THIS FILE OWNS, one thing: WHERE the map's view lives and which door
 * writes it. The store, the seed-scan, the drag-rank, and the pen all live
 * server-side in live/skillmap.py; the view carries its own controls, so
 * this entry only names the saved view and the refresh door — the same
 * split the bibex entry holds.
 *
 * The visible surface now lives at 🧭 Outline → Page Records → Skills. The
 * server routes and generated ranked editor remain compatibility machinery;
 * this asset intentionally registers no duplicate top-level tab.
 */
(function () {
  'use strict';

  function pageFile(page) {
    return (page && page.getAttribute('data-file')) || '';
  }

  function board() {
    try { return boardPath(); } catch (e) { return location.pathname; }
  }

  /* folded page -> <dir>/<stem>/outline/skill/<stem>-skill.html; a flat page
     falls back to the board-level outline/skill/ home. */
  function savedUrl(page) {
    var f = pageFile(page);
    if (!f) return '';
    var p = decodeURIComponent(location.pathname || '');
    var cut = p.lastIndexOf('/board/');
    if (cut < 0) return '';
    var base = p.slice(0, cut);
    var m = f.match(/^(.*)\/([^\/]+)\/\2\.md$/);
    if (m) return base + '/' + m[1] + '/' + m[2] + '/outline/skill/' + m[2] + '-skill.html';
    var stem = (f.split('/').pop() || '').replace(/\.md$/, '');
    return stem ? base + '/outline/skill/' + stem + '-skill.html' : '';
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

  // No registry row: Outline embeds the generated view from savedUrl().
})();
