/* 🏷 Labeling · one right-pane plugin for a Page's optional subjective-label job.
 *
 * The retired version of this file was a bottom workflow inferred from
 * `## States` and offered /label-* commands.  The 0.6 family made canonical
 * receipts authoritative and retired those commands, so this file now owns
 * only the registry row.  plugins/subjective-label/servers/workbench-labeling/labeling.py owns the page: five Spaces (Data,
 * Labeling, Quality, Run, Delivery) and the keyboard Label screen, whose writes
 * go through POST /_board/labeling/act to the subjective-label engine.  Studio
 * Chat opens separately from its header and is never a permanent bottom panel.
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
     that exact address in the presenter request so plugins/subjective-label/servers/workbench-labeling/labeling.py can frame
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

  /* ── Board level (zoom out): every labeling job on this Board ──────────
     It applies on the Board index and on the S-Label-Dash control Page, never
     on a job Page, so the two 🏷 entries are never offered together.  A Board
     that names its job Pages S-Label-* is recognised at once; any other Board
     is recognised after one cheap server probe counts its labeling/ lanes. */
  function isDash(page) { return /(?:^|\/)S-Label-Dash\.md$/.test(pageFile(page)); }
  function isBoardIndex() {
    return !!(document.body && document.body.classList.contains('single')) &&
      !document.querySelector('.wrap section.slide.q');
  }
  function boardApplies(page) {
    if (page) return isDash(page);
    if (!isBoardIndex()) return false;
    return window.__labelingBoardJobs > 0 ||
      !!document.querySelector('a[href*="S-Label-"]');
  }
  function boardURL() {
    return '/_board/labeling-board?path=' + encodeURIComponent(board());
  }
  if (isBoardIndex()) {
    fetch('/_board/labeling-board', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: board() })
    }).then(function (r) { return r.json(); })
      .then(function (j) { if (j && j.ok) window.__labelingBoardJobs = j.jobs || 0; })
      .catch(function () {});
  }

  if (window.boardWorkbenches) {
    window.boardWorkbenches.register({
      id: 'labeling-board',
      label: '🏷 Labeling',
      hint: 'Every labeling job on this Board · click one to open it',
      menu: 'workbench',
      order: 70,
      applies: boardApplies,
      open: function () { window.open(boardURL(), '_blank', 'noopener'); },
      tab: {
        url: function () { return boardURL(); },
        write: function (page, done, fail) {
          fetch('/_board/labeling-board', {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ path: board() })
          }).then(function (r) { return r.json(); })
            .then(function (j) { if (j.ok) done(j); else if (fail) fail(j.err || 'labeling board failed'); })
            .catch(function (e) { if (fail) fail(String(e)); });
        }
      }
    });
    window.boardWorkbenches.register({
      id: 'labeling',
      label: '🏷 Labeling',
      hint: 'Confirm the meaning, then label with the keyboard · Studio Chat opens separately',
      menu: 'workbench',
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
