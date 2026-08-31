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
  // The sidebar needs the same answer and must not compute it a second way.
  window.__boardDocPage = docPage;
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

  /* ── THE CHAT PICKER (JL 260802: "could we make it a list that I can choose
     GUI-Chat or TUI-Chat") ────────────────────────────────────────────────
     This board has TWO chats and one button, so which one you got was decided
     by a stored preference you could not see, and the only way to switch was a
     `>_` in the drawer header that is hard to find on a phone ("我咋按这个键啊",
     260801). The list makes the pair visible at the moment you are choosing.

     It also carries the thing no surface reported until now: whether something
     is ALREADY running. The ring answers that for a turn and `term-probe` for
     a parked PTY, so the extra tap buys a fact rather than costing one.

     Deliberately the FAB only. A per-card `🤖 Chat` means "talk about THIS
     card" and its reader has already decided; giving twelve buttons a chooser
     would be noise. Those keep going straight to the last-used view. */
  var TUIKEY = 'board-tui-default';
  function tuiDefault() {
    /* GUI unless the reader chose TUI (JL 260831); the shell's radio writes this key. */
    try { return localStorage.getItem(TUIKEY) === '1'; } catch (e) { return false; }
  }
  var pick = document.createElement('div');
  pick.id = 'chatpick';
  pick.hidden = true;
  pick.setAttribute('role', 'menu');
  document.body.appendChild(pick);

  function pickClose() {
    pick.hidden = true;
    document.removeEventListener('pointerdown', pickAway, true);
    document.removeEventListener('keydown', pickKey, true);
  }
  function pickAway(e) {
    if (!pick.contains(e.target) && e.target !== fab) pickClose();
  }
  function pickKey(e) { if (e.key === 'Escape') { e.preventDefault(); pickClose(); } }

  function pickTarget(tgt) {
    if (!tgt) return { file: 'board.md' };
    if (tgt.group) return { file: 'board.md', group: tgt.group };
    return { file: tgt.getAttribute && tgt.getAttribute('data-file') || 'board.md' };
  }

  /* Both questions at once, and neither is allowed to hold the menu up: a
     picker that waits on the network is a picker that feels broken, so the
     rows paint immediately and the state lines fill in when they arrive. */
  function pickState(body, paint) {
    fetch('/_board/attach', { method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(Object.assign({ path: boardPath(), probe: 1 }, body)) })
      .then(function (r) { return r.json(); })
      .then(function (j) { paint('gui', j && j.live ? '⚡ a turn is still running' : ''); })
      .catch(function () {});
    fetch('/_board/term-probe', { method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(Object.assign({ path: boardPath() }, body)) })
      .then(function (r) { return r.json(); })
      .then(function (j) {
        var n = (j && j.terminals || []).length;
        paint('tui', n ? '🟢 a session is parked here' : '');
      })
      .catch(function () {});
  }

  function pickOpen() {
    var tgt = chatTarget();
    var tui = tuiDefault();
    // 🔌 The menu is a REGISTRY now (JL 260807): the board contributes the two chats,
    // a plugin contributes its own surface, and an entry that cannot act on the open
    // page is never drawn. `data-v` stays the id so the existing handler still reads it.
    var page = window.boardPlugins ? window.boardPlugins.livePage() : null;
    // TWO GROUPS, ONE LIST (JL 260808). The shell splits these into two buttons because
    // it has a bar to put them in; the in-page picker is one popup, so the split shows
    // as two titled groups. Same registry, same ids, so `data-v` still resolves.
    // A group with nothing applicable prints no heading: an empty heading claims the
    // page has a workflow and then shows none, which is worse than saying nothing.
    function group(title, menu) {
      var rows = window.boardPlugins
        ? window.boardPlugins.applicable(page, menu) : [];
      if (!rows.length) return '';
      return '<div class="pkh">' + title + '</div>' + rows.map(function (e) {
        var dot = e.id === 'gui' ? (tui ? '' : '●')
                : e.id === 'tui' ? (tui ? '●' : '') : '';
        return '<button class="pk" data-v="' + e.id + '" role="menuitem">'
          + '<b>' + e.label + '</b><i>' + (e.hint || '') + '</i>'
          + '<u></u><s>' + dot + '</s></button>';
      }).join('');
    }
    pick.innerHTML = group('\u{1F50C} Plugin', 'plugin')
                   + group('\u{1FA9C} Workflow', 'workflow');
    pick.hidden = false;
    document.addEventListener('pointerdown', pickAway, true);
    document.addEventListener('keydown', pickKey, true);
    pickState(pickTarget(tgt), function (which, text) {
      var row = pick.querySelector('.pk[data-v="' + which + '"] u');
      if (row) row.textContent = text;
    });
    pick.querySelectorAll('.pk').forEach(function (b) {
      b.onclick = function () {
        var id = b.dataset.v;
        var hit = (window.boardPlugins ? window.boardPlugins.all() : [])
                    .filter(function (e) { return e.id === id; })[0];
        pickClose();
        if (hit) hit.open(window.boardPlugins.livePage());
      };
    });
    var first = pick.querySelector('.pk');
    if (first) first.focus();
  }

  // The board owns exactly two surfaces and registers them like anybody else, so the
  // engine has no privileged path a plugin cannot take. Both are PLUGINS: they open a
  // surface to the right and neither knows or cares where you are on the page, which
  // is exactly the line the Workflow menu is on the other side of.
  if (window.boardPlugins) {
    /* ONE CHAT (JL 260815: "just have one Chat in the plugin, not more ChatGUI
       or Chat TUI"). The registry stops selling the form: one entry, opening in
       the last-used form, and the choice lives INSIDE the surface — the shell's
       mode segment, or the drawer's own `>_` / back pair on a bare page. */
    window.boardPlugins.register({
      id: 'chat', label: '\u{1F4AC} Chat',
      hint: 'this page’s conversation · pick GUI or TUI inside',
      open: function () {
        chatOpen(chatTarget() || 'board');
      } });
  }

  /* JL 260818: "how to make the outline be the default plugin when we open
     it" — a plain FAB click now opens the registry's default (outline) on
     the page in view, same as clicking its row in the picker would; the
     picker itself moved to #chatfabmore, right beside it. On a board/group
     session (no live page) outline never `applies`, so getDefault() returns
     null and the FAB falls back to its old job, opening chat. */
  var fabMore = document.createElement('button');
  fabMore.id = 'chatfabmore';
  fabMore.type = 'button';
  fabMore.setAttribute('aria-label', 'Open the plugin and chat picker');
  fabMore.title = 'Other plugins, GUI/TUI chat, workflow';
  fabMore.textContent = '⋯';
  fabMore.onclick = function () {
    if (!pick.hidden) return pickClose();
    pickOpen();
  };
  document.body.appendChild(fabMore);

  fab.onclick = function () {
    if (!pick.hidden) pickClose();
    var page = window.boardPlugins ? window.boardPlugins.livePage() : null;
    var def = window.boardPlugins ? window.boardPlugins.getDefault(page) : null;
    if (def) { def.open(page); return; }
    pickOpen();
  };
  function fabLbl() {
    var tgt = chatTarget();
    var page = window.boardPlugins ? window.boardPlugins.livePage() : null;
    var def = window.boardPlugins ? window.boardPlugins.getDefault(page) : null;
    fab.innerHTML = def ? def.label
                  : !tgt ? '\u{1F916} Board chat'
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
  /* "Add to chat" in the TUI (JL 260801). The SDK half shows the quote in a
     focus card and augments the next message; a real CLI has no such card, so
     the address and the sentence are typed into the prompt instead, unsubmitted,
     for the reader to finish. Same gesture, whichever half is open. */
  function sentenceToTerm(ref, sentence, contentPath) {
    if (!(window.__boardTermOn && window.__boardTermOn())) return false;
    var where = (contentPath ? contentPath + ' · ' : '') + (ref || '');
    var q = 'About ' + where + ':\n> ' + String(sentence || '').trim() + '\n';
    return !!window.__boardTermType(q);
  }

  window.__boardSentenceChat = async function (sec, ref, sentence, attached, contentPath) {
    if (!sec || !sec.classList.contains('q')) return;
    await chatOpen(sec);
    if (sentenceToTerm(ref, sentence, contentPath)) return;
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
    if (sentenceToTerm(path, block, file)) return;
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
    safewire([marks, paint, wireDadd, wireQBtns, wireStruct]);
    try {
      if (window.__boardWireSentenceChats) window.__boardWireSentenceChats();
    } catch (e) { console.warn('board wire failed:', e); }
  }
  window.__boardRewire = rewire;
  safewire([marks, paint, wireDadd]);
})();