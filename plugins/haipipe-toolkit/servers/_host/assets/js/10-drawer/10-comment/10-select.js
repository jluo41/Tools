  /* Copy a selected passage, without opening a writer or sending a request. */
  var selectedPrompt = '';
  function hideSelectionCopy() {
    btn.style.display = 'none';
    selectedPrompt = '';
  }
  function offerSelectionCopy() {
    var active = document.activeElement;
    if (active === btn || (active && active.matches('[data-copy-buffer]'))) return;
    var selection = window.getSelection();
    if (!selection || selection.isCollapsed || !selection.rangeCount) {
      hideSelectionCopy(); return;
    }
    var range = selection.getRangeAt(0);
    function element(node) { return node.nodeType === 1 ? node : node.parentElement; }
    var start = element(range.startContainer), end = element(range.endContainer);
    var sec = start && start.closest('section.slide.q');
    if (!sec || !end || end.closest('section.slide.q') !== sec ||
        start.closest('input,textarea,button,.hpath,.schatbar') ||
        end.closest('input,textarea,button,.hpath,.schatbar')) {
      hideSelectionCopy(); return;
    }
    var excerpt = document.createElement('div');
    excerpt.appendChild(range.cloneContents());
    var text = window.__boardReadableText(excerpt);
    if (!text) { hideSelectionCopy(); return; }
    var p = start.closest('p');
    var address = (p && p.dataset.sentenceRef) || sec.id + ' / selected passage';
    var sentence = containingSentence(range);
    selectedPrompt = window.__boardPromptText(sec, address, text,
      sentence && sentence !== text ? sentence : '');
    var rect = range.getBoundingClientRect();
    btn.style.display = 'block';
    btn.style.left = (window.scrollX + Math.max(8,
      Math.min(rect.left, window.innerWidth - btn.offsetWidth - 8))) + 'px';
    btn.style.top = (window.scrollY + Math.max(8,
      Math.min(rect.bottom + 7, window.innerHeight - btn.offsetHeight - 8))) + 'px';
  }
  document.addEventListener('selectionchange', offerSelectionCopy);
  document.addEventListener('pointerup', function () { setTimeout(offerSelectionCopy, 0); });
  btn.addEventListener('mousedown', function (e) { e.preventDefault(); });
  btn.onclick = function () {
    if (selectedPrompt) window.__boardCopyPrompt(btn, selectedPrompt);
  };
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') hideSelectionCopy();
  });
  window.addEventListener('board:updated', hideSelectionCopy);
