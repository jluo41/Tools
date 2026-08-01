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
