/* 📂 Folder · the page-folder's own status, registered FIRST on purpose.
 *
 * THE GAP IT CLOSES (JL 260815: "a first item in the plugin to show the
 * content of the page-folder status"): the rail shows the surfaces someone
 * built; this shows what the folder actually HOLDS — which plugins exist,
 * how heavy each is, and whether a DERIVED one (latex, word, bibex, slide,
 * display) now predates the .md it was made from. The folder is the truth;
 * the tabs are surfaces over it; the first tab shows the truth.
 *
 * FIRST because this file sorts at 06-, directly after the registry itself:
 * registration order is asset sort order, which is the rail's order.
 *
 * The URL is a LIVE route, not a saved view: a status written to disk starts
 * aging as it lands, and a stale page about staleness would be absurd. The
 * POST twin exists only so the shell's `tab: {url, write}` contract holds.
 */
(function () {
  'use strict';

  function pageFile(page) {
    return (page && page.getAttribute('data-file')) || '';
  }

  function board() {
    try { return boardPath(); } catch (e) { return location.pathname; }
  }

  function statUrl(page) {
    var f = pageFile(page);
    if (!f) return '';
    return '/_board/folderstat?path=' + encodeURIComponent(board())
         + '&file=' + encodeURIComponent(f);
  }

  function write(page, cb, err) {
    fetch('/_board/folderstat', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: board(), file: pageFile(page) })
    }).then(function (r) { return r.json(); })
      .then(function (j) {
        if (!j.ok) { err && err(j.err || 'folder status failed'); return; }
        cb(j);
      })
      .catch(function (e) { err && err(String(e)); });
  }

  if (window.boardPlugins) {
    window.boardPlugins.register({
      id: 'folder',
      label: '📂 Folder',
      hint: "what this page's folder holds, and what has gone stale",
      menu: 'plugin',
      /* Only a FOLDED page owns a folder; a flat page has nothing to show. */
      applies: function (page) {
        return /^(.*\/)?([^\/]+)\/\2\.md$/.test(pageFile(page));
      },
      open: function (page) {
        var u = statUrl(page);
        if (u) window.open(u, '_blank', 'noopener');
      },
      tab: { url: statUrl, write: write }
    });
  }
})();
