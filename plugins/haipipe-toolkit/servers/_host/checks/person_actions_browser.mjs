// A person's own actions, clicked in a real browser (b11 s12, b12 s12, 261023): CHECK a page (pass, and return with
// a reason), sign a Job's close, and Review and approve a design release. Each is tried first without its tick (it
// must refuse and write nothing), then done; the page reloads on its new state and the files on disk say so.
// WRITES to the throwaway Projects only: never point it at a real Board.
//
//   python checks/person_actions_fixture.py <dir>
//   python serve.py --root <dir> --port <p> --no-auth --no-terminal
//   chrome --headless=new --remote-debugging-port=9333 --user-data-dir=<tmp> about:blank &
//   CHECK_HOST=http://127.0.0.1:<p> CHECK_ROOT=<dir> node checks/person_actions_browser.mjs <shots dir>
import fs from 'node:fs';

const CDP = 'http://' + (process.env.CHECK_CDP || '127.0.0.1:9333');
const HOST = process.env.CHECK_HOST || 'http://127.0.0.1:5876';
const ROOT = process.env.CHECK_ROOT;
const OUT = process.argv[2] || '.';
const BOARD = 'Project-InsightDemo/insights/b01_topic';
const J04 = `${BOARD}/j04_prototype-p2_data-demov3`;
const J03 = `${BOARD}/j03_prototype-p2_data-demov2`;
const DJOB = 'Project-DesignDemo/designs/b01_demo_app/j03_g01_m04';
const url = (path, space, sub = '') => `${HOST}/_board/workbench?path=${encodeURIComponent(path)}` +
  `&space=${encodeURIComponent(space)}` + (sub ? `&sub=${encodeURIComponent(sub)}` : '');
const disk = p => fs.readFileSync(`${ROOT}/${p}`, 'utf8');
if (!ROOT || !fs.existsSync(`${ROOT}/${BOARD}`)) { console.error('CHECK_ROOT: a person_actions_fixture.py folder'); process.exit(2); }

const results = [];
const ok = (name, cond, detail = '') => results.push({ name, pass: !!cond, detail });

class Tab {
  async open() {
    const t = await (await fetch(`${CDP}/json/new?about:blank`, { method: 'PUT' })).json();
    this.id = t.id; this.ws = new WebSocket(t.webSocketDebuggerUrl); this.n = 0; this.wait = {}; this.errors = []; this.loads = [];
    await new Promise(r => this.ws.addEventListener('open', r));
    this.ws.addEventListener('message', ev => {
      const m = JSON.parse(ev.data);
      if (m.id && this.wait[m.id]) { this.wait[m.id](m); delete this.wait[m.id]; return; }
      if (m.method === 'Runtime.exceptionThrown') this.errors.push('exception: ' + (m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text));
      if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') this.errors.push('console: ' + m.params.args.map(a => a.value ?? a.description).join(' '));
      if (m.method === 'Page.loadEventFired') { this.loads.forEach(f => f()); this.loads = []; }
    });
    for (const d of ['Runtime', 'Page']) await this.send(`${d}.enable`);
  }
  send(method, params = {}) {
    const id = ++this.n;
    return new Promise(r => { this.wait[id] = m => r(m.result ?? m); this.ws.send(JSON.stringify({ id, method, params })); });
  }
  loaded() { return new Promise(r => { this.loads.push(r); setTimeout(r, 30000); }); }
  async go(u) { const l = this.loaded(); await this.send('Page.navigate', { url: u }); await l; await new Promise(r => setTimeout(r, 300)); }
  async ev(expr) {
    const r = await this.send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true });
    if (r.exceptionDetails) throw new Error('eval: ' + (r.exceptionDetails.exception?.description || r.exceptionDetails.text));
    return r.result.value;
  }
  // click, then wait for the reload a successful write makes (or a moment, when it is refused)
  async clickAndMaybeReload(expr) {
    const l = this.loaded();
    await this.ev(expr);
    await Promise.race([l, new Promise(r => setTimeout(r, 2500))]);
    await new Promise(r => setTimeout(r, 300));
  }
  async shot(name) {
    const r = await this.send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(`${OUT}/${name}.png`, Buffer.from(r.data, 'base64'));
  }
  close() { return fetch(`${CDP}/json/close/${this.id}`); }
}

// the form in one Task's row of 4 · Check: open it, tick or not, a reason, then press a button
const ROW = (task, tick, why, button) => `(() => {
  const row = [...document.querySelectorAll('tr')].find(tr => tr.querySelector('a[data-pop]') && tr.textContent.includes(${JSON.stringify(task)}));
  const d = row && row.querySelector('details.check-it'); if (!d) return 'no form';
  d.open = true; const p = d.querySelector('p.sign-row');
  p.querySelector('[name=attest]').checked = ${tick}; p.querySelector('[name=why]').value = ${JSON.stringify(why)};
  [...p.querySelectorAll('button')].find(b => JSON.parse(b.dataset.body).verdict === ${JSON.stringify(button)}).click(); return 'clicked';
})()`;
const BUTTON_TEXT = (task, button) => `(() => { const row = [...document.querySelectorAll('tr')].find(tr => tr.querySelector('a[data-pop]') && tr.textContent.includes(${JSON.stringify(task)}));
  return [...row.querySelectorAll('button')].filter(b => JSON.parse(b.dataset.body).verdict === ${JSON.stringify(button)})
    .map(b => b.textContent).join(' | '); })()`;

async function main() {
  const tab = new Tab(); await tab.open();
  const t03 = `${J04}/t03_K01_question-c/t03_K01_question-c.md`, t02 = `${J04}/t02_I01_question-b/t02_I01_question-b.md`;

  // 1 · CHECK, pass: refused without the tick, then done
  await tab.go(url(J04, 'Work Details', '4 · Check'));
  await tab.shot('1-check-before');
  const before = disk(t03);
  await tab.clickAndMaybeReload(ROW('t03_K01', false, '', 'pass'));
  ok('1a no tick: refused on the button', /✗ tick that you read it first/.test(await tab.ev(BUTTON_TEXT('t03_K01', 'pass'))));
  ok('1b no tick: the page is untouched', disk(t03) === before);
  await tab.clickAndMaybeReload(ROW('t03_K01', true, '', 'pass'));
  ok('1c pass: the page says ✅ · a person', /check: ✅ \d{6} · a person/.test(disk(t03)), disk(t03).split('\n').find(l => l.startsWith('check')));
  ok('1d pass: the row shows it after the reload', await tab.ev(`[...document.querySelectorAll('tr')].find(tr => tr.querySelector('a[data-pop]') && tr.textContent.includes('t03_K01')).textContent.includes('· a person')`));
  ok('1e pass: a pass of run-check-t03, by a person', /by: a person/.test(disk(`${J04}/t03_K01_question-c/runs/run-check-t03/run.yaml`)));

  // 2 · CHECK, return: a reason is required, then the page goes back to 3 · Write
  await tab.clickAndMaybeReload(ROW('t02_I01', true, '', 'return'));
  ok('2a return with no reason: refused', /✗ say why/.test(await tab.ev(BUTTON_TEXT('t02_I01', 'return'))));
  await tab.clickAndMaybeReload(ROW('t02_I01', true, 'part-b is not cited', 'return'));
  ok('2b return: the page says ↩ and why', /check: ↩ \d{6} · a person · part-b is not cited/.test(disk(t02)));
  await tab.shot('2-check-after');
  await tab.go(url(J04, 'Work Details', '3 · Write'));
  ok('2c 3 · Write takes it back', await tab.ev(`document.body.textContent.includes('Returned by CHECK') && document.body.textContent.includes('t02_I01')`));

  // 3 · the close: waits on j04; signed on j03 (every step done)
  await tab.go(url(J04, 'Work Details', '6 · Close'));
  ok('3a j04: the sign is off, it says what it waits on', await tab.ev(`(() => { const b = [...document.querySelectorAll('button')].find(x => x.textContent === 'Sign the close'); return !!b && b.disabled && document.body.textContent.includes('it waits on'); })()`));
  await tab.go(url(J03, 'Work Details', '6 · Close'));
  await tab.ev(`document.querySelector('details.items-step').open = true`);
  await tab.shot('3-close-before');
  const SIGN = tick => `(() => { const b = document.querySelector('button[data-post="/_board/insight-act"]');
    b.parentNode.querySelector('[name=attest]').checked = ${tick}; b.click(); return true; })()`;
  await tab.clickAndMaybeReload(SIGN(false));
  ok('3b no tick: refused, the Job still open', /state: open/.test(disk(`${J03}/j03_prototype-p2_data-demov2.md`)));
  await tab.clickAndMaybeReload(SIGN(true));
  const face = disk(`${J03}/j03_prototype-p2_data-demov2.md`);
  ok('3c signed: the Job is closed, ✅ and the date', /state: closed/.test(face) && /signed: ✅ \d{6}/.test(face));
  ok('3d the close Run says a person, in the workbench', /signed: ✅ \d{6} · a person, in the workbench/.test(disk(`${J03}/runs/run-close-j03/run.yaml`)));
  await tab.ev(`document.querySelector('details.items-step').open = true`);
  ok('3e the page shows ✓ closed', await tab.ev(`document.body.innerText.includes('✓ closed')`));
  await tab.shot('3-close-after');

  // 4 · Review and approve, on the design Job's Delivery
  await tab.go(url(DJOB, 'Delivery'));
  ok('4a the panel lists what one sign releases', await tab.ev(`document.body.innerText.includes('Review and approve') && document.body.innerText.includes('freezes the 3 predictions')`));
  await tab.shot('4-approve-before');
  const APPROVE = tick => `(() => { const b = document.querySelector('button[data-post="/_board/design-ladder-act"]');
    b.parentNode.querySelector('[name=attest]').checked = ${tick}; b.click(); return true; })()`;
  await tab.clickAndMaybeReload(APPROVE(false));
  const kept = fs.readdirSync(`${ROOT}/${DJOB}`).filter(n => /^t\d+_d\d+_/.test(n)).sort().slice(0, 3);
  ok('4b no tick: nothing frozen', kept.every(t => /frozen: draft/.test(disk(`${DJOB}/${t}/prediction.yaml`))));
  await tab.clickAndMaybeReload(APPROVE(true));
  ok('4c approved: each kept prediction frozen with the date', kept.every(t => /frozen: '?\d{6}'?/.test(disk(`${DJOB}/${t}/prediction.yaml`))));
  ok('4d approved: each kept design released', kept.every(t => /state: released/.test(disk(`${DJOB}/${t}/${t}.md`))));
  ok('4e the release Run says a person, in the workbench', /signed: ✅ \d{6} · a person, in the workbench/.test(disk(`${DJOB}/runs/run-release-j03/run.yaml`)));
  ok('4f the page shows ✓ released', await tab.ev(`document.body.innerText.includes('✓ released')`));
  await tab.shot('4-approve-after');

  ok('console clean', tab.errors.length === 0, tab.errors.slice(0, 5).join(' || '));
  await tab.close();
  const failed = results.filter(r => !r.pass);
  for (const r of results) console.log(`${r.pass ? 'PASS' : 'FAIL'}  ${r.name}${r.pass ? '' : '  ·  ' + r.detail}`);
  console.log(`\n${results.length - failed.length} of ${results.length} pass`);
  process.exit(failed.length ? 1 : 0);
}
main().catch(e => { console.error(e); process.exit(2); });
