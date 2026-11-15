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
