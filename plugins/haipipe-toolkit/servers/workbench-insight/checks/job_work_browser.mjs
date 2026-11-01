// The insight Job's Work step tabs in a real browser (b11 s12, 261022): open each tab, open its work panel, type a
// note, Copy prompt (the clipboard stubbed), reload, open a pop-out, follow every link; console errors fail it.
// Read-only gestures only. Same harness as servers/_host/checks/*.mjs: your own Chrome with a debugging port.
//
//   chrome --headless=new --remote-debugging-port=9333 --user-data-dir=<tmp> about:blank &
//   python tests/plan_c_fixture.py <dir>; python ../_host/serve.py --root <dir> --port <p> --no-auth --no-terminal
//   CHECK_FIX=http://127.0.0.1:<p> node checks/job_work_browser.mjs <shots dir>
//
// Optional, a real Board on another host: CHECK_REAL=<origin> CHECK_REAL_JOB=<SPACE-relative Job folder>
// (a Job with Runs and pages, its D · I · K Runs on disk) adds every tab of that Job, its pop-out, every link,
// a narrow screen, and its other Spaces.
import fs from 'node:fs';

const CDP = 'http://' + (process.env.CHECK_CDP || '127.0.0.1:9333');
const OUT = process.argv[2] || '.';
const FIX = process.env.CHECK_FIX || 'http://127.0.0.1:5875';
const REAL = process.env.CHECK_REAL || '';
const REAL_JOB = process.env.CHECK_REAL_JOB || '';
const FIX_BOARD = 'Project-InsightDemo/insights/b01_topic';
const STEPS = ['1 · Launch', '2 · Run', '3 · Write', '4 · Check', '5 · Compare', '6 · Close'];
const url = (host, path, space = 'Work Details', sub = '') =>
  `${host}/_board/workbench?path=${encodeURIComponent(path)}&space=${encodeURIComponent(space)}` +
  (sub ? `&sub=${encodeURIComponent(sub)}` : '');

const results = [];
const ok = (name, cond, detail = '') => { results.push({ name, pass: !!cond, detail }); };

class Tab {
  async open() {
    const t = await (await fetch(`${CDP}/json/new?about:blank`, { method: 'PUT' })).json();
    this.id = t.id; this.ws = new WebSocket(t.webSocketDebuggerUrl); this.n = 0; this.wait = {}; this.errors = [];
    this.loads = [];
    await new Promise(r => this.ws.addEventListener('open', r));
    this.ws.addEventListener('message', ev => {
      const m = JSON.parse(ev.data);
      if (m.id && this.wait[m.id]) { this.wait[m.id](m); delete this.wait[m.id]; return; }
      if (m.method === 'Runtime.exceptionThrown') this.errors.push('exception: ' + (m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text));
      if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') this.errors.push('console: ' + m.params.args.map(a => a.value ?? a.description).join(' '));
      if (m.method === 'Log.entryAdded' && m.params.entry.level === 'error') this.errors.push('log: ' + m.params.entry.text + ' ' + (m.params.entry.url || ''));
      if (m.method === 'Page.loadEventFired') this.loads.forEach(f => f()), this.loads = [];
    });
    for (const d of ['Runtime', 'Page', 'Log']) await this.send(`${d}.enable`);
  }
  send(method, params = {}) {
    const id = ++this.n;
    return new Promise(r => { this.wait[id] = m => r(m.result ?? m); this.ws.send(JSON.stringify({ id, method, params })); });
  }
  async go(u) {
    const loaded = new Promise(r => this.loads.push(r));
    const t0 = Date.now();
    await this.send('Page.navigate', { url: u });
    await Promise.race([loaded, new Promise(r => setTimeout(r, 60000))]);
    await new Promise(r => setTimeout(r, 400));
    return Date.now() - t0;
  }
  async ev(expr) {
    const r = await this.send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true });
    if (r.exceptionDetails) throw new Error('eval: ' + (r.exceptionDetails.exception?.description || r.exceptionDetails.text));
    return r.result.value;
  }
  async shot(name) {
    const r = await this.send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false });
    fs.writeFileSync(`${OUT}/${name}.png`, Buffer.from(r.data, 'base64'));
  }
  close() { return fetch(`${CDP}/json/close/${this.id}`); }
}

// what the page shows: the open step tab, the step box, its chip, the Runs panel's buttons
const STATE = `(() => {
  const tabs = [...document.querySelectorAll('a.tab, .tab')].map(a => a.textContent.trim()).filter(t => /^\\d · /.test(t));
  const on = [...document.querySelectorAll('.tab.on, a.tab.on')].map(a => a.textContent.trim()).filter(t => /^\\d · /.test(t));
  const box = document.querySelector('details.items-step');
  const panel = document.querySelector('section.runs-panel');
  const runs = panel ? [...panel.querySelectorAll('button.run-type:not(.run-new)')].map(b => b.dataset.label || b.textContent.trim()) : [];
  return { tabs, on, box: !!box, open: box ? box.open : null, chip: box ? box.querySelector('summary .st')?.textContent.trim() : '',
           summary: box ? box.querySelector('summary')?.textContent.trim() : '', runs,
           running: document.body.innerText.includes('Running now'),
           scrollW: document.documentElement.scrollWidth, innerW: innerWidth, title: document.title };
})()`;

async function main() {
  const tab = new Tab(); await tab.open();

  // A · the open fixture Job (j04): opens on 1 · Launch, Running now, panel folded, notes, Copy, reload keeps notes
  const j04 = `${FIX_BOARD}/j04_prototype-p2_data-demov3`;
  await tab.go(url(FIX, j04));
  let s = await tab.ev(STATE);
  ok('A1 six step tabs', JSON.stringify(s.tabs.slice(0, 6)) === JSON.stringify(STEPS), s.tabs.join(' | '));
  ok('A2 opens on 1 · Launch', s.on.includes('1 · Launch'), s.on.join(','));
  ok('A3 work panel folded at first', s.box && s.open === false, `box=${s.box} open=${s.open}`);
  ok('A4 chip says next', /next/.test(s.chip), s.chip);
  ok('A5 Running now shown (run-launch-j04 open)', await tab.ev(`document.body.innerHTML.includes('Running now') && document.body.innerHTML.includes('run-launch-j04')`));
  ok('A6 Runs panel = launch cards', JSON.stringify(s.runs) === JSON.stringify(['run-launch-j04', 'run-power-j04']), s.runs.join(','));
  await tab.shot('A-j04-launch-folded');
  // open the panel by clicking its bar
  await tab.ev(`document.querySelector('details.items-step > summary').click(), true`);
  s = await tab.ev(STATE);
  ok('A7 click opens the work panel', s.open === true);
  const vis = await tab.ev(`(() => { const t = document.querySelector('details.items-step textarea.run-notes'); return !!t && t.offsetHeight > 0; })()`);
  ok('A8 notes box visible once open', vis);
  await tab.shot('A-j04-launch-open');
  // type a note, then Copy prompt with the clipboard captured
  const note = 'start with the K questions; skip retired ones';
  await tab.ev(`(() => { const t = document.querySelector('details.items-step textarea.run-notes'); t.focus(); t.value = ${JSON.stringify(note)};
                t.dispatchEvent(new Event('input', {bubbles: true})); return true; })()`);
  const copied = await tab.ev(`new Promise(r => { window.__copied = null;
      navigator.clipboard.writeText = t => { window.__copied = t; return Promise.resolve(); };
      document.querySelector('details.items-step .run-copy').click(); setTimeout(() => r({ text: window.__copied,
        btn: document.querySelector('details.items-step .run-copy').textContent }), 300); })`);
  ok('A9 Copy gives the card prompt', /^Run with haipipe-task-orchestrator-agent\. \/haipipe-insight run the Job /.test(copied.text || ''), (copied.text || '').slice(0, 90));
  ok('A10 the prompt names the Job folder', (copied.text || '').includes(j04));
  ok('A11 your note goes with it', (copied.text || '').includes('user feedback: ' + note));
  ok('A12 the session line ends it', /\nRun this in the Claude session "b01_topic: j04-prototype-p2-data-demov3"; start it if it is not running\.$/.test(copied.text || ''), (copied.text || '').split('\n').pop());
  ok('A13 button says Copied', copied.btn === 'Copied', copied.btn);
  fs.writeFileSync(`${OUT}/A-copied.txt`, copied.text || '');
  await tab.go(url(FIX, j04));
  const kept = await tab.ev(`document.querySelector('details.items-step textarea.run-notes').value`);
  ok('A14 the note survives a reload', kept === note, kept);
  await tab.ev(`localStorage.clear(), true`);

  // B · each step tab of j04: its chip, its Runs panel, no console error
  const want = { '1 · Launch': ['run-launch-j04', 'run-power-j04'], '2 · Run': ['rNN_<partition>', 'run-pool-t<NN>'],
    '3 · Write': ['run-write-t<NN>', 'run-write-t<NN>', 'run-write-t<NN>', 'run-write-t<NN>', 'run-overall-j04'],
    '4 · Check': ['run-check-alignment-t<NN>', 'run-check-t<NN>'], '5 · Compare': ['run-compare-j03', 'run-propose-j04'],
    '6 · Close': ['run-close-j04'] };
  for (const st of STEPS) {
    // reach the tab by clicking it, as a person does
    const href = await tab.ev(`[...document.querySelectorAll('a.tab')].find(a => a.textContent.trim() === ${JSON.stringify(st)})?.href || ''`);
    ok(`B ${st}: its tab is a link`, !!href);
    if (href) await tab.go(href);
    s = await tab.ev(STATE);
    ok(`B ${st}: opens`, s.on.includes(st), s.on.join(','));
    ok(`B ${st}: Runs panel`, JSON.stringify(s.runs) === JSON.stringify(want[st]), s.runs.join(','));
    ok(`B ${st}: has a chip`, !!s.chip, s.summary);
  }
  ok('B j04 console clean', tab.errors.length === 0, tab.errors.slice(0, 5).join(' || '));
  tab.errors = [];

  // C · the closed fixture Job (j03): every step done, opens on 6 · Close
  await tab.go(url(FIX, `${FIX_BOARD}/j03_prototype-p2_data-demov2`));
  s = await tab.ev(STATE);
  ok('C1 closed Job opens on 6 · Close', s.on.includes('6 · Close'), s.on.join(','));
  ok('C2 its chip is done', /done/.test(s.chip), s.chip);
  for (const st of STEPS) {
    await tab.go(url(FIX, `${FIX_BOARD}/j03_prototype-p2_data-demov2`, 'Work Details', st));
    const chip = (await tab.ev(STATE)).chip;
    ok(`C ${st}: done or optional`, /done|optional/.test(chip), chip);
  }
  // the older tree links still land
  for (const [old, st] of [['All', '2 · Run'], ['hard', '2 · Run'], ['soft', '4 · Check']]) {
    await tab.go(url(FIX, `${FIX_BOARD}/j03_prototype-p2_data-demov2`, 'Work Details', old));
    ok(`C old view ${old} → ${st}`, (await tab.ev(STATE)).on.includes(st));
  }
  ok('C j03 console clean', tab.errors.length === 0, tab.errors.slice(0, 5).join(' || '));
  tab.errors = [];

  if (REAL && REAL_JOB) await realJob(tab);
  await tab.close();
  return finish();
}

async function realJob(tab) {
  let s;
  // D · the real Job: every tab, load time, panel, copy, pop-outs and every link it carries
  const times = {};
  const links = new Set();
  for (const st of STEPS) {
    times[st] = await tab.go(url(REAL, REAL_JOB, 'Work Details', st));
    s = await tab.ev(STATE);
    ok(`D ${st}: opens`, s.on.includes(st), s.on.join(','));
    ok(`D ${st}: panel folded`, s.box && s.open === false);
    await tab.ev(`document.querySelector('details.items-step > summary').click(), true`);
    const c = await tab.ev(`new Promise(r => { window.__copied = null; navigator.clipboard.writeText = t => { window.__copied = t; return Promise.resolve(); };
       const b = document.querySelector('details.items-step .run-copy'); if (!b) return r(null); b.click(); setTimeout(() => r(window.__copied), 300); })`);
    ok(`D ${st}: Copy prompt works`, !!c && c.includes(REAL_JOB) && /\nRun this in the Claude session "[^"]+: j\d+-[^"]+"; start it if it is not running\.$/.test(c),
       (c || 'no copy button').slice(0, 80));
    if (st === '2 · Run' || st === '4 · Check') await tab.shot(`D-real-${st.replace(/\W+/g, '')}-open`);
    for (const h of await tab.ev(`[...document.querySelectorAll('main a[href], .space-body a[href], a[data-pop]')].map(a => a.getAttribute('href'))`))
      if (h && h.startsWith('/')) links.add(h);
  }
  ok('D real Job console clean', tab.errors.length === 0, tab.errors.slice(0, 5).join(' || '));
  tab.errors = [];
  fs.writeFileSync(`${OUT}/D-times.json`, JSON.stringify(times, null, 1));
  // a run mark's pop-out on 2 · Run opens its run page
  await tab.go(url(REAL, REAL_JOB, 'Work Details', '2 · Run'));
  const popped = await tab.ev(`new Promise(r => { const a = [...document.querySelectorAll('a[data-pop]')].find(x => x.getAttribute('href').includes('insight-run?run='));
      if (!a) return r(null); a.click(); const f = document.getElementById('frame-pop-frame');
      setTimeout(() => r({ open: document.getElementById('frame-pop').open, src: f.getAttribute('src') || f.src,
                            text: (f.contentDocument && f.contentDocument.body ? f.contentDocument.body.innerText.slice(0, 120) : '') }), 2500); })`);
  ok('D a run mark opens the pop-out', popped && popped.open && /insight-run\?run=/.test(popped.src), JSON.stringify(popped).slice(0, 160));
  ok('D the pop-out shows the run page', popped && popped.text.length > 20, popped && popped.text);
  await tab.shot('D-real-run-popout');
  // every link the six tabs carry answers
  const bad = [];
  const all = [...links];
  for (let i = 0; i < all.length; i += 12) {
    await Promise.all(all.slice(i, i + 12).map(async h => {
      try { const r = await fetch(REAL + h); if (r.status !== 200) bad.push(`${r.status} ${h}`); } catch (e) { bad.push(`ERR ${h}`); }
    }));
  }
  ok(`D every link answers (${all.length})`, bad.length === 0, bad.slice(0, 5).join(' || '));

  // E · narrow screen: no sideways scroll on a step tab
  await tab.send('Emulation.setDeviceMetricsOverride', { width: 420, height: 900, deviceScaleFactor: 1, mobile: true });
  await tab.go(url(REAL, REAL_JOB, 'Work Details', '4 · Check'));
  s = await tab.ev(STATE);
  ok('E narrow: no sideways scroll', s.scrollW <= s.innerW + 2, `${s.scrollW} > ${s.innerW}`);
  await tab.shot('E-narrow-check');
  await tab.send('Emulation.clearDeviceMetricsOverride');

  // F · the rest of the Job, the Board and a Task still render without errors
  for (const [p, sp] of [[REAL_JOB, 'Description'], [REAL_JOB, 'Audience Report'], [REAL_JOB, 'Runs'],
                         [REAL_JOB.split('/').slice(0, -1).join('/'), 'Work Details'], [REAL_JOB + '/t30_K01_psychological-triggers', 'Work Details']]) {
    await tab.go(url(REAL, p, sp));
    ok(`F ${sp} at ${p.split('/').pop()}: renders`, (await tab.ev(`document.title`)).length > 0);
  }
  ok('F console clean', tab.errors.length === 0, tab.errors.slice(0, 5).join(' || '));

}

function finish() {
  fs.writeFileSync(`${OUT}/results.json`, JSON.stringify(results, null, 1));
  const failed = results.filter(r => !r.pass);
  for (const r of results) console.log(`${r.pass ? 'PASS' : 'FAIL'}  ${r.name}${r.pass ? '' : '  ·  ' + r.detail}`);
  console.log(`\n${results.length - failed.length} of ${results.length} pass`);
  process.exit(failed.length ? 1 : 0);
}

main().catch(e => { console.error(e); process.exit(2); });
