  if (!b) return;
  // The heading is now the section's own <summary>, so a click here would also
  // fold the section. Expand-all must not do that (JL 260725).
  ev.preventDefault();
  ev.stopPropagation();
  var sec = b.closest('.sect, .col, .f');
  if (!sec) return;
  var open = b.getAttribute('data-open') !== '1';
  sec.querySelectorAll('details.it').forEach(function (d) { d.open = open; });
  b.setAttribute('data-open', open ? '1' : '0');
  var lbl = b.querySelector('.lbl');
  if (lbl) lbl.textContent = open ? 'collapse all' : 'expand all';
});

/* Read-only sentence context; the next two files continue this scope. */
(function () {
  function sentenceText(p) {
    var c = p.cloneNode(true);
    // Span-card labels are authored words, so retain them when copying.
    c.querySelectorAll('button.chip.card.span').forEach(function (b) {
      b.parentNode.replaceChild(document.createTextNode(b.textContent), b);
    });
    c.querySelectorAll('.cmk,.sbz,.sbadge,.cv,.schatbar,button,input,select,textarea')
      .forEach(function (x) { x.remove(); });
    return c.textContent.replace(/\s+/g, ' ').trim();
  }
  window.__boardSentenceText = sentenceText;
