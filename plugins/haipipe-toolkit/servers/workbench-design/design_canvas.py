"""Two live pictures for the design theme, at the insight theme's level (b11's plan × freeze matrix and question
canvas, JL 261102: "make it the same level"). Both read the folders only; nothing here writes.

    matrix(b, root)     the Block: goals down × methods across; each cell is its chain of Jobs, each Job a card that
                        shows how far it has got (the five method steps as a strip, designs passed and kept as a bar,
                        the top design and its prediction), the clock that moved between two Jobs of one cell, the
                        newest Job tagged, a held Job dashed, and an empty cell as the next Job to launch.
    lineage(j, root)    one Job: where each design came from, left to right, inside the fence: the fence's files →
                        the reasoning (t00's chains) → the ideas → the designs, ranked. A line joins each piece to what
                        it cites (a chain step's `from:`, an idea's topic, a design's idea, an element's `from:`).
                        Hover a card to light what it rests on (green) and what rests on it (orange); click to pin
                        and read it in the side panel; `#d=d01` opens with a design pinned.

Full names on screen (excalidraw-studio look rule 5): "version 2", "inputs version 1", "design 4 · fewest words";
an id is only a key or a folder name. Plain HTML, SVG and a little JavaScript; no package.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from live import design_reader as R
from live.frame import esc

OK_STATES = ("kept", "released")


# ── words for ids ───────────────────────────────────────────────────────────────────────────────────────────────
def version_words(v: str) -> str:
    m = re.match(r"^m(\d+)$", str(v or ""))
    return f"version {m.group(1)}" if m else str(v or "—")


def inputs_words(v: str) -> str:
    m = re.match(r"^i(\d+)$", str(v or ""))
    return f"inputs version {m.group(1)}" if m else str(v or "no inputs yet")


def job_words(j: dict) -> str:
    m = re.match(r"^j(\d+)$", j["id"])
    return f"Job {int(m.group(1))}" if m else j["id"]


def design_words(d: dict) -> str:
    return f'design {d["number"] or d["id"]} · {d["short"].replace("-", " ")}'


def method_words(m: str) -> str:
    name = R.METHODS.get(m, ("", ""))[0]
    return name.replace("-", " ") if name else m


def goal_words(g: dict) -> str:
    return str(g.get("aim") or g.get("name") or g.get("id") or "")


def pred_words(p: str) -> str:
    """`+3.6 [+2.0; +4.7]` → `+3.6 points (+2.0 to +4.7)`."""
    u = r"\s*(?:%|pp|pts|points)?\s*"
    m = re.match(rf"^\s*([+-]?[\d.]+){u}\[\s*([+-]?[\d.]+){u};\s*([+-]?[\d.]+){u}\]", str(p or ""))
    return f"{m.group(1)} points ({m.group(2)} to {m.group(3)})" if m else str(p or "")


# ── the Block's matrix ──────────────────────────────────────────────────────────────────────────────────────────
def _steps(j: dict) -> list:
    """The five method steps as done (1), started (0.5) or not (0): ① see input · ② reason · ③ conduct · ④ review
    item · ⑤ review whole, then the release."""
    ds = j["designs"]
    passed = sum(1 for d in ds if d["verifies"] and d["verifies"][-1]["status"] == "passed")
    released = sum(1 for d in ds if d["state"] == "released")
    drafted = sum(1 for d in ds if d["drafts"])
    return [("see input", 1 if j["manifest"] else 0),
            ("reason ideas", 1 if j["ideas"] else 0.5 if j["reason"] else 0),
            ("write designs", 1 if ds and drafted == len(ds) else 0.5 if drafted else 0),
            ("check each", 1 if ds and all((d["verifies"] and d["verifies"][-1]["status"] == "passed") or d["state"] == "dropped"
                                           for d in ds) else 0.5 if passed else 0),
            ("rank the whole", 1 if j["ranking"] else 0),
            ("released", 1 if released else 0)]


def _top(j: dict) -> tuple:
    """The rank-1 design and its predicted effect, from t99's ranking."""
    first = next((r for r in j["ranking"] if str(r.get("rank", "")).strip() == "1"), None)
    if not first:
        return None, ""
    d = next((d for d in j["designs"] if d["id"] == first.get("design")), None)
    return d, str(first.get("predicted") or "")


def _moved(a: dict, c: dict) -> str:
    if (a["method"], a["version"]) != (c["method"], c["version"]) and a["inputs"] != c["inputs"]:
        return "moved both: not one change"
    if a["inputs"] != c["inputs"]:
        return f'a new inputs version: {inputs_words(a["inputs"])} → {inputs_words(c["inputs"])}'
    return f'a new method version: {version_words(a["version"])} → {version_words(c["version"])}'


def _job_card(j: dict, newest: bool, href) -> str:
    """Two short lines under the name (JL 261102 walk: "do not make it too word"): how far, then the best design."""
    ds = j["designs"]
    passed = sum(1 for d in ds if d["verifies"] and d["verifies"][-1]["status"] == "passed")
    kept = sum(1 for d in ds if d["state"] in OK_STATES)
    released = sum(1 for d in ds if d["state"] == "released")
    held = str(j["state"]).lower() == "held"
    steps = _steps(j)
    done = sum(1 for _w, v in steps if v == 1)
    strip = "".join(f'<i class="s{int(v * 2)}" title="{esc(w)}{"" if v == 1 else " (started)" if v else " (not yet)"}"></i>'
                    for w, v in steps)
    top, pred = _top(j)
    state = ("held" if held else "released" if released else "waits for your review" if kept
             else "ranked" if j["ranking"] else str(j["state"]))
    pill = "ok" if released else "wait" if kept or held else "open"
    hold = f' title="{esc(re.sub(r"\s+", " ", j["hold"])[:400])}"' if held and j["hold"] else ""
    m = re.match(r"^\s*([+-]?[\d.]+)", str(pred or ""))
    return (f'<a class="dm-job{" held" if held else ""}{" newest" if newest else ""}" href="{esc(href("", "", j["path"]))}"{hold}>'
            + ('<em class=dm-new>newest</em>' if newest else "")
            + f'<span class=dm-t><b>{esc(job_words(j))}</b><span class="dm-st {pill}">{esc(state)}</span></span>'
            + (f'<span class=dm-sig>{esc(_approved_words(j))}</span>' if released else "")
            + f'<span class=dm-pin><span>method {esc(version_words(j["version"]))} ·</span> <span>{esc(inputs_words(j["inputs"]))}</span></span>'
            + f'<span class=dm-row><span class=dm-strip>{strip}</span><span class=dm-n>{done} of 6 steps</span></span>'
            + f'<span class=dm-n>{passed} of {len(ds) or "—"} passed · {kept} kept</span>'
            + (f'<span class=dm-top><span class=dm-nm>★ {esc(design_words(top))}</span>'
               f'<b>{esc(pred_words(pred))}</b></span>' if top else "")
            + "</a>")


def _approved_words(j: dict) -> str:
    """Who approved the release and when, in words: `approved 261012` (design_views._approved reads the Run)."""
    from live import design_views as V
    short, full = V._approved(j)
    day = re.search(r"\d{6}", str(short or ""))
    return f"✅ signed by a person {day.group(0)}" if day else "✅ signed by a person"


def matrix(b: dict, root: Path, href) -> str:
    methods = sorted(R.REGISTRY) if R.REGISTRY else []
    for j in b["jobs"]:
        if j["method"] and j["method"] not in methods:
            methods.append(j["method"])
    goals = [g for g in b["goals"] if str(g.get("signed", "")).startswith("✅")] or b["goals"]
    if not goals and not b["jobs"]:
        return '<p class=mut>No goal yet: a person writes and signs the first goal, then a Job pins it.</p>'
    newest = b["jobs"][-1]["name"] if b["jobs"] else ""
    out = ""
    for g in goals:
        gid = g.get("id")
        lanes = ""
        for m in methods:
            chain = [j for j in b["jobs"] if j["goal"] == gid and j["method"] == m]
            cards = []
            for a, c in zip([None] + chain, chain):
                if a is not None:
                    cards.append(f'<span class=dm-arrow>↓ {esc(_moved(a, c))}</span>')
                cards.append(_job_card(c, c["name"] == newest, href))
            body = "".join(cards) or '<span class=dm-empty>+ launch a Job</span>'
            lanes += (f'<div class=dm-lane><div class=dm-h title="{esc(m)}"><b>{esc(method_words(m))}</b>'
                      f'<span>{esc(R.METHODS.get(m, ("", ""))[1] or "")}</span></div>{body}</div>')
        signed = "signed" if str(g.get("signed", "")).startswith("✅") else "not signed"
        out += (f'<div class=dm-goal><span class=dm-gk>goal</span><b>{esc(goal_words(g))}</b>'
                f'<span>{esc(g.get("who", ""))} · {esc(g.get("venue", ""))} · {esc(g.get("n", ""))} designs a Job · {signed}'
                f'</span></div><div class=dm-lanes>{lanes}</div>')
    key = '<p class=dm-key>★ the best design · its predicted effect against the control, in points</p>'
    return f'<style>{MATRIX_CSS}</style><div class=dm>{out}</div>{key}'


MATRIX_CSS = """
.dm{display:flex;flex-direction:column;gap:8px;margin:6px 0 4px}
.dm-lanes{display:flex;flex-wrap:wrap;gap:10px;padding-top:6px}
.dm-lane{flex:1 1 150px;min-width:150px;max-width:260px;display:flex;flex-direction:column;gap:5px}
.dm-empty{border:1.5px dashed #9aa1ab;border-radius:10px;color:var(--muted,#57606a);font-size:12.5px;padding:18px 8px;text-align:center}
.dm-gk{font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted,#57606a);margin-right:8px}
.dm-h{font-size:12px;color:var(--muted,#57606a);padding:2px 4px}.dm-h b{display:block;color:var(--ink,#1e1e1e);font-size:13px;text-transform:capitalize}
.dm-goal{border:1px solid var(--line,#d0d7de);border-radius:10px;padding:8px 12px;background:#eef3fb;font-size:13.5px}
.dm-goal b{margin-right:8px}.dm-goal span:last-child{font-size:11.5px;color:var(--muted,#57606a)}
.dm-h{min-height:34px}
.dm-job,.dm-job:hover,.dm-job *{text-decoration:none}
.dm-job{position:relative;display:flex;flex-direction:column;gap:4px;border:1.4px solid #1e1e1e;border-radius:10px;min-width:0;
  padding:8px 9px;background:var(--paper,#fff);color:inherit;font-size:12.5px;transition:transform .12s,box-shadow .12s}
.dm-job:hover{transform:translateY(-1px);box-shadow:0 3px 10px rgba(0,0,0,.12)}
.dm-job.held{border-style:dashed;background:#f6f6f4}.dm-job.newest{border-color:#1f6feb;border-width:2px}
.dm-new{position:absolute;top:-9px;right:8px;background:#1f6feb;color:#fff;font-style:normal;font-size:10.5px;border-radius:8px;padding:0 6px}
.dm-t{display:flex;justify-content:space-between;align-items:center;gap:4px;flex-wrap:wrap}
.dm-st{font-size:10.5px;border-radius:8px;padding:0 6px;background:#eaeef2;white-space:nowrap}
.dm-st.ok{background:#d6f0dd;color:#1a5f2a}.dm-st.wait{background:#ffe7cc;color:#8a4600}
.dm-pin{font-size:11px;color:var(--muted,#57606a)}.dm-pin>span{white-space:nowrap}.dm-sig{font-size:11px;color:#1a5f2a}
.dm-row{display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.dm-strip{display:inline-flex;gap:2px}.dm-strip i{display:inline-block;width:11px;height:8px;border-radius:2px;border:1px solid #1e1e1e}
.dm-strip i.s2{background:#1a7f37;border-color:#1a7f37}.dm-strip i.s1{background:linear-gradient(90deg,#1a7f37 50%,#fff 50%)}
.dm-strip i.s0{background:#fff;border-color:#9aa1ab}
.dm-n{font-size:11.5px}.dm-top{display:flex;flex-direction:column;gap:1px;border-top:1px solid var(--line,#d0d7de);padding-top:4px;font-size:12px}
.dm-nm{min-width:0}.dm-top b{color:#1a7f37}
.dm-arrow{font-size:11px;color:#bc4c00;padding-left:6px}
.dm-key{font-size:11.5px;color:var(--muted,#57606a);margin:4px 0 0}
"""


# ── one Job's lineage canvas ────────────────────────────────────────────────────────────────────────────────────
COLUMNS = (("F", "The fence", "the inputs the work may read"), ("T", "The reasoning", "chains of steps, each with its source"),
           ("I", "The ideas", "what each design tries"), ("D", "The designs", "as ranked by another agent"))


def _cites(text: str, files: list) -> list:
    """The fence files a `from:` line names (`knowledge-wisdom-pages.md · Send salience § 3`), or `own knowledge`."""
    s = str(text or "")
    out = [f for f in files if f in s]
    if "own knowledge" in s.lower():
        out.append("own knowledge")
    return out


def lineage_data(j: dict, href) -> dict:
    files = sorted(f["name"].rstrip("/") for f in j["files"] if f["name"].rstrip("/") not in ("manifest.yaml",))
    rank = {r.get("design"): r for r in j["ranking"]}
    nodes, edges = [], set()
    used = set()
    for t in j["topics"]:
        tid = "T:" + str(t.get("id"))
        srcs = _cites(t.get("from"), files)
        for st in t.get("steps") or []:
            srcs += _cites(st.get("from"), files)
        for f in srcs:
            edges.add((tid, "F:" + f))
            used.add(f)
        nodes.append({"id": tid, "col": "T", "name": str(t.get("title") or t.get("id")),
                      "text": f'{len(t.get("steps") or [])} steps of reasoning', "state": "", "href": ""})
    ideas = {}
    for i in j["ideas"]:
        iid = "I:" + str(i.get("id"))
        ideas[str(i.get("id"))] = iid
        num = re.sub(r"\D", "", str(i.get("id"))).lstrip("0")
        nodes.append({"id": iid, "col": "I", "name": f'idea {num} · {str(i.get("name") or "").replace("-", " ")}',
                      "text": str(i.get("idea") or ""), "state": "", "href": ""})
        if i.get("topic"):
            edges.add((iid, "T:" + str(i["topic"])))
    for d in j["designs"]:
        did = "D:" + d["id"]
        r = rank.get(d["id"]) or {}
        state = d["state"] if d["state"] in ("kept", "released", "dropped") else (
            "passed" if d["verifies"] and d["verifies"][-1]["status"] == "passed" else
            "failed" if d["verifies"] and d["verifies"][-1]["status"] == "failed" else "draft")
        nodes.append({"id": did, "col": "D", "name": design_words(d), "text": d["message"][:600], "state": state,
                      "rank": str(r.get("rank") or ""), "pred": pred_words(r.get("predicted") or (d["prediction"] or {}).get("predicted")),
                      "why": str(r.get("why") or (d["prediction"] or {}).get("why") or "")[:600],
                      "href": href("", "", d["path"]), "key": d["id"]})
        idea = ideas.get(d["idea"]) or next((v for k, v in ideas.items()
                                             if str(next((i.get("design") for i in j["ideas"] if str(i.get("id")) == k), "")) == d["id"]), None)
        if idea:
            edges.add((did, idea))
        for el in d["elements"]:
            for f in _cites(el.get("from") if isinstance(el, dict) else "", files):
                edges.add((did, "F:" + f))
                used.add(f)
    for f in files + (["own knowledge"] if "own knowledge" in used else []):
        every = {"goal.md": "the goal: every step reads it, and the rules check and the ranking test against it",
                 "method.md": "the method version: the recipe every step follows"}.get(f)
        nodes.append({"id": "F:" + f, "col": "F", "name": f, "text": every or "",
                      "state": "every" if every else "" if f in used else "unused", "href": ""})
    ids = {n["id"] for n in nodes}
    return {"nodes": nodes, "edges": sorted([a, b] for a, b in edges if a in ids and b in ids), "columns": COLUMNS}


LINEAGE_CSS = """
.dc{display:flex;flex-direction:column;gap:10px;margin:6px 0 4px}
.dc-body{position:relative}
.dc-hint{font-size:12.5px;color:#57606a}
.dc-bar{display:flex;gap:10px;align-items:center;font-size:13px;flex-wrap:wrap}
.dc-bar input[type=search]{padding:4px 8px;border:1px solid #c9ccd1;border-radius:6px;width:220px;font:inherit}
.dc-key{display:inline-flex;gap:10px;color:#57606a;flex-wrap:wrap}.dc-key i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:4px;vertical-align:-1px;border:1px solid #1e1e1e}
.dc-svg{width:100%;border:1px solid #d0d7de;border-radius:10px;background:#fbfbfa}
.dc-svg .band{fill:#f2f1ee}.dc-svg .band.fence{fill:#eef3fb}.dc-svg .bandt{font:600 12px system-ui;fill:#57606a;letter-spacing:.04em}
.dc-svg .bands{font:11px system-ui;fill:#8a8f98}.dc-svg path.flow{fill:none;stroke:#8a8f98;stroke-width:2}
.dc-svg .card rect{fill:#fff;stroke:#1e1e1e;stroke-width:1.2}
.dc-svg .card text{font:12px system-ui;fill:#1e1e1e;pointer-events:none}.dc-svg .card .rk{font-weight:700}
.dc-svg .card .pr{fill:#1a7f37;font-weight:600}.dc-svg .card .pr.neg{fill:#57606a}
.dc-svg .card{cursor:pointer;transition:opacity .15s}
.dc-svg .card.s-kept rect,.dc-svg .card.s-released rect{fill:#c8ebd2}.dc-svg .card.s-released rect{stroke-width:2}
.dc-svg .card.s-failed rect{fill:#ffe08a}.dc-svg .card.s-every rect{fill:#eef3fb;stroke-width:2}.dc-svg .card.s-dropped rect,.dc-svg .card.s-unused rect{fill:#eee;stroke-dasharray:4 3}
.dc-svg .card.s-dropped text,.dc-svg .card.s-unused text{fill:#8a8f98}
.dc-svg path.e{fill:none;stroke:#9aa1ab;stroke-width:1;opacity:.3;transition:opacity .15s}
.dc-svg.lit .card{opacity:.38}.dc-svg.lit path.e{opacity:.04}
.dc-svg.lit .card.on,.dc-svg.lit .card.up,.dc-svg.lit .card.down{opacity:1}
.dc-svg .card.on rect{stroke-width:2.6;stroke:#1f6feb}
.dc-svg .card.down rect{stroke:#1a7f37;stroke-width:2}.dc-svg .card.up rect{stroke:#bc4c00;stroke-width:2}
.dc-svg.lit path.e.down{opacity:1;stroke:#1a7f37;stroke-width:1.8}.dc-svg.lit path.e.up{opacity:1;stroke:#bc4c00;stroke-width:1.8}
.dc-side{border:1px solid #d0d7de;border-radius:10px;padding:10px 12px;font-size:13px;background:#fff;position:sticky;bottom:8px;z-index:3;box-shadow:0 -4px 18px rgba(0,0,0,.12);display:none;max-height:38vh;overflow:auto;margin-top:8px}
.dc-side.on{display:block}
.dc-two{display:grid;grid-template-columns:1.6fr 1fr;gap:14px}.dc-side h4{margin:0 0 4px;font-size:15px}.dc-side .mut{color:#57606a}
.dc-side .msg{background:#e9f0fb;border-radius:12px;padding:6px 10px;margin:4px 0;white-space:pre-wrap}
.dc-side .why summary{cursor:pointer;color:#1864ab;font-size:12.5px}
.dc-side .chips{display:flex;flex-wrap:wrap;gap:4px;margin:4px 0 8px}
.dc-side .chips a{border:1px solid #c9ccd1;border-radius:10px;padding:1px 7px;cursor:pointer;text-decoration:none;color:inherit;font-size:12px}
.dc-side .chips a.down{border-color:#1a7f37}.dc-side .chips a.up{border-color:#bc4c00}
.dc-list{display:none}
@media(max-width:700px){.dc-two{grid-template-columns:1fr}.dc-scroll{display:none}.dc-list{display:block;font-size:13px}.dc-list a{display:flex;justify-content:space-between;border:1px solid #d0d7de;border-radius:8px;padding:5px 9px;margin:4px 0;cursor:pointer;color:inherit;text-decoration:none}.dc-list a.s-dropped{border-style:dashed;color:#8a8f98}.dc-list b{color:#1a7f37}.dc-list b.neg{color:#57606a}.dc-side.on{display:block}}
.dc-drop{font-size:12.5px;color:#57606a}.dc-drop a{display:inline-block;white-space:nowrap;border:1px dashed #9aa1ab;border-radius:10px;padding:1px 7px;margin:2px;cursor:pointer;color:inherit;text-decoration:none}
"""

LINEAGE_JS = r"""
(function(){
var root=document.currentScript.previousElementSibling, D=JSON.parse(root.querySelector('script[type="application/json"]').textContent);
var svg=root.querySelector('svg'), side=root.querySelector('.dc-side'), NS='http://www.w3.org/2000/svg';
var W=900, CH=30, GY=6, GX=30, TOP=8;
var by={}, down={}, up={}; D.nodes.forEach(function(n){by[n.id]=n;down[n.id]=[];up[n.id]=[];});
D.edges.forEach(function(e){down[e[0]].push(e[1]);up[e[1]].push(e[0]);});
var pinned=null, pos={};
function el(t,a,p){var x=document.createElementNS(NS,t);for(var k in a)x.setAttribute(k,a[k]);if(p)p.appendChild(x);return x;}
function short(s,k){return s.length>k?s.slice(0,k-1)+'…':s;}
function esc(s){return String(s==null?'':s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function draw(){
  svg.innerHTML='';pos={};
  var bandg=el('g',{},svg), eg=el('g',{},svg), cg=el('g',{},svg);
  var cols=D.columns, n=cols.length, colW=(W-16-(n-1)*GX)/n, cw=colW-20, bottom=0;
  cols.forEach(function(C,c){var lv=C[0], ns=D.nodes.filter(function(x){return x.col===lv;}), x=8+c*(colW+GX);
    function rk(m){if(m.col==='D')return parseInt(m.rank)||99;var d=up[m.id].filter(function(i){return by[i].col==='D';})[0];return d?(parseInt(by[d].rank)||99):999;}
    if(lv==='D'||lv==='I')ns.sort(function(a,b){return rk(a)-rk(b);});
    else if(c>0)ns.sort(function(a,b){function k(m){var ys=down[m.id].concat(up[m.id]).filter(function(i){return pos[i];}).map(function(i){return pos[i].y;});
      return ys.length?ys.reduce(function(s,v){return s+v;},0)/ys.length:1e5;}return k(a)-k(b);});
    var h=42+ns.length*(CH+GY)+4;
    el('rect',{x:x,y:TOP,width:colW,height:Math.max(h,70),rx:10,'class':'band'+(lv==='F'?' fence':'')},bandg);
    var t=el('text',{x:x+10,y:TOP+18,'class':'bandt'},bandg);t.textContent=C[1].toUpperCase();
    var s=el('text',{x:x+10,y:TOP+32,'class':'bands'},bandg);s.textContent=C[2];
    ns.forEach(function(m,i){card(m,x+10,TOP+42+i*(CH+GY),cw,CH,cg);});
    bottom=Math.max(bottom,TOP+Math.max(h,70));
    if(c<n-1){var ax=x+colW+GX/2;el('path',{d:'M'+(ax-7)+','+(TOP+12)+' l7,6 l-7,6','class':'flow'},bandg);}
  });
  D.edges.forEach(function(e){var a=pos[e[0]],b=pos[e[1]];if(!a||!b)return;
    var L=b.x<a.x?b:a,R=b.x<a.x?a:b,x1=L.x+L.w,y1=L.y+L.h/2,x2=R.x,y2=R.y+R.h/2,mx=(x1+x2)/2;
    el('path',{d:'M'+x1+','+y1+' C'+mx+','+y1+' '+mx+','+y2+' '+x2+','+y2,'class':'e','data-a':e[0],'data-b':e[1]},eg);});
  svg.setAttribute('viewBox','0 0 '+W+' '+(bottom+8));svg.style.height='auto';
  if(pinned&&pos[pinned])light(pinned);else{pinned=null;light(null);}
}
function card(m,x,y,w,h,g0){pos[m.id]={x:x,y:y,w:w,h:h};
  var g=el('g',{'class':'card'+(m.state?' s-'+m.state:''),'data-id':m.id,transform:'translate('+x+','+y+')'},g0);
  el('rect',{width:w,height:h,rx:7},g);
  var off=8;
  if(m.col==='D'&&m.rank){var r=el('text',{x:8,y:h/2+4,'class':'rk'},g);r.textContent='#'+m.rank;off=m.rank.length>1?38:30;}
  var room=w-off-8, pr=m.col==='D'&&m.pred?m.pred.split(' ')[0]:'';
  if(pr){var p=el('text',{x:w-8,y:h/2+4,'class':'pr'+(pr.charAt(0)==='-'?' neg':''),'text-anchor':'end'},g);p.textContent=pr;room-=38;}
  var b=el('text',{x:off,y:h/2+4},g);b.textContent=short(m.col==='D'?m.name.replace(/^design \d+ · /,''):m.name,Math.floor(room/6.4));
  var tt=el('title',{},g);tt.textContent=m.name+(m.state?' · '+m.state:'');
  g.addEventListener('mouseenter',function(){if(!pinned)light(m.id);});
  g.addEventListener('mouseleave',function(){if(!pinned)light(null);});
  g.addEventListener('click',function(){pin(pinned===m.id?null:m.id);});
}
function reach(id,map){var seen={},st=[id];while(st.length){var k=st.pop();map[k].forEach(function(j){if(!seen[j]){seen[j]=1;st.push(j);}});}return seen;}
function light(id){
  svg.classList.toggle('lit',!!id);
  var dn=id?reach(id,down):{}, upp=id?reach(id,up):{};
  svg.querySelectorAll('.card').forEach(function(g){var k=g.dataset.id;g.classList.toggle('on',k===id);g.classList.toggle('down',!!dn[k]);g.classList.toggle('up',!!upp[k]);});
  svg.querySelectorAll('path.e').forEach(function(p){var a=p.dataset.a,b=p.dataset.b;
    p.classList.toggle('down',!!(id&&(a===id||dn[a])&&dn[b]));p.classList.toggle('up',!!(id&&(b===id||upp[b])&&upp[a]));});
  panel(id);
}
function chips(ids,cls){return ids.length?'<div class=chips>'+ids.map(function(i){return '<a class='+cls+' data-go="'+esc(i)+'">'+esc(short(by[i].name,34))+'</a>';}).join('')+'</div>':'<p class=mut>none</p>';}
function panel(id){
  if(!id){side.classList.remove('on');return;}
  var n=by[id], body='';
  if(n.col==='D')body=(n.text?'<div class=msg>'+esc(n.text)+'</div>':'')+'<p style="margin:2px 0">'+(n.rank?'ranked <b>#'+esc(n.rank)+'</b> · ':'')+'<b>'+esc(n.state)+'</b>'
    +(n.pred?' · predicted <b>'+esc(n.pred)+'</b> against the control':'')+'</p>'+(n.why?'<details class=why><summary>why this rank</summary><p class=mut style="margin:2px 0">'+esc(n.why)+'</p></details>':'');
  else body=(n.text?'<p style="margin:2px 0">'+esc(n.text)+'</p>':'')+(n.state==='unused'?'<p class=mut>in the fence, cited by nothing</p>':'');
  side.innerHTML='<div class=dc-two><div><h4>'+esc(n.name)+'</h4>'+body+(n.href?'<p class=mut style="margin:2px 0"><a href="'+esc(n.href)+'">open its Task ↗</a></p>':'')
    +'</div><div><b>Rests on</b>'+chips(down[id],'down')+(up[id].length?'<b>Used by</b>'+chips(up[id],'up'):'')+'</div></div>';
  side.querySelectorAll('[data-go]').forEach(function(a){a.addEventListener('click',function(){pin(a.dataset.go);});});
  side.classList.add('on');
}
function pin(id){pinned=id;light(id);}
root.querySelectorAll('.dc-drop a,.dc-list a').forEach(function(a){a.addEventListener('click',function(){pin(a.dataset.go);});});
root.querySelector('.dc-find').addEventListener('input',function(e){var s=e.target.value.trim().toLowerCase();if(!s){pin(null);return;}
  // a design first, then an idea, the reasoning, a file: what a reader most often looks for
  var order=['D','I','T','F'], hit=null;order.some(function(c){hit=D.nodes.find(function(n){return n.col===c&&n.name.toLowerCase().indexOf(s)>=0;});return hit;});
  if(!hit)hit=D.nodes.find(function(n){return (n.name+' '+n.text).toLowerCase().indexOf(s)>=0;});if(hit)pin(hit.id);});
function fit(){var w=svg.getBoundingClientRect().width||900;W=Math.max(760,Math.round(w));draw();}
window.addEventListener('resize',function(){clearTimeout(fit.t);fit.t=setTimeout(fit,150);});fit();
var h=(location.hash.match(/d=(d\d+)/)||[])[1];if(h&&by['D:'+h])pin('D:'+h);
})();
"""


def lineage(j: dict, href) -> str:
    d = lineage_data(j, href)
    if not any(n["col"] == "D" for n in d["nodes"]) and not d["edges"]:
        return ""
    blob = json.dumps(d).replace("</", "<\\/")
    dropped = sorted((n for n in d["nodes"] if n["col"] == "D" and n["state"] == "dropped"),
                     key=lambda n: int(n.get("rank") or 99) if str(n.get("rank") or "").isdigit() else 99)
    ranked = sorted((n for n in d["nodes"] if n["col"] == "D"),
                    key=lambda n: int(n.get("rank")) if str(n.get("rank") or "").isdigit() else 99)
    phone = ('<div class=dc-list><p class=mut>Tap a design: its chain back to the fence shows below.</p>' + "".join(
        f'<a class="s-{esc(n["state"])}" data-go="{esc(n["id"])}"><span>#{esc(n.get("rank") or "")} '
        f'{esc(n["name"].split(" · ", 1)[-1])}</span><b{' class=neg' if (n.get("pred") or "").startswith("-") else ""}>{esc((n.get("pred") or "").split(" ")[0])}</b></a>' for n in ranked)
        + '</div>')
    drop = ('<p class=dc-drop>Dropped at the ranking: ' + "".join(
        f'<a data-go="{esc(n["id"])}">#{esc(n.get("rank") or "")} {esc(n["name"].split(" · ", 1)[-1])}</a>' for n in dropped)
        + '</p>') if dropped else ""
    key = ('<span class=dc-key><span><i style="background:#c8ebd2"></i>kept or released</span>'
           '<span><i style="background:#fff"></i>passed its check</span><span><i style="background:#ffe08a"></i>failed, to revise</span>'
           '<span><i style="background:#eee;border-style:dashed"></i>dropped or unused</span>'
           '<span><i style="background:#eef3fb"></i>read by every step</span><span><b style="color:#1a7f37">+3.6</b> predicted, in points</span></span>')
    return (f'<style>{LINEAGE_CSS}</style><div class=dc><div class=dc-bar><input class=dc-find type=search '
            f'placeholder="find a design, an idea, a file …">{key}</div><div class=dc-body><div class=dc-scroll><svg class=dc-svg></svg></div>{phone}{drop}<aside class=dc-side></aside></div>'
            f'<script type="application/json">{blob}</script></div><script>{LINEAGE_JS}</script>')
