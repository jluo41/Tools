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
    chat.querySelector('.bd').scrollTop = 1e9;
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
          'Inspect this question against its declared template and purpose: aim/question clarity, required sections, ' +
          'Content answering the question, testable Items to Finish, and an honest Where we are. ' +
          'Report exactly: ✅ Meets; ⚠️ Needs work; evidence (section or text); and the 1–3 smallest proposed fixes. ' +
          'Separate mechanical consistency from human readability. Do not claim a rule is met unless you can name its evidence.';
      chatSend(prompt, { scope: 'scoped', qualityCheck: true });
    }, true);
    add('📍 Where are we?', function () {
      chatSend('Answer only, do not edit any file: summarize the current status, ' +
               'what is decided, what remains open, and the one concrete blocker. ' +
               'Use short bullets with evidence from this page.');
    });
    add('➡️ What next?', function () {
      chatSend('Answer only, do not edit any file: propose the smallest valuable ' +
               'next step. Name its owner, the evidence it needs, and which item it closes.');
    });
    add('🎯 Clarify aim', function () {
      chatSend('Answer only, do not edit any file: rewrite this page\'s aim/question ' +
               'as one plain-language sentence. Then identify any ambiguity that still ' +
               'needs a human decision.');
    });
    if (isBoard) {
      add('🧭 Which question should I act on?', function () {
        chatSend('Answer only, do not edit any file: which page on this board should ' +
                 'be acted on next, and why? Consider state and unchecked items. ' +
                 'Give 1-3 candidates, one line each: id · reason.');
      });
    } else {
      add('📝 What is this question missing?', function () {
        chatSend('Answer only, do not edit any file: which items in this question\'s ' +
                 '## Done when are still unchecked, and what is each one blocked on? ' +
                 'One per line.');
      });
    }
    add('↻ Refresh', function () { (window.__boardRefresh || function () { location.reload(); })(); });
  }

  async function chatOpen(sec) {
    /* sec 是某一题的 <section>，或字符串 'board'（QD5）：整板会话，挂在 board.md 上。
       服务器端认 file=board.md，规则和开场定位换成整板那份；session 记在 board.md 头部。 */
    var isBoard = (sec === 'board');
    /* NEVER re-open over a turn that is still streaming (JL 260731: "why the
       progress is not shown here again?"). This function clears .bd, calls
       busyEnd() and drops traceEl, so running it mid-turn leaves the user
       bubble replayed from the log, the trace orphaned, nothing rendering and
       the ⏹ button stuck — which is exactly what the screenshot showed. A
       rebuild, a hash bounce, or a stray follow() can all land us here. */
    if (inflight) {
      diag('chatOpen WHILE INFLIGHT', (sec && sec.id) || (isBoard ? 'board' : '?'));
      var sameTarget =
        (isBoard && cq && cq.board) ||
        (sec && sec.group && cq && cq.group === sec.group) ||
        (sec && sec.id && cq && cq.id === sec.id);
      if (sameTarget) return;              // same page: leave the live turn alone
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
    var bd = chat.querySelector('.bd'); bd.innerHTML = '';
    var log = chatLoad(isGroup ? 'G:' + cq.id : cq.id);
    if (!log.length) bubble('sys', isBoard
      ? 'This chat sees the WHOLE board — ask it which question to act on, or have it edit the Pages.'
      : isGroup
      ? 'This chat sees the GROUP ' + cq.group + ' — its pages, their states, and how they fit.'
      : 'This chat is attached to ' + cq.file);
    log.forEach(function (m) { bubble(m.k, m.t); });
    chat.querySelector('.tip').textContent = isBoard ? 'board.md · whole-board session'
      : isGroup ? cq.group + ' · group session' : cq.file;
    /* 这一题的 Claude Code session id —— 抽屉和终端用的是同一个。
       整板会话的 id 在 .wrap 的 data-bsession 上（live swap 会跟着换）。 */
    var sid = isBoard
      ? ((document.querySelector('.wrap') || document.body).getAttribute('data-bsession') || '')
      : isGroup ? ''
      : (sec.getAttribute('data-session') || '');
    var sidbox = chat.querySelector('.sid');
    /* session 归档在 cwd（= serve.py 的 --root，现在是 SPACE 根）下的 project 目录，
       所以要 cd 到 root，不是板文件夹 —— cd 错了 --resume 就找不到这个 session。
       root 精确算法：serve.py 在 <root> + location.pathname 处提供文件，
       所以 root = 板文件夹绝对路径 减去 URL 里的那段目录。不靠 .git/pyproject 猜。 */
    var board = document.body.getAttribute('data-board') || '.';
    var urlDir = location.pathname.replace(/\/[^\/]*$/, '');   // 去掉 board.html
    var root = board;
    if (urlDir && board.slice(-urlDir.length) === urlDir) {
      root = board.slice(0, board.length - urlDir.length) || '/';
    }
    if (sid) {
      sidbox.innerHTML = '<code>' + sid + '</code>';
      // 复制的是一整条能直接跑的命令（带注释说明是哪一题），不是光一个 uuid
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
    } else {
      sidbox.innerHTML = '<span class="mut">' + (isGroup
        ? 'Group sessions live in the 🗂 strip above — pick one or start a new one.'
        : 'No session yet — it appears after your first message and is written into the header of ' + cq.file) + '</span>';
    }
    chatActs(isGroup ? null : sec);
    chatSid = '';                 // 换题回到「跟着头部 current」；清单重新拉
    loadSessions();
    termView(false); disposeTerm();
    chat.classList.add('on'); document.body.classList.add('chaton');

    chat.querySelector('textarea').focus();
  }
  chat.querySelector('.x').onclick = function () {
    chat.classList.remove('on'); document.body.classList.remove('chaton'); };
