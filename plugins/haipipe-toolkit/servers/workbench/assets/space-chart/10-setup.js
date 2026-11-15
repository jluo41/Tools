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

