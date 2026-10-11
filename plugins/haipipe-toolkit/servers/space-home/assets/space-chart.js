(() => {
  'use strict';
  const panel = document.getElementById('space-chart');
  if (!panel) return;
  const payload = JSON.parse(document.getElementById('space-chart-data').textContent);
  const original = payload.tree;
  const byId = new Map();
  const labels = {done: 'Done', active: 'In progress', open: 'Open', blocked: 'Blocked', paused: 'Paused', unknown: 'Unknown'};
  const stateKeys = Object.keys(labels);
  const $ = (id) => document.getElementById(id);
  const controls = {example: $('chart-example'), project: $('chart-project'), block: $('chart-block'),
    measure: $('chart-measure'), jobs: $('chart-jobs'), tasks: $('chart-tasks'),
    archived: $('chart-archived'), names: $('chart-names')};
  const canvas = $('chart-canvas');
  const kindFilters = document.querySelector('.kind-filter');
  const kindHomeSlot = document.createComment('Block type controls in List Index');
  if (kindFilters) kindFilters.before(kindHomeSlot);
  const scopeLabel = el('div', undefined, 'chart-scope-label');
  const nameKey = el('details', undefined, 'chart-name-key');
  nameKey.setAttribute('aria-label', 'Project, folder, and theme names');
  nameKey.open = false;
  canvas.before(scopeLabel);
  canvas.after(nameKey);
  const svgNS = 'http://www.w3.org/2000/svg';
  const params = new URLSearchParams(location.search);
  let focusId = params.get('focus') || 'space';
  let exampleId = params.get('example') || '';
  let projectId = '';
  let blockId = '';
  let selectedState = stateKeys.includes(params.get('state')) ? params.get('state') : '';
  let selectedLevel = ['Block', 'Job', 'Task'].includes(params.get('state_level')) ? params.get('state_level') : 'Task';
  let query = params.get('q') || '';
  let kinds = new Set([...document.querySelectorAll('.kind-toggle[aria-pressed="true"]')]
    .map((node) => node.dataset.kind).filter((kind) => kind !== 'all'));
  let measure = ['tasks', 'jobs', 'blocks', 'studios'].includes(params.get('measure')) ? params.get('measure') : 'blocks';
  let showJobs = params.get('jobs') !== '0';
  let showTasks = params.get('tasks') === '1';
  let includeArchived = params.get('archived') === '1';
  let namePlacement = params.get('names') === 'outside' ? 'outside' : 'inside';
  let view = params.get('view') === 'list' ? 'list' : 'radial';
  let currentTree;
  let currentFocus;
  let filteredById = new Map();
  let effectiveMeasure = measure;
  let searchTimer;
  let previewNode = null;
  let zoom = 1, panX = 0, panY = 0;
  let figureWidth = 0, figureHeight = 0;
  let drag = null, suppressClick = false;
  const inspector = el('dialog', undefined, 'chart-inspector');
  inspector.id = 'chart-inspector';
  inspector.setAttribute('aria-labelledby', 'chart-inspector-title');
  panel.append(inspector);
  inspector.addEventListener('close', () => {
    previewNode = null;
    canvas.querySelectorAll('.is-inspected').forEach((mark) => mark.classList.remove('is-inspected'));
    clearHover();
  });
  inspector.addEventListener('click', (event) => {
    const rect = inspector.getBoundingClientRect();
    if (event.target === inspector && (event.clientX < rect.left || event.clientX > rect.right ||
      event.clientY < rect.top || event.clientY > rect.bottom)) inspector.close();
  });

  function el(tag, text, className) {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = text;
    if (className) node.className = className;
    return node;
  }
  function button(text, action, className) {
    const node = el('button', text, className);
    node.type = 'button';
    if (action) node.addEventListener('click', action);
    return node;
  }
  function number(value) { return value.toLocaleString('en-US'); }
  function pct(a, b) { return b ? (100 * a / b).toFixed(1).replace(/\.0$/, '') + '%' : '—'; }
  function blankStates() { return Object.fromEntries(stateKeys.map((key) => [key, 0])); }
  function isProjectGroup(node) { return ['Project', 'Folder'].includes(node?.level); }
  function collect(node) {
    const out = {projects: +(node.level === 'Project'), folders: +(node.level === 'Folder'), blocks: +(node.level === 'Block'),
      jobs: +(node.level === 'Job'), tasks: +(node.level === 'Task'),
      studios: node.emptyMatch ? 0 : node.level === 'Studio' ? 1 : (node.studios || []).length,
      taskStates: blankStates(), jobStates: blankStates(), blockStates: blankStates()};
    const own = {Task: 'taskStates', Job: 'jobStates', Block: 'blockStates'}[node.level];
    const ownCount = {Project: 'projects', Folder: 'folders', Block: 'blocks', Job: 'jobs', Task: 'tasks'}[node.level];
    if (node.emptyMatch && ownCount) out[ownCount] = 0;
    if (own && !node.emptyMatch) out[own][node.status || 'unknown']++;
    node.children.forEach((child) => {
      const sub = child.stats || collect(child);
      ['projects', 'folders', 'blocks', 'jobs', 'tasks', 'studios'].forEach((key) => out[key] += sub[key]);
      ['taskStates', 'jobStates', 'blockStates'].forEach((key) =>
        stateKeys.forEach((state) => out[key][state] += sub[key][state]));
    });
    node.stats = out;
    return out;
  }
  function prepare(node, parent, inherited = '') {
    node.parentId = parent ? parent.id : '';
    node.kind = node.kind || (parent && parent.kind) || '';
    node.archived = node.archived || !!parent?.archived;
    node.search = (inherited + ' ' + [node.name, node.title, node.folder, node.path, node.note].filter(Boolean).join(' ')).toLowerCase();
    byId.set(node.id, node);
    (node.studios || []).forEach((topic) => prepare(topic, node, node.search));
    const studioSearch = (node.studios || []).map((topic) => topic.search).join(' ');
    node.children.forEach((child) => prepare(child, node, node.search + ' ' + studioSearch));
    collect(node);
  }
  prepare(original, null);
  function ancestors(node) {
    const result = [];
    while (node) { result.unshift(node); node = byId.get(node.parentId); }
    return result;
  }
  function progressKey(node) {
    return node.stats.tasks ? 'tasks' : node.stats.jobs ? 'jobs' : 'blocks';
  }
  function progress(node) {
    const countKey = node.progressSource || progressKey(node.emptyMatch ? byId.get(node.id) : node);
    const source = {tasks: 'Task', jobs: 'Job', blocks: 'Block'}[countKey];
    const states = node.emptyMatch ? blankStates() :
      node.stats[{tasks: 'taskStates', jobs: 'jobStates', blocks: 'blockStates'}[countKey]];
    return {total: node.emptyMatch ? 0 : node.stats[countKey], states, source, done: states.done};
  }
  function colorClass(node) {
    if (node.level === 'Studio') return 'status-unknown';
    if (node.level === 'Task' || (!node.children.length && node.status)) return 'status-' + (node.status || 'unknown');
    const p = progress(node);
    if (!p.total || p.states.unknown === p.total) return 'status-unknown';
    if (p.done === p.total) return 'status-done';
    if (p.states.blocked) return 'status-blocked';
    if (p.states.active || p.done) return 'status-active';
    if (p.states.paused === p.total) return 'status-paused';
    return 'status-open';
  }
  function tone(node) {
    if (!node.children.length) return '';
    const p = progress(node);
    if (!p.total || p.states.unknown === p.total || p.states.paused === p.total) return '';
    return `color-mix(in srgb, var(--chart-done) ${100 * p.done / p.total}%, var(--chart-open))`;
  }
  function prune(node, withState, matchedParent = false) {
    if (node.archived && !includeArchived) return null;
    if (node.level === 'Examples' && exampleId && node.id !== exampleId) return null;
    if (isProjectGroup(node) && projectId && node.id !== projectId) return null;
    if (node.level === 'Block' && blockId && node.id !== blockId) return null;
    if (node.kind && kinds.size && !kinds.has(node.kind)) return null;
    let matched = matchedParent;
    if (withState && selectedState && node.level === selectedLevel) {
      if ((node.status || 'unknown') !== selectedState) return null;
      matched = true;
    }
    const children = node.children.map((child) => prune(child, withState, matched)).filter(Boolean);
    if (node.children.length && !children.length && node.level !== 'Space') return null;
    if (!node.children.length && node.level !== 'Space') {
      if (query && !node.search.includes(query.toLowerCase()) &&
        !(node.studios || []).some((topic) => topic.search.includes(query.toLowerCase()))) return null;
      if (withState && selectedState && !matched) return null;
    }
    const copy = {...node, children, emptyMatch: !!node.children.length && !children.length};
    collect(copy);
    return copy;
  }
  function visual(node) {
    if (measure === 'studios' && node.level === 'Block') {
      return {...node, children: node.emptyMatch ? [] : (node.studios || [])};
    }
    const children = [];
    node.children.forEach((child) => {
      if (child.level === 'Task' && !showTasks) return;
      if (!showJobs && child.level === 'Job') {
        if (showTasks) child.children.forEach((task) => children.push(visual(task)));
      } else children.push(visual(child));
    });
    return {...node, children};
  }
  function indexFiltered(node) {
    filteredById.set(node.id, node);
    node.children.forEach(indexFiltered);
  }
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
  function showPreview(node) {
    previewNode = node;
    const heading = el('h3', node.name);
    heading.id = 'chart-inspector-title';
    const header = el('div', undefined, 'chart-inspector-head');
    const close = button('Close', () => inspector.close(), 'chart-inspector-close');
    close.setAttribute('aria-label', 'Close details');
    header.append(el('p', displayLevel(node), 'chart-level'), close);
    const content = el('div', undefined, 'chart-inspector-content');
    const project = ancestors(byId.get(node.id)).find((parent) => isProjectGroup(parent));
    const p = progress(node);
    content.append(heading);
    if (node.archived) content.append(el('p', 'Legacy Block: excluded from the default overview.', 'chart-note'));
    if (node.title && node.title !== node.name) content.append(el('p', 'Page title: ' + node.title, 'chart-note'));
    if (project && !isProjectGroup(node)) content.append(el('p', displayLevel(project) + ': ' + project.name));
    content.append(el('p', summaryLine(node)),
      el('p', 'Share of current view: ' + pct(node.weight, currentFocus.weight)));
    if (node.level !== 'Studio') content.append(el('p', p.source + ' completion: ' + number(p.done) + ' / ' + number(p.total) +
        ' (' + pct(p.done, p.total) + ')'));
    if (node.state && node.level !== 'Studio') content.append(el('p', 'Page status: ' + node.state));
    if (node.level !== 'Studio') content.append(statusSummary(node));
    if (node.level === 'Block') content.append(studioList(node));
    if (node.note) content.append(el('p', node.note, 'chart-note'));
    if (node.path) content.append(el('p', node.path, 'chart-path'));
    const actions = el('div', undefined, 'chart-inspector-actions');
    if (node.children.length && node.id !== focusId) actions.append(button('Zoom in', () => selectFocus(node.id), 'chart-inspector-zoom'));
    if (node.href) {
      const link = el('a', openLabel(node), 'chart-open');
      link.href = node.href;
      actions.append(link);
    }
    if (!node.children.length && node.level !== 'Studio') content.append(el('p', 'No deeper levels. Open the work page to read its content.', 'chart-note'));
    inspector.replaceChildren(header, content, actions);
    canvas.querySelectorAll('[data-chart-node]').forEach((mark) =>
      mark.classList.toggle('is-inspected', mark.dataset.chartNode === node.id));
    hover(node);
    if (!inspector.open) inspector.showModal();
    (actions.querySelector('button, a') || close).focus({preventScroll: true});
  }
  function summaryLine(node) {
    if (node.level === 'Studio') return number(node.drawings) + ' drawing' + (node.drawings === 1 ? '' : 's') + ' · Block Studio topic';
    return [node.stats.blocks && number(node.stats.blocks) + ' Blocks',
      node.stats.jobs && number(node.stats.jobs) + ' Jobs', number(node.stats.tasks) + ' Tasks',
      (node.level === 'Block' || node.stats.studios) && number(node.stats.studios) + ' Studio topics (sNN)'].filter(Boolean).join(' · ');
  }
  function studioList(node) {
    const section = el('section', undefined, 'chart-studios');
    section.setAttribute('aria-label', 'Block Studio topics');
    const topics = node.emptyMatch ? [] : (node.studios || []);
    section.append(el('h4', 'Studio topics (sNN) · ' + number(topics.length)));
    if (!topics.length) section.append(el('p', 'No sNN topic folders in this Block’s studio/.', 'chart-note'));
    topics.forEach((topic) => {
      const link = el('a', undefined, 'chart-studio-topic');
      link.href = topic.href;
      link.append(el('strong', topic.folder), el('small', number(topic.drawings) + ' drawing' + (topic.drawings === 1 ? '' : 's') + ' · Open topic ↗'));
      section.append(link);
    });
    return section;
  }
  function selection() {
    const node = currentFocus;
    const p = progress(node);
    const heading = el('h3', node.name);
    const level = el('p', displayLevel(node), 'chart-level');
    const totals = el('p', summaryLine(node));
    const rate = el('p', p.source + ' completion: ' + number(p.done) + ' / ' + number(p.total) + ' (' + pct(p.done, p.total) + ')');
    const nodes = [level, heading, totals, rate];
    if (node.archived) nodes.push(el('p', 'Legacy Block: excluded from the default overview.', 'chart-note'));
    if (node.title && node.title !== node.name) nodes.splice(2, 0, el('p', 'Page title: ' + node.title, 'chart-note'));
    if (node.path) nodes.push(el('p', node.path, 'chart-path'));
    if (node.state) nodes.push(el('p', 'Page status: ' + node.state, 'chart-own-state'));
    nodes.push(statusSummary(node));
    if (node.note) nodes.push(el('p', node.note, 'chart-note'));
    if (!node.stats.tasks && node.stats.jobs) nodes.push(el('p', 'No Tasks in this scope; completion uses Job states.', 'chart-note'));
    if (node.href) {
      const link = el('a', openLabel(node), 'chart-open');
      link.href = node.href;
      nodes.push(link);
    }
    if (node.level === 'Block' && measure !== 'studios') nodes.push(studioList(node));
    $('chart-selection').replaceChildren(...nodes);
    const display = visual(node);
    weights(display);
    const children = display.children;
    $('chart-scope-count').textContent = children.length ? number(children.length) + ' items' : 'No deeper levels';
    const section = $('chart-children');
    const headingRow = el('h4', measure === 'studios' && node.level === 'Block' ? 'Studio topics (sNN) · ' + number(children.length) : children.length ? 'Next level · ' + number(children.length) : !showTasks && node.stats.tasks ? 'Task layer hidden · ' + number(node.stats.tasks) + ' Tasks' : 'No deeper levels');
    const rows = children.slice().sort((a, b) => b.stats[effectiveMeasure] - a.stats[effectiveMeasure]);
    section.replaceChildren(headingRow, ...rows.map((child) => {
      const control = button('', (event) => activateNode(child, event), 'chart-child');
      const copy = el('span', undefined, 'chart-child-copy');
      copy.append(el('strong', child.name));
      if (child.title && child.title !== child.name) copy.append(el('small', child.title));
      copy.append(el('small', displayLevel(child) + ' · ' + summaryLine(child)));
      if (recordedStatus(child)) copy.append(el('small', recordedStatus(child), 'chart-child-status'));
      const sub = progress(child);
      const value = el('span', undefined, 'chart-child-value');
      value.append(el('strong', pct(child.weight, display.weight)),
        el('small', child.level === 'Studio' ? 'Studio topic' : sub.total ? 'completion ' + pct(sub.done, sub.total) : 'No status items'));
      const swatch = el('i', undefined, 'chart-swatch ' + colorClass(child));
      if (tone(child)) swatch.style.background = tone(child);
      control.append(swatch, copy, value);
      return control;
    }));
    if (measure !== 'studios' && !showTasks && node.stats.tasks) {
      section.append(el('p', number(node.stats.tasks) + ' Tasks are counted in completion. Enable Show Task layer to draw them.', 'chart-note'));
    }
  }
  function svg(tag, attrs = {}, text) {
    const node = document.createElementNS(svgNS, tag);
    Object.entries(attrs).forEach(([key, value]) => node.setAttribute(key, value));
    if (text !== undefined) node.textContent = text;
    return node;
  }
  function themeName(node) {
    return node.name.charAt(0).toUpperCase() + node.name.slice(1);
  }
  function displayLevel(node) { return node.level === 'Examples' ? 'Group' : node.level === 'Scene' ? 'Theme' : node.level === 'Studio' ? 'Studio topic' : node.level; }
  function openLabel(node) {
    if (node.linked && node.level === 'Examples') return 'Open ' + node.name + ' Index ↗';
    if (node.level === 'Folder') return 'Open Folder Index ↗';
    if (node.level === 'Project') return 'Open Project Index ↗';
    return node.level === 'Studio' ? 'Open Studio topic ↗' : 'Open work page ↗';
  }
  function nameRecords(node) {
    if (isProjectGroup(node)) return node.children.filter((child) => child.level === 'Scene');
    const records = [];
    (function walk(parent) {
      parent.children.forEach((child) => {
        if (isProjectGroup(child)) records.push(child);
        else walk(child);
      });
    })(node);
    return records;
  }
  function wrapName(text, limit) {
    const lines = [];
    while (text.length > limit) {
      const sample = text.slice(0, limit + 1);
      let cut = Math.max(sample.lastIndexOf('-') + 1, sample.lastIndexOf(' '));
      if (cut < limit / 2) cut = limit;
      lines.push(text.slice(0, cut));
      text = text.slice(cut);
    }
    if (text) lines.push(text);
    return lines;
  }
  function stackLabels(items, minY, maxY) {
    items.sort((a, b) => a.anchorY - b.anchorY);
    items.forEach((item, index) => {
      const previous = items[index - 1];
      item.y = Math.max(minY + item.height / 2, item.anchorY,
        previous ? previous.y + (previous.height + item.height) / 2 + 8 : minY);
    });
    for (let i = items.length - 1; i >= 0; i--) {
      const next = items[i + 1], item = items[i];
      item.y = Math.min(item.y, maxY - item.height / 2,
        next ? next.y - (next.height + item.height) / 2 - 8 : maxY);
    }
    return items;
  }
  function bindNameControl(control, node) {
    control.addEventListener('click', (event) => {event.stopPropagation(); activateNode(node, event);});
    control.addEventListener('pointerenter', (event) => {
      if (event.pointerType === 'mouse' && !touchDetails() && !inspector.open) hover(node);
    });
    control.addEventListener('pointerleave', clearHover);
  }
  function drawNames(group, records, radius, labelWidth, initialHeight) {
    const candidates = records.map((record) => {
      const name = record.node.level === 'Scene' ? themeName(record.node) : record.node.name;
      const themes = record.node.children.filter((child) => child.level === 'Scene');
      const secondary = themes.length ? 'Themes: ' + themes.map(themeName).join(' · ') :
        summaryLine(record.node);
      const lines = wrapName(name, Math.max(18, Math.floor(labelWidth / 7.1)));
      const subLines = wrapName(secondary, Math.max(20, Math.floor(labelWidth / 6.2)));
      const angle = (record.start + record.end) / 2;
      return {...record, angle, side: Math.sin(angle) >= 0 ? 1 : -1,
        anchorY: -radius * Math.cos(angle), lines, subLines,
        height: lines.length * 17 + subLines.length * 15 + 10};
    });
    const sides = [-1, 1].map((side) => candidates.filter((item) => item.side === side));
    const height = Math.max(initialHeight, ...sides.map((items) =>
      items.reduce((sum, item) => sum + item.height + 8, 24)));
    const labelsGroup = svg('g', {class: 'chart-name-labels'});
    sides.forEach((items) => {
      stackLabels(items, -height / 2 + 12, height / 2 - 12).forEach((item) => {
        const x = item.side * (radius + 36);
        const anchor = item.side === 1 ? 'start' : 'end';
        const start = point(radius + 3, item.angle), shoulder = point(radius + 16, item.angle);
        const callout = svg('g', {class: 'chart-name-label', 'data-chart-label': item.node.id,
          'data-chart-node': item.node.id});
        callout.append(svg('polyline', {points: `${start} ${shoulder} ${item.side * (radius + 24)},${item.y} ${x - item.side * 5},${item.y}`,
          class: 'chart-name-line'}));
        callout.append(svg('circle', {cx: start[0], cy: start[1], r: 2.5, class: 'chart-name-dot'}));
        callout.append(svg('rect', {x: item.side === 1 ? x - 4 : x - labelWidth - 4,
          y: item.y - item.height / 2, width: labelWidth + 8, height: item.height, rx: 4,
          class: 'chart-name-background'}));
        let y = item.y - item.height / 2 + 17;
        item.lines.forEach((line) => {
          callout.append(svg('text', {x, y, 'text-anchor': anchor, class: 'chart-name-title'}, line));
          y += 17;
        });
        item.subLines.forEach((line) => {
          callout.append(svg('text', {x, y, 'text-anchor': anchor, class: 'chart-name-theme'}, line));
          y += 15;
        });
        bindNameControl(callout, item.node);
        labelsGroup.append(callout);
      });
    });
    group.append(labelsGroup);
    return height;
  }
  function setNameKey(node, records, outsideNames) {
    const project = ancestors(byId.get(node.id)).find((parent) => isProjectGroup(parent));
    const theme = ancestors(byId.get(node.id)).find((parent) => parent.level === 'Scene');
    const context = project && project.id !== node.id ? project.name + ' › ' +
      (theme && theme.id !== node.id ? themeName(theme) + ' › ' : '') : '';
    scopeLabel.replaceChildren(el('strong', context + (node.level === 'Scene' ? themeName(node) : node.name)),
      el('small', 'Area: ' + {blocks: 'Blocks', jobs: 'Jobs', tasks: 'Tasks', studios: 'Studio topics (sNN)'}[effectiveMeasure]));
    const visible = outsideNames ? records.filter((record) => !record.weight) : records;
    nameKey.hidden = !visible.length;
    if (!visible.length) return;
    const isThemes = isProjectGroup(node);
    const title = outsideNames ? (isThemes ? 'Themes' : 'Projects') + ' outside the chart' : isThemes ? 'Theme names' : 'Project, folder, and theme names';
    const summary = el('summary', title + ' · ' + number(visible.length));
    const list = el('div', undefined, 'chart-name-list');
    visible.forEach((record) => {
      const row = el('div', undefined, 'chart-name-row');
      const control = button('', undefined, 'chart-key-name');
      const swatch = el('i', undefined, 'chart-swatch ' + colorClass(record));
      if (tone(record)) swatch.style.background = tone(record);
      const copy = el('span');
      copy.append(el('strong', record.level === 'Scene' ? themeName(record) : record.name));
      if (!record.weight) copy.append(el('small', 'No ' + effectiveMeasure + ' in this view. Select to inspect.'));
      control.append(swatch, copy);
      bindNameControl(control, record);
      row.append(control);
      const themes = record.children.filter((child) => child.level === 'Scene');
      if (themes.length) {
        const themeRow = el('div', undefined, 'chart-key-themes');
        themeRow.append(el('span', 'Themes:'));
        themes.forEach((theme) => {
          const link = button(themeName(theme), undefined);
          bindNameControl(link, theme);
          themeRow.append(link);
        });
        row.append(themeRow);
      }
      list.append(row);
    });
    nameKey.replaceChildren(summary, list);
  }
  function point(radius, angle) { return [radius * Math.sin(angle), -radius * Math.cos(angle)]; }
  function ringPath(start, end, inner, outer) {
    const endSafe = Math.min(end, start + Math.PI * 2 - 0.00001);
    const a = point(outer, start), b = point(outer, endSafe), c = point(inner, endSafe), d = point(inner, start);
    const large = endSafe - start > Math.PI ? 1 : 0;
    return `M${a} A${outer},${outer} 0 ${large} 1 ${b} L${c} A${inner},${inner} 0 ${large} 0 ${d} Z`;
  }
  function projectName(group, node, start, end, inner, outer, index) {
    const middle = (inner + outer) / 2;
    const available = middle * (end - start) - 16;
    const maxLines = Math.min(3, Math.floor((outer - inner - 10) / 18));
    if (available < 52 || maxLines < 1) return;
    let font = 15, lines;
    for (; font >= 11; font--) {
      lines = wrapName(node.name, Math.max(6, Math.floor(available / (font * .58))));
      if (lines.length <= maxLines) break;
    }
    if (font < 11) return;
    const angle = (start + end) / 2;
    const reversed = angle > Math.PI / 2 && angle < Math.PI * 1.5;
    lines.forEach((line, i) => {
      const radius = middle + (i - (lines.length - 1) / 2) * 18 * (reversed ? 1 : -1);
      const from = point(radius, reversed ? end : start);
      const to = point(radius, reversed ? start : end);
      const id = 'chart-project-text-' + index + '-' + i;
      group.append(svg('path', {id, d: `M${from} A${radius},${radius} 0 ${end - start > Math.PI ? 1 : 0} ${reversed ? 0 : 1} ${to}`, fill: 'none', stroke: 'none'}));
      const text = svg('text', {class: 'chart-project-name', 'font-size': font, 'text-anchor': 'middle', 'data-project-name': node.id});
      text.append(svg('textPath', {href: '#' + id, startOffset: '50%'}, line));
      group.append(text);
    });
  }
  function weights(node, forced) {
    node.weight = forced === undefined ? node.stats[effectiveMeasure] : forced;
    const below = (effectiveMeasure === 'blocks' && ['Block', 'Job', 'Task'].includes(node.level)) ||
      (effectiveMeasure === 'jobs' && ['Job', 'Task'].includes(node.level));
    if (below || forced !== undefined) {
      const scores = node.children.map((child) => child.stats.tasks || child.stats.jobs || 1);
      const total = scores.reduce((a, b) => a + b, 0);
      node.children.forEach((child, index) => weights(child, node.weight * scores[index] / total));
    } else node.children.forEach((child) => weights(child));
  }
  function depth(node) { return node.children.length ? 1 + Math.max(...node.children.map(depth)) : 0; }
  function hover(node) {
    canvas.querySelectorAll('[data-chart-node]').forEach((mark) => {
      const id = mark.dataset.chartNode;
      const related = id === node.id || ancestors(byId.get(id)).some((p) => p.id === node.id) ||
        ancestors(byId.get(node.id)).some((p) => p.id === id);
      mark.style.opacity = related ? '1' : '.24';
    });
    const p = progress(node);
    $('chart-hover').textContent = node.name + ' · ' + summaryLine(node) +
      ' · Share of current scope ' + pct(node.weight, currentFocus.weight) + (node.level === 'Studio' ? '' : ' · ' + p.source + ' completion ' + pct(p.done, p.total)) +
      (recordedStatus(node) ? ' · ' + recordedStatus(node) : '');
  }
  function clearHover() {
    if (inspector.open) return;
    canvas.querySelectorAll('[data-chart-node]').forEach((mark) => mark.style.opacity = '');
    $('chart-hover').textContent = interactionHint();
  }
  function applyCamera() {
    const figure = canvas.querySelector('svg');
    if (!figure || !figureWidth || !figureHeight) return;
    const limitX = figureWidth * (1 - 1 / zoom) / 2;
    const limitY = figureHeight * (1 - 1 / zoom) / 2;
    panX = Math.max(-limitX, Math.min(limitX, panX));
    panY = Math.max(-limitY, Math.min(limitY, panY));
    const width = figureWidth / zoom, height = figureHeight / zoom;
    figure.setAttribute('viewBox', `${(figureWidth - width) / 2 - panX} ${(figureHeight - height) / 2 - panY} ${width} ${height}`);
    canvas.classList.toggle('is-zoomed', zoom > 1);
    $('chart-zoom-value').textContent = Math.round(zoom * 100) + '%';
    $('chart-zoom-out').disabled = zoom <= 1;
    $('chart-zoom-in').disabled = zoom >= 6;
    $('chart-up').disabled = currentFocus.id === 'space';
  }
  function changeZoom(next) {
    zoom = Math.max(1, Math.min(6, next));
    applyCamera();
    clearHover();
  }
  $('chart-zoom-in').addEventListener('click', () => changeZoom(zoom * 1.5));
  $('chart-zoom-out').addEventListener('click', () => changeZoom(zoom / 1.5));
  $('chart-fit').addEventListener('click', () => {panX = 0; panY = 0; changeZoom(1);});
  $('chart-up').addEventListener('click', () => selectFocus(byId.get(focusId).parentId || 'space'));
  $('chart-details').addEventListener('click', () => showPreview(currentFocus));
  canvas.addEventListener('pointerdown', (event) => {
    suppressClick = false;
    if (zoom <= 1 || event.button !== 0 || inspector.open) return;
    drag = {id: event.pointerId, x: event.clientX, y: event.clientY, panX, panY, moved: false};
  });
  canvas.addEventListener('pointermove', (event) => {
    if (!drag || event.pointerId !== drag.id) return;
    const dx = event.clientX - drag.x, dy = event.clientY - drag.y;
    if (!drag.moved && Math.hypot(dx, dy) < 5) return;
    if (!drag.moved) {
      drag.moved = true;
      canvas.setPointerCapture(event.pointerId);
      canvas.classList.add('is-panning');
      clearHover();
    }
    const scale = figureWidth / canvas.getBoundingClientRect().width / zoom;
    panX = drag.panX + dx * scale; panY = drag.panY + dy * scale;
    applyCamera();
  });
  function endDrag(event) {
    if (!drag || event.pointerId !== drag.id) return;
    suppressClick = drag.moved;
    drag = null;
    canvas.classList.remove('is-panning');
    if (canvas.hasPointerCapture(event.pointerId)) canvas.releasePointerCapture(event.pointerId);
  }
  canvas.addEventListener('pointerup', endDrag);
  canvas.addEventListener('pointercancel', endDrag);
  canvas.addEventListener('pointerleave', () => {if (drag && !drag.moved) drag = null;});
  canvas.addEventListener('click', (event) => {
    if (!suppressClick) return;
    event.preventDefault(); event.stopPropagation(); suppressClick = false;
  }, true);
  canvas.addEventListener('keydown', (event) => {
    if (event.key === '+' || event.key === '=') changeZoom(zoom * 1.5);
    else if (event.key === '-') changeZoom(zoom / 1.5);
    else if (event.key === '0') {panX = 0; panY = 0; changeZoom(1);}
    else if (zoom > 1 && ['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(event.key)) {
      const step = 50 / zoom;
      panX += event.key === 'ArrowLeft' ? step : event.key === 'ArrowRight' ? -step : 0;
      panY += event.key === 'ArrowUp' ? step : event.key === 'ArrowDown' ? -step : 0;
      applyCamera();
    } else return;
    event.preventDefault();
  });
  function draw() {
    if (panel.hidden || !currentFocus) return;
    const node = visual(currentFocus);
    effectiveMeasure = measure;
    if (measure !== 'studios' && !node.stats[effectiveMeasure]) effectiveMeasure = node.stats.tasks ? 'tasks' : node.stats.jobs ? 'jobs' : 'blocks';
    currentFocus.weight = node.stats[effectiveMeasure];
    weights(node);
    const width = Math.max(280, Math.floor(canvas.getBoundingClientRect().width));
    const records = nameRecords(node);
    const outsideNames = namePlacement === 'outside' && width >= 1000 && records.length > 0 && records.length <= 30;
    const labelWidth = outsideNames ? Math.min(260, Math.max(190, width * .19)) : 0;
    const radius = Math.min(width / 2 - (outsideNames ? labelWidth + 48 : 18), 600);
    const hole = Math.max(42, Math.min(76, radius * .24));
    const layers = Math.max(1, depth(node));
    const step = (radius - hole) / layers;
    let height = radius * 2 + 24;
    figureWidth = width; figureHeight = height;
    const figure = svg('svg', {viewBox: `0 0 ${width} ${height}`, width, height, role: 'img',
      'aria-label': `${node.name} hierarchy chart, sized by ${effectiveMeasure} count. The list below supports keyboard navigation.`});
    const group = svg('g', {transform: `translate(${width / 2},${height / 2})`});
    const layerNames = new Map();
    const projectBorders = [];
    const nameSpans = [];
    let marks = 0;
    function partition(parent, start, end, level) {
      let angle = start;
      parent.children.forEach((child) => {
        if (!child.weight || !parent.weight) return;
        const next = angle + (end - start) * child.weight / parent.weight;
        const span = next - angle;
        const gap = Math.min(.005, span * .04);
        const inner = hole + level * step + 1;
        const outer = hole + (level + 1) * step - 1;
        const mark = svg('path', {d: ringPath(angle + gap, next - gap, inner, outer),
          class: 'chart-arc ' + colorClass(child), 'data-chart-node': child.id});
        if (tone(child)) mark.style.fill = tone(child);
        const p = progress(child);
        mark.append(svg('title', {}, child.name + '\n' + displayLevel(child) + ' · ' + summaryLine(child) +
          '\nShare of current scope ' + pct(child.weight, node.weight) + (child.level === 'Studio' ? '' : '\n' + p.source + ' completion ' + pct(p.done, p.total)) +
          (recordedStatus(child) ? '\n' + recordedStatus(child) : '')));
        mark.addEventListener('pointerenter', (event) => {
          if (event.pointerType === 'mouse' && !touchDetails() && !inspector.open) hover(child);
        });
        mark.addEventListener('pointerleave', clearHover);
        mark.addEventListener('click', (event) => activateNode(child, event));
        if (isProjectGroup(child)) {
          projectBorders.push({id: child.id, start: angle, end: next, inner});
        }
        if (outsideNames && records.some((record) => record.id === child.id)) {
          nameSpans.push({node: child, start: angle, end: next});
        }
        group.append(mark);
        marks++;
        const ring = layerNames.get(level) || new Set(); ring.add(displayLevel(child)); layerNames.set(level, ring);
        const middle = (inner + outer) / 2;
        const available = middle * span;
        const labelSpace = child.level === 'Scene' ? Math.max(52, themeName(child).length * 8) : 52;
        if (isProjectGroup(child) && !outsideNames) {
          projectName(group, child, angle + gap, next - gap, inner, outer, marks);
        } else if (available > labelSpace && step >= 16 && width >= 430 && !(outsideNames && isProjectGroup(child))) {
          const short = (child.level === 'Block' || child.level === 'Task' || child.level === 'Job') ? child.folder : child.name;
          const max = Math.floor(available / 6.5);
          const name = child.level === 'Scene' ? themeName(child) : short.length > max ? short.slice(0, Math.max(4, max - 1)) + '…' : short;
          const middleAngle = (angle + next) / 2;
          const [x, y] = point(middle, middleAngle);
          const rotate = middleAngle * 180 / Math.PI + (middleAngle > Math.PI / 2 && middleAngle < Math.PI * 1.5 ? 180 : 0);
          group.append(svg('text', {x, y, transform: `rotate(${rotate},${x},${y})`,
            class: 'chart-arc-label' + (['Project', 'Folder', 'Scene'].includes(child.level) ? ' chart-important-label' : ''),
            'text-anchor': 'middle', 'dominant-baseline': 'middle'}, name));
        }
        partition(child, angle, next, level + 1);
        angle = next;
      });
    }
    partition(node, 0, Math.PI * 2, 0);
    if (isProjectGroup(node) && node.weight) {
      projectBorders.push({id: node.id, start: 0, end: Math.PI * 2, inner: hole});
    }
    // Project outlines continue through their descendants without taking clicks.
    const borders = svg('g', {class: 'chart-project-borders', 'aria-hidden': 'true'});
    projectBorders.forEach((border) => {
      const span = border.end - border.start;
      const stroke = Math.max(.4, Math.min(3.5, border.inner * span * .3));
      const path = ringPath(border.start, border.end, border.inner, radius + 1);
      borders.append(svg('path', {d: path, class: 'chart-project-halo', 'stroke-width': stroke + 1}));
      borders.append(svg('path', {d: path, class: 'chart-project-border', 'stroke-width': Math.max(.4, stroke * .38),
        'data-project-boundary': border.id}));
    });
    group.append(borders);
    const center = svg('g', {class: 'chart-center'});
    center.append(svg('circle', {r: hole - 3}));
    const p = progress(node);
    center.append(svg('text', {y: -14, 'text-anchor': 'middle', class: 'chart-center-caption'}, measure === 'studios' ? 'Studio topics' : p.source + ' completion'));
    center.append(svg('text', {y: 13, 'text-anchor': 'middle', class: 'chart-center-rate'}, measure === 'studios' ? number(node.stats.studios) : pct(p.done, p.total)));
    center.append(svg('text', {y: 34, 'text-anchor': 'middle', class: 'chart-center-back'}, node.id === 'space' ? 'SPACE' : '↖ Back'));
    center.addEventListener('click', () => selectFocus(byId.get(node.id).parentId || 'space'));
    group.append(center);
    if (outsideNames) {
      height = drawNames(group, nameSpans, radius, labelWidth, height);
      figureHeight = height;
      figure.setAttribute('height', height);
      group.setAttribute('transform', `translate(${width / 2},${height / 2})`);
    }
    figure.append(group);
    if (!marks) figure.append(svg('text', {x: width / 2, y: height / 2 + hole + 32, 'text-anchor': 'middle', class: 'chart-empty'},
      measure === 'studios' && !node.stats.studios ? 'No Block Studio topics in this scope' : measure !== 'studios' && !showTasks && node.stats.tasks && !node.emptyMatch ? 'Task layer is hidden; enable Show Task layer to explore' : node.children.length || node.emptyMatch ? 'No items match the current filters' : 'No deeper levels in this scope; see the details panel'));
    canvas.replaceChildren(figure);
    applyCamera();
    $('chart-hover').textContent = interactionHint();
    const names = [...layerNames.values()].map((levels) => [...levels].join('/')).join(' → ');
    const metricNames = {tasks: 'Task', blocks: 'Block', jobs: 'Job', studios: 'Studio topic'};
    const fallback = effectiveMeasure === measure ? '' : `No ${metricNames[measure]} items in this scope; using ${metricNames[effectiveMeasure]} count. `;
    const metricLabel = metricNames[effectiveMeasure];
    $('chart-area-note').textContent = `Area: ${metricLabel} count. ${fallback}` +
      (measure !== 'studios' && !showTasks ? 'Task segments are hidden; completion still counts all Tasks in this scope. ' : '') +
      (includeArchived ? 'Legacy Blocks are included. ' : 'Legacy Blocks are excluded. ') + (names ? 'Inner to outer: ' + names + '. ' : '') +
      (effectiveMeasure === 'tasks' ? 'Blocks without Tasks can be selected using the filters or list. ' : effectiveMeasure === 'studios' ? 'Blocks with no Studio topics remain in the filters and list. ' : 'Each ' + metricLabel + ' shares its area among its descendants. ') +
      'Project and folder outlines continue through the outer rings. ' + (measure === 'studios' ?
        'One segment per sNN folder in a Block’s studio/. Gray Studio topics have no completion score; parent colors still show work completion.' :
        'Inner rings blend from light blue to green by completion; leaf colors show status.');
    selection();
    setNameKey(node, records, outsideNames);
    if (inspector.open && previewNode) {
      canvas.querySelectorAll('[data-chart-node]').forEach((mark) =>
        mark.classList.toggle('is-inspected', mark.dataset.chartNode === previewNode.id));
      hover(previewNode);
    }
  }
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
