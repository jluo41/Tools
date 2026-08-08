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
  // 🪪 the SECOND thing a selection can become (JL 260802, QB5 option D):
  // a comment goes UNDER the line, a card goes ON these exact words. Two
  // buttons rather than one with a mode, because the reader has already made
  // the choice by the time they let go of the mouse.
  var cbtn = mk('button', 'ccard', '\u{1FAAA} Card');
  var box = mk('div', 'cbox',
    '<div class="qq"></div><textarea placeholder="Write a comment…"></textarea>' +
    '<div class="row"><select></select><span style="flex:1"></span>' +
    '<button class="cx">Cancel</button><button class="ok cs">Save</button></div>' +
    '<input class="nu" placeholder="New initials, e.g. ZW — press Enter">');
  var dock = mk('button', 'cdock', '');
  var panel = mk('div', 'cpanel', '');
  var toast = mk('div', 'ctoast', '');
  [btn, cbtn, box, dock, panel, toast].forEach(function (e) { document.body.appendChild(e); });

  function save() { localStorage.setItem(KEY, JSON.stringify(db)); marks(); paint(); }
  function say(m) {
    toast.textContent = m; toast.style.display = 'block';
    clearTimeout(toast._t);
    toast._t = setTimeout(function () { toast.style.display = 'none'; }, 3000);
  }

/* 🔌 Registry of what a page can OPEN · two menus, one list.
 *
 * WHY A REGISTRY. The picker used to be two hardcoded buttons, so the board engine
 * had to know every surface by name. A plugin now registers its own entry, and the
 * engine never learns that labeling exists (JL 260807).
 *
 * TWO MENUS, AND THE SPLIT IS NOT COSMETIC (JL 260808).
 *
 *   🔌 Plugin    a SURFACE you open. Opens to the RIGHT, tab-like. It has no
 *                opinion about where you are on the page, so it applies almost
 *                everywhere. GUI Chat, TUI Chat, and later Draw and Slide.
 *   🪜 Workflow  a STEPPER over THIS page. Opens along the BOTTOM. Its whole job
 *                is to say which step is live and which are refused, so it is
 *                gated on the page's declared type. Labeling, and later Page.
 *
 * This reverses the 260807 ruling that there is no Workflow entry, and the reason
 * the earlier one was right is the reason this one is: a category with one member
 * names a concept nobody owns. Page's four phases arrive as the second member, so
 * the category now describes something real instead of anticipating it.
 *
 * A WORKFLOW IS NOT ALWAYS A LADDER. Labeling's five doors are ordered and each is
 * locked by the one before. Page's DRAFT/PROBE/REVISE/CHECK is a loop whose CHECK
 * routes BACKWARD ("RUN is deliberately not ADVANCE"), so it has a current phase and
 * legal next phases and no locks at all. Each surface computes its own dimming; the
 * registry holds no step model, which is what lets both live in one menu.
 *
 * `applies` KEEPS THE MENU HONEST. An entry that cannot act on the open page is not
 * shown, so the menu never offers work that would be refused. It follows that an
 * entry ships when its surface does: registering Draw before it opens anything makes
 * the menu lie, and a menu that lies once stops being read.
 */
(function () {
  'use strict';

  var reg = [];

  var MENUS = ['plugin', 'workflow'];

  /* {id, label, hint, menu, applies(page)->bool, open(page)} · order is registration
     order, which is asset sort order, which is stable across builds.

     `menu` defaults to 'plugin' so an entry written before the split still lands
     somewhere visible rather than silently in neither menu. An unknown menu name is
     corrected to 'plugin' for the same reason: a typo should misfile an entry, not
     delete it. */
  function register(spec) {
    if (!spec || !spec.id || typeof spec.open !== 'function') return;
    if (MENUS.indexOf(spec.menu) < 0) spec.menu = 'plugin';
    reg = reg.filter(function (e) { return e.id !== spec.id; });
    reg.push(spec);
  }

  function livePage() {
    var secs = document.querySelectorAll('.wrap section.slide.q');
    for (var i = 0; i < secs.length; i++) {
      if (secs[i].offsetParent !== null) return secs[i];
    }
    return secs[0] || null;
  }

  /* A page's declared type, read off the rendered page rather than the source, so a
     surface can gate on it without the engine parsing frontmatter a second time. */
  function pageType(page) {
    if (!page) return '';
    return (page.getAttribute('data-page-type')
            || page.getAttribute('data-type') || '').trim();
  }

  /* `menu` is optional: omitted, this answers "everything this page can open", which
     is what the in-page picker wants when it draws both groups in one list. */
  function applicable(page, menu) {
    return reg.filter(function (e) {
      if (menu && e.menu !== menu) return false;
      try { return !e.applies || e.applies(page, pageType(page)); }
      catch (err) { return false; }
    });
  }

  window.boardPlugins = {
    register: register,
    all: function () { return reg.slice(); },
    applicable: applicable,
    menus: function () { return MENUS.slice(); },
    livePage: livePage,
    pageType: pageType
  };
})();

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
    // Through the shared reader, not textContent: a sentence that already
    // carries apparatus ends with its ⚑ badge inside the <p>, and posting that
    // makes the anchor miss every time (JL 260801). Looked up at call time
    // because this module is bundled before the one that defines it.
    return window.__boardSentenceText ? window.__boardSentenceText(a)
                                      : a.textContent.replace(/\s+/g, ' ').trim();
  }

  /* ── select -> floating button ───────────────────────────── */
  function hideBtns() { btn.style.display = 'none'; cbtn.style.display = 'none'; }
  document.addEventListener('mouseup', function (ev) {
    if (box.contains(ev.target) || panel.contains(ev.target)
        || ev.target === btn || ev.target === cbtn) return;
    setTimeout(function () {
      var s = window.getSelection();
      var txt = s && String(s).trim();
      if (!txt || txt.length < 2 || !s.rangeCount) { hideBtns(); return; }
      var node = s.anchorNode;
      node = node.nodeType === 1 ? node : node.parentNode;
      var q = node.closest && node.closest('section.q');
      if (!q) { hideBtns(); return; }
      var live = s.getRangeAt(0);
      var sentence = containingSentence(live);
      if (!sentence) { hideBtns(); return; }
      var r = live.getBoundingClientRect();
      pend = { id: q.id, file: q.getAttribute('data-file') || '',
               quote: txt, sentence: sentence, range: live.cloneRange() };
      btn.style.left = (r.left + window.scrollX) + 'px';
      btn.style.top = (r.bottom + window.scrollY + 7) + 'px';
      btn.style.display = 'block';
      // 🪪 offered only when the words are ACTUALLY IN the sentence. A card
      // binds by matching them in the source line, so a selection that spans
      // a code span or crosses two sentences has nothing to bind with, and
      // showing a button that can only fail is worse than showing none.
      cbtn.style.display = sentence.indexOf(txt) >= 0 && txt.indexOf(':') < 0
        ? 'block' : 'none';
      cbtn.style.left = (r.left + window.scrollX + btn.offsetWidth + 6) + 'px';
      cbtn.style.top = btn.style.top;
    }, 0);
  });

  /* ── 🪪 write a card on the selected words ─────────────────────────────
     Reuses the comment composer, minus the person: a card says what a phrase
     IS, and no author's initials belong on that. */
  cbtn.onclick = function () {
    hideBtns();
    var words = pend.quote;
    box.querySelector('.qq').textContent = '\u{1FAAA} ' + words;
    box.querySelector('select').style.display = 'none';
    box.querySelector('.nu').style.display = 'none';
    var ta = box.querySelector('textarea');
    ta.value = '';
    ta.placeholder = 'What should open when someone clicks “' + words + '”…';
    box.style.left = btn.style.left; box.style.top = btn.style.top;
    box.style.display = 'block';
    ta.focus();
    box.dataset.mode = 'card';
  };

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
    hideBtns();
    box.dataset.mode = 'comment';
    fillWho(); box.querySelector('.nu').style.display = 'none';
    box.querySelector('select').style.display = '';
    box.querySelector('.qq').textContent = pend.quote;
    var ta = box.querySelector('textarea');
    ta.value = ''; ta.placeholder = 'Write a comment…';
    box.style.left = btn.style.left; box.style.top = btn.style.top;
    box.style.display = 'block';
    ta.focus();
  };
  box.querySelector('.cx').onclick = function () { box.style.display = 'none'; };
  box.querySelector('.cs').onclick = function () {
    var v = box.querySelector('textarea').value.trim();
    if (!v) return;
    if (box.dataset.mode === 'card') {
      var words = pend.quote, file = pend.file;
      var save = box.querySelector('.cs');
      // The composer stays OPEN until the server says it wrote. A refusal is
      // the whole reason this endpoint has three gates, and closing the box on
      // the way out would throw away what the person had just typed.
      save.disabled = true; save.textContent = 'Saving…';
      post('/_board/card', { file: file, sentence: pend.sentence, span: words, text: v })
        .then(function (j) {
          save.disabled = false; save.textContent = 'Save';
          if (!j) { say('The Board server is not running, so no card was written'); return; }
          if (!j.ok) { say(j.err || 'the card was not written'); return; }
          // A successful write rebuilds, so the card appearing on the words IS
          // the confirmation and a toast would only say it again. Only the
          // failures above still need words.
          box.style.display = 'none';
          // Clear the selection BEFORE refreshing: the swap holds itself back
          // while text is selected, on the assumption that the reader is still
          // working on it, and this selection is the one we just consumed.
          window.getSelection().removeAllRanges();
          // Do not wait for the poll to notice. The writer already knows the
          // file changed, so ask for the swap now: it is the difference
          // between the words lighting up at once and up to 800ms of nothing.
          if (window.__boardRefresh) window.__boardRefresh();
        })
        .catch(function () {
          save.disabled = false; save.textContent = 'Save';
          say('The Board server did not answer');
        });
      return;
    }
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
      if (n && srvOK) {
        // Same reason as the card path: the comment appearing under its
        // sentence is the confirmation, and asking for the swap now is what
        // makes it feel like one action instead of a save and then a wait.
        window.getSelection().removeAllRanges();
        if (window.__boardRefresh) window.__boardRefresh();
      }
      if (n) say((ok ? 'Highlighted and ' : 'Saved (not anchored) and ') +
                 'written to ' + pend.file + (srvOK ? ' — rendered below the sentence'
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
          quote: c.quote, when: c.when || stamp() });
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

  /* ── session 拣选器（QD1 Law 修正 260731：一题多 session，一个 current）──
     打开抽屉先亮清单：current 在头一行，历史按最后动笔新→旧，还有「＋新开一段」。
     选中的那段随下一条消息（或 ⌨ 终端）被 resume，同时成为 current，头部跟着换。 */
  var chatSid = '';        // '' = 跟着头部的 current · 'new' = 新开 · uuid = 点名的历史
  /* THE SESSION THE DRAWER IS SHOWING (JL 260801: "我们打开了一个新的 session
     webpage，为什么整个页面没有跟着更新呢?").

     `chatSid` was only ever a PENDING INTENT: what the NEXT message should ask
     the server for. Nothing on screen was bound to it, so picking a session
     printed a sentence and left the header, the transcript, the local log key
     and the row highlight all describing the session you had just left. That is
     the whole difference from the VS Code plugin, which keeps ONE active
     conversation id and renders every part of the panel from it.

     `activeSid` is that id. It is the session the body, the `.sid` box, the
     picker highlight and `logKey()` all agree they are showing, and `switchTo`
     is the ONLY thing allowed to change it. '' means "a new session, not started
     yet". */
  var activeSid = '';
  var lastSessJson = null;             // what the picker last drew, for repaint
  function sessAge(t) {
    if (!t) return '';
    var s = Math.max(0, Date.now() / 1000 - t);
    return s < 90 ? 'now' : s < 5400 ? Math.round(s / 60) + 'm'
         : s < 129600 ? Math.round(s / 3600) + 'h' : Math.round(s / 86400) + 'd';
  }
  function paintSessSummary(rows) {
    var n = rows.filter(function (r) { return r.landed; }).length;
    var named = function (r) { return r && (r.name || (r.id ? r.id.slice(0, 8) + '…' : '')); };
    var row = null;
    for (var pi = 0; pi < rows.length; pi++) if (rows[pi].id === activeSid) row = rows[pi];
    /* the summary says what you ARE ON, not what you have queued up: "picked"
       and "next" were the old model's words for an intent nothing obeyed */
    var cur = !activeSid ? ('new session' + (sessName ? ': ' + sessName : ''))
            : row ? named(row) : activeSid.slice(0, 8) + '…';
    chat.querySelector('.spick summary').textContent =
      '🗂 Session: ' + cur + (n > 1 ? ' · ' + n + ' on record' : '') + ' ▾';
  }

  /* THE HEADER FOLLOWS THE SWITCH. The `.sid` box used to be written in exactly
     one place, inside chatOpen, so it could only ever show the session the PAGE
     was opened on; switching sessions left it naming the old one, with a
     `claude --resume` command that resumed the wrong conversation. */
  function paintSid(sid) {
    var sidbox = chat.querySelector('.sid');
    if (!sidbox || !cq) return;
    if (!sid) {
      sidbox.innerHTML = '<span class="mut">' + (cq.group
        ? 'Group sessions live in the 🗂 tab — pick one, or start a new one here.'
        : 'No session yet — it appears after your first message and is written into the header of '
          + cq.file) + '</span>';
      return;
    }
    /* session 归档在 cwd（= serve.py 的 --root）下的 project 目录，所以要 cd 到
       root，不是板文件夹 —— cd 错了 --resume 就找不到这个 session。 */
    var board = document.body.getAttribute('data-board') || '.';
    var urlDir = boardDirPath();
    var root = board;
    if (urlDir && board.slice(-urlDir.length) === urlDir) {
      root = board.slice(0, board.length - urlDir.length) || '/';
    }
    sidbox.innerHTML = '<code>' + sid + '</code>';
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

    /* A THIRD way into the same session: a terminal on the machine YOU are
       sitting at (JL 260801: "在这个 App 上打开 Terminal，然后在 Terminal 里面
       进入这个 Chat").

       The board cannot open it for you, and the reason is worth stating once so
       nobody tries again: a page cannot start a program on the machine viewing
       it, and having the SERVER open a window is not a workaround, because the
       server is on the Mac while the reader is usually somewhere else over ssh.
       Tried on 260801, it opened nothing and blocked the call.

       What the server DOES know is the exact command, including the ssh hop
       back to itself. One paste in any terminal, on any machine, lands in this
       same conversation. */
    var lb = document.createElement('button');
    lb.className = 'act'; lb.textContent = '🖥 Copy: open on my machine';
    lb.title = 'An ssh command that drops any terminal, anywhere, into this session';
    lb.onclick = async function () {
      try {
        var r = await fetch('/_board/local-cmd', { method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ path: boardPath(), file: cq.file,
                                 group: (cq && cq.group) || undefined, session: sid }) });
        var j = await r.json();
        if (!j || j.ok === false) { say('⚠ ' + ((j && j.err) || 'could not build the command')); return; }
        await navigator.clipboard.writeText(j.remote);
        lb.textContent = 'Copied — paste in any terminal';
        say('Paste this in a terminal on your own machine:\n' + j.remote
            + '\nAlready on ' + j.host + '? Then: ' + j.here);
      } catch (e) { say('⚠ ' + e.message); }
    };
    sidbox.appendChild(lb);
  }

  /* A SWITCH LEAVES A MARK IN THE TRANSCRIPT (JL 260801: "为什么 history 没有
     对应的，比如说 switch 呢?"). Without it the pane silently becomes a
     different conversation and a reader cannot tell where one ended and the
     next began. Same shape as the turn separator, one class louder. */
  function switchMark(label) {
    var el = document.createElement('div');
    el.className = 'turnsep switchsep';
    el.textContent = label;
    return el;
  }

  /* THE ONE PLACE A SESSION CHANGES. Everything the reader can see is repainted
     here, in one go: the transcript body, the switch banner, the `.sid` box,
     the picker highlight and the summary line. Nothing else may assign
     activeSid. */
  async function switchTo(sid, name, landed) {
    /* NEVER SWITCH OUT FROM UNDER A LIVE TURN. This clears .bd, calls busyEnd()
       and drops traceEl, so running it mid-stream orphans the trace and leaves
       the ⏹ button stuck — the same defect chatOpen was fixed for on 260731,
       and the tool cards and 💭 thinking block are exactly what disappears. */
    if (typeof inflight !== 'undefined' && inflight) {
      bubble('sys', 'A turn is still running — stop it with ⏹ first, then switch.');
      return;
    }
    var from = activeSid;
    activeSid = sid || '';
    chatSid = sid || 'new';            // what the NEXT message asks the server for
    if (name != null) sessName = sid ? '' : name;
    var bd = chat.querySelector('.bd');
    busyEnd(); traceEl = null; toolCards = {};
    if (activeSid && landed) {
      await replaySession(activeSid, true);          // clears and refills .bd itself
    } else {
      bd.innerHTML = '';
      chatLoad(logKey()).forEach(replayRow);         // a fresh one may have local text
    }
    paintSid(activeSid);
    var label = activeSid
      ? '🗂 ' + (name || (lookupName(activeSid) || activeSid.slice(0, 8) + '…'))
        + (from && from !== activeSid ? '  ·  switched from ' + from.slice(0, 8) + '…' : '')
      : '🗂 new session' + (sessName ? ' · ' + sessName : '')
        + '  ·  starts with your next message';
    bd.insertBefore(switchMark(label), bd.firstChild);
    if (lastSessJson) renderSessions(lastSessJson);   // repaint the highlight
    bdJump();
    syncSchedule();                                  // re-aim the heartbeat
  }
  function lookupName(sid) {
    var rows = (lastSessJson && lastSessJson.sessions) || [];
    for (var i = 0; i < rows.length; i++) if (rows[i].id === sid) return rows[i].name || rows[i].title;
    return '';
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
  function diagSync(m) { try { if (typeof diag === 'function') diag('SYNC', m); } catch (e) {} }
  async function syncFromServer() {
    if (!cq || !cq.file) return;
    try {
      var r = await fetch('/_board/sessions', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: boardPath(), file: cq.file,
                               group: (cq && cq.group) || undefined }) });
      var j = await r.json();
      if (window.__boardTermLive) { try { await loadTermList(); } catch (e) {} }
      if (!j || j.ok === false) return;
      lastSessJson = j;
      /* SYNC THE SESSION BEING SHOWN, NOT THE ONE THE FILE HEADER CALLS CURRENT.
         This asked for `current` unconditionally and wrote the answer into the
         page's log, so picking any other session was undone by the very next
         heartbeat: the replayed history was painted over, in place, a few
         seconds later. That is the "why doesn't the page follow" seen from the
         other side — it followed, and then the sync dragged it back. */
      var want = activeSid;
      if (!want) {
        if (chatSid === 'new') return;      // deliberately on a fresh one: nothing to adopt
        var cur = ((j.sessions) || []).filter(function (s) { return s.current && s.landed; })[0];
        if (!cur) return;
        want = cur.id;
        activeSid = want;                   // the first turn landed; adopt it
        paintSid(want);
      }
      var r2 = await fetch('/_board/session-log', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: boardPath(), file: cq.file,
                               group: (cq && cq.group) || undefined, id: want }) });
      var j2 = await r2.json();
      if (!j2 || j2.ok === false) return;
      var srv = j2.log || [];
      var local = chatLoad(logKey());
      /* Adopt when the server knows BETTER, which is not the same as knowing
         MORE. A cut-short turn leaves a provisional reply in the local log, so
         the two sides have equal LENGTH while one of them is a fragment; the
         old length test therefore refused to upgrade it, forever. Anything
         marked partial is an open invitation to be replaced. */
      var provisional = local.some(function (m) { return m && m.partial; });
      if (srv.length <= local.length && !provisional) return;
      var bd = chat.querySelector('.bd');
      /* Never clobber a turn that is genuinely running, but do not trust a
         STALE flag either: `chatbusy` is a class that an aborted turn can
         leave behind, and while it sat there this function refused to adopt
         anything, forever. `inflight` is the real signal. */
      if ((typeof inflight !== 'undefined' && inflight) || bd.querySelector('.trace')) return;
      /* keep the switch banner: it says which conversation this pane is, and a
         repaint that removed it would leave the reader in an unlabelled one */
      var mark = bd.querySelector('.switchsep');
      bd.innerHTML = '';
      if (mark) bd.appendChild(mark);
      if (j2.clipped) bubble('sys', 'Showing the last ' + srv.length + ' of ' + j2.total + ' messages.');
      /* ADOPTING MUST NOT DELETE. This wiped the pane and repainted the
         SERVER's rows only, then saved them over the local log — so any answer
         this browser had that the session's .jsonl does not carry was lost from
         the screen AND from storage. It happens: a turn that was stopped, or
         one whose reply never reached the transcript, is real to the reader and
         absent from the file (found 260802 — leaving the page and coming back
         dropped two 8k answers). Keep whatever the server does not have, in
         order, after what it does. */
      var seen = {};
      srv.forEach(function (m) { if (m && m.t) seen[m.k + '\u0000' + m.t] = 1; });
      var kept = local.filter(function (m) {
        return m && m.t && !m.partial && !seen[m.k + '\u0000' + m.t];
      });
      var merged = srv.concat(kept);
      merged.forEach(replayRow);
      chatSave(logKey(), merged);
      if (kept.length) diagSync('kept ' + kept.length + ' local row(s) the server did not have');
      bdJump();
    } catch (e) { /* offline or an old server: the local paint still stands */ }
    return true;
  }

  /* THE DRAWER HAS TO KEEP ASKING (JL 260801: "你这个 Chatbot 是不是没有自主地
     去 check session update？我这一回来，然后东西就没有了").
     syncFromServer used to be called from exactly ONE place, chatOpen, so it
     asked the server once at the instant the drawer opened and never again. If
     the turn had not landed in the .jsonl by that instant — and coming back
     mid-turn is exactly when it has not — the reader was left staring at a gap
     that the server could have filled a second later. Nothing was missing; no
     one was asking. So: retry with backoff after opening, ask again whenever
     the tab comes back to the front, and keep a slow idle heartbeat while the
     drawer is open. All of them are cheap reads and all refuse to run while a
     turn is genuinely in flight. */
  var syncTimers = [], syncBeat = null;
  function syncStop() {
    syncTimers.forEach(clearTimeout); syncTimers = [];
    if (syncBeat) { clearInterval(syncBeat); syncBeat = null; }
  }
  function syncNow() {
    if (!cq) return;
    if (typeof inflight !== 'undefined' && inflight) return;   // a live turn owns the view
    /* R1 · REJOIN BEFORE READING. A turn may still be RUNNING on the server
       with nobody watching it, and the transcript cannot help there because it
       is not written until the turn ends — which is exactly the gap JL kept
       hitting ("我这一回来，然后东西就没有了"). Ask the ring first; only when
       nothing is live does the transcript become the right answer. */
    if (typeof chatRejoin === 'function') {
      Promise.resolve(chatRejoin()).then(function (attached) {
        if (!attached) { try { syncFromServer(logKey()); } catch (e) {} }
      }, function () { try { syncFromServer(logKey()); } catch (e) {} });
      return;
    }
    try { syncFromServer(logKey()); } catch (e) {}
  }
  function syncSchedule() {
    syncStop();
    /* the .jsonl is written as the turn ends, so the useful window is the few
       seconds AFTER opening, not the instant of it */
    [1500, 4000, 9000, 20000].forEach(function (ms) {
      syncTimers.push(setTimeout(syncNow, ms));
    });
    syncBeat = setInterval(function () {
      var c = document.getElementById('chat');
      if (!c || !c.classList.contains('on')) return;    // closed: nothing to repaint
      if (document.hidden) return;                      // not being looked at
      syncNow();
    }, 25000);
  }
  document.addEventListener('visibilitychange', function () {
    if (!document.hidden) syncNow();                    // you came back to the tab
  });
  window.addEventListener('focus', syncNow);            // you came back to the window


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
      log.forEach(replayRow);
      bubble('sys', '\u2191 history of the picked session \u00b7 your next message resumes it');
      bdJump();
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
      /* one authority, so the highlight cannot disagree with the pane */
      var picked = r.id === activeSid;
      // 有名字显名字（QD3m-fix-black-screen），没名字退回第一句话
      /* ⌨ marks a session that already has a terminal running, so the picker
         is the one place that shows what exists (JL 260801). */
      var liveT = (window.__boardTermLive ? window.__boardTermLive() : [])
        .filter(function (x) { return x.session === r.id; })[0];
      var d = mk((liveT ? '⌨ ' : '') + (r.name || r.title || (r.landed ? '(untitled)' : '(recorded, never talked)')),
         (r.current ? 'current · ' : '')
           + (liveT ? (liveT.parked ? 'terminal parked · ' : 'terminal running · ') : '')
           + (r.landed ? sessAge(r.mtime) + ' · ' + Math.round((r.size || 0) / 1024) + 'k'
                       : 'hollow'),
         (picked ? 'cur' : '') + (r.name ? ' named' : '') + (r.landed || r.current ? '' : ' dim'),
         async function () {
           if (r.id === activeSid) { sp.open = false; return; }   // already here
           sp.open = false;
           /* ONE chooser for both halves (JL 260801). In the TUI this is not a
              plan for later: attach that session's terminal now. Terminals are
              keyed per (page, session) since 260801, so the one you are leaving
              keeps running and you can come straight back to it. */
           if (window.__boardTermOn && window.__boardTermOn()) {
             chatSid = r.id;
             say('Attaching the terminal for ' + (r.name || r.id.slice(0, 8) + '…') + '…');
             await window.__boardTermAttach(r.id);
             loadSessions();
             return;
           }
           /* SWITCH, do not merely INTEND to. The old code set chatSid, printed
              a sentence and replayed the body, leaving the header, the log key
              and the row highlight on the session you had just left — and the
              sync then painted that one back over the replay (JL 260801). */
           await switchTo(r.id, r.name || r.title || '', r.landed);
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
    var nu = mk('＋ New session', 'starts fresh, primed with this question',
                'new' + (activeSid ? '' : ' cur'), function () {
      // 先问一句这段是干嘛的（可留空）：名字跟着第一条消息/⌨ 一起落进登记表
      var inp = document.createElement('input');
      inp.type = 'text'; inp.className = 'spin';
      inp.placeholder = 'name it: what is this session for? (Enter · empty = unnamed)';
      nu.querySelector('.t').replaceChildren(inp); inp.focus();
      inp.onclick = function (ev) { ev.stopPropagation(); };
      inp.onkeydown = function (k) {
        if (k.key === 'Enter') {
          var nm = inp.value.trim();
          sp.open = false;
          if (window.__boardTermOn && window.__boardTermOn()) {
            sessName = nm; chatSid = 'new';
            say('Starting another terminal…');
            window.__boardTermAttach('new').then(function () { loadSessions(); });
            return;
          }
          /* CLEAR THE PANE. This used to print one sentence into the OLD
             session's transcript and change nothing else, so a "new session"
             looked exactly like the one you were already in (JL 260801:
             "为什么整个页面没有跟着更新呢?"). */
          switchTo('', nm, false);
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
      if (j.ok) { lastSessJson = j; renderSessions(j); }
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
  /* The ONE key for the scope the drawer is on. chatOpen and syncFromServer
     already read 'G:'+id for a group, but the send path saved under the bare
     id, so a GROUP chat wrote to one key and read from another and its
     history never came back (JL 260801: "我再把你打开，你这个新东西又没有了").
     Everything goes through here now, so the two halves cannot drift again.

     ONE MORE HALF, 260801: the key was per PAGE, so every session of a question
     shared a single transcript in this browser. Switching sessions therefore
     could not change what was stored, only what happened to be drawn, and the
     next save wrote the new session's turns on top of the old one's. The key is
     now per (scope, session), which is what makes a switch survive a reload. */
  function logKey() {
    if (!cq) return '';
    var base = cq.group ? 'G:' + cq.id : cq.id;
    return base + '#' + (activeSid || 'new');
  }

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
  /* Autoscroll must FOLLOW, never YANK (JL 260801: "我想 scroll up 去看看之前的
     聊天内容,为啥它就不行 ... 每一次都是一下子给我弄到最下面去了"). Every
     streamed event called scrollTop = 1e9 unconditionally, so reading back
     through a LIVE turn was impossible: each token dragged the reader down
     again. A scroll listener now remembers whether the reader has left the
     bottom, and the stream stops chasing them until they come back down.
     Programmatic jumps land AT the bottom, so they clear the flag themselves.
     Deliberate jumps (opening, replaying, sending) still use bdJump. */
  var BD_SLACK = 48;                    // "close enough to the bottom" in px
  var bdAway = false;                   // the reader scrolled up; do not chase
  (function () {
    var bd = chat.querySelector('.bd');
    if (!bd) return;
    bd.addEventListener('scroll', function () {
      bdAway = (bd.scrollHeight - bd.scrollTop - bd.clientHeight) > BD_SLACK;
    }, { passive: true });
  })();
  function bdAuto() {                   // follow the stream, only if not reading back
    if (bdAway) return;
    var bd = chat.querySelector('.bd');
    if (bd) bd.scrollTop = bd.scrollHeight;
  }
  function bdJump() {                   // deliberate: open, replay, your own message
    bdAway = false;
    var bd = chat.querySelector('.bd');
    if (bd) bd.scrollTop = bd.scrollHeight;
  }
  /* A REPLAY SHOULD READ LIKE THE THING IT REPLAYS (JL 260801: "我重新打开一个
     过去的 session，打开之后，它这个 content 和界面都非常差").
     A live turn ends with a meta line saying how long it took and when it
     finished. A replay had nothing: no times, no turn boundaries, just a flat
     run of bubbles, so a long session read as one undifferentiated wall. The
     jsonl carries a timestamp on every message, so a replay can at least mark
     where each turn began and when. Same separator, whatever the source. */
  function turnMark(iso) {
    var d = new Date(iso);
    if (isNaN(d)) return null;
    var z = function (n) { return String(n).padStart(2, '0'); };
    var el = document.createElement('div');
    el.className = 'turnsep';
    el.textContent = String(d.getFullYear()).slice(2) + z(d.getMonth() + 1)
                   + z(d.getDate()) + ' ' + z(d.getHours()) + ':' + z(d.getMinutes());
    chat.querySelector('.bd').appendChild(el);
    return el;
  }
  /* Draw one row of a REPLAYED transcript. The live path has three shapes on
     screen (a bubble, a tool card, a turn separator) and the replay only had
     one, which is most of why an old session looked nothing like the turn it
     was a recording of. Tools now come back from the server, so they get the
     same compact card, marked done because it already is. */
  var replayTrace = null;      // the box consecutive replayed tool rows collect into
  function replayRow(m) {
    if (!m) return;
    /* A ROW WITH NOTHING IN IT IS A LINE ACROSS THE SCREEN, and eighteen of
       them look like the drawer broke (JL 260802, screenshot: "the thinking
       process become lines"). An entry can arrive empty from an older saved
       log or from a server that returned a message carrying only thinking, and
       every one of those used to become a bordered row with no text in it.
       Draw nothing instead: an absent row reads as absent, a blank one reads
       as a fault. */
    var body = ((m.t || '') + (m.name || '')).trim();
    if (!body) return;
    if (m.k === 'you' && m.ts) turnMark(m.ts);
    /* A REPLAYED TURN GETS THE SAME BOX A LIVE ONE GETS (JL 260803: "I want the
       box like this to host the old thinking process"). A live turn folds its
       tool calls into one bounded `.trace`, which scrolls inside itself; the
       replay appended each card straight into the transcript, so a turn that
       ran 35 tools became 35 rows a reader had to scroll past to reach the
       answer. Consecutive tool rows now collect into one `.trace done`, and
       any other row closes it — the shape of the recording matches the shape
       of the thing it recorded. */
    if (replayTrace && !replayTrace.parentNode) replayTrace = null;  // .bd was cleared
    if (m.k !== 'tool') {
      replayTrace = null;
      bubble(m.k, m.t);
      return;
    }
    if (!replayTrace) {
      replayTrace = document.createElement('div');
      replayTrace.className = 'trace done';
      replayTrace.dataset.n = '';
      chat.querySelector('.bd').appendChild(replayTrace);
    }
    var d = document.createElement('details');
    d.className = 'tool done';
    d.innerHTML = '<summary><span class="tn"></span><span class="tb"></span>' +
                  '<span class="ts">done</span></summary>';
    d.querySelector('.tn').textContent = m.name || '?';
    d.querySelector('.tb').textContent = (m.t || '').replace((m.name || '') + '  ', '');
    replayTrace.appendChild(d);
    var n = replayTrace.querySelectorAll('.tool').length;
    replayTrace.dataset.n = n + (n === 1 ? ' tool call' : ' tool calls');
    bdAuto();
  }
  function bubble(kind, text) {
    /* The live path bubbles an answer as 'cc'; the server's session-log
       (live/chat.py) returns the very same thing as 'ai'. Only 'cc' got
       md2html and only '.m.cc' has a style, so a REPLAYED answer arrived as
       raw text in an unstyled box while the identical live answer rendered
       (JL 260801: "History content 没有 Markdown render 的模式").
       One word apart, two symptoms; normalize here so old servers work too. */
    if (kind === 'ai') kind = 'cc';
    var d = document.createElement('div');
    d.className = 'm ' + kind;
    if (kind === 'cc') { d.classList.add('md'); d.innerHTML = md2html(text); }
    else { d.textContent = text; }
    chat.querySelector('.bd').appendChild(d);
    bdAuto();
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
    /* the trace is its own small scroller and always shows its newest row;
       the transcript behind it only follows when the reader is at the bottom */
    if (traceEl) traceEl.scrollTop = traceEl.scrollHeight;
    bdAuto();
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
    bdJump();          /* a gate needs an answer: this one may interrupt reading */
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
          'First use Read to load the canonical evaluation contract at ' +
          'Tools/plugins/haipipe-toolkit/skills/board/haipipe-board-page/SKILL.md and the cold-read rules at ' +
          'Tools/plugins/haipipe-toolkit/skills/board/haipipe-board/ref/writing-rules.md. ' +
          'Resolve requirements in order: base contract; page-kind or consumer variant; this page\'s Writing Style ' +
          'and Stage Contract; then each local division purpose and paragraph job. Report any conflict instead of choosing silently. ' +
          'Review every present ## section, every direct ### Content division, and every #### paragraph whose job must be tested. ' +
          'Report exactly: Requirement conflicts; then a table with unit | applicable requirements + source | verdict | evidence | smallest fix; ' +
          'then Mechanical findings; then one Page verdict. Use only MEETS, NEEDS WORK, N/A, or NOT VERIFIABLE. ' +
          'Separate mechanics, function, evidence, and readability. Every MEETS needs visible evidence; NOT VERIFIABLE is never a pass.';
      chatSend(prompt, { scope: 'scoped', qualityCheck: true });
    }, true);
    add('📍 Where are we?', function () {
      askHere('Answer only, do not edit any file: summarize the current status, ' +
               'what is decided, what remains open, and the one concrete blocker. ' +
               'Use short bullets with evidence from this page.');
    });
    add('➡️ What next?', function () {
      askHere('Answer only, do not edit any file: propose the smallest valuable ' +
               'next step. Name its owner, the evidence it needs, and which item it closes.');
    });
    add('🎯 Clarify aim', function () {
      askHere('Answer only, do not edit any file: rewrite this page\'s aim/question ' +
               'as one plain-language sentence. Then identify any ambiguity that still ' +
               'needs a human decision.');
    });
    if (isBoard) {
      add('🧭 Which question should I act on?', function () {
        askHere('Answer only, do not edit any file: which page on this board should ' +
                 'be acted on next, and why? Consider page state and open Aim States. ' +
                 'Give 1-3 candidates, one line each: id · reason.');
      });
    } else {
      add('📝 What is this question missing?', function () {
        askHere('Answer only, do not edit any file: which Aims on this page have ' +
                 'a State other than met or held, and what is each one blocked on? ' +
                 'One per line, using the Aim id.');
      });
    }
    add('↻ Refresh', function () { (window.__boardRefresh || function () { location.reload(); })(); });
  }
  /* ONE door for every "ask this" affordance in the drawer. Whichever half is
     on screen is the half that receives it (JL 260801). */
  function askHere(prompt, opts) {
    if (window.__boardTermOn && window.__boardTermOn()) {
      if (window.__boardTermType(prompt)) return;
    }
    chatSend(prompt, opts);
  }


  async function chatOpen(sec) {
    /* sec 是某一题的 <section>，或字符串 'board'（QD5）：整板会话，挂在 board.md 上。
       服务器端认 file=board.md，规则和开场定位换成整板那份；session 记在 board.md 头部。 */
    var isBoard = (sec === 'board');
    var sameTarget =
      (isBoard && cq && cq.board) ||
      (sec && sec.group && cq && cq.group === sec.group) ||
      (sec && sec.id && cq && cq.id === sec.id);

    /* REOPENING THE SAME CHAT IS NOT A REASON TO REBUILD IT (JL 260801: "我把
       它打开、关了、又打开，它就没有那么丝滑了 ... VS Code 的 plugin 无论什么
       时候开它都是非常丝滑的").
       That is exactly what VS Code does differently: its webview is RETAINED,
       so hiding a panel changes visibility and nothing else, and showing it
       again costs one repaint. Ours tore the transcript down and built every
       bubble again from storage, re-parsing markdown for each one, and then
       sometimes wiped and rebuilt a second time when the server answered. All
       of that work produced a transcript identical to the one just thrown
       away, and the flash between the two is the thing that reads as janky.
       So when the same scope is already painted and nothing is running, just
       show it. The server is still asked, quietly, through the sync. */
    if (!inflight && sameTarget && chat.querySelector('.bd').children.length) {
      chat.classList.add('on'); document.body.classList.add('chaton');
      requestAnimationFrame(bdJump);
      chat.querySelector('textarea').focus();
      if (typeof syncNow === 'function') syncNow();
      return;
    }

    /* NEVER re-open over a turn that is still streaming (JL 260731: "why the
       progress is not shown here again?"). This function clears .bd, calls
       busyEnd() and drops traceEl, so running it mid-turn leaves the user
       bubble replayed from the log, the trace orphaned, nothing rendering and
       the ⏹ button stuck — which is exactly what the screenshot showed. A
       rebuild, a hash bounce, or a stray follow() can all land us here. */
    if (inflight) {
      diag('chatOpen WHILE INFLIGHT', (sec && sec.id) || (isBoard ? 'board' : '?'));
      if (sameTarget) {                    // same page: leave the live turn alone
        /* ...but still OPEN it. The early return sat above the line that adds
           .on, so closing the drawer mid-turn and pressing 💬 again did
           nothing at all: the turn was fine, the drawer just never came back. */
        chat.classList.add('on'); document.body.classList.add('chaton');
        requestAnimationFrame(bdJump);
        return;
      }
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
    /* BIND THE SESSION FIRST. Everything below — the local log key, the body,
       the picker highlight — is now a render of `activeSid`, so it has to be
       known before the first paint rather than assigned twenty lines later.
       这一题的 Claude Code session id —— 抽屉和终端用的是同一个；整板会话的 id 在
       .wrap 的 data-bsession 上（live swap 会跟着换）。 */
    activeSid = isBoard
      ? ((document.querySelector('.wrap') || document.body).getAttribute('data-bsession') || '')
      : isGroup ? ''
      : (sec.getAttribute('data-session') || '');
    chatSid = '';                 // 换题回到「跟着头部 current」；清单重新拉
    var bd = chat.querySelector('.bd'); bd.innerHTML = '';
    var log = chatLoad(logKey());
    if (!log.length) bubble('sys', isBoard
      ? 'This chat sees the WHOLE board — ask it which question to act on, or have it edit the Pages.'
      : isGroup
      ? 'This chat sees the GROUP ' + cq.group + ' — its pages, their states, and how they fit.'
      : 'This chat is attached to ' + cq.file);
    log.forEach(replayRow);
    /* The local paint above is instant; the server holds the truth.
       R1: this goes through syncNow rather than straight to syncFromServer,
       because REOPENING AFTER A RELOAD is the single most important moment to
       rejoin a running turn — the transcript cannot answer then, since it is
       not written until the turn ends. syncNow asks the ring first and falls
       back to the transcript only when nothing is live. */
    syncNow();
    syncSchedule();          /* and keep asking; one shot at open WAS the bug */
    /* TUI first, unless the reader has chosen the chat box (JL 260801) */
    if (window.__boardOpenDefaultView) {
      setTimeout(function () { try { window.__boardOpenDefaultView(); } catch (e) {} }, 0);
    }
    chat.querySelector('.tip').textContent = isBoard ? 'board.md · whole-board session'
      : isGroup ? cq.group + ' · group session' : cq.file;
    /* one painter, shared with switchTo, so the header can never describe a
       different session from the one the body is showing */
    paintSid(activeSid);
    chatActs(isGroup ? null : sec);
    loadSessions();
    termView(false); disposeTerm();
    chat.classList.add('on'); document.body.classList.add('chaton');
    /* Land on the NEWEST message, not the oldest (JL 260801: "它还是一直在最
       上面 ... 我还得往下面去翻"). bubble() already scrolls on every append,
       but the replay above runs while #chat is still display:none, where
       scrollHeight is 0 and every scrollTop assignment is clamped to 0. The
       drawer only becomes visible on the line above, so the scroll has to
       happen after layout, which is what the frame callback buys. */
    requestAnimationFrame(bdJump);

    chat.querySelector('textarea').focus();
  }
  function chatClose() {
    chat.classList.remove('on'); document.body.classList.remove('chaton');
  }
  chat.querySelector('.x').onclick = chatClose;
  chat.querySelector('.back').onclick = chatClose;   /* same act, named for where it goes */

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
    /* ONE ACTION, ONE MESSAGE. The abort below lands in the catch, which says
       "Stopped waiting. The server got the stop signal too." — so pressing ⏹
       printed two lines that half contradict each other, the first saying it
       will wrap up and the second that we stopped waiting (found 260802 by
       asserting the drawer says exactly one thing about stopping). The line
       above is the honest one and it is already on screen. */
    if (inflight.mark) inflight.mark();
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
  /* THE TEST BRIDGE. The drawer is one closure, so nothing inside it is
     reachable from Runtime.evaluate, and `checks/chatui.mjs` T8 and T10 were
     therefore reporting "not reachable" and had NEVER ONCE RUN — two checks
     that looked like coverage and were not. Anything the suite must reach goes
     here, deliberately and by name, rather than by leaking the whole scope. */
  window.__chatProbe = {
    bubble: function (k, t) { return bubble(k, t); },
    inflight: function () { return !!inflight; },
    activeSid: function () { return activeSid; },
    logKey: function () { return logKey(); },
    switchTo: function (sid, name, landed) { return switchTo(sid, name, landed); },
    sidText: function () { return (chat.querySelector('.sid') || {}).textContent || ''; },
    switchMarks: function () {
      return [].map.call(chat.querySelectorAll('.bd .switchsep'),
                         function (e) { return e.textContent; });
    }
  };
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
    var d = bubble('you', text); bdJump();
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

  /* R1 · HOW FAR THIS READER GOT IN THE TURN'S RING.
     The server now keeps every turn's events in a ring with a monotonic cursor
     (`live/turnring.py`), so the only thing a returning drawer needs in order to
     rejoin is the number of the last event it saw. It lives in storage rather
     than in a variable precisely because the thing it has to survive is the
     page that was reading — a reload, a navigation, a phone locking. */
  /* Keyed on the SCOPE, never on the session. The ring is per question path on
     the server, and `logKey()` folds in the session id — which CHANGES mid-turn
     the first time a new session is created, so a cursor written before that
     point was looked for under a key that no longer existed and the rejoin
     started from near zero. Caught by reloading a real page, not by reading. */
  var CURK = function () {
    return 'board-chat-cur:' + location.pathname + ':'
         + ((cq && (cq.group ? 'G:' + cq.group : cq.file)) || '');
  };
  function curGet() {
    try { return parseInt(localStorage.getItem(CURK()) || '0', 10) || 0; }
    catch (e) { return 0; }
  }
  function curSet(n) { try { localStorage.setItem(CURK(), String(n)); } catch (e) {} }

  /* ── THE REJOIN IS NOT A TURN ────────────────────────────────────────────
     It used to be: `chatRejoin` called `chatSend({attach:true})` and every
     failure branch of a 250-line turn function became something the reader
     saw. That cost two separate fixes in one day — the 404 branch, then the
     abort branch — and JL still ended up with ~120 copies of "Stopped waiting.
     The server got the stop signal too." on one page (260802), a sentence that
     was false twice over. A third branch would have been missed the same way.

     So the two are separated the way the VS Code extension separates them. Its
     webview never owns a turn: the extension host owns the session and the
     webview only RENDERS events, which is why it can be thrown away and
     rebuilt at any moment without anything being lost or anything being said
     about it. `chatSend` owns a turn: the composer, the log, the cost line,
     the failure report. `chatAttach` owns nothing at all. It paints events
     into the transcript and, on any failure whatsoever, returns false without
     a word. There is no branch left in it that can address the reader. */
  var reattaching = false;

  async function chatAttach() {
    if (inflight || reattaching || !cq) return false;
    reattaching = true;
    var painted = false, cur = null, acc = '', seg = '';
    var thinkEl = null, thinkAcc = '', lastRow = null, lastSeg = '';
    var t0 = Date.now();
    try {
      var r = await fetch('/_board/attach', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: boardPath(), file: cq.file,
          group: (cq && cq.group) || undefined, cursor: curGet() })
      });
      /* Nothing running is the ORDINARY answer, and an older server with no
         ring is an ordinary answer too. Both are "false", both are silent. */
      if (!r.ok || (r.headers.get('Content-Type') || '').indexOf('ndjson') < 0) {
        diag('REJOIN', 'nothing live');
        return false;
      }
      diag('REJOIN', 'attached at cursor ' + curGet());
      var log = chatLoad(logKey());
      traceStart(); busyStart('Rejoining'); chatBusy(true); painted = true;
      var rd = r.body.getReader(), dec = new TextDecoder(), buf = '', j = null;
      while (true) {
        var ch = await rd.read();
        if (ch.done) break;
        buf += dec.decode(ch.value, { stream: true });
        var lines = buf.split('\n'); buf = lines.pop();
        for (var i = 0; i < lines.length; i++) {
          if (!lines[i].trim()) continue;
          var ev; try { ev = JSON.parse(lines[i]); } catch (e) { continue; }
          if (typeof ev.n === 'number') curSet(ev.n + 1);
          if (ev.t === 'ping') continue;
          if (ev.t === 'gap') {
            bubble('sys', '⚠ ' + (ev.text || 'reconnected mid-turn'));
          } else if (ev.t === 'stage') {
            busySay(ev.text.length > 46 ? ev.text.slice(0, 46) + '…' : ev.text);
          } else if (ev.t === 'think') {
            busySay('Thinking');
            if (!thinkEl) thinkEl = thinkBubble();
            thinkAcc += ev.text;
            thinkEl.querySelector('.tk-body').textContent = thinkAcc;
            bdAuto();
          } else if (ev.t === 'delta') {
            if (busyWhat !== 'Responding') busySay('Responding');
            if (thinkEl && thinkEl.open) {
              thinkEl.open = false;
              thinkEl.querySelector('summary').textContent =
                '💭 Thinking (' + thinkAcc.length + ' chars — click to reopen)';
            }
            if (!cur) { cur = traceRow('say', '✍️', ''); seg = ''; }
            seg += ev.text; acc += ev.text;
            cur.querySelector('.x').textContent = seg;
            lastRow = cur; lastSeg = seg;
            traceScroll();
          } else if (ev.t === 'tool') {
            cur = null; seg = ''; toolCard(ev); busySay(ev.name || 'tool');
          } else if (ev.t === 'tool_result') {
            toolResult(ev); busySay('Thinking');
          } else if (ev.t === 'ask') {
            cur = null; askUI(ev);
          } else if (ev.t === 'done') {
            j = ev;
          }
        }
      }
      if (!j) return false;             /* the stream ended without an answer */
      busyEnd();
      if (lastRow && lastRow.parentNode) lastRow.parentNode.removeChild(lastRow);
      var took = (Date.now() - t0) / 1000;
      traceEnd('rejoined · ' + (took < 60 ? took.toFixed(1) + 's'
        : Math.floor(took / 60) + 'm' + String(Math.round(took % 60)).padStart(2, '0') + 's'));
      var txt = lastSeg || j.text || acc;
      if (!txt) return false;
      bubble('cc', txt);
      log.push({ k: 'cc', t: j.text || acc || txt });
      chatSave(logKey(), log);
      if (j.session) loadSessions();
      return true;
    } catch (e) {
      /* EVERY failure lands here and NONE of it is the reader's business:
         an abort, a dropped socket, a restarted server, a parse error. It goes
         to the drawer's own diagnostics and nowhere else. */
      diag('REJOIN', 'gave up quietly: ' + (e.name || e.message || 'error'));
      return false;
    } finally {
      reattaching = false;
      if (painted) { busyEnd(); traceEnd(); chatBusy(false); }
    }
  }

  /* Rejoin a turn that is still running with nobody watching it.
     Returns true when it actually attached, so the caller can fall back to
     reading the transcript when nothing is live. */
  function chatRejoin() { return chatAttach(); }

  async function chatSend(preset, opts) {
    /* Attach mode replays the SAME reader loop against /_board/attach instead
       of /_board/chat. Everything below the fetch is identical on purpose: a
       rejoined turn has to paint exactly like the live one it is a continuation
       of, which is the whole difference between this and the transcript
       replay it replaces. */
    /* ⚠️ DEAD PATH. `chatRejoin` calls `chatAttach` now, so nothing passes
       `{attach:true}` any more and every `attach` branch below is unreachable.
       It is left in place rather than surgically removed from a 250-line
       function at the end of a long session, but DO NOT FIX BUGS IN IT: that
       is exactly how the same rejoin defect got patched twice and missed a
       third branch (260802). The live rejoin is `chatAttach`, above. */
    var attach = !!(opts && opts.attach);
    var ta = chat.querySelector('textarea'), btn = chat.querySelector('.send');
    if (inflight) return attach ? false : chatStop();   // 正在跑 → 这一下是「停」
    if (!cq) return false;
    var msg = attach ? '' : (preset || ta.value).trim();
    if (!attach && !msg) return false;
    if (!preset && !attach) ta.value = '';
    /* On a phone the utility controls are deliberately folded.  Starting the
       next turn must give its live answer the room, rather than leaving model,
       permission and session metadata above the composer. */
    setUtility(false);
    chatBusy(true);
    var log = chatLoad(logKey());
    if (!attach) {
      bubble('you', msg); bdJump(); log.push({ k: 'you', t: msg }); chatSave(logKey(), log);
    }
    diag(attach ? 'REJOIN' : 'SEND', attach ? ('at cursor ' + curGet()) : msg.slice(0, 60));
    traceStart();
    /* A REJOIN IS A PROBE, AND A PROBE THAT FINDS NOTHING MUST SAY NOTHING.
       The sync heartbeat calls this on a timer to ask whether a turn is running
       with nobody watching, so on a quiet page it fires over and over — and it
       used to paint "Rejoining" every time, then let the watchdog escalate to
       "no reply for 60s — ⏹ to stop" and a diagnostics button, for a question
       whose honest answer was "nothing is running" (JL 260802: "why it is
       always indicating the rejoining? what is it about?"). So the label waits
       for the first real event: a rejoin that finds a live turn paints exactly
       as before, and one that finds nothing is invisible. */
    if (!attach) busyStart('Thinking');
    var ctrl = new AbortController();
    inflight = { ctrl: ctrl, file: cq.file };
    var stoppedByUser = false;
    inflight.mark = function () { stoppedByUser = true; };
    /* Watchdog. The fetch can hang with no event ever arriving, and then the
       code below never reaches chatBusy(false): red stop button, dead drawer,
       nothing moving. Report the silence, then give up rather than hang. */
    var lastEv = Date.now();
    /* A silent PROBE is the expected case, not a hang: give up in seconds and
       without a word. A real turn keeps the long, loud timings. */
    var QUIET_WARN = attach ? Infinity : 45000;
    var QUIET_GIVEUP = attach ? 6000 : 420000;
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
      var r = await fetch(attach ? '/_board/attach' : '/_board/chat', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        signal: ctrl.signal,
        body: JSON.stringify(attach
        ? { path: boardPath(), file: cq.file,
            group: (cq && cq.group) || undefined, cursor: curGet() }
        : { path: boardPath(), file: cq.file,
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
        /* A REJOIN that is refused is not the reader's problem and must never
           reach the transcript. A server older than the ring answers 404 to
           /_board/attach, and because the drawer asks on open, on focus and on
           a 25s heartbeat, the polite version of this bug painted a ⚠ bubble
           into the conversation several times a minute and made a working
           drawer look broken (found 260802 by opening the live board and
           clicking the button, which is the only way this was ever going to
           show up). Fail silently and let the caller read the transcript. */
        if (attach) {
          busyEnd(); traceEnd();
          clearInterval(watchdog); window.__pendingSince = 0;
          inflight = null; chatBusy(false);
          return false;
        }
        busyEnd(); traceEnd();
        bubble('sys', '⚠ ' + (errTxt || ('the server refused this turn (HTTP ' + r.status + ')')));
        clearInterval(watchdog); window.__pendingSince = 0;
        inflight = null; chatBusy(false); ta.focus();
        return false;
      }
      /* R1: /_board/attach answers one of two ways — the rest of a live turn as
         NDJSON, or a plain JSON `live:false`. Nothing running is the ORDINARY
         case, not an error: leave the drawer exactly as it was and let the
         caller fall back to reading the transcript. */
      if (attach && (r.headers.get('Content-Type') || '').indexOf('ndjson') < 0) {
        diag('REJOIN', 'nothing live');
        busyEnd(); traceEnd();
        clearInterval(watchdog); window.__pendingSince = 0;
        inflight = null; chatBusy(false);
        return false;
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
          /* A ring keepalive is NOT progress. The watchdog exists to notice a
             turn that has gone silent, so counting a ping as activity would
             make a hung turn look healthy forever. */
          /* A keepalive is not progress FOR A TURN — the watchdog exists to
             notice one that has gone silent, so counting it would make a hung
             turn look healthy. For a REJOIN it is the opposite: a ping is the
             server saying the turn is alive and still working, and the only
             thing the rejoin is waiting for. Without this the 6s give-up below
             fired on every single rejoin, because between events the ring
             sends nothing else (JL 260802: ~120 × "Stopped waiting"). */
          if (ev.t === 'ping') { if (attach) lastEv = Date.now(); continue; }
          lastEv = Date.now();
          /* ask the DOM, not `busyWhat`: that variable keeps its last value
             after a turn ends, so it cannot answer "is anything painted now" */
          if (attach && !document.querySelector('#chat .busy')) busyStart('Rejoining');
          /* Remember where we are, every event, so an interruption at any
             point can be rejoined at the next one rather than from the top. */
          if (typeof ev.n === 'number') curSet(ev.n + 1);
          if (ev.t !== 'delta' && ev.t !== 'think') diag('ev:' + ev.t, ev.name || ev.text || '');
          if (ev.t === 'gap') {                   // rejoined past the buffer's front
            bubble('sys', '⚠ ' + (ev.text || 'reconnected mid-turn; some earlier output is past the buffer'));
          } else if (ev.t === 'stage') {          // real progress while nothing streams yet
            busySay(ev.text.length > 46 ? ev.text.slice(0, 46) + '…' : ev.text);
          } else if (ev.t === 'think') {          // 思考过程 → 折叠块，边想边展开
            busySay('Thinking');
            if (!thinkEl) thinkEl = thinkBubble();
            thinkAcc += ev.text;
            thinkEl.querySelector('.tk-body').textContent = thinkAcc;
            bdAuto();
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
      /* The context meter, which the CLI shows under /context and the drawer
         never had (JL 260801: "我怎么看到我现在这个 context 的 usage，就是用了
         百分之几"). It rides the turn's own done event, so it costs no extra
         call, and it is absent rather than wrong on an SDK that cannot report
         it. Shown on the trace label, beside how long the turn took. */
      var ctxTxt = '';
      if (j.ctx && typeof j.ctx.pct === 'number') {
        var k = function (n) {
          return typeof n === 'number' ? Math.round(n / 1000) + 'k' : '?';
        };
        ctxTxt = ' · ctx ' + Math.round(j.ctx.pct) + '%'
               + (j.ctx.used ? ' (' + k(j.ctx.used) + '/' + k(j.ctx.max) + ')' : '');
        var cw = chat.querySelector('.cost');
        if (cw) cw.textContent = 'ctx ' + Math.round(j.ctx.pct) + '%'
                               + (typeof j.usd === 'number' ? ' · $' + j.usd.toFixed(3) : '');
      }
      traceEnd(tookTxt + ' · finished ' + stamp + ctxTxt);
      var txt = j.ok ? (lastSeg || j.text || acc ||
                        '(no text reply — it may have only used tools)')
                     : ('⚠ ' + (j.err || 'failed'));
      if (j.stopped) txt = txt + '\n(you stopped this turn, so it may be unfinished)';
      bubble('cc', txt);              /* the answer, once, at full size */
      /* history keeps the WHOLE turn, not just its last line */
      log.push({ k: 'cc', t: (j.ok ? (j.text || acc || txt) : txt) });
      chatSave(logKey(), log);
      if (j.ok) {
        // 这一轮聊到的 session 现在就是 current（服务器已写回头部）——
        // 拣选状态归位、清单重拉，免得下一条还带着旧的点名
        if (j.session) {
          /* The server has just told us which session this turn actually ran
             in, which for a NEW one is the first time that id exists anywhere.
             Move the log we wrote under the '#new' key onto the real id, adopt
             it as the shown session, and repaint the header — otherwise a new
             session's first turn is stored where nothing will ever look for it
             and `.sid` keeps naming the session you started from. */
          if (j.session !== activeSid) {
            var oldKey = logKey();
            activeSid = j.session;
            chatSave(logKey(), log);
            try { localStorage.removeItem(CHATK(oldKey)); } catch (e) {}
            paintSid(activeSid);
          }
          chatSid = ''; sessName = ''; loadSessions();
        }
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
      /* A REJOIN THAT FAILS IS NEVER THE READER'S PROBLEM, and it must never
         reach the transcript. The drawer rejoins on open, on focus, on a 25s
         heartbeat and on four backoff timers, so one noisy failure path is not
         one message: it is a wall of them. JL got ~120 of "Stopped waiting.
         The server got the stop signal too." on one page (260802), and that
         sentence was a lie twice over — nobody pressed stop and no stop signal
         was sent. The 404 half of this was made silent earlier the same day;
         this is the half that was missed, which is abort, network and anything
         else that throws. Fail quietly and let the transcript speak. */
      if (attach) {
        clearInterval(watchdog); window.__pendingSince = 0;
        inflight = null; chatBusy(false);
        diag('REJOIN', 'gave up quietly: ' + (e.name || e.message || 'error'));
        return false;
      }
      if (!(e.name === 'AbortError' && stoppedByUser)) {
        bubble('sys', e.name === 'AbortError'
          ? 'Stopped waiting. The server got the stop signal too.'
          : '⚠ ' + e.message);
      }
      /* KEEP WHAT ARRIVED. The answer was only written to the local log at
         'done', so a turn that never got there left the question saved and the
         reply lost: reopening showed your own message with nothing under it,
         and the text seemed to reappear only once a new message was sent
         (JL 260801: "只有我发一个新的 message 之后，你的 response 才能显现出来").
         Whatever streamed is real; save it, marked, instead of dropping it. */
      try {
        if (acc && acc.trim()) {
          /* `partial` is what lets syncFromServer REPLACE this later. Without
             it the local log is the same LENGTH as the server's, and the
             length test concluded the server knew nothing new, so a half
             answer could never be upgraded to the real one. */
          log.push({ k: 'cc', t: acc + '\n\n(this turn was cut short)', partial: true });
          chatSave(logKey(), log);
        }
      } catch (e2) {}
    }
    clearInterval(watchdog);
    window.__pendingSince = 0;
    inflight = null; chatBusy(false);
    if (!attach) ta.focus();     // a rejoin must not steal focus from a reader
    drainQueue();                       // whatever you typed while it ran
    if (followPending && !inflight) follow();   // you navigated while it ran
    return true;
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
  var termT = null, termWS = null, xtermP = null, termSubs = null;
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
    /* MEASURE THE FRAME WHEN THE HOST MEASURES NONSENSE. Inside QD5's chat
       PANE the drawer is `position:fixed;inset:0` and `.tm` reported a
       clientWidth of 16, which is its horizontal padding and nothing else. The
       guard below then returned every time, so xterm kept whatever size it was
       built with — a 501px screen inside a 16px box, 64 columns that never
       changed however the pane was dragged. That is the messy terminal layout
       (JL 260802), and it is measurable rather than a matter of taste.
       The viewport is always right, so fall back to it. */
    if (w < 40 && window.innerWidth >= 40) w = window.innerWidth;
    if (h < 40 && window.innerHeight >= 40) {
      var hd = chat.querySelector('.hd');
      h = window.innerHeight - (hd ? hd.getBoundingClientRect().height : 0) - 8;
    }
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
    if (termSubs) {
      termSubs.forEach(function (d) { try { d.dispose(); } catch (e) {} });
      termSubs = null;
    }
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
      /* A FRAME CAN ARRIVE AFTER THE TERMINAL IS GONE. `onclose` has guarded
         against a null `termT` since it was written; this one never did, so
         switching the pane from the TUI to the GUI while bytes were still in
         flight threw `Cannot read properties of null (reading 'write')` into
         the page (found 260802 by a suite that does exactly that switch).
         Nothing to write to means nothing to write. */
      if (!termT) return;
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
    /* Bind input ONCE per terminal, not once per socket (JL 260801: "I enter
       one letter, it types two letters").

       `connectWS` runs again on every reconnect, and the Terminal instance
       survives that, so each reconnect used to add ANOTHER onData listener to
       the same xterm. xterm fires all of them, so one keystroke was written
       twice after the first drop, three times after the second, and so on:
       `what happened?` arrived as `wwhhaatt hhaappppeenneedd??`. The listeners
       are disposables, so drop the previous pair before adding the next, and
       always send through the CURRENT socket rather than the one captured when
       the listener was created. */
    if (termSubs) {
      termSubs.forEach(function (d) { try { d.dispose(); } catch (e) {} });
    }
    termSubs = [
      termT.onData(function (s) {
        if (termWS && termWS.readyState === 1) termWS.send('0' + s);
      }),
      termT.onResize(function (sz) {
        if (termWS && termWS.readyState === 1)
          termWS.send('1' + JSON.stringify({ columns: sz.cols, rows: sz.rows }));
      })
    ];
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
  /* A FRAME CAN CHANGE SIZE WITHOUT A WINDOW RESIZE. Dragging the split's
     handle changes the chat pane's width and fires no `resize` inside it, so
     the terminal kept its old column count and the text ran wrong until
     something else happened to refit it. Watch the box itself. */
  (function () {
    if (typeof ResizeObserver !== 'function') return;
    var host = chat.querySelector('.tm');
    if (!host) return;
    var t = null;
    new ResizeObserver(function () {
      clearTimeout(t);
      t = setTimeout(function () { if (termOn) fitTerm(); }, 80);
    }).observe(host);
  })();
  /* Anything that changes the pane's box must refit, not just a window resize:
     the strip appearing, the drawer being dragged, a font swap. One observer on
     the pane covers every cause, including ones not invented yet. */
  (function () {
    var host = chat.querySelector('.tm');
    if (!host || !window.ResizeObserver) return;
    var t = null;
    new ResizeObserver(function () {
      clearTimeout(t);
      t = setTimeout(function () { if (termOn) fitTerm(); }, 60);
    }).observe(host);
  })();
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

  /* A release that nobody waits for is still a release the NEXT open must not
     overtake. Flipping the view before the round trip made the click instant
     and made this race possible: switch to the chat and straight back, and the
     open reached the server first, so the park landed on the terminal that had
     just been attached and the pane stayed empty (measured 260802). Whoever
     starts a terminal waits for the hand-back to finish first. */
  var releasing = null;
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
  /* Which terminal is on screen, and which sessions have one running. The
     PICKER owns choosing (JL 260801: "为什么不把这个 session 放到那个 session
     的选择那里去"), so this file only tracks state and attaches; a second
     chooser above the pane was one UI too many, and it stole rows from the
     terminal every time it rendered. */
  var termKeyNow = null, termLive = [];
  async function loadTermList() {
    if (!cq || !cq.file) return [];
    try {
      var r = await fetch('/_board/term-probe', { method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: boardPath(), file: cq.file,
                               group: (cq && cq.group) || undefined }) });
      var j = await r.json();
      termLive = (j && j.terminals) || [];
    } catch (e) { termLive = []; }
    return termLive;
  }
  window.__boardTermLive = function () { return termLive; };
  window.__boardTermKeyNow = function () { return termKeyNow; };
  window.__boardTermAttach = function (sid) { return termOpen(true, sid); };

  async function termOpen(quiet, wantSession) {
    if (!cq) return false;
    /* ...but awaited HERE, and never for long. A hand-back that hangs must not
       be able to stop a terminal from opening: the race this closes is a few
       hundred milliseconds wide, so a second is already generous, and the
       failure mode of waiting forever is a drawer that says "Starting a
       terminal…" and never does (measured 260802, one edit after the race). */
    if (releasing) {
      try {
        await Promise.race([releasing, new Promise(function (r) { setTimeout(r, 1000); })]);
      } catch (e) {}
    }
    if (!quiet) say('Starting a terminal for this question…');
    try {
      var r = await fetch('/_board/term', { method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: boardPath(), file: cq.file,
                               group: (cq && cq.group) || undefined,
                               session: (wantSession !== undefined && wantSession !== null)
                                        ? wantSession : chatSid,
                               name: sessName }) });
      var j = await r.json();
      if (!j.ok) { say('⚠ ' + j.err); return false; }
      // 拣选的那段（或新开的）从这一刻起就是 current —— 状态归位、清单重拉
      // 抽屉那半边也得跟着换：终端和聊天共用一个 session，
      // 只把 chatSid 归零会让聊天框还停在上一段的抬头和记录上
      if (j.session && j.session !== activeSid) { activeSid = j.session; paintSid(activeSid); }
      if (chatSid) { chatSid = ''; sessName = ''; loadSessions(); }
      termKeyNow = j.key;
      termView(true);
      await mountTerm(j.key);
      loadTermList();                 // so the picker can mark what is running
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
  /* TUI FIRST (JL 260801: "make the TUI to be the default version").
     Opening the drawer now goes straight to the terminal, because the TUI is
     the real CLI and the SDK chat is the rebuilt one. `.term` still toggles
     back, and the choice is remembered per machine so a reader who prefers the
     chat box is not overruled on every page. */
  var TUIDEF = 'board-tui-default';
  function tuiIsDefault() {
    try { return localStorage.getItem(TUIDEF) !== '0'; } catch (e) { return true; }
  }
  window.__boardTuiDefault = tuiIsDefault;
  window.__boardOpenDefaultView = async function () {
    if (!tuiIsDefault() || termOn || !cq) return false;
    return await termOpen(true);
  };

  /* Putting the caret BACK. A live update swaps div.wrap and then re-resolves
     the URL fragment, and setting location.hash moves focus to the target
     element, so a reader who was typing in the terminal lost the caret on every
     board update and had to click the pane again (JL 260801: "我正在打字，然后
     它突然更新了，我就打不了字了"). xterm owns a hidden textarea, so ask xterm
     rather than poking at the DOM. */
  /* Type a prompt INTO the running CLI. Quick actions and "add to chat" used to
     call the SDK path only, so in the TUI they did nothing at all (JL 260801:
     "add to chat 以及一些 quick question ... 在 TUI work 不了").

     The text is typed but NOT submitted: in a chat box the send is the whole
     gesture, while in a terminal the prompt is a draft you may want to extend
     before pressing Enter, and a button that silently runs something in a real
     CLI is worse than one that does nothing. Newlines become the CLI's own
     continuation sequence so a multi-line prompt does not submit halfway. */
  window.__boardTermType = function (text, opts) {
    if (!termOn || !termWS || termWS.readyState !== 1) return false;
    var s = String(text || '').replace(/\r?\n/g, '\\\r');
    /* CLEAR THE PROMPT FIRST. Typing blindly appends to whatever draft is
       already sitting there, so a quick action ran together with the reader's
       half-written sentence into one unreadable run-on line: "hello
       worldAnswer only, do not edit any file: …" (JL 260801: "这个字跟我的
       input message 叠到了一块儿"). Escape is the CLI's own "clear the input",
       so the prompt starts empty and what lands is exactly what was asked for.
       Pass {append:true} to add to a draft on purpose. */
    if (!(opts && opts.append)) {
      /* A lone ESC does NOT clear it: the app waits to see whether more bytes
         follow, so ESC + text arrives as Alt+<key> and the draft survives.
         Measured 260801, and the prompt then read
         "hello worldAnswer only…immediatelyMYDRAFTAnswer only…".
         Backspace has no such ambiguity and is a no-op on an empty prompt, so
         send a generous run of it: deterministic, and it costs 2KB. */
      var ws0 = termWS;
      ws0.send('0' + new Array(2001).join('\u007f'));
      setTimeout(function () {
        if (ws0 && ws0.readyState === 1) ws0.send('0' + s);
        window.__boardTermFocus();
      }, 140);
      return true;
    }
    termWS.send('0' + s);
    window.__boardTermFocus();
    return true;
  };

  window.__boardTermFocused = function () {
    var host = chat.querySelector('.tm');
    return !!(termOn && host && host.contains(document.activeElement));
  };
  window.__boardTermFocus = function () {
    try { if (termT) termT.focus(); } catch (e) {}
  };

  window.__boardTermOn = function () { return !!termOn; };
  window.__boardTermReopen = async function () {
    /* RESTORE MUST NOT OVERRULE THE READER. `80-restore.js` calls this when the
       saved drawer state says a terminal was open, which is right after a plain
       reload and WRONG right after someone clicked 💬 GUI: the click set the
       mode, the pane came up correctly in GUI, and then this reattached the
       parked terminal a second later and put the strip back on >_ TUI. That is
       the whole of "I click GUI and get TUI" (JL 260802), measured at +1.5s
       correct and +2.5s flipped. The chosen mode is the authority. */
    if (!cq || termOn || !tuiIsDefault()) return false;
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
      try { localStorage.setItem(TUIDEF, '0'); } catch (e) {}   // you chose chat
      /* SWAP THE VIEW FIRST, HAND THE SESSION BACK AFTER. The release is a
         POST, and awaiting it before flipping the panel meant the click showed
         nothing for a round trip — a third of a second of the old view, which
         is exactly what reads as "not smooth" (JL 260802, measured at 284 ms).
         Nothing downstream depends on the order: the park is idempotent and the
         drawer it reveals does not touch the PTY. */
      termView(false);
      say('Terminal closed, session handed back');
      releasing = termRelease(cq.file, cq.group)   // not awaited HERE...
        .catch(function () {})
        .then(function () { releasing = null; });
      return;
    }
    try { localStorage.setItem(TUIDEF, '1'); } catch (e) {}     // you chose TUI
    /* THE OTHER DIRECTION MUST NOT CHEAT. Revealing the terminal panel before
       the server names the PTY was tried and reverted the same minute: when the
       open then fails — a 409 because something else holds the session, say —
       it leaves a black empty panel with nothing on the way, which is worse
       than the wait it saved. `termOpen` reveals it only once it has a key.
       Measured: the pane sat at rows=0 for the whole 2.5 s film. */
    await termOpen(false);
  };

  /* 🖼 Attach an image WITHOUT a clipboard (QD14, JL 260801: "然后我们手机上的话，
     如何 upload 这个 image 呢?").

     Until now the only two ways an image could enter the board were `paste`
     listeners — the terminal pane in 30-terminal.js and the comment box in
     10-comment/40-paste.js — and pasting an image into a pane is a DESKTOP
     gesture. A phone offers a photo library and a camera, and both of those are
     an `<input type="file">`, which this board never had. So on a phone the
     board simply could not take a screenshot or a photo at all.

     The server half needed nothing: /_board/image already accepts a base64 data
     URL and writes into the board's fig/, so the whole gap was this gesture.

     Why it re-encodes instead of forwarding the file untouched: live/write.py
     caps an image at 8MB and accepts png/jpeg/gif/webp ONLY, while a modern
     phone routinely shoots larger than the cap and an iPhone shoots HEIC, which
     is not on that list. Drawing the file through a canvas both shrinks it and
     normalises the format, so one button serves a 12MP photo and a screenshot.
     A small PNG is passed through instead, because re-encoding a screenshot to
     JPEG blurs exactly the text you took the screenshot to show. */
  var PICK_MAX = 1600, PICK_Q = 0.85, PICK_PNG_KEEP = 3 * 1024 * 1024;

  function shrinkImage(file) {
    return new Promise(function (res, rej) {
      if (file.type === 'image/png' && file.size < PICK_PNG_KEEP) {
        var fr = new FileReader();
        fr.onload = function () { res(fr.result); };
        fr.onerror = function () { rej(new Error('could not read that file')); };
        return fr.readAsDataURL(file);
      }
      var url = URL.createObjectURL(file);
      var img = new Image();
      img.onload = function () {
        var w = img.naturalWidth, h = img.naturalHeight;
        var s = Math.min(1, PICK_MAX / Math.max(w, h));
        var c = document.createElement('canvas');
        c.width = Math.max(1, Math.round(w * s));
        c.height = Math.max(1, Math.round(h * s));
        c.getContext('2d').drawImage(img, 0, 0, c.width, c.height);
        URL.revokeObjectURL(url);
        /* toDataURL throws on a tainted canvas; a local file cannot taint one,
           so this only fires on a decode the browser half-managed. */
        try { res(c.toDataURL('image/jpeg', PICK_Q)); }
        catch (e) { rej(new Error('could not convert that image')); }
      };
      img.onerror = function () {
        URL.revokeObjectURL(url);
        rej(new Error('this browser cannot decode that image (HEIC outside Safari?)'));
      };
      img.src = url;
    });
  }

  /* Where the path GOES depends on which half is showing, because the two halves
     want different things: the CLI wants a bare repo-root-relative path it can
     hand to its Read tool, the chat composer wants markdown it can send. Both
     are repo-root-relative rather than board-relative, because the session's cwd
     is the SPACE root and a bare fig/… does not resolve there. */
  async function attachImageFile(file) {
    if (!cq || !file) return;
    var data;
    try { data = await shrinkImage(file); }
    catch (e) { return say(e.message); }
    var j = null;
    try {
      j = await post('/_board/image',
        { file: cq.file, name: file.name || 'photo', data: data });
    } catch (e) { j = null; }
    if (!j || !j.ok) {
      return say((j && j.err) || 'image upload failed (is serve.py running?)');
    }
    var dir = boardDirPath().replace(/^\//, '');
    var path = (dir ? dir + '/' : '') + j.rel;
    if (termOn && termWS && termWS.readyState === 1) {
      termWS.send('0' + path);
      say('Attached ' + j.rel + ' — it is on the prompt line, press Enter');
    } else {
      var ta = chat.querySelector('.ft textarea');
      if (ta) insertAtCursor(ta, '![image](' + path + ')');
      else say('Saved ' + j.rel);
    }
  }

  (function () {
    var btn = chat.querySelector('.imgpick');
    if (!btn) return;
    var inp = document.createElement('input');
    inp.type = 'file';
    inp.accept = 'image/*';
    /* deliberately NOT `capture`: that attribute forces the camera and takes the
       photo library away, and a screenshot already in the library is the common
       case here. Without it a phone offers both. */
    inp.style.display = 'none';
    chat.appendChild(inp);
    btn.onclick = function () { inp.value = ''; inp.click(); };
    inp.onchange = function () {
      if (inp.files && inp.files[0]) attachImageFile(inp.files[0]);
    };
  })();

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
  // The sidebar needs the same answer and must not compute it a second way.
  window.__boardDocPage = docPage;
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

  /* ── THE CHAT PICKER (JL 260802: "could we make it a list that I can choose
     GUI-Chat or TUI-Chat") ────────────────────────────────────────────────
     This board has TWO chats and one button, so which one you got was decided
     by a stored preference you could not see, and the only way to switch was a
     `>_` in the drawer header that is hard to find on a phone ("我咋按这个键啊",
     260801). The list makes the pair visible at the moment you are choosing.

     It also carries the thing no surface reported until now: whether something
     is ALREADY running. The ring answers that for a turn and `term-probe` for
     a parked PTY, so the extra tap buys a fact rather than costing one.

     Deliberately the FAB only. A per-card `🤖 Chat` means "talk about THIS
     card" and its reader has already decided; giving twelve buttons a chooser
     would be noise. Those keep going straight to the last-used view. */
  var TUIKEY = 'board-tui-default';
  function tuiDefault() {
    try { return localStorage.getItem(TUIKEY) !== '0'; } catch (e) { return true; }
  }
  var pick = document.createElement('div');
  pick.id = 'chatpick';
  pick.hidden = true;
  pick.setAttribute('role', 'menu');
  document.body.appendChild(pick);

  function pickClose() {
    pick.hidden = true;
    document.removeEventListener('pointerdown', pickAway, true);
    document.removeEventListener('keydown', pickKey, true);
  }
  function pickAway(e) {
    if (!pick.contains(e.target) && e.target !== fab) pickClose();
  }
  function pickKey(e) { if (e.key === 'Escape') { e.preventDefault(); pickClose(); } }

  function pickTarget(tgt) {
    if (!tgt) return { file: 'board.md' };
    if (tgt.group) return { file: 'board.md', group: tgt.group };
    return { file: tgt.getAttribute && tgt.getAttribute('data-file') || 'board.md' };
  }

  /* Both questions at once, and neither is allowed to hold the menu up: a
     picker that waits on the network is a picker that feels broken, so the
     rows paint immediately and the state lines fill in when they arrive. */
  function pickState(body, paint) {
    fetch('/_board/attach', { method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(Object.assign({ path: boardPath(), probe: 1 }, body)) })
      .then(function (r) { return r.json(); })
      .then(function (j) { paint('gui', j && j.live ? '⚡ a turn is still running' : ''); })
      .catch(function () {});
    fetch('/_board/term-probe', { method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(Object.assign({ path: boardPath() }, body)) })
      .then(function (r) { return r.json(); })
      .then(function (j) {
        var n = (j && j.terminals || []).length;
        paint('tui', n ? '🟢 a session is parked here' : '');
      })
      .catch(function () {});
  }

  function pickOpen() {
    var tgt = chatTarget();
    var tui = tuiDefault();
    // 🔌 The menu is a REGISTRY now (JL 260807): the board contributes the two chats,
    // a plugin contributes its own surface, and an entry that cannot act on the open
    // page is never drawn. `data-v` stays the id so the existing handler still reads it.
    var page = window.boardPlugins ? window.boardPlugins.livePage() : null;
    // TWO GROUPS, ONE LIST (JL 260808). The shell splits these into two buttons because
    // it has a bar to put them in; the in-page picker is one popup, so the split shows
    // as two titled groups. Same registry, same ids, so `data-v` still resolves.
    // A group with nothing applicable prints no heading: an empty heading claims the
    // page has a workflow and then shows none, which is worse than saying nothing.
    function group(title, menu) {
      var rows = window.boardPlugins
        ? window.boardPlugins.applicable(page, menu) : [];
      if (!rows.length) return '';
      return '<div class="pkh">' + title + '</div>' + rows.map(function (e) {
        var dot = e.id === 'gui' ? (tui ? '' : '●')
                : e.id === 'tui' ? (tui ? '●' : '') : '';
        return '<button class="pk" data-v="' + e.id + '" role="menuitem">'
          + '<b>' + e.label + '</b><i>' + (e.hint || '') + '</i>'
          + '<u></u><s>' + dot + '</s></button>';
      }).join('');
    }
    pick.innerHTML = group('\u{1F50C} Plugin', 'plugin')
                   + group('\u{1FA9C} Workflow', 'workflow');
    pick.hidden = false;
    document.addEventListener('pointerdown', pickAway, true);
    document.addEventListener('keydown', pickKey, true);
    pickState(pickTarget(tgt), function (which, text) {
      var row = pick.querySelector('.pk[data-v="' + which + '"] u');
      if (row) row.textContent = text;
    });
    pick.querySelectorAll('.pk').forEach(function (b) {
      b.onclick = function () {
        var id = b.dataset.v;
        var hit = (window.boardPlugins ? window.boardPlugins.all() : [])
                    .filter(function (e) { return e.id === id; })[0];
        pickClose();
        if (hit) hit.open(window.boardPlugins.livePage());
      };
    });
    var first = pick.querySelector('.pk');
    if (first) first.focus();
  }

  // The board owns exactly two surfaces and registers them like anybody else, so the
  // engine has no privileged path a plugin cannot take. Both are PLUGINS: they open a
  // surface to the right and neither knows or cares where you are on the page, which
  // is exactly the line the Workflow menu is on the other side of.
  if (window.boardPlugins) {
    window.boardPlugins.register({
      id: 'gui', label: '\u{1F4AC} GUI Chat',
      hint: 'the SDK drawer: gated edits, diffs, tool cards',
      open: function () {
        try { localStorage.setItem(TUIKEY, '0'); } catch (e) {}
        chatOpen(chatTarget() || 'board');
      } });
    window.boardPlugins.register({
      id: 'tui', label: '⌨️ TUI Chat',
      hint: 'the real CLI in a terminal: long jobs, skills',
      open: function () {
        try { localStorage.setItem(TUIKEY, '1'); } catch (e) {}
        chatOpen(chatTarget() || 'board');
      } });
  }

  fab.onclick = function () {
    if (!pick.hidden) return pickClose();
    pickOpen();
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
  /* "Add to chat" in the TUI (JL 260801). The SDK half shows the quote in a
     focus card and augments the next message; a real CLI has no such card, so
     the address and the sentence are typed into the prompt instead, unsubmitted,
     for the reader to finish. Same gesture, whichever half is open. */
  function sentenceToTerm(ref, sentence, contentPath) {
    if (!(window.__boardTermOn && window.__boardTermOn())) return false;
    var where = (contentPath ? contentPath + ' · ' : '') + (ref || '');
    var q = 'About ' + where + ':\n> ' + String(sentence || '').trim() + '\n';
    return !!window.__boardTermType(q);
  }

  window.__boardSentenceChat = async function (sec, ref, sentence, attached, contentPath) {
    if (!sec || !sec.classList.contains('q')) return;
    await chatOpen(sec);
    if (sentenceToTerm(ref, sentence, contentPath)) return;
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
    if (sentenceToTerm(path, block, file)) return;
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
/* 🏷 Labeling · the subjective-label plugin's surface, registered into the 🔌 Plugin menu.
 *
 * THIS IS THE WORKFLOW FOR A LABELING PAGE, AND IT CARRIES THAT PLUGIN'S NAME, NOT
 * A GENERIC ONE (JL 260807: "Labeling is the workflow"). A display plugin will register
 * 🖼 Display and that entry will be the display workflow. There is deliberately no
 * abstract "Workflow" entry: it would name a concept no plugin owns, and it would show
 * on every page whether or not it meant anything there.
 *
 * WHAT IT IS. The page's own lifecycle, drawn left to right, one cell per step,
 * with exactly one cell live and everything after it locked.
 *
 * ⚠️ WHERE THIS FILE OUGHT TO LIVE. With its plugin, at
 * `subjective-label/skills/haipipe-board-page-for-labeling/`, beside the contract it
 * serves. It sits in the board engine's assets only because `assets.py` concatenates
 * `assets/js/**` from THIS skill and has no way to load a file a plugin contributes.
 * That loader is owed; until it exists this file is a guest here, and the registration
 * below is written so that moving it changes nothing but the path.
 *
 * WHERE ITS DATA COMES FROM. `## States`, and nothing else. Each `### A<n>` group
 * in States is one STEP, and the step's state is the WORST of its rows. There is no
 * second source and no new markdown: a page that keeps States true keeps this true.
 * JL 260807: "这个console就是我们人机交互的地方" — so it lives in the live layer,
 * where it cannot go stale against the file the way a `## Console` section would.
 *
 * WHY THE AIM GROUPS ARE THE STEPS. Every page type already declares an ordered
 * lifecycle in its own Aims: a labeling page runs init/round/gates/evaluate/complete,
 * a display page runs the acceptance ladder, a slide page runs per-slide acceptance.
 * Reading the groups means this surface generalizes with zero per-type declaration.
 *
 * LOCKED IS COMPUTED, NEVER STORED. The Board has five states (⬜ 🔨 🧠 ✅ ❄️) and no
 * "locked". A step is locked when an earlier step is not yet ✅, which is derived here
 * and never written back, so no page has to invent a sixth state to be drawn.
 *
 * SCRIPTS OFF. This whole surface disappears and the page's prose is untouched, which
 * is the invariant build.py asserts on every build.
 */
(function () {
  'use strict';

  /* The five current states, PLUS the legacy ones src/common.py still parses. A page
     written or edited by anything that reaches for 🟡 must not fall out of the strip
     (JL 260808: "why starting from Step 2?" — A1 had one 🟡 row and vanished whole). */
  var RANK = { '❄️': -1, '⏸️': -1, '⬜': 0, '🔨': 1, '🟡': 1, '🟠': 1,
               '🧠': 2, '✅': 3 };
  var LABEL = { '-1': 'on ice', '0': 'not started', '1': 'working',
                '2': 'waiting on a person', '3': 'done' };

  function livePage() {
    var secs = document.querySelectorAll('.wrap section.slide.q');
    for (var i = 0; i < secs.length; i++) {
      if (secs[i].offsetParent !== null) return secs[i];
    }
    return secs[0] || null;
  }

  /* One STEP per `### A<n>` group in States. Worst row wins, because a step with one
     row still open is not a step anybody may treat as finished. */
  function readSteps(page) {
    var now = page.querySelector('.sect.col.now');
    if (!now) return [];
    var out = [];
    now.querySelectorAll('details.csec').forEach(function (g) {
      var head = g.querySelector('summary');
      if (!head) return;
      // The summary reads "<emoji> <name> A<n>⧉🤖": the id TRAILS the name and drags the
      // copy and chat affordances with it. Take the id from the tail, then cut the tail off.
      var raw = (head.textContent || '').trim();
      /* States also holds `### Decision Now`, which is a question for a person and not a
         step. Only a group that carries an Aim id is one (JL 260808: it showed up as a
         seventh door). */
      if (!/\bA\d+\b/.test(raw)) return;
      var idm = /\bA(\d+)\s*[^A-Za-z0-9]*$/.exec(raw);
      var aid = idm ? idm[1] : null;
      var name = raw.replace(/\s*\bA\d+\s*[^A-Za-z0-9]*$/, '').trim();
      var worst = null, rows = [];
      g.querySelectorAll('.bt').forEach(function (r) {
        var ti = r.querySelector('.ti'), tl = r.querySelector('.ttl');
        var em = ti ? (ti.textContent || '').trim() : '';
        if (!(em in RANK)) return;
        rows.push({ emoji: em, text: tl ? (tl.textContent || '').trim() : '' });
        if (worst === null || RANK[em] < RANK[worst]) worst = em;
      });
      /* NEVER drop a group. A step that vanishes is worse than a step whose state is
         unreadable: the first hides that the step exists at all. */
      if (!rows.length) {
        out.push({ name: name, aid: aid, emoji: '❔', rank: 0, unknown: true,
                   rows: [{ emoji: '❔', text: 'no row here uses a state this surface '
                            + 'knows; the step is real, its state is not readable' }] });
        return;
      }
      out.push({ name: name, aid: aid, emoji: worst, rank: RANK[worst], rows: rows });
    });
    return out;
  }

  /* The live step is the first one not yet done. Everything after it is LOCKED, and
     an ❄️ step is skipped rather than blocking, because parking is deliberate. */
  function mark(steps) {
    var live = -1;
    for (var i = 0; i < steps.length; i++) {
      if (steps[i].rank !== 3 && steps[i].rank !== -1) { live = i; break; }
    }
    steps.forEach(function (s, i) {
      s.live = (i === live);
      s.locked = (live >= 0 && i > live && s.rank !== 3);
    });
    return live;
  }

  /* QF1 §1's five doors, in Aim-group order. `null` means the step closes on a human
     signoff and no command may stand in for it (QF1 §3.1), so the surface offers none. */
  var DOOR = { '1': '/sl-init', '2': '/sl-round', '3': null,
               '4': '/sl-evaluate', '5': '/sl-complete' };

  /* Each door's own options, asked BEFORE it runs (JL 260808: "provide the option and
     run"). A field is only here when the door genuinely takes it: inventing a knob the
     command ignores would teach a person a setting that does nothing. */
  var FIELDS = {
    '1': [ {k:'corpus', label:'data',            ph:'_WorkSpace/InLabStore/runs/<run>/items.jsonl'},
           {k:'trait',  label:'trait',           ph:'authority'},
           {k:'embed',  label:'embedding model', ph:'bge-m3'} ],
    '2': [ {k:'n',      label:'batch size',      ph:'60'} ],
    '4': [],
    '5': []
  };

  /* ⚠️ The map above is by Aim NUMBER, so it is only true on a page whose Aim groups ARE
     the five doors. A page organized by SUBJECT has an A1 that means the policy, not
     init, and offering `/sl-init` there would hand a person the wrong command with a
     straight face. So the surface checks first and says nothing rather than lying.
     The two shapes disagree today, which is an open Decision Now row on QBt11; this
     check is what keeps that disagreement from becoming a wrong button. */
  function stepShaped(steps) {
    return steps.some(function (s) { return /Step\s*[①②③④⑤]/.test(s.name); });
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  /* `A2 · 🔁 Step ② round` → the `§2` division this step opens. The Aim id's number
     is the division number, which is the base contract's own 1:1 rule between an Aim
     group and the Content division it belongs to; the checker enforces it as
     `group-no-division`, so this mapping is never a guess. */
  function divisionOf(step) { return step.aid; }

  function render(host, page) {
    var steps = readSteps(page);
    if (!steps.length) {
      host.innerHTML = '<div class="wf-empty">This page declares no Aim groups, '
        + 'so it has no lifecycle to walk. Workflow reads <code>## States</code>.</div>';
      return;
    }
    var live = mark(steps);
    var pid = page.id || '';

    var cells = steps.map(function (s, i) {
      var cls = 'wf-step' + (s.live ? ' live' : '') + (s.locked ? ' locked' : '')
              + (s.rank === 3 ? ' done' : '');
      var done = s.rows.filter(function (r) { return r.emoji === '✅'; }).length;
      if (s.unknown) cls += ' unknown';
      return '<button class="' + cls + '" type="button" data-i="' + i + '"'
        + ' title="' + esc(s.name) + '">'
        + '<span class="wf-n">' + (i + 1) + '</span>'
        + '<span class="wf-t">' + esc(s.name) + '</span>'
        + '<span class="wf-s">' + s.emoji + ' '
        + (s.unknown ? 'state unreadable' : LABEL[String(s.rank)]) + '</span>'
        + '<span class="wf-c">' + done + '/' + s.rows.length + '</span>'
        + (s.locked ? '<span class="wf-lock">🔒</span>' : '')
        + (s.live ? '<span class="wf-here">▲ you are here</span>' : '')
        + '</button>';
    }).join('<span class="wf-arrow">›</span>');

    var cur = live >= 0 ? steps[live] : null;
    var detail = '';
    if (cur) {
      var div = divisionOf(cur);
      detail =
        '<div class="wf-detail">'
        + '<div class="wf-dh">' + cur.emoji + ' ' + esc(cur.name) + '</div>'
        + '<ul class="wf-rows">'
        + cur.rows.map(function (r) {
            return '<li><span class="ti">' + r.emoji + '</span> ' + esc(r.text) + '</li>';
          }).join('')
        + '</ul>'
        + (div
            ? '<a class="wf-jump" href="#' + esc(pid) + '">§' + esc(div)
              + ' · open this step in Content ↗</a>'
            : '')
        + action(cur, stepShaped(steps))
        + '</div>';
    } else {
      detail = '<div class="wf-detail"><div class="wf-dh">✅ every step is done</div>'
             + '<p class="mut">Nothing on this page is waiting.</p></div>';
    }

    host.innerHTML =
      '<div class="wf-head">\u{1F3F7} Labeling · <b>' + esc(pid) + '</b>'
      + '<span class="mut"> · read from <code>## States</code>, never stored</span></div>'
      + '<div class="wf-strip">' + cells + '</div>'
      + detail;

    /* Live preview: the command line updates as the options are typed, so RUN never
       sends something the person has not read. */
    function refresh() {
      var el = host.querySelector('.wf-cmd');
      if (el && cur) el.textContent = composed(cur, host);
    }
    host.querySelectorAll('.wf-f').forEach(function (i) { i.oninput = refresh; });
    refresh();

    host.querySelectorAll('.wf-copy').forEach(function (b) {
      b.onclick = function () {
        try { navigator.clipboard.writeText(composed(cur, host)); b.textContent = 'copied'; }
        catch (e) {}
        setTimeout(function () { b.textContent = 'copy'; }, 1600);
      };
    });

    host.querySelectorAll('.wf-run').forEach(function (b) {
      b.onclick = function () {
        var note = host.querySelector('.wf-note');
        b.disabled = true; b.textContent = '…';
        sendToChat(prompt(cur, host, pid), function (err) {
          b.disabled = false; b.textContent = '▶ RUN';
          if (!note) return;
          note.textContent = err ? '⚠️ ' + err
            : '✅ handed to 💬 GUI Chat — watch the pane on the right';
        });
      };
    });

    host.querySelectorAll('.wf-step').forEach(function (b) {
      b.onclick = function () {
        var s = steps[+b.dataset.i];
        var d = divisionOf(s);
        var t = page.querySelector('.sect.col.content');
        if (t) t.open = true;
        if (d) {
          var heads = page.querySelectorAll('.sect.col.content details.csec');
          var want = heads[+d - 1];
          if (want) { want.open = true; want.scrollIntoView({ block: 'center' }); }
        }
      };
    });
  }

  /* QB7's law: what lands is what an author would have typed. The button copies the
     command; it does not run it, and it invents no syntax only a button could produce.
     A step whose door is null offers nothing, because a human signoff has no command. */
  /* One line, exactly what will be typed, shown before it is typed. QB7's law survives
     the change from copy to run: what lands is still what an author would have typed. */
  function composed(step, host) {
    var cmd = DOOR[step.aid];
    if (!cmd) return '';
    var parts = [cmd];
    (FIELDS[step.aid] || []).forEach(function (f) {
      var el = host.querySelector('.wf-f[data-k="' + f.k + '"]');
      var v = el && el.value.trim();
      if (v) parts.push('--' + f.k + ' ' + v);
    });
    return parts.join(' ');
  }

  /* RUN does not execute a program (JL 260808: "相当于是你通过点那个 button，然后它就是
     自动地去打开 GUI，然后去跟它交流"). It opens the GUI chat and says the task, so the
     agent does the work in a conversation a person can watch, interrupt and correct. That
     is why the chat is the right surface and a shell was the wrong one: this step is a
     judgment call with a person in it, not a batch job. */
  function shell() {
    try {
      var w = window.parent;
      return (w && w !== window && w.document.getElementById('mgui')) ? w : null;
    } catch (e) { return null; }
  }

  function sendToChat(text, done) {
    var sh = shell();
    if (!sh) return done('open this page inside the board viewer to use RUN');
    sh.document.getElementById('mgui').click();          // switch the pane to GUI
    var tries = 0;
    (function wait() {
      var ta = null;
      try { ta = sh.frames.chat.document.querySelector('#chat textarea'); } catch (e) {}
      if (!ta) {
        if (++tries > 40) return done('the GUI chat did not come up');
        return setTimeout(wait, 250);
      }
      ta.focus();
      ta.value = text;
      ta.dispatchEvent(new sh.frames.chat.Event('input', { bubbles: true }));
      ta.dispatchEvent(new sh.frames.chat.KeyboardEvent('keydown',
        { key: 'Enter', bubbles: true }));
      done(null);
    })();
  }

  /* What the agent is actually asked. The command line stays in it verbatim, so the
     person still sees exactly what they authorized, and the page is named so the agent
     writes its record back where it belongs. */
  function prompt(step, host, pid) {
    var lines = [
      'Run ' + step.name.replace(/^A\d+\s*·\s*/, '') + ' for this labeling page.',
      '',
      'page: ' + pid,
      'command: ' + composed(step, host)
    ];
    (FIELDS[step.aid] || []).forEach(function (f) {
      var el = host.querySelector('.wf-f[data-k="' + f.k + '"]');
      if (el && el.value.trim()) lines.push(f.label + ': ' + el.value.trim());
    });
    lines.push('', 'Follow the step contract on this page, stop at its human gate, '
      + 'and append the record to the page rather than only reporting it here.');
    return lines.join('\n');
  }

  function action(step, shaped) {
    if (!shaped) {
      return '<div class="wf-act wf-human">📄 This page\u2019s Content is organized by '
           + 'SUBJECT, not by the five doors, so no step command can be offered here. '
           + 'The shape is an open decision on <code>QBt11</code>.</div>';
    }
    var cmd = DOOR[step.aid];
    if (step.rank === 2) {
      return '<div class="wf-act wf-human">🧠 This step is waiting on a person. '
           + 'No command closes it.</div>';
    }
    if (!cmd) return '';
    var fs = (FIELDS[step.aid] || []).map(function (f) {
      return '<label class="wf-fl">' + esc(f.label)
        + '<input class="wf-f" data-k="' + esc(f.k) + '" placeholder="' + esc(f.ph) + '"></label>';
    }).join('');
    return '<div class="wf-act">'
      + (fs ? '<div class="wf-form">' + fs + '</div>' : '')
      + '<div class="wf-runrow">'
      + '<code class="wf-cmd">' + esc(cmd) + '</code>'
      + '<button class="wf-run" type="button" data-aid="' + esc(step.aid) + '">▶ RUN</button>'
      + '<button class="wf-copy" type="button">copy</button>'
      + '<span class="wf-note">opens 💬 GUI Chat and hands it this step</span>'
      + '</div></div>';
  }

  function panel() {
    var p = document.getElementById('wfpanel');
    if (p) return p;
    p = document.createElement('div');
    p.id = 'wfpanel';
    p.hidden = true;
    p.innerHTML = '<button class="wf-x" type="button" title="close (Esc)">✕ close</button>'
                + '<div class="wf-body"></div>';
    document.body.appendChild(p);
    p.querySelector('.wf-x').onclick = function () { p.hidden = true; };
    return p;
  }

  /* A surface a person cannot shut is worse than one they cannot open (JL 260808:
     "我关不掉labeling了"). Three ways out: the ✕, Escape, and choosing the entry again. */
  function open() {
    var page = livePage();
    if (!page) return;
    var p = panel();
    if (!p.hidden) { p.hidden = true; return; }        // the entry TOGGLES
    render(p.querySelector('.wf-body'), page);
    p.hidden = false;
  }

  document.addEventListener('keydown', function (ev) {
    if (ev.key !== 'Escape') return;
    var p = document.getElementById('wfpanel');
    if (p && !p.hidden) { p.hidden = true; }
  });

  /* Re-render in place when the router swaps the page under an open panel, so the
     surface can never show one page's steps under another page's title. */
  window.addEventListener('board:updated', function () {
    var p = document.getElementById('wfpanel');
    if (p && !p.hidden) open();
  });

  /* Registered, not wired: the engine holds no branch for this surface, and `applies`
     keeps it off every page that is not a labeling page. */
  if (window.boardPlugins) {
    window.boardPlugins.register({
      id: 'labeling',
      label: '\u{1F3F7} Labeling',
      hint: 'this run’s steps, left to right, one live',
      // 🪜 A WORKFLOW, not a plugin (JL 260808): it opens along the bottom and its
      // whole content is where THIS page stands, which is why it is type-gated and
      // GUI Chat is not. Page's four phases join this menu, not the other one.
      menu: 'workflow',
      applies: function (page, type) { return type === 'labeling'; },
      open: function () { open(); }
    });
  }

  window.boardWorkflowOpen = open;   // kept for direct calls and for the tests
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
    fetch(location.href, { method: 'HEAD', cache: 'no-store' })
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
        return fetch(location.href, { cache: 'no-store' })
          .then(function (r) { return r.text(); })
          .then(function (t) {
            var doc = new DOMParser().parseFromString(t, 'text/html');
            /* SURGICAL UPDATES (JL 260801: "只更新这个配置的一小部分",
               "我一旦改了之后，我想看到这个变化是 immediate 的变化").

               A full reload is the only thing that can destroy a running
               terminal, so it is now the last resort rather than the first
               move, and the two assets are handled apart:

                 CSS changed  → swap the <link>. Instant, and nothing in the
                                page even notices; no reload, ever.
                 JS  changed  → cannot be hot-swapped safely, so reload, but
                                NEVER while a terminal or a turn is live. The
                                badge then says so and reloads the moment that
                                work ends, or immediately if you click it.

               The old code used one stamp for both, so a CSS tweak reloaded the
               page and took the terminal with it, and a 90-second hard cap
               reloaded even with a terminal open. Both are gone. */
            var newCss = (doc.querySelector('meta[name="board-css"]') || {}).content;
            var myCss = (document.querySelector('meta[name="board-css"]') || {}).content;
            if (newCss && myCss && newCss !== myCss) {
              var link = document.querySelector('link[rel="stylesheet"][href*="board.css"]');
              if (link) {
                var href = link.getAttribute('href').split('?')[0] + '?v=' + newCss;
                var fresh = link.cloneNode();
                fresh.setAttribute('href', href);
                /* load the new sheet BEFORE dropping the old one, or the page
                   flashes unstyled for a frame */
                fresh.onload = function () { if (link.parentNode) link.remove(); };
                link.parentNode.insertBefore(fresh, link.nextSibling);
                var m = document.querySelector('meta[name="board-css"]');
                if (m) m.content = newCss;
              }
            }

            var newJs = (doc.querySelector('meta[name="board-js"]') || {}).content;
            var myJs = (document.querySelector('meta[name="board-js"]') || {}).content;
            if (newJs && myJs && newJs !== myJs) {
              /* RELOAD, even with a terminal open (JL 260801: "你能够把这个
                 reload 变成自动 reload 吗... 哪怕我打开 terminal TUI 的时候").

                 This was deferred for a while because a reload used to destroy
                 the terminal. It no longer does, and each part of that is now
                 held up by its own check:
                   · the PTY is PARKED, not killed, so the process survives
                   · the drawer comes back in TUI mode and reattaches to it
                   · the ring replay repaints at THIS browser's size, so the
                     screen is not shredded
                   · a half-typed prompt lives in the CLI process, not in the
                     page, so it is still there afterwards
                 The badge stays for the moment it takes, so the reload is
                 explained rather than mysterious. */
              var bar = document.getElementById('lrf-hold');
              if (!bar) {
                bar = document.createElement('div');
                bar.id = 'lrf-hold'; bar.className = 'lrf';
                document.body.appendChild(bar);
              }
              bar.textContent = '↻ new board code · reloading…';
              /* remember the caret so the reattached terminal gets it back */
              try {
                sessionStorage.setItem('board-refocus',
                  (window.__boardTermFocused && window.__boardTermFocused()) ? 'term' : '');
              } catch (e) {}
              location.reload();
              return;
            }

            var nw = doc.querySelector('div.wrap');
            var old = document.querySelector('div.wrap');
            if (!nw || !old) return;
            var y = window.scrollY;
            /* Remember the caret BEFORE anything moves it. The hash re-bind
               below focuses the fragment's element, and a reader mid-sentence
               in the terminal or the composer should not pay for a board
               update they did not ask for (JL 260801). */
            var hadTerm = !!(window.__boardTermFocused && window.__boardTermFocused());
            var hadEl = document.activeElement;
            var hadChat = !hadTerm && hadEl && hadEl.closest && hadEl.closest('#chat');
            var selStart = hadChat && 'selectionStart' in hadEl ? hadEl.selectionStart : null;
            // Carry the OPEN/CLOSED state of every drawer across the swap
            // (JL 260731: "even when a section is open, the change should be
            // smooth"). Without this, replacing div.wrap silently re-collapses
            // whatever the reader had opened, which reads as the page resetting
            // itself under them. Keyed by the drawer's own heading text, so it
            // survives a section moving up or down the page.
            /* THE KEY IS THE AUTHORED HEADING, NOT WHAT IS ON SCREEN
               (JL 260802, measured: a comment saved at scroll 1112 came back
               at 171 with every section shut, on a document that had shrunk
               from 2000px to 1091px).

               `board.js` DECORATES a summary after each render: the `C1`/`H1`
               address chip, the ⧉ copy, the 🤖 chat, the sentence badge. So
               the OLD summary reads "📚 Content C1 ⧉ 🤖" while the same
               summary in the freshly fetched html reads "📚 Content", and the
               two never matched. Nothing reported it, because the fallback
               only runs when the drawer COUNT changed, and the count changes
               exactly when a sentence gains its first record: the comment
               path, and nothing else. That is why the card path looked smooth
               and the comment path did not.

               So both sides are read with the decoration removed, the same way
               `sentenceText` reads a sentence for its anchor. */
            function sumKey(d) {
              var s = d.querySelector('summary');
              if (!s) return '';
              var c = s.cloneNode(true);
              c.querySelectorAll('.caddr,.haddr,.sbz,.sbadge,.cmk,.cv,'
                                 + '.schatbar,button,input,select').forEach(
                function (x) { x.remove(); });
              return c.textContent.replace(/\s+/g, ' ').trim();
            }
            var oldD = old.querySelectorAll('details');
            var openAt = [], openKey = {};
            oldD.forEach(function (d, i) {
              if (!d.open) return;
              openAt.push(i);
              var k = sumKey(d);
              if (k) openKey[k] = 1;
            });
            old.replaceWith(nw);
            var newD = nw.querySelectorAll('details');
            if (newD.length === oldD.length) {
              // Same shape, so position is the exact identity: editing a
              // sentence does not add or remove drawers.
              openAt.forEach(function (i) { newD[i].open = true; });
            } else {
              // The page gained or lost a drawer, so fall back to the heading,
              // which survives a section moving up or down the page.
              newD.forEach(function (d) {
                var k = sumKey(d);
                if (k && openKey[k]) d.open = true;
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
            /* ...and put it back, after every one of those has had its turn. */
            if (hadTerm && window.__boardTermFocus) {
              window.__boardTermFocus();
            } else if (hadChat && hadEl && document.contains(hadEl)) {
              try {
                hadEl.focus({ preventScroll: true });
                if (selStart !== null && 'setSelectionRange' in hadEl)
                  hadEl.setSelectionRange(selStart, selStart);
              } catch (e) {}
            }
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
  /* QD5 · IN A PANE, A FRAME REFRESHES ITSELF.
     The swap above exists to keep a drawer and a terminal alive inside the one
     document that held everything. A pane holds one of those things and nothing
     else, so the honest update is a real reload of this frame — the browser
     rebuilds the document correctly instead of us patching it, and no other pane
     can even observe it.

     It asks about ITSELF, which is the whole difference from the 4000 ms poll
     this replaces: that one ran in a document carrying the sidebar, the page and
     the chat, so its answer had to be surgery. Here a HEAD on our own URL is the
     complete question, so it can be asked often and answered by reloading.

     The chat pane never asks. It is the one frame whose whole value is that it
     is NOT interrupted, and a terminal mid-command is exactly what a reload
     would take. Everything the shell knows about refreshing is now this. */
  if (window.__boardPane) {
    /* A PANE SWAPS TOO (JL 260802: "怎么让这个东西变得比较丝滑… 我加了
       comments，一点提交，然后它就 refresh 一下").

       This used to reload, on the reasoning that a pane holds one thing and
       the browser rebuilds a document better than we can patch it. That is
       true of the DOCUMENT and false of the READER: a page pane holds the
       scroll position, every `details` the reader opened to get here, the
       text they have selected, and the composer they are typing into. A
       reload takes all four and hands back a page scrolled to the top with
       every section shut, which is what "not smooth" means.

       The swap above already keeps all of it, and it was written for exactly
       this. It also holds itself back mid-selection and mid-typing, and it
       still falls back to a real reload when the board's JS changed, which is
       the one case a patch cannot cover. So the pane gets the swap and keeps
       the reload only as that fallback. */
    window.__boardRefresh = function () { if (last === null) last = '0'; tick(); };
    if (window.__boardPane === 'chat') return;
    /* THE BASELINE IS THIS DOCUMENT, not the first answer we happen to get.
       Asking once and keeping that as "current" looks equivalent and is not:
       an edit that lands between this document loading and the first tick is
       then adopted as the baseline, and the frame sits on the old page forever
       while believing it is fresh. `document.lastModified` is the timestamp of
       the response this frame is ACTUALLY showing, so it cannot drift. */
    /* Compare the ETag, which the server sets from the file's mtime in
       NANOSECONDS. `Last-Modified` is whole seconds, so an edit landing in the
       same second as this document was served looks identical to it and the
       frame sits stale forever believing it is current — narrow, but this board
       is rebuilt in bursts and it was hit (260802). The timestamp stays as the
       fallback for anything that does not send a tag. */
    /* BACK OFF WHEN NOTHING IS HAPPENING. 800 ms was chosen while measuring on
       localhost, where a HEAD is free. It is not free across a tailnet: two
       panes asking every 800 ms is 2.5 requests a second forever, each costing
       a round trip, and they compete with a CLICK for the six connections a
       browser allows per origin. That is why navigating one page to the next
       felt slower in the split than in the board it replaced (JL 260802), while
       the same click measured 42 ms against 49 ms on the machine serving it.

       So the interval grows while the answer keeps being "nothing changed", and
       snaps back to fast the moment this tab is looked at again. Editing feels
       instant because editing means the tab is focused; an idle pane in a tab
       you are not using costs a request every five seconds instead of every
       800 ms. */
    var tag = window.__paneStamp || '';
    var mine = Date.parse(document.lastModified);
    /* the router swaps the content without a reload, so it hands us the stamp
       of what it just put on screen */
    window.__paneRebase = function (t) { if (t) { tag = t; wait = FAST; } };
    var FAST = 800, SLOW = 5000, wait = FAST, timer = null;
    function quick() { wait = FAST; if (timer) { clearTimeout(timer); arm(); } }
    window.addEventListener('focus', quick);
    window.addEventListener('pageshow', quick);
    document.addEventListener('visibilitychange', function () {
      if (!document.hidden) quick();
    });
    function arm() { timer = setTimeout(ask, wait); }
    /* The swap landed, so THIS frame is now showing that build: take its tag
       as the new baseline and go back to polling fast. */
    window.addEventListener('board:updated', function () {
      fetch(location.href, { method: 'HEAD', cache: 'no-store' })
        .then(function (h) { var t = h.headers.get('etag'); if (t) tag = t; })
        .catch(function () {});
      wait = FAST;
    });
    function ask() {
      if (document.hidden) { wait = SLOW; return arm(); }
      fetch(location.href, { method: 'HEAD', cache: 'no-store' })
        .then(function (h) {
          var t = h.headers.get('etag');
          /* The tag is NOT rebased here. `tick()` holds itself back while the
             reader is selecting or typing, so rebasing on the poll would tell
             this frame it is current while it still shows the old build, and
             the change would never arrive. It is rebased on `board:updated`
             below, which only fires once the swap actually landed. */
          if (tag && t) { if (t !== tag) { window.__boardRefresh(); return arm(); } }
          else {
            var lm = Date.parse(h.headers.get('last-modified') || '');
            if (lm && mine && lm !== mine) { window.__boardRefresh(); return arm(); }
          }
          /* nothing changed: ask a little less often, up to the ceiling */
          wait = Math.min(SLOW, Math.round(wait * 1.6));
          arm();
        })
        .catch(function () { wait = SLOW; arm(); });
    }
    arm();
    return;
  }
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

  /* ONE reading of "what this sentence says". `QC7`'s anchor is an EXACT match
     on this string against a source line, so anything the renderer added has to
     come back out. The ⚑ badge is the trap: it lives INSIDE the <p> (it became a
     zero-width span so it could never wrap), so a raw textContent posts
     "…below the read.⚑ 1", which is not in the markdown and never will be, and
     the server correctly answers "not found, nothing written" (JL 260801, with
     a screenshot of exactly that). Both writers on this page use this, and the
     address module reuses it rather than keeping a second copy. */
  function sentenceText(p) {
    var c = p.cloneNode(true);
    // 🪪 A SPAN CARD IS THE EXCEPTION TO THE RULE BELOW (JL 260802, QB5 D).
    // Every other button in a sentence is a paper-dialect chip, whose label
    // replaced a marker and is NOT the source text, so deleting it is what
    // makes the posted string match the file. A span card is the opposite: it
    // sits on words the author typed and its label IS those words. Deleting it
    // would post a sentence with a hole in it, and every later write on that
    // sentence would miss its anchor forever. So it is UNWRAPPED, not removed.
    c.querySelectorAll('button.chip.card.span').forEach(function (b) {
      b.parentNode.replaceChild(document.createTextNode(b.textContent), b);
    });
    // `.cmk` is the 💬 the comment layer inserts INSIDE the paragraph for every
    // pending comment it still holds in localStorage. It is added text, so a
    // sentence that once failed to write would post "…text 💬" and keep failing
    // forever, poisoned by the very comment that failed. `button` covers the
    // paper dialect's chips, whose LABEL is not the source text anyway
    // (`Smith 2024` for `\citep{smith2024}`), so both sides delete rather than
    // keep: the server strips the marker out of the source line to match.
    c.querySelectorAll('.cmk,.sbz,.sbadge,.cv,.schatbar,button,input,select,textarea')
      .forEach(function (x) { x.remove(); });
    return c.textContent.replace(/\s+/g, ' ').trim();
  }
  window.__boardSentenceText = sentenceText;
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
          sentence: sentenceText(sentP),
          lane: sel.value, text: text })
      }).then(function (r) { return r.json(); })
        .then(function (j) {
          if (!j.ok) { err.textContent = '⚠ ' + (j.err || 'failed'); return; }
          err.textContent = '✔ saved';
          // CLOSE FIRST, THEN ASK (JL 260802). The swap refuses to run while
          // any textarea inside `div.wrap` still holds text, which is the rule
          // that stops a board rebuild from eating what someone is typing.
          // This form is inside `div.wrap` and its input still holds what was
          // just saved, so asking before closing asks for something that can
          // only be refused, and the lane then waited for the poll instead.
          close();
          if (window.__boardRefresh) window.__boardRefresh();
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
    var before = sentenceText(sentP);
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
        // A RELOAD IS THE WRONG TOOL HERE (JL 260802: adding something and
        // having the whole page refresh is what "not smooth" means). It threw
        // away the scroll position, shut every section the reader had opened
        // to reach this sentence, and cost a full document parse, all to show
        // one changed line. The swap keeps the reader exactly where they were
        // and still falls back to a real reload when the board's JS changed.
        //
        // CLOSE FIRST. This editor's textarea lives inside `div.wrap` and
        // still holds the sentence that was just saved, and the swap refuses
        // to run while any textarea in there has text, which is the rule that
        // stops a rebuild from eating what someone is typing. The reload this
        // replaced never met that rule, so the guard had never been crossed
        // here before: the markdown gained its `> ✎` record and the page sat
        // unchanged until the reader refreshed by hand.
        close();
        if (window.__boardRefresh) window.__boardRefresh();
        else location.reload();
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
  // Defined in 00-apparatus.js, which runs first: one grammar, never two.
  var sentenceText = window.__boardSentenceText;
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
     can say out loud: `QB4 / State / Decision Now`. Every rendered `##`
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
  /* The chip SHOWS the short id and COPIES the full address (JL 260801: "the
     address here is too long ... maybe just C1 is ok, when I click C1, I can
     copy the link"). Two different jobs were being served by one string: the
     reader needs a token they can see at a glance and say out loud, and Claude
     Code needs `QB4 / Content / 0 · The page protocol · <file>` to open the
     right place. So the label shrinks and the clipboard payload does not.
     A Content division already carries `C1` from the sentence grammar, so it
     reuses that id rather than inventing a second one; everywhere else the
     page id drops off the front, since the tab and the breadcrumb both
     already say which page this is. */
  function headingRail(head, sec, path, short, file, blockEl, withCopy) {
    if (head.querySelector(':scope > .hpath')) return;
    var rail = document.createElement('span');
    rail.className = 'hpath';
    var chip = document.createElement('button');
    chip.type = 'button';
    chip.className = 'hpid';
    chip.textContent = short || path;
    chip.title = 'Copy this address' + (file ? '\n' + path + '\n' + file : '');
    chip.addEventListener('click', function (e) {
      e.preventDefault(); e.stopPropagation();
      copyInto(chip, path + (file ? ' · ' + file : ''), '✓ copied');
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
  function shortLabel(label) {
    /* The chip is a HANDLE, not a caption (JL 260802: "we don't want this long
       copy button, please make them the same to the Content"). A Content part
       shows `C1`; every other group heading now shows only what comes before
       its first ` · `, so `⚙️ Engines · what RUNS this subject` becomes
       `Engines` instead of repeating the whole heading the reader is looking
       at. The clipboard still carries the full address. */
    var id = label.match(/^((?:A\d+|C\d+|P\d*))\s*·/);
    if (id) return id[1];
    var head = label.split(' · ')[0].trim();
    return head.replace(/^[^\p{L}\p{N}]+/u, '').trim() || label;
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
        headingRail(ch, sec, sec.id + ' / ' + name, shortLabel(name), file,
                    function () { return box; }, false);
      });
      function subPath(el) {
        var head = ownHead(el.closest(SECT + ', .folds'));
        var parent = head ? plainLabel(head) : '';
        return [sec.id, parent, plainLabel(el)].filter(Boolean).join(' / ');
      }
      sec.querySelectorAll('.sh').forEach(function (sh) {
        if (!plainLabel(sh)) return;
        headingRail(sh, sec, subPath(sh), shortLabel(plainLabel(sh)), file,
                    function () { return shRun(sh); }, true);
      });
      sec.querySelectorAll('details.csec > summary').forEach(function (sm) {
        if (!plainLabel(sm)) return;
        // `C1` comes from 10-address.js, which runs first; the visible `.caddr`
        // chip beside it is the same id, so this rail shows no second copy of
        // it and contributes only the ⧉ and 🤖 buttons.
        var cid = (sm.parentElement && sm.parentElement.dataset)
          ? sm.parentElement.dataset.contentId : '';
        // Aims and States groups fold like Content divisions since 260802, so
        // they arrive here too. They have no `C1` from the sentence grammar,
        // and the fallback printed the WHOLE title beside a heading already
        // showing it (JL 260802: "they are nested together"). Their own id is
        // the first token of the heading, `A0` or `P`, so use that.
        if (!cid) cid = shortLabel(plainLabel(sm));
        headingRail(sm, sec, subPath(sm), cid || plainLabel(sm), file,
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

/* A hidden ⧉ on every Decision Now row (JL 260802: "could you give a hidden
   copy button so I can copy the decision easier?").

   A decision row is the one block on a page a person routinely moves OUT of the
   board: into a chat, a message, a commit. Copying it by hand means dragging
   across six wrapped lines and picking up the checkbox glyph with them.

   Hidden the same way the heading rail is: absent until the row is hovered or
   something inside it takes focus, so a page at rest still reads as a document.
   Keyboard users get it from focus, which is why this is not a :hover-only rule.

   The clipboard gets the row as PLAIN TEXT with the ☐/☑ box dropped, because the
   box is the page's state and means nothing once the text is somewhere else. */
(function () {
  'use strict';

  function rowText(row) {
    /* textContent, NOT innerText. innerText reads LAID-OUT text, and a decision
       row lives inside `details.it` nested in `details.sect`, both shut on load.
       Nothing is rendered, so innerText returns '' and the button cheerfully
       copies an empty string while still flashing \u2713. Caught by clicking it
       (JL 260731: "did you clicked it yourself?"), never by reading the markup.

       textContent ignores layout but also drops every line break, so block
       boundaries are re-inserted on a DETACHED clone first. */
    var body = row.querySelector('.itw') || row;
    var clone = body.cloneNode(true);
    var blocks = clone.querySelectorAll('div,p,br,summary,li,tr');
    Array.prototype.forEach.call(blocks, function (el) {
      if (el.parentNode) { el.parentNode.insertBefore(document.createTextNode('\n'), el); }
    });
    return (clone.textContent || '')
      .replace(/\u00a0/g, ' ')
      .split('\n')
      .map(function (l) { return l.replace(/\s+/g, ' ').trim(); })
      .filter(function (l, i, a) { return l || (i > 0 && a[i - 1]); })
      .join('\n')
      .trim();
  }

  function copy(btn, text) {
    var done = function () {
      var was = btn.textContent;
      btn.textContent = '✓';
      setTimeout(function () { btn.textContent = was; }, 1200);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, function () { fallback(text, done); });
    } else {
      fallback(text, done);
    }
  }

  function fallback(text, done) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.setAttribute('readonly', '');
    ta.style.cssText = 'position:fixed;top:-1000px;left:-1000px';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); done(); } catch (e) {}
    document.body.removeChild(ta);
  }

  function isDecisionRow(row) {
    /* Only rows under `Decision Now`. Every other `- [ ]` on a board is a legacy
       checklist item, and putting the affordance on those would decorate
       hundreds of rows nobody moves anywhere.

       The heading is NOT a sibling: a `###` inside States renders as
       `details.csec > summary` with the rows in a following `div.cbody`, so this
       climbs to the owning `details` and reads its own summary. A first version
       walked previousElementSibling for a `.sh` and matched nothing, which is
       invisible in the markup and obvious the moment you open the page. */
    var host = row.closest ? row.closest('details.csec') : null;
    var head = host && host.querySelector(':scope > summary');
    if (head) { return /decision now/i.test(head.textContent || ''); }
    /* Fallback for a flat render, where `###` becomes a plain `div.sh`. */
    var n = row.previousElementSibling;
    while (n) {
      if (n.classList && n.classList.contains('sh')) {
        return /decision now/i.test(n.textContent || '');
      }
      n = n.previousElementSibling;
    }
    return false;
  }

  function wire(root) {
    var rows = (root || document).querySelectorAll('.ck');
    Array.prototype.forEach.call(rows, function (row) {
      if (row.__dcopy || !isDecisionRow(row)) { return; }
      row.__dcopy = true;
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'dcopy';
      b.textContent = '⧉';
      b.title = 'Copy this decision as plain text';
      b.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        copy(b, rowText(row));
      });
      row.appendChild(b);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { wire(); });
  } else {
    wire();
  }
  /* The live layer re-renders sections in place, so re-wire after a refresh. */
  window.__boardWireDecisionCopy = wire;
})();

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
  /* On narrow screens the sidebar overlays the text: a jump closes it (not
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
    /* WHERE AM I, asked of the DOCUMENT rather than of the URL.

       The sidebar was written for the one-file board, where every page is a
       section and `location.hash` names the open one. In the tree a page is
       its own file with no hash at all and the row hrefs are file paths, so
       the comparison matched nothing: no row was highlighted and no section
       outline ever opened (JL 260801). That is the same assumption QC9 took
       out of the drawer; the sidebar kept it.

       Three kinds of file, answered in order, because a wrong order lets the
       Index row win on a group page:
         a page   -> the one `section.q` in the document, matched by data-page
         a group  -> the row whose href IS this file
         neither  -> the Index row

       `data-page` exists so the match survives BOTH packagings: the id is the
       same, the href is not. The drawer's docPage() is reused, never copied. */
    var doc = window.__boardDocPage && window.__boardDocPage();
    var here = location.pathname.split('/').pop();
    var on = null, want = null;

    if (doc) {
      want = '#' + doc.id;
    } else if (document.querySelector('section.q')) {
      want = location.hash || '#top';            // the one-file board
    }
    if (want) {
      sb.querySelectorAll('a.sb-top,a.sb-g,a.sb-p').forEach(function (a) {
        var id = a.getAttribute('data-page');
        var hit = id ? ('#' + id) === want : a.getAttribute('href') === want;
        a.classList.toggle('on', hit);
        if (hit) on = a;
      });
    }
    if (!on && here) {                           // a group file in the tree
      sb.querySelectorAll('a.sb-g').forEach(function (a) {
        var hit = (a.getAttribute('href') || '').split('/').pop() === here;
        a.classList.toggle('on', hit);
        if (hit) { on = a; want = null; }
      });
    }
    if (!on) {                                   // the Index
      var top = sb.querySelector('a.sb-top');
      if (top) { top.classList.add('on'); on = top; want = '#top'; }
    }
    /* Accordion (QB2a, JL 260731): only the open page's outline shows. */
    sb.querySelectorAll('.sb-out.open').forEach(function (o) {
      o.classList.remove('open');
    });
    var out = want && sb.querySelector('.sb-out[data-out="' + want.slice(1) + '"]');
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
  /* Wait for the page element to EXIST rather than guessing how long a
     navigation takes. In the tree the row's click is intercepted by the router,
     which fetches the file and swaps div.wrap; 80ms was a race it usually lost,
     and losing it silently did nothing at all. */
  function afterPage(pid, fn, tries) {
    var page = document.getElementById(pid);
    if (page) { fn(page); return; }
    if ((tries || 0) > 40) return;                 // ~2.5s, then give up quietly
    setTimeout(function () { afterPage(pid, fn, (tries || 0) + 1); }, 60);
  }
  /* A click on an outline row is a REQUEST that outlives the click: it names a
     page that may still have to load. Two things can happen, and the row must
     work under both. The router usually intercepts and swaps div.wrap. But if
     scripts are stripped, if the fetch fails, or if the page is opened in a new
     tab, the browser does an ordinary navigation and this document is gone. So
     the request is PARKED in sessionStorage and applied by whoever ends up
     holding the page: this document after a swap, or the fresh one after a
     load. It is cleared the moment it is honoured, so it can never fire twice.
     (JL 260801: "clicking a content division does not take me there".) */
  var PARK = 'bnav:goto';
  function park(a) {
    var out = a.closest('.sb-out');
    try {
      sessionStorage.setItem(PARK, JSON.stringify({
        /* the id, read off the outline the row lives in: the href is `#QB5c`
           in the one-file board and `QB/QB5c-editing.html` in the tree, and
           slicing one character off the second gave an id nothing has. */
        pid: out ? out.getAttribute('data-out') : (a.getAttribute('href') || '').slice(1),
        k: a.dataset.k || '',
        div: a.dataset.div === undefined ? null : a.dataset.div,
        t: a.dataset.t || ''
      }));
    } catch (e) { /* private mode: the row still navigates, it just lands at the top */ }
  }
  function honour() {
    var req;
    try { req = JSON.parse(sessionStorage.getItem(PARK) || 'null'); } catch (e) { req = null; }
    if (!req || !req.pid) return;
    var page = document.getElementById(req.pid);
    if (!page) return;                       // not here yet; a later call will
    try { sessionStorage.removeItem(PARK); } catch (e) {}
    reveal(req, page);
  }
  sb.addEventListener('click', function (e) {
    var a = e.target.closest('a.sb-s,a.sb-ss');
    if (!a) return;
    park(a);
    /* Do NOT honour it here when the router will handle the click. Honouring
       eagerly opened the division on the DOM that was about to be REPLACED and
       consumed the request on the way, so the fresh wrap arrived with nothing
       left to apply: the row worked from another page and did nothing from its
       own (JL 260801, found by clicking §6 and watching §3 open instead).
       In the one-file board no fetch happens, so 90ms is the whole story. */
    var routed = document.body.classList.contains('split') &&
                 /\.html(\?|#|$)/.test(a.getAttribute('href') || '');
    if (!routed) setTimeout(honour, 90);
  });
  function reveal(req, page) {
    {
      var el = SEL[req.k] ? page.querySelector(SEL[req.k]) : null;
      if (el && req.div !== null && req.div !== undefined) {
        var divs = Array.prototype.filter.call(el.children, function (x) {
          return x.matches && x.matches('details.csec') &&
                 x.className.indexOf('display') < 0;
        });
        var d = divs[+req.div];
        if (d) { el.open = true; d.open = true; el = d; }
      } else if (el && req.t) {
        /* a non-Content subsection (### Decision Now …) is found by its
           rendered .sh heading text */
        var m = req.t.trim().toLowerCase();
        var hs = el.querySelectorAll('.sh');
        for (var i = 0; i < hs.length; i++) {
          if (hs[i].textContent.trim().toLowerCase().indexOf(m) === 0) {
            el.open = true;
            el = hs[i];
            break;
          }
        }
      }
      var to = el || page;
      if (el && el.tagName === 'DETAILS') el.open = true;
      /* Scroll TWICE, deliberately. The arrival path that swaps the wrap calls
         `window.scrollTo(0, 0)` on its way in, and the path that reloads gets
         the browser's own scroll restoration; either can land after this one
         and put the reader back at the top of a page they asked to enter part
         way down. The second call is cheap and it is what makes the row feel
         like it went somewhere (JL 260801). */
      to.scrollIntoView({ block: 'start' });
      setTimeout(function () { to.scrollIntoView({ block: 'start' }); }, 140);
    }
  }
  window.addEventListener('hashchange', mark);
  // A tree navigation replaces div.wrap and fires no hashchange.
  window.addEventListener('board:updated', function () { mark(); honour(); });
  mark();
  honour();                       // a real page load, arriving with a parked request
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
  /* QD5, corrected 260802. The first cut turned the router OFF in every pane,
     reasoning that a frame is the unit that reloads. That made every click a
     full DOCUMENT boot: fetch the page, parse 400 KB of html, and execute this
     whole bundle again, where the one-document board had swapped one column and
     kept everything else alive. JL felt it immediately ("really slow to click
     and go to a new page"), and he was right: 42 ms against 49 ms on the machine
     serving it, and far worse across a tailnet.

     So the PAGE pane keeps the router and a click is a swap again. The index and
     chat panes still return here: nothing in them should swap anything. */
  if (window.__boardPane && window.__boardPane !== 'page') return;
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
      /* `no-store` re-downloaded the whole page on every visit, and 82% of a
         page's bytes are the sidebar, which this swap then throws away because the
         sidebar lives outside div.wrap. `no-cache` still REVALIDATES every time, so
         a rebuilt page is never served stale, but an unchanged one comes back as
         a 0-byte 304 instead of 136 KB (JL 260801: "why does it take a long time
         to navigate"). Correctness is unchanged; only the wire is. */
      /* A HUNG FETCH MUST NOT WEDGE THE ROUTER. `busy` guards against two
         clicks racing, and its only release is this function finishing, so a
         request that never settles left every later click queued forever and
         the sidebar simply stopped working (measured 260802, after the swap was
         put back in the page pane). Five seconds, then fall back to an ordinary
         navigation, which is slower but always arrives. */
      var ctl = new AbortController();
      var bell = setTimeout(function () { ctl.abort(); }, 5000);
      var r;
      /* The sidebar is repeated in every generated page. Navigation only replaces
         `.wrap`, so ask the live server for that fragment directly. A static
         server that ignores the query still returns the full page as fallback. */
      var fragmentUrl = new URL(url, location.href);
      fragmentUrl.searchParams.set('fragment', 'wrap');
      try { r = await fetch(fragmentUrl.href, { cache: 'no-cache', signal: ctl.signal }); }
      finally { clearTimeout(bell); }
      var doc = new DOMParser().parseFromString(await r.text(), 'text/html');
      var nw = doc.querySelector('div.wrap'), old = document.querySelector('div.wrap');
      if (!nw || !old) { location.href = url; return; }
      old.replaceWith(nw);
      document.title = doc.title || document.title;
      if (push) history.pushState({ board: 1 }, '', url);
      /* A SWAP LEAVES THE DOCUMENT'S OWN STAMP BEHIND. The pane's refresh poll
         compares this document's `__paneStamp` against the server's ETag, and
         after a swap that stamp still describes the page we just LEFT, so the
         next tick would see a difference and reload the frame we were trying
         not to reload. Rebase it from the response we just read. */
      try {
        var et = r.headers.get('etag');
        if (et && window.__paneRebase) window.__paneRebase(et);
      } catch (e) {}
      /* and tell the shell, so the address bar and the strip follow a swap the
         same way they follow a real navigation */
      try { if (parent !== window && parent.__boardMirror) parent.__boardMirror(); } catch (e) {}
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
  /* the index pane calls this instead of navigating this frame (QD5, 260802) */
  window.__boardGo = go;
})();

/* Sidebar drag-to-resize (JL 260731: "can the left panel be dragged, it feels
   fixed"). Same shape the chat drawer uses for --chatw: one CSS variable, a
   handle on the edge that sets it, and the width remembered per machine.
   Pure enhancement, so with scripts off the sidebar keeps its default width. */
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
            try {
              Promise.resolve(window.__boardTermReopen()).then(function () {
                /* and give the caret back, so an automatic reload costs you a
                   moment rather than a click (JL 260801) */
                var want = '';
                try { want = sessionStorage.getItem('board-refocus') || ''; } catch (e) {}
                if (want === 'term' && window.__boardTermFocus) {
                  setTimeout(window.__boardTermFocus, 400);
                  setTimeout(window.__boardTermFocus, 1500);
                }
              });
            } catch (e) {}
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
