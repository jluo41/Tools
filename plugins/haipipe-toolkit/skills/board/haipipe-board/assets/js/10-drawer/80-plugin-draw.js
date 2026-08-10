/* 🖌 Draw · open THIS page's own drawing, beside the page you are reading.
 *
 * WHY IT NEEDED BUILDING AT ALL. The linked-drawing split (QD5a) gave every page
 * its own `draw/<Page>.excalidraw` and gave every group a `group.excalidraw` that
 * composes them. The GROUP pages then got a canvas printed into their body. The
 * 68 PAGE sources got nothing: the files existed and no surface opened them, so a
 * page's own picture was reachable only by opening its group and hunting for it
 * (verified in Chrome 260810, QD5: zero `_excalidraw` references on the page).
 *
 * IT OPENS ON THE RIGHT, WHICH IS THE AXIS RULE (JL 260808). A workflow is an
 * ordered set of steps you RUN, so it goes along the bottom; a plugin is a surface
 * you LOOK AT while reading, so it goes down the right. The drawing is the second
 * kind: you are comparing it against the prose next to it, which is exactly why a
 * full-bleed canvas would be the wrong answer even though it is the easier one.
 *
 * IT DRAWS IN THE PAGE FRAME, NEVER THE SHELL, for the same reason Slides does:
 * inside the 5599 viewer the page is the centre column, and the shell owns the
 * panes. A surface that repainted another pane is the thing the pane split exists
 * to prevent. So "the right" means the right of the page column, and the effect is
 * the same in the viewer and on a bare page, with no code that knows which it is.
 *
 * THE OWNER IS DERIVED, NOT GUESSED, and the derivation is the only subtle part.
 * `/_excalidraw/?board=<path>` wants the scene path relative to the SERVER ROOT,
 * which is the repo root, which is also what `location.pathname` is relative to.
 * So the built page's own URL already carries the answer:
 *
 *   /Tools/…/01-boardform-260722/board/QD/QD5-split-workspace.html
 *    └────────── board folder ─────────┘ └─ output ─┘
 *
 * Cut at the last `/board/` and the prefix IS the repo-relative board folder. Add
 * the group folder from `data-file`, then `draw/<section id>.excalidraw`. Nothing
 * here re-implements the build's path logic; it reads the URL the build produced.
 *
 * A GROUP PAGE OPENS THE GROUP'S OWN SCENE. `livePage()` finds `section.slide.q`,
 * which a generated group page does not have, so the fallback reads the composed
 * canvas the group page already prints and reuses ITS url. That keeps one answer
 * for "which file does this view save to" instead of two that can drift.
 *
 * IT REFUSES RATHER THAN GUESSES. No `excalidraw:` on the Board, or no owner it
 * can name, and the entry is not drawn. `applies` returning false is the menu
 * staying honest: an entry that cannot act on the open page is never offered.
 */
(function () {
  'use strict';

  var ID = 'xcalpanel';
  var WKEY = 'board-draw-width';

  function host() {
    return (document.body.getAttribute('data-xcal') || '').trim();
  }

  /* The repo-relative board folder, read off this page's own URL. */
  function boardRel() {
    var p = decodeURIComponent(location.pathname || '');
    var cut = p.lastIndexOf('/board/');
    if (cut < 0) return '';
    return p.slice(0, cut).replace(/^\/+/, '');
  }

  /* {url, label, owner} for whatever the open view owns, or null. */
  function owner(page) {
    var h = host();
    if (!h) return null;                       // Board declares no drawing host
    if (page) {
      var file = page.getAttribute('data-file') || '';
      var id = page.id || '';
      var dir = file.indexOf('/') < 0 ? '' : file.slice(0, file.lastIndexOf('/'));
      var base = boardRel();
      if (!id || !base) return null;
      var rel = [base, dir, 'draw', id + '.excalidraw']
                  .filter(Boolean).join('/');
      /* EDITABLE, because a page's own source has exactly ONE owner and there is
         nothing to disambiguate: the composed group view is the ambiguous case,
         and that is the one that stays read-only until a person picks a mode.
         Opening armed is safe here because xcal-boot arms a save only from a
         non-toolbar human gesture (QD5a 260807), so merely looking writes nothing.
         `mode` is deliberately omitted: the boot derives `page-source` from the
         scene's own ownerKind, and a second guess here could disagree with it. */
      return { url: h + '/?board=' + encodeURI(rel) + '&edit=1', label: id,
               rel: rel, kind: 'page' };
    }
    /* A generated GROUP page: reuse the url its own composed canvas already has,
       so the panel and the inline canvas can never name different files. */
    var f = document.querySelector('.group-canvas iframe[src*="_excalidraw"]');
    if (!f) return null;
    var src = f.getAttribute('src') || '';
    var m = /board=([^&]+)/.exec(src);
    return { url: src, label: 'this group', rel: m ? decodeURIComponent(m[1]) : '',
             kind: 'group' };
  }

  function widthNow() {
    var w = 0;
    try { w = parseInt(localStorage.getItem(WKEY) || '0', 10) || 0; } catch (e) {}
    var max = Math.max(320, Math.floor(window.innerWidth * 0.72));
    return Math.min(max, Math.max(300, w || Math.floor(window.innerWidth * 0.42)));
  }

  function remember(w) {
    try { localStorage.setItem(WKEY, String(w)); } catch (e) {}
  }

  function mount() {
    var d = document.getElementById(ID);
    if (d) return d;
    d = document.createElement('aside');
    d.id = ID;
    d.hidden = true;
    d.innerHTML =
      '<div class="xp-rz" title="drag to resize"></div>'
      + '<header class="xp-hd">'
      + '<span class="xp-t">\u{1F58C} <b class="xp-who"></b></span>'
      + '<span class="xp-mut"></span>'
      + '<a class="xp-out" target="_blank" rel="noopener" title="open in a full tab">↗</a>'
      + '<button class="xp-x" type="button">✕ close</button>'
      + '</header>'
      + '<iframe class="xp-fr" title="drawing" referrerpolicy="no-referrer"></iframe>';
    document.body.appendChild(d);
    d.querySelector('.xp-x').onclick = close;
    grip(d.querySelector('.xp-rz'), d);
    document.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape' && !d.hidden) { close(); }
    }, true);
    /* A NEW PAGE IS A NEW OWNER. The router swaps the page under a panel that is
       already open, and a panel still showing the previous page's drawing is the
       exact bug the chat pane had (JL 260803: page pane on QA2, chat header on
       QB0). Re-aim on the same event the rest of the live layer listens to. */
    window.addEventListener('board:updated', reaim);
    window.addEventListener('hashchange', reaim);
    return d;
  }

  /* Dragging the left edge. Width is stored, because a canvas the reader sized
     once should not snap back on the next page. */
  function grip(bar, panel) {
    var from = 0, w0 = 0;
    function move(ev) {
      var dx = from - (ev.touches ? ev.touches[0].clientX : ev.clientX);
      var w = Math.min(Math.floor(window.innerWidth * 0.72),
                       Math.max(300, w0 + dx));
      size(panel, w);
    }
    function up() {
      document.removeEventListener('mousemove', move);
      document.removeEventListener('touchmove', move);
      document.removeEventListener('mouseup', up);
      document.removeEventListener('touchend', up);
      document.body.classList.remove('xp-dragging');
      remember(panel.getBoundingClientRect().width | 0);
    }
    function down(ev) {
      from = ev.touches ? ev.touches[0].clientX : ev.clientX;
      w0 = panel.getBoundingClientRect().width | 0;
      document.body.classList.add('xp-dragging');
      document.addEventListener('mousemove', move);
      document.addEventListener('touchmove', move, { passive: true });
      document.addEventListener('mouseup', up);
      document.addEventListener('touchend', up);
      ev.preventDefault();
    }
    bar.addEventListener('mousedown', down);
    bar.addEventListener('touchstart', down, { passive: false });
  }

  function size(panel, w) {
    panel.style.width = w + 'px';
    document.documentElement.style.setProperty('--draw-w', w + 'px');
  }

  function reaim() {
    var d = document.getElementById(ID);
    if (!d || d.hidden) return;
    var o = owner(window.boardPlugins && window.boardPlugins.livePage());
    if (!o) return close();
    if (d.dataset.rel === o.rel) return;         // same owner, leave it alone
    fill(d, o);
  }

  function fill(d, o) {
    d.dataset.rel = o.rel || '';
    d.querySelector('.xp-who').textContent = o.label;
    d.querySelector('.xp-mut').textContent =
      o.kind === 'group' ? 'composed · page sources stay their own'
                         : 'this page’s own source';
    d.querySelector('.xp-out').setAttribute('href', o.url);
    var fr = d.querySelector('.xp-fr');
    if (fr.getAttribute('src') !== o.url) fr.setAttribute('src', o.url);
  }

  function close() {
    var d = document.getElementById(ID);
    if (!d) return;
    d.hidden = true;
    document.body.classList.remove('has-draw');
    document.documentElement.style.removeProperty('--draw-w');
    /* The iframe is dropped on close ON PURPOSE. A proxied Excalidraw left in a
       hidden frame keeps a live editor and its unsaved buffer somewhere nobody
       can see, and the save it might issue would carry a revision from a view
       the reader has forgotten. Reopening costs one fetch; a ghost editor costs
       a conflict nobody can explain. */
    d.querySelector('.xp-fr').removeAttribute('src');
    d.dataset.rel = '';
  }

  function open(page) {
    page = page || (window.boardPlugins && window.boardPlugins.livePage());
    var o = owner(page);
    if (!o) return;
    var d = mount();
    if (!d.hidden) return close();          // a second click puts it away
    fill(d, o);
    size(d, widthNow());
    d.hidden = false;
    document.body.classList.add('has-draw');
  }

  if (window.boardPlugins) {
    window.boardPlugins.register({
      id: 'draw',
      label: '\u{1F58C} Draw',
      hint: 'this page’s drawing, beside the page',
      // 🔌 A PLUGIN: a surface you look through. It stores no state on the page
      // and locks no step, which is the test the two menus split on.
      menu: 'plugin',
      applies: function (page) { return !!owner(page); },
      open: open
    });
  }

  window.boardDrawOpen = open;   // for direct calls and for the tests
})();
