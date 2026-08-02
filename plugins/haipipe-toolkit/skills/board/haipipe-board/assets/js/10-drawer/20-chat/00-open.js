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
    '<div class="utility"><div class="utility-tabs">' +
    /* Sessions belongs beside the other two, not in a separate strip under the
       header (JL 260801: "我怎么能加一个新的 button，叫 Sessions"). The picker
       element itself is UNMOVED in every other sense: same .spick / .spl
       selectors, so loadSessions and renderSessions need no change.
       ORDER, left to right (JL 260802): which conversation, then what to say in
       it, then how it is configured — widest scope first, and Settings last
       because it is the one you touch least. */
    '<button class="gtoggle" type="button" aria-expanded="false">🗂 Sessions</button>' +
    '<button class="utoggle" type="button" aria-expanded="false">✨ Quick actions</button>' +
    '<button class="stoggle" type="button" aria-expanded="false">⚙ Settings</button></div>' +
    '<div class="utility-body"><div class="acts"></div>' +
    '<div class="sessions"><details class="spick" hidden open>'+
    '<summary></summary><div class="spl"></div></details></div>' +
    '<div class="settings"><div class="tip"></div>' +
    '<div class="cfg">' +
    '<select class="mdl"><option value="opus">Opus 5</option>' +
    '<option value="opus48">Opus 4.8</option>' +
    '<option value="sonnet">Sonnet 5</option><option value="haiku">Haiku 4.5</option></select>' +
    '<select class="eff"><option>low</option><option>medium</option>' +
    '<option selected>high</option><option>xhigh</option><option>max</option></select>' +
    '<select class="scope" title="Permission tier: Scoped = this question only · Full = all tools + skills, like the CLI">' +
    '<option value="scoped">Scoped</option>' +
    '<option value="full" selected>Full · ask</option>' +
    '<option value="bypass">Full · no ask</option></select>' +
    '<span class="cost"></span></div>' +
    '<div class="sid"></div></div></div></div>' +
    '<div class="ft"><textarea rows="1" placeholder="Ask about this question…"></textarea>' +
    '<button class="send">➤</button></div>';
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
  var UTABS = [['actions', 'show-actions', utilityToggle],
               ['sessions', 'show-sessions', sessionsToggle],
               ['settings', 'show-settings', settingsToggle]];
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
  }
  UTABS.forEach(function (t) {
    t[2].onclick = function () {
      setUtility(utility.classList.contains(t[1]) ? '' : t[0]);
    };
  });
