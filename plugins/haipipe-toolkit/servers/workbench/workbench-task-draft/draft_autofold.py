"""Draft Lab folds a paragraph once every sentence in it is checked (✓, `li[data-checked="1"]`), and a Section once all
of its paragraphs are folded that way. Each head is judged once, when the page is whole: a paragraph the reader opens
stays open, and a ✓ clicked later never snaps it shut while it is being read. The fold itself is draft_step_evidence's
`pfold` (exposed as `window.sxPfold`), so the folded head keeps its title and marks.
"""

AUTOFOLD_JS = """<script>(function(){if(window.sxAutofold)return;window.sxAutofold=1;
 function rowsUnder(h){var out=[],sec=h.classList.contains('sx-c'),n=h.nextElementSibling;
  while(n&&n.classList.contains('sx-row')&&!n.classList.contains('sx-c')&&(sec||!n.classList.contains('sx-p'))){out.push(n);n=n.nextElementSibling;}
  return out;}
 function run(){if(document.readyState!=='complete'||!window.sxPfold)return;
  if(document.querySelector('.sx-board .sx-row:not([data-sx])'))return;          /* wait until every row is set up */
  document.querySelectorAll('.sx-board .sx-row.sx-p:not([data-autofold])').forEach(function(h){
   var s=rowsUnder(h).map(function(r){return r.querySelector('.rv-left li[data-s]');}).filter(Boolean);
   var done=s.length&&s.every(function(li){return li.getAttribute('data-checked')==='1';});
   h.dataset.autofold=done?'1':'0';if(done)window.sxPfold(h,true);});
  document.querySelectorAll('.sx-board .sx-row.sx-c:not([data-autofold])').forEach(function(c){
   var ps=rowsUnder(c).filter(function(r){return r.classList.contains('sx-p');});
   var done=ps.length&&ps.every(function(p){return p.dataset.autofold==='1';});
   c.dataset.autofold=done?'1':'0';if(done)window.sxPfold(c,true);});}
 window.addEventListener('load',run);
 var due=0;new MutationObserver(function(){if(due)return;due=1;requestAnimationFrame(function(){due=0;run();});})
  .observe(document.documentElement,{childList:true,subtree:true});
})();</script>"""
