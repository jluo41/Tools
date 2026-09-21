/* 📄 Paper Plugin · the Board-altitude sibling of 🧭 Outline.
 *
 * Outline applies to a Page; this applies to the Board index of a PAPER board,
 * which page_board.py marks with `data-board-dialect="paper"` from board.md's
 * `dialect:` line (JL 260916: "like haipipe-plugin-outline, you should have
 * haipipe-plugin-paper"). No Links key, no per-paper file: the route
 * /_board/paper renders the five Spaces from Markdown on every open.
 * `data-board-paper` (the retired console/ Links key) still opts a board in.
 *
 * The tab is read-only. Its rows route back to the owning Story, Section,
 * Run and receipt records; it keeps no second roster and no second registry.
 */
(function () {
  'use strict';

  function isPaperBoard() {
    var b = document.body;
    if (!b) return false;
    return (b.getAttribute('data-board-dialect') || '').trim() === 'paper'
        || !!(b.getAttribute('data-board-paper') || '').trim();
  }

  function board() {
    try { return boardPath(); } catch (e) { return location.pathname; }
  }

  function paperUrl() {
    if (!isPaperBoard()) return '';
    return '/_board/paper?path=' + encodeURIComponent(board())
         + '&file=' + encodeURIComponent('board.md');
  }

  function isBoardIndex(page) {
    return !page && !!paperUrl() && document.body &&
      document.body.classList.contains('single');
  }

  if (window.boardPlugins) {
    window.boardPlugins.register({
      id: 'paper',
      label: '📄 Paper',
      hint: 'Setup, Ideation, Story, Run, and Delivery spaces',
      menu: 'plugin',
      order: 15,
      applies: isBoardIndex,
      open: function () {
        var url = paperUrl();
        if (url) window.open(url, '_blank', 'noopener');
      },
      tab: {
        url: function () { return paperUrl(); },
        write: function (page, done, fail) {
          var url = paperUrl();
          if (url) done({ ok: true, url: url });
          else if (fail) fail('this Board is not a paper Board (no dialect: paper)');
        }
      }
    });
  }
})();
