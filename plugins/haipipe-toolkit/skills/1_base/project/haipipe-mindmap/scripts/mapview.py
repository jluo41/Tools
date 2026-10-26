"""The structure map, shared: the one renderer behind a draft Task's §1 Structure map
(servers/workbench/workbench-task-draft/draft_steps.py `_plan_map`) and a Studio topic's mind map (`mmmap.py`), so the
two look and edit alike (JL 261026: "你把他们那个 map 也放到我们这个新的 skill 里面去 … 这样的话他们就共享了").

    render(name, arc, parts, asks, paras, …)   the map: the root card, a card per paragraph (or branch) with the
                                                question it hands to the next, a plain line per point

The page posts each change to its `endpoint` (a draft's `/_board/draft-plan`, a mind map's `/_board/mindmap`) with one
payload both answer: `what` (words, role, para, ask, arc, add, addpara, drop, move; a mind map also note), `s` a point,
`p` a paragraph, `was`, `value`, and `task` and `file`, where the map came from. A mind map also asks for `extras`: a
point's detail behind ▸, the lines under a point, and a chip per file it names; a draft's map draws without them.
"""
from __future__ import annotations

import html

esc = lambda s: html.escape(str(s), quote=True)


def editable(what: str, raw: str, shown: str, tag: str, p: str = "") -> str:
    """One piece of the map a person types into: it shows `shown`, and while typed in, its words as written."""
    name = tag.split()[0]
    return (f'<{tag} data-edit={what}{(" data-p=" + chr(34) + esc(p) + chr(34)) if p else ""} '
            f'data-raw="{esc(raw)}" contenteditable=plaintext-only spellcheck=false>{shown}</{name}>')


def render(name: str, arc: str, parts: list, asks: dict, paras: list, *, task: str = "", file: str = "",
           inline=esc, chips=None, plabel=None, pnode=None, more=None, sub=None, endpoint: str = "",
           extras: bool = False) -> str:
    """The map. `parts` [(C<n>, its name)] (a part is drawn when there is more than one), `asks` {paragraph: the
    question it hands on}, `paras` [(paragraph, its job, [(point, role, words, note)])]. `inline(words)` shows a
    point's words; `chips(point, words, note)` what follows them (a draft's evidence cards; a mind map's file chips);
    `plabel(paragraph)` the small grey label over a paragraph's name; `pnode(paragraph)` what follows that name;
    `more(id, note)` a mind map's (▸, detail); `sub(point)` the lines under a point. Without them, §1 exactly."""
    chips = chips or (lambda s, words, note: "")
    plabel = plabel or (lambda pid: pid)

    def para_html(i, pid, job, bullets):
        leaves = []
        for s, role, words, note in bullets:
            btn, detail = more(s, note) if more else ("", "")
            tip = (" title=" + chr(34) + esc(note) + chr(34)) if note and not more else ""
            leaves.append(f'<li data-s="{esc(s)}"{tip}>'
                          f'<span class=pm-s draggable=true>{esc(s) if not more else esc(plabel(s))}</span>'
                          f'{editable("role", role, esc(role), "span class=pm-role")}'
                          f'<span class=pm-w>{editable("words", words, inline(words), "span class=pm-t")}'
                          f'{chips(s, words, note)}{btn}</span>{detail}{sub(s) if sub else ""}</li>')
        # a point or a paragraph added where it goes (JL 261020: "How could I add the P here or add the S here?")
        leaves.append('<li class=pm-add><button type=button class=pm-plus data-add=point>＋ point</button></li>')
        ask = (f'<div class=pm-q>{editable("ask", asks.get(pid, ""), esc(asks.get(pid, "")), "span", pid)}</div>'
               if i < len(paras) - 1 else "")
        return (f'<div class=pm-para data-p="{esc(pid)}"><div class="pm-node pm-pnode"><span class=pm-id>{esc(plabel(pid))}'
                f'</span>{editable("para", job, esc(job), "b")}{pnode(pid) if pnode else ""}</div><ul class=pm-leaves>'
                f'{"".join(leaves)}</ul></div>{ask}'
                f'<div class=pm-addp><button type=button class=pm-plus data-add=para data-after="{esc(pid)}">＋ paragraph'
                '</button></div>')

    one = len(parts) <= 1
    name = f"{parts[0][0]} · {parts[0][1]}" if one and parts else name
    body = []
    if one:
        body = [para_html(i, *p) for i, p in enumerate(paras)]
    else:
        for cid, cname in parts:
            mine = [(i, p) for i, p in enumerate(paras) if p[0].split(".")[0] == cid]
            if mine:
                body.append(f'<div class=pm-part><div class="pm-node pm-cnode"><span class=pm-id>{esc(cid)}</span>'
                            f'<b>{esc(cname)}</b></div><div>{"".join(para_html(i, *p) for i, p in mine)}</div></div>')
    # editable in place where it is read (JL 261020: "how could I operate and edit it?"): its endpoint writes it
    point = f' data-endpoint="{esc(endpoint)}"' if endpoint else ""
    return (CSS + (EXTRA_CSS if extras else "") + f'<div class=pm-edit data-task="{esc(task)}" data-file="{esc(file)}"{point}>'
            '<span class=pm-msg role=status></span><div class=pm><svg class=pm-wires aria-hidden=true></svg>'
            f'<div class="pm-node pm-root"><b>{esc(name)}</b>' + (editable("arc", arc, esc(arc), "p") if arc else "")
            + f'</div><div>{"".join(body)}</div></div></div>' + JS + (EXTRA_JS if extras else ""))


CSS = """<style>
/* the map grows to its widest Point and its box scrolls sideways; a Point never wraps (JL 261021: "怎么让这个 structure
   的宽度能够无限延伸 ... 我就是想让它一直不要有这个 break") */
.pm{position:relative;display:grid;grid-template-columns:250px auto;gap:0 64px;align-items:center;padding:8px 4px;
 width:max-content;min-width:100%;box-sizing:border-box}
.pm-wires{position:absolute;left:0;top:0;pointer-events:none;overflow:visible}
.pm-wires path{fill:none;stroke:var(--mut);stroke-opacity:.45;stroke-width:1.4}
.pm-node{position:relative;background:var(--card);border:1.5px solid var(--fg);border-radius:10px}
.pm-root{padding:14px 16px;font-size:13px;line-height:1.5}.pm-root b{display:block;font-size:17px;margin-bottom:6px}
.pm-root p{margin:0;color:var(--mut)}
.pm-para{display:grid;grid-template-columns:230px auto;gap:0 56px;align-items:center;margin:4px 0}
.pm-pnode,.pm-cnode{padding:9px 12px;font-size:14.5px;line-height:1.35}.pm-id{display:block;font-size:11.5px;color:var(--mut)}
.pm-part{display:grid;grid-template-columns:180px auto;gap:0 48px;align-items:center;margin:8px 0}
.pm-part .pm-para{grid-template-columns:210px auto;gap:0 48px}.pm-part .pm-q{width:210px}
.pm-leaves{list-style:none;margin:0;padding:0}
.pm-leaves li{position:relative;padding:3px 0;line-height:1.5;font-size:14px;white-space:nowrap}
.pm-s{display:inline-block;min-width:30px;font-size:12px;color:var(--mut)}
.pm-role{display:inline-block;min-width:86px;box-sizing:border-box;text-align:center;margin-right:7px;padding:0 6px;border:1px solid var(--line);border-radius:9px;font-size:11.5px;color:var(--mut)}
.pm-card{display:inline-block;margin-left:2px;padding:0 5px;border:1px solid;border-radius:3px;font-size:11px;font-weight:600}
.pm-flag{color:#e03131;font-weight:600}
.pm-edit{position:relative}.pm-msg{position:absolute;right:4px;top:0;font-size:12px;color:var(--mut)}
[data-edit]{outline:none;border-radius:3px;cursor:text}[data-edit]:hover{background:var(--wash)}
[data-edit]:focus{background:#fff3bf;color:var(--fg)}.pm-role[data-edit]{border-radius:9px}.pm-role:empty{border-style:dashed}
.pm-q [data-edit]::before{content:"↓ "}.pm-s{cursor:grab}.pm-leaves li.pm-drop{box-shadow:0 -2px 0 var(--acc)}
.pm-pnode.pm-drop{border-color:var(--acc)}[data-edit].pm-bad{outline:1.5px dashed #e03131;outline-offset:2px}
.pm-err{color:#e03131;font-size:12px;font-weight:600;font-style:normal}.pm-leaves li.pm-new .pm-s{visibility:hidden}
.pm-q{width:230px;box-sizing:border-box;margin:2px 0;padding:2px 8px 2px 14px;font-size:12.5px;font-style:italic;color:var(--mut);line-height:1.4}
.pm-q [data-edit]:empty::before{content:"↓ ＋ question";opacity:.7}
.pm-plus{border:0;background:none;padding:1px 4px;font:12px/1.4 system-ui,sans-serif;color:var(--mut);opacity:.6;cursor:pointer}
.pm-plus:hover{opacity:1;color:var(--acc)}.pm-leaves li.pm-add{padding:1px 0 0 30px}
.pm-addp{width:230px;box-sizing:border-box;padding:0 0 2px 10px}.pm-part .pm-addp{width:210px}
/* the ＋ marks stay hidden until the mouse is over their paragraph or their gap (JL 261020: "能不能让它默认隐身，等我鼠标
   移过去的时候再显示出来"); they keep their room, so nothing moves; a touch screen, with no hover, always shows them */
@media(hover:hover){.pm-leaves li.pm-add,.pm-addp,.pm-q [data-edit]:empty::before{opacity:0;transition:opacity .12s}
 .pm-para:hover li.pm-add,.pm-addp:hover,.pm-para:hover+.pm-addp,.pm-para:hover+.pm-q+.pm-addp,.pm-q:hover+.pm-addp,
 .pm-add:focus-within,.pm-addp:focus-within{opacity:1}
 .pm-para:hover+.pm-q [data-edit]:empty::before,.pm-q:hover [data-edit]:empty::before,.pm-q [data-edit]:empty:focus::before{opacity:.7}}
.pm-pnode [data-edit]:empty{display:block;min-height:1.35em;border-bottom:1px dashed var(--line)}
@media(max-width:1000px){.pm,.pm-para,.pm-part,.pm-part .pm-para{grid-template-columns:minmax(0,1fr);gap:8px}.pm-wires{display:none}
 .pm{width:auto}
 .pm-leaves{padding-left:14px;border-left:2px solid var(--line)}.pm-q,.pm-part .pm-q,.pm-addp,.pm-part .pm-addp{width:auto}}
</style>"""
# the branches drawn after layout, so a leaf that wraps still gets its wire: the Section to each part (or straight to
# each paragraph), each part to its paragraphs, each paragraph to each of its Bullets
JS = """<script>
(function(){if(window.__pmMap)return;window.__pmMap=1;
 function wire(a,b,o,leaf){var p=a.getBoundingClientRect(),q=b.getBoundingClientRect();
  var x1=p.right-o.left,y1=p.top+p.height/2-o.top,x2=q.left-o.left-6,y2=(leaf?q.top+12:q.top+q.height/2)-o.top,m=(x1+x2)/2;
  return '<path d="M'+x1+','+y1+' C'+m+','+y1+' '+m+','+y2+' '+x2+','+y2+'"/>';}
 function draw(){document.querySelectorAll('.pm').forEach(function(m){var svg=m.querySelector('.pm-wires');
  if(!m.offsetParent||getComputedStyle(svg).display==='none')return;
  var o=m.getBoundingClientRect(),root=m.querySelector('.pm-root'),d='';
  svg.setAttribute('width',o.width);svg.setAttribute('height',o.height);
  m.querySelectorAll('.pm-part').forEach(function(pt){d+=wire(root,pt.querySelector('.pm-cnode'),o);});
  m.querySelectorAll('.pm-para').forEach(function(pa){var p=pa.querySelector('.pm-pnode'),pt=pa.closest('.pm-part');
   d+=wire(pt?pt.querySelector('.pm-cnode'):root,p,o);
   pa.querySelectorAll('.pm-leaves>li:not(.pm-add)').forEach(function(l){d+=wire(p,l,o,true);});});
  svg.innerHTML=d;});}
 window.addEventListener('resize',draw);window.addEventListener('load',draw);setTimeout(draw,60);
 document.addEventListener('toggle',function(){setTimeout(draw,0);},true);
 window.pmDraw=draw;document.addEventListener('input',function(e){if(e.target.closest&&e.target.closest('.pm'))draw();});
})();
</script>""" + """<script>
(function(){if(window.__pmEdit)return;window.__pmEdit=1;
 function host(el){return el.closest('.pm-edit');}
 function say(el,t,bad){var m=host(el).querySelector('.pm-msg');m.textContent=t||'';m.style.color=bad?'#c92a2a':'';
  if(t&&!bad)setTimeout(function(){if(m.textContent===t)m.textContent='';},1800);}
 /* a refusal is said where the person typed, and the words they typed stay, outlined red (JL 261020: "why the
    content is not saved here?") */
 function bad(el,msg){var x=el.parentNode.querySelector(':scope > .pm-err');if(!x){x=document.createElement('span');x.className='pm-err';el.after(x);}
  x.textContent=' not saved: '+msg;el.classList.add('pm-bad');say(el,'not saved: '+msg,true);if(window.pmDraw)window.pmDraw();}
 function post(el,body){var h=host(el);body.task=h.dataset.task;body.file=h.dataset.file;say(el,'…');
  return fetch(h.dataset.endpoint||'/_board/draft-plan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})
   .then(function(r){return r.json();}).then(function(j){if(j.file)h.dataset.file=j.file;
    if(!j.ok){var e=new Error(j.err||'not saved');e.reload=/newer/.test(j.err||'');throw e;}
    el.classList.remove('pm-bad');var x=el.parentNode&&el.parentNode.querySelector(':scope > .pm-err');if(x)x.remove();
    say(el,'saved');return j;});}
 /* the map again from the server, after a point was added, taken out or moved */
 function refresh(h,then){fetch(location.href,{credentials:'same-origin'}).then(function(r){return r.text();}).then(function(t){
  var n=new DOMParser().parseFromString(t,'text/html').querySelector('.pm-edit[data-task="'+h.dataset.task+'"]');
  if(n){h.innerHTML=n.innerHTML;h.dataset.file=n.dataset.file;}if(window.pmDraw)window.pmDraw();if(then)then();});}
 /* a new point or paragraph refused because the draft changed under the page: the map reloads, and what was typed
    comes back in the same paragraph, outlined red, so clicking away adds it to the newest draft */
 var AGAIN='the draft changed under this page; click away to add it again';
 function again(h,what,pid,txt,role){refresh(h,function(){var pa=h.querySelector('.pm-para[data-p="'+pid+'"]');
  if(!pa){say(h.querySelector('.pm-msg')||h,'not saved: '+pid+' is gone in the newest draft',true);return;}
  if(what==='para'){var row=pa.nextElementSibling;while(row&&!row.classList.contains('pm-addp'))row=row.nextElementSibling;
   var b=row&&row.querySelector('[data-add=para]');if(!b)return;b.click();var e=h.querySelector('.pm-newp [data-edit]');e.textContent=txt;bad(e,AGAIN);return;}
  var pts=pa.querySelectorAll('li[data-s]');newpoint(pa.querySelector('li.pm-add'),pts.length?pts[pts.length-1].dataset.s:'',pid);
  var n=pa.querySelector('li.pm-new');n.querySelector('.pm-role').textContent=role||'';var w=n.querySelector('.pm-t');w.textContent=txt;bad(w,AGAIN);});}
 function words(el){return el.innerText.replace(/\\s+/g,' ').trim();}
 function newpoint(before,after,pid){var n=document.createElement('li');n.className='pm-new';n.dataset.after=after||'';n.dataset.p=pid;
  n.innerHTML='<span class=pm-s>+</span><span class=pm-role data-edit=role data-raw="" contenteditable=plaintext-only></span>'+
   '<span class=pm-w><span class=pm-t data-edit=words data-raw="" contenteditable=plaintext-only></span></span>';
  before.parentNode.insertBefore(n,before);n.querySelector('.pm-t').focus();if(window.pmDraw)window.pmDraw();}
 /* ＋ point: a new point last in its paragraph; ＋ paragraph: a new paragraph after this one, named first */
 document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.pm-edit [data-add]');if(!b)return;e.preventDefault();
  if(b.dataset.add==='point'){var ul=b.closest('.pm-leaves'),pts=ul.querySelectorAll('li[data-s]');
   newpoint(b.closest('li'),pts.length?pts[pts.length-1].dataset.s:'',b.closest('.pm-para').dataset.p);return;}
  var row=b.closest('.pm-addp'),n=document.createElement('div');n.className='pm-para pm-newp';n.dataset.after=b.dataset.after;
  n.innerHTML='<div class="pm-node pm-pnode"><span class=pm-id>＋</span><b data-edit=newpara data-raw="" contenteditable=plaintext-only></b></div><ul class=pm-leaves></ul>';
  row.after(n);n.querySelector('[data-edit]').focus();if(window.pmDraw)window.pmDraw();});
 document.addEventListener('focusin',function(e){var el=e.target.closest&&e.target.closest('.pm-edit [data-edit]');if(!el||el._html!=null)return;
  el._html=el.innerHTML;if(!el.classList.contains('pm-bad'))el.textContent=el.dataset.raw;});
 document.addEventListener('keydown',function(e){var el=e.target.closest&&e.target.closest('.pm-edit [data-edit]');if(!el)return;
  if(e.key==='Escape'){e.preventDefault();el.textContent=el.dataset.raw;el.blur();return;}
  if(e.key!=='Enter')return;e.preventDefault();
  /* Enter after a point: a new point below it, in the same paragraph */
  var li=el.dataset.edit==='words'&&el.closest('li');
  if(li&&words(el)){el.blur();newpoint(li.nextSibling,li.dataset.s||li.dataset.after||'',li.closest('.pm-para').dataset.p);}else el.blur();});
 document.addEventListener('focusout',function(e){var el=e.target.closest&&e.target.closest('.pm-edit [data-edit]');if(!el)return;
  var h=host(el),li=el.closest('li'),v=words(el),was=el.dataset.raw,html=el._html;el._html=null;
  if(el.dataset.edit==='newpara'){var np=el.closest('.pm-newp');if(!v){np.remove();if(window.pmDraw)window.pmDraw();return;}
   post(el,{what:'addpara',after:np.dataset.after,value:v}).then(function(){refresh(h);})
    .catch(function(err){if(err.reload)again(h,'para',np.dataset.after,v);else bad(el,err.message);});return;}
  if(li&&li.classList.contains('pm-new')){
   if(e.relatedTarget&&li.contains(e.relatedTarget))return;          /* from the role to the words of the new point */
   var t=words(li.querySelector('.pm-t'));if(!t){li.remove();if(window.pmDraw)window.pmDraw();return;}
   var role=words(li.querySelector('.pm-role'));
   post(el,{what:'add',after:li.dataset.after,p:li.dataset.p,value:t,role:role})
    .then(function(){refresh(h);}).catch(function(err){if(err.reload)again(h,'point',li.dataset.p,t,role);else bad(el,err.message);});return;}
  if(v===was){el.innerHTML=html!=null?html:el.innerHTML;return;}
  var body={what:el.dataset.edit,was:was,value:v};if(li)body.s=li.dataset.s;
  if(el.dataset.p)body.p=el.dataset.p;else if(el.dataset.edit==='para')body.p=el.closest('.pm-para').dataset.p;
  /* a point emptied is taken out */
  if(el.dataset.edit==='words'&&!v)body.what='drop';
  post(el,body).then(function(j){if(body.what==='drop'){refresh(h);return;}el.dataset.raw=v;el.innerHTML=j.html!=null?j.html:v;
    if(window.pmDraw)window.pmDraw();})
   .catch(function(err){bad(el,err.message);});});
 /* a point dragged by its S label: onto another point to go before it, onto a paragraph to go last in it */
 var drag=null;
 document.addEventListener('dragstart',function(e){var s=e.target.closest&&e.target.closest('.pm-edit .pm-s');if(!s)return;
  drag=s.closest('li');e.dataTransfer.effectAllowed='move';e.dataTransfer.setData('text/plain',drag.dataset.s);});
 function spot(e){return drag&&e.target.closest&&(e.target.closest('.pm-leaves li[data-s]')||e.target.closest('.pm-pnode'));}
 document.addEventListener('dragover',function(e){var t=spot(e);document.querySelectorAll('.pm-drop').forEach(function(x){x.classList.remove('pm-drop');});
  if(!t||t===drag||host(t)!==host(drag))return;e.preventDefault();t.classList.add('pm-drop');});
 document.addEventListener('drop',function(e){var t=spot(e);document.querySelectorAll('.pm-drop').forEach(function(x){x.classList.remove('pm-drop');});
  if(!t||t===drag)return;e.preventDefault();var h=host(drag),body={what:'move',s:drag.dataset.s,p:t.closest('.pm-para').dataset.p};
  if(t.tagName==='LI')body.before=t.dataset.s;drag=null;
  post(t,body).then(function(){refresh(h);}).catch(function(err){say(t,'not saved: '+err.message,true);if(err.reload)refresh(h);});});
 document.addEventListener('dragend',function(){drag=null;});
})();
</script>"""


# A mind map's extras on §1's look: ▸ opens a point's detail below it (Markdown, its links and pictures), ✎ edits the
# detail; the lines under a point, indented; a chip per file a point names, as §1's evidence chips
EXTRA_CSS = """<style>
.pm-more{border:0;background:none;padding:0 2px 0 6px;font:11px/1 system-ui,sans-serif;color:var(--mut);cursor:pointer}
.pm-more[aria-expanded=true]{transform:rotate(90deg)}.pm-more[data-empty]{opacity:0}.pm-leaves li:hover .pm-more[data-empty]{opacity:.5}
.pm-detail{margin:3px 0 6px 30px;padding:6px 10px;max-width:560px;white-space:normal;font-size:12.5px;line-height:1.5;
 color:var(--fg);background:var(--wash);border:1px solid var(--line);border-radius:7px}
.pm-detail p{margin:0 0 4px}.pm-detail ul{margin:0 0 4px;padding-left:18px}.pm-detail img{display:block;max-width:420px;
 max-height:300px;border:1px solid var(--line);border-radius:6px;margin:4px 0;background:#fff}
.pm-pen{border:0;background:none;padding:0;font-size:12px;color:var(--mut);cursor:pointer;opacity:.6}.pm-pen:hover{opacity:1}
.pm-detail textarea{display:block;width:520px;min-height:90px;font:12.5px/1.5 ui-monospace,Menlo,monospace}
.pm-sub{list-style:none;margin:0;padding:0 0 0 30px}.pm-sub li{padding:2px 0;font-size:13.5px}
.pm-open{text-decoration:none;color:var(--mut)}.pm-open:hover{color:var(--acc)}
/* a point with no role keeps its pill hidden until the line is hovered, so a role can still be typed */
.pm-leaves li .pm-role:empty,.pm-sub li .pm-role:empty{visibility:hidden}.pm-leaves li:hover>.pm-role:empty,.pm-sub li:hover>.pm-role:empty,.pm-role:empty:focus{visibility:visible}
</style>"""
EXTRA_JS = """<script>
(function(){if(window.__pmMore)return;window.__pmMore=1;
 window.pmOpen=window.pmOpen||new Set();
 function draw(){if(window.pmDraw)window.pmDraw();}
 /* ▸: a point's detail opens below it; an empty one (on an editable map) opens straight into its editor */
 document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.pm .pm-more');if(!b)return;
  e.preventDefault();e.stopPropagation();var li=b.closest('li'),d=li.querySelector(':scope>.pm-detail'),on=d.hidden;
  d.hidden=!on;b.setAttribute('aria-expanded',String(on));if(on)window.pmOpen.add(li.dataset.s);else window.pmOpen.delete(li.dataset.s);
  if(on&&b.dataset.empty){var pen=d.querySelector('.pm-pen');if(pen)pen.click();}draw();});
 /* after the map reloads (an edit), the details that were open open again */
 new MutationObserver(function(){document.querySelectorAll('.pm-edit li[data-s]').forEach(function(li){
  if(!window.pmOpen.has(li.dataset.s))return;var d=li.querySelector(':scope>.pm-detail'),b=li.querySelector('.pm-more');
  if(d&&d.hidden){d.hidden=false;if(b)b.setAttribute('aria-expanded','true');draw();}});})
  .observe(document.body,{childList:true,subtree:true});
 /* ✎: the detail as its Markdown, in a box; leaving the box saves it */
 document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.pm-edit .pm-pen');if(!b)return;e.preventDefault();
  var d=b.closest('.pm-detail'),t=document.createElement('textarea');t.value=b.dataset.raw;t.dataset.raw=b.dataset.raw;t.className='pm-notebox';
  d.innerHTML='';d.appendChild(t);t.focus();draw();});
 document.addEventListener('focusout',function(e){var t=e.target.closest&&e.target.closest('.pm-edit .pm-notebox');if(!t)return;
  var h=t.closest('.pm-edit'),li=t.closest('li'),v=t.value.replace(/\s+$/,'');
  function again(){fetch(location.href,{credentials:'same-origin'}).then(function(r){return r.text();}).then(function(x){
   var n=new DOMParser().parseFromString(x,'text/html').querySelector('.pm-edit[data-task="'+h.dataset.task+'"]');
   if(n)h.innerHTML=n.innerHTML;draw();});}
  if(v===t.dataset.raw){again();return;}
  fetch(h.dataset.endpoint||'/_board/draft-plan',{method:'POST',headers:{'Content-Type':'application/json'},
   body:JSON.stringify({what:'note',s:li.dataset.s,was:t.dataset.raw,value:v,task:h.dataset.task,file:h.dataset.file})})
   .then(function(r){return r.json();}).then(function(j){if(!j.ok)throw new Error(j.err);again();})
   .catch(function(err){t.style.outline='1.5px dashed #e03131';t.title='not saved: '+err.message;});});
})();
</script>"""
