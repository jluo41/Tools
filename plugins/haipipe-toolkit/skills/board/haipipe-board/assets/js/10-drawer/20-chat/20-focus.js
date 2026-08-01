  /* One focus card, two kinds of focus (QB5d): a SENTENCE, or a HEADING — a
     `##` section or a `###` subsection. Same card, same session, same clear
     button; only the packet's wording and the placeholder differ. */
  function setSentenceFocus(ref, sentence, attached, contentPath, kind) {
    sentenceFocus = { ref: ref, sentence: sentence, attached: attached || '',
                      contentPath: contentPath || '', kind: kind || 'sentence' };
    var box = chat.querySelector('.sfocus');
    box.hidden = false;
    box.querySelector('.sfref').textContent = ref;
    box.querySelector('.sfpath').textContent = contentPath || '';
    box.querySelector('.sfpath').hidden = !contentPath;
    box.querySelector('.sfquote').textContent = sentence;
    var details = box.querySelector('.sfattached');
    var rows = (attached || '').split(/\n+/).filter(function (x) { return x.trim(); });
    details.hidden = !rows.length;
    details.open = false;
    details.querySelector('summary').textContent =
      'Attached · ' + rows.length;
    details.querySelector('pre').textContent = attached || '';
    chat.querySelector('textarea').placeholder =
      sentenceFocus.kind === 'heading' ? 'Ask about this section…'
                                       : 'Ask about this sentence…';
  }
  function focusedMessage(message) {
    if (!sentenceFocus) return message;
    if (sentenceFocus.kind === 'heading') {
      return 'Focus this turn on ' + sentenceFocus.ref + '.\n\n' +
        (sentenceFocus.contentPath
          ? 'Markdown source:\n' + sentenceFocus.contentPath + '\n\n' : '') +
        'What is visible under that heading:\n' + sentenceFocus.sentence +
        '\n\nUser message:\n' + message +
        '\n\nDiscuss this section specifically. Read the rest of the page when ' +
        'needed, but keep this section as the explicit focus.';
    }
    return 'Focus this turn on sentence ' + sentenceFocus.ref + '.\n\n' +
      (sentenceFocus.contentPath
        ? 'Content location:\n' + sentenceFocus.contentPath + '\n\n' : '') +
      'Sentence:\n' + sentenceFocus.sentence +
      (sentenceFocus.attached
        ? '\n\nAttached directly beneath it:\n' + sentenceFocus.attached : '') +
      '\n\nUser message:\n' + message +
      '\n\nDiscuss this sentence specifically. Read the rest of the page when needed, ' +
      'but keep this sentence as the explicit focus.';
  }
  chat.querySelector('.sfclear').onclick = clearSentenceFocus;

  function chatLoad(id) {
    try { return JSON.parse(localStorage.getItem(CHATK(id)) || '[]'); } catch (e) { return []; }
  }
  function chatSave(id, log) { localStorage.setItem(CHATK(id), JSON.stringify(log)); }
