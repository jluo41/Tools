/* 🧭 Outline · the page re-read per division, the rail's SECOND surface.
 *
 * THE GAP IT CLOSES (JL 260816): a page is grouped by section kind — all
 * Content, then all Aims, then all States — so nothing shows one division
 * beside ITS aims, ITS ticks, and ITS state receipts. This flips the axis:
 * one card per Content division, everything belonging to it inside, plus a
 * 🚦 lens that buckets every aim into ⬜ open and ✅ done.
 *
 * SECOND because this file sorts at 07-, right after 📂 folder: registration
 * order is asset sort order, which is the rail's order. The two are twins —
 * 📂 shows what the page's FOLDER holds, 🧭 what its PROSE holds — and both
 * are live meta-surfaces with no subfolder and no roster row.
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

  if (window.boardPlugins) {
    window.boardPlugins.register({
      id: 'outline',
      label: '🧭 Outline',
      hint: 'each Content division with its own aims, ticks, and states',
      menu: 'plugin',
      /* Every page has prose, so unlike 📂 this applies flat or folded. */
      applies: function (page) { return !!pageFile(page); },
      open: function (page) {
        var u = outlineUrl(page);
        if (u) window.open(u, '_blank', 'noopener');
      },
      tab: { url: outlineUrl, write: write }
    });
  }
})();
