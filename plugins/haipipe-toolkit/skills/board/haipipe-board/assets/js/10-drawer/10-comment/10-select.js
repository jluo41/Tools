  /* ── select -> floating button ───────────────────────────── */
  document.addEventListener('mouseup', function (ev) {
    if (box.contains(ev.target) || panel.contains(ev.target) || ev.target === btn) return;
    setTimeout(function () {
      var s = window.getSelection();
      var txt = s && String(s).trim();
      if (!txt || txt.length < 2 || !s.rangeCount) { btn.style.display = 'none'; return; }
      var node = s.anchorNode;
      node = node.nodeType === 1 ? node : node.parentNode;
      var q = node.closest && node.closest('section.q');
      if (!q) { btn.style.display = 'none'; return; }
      var live = s.getRangeAt(0);
      var sentence = containingSentence(live);
      if (!sentence) { btn.style.display = 'none'; return; }
      var r = live.getBoundingClientRect();
      pend = { id: q.id, file: q.getAttribute('data-file') || '',
               quote: txt, sentence: sentence, range: live.cloneRange() };
      btn.style.left = (r.left + window.scrollX) + 'px';
      btn.style.top = (r.bottom + window.scrollY + 7) + 'px';
      btn.style.display = 'block';
    }, 0);
  });

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
    btn.style.display = 'none';
    fillWho(); box.querySelector('.nu').style.display = 'none';
    box.querySelector('.qq').textContent = pend.quote;
    box.querySelector('textarea').value = '';
    box.style.left = btn.style.left; box.style.top = btn.style.top;
    box.style.display = 'block';
    box.querySelector('textarea').focus();
  };
  box.querySelector('.cx').onclick = function () { box.style.display = 'none'; };
  box.querySelector('.cs').onclick = function () {
    var v = box.querySelector('textarea').value.trim();
    if (!v) return;
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
      if (n) say((ok ? 'Highlighted and ' : 'Saved (not anchored) and ') +
                 'written to ' + pend.file + (srvOK ? ' — reload to see it rendered'
                                                    : ' — rebuild to render it'));
      else say(ok ? 'Highlighted — ' + db.length + ' pending (no folder access yet)'
                  : 'Saved, but could not anchor it (see ⚠ in the panel)');
    });
  };
