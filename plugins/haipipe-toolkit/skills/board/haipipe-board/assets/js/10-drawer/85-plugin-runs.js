/* ⚙️ Runs · one read-only page surface for allocated local Run → Result pairs.
 *
 * Evidence owns Supporting Runs and unallocated new-* routes. Runs never
 * repeats those declarations: it reads only this page's actual runs/ and
 * results/ pair, then offers the execution detail for each real Run.
 */
(function () {
  'use strict';

  function pageFile(page) {
    return (page && page.getAttribute('data-file')) || '';
  }

  function board() {
    try { return boardPath(); } catch (e) { return location.pathname; }
  }

  function runsUrl(page) {
    var f = pageFile(page);
    if (!f) return '';
    return '/_board/runs?path=' + encodeURIComponent(board())
         + '&file=' + encodeURIComponent(f);
  }

  /* The shell's tab contract requires a write twin.  Runs owns no storage, so
     this POST only returns the same fresh live URL. */
  function write(page, cb, err) {
    fetch('/_board/runs', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: board(), file: pageFile(page) })
    }).then(function (r) { return r.json(); })
      .then(function (j) {
        if (!j.ok) { err && err(j.err || 'runs view failed'); return; }
        cb(j);
      })
      .catch(function (e) { err && err(String(e)); });
  }

  if (window.boardPlugins) {
    window.boardPlugins.register({
      id: 'runs',
      label: '⚙️ Runs',
      hint: 'local Run → Result pairs · read-only',
      menu: 'plugin',
      order: 30,
      /* A page with a source can truthfully show that no local Run has been
         allocated. It must not disappear merely because runs/ is absent. */
      applies: function (page) { return !!pageFile(page); },
      open: function (page) {
        var u = runsUrl(page);
        if (u) window.open(u, '_blank', 'noopener');
      },
      tab: { url: runsUrl, write: write }
    });
  }
})();
