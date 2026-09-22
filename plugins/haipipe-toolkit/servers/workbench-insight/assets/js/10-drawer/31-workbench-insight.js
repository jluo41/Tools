/* 🔎 Insight · one InsightBoard page in its ladder.
 *
 * The tab opens the page-level Insight surface (`/_board/insight`): which
 * register cell this page answers, what it cites, who cites it, its gates
 * and its log.  Board-level Insight (`/_board/insight-board`) is one link up.
 *
 * `applies` KEEPS THE MENU HONEST: only a page laid out the InsightBoard way
 * (`<n>-<letter>-<group>/<ID>-<slug>/<ID>-<slug>.md`, page-type on the DIKW
 * ladder) gets the tab.  The server repeats the authoritative disk check.
 */
(function () {
  'use strict';

  var LADDER = { meta: 1, question: 1, data: 1, information: 1, knowledge: 1, wisdom: 1 };
  var LAYOUT = /^\d+-[A-Z]{1,2}-[^/]+\/[A-Z]{2}\d{2}-[^/]*\/[A-Z]{2}\d{2}-[^/]*\.md$/;

  function pageFile(page) {
    return (page && page.getAttribute('data-file')) || '';
  }

  function isInsightPage(page, type) {
    return !!LADDER[type || ''] && LAYOUT.test(pageFile(page));
  }

  function board() {
    try { return boardPath(); } catch (e) { return location.pathname; }
  }

  function url(page) {
    var file = pageFile(page);
    if (!file) return '';
    return '/_board/insight?path=' + encodeURIComponent(board())
         + '&file=' + encodeURIComponent(file);
  }

  function write(page, cb, err) {
    fetch('/_board/insight', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: board(), file: pageFile(page) })
    }).then(function (r) { return r.json(); })
      .then(function (j) {
        if (!j.ok) { if (err) err(j.err || 'insight surface failed'); return; }
        if (cb) cb(j);
      })
      .catch(function (e) { if (err) err(String(e)); });
  }

  /* The BOARD level of the same workbench: the register of every question on
     this InsightBoard.  Offered from any of the board's pages, because the
     board UI had no way to reach it except a typed URL (JL 260917). */
  function boardUrl() {
    return '/_board/insight-board?path=' + encodeURIComponent(board());
  }

  if (window.boardWorkbenches) {
    window.boardWorkbenches.register({
      id: 'insight-board',
      label: '\u{1F50E} Insight Board',
      hint: 'Every question on this board, by partition: register, answers, runs',
      menu: 'workbench',
      order: 32,
      applies: isInsightPage,
      open: function () { window.open(boardUrl(), '_blank', 'noopener'); },
      tab: { url: boardUrl, write: function (page, cb, err) {
        fetch('/_board/insight-board', {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ path: board(), file: 'board.md' })
        }).then(function (r) { return r.json(); })
          .then(function (j) { if (!j.ok) { if (err) err(j.err || 'insight board failed'); return; } if (cb) cb(j); })
          .catch(function (e) { if (err) err(String(e)); });
      } }
    });
    window.boardWorkbenches.register({
      id: 'insight',
      label: '🔎 Insight',
      hint: 'This page in the Insight ladder: cell, cites, cited by, gates, log',
      menu: 'workbench',
      order: 31,
      applies: isInsightPage,
      open: function (page) {
        var u = url(page);
        if (u) window.open(u, '_blank', 'noopener');
      },
      tab: { url: url, write: write }
    });
  }
})();
