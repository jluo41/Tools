/* 🔌 Plugin registry · what a page can OPEN, and who contributed it.
 *
 * WHY A REGISTRY. The picker used to be two hardcoded buttons, so the board engine
 * had to know every surface by name. A plugin now registers its own entry, and the
 * engine never learns that labeling exists (JL 260807).
 *
 * THERE IS NO GENERIC "WORKFLOW" ENTRY (JL 260807: "Labeling is the workflow").
 * A page type's workflow is contributed BY the plugin that owns that page type and
 * carries that plugin's name. A display plugin would register 🖼 Display, and that
 * entry IS the display workflow. An abstract Workflow entry would name a concept no
 * plugin owns, and every page would carry it whether or not it means anything there.
 *
 * `applies` KEEPS THE MENU HONEST. An entry that cannot act on the open page is not
 * shown, so the menu never offers work that would be refused. This is the same rule
 * the step strip uses inside a surface, one level up.
 */
(function () {
  'use strict';

  var reg = [];

  /* {id, label, hint, applies(page)->bool, open(page)} · order is registration order,
     which is asset sort order, which is stable across builds. */
  function register(spec) {
    if (!spec || !spec.id || typeof spec.open !== 'function') return;
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

  function applicable(page) {
    return reg.filter(function (e) {
      try { return !e.applies || e.applies(page, pageType(page)); }
      catch (err) { return false; }
    });
  }

  window.boardPlugins = {
    register: register,
    all: function () { return reg.slice(); },
    applicable: applicable,
    livePage: livePage,
    pageType: pageType
  };
})();
