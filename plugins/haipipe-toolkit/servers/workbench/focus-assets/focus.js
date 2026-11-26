(() => {
  document.querySelectorAll('[data-rail-menu]').forEach(menu => {
    const drawer = document.getElementById(menu.getAttribute('aria-controls'));
    if (!drawer) return;
    const panel = drawer.querySelector('iframe[data-drawer-src]');
    panel?.addEventListener('load', () => {
      panel.contentDocument?.addEventListener('keydown', e => {
        if (e.key === 'Escape' && !e.defaultPrevented && !panel.contentDocument.querySelector('dialog[open]')) {
          e.preventDefault();
          drawer.close();
        }
      });
    });
    menu.addEventListener('click', () => {
      if (panel && !panel.hasAttribute('src')) panel.src = panel.dataset.drawerSrc;
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
    if (menu.classList.contains('rail-tab')) {
      window.matchMedia('(max-width:600px)').addEventListener('change', e => {
        if (!e.matches && drawer.open) drawer.close();
      });
    }
  });
  // The side pane: the right rail's sections behind the round button. A pick opens that section in the pane,
  // a right split on a wide screen (the page narrows beside it) and a drawer on a phone. The pane has no header:
  // the same button switches it and its menu's last row closes it (on a phone, a tap outside the drawer too).
  // The open section and the dragged width carry to the next page.
  (() => {
    const ball = document.querySelector('.files-ball[aria-controls="side-menu"]');
    const menu = document.getElementById('side-menu');
    const pane = document.getElementById('files-drawer');
    if (!ball || !menu || !pane) return;
    const frame = pane.querySelector('iframe'), shut = menu.querySelector('[data-side-close]');
    const narrow = window.matchMedia('(max-width:600px)');
    const store = (s, k, v) => { try { v === undefined ? s.removeItem(k) : s.setItem(k, v); } catch (e) {} };
    const recall = (s, k) => { try { return s.getItem(k); } catch (e) { return null; } };
    // the section word beside the title (Report ▾) is the sections menu; the ball is Files alone (JL 261125: "when I
    // click this, I can choose different things, like Studio, things to know"; "keep [the ball] to be just the file")
    const pick = document.querySelector('.h1-pick'), filesItem = menu.querySelector('[data-side-key="files"]');
    let from = ball;
    const hideMenu = () => { menu.hidden = true; ball.setAttribute('aria-expanded', 'false'); pick?.setAttribute('aria-expanded', 'false'); };
    const showMenu = (anchor = ball) => {      // under the word, or to the left of the ball, kept on screen
      from = anchor;
      shut.hidden = !pane.open;
      if (filesItem) filesItem.hidden = anchor === pick;
      menu.hidden = false;
      const r = anchor.getBoundingClientRect(), h = menu.offsetHeight;
      if (anchor === pick) {
        menu.style.right = 'auto';
        menu.style.left = Math.max(8, Math.min(r.left, innerWidth - menu.offsetWidth - 8)) + 'px';
        menu.style.top = Math.min(r.bottom + 6, innerHeight - h - 8) + 'px';
      } else {
        menu.style.left = 'auto';
        menu.style.right = (innerWidth - r.left + 8) + 'px';
        menu.style.top = Math.max(8, Math.min(r.top + r.height / 2 - h / 2, innerHeight - h - 8)) + 'px';
      }
      anchor.setAttribute('aria-expanded', 'true');
      (menu.querySelector('[data-side-key].on:not([hidden])') || menu.querySelector('[data-side-key]:not([hidden])'))?.focus();
    };
    const open = item => {
      menu.querySelectorAll('[data-side-key]').forEach(b => b.classList.toggle('on', b === item));
      if (frame.getAttribute('src') !== item.dataset.sideSrc) frame.src = item.dataset.sideSrc;
      if (!pane.open) {
        if (narrow.matches) { pane.showModal(); document.body.classList.add('section-drawer-open'); }
        else { pane.show(); document.body.classList.add('files-split'); }
      }
      store(sessionStorage, 'wb:side', item.dataset.sideKey);
    };
    ball.addEventListener('click', () => {
      if (!filesItem || !pick) return menu.hidden ? showMenu() : hideMenu();
      hideMenu();
      if (pane.open && filesItem.classList.contains('on')) pane.close(); else open(filesItem);
    });
    pick?.addEventListener('click', () => (menu.hidden || from !== pick ? showMenu(pick) : hideMenu()));
    menu.addEventListener('click', e => {
      if (e.target.closest('[data-side-close]')) { hideMenu(); pane.close(); return; }
      const it = e.target.closest('[data-side-key]'); if (!it) return;
      hideMenu();
      if (it === filesItem) return open(it);
      // a section opens in the main page; the side pane holds Files only (JL 261125: "Now I want in the right panel. we
      // will just show the files")
      const to = new URL(it.dataset.sideSrc, location.href); to.searchParams.delete('panel');
      location.href = to.pathname + to.search;
    });
    menu.addEventListener('keydown', e => {
      const all = [...menu.querySelectorAll('[role=menuitem]:not([hidden])')], i = all.indexOf(document.activeElement);
      if (e.key === 'Escape') { hideMenu(); from.focus(); }
      else if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); all[(i + (e.key === 'ArrowDown' ? 1 : all.length - 1)) % all.length]?.focus(); }
    });
    document.addEventListener('click', e => { if (!menu.hidden && !menu.contains(e.target) && !e.target.closest('.files-ball, .h1-pick')) hideMenu(); });
    document.addEventListener('keydown', e => {   // Esc closes the menu wherever focus is, and only the menu
      if (e.key === 'Escape' && !menu.hidden && !e.defaultPrevented) { e.preventDefault(); hideMenu(); from.focus(); }
    });
    pane.addEventListener('close', () => {
      hideMenu();
      document.body.classList.remove('files-split', 'section-drawer-open');
      store(sessionStorage, 'wb:side');
    });
    frame.addEventListener('load', () => {
      frame.contentDocument?.addEventListener('keydown', e => {
        if (e.key === 'Escape' && !e.defaultPrevented && !frame.contentDocument.querySelector('dialog[open]')) { e.preventDefault(); pane.close(); }
      });
    });
    // a right-click on an element folds the Files pane to its folder and the code it owns (element_info.py)
    addEventListener('wb:show-files', e => {
      if (!pane.open && filesItem) open(filesItem);
      const go = () => frame.contentWindow?.__scopeFocus?.(e.detail);
      if (frame.contentDocument?.readyState === 'complete' && frame.contentWindow?.__scopeFocus) go();
      else frame.addEventListener('load', go, { once: true });
    });
    narrow.addEventListener('change', e => { if (e.matches && document.body.classList.contains('files-split')) pane.close(); });
    pane.addEventListener('click', e => {       // the phone drawer is modal: a tap on its backdrop closes it
      if (e.target !== pane || !pane.matches(':modal')) return;
      const r = pane.getBoundingClientRect();
      if (e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom) pane.close();
    });
    const width = w => document.documentElement.style.setProperty('--files-w', w + 'px');
    const saved = +recall(localStorage, 'wb:files-w');
    if (saved) width(saved);
    const grip = pane.querySelector('.files-grip');
    grip?.addEventListener('pointerdown', e => {
      e.preventDefault();
      grip.setPointerCapture(e.pointerId);
      document.body.classList.add('files-dragging');
      let last = 0;
      const move = ev => { last = Math.round(Math.min(Math.max(innerWidth - ev.clientX, 260), innerWidth * 0.7)); width(last); };
      grip.addEventListener('pointermove', move);
      grip.addEventListener('pointerup', () => {
        grip.removeEventListener('pointermove', move);
        document.body.classList.remove('files-dragging');
        if (last) store(localStorage, 'wb:files-w', String(last));
      }, { once: true });
    });
    const asked = new URLSearchParams(location.search);
    if (asked.get('section') === 'files') {   // an old link to the Files page: the page, with Files beside it
      asked.delete('section'); asked.delete('group');
      history.replaceState(null, '', location.pathname + '?' + asked + location.hash);
      const files = menu.querySelector('[data-side-key="files"]');
      if (files) { open(files); return; }
    }
    if (filesItem && recall(sessionStorage, 'wb:side') === 'files' && !narrow.matches) open(filesItem);
  })();
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
  const pop = (href, title) => {
    dialog.querySelector('[data-viewer-title]').textContent = title;
    dialog.querySelector('iframe').src = href;
    dialog.querySelector('[data-viewer-go]').href = href;   // the pop-out's way to switch to the page
    dialog.showModal();
  };
  window.__wbPop = pop;
  // a page shown inside the side pane opens its files in the main page's viewer, full size, not in the pane
  const host = (() => { try { return window.parent !== window && window.parent.__wbPop ? window.parent : null; } catch (e) { return null; } })();
  document.addEventListener('click', e => {
    const link = e.target.closest('a[data-pop]');
    if (!link || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
    e.preventDefault(); closeRails();
    if (host && window.frameElement?.closest('#files-drawer')) { host.__wbPop(link.href, link.dataset.pop); return; }
    opener = link;
    pop(link.href, link.dataset.pop);
  });
  dialog.querySelector('[data-close]').addEventListener('click', () => dialog.close());
  // One header line: the file's own tools (Open, Download, Line wrap) move up beside its name, and the preview's
  // second row is hidden; Line wrap here drives the preview's own switch.
  const viewerFrame = dialog.querySelector('iframe'), title = dialog.querySelector('[data-viewer-title]');
  viewerFrame.addEventListener('load', () => {
    dialog.querySelector('.viewer-tools')?.remove();
    let doc; try { doc = viewerFrame.contentDocument; } catch (e) { return; }
    const tools = doc?.querySelector('.preview-tools');
    if (!tools) return;
    const bar = document.createElement('span');
    bar.className = 'viewer-tools';
    tools.querySelectorAll('a').forEach(a => {
      const b = document.createElement('a');
      b.href = a.href; b.textContent = a.textContent.trim();
      if (a.hasAttribute('download')) b.setAttribute('download', ''); else { b.target = '_blank'; b.rel = 'noopener'; }
      bar.append(b);
    });
    const wrap = doc.getElementById('wrap-lines');
    if (wrap) {
      const label = document.createElement('label'), box = document.createElement('input');
      box.type = 'checkbox'; box.checked = wrap.checked;
      box.addEventListener('change', () => { wrap.checked = box.checked; });
      label.append(box, ' Line wrap');
      bar.append(label);
    }
    tools.hidden = true;
    title.after(bar);
  });
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

// A UI preview's live view names the part it is about (haipipe-studio ref/ui-preview-topic.md): `mark=jobs-rows`
// (comma-separated: a class name, or `jsub=main` for [data-jsub="main"]) outlines the visible ones in red and
// scrolls the first into view.
(function () {
  const sel = (new URLSearchParams(location.search).get('mark') || '').split(',').map(s => s.trim()).map(s =>
    /^[\w-]+$/.test(s) ? '.' + s : (/^([\w-]+)=([\w-]+)$/.test(s) ? s.replace(/^([\w-]+)=([\w-]+)$/, '[data-$1="$2"]') : ''))
    .filter(Boolean);
  if (!sel.length) return;
  const css = document.createElement('style');
  css.textContent = '.preview-mark{outline:2px solid #e03131;outline-offset:4px;border-radius:6px}';
  document.head.appendChild(css);
  const draw = () => {
    document.querySelectorAll('.preview-mark').forEach(el => el.classList.remove('preview-mark'));
    const hits = sel.flatMap(q => [...document.querySelectorAll(q)]).filter(el => el.getClientRects().length);
    hits.forEach(el => el.classList.add('preview-mark'));
    return hits;
  };
  requestAnimationFrame(() => { const hits = draw(); if (hits[0]) hits[0].scrollIntoView({ block: 'center' }); });
  document.addEventListener('click', () => setTimeout(draw, 60));   // a picked Job or Task shows its own part
})();
