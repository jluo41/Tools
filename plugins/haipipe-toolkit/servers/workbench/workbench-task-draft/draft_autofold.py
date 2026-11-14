"""Draft Lab folds a paragraph once every sentence in it is checked (✓, `li[data-checked="1"]`), to one line with its
title; a Section head never folds, so the folded paragraphs' titles stay in view. Each head is judged once, when the page is whole: a paragraph the reader opens
stays open, and a ✓ clicked later never snaps it shut while it is being read. The fold itself is draft_step_evidence's
`pfold` (exposed as `window.sxPfold`), so the folded head keeps its title and marks.

The page also keeps still under the reader: a write the page makes itself (✓, a comment, a card's act: any POST to
/_board/draft-*) opens a short quiet window in which the 4 s file poll (draft_step_evidence `live`) takes the new stamp
without reloading; and after a reload, the paragraph holding the sentence the reader was on (`window.sxKept`) never folds.
"""

AUTOFOLD_JS = """<script>(function(){if(window.sxAutofold)return;window.sxAutofold=1;
 var f0=window.fetch;window.fetch=function(u,o){if(o&&/post/i.test(o.method||'')&&/^\\/_board\\/draft-/.test(String(u)))
  window.sxQuiet=Date.now()+6000;return f0.apply(this,arguments);};          /* the page's own write never reloads it */
 function rowsUnder(h){var out=[],sec=h.classList.contains('sx-c'),n=h.nextElementSibling;
  while(n&&n.classList.contains('sx-row')&&!n.classList.contains('sx-c')&&(sec||!n.classList.contains('sx-p'))){out.push(n);n=n.nextElementSibling;}
  return out;}
 function run(){if(document.readyState!=='complete'||!window.sxPfold)return;
  if(document.querySelector('.sx-board .sx-row:not([data-sx])'))return;          /* wait until every row is set up */
  document.querySelectorAll('.sx-board .sx-row.sx-p:not([data-autofold])').forEach(function(h){
   var s=rowsUnder(h).map(function(r){return r.querySelector('.rv-left li[data-s]');}).filter(Boolean);
   var k=window.sxKept,here=k&&s.some(function(li){return li.dataset.a===k||li.dataset.s===k;});   /* the reader is here */
   var done=!here&&s.length&&s.every(function(li){return li.getAttribute('data-checked')==='1';});
   h.dataset.autofold=done?'1':'0';if(done)window.sxPfold(h,true);});}   /* a Section never folds: its paragraph titles stay seen */
 window.addEventListener('load',run);
 var due=0;new MutationObserver(function(){if(due)return;due=1;requestAnimationFrame(function(){due=0;run();});})
  .observe(document.documentElement,{childList:true,subtree:true});
})();</script>"""
