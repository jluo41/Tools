/* QD8 A2.3 · DOES ANY REQUEST HOLD A CONNECTION AFTER THE PAGE HAS SETTLED?
 *
 * Every other check on this board asks whether the page is CORRECT, and on
 * 260802 they all passed while a reader waited two minutes for a click. The
 * page was right, the server answered it in 20 ms, the link was 30 ms, and
 * `POST /_board/activity` never returned at all: it ran an unpruned walk over
 * the whole repository. A browser allows SIX connections per origin across all
 * its tabs, so a few open pages held every one and the next click sat in
 * Chrome's queue showing "Provisional headers are shown".
 *
 * Nothing was watching for that, because "did it load" and "did everything
 * finish" are different questions and only the first was ever asked. This
 * asks the second.
 *
 *   node checks/pending.mjs [base-url] [board-path]
 *
 * Needs `ws`. Skips cleanly (exit 0, SKIP) when Chrome or ws is missing, so it
 * can sit in a suite that runs where neither exists.
 */
import { spawn } from 'node:child_process';

const HOST = process.argv[2] || 'http://127.0.0.1:5599';
const BOARD = process.argv[3] ||
  '/Tools/plugins/haipipe-toolkit/skills/diagrams/BoardSkillBoard-260722/board';
const SETTLE_MS = 12000;     // generous: a slow endpoint must look slow, not absent
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

let WebSocket;
try { ({ default: WebSocket } = await import('ws')); }
catch { console.log('SKIP pending.mjs · no `ws` module'); process.exit(0); }

const sh = (c) => new Promise(r => spawn('bash', ['-lc', c]).on('close', r));
const out = (c) => new Promise(r => {
  let s = ''; const p = spawn('bash', ['-lc', c]);
  p.stdout.on('data', d => s += d); p.on('close', () => r(s.trim()));
});

if (!(await out(`test -x "${CHROME}" && echo ok`))) {
  console.log('SKIP pending.mjs · no Chrome'); process.exit(0);
}

const port = 9334;
/* KILL CHROME BY ITS OWN PID, never by whoever holds the port: `lsof -ti` on
   the debug port matches THIS process too, because the CDP websocket is a
   connection to it, so the cleanup killed the checker mid-run (exit 137). */
await sh(`pkill -f cdp-pending-check 2>/dev/null; true`);
const kid = spawn(CHROME, [`--remote-debugging-port=${port}`, '--headless=new', '--no-first-run',
               '--user-data-dir=/tmp/cdp-pending-check', 'about:blank'],
      { detached: true, stdio: 'ignore' });
kid.unref();
const reap = () => { try { process.kill(-kid.pid, 'SIGKILL'); } catch {}
                     try { kid.kill('SIGKILL'); } catch {} };

let ws, tries = 0;
while (tries++ < 40) {
  try {
    const j = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
    const t = j.find(x => x.type === 'page');
    if (t) { ws = new WebSocket(t.webSocketDebuggerUrl, { maxPayload: 1 << 28 }); break; }
  } catch {}
  await new Promise(r => setTimeout(r, 250));
}
if (!ws) { console.log('SKIP pending.mjs · Chrome never opened a debug port'); process.exit(0); }
await new Promise(r => ws.on('open', r));

let id = 0; const waiters = new Map(); const evs = [];
ws.on('message', m => {
  const d = JSON.parse(m);
  if (d.id && waiters.has(d.id)) { waiters.get(d.id)(d.result); waiters.delete(d.id); }
  else if (d.method) evs.push(d);
});
const cmd = (method, params = {}) => new Promise(res => {
  const i = ++id; waiters.set(i, res); ws.send(JSON.stringify({ id: i, method, params }));
});

await cmd('Network.enable'); await cmd('Page.enable'); await cmd('Runtime.enable');

/* the page pane is the frame a reader is actually looking at, and the one whose
   scripts post to /_board/activity */
const page = await out(
  `ls "${process.env.HOME}/Desktop/Physician-SPACE${BOARD}"/*/[QS]*.html 2>/dev/null | head -1`);
const rel = page ? page.split('/board/')[1] : 'index.html';
const url = `${HOST}${BOARD}/${rel}${rel === 'index.html' ? '?pane=index' : '?pane=page'}`;

await cmd('Page.navigate', { url });
await new Promise(r => setTimeout(r, SETTLE_MS));

const sent = new Map(), done = new Set();
for (const e of evs) {
  if (e.method === 'Network.requestWillBeSent') sent.set(e.params.requestId, e.params.request.url);
  if (e.method === 'Network.loadingFinished' || e.method === 'Network.loadingFailed')
    done.add(e.params.requestId);
}
const stuck = [...sent].filter(([k]) => !done.has(k)).map(([, u]) => u.replace(HOST, ''));

const fail = [];
if (!sent.size) fail.push(`P1 the page issued no requests at all — ${url} is probably a 404`);
if (stuck.length) fail.push(`P2 still pending after ${SETTLE_MS / 1000}s: ${stuck.join(', ')}`);

/* and the endpoint that caused this, asked ten times at once the way ten tabs do */
const many = await cmd('Runtime.evaluate', {
  awaitPromise: true, returnByValue: true,
  expression: `(async () => { const t = performance.now();
    await Promise.all(Array.from({length:10}, () => fetch('/_board/activity', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({op:'stats', path:'${BOARD.replace(/\/board$/, '')}/board.md'}) })));
    return Math.round(performance.now() - t); })()`,
});
const ms = many.result?.value;
if (typeof ms !== 'number') fail.push('P3 ten concurrent /_board/activity posts did not all resolve');
else if (ms > 5000) fail.push(`P3 ten concurrent /_board/activity posts took ${ms} ms (ceiling 5000)`);

reap();
if (fail.length) { fail.forEach(f => console.log('FAIL ' + f)); process.exit(1); }
console.log(`PASS pending.mjs · ${sent.size} requests, none pending · 10x activity in ${ms} ms`);
process.exit(0);
