(function () {
  'use strict';
  var app = document.getElementById('task-workbench');
  if (!app) return;
  var config = JSON.parse(document.getElementById('tw-config').textContent);
  var search = document.getElementById('tw-search'), auto = document.getElementById('tw-auto');
  var panels = Array.from(app.querySelectorAll('[data-panel]'));
  var params = new URL(location.href).searchParams;
  var views = ['task', 'studio', 'related-paper', 'progress'];
  var view = params.get('view') || params.get('space') || 'task';
  view = ({runs:'task', scope:'progress'})[view] || view;
  if (!views.includes(view)) view = 'task';
  var storageKey = 'task-workbench:' + config.path;
  var editing = null, formChanged = false;
  var runDialog = document.getElementById('tw-run-dialog');
  var runFrame = document.getElementById('tw-run-frame');
  app.querySelectorAll('[data-run-result]').forEach(function (a) {
    a.addEventListener('click', function (event) {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      document.getElementById('tw-run-title').textContent = a.dataset.runResult;
      document.getElementById('tw-run-new').href = a.href;
      runFrame.src = a.href;
      runDialog.showModal();
    });
  });
  document.getElementById('tw-run-close').addEventListener('click', function () { runDialog.close(); });
  runDialog.addEventListener('click', function (event) { if (event.target === runDialog) runDialog.close(); });
  runDialog.addEventListener('close', function () { runFrame.removeAttribute('src'); });
  search.value = params.get('q') || '';
  auto.checked = params.get('auto') === '1';
  function status(message) { document.getElementById('tw-status').textContent = message; }
  function saveURL() {
    var url = new URL(location.href);
    url.searchParams.set('view', view); url.searchParams.delete('space');
    [['q', search.value], ['auto', auto.checked ? '1' : '']].forEach(function (pair) {
      if (pair[1]) url.searchParams.set(pair[0], pair[1]); else url.searchParams.delete(pair[0]);
    });
    history.replaceState(null, '', url);
  }
  function filter() {
    var term = search.value.trim().toLowerCase(), visible = 0, total = 0;
    app.querySelectorAll('[data-search]').forEach(function (row) {
      row.hidden = !!term && !row.dataset.search.includes(term);
      if (row.closest('[data-panel]').dataset.panel === view) { total++; if (!row.hidden) visible++; }
    });
    document.getElementById('tw-no-match').hidden = !total || visible > 0 || view === 'studio';
    saveURL();
  }
  function select(next) {
    view = next;
    status('');
    panels.forEach(function (panel) { panel.hidden = panel.dataset.panel !== view; });
    app.querySelectorAll('[data-view]').forEach(function (tab) { tab.setAttribute('aria-current', String(tab.dataset.view === view)); });
    app.querySelector('.tw-toolbar').hidden = view === 'studio';
    filter();
  }
  app.querySelectorAll('[data-view]').forEach(function (tab) {
    tab.addEventListener('click', function (event) {
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault(); select(tab.dataset.view);
    });
  });
  app.querySelectorAll('[data-question]').forEach(function (a) {
    a.addEventListener('click', function (event) {
      event.preventDefault(); select('task'); search.value = ''; filter();
      var q = document.getElementById('question-' + a.dataset.question);
      if (q) { q.open = true; q.scrollIntoView({block:'start'}); }
    });
  });
  app.querySelectorAll('[data-copy]').forEach(function (button) {
    button.addEventListener('click', async function () {
      try { await navigator.clipboard.writeText(button.dataset.copy); status('Context copied.'); }
      catch (_) { var box = document.createElement('textarea'); box.value = button.dataset.copy; app.append(box); box.select(); status('Select and copy this context to your session.'); }
    });
  });
  function foldKey(row) { return row.dataset.board || row.id; }
  function remember() {
    try { var folds = {}; app.querySelectorAll('details').forEach(function (d) { if (foldKey(d)) folds[foldKey(d)] = d.open; }); sessionStorage.setItem(storageKey, JSON.stringify(folds)); }
    catch (_) { /* Folding still works when storage is unavailable. */ }
  }
  function loadDrawing(row) {
    if (!config.studioEnabled || !row.open) return;
    var frame = row.querySelector('iframe');
    if (!frame.getAttribute('src')) frame.src = frame.dataset.src;
  }
  function stopEditing() {
    if (!editing) return;
    var frame = editing.querySelector('iframe'); frame.src = frame.dataset.src;
    editing.querySelector('[data-edit-drawing]').textContent = 'Edit drawing'; editing = null;
  }
  function prepareDrawing(row) {
    row.addEventListener('toggle', function () { loadDrawing(row); remember(); });
    row.querySelector('[data-edit-drawing]').disabled = !config.studioEnabled;
    row.querySelector('[data-edit-drawing]').addEventListener('click', function () {
      if (editing === row) { stopEditing(); status('Drawing viewer opened. Refresh is available.'); return; }
      stopEditing(); editing = row; row.open = true;
      row.querySelector('iframe').src = row.querySelector('iframe').dataset.src + '&edit=1';
      row.querySelector('[data-edit-drawing]').textContent = 'Finish editing';
      status('The native Excalidraw editor saves this drawing. Automatic refresh is paused while editing.');
    });
    loadDrawing(row);
  }
  try {
    var folds = JSON.parse(sessionStorage.getItem(storageKey) || '{}');
    app.querySelectorAll('details').forEach(function (d) { if (Object.prototype.hasOwnProperty.call(folds, foldKey(d))) d.open = folds[foldKey(d)]; });
  } catch (_) { /* Use the document defaults. */ }
  app.querySelectorAll('details').forEach(function (d) { d.addEventListener('toggle', remember); });
  app.querySelectorAll('.tw-drawing').forEach(prepareDrawing);
  var drawingForm = document.getElementById('tw-add-drawing');
  drawingForm.querySelector('button').disabled = !config.studioEnabled;
  drawingForm.addEventListener('submit', async function (event) {
    event.preventDefault();
    if (!config.studioEnabled) return;
    var name = drawingForm.elements.name.value.trim();
    if (!/^[A-Za-z0-9][A-Za-z0-9_ -]{0,79}$/.test(name)) { drawingForm.querySelector('[role=status]').textContent = 'Use a name with letters, numbers, spaces, underscores or hyphens.'; return; }
    var path = config.studio + '/' + name + '.excalidraw';
    var existing = Array.from(app.querySelectorAll('.tw-drawing')).find(function (d) { return d.dataset.board === path; });
    if (existing) { existing.open = true; existing.scrollIntoView({block:'center'}); return; }
    var button = drawingForm.querySelector('button'); button.disabled = true;
    try {
      var response = await fetch('/' + path.split('/').map(encodeURIComponent).join('/'), {credentials:'same-origin'});
      var scene = await response.json();
      if (!response.ok || scene.type !== 'excalidraw') throw new Error(scene.err || 'Could not open this drawing.');
      var row = document.createElement('details'); row.className = 'tw-drawing'; row.dataset.board = path;
      var summary = document.createElement('summary'); summary.textContent = name; row.append(summary);
      var body = document.createElement('div'); body.className = 'tw-drawing-body';
      var bar = document.createElement('div'); bar.className = 'tw-links';
      var edit = document.createElement('button'); edit.type = 'button'; edit.dataset.editDrawing = ''; edit.textContent = 'Edit drawing'; bar.append(edit);
      var source = '/_excalidraw/?' + new URLSearchParams({board:path});
      var full = document.createElement('a'); full.href = source + '&edit=1'; full.target = '_blank'; full.rel = 'noopener'; full.textContent = 'Open full screen ↗'; bar.append(full);
      var frame = document.createElement('iframe'); frame.title = name; frame.referrerPolicy = 'no-referrer'; frame.dataset.src = source;
      body.append(bar, frame); row.append(body); document.getElementById('tw-drawings').append(row);
      var empty = document.getElementById('tw-no-drawings'); if (empty) empty.remove();
      prepareDrawing(row); row.open = true; edit.click(); remember(); drawingForm.reset();
    } catch (error) { drawingForm.querySelector('[role=status]').textContent = error.message; }
    finally { button.disabled = false; }
  });
  var resourceForm = document.getElementById('tw-add-resource');
  resourceForm.addEventListener('input', function () { formChanged = true; });
  resourceForm.addEventListener('submit', async function (event) {
    event.preventDefault(); var button = resourceForm.querySelector('button'); button.disabled = true;
    var fields = new FormData(resourceForm);
    var payload = {path:config.path, action:'add-resource', title:fields.get('title'), url:fields.get('url'), contribution:fields.get('contribution'), notes:fields.get('notes'), questions:String(fields.get('questions') || '').split(/[\s,]+/).filter(Boolean)};
    try {
      var response = await fetch('/_board/task-board', {method:'POST', headers:{'Content-Type':'application/json'}, credentials:'same-origin', body:JSON.stringify(payload)});
      var result = await response.json(); if (!response.ok || !result.ok) throw new Error(result.err || 'Could not save resource.');
      formChanged = false; resourceForm.reset(); resourceForm.querySelector('[role=status]').textContent = 'Saved. Refresh to read the updated resource list.';
      if (!editing) refresh();
    } catch (error) { resourceForm.querySelector('[role=status]').textContent = error.message; }
    finally { button.disabled = false; }
  });
  function refresh() {
    if (editing || formChanged || runDialog.open) { status('Finish editing or close the Run result before refreshing.'); return; }
    remember(); saveURL(); location.reload();
  }
  search.addEventListener('input', filter); auto.addEventListener('change', saveURL);
  document.getElementById('tw-refresh').addEventListener('click', refresh);
  document.getElementById('tw-task-space').addEventListener('click', function () { select(view); });
  select(view);
  setInterval(function () { if (auto.checked && !editing && !formChanged && !runDialog.open && !document.hidden && !['INPUT','TEXTAREA','SELECT','IFRAME'].includes(document.activeElement.tagName) && !String(window.getSelection())) refresh(); }, 30000);
})();
