"""Draft Lab folds a paragraph once every sentence in it is checked (✓, `li[data-checked="1"]`), to one line with its
title; a Section head never folds, so the folded paragraphs' titles stay in view. Each head is judged once, when the page is whole: a paragraph the reader opens
stays open, and a ✓ clicked later never snaps it shut while it is being read. The fold itself is draft_step_evidence's
`pfold` (exposed as `window.sxPfold`), so the folded head keeps its title and marks.

The page also keeps still under the reader: a write the page makes itself (✓, a comment, a card's act: any POST to
/_board/draft-*) opens a short quiet window in which the 4 s file poll (draft_step_evidence `live`) takes the new stamp
without reloading; a change made elsewhere shows a quiet "↻ Show changes" pill, and only its click reloads (back at the
sentence in view); and the fold is judged from the checks on every load, less any paragraph the reader opened by hand in
this tab (sessionStorage) or is reading, and a paragraph opens again when one of its checks lapses.
"""

AUTOFOLD_JS = """<script>(function(){if(window.sxAutofold)return;window.sxAutofold=1;
 var f0=window.fetch;window.fetch=function(u,o){if(o&&/post/i.test(o.method||'')&&/^\\/_board\\/draft-/.test(String(u)))
  window.sxQuiet=Date.now()+6000;return f0.apply(this,arguments);};          /* the page's own write never reloads it */
 /* a change from elsewhere reloads by itself once the reader has been still for 3 s (JL 261114: "why not the auto
    relaod"); until then the pill shows, so a page never moves under a hand that is scrolling, clicking or typing */
 var lastAct=Date.now();['scroll','mousedown','keydown','touchstart','wheel'].forEach(function(k){
  window.addEventListener(k,function(){lastAct=Date.now();},{passive:true,capture:true});});
 function busy(){var a=document.activeElement;if(a&&(a.isContentEditable||/^(INPUT|TEXTAREA|SELECT)$/.test(a.tagName)))return true;
  if(document.querySelector('.rv-card.editing,.rv-note.writing,.rv-note.nt-new'))return true;
  var sel=window.getSelection&&window.getSelection();return !!(sel&&String(sel).trim());}
 var pend=null;setInterval(function(){if(pend&&!document.hidden&&Date.now()-lastAct>3000&&!busy()){var r=pend;pend=null;r();}},1000);
 window.sxPill=function(reload){pend=reload;if(document.querySelector('.sx-pill'))return;var b=document.createElement('button');
  b.type='button';b.className='sx-pill';b.textContent='↻ Show changes';b.onclick=function(){b.disabled=true;reload();};
  b.style.cssText='position:fixed;top:12px;left:50%;transform:translateX(-50%);z-index:50;padding:5px 14px;border-radius:14px;'
   +'border:1px solid var(--line,#ddd);background:var(--paper,#fff);color:var(--ink,#222);font-size:13px;box-shadow:0 2px 8px rgba(0,0,0,.12);cursor:pointer';
  document.body.appendChild(b);};                                            /* a change from elsewhere waits for the reader */
 /* the fold is judged from today's checks on every load (JL 261115: "the first paragraph are all checked, right? why
    it is not collapsed?"): a paragraph folds when each of its sentences is checked with its words unchanged, unless the
    reader opened it by hand in this tab (kept in sessionStorage) or is reading it; it opens again by itself when a
    check lapses (a stale or removed ✓). A ✓ clicked while the page is open never snaps a paragraph shut */
 var key='sx-opened:'+location.pathname+location.search,opened=[];
 try{opened=JSON.parse(sessionStorage.getItem(key)||'[]')||[];}catch(x){}
 function save(){try{sessionStorage.setItem(key,JSON.stringify(opened));}catch(x){}}
 document.addEventListener('click',function(e){var t=e.target.closest&&e.target.closest('.sx-ptog');if(!t)return;
  var h=t.closest('.sx-row'),p=h&&h.querySelector('[data-p]');if(!p)return;var pid=p.dataset.p;
  setTimeout(function(){var shut=h.classList.contains('sx-pfold');opened=opened.filter(function(x){return x!==pid;});
   if(!shut)opened.push(pid);save();});},true);
 function rowsUnder(h){var out=[],sec=h.classList.contains('sx-c'),n=h.nextElementSibling;
  while(n&&n.classList.contains('sx-row')&&!n.classList.contains('sx-c')&&(sec||!n.classList.contains('sx-p'))){out.push(n);n=n.nextElementSibling;}
  return out;}
 function run(){if(document.readyState!=='complete'||!window.sxPfold)return;
  if(document.querySelector('.sx-board .sx-row:not([data-sx])'))return;          /* wait until every row is set up */
  document.querySelectorAll('.sx-board .sx-row.sx-p').forEach(function(h){
   var s=rowsUnder(h).map(function(r){return r.querySelector('.rv-left li[data-s]');}).filter(Boolean);
   var all=s.length&&s.every(function(li){return li.getAttribute('data-checked')==='1';});
   var pid=(h.querySelector('[data-p]')||{dataset:{}}).dataset.p;
   if(h.dataset.autofold===undefined){                                          /* judged once per page load */
    var k=window.sxKept,here=k&&s.some(function(li){return li.dataset.a===k||li.dataset.s===k;});
    var fold=all&&!here&&opened.indexOf(pid)<0;h.dataset.autofold=fold?'1':'0';if(fold)window.sxPfold(h,true);}
   else if(h.dataset.autofold==='1'&&!all){h.dataset.autofold='0';window.sxPfold(h,false);}});}   /* a check lapsed */
 window.addEventListener('load',run);
 var due=0;new MutationObserver(function(){if(due)return;due=1;requestAnimationFrame(function(){due=0;run();});})
  .observe(document.documentElement,{childList:true,subtree:true});
})();</script>"""
