"""Shared HTML pieces of the work pages: links, cards, tree nodes, Run marks, tables, and the page scripts."""
from collections import Counter
import re
from urllib.parse import urlencode, quote

from live import frame
from live.work_progress_records import (
    e, STATE, state_of,
)


TICKS = {"done": "✅", "running": "🏃", "failed": "❌", "partly": "🔶", "todo": "⬜"}


TREE_CSS = """<style>
.dtree,.dtree ul{list-style:none;margin:0;padding-left:22px}
.dtree{padding-left:6px;margin:8px 0 4px}
.dtree li{position:relative;padding:2px 0 2px 22px;line-height:1.5}
.dtree>li{padding-top:5px}
.dtree>li::after{top:17px}
.dtree>li:last-child::before{height:17px}
.dtree details{margin:0}
.dtree li::before{content:"";position:absolute;left:0;top:0;bottom:0;border-left:1.5px solid var(--tab-line,#ced4da)}
.dtree li:last-child::before{bottom:auto;height:14px}
.dtree li::after{content:"";position:absolute;left:0;top:14px;width:17px;border-top:1.5px solid var(--tab-line,#ced4da)}
.dtree summary{list-style:none;cursor:pointer;border-radius:6px;padding:1px 4px;margin-left:-4px}
.dtree summary:hover{background:rgba(127,127,127,.08)}
.dtree summary::-webkit-details-marker{display:none}
.dtree summary::before{content:"▸";color:var(--mut,#6f6f6b);display:inline-block;width:14px}
.dtree details[open]>summary::before{content:"▾"}
.dtree .lvl{font-weight:650}
.dtree .job{font-size:15.5px}
.dtree .chip{display:inline-block;font-size:11.5px;line-height:18px;padding:0 8px;border-radius:9px;background:var(--wash,#f6f6f7);border:1px solid var(--line,#e3e3e6);color:var(--mut,#6f6f6b);margin-left:10px;vertical-align:1px}
.dtree .chip.ok{color:var(--ok,#24733d)}
.dtree .chip.part{color:var(--warn,#996b00)}
.dtree .chip.todo{background:transparent;border-style:dashed}
.dtree .m{color:var(--mut,#6f6f6b);font-size:12.5px;margin-left:10px}
.dtree .means{color:var(--fg,#1c1c1c);font-size:13px;margin:0 0 4px}
.dtree .box .lead{font-size:15px;line-height:1.6;margin:2px 0 12px;max-width:820px}   /* what the item is, read first (JL 261021) */
.dtree .box ul.means{list-style:disc;padding-left:22px}
.dtree .box ul.means li{padding:1px 0;line-height:1.55}
.dtree .box ul.means li::before,.dtree .box ul.means li::after{display:none}
.dtree .box{margin:4px 0 4px 21px;padding:6px 12px 6px 14px;border-left:3px solid var(--line,#e3e3e6);font-size:12.5px;color:var(--mut,#6f6f6b);max-width:980px}
.dtree .box h5{margin:6px 0 2px;font-size:12px;color:var(--fg,#1c1c1c);font-weight:650}
.dtree .box h5:first-child{margin-top:0}
.dtree .box .f{margin-left:20px}
.dtree .box details{margin:2px 0}
.dtree .box details>summary{margin-left:0}
.dtree .box details>:not(summary){margin-left:18px}
.dtree .hollow{display:inline-block;width:18px;text-align:center;color:var(--mut,#6f6f6b)}
.dtree-tools{display:inline-flex;margin:8px 0 2px;border:1px solid var(--line,#e3e3e6);border-radius:999px;overflow:hidden;background:var(--card,#fff)}
.dtree-tools button{all:unset;cursor:pointer;font-size:12.5px;line-height:22px;padding:0 12px;color:var(--mut,#6f6f6b)}
.dtree-tools button+button{border-left:1px solid var(--line,#e3e3e6)}
.dtree-tools button:hover{background:var(--tab-wash,#e7f5ff);color:var(--tab-on,#1864ab)}
</style>"""
TREE_TOOLS = ('<div><span class=dtree-tools><button type=button title="Open every Job and Task" onclick="this.closest(\'.dtree-wrap\')'
              '.querySelectorAll(\'details.branch\').forEach(d=>d.open=true)">▾ Open all</button><button type=button '
              'title="Fold every Job, Task and item" onclick="this.closest(\'.dtree-wrap\').querySelectorAll(\'details\')'
              '.forEach(d=>d.open=false)">▸ Fold all</button></span></div>')


def mark(state):
    """An item's mark: done, partly, running, failed; an item not started is an empty box marked todo (JL 261020:
    "如果是没完成的，就变成一个中括号 ... todo、plan 之类的")."""
    return '<span class=hollow>☐</span>' if state == "todo" else TICKS[state]


def chip(state, text):
    kind = {"done": "ok", "todo": "todo"}.get(state, "part")
    return f'<span class="chip {kind}">{e(text)}</span>'


def run_mark(row):
    """A Run's own mark (JL 261020: "这些 run 应该也要有不同的状态或者标识"): ✅ finished; 🔶 finished with searches
    unanswered or its gate missed; a receipt rebuilt from the Run's files counts the same as one its ticket wrote."""
    state = state_of(row)
    rec = row["receipt"]
    out = rec.get("outcome") if isinstance(rec.get("outcome"), dict) else {}
    asked, answered = out.get("searches_asked"), out.get("searches_answered")
    counted = f"{answered:,} of {asked:,} answered" if isinstance(asked, int) and isinstance(answered, int) else ""
    if not counted and isinstance(rec.get("expected_rows"), int) and isinstance(rec.get("stored_rows"), int):
        asked, answered = rec["expected_rows"], rec["stored_rows"]          # a CallStore receipt (bind_callstore_receipts.py)
        counted = f"{answered:,} of {asked:,} stored" + (f", audit {rec['audit_verdict']}" if rec.get("audit_verdict") else "")
    gate = str(rec.get("gate") or "")
    if state == "finished":
        if gate.startswith("missed"):
            return "🔶 finished, gate " + gate + (f"; {counted}" if counted else "")
        if counted and answered < asked:
            return f"🔶 finished, {counted}"
        return "✅ finished" + (f", {counted}" if counted and rec.get("audit_verdict") else "")
    if state == "partial":
        return "🔶 partial" + (f", {counted}" if counted else "")
    if state == "blocked" and isinstance(rec.get("repair"), dict):
        return f"📦 ran {str(rec['repair'].get('newest_file_at') or '')[:10]}, no receipt"
    return {"running": "🏃 running", "failed": "❌ failed", "blocked": "⛔ blocked", "waiting": "◌ planned"}.get(state, "⚪ no record")


def means_html(means, cls="means"):
    """What an item or batch is: a list is bullets, one short point each (JL 261021: "这里可以用 bullet points 吗"); a
    sentence stays one paragraph."""
    if isinstance(means, list):
        return f'<ul class="{cls}">' + "".join(f"<li>{e(str(x))}</li>" for x in means) + "</ul>"
    return f'<div class="{cls}">{e(str(means))}</div>'


def node(head, kids="", key="", body="", open_=False, below=""):
    """One branch of the Goal tree, a folder structure (JL 261020: "像 folder 那种 structure 的 mind map"; "could I
    collapse them"): a Job or Task folds its children; a deliverable folds its details. Everything starts folded (JL
    261021: "could you make the fold all to be default?"); what a reader opens stays open across a refresh."""
    inner = (f"<ul>{kids}</ul>" if kids else "") + (f"<div class=box>{body}</div>" if body else "")
    summary = head + (f"<div class=means>{below}</div>" if below else "")
    if not inner:
        return f"<li>{summary}</li>"
    kind = "branch" if kids else "leaf"
    return (f'<li><details class={kind}{" open" if open_ else ""} data-work-key="{e(key)}"><summary>{summary}</summary>'
            f"{inner}</details></li>")


def address(row, root):
    chain = frame.chain(row["task"], root)
    return " / ".join([chain[k].name for k in ("Block", "Job", "Task") if k in chain] + [row["run"]])


def run_link(row, root):
    url = frame.ROUTE + "?" + urlencode({"view": "work-run", "path": frame.rel(row["task"], root), "run": row["run"]})
    return frame.pop(url, address(row, root), row["run"])


def nav(folder, root, mode, view, label):
    url = frame.ROUTE + "?" + urlencode({"path": frame.rel(folder, root), "space": mode, "sub": view})
    return frame.link(url, label)


def source_link(path, root, label=None):
    if not path or not path.is_file() or not path.resolve().is_relative_to(root.resolve()):
        return ""
    rel = frame.rel(path, root)
    url = frame.reader(path, root) if path.suffix == ".md" else "/" + "/".join(quote(p) for p in rel.split("/"))
    return frame.pop(url, label or rel, label or path.name)


def counts(rows):
    """Runs by state, five words with their icons ("complete" and "completed" are one), then any without a record."""
    tally = Counter(state_of(r) for r in rows)
    icon = {k: l.split(" ")[0] for k, l, _ in STATE}
    out = [f"{icon[k]} {tally[k]}" for k, _, _ in STATE if tally[k]]
    return " · ".join(out + ([f"no record {tally['no record']}"] if tally["no record"] else [])) or "no Runs yet"


def runs_n(n):
    return f"{n} Run" + ("" if n == 1 else "s")


def part(name):
    """A part of a view, as the Draft page parts its tabs: Operation over Result (draft_steps._part)."""
    return f'<h3 style="margin:18px 0 6px">{e(name)}</h3>'


def card(title, body, tag="", open_=False, key=""):
    """A folded card, as the Draft page's (draft_steps._fold): an emoji title, a small grey tag, the body opened."""
    return (f'<details class="topic work-task"{" open" if open_ else ""}' + (f' data-work-key="{e(key)}"' if key else "")
            + f'><summary><span class=related-head><b>{e(title)}</b>'
            + (f' <span class=mut style="font-weight:400;font-size:12.5px">{e(tag)}</span>' if tag else "")
            + f'</span></summary><div class=work-body>{body}</div></details>')


RUN_MARKS = ("✅", "🔶", "🏃", "❌", "📦", "⛔", "◌", "⚪")
RUN_LEGEND = ("<p class=mut style='font-size:12px'>✅ finished · 🔶 finished, some searches unanswered or its gate missed · "
              "🏃 running · ❌ failed · 📦 ran, no receipt · ⛔ blocked · ◌ planned · ⚪ no record. From each Run's receipt "
              "(runtime.yaml), else its card; an old Run's receipt is rebuilt from the files it left (work/_tools/"
              "rebuild_receipts.py). A finished Run is not the goal accepted.</p>")


RUN_WORDS = {"✅": "finished", "🔶": "finished with gaps", "🏃": "running", "❌": "failed", "📦": "ran, no receipt",
             "⛔": "blocked", "◌": "planned", "⚪": "no record"}
RUN_URGENCY = ("❌", "⛔", "🏃", "🔶", "📦", "◌", "⚪", "✅")   # the word a group of Runs shows: its most pressing one


def run_tally(rows):
    """One state word for a group of Runs, its most pressing mark ("🏃 running", "✅ finished"), never a count: a page
    carries no tally (AGENTS.md Page words, JL 261113); each Run shows its own mark where it sits."""
    marks = {run_mark(r).split(" ")[0] for r in rows}
    m = next((m for m in RUN_URGENCY if m in marks), "")
    return f"{m} {RUN_WORDS[m]}" if m else ""


# A picture opens over the page, not in a new tab (JL 261023: "pop out, not a new link"). One listener on the document,
# so it keeps working after the 20-second refresh swaps the section; Cmd/Ctrl-click still opens the file in a tab.
ZOOM = """<style>.wz-pop{position:fixed;inset:0;z-index:9999;background:rgba(20,20,20,.82);display:flex;align-items:center;
justify-content:center;cursor:zoom-out}.wz-pop img{max-width:96vw;max-height:94vh;background:#fff;box-shadow:0 6px 30px #0008;
border-radius:4px}.workflow-view img,figure img,a[href$='.png'] img{cursor:zoom-in}</style><script>(function(){
if(window.__wzPop)return;window.__wzPop=1;const pic=/\\.(png|jpe?g|gif|svg|webp)(\\?|#|$)/i;
document.addEventListener('click',ev=>{
 const img=ev.target.closest&&ev.target.closest('img');if(!img||img.closest('.wz-pop'))return;
 if(ev.metaKey||ev.ctrlKey||ev.shiftKey||ev.button)return;
 const a=img.closest('a'),href=a?a.getAttribute('href')||'':'';
 if(a?!pic.test(href):!img.closest('.workflow-view,figure'))return;
 ev.preventDefault();const box=document.createElement('div');box.className='wz-pop';
 const big=document.createElement('img');big.src=a?a.href:img.src;big.alt=img.alt;box.appendChild(big);
 const close=()=>{box.remove();document.removeEventListener('keydown',key)};
 const key=e=>{if(e.key==='Escape')close()};box.addEventListener('click',close);document.addEventListener('keydown',key);
 document.body.appendChild(box);
});})();</script>"""


REFRESH = """<script>(function(){
let timer;const selector='[data-work-progress]';
async function refresh(){
 if(document.hidden){timer=setTimeout(refresh,20000);return;}
 const current=document.querySelector(selector);if(!current)return;
 if(current.contains(document.activeElement)&&/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)){
  timer=setTimeout(refresh,20000);return;}
 const opened=[...current.querySelectorAll('details[open][data-work-key]')].map(el=>el.dataset.workKey);
 try{const response=await fetch(location.href,{cache:'no-store'});if(!response.ok)throw Error();
  const doc=new DOMParser().parseFromString(await response.text(),'text/html');const next=doc.querySelector(selector);
  if(!next)throw Error();next.querySelectorAll('details[data-work-key]').forEach(el=>el.open=opened.includes(el.dataset.workKey));
  current.replaceWith(next);
 }catch(err){const status=current.querySelector('[data-work-refresh]');if(status)status.textContent='Refresh failed; showing the last records';}
 timer=setTimeout(refresh,20000);
}
timer=setTimeout(refresh,20000);window.addEventListener('pagehide',()=>clearTimeout(timer),{once:true});
})();</script>"""


IMAGES = (".png", ".jpg", ".jpeg", ".svg", ".gif", ".webp")
TEXTS = (".json", ".yaml", ".yml", ".txt")


def file_url(path, root):
    return "/" + "/".join(quote(part) for part in frame.rel(path, root).split("/"))


def csv_preview(path, n=12):
    """A CSV's first rows as a table, and how big it is (JL 261021: "why I cannot do the preview of the csv")."""
    import csv
    import itertools
    try:
        with path.open(newline="", encoding="utf-8", errors="replace") as fh:
            rows = list(itertools.islice(csv.reader(fh), n + 1))
        total = sum(1 for _ in path.open(encoding="utf-8", errors="replace")) - 1 if path.stat().st_size < 30_000_000 else None
    except (OSError, csv.Error):
        return 0, 0, "<p class=mut>Could not read this file.</p>"
    if not rows:
        return 0, 0, "<p class=mut>Empty file.</p>"
    return total, len(rows[0]), rows_table(rows[0], rows[1:])


CSVP_CSS = ("<style>.csvp-wrap{overflow-x:auto;margin:4px 0 10px}"
            ".csvp{margin:0;width:auto}.csvp th,.csvp td{white-space:nowrap;padding:4px 10px;font-size:12.5px}"
            ".csvp th{position:sticky;top:0;background:var(--wash)}.csvp tr:nth-child(even) td{background:var(--wash)}"
            ".dossier{color:var(--fg);font-size:13px;line-height:1.5}.dossier h1{font-size:17px;margin:0 0 6px}"
            ".dossier h2{font-size:14px;margin:12px 0 4px}.dossier ul{margin:2px 0 6px;padding-left:18px;list-style:disc}"
            ".dtree .dossier li{padding:0;line-height:1.5}.dtree .dossier li::before,.dtree .dossier li::after{display:none}</style>")
NUMBER = re.compile(r"^-?[\d,]*\.?\d+(e-?\d+)?%?$")


def rows_table(header, rows):
    """A table that reads: one line per cell, a long value cut with its whole text on hover, numbers to the right
    (JL 261021: "things here is so hard to read")."""
    def cell(v, tag="td"):
        v = "" if v is None else str(v)
        short = v if len(v) <= 48 else v[:45] + "…"
        right = ' style="text-align:right"' if tag == "td" and NUMBER.match(v.strip() or "x") else ""
        return f'<{tag}{right} title="{e(v)}">{e(short)}</{tag}>'
    head = "".join(cell(h, "th") for h in header)
    body = "".join("<tr>" + "".join(cell(v) for v in r) + "</tr>" for r in rows)
    return f'<div class=csvp-wrap><table class="wf-table csvp"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'
