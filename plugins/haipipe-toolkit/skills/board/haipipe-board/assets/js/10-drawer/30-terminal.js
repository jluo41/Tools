  /* ── ⌨ 真终端：同一个 session 换个窗口 ────────────────────────
     LAW（JL 260723）：一个 session 同时只能有一个窗口。
     抽屉和终端读写的是磁盘上同一个 .jsonl，两边同时开会互相盖或者 fork 出第二段历史。
     所以开终端前服务器先看抽屉在不在用；从终端切回来时要「交回 session」。 */
  var termOn = false;
  function termView(on) {
    termOn = on;
    // body 上留个记号给刷新轮询看：终端开着时资产戳变化只挂角标、不整页 reload
    document.body.classList.toggle('termon', on);
    if (!on && window.__pendingReload) { location.reload(); return; }
    chat.querySelector('.tm').style.display = on ? 'block' : 'none';
    ['.sfocus', '.bd', '.acts', '.cfg', '.sid', '.ft', '.tip'].forEach(function (s) {
      var e = chat.querySelector(s); if (e) e.style.display = on ? 'none' : '';
    });
    var b = chat.querySelector('.term');
    b.textContent = on ? '←' : '>_';
    b.setAttribute('aria-label', on ? 'Back to chat' : 'Open terminal');
    b.title = on ? 'Back to the web chat (hands the session back)' : 'Open this question in a real terminal (same session)';
    if (on && termT) setTimeout(fitTerm, 0);
  }

  /* ── xterm.js 直接画在抽屉里（不再用 iframe，closer to myrlin）──────
     终端后端仍是 serve.py 起的 ttyd；这里我们自己拿 xterm 连它的 WebSocket，
     省掉 iframe 那层（CSP、加载慢、控制不了）。ttyd 的 WS 子协议：
       连接子协议 'tty'；开场发 JSON auth；输入 '0'+data；输出帧首字节 '0'。 */
  var termT = null, termWS = null, xtermP = null;
  function loadXterm() {
    if (xtermP) return xtermP;
    xtermP = new Promise(function (res, rej) {
      var css = document.createElement('link');
      css.rel = 'stylesheet'; css.href = '/_board/asset/xterm.css';
      document.head.appendChild(css);
      var s = document.createElement('script');
      s.src = '/_board/asset/xterm.min.js';
      s.onload = function () {
        // unicode11 addon: claude's TUI counts 🟡✅💬 as 2 cells (modern wcwidth);
        // xterm's built-in tables are Unicode 6 and say 1 — every emoji shifts the
        // row and repaints land off-cell (the QD3 smeared-frames screenshot).
        var u = document.createElement('script');
        u.src = '/_board/asset/addon-unicode11.js';
        u.onload = function () { res(window.Terminal); };
        u.onerror = function () {
          console.warn('addon-unicode11 missing — emoji-heavy TUIs may smear (restart serve.py?)');
          res(window.Terminal);
        };
        document.head.appendChild(u);
      };
      s.onerror = function () { rej(new Error('xterm.js failed to load (is serve.py running?)')); };
      document.head.appendChild(s);
    });
    return xtermP;
  }
  function cellDims() {
    // xterm's rendered cell size — the truth the pty must match. Guessed
    // constants drift with CJK-heavy fonts and mangle claude's TUI columns
    // (JL's screenshot, fig/qd3-reconnect-after-release-260724.png).
    try {
      var d = termT._core._renderService.dimensions;
      var w = d.css ? d.css.cell.width : d.actualCellWidth;
      var h = d.css ? d.css.cell.height : d.actualCellHeight;
      if (w > 3 && h > 6) return { w: w, h: h };
    } catch (e) {}
    return { w: 8.4, h: 17 };
  }
  function fitTerm() {
    if (!termT) return;
    var host = chat.querySelector('.tm');
    var w = host.clientWidth, h = host.clientHeight;
    if (w < 40 || h < 40) return;
    var c = cellDims();
    var cols = Math.max(20, Math.floor((w - 16) / c.w));
    var rows = Math.max(6, Math.floor((h - 12) / c.h));
    try { termT.resize(cols, rows); } catch (e) {}
  }
  var termKey = null, termRetry = 0, termPing = null, termClosing = false, termRespawn = false;
  function disposeTerm() {
    termClosing = true;                       // an intentional close never reconnects
    if (termPing) { clearInterval(termPing); termPing = null; }
    try { if (termWS) termWS.close(); } catch (e) {}
    try { if (termT) termT.dispose(); } catch (e) {}
    termWS = null; termT = null; termKey = null; termRetry = 0;
    var host = chat.querySelector('.tm'); if (host) host.innerHTML = '';
  }
  /* smoothness (QD3 260724): the WS is rebuilt on drops, the TERMINAL is not —
     scrollback survives a reconnect; the post-auth resize (SIGWINCH) makes
     claude repaint. Keepalive = a same-size resize op every 30s, so an idle
     relay/proxy never reaps the pipe. */
  function connectWS(key) {
    var proto = location.protocol === 'https:' ? 'wss://' : 'ws://';
    var ws = new WebSocket(proto + location.host + '/_term/' + key + '/ws', ['tty']);
    ws.binaryType = 'arraybuffer';
    termWS = ws;
    window.__wsDbg = { state: 'new', msgs: 0, err: null };
    ws.onopen = function () {
      window.__wsDbg.state = 'open';
      termRetry = 0; termRespawn = false;
      setTimeout(fitTerm, 350);            // refit with REAL cell metrics, repaints claude
      // the ttyd handshake: auth as one message, size as another (merged = no output)
      ws.send(JSON.stringify({ AuthToken: '' }));
      ws.send(JSON.stringify({ columns: termT.cols || 100, rows: termT.rows || 30 }));
      if (termPing) clearInterval(termPing);
      termPing = setInterval(function () {           // keepalive: same-size resize op
        if (ws.readyState === 1 && termT)
          ws.send('1' + JSON.stringify({ columns: termT.cols, rows: termT.rows }));
      }, 30000);
    };
    ws.onmessage = function (ev) {
      window.__wsDbg.msgs++;
      var d = ev.data;
      if (typeof d === 'string') { if (d.charCodeAt(0) === 48) termT.write(d.slice(1)); return; }
      var b = new Uint8Array(d);
      if (b[0] === 48) termT.write(new TextDecoder().decode(b.subarray(1)));
    };
    ws.onerror = function (e) { window.__wsDbg.err = 'error'; };
    ws.onclose = function (e) {
      window.__wsDbg.state = 'closed:' + (e && e.code);
      if (termPing) { clearInterval(termPing); termPing = null; }
      if (termClosing || !termOn || !termT) return;  // closed on purpose → stay quiet
      if (termRetry >= 2 && !termRespawn) {
        // the socket keeps dying → the ttyd behind it is probably GONE (released
        // or reaped), and no amount of reconnecting revives a dead terminal.
        // Ask serve.py for a fresh one — --resume brings the same session back.
        termRespawn = true;
        termT.write('\r\n\x1b[90m[terminal is gone — restarting it (same session)…]\x1b[0m\r\n');
        termOpen(true).then(function (ok) {
          if (!ok && termT)
            termT.write('\r\n\x1b[90m[could not restart — click ⌨ twice to reopen]\x1b[0m\r\n');
        });
        return;
      }
      if (termRetry >= 6) {
        termT.write('\r\n\x1b[90m[disconnected — click ⌨ twice to reopen]\x1b[0m\r\n');
        return;
      }
      var wait = Math.min(15000, 1000 * Math.pow(2, termRetry));
      termRetry += 1;
      termT.write('\r\n\x1b[90m[connection lost — reconnecting in ' +
                  Math.round(wait / 1000) + 's (' + termRetry + '/6)]\x1b[0m\r\n');
      setTimeout(function () {
        if (!termClosing && termOn && termT && termKey === key) connectWS(key);
      }, wait);
    };
    termT.onData(function (s) { if (ws.readyState === 1) ws.send('0' + s); });
    termT.onResize(function (sz) {
      if (ws.readyState === 1) ws.send('1' + JSON.stringify({ columns: sz.cols, rows: sz.rows }));
    });
  }
  async function mountTerm(key) {
    await loadXterm();
    disposeTerm();
    var host = chat.querySelector('.tm');
    termT = new window.Terminal({
      // unicode11 addon 用的是 xterm 的 proposed API：不开这个开关，loadAddon
      // 直接 throw，被 termOpen 的 catch 吞成 3 秒 toast —— 面板就是纯黑
      //（JL 260731 的黑屏主因；netlog/探针一路排查到 toast 才现形）。
      allowProposedApi: true,
      // CJK fallbacks + lineHeight headroom: Menlo has no 汉字, the browser falls
      // back to a taller proportional font whose glyphs overflow the measured row
      // and bleed into the next line — the vertical smear in JL's QD3 screenshot.
      fontSize: 13, lineHeight: 1.2,
      fontFamily: 'Menlo, "SF Mono", ui-monospace, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", monospace',
      cursorBlink: true, convertEol: false, scrollback: 4000,
      theme: { background: '#0b0d12', foreground: '#e8e8e6', cursor: '#6ea8f0' }
    });
    if (window.Unicode11Addon) {           // match claude's wcwidth (see loadXterm)
      termT.loadAddon(new window.Unicode11Addon.Unicode11Addon());
      termT.unicode.activeVersion = '11';
    }
    /* Shift+Enter = 换行不发送（JL 260731「shift+enter 直接把消息发出去了」）：
       裸终端里 Shift+Enter 和 Enter 都是 \r，claude 分不出来。两个候选序列
       实测（260731，走 WS 打真字节看屏）：ESC+CR 会直接提交；反斜杠+CR 才是
       claude 原生的「续行」——插一行，不发送。所以 Shift+Enter 改发 \ + CR。 */
    termT.attachCustomKeyEventHandler(function (e) {
      if (e.type === 'keydown' && e.key === 'Enter' && e.shiftKey) {
        if (termWS && termWS.readyState === 1) termWS.send('0\\\r');
        return false;                      // 拦住 xterm 自己的 \r，不然还是发送
      }
      return true;
    });
    termT.open(host);
    try { window.__boardTerm = termT; } catch (e) {}   // debug handle, inspect from the console
    fitTerm();
    termClosing = false; termKey = key; termRetry = 0;
    connectWS(key);
    setTimeout(function () { termT && termT.focus(); }, 50);
  }
  window.addEventListener('resize', function () { if (termOn) fitTerm(); });
  // fit when the drawer pane itself changes size, not only the window (debounced)
  (function () {
    var host = chat.querySelector('.tm'), t = null;
    if (window.ResizeObserver && host)
      new ResizeObserver(function () {
        clearTimeout(t); t = setTimeout(function () { if (termOn) fitTerm(); }, 150);
      }).observe(host);
  })();
  /* 贴图进真终端（QD3m M4，260731）：图在 JL 笔记本的剪贴板里，claude 在服务器上，
     所以浏览器把 blob 摆渡给 serve.py（/_board/image → 板子的 fig/），再把
     repo 根相对路径打进 PTY —— claude 用 Read 工具看图。纯文字粘贴不拦，xterm 自己管。 */
  chat.querySelector('.tm').addEventListener('paste', function (e) {
    if (!termOn || !cq || !termWS || termWS.readyState !== 1) return;
    var items = (e.clipboardData && e.clipboardData.items) || [];
    var it = null;
    for (var i = 0; i < items.length; i++) {
      if (items[i].kind === 'file' && /^image\//.test(items[i].type)) { it = items[i]; break; }
    }
    if (!it) return;
    e.preventDefault(); e.stopPropagation();
    var blob = it.getAsFile();
    var fr = new FileReader();
    fr.onload = async function () {
      var j = null;
      try {
        j = await post('/_board/image',
          { file: cq.file, name: (blob && blob.name) || 'paste', data: fr.result });
      } catch (err) { j = null; }
      if (j && j.ok && termWS && termWS.readyState === 1) {
        var dir = boardDirPath().replace(/^\//, '');
        termWS.send('0' + (dir ? dir + '/' : '') + j.rel);
      } else {
        say((j && j.err) || 'image upload failed (is serve.py running?)');
      }
    };
    fr.readAsDataURL(blob);
  }, true);

  async function termRelease(file, g) {
    disposeTerm();
    if (!file) return;
    try {
      /* park:true（QD3 ⑤，260731）：进程原地停靠 10 分钟，再点 ⌨ 秒接同一屏。
         真正的杀留给 killall 和过期清扫 —— reload / 切回抽屉不再杀终端。 */
      await fetch('/_board/release', { method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: boardPath(), file: file, park: true,
                               group: g || undefined }) });
    } catch (e) { /* 服务器没了也要让界面回得来 */ }
  }
  /* 关整个板页面时（含 reload！），开着的终端停靠而不是被杀 ——
     「板一刷新终端就没了」的元凶就是这个 beacon 原来直接杀（JL 260731）。 */
  window.addEventListener('pagehide', function () {
    if (termOn && cq && cq.file && navigator.sendBeacon) {
      navigator.sendBeacon('/_board/release',
        new Blob([JSON.stringify({ path: boardPath(), file: cq.file, park: true,
                                   group: cq.group || undefined })],
                 { type: 'application/json' }));
    }
  });
  async function termOpen(quiet) {
    if (!cq) return false;
    if (!quiet) say('Starting a terminal for this question…');
    try {
      var r = await fetch('/_board/term', { method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: boardPath(), file: cq.file,
                               group: (cq && cq.group) || undefined,
                               session: chatSid, name: sessName }) });
      var j = await r.json();
      if (!j.ok) { say('⚠ ' + j.err); return false; }
      // 拣选的那段（或新开的）从这一刻起就是 current —— 状态归位、清单重拉
      if (chatSid) { chatSid = ''; sessName = ''; loadSessions(); }
      termView(true);
      await mountTerm(j.key);
      if (!quiet) say(j.reused ? 'Reattached to the terminal already running'
                               : (j.note || 'Terminal ready'));
      return true;
    } catch (e) { say('⚠ ' + e.message); return false; }
  }
  // pre-warm on hover: pull the 480KB xterm.js while the pointer is still on ⌨,
  // so the click feels instant. Assets only — never POST /_board/term here (it takes HOLD).
  chat.querySelector('.term').addEventListener('mouseenter', function () {
    loadXterm().catch(function () {});
  });
  /* The PTY is a real process on the server and a page reload PARKS it rather
     than killing it, so coming back to a page whose terminal is still running
     and being shown the chat box is the view lying about the state (JL 260801:
     "when I come back it became the GUI again, in truth the TUI is running").
     The reload-restore block at the end of board.js needs to see and redo this,
     and it lives outside this closure. */
  window.__boardTermOn = function () { return !!termOn; };
  window.__boardTermReopen = async function () {
    if (!cq || termOn) return false;
    /* only reattach to a terminal that is genuinely still there; starting a new
       one on a reload would spawn a process nobody asked for */
    try {
      var r = await fetch('/_board/term-probe', { method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: boardPath(), file: cq.file,
                               group: (cq && cq.group) || undefined }) });
      var j = await r.json();
      if (!j || !j.live) return false;
    } catch (e) { return false; }
    return await termOpen(true);
  };

  chat.querySelector('.term').onclick = async function () {
    if (!cq) return;
    if (termOn) {                                  // 切回抽屉 = 交回 session
      await termRelease(cq.file, cq.group);
      termView(false);
      say('Terminal closed, session handed back');
      return;
    }
    await termOpen(false);
  };
