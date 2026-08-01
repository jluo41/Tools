
/* ── Pages sidebar: toggle, per-board persistence, active row (JL 260731) ── */
(function () {
  var sb = document.getElementById('sidebar');
  var bt = document.getElementById('sbtoggle');
  if (!sb || !bt) return;
  var key = 'bnav:' + (document.body.dataset.board || '');
  function apply(state) {
    document.body.classList.toggle('nav-open', state === 'open');
    document.body.classList.toggle('nav-closed', state === 'closed');
  }
  try {
    var saved = localStorage.getItem(key);
    if (saved) apply(saved);
  } catch (e) {}
  bt.addEventListener('click', function () {
    var state = sb.getBoundingClientRect().right > 30 ? 'closed' : 'open';
    apply(state);
    try { localStorage.setItem(key, state); } catch (e) {}
  });
  /* On narrow screens the rail overlays the text: a jump closes it (not
     persisted, so a wide screen later still opens by default). */
  sb.addEventListener('click', function (e) {
    var x = e.target.closest('.sb-x');
    if (x) {
      /* The hidden ▸ at the row's end toggles that page's outline
         (JL 260731); the accordion holds: at most one outline open. */
      e.preventDefault();
      var row = x.closest('a.sb-p,a.sb-top');
      var o = row && sb.querySelector(
        '.sb-out[data-out="' + (row.getAttribute('href') || '').slice(1) + '"]');
      var was = o && o.classList.contains('open');
      sb.querySelectorAll('.sb-out.open').forEach(function (q) {
        q.classList.remove('open');
      });
      if (o && !was) o.classList.add('open');
      return;
    }
    var p = e.target.closest('a.sb-p,a.sb-top');
    if (p && p.getAttribute('href') === location.hash) {
      /* Re-clicking the open page's row returns to its top (JL 260731);
         a cross-page click already lands at the top via :target. */
      e.preventDefault();
      var page = document.getElementById(location.hash.slice(1));
      if (page) page.scrollIntoView({ block: 'start' });
      return;
    }
    if (e.target.closest('a') && window.innerWidth < 1150) apply('closed');
  });
  function mark() {
    var want = location.hash || '#top';
    var on = null;
    sb.querySelectorAll('a.sb-top,a.sb-g,a.sb-p').forEach(function (a) {
      var hit = a.getAttribute('href') === want;
      a.classList.toggle('on', hit);
      if (hit) on = a;
    });
    /* Accordion (QB2a, JL 260731): only the open page's outline shows. */
    sb.querySelectorAll('.sb-out.open').forEach(function (o) {
      o.classList.remove('open');
    });
    var out = on && sb.querySelector('.sb-out[data-out="' + want.slice(1) + '"]');
    if (out) out.classList.add('open');
    if (on) on.scrollIntoView({ block: 'nearest' });
  }
  /* An outline row opens its page (the anchor's own navigation), then opens
     and scrolls to the section once :target has applied. */
  var SEL = { diagram: 'details.diagram-section', content: 'details.sect.content',
              items: 'details.sect.goal', now: 'details.sect.now',
              files: 'details.sect.fls',
              /* the Index's own components (QB2a): #top is the wrap, so the
                 same page.querySelector path resolves them */
              map: 'details.board-map', status: 'details.board-status',
              pages: '#qlist', activity: '#activity' };
  sb.addEventListener('click', function (e) {
    var a = e.target.closest('a.sb-s,a.sb-ss');
    if (!a) return;
    var pid = (a.getAttribute('href') || '').slice(1);
    setTimeout(function () {
      var page = document.getElementById(pid);
      if (!page) return;
      var el = SEL[a.dataset.k] ? page.querySelector(SEL[a.dataset.k]) : null;
      if (el && a.dataset.div !== undefined) {
        var divs = Array.prototype.filter.call(el.children, function (x) {
          return x.matches && x.matches('details.csec') &&
                 x.className.indexOf('display') < 0;
        });
        var d = divs[+a.dataset.div];
        if (d) { el.open = true; d.open = true; el = d; }
      } else if (el && a.dataset.t) {
        /* a non-Content subsection (### Decision Now …) is found by its
           rendered .sh heading text */
        var m = a.dataset.t.trim().toLowerCase();
        var hs = el.querySelectorAll('.sh');
        for (var i = 0; i < hs.length; i++) {
          if (hs[i].textContent.trim().toLowerCase().indexOf(m) === 0) {
            el.open = true;
            el = hs[i];
            break;
          }
        }
      }
      if (el) {
        if (el.tagName === 'DETAILS') el.open = true;
        el.scrollIntoView({ block: 'start' });
      } else {
        page.scrollIntoView({ block: 'start' });
      }
    }, 80);
  });
  window.addEventListener('hashchange', mark);
  mark();
})();