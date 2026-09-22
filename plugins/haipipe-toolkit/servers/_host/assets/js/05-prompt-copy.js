/* The Page is a reading surface. Copying context never writes or submits it. */
(function () {
  'use strict';
  window.__boardReadableText = function (el) {
    var c = el.cloneNode(true);
    c.querySelectorAll('button.chip.card.span').forEach(function (b) {
      b.replaceWith(document.createTextNode(b.textContent));
    });
    c.querySelectorAll('.hpath,.schatbar,.caddr,.haddr,.cmk,.sbz,.sbadge,.cv,' +
      '.sadd,.sedit,.saddrow,.dadd,.chcopy,button,input,select,textarea')
      .forEach(function (x) { x.remove(); });
    c.removeAttribute('id');
    c.querySelectorAll('[id]').forEach(function (x) { x.removeAttribute('id'); });
    if (c.tagName === 'DETAILS') c.open = true;
    c.querySelectorAll('details').forEach(function (d) { d.open = true; });
    c.style.cssText = 'position:fixed;left:-99999px;top:0;width:800px';
    document.body.appendChild(c);
    var text = c.innerText.replace(/\n{3,}/g, '\n\n').trim();
    c.remove();
    return text;
  };

  window.__boardPromptText = function (sec, address, passage, context) {
    var board = boardPath();
    try { board = decodeURIComponent(board); } catch (e) {}
    var lines = [
      'Page: ' + sec.id + (sec.dataset.title ? ' · ' + sec.dataset.title : ''),
      'Board source: ' + board,
      'Page source (relative to Board folder): ' + (sec.dataset.file || '(unavailable)'),
      'Location: ' + address,
      '', 'Quoted passage:',
      String(passage || '').trim().split('\n').map(function (s) { return '> ' + s; }).join('\n')
    ];
    if (context) lines.push('', 'Attached context:',
      String(context).trim().split('\n').map(function (s) { return '> ' + s; }).join('\n'));
    lines.push('', 'My request:', '');
    return lines.join('\n');
  };

  var status = document.createElement('div');
  status.className = 'prompt-copy-status';
  status.setAttribute('role', 'status');
  status.setAttribute('aria-live', 'polite');
  document.body.appendChild(status);

  window.__boardCopyPrompt = async function (button, text) {
    var copied = false;
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(text);
        copied = true;
      }
    } catch (e) { /* HTTP and denied clipboard permission use the fallback. */ }
    if (!copied) {
      var active = document.activeElement, selection = window.getSelection();
      var ranges = [];
      if (selection) for (var i = 0; i < selection.rangeCount; i++) {
        ranges.push(selection.getRangeAt(i).cloneRange());
      }
      var ta = document.createElement('textarea');
      ta.value = text;
      ta.readOnly = true;
      ta.setAttribute('data-copy-buffer', '');
      ta.style.cssText = 'position:fixed;left:-99999px;top:0';
      document.body.appendChild(ta);
      ta.select();
      try { copied = document.execCommand('copy'); } catch (e) {}
      ta.remove();
      if (active && active.isConnected) active.focus({ preventScroll: true });
      if (selection) {
        selection.removeAllRanges();
        ranges.forEach(function (range) { selection.addRange(range); });
      }
    }
    if (!button.dataset.copyLabel) button.dataset.copyLabel = button.textContent;
    clearTimeout(button._copyTimer);
    button.textContent = copied ? '✓' : '!';
    status.textContent = copied ? 'Prompt copied. Paste it into your agent conversation and add your request.'
      : 'Could not copy the prompt. Select the passage and copy it manually.';
    status.classList.add('on');
    clearTimeout(status._timer);
    status._timer = setTimeout(function () { status.classList.remove('on'); }, 4000);
    button._copyTimer = setTimeout(function () { button.textContent = button.dataset.copyLabel; }, 1200);
    return copied;
  };
})();
