/* Native details remain usable without script, including static exports. */
document.addEventListener('click', event => {
  const button = event.target.closest('.secall');
  if (!button) return;
  event.preventDefault();
  event.stopPropagation();
  const section = button.closest('details');
  if (!section) return;
  const nested = [...section.querySelectorAll('details')];
  const open = nested.some(item => !item.open);
  section.open = true;
  nested.forEach(item => { item.open = open; });
  const label = button.querySelector('.lbl');
  if (label) label.textContent = open ? 'collapse all' : 'expand all';
});
/* Reader mode: one folded Sources list per subsection, built from the sentences' evidence lanes,
   and the Evidence toggle. Without script the page still reads (lanes stay one click away). */
(() => {
  const ready = fn => document.readyState === 'loading' ? document.addEventListener('DOMContentLoaded', fn) : fn();
  ready(() => {
    const body = document.body;
    document.querySelectorAll('.cbody').forEach(section => {
      let lanes = [], anchor = null;
      const flush = before => {
        const seen = new Map();
        lanes.forEach(l => { const k = l.textContent.trim(); if (k && !seen.has(k)) seen.set(k, l); });
        lanes = [];
        if (!seen.size) return;
        const box = document.createElement('details');
        box.className = 'psrc';
        box.innerHTML = '<summary>Sources · ' + seen.size + '</summary>';
        seen.forEach(l => box.appendChild(l.cloneNode(true)));
        section.insertBefore(box, before);
      };
      let para = null;
      [...section.children].forEach(child => {
        if (!child.matches('details.sent')) { para = null; if (child.classList.contains('ph')) flush(child); return; }
        lanes.push(...child.querySelectorAll('.sapp .lane'));
        const sentence = child.querySelector(':scope>summary p');
        if (!sentence) return;
        if (!para || sentence.classList.contains('pnew')) {
          para = document.createElement('p');
          para.className = 'rpara';
          section.insertBefore(para, child);
        }
        const copy = sentence.cloneNode(true);
        copy.querySelectorAll('.sbz').forEach(b => b.remove());
        para.append(...copy.childNodes, ' ');
      });
      flush(null);
    });
    document.addEventListener('click', event => {
      const summary = event.target.closest('details.sent>summary');
      if (summary && body.classList.contains('reader') && !event.target.closest('a')) event.preventDefault();
    });
    const nav = document.querySelector('.page-toolbar nav');
    if (!nav || document.getElementById('page-reader-toggle')) return;
    const button = document.createElement('button');
    button.id = 'page-reader-toggle';
    button.type = 'button';
    button.textContent = '🔍 Evidence';
    button.title = 'Show every sentence with its evidence lanes';
    const set = evidence => {
      body.classList.toggle('reader', !evidence);
      button.setAttribute('aria-pressed', String(evidence));
      try { localStorage.setItem('page-evidence', evidence ? '1' : ''); } catch (e) { /* storage off */ }
    };
    let start = false;
    try { start = localStorage.getItem('page-evidence') === '1'; } catch (e) { /* storage off */ }
    set(start);
    button.addEventListener('click', () => set(body.classList.contains('reader')));
    nav.insertBefore(button, nav.firstChild);
  });
})();
