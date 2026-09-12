/* One sentence-targeted comment composer below each paragraph; no agent launch. */
(function () {
  function preview(form) {
    var address = form.elements.address.value;
    return Array.from(form.closest('.paragraph-group').querySelectorAll('form[data-preview-write]'))
      .find(function (draft) { return draft.elements.address.value === address; });
  }
  function freshId() {
    // getRandomValues is available on the trusted HTTP/Tailscale origin too.
    var bytes = crypto.getRandomValues(new Uint8Array(16));
    return 'PC' + Array.from(bytes, function (b) { return b.toString(16).padStart(2, '0'); }).join('');
  }
  function selectSentence(form) {
    var draft = preview(form), quote = form.querySelector('[data-comment-quote]');
    quote.textContent = draft ? (draft._savedText || '') : '';
    quote.hidden = !quote.textContent;
    form._anchor = draft ? {
      address: draft.elements.address.value,
      expected_bullet: draft.elements.expected_bullet.value,
      expected_record: draft.elements.expected_record.value
    } : null;
  }
  document.querySelectorAll('form[data-preview-comment]').forEach(function (form) {
    form.elements.address.addEventListener('focus', function () {
      var drafts = form.closest('.paragraph-group').querySelectorAll('form[data-preview-write]');
      Array.from(form.elements.address.options).forEach(function (option) {
        var draft = Array.from(drafts).find(function (d) { return d.elements.address.value === option.value; });
        if (!draft) return;
        var text = draft._savedText || '';
        option.disabled = !text || draft.elements.expected_record.value === 'missing';
        option.textContent = option.value + ' · ' + (text ? text.slice(0, 100) : 'No saved draft yet');
      });
    });
    form.addEventListener('change', function (event) {
      if (event.target === form.elements.address) {
        selectSentence(form);
        // A new target after a submitted attempt is a different comment.
        form._attempt = null;
      }
    });
    form.addEventListener('input', function () { form.dataset.dirty = 'true'; });
    form.addEventListener('submit', async function (event) {
      event.preventDefault();
      if (form.dataset.saving === 'true') return;
      var status = form.querySelector('[data-comment-status]');
      var draft = preview(form);
      if (!draft || !form._anchor) { status.textContent = 'Choose a sentence first.'; return; }
      if (draft.dataset.dirty === 'true') {
        status.textContent = 'Save or cancel the sentence edit before commenting.'; return;
      }
      if (draft.elements.expected_record.value !== form._anchor.expected_record) {
        selectSentence(form);
        status.textContent = 'Sentence changed. Review the updated quote, then save again.'; return;
      }
      var payload = Object.assign(Object.fromEntries(new FormData(form)), form._anchor, {action: 'comment-preview'});
      var signature = JSON.stringify([payload.address, payload.author, payload.comment]);
      if (!form._attempt || form._attempt.signature !== signature) {
        form._attempt = {signature: signature, id: freshId()};
      }
      payload.comment_id = form._attempt.id;
      var button = form.querySelector('button[type=submit]');
      button.disabled = true;
      form.dataset.saving = 'true';
      status.textContent = 'Saving…';
      try {
        var response = await fetch('/_board/outline', {
          method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload)
        });
        var result = await response.json();
        if (!response.ok || !result.ok) throw new Error(result.err || 'Save failed');
        var panel = form.closest('.paragraph-comments');
        panel.querySelector('[data-comment-list]').innerHTML = result.comments_html;
        panel.querySelector('[data-comment-count]').textContent = result.summary;
        // Do not erase a second comment typed while the first save was in flight.
        if (form.elements.comment.value === payload.comment && form.elements.address.value === payload.address &&
            form.elements.author.value === payload.author) {
          form.elements.comment.value = '';
          delete form.dataset.dirty;
          form._attempt = null;
          status.textContent = 'Saved. Ask your agent to apply comments.';
        } else {
          status.textContent = 'Earlier comment saved · new changes unsaved';
        }
      } catch (error) {
        status.textContent = 'Not saved: ' + error.message;
        form.dataset.dirty = 'true';
      } finally {
        delete form.dataset.saving;
        button.disabled = false;
      }
    });
  });
  window.addEventListener('beforeunload', function (event) {
    if (document.querySelector('form[data-preview-comment][data-dirty="true"]')) {
      event.preventDefault(); event.returnValue = '';
    }
  });
})();
