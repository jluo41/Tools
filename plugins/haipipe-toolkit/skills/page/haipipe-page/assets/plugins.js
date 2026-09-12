/* The standalone host for the same category-plugin shape used by Board Pages.
 * The server supplies applicable entries; this shell only opens, switches,
 * closes, and remembers their frames. Internal lanes never become rows. */
(function () {
  'use strict';
  if (document.body.dataset.live !== 'true') return;

  var node = document.getElementById('page-plugin-config');
  var button = document.getElementById('page-plugin-button');
  var menu = document.getElementById('page-plugin-menu');
  var pane = document.getElementById('page-plugin-pane');
  var tabs = document.getElementById('page-plugin-tabs');
  var frames = document.getElementById('page-plugin-frames');
  if (!node || !button || !menu || !pane || !tabs || !frames) return;

  var config;
  try { config = JSON.parse(node.textContent); } catch (error) { return; }
  var plugins = (config.plugins || []).slice().sort(function (a, b) {
    return (a.order || 1000) - (b.order || 1000);
  });
  if (!plugins.length) { button.hidden = true; return; }
  var byId = {};
  plugins.forEach(function (plugin) { byId[plugin.id] = plugin; });

  var key = 'haipipe-page-plugins:' + (config.page || location.pathname);
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
  function frameFor(plugin, directUrl) {
    var frame = frames.querySelector('[data-plugin-frame="' + plugin.id + '"]');
    if (!frame) {
      frame = document.createElement('iframe');
      frame.className = 'page-plugin-frame';
      frame.dataset.pluginFrame = plugin.id;
      frame.title = plugin.label;
      frame.loading = 'eager';
      frame.src = directUrl || plugin.url;
      frames.appendChild(frame);
    } else if (directUrl && frame.getAttribute('src') !== directUrl) {
      frame.src = directUrl;
    }
    return frame;
  }
  function paint() {
    tabs.innerHTML = '';
    frames.querySelectorAll('[data-plugin-frame]').forEach(function (frame) {
      frame.hidden = true;
    });
    state.open.forEach(function (id) {
      var plugin = byId[id];
      var wrap = document.createElement('span');
      wrap.className = 'page-plugin-tab-wrap';
      var tab = document.createElement('button');
      tab.type = 'button'; tab.className = 'page-plugin-tab';
      tab.dataset.plugin = id; tab.setAttribute('role', 'tab');
      tab.setAttribute('aria-selected', String(id === state.active));
      tab.textContent = plugin.label;
      tab.onclick = function () { openPlugin(id); };
      var close = document.createElement('button');
      close.type = 'button'; close.className = 'page-plugin-close';
      close.setAttribute('aria-label', 'Close ' + plugin.label);
      close.textContent = '×'; close.onclick = function (event) {
        event.stopPropagation(); closePlugin(id);
      };
      wrap.appendChild(tab); wrap.appendChild(close); tabs.appendChild(wrap);
      frameFor(plugin).hidden = id !== state.active;
    });
    pane.hidden = !state.visible || !state.open.length;
    document.body.classList.toggle('plugin-open', !pane.hidden);
    button.setAttribute('aria-pressed', String(!pane.hidden));
    persist();
  }
  function openPlugin(id, directUrl) {
    if (!byId[id]) return;
    if (state.open.indexOf(id) < 0) state.open.push(id);
    state.active = id; state.visible = true;
    frameFor(byId[id], directUrl); paint(); closeMenu();
  }
  function closePlugin(id) {
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
    plugins.forEach(function (plugin) {
      var row = document.createElement('button');
      row.type = 'button'; row.className = 'page-plugin-menu-row';
      row.setAttribute('role', 'menuitem');
      row.innerHTML = '<b>' + plugin.label + '</b><span>' + plugin.hint + '</span>';
      row.onclick = function () { openPlugin(plugin.id); };
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
    event.preventDefault(); openPlugin('outline', link.href);
  });
  paint();
}());
