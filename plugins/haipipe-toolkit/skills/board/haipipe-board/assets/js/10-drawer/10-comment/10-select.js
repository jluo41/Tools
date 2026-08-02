  /* ── select -> floating button ───────────────────────────── */
  function hideBtns() { btn.style.display = 'none'; cbtn.style.display = 'none'; }
  document.addEventListener('mouseup', function (ev) {
    if (box.contains(ev.target) || panel.contains(ev.target)
        || ev.target === btn || ev.target === cbtn) return;
    setTimeout(function () {
      var s = window.getSelection();
      var txt = s && String(s).trim();
      if (!txt || txt.length < 2 || !s.rangeCount) { hideBtns(); return; }
      var node = s.anchorNode;
      node = node.nodeType === 1 ? node : node.parentNode;
      var q = node.closest && node.closest('section.q');
      if (!q) { hideBtns(); return; }
      var live = s.getRangeAt(0);
      var sentence = containingSentence(live);
      if (!sentence) { hideBtns(); return; }
      var r = live.getBoundingClientRect();
      pend = { id: q.id, file: q.getAttribute('data-file') || '',
               quote: txt, sentence: sentence, range: live.cloneRange() };
      btn.style.left = (r.left + window.scrollX) + 'px';
      btn.style.top = (r.bottom + window.scrollY + 7) + 'px';
      btn.style.display = 'block';
      // 🪪 offered only when the words are ACTUALLY IN the sentence. A card
      // binds by matching them in the source line, so a selection that spans
      // a code span or crosses two sentences has nothing to bind with, and
      // showing a button that can only fail is worse than showing none.
      cbtn.style.display = sentence.indexOf(txt) >= 0 && txt.indexOf(':') < 0
        ? 'block' : 'none';
      cbtn.style.left = (r.left + window.scrollX + btn.offsetWidth + 6) + 'px';
      cbtn.style.top = btn.style.top;
    }, 0);
  });

  /* ── 🪪 write a card on the selected words ─────────────────────────────
     Reuses the comment composer, minus the person: a card says what a phrase
     IS, and no author's initials belong on that. */
  cbtn.onclick = function () {
    hideBtns();
    var words = pend.quote;
    box.querySelector('.qq').textContent = '\u{1FAAA} ' + words;
    box.querySelector('select').style.display = 'none';
    box.querySelector('.nu').style.display = 'none';
    var ta = box.querySelector('textarea');
    ta.value = '';
    ta.placeholder = 'What should open when someone clicks “' + words + '”…';
    box.style.left = btn.style.left; box.style.top = btn.style.top;
    box.style.display = 'block';
    ta.focus();
    box.dataset.mode = 'card';
  };

  function fillWho() {
    var sel = box.querySelector('select'), last = localStorage.getItem(WK) || users[0];
    sel.innerHTML = users.map(function (u) {
      return '<option' + (u === last ? ' selected' : '') + '>' + u + '</option>';
    }).join('') + '<option value="__new">+ new person…</option>';
    sel.onchange = function () {
      var nu = box.querySelector('.nu');
      if (sel.value === '__new') { nu.style.display = 'block'; nu.value = ''; nu.focus(); }
      else { nu.style.display = 'none'; localStorage.setItem(WK, sel.value); }
    };
  }
  box.querySelector('.nu').onkeydown = function (ev) {
    if (ev.key !== 'Enter') return;
    ev.preventDefault();
    var v = this.value.trim().toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 4);
    if (!v) return;
    if (users.indexOf(v) < 0) users.push(v);
    localStorage.setItem(UK, JSON.stringify(users));
    localStorage.setItem(WK, v);
    this.style.display = 'none'; fillWho();
  };

  btn.onclick = function () {
    hideBtns();
    box.dataset.mode = 'comment';
    fillWho(); box.querySelector('.nu').style.display = 'none';
    box.querySelector('select').style.display = '';
    box.querySelector('.qq').textContent = pend.quote;
    var ta = box.querySelector('textarea');
    ta.value = ''; ta.placeholder = 'Write a comment…';
    box.style.left = btn.style.left; box.style.top = btn.style.top;
    box.style.display = 'block';
    ta.focus();
  };
  box.querySelector('.cx').onclick = function () { box.style.display = 'none'; };
  box.querySelector('.cs').onclick = function () {
    var v = box.querySelector('textarea').value.trim();
    if (!v) return;
    if (box.dataset.mode === 'card') {
      var words = pend.quote, file = pend.file;
      var save = box.querySelector('.cs');
      // The composer stays OPEN until the server says it wrote. A refusal is
      // the whole reason this endpoint has three gates, and closing the box on
      // the way out would throw away what the person had just typed.
      save.disabled = true; save.textContent = 'Saving…';
      post('/_board/card', { file: file, sentence: pend.sentence, span: words, text: v })
        .then(function (j) {
          save.disabled = false; save.textContent = 'Save';
          if (!j) { say('The Board server is not running, so no card was written'); return; }
          if (!j.ok) { say(j.err || 'the card was not written'); return; }
          // A successful write rebuilds, so the card appearing on the words IS
          // the confirmation and a toast would only say it again. Only the
          // failures above still need words.
          box.style.display = 'none';
          // Clear the selection BEFORE refreshing: the swap holds itself back
          // while text is selected, on the assumption that the reader is still
          // working on it, and this selection is the one we just consumed.
          window.getSelection().removeAllRanges();
          // Do not wait for the poll to notice. The writer already knows the
          // file changed, so ask for the swap now: it is the difference
          // between the words lighting up at once and up to 800ms of nothing.
          if (window.__boardRefresh) window.__boardRefresh();
        })
        .catch(function () {
          save.disabled = false; save.textContent = 'Save';
          say('The Board server did not answer');
        });
      return;
    }
    var who = box.querySelector('select').value;
    if (who === '__new') who = users[0];
    localStorage.setItem(WK, who);
    var live = pend.range;
    db.push({ id: pend.id, file: pend.file, quote: pend.quote, sentence: pend.sentence,
              who: who, text: v });
    var idx = db.length - 1;
    box.style.display = 'none';
    /* wrap the live range FIRST — guaranteed exact, no text search involved */
    var ok = false;
    try { ok = wrapRange(live, idx); } catch (e) { ok = false; }
    window.getSelection().removeAllRanges();
    db[idx].lost = !ok;
    localStorage.setItem(KEY, JSON.stringify(db));
    if (!ok) marks();
    paint();
    /* 这一次点击本身就是用户手势 —— 直接写盘，不用再点 Sync */
    drain(true).then(function (n) {
      if (n && srvOK) {
        // Same reason as the card path: the comment appearing under its
        // sentence is the confirmation, and asking for the swap now is what
        // makes it feel like one action instead of a save and then a wait.
        window.getSelection().removeAllRanges();
        if (window.__boardRefresh) window.__boardRefresh();
      }
      if (n) say((ok ? 'Highlighted and ' : 'Saved (not anchored) and ') +
                 'written to ' + pend.file + (srvOK ? ' — rendered below the sentence'
                                                    : ' — rebuild to render it'));
      else say(ok ? 'Highlighted — ' + db.length + ' pending (no folder access yet)'
                  : 'Saved, but could not anchor it (see ⚠ in the panel)');
    });
  };
