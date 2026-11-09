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
