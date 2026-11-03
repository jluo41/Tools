"""The question canvas (JL 261102: "how to make the questions to be a canvas, to show their relationships?"):
an analysis plan's questions drawn as cards, one band per DIKW level, Executive at the top and Data at the bottom,
with an arrow from each question to the ones whose answers it cites (its evidence plan, `needs: Ek: from: D01.E8`).

Interactive in the page, nothing written: hover a card to light up what it rests on (below) and what rests on it
(above); click to pin it and read it in the side panel, whose chips walk the links; "Only linked" hides questions
with no link; the search box finds a question by id or words. Plain SVG and a little JavaScript, no package.
"""
import json
import re
from html import escape as esc
from pathlib import Path

from live import insight_plan_c as P

LEVELS = (("X", "Executive"), ("W", "Wisdom"), ("K", "Knowledge"), ("I", "Information"), ("D", "Data"))
WRITTEN = ("written", "answered", "checked")


def _links(q: dict) -> list:
    """The questions this one cites, from its evidence plan's `from:` (D01.E8, or a list of them)."""
    face = P.front(q["file"]) if q.get("file") else {}
    out = []
    for need in (face.get("needs") or {}).values():
        src = need.get("from") if isinstance(need, dict) else None
        for x in (src if isinstance(src, list) else [src]):
            m = re.match(r"([DIKWX]\d+)\.", str(x or ""))
            if m and m.group(1) != q["id"] and m.group(1) not in out:
                out.append(m.group(1))
    return out, face


REFUSED = ("refused", "failed", "error", "thin")


def _gaps(qid: str, face: dict, t: dict | None, cites: list) -> list:
    """Up to three follow-up questions, from what this question's own record lacks: a refused or failed cut, a cut it
    asks with no Run, a claim with no evidence named, and always what would change its answer. Work only."""
    out = []
    hard = (t or {}).get("hard", [])
    for r in hard:
        if str(r.get("status") or "").lower() in REFUSED:
            out.append(f"Why was the {r.get('partition')} cut refused for {qid}, and which cut could answer it instead?")
    asked = (face.get("partitions") or {}).get("asked") if isinstance(face.get("partitions"), dict) else None
    ran = {str(r.get("partition")) for r in hard}
    if t and hard and isinstance(asked, list):        # only a question that runs (X and W are written from pages)
        out += [f"Answer {qid} on the {c} cut too: it is asked there but has no Run yet" for c in asked if str(c) not in ran]
    if qid[:1] in "KWX" and not cites:
        out.append(f"Which Data or Information answers should {qid} rest on? Its evidence plan names none")
    out.append(f"What would change the answer to {qid}, and how would we see it in the next data freeze?")
    return out[:3]


def data(release: dict, job: dict | None, task_href, root: Path | None = None, proposals=()) -> dict:
    """{nodes: [{id, lv, name, q, ask, answer, state, href, task, gaps}], edges: [[from, to]]}: from = the citing
    question. `proposals` (Work only): the Prototype's open proposals, drawn as dashed "asked" cards."""
    tasks = {t["qid"]: t for t in (job or {}).get("tasks", [])}
    nodes, edges = [], []
    for qid, q in release.get("questions", {}).items():
        cites, face = _links(q)
        t = tasks.get(qid)
        tf = (t or {}).get("face", {})
        state = str(tf.get("answer-status") or ("not in a Job" if not t else "—")).lower()
        if face.get("retired"):
            state = "retired"
        task = ""
        if t and root:
            try:
                task = str(Path(t["path"]).resolve().relative_to(Path(root).resolve()))
            except ValueError:
                task = Path(t["path"]).name
        nodes.append({"id": qid, "lv": qid[:1], "name": str(face.get("name") or ""), "q": str(q.get("question") or ""),
                      "ask": str(face.get("ask") or ""), "answer": str(tf.get("answer") or ""), "state": state,
                      "href": task_href(t) if t else "", "task": task, "gaps": _gaps(qid, face, t, cites)})
        edges += [[qid, c] for c in cites if c in release.get("questions", {})]
    for k, pr in enumerate(proposals):
        src = str(pr.get("from") or pr.get("question") or "")
        m = re.match(r"([DIKWX]\d+)", src)
        lv = str(pr.get("level") or "")[:1].upper() or (m.group(1)[0] if m else "X")
        pid = f"P{k + 1:02d}"
        nodes.append({"id": pid, "lv": lv if lv in "XDIKW" else "X", "name": str(pr.get("title") or ""),
                      "q": str(pr.get("question") or pr.get("title") or ""), "ask": "", "answer": "", "state": "asked",
                      "href": "", "task": "", "gaps": []})
        if m and m.group(1) in release.get("questions", {}):
            edges.append([pid, m.group(1)])
    return {"nodes": nodes, "edges": edges, "levels": LEVELS}


CSS = """
.qc{position:relative;display:flex;flex-direction:column;gap:10px;margin:6px 0 4px}
.qc-bar{display:flex;gap:10px;align-items:center;font-size:13px;flex-wrap:wrap}
.qc-bar input[type=search]{padding:4px 8px;border:1px solid #c9ccd1;border-radius:6px;width:220px;font:inherit}
.qc-key{display:inline-flex;gap:10px;color:#57606a}.qc-key i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:4px;vertical-align:-1px}
.qc-svg{width:100%;border:1px solid #d0d7de;border-radius:10px;background:#fbfbfa}
.qc-svg .band{fill:#f2f1ee}.qc-svg .bandx{fill:#eef3fb}.qc-svg path.flow{fill:none;stroke:#8a8f98;stroke-width:2}.qc-svg .bandt{font:600 12px system-ui;fill:#8a8f98;letter-spacing:.04em}
.qc-svg .card rect{fill:#fff;stroke:#1e1e1e;stroke-width:1.2;rx:7}
.qc-svg .card text{font:12px system-ui;fill:#1e1e1e;pointer-events:none}.qc-svg .card .qid{font-weight:700}
.qc-svg .card{cursor:pointer}.qc-svg .card rect,.qc-svg .card text{transition:fill .12s,stroke .12s}
.qc-svg .card.s-written rect,.qc-svg .card.s-answered rect,.qc-svg .card.s-checked rect{fill:#e9f6ec}
.qc-svg .card.s-drafted rect{fill:#fff6db}.qc-svg .card.s-retired rect{fill:#eee;stroke-dasharray:4 3}
.qc-svg .card.s-retired text{fill:#8a8f98}
.qc-svg path.e{fill:none;stroke:#9aa1ab;stroke-width:1;opacity:.35;transition:opacity .12s}
/* lit: the rest fades but stays opaque, so a lit line passes behind a card, never through its words */
.qc-svg.lit .card:not(.on):not(.up):not(.down) rect{fill:#fff;stroke:#e1e4e8}
.qc-svg.lit .card:not(.on):not(.up):not(.down) text{fill:#c3c8ce}.qc-svg.lit path.e{opacity:.04}
.qc-svg .card.on rect{stroke-width:2.6;stroke:#1f6feb}
.qc-svg .card.down rect{stroke:#1a7f37;stroke-width:2}.qc-svg .card.up rect{stroke:#bc4c00;stroke-width:2}
.qc-svg.lit path.e.down{opacity:1;stroke:#1a7f37;stroke-width:1.8}.qc-svg.lit path.e.up{opacity:1;stroke:#bc4c00;stroke-width:1.8}
.qc-side{border:1px solid #d0d7de;border-radius:10px;padding:10px 12px;font-size:13px;background:#fff;min-height:92px;position:sticky;top:0;z-index:2}
.qc-ans{margin:6px 0;padding:6px 8px;border-left:3px solid #1a7f37;background:#f3faf4}.qc-act{margin-top:10px;border-top:1px solid #e1e4e8;padding-top:8px;display:flex;flex-direction:column;gap:6px}.qc-act .pb-prompt{display:flex;gap:6px;align-items:flex-start;border:0;padding:0;margin:0;background:none;box-shadow:none}.qc-side:has(.qc-act){position:static}.qc-act textarea{flex:1;font:inherit;padding:4px 6px;border:1px solid #c9ccd1;border-radius:6px}.qc-gaps{margin:0;padding-left:0;list-style:none}.qc-gaps li{margin:3px 0;display:flex;gap:6px;align-items:baseline}.qc-svg .card.s-asked rect{fill:#fff;stroke-dasharray:5 3}.qc-side .chips a{color:#1864ab}.qc-two{display:grid;grid-template-columns:1.4fr 1fr;gap:14px}.qc-side .chips+b{display:block}.qc-side h4{margin:0 0 4px;font-size:15px}.qc-side .mut{color:#57606a}
.qc-tip{position:absolute;z-index:5;pointer-events:none;max-width:340px;background:#fff;border:1px solid #d0d7de;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,.12);padding:7px 10px;font-size:12.5px;line-height:1.4;display:none}
.qc-tip b{font-size:13px}.qc-tip .mut{color:#57606a}
.qc-side .chips{display:flex;flex-wrap:wrap;gap:4px;margin:4px 0 8px}
.qc-side .chips a{border:1px solid #c9ccd1;border-radius:10px;padding:1px 7px;cursor:pointer;text-decoration:none;color:inherit}
.qc-side .chips a.down{border-color:#1a7f37}.qc-side .chips a.up{border-color:#bc4c00}
@media(max-width:600px){.qc-two{grid-template-columns:1fr}.qc-bar input[type=search]{width:100%}}   /* phone last (haipipe-ui rule 5) */
"""

JS = r"""
(function(){
var root=document.currentScript.previousElementSibling, D=JSON.parse(root.querySelector('script[type="application/json"]').textContent);
var svg=root.querySelector('svg'), side=root.querySelector('.qc-side'), NS='http://www.w3.org/2000/svg';
var W=900, CW=142, CH2=30, GX=10, GX2=26, GY=6, TOP=8;
var by={}, down={}, up={}; D.nodes.forEach(function(n){by[n.id]=n;down[n.id]=[];up[n.id]=[];});
D.edges.forEach(function(e){down[e[0]].push(e[1]);up[e[1]].push(e[0]);});
var onlyLinked=false, pinned=null, pos={}, hov=0, tipEl=document.createElement('div');tipEl.className='qc-tip';root.appendChild(tipEl);
function el(t,a,p){var x=document.createElementNS(NS,t);for(var k in a)x.setAttribute(k,a[k]);if(p)p.appendChild(x);return x;}
function linked(n){return down[n.id].length||up[n.id].length;}
function short(s,k){return s.length>k?s.slice(0,k-1)+'…':s;}
function draw(){
  // Executive on top, as a row; under it the evidence builds left to right, D → I → K → W, one column a level
  // (JL 261102: "should we start from the Executive, and the Data, and then I, K, W").
  svg.innerHTML='';pos={};
  var bandg=el('g',{},svg), eg=el('g',{},svg), cg=el('g',{},svg);
  var cols=['D','I','K','W'], names={};D.levels.forEach(function(L){names[L[0]]=L[1];});
  function keep(lv){return D.nodes.filter(function(n){return n.lv===lv&&(!onlyLinked||linked(n));});}
  var colW=(W-16-3*GX2)/4, cw=colW-20, ch=CH2;
  // the Executive row
  var xs=keep('X'), per=Math.max(1,Math.floor((W-24+GX)/(cw+GX))), xr=Math.ceil(xs.length/per)||0, y=TOP;
  if(xs.length){var h=26+xr*(ch+GY)+4;el('rect',{x:4,y:y,width:W-8,height:h,rx:10,'class':'band bandx'},bandg);
    var t=el('text',{x:16,y:y+18,'class':'bandt'},bandg);t.textContent='EXECUTIVE · '+xs.length+' · what a leader reads first';
    xs.forEach(function(n,i){card(n,14+(i%per)*(cw+GX),y+26+Math.floor(i/per)*(ch+GY),cw,ch);});
    y+=h+22;}
  var colTop=y, bottom=y;
  cols.forEach(function(lv,c){var ns=keep(lv), x=8+c*(colW+GX2);
    // order a column by where its links point on the column before, so lines cross less
    ns.sort(function(a,b){function k(n){var ys=down[n.id].concat(up[n.id]).filter(function(i){return pos[i];}).map(function(i){return pos[i].y;});
      return ys.length?ys.reduce(function(s,v){return s+v;},0)/ys.length:1e5+parseInt(n.id.slice(1));}return k(a)-k(b);});
    var h=28+ns.length*(ch+GY)+4;
    el('rect',{x:x,y:colTop,width:colW,height:Math.max(h,60),rx:10,'class':'band'},bandg);
    var t=el('text',{x:x+10,y:colTop+18,'class':'bandt'},bandg);t.textContent=(names[lv]||lv).toUpperCase()+' · '+ns.length;
    ns.forEach(function(n,i){card(n,x+10,colTop+28+i*(ch+GY),cw,ch);});
    bottom=Math.max(bottom,colTop+Math.max(h,60));
    if(c<3){var ax=x+colW+GX2/2;el('path',{d:'M'+(ax-7)+','+(colTop+12)+' l7,6 l-7,6','class':'flow'},bandg);}
  });
  D.edges.forEach(function(e){var a=pos[e[0]],b=pos[e[1]];if(!a||!b)return;var d;
    if(a.lv==='X'){var x1=a.x+a.w/2,y1=a.y+a.h,x2=b.x+b.w/2,y2=b.y,m=(y1+y2)/2;d='M'+x1+','+y1+' C'+x1+','+m+' '+x2+','+m+' '+x2+','+y2;}
    else if(a.lv===b.lv){var rx=a.x+a.w,y1=a.y+a.h/2,y2=b.y+b.h/2;d='M'+rx+','+y1+' C'+(rx+26)+','+y1+' '+(rx+26)+','+y2+' '+rx+','+y2;}
    else{var L=b.x<a.x?b:a,R=b.x<a.x?a:b,x1=L.x+L.w,y1=L.y+L.h/2,x2=R.x,y2=R.y+R.h/2,mx=(x1+x2)/2;
      d='M'+x1+','+y1+' C'+mx+','+y1+' '+mx+','+y2+' '+x2+','+y2;}
    el('path',{d:d,'class':'e','data-a':e[0],'data-b':e[1]},eg);});
  svg.setAttribute('viewBox','0 0 '+W+' '+(bottom+8));svg.style.height='auto';
  if(!(pinned&&pos[pinned]))pinned=null;light(pinned);panel(pinned);
}
function card(n,x,y,w,h){pos[n.id]={x:x,y:y,w:w,h:h,lv:n.lv};
  var g=el('g',{'class':'card s-'+n.state.replace(/\s+/g,'-'),'data-id':n.id,transform:'translate('+x+','+y+')'},svg.lastChild);
  el('rect',{width:w,height:h,rx:7},g);
  var a=el('text',{x:8,y:h/2+4,'class':'qid'},g);a.textContent=n.id;
  var b=el('text',{x:40,y:h/2+4},g);b.textContent=short(n.name||n.q,Math.floor((w-48)/6.6));
  var tt=el('title',{},g);tt.textContent=n.id+' · '+n.q+'\n'+n.state;
  // hover lights the chain and shows a small tip; the panel above changes only on a click, so the canvas never
  // jumps under the mouse; a short delay keeps the light steady while the mouse crosses the gap to the next card
  g.addEventListener('mouseenter',function(){clearTimeout(hov);light(n.id);tip(n,g);});
  g.addEventListener('mouseleave',function(){clearTimeout(hov);hov=setTimeout(function(){light(pinned);tip(null);},90);});
  g.addEventListener('click',function(){pin(pinned===n.id?null:n.id);});
}
function reach(id,map){var seen={},st=[id];while(st.length){var k=st.pop();map[k].forEach(function(j){if(!seen[j]){seen[j]=1;st.push(j);}});}return seen;}
function light(id){
  svg.classList.toggle('lit',!!id);
  var dn=id?reach(id,down):{}, upp=id?reach(id,up):{};
  svg.querySelectorAll('.card').forEach(function(g){var k=g.dataset.id;g.classList.toggle('on',k===id);g.classList.toggle('down',!!dn[k]);g.classList.toggle('up',!!upp[k]);});
  svg.querySelectorAll('path.e').forEach(function(p){var a=p.dataset.a,b=p.dataset.b;
    p.classList.toggle('down',!!(id&&(a===id||dn[a])&&dn[b]));p.classList.toggle('up',!!(id&&(b===id||upp[b])&&upp[a]));});
}
function tip(n,g){if(!n){tipEl.style.display='none';return;}
  var a=n.answer||n.ask||n.q;a=a.split(/(?<=[.!?])\s/)[0];
  tipEl.innerHTML='<b>'+esc(n.id)+' · '+esc(n.name||'')+'</b><br>'+esc(short(a,180))
    +'<br><span class=mut>'+esc(n.state)+' · rests on '+down[n.id].length+' · used by '+up[n.id].length+(pinned===n.id?'':' · click to pin')+'</span>';
  tipEl.style.display='block';
  var R=root.getBoundingClientRect(), c=g.getBoundingClientRect(), tw=tipEl.offsetWidth, x=c.left-R.left, y=c.bottom-R.top+6;
  if(x+tw>R.width)x=Math.max(0,R.width-tw);
  if(c.bottom+tipEl.offsetHeight+8>window.innerHeight)y=c.top-R.top-tipEl.offsetHeight-6;
  tipEl.style.left=x+'px';tipEl.style.top=y+'px';}
function chips(ids,cls){return ids.length?'<div class=chips>'+ids.map(function(i){return '<a class='+cls+' data-go="'+i+'" title="'+esc(by[i].q)+'">'+i+'</a>';}).join('')+'</div>':'<p class=mut>none</p>';}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function panel(id){
  if(!id){side.innerHTML='<h4>Click a question to read it here</h4><p class=mut>Hover lights its chain. Green: what it rests on, all the way down. Orange: what uses it. Click to pin; click the chips to walk.'
    +(D.work?' Pinned, a question can be asked about or followed up.':'')+'</p><p class=mut>'+D.nodes.length+' questions · '+D.edges.length+' links</p>';return;}
  var n=by[id];
  side.innerHTML='<div class=qc-two><div><h4>'+esc(n.id)+' · '+esc(n.name)+'</h4><p style="margin:2px 0">'+esc(n.q)+'</p>'
    +(n.answer?'<p class=qc-ans>'+esc(n.answer)+'</p>':(n.ask?'<p class=mut style="margin:2px 0">'+esc(n.ask)+'</p>':''))
    +'<p class=mut style="margin:2px 0">page: <b>'+esc(n.state)+'</b>'
    +(n.href?' · <a href="'+esc(n.href)+'">open its Task ↗</a>':'')+'</p></div><div><b>Rests on</b>'+chips(down[id],'down')
    +'<b>Used by</b>'+chips(up[id],'up')+'</div></div>'+(D.work?act(n):'');
  side.querySelectorAll('[data-go]').forEach(function(a){a.addEventListener('click',function(){pin(a.dataset.go,true);});});
}
function ids(a){return a.length?a.join(', '):'none';}
function act(n){  // Work only: ask about it, or propose a follow-up for the next plan; copies a prompt, writes nothing
  var w=D.work, where='the insight Board '+w.board+(w.job?', Job '+w.job:'');
  var ask='On '+where+': a question about '+n.id+' ('+n.q+').'+(n.answer?' Its answer now: '+n.answer:'')
    +' It rests on '+ids(down[n.id])+' and is used by '+ids(up[n.id])+'.'+(n.task?' Read its Task '+n.task+' and its Runs\' results first, then answer from them; say what they cannot tell.':'');
  var prop=function(t){return 'Propose a follow-up to '+n.id+' ('+n.q+') for the next analysis plan: write it as a proposal in '
    +w.proposals+' (haipipe-insight-question), with from: '+n.id+' and the level it asks at. The follow-up: '+t;};
  var h='<div class=qc-act><span class="pb-prompt qc-askbox"><textarea data-field="My question" rows=2 placeholder="Ask about '+esc(n.id)+' …"></textarea>'
    +'<button type=button class="fd-btn pb-copy" data-copy="'+esc(ask)+'" data-tail="'+esc(w.tail)+'">Ask about it</button></span>';
  if(n.gaps&&n.gaps.length){h+='<b>Follow up</b><ul class=qc-gaps>'+n.gaps.map(function(g){return '<li><span class=pb-prompt>'
    +'<button type=button class="fd-btn pb-copy" data-copy="'+esc(prop(g))+'" data-tail="'+esc(w.tail)+'">Propose</button></span> '+esc(g)+'</li>';}).join('')+'</ul>';}
  h+='<span class=pb-prompt><textarea data-field="The follow-up" rows=1 placeholder="or your own follow-up …"></textarea>'
    +'<button type=button class="fd-btn pb-copy" data-copy="'+esc(prop(''))+'" data-tail="'+esc(w.tail)+'">Propose mine</button></span></div>';
  return h;
}
function pin(id,go){pinned=id;if(id&&!pos[id]){onlyLinked=false;root.querySelector('.qc-only').checked=false;draw();}light(id);panel(id);tip(null);
  try{history.replaceState(null,'',location.pathname+location.search+(id?'#q='+id:''));}catch(e){}   // the share link follows the pin
  if(id&&go){var c=svg.querySelector('.card[data-id="'+id+'"]');if(c)c.scrollIntoView({block:'nearest',behavior:'smooth'});}}
root.querySelector('.qc-only').addEventListener('change',function(e){onlyLinked=e.target.checked;draw();});
root.querySelector('.qc-find').addEventListener('input',function(e){var s=e.target.value.trim().toLowerCase();if(!s){pin(null);return;}
  var hit=D.nodes.find(function(n){return n.id.toLowerCase()===s;})||D.nodes.find(function(n){return (n.id+' '+n.name+' '+n.q).toLowerCase().indexOf(s)>=0;});if(hit)pin(hit.id,true);});
function fit(){var w=svg.getBoundingClientRect().width||900;W=Math.max(520,Math.round(w));draw();}
window.addEventListener('resize',function(){clearTimeout(fit.t);fit.t=setTimeout(fit,150);});fit();
var h=(location.hash.match(/q=([DIKWX]\d+)/)||[])[1];if(h&&by[h])pin(h);
})();
"""


def canvas(release: dict, job: dict | None, task_href, root: Path | None = None, work: dict | None = None,
           proposals=()) -> str:
    """Report (work=None): read and explore. Work (work={board, job, proposals, tail}): the same canvas, and a pinned
    question's panel can be asked about or followed up (JL 261102: "the questions should be in the Work")."""
    d = data(release, job, task_href, root, proposals if work else ())
    if not d["nodes"]:
        return ""
    d["work"] = work
    blob = json.dumps(d).replace("</", "<\\/")
    key = ('<span class=qc-key><span><i style="background:#e9f6ec;border:1px solid #1e1e1e"></i>page written</span>'
           '<span><i style="background:#fff6db;border:1px solid #1e1e1e"></i>drafted</span>'
           '<span><i style="background:#fff;border:1px solid #1e1e1e"></i>not yet</span>'
           + ('<span><i style="background:#fff;border:1px dashed #1e1e1e"></i>asked, not planned</span>' if work else "")
           + '</span>')
    return (f'<style>{CSS}</style><div class=qc><div class=qc-bar><input class=qc-find type=search placeholder="find X03, timing …">'
            f'<label><input class=qc-only type=checkbox> Only linked</label>{key}</div>'
            f'<aside class=qc-side></aside><svg class=qc-svg></svg>'
            f'<script type="application/json">{blob}</script></div><script>{JS}</script>')
