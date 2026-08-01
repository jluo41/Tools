/* Every write posts `path`, and the server takes that path's PARENT as the
   board folder. In the board/ tree a page lives at
   `<board>/board/<GROUP>/<page>.html`, so the naive pathname makes the server
   look for board.md inside `board/<GROUP>/` and every write silently fails
   (found by driving a real submit, JL 260731). Collapse the tree tail back to
   the board root so both packagings post the same thing.
   Declared at file scope on purpose: SEVEN separate writers call it. */
function boardPath() {
  var p = location.pathname;
  var i = p.lastIndexOf('/board/');
  // Name the board by its SOURCE, `board.md`, not by a generated artifact.
  // This said `board.html` until 260731 and kept working only because the
  // server takes the path's PARENT and never stats the file: once the
  // monolith was retired it pointed at something that no longer exists.
  return (i === -1 ? p.replace(/\/[^/]*$/, '') : p.slice(0, i)) + '/board.md';
}

/* Public path of the editable Board folder, independent of whether the open
   document is the Index, a group, or a focused page. Consumers that need a
   repo-relative path must use this instead of taking location.pathname's
   immediate parent, which is `board/<GROUP>/` on a split page. */
function boardDirPath() {
  return boardPath().replace(/\/board\.md$/, '');
}

/* ─────────────────────────────────────────────────────────────
   Comment layer — PURE ENHANCEMENT. The prose is already real HTML;
   this script only ADDS "select -> comment -> highlight right away".
   Strip this script block and the board still reads fine (just no commenting).

   Comments go straight to the server, which writes each one beneath its
   selected sentence in the source Markdown.
   ───────────────────────────────────────────────────────────── */

(function () {
  var KEY = 'board-comments:' + location.pathname;
  var UK = 'board-users', WK = 'board-user-last';
  var db = [], users = [];
  try { db = JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { db = []; }
  try { users = JSON.parse(localStorage.getItem(UK) || 'null') || ['JL','CC']; }
  catch (e) { users = ['JL','CC']; }
  users = users.filter(function (u) { return u !== 'RA'; });
  if (!users.length) users = ['JL','CC'];
  localStorage.setItem(UK, JSON.stringify(users));
  if (localStorage.getItem(WK) === 'RA') localStorage.removeItem(WK);
  var pend = null;

  function mk(tag, id, html) {
    var e = document.createElement(tag); e.id = id; e.innerHTML = html || ''; return e;
  }
  var btn = mk('button', 'cbtn', '\u{1F4AC} Comment');
  var box = mk('div', 'cbox',
    '<div class="qq"></div><textarea placeholder="Write a comment…"></textarea>' +
    '<div class="row"><select></select><span style="flex:1"></span>' +
    '<button class="cx">Cancel</button><button class="ok cs">Save</button></div>' +
    '<input class="nu" placeholder="New initials, e.g. ZW — press Enter">');
  var dock = mk('button', 'cdock', '');
  var panel = mk('div', 'cpanel', '');
  var toast = mk('div', 'ctoast', '');
  [btn, box, dock, panel, toast].forEach(function (e) { document.body.appendChild(e); });

  function save() { localStorage.setItem(KEY, JSON.stringify(db)); marks(); paint(); }
  function say(m) {
    toast.textContent = m; toast.style.display = 'block';
    clearTimeout(toast._t);
    toast._t = setTimeout(function () { toast.style.display = 'none'; }, 3000);
  }

  /* ── highlighting ────────────────────────────────────────────
     Two paths, because they have different information:
       NEW comment  -> we still hold the live Range. Wrap THAT. Always exact,
                       even when the selection crosses <code>/<b> boundaries.
       ON RELOAD    -> the Range is gone, so find the quote by text. Search the
                       section's whole text (concatenated across nodes) with a
                       whitespace-tolerant regex, then map the hit back to
                       (node, offset) so the wrap can span several nodes.
     The old version only did indexOf() inside ONE text node — which is why a
     selection crossing any inline tag silently failed to highlight.          */
  function clearMarks() {
    document.querySelectorAll('span.cmk').forEach(function (e) { e.remove(); });
    document.querySelectorAll('mark.pend').forEach(function (m) {
      var par = m.parentNode;
      while (m.firstChild) par.insertBefore(m.firstChild, m);
      par.removeChild(m); par.normalize();
    });
  }
  function badge(mark, idx) {
    var s = document.createElement('span');
    s.className = 'cmk'; s.textContent = '\u{1F4AC}';
    s.setAttribute('data-i', idx);
    s.title = db[idx].who + ': ' + db[idx].text;
    mark.parentNode.insertBefore(s, mark.nextSibling);
  }
  function wrapRange(r, idx) {
    var m = document.createElement('mark');
    m.className = 'pend'; m.setAttribute('data-i', idx);
    try { r.surroundContents(m); }
    catch (e) { m.appendChild(r.extractContents()); r.insertNode(m); }
    if (!m.parentNode) return false;
    badge(m, idx);
    return true;
  }
  // One entry per TEXT NODE, not per character. The per-character version
  // allocated a two-element array for every character in the section, so a
  // 500k-character board with 84 comments built tens of millions of arrays at
  // load and the tab never painted. Index by node, look up by binary search.
  function scan(sec) {
    var w = document.createTreeWalker(sec, NodeFilter.SHOW_TEXT, null);
    var n, parts = [], nodes = [], at = 0;
    while ((n = w.nextNode())) {
      var p = n.parentNode;
      // .folds text is scannable (JL 260731: fold prose takes comments), so a
      // fold sentence's highlight anchors like any other.
      if (p.closest && p.closest('.qh, .nav, pre')) continue;
      var v = n.nodeValue;
      if (!v.length) continue;
      nodes.push([n, at, v.length]);            // node, start in s, length
      parts.push(v);
      at += v.length;
    }
    return { s: parts.join(''), nodes: nodes };
  }
  // string index -> [textNode, offsetInNode]
  function locate(t, i) {
    var lo = 0, hi = t.nodes.length - 1;
    while (lo <= hi) {
      var mid = (lo + hi) >> 1, e = t.nodes[mid];
      if (i < e[1]) hi = mid - 1;
      else if (i >= e[1] + e[2]) lo = mid + 1;
      else return [e[0], i - e[1]];
    }
    return null;
  }
  function rx(q) {
    var parts = q.trim().split(/\s+/).map(function (x) {
      return x.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    });
    return new RegExp(parts.join('[\\s]*'));
  }
  function findAndWrap(sec, quote, idx) {
    var t = scan(sec);
    if (!t.s) return false;
    var m = rx(quote).exec(t.s);
    if (!m) {                                   // last resort: first 12 chars
      var head = quote.trim().slice(0, 12);
      if (head.length < 4) return false;
      m = rx(head).exec(t.s);
      if (!m) return false;
    }
    var a = locate(t, m.index), b = locate(t, m.index + m[0].length - 1);
    if (!a || !b) return false;
    var r = document.createRange();
    r.setStart(a[0], a[1]); r.setEnd(b[0], b[1] + 1);
    return wrapRange(r, idx);
  }
  function marks() {
    clearMarks();
    db.forEach(function (c, i) {
      var sec = document.getElementById(c.id);
      c.lost = !(sec && findAndWrap(sec, c.quote, i));
    });
    document.querySelectorAll('span.cmk').forEach(function (s) {
      s.onclick = function () {
        panel.style.display = 'block'; flash(+s.getAttribute('data-i'));
      };
    });
  }
  function flash(i) {
    var el = panel.querySelector('[data-row="' + i + '"]');
    if (!el) return;
    el.scrollIntoView({ block: 'nearest' });
    el.style.background = 'rgba(255,214,0,.28)';
    setTimeout(function () { el.style.background = ''; }, 1300);
  }

  function containingSentence(r) {
    function paragraph(n) {
      n = n && (n.nodeType === 1 ? n : n.parentElement);
      return n && n.closest && n.closest('p');
    }
    var a = paragraph(r.startContainer), b = paragraph(r.endContainer);
    // fold PROSE is a sentence like any other (JL 260731); what stays excluded
    // is rendered apparatus/comments, which serve.py refuses to anchor on anyway.
    if (!a || a !== b || a.closest('.sapp,.cmb,.cmt,.change')) return '';
    return a.textContent.replace(/\s+/g, ' ').trim();
  }

  /* ── select -> floating button ───────────────────────────── */
  document.addEventListener('mouseup', function (ev) {
    if (box.contains(ev.target) || panel.contains(ev.target) || ev.target === btn) return;
    setTimeout(function () {
      var s = window.getSelection();
      var txt = s && String(s).trim();
      if (!txt || txt.length < 2 || !s.rangeCount) { btn.style.display = 'none'; return; }
      var node = s.anchorNode;
      node = node.nodeType === 1 ? node : node.parentNode;
      var q = node.closest && node.closest('section.q');
      if (!q) { btn.style.display = 'none'; return; }
      var live = s.getRangeAt(0);
      var sentence = containingSentence(live);
      if (!sentence) { btn.style.display = 'none'; return; }
      var r = live.getBoundingClientRect();
      pend = { id: q.id, file: q.getAttribute('data-file') || '',
               quote: txt, sentence: sentence, range: live.cloneRange() };
      btn.style.left = (r.left + window.scrollX) + 'px';
      btn.style.top = (r.bottom + window.scrollY + 7) + 'px';
      btn.style.display = 'block';
    }, 0);
  });

  function fillWho() {
    var sel = box.querySelector('select'), last = localStorage.getItem(WK) || users[0];
    sel.innerHTML = users.map(function (u) {
      return '<option' + (u === last ? ' selected' : '') + '>' + u + '</option>';
    }).join('') + '<option value="__new">+ new person…</option>';
    sel.onchange = function () {
      var nu = box.querySelector('.nu');
      if (sel.value === '__new') { nu.style.display = 'block'; nu.value = ''; nu.focus(); }
      else { nu.style.display = 'none'; localStorage.setItem(WK, sel.value); }
    };
  }
  box.querySelector('.nu').onkeydown = function (ev) {
    if (ev.key !== 'Enter') return;
    ev.preventDefault();
    var v = this.value.trim().toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 4);
    if (!v) return;
    if (users.indexOf(v) < 0) users.push(v);
    localStorage.setItem(UK, JSON.stringify(users));
    localStorage.setItem(WK, v);
    this.style.display = 'none'; fillWho();
  };

  btn.onclick = function () {
    btn.style.display = 'none';
    fillWho(); box.querySelector('.nu').style.display = 'none';
    box.querySelector('.qq').textContent = pend.quote;
    box.querySelector('textarea').value = '';
    box.style.left = btn.style.left; box.style.top = btn.style.top;
    box.style.display = 'block';
    box.querySelector('textarea').focus();
  };
  box.querySelector('.cx').onclick = function () { box.style.display = 'none'; };
  box.querySelector('.cs').onclick = function () {
    var v = box.querySelector('textarea').value.trim();
    if (!v) return;
    var who = box.querySelector('select').value;
    if (who === '__new') who = users[0];
    localStorage.setItem(WK, who);
    var live = pend.range;
    db.push({ id: pend.id, file: pend.file, quote: pend.quote, sentence: pend.sentence,
              who: who, text: v });
    var idx = db.length - 1;
    box.style.display = 'none';
    /* wrap the live range FIRST — guaranteed exact, no text search involved */
    var ok = false;
    try { ok = wrapRange(live, idx); } catch (e) { ok = false; }
    window.getSelection().removeAllRanges();
    db[idx].lost = !ok;
    localStorage.setItem(KEY, JSON.stringify(db));
    if (!ok) marks();
    paint();
    /* 这一次点击本身就是用户手势 —— 直接写盘，不用再点 Sync */
    drain(true).then(function (n) {
      if (n) say((ok ? 'Highlighted and ' : 'Saved (not anchored) and ') +
                 'written to ' + pend.file + (srvOK ? ' — reload to see it rendered'
                                                    : ' — rebuild to render it'));
      else say(ok ? 'Highlighted — ' + db.length + ' pending (no folder access yet)'
                  : 'Saved, but could not anchor it (see ⚠ in the panel)');
    });
  };

  /* ── panel ──────────────────────────────────────────────── */
  function esc(s) { return s.replace(/[&<>]/g, function (c) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]; }); }
  function stamp() {
    var d = new Date(), z = function (n) { return (n < 10 ? '0' : '') + n; };
    return String(d.getFullYear()).slice(2) + z(d.getMonth() + 1) + z(d.getDate()) +
           ' ' + z(d.getHours()) + z(d.getMinutes());
  }
  /* One sentence-local comment; this is also the manual fallback patch. */
  function line(c) {
    return c.sentence + '\n> ' + c.who + ': ' + c.text.replace(/\n/g, ' ') +
           ' · ' + (c.when || stamp());
  }
  function patch() {
    var by = {};
    db.forEach(function (c) { (by[c.file] = by[c.file] || []).push(line(c)); });
    return Object.keys(by).map(function (f) {
      return '### ' + f + '\n' + by[f].join('\n');
    }).join('\n\n');
  }
  function paint() {
    // 这个角标只在「真有没写盘的评论」时才出现（JL 260723）。
    // serve.py 跑着的时候 Save 直接落盘，pending 永远是 0 —— 那就不该在右下角常驻碍眼。
    // 它仍是 serve.py 没跑时的兜底入口，所以不是删掉，是平时藏起来。
    dock.style.display = db.length ? 'block' : 'none';
    dock.textContent = db.length ? ('\u{1F4AC} ' + db.length + ' pending')
                                 : '\u{1F4AC} Comment';
    dock.className = db.length ? 'has' : '';
    panel.innerHTML =
      '<div class="hd"><b>Pending comments</b><span style="flex:1"></span>' +
      '<button class="ok sy">Write now</button>' +
      '<button class="cp">Copy</button></div>' +
      (db.length ? db.map(function (c, i) {
        return '<div class="it" data-row="' + i + '"><div class="q">' + c.id +
          (c.lost ? ' <span style="color:var(--mut)">· unanchored</span> ' : ' ') +
          '“' + esc(c.sentence.slice(0, 40)) + '”</div><b>' + c.who + '</b> ' +
          esc(c.text) + ' <button data-i="' + i +
          '" class="rm" style="padding:2px 8px">del</button></div>';
      }).join('') : '<div class="it mut">Nothing yet. Select a sentence in the text.</div>') +
      '<div class="hint">Comments are written to the <code>.md</code> by the Board server. ' +
      'Anything listed above has NOT been written yet; use Copy to retain a patch. ' +
      'each comment directly below its selected sentence as ' +
      '<code>&gt; WHO: comment · time</code>. ' +
      'Re-run <code>python3 build.py</code> afterwards.</div>';
    panel.querySelectorAll('.rm').forEach(function (b) {
      b.onclick = function () { db.splice(+b.getAttribute('data-i'), 1); save(); };
    });
    panel.querySelector('.sy').onclick = sync;
    panel.querySelector('.cp').onclick = function () {
      navigator.clipboard.writeText(patch()).then(function () { say('Patch copied'); });
    };
  }
  dock.onclick = function () {
    panel.style.display = panel.style.display === 'block' ? 'none' : 'block';
  };

  /* ── 写盘：优先让服务器写 ───────────────────────────────────
     板文件在服务器上，浏览器在你自己的机器上（Remote-SSH）——
     File System Access 的文件夹选择器只看得到你本机的盘，够不着这些文件。
     所以第一选择是发个 POST 让服务器写（serve.py），它写完顺手重新生成 html。
     只有服务器不支持时，才退回浏览器直接写文件 / 复制补丁。          */
  var srvOK = null;                       // null=没试过, true/false=试过
  async function post(url, payload) {
    payload.path = boardPath();
    var r = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' },
                               body: JSON.stringify(payload) });
    if (r.status === 404 || r.status === 501) { srvOK = false; return null; }
    srvOK = true;
    return await r.json();
  }
  async function srvComment(c) {
    try {
      var j = await post('/_board/comment',
        { file: c.file, who: c.who, sentence: c.sentence, text: c.text,
          when: c.when || stamp() });
      if (!j) return null;
      return j.ok ? true : j.err;
    } catch (e) { srvOK = false; return null; }
  }
  /* ── 兜底：浏览器自己写文件（只在服务器不支持时才用到）
     文件夹句柄记在 IndexedDB 里，授权一次，之后每次保存直接写盘 ──
     浏览器规定：第一次挑文件夹必须由用户点击触发，无法自动。
     但句柄可以存下来；之后每次「Save」本身就是一次点击，够格再申请权限，
     所以正常情况下你一个 session 只会看到一次 Allow。                */
  function idb(fn) {
    return new Promise(function (res) {
      var r = indexedDB.open('board-fs', 1);
      r.onupgradeneeded = function () { r.result.createObjectStore('h'); };
      r.onsuccess = function () {
        var db = r.result, tx = db.transaction('h', 'readwrite');
        fn(tx.objectStore('h'), res);
      };
      r.onerror = function () { res(null); };
    });
  }
  function getDir() { return idb(function (s, res) {
    var g = s.get('dir'); g.onsuccess = function () { res(g.result || null); }; }); }
  function putDir(h) { return idb(function (s, res) { s.put(h, 'dir'); res(1); }); }

  var dirH = null;
  async function ensureDir(ask) {
    if (!window.showDirectoryPicker) return null;
    if (!dirH) dirH = await getDir();
    if (dirH) {
      var st = await dirH.queryPermission({ mode: 'readwrite' });
      if (st === 'granted') return dirH;
      if (ask) {
        st = await dirH.requestPermission({ mode: 'readwrite' });
        if (st === 'granted') return dirH;
      }
      return null;
    }
    if (!ask) return null;
    try {
      dirH = await window.showDirectoryPicker({ mode: 'readwrite' });
      await putDir(dirH);
      return dirH;
    } catch (e) { return null; }
  }

  async function edit(dir, file, fn) {
    var fh = await dir.getFileHandle(file);
    var txt = await (await fh.getFile()).text();
    var next = fn(txt);
    if (next === txt) return false;
    var w = await fh.createWritable();
    await w.write(next); await w.close();
    return true;
  }
  /* 把已经写盘的从待办里剔掉；写不进去的留着，面板里还看得见 */
  async function drain(ask) {
    if (!db.length) return 0;
    if (srvOK !== false) {                       // 先试服务器
      var n = 0, err = null;
      for (var i = 0; i < db.length; i++) {
        var r = await srvComment(db[i]);
        if (r === true) { db[i].written = 1; n++; }
        else if (typeof r === 'string') { err = r; }
        else break;                              // null = 服务器不支持，退出去走老路
      }
      if (n || srvOK) {
        db = db.filter(function (c) { return !c.written; });
        localStorage.setItem(KEY, JSON.stringify(db));
        paint();
        if (err) say(err);
        if (srvOK) return n;
      }
    }
    return 0;
  }

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

  /* ➕ Excalidraw (QD7, JL 260726): attach a canvas to a 🖼 Diagram from the page.
     Save posts the URL, serve.py writes it as its own line inside ## Diagram, and the
     canvas comes back through build.py like any other body content. Script-only, as
     every write affordance is: with scripts stripped the figure and its link still read. */
  function wireXcal() {
    /* Walk PAGES, not Diagram sections (QD7, JL 260726). The control used to be
       generated inside `details.diagram-section`, so exactly the pages with no
       figure  — the ones that most need a way in — had no button at all. The
       endpoint could always create the section; only the entry point was
       missing. */
    document.querySelectorAll('section.slide.q[data-file]').forEach(function (page) {
      var sec = page.querySelector('details.diagram-section');
      // the attach control belongs in the ✏️ Excalidraw subsection (QA4, JL
      // 260726); older single-body diagrams fall back to .dia itself.
      var host = sec && (sec.querySelector('.dsub-x > .dsubb') || sec.querySelector('.dia'));
      if (sec && !host) return;
      if ((host || page).querySelector('.xadd')) return;
      var has = !!(sec && sec.querySelector('.xcal'));
      var box = document.createElement('div');
      box.className = 'xadd' + (host ? '' : ' xadd-bare');
      var open = document.createElement('button');
      open.type = 'button';
      open.className = 'xadd-open';
      open.textContent = host ? '🖌 Excalidraw Canvas' : '🖼 Add a Diagram';
      var row = document.createElement('div');
      row.className = 'xadd-row';
      row.hidden = true;
      var inp = document.createElement('input');
      inp.type = 'text';
      inp.placeholder = 'https://app.excalidraw.com/s/…';
      var ok = document.createElement('button'); ok.type = 'button'; ok.textContent = 'Save';
      // ✨ mint one instead of going to make it yourself. serve.py creates the
      // scene through the Excalidraw+ API and writes the link back, so the paste
      // field is for a drawing that already exists, not a chore.
      var mk = document.createElement('button'); mk.type = 'button';
      mk.className = 'xnew'; mk.textContent = '✨ Create one for me';
      // 🗑 QD7: attaching used to be reversible only by opening the editor, so a
      // wrong paste sent you to the very place the button exists to avoid. It
      // clears the URL line and leaves the ascii figure and the section alone.
      var rm = document.createElement('button'); rm.type = 'button';
      rm.className = 'xrm'; rm.textContent = '🗑 Remove';
      rm.hidden = !has;
      var no = document.createElement('button'); no.type = 'button'; no.textContent = '✕';
      var err = document.createElement('span'); err.className = 'xerr';
      row.append(inp, ok, mk, rm, no, err);
      function done(msg) {
        err.textContent = msg;
        (window.__boardRefresh || function () { location.reload(); })();
      }
      async function write(payload, busy, label) {
        busy.disabled = true; err.textContent = '…';
        var j = null;
        try { j = await post('/_board/diagram', payload); }
        catch (e) { j = null; }
        busy.disabled = false;
        if (j === null) {
          err.textContent = '';
          say('serve.py is not running — edit the URL line in ## Diagram yourself');
          return;
        }
        if (!j.ok) { err.textContent = '⚠ ' + (j.err || 'write failed'); return; }
        if (j.warn) say(j.warn);
        done(label);
      }
      mk.onclick = async function () {
        mk.disabled = true; err.textContent = 'creating…';
        var j = null;
        try { j = await post('/_board/excalidraw', { file: page.dataset.file }); }
        catch (e) { j = null; }
        mk.disabled = false;
        if (j === null) { err.textContent = ''; say('serve.py is not running'); return; }
        if (!j.ok) { err.textContent = ''; say(j.err || 'could not create one'); return; }
        done('✔ created');
      };
      box.append(open, row);
      if (host) host.appendChild(box);
      else {
        // where the section WOULD render: after Opening, before Content, which
        // is the same fixed place the endpoint inserts `## Diagram` itself.
        var op = page.querySelector('.opening');
        if (!op || !op.parentNode) return;
        op.parentNode.insertBefore(box, op.nextSibling);
      }
      open.onclick = function () { row.hidden = !row.hidden; if (!row.hidden) inp.focus(); };
      no.onclick = function () { row.hidden = true; err.textContent = ''; };
      rm.onclick = function () {
        write({ file: page.dataset.file, remove: true }, rm, '✔ removed');
      };
      function save() {
        var url = inp.value.trim();
        if (!url) { inp.focus(); return; }
        write({ file: page.dataset.file, url: url }, ok, '✔ saved');
      }
      ok.onclick = save;
      inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') save(); });
    });
  }


  /* ── 手动兜底：面板上的按钮 ───────────────────────────── */
  async function sync() {
    if (!db.length) { say('Nothing pending'); return; }
    if (!window.showDirectoryPicker) {
      navigator.clipboard.writeText(patch());
      say('This browser cannot write files — patch copied instead');
      return;
    }
    var n = await drain(true);
    say(n ? ('Wrote ' + n + ' comment(s) — rebuild to see them rendered')
          : 'Could not write. Grant access to the board folder.');
  }

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

  /* ── session 拣选器（QD1 Law 修正 260731：一题多 session，一个 current）──
     打开抽屉先亮清单：current 在头一行，历史按最后动笔新→旧，还有「＋新开一段」。
     选中的那段随下一条消息（或 ⌨ 终端）被 resume，同时成为 current，头部跟着换。 */
  var chatSid = '';        // '' = 跟着头部的 current · 'new' = 新开 · uuid = 点名的历史
  function sessAge(t) {
    if (!t) return '';
    var s = Math.max(0, Date.now() / 1000 - t);
    return s < 90 ? 'now' : s < 5400 ? Math.round(s / 60) + 'm'
         : s < 129600 ? Math.round(s / 3600) + 'h' : Math.round(s / 86400) + 'd';
  }
  function paintSessSummary(rows) {
    var n = rows.filter(function (r) { return r.landed; }).length;
    var named = function (r) { return r && (r.name || (r.id ? r.id.slice(0, 8) + '…' : '')); };
    var pickedRow = null;
    for (var pi = 0; pi < rows.length; pi++) if (rows[pi].id === chatSid) pickedRow = rows[pi];
    var cur = chatSid === 'new' ? ('new session next' + (sessName ? ': ' + sessName : ''))
            : chatSid ? named(pickedRow) + ' picked'
            : (rows[0] && rows[0].current ? named(rows[0]) : 'none yet');
    chat.querySelector('.spick summary').textContent =
      '🗂 Session: ' + cur + (n > 1 ? ' · ' + n + ' on record' : '') + ' ▾';
  }

  /* Paint from the browser, then correct from the SERVER (JL 260801: "when it
     is reloaded the chat box UI is just gone... should I make chat detached
     from the page html?").

     The session is ALREADY detached: it lives on the SessionHost and on disk as
     a .jsonl, and a turn started before a reload finishes there whether or not
     a browser is watching (measured 260801: the answer landed while the tab was
     reloading). What was NOT detached is what the drawer RENDERS, because it
     replayed a log kept per page in this browser. So a reload showed a
     transcript that was merely the last thing this tab happened to save.

     Fix the render, not the architecture: keep the instant local paint so the
     drawer never flashes empty, then ask the server for the session's real
     transcript and adopt it when it knows more. A reload now costs the live
     trace of an in-flight turn and nothing else.  */
  async function syncFromServer(logKey) {
    if (!cq || !cq.file) return;
    try {
      var r = await fetch('/_board/sessions', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: boardPath(), file: cq.file,
                               group: (cq && cq.group) || undefined }) });
      var j = await r.json();
      if (!j || j.ok === false) return;
      var cur = ((j.sessions) || []).filter(function (s) { return s.current && s.landed; })[0];
      if (!cur) return;
      var r2 = await fetch('/_board/session-log', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: boardPath(), file: cq.file,
                               group: (cq && cq.group) || undefined, id: cur.id }) });
      var j2 = await r2.json();
      if (!j2 || j2.ok === false) return;
      var srv = j2.log || [];
      var local = chatLoad(logKey);
      /* only adopt when the server genuinely knows more, so a page whose local
         log is ahead (a turn this tab just rendered) is never rolled back */
      if (srv.length <= local.length) return;
      var bd = chat.querySelector('.bd');
      if (bd.querySelector('.trace') || document.body.classList.contains('chatbusy')) return;
      bd.innerHTML = '';
      if (j2.clipped) bubble('sys', 'Showing the last ' + srv.length + ' of ' + j2.total + ' messages.');
      srv.forEach(function (m) { bubble(m.k, m.t); });
      chatSave(logKey, srv);
      bd.scrollTop = 1e9;
    } catch (e) { /* offline or an old server: the local paint still stands */ }
  }

  /* Replace the drawer's body with a session's REAL transcript, read from its
     .jsonl by the server (POST /_board/session-log). Read-only: this does not
     touch the page's own saved log, so switching back to the current session
     shows that one again, unchanged. */
  async function replaySession(sid, landed) {
    var bd = chat.querySelector('.bd');
    if (!landed) {
      bubble('sys', 'Nothing was ever said in that session, so there is no history to show.');
      return;
    }
    var note = bubble('sys', 'Loading that session\u2019s history\u2026');
    try {
      var r = await fetch('/_board/session-log', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        /* `path` is not optional: the server locates the board folder from the
           browser pathname, and without it every call answers "outside --root".
           Leaving it out is why this looked like an empty session. */
        body: JSON.stringify({ path: boardPath(), file: cq && cq.file,
                               group: (cq && cq.group) || undefined, id: sid })
      });
      var j = await r.json();
      if (note && note.parentNode) note.parentNode.removeChild(note);
      if (!j || j.ok === false) {
        bubble('sys', '\u26a0 could not read that session: ' + ((j && j.err) || 'unknown'));
        return;
      }
      var log = j.log || [];
      if (!log.length) {
        bubble('sys', 'That session has no readable messages yet.');
        return;
      }
      bd.innerHTML = '';
      if (j.clipped) {
        bubble('sys', 'Showing the last ' + log.length + ' of ' + j.total
                    + ' messages in this session.');
      }
      log.forEach(function (m) { bubble(m.k, m.t); });
      bubble('sys', '\u2191 history of the picked session \u00b7 your next message resumes it');
      bd.scrollTop = 1e9;
    } catch (e) {
      if (note && note.parentNode) note.parentNode.removeChild(note);
      bubble('sys', '\u26a0 could not load that session\u2019s history: ' + e.message);
    }
  }

  var sessName = '';   // 「＋ 新开一段」时给它起的名字（QD1 260731：Qxxx-干嘛用的）
  function renderSessions(j) {
    var sp = chat.querySelector('.spick'), sl = chat.querySelector('.spl');
    sl.innerHTML = '';
    var rows = (j && j.sessions) || [];
    var mk = function (label, meta, cls, onpick) {
      var d = document.createElement('div');
      d.className = 'sprow' + (cls ? ' ' + cls : '');
      d.innerHTML = '<span class="t"></span><span class="meta"></span>';
      d.querySelector('.t').textContent = label;
      d.querySelector('.meta').textContent = meta || '';
      d.onclick = onpick;
      sl.appendChild(d);
      return d;
    };
    rows.forEach(function (r) {
      var picked = chatSid ? chatSid === r.id : r.current;
      // 有名字显名字（QD3m-fix-black-screen），没名字退回第一句话
      var d = mk(r.name || r.title || (r.landed ? '(untitled)' : '(recorded, never talked)'),
         (r.current ? 'current · ' : '')
           + (r.landed ? sessAge(r.mtime) + ' · ' + Math.round((r.size || 0) / 1024) + 'k'
                       : 'hollow'),
         (picked ? 'cur' : '') + (r.name ? ' named' : '') + (r.landed || r.current ? '' : ' dim'),
         function () {
           chatSid = r.current ? '' : r.id;
           sp.open = false;
           paintSessSummary(rows);
           bubble('sys', r.current ? 'Back on the current session.'
             : 'Picked ' + (r.name || r.id.slice(0, 8) + '…') + ' — the next message (or ⌨) resumes it and makes it current.');
           /* Show what you are resuming (JL 260801: "I cannot see previous chat
              history"). The drawer's own log is per PAGE and kept in this
              browser, so it is the wrong transcript for a session picked here
              and empty for one started in a terminal or on another machine.
              The session's .jsonl on disk is the only honest source. */
           replaySession(r.id, r.landed);
         });
      // ✎ 改名：行内输入，写进登记表，不打断挑选
      var e = document.createElement('button');
      e.className = 'sprn'; e.textContent = '✎'; e.title = 'Name this session';
      e.onclick = function (ev) {
        ev.stopPropagation();
        var inp = document.createElement('input');
        inp.type = 'text'; inp.className = 'spin';
        inp.placeholder = 'what is this session for?';
        inp.value = (r.name || '').replace(/^[^-]*-/, '');
        d.querySelector('.t').replaceChildren(inp); inp.focus();
        var done = function () {
          fetch('/_board/session-name', { method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ path: boardPath(), file: cq.file,
                                   group: (cq && cq.group) || undefined,
                                   id: r.id, name: inp.value.trim() }) })
            .then(function () { loadSessions(); });
        };
        inp.onkeydown = function (k) { if (k.key === 'Enter') done(); if (k.key === 'Escape') loadSessions(); };
        inp.onblur = done;
      };
      d.appendChild(e);
    });
    var nu = mk('＋ New session', 'starts fresh, primed with this question', 'new', function () {
      // 先问一句这段是干嘛的（可留空）：名字跟着第一条消息/⌨ 一起落进登记表
      var inp = document.createElement('input');
      inp.type = 'text'; inp.className = 'spin';
      inp.placeholder = 'name it: what is this session for? (Enter · empty = unnamed)';
      nu.querySelector('.t').replaceChildren(inp); inp.focus();
      inp.onclick = function (ev) { ev.stopPropagation(); };
      inp.onkeydown = function (k) {
        if (k.key === 'Enter') {
          sessName = inp.value.trim();
          chatSid = 'new'; sp.open = false; paintSessSummary(rows);
          bubble('sys', 'The next message (or ⌨) starts a NEW session'
            + (sessName ? ' named "' + sessName + '"' : '') + ' for this question.');
        }
        if (k.key === 'Escape') loadSessions();
      };
    });
    sp.hidden = false;
    sp.open = rows.filter(function (r) { return r.landed; }).length > 1;
    paintSessSummary(rows);
  }
  async function loadSessions() {
    var sp = chat.querySelector('.spick');
    sp.hidden = true;
    if (!cq) return;
    try {
      var r = await fetch('/_board/sessions', { method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: boardPath(), file: cq.file,
                               group: (cq && cq.group) || undefined }) });
      var j = await r.json();
      if (j.ok) renderSessions(j);
    } catch (e) { /* serve.py 没跑 → 没有拣选器，其余照旧 */ }
  }

  function clearSentenceFocus() {
    sentenceFocus = null;
    var box = chat.querySelector('.sfocus');
    box.hidden = true;
    box.querySelector('.sfref').textContent = '';
    box.querySelector('.sfpath').textContent = '';
    box.querySelector('.sfquote').textContent = '';
    box.querySelector('.sfattached pre').textContent = '';
    box.querySelector('.sfattached').hidden = true;
    chat.querySelector('textarea').placeholder = cq && cq.board
      ? 'Ask about this board — e.g. what should we act on next?'
      : 'Ask about this question…';
  }

  /* One focus card, two kinds of focus (QB5d): a SENTENCE, or a HEADING — a
     `##` section or a `###` subsection. Same card, same session, same clear
     button; only the packet's wording and the placeholder differ. */
  function setSentenceFocus(ref, sentence, attached, contentPath, kind) {
    sentenceFocus = { ref: ref, sentence: sentence, attached: attached || '',
                      contentPath: contentPath || '', kind: kind || 'sentence' };
    var box = chat.querySelector('.sfocus');
    box.hidden = false;
    box.querySelector('.sfref').textContent = ref;
    box.querySelector('.sfpath').textContent = contentPath || '';
    box.querySelector('.sfpath').hidden = !contentPath;
    box.querySelector('.sfquote').textContent = sentence;
    var details = box.querySelector('.sfattached');
    var rows = (attached || '').split(/\n+/).filter(function (x) { return x.trim(); });
    details.hidden = !rows.length;
    details.open = false;
    details.querySelector('summary').textContent =
      'Attached · ' + rows.length;
    details.querySelector('pre').textContent = attached || '';
    chat.querySelector('textarea').placeholder =
      sentenceFocus.kind === 'heading' ? 'Ask about this section…'
                                       : 'Ask about this sentence…';
  }
  function focusedMessage(message) {
    if (!sentenceFocus) return message;
    if (sentenceFocus.kind === 'heading') {
      return 'Focus this turn on ' + sentenceFocus.ref + '.\n\n' +
        (sentenceFocus.contentPath
          ? 'Markdown source:\n' + sentenceFocus.contentPath + '\n\n' : '') +
        'What is visible under that heading:\n' + sentenceFocus.sentence +
        '\n\nUser message:\n' + message +
        '\n\nDiscuss this section specifically. Read the rest of the page when ' +
        'needed, but keep this section as the explicit focus.';
    }
    return 'Focus this turn on sentence ' + sentenceFocus.ref + '.\n\n' +
      (sentenceFocus.contentPath
        ? 'Content location:\n' + sentenceFocus.contentPath + '\n\n' : '') +
      'Sentence:\n' + sentenceFocus.sentence +
      (sentenceFocus.attached
        ? '\n\nAttached directly beneath it:\n' + sentenceFocus.attached : '') +
      '\n\nUser message:\n' + message +
      '\n\nDiscuss this sentence specifically. Read the rest of the page when needed, ' +
      'but keep this sentence as the explicit focus.';
  }
  chat.querySelector('.sfclear').onclick = clearSentenceFocus;

  function chatLoad(id) {
    try { return JSON.parse(localStorage.getItem(CHATK(id)) || '[]'); } catch (e) { return []; }
  }
  function chatSave(id, log) { localStorage.setItem(CHATK(id), JSON.stringify(log)); }

  /* 回复是 markdown，得渲染出来 —— 先转义，再只认几种最常用的写法。
     不引第三方库：这一页坚持自带一切，而且要渲染的只是我们自己 agent 的输出。 */
  function mdEsc(s) {
    return s.replace(/[&<>]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]; });
  }
  function mdInline(s) {
    return mdEsc(s)
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      /* [text](url) — only http/https, so an escaped javascript: cannot ride in */
      .replace(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/g,
               '<a href="$2" target="_blank" rel="noopener">$1</a>')
      .replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>')
      .replace(/(^|[\s(])\*([^*\s][^*]*)\*/g, '$1<i>$2</i>');
  }
  /* A pipe table is one row per line and a |---|---| rule under the header.
     Without this every table in a reply printed as its own raw pipe lines, which
     is most of what "the readme is not well rendered" was (JL 260731). Indexed
     loop rather than forEach, because a table needs to look ahead and skip. */
  function mdRow(ln) {
    var s = ln.trim().replace(/^\|/, '').replace(/\|$/, '');
    return s.split('|').map(function (c) { return c.trim(); });
  }
  function isRule(ln) { return /^\s*\|?[\s:|-]*-[\s:|-]*\|?\s*$/.test(ln) && ln.indexOf('-') >= 0; }
  function md2html(src) {
    var out = [], fence = null, list = null;
    var flush = function () { if (list) { out.push('</' + list + '>'); list = null; } };
    var LN = (src || '').split('\n');
    for (var li = 0; li < LN.length; li++) {
      var ln = LN[li];
      if (fence === null && ln.trim().charAt(0) === '|' && li + 1 < LN.length
          && isRule(LN[li + 1]) && LN[li + 1].indexOf('|') >= 0) {
        flush();
        var head = mdRow(ln), rows = [];
        li += 2;
        while (li < LN.length && LN[li].trim().charAt(0) === '|') { rows.push(mdRow(LN[li])); li++; }
        li--;
        out.push('<table class="mdt"><thead><tr>'
          + head.map(function (c) { return '<th>' + mdInline(c) + '</th>'; }).join('')
          + '</tr></thead><tbody>'
          + rows.map(function (r) {
              return '<tr>' + r.map(function (c) { return '<td>' + mdInline(c) + '</td>'; }).join('') + '</tr>';
            }).join('')
          + '</tbody></table>');
        continue;
      }
      if (ln.trim().slice(0, 3) === '```') {
        if (fence === null) { flush(); fence = []; }
        else { out.push('<pre>' + mdEsc(fence.join('\n')) + '</pre>'); fence = null; }
        continue;
      }
      if (fence !== null) { fence.push(ln); continue; }
      if (!ln.trim()) { flush(); continue; }
      var h = ln.match(/^(#{1,6})\s+(.*)$/);
      if (h) { flush(); out.push('<div class="mh">' + mdInline(h[2]) + '</div>'); continue; }
      var b = ln.match(/^\s*[-*]\s+(.*)$/);
      if (b) {
        if (list !== 'ul') { flush(); out.push('<ul>'); list = 'ul'; }
        out.push('<li>' + mdInline(b[1]) + '</li>'); continue;
      }
      var n = ln.match(/^\s*\d+[.)]\s+(.*)$/);
      if (n) {
        if (list !== 'ol') { flush(); out.push('<ol>'); list = 'ol'; }
        out.push('<li>' + mdInline(n[1]) + '</li>'); continue;
      }
      if (list) { out.push('<li class="cont">' + mdInline(ln.trim()) + '</li>'); continue; }
      out.push('<p>' + mdInline(ln) + '</p>');
    }
    if (fence !== null) out.push('<pre>' + mdEsc(fence.join('\n')) + '</pre>');
    flush();
    return out.join('');
  }
  function bubble(kind, text) {
    var d = document.createElement('div');
    d.className = 'm ' + kind;
    if (kind === 'cc') { d.classList.add('md'); d.innerHTML = md2html(text); }
    else { d.textContent = text; }
    chat.querySelector('.bd').appendChild(d);
    chat.querySelector('.bd').scrollTop = 1e9;
    return d;
  }
  /* 思考过程：一个可折叠块。默认展开着让你看它边想，答案一到就自动收起；
     之后随时点标题再展开。跟 CLI 里的 thinking 一个意思，只是这里能折叠。 */
  /* One card per tool call, the shape the VS Code plugin shows (JL 260731:
     "make the thinking and tool calling to be out as well"). Before this the
     drawer put the tool NAME in the transient waiting line and dropped it on
     the next event, so a turn that ran ten tools left no trace of any of them. */
  /* The "still working" line (JL 260731: "check how claude code indicates that
     claude is still working"). The CLI keeps ONE line alive for the whole turn:
     a pulsing glyph, what it is doing right now, and the seconds so far. Ours
     did the opposite — a static '…thinking' bubble that the first event deleted,
     so the longest part of a turn showed nothing at all. */
  /* THE TRACE (JL 260731). A turn produces two very different kinds of thing:
     the interim stream (thinking, narration between tool calls, the calls
     themselves) and the ANSWER. Mixing them at the same size made the answer
     hard to find and, worse, the interim segments were being re-rendered
     cumulatively — each new bubble repeated everything before it. The interim
     stream now lives in one scrollable box at a smaller size, and the answer
     lands under it at full size. */
  var traceEl = null;
  function traceHost() { return traceEl || chat.querySelector('.bd'); }
  function traceStart() {
    traceEl = document.createElement('div');
    traceEl.className = 'trace';
    chat.querySelector('.bd').appendChild(traceEl);
    return traceEl;
  }
  function traceRow(cls, icon, text) {
    var d = document.createElement('div');
    d.className = 'tr ' + cls;
    d.innerHTML = '<span class="i"></span><span class="x"></span>';
    d.querySelector('.i').textContent = icon;
    d.querySelector('.x').textContent = text;
    traceHost().appendChild(d);
    traceScroll();
    return d;
  }
  function traceScroll() {
    if (traceEl) traceEl.scrollTop = 1e9;
    var bd = chat.querySelector('.bd'); if (bd) bd.scrollTop = 1e9;
  }
  function traceEnd(meta) {             /* keep it, labelled and re-openable */
    if (!traceEl) return;
    var rows = traceEl.querySelectorAll('.tr').length;
    var tools = traceEl.querySelectorAll('.tool').length;
    var thinks = traceEl.querySelectorAll('.tk').length;
    var n = rows + tools + thinks;
    if (!n) {                           /* a plain question used no tools and did
                                           not narrate: no trace to show at all */
      if (traceEl.parentNode) traceEl.parentNode.removeChild(traceEl);
      traceEl = null; return;
    }
    /* JL 260731: "the thinking process is good, but when it is finished, they
       are gone, could we keep them." It WAS kept, but as a dimmed 120px sliver
       that read as empty. A finished turn now gets a real <details> with a
       labelled summary, closed but obviously openable, and nothing is dropped. */
    var box = traceEl, host = box.parentNode;
    var det = document.createElement('details');
    det.className = 'traced';
    var bits = [];
    if (thinks) bits.push('💭 thinking');
    if (tools) bits.push('⚒ ' + tools + (tools === 1 ? ' tool' : ' tools'));
    if (rows) bits.push('✍️ ' + rows + (rows === 1 ? ' note' : ' notes'));
    det.innerHTML = '<summary><span class="tsum"></span><span class="tmeta"></span></summary>';
    det.querySelector('.tsum').textContent = n + (n === 1 ? ' step · ' : ' steps · ') + bits.join(' · ');
    if (meta) det.querySelector('.tmeta').textContent = meta;
    box.classList.remove('trace'); box.classList.add('tracebody');
    box.style.maxHeight = ''; box.scrollTop = 0;
    host.insertBefore(det, box);
    det.appendChild(box);
    traceEl = null;
  }

  var BUSY_GLYPHS = ['✻', '✽', '✳', '✢', '·', '✢', '✳', '✽'];
  var busyEl = null, busyTimer = null, busyT0 = 0, busyStep = 0, busyWhat = '';
  function busyStart(what) {
    busyEnd();
    busyT0 = Date.now(); busyStep = 0; busyWhat = what || 'Working';
    busyEl = document.createElement('div');
    busyEl.className = 'busy';
    busyEl.innerHTML = '<span class="g"></span><span class="w"></span>' +
                       '<span class="s"></span>';
    traceHost().appendChild(busyEl);
    busyTick();
    busyTimer = setInterval(busyTick, 400);
  }
  function busyTick() {
    if (!busyEl) return;
    busyEl.querySelector('.g').textContent = BUSY_GLYPHS[busyStep++ % BUSY_GLYPHS.length];
    busyEl.querySelector('.w').textContent = busyWhat;
    var s = Math.round((Date.now() - busyT0) / 1000);
    busyEl.querySelector('.s').textContent = s >= 1 ? s + 's' : '';
  }
  function busySay(what) {
    busyWhat = what || busyWhat;
    if (!busyEl) busyStart(busyWhat); else busyTick();
    busyBump();
  }
  function busyBump() {          /* keep it the last row as content arrives */
    if (busyEl && busyEl.parentNode) busyEl.parentNode.appendChild(busyEl);
    traceScroll();
  }
  function busyEnd() {
    if (busyTimer) { clearInterval(busyTimer); busyTimer = null; }
    if (busyEl && busyEl.parentNode) busyEl.parentNode.removeChild(busyEl);
    busyEl = null;
  }

  var toolCards = {};   /* tool_use_id -> its card, cleared when the page changes */
  function toolCard(ev) {
    var d = document.createElement('details');
    d.className = 'tool';
    d.innerHTML = '<summary><span class="tn"></span><span class="tb"></span>' +
                  '<span class="ts">running…</span></summary>' +
                  '<div class="tio"></div>';
    d.querySelector('.tn').textContent = ev.name || '?';
    d.querySelector('.tb').textContent = (ev.brief || '').replace(ev.name + '  ', '');
    if (ev.input) {
      var pre = document.createElement('pre');
      pre.className = 'tin'; pre.textContent = ev.input;
      d.querySelector('.tio').appendChild(pre);
    }
    traceHost().appendChild(d);
    busyBump();
    if (ev.id) toolCards[ev.id] = d;
    return d;
  }
  function toolResult(ev) {
    var d = ev.id && toolCards[ev.id];
    if (!d) return;                       /* result with no card: nothing to fill */
    d.querySelector('.ts').textContent = ev.is_error ? 'error' : 'done';
    d.classList.toggle('err', !!ev.is_error);
    if (ev.output) {
      var pre = document.createElement('pre');
      pre.className = 'tout'; pre.textContent = ev.output;
      d.querySelector('.tio').appendChild(pre);
    }
    delete toolCards[ev.id];
  }

  function thinkBubble() {
    var d = document.createElement('details');
    d.className = 'tk'; d.open = true;
    d.innerHTML = '<summary>💭 Thinking</summary><div class="tk-body"></div>';
    traceHost().appendChild(d);
    traceScroll();
    return d;
  }

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
    /* the local paint above is instant; the server holds the truth */
    syncFromServer(isGroup ? 'G:' + cq.id : cq.id);
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
       root 精确算法：serve.py 在 <root> + Board public path 处提供文件，
       所以 root = 板文件夹绝对路径 减去 URL 里的 Board 目录。不靠 .git/pyproject 猜，
       也不把 split page 的 board/<GROUP>/ 误当成 Board 目录。 */
    var board = document.body.getAttribute('data-board') || '.';
    var urlDir = boardDirPath();
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

  /* 模型 / effort / 权限档 记在本机；default Opus 5 · high · full·ask */
  (function () {
    var m = chat.querySelector('.mdl'), e = chat.querySelector('.eff'),
        s = chat.querySelector('.scope');
    m.value = localStorage.getItem(MK) || 'opus';
    e.value = localStorage.getItem(EK) || 'high';
    s.value = localStorage.getItem(SK) || 'full';
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

  var inflight = null;                    // 正在跑的那一轮：{ctrl, file}
  var followPending = false;              // navigated mid-turn; switch when it ends
  async function chatStop() {
    if (!inflight) return;
    if (chatQueue.length) {             // stopping means stop, including what is queued
      chatQueue.length = 0;
      chat.querySelectorAll('.bd .m.you.queued').forEach(function (d) { d.remove(); });
      bubble('sys', 'Stopped — queued messages were dropped.');
    }
    try {
      await fetch('/_board/stop', { method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: boardPath(), file: inflight.file }) });
      bubble('sys', 'Stop signal sent — it will wrap up at the next message…');
    } catch (e) { /* 服务器都不通了，直接放弃等待 */ }
    inflight.ctrl.abort();                // 浏览器这边立刻不等了
  }
  function chatBusy(on) {
    /* A turn in flight is exactly as interruptible as an open terminal: the
       asset-stamp guard already defers a full reload for `termon`, and without
       the same flag here a rebuild mid-turn wipes the trace and aborts the
       stream. Ships happen often (three sessions shipped JS in one day). */
    document.body.classList.toggle('chatbusy', on);
    if (!on && window.__pendingReload) { location.reload(); return; }
    var btn = chat.querySelector('.send');
    btn.textContent = on ? '⏹' : '➤';
    btn.title = on ? 'Stop this turn' : 'Send';
    btn.classList.toggle('stop', on);
    btn.disabled = false;                 // 忙的时候也能点 —— 那是停止键
    /* Type-ahead (JL 260731: "when the SDK chat draw is running, I cannot enter
       the new messages, why?"). Disabling the box was the easy way to enforce
       one turn at a time, but it also stops you composing the next thought while
       you wait, which the CLI has always allowed. The box stays live; Enter
       QUEUES instead of racing the server, which still refuses two turns. */
    var ta = chat.querySelector('textarea');
    ta.disabled = false;
    ta.placeholder = on ? 'Type the next message — it sends when this turn finishes…'
                        : (cq && cq.board ? 'Ask about this board…' : 'Ask about this question…');
  }

  /* Messages typed while a turn is running, sent in order once it ends. */
  /* Flight recorder (JL 260731, after the same wedge recurred and every
     synthetic test passed). Keeps the last 200 things the drawer did, so a
     stuck turn can be described instead of guessed at. Cheap, no I/O. */
  var chatDiag = [];
  function diag(kind, detail) {
    chatDiag.push(new Date().toISOString().slice(11, 19) + ' ' + kind
                  + (detail ? ' ' + String(detail).slice(0, 120) : ''));
    if (chatDiag.length > 200) chatDiag.shift();
  }
  window.__chatDiag = function () {
    var d = {
      when: new Date().toISOString(),
      page: cq && (cq.id + ' · ' + cq.file),
      settings: [(chat.querySelector('.mdl') || {}).value,
                 (chat.querySelector('.eff') || {}).value,
                 (chat.querySelector('.scope') || {}).value].join(' / '),
      session: chatSid || '(current)',
      inflight: !!inflight,
      queued: chatQueue.length,
      dom: {
        busy: !!chat.querySelector('.busy'),
        trace: !!chat.querySelector('.trace'),
        traced: chat.querySelectorAll('.traced').length,
        answers: chat.querySelectorAll('.bd > .m.cc').length,
        stopBtn: chat.querySelector('.send').classList.contains('stop')
      },
      log: chatDiag.slice(-80)
    };
    return JSON.stringify(d, null, 1);
  };

  var chatQueue = [];
  function queueMsg(text) {
    chatQueue.push(text);
    var d = bubble('you', text);
    d.classList.add('queued');
    d.title = 'queued — sends when the current turn finishes';
    busyBump();
    return d;
  }
  function drainQueue() {
    if (!chatQueue.length || inflight) return;
    var next = chatQueue.shift();
    /* the queued bubble was already drawn; chatSend draws its own, so drop the
       placeholder first and let the real one take its place */
    var ph = chat.querySelector('.bd .m.you.queued');
    if (ph && ph.parentNode) ph.parentNode.removeChild(ph);
    chatSend(next);
  }

  async function chatSend(preset, opts) {
    var ta = chat.querySelector('textarea'), btn = chat.querySelector('.send');
    if (inflight) return chatStop();       // 正在跑 → 这一下是「停」
    var msg = (preset || ta.value).trim();
    if (!msg || !cq) return;
    if (!preset) ta.value = '';
    /* On a phone the utility controls are deliberately folded.  Starting the
       next turn must give its live answer the room, rather than leaving model,
       permission and session metadata above the composer. */
    setUtility(false);
    chatBusy(true);
    var log = chatLoad(cq.id);
    bubble('you', msg); log.push({ k: 'you', t: msg }); chatSave(cq.id, log);
    diag('SEND', msg.slice(0, 60));
    traceStart();
    busyStart('Thinking');
    var ctrl = new AbortController();
    inflight = { ctrl: ctrl, file: cq.file };
    /* Watchdog. The fetch can hang with no event ever arriving, and then the
       code below never reaches chatBusy(false): red stop button, dead drawer,
       nothing moving. Report the silence, then give up rather than hang. */
    var lastEv = Date.now();
    var QUIET_WARN = 45000, QUIET_GIVEUP = 420000;
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
      var r = await fetch('/_board/chat', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        signal: ctrl.signal,
        body: JSON.stringify({ path: boardPath(), file: cq.file,
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
          scope: (opts && opts.scope) || chat.querySelector('.scope').value,
          quality_check: !!(opts && opts.qualityCheck) })
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
        busyEnd(); traceEnd();
        bubble('sys', '⚠ ' + (errTxt || ('the server refused this turn (HTTP ' + r.status + ')')));
        clearInterval(watchdog); window.__pendingSince = 0;
        inflight = null; chatBusy(false); ta.focus();
        return;
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
          lastEv = Date.now();
          if (ev.t !== 'delta' && ev.t !== 'think') diag('ev:' + ev.t, ev.name || ev.text || '');
          if (ev.t === 'stage') {                 // real progress while nothing streams yet
            busySay(ev.text.length > 46 ? ev.text.slice(0, 46) + '…' : ev.text);
          } else if (ev.t === 'think') {          // 思考过程 → 折叠块，边想边展开
            busySay('Thinking');
            if (!thinkEl) thinkEl = thinkBubble();
            thinkAcc += ev.text;
            thinkEl.querySelector('.tk-body').textContent = thinkAcc;
            chat.querySelector('.bd').scrollTop = 1e9;
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
      traceEnd(tookTxt + ' · finished ' + stamp);
      var txt = j.ok ? (lastSeg || j.text || acc ||
                        '(no text reply — it may have only used tools)')
                     : ('⚠ ' + (j.err || 'failed'));
      if (j.stopped) txt = txt + '\n(you stopped this turn, so it may be unfinished)';
      bubble('cc', txt);              /* the answer, once, at full size */
      /* history keeps the WHOLE turn, not just its last line */
      log.push({ k: 'cc', t: (j.ok ? (j.text || acc || txt) : txt) });
      chatSave(cq.id, log);
      if (j.ok) {
        // 这一轮聊到的 session 现在就是 current（服务器已写回头部）——
        // 拣选状态归位、清单重拉，免得下一条还带着旧的点名
        if (j.session) { chatSid = ''; sessName = ''; loadSessions(); }
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
      bubble('sys', e.name === 'AbortError'
        ? 'Stopped waiting. The server got the stop signal too.'
        : '⚠ ' + e.message);
    }
    clearInterval(watchdog);
    window.__pendingSince = 0;
    inflight = null; chatBusy(false); ta.focus();
    drainQueue();                       // whatever you typed while it ran
    if (followPending && !inflight) follow();   // you navigated while it ran
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

  /* ── 面板跟着题走（JL 260723）────────────────────────────────
     换一题 = 换一个 session。抽屉开着的时候，切到哪一题它就跟到哪一题：
     聊天记录换成那一题的，session id 换成那一题的；
     本来在终端模式的话，先把上一题的 session 交回去，再开新那一题的终端。 */
  async function follow() {
    var id = (location.hash || '').slice(1);
    if (!chat.classList.contains('on')) return;     // 抽屉没开就别多事
    /* A turn is streaming for the page we are LEAVING. Switching now would
       abort it (see the inflight guard in chatOpen), so hold the switch and
       replay it the moment the turn ends. */
    if (inflight) { followPending = true; diag('follow DEFERRED (turn running)'); return; }
    followPending = false;
    var sec = id && document.getElementById(id);
    var isQ = sec && sec.classList.contains('q');
    if (!isQ && docPage()) {            // a split page file: it is its own page
      var only = docPage();
      if (!cq || cq.id !== only.id) {
        /* same hand-over as the hash branch below: park the old scope's PTY
           and reopen on the new one, or the drawer label switches while the
           OLD page's claude keeps the screen (⌨ on the tree, 260731). */
        var wtp = termOn, ofp = cq && cq.file, ogp = cq && cq.group;
        if (wtp) await termRelease(ofp, ogp);
        await chatOpen(only);
        if (wtp) await termOpen(true);
      }
      return;
    }
    if (!isQ && docGroup()) {           // a split group file: its own group
      var gname = docGroup();
      if (!cq || cq.group !== gname) {
        var wtg = termOn, ofg = cq && cq.file, ogg = cq && cq.group;
        if (wtg) await termRelease(ofg, ogg);
        await chatOpen({ group: gname });
        if (wtg) await termOpen(true);
      }
      return;
    }
    if (!isQ) {
      /* 回到目录（#top / #qlist / #all / 无锚点）→ 跟到整板会话（QD5）。
         别的锚点（某个小节之类）不算换地方，不动。 */
      if (id && id !== 'top' && id !== 'qlist' && id !== 'all') return;
      if (cq && cq.board) return;                   // 已经是整板会话
      var wt = termOn, of = cq && cq.file, og = cq && cq.group;
      if (wt) await termRelease(of, og);
      await chatOpen('board');
      if (wt) await termOpen(true);
      say('Now following the board');
      return;
    }
    if (cq && cq.id === sec.id) return;             // 还是同一题
    var wasTerm = termOn, oldFile = cq && cq.file, oldGroup = cq && cq.group;
    if (wasTerm) await termRelease(oldFile, oldGroup);  // 一个 session 一个窗口
    await chatOpen(sec);                            // 重新绑到新题（会重置成聊天视图）
    if (wasTerm) await termOpen(true);              // 本来在终端 → 跟着切过去
    say('Now following ' + sec.id);
  }
  window.addEventListener('hashchange', follow);
  /* The split site (QC9) navigates through the client-side router in
     assets/board.js's `go()`, which swaps div.wrap and never touches the hash.
     Without this line the drawer keeps whatever page it opened on, which is
     JL's 260731 report: "换一个 page 之后再打开它，这个 chatbot 还是之前的 page". */
  window.addEventListener('board:updated', follow);

  /* 每张卡片的头部挂一个入口（idempotent —— live refresh 换掉 .wrap 后要重挂） */
  function wireQBtns() {
    document.querySelectorAll('section.q').forEach(function (sec) {
      if (sec.querySelector('.chatbtn')) return;
      var b = document.createElement('button');
      b.className = 'chatbtn'; b.textContent = '\u{1F916} Chat';
      b.onclick = function () {
        // 顺便把 URL 也切到这一题，这样 follow() 和「回目录」都对得上
        if (location.hash !== '#' + sec.id) location.hash = sec.id;
        chatOpen(sec);
      };
      var qh = sec.querySelector('.qh');
      if (qh) qh.appendChild(b);
    });
  }
  wireQBtns();

  /* ── index structure controls (QC2, JL 260724): add / archive groups and
     questions straight from the front page. Every button is only a WRITER:
     POST /_board/structure edits board.md (and seeds/moves the Q files), the
     server rebuilds, and the live watcher (QD6) swaps the new index in place.
     Archive never deletes: files move to _archive/ inside the board folder. */
  function structPost(op, extra, okMsg) {
    var payload = { op: op };
    Object.keys(extra).forEach(function (k) { payload[k] = extra[k]; });
    post('/_board/structure', payload).then(function (j) {
      if (!j) { say('No live server behind this page'); return; }
      if (!j.ok) { say(j.err || 'failed'); return; }
      say(okMsg(j));
      if (window.__boardRefresh) window.__boardRefresh();
    }).catch(function () { say('No live server behind this page'); });
  }
  function arm(btn, fire) {
    /* two-step confirm, no native dialogs: first click arms, second fires */
    if (btn._armT) {
      clearTimeout(btn._armT); btn._armT = null;
      btn.classList.remove('arm'); btn.textContent = btn._lbl;
      fire(); return;
    }
    btn._lbl = btn.textContent;
    btn.classList.add('arm'); btn.textContent = 'sure?';
    btn._armT = setTimeout(function () {
      btn._armT = null; btn.classList.remove('arm'); btn.textContent = btn._lbl;
    }, 2600);
  }
  function miniForm(anchor, fields, onGo) {
    var old = document.querySelector('.gform');
    if (old) old.remove();
    var f = document.createElement('span');
    f.className = 'gform';
    var ins = fields.map(function (ph) {
      var i = document.createElement('input');
      i.placeholder = ph; f.appendChild(i); return i;
    });
    var go = document.createElement('button'); go.className = 'go'; go.textContent = 'Add';
    var cx = document.createElement('button'); cx.className = 'cx2'; cx.textContent = '×';
    f.appendChild(go); f.appendChild(cx);
    go.onclick = function () {
      var vals = ins.map(function (i) { return i.value.trim(); });
      if (!vals[0]) { ins[0].focus(); return; }
      f.remove(); onGo(vals);
    };
    cx.onclick = function () { f.remove(); };
    ins.forEach(function (i) {
      i.onkeydown = function (ev) {
        if (ev.key === 'Enter') go.onclick();
        if (ev.key === 'Escape') cx.onclick();
      };
    });
    anchor.appendChild(f);
    ins[0].focus();
  }
  function wireStruct() {
    document.querySelectorAll('div.grp').forEach(function (g) {
      if (g.querySelector('.gadd')) return;
      var name = g.getAttribute('data-g') || '';
      var add = document.createElement('button');
      add.className = 'gadd'; add.type = 'button'; add.textContent = '＋ Q';
      add.title = 'Add a question to ' + name;
      add.onclick = function () {
        miniForm(g, ['new question title'], function (v) {
          structPost('add_question', { group: name, title: v[0] },
            function (j) { return 'Added ' + j.file; });
        });
      };
      var gc = document.createElement('button');
      gc.className = 'gchat'; gc.type = 'button'; gc.textContent = '\u{1F4AC}';
      gc.title = 'Chat about this group (SDK drawer; \u2328 inside switches to the CLI)';
      gc.onclick = function () { chatOpen({ group: name }); };
      g.appendChild(gc);
      var del = document.createElement('button');
      del.className = 'garch'; del.type = 'button'; del.textContent = '\u{1F5C4}';
      del.title = 'Archive this group (only when it lists no questions)';
      del.onclick = function () {
        arm(del, function () {
          structPost('archive_group', { group: name },
            function (j) { return 'Archived group ' + j.group; });
        });
      };
      g.appendChild(add); g.appendChild(del);
    });
    document.querySelectorAll('a.ir[data-f]').forEach(function (row) {
      if (row.querySelector('.qarch')) return;
      var b = document.createElement('span');
      b.className = 'qarch'; b.textContent = '\u{1F5C4}';
      b.title = 'Archive ' + row.getAttribute('data-f') +
        ' (moves to _archive/, never deletes)';
      b.onclick = function (ev) {
        ev.preventDefault(); ev.stopPropagation();
        arm(b, function () {
          structPost('archive_question', { q: row.getAttribute('data-f') },
            function (j) { return 'Archived ' + j.file + ' → ' + j.to; });
        });
      };
      row.appendChild(b);
    });
    var idxBox = document.querySelector('div.idx');
    if (idxBox && !idxBox.querySelector('.gnew')) {
      var ng = document.createElement('button');
      ng.className = 'gnew'; ng.type = 'button'; ng.textContent = '＋ Group';
      ng.title = 'Add a question group (letter is picked automatically)';
      ng.onclick = function () {
        miniForm(idxBox, ['new group title', 'one-line intro (optional)'], function (v) {
          structPost('add_group', { title: v[0], hook: v[1] || '' },
            function (j) { return 'Added group ' + j.group; });
        });
      };
      idxBox.appendChild(ng);
    }
  }
  wireStruct();

  /* 右下角悬浮的「🤖 Chat」—— 聚焦某一题时开这一题的抽屉；
     在目录页（QD5，JL 260725「chatbot in the index page」）开整板会话。 */
  /* Which page is this document ABOUT? (JL 260731, after the QC9 split.)
     In the one-file board every page is a section and the hash names the one
     you are looking at. In the split site each page is its OWN file with no
     hash at all, so hash-only logic fell through to the board session and the
     drawer stayed on board.md no matter which page you opened. A file holding
     exactly one `section.q` IS that page; the index and the group files hold
     none and correctly mean the board. */
  function docPage() {
    var qs = document.querySelectorAll('section.q');
    return qs.length === 1 ? qs[0] : null;
  }
  /* A GROUP file (board/QA.html) holds no page section and its own h1 IS the
     group title, in board.md's `### QA · Design` grammar. That title is exactly
     what a group session is keyed by, so no new registry is needed. The index's
     h1 is the board title and does not match, which keeps the three levels
     apart: page → group → board (JL 260731). */
  function docGroup() {
    if (docPage()) return null;
    var h = document.querySelector('.h1');
    var txt = h ? h.textContent.trim() : '';
    return /^[QS][A-Za-z]*\d*\s*[·:]/.test(txt) ? txt : null;
  }
  function chatTarget() {
    var id = (location.hash || '').slice(1);
    var sec = id && document.getElementById(id);
    if (sec && sec.classList.contains('q')) return sec;
    var only = docPage();
    if (only) return only;
    var g = docGroup();
    return g ? { group: g } : null;   // null only on the index → board session
  }
  var fab = document.createElement('button');
  fab.id = 'chatfab';
  fab.onclick = function () {
    var sec = chatTarget();
    if (sec) chatOpen(sec); else chatOpen('board');
  };
  function fabLbl() {
    var tgt = chatTarget();
    fab.innerHTML = !tgt ? '\u{1F916} Board chat'
                  : (tgt.group ? '\u{1F916} Group chat' : '\u{1F916} Chat');
  }
  window.addEventListener('hashchange', fabLbl);
  window.addEventListener('board:updated', fabLbl);   // router swap (QC9 split site)
  fabLbl();
  /* the reload-restore block at the end of this file needs to read and rebuild
     the drawer, and it lives outside this closure */
  window.__boardDrawerOpen = function () { return chat.classList.contains('on'); };
  window.__boardDrawerReopen = function () {
    if (chat.classList.contains('on')) return;
    var t = chatTarget();
    return chatOpen(t || 'board');
  };
  document.body.appendChild(fab);

  /* Sentence chat reuses this question's existing session. The click establishes
     a visible focus card but does not spend a model turn. The next user message
     is augmented with the address, sentence, and direct apparatus at send time. */
  window.__boardSentenceChat = async function (sec, ref, sentence, attached, contentPath) {
    if (!sec || !sec.classList.contains('q')) return;
    await chatOpen(sec);
    if (location.hash !== '#' + sec.id) location.hash = sec.id;
    setSentenceFocus(ref, sentence, attached, contentPath);
    chat.querySelector('textarea').focus();
  };

  /* The same door for a heading (QB5d): a `##` section or `###` subsection
     focuses THIS page's existing session, never a session of its own. The hash
     is left alone because a tree page has none, and the reader is already on
     the heading they clicked. */
  window.__boardHeadingChat = async function (sec, path, block, file) {
    if (!sec || !sec.classList.contains('q')) return;
    await chatOpen(sec);
    setSentenceFocus(path, block, '', file, 'heading');
    chat.querySelector('textarea').focus();
  };

  // Each step guarded on its own: one wire function throwing (old JS meeting
  // newer markup, a bad page, anything) must not kill the buttons after it —
  // that failure mode is exactly a page full of dead ➕ buttons (JL 260731).
  function safewire(fns) {
    fns.forEach(function (f) {
      try { f(); } catch (e) { console.warn('board wire failed:', e); }
    });
  }
  function rewire() {
    safewire([marks, paint, wireDadd, wireQBtns, wireStruct, wireXcal]);
    try {
      if (window.__boardWireSentenceChats) window.__boardWireSentenceChats();
    } catch (e) { console.warn('board wire failed:', e); }
  }
  window.__boardRewire = rewire;
  safewire([marks, paint, wireDadd, wireXcal]);
})();

/* ── live refresh (QD6, JL 260724) ─────────────────────────────────────────
   "when the chat changed something, refresh automatically — and my chat
   interface is still there." So: NEVER reload. Poll our own Last-Modified
   (both servers send it); when the file changes, fetch the new page and swap
   ONLY div.wrap. Everything the scripts appended to <body> — comment dock,
   chat drawer (mid-stream included), terminal, fab — stays alive. No Node,
   no framework: the drawer survives because it was never inside the content. */
(function () {
  var last = null, busy = false;
  function tick() {
    if (busy || document.hidden) return;
    fetch(location.pathname, { method: 'HEAD', cache: 'no-store' })
      .then(function (h) {
        var lm = h.headers.get('last-modified');
        if (!lm) return;
        if (last === null) { last = lm; return; }
        if (lm === last) return;
        // mid-selection = probably writing a comment on that text; hold the swap
        if (window.getSelection && String(window.getSelection())) return;
        // mid-TYPING（JL 260731「add discussion 打到一半，板一刷，字没了」）：
        // 换掉整个 .wrap 会把正在打的讨论/评论框连字带框一起扔掉。
        // 光标在 .wrap 里的输入框上，或任何框里有没保存的草稿 → 这一轮不换，
        // 4 秒后的下一轮再看。抽屉在 .wrap 外面，不受这条影响。
        var wrapEl = document.querySelector('div.wrap');
        if (wrapEl) {
          var ae = document.activeElement;
          if (ae && /^(TEXTAREA|INPUT)$/.test(ae.tagName) && wrapEl.contains(ae)) return;
          var drafts = wrapEl.querySelectorAll('textarea');
          for (var di = 0; di < drafts.length; di++) {
            if (drafts[di].value && drafts[di].value.trim()) return;
          }
        }
        busy = true;
        return fetch(location.pathname, { cache: 'no-store' })
          .then(function (r) { return r.text(); })
          .then(function (t) {
            var doc = new DOMParser().parseFromString(t, 'text/html');
            // The swap keeps THIS tab's scripts alive forever, so when the
            // BUILD's assets changed (three sessions shipped JS today while a
            // tab sat open, JL 260731), old JS would rewire new markup and die
            // silently — dead ➕ buttons. Different stamp = the one full reload.
            var theirs = doc.querySelector('meta[name="board-assets"]');
            var mine = document.querySelector('meta[name="board-assets"]');
            if (theirs && (!mine || mine.content !== theirs.content)) {
              // ⌨ 开着时不整页 reload（JL 260731「开一会儿它自己退了」的另一半）：
              // 挂个角标等着，终端一关（termView(false)）再 reload。
              // park 让 reload 后也能秒接，但正打着字被刷掉仍然是打断。
              var termOpen = document.body.classList.contains('termon');
              var chatRunning = document.body.classList.contains('chatbusy');
              if (!window.__pendingSince) window.__pendingSince = Date.now();
              // HARD CAP: holding the reload is a courtesy, not a promise. A
              // wedged turn must not pin the tab on stale JS indefinitely.
              var heldTooLong = Date.now() - window.__pendingSince > 90000;
              if ((termOpen || chatRunning) && !heldTooLong) {
                window.__pendingReload = 1;
                if (!document.getElementById('lrf-hold')) {
                  var b = document.createElement('div');
                  b.id = 'lrf-hold'; b.className = 'lrf';
                  b.textContent = termOpen
                    ? '↻ board updated — will reload when the terminal closes'
                    : '↻ board updated — will reload when this turn finishes';
                  document.body.appendChild(b);
                }
                return;
              }
              location.reload();
              return;
            }
            var nw = doc.querySelector('div.wrap');
            var old = document.querySelector('div.wrap');
            if (!nw || !old) return;
            var y = window.scrollY;
            // Carry the OPEN/CLOSED state of every drawer across the swap
            // (JL 260731: "even when a section is open, the change should be
            // smooth"). Without this, replacing div.wrap silently re-collapses
            // whatever the reader had opened, which reads as the page resetting
            // itself under them. Keyed by the drawer's own heading text, so it
            // survives a section moving up or down the page.
            var oldD = old.querySelectorAll('details');
            var openAt = [], openKey = {};
            oldD.forEach(function (d, i) {
              if (!d.open) return;
              openAt.push(i);
              var s = d.querySelector('summary');
              if (s) openKey[s.textContent.replace(/\s+/g, ' ').trim()] = 1;
            });
            old.replaceWith(nw);
            var newD = nw.querySelectorAll('details');
            if (newD.length === oldD.length) {
              // Same shape, so position is the exact identity: editing a
              // sentence does not add or remove drawers.
              openAt.forEach(function (i) { newD[i].open = true; });
            } else {
              // The page gained or lost a drawer, so fall back to the summary
              // text, which survives a section moving.
              newD.forEach(function (d) {
                var s = d.querySelector('summary');
                if (s && openKey[s.textContent.replace(/\s+/g, ' ').trim()]) d.open = true;
              });
            }
            if (window.__boardRewire) window.__boardRewire();
            // RE-BIND :target, or the swap silently returns you to the index.
            // The page router is pure CSS (`body:has(.q:target) .q:target`), and
            // :target binds to an ELEMENT, not to an id. Replacing div.wrap
            // destroys the section the hash pointed at; the fresh one carries the
            // same id but the browser never re-resolves the fragment, so nothing
            // matches, `.q{display:none}` hides every page and the index comes
            // back — with the hash still in the URL, which is why it reads as
            // "the refresh threw me out" rather than as a bug. Only a real
            // navigation re-resolves it; history.replaceState does not.
            // Verified in headless Chrome 260727 (JL).
            var h = location.hash;
            if (h) { location.hash = ''; location.hash = h; }
            window.scrollTo(0, y);
            last = lm;
            var n = document.createElement('div');
            n.className = 'lrf';
            n.textContent = '↻ board updated';
            document.body.appendChild(n);
            window.dispatchEvent(new CustomEvent('board:updated'));
            setTimeout(function () { n.remove(); }, 2200);
          });
      })
      .catch(function () {})
      .then(function () { busy = false; });
  }
  // instant, drawer-preserving refresh — what every former location.reload() now calls
  window.__boardRefresh = function () { if (last === null) last = '0'; tick(); };
  setInterval(tick, 4000);
})();

/* ── section「expand / collapse all」──────────────────────────────
   Pure enhancement over native <details>. Strip this block and every
   item is still individually openable; all text stays in the DOM. */
document.addEventListener('click', function (ev) {
  var b = ev.target.closest && ev.target.closest('.secall');
  if (!b) return;
  // The heading is now the section's own <summary>, so a click here would also
  // fold the section. Expand-all must not do that (JL 260725).
  ev.preventDefault();
  ev.stopPropagation();
  var sec = b.closest('.sect, .col, .f');
  if (!sec) return;
  var open = b.getAttribute('data-open') !== '1';
  sec.querySelectorAll('details.it').forEach(function (d) { d.open = open; });
  b.setAttribute('data-open', open ? '1' : '0');
  var lbl = b.querySelector('.lbl');
  if (lbl) lbl.textContent = open ? 'collapse all' : 'expand all';
});

/* ➕ sentence apparatus add (QA8, JL 260725): click a bare prose sentence, or the
   "➕ add to this sentence" row in an open drawer, and Save inserts `> Lane: text`
   directly under that sentence in the markdown (POST /_board/sentence). Script-only
   enhancement: without scripts the page still reads; writing needs serve.py anyway. */
(function () {
  var LANES = ['JL', 'CC', 'Note', 'Check', 'Citation', 'Value', 'Display',
               'Q-consumer', 'Link', 'Source'];
  var cur = null;
  function stamp() {
    var d = new Date(), z = function (n) { return (n < 10 ? '0' : '') + n; };
    return String(d.getFullYear()).slice(2) + z(d.getMonth() + 1) + z(d.getDate()) +
           ' ' + z(d.getHours()) + z(d.getMinutes());
  }
  function close() { if (cur) { cur.remove(); cur = null; } }
  function mk(afterEl, sentP, file) {
    close();
    var d = document.createElement('div');
    d.className = 'sadd';
    var sel = document.createElement('select');
    LANES.forEach(function (u) { sel.appendChild(new Option(u, u)); });
    try { sel.value = localStorage.getItem('board-sadd-last') || 'JL'; } catch (e) {}
    var inp = document.createElement('input');
    inp.type = 'text';
    inp.placeholder = 'Add to this sentence…';
    var ok = document.createElement('button'); ok.type = 'button'; ok.textContent = 'Save';
    var x = document.createElement('button'); x.type = 'button'; x.textContent = '✕';
    var err = document.createElement('span'); err.className = 'serr';
    d.append(sel, inp, ok, x, err);
    x.onclick = close;
    function save() {
      var text = inp.value.trim();
      if (!text) { inp.focus(); return; }
      try { localStorage.setItem('board-sadd-last', sel.value); } catch (e) {}
      err.textContent = '…';
      fetch('/_board/sentence', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: boardPath(), file: file,
          sentence: sentP.textContent.replace(/\s+/g, ' ').trim(),
          lane: sel.value, text: text })
      }).then(function (r) { return r.json(); })
        .then(function (j) {
          if (!j.ok) { err.textContent = '⚠ ' + (j.err || 'failed'); return; }
          err.textContent = '✔ saved';
          setTimeout(close, 700);
        })
        .catch(function () { err.textContent = '⚠ serve.py not running?'; });
    }
    ok.onclick = save;
    inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') save(); });
    afterEl.insertAdjacentElement('afterend', d);
    cur = d;
    inp.focus();
  }
  function edit(afterEl, sentP, file) {
    close();
    var before = sentP.textContent.replace(/\s+/g, ' ').trim();
    var d = document.createElement('div');
    d.className = 'sedit';
    var inp = document.createElement('textarea'); inp.value = before;
    inp.setAttribute('aria-label', 'Edit this sentence');
    var who = document.createElement('input'); who.maxLength = 4;
    who.value = (localStorage.getItem('board-user-last') || 'JL').toUpperCase();
    who.setAttribute('aria-label', 'Your initials');
    var ok = document.createElement('button'); ok.type = 'button'; ok.textContent = 'Save';
    var x = document.createElement('button'); x.type = 'button'; x.textContent = 'Cancel';
    var err = document.createElement('span'); err.className = 'serr';
    d.append(inp, who, ok, x, err);
    x.onclick = close;
    function save() {
      var replacement = inp.value.replace(/\s+/g, ' ').trim();
      var actor = who.value.toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 4) || 'JL';
      if (!replacement || replacement === before) { inp.focus(); return; }
      err.textContent = '…';
      fetch('/_board/edit-sentence', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: boardPath(), file: file, sentence: before,
          replacement: replacement, who: actor, when: stamp() })
      }).then(function (r) { return r.json(); }).then(function (j) {
        if (!j.ok) { err.textContent = '⚠ ' + (j.err || 'failed'); return; }
        localStorage.setItem('board-user-last', actor);
        location.reload();
      }).catch(function () { err.textContent = '⚠ serve.py not running?'; });
    }
    ok.onclick = save;
    inp.addEventListener('keydown', function (e) {
      if ((e.metaKey || e.ctrlKey) && e.key === 'Enter') save();
      if (e.key === 'Escape') close();
    });
    afterEl.insertAdjacentElement('afterend', d);
    cur = d; inp.focus(); inp.select();
  }
  function openSentenceComment(p, afterEl) {
    var q = p && p.closest('section.slide.q');
    if (!q) return;
    var det = p.closest('details.sent');
    if (det) {
      det.open = true;
      var target = det.querySelector('summary p');
      var sapp = Array.from(det.children).find(function (x) {
        return x.classList && x.classList.contains('sapp');
      });
      mk(det.querySelector('.saddrow') || sapp || p, target, q.dataset.file);
      return;
    }
    mk(afterEl || p, p, q.dataset.file);
  }
  function openSentenceEdit(p, afterEl) {
    var q = p && p.closest('section.slide.q');
    if (!q) return;
    var det = p.closest('details.sent');
    if (det) {
      det.open = true;
      var sapp = Array.from(det.children).find(function (x) {
        return x.classList && x.classList.contains('sapp');
      });
      edit(det.querySelector('.saddrow') || sapp || p, det.querySelector('summary p'),
           q.dataset.file);
      return;
    }
    edit(afterEl || p, p, q.dataset.file);
  }
  document.addEventListener('click', function (e) {
    if (e.target.closest('.sadd')) return;
    var row = e.target.closest('.saddrow');
    if (row) {
      var det = row.closest('details.sent');
      var qr = row.closest('section.slide.q');
      if (det && qr) mk(row, det.querySelector('summary p'), qr.dataset.file);
    }
  });
  // DOUBLE-click edits the sentence.  Adding a lane remains available from the
  // explicit ➕ row, so editing never competes with attaching evidence.
  document.addEventListener('dblclick', function (e) {
    if (e.target.closest('.sadd')) return;
    var p = e.target.closest('p');
    // `summary` is NOT excluded (JL 260727). `QA8@boardform` says double-click
    // opens the form on a BARE sentence and a drawer gets its own ➕ row, which is
    // a real second path — but it is only reachable once the drawer is already
    // open, so on a sentence that carries evidence the gesture people actually
    // learned did nothing at all, silently. As the evidence card becomes the
    // default that stops being an edge case: 116 of this board's sentences are
    // already drawers. So both shapes now answer the same gesture.
    // The other clauses still cover what `summary` stood in for: the sentence text
    // resolves to the inner `p`, the `.sbadge` has no `p` ancestor so `!p` catches
    // it, and a marker is a `<button>`.
    if (!p || e.target.closest('a,code,button,select,input,textarea,mark')) return;
    if (!p.closest('section.slide.q')) return;
    if (p.closest('.sapp,.bd,.cmt,.cmb,.qh,.dadd,.spine')) return;
    e.preventDefault();
    if (window.getSelection) window.getSelection().removeAllRanges();
    // WHERE the form goes differs by shape, and getting this wrong is silent.
    // `mk` does `afterEl.insertAdjacentElement('afterend', …)`, so passing the
    // summary's own `p` would drop the form INSIDE the <summary>, where every
    // click toggles the drawer and the inputs cannot be used. A drawer therefore
    // takes the same two arguments the ➕ row path uses: insert at the END OF THE
    // DRAWER BODY, while still naming the summary's sentence as the target line.
    openSentenceEdit(p, p);
  });
  // ⧉ copy a WHOLE SECTION (JL 260725: section-level, not per-sentence):
  // every section heading carries a copy button; it copies the section's full
  // text (folded drawers and item explanations included) as clean plain text —
  // no badges, no forms, no highlight formatting.
  document.querySelectorAll('section.slide.q .ch').forEach(function (ch) {
    if (ch.querySelector('.chcopy')) return;
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'chcopy'; b.textContent = '⧉';
    b.title = 'Copy this section as plain text';
    b.addEventListener('click', function (e) {
      e.preventDefault(); e.stopPropagation();
      var box = ch.closest('summary') ? ch.closest('details') : ch.parentElement;
      var c = box.cloneNode(true);
      c.querySelectorAll('.ch,.sadd,.saddrow,.sbadge,button,select,input,textarea,.dadd')
        .forEach(function (x) { x.remove(); });
      if (c.tagName === 'DETAILS') c.open = true;   // the section itself may be folded
      c.querySelectorAll('details').forEach(function (d) { d.open = true; });
      c.style.cssText = 'position:absolute;left:-99999px;top:0;width:800px';
      document.body.appendChild(c);
      var t = c.innerText.replace(/\n{3,}/g, '\n\n').trim();
      c.remove();
      function done() { b.textContent = '✓'; setTimeout(function () { b.textContent = '⧉'; }, 700); }
      function fallback() {
        var ta = document.createElement('textarea');
        ta.value = t; document.body.appendChild(ta); ta.select();
        try { document.execCommand('copy'); } catch (e2) {}
        ta.remove(); done();
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(t).then(done, fallback);
      } else fallback();
    });
    ch.appendChild(b);
  });
  document.querySelectorAll('details.sent>.sapp').forEach(function (ap) {
    var r = document.createElement('div');
    r.className = 'saddrow';
    r.textContent = '➕ add to this sentence';
    ap.appendChild(r);
  });

  /* Automatic Content addresses + sentence-specific chat.

     Only ## Content participates. C is a ### division. H is a terminal,
     addressable #### heading and never parents P/S in the address grammar.
     Paragraphs are siblings of headings inside C; each source-line paragraph
     currently carries one sentence, so its leaf is Pn.S1.

       QAb3.C1.H1       heading itself
       QAb3.C1.P2.S1    sentence in the second paragraph of C1

     These are render-local focus addresses, not durable Markdown identity. */
  function sentenceText(p) {
    var c = p.cloneNode(true);
    c.querySelectorAll('.sbadge,.cv,.schatbar,button,input,select,textarea')
      .forEach(function (x) { x.remove(); });
    return c.textContent.replace(/\s+/g, ' ').trim();
  }
  function apparatusText(p) {
    var box = null;
    var sent = p.closest('details.sent');
    if (sent) {
      box = Array.from(sent.children).find(function (x) {
        return x.classList && x.classList.contains('sapp');
      });
    } else {
      var opening = p.closest('details.qd');
      var body = opening && Array.from(opening.children).find(function (x) {
        return x.classList && x.classList.contains('qbd');
      });
      if (body) {
        box = Array.from(body.children).find(function (x) {
          return x.classList && x.classList.contains('sapp');
        });
      }
    }
    if (!box) return '';
    var c = box.cloneNode(true);
    c.querySelectorAll('.saddrow,.schatbar,button,input,select,textarea')
      .forEach(function (x) { x.remove(); });
    return c.innerText.replace(/\n{3,}/g, '\n\n').trim();
  }
  function directChild(parent, cls) {
    return Array.from(parent.children).find(function (x) {
      return x.classList && x.classList.contains(cls);
    }) || null;
  }
  function cleanLabel(el) {
    if (!el) return '';
    var c = el.cloneNode(true);
    c.querySelectorAll('.caddr,.haddr,.schatbar,button').forEach(function (x) {
      x.remove();
    });
    return c.textContent.replace(/\s+/g, ' ').trim();
  }
  function eligibleContentSentence(p, cbody) {
    if (p.closest('.cbody') !== cbody) return false;
    if (p.closest('.folds,.sapp,.cmt,.change,.lane,.lane-cont,.qh,.dadd,' +
                  '.sadd,.sedit,.spine,.nav,.gi,.idx')) return false;
    return !!sentenceText(p);
  }
  function wireSentenceChats() {
    document.querySelectorAll('.schatbar').forEach(function (x) { x.remove(); });
    document.querySelectorAll('.caddr,.haddr').forEach(function (x) { x.remove(); });
    document.querySelectorAll('p.sentence-target').forEach(function (p) {
      p.classList.remove('sentence-target');
      delete p.dataset.sentenceId;
      delete p.dataset.sentenceRef;
    });
    document.querySelectorAll('.csec[data-content-id]').forEach(function (c) {
      delete c.dataset.contentId;
      delete c.dataset.contentRef;
    });
    document.querySelectorAll('.ph[data-heading-id]').forEach(function (h) {
      h.classList.remove('heading-target');
      delete h.dataset.headingId;
      delete h.dataset.headingRef;
    });
    document.querySelectorAll('section.slide.q').forEach(function (sec) {
      var content = sec.querySelector('details.sect.content');
      if (!content) return;
      var divisions = Array.from(content.children).filter(function (x) {
        return x.matches && x.matches('details.csec');
      });
      divisions.forEach(function (csec, ci) {
        var contentId = 'C' + (ci + 1);
        var contentRef = sec.id + '.' + contentId;
        var summary = csec.querySelector(':scope > summary');
        var contentTitle = cleanLabel(summary);
        csec.dataset.contentId = contentId;
        csec.dataset.contentRef = contentRef;
        if (summary) {
          var caddr = document.createElement('span');
          caddr.className = 'caddr';
          caddr.textContent = contentId;
          caddr.title = 'Generated Content address: ' + contentRef;
          summary.appendChild(caddr);
        }
        var cbody = directChild(csec, 'cbody');
        if (!cbody) return;
        var nextH = 0, nextP = 0, headingPath = '';
        cbody.querySelectorAll('.ph,p').forEach(function (node) {
          if (node.closest('.cbody') !== cbody) return;
          if (node.classList.contains('ph')) {
            nextH += 1;
            var headingId = 'H' + nextH;
            var headingRef = contentRef + '.' + headingId;
            var headingTitle = cleanLabel(node);
            node.classList.add('heading-target');
            node.dataset.headingId = headingId;
            node.dataset.headingRef = headingRef;
            var haddr = document.createElement('span');
            haddr.className = 'haddr';
            haddr.textContent = headingId;
            haddr.title = 'Generated Heading address: ' + headingRef;
            node.appendChild(haddr);
            headingPath = headingId + (headingTitle ? ' · ' + headingTitle : '');
            return;
          }
          var p = node;
          if (!eligibleContentSentence(p, cbody)) return;
          nextP += 1;
          var shortId = contentId + '.P' + nextP + '.S1';
          var fullId = sec.id + '.' + shortId;
          var contentPath = contentId + (contentTitle ? ' · ' + contentTitle : '') +
            (headingPath ? '\n' + headingPath : '');
        p.classList.add('sentence-target');
        p.dataset.sentenceId = shortId;
        p.dataset.sentenceRef = fullId;

        var bar = document.createElement('span');
        bar.className = 'schatbar';
        bar.dataset.sentenceRef = fullId;
        var id = document.createElement('span');
        id.className = 'sidchip';
        id.textContent = shortId;
        id.title = 'Generated sentence address: ' + fullId;
        var comment = document.createElement('button');
        comment.type = 'button';
        comment.className = 'scomment';
        comment.textContent = '＋';
        comment.title = 'Comment on ' + fullId;
        comment.setAttribute('aria-label', 'Comment on sentence ' + fullId);
        comment.addEventListener('click', function (e) {
          e.preventDefault();
          e.stopPropagation();
          openSentenceComment(p, bar);
        });
        var chatButton = document.createElement('button');
        chatButton.type = 'button';
        chatButton.className = 'schat';
        chatButton.textContent = '💬';
        chatButton.title = 'Chat about ' + fullId;
        chatButton.setAttribute('aria-label', 'Chat about sentence ' + fullId);
        chatButton.addEventListener('click', function (e) {
          e.preventDefault();
          e.stopPropagation();
          var text = sentenceText(p);
          if (window.__boardSentenceChat) {
              window.__boardSentenceChat(
                sec, fullId, text, apparatusText(p), contentPath
              );
          }
        });
        var more = document.createElement('button');
        more.type = 'button';
        more.className = 'smore';
        more.textContent = '⋯';
        more.title = 'Actions for ' + fullId;
        more.setAttribute('aria-label', 'Actions for sentence ' + fullId);
        more.setAttribute('aria-expanded', 'false');
        var menu = document.createElement('div');
        menu.className = 'smenu';
        var menuRef = document.createElement('div');
        menuRef.className = 'smenu-ref';
        menuRef.textContent = fullId;
        function menuAction(label, cls, fn) {
          var action = document.createElement('button');
          action.type = 'button';
          action.className = cls;
          action.textContent = label;
          action.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            bar.classList.remove('menu-open');
            more.setAttribute('aria-expanded', 'false');
            fn();
          });
          menu.appendChild(action);
        }
        menu.appendChild(menuRef);
        menuAction('＋ Comment', 'sm-comment', function () {
          openSentenceComment(p, bar);
        });
        menuAction('💬 Chat', 'sm-chat', function () {
          if (window.__boardSentenceChat) {
              window.__boardSentenceChat(
                sec, fullId, sentenceText(p), apparatusText(p), contentPath
              );
          }
        });
        menuAction('✎ Edit', 'sm-edit', function () {
          openSentenceEdit(p, bar);
        });
        more.addEventListener('click', function (e) {
          e.preventDefault();
          e.stopPropagation();
          var open = !bar.classList.contains('menu-open');
          document.querySelectorAll('.schatbar.menu-open').forEach(function (x) {
            x.classList.remove('menu-open');
            var old = x.querySelector('.smore');
            if (old) old.setAttribute('aria-expanded', 'false');
          });
          bar.classList.toggle('menu-open', open);
          more.setAttribute('aria-expanded', open ? 'true' : 'false');
        });
        bar.addEventListener('click', function (e) {
          e.preventDefault();
          e.stopPropagation();
        });
        bar.append(id, comment, chatButton, more, menu);
        p.insertAdjacentElement('afterend', bar);
      });
      });
    });
  }

  /* ── Section and subsection breadcrumbs (QB5d) ────────────────────────────
     Above Content's fine `C.H.P.S` grammar sits a coarser address every reader
     can say out loud: `QB4e / Where we are / Decision Now`. Every rendered `##`
     section and `###` subsection heading gets one, at the END of the heading
     and invisible until that heading is hovered — the contract the sentence
     rail and the C/H chips already follow.

     The chip copies the address plus the markdown source path, so Claude Code
     can open the right file without guessing; `🤖` focuses THIS page's existing
     chat on that heading. Both are generated per render: nothing is written
     into the markdown, and a live refresh recomputes them because this runs
     inside the rewire below. */
  function plainLabel(el) {
    // An address is spoken and pasted, so it carries the NAME only: not the
    // heading's emoji, not its `1/7` progress count, not `· 6 sections`.
    var c = (el.querySelector(':scope > .chl') || el).cloneNode(true);
    c.querySelectorAll('.hpath,.chcopy,.caddr,.haddr,.shc,.cnt,button')
      .forEach(function (x) { x.remove(); });
    return c.textContent.replace(/\s+/g, ' ').trim()
      .replace(/^[^\p{L}\p{N}]+/u, '')
      .replace(/\s·\s\d+\s+\w+$/, '')
      .trim();
  }
  function blockOf(el) {
    // innerText needs layout, so the clone is measured off-screen and removed.
    var c = el.cloneNode(true);
    c.querySelectorAll('.hpath,.schatbar,.sadd,.saddrow,.dadd,button,select,input,textarea')
      .forEach(function (x) { x.remove(); });
    if (c.tagName === 'DETAILS') c.open = true;
    c.querySelectorAll('details').forEach(function (d) { d.open = true; });
    c.style.cssText = 'position:absolute;left:-99999px;top:0;width:800px';
    document.body.appendChild(c);
    var t = c.innerText.replace(/\n{3,}/g, '\n\n').trim();
    c.remove();
    return t.length > 1600 ? t.slice(0, 1600) + '\n…' : t;
  }
  function shRun(sh) {
    // A `###` outside Content is a flat `div.sh`; its block is the run of
    // siblings up to the next one.
    var box = document.createElement('div');
    box.appendChild(sh.cloneNode(true));
    var n = sh.nextElementSibling;
    while (n && !(n.classList && n.classList.contains('sh'))) {
      box.appendChild(n.cloneNode(true));
      n = n.nextElementSibling;
    }
    return box;
  }
  function copyInto(btn, text, label) {
    function done() {
      var old = btn.textContent;
      btn.textContent = label || '✓';
      setTimeout(function () { btn.textContent = old; }, 700);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, done);
      return;
    }
    var ta = document.createElement('textarea');
    ta.value = text; document.body.appendChild(ta); ta.select();
    try { document.execCommand('copy'); } catch (e) {}
    ta.remove(); done();
  }
  function headingRail(head, sec, path, file, blockEl, withCopy) {
    if (head.querySelector(':scope > .hpath')) return;
    var rail = document.createElement('span');
    rail.className = 'hpath';
    var chip = document.createElement('button');
    chip.type = 'button';
    chip.className = 'hpid';
    chip.textContent = path;
    chip.title = 'Copy this address' + (file ? '\n' + path + '\n' + file : '');
    chip.addEventListener('click', function (e) {
      e.preventDefault(); e.stopPropagation();
      copyInto(chip, path + (file ? ' · ' + file : ''), '✓ address copied');
    });
    rail.appendChild(chip);
    if (withCopy) {                 // `##` headings already carry their own ⧉
      var cp = document.createElement('button');
      cp.type = 'button';
      cp.className = 'hcopy';
      cp.textContent = '⧉';
      cp.title = 'Copy this subsection as plain text';
      cp.addEventListener('click', function (e) {
        e.preventDefault(); e.stopPropagation();
        copyInto(cp, blockOf(blockEl()), '✓');
      });
      rail.appendChild(cp);
    }
    var bot = document.createElement('button');
    bot.type = 'button';
    bot.className = 'hchat';
    bot.textContent = '🤖';
    bot.title = 'Chat about ' + path;
    bot.addEventListener('click', function (e) {
      e.preventDefault(); e.stopPropagation();
      if (window.__boardHeadingChat) {
        window.__boardHeadingChat(sec, path, blockOf(blockEl()), file);
      }
    });
    rail.appendChild(bot);
    head.appendChild(rail);
  }
  function ownHead(host) {
    return host ? host.querySelector(':scope > summary.ch, :scope > .ch') : null;
  }
  function wireHeadingPaths() {
    document.querySelectorAll('.hpath').forEach(function (x) { x.remove(); });
    document.querySelectorAll('section.slide.q').forEach(function (sec) {
      var file = sec.getAttribute('data-file') || '';
      var SECT = 'details.sect, details.diagram-section, details.qd';
      sec.querySelectorAll('.ch').forEach(function (ch) {
        var name = plainLabel(ch);
        if (!name) return;
        var box = ch.closest(SECT) || ch.parentElement || ch;
        headingRail(ch, sec, sec.id + ' / ' + name, file,
                    function () { return box; }, false);
      });
      function subPath(el) {
        var head = ownHead(el.closest(SECT + ', .folds'));
        var parent = head ? plainLabel(head) : '';
        return [sec.id, parent, plainLabel(el)].filter(Boolean).join(' / ');
      }
      sec.querySelectorAll('.sh').forEach(function (sh) {
        if (!plainLabel(sh)) return;
        headingRail(sh, sec, subPath(sh), file,
                    function () { return shRun(sh); }, true);
      });
      sec.querySelectorAll('details.csec > summary').forEach(function (sm) {
        if (!plainLabel(sm)) return;
        headingRail(sm, sec, subPath(sm), file,
                    function () { return sm.parentElement; }, true);
      });
    });
  }
  window.__boardWireSentenceChats = function () {
    wireSentenceChats();
    wireHeadingPaths();
  };
  wireSentenceChats();
  wireHeadingPaths();
  document.addEventListener('click', function () {
    document.querySelectorAll('.schatbar.menu-open').forEach(function (bar) {
      bar.classList.remove('menu-open');
      var more = bar.querySelector('.smore');
      if (more) more.setAttribute('aria-expanded', 'false');
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    close();
    document.querySelectorAll('.schatbar.menu-open').forEach(function (bar) {
      bar.classList.remove('menu-open');
      var more = bar.querySelector('.smore');
      if (more) more.setAttribute('aria-expanded', 'false');
    });
  });
})();

/* A chip inside a sentence's <summary> also toggles that sentence's drawer on
   its way to opening its own panel. That is left alone ON PURPOSE.

   The first version called e.preventDefault() here to stop the drawer flapping.
   Showing a popover IS the button's default action, so that cancelled the panel
   as well: on every sentence carrying a `>` lane, clicking a chip did nothing at
   all. A cosmetic guard silently disabled the feature it was decorating, and it
   only showed up on the composite example, where every chip sits in a lane.

   Opening the drawer is not a defect anyway: the lane under the sentence holds
   the same evidence the panel is about, so getting both is better than either.
   If this ever does need suppressing, it must NOT use preventDefault; restore
   `details.open` on the next animation frame instead. */

/* AND THE REAL CAUSE WAS NEITHER OF THOSE (JL 260726: "for the values,
   displays, figures, I cannot click them"). No handler belongs here at all.

   The story this file told for one revision was wrong, and the measurement
   that killed it is worth keeping: with a click handler added to force the
   panel open, chips inside a <summary> opened; with it removed, they ALSO
   opened. So <summary> was never swallowing anything, and element.click()
   was the wrong instrument, because it skips hit-testing. Testing what a real
   MOUSE would hit found 11 of 11 chips unreachable: `.fig`, meant for markdown
   images, also matched every figure PANEL (class `chipcard disp fig ready`),
   and its display:block beat the UA rule that hides a closed popover. Five
   invisible full-width panels sat over the page eating every click.

   Fixed in board.css by scoping that rule to `img.fig`, plus an explicit
   `.chipcard:not(:popover-open){display:none}` so no future class collision
   can resurrect a ghost. The chip needs NO script: `popovertarget` alone is
   enough, inside a <summary> or out of it, verified in Chrome 150. */

/* ── QD8 · activity timing and layout ───────────────────────────────────
   Timing is runtime data, so it is enhancement-only by definition. The static
   shell above still explains the measurement when this script or serve.py is
   absent. HEAD polling never counts as activity. Only a visible, non-idle span
   sends heartbeats, and the server stores completed seconds outside Git. */
(function () {
  var PULSE = 30000, IDLE = 5 * 60 * 1000;
  var span = '', seq = 0, lastAction = Date.now(), changed = false;
  var tab = '', spanContext = null, idleTimer = null;
  try {
    tab = sessionStorage.getItem('board-activity-tab') || '';
    if (!tab) {
      tab = (crypto.randomUUID ? crypto.randomUUID() :
        Date.now().toString(36) + Math.random().toString(36).slice(2));
      sessionStorage.setItem('board-activity-tab', tab);
    }
  } catch (e) {
    tab = Date.now().toString(36) + Math.random().toString(36).slice(2);
  }

  function escAct(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
    });
  }
  function fmtAct(sec) {
    sec = Math.max(0, Math.round(Number(sec) || 0));
    if (sec < 60) return sec ? '<1m' : '0m';
    var min = Math.round(sec / 60);
    if (min < 60) return min + 'm';
    var h = Math.floor(min / 60), rem = min % 60;
    return h + 'h' + (rem ? ' ' + rem + 'm' : '');
  }
  function context() {
    var id = (location.hash || '').slice(1);
    var row = null;
    document.querySelectorAll('a.ir[href^="#"]').forEach(function (r) {
      if (r.getAttribute('href') === '#' + id) row = r;
    });
    if (!row) return { page: 'board', group: '', title: 'Whole board' };
    var p = row.previousElementSibling;
    while (p && !p.classList.contains('grp')) p = p.previousElementSibling;
    return {
      page: (row.querySelector('.i') || {}).textContent || id,
      group: p ? p.getAttribute('data-g') || '' : '',
      title: (row.querySelector('.t') || {}).textContent || id
    };
  }
  function actor() {
    try { return localStorage.getItem('board-user-last') || 'JL'; }
    catch (e) { return 'JL'; }
  }
  function payload(op, active, reason, activeUntil) {
    var c = spanContext || context();
    var p = {
      op: op, path: boardPath(), span: span, page: c.page,
      group: c.group, title: c.title, actor: actor(),
      active: active !== false, changed: changed, reason: reason || ''
    };
    if (activeUntil) p.active_until = activeUntil / 1000;
    return p;
  }
  function status(text, cls) {
    var s = document.getElementById('activity-status');
    if (!s) return;
    s.textContent = text;
    s.className = 'act-status' + (cls ? ' ' + cls : '');
  }
  function post(p, beacon) {
    var raw = JSON.stringify(p);
    if (beacon && navigator.sendBeacon) {
      navigator.sendBeacon('/_board/activity',
        new Blob([raw], { type: 'application/json' }));
      return;
    }
    fetch('/_board/activity', {
      method: 'POST', headers: {'Content-Type':'application/json'}, body: raw
    }).then(function (r) {
      if (!r.ok) throw new Error(String(r.status));
      return r.json();
    }).then(function (data) {
      if (p.changed && p.span === span) changed = false;
      render(data);
    }).catch(function () {
      status('timing unavailable', '');
    });
  }
  function begin() {
    if (span || document.hidden) return;
    spanContext = context();
    span = tab + ':' + (++seq) + ':' + Date.now().toString(36);
    post(payload('start', true), false);
    scheduleIdle();
  }
  function clearIdle() {
    if (idleTimer) window.clearTimeout(idleTimer);
    idleTimer = null;
  }
  function scheduleIdle() {
    clearIdle();
    if (!span || document.hidden) return;
    var due = lastAction + IDLE;
    idleTimer = window.setTimeout(function stopAtIdleBoundary() {
      idleTimer = null;
      if (!span || document.hidden) return;
      if (Date.now() < due) {
        scheduleIdle();
        return;
      }
      finish(false, 'idle', due);
      status('paused', '');
    }, Math.max(0, due - Date.now()));
  }
  function finish(beacon, reason, activeUntil) {
    if (!span) return;
    var p = payload('stop', true, reason || 'stop', activeUntil);
    span = '';
    spanContext = null;
    changed = false;
    clearIdle();
    post(p, beacon);
  }
  function pulse() {
    if (document.hidden || Date.now() - lastAction >= IDLE) {
      finish(false, document.hidden ? 'hidden' : 'idle',
        document.hidden ? 0 : lastAction + IDLE);
      status('paused', '');
      return;
    }
    if (!span) begin();
    else post(payload('pulse', true), false);
  }
  function touch() {
    lastAction = Date.now();
    if (!span && !document.hidden) begin();
    else scheduleIdle();
  }
  ['pointerdown','keydown','wheel','touchstart','scroll'].forEach(function (name) {
    window.addEventListener(name, touch, { passive: true });
  });
  window.addEventListener('hashchange', function () {
    finish(false, 'page-change'); lastAction = Date.now(); begin();
  });
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) finish(true, 'hidden');
    else { lastAction = Date.now(); begin(); }
  });
  window.addEventListener('pagehide', function () { finish(true, 'pagehide'); });
  window.addEventListener('board:updated', function () {
    changed = true;
    if (span) post(payload('pulse', true), false);
  });

  /* ── the dashboard counts UPDATES, not time (QD8 -> QC2, JL 260726) ──────
     "I don't care about the time. What I care is about the numbers of
     updates." One update = one dated line in one page's ## Log. That unit is
     written by whoever did the work in whatever tool, so it sees the days a
     browser timer structurally could not: most work on these boards arrives
     through Claude Code, and the timer only ever watched a tab. */
  function sampleData() {
    var title = (document.querySelector('.h1') || {}).textContent || 'This board';
    var path = boardDirPath().replace(/^\//, '');
    var vals = [0,0,0,4,11,0,7,22,9,0,14,31,18,26];
    var days = [], now = new Date();
    vals.forEach(function (v, i) {
      var d = new Date(now); d.setDate(now.getDate() - 13 + i);
      var key = d.getFullYear() + '-' + String(d.getMonth()+1).padStart(2,'0') +
        '-' + String(d.getDate()).padStart(2,'0');
      days.push({ day:key, updates:v, here:Math.round(v * .6) });
    });
    return {
      sample: true, unit: 'updates', days: days,
      totals: {today:26, week:89, updates:142, boards:3, pages:24},
      boards: [
        {board:path,title:title,updates:86,days:5,pages:12,last:days[13].day},
        {board:'sample/paper',title:'Paper lifecycle',updates:38,days:3,pages:8,last:days[12].day},
        {board:'sample/data',title:'CMS store',updates:18,days:2,pages:4,last:days[10].day}
      ],
      current: {
        board:path,title:title,updates:86,days:5,pages:12,last:days[13].day,
        groups:[
          {group:'QA · Defining a board',updates:44,
           pages:[
             {page:'QA4',title:'Shared Q/S Page Layout',updates:26,last:days[13].day},
             {page:'QA2',title:'Shared Q/S source template',updates:18,last:days[12].day}
           ]},
          {group:'QD · Working on the board',updates:28,
           pages:[{page:'QD2',title:'SDK version: the chat box',updates:28,last:days[11].day}]},
          {group:'QC · Index and structure',updates:14,
           pages:[{page:'QC2',title:'Index page design',updates:14,last:days[13].day}]}
        ]
      }
    };
  }
  function agoAct(day) {
    if (!day) return '';
    var d = Math.round((new Date().setHours(0,0,0,0) -
      new Date(day + 'T00:00:00').getTime()) / 86400000);
    return d <= 0 ? 'today' : d === 1 ? 'yesterday' : d + 'd ago';
  }
  function rowHtml(kind, name, updates, max, meta, current) {
    var f = max ? Math.max(1, updates / max * 100) : 0;
    return '<div class="act-row ' + kind + (current ? ' current' : '') +
      '" title="' + escAct(name + ': ' + updates + ' update' +
      (updates === 1 ? '' : 's') + (meta ? ' · ' + meta : '')) + '">' +
      '<span class="act-name">' + escAct(name) + '</span>' +
      '<span class="act-track" style="--focus:' + f.toFixed(2) +
      ';--changed:0"><i class="act-focus"></i></span>' +
      '<span class="act-time">' + updates + '</span></div>';
  }
  function render(raw) {
    var body = document.getElementById('activity-body');
    if (!body) return;
    var data = raw;
    if (!data || !data.totals || Number(data.totals.updates || 0) < 1) data = sampleData();
    status(data.sample ? 'layout preview · no logs read' : 'counting · ## Log',
      data.sample ? 'sample' : 'live');
    var t = data.totals, dayMax = Math.max.apply(null, data.days.map(function (d) {
      return Number(d.updates || 0);
    }).concat([1]));
    var days = data.days.map(function (d) {
      var n = Number(d.updates || 0), h = Number(d.here || 0);
      var f = n / dayMax * 100, c = h / dayMax * 100;
      var date = new Date(d.day + 'T12:00:00');
      var label = ['S','M','T','W','T','F','S'][date.getDay()] + d.day.slice(8);
      return '<div class="act-day" title="' + escAct(d.day + ': ' + n +
        ' update' + (n === 1 ? '' : 's') + ' across all boards, ' + h +
        ' on this one') + '">' +
        '<span class="act-day-n' + (n ? '' : ' zero') + '">' +
        escAct(n ? String(n) : '·') + '</span>' +
        '<div class="act-day-bars" style="--focus:' + f.toFixed(2) +
        ';--changed:' + c.toFixed(2) + '"><i class="act-day-focus"></i>' +
        '<i class="act-day-changed"></i>' +
        (h && h !== n ? '<span class="act-day-here">' + escAct(String(h)) +
         '</span>' : '') + '</div>' +
        '<span class="act-day-label">' + escAct(label) + '</span></div>';
    }).join('');
    var boardMax = Math.max.apply(null, data.boards.map(function (b) {
      return Number(b.updates || 0);
    }).concat([1]));
    var boards = data.boards.slice(0, 6).map(function (b) {
      return rowHtml('board', b.title, Number(b.updates || 0), boardMax,
        b.pages + ' pages · ' + b.days + ' active days · last ' + agoAct(b.last),
        b.board === data.current.board);
    }).join('');
    var groupMax = Math.max.apply(null, (data.current.groups || []).map(function (g) {
      return Number(g.updates || 0);
    }).concat([1]));
    var groups = (data.current.groups || []).map(function (g) {
      var html = rowHtml('group', g.group, Number(g.updates || 0), groupMax,
        (g.pages || []).length + ' pages', false);
      (g.pages || []).forEach(function (p) {
        html += rowHtml('page', p.page + ' · ' + p.title, Number(p.updates || 0),
          groupMax, 'last ' + agoAct(p.last), false);
      });
      return html;
    }).join('');
    body.innerHTML =
      '<div class="act-metrics">' +
      '<div class="act-metric"><b>' + Number(t.today || 0) + '</b><span>updates today</span></div>' +
      '<div class="act-metric"><b>' + Number(t.week || 0) + '</b><span>last 7 days</span></div>' +
      '<div class="act-metric"><b>' + Number(t.updates || 0) + '</b><span>all boards</span></div>' +
      '<div class="act-metric"><b>' + Number(t.boards || 0) + '</b><span>boards with a log</span></div>' +
      '<div class="act-metric"><b>' + Number(t.pages || 0) + '</b><span>pages ever updated</span></div>' +
      '</div>' +
      '<div class="act-block"><div class="act-block-head"><b>Last 14 days</b>' +
      '<span class="act-legend"><i></i>all boards <i class="changed"></i>this board</span></div>' +
      '<div class="act-days">' + days + '</div></div>' +
      '<div class="act-block"><div class="act-block-head"><b>Across boards</b>' +
      '<span class="act-legend">top 6 · every ## Log line ever</span></div><div class="act-tree">' +
      boards + '</div></div>' +
      '<div class="act-block"><div class="act-block-head"><b>This board: Group → Page</b>' +
      '<span class="act-legend">' + Number(data.current.updates || 0) +
      ' updates</span></div><div class="act-tree">' + groups + '</div></div>' +
      (data.sample ? '<p class="act-empty">Preview data shows the layout only. It disappears once any page carries a dated ## Log line.</p>' : '');
  }


  status('reading logs', '');
  begin();
  setInterval(pulse, PULSE);
})();


/* ── Pages sidebar: toggle, per-board persistence, active row (JL 260731) ── */
(function () {
  var sb = document.getElementById('sidebar');
  var bt = document.getElementById('sbtoggle');
  if (!sb || !bt) return;
  var key = 'bnav:' + (document.body.dataset.board || '');
  function apply(state) {
    document.body.classList.toggle('nav-open', state === 'open');
    document.body.classList.toggle('nav-closed', state === 'closed');
  }
  try {
    var saved = localStorage.getItem(key);
    if (saved) apply(saved);
  } catch (e) {}
  bt.addEventListener('click', function () {
    var state = sb.getBoundingClientRect().right > 30 ? 'closed' : 'open';
    apply(state);
    try { localStorage.setItem(key, state); } catch (e) {}
  });
  /* On narrow screens the rail overlays the text: a jump closes it (not
     persisted, so a wide screen later still opens by default). */
  sb.addEventListener('click', function (e) {
    var x = e.target.closest('.sb-x');
    if (x) {
      /* The hidden ▸ at the row's end toggles that page's outline
         (JL 260731); the accordion holds: at most one outline open. */
      e.preventDefault();
      var row = x.closest('a.sb-p,a.sb-top');
      var o = row && sb.querySelector(
        '.sb-out[data-out="' + (row.getAttribute('href') || '').slice(1) + '"]');
      var was = o && o.classList.contains('open');
      sb.querySelectorAll('.sb-out.open').forEach(function (q) {
        q.classList.remove('open');
      });
      if (o && !was) o.classList.add('open');
      return;
    }
    var p = e.target.closest('a.sb-p,a.sb-top');
    if (p && p.getAttribute('href') === location.hash) {
      /* Re-clicking the open page's row returns to its top (JL 260731);
         a cross-page click already lands at the top via :target. */
      e.preventDefault();
      var page = document.getElementById(location.hash.slice(1));
      if (page) page.scrollIntoView({ block: 'start' });
      return;
    }
    if (e.target.closest('a') && window.innerWidth < 1150) apply('closed');
  });
  function mark() {
    var want = location.hash || '#top';
    var on = null;
    sb.querySelectorAll('a.sb-top,a.sb-g,a.sb-p').forEach(function (a) {
      var hit = a.getAttribute('href') === want;
      a.classList.toggle('on', hit);
      if (hit) on = a;
    });
    /* Accordion (QB2a, JL 260731): only the open page's outline shows. */
    sb.querySelectorAll('.sb-out.open').forEach(function (o) {
      o.classList.remove('open');
    });
    var out = on && sb.querySelector('.sb-out[data-out="' + want.slice(1) + '"]');
    if (out) out.classList.add('open');
    if (on) on.scrollIntoView({ block: 'nearest' });
  }
  /* An outline row opens its page (the anchor's own navigation), then opens
     and scrolls to the section once :target has applied. */
  var SEL = { diagram: 'details.diagram-section', content: 'details.sect.content',
              items: 'details.sect.goal', now: 'details.sect.now',
              files: 'details.sect.fls',
              /* the Index's own components (QB2a): #top is the wrap, so the
                 same page.querySelector path resolves them */
              map: 'details.board-map', status: 'details.board-status',
              pages: '#qlist', activity: '#activity' };
  sb.addEventListener('click', function (e) {
    var a = e.target.closest('a.sb-s,a.sb-ss');
    if (!a) return;
    var pid = (a.getAttribute('href') || '').slice(1);
    setTimeout(function () {
      var page = document.getElementById(pid);
      if (!page) return;
      var el = SEL[a.dataset.k] ? page.querySelector(SEL[a.dataset.k]) : null;
      if (el && a.dataset.div !== undefined) {
        var divs = Array.prototype.filter.call(el.children, function (x) {
          return x.matches && x.matches('details.csec') &&
                 x.className.indexOf('display') < 0;
        });
        var d = divs[+a.dataset.div];
        if (d) { el.open = true; d.open = true; el = d; }
      } else if (el && a.dataset.t) {
        /* a non-Content subsection (### Decision Now …) is found by its
           rendered .sh heading text */
        var m = a.dataset.t.trim().toLowerCase();
        var hs = el.querySelectorAll('.sh');
        for (var i = 0; i < hs.length; i++) {
          if (hs[i].textContent.trim().toLowerCase().indexOf(m) === 0) {
            el.open = true;
            el = hs[i];
            break;
          }
        }
      }
      if (el) {
        if (el.tagName === 'DETAILS') el.open = true;
        el.scrollIntoView({ block: 'start' });
      } else {
        page.scrollIntoView({ block: 'start' });
      }
    }, 80);
  });
  window.addEventListener('hashchange', mark);
  mark();
})();

/* ── SECTION MATRIX cells open their page at the named section (QB2). ── */
(function () {
  var bs = document.querySelector('.board-status');
  if (!bs) return;
  var SEL = { diagram: 'details.diagram-section', content: 'details.sect.content',
              items: 'details.sect.goal', now: 'details.sect.now',
              files: 'details.sect.fls', folds: '.folds' };
  bs.addEventListener('click', function (e) {
    var a = e.target.closest('a[data-k]');
    if (!a) return;
    setTimeout(function () {
      var page = document.getElementById((a.getAttribute('href') || '').slice(1));
      if (!page) return;
      var el = SEL[a.dataset.k] ? page.querySelector(SEL[a.dataset.k]) : null;
      if (el) {
        if (el.tagName === 'DETAILS') el.open = true;
        el.scrollIntoView({ block: 'start' });
      }
    }, 80);
  });
})();

/* ── board/ tree navigation (QC9, JL 260731) ───────────────────────────────
   In the tree each page is its own document, so a plain link click is a real
   navigation and a real navigation destroys the chat drawer and the terminal,
   which is the exact failure QD4's parked-outside-the-wrap design exists to
   avoid. So in site mode we intercept internal links, fetch the target, swap
   ONLY div.wrap, and pushState. The drawer never notices it moved.

   With scripts off every link is still an ordinary href, so the tree stays
   fully navigable and the strip-scripts invariant holds. */
(function () {
  if (!document.body.classList.contains('split')) return;  // single-file mode
  var busy = false, pending = null;

  function samesite(a) {
    if (!a || !a.getAttribute) return false;
    var href = a.getAttribute('href') || '';
    if (!href || href[0] === '#' || /^[a-z]+:/i.test(href)) return false;
    if (a.target === '_blank') return false;
    return /\.html(\?|#|$)/.test(href);
  }

  async function go(url, push) {
    /* Dropping a navigation that arrives mid-swap loses it for good: the second
       of two quick clicks does nothing, and Back pressed during a swap moves
       the URL while the content stays put (both reproduced in headless Chrome
       260731). Hold the latest request and run it when this one lands. */
    if (busy) { pending = [url, push]; return; }
    busy = true;
    try {
      var r = await fetch(url, { cache: 'no-store' });
      var doc = new DOMParser().parseFromString(await r.text(), 'text/html');
      var nw = doc.querySelector('div.wrap'), old = document.querySelector('div.wrap');
      if (!nw || !old) { location.href = url; return; }
      old.replaceWith(nw);
      document.title = doc.title || document.title;
      if (push) history.pushState({ board: 1 }, '', url);
      window.scrollTo(0, 0);
      if (window.__boardRewire) window.__boardRewire();
      window.dispatchEvent(new CustomEvent('board:updated'));
    } catch (e) {
      location.href = url;          // a failed swap must still navigate
    } finally {
      busy = false;
      if (pending) { var p = pending; pending = null; go(p[0], p[1]); }
    }
  }

  document.addEventListener('click', function (e) {
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button) return;
    var a = e.target.closest && e.target.closest('a');
    if (!samesite(a)) return;
    e.preventDefault();
    go(a.href, true);
  });

  window.addEventListener('popstate', function () { go(location.href, false); });
})();

/* Rail drag-to-resize (JL 260731: "can the left panel be dragged, it feels
   fixed"). Same shape the chat drawer uses for --chatw: one CSS variable, a
   handle on the edge that sets it, and the width remembered per machine.
   Pure enhancement, so with scripts off the rail keeps its default width. */
(function () {
  var KEY = 'board-sidebar-width';
  function setW(px) {
    px = Math.max(150, Math.min(px, Math.round(window.innerWidth * 0.6)));
    document.documentElement.style.setProperty('--sbw', px + 'px');
    try { localStorage.setItem(KEY, String(px)); } catch (e) {}
  }
  var saved = parseInt(localStorage.getItem(KEY) || '', 10);
  if (saved) setW(saved);
  function wire() {
    var rz = document.querySelector('.sbrz');
    if (!rz || rz.dataset.wired) return;
    rz.dataset.wired = '1';
    rz.addEventListener('pointerdown', function (e) {
      e.preventDefault();
      rz.setPointerCapture(e.pointerId);
      document.body.style.userSelect = 'none';
      var move = function (ev) { setW(ev.clientX); };
      var up = function () {
        rz.removeEventListener('pointermove', move);
        rz.removeEventListener('pointerup', up);
        rz.removeEventListener('pointercancel', up);
        document.body.style.userSelect = '';
      };
      rz.addEventListener('pointermove', move);
      rz.addEventListener('pointerup', up);
      rz.addEventListener('pointercancel', up);
    });
    // double-click the handle to snap back to the default
    rz.addEventListener('dblclick', function () {
      document.documentElement.style.removeProperty('--sbw');
      try { localStorage.removeItem(KEY); } catch (e) {}
    });
  }
  wire();
  window.addEventListener('board:updated', wire);   // survives a live swap
})();

/* ── the reload must not cost you your place (QD2/QD6, JL 260731) ──────────
   Two reports, one cause. When BUILD ships new assets, the tab must take the
   new JS, and the asset-stamp guard reloads it — deferred while a turn runs,
   so it lands the moment the turn ends. A full reload destroys the drawer's
   transcript ("第二个 talk 的时候 thinking 都不见了") and re-collapses every
   section you had opened ("我一旦打开它，它就应该一直在那，直到我选择把它关上").
   The reload itself is right: stale JS wiring new markup is worse. So make it
   lossless instead: remember what was open before unload, put it back after.
   Sections persist across sessions because that is what "until I close it"
   means; the drawer's open/closed state is per tab, like the tab itself. */
(function () {
  var DK = 'board-open:' + location.pathname;     // sections, sticky
  var CK = 'board-drawer:' + location.pathname;   // drawer, this tab only

  function key(d) {
    var s = d.querySelector('summary');
    return s ? s.textContent.replace(/\s+/g, ' ').trim() : '';
  }
  function save() {
    try {
      var open = [];
      document.querySelectorAll('div.wrap details[open]').forEach(function (d) {
        var k = key(d); if (k) open.push(k);
      });
      localStorage.setItem(DK, JSON.stringify(open));
      sessionStorage.setItem(CK, JSON.stringify({
        on: !!(window.__boardDrawerOpen && window.__boardDrawerOpen()),
        term: !!(window.__boardTermOn && window.__boardTermOn()),
        y: Math.round(window.scrollY)
      }));
    } catch (e) {}
  }
  function restoreSections() {
    var want = {}, n = 0;
    try { (JSON.parse(localStorage.getItem(DK)) || []).forEach(function (k) { want[k] = 1; n++; }); }
    catch (e) { return; }
    if (!n) return;
    document.querySelectorAll('div.wrap details').forEach(function (d) {
      if (want[key(d)]) d.open = true;
    });
  }

  /* LOAD ONLY. Replaying the drawer on every router swap would fight the user:
     close it, navigate, and the saved "it was open" would reopen it. A swap is
     not a new page load, and `follow()` already keeps an open drawer bound. */
  function restoreDrawer() {
    var st;
    try { st = JSON.parse(sessionStorage.getItem(CK) || 'null'); } catch (e) { st = null; }
    if (!st) return;
    if (st.y) window.scrollTo(0, st.y);
    /* Reopening replays this page's saved log, so the conversation comes back
       even though the live trace of the interrupted turn cannot. */
    if (st.on && window.__boardDrawerReopen) {
      try {
        var opened = window.__boardDrawerReopen();
        /* A parked PTY is still running, so a drawer that comes back showing the
           chat box is showing the wrong half of QD1's one-session-per-page Law.
           Reattach to the terminal if one is genuinely still alive; the check
           lives in __boardTermReopen so a reload never SPAWNS one. */
        if (st.term && window.__boardTermReopen) {
          Promise.resolve(opened).then(function () {
            try { window.__boardTermReopen(); } catch (e) {}
          });
        }
      } catch (e) {}
    }
  }

  window.addEventListener('pagehide', save);      // fires on reload AND on close
  window.addEventListener('beforeunload', save);
  /* Saving ONLY at unload leaves one gap that reads as the feature not working
     at all (JL 260801, twice): a tab running JS from before this block existed
     never wrote anything, so the FIRST refresh after it opened the drawer has
     nothing to restore from, and only the second one works. Some mobile
     browsers also drop `beforeunload` entirely. So record the drawer the moment
     it opens or closes: one class flip on #chat, watched directly, no coupling
     to the chat code. */
  var chatEl = document.getElementById('chat');
  if (window.MutationObserver) {
    var watch = new MutationObserver(save);
    if (chatEl) watch.observe(chatEl, { attributes: true, attributeFilter: ['class'] });
    /* <body> too, and not as belt-and-braces: opening the terminal toggles
       `termon` on BODY and touches nothing on #chat, so watching only the
       drawer meant the terminal view was never recorded when it opened, and
       the flag existed only if `pagehide` happened to run (JL 260801: "still
       the same problem, when I refresh it switches from terminal to GUI"). */
    watch.observe(document.body, { attributes: true, attributeFilter: ['class'] });
  }
  window.addEventListener('board:updated', restoreSections);
  restoreSections();
  restoreDrawer();
})();
