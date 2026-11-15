  async function chatSend(preset, opts) {
    /* Attach mode replays the SAME reader loop against /_board/attach instead
       of /_board/chat. Everything below the fetch is identical on purpose: a
       rejoined turn has to paint exactly like the live one it is a continuation
       of, which is the whole difference between this and the transcript
       replay it replaces. */
    /* ⚠️ DEAD PATH. `chatRejoin` calls `chatAttach` now, so nothing passes
       `{attach:true}` any more and every `attach` branch below is unreachable.
       It is left in place rather than surgically removed from a 250-line
       function at the end of a long session, but DO NOT FIX BUGS IN IT: that
       is exactly how the same rejoin defect got patched twice and missed a
       third branch (260802). The live rejoin is `chatAttach`, above. */
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
    /* A REJOIN IS A EVIDENCE, AND A EVIDENCE THAT FINDS NOTHING MUST SAY NOTHING.
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
    var stoppedByUser = false;
    inflight.mark = function () { stoppedByUser = true; };
    /* Watchdog. The fetch can hang with no event ever arriving, and then the
       code below never reaches chatBusy(false): red stop button, dead drawer,
       nothing moving. Report the silence, then give up rather than hang. */
    var lastEv = Date.now();
    /* A silent EVIDENCE is the expected case, not a hang: give up in seconds and
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
          scope: labelingHold ? 'scoped' :
                 ((opts && opts.scope) || chat.querySelector('.scope').value),
          quality_check: !!(opts && opts.qualityCheck) || labelingHold })
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
          /* A keepalive is not progress FOR A TURN — the watchdog exists to
             notice one that has gone silent, so counting it would make a hung
             turn look healthy. For a REJOIN it is the opposite: a ping is the
             server saying the turn is alive and still working, and the only
             thing the rejoin is waiting for. Without this the 6s give-up below
             fired on every single rejoin, because between events the ring
             sends nothing else (JL 260802: ~120 × "Stopped waiting"). */
          if (ev.t === 'ping') { if (attach) lastEv = Date.now(); continue; }
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
      /* A REJOIN THAT FAILS IS NEVER THE READER'S PROBLEM, and it must never
         reach the transcript. The drawer rejoins on open, on focus, on a 25s
         heartbeat and on four backoff timers, so one noisy failure path is not
         one message: it is a wall of them. JL got ~120 of "Stopped waiting.
         The server got the stop signal too." on one page (260802), and that
         sentence was a lie twice over — nobody pressed stop and no stop signal
         was sent. The 404 half of this was made silent earlier the same day;
         this is the half that was missed, which is abort, network and anything
         else that throws. Fail quietly and let the transcript speak. */
      if (attach) {
        clearInterval(watchdog); window.__pendingSince = 0;
        inflight = null; chatBusy(false);
        diag('REJOIN', 'gave up quietly: ' + (e.name || e.message || 'error'));
        return false;
      }
      if (!(e.name === 'AbortError' && stoppedByUser)) {
        bubble('sys', e.name === 'AbortError'
          ? 'Stopped waiting. The server got the stop signal too.'
          : '⚠ ' + e.message);
      }
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
