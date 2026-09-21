  // Selection context only; old pending-comment storage is left untouched.
  function containingSentence(range) {
    function paragraph(node) {
      node = node && (node.nodeType === 1 ? node : node.parentElement);
      return node && node.closest && node.closest('p');
    }
    var start = paragraph(range.startContainer), end = paragraph(range.endContainer);
    if (!start || start !== end || start.closest('.sapp,.cmb,.cmt,.change')) return '';
    return window.__boardSentenceText ? window.__boardSentenceText(start)
      : start.textContent.replace(/\s+/g, ' ').trim();
  }
