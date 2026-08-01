  /* 贴图（JL 260731）：往评论框/讨论框里 Ctrl+V 一张图 → POST /_board/image
     存进这块板的 fig/ → 光标处插一行 ![…](fig/…)，随后的保存把这行当普通
     markdown 落盘。serve.py 没跑时图没法落盘 —— 提示作者自己放进 fig/。 */
  function insertAtCursor(ta, s) {
    var a = ta.selectionStart || 0, b = ta.selectionEnd || 0;
    ta.value = ta.value.slice(0, a) + s + ta.value.slice(b);
    ta.selectionStart = ta.selectionEnd = a + s.length;
    ta.focus();
  }
  function wireImagePaste(ta, fileOf, mk) {
    // mk(rel)：贴进输入框的那行长什么样。默认是板内相对路径的 markdown 图
    //（评论/讨论落进 .md 用）；抽屉聊天传自己的 mk，给 claude 一个 repo 根相对路径。
    ta.addEventListener('paste', function (e) {
      var items = (e.clipboardData && e.clipboardData.items) || [];
      var it = null;
      for (var i = 0; i < items.length; i++) {
        if (items[i].kind === 'file' && /^image\//.test(items[i].type)) { it = items[i]; break; }
      }
      if (!it) return;                          // 纯文字粘贴走浏览器原生
      e.preventDefault();
      var blob = it.getAsFile();
      var fr = new FileReader();
      fr.onload = async function () {
        var j = null;
        try {
          j = await post('/_board/image',
            { file: fileOf(), name: (blob && blob.name) || 'paste', data: fr.result });
        } catch (err) { j = null; }
        if (j && j.ok) insertAtCursor(ta,
          (mk || function (rel) { return '![image](' + rel + ')'; })(j.rel));
        else say((j && j.err) || 'serve.py is not running — put the image into fig/ yourself and write ![…](fig/…)');
      };
      fr.readAsDataURL(blob);
    });
  }
  wireImagePaste(box.querySelector('textarea'), function () { return pend && pend.file; });


  /* One discussion line, rendered exactly as build.py renders it, inserted
     next to the box that wrote it. Mirrors `body.py`'s `<div class="cmt {who}">`
     and `common.py`'s who_class, so the row a reader sees now is byte-for-byte
     what they will see after the next rebuild. */
  function whoClass(who) {
    var base = String(who).replace(/\d+$/, '').toUpperCase();
    if (base === 'JL' || base === 'CC') return base.toLowerCase();
    var s = 0;
    for (var i = 0; i < base.length; i++) s += base.charCodeAt(i);
    return 'u' + (s % 4);
  }
  function appendDiscuss(box, who, text) {
    var row = document.createElement('div');
    row.className = 'cmt ' + whoClass(who) + ' just-landed';
    var b = document.createElement('b'); b.textContent = who;
    row.appendChild(b);
    row.appendChild(document.createTextNode(' ' + text));
    // the empty-state line goes away the moment there is a real line
    var host = box.parentElement;
    var mut = host && host.querySelector('p.mut');
    if (mut) mut.remove();
    if (host) host.insertBefore(row, box);
    setTimeout(function () { row.classList.remove('just-landed'); }, 1200);
  }

  // 讨论框：整段写想法 → POST /_board/discuss → 追加进 ## Discussion → 刷新（JL 260723）
  function wireDadd() {
    var last = localStorage.getItem(WK) || users[0];
    document.querySelectorAll('.dadd').forEach(function (box) {
      var ta = box.querySelector('textarea');
      var sel = box.querySelector('select');
      var btn = box.querySelector('.dsave');
      wireImagePaste(ta, function () { return box.getAttribute('data-file'); });
      users.forEach(function (u) { sel.appendChild(new Option(u, u)); });
      sel.value = last;
      btn.onclick = async function () {
        var text = ta.value.trim();
        if (!text) { ta.focus(); return; }
        btn.disabled = true; btn.textContent = '…';
        var j = null;
        try {
          j = await post('/_board/discuss',
            { file: box.getAttribute('data-file'), who: sel.value, text: text });
        } catch (e) { j = null; }
        btn.disabled = false; btn.textContent = '➕ Add to discussion';
        if (j === null) {
          say('serve.py is not running — write > ' + sel.value + ': … into ## Discussion in the md yourself');
          return;
        }
        if (j.ok) {
          localStorage.setItem(WK, sel.value);
          // Land the line IN PLACE, the way a comment lands anywhere else on the
          // web (JL 260731: "like commenting on Reddit, it just loads in, not
          // the whole page refreshing and jumping"). The server has already
          // written the .md and rebuilt, so this is not optimistic: it is the
          // same row the next build emits, inserted now instead of arriving
          // through a whole-page swap that moves the reader.
          appendDiscuss(box, sel.value, text);
          ta.value = '';
          ta.style.height = '';
        } else say(j.err || 'write failed');
      };
    });
  }
