/* 🔌 Registry of what a page can OPEN · one menu, one list.
 *
 * WHY A REGISTRY. The picker used to be two hardcoded buttons, so the board engine
 * had to know every surface by name. A plugin now registers its own entry, and the
 * engine never learns that labeling exists (JL 260807).
 *
 * ONE MENU. The picker sells category surfaces, not the internal lanes they
 * present. Chat + Draw live in Studio; Slides lives in Delivery. Page phases is
 * lifecycle machinery, not a reader-facing Plugin row.
 *
 * `applies` KEEPS THE MENU HONEST. An entry that cannot act on the open page is not
 * shown, so the menu never offers work that would be refused. It follows that an
 * entry ships when its surface does: registering Draw before it opens anything makes
 * the menu lie, and a menu that lies once stops being read.
 */
(function () {
  'use strict';

  var reg = [];
  var seq = 0;
  var defaultId = '';

  var MENUS = ['plugin'];

  /* {id, label, hint, menu, order, applies(page)->bool, open(page)}.

     `order` is the reader-facing sequence and must not depend on asset load order.
     Equal or omitted values retain registration order, so third-party entries remain
     stable without the registry knowing their names.

     `menu` defaults to 'plugin'. An unknown menu name is corrected to 'plugin',
     so a typo cannot hide an otherwise usable surface. */
  function register(spec) {
    if (!spec || !spec.id || typeof spec.open !== 'function') return;
    if (MENUS.indexOf(spec.menu) < 0) spec.menu = 'plugin';
    reg = reg.filter(function (e) { return e.id !== spec.id; });
    spec._pluginSeq = seq++;
    reg.push(spec);
  }

  function ordered(entries) {
    return entries.slice().sort(function (a, b) {
      var ao = Number.isFinite(a.order) ? a.order : 1000;
      var bo = Number.isFinite(b.order) ? b.order : 1000;
      return ao - bo || a._pluginSeq - b._pluginSeq;
    });
  }

  function livePage() {
    var secs = document.querySelectorAll('.wrap section.slide.q');
    for (var i = 0; i < secs.length; i++) {
      if (secs[i].offsetParent !== null) return secs[i];
    }
    return secs[0] || null;
  }

  /* A page's declared type, read off the rendered page rather than the source, so a
     surface can gate on it without the engine parsing frontmatter a second time. */
  function pageType(page) {
    if (!page) return '';
    return (page.getAttribute('data-page-type')
            || page.getAttribute('data-type') || '').trim();
  }

  /* `menu` is optional: omitted, this answers "everything this page can open", which
     is what the in-page picker wants when it draws both groups in one list. */
  function applicable(page, menu) {
    return ordered(reg.filter(function (e) {
      if (menu && e.menu !== menu) return false;
      try { return !e.applies || e.applies(page, pageType(page)); }
      catch (err) { return false; }
    }));
  }

  /* THE DEFAULT, and why it is a second call rather than a `register` field:
     a plugin ships not knowing whether it wants to be the default, and the
     answer can change (JL 260818: outline should open on a plain FAB click
     instead of the picker every time). One id is remembered; the FAB reads
     it and falls back to the picker when the id is unset, unknown, or does
     not apply to the page in view — the same `applies` gate every row uses,
     so a default never opens on a page it would refuse. */
  function setDefault(id) { defaultId = id || ''; }
  function getDefault(page) {
    if (!defaultId) return null;
    var hit = reg.filter(function (e) { return e.id === defaultId; })[0];
    if (!hit) return null;
    try { if (hit.applies && !hit.applies(page, pageType(page))) return null; }
    catch (e) { return null; }
    return hit;
  }

  window.boardPlugins = {
    register: register,
    all: function () { return ordered(reg); },
    applicable: applicable,
    menus: function () { return MENUS.slice(); },
    livePage: livePage,
    pageType: pageType,
    setDefault: setDefault,
    getDefault: getDefault
  };
})();
