/* 🏷 Labeling · one right-pane plugin for a page-local subjective-label job.
 *
 * The retired version of this file was a bottom workflow inferred from
 * `## States` and offered /label-* commands.  The 0.5 family made canonical
 * receipts authoritative and retired those commands, so this file now owns
 * only the registry row.  live/labeling.py owns the receipt-first surface and
 * embeds the page's existing Studio Chat as transport.
 */
(function () {
  'use strict';

  function pageFile(page) {
    return (page && page.getAttribute('data-file')) || '';
  }

  function isRunPage(page, type) {
    var file = pageFile(page);
    return type === 'labeling' && !!file && !/(?:^|\/)S-Label-Dash\.md$/.test(file);
  }

  function board() {
    try { return boardPath(); } catch (e) { return location.pathname; }
  }

  function url(page) {
    var file = pageFile(page);
    if (!file) return '';
    return '/_board/labeling?path=' + encodeURIComponent(board())
         + '&file=' + encodeURIComponent(file);
  }

  function write(page, cb, err) {
    fetch('/_board/labeling', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: board(), file: pageFile(page) })
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
      hint: 'canonical frontier and gates above · Studio Chat below',
      menu: 'plugin',
      applies: isRunPage,
      open: function (page) {
        var u = url(page);
        if (u) window.open(u, '_blank', 'noopener');
      },
      tab: { url: url, write: write }
    });
  }
})();
