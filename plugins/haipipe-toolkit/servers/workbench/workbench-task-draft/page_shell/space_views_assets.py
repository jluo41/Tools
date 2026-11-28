"""The Space views' stylesheets and script."""
from __future__ import annotations


# SPACE_CSS is two parts (261007, b03: a theme carries no look of its own, so the base frame takes
# only the view part): SPACE_VIEW_CSS styles view bodies (Space tabs and views, evidence tables,
# paragraph groups, the Supporting Runs tree) and names no class the frame draws; SPACE_SHELL_CSS is
# the Page workbench's layout and shell. The Page workbench reads both, unchanged.
SPACE_VIEW_CSS = """
.space-tabs{display:flex;flex-wrap:wrap;gap:6px;margin:4px 0 8px}
.space-tab,.space-view,.ev-open{font:600 11.5px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
 border:1px solid var(--line);border-radius:7px;padding:3px 10px;cursor:pointer;background:var(--card);color:var(--mut)}
.space-tab{color:var(--fg);font-size:12.5px;padding:4px 12px}
.space-tab.on,.space-view.on,.space-view.shown{border-color:var(--acc);color:var(--acc)}
.space-count{margin-left:4px;color:var(--mut);font-weight:500}
.space-count.st-stale{color:#a43d35}.space-count.st-pass{color:#24733d}
.space-reads{margin:2px 0 8px;color:var(--mut);font:12px/1.6 system-ui,sans-serif}
.space-reads code{font-size:11.5px;color:var(--fg)}
.space-views{display:flex;align-items:center;gap:5px;margin:2px 0 12px}
.space-views-label{font:600 10px/1.5 system-ui,sans-serif;color:var(--mut);text-transform:uppercase;
 letter-spacing:.05em;margin-right:2px}
.space-head{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 12px;margin:6px 0 10px;
 font:13.5px/1.45 system-ui,sans-serif}
.space-hint{color:var(--mut);font-size:12px}
.space-empty{color:var(--mut);font:13px/1.5 system-ui,sans-serif;padding:14px;border:1px dashed var(--line);
 border-radius:9px}
.space-source{white-space:pre-wrap;overflow-wrap:anywhere;margin:0;padding:10px 12px;border:1px solid var(--line);
 border-radius:9px;background:var(--card);font:12px/1.55 ui-monospace,Menlo,monospace}
.space-frame{display:block;width:100%;height:calc(100vh - 230px);min-height:360px;
 border:1px solid var(--line);border-radius:10px;background:var(--card)}
.ev-table{width:100%;border-collapse:collapse;font:13px/1.45 system-ui,sans-serif}
.ev-table th{text-align:left;font-weight:500;color:var(--mut);font-size:12px;padding:6px 8px;
 border-bottom:1px solid var(--line)}
.ev-table td{padding:7px 8px;border-bottom:1px solid var(--line);vertical-align:top}
.ev-table td:last-child{text-align:right;width:1%;white-space:nowrap}
.ev-row{cursor:pointer}
.ev-row:hover{background:color-mix(in srgb,var(--acc) 6%,var(--card))}
.ev-row.runs-selected{outline:2px solid var(--acc);outline-offset:-2px}
.ev-label{color:var(--mut)}
.ev-state{white-space:nowrap;color:var(--mut)}.ev-state.st-verified{color:#24733d}
details.paragraph-group>summary.prow::before{display:inline;content:"▸";position:static;transform:none;
 width:10px;height:auto;background:none;border-radius:0;color:var(--acc)}
details.paragraph-group[open]>summary.prow::before{content:"▾"}
.structure-card:not([open]) .structure-hint{display:none}
/* Evidence · Supporting Runs: Block > Job > Task > Run, each Run with the items it feeds.
   A file-tree look: guide lines, the level prefix (b03 j02 t01 r04) in the accent colour,
   the items by their short names (Edisplay13), grouped by type, a status dot, no box per row. */
.space-view[hidden]{display:none}
.sup-tree{font:13px/1.55 system-ui,sans-serif;margin:4px 0 12px}
.sup-node>summary{cursor:pointer;list-style:none;padding:2px 4px;border-radius:6px;text-transform:none;
 letter-spacing:normal;font:13px/1.55 system-ui,sans-serif;color:var(--fg);display:flex;align-items:center;gap:4px}
.sup-node>summary::-webkit-details-marker{display:none}
.sup-node>summary::before{content:"▸";width:12px;color:var(--mut);font-size:11px;flex:none}
.sup-node[open]>summary::before{content:"▾"}
.sup-node>summary:hover{background:color-mix(in srgb,var(--acc) 6%,transparent)}
.sup-world{margin:6px 0 10px}
.sup-world>summary{font-weight:600;font-size:13.5px}
.sup-path{color:var(--mut);font:12px ui-monospace,Menlo,monospace;font-weight:400}
.sup-node .sup-node,.sup-node>.sup-run{margin-left:10px;padding-left:12px;border-left:1px solid var(--line)}
.sup-node code{font:12.5px ui-monospace,Menlo,monospace;color:var(--fg)}
.sup-lvl{color:var(--acc);font-weight:700}
.sup-run{display:flex;align-items:center;gap:8px;padding:4px 8px;border-radius:0 7px 7px 0;cursor:pointer;min-height:28px}
.sup-run:hover{background:color-mix(in srgb,var(--acc) 6%,transparent)}
.sup-run.runs-selected{background:color-mix(in srgb,var(--acc) 12%,transparent);box-shadow:inset 2px 0 0 var(--acc)}
.sup-dot{width:8px;height:8px;border-radius:50%;background:var(--mut);flex:none}
.sup-dot.st-ready,.sup-dot.st-done{background:var(--ok)}
.sup-dot.st-held,.sup-dot.st-failed,.sup-dot.st-running{background:var(--warn)}
.sup-name{font:12.5px ui-monospace,Menlo,monospace}
.sup-state{font-size:12px;color:var(--mut)}
.sup-items{margin-left:auto;display:flex;flex-wrap:wrap;justify-content:flex-end;gap:4px 16px}
.sup-group{display:inline-flex;flex-wrap:wrap;align-items:center;gap:2px}
.sup-item{font:600 12px ui-monospace,Menlo,monospace;color:var(--fg);background:none;border:0;
 border-radius:5px;padding:1px 4px;cursor:pointer}
.sup-item:hover{background:color-mix(in srgb,var(--acc) 14%,transparent);color:var(--acc)}
"""
SPACE_SHELL_CSS = """/* Each Space: the content on the left, its Runs panel on the right at every width
   (JL 260927). The panel stays in view while the page scrolls; folded, it is a thin strip. */
.lens.show.space-split{display:flex;align-items:flex-start;gap:16px}
.space-split>.space-main{flex:1 1 auto;min-width:0}
.space-split>.runs-panel{flex:0 0 clamp(260px,30vw,600px);margin:0;position:sticky;top:8px;
 max-height:calc(100vh - 16px);display:flex;flex-direction:column;overflow:hidden}
.space-split>.runs-panel .runs-bar{flex-wrap:wrap}
.space-split>.runs-panel .runs-body{overflow:auto;min-height:0;grid-template-columns:1fr}
.space-split>.runs-panel .runs-types{flex-direction:row;flex-wrap:wrap}
.space-split>.runs-panel .run-type{gap:8px}
.space-split>.runs-panel.folded{flex-basis:42px}
.space-split>.runs-panel.folded .runs-bar{writing-mode:vertical-rl;flex-wrap:nowrap;padding:10px 9px;gap:10px}
/* The shared workbench shell (servers/README.md "Adding a workbench", rule 1; JL 261003):
   the Insight workbench's title, band, Space row and tab sizes, and each Space's
   tabs, views and content in one box. Page and Paper read this; neither restyles it. */
:root{--tab-line:#ced4da;--tab-on:#1864ab;--tab-wash:#e7f5ff;--acc-soft:#e6edf5;--box-line:#e3e3e6}
@media(prefers-color-scheme:dark){:root{--tab-line:#414852;--tab-on:#91caff;--tab-wash:#253749;
 --acc-soft:#22304a;--box-line:#2c2e33}}
body>h1{font-size:18px;margin:0 0 2px}
.wb-links{color:var(--mut);font-size:13px}.wb-links a{color:var(--acc)}
.wb-band{margin:10px 0 4px;padding:8px 14px;border:1px solid var(--acc);border-radius:10px;
 background:var(--acc-soft);color:var(--acc);font-size:14px;line-height:1.5}
.spaces{display:flex;gap:6px;margin:12px 0 8px;flex-wrap:wrap}
.spaces .space{font:400 16px system-ui,sans-serif;border:1px solid var(--tab-line);border-radius:6px;
 padding:6px 14px;cursor:pointer;background:var(--bg);color:var(--fg);white-space:nowrap}
.spaces .space.on{border-color:var(--tab-on);color:var(--tab-on);background:var(--tab-wash)}
.space-split>.space-main{border:1px solid var(--box-line);border-radius:10px;padding:12px 16px 16px}
.space-tabs{gap:6px;padding:0 0 10px;margin:0 0 12px;border-bottom:1px solid var(--box-line)}
.space-tab,.space-view{font:400 16px system-ui,sans-serif;border-color:var(--tab-line);border-radius:6px;
 padding:5px 12px;background:transparent;color:var(--fg)}
.space-tab.on,.space-view.on,.space-view.shown{border-color:var(--tab-on);color:var(--tab-on);background:var(--tab-wash)}
.space-views{gap:6px;margin:0 0 12px}
/* Draft: the View row first, as Guide's (a rule under it, no "View" label); the Structure
   fold belongs to Table, the view that reads `## 1 Structure` (JL 261003). */
.draft-lens>.space-main>.draft-mode-switcher{gap:6px;margin:0 0 12px;padding:0 0 12px;border-bottom:1px solid var(--box-line)}
.draft-mode-switcher .draft-mode-label{display:none}
.draft-lens:not([data-draft-mode="table"]) .draft-structure{display:none}
.draft-roadmap{display:none}
.draft-lens[data-draft-mode="roadmap"] .draft-roadmap{display:block}
.draft-lens[data-draft-mode="roadmap"]>.space-main>:not(.draft-mode-switcher):not(.draft-roadmap){display:none}
.draft-roadmap .rd-bar{display:flex;justify-content:flex-end;margin:0 0 8px;font-size:13px}
.page-roadmap-frame{display:block;width:100%;height:640px;border:1px solid var(--box-line);border-radius:8px;background:#fff}
.draft-roadmap details.rd-card{margin:0 0 14px}.draft-roadmap details.rd-card>summary{cursor:pointer;font-weight:650;font-size:15px;margin:0 0 8px}
.draft-roadmap .rd-stale{margin:0 0 6px;font-size:13px;color:#b3541e}
.draft-mode-switcher .draft-mode-tab{font:400 16px system-ui,sans-serif;border:1px solid var(--tab-line);border-radius:6px;
 padding:5px 12px;background:transparent;color:var(--fg)}
.draft-mode-switcher .draft-mode-tab.on{border-color:var(--tab-on);color:var(--tab-on);background:var(--tab-wash)}
@media(max-width:600px){.spaces{flex-wrap:nowrap;overflow-x:auto}.spaces .space{font-size:15px;padding:5px 10px}
 .space-split>.space-main{padding:10px}}
"""
SPACE_CSS = SPACE_VIEW_CSS + SPACE_SHELL_CSS

SPACE_JS = r"""
(function(){
 function store(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v);}catch(e){return null;}}
 function scope(space,view,label,mode){document.dispatchEvent(new CustomEvent('space-scope',{detail:{space:space,view:view,label:label,mode:mode}}));}
 function target(space,t){document.dispatchEvent(new CustomEvent('space-target',{detail:{space:space,target:t}}));}
 function lazy(root){root.querySelectorAll('iframe[data-src]').forEach(function(f){
  if(f.closest('[hidden]'))return;if(!f.getAttribute('src')&&f.dataset.src)f.setAttribute('src',f.dataset.src);});}
 document.querySelectorAll('.space-body').forEach(function(body){
  var space=body.dataset.space,lens=body.closest('.lens');
  var tabs=lens.querySelectorAll('.space-tabs[data-space="'+space+'"] .space-tab');
  var views=lens.querySelectorAll('.space-views[data-space="'+space+'"] .space-view');
  function current(list){var on=[].filter.call(list,function(b){return b.classList.contains('on');})[0];return on||list[0];}
  function show(){
   var tab=current(tabs),view=current(views);
   /* a tab may offer only some views (Supporting Runs: All items, Source); the
      chosen view stays chosen for the other tabs */
   var allow=(tab.dataset.views||'').split(' ').filter(Boolean),forced=false;
   views.forEach(function(b){b.hidden=allow.length>0&&allow.indexOf(b.dataset.view)<0;});
   if(view.hidden){view=[].filter.call(views,function(b){return !b.hidden;})[0]||view;forced=true;}
   views.forEach(function(b){b.classList.toggle('shown',b===view);});
   body.querySelectorAll('.space-pane').forEach(function(p){
    p.hidden=!((p.dataset.view===view.dataset.view)&&(!p.dataset.tab||p.dataset.tab===tab.dataset.tab));});
   if(lens.classList.contains('show'))lazy(body);
   store('space-tab:'+space,tab.dataset.tab);if(!forced)store('space-view:'+space,view.dataset.view);
   scope(space,tab.dataset.tab,tab.dataset.label,view.dataset.view);
   syncCards();
  }
  /* Evidence Card view: the cards come from the older Evidence page in a frame
     (same origin). Opening a card selects its item, like clicking its row; a
     selected item opens its card; the frame shows only the current tab's kind. */
  var frame=body.querySelector('.space-pane[data-view=card] iframe');
  var KIND={citations:'CITE',displays:'DISPLAY',values:'VALUE'};
  function frameDoc(){try{return frame&&frame.contentDocument&&frame.contentDocument.body?frame.contentDocument:null;}catch(e){return null;}}
  function selectItem(item){
   body.querySelectorAll('.ev-row.runs-selected').forEach(function(x){x.classList.remove('runs-selected');});
   var r=item&&body.querySelector('.ev-row[data-item="'+item+'"]');if(r)r.classList.add('runs-selected');
   target(space,item||'');
  }
  function syncCards(){
   var d=frameDoc();if(!d)return;
   if(!d.getElementById('space-card-style')){
    var st=d.createElement('style');st.id='space-card-style';
    st.textContent='body.embedded>header,.evidence-overview,.source-details{display:none!important}';
    d.head.appendChild(st);
    d.addEventListener('toggle',function(ev){var c=ev.target;
     if(!c.matches||!c.matches('details.evidence-card')||!c.open)return;
     var id=(c.dataset.evidenceId||'').match(/^E\d+/);if(id)selectItem(id[0]);},true);
   }
   var tab=current(tabs).dataset.tab;
   d.querySelectorAll('section.evidence-type-section').forEach(function(sec){
    sec.hidden=!!KIND[tab]&&sec.dataset.evidenceType!==KIND[tab];});
   var row=body.querySelector('.ev-row.runs-selected');
   if(row&&current(views).dataset.view==='card'){
    var card=d.querySelector('details.evidence-card[data-evidence-id^="'+row.dataset.item+'-"]');
    if(card){if(!card.open)card.open=true;card.scrollIntoView({block:'center'});}
   }
  }
  if(frame)frame.addEventListener('load',syncCards);
  function pick(list,key,value){list.forEach(function(b){b.classList.toggle('on',b.dataset[key]===value);});}
  tabs.forEach(function(b){b.addEventListener('click',function(){
   pick(tabs,'tab',b.dataset.tab);
   var chosen=body.querySelectorAll('.ev-row.runs-selected,.sup-run.runs-selected');
   chosen.forEach(function(x){x.classList.remove('runs-selected');});
   show();if(chosen.length)target(space,'');});});
  views.forEach(function(b){b.addEventListener('click',function(){pick(views,'view',b.dataset.view);show();});});
  var t=store('space-tab:'+space),v=store('space-view:'+space);
  if(t&&[].some.call(tabs,function(b){return b.dataset.tab===t;}))pick(tabs,'tab',t);
  if(v&&[].some.call(views,function(b){return b.dataset.view===v;}))pick(views,'view',v);
  var q=new URLSearchParams(location.search);
  if(space==='evidence'&&q.get('lens')==='evidence'&&q.get('focus'))pick(views,'view','card');
  show();
  /* A Draft evidence chip opens the Evidence Space on that item's card. */
  document.addEventListener('lens-shown',function(ev){
   if(ev.detail.name!==space)return;
   if(space==='evidence'&&ev.detail.focus){pick(views,'view','card');show();}
   else lazy(body);});
  new MutationObserver(function(){if(lens.classList.contains('show'))lazy(body);}).observe(lens,{attributes:true,attributeFilter:['class']});
  body.addEventListener('click',function(ev){
   /* Supporting Runs: an item chip opens that item on its own tab; a Run narrows the Runs panel */
   var chip=ev.target.closest('.sup-item');
   if(chip){pick(tabs,'tab',chip.dataset.tab);pick(views,'view','items');show();selectItem(chip.dataset.item);
    var hit=body.querySelector('.ev-row.runs-selected');if(hit)hit.scrollIntoView({block:'center'});return;}
   var run=ev.target.closest('.sup-run');
   if(run){var again=run.classList.contains('runs-selected');
    body.querySelectorAll('.sup-run.runs-selected').forEach(function(x){x.classList.remove('runs-selected');});
    if(!again)run.classList.add('runs-selected');target(space,again?'':run.dataset.run);return;}
   var row=ev.target.closest('.ev-row');if(!row)return;
   if(ev.target.closest('.ev-open')){
    selectItem(row.dataset.item);
    if(!frame.getAttribute('src'))frame.setAttribute('src',frame.dataset.src);
    pick(views,'view','card');show();return;}
   selectItem(row.classList.contains('runs-selected')?'':row.dataset.item);
  });
  body.addEventListener('keydown',function(ev){var row=ev.target.closest('.ev-row,.sup-run');if(row&&ev.key==='Enter')row.click();});
 });
 /* Draft Space: the Structure card remembers whether it is open. */
 var card=document.querySelector('.structure-card');
 if(card){
  if(store('structure-open')==='1')card.open=true;
  card.addEventListener('toggle',function(){store('structure-open',card.open?'1':'0');});
 }
})();
"""
