/* QD3 · the TUI chat, driven the way a reader uses it.
 *
 * `checks/guichat.mjs` covers the drawn chat and the handover between the two.
 * This covers the terminal's own half, which nothing asserted before:
 *
 *   U1  >_ TUI Chat opens a REAL terminal, attached to this question
 *   U2  what you type reaches the shell and its output comes back
 *   U3  moving the page pane does not disturb the terminal
 *   U4  reloading the whole shell PARKS the PTY; the session comes back
 *   U5  the terminal throws nothing while any of that happens
 *
 * Costs nothing: it runs `echo`, never a model turn.
 *
 *   node checks/tuichat.mjs      (server on :5599, Chrome with --remote-debugging)
 */
const CDP = process.env.CHECK_CDP || '127.0.0.1:9335';
const BASE = process.env.CHECK_BASE
  || 'http://127.0.0.1:5599/Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/board';
const PAGE = process.env.CHECK_PAGE || 'QD/QD3-chat-terminal.html';
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
const ev = async x => {
  const r = await send('Runtime.evaluate', { expression: x, awaitPromise: true, returnByValue: true });
  return r.result?.exceptionDetails ? '__EX__ ' + JSON.stringify(r.result.exceptionDetails.exception).slice(0, 160)
                                    : r.result.result.value;
};
const fails = [];
const ok = (n, c, d) => { console.log(`${c ? '  ✅' : '  ❌'} ${n}${c ? '' : '  — ' + d}`); if (!c) fails.push(`${n}: ${d}`); };
const W = `document.querySelector('iframe[name="chat"]').contentWindow`;
/* xterm keeps its own buffer; read it rather than the DOM, which only holds
   the rows currently painted. */
const SCREEN = `(function(){ try{ var t=${W}.__boardTerm; if(!t||!t.buffer) return '';
  var b=t.buffer.active, out=[];
  for (var i=0;i<b.length;i++){ var l=b.getLine(i); if(l) out.push(l.translateToString(true)); }
  return out.join('\\n'); }catch(e){ return '__ERR__'+e.message; } })()`;

await send('Runtime.enable'); await send('Page.enable');
await send('Page.navigate', { url: URL }); await sleep(7000);

// ── U1 ────────────────────────────────────────────────────────────────────
console.log('U1 · >_ TUI Chat opens a real terminal');
/* CLICK IT ONLY IF IT IS NOT ALREADY LIT. The two strip buttons are a radio
   with an OFF position: clicking the lit one PUTS THE CHAT AWAY. A previous
   run can leave `board-split-chat` set to shown, so an unconditional click
   closed the pane instead of opening it — which is what made this suite look
   like a non-deterministic terminal reattach, roughly half the runs, for
   hours (260802). The product was right; the test was toggling. */
await ev(`(function(){var b=document.getElementById('mtui');
  if (b.getAttribute('aria-pressed') !== 'true') b.click();
  return b.getAttribute('aria-pressed');})()`);
let up = false;
for (let i = 0; i < 24; i++) {
  await sleep(2500);
  if (await ev(`(function(){try{return !!${W}.__boardTerm;}catch(e){return false;}})()`) === true) { up = true; break; }
}
ok('a terminal exists in the chat pane', up, 'no xterm after 60s');
ok('the pane reports it is in TUI mode',
   (await ev(`(function(){try{return ${W}.__paneModeNow();}catch(e){return 'ERR';}})()`)) === 'tui', 'not tui');

// ── U2 ────────────────────────────────────────────────────────────────────
console.log('U2 · typing reaches the shell and output comes back');
const MARK = 'TUIOK' + Math.floor(Date.now() / 1000 % 100000);
await ev(`(function(){ try { ${W}.__boardTermType('echo ${MARK}', {enter:true}); return 1; }
  catch(e){ return 'EX '+e.message; } })()`);
let saw = false, screen = '';
for (let i = 0; i < 20; i++) {
  await sleep(2000);
  screen = await ev(SCREEN);
  if (typeof screen === 'string' && screen.indexOf(MARK) >= 0) { saw = true; break; }
}
ok('what you type runs, and its output comes back', saw,
   'never saw ' + MARK + ' on screen; tail=' + String(screen).slice(-120));

// ── U3 ────────────────────────────────────────────────────────────────────
console.log('U3 · moving the page pane leaves the terminal alone');
await ev(`frames.page.location.href='${BASE}/QD/QD6-session-status-strip.html?pane=page'`);
await sleep(6000);
const alive3 = await ev(`(function(){try{return !!${W}.__boardTerm && ${W}.__boardTermOn();}catch(e){return false;}})()`);
const kept3 = (await ev(SCREEN) || '').indexOf(MARK) >= 0;
ok('the terminal survives a page-pane navigation', alive3 === true, 'terminal gone');
ok('its scrollback is untouched', kept3, 'the earlier output disappeared');

// ── U4 ────────────────────────────────────────────────────────────────────
console.log('U4 · reloading the shell parks the PTY and comes back');
/* PUT THE PAGE FRAME BACK FIRST. U3 navigated it, and the shell mirrors the
   page frame's path into its own address (QD5 A4.3), so reloading now would
   load the shell showing the OTHER page and bind the terminal to that page's
   key — a different terminal, correctly. Asserting sameness across that is the
   test lying, which it did once (260802). */
await ev(`frames.page.location.href='${BASE}/${PAGE}?pane=page'`);
await sleep(6000);
const keyBefore = await ev(`(function(){try{return (${W}.__boardTermKeyNow&&${W}.__boardTermKeyNow())||'';}catch(e){return '';}})()`);
await send('Page.reload', { ignoreCache: true }); await sleep(9000);
let back = false;
for (let i = 0; i < 24; i++) {
  await sleep(2500);
  if (await ev(`(function(){try{return !!${W}.__boardTerm;}catch(e){return false;}})()`) === true) { back = true; break; }
}
/* THE RIGHT PROPERTY IS THE SESSION, NOT THE PIXELS. I first asserted that the
   pre-reload output must still be on screen, saw it absent, and reported the
   terminal as coming back EMPTY. Measured properly it is not: the terminal key
   is IDENTICAL either side of a full reload (1c87f5ece80e both times) and the
   ring replays over a thousand characters. The earlier `echo` is gone from the
   VISIBLE screen because the CLI running inside repaints it, which is what a
   full-screen app does on reconnect. So assert what parking actually promises:
   the same terminal, with content. */
const key4 = await ev(`(function(){try{return (${W}.__boardTermKeyNow&&${W}.__boardTermKeyNow())||'';}catch(e){return '';}})()`);
const chars4 = (await ev(SCREEN) || '').replace(/\s/g, '').length;
/* ASSERTED NOW. This read as non-deterministic for hours and was not: Three outcomes
   the suite was clicking `>_ TUI` unconditionally, and the strip's buttons are
   a radio with an OFF position, so clicking the lit one PUT THE CHAT AWAY.
   Whether it was already lit depended on the previous run's storage, which is
   where the coin-flip came from. Click-only-if-not-lit: four runs, four times
   the same terminal back with its ring. */
console.log(`      back=${back} · key ${keyBefore || '?'} → ${key4 || '(none)'} · ${chars4} chars`);
ok('the terminal comes back after a full reload', back, 'no terminal after 60s');
ok('and it is the SAME terminal, not a fresh one', key4 === keyBefore && !!key4,
   `key was ${keyBefore}, now ${key4}`);
ok('with its screen replayed from the ring', chars4 > 100, chars4 + ' chars on screen');
const kept4 = false;
/* superseded, kept for the note below. `QD3` parks the PTY on a
   reload and `term.py` replays its ring on reconnect, so the session should
   come back with its scrollback. Measured 260802 across runs it is NOT
   reliable: sometimes the terminal returns empty, sometimes it does not return
   inside 60s. Asserting it would give a flaky red that teaches nothing; not
   saying it would hide a real edge. So the suite states what it saw and the
   defect lives on QD3 as an Aim. */


// ── U5 ────────────────────────────────────────────────────────────────────
ok('nothing threw while doing all of that', errs.length === 0, errs.slice(0, 2).join(' ; '));

console.log();
if (fails.length) { console.log(`❌ ${fails.length} failed:`); fails.forEach(f => console.log('   · ' + f)); process.exit(1); }
console.log('✅ the TUI chat passed every assertion');
await fetch(`http://${CDP}/json/close/${tab.id}`);
process.exit(0);
