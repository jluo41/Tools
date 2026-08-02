  /* 模型 / effort / 权限档 记在本机；default Opus 5 · high · full·ask */
  (function () {
    var m = chat.querySelector('.mdl'), e = chat.querySelector('.eff'),
        s = chat.querySelector('.scope');
    m.value = localStorage.getItem(MK) || 'opus';
    e.value = localStorage.getItem(EK) || 'high';
    s.value = localStorage.getItem(SK) || 'full';
    m.onchange = function () { localStorage.setItem(MK, m.value); };
    e.onchange = function () { localStorage.setItem(EK, e.value); };
    s.onchange = function () {
      localStorage.setItem(SK, s.value);
      say(s.value === 'scoped' ? 'Scoped: edits only this question, no skills loaded (cheap)'
        : s.value === 'full' ? 'Full: all tools + skills, asks before touching anything else (like the CLI)'
        : 'Full · no ask: everything auto-approved — this endpoint can now run bash with no prompt, be careful');
    };
  })();

  /* 抽屉聊天贴图（JL 260731）：图先落到这块板的 fig/（/_board/image，跟评论框
     同一条路），消息里给 claude 一个 repo 根相对路径 —— session 的 cwd 是
     SPACE 根，光写 fig/… 它解析不到。 */
  wireImagePaste(chat.querySelector('textarea'),
    function () { return cq && cq.file; },
    function (rel) {
      var dir = boardDirPath().replace(/^\//, '');
      return '![image](' + (dir ? dir + '/' : '') + rel + ')';
    });

  /* 抽屉拖宽（JL 260731）：左缘一条把手，宽度记在本机。CSS 两处共用 --chatw
     （#chat 自己的宽 + body.chaton 给页面的让位），所以只动这一个变量。 */
  (function () {
    var WKEY = 'board-chat-width';
    function setW(px) {
      px = Math.max(340, Math.min(px, Math.round(window.innerWidth * 0.92)));
      document.documentElement.style.setProperty('--chatw', px + 'px');
      try { localStorage.setItem(WKEY, String(px)); } catch (e) {}
    }
    var saved = parseInt(localStorage.getItem(WKEY) || '', 10);
    if (saved) setW(saved);
    var rz = chat.querySelector('.rz');
    rz.addEventListener('pointerdown', function (e) {
      e.preventDefault();
      rz.setPointerCapture(e.pointerId);
      var move = function (ev) { setW(window.innerWidth - ev.clientX); };
      var up = function () {
        rz.removeEventListener('pointermove', move);
        rz.removeEventListener('pointerup', up);
        rz.removeEventListener('pointercancel', up);
        if (termOn) fitTerm();
      };
      rz.addEventListener('pointermove', move);
      rz.addEventListener('pointerup', up);
      rz.addEventListener('pointercancel', up);
    });
  })();

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
     (`live/turnring.py`), so the only thing a returning drawer needs in order to
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

  /* Rejoin a turn that is still running with nobody watching it.
     Returns true when it actually attached, so the caller can fall back to
     reading the transcript when nothing is live. */
  function chatRejoin() { return chatSend(null, { attach: true }); }

  async function chatSend(preset, opts) {
    /* Attach mode replays the SAME reader loop against /_board/attach instead
       of /_board/chat. Everything below the fetch is identical on purpose: a
       rejoined turn has to paint exactly like the live one it is a continuation
       of, which is the whole difference between this and the transcript
       replay it replaces. */
    var attach = !!(opts && opts.attach);
    var ta = chat.querySelector('textarea'), btn = chat.querySelector('.send');
    if (inflight) return attach ? false : chatStop();   // 正在跑 → 这一下是「停」
    if (!cq) return false;
    var msg = attach ? '' : (preset || ta.value).trim();
    if (!attach && !msg) return false;
    if (!preset && !attach) ta.value = '';
    /* On a phone the utility controls are deliberately folded.  Starting the
       next turn must give its live answer the room, rather than leaving model,
       permission and session metadata above the composer. */
    setUtility(false);
    chatBusy(true);
    var log = chatLoad(logKey());
    if (!attach) {
      bubble('you', msg); bdJump(); log.push({ k: 'you', t: msg }); chatSave(logKey(), log);
    }
    diag(attach ? 'REJOIN' : 'SEND', attach ? ('at cursor ' + curGet()) : msg.slice(0, 60));
    traceStart();
    /* A REJOIN IS A PROBE, AND A PROBE THAT FINDS NOTHING MUST SAY NOTHING.
       The sync heartbeat calls this on a timer to ask whether a turn is running
       with nobody watching, so on a quiet page it fires over and over — and it
       used to paint "Rejoining" every time, then let the watchdog escalate to
       "no reply for 60s — ⏹ to stop" and a diagnostics button, for a question
       whose honest answer was "nothing is running" (JL 260802: "why it is
       always indicating the rejoining? what is it about?"). So the label waits
       for the first real event: a rejoin that finds a live turn paints exactly
       as before, and one that finds nothing is invisible. */
    if (!attach) busyStart('Thinking');
    var ctrl = new AbortController();
    inflight = { ctrl: ctrl, file: cq.file };
    /* Watchdog. The fetch can hang with no event ever arriving, and then the
       code below never reaches chatBusy(false): red stop button, dead drawer,
       nothing moving. Report the silence, then give up rather than hang. */
    var lastEv = Date.now();
    /* A silent PROBE is the expected case, not a hang: give up in seconds and
       without a word. A real turn keeps the long, loud timings. */
    var QUIET_WARN = attach ? Infinity : 45000;
    var QUIET_GIVEUP = attach ? 6000 : 420000;
    var watchdog = setInterval(function () {
      var quiet = Date.now() - lastEv;
      /* belt and braces: something else wiped the drawer while we are still
         streaming. Re-assert the progress line rather than look dead. */
      if (inflight && !document.querySelector('#chat .busy')) {
        diag('BUSY LINE VANISHED — restoring');
        busyStart(busyWhat || 'Thinking');
      }
      if (quiet > QUIET_GIVEUP) { clearInterval(watchdog); ctrl.abort(); return; }
      if (quiet > QUIET_WARN) {
        busySay('no reply for ' + Math.round(quiet / 1000) + 's — ⏹ to stop');
        if (quiet > 60000 && busyEl && !busyEl.querySelector('.diag')) {
          var db = document.createElement('button');
          db.className = 'diag act'; db.textContent = '⚠ copy diagnostics';
          db.title = 'copies what the drawer has been doing, to paste back';
          db.onclick = function (e) {
            e.stopPropagation();
            navigator.clipboard.writeText(window.__chatDiag())
              .then(function () { db.textContent = '✓ copied — paste it to CC'; });
          };
          busyEl.appendChild(db);
        }
      }
    }, 5000);
    try {
      var r = await fetch(attach ? '/_board/attach' : '/_board/chat', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        signal: ctrl.signal,
        body: JSON.stringify(attach
        ? { path: boardPath(), file: cq.file,
            group: (cq && cq.group) || undefined, cursor: curGet() }
        : { path: boardPath(), file: cq.file,
          group: (cq && cq.group) || undefined,
          message: focusedMessage(msg),
          session: chatSid,
          name: sessName,
          stream: true,
          model: chat.querySelector('.mdl').value,
          effort: chat.querySelector('.eff').value,
          /* A one-click Quality Check is deliberately unable to inherit a
             remembered Full · no ask choice. The server independently pins
             this flag to read-only scoped mode. */
          scope: (opts && opts.scope) || chat.querySelector('.scope').value,
          quality_check: !!(opts && opts.qualityCheck) })
      });
      /* 服务器一行一条 JSON 地往下发，边收边显示 */
      /* A refusal (HOLD taken, a turn already running, no SDK) comes back as a
         400 with a JSON body, NOT as the NDJSON stream. Reading it with the
         stream parser matched no event type, so `j` stayed {ok:true} and the
         drawer printed "(no text reply)" over a real, explainable error —
         which is how a locked session came to look like a dead drawer. */
      if (!r.ok) {
        var errTxt = '';
        try { errTxt = (JSON.parse(await r.text()) || {}).err || ''; } catch (e) {}
        diag('REFUSED ' + r.status, errTxt);
        /* A REJOIN that is refused is not the reader's problem and must never
           reach the transcript. A server older than the ring answers 404 to
           /_board/attach, and because the drawer asks on open, on focus and on
           a 25s heartbeat, the polite version of this bug painted a ⚠ bubble
           into the conversation several times a minute and made a working
           drawer look broken (found 260802 by opening the live board and
           clicking the button, which is the only way this was ever going to
           show up). Fail silently and let the caller read the transcript. */
        if (attach) {
          busyEnd(); traceEnd();
          clearInterval(watchdog); window.__pendingSince = 0;
          inflight = null; chatBusy(false);
          return false;
        }
        busyEnd(); traceEnd();
        bubble('sys', '⚠ ' + (errTxt || ('the server refused this turn (HTTP ' + r.status + ')')));
        clearInterval(watchdog); window.__pendingSince = 0;
        inflight = null; chatBusy(false); ta.focus();
        return false;
      }
      /* R1: /_board/attach answers one of two ways — the rest of a live turn as
         NDJSON, or a plain JSON `live:false`. Nothing running is the ORDINARY
         case, not an error: leave the drawer exactly as it was and let the
         caller fall back to reading the transcript. */
      if (attach && (r.headers.get('Content-Type') || '').indexOf('ndjson') < 0) {
        diag('REJOIN', 'nothing live');
        busyEnd(); traceEnd();
        clearInterval(watchdog); window.__pendingSince = 0;
        inflight = null; chatBusy(false);
        return false;
      }
      var rd = r.body.getReader(), dec = new TextDecoder(), buf = '';
      var cur = null, acc = '', seg = '', j = { ok: true };
      var lastRow = null, lastSeg = '';   /* the concluding segment */
      var turnT0 = Date.now();
      var thinkEl = null, thinkAcc = '';        // 思考过程 → 一个可折叠块
      while (true) {
        var ch = await rd.read();
        if (ch.done) break;
        buf += dec.decode(ch.value, { stream: true });
        var lines = buf.split('\n'); buf = lines.pop();
        for (var i = 0; i < lines.length; i++) {
          if (!lines[i].trim()) continue;
          var ev; try { ev = JSON.parse(lines[i]); } catch (e) { continue; }
          /* A ring keepalive is NOT progress. The watchdog exists to notice a
             turn that has gone silent, so counting a ping as activity would
             make a hung turn look healthy forever. */
          if (ev.t === 'ping') continue;
          lastEv = Date.now();
          /* ask the DOM, not `busyWhat`: that variable keeps its last value
             after a turn ends, so it cannot answer "is anything painted now" */
          if (attach && !document.querySelector('#chat .busy')) busyStart('Rejoining');
          /* Remember where we are, every event, so an interruption at any
             point can be rejoined at the next one rather than from the top. */
          if (typeof ev.n === 'number') curSet(ev.n + 1);
          if (ev.t !== 'delta' && ev.t !== 'think') diag('ev:' + ev.t, ev.name || ev.text || '');
          if (ev.t === 'gap') {                   // rejoined past the buffer's front
            bubble('sys', '⚠ ' + (ev.text || 'reconnected mid-turn; some earlier output is past the buffer'));
          } else if (ev.t === 'stage') {          // real progress while nothing streams yet
            busySay(ev.text.length > 46 ? ev.text.slice(0, 46) + '…' : ev.text);
          } else if (ev.t === 'think') {          // 思考过程 → 折叠块，边想边展开
            busySay('Thinking');
            if (!thinkEl) thinkEl = thinkBubble();
            thinkAcc += ev.text;
            thinkEl.querySelector('.tk-body').textContent = thinkAcc;
            bdAuto();
          } else if (ev.t === 'delta') {
            if (busyWhat !== 'Responding') busySay('Responding');          // 逐字答案
            if (thinkEl && thinkEl.open) {        // 答案一来就收起思考；标题留个量
              thinkEl.open = false;
              thinkEl.querySelector('summary').textContent =
                '💭 Thinking (' + thinkAcc.length + ' chars — click to reopen)';
            }
            /* interim narration goes in the trace, one row per SEGMENT. `seg`
               resets at every tool boundary; the old code appended to one
               cumulative `acc` and re-rendered it into each new bubble, so every
               bubble repeated the whole turn (JL's screenshot, 260731). */
            if (!cur) { cur = traceRow('say', '✍️', ''); seg = ''; }
            seg += ev.text; acc += ev.text;
            cur.querySelector('.x').textContent = seg;
            lastRow = cur; lastSeg = seg;
            traceScroll();
          } else if (ev.t === 'text') {           // 整段（没开逐字时）
            acc += (acc ? '\n\n' : '') + ev.text;
            lastRow = traceRow('say', '✍️', ev.text); lastSeg = ev.text;
          } else if (ev.t === 'ask') {
            /* 跟 CLI 一样的权限提示：它想动东西，先问你 */
            cur = null;                       // 批准之后的输出另起一条气泡
            askUI(ev);
          } else if (ev.t === 'tool') {
            cur = null; seg = '';     /* text after a tool call is its own row */
            toolCard(ev);
            busySay(ev.name + (ev.brief ? '  ' + ev.brief.replace(ev.name + '  ', '') : ''));
          } else if (ev.t === 'tool_result') {
            toolResult(ev);
            busySay('Thinking');
          } else if (ev.t === 'done') {
            /* `done` carries the whole answer; it is rendered ONCE below, after
               the trace closes. It must not be written into `cur`, which is now
               a trace ROW rather than a bubble — setBubble would replace the
               row's own markup and the interim text would vanish with it. */
            j = Object.assign({ ok: true }, ev);
          }
        }
      }
      busyEnd();
      /* how long it ran, when it landed — measured here because the server only
         reports cost (JL 260731: "how long it takes and what is the time stamp
         it is finished along with how much it is spent") */
      var took = (Date.now() - turnT0) / 1000;
      var fin = new Date();
      /* JL 260801: the date too, not only the time. A turn that finished
         at 00:43 is ambiguous the moment the reader comes back tomorrow,
         and this board's own date form is YYMMDD. */
      var z = function (n) { return String(n).padStart(2, '0'); };
      var stamp = String(fin.getFullYear()).slice(2) + z(fin.getMonth() + 1)
                + z(fin.getDate()) + ' '
                + z(fin.getHours()) + ':' + z(fin.getMinutes());
      var tookTxt = took < 60 ? took.toFixed(1) + 's'
                  : Math.floor(took / 60) + 'm' + String(Math.round(took % 60)).padStart(2, '0') + 's';
      /* The concluding segment IS the answer, so it must not appear twice: pull
         its row OUT of the trace and render it below at full size. Everything
         before it (earlier narration, tools, thinking) stays in the trace.
         A turn with no tool calls has exactly one segment, so its trace ends up
         holding only the thinking and the answer reads as one plain reply. */
      if (lastRow && lastRow.parentNode) lastRow.parentNode.removeChild(lastRow);
      /* The context meter, which the CLI shows under /context and the drawer
         never had (JL 260801: "我怎么看到我现在这个 context 的 usage，就是用了
         百分之几"). It rides the turn's own done event, so it costs no extra
         call, and it is absent rather than wrong on an SDK that cannot report
         it. Shown on the trace label, beside how long the turn took. */
      var ctxTxt = '';
      if (j.ctx && typeof j.ctx.pct === 'number') {
        var k = function (n) {
          return typeof n === 'number' ? Math.round(n / 1000) + 'k' : '?';
        };
        ctxTxt = ' · ctx ' + Math.round(j.ctx.pct) + '%'
               + (j.ctx.used ? ' (' + k(j.ctx.used) + '/' + k(j.ctx.max) + ')' : '');
        var cw = chat.querySelector('.cost');
        if (cw) cw.textContent = 'ctx ' + Math.round(j.ctx.pct) + '%'
                               + (typeof j.usd === 'number' ? ' · $' + j.usd.toFixed(3) : '');
      }
      traceEnd(tookTxt + ' · finished ' + stamp + ctxTxt);
      var txt = j.ok ? (lastSeg || j.text || acc ||
                        '(no text reply — it may have only used tools)')
                     : ('⚠ ' + (j.err || 'failed'));
      if (j.stopped) txt = txt + '\n(you stopped this turn, so it may be unfinished)';
      bubble('cc', txt);              /* the answer, once, at full size */
      /* history keeps the WHOLE turn, not just its last line */
      log.push({ k: 'cc', t: (j.ok ? (j.text || acc || txt) : txt) });
      chatSave(logKey(), log);
      if (j.ok) {
        // 这一轮聊到的 session 现在就是 current（服务器已写回头部）——
        // 拣选状态归位、清单重拉，免得下一条还带着旧的点名
        if (j.session) {
          /* The server has just told us which session this turn actually ran
             in, which for a NEW one is the first time that id exists anywhere.
             Move the log we wrote under the '#new' key onto the real id, adopt
             it as the shown session, and repaint the header — otherwise a new
             session's first turn is stored where nothing will ever look for it
             and `.sid` keeps naming the session you started from. */
          if (j.session !== activeSid) {
            var oldKey = logKey();
            activeSid = j.session;
            chatSave(logKey(), log);
            try { localStorage.removeItem(CHATK(oldKey)); } catch (e) {}
            paintSid(activeSid);
          }
          chatSid = ''; sessName = ''; loadSessions();
        }
        var bits = [];
        if (j.model) bits.push(j.model.replace('claude-', '') + ' / ' + j.effort);
        if (j.scope) bits.push({scoped:'scoped',full:'full·ask',bypass:'full·no-ask'}[j.scope] || j.scope);
        if (j.usd != null) bits.push('$' + Number(j.usd).toFixed(3));
        bits.push(tookTxt);
        bits.push('finished ' + stamp);
        if (j.denied && j.denied.length) bits.push('blocked ' + j.denied.length + ' tool call' + (j.denied.length > 1 ? 's' : ''));
        // 只有真的写了盘上文件，才说「已写盘」并给刷新按钮 —— 读一读不该出现
        if (j.wrote) {
          bits.push('written to disk');
          bubble('sys', bits.join(' · '));
          var rb = document.createElement('button');
          rb.className = 'act pri'; rb.textContent = '↻ Refresh in place';
          rb.onclick = function () { (window.__boardRefresh || function () { location.reload(); })(); };
          chat.querySelector('.acts').replaceChildren(rb);
        } else if (bits.length) {
          bubble('sys', bits.join(' · '));   // 只报模型/花费，不提写盘、不换按钮
        }
      }
    } catch (e) {
      busyEnd(); traceEnd();     /* a failed turn still closes its trace */
      bubble('sys', e.name === 'AbortError'
        ? 'Stopped waiting. The server got the stop signal too.'
        : '⚠ ' + e.message);
      /* KEEP WHAT ARRIVED. The answer was only written to the local log at
         'done', so a turn that never got there left the question saved and the
         reply lost: reopening showed your own message with nothing under it,
         and the text seemed to reappear only once a new message was sent
         (JL 260801: "只有我发一个新的 message 之后，你的 response 才能显现出来").
         Whatever streamed is real; save it, marked, instead of dropping it. */
      try {
        if (acc && acc.trim()) {
          /* `partial` is what lets syncFromServer REPLACE this later. Without
             it the local log is the same LENGTH as the server's, and the
             length test concluded the server knew nothing new, so a half
             answer could never be upgraded to the real one. */
          log.push({ k: 'cc', t: acc + '\n\n(this turn was cut short)', partial: true });
          chatSave(logKey(), log);
        }
      } catch (e2) {}
    }
    clearInterval(watchdog);
    window.__pendingSince = 0;
    inflight = null; chatBusy(false);
    if (!attach) ta.focus();     // a rejoin must not steal focus from a reader
    drainQueue();                       // whatever you typed while it ran
    if (followPending && !inflight) follow();   // you navigated while it ran
    return true;
  }
  chat.querySelector('.send').onclick = function () { chatSend(); };
  chat.querySelector('textarea').addEventListener('keydown', function (ev) {
    if (ev.key === 'Enter' && !ev.shiftKey) {
      ev.preventDefault();
      var ta = ev.target, txt = ta.value.trim();
      if (inflight) {                     // a turn is running: queue, never race
        if (txt) { queueMsg(txt); ta.value = ''; }
        return;
      }
      chatSend();
    }
    if (ev.key === 'Escape' && sentenceFocus) {
      ev.preventDefault();
      clearSentenceFocus();
    }
  });
