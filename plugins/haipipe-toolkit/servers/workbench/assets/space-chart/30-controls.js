  function setOptions(select, nodes, empty, selected) {
    select.replaceChildren(el('option', empty));
    select.firstChild.value = '';
    nodes.forEach((node) => {
      const option = el('option', node.level === 'Block' ? (node.folder + (node.archived ? ' [legacy]' : '') + (node.title && node.title !== node.folder ? ' · ' + node.title : '')) : node.name);
      option.value = node.id;
      select.append(option);
    });
    select.value = selected;
  }
  function syncSelectors() {
    const all = [...byId.values()];
    setOptions(controls.example, original.children, 'All groups', exampleId);
    setOptions(controls.project, all.filter((node) => isProjectGroup(node) &&
      (!exampleId || ancestors(node).some((p) => p.id === exampleId))), 'All Projects and Folders', projectId);
    setOptions(controls.block, all.filter((node) => node.level === 'Block' && (includeArchived || !node.archived) &&
      (!exampleId || ancestors(node).some((p) => p.id === exampleId)) &&
      (!projectId || ancestors(node).some((p) => p.id === projectId))), 'All Blocks', blockId);
    controls.measure.value = measure;
    controls.jobs.checked = showJobs;
    controls.jobs.disabled = measure === 'studios';
    controls.tasks.checked = showTasks;
    controls.tasks.disabled = measure === 'studios';
    controls.archived.checked = includeArchived;
    controls.names.value = namePlacement;
    panel.querySelector('.chart-top p').textContent = 'Groups → Projects / Folders → Themes → Blocks' +
      (measure === 'studios' ? ' → Studio topics (sNN)' : (showJobs ? ' → Jobs' : '') + (showTasks ? ' → Tasks' : ''));
  }
  function leaveProjectScope(reset = false, focus = 'space') {
    const url = new URL(location.href);
    ['project', 'focus', 'example', ...(reset ? ['kind', 'state', 'state_level', 'q', 'measure', 'jobs', 'tasks', 'archived', 'names'] : [])]
      .forEach((key) => url.searchParams.delete(key));
    url.searchParams.set('view', 'radial');
    if (focus !== 'space') { url.searchParams.set('focus', focus); url.searchParams.set('example', focus); }
    location.assign(url.pathname + url.search + url.hash);
  }
  function selectFocus(id) {
    if (inspector.open) inspector.close();
    if (params.has('project') && (id === 'space' || byId.get(id)?.level === 'Examples')) {
      leaveProjectScope(false, id); return;
    }
    focusId = id;
    const target = byId.get(id);
    if (target?.archived) includeArchived = true;
    const chain = ancestors(byId.get(id));
    const foundExample = chain.find((node) => node.level === 'Examples');
    const foundProject = chain.find((node) => isProjectGroup(node));
    const foundBlock = chain.find((node) => node.level === 'Block');
    exampleId = foundExample ? foundExample.id : '';
    projectId = foundProject ? foundProject.id : '';
    blockId = foundBlock ? foundBlock.id : '';
    syncSelectors();
    update();
  }
  function writeURL() {
    const url = new URL(location.href);
    const changes = {view, focus: focusId === 'space' ? '' : focusId, example: exampleId,
      measure: measure === 'blocks' ? '' : measure, state: selectedState, q: query, jobs: showJobs ? '1' : '0', tasks: showTasks ? '1' : '',
      archived: includeArchived ? '1' : '', names: namePlacement === 'outside' ? 'outside' : ''};
    changes.state_level = selectedState ? selectedLevel : '';
    Object.entries(changes).forEach(([key, value]) => value ? url.searchParams.set(key, value) : url.searchParams.delete(key));
    history.replaceState(null, '', url.pathname + url.search + url.hash);
  }
  function setView(next, write = true) {
    if (inspector.open) inspector.close();
    view = next;
    panel.hidden = view !== 'radial';
    $('board-list').hidden = view !== 'list';
    $('no-results').hidden = view !== 'list' || !!document.querySelector('.space-section:not([hidden])') ||
      !document.querySelector('.space-section');
    document.querySelectorAll('[data-home-view]').forEach((node) =>
      node.setAttribute('aria-pressed', String(node.dataset.homeView === view)));
    document.querySelector('main').classList.toggle('home-chart-view', view === 'radial');
    if (kindFilters) {
      if (view === 'radial') $('chart-kind-slot').append(kindFilters);
      else kindHomeSlot.after(kindFilters);
    }
    if (write) writeURL();
    if (view === 'radial' && currentFocus) draw();
  }
  function setStats(node) {
    const p = progress(node);
    const parents = ancestors(byId.get(node.id));
    const projects = node.stats.projects || +parents.some((n) => n.level === 'Project');
    const folders = node.stats.folders || +parents.some((n) => n.level === 'Folder');
    const summaries = [];
    if (projects || !folders) summaries.push(['Projects', projects]);
    if (folders) summaries.push(['Folders', folders]);
    summaries.push(['Blocks', node.stats.blocks || +parents.some((n) => n.level === 'Block')],
      ['Jobs', node.stats.jobs], ['Tasks', node.stats.tasks], ['Studio topics (sNN)', node.stats.studios],
      [p.source + ' completion', p.total ? pct(p.done, p.total) : '—']);
    $('chart-stats').replaceChildren(...summaries.map(([label, value]) => {
      const item = el('div', undefined, 'chart-stat');
      item.append(el('strong', typeof value === 'number' ? number(value) : value), el('span', label));
      if (label.endsWith('completion')) item.title = number(p.done) + ' / ' + number(p.total) + ' complete';
      return item;
    }));
  }
  function setActiveFilters() {
    const items = [];
    if (query) items.push(button('Search: ' + query + ' ×', () => {
      $('board-filter').value = '';
      $('board-filter').dispatchEvent(new Event('input', {bubbles: true}));
    }));
    if (kinds.size) items.push(button('Type: ' + [...kinds].join(', ') + ' ×', () => {
      document.querySelector('.kind-toggle[data-kind="all"]')?.click();
    }));
    if (selectedState) items.push(button(selectedLevel + ': ' + labels[selectedState] + ' ×', () => {
      selectedState = ''; update();
    }));
    const active = $('chart-active-filters');
    active.hidden = !items.length;
    active.replaceChildren(...items);
    $('chart-filter-count').textContent = items.length ? items.length + ' active' : '';
    $('chart-layer-summary').textContent = measure === 'studios' ? 'Studio topics (sNN)' :
      [showJobs ? 'Jobs shown' : 'Jobs hidden', showTasks ? 'Tasks shown' : 'Tasks hidden',
        includeArchived ? 'Legacy included' : ''].filter(Boolean).join(' · ');
  }
  function setStatuses(unfiltered) {
    const rows = ['Block', 'Job', 'Task'].map((level) => {
      const row = el('div', undefined, 'chart-status-row');
      row.dataset.level = level;
      row.setAttribute('role', 'group');
      row.setAttribute('aria-label', level + ' status');
      const states = unfiltered.stats[{Block: 'blockStates', Job: 'jobStates', Task: 'taskStates'}[level]];
      const total = Object.values(states).reduce((sum, count) => sum + count, 0);
      const active = selectedLevel === level && !!selectedState;
      const caption = el('span', level + ' status', 'chart-status-caption');
      const all = button('All ' + number(total), () => {selectedState = ''; update();});
      all.setAttribute('aria-pressed', String(!selectedState));
      all.dataset.state = 'all';
      const nodes = stateKeys.map((key) => {
        const control = button(labels[key] + ' ' + number(states[key]), () => {
          selectedState = active && selectedState === key ? '' : key;
          selectedLevel = level;
          if (selectedState && level === 'Job') showJobs = true;
          if (selectedState && level === 'Task') {showJobs = true; showTasks = true;}
          syncSelectors();
          update();
        }, 'chart-status-button');
        control.prepend(el('i', undefined, 'chart-swatch status-' + key));
        control.setAttribute('aria-pressed', String(active && selectedState === key));
        control.dataset.state = key;
        return control;
      });
      row.append(caption, all, ...nodes);
      return row;
    });
    const note = el('div', undefined, 'chart-status-note');
    note.append(el('span', selectedState ? 'Filtering ' + selectedLevel + ' status: ' + labels[selectedState] + '. ' :
      'Recorded states at each level. '));
    note.append(el('span', 'Counts are before the status filter. Choose one level at a time; matching Blocks or Jobs keep their children.'));
    if (selectedState) note.append(button('Clear status filter', () => {selectedState = ''; update();}));
    $('chart-status').replaceChildren(...rows, note);
  }
  function recordedStatus(node) {
    return ['Block', 'Job', 'Task'].includes(node.level) ? node.level + ' status: ' + labels[node.status || 'unknown'] : '';
  }
  function statusSummary(node) {
    const container = el('div', undefined, 'chart-status-summary');
    ['Block', 'Job', 'Task'].forEach((level) => {
      const states = node.stats[{Block: 'blockStates', Job: 'jobStates', Task: 'taskStates'}[level]];
      if (!Object.values(states).some(Boolean)) return;
      const row = el('div', undefined, 'chart-summary-row');
      row.append(el('strong', level + ' status'));
      stateKeys.filter((key) => states[key]).forEach((key) => {
        const item = el('span', labels[key] + ' ' + number(states[key]));
        item.prepend(el('i', undefined, 'chart-swatch status-' + key));
        row.append(item);
      });
      container.append(row);
    });
    return container;
  }
  function breadcrumbs() {
    const nodes = ancestors(byId.get(focusId) || original).filter((node) => showJobs || node.level !== 'Job' || node.id === focusId);
    $('chart-breadcrumb').replaceChildren(...nodes.map((node, index) => {
      const control = button(index === 0 ? 'All SPACE' : node.name, () => selectFocus(node.id));
      if (node.id === focusId) control.setAttribute('aria-current', 'location');
      return control;
    }));
  }
  function touchDetails(event) {
    return event?.pointerType === 'touch' || event?.pointerType === 'pen' ||
      window.matchMedia('(hover: none), (pointer: coarse), (max-width: 840px)').matches;
  }
  function interactionHint() {
    if (measure === 'studios') return 'Select a Studio topic for details and its drawing.';
    return touchDetails() ? 'Tap a segment for details, then choose Zoom in.' :
      'Hover for details · Click a segment to focus · + / − to magnify';
  }
  function activateNode(node, event) {
    if (node.level === 'Studio' || touchDetails(event)) showPreview(node);
    else selectFocus(node.id);
  }
