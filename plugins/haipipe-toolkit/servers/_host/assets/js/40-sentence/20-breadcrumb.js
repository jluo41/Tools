  /* Heading rails copy a source address and its full reading context. */
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
    return window.__boardReadableText(el);
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
  function headingRail(head, sec, path, short, blockEl) {
    if (head.querySelector(':scope > .hpath')) return;
    var rail = document.createElement('span');
    rail.className = 'hpath';
    // Content/terminal headings already display their generated address.
    if (!head.querySelector('.caddr,.haddr')) {
      var chip = document.createElement('span');
      chip.className = 'hpid';
      chip.textContent = short || path;
      chip.title = path;
      rail.appendChild(chip);
    }
    var copy = document.createElement('button');
    copy.type = 'button';
    copy.className = 'hcopy';
    copy.textContent = '⧉';
    copy.title = 'Copy prompt for ' + path;
    copy.setAttribute('aria-label', copy.title);
    copy.addEventListener('click', function (e) {
      e.preventDefault(); e.stopPropagation();
      window.__boardCopyPrompt(copy,
        window.__boardPromptText(sec, path, blockOf(blockEl()), ''));
    });
    rail.appendChild(copy);
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
    document.querySelectorAll('.hpath,.chcopy').forEach(function (x) { x.remove(); });
    document.querySelectorAll('section.slide.q').forEach(function (sec) {
      var SECT = 'details.sect, details.outline-section, details.qd';
      sec.querySelectorAll('.ch').forEach(function (ch) {
        var name = plainLabel(ch);
        if (!name) return;
        var box = ch.closest(SECT) || ch.parentElement || ch;
        headingRail(ch, sec, sec.id + ' / ' + name, shortLabel(name),
                    function () { return box; });
      });
      function subPath(el) {
        var head = ownHead(el.closest(SECT + ', .folds'));
        var parent = head ? plainLabel(head) : '';
        return [sec.id, parent, plainLabel(el)].filter(Boolean).join(' / ');
      }
      sec.querySelectorAll('.sh').forEach(function (sh) {
        if (!plainLabel(sh)) return;
        headingRail(sh, sec, subPath(sh), shortLabel(plainLabel(sh)),
                    function () { return shRun(sh); });
      });
      sec.querySelectorAll('.ph.heading-target').forEach(function (head) {
        headingRail(head, sec, head.dataset.headingRef, head.dataset.headingId,
                    function () { return head; });
      });
      sec.querySelectorAll('details.csec > summary').forEach(function (sm) {
        if (!plainLabel(sm)) return;
        // `C1` comes from 10-address.js, which runs first; the visible `.caddr`
        // chip beside it is the same id, so this rail shows no second copy of
        // it and contributes only the ⧉ copy button.
        var cid = (sm.parentElement && sm.parentElement.dataset)
          ? sm.parentElement.dataset.contentId : '';
        // Aims and States groups fold like Content divisions since 260802, so
        // they arrive here too. They have no `C1` from the sentence grammar,
        // and the fallback printed the WHOLE title beside a heading already
        // showing it (JL 260802: "they are nested together"). Their own id is
        // the first token of the heading, `A0` or `P`, so use that.
        if (!cid) cid = shortLabel(plainLabel(sm));
        headingRail(sm, sec, subPath(sm), cid || plainLabel(sm),
                    function () { return sm.parentElement; });
      });
    });
  }
  window.__boardWireSentenceChats = function () {
    wireSentenceCopies();
    wireHeadingPaths();
  };
  wireSentenceCopies();
  wireHeadingPaths();
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
