  /* ── index structure controls (QC2, JL 260724): add / archive groups and
     questions straight from the front page. Every button is only a WRITER:
     POST /_board/structure edits board.md (and seeds/moves the Q files), the
     server rebuilds, and the live watcher (QD6) swaps the new index in place.
     Archive never deletes: files move to _archive/ inside the board folder. */
  function structPost(op, extra, okMsg) {
    var payload = { op: op };
    Object.keys(extra).forEach(function (k) { payload[k] = extra[k]; });
    post('/_board/structure', payload).then(function (j) {
      if (!j) { say('No live server behind this page'); return; }
      if (!j.ok) { say(j.err || 'failed'); return; }
      say(okMsg(j));
      if (window.__boardRefresh) window.__boardRefresh();
    }).catch(function () { say('No live server behind this page'); });
  }
  function arm(btn, fire) {
    /* two-step confirm, no native dialogs: first click arms, second fires */
    if (btn._armT) {
      clearTimeout(btn._armT); btn._armT = null;
      btn.classList.remove('arm'); btn.textContent = btn._lbl;
      fire(); return;
    }
    btn._lbl = btn.textContent;
    btn.classList.add('arm'); btn.textContent = 'sure?';
    btn._armT = setTimeout(function () {
      btn._armT = null; btn.classList.remove('arm'); btn.textContent = btn._lbl;
    }, 2600);
  }
  function miniForm(anchor, fields, onGo) {
    var old = document.querySelector('.gform');
    if (old) old.remove();
    var f = document.createElement('span');
    f.className = 'gform';
    var ins = fields.map(function (ph) {
      var i = document.createElement('input');
      i.placeholder = ph; f.appendChild(i); return i;
    });
    var go = document.createElement('button'); go.className = 'go'; go.textContent = 'Add';
    var cx = document.createElement('button'); cx.className = 'cx2'; cx.textContent = '×';
    f.appendChild(go); f.appendChild(cx);
    go.onclick = function () {
      var vals = ins.map(function (i) { return i.value.trim(); });
      if (!vals[0]) { ins[0].focus(); return; }
      f.remove(); onGo(vals);
    };
    cx.onclick = function () { f.remove(); };
    ins.forEach(function (i) {
      i.onkeydown = function (ev) {
        if (ev.key === 'Enter') go.onclick();
        if (ev.key === 'Escape') cx.onclick();
      };
    });
    anchor.appendChild(f);
    ins[0].focus();
  }
  function wireStruct() {
    document.querySelectorAll('div.grp').forEach(function (g) {
      if (g.querySelector('.gadd')) return;
      var name = g.getAttribute('data-g') || '';
      var add = document.createElement('button');
      add.className = 'gadd'; add.type = 'button'; add.textContent = '＋ Q';
      add.title = 'Add a question to ' + name;
      add.onclick = function () {
        miniForm(g, ['new question title'], function (v) {
          structPost('add_question', { group: name, title: v[0] },
            function (j) { return 'Added ' + j.file; });
        });
      };
      var gc = document.createElement('button');
      gc.className = 'gchat'; gc.type = 'button'; gc.textContent = '\u{1F4AC}';
      gc.title = 'Chat about this group (SDK drawer; \u2328 inside switches to the CLI)';
      gc.onclick = function () { chatOpen({ group: name }); };
      g.appendChild(gc);
      var del = document.createElement('button');
      del.className = 'garch'; del.type = 'button'; del.textContent = '\u{1F5C4}';
      del.title = 'Archive this group (only when it lists no questions)';
      del.onclick = function () {
        arm(del, function () {
          structPost('archive_group', { group: name },
            function (j) { return 'Archived group ' + j.group; });
        });
      };
      g.appendChild(add); g.appendChild(del);
    });
    document.querySelectorAll('a.ir[data-f]').forEach(function (row) {
      if (row.querySelector('.qarch')) return;
      var b = document.createElement('span');
      b.className = 'qarch'; b.textContent = '\u{1F5C4}';
      b.title = 'Archive ' + row.getAttribute('data-f') +
        ' (moves to _archive/, never deletes)';
      b.onclick = function (ev) {
        ev.preventDefault(); ev.stopPropagation();
        arm(b, function () {
          structPost('archive_question', { q: row.getAttribute('data-f') },
            function (j) { return 'Archived ' + j.file + ' → ' + j.to; });
        });
      };
      row.appendChild(b);
    });
    var idxBox = document.querySelector('div.idx');
    if (idxBox && !idxBox.querySelector('.gnew')) {
      var ng = document.createElement('button');
      ng.className = 'gnew'; ng.type = 'button'; ng.textContent = '＋ Group';
      ng.title = 'Add a question group (letter is picked automatically)';
      ng.onclick = function () {
        miniForm(idxBox, ['new group title', 'one-line intro (optional)'], function (v) {
          structPost('add_group', { title: v[0], hook: v[1] || '' },
            function (j) { return 'Added group ' + j.group; });
        });
      };
      idxBox.appendChild(ng);
    }
  }
  wireStruct();

  /* 右下角悬浮的「🤖 Chat」—— 聚焦某一题时开这一题的抽屉；
     在目录页（QD5，JL 260725「chatbot in the index page」）开整板会话。 */
  /* Which page is this document ABOUT? (JL 260731, after the QC9 split.)
     In the one-file board every page is a section and the hash names the one
     you are looking at. In the split site each page is its OWN file with no
     hash at all, so hash-only logic fell through to the board session and the
     drawer stayed on board.md no matter which page you opened. A file holding
     exactly one `section.q` IS that page; the index and the group files hold
     none and correctly mean the board. */
  function docPage() {
    var qs = document.querySelectorAll('section.q');
    return qs.length === 1 ? qs[0] : null;
  }
  /* A GROUP file (board/QA.html) holds no page section and its own h1 IS the
     group title, in board.md's `### QA · Design` grammar. That title is exactly
     what a group session is keyed by, so no new registry is needed. The index's
     h1 is the board title and does not match, which keeps the three levels
     apart: page → group → board (JL 260731). */
  function docGroup() {
    if (docPage()) return null;
    var h = document.querySelector('.h1');
    var txt = h ? h.textContent.trim() : '';
    return /^[QS][A-Za-z]*\d*\s*[·:]/.test(txt) ? txt : null;
  }
  function chatTarget() {
    var id = (location.hash || '').slice(1);
    var sec = id && document.getElementById(id);
    if (sec && sec.classList.contains('q')) return sec;
    var only = docPage();
    if (only) return only;
    var g = docGroup();
    return g ? { group: g } : null;   // null only on the index → board session
  }
  var fab = document.createElement('button');
  fab.id = 'chatfab';
  fab.onclick = function () {
    var sec = chatTarget();
    if (sec) chatOpen(sec); else chatOpen('board');
  };
  function fabLbl() {
    var tgt = chatTarget();
    fab.innerHTML = !tgt ? '\u{1F916} Board chat'
                  : (tgt.group ? '\u{1F916} Group chat' : '\u{1F916} Chat');
  }
  window.addEventListener('hashchange', fabLbl);
  window.addEventListener('board:updated', fabLbl);   // router swap (QC9 split site)
  fabLbl();
  /* the reload-restore block at the end of this file needs to read and rebuild
     the drawer, and it lives outside this closure */
  window.__boardDrawerOpen = function () { return chat.classList.contains('on'); };
  window.__boardDrawerReopen = function () {
    if (chat.classList.contains('on')) return;
    var t = chatTarget();
    return chatOpen(t || 'board');
  };
  document.body.appendChild(fab);

  /* Sentence chat reuses this question's existing session. The click establishes
     a visible focus card but does not spend a model turn. The next user message
     is augmented with the address, sentence, and direct apparatus at send time. */
  window.__boardSentenceChat = async function (sec, ref, sentence, attached, contentPath) {
    if (!sec || !sec.classList.contains('q')) return;
    await chatOpen(sec);
    if (location.hash !== '#' + sec.id) location.hash = sec.id;
    setSentenceFocus(ref, sentence, attached, contentPath);
    chat.querySelector('textarea').focus();
  };

  /* The same door for a heading (QB5d): a `##` section or `###` subsection
     focuses THIS page's existing session, never a session of its own. The hash
     is left alone because a tree page has none, and the reader is already on
     the heading they clicked. */
  window.__boardHeadingChat = async function (sec, path, block, file) {
    if (!sec || !sec.classList.contains('q')) return;
    await chatOpen(sec);
    setSentenceFocus(path, block, '', file, 'heading');
    chat.querySelector('textarea').focus();
  };

  // Each step guarded on its own: one wire function throwing (old JS meeting
  // newer markup, a bad page, anything) must not kill the buttons after it —
  // that failure mode is exactly a page full of dead ➕ buttons (JL 260731).
  function safewire(fns) {
    fns.forEach(function (f) {
      try { f(); } catch (e) { console.warn('board wire failed:', e); }
    });
  }
  function rewire() {
    safewire([marks, paint, wireDadd, wireQBtns, wireStruct, wireXcal]);
    try {
      if (window.__boardWireSentenceChats) window.__boardWireSentenceChats();
    } catch (e) { console.warn('board wire failed:', e); }
  }
  window.__boardRewire = rewire;
  safewire([marks, paint, wireDadd, wireXcal]);
})();