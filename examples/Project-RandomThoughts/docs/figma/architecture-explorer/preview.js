// Presentation prototype. Source files are read through ordinary links; nothing is written.
const ROOT = '';
const BLOCK = 'sources/';
const CHAT = 'sources/chat.md';
const SKILL = 'sources/';
const READER = 'sources/frame_sessions.py';
const content = document.querySelector('#content');
const source = (path, label, cls = '') => `<a class="${cls}" href="${ROOT}${path}">${label}</a>`;
const button = (label, route, primary = false) => `<a class="button${primary ? ' primary' : ''}" href="#${route}">${label}</a>`;
const property = (label, value) => `<div class="property"><div class="property-label">${label}</div><div class="property-value">${value}</div></div>`;
const heading = (crumb, title, subtitle, action = '') => `<p class="breadcrumb">${crumb}</p><div class="heading"><div><h2>${title}</h2>${subtitle ? `<p class="subtitle">${subtitle}</p>` : ''}</div>${action}</div>`;
const fileRow = (name, purpose, href, type = 'MD') => `<a class="file-row" href="${href}"><span class="file-icon">${type}</span><div><div class="filename">${name}</div><p class="file-purpose">${purpose}</p></div><span class="arrow" aria-hidden="true">↗</span></a>`;

function filesView() {
  return heading('Block / Project workbench / c01', 'Plugin principle and Chat', 'c01_plugin_principle_and_chat/', button('View in UI →', 'ui', true)) + `
    <section class="panel">
      <div class="panel-heading"><h3>Files</h3>${source(CHAT, 'Open source ↗', 'quiet-link')}</div>
      ${fileRow('c01_plugin_principle_and_chat.md', 'Concise questions, outputs, and links to the files they changed.', '#session')}
      <div class="properties">
        ${property('CONTAINS', 'Question · Output · Changed files')}
        ${property('WRITER', source(SKILL + 'qa.py', '<code>hai-chat / qa.py</code>'))}
        ${property('READ BY', '<a href="#ui">Block → Sessions</a>')}
      </div>
    </section>
    <section class="panel">
      <div class="panel-heading"><h3>How this file is produced</h3></div>
      <div class="lifecycle">
        <div><div class="step-number">01 / CREATE</div><div class="step-title">Keep a Chat</div>${source(SKILL + 'new_chat.py', '<code>new_chat.py</code>')}<p class="step-copy">Creates the cNN folder and its record.</p></div>
        <div class="flow-arrow" aria-hidden="true">→</div>
        <div><div class="step-number">02 / UPDATE</div><div class="step-title">Finish an answer</div>${source(SKILL + 'qa.py', '<code>qa.py refresh</code>')}<p class="step-copy">Refreshes the QAs and changed-file links.</p></div>
        <div class="flow-arrow" aria-hidden="true">→</div>
        <div><div class="step-number">03 / READ</div><div class="step-title">Open Sessions</div>${source(READER, '<code>frame_sessions.py</code>')}<p class="step-copy">Reads the saved record for the Block page.</p></div>
      </div>
    </section>
    <div class="actions">${button('Inspect mapping', 'mapping')}${button('Read QAs', 'session')}${button('Inspect skill', 'skill')}</div>`;
}

function uiView() {
  return heading('UI System / Block page / Sessions', 'The file, presented as a page', 'Selected element · c01.q10', button('Show file', 'files')) + `
    <div class="preview-grid">
      <section class="page-preview" aria-label="Proposed Block page">
        <p class="breadcrumb">Project-Ladder / Work</p><h2>Project workbench</h2>
        <p class="mission">How should a plugin connect its folders, pages and sessions?</p>
        <details class="page-fold"><summary>Report</summary><p>A plugin is two systems and the map between them. ${source('sources/principle.md', 'Read the principle ↗')}</p></details>
        <details class="page-fold"><summary>Studio</summary><p>${source(BLOCK + 'element-ui.md', 'Element UI: how the workbench presents its parts ↗')}</p></details>
        <div class="page-fold"><h3 class="section-label">Sessions</h3>
          <div class="session-preview"><p class="section-label">Plugin principle and Chat</p><span class="qa-address">c01.q10</span>
            <p class="qa-title">What should chat tracing keep?</p><p class="qa-output">A concise question, its output, and the files it changed.</p>
            ${source(SKILL + 'qa.py', 'scripts/qa.py ↗', 'qa-file')}
            <div class="actions">${button('Open session', 'session')}</div>
          </div>
        </div>
      </section>
      <aside class="inspector" aria-label="Selected element source">
        <div class="inspector-heading">QA ELEMENT</div>
        ${property('SOURCE FOLDER', 'c01_plugin_principle_and_chat/')}
        ${property('SOURCE FILE', source(CHAT, 'c01_plugin_principle_and_chat.md'))}
        ${property('ADDRESS', '<code>c01.q10</code>')}
        ${property('READER', source(READER, '<code>frame_sessions.py</code>'))}
        ${button('Show mapping', 'mapping')}${button('Show file', 'files')}
      </aside>
    </div>`;
}

function mappingView() {
  return heading('Mapping / c01.q10', 'One record, connected views', 'Plugin principle and Chat', button('Open session', 'session')) + `
    <div class="map-grid">
      <a href="#files" class="map-card source"><span class="map-kicker">FILE SYSTEM</span><h3>Chat record</h3><p>Question, output and changed-file links.</p><code>c01_… / c01_….md</code></a>
      <div class="map-arrow" aria-hidden="true"><small>READ</small>→</div>
      <a href="${ROOT + READER}" class="map-card"><span class="map-kicker">MAPPING</span><h3>Sessions reader</h3><p>Finds the record and the work it touched.</p><code>frame_sessions.py ↗</code></a>
      <div class="map-arrow" aria-hidden="true"><small>RENDER</small>→</div>
      <a href="#ui" class="map-card destination"><span class="map-kicker">UI SYSTEM</span><h3>QA element</h3><p>Block → Sessions → the relevant question.</p><code>c01.q10</code></a>
    </div>
    <section class="panel"><div class="panel-heading"><h3>When the next answer ends</h3></div>
      <div class="write-flow"><a class="write-step" href="#session">Answer completes</a><span class="flow-arrow" aria-hidden="true">→</span>${source(SKILL + 'qa.py', '<code>qa.py refresh</code>', 'write-step')}<span class="flow-arrow" aria-hidden="true">→</span><a class="write-step" href="#files">Chat record updates</a><span class="flow-arrow" aria-hidden="true">→</span><a class="write-step" href="#ui">Sessions reads it</a></div>
      <p class="footnote">For a kept session with the refresh hook configured. ${source(SKILL + 'chat-contract.md', 'Update contract ↗')}</p>
    </section>
    <section class="panel"><div class="panel-heading"><h3>Follow the work in either direction</h3></div>
      <div class="actions" style="margin-top:0">${button('Session → Files', 'files')}${button('Files → UI', 'ui')}${button('UI → Session', 'session')}</div>
      <p class="footnote">The file owns the record. Each view reaches the same source.</p>
    </section>`;
}

const qas = [
  { id:'q07', q:'Can Chats sit beside Jobs and Studio topics?', answer:'The principle puts cNN Chat folders beside jNN Jobs and sNN Studio topics inside a Block.', files:[['PRINCIPLE.md','sources/principle.md']] },
  { id:'q09', q:'Create the hai-chat skill.', answer:'The skill was built and this conversation was saved in a Block-owned cNN folder.', files:[['SKILL.md',SKILL+'skill.md'],['new_chat.py',SKILL+'new_chat.py'],['chat-contract.md',SKILL+'chat-contract.md']] },
  { id:'q10', q:'What should chat tracing keep?', answer:'The question, the output, and the files changed. This QA led to the concise tracing contract in qa.py.', files:[['qa.py',SKILL+'qa.py']], open:true },
  { id:'q11', q:'Update the Chat once, at the end of the answer.', answer:'Refresh the record after the answer ends. Connecting the hook still requires the session environment to be configured.', files:[], related:['chat_hook.py',SKILL+'chat_hook.py'] }
];

function sessionView() {
  return heading('Block / Sessions / c01', 'Plugin principle and Chat', 'Questions, outputs, and the files they changed.', source(CHAT, 'Original record ↗', 'button')) + `
    <div class="session-layout"><section aria-label="Questions and outputs">${qas.map(qa => `
      <details class="qa" ${qa.open ? 'open' : ''}><summary><span class="qa-address">c01.${qa.id}</span><span>${qa.q}</span></summary>
        <div class="qa-body"><p>${qa.answer}</p><div class="qa-files">${qa.files.map(([label,path])=>source(path,label+' ↗','file-chip')).join('')}${qa.related?source(qa.related[1],'Related: '+qa.related[0]+' ↗','file-chip'):''}</div>
          <div class="actions">${button('Show files', 'files')}${button('Show mapping', 'mapping')}</div>
        </div>
      </details>`).join('')}</section>
      <aside class="owner-panel"><div class="panel"><h3>Kept with its Block</h3><div class="owner-tree">b10_project_workbench/
  jNN_…/
  sNN-…/
  <span class="chat-path">c01_…/</span></div><p class="footnote">The Block keeps concise QAs. The full native conversation stays with its chat provider.</p><div class="actions">${button('Inspect skill', 'skill')}</div></div></aside>
    </div><div class="actions">${button('Show folder', 'files')}${button('Show UI element', 'ui')}</div>`;
}

function skillView() {
  const rows = [
    ['SKILL.md','When to use the skill, and how.','MD','skill.md'],
    ['ref/chat-contract.md','The folder, QA and update contract.','MD','chat-contract.md'],
    ['scripts/new_chat.py','Allocates a cNN folder and creates its record.','PY','new_chat.py'],
    ['scripts/qa.py','Extracts concise QAs and changed files from a saved session.','PY','qa.py'],
    ['scripts/chat_hook.py','Refreshes configured, kept sessions after an answer.','PY','chat_hook.py'],
    ['tests/test_new_chat.py','Checks the folder and record behavior.','PY','test_new_chat.py']
  ];
  return heading('Skill folders / hai-chat', 'How a Chat record is made', 'Reusable instructions, contract, writer and checks.', button('See generated file →', 'files', true)) + `
    <section class="panel skill-files">${rows.map(([name,why,type,path])=>fileRow(name,why,ROOT+SKILL+path,type)).join('')}</section>
    <div class="actions">${button('Inspect mapping', 'mapping')}${button('Read the session', 'session')}</div>`;
}

const views = { files:filesView, ui:uiView, mapping:mappingView, session:sessionView, skill:skillView };
function render() {
  const requested = location.hash.slice(1);
  const route = Object.hasOwn(views, requested) ? requested : 'files';
  const tab = route === 'session' ? 'ui' : route === 'skill' ? 'files' : route;
  content.innerHTML = views[route]();
  document.querySelectorAll('[data-tab]').forEach(link => {
    if (link.dataset.tab === tab) link.setAttribute('aria-current','page');
    else link.removeAttribute('aria-current');
  });
  document.querySelectorAll('[data-route]').forEach(link => {
    if (link.dataset.route === route) link.setAttribute('aria-current','page');
    else link.removeAttribute('aria-current');
  });
  document.title = `${{files:'File System',ui:'UI System',mapping:'Mapping',session:'Session',skill:'Skill'}[route]} · Architecture explorer`;
}
window.addEventListener('hashchange', render);
render();
