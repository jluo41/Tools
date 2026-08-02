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
    var body = row.querySelector('.itw');
    var txt = (body || row).innerText || '';
    return txt.replace(/ /g, ' ')
              .split('\n')
              .map(function (l) { return l.replace(/\s+$/, ''); })
              .filter(function (l, i, a) { return l || (i && a[i - 1]); })
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
    /* Only rows under a `### Decision Now` subheading. Every other `- [ ]` on a
       board is a legacy checklist item, and a copy button on those would put the
       affordance on hundreds of rows that nobody moves anywhere. */
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
