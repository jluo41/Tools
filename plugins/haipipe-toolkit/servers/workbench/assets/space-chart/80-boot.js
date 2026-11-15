  function update(write = true) {
    if (inspector.open) inspector.close();
    const beforeState = prune(original, false);
    const unfilteredById = new Map();
    (function walk(node) {
      node.progressSource = progressKey(node.emptyMatch ? byId.get(node.id) : node);
      unfilteredById.set(node.id, node); node.children.forEach(walk);
    })(beforeState);
    const scope = unfilteredById.get(focusId) || byId.get(focusId) || original;
    currentTree = prune(original, true);
    (function retainSource(node) {
      const baseline = unfilteredById.get(node.id) || byId.get(node.id);
      node.progressSource = baseline.progressSource || progressKey(baseline);
      node.children.forEach(retainSource);
    })(currentTree);
    filteredById = new Map(); indexFiltered(currentTree);
    // Keep the chosen scope visible when any filter leaves it empty.
    currentFocus = filteredById.get(focusId);
    if (!currentFocus && byId.has(focusId)) {
      currentFocus = {...scope, children: [], emptyMatch: true}; collect(currentFocus);
    }
    if (!currentFocus) { focusId = 'space'; currentFocus = currentTree; }
    const unfiltered = unfilteredById.get(focusId) || currentFocus;
    breadcrumbs();
    setStats(currentFocus);
    setActiveFilters();
    setStatuses(unfiltered);
    zoom = 1; panX = 0; panY = 0;
    draw();
    if (view === 'radial') $('no-results').hidden = true;
    if (write) writeURL();
  }
  controls.example.addEventListener('change', () => selectFocus(controls.example.value || 'space'));
  controls.project.addEventListener('change', () => selectFocus(controls.project.value || exampleId || 'space'));
  controls.block.addEventListener('change', () => selectFocus(controls.block.value || projectId || exampleId || 'space'));
  controls.measure.addEventListener('change', () => {measure = controls.measure.value; syncSelectors(); update();});
  controls.jobs.addEventListener('change', () => {showJobs = controls.jobs.checked; syncSelectors(); update();});
  controls.tasks.addEventListener('change', () => {showTasks = controls.tasks.checked; syncSelectors(); update();});
  controls.names.addEventListener('change', () => {namePlacement = controls.names.value; update();});
  controls.archived.addEventListener('change', () => {
    includeArchived = controls.archived.checked;
    if (!includeArchived && byId.get(focusId)?.archived) {selectFocus(byId.get(blockId)?.parentId || 'space'); return;}
    syncSelectors(); update();
  });
  $('chart-refresh').addEventListener('click', () => location.reload());
  $('chart-reset').addEventListener('click', () => {
    if (params.has('project')) { leaveProjectScope(true); return; }
    selectedState = ''; selectedLevel = 'Task'; query = ''; kinds = new Set(); measure = 'blocks'; showJobs = true; showTasks = false; includeArchived = false; namePlacement = 'inside';
    $('board-filter').value = '';
    const all = document.querySelector('.kind-toggle[data-kind="all"]');
    if (all) all.click();
    selectFocus('space');
  });
  document.querySelectorAll('[data-home-view]').forEach((node) =>
    node.addEventListener('click', () => setView(node.dataset.homeView)));
  document.addEventListener('space-home-filter', (event) => {
    query = event.detail.query;
    kinds = new Set(event.detail.kinds);
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => {syncSelectors(); update();}, 100);
  });
  $('chart-legend').replaceChildren(...stateKeys.map((key) => {
    const item = el('span', labels[key]);
    item.prepend(el('i', undefined, 'chart-swatch status-' + key));
    return item;
  }));
  $('chart-read-at').textContent = 'Read at ' + new Date(payload.read_at).toLocaleString('en-US');
  if (!byId.has(focusId)) focusId = 'space';
  if (focusId === 'space' && params.has('project')) {
    const scopedProject = [...byId.values()].find((node) =>
      isProjectGroup(node) && node.path === params.get('project'));
    if (scopedProject) focusId = scopedProject.id;
  }
  if (byId.get(focusId)?.archived) includeArchived = true;
  const initialChain = ancestors(byId.get(focusId));
  projectId = (initialChain.find((n) => isProjectGroup(n)) || {}).id || '';
  blockId = (initialChain.find((n) => n.level === 'Block') || {}).id || '';
  exampleId = (initialChain.find((n) => n.level === 'Examples') || {}).id || exampleId;
  $('board-filter').value = query;
  $('board-filter').dispatchEvent(new Event('input', {bubbles: true}));
  syncSelectors();
  setView(view, false);
  update(false);
  window.addEventListener('resize', draw);
  if (typeof ResizeObserver !== 'undefined') new ResizeObserver(() => draw()).observe(canvas);
})();
