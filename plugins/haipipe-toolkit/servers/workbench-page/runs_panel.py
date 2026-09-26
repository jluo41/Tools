"""Runs beside the content (Page 0.118): one Runs panel per Space, plus a Page bar.

Each Space (Draft, Evidence, Delivery) shows its own runs under its content:
on the left the run types that the Run cards give that Space (`🔘 BUTTON` lines
in haipipe-page-workflow/ref/run-cards.md), on the right one run with its
prompt to copy, its process and its results. A selected paragraph or item
narrows the panel to that target. A panel folds to one line, and Focus hides
every panel so only the content shows.

The panel starts nothing by itself: Rerun and "+ New Run" copy a prompt the
person runs in a Claude or Codex session, which records who started it.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

from src.run_folders import folder_for, space_of

CARDS = Path(__file__).resolve().parents[2] / "skills" / "page" / "haipipe-page-workflow" / "ref" / "run-cards.md"
_CARD = re.compile(r"^## `(?P<card>[^`]+)`", re.M)
_BUTTON = re.compile(r"^🔘 BUTTON\s+(?P<label>.+?)\s+·\s+(?P<space>Draft|Evidence|Delivery|Page)\s+·\s+(?P<pattern>\S.*?)\s*$")
_PROMPT = re.compile(r"^💬 PROMPT\s+(?P<prompt>.+?)\s*$")
_STATE = {"done": "Closed", "held": "Held", "waiting": "Awaiting you", "running": "Running",
          "review-ready": "Awaiting you", "open": "Running"}


def _e(value) -> str:
    return html.escape(str(value or ""), quote=True)


def run_types(cards: Path = CARDS) -> list[dict]:
    """-> [{card, label, space, pattern, prompt}] from the Run cards, in card order."""
    try:
        text = cards.read_text(encoding="utf-8")
    except OSError:
        return []
    types = []
    for match in _CARD.finditer(text):
        end = text.find("\n## ", match.end())
        body = text[match.end():end if end >= 0 else len(text)]
        prompt = next((m["prompt"] for line in body.splitlines() if (m := _PROMPT.match(line))), "")
        for line in body.splitlines():
            button = _BUTTON.match(line)
            if button:
                types.append({"card": match["card"], "label": button["label"], "space": button["space"],
                              "pattern": button["pattern"], "prompt": prompt})
    return types


def _fill(template: str, **values) -> str:
    return re.sub(r"\{(\w+)\}", lambda m: str(values.get(m.group(1), m.group(0))), template or "")


def _ticket_name(row: dict) -> str:
    ticket = row.get("ticket")
    return Path(str(ticket)).name if ticket else str(row.get("global_id") or row.get("run_id") or "")


def _run_id(row: dict) -> str:
    return str(row.get("global_id") or row.get("run_id") or "").split(" ")[-1]


def row_space(row: dict) -> str:
    ticket = row.get("ticket")
    if ticket:
        return space_of(ticket)
    folder = folder_for(_run_id(row))
    return space_of("runs/%s/x" % folder) if folder else "other"


def _targets(row: dict) -> str:
    """Addresses and Evidence Item ids a run touches (C1.P1.B2 also adds C1.P1; E40)."""
    found = set(re.findall(r"C\d+(?:\.P\d+)?(?:\.B\d+)?", str(row.get("target") or "")))
    found |= {re.sub(r"\.B\d+$", "", t) for t in found}
    ticket = Path(str(row.get("ticket") or ""))
    if ticket.suffix == ".md" and ticket.is_file():
        head = ticket.read_text(encoding="utf-8", errors="replace")[:1500]
        for item in re.findall(r"(?m)^item:\s*(E\d+)(-[A-Z]+-[\w-]+)?", head):
            found |= {item[0], item[0] + item[1]}
    return " ".join(sorted(found))


def _number(row: dict) -> tuple:
    digits = re.findall(r"\d+", _run_id(row))
    return tuple(int(d) for d in digits[:1]) or (0,)


def _rel(path, base: Path) -> str:
    if not path:
        return ""
    try:
        return Path(str(path)).resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        return str(path)


def _result_files(row: dict) -> list[str]:
    folder = Path(str(row.get("result_path") or ""))
    if folder.is_file():
        folder = folder.parent
    if not folder.is_dir():
        return []
    return sorted(p.name for p in folder.iterdir() if p.is_file() and not p.name.startswith("."))[:8]


def _card_html(row: dict, index: int, kind: dict, base: Path, fill: dict) -> str:
    run = _run_id(row)
    state = _STATE.get(str(row.get("status") or "").lower(), str(row.get("status") or "unknown"))
    target = str(row.get("target") or "whole page")
    ticket = _rel(row.get("ticket"), base)
    result = str(row.get("result") or _rel(row.get("result_path"), base))
    folder = re.sub(r"/[^/]+\.(?:ya?ml|md|json)$", "", result)
    prompt = _fill(kind["prompt"], target=target, button=kind["label"], run=run, **fill)
    prompt = "%s\n\nContinue %s. Ticket: %s · Result: %s" % (prompt, run, ticket or "none", result or "none")
    rerun = "Rerun %s as a new %s run.\n%s" % (run, kind["label"], _fill(kind["prompt"], target=target,
                                                                       button=kind["label"], run=run, **fill))
    step = " · ".join(x for x in (row.get("version"), row.get("step")) if x)
    files = "".join("<li><code class=repo-path>%s</code></li>" % _e(f) for f in _result_files(row))
    return (
        '<article class=run-card data-type="%d" data-run="%s" data-targets="%s" data-state="%s" hidden>'
        '<header><b>%s</b><span class="run-state st-%s">%s</span>'
        '<button type=button class=run-copy data-copy="%s">Rerun</button></header>'
        '<div class=run-sub>%s%s</div>'
        '<h4>Prompt <button type=button class=run-copy data-copy="%s">Copy</button></h4>'
        '<pre class=run-prompt>%s</pre>'
        '<h4>Running process</h4><div class=run-process>%s%s</div>'
        '<h4>Results</h4><div class=run-results><code class=repo-path>%s</code><ul>%s</ul></div>'
        '</article>'
        % (index, _e(run), _e(_targets(row)), _e(state.lower().replace(" ", "-")),
           _e(run), _e(state.lower().replace(" ", "-")), _e(state), _e(rerun),
           _e(target), (" · " + _e(step)) if step else "", _e(prompt), _e(prompt),
           _e(state), (" · " + _e(row.get("goal"))) if row.get("goal") else "",
           _e(folder or "no result yet"), files))


def panel_html(page_src: Path, space: str, rows: list[dict], types: list[dict], *,
               plan_name: str, extra: str = "") -> str:
    """One Space's Runs panel: run types on the left, the selected run on the right."""
    base = page_src.parent
    fill = {"page": page_src.stem, "plan": plan_name}
    mine = [t for t in types if t["space"].lower() == space]
    rows = [r for r in rows if row_space(r) == space]
    buckets = [[] for _ in mine]
    other = []
    for row in sorted(rows, key=_number, reverse=True):
        name = _ticket_name(row)
        hit = next((i for i, t in enumerate(mine) if re.search(t["pattern"], name)), None)
        (buckets[hit] if hit is not None else other).append(row)
    kinds = list(mine)
    if other:
        kinds.append({"card": "", "label": "Other", "space": space, "pattern": "", "prompt":
                      "/haipipe-page run {page} {run} again: {target}."})
        buckets.append(other)
    def waiting_in(rows_):
        return sum(1 for r in rows_ if str(r.get("status") or "").lower() in ("waiting", "review-ready"))
    # Open on the type that has a run waiting for the person, else the busiest one.
    # "Other" (older names, unmatched tickets) is never the default.
    named = [i for i in range(len(buckets)) if i < len(mine)] or list(range(len(buckets)))
    first = max(named, key=lambda i: (waiting_in(buckets[i]), len(buckets[i])), default=0)
    buttons = "".join(
        '<button type=button class="run-type%s" data-type="%d" data-label="%s" data-prompt="%s">'
        '%s <span class=run-count>%d</span></button>'
        % (" on" if i == first else "", i, _e(k["label"]),
           _e(_fill(k["prompt"], button=k["label"], **fill)), _e(k["label"]), len(buckets[i]))
        for i, k in enumerate(kinds))
    cards = "".join(_card_html(row, i, kinds[i], base, fill)
                    for i, rows_ in enumerate(buckets) for row in rows_)
    waiting = sum(1 for r in rows if str(r.get("status") or "").lower() in ("waiting", "review-ready"))
    summary = ("%d run%s · %d waiting for you" % (len(rows), "s"[:len(rows) != 1], waiting)
               if rows else "no runs yet")
    return (
        '<section class=runs-panel data-space="%s" data-waiting="%d">'
        '<div class=runs-bar><button type=button class=runs-fold title="Fold or open (the Page bar Focus hides all)">▾</button>'
        '<b>Runs › %s</b><span class=runs-target>› whole page</span>'
        '<span class=runs-summary>%s</span>%s</div>'
        '<div class=runs-body><div class=runs-types>%s'
        '<button type=button class="run-type run-new">+ New Run</button></div>'
        '<div class=runs-detail><div class=run-list></div>%s'
        '<article class="run-card run-card-new" hidden><header><b>New run</b></header>'
        '<div class=run-sub>Copy this prompt into a Claude or Codex session to start it; '
        'the run records who started it.</div>'
        '<h4>Prompt <button type=button class=run-copy data-copy="">Copy</button></h4>'
        '<pre class=run-prompt></pre></article>'
        '<div class=run-empty hidden>No run of this type for this target yet. Use + New Run.</div>'
        '</div></div></section>'
        % (_e(space), waiting, _e(space.title()), _e(summary), extra, buttons, cards))


def page_bar_html(page_src: Path, types: list[dict], rows: list[dict], *, plan_name: str,
                  readiness: str) -> str:
    """The Page bar: plan and readiness, the Page-level runs, Focus, and waiting runs."""
    fill = {"page": page_src.stem, "plan": plan_name, "target": page_src.stem}
    page_runs = "".join(
        '<button type=button class=run-copy data-copy="%s" title="Copy the prompt">%s run</button>'
        % (_e(_fill(t["prompt"], button=t["label"], **fill)), _e(t["label"]))
        for t in types if t["space"] == "Page")
    waiting = sum(1 for r in rows if str(r.get("status") or "").lower() in ("waiting", "review-ready"))
    return (
        '<div class=pagebar><span class=pagebar-plan><code>%s</code></span>'
        '<span class=pagebar-ready>%s</span><span class=pagebar-actions>%s'
        '<button type=button class=pagebar-allruns>All runs</button>'
        '<button type=button class=pagebar-focus aria-pressed=false title="Hide every Runs panel (F)">Focus</button>'
        '<button type=button class=pagebar-badge%s>Runs · %d waiting</button></span></div>'
        % (_e(plan_name), _e(readiness), page_runs, "" if waiting else " hidden", waiting))


def readiness(page_src: Path) -> str:
    """One line from the folder health check: drafts on the Page, evidence, delivery."""
    try:
        from src.folder_health import folder_health
        report = folder_health(page_src)
    except Exception:  # the bar is a convenience; the page renders without it
        return ""
    parts = []
    for finding in report["findings"]:
        text = finding["message"]
        if finding["check"] == "sync":
            m = re.match(r"(\d+) of (\d+) Drafts equal", text)
            parts.append("Drafts on the Page %s/%s" % m.groups() if m else "Drafts: see health")
        elif finding["check"] == "evidence":
            m = re.match(r"(\d+) Evidence Item", text)
            parts.append("Evidence items %s%s" % (m.group(1) if m else "?",
                                                   "" if finding["level"] == "OK" else " (check)"))
        elif finding["check"] == "delivery":
            parts.append("Delivery stale")
    return " · ".join(parts)


PANEL_CSS = """
.pagebar{display:flex;flex-wrap:wrap;align-items:center;gap:8px 14px;margin:6px 0 12px;
 padding:8px 12px;border:1px solid var(--line);border-radius:10px;background:var(--card);
 font:12.5px/1.45 system-ui,sans-serif;color:var(--mut)}
.pagebar-plan code{color:var(--fg)}
.pagebar-actions{display:flex;gap:6px;margin-left:auto;flex-wrap:wrap}
.pagebar button,.runs-panel button{font:600 11.5px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
 border:1px solid var(--line);border-radius:7px;padding:3px 9px;cursor:pointer;background:var(--card);color:var(--fg)}
.pagebar-focus[aria-pressed=true],.run-type.on{border-color:var(--acc);color:var(--acc)}
.pagebar-badge{border-color:#2b8a3e!important;color:#2b8a3e!important}
.runs-panel{margin:14px 0 6px;border:1px solid var(--line);border-radius:10px;background:var(--card)}
.runs-bar{display:flex;align-items:center;gap:8px;padding:8px 12px;font:13px/1.4 system-ui,sans-serif}
.runs-bar .runs-fold{padding:0 7px}
.runs-target{color:var(--acc)} .runs-summary{margin-left:auto;color:var(--mut);font-size:12px}
.runs-panel[data-waiting]:not([data-waiting="0"]) .runs-summary{color:#2b8a3e}
.runs-filter{font:12px system-ui,sans-serif;padding:2px 6px;border:1px solid var(--line);border-radius:6px;width:150px}
.runs-body{display:grid;grid-template-columns:minmax(150px,210px) minmax(0,1fr);gap:12px;padding:0 12px 12px}
.runs-panel.folded .runs-body{display:none}
.runs-types{display:flex;flex-direction:column;gap:6px}
.run-type{text-align:left;display:flex;justify-content:space-between}
.run-type .run-count{color:var(--mut);font-weight:500}
.run-new{border-style:dashed!important}
.runs-detail{border:1px solid var(--line);border-radius:9px;padding:10px 12px;min-width:0}
.run-list{display:flex;flex-wrap:wrap;gap:4px;margin-bottom:8px}
.run-list button{font:500 11px ui-monospace,Menlo,monospace!important;padding:1px 6px!important}
.run-list button.on{border-color:var(--acc);color:var(--acc)}
.run-card header{display:flex;align-items:center;gap:8px}
.run-card header .run-copy{margin-left:auto}
.run-card h4{display:flex;align-items:center;justify-content:space-between;margin:10px 0 4px;
 font:600 12px system-ui,sans-serif}
.run-sub,.run-process{color:var(--mut);font-size:12px;line-height:1.5;overflow-wrap:anywhere}
.run-prompt{white-space:pre-wrap;overflow-wrap:anywhere;margin:0;padding:7px 9px;border-radius:7px;
 background:color-mix(in srgb,var(--acc) 6%,var(--card));font:12px/1.5 ui-monospace,Menlo,monospace}
.run-results ul{margin:4px 0 0;padding-left:18px;font-size:12px}
.run-state{font:600 10.5px/1.4 system-ui,sans-serif;border-radius:5px;padding:1px 6px;
 border:1px solid var(--line);color:var(--mut)}
.run-state.st-awaiting-you{color:#2b8a3e;border-color:#2b8a3e}
.run-state.st-running{color:var(--acc);border-color:var(--acc)}
.run-empty{color:var(--mut);font-size:12px}
.focus-runs .runs-panel{display:none}
.lens:has(.runs-panel:not(.folded)) .workspace-frame{height:calc(100vh - 470px)}
.focus-runs .lens .workspace-frame{height:calc(100vh - 170px)!important}
.paragraph-group.runs-selected>summary{outline:2px solid var(--acc);outline-offset:2px;border-radius:6px}
@media (max-width:700px){.runs-body{grid-template-columns:1fr}.pagebar-actions{margin-left:0}}
"""

PANEL_JS = r"""
(function(){
 function store(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v);}catch(e){return null;}}
 function copy(text,btn){
  function done(){var old=btn.textContent;btn.textContent='Copied';setTimeout(function(){btn.textContent=old;},1200);}
  if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(text).then(done,function(){fallback();});}
  else fallback();
  function fallback(){var t=document.createElement('textarea');t.value=text;document.body.appendChild(t);t.select();
   try{document.execCommand('copy');done();}catch(e){}document.body.removeChild(t);}
 }
 document.addEventListener('click',function(ev){
  var b=ev.target.closest('.run-copy');if(!b)return;
  var text=b.dataset.copy||'';
  if(!text){var pre=b.closest('.run-card')&&b.closest('.run-card').querySelector('.run-prompt');text=pre?pre.textContent:'';}
  copy(text,b);
 });
 function matches(card,target){
  if(!target)return true;
  var t=(card.dataset.targets||'').split(' ');
  return t.indexOf(target)>=0||t.some(function(x){return x.indexOf(target+'.')===0;});
 }
 function render(p){
  var on=p.querySelector('.run-type.on'),newMode=on&&on.classList.contains('run-new');
  var target=p.dataset.target||'',list=p.querySelector('.run-list');
  var type=newMode?p.dataset.lastType:(on?on.dataset.type:'0');
  var cards=[].slice.call(p.querySelectorAll('.run-card[data-type="'+type+'"]')).filter(function(c){return matches(c,target);});
  p.querySelectorAll('.run-card').forEach(function(c){c.hidden=true;});
  list.innerHTML='';p.querySelector('.run-empty').hidden=true;
  if(newMode){
   var src=p.querySelector('.run-type[data-type="'+type+'"]'),card=p.querySelector('.run-card-new');
   card.querySelector('.run-prompt').textContent=(src?src.dataset.prompt:'').replace(/\{target\}/g,target||'the whole page');
   card.hidden=false;return;
  }
  p.dataset.lastType=type;
  if(!cards.length){p.querySelector('.run-empty').hidden=false;return;}
  cards.forEach(function(c,i){var b=document.createElement('button');b.type='button';b.textContent=c.dataset.run;
   b.addEventListener('click',function(){cards.forEach(function(x){x.hidden=true;});c.hidden=false;
    list.querySelectorAll('button').forEach(function(x){x.classList.remove('on');});b.classList.add('on');});
   if(i===0)b.classList.add('on');list.appendChild(b);});
  cards[0].hidden=false;
 }
 function setTarget(p,target){p.dataset.target=target||'';
  p.querySelector('.runs-target').textContent='› '+(target||'whole page');render(p);}
 document.querySelectorAll('.runs-panel').forEach(function(p){
  var space=p.dataset.space,fold=p.querySelector('.runs-fold');
  function setFold(on){p.classList.toggle('folded',on);fold.textContent=on?'▸':'▾';store('runs-fold:'+space,on?'1':'0');}
  fold.addEventListener('click',function(){setFold(!p.classList.contains('folded'));});
  if(store('runs-fold:'+space)==='1')setFold(true);
  p.querySelectorAll('.run-type').forEach(function(b){b.addEventListener('click',function(){
   p.querySelectorAll('.run-type').forEach(function(x){x.classList.remove('on');});b.classList.add('on');render(p);});});
  var filter=p.querySelector('.runs-filter');
  if(filter)filter.addEventListener('input',function(){setTarget(p,filter.value.trim());});
  render(p);
 });
 var draft=document.querySelector('.runs-panel[data-space="draft"]');
 document.addEventListener('click',function(ev){
  if(!draft||ev.target.closest('.runs-panel,button,a,input,textarea,select,[contenteditable]'))return;
  var g=ev.target.closest('.paragraph-group[data-paragraph]');if(!g)return;
  var same=g.classList.contains('runs-selected');
  document.querySelectorAll('.paragraph-group.runs-selected').forEach(function(x){x.classList.remove('runs-selected');});
  if(!same)g.classList.add('runs-selected');
  var id=g.dataset.paragraph||'';setTarget(draft,same?'':id);
 });
 var focusBtn=document.querySelector('.pagebar-focus'),badge=document.querySelector('.pagebar-badge');
 function setFocus(on){document.body.classList.toggle('focus-runs',on);if(focusBtn)focusBtn.setAttribute('aria-pressed',on?'true':'false');store('runs-focus',on?'1':'0');}
 if(focusBtn)focusBtn.addEventListener('click',function(){setFocus(!document.body.classList.contains('focus-runs'));});
 if(badge)badge.addEventListener('click',function(){setFocus(false);});
 if(store('runs-focus')==='1')setFocus(true);
 document.addEventListener('keydown',function(ev){
  if(ev.key!=='f'&&ev.key!=='F')return;if(ev.metaKey||ev.ctrlKey||ev.altKey)return;
  if(ev.target.closest('input,textarea,select,[contenteditable]'))return;
  setFocus(!document.body.classList.contains('focus-runs'));
 });
 var all=document.querySelector('.pagebar-allruns');
 if(all)all.addEventListener('click',function(){if(typeof activateLens==='function')activateLens('run');});
})();
"""
