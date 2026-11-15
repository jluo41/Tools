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
