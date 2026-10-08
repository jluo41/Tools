
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
  /* On narrow screens the sidebar overlays the text: a jump closes it (not
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
    /* WHERE AM I, asked of the DOCUMENT rather than of the URL.

       The sidebar was written for the one-file board, where every page is a
       section and `location.hash` names the open one. In the tree a page is
       its own file with no hash at all and the row hrefs are file paths, so
       the comparison matched nothing: no row was highlighted and no section
       outline ever opened (JL 260801). That is the same assumption QC9 took
       out of the drawer; the sidebar kept it.

       Three kinds of file, answered in order, because a wrong order lets the
       Index row win on a group page:
         a page   -> the one `section.q` in the document, matched by data-page
         a group  -> the row whose href IS this file
         neither  -> the Index row

       `data-page` exists so the match survives BOTH packagings: the id is the
       same, the href is not. The drawer's docPage() is reused, never copied. */
    var doc = window.__boardDocPage && window.__boardDocPage();
    var here = location.pathname.split('/').pop();
    var on = null, want = null;

    if (doc) {
      want = '#' + doc.id;
    } else if (document.querySelector('section.q')) {
      want = location.hash || '#top';            // the one-file board
    }
    if (want) {
      sb.querySelectorAll('a.sb-top,a.sb-g,a.sb-p').forEach(function (a) {
        var id = a.getAttribute('data-page');
        var hit = id ? ('#' + id) === want : a.getAttribute('href') === want;
        a.classList.toggle('on', hit);
        if (hit) on = a;
      });
    }
    if (!on && here) {                           // a group file in the tree
      sb.querySelectorAll('a.sb-g').forEach(function (a) {
        var hit = (a.getAttribute('href') || '').split('/').pop() === here;
        a.classList.toggle('on', hit);
        if (hit) { on = a; want = null; }
      });
    }
    if (!on) {                                   // the Index
      var top = sb.querySelector('a.sb-top');
      if (top) { top.classList.add('on'); on = top; want = '#top'; }
    }
    /* Accordion (QB2a, JL 260731): only the open page's outline shows. */
    sb.querySelectorAll('.sb-out.open').forEach(function (o) {
      o.classList.remove('open');
    });
    var out = want && sb.querySelector('.sb-out[data-out="' + want.slice(1) + '"]');
    if (out) out.classList.add('open');
    if (on) on.scrollIntoView({ block: 'nearest' });
  }
  /* An outline row opens its page (the anchor's own navigation), then opens
     and scrolls to the section once :target has applied. */
  var SEL = { outline: 'details.outline-section', content: 'details.sect.content',
              items: 'details.sect.goal', now: 'details.sect.now',
              files: 'details.sect.fls',
              /* the Index's own components (QB2a): #top is the wrap, so the
                 same page.querySelector path resolves them */
              map: 'details.board-map', status: 'details.board-status',
              pages: '#qlist', activity: '#activity' };
  /* Wait for the page element to EXIST rather than guessing how long a
     navigation takes. In the tree the row's click is intercepted by the router,
     which fetches the file and swaps div.wrap; 80ms was a race it usually lost,
     and losing it silently did nothing at all. */
  function afterPage(pid, fn, tries) {
    var page = document.getElementById(pid);
    if (page) { fn(page); return; }
    if ((tries || 0) > 40) return;                 // ~2.5s, then give up quietly
    setTimeout(function () { afterPage(pid, fn, (tries || 0) + 1); }, 60);
  }
  /* A click on an outline row is a REQUEST that outlives the click: it names a
     page that may still have to load. Two things can happen, and the row must
     work under both. The router usually intercepts and swaps div.wrap. But if
     scripts are stripped, if the fetch fails, or if the page is opened in a new
     tab, the browser does an ordinary navigation and this document is gone. So
     the request is PARKED in sessionStorage and applied by whoever ends up
     holding the page: this document after a swap, or the fresh one after a
     load. It is cleared the moment it is honoured, so it can never fire twice.
     (JL 260801: "clicking a content division does not take me there".) */
  var PARK = 'bnav:goto';
  function park(a) {
    var out = a.closest('.sb-out');
    try {
      sessionStorage.setItem(PARK, JSON.stringify({
        /* the id, read off the outline the row lives in: the href is `#QB5c`
           in the one-file board and `QB/QB5c-editing.html` in the tree, and
           slicing one character off the second gave an id nothing has. */
        pid: out ? out.getAttribute('data-out') : (a.getAttribute('href') || '').slice(1),
        k: a.dataset.k || '',
        div: a.dataset.div === undefined ? null : a.dataset.div,
        t: a.dataset.t || ''
      }));
    } catch (e) { /* private mode: the row still navigates, it just lands at the top */ }
  }
  function honour() {
    var req;
    try { req = JSON.parse(sessionStorage.getItem(PARK) || 'null'); } catch (e) { req = null; }
    if (!req || !req.pid) return;
    var page = document.getElementById(req.pid);
    if (!page) return;                       // not here yet; a later call will
    try { sessionStorage.removeItem(PARK); } catch (e) {}
    reveal(req, page);
  }
  sb.addEventListener('click', function (e) {
    var a = e.target.closest('a.sb-s,a.sb-ss');
    if (!a) return;
    park(a);
    /* Do NOT honour it here when the router will handle the click. Honouring
       eagerly opened the division on the DOM that was about to be REPLACED and
       consumed the request on the way, so the fresh wrap arrived with nothing
       left to apply: the row worked from another page and did nothing from its
       own (JL 260801, found by clicking §6 and watching §3 open instead).
       In the one-file board no fetch happens, so 90ms is the whole story. */
    var routed = document.body.classList.contains('split') &&
                 /\.html(\?|#|$)/.test(a.getAttribute('href') || '');
    if (!routed) setTimeout(honour, 90);
  });
  function reveal(req, page) {
    {
      var el = SEL[req.k] ? page.querySelector(SEL[req.k]) : null;
      if (el && req.div !== null && req.div !== undefined) {
        var divs = Array.prototype.filter.call(el.children, function (x) {
          return x.matches && x.matches('details.csec') &&
                 x.className.indexOf('display') < 0;
        });
        var d = divs[+req.div];
        if (d) { el.open = true; d.open = true; el = d; }
      } else if (el && req.t) {
        /* a non-Content subsection (### Decision Now …) is found by its
           rendered .sh heading text */
        var m = req.t.trim().toLowerCase();
        var hs = el.querySelectorAll('.sh');
        for (var i = 0; i < hs.length; i++) {
          if (hs[i].textContent.trim().toLowerCase().indexOf(m) === 0) {
            el.open = true;
            el = hs[i];
            break;
          }
        }
      }
      var to = el || page;
      if (el && el.tagName === 'DETAILS') el.open = true;
      /* Scroll TWICE, deliberately. The arrival path that swaps the wrap calls
         `window.scrollTo(0, 0)` on its way in, and the path that reloads gets
         the browser's own scroll restoration; either can land after this one
         and put the reader back at the top of a page they asked to enter part
         way down. The second call is cheap and it is what makes the row feel
         like it went somewhere (JL 260801). */
      to.scrollIntoView({ block: 'start' });
      setTimeout(function () { to.scrollIntoView({ block: 'start' }); }, 140);
    }
  }
  window.addEventListener('hashchange', mark);
  // A tree navigation replaces div.wrap and fires no hashchange.
  window.addEventListener('board:updated', function () { mark(); honour(); });
  mark();
  honour();                       // a real page load, arriving with a parked request
})();
