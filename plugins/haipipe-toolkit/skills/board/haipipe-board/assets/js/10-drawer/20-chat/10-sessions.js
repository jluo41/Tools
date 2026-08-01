  /* ── session 拣选器（QD1 Law 修正 260731：一题多 session，一个 current）──
     打开抽屉先亮清单：current 在头一行，历史按最后动笔新→旧，还有「＋新开一段」。
     选中的那段随下一条消息（或 ⌨ 终端）被 resume，同时成为 current，头部跟着换。 */
  var chatSid = '';        // '' = 跟着头部的 current · 'new' = 新开 · uuid = 点名的历史
  function sessAge(t) {
    if (!t) return '';
    var s = Math.max(0, Date.now() / 1000 - t);
    return s < 90 ? 'now' : s < 5400 ? Math.round(s / 60) + 'm'
         : s < 129600 ? Math.round(s / 3600) + 'h' : Math.round(s / 86400) + 'd';
  }
  function paintSessSummary(rows) {
    var n = rows.filter(function (r) { return r.landed; }).length;
    var named = function (r) { return r && (r.name || (r.id ? r.id.slice(0, 8) + '…' : '')); };
    var pickedRow = null;
    for (var pi = 0; pi < rows.length; pi++) if (rows[pi].id === chatSid) pickedRow = rows[pi];
    var cur = chatSid === 'new' ? ('new session next' + (sessName ? ': ' + sessName : ''))
            : chatSid ? named(pickedRow) + ' picked'
            : (rows[0] && rows[0].current ? named(rows[0]) : 'none yet');
    chat.querySelector('.spick summary').textContent =
      '🗂 Session: ' + cur + (n > 1 ? ' · ' + n + ' on record' : '') + ' ▾';
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
  async function syncFromServer(logKey) {
    if (!cq || !cq.file) return;
    try {
      var r = await fetch('/_board/sessions', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: boardPath(), file: cq.file,
                               group: (cq && cq.group) || undefined }) });
      var j = await r.json();
      if (!j || j.ok === false) return;
      var cur = ((j.sessions) || []).filter(function (s) { return s.current && s.landed; })[0];
      if (!cur) return;
      var r2 = await fetch('/_board/session-log', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: boardPath(), file: cq.file,
                               group: (cq && cq.group) || undefined, id: cur.id }) });
      var j2 = await r2.json();
      if (!j2 || j2.ok === false) return;
      var srv = j2.log || [];
      var local = chatLoad(logKey);
      /* only adopt when the server genuinely knows more, so a page whose local
         log is ahead (a turn this tab just rendered) is never rolled back */
      if (srv.length <= local.length) return;
      var bd = chat.querySelector('.bd');
      if (bd.querySelector('.trace') || document.body.classList.contains('chatbusy')) return;
      bd.innerHTML = '';
      if (j2.clipped) bubble('sys', 'Showing the last ' + srv.length + ' of ' + j2.total + ' messages.');
      srv.forEach(function (m) { bubble(m.k, m.t); });
      chatSave(logKey, srv);
      bd.scrollTop = 1e9;
    } catch (e) { /* offline or an old server: the local paint still stands */ }
  }

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
      log.forEach(function (m) { bubble(m.k, m.t); });
      bubble('sys', '\u2191 history of the picked session \u00b7 your next message resumes it');
      bd.scrollTop = 1e9;
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
      var picked = chatSid ? chatSid === r.id : r.current;
      // 有名字显名字（QD3m-fix-black-screen），没名字退回第一句话
      var d = mk(r.name || r.title || (r.landed ? '(untitled)' : '(recorded, never talked)'),
         (r.current ? 'current · ' : '')
           + (r.landed ? sessAge(r.mtime) + ' · ' + Math.round((r.size || 0) / 1024) + 'k'
                       : 'hollow'),
         (picked ? 'cur' : '') + (r.name ? ' named' : '') + (r.landed || r.current ? '' : ' dim'),
         function () {
           chatSid = r.current ? '' : r.id;
           sp.open = false;
           paintSessSummary(rows);
           bubble('sys', r.current ? 'Back on the current session.'
             : 'Picked ' + (r.name || r.id.slice(0, 8) + '…') + ' — the next message (or ⌨) resumes it and makes it current.');
           /* Show what you are resuming (JL 260801: "I cannot see previous chat
              history"). The drawer's own log is per PAGE and kept in this
              browser, so it is the wrong transcript for a session picked here
              and empty for one started in a terminal or on another machine.
              The session's .jsonl on disk is the only honest source. */
           replaySession(r.id, r.landed);
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
    var nu = mk('＋ New session', 'starts fresh, primed with this question', 'new', function () {
      // 先问一句这段是干嘛的（可留空）：名字跟着第一条消息/⌨ 一起落进登记表
      var inp = document.createElement('input');
      inp.type = 'text'; inp.className = 'spin';
      inp.placeholder = 'name it: what is this session for? (Enter · empty = unnamed)';
      nu.querySelector('.t').replaceChildren(inp); inp.focus();
      inp.onclick = function (ev) { ev.stopPropagation(); };
      inp.onkeydown = function (k) {
        if (k.key === 'Enter') {
          sessName = inp.value.trim();
          chatSid = 'new'; sp.open = false; paintSessSummary(rows);
          bubble('sys', 'The next message (or ⌨) starts a NEW session'
            + (sessName ? ' named "' + sessName + '"' : '') + ' for this question.');
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
      if (j.ok) renderSessions(j);
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
