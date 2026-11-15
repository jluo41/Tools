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
