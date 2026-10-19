/* Standalone Page source editor; no Board, agent, or terminal dependencies. */
(() => {
  'use strict';
  function init() {
    const file = document.getElementById('source-file');
    const text = document.getElementById('source-text');
    const save = document.getElementById('save-source');
    const status = document.getElementById('editor-status');
    if (!file || !text || !save || !status) return;
    status.setAttribute('role', 'status');
    status.setAttribute('aria-live', 'polite');
    const live = document.body.dataset.live === 'true' && /^https?:$/.test(location.protocol);
    const readOnly = document.body.dataset.readOnly === 'true';
    let current = '', hash = '', original = text.value, busy = false;
    const dirty = () => text.value !== original;
    const message = (value, error = false) => {
      status.textContent = value;
      status.dataset.error = String(error);
    };
    function controls() {
      file.disabled = !live || busy;
      text.readOnly = !live || readOnly || busy || !hash;
      save.disabled = !live || readOnly || busy || !hash || !dirty();
    }
    async function request(url, options = {}) {
      const response = await fetch(url, {credentials: 'same-origin', cache: 'no-store', ...options});
      let data;
      try { data = await response.json(); }
      catch (_) { throw new Error('The server returned an unreadable response. Your text is preserved.'); }
      if (!response.ok || data.ok === false) {
        if (response.status === 409) throw new Error('The file changed on disk. Your edits are preserved here; copy them before reloading.');
        if (response.status === 401) throw new Error('Login required. Open the server startup URL, then return to this editor.');
        throw new Error(data.err || `Request failed (${response.status}).`);
      }
      return data;
    }
    async function load() {
      const selected = file.value;
      if (dirty() && !window.confirm('Discard unsaved edits and open another file?')) {
        file.value = current;
        return;
      }
      busy = true;
      controls();
      message('Loading source…');
      try {
        const data = await request('/_page/source?file=' + encodeURIComponent(selected));
        current = selected;
        hash = data.sha256;
        text.value = original = data.text;
        message(readOnly ? 'Read-only server.' : 'Source loaded.');
      } catch (error) {
        file.value = current || selected;
        message(error.message, true);
      } finally { busy = false; controls(); }
    }
    async function write() {
      if (save.disabled) return;
      busy = true;
      controls();
      message('Saving…');
      try {
        const sent = text.value;
        const data = await request('/_page/source', {
          method: 'POST', headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({file: current, text: sent, sha256: hash})
        });
        hash = data.sha256;
        original = sent;
        message('Saved. Reload the Page to refresh its rendered view.');
      } catch (error) { message(error.message, true); }
      finally { busy = false; controls(); }
    }
    file.addEventListener('change', load);
    save.addEventListener('click', event => { event.preventDefault(); write(); });
    text.addEventListener('input', () => { controls(); message(dirty() ? 'Unsaved edits.' : 'No unsaved edits.'); });
    text.addEventListener('keydown', event => {
      if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 's') {
        event.preventDefault(); write();
      }
    });
    window.addEventListener('beforeunload', event => {
      if (dirty()) { event.preventDefault(); event.returnValue = ''; }
    });
    controls();
    if (!live) message('Static build. Start the Page server to load and edit source.');
    else if (file.options.length) load();
    else message('No editable source files.');
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
