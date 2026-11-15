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
