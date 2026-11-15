"""The frame's page scripts: Studio, pop-out, embed and Guide title."""

from __future__ import annotations



# Idea Studio: a topic's canvas loads when its row opens; Edit switches that canvas to the editor in
# place; #topic-<name> in the address opens that row (the Audience Report links here).
STUDIO_JS = """
(function(){
function load(d){var f=d.querySelector(':scope > iframe[data-src], :scope > .dv-pane:not([hidden]) > iframe[data-src], :scope > .st-pane:not([hidden]) > iframe[data-src]');if(d.open&&f&&!f.getAttribute('src'))f.src=f.dataset.src;}
// a Delivery item's versions (JL 261014): a version button shows its pane and loads its preview
document.addEventListener('click',function(ev){var b=ev.target.closest('.dv-vers [data-dv]');if(!b)return;
  var d=b.closest('details');d.querySelectorAll(':scope > .dv-vers [data-dv]').forEach(function(x){x.setAttribute('aria-pressed',String(x===b));});
  d.querySelectorAll(':scope > .dv-pane').forEach(function(p){p.hidden=p.dataset.dv!==b.dataset.dv;});load(d);});
function hashTarget(){
  var id;try{id=decodeURIComponent(location.hash.slice(1));}catch(e){return null;}
  var found=document.getElementById(id);if(found)return found;
  if(id.indexOf('topic-')!==0)return null;
  var name=id.slice(6),path=new URL(location.href).searchParams.get('path')||'';
  var matches=Array.from(document.querySelectorAll('[data-studio-name]')).filter(function(r){return r.dataset.studioName===name&&!r.closest('[data-group-kind]');});
  return matches.find(function(r){return path.endsWith('/'+r.dataset.studioSource);})||matches[0]||null;
}
// a row a person clicks open scrolls so its drawing sits in the middle of the window (JL 261019: "when I click it,
// the draw will in the center of the page"); rows the page opens itself (a #link, a restored Current) do not jump
var clicked=0;document.addEventListener('click',function(e){if(e.target.closest('details.topic > summary'))clicked=Date.now();},true);
document.querySelectorAll('details.topic').forEach(function(d){d.addEventListener('toggle',function(){load(d);
  if(d.open&&Date.now()-clicked<1500){var f=d.querySelector(':scope > iframe.st-frame')||d;
    setTimeout(function(){f.scrollIntoView({behavior:'smooth',block:'center'});},60);}});});
// a #question-QNN link opens that Question's card in the Report (b10 s05: each Question is a folding card)
(function(){var h=decodeURIComponent(location.hash.slice(1));if(h.indexOf('question-')!==0)return;
  var el=document.getElementById(h),card=el&&el.closest('details.q-card');if(card){card.open=true;el.scrollIntoView();}})();
document.querySelectorAll('.studio-topics').forEach(function(list){
  // Groups (b10 s02-D16): Current lives in this browser; every other group is a tag on the topic's
  // **Tags:** line, written by POST /_board/studio-group, so it is the same for everyone. The same bar
  // sorts Related's items (data-group-kind=related, JL 261011): there a group is the row's group cell.
  var rows=Array.from(list.querySelectorAll('details[data-studio-key]'));
  var nav=list.querySelector('.studio-filters');
  var empty=list.querySelector('.studio-empty'),status=list.querySelector('.studio-status');
  var source=list.querySelector('[data-studio-source-filter]');
  var owner=list.dataset.studioOwner,kind=list.dataset.groupKind||'studio',noun=list.dataset.groupNoun||'topic',pre=kind+'_';
  var storageKey='workbench.'+kind+'.current.v1:'+owner,groupsKey='workbench.studio.groups.v1:'+owner;
  var current=new Set(),active='';
  function buttons(){return Array.from(nav.querySelectorAll('[data-studio-tag]'));}
  function button(key){return buttons().find(function(b){return b.dataset.studioTag===key;})||null;}
  function isGroup(key){return key!=='__current__'&&key!=='__untagged__'&&key!=='';}
  function readList(k){try{var v=JSON.parse(localStorage.getItem(k)||'[]');
    return Array.isArray(v)?v.filter(function(x){return typeof x==='string';}):[];}catch(e){return [];}}
  function writeList(k,v){try{localStorage.setItem(k,JSON.stringify(v));return true;}catch(e){return false;}}
  function read(){return new Set(readList(storageKey));}
  current=read();
  function labels(row){try{return JSON.parse(row.dataset.studioTags||'[]');}catch(e){return [];}}
  function tags(row){return labels(row).map(function(t){return t.toLowerCase();});}
  function matches(row,key){var names=tags(row);
    return !key||(key==='__current__'?current.has(row.dataset.studioKey):key==='__untagged__'?names.length===0:names.indexOf(key)>=0);}
  function say(text){status.textContent=text;}
  // the Studio's Timeline follows this bar: a topic's lines show when its row shows (JL 261011)
  function timeline(key){var tl=document.querySelector('.studio-timeline');if(!tl)return;
    var hidden={},shown=0;rows.forEach(function(r){hidden[r.dataset.studioKey]=r.hidden;});
    var peak=0,sums=[];
    tl.querySelectorAll('[data-tl-key]').forEach(function(t){t.hidden=!!hidden[t.dataset.tlKey];});
    tl.querySelectorAll('.tl-mrow').forEach(function(r){var n=0;
      r.querySelectorAll('.tl-cell:not([hidden])').forEach(function(c){n+=Number(c.dataset.tlCount||0);});
      r.dataset.tlN=n;shown+=n;peak=Math.max(peak,n);sums.push([r,n]);});
    sums.forEach(function(s){var i=s[0].querySelector('.tl-track i'),b=s[0].querySelector('.tl-bar b');
      if(i)i.style.width=(peak?Math.round(s[1]/peak*100):0)+'%';if(b)b.textContent=s[1];});
    // a group's bubble adds up its topics that still show; a group with none left drops its column
    var gsum={},gpeak=0,gcells=tl.querySelectorAll('.tl-gcell');
    gcells.forEach(function(c){var n=0,parts={};try{parts=JSON.parse(c.dataset.tlParts||'{}');}catch(e){}
      Object.keys(parts).forEach(function(k){if(!hidden[k])n+=parts[k];});c.dataset.tlNow=n;gpeak=Math.max(gpeak,n);
      gsum[c.dataset.tlGroup]=(gsum[c.dataset.tlGroup]||0)+n;});
    gcells.forEach(function(c){var n=Number(c.dataset.tlNow),b=c.querySelector('.tl-gb');c.hidden=!gsum[c.dataset.tlGroup];
      if(b){b.hidden=!n;if(n)b.style.setProperty('--s',Math.round(8+22*Math.sqrt(n/gpeak))+'px');}});
    tl.querySelectorAll('.tl-gcol').forEach(function(h){h.hidden=!gsum[h.dataset.tlGroup];});
    // the slanted names' header is as tall as the longest name still shown
    var ln=0;tl.querySelectorAll('.tl-col:not([hidden])').forEach(function(c){ln=Math.max(ln,c.title.length);});
    var map=tl.querySelector('.tl-map');if(map)map.style.setProperty('--tl-slant',Math.min(Math.round(Math.max(ln-4,0)*7.2*0.71)+40,200)+'px');
    // the Timeline's own group picker: All, then this bar's buttons, the picked one on (JL 261012)
    var strip=tl.querySelector('.tl-groups');if(strip){strip.textContent='';
      var w=document.createElement('span');w.textContent='groups';strip.appendChild(w);
      [['','All','',rows.length]].concat(buttons().map(function(b){var e=b.querySelector('.grp-emoji'),c=b.querySelector('.tag-count');
        return [b.dataset.studioTag,b.dataset.studioLabel||b.dataset.studioTag,e?e.textContent+' ':'',c?c.textContent:''];}))
      .forEach(function(o){var x=document.createElement('button');x.type='button';x.dataset.tlTag=o[0];
        x.setAttribute('aria-pressed',String(o[0]===key));x.textContent=o[2]+o[1];
        var n=document.createElement('i');n.textContent=o[3];x.appendChild(n);strip.appendChild(x);});}
    tlGaps(tl);tl.dispatchEvent(new Event('tl-shown'));
  }
  function labelOf(key){var b=button(key);return b?(b.dataset.studioLabel||key):key;}
  function paint(){
    buttons().forEach(function(b){var key=b.dataset.studioTag;
      b.querySelector('.tag-count').textContent=rows.filter(function(r){return matches(r,key);}).length;});
    rows.forEach(function(r){var b=r.querySelector('.studio-current'),on=current.has(r.dataset.studioKey);
      if(b){b.textContent=on?'Remove from Current':'Add to Current';b.setAttribute('aria-pressed',String(on));}});
  }
  function apply(key,save){
    if(!button(key))key='';
    active=key;
    rows.forEach(function(row){row.hidden=!matches(row,key)||(source&&source.value!=='__all__'&&row.dataset.studioSource!==source.value);});
    buttons().forEach(function(b){var on=b.dataset.studioTag===key;b.classList.toggle('on',on);b.setAttribute('aria-pressed',String(on));});
    paint();
    empty.hidden=rows.some(function(r){return !r.hidden;})||rows.length===0;
    if(kind==='studio')timeline(key);
    empty.textContent=key==='__current__'?'Current is empty. Unpick it to see every '+noun+', then add the ones you want to focus on.':
      isGroup(key)?'This group is empty. Unpick it to see every '+noun+', then drag '+noun+'s onto it by ⋮⋮.':'No '+noun+'s in this source.';
    if(save){var url=new URL(location.href);
      url.searchParams.delete(pre+'tag');url.searchParams.delete(pre+'group');
      if(key==='__current__')url.searchParams.set(pre+'group','current');
      else if(key)url.searchParams.set(pre+'tag',key);
      if(source&&source.value!=='__all__')url.searchParams.set('studio_source',source.value);else url.searchParams.delete('studio_source');
      var target=hashTarget();if(target&&target.hidden)url.hash='';history.replaceState(null,'',url);}
  }
  function setCurrent(row,on){
    var next=new Set(current);if(on)next.add(row.dataset.studioKey);else next.delete(row.dataset.studioKey);
    if(!writeList(storageKey,Array.from(next))){say('Could not save Current in this browser. Your selection has not changed.');return false;}
    current=next;apply(active,false);
    say(row.dataset.studioName+(on?' added to Current.':' removed from Current.'));return true;
  }
  function chips(row){
    var box=row.querySelector('.topic-tags');
    if(!box){box=document.createElement('span');box.className='topic-tags';row.querySelector('summary b').after(box);}
    box.textContent='';
    var fixed=[];try{fixed=JSON.parse(row.dataset.studioFixed||'[]');}catch(e){}   // a subfolder's or a theme's: no ×
    labels(row).forEach(function(t){var c=document.createElement('span');c.className='chip';c.dataset.tag=t;c.textContent=t;
      if(fixed.indexOf(t.toLowerCase())<0){var x=document.createElement('button');x.type='button';x.className='tag-x';
        x.title='Take out of '+t;x.setAttribute('aria-label','Take '+row.dataset.studioName+' out of '+t);x.textContent='×';
        c.appendChild(x);}
      box.appendChild(c);});
  }
  function makeGroup(label){
    var key=label.toLowerCase(),b=button(key);if(b)return b;
    var wrap=document.createElement('span');wrap.className='grp';
    b=document.createElement('button');b.type='button';b.className='tab';b.dataset.studioLabel=label;b.dataset.studioTag=key;
    b.setAttribute('aria-pressed','false');
    var em=document.createElement('span');em.className='grp-emoji';em.setAttribute('aria-hidden','true');em.textContent=emojiFor(label);
    b.appendChild(em);b.appendChild(document.createTextNode(label+' '));
    var n=document.createElement('span');n.className='tag-count';n.textContent='0';b.appendChild(n);
    var x=document.createElement('button');x.type='button';x.className='grp-x';x.dataset.studioDelete=key;
    x.title='Delete group '+label;x.setAttribute('aria-label','Delete group '+label);x.textContent='×';
    wrap.appendChild(b);wrap.appendChild(x);nav.insertBefore(wrap,button('__untagged__')||nav.querySelector('.grp-new'));return b;
  }
  var emo={};try{emo=JSON.parse(nav.dataset.studioEmoji||'{}');}catch(e){}
  function emojiFor(label){var low=label.toLowerCase(),words=emo.words||{},pal=emo.palette||[];
    var tokens=low.split(/[ _/&+-]+/).filter(Boolean);
    for(var w in words){var ascii=w.split('').every(function(c){return c.charCodeAt(0)<128;});
      if(ascii?tokens.some(function(t){return t===w||t.replace(/s$/,'')===w;}):low.indexOf(w)>=0)return words[w];}
    if(!pal.length)return '';var n=0;for(var ch of label)n+=ch.codePointAt(0);return pal[n%pal.length];}
  function post(body){body.path=owner;body.kind=kind;
    return fetch('/_board/studio-group',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})
      .then(function(r){return r.json().catch(function(){return {ok:false,err:'HTTP '+r.status};})
        .then(function(j){if(!r.ok||!j.ok)throw new Error(j.err||('HTTP '+r.status));return j;});});}
  function update(j){Object.keys(j.topics||{}).forEach(function(k){
    var row=rows.find(function(r){return r.dataset.studioKey===k;});
    if(row){row.dataset.studioTags=JSON.stringify(j.topics[k]);chips(row);}});apply(active,false);}
  function addTo(row,key){
    if(key==='__current__'){setCurrent(row,true);return;}
    var label=labelOf(key),name=row.dataset.studioName;
    post({op:'add',topic:row.dataset.studioKey,tag:label}).then(function(j){update(j);
      say(name+(j.changed?' added to ':' is already in ')+label+'.');})
      .catch(function(e){say('Could not add '+name+' to '+label+': '+e.message);});
  }
  function takeOut(row,label){var name=row.dataset.studioName;
    post({op:'remove',topic:row.dataset.studioKey,tag:label}).then(function(j){update(j);say(name+' taken out of '+label+'.');})
      .catch(function(e){say('Could not take '+name+' out of '+label+': '+e.message);});
  }
  function dropGroup(key){
    var label=labelOf(key),n=rows.filter(function(r){return tags(r).indexOf(key)>=0;}).length;
    function gone(){var b=button(key);if(b)(b.closest('.grp')||b).remove();
      apply(active===key?'':active,active===key);}
    if(!n){post({op:'delete',tag:label}).then(function(){gone();say('Group '+label+' deleted.');})
      .catch(function(e){say('Could not delete '+label+': '+e.message);});return;}
    say('');status.append('Delete group '+label+'? It comes off '+n+' '+noun+(n===1?'':'s')+'; the '+noun+'s stay. ');
    var yes=document.createElement('button');yes.type='button';yes.className='grp-ok';yes.textContent='Delete';
    var no=document.createElement('button');no.type='button';no.className='grp-cancel';no.textContent='Cancel';
    status.append(yes,' ',no);
    no.addEventListener('click',function(){say('');});
    yes.addEventListener('click',function(){say('Deleting '+label+' …');
      post({op:'delete',tag:label}).then(function(j){update(j);gone();
        say('Group '+label+' deleted. Its '+j.changed+' '+noun+(j.changed===1?' is':'s are')+' still listed.');})
        .catch(function(e){say('Could not delete '+label+': '+e.message);});});
  }
  var newBtn=nav.querySelector('.grp-new'),form=nav.querySelector('.grp-form'),input=form.querySelector('input');
  function openForm(on){form.hidden=!on;newBtn.hidden=on;if(on){input.value='';input.focus();}}
  function create(){var label=input.value.trim();
    if(!label){openForm(false);return;}
    if(label.length>30||/[`,·|*]/.test(label)||['current','all','untagged'].indexOf(label.toLowerCase())>=0){
      say('A group name is 1 to 30 characters, without ` , · | or *, and is not Current, All or Untagged.');return;}
    openForm(false);
    if(button(label.toLowerCase())){say('Group '+label+' already exists.');return;}
    post({op:'create',tag:label}).then(function(){makeGroup(label);apply(active,false);
      say('Group '+label+' made. Drag '+noun+'s onto it by ⋮⋮.');}).catch(function(e){say('Could not make '+label+': '+e.message);});}
  // groups made before they were saved on disk waited in this browser: save them once, then forget them
  if(kind==='studio'){readList(groupsKey).forEach(function(label){if(!button(label.toLowerCase()))
    post({op:'create',tag:label}).then(function(){makeGroup(label);apply(active,false);}).catch(function(){});});
  try{localStorage.removeItem(groupsKey);}catch(e){}}
  // drag a group button sideways to move it; the order is saved to studio/ (or related/) _groups.txt (b10 s02-D17)
  var dragged=false;
  nav.addEventListener('pointerdown',function(ev){
    var tab=ev.target.closest('.grp>.tab');if(!tab||ev.button!==0)return;
    var wrap=tab.parentNode,startX=ev.clientX,startY=ev.clientY,moved=false;
    function move(e){if(e.pointerId!==ev.pointerId)return;
      if(!moved&&Math.hypot(e.clientX-startX,e.clientY-startY)<6)return;
      if(!moved){moved=true;wrap.classList.add('moving');nav.classList.add('sorting');}
      var over=Array.from(nav.querySelectorAll('.grp')).find(function(g){if(g===wrap)return false;var r=g.getBoundingClientRect();
        return e.clientX>=r.left&&e.clientX<=r.right&&e.clientY>=r.top-8&&e.clientY<=r.bottom+8;});
      if(over){var r=over.getBoundingClientRect();nav.insertBefore(wrap,e.clientX<r.left+r.width/2?over:over.nextSibling);}
    }
    function finish(e){if(e.pointerId!==ev.pointerId)return;
      document.removeEventListener('pointermove',move);document.removeEventListener('pointerup',finish);document.removeEventListener('pointercancel',finish);
      if(!moved)return;
      wrap.classList.remove('moving');nav.classList.remove('sorting');dragged=true;setTimeout(function(){dragged=false;},0);
      var order=Array.from(nav.querySelectorAll('.grp>.tab')).map(function(b){return b.dataset.studioLabel;});
      post({op:'order',groups:order}).then(function(){say('Group order saved.');})
        .catch(function(e2){say('Could not save the group order: '+e2.message);});
    }
    document.addEventListener('pointermove',move);document.addEventListener('pointerup',finish);document.addEventListener('pointercancel',finish);
  });
  newBtn.addEventListener('click',function(){openForm(true);});
  form.querySelector('.grp-ok').addEventListener('click',create);
  form.querySelector('.grp-cancel').addEventListener('click',function(){openForm(false);});
  input.addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();create();}else if(e.key==='Escape'){openForm(false);}});
  nav.addEventListener('click',function(ev){
    var del=ev.target.closest('[data-studio-delete]');if(del){ev.preventDefault();dropGroup(del.dataset.studioDelete);return;}
    var b=ev.target.closest('[data-studio-tag]');if(!b||dragged)return;
    apply(b.dataset.studioTag===active?'':b.dataset.studioTag,true);});
  list.addEventListener('click',function(ev){var x=ev.target.closest('.tag-x');if(!x)return;
    ev.preventDefault();ev.stopPropagation();var row=x.closest('details[data-studio-key]'),chip=x.closest('.chip');
    if(row&&chip)takeOut(row,chip.dataset.tag);});
  if(source)source.addEventListener('change',function(){apply(active,true);});
  rows.forEach(function(row){
    var cur=row.querySelector('.studio-current');   // a Delivery row has none; without this guard the throw stopped every later handler (Free | Structured)
    if(cur)cur.addEventListener('click',function(ev){
      ev.preventDefault();ev.stopPropagation();setCurrent(row,!current.has(row.dataset.studioKey));});
    var handle=row.querySelector('.studio-drag');
    if(!handle)return;                      // a theme's own Report card (b10 s05): not draggable, its groups fixed
    handle.addEventListener('click',function(ev){ev.preventDefault();ev.stopPropagation();});
    handle.addEventListener('pointerdown',function(ev){
      if(ev.button!==0)return;ev.preventDefault();ev.stopPropagation();
      var startX=ev.clientX,startY=ev.clientY,ghost=null,moved=false,hot=null;
      if(handle.setPointerCapture)handle.setPointerCapture(ev.pointerId);
      function under(x,y){return buttons().find(function(b){var k=b.dataset.studioTag;if(k==='__untagged__')return false;
        var r=b.getBoundingClientRect();return x>=r.left&&x<=r.right&&y>=r.top&&y<=r.bottom;})||null;}
      function mark(b){if(hot)hot.classList.remove('drop-ready');hot=b;if(hot)hot.classList.add('drop-ready');}
      function move(e){
        if(e.pointerId!==ev.pointerId)return;
        if(!moved&&Math.hypot(e.clientX-startX,e.clientY-startY)<6)return;
        if(!moved){moved=true;row.classList.add('dragging');ghost=document.createElement('div');
          ghost.className='studio-drag-preview';ghost.textContent=row.dataset.studioName;document.body.appendChild(ghost);}
        ghost.style.left=(e.clientX+12)+'px';ghost.style.top=(e.clientY+12)+'px';
        mark(under(e.clientX,e.clientY));
      }
      function finish(e){
        if(e.pointerId!==ev.pointerId)return;
        document.removeEventListener('pointermove',move);document.removeEventListener('pointerup',finish);document.removeEventListener('pointercancel',finish);
        row.classList.remove('dragging');mark(null);if(ghost)ghost.remove();
        var b=moved&&e.type==='pointerup'?under(e.clientX,e.clientY):null;
        if(b)addTo(row,b.dataset.studioTag);
      }
      document.addEventListener('pointermove',move);document.addEventListener('pointerup',finish);document.addEventListener('pointercancel',finish);
    });
  });
  function restore(){var url=new URL(location.href),group=url.searchParams.get(pre+'group');
    var key=url.searchParams.get(pre+'tag')||(group==='current'?'__current__':'');
    if(source){var wanted=url.searchParams.get('studio_source')||'__all__';
      source.value=Array.from(source.options).some(function(o){return o.value===wanted;})?wanted:'__all__';}
    var target=hashTarget();
    if(target&&rows.indexOf(target)>=0){if(!matches(target,key))key='';if(source)source.value='__all__';}
    apply(key,false);
  }
  restore();window.addEventListener('popstate',restore);
  window.addEventListener('storage',function(ev){
    if(ev.key===storageKey){current=read();apply(active,false);}});
});
function tlGaps(tl){
  // one real axis (JL 261012: "show the days between them"): a day with nothing shown, between two that have
  // something, stays as a short row with a hollow dot; a run of more than 3 is one row, "N quiet days".
  // Before the first such day and after the last, nothing shows. The chart counts what the group shows; the
  // list below also what is picked.
  var wrap=tl.querySelector('.tl-wrap');if(!wrap)return;
  var picking=wrap.classList.contains('picking')&&wrap.dataset.level==='days';
  function lay(rs,full){var on=rs.map(full),a=on.indexOf(true),b=on.lastIndexOf(true);
    rs.forEach(function(r,j){var t=r.querySelector('time');if(t.dataset.label===undefined)t.dataset.label=t.textContent;
      t.textContent=t.dataset.label;r.hidden=a<0||j<a||j>b;r.classList.toggle('tl-quiet',!on[j]);});
    for(var j=a;a>=0&&j<=b;j++){if(on[j])continue;var k=j;while(k<=b&&!on[k])k++;
      if(k-j>3){rs[j].querySelector('time').textContent=(k-j)+' quiet days';for(var m=j+1;m<k;m++)rs[m].hidden=true;}j=k;}}
  lay(Array.from(tl.querySelectorAll('.tl-mrow')),function(r){return Number(r.dataset.tlN||0)>0;});
  lay(Array.from(tl.querySelectorAll('.tl-day')),function(d){
    return !!d.querySelector('.tl-topic:not([hidden])'+(picking?':not(.tl-off)':''));});
}
document.querySelectorAll('.studio-timeline .tl-levels').forEach(function(nav){
  // how much the Timeline shows: Days · Topics · Everything (JL 261011), remembered in this browser
  var axis=nav.closest('.tl-wrap'),saved='';if(!axis)return;
  function show(level){axis.dataset.level=level;nav.querySelectorAll('[data-tl-level]').forEach(function(b){
    b.setAttribute('aria-pressed',String(b.dataset.tlLevel===level));});tlGaps(axis.closest('.studio-timeline'));}
  try{saved=localStorage.getItem('workbench.timeline.level.v1')||'';}catch(e){}
  if(nav.querySelector('[data-tl-level="'+saved+'"]'))show(saved);
  nav.addEventListener('click',function(ev){var b=ev.target.closest('[data-tl-level]');if(!b)return;show(b.dataset.tlLevel);
    try{localStorage.setItem('workbench.timeline.level.v1',b.dataset.tlLevel);}catch(e){}});});
document.querySelectorAll('.studio-timeline .tl-map').forEach(function(map){
  // the chart's columns: the topic groups or the topics (JL 261011), remembered in this browser. A picked
  // group shows its topics; by group shows every group, so it unpicks the group (JL 261012: "我好像没法选了")
  var nav=map.closest('.tl-wrap').querySelector('.tl-cols'),saved='',pref=map.dataset.cols;if(!nav)return;
  var bar='.studio-topics:not([data-group-kind]) .studio-filters';
  function on(){return document.querySelector(bar+' [data-studio-tag].on');}
  // a group picked from here hides or shows the topic cards above, so the page grows or shrinks over the
  // Timeline; keep its toolbar where it was on screen (JL 261012: "它会跳到最上面，而不是留在 timeline 这里")
  var levels=map.closest('.tl-wrap').querySelector('.tl-levels');
  function keep(fn){var y=levels.getBoundingClientRect().top;fn();
    var d=levels.getBoundingClientRect().top-y;if(d)window.scrollBy(0,d);}
  function cols(){var c=on()?'topics':pref;map.dataset.cols=c;nav.querySelectorAll('[data-tl-cols]').forEach(function(b){
    b.setAttribute('aria-pressed',String(b.dataset.tlCols===c));});}
  try{saved=localStorage.getItem('workbench.timeline.cols.v1')||'';}catch(e){}
  if(saved==='groups'||saved==='topics')pref=saved;
  cols();
  nav.addEventListener('click',function(ev){var b=ev.target.closest('[data-tl-cols]');if(!b)return;pref=b.dataset.tlCols;
    try{localStorage.setItem('workbench.timeline.cols.v1',pref);}catch(e){}
    var g=on();keep(function(){if(pref==='groups'&&g)g.click();cols();});});
  // the Timeline's group picker clicks the bar's own button: picking the picked one again, or All, unpicks it
  var strip=map.closest('.tl-wrap').querySelector('.tl-groups');
  if(strip)strip.addEventListener('click',function(ev){var x=ev.target.closest('[data-tl-tag]');if(!x)return;
    var k=x.dataset.tlTag,t=k?document.querySelector(bar+' [data-studio-tag="'+CSS.escape(k)+'"]'):on();
    if(t)keep(function(){t.click();});});
  // pick topics in the chart (JL 261011: "we can select the topics we are interest in we show there content"):
  // their decisions, sessions and notes show under it, on the same axis; pick again to drop one
  var wrap=map.closest('.tl-wrap'),list=wrap.querySelector('.tl-list'),line=wrap.querySelector('.tl-picked'),picked=new Set();
  function pick(){wrap.classList.toggle('picking',picked.size>0);
    map.querySelectorAll('.tl-col,.tl-cell').forEach(function(c){c.classList.toggle('on',picked.has(c.dataset.tlKey));});
    list.querySelectorAll('.tl-topic').forEach(function(t){t.classList.toggle('tl-off',!picked.has(t.dataset.tlKey));});
    tlGaps(wrap.closest('.studio-timeline'));
    line.textContent='';if(!picked.size)return;
    var names=Array.from(map.querySelectorAll('.tl-col')).filter(function(c){return picked.has(c.dataset.tlKey);})
      .map(function(c){return c.title||c.textContent;});
    line.appendChild(document.createTextNode('Reading '+names.join(' · ')));
    var x=document.createElement('button');x.type='button';x.textContent='Clear';
    x.addEventListener('click',function(){picked.clear();pick();});line.appendChild(x);}
  // a group or source picked anywhere: the columns follow, and a picked topic that no longer shows is dropped
  map.closest('.studio-timeline').addEventListener('tl-shown',function(){cols();
    map.querySelectorAll('.tl-col[hidden]').forEach(function(c){picked.delete(c.dataset.tlKey);});pick();});
  map.addEventListener('click',function(ev){var g=ev.target.closest('.tl-gcol,.tl-gb');
    if(g){var key=(g.closest('[data-tl-group]')||g).dataset.tlGroup;
      var t=document.querySelector(bar+' [data-studio-tag="'+CSS.escape(key)+'"]');
      keep(function(){if(t&&!t.classList.contains('on'))t.click();cols();});return;}
    var c=ev.target.closest('.tl-col,.tl-cell');if(!c||(c.classList.contains('tl-cell')&&!c.querySelector('.tl-b')))return;
    ev.preventDefault();var k=c.dataset.tlKey;if(picked.has(k))picked.delete(k);else picked.add(k);pick();});});
document.querySelectorAll('.studio-timeline .tl-name').forEach(function(a){a.addEventListener('click',function(ev){
  // a topic's name in the Timeline opens its row above
  var d=document.getElementById(decodeURIComponent(a.hash.slice(1)));if(!d)return;
  ev.preventDefault();d.open=true;load(d);d.scrollIntoView({block:'start'});history.replaceState(null,'',a.hash);});});
document.querySelectorAll('.studio-folder').forEach(function(box){
  // Folder (b10 s09): a folder's rows load the first time it is opened, from ?view=dir (toggle does not bubble)
  box.addEventListener('toggle',function(ev){var d=ev.target;
    if(!d.matches('details[data-dir]')||!d.open||d.dataset.loaded)return;
    var ul=d.querySelector(':scope>ul');d.dataset.loaded='1';ul.innerHTML='<li class=mut>Loading…</li>';
    fetch('/_board/workbench?'+new URLSearchParams({view:'dir',path:d.dataset.dir}))
      .then(function(r){if(!r.ok)throw r.status;return r.text();}).then(function(h){ul.innerHTML=h;})
      .catch(function(){ul.innerHTML='<li class=mut>This folder could not be read.</li>';delete d.dataset.loaded;});},true);
  // past 300 rows a folder stops; its button loads them all
  box.addEventListener('click',function(ev){var b=ev.target.closest('.fd-more button');if(!b)return;
    var ul=b.closest('ul');b.disabled=true;b.textContent='Loading…';
    fetch('/_board/workbench?'+new URLSearchParams({view:'dir',path:b.dataset.dir,all:'1'}))
      .then(function(r){if(!r.ok)throw r.status;return r.text();}).then(function(h){ul.innerHTML=h;})
      .catch(function(){b.disabled=false;b.textContent='Could not load; try again';});});});
document.querySelectorAll('details.topic .draw-edit').forEach(function(b){b.addEventListener('click',function(ev){
  ev.preventDefault();ev.stopPropagation();
  var d=b.closest('details'),f=d.querySelector(':scope > .st-pane:not([hidden]) > iframe')||d.querySelector('iframe'),on=b.textContent==='Edit';
  d.open=true;f.src=on?f.dataset.edit:f.dataset.src;b.textContent=on?'Finish editing':'Edit';});});
// a topic with a structured side (its mind map, <topic>.mindmap.md): Free | Structured, one pane a side, the mind map drawn and
// edited in place as the draft's §1 map; Edit (the free canvas) shows only on Free; the ↗ opens the side showing; the
// card remembers the choice in this browser
document.querySelectorAll('details.topic[data-sides]').forEach(function(d){
  var key='workbench.studio.side.v1:'+d.id,bar=d.querySelector(':scope > summary .st-side');
  function show(side,save){
    bar.querySelectorAll('[data-side]').forEach(function(b){b.setAttribute('aria-pressed',String(b.dataset.side===side));});
    d.querySelectorAll(':scope > .st-pane').forEach(function(p){p.hidden=p.dataset.side!==side;
      var f=p.querySelector(':scope > iframe');if(f&&f.dataset.edit&&f.getAttribute('src')===f.dataset.edit)f.src=f.dataset.src;});
    var ed=d.querySelector(':scope > summary .draw-edit');
    if(ed){ed.hidden=(ed.dataset.sides||'').split(' ').indexOf(side)<0;ed.textContent='Edit';}
    var a=d.querySelector(':scope > summary a.side-link'),h=a&&a.getAttribute('data-href-'+side);
    if(a){a.hidden=!h;if(h){a.href=h;a.dataset.pop=a.getAttribute('data-pop-'+side);}}
    d.dataset.side=side;if(save){try{localStorage.setItem(key,side);}catch(e){}}load(d);if(window.mmDraw)setTimeout(window.mmDraw,0);}
  var saved=null;try{saved=localStorage.getItem(key);}catch(e){}
  var ok=function(s){var b=bar.querySelector('[data-side="'+s+'"]');return b&&!b.disabled;};
  show(saved&&ok(saved)?saved:d.dataset.side,false);
  bar.addEventListener('click',function(ev){var b=ev.target.closest('[data-side]');if(!b||b.disabled)return;
    ev.preventDefault();ev.stopPropagation();d.open=true;show(b.dataset.side,true);});});
document.querySelectorAll('.rp-live').forEach(function(b){b.addEventListener('click',function(){
  var f=b.querySelector('iframe');if(f&&f.hasAttribute('inert')){f.removeAttribute('inert');b.classList.add('on');}});});
var t=hashTarget();if(t&&t.tagName==='DETAILS'){for(var a=t;a;a=a.parentElement){if(a.tagName==='DETAILS'){a.open=true;load(a);}}t.scrollIntoView({block:'start'});}
})();
"""

# The pop-out (Insight's pop box, as the old boards had it): any [data-pop] link opens in it.
POP_HTML = ('<dialog id=frame-pop aria-label="Pop-out"><div class=pop-bar><span class=pop-title id=frame-pop-title>Pop-out</span>'
            '<a id=frame-pop-new target=_blank rel=noopener>Open in its own tab ↗</a>'
            '<button type=button class=pop-x id=frame-pop-x aria-label=Close>×</button></div>'
            '<iframe class=pop-frame id=frame-pop-frame title="Pop-out"></iframe></dialog>')
# A page the frame shows inside a Space (a Page view, an older theme page) keeps only its content: its own
# top (the title, back link and band in <body>'s <header>, its tab row in <body>'s <nav>, a bare <h1>) is
# hidden, so the frame's top is the only one (b03 s32-D14, JL 261008: "update all of them"). Same-origin
# pages only; a page that already drops its top for embed=1 is left as it is.
EMBED_JS = """
(function(){
  var CSS='html.wb-embed body>header,html.wb-embed body>nav,html.wb-embed body>h1,html.wb-embed .wb-band,'
   +'html.wb-embed .wb-links{display:none!important}html.wb-embed body{padding-top:4px}';
  function tidy(f){try{var d=f.contentDocument;if(!d||!d.documentElement)return;
    var h=d.documentElement;if(h.classList.contains('wb-embed-top'))return;h.classList.add('wb-embed','wb-embed-top');
    var st=d.createElement('style');st.textContent=CSS;(d.head||h).appendChild(st);}catch(e){}}
  function hook(f){f.addEventListener('load',function(){tidy(f);});tidy(f);}
  document.querySelectorAll('iframe.page-view,iframe.space-frame').forEach(hook);
  new MutationObserver(function(ms){ms.forEach(function(m){m.addedNodes.forEach(function(n){
    if(n.nodeType!==1)return;(n.matches('iframe.page-view,iframe.space-frame')?[n]:
      [].slice.call(n.querySelectorAll('iframe.page-view,iframe.space-frame'))).forEach(hook);});});})
   .observe(document.body,{childList:true,subtree:true});
})();
"""

# The Guide opens under the page's title, not above it, and the title reads "<theme> · Guide" while it is open
# (JL 261008: "seems we have issues in the guide"): the Guide's mount puts its frame after the level row
GUIDE_TITLE_JS = """
document.addEventListener('DOMContentLoaded',function(){
  var f=document.getElementById('wb-guide-frame'),hd=document.querySelector('header.page-title'),h=hd&&hd.querySelector('h1');
  if(!f||!hd||!h)return;hd.after(f);var own=h.innerHTML,g=h.getAttribute('data-guide');
  function sync(){var open=document.body.classList.contains('wb-guide-open');
    if(open&&h.textContent!==g)h.textContent=g;else if(!open&&h.innerHTML!==own)h.innerHTML=own;}
  new MutationObserver(sync).observe(document.body,{attributes:true,attributeFilter:['class']});sync();
});
"""

POP_JS = """
(function(){var dlg=document.getElementById('frame-pop'),fr=document.getElementById('frame-pop-frame');if(!dlg)return;
document.addEventListener('click',function(ev){var a=ev.target.closest('a[data-pop]');
  if(!a||ev.ctrlKey||ev.metaKey||ev.shiftKey||ev.altKey||!dlg.showModal)return;ev.preventDefault();
  document.getElementById('frame-pop-title').textContent=a.dataset.pop;document.getElementById('frame-pop-new').href=a.href;
  // Excalidraw refuses a same-site embed: a drawing opens with no referrer, as the folds do
  fr.referrerPolicy=new URL(a.href,location.href).pathname.indexOf('/_excalidraw/')===0?'no-referrer':'';
  fr.src=a.href;dlg.showModal();});
document.getElementById('frame-pop-x').addEventListener('click',function(){dlg.close();});
dlg.addEventListener('click',function(ev){if(ev.target===dlg)dlg.close();});
dlg.addEventListener('close',function(){fr.removeAttribute('src');});})();
"""
