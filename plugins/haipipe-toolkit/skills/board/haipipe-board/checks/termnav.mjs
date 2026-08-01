/* Terminal-follows-navigation suite — the ⌨ coverage navtest.mjs doesn't have.
   Same harness shape as SDK-Talk's navtest.mjs, own Chrome on :9333.

   The scenario that found the bug: a GROUP terminal, then navigate away.
   follow() must PARK the group's PTY (release with the group param); the old
   code called termRelease(oldFile) which posts file='board.md' with no group,
   so the park landed on the BOARD scope and the group PTY stayed HELD. */
/* All overridable so checks/run.py can aim this at a throwaway fixture board
   and its own Chrome. Defaults = the family's design board on the live 5599. */
const BOARD = process.env.CHECK_BOARD_URL
  || '/Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722';
const HOSTPORT = process.env.CHECK_HOSTPORT || '127.0.0.1:5599';
const BASE = `http://${HOSTPORT}${BOARD}/board`;
const CDP = process.env.CHECK_CDP || '127.0.0.1:9333';
const FIGDIR = process.env.CHECK_FIGDIR
  || ('/Users/jluo41/Desktop/Physician-SPACE' + BOARD + '/fig');

const targets = await (await fetch(`http://${CDP}/json`)).json();
const page = targets.find(t => t.type === 'page');
const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise(r => ws.addEventListener('open', r));
let id = 0; const waits = new Map(); const errors = [];
ws.addEventListener('message', e => {
  const m = JSON.parse(e.data);
  if (m.id && waits.has(m.id)) { waits.get(m.id)(m); waits.delete(m.id); }
  if (m.method === 'Runtime.exceptionThrown')
    errors.push(m.params.exceptionDetails.exception?.description || 'exception');
  if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error')
    errors.push('console.error: ' + (m.params.args[0]?.value || ''));
});
const send = (method, params = {}) =>
  new Promise(r => { const i = ++id; waits.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function evaluate(expr) {
  const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true });
  if (r.result?.exceptionDetails) throw new Error(JSON.stringify(r.result.exceptionDetails.exception));
  return r.result.result.value;
}
await send('Runtime.enable');

const STATE = `(function(){
  var c = document.getElementById('chat'), q = c && c.querySelector('.qid');
  return { open: !!(c && c.classList.contains('on')),
           qid: q ? q.textContent.trim() : null,
           url: location.pathname.split('/').slice(-2).join('/'),
           term: document.body.classList.contains('termon') };
})()`;
async function waitUrl(endsWith, ms = 8000) {
  const t0 = Date.now();
  while (Date.now() - t0 < ms) {
    const u = await evaluate('location.pathname');
    if (u.endsWith(endsWith) && await evaluate('!!document.querySelector("div.wrap")')) {
      await sleep(250); return true;
    }
    await sleep(150);
  }
  throw new Error(`url never became ${endsWith} (now ${await evaluate('location.pathname')})`);
}
async function clickLink(match, expectUrl) {
  const ok = await evaluate(`(function(){
    var as = [].slice.call(document.querySelectorAll('div.wrap a[href]'));
    var a = as.filter(function(x){ return x.getAttribute('href').indexOf(${JSON.stringify(match)}) >= 0; })[0];
    if (!a) return false; a.click(); return true;
  })()`);
  if (!ok) throw new Error('no link matching ' + match);
  await waitUrl(expectUrl || match.replace(/^\.\.\//, ''));
}
async function openDrawer() { await evaluate(`document.getElementById('chatfab').click()`); await sleep(500); }
async function goto(u) { await send('Page.navigate', { url: u }); await waitUrl(u.split('/').pop()); await sleep(400); }
async function clickTermBtn() { await evaluate(`document.querySelector('#chat .term').click()`); }

/* the terminal's painted screen, to prove a real claude is on the other end */
const SCREEN = `(function(){var t=window.__boardTerm; if(!t) return '';
  var out=[], b=t.buffer.active;
  for (var i=0;i<b.length;i++){var l=b.getLine(i); if(l){var s=l.translateToString(true).trim(); if(s) out.push(s);}}
  return out.join('\\n');})()`;
async function waitPaint(ms = 20000) {
  const t0 = Date.now();
  while (Date.now() - t0 < ms) {
    const s = await evaluate(SCREEN);
    if (s && s.length > 80) return s;
    await sleep(500);
  }
  return '';
}

/* server-side truth: ask serve.py to (re)open a terminal for a target.
   parked-and-reusable => {ok, reused:true}. held-by-someone => error. */
async function apiTerm(body) {
  const r = await fetch(`http://${HOSTPORT}/_board/term`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ path: BOARD + '/board/index.html', ...body }) });
  return await r.json();
}
async function apiKill(body) {
  const r = await fetch(`http://${HOSTPORT}/_board/release`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ path: BOARD + '/board/index.html', ...body }) });
  return await r.json();
}

const results = [];
function check(name, got, want) {
  const pass = got === want;
  results.push({ name, pass, got, want });
  console.log(`${pass ? 'PASS' : 'FAIL'}  ${name}\n      got=${got}  want=${want}`);
}

/* ── T9a group terminal opens on a TREE group page ─────────────── */
await goto(`${BASE}/QD.html`);
await openDrawer();
check('T9a drawer binds group', (await evaluate(STATE)).qid, '🗂 QD');
await clickTermBtn();
const paint1 = await waitPaint();
check('T9a group ⌨ paints', paint1.length > 80, true);

/* ── T9b navigate group -> page WITH the terminal on ───────────── */
await clickLink('QD/QD1-chat-per-question.html');
await sleep(1500);                      // follow(): release old, open new
let s = await evaluate(STATE);
check('T9b drawer follows to QD1', s.qid, 'QD1');
check('T9b terminal view stays on', s.term, true);
const paint2 = await waitPaint();
check('T9b page ⌨ paints', paint2.length > 80, true);

/* ── T9b' image paste into the TREE page's terminal ────────────
   board.html is being discarded (JL 260731), so the paste proof must hold
   on a tree URL: synthetic ClipboardEvent with a real PNG File, expect the
   repo-root-relative fig/ path typed into the PTY. */
const PNG = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGP4z8DwHwAFAAH/q842iQAAAABJRU5ErkJggg==';
await evaluate(`(function(){
  var el = document.querySelector('#chat .tm .xterm-helper-textarea');
  if (!el) return 'no textarea';
  var b = atob('${PNG}'), u = new Uint8Array(b.length);
  for (var i = 0; i < b.length; i++) u[i] = b.charCodeAt(i);
  var dt = new DataTransfer();
  dt.items.add(new File([u], 'treenav-paste.png', {type: 'image/png'}));
  el.focus();
  el.dispatchEvent(new ClipboardEvent('paste', {clipboardData: dt, bubbles: true,
                                                cancelable: true, composed: true}));
  return 'dispatched';
})()`);
await sleep(4000);
const afterPaste = await evaluate(SCREEN);
check('T9b\' paste path typed on tree page', /fig\/treenav-paste-/.test(afterPaste), true);

/* ── T9c the group PTY was PARKED, not left held ───────────────
   If follow() dropped the group on release, the group key is still HELD
   and this reopen errors; parked-or-fresh both answer ok:true. reused:true
   proves the park (same process handed back). */
const g = await apiTerm({ file: 'board.md', group: 'QD', name: 'termnav-t9c' });
check('T9c group PTY reopenable', g.ok, true);
check('T9c group PTY was parked (reused)', g.reused === true, true);
await apiKill({ file: 'board.md', group: 'QD' });   // kill, not park: test session

/* ── T9d navigate page -> index WITH terminal on: board terminal ─ */
await clickLink('index.html');
await sleep(1500);
s = await evaluate(STATE);
check('T9d drawer follows to BOARD', s.qid, '🗂 BOARD');
/* the QD1 page PTY must now be parked, and reopenable */
const p = await apiTerm({ file: 'QD-working/QD1-chat-per-question.md' });
check('T9d page PTY reopenable', p.ok, true);
check('T9d page PTY was parked (reused)', p.reused === true, true);
await apiKill({ file: 'QD-working/QD1-chat-per-question.md' });

/* ── T9e close the board terminal, zero errors ─────────────────── */
await clickTermBtn();                    // back to chat view = park board PTY
await sleep(800);
await apiKill({ file: 'board.md' });     // reap the board test PTY too
check('T9f zero JS errors', errors.length, 0);
if (errors.length) console.log(errors.join('\n'));

/* clean the pasted test image out of the real board's fig/ */
try {
  const { readdirSync, unlinkSync } = await import('node:fs');
  const fig = FIGDIR;
  for (const f of readdirSync(fig))
    if (f.startsWith('treenav-paste-')) { unlinkSync(fig + '/' + f); console.log('cleaned fig/' + f); }
} catch (e) { console.log('fig cleanup skipped:', e.message); }

const fails = results.filter(r => !r.pass).length;
console.log(`\n${fails === 0 ? 'ALL PASS' : fails + ' FAILURES'} · ${results.length} checks`);
ws.close();
process.exit(fails === 0 ? 0 : 1);
