/* 🔌 Registry of what a page can OPEN · two menus, one list.
 *
 * WHY A REGISTRY. The picker used to be two hardcoded buttons, so the board engine
 * had to know every surface by name. A plugin now registers its own entry, and the
 * engine never learns that labeling exists (JL 260807).
 *
 * TWO MENUS, AND THE SPLIT IS NOT COSMETIC (JL 260808).
 *
 *   🔌 Plugin    a SURFACE you open. Opens to the RIGHT, tab-like. It has no
 *                opinion about where you are on the page, so it applies almost
 *                everywhere. GUI Chat, TUI Chat, and later Draw and Slide.
 *   🪜 Workflow  a STEPPER over THIS page. Opens along the BOTTOM. Its whole job
 *                is to say which step is live and which are refused, so it is
 *                gated on the page's declared type. Labeling, and later Page.
 *
 * This reverses the 260807 ruling that there is no Workflow entry, and the reason
 * the earlier one was right is the reason this one is: a category with one member
 * names a concept nobody owns. Page's four phases arrive as the second member, so
 * the category now describes something real instead of anticipating it.
 *
 * A WORKFLOW IS NOT ALWAYS A LADDER. Labeling's five doors are ordered and each is
 * locked by the one before. Page's DRAFT/EVIDENCE/REVISE/CHECK is a loop whose CHECK
 * routes BACKWARD ("RUN is deliberately not ADVANCE"), so it has a current phase and
 * legal next phases and no locks at all. Each surface computes its own dimming; the
 * registry holds no step model, which is what lets both live in one menu.
 *
 * `applies` KEEPS THE MENU HONEST. An entry that cannot act on the open page is not
 * shown, so the menu never offers work that would be refused. It follows that an
 * entry ships when its surface does: registering Draw before it opens anything makes
 * the menu lie, and a menu that lies once stops being read.
 */
(function () {
  'use strict';

  var reg = [];

  var MENUS = ['plugin', 'workflow'];

  /* {id, label, hint, menu, applies(page)->bool, open(page)} · order is registration
     order, which is asset sort order, which is stable across builds.

     `menu` defaults to 'plugin' so an entry written before the split still lands
     somewhere visible rather than silently in neither menu. An unknown menu name is
     corrected to 'plugin' for the same reason: a typo should misfile an entry, not
     delete it. */
  function register(spec) {
    if (!spec || !spec.id || typeof spec.open !== 'function') return;
    if (MENUS.indexOf(spec.menu) < 0) spec.menu = 'plugin';
    reg = reg.filter(function (e) { return e.id !== spec.id; });
    reg.push(spec);
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
    return reg.filter(function (e) {
      if (menu && e.menu !== menu) return false;
      try { return !e.applies || e.applies(page, pageType(page)); }
      catch (err) { return false; }
    });
  }

  window.boardPlugins = {
    register: register,
    all: function () { return reg.slice(); },
    applicable: applicable,
    menus: function () { return MENUS.slice(); },
    livePage: livePage,
    pageType: pageType
  };
})();
