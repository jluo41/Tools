  /* ── Section and subsection breadcrumbs (QB5d) ────────────────────────────
     Above Content's fine `C.H.P.S` grammar sits a coarser address every reader
     can say out loud: `QB4 / State / Decision Now`. Every rendered `##`
     section and `###` subsection heading gets one, at the END of the heading
     and invisible until that heading is hovered — the contract the sentence
     rail and the C/H chips already follow.

     The chip copies the address plus the markdown source path, so Claude Code
     can open the right file without guessing; `🤖` focuses THIS page's existing
     chat on that heading. Both are generated per render: nothing is written
     into the markdown, and a live refresh recomputes them because this runs
     inside the rewire below. */
  function plainLabel(el) {
    // An address is spoken and pasted, so it carries the NAME only: not the
    // heading's emoji, not its `1/7` progress count, not `· 6 sections`.
    var c = (el.querySelector(':scope > .chl') || el).cloneNode(true);
    c.querySelectorAll('.hpath,.chcopy,.caddr,.haddr,.shc,.cnt,button')
      .forEach(function (x) { x.remove(); });
    return c.textContent.replace(/\s+/g, ' ').trim()
      .replace(/^[^\p{L}\p{N}]+/u, '')
      .replace(/\s·\s\d+\s+\w+$/, '')
      .trim();
  }
  function blockOf(el) {
    // innerText needs layout, so the clone is measured off-screen and removed.
    var c = el.cloneNode(true);
    c.querySelectorAll('.hpath,.schatbar,.sadd,.saddrow,.dadd,button,select,input,textarea')
      .forEach(function (x) { x.remove(); });
    if (c.tagName === 'DETAILS') c.open = true;
    c.querySelectorAll('details').forEach(function (d) { d.open = true; });
    c.style.cssText = 'position:absolute;left:-99999px;top:0;width:800px';
    document.body.appendChild(c);
    var t = c.innerText.replace(/\n{3,}/g, '\n\n').trim();
    c.remove();
    return t.length > 1600 ? t.slice(0, 1600) + '\n…' : t;
  }
  function shRun(sh) {
    // A `###` outside Content is a flat `div.sh`; its block is the run of
    // siblings up to the next one.
    var box = document.createElement('div');
    box.appendChild(sh.cloneNode(true));
    var n = sh.nextElementSibling;
    while (n && !(n.classList && n.classList.contains('sh'))) {
      box.appendChild(n.cloneNode(true));
      n = n.nextElementSibling;
    }
    return box;
  }
  function copyInto(btn, text, label) {
    function done() {
      var old = btn.textContent;
      btn.textContent = label || '✓';
      setTimeout(function () { btn.textContent = old; }, 700);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, done);
      return;
    }
    var ta = document.createElement('textarea');
    ta.value = text; document.body.appendChild(ta); ta.select();
    try { document.execCommand('copy'); } catch (e) {}
    ta.remove(); done();
  }
  /* The chip SHOWS the short id and COPIES the full address (JL 260801: "the
     address here is too long ... maybe just C1 is ok, when I click C1, I can
     copy the link"). Two different jobs were being served by one string: the
     reader needs a token they can see at a glance and say out loud, and Claude
     Code needs `QB4 / Content / 0 · The page protocol · <file>` to open the
     right place. So the label shrinks and the clipboard payload does not.
     A Content division already carries `C1` from the sentence grammar, so it
     reuses that id rather than inventing a second one; everywhere else the
     page id drops off the front, since the tab and the breadcrumb both
     already say which page this is. */
  function headingRail(head, sec, path, short, file, blockEl, withCopy) {
    if (head.querySelector(':scope > .hpath')) return;
    var rail = document.createElement('span');
    rail.className = 'hpath';
    var chip = document.createElement('button');
    chip.type = 'button';
    chip.className = 'hpid';
    chip.textContent = short || path;
    chip.title = 'Copy this address' + (file ? '\n' + path + '\n' + file : '');
    chip.addEventListener('click', function (e) {
      e.preventDefault(); e.stopPropagation();
      copyInto(chip, path + (file ? ' · ' + file : ''), '✓ copied');
    });
    rail.appendChild(chip);
    if (withCopy) {                 // `##` headings already carry their own ⧉
      var cp = document.createElement('button');
      cp.type = 'button';
      cp.className = 'hcopy';
      cp.textContent = '⧉';
      cp.title = 'Copy this subsection as plain text';
      cp.addEventListener('click', function (e) {
        e.preventDefault(); e.stopPropagation();
        copyInto(cp, blockOf(blockEl()), '✓');
      });
      rail.appendChild(cp);
    }
    var bot = document.createElement('button');
    bot.type = 'button';
    bot.className = 'hchat';
    bot.textContent = '🤖';
    bot.title = 'Chat about ' + path;
    bot.addEventListener('click', function (e) {
      e.preventDefault(); e.stopPropagation();
      if (window.__boardHeadingChat) {
        window.__boardHeadingChat(sec, path, blockOf(blockEl()), file);
      }
    });
    rail.appendChild(bot);
    head.appendChild(rail);
  }
  function shortLabel(label) {
    /* The chip is a HANDLE, not a caption (JL 260802: "we don't want this long
       copy button, please make them the same to the Content"). A Content part
       shows `C1`; every other group heading now shows only what comes before
       its first ` · `, so `⚙️ Engines · what RUNS this subject` becomes
       `Engines` instead of repeating the whole heading the reader is looking
       at. The clipboard still carries the full address. */
    var id = label.match(/^((?:A\d+|C\d+|P\d*))\s*·/);
    if (id) return id[1];
    var head = label.split(' · ')[0].trim();
    return head.replace(/^[^\p{L}\p{N}]+/u, '').trim() || label;
  }

  function ownHead(host) {
    return host ? host.querySelector(':scope > summary.ch, :scope > .ch') : null;
  }
  function wireHeadingPaths() {
    document.querySelectorAll('.hpath').forEach(function (x) { x.remove(); });
    document.querySelectorAll('section.slide.q').forEach(function (sec) {
      var file = sec.getAttribute('data-file') || '';
      var SECT = 'details.sect, details.diagram-section, details.qd';
      sec.querySelectorAll('.ch').forEach(function (ch) {
        var name = plainLabel(ch);
        if (!name) return;
        var box = ch.closest(SECT) || ch.parentElement || ch;
        headingRail(ch, sec, sec.id + ' / ' + name, shortLabel(name), file,
                    function () { return box; }, false);
      });
      function subPath(el) {
        var head = ownHead(el.closest(SECT + ', .folds'));
        var parent = head ? plainLabel(head) : '';
        return [sec.id, parent, plainLabel(el)].filter(Boolean).join(' / ');
      }
      sec.querySelectorAll('.sh').forEach(function (sh) {
        if (!plainLabel(sh)) return;
        headingRail(sh, sec, subPath(sh), shortLabel(plainLabel(sh)), file,
                    function () { return shRun(sh); }, true);
      });
      sec.querySelectorAll('details.csec > summary').forEach(function (sm) {
        if (!plainLabel(sm)) return;
        // `C1` comes from 10-address.js, which runs first; the visible `.caddr`
        // chip beside it is the same id, so this rail shows no second copy of
        // it and contributes only the ⧉ and 🤖 buttons.
        var cid = (sm.parentElement && sm.parentElement.dataset)
          ? sm.parentElement.dataset.contentId : '';
        // Aims and States groups fold like Content divisions since 260802, so
        // they arrive here too. They have no `C1` from the sentence grammar,
        // and the fallback printed the WHOLE title beside a heading already
        // showing it (JL 260802: "they are nested together"). Their own id is
        // the first token of the heading, `A0` or `P`, so use that.
        if (!cid) cid = shortLabel(plainLabel(sm));
        headingRail(sm, sec, subPath(sm), cid || plainLabel(sm), file,
                    function () { return sm.parentElement; }, true);
      });
    });
  }
  window.__boardWireSentenceChats = function () {
    wireSentenceChats();
    wireHeadingPaths();
  };
  wireSentenceChats();
  wireHeadingPaths();
  document.addEventListener('click', function () {
    document.querySelectorAll('.schatbar.menu-open').forEach(function (bar) {
      bar.classList.remove('menu-open');
      var more = bar.querySelector('.smore');
      if (more) more.setAttribute('aria-expanded', 'false');
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    close();
    document.querySelectorAll('.schatbar.menu-open').forEach(function (bar) {
      bar.classList.remove('menu-open');
      var more = bar.querySelector('.smore');
      if (more) more.setAttribute('aria-expanded', 'false');
    });
  });
})();

/* A chip inside a sentence's <summary> also toggles that sentence's drawer on
   its way to opening its own panel. That is left alone ON PURPOSE.

   The first version called e.preventDefault() here to stop the drawer flapping.
   Showing a popover IS the button's default action, so that cancelled the panel
   as well: on every sentence carrying a `>` lane, clicking a chip did nothing at
   all. A cosmetic guard silently disabled the feature it was decorating, and it
   only showed up on the composite example, where every chip sits in a lane.

   Opening the drawer is not a defect anyway: the lane under the sentence holds
   the same evidence the panel is about, so getting both is better than either.
   If this ever does need suppressing, it must NOT use preventDefault; restore
   `details.open` on the next animation frame instead. */

/* AND THE REAL CAUSE WAS NEITHER OF THOSE (JL 260726: "for the values,
   displays, figures, I cannot click them"). No handler belongs here at all.

   The story this file told for one revision was wrong, and the measurement
   that killed it is worth keeping: with a click handler added to force the
   panel open, chips inside a <summary> opened; with it removed, they ALSO
   opened. So <summary> was never swallowing anything, and element.click()
   was the wrong instrument, because it skips hit-testing. Testing what a real
   MOUSE would hit found 11 of 11 chips unreachable: `.fig`, meant for markdown
   images, also matched every figure PANEL (class `chipcard disp fig ready`),
   and its display:block beat the UA rule that hides a closed popover. Five
   invisible full-width panels sat over the page eating every click.

   Fixed in board.css by scoping that rule to `img.fig`, plus an explicit
   `.chipcard:not(:popover-open){display:none}` so no future class collision
   can resurrect a ghost. The chip needs NO script: `popovertarget` alone is
   enough, inside a <summary> or out of it, verified in Chrome 150. */
