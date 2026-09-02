/* 🎞 Slides · show THIS page's saved deck in a right split.
 *
 * THE DECK IS THE AI DECK (JL 260815: "We will just have the AI deck"). A deck
 * is an AUTHORED artifact: an agent reads the page's Content, makes editorial
 * choices, and writes `<page>/slide/<page>-deck.html` on html-ppt's own shell.
 * This file owns none of that. It owns exactly one thing: WHERE a page's saved
 * deck lives, and showing it beside the prose it was written from.
 *
 * WHAT RETIRED HERE, so the next reader knows it was a decision and not a gap.
 * The first version painted its own slides in this document (a second
 * presentation system growing beside the display plugin's — killed 260808).
 * The second version REFLOWED the page's rendered DOM into slides and posted
 * them to `live/deck.py`, which wrapped them verbatim. It needed no model and
 * made no editorial choice — and that was its disease: the deck was the page's
 * own words wearing a theme, so opening Slides showed you what you had just
 * read. JL retired the tier on 260815: a deck that claims nothing says
 * nothing. Now a page with no saved deck gets a pointer to the author path,
 * never a silently generated verbatim copy.
 *
 * WHAT html-ppt OWNS: the deck file itself links straight at the skill's
 * assets, so the saved artifact carries base.css, a theme, and runtime.js
 * (← → move, T themes, F fullscreen, O overview, S presenter). None of that is
 * reimplemented or copied here.
 *
 * WHY A PLUGIN AND NOT A WORKFLOW. It stores nothing on the page and locks no
 * step; it is a surface you look through. It applies to every page, because
 * every page CAN have a deck — the panel says how to get one when none exists.
 */
(function () {
  'use strict';

  var ID = 'sdeck';
  var WKEY = 'board-slides-width';
  var curPage = null;     // the page the open panel belongs to, for ✨ regenerate

  /* The split geometry is Draw's, one number and one class: the panel sets
     --slides-w as it is sized and body.has-slides moves the prose over.
     (JL 260815: "a right split of the page", reversing the 260810 mode.) */
  function widthNow() {
    var w = 0;
    try { w = parseInt(localStorage.getItem(WKEY) || '0', 10) || 0; } catch (e) {}
    var max = Math.max(340, Math.floor(window.innerWidth * 0.72));
    return Math.min(max, Math.max(320, w || Math.floor(window.innerWidth * 0.46)));
  }

  function remember(w) {
    try { localStorage.setItem(WKEY, String(w)); } catch (e) {}
  }

  function size(panel, w) {
    panel.style.width = w + 'px';
    document.documentElement.style.setProperty('--slides-w', w + 'px');
  }

  function grip(bar, panel) {
    var from = 0, w0 = 0;
    function move(ev) {
      var dx = from - (ev.touches ? ev.touches[0].clientX : ev.clientX);
      var w = Math.min(Math.floor(window.innerWidth * 0.72),
                       Math.max(320, w0 + dx));
      size(panel, w);
    }
    function up() {
      document.removeEventListener('mousemove', move);
      document.removeEventListener('touchmove', move);
      document.removeEventListener('mouseup', up);
      document.removeEventListener('touchend', up);
      document.body.classList.remove('sd-dragging');
      remember(panel.getBoundingClientRect().width | 0);
    }
    function down(ev) {
      from = ev.touches ? ev.touches[0].clientX : ev.clientX;
      w0 = panel.getBoundingClientRect().width | 0;
      document.body.classList.add('sd-dragging');
      document.addEventListener('mousemove', move);
      document.addEventListener('touchmove', move, { passive: true });
      document.addEventListener('mouseup', up);
      document.addEventListener('touchend', up);
      ev.preventDefault();
    }
    bar.addEventListener('mousedown', down);
    bar.addEventListener('touchstart', down, { passive: false });
  }

  function pageFile(page) {
    return (page && page.getAttribute('data-file')) || '';
  }

  /* WHERE A DECK LIVES. A page folder's slide/ plugin is the deck's one home:
     the agent-authored deck lands there and nothing else writes one. The path
     is derived the way Draw derives its owner: the page's own URL carries the
     board folder, and `data-file` carries the rest. */
  function savedUrl(page) {
    var f = pageFile(page);
    var m = f.match(/^(.*)\/([^\/]+)\/\2\.md$/);   // folded: <dir>/<stem>/<stem>.md
    if (!m) return '';
    var p = decodeURIComponent(location.pathname || '');
    var cut = p.lastIndexOf('/board/');
    if (cut < 0) return '';
    return p.slice(0, cut) + '/' + m[1] + '/' + m[2] + '/slide/' + m[2] + '-deck.html';
  }

  /* The page's own .md, root-relative — what /_board/autodeck reads. */
  function mdUrl(page) {
    var f = pageFile(page);
    if (!f) return '';
    var p = decodeURIComponent(location.pathname || '');
    var cut = p.lastIndexOf('/board/');
    if (cut < 0) return '';
    return p.slice(0, cut) + '/' + f;
  }

  function mount() {
    var d = document.getElementById(ID);
    if (d) return d;
    d = document.createElement('div');
    d.id = ID;
    d.hidden = true;
    d.innerHTML =
      '<div class="sd-rz" title="drag to resize"></div>'
      + '<div class="sd-head">'
      + '<span class="sd-what">🎞 <b>Slides</b></span>'
      + '<span class="sd-note">looking for the deck…</span>'
      + '<span class="sd-sp"></span>'
      + '<a class="sd-regen" href="#" title="Claude authors the deck afresh from the page">✨ regenerate</a>'
      + '<a class="sd-open" target="_blank" rel="noopener" hidden>↗ open on its own</a>'
      + '<button class="sd-x" type="button">✕ close</button>'
      + '</div>'
      + '<iframe class="sd-frame" title="slides"></iframe>';
    document.body.appendChild(d);
    d.querySelector('.sd-x').onclick = close;
    d.querySelector('.sd-regen').onclick = function (ev) {
      ev.preventDefault();
      if (curPage) regen(curPage, d);
    };
    grip(d.querySelector('.sd-rz'), d);
    /* Esc closes from the BOARD side. Inside the iframe the key belongs to
       html-ppt's runtime, which is a different document and rightly does not
       know this panel exists, so the shortcut is only bound out here. */
    document.addEventListener('keydown', function (ev) {
      var el = document.getElementById(ID);
      if (el && !el.hidden && ev.key === 'Escape') close();
    }, true);
    return d;
  }

  function close() {
    var d = document.getElementById(ID);
    if (!d) return;
    d.hidden = true;
    document.body.classList.remove('has-slides');
    document.documentElement.style.removeProperty('--slides-w');
    /* The frame is blanked, not merely hidden: a deck left loaded keeps
       html-ppt's runtime listening for arrow keys behind the page. */
    var f = d.querySelector('.sd-frame');
    f.removeAttribute('srcdoc');
    f.src = 'about:blank';
  }

  function note(d, msg) { d.querySelector('.sd-note').textContent = msg; }

  /* SLIDES IS A RIGHT SPLIT (JL 260815, reversing the 260810 full-screen
     mode): the deck sits beside the prose it was cut from. It still puts the
     other right-side surfaces away, because Draw and the deck would otherwise
     contest the same edge.
     Each is closed through its OWN control, so its own teardown runs: Draw drops
     its iframe on close for a reason (a hidden Excalidraw keeps a live editor and
     an unsaved buffer), and reaching past that to hide the element would keep the
     ghost this whole surface is trying not to create. */
  function putOthersAway() {
    var wf = document.getElementById('wfpanel');
    if (wf && !wf.hidden) {
      var wx = wf.querySelector('.wf-x');
      if (wx) wx.click();
    }
    var dx = document.querySelector('.xp-x');
    if (dx && dx.closest('[hidden]') === null) dx.click();
  }

  function showSaved(d, saved) {
    note(d, 'saved deck · ← → move, T theme, F full, O overview, S presenter');
    var a = d.querySelector('.sd-open');
    a.href = saved + '?plain'; a.hidden = false;
    var f = d.querySelector('.sd-frame');
    f.removeAttribute('srcdoc');
    /* `?plain` OR YOU GET A BOARD INSIDE A BOARD. The server wraps any .html it
       serves in the operating shell, so the bare deck URL returns the three-pane
       viewer with the deck hidden in its page frame. The `v=` buster is the
       260815 lesson: a same-src iframe keeps showing the stale document. */
    f.src = saved + '?plain&v=' + Date.now();
  }

  /* ✨ REGENERATE (JL 260815: "add a new button to it so we can regenerate the
     slide"). One POST; Claude authors the deck server-side (/_board/autodeck)
     and the frame reloads onto the fresh file. */
  function regen(page, d) {
    var md = mdUrl(page), saved = savedUrl(page);
    if (!md || !saved) { note(d, '⚠ not a folded page — no slide/ home'); return; }
    var b = d.querySelector('.sd-regen');
    b.style.pointerEvents = 'none'; b.style.opacity = '.5';
    note(d, '🎞 Claude is authoring the deck… (a few minutes)');
    fetch('/_board/autodeck', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ file: md })
    }).then(function (r) { return r.json(); }).then(function (j) {
      b.style.pointerEvents = ''; b.style.opacity = '';
      if (j.ok) showSaved(d, saved);
      else note(d, '✋ ' + (j.err || 'refused'));
    }).catch(function () {
      /* A dropped connection is usually a serve.py restart mid-flight; the
         deck may still land server-side. Look again rather than re-write. */
      note(d, '⏳ connection dropped — checking for the deck…');
      setTimeout(function () {
        b.style.pointerEvents = ''; b.style.opacity = '';
        fetch(saved, { method: 'HEAD', cache: 'no-store' })
          .then(function (r) { r.ok ? showSaved(d, saved) : showNone(d, page); })
          .catch(function () { note(d, '✋ server unreachable'); });
      }, 5000);
    });
  }

  /* NO DECK IS AN ANSWER, not a trigger. The retired reflow used to write a
     verbatim deck here; now the panel says where a deck comes from and stops. */
  function showNone(d, page) {
    note(d, 'no deck yet');
    d.querySelector('.sd-open').hidden = true;
    var stem = (pageFile(page).match(/([^\/]+)\.md$/) || [])[1] || 'this page';
    d.querySelector('.sd-frame').setAttribute('srcdoc',
      '<body style="margin:0;display:flex;align-items:center;justify-content:center;'
      + 'height:100vh;font:15px/1.7 ui-serif,Georgia,serif;color:#444;background:#fff">'
      + '<div style="max-width:34em;padding:2em;text-align:center">'
      + '<div style="font-size:2.4em">🎞</div>'
      + '<p><b>' + stem + '</b> has no deck yet.</p>'
      + '<p>A deck is authored — an agent reads the page’s Content and writes '
      + '<code style="background:#f3f3f3;padding:1px 5px;border-radius:4px">'
      + 'slide/' + stem + '-deck.html</code> on the html-ppt shell '
      + '(JL 260815: the deck is the AI deck; nothing generates one verbatim).</p>'
      + '<p style="color:#888">Press ✨ regenerate above and Claude will author it now.</p>'
      + '</div></body>');
  }

  function open(page) {
    page = page || (window.boardPlugins && window.boardPlugins.livePage());
    if (!page) return;
    var d = mount();
    if (!d.hidden) return close();       // a second click puts it away

    curPage = page;
    putOthersAway();
    d.hidden = false;
    document.body.classList.add('has-slides');
    size(d, widthNow());
    d.querySelector('.sd-open').hidden = true;

    var saved = savedUrl(page);
    if (!saved) return showNone(d, page);
    note(d, 'looking for the deck…');
    fetch(saved, { method: 'HEAD', cache: 'no-store' })
      .then(function (r) { r.ok ? showSaved(d, saved) : showNone(d, page); })
      .catch(function () { showNone(d, page); });
  }

  /* Slides is an internal Delivery lane. Keep its URL/opener exports for the
     Delivery presenter; do not register a second top-level Plugin row. */
  window.boardSlidesOpen = open;   // for direct calls and for the tests
  /* Delivery asks where this page's saved deck would be; whether one exists is
     a HEAD request away, and writing one is an agent's job, not a browser's. */
  window.boardSlidesURL = function (page) {
    page = page || (window.boardPlugins && window.boardPlugins.livePage());
    return page ? savedUrl(page) : '';
  };
})();
