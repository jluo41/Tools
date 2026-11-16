"""The question canvas (cards and lines show which question rests on which):
a question version's questions drawn as cards, one band per DIKW level, Executive at the top and Data at the bottom,
with an arrow from each question to the ones whose answers it cites (its evidence plan, `needs: Ek: from: D01.E8`).

Interactive in the page, nothing written: hover a card to light up what it rests on (below) and what rests on it
(above); click to pin it and read it in the side panel, whose chips walk the links; "Only linked" hides questions
with no link; the search box finds a question by id or words. Plain SVG and a little JavaScript, no package.
"""
import html
import json
import re
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


def _segs(face: dict, segments: list) -> list:
    """The segments a question is asked on, in the version's own order: its `partitions.asked` (all, one name or a
    list), and `cross` when one of its needs is cut across segments."""
    asked = (face.get("partitions") or {}).get("asked") if isinstance(face.get("partitions"), dict) else None
    names = set(segments) if asked == "all" else {str(x) for x in (asked if isinstance(asked, list) else [asked] if asked else [])}
    if any(isinstance(n, dict) and n.get("cut") == "cross" for n in (face.get("needs") or {}).values()):
        names.add("cross")
    return [x for x in segments if x in names]


REFUSED = ("refused", "failed", "error", "thin")


def _gaps(qid: str, face: dict, t: dict | None, cites: list) -> list:
    """Up to three follow-up questions, from what this question's own record lacks: a refused or failed segment, a segment it
    asks with no Run, a claim with no evidence named, and always what would change its answer. Work only."""
    out = []
    hard = (t or {}).get("hard", [])
    for r in hard:
        if str(r.get("status") or "").lower() in REFUSED:
            out.append(f"Why was the {r.get('partition')} segment refused for {qid}, and which segment could answer it instead?")
    asked = (face.get("partitions") or {}).get("asked") if isinstance(face.get("partitions"), dict) else None
    ran = {str(r.get("partition")) for r in hard}
    if t and hard and isinstance(asked, list):        # only a question that runs (X and W are written from pages)
        out += [f"Answer {qid} on the {c} segment too: it is asked there but has no Run yet" for c in asked if str(c) not in ran]
    if qid[:1] in "KWX" and not cites:
        out.append(f"Which Data or Information answers should {qid} rest on? Its evidence plan names none")
    out.append(f"What would change the answer to {qid}, and how would we see it in the next data version?")
    return out[:3]


def data(release: dict, job: dict | None, task_href, root: Path | None = None, proposals=(), mode: str = "board") -> dict:
    """{nodes: [{id, lv, name, q, ask, answer, state, href, task, gaps}], edges: [[from, to]]}: from = the citing
    question. `proposals` (Work only): the Question Book's open proposals, drawn as dashed "asked" cards."""
    tasks = {t["qid"]: t for t in (job or {}).get("tasks", [])}
    nodes, edges = [], []
    segments = [str(p.get("name") or "") for p in (release.get("partitions") or []) if p.get("name")]
    for qid, q in release.get("questions", {}).items():
        cites, face = _links(q)
        t = tasks.get(qid)
        tf = (t or {}).get("face", {})
        state = str(tf.get("answer-status") or ("not in a Job" if not t else "—")).lower()
        if mode == "code":                                         # a Code Board: what this version did to it
            state = "new" if str(q.get("change") or "") == "new" else (
                "changed" if str(q.get("change") or "") == "changed" else "kept")
        if face.get("retired"):
            state = "retired"
        elif str(tf.get("check") or "").startswith("↩"):          # a returned page is not written (the one count)
            state = "returned"
        task = ""
        if t and root:
            try:
                task = str(Path(t["path"]).resolve().relative_to(Path(root).resolve()))
            except ValueError:
                task = Path(t["path"]).name
        nodes.append({"id": qid, "lv": qid[:1], "name": str(face.get("name") or ""), "q": str(q.get("question") or ""),
                      "ask": str(face.get("ask") or ""), "answer": str(tf.get("answer") or ""), "state": state,
                      "href": task_href(t) if t else (task_href({"path": q["task"]}) if mode == "code" and q.get("task") else ""), "task": task, "gaps": _gaps(qid, face, t, cites),
                      "segs": _segs(face, segments)})
        edges += [[qid, c] for c in cites if c in release.get("questions", {})]
    for k, pr in enumerate(proposals):
        src = str(pr.get("from") or pr.get("question") or "")
        m = re.match(r"([DIKWX]\d+)", src)
        lv = str(pr.get("level") or "")[:1].upper() or (m.group(1)[0] if m else "X")
        pid = f"P{k + 1:02d}"
        nodes.append({"id": pid, "lv": lv if lv in "XDIKW" else "X", "name": str(pr.get("title") or ""),
                      "q": str(pr.get("question") or pr.get("title") or ""), "ask": "", "answer": "", "state": "asked",
                      "href": "", "task": "", "gaps": [], "segs": []})
        if m and m.group(1) in release.get("questions", {}):
            edges.append([pid, m.group(1)])
    used = {x for n in nodes for x in n["segs"]}
    return {"nodes": nodes, "edges": edges, "levels": LEVELS, "mode": mode, "segments": [x for x in segments if x in used]}


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
.qc-svg .card.s-drafted rect,.qc-svg .card.s-returned rect{fill:#fff6db}.qc-svg .card.s-retired rect{fill:#eee;stroke-dasharray:4 3}
.qc-svg .card.s-retired text{fill:#8a8f98}
.qc-svg path.e{fill:none;stroke:#9aa1ab;stroke-width:1;opacity:.35;transition:opacity .12s}
/* lit: the rest fades but stays opaque, so a lit line passes behind a card, never through its words */
.qc-svg.lit .card:not(.on):not(.up):not(.down) rect{fill:#fff;stroke:#e1e4e8}
.qc-svg.lit .card:not(.on):not(.up):not(.down) text{fill:#c3c8ce}.qc-svg.lit path.e{opacity:.04}
.qc-svg .card.on rect{stroke-width:2.6;stroke:#1f6feb}
.qc-svg .card.down rect{stroke:#1a7f37;stroke-width:2}.qc-svg .card.up rect{stroke:#bc4c00;stroke-width:2}
.qc-svg.lit path.e.down{opacity:1;stroke:#1a7f37;stroke-width:1.8}.qc-svg.lit path.e.up{opacity:1;stroke:#bc4c00;stroke-width:1.8}
.qc-side{position:fixed;bottom:14px;z-index:5;box-sizing:border-box;max-height:46vh;overflow:auto;border:1px solid #1f6feb;border-radius:10px;padding:10px 12px;font-size:13px;background:#fff;box-shadow:0 10px 28px rgba(0,0,0,.22)}.qc-side h4{margin:0 26px 2px 0}.qc-x{position:absolute;top:6px;right:8px;border:0;background:none;font-size:15px;line-height:1;cursor:pointer;color:#57606a;padding:4px}.qc-side[hidden],.qc-side.away{display:none}
.qc-ans{margin:6px 0;padding:6px 8px;border-left:3px solid #1a7f37;background:#f3faf4}.qc-act{margin-top:10px;border-top:1px solid #e1e4e8;padding-top:8px;display:flex;flex-direction:column;gap:6px}.qc-act .pb-prompt{display:flex;gap:6px;align-items:flex-start;border:0;padding:0;margin:0;background:none;box-shadow:none}.qc-side:has(.qc-act){position:static}.qc-act textarea{flex:1;font:inherit;padding:4px 6px;border:1px solid #c9ccd1;border-radius:6px}.qc-gaps{margin:0;padding-left:0;list-style:none}.qc-gaps li{margin:3px 0;display:flex;gap:6px;align-items:baseline}.qc-svg .card.s-asked rect{fill:#fff;stroke-dasharray:5 3}.qc-side .chips a{color:#1864ab}.qc-two{display:grid;grid-template-columns:1.4fr 1fr;gap:14px}.qc-side .chips+b{display:block}.qc-side h4{margin:0 0 4px;font-size:15px}.qc-side .mut{color:#57606a}
.qc-tip{position:absolute;z-index:6;pointer-events:none;max-width:320px;background:#fff;border:1px solid #1f6feb;border-radius:8px;box-shadow:0 10px 28px rgba(0,0,0,.22);padding:7px 10px;font-size:12.5px;line-height:1.4;display:none}
.qc-tip b{font-size:13px}.qc-tip .mut{color:#57606a}
.qc-side .chips{display:flex;flex-wrap:wrap;gap:4px;margin:4px 0 8px}
.qc-side .chips a{border:1px solid #c9ccd1;border-radius:10px;padding:1px 7px;cursor:pointer;text-decoration:none;color:inherit}
.qc-side .chips a.down{border-color:#1a7f37}.qc-side .chips a.up{border-color:#bc4c00}
.qc-style{display:inline-flex;border:1px solid #c9ccd1;border-radius:6px;overflow:hidden}
.qc-style button{border:0;background:#fff;padding:3px 10px;font:inherit;cursor:pointer;color:#57606a}.qc-style button.on{background:#eaf2fe;color:#1f6feb}
.qc-svg .card circle{fill:#fff;stroke:#1e1e1e;stroke-width:1.4;transition:fill .12s,stroke .12s}
.qc-svg .card .nid{font:700 11px system-ui;text-anchor:middle}.qc-svg .card .nname{font:11px system-ui;fill:#57606a;text-anchor:middle}
.qc-svg .colt{font:600 12px system-ui;fill:#8a8f98;letter-spacing:.04em;text-anchor:middle}
.qc-svg .card.s-written circle,.qc-svg .card.s-answered circle,.qc-svg .card.s-checked circle{fill:#d3f0da}
.qc-svg .card.s-drafted circle,.qc-svg .card.s-returned circle{fill:#fff1c2}.qc-svg .card.s-new circle{fill:#dbe9ff}
.qc-svg .card.s-changed circle{fill:#fff1c2}.qc-svg .card.s-new rect{fill:#dbe9ff}.qc-svg .card.s-changed rect{fill:#fff1c2}.qc-svg .card.s-retired circle,.qc-svg .card.s-asked circle{stroke-dasharray:4 3}
.qc-svg.net path.e{opacity:.55;stroke:#9aa1ab;stroke-width:1.3}
.qc-svg.net path.e.ex:not(.down):not(.up){opacity:0}
.qc-svg.lit .card:not(.on):not(.up):not(.down) circle{fill:#fff;stroke:#e1e4e8}
.qc-svg .card.on circle{stroke-width:3;stroke:#1f6feb}.qc-svg .card.down circle{stroke:#1a7f37;stroke-width:2.4}.qc-svg .card.up circle{stroke:#bc4c00;stroke-width:2.4}
.qc-seg{padding:3px 6px;border:1px solid #c9ccd1;border-radius:6px;font:inherit;background:#fff}
/* a picked segment: the questions asked on it stay, the rest fade (as lit does) */
.qc-svg.seg .card:not(.inseg):not(.on) rect,.qc-svg.seg .card:not(.inseg):not(.on) circle{fill:#fff;stroke:#e1e4e8}
.qc-svg.seg .card:not(.inseg):not(.on) text{fill:#c3c8ce}
.qc-side .chips a.sg{border-style:dashed}.qc-side .chips a.sg.on{background:#eaf2fe;border-color:#1f6feb;border-style:solid}
/* a narrow canvas (a phone): one level at a time as a full-width list, picked by the level tabs; a tap pins */
.qc-lv{display:none;border:1px solid #c9ccd1;border-radius:6px;overflow:hidden;width:100%}
.qc-lv button{flex:1;border:0;border-right:1px solid #e1e4e8;background:#fff;padding:7px 2px;font:600 12px system-ui;color:#57606a;cursor:pointer;position:relative}
.qc-lv button:last-child{border-right:0}.qc-lv button.on{background:#eaf2fe;color:#1f6feb}
.qc-lv button.has:after{content:"";position:absolute;top:4px;right:5px;width:6px;height:6px;border-radius:50%;background:#1a7f37}
.qc.ph .qc-lv{display:flex}.qc.ph .qc-style,.qc.ph .qc-key{display:none}
.qc.ph .qc-svg .card text{font-size:14px}.qc.ph .qc-two{grid-template-columns:1fr}.qc.ph .qc-bar input[type=search]{width:100%}
.qc.ph .qc-side{max-height:52vh}
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
var style='cards', phone=false, level='X', seg='';
function inSeg(n){return !seg||(n.segs||[]).indexOf(seg)>=0;}
function draw(){svg.classList.toggle('net',style==='net'&&!phone);if(phone)return drawList();if(style==='net')return drawNet();drawCards();}
function drawList(){
  // a phone: the map at 390 px would be 5 px words and 13 px cards, so one level shows at a time, full width; the
  // level tabs walk the ladder, and a pinned question's chips jump to the level its links sit on
  svg.innerHTML='';pos={};el('g',{},svg);
  var ns=D.nodes.filter(function(n){return n.lv===level&&(!onlyLinked||linked(n));});
  ns.sort(function(a,b){return parseInt(a.id.slice(1))-parseInt(b.id.slice(1));});
  ns.forEach(function(n,i){card(n,6,6+i*48,W-12,40);});
  svg.setAttribute('viewBox','0 0 '+W+' '+(12+Math.max(ns.length,1)*48));svg.style.height='auto';
  lvEl.querySelectorAll('button').forEach(function(b){b.classList.toggle('on',b.dataset.lv===level);});
  light(pinned);panel(pinned);
}
function drawNet(){
  // the questions as a network: Executive across the top as cards with their titles, in number order (what a reader
  // opens the Book for); under it one column a level, Data on the left to Wisdom on the right, a dot a question, a line
  // from each answer to every question that uses it. An Executive question cites every level, so its lines are drawn
  // only while it, or a question in its chain, is hovered or pinned
  svg.innerHTML='';pos={};
  var eg=el('g',{},svg), cg=el('g',{},svg), cols=['D','I','K','W'], names={};D.levels.forEach(function(L){names[L[0]]=L[1];});
  function keep(lv){return D.nodes.filter(function(n){return n.lv===lv&&(!onlyLinked||linked(n));});}
  function num(a,b){return parseInt(a.id.slice(1))-parseInt(b.id.slice(1));}
  var colW=(W-16)/4, R=16, SP=74, y0=44, most=Math.max.apply(null,cols.map(function(lv){return keep(lv).length;}).concat([1]));
  var xs=keep('X').sort(num), per=Math.max(1,Math.min(xs.length,Math.floor((W-16)/128))), xw=(W-16)/per, XH=30, XS=38;
  if(xs.length){var t0=el('text',{x:W/2,y:16,'class':'colt'},cg);t0.textContent=(names.X||'X').toUpperCase();
    xs.forEach(function(n,i){var k=i%per, inRow=Math.min(per,xs.length-(i-k)), left=8+(W-16-inRow*xw)/2;   // a short last row is centred
      card(n,left+xw*k+4,26+Math.floor(i/per)*XS,xw-8,XH);});
    y0=26+Math.ceil(xs.length/per)*XS+40;}
  cols.forEach(function(lv,c){var ns=keep(lv), cx=8+colW*c+colW/2;
    ns.sort(function(a,b){function k(n){var ys=down[n.id].concat(up[n.id]).filter(function(i){return pos[i]&&pos[i].lv!=='X';}).map(function(i){return pos[i].y;});
      return ys.length?ys.reduce(function(s,v){return s+v;},0)/ys.length:1e5+parseInt(n.id.slice(1));}return k(a)-k(b);});
    var t=el('text',{x:cx,y:y0-28,'class':'colt'},cg);t.textContent=(names[lv]||lv).toUpperCase();
    var off=y0+R+(most-ns.length)*SP/2;
    ns.forEach(function(n,i){dot(n,cx,off+i*SP,R,colW-8,cg);});});
  D.edges.forEach(function(e){var a=pos[e[0]],b=pos[e[1]];if(!a||!b)return;var d,ay=a.y+R,by_=b.y+R,ex=a.lv==='X'||b.lv==='X';
    if(a.lv==='X'&&b.lv==='X'){var ax=a.x+a.w/2,bx=b.x+b.w/2,lift=a.y===b.y?14:0;   // two Executive questions: an arc over the row
      d='M'+ax+','+a.y+' C'+ax+','+(a.y-lift)+' '+bx+','+(b.y-lift)+' '+bx+','+b.y;}
    else if(ex){var T=a.lv==='X'?a:b,B=a.lv==='X'?b:a,x1=T.x+T.w/2,y1=T.y+T.h,x2=B.x+B.w/2,y2=B.y,m=(y1+y2)/2;   // from under its card, down
      d='M'+x1+','+y1+' C'+x1+','+m+' '+x2+','+m+' '+x2+','+y2;}
    else if(a.lv===b.lv){var rx=a.x+2*R;d='M'+rx+','+ay+' C'+(rx+30)+','+ay+' '+(rx+30)+','+by_+' '+rx+','+by_;}
    else{var L=b.x<a.x?b:a,Rr=b.x<a.x?a:b,x1=L.x+2*R,y1=L.y+R,x2=Rr.x,y2=Rr.y+R,mx=(x1+x2)/2,
      skip=Math.round((x2-x1)/colW), bow=skip>0?skip*16+(y1===y2?10:0):0;   // a line past a level arcs over it,
      d=bow?'M'+x1+','+y1+' C'+(x1+(x2-x1)/3)+','+(y1-bow)+' '+(x2-(x2-x1)/3)+','+(y2-bow)+' '+x2+','+y2   // never through its dots
        :'M'+x1+','+y1+' C'+mx+','+y1+' '+mx+','+y2+' '+x2+','+y2;}
    el('path',{d:d,'class':ex?'e ex':'e','data-a':e[0],'data-b':e[1]},eg);});
  svg.setAttribute('viewBox','0 0 '+W+' '+(y0+most*SP+12));svg.style.height='auto';
  if(!(pinned&&pos[pinned]))pinned=null;light(pinned);panel(pinned);
}
function dot(n,cx,cy,r,w,parent){pos[n.id]={x:cx-r,y:cy-r,w:2*r,h:2*r,lv:n.lv};
  var g=el('g',{'class':'card s-'+n.state.replace(/\s+/g,'-'),'data-id':n.id,transform:'translate('+cx+','+cy+')'},parent);
  el('circle',{r:r},g);
  var a=el('text',{y:4,'class':'nid'},g);a.textContent=n.id;
  var b=el('text',{y:r+14,'class':'nname'},g);b.textContent=short(n.name||n.q,Math.floor(w/6.2));
  g.setAttribute('aria-label',n.id+' · '+n.q);   // no <title>: the browser's grey tooltip would sit on the hover card
  g.addEventListener('mouseenter',function(){clearTimeout(hov);light(n.id);tip(n,g);});
  g.addEventListener('mouseleave',function(){clearTimeout(hov);hov=setTimeout(function(){light(pinned);tip(null);},90);});
  g.addEventListener('click',function(){pin(pinned===n.id?null:n.id);});
}
function drawCards(){
  // Executive on top, as a row; under it the evidence builds left to right, D → I → K → W, one column a level.
  svg.innerHTML='';pos={};
  var bandg=el('g',{},svg), eg=el('g',{},svg), cg=el('g',{},svg);
  var cols=['D','I','K','W'], names={};D.levels.forEach(function(L){names[L[0]]=L[1];});
  function keep(lv){return D.nodes.filter(function(n){return n.lv===lv&&(!onlyLinked||linked(n));});}
  var colW=(W-16-3*GX2)/4, cw=colW-20, ch=CH2;
  // the Executive row
  var xs=keep('X'), per=Math.max(1,Math.floor((W-24+GX)/(cw+GX))), xr=Math.ceil(xs.length/per)||0, y=TOP;
  if(xs.length){var h=26+xr*(ch+GY)+4;el('rect',{x:4,y:y,width:W-8,height:h,rx:10,'class':'band bandx'},bandg);
    var t=el('text',{x:16,y:y+18,'class':'bandt'},bandg);t.textContent='EXECUTIVE';
    xs.forEach(function(n,i){card(n,14+(i%per)*(cw+GX),y+26+Math.floor(i/per)*(ch+GY),cw,ch);});
    y+=h+22;}
  var colTop=y, bottom=y;
  cols.forEach(function(lv,c){var ns=keep(lv), x=8+c*(colW+GX2);
    // order a column by where its links point on the column before, so lines cross less
    ns.sort(function(a,b){function k(n){var ys=down[n.id].concat(up[n.id]).filter(function(i){return pos[i];}).map(function(i){return pos[i].y;});
      return ys.length?ys.reduce(function(s,v){return s+v;},0)/ys.length:1e5+parseInt(n.id.slice(1));}return k(a)-k(b);});
    var h=28+ns.length*(ch+GY)+4;
    el('rect',{x:x,y:colTop,width:colW,height:Math.max(h,60),rx:10,'class':'band'},bandg);
    var t=el('text',{x:x+10,y:colTop+18,'class':'bandt'},bandg);t.textContent=(names[lv]||lv).toUpperCase();
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
  var b=el('text',{x:phone?46:40,y:h/2+4},g);b.textContent=short(n.name||n.q,Math.floor((w-48)/(phone?8.2:6.6)));
  g.setAttribute('aria-label',n.id+' · '+n.q);   // no <title>: the browser's grey tooltip would sit on the hover card
  // hover lights the chain and shows a small tip; the panel above changes only on a click, so the canvas never
  // jumps under the mouse; a short delay keeps the light steady while the mouse crosses the gap to the next card
  g.addEventListener('mouseenter',function(){clearTimeout(hov);light(n.id);tip(n,g);});
  g.addEventListener('mouseleave',function(){clearTimeout(hov);hov=setTimeout(function(){light(pinned);tip(null);},90);});
  g.addEventListener('click',function(){pin(pinned===n.id?null:n.id);});
}
function reach(id,map){var seen={},st=[id];while(st.length){var k=st.pop();map[k].forEach(function(j){if(!seen[j]){seen[j]=1;st.push(j);}});}return seen;}
function light(id){
  svg.classList.toggle('lit',!!id);svg.classList.toggle('seg',!!seg);
  var dn=id?reach(id,down):{}, upp=id?reach(id,up):{};
  svg.querySelectorAll('.card').forEach(function(g){g.classList.toggle('inseg',inSeg(by[g.dataset.id]));});
  lvEl.querySelectorAll('button').forEach(function(b){   // a level tab is dotted when the pinned question's chain passes through it
    b.classList.toggle('has',!!id&&D.nodes.some(function(n){return n.lv===b.dataset.lv&&n.id!==id&&(dn[n.id]||upp[n.id]);}));});
  svg.querySelectorAll('.card').forEach(function(g){var k=g.dataset.id;g.classList.toggle('on',k===id);g.classList.toggle('down',!!dn[k]);g.classList.toggle('up',!!upp[k]);});
  svg.querySelectorAll('path.e').forEach(function(p){var a=p.dataset.a,b=p.dataset.b;
    p.classList.toggle('down',!!(id&&(a===id||dn[a])&&dn[b]));p.classList.toggle('up',!!(id&&(b===id||upp[b])&&upp[a]));});
}
function tip(n,g){if(!n||phone){tipEl.style.display='none';return;}
  var a=n.answer||n.ask||n.q;a=a.split(/(?<=[.!?])\s/)[0];
  tipEl.innerHTML='<b>'+esc(n.id)+' · '+esc(n.name||'')+'</b><br>'+esc(short(a,180));
  tipEl.style.display='block';
  // beside the card (right of it, left when the edge is near), so its own column stays readable; under it only when
  // neither side has room (a narrow screen)
  var R=root.getBoundingClientRect(), c=g.getBoundingClientRect(), tw=tipEl.offsetWidth, th=tipEl.offsetHeight;
  var x=c.right-R.left+10, y=c.top-R.top+(c.height-th)/2;
  if(x+tw>R.width)x=c.left-R.left-tw-10;
  if(x<0){x=Math.max(0,Math.min(c.left-R.left,R.width-tw));y=c.bottom-R.top+8;
    if(c.bottom+th+10>window.innerHeight)y=c.top-R.top-th-8;}
  else{var top=8-R.top, bot=window.innerHeight-8-R.top-th;y=Math.max(Math.min(y,bot),top);}
  tipEl.style.left=x+'px';tipEl.style.top=y+'px';}
function chips(ids,cls){return ids.length?'<div class=chips>'+ids.map(function(i){return '<a class='+cls+' data-go="'+i+'" title="'+esc(by[i].q)+'">'+i+'</a>';}).join('')+'</div>':'<p class=mut>none</p>';}
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function panel(id){
  // nothing pinned, nothing shown: a click pops the panel out at the foot of the window, over the canvas, so the result
  // of a click is in view wherever the card sits; ✕ or a second click on the card lets go. Fixed, not sticky: the
  // fold's body scrolls sideways (overflow), which would hold a sticky panel at the canvas's own foot
  if(!id){side.hidden=true;side.innerHTML='';root.style.paddingBottom='';return;}
  side.hidden=false;place();
  var n=by[id];
  side.innerHTML='<button type=button class=qc-x aria-label="Close">✕</button><div class=qc-two><div><h4>'+esc(n.id)+' · '+esc(n.name)+'</h4><p style="margin:2px 0">'+esc(n.q)+'</p>'
    +(n.answer?'<p class=qc-ans>'+esc(n.answer)+'</p>':(n.ask?'<p class=mut style="margin:2px 0">'+esc(n.ask)+'</p>':''))
    +(n.href?'<p class=mut style="margin:2px 0"><a href="'+esc(n.href)+'">open its Task ↗</a></p>':'')+'</div><div><b>Rests on</b>'+chips(down[id],'down')
    +'<b>Used by</b>'+chips(up[id],'up')+((n.segs||[]).length?'<b>Segments</b><div class=chips>'+n.segs.map(function(x){
      return '<a class="sg'+(x===seg?' on':'')+'" data-seg="'+esc(x)+'">'+esc(x)+'</a>';}).join('')+'</div>':'')+'</div></div>'+(D.work?act(n):'');
  root.style.paddingBottom=(side.offsetHeight+24)+'px';   // room to scroll the last cards clear of the panel
  side.querySelector('.qc-x').addEventListener('click',function(){pin(null);});
  side.querySelectorAll('[data-seg]').forEach(function(a){a.addEventListener('click',function(){setSeg(a.dataset.seg===seg?'':a.dataset.seg);});});
  side.querySelectorAll('[data-go]').forEach(function(a){a.addEventListener('click',function(){pin(a.dataset.go,true);});});
}
function place(){var R=svg.getBoundingClientRect();side.style.left=R.left+'px';side.style.width=R.width+'px';}
// the panel belongs to its canvas: it leaves with it when the canvas is scrolled out of the window
if(window.IntersectionObserver)new IntersectionObserver(function(es){side.classList.toggle('away',!es[0].isIntersecting);}).observe(svg);
function ids(a){return a.length?a.join(', '):'none';}
function act(n){  // Work only: ask about it, or propose a follow-up for the next plan; copies a prompt, writes nothing
  var w=D.work, where='the insight Board '+w.board+(w.job?', Job '+w.job:'');
  var ask='On '+where+': a question about '+n.id+' ('+n.q+').'+(n.answer?' Its answer now: '+n.answer:'')
    +' It rests on '+ids(down[n.id])+' and is used by '+ids(up[n.id])+'.'+(n.task?' Read its Task '+n.task+' and its Runs\' results first, then answer from them; say what they cannot tell.':'');
  var prop=function(t){return 'Propose a follow-up to '+n.id+' ('+n.q+') for the next question version: write it as a proposal in '
    +w.proposals+' (haipipe-insight-question), with from: '+n.id+' and the level it asks at. The follow-up: '+t;};
  var h='<div class=qc-act><span class="pb-prompt qc-askbox"><textarea data-field="My question" rows=2 placeholder="Ask about '+esc(n.id)+' …"></textarea>'
    +'<button type=button class="fd-btn pb-copy" data-copy="'+esc(ask)+'" data-tail="'+esc(w.tail)+'">Ask about it</button></span>';
  if(n.gaps&&n.gaps.length){h+='<b>Follow up</b><ul class=qc-gaps>'+n.gaps.map(function(g){return '<li><span class=pb-prompt>'
    +'<button type=button class="fd-btn pb-copy" data-copy="'+esc(prop(g))+'" data-tail="'+esc(w.tail)+'">Propose</button></span> '+esc(g)+'</li>';}).join('')+'</ul>';}
  h+='<span class=pb-prompt><textarea data-field="The follow-up" rows=1 placeholder="or your own follow-up …"></textarea>'
    +'<button type=button class="fd-btn pb-copy" data-copy="'+esc(prop(''))+'" data-tail="'+esc(w.tail)+'">Propose mine</button></span></div>';
  return h;
}
function setSeg(x){seg=x;if(segEl)segEl.value=x;light(pinned);panel(pinned);}
function pin(id,go){pinned=id;
  if(id&&phone&&by[id].lv!==level){level=by[id].lv;draw();}
  if(id&&!pos[id]){onlyLinked=false;root.querySelector('.qc-only').checked=false;draw();}light(id);panel(id);tip(null);
  try{history.replaceState(null,'',location.pathname+location.search+(id?'#q='+id:''));}catch(e){}   // the share link follows the pin
  if(id&&go){var c=svg.querySelector('.card[data-id="'+id+'"]');if(c)c.scrollIntoView({block:'nearest',behavior:'smooth'});}
  if(id){var k=svg.querySelector('.card[data-id="'+id+'"]');   // the pinned card never hides under its own panel
    if(k){var over=k.getBoundingClientRect().bottom+12-side.getBoundingClientRect().top;if(over>0)window.scrollBy({top:over,behavior:'smooth'});}}}
root.querySelectorAll('.qc-style button').forEach(function(b){b.addEventListener('click',function(){style=b.dataset.s;
  root.querySelectorAll('.qc-style button').forEach(function(x){x.classList.toggle('on',x===b);});draw();});});
root.querySelector('.qc-only').addEventListener('change',function(e){onlyLinked=e.target.checked;draw();});
root.querySelector('.qc-find').addEventListener('input',function(e){var s=e.target.value.trim().toLowerCase();if(!s){pin(null);return;}
  var hit=D.nodes.find(function(n){return n.id.toLowerCase()===s;})||D.nodes.find(function(n){return (n.id+' '+n.name+' '+n.q).toLowerCase().indexOf(s)>=0;});if(hit)pin(hit.id,true);});
var lvEl=root.querySelector('.qc-lv'), segEl=root.querySelector('.qc-seg');
['X','D','I','K','W'].forEach(function(k){var L=D.levels.filter(function(x){return x[0]===k;})[0];if(!L)return;var b=document.createElement('button');b.type='button';b.dataset.lv=L[0];b.textContent=L[1];lvEl.appendChild(b);
  b.addEventListener('click',function(){level=L[0];draw();});});
if(segEl)segEl.addEventListener('change',function(){setSeg(segEl.value);});
function fit(){var w=svg.getBoundingClientRect().width||900;phone=w<600;root.classList.toggle('ph',phone);
  W=phone?Math.round(w):Math.max(520,Math.round(w));draw();place();}
window.addEventListener('resize',function(){clearTimeout(fit.t);fit.t=setTimeout(fit,150);});fit();
// a canvas in a closed tab draws at its real width when the tab opens (one canvas per question version or Job)
if(window.ResizeObserver){var lastW=0;new ResizeObserver(function(){var w=Math.round(svg.getBoundingClientRect().width);
  if(w&&Math.abs(w-lastW)>4){lastW=w;fit();}}).observe(root);}
var h=(location.hash.match(/q=([DIKWX]\d+)/)||[])[1];if(h&&by[h])pin(h);
})();
"""


def canvas(release: dict, job: dict | None, task_href, root: Path | None = None, work: dict | None = None,
           proposals=(), mode: str = "board") -> str:
    """Report (work=None): read and explore. Work (work={board, job, proposals, tail}): the same canvas, and a pinned
    question's panel can be asked about or followed up (a question is asked where the work is done)."""
    d = data(release, job, task_href, root, proposals if work else (), mode)
    if not d["nodes"]:
        return ""
    d["work"] = work
    blob = json.dumps(d).replace("</", "<\\/")
    seen = {n["state"] for n in d["nodes"]}
    swatch = lambda fill, word, dash="solid": (f'<span><i style="background:{fill};border:1px {dash} #1e1e1e;border-radius:50%"></i>{word}</span>')
    # a Question Book's legend names a difference only where one shows: a first version (every question new) has none
    code_key = [swatch(*x) for st, x in (("new", ("#dbe9ff", "new in this version")), ("changed", ("#fff1c2", "changed")),
                                         ("kept", ("#fff", "kept")), ("retired", ("#eee", "retired", "dashed")))
                if st in seen and (st == "retired" or seen & {"kept", "changed"})]
    key = ('<span class=qc-key>' + "".join(code_key) + '</span>' if code_key else "") if mode == "code" else (
           '<span class=qc-key><span><i style="background:#e9f6ec;border:1px solid #1e1e1e;border-radius:50%"></i>page written</span>'
           '<span><i style="background:#fff6db;border:1px solid #1e1e1e;border-radius:50%"></i>drafted</span>'
           '<span><i style="background:#fff;border:1px solid #1e1e1e;border-radius:50%"></i>not yet</span>'
           + ('<span><i style="background:#fff;border:1px dashed #1e1e1e;border-radius:50%"></i>asked, not planned</span>' if work else "")
           + '</span>')
    segs = ('<select class=qc-seg aria-label="Segment"><option value="">every segment</option>'
            + "".join(f'<option>{html.escape(x)}</option>' for x in d["segments"]) + '</select>') if d["segments"] else ""
    return (f'<style>{CSS}</style><div class=qc><div class=qc-bar><input class=qc-find type=search placeholder="find X03, timing …">'
            f'<span class=qc-style><button type=button class=on data-s=cards>Cards</button><button type=button data-s=net>Dots</button></span>'
            f'<label><input class=qc-only type=checkbox> Only linked</label>{segs}{key}<span class=qc-lv></span></div>'
            f'<svg class=qc-svg></svg><aside class=qc-side hidden></aside>'
            f'<script type="application/json">{blob}</script></div><script>{JS}</script>')
