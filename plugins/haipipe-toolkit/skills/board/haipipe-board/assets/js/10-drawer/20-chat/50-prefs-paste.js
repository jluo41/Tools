  /* 模型 / effort / 权限档 记在本机；默认 Opus 4.8 · high · 完整·问我 */
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
      var dir = location.pathname.replace(/\/[^\/]*$/, '').replace(/^\//, '');
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
    var d = bubble('you', text);
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

  async function chatSend(preset, opts) {
    var ta = chat.querySelector('textarea'), btn = chat.querySelector('.send');
    if (inflight) return chatStop();       // 正在跑 → 这一下是「停」
    var msg = (preset || ta.value).trim();
    if (!msg || !cq) return;
    if (!preset) ta.value = '';
    /* On a phone the utility controls are deliberately folded.  Starting the
       next turn must give its live answer the room, rather than leaving model,
       permission and session metadata above the composer. */
    setUtility(false);
    chatBusy(true);
    var log = chatLoad(cq.id);
    bubble('you', msg); log.push({ k: 'you', t: msg }); chatSave(cq.id, log);
    diag('SEND', msg.slice(0, 60));
    traceStart();
    busyStart('Thinking');
    var ctrl = new AbortController();
    inflight = { ctrl: ctrl, file: cq.file };
    /* Watchdog. The fetch can hang with no event ever arriving, and then the
       code below never reaches chatBusy(false): red stop button, dead drawer,
       nothing moving. Report the silence, then give up rather than hang. */
    var lastEv = Date.now();
    var QUIET_WARN = 45000, QUIET_GIVEUP = 420000;
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
      var r = await fetch('/_board/chat', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        signal: ctrl.signal,
        body: JSON.stringify({ path: boardPath(), file: cq.file,
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
        busyEnd(); traceEnd();
        bubble('sys', '⚠ ' + (errTxt || ('the server refused this turn (HTTP ' + r.status + ')')));
        clearInterval(watchdog); window.__pendingSince = 0;
        inflight = null; chatBusy(false); ta.focus();
        return;
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
          lastEv = Date.now();
          if (ev.t !== 'delta' && ev.t !== 'think') diag('ev:' + ev.t, ev.name || ev.text || '');
          if (ev.t === 'stage') {                 // real progress while nothing streams yet
            busySay(ev.text.length > 46 ? ev.text.slice(0, 46) + '…' : ev.text);
          } else if (ev.t === 'think') {          // 思考过程 → 折叠块，边想边展开
            busySay('Thinking');
            if (!thinkEl) thinkEl = thinkBubble();
            thinkAcc += ev.text;
            thinkEl.querySelector('.tk-body').textContent = thinkAcc;
            chat.querySelector('.bd').scrollTop = 1e9;
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
      var stamp = String(fin.getHours()).padStart(2, '0') + ':'
                + String(fin.getMinutes()).padStart(2, '0');
      var tookTxt = took < 60 ? took.toFixed(1) + 's'
                  : Math.floor(took / 60) + 'm' + String(Math.round(took % 60)).padStart(2, '0') + 's';
      /* The concluding segment IS the answer, so it must not appear twice: pull
         its row OUT of the trace and render it below at full size. Everything
         before it (earlier narration, tools, thinking) stays in the trace.
         A turn with no tool calls has exactly one segment, so its trace ends up
         holding only the thinking and the answer reads as one plain reply. */
      if (lastRow && lastRow.parentNode) lastRow.parentNode.removeChild(lastRow);
      traceEnd(tookTxt + ' · finished ' + stamp);
      var txt = j.ok ? (lastSeg || j.text || acc ||
                        '(no text reply — it may have only used tools)')
                     : ('⚠ ' + (j.err || 'failed'));
      if (j.stopped) txt = txt + '\n(you stopped this turn, so it may be unfinished)';
      bubble('cc', txt);              /* the answer, once, at full size */
      /* history keeps the WHOLE turn, not just its last line */
      log.push({ k: 'cc', t: (j.ok ? (j.text || acc || txt) : txt) });
      chatSave(cq.id, log);
      if (j.ok) {
        // 这一轮聊到的 session 现在就是 current（服务器已写回头部）——
        // 拣选状态归位、清单重拉，免得下一条还带着旧的点名
        if (j.session) { chatSid = ''; sessName = ''; loadSessions(); }
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
    }
    clearInterval(watchdog);
    window.__pendingSince = 0;
    inflight = null; chatBusy(false); ta.focus();
    drainQueue();                       // whatever you typed while it ran
    if (followPending && !inflight) follow();   // you navigated while it ran
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
