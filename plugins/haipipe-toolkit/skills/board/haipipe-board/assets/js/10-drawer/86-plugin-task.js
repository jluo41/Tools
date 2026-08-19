/* 🗂 Task · the page's citations into the repo's TASK FOLDERS (QPf13).
 *
 * WHAT THIS FILE OWNS, one thing: WHERE the linked-task view lives and which
 * door writes it. The store, the minter, and the pen all live server-side in
 * live/task.py; this entry only names the saved view and the re-mint door,
 * pagex's own split.
 */
(function () {
  'use strict';

  function pageFile(page) {
    return (page && page.getAttribute('data-file')) || '';
  }

  function board() {
    try { return boardPath(); } catch (e) { return location.pathname; }
  }

  /* folded page -> <dir>/<stem>/task/<stem>-view.html; a flat page falls
     back to the board-level task/ home, the same fork every plugin takes. */
  function savedUrl(page) {
    var f = pageFile(page);
    if (!f) return '';
    var p = decodeURIComponent(location.pathname || '');
    var cut = p.lastIndexOf('/board/');
    if (cut < 0) return '';
    var base = p.slice(0, cut);
    var m = f.match(/^(.*)\/([^\/]+)\/\2\.md$/);
    if (m) return base + '/' + m[1] + '/' + m[2] + '/task/' + m[2] + '-view.html';
    var stem = (f.split('/').pop() || '').replace(/\.md$/, '');
    return stem ? base + '/task/' + stem + '-view.html' : '';
  }

  function write(page, cb, err) {
    fetch('/_board/task', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: board(), file: pageFile(page) })
    }).then(function (r) { return r.json(); })
      .then(function (j) {
        if (!j.ok) { err && err(j.err || 'the task view did not build'); return; }
        cb(j);
      })
      .catch(function (e) { err && err(String(e)); });
  }

  if (window.boardPlugins) {
    window.boardPlugins.register({
      id: 'task',
      label: '🗂 Task',
      hint: 'task folders this page is written about, linked live',
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
