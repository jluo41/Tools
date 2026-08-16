/* ↕ A BOTTOM PANEL CAN BE DRAGGED TALLER OR SHORTER (JL 260816: "我好像没有办法按照
 * 上下的幅度去 change 这个 workflow split size").
 *
 * The shell's three columns each got a hairline grabber the day the split shipped;
 * the bottom panels never did. They opened at a fixed 58vh, which is wrong in both
 * directions: a four-phase index wants a third of that, and a run with a long trail
 * wants two thirds. A surface whose size the reader cannot set is a surface that is
 * the wrong size most of the time.
 *
 * ONE OWNER, BOTH PANELS. #wfpanel (Labeling) and #pfpanel (Page phases) are built
 * by their own plugins; a second copy of drag-and-persist is how the two would
 * drift, so the mechanism lives here and each panel asks for it by one call. The
 * file sorts before both, because asset order is load order.
 *
 * THE GRIP IS THE TOP EDGE, and the panel is anchored at the BOTTOM, so dragging up
 * grows it: `height = startH + (startY - y)`. The height persists per panel id, the
 * way the column widths already persist, so a reader returns to the panel the size
 * they left it. Double-click resets to the default, because a panel dragged to 8px
 * by accident must have a way back that is not devtools.
 */
(function () {
  'use strict';

  var MIN = 120;
  var MAXF = 0.92;          // never swallow the whole viewport

  function clamp(h) {
    return Math.max(MIN, Math.min(window.innerHeight * MAXF, h));
  }

  function apply(panel, h) {
    panel.style.height = clamp(h) + 'px';
    panel.style.maxHeight = 'none';       // the CSS default must yield to a choice
  }

  function reset(panel, key) {
    panel.style.height = '';
    panel.style.maxHeight = '';
    try { localStorage.removeItem(key); } catch (e) {}
  }

  /* Give one bottom panel a top-edge grip. Safe to call twice: the grip is added
     once, so a plugin that rebuilds its panel does not stack handles. */
  window.boardPanelResize = function (panel) {
    if (!panel || panel.querySelector(':scope > .wf-grip')) return;
    var key = 'board-panel-h-' + (panel.id || 'anon');

    try {
      var saved = parseFloat(localStorage.getItem(key));
      if (saved > 0) apply(panel, saved);
    } catch (e) {}

    var grip = document.createElement('div');
    grip.className = 'wf-grip';
    grip.title = 'drag to resize · double-click to reset';
    panel.insertBefore(grip, panel.firstChild);

    grip.addEventListener('pointerdown', function (ev) {
      ev.preventDefault();
      var startY = ev.clientY;
      var startH = panel.getBoundingClientRect().height;
      grip.classList.add('on');
      try { grip.setPointerCapture(ev.pointerId); } catch (e) {}

      function move(e) { apply(panel, startH + (startY - e.clientY)); }
      function up() {
        grip.classList.remove('on');
        grip.removeEventListener('pointermove', move);
        grip.removeEventListener('pointerup', up);
        grip.removeEventListener('pointercancel', up);
        try { localStorage.setItem(key, panel.getBoundingClientRect().height); }
        catch (e) {}
      }
      grip.addEventListener('pointermove', move);
      grip.addEventListener('pointerup', up);
      grip.addEventListener('pointercancel', up);
    });

    grip.addEventListener('dblclick', function () { reset(panel, key); });
  };
})();
