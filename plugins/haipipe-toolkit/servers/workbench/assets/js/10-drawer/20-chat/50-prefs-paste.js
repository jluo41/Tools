  /* A Labeling HOLD is visible in the iframe URL, but the server independently
     re-derives it from canonical artifacts. This flag only makes the UI honest. */
  var labelingHold = new URLSearchParams(location.search).get('labeling_hold') === '1';

  /* 模型 / effort / 权限档 记在本机；default Opus 5 · high · full·ask */
  (function () {
    var m = chat.querySelector('.mdl'), e = chat.querySelector('.eff'),
        s = chat.querySelector('.scope');
    m.value = localStorage.getItem(MK) || 'opus';
    e.value = localStorage.getItem(EK) || 'high';
    /* DEFAULT: Full · no ask (JL 260802 ruled it). The board's chat is a tool
       you drive on your own machine, on your own files, and a prompt before
       every edit is a click you make hundreds of times a day to answer "yes"
       every time. `scoped` stays for a session you want fenced to one page, and
       `full` for CLI-style per-call prompts. A choice already made is
       remembered, so this only changes what a NEW browser starts with. */
    s.value = localStorage.getItem(SK) || 'bypass';
    if (labelingHold) {
      s.value = 'scoped';
      s.disabled = true;
      s.title = 'Labeling HOLD: read-only consultation, enforced again by the server';
    }
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
