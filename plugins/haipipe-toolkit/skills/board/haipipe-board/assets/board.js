/* ─────────────────────────────────────────────────────────────
   Comment layer — PURE ENHANCEMENT. The prose is already real HTML;
   this script only ADDS "select -> comment -> highlight right away".
   Strip this script block and the board still reads fine (just no commenting).

   Comments live in localStorage until you press "Sync to md", which writes
   them into each Q file's ## Discussion as:   > JL 「quoted sentence」: text
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
      if (p.closest && p.closest('.folds, .qh, .nav, pre')) continue;
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
      var r = live.getBoundingClientRect();
      pend = { id: q.id, file: q.getAttribute('data-file') || '',
               quote: txt, range: live.cloneRange() };
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
    db.push({ id: pend.id, file: pend.file, quote: pend.quote, who: who, text: v });
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
  /* md 里一条评论长这样，[ ] 未解决 / [x] 已解决 */
  function line(c) {
    return '- [ ] ' + c.who + ' 「' + c.quote.replace(/\s+/g, ' ').trim() +
           '」 · ' + (c.when || stamp()) + '\n      ' + c.text.replace(/\n/g, '\n      ');
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
      '<button class="cf">Connect folder</button>' +
      '<button class="cp">Copy</button></div>' +
      (db.length ? db.map(function (c, i) {
        return '<div class="it" data-row="' + i + '"><div class="q">' + c.id +
          (c.lost ? ' <span style="color:var(--mut)">· unanchored</span> ' : ' ') +
          '“' + esc(c.quote.slice(0, 40)) + '”</div><b>' + c.who + '</b> ' +
          esc(c.text) + ' <button data-i="' + i +
          '" class="rm" style="padding:2px 8px">del</button></div>';
      }).join('') : '<div class="it mut">Nothing yet. Select a sentence in the text.</div>') +
      '<div class="hint">Comments are written to the <code>.md</code> the moment you save — ' +
      'once you have connected this board’s folder. Anything listed above has NOT been ' +
      'written yet. ' +
      'each comment into its Q file under <code>## Comments</code> as ' +
      '<code>- [ ] WHO 「quote」 · time</code> — flip it to <code>[x]</code> when solved. ' +
      'Re-run <code>python3 build.py</code> afterwards.</div>';
    panel.querySelectorAll('.rm').forEach(function (b) {
      b.onclick = function () { db.splice(+b.getAttribute('data-i'), 1); save(); };
    });
    panel.querySelector('.sy').onclick = sync;
    panel.querySelector('.cf').onclick = async function () {
      dirH = null; await putDir(undefined);
      var d = await ensureDir(true);
      say(d ? 'Folder connected — comments now save straight to the .md' : 'Not connected');
      if (d) drain(false);
    };
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
    payload.path = location.pathname;
    var r = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' },
                               body: JSON.stringify(payload) });
    if (r.status === 404 || r.status === 501) { srvOK = false; return null; }
    srvOK = true;
    return await r.json();
  }
  async function srvComment(c) {
    try {
      var j = await post('/_board/comment',
        { file: c.file, who: c.who, quote: c.quote, text: c.text, when: c.when || stamp() });
      if (!j) return null;
      return j.ok ? true : j.err;
    } catch (e) { srvOK = false; return null; }
  }
  async function srvResolve(file, quote, done) {
    try {
      var j = await post('/_board/resolve', { file: file, quote: quote, done: done });
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
  function insertComments(txt, add) {
    if (/^## Comments[^\n]*$/m.test(txt))
      return txt.replace(/^## Comments[^\n]*\n/m, function (mm) { return mm + add + '\n'; });
    if (/\n## Log\b/.test(txt))
      return txt.replace(/\n## Log\b/, '\n## Comments\n' + add + '\n\n## Log');
    return txt.replace(/\s*$/, '') + '\n\n## Comments\n' + add + '\n';
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
    var dir = await ensureDir(ask);
    if (!dir) return 0;
    var by = {}, done = 0;
    db.forEach(function (c) { (by[c.file] = by[c.file] || []).push(c); });
    for (var f in by) {
      var add = by[f].map(line).join('\n');
      try {
        await edit(dir, f, function (txt) { return insertComments(txt, add); });
        by[f].forEach(function (c) { c.written = 1; });
        done += by[f].length;
      } catch (e) { console.log('[board] ' + f + ': ' + e.message); }
    }
    db = db.filter(function (c) { return !c.written; });
    localStorage.setItem(KEY, JSON.stringify(db));
    paint();
    return done;
  }

  /* ── 页面上直接把一条评论标成已解决 / 重新打开 ───────────── */
  function esc4re(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
  async function toggle(file, quote, to) {
    if (srvOK !== false) {
      var r = await srvResolve(file, quote, to);
      if (r === true) return true;
      if (typeof r === 'string') { say(r); return false; }
    }
    var dir = await ensureDir(true);
    if (!dir) { say('No folder access — press Connect folder in the panel'); return false; }
    var re = new RegExp('^(-\\s*\\[)[ xX](\\]\\s*[A-Z]{1,4}\\d{0,4}\\s*[「"]' +
                        esc4re(quote) + ')', 'm');
    var hit = false;
    await edit(dir, file, function (txt) {
      if (!re.test(txt)) return txt;
      hit = true;
      return txt.replace(re, '$1' + (to ? 'x' : ' ') + '$2');
    });
    return hit;
  }
  // 讨论框：整段写想法 → POST /_board/discuss → 追加进 ## Discussion → 刷新（JL 260723）
  function wireDadd() {
    var last = localStorage.getItem(WK) || users[0];
    document.querySelectorAll('.dadd').forEach(function (box) {
      var ta = box.querySelector('textarea');
      var sel = box.querySelector('select');
      var btn = box.querySelector('.dsave');
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
        if (j.ok) { localStorage.setItem(WK, sel.value); (window.__boardRefresh || function () { location.reload(); })(); }
        else say(j.err || 'write failed');
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

  function wireResolve() {
    document.querySelectorAll('.cms').forEach(function (box) {
      var file = box.getAttribute('data-cfile');
      box.querySelectorAll('.cm').forEach(function (row) {
        if (row.querySelector('.cres')) return;
        var b = document.createElement('button');
        b.className = 'cres';
        var setLbl = function () {
          b.textContent = row.classList.contains('done') ? 'reopen' : 'mark solved';
        };
        setLbl();
        b.onclick = async function () {
          var to = !row.classList.contains('done');
          b.disabled = true;
          var ok = await toggle(file, row.getAttribute('data-quote'), to);
          b.disabled = false;
          if (!ok) { say('Could not find that line in ' + file); return; }
          row.classList.toggle('done', to);
          var s = row.querySelector('.cs:last-of-type');
          if (s) s.textContent = to ? 'solved' : 'open';
          var bx = row.querySelector('.bx'); if (bx) bx.textContent = to ? '☑' : '☐';
          setLbl();
          say('Written to ' + file + (srvOK ? ' — reload to refresh' : ' — rebuild to refresh'));
        };
        row.querySelector('.cmh').appendChild(b);
      });
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
    '<div class="hd"><span class="qid"></span><span class="ti"></span>' +
    '<button class="term" type="button" aria-label="Open terminal" title="Open this question in a real terminal (same session)">&gt;_</button>' +
    '<button class="x" type="button" aria-label="Close chat" title="Close chat">×</button></div>' +
    '<div class="bd"></div><div class="tm"></div>' +
    '<div class="acts"></div>' +
    '<div class="tip"></div>' +
    '<div class="cfg">' +
    '<select class="mdl"><option value="opus">Opus 4.8</option>' +
    '<option value="sonnet">Sonnet 5</option><option value="haiku">Haiku 4.5</option></select>' +
    '<select class="eff"><option>low</option><option>medium</option>' +
    '<option selected>high</option><option>xhigh</option><option>max</option></select>' +
    '<select class="scope" title="Permission tier: Scoped = this question only · Full = all tools + skills, like the CLI">' +
    '<option value="scoped">Scoped</option>' +
    '<option value="full" selected>Full · ask</option>' +
    '<option value="bypass">Full · no ask</option></select>' +
    '<span class="cost"></span></div>' +
    '<div class="sid"></div>' +
    '<div class="ft"><textarea rows="1" placeholder="Ask about this question…"></textarea>' +
    '<button class="send">➤</button></div>';
  document.body.appendChild(chat);
  var cq = null;                                    // 当前挂在哪一题
  var MK = 'board-chat-model', EK = 'board-chat-effort', SK = 'board-chat-scope';
  var CHATK = function (id) { return 'board-chat:' + location.pathname + ':' + id; };

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
      .replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>')
      .replace(/(^|[\s(])\*([^*\s][^*]*)\*/g, '$1<i>$2</i>');
  }
  function md2html(src) {
    var out = [], fence = null, list = null;
    var flush = function () { if (list) { out.push('</' + list + '>'); list = null; } };
    (src || '').split('\n').forEach(function (ln) {
      if (ln.trim().slice(0, 3) === '```') {
        if (fence === null) { flush(); fence = []; }
        else { out.push('<pre>' + mdEsc(fence.join('\n')) + '</pre>'); fence = null; }
        return;
      }
      if (fence !== null) { fence.push(ln); return; }
      if (!ln.trim()) { flush(); return; }
      var h = ln.match(/^(#{1,6})\s+(.*)$/);
      if (h) { flush(); out.push('<div class="mh">' + mdInline(h[2]) + '</div>'); return; }
      var b = ln.match(/^\s*[-*]\s+(.*)$/);
      if (b) {
        if (list !== 'ul') { flush(); out.push('<ul>'); list = 'ul'; }
        out.push('<li>' + mdInline(b[1]) + '</li>'); return;
      }
      var n = ln.match(/^\s*\d+[.)]\s+(.*)$/);
      if (n) {
        if (list !== 'ol') { flush(); out.push('<ol>'); list = 'ol'; }
        out.push('<li>' + mdInline(n[1]) + '</li>'); return;
      }
      if (list) { out.push('<li class="cont">' + mdInline(ln.trim()) + '</li>'); return; }
      out.push('<p>' + mdInline(ln) + '</p>');
    });
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
  function setBubble(el, text) {
    if (el.classList.contains('md')) el.innerHTML = md2html(text);
    else el.textContent = text;
  }
  /* 思考过程：一个可折叠块。默认展开着让你看它边想，答案一到就自动收起；
     之后随时点标题再展开。跟 CLI 里的 thinking 一个意思，只是这里能折叠。 */
  function thinkBubble() {
    var d = document.createElement('details');
    d.className = 'tk'; d.open = true;
    d.innerHTML = '<summary>💭 Thinking</summary><div class="tk-body"></div>';
    chat.querySelector('.bd').appendChild(d);
    chat.querySelector('.bd').scrollTop = 1e9;
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
  var FIXALL =
    'Work through every unresolved comment in this question\'s ## Comments ' +
    '(the ones starting with `- [ ]`). For each one:\n' +
    '1. Edit this question\'s body the way the comment asks;\n' +
    '2. Flip that line to `- [x]` and reply on an indented line below it with ' +
    '`>> CC<MMDD>: what you did`;\n' +
    '3. Add one line at the TOP of ## Log: `YYMMDD HHMM · what changed`.\n' +
    'If you cannot do one, or disagree, do NOT flip it to [x] — write why underneath.\n' +
    'End with a short summary of what you changed.';

  /* BOARDFIX = FIXALL 的整板版（QD5）：不是这一题的评论，是每个 page 的。 */
  var BOARDFIX =
    'You are on the WHOLE board. Work through every unresolved comment (`- [ ]`) ' +
    'in the ## Comments of EVERY page file on this board. For each one:\n' +
    '1. Edit that page\'s body the way the comment asks;\n' +
    '2. Flip that line to `- [x]` and reply on an indented line below it with ' +
    '`>> CC<MMDD>: what you did`;\n' +
    '3. Add one line at the TOP of that page\'s ## Log: `YYMMDD HHMM · what changed`.\n' +
    'If you cannot do one, or disagree, do NOT flip it to [x] — write why underneath.\n' +
    'End with a short per-file summary of what you changed.';

  function openCount(sec) {
    return sec.querySelectorAll('.cm:not(.done)').length;
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
    var n = isBoard ? document.querySelectorAll('.cm:not(.done)').length : openCount(sec);
    if (n) add('🔧 Handle ' + n + ' open comment' + (n > 1 ? 's' : '') + (isBoard ? ' (whole board)' : ''),
               function () { chatSend(isBoard ? BOARDFIX : FIXALL); }, true);
    if (isBoard) {
      add('🧭 Which question should I act on?', function () {
        chatSend('Answer only, do not edit any file: which page on this board should ' +
                 'be acted on next, and why? Consider state, unchecked items and open ' +
                 'comments. Give 1-3 candidates, one line each: id · reason.');
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
    if (isBoard) {
      var h1 = document.querySelector('.h1');
      cq = { id: 'BOARD', file: 'board.md',
             title: (h1 ? h1.textContent : 'this board'), board: true };
    } else {
      cq = { id: sec.id, file: sec.getAttribute('data-file') || '',
             title: sec.getAttribute('data-title') || '' };
    }
    chat.querySelector('.qid').textContent = isBoard ? '🗂 BOARD' : cq.id;
    chat.querySelector('.ti').textContent = cq.title;
    chat.querySelector('.ti').title = cq.title;
    chat.querySelector('textarea').placeholder = isBoard
      ? 'Ask about this board — e.g. what should we act on next?'
      : 'Ask about this question…';
    var bd = chat.querySelector('.bd'); bd.innerHTML = '';
    var log = chatLoad(cq.id);
    if (!log.length) bubble('sys', isBoard
      ? 'This chat sees the WHOLE board — ask it which question to act on, or have it edit the Pages.'
      : 'This chat is attached to ' + cq.file);
    log.forEach(function (m) { bubble(m.k, m.t); });
    chat.querySelector('.tip').textContent = isBoard ? 'board.md · whole-board session' : cq.file;
    /* 这一题的 Claude Code session id —— 抽屉和终端用的是同一个。
       整板会话的 id 在 .wrap 的 data-bsession 上（live swap 会跟着换）。 */
    var sid = isBoard
      ? ((document.querySelector('.wrap') || document.body).getAttribute('data-bsession') || '')
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
      sidbox.innerHTML = '<span class="mut">No session yet — it appears after your first '
        + 'message and is written into the header of ' + cq.file + '</span>';
    }
    chatActs(sec);
    termView(false); disposeTerm();
    chat.classList.add('on'); document.body.classList.add('chaton');

    /* 第一步：先把浏览器里还没写盘的评论同步过去 —— 不然 chat 读不到它们。
       整板会话看得见每个 page，所以把所有还没写盘的都同步，不只这一个文件的。 */
    var mine = isBoard ? db.length
                       : db.filter(function (c) { return c.file === cq.file; }).length;
    if (mine) {
      bubble('sys', 'Writing ' + mine + ' new comment' + (mine > 1 ? 's' : '') + ' into ' +
                    (isBoard ? 'their files' : cq.file) + '…');
      var n = await drain(true);
      bubble('sys', n ? ('Synced ' + n + '. You can now have it work through the comments.')
                      : 'Sync failed — the comments are still pending.');
      if (n) chat.querySelector('.acts').firstChild &&
             chat.querySelector('.acts').replaceChildren();
      if (n) {
        var b = document.createElement('button');
        b.className = 'act pri'; b.textContent = '🔧 Handle the ' + n + ' just-synced comment' + (n > 1 ? 's' : '');
        b.onclick = function () { chatSend(isBoard ? BOARDFIX : FIXALL); };
        chat.querySelector('.acts').appendChild(b);
        var r = document.createElement('button');
        r.className = 'act'; r.textContent = '↻ Refresh';
        r.onclick = function () { (window.__boardRefresh || function () { location.reload(); })(); };
        chat.querySelector('.acts').appendChild(r);
      }
    }
    chat.querySelector('textarea').focus();
  }
  chat.querySelector('.x').onclick = function () {
    chat.classList.remove('on'); document.body.classList.remove('chaton'); };
  /* 模型 / effort / 权限档 记在本机；默认 Opus 4.8 · high · 完整·问我 */
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

  var inflight = null;                    // 正在跑的那一轮：{ctrl, file}
  async function chatStop() {
    if (!inflight) return;
    try {
      await fetch('/_board/stop', { method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: location.pathname, file: inflight.file }) });
      bubble('sys', 'Stop signal sent — it will wrap up at the next message…');
    } catch (e) { /* 服务器都不通了，直接放弃等待 */ }
    inflight.ctrl.abort();                // 浏览器这边立刻不等了
  }
  function chatBusy(on) {
    var btn = chat.querySelector('.send');
    btn.textContent = on ? '⏹' : '➤';
    btn.title = on ? 'Stop this turn' : 'Send';
    btn.classList.toggle('stop', on);
    btn.disabled = false;                 // 忙的时候也能点 —— 那是停止键
    chat.querySelector('textarea').disabled = on;
  }

  async function chatSend(preset) {
    var ta = chat.querySelector('textarea'), btn = chat.querySelector('.send');
    if (inflight) return chatStop();       // 正在跑 → 这一下是「停」
    var msg = (preset || ta.value).trim();
    if (!msg || !cq) return;
    if (!preset) ta.value = '';
    chatBusy(true);
    var log = chatLoad(cq.id);
    bubble('you', msg); log.push({ k: 'you', t: msg }); chatSave(cq.id, log);
    var wait = bubble('sys', '…thinking (click ⏹ again to stop)');
    var ctrl = new AbortController();
    inflight = { ctrl: ctrl, file: cq.file };
    try {
      var r = await fetch('/_board/chat', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        signal: ctrl.signal,
        body: JSON.stringify({ path: location.pathname, file: cq.file, message: msg,
          stream: true,
          model: chat.querySelector('.mdl').value,
          effort: chat.querySelector('.eff').value,
          scope: chat.querySelector('.scope').value })
      });
      /* 服务器一行一条 JSON 地往下发，边收边显示 */
      var rd = r.body.getReader(), dec = new TextDecoder(), buf = '';
      var cur = null, acc = '', j = { ok: true };
      var thinkEl = null, thinkAcc = '';        // 思考过程 → 一个可折叠块
      while (true) {
        var ch = await rd.read();
        if (ch.done) break;
        buf += dec.decode(ch.value, { stream: true });
        var lines = buf.split('\n'); buf = lines.pop();
        for (var i = 0; i < lines.length; i++) {
          if (!lines[i].trim()) continue;
          var ev; try { ev = JSON.parse(lines[i]); } catch (e) { continue; }
          if (ev.t === 'stage') {                 // real progress while nothing streams yet
            if (wait.isConnected) wait.textContent = '… ' + ev.text + '  (⏹ to stop)';
          } else if (ev.t === 'think') {          // 思考过程 → 折叠块，边想边展开
            wait.remove();
            if (!thinkEl) thinkEl = thinkBubble();
            thinkAcc += ev.text;
            thinkEl.querySelector('.tk-body').textContent = thinkAcc;
            chat.querySelector('.bd').scrollTop = 1e9;
          } else if (ev.t === 'delta') {          // 逐字答案
            wait.remove();
            if (thinkEl && thinkEl.open) {        // 答案一来就收起思考；标题留个量
              thinkEl.open = false;
              thinkEl.querySelector('summary').textContent =
                '💭 Thinking (' + thinkAcc.length + ' chars — click to reopen)';
            }
            if (!cur) cur = bubble('cc', '');
            acc += ev.text;
            setBubble(cur, acc);
            chat.querySelector('.bd').scrollTop = 1e9;
          } else if (ev.t === 'text') {           // 整段（没开逐字时）
            wait.remove();
            if (!cur) cur = bubble('cc', '');
            acc += (acc ? '\n\n' : '') + ev.text;
            setBubble(cur, acc);
            chat.querySelector('.bd').scrollTop = 1e9;
          } else if (ev.t === 'ask') {
            /* 跟 CLI 一样的权限提示：它想动东西，先问你 */
            wait.remove();
            cur = null;                       // 批准之后的输出另起一条气泡
            askUI(ev);
          } else if (ev.t === 'tool') {
            wait.textContent = '…' + ev.name;
          } else if (ev.t === 'done') {
            j = Object.assign({ ok: true }, ev);
            if (ev.text && cur) { acc = ev.text; setBubble(cur, acc); }
          }
        }
      }
      wait.remove();
      var txt = j.ok ? (acc || j.text || '(no text reply — it may have only used tools)')
                     : ('⚠ ' + (j.err || 'failed'));
      if (j.stopped) txt = txt + '\n(you stopped this turn, so it may be unfinished)';
      if (!cur) bubble('cc', txt);
      log.push({ k: 'cc', t: txt }); chatSave(cq.id, log);
      if (j.ok) {
        var bits = [];
        if (j.model) bits.push(j.model.replace('claude-', '') + ' / ' + j.effort);
        if (j.scope) bits.push({scoped:'scoped',full:'full·ask',bypass:'full·no-ask'}[j.scope] || j.scope);
        if (j.usd != null) bits.push('$' + Number(j.usd).toFixed(3));
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
      wait.remove();
      bubble('sys', e.name === 'AbortError'
        ? 'Stopped waiting. The server got the stop signal too.'
        : '⚠ ' + e.message);
    }
    inflight = null; chatBusy(false); ta.focus();
  }
  chat.querySelector('.send').onclick = chatSend;
  chat.querySelector('textarea').addEventListener('keydown', function (ev) {
    if (ev.key === 'Enter' && !ev.shiftKey) { ev.preventDefault(); chatSend(); }
  });

  /* ── ⌨ 真终端：同一个 session 换个窗口 ────────────────────────
     LAW（JL 260723）：一个 session 同时只能有一个窗口。
     抽屉和终端读写的是磁盘上同一个 .jsonl，两边同时开会互相盖或者 fork 出第二段历史。
     所以开终端前服务器先看抽屉在不在用；从终端切回来时要「交回 session」。 */
  var termOn = false;
  function termView(on) {
    termOn = on;
    chat.querySelector('.tm').style.display = on ? 'block' : 'none';
    ['.bd', '.acts', '.cfg', '.sid', '.ft', '.tip'].forEach(function (s) {
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

  async function termRelease(file) {
    disposeTerm();
    if (!file) return;
    try {
      await fetch('/_board/release', { method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: location.pathname, file: file }) });
    } catch (e) { /* 服务器没了也要让界面回得来 */ }
  }
  /* 关整个板页面时，如果抽屉里还开着终端，用 beacon 通知服务器收掉。 */
  window.addEventListener('pagehide', function () {
    if (termOn && cq && cq.file && navigator.sendBeacon) {
      navigator.sendBeacon('/_board/release',
        new Blob([JSON.stringify({ path: location.pathname, file: cq.file })],
                 { type: 'application/json' }));
    }
  });
  async function termOpen(quiet) {
    if (!cq) return false;
    if (!quiet) say('Starting a terminal for this question…');
    try {
      var r = await fetch('/_board/term', { method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: location.pathname, file: cq.file }) });
      var j = await r.json();
      if (!j.ok) { say('⚠ ' + j.err); return false; }
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
  chat.querySelector('.term').onclick = async function () {
    if (!cq) return;
    if (termOn) {                                  // 切回抽屉 = 交回 session
      await termRelease(cq.file);
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
    var sec = id && document.getElementById(id);
    var isQ = sec && sec.classList.contains('q');
    if (!isQ) {
      /* 回到目录（#top / #qlist / #all / 无锚点）→ 跟到整板会话（QD5）。
         别的锚点（某个小节之类）不算换地方，不动。 */
      if (id && id !== 'top' && id !== 'qlist' && id !== 'all') return;
      if (cq && cq.board) return;                   // 已经是整板会话
      var wt = termOn, of = cq && cq.file;
      if (wt) await termRelease(of);
      await chatOpen('board');
      if (wt) await termOpen(true);
      say('Now following the board');
      return;
    }
    if (cq && cq.id === sec.id) return;             // 还是同一题
    var wasTerm = termOn, oldFile = cq && cq.file;
    if (wasTerm) await termRelease(oldFile);        // 一个 session 一个窗口
    await chatOpen(sec);                            // 重新绑到新题（会重置成聊天视图）
    if (wasTerm) await termOpen(true);              // 本来在终端 → 跟着切过去
    say('Now following ' + sec.id);
  }
  window.addEventListener('hashchange', follow);

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
  var fab = document.createElement('button');
  fab.id = 'chatfab';
  fab.onclick = function () {
    var id = (location.hash || '').slice(1);
    var sec = id && document.getElementById(id);
    if (sec && sec.classList.contains('q')) chatOpen(sec);
    else chatOpen('board');
  };
  function fabLbl() {
    var id = (location.hash || '').slice(1);
    var sec = id && document.getElementById(id);
    fab.innerHTML = (sec && sec.classList.contains('q'))
      ? '\u{1F916} Chat' : '\u{1F916} Board chat';
  }
  window.addEventListener('hashchange', fabLbl);
  fabLbl();
  document.body.appendChild(fab);

  function rewire() { marks(); paint(); wireResolve(); wireDadd(); wireQBtns(); wireStruct(); wireXcal(); }
  window.__boardRewire = rewire;
  marks(); paint(); wireResolve(); wireDadd(); wireXcal();
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
        busy = true;
        return fetch(location.pathname, { cache: 'no-store' })
          .then(function (r) { return r.text(); })
          .then(function (t) {
            var doc = new DOMParser().parseFromString(t, 'text/html');
            var nw = doc.querySelector('div.wrap');
            var old = document.querySelector('div.wrap');
            if (!nw || !old) return;
            var y = window.scrollY;
            old.replaceWith(nw);
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
        body: JSON.stringify({ path: location.pathname, file: file,
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
  document.addEventListener('click', function (e) {
    if (e.target.closest('.sadd')) return;
    var row = e.target.closest('.saddrow');
    if (row) {
      var det = row.closest('details.sent');
      var qr = row.closest('section.slide.q');
      if (det && qr) mk(row, det.querySelector('summary p'), qr.dataset.file);
    }
  });
  // DOUBLE-click opens the ➕ form (JL 260725: single click stays free for
  // reading and selecting; the incidental word-selection is cleared first).
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
    var q = p.closest('section.slide.q');
    if (!q) return;
    if (p.closest('.folds,.sapp,.bd,.cmt,.cmb,.qh,.dadd,.spine')) return;
    if (window.getSelection) window.getSelection().removeAllRanges();
    // WHERE the form goes differs by shape, and getting this wrong is silent.
    // `mk` does `afterEl.insertAdjacentElement('afterend', …)`, so passing the
    // summary's own `p` would drop the form INSIDE the <summary>, where every
    // click toggles the drawer and the inputs cannot be used. A drawer therefore
    // takes the same two arguments the ➕ row path uses: insert at the END OF THE
    // DRAWER BODY, while still naming the summary's sentence as the target line.
    var det = p.closest('details.sent');
    if (det) {
      det.open = true;                       // two clicks toggled it net-zero
      var sapp = det.querySelector('.sapp');
      mk(det.querySelector('.saddrow') || sapp || p, det.querySelector('summary p'),
         q.dataset.file);
      return;
    }
    mk(p, p, q.dataset.file);
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
      op: op, path: location.pathname, span: span, page: c.page,
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
    var path = location.pathname.replace(/\/board\.html$/, '').replace(/^\//, '');
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
