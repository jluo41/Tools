(() => {
  document.querySelectorAll('[data-rail-menu]').forEach(menu => {
    const drawer = document.getElementById(menu.getAttribute('aria-controls'));
    if (!drawer) return;
    menu.addEventListener('click', () => {
      drawer.showModal();
      menu.setAttribute('aria-expanded', 'true');
      document.body.classList.add('section-drawer-open');
    });
    drawer.querySelector('[data-drawer-close]').addEventListener('click', () => drawer.close());
    drawer.addEventListener('click', e => {
      if (e.target === drawer) {
        const r = drawer.getBoundingClientRect();
        if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) drawer.close();
      }
    });
    drawer.addEventListener('close', () => {
      menu.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('section-drawer-open');
    });
    window.matchMedia('(max-width:600px)').addEventListener('change', e => {
      if (!e.matches && drawer.open) drawer.close();
    });
  });
  const rails = [...document.querySelectorAll('.focus-rail')];
  function closeRails() { rails.forEach(rail => rail.classList.remove('is-open')); }
  rails.forEach(rail => {
    let leaveTimer;
    rail.addEventListener('pointerenter', e => {
      clearTimeout(leaveTimer);
      if (e.pointerType !== 'touch') { closeRails(); rail.classList.add('is-open'); }
    });
    rail.addEventListener('pointerleave', e => {
      if (e.pointerType !== 'touch') leaveTimer = setTimeout(() => rail.classList.remove('is-open'), 240);
    });
    rail.addEventListener('focusin', e => {
      if (e.target.matches(':focus-visible')) { closeRails(); rail.classList.add('is-open'); }
    });
    rail.addEventListener('focusout', e => {
      if (!rail.contains(e.relatedTarget)) rail.classList.remove('is-open');
    });
    rail.addEventListener('click', e => {
      if (!rail.classList.contains('is-open')) {
        e.preventDefault(); closeRails(); rail.classList.add('is-open');
      }
    });
    rail.addEventListener('keydown', e => {
      if (e.key === 'Escape') { e.target.blur(); rail.classList.remove('is-open'); }
    });
  });
  document.addEventListener('pointerdown', e => { if (!e.target.closest('.focus-rail')) closeRails(); });
  const dialog = document.querySelector('#focus-viewer');
  let opener = null;
  document.addEventListener('click', e => {
    const link = e.target.closest('a[data-pop]');
    if (!link || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
    e.preventDefault(); opener = link; closeRails();
    dialog.querySelector('[data-viewer-title]').textContent = link.dataset.pop;
    dialog.querySelector('iframe').src = link.href;
    dialog.querySelector('[data-viewer-go]').href = link.href;   // the pop-out's way to switch to the page
    dialog.showModal();
  });
  dialog.querySelector('[data-close]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => { dialog.querySelector('iframe').removeAttribute('src'); opener?.focus(); });
  dialog.addEventListener('click', e => {
    if (e.target !== dialog) return;
    const r = dialog.getBoundingClientRect();
    if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) dialog.close();
  });
  const from = document.querySelector('[data-from]'), to = document.querySelector('[data-to]');
  if (from && to) {
    const events = [...document.querySelectorAll('[data-day]')], message = document.querySelector('[data-date-message]');
    if (events.length) { const days = events.map(e => e.dataset.day).sort(); from.value = days[0]; to.value = days.at(-1); }   // oldest to newest, whatever the order shown
    function filter() {
      const invalid = from.value && to.value && from.value > to.value;
      from.setAttribute('aria-invalid', String(Boolean(invalid))); to.setAttribute('aria-invalid', String(Boolean(invalid)));
      let shown = 0;
      events.forEach(row => { row.hidden = Boolean(invalid || (from.value && row.dataset.day < from.value) || (to.value && row.dataset.day > to.value)); if (!row.hidden) shown++; });
      message.textContent = invalid ? 'Choose an end date on or after the start date.' : shown ? '' : 'No recorded events in this date range.';
    }
    from.addEventListener('change', filter); to.addEventListener('change', filter);
  }
})();
/* the Report mind map (JL 261029): one line per item that slides left and right (wheel, trackpad, or drag), and each
   Block's items fold under a toggle; Collapse all / Expand all above it; a big map starts folded */
(function () {
  const map = document.querySelector('.focus-map');
  if (!map) return;
  const redraw = () => { if (window.pmDraw) window.pmDraw(); };
  const items = [...map.querySelectorAll('.pm-leaves > li')].filter(li => li.querySelector(':scope > .pm-sub'));
  const set = (li, open) => {
    const sub = li.querySelector(':scope > .pm-sub'), btn = li.querySelector(':scope > .pm-w > .pm-fold, :scope > .pm-fold');
    sub.hidden = !open; btn.textContent = (open ? '▾ ' : '▸ ') + sub.children.length; btn.setAttribute('aria-expanded', String(open));
    btn.title = (open ? 'Fold ' : 'Show ') + sub.children.length + ' items';
  };
  items.forEach(li => {
    const btn = document.createElement('button');
    btn.type = 'button'; btn.className = 'pm-fold';
    (li.querySelector(':scope > .pm-w') || li).append(btn);   // at the end of its line, clear of the curve (JL 261029)
    btn.addEventListener('click', e => { e.stopPropagation(); set(li, li.querySelector(':scope > .pm-sub').hidden); redraw(); });
  });
  const total = items.reduce((n, li) => n + li.querySelector(':scope > .pm-sub').children.length, 0);
  items.forEach(li => set(li, total <= 15));
  // fold-all and unfold-all sit inside the map's top-left corner, small, pinned while the map slides (JL 261029)
  const wrap = document.createElement('div');
  wrap.className = 'map-wrap';
  map.before(wrap); wrap.append(map);
  const bar = document.createElement('div');
  bar.className = 'map-bar';
  bar.innerHTML = '<button type="button" data-all="0" title="Fold every Block" aria-label="Fold every Block">⊟</button>'
                + '<button type="button" data-all="1" title="Unfold every Block" aria-label="Unfold every Block">⊞</button>';
  bar.addEventListener('click', e => { const b = e.target.closest('[data-all]'); if (!b) return; items.forEach(li => set(li, b.dataset.all === '1')); redraw(); });
  if (items.length) { wrap.append(bar); wrap.classList.add('has-bar'); }   // room above the map only for its bar (round 3: 40 px blank)
  let down = null;
  map.addEventListener('pointerdown', e => { if (e.button || e.target.closest('a,button,[contenteditable]')) return; down = {x: e.clientX, left: map.scrollLeft}; map.classList.add('panning'); });
  window.addEventListener('pointermove', e => { if (down) map.scrollLeft = down.left - (e.clientX - down.x); });
  window.addEventListener('pointerup', () => { down = null; map.classList.remove('panning'); });
  setTimeout(redraw, 0);
})();
/* 🙋 tray (JL 261114: "if there are things for me to make decision, could they just pop out?"): every orange mark on the
   page (a section bar's 🙋 N, a Draft Lab sentence's waiting cards) is gathered under one 🙋 beside the title. The tray is
   a native popover (Esc or a click outside closes it); Go opens that fold, scrolls to it and flashes it. No mark, no tray. */
(function () {
  const h1 = document.querySelector('.focus-page > h1');
  if (!h1 || !('popover' in HTMLElement.prototype)) return;
  const name = el => {
    const im = el.closest('.im-marks');                                   // an item card mark (ref/cards.md)
    const bar = im ? (im.closest('tr[data-addr], [data-addr]:not(.im-marks)') || im.parentElement)
                   : el.closest('.fd-h, summary, .sx-row, [data-s]');
    const t = bar ? bar.cloneNode(true) : null;
    if (t) t.querySelectorAll('.word, .mk, .sx-bar, .bar, button, .im-marks, .im-slot').forEach(x => x.remove());
    return ((t && t.textContent) || el.textContent || '').replace(/\s+/g, ' ').trim().slice(0, 90);
  };
  const marks = Array.from(document.querySelectorAll('.focus-content .word.you, .focus-content .sx-sum.wait, '
    + '.focus-content .im-marks:not(.im-roll) .im-mk.im-w'));
  const asked = document.getElementById('wait-items');                   // waiting questions at this page or below
  const rows = asked ? Array.from(asked.content.children) : [];
  // a bar's 🙋 N that only rolls up collection Runs (data-src="ix") is already listed as rows: never count it twice
  if (rows.length) for (let i = marks.length - 1; i >= 0; i--) if (marks[i].dataset.src === 'ix') marks.splice(i, 1);
  if (!marks.length && !rows.length) return;
  const weight = m => { const k = (m.textContent.match(/\d+/) || [1])[0]; return +k || 1; };   // 🙋 3 counts 3
  const n = rows.length + marks.reduce((t, m) => t + weight(m), 0);
  const btn = document.createElement('button');
  btn.type = 'button'; btn.className = 'tray-btn'; btn.textContent = '🙋 ' + n;
  btn.title = n + (n === 1 ? ' waits' : ' wait') + ' for you'; btn.setAttribute('popovertarget', 'wait-tray');
  const tray = document.createElement('div');
  tray.id = 'wait-tray'; tray.setAttribute('popover', ''); tray.className = 'wait-tray';
  tray.innerHTML = '<b>Waiting for you</b><ul></ul>';
  const ul = tray.querySelector('ul');
  marks.forEach(m => {
    const li = document.createElement('li');
    const what = document.createElement('span');
    what.textContent = name(m) || m.title || m.textContent;
    const go = document.createElement('button');
    go.type = 'button'; go.textContent = 'Go';
    go.addEventListener('click', () => {
      tray.hidePopover();
      for (let d = m.closest('details'); d; d = d.parentElement && d.parentElement.closest('details')) d.open = true;
      const h = m.closest('.fd-h');
      if (h && h.getAttribute('aria-expanded') === 'false') h.click();
      if (m.classList.contains('sx-sum') && !m.closest('.sx-open')) m.click();
      const slot = m.dataset.imOpen && document.querySelector('[data-im-slot="' + CSS.escape(m.dataset.imOpen) + '"]');
      if (slot && slot.hidden) m.click();
      const at = m.closest('tr[data-addr], .fd-sec, details, .sx-row, [data-s]') || m;
      at.scrollIntoView({block: 'center', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'});
      at.classList.remove('tray-flash'); void at.offsetWidth; at.classList.add('tray-flash');
    });
    li.append(what, go); ul.append(li);
  });
  rows.forEach(li => { const a = li.querySelector('a'); if (a) a.classList.add('tray-open'); ul.append(li); });
  h1.append(btn); document.body.append(tray);
  tray.addEventListener('toggle', e => {
    if (e.newState !== 'open') return;
    const r = btn.getBoundingClientRect(), w = tray.offsetWidth;
    tray.style.top = (r.bottom + 6) + 'px';
    tray.style.left = Math.max(12, Math.min(r.right - w, innerWidth - w - 12)) + 'px';
  });
})();
/* 📝 💬 on a section bar (JL 261114, mockup B: "for each section's card, we want to add the emojis" like a sentence's):
   a bar counts what lies inside its section, 📝 edit cards that wait on you (orange) and 💬 comments; a click opens the
   section and the first such sentence's cards, then scrolls to it and flashes it. Nothing inside, no mark. */
(function () {
  const bars = document.querySelectorAll('.focus-content section.fd-sec > h3.fd-h, .focus-content details.band-sec > summary');
  bars.forEach(h => {
    const box = h.closest('section.fd-sec, details.band-sec');
    if (!box) return;
    const inside = sel => Array.from(box.querySelectorAll(sel));
    const kinds = [
      ['📝', inside('.rv-card[data-state=proposed], .rv-card[data-state=open], .im-card.im-edit.im-e-proposed'), 'you', ' edit card', ' wait for you', '.sx-pen, .sx-sum'],
      ['💬', inside('.rv-note:not(.nt-new), article.im-card:not(.im-edit):not(.im-c-done)'), '', ' comment', '', '.sx-cmt'],
    ];
    const at = h.querySelector('.word') || null;
    kinds.forEach(([icon, list, cls, one, tail, opener]) => {
      if (!list.length) return;
      const n = list.length, b = document.createElement('span');
      b.className = 'word mk bar-mk' + (cls ? ' ' + cls : ''); b.setAttribute('role', 'button'); b.tabIndex = 0;
      b.textContent = icon + ' ' + n; b.title = n + one + (n === 1 ? '' : 's') + tail;
      const go = e => {
        e.preventDefault(); e.stopPropagation();
        if (box.tagName === 'DETAILS') box.open = true;
        else if (h.getAttribute('aria-expanded') === 'false') h.click();
        const slot = list[0].closest('[data-im-slot]');
        if (slot) slot.hidden = false;
        const row = list[0].closest('.sx-row') || (slot && (slot.previousElementSibling || slot)) || list[0];
        for (let d = row.closest('details'); d; d = d.parentElement && d.parentElement.closest('details')) d.open = true;
        const o = row.querySelector && row.querySelector(opener);
        if (o && !row.classList.contains('sx-open')) o.click();
        row.scrollIntoView({block: 'center', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'});
        row.classList.remove('tray-flash'); void row.offsetWidth; row.classList.add('tray-flash');
      };
      b.addEventListener('click', go);
      b.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') go(e); });
      h.insertBefore(b, at);
    });
  });
})();
