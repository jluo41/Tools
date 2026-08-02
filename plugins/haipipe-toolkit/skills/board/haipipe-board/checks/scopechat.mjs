/* QD2 · the chat at THREE scopes: one page, one group, the whole board.
 *
 * Every check so far drove a PAGE chat. A board session (file=board.md) and a
 * group session (file=<group folder>) are separate identities with their own
 * priming, their own session registry entry and their own permission surface,
 * and nothing has ever driven them.
 *
 *   B1  the index page opens a BOARD chat, and it knows it is the board
 *   B2  a group folder opens a GROUP chat, and it knows its group
 *   B3  each scope keeps its own transcript, not the page's
 *   B4  none of it throws
 *
 * Cheap: haiku + low, and the questions are one line each.
 */
const CDP = process.env.CHECK_CDP || '127.0.0.1:9335';
const BASE = process.env.CHECK_BASE
  || 'http://127.0.0.1:5599/Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/board';

const tab = await (await fetch(`http://${CDP}/json/new`, { method: 'PUT' })).json();
const ws = new WebSocket(tab.webSocketDebuggerUrl);
await new Promise(r => ws.addEventListener('open', r));
let id = 0; const waits = new Map(); const errs = [];
ws.addEventListener('message', e => {
  const m = JSON.parse(e.data);
  if (m.id && waits.has(m.id)) { waits.get(m.id)(m); waits.delete(m.id); }
  if (m.method === 'Runtime.exceptionThrown')
    errs.push((m.params.exceptionDetails.exception?.description || 'ex').slice(0, 130));
});
const send = (method, params = {}) =>
  new Promise(r => { const i = ++id; waits.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const sleep = ms => new Promise(r => setTimeout(r, ms));
const ev = async x => {
  const r = await send('Runtime.evaluate', { expression: x, awaitPromise: true, returnByValue: true });
  return r.result?.exceptionDetails ? '__EX__ ' + JSON.stringify(r.result.exceptionDetails.exception).slice(0, 150)
                                    : r.result.result.value;
};
const fails = [];
const ok = (n, c, d) => { console.log(`${c ? '  ✅' : '  ❌'} ${n}${c ? '' : '  — ' + d}`); if (!c) fails.push(`${n}: ${d}`); };

/* These pages are opened PLAIN, not in the split: the index and a group file
   are where a board/group session is offered, and the split's chat pane always
   binds to the page in its page frame. */
async function openPlain(url) {
  await send('Page.navigate', { url }); await sleep(6000);
  await ev(`Object.keys(localStorage).filter(function(k){return /board-split/.test(k)}).forEach(function(k){localStorage.removeItem(k)})`);
  await send('Page.navigate', { url: url + (url.includes('?') ? '&' : '?') + 'plain' }); await sleep(6500);
  for (let i = 0; i < 40; i++) {
    if (await ev(`!!document.getElementById('chatfab')`) === true) return true;
    await sleep(500);
  }
  return false;
}
async function openDrawer() {
  await ev(`document.getElementById('chatfab').click()`); await sleep(1600);
  await ev(`(function(){var b=document.querySelector('#chatpick .pk[data-v="gui"]'); if(b){b.click(); return 1;} return 0;})()`);
  await sleep(3000);
  return ev(`document.getElementById('chat').classList.contains('on')`);
}
async function ask(text) {
  await ev(`(function(){var c=document.getElementById('chat');
    c.querySelector('.scope').value='scoped'; c.querySelector('.mdl').value='haiku'; c.querySelector('.eff').value='low';
    c.querySelector('textarea').value=${JSON.stringify(text)}; c.querySelector('.send').click(); return 1;})()`);
  for (let i = 0; i < 60; i++) { await sleep(2500);
    if (await ev(`document.body.classList.contains('chatbusy')`) === false) break; }
  return ev(`(function(){var cc=document.querySelectorAll('#chat .bd .cc');
    return cc.length? cc[cc.length-1].textContent.trim().slice(0,200) : '';})()`);
}
const tip = () => ev(`(function(){var t=document.querySelector('#chat .tip'); return t? t.textContent.trim() : '';})()`);

await send('Runtime.enable'); await send('Page.enable');

// ── B1 · the board session ────────────────────────────────────────────────
console.log('B1 · the index opens a whole-board chat');
ok('the index page offers a chat', await openPlain(`${BASE}/index.html`), 'no chat button on the index');
ok('the drawer opens there', (await openDrawer()) === true, 'drawer did not open');
const boardTip = await tip();
ok('it is bound to board.md, not a page', /board\.md/.test(boardTip), `tip says ${JSON.stringify(boardTip)}`);
const a1 = await ask('In one short sentence: are you attached to one question, one group, or the whole board?');
console.log('    it says:', JSON.stringify(a1.slice(0, 120)));
ok('a board chat answers', a1.length > 5, 'no answer');
ok('and it knows it is the board', /board/i.test(a1), `answer: ${a1.slice(0,90)}`);

// ── B2 · the group session ────────────────────────────────────────────────
console.log('B2 · a group page opens a group chat');
const grpOk = await openPlain(`${BASE}/QD.html`);
ok('the group page offers a chat', grpOk, 'no chat button on the group page');
if (grpOk) {
  ok('the drawer opens there', (await openDrawer()) === true, 'drawer did not open');
  const gTip = await tip();
  ok('it is bound to a GROUP, not a page', /group/i.test(gTip) || /QD/.test(gTip),
     `tip says ${JSON.stringify(gTip)}`);
  const a2 = await ask('In one short sentence: which page group are you attached to?');
  console.log('    it says:', JSON.stringify(a2.slice(0, 120)));
  ok('a group chat answers', a2.length > 5, 'no answer');
  ok('and it names its own group', /QD/i.test(a2), `answer: ${a2.slice(0,90)}`);
}

// ── B3 · the scopes do not share a transcript ─────────────────────────────
console.log('B3 · each scope keeps its own transcript');
const keys = await ev(`JSON.stringify(Object.keys(localStorage).filter(function(k){return k.indexOf('board-chat:')===0}))`);
const parsed = JSON.parse(keys || '[]');
ok('board and group chats store under their own keys', parsed.length >= 2,
   `${parsed.length} chat key(s): ${keys}`);

ok('none of it threw', errs.length === 0, errs.slice(0, 2).join(' ; '));
console.log();
if (fails.length) { console.log(`❌ ${fails.length} failed:`); fails.forEach(f => console.log('   · ' + f)); process.exit(1); }
console.log('✅ board and group chats both work and stay separate');
await fetch(`http://${CDP}/json/close/${tab.id}`);
process.exit(0);
