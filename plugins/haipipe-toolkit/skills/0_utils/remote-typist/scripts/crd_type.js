// Paste into the CRD tab with the browser's page-script tool (claude-in-chrome
// javascript_tool). Defines window.__crdType(keys, delayMs): it presses the
// on-screen keyboard's own buttons in order, so the keys still go through the
// CRD keyboard, one button per key. keys are base-key names from key_plan.py:
// letters, digits, punctuation, Shift, Backslash, Space, Enter, Backspace, Tab,
// Control. Read the keyboard while it is unshifted (no Shift latched).
//
// Measured 261025: 70 ms per key is clean (1,162 keys in 84 s); 25 ms scrambled
// lines because the remote fell behind. Start it without await and read
// window.__crdResult afterwards, so the tool call does not time out:
//
//   window.__keys = [...];  window.__crdResult = 'running';
//   window.__crdType(window.__keys, 70).then(r => { window.__crdResult = r; });

window.__crdType = async function (keys, delay) {
  const ks = [...document.querySelectorAll('[role=button]')].filter((e) => {
    const r = e.getBoundingClientRect();
    return r.width > 0 && r.top > innerHeight * 0.6;
  });
  const names = { Back: 'Backspace', Ente: 'Enter', Shif: 'Shift', Spac: 'Space', Cont: 'Control', Tab: 'Tab' };
  const map = {};
  for (const e of ks) {
    const t = (e.innerText || e.getAttribute('aria-label') || '').trim();
    const n = t.length === 1 ? t : names[t.slice(0, 4)] || names[t.slice(0, 3)];
    if (n && !(n in map)) map[n] = e;
  }
  map.Backslash = map['\\'];
  const missing = [...new Set(keys)].filter((k) => !map[k]);
  if (missing.length) return 'MISSING ' + missing.join(' ');
  const press = (el) => {
    const r = el.getBoundingClientRect();
    const o = { bubbles: true, cancelable: true, composed: true, clientX: r.x + r.width / 2, clientY: r.y + r.height / 2, button: 0, pointerId: 1, pointerType: 'mouse', isPrimary: true };
    el.dispatchEvent(new PointerEvent('pointerdown', o));
    el.dispatchEvent(new MouseEvent('mousedown', o));
    el.dispatchEvent(new PointerEvent('pointerup', o));
    el.dispatchEvent(new MouseEvent('mouseup', o));
    el.dispatchEvent(new MouseEvent('click', o));
  };
  const t0 = Date.now();
  for (const k of keys) {
    press(map[k]);
    await new Promise((r) => setTimeout(r, delay));
  }
  return 'typed ' + keys.length + ' keys in ' + (Date.now() - t0) + ' ms';
};
'crd_type ready';
