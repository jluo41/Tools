// Unit tests for the editor state machine (no browser or live writes).
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../live/outline_preview.js'), 'utf8');

function fixture() {
  const events = {};
  const copy = {innerHTML: 'Original.', classList: {toggle() {}}};
  const status = {textContent: ''};
  const state = {textContent: ''};
  const button = {disabled: false};
  const reading = {innerHTML: ''};
  const stale = {removed: false, remove() { this.removed = true; }};
  const editor = {open: false, querySelector: () => copy};
  const area = {value: 'Original.', dataset: {shared: 'C1.P1.B0', evidenceItems: '{}'}};
  const group = {
    querySelector: () => reading,
    querySelectorAll: () => [area],
  };
  const form = {
    dataset: {},
    elements: {address: {value: 'C1.P1.B1'}, expected_record: {value: 'missing'}},
    parentElement: {querySelector: () => state},
    querySelector: (selector) => ({
      'textarea': area, '.preview-status': status, 'button[type=submit]': button,
    })[selector],
    closest: (selector) => ({
      '.preview-editor': editor, '.paragraph-group': group,
      '.point-preview': {querySelector: () => stale},
    })[selector],
  };
  area.form = form;
  area.closest = () => form;
  const cancel = {closest: (s) => s === 'form' ? form : cancel};
  let complete;
  vm.runInNewContext(source, {
    document: {
      querySelectorAll: (s) => s === '.paragraph-group' ? [group] :
        (s === 'form[data-preview-write]' ? [form] : []),
      querySelector: () => form.dataset.dirty ? form : null,
      addEventListener: (name, fn) => { events[name] = fn; },
    },
    window: {addEventListener: (name, fn) => { events[name] = fn; }},
    FormData: function () { return [['text', area.value]]; },
    fetch: () => new Promise(resolve => { complete = resolve; }),
  });
  return {
    form, area, editor, copy, status, reading, stale,
    type(text) { area.value = text; events.input({target: area}); },
    cancel() { events.click({target: cancel}); },
    save() { return events.submit({target: area, preventDefault() {}}); },
    respond(text, ok = true) {
      complete({ok, json: async () => ({ok, text, record_token: 'new', err: 'stale'})});
    },
  };
}

test('cancel restores seeded prose, shared address, and read-through', () => {
  const f = fixture();
  f.editor.open = true;
  f.type('Unsaved.');
  f.cancel();
  assert.equal(f.area.value, 'Original.');
  assert.equal(f.area.dataset.shared, 'C1.P1.B0');
  assert.equal(f.editor.open, false);
  assert.equal(f.form.dataset.dirty, undefined);
  assert.equal(f.reading.innerHTML, 'Original.');
});

test('save returns to readable text; later cancel restores last save', async () => {
  const f = fixture();
  f.editor.open = true;
  f.type('Candidate.');
  const saving = f.save();
  f.respond('Candidate.');
  await saving;
  assert.equal(f.copy.innerHTML, 'Candidate.');
  assert.equal(f.editor.open, false);
  f.type('Another edit.');
  f.cancel();
  assert.equal(f.area.value, 'Candidate.');
  assert.equal(f.area.dataset.shared, '');
});

test('typing during save stays open and is not overwritten', async () => {
  const f = fixture();
  f.editor.open = true;
  f.type('First.');
  const saving = f.save();
  f.type('Second.');
  f.respond('First.');
  await saving;
  assert.equal(f.area.value, 'Second.');
  assert.equal(f.editor.open, true);
  assert.equal(f.form.dataset.dirty, 'true');
  assert.equal(f.stale.removed, true);
  f.cancel();
  assert.equal(f.area.value, 'First.');
});

test('stale save keeps unsaved prose editable', async () => {
  const f = fixture();
  f.editor.open = true;
  f.type('Keep this.');
  const saving = f.save();
  f.respond('', false);
  await saving;
  assert.equal(f.editor.open, true);
  assert.equal(f.area.value, 'Keep this.');
  assert.equal(f.form.dataset.dirty, 'true');
  assert.match(f.status.textContent, /Not saved/);
  assert.equal(f.stale.removed, false);
});

test('reader compresses colon and spaced evidence placeholders into a short label', () => {
  const f = fixture();
  f.area.dataset.evidenceItems = JSON.stringify({
    'E33-CITE-opioid-system-stakes': {label: 'E33C.SystemStakes', status: 'specified'},
  });
  [
    'Patients and systems [E33-CITE-opioid-system-stakes: source verification pending].',
    'Patients and systems [E33-CITE-opioid-system-stakes pending].',
  ].forEach((source) => {
    f.type(source);
    assert.match(f.reading.innerHTML, /\(E33C\.SystemStakes\)/);
    assert.doesNotMatch(f.reading.innerHTML, /verification pending|stakes pending/);
    assert.doesNotMatch(f.reading.innerHTML, /evtag|preview-evidence/);
  });
});
