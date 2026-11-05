"""A paper Board's evidence layer (j01 displays, j02 values, j03 citations): each item's drawn file, its body to
read, and the LaTeX table as HTML. haipipe-paper-evidence's build_displays_pdf.py reads the same files through here."""
from __future__ import annotations

import filecmp
import json
import re
import time
from pathlib import Path
from urllib.parse import quote

import yaml

from live import draft_steps as ds
from live.frame import esc, face
from live.ui_parts import _section
from live.board_read import _field, _num, _task_url, is_version
from live.board_interactions import IX_CSS


# ── the evidence layer (JL 261031: command → creation → evidence → writing; "I agree"): one Job of the paper Board
# beside the versions, holding Values, Citations and Displays; it reads work's returned Results, never raw data, and
# every version quotes it. Its bands: Displays t01-t19 main, t51-t59 appendix; Values t61-t69; Citations t71-t79. The
# older split Jobs (j21_displays, j22_citations) read the same way until they are merged ────────────────────────────
EVIDENCE_KINDS = (("Displays", r"display"), ("Values", r"value"), ("Citations", r"cite|citation"))


def evidence_html(board: Path, root: Path) -> str:
    """One section per evidence Job (JL 261031: "could we sepearte them? like job-evidence-cite, job-evidence-value,
    job-evidence-display"; evidence is independent of the writing and the venue, so it sits beside the versions). A
    display Job lists its main displays (t01-t49) then its appendix ones (t50 on); the others list their Tasks."""
    jobs = [d for d in sorted(board.glob("j[0-9]*_*")) if d.is_dir() and not is_version(d)]
    # a combined evidence Job (j21_evidence) splits by its bands: displays t01-t59, values t61-t69, citations t71-t79
    band = {"Displays": (1, 59), "Values": (61, 69), "Citations": (71, 79)}
    out = ""
    for kind, pat in EVIDENCE_KINDS:
        for job in (j for j in jobs if re.search(pat, j.name, re.I) or not any(re.search(q, j.name, re.I) for _, q in EVIDENCE_KINDS)):
            tasks = sorted((x for x in job.glob("t[0-9]*_*") if x.is_dir()), key=_num)
            if not re.search(pat, job.name, re.I):
                tasks = [x for x in tasks if band[kind][0] <= _num(x) <= band[kind][1]]
            if kind == "Displays":
                main = [x for x in tasks if _num(x) < 50]
                app = [x for x in tasks if _num(x) >= 50]
                body = ("<h4 class=pb-part>Main</h4>" + "".join(evidence_item(x, root) for x in main) if main else "") + \
                       ("<h4 class=pb-part>Appendix</h4>" + "".join(evidence_item(x, root) for x in app) if app else "")
            else:
                body = "".join(evidence_item(x, root) for x in tasks)
            if not body:
                md = face(job)
                state = (_field(md.read_text(encoding="utf-8", errors="ignore"), "state") if md else "") or "no Tasks yet"
                body = f'<p class=mut>{esc(state)}</p>'
            out += _section(f"{kind} · {job.name}", body + f'<p><a class=fd-btn href="{esc(_task_url(job, root))}">Open {esc(job.name)} ↗</a></p>')
    return out or '<p class=mut>No evidence Job yet.</p>'


# ── each evidence opens to show itself (JL 261031: "how could we preview these evidences? to be collapse open and
# close, them to see all of them"): a folded row per display, value or citation; open, its picture or table (the
# Task's own Run result, else the work Run its made-by names), or its list of values, then its facts ────────────────
PREVIEW_EXT = (".png", ".svg", ".jpg", ".jpeg", ".pdf", ".html")


EV_FACTS = ("answers", "cited-in", "layout", "sources", "made-by", "caption")


def _evidence_file(task: Path, text: str) -> Path | None:
    """The drawn display: the newest picture in the Task's own Runs, else in the work Run its `made-by:` names."""
    def best(files):
        files = [f for f in files if f.suffix.lower() in PREVIEW_EXT and f.is_file()]
        return min(files, key=lambda f: (PREVIEW_EXT.index(f.suffix.lower()), -f.stat().st_mtime)) if files else None
    own = best(list(task.glob("runs/*/result/**/*")) + list(task.glob("result/**/*")))
    if own:
        return own
    m = re.search(r"(?mi)^made-by:.*?\bb(\d+)\.j(\d+)\.t(\d+)\.r(\d+)", text)
    project = next((d for d in task.parents if (d / "work").is_dir()), None)
    if not m or project is None:                # drawn inside a Section's display/ unit (status: drawn in tNN's draft)
        slug = re.sub(r"[^a-z0-9]", "", _field(text, "label").lower())
        board = task.parent.parent
        units = [u for u in board.glob("j*_*/t*_*/display/*")      # a whole name part: "table1" is not in "etable1"
                 if u.is_dir() and slug and slug in re.split(r"[^a-z0-9]+", u.name.lower())]
        for u in units:
            pic = best(list(u.rglob("*")))
            if pic:
                return pic
            if (u / "float.tex").is_file():
                return u / "float.tex"
        return None
    b, j, k, r = m.groups()
    return best([f for d in project.glob(f"work/b{b}_*/j{j}_*/t{k}_*/runs/r{r}_*/result") for f in d.rglob("*")])


LEDGERS = ("values.html", "citations.html")


def ledger_file(task: Path) -> Path | None:
    """The newest Run's ledger page of a value or citation Task (values.html or citations.html), else None."""
    found = [f for name in LEDGERS for f in task.glob(f"runs/*/result/{name}")]
    return max(found, key=lambda f: (f.parent.parent.name, f.stat().st_mtime)) if found else None


def empty_job(job: Path) -> str:
    """An evidence Job with no Task yet: its face's state, and the script that makes its Tasks."""
    md = face(job)
    state = _field(md.read_text(encoding="utf-8", errors="ignore"), "state") if md else ""
    how = ("write a value map, tNN_<group>/scripts/value_map.yaml, then run haipipe-paper-evidence gen_value_runs.py"
           if re.search(r"value", job.name) else
           "write a claim group, tNN_<group>/scripts/claim_group.yaml, then run haipipe-paper-evidence cite_tasks.py gen"
           if re.search(r"cite|citation", job.name) else "")
    return f'<p class=mut>No Tasks yet{(" (state: " + esc(state) + ")") if state else ""}.' + (f" To make them: {esc(how)}." if how else "") + "</p>"


def evidence_item(task: Path, root: Path) -> str:
    label, status, body = evidence_body(task, root)
    return (IX_CSS + f'<details class=ix-fold><summary><b>{esc(task.name)}</b><span class=ix-state>{esc(label)}</span>'
            f'<span class=ix-state>{esc(status)}</span></summary><div class=ix-body>{body}</div></details>')


# ── the Values tabs (JL 261104, r04_collect_values_tables): the side tabs stay, each tab one readable topic; its right side a
# raw table, one window at a time, and the numbered values below it. Tables and values come from Runs; the status is checked on
# every open, against the source Run, never typed. A table's cells are drawn in the browser: there are 25,000 of them. ─────
VALUES_CSS = """<style>
.vt-full{width:calc(100vw - 48px);max-width:none;height:calc(100vh - 48px)!important;max-height:none!important;border:1px solid var(--line);border-radius:10px;padding:0 22px 20px;color:inherit;background:var(--bg,#fff);overflow:auto}
.vt-full::backdrop{background:rgba(0,0,0,.35)}.vt-fullbar{position:sticky;top:0;z-index:5;display:flex;justify-content:space-between;align-items:center;padding:14px 0 10px;background:var(--bg,#fff);font-size:17px}
.vt-full .vt-popb{display:none}.vt-full .vt-scroll{max-height:calc(100vh - 300px)}
.vt-head{display:flex;align-items:flex-start;justify-content:space-between;gap:14px;margin:0 0 10px}.vt-head .vt-popb{flex:none;white-space:nowrap}
.vt-story{margin:0;font-size:14px;line-height:1.45}
.vt-cols{align-items:center;padding-top:4px}.vt-cols span{font-size:12.5px;font-weight:600;margin-right:2px}
.vt-how{margin:12px 0;border:1px solid var(--line);border-radius:8px;padding:8px 12px}.vt-how summary{cursor:pointer;font-size:14px;font-weight:600}.vt-how[open] summary{margin-bottom:8px}.vt-now,.vt-now-runs{margin:6px 0;font-size:12.5px;opacity:.8;overflow-wrap:anywhere}
.vt-axes{margin:8px 0 0;font-size:12.5px;opacity:.75}
.vt-chips{display:flex;flex-wrap:wrap;gap:5px;margin:0 0 7px}
.vt-chips button{all:unset;cursor:pointer;font-size:12.5px;padding:3px 10px;border:1px solid var(--line);border-radius:999px}
.vt-chips button.on{background:#1971c2;border-color:#1971c2;color:#fff}
.vt-chips button:focus-visible{outline:2px solid #1971c2;outline-offset:1px}
.vt-scroll{overflow:auto;max-height:560px;border:1px solid var(--line);border-radius:8px;margin:8px 0 14px}
.vt-t{border-collapse:collapse;font-size:13px;font-variant-numeric:tabular-nums;width:100%}
.vt-t th,.vt-t td{border:1px solid var(--line);padding:5px 8px;text-align:right;white-space:nowrap}
.vt-t th{position:sticky;top:0;z-index:2;font-weight:600;font-size:12px;background:var(--bg,#fff)}
.vt-t th:first-child,.vt-t td:first-child{position:sticky;left:0;z-index:1;text-align:left;font-weight:600;background:var(--bg,#fff)}
.vt-t th:first-child{z-index:3}
.vt-t td.c{cursor:pointer}.vt-t td.c:hover{background:color-mix(in srgb,#1971c2 10%,var(--bg,#fff))}
.vt-t.vt-marks td.c{text-align:center;font-size:15px}.vt-t.vt-marks th{text-align:center}.vt-t.vt-marks th:first-child{text-align:left}
.vt-t td.vt-grp{text-align:left;font-size:12.5px;font-weight:700;background:color-mix(in srgb,#868e96 12%,var(--bg,#fff))}.vt-state{margin:8px 0 0;font-size:13px;font-weight:600}
.vt-t td small{display:block;font-size:10.5px;font-weight:400;opacity:.72}
.vt-list{margin:6px 0 0;padding-left:24px;font-size:13.5px}.vt-list li{margin-bottom:6px}.vt-list small{display:block;opacity:.68;font-size:11.5px}
.vt-d .d{overflow-wrap:anywhere;min-width:0}
.vt-d{height:fit-content!important;max-height:80vh!important;overflow:auto;max-width:620px;width:calc(100vw - 32px);border:1px solid var(--line);border-radius:10px;padding:18px 20px;color:inherit;background:var(--bg,#fff)}
.vt-d::backdrop{background:rgba(0,0,0,.35)}.vt-d h4{margin:0 26px 8px 0;font-size:24px;overflow-wrap:anywhere}.vt-x{position:absolute;top:10px;right:12px}
</style>"""

VALUES_JS = r"""<script>
(function(){
if(window.vtReady)return;window.vtReady=1;
var WORDS={},ENDS={},MARK=['✅','🔶','⬜'];
function marksOnly(t){return !!t.row_head&&t.rows.length>0&&t.rows.every(function(r){return r.cells.every(function(c){return MARK.indexOf(c.v)>=0})})}
function grouped(t){return !!t.row_head&&t.rows.length>0&&t.rows.every(function(r){return /^\d{4}\s.+\s·\s/.test(String(r.head))})}
function attr(v){return esc(v).replace(/"/g,'&quot;')}
function word(w){if(WORDS[w])return WORDS[w];var m=w.match(/^(.*)_([^_]+)$/);
 if(m&&ENDS[m[2]])return word(m[1])+', '+ENDS[m[2]];w=w.replace(/_/g,' ');return w.charAt(0).toUpperCase()+w.slice(1)}
function one(v){var x=Number(v);if(v===''||isNaN(x))return WORDS[v]||v;if(Number.isInteger(x))return v;return Math.abs(x)<10?x.toFixed(3).replace(/0$/,''):x.toFixed(1)}
function show(v){return String(v).split(' / ').map(one).join(' / ')}
function esc(t){var d=document.createElement('div');d.textContent=t;return d.innerHTML}
var data={};
function load(url){return data[url]||(data[url]=fetch(url).then(function(r){return r.json()}))}
function dlg(box){return document.querySelector('.vt-d')}
window.vtPop=function(b){var w=b.closest('.vt-panel'),d=document.createElement('dialog');d.className='vt-full';
 var bar=document.createElement('div');bar.className='vt-fullbar';var h=document.createElement('b');h.textContent=w.dataset.title;
 var x=document.createElement('button');x.type='button';x.className='fd-btn';x.textContent='✕ Close';x.onclick=function(){d.close()};bar.appendChild(h);bar.appendChild(x);
 var kids=[].slice.call(w.childNodes);d.appendChild(bar);kids.forEach(function(k){d.appendChild(k)});w.appendChild(d);
 d.addEventListener('close',function(){kids.forEach(function(k){w.appendChild(k)});d.remove()});
 d.addEventListener('click',function(e){if(e.target===d)d.close()});d.showModal()};
function open(box,t,c,row){var m=JSON.parse(box.dataset.meta)[t.from]||{},d=dlg(box);var flag=c.flag;
 var st=flag?'🔶 check: '+flag:m.status+': '+m.why;var line=function(a,b){return '<div class=fd-row><span class=n>'+a+'</span><span class=d>'+b+'</span></div>'};
 d.querySelector('.vt-b').innerHTML='<h4>'+esc(c.v||'—')+'</h4><p>'+esc(c.at||row)+(c.n?' ('+c.n+' source rows, shown as they are)':'')+'</p>'
 +line('Status',esc(st))+line('Source Run',esc(m.run||''))+line('Read from','<a data-pop="'+esc(t.file)+'" href="'+esc(box.dataset.base+t.file)+'">'+esc(t.file)+'</a>')
 +line('Figures reading it',esc(m.figures||'none'))+line('Sections quoting its values',esc(m.sections||'none yet'));d.showModal()}
function draw(box,tab){var keys=tab.tables.map(function(t){return t.key});var depth=keys.length?Math.max.apply(null,keys.map(function(k){return k.length})):0;
 var sel=box._sel||(box._sel=[]);var chips=box.querySelector('.vt-pick');chips.innerHTML='';var match=keys;
 for(var j=0;j<depth;j++){var opts=[];match.forEach(function(k){if(k[j]!==undefined&&opts.indexOf(k[j])<0)opts.push(k[j])});
  if(opts.indexOf(sel[j])<0)sel[j]=opts[0];
  if(opts.length>1){var r=document.createElement('div');r.className='vt-chips';opts.forEach(function(o){var b=document.createElement('button');b.type='button';b.textContent=o;
    if(o===sel[j])b.className='on';(function(j,o){b.onclick=function(){sel[j]=o;draw(box,tab)}})(j,o);r.appendChild(b)});chips.appendChild(r)}
  match=match.filter(function(k){return k[j]===sel[j]})}
 var t=tab.tables.filter(function(x){return x.key.join('|')===match[0].join('|')})[0]||tab.tables[0];
 var m=JSON.parse(box.dataset.meta)[t.from]||{},head=t.row_head?['<th>'+esc(word(t.row_head))+'</th>']:[];
 var picked=box._cols||(box._cols=[]),shown=function(c){return !t.row_head||!picked.length||picked.indexOf(c)>=0||t.cols.every(function(x){return picked.indexOf(x)<0})};
 if(t.row_head&&t.cols.length>2){var cr=document.createElement('div');cr.className='vt-chips vt-cols';var lab=document.createElement('span');lab.textContent='Compare:';cr.appendChild(lab);
  var none=t.cols.every(function(c){return !picked.length||picked.indexOf(c)<0});
  var allb=document.createElement('button');allb.type='button';allb.textContent='All';if(none)allb.className='on';allb.onclick=function(){box._cols=[];draw(box,tab)};cr.appendChild(allb);
  t.cols.forEach(function(c){var b=document.createElement('button');b.type='button';b.textContent=c;if(picked.indexOf(c)>=0)b.className='on';
   b.onclick=function(){var i=picked.indexOf(c);if(i>=0)picked.splice(i,1);else picked.push(c);draw(box,tab)};cr.appendChild(b)});chips.appendChild(cr)}
 t.cols.forEach(function(c){if(shown(c))head.push('<th>'+esc(word(c))+'</th>')});if(!t.row_head)head.push('<th>Status</th>');
 var marks=marksOnly(t),plain=marks||grouped(t),n=head.length,last=null,names=marks?tab.tables.filter(function(x){return x!==t&&x.from===t.from&&x.rows.length===t.rows.length})[0]:null;
 var html='<table class="vt-t'+(marks?' vt-marks':'')+'"><thead><tr>'+head.join('')+'</tr></thead><tbody>';
 t.rows.forEach(function(r,i){var g=plain?String(r.head).match(/^\d+\s+(.+?)\s+·\s+(.+)$/):null;
  if(g&&g[1]!==last){last=g[1];html+='<tr><td class=vt-grp colspan="'+n+'">'+esc(g[1])+'</td></tr>'}
  html+='<tr>'+(t.row_head?'<td>'+esc(g?g[2]:r.head)+'</td>':'');
  r.cells.forEach(function(c,k){if(!shown(t.cols[k]))return;var st=c.flag?'🔶 check':m.status;
   var tip=names&&names.rows[i]&&names.rows[i].cells[k]?' title="'+attr(names.rows[i].cells[k].v)+'"':'';
   html+=(!t.row_head&&k===0?'<td class=c':'<td class=c')+tip+' data-r="'+i+'" data-k="'+k+'">'+esc(show(c.v))+(t.row_head&&c.v!==''&&!plain?'<small>'+esc(st)+'</small>':'')+'</td>'});
  if(!t.row_head)html+='<td>'+esc(m.status||'')+'</td>';html+='</tr>'});
 box.querySelector('.vt-scroll').innerHTML=html+'</tbody></table>';
 var now=box.parentElement.querySelector('.vt-now');if(now)now.textContent='This table: '+t.from.split('/').pop()+(t.keeps?', keeping '+t.keeps:'')+(t.column?', column '+t.column:'')+'.';
 var state=box.querySelector('.vt-state');if(!state){state=document.createElement('p');state.className='vt-state';box.insertBefore(state,box.querySelector('.vt-axes'))}
 state.textContent=plain?(m.status==='✅ current'?'✅ All current':(m.status||'')+': '+(m.why||'')):'';state.style.display=plain?'':'none';
 box.querySelector('.vt-axes').textContent=marks?'✅ has it · 🔶 partly · ⬜ none. Hover a cell for its raw fields; click for its source.':plain?'Click a cell for its source.':t.row_head?'Rows: '+word(t.row_head)+'. Columns: '+word(t.col_head||'')+'. Cells: '+word(t.cell_head||'')+'. Click a cell for its source.':'One row per source row. Click a cell for its source.';
 box.querySelector('.vt-scroll').onclick=function(ev){var td=ev.target.closest('td.c');if(!td)return;var r=t.rows[+td.dataset.r],c=r.cells[+td.dataset.k];
  var label=t.row_head?'':t.cols.map(function(n,i){return i<3?word(n)+' '+r.cells[i].v:''}).filter(Boolean).join(', ')+'; column '+t.cols[+td.dataset.k];open(box,t,c,label)}}
function init(){document.querySelectorAll('.vt-tab').forEach(function(box){if(box._on)return;box._on=1;
 load(box.dataset.url).then(function(all){WORDS=all.words||{};ENDS=all.suffixes||{};draw(box,all.tabs[+box.dataset.i])}).catch(function(){box.querySelector('.vt-scroll').textContent='The table file did not load.'})})}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init();
})();
</script>"""


def source_status(res: Path, frm: str, built: float, root: Path) -> tuple:
    """(status word, why, source Run) of one source file, from the disk as it is now. res: the tables' result folder."""
    task, key, rest = frm.split("/", 2)
    run = next((r for r in sorted((res.parents[3] / task / "runs").glob("*/result"), reverse=True) if (r / key / rest).is_file()),
               res.parents[3] / task)                    # the newest of the Task's Runs that holds it (build_tables.py)
    note = run / key / "SOURCE.txt"
    copied = note.read_text(encoding="utf-8", errors="ignore").strip().removeprefix("copied from ") if note.is_file() else ""
    real = root / copied / rest if copied else None
    if real is None or not real.is_file():
        return "❗ source gone", "The source file is no longer in its Run's result.", copied
    if not filecmp.cmp(real, run / key / rest):
        return "❗ source changed", "The source file changed after it was collected. Rerun the value Run, then this table.", copied
    if (run / key / rest).stat().st_mtime > built + 1:
        return "❗ rebuild", "The value Run collected again after this table was built. Rerun r01_build_tables.", copied
    return "✅ current", "This table's source file is the same as the file in the source Run.", copied


def _values(job: Path) -> dict:
    """Every printed value of a value Job, the newest Run of each Task winning: id -> (its Task, its entry)."""
    out = {}
    for f in sorted(job.glob("t[0-9]*_*/runs/*/result/values.json")):
        out.update({vid: (f.parents[3].name, v) for vid, v in json.loads(f.read_text(encoding="utf-8")).items()})
    return out


def _section_quotes(board: Path, ids) -> dict:
    """value id -> the Sections whose text holds it, read from every version's Tasks, each Task's newest draft."""
    ids, out = set(ids), {}
    for job in sorted(j for j in board.glob("j[0-9]*_*") if j.is_dir() and is_version(j)):
        for t in sorted(job.glob("t[0-9]*_*")):
            drafts = sorted((t / "draft").glob("*.md")) if (t / "draft").is_dir() else []
            text = drafts[-1].read_text(encoding="utf-8", errors="ignore") if drafts else ""
            for vid in ids & set(re.findall(r"[\w-]+", text)):
                out.setdefault(vid, []).append(t.name)
    return out


def _read_by(job: Path) -> dict:
    """<value Task>/<key> -> the displays whose newest Run reads that file, from each display Task's Run configs."""
    out = {}
    disp = next((d for d in sorted(job.parent.glob("j[0-9]*_*")) if re.search("display", d.name, re.I)), None)
    for t in sorted(disp.glob("t[0-9]*_*")) if disp else []:
        faces = face(t)
        name = _field(faces.read_text(encoding="utf-8", errors="ignore"), "label") if faces else ""
        cfgs = sorted((t / "scripts" / "config").glob("r[0-9]*.yaml"))
        run = next((c for c in reversed(cfgs) if (t / "runs" / c.stem).is_dir()), None)
        for a in (yaml.safe_load(run.read_text(encoding="utf-8")) or {}).get("args", []) if run else []:
            out.setdefault(str(a), []).append(name or t.name)
    return out


def _value_lines(values: dict, wanted: list, used: set) -> str:
    """The numbered list under a tab's table: every printed value whose id starts with one of `wanted`."""
    items = ""
    for vid, (_, v) in values.items():
        if vid in used or not any(vid.startswith(w) for w in wanted):
            continue
        used.add(vid)
        items += (f'<li><b>{esc(v.get("text", ""))}</b>: {esc(v.get("says", ""))}'
                  f'<small>{esc(vid)} · {esc(v.get("source", ""))}</small></li>')
    return f'<p class=pb-state>Numbers the text can quote</p><ol class=vt-list>{items}</ol>' if items else ""


def _method(tab: dict, meta: dict, root: Path) -> str:
    """How this tab's tables are made (JL 261104): the steps from the source Runs, each source Run linked to its Task page."""
    steps = "".join(f"<li>{esc(x)}</li>" for x in tab.get("method") or [])
    runs = {m["path"]: m["run"] for m in meta.values() if m.get("path")}
    links = " · ".join(f'<a data-pop="{esc(p.rsplit("/", 1)[-1])}" href="/_board/workbench?path={quote(p.split("/runs/")[0])}&layout=focus">{esc(r)}</a>'
                       for p, r in runs.items())
    return (f'<details class=vt-how><summary>How this table is made</summary><ol class=vt-list>{steps}</ol><p class=vt-now></p>'
            + (f'<p class=vt-now-runs>Source Runs: {links}</p>' if links else "") + '</details>')


def value_tabs(job: Path, root: Path) -> list | None:
    """[(tab name, its line, its panel)] from the newest tables.json of a value Job, or None when it has none."""
    found = sorted(job.glob("t[0-9]*_*/runs/r[0-9]*/result/tables.json"))
    if not found:
        return None
    res = found[-1].parent
    built = found[-1].stat().st_mtime
    tabs = json.loads(found[-1].read_text(encoding="utf-8"))["tabs"]
    read_by, base = _read_by(job), "/" + quote(ds._rel(res, root)) + "/"
    values = _values(job)
    quotes = _section_quotes(job.parent, values)
    used, out = set(), []
    for i, tab in enumerate(tabs):
        meta = {}
        for t in tab["tables"]:
            frm = t["from"]
            if frm not in meta:
                st, why, run = source_status(res, frm, built, root)
                who = read_by.get("/".join(frm.split("/")[:2]), [])
                said = [q for vid, (task, v) in values.items() if task == frm.split("/")[0] and Path(frm).name in str(v.get("source", ""))
                        for q in quotes.get(vid, [])]
                meta[frm] = {"status": st, "why": why, "run": re.sub(r"(b\d+)_[^/]+/", r"\1 ", run.split("work/", 1)[-1].removesuffix("/result"), count=1), "path": run,
                             "figures": ", ".join(dict.fromkeys(who)), "sections": ", ".join(dict.fromkeys(said))}
        panel = (f'<div class=vt-panel data-title="{esc(tab["title"])}"><div class=vt-head><p class=vt-story>{esc(tab["story"])}</p>'
                 f'<button type=button class="fd-btn vt-popb" onclick="vtPop(this)">Pop out ↗</button></div>'
                 f'<div class=vt-tab data-i="{i}" data-url="{esc(base)}tables.json" data-base="{esc(base)}" '
                 f"data-meta='{esc(json.dumps(meta, ensure_ascii=False))}'><div class=vt-pick></div><p class=vt-axes></p><div class=vt-scroll>Loading the table…</div></div>"
                 + _method(tab, meta, root) + _value_lines(values, tab.get("values") or [], used) + '</div>')
        out.append((tab["title"], tab["line"], panel))
    return out


VALUES_DIALOG = ('<dialog class=vt-d onclick="if(event.target===this)this.close()"><form method=dialog><button class="fd-btn vt-x" '
                 'aria-label=Close>✕</button></form><div class=vt-b></div></dialog>')


def evidence_body(task: Path, root: Path):
    """(label, status, body) of one evidence Task: its picture or table, its values, its facts, its Open button."""
    md = face(task)
    text = md.read_text(encoding="utf-8", errors="ignore") if md else ""
    label, status = _field(text, "label"), _field(text, "status")
    url = lambda f: "/" + quote(ds._rel(f, root))
    body = ""
    ledger = ledger_file(task)
    if ledger is not None:                       # a value or citation Task: its Run's ledger page, tall, with a pop-out
        head = ledger.parent / "headline.txt"    # (haipipe-paper-evidence values_ledger.py, cite_tasks.py; JL 261103)
        line = head.read_text(encoding="utf-8", errors="ignore").strip().split(": ", 1)[-1] if head.is_file() else ""
        if line and (not status or status.startswith("see runs/")):
            status = line
        body += (f'<div class=pb-ptop style="flex-wrap:wrap"><span class=pb-state style="flex:1 1 220px;min-width:0">{esc(ledger.parent.parent.name)} · {esc(line)}</span>'
                 f'<a class=fd-btn data-pop="{esc(label or task.name)} · {esc(ledger.stem)}" href="{esc(url(ledger))}">⤢ Pop out</a>'
                 f'<a class=fd-btn target=_blank href="{esc(url(ledger))}">Open in a new tab ↗</a></div>'
                 f'<iframe src="{esc(url(ledger))}" loading=lazy title="{esc(label or task.name)}" style="width:100%;'
                 f'height:max(560px,78vh);border:1px solid var(--line);border-radius:6px;background:#fff"></iframe>')
        facts = [(k, _field(text, k)) for k in EV_FACTS if _field(text, k)]
        body += "".join(f'<div class=fd-row><span class=n>{esc(k)}</span><span class=d>{esc(v)}</span></div>' for k, v in facts)
        body += f'<p><a class=fd-btn href="{esc(_task_url(task, root))}">Open {esc(task.name)} ↗</a></p>'
        return label, status, body
    # a display's newest version shows as its preview.pdf, both pages: the display with its caption, then how it was
    # made (haipipe-display scripts/build_preview.py; JL 261101: "I want to make this to be things like the pdf")
    preview, forced = display_pick(task, text)
    shown = None if preview else (forced or _evidence_file(task, text))
    if preview is not None:
        body += (f'<div class=pb-ptop style="flex-wrap:wrap"><span class=pb-state style="flex:1 1 220px;min-width:0">{esc(preview.parent.parent.name)} · the display, then how it was made</span>'
                 f'<a class=fd-btn data-pop="{esc(label or task.name)} · preview" href="{esc(url(preview))}">⤢ Pop out</a></div>'
                 f'<iframe class=pb-pdf src="{esc(url(preview))}#view=FitH" loading=lazy title="{esc(label or task.name)}"></iframe>')
    if shown is not None:
        if shown.suffix == ".tex":               # a LaTeX table, shown as a table
            body += latex_table_html(shown.read_text(encoding="utf-8", errors="ignore"))
        elif shown.suffix.lower() in (".png", ".svg", ".jpg", ".jpeg"):
            body += (f'<a data-pop="{esc(task.name)}" href="{esc(url(shown))}"><img src="{esc(url(shown))}" alt="{esc(label)}" '
                     f'style="display:block;max-width:100%;max-height:440px;border:1px solid var(--line);border-radius:6px"></a>')
        else:
            body += (f'<iframe src="{esc(url(shown))}" loading=lazy title="{esc(label)}" style="width:100%;height:460px;'
                     f'border:1px solid var(--line);border-radius:6px;background:#fff"></iframe>')
        body += f'<p class=mut>{esc(shown.name)} · <a data-pop="{esc(task.name)}" href="{esc(url(shown))}">Open ↗</a></p>'
        # a work Run with several pictures (an Others candidate, JL 261102): show the rest too, so all can be compared
        res = next((p for p in shown.parents if p.name == "result"), None)
        more = [f for f in sorted(res.rglob("*.png")) if f != shown] if res is not None and not any(task.glob("runs/*/result")) else []
        for f in more:
            body += (f'<a data-pop="{esc(task.name)}" href="{esc(url(f))}"><img src="{esc(url(f))}" alt="{esc(f.name)}" loading=lazy '
                     f'style="display:block;max-width:100%;max-height:440px;margin-top:10px;border:1px solid var(--line);border-radius:6px"></a>'
                     f'<p class=mut>{esc(f.name)}</p>')
    values =re.search(r"(?ms)^## Values\s*\n(.*?)(?=^## |\Z)", text)
    if values:                                   # a value Task: each printed number and where it comes from
        items = re.findall(r"(?m)^- (.+)\n(?:\s+(.+)\n?)?", values.group(1))
        body += "<ol>" + "".join(f'<li>{esc(a)}' + (f'<br><span class=mut>{esc(b)}</span>' if b else '') + '</li>' for a, b in items) + "</ol>"
    papers = re.search(r"(?ms)^## Papers\s*\n(.*?)(?=^## |\Z)", text)
    if papers:                                   # a citation Task: each paper, its check, where the text cites it
        rows = [[c.strip() for c in ln[2:].split("·")] for ln in papers.group(1).splitlines() if ln.startswith("- ")]
        body += "".join(f'<div class=fd-row><span class=n>{esc(r[1] if len(r) > 1 else r[0])}</span><span class=d>{esc(r[3] if len(r) > 3 else "")}</span>'
                        f'<span class=w>{esc(r[2] if len(r) > 2 else "")}</span></div>' for r in rows)
        values = values or papers
    facts = [(k, _field(text, k)) for k in EV_FACTS if _field(text, k)]
    body += "".join(f'<div class=fd-row><span class=n>{esc(k)}</span><span class=d>{esc(v)}</span></div>' for k, v in facts)
    body += f'<p><a class=fd-btn href="{esc(_task_url(task, root))}">Open {esc(task.name)} ↗</a></p>'
    if shown is None and preview is None and not values:
        body = '<p class=mut>Not drawn yet.</p>' + body
    return label, status, body


def _tex_plain(s: str) -> str:
    s = re.sub(r"\\(?:textbf|textit|emph|mathrm|text)\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"\\(?:multicolumn|multirow)\{[^{}]*\}\{[^{}]*\}\{([^{}]*)\}", r"\1", s)
    s = s.replace(r"\%", "%").replace(r"\&", "&").replace("~", " ").replace("--", "–").replace(r"\,", " ")
    s = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?", "", s)
    return re.sub(r"[{}$]", "", s).strip()


def latex_table_html(tex: str) -> str:
    """A LaTeX table's caption and rows as a small HTML table, so a drawn table previews in place."""
    cap = re.search(r"\\caption\{(.*?)\}\s*\n", tex, re.S)
    body = re.search(r"\\begin\{tabular\}.*?\n(.*?)\\end\{tabular\}", tex, re.S)
    rows = []
    for line in re.split(r"\\\\", body.group(1) if body else ""):
        line = re.sub(r"\\(?:toprule|midrule|bottomrule|hline|cmidrule(?:\([^)]*\))?\{[^}]*\})", "", line).strip()
        if line and not line.startswith("%"):
            rows.append([_tex_plain(c) for c in line.split("&")])
    if not rows:
        return '<p class=mut>A LaTeX table with no rows read.</p>'
    head, rest = rows[0], rows[1:]
    return ((f'<p><b>{esc(_tex_plain(cap.group(1)))}</b></p>' if cap else '')
            + '<table style="border-collapse:collapse;font-size:13px;margin:0 0 8px"><tr>'
            + "".join(f'<th style="text-align:left;border-bottom:1px solid var(--line);padding:4px 8px">{esc(c)}</th>' for c in head)
            + "</tr>" + "".join("<tr>" + "".join(f'<td style="border-bottom:1px solid var(--line);padding:4px 8px;vertical-align:top">{esc(c)}</td>'
                                                 for c in r) + "</tr>" for r in rest) + "</table>")


def display_pick(task: Path, text: str) -> tuple:
    """A display Task's shown version, as (preview.pdf, None) or (None, a picture) or (None, None): the face's
    `printed: <run> [· <stem>]` wins over the newest alternative (JL 261101: Figure 1 showed its r02 alternative, Table
    1 an unprinted table1-patients); else the newest preview.pdf. The Evidence view and haipipe-paper-evidence
    build_displays_pdf.py both read it, so the all-displays PDF prints the version the paper prints (pp-LBP-JAMA 261103:
    t05 prints r07 but the PDF showed r08, its newest)."""
    previews = sorted(task.glob("runs/*/result/preview.pdf")) + sorted(task.glob("display/*/preview.pdf"))
    preview = previews[-1] if previews else None
    printed = re.match(r"(\S+)(?:\s*·\s*(\S+))?", _field(text, "printed") or "")
    if printed:
        res = task / "runs" / printed.group(1) / "result"
        pre = f"{printed.group(2)}-" if printed.group(2) else ""
        pick = next((f for f in (res / f"{pre}preview.pdf", res / f"{pre}preview.png") if f.is_file()), None)
        if pick is not None:
            return (pick, None) if pick.suffix == ".pdf" else (None, pick)
    return preview, None
