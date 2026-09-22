/* 📚 Content · the ONE reader every export shares.
 *
 * WHY THIS FILE EXISTS. Three surfaces now take the open page and hand it to
 * somebody else: 🎞 Slides writes an html-ppt deck, 📕 PDF writes a print sheet,
 * 📝 Word writes a .docx. Each of them needs the same three answers — which nodes
 * are the page's CONTENT, what is each one called, and what has to be stripped out
 * of a clone before it leaves the board — and the moment two of them answer
 * differently the deck and the document stop being the same page.
 *
 * So the answers live here, once, and the three exports are renderers with no
 * opinion about what a division is.
 *
 * CONTENT, NOT APPARATUS (JL 260812: "slides should focus on the content as well").
 * A board page carries two different kinds of thing. `## Content` is the writing:
 * numbered divisions of real prose, which is what a reader came for. Everything
 * around it — Aims, States, Law, Glossary, Files, Discussion, Log — is APPARATUS:
 * status the page keeps about itself, useful while you work on the page and noise
 * the moment you are trying to read it. The first Slides run exported all of it, so
 * a nine-division page arrived as twenty-two slides of which half were fold counts
 * and log rows. `divisions()` reads `details.sect.content` and nothing else.
 *
 * THE FALLBACK IS NOT AN AFTERTHOUGHT. Not every page has a `## Content`: an index
 * page, a stage hub, a page mid-DRAFT. Refusing to export those would make the menu
 * lie about applying everywhere, so when there is no Content section the walk falls
 * back to the whole page and SAYS SO in the returned `source`, which each renderer
 * shows in its header strip. A silent fallback would be the worse bug: the reader
 * would think the apparatus WAS the content.
 */
(function () {
  'use strict';

  function txt(node) {
    return node ? (node.textContent || '').replace(/\s+/g, ' ').trim() : '';
  }

  /* THE AUTHOR'S WORDS, WITHOUT THE INJECTED CONTROLS. A summary is plain text in
     the source; the anchor chips, the ⧉ copy and the 🤖 hand-off are added by the
     board's own scripts after load. Reading only the node's direct TEXT children
     takes what the author typed and drops every control, without this file having
     to know their class names, which it would otherwise have to track forever.
     The first run showed exactly what that costs: "1 · Step ① initC1C1⧉🤖". */
  function ownText(node) {
    if (!node) return '';
    var s = '';
    Array.prototype.forEach.call(node.childNodes, function (n) {
      if (n.nodeType === 3) s += n.nodeValue;
    });
    return s.replace(/\s+/g, ' ').trim();
  }

  function heading(det) {
    if (!det) return '';
    var sm = det.querySelector(':scope > summary');
    if (!sm) return '';
    return ownText(sm.querySelector('.chl')) || ownText(sm) || txt(sm);
  }

  /* A clone is taken rather than the node itself, because an export must be able to
     open what the page keeps shut without the page losing its own fold state. Every
     control that acts on the PAGE is stripped from the copy: a copy button inside a
     slide, a PDF or a Word file would act on a detached node, or on nothing at all,
     and appear broken — which is worse than not being there. */
  function clean(node) {
    if (!node) return null;
    var c = node.cloneNode(true);
    /* The clone's OWN tag counts. `querySelectorAll` never returns the root, so a
       section cloned whole kept its wrapper shut while every child inside it was
       opened, and with the summary removed as well it rendered as a title over
       nothing. */
    if (c.tagName === 'DETAILS') c.open = true;
    c.querySelectorAll('details').forEach(function (d) { d.open = true; });
    /* `.schatbar` and `.smenu` are the SENTENCE APPARATUS, injected after load and
       therefore invisible in the HTML on disk. On the page they are quiet controls
       beside a sentence; cloned into an export they print as bare text, so every
       slide of QBt1 carried a stack of "C1.P1.S1 / QBt1.C1.P1.S1" between its
       sentences and half the slide was ids (JL 260810: "the quality is not that
       good"). They are stripped by WRAPPER, not by the `.sidchip` inside, because
       removing the chip alone leaves the empty bar holding its own vertical space. */
    c.querySelectorAll('.secall,.cpy,.copy,.sb-x,.schatbar,.smenu,.shc,button')
      .forEach(function (b) { b.parentNode && b.parentNode.removeChild(b); });
    /* Links keep their text but stop being links: a click inside a deck that
       navigated the frame away would look like the deck crashed, and a live href
       means nothing at all inside a .docx. */
    c.querySelectorAll('a').forEach(function (a) {
      var s = document.createElement('span');
      s.className = 'sd-was-link';
      s.innerHTML = a.innerHTML;
      a.parentNode.replaceChild(s, a);
    });
    return c;
  }

  /* The page head, which every export opens with: the id, the title, the state
     pill and the metadata line. `.hid` holds the page id, which the kicker already
     carries, so reading it twice printed "QG1 QG1 · page-type LABELING". */
  function cover(page) {
    var h2raw = page && page.querySelector('h2.h2');
    var h2 = h2raw ? h2raw.cloneNode(true) : null;
    if (h2) h2.querySelectorAll('.hid').forEach(function (n) { n.remove(); });
    var pill = page && page.querySelector('.qh .pill');
    var metas = [];
    Array.prototype.forEach.call(
      (page && page.querySelectorAll('.qh .mut')) || [],
      function (m) {
        var s = txt(m).replace(/^·\s*/, '');
        if (s) metas.push(s);
      });
    return { id: (page && page.id) || '', title: txt(h2),
             state: txt(pill), metas: metas };
  }

  /* The Opening's lead paragraph: the question the page exists to answer. It is
     kept even though it is not inside `## Content`, because it is the one piece of
     apparatus that is genuinely prose and reads as the abstract of everything
     after it. Its own heading row is dropped, since the renderer supplies one. */
  function opening(page) {
    var op = page && page.querySelector('.opening');
    var lead = clean(op && op.querySelector('.ask'));
    if (!lead) return null;
    lead.querySelectorAll('.ch, .opening-head').forEach(function (n) {
      n.parentNode && n.parentNode.removeChild(n);
    });
    return txt(lead) ? lead : null;
  }

  /* The FALLBACK walk, for a page with no `## Content`. Sections are not all direct
     children: Aims and States sit side by side inside `div.cmp`, and Law, Glossary,
     Log and Discussion inside `div.folds`, both layout wrappers the renderer adds.
     A walk that read only direct children lost half of every page and said nothing
     about it. */
  function allSections(page) {
    var out = [];
    Array.prototype.forEach.call(page.children, function (el) {
      if (el.tagName === 'DETAILS') { out.push(el); return; }
      if (el.tagName !== 'DIV') return;
      if (/\b(qh|opening|nav)\b/.test(el.className || '')) return;
      Array.prototype.forEach.call(el.children, function (k) {
        if (k.tagName === 'DETAILS') out.push(k);
      });
    });
    return out;
  }

  /* ── divisions ──────────────────────────────────────────────────────────────
     -> {source:'content'|'page', items:[{kicker, title, node}]}

     `source` is not decoration. 'content' means these ARE the page's `## Content`
     divisions; 'page' means the page had none and this is every section it has,
     apparatus included. Each renderer prints that word, so a document that is not
     really the content never passes for the content. */
  function divisions(page) {
    if (!page) return { source: 'page', items: [] };

    var content = page.querySelector(':scope > details.sect.content')
               || page.querySelector('details.sect.content');
    if (content) {
      var csecs = content.querySelectorAll(':scope > .cbody > details.csec, '
                                         + ':scope > details.csec');
      var items = [];
      Array.prototype.forEach.call(csecs, function (d) {
        if (items.some(function (it) { return it.src === d; })) return;
        items.push({ kicker: '', title: heading(d) || '…', src: d,
                     node: clean(d.querySelector(':scope > .cbody') || d) });
      });
      /* A Content section with no divisions is a flat one: the prose sits straight
         in its body with no numbered headings. That is still content, so it is
         exported as a single division rather than dropped. */
      if (!items.length) {
        var flat = clean(content.querySelector(':scope > .cbody') || content);
        if (flat && txt(flat)) {
          flat.querySelectorAll(':scope > summary').forEach(function (s) {
            s.parentNode && s.parentNode.removeChild(s);
          });
          items.push({ kicker: '', title: 'Content', node: flat });
        }
      }
      if (items.length) return { source: 'content', items: items };
    }

    var out = [];
    allSections(page).forEach(function (el) {
      var label = heading(el);
      /* One node can satisfy two of these selectors at once, and querySelectorAll
         returns it once per match, which is how the Files section shipped its
         Related-pages group as two identical entries. */
      var subs = [];
      ['details', '.cbody > details', 'div > details'].forEach(function (sel) {
        Array.prototype.forEach.call(el.querySelectorAll(':scope > ' + sel),
          function (s) { if (subs.indexOf(s) < 0) subs.push(s); });
      });
      if (subs.length) {
        subs.forEach(function (sub) {
          out.push({ kicker: label, title: heading(sub) || '…',
                     node: clean(sub.querySelector(':scope > .cbody') || sub) });
        });
      } else {
        var inner = el.cloneNode(true);
        var sm = inner.querySelector(':scope > summary');
        if (sm) sm.parentNode.removeChild(sm);
        out.push({ kicker: '', title: label, node: clean(inner) });
      }
    });
    return { source: 'page', items: out };
  }

  function pageFile(page) {
    return (page && page.getAttribute('data-file')) || '';
  }

  function boardOf() {
    try { return boardPath(); } catch (e) { return location.pathname; }
  }

  window.boardContent = {
    txt: txt, ownText: ownText, heading: heading, clean: clean,
    cover: cover, opening: opening, divisions: divisions,
    pageFile: pageFile, board: boardOf
  };
})();
