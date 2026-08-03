/* QD2/QD5 · ONE PAGE, ITS OWN CHAT — the hardest ordering tests.
 *
 * JL 260803: "your chat split is not attached to the page split... we should
 * make these binding relationships". Every case below is an ORDER of
 * operations, because that is where every instance of this bug has lived:
 * the chat followed the page when it was already open, and did not when it was
 * opened afterwards, and the difference was invisible until someone did it in
 * the other order.
 *
 *   B1  open chat, THEN navigate            → chat follows
 *   B2  navigate, THEN open chat            → chat opens on the page you see
 *   B3  open as TUI, then navigate          → follows, still TUI
 *   B4  navigate A→B→C fast                 → chat ends on C, not B
 *   B5  cross-group A(QA)→B(QB)             → follows across groups
 *   B6  reload after navigating             → chat is the CURRENT page
 *   B7  switch mode, then navigate          → mode kept, page followed
 *   B8  chat never re-points to a stale plan (the dataset.src trap)
 */
const CDP = process.env.CHECK_CDP || '127.0.0.1:9335';
const BOARD = process.env.CHECK_BOARD
  || 'http://127.0.0.1:5599/Tools/plugins/haipipe-toolkit/skills/diagrams/01-haipipe-paper-260725/board';
const P1 = 'QB/QB0-paper-board-layout.html', ID1 = 'QB0';
const P2 = 'QA/QA2-the-skill-set.html',      ID2 = 'QA2';
const P3 = 'QA/QA5-the-probe-layer.html',    ID3 = 'QA5';

let tab = await (await fetch(`http://${CDP}/json/new`, { method: 'PUT' })).json();
let ws, id = 0; const waits = new Map(); const errs = [];
async function attach(t) {
  ws = new WebSocket(t.webSocketDebuggerUrl);
  await new Promise(r => ws.addEventListener('open', r));
  ws.addEventListener('message', e => {
    const m = JSON.parse(e.data);
    if (m.id && waits.has(m.id)) { waits.get(m.id)(m); waits.delete(m.id); }
    if (m.method === 'Runtime.exceptionThrown')
      errs.push((m.params.exceptionDetails.exception?.description || 'ex').slice(0, 120));
  });
  await send('Runtime.enable'); await send('Page.enable');
}
const send = (method, params = {}) =>
  new Promise(r => { const i = ++id; waits.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const sleep = ms => new Promise(r => setTimeout(r, ms));
const ev = async x => {
  const r = await send('Runtime.evaluate', { expression: x, awaitPromise: true, returnByValue: true });
  return r.result?.exceptionDetails ? '__EX__' : r.result.result.value;
};
const fails = [];
const ok = (n, c, d) => { console.log(`${c ? '  ✅' : '  ❌'} ${n}${c ? '' : '  — ' + d}`); if (!c) fails.push(n); };

const ST = `(function(){var o={};
 try{o.page=frames.page.location.pathname.split('/').pop();}catch(e){o.page='?';}
 var fc=document.querySelector('iframe[name="chat"]');
 o.src=(fc.getAttribute('src')||'').split('/').pop();
 o.plan=(fc.dataset.src||'').split('/').pop();
 try{o.hdr=(frames.chat.document.querySelector('#chat .qid')||{}).textContent||'';
     o.tip=(frames.chat.document.querySelector('#chat .tip')||{}).textContent||'';
     o.mode=frames.chat.__paneModeNow?frames.chat.__paneModeNow():'-';}catch(e){}
 return JSON.stringify(o);})()`;
const st = async () => JSON.parse(await ev(ST));
const openShell = async (p, mode) => {
  await send('Page.navigate', { url: `${BOARD}/${p}?split` }); await sleep(3500);
  await ev(`localStorage.clear(); localStorage.setItem('board-split-mode','${mode||'gui'}'); localStorage.setItem('board-split-chat','0');`);
  await send('Page.navigate', { url: `${BOARD}/${p}?split` }); await sleep(6500);
};
const openChat = async (which) => {
  await ev(`(function(){var b=document.getElementById('${which === 'tui' ? 'mtui' : 'mgui'}');
    if(b && b.getAttribute('aria-pressed')!=='true') b.click(); return 1;})()`);
  await sleep(6500);
};
const openRail = async () => {
  await ev(`(function(){var b=[].filter.call(document.querySelectorAll('button,a'),function(x){return /Pages|Index|☰/.test(x.textContent||'')})[0]; if(b)b.click();})()`);
  await sleep(5000);
};
const clickPage = async (frag) => {
  const r = await ev(`(function(){try{var d=frames.index.document;
    var a=[].filter.call(d.querySelectorAll('a[href]'),function(x){return /${frag}/.test(x.getAttribute('href')||'');})[0];
    if(a){a.click(); return 'ok';} return 'none';}catch(e){return 'EX';}})()`);
  await sleep(6500); return r;
};
const bound = (s, want) => new RegExp(want).test(s.src) && (!s.tip || new RegExp(want).test(s.tip))
                        && (!s.hdr || new RegExp(want).test(s.hdr));

await attach(tab);

console.log('B1 · open the chat, THEN navigate');
await openShell(P1); await openChat('gui'); await openRail();
await clickPage('QA2-the-skill-set');
let s = await st(); ok('the chat follows to ' + ID2, bound(s, ID2), JSON.stringify(s));

console.log('B2 · navigate, THEN open the chat');
await openShell(P1); await openRail();
await clickPage('QA2-the-skill-set');
await openChat('gui');
s = await st(); ok('the chat opens on ' + ID2 + ', not the page the shell started on', bound(s, ID2), JSON.stringify(s));
ok('and the lazy PLAN is not stale', new RegExp(ID2).test(s.plan), 'plan=' + s.plan);

console.log('B3 · open as TUI, then navigate');
await openShell(P1, 'tui'); await openChat('tui'); await openRail();
await clickPage('QA2-the-skill-set');
s = await st(); ok('the TUI follows the page', bound(s, ID2), JSON.stringify(s));
ok('and it is still the TUI', s.mode === 'tui', 'mode=' + s.mode);

console.log('B4 · navigate A → B → C quickly');
await openShell(P1); await openChat('gui'); await openRail();
await ev(`(function(){try{var d=frames.index.document;
  var a=[].filter.call(d.querySelectorAll('a[href]'),function(x){return /QA2-the-skill-set/.test(x.getAttribute('href')||'');})[0]; if(a)a.click();}catch(e){}})()`);
await sleep(1200);
await clickPage('QA5-the-probe-layer');
s = await st(); ok('the chat lands on the LAST page, ' + ID3, bound(s, ID3), JSON.stringify(s));

console.log('B5/B6 · reload after navigating');
await send('Page.reload', { ignoreCache: true }); await sleep(9000);
await openChat('gui');
s = await st(); ok('after a reload the chat is the page you are on', bound(s, ID3), JSON.stringify(s));

console.log('B7 · switch mode, then navigate');
await openChat('tui'); await sleep(2000); await openRail();
await clickPage('QA2-the-skill-set');
s = await st();
ok('switching then navigating keeps both right', bound(s, ID2) && s.mode === 'tui',
   JSON.stringify(s));

ok('nothing threw across all of it', errs.length === 0, errs.slice(0, 2).join(' ; '));
console.log();
if (fails.length) { console.log(`❌ ${fails.length} failed`); process.exit(1); }
console.log('✅ the chat is bound to the page, in every order');
await fetch(`http://${CDP}/json/close/${tab.id}`);
process.exit(0);
