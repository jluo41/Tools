  var inflight = null;                    // 正在跑的那一轮：{ctrl, file}
  var followPending = false;              // navigated mid-turn; switch when it ends
  async function chatStop() {
    if (!inflight) return;
    if (chatQueue.length) {             // stopping means stop, including what is queued
      chatQueue.length = 0;
      chat.querySelectorAll('.bd .m.you.queued').forEach(function (d) { d.remove(); });
      bubble('sys', 'Stopped — queued messages were dropped.');
    }
    try {
      await fetch('/_board/stop', { method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: boardPath(), file: inflight.file }) });
      bubble('sys', 'Stop signal sent — it will wrap up at the next message…');
    } catch (e) { /* 服务器都不通了，直接放弃等待 */ }
    /* ONE ACTION, ONE MESSAGE. The abort below lands in the catch, which says
       "Stopped waiting. The server got the stop signal too." — so pressing ⏹
       printed two lines that half contradict each other, the first saying it
       will wrap up and the second that we stopped waiting (found 260802 by
       asserting the drawer says exactly one thing about stopping). The line
       above is the honest one and it is already on screen. */
    if (inflight.mark) inflight.mark();
    inflight.ctrl.abort();                // 浏览器这边立刻不等了
  }
  function chatBusy(on) {
    /* A turn in flight is exactly as interruptible as an open terminal: the
       asset-stamp guard already defers a full reload for `termon`, and without
       the same flag here a rebuild mid-turn wipes the trace and aborts the
       stream. Ships happen often (three sessions shipped JS in one day). */
    document.body.classList.toggle('chatbusy', on);
    if (!on && window.__pendingReload) { location.reload(); return; }
    var btn = chat.querySelector('.send');
    btn.textContent = on ? '⏹' : '➤';
    btn.title = on ? 'Stop this turn' : 'Send';
    btn.classList.toggle('stop', on);
    btn.disabled = false;                 // 忙的时候也能点 —— 那是停止键
    /* Type-ahead (JL 260731: "when the SDK chat draw is running, I cannot enter
       the new messages, why?"). Disabling the box was the easy way to enforce
       one turn at a time, but it also stops you composing the next thought while
       you wait, which the CLI has always allowed. The box stays live; Enter
       QUEUES instead of racing the server, which still refuses two turns. */
    var ta = chat.querySelector('textarea');
    ta.disabled = false;
    ta.placeholder = on ? 'Type the next message — it sends when this turn finishes…'
                        : (cq && cq.board ? 'Ask about this board…' : 'Ask about this question…');
  }

  /* Messages typed while a turn is running, sent in order once it ends. */
  /* Flight recorder (JL 260731, after the same wedge recurred and every
     synthetic test passed). Keeps the last 200 things the drawer did, so a
     stuck turn can be described instead of guessed at. Cheap, no I/O. */
  var chatDiag = [];
  function diag(kind, detail) {
    chatDiag.push(new Date().toISOString().slice(11, 19) + ' ' + kind
                  + (detail ? ' ' + String(detail).slice(0, 120) : ''));
    if (chatDiag.length > 200) chatDiag.shift();
  }
  /* THE TEST BRIDGE. The drawer is one closure, so nothing inside it is
     reachable from Runtime.evaluate, and `checks/chatui.mjs` T8 and T10 were
     therefore reporting "not reachable" and had NEVER ONCE RUN — two checks
     that looked like coverage and were not. Anything the suite must reach goes
     here, deliberately and by name, rather than by leaking the whole scope. */
  window.__chatProbe = {
    bubble: function (k, t) { return bubble(k, t); },
    inflight: function () { return !!inflight; },
    activeSid: function () { return activeSid; },
    logKey: function () { return logKey(); },
    switchTo: function (sid, name, landed) { return switchTo(sid, name, landed); },
    sidText: function () { return (chat.querySelector('.sid') || {}).textContent || ''; },
    switchMarks: function () {
      return [].map.call(chat.querySelectorAll('.bd .switchsep'),
                         function (e) { return e.textContent; });
    }
  };
  window.__chatDiag = function () {
    var d = {
      when: new Date().toISOString(),
      page: cq && (cq.id + ' · ' + cq.file),
      settings: [(chat.querySelector('.mdl') || {}).value,
                 (chat.querySelector('.eff') || {}).value,
                 (chat.querySelector('.scope') || {}).value].join(' / '),
      session: chatSid || '(current)',
      inflight: !!inflight,
      queued: chatQueue.length,
      dom: {
        busy: !!chat.querySelector('.busy'),
        trace: !!chat.querySelector('.trace'),
        traced: chat.querySelectorAll('.traced').length,
        answers: chat.querySelectorAll('.bd > .m.cc').length,
        stopBtn: chat.querySelector('.send').classList.contains('stop')
      },
      log: chatDiag.slice(-80)
    };
    return JSON.stringify(d, null, 1);
  };

  var chatQueue = [];
  function queueMsg(text) {
    chatQueue.push(text);
    var d = bubble('you', text); bdJump();
    d.classList.add('queued');
    d.title = 'queued — sends when the current turn finishes';
    busyBump();
    return d;
  }
  function drainQueue() {
    if (!chatQueue.length || inflight) return;
    var next = chatQueue.shift();
    /* the queued bubble was already drawn; chatSend draws its own, so drop the
       placeholder first and let the real one take its place */
    var ph = chat.querySelector('.bd .m.you.queued');
    if (ph && ph.parentNode) ph.parentNode.removeChild(ph);
    chatSend(next);
  }

  /* R1 · HOW FAR THIS READER GOT IN THE TURN'S RING.
     The server now keeps every turn's events in a ring with a monotonic cursor
     (`servers/workbench/chat_drawer/turnring.py`), so the only thing a returning drawer needs in order to
     rejoin is the number of the last event it saw. It lives in storage rather
     than in a variable precisely because the thing it has to survive is the
     page that was reading — a reload, a navigation, a phone locking. */
  /* Keyed on the SCOPE, never on the session. The ring is per question path on
     the server, and `logKey()` folds in the session id — which CHANGES mid-turn
     the first time a new session is created, so a cursor written before that
     point was looked for under a key that no longer existed and the rejoin
     started from near zero. Caught by reloading a real page, not by reading. */
  var CURK = function () {
    return 'board-chat-cur:' + location.pathname + ':'
         + ((cq && (cq.group ? 'G:' + cq.group : cq.file)) || '');
  };
  function curGet() {
    try { return parseInt(localStorage.getItem(CURK()) || '0', 10) || 0; }
    catch (e) { return 0; }
  }
  function curSet(n) { try { localStorage.setItem(CURK(), String(n)); } catch (e) {} }

  /* ── THE REJOIN IS NOT A TURN ────────────────────────────────────────────
     It used to be: `chatRejoin` called `chatSend({attach:true})` and every
     failure branch of a 250-line turn function became something the reader
     saw. That cost two separate fixes in one day — the 404 branch, then the
     abort branch — and JL still ended up with ~120 copies of "Stopped waiting.
     The server got the stop signal too." on one page (260802), a sentence that
     was false twice over. A third branch would have been missed the same way.

     So the two are separated the way the VS Code extension separates them. Its
     webview never owns a turn: the extension host owns the session and the
     webview only RENDERS events, which is why it can be thrown away and
     rebuilt at any moment without anything being lost or anything being said
     about it. `chatSend` owns a turn: the composer, the log, the cost line,
     the failure report. `chatAttach` owns nothing at all. It paints events
     into the transcript and, on any failure whatsoever, returns false without
     a word. There is no branch left in it that can address the reader. */
  var reattaching = false;

  async function chatAttach() {
    if (inflight || reattaching || !cq) return false;
    reattaching = true;
    var painted = false, cur = null, acc = '', seg = '';
    var thinkEl = null, thinkAcc = '', lastRow = null, lastSeg = '';
    var t0 = Date.now();
    try {
      var r = await fetch('/_board/attach', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: boardPath(), file: cq.file,
          group: (cq && cq.group) || undefined, cursor: curGet() })
      });
      /* Nothing running is the ORDINARY answer, and an older server with no
         ring is an ordinary answer too. Both are "false", both are silent. */
      if (!r.ok || (r.headers.get('Content-Type') || '').indexOf('ndjson') < 0) {
        diag('REJOIN', 'nothing live');
        return false;
      }
      diag('REJOIN', 'attached at cursor ' + curGet());
      var log = chatLoad(logKey());
      traceStart(); busyStart('Rejoining'); chatBusy(true); painted = true;
      var rd = r.body.getReader(), dec = new TextDecoder(), buf = '', j = null;
      while (true) {
        var ch = await rd.read();
        if (ch.done) break;
        buf += dec.decode(ch.value, { stream: true });
        var lines = buf.split('\n'); buf = lines.pop();
        for (var i = 0; i < lines.length; i++) {
          if (!lines[i].trim()) continue;
          var ev; try { ev = JSON.parse(lines[i]); } catch (e) { continue; }
          if (typeof ev.n === 'number') curSet(ev.n + 1);
          if (ev.t === 'ping') continue;
          if (ev.t === 'gap') {
            bubble('sys', '⚠ ' + (ev.text || 'reconnected mid-turn'));
          } else if (ev.t === 'stage') {
            busySay(ev.text.length > 46 ? ev.text.slice(0, 46) + '…' : ev.text);
          } else if (ev.t === 'think') {
            busySay('Thinking');
            if (!thinkEl) thinkEl = thinkBubble();
            thinkAcc += ev.text;
            thinkEl.querySelector('.tk-body').textContent = thinkAcc;
            bdAuto();
          } else if (ev.t === 'delta') {
            if (busyWhat !== 'Responding') busySay('Responding');
            if (thinkEl && thinkEl.open) {
              thinkEl.open = false;
              thinkEl.querySelector('summary').textContent =
                '💭 Thinking (' + thinkAcc.length + ' chars — click to reopen)';
            }
            if (!cur) { cur = traceRow('say', '✍️', ''); seg = ''; }
            seg += ev.text; acc += ev.text;
            cur.querySelector('.x').textContent = seg;
            lastRow = cur; lastSeg = seg;
            traceScroll();
          } else if (ev.t === 'tool') {
            cur = null; seg = ''; toolCard(ev); busySay(ev.name || 'tool');
          } else if (ev.t === 'tool_result') {
            toolResult(ev); busySay('Thinking');
          } else if (ev.t === 'ask') {
            cur = null; askUI(ev);
          } else if (ev.t === 'done') {
            j = ev;
          }
        }
      }
      if (!j) return false;             /* the stream ended without an answer */
      busyEnd();
      if (lastRow && lastRow.parentNode) lastRow.parentNode.removeChild(lastRow);
      var took = (Date.now() - t0) / 1000;
      traceEnd('rejoined · ' + (took < 60 ? took.toFixed(1) + 's'
        : Math.floor(took / 60) + 'm' + String(Math.round(took % 60)).padStart(2, '0') + 's'));
      var txt = lastSeg || j.text || acc;
      if (!txt) return false;
      bubble('cc', txt);
      log.push({ k: 'cc', t: j.text || acc || txt });
      chatSave(logKey(), log);
      if (j.session) loadSessions();
      return true;
    } catch (e) {
      /* EVERY failure lands here and NONE of it is the reader's business:
         an abort, a dropped socket, a restarted server, a parse error. It goes
         to the drawer's own diagnostics and nowhere else. */
      diag('REJOIN', 'gave up quietly: ' + (e.name || e.message || 'error'));
      return false;
    } finally {
      reattaching = false;
      if (painted) { busyEnd(); traceEnd(); chatBusy(false); }
    }
  }

  /* Rejoin a turn that is still running with nobody watching it.
     Returns true when it actually attached, so the caller can fall back to
     reading the transcript when nothing is live. */
  function chatRejoin() { return chatAttach(); }
