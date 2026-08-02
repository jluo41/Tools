/* QD5 gap checks — driven by checks/splitgaps.py, which owns the fixture,
   the server and the Chrome. See that file for what each G proves.

   Everything here writes or measures on a THROWAWAY board. G4 posts a real
   comment through the same endpoint the drawer and the terminal both use, so
   it must never be pointed at a board anyone reads.
*/
const HOSTPORT = process.env.CHECK_HOSTPORT;
const BOARD = process.env.CHECK_BOARD_URL || '/gapfixture';
const CDP = process.env.CHECK_CDP;
/* an ungrouped page lands in board/_ungrouped/ — the fixture declares no groups */
const PAGE = `${BOARD}/board/_ungrouped/QA1-thepage.html`;

const targets = await (await fetch(`http://${CDP}/json`)).json();
const target = targets.find(t => t.type === 'page');
const ws = new WebSocket(target.webSocketDebuggerUrl);
await new Promise(r => ws.addEventListener('open', r));
let id = 0; const waits = new Map();
ws.addEventListener('message', e => {
  const m = JSON.parse(e.data);
  if (m.id && waits.has(m.id)) { waits.get(m.id)(m); waits.delete(m.id); }
});
const send = (method, params = {}) =>
  new Promise(r => { const i = ++id; waits.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function ev(expr) {
  const r = await send('Runtime.evaluate',
    { expression: expr, awaitPromise: true, returnByValue: true });
  if (r.result?.exceptionDetails) return { __err: JSON.stringify(r.result.exceptionDetails.exception).slice(0, 200) };
  return r.result.result.value;
}
await send('Runtime.enable');

let pass = 0, fail = 0;
function ok(name, cond, got) {
  if (cond) { pass++; console.log(`  ✅ ${name}`); }
  else { fail++; console.log(`  ❌ ${name}${got === undefined ? '' : `  got: ${JSON.stringify(got)}`}`); }
}
const { execSync } = await import('node:child_process');
const rebuild = () => execSync(
  `${process.env.CHECK_PY} ${process.env.CHECK_SKILL}/cli/build.py ${process.env.CHECK_FIXTURE}`,
  { stdio: 'ignore' });

/* Go somewhere and do not return until THIS document is the one answering:
   the outgoing document is stamped, so the poll cannot be satisfied by the page
   we are leaving (the race that made splitshell.mjs fail in a new place on
   every run, 260801). */
async function goto(url, ready) {
  await ev(`window.__gone = 1`);
  await ev(`location.href='http://${HOSTPORT}${url}'`);
  for (let i = 0; i < 150; i++) {
    if (!await ev(`!!window.__gone`)) break;
    await sleep(100);
  }
  for (let i = 0; i < 150; i++) {
    if (await ev(ready)) return true;
    await sleep(100);
  }
  return false;
}

// ── G1 · the ordinary page is exactly as it was ────────────────────────────
console.log('G1 · an ordinary board page, opened on its own, is unchanged');
/* `?plain` NOW, because a bare board url opened in a browser is the split
   (260802). The opt-out is what this whole G is about: the one-document board
   has to be reachable and unchanged, and this is the address that reaches it. */
const PLAIN = PAGE + '?plain';
ok('the plain page loaded',
   await goto(PLAIN, `document.readyState === 'complete' && !!document.querySelector('div.wrap')`));
ok('no pane marker outside the shell',
   await ev(`typeof window.__boardPane`) === 'undefined');

/* the router: a click must SWAP, not navigate — the window survives */
await ev(`window.__alive = 1; 1`);
const href = await ev(`(function(){
  var a = [...document.querySelectorAll('.sidebar a[href$=".html"]')]
            .find(function(x){ return !/QA1-thepage/.test(x.getAttribute('href')) });
  if (!a) return null; a.click(); return a.getAttribute('href');
})()`);
await sleep(1500);
ok('there was a link to click', !!href, href);
ok('the router swapped instead of navigating (window survived)',
   await ev(`!!window.__alive`) === true);
/* any internal link proves the point; which one the rail offers first is not
   this check's business */
const moved = await ev(`location.pathname`);
ok('and the url moved anyway (pushState)', moved !== PAGE, moved);


/* live refresh: an edit must land IN PLACE, still without a reload */
await goto(PLAIN, `document.readyState === 'complete' && !!document.querySelector('div.wrap')`);
await ev(`window.__alive = 1; window.__upd = 0;
          window.addEventListener('board:updated', function(){ window.__upd++ }); 1`);
/* LET THE 4000 ms POLL TAKE ITS BASELINE FIRST. `20-live-refresh.js` records
   what it sees on its first tick, so an edit landing inside that first window
   is adopted as current and never reported — the ordinary page's own version
   of the race the panes were given `document.lastModified` to avoid. Waiting
   here measures the refresh rather than that race. */
await sleep(5000);
rebuild();
let updated = false;
for (let i = 0; i < 120; i++) {
  await sleep(250);
  if (await ev(`window.__upd > 0`) === true) { updated = true; break; }
}
ok('the ordinary page still refreshed itself', updated);
ok('and it did so WITHOUT a reload (window survived)',
   await ev(`!!window.__alive`) === true);

// ── G2 · a pane refresh keeps your place (A2.3) ────────────────────────────
console.log('G2 · a pane refresh keeps scroll and open sections');
const READY = `(function(){try{
  return ['index','page','chat'].every(function(n){
    return typeof frames[n].__boardPane === 'string' &&
           frames[n].document.readyState === 'complete' })
}catch(e){return false}})()`;
/* The side panes are hidden AND UNLOADED by default (260802), so a suite that
   wants three of them has to ask, the way a reader does. */
async function openSides() {
  for (let i = 0; i < 60; i++) {
    if (await ev(`!!document.getElementById('ti')`) === true) break;
    await sleep(100);
  }
  await ev(`document.getElementById('ti').click(); document.getElementById('mtui').click(); 1`);
  for (let i = 0; i < 150; i++) {
    if (await ev(READY) === true) return true;
    await sleep(100);
  }
  return false;
}
await goto(`${PAGE}?split`, `!!document.getElementById('split')`);
ok('the shell opened', await openSides());
const opened = await ev(`(function(){
  var d = frames.page.document.querySelector('div.wrap details');
  if (!d) return null;
  d.open = true;
  d.dispatchEvent(new Event('toggle'));
  var se = frames.page.document.scrollingElement || frames.page.document.documentElement;
  se.scrollTop = 900;
  frames.page.scrollTo(0, 900);
  return JSON.stringify({ sum: (d.querySelector('summary')||{}).textContent || 'a drawer',
                          y: Math.round(frames.page.scrollY || se.scrollTop),
                          h: se.scrollHeight, c: se.clientHeight });
})()`);
await sleep(900);                        // let 80-restore.js persist it
const O = JSON.parse(opened || '{}');
ok('a drawer was opened', !!O.sum, O);
ok('and the frame really scrolled (not a no-op)', O.y > 300, O);
const before = await ev(`frames.page.document.lastModified`);
rebuild();
let repainted = false;
for (let i = 0; i < 200; i++) {
  await sleep(100);
  const now = await ev(`(function(){try{return frames.page.document.lastModified}catch(e){return ''}})()`);
  if (now && now !== before) { repainted = true; break; }
}
await sleep(1200);                       // let the restore run
ok('the pane repainted', repainted);
const kept = await ev(`(function(){try{
  var d = frames.page.document.querySelector('div.wrap details');
  var se = frames.page.document.scrollingElement || frames.page.document.documentElement;
  return JSON.stringify({ open: !!(d && d.open),
                          y: Math.round(frames.page.scrollY || se.scrollTop) });
}catch(e){return '{}'}})()`);
const K = JSON.parse(kept || '{}');
ok('the open drawer came back', K.open === true, K);
ok('the scroll position came back', K.y > 300, K);

// ── G3 · a pane's page still reads with every script stripped (A3.3) ───────
console.log('G3 · the SERVED pane still reads with JS stripped');
for (const kind of ['page', 'index', 'chat']) {
  const html = await (await fetch(`http://${HOSTPORT}${PAGE}?pane=${kind}`)).text();
  const bare = html.replace(/<script[\s\S]*?<\/script>/g, '');
  const body = bare.split('<body')[1] || '';
  const plain = body.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
  ok(`pane=${kind} keeps its text with scripts stripped (${plain.length} chars)`,
     plain.length > 1200, plain.length);
}

// ── G4 · a write through the server repaints the pane (A3.1 · P1) ──────────
console.log('G4 · a comment written through the server repaints the page pane');
/* From a blank tab: the shell G2 just used still holds a terminal socket, and a
   browser has six connections per origin, so opening straight into a second
   shell measures that residue rather than the write (QD5 C4 P6). */
await ev(`location.href='about:blank'`);
await sleep(3000);
await goto(`${PAGE}?split`, `!!document.getElementById('split')`);
await openSides();
await sleep(1500);
await ev(`frames.chat.__mark = 1; frames.index.__mark = 1; 1`);
const was = await ev(`frames.page.document.lastModified`);
const stamp = 'gapcheck-' + id;
const posted = await ev(`fetch('/_board/comment', {
  method: 'POST', headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ path: '${BOARD}/board.md', file: 'QA1-thepage.md',
                         who: 'CC', sentence: 'The quick brown fox jumps over the lazy dog.',
                         text: ${JSON.stringify(stamp)} })
}).then(function(r){ return r.json() }).then(function(j){ return JSON.stringify(j).slice(0,200) })`);
ok('the server accepted the write', /"ok": ?true/.test(String(posted)), posted);
let landed = null;
const t0 = Date.now();
for (let i = 0; i < 300; i++) {
  await sleep(100);
  const now = await ev(`(function(){try{return frames.page.document.lastModified}catch(e){return ''}})()`);
  if (now && was && now !== was) { landed = Date.now() - t0; break; }
}
ok('the page pane repainted on that write', landed !== null, landed);
let shows = false;
for (let i = 0; i < 60; i++) {          // the reload we just detected is still landing
  await sleep(250);
  /* innerHTML, not innerText: a comment lands inside `<details class="sent">`
     which ships SHUT, and innerText does not see collapsed text. */
  shows = await ev(`(function(){try{
    return frames.page.document.body.innerHTML.indexOf(${JSON.stringify(stamp)}) > -1
  }catch(e){return false}})()`) === true;
  if (shows) break;
}
ok('and the comment is visible in the pane', shows === true);
ok('the CHAT frame was not touched by that write — the whole point',
   await ev(`!!frames.chat.__mark`) === true);
/* The index frame SHOULD refresh: a rebuild rewrites index.html, the rail's
   state markers move with it, and a stale rail is the thing A2.2 complains
   about. This asserts it happened, not that it was spared. */
ok('the index frame refreshed too, because the rail changed as well',
   await ev(`!!frames.index.__mark`) === false);

console.log(`\n${fail ? '❌' : '✅'} ${pass} passed · ${fail} failed`);
process.exit(fail ? 1 : 0);
