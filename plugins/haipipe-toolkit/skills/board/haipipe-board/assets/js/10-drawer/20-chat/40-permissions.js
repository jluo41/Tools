  /* 权限提示 —— 行为跟 Claude Code CLI 一致：只读的自动放行，
     会动东西的弹出来问；「总是允许」只在这一轮这一题里有效。 */
  function askUI(ev) {
    var box = document.createElement('div');
    box.className = 'ask';
    box.innerHTML = '<div class="q">Allow this tool?</div>' +
      '<div class="w"><code></code></div>' +
      '<div class="b"><button class="ok y">Allow once</button>' +
      '<button class="a">Always allow</button><button class="n">Deny</button></div>';
    box.querySelector('code').textContent = ev.brief || ev.tool;
    /* diff preview — what the VS Code extension shows at its gate: the actual
       proposed change. − old in red, + new in green, Bash commands verbatim. */
    if (ev.detail) {
      var d = ev.detail, dv = document.createElement('div');
      dv.className = 'askd';
      var pre = function (cls, txt) {
        var p = document.createElement('pre'); p.className = cls; p.textContent = txt;
        dv.appendChild(p);
      };
      if (d.command) pre('cmd', d.command);
      else if (d.edits) {
        d.edits.forEach(function (e) { if (e.old) pre('del', e.old); if (e.new) pre('add', e.new); });
        if (d.count > d.edits.length) {
          var m = document.createElement('div'); m.className = 'mut';
          m.textContent = '… ' + (d.count - d.edits.length) + ' more edit(s)';
          dv.appendChild(m);
        }
      } else {
        if (d.old) pre('del', d.old);
        if (d.new) pre('add', d.new);
      }
      if (dv.childNodes.length) box.insertBefore(dv, box.querySelector('.b'));
    }
    chat.querySelector('.bd').appendChild(box);
    bdJump();          /* a gate needs an answer: this one may interrupt reading */
    var send = function (ok, always) {
      box.querySelector('.b').innerHTML =
        '<span class="mut">' + (ok ? (always ? 'Always allowed' : 'Allowed') : 'Denied') + '</span>';
      fetch('/_board/answer', { method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: ev.id, ok: ok, always: always }) })
        .catch(function () {});
    };
    box.querySelector('.y').onclick = function () { send(true, false); };
    box.querySelector('.a').onclick = function () { send(true, true); };
    box.querySelector('.n').onclick = function () { send(false, false); };
  }
  function chatActs(sec) {
    var isBoard = (sec === 'board');
    var box = chat.querySelector('.acts');
    box.innerHTML = '';
    var add = function (label, fn, primary) {
      var b = document.createElement('button');
      b.className = 'act' + (primary ? ' pri' : '');
      b.textContent = label; b.onclick = fn;
      box.appendChild(b);
    };
    add('✅ Quality Check', function () {
      var prompt = isBoard
        ? 'QUALITY CHECK — answer only. Do not modify any file or run commands. ' +
          'Check this Board against its declared structure and completion rules. ' +
          'Report exactly: ✅ Meets; ⚠️ Needs work; evidence (page/section); and the 1–3 smallest proposed fixes. ' +
          'Separate mechanical consistency from human readability. Do not claim a rule is met unless you can name its evidence.'
        : 'QUALITY CHECK — answer only. Do not modify any file or run commands. ' +
          'First use Read to load the canonical evaluation contract at ' +
          'Tools/plugins/haipipe-toolkit/skills/board/haipipe-board-page/SKILL.md and the cold-read rules at ' +
          'Tools/plugins/haipipe-toolkit/skills/board/haipipe-board/ref/writing-rules.md. ' +
          'Resolve requirements in order: base contract; page-kind or consumer variant; this page\'s Writing Style ' +
          'and Stage Contract; then each local division purpose and paragraph job. Report any conflict instead of choosing silently. ' +
          'Review every present ## section, every direct ### Content division, and every #### paragraph whose job must be tested. ' +
          'Report exactly: Requirement conflicts; then a table with unit | applicable requirements + source | verdict | evidence | smallest fix; ' +
          'then Mechanical findings; then one Page verdict. Use only MEETS, NEEDS WORK, N/A, or NOT VERIFIABLE. ' +
          'Separate mechanics, function, evidence, and readability. Every MEETS needs visible evidence; NOT VERIFIABLE is never a pass.';
      chatSend(prompt, { scope: 'scoped', qualityCheck: true });
    }, true);
    add('📍 Where are we?', function () {
      askHere('Answer only, do not edit any file: summarize the current status, ' +
               'what is decided, what remains open, and the one concrete blocker. ' +
               'Use short bullets with evidence from this page.');
    });
    add('➡️ What next?', function () {
      askHere('Answer only, do not edit any file: propose the smallest valuable ' +
               'next step. Name its owner, the evidence it needs, and which item it closes.');
    });
    add('🎯 Clarify aim', function () {
      askHere('Answer only, do not edit any file: rewrite this page\'s aim/question ' +
               'as one plain-language sentence. Then identify any ambiguity that still ' +
               'needs a human decision.');
    });
    if (isBoard) {
      add('🧭 Which question should I act on?', function () {
        askHere('Answer only, do not edit any file: which page on this board should ' +
                 'be acted on next, and why? Consider page state and open Aim States. ' +
                 'Give 1-3 candidates, one line each: id · reason.');
      });
    } else {
      add('📝 What is this question missing?', function () {
        askHere('Answer only, do not edit any file: which Aims on this page have ' +
                 'a State other than met or held, and what is each one blocked on? ' +
                 'One per line, using the Aim id.');
      });
    }
    add('↻ Refresh', function () { (window.__boardRefresh || function () { location.reload(); })(); });
  }
  /* ONE door for every "ask this" affordance in the drawer. Whichever half is
     on screen is the half that receives it (JL 260801). */
  function askHere(prompt, opts) {
    if (window.__boardTermOn && window.__boardTermOn()) {
      if (window.__boardTermType(prompt)) return;
    }
    chatSend(prompt, opts);
  }


  async function chatOpen(sec) {
    /* sec 是某一题的 <section>，或字符串 'board'（QD5）：整板会话，挂在 board.md 上。
       服务器端认 file=board.md，规则和开场定位换成整板那份；session 记在 board.md 头部。 */
    var isBoard = (sec === 'board');
    var sameTarget =
      (isBoard && cq && cq.board) ||
      (sec && sec.group && cq && cq.group === sec.group) ||
      (sec && sec.id && cq && cq.id === sec.id);

    /* REOPENING THE SAME CHAT IS NOT A REASON TO REBUILD IT (JL 260801: "我把
       它打开、关了、又打开，它就没有那么丝滑了 ... VS Code 的 plugin 无论什么
       时候开它都是非常丝滑的").
       That is exactly what VS Code does differently: its webview is RETAINED,
       so hiding a panel changes visibility and nothing else, and showing it
       again costs one repaint. Ours tore the transcript down and built every
       bubble again from storage, re-parsing markdown for each one, and then
       sometimes wiped and rebuilt a second time when the server answered. All
       of that work produced a transcript identical to the one just thrown
       away, and the flash between the two is the thing that reads as janky.
       So when the same scope is already painted and nothing is running, just
       show it. The server is still asked, quietly, through the sync. */
    if (!inflight && sameTarget && chat.querySelector('.bd').children.length) {
      chat.classList.add('on'); document.body.classList.add('chaton');
      requestAnimationFrame(bdJump);
      chat.querySelector('textarea').focus();
      if (typeof syncNow === 'function') syncNow();
      return;
    }

    /* NEVER re-open over a turn that is still streaming (JL 260731: "why the
       progress is not shown here again?"). This function clears .bd, calls
       busyEnd() and drops traceEl, so running it mid-turn leaves the user
       bubble replayed from the log, the trace orphaned, nothing rendering and
       the ⏹ button stuck — which is exactly what the screenshot showed. A
       rebuild, a hash bounce, or a stray follow() can all land us here. */
    if (inflight) {
      diag('chatOpen WHILE INFLIGHT', (sec && sec.id) || (isBoard ? 'board' : '?'));
      if (sameTarget) {                    // same page: leave the live turn alone
        /* ...but still OPEN it. The early return sat above the line that adds
           .on, so closing the drawer mid-turn and pressing 💬 again did
           nothing at all: the turn was fine, the drawer just never came back. */
        chat.classList.add('on'); document.body.classList.add('chaton');
        requestAnimationFrame(bdJump);
        return;
      }
      try { inflight.ctrl.abort(); } catch (e) {}   // switching away: end it cleanly
    }
    var isGroup = !!(sec && sec.group);            // 组级会话（JL 260731）
    clearSentenceFocus();
    if (isBoard) {
      var h1 = document.querySelector('.h1');
      cq = { id: 'BOARD', file: 'board.md',
             title: (h1 ? h1.textContent : 'this board'), board: true };
    } else if (isGroup) {
      var gl = (sec.group.match(/^\s*(\S+)/) || [])[1] || sec.group;
      cq = { id: gl, file: 'board.md', group: sec.group, title: sec.group };
    } else {
      cq = { id: sec.id, file: sec.getAttribute('data-file') || '',
             title: sec.getAttribute('data-title') || '' };
    }
    chat.querySelector('.qid').textContent = isBoard ? '🗂 BOARD'
      : isGroup ? '🗂 ' + cq.id : cq.id;
    chat.querySelector('.ti').textContent = cq.title;
    chat.querySelector('.ti').title = cq.title;
    chat.querySelector('textarea').placeholder = isBoard
      ? 'Ask about this board — e.g. what should we act on next?'
      : isGroup ? 'Ask about this group — its pages, gaps, and order…'
      : 'Ask about this question…';
    /* leaving a page mid-turn: stop the ticker and forget the trace BEFORE the
       transcript is cleared, or the interval keeps writing to a detached node */
    busyEnd(); traceEl = null; toolCards = {};
    /* BIND THE SESSION FIRST. Everything below — the local log key, the body,
       the picker highlight — is now a render of `activeSid`, so it has to be
       known before the first paint rather than assigned twenty lines later.
       这一题的 Claude Code session id —— 抽屉和终端用的是同一个；整板会话的 id 在
       .wrap 的 data-bsession 上（live swap 会跟着换）。 */
    activeSid = isBoard
      ? ((document.querySelector('.wrap') || document.body).getAttribute('data-bsession') || '')
      : isGroup ? ''
      : (sec.getAttribute('data-session') || '');
    chatSid = '';                 // 换题回到「跟着头部 current」；清单重新拉
    var bd = chat.querySelector('.bd'); bd.innerHTML = '';
    var log = chatLoad(logKey());
    if (!log.length) bubble('sys', isBoard
      ? 'This chat sees the WHOLE board — ask it which question to act on, or have it edit the Pages.'
      : isGroup
      ? 'This chat sees the GROUP ' + cq.group + ' — its pages, their states, and how they fit.'
      : 'This chat is attached to ' + cq.file);
    log.forEach(replayRow);
    /* The local paint above is instant; the server holds the truth.
       R1: this goes through syncNow rather than straight to syncFromServer,
       because REOPENING AFTER A RELOAD is the single most important moment to
       rejoin a running turn — the transcript cannot answer then, since it is
       not written until the turn ends. syncNow asks the ring first and falls
       back to the transcript only when nothing is live. */
    syncNow();
    syncSchedule();          /* and keep asking; one shot at open WAS the bug */
    /* TUI first, unless the reader has chosen the chat box (JL 260801) */
    if (window.__boardOpenDefaultView) {
      setTimeout(function () { try { window.__boardOpenDefaultView(); } catch (e) {} }, 0);
    }
    chat.querySelector('.tip').textContent = isBoard ? 'board.md · whole-board session'
      : isGroup ? cq.group + ' · group session' : cq.file;
    /* one painter, shared with switchTo, so the header can never describe a
       different session from the one the body is showing */
    paintSid(activeSid);
    chatActs(isGroup ? null : sec);
    loadSessions();
    termView(false); disposeTerm();
    chat.classList.add('on'); document.body.classList.add('chaton');
    /* Land on the NEWEST message, not the oldest (JL 260801: "它还是一直在最
       上面 ... 我还得往下面去翻"). bubble() already scrolls on every append,
       but the replay above runs while #chat is still display:none, where
       scrollHeight is 0 and every scrollTop assignment is clamped to 0. The
       drawer only becomes visible on the line above, so the scroll has to
       happen after layout, which is what the frame callback buys. */
    requestAnimationFrame(bdJump);

    chat.querySelector('textarea').focus();
  }
  function chatClose() {
    chat.classList.remove('on'); document.body.classList.remove('chaton');
  }
  chat.querySelector('.x').onclick = chatClose;
  chat.querySelector('.back').onclick = chatClose;   /* same act, named for where it goes */
