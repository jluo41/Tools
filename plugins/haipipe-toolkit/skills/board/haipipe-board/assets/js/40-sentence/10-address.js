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
