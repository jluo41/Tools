"""HTML page templates of the paper workbench: the classic Board page (_PAGE) and one Run's result page (_RESULT_PAGE).
Plain str.format templates moved verbatim from paper.py, which re-exports both; nothing here reads a file."""

_PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>
:root{{--bg:#ffffff;--fg:#1c1c1c;--mut:#7c7c78;--line:#e4e4e7;--card:#fff;
 --warn:#b3541e;--ok:#3a7d44;--acc:#3e5c84;--soft:#f6f7f9}}
@media(prefers-color-scheme:dark){{:root{{--bg:#161719;--fg:#e8e8e6;
 --mut:#9a9a97;--line:#2c2e33;--card:#1d1f23;--warn:#e0955a;--ok:#7dbb87;
 --acc:#7d9cc4;--soft:#1b1d21}}}}
body{{margin:0;padding:18px;background:var(--bg);color:var(--fg);
 font:16px/1.65 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}
h1{{font-size:20px;margin:0 0 2px}} .mut{{color:var(--mut)}}
.spaces{{display:flex;gap:6px;margin:10px 0 10px;flex-wrap:wrap}}
.space{{font:600 13px -apple-system,sans-serif;border:1px solid var(--line);border-radius:9px;padding:5px 12px;
 cursor:pointer;background:var(--card);color:var(--fg);white-space:nowrap}}
.space.on{{border-color:var(--acc);color:var(--acc)}}
.panel{{display:none}} .panel.on{{display:block}}
.panel.on.space-split{{display:flex;align-items:flex-start;gap:16px}}
.space-views[hidden]{{display:none}}
.space-frame{{height:calc(100vh - 170px)}}
.space-h{{font-size:15px;margin:18px 0 6px}} .space-h:first-child{{margin-top:0}}
.story-name{{font:600 13px ui-monospace,Menlo,monospace;color:var(--mut);margin:14px 0 6px}}
.ok{{color:var(--ok);font-weight:600}} .warn{{color:var(--warn);font-weight:600}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin:0 0 14px}}
.card h2{{font-size:17px;margin:0 0 8px;display:flex;gap:8px;align-items:baseline}}
.card h2 .tally{{margin-left:auto;flex:none;font-size:13px;font-weight:500}}
.spine-card{{cursor:pointer}}
/* inside the Space's one box a Spine division is a row, not a second box (JL 260929) */
.space-main .spine-card{{border:0;border-bottom:1px solid var(--line);border-radius:0;padding:12px 4px 14px;margin:0}}
.space-main .spine-card:last-child{{border-bottom:0}}
.runs-selected.spine-card,.item-card.runs-selected{{border-color:var(--acc);box-shadow:0 0 0 1px var(--acc)}}
table.grid{{width:100%;font-size:14.5px;line-height:1.55;border:1px solid var(--line);border-radius:9px;
 border-collapse:separate;border-spacing:0;overflow:hidden;margin:6px 0 12px}}
table.grid th{{text-align:left;background:var(--soft);font:600 11.5px -apple-system,sans-serif;text-transform:uppercase;
 letter-spacing:.03em;padding:9px 11px;border-bottom:1px solid var(--line);border-right:1px solid var(--line);opacity:.8}}
table.grid td{{padding:9px 11px;border-bottom:1px solid var(--line);border-right:1px solid var(--line);vertical-align:top}}
table.grid th:last-child,table.grid td:last-child{{border-right:0}} table.grid tr:last-child td{{border-bottom:0}}
.idtag,.path{{font:500 12.5px ui-monospace,Menlo,monospace;color:var(--mut)}} .path{{overflow-wrap:anywhere}}
.bjt-chev{{color:var(--mut);display:inline-block;width:1em;text-align:center;transition:transform .12s ease}}
.qc>summary{{list-style:none;cursor:pointer}} .qc>summary::-webkit-details-marker{{display:none}}
.qc[open]>summary .bjt-chev{{transform:rotate(90deg)}}
/* Story › High-level logic + Low-level work: one tree, split down the middle (JL 260929) */
.lw{{border:1px solid var(--line);border-radius:12px;overflow:hidden;background:var(--card)}}
.lw-row{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr)}}
.lw-row.lw-3{{grid-template-columns:minmax(0,1fr) minmax(0,1fr) minmax(0,.72fr)}}
.lw-p{{padding:7px 14px;border-left:1px solid var(--line);min-width:0}} .lw-g>.lw-p{{padding-top:0;padding-bottom:10px}}
.lw-rstate{{font-size:13px;font-weight:600}} .lw-rstate.ok{{color:var(--ok)}} .lw-rstate.warn{{color:var(--warn)}} .lw-rstate.mut{{color:var(--mut)}}
.lw-l{{padding:7px 14px;min-width:0}} .lw-r{{padding:7px 14px;border-left:1px solid var(--line);min-width:0}}
.lw-head{{background:var(--soft);border-bottom:1px solid var(--line);font:700 12px -apple-system,sans-serif;
 text-transform:uppercase;letter-spacing:.04em;color:var(--mut)}}
.lw-q+.lw-q{{border-top:1px solid var(--line)}}
.lw-q>summary{{display:flex;gap:8px;align-items:baseline;padding:12px 14px;margin-bottom:6px;font-weight:650;font-size:15.5px;line-height:1.45;
 background:var(--soft);border-bottom:1px solid var(--line)}}

.lw-qhead{{flex:1 1 0;min-width:0}} .lw-qtop{{display:flex;gap:8px;align-items:baseline;flex-wrap:wrap}} .lw-qname{{font-weight:700}} .lw-q .lw-qtext{{display:block;margin-top:4px;font-weight:500}}
.lw-q>summary:hover{{background:color-mix(in srgb,var(--acc) 5%,var(--soft))}}
/* a pick draws nothing (JL 260930, the blue bar: "I don't want this as well"); an open item shows it */
.lw-h.runs-selected,.lw-w.runs-selected{{background:transparent}}
.lw-g .lw-l{{padding-left:40px}} .lw-g>.lw-l,.lw-g>.lw-r{{padding-top:0;padding-bottom:10px}}
.lw-k{{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 10px;margin:16px 0 8px;padding:6px 10px;
 border-radius:7px;font:700 12.5px -apple-system,sans-serif;text-transform:uppercase;letter-spacing:.05em}}
.lw-l>.lw-k:first-child,.lw-r>.lw-k:first-child{{margin-top:4px}}
.lw-kn{{font-weight:500;text-transform:none;letter-spacing:0;opacity:.85}}
.lw-k-task,.lw-k-hyp,.lw-k-work{{color:var(--acc)}}
.lw-k-claim{{color:var(--ok)}}
.lw-k-contrib{{color:var(--warn)}}
.lw-k-found{{color:var(--mut)}}
.lw-c{{margin:0 0 16px}} .lw-g+.lw-g{{margin-top:22px}}
{work_item_css}
.lw-h{{cursor:pointer;border-radius:7px;padding:5px 8px;margin:0 -8px 6px}} .lw-h:hover{{background:var(--soft)}}
.lw-say{{color:var(--mut);font-size:14px;line-height:1.5;margin-top:3px}}
.lw-text{{font-size:14.5px}}
.lw-hline{{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:8px;align-items:baseline;line-height:1.45}}
.lw-top{{display:flex;justify-content:space-between;align-items:center;gap:8px}} .lw-body{{margin-top:3px;font-size:15px;line-height:1.5}} .lw-name{{font-weight:650}} .lw-mark{{font-size:14px}}
#rr-pop{{position:fixed;inset:0;z-index:50;background:rgba(0,0,0,.35);display:flex;align-items:center;justify-content:center}}
#rr-pop[hidden]{{display:none}}
.rr-box{{width:min(1240px,94vw);height:90vh;background:var(--bg);border:1px solid var(--line);border-radius:12px;display:flex;flex-direction:column;overflow:hidden;box-shadow:0 12px 40px rgba(0,0,0,.25)}}
.rr-box>header{{display:flex;gap:14px;align-items:center;padding:10px 14px;border-bottom:1px solid var(--line)}}
.rr-title{{font:600 14px ui-monospace,Menlo,monospace}} .rr-new{{margin-left:auto;font-size:13px}}
.rr-x{{border:0;background:transparent;color:inherit;font-size:18px;line-height:1;cursor:pointer;padding:2px 6px}}
.rr-frame{{flex:1;width:100%;border:0;background:var(--bg)}}
/* Story › Related Papers: one card per paper, the target venue first, its PDF inside (JL 260930) */
.rp-head{{font:700 12px -apple-system,sans-serif;text-transform:uppercase;letter-spacing:.04em;color:var(--mut);margin:0 0 2px}}
.rp-venue{{display:flex;gap:10px;align-items:baseline;margin:22px 0 4px;padding-bottom:6px;border-bottom:1px solid var(--line);
 font-size:16px;font-weight:700}} .rp-list>.rp-venue:first-of-type{{margin-top:8px}}
.rp-group{{border:1px solid var(--line);border-radius:10px;background:var(--card);overflow:hidden;margin:0 0 4px}}
.rp-card+.rp-card{{border-top:1px solid var(--line)}}
.rp-card>summary{{list-style:none;cursor:pointer;display:grid;grid-template-columns:1em minmax(0,1fr);gap:6px;align-items:baseline;padding:10px 14px}}
.rp-card>summary::-webkit-details-marker{{display:none}} .rp-card[open]>summary .bjt-chev{{transform:rotate(90deg)}}
.rp-card>summary:hover,.rp-card[open]>summary{{background:var(--soft)}}
.rp-title{{font-weight:600;font-size:14.5px;line-height:1.4}}
.rp-sub{{display:flex;justify-content:space-between;align-items:baseline;gap:12px;margin-top:2px;font-size:13px;color:var(--mut)}}
.rp-marks{{display:flex;gap:10px;flex:none}} .rp-q{{color:var(--acc);font-weight:600}}
.rp-body{{padding:6px 14px 14px calc(14px + 1em + 6px)}}
.rp-why{{font-size:14.5px;line-height:1.55;margin:4px 0 6px}}
.rp-keep{{border:1px solid var(--line);border-left:3px solid var(--acc);border-radius:8px;background:var(--soft);padding:8px 12px;margin:4px 0 10px}}
.rp-keep-h{{font:700 12px -apple-system,sans-serif;text-transform:uppercase;letter-spacing:.04em;color:var(--mut)}}
.rp-keep>p{{font-size:14.5px;line-height:1.55;margin:4px 0 0}}
.rp-bears{{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0 2px}}
.rp-bear{{font-size:12.5px;padding:1px 8px;border-radius:10px;border:1px solid var(--line);background:var(--card)}}
.rp-bear-ok{{color:var(--ok)}} .rp-bear-warn{{color:var(--warn)}} .rp-bear-bad{{color:#c92a2a}} .rp-bear-acc{{color:var(--acc)}} .rp-bear-mut{{color:var(--mut)}}
.rp-lw{{border:1px solid var(--line);border-radius:8px;overflow:hidden;margin:4px 0 10px}}
.rp-lw .lw-row+.lw-row{{border-top:1px solid var(--line)}} .rp-lw .lw-c{{margin:0}} .rp-lw .lw-c+.lw-c{{margin-top:8px}}
.rp-acts{{display:flex;gap:6px 16px;flex-wrap:wrap;font-size:13.5px;margin:0 0 6px}}
.rp-absd>summary,.rp-lwd>summary{{cursor:pointer;font-size:13.5px;color:var(--mut)}} .rp-lwd{{margin:4px 0 10px}} .rp-lwd>.rp-lw{{margin-top:6px}} .rp-absd>p{{font-size:14px;line-height:1.55;margin:6px 0 0}}
.rp-nopdf{{font-size:13.5px;margin-top:8px}}
.rd-bar{{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:0 0 8px}} .rd-open{{margin-left:auto;font-size:13px}}
.rd-file{{border:1px solid var(--line);background:transparent;color:inherit;border-radius:999px;padding:3px 10px;font:inherit;font-size:13px;cursor:pointer}}
.rd-file.on{{border-color:var(--acc);color:var(--acc);font-weight:600}}
.rd-frame{{display:block;width:100%;height:calc(100vh - 190px);min-height:560px;border:1px solid var(--line);border-radius:8px;background:#fff}}
.rp-frame{{display:block;width:100%;height:82vh;border:1px solid var(--line);border-radius:8px;background:#fff;margin-top:8px}}
/* Logic beside its work at every width (JL 261003: "always be two columns no matter of the page width") */
code{{font:12.5px ui-monospace,Menlo,monospace}}
.sec-list{{display:grid;border:1px solid var(--line);border-radius:10px;overflow:hidden}}
.sec-row{{display:grid;grid-template-columns:2.4em minmax(0,1fr) 4.5em 12em 4.5em;gap:10px;align-items:baseline;
 padding:9px 12px;border-top:1px solid var(--line);cursor:pointer}}
.sec-row:first-child{{border-top:0}}
.sec-row:hover{{background:var(--soft)}}
.sec-row.runs-selected{{background:transparent;box-shadow:inset 3px 0 0 var(--acc)}}
.sec-num,.sec-ver{{font:500 13px ui-monospace,Menlo,monospace;color:var(--mut)}} .sec-name{{font-weight:600}}
.sec-state{{font-size:13px;white-space:nowrap}} .sec-state.ok,.sec-state.warn{{font-weight:500}} .sec-open{{font-size:13px;text-align:right;white-space:nowrap}}
.item-cards{{display:grid;gap:9px;margin:0 0 12px}}
.item-card{{border:1px solid var(--line);border-radius:10px;background:var(--bg);overflow:hidden;margin:0}}
.item-card:hover{{border-color:#b8c4d2}}
.item-card>summary{{list-style:none;cursor:pointer;padding:0}}
.item-card>summary::-webkit-details-marker{{display:none}}
.item-summary{{display:grid;grid-template-columns:1.1em auto minmax(0,1fr) auto fit-content(34%);align-items:start;gap:10px;padding:12px 13px;min-width:0}}
.item-chevron{{color:var(--mut);font-size:18px;line-height:1.2;transition:transform .12s ease}}
.item-card[open]>summary .item-chevron{{transform:rotate(90deg)}}
.item-main{{min-width:0;display:grid}}
.item-label{{font-weight:650;font-size:15.5px;line-height:1.4}} .item-title{{color:var(--mut);font-size:13.5px}}
.item-where{{color:var(--mut);font-size:12px;white-space:nowrap}} .item-status{{font-weight:650;font-size:14px;line-height:1.4;overflow-wrap:anywhere}}
.item-detail{{border-top:1px solid var(--line);padding:10px 12px 13px}}
.item-detail td .idtag,.item-detail td:first-child{{white-space:nowrap}}
.row-details{{margin-top:8px}} .row-details>summary{{cursor:pointer;color:var(--mut);font-size:12px;list-style:none}}
.row-details>summary::before{{content:"▸ "}} .row-details[open]>summary::before{{content:"▾ "}}
.item-bullets{{margin:0;padding-left:1.1em;font-size:14.5px}} .item-bullets li{{margin:2px 0}}
.item-bullets b{{font:500 12px ui-monospace,Menlo,monospace;color:var(--mut)}}
.item-note{{color:var(--mut);font-size:12.5px;line-height:1.45}} .item-sub{{color:var(--mut);font-size:12px;text-transform:uppercase;margin-right:4px}}
.item-plan>summary{{cursor:pointer;color:var(--mut);font-size:13px}}
.kv{{border:1px solid var(--line);border-radius:9px;overflow:hidden;margin:8px 0 10px;background:var(--card)}}
.kv>.item-row{{display:grid;grid-template-columns:11.5em minmax(0,1fr);border-top:1px solid var(--line);font-size:14.5px;line-height:1.6}}
.kv>.item-row:first-child{{border-top:0}}
.kv>.item-row>b{{background:var(--soft);border-right:1px solid var(--line);padding:11px 12px;font-size:11.5px;line-height:1.45;
 text-transform:uppercase;letter-spacing:.03em;font-weight:700;opacity:.75}}
.kv>.item-row>span{{padding:10px 14px;min-width:0;overflow-wrap:anywhere}}
.kv>.item-row.spine-row{{font-size:16px;line-height:1.75}}
.kv>.item-row.nolabel{{grid-template-columns:minmax(0,1fr)}}
.kv-cap{{background:var(--soft);border-bottom:1px solid var(--line);padding:6px 12px;font:700 11.5px -apple-system,sans-serif;
 text-transform:uppercase;letter-spacing:.03em;opacity:.75}}
.para{{display:block;max-width:86ch}} .para+.para{{margin-top:12px}} .sent{{display:block}} .sent+.sent{{margin-top:7px}}
.tree-job{{font-size:14.5px;margin:12px 0 4px;font-weight:650}} .tree-task{{font-size:14px;margin:8px 0 4px 18px}}
.tree-runs{{margin:0 0 6px 36px;border-left:2px solid var(--line);padding-left:10px}}
a{{color:var(--acc);text-decoration:none}} a:hover{{text-decoration:underline}}
@media(max-width:620px){{.kv>.item-row{{grid-template-columns:minmax(0,1fr)}}
 .kv>.item-row>b{{border-right:0;border-bottom:1px solid var(--line);padding:6px 12px}}
 .sec-row{{grid-template-columns:2em minmax(0,1fr) auto}} .sec-ver,.sec-state{{display:none}}
 .item-summary{{grid-template-columns:1.1em auto minmax(0,1fr) fit-content(40%)}} .item-where{{display:none}}}}
{space_css}{panel_css}
/* the paper's 12px type floor (JL 260918) holds inside the Runs panel too */
.runs-panel button,.run-list button{{font-size:12px!important}} .run-state{{font-size:12px}} .space-views-label{{font-size:12px}}
</style></head><body data-paper="{paper_id}">
<h1>📄 {title}</h1>
<div class="wb-band">{band}</div>
<div class="spaces">{space_chips}</div>
{panels}
<div id="rr-pop" hidden><div class="rr-box" role="dialog" aria-label="Run results"><header><span class="rr-title"></span>
<a class="rr-new" target="_blank" rel="noopener">Open in its own tab ↗</a><button type=button class="rr-x" title="Close (Esc)">✕</button></header>
<iframe class="rr-frame" title="Run results"></iframe></div></div>
<script>{panel_js}</script>
<script>
(function(){{
 var DEFAULT='{default_space}';
 /* the pre-260927 routes (five Spaces) still land on the view that holds their content */
 var ALIAS={{'setup':'sections','run':'sections','run/page':'sections/table','run/evidence':'sections/evidence',
  'run/supporting':'story/logic-work','run/gates':'delivery/latex/checks','run/workflow':'story',
  'story/questions':'story/logic-work',
  'ideation/pool':'ideation','ideation/evidence':'ideation','ideation/admission':'ideation',
  'story/claims':'story/logic-work','story/tasks':'story/logic-work','story/roadmap':'story/logic-work',
  'story/sections':'sections/narrative',
  'story/evidence':'sections/evidence','delivery/manuscript':'delivery/latex/artifacts',
  'delivery/sections':'sections/table','delivery/displays':'delivery/latex/artifacts',
  'delivery/checks':'delivery/latex/checks','setup/sessions':'sections/narrative'}};
 var panels={{}};
 document.querySelectorAll('.panel[data-space]').forEach(function(p){{panels[p.dataset.space]=p;}});
 function emit(name,detail){{document.dispatchEvent(new CustomEvent(name,{{detail:detail}}));}}
 function clearSel(p){{p.querySelectorAll('.runs-selected,.lw-lit').forEach(function(x){{x.classList.remove('runs-selected','lw-lit');}});}}
 function lazy(p){{p.querySelectorAll('iframe[data-src]').forEach(function(f){{
  if(!f.closest('[hidden]')&&!f.getAttribute('src'))f.setAttribute('src',f.dataset.src);}});}}
 function pick(space,parts){{
  var p=panels[space];if(!p)return;
  document.querySelectorAll('.space').forEach(function(c){{c.classList.toggle('on',c.dataset.space===space);}});
  Object.keys(panels).forEach(function(k){{panels[k].classList.toggle('on',k===space);}});
  var tabs=[].slice.call(p.querySelectorAll('.space-tab')),views=[].slice.call(p.querySelectorAll('.space-view'));
  function has(list,key,v){{return list.some(function(x){{return x.dataset[key]===v;}});}}
  function cur(list,key){{var on=list.filter(function(x){{return x.classList.contains('on');}})[0]||list[0];return on?on.dataset[key]:'';}}
  var tab=cur(tabs,'tab'),view=cur(views,'view');
  parts.forEach(function(x){{if(has(tabs,'tab',x))tab=x;else if(has(views,'view',x))view=x;}});
  tabs.forEach(function(x){{x.classList.toggle('on',x.dataset.tab===tab);}});
  views.forEach(function(x){{x.classList.toggle('on',x.dataset.view===view);}});
  var tb=tabs.filter(function(x){{return x.dataset.tab===tab;}})[0],noviews=!!(tb&&tb.hasAttribute('data-noviews'));
  var row=p.querySelector('.space-views');if(row)row.hidden=noviews;
  p.querySelectorAll('.space-pane').forEach(function(q){{
   q.hidden=!((!q.dataset.tab||q.dataset.tab===tab)&&(noviews||!q.dataset.view||q.dataset.view===view));}});
  lazy(p);
  if(p.dataset.tab!==tab||p.dataset.vw!==view){{
   if(p.dataset.tab!==undefined){{clearSel(p);emit('space-target',{{space:space,target:''}});}}
   p.dataset.tab=tab;p.dataset.vw=view;}}
  emit('space-scope',{{space:space,view:tab||view,label:tb?tb.dataset.label:'',mode:noviews?tab:(view||tab)}});
 }}
 function route(){{
  var h=decodeURIComponent((location.hash||'').slice(1));
  if(ALIAS[h])h=ALIAS[h];else if(ALIAS[h.split('/')[0]])h=ALIAS[h.split('/')[0]];
  var parts=h.split('/');
  pick(panels[parts[0]]?parts[0]:DEFAULT,parts.slice(1));
 }}
 document.addEventListener('click',function(ev){{
  var c=ev.target.closest('.space,.space-tab,.space-view');
  if(c){{
   var p=c.closest('.panel'),space=c.dataset.space||(p&&p.dataset.space);
   var parts=c.dataset.space?[]:[c.dataset.tab||c.dataset.view];
   pick(space,parts);
   var q=panels[space],t=q.dataset.tab,v=q.dataset.vw;
   history.replaceState(null,'','#'+space+(t?'/'+t:'')+(v?'/'+v:''));
   return;
  }}
  /* a fold of the Questions tree starts closed: a click on a closed fold opens and selects it; on an open, unselected fold it selects; on the selected fold it closes */
  var sm=ev.target.closest('details.qc[data-key]>summary');
  if(sm&&!ev.target.closest('a,button')){{
   var f=sm.parentElement,fp=f.closest('.panel');
   if(!f.open||!f.classList.contains('runs-selected')){{
    if(f.open)ev.preventDefault();
    clearSel(fp);f.classList.add('runs-selected');emit('space-target',{{space:fp.dataset.space,target:f.dataset.key}});return;}}
   f.classList.remove('runs-selected');
   var above=f.parentElement.closest('details.qc[data-key][open],details.item-card[data-key][open]');
   if(above)above.classList.add('runs-selected');
   emit('space-target',{{space:fp.dataset.space,target:above?above.dataset.key:''}});return;
  }}
  if(ev.target.closest('a,button,summary,.runs-panel'))return;
  var el=ev.target.closest('.sec-row[data-key],.spine-card[data-key],.lw-h[data-key],.lw-w[data-key]');if(!el)return;
  var panel=el.closest('.panel'),same=el.classList.contains('runs-selected');
  clearSel(panel);if(!same)el.classList.add('runs-selected');
  if(!same&&el.classList.contains('lw-h')){{var blk=el.closest('.lw-q')||panel,k=' '+el.dataset.key+' ';
   blk.querySelectorAll('.lw-w[data-for]').forEach(function(w){{if((' '+w.dataset.for+' ').indexOf(k)>=0){{w.classList.add('lw-lit');
    if(!w.open){{auto.add(w);w.open=true;}}}}}});}}
  emit('space-target',{{space:panel.dataset.space,target:same?'':el.dataset.key}});
 }});
 document.addEventListener('keydown',function(ev){{var r=ev.target.closest&&ev.target.closest('.sec-row');if(r&&ev.key==='Enter')r.click();}});
 /* RoadMap Draw: another drawing in studio/ swaps the canvas and the full-screen link */
 document.addEventListener('click',function(ev){{var b=ev.target.closest&&ev.target.closest('.rd-file');if(!b)return;
  var w=b.closest('.space-pane');w.querySelectorAll('.rd-file').forEach(function(x){{x.classList.toggle('on',x===b);}});
  var f=w.querySelector('.rd-frame'),a=w.querySelector('.rd-open');f.dataset.src=b.dataset.src;f.setAttribute('src',b.dataset.src);
  if(a)a.setAttribute('href',b.dataset.src);}});
 /* Opening a card selects it for the Runs panel; closing it hands the selection back to the card around it. */
 var auto=new WeakSet();   /* work a picked hypothesis opened: its toggle must not steal the pick */
 document.addEventListener('toggle',function(ev){{
  var w=ev.target;
  /* a related paper's PDF loads only when its card opens (data-pdf, so lazy() leaves it alone) */
  if(w.matches&&w.matches('details.rp-card')){{var f=w.open&&w.querySelector('iframe[data-pdf]');
   if(f&&!f.getAttribute('src'))f.setAttribute('src',f.dataset.pdf);return;}}
  if(w.matches&&w.matches('details.lw-w[data-key]')){{
   if(auto.has(w)){{auto.delete(w);return;}}
   var wp=w.closest('.panel');if(!wp)return;
   if(w.open){{clearSel(wp);w.classList.add('runs-selected');emit('space-target',{{space:wp.dataset.space,target:w.dataset.key}});}}
   else if(w.classList.contains('runs-selected')){{w.classList.remove('runs-selected');emit('space-target',{{space:wp.dataset.space,target:''}});}}
   return;}}
  var c=ev.target;if(!c.matches||!c.matches('details.item-card[data-key]'))return;
  var p=c.closest('.panel');if(!p)return;
  if(c.open){{clearSel(p);c.classList.add('runs-selected');emit('space-target',{{space:p.dataset.space,target:c.dataset.key}});return;}}
  var held=c.querySelector('.runs-selected');
  if(!c.classList.contains('runs-selected')&&!held)return;
  c.classList.remove('runs-selected');if(held)held.classList.remove('runs-selected');
  var up=c.parentElement.closest('details.item-card[data-key][open]');
  if(up)up.classList.add('runs-selected');
  emit('space-target',{{space:p.dataset.space,target:up?up.dataset.key:''}});
 }},true);
 /* a run's results open in a pop-out over the page (JL 260930); a modified click or
    "Open in its own tab" keeps the page, and Esc or a click outside closes it */
 var pop=document.getElementById('rr-pop');
 function popClose(){{pop.hidden=true;pop.querySelector('.rr-frame').removeAttribute('src');}}
 document.addEventListener('click',function(ev){{
  var a=ev.target.closest&&ev.target.closest('a[data-pop]');
  if(a&&!ev.metaKey&&!ev.ctrlKey&&!ev.shiftKey&&!ev.altKey&&ev.button===0){{
   ev.preventDefault();ev.stopPropagation();
   pop.querySelector('.rr-title').textContent=a.dataset.pop;pop.querySelector('.rr-new').href=a.href;
   pop.querySelector('.rr-frame').src=a.href;pop.hidden=false;return;}}
  if(!pop.hidden&&(ev.target===pop||(ev.target.closest&&ev.target.closest('.rr-x')))){{ev.stopPropagation();popClose();}}
 }},true);
 document.addEventListener('keydown',function(ev){{if(ev.key==='Escape'&&!pop.hidden)popClose();}});
 window.addEventListener('hashchange',route);route();
}})();
</script></body></html>"""


_RESULT_PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>
:root{{--bg:#fff;--fg:#1c1c1c;--mut:#7c7c78;--line:#e4e4e7;--acc:#3e5c84;--soft:#f6f7f9}}
@media(prefers-color-scheme:dark){{:root{{--bg:#161719;--fg:#e8e8e6;--mut:#9a9a97;--line:#2c2e33;--acc:#7d9cc4;--soft:#1b1d21}}}}
body{{margin:0;padding:18px 22px 40px;background:var(--bg);color:var(--fg);font:15px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}
h1{{font-size:20px;margin:0 0 2px}} h2{{font-size:16px;margin:26px 0 8px;padding-top:12px;border-top:1px solid var(--line)}}
h3,h4,h5,h6{{font-size:14.5px;margin:14px 0 6px}} .mut{{color:var(--mut)}} a{{color:var(--acc)}}
.where{{margin:0 0 6px}} .links{{display:flex;gap:16px;flex-wrap:wrap;font-size:14px}}
code,pre{{font:12.5px/1.5 ui-monospace,Menlo,monospace}} pre{{background:var(--soft);padding:10px 12px;border-radius:8px;overflow:auto}}
.doc{{border:1px solid var(--line);border-radius:10px;padding:4px 16px 10px;margin:0 0 14px}}
.doc>h3:first-child{{font:600 13px ui-monospace,Menlo,monospace;color:var(--mut)}}
.figs{{display:grid;grid-template-columns:repeat(auto-fill,minmax(420px,1fr));gap:16px}}
figure{{margin:0;border:1px solid var(--line);border-radius:10px;padding:10px;background:#fff}}
.doc figure{{margin:10px 0;max-width:920px}} figure img{{width:100%;height:auto;display:block}} figcaption{{font:12px ui-monospace,Menlo,monospace;color:#555;margin-top:6px;word-break:break-all}}
.tw{{overflow:auto;max-height:420px;border:1px solid var(--line);border-radius:8px}}
table{{border-collapse:collapse;font-size:13px}} th,td{{border-bottom:1px solid var(--line);padding:4px 10px;text-align:left;white-space:nowrap}}
th{{position:sticky;top:0;background:var(--soft)}} .doc table{{margin:8px 0}}
ul.files{{list-style:none;padding:0;margin:0}} ul.files li{{font:13px ui-monospace,Menlo,monospace;padding:2px 0}}
</style></head><body>
{body}
</body></html>"""
