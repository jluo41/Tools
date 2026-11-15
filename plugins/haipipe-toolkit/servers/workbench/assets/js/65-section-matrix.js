
/* ── SECTION MATRIX cells open their page at the named section (QB2). ── */
(function () {
  var bs = document.querySelector('.board-status');
  if (!bs) return;
  var SEL = { outline: 'details.outline-section', content: 'details.sect.content',
              items: 'details.sect.goal', now: 'details.sect.now',
              files: 'details.sect.fls', folds: '.folds' };
  bs.addEventListener('click', function (e) {
    var a = e.target.closest('a[data-k]');
    if (!a) return;
    setTimeout(function () {
      var page = document.getElementById((a.getAttribute('href') || '').slice(1));
      if (!page) return;
      var el = SEL[a.dataset.k] ? page.querySelector(SEL[a.dataset.k]) : null;
      if (el) {
        if (el.tagName === 'DETAILS') el.open = true;
        el.scrollIntoView({ block: 'start' });
      }
    }, 80);
  });
})();
