/* 🧮 Value · every number the page owes or uses, the rail's THIRD surface.
 *
 * THE GAP IT CLOSES (JL 260819): a probe card is ONE question whose answer
 * holds SEVERAL numbers, and a sentence uses one of them. Citing the card
 * alone could not say which, so a value nobody used looked exactly like one
 * everybody did. The `PP<NN>.v<n>` id fixed the address; this surface is what
 * makes it checkable, joining both ways:
 *
 *   🕳 a number in the prose citing no PP<NN>.v<n>   unsourced
 *   🎈 a value in a card that no sentence cites      answered for nobody
 *
 * THIRD because this file sorts at 08-, right after 🧭 outline: registration
 * order is asset sort order, which is the rail's order.
 *
 * NO STORAGE and NO WRITER (haipipe-plugin-value §🧊): the number already
 * lives in probe/PP<NN>/proof/ with its source, run and sha256. This is a
 * LIVE route rendered from card.md plus the page's own prose on every open,
 * stored nowhere. The POST twin exists only so the shell's
 * `tab: {url, write}` contract holds; it writes nothing.
 */
(function () {
  'use strict';

  function pageFile(page) {
    return (page && page.getAttribute('data-file')) || '';
  }

  function board() {
    try { return boardPath(); } catch (e) { return location.pathname; }
  }

  function valueUrl(page) {
    var f = pageFile(page);
    if (!f) return '';
    return '/_board/value?path=' + encodeURIComponent(board())
         + '&file=' + encodeURIComponent(f);
  }

  function write(page, cb, err) {
    fetch('/_board/value', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: board(), file: pageFile(page) })
    }).then(function (r) { return r.json(); })
      .then(function (j) {
        if (!j.ok) { err && err(j.err || 'value failed'); return; }
        cb(j);
      })
      .catch(function (e) { err && err(String(e)); });
  }

  if (window.boardPlugins) {
    window.boardPlugins.register({
      id: 'value',
      label: '🧮 Values',
      hint: 'every number, where it was read from, and which part uses it',
      menu: 'plugin',
      /* Any page may cite a value, and a page with none renders the empty
       * state rather than vanishing from the rail: an empty cell is a
       * status, never a blank. */
      applies: function (page) { return !!pageFile(page); },
      open: function (page) {
        var u = valueUrl(page);
        if (u) window.open(u, '_blank', 'noopener');
      },
      tab: { url: valueUrl, write: write }
    });
  }
})();
