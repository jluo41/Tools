/* 🎞 Slides · read THIS page one idea at a time, instead of scrolling it.
 *
 * WHAT THIS IS NOT. The board already has a slide story: `page-type: slide`,
 * whose specimen is QBt9, where a person AUTHORS a deck with html-ppt and then
 * accepts each render. That is for giving a talk, and it claims things, which is
 * why it has an acceptance gate.
 *
 * This is the other thing that wears the same word: a DERIVED VIEW. It reflows the
 * open page's own sections into slides, live, in the browser. Nothing is written,
 * nothing is claimed that the page does not already say, so there is nothing for a
 * person to accept. It cannot disagree with the page because it IS the page, moved
 * around (JL 260808).
 *
 * WHY IT WORKS AT ALL, which is the part worth knowing: board pages were already
 * slide-shaped and nobody had used it. Every Content division opens with a bold
 * caption line, every subdivision with a parenthetical, and both are titles someone
 * already wrote. So the reflow needs no model and makes no editorial choice; it reads
 * headings the page grammar guarantees are there.
 *
 * IT IS A PAGINATOR, NOT A DECK, and the honest name matters. The prose in a Content
 * division is written to be READ: `QG1 §1.1` is five full sentences, and five
 * sentences on a slide is a page with less text visible. What this buys is position
 * and pacing: "7 / 31", arrow keys, one thing on screen. Turning those paragraphs
 * into bullets would need a model rewriting the page's words, which is the authored
 * path above, not this one.
 *
 * THE html-ppt CONNECTION IS THE STYLESHEET, and it is deliberately left as a seam.
 * Slides are emitted as `.sd-kicker / .sd-title / .sd-body` inside `.sd-slide`, four
 * class names an html-ppt theme can be mapped onto without touching this file. They
 * are NOT called `.slide`: the board already uses `section.slide.q` for a whole page,
 * and html-ppt's runtime binds to `.slide`, so the two would fight over every node.
 *
 * WHY A PLUGIN AND NOT A WORKFLOW. It has no state the page stores and no step that
 * can be locked; it is a surface you look through. That is the whole test the two
 * menus split on, and this entry is the first that applies to EVERY page, which is
 * the case the registry was built for and had never carried.
 */
(function () {
  'use strict';

  var ID = 'sdeck';

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
    var sm = det.querySelector(':scope > summary');
    if (!sm) return '';
    return ownText(sm.querySelector('.chl')) || ownText(sm) || txt(sm);
  }

  /* Sections are NOT all direct children. Aims and States sit side by side inside
     `div.cmp`, and Law, Glossary, Log and Discussion inside `div.folds`; both are
     layout wrappers the renderer adds. A walk that read only direct children lost
     half of every page and said nothing about it: the first run on QG1 produced
     twelve slides with no Aim, no State, no Law and no Log on any of them. */
  function sectionsOf(page) {
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

  /* A clone is taken rather than the node itself, because the deck must be able to
     open what the page keeps shut without the page losing its own fold state when
     the deck closes. Everything that acts on the PAGE is stripped from the copy:
     a copy button or an expand-all inside a slide would act on a detached node and
     appear broken, which is worse than not being there. */
  function body(node) {
    if (!node) return null;
    var c = node.cloneNode(true);
    /* The clone's OWN tag counts. `querySelectorAll` never returns the root, so a
       section cloned whole (Law, Log, Discussion: the `div.folds` members, which
       have no sub-items and so take this path) kept its wrapper shut while every
       child inside it was opened. With the summary removed as well, the slide
       rendered as a title over nothing. */
    if (c.tagName === 'DETAILS') c.open = true;
    c.querySelectorAll('details').forEach(function (d) { d.open = true; });
    c.querySelectorAll('.secall,.cpy,.copy,.sb-x,button').forEach(function (b) {
      b.parentNode && b.parentNode.removeChild(b);
    });
    /* Links keep their text but stop being links: a click inside the deck that
       navigated the frame away would look like the deck crashed. */
    c.querySelectorAll('a').forEach(function (a) {
      var s = document.createElement('span');
      s.className = 'sd-was-link';
      s.innerHTML = a.innerHTML;
      a.parentNode.replaceChild(s, a);
    });
    return c;
  }

  /* ── the reflow ────────────────────────────────────────────────────────────
     One pass over the page in DOM order, so the deck's order is the page's order
     and a reader who knows one knows the other. The rule is deliberately shallow:
     a section with foldable sub-items gives one slide per item, and a section
     without them gives one slide. Splitting deeper produces forty slides of two
     sentences, which is the scroll it was meant to replace, in smaller pieces. */
  function build(page) {
    var out = [];

    function push(kicker, title, node, klass) {
      var b = body(node);
      if (!b && !title) return;
      out.push({ kicker: kicker || '', title: title || '', body: b, klass: klass || '' });
    }

    // ① the title slide, from the head the page already renders. `.hid` holds the
    // page id, which the kicker already says, so reading it twice printed
    // "QG1 QG1 · page-type LABELING".
    var h2raw = page.querySelector('h2.h2');
    var h2 = h2raw ? h2raw.cloneNode(true) : null;
    if (h2) h2.querySelectorAll('.hid').forEach(function (n) { n.remove(); });
    var pill = page.querySelector('.qh .pill');
    var muts = Array.prototype.map.call(page.querySelectorAll('.qh .mut'), txt);
    var head = document.createElement('div');
    if (pill) {
      var s = document.createElement('p');
      s.className = 'sd-state';
      s.textContent = txt(pill);
      head.appendChild(s);
    }
    muts.forEach(function (m) {
      if (!m) return;
      var p = document.createElement('p');
      p.className = 'sd-meta';
      p.textContent = m.replace(/^·\s*/, '');
      head.appendChild(p);
    });
    out.push({ kicker: page.id || '', title: txt(h2), body: head, klass: 'sd-cover' });

    // ② the Opening, which is a div rather than a section and so is read by name
    var op = page.querySelector('.opening');
    if (op) {
      var ask = op.querySelector('.ask');
      // The lead is everything in `.ask` except its own heading row.
      var lead = body(ask);
      if (lead) {
        lead.querySelectorAll('.ch, .opening-head').forEach(function (n) {
          n.parentNode && n.parentNode.removeChild(n);
        });
        push('', 'Opening', lead, 'sd-lead');
      }
      Array.prototype.forEach.call(op.querySelectorAll(':scope > details'), function (d) {
        push('Opening', heading(d) || 'More detail', d);
      });
    }

    // ③ every section, in order, split exactly one level deep
    sectionsOf(page).forEach(function (el) {
      var label = heading(el);
      /* One node can satisfy two of these selectors at once, and querySelectorAll
         returns it once per match, which is how the Files section shipped its
         Related-pages group as two identical slides. A Set makes the split
         idempotent no matter how the renderer nests a body. */
      var subs = [];
      ['details', '.cbody > details', 'div > details'].forEach(function (sel) {
        Array.prototype.forEach.call(el.querySelectorAll(':scope > ' + sel), function (s) {
          if (subs.indexOf(s) < 0) subs.push(s);
        });
      });
      if (subs.length) {
        subs.forEach(function (sub) {
          push(label, heading(sub) || '…', sub.querySelector(':scope > .cbody') || sub);
        });
      } else {
        var inner = el.cloneNode(true);
        var sm = inner.querySelector(':scope > summary');
        if (sm) sm.parentNode.removeChild(sm);
        push('', label, inner);
      }
    });

    return out;
  }

  /* ── the surface ───────────────────────────────────────────────────────────── */
  var slides = [], at = 0;

  function render() {
    var deck = document.getElementById(ID);
    if (!deck) return;
    var s = slides[at];
    if (!s) return;
    var art = deck.querySelector('.sd-slide');
    art.className = 'sd-slide ' + (s.klass || '');
    art.innerHTML = '';
    if (s.kicker) {
      var k = document.createElement('div');
      k.className = 'sd-kicker';
      k.textContent = s.kicker;
      art.appendChild(k);
    }
    var t = document.createElement('h1');
    t.className = 'sd-title';
    t.textContent = s.title;
    art.appendChild(t);
    if (s.body) {
      var b = document.createElement('div');
      b.className = 'sd-body';
      b.appendChild(s.body.cloneNode(true));
      art.appendChild(b);
    }
    deck.querySelector('.sd-count').textContent = (at + 1) + ' / ' + slides.length;
    /* The stage scrolls back to the top on every move. Without it a long slide
       leaves the next one opening halfway down, which reads as a skipped slide. */
    deck.querySelector('.sd-stage').scrollTop = 0;
  }

  function go(n) {
    if (!slides.length) return;
    at = Math.max(0, Math.min(slides.length - 1, n));
    render();
  }

  function keys(ev) {
    var deck = document.getElementById(ID);
    if (!deck || deck.hidden) return;
    if (ev.key === 'ArrowRight' || ev.key === 'PageDown' || ev.key === ' ') { go(at + 1); ev.preventDefault(); }
    else if (ev.key === 'ArrowLeft' || ev.key === 'PageUp') { go(at - 1); ev.preventDefault(); }
    else if (ev.key === 'Home') { go(0); ev.preventDefault(); }
    else if (ev.key === 'End') { go(slides.length - 1); ev.preventDefault(); }
    else if (ev.key === 'Escape') { close(); }
  }

  function shellFor() {
    /* The deck is drawn in the PAGE frame, which inside the 5599 viewer is the
       centre column. Escaping to the whole window would mean writing into the
       shell's document, and the shell owns the panes; a surface that repaints
       another pane is the thing the pane split exists to prevent. */
    return document;
  }

  function mount() {
    var d = document.getElementById(ID);
    if (d) return d;
    d = document.createElement('div');
    d.id = ID;
    d.hidden = true;
    d.innerHTML =
      '<div class="sd-stage"><article class="sd-slide"></article></div>'
      + '<footer class="sd-bar">'
      + '<button class="sd-nav" data-go="-1" type="button" title="previous (←)">‹</button>'
      + '<span class="sd-count"></span>'
      + '<button class="sd-nav" data-go="1" type="button" title="next (→)">›</button>'
      + '<span class="sd-hint">← → to move · Esc to close</span>'
      + '<button class="sd-x" type="button">✕ close</button>'
      + '</footer>';
    shellFor().body.appendChild(d);
    d.querySelectorAll('.sd-nav').forEach(function (b) {
      b.onclick = function () { go(at + (+b.dataset.go)); };
    });
    d.querySelector('.sd-x').onclick = close;
    document.addEventListener('keydown', keys, true);
    return d;
  }

  function close() {
    var d = document.getElementById(ID);
    if (d) d.hidden = true;
  }

  function open(page) {
    page = page || (window.boardPlugins && window.boardPlugins.livePage());
    if (!page) return;
    var d = mount();
    /* A SECOND CLICK PUTS IT AWAY. Every other surface here can be closed by the
       control that opened it, and one that could not was the first complaint the
       labeling panel got (JL 260807: "我关不掉labeling了"). */
    if (!d.hidden) return close();
    slides = build(page);
    at = 0;
    d.hidden = false;
    render();
  }

  if (window.boardPlugins) {
    window.boardPlugins.register({
      id: 'slides',
      label: '\u{1F39E} Slides',
      hint: 'read this page one section at a time',
      // 🔌 A PLUGIN, not a workflow: it stores nothing on the page and locks no step.
      menu: 'plugin',
      // The first entry that applies everywhere. Labeling gates on a page type; a
      // reading surface has nothing to gate on, because every page can be read.
      applies: function () { return true; },
      open: open
    });
  }

  window.boardSlidesOpen = open;   // for direct calls and for the tests
})();
