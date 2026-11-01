(() => {
  const root = document.querySelector('.labeling-focus');
  if (!root) return;
  function unifyPrompts() {
    root.querySelectorAll('.items-step').forEach(step => {
      const row = step.querySelector('.sign-row');
      const box = step.querySelector('.run-prompt-box');
      const sign = row?.querySelector('button[data-post]');
      const name = row?.querySelector('input[name="by"]');
      const copy = box?.querySelector('.run-copy');
      const notes = box?.querySelector('textarea.run-notes');
      const preview = box?.querySelector('.run-prompt');
      if (!sign || !name || !copy || !notes || !preview || box.dataset.unified) return;
      box.dataset.unified = 'true'; box.classList.add('lf-compose');
      const endpoint = sign.dataset.post, payload = JSON.parse(sign.dataset.body);
      const base = copy.dataset.copy, verb = sign.textContent.trim();
      const form = document.createElement('form');
      const nameLabel = document.createElement('label'); nameLabel.textContent = 'Your name';
      name.required = true; name.maxLength = 80; name.autocomplete = 'name'; name.placeholder = 'Name recorded with this confirmation';
      nameLabel.append(name);
      const notesLabel = document.createElement('label'); notesLabel.textContent = 'Comments (optional)';
      notes.placeholder = 'Add context or instructions for the agent'; notesLabel.append(notes);
      const explanation = document.createElement('p'); explanation.className = 'lf-compose-help';
      explanation.textContent = 'Confirm the proposal shown above and copy the request. The agent runs it after you send the request.';
      const previewLabel = document.createElement('div'); previewLabel.className = 'lf-compose-help'; previewLabel.textContent = 'Request preview';
      const submit = document.createElement('button'); submit.type = 'submit'; submit.textContent = verb + ' & copy prompt';
      const message = document.createElement('p'); message.setAttribute('role','status');
      const heading = document.createElement('h3'); heading.textContent = 'Prompt';
      row.remove(); box.replaceChildren(heading, form);
      form.append(nameLabel, notesLabel, previewLabel, preview, explanation, submit, message);
      let saved = false, busy = false, confirmedRequest = '';
      function requestText() {
        const person = name.value.trim().replace(/\s+/g,' ');
        return base + '\nhuman name: ' + (person || '[your name]') + (notes.value.trim() ? '\nuser feedback: ' + notes.value.trim() : '');
      }
      function updatePreview() { if (!saved) preview.textContent = requestText(); }
      name.addEventListener('input', updatePreview); notes.addEventListener('input', updatePreview); updatePreview();
      async function copyText(text) {
        try { if (navigator.clipboard?.writeText) { await navigator.clipboard.writeText(text); return true; } } catch (_) {}
        const t = document.createElement('textarea'); t.value = text; t.style.position = 'fixed'; t.style.opacity = '0';
        document.body.append(t); t.select(); let ok = false;
        try { ok = document.execCommand('copy'); } catch (_) {} t.remove(); return ok;
      }
      form.addEventListener('submit', async e => {
        e.preventDefault(); if (busy) return;
        if (!name.value.trim()) { name.setCustomValidity('Enter your name.'); name.reportValidity(); return; }
        name.setCustomValidity(''); busy = true; submit.disabled = true;
        try {
          if (!saved) {
            message.textContent = 'Recording your confirmation…';
            const person = name.value.trim().replace(/\s+/g,' ');
            const request = requestText();
            let response;
            try { response = await fetch(endpoint, {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({...payload,by:person})}); }
            catch (_) { throw new Error('Confirmation status is unknown. Reload this page to check the record before trying again.'); }
            let result;
            try { result = await response.json(); }
            catch (_) { throw new Error('Confirmation status is unknown. Reload this page to check the record before trying again.'); }
            if (!response.ok || !result.ok) { const error = new Error(result.err || 'Confirmation was refused.'); error.refused = true; throw error; }
            saved = true; confirmedRequest = request; name.disabled = true; notes.disabled = true;
            try { localStorage.setItem('sign:by',person); } catch (_) {}
            preview.textContent = confirmedRequest;
            step.querySelectorAll('.st').forEach(el => { if (el.textContent.includes('sign')) el.textContent = '✓ confirmed'; });
          }
          const copied = await copyText(confirmedRequest);
          message.textContent = copied ? 'Confirmation saved. Prompt copied. Paste it into your agent conversation to continue.' : 'Confirmation saved. Copy the request preview above, or try Copy prompt again. Nothing has been run.';
          submit.textContent = 'Copy prompt again'; submit.disabled = false;
        } catch (error) {
          message.textContent = error.message;
          submit.disabled = !error.refused;
        } finally { busy = false; }
      });
      name.addEventListener('input', () => name.setCustomValidity(''));
    });
  }

  function paginate() {
    root.querySelectorAll('table:not([data-paged])').forEach(table => {
      table.dataset.paged = 'true';
      const rows = [...table.querySelectorAll(':scope > tbody > tr')];
      if (rows.length <= 20) return;
      let page = 0;
      const bar = document.createElement('div'); bar.className = 'lf-pagination';
      const back = document.createElement('button'), next = document.createElement('button'), label = document.createElement('span');
      back.type = next.type = 'button'; back.textContent = 'Previous'; next.textContent = 'Next';
      label.setAttribute('role','status');
      function show() {
        rows.forEach((r,i) => { r.hidden = i < page*20 || i >= (page+1)*20; });
        label.textContent = `${page*20+1}–${Math.min((page+1)*20,rows.length)} of ${rows.length}`;
        back.disabled = page === 0; next.disabled = (page+1)*20 >= rows.length;
      }
      back.onclick=()=>{page--;show();}; next.onclick=()=>{page++;show();};
      bar.append(back,label,next); table.before(bar); show();
    });
  }
  // Samples fetched by the existing read route use the same steady content style.
  function flatten() {
    root.querySelectorAll('details').forEach(d => {
      const section = document.createElement('section');
      [...d.attributes].forEach(a => { if (a.name !== 'open') section.setAttribute(a.name, a.value); });
      section.dataset.staticContent = 'true';
      const heading = d.querySelector(':scope > summary');
      if (heading) {
        const h = document.createElement('div'); h.setAttribute('role', 'heading'); h.setAttribute('aria-level', '3');
        h.append(...heading.childNodes); heading.replaceWith(h);
      }
      section.append(...d.childNodes); d.replaceWith(section);
    });
  }
  function focusLinks() {
    const tabs = {'1 · Data':'data','2 · Items':'items','3 · Embedding':'embedding'};
    root.querySelectorAll('a[href]').forEach(a => {
      const url = new URL(a.href, location.href);
      if (url.origin !== location.origin || url.pathname !== '/_board/workbench') return;
      const section = tabs[url.searchParams.get('sub')];
      if (!section) return;
      url.searchParams.set('layout','focus'); url.searchParams.set('section',section);
      url.searchParams.delete('space'); url.searchParams.delete('sub'); a.href = url.href;
    });
  }
  flatten(); unifyPrompts(); paginate(); focusLinks();
  new MutationObserver(() => { flatten(); unifyPrompts(); paginate(); focusLinks(); }).observe(root, {childList:true, subtree:true});
  window.addEventListener('message', e => {
    const iframe = root.querySelector('.lf-engine');
    if (!iframe || e.origin !== location.origin || e.source !== iframe.contentWindow) return;
    if (e.data?.type === 'labeling-focus:height' && Number.isFinite(e.data.height)) {
      iframe.style.height = Math.max(300, Math.min(60000, e.data.height)) + 'px';
    }
  });
})();
