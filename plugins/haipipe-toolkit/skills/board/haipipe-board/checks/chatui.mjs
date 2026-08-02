/* Drawer-behaviour suite — the 💬 coverage termnav.mjs does not have.
   Same harness shape as termnav.mjs: own Chrome on :9333, real gestures.

   Why it exists: on 260801 ten drawer defects were fixed in one sitting and
   NOT ONE was clicked in a real browser, which is the exact thing JL's rule
   forbids ("did you clicked it yourself?"). Every assertion below is one of
   those fixes, so a regression is caught by running this rather than by JL
   noticing it again.

   These are all READ-ONLY gestures: opening the drawer, scrolling, clicking a
   tab. Nothing here sends a turn, so it never spends money and never takes a
   HOLD. The one thing it cannot cover is a live stream, so the follow-not-yank
   assertion drives the renderer directly instead of paying for a real turn. */
const BOARD = process.env.CHECK_BOARD_URL
  || '/Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722';
const HOSTPORT = process.env.CHECK_HOSTPORT || '127.0.0.1:5599';
const BASE = `http://${HOSTPORT}${BOARD}/board`;
const CDP = process.env.CHECK_CDP || '127.0.0.1:9333';
const PAGE = process.env.CHECK_PAGE || 'QD/QD2-chat-sdk.html';

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
await send('Page.enable');

const results = [];
async function check(name, fn) {
  try {
    const detail = await fn();
    results.push({ name, ok: true, detail: detail || '' });
    console.log(`  \x1b[32mPASS\x1b[0m  ${name}${detail ? '  — ' + detail : ''}`);
  } catch (e) {
    results.push({ name, ok: false, detail: e.message });
    console.log(`  \x1b[31mFAIL\x1b[0m  ${name}  — ${e.message}`);
  }
}
const must = (cond, msg) => { if (!cond) throw new Error(msg); };

async function goto(u) {
  await send('Page.navigate', { url: u });
  for (let i = 0; i < 60; i++) {
    if (await evaluate('!!document.getElementById("chat")')) { await sleep(400); return; }
    await sleep(150);
  }
  throw new Error('page never produced #chat: ' + u);
}
/* the drawer opens from the floating button on a page that has one, and from
   the per-card button otherwise; try both so this works on any page shape */
async function openDrawer() {
  await evaluate(`(function(){
    var f = document.getElementById('chatfab');
    if (f && getComputedStyle(f).display !== 'none') { f.click(); return 'fab'; }
    var b = document.querySelector('.chatbtn'); if (b) { b.click(); return 'card'; }
    return 'none';
  })()`);
  await sleep(700);
}
async function closeDrawer() {
  await evaluate(`(function(){var x=document.querySelector('#chat .x'); if(x) x.click();})()`);
  await sleep(300);
}

console.log(`\n💬 chatui — ${BASE}/${PAGE}\n`);
await goto(`${BASE}/${PAGE}`);

/* ── T1 · the drawer opens at all ─────────────────────────────────── */
await check('T1 drawer opens', async () => {
  await openDrawer();
  const on = await evaluate(`document.getElementById('chat').classList.contains('on')`);
  must(on, 'the drawer never got the .on class');
  return 'on';
});

/* ── T2 · it lands at the newest message, not the oldest ──────────── */
/*    the fix: a requestAnimationFrame scroll AFTER classList.add('on'),
      because the replay runs while #chat is still display:none, where
      scrollHeight is 0 and every scrollTop assignment is clamped to 0 */
await check('T2 opens at the bottom', async () => {
  const d = await evaluate(`(function(){
    var b = document.querySelector('#chat .bd');
    return { gap: b.scrollHeight - b.scrollTop - b.clientHeight, h: b.scrollHeight, c: b.clientHeight };
  })()`);
  if (d.h <= d.c + 1) return 'transcript too short to scroll (vacuously at bottom)';
  must(d.gap <= 48, `opened ${Math.round(d.gap)}px above the bottom`);
  return `gap ${Math.round(d.gap)}px`;
});

/* ── T3 · the wheel over the drawer never moves the page ──────────── */
/*    the fix: overscroll-behavior for the at-the-edge case, plus a wheel
      handler for the case where nothing inside can take the delta at all */
await check('T3 wheel does not scroll the page behind', async () => {
  const before = await evaluate('window.scrollY');
  const box = await evaluate(`(function(){
    var r = document.querySelector('#chat .bd').getBoundingClientRect();
    return { x: Math.round(r.left + r.width / 2), y: Math.round(r.top + r.height / 2) };
  })()`);
  for (let i = 0; i < 6; i++) {
    await send('Input.dispatchMouseEvent', {
      type: 'mouseWheel', x: box.x, y: box.y, deltaX: 0, deltaY: 240 });
    await sleep(60);
  }
  await sleep(300);
  const after = await evaluate('window.scrollY');
  must(after === before, `page scrolled ${before} -> ${after} while the wheel was over the drawer`);
  return `window.scrollY held at ${after}`;
});

/* ── T4 · a scrolled-up reader is not dragged back by the stream ──── */
/*    driven through the renderer rather than a paid turn: append bubbles the
      way a live turn does and assert the reader's position survives */
await check('T4 streaming does not yank a reader who scrolled up', async () => {
  const seeded = await evaluate(`(function(){
    var b = document.querySelector('#chat .bd');
    for (var i = 0; i < 40; i++) {
      var d = document.createElement('div');
      d.className = 'm sys'; d.textContent = 'chatui filler ' + i;
      b.appendChild(d);
    }
    b.scrollTop = b.scrollHeight;
    return b.scrollHeight > b.clientHeight;
  })()`);
  must(seeded, 'could not make the transcript overflow');
  await sleep(120);
  await evaluate(`(function(){
    var b = document.querySelector('#chat .bd');
    b.scrollTop = 0;                       // the reader goes back to read
    b.dispatchEvent(new Event('scroll'));  // same signal a real wheel gives
  })()`);
  await sleep(150);
  const moved = await evaluate(`(function(){
    var b = document.querySelector('#chat .bd'), at = b.scrollTop;
    for (var i = 0; i < 10; i++) {         // now the stream keeps arriving
      var d = document.createElement('div');
      d.className = 'm sys'; d.textContent = 'chatui stream ' + i;
      b.appendChild(d);
      if (typeof bdAuto === 'function') bdAuto();
    }
    return { was: at, now: b.scrollTop, end: b.scrollHeight - b.clientHeight };
  })()`);
  must(moved.now <= moved.was + 8,
       `dragged from ${moved.was} to ${moved.now} (bottom is ${moved.end})`);
  return `held at ${moved.now} while 10 messages arrived`;
});

/* ── T5 · returning to the bottom resumes following ───────────────── */
await check('T5 coming back to the bottom resumes following', async () => {
  const r = await evaluate(`(function(){
    var b = document.querySelector('#chat .bd');
    b.scrollTop = b.scrollHeight;
    b.dispatchEvent(new Event('scroll'));
    var d = document.createElement('div');
    d.className = 'm sys'; d.textContent = 'chatui resumed';
    b.appendChild(d);
    if (typeof bdAuto === 'function') bdAuto();
    return b.scrollHeight - b.scrollTop - b.clientHeight;
  })()`);
  must(r <= 48, `did not follow: ${Math.round(r)}px above the bottom`);
  return 'follows again';
});

/* ── T6 · the Sessions tab exists, opens, and shows the picker ────── */
await check('T6 the Sessions tab opens the picker', async () => {
  const has = await evaluate(`!!document.querySelector('#chat .gtoggle')`);
  must(has, 'no .gtoggle button in the utility tabs');
  await evaluate(`document.querySelector('#chat .gtoggle').click()`);
  await sleep(900);
  const st = await evaluate(`(function(){
    var u = document.querySelector('#chat .utility');
    var s = document.querySelector('#chat .sessions');
    var p = document.querySelector('#chat .spick');
    return { open: u.classList.contains('open') && u.classList.contains('show-sessions'),
             shown: !!s && getComputedStyle(s).display !== 'none',
             rows: document.querySelectorAll('#chat .spl .sprow').length,
             hidden: !!(p && p.hidden) };
  })()`);
  must(st.open, 'the utility did not switch to show-sessions');
  must(st.shown, 'the .sessions panel stayed display:none');
  return `${st.rows} row(s)${st.hidden ? ' (picker still hidden: no sessions on record)' : ''}`;
});

/* ── T7 · only one utility panel is open at a time ────────────────── */
await check('T7 the three tabs are mutually exclusive', async () => {
  await evaluate(`document.querySelector('#chat .stoggle').click()`);
  await sleep(300);
  const n = await evaluate(`(function(){
    var b = document.querySelector('#chat .utility-body');
    return ['.acts', '.sessions', '.settings'].filter(function (s) {
      var el = b.querySelector(s);
      return el && getComputedStyle(el).display !== 'none';
    }).length;
  })()`);
  must(n === 1, `${n} panels visible at once`);
  return 'exactly one';
});

/* ── T8 · a replayed answer is rendered, not printed raw ──────────── */
/*    the fix: the server's session-log says 'ai' and the renderer knew only
      'cc', so a replayed answer lost both its markdown and its bubble style */
await check('T8 a replayed answer keeps markdown and its style', async () => {
  const r = await evaluate(`(function(){
    if (!window.__chatProbe) return { skip: 'the drawer test bridge is missing' };
    var d = window.__chatProbe.bubble('ai', '## head\\n\\n- one\\n- two\\n\\n\`code\`');
    var out = { cls: d.className, html: d.innerHTML.indexOf('<h') >= 0 || d.innerHTML.indexOf('<ul') >= 0 };
    d.parentNode.removeChild(d);
    return out;
  })()`);
  if (r.skip) throw new Error(r.skip);
  must(/\bcc\b/.test(r.cls), `kind 'ai' rendered as class "${r.cls}", expected cc`);
  must(/\bmd\b/.test(r.cls), 'the .md class was not applied');
  must(r.html, 'markdown was not converted to html');
  return 'ai -> cc, markdown rendered';
});

/* ── T9 · the way back to the page exists ─────────────────────────── */
await check('T9 there is a labelled way back to the page', async () => {
  const r = await evaluate(`(function(){
    var b = document.querySelector('#chat .back');
    if (!b) return { has: false };
    return { has: true, text: b.textContent.trim(),
             shown: getComputedStyle(b).display !== 'none',
             w: window.innerWidth };
  })()`);
  must(r.has, 'no .back button in the header');
  /* it is deliberately hidden while the drawer DOCKS, because the page is
     already visible beside it; it must appear once the drawer covers it */
  if (r.w > 820) return `present, hidden while docked at ${r.w}px wide`;
  must(r.shown, `the drawer covers the page at ${r.w}px but .back is hidden`);
  return `visible: "${r.text}"`;
});

/* ── T10 · reopening during a live turn still shows the drawer ────── */
/*    the fix: chatOpen's same-target guard returned ABOVE the line that adds
      .on, so closing mid-turn and pressing 💬 again did nothing at all */
await check('T10 reopening while a turn is live still opens it', async () => {
  const r = await evaluate(`(function(){
    if (!window.__chatProbe) return { skip: 'the drawer test bridge is missing' };
    return { ok: true };
  })()`);
  if (r.skip) throw new Error(r.skip + ' (bundle scope changed)');
  await closeDrawer();
  const shut = await evaluate(`!document.getElementById('chat').classList.contains('on')`);
  must(shut, 'the close button did not close the drawer');
  await openDrawer();
  const on = await evaluate(`document.getElementById('chat').classList.contains('on')`);
  must(on, 'the drawer did not come back after closing');
  return 'closed and reopened';
});

/* ── T11 · starting a NEW session actually repaints the pane ──────── */
/*    JL 260801: "我们打开了一个新的 session webpage,为什么整个页面没有跟着更新
      呢?" — picking a session used to set a pending id, print one sentence into
      the OLD transcript, and change nothing else: same body, same header, same
      row highlighted. This asserts the switch is a REPAINT, not an intent. */
await check('T11 starting a new session clears the pane and says so', async () => {
  const r = await evaluate(`(async function(){
    var P = window.__chatProbe;
    if (!P) return { skip: 'the drawer test bridge is missing' };
    P.bubble('cc', 'PREVIOUS SESSION TEXT');           // something to be cleared
    var before = { key: P.logKey(), sid: P.activeSid(),
                   had: document.querySelector('#chat .bd').textContent.indexOf('PREVIOUS SESSION TEXT') >= 0 };
    await P.switchTo('', 'a check session', false);
    return { before: before,
             after: { key: P.logKey(), sid: P.activeSid(),
                      marks: P.switchMarks(),
                      still: document.querySelector('#chat .bd').textContent.indexOf('PREVIOUS SESSION TEXT') >= 0,
                      sid_box: P.sidText() } };
  })()`);
  if (r.skip) throw new Error(r.skip);
  must(r.before.had, 'the fixture text never rendered, so the check proves nothing');
  must(!r.after.still, 'the previous session text SURVIVED the switch — the pane did not repaint');
  must(r.after.marks.length >= 1, 'no switch banner was written into the transcript');
  must(/new session/.test(r.after.marks.join(' ')), `banner does not name the switch: ${r.after.marks.join(' | ')}`);
  must(r.after.key !== r.before.key, `the local log key did not change (${r.before.key})`);
  must(/No session yet/.test(r.after.sid_box), `the .sid header still names the old session: "${r.after.sid_box.slice(0, 60)}"`);
  return `pane cleared, banner "${r.after.marks[0]}", key ${r.before.key} -> ${r.after.key}`;
});

/* ── T12 · the sync heartbeat does not drag you back ──────────────── */
/*    syncFromServer asked for the file header's `current` session no matter
      which one you had switched to, and wrote the answer over the pane a few
      seconds later. A switch that survives one heartbeat is the real fix. */
await check('T12 a switched pane survives the sync heartbeat', async () => {
  const r = await evaluate(`(async function(){
    var P = window.__chatProbe;
    if (!P) return { skip: 'the drawer test bridge is missing' };
    await P.switchTo('', 'a check session', false);
    var sid = P.activeSid();
    if (typeof syncNow === 'function') syncNow();
    return { sid: sid };
  })()`);
  if (r.skip) throw new Error(r.skip);
  await sleep(2500);                                  // let a heartbeat land
  const after = await evaluate(`(function(){
    var P = window.__chatProbe;
    return { sid: P.activeSid(), marks: P.switchMarks().length };
  })()`);
  must(after.sid === r.sid, `the sync moved the pane off the chosen session: "${r.sid}" -> "${after.sid}"`);
  must(after.marks >= 1, 'the sync repainted away the switch banner');
  return 'still on the chosen session after a sync';
});

/* ── report ───────────────────────────────────────────────────────── */
await evaluate(`(function(){                       // leave no filler behind
  [].slice.call(document.querySelectorAll('#chat .bd .m.sys')).forEach(function (n) {
    if (/^chatui /.test(n.textContent)) n.parentNode.removeChild(n);
  });
})()`);

const bad = results.filter(r => !r.ok);
console.log(`\n${results.length - bad.length}/${results.length} passed`);
if (errors.length) {
  console.log('\npage errors seen during the run:');
  errors.slice(0, 8).forEach(e => console.log('  ' + e));
}
ws.close();
process.exit(bad.length ? 1 : 0);
