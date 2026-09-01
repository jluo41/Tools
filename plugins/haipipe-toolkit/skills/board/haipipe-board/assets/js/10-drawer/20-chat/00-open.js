  /* ── 每题一个对话窗（QD1）──────────────────────────────────
     打开它 = 在服务器上起一个 claude_agent_sdk 会话，作用域锁死在这一题：
     只能读这个板文件夹，只能改这一个 Q 文件（服务器端 can_use_tool 把关）。
     session id 由服务器写回 Q 文件头部的 `session:`，所以关掉再开还接得上。 */
  var chat = document.createElement('div');
  chat.id = 'chat';
  chat.innerHTML =
    '<div class="rz" title="Drag to resize"></div>' +
    '<div class="hd"><span class="qid"></span><span class="ti"></span>' +
    /* 🖼 lives in the HEADER, not beside the composer, because the header is the
       one strip that survives termView(): the composer `.ft` is hidden while the
       terminal is showing, and the terminal is exactly where a phone reader wants
       to hand claude a screenshot (QD14, JL 260801: "手机上的话，如何 upload 这个
       image 呢?"). One button, both halves; it decides where the path goes. */
    '<button class="imgpick" type="button" aria-label="Attach an image" title="Attach an image from this device (photo library or camera) — paste needs a desktop clipboard">🖼</button>' +
    '<button class="term" type="button" aria-label="Open terminal" title="Open this question in a real terminal (same session)">&gt;_</button>' +
    /* Below 820px the drawer stops docking and covers the page entirely, and
       #chatfab hides while it is open, so a 32px × was the only way back and it
       reads as "close the chat", not "return to the page" (JL 260801: "这好像
       没有 button 让我去重新打开 page"). A labelled button says where it goes;
       nothing is lost by pressing it, because the session lives on disk. */
    '<button class="back" type="button" aria-label="Back to the page" title="Back to the page — this session is kept and resumes when you reopen">⇤ Page</button>' +
    '<button class="x" type="button" aria-label="Close chat" title="Close chat">×</button></div>' +
    '<div class="sfocus" hidden><div class="sfrow"><span class="sflabel">FOCUS</span>' +
    '<code class="sfref"></code><button class="sfclear" type="button" aria-label="Clear sentence focus" title="Clear sentence focus">×</button></div>' +
    '<div class="sfpath"></div><div class="sfquote"></div>' +
    '<details class="sfattached"><summary></summary><pre></pre></details></div>' +
    '<div class="bd"></div><div class="tm"></div>' +
    /* THE COMPOSER CARD (JL 260831, from the Claude Code composer he showed):
       one rounded box — the textarea on top, a control ROW under it: ＋ new
       chat · 🗂 sessions · ✨ quick actions · ⚙ settings · 🖌 draw fold on
       the left, ➤ send on the right. The three toggles open POPUP menus
       floating above the composer instead of expanding the pane, and nothing
       opens by itself (reverses the 260815 "list first" boot ruling — JL
       260831: "make the sessions hidden ... it will show a list of menu").
       Same .gtoggle/.utoggle/.stoggle classes, so setUtility is unchanged. */
    '<div class="utility"><div class="utility-body"><div class="acts"></div>' +
    /* 🖌 the draw menu (JL 260831: the shell's ✨ drawbar retired — "I want
       it to be in the input box"): Draw-it reads the COMPOSER text as the
       ask, the fold row is the studio's hide/show. */
    '<div class="drawmenu">' +
    '<button class="dact draw-go" type="button">✨ Draw it — uses the text in the box · empty = this page&#39;s ## Diagram</button>' +
    '<button class="dact draw-fold" type="button">🖌 Hide the drawing</button>' +
    '</div>' +
    '<div class="sessions"><details class="spick" hidden open>'+
    '<summary></summary><div class="spl"></div></details></div>' +
    '<div class="settings"><div class="tip"></div>' +
    '<div class="cfg">' +
    '<select class="mdl"><option value="opus">Opus 5</option>' +
    '<option value="opus48">Opus 4.8</option>' +
    '<option value="sonnet">Sonnet 5</option><option value="haiku">Haiku 4.5</option></select>' +
    '<select class="eff"><option>low</option><option>medium</option>' +
    '<option selected>high</option><option>xhigh</option><option>max</option></select>' +
    '<select class="fsz" title="chat text size — JL 260831: windows differ in width and zoom, so the size is yours to set">' +
    '<option value="10.5">Aa 10.5</option><option value="11.5" selected>Aa 11.5</option>' +
    '<option value="12.5">Aa 12.5</option><option value="14">Aa 14</option>' +
    '<option value="16">Aa 16</option></select>' +
    '<select class="scope" title="Permission tier: Scoped = this question only · Full = all tools + skills, like the CLI">' +
    '<option value="scoped">Scoped</option>' +
    '<option value="full" selected>Full · ask</option>' +
    '<option value="bypass">Full · no ask</option></select>' +
    '<span class="cost"></span></div>' +
    '<div class="sid"></div></div></div></div>' +
    '<div class="ft"><div class="composer">' +
    '<textarea rows="1" placeholder="Ask about this question…"></textarea>' +
    '<div class="crow">' +
    '<button class="gnew" type="button" title="new chat — starts fresh, primed with this page">＋</button>' +
    '<button class="gtoggle" type="button" aria-expanded="false" title="sessions">🗂</button>' +
    '<button class="utoggle" type="button" aria-expanded="false" title="quick actions">✨</button>' +
    '<button class="stoggle" type="button" aria-expanded="false" title="settings">⚙</button>' +
    '<button class="dtoggle" type="button" title="show / hide the drawing above">🖌</button>' +
    '<button class="mtoggle" type="button" title="open this chat in the real terminal (same session) — the ← in the header returns">⌨ TUI</button>' +
    '<button class="send" title="send">➤</button>' +
    '</div></div></div>';
  document.body.appendChild(chat);
  /* The drawer is position:fixed OVER the page, so a wheel with nothing to
     scroll inside it chains to the document and the PAGE moves instead — and
     an empty-ish transcript is exactly the case with nothing to scroll, which
     is why it only felt fixed after sending a message (JL 260801: "感觉还是
     背后的那个 page 页面在滑动 ... 只有发一个 message 之后才能够滑动").
     overscroll-behavior alone cannot help here: it governs a scroller that has
     reached its edge, not one that never had overflow. So ask the real
     question — can anything under the pointer take this delta? — and if the
     answer is no, keep the event rather than hand it to the page. */
  chat.addEventListener('wheel', function (ev) {
    var dy = ev.deltaY;
    if (!dy) return;
    for (var n = ev.target; n && n !== chat; n = n.parentNode) {
      if (!n.scrollHeight || n.scrollHeight - n.clientHeight <= 1) continue;
      var oy = getComputedStyle(n).overflowY;
      if (oy !== 'auto' && oy !== 'scroll') continue;
      var room = dy > 0 ? (n.scrollHeight - n.scrollTop - n.clientHeight) : n.scrollTop;
      if (room > 1) return;                  /* this one can take it: let it */
    }
    ev.preventDefault();                     /* nothing can: do not move the page */
  }, { passive: false });
  var cq = null;                                    // 当前挂在哪一题
  var sentenceFocus = null;
  var MK = 'board-chat-model', EK = 'board-chat-effort', SK = 'board-chat-scope';
  var CHATK = function (id) { return 'board-chat:' + location.pathname + ':' + id; };
  var utility = chat.querySelector('.utility'), utilityToggle = chat.querySelector('.utoggle'),
      settingsToggle = chat.querySelector('.stoggle'),
      sessionsToggle = chat.querySelector('.gtoggle');
  var drawToggle = chat.querySelector('.dtoggle');
  var UTABS = [['actions', 'show-actions', utilityToggle],
               ['sessions', 'show-sessions', sessionsToggle],
               ['settings', 'show-settings', settingsToggle],
               ['draw', 'show-draw', drawToggle]];
  function setUtility(mode) {
    var known = UTABS.filter(function (t) { return t[0] === mode; }).length;
    mode = known ? mode : '';
    utility.classList.toggle('open', !!mode);
    chat.classList.toggle('utility-open', !!mode);
    UTABS.forEach(function (t) {
      var on = mode === t[0];
      utility.classList.toggle(t[1], on);
      t[2].setAttribute('aria-expanded', on ? 'true' : 'false');
      t[2].classList.toggle('active', on);
    });
    /* the picker is a <details> that other code opens and closes on its own;
       inside a tab it should simply be open whenever the tab is */
    if (mode === 'sessions') {
      var sp = chat.querySelector('.spick');
      if (sp) sp.open = true;
      if (typeof loadSessions === 'function') loadSessions();   // refresh on reveal
    }
    if (mode === 'draw') {
      var fr = chat.querySelector('.draw-fold'), shown = true;
      try { shown = !parent || !parent.__studioDrawShown || parent.__studioDrawShown(); }
      catch (e) {}
      fr.textContent = shown ? '🖌 Hide the drawing' : '🖌 Show the drawing';
    }
  }
  UTABS.forEach(function (t) {
    t[2].onclick = function (ev) {
      if (ev) ev.stopPropagation();
      setUtility(utility.classList.contains(t[1]) ? '' : t[0]);
    };
  });
  /* a popup closes on a click anywhere outside it (the Claude Code manner) */
  document.addEventListener('click', function (ev) {
    if (!utility.classList.contains('open')) return;
    for (var n = ev.target; n; n = n.parentNode) {
      if (n === utility) return;
      if (n.classList && n.classList.contains('crow')) return;
    }
    setUtility('');
  });
  /* ＋ new chat: one press, no menu — the session registry names it later */
  chat.querySelector('.gnew').onclick = function () {
    setUtility('');
    if (window.__chatNewSession) window.__chatNewSession('');
  };
  /* one small toast pill for the draw menu's progress words */
  function drawNote(msg) {
    var t = chat.querySelector('.lrf.draw');
    if (!t) {
      t = document.createElement('div');
      t.className = 'lrf draw';
      chat.appendChild(t);
    }
    t.textContent = msg;
    clearTimeout(t._bye);
    if (/^(✅|✋)/.test(msg)) t._bye = setTimeout(function () { t.remove(); }, 6000);
  }
  /* the drawing itself lives in the SHELL (the studio's upper half); the
     menu rows are the composer's remote for it. Outside the shell they say so. */
  chat.querySelector('.draw-go').onclick = function () {
    setUtility('');
    var ta = chat.querySelector('textarea');
    var ask = ta.value.trim();
    try {
      if (parent && parent.__studioDrawIt) {
        parent.__studioDrawIt(ask, drawNote);
        if (ask) ta.value = '';
        return;
      }
    } catch (e) {}
    drawNote('✋ the drawing lives in the board shell — open this page in the split view');
  };
  /* ⤓ open at the NEWEST message EVERY time the pane becomes visible (JL
     260831 "make the GUI chat to the bottom everytime I open it"): the
     replay-time scroll (40-permissions) only covers the first open — a tab
     switch or a return from the terminal reveals the pane mid-transcript.
     Watch visibility itself: on every hidden→shown edge, snap to bottom. */
  (function () {
    var bd = chat.querySelector('.bd');
    var wasVisible = false;
    setInterval(function () {
      var vis = !!bd.offsetParent && bd.clientHeight > 0;
      if (vis && !wasVisible) bd.scrollTop = bd.scrollHeight;
      wasVisible = vis;
    }, 400);
  })();
  /* Aa the chat text size is the reader's (JL 260831 "still large here"):
     one CSS variable, one stored choice, applied at boot. */
  var FSZ = 'board-chat-fsz';
  var fszSel = chat.querySelector('.fsz');
  function applyFsz(v) {
    chat.style.setProperty('--chatfs', v + 'px');
    if (fszSel) fszSel.value = v;
  }
  try { applyFsz(localStorage.getItem(FSZ) || '11.5'); } catch (e) { applyFsz('11.5'); }
  if (fszSel) fszSel.onchange = function () {
    try { localStorage.setItem(FSZ, fszSel.value); } catch (e) {}
    applyFsz(fszSel.value);
  };
  /* ⌨ the GUI/TUI switch moved here from the shell strip (JL 260831).
     One implementation law (QD1): the header's .term button IS the switch,
     this row button only presses it. The composer hides in TUI, so this
     door only ever leads IN; the header's ← leads back. */
  chat.querySelector('.mtoggle').onclick = function () {
    var t = chat.querySelector('.hd .term');
    if (t) t.click();
  };
  chat.querySelector('.draw-fold').onclick = function () {
    setUtility('');
    try { if (parent && parent.__studioToggleDraw) { parent.__studioToggleDraw(); return; } }
    catch (e) {}
    drawNote('✋ the drawing lives in the board shell — open this page in the split view');
  };
