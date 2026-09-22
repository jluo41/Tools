  // Image paste belongs to the explicit Studio composer.
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

  function wireDadd() {
    // Remove forms from older generated Pages during navigation/live refresh.
    document.querySelectorAll('section.q .dadd,section.q .sadd,section.q .sedit,section.q .saddrow')
      .forEach(function (form) { form.remove(); });
  }
