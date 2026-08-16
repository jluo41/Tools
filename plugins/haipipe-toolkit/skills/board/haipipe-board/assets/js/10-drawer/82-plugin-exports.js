/* 📜📝📚 Exports · the DERIVED paper-facing plugins: latex/, word/, bibex/.
 *
 * WHAT THIS FILE OWNS, and it is one thing: WHERE each export's artifact LIVES
 * and which door writes it. The writers themselves are the paper family's
 * (md2tex, md2docx, docx2pdf, the bibex extractor), reached through one
 * /_board/<plugin> route each (live/export.py). No export is authored here.
 *
 * THE `tab` SPEC is the shell's whole interface (haipipe-plugin): the
 * shell reads registry entries carrying `tab: {url, write}` and builds its
 * right-pane tab from them, so plugin N+1 ships by registering — the shell is
 * never edited for it. Draw and Slides predate the spec and still use their
 * window hooks; these three are the first conforming instances.
 *
 * WHY `url()` NAMES A VIEW PAGE for all three: a tab needs a URL a browser
 * can frame, and the view is where the artifact's second half lives — latex
 * shows the compiled PDF with the raw .tex one fold below (JL 260815), word
 * frames the PDF twin beside the ⬇ .docx, bibex renders the workbench.
 */
(function () {
  'use strict';

  function pageFile(page) {
    return (page && page.getAttribute('data-file')) || '';
  }

  function board() {
    try { return boardPath(); } catch (e) { return location.pathname; }
  }

  /* The saved artifact, by the plugin contract's one naming rule:
     folded page -> <dir>/<stem>/<plugin>/<stem><ext>; a flat page falls back
     to the board-level <board>/<plugin>/ home, the same fork the server takes. */
  function savedUrl(page, plugin, ext) {
    var f = pageFile(page);
    if (!f) return '';
    var p = decodeURIComponent(location.pathname || '');
    var cut = p.lastIndexOf('/board/');
    if (cut < 0) return '';
    var base = p.slice(0, cut);
    var m = f.match(/^(.*)\/([^\/]+)\/\2\.md$/);   // folded: <dir>/<stem>/<stem>.md
    if (m) return base + '/' + m[1] + '/' + m[2] + '/' + plugin + '/' + m[2] + ext;
    var stem = (f.split('/').pop() || '').replace(/\.md$/, '');
    return stem ? base + '/' + plugin + '/' + stem + ext : '';
  }

  function writer(route) {
    return function (page, cb, err) {
      fetch('/_board/' + route, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: board(), file: pageFile(page) })
      }).then(function (r) { return r.json(); })
        .then(function (j) {
          if (!j.ok) { err && err(j.err || 'the ' + route + ' export failed'); return; }
          cb(j);
        })
        .catch(function (e) { err && err(String(e)); });
    };
  }

  /* On a BARE page there is no shell and no tab strip, so `open` writes the
     export and shows it in its own browser tab — the menu row stays the one
     door that works everywhere, which is the registry's own rule. */
  function opener(write) {
    return function (page) {
      write(page, function (j) {
        if (j.url) window.open(j.url + (/\.html$/.test(j.url) ? '?plain' : ''),
                               '_blank', 'noopener');
      }, function (e) { alert('⚠ ' + e); });
    };
  }

  var DEFS = [
    { id: 'latex', label: '📜 LaTeX', route: 'latex', ext: '-view.html',
      hint: 'the compiled PDF with the raw .tex one fold below' },
    { id: 'word', label: '📝 Word', route: 'word', ext: '-view.html',
      hint: 'a coauthor .docx with its PDF twin, via md2docx' },
    { id: 'bibex', label: '📚 BibEx', route: 'bibex', ext: '-bib.html',
      hint: 'this page’s citations, subset from the paper’s .bib' }
  ];

  if (window.boardPlugins) {
    DEFS.forEach(function (d) {
      var write = writer(d.route);
      window.boardPlugins.register({
        id: d.id,
        label: d.label,
        hint: d.hint,
        /* 🔌 A PLUGIN, not a workflow: a surface you open beside the page. */
        menu: 'plugin',
        /* Any page with a source file can export; the builder degrades
           cite-less outside a paper rather than refusing (the roster's rule). */
        applies: function (page) { return !!pageFile(page); },
        open: opener(write),
        tab: {
          url: function (page) { return savedUrl(page, d.id, d.ext); },
          write: write
        }
      });
    });
  }
})();
