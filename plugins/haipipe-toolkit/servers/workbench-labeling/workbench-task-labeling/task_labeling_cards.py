"""The cards each items step shows: the Data cards, the items' cards, and the embedding map with its cards."""
from __future__ import annotations

from pathlib import Path
from live.frame import esc, table
from live.ui_parts import plural_word
from live.labeling_theme import VIEW, _open, _view_url

from live.task_labeling_read import (IT, SAMPLE_N, _at, _bars, _cell, _code, _draw_again, _embedding_state,
                                     _fit_table, _fold, _histogram, _item_rows, _items_facts, _items_file, _json,
                                     _kv, _median, _not_yet, _raw_card, _raw_rows, _row_table, _runs_of, _stats,
                                     _status, _value, _yaml_file, sample_html)


# ── step 1 · Data: the Data cards ──────────────────────────────────────────────────────────────────
def _tiles(pairs) -> str:
    """The step's main numbers as tiles, the look of the meaning and expression Tasks' (round 4: Data's point, "600
    rows · 30 chats · 20 raters", sat inside its third fold)."""
    return ('<div class="pb-tiles ls-tiles4">' + "".join(f'<div class=pb-tile><span class=ls-num>{esc(v)}</span>'
                                                         f'<small>{esc(k)}</small></div>' for v, k in pairs) + "</div>")


def _cards(parts: list, top: str, as_parts: bool):
    """A step's cards: [(title, its state word, body)] and the tiles above them. The older single-section layout folds
    each card (its tiles inside the first); the shared layout takes (word, tiles, parts) and shows them as side tabs."""
    if as_parts:
        return parts, top
    return "".join(_fold(t, w, (top if i == 0 else "") + b) for i, (t, w, b) in enumerate(parts))


def data_point(task: Path) -> str:
    """Data's point in one line, its Results bar's word: "600 rows · 30 chats · 20 raters" (round 4)."""
    _, card = _raw_card(task)
    if not card:
        return ""
    t, proof = card.get("table") or {}, (card.get("grain") or {}).get("proof") or {}
    units = [f"{v:,} " + k[len("distinct_"):].removesuffix("_id") + "s" for k, v in proof.items()
             if k.startswith("distinct_") and isinstance(v, int) and v != t.get("rows")]
    return " · ".join([f'{t.get("rows", 0):,} rows'] + units)


def _data_cards(task: Path, root: Path, job, block, as_parts: bool = False):
    run, card = _raw_card(task)
    if not card:
        return ([], "") if as_parts else _not_yet("Step 1 fills this.")
    t, g = card.get("table") or {}, card.get("grain") or {}
    proof = g.get("proof") or {}
    seed = (card.get("samples") or {}).get("seed", 7)
    units = [(f"{v:,}", k[len("distinct_"):].removesuffix("_id") + "s") for k, v in proof.items()
             if k.startswith("distinct_") and v != t.get("rows")]
    size = t.get("bytes")
    pairs = [(f'{t.get("rows", 0):,}', "rows"), (str(t.get("columns", "—")), "columns"), *units]
    top = _tiles(pairs) if as_parts else _stats(pairs)      # the older layout keeps its stat row
    basic = _kv([("one row", esc(g.get("one_row_is") or "—")), ("the file", f'<code>{esc(t.get("file"))}</code>'),
                 ("size", esc(f"{size / 1e6:.1f} MB" if size else "—")), ("read by", _run_link(task, root, run))]
                + [(esc(k.replace("_", " ")), esc(f"{v:,}" if isinstance(v, int) else str(v))) for k, v in proof.items()])
    parts = [("📊 Basic description", f'{t.get("rows", 0):,} rows · ' + plural_word(t.get("columns", 0), "column", "columns"),
              basic),
             ("🎲 Random samples", plural_word(SAMPLE_N, "row", "rows") + ", drawn",
              f'<p>{_draw_again(task, root, "raw", "sample-raw")}</p>'
              f'<div id=sample-raw>{sample_html(task, root, "raw", int(seed))}</div>')]
    raw = _raw_rows(root, str(t.get("file") or ""))
    if raw[1]:
        parts.append(("📄 Raw rows", f"the first {len(raw[1])}",
                      _fit_table(raw[0], [[_cell(v) for v in r] for r in raw[1]], raw[1])))
    bg = card.get("background") or {}
    if bg:
        parts.append(("📖 Background", "recorded", _kv([(esc(k), _code(esc(str(v)))) for k, v in bg.items()])))
    groups = card.get("groups") or []
    rows = (card.get("synth_df") or {}).get("rows") or []
    if rows:
        parts.append(("🧩 One row (made up)", "made up", _row_table(groups, rows[0])))
    labels = card.get("labels") or []
    if labels:
        parts.append(("🏷 Current labels", plural_word(len(labels), "column", "columns"),
                      "".join(f"<h4 style=\"margin:12px 0 2px;font-size:14px\"><code>{esc(lb['column'])}</code> "
                              f"· {esc(lb.get('who'))}</h4>{_bars(lb.get('values') or {})}" for lb in labels)))
    text = (card.get("text_to_label") or {}).get("columns") or []
    if text:
        parts.append(("💬 Text to label", plural_word(len(text), "column", "columns"),
                      table(("column", "values", "words: median · min · max", "lines, median"),
                            [(f"<code>{esc(x['column'])}</code>", esc(f"{x.get('values', 0):,}"),
                              esc(f"{x.get('words_median')} · {x.get('words_min')} · {x.get('words_max')}"),
                              esc(x.get("lines_median"))) for x in text])))
    columns = "".join(f"<h4 title=\"{esc(grp.get('meaning') or '')}\">{esc(grp['name'])}</h4>" + table(
        ("column", "filled", "distinct", "typical values"),
        [(f"<code>{esc(c['name'])}</code>", esc(f"{c.get('filled', 0):.0%}"), esc(f"{c.get('distinct', 0):,}"),
          esc(c.get("typical") or "")) for c in grp.get("columns") or []]) for grp in groups)
    if columns:
        parts.append(("🗃 Columns", plural_word(len(groups), "group", "groups"), columns))
    gotchas = card.get("gotchas") or []
    dups = proof.get("exact_duplicate_rows", 0)
    parts.append(("⚠️ Watch out", plural_word(len(gotchas), "thing", "things") + " to watch" if gotchas
                  else "nothing to watch",
                  f"<p>{esc(plural_word(dups, 'exact duplicate row', 'exact duplicate rows'))}.</p>"
                  + ("<ul>" + "".join(f"<li>{esc(x)}</li>" for x in gotchas) + "</ul>" if gotchas else "")))
    return _cards(parts, top, as_parts)


def _run_link(task: Path, root: Path, run: Path | None) -> str:
    """A Run's name as the link that opens its card and receipt in the pop-out (round 4: no view linked a Run)."""
    if run is None:
        return "—"
    from live import focus_page as F
    return f'<a data-pop="{esc(run.name)}" href="{esc(F.run_url(run, root))}"><code>{esc(run.name)}</code></a>'


# ── step 2 · Items: the items' cards ───────────────────────────────────────────────────────────────
def _items_cards(task: Path, root: Path, job, block, as_parts: bool = False):
    f = _items_facts(task, root)
    if not f["done"]:
        return ([], "") if as_parts else _not_yet("Step 2 fills this, after Sign.")
    m, items = f["manifest"], _items_file(f, root)
    every = _item_rows(items) if items else []
    res = f["run"] / "result"
    stats, check = _json(res / "stats.json") or {}, _json(res / "check.json")
    out = [("🎲 Random items", plural_word(SAMPLE_N, "item", "items") + ", drawn",
            f'<p>{_draw_again(task, root, "items", "sample-items")}</p>'
            f'<div id=sample-items>{sample_html(task, root, "items", 7)}</div>')]
    n_items = m.get("items", len(every))
    pairs = [(f"{n_items:,}" if isinstance(n_items, int) else str(n_items), "items")]
    if every:
        pairs += [(_median([r[1] for r in every]), "words judged, median"),
                  (_median([r[2] for r in every]), "turns before, median")]
    if job and job.get("n_sealed") not in (None, "—"):
        pairs.append((str(job["n_sealed"]), "held back"))
    head = ("item", "context before", "main (judged)", "words", "turns")
    rowfmt = lambda r: (f"<code>{esc(r[0])}</code>", _cell(r[4].get('context_before', '')),
                        _cell(r[4].get("main", "")), esc(r[1]), esc(r[2]))
    top = _tiles(pairs) if as_parts else _stats(pairs)
    out.insert(0, ("📊 Items", f"{pairs[0][0]} items", _kv([("One item", esc(str(m.get("item") or "—"))),
                                                            ("made by", _run_link(task, root, f["run"]))])))
    if every:
        out.append(("📋 All items", "as they are", _fit_table(head, [rowfmt(r) for r in every])))
    if stats or every:
        wj = stats.get("words_judged") or {}
        tb = stats.get("turns_before") or {}
        if not wj and every and IT:
            w, t = [r[1] for r in every], [r[2] for r in every]
            wj = {"min": min(w), "median": _median(w), "max": max(w), "histogram": IT.histogram(w)}
            tb = {"min": min(t), "median": _median(t), "max": max(t), "histogram": IT.histogram(t)}
        body = (_histogram(wj.get("histogram") or {}, f"words judged: {wj.get('min')} · {wj.get('median')} · "
                                                        f"{wj.get('max')} (min · median · max)")
                + _histogram(tb.get("histogram") or {}, f"turns before: {tb.get('min')} · {tb.get('median')} · "
                                                          f"{tb.get('max')}")
                + (_kv([("shortest", " · ".join(f"<code>{esc(i)}</code>" for i in stats.get("shortest") or [])),
                                    ("longest", " · ".join(f"<code>{esc(i)}</code>" for i in stats.get("longest") or []))])
                   if stats.get("shortest") else ""))
        out.append(("📈 Statistics", "histograms", body))
    if every:
        first = every[0][4]
        out.append(("🧩 One item", str(every[0][0]), (
            "<div class=card-row>"
            f"<div><h4>before</h4>{_cell(first.get('context_before', ''))}</div>"
            f"<div class=key><h4>judged</h4>"
            f"{_cell(first.get('main', ''))}</div>"
            f"<div><h4>after</h4>"
            f"{_cell(first.get('context_after') or '') or '<span class=mut>none</span>'}</div></div>")))
    if check:
        names = (("ids_unique", "ids unique"), ("one_item_per_unit", "one item per unit"),
                 ("nothing_judged_empty", "nothing judged empty"), ("no_key_inside", "no label inside"))
        out.append(("✅ Check", "passed" if check.get("passed") else "failed",
                         table(("check", ""), [(esc(w), '<span class="st st-ok">✓</span>' if check.get(k)
                                               else '<span class="st st-warn">✗</span>') for k, w in names])))
    store = _at(root, str(f["metrics"].get("store") or m.get("store") or ""))
    kept = [(f"<code>{esc(p.name)}</code>", esc(f"{sum(1 for _ in open(p, encoding='utf-8')):,} rows"))
            for p in (store / "items.ground-truth.jsonl", store / "items.raters.jsonl") if p.is_file()]
    if kept or m.get("kept_out"):
        out.append(("🏷 Labels kept out", plural_word(len(kept), "file", "files"),
                    table(("file", ""), kept)))
    version = _kv([("store", f'<code>{esc(f["metrics"].get("store") or m.get("store") or "—")}</code>'),
                               ("made by", f'<code>{esc(f["run"].name)}</code>' + (f' · {esc(f["headline"])}'
                                                                                 if f["headline"] else "")),
                               ("revises", esc(m.get("revise_of") or "—")), ("what changed", esc(m.get("changed") or "—")),
                               ("the notes it was given", _cell(m.get("notes") or "—"))]
                    + [(esc(k), esc(_value(v))) for k, v in m.items()
                       if k not in {"source", "transform", "item", "items", "store", "kept_out", "revise_of", "changed",
                                    "notes"}])
    out.append(("📦 Version", f'{Path(str(f["metrics"].get("store") or m.get("store") or "")).name or "—"}', version))
    return _cards(out, top, as_parts)


# ── step 3 · Embedding: the map, then its cards ────────────────────────────────────────────────────
PALETTE = ("#4e79a7", "#f28e2b", "#e15759", "#76b7b2", "#59a14f", "#edc948", "#b07aa1", "#ff9da7", "#9c755f", "#bab0ac")


def _embed_runs(task: Path) -> list:
    """The items Task's own embedding Runs, oldest first: (folder, card, complete?)."""
    return [(r, _yaml_file(r / "run.yaml"), _status(r) == "complete" and (r / "result" / "map.json").is_file())
            for r in _runs_of(task, "embed")]


_MAP3D: dict = {}


def _map3d(res: Path, man: dict, root: Path) -> list:
    """The 3-D places: the Run's map3d.json; a Run made before it existed gets them from its vectors, worked out
    here and kept in memory, never written into its result (AGENTS.md rule 0)."""
    got = _json(res / "map3d.json")
    if got:
        return got
    vec = _at(root, str(man.get("vectors") or ""))
    if not man.get("vectors") or not vec.is_file():
        return []
    key = (str(vec), vec.stat().st_mtime)
    if key not in _MAP3D:
        try:
            import sys
            import numpy as np
            sys.path.insert(0, str(Path(IT.__file__).parent))
            from embedding_build import _map_3d
            ids = [p["item_id"] for p in _json(res / "map.json") or []]
            xyz = _map_3d(np.load(vec).astype("float32"), int(man.get("seed") or 0), str(man.get("map") or "tsne"))
            _MAP3D[key] = [{"item_id": i, "x": x, "y": y, "z": z} for i, (x, y, z) in zip(ids, xyz)]
        except Exception:                                            # no numpy or sklearn here: the 2-D map only
            _MAP3D[key] = []
    return _MAP3D[key]


def _item_texts(root: Path, man: dict) -> dict:
    """item id → (the turns before, the judged text), from the items the build embedded."""
    import json
    path = _at(root, str(man.get("items_store") or "")) / "items.jsonl"
    out = {}
    if man.get("items_store") and path.is_file():
        for line in open(path, encoding="utf-8"):
            try:
                r = json.loads(line)
            except ValueError:
                continue
            out[str(r.get("item_id"))] = (str(r.get("context_before") or ""), str(r.get("main") or ""))
    return out


MAP_JS = r"""<style>.imap button.on{background:var(--tab-wash);border-color:var(--tab-on);color:var(--tab-on)}</style><script>(function(){document.querySelectorAll('.imap:not([data-on])').forEach(function(w){w.dataset.on=1;
var D=JSON.parse(w.querySelector('.imap-data').textContent),svg=w.querySelector('svg'),g=svg.querySelector('g'),cv=w.querySelector('canvas'),
pick=w.querySelector('.imap-pick'),vb=svg.viewBox.baseVal,view={x:0,y:0,k:1},cam={yaw:.6,pitch:.35,zoom:1},focus=null,sel=null,spin=false,dots=[].slice.call(svg.querySelectorAll('circle'));
function esc(t){return String(t).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
var tip=w.querySelector('.imap-tip');function showTip(id,x,y){var t=D.items[id]||['',''];tip.innerHTML='<b>'+esc(id)+'</b> · G'+(D.group[id]+1)+(t[0]?'<div style="white-space:pre-wrap;margin-top:4px;padding-left:8px;border-left:3px solid var(--line)">'+esc(t[0])+'</div>':'')+'<div style="white-space:pre-wrap;margin-top:6px;padding:4px 8px;border-radius:6px;background:var(--tab-wash)">'+esc(t[1])+'</div>';tip.hidden=false;var r=tip.getBoundingClientRect();tip.style.left=Math.max(8,Math.min(x+14,innerWidth-r.width-8))+'px';tip.style.top=Math.max(8,(y+14+r.height>innerHeight?y-14-r.height:y+14))+'px';}function hideTip(){tip.hidden=true;}function three(){return cv&&!cv.hidden;}
function apply(){g.setAttribute('transform','translate('+view.x+' '+view.y+') scale('+view.k+')');var r=(5/Math.sqrt(view.k)).toFixed(2);
 dots.forEach(function(c){c.setAttribute('r',c.dataset.item===sel?r*1.8:r);c.style.opacity=(focus!==null&&c.dataset.group!==focus)?.12:.9;
 c.setAttribute('stroke',c.dataset.item===sel?'#000':'none');});draw();}
function choose(id){sel=id;var t=D.items[id]||['',''],gr=D.group[id];
 pick.innerHTML='<p><b>'+esc(id)+'</b> · G'+(gr+1)+'</p>'+(t[0]?'<div style="white-space:pre-wrap;max-height:12em;overflow-y:auto;padding:6px 10px;border-left:3px solid var(--line)">'+esc(t[0])+'</div>':'')
  +'<div style="white-space:pre-wrap;padding:6px 10px;margin-top:6px;border-radius:8px;background:var(--tab-wash)">'+esc(t[1])+'</div>';pick.hidden=false;apply();}
function zoomAt(px,py,f){var k=Math.min(16,Math.max(1,view.k*f));view.x=px-(px-view.x)*(k/view.k);view.y=py-(py-view.y)*(k/view.k);view.k=k;if(k===1){view.x=0;view.y=0;}apply();}
var drag=null;svg.addEventListener('pointerdown',function(e){drag={x:e.clientX,y:e.clientY,vx:view.x,vy:view.y,m:false};});
svg.addEventListener('pointermove',function(e){if(!drag)return;var dx=e.clientX-drag.x,dy=e.clientY-drag.y;if(!drag.m&&Math.abs(dx)+Math.abs(dy)<5)return;drag.m=true;
 var b=svg.getBoundingClientRect();view.x=drag.vx+dx*vb.width/b.width;view.y=drag.vy+dy*vb.height/b.height;apply();});
svg.addEventListener('pointerup',function(e){var m=drag&&drag.m;drag=null;if(!m&&e.target.dataset&&e.target.dataset.item)choose(e.target.dataset.item);});
svg.addEventListener('pointerleave',function(){drag=null;hideTip();});svg.addEventListener('mouseover',function(e){if(!drag&&e.target.dataset&&e.target.dataset.item)showTip(e.target.dataset.item,e.clientX,e.clientY);});svg.addEventListener('mouseout',function(e){if(e.target.dataset&&e.target.dataset.item)hideTip();});
svg.addEventListener('wheel',function(e){if(!e.ctrlKey&&!e.metaKey)return;e.preventDefault();var b=svg.getBoundingClientRect();
 zoomAt((e.clientX-b.left)*vb.width/b.width,(e.clientY-b.top)*vb.height/b.height,e.deltaY<0?1.15:1/1.15);},{passive:false});
function size(){var w=cv.clientWidth||800,d=devicePixelRatio||1;cv.width=w*d;cv.height=w*.55*d;cv.style.height=(w*.55)+'px';}
function proj(x,y,z){var cy=Math.cos(cam.yaw),sy=Math.sin(cam.yaw),cp=Math.cos(cam.pitch),sp=Math.sin(cam.pitch),x1=x*cy-z*sy,z1=x*sy+z*cy,y1=y*cp-z1*sp,z2=y*sp+z1*cp,f=3.2/(3.2-z2*.9),s=Math.min(cv.width,cv.height)*.4*cam.zoom;
 return{x:cv.width/2+x1*f*s,y:cv.height/2-y1*f*s,z:z2,f:f};}
function draw(){if(!cv||!three())return;var c=cv.getContext('2d'),d=devicePixelRatio||1;c.clearRect(0,0,cv.width,cv.height);c.strokeStyle='#adb5bd';c.fillStyle='#495057';c.lineWidth=1.2*d;c.font=(13*d)+'px sans-serif';[[1,0,0],[0,1,0],[0,0,1]].forEach(function(a,i){var p1=proj(-a[0],-a[1],-a[2]),p2=proj(a[0],a[1],a[2]);c.beginPath();c.moveTo(p1.x,p1.y);c.lineTo(p2.x,p2.y);c.stroke();c.fillText(D.axis+' '+(i+1),p2.x+4*d,p2.y-4*d);});
 var q=D.p3.map(function(p){var o=proj(p[1],p[2],p[3]);o.id=p[0];o.g=D.group[p[0]];return o;}).sort(function(a,b){return a.z-b.z;});
 q.forEach(function(o){o.r=Math.max(2,4.5*o.f*Math.sqrt(cam.zoom))*d;c.globalAlpha=(focus!==null&&String(o.g)!==focus)?.1:(.5+.5*(o.z+1)/2);
  c.fillStyle=D.colors[o.g%D.colors.length];c.beginPath();c.arc(o.x,o.y,o.r,0,6.2832);c.fill();if(o.id===sel){c.globalAlpha=1;c.lineWidth=3*d;c.strokeStyle='#000';c.stroke();}});
 c.globalAlpha=1;cv.__q=q;}
function loop(){if(!spin||!three())return;cam.yaw+=.006;draw();requestAnimationFrame(loop);}
function near(e){var b=cv.getBoundingClientRect(),d=devicePixelRatio||1,mx=(e.clientX-b.left)*d,my=(e.clientY-b.top)*d,best=null,bd=1e9;(cv.__q||[]).forEach(function(p){var dd=Math.hypot(p.x-mx,p.y-my);if(dd<Math.max(p.r+4*d,10*d)&&dd<=bd){best=p;bd=dd;}});return best;}
var d3=null;if(cv){cv.addEventListener('pointerdown',function(e){d3={x:e.clientX,y:e.clientY,m:false};});
 cv.addEventListener('pointermove',function(e){if(!d3){var h=near(e);if(h)showTip(h.id,e.clientX,e.clientY);else hideTip();cv.style.cursor=h?'pointer':'grab';return;}hideTip();var dx=e.clientX-d3.x,dy=e.clientY-d3.y;if(!d3.m&&Math.abs(dx)+Math.abs(dy)<4)return;d3.m=true;
  cam.yaw+=dx*.01;cam.pitch=Math.max(-1.45,Math.min(1.45,cam.pitch+dy*.01));d3.x=e.clientX;d3.y=e.clientY;draw();});
 cv.addEventListener('pointerup',function(e){var o=d3;d3=null;if(!o||o.m)return;var best=near(e);if(best)choose(best.id);});
 cv.addEventListener('pointerleave',function(){d3=null;hideTip();});
 cv.addEventListener('wheel',function(e){if(!e.ctrlKey&&!e.metaKey)return;e.preventDefault();cam.zoom=Math.max(.5,Math.min(6,cam.zoom*(e.deltaY<0?1.12:1/1.12)));draw();},{passive:false});}
w.querySelectorAll('[data-dim]').forEach(function(b){b.onclick=function(){var t=b.dataset.dim==='3';w.querySelectorAll('[data-dim]').forEach(function(x){x.classList.toggle('on',x===b);});
 svg.style.display=t?'none':'';cv.hidden=!t;w.querySelector('[data-spin]').hidden=!t;if(t){size();draw();}else{spin=false;}};});
var sp=w.querySelector('[data-spin]');if(sp)sp.onclick=function(){spin=!spin;sp.classList.toggle('on',spin);if(spin)requestAnimationFrame(loop);};
w.querySelectorAll('[data-zoom]').forEach(function(b){b.onclick=function(){var z=b.dataset.zoom;
 if(three()){if(z==='reset')cam={yaw:.6,pitch:.35,zoom:1};else cam.zoom=Math.max(.5,Math.min(6,cam.zoom*(z==='in'?1.3:1/1.3)));draw();return;}
 if(z==='reset'){view={x:0,y:0,k:1};apply();}else zoomAt(vb.width/2,vb.height/2,z==='in'?1.5:1/1.5);};});
w.querySelectorAll('[data-g]').forEach(function(b){b.onclick=function(){focus=focus===b.dataset.g?null:b.dataset.g;
 w.querySelectorAll('[data-g]').forEach(function(x){x.classList.toggle('on',x.dataset.g===focus);});apply();};});
});})();</script>"""


def _map_card(points: list, p3: list, groups: list, texts: dict, method: str = "tsne") -> str:
    """The items on an interactive map (JL 261014: "one for 2-D and one for 3-D ... the interactive one"; the
    labeling job's old map): 2-D drags and zooms, 3-D turns and spins; a group's button lights it; a dot clicked
    shows its item."""
    import json
    if not points:
        return ""
    xs, ys = [p["x"] for p in points], [p["y"] for p in points]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    w, h, pad = 1000, 560, 32
    sx = lambda v: pad + (v - x0) / ((x1 - x0) or 1) * (w - 2 * pad)
    sy = lambda v: pad + (v - y0) / ((y1 - y0) or 1) * (h - 2 * pad)
    dots = "".join(f'<circle cx="{sx(p["x"]):.1f}" cy="{sy(p["y"]):.1f}" r="5" fill="{PALETTE[p["group"] % 10]}" '
                   f'data-item="{esc(p["item_id"])}" data-group="{p["group"]}" style="cursor:pointer"></circle>' for p in points)
    axis = {"tsne": "t-SNE", "pca": "PC", "umap": "UMAP"}.get(method.lower(), method.upper())
    axes = (f'<path d="M{pad} {pad} V{h - pad} H{w - pad}" fill="none" stroke="#adb5bd" stroke-width="1.2"/>'
            f'<text x="{w - pad}" y="{h - 4}" text-anchor="end" font-size="13" fill="#495057">{esc(axis)} 1 →</text>'
            f'<text x="{pad + 4}" y="{pad - 4}" font-size="13" fill="#495057">↑ {esc(axis)} 2</text>')
    data = {"axis": axis, "colors": PALETTE, "group": {str(p["item_id"]): p["group"] for p in points},
            "p3": [[str(r["item_id"]), r["x"], r["y"], r["z"]] for r in p3],
            "items": {k: [v[0], v[1]] for k, v in texts.items()}}
    blob = json.dumps(data).replace("</", "<\\/")
    btn = lambda attr, word, on=False: (f'<button type=button class="work-act{" on" if on else ""}" {attr}>{word}</button>')
    legend = "".join(btn(f'data-g="{g["group"]}"', f'<svg width="10" height="10"><circle cx="5" cy="5" r="5" '
                         f'fill="{PALETTE[g["group"] % 10]}"/></svg> G{g["group"] + 1} {esc(g.get("size", ""))}')
                     for g in groups)
    bar = (((btn("data-dim=2", "2-D", True) + btn("data-dim=3", "3-D") + btn("data-spin hidden", "Spin")) if p3 else "")
           + btn("data-zoom=in", "+") + btn("data-zoom=out", "−") + btn("data-zoom=reset", "Reset"))
    return (f'<div class=imap><p style="display:flex;gap:6px;flex-wrap:wrap">{bar}</p>'
            f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px;touch-action:none;cursor:grab;'
            f'border:1px solid var(--line);border-radius:8px" role="img" aria-label="the items on the map">{axes}<g>{dots}</g></svg>'
            + (f'<canvas hidden style="display:block;width:100%;max-width:{w}px;border:1px solid var(--line);'
               f'border-radius:8px;touch-action:none;cursor:grab"></canvas>' if p3 else "")
            + f'<p style="display:flex;gap:6px;flex-wrap:wrap">{legend}</p><div class=imap-pick hidden></div><div class=imap-tip hidden style="position:fixed;z-index:50;'
            f'max-width:560px;max-height:90vh;overflow:hidden;padding:6px 10px;background:var(--bg);border:1px solid var(--line);border-radius:8px;'
            f'box-shadow:0 2px 8px rgba(0,0,0,.15);font-size:13px;pointer-events:none"></div>'
            f'<script type=application/json class=imap-data>{blob}</script></div>'
            + MAP_JS)


def _text_cell(texts: dict, i: str) -> str:
    """An item's id over its judged text, for a table."""
    return f"<code>{esc(i)}</code><br>{_cell((texts.get(str(i)) or ('', ''))[1])}"


def _embedding_cards(task: Path, root: Path, job, block, as_parts: bool = False):
    built = [r for r in _embed_runs(task) if r[2]]
    if not built:
        lane, emb, summary = _embedding_state(job, block)
        builds = (emb or {}).get("builds") or [] if isinstance(emb, dict) else []
        if builds:                                     # an older build on the labeling job's lane
            src = _view_url(job, VIEW["embedding"])
            return _cards([("📍 Map", "on the job's lane",
                            f'<iframe class=page-view src="{esc(src)}" loading=lazy title="Embedding"></iframe>'
                            f'<p class=mut>{_open(src, "open it on its own ↗")}</p>')], "", as_parts)
        return ([], "") if as_parts else _not_yet("Step 3 fills this, after Agree.")
    run, card, _ = built[-1]
    res = run / "result"
    points = _json(res / "map.json") or []
    groups = _json(res / "groups.json") or []
    dups = _json(res / "duplicates.json") or []
    far = _json(res / "outliers.json") or []
    man = _yaml_file(res / "manifest.yaml")
    dot = lambda g: (f'<svg width="12" height="12" aria-hidden="true"><circle cx="6" cy="6" r="5" '
                     f'fill="{PALETTE[g % 10]}"/></svg>')
    model = str(man.get("model", "")).split("/")[-1]
    texts = _item_texts(root, man)
    out = [("📍 Map", plural_word(len(points), "item", "items"),
            _map_card(points, _map3d(res, man, root), groups, texts, str(man.get("map") or "tsne"))),
           ("🧩 Groups", plural_word(len(groups), "group", "groups"),
            table(("group", "items", "top words", "typical items"),
                  [(f"{dot(g['group'])} G{g['group'] + 1}", esc(g.get("size", "")),
                    esc(" · ".join(g.get("keywords") or [])),
                    " · ".join(f"<code>{esc(i)}</code>" for i in g.get("typical") or [])) for g in groups])),
           ("📏 Near-duplicates", plural_word(len(dups), "pair", "pairs") if dups else "none",
            _fit_table(("item", "item", "cosine"), [(_text_cell(texts, d["a"]), _text_cell(texts, d["b"]),
                                                     esc(d["cosine"])) for d in dups]) if dups else "<p>none</p>"),
           ("🧭 Outliers", plural_word(len(far), "item", "items") if far else "none",
            _fit_table(("item", "group", "closeness"),
                       [(_text_cell(texts, o["item_id"]), f"G{o['group'] + 1}", esc(o["to_its_group"]))
                        for o in far]) if far else "<p>none</p>")]
    rows = [("model", esc(man.get("model", "—"))), ("vector size", esc(man.get("dim", "—"))),
            ("input", esc(man.get("input", "—"))), ("map", esc(str(man.get("map", "—")).upper())),
            ("seed", esc(man.get("seed", "—"))), ("items", f'<code>{esc(man.get("items_store", "—"))}</code>'),
            ("vectors", f'<code>{esc(man.get("vectors", "—"))}</code>'), ("Run", _run_link(task, root, run))]
    others = built[:-1]
    out.append(("⚙️ Builds", model or run.name,
                _kv(rows + ([("earlier", esc(" · ".join(r[0].name for r in others)))] if others else []))))
    return _cards(out, "", as_parts)
