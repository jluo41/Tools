
(function(){'use strict';
var boot=JSON.parse(document.getElementById('labeling-boot').textContent);
var spaces=boot.spaces, key='labeling-view:'+boot.identity;
function $(s,r){return (r||document).querySelector(s);} function $$(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s));}
function esc(v){return String(v==null?'':v).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];});}
/* ── Space and view selection ─────────────────────────────── */
function select(space,view,remember){
 if(!spaces[space]){space=boot.default_space;}
 if(spaces[space].indexOf(view)<0){view=spaces[space][0];}
 $$('.space').forEach(function(b){var on=b.dataset.space===space;b.classList.toggle('on',on);b.setAttribute('aria-selected',on?'true':'false');b.tabIndex=on?0:-1;});
 $$('.panel').forEach(function(p){p.hidden=p.dataset.space!==space;});
 $$('.chip').forEach(function(c){if(c.dataset.space===space){c.classList.toggle('on',c.dataset.view===view);}});
 $$('.pane').forEach(function(p){p.hidden=!(p.dataset.space===space&&p.dataset.view===view);});
 runsFor(space,view);
 if(remember){try{localStorage.setItem(key,JSON.stringify({space:space,view:view}));}catch(e){}
  try{var u=new URL(location.href);u.searchParams.set('space',space);u.searchParams.set('view',view);history.replaceState(null,'',u.toString());}catch(e){}}
 current={space:space,view:view};
}
var current={};
$$('.space').forEach(function(b){b.addEventListener('click',function(){select(b.dataset.space,null,true);});
 b.addEventListener('keydown',function(e){var ids=Object.keys(spaces),i=ids.indexOf(b.dataset.space);
  if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();var n=ids[(i+(e.key==='ArrowRight'?1:ids.length-1))%ids.length];select(n,null,true);$('#tab-'+n).focus();}});});
$$('.chip').forEach(function(c){c.addEventListener('click',function(){select(c.dataset.space,c.dataset.view,true);});});
/* ── Runs panel: the shared one (live.runs_panel PANEL_JS). Choosing a view scopes it
   (space-scope); a round or a build in the content picks its run, and a run picks its round. ── */
var quiet=false;
function visibleCard(p){return $$('.run-card[data-op]',p).filter(function(c){return !c.hidden;})[0];}
function runsWant(space,target){var p=$('.runs-panel[data-space="'+space+'"]');if(!p||!target){return;}
 var shown=visibleCard(p);if(shown&&shown.dataset.target===target){return;}
 var card=$$('.run-card[data-op]',p).filter(function(c){var b=$('.run-type[data-type="'+c.dataset.type+'"]',p);
  return c.dataset.target===target&&b&&!b.hidden;})[0];if(!card){return;}
 quiet=true;
 try{var type=$('.run-type[data-type="'+card.dataset.type+'"]',p);if(!type.classList.contains('on')){type.click();}
  var pick=$$('.run-list button',p).filter(function(b){return b.title===card.dataset.run;})[0];if(pick){pick.click();}}
 finally{quiet=false;}}
function runsFor(space,view){var chip=$('.chip[data-space="'+space+'"][data-view="'+view+'"]');
 document.dispatchEvent(new CustomEvent('space-scope',{detail:{space:space,view:view,label:chip?chip.textContent:'',mode:view}}));}
document.addEventListener('click',function(ev){if(quiet||!ev.target.closest){return;}
 var hit=ev.target.closest('.runs-panel .run-list button,.runs-panel .run-type:not(.run-new)');if(!hit){return;}
 var p=hit.closest('.runs-panel'),c=visibleCard(p);
 if(c&&c.dataset.target){document.dispatchEvent(new CustomEvent('labeling:run',{detail:{space:p.dataset.space,op:c.dataset.op,target:c.dataset.target}}));}});
function roundLight(target){$$('details.roundbox').forEach(function(d){d.classList.toggle('on',d.dataset.target===target);});}
$$('details.roundbox').forEach(function(d){d.addEventListener('toggle',function(){
 if(d.open){roundLight(d.dataset.target);runsWant('labeling',d.dataset.target);}});});
document.addEventListener('labeling:run',function(e){var d=$$('details.roundbox').filter(function(x){return x.dataset.target===e.detail.target;})[0];
 if(!d){return;}d.open=true;roundLight(d.dataset.target);if(d.getBoundingClientRect().top>innerHeight||d.getBoundingClientRect().bottom<0){d.scrollIntoView({block:'start'});}});
document.addEventListener('labeling:run',function(e){if(e.detail.op!=='definition-discussion'){return;}
 var recs=$$('.discrec');if(!recs.some(function(r){return r.dataset.target===e.detail.target;})){return;}
 recs.forEach(function(r){r.hidden=r.dataset.target!==e.detail.target;});});
/* a Copy inside a folded Prompt summary copies without opening it */
document.addEventListener('click',function(ev){if(ev.target.closest&&ev.target.closest('summary [data-copy]')){ev.preventDefault();}},true);
/* Workflow (Phases, SOP, map) and All runs open only from ?drawer=workflow|allruns; Esc closes */
(function(){var d=null;try{d=new URLSearchParams(location.search).get('drawer');}catch(e){}
 $$('[data-drawer-panel]').forEach(function(x){x.hidden=x.dataset.drawerPanel!==d;});})();
document.addEventListener('keydown',function(e){if(e.key==='Escape'){$$('[data-drawer-panel]').forEach(function(x){x.hidden=true;});}});
$$('[data-map-color]').forEach(function(b){b.addEventListener('click',function(){var w=b.closest('.mapwrap');
 w.dataset.color=b.dataset.mapColor;$$('[data-map-color]',w).forEach(function(x){x.classList.toggle('on',x===b);});});});
/* ── embedding map: pick a dot, light a group, zoom and pan ── */
$$('.embpane').forEach(function(pane){
 var dataEl=$('.embdata',pane),svg=$('svg.map',pane);if(!dataEl||!svg){return;}
 var data=JSON.parse(dataEl.textContent),wrap=$('.mapwrap',pane),zoom=$('g.zoom',svg),links=$('g.links',svg),pick=$('[data-pick]',pane);
 var vb=svg.viewBox.baseVal,view={x:0,y:0,k:1},dots=$$('circle.pt',svg),focusGroup=null;
 function byId(id){return $('circle.pt[data-item="'+id+'"]',svg);}
 function apply(){zoom.setAttribute('transform','translate('+view.x+' '+view.y+') scale('+view.k+')');
  var r=7/Math.sqrt(view.k);dots.forEach(function(c){c.setAttribute('r',r.toFixed(2));});}
 function toSvg(cx,cy){var b=svg.getBoundingClientRect();return {x:(cx-b.left)*vb.width/b.width,y:(cy-b.top)*vb.height/b.height};}
 function zoomAt(px,py,factor){var k=Math.min(16,Math.max(1,view.k*factor));
  view.x=px-(px-view.x)*(k/view.k);view.y=py-(py-view.y)*(k/view.k);view.k=k;if(k===1){view.x=0;view.y=0;}apply();}
 $$('[data-zoom]',pane).forEach(function(b){b.addEventListener('click',function(){if(svg.hasAttribute('hidden')){return;}
  if(b.dataset.zoom==='reset'){view={x:0,y:0,k:1};apply();return;}zoomAt(vb.width/2,vb.height/2,b.dataset.zoom==='in'?1.5:1/1.5);});});
 svg.addEventListener('wheel',function(e){if(!e.ctrlKey){return;}e.preventDefault();var q=toSvg(e.clientX,e.clientY);zoomAt(q.x,q.y,e.deltaY<0?1.15:1/1.15);},{passive:false});
 var drag=null;
 svg.addEventListener('pointerdown',function(e){drag={x:e.clientX,y:e.clientY,vx:view.x,vy:view.y,moved:false,touch:e.pointerType==='touch'};});
 svg.addEventListener('pointermove',function(e){if(!drag){return;}var dx=e.clientX-drag.x,dy=e.clientY-drag.y;
  if(!drag.moved&&Math.abs(dx)+Math.abs(dy)<5){return;}drag.moved=true;if(drag.touch){return;}svg.classList.add('dragging');
  var b=svg.getBoundingClientRect();view.x=drag.vx+dx*vb.width/b.width;view.y=drag.vy+dy*vb.height/b.height;apply();});
 function endDrag(e){if(!drag){return;}var moved=drag.moved;drag=null;svg.classList.remove('dragging');
  if(!moved&&e&&e.target&&e.target.classList&&e.target.classList.contains('pt')){choose(e.target.dataset.item);}}
 svg.addEventListener('pointerup',endDrag);svg.addEventListener('pointerleave',function(){drag=null;svg.classList.remove('dragging');});
 svg.addEventListener('pointercancel',function(){drag=null;svg.classList.remove('dragging');});
 function lightGroup(g){focusGroup=(focusGroup===g)?null:g;
  dots.forEach(function(c){c.classList.toggle('dim',focusGroup!==null&&c.dataset.group!==focusGroup);});
  $$('[data-group-pick]',pane).forEach(function(el){el.classList.toggle('on',el.dataset.groupPick===focusGroup);});
  if(pane.__setPick){pane.__setPick(pickStateOf());}
  if(focusGroup!==null){(svg.hasAttribute('hidden')?$('canvas.map3d',pane):svg).scrollIntoView({block:'nearest',behavior:'smooth'});}}
 function pickStateOf(){var s=$('circle.pt.sel',svg);if(!s){return null;}
  return {id:s.dataset.item,nbs:$$('circle.pt.nb',svg).map(function(c){return c.dataset.item;})};}
 $$('[data-group-pick]',pane).forEach(function(el){el.addEventListener('click',function(e){
   if(e.target.closest&&e.target.closest('[data-no-light]')){return;}lightGroup(el.dataset.groupPick);});
  el.addEventListener('keydown',function(e){if(e.target!==el){return;}
   if(e.key==='Enter'||e.key===' '){e.preventDefault();lightGroup(el.dataset.groupPick);}});});
 /* item text: typical items per group, or one picked dot; items waiting in a round never show here */
 var SPEAKER=/^\s*([A-Z][A-Z_ ]{1,20}):\s*/;
 function marked(text,words){var t=String(text||'');if(!words||!words.length){return esc(t);}
  var re=new RegExp('\\b('+words.join('|')+')\\b','gi'),out='',last=0,m;
  while((m=re.exec(t))){out+=esc(t.slice(last,m.index))+'<mark>'+esc(m[0])+'</mark>';last=m.index+m[0].length;}
  return out+esc(t.slice(last));}
 function clip(t,n){t=String(t||'').trim();return t.length>n?t.slice(0,n).replace(/\s+\S*$/,'')+' …':t;}
 function itemTextHtml(r,words){
  var turns=String(r.context||'').split('\n').filter(function(l){return l.trim();}),earlier=Math.max(0,turns.length-2);
  function turn(l){var m=l.match(SPEAKER),name=m?who(m[1]):'',body=m?l.slice(m[0].length):l;
   return '<div class=turn><b>'+esc(name)+'</b><span>'+marked(clip(body,260),words)+'</span></div>';}
  var ctx=(earlier?'<button class="pill tog" type=button data-earlier>Show '+earlier+' earlier turn'+(earlier>1?'s':'')+'</button>'+
    '<div class=earlier hidden>'+turns.slice(0,earlier).map(turn).join('')+'</div>':'')+turns.slice(earlier).map(turn).join('');
  return (ctx?'<div class=exctx>'+ctx+'</div>':'')+
   '<div class="turn exreply"><b>AI reply</b><span>'+marked(clip(r.text,600),words)+'</span></div>';}
 function exItem(e,words){var mk=data.marks[e.item_id];
  return '<div class=ex><div class=exh><button class="pill tog" type=button data-ex-item="'+esc(e.item_id)+'" title="Show this item on the map">item '+esc(e.item_id)+' · see on map</button>'+
   '<span class=mut>similarity to the group centre '+e.closeness.toFixed(2)+'</span>'+(mk&&mk.final?'<span class=pill>your label: '+esc(mk.final)+'</span>':'')+
   '</div>'+itemTextHtml(e,words)+'</div>';}
 function wireItems(root){$$('[data-ex-item]',root).forEach(function(b){if(b.__wired){return;}b.__wired=true;
  b.addEventListener('click',function(){choose(b.dataset.exItem);
   (svg.hasAttribute('hidden')?$('canvas.map3d',pane):svg).scrollIntoView({block:'center',behavior:'smooth'});});});}
 pane.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-earlier]');if(!b){return;}
  var box=b.nextElementSibling,open=box.hidden;box.hidden=!open;
  b.textContent=(open?'Hide ':'Show ')+box.children.length+' earlier turn'+(box.children.length>1?'s':'');});
 $$('[data-ex-group]',pane).forEach(function(btn){
  var g=btn.dataset.exGroup,list=$('[data-ex-list="'+g+'"]',pane),box=list.closest('tr')||list,offset=0,words=(data.groups[g]||{}).keywords||[];
  function more(){var b=$('[data-ex-more]',list);if(b){b.disabled=true;b.textContent='Loading…';}
   act('group_examples',{version:data.version,group_index:Number(g),k:3,offset:offset}).then(function(j){var r=j.result;
    if(b){b.remove();}
    if(offset===0&&r.hidden_waiting){list.insertAdjacentHTML('beforeend','<p class=mut>hidden, waiting in '+esc(r.hidden_rounds.map(roundWords).join(', '))+': '+r.hidden_waiting+'</p>');}
    if(offset===0&&!r.examples.length){list.insertAdjacentHTML('beforeend','<p class=mut>No item of this group can be shown yet.</p>');}
    list.insertAdjacentHTML('beforeend',r.examples.map(function(e){return exItem(e,words);}).join(''));
    offset+=r.examples.length;
    if(r.more){list.insertAdjacentHTML('beforeend','<button class="pill tog" type=button data-ex-more>Show 3 more</button>');
     $('[data-ex-more]',list).addEventListener('click',more);}
    wireItems(list);})
   .catch(function(e){if(b){b.disabled=false;b.textContent='Show 3 more';}
    list.insertAdjacentHTML('beforeend','<p class=warn>'+esc(e.message)+'</p>');});}
  btn.addEventListener('click',function(){
   if(!box.hidden){box.hidden=true;btn.textContent='Show typical items';btn.classList.remove('on');return;}
   box.hidden=false;btn.textContent='Hide typical items';btn.classList.add('on');if(!offset&&!list.children.length){more();}});});
 function markText(id){var mk=data.marks[id];if(!mk){return 'not picked for labeling';}
  return roundWords(mk.round)+(mk.final?' · your label: '+mk.final:' · not labeled yet');}
 function groupTag(g){var info=data.groups[String(g)];if(!info){return '';}
  return '<span class="pill mut"><i class=dot style="background:'+info.color+'"></i>'+esc(info.name)+'</span>';}
 function clearPick(){$$('circle.pt.sel,circle.pt.nb',svg).forEach(function(c){c.classList.remove('sel','nb');});links.innerHTML='';
  if(pane.__setPick){pane.__setPick(null);}}
 function choose(id){
  clearPick();var c=byId(id);if(!c){return;}c.classList.add('sel');
  pick.hidden=false;pick.innerHTML='<p class=mut>Finding the nearest items…</p>';
  act('embedding_item',{version:data.version,item_id:id,k:6}).then(function(j){
   var r=j.result,info=data.groups[String(r.group)]||{},lines='';
   r.neighbors.forEach(function(n){var d=byId(n.item_id);if(!d){return;}d.classList.add('nb');
    lines+='<line x1="'+c.getAttribute('cx')+'" y1="'+c.getAttribute('cy')+'" x2="'+d.getAttribute('cx')+'" y2="'+d.getAttribute('cy')+'"/>';});
   links.innerHTML=lines;c.parentNode.appendChild(c);
   if(pane.__setPick){pane.__setPick({id:r.item_id,nbs:r.neighbors.map(function(n){return n.item_id;})});}
   pick.innerHTML='<div class=rh><span class=rid>item '+esc(r.item_id)+'</span><span class=mut>in group</span>'+groupTag(r.group)+'<span class=mut>'+esc((info.keywords||[]).slice(0,3).join(' · '))+'</span>'+
    '<button class=ghost type=button data-pick-close aria-label="Close">×</button></div>'+
    '<div class=rrows><div class=rr><b>round</b><span>'+esc(markText(r.item_id))+'</span></div>'+
    '<div class=rr><b>most similar 6</b><span class=nbs>'+r.neighbors.map(function(n){
      return '<button class="pill tog" type=button data-pick-item="'+esc(n.item_id)+'" title="'+esc(markText(n.item_id))+'">'+
       '<i class=dot style="background:'+((data.groups[String(n.group)]||{}).color||'var(--mut)')+'"></i>item '+esc(n.item_id)+' · '+n.similarity.toFixed(2)+
       (data.marks[n.item_id]&&data.marks[n.item_id].final?' · '+esc(data.marks[n.item_id].final):'')+'</button>';}).join('')+'</span></div></div>'+
    '<div class=pktext data-pick-text>'+(data.marks[r.item_id]&&!data.marks[r.item_id].final
      ?'<p class=mut>waits in '+esc(roundWords(data.marks[r.item_id].round))+'</p>'
      :'<button class="pill tog" type=button data-pick-show>Show its text</button>')+'</div>';
   $('[data-pick-close]',pick).addEventListener('click',function(){clearPick();pick.hidden=true;});
   var show=$('[data-pick-show]',pick);if(show){show.addEventListener('click',function(){show.disabled=true;show.textContent='Loading…';
    act('embedding_item_text',{version:data.version,item_id:r.item_id}).then(function(t){
     $('[data-pick-text]',pick).innerHTML='<div class=ex>'+itemTextHtml(t.result,info.keywords||[])+'</div>';})
    .catch(function(e){$('[data-pick-text]',pick).innerHTML='<p class=warn>'+esc(e.message)+'</p>';});});}
   $$('[data-pick-item]',pick).forEach(function(b){b.addEventListener('click',function(){choose(b.dataset.pickItem);});});
  }).catch(function(e){pick.innerHTML='<p class=warn>'+esc(e.message)+'</p>';});
 }
 $$('[data-map-show]',pane).forEach(function(b){b.addEventListener('click',function(){wrap.dataset.show=b.dataset.mapShow;
  $$('[data-map-show]',pane).forEach(function(x){x.classList.toggle('on',x===b);});draw3d();});});
 /* 3D: the same items, turned and zoomed on a canvas */
 var canvas=$('canvas.map3d',pane),pts=data.points3d||[],cam={yaw:0.6,pitch:0.35,zoom:1},spin=false,raf=null,pickState=null,drag3=null;
 function cssColor(v){if(!v||v.indexOf('var(')!==0){return v||'#888';}
  return getComputedStyle(document.documentElement).getPropertyValue(v.slice(4,-1)).trim()||'#888';}
 function is3d(){return canvas&&!canvas.hidden;}
 function sizeCanvas(){if(!canvas){return;}var w=canvas.clientWidth||600,dpr=window.devicePixelRatio||1;
  canvas.width=Math.round(w*dpr);canvas.height=Math.round(w*0.6*dpr);canvas.style.height=Math.round(w*0.6)+'px';}
 function project(x,y,z){var cy=Math.cos(cam.yaw),sy=Math.sin(cam.yaw),cp=Math.cos(cam.pitch),sp=Math.sin(cam.pitch);
  var x1=x*cy-z*sy,z1=x*sy+z*cy,y1=y*cp-z1*sp,z2=y*sp+z1*cp,f=3.2/(3.2-z2*0.9),
   s=Math.min(canvas.width,canvas.height)*0.36*cam.zoom;
  return {x:canvas.width/2+x1*f*s,y:canvas.height/2-y1*f*s,z:z2,f:f};}
 function draw3d(){
  if(!is3d()){return;}var ctx=canvas.getContext('2d'),dpr=window.devicePixelRatio||1,W=canvas.width,H=canvas.height;
  ctx.clearRect(0,0,W,H);
  var line=cssColor('var(--line)'),fg=cssColor('var(--fg)'),acc=cssColor('var(--acc)');
  ctx.strokeStyle=line;ctx.lineWidth=1.2*dpr;ctx.beginPath();
  [[1,0,0],[0,1,0],[0,0,1]].forEach(function(a){var p1=project(-a[0],-a[1],-a[2]),p2=project(a[0],a[1],a[2]);
   ctx.moveTo(p1.x,p1.y);ctx.lineTo(p2.x,p2.y);});ctx.stroke();
  var byColor=wrap.dataset.color==='label',roundOnly=wrap.dataset.show==='round';
  var drawn=pts.map(function(p){var q=project(p[1],p[2],p[3]);q.id=p[0];q.group=p[4];return q;});
  drawn.sort(function(a,b){return a.z-b.z;});
  var nbs=pickState?pickState.nbs:[],selQ=null;
  if(pickState){var sq=drawn.filter(function(q){return q.id===pickState.id;})[0];
   if(sq){ctx.strokeStyle=acc;ctx.globalAlpha=0.6;ctx.lineWidth=1.5*dpr;
    drawn.forEach(function(q){if(nbs.indexOf(q.id)>=0){ctx.beginPath();ctx.moveTo(sq.x,sq.y);ctx.lineTo(q.x,q.y);ctx.stroke();}});ctx.globalAlpha=1;}}
  drawn.forEach(function(q){
   var mk=data.marks[q.id],g=data.groups[String(q.group)]||{},fill=byColor?(mk&&mk.final?cssColor(data.label_colors[mk.final]):cssColor('var(--mut)')):g.color;
   var faded=(focusGroup!==null&&String(q.group)!==focusGroup)||(roundOnly&&!mk)||(byColor&&!(mk&&mk.final));
   var r=Math.max(2,5.5*q.f*Math.sqrt(cam.zoom))*dpr;
   ctx.globalAlpha=faded?0.13:(0.55+0.45*(q.z+1)/2);ctx.fillStyle=fill;ctx.beginPath();ctx.arc(q.x,q.y,r,0,6.2832);ctx.fill();
   ctx.globalAlpha=faded?0.2:1;
   if(pickState&&q.id===pickState.id){ctx.strokeStyle=acc;ctx.lineWidth=3.5*dpr;ctx.stroke();selQ=q;}
   else if(nbs.indexOf(q.id)>=0){ctx.strokeStyle=acc;ctx.lineWidth=2*dpr;ctx.stroke();}
   else if(mk){ctx.strokeStyle=fg;ctx.lineWidth=1.6*dpr;ctx.stroke();}
   q.r=r;});
  ctx.globalAlpha=1;canvas.__pts=drawn;}
 function loop(){if(!spin||!is3d()){raf=null;return;}cam.yaw+=0.006;draw3d();raf=requestAnimationFrame(loop);}
 if(canvas){
  sizeCanvas();window.addEventListener('resize',function(){if(is3d()){sizeCanvas();draw3d();}});
  $$('[data-map-dim]',pane).forEach(function(b){b.addEventListener('click',function(){
   var three=b.dataset.mapDim==='3d';$$('[data-map-dim]',pane).forEach(function(x){x.classList.toggle('on',x===b);});
   svg.toggleAttribute('hidden',three);canvas.hidden=!three;$('[data-spin]',pane).hidden=!three;
   if(three){sizeCanvas();draw3d();}else{spin=false;$('[data-spin]',pane).classList.remove('on');}});});
  $('[data-spin]',pane).addEventListener('click',function(){spin=!spin;this.classList.toggle('on',spin);if(spin&&!raf){raf=requestAnimationFrame(loop);}});
  canvas.addEventListener('pointerdown',function(e){drag3={x:e.clientX,y:e.clientY,moved:false};canvas.setPointerCapture(e.pointerId);});
  canvas.addEventListener('pointermove',function(e){if(!drag3){return;}var dx=e.clientX-drag3.x,dy=e.clientY-drag3.y;
   if(!drag3.moved&&Math.abs(dx)+Math.abs(dy)<4){return;}drag3.moved=true;canvas.classList.add('dragging');
   cam.yaw+=dx*0.01;cam.pitch=Math.max(-1.45,Math.min(1.45,cam.pitch+dy*0.01));drag3.x=e.clientX;drag3.y=e.clientY;draw3d();});
  canvas.addEventListener('pointerup',function(e){var d=drag3;drag3=null;canvas.classList.remove('dragging');
   if(d&&!d.moved){var b=canvas.getBoundingClientRect(),dpr=window.devicePixelRatio||1,mx=(e.clientX-b.left)*dpr,my=(e.clientY-b.top)*dpr,best=null,bd=1e9;
    (canvas.__pts||[]).forEach(function(q){var dd=Math.hypot(q.x-mx,q.y-my);if(dd<Math.max(q.r+4*dpr,10*dpr)&&(dd<bd||(best&&dd===bd&&q.z>best.z))){best=q;bd=dd;}});
    if(best){choose(best.id);}}});
  canvas.addEventListener('pointercancel',function(){drag3=null;canvas.classList.remove('dragging');});
  canvas.addEventListener('wheel',function(e){if(!e.ctrlKey){return;}e.preventDefault();cam.zoom=Math.max(0.5,Math.min(6,cam.zoom*(e.deltaY<0?1.12:1/1.12)));draw3d();},{passive:false});
  $$('[data-map-color]',pane).forEach(function(b){b.addEventListener('click',function(){draw3d();});});
 }
 $$('[data-zoom]',pane).forEach(function(b){b.addEventListener('click',function(){if(!is3d()){return;}
  if(b.dataset.zoom==='reset'){cam={yaw:0.6,pitch:0.35,zoom:1};}else{cam.zoom=Math.max(0.5,Math.min(6,cam.zoom*(b.dataset.zoom==='in'?1.3:1/1.3)));}draw3d();});});
 pane.__setPick=function(state){pickState=state;draw3d();};
});
/* ── embedding model: show one build, start a build, watch it ─ */
(function(){
 var panes=$$('.embpane');
 function showEmb(v,remember){
  if(!panes.length){return;}
  if(!panes.some(function(p){return p.dataset.emb===v;})){v=panes[panes.length-1].dataset.emb;}
  panes.forEach(function(p){p.hidden=p.dataset.emb!==v;});
  $$('.pill.tog[data-emb-show]').forEach(function(b){b.classList.toggle('on',b.dataset.embShow===v);});
  runsWant('data',v);
  if(remember){try{var u=new URL(location.href);u.searchParams.set('emb',v);history.replaceState(null,'',u.toString());}catch(e){}}
 }
 var want=null;try{want=new URLSearchParams(location.search).get('emb');}catch(e){}
 showEmb(want,false);
 $$('[data-emb-show]').forEach(function(b){b.addEventListener('click',function(){showEmb(b.dataset.embShow,true);
  if(!b.classList.contains('tog')){var d=b.closest('details');if(d){d.open=false;}var pane=$('.embpane:not([hidden])');if(pane){pane.scrollIntoView({block:'start'});}}});});
 document.addEventListener('labeling:run',function(e){if(e.detail.op==='embedding-build'){showEmb(e.detail.target,true);}});
 var timer=null,form=$('[data-emb-form]'),runBtn=$('[data-emb-run]'),runMsg=$('[data-emb-form] [data-emb-msg]');
 var info={};try{info=JSON.parse($('.embcatalog').textContent);}catch(e){}
 var choice={input_mode:'reply_context',map_method:'tsne'};
 function say(text,err){if(runMsg){runMsg.textContent=text;runMsg.className='msg'+(err?' err':'');}}
 function modelChanged(){if(!form){return;}var sel=$('[data-emb-field=model]',form),opt=sel.options[sel.selectedIndex],ins=$('[data-emb-field=instruction]',form);
  $('[data-emb-modelinfo]',form).textContent=info[sel.value]||'';ins.disabled=!(opt&&opt.dataset.instruct);
  ins.placeholder=ins.disabled?'this model takes no instruction':'optional, e.g. Represent this text by the trait being labeled';
  if(ins.disabled){ins.value='';}}
 if(form){
  modelChanged();$('[data-emb-field=model]',form).addEventListener('change',modelChanged);
  $$('[data-emb-input]',form).forEach(function(b){b.addEventListener('click',function(){choice.input_mode=b.dataset.embInput;
   $$('[data-emb-input]',form).forEach(function(x){x.classList.toggle('on',x===b);});});});
  $$('[data-emb-map]',form).forEach(function(b){b.addEventListener('click',function(){choice.map_method=b.dataset.embMap;
   $$('[data-emb-map]',form).forEach(function(x){x.classList.toggle('on',x===b);});});});
 }
 function watch(version){
  if(timer){return;}if(runBtn){runBtn.disabled=true;}
  timer=setInterval(function(){
   act('embedding_status',{}).then(function(j){
    (j.result.models||[]).forEach(function(r){
     if(r.version!==version){return;}
     if(r.state==='built'){clearInterval(timer);timer=null;
      if(current.space==='data'&&current.view==='embedding'){var u=new URL(location.href);u.searchParams.set('space','data');u.searchParams.set('view','embedding');u.searchParams.set('emb',r.version);location.href=u.toString();}
      else{say('Done: '+r.version+'. Reload the page to see it.');if(runBtn){runBtn.disabled=false;}}}
     else if(r.state==='failed'||r.state==='stopped'){clearInterval(timer);timer=null;
      say([r.failure||'The run ended early.'].concat(r.log_tail||[]).join(' · '),true);if(runBtn){runBtn.disabled=false;}}
    });
   }).catch(function(){});
  },3000);
 }
 if(runBtn){runBtn.addEventListener('click',function(){
  var g=$('[data-emb-field=groups]',form).value.trim(),seed=$('[data-emb-field=seed]',form).value.trim();
  var body={model:$('[data-emb-field=model]',form).value,input_mode:choice.input_mode,map_method:choice.map_method,
   instruction:$('[data-emb-field=instruction]',form).value.trim(),groups:g===''?null:+g,seed:seed===''?0:+seed};
  runBtn.disabled=true;say('Starting…');
  act('build_embedding',body).then(function(j){say('Running in the background as '+j.result.version+'. You can leave this view; labeling is not affected.');watch(j.result.version);})
  .catch(function(e){say(e.message,true);runBtn.disabled=false;});
 });}
 var busy=$('[data-emb-row][data-state=building]');
 if(busy){say('A run is in progress: '+busy.dataset.embRow+'.');watch(busy.dataset.embRow);}
})();
(function(){var s=null,v=null;try{var q=new URLSearchParams(location.search);s=q.get('space');v=q.get('view');}catch(e){}
 if(!s){try{var saved=JSON.parse(localStorage.getItem(key)||'null');if(saved){s=saved.space;v=saved.view;}}catch(e){}}
 select(s||boot.default_space,v,false);})();
/* ── server calls ─────────────────────────────────────────── */
var sessionId;try{sessionId=sessionStorage.getItem('labeling-session')||'';}catch(e){sessionId='';}
if(!sessionId){sessionId='s'+Date.now().toString(36)+Math.random().toString(36).slice(2,8);try{sessionStorage.setItem('labeling-session',sessionId);}catch(e){}}
function act(action,body){
 var payload=Object.assign({mode:boot.mode,path:boot.path,file:boot.file,page:boot.page,action:action,
  human_id:boot.human_id,session_id:sessionId},body||{});
 if(action!=='confirm_meaning')payload.attest=true;
 return fetch('/_board/labeling/act',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)})
  .then(function(r){return r.json().then(function(j){if(!r.ok||!j.ok){throw new Error(j.err||('HTTP '+r.status));}return j;});});
}
/* ── Data → Preparation: items to label, a page at a time (each page is an exposure) ──
   One table, one row per item: who it is, its state, what the person said last, the reply to
   label, and the earlier turns folded. Items drawn into an open round stay out of the table,
   counted on one line, so they are judged blind in Labeling › Rounds. */
(function(){var btn=$('[data-items-show]');if(!btn){return;}
 var box=$('[data-items-box]'),rows=$('[data-items-rows]'),note=$('[data-items-note]'),bar=$('[data-items-filter]'),
  more=$('[data-items-more]'),offset=0,k=20,all=[],filter='all';
 function speaker(w){w=String(w||'').trim();if(/^(lamda|assistant|bot|chatbot|ai|model|gpt|claude)$/i.test(w)){return 'AI';}
  if(/^user$/i.test(w)){return 'Person';}return w?w.charAt(0).toUpperCase()+w.slice(1):'';}
 function split(c){return String(c||'').split('\n').filter(function(l){return l.trim();}).map(function(l){
  var m=l.match(/^([A-Za-z][A-Za-z_ ]{0,20}):\s?(.*)$/);return m?{who:speaker(m[1]),text:m[2]}:{who:'',text:l};});}
 function shown(it){return !/^waiting in /.test(it.state);}
 function keep(it){return shown(it)&&(filter==='all'||(filter==='to label'?it.state==='to label':it.state!=='to label'));}
 function stateWords(s){return s.replace(/^labeled in (\S+)$/,function(_,r){return 'labeled in '+roundWords(r);});}
 /* the whole item as plain text: the context before it (folded), Main, the context after it (folded) */
 function lines(c){return String(c||'').split('\n').filter(function(l){return l.trim();});}
 function fold(name,c){var ls=lines(c);if(!ls.length){return '';}
  return '<details class=plainctx><summary>'+name+' · '+ls.length+(ls.length===1?' line':' lines')+'</summary><div class=plain>'+
   ls.map(esc).join('<br>')+'</div></details>';}
 function row(it){var body=fold('Before context',it.context)+'<div class=plain>Main: '+esc(it.text)+'</div>'+fold('After context',it.after);
  return '<tr><td class=itemid>'+esc(it.item_id)+'</td><td>'+body+'</td>'+
   '<td><span class="pill'+(it.state==='to label'?'':' mut')+'">'+esc(stateWords(it.state))+'</span></td></tr>';}
 function render(){var hidden=all.filter(function(it){return !shown(it);}).length,n={'all':0,'to label':0,'labeled':0};
  all.filter(shown).forEach(function(it){n.all++;n[it.state==='to label'?'to label':'labeled']++;});
  note.innerHTML=hidden?'<p class=mut>'+hidden+(hidden===1?' item is':' items are')+' in an open round and '+(hidden===1?'is':'are')+
   ' left out of this table: you see '+(hidden===1?'it':'them')+' first in Labeling › Rounds and judge blind.</p>':'';
  bar.innerHTML=['all','to label','labeled'].map(function(f){return '<button type=button class="pill tog'+(f===filter?' on':'')+'" data-f="'+f+'">'+f+' · '+n[f]+'</button>';}).join('');
  var picked=all.filter(keep);
  rows.innerHTML=picked.length?picked.map(row).join(''):'<tr><td colspan=3 class=mut>No item matches.</td></tr>';}
 bar.addEventListener('click',function(e){var b=e.target.closest('[data-f]');if(b){filter=b.getAttribute('data-f');render();}});
 function load(){btn.disabled=true;var m=$('button',more);if(m){m.disabled=true;m.textContent='Loading…';}
  act('item_page',{offset:offset,k:k}).then(function(j){var r=j.result;box.hidden=false;btn.hidden=true;
   all=all.concat(r.items);offset+=r.items.length;render();
   more.innerHTML=r.more?'<button type=button class="pill tog">Show '+Math.min(k,r.total-offset)+' more ('+offset+' of '+r.total+' items)</button>':
    '<p class=mut>All '+r.total+' items shown.</p>';
   var b=$('button',more);if(b){b.addEventListener('click',load);}})
  .catch(function(e){btn.disabled=false;more.innerHTML='<p class=warn>'+esc(e.message)+'</p>';});}
 btn.addEventListener('click',load);})();
/* ── The data: the script that made the items, read-only in a pop-out ── */
(function(){var o=$('[data-code-open]'),d=$('[data-code-dialog]');if(!o||!d){return;}
 o.addEventListener('click',function(){d.showModal();});
 $('[data-code-close]',d).addEventListener('click',function(){d.close();});
 d.addEventListener('click',function(e){if(e.target===d){d.close();}});})();
/* ── G0: confirm meaning ─────────────────────────────────── */
var attest=$('[data-confirm-attest]'),confirmBtn=$('[data-confirm-meaning]'),confirmMsg=$('[data-confirm-msg]');
if(attest&&confirmBtn){attest.addEventListener('change',function(){confirmBtn.disabled=!attest.checked;});
 confirmBtn.addEventListener('click',function(){
  var ask=boot.g0_repair_request?
   'This restores the missing G0 receipt from the earlier human confirmation. The Workbench does not verify your identity. Continue?':
   'This records your caller attestation as '+boot.human_id+'. The Workbench does not verify your identity. Continue?';
  if(!window.confirm(ask))return;
  confirmBtn.disabled=true;confirmMsg.textContent='Saving…';confirmMsg.className='msg';
  act('confirm_meaning',{attest:true}).then(function(){confirmMsg.textContent=boot.g0_repair_request?'G0 receipt restored. Opening the round…':'Confirmed. Opening round 1…';
   var u=new URL(location.href);u.searchParams.set('space','labeling');u.searchParams.set('view','rounds');location.href=u.toString();})
  .catch(function(e){confirmMsg.textContent=e.message;confirmMsg.className='msg err';confirmBtn.disabled=false;});});}
/* ── Label: start a round; a round in progress is the server's table, labeled in chat ── */
/* chat prompts: any [data-copy] button copies its text; plain http needs the textarea fallback */
function toast(m,bad){var t=$('#cc-toast');if(!t){t=document.createElement('div');t.id='cc-toast';t.setAttribute('role','status');document.body.appendChild(t);}
 t.textContent=m;t.className='on'+(bad?' bad':'');clearTimeout(toast.t);toast.t=setTimeout(function(){t.className='';},2400);}
function legacyCopy(t){
 var a=document.createElement('textarea');a.value=t;a.style.position='fixed';a.style.opacity='0';document.body.appendChild(a);
 a.focus();a.select();var ok=false;try{ok=document.execCommand('copy');}catch(e){}document.body.removeChild(a);
 return ok?Promise.resolve():Promise.reject(new Error('Legacy clipboard copy failed'));}
function copyText(t){
 if(navigator.clipboard&&window.isSecureContext){return navigator.clipboard.writeText(t).catch(function(){return legacyCopy(t);});}
 return legacyCopy(t);}
document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-copy]');if(!b){return;}
 copyText(b.dataset.copy).then(function(){toast('Copied');},function(){toast('Copy failed. Check clipboard access and try again.',true);});});
var app=$('#label-app');
var AI_NAMES=/^(lamda|assistant|bot|chatbot|ai|model|system|gpt|chatgpt|claude|bard|gemini|agent)$/i;
function who(tag){return AI_NAMES.test(String(tag||'').trim())?'AI':String(tag||'');}
function roundWords(id){var m=String(id||'').match(/^round_0*(\d+)$/);return m?'round '+m[1]:String(id||'');}
function message(html){app.innerHTML='<div class=card>'+html+'</div>';}
function load(){
 if(!app){return;}
 if(boot.hold){message('<p class=warn>Read-only · '+esc(boot.next||'')+'</p>');return;}
 if(boot.phase!=='P1'){
  if(boot.g0_open){
   if(boot.g0_retroactive_block){message('<p>A round was released without valid prior meaning confirmation. Keep this job as history; start a new job for new labels.</p>');}
   else if(boot.g0_repair_request){message('<p>Restore the missing G0 receipt from the earlier human confirmation.</p><div class=actions><button class=primary type=button id=go-confirm>Go to Definition</button></div>');
    $('#go-confirm').addEventListener('click',function(){select('labeling','definition',true);});}
   else if(boot.missing_meanings.length){message('<p>Define every label meaning in a Definition discussion before confirming G0.</p><div class=actions><button class=primary type=button id=go-confirm>Go to Definition</button></div>');
    $('#go-confirm').addEventListener('click',function(){select('labeling','definition',true);});}
   else{message('<p><b>Step 1 first:</b> '+(boot.definition_open?'finish the open label-meaning discussion.':'review or discuss the label meanings, then confirm them.')+'</p><div class=actions><button class=primary type=button id=go-confirm>Go to Definition</button></div>');
    $('#go-confirm').addEventListener('click',function(){select('labeling','definition',true);});}}
  else{message('<p class=mut>Labeling opens after P0 Contract passes.</p>');}
  return;}
 var cur=boot.current_round, rounds=boot.rounds||[];
 if(boot.definition_open){message('<p>Finish the open label-meaning discussion before releasing a round.</p>');return;}
 if(!cur&&rounds.length&&rounds[rounds.length-1].state==='judged'){
  var r=rounds[rounds.length-1];message('<p class=ok>'+esc(r.round_id)+' is done: '+r.finals+' of '+r.batch_size+' labeled.</p>');return;}
 if(!cur){
  var sizes=[10,20,30,50];if(sizes.indexOf(boot.batch_default)<0){sizes.push(boot.batch_default);sizes.sort(function(a,b){return a-b;});}
  message('<h2>Start round 1</h2><p>Round 1 picks items at random from the items to label. Held-back test items are never picked.</p>'+
   '<div class=line><span class=lbl>how many</span>'+sizes.map(function(n){return '<button type=button class="pill tog'+(n===boot.batch_default?' on':'')+'" data-size='+n+'>'+n+'</button>';}).join('')+'</div>'+
   '<div class=actions><button class=primary type=button id=start-round>Start round 1</button><span class=msg id=start-msg role=status></span></div>');
  var size=boot.batch_default;$$('[data-size]',app).forEach(function(b){b.addEventListener('click',function(){size=+b.dataset.size;$$('[data-size]',app).forEach(function(x){x.classList.toggle('on',x===b);});});});
  $('#start-round').addEventListener('click',function(){var btn=this;btn.disabled=true;$('#start-msg').textContent='Drawing…';
   act('release_round',{n:size}).then(function(){location.reload();})
   .catch(function(e){$('#start-msg').textContent=e.message;$('#start-msg').className='msg err';btn.disabled=false;});});
  return;}
}
load();
})();
