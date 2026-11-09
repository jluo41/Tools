"""🙋 Interaction, the last section of every Report and Work view of a Block, a Job or a Task (JL 261104: "could you try to
make this section at the bottom for each of the view? not matter for the block, or job or task"): the collection Runs at
the page or below, in one left list, each Run a folding group, waiting sets first and the newest first. The right side is
the Run's own built form in one frame, showing one card at a time, so its picks, its one Copy feedback and collect.py save
stay the form's, and a form already built needs no rebuild. Back and Next walk the questions, each tab's small line shows
its pick, ✓ once visited, and Copy feedback comes on the last question ("we can click the questions one by one, by next
--->"). There the Copy text box stays on screen: off https the copy needs it. A frame loads when its set first opens."""
from __future__ import annotations

import re
from pathlib import Path

from live.frame import _file_url, esc
from live.ui_parts import PB_CSS, WORD_CSS, _section, plural_word

LEVELS = ("Block", "Job", "Task")

INTERACTION_CSS = ("<style>.pb-ixfoot{margin:6px 0 0;font-size:11.5px;color:var(--muted)}.pb-thin .pb-item{padding:3px 9px;margin:0 0 1px}.pb-thin .pb-item b{font-size:13px;line-height:1.3}"
                   ".pb-thin .pb-item span{font-size:11.5px;line-height:1.3}.pb-ix{align-items:start}"
                   ".pb-ixset{margin:0 0 6px}.pb-ixset>summary{cursor:pointer;padding:3px 4px;font-size:13px;line-height:1.3}"
                   ".pb-ixset>summary small{display:block;margin-left:1.1em;font-size:11.5px;color:var(--muted)}"
                   ".pb-ixset.waits>summary small{color:light-dark(#b35c00,#ffc078)}"
                   ".pb-ixframe{display:block;width:100%;height:60vh;border:0;background:transparent}"
                   # the frame is as tall as its card and the page scrolls, so Copy feedback is never cut off inside a box
                   ".pb-side.pb-ix>.pb-read{max-height:none}.pb-side.pb-ix>.pb-read>.pb-panel:not([hidden]){overflow:visible}</style>")

INTERACTION_JS = """<script>(function(){
var RULE='.wrap{max-width:none;padding:0 0 8px}.wrap>.label,.wrap>h1,.wrap>.addr,.wrap>.lead{display:none}.card{display:none;margin:0 0 10px;border:0;padding:0}.card.pb-on{display:block}.send{padding:8px 0}'
 +'#pb-ixnav{display:flex;justify-content:space-between;gap:10px;margin:4px 0 10px}#pb-ixnav [hidden]{visibility:hidden;display:inline-block}body.pb-notlast .send,body.pb-notlast details.box{display:none}';
function root(b){return b.closest('.pb-ix');}
function frame(b){return root(b).querySelector('[data-ixpanel="'+b.dataset.ixset+'"] iframe');}
function doc(b){try{return frame(b).contentDocument;}catch(e){return null;}}
function fit(b){var f=frame(b),d=doc(b);if(!d||!d.body||!f.offsetWidth)return;f.style.height='0';f.style.height=d.documentElement.scrollHeight+'px';}
function tabs(b){return Array.prototype.slice.call(b.querySelectorAll('[data-ixq]'));}
function lines(b){var d=doc(b);if(!b.dataset.live||!d)return;b._seen=b._seen||{};
 tabs(b).forEach(function(x){var q=x.dataset.ixq,c=d.querySelector('input[name="'+q+'"]:checked'),s=x.querySelector('span'),w='waiting';
  if(c&&c.closest('label')){var l=c.closest('label').cloneNode(true),r=l.querySelector('.rec');if(r)r.remove();w=l.textContent.trim();}
  s.textContent=(b._seen[q]?'✓ ':'')+w;s.title=w;});}
function place(b){var d=doc(b),q=b._cur,all=tabs(b);if(!d||!d.getElementById(q))return;
 d.querySelectorAll('.card').forEach(function(c){c.classList.toggle('pb-on',c.id===q);});
 var i=all.findIndex(function(x){return x.dataset.ixq===q;}),back=d.getElementById('pb-back'),next=d.getElementById('pb-next');
 if(back){back.hidden=i===0;next.hidden=i===all.length-1;}
 d.body.classList.toggle('pb-notlast',i<all.length-1);lines(b);fit(b);}
function load(b){var f=frame(b);if(!f.getAttribute('src')&&f.dataset.src)f.src=f.dataset.src;}
function show(b,q){var w=root(b);load(b);b._seen=b._seen||{};if(b._cur&&b._cur!==q)b._seen[b._cur]=1;b._cur=q;
 w.querySelectorAll('.pb-ixset .pb-item.on').forEach(function(x){x.classList.remove('on');});
 var t=b.querySelector('[data-ixq="'+q+'"]');if(t)t.classList.add('on');
 w.querySelectorAll('[data-ixpanel]').forEach(function(p){p.hidden=p.dataset.ixpanel!==b.dataset.ixset;});
 place(b);w.scrollIntoView({block:'nearest'});}
function step(b,by){var all=tabs(b),i=all.findIndex(function(x){return x.dataset.ixq===b._cur;})+by;if(all[i])show(b,all[i].dataset.ixq);}
function ready(b){var d=doc(b);if(!d||!d.head||d.readyState==='loading')return;
 d.querySelectorAll('.card').forEach(function(c,i){if(!c.id)c.id='Q'+(i+1);});if(!d.getElementById(b._cur))return;
 if(!d.getElementById('pb-ix')){var s=d.createElement('style');s.id='pb-ix';s.textContent=RULE;d.head.appendChild(s);
  var nav=d.createElement('div');nav.id='pb-ixnav';nav.innerHTML='<button type=button class=quiet id=pb-back>← Back</button><button type=button id=pb-next>Next →</button>';
  var box=d.querySelector('details.box'),last=d.querySelector('.card:last-of-type');if(box)box.parentNode.insertBefore(nav,box);else last.parentNode.insertBefore(nav,last.nextSibling);
  d.getElementById('pb-back').addEventListener('click',function(){step(b,-1);});d.getElementById('pb-next').addEventListener('click',function(){step(b,1);});
  d.addEventListener('change',function(){lines(b);});
  d.addEventListener('click',function(){setTimeout(function(){lines(b);fit(b);},60);});
  d.addEventListener('toggle',function(){fit(b);},true);}
 place(b);}
document.addEventListener('click',function(e){if(!e.target.closest)return;var t=e.target.closest('[data-ixq]');if(t){show(t.closest('.pb-ixset'),t.dataset.ixq);return;}
 var m=e.target.closest('.pb-ixset>summary');if(m&&!m.parentNode.open)show(m.parentNode,m.parentNode._cur);});
function start(){var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting)e.target.querySelectorAll('.pb-ixset').forEach(function(b){fit(b);});});});
 document.querySelectorAll('.pb-ix').forEach(function(w){w.querySelectorAll('.pb-ixset').forEach(function(b){b._cur=tabs(b)[0].dataset.ixq;var f=frame(b);f.addEventListener('load',function(){ready(b);});ready(b);});o.observe(w);});}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();
})();</script>"""


def _saved_answers(path) -> dict:
    """{QN: the answer's words} from a Run's result/answer_collection.md, for each left tab's small line."""
    if path is None:
        return {}
    blocks = re.split(r"(?m)^## (Q\d+) · ", path.read_text(encoding="utf-8", errors="ignore").split("\nThe pasted", 1)[0])
    out = {}
    for q, block in zip(blocks[1::2], blocks[2::2]):
        ticked = re.search(r"(?m)^- \[x\] (.+)$", block)
        out[q] = "my own decision" if "Answer: my own decision" in block else (ticked[1] if ticked else "none picked")
    return out


def _interaction_set(r: dict, k: int, root: Path, foot=None) -> tuple:
    """One collection Run: (its folding group of question tabs for the left, its form for the right). Waiting sets open,
    answered ones folded; the first set shows. Next stops at a set's end, as each Run is saved on its own."""
    waits = r["state"] == "waiting"
    said = _saved_answers(r["answers"])
    rows = ""
    for i, (q, title, _) in enumerate(r["asks"]):
        mark = r["applied"].get(q)
        line = said.get(q) or ("waiting" if waits else r["state"])
        line = (("✅ applied · " if mark[0] == "applied" else "⏳ in progress · ") + line) if mark else line
        rows += (f'<button type=button class="pb-item{" on" if i == 0 and k == 0 else ""}" data-ixq="{esc(q)}"><b>{"" if r["state"] == "to know" else esc(q) + " · "}{esc(title)}</b>'
                 f'<span title="{esc(line)}">{esc(line)}</span></button>')
    state = "waiting for you" if waits else r["state"]
    group = (f'<details class="pb-ixset{" waits" if waits else ""}" data-ixset="{k}"{" data-live=1" if waits else ""}{" open" if waits or k == 0 else ""}>'
             f'<summary><b>{esc(r["title"])}</b><small>{esc(state)}</small></summary>{rows}</details>')
    panel = (f'<div class=pb-panel data-ixpanel="{k}"{"" if k == 0 else " hidden"}>'
             f'<iframe class=pb-ixframe title="{esc(r["title"])}" {"src" if k == 0 else "data-src"}="{esc(_file_url(r["form"], root))}"></iframe>'
             + (f'<p class=pb-ixfoot>{foot(r)}</p>' if foot else "") + "</div>")
    return group, panel


# the same folding row a paper or draft page gives its sections, on a page that has no such look of its own (JL 261104: "you
# might make this to be like this style as well"): closed at first, what you open stays open in this browser
FOLD = """<style>.pb-ixsec{margin:12px 0}.pb-ixsec>.fd-h{font-size:15px;font-weight:600;margin:0;display:flex;align-items:center;gap:8px;
border:1px solid var(--line);border-radius:8px;background:var(--paper);padding:8px 14px;cursor:pointer;user-select:none}
.pb-ixsec>.fd-h::before{content:"▾";flex:none;display:inline-block;width:16px;font-size:10px;color:var(--muted)}
.pb-ixsec>.fd-h[aria-expanded="false"]::before{content:"▸"}.pb-ixsec>.fd-body{margin:10px 0 18px}.pb-ixsec>.fd-body[hidden]{display:none}</style>""" + WORD_CSS + """
<script>document.addEventListener('DOMContentLoaded',function(){setTimeout(function(){
var s=document.querySelector('section.pb-ixsec'),h=s&&s.querySelector(':scope>h3.fd-h');if(!h||h.dataset.fold)return;
var p=new URLSearchParams(location.search),at='fd-fold:'+(p.get('path')||'')+':'+(p.get('section')||'')+':'+(p.get('group')||''),shut={};
try{shut=JSON.parse(localStorage.getItem(at)||'{}');}catch(e){}
var b=document.createElement('div');b.className='fd-body';for(var n=h.nextSibling,x;n;n=x){x=n.nextSibling;if(!(n.classList&&n.classList.contains('fd-wait')))b.appendChild(n);}s.appendChild(b);
var c=h.cloneNode(true);c.querySelectorAll('.word').forEach(function(w){w.remove();});var k=c.textContent.trim().slice(0,80);h.dataset.fold='1';h.tabIndex=0;h.setAttribute('role','button');
function set(o){b.hidden=!o;h.setAttribute('aria-expanded',String(o));}set(k in shut?!shut[k]:false);
function flip(){var o=b.hidden;set(o);shut[k]=o?0:1;try{localStorage.setItem(at,JSON.stringify(shut));}catch(e){}window.dispatchEvent(new Event('resize'));}
h.addEventListener('click',function(e){if(e.target.closest('a,button'))return;flip();});h.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();flip();}});
},0);});</script>"""

NONE_YET = '<p class=mut>Nothing asked yet.</p>'   # one plain line; how a form is made lives in haipipe-interaction (261105:
                                                    # every reviewer read the old how-to sentence as an instruction paragraph)


def view_section(rows: list, root: Path, n: int = 0, foot=None) -> str:
    """The section a view always ends in, empty or not, so it stands in one place on every page (JL 261104: "make this to
    be the standard items for any of them"; "I still didn't see them here"). `rows` are this view's own items (JL
    261106: "a view's bottom section shows that view's own items"); the rail's Interactions keeps every item."""
    html = interaction_section(rows, root, n, foot) or _section((f"{n} · " if n else "") + "🙋 Interaction", NONE_YET,
                                                                "nothing yet")
    return html.replace("<section class=fd-sec>", '<section class="fd-sec pb-ixsec">', 1) + FOLD


def next_number(body: str) -> int:
    """The next number after the view's last band's numbered sections, 0 when its sections carry none. A band starts at
    a paper page's `pb-group` heading or a work page's `wk-band` one; a section is numbered in its `fd-h` heading
    (paper) or in its fold's `<summary>` (a work page's band-sec), so Interaction is numbered on both (261105)."""
    last = re.split(r"<h3 class=(?:pb-group|wk-band)>", body)[-1]
    found = [int(a or b) for a, b in re.findall(r"<h3 class=fd-h>(\d+) · |<details class=\"?band-sec[^>]*><summary>(\d+) · ", last)]
    return max(found) + 1 if found else 0


def state_word(rows: list) -> tuple:
    """(state word, waiting line) of these interactions: how many questions wait for you and the first of them (its
    form's title, then the question), else whether they are answered, not sent yet or there to read (JL 261106: "every
    closed bar shows a state word", "a section that waits on you also shows that one item under its closed bar")."""
    waiting = [r for r in rows if r.get("state") == "waiting"]
    if waiting:
        open_ = [(r, q) for r in waiting for q in r.get("asks") or [] if not r.get("applied", {}).get(q[0])]
        count = len(open_) or len(waiting)
        first = open_[0] if open_ else (waiting[0], None)
        line = f'🙋 {first[0]["title"]}' + (f": {first[1][0]} · {first[1][1]}" if first[1] else "")
        return f'{count} wait{"s" if count == 1 else ""} for you', line
    states = {r.get("state") for r in rows}
    if states <= {"answered"}:
        return "answered", ""
    if "planned" in states:
        return "not sent yet", ""
    if states <= {"to know", "answered"}:
        return plural_word(sum(r.get("state") == "to know" for r in rows), "note to read", "notes to read"), ""
    return "", ""


PLAIN_CSS = ("<style>.pb-ixplain{list-style:none;margin:6px 0 0;padding:0;font-size:14px}.pb-ixplain li{display:flex;flex-wrap:wrap;"
             "align-items:baseline;gap:4px 10px;padding:6px 2px;border-bottom:1px solid var(--line)}.pb-ixplain li:last-child{border-bottom:0}"
             ".pb-ixplain small{color:var(--muted);font-size:12px}.pb-ixplain a{margin-left:auto;font-size:13px}</style>")


def _plain_row(r: dict, root: Path) -> str:
    """A set with no question cards to step through (no built form, or a form without `## QN` cards): its title, its
    state and one link, its form or what it has, so it is never dropped (round 2, 261106)."""
    run = r.get("path")
    kept = [r.get("form"), r.get("answers")] + ([Path(run) / "question_collection.md"] if run else [])
    target = next((f for f in kept if f is not None and Path(f).is_file()), None)
    verb = "Answer ↗" if r.get("state") == "waiting" and r.get("form") is not None else "Open ↗"
    state = "waiting for you" if r.get("state") == "waiting" else str(r.get("state") or "")
    return (f'<li><b>{esc(r.get("title") or r.get("run") or "")}</b><small>{esc(state)}</small>'
            + (f'<a data-pop="{esc(r.get("title") or "")}" href="{esc(_file_url(Path(target), root))}" target=_blank '
               f'rel=noopener>{verb}</a>' if target is not None else '') + '</li>')


def interaction_section(rows: list, root: Path, n: int = 0, foot=None, plain: bool = True, title: str = "🙋 Interaction", *, body_only=False) -> str:
    """The section for these interactions (focus_page.interactions); nothing to ask or show, no section. A set still
    waiting says so in the bar's state word, as it flags the Interaction button, and its first question shows under the
    closed bar. A set with no question cards shows as one plain row (`plain`; the rail draws its own fuller row)."""
    full = [r for r in rows if r.get("form") is not None and r.get("asks")]
    rest = [r for r in rows if r not in full] if plain else []
    if not full and not rest:
        return ""
    full = sorted(sorted(full, key=lambda r: r["run"], reverse=True), key=lambda r: r["state"] != "waiting")
    rest = sorted(sorted(rest, key=lambda r: r.get("run", ""), reverse=True), key=lambda r: r.get("state") != "waiting")
    word, waits = state_word(full + rest)
    sets = [_interaction_set(r, k, root, foot) for k, r in enumerate(full)]
    body = (PB_CSS + INTERACTION_CSS + f'<div class="pb-side pb-thin pb-ix"><div class=pb-list>{"".join(g for g, _ in sets)}</div>'
            + f'<div class=pb-read>{"".join(p for _, p in sets)}</div></div>' + INTERACTION_JS) if full else ""
    if rest:
        body += PLAIN_CSS + '<ul class=pb-ixplain>' + "".join(_plain_row(r, root) for r in rest) + '</ul>'
    return body if body_only else _section((f"{n} · " if n else "") + title, body, word, waits)
