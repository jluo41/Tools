/* 🧭 Outline · the page re-read per division, the rail's FIRST surface.
 *
 * THE GAP IT CLOSES (JL 260816): a page is grouped by section kind — all
 * Content, then all Aims, then all States — so nothing shows one division
 * beside ITS aims, ITS ticks, and ITS state receipts. This flips the axis:
 * one card per Content division, everything belonging to it inside, plus a
 * 🚦 lens that buckets every aim into ⬜ open and ✅ done.
 *
 * FIRST by explicit Plugin order. Outline owns the Page's process folder and
 * reads Bullet + Evidence together; 📂 Folder is the raw inventory twin.
 *
 * RULE-BASED, never authored (QPf12): the mapping is read from the material
 * (the `### A<n>` group grammar, then the `§N` anchor), so the URL is a LIVE
 * route rendered from the .md on every open and stored nowhere. The POST twin
 * exists only so the shell's `tab: {url, write}` contract holds.
 */
(function () {
  'use strict';

  function pageFile(page) {
    return (page && page.getAttribute('data-file')) || '';
  }

  function board() {
    try { return boardPath(); } catch (e) { return location.pathname; }
  }

  function outlineUrl(page) {
    var f = pageFile(page);
    if (!f) return '';
    return '/_board/outline?path=' + encodeURIComponent(board())
         + '&file=' + encodeURIComponent(f);
  }

  function write(page, cb, err) {
    fetch('/_board/outline', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: board(), file: pageFile(page) })
    }).then(function (r) { return r.json(); })
      .then(function (j) {
        if (!j.ok) { err && err(j.err || 'outline failed'); return; }
        cb(j);
      })
      .catch(function (e) { err && err(String(e)); });
  }

  /* A Run in the compact Page table belongs to the detailed Outline
     workspace.  Keep one public plugin: select Outline, open its Evidence
     Workspace lens, and focus the owning Evidence Item. */
  document.addEventListener('click', function (event) {
    var link = event.target.closest && event.target.closest('a[data-outline-focus]');
    if (!link) return;
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey ||
        event.altKey) return;
    var page = link.closest('section.slide.q')
            || (window.boardPlugins && window.boardPlugins.livePage());
    var focus = link.getAttribute('data-outline-focus') || '';
    var run = link.getAttribute('data-outline-run') || '';
    var url = outlineUrl(page);
    if (!url) return;
    event.preventDefault();
    try {
      localStorage.setItem('board-outline-evidence-focus', focus);
      localStorage.setItem('board-outline-evidence-run', run);
      localStorage.setItem('board-outline-lens', 'workspace');
    } catch (e) {}
    try {
      if (parent !== window && typeof parent.__boardShowTab === 'function') {
        parent.__boardShowTab('outline');
        return;
      }
    } catch (e) {}
    window.location.assign(url + '&lens=workspace&focus=' + encodeURIComponent(focus)
                         + '&run=' + encodeURIComponent(run));
  });

  if (window.boardPlugins) {
    window.boardPlugins.register({
      id: 'outline',
      label: '🧭 Outline',
      hint: 'each Content division with its own aims, ticks, and states',
      menu: 'plugin',
      order: 10,
      /* Every page has prose, so unlike 📂 this applies flat or folded. */
      applies: function (page) { return !!pageFile(page); },
      open: function (page) {
        var u = outlineUrl(page);
        if (u) window.open(u, '_blank', 'noopener');
      },
      tab: { url: outlineUrl, write: write }
    });
    // JL 260818: "how to make the outline be the default plugin when we
    // open it" — a plain FAB click now goes straight here instead of the
    // picker (50-structure.js reads this back through getDefault()).
    window.boardPlugins.setDefault('outline');
  }
})();
