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
