  /* ── session 拣选器（QD1 Law 修正 260731：一题多 session，一个 current）──
     打开抽屉先亮清单：current 在头一行，历史按最后动笔新→旧，还有「＋新开一段」。
     选中的那段随下一条消息（或 ⌨ 终端）被 resume，同时成为 current，头部跟着换。 */
  var chatSid = '';        // '' = 跟着头部的 current · 'new' = 新开 · uuid = 点名的历史
  /* THE SESSION THE DRAWER IS SHOWING (JL 260801: "我们打开了一个新的 session
     webpage，为什么整个页面没有跟着更新呢?").

     `chatSid` was only ever a PENDING INTENT: what the NEXT message should ask
     the server for. Nothing on screen was bound to it, so picking a session
     printed a sentence and left the header, the transcript, the local log key
     and the row highlight all describing the session you had just left. That is
     the whole difference from the VS Code plugin, which keeps ONE active
     conversation id and renders every part of the panel from it.

     `activeSid` is that id. It is the session the body, the `.sid` box, the
     picker highlight and `logKey()` all agree they are showing, and `switchTo`
     is the ONLY thing allowed to change it. '' means "a new session, not started
     yet". */
  var activeSid = '';
  var lastSessJson = null;             // what the picker last drew, for repaint
  function sessAge(t) {
    if (!t) return '';
    var s = Math.max(0, Date.now() / 1000 - t);
    return s < 90 ? 'now' : s < 5400 ? Math.round(s / 60) + 'm'
         : s < 129600 ? Math.round(s / 3600) + 'h' : Math.round(s / 86400) + 'd';
  }
  function paintSessSummary(rows) {
    var n = rows.filter(function (r) { return r.landed; }).length;
    var named = function (r) { return r && (r.name || (r.id ? r.id.slice(0, 8) + '…' : '')); };
    var row = null;
    for (var pi = 0; pi < rows.length; pi++) if (rows[pi].id === activeSid) row = rows[pi];
    /* the summary says what you ARE ON, not what you have queued up: "picked"
       and "next" were the old model's words for an intent nothing obeyed */
    var cur = !activeSid ? ('new session' + (sessName ? ': ' + sessName : ''))
            : row ? named(row) : activeSid.slice(0, 8) + '…';
    chat.querySelector('.spick summary').textContent =
      '🗂 Session: ' + cur + (n > 1 ? ' · ' + n + ' on record' : '') + ' ▾';
  }

  /* THE HEADER FOLLOWS THE SWITCH. The `.sid` box used to be written in exactly
     one place, inside chatOpen, so it could only ever show the session the PAGE
     was opened on; switching sessions left it naming the old one, with a
     `claude --resume` command that resumed the wrong conversation. */
  function paintSid(sid) {
    var sidbox = chat.querySelector('.sid');
    if (!sidbox || !cq) return;
    if (!sid) {
      sidbox.innerHTML = '<span class="mut">' + (cq.group
        ? 'Group sessions live in the 🗂 tab — pick one, or start a new one here.'
        : 'No session yet — it appears after your first message and is written into the header of '
          + cq.file) + '</span>';
      return;
    }
    /* session 归档在 cwd（= serve.py 的 --root）下的 project 目录，所以要 cd 到
       root，不是板文件夹 —— cd 错了 --resume 就找不到这个 session。 */
    var board = document.body.getAttribute('data-board') || '.';
    var urlDir = boardDirPath();
    var root = board;
    if (urlDir && board.slice(-urlDir.length) === urlDir) {
      root = board.slice(0, board.length - urlDir.length) || '/';
    }
    sidbox.innerHTML = '<code>' + sid + '</code>';
    var full = '# ' + cq.id + ' · ' + cq.title + '\n'
             + 'cd "' + root + '" && claude --resume ' + sid;
    var cb = document.createElement('button');
    cb.className = 'act'; cb.textContent = '⌨ Copy: claude --resume';
    cb.title = full;
    cb.onclick = function () {
      navigator.clipboard.writeText(full)
        .then(function () { cb.textContent = 'Copied full command'; });
    };
    sidbox.appendChild(cb);

    /* A THIRD way into the same session: a terminal on the machine YOU are
       sitting at (JL 260801: "在这个 App 上打开 Terminal，然后在 Terminal 里面
       进入这个 Chat").

       The board cannot open it for you, and the reason is worth stating once so
       nobody tries again: a page cannot start a program on the machine viewing
       it, and having the SERVER open a window is not a workaround, because the
       server is on the Mac while the reader is usually somewhere else over ssh.
       Tried on 260801, it opened nothing and blocked the call.

       What the server DOES know is the exact command, including the ssh hop
       back to itself. One paste in any terminal, on any machine, lands in this
       same conversation. */
    var lb = document.createElement('button');
    lb.className = 'act'; lb.textContent = '🖥 Copy: open on my machine';
    lb.title = 'An ssh command that drops any terminal, anywhere, into this session';
    lb.onclick = async function () {
      try {
        var r = await fetch('/_board/local-cmd', { method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ path: boardPath(), file: cq.file,
                                 group: (cq && cq.group) || undefined, session: sid }) });
        var j = await r.json();
        if (!j || j.ok === false) { say('⚠ ' + ((j && j.err) || 'could not build the command')); return; }
        await navigator.clipboard.writeText(j.remote);
        lb.textContent = 'Copied — paste in any terminal';
        say('Paste this in a terminal on your own machine:\n' + j.remote
            + '\nAlready on ' + j.host + '? Then: ' + j.here);
      } catch (e) { say('⚠ ' + e.message); }
    };
    sidbox.appendChild(lb);
  }

  /* A SWITCH LEAVES A MARK IN THE TRANSCRIPT (JL 260801: "为什么 history 没有
     对应的，比如说 switch 呢?"). Without it the pane silently becomes a
     different conversation and a reader cannot tell where one ended and the
     next began. Same shape as the turn separator, one class louder. */
  function switchMark(label) {
    var el = document.createElement('div');
    el.className = 'turnsep switchsep';
    el.textContent = label;
    return el;
  }

  /* THE ONE PLACE A SESSION CHANGES. Everything the reader can see is repainted
     here, in one go: the transcript body, the switch banner, the `.sid` box,
     the picker highlight and the summary line. Nothing else may assign
     activeSid. */
  async function switchTo(sid, name, landed) {
    /* NEVER SWITCH OUT FROM UNDER A LIVE TURN. This clears .bd, calls busyEnd()
       and drops traceEl, so running it mid-stream orphans the trace and leaves
       the ⏹ button stuck — the same defect chatOpen was fixed for on 260731,
       and the tool cards and 💭 thinking block are exactly what disappears. */
    if (typeof inflight !== 'undefined' && inflight) {
      bubble('sys', 'A turn is still running — stop it with ⏹ first, then switch.');
      return;
    }
    var from = activeSid;
    activeSid = sid || '';
    chatSid = sid || 'new';            // what the NEXT message asks the server for
    if (name != null) sessName = sid ? '' : name;
    var bd = chat.querySelector('.bd');
    busyEnd(); traceEl = null; toolCards = {};
    if (activeSid && landed) {
      await replaySession(activeSid, true);          // clears and refills .bd itself
    } else {
      bd.innerHTML = '';
      chatLoad(logKey()).forEach(replayRow);         // a fresh one may have local text
    }
    paintSid(activeSid);
    var label = activeSid
      ? '🗂 ' + (name || (lookupName(activeSid) || activeSid.slice(0, 8) + '…'))
        + (from && from !== activeSid ? '  ·  switched from ' + from.slice(0, 8) + '…' : '')
      : '🗂 new session' + (sessName ? ' · ' + sessName : '')
        + '  ·  starts with your next message';
    bd.insertBefore(switchMark(label), bd.firstChild);
    if (lastSessJson) renderSessions(lastSessJson);   // repaint the highlight
    bdJump();
    syncSchedule();                                  // re-aim the heartbeat
  }
  function lookupName(sid) {
    var rows = (lastSessJson && lastSessJson.sessions) || [];
    for (var i = 0; i < rows.length; i++) if (rows[i].id === sid) return rows[i].name || rows[i].title;
    return '';
  }

  /* Paint from the browser, then correct from the SERVER (JL 260801: "when it
     is reloaded the chat box UI is just gone... should I make chat detached
     from the page html?").

     The session is ALREADY detached: it lives on the SessionHost and on disk as
     a .jsonl, and a turn started before a reload finishes there whether or not
     a browser is watching (measured 260801: the answer landed while the tab was
     reloading). What was NOT detached is what the drawer RENDERS, because it
     replayed a log kept per page in this browser. So a reload showed a
     transcript that was merely the last thing this tab happened to save.

     Fix the render, not the architecture: keep the instant local paint so the
     drawer never flashes empty, then ask the server for the session's real
     transcript and adopt it when it knows more. A reload now costs the live
     trace of an in-flight turn and nothing else.  */
  async function syncFromServer() {
    if (!cq || !cq.file) return;
    try {
      var r = await fetch('/_board/sessions', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: boardPath(), file: cq.file,
                               group: (cq && cq.group) || undefined }) });
      var j = await r.json();
      if (window.__boardTermLive) { try { await loadTermList(); } catch (e) {} }
      if (!j || j.ok === false) return;
      lastSessJson = j;
      /* SYNC THE SESSION BEING SHOWN, NOT THE ONE THE FILE HEADER CALLS CURRENT.
         This asked for `current` unconditionally and wrote the answer into the
         page's log, so picking any other session was undone by the very next
         heartbeat: the replayed history was painted over, in place, a few
         seconds later. That is the "why doesn't the page follow" seen from the
         other side — it followed, and then the sync dragged it back. */
      var want = activeSid;
      if (!want) {
        if (chatSid === 'new') return;      // deliberately on a fresh one: nothing to adopt
        var cur = ((j.sessions) || []).filter(function (s) { return s.current && s.landed; })[0];
        if (!cur) return;
        want = cur.id;
        activeSid = want;                   // the first turn landed; adopt it
        paintSid(want);
      }
      var r2 = await fetch('/_board/session-log', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: boardPath(), file: cq.file,
                               group: (cq && cq.group) || undefined, id: want }) });
      var j2 = await r2.json();
      if (!j2 || j2.ok === false) return;
      var srv = j2.log || [];
      var local = chatLoad(logKey());
      /* Adopt when the server knows BETTER, which is not the same as knowing
         MORE. A cut-short turn leaves a provisional reply in the local log, so
         the two sides have equal LENGTH while one of them is a fragment; the
         old length test therefore refused to upgrade it, forever. Anything
         marked partial is an open invitation to be replaced. */
      var provisional = local.some(function (m) { return m && m.partial; });
      if (srv.length <= local.length && !provisional) return;
      var bd = chat.querySelector('.bd');
      /* Never clobber a turn that is genuinely running, but do not trust a
         STALE flag either: `chatbusy` is a class that an aborted turn can
         leave behind, and while it sat there this function refused to adopt
         anything, forever. `inflight` is the real signal. */
      if ((typeof inflight !== 'undefined' && inflight) || bd.querySelector('.trace')) return;
      /* keep the switch banner: it says which conversation this pane is, and a
         repaint that removed it would leave the reader in an unlabelled one */
      var mark = bd.querySelector('.switchsep');
      bd.innerHTML = '';
      if (mark) bd.appendChild(mark);
      if (j2.clipped) bubble('sys', 'Showing the last ' + srv.length + ' of ' + j2.total + ' messages.');
      srv.forEach(replayRow);
      chatSave(logKey(), srv);
      bdJump();
    } catch (e) { /* offline or an old server: the local paint still stands */ }
    return true;
  }

  /* THE DRAWER HAS TO KEEP ASKING (JL 260801: "你这个 Chatbot 是不是没有自主地
     去 check session update？我这一回来，然后东西就没有了").
     syncFromServer used to be called from exactly ONE place, chatOpen, so it
     asked the server once at the instant the drawer opened and never again. If
     the turn had not landed in the .jsonl by that instant — and coming back
     mid-turn is exactly when it has not — the reader was left staring at a gap
     that the server could have filled a second later. Nothing was missing; no
     one was asking. So: retry with backoff after opening, ask again whenever
     the tab comes back to the front, and keep a slow idle heartbeat while the
     drawer is open. All of them are cheap reads and all refuse to run while a
     turn is genuinely in flight. */
  var syncTimers = [], syncBeat = null;
  function syncStop() {
    syncTimers.forEach(clearTimeout); syncTimers = [];
    if (syncBeat) { clearInterval(syncBeat); syncBeat = null; }
  }
  function syncNow() {
    if (!cq) return;
    if (typeof inflight !== 'undefined' && inflight) return;   // a live turn owns the view
    /* R1 · REJOIN BEFORE READING. A turn may still be RUNNING on the server
       with nobody watching it, and the transcript cannot help there because it
       is not written until the turn ends — which is exactly the gap JL kept
       hitting ("我这一回来，然后东西就没有了"). Ask the ring first; only when
       nothing is live does the transcript become the right answer. */
    if (typeof chatRejoin === 'function') {
      Promise.resolve(chatRejoin()).then(function (attached) {
        if (!attached) { try { syncFromServer(logKey()); } catch (e) {} }
      }, function () { try { syncFromServer(logKey()); } catch (e) {} });
      return;
    }
    try { syncFromServer(logKey()); } catch (e) {}
  }
  function syncSchedule() {
    syncStop();
    /* the .jsonl is written as the turn ends, so the useful window is the few
       seconds AFTER opening, not the instant of it */
    [1500, 4000, 9000, 20000].forEach(function (ms) {
      syncTimers.push(setTimeout(syncNow, ms));
    });
    syncBeat = setInterval(function () {
      var c = document.getElementById('chat');
      if (!c || !c.classList.contains('on')) return;    // closed: nothing to repaint
      if (document.hidden) return;                      // not being looked at
      syncNow();
    }, 25000);
  }
  document.addEventListener('visibilitychange', function () {
    if (!document.hidden) syncNow();                    // you came back to the tab
  });
  window.addEventListener('focus', syncNow);            // you came back to the window


  /* Replace the drawer's body with a session's REAL transcript, read from its
     .jsonl by the server (POST /_board/session-log). Read-only: this does not
     touch the page's own saved log, so switching back to the current session
     shows that one again, unchanged. */
  async function replaySession(sid, landed) {
    var bd = chat.querySelector('.bd');
    if (!landed) {
      bubble('sys', 'Nothing was ever said in that session, so there is no history to show.');
      return;
    }
    var note = bubble('sys', 'Loading that session\u2019s history\u2026');
    try {
      var r = await fetch('/_board/session-log', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        /* `path` is not optional: the server locates the board folder from the
           browser pathname, and without it every call answers "outside --root".
           Leaving it out is why this looked like an empty session. */
        body: JSON.stringify({ path: boardPath(), file: cq && cq.file,
                               group: (cq && cq.group) || undefined, id: sid })
      });
      var j = await r.json();
      if (note && note.parentNode) note.parentNode.removeChild(note);
      if (!j || j.ok === false) {
        bubble('sys', '\u26a0 could not read that session: ' + ((j && j.err) || 'unknown'));
        return;
      }
      var log = j.log || [];
      if (!log.length) {
        bubble('sys', 'That session has no readable messages yet.');
        return;
      }
      bd.innerHTML = '';
      if (j.clipped) {
        bubble('sys', 'Showing the last ' + log.length + ' of ' + j.total
                    + ' messages in this session.');
      }
      log.forEach(replayRow);
      bubble('sys', '\u2191 history of the picked session \u00b7 your next message resumes it');
      bdJump();
    } catch (e) {
      if (note && note.parentNode) note.parentNode.removeChild(note);
      bubble('sys', '\u26a0 could not load that session\u2019s history: ' + e.message);
    }
  }

  var sessName = '';   // 「＋ 新开一段」时给它起的名字（QD1 260731：Qxxx-干嘛用的）
  function renderSessions(j) {
    var sp = chat.querySelector('.spick'), sl = chat.querySelector('.spl');
    sl.innerHTML = '';
    var rows = (j && j.sessions) || [];
    var mk = function (label, meta, cls, onpick) {
      var d = document.createElement('div');
      d.className = 'sprow' + (cls ? ' ' + cls : '');
      d.innerHTML = '<span class="t"></span><span class="meta"></span>';
      d.querySelector('.t').textContent = label;
      d.querySelector('.meta').textContent = meta || '';
      d.onclick = onpick;
      sl.appendChild(d);
      return d;
    };
    rows.forEach(function (r) {
      /* one authority, so the highlight cannot disagree with the pane */
      var picked = r.id === activeSid;
      // 有名字显名字（QD3m-fix-black-screen），没名字退回第一句话
      /* ⌨ marks a session that already has a terminal running, so the picker
         is the one place that shows what exists (JL 260801). */
      var liveT = (window.__boardTermLive ? window.__boardTermLive() : [])
        .filter(function (x) { return x.session === r.id; })[0];
      var d = mk((liveT ? '⌨ ' : '') + (r.name || r.title || (r.landed ? '(untitled)' : '(recorded, never talked)')),
         (r.current ? 'current · ' : '')
           + (liveT ? (liveT.parked ? 'terminal parked · ' : 'terminal running · ') : '')
           + (r.landed ? sessAge(r.mtime) + ' · ' + Math.round((r.size || 0) / 1024) + 'k'
                       : 'hollow'),
         (picked ? 'cur' : '') + (r.name ? ' named' : '') + (r.landed || r.current ? '' : ' dim'),
         async function () {
           if (r.id === activeSid) { sp.open = false; return; }   // already here
           sp.open = false;
           /* ONE chooser for both halves (JL 260801). In the TUI this is not a
              plan for later: attach that session's terminal now. Terminals are
              keyed per (page, session) since 260801, so the one you are leaving
              keeps running and you can come straight back to it. */
           if (window.__boardTermOn && window.__boardTermOn()) {
             chatSid = r.id;
             say('Attaching the terminal for ' + (r.name || r.id.slice(0, 8) + '…') + '…');
             await window.__boardTermAttach(r.id);
             loadSessions();
             return;
           }
           /* SWITCH, do not merely INTEND to. The old code set chatSid, printed
              a sentence and replayed the body, leaving the header, the log key
              and the row highlight on the session you had just left — and the
              sync then painted that one back over the replay (JL 260801). */
           await switchTo(r.id, r.name || r.title || '', r.landed);
         });
      // ✎ 改名：行内输入，写进登记表，不打断挑选
      var e = document.createElement('button');
      e.className = 'sprn'; e.textContent = '✎'; e.title = 'Name this session';
      e.onclick = function (ev) {
        ev.stopPropagation();
        var inp = document.createElement('input');
        inp.type = 'text'; inp.className = 'spin';
        inp.placeholder = 'what is this session for?';
        inp.value = (r.name || '').replace(/^[^-]*-/, '');
        d.querySelector('.t').replaceChildren(inp); inp.focus();
        var done = function () {
          fetch('/_board/session-name', { method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ path: boardPath(), file: cq.file,
                                   group: (cq && cq.group) || undefined,
                                   id: r.id, name: inp.value.trim() }) })
            .then(function () { loadSessions(); });
        };
        inp.onkeydown = function (k) { if (k.key === 'Enter') done(); if (k.key === 'Escape') loadSessions(); };
        inp.onblur = done;
      };
      d.appendChild(e);
    });
    var nu = mk('＋ New session', 'starts fresh, primed with this question',
                'new' + (activeSid ? '' : ' cur'), function () {
      // 先问一句这段是干嘛的（可留空）：名字跟着第一条消息/⌨ 一起落进登记表
      var inp = document.createElement('input');
      inp.type = 'text'; inp.className = 'spin';
      inp.placeholder = 'name it: what is this session for? (Enter · empty = unnamed)';
      nu.querySelector('.t').replaceChildren(inp); inp.focus();
      inp.onclick = function (ev) { ev.stopPropagation(); };
      inp.onkeydown = function (k) {
        if (k.key === 'Enter') {
          var nm = inp.value.trim();
          sp.open = false;
          if (window.__boardTermOn && window.__boardTermOn()) {
            sessName = nm; chatSid = 'new';
            say('Starting another terminal…');
            window.__boardTermAttach('new').then(function () { loadSessions(); });
            return;
          }
          /* CLEAR THE PANE. This used to print one sentence into the OLD
             session's transcript and change nothing else, so a "new session"
             looked exactly like the one you were already in (JL 260801:
             "为什么整个页面没有跟着更新呢?"). */
          switchTo('', nm, false);
        }
        if (k.key === 'Escape') loadSessions();
      };
    });
    sp.hidden = false;
    sp.open = rows.filter(function (r) { return r.landed; }).length > 1;
    paintSessSummary(rows);
  }
  async function loadSessions() {
    var sp = chat.querySelector('.spick');
    sp.hidden = true;
    if (!cq) return;
    try {
      var r = await fetch('/_board/sessions', { method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: boardPath(), file: cq.file,
                               group: (cq && cq.group) || undefined }) });
      var j = await r.json();
      if (j.ok) { lastSessJson = j; renderSessions(j); }
    } catch (e) { /* serve.py 没跑 → 没有拣选器，其余照旧 */ }
  }

  function clearSentenceFocus() {
    sentenceFocus = null;
    var box = chat.querySelector('.sfocus');
    box.hidden = true;
    box.querySelector('.sfref').textContent = '';
    box.querySelector('.sfpath').textContent = '';
    box.querySelector('.sfquote').textContent = '';
    box.querySelector('.sfattached pre').textContent = '';
    box.querySelector('.sfattached').hidden = true;
    chat.querySelector('textarea').placeholder = cq && cq.board
      ? 'Ask about this board — e.g. what should we act on next?'
      : 'Ask about this question…';
  }
