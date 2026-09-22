/* 🎨 Design · one page-folder-level category surface.
 *
 * The tab is available only for a current `folder-kind: design` Page.  It
 * presents the whole Design Folder and lets the server re-read it live;
 * candidates, Results, Runs, delivery, and adoption keep their own writers.
 */
(function () {
  'use strict';

  function pageFile(page) {
    return (page && page.getAttribute('data-file')) || '';
  }

  function isDesignFolder(page, type) {
    var declared = (page && page.getAttribute('data-folder-kind')) || '';
    /* `type` is retained for pages whose renderer exposes only the generic
       type attribute.  The server repeats the authoritative disk check. */
    return !!pageFile(page) && (declared === 'design' || type === 'design');
  }

  function board() {
    try { return boardPath(); } catch (e) { return location.pathname; }
  }

  function url(page) {
    var file = pageFile(page);
    if (!file) return '';
    return '/_board/design?path=' + encodeURIComponent(board())
         + '&file=' + encodeURIComponent(file);
  }

  function write(page, cb, err) {
    fetch('/_board/design', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: board(), file: pageFile(page) })
    }).then(function (r) { return r.json(); })
      .then(function (j) {
        if (!j.ok) { if (err) err(j.err || 'design surface failed'); return; }
        if (cb) cb(j);
      })
      .catch(function (e) { if (err) err(String(e)); });
  }

  if (window.boardWorkbenches) {
    window.boardWorkbenches.register({
      id: 'design',
      label: '🎨 Design',
      hint: 'Design Items across Goal, Design, Insight, Run, and Delivery Space',
      menu: 'workbench',
      order: 30,
      applies: isDesignFolder,
      open: function (page) {
        var u = url(page);
        if (u) window.open(u, '_blank', 'noopener');
      },
      tab: { url: url, write: write }
    });
  }
})();
