/* Draft edits update the paragraph read-through without navigating away. */
(function () {
  var evidencePattern = /\[(E\d+-(VALUE|CITE|DISPLAY)-[a-z0-9]+(?:-[a-z0-9]+)*)(?:(?::|\s+)[^\]]*)?\]/gi;
  function cleanProse(text) {
    return text.replace(/\\cite\w*\*?(?:\[[^\]]*\])*\{[^}]*\}/g, '')
      .replace(/\s+/g, ' ').replace(/\s+([.,;:!?])/g, '$1').trim();
  }
  function escapeHTML(text) {
    return text.replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
  }
  function fallbackLabel(id, type) {
    var number = (id.match(/^E0*(\d+)/) || [null, id])[1];
    var shortType = {VALUE: 'V', CITE: 'C', DISPLAY: 'D'}[type.toUpperCase()] || type[0].toUpperCase();
    var words = id.split('-').slice(2);
    var name = words.map(function (word) {
      return word ? word[0].toUpperCase() + word.slice(1) : '';
    }).join('').slice(0, 12) || 'Item';
    return 'E' + number + shortType + '.' + name;
  }
  function evidenceItems(area) {
    var items = {};
    try { items = JSON.parse(area.dataset.evidenceItems || '{}'); }
    catch (_) {}
    // A long-running Board server may have rendered the textarea before this
    // data attribute existed. Its adjacent Evidence chips still carry the
    // authoritative short labels, and this script is loaded fresh per request.
    document.querySelectorAll('.typed-ev').forEach(function (chip) {
      var id = (chip.title || '').split(' · ')[0];
      if (!id || items[id]) return;
      items[id] = {
        label: chip.textContent,
        status: chip.classList.contains('ok') ? 'ready' :
          (chip.classList.contains('mut') ? 'deferred' : 'specified'),
      };
    });
    return items;
  }
  function readerHTML(text, area) {
    var prose = cleanProse(text);
    var items = evidenceItems(area);
    var output = '', cursor = 0, match;
    evidencePattern.lastIndex = 0;
    while ((match = evidencePattern.exec(prose)) !== null) {
      var item = items[match[1]] || {};
      output += escapeHTML(prose.slice(cursor, match.index));
      output += '(' + escapeHTML(item.label || fallbackLabel(match[1], match[2])) + ')';
      cursor = match.index + match[0].length;
    }
    return output + escapeHTML(prose.slice(cursor));
  }
  function readParagraph(group) {
    var output = group.querySelector('[data-paragraph-reading]');
    if (!output) return;
    var text = [];
    group.querySelectorAll('.preview-form textarea').forEach(function (area) {
      if (area.value.trim()) text.push(readerHTML(area.value, area));
      else if (!area.dataset.shared) text.push(escapeHTML('[' + area.form.elements.address.value + ' draft missing]'));
    });
    output.innerHTML = text.join(' ') || 'Write a candidate sentence to preview this paragraph.';
  }
  document.querySelectorAll('.paragraph-group').forEach(readParagraph);
  document.querySelectorAll('form[data-preview-write]').forEach(function (form) {
    var area = form.querySelector('textarea');
    form._savedText = area.value;
    form._savedShared = area.dataset.shared || '';
    showCopy(form);
  });
  function showCopy(form) {
    var area = form.querySelector('textarea');
    var copy = form.closest('.preview-editor').querySelector('.preview-copy');
    copy.innerHTML = readerHTML(area.value, area) || escapeHTML(area.dataset.shared ? 'See ' + area.dataset.shared : 'Write a sentence…');
    copy.classList.toggle('preview-placeholder', !area.value);
  }
  document.addEventListener('click', function (event) {
    var cancel = event.target.closest('[data-preview-cancel]');
    if (!cancel) return;
    var form = cancel.closest('form');
    if (form.dataset.saving === 'true') return;
    var area = form.querySelector('textarea');
    area.value = form._savedText;
    area.dataset.shared = form._savedShared;
    delete form.dataset.dirty;
    form.querySelector('.preview-status').textContent = '';
    form.closest('.preview-editor').open = false;
    showCopy(form);
    readParagraph(form.closest('.paragraph-group'));
  });
  document.addEventListener('input', function (event) {
    var form = event.target.closest('form[data-preview-write]');
    if (!form) return;
    form.dataset.dirty = 'true';
    delete event.target.dataset.shared;
    form.querySelector('.preview-status').textContent = 'Unsaved';
    readParagraph(form.closest('.paragraph-group'));
  });
  window.addEventListener('beforeunload', function (event) {
    if (document.querySelector('.preview-form[data-dirty="true"]')) {
      event.preventDefault();
      event.returnValue = '';
    }
  });
  document.addEventListener('submit', async function (event) {
    var form = event.target.closest('form[data-preview-write]');
    if (!form) return;
    event.preventDefault();
    if (form.dataset.saving === 'true') return;
    var payload = Object.fromEntries(new FormData(form));
    var status = form.querySelector('.preview-status');
    var button = form.querySelector('button[type=submit]');
    form.dataset.saving = 'true';
    button.disabled = true;
    status.textContent = 'Saving…';
    try {
      var response = await fetch('/_board/outline', {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
      });
      var result = await response.json();
      if (!response.ok || !result.ok) throw new Error(result.err || 'Save failed');
      form.elements.expected_record.value = result.record_token;
      form._savedText = result.text;
      form._savedShared = '';
      var stale = form.closest('.point-preview').querySelector('.preview-stale');
      if (stale) stale.remove();
      var area = form.querySelector('textarea');
      // Typing while a save is in flight must never be overwritten.
      if (area.value === payload.text) {
        area.value = result.text;
        delete form.dataset.dirty;
        status.textContent = 'Saved';
        delete area.dataset.shared;
        showCopy(form);
        form.closest('.preview-editor').open = false;
      } else {
        status.textContent = 'Earlier edit saved · new changes unsaved';
      }
      form.parentElement.querySelector('.preview-state').textContent = 'Draft for discussion';
      readParagraph(form.closest('.paragraph-group'));
    } catch (error) {
      status.textContent = 'Not saved: ' + error.message;
      form.dataset.dirty = 'true';
    } finally {
      delete form.dataset.saving;
      button.disabled = false;
    }
  });
})();
