/* 🎞 Slides · write THIS page out as a real html-ppt deck, and show it.
 *
 * WHAT THIS FILE OWNS, and it is one thing: WHAT A SLIDE IS. It reflows the open
 * page's rendered DOM into an ordered list of {kicker, title, body} and posts it
 * to `/_board/deck`. It holds no opinion about what a deck looks like.
 *
 * WHAT html-ppt OWNS: everything else. `live/deck.py` wraps these slides in the
 * skill's own shell, so the deck gets base.css, a theme, and runtime.js, which
 * means ← → to move, T to cycle themes, F fullscreen, O overview and S presenter
 * mode with the speaker cards. None of that is reimplemented here and none of it
 * is copied; the deck links straight at the skill's files.
 *
 * IT WAS NOT ALWAYS THIS WAY, and the first version is why the note exists. It
 * painted its own slides in this document with its own stylesheet: the board was
 * quietly growing a second presentation system beside the one the display plugin
 * already maintains, and the deck vanished on Escape with no file behind it. JL
 * asked for the skill to generate the slides and for the result to be embedded
 * (260808), which is both of those problems answered by the same move.
 *
 * WHY IT WORKS AT ALL: board pages were already slide-shaped and nobody had used
 * it. Every Content division opens with a bold caption line and every subdivision
 * with a parenthetical, so the reflow reads titles the page grammar guarantees are
 * there. It needs no model and makes no editorial choice.
 *
 * IT IS STILL NOT AN AUTHORED DECK. The words are the page's own, so a division
 * arrives as its paragraph rather than as three bullets. `page-type: slide` and
 * its QBt9 specimen stay the authored path, where a person writes the talk and
 * accepts each render. This claims nothing, so it needs no acceptance.
 *
 * WHY A PLUGIN AND NOT A WORKFLOW. It stores nothing on the page and locks no
 * step; it is a surface you look through. That is the whole test the two menus
 * split on, and this entry is the first that applies to EVERY page, which is the
 * case the registry was built for and had never carried.
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
    /* `.schatbar` and `.smenu` are the SENTENCE APPARATUS, injected after load and
       therefore invisible in the HTML on disk. On the page they are quiet controls
       beside a sentence; cloned into a deck they print as bare text, so every slide
       of QBt1 carried a stack of "C1.P1.S1 / QBt1.C1.P1.S1" between its sentences
       and half the slide was ids (JL 260810: "the quality is not that good"). They
       are stripped by WRAPPER, not by the `.sidchip` inside, because removing the
       chip alone leaves the empty bar holding its own vertical space. */
    c.querySelectorAll('.secall,.cpy,.copy,.sb-x,.schatbar,.smenu,button')
      .forEach(function (b) { b.parentNode && b.parentNode.removeChild(b); });
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

    return chunk(out);
  }

  /* A SECTION IS NOT A SLIDE, which the first version assumed. Measured on QBt1:
     22 slides carrying 138 to 2231 characters, and the 2231 one rendered at 118%
     of the box, so its foot was cut off. One heading can hold a paragraph or a
     whole figure plus four subdivisions, and nothing in the page grammar bounds it.

     So the split MEASURES instead of counting headings. An over-long body is cut at
     its own TOP-LEVEL child boundaries, never inside one: a `<pre>` figure cut down
     the middle is worse than a tall slide, because the reader cannot tell the halves
     apart. A single child already over the limit therefore stays whole and overflows,
     which the deck scrolls rather than clips. */
  var LIMIT = 1500;   // characters of body text; about a screenful at deck size

  function chunk(slides) {
    var out = [];
    slides.forEach(function (s) {
      var b = s.body;
      if (!b || txt(b).length <= LIMIT || b.children.length < 2) { out.push(s); return; }
      /* A SPLIT THAT CANNOT HELP MUST NOT HAPPEN. When one child is already over
         the limit, cutting at child boundaries only peels the small ones off it:
         the first attempt turned QBt1's ASCII section into a 7-character slide
         followed by a 2249-character one still at 127%, which is the original
         problem plus a useless slide. A lone oversized figure stays whole and the
         deck scrolls it. */
      var big = 0;
      Array.prototype.forEach.call(b.children, function (k) {
        big = Math.max(big, (k.textContent || '').length);
      });
      if (big > LIMIT) { out.push(s); return; }
      var parts = [], cur = document.createElement('div'), used = 0;
      Array.prototype.slice.call(b.children).forEach(function (kid) {
        var len = (kid.textContent || '').length;
        if (used && used + len > LIMIT) {
          parts.push(cur); cur = document.createElement('div'); used = 0;
        }
        cur.appendChild(kid.cloneNode(true));
        used += len;
      });
      if (cur.children.length) parts.push(cur);
      parts.forEach(function (p, i) {
        out.push({ kicker: s.kicker, klass: s.klass, body: p,
                   /* a continuation says so in the TITLE, because a reader who
                      arrives mid-section otherwise reads it as a repeated heading */
                   title: i === 0 ? s.title : s.title + ' (' + (i + 1) + ')' });
      });
    });
    return out;
  }
  /* ── the surface: an html-ppt deck, in an iframe ─────────────────────────────
     WHY AN IFRAME AND NOT MORE DIVS. The first version painted its own slides in
     this document with its own stylesheet, which meant the board was quietly
     growing a second presentation system beside the one the display plugin
     already maintains. html-ppt has 36 themes, the T key, F, O, and S presenter
     mode with speaker cards; none of that is worth rewriting and all of it comes
     free the moment the slides live in a real deck file (JL 260808).

     The seam runs at the SERVER, not here: this posts the slides it cut, and
     live/deck.py wraps them in html-ppt's shell and writes the file. So this file
     still owns exactly one thing, what a slide is, and owns no opinion at all
     about what a deck looks like. */

  var url = '';           // where the last written deck lives

  function pageFile(page) {
    return (page && page.getAttribute('data-file')) || '';
  }

  function board() {
    try { return boardPath(); } catch (e) { return location.pathname; }
  }

  function mount() {
    var d = document.getElementById(ID);
    if (d) return d;
    d = document.createElement('div');
    d.id = ID;
    d.hidden = true;
    d.innerHTML =
      '<div class="sd-head">'
      + '<span class="sd-what">🎞 <b>Slides</b></span>'
      + '<span class="sd-note">writing the deck…</span>'
      + '<span class="sd-sp"></span>'
      + '<a class="sd-open" target="_blank" rel="noopener" hidden>↗ open on its own</a>'
      + '<button class="sd-x" type="button">✕ close</button>'
      + '</div>'
      + '<iframe class="sd-frame" title="slides"></iframe>';
    document.body.appendChild(d);
    d.querySelector('.sd-x').onclick = close;
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
    /* The frame is blanked, not merely hidden: a deck left loaded keeps
       html-ppt's runtime listening for arrow keys behind the page. */
    d.querySelector('.sd-frame').src = 'about:blank';
  }

  function note(d, msg) { d.querySelector('.sd-note').textContent = msg; }

  /* A slide's body is HTML because it IS HTML: the page's own rendered nodes,
     cloned. Serialising them here is what lets the server be a pure template
     with no parser of its own. */
  function payload(page) {
    return build(page).map(function (s) {
      var t = s.body ? txt(s.body) : '';
      return { kicker: s.kicker || '', title: s.title || '',
               /* A slide the split could not rescue (one oversized child) is
                  flagged so the deck can set it smaller rather than let it run
                  off the bottom. Measured, not guessed: QBt1's ASCII figure was
                  128% of the box. */
               dense: t.length > LIMIT,
               body: s.body ? s.body.innerHTML : '' };
    });
  }

  /* SLIDES IS A MODE, NOT A PANE (JL 260810). Measured at 1600x970 it is
     100% x 100% at z-index 120, so opening it left Draw and the workflow strip
     alive and invisible underneath. One thing on screen is the entire point of
     it, so the others are PUT AWAY rather than covered.
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

  function open(page) {
    page = page || (window.boardPlugins && window.boardPlugins.livePage());
    if (!page) return;
    var d = mount();
    if (!d.hidden) return close();       // a second click puts it away

    var slides = payload(page);
    putOthersAway();
    d.hidden = false;
    note(d, 'writing ' + slides.length + ' slides…');
    d.querySelector('.sd-open').hidden = true;

    fetch('/_board/deck', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        path: board(), file: pageFile(page),
        title: (page.getAttribute('data-title') || page.id || 'deck'),
        foot: page.id || '', slides: slides
      })
    }).then(function (r) { return r.json(); })
      .then(function (j) {
        if (!j.ok) { note(d, '⚠ ' + (j.err || 'the deck was not written')); return; }
        url = j.url;
        note(d, j.n + ' slides · theme ' + j.theme
                + ' · ← → move, T theme, F full, O overview, S presenter');
        /* `?plain` OR YOU GET A BOARD INSIDE A BOARD. The server wraps any .html
           it serves in the operating shell, so the bare deck URL returns the
           three-pane viewer with the deck hidden in its page frame: a bar, a
           sidebar and a Plugin menu, nested inside the panel that a Plugin menu
           just opened. `?plain` is the board's own escape from that, and it is
           what the shell's own "↗ plain" link uses. */
        var a = d.querySelector('.sd-open');
        a.href = url + '?plain'; a.hidden = false;
        d.querySelector('.sd-frame').src = url + '?plain';
      })
      .catch(function (e) { note(d, '⚠ ' + e); });
  }

  if (window.boardPlugins) {
    window.boardPlugins.register({
      id: 'slides',
      label: '\u{1F39E} Slides',
      hint: 'write this page as an html-ppt deck, and show it',
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
