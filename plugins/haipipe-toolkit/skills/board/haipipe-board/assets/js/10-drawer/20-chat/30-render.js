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
  function replayRow(m) {
    if (!m) return;
    if (m.k === 'you' && m.ts) turnMark(m.ts);
    if (m.k !== 'tool') { bubble(m.k, m.t); return; }
    var d = document.createElement('details');
    d.className = 'tool done';
    d.innerHTML = '<summary><span class="tn"></span><span class="tb"></span>' +
                  '<span class="ts">done</span></summary>';
    d.querySelector('.tn').textContent = m.name || '?';
    d.querySelector('.tb').textContent = (m.t || '').replace((m.name || '') + '  ', '');
    chat.querySelector('.bd').appendChild(d);
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
