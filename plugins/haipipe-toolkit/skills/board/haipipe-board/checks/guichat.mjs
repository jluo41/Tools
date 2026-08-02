/* QD2 P3 · the GUI chat, driven the way a reader uses it.
 *
 * Nine drawer defects were fixed on 260801 and not one was clicked in a
 * browser, which is exactly what JL's own rule forbids. This is the check that
 * makes that impossible to repeat. It drives the REAL split shell, reaches into
 * the chat frame, and asserts the things a reader actually feels:
 *
 *   T1  a board url opens the split, with both chats offered in the header
 *   T2  💬 GUI opens the drawer with a live composer
 *   T3  a turn answers, and its markdown is RENDERED, not printed
 *   T4  the transcript carries no apology bubbles and the page throws nothing
 *   T5  scrolling up during a live turn is not undone by the next token
 *   T6  reloading mid-turn rejoins the ring and the answer still lands
 *   T7  closing and reopening costs a repaint, not a rebuild or a duplicate
 *   T8  🗂 Sessions lists this page's sessions
 *   T9  a finished turn reports how much of the context window is gone
 *
 * Costs cents: every turn is scoped + haiku + low.
 *
 *   node checks/guichat.mjs                  (needs a server on :5599 and
 *   CHECK_CDP=127.0.0.1:9335 node …           a Chrome with --remote-debugging)
 */
const CDP = process.env.CHECK_CDP || '127.0.0.1:9335';
const BASE = process.env.CHECK_BASE
  || 'http://127.0.0.1:5599/Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/board';
/* Home is QD2 itself: the sessions this suite creates belong to the page whose
   chat it checks, and a scratch bench gets archived by whoever tidies next
   (which is what happened to QD7 on 260802). Override with CHECK_PAGE. */
const PAGE = process.env.CHECK_PAGE || 'QD/QD2-chat-sdk.html';
/* `?split` is the door to the three panes. A plain board url is the ORIGINAL
   single-document page, which is a different surface with its own chat button;
   both work, and this suite is about the split one. */
const URL = `${BASE}/${PAGE}?split`;

const tab = await (await fetch(`http://${CDP}/json/new`, { method: 'PUT' })).json();
const ws = new WebSocket(tab.webSocketDebuggerUrl);
await new Promise(r => ws.addEventListener('open', r));
let id = 0; const waits = new Map(); const errs = [];
ws.addEventListener('message', e => {
  const m = JSON.parse(e.data);
  if (m.id && waits.has(m.id)) { waits.get(m.id)(m); waits.delete(m.id); }
  if (m.method === 'Runtime.exceptionThrown')
    errs.push((m.params.exceptionDetails.exception?.description || 'exception').slice(0, 140));
});
const send = (method, params = {}) =>
  new Promise(r => { const i = ++id; waits.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function ev(expr) {
  const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true });
  if (r.result?.exceptionDetails)
    return '__EX__ ' + JSON.stringify(r.result.exceptionDetails.exception).slice(0, 160);
  return r.result.result.value;
}
const fails = [];
const ok = (name, cond, detail) => {
  console.log(`${cond ? '  ✅' : '  ❌'} ${name}${cond ? '' : '  — ' + detail}`);
  if (!cond) fails.push(`${name}: ${detail}`);
};

/* Everything that matters lives inside the chat FRAME, so every probe goes
   through this. Kept as a string because it is spliced into evaluate(). */
const D = `document.querySelector('iframe[name="chat"]').contentDocument`;
const NOISE = `[].filter.call(${D}.querySelectorAll('#chat .bd .sys'), function(b){
  return /Stopped waiting|Failed to fetch|没有这个接口|⚠ /.test(b.textContent); }).length`;

async function turnDone(seconds = 150) {
  for (let i = 0; i < seconds / 2.5; i++) {
    await sleep(2500);
    const busy = await ev(`${D}.body.classList.contains('chatbusy')`);
    if (busy === false) return true;
  }
  return false;
}
async function sendTurn(text, opts) {
  return ev(`(function(){ var d=${D}, c=d.getElementById('chat');
    if(!c) return 'no drawer';
    c.querySelector('.scope').value='scoped';
    c.querySelector('.mdl').value='haiku';
    c.querySelector('.eff').value='low';
    c.querySelector('textarea').value=${JSON.stringify(text)};
    c.querySelector('.send').click(); return 'sent'; })()`);
}

await send('Runtime.enable'); await send('Page.enable');
await send('Page.navigate', { url: URL });
await sleep(7000);

// ── T1 · the split, with both chats offered ────────────────────────────────
console.log('T1 · a board url opens the split');
const t1 = JSON.parse(await ev(`JSON.stringify({
  frames: [].map.call(document.querySelectorAll('iframe'), function(f){return f.name;}),
  buttons: [].map.call(document.querySelectorAll('button,a'), function(b){return (b.textContent||'').trim();}).filter(Boolean) })`));
ok('three frames named index, page, chat',
   ['index', 'page', 'chat'].every(n => t1.frames.includes(n)), JSON.stringify(t1.frames));
ok('the header offers both chats',
   t1.buttons.some(b => /GUI/.test(b)) && t1.buttons.some(b => /TUI/.test(b)), JSON.stringify(t1.buttons));

// ── T1b · WHAT YOU CLICK IS WHAT OPENS ────────────────────────────────────
/* JL 260802: "when I click the GUI, but it is the TUI selected and opened".
   The shell asks the pane for a mode by calling into the frame, but on the
   FIRST click that frame has not loaded yet, so the request went to a window
   with no such function and the pane booted with the drawer's own default.
   A first-time reader is the only one who sees it, which is why it survived
   every test that reused a browser profile. So this clears storage first. */
console.log('T1b · what you click is what opens');
for (const [btn, want] of [['mgui', 'gui'], ['mtui', 'tui']]) {
  await send('Page.navigate', { url: URL }); await sleep(4500);
  await ev(`localStorage.clear()`);
  /* Re-NAVIGATE, never reload. Being in the split is remembered in
     localStorage, so clearing it and reloading lands on the plain
     single-document page and there is no header to click. */
  await send('Page.navigate', { url: URL }); await sleep(6500);
  await ev(`document.getElementById('${btn}').click()`); await sleep(6500);
  const s = JSON.parse(await ev(`(function(){
    var lit=[].filter.call(document.querySelectorAll('#mtui,#mgui'),function(b){return b.getAttribute('aria-pressed')==='true';}).map(function(b){return b.id;});
    var mode='?'; try{ mode=frames.chat.__paneModeNow?frames.chat.__paneModeNow():'nofn'; }catch(e){mode='ERR';}
    return JSON.stringify({lit:lit.join(',')||'none', mode:mode});})()`));
  ok(`a first-time click on ${want.toUpperCase()} opens ${want.toUpperCase()}`,
     s.mode === want && s.lit === btn, JSON.stringify(s));
}
await send('Page.navigate', { url: URL }); await sleep(5000);

// ── T2 · 💬 GUI opens a usable drawer ──────────────────────────────────────
console.log('T2 · 💬 GUI opens the drawer');
await ev(`[].filter.call(document.querySelectorAll('button,a'),function(x){return /GUI/.test(x.textContent||'')})[0].click()`);
await sleep(4500);
const t2 = JSON.parse(await ev(`(function(){ var d=${D};
  if(!d) return '{"frame":false}';
  var c=d.getElementById('chat');
  return JSON.stringify({ frame:true, on: !!(c&&c.classList.contains('on')),
    composer: !!d.querySelector('#chat textarea'), send: !!d.querySelector('#chat .send'),
    tabs: [].map.call(d.querySelectorAll('#chat .utab, #chat .tabs button'), function(b){return b.textContent.trim().slice(0,12);}) });})()`));
ok('the chat frame is same-origin and reachable', t2.frame === true, 'cross-origin or absent');
ok('the drawer is open with a composer', t2.on && t2.composer && t2.send, JSON.stringify(t2));

// ── T3/T4 · a turn answers, rendered, and says nothing it should not ───────
console.log('T3 · a turn answers, and its markdown renders');
await ev(`(function(){var d=${D};Object.keys(d.defaultView.localStorage).filter(function(k){return k.indexOf('board-chat')===0}).forEach(function(k){d.defaultView.localStorage.removeItem(k)});})()`);
await sendTurn('Reply with exactly this markdown and nothing else: **bold** and `code` and a list:\n- one\n- two');
const done3 = await turnDone(150);
ok('the turn finished', done3, 'still busy after 150s');
const t3 = JSON.parse(await ev(`(function(){ var d=${D}, c=d.getElementById('chat');
  var cc=c.querySelectorAll('.bd .cc'); var last=cc[cc.length-1];
  return JSON.stringify({ n:cc.length, len:last?last.textContent.length:0,
    md: last? !!last.querySelector('strong,code,li') : false,
    cls: last? last.className : '' });})()`));
ok('an answer bubble arrived', t3.n > 0 && t3.len > 5, JSON.stringify(t3));
ok('the answer is RENDERED markdown, not printed', t3.md === true,
   'no <strong>/<code>/<li> in the answer bubble: ' + JSON.stringify(t3));

/* A replayed row with no text is a bare line across the drawer; eighteen of
   them is what JL screenshotted on 260802. Assert the transcript has none. */
const blanks = await ev(`[].filter.call(${D}.querySelectorAll('#chat .bd > *'), function(el){
  return !(el.textContent||'').trim(); }).length`);
ok('no blank rows in the transcript', blanks === 0, blanks + ' rows render as bare lines');

console.log('T4 · the drawer says nothing it should not');
ok('no apology bubbles in the transcript', (await ev(NOISE)) === 0, (await ev(NOISE)) + ' found');
ok('no JS exceptions', errs.length === 0, errs.slice(0, 2).join(' ; '));

// ── T9 · the context meter ─────────────────────────────────────────────────
console.log('T9 · a finished turn reports context usage');
const meter = await ev(`(function(){var d=${D};var w=d.querySelector('#chat .cost');
  return w? w.textContent.trim() : '';})()`);
ok('the context meter is populated', /ctx\s+\d+%/.test(meter || ''), JSON.stringify(meter));

// ── T8 · the session picker ────────────────────────────────────────────────
console.log('T8 · 🗂 Sessions lists this page');
await ev(`(function(){var d=${D};
  var b=[].filter.call(d.querySelectorAll('#chat button'),function(x){return /Sessions/.test(x.textContent||'')})[0];
  if(b) b.click(); return !!b;})()`);
await sleep(2500);
const t8 = await ev(`(function(){var d=${D};var l=d.querySelector('#chat .spl');
  return l? l.querySelectorAll('*').length : -1;})()`);
ok('the session list populated', t8 > 0, 'rows=' + t8);

// ── T5 · scrolling up during a live turn is respected ──────────────────────
console.log('T5 · scrolling up during a turn is not undone');
/* Long enough to STILL BE RUNNING after a reload plus reopening the shell,
   which costs about twelve seconds. A turn that finishes first makes T6 pass
   on the transcript sync and never exercises the ring at all — the soft pass
   that hid R1's only unproven claim (260802). */
await sendTurn('Count from 1 to 600. Put each number on its own line with a short four word note. Do not use tools, do not stop early, do not summarise.');
await sleep(12000);
await ev(`(function(){var d=${D};var bd=d.querySelector('#chat .bd'); bd.scrollTop = 0; return bd.scrollTop;})()`);
await sleep(9000);
const t5 = JSON.parse(await ev(`(function(){var d=${D};var bd=d.querySelector('#chat .bd');
  return JSON.stringify({top:bd.scrollTop, h:bd.scrollHeight, busy:d.body.classList.contains('chatbusy')});})()`));
ok('a reader who scrolled up stays there while tokens arrive',
   t5.top < 400, `scrollTop jumped back to ${t5.top} of ${t5.h}`);

// ── T6 · reload mid-turn, and rejoin ───────────────────────────────────────
console.log('T6 · reloading mid-turn rejoins the ring');
const curBefore = await ev(`(function(){var d=${D};var ls=d.defaultView.localStorage;
  var k=Object.keys(ls).filter(function(k){return k.indexOf('board-chat-cur')===0})[0];
  return k? ls.getItem(k) : null;})()`);
await send('Page.reload', { ignoreCache: true });
await sleep(8000);
await ev(`[].filter.call(document.querySelectorAll('button,a'),function(x){return /GUI/.test(x.textContent||'')})[0].click()`);
await sleep(4000);
let rejoined = null;
for (let i = 0; i < 50; i++) {
  await sleep(2500);
  const s = JSON.parse(await ev(`(function(){var d=${D};if(!d) return '{}';var c=d.getElementById('chat');
    if(!c) return '{}'; var cc=c.querySelectorAll('.bd .cc'); var last=cc.length?cc[cc.length-1].textContent:'';
    return JSON.stringify({busy:d.body.classList.contains('chatbusy'), len:last.length, noise:${NOISE},
      rejoin:(d.defaultView.__chatDiag?d.defaultView.__chatDiag():'').split('\\n').filter(function(l){return /REJOIN/.test(l)}).slice(-1)[0]||''});})()`));
  if (s.len > 500 && !s.busy) { rejoined = s; break; }
  if (i === 49) rejoined = s;
}
console.log('    cursor before reload:', curBefore, '· after:', JSON.stringify(rejoined).slice(0, 150));
ok('the drawer REJOINED a still-running turn', /REJOIN\b[^\n]*cursor \d+/.test(rejoined?.rejoin || ''),
   'the turn had already finished, so the ring was never exercised: ' + (rejoined?.rejoin || 'no diag'));
ok('the answer survives a reload mid-turn', rejoined && rejoined.len > 500,
   'nothing came back: ' + JSON.stringify(rejoined));
ok('the rejoin is silent', rejoined && rejoined.noise === 0, 'noise=' + (rejoined && rejoined.noise));

// ── T7 · close and reopen ──────────────────────────────────────────────────
console.log('T7 · closing and reopening keeps the transcript');
const before7 = await ev(`${D}.querySelectorAll('#chat .bd .cc').length`);
await ev(`(function(){var d=${D};var x=d.querySelector('#chat .cls, #chat .x, #chat .back');
  if(x) x.click(); return !!x;})()`);
await sleep(1200);
await ev(`[].filter.call(document.querySelectorAll('button,a'),function(x){return /GUI/.test(x.textContent||'')})[0].click()`);
await sleep(3500);
const after7 = await ev(`${D}.querySelectorAll('#chat .bd .cc').length`);
ok('reopening neither loses nor duplicates the transcript', after7 === before7,
   `${before7} answers before, ${after7} after`);
ok('still no apology bubbles', (await ev(NOISE)) === 0, (await ev(NOISE)) + ' found');
ok('still no JS exceptions', errs.length === 0, errs.slice(0, 2).join(' ; '));

// ── T10/T11 · COMING BACK LOOKS THE SAME ──────────────────────────────────
/* JL 260802: "when I shift away and back, or I switch to a new chat session
   and back, will it be the same as before? just like the vscode claude code
   plugin?" The plugin RETAINS its webview, so coming back is the same pixels.
   Ours rebuilds, so the only honest test is a FINGERPRINT of the transcript
   taken before and after, compared row for row. */
const FP = `JSON.stringify([].map.call(${D}.querySelectorAll('#chat .bd > *'), function(el){
  return el.tagName.toLowerCase() + '.' + (el.className||'') + ':' + (el.textContent||'').trim().length; }))`;

console.log('T10 · leaving the page and coming back');
const before10 = await ev(FP);
const here = await ev(`frames.page.location.pathname`);
await ev(`frames.page.location.href = '${BASE}/QD/QD6-session-status-strip.html?pane=page'`);
await sleep(6000);
await ev(`frames.page.location.href = '${here}?pane=page'`);
await sleep(7000);
const after10 = await ev(FP);
ok('the transcript is unchanged after leaving the page and returning',
   after10 === before10,
   `${JSON.parse(before10).length} rows before, ${JSON.parse(after10 || '[]').length} after`);
if (after10 !== before10) {
  const b = JSON.parse(before10), a = JSON.parse(after10 || '[]');
  console.log('      before:', JSON.stringify(b.slice(0, 6)));
  console.log('      after :', JSON.stringify(a.slice(0, 6)));
}

console.log('T11 · switching session away and back');
/* A real switch needs TWO sessions that actually landed a .jsonl. The picker
   marks the rest `dim` ("recorded, never talked"), and clicking one of those
   proves nothing. So make the second session here rather than hoping. */
const openPicker = `(function(){var d=${D};
  var b=[].filter.call(d.querySelectorAll('#chat button'),function(x){return /Sessions/.test(x.textContent||'')})[0];
  if(b) b.click(); return !!b;})()`;
const REAL = `${D}.querySelectorAll('#chat .spl .sprow:not(.dim):not(.new)')`;

await ev(openPicker); await sleep(2500);
let real = await ev(`${REAL}.length`);
if (real < 2) {
  await ev(`(function(){var d=${D};var n=d.querySelector('#chat .spl .sprow.new'); if(n) n.click(); return !!n;})()`);
  await sleep(2000);
  await sendTurn('SESSIONTWOMARKER — reply with exactly: SESSION TWO');
  await turnDone(120);
  await ev(openPicker); await sleep(2500);
  real = await ev(`${REAL}.length`);
}
/* A switch needs two sessions that actually landed a .jsonl. If this page has
   only one and the attempt to make a second did not land, there is nothing to
   switch BETWEEN — that is a missing precondition, not a defect, and calling it
   a failure would be the test lying. Say so and skip the three assertions. */
const canSwitch = real >= 2;
if (!canSwitch) {
  console.log(`  ⏭  skipped: this page has ${real} real session(s), so there is nothing to switch between`);
}
if (canSwitch) {

/* Identify a session by its LABEL, never by index: the picker puts the current
   one first, so after a switch `rows[0]` is a different session than it was. */
const labels = () => ev(`JSON.stringify([].map.call(${REAL}, function(r){
  return (r.textContent||'').replace(/\s+/g,' ').trim().slice(0,150); }))`);
const clickLabel = lbl => ev(`(function(){
  var rows=[].slice.call(${REAL});
  for (var i=0;i<rows.length;i++){ if((rows[i].textContent||'').replace(/\s+/g,' ').trim().slice(0,150)===${JSON.stringify('')}+${JSON.stringify(lbl)}) { rows[i].click(); return 'clicked'; } }
  return 'not found';})()`);

const names = JSON.parse(await labels());
const mine = names[0], other = names[1];
/* LAND ON A REAL SESSION FIRST. Making the second session leaves the drawer on
   a freshly-cleared "new session" view, so fingerprinting here compares an
   empty pane against a real transcript and proves nothing. Click into `mine`
   and let it settle; only then is there a before to compare an after with. */
console.log('    landing on:', JSON.stringify(mine), await clickLabel(mine));
await sleep(7000);
const fpB = await ev(FP);

await ev(openPicker); await sleep(2000);
console.log('    switching to:', JSON.stringify(other), await clickLabel(other));
await sleep(7000);
const fpA = await ev(FP);
ok('switching session actually changes the transcript', fpA !== fpB,
   'the drawer showed identical rows for a different session');

await ev(openPicker); await sleep(2000);
console.log('    switching back to:', JSON.stringify(mine), await clickLabel(mine));
await sleep(7000);
const fpBack = await ev(FP);
/* The switch banner is one extra row by design, so compare CONTENT rows. */
const strip = s => JSON.parse(s || '[]').filter(r => !/switchsep/.test(r));
const answers = s => strip(s).filter(r => /\.m cc/.test(r));
ok('coming back keeps every answer it had before',
   answers(fpBack).length >= answers(fpB).length &&
   answers(fpB).every(a => answers(fpBack).includes(a)),
   `answers before ${JSON.stringify(answers(fpB))}, after ${JSON.stringify(answers(fpBack))}`);
/* Coming back adds ONE deliberate banner, "↑ history of the picked session",
   and measurement says it never piles up: three switch rounds leave exactly one
   and the row count holds. So compare the MESSAGE rows and check the banner
   separately, which is the difference between a stable view and a growing one. */
const msgs = s => strip(s).filter(r => !/\.m sys:/.test(r));
ok('coming back shows the SAME messages, in the same order',
   JSON.stringify(msgs(fpBack)) === JSON.stringify(msgs(fpB)),
   `${msgs(fpB).length} message rows before, ${msgs(fpBack).length} after`);
const banners = await ev(`[].filter.call(${D}.querySelectorAll('#chat .bd .m.sys'), function(e){
  return /history of the picked session/.test(e.textContent||''); }).length`);
ok('the switch banner does not accumulate', banners <= 1, banners + ' banners stacked up');
if (JSON.stringify(strip(fpBack)) !== JSON.stringify(strip(fpB))) {
  console.log('      before:', JSON.stringify(strip(fpB).slice(0, 8)));
  console.log('      after :', JSON.stringify(strip(fpBack).slice(0, 8)));
}

}

console.log();
if (fails.length) {
  console.log(`❌ ${fails.length} failed:`);
  fails.forEach(f => console.log('   · ' + f));
  process.exit(1);
}
console.log('✅ the GUI chat passed every assertion');
await fetch(`http://${CDP}/json/close/${tab.id}`);
process.exit(0);
