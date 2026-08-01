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
