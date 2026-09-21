  /* Automatic Content addresses + prompt copying.

     Only ## Content participates. C is a ### division. H is a terminal,
     addressable #### heading and never parents P/S in the address grammar.
     A source PARAGRAPH is a blank-line block; each source line inside it is
     one sentence. build.py stamps the first sentence of each block with
     class="pnew", so P counts blocks and S counts sentences within one
     (JL 260819: "the paragraph should not change every sentence"). A page
     built before the stamp has no .pnew anywhere; it falls back to the old
     one-P-per-sentence numbering instead of collapsing into a single P.

       QAb3.C1.H1       heading itself
       QAb3.C1.P2.S3    third sentence in the second paragraph of C1

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
    return window.__boardReadableText(box);
  }

  function directChild(parent, cls) {
    return Array.from(parent.children).find(function (x) {
      return x.classList && x.classList.contains(cls);
    }) || null;
  }
  function cleanLabel(el) {
    if (!el) return '';
    var c = el.cloneNode(true);
    c.querySelectorAll('.caddr,.haddr,.hpath,.schatbar,button').forEach(function (x) {
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
  function sentenceRail(p, sec, shortId, fullId, contentPath) {
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
    var copy = document.createElement('button');
    copy.type = 'button';
    copy.className = 'scopy';
    copy.textContent = '⧉';
    copy.title = 'Copy prompt for ' + fullId;
    copy.setAttribute('aria-label', copy.title);
    copy.addEventListener('click', function (e) {
      e.preventDefault(); e.stopPropagation();
      var context = [contentPath, apparatusText(p)].filter(Boolean).join('\n\n');
      window.__boardCopyPrompt(copy,
        window.__boardPromptText(sec, fullId, sentenceText(p), context));
    });
    bar.append(id, copy);
    p.insertAdjacentElement('afterend', bar);
  }
  function wireSentenceCopies() {
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
      sec.querySelectorAll('p.qlead').forEach(function (p, i) {
        sentenceRail(p, sec, 'Opening', sec.id + ' / Opening' + (i ? ' / ' + (i + 1) : ''), '');
      });
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
        var hasPnew = !!cbody.querySelector('p.pnew');
        var nextH = 0, nextP = 0, nextS = 0, headingPath = '';
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
          if (!hasPnew || p.classList.contains('pnew') || nextP === 0) {
            nextP += 1; nextS = 1;
          } else {
            nextS += 1;
          }
          var shortId = contentId + '.P' + nextP + '.S' + nextS;
          var fullId = sec.id + '.' + shortId;
          var contentPath = contentId + (contentTitle ? ' · ' + contentTitle : '') +
            (headingPath ? '\n' + headingPath : '');
          sentenceRail(p, sec, shortId, fullId, contentPath);
        });
      });
    });
  }
