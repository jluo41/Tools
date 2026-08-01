  /* ── 每题一个对话窗（QD1）──────────────────────────────────
     打开它 = 在服务器上起一个 claude_agent_sdk 会话，作用域锁死在这一题：
     只能读这个板文件夹，只能改这一个 Q 文件（服务器端 can_use_tool 把关）。
     session id 由服务器写回 Q 文件头部的 `session:`，所以关掉再开还接得上。 */
  var chat = document.createElement('div');
  chat.id = 'chat';
  chat.innerHTML =
    '<div class="rz" title="Drag to resize"></div>' +
    '<div class="hd"><span class="qid"></span><span class="ti"></span>' +
    '<button class="term" type="button" aria-label="Open terminal" title="Open this question in a real terminal (same session)">&gt;_</button>' +
    '<button class="x" type="button" aria-label="Close chat" title="Close chat">×</button></div>' +
    '<details class="spick" hidden><summary></summary><div class="spl"></div></details>' +
    '<div class="sfocus" hidden><div class="sfrow"><span class="sflabel">FOCUS</span>' +
    '<code class="sfref"></code><button class="sfclear" type="button" aria-label="Clear sentence focus" title="Clear sentence focus">×</button></div>' +
    '<div class="sfpath"></div><div class="sfquote"></div>' +
    '<details class="sfattached"><summary></summary><pre></pre></details></div>' +
    '<div class="bd"></div><div class="tm"></div>' +
    '<div class="utility"><div class="utility-tabs">' +
    '<button class="utoggle" type="button" aria-expanded="false">✨ Quick actions</button>' +
    '<button class="stoggle" type="button" aria-expanded="false">⚙ Settings</button></div>' +
    '<div class="utility-body"><div class="acts"></div>' +
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
  var cq = null;                                    // 当前挂在哪一题
  var sentenceFocus = null;
  var MK = 'board-chat-model', EK = 'board-chat-effort', SK = 'board-chat-scope';
  var CHATK = function (id) { return 'board-chat:' + location.pathname + ':' + id; };
  var utility = chat.querySelector('.utility'), utilityToggle = chat.querySelector('.utoggle'),
      settingsToggle = chat.querySelector('.stoggle');
  function setUtility(mode) {
    mode = mode === 'actions' || mode === 'settings' ? mode : '';
    utility.classList.toggle('open', !!mode);
    utility.classList.toggle('show-actions', mode === 'actions');
    utility.classList.toggle('show-settings', mode === 'settings');
    chat.classList.toggle('utility-open', !!mode);
    utilityToggle.setAttribute('aria-expanded', mode === 'actions' ? 'true' : 'false');
    settingsToggle.setAttribute('aria-expanded', mode === 'settings' ? 'true' : 'false');
    utilityToggle.classList.toggle('active', mode === 'actions');
    settingsToggle.classList.toggle('active', mode === 'settings');
  }
  utilityToggle.onclick = function () {
    setUtility(utility.classList.contains('show-actions') ? '' : 'actions');
  };
  settingsToggle.onclick = function () {
    setUtility(utility.classList.contains('show-settings') ? '' : 'settings');
  };
