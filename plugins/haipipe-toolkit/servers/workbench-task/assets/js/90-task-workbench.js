(function () {
  'use strict';
  var app = document.getElementById('task-workbench');
  if (!app) return;
  var config = JSON.parse(document.getElementById('tw-config').textContent);
  var panels = Array.from(app.querySelectorAll('[data-panel]'));
  var params = new URL(location.href).searchParams;
  // Spaces and their Views come from the page (task_views.SPACES); a View key is `view=`.
  var spaces = config.spaces, spaceOf = {}, lastView = {}, aliases = config.aliases || {};
  Object.keys(spaces).forEach(function (s) { spaces[s].forEach(function (v) { spaceOf[v] = s; }); lastView[s] = spaces[s][0]; });
  var first = spaces.task[0];
  var view = params.get('view') || params.get('space') || first;
  view = aliases[view] || view;
  if (!spaceOf[view]) view = first;
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
  function status(message) { document.getElementById('tw-status').textContent = message; }
  function saveURL() {
    var url = new URL(location.href);
    url.searchParams.set('view', view); url.searchParams.delete('space');
    history.replaceState(null, '', url);
  }
  function select(next) {
    view = next;
    status('');
    var space = spaceOf[view]; lastView[space] = view;
    app.querySelectorAll('[data-space-pane]').forEach(function (pane) { pane.classList.toggle('on', pane.dataset.spacePane === space); });
    app.querySelectorAll('nav.spaces [data-space]').forEach(function (b) {
      b.classList.toggle('on', b.dataset.space === space); b.setAttribute('aria-selected', String(b.dataset.space === space));
    });
    panels.forEach(function (panel) { panel.classList.toggle('on', panel.dataset.panel === view); });
    app.querySelectorAll('.wtab[data-view]').forEach(function (tab) { tab.classList.toggle('on', tab.dataset.view === view); });
    saveURL();
  }
  app.querySelectorAll('.wtab[data-view]').forEach(function (tab) {
    tab.addEventListener('click', function () { select(tab.dataset.view); });
  });
  // A Question row is selected by a click outside its links (Insight's .hl-row): the Task Runs
  // panel narrows to that Question's Runs and names it in each prompt (space-target).
  function pick(row) {
    var same = row && row.classList.contains('on');
    app.querySelectorAll('.hl-row.on').forEach(function (r) { r.classList.remove('on'); });
    if (row && !same) row.classList.add('on');
    document.dispatchEvent(new CustomEvent('space-target', {detail: {space: 'task', target: row && !same ? row.dataset.key : ''}}));
  }
  app.querySelectorAll('.hl-row').forEach(function (row) {
    row.addEventListener('click', function (event) { if (!event.target.closest('a,summary,button')) pick(row); });
  });
  app.querySelectorAll('[data-question]').forEach(function (a) {
    a.addEventListener('click', function (event) {
      var row = document.getElementById('question-' + a.dataset.question);
      if (!row) return;
      event.preventDefault();
      var panel = row.closest('[data-panel]'); if (panel) select(panel.dataset.panel);
      if (!row.classList.contains('on')) pick(row);
      row.scrollIntoView({block:'center'});
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
    editing.querySelector('.draw-edit').textContent = 'Edit drawing'; editing = null;
  }
  function prepareDrawing(row) {
    row.addEventListener('toggle', function () { loadDrawing(row); remember(); });
    var edit = row.querySelector('.draw-edit');
    if (!edit) { loadDrawing(row); return; }          // a generated drawing is view only
    edit.disabled = !config.studioEnabled;
    edit.addEventListener('click', function () {
      if (editing === row) { stopEditing(); status('Drawing viewer opened. Refresh is available.'); return; }
      stopEditing(); editing = row; row.open = true;
      row.querySelector('iframe').src = row.querySelector('iframe').dataset.src + '&edit=1';
      edit.textContent = 'Finish editing';
      status('The native Excalidraw editor saves this drawing. Automatic refresh is paused while editing.');
    });
    loadDrawing(row);
  }
  try {
    var folds = JSON.parse(sessionStorage.getItem(storageKey) || '{}');
    app.querySelectorAll('details').forEach(function (d) { if (Object.prototype.hasOwnProperty.call(folds, foldKey(d))) d.open = folds[foldKey(d)]; });
  } catch (_) { /* Use the document defaults. */ }
  app.querySelectorAll('details').forEach(function (d) { d.addEventListener('toggle', remember); });
  app.querySelectorAll('details.draw[data-board]').forEach(prepareDrawing);
  var drawingForm = document.getElementById('tw-add-drawing');
  drawingForm.querySelector('button').disabled = !config.studioEnabled;
  drawingForm.addEventListener('submit', async function (event) {
    event.preventDefault();
    if (!config.studioEnabled) return;
    var name = drawingForm.elements.name.value.trim();
    if (!/^[A-Za-z0-9][A-Za-z0-9_ -]{0,79}$/.test(name)) { drawingForm.querySelector('[role=status]').textContent = 'Use a name with letters, numbers, spaces, underscores or hyphens.'; return; }
    var path = config.studio + '/' + name + '.excalidraw';
    var existing = Array.from(app.querySelectorAll('details.draw[data-board]')).find(function (d) { return d.dataset.board === path; });
    if (existing) { existing.open = true; existing.scrollIntoView({block:'center'}); return; }
    var button = drawingForm.querySelector('button'); button.disabled = true;
    try {
      var response = await fetch('/' + path.split('/').map(encodeURIComponent).join('/'), {credentials:'same-origin'});
      var scene = await response.json();
      if (!response.ok || scene.type !== 'excalidraw') throw new Error(scene.err || 'Could not open this drawing.');
      var row = document.createElement('details'); row.className = 'draw'; row.dataset.board = path;
      var summary = document.createElement('summary'); summary.textContent = name; row.append(summary);
      var bar = document.createElement('div'); bar.className = 'st-bar';
      var left = document.createElement('span');
      var edit = document.createElement('button'); edit.type = 'button'; edit.className = 'draw-edit'; edit.textContent = 'Edit drawing'; left.append(edit);
      var where = document.createElement('span'); where.className = 'mono mut'; where.textContent = ' ' + path; left.append(where); bar.append(left);
      var source = '/_excalidraw/?' + new URLSearchParams({board:path});
      var full = document.createElement('a'); full.href = source + '&edit=1'; full.target = '_blank'; full.rel = 'noopener'; full.textContent = 'Open full screen ↗'; bar.append(full);
      var frame = document.createElement('iframe'); frame.className = 'st-frame'; frame.title = name; frame.referrerPolicy = 'no-referrer'; frame.dataset.src = source;
      row.append(bar, frame); document.getElementById('tw-drawings').append(row);
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
  app.querySelectorAll('nav.spaces [data-space]').forEach(function (b) {
    b.addEventListener('click', function () { select(lastView[b.dataset.space]); });
  });
  select(view);
})();
