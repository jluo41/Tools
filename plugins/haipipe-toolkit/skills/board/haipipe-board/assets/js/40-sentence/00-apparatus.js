  if (!b) return;
  // The heading is now the section's own <summary>, so a click here would also
  // fold the section. Expand-all must not do that (JL 260725).
  ev.preventDefault();
  ev.stopPropagation();
  var sec = b.closest('.sect, .col, .f');
  if (!sec) return;
  var open = b.getAttribute('data-open') !== '1';
  sec.querySelectorAll('details.it').forEach(function (d) { d.open = open; });
  b.setAttribute('data-open', open ? '1' : '0');
  var lbl = b.querySelector('.lbl');
  if (lbl) lbl.textContent = open ? 'collapse all' : 'expand all';
});

/* ➕ sentence apparatus add (QA8, JL 260725): click a bare prose sentence, or the
   "➕ add to this sentence" row in an open drawer, and Save inserts `> Lane: text`
   directly under that sentence in the markdown (POST /_board/sentence). Script-only
   enhancement: without scripts the page still reads; writing needs serve.py anyway. */
(function () {

  /* ONE reading of "what this sentence says". `QC7`'s anchor is an EXACT match
     on this string against a source line, so anything the renderer added has to
     come back out. The ⚑ badge is the trap: it lives INSIDE the <p> (it became a
     zero-width span so it could never wrap), so a raw textContent posts
     "…below the read.⚑ 1", which is not in the markdown and never will be, and
     the server correctly answers "not found, nothing written" (JL 260801, with
     a screenshot of exactly that). Both writers on this page use this, and the
     address module reuses it rather than keeping a second copy. */
  function sentenceText(p) {
    var c = p.cloneNode(true);
    // 🪪 A SPAN CARD IS THE EXCEPTION TO THE RULE BELOW (JL 260802, QB5 D).
    // Every other button in a sentence is a paper-dialect chip, whose label
    // replaced a marker and is NOT the source text, so deleting it is what
    // makes the posted string match the file. A span card is the opposite: it
    // sits on words the author typed and its label IS those words. Deleting it
    // would post a sentence with a hole in it, and every later write on that
    // sentence would miss its anchor forever. So it is UNWRAPPED, not removed.
    c.querySelectorAll('button.chip.card.span').forEach(function (b) {
      b.parentNode.replaceChild(document.createTextNode(b.textContent), b);
    });
    // `.cmk` is the 💬 the comment layer inserts INSIDE the paragraph for every
    // pending comment it still holds in localStorage. It is added text, so a
    // sentence that once failed to write would post "…text 💬" and keep failing
    // forever, poisoned by the very comment that failed. `button` covers the
    // paper dialect's chips, whose LABEL is not the source text anyway
    // (`Smith 2024` for `\citep{smith2024}`), so both sides delete rather than
    // keep: the server strips the marker out of the source line to match.
    c.querySelectorAll('.cmk,.sbz,.sbadge,.cv,.schatbar,button,input,select,textarea')
      .forEach(function (x) { x.remove(); });
    return c.textContent.replace(/\s+/g, ' ').trim();
  }
  window.__boardSentenceText = sentenceText;
  var LANES = ['JL', 'CC', 'Note', 'Check', 'Citation', 'Value', 'Display',
               'Q-consumer', 'Link', 'Source'];
  var cur = null;
  function stamp() {
    var d = new Date(), z = function (n) { return (n < 10 ? '0' : '') + n; };
    return String(d.getFullYear()).slice(2) + z(d.getMonth() + 1) + z(d.getDate()) +
           ' ' + z(d.getHours()) + z(d.getMinutes());
  }
  function close() { if (cur) { cur.remove(); cur = null; } }
  function mk(afterEl, sentP, file) {
    close();
    var d = document.createElement('div');
    d.className = 'sadd';
    var sel = document.createElement('select');
    LANES.forEach(function (u) { sel.appendChild(new Option(u, u)); });
    try { sel.value = localStorage.getItem('board-sadd-last') || 'JL'; } catch (e) {}
    var inp = document.createElement('input');
    inp.type = 'text';
    inp.placeholder = 'Add to this sentence…';
    var ok = document.createElement('button'); ok.type = 'button'; ok.textContent = 'Save';
    var x = document.createElement('button'); x.type = 'button'; x.textContent = '✕';
    var err = document.createElement('span'); err.className = 'serr';
    d.append(sel, inp, ok, x, err);
    x.onclick = close;
    function save() {
      var text = inp.value.trim();
      if (!text) { inp.focus(); return; }
      try { localStorage.setItem('board-sadd-last', sel.value); } catch (e) {}
      err.textContent = '…';
      fetch('/_board/sentence', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: boardPath(), file: file,
          sentence: sentenceText(sentP),
          lane: sel.value, text: text })
      }).then(function (r) { return r.json(); })
        .then(function (j) {
          if (!j.ok) { err.textContent = '⚠ ' + (j.err || 'failed'); return; }
          err.textContent = '✔ saved';
          // CLOSE FIRST, THEN ASK (JL 260802). The swap refuses to run while
          // any textarea inside `div.wrap` still holds text, which is the rule
          // that stops a board rebuild from eating what someone is typing.
          // This form is inside `div.wrap` and its input still holds what was
          // just saved, so asking before closing asks for something that can
          // only be refused, and the lane then waited for the poll instead.
          close();
          if (window.__boardRefresh) window.__boardRefresh();
        })
        .catch(function () { err.textContent = '⚠ serve.py not running?'; });
    }
    ok.onclick = save;
    inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') save(); });
    afterEl.insertAdjacentElement('afterend', d);
    cur = d;
    inp.focus();
  }
  function edit(afterEl, sentP, file) {
    close();
    var before = sentenceText(sentP);
    var d = document.createElement('div');
    d.className = 'sedit';
    var inp = document.createElement('textarea'); inp.value = before;
    inp.setAttribute('aria-label', 'Edit this sentence');
    var who = document.createElement('input'); who.maxLength = 4;
    who.value = (localStorage.getItem('board-user-last') || 'JL').toUpperCase();
    who.setAttribute('aria-label', 'Your initials');
    var ok = document.createElement('button'); ok.type = 'button'; ok.textContent = 'Save';
    var x = document.createElement('button'); x.type = 'button'; x.textContent = 'Cancel';
    var err = document.createElement('span'); err.className = 'serr';
    d.append(inp, who, ok, x, err);
    x.onclick = close;
    function save() {
      var replacement = inp.value.replace(/\s+/g, ' ').trim();
      var actor = who.value.toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 4) || 'JL';
      if (!replacement || replacement === before) { inp.focus(); return; }
      err.textContent = '…';
      fetch('/_board/edit-sentence', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: boardPath(), file: file, sentence: before,
          replacement: replacement, who: actor, when: stamp() })
      }).then(function (r) { return r.json(); }).then(function (j) {
        if (!j.ok) { err.textContent = '⚠ ' + (j.err || 'failed'); return; }
        localStorage.setItem('board-user-last', actor);
        // A RELOAD IS THE WRONG TOOL HERE (JL 260802: adding something and
        // having the whole page refresh is what "not smooth" means). It threw
        // away the scroll position, shut every section the reader had opened
        // to reach this sentence, and cost a full document parse, all to show
        // one changed line. The swap keeps the reader exactly where they were
        // and still falls back to a real reload when the board's JS changed.
        //
        // CLOSE FIRST. This editor's textarea lives inside `div.wrap` and
        // still holds the sentence that was just saved, and the swap refuses
        // to run while any textarea in there has text, which is the rule that
        // stops a rebuild from eating what someone is typing. The reload this
        // replaced never met that rule, so the guard had never been crossed
        // here before: the markdown gained its `> ✎` record and the page sat
        // unchanged until the reader refreshed by hand.
        close();
        if (window.__boardRefresh) window.__boardRefresh();
        else location.reload();
      }).catch(function () { err.textContent = '⚠ serve.py not running?'; });
    }
    ok.onclick = save;
    inp.addEventListener('keydown', function (e) {
      if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') save();
      if (e.key === 'Escape') close();
    });
    afterEl.insertAdjacentElement('afterend', d);
    cur = d; inp.focus(); inp.select();
  }
  function openSentenceComment(p, afterEl) {
    var q = p && p.closest('section.slide.q');
    if (!q) return;
    var det = p.closest('details.sent');
    if (det) {
      det.open = true;
      var target = det.querySelector('summary p');
      var sapp = Array.from(det.children).find(function (x) {
        return x.classList && x.classList.contains('sapp');
      });
      mk(det.querySelector('.saddrow') || sapp || p, target, q.dataset.file);
      return;
    }
    mk(afterEl || p, p, q.dataset.file);
  }
  function openSentenceEdit(p, afterEl) {
    var q = p && p.closest('section.slide.q');
    if (!q) return;
    var det = p.closest('details.sent');
    if (det) {
      det.open = true;
      var sapp = Array.from(det.children).find(function (x) {
        return x.classList && x.classList.contains('sapp');
      });
      edit(det.querySelector('.saddrow') || sapp || p, det.querySelector('summary p'),
           q.dataset.file);
      return;
    }
    edit(afterEl || p, p, q.dataset.file);
  }
  document.addEventListener('click', function (e) {
    if (e.target.closest('.sadd')) return;
    var row = e.target.closest('.saddrow');
    if (row) {
      var det = row.closest('details.sent');
      var qr = row.closest('section.slide.q');
      if (det && qr) mk(row, det.querySelector('summary p'), qr.dataset.file);
    }
  });
  // DOUBLE-click edits the sentence.  Adding a lane remains available from the
  // explicit ➕ row, so editing never competes with attaching evidence.
  document.addEventListener('dblclick', function (e) {
    if (e.target.closest('.sadd')) return;
    var p = e.target.closest('p');
    // `summary` is NOT excluded (JL 260727). `QA8@boardform` says double-click
    // opens the form on a BARE sentence and a drawer gets its own ➕ row, which is
    // a real second path — but it is only reachable once the drawer is already
    // open, so on a sentence that carries evidence the gesture people actually
    // learned did nothing at all, silently. As the evidence card becomes the
    // default that stops being an edge case: 116 of this board's sentences are
    // already drawers. So both shapes now answer the same gesture.
    // The other clauses still cover what `summary` stood in for: the sentence text
    // resolves to the inner `p`, the `.sbadge` has no `p` ancestor so `!p` catches
    // it, and a marker is a `<button>`.
    if (!p || e.target.closest('a,code,button,select,input,textarea,mark')) return;
    if (!p.closest('section.slide.q')) return;
    if (p.closest('.sapp,.bd,.cmt,.cmb,.qh,.dadd,.spine')) return;
    e.preventDefault();
    if (window.getSelection) window.getSelection().removeAllRanges();
    // WHERE the form goes differs by shape, and getting this wrong is silent.
    // `mk` does `afterEl.insertAdjacentElement('afterend', …)`, so passing the
    // summary's own `p` would drop the form INSIDE the <summary>, where every
    // click toggles the drawer and the inputs cannot be used. A drawer therefore
    // takes the same two arguments the ➕ row path uses: insert at the END OF THE
    // DRAWER BODY, while still naming the summary's sentence as the target line.
    openSentenceEdit(p, p);
  });
  // ⧉ copy a WHOLE SECTION (JL 260725: section-level, not per-sentence):
  // every section heading carries a copy button; it copies the section's full
  // text (folded drawers and item explanations included) as clean plain text —
  // no badges, no forms, no highlight formatting.
  document.querySelectorAll('section.slide.q .ch').forEach(function (ch) {
    if (ch.querySelector('.chcopy')) return;
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'chcopy'; b.textContent = '⧉';
    b.title = 'Copy this section as plain text';
    b.addEventListener('click', function (e) {
      e.preventDefault(); e.stopPropagation();
      var box = ch.closest('summary') ? ch.closest('details') : ch.parentElement;
      var c = box.cloneNode(true);
      c.querySelectorAll('.ch,.sadd,.saddrow,.sbadge,button,select,input,textarea,.dadd')
        .forEach(function (x) { x.remove(); });
      if (c.tagName === 'DETAILS') c.open = true;   // the section itself may be folded
      c.querySelectorAll('details').forEach(function (d) { d.open = true; });
      c.style.cssText = 'position:absolute;left:-99999px;top:0;width:800px';
      document.body.appendChild(c);
      var t = c.innerText.replace(/\n{3,}/g, '\n\n').trim();
      c.remove();
      function done() { b.textContent = '✓'; setTimeout(function () { b.textContent = '⧉'; }, 700); }
      function fallback() {
        var ta = document.createElement('textarea');
        ta.value = t; document.body.appendChild(ta); ta.select();
        try { document.execCommand('copy'); } catch (e2) {}
        ta.remove(); done();
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(t).then(done, fallback);
      } else fallback();
    });
    ch.appendChild(b);
  });
  document.querySelectorAll('details.sent>.sapp').forEach(function (ap) {
    var r = document.createElement('div');
    r.className = 'saddrow';
    r.textContent = '➕ add to this sentence';
    ap.appendChild(r);
  });
