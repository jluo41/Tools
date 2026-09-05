/* 🏷 Labeling · one right-pane plugin for a Page's optional subjective-label job.
 *
 * The retired version of this file was a bottom workflow inferred from
 * `## States` and offered /label-* commands.  The 0.6 family made canonical
 * receipts authoritative and retired those commands, so this file now owns
 * only the registry row.  live/labeling.py owns five receipt-first Workspaces
 * in the upper stage and keeps the page's existing Studio Chat below them.
 */
(function () {
  'use strict';

  function pageFile(page) {
    return (page && page.getAttribute('data-file')) || '';
  }

  function isSurfacePage(page) {
    var file = pageFile(page);
    /* Plugin availability belongs to the Page/Folder, not to whether a job
       already exists or whether the Page chose the specialized labeling Page
       grammar. The control dashboard is the only Page with no per-Page lane. */
    return !!file && !/(?:^|\/)S-Label-Dash\.md$/.test(file);
  }

  function board() {
    try { return boardPath(); } catch (e) { return location.pathname; }
  }

  /* Studio binds Chat to the CURRENT generated Page URL, not board.md.  Keep
     that exact address in the presenter request so live/labeling.py can frame
     the same `?pane=chat` document Studio uses. */
  function pageURL() { return location.pathname; }

  function url(page) {
    var file = pageFile(page);
    if (!file) return '';
    return '/_board/labeling?path=' + encodeURIComponent(board())
         + '&file=' + encodeURIComponent(file)
         + '&page=' + encodeURIComponent(pageURL());
  }

  function write(page, cb, err) {
    fetch('/_board/labeling', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: board(), file: pageFile(page), page: pageURL() })
    }).then(function (r) { return r.json(); })
      .then(function (j) {
        if (!j.ok) { if (err) err(j.err || 'labeling surface failed'); return; }
        cb(j);
      })
      .catch(function (e) { if (err) err(String(e)); });
  }

  if (window.boardPlugins) {
    window.boardPlugins.register({
      id: 'labeling',
      label: '🏷 Labeling',
      hint: 'five artifact workspaces above · Studio Chat always below',
      menu: 'plugin',
      order: 70,
      applies: isSurfacePage,
      open: function (page) {
        var u = url(page);
        if (u) window.open(u, '_blank', 'noopener');
      },
      tab: { url: url, write: write }
    });
  }
})();
