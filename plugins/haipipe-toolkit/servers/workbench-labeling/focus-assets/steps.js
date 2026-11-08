/* A meaning or expression Task's steps (labeling_steps.py; b15 s58). Three things only:
   1. the form embedded in Preferences takes its own height, its own Copy hidden: the prompt below sends it;
   2. one send (s58-D15, Q5): that prompt's Copy carries the form's answers after your notes and the session line;
   3. your sign on a guideline (Approve mNN) posts to /_board/labeling/approve, then the page reloads. */
(() => {
  function fit(f) {
    try {
      const d = f.contentDocument;
      if (!d || !d.body) return;
      if (!d.getElementById('ls-embed')) {               // the page names the report and sends it: the form shows its cards only
        const s = d.createElement('style'); s.id = 'ls-embed';
        s.textContent = '.send,details.box,.label,.lead,h1{display:none!important}'
          + 'pre.sketch{white-space:pre-wrap;overflow-wrap:anywhere}';
        d.head.append(s);
      }
      const full = d.documentElement.scrollHeight + 4;   // on a wide screen the form scrolls inside a frame, so Copy
      const phone = window.matchMedia('(max-width:600px)').matches;   // prompt stays near it (review C3 r01)
      f.style.height = (phone ? full : Math.min(full, Math.round(window.innerHeight * 0.72))) + 'px';
    } catch (_) {}
  }
  document.querySelectorAll('iframe[data-ls-form]').forEach(f => {
    f.addEventListener('load', () => {
      fit(f);
      try { new ResizeObserver(() => fit(f)).observe(f.contentDocument.body); } catch (_) {}
      try { f.contentDocument.addEventListener('click', () => setTimeout(() => fit(f), 60)); } catch (_) {}
    });
  });

  document.addEventListener('click', ev => {         // capture: runs before the shared Copy prompt handler
    const b = ev.target.closest('.ls-send .pb-copy');
    if (!b) return;
    if (b.dataset.base === undefined) b.dataset.base = b.dataset.tail || '';
    let answers = '';
    try {                                               // the form is the view's 🙋 Interaction now (round 2), found by its URL
      const url = (b.closest('.ls-send') || {}).dataset?.form || '';
      const f = [...document.querySelectorAll('iframe')].find(x => url && (x.getAttribute('src') === url || x.dataset.src === url))
        || document.getElementById('ls-form');
      const out = f.contentDocument.getElementById('out');
      answers = out ? out.value.trim() : '';
    } catch (_) {}
    b.dataset.tail = b.dataset.base + '\n\n' + (answers || '(no answer picked in the form yet)');
  }, true);

  document.querySelectorAll('.ls-by').forEach(i => {
    try { if (!i.value) i.value = localStorage.getItem('sign:by') || ''; } catch (_) {}
  });
  document.addEventListener('click', async ev => {
    const b = ev.target.closest('[data-approve]');
    if (!b) return;
    const bar = b.closest('.ls-bar'), by = bar.querySelector('.ls-by'), msg = bar.querySelector('.ls-msg');
    const name = ((by && by.value) || '').trim().replace(/\s+/g, ' ') || 'a person';   // no name needed to sign
    b.disabled = true; msg.textContent = 'Signing…';
    try {
      const r = await fetch('/_board/labeling/approve', {method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({task: b.dataset.task, version: b.dataset.approve, by: name})});
      const j = await r.json();
      if (!r.ok || !j.ok) throw new Error(j.err || 'refused');
      try { localStorage.setItem('sign:by', name); } catch (_) {}
      msg.textContent = 'Signed.'; location.reload();
    } catch (e) {
      msg.textContent = 'Not signed: ' + e.message; b.disabled = false;
    }
  });
})();
