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

  /* A compact Outline token belongs to a precise element inside the detailed
     Outline workspace. Run tokens land on the actual Runs element; Evidence
     chips land on their Evidence Workspace item card; Feedback tokens land on
     their Context Workspace record. Keep the complete route in one URL so an
     already-open Outline frame cannot consume partial state. */
  document.addEventListener('click', function (event) {
    var link = event.target.closest && event.target.closest('a[data-outline-focus]');
    if (!link) return;
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey ||
        event.altKey) return;
    var page = link.closest('section.slide.q')
            || (window.boardPlugins && window.boardPlugins.livePage());
    var focus = link.getAttribute('data-outline-focus') || '';
    var run = link.getAttribute('data-outline-run') || '';
    var lens = link.getAttribute('data-outline-lens') || (run ? 'workspace' : 'div');
    /* The Evidence Workspace segment is part of the destination, not a guess
       made later from whether a Run was named: items for an Evidence chip,
       runs for a Run token. */
    var seg = link.getAttribute('data-outline-seg') || '';
    var url = outlineUrl(page);
    if (!url) return;
    event.preventDefault();
    /* This link is not Page navigation.  The later generic same-site router
       would otherwise also consume the same click, swap the Page frame to the
       /_board/outline response, and make the shell re-aim Outline at its
       default URL.  That second route erases lens/focus/run on both touch and
       mouse input. */
    event.stopImmediatePropagation();
    /* Carry the whole request in ONE value.  The old localStorage hand-off
       could be consumed by the already-open Outline frame just before the
       shell rebuilt that frame; the replacement then opened at its default
       Bullet Workspace with no Run left to focus. */
    var direct = url + '&lens=' + encodeURIComponent(lens);
    if (seg) direct += '&seg=' + encodeURIComponent(seg);
    if (focus) direct += '&focus=' + encodeURIComponent(focus);
    if (run) direct += '&run=' + encodeURIComponent(run);
    try {
      if (parent !== window && typeof parent.__boardShowTab === 'function') {
        parent.__boardShowTab('outline', direct);
        return;
      }
    } catch (e) {}
    window.location.assign(direct);
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
