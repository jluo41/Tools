/* QD5 · the operating shell, driven in a real browser.

   Same harness shape as termnav.mjs: raw CDP over a WebSocket, no dependency.
   What it proves is the thing the page's Aims actually ask for — that the three
   panes are three DOCUMENTS, so an event in one cannot reach the others:

     T1  the shell serves three frames named index · page · chat
     T2  the panes know they are panes, and the router is off in all three
     T3  a click in the index pane navigates the PAGE frame, and neither the
         index frame nor the chat frame reloads          (A4.2)
     T4  the address bar follows the page frame           (A4.3)
     T5  a rebuild reloads the page frame within a second, and the chat frame
         survives it untouched                            (A2.1 · A3.1 · A3.2)
     T6  the chat pane opens the drawer on this page

   The survival tests plant a marker on each frame's `window` and check it is
   still there afterwards: a marker survives a reflow, and cannot survive a
   document reload. That is the difference this whole page is about.

   RUN IT AGAINST A CHROME OF ITS OWN, the way checks/run.py --full does for
   termnav.mjs. A shell leaves a terminal socket behind, and a browser allows
   six connections per origin, so re-running in a tab that held a shell moments
   ago measures that residue rather than the split (QD5 C4 P6).
*/
const HOSTPORT = process.env.CHECK_HOSTPORT || '127.0.0.1:5601';
const BOARD = process.env.CHECK_BOARD_URL
  || '/Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722';
const PAGE = `${BOARD}/board/QD/QD5-split-workspace.html`;
const CDP = process.env.CHECK_CDP || '127.0.0.1:9334';
const SHOT = process.env.CHECK_SHOT || '/tmp/qd5-split.png';

const targets = await (await fetch(`http://${CDP}/json`)).json();
const target = targets.find(t => t.type === 'page');
const ws = new WebSocket(target.webSocketDebuggerUrl);
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
async function ev(expr) {
  const r = await send('Runtime.evaluate',
    { expression: expr, awaitPromise: true, returnByValue: true });
  if (r.result?.exceptionDetails)
    throw new Error(JSON.stringify(r.result.exceptionDetails.exception));
  return r.result.result.value;
}
await send('Runtime.enable');

/* Wait for all three frames to be real documents rather than counting seconds:
   a pane is 150 KB and a fixed sleep turns a slow machine into a failing test. */
async function settled(ms = 15000) {
  const t0 = Date.now();
  while (Date.now() - t0 < ms) {
    const ok = await ev(`(function(){try{
      return ['index','page','chat'].every(function(n){
        var w = frames[n];
        /* Ask the PANE'S OWN MARKER, not the URL. A frame's location commits
           before its document does, so for about a second location already
           reads ?pane=chat while the window is still the placeholder, whose
           readyState is 'complete' too. Every readiness test built out of those
           two therefore passes on a document that has not run a line of the
           page's script, which is what made this suite fail in a different
           place on every run (measured 260801). __boardPane is set by the first
           thing in the served head, so it exists only in the real document. */
        return w && typeof w.__boardPane === 'string' && w.document.readyState === 'complete';
      });
    }catch(e){return false}})()`);
    if (ok) { await sleep(250); return true; }
    await sleep(200);
  }
  return false;
}

/* Wait for the page frame to actually BECOME something else. `settled()` alone
   is not enough right after a click: the old document is still 'complete' for
   the moment before the new one commits, so the poll returns on the document we
   were trying to leave and every later assertion reads the wrong frame. */
async function navigated(from, ms = 15000) {
  const t0 = Date.now();
  while (Date.now() - t0 < ms) {
    const now = await ev(`(function(){try{return frames.page.location.pathname}catch(e){return ''}})()`);
    if (now && now !== from) return await settled();
    await sleep(150);
  }
  return false;
}
async function pagePath() {
  return await ev(`(function(){try{return frames.page.location.pathname}catch(e){return ''}})()`);
}

/* Put the page frame on a named page and do not continue until it is THERE.
   Asking for a navigation and waiting for "something changed" is not the same
   claim, and the difference showed up as a test that sometimes measured the
   wrong document. Re-issued once, because a navigation racing an in-flight one
   is dropped by the browser rather than queued. */
async function goPage(path, ms = 15000) {
  const t0 = Date.now();
  let asked = 0;
  while (Date.now() - t0 < ms) {
    if (await pagePath() === path) return await settled();
    if (Date.now() - t0 > asked * 3000) {
      asked++;
      await ev(`frames.page.location.replace(${JSON.stringify(path + '?pane=page')})`);
    }
    await sleep(200);
  }
  return false;
}

let pass = 0, fail = 0;
function ok(name, cond, got) {
  if (cond) { pass++; console.log(`  ✅ ${name}`); }
  else { fail++; console.log(`  ❌ ${name}${got === undefined ? '' : `  got: ${JSON.stringify(got)}`}`); }
}

/* Open the shell on a page and do not return until THIS document is the one
   answering. Stamping the outgoing document is the whole trick: without it the
   poll is satisfied by the shell left over from the previous open — three .html
   frames, all 'complete' — and every later assertion reads a page on its way
   out, which is what made this suite's failures move around (260801). */
async function openShell(page) {
  await ev(`window.__gone = 1`);
  /* the page's OWN url, plus ?split — one url per page (260802) */
  await ev(`location.href='http://${HOSTPORT}${page}?split'`);
  for (let i = 0; i < 100; i++) {
    if (!await ev(`!!window.__gone`)) break;
    await sleep(100);
  }
  /* ASK FOR THE SIDE PANES. They are hidden AND UNLOADED by default now
     (260802), which is the whole point of that change: a page open pays for one
     document. Everything below tests three panes, so this suite opens them the
     way a reader does, with the two toggles. */
  for (let i = 0; i < 60; i++) {
    if (await ev(`!!document.getElementById('ti')`) === true) break;
    await sleep(100);
  }
  await ev(`document.getElementById('ti').click(); document.getElementById('mtui').click(); 1`);
  return await settled();
}

// ── T1 · three frames ──────────────────────────────────────────────────────
await send('Page.enable');
/* Start from a blank tab. A shell this suite opened moments ago still holds its
   stream and its terminal socket, and a browser has six per origin to spend, so
   running back-to-back would measure the residue of the previous run rather than
   the product. Leaving and pausing hands those back (P6). */
await ev(`location.href='about:blank'`);
await sleep(2500);
/* Stamp the CURRENT top document before navigating. Without this the poll below
   is satisfied by the shell left over from the previous run — three .html frames,
   all 'complete' — and every later assertion reads a page that is on its way out.
   That produced a suite whose failures moved around between runs (260801). */
await openShell(PAGE);
const frames = await ev(`JSON.stringify({
  n: window.frames.length,
  names: [...document.querySelectorAll('iframe')].map(f => f.name),
  index: frames.index.location.pathname + frames.index.location.search,
  page:  frames.page.location.pathname  + frames.page.location.search,
  chat:  frames.chat.location.pathname  + frames.chat.location.search
})`);
const F = JSON.parse(frames);
console.log('T1 · the shell serves three frames');
ok('three iframes', F.n === 3, F.n);
ok('named index · page · chat', F.names.join(',') === 'index,page,chat', F.names);
ok('index frame loads the board index', /\/board\/index\.html\?pane=index$/.test(F.index), F.index);
ok('page frame loads the page', F.page.endsWith('QD5-split-workspace.html?pane=page'), F.page);
ok('chat frame loads the same page as a chat pane', F.chat.endsWith('?pane=chat'), F.chat);

// ── T2 · the panes know they are panes ─────────────────────────────────────
const panes = await ev(`JSON.stringify({
  kinds: [frames.index.__boardPane, frames.page.__boardPane, frames.chat.__boardPane],
  base:  frames.index.document.querySelector('base') ? frames.index.document.querySelector('base').target : null,
  cls:   frames.page.document.body.className,
  rail:  (function(){var e=frames.index.document.querySelector('.sidebar');
          return e ? getComputedStyle(e).transform : 'MISSING'})(),
  wrap:  (function(){var e=frames.page.document.querySelector('div.wrap');
          return e ? getComputedStyle(e).display : 'MISSING'})()
})`);
const P = JSON.parse(panes);
console.log('T2 · every pane is marked, and the sidebar is open in its own frame');
ok('__boardPane set in all three', P.kinds.join(',') === 'index,page,chat', P.kinds);
ok('index frame carries <base target="page">', P.base === 'page', P.base);
ok('page frame body carries pane-page', /pane-page/.test(P.cls), P.cls);
ok('sidebar is untranslated (visible) in the index pane', P.rail !== 'matrix(1, 0, 0, 1, -238, 0)', P.rail);
ok('page pane still renders its wrap', P.wrap !== 'none', P.wrap);

// ── T3 · a click in the index pane moves ONLY the page frame ───────────────
console.log('T3 · a click in the index navigates the page frame alone');
await ev(`frames.index.__mark=1; frames.chat.__mark=1; frames.page.__mark=1; 1`);
const before = await pagePath();
const clicked = await ev(`(function(){
  var d = frames.index.document;
  var a = [...d.querySelectorAll('.sidebar a[href*=".html"]')]
            .find(x => !/QD5-split-workspace/.test(x.getAttribute('href')));
  if (!a) return null;
  var href = a.getAttribute('href');
  a.click();
  return href;
})()`);
await navigated(before);
const after = JSON.parse(await ev(`JSON.stringify({
  page: frames.page.location.pathname,
  pageMark: !!frames.page.__mark,
  indexMark: !!frames.index.__mark,
  chatMark: !!frames.chat.__mark,
  top: location.search
})`));
ok('the click had a target to hit', !!clicked, clicked);
ok('page frame navigated', !after.page.endsWith('QD5-split-workspace.html'), after.page);
/* INVERTED 260802, and the inversion is the point. This asserted `=== false`,
   meaning a sidebar click must produce a NEW document in the page frame, which
   was the design on 260801: the router returned early in every pane, so a click
   was a real frame load. That made every click re-parse the page and re-execute
   the whole bundle, JL felt it immediately ("really slow to click and go to a
   new page"), and `70-router.js` now keeps the router in the PAGE pane so a
   click swaps `div.wrap` instead. `__mark` surviving is the proof the document
   was never replaced, which is QD5's A3.1. The check outlived the ruling by one
   day and would have failed every run from here on. */
ok('page frame SWAPPED rather than reloaded', after.pageMark === true, after.pageMark);
ok('index frame did NOT reload', after.indexMark === true);
ok('chat frame did NOT reload', after.chatMark === true);

// ── T4 · the address bar follows the page frame ────────────────────────────
console.log('T4 · the address bar follows the page frame');
const bar = await ev(`location.pathname + location.search`);
/* BARE, because the split is what a bare board url opens as now (260802):
   the shell mirrors the page's own address and adds nothing to it. */
ok('the address bar IS the page url, bare', bar === after.page, bar);

/* Back to QD5 for the rest, through the product's own front door rather than by
   scripting the frame. VIA A BLANK TAB, for the same reason T1 starts there:
   this is the second shell of the run, and the first one still holds a terminal
   socket out of the browser's six per origin, so reopening straight into it
   measures that residue (C4 P6) instead of the refresh. Measured directly, a
   pane in a FIRST shell repaints 200 ms after a rebuild finishes; skipping this
   pause it can take tens of seconds, and T5 then reports a failure that is
   about the queue. */
await ev(`location.href='about:blank'`);
await sleep(3000);
await openShell(PAGE);

// ── T5 · a rebuild refreshes the page frame, and nothing else ─────────────
console.log('T5 · a rebuild reloads the page frame, and nothing else');
/* MEASURE THE DOCUMENT, NOT A MARKER WE PLANTED. A window marker is read
   through the parent's handle on the frame, and that handle is exactly what a
   navigation is busy replacing, so the read can answer from either side of the
   swap. The chat frame keeps a planted marker on purpose — nothing should
   reload it, so nothing can make that read ambiguous.

   `__paneStamp` and NOT `document.lastModified`: the pane's own stamp is the
   file's mtime in nanoseconds, which is what the product compares now, while
   `lastModified` is whole seconds. A rebuild landing in the same second as the
   page was served leaves those two strings identical, so this test reported a
   refresh that had plainly happened as a failure (260802). Measure what the
   feature measures. */
const docStamp = async () => await ev(
  `(function(){try{return frames.page.__paneStamp || frames.page.document.lastModified}catch(e){return ''}})()`);
await ev(`frames.chat.__mark = 1; frames.index.__mark = 1; 1`);
const was = await docStamp();
const t0 = Date.now();
process.stdout.write('  … rebuilding the board\n');
const { execSync } = await import('node:child_process');
execSync(`${process.env.CHECK_PY || 'python3'} ${process.env.CHECK_SKILL}/cli/build.py `
         + `${process.env.CHECK_ROOT}${BOARD}`, { stdio: 'ignore' });
let took = null;
for (let i = 0; i < 300; i++) {
  await sleep(100);
  const now = await docStamp();
  if (now && was && now !== was) { took = Date.now() - t0; break; }
}
await settled();      /* the reload we just measured is still landing */
const kept = JSON.parse(await ev(`JSON.stringify({
  chat: !!frames.chat.__mark, index: !!frames.index.__mark,
  page: (function(){try{return frames.page.location.pathname}catch(e){return ''}})()
})`));
if (took === null) console.log(`     was ${was}, still ${await docStamp()}`);
ok('page frame reloaded itself on the rebuild', took !== null, took);
/* NO TIMING ASSERTION HERE, on purpose. This is the SECOND shell of the run by
   construction — T1 to T4 opened one already — and the shell it replaced still
   holds a terminal socket out of the browser's six per origin, so what this
   measures is the residue of C4 P6, not the refresh: measured 260802 at 1.5 s
   in a first shell against ~14 s here, varying run to run. The refresh's own
   latency is asserted where it is clean, in checks/splitgaps.py G2, on a
   fixture with one shell and no terminal. Widening a bound until it passes
   would have turned a real, named cost into a number nobody trusts. */
console.log('     (took ' + took + ' ms — second shell in this tab, see C4 P6)');
ok('chat frame untouched by the page reload', kept.chat === true);
ok('page frame still shows the same page', /QD5-split-workspace/.test(kept.page), kept.page);

// ── T6 · the chat pane opened the drawer ───────────────────────────────────
console.log('T6 · the chat pane opens the drawer on this page');
/* The drawer opens through the server (it asks which sessions this page has),
   so it is a request-shaped event, not a paint. Reading it the instant a
   61-page rebuild finished measures the queue, not the feature. */
for (let i = 0; i < 60; i++) {
  if (await ev(`(function(){try{var c=frames.chat.document.getElementById('chat');
      return !!(c && c.classList.contains('on'))}catch(e){return false}})()`)) break;
  await sleep(250);
}
const chat = JSON.parse(await ev(`JSON.stringify({
  on: !!(frames.chat.document.getElementById('chat')||{classList:{contains:()=>false}}).classList.contains('on'),
  qid: (frames.chat.document.querySelector('#chat .qid')||{}).textContent || null,
  w: (frames.chat.document.getElementById('chat')||{}).clientWidth || 0,
  fw: frames.chat.innerWidth
})`));
ok('drawer is open in the chat frame', chat.on === true, chat);
ok('drawer fills the chat frame', chat.w > 0 && Math.abs(chat.w - chat.fw) < 4, chat);
ok('drawer is bound to a question', !!chat.qid, chat.qid);

const shot = await send('Page.captureScreenshot', { format: 'png' });
const fs = await import('node:fs');
fs.writeFileSync(SHOT, Buffer.from(shot.result.data, 'base64'));
console.log(`\n📸 ${SHOT}`);
if (errors.length) console.log('⚠️  page errors:\n   ' + errors.slice(0, 8).join('\n   '));
console.log(`\n${fail ? '❌' : '✅'} ${pass} passed · ${fail} failed`);
process.exit(fail ? 1 : 0);
