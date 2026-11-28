"""The Runs panel's own CSS and JS (moved out of runs_panel.py to keep it short; AGENTS.md "Keep files short")."""

PANEL_CSS = """
.runs-panel button{font:600 11.5px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
 border:1px solid var(--line);border-radius:7px;padding:3px 9px;cursor:pointer;background:var(--card);color:var(--fg)}
.run-type.on{border-color:var(--acc);color:var(--acc)}
.runs-panel{margin:14px 0 6px;border:1px solid var(--line);border-radius:10px;background:var(--card)}
.runs-bar{display:flex;align-items:center;gap:8px;padding:8px 12px;font:13px/1.4 system-ui,sans-serif}
.runs-bar .runs-fold{padding:0 7px}
.runs-saved{padding:0 12px 10px;color:var(--mut);font:11.5px/1.5 system-ui,sans-serif}
.runs-saved code{font-size:11px} .runs-panel.folded .runs-saved{display:none}
.runs-panel.folded{cursor:pointer}
.runs-body{display:grid;grid-template-columns:minmax(150px,210px) minmax(0,1fr);gap:12px;padding:0 12px 12px}
.runs-panel.folded .runs-body{display:none}
.runs-types{display:flex;flex-direction:column;gap:6px}
.run-type{text-align:left;display:flex;justify-content:space-between}
.run-type[hidden]{display:none}
.run-type .run-count{color:var(--mut);font-weight:500}
.run-new{border-style:dashed!important}
.runs-detail{border:1px solid var(--line);border-radius:9px;padding:10px 12px;min-width:0}
.run-list{display:flex;flex-wrap:nowrap;overflow-x:auto;gap:4px;margin-bottom:8px;padding-bottom:2px}
.run-list[hidden]{display:none}
.run-list button{flex:none;font:500 11px ui-monospace,Menlo,monospace!important;padding:1px 6px!important}
.run-list button.on{border-color:var(--acc);color:var(--acc)}
.run-card header{display:flex;align-items:center;gap:8px}
.run-lbl{display:flex;flex-direction:column;min-width:0;text-align:left}
.run-list .run-row{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:0 8px;text-align:left;width:100%;
 font:600 12px ui-monospace,Menlo,monospace!important;padding:5px 10px!important}
.run-row-state{font:500 11px system-ui,sans-serif;color:var(--mut)}
.run-row-of{grid-column:1/-1;font:400 11px system-ui,sans-serif;color:var(--mut);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.runs-panel[data-compact] .run-card{margin-top:6px}
.run-list .run-more{background:none;border:0;padding:2px 0;color:var(--mut);font:400 12px system-ui,sans-serif;cursor:pointer;text-align:left}
/* compact (the frame): a small card, its prompt folded (Copy still works) (JL 261007: "it is just too big") */
.runs-panel[data-compact] .runs-detail{padding:8px 10px}
.runs-panel[data-compact] .run-card header b{font:600 12.5px system-ui,sans-serif}
.runs-panel[data-compact] .run-card h4,.runs-panel[data-compact] .run-prompt-box>summary{font-size:11.5px;margin:6px 0 2px}
.runs-panel[data-compact] .run-prompt{font-size:11px;padding:6px 8px}
.runs-panel[data-compact] .run-skill,.runs-panel[data-compact] .run-process{font-size:11.5px}
.run-name{font:600 12px ui-monospace,Menlo,monospace;overflow-wrap:anywhere}
.run-doing{font:400 11px system-ui,sans-serif;color:var(--mut)}
.run-of{margin:0 0 4px;color:var(--mut);font:600 11px system-ui,sans-serif;text-transform:uppercase;letter-spacing:.03em}
.runs-head{margin:10px 0 6px;font:13px/1.4 system-ui,sans-serif}.runs-sub{color:var(--mut);font-size:12px}
.run-card header .run-copy{margin-left:auto}
.run-skill{margin:6px 0 0;color:var(--mut);font-size:12px}.run-skill code{font-size:11.5px;color:var(--fg)}
/* The prompt folds (JL 260927); Copy works while it is folded. */
.run-prompt-box>summary{display:flex;align-items:center;gap:6px;margin:10px 0 4px;cursor:pointer;
 list-style:none;font:600 12px system-ui,sans-serif;text-transform:none;letter-spacing:normal;color:var(--fg)}
.run-prompt-box>summary::-webkit-details-marker{display:none}
.run-prompt-box>summary::before{content:"▸";color:var(--acc);width:10px}
.run-prompt-box[open]>summary::before{content:"▾"}
.run-prompt-box>summary .run-copy{margin-left:auto}
.run-card h4{display:flex;align-items:center;justify-content:space-between;margin:10px 0 4px;
 font:600 12px system-ui,sans-serif}
.run-sub,.run-process{color:var(--mut);font-size:12px;line-height:1.5;overflow-wrap:anywhere}
.run-prompt{white-space:pre-wrap;overflow-wrap:anywhere;margin:0;padding:7px 9px;border-radius:7px;
 background:color-mix(in srgb,var(--acc) 6%,var(--card));font:12px/1.5 ui-monospace,Menlo,monospace}
.run-results ul{margin:4px 0 0;padding-left:18px;font-size:12px}
.run-open{display:block;margin:0 0 6px;font-size:13px;font-weight:600}
.run-state{font:600 10.5px/1.4 system-ui,sans-serif;border-radius:5px;padding:1px 6px;
 border:1px solid var(--line);color:var(--mut)}
.run-state.st-awaiting-you{color:#2b8a3e;border-color:#2b8a3e}
.run-state.st-running{color:var(--acc);border-color:var(--acc)}
.run-empty{color:var(--mut);font-size:12px}
.paragraph-group.runs-selected>summary{outline:2px solid var(--acc);outline-offset:2px;border-radius:6px}
@media (max-width:700px){.runs-body{grid-template-columns:1fr}}
"""

# The Runs panel beside a Space, shared by every workbench (JL 261003: "always put the run in
# the right panel"): `<div class="split"><div class="space-main">content</div>{panel}</div>`.
# The content sits in one box; the panel stays on the right at every width and folds to a
# narrow vertical "◂ Runs" tab. First written in the Design workbench (design.py).
SPLIT_CSS = """
.split:not(.pane),.pane.on.split{display:flex;align-items:flex-start;gap:16px}
.split>.space-main{flex:1 1 auto;min-width:0;border:1px solid #e3e3e6;border-radius:10px;padding:12px 16px 16px}
.split>.space-main>h2:first-child,.split>.space-main>.views:first-child{margin-top:0}
@media(prefers-color-scheme:dark){.split>.space-main{border-color:#2c2e33}}
@media(max-width:520px){.split>.space-main{padding:10px}}
.split>.runs-panel{flex:0 0 clamp(260px,28vw,440px);margin:0;position:sticky;top:8px;
 max-height:calc(100vh - 16px);display:flex;flex-direction:column;overflow:hidden}
.split>.runs-panel .runs-bar{flex-wrap:wrap}
.split>.runs-panel .runs-body{overflow:auto;min-height:0;grid-template-columns:1fr}
.split>.runs-panel .runs-types{flex-direction:row;flex-wrap:wrap}
.split>.runs-panel .run-type{gap:8px}
.split>.runs-panel.folded{flex-basis:42px}
.split>.runs-panel.folded .runs-bar{writing-mode:vertical-rl;flex-wrap:nowrap;padding:10px 9px;gap:10px}
@media(max-width:900px){.split:not(.pane),.pane.on.split{gap:8px}.split>.runs-panel{flex-basis:clamp(200px,34vw,300px)}}
"""

PANEL_JS = r"""
(function(){
 function store(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v);}catch(e){return null;}}
 function copy(text,btn){
  function done(){var old=btn.textContent;btn.textContent='Copied';setTimeout(function(){btn.textContent=old;},1200);}
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(text).then(done,function(){fallback();});}
  else fallback();
  function fallback(){var t=document.createElement('textarea');t.value=text;document.body.appendChild(t);t.select();
   try{document.execCommand('copy');done();}catch(e){}document.body.removeChild(t);}
 }
 document.addEventListener('click',function(ev){
  var b=ev.target.closest('.run-copy');if(!b)return;
  ev.preventDefault();  /* a Copy inside a folded summary copies without opening it */
  var text=b.dataset.copy||'';
  if(!text){var pre=b.closest('.run-card')&&b.closest('.run-card').querySelector('.run-prompt');text=pre?pre.textContent:'';}
  /* a prompt box that takes notes (b15 s41-D14): the person's notes go with the prompt */
  var nb=b.closest('.run-prompt-box'),notes=nb&&nb.querySelector('textarea.run-notes');
  if(notes&&notes.value.trim())text+='\nuser feedback: '+notes.value.trim();
  /* then the lines that send it to its session, wherever it is pasted (JL 261020) */
  if(b.dataset.tail)text+='\n'+b.dataset.tail;
  copy(text,b);
 });
 /* the notes stay in this browser until sent; a pasted image is kept by the host and its path written in */
 document.querySelectorAll('textarea.run-notes[data-key]').forEach(function(t){
  var v=store(t.dataset.key);if(v&&!t.value)t.value=v;
  t.addEventListener('input',function(){store(t.dataset.key,t.value);});
 });
 document.addEventListener('paste',function(ev){
  var t=ev.target.closest&&ev.target.closest('textarea.run-notes[data-upload]');if(!t)return;
  var items=(ev.clipboardData&&ev.clipboardData.items)||[];
  for(var i=0;i<items.length;i++){if(items[i].type.indexOf('image/')!==0)continue;
   ev.preventDefault();var r=new FileReader();
   r.onload=function(){fetch(t.dataset.upload,{method:'POST',headers:{'Content-Type':'application/json'},
     body:JSON.stringify({folder:t.dataset.folder,data:r.result})}).then(function(x){return x.json();}).then(function(j){
     var line=j.ok?('🖼 an image, kept at '+j.path):('✗ the image was not kept: '+j.err);
     t.value=(t.value?t.value.replace(/\s*$/,'\n'):'')+line+'\n';store(t.dataset.key,t.value);});};
   r.readAsDataURL(items[i].getAsFile());return;}
 });
 /* a button that writes (data-post: a JSON body, plus the named inputs beside it) or reads into a target
    (data-fetch, with a fresh seed): an items Task's Sign, Agree and Draw again (b15 s41) */
 document.addEventListener('click',function(ev){
  var b=ev.target.closest('button[data-post]');if(!b)return;ev.preventDefault();
  var body={};try{body=JSON.parse(b.dataset.body||'{}');}catch(e){}
  var row=b.parentNode;(b.dataset.fields||'').split(' ').filter(Boolean).forEach(function(n){
   /* a tick box says whether it is ticked (a person's "I read it"), and is never remembered */
   var i=row.querySelector('[name="'+n+'"]');if(i){if(i.type==='checkbox'){body[n]=i.checked;return;}
    body[n]=i.value;store('sign:'+n,i.value);}});
  b.disabled=true;
  fetch(b.dataset.post,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})
   .then(function(x){return x.json();}).then(function(j){if(j.ok){location.reload();return;}
    b.disabled=false;b.title=j.err||'';b.textContent='✗ '+(j.err||'refused');});
 });
 document.querySelectorAll('input.sign-by').forEach(function(i){var v=store('sign:by');if(v&&!i.value)i.value=v;});
 document.addEventListener('click',function(ev){
  var b=ev.target.closest('button[data-fetch]');if(!b)return;ev.preventDefault();
  var t=document.getElementById(b.dataset.target);if(!t)return;
  var seed=Math.floor(Math.random()*1e6);
  fetch(b.dataset.fetch+'&seed='+seed).then(function(x){return x.text();}).then(function(h){t.innerHTML=h;});
 });
 function matches(card,target){
  if(!target)return true;
  var t=(card.dataset.targets||'').split(' ');
  return t.indexOf(target)>=0||t.some(function(x){return x.indexOf(target+'.')===0;});
 }
 /* data-views="" belongs everywhere; otherwise only to the views or tabs it names.
    A run type follows the view (Draft view, Evidence tab, Delivery view); a Delivery
    build card follows the format tab. */
 function inView(el,view){var v=(el.dataset.views||'').trim();return !v||!view||v.split(' ').indexOf(view)>=0;}
 function typeShown(el,p){var v=(el.dataset.views||'').trim();if(!v)return true;
  var names=v.split(' ');return names.indexOf(p.dataset.view||'')>=0||names.indexOf(p.dataset.mode||'')>=0;}
 function skillLine(sk,src){if(!sk)return;var names=(src&&src.dataset.skills||'').split(' · ').filter(Boolean);
  sk.innerHTML=names.length?'Skill '+names.map(function(n){return '<code>'+n.replace(/[<>&"]/g,'')+'</code>';}).join(' · '):'';
  sk.hidden=!names.length;}
 function typeLabel(p,type){var b=p.querySelector('.run-type[data-type="'+type+'"]');return b?b.dataset.label:'';}
 function render(p){
  var on=p.querySelector('.run-type.on'),newMode=on&&on.classList.contains('run-new');
  var target=p.dataset.target||'',view=p.dataset.view||'',list=p.querySelector('.run-list');
  var type=newMode?p.dataset.lastType:(on?on.dataset.type:'0');
  /* no run type here, or one with no prompt to start (a gate not passed yet): no "+ New Run" */
  var startable=p.querySelector('.run-type[data-type="'+type+'"]'),nb=p.querySelector('.run-new');
  if(nb)nb.hidden=!startable||startable.hidden||!startable.dataset.prompt;
  var cards=[].slice.call(p.querySelectorAll('.run-card[data-type="'+type+'"]'))
   .filter(function(c){return matches(c,target)&&inView(c,view);});
  /* each type counts the runs of the selected target (and view), not the whole list */
  p.querySelectorAll('.run-type[data-type]').forEach(function(b){var s=b.querySelector('.run-count');if(!s)return;
   s.textContent=[].filter.call(p.querySelectorAll('.run-card[data-type="'+b.dataset.type+'"]'),
    function(c){return matches(c,target)&&inView(c,view);}).length;});
  p.querySelectorAll('.run-card').forEach(function(c){c.hidden=true;});
  list.innerHTML='';p.querySelector('.run-empty').hidden=true;
  if(newMode){
   var src=p.querySelector('.run-type[data-type="'+type+'"]'),card=p.querySelector('.run-card-new');
   var what=target||(p.dataset.space==='delivery'?p.dataset.viewLabel:'')||p.dataset.whole||'the whole page';
   card.querySelector('.run-prompt').textContent=(src?src.dataset.prompt:'').replace(/\{target\}/g,what);
   skillLine(card.querySelector('.run-skill'),src);
   card.hidden=false;return;
  }
  p.dataset.lastType=type;
  /* a type with no run yet still names the skill that does its work (JL 260929) */
  if(!cards.length){var em=p.querySelector('.run-empty');
   skillLine(em.querySelector('.run-skill'),p.querySelector('.run-type[data-type="'+type+'"]'));em.hidden=false;return;}
  function showCard(c){cards.forEach(function(x){x.hidden=true;});c.hidden=false;
}
  /* compact (the frame): one row per run, every card closed until its row is clicked; a second
     click closes it again */
  var compact=p.dataset.compact==='1';
  cards.forEach(function(c,i){var b=document.createElement('button');b.type='button';b.title=c.dataset.run;
   if(compact){b.className='run-row';b.innerHTML='<span class=run-row-name></span><span class=run-row-state></span>'
     +'<small class=run-row-of></small>';
    b.querySelector('.run-row-name').textContent=c.dataset.name||c.dataset.run;
    b.querySelector('.run-row-state').textContent=(c.querySelector('.run-state')||{}).textContent||'';
    b.querySelector('.run-row-of').textContent=(c.querySelector('.run-of')||{}).textContent||'';}
   else b.textContent=c.dataset.name||c.dataset.run;
   b.addEventListener('click',function(){
    if(compact&&b.classList.contains('on')){c.hidden=true;b.classList.remove('on');return;}
    showCard(c);list.querySelectorAll('button').forEach(function(x){x.classList.remove('on');});b.classList.add('on');});
   if(i===0&&!compact)b.classList.add('on');list.appendChild(b);});
  /* compact: four rows, then "+N more", as the Disk part above pages its files (b12 s32, 261008) */
  var rows=[].slice.call(list.querySelectorAll('.run-row'));
  if(compact&&rows.length>4){rows.slice(4).forEach(function(r){r.hidden=true;});
   var more=document.createElement('button');more.type='button';more.className='run-more';
   more.textContent='+'+(rows.length-4)+' more';
   more.addEventListener('click',function(){rows.forEach(function(r){r.hidden=false;});more.remove();});
   list.appendChild(more);}
  list.hidden=compact?false:cards.length<2;  /* one run: its title already names it */
  if(!compact)showCard(cards[0]);
 }
 /* A view or tab shows only its own run types. It opens on a type with a run
    waiting for the person, else on one that has runs in this view, else on the
    first type that belongs to this view (Table opens on Structure revise). */
 function pickType(p){
  var view=p.dataset.view||'',buttons=[].slice.call(p.querySelectorAll('.run-type:not(.run-new)'));
  buttons.forEach(function(b){b.hidden=!typeShown(b,p);});
  var target=p.dataset.target||'';
  function live(b){return [].some.call(p.querySelectorAll('.run-card[data-type="'+b.dataset.type+'"]'),
   function(c){return matches(c,target)&&inView(c,view);});}
  /* a run waiting for the person first, then a type that has runs here, then a view-specific one */
  function score(b){return (+b.dataset.waiting>0?4:0)+(live(b)?2:0)+((b.dataset.views||'').trim()?1:0);}
  var best=null;
  buttons.forEach(function(b){if(!b.hidden&&(!best||score(b)>score(best)))best=b;});
  p.querySelectorAll('.run-type').forEach(function(x){x.classList.remove('on');});
  if(best)best.classList.add('on');
 }
 function setTarget(p,target){p.dataset.target=target||'';render(p);}
 function setView(p,view,label,mode){p.dataset.view=view||'';p.dataset.viewLabel=label||'';p.dataset.mode=mode||view||'';pickType(p);render(p);}
 var panels={};
 document.querySelectorAll('.runs-panel').forEach(function(p){
  var space=p.dataset.space,fold=p.querySelector('.runs-fold');panels[space]=p;
  function setFold(on){p.classList.toggle('folded',on);fold.textContent=on?'◂':'▸';store('runs-fold:'+space,on?'1':'0');}
  fold.addEventListener('click',function(ev){ev.stopPropagation();setFold(!p.classList.contains('folded'));});
  p.querySelector('.runs-bar').addEventListener('click',function(ev){
   if(p.classList.contains('folded')&&!ev.target.closest('input,button'))setFold(false);});
  var kept=store('runs-fold:'+space);
  if(kept==='1'||(kept!=='0'&&p.dataset.fold==='1'))setFold(true);
  p.querySelectorAll('.run-type').forEach(function(b){b.addEventListener('click',function(){
   p.querySelectorAll('.run-type').forEach(function(x){x.classList.remove('on');});b.classList.add('on');render(p);});});
  render(p);
 });
 document.addEventListener('space-scope',function(ev){var p=panels[ev.detail.space];if(p)setView(p,ev.detail.view,ev.detail.label,ev.detail.mode);});
 document.addEventListener('space-target',function(ev){var p=panels[ev.detail.space];if(p)setTarget(p,ev.detail.target);});
 var draft=panels.draft,lensDiv=document.getElementById('lens-div');
 if(draft&&lensDiv){
  setView(draft,lensDiv.dataset.draftMode||'table','');
  document.querySelectorAll('.draft-mode-tab').forEach(function(b){
   b.addEventListener('click',function(){setView(draft,b.dataset.draftMode,'');});});
 }
 document.addEventListener('click',function(ev){
  if(!draft||ev.target.closest('.runs-panel,button,a,input,textarea,select,[contenteditable],.structure-card'))return;
  var g=ev.target.closest('.paragraph-group[data-paragraph]');if(!g)return;
  var same=g.classList.contains('runs-selected');
  document.querySelectorAll('.paragraph-group.runs-selected').forEach(function(x){x.classList.remove('runs-selected');});
  if(!same)g.classList.add('runs-selected');
  setTarget(draft,same?'':(g.dataset.paragraph||''));
 });
})();
"""
