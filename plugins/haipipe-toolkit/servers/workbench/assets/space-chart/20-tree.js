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
