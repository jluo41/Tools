/* The standalone host for the same category-workbench shape used by Board Pages.
 * The server supplies applicable entries; this shell only opens, switches,
 * closes, and remembers their frames. Internal lanes never become rows. */
(function () {
  'use strict';
  if (document.body.dataset.live !== 'true') return;

  var node = document.getElementById('page-workbench-config');
  var button = document.getElementById('page-workbench-button');
  var menu = document.getElementById('page-workbench-menu');
  var pane = document.getElementById('page-workbench-pane');
  var tabs = document.getElementById('page-workbench-tabs');
  var frames = document.getElementById('page-workbench-frames');
  if (!node || !button || !menu || !pane || !tabs || !frames) return;

  var config;
  try { config = JSON.parse(node.textContent); } catch (error) { return; }
  var workbenches = (config.workbenches || []).slice().sort(function (a, b) {
    return (a.order || 1000) - (b.order || 1000);
  });
  if (!workbenches.length) { button.hidden = true; return; }
  var byId = {};
  workbenches.forEach(function (workbench) { byId[workbench.id] = workbench; });

  var key = 'haipipe-page-workbenches:' + (config.page || location.pathname);
  var state = { open: [], active: '', visible: true };
  var saved = false;
  try {
    var raw = localStorage.getItem(key);
    if (raw) { state = Object.assign(state, JSON.parse(raw)); saved = true; }
  } catch (error) {}
  state.open = (state.open || []).filter(function (id) { return !!byId[id]; });
  if (!state.open.length && !saved && byId[config.default]) {
    state.open = [config.default]; state.active = config.default;
  }
  if (!byId[state.active]) state.active = state.open[0] || '';

  function persist() {
    try { localStorage.setItem(key, JSON.stringify(state)); } catch (error) {}
  }
  function frameFor(workbench, directUrl) {
    var frame = frames.querySelector('[data-workbench-frame="' + workbench.id + '"]');
    if (!frame) {
      frame = document.createElement('iframe');
      frame.className = 'page-workbench-frame';
      frame.dataset.workbenchFrame = workbench.id;
      frame.title = workbench.label;
      frame.loading = 'eager';
      frame.src = directUrl || workbench.url;
      frames.appendChild(frame);
    } else if (directUrl && frame.getAttribute('src') !== directUrl) {
      frame.src = directUrl;
    }
    return frame;
  }
  function paint() {
    tabs.innerHTML = '';
    frames.querySelectorAll('[data-workbench-frame]').forEach(function (frame) {
      frame.hidden = true;
    });
    state.open.forEach(function (id) {
      var workbench = byId[id];
      var wrap = document.createElement('span');
      wrap.className = 'page-workbench-tab-wrap';
      var tab = document.createElement('button');
      tab.type = 'button'; tab.className = 'page-workbench-tab';
      tab.dataset.workbench = id; tab.setAttribute('role', 'tab');
      tab.setAttribute('aria-selected', String(id === state.active));
      tab.textContent = workbench.label;
      tab.onclick = function () { openWorkbench(id); };
      var close = document.createElement('button');
      close.type = 'button'; close.className = 'page-workbench-close';
      close.setAttribute('aria-label', 'Close ' + workbench.label);
      close.textContent = '×'; close.onclick = function (event) {
        event.stopPropagation(); closeWorkbench(id);
      };
      wrap.appendChild(tab); wrap.appendChild(close); tabs.appendChild(wrap);
      frameFor(workbench).hidden = id !== state.active;
    });
    pane.hidden = !state.visible || !state.open.length;
    document.body.classList.toggle('workbench-open', !pane.hidden);
    button.setAttribute('aria-pressed', String(!pane.hidden));
    persist();
  }
  function openWorkbench(id, directUrl) {
    if (!byId[id]) return;
    if (state.open.indexOf(id) < 0) state.open.push(id);
    state.active = id; state.visible = true;
    frameFor(byId[id], directUrl); paint(); closeMenu();
  }
  function closeWorkbench(id) {
    var at = state.open.indexOf(id);
    if (at < 0) return;
    state.open.splice(at, 1);
    if (state.active === id) state.active = state.open[Math.min(at, state.open.length - 1)] || '';
    if (!state.open.length) state.visible = false;
    paint();
  }
  function closeMenu() {
    menu.hidden = true; button.setAttribute('aria-expanded', 'false');
  }
  function openMenu() {
    menu.innerHTML = '';
    workbenches.forEach(function (workbench) {
      var row = document.createElement('button');
      row.type = 'button'; row.className = 'page-workbench-menu-row';
      row.setAttribute('role', 'menuitem');
      row.innerHTML = '<b>' + workbench.label + '</b><span>' + workbench.hint + '</span>';
      row.onclick = function () { openWorkbench(workbench.id); };
      menu.appendChild(row);
    });
    menu.hidden = false; button.setAttribute('aria-expanded', 'true');
  }

  button.onclick = function () { menu.hidden ? openMenu() : closeMenu(); };
  document.addEventListener('pointerdown', function (event) {
    if (!menu.hidden && !menu.contains(event.target) && event.target !== button) closeMenu();
  }, true);
  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Escape') return;
    if (!menu.hidden) { closeMenu(); return; }
    if (!pane.hidden) { state.visible = false; paint(); }
  });
  document.addEventListener('click', function (event) {
    var link = event.target.closest && event.target.closest('a[href^="/_board/outline"]');
    if (!link || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault(); openWorkbench('outline', link.href);
  });
  paint();
}());
