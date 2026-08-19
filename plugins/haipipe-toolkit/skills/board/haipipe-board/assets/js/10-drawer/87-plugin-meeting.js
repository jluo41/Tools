/* 🗣 Meeting · a page's own kept record of a conversation (QPf14).
 *
 * WHAT THIS FILE OWNS, one thing: WHERE the meeting view lives and which
 * door writes it. Listing kept meetings and landing a new one both live
 * server-side in live/meeting.py; this entry only names the saved view and
 * the refresh door, the same split every plugin holds.
 */
(function () {
  'use strict';

  function pageFile(page) {
    return (page && page.getAttribute('data-file')) || '';
  }

  function board() {
    try { return boardPath(); } catch (e) { return location.pathname; }
  }

  function savedUrl(page) {
    var f = pageFile(page);
    if (!f) return '';
    var p = decodeURIComponent(location.pathname || '');
    var cut = p.lastIndexOf('/board/');
    if (cut < 0) return '';
    var base = p.slice(0, cut);
    var m = f.match(/^(.*)\/([^\/]+)\/\2\.md$/);
    if (m) return base + '/' + m[1] + '/' + m[2] + '/meeting/' + m[2] + '-view.html';
    var stem = (f.split('/').pop() || '').replace(/\.md$/, '');
    return stem ? base + '/meeting/' + stem + '-view.html' : '';
  }

  function write(page, cb, err) {
    fetch('/_board/meeting', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: board(), file: pageFile(page) })
    }).then(function (r) { return r.json(); })
      .then(function (j) {
        if (!j.ok) { err && err(j.err || 'the meeting view did not build'); return; }
        cb(j);
      })
      .catch(function (e) { err && err(String(e)); });
  }

  if (window.boardPlugins) {
    window.boardPlugins.register({
      id: 'meeting',
      label: '🗣 Meeting',
      hint: "this page's own kept meeting notes",
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
