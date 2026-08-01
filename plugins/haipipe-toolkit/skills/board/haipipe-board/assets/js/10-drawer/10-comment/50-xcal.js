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
