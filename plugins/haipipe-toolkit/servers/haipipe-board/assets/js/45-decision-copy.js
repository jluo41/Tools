/* A hidden ⧉ on every Decision Now row (JL 260802: "could you give a hidden
   copy button so I can copy the decision easier?").

   A decision row is the one block on a page a person routinely moves OUT of the
   board: into a chat, a message, a commit. Copying it by hand means dragging
   across six wrapped lines and picking up the checkbox glyph with them.

   Hidden the same way the heading rail is: absent until the row is hovered or
   something inside it takes focus, so a page at rest still reads as a document.
   Keyboard users get it from focus, which is why this is not a :hover-only rule.

   The clipboard gets the row as PLAIN TEXT with the ☐/☑ box dropped, because the
   box is the page's state and means nothing once the text is somewhere else. */
(function () {
  'use strict';

  function rowText(row) {
    /* textContent, NOT innerText. innerText reads LAID-OUT text, and a decision
       row lives inside `details.it` nested in `details.sect`, both shut on load.
       Nothing is rendered, so innerText returns '' and the button cheerfully
       copies an empty string while still flashing \u2713. Caught by clicking it
       (JL 260731: "did you clicked it yourself?"), never by reading the markup.

       textContent ignores layout but also drops every line break, so block
       boundaries are re-inserted on a DETACHED clone first. */
    var body = row.querySelector('.itw') || row;
    var clone = body.cloneNode(true);
    var blocks = clone.querySelectorAll('div,p,br,summary,li,tr');
    Array.prototype.forEach.call(blocks, function (el) {
      if (el.parentNode) { el.parentNode.insertBefore(document.createTextNode('\n'), el); }
    });
    return (clone.textContent || '')
      .replace(/\u00a0/g, ' ')
      .split('\n')
      .map(function (l) { return l.replace(/\s+/g, ' ').trim(); })
      .filter(function (l, i, a) { return l || (i > 0 && a[i - 1]); })
      .join('\n')
      .trim();
  }

  function copy(btn, text) {
    var done = function () {
      var was = btn.textContent;
      btn.textContent = '✓';
      setTimeout(function () { btn.textContent = was; }, 1200);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, function () { fallback(text, done); });
    } else {
      fallback(text, done);
    }
  }

  function fallback(text, done) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.cssText = 'position:fixed;top:-1000px;left:-1000px';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); done(); } catch (e) {}
    document.body.removeChild(ta);
  }

  function isDecisionRow(row) {
    /* Only rows under `Decision Now`. Every other `- [ ]` on a board is a legacy
       checklist item, and putting the affordance on those would decorate
       hundreds of rows nobody moves anywhere.

       The heading is NOT a sibling: a `###` inside States renders as
       `details.csec > summary` with the rows in a following `div.cbody`, so this
       climbs to the owning `details` and reads its own summary. A first version
       walked previousElementSibling for a `.sh` and matched nothing, which is
       invisible in the markup and obvious the moment you open the page. */
    var host = row.closest ? row.closest('details.csec') : null;
    var head = host && host.querySelector(':scope > summary');
    if (head) { return /decision now/i.test(head.textContent || ''); }
    /* Fallback for a flat render, where `###` becomes a plain `div.sh`. */
    var n = row.previousElementSibling;
    while (n) {
      if (n.classList && n.classList.contains('sh')) {
        return /decision now/i.test(n.textContent || '');
      }
      n = n.previousElementSibling;
    }
    return false;
  }

  function wire(root) {
    var rows = (root || document).querySelectorAll('.ck');
    Array.prototype.forEach.call(rows, function (row) {
      if (row.__dcopy || !isDecisionRow(row)) { return; }
      row.__dcopy = true;
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'dcopy';
      b.textContent = '⧉';
      b.title = 'Copy this decision as plain text';
      b.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        copy(b, rowText(row));
      });
      row.appendChild(b);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { wire(); });
  } else {
    wire();
  }
  /* The live layer re-renders sections in place, so re-wire after a refresh. */
  window.__boardWireDecisionCopy = wire;
})();
