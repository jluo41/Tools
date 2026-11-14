"""Draft Lab folds a paragraph once every sentence in it is checked (✓, `li[data-checked="1"]`), to one line with its
title; a Section head never folds, so the folded paragraphs' titles stay in view. Each head is judged once, when the page is whole: a paragraph the reader opens
stays open, and a ✓ clicked later never snaps it shut while it is being read. The fold itself is draft_step_evidence's
`pfold` (exposed as `window.sxPfold`), so the folded head keeps its title and marks.

The page also keeps still under the reader: a write the page makes itself (✓, a comment, a card's act: any POST to
/_board/draft-*) opens a short quiet window in which the 4 s file poll (draft_step_evidence `live`) takes the new stamp
without reloading; a change made elsewhere shows a quiet "↻ Show changes" pill, and only its click reloads (back at the
sentence in view); and the fold is judged on the page's first open only: after a reload the same paragraphs fold again
(kept in sessionStorage, less any the reader opened by hand), so nothing moves, and the reader's paragraph never folds.
"""

AUTOFOLD_JS = """<script>(function(){if(window.sxAutofold)return;window.sxAutofold=1;
 var f0=window.fetch;window.fetch=function(u,o){if(o&&/post/i.test(o.method||'')&&/^\\/_board\\/draft-/.test(String(u)))
  window.sxQuiet=Date.now()+6000;return f0.apply(this,arguments);};          /* the page's own write never reloads it */
 window.sxPill=function(reload){if(document.querySelector('.sx-pill'))return;var b=document.createElement('button');
  b.type='button';b.className='sx-pill';b.textContent='↻ Show changes';b.onclick=function(){b.disabled=true;reload();};
  b.style.cssText='position:fixed;top:12px;left:50%;transform:translateX(-50%);z-index:50;padding:5px 14px;border-radius:14px;'
   +'border:1px solid var(--line,#ddd);background:var(--paper,#fff);color:var(--ink,#222);font-size:13px;box-shadow:0 2px 8px rgba(0,0,0,.12);cursor:pointer';
  document.body.appendChild(b);};                                            /* a change from elsewhere waits for the reader */
 /* fold on the first open only; after a reload the same paragraphs fold again, so nothing moves, less any the reader
    opened by hand (it stays open) */
 var key='sx-folded:'+location.pathname+location.search,kept=null;
 try{kept=JSON.parse(sessionStorage.getItem(key)||'null');}catch(x){}
 function save(){try{sessionStorage.setItem(key,JSON.stringify(kept));}catch(x){}}
 document.addEventListener('click',function(e){var t=e.target.closest&&e.target.closest('.sx-ptog');if(!t||!kept)return;
  var p=t.closest('.sx-row').querySelector('[data-p]');if(p){kept=kept.filter(function(x){return x!==p.dataset.p;});save();}},true);
 function rowsUnder(h){var out=[],sec=h.classList.contains('sx-c'),n=h.nextElementSibling;
  while(n&&n.classList.contains('sx-row')&&!n.classList.contains('sx-c')&&(sec||!n.classList.contains('sx-p'))){out.push(n);n=n.nextElementSibling;}
  return out;}
 function run(){if(document.readyState!=='complete'||!window.sxPfold)return;
  if(document.querySelector('.sx-board .sx-row:not([data-sx])'))return;          /* wait until every row is set up */
  document.querySelectorAll('.sx-board .sx-row.sx-p:not([data-autofold])').forEach(function(h){
   var s=rowsUnder(h).map(function(r){return r.querySelector('.rv-left li[data-s]');}).filter(Boolean);
   var k=window.sxKept,here=k&&s.some(function(li){return li.dataset.a===k||li.dataset.s===k;});   /* the reader is here */
   var pid=(h.querySelector('[data-p]')||{dataset:{}}).dataset.p;
   var done=!here&&(first?s.length&&s.every(function(li){return li.getAttribute('data-checked')==='1';}):kept.indexOf(pid)>=0);
   h.dataset.autofold=done?'1':'0';if(done){window.sxPfold(h,true);if(first)kept.push(pid);}});
  if(first)save();}   /* a Section never folds: its paragraph titles stay seen */
 var first=!kept;if(first)kept=[];
 window.addEventListener('load',run);
 var due=0;new MutationObserver(function(){if(due)return;due=1;requestAnimationFrame(function(){due=0;run();});})
  .observe(document.documentElement,{childList:true,subtree:true});
})();</script>"""
