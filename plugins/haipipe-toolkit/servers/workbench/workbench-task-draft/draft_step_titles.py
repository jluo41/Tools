"""Each part title (C4) and paragraph title (C4.P8) carries its own ★, rated and settled like a sentence
(haipipe-paper-draft CONSTITUTION A02; JL 261118: "for the section name, it should be trated as the setneces bricks as
well, we should also need to evaluat ehem as well"). The review report's `Titles:` block, before `Sentences:`:

    Titles:
    - C4 · title 7/10 · register 8 · first-read 7 · names 7 · <why> · AI decided: … · Fix: none | <new title>

becomes one hidden card per title; the page's script (TITLE_JS) puts a ★ after the heading and opens the card under it
on a click. The ★ is tinted as a sentence's is: under 7 low, 7 mid, 8 and up quiet."""
from __future__ import annotations

import re

from live.frame import esc

LINE = re.compile(r"(?m)^- (C\d+(?:\.P\d+)?) · (?:title )?(\d+(?:\.\d+)?)/10 · (.*)$")
AXIS = re.compile(r"^([a-z][a-z-]*) (\d+(?:\.\d+)?)(?:/10)?(?: \([^)]*\))?$")


def _block(body: str, name: str) -> str:
    """The lines of one report block (`Titles:`, `Paragraphs:`), up to the next block or the end."""
    sec = body.partition(f"\n{name}:")[2]
    end = re.search(r"(?m)^(?:Titles|Paragraphs|Sentences|Flow [^\n]*):", sec)
    return sec[:end.start()] if end else sec


def score_lines(body: str, name: str = "Titles") -> list:
    """[{t, score, axes, why, decided, fix}] from a report's `Titles:` or `Paragraphs:` block: after the score, each
    `· <axis> <n>` part is an axis, `AI decided: …` or `asked in Comment N` the decision, `Fix: …` the suggestion."""
    out = []
    for m in LINE.finditer(_block(body, name)):
        rest, _, fix = m.group(3).partition(" · Fix: ")
        axes, why, decided = [], [], ""
        for part in rest.split(" · "):
            part = part.strip()
            if AXIS.match(part):
                axes.append(part)
            elif part.startswith("AI decided:") or re.match(r"asked in Comment \d+", part):
                decided = part.removeprefix("AI decided:").strip()
            elif part:
                why.append(part)
        out.append({"t": m.group(1), "score": float(m.group(2)), "axes": axes, "why": " · ".join(why),
                    "decided": decided, "fix": "" if re.match(r"(?i)\s*(none\b|$)", fix) else fix.strip()})
    return out


def title_lines(body: str) -> list:
    return score_lines(body, "Titles")


def _cards(rows: list, kind: str, label: str) -> str:
    out = []
    for x in rows:
        inner = [f'<p class=tt-why>{esc(x["why"])}</p>' if x["why"] else ""]
        if x["decided"]:
            inner.append(f'<p class=tt-dec>{"🙋" if x["decided"].startswith("asked") else "🤖"} {esc(x["decided"])}</p>')
        if x["fix"]:
            inner.append(f'<p class=tt-fix><span class=mut>Suggested:</span> {esc(x["fix"])}</p>')
        scores = " · ".join([f'{label} {x["score"]:g}/10'] + x["axes"])
        out.append(f'<template class={kind} data-t="{esc(x["t"])}" data-low="{x["score"]:g}" '
                   f'data-scores="{esc(scores)}"><div class=tt-box><p class=tt-sc>{esc(scores)}</p>{"".join(inner)}'
                   f'</div></template>')
    return "".join(out)


def title_cards(body: str) -> str:
    """One hidden <template> per rated title and per rated paragraph, read by TITLE_JS."""
    return (_cards(score_lines(body, "Titles"), "tt-card", "title")
            + _cards(score_lines(body, "Paragraphs"), "tt-pcard", "paragraph"))


TITLE_JS = """<style>
.sx-tscore{cursor:pointer;margin-left:8px;font:500 11.5px system-ui,-apple-system,sans-serif;color:var(--mut)}
.sx-tscore.pass{font-size:10.5px;opacity:.6}.sx-tscore.mid{color:color-mix(in srgb,var(--mut) 80%,#b5651d)}
.sx-tscore.low{color:color-mix(in srgb,var(--mut) 70%,#8a3b2b)}.sx-tscore:hover{color:var(--acc)}
.tt-box{font:13px/1.5 system-ui,-apple-system,sans-serif;margin:4px 0 8px;padding:6px 10px;border-left:3px solid var(--line,#ddd)}
.tt-box p{margin:2px 0}.tt-sc{color:var(--mut);font-size:12px}
</style><script>
window.ttScore=function(){document.querySelectorAll('.sx-board h3.rv-part[data-p],.sx-board .rv-left h4[data-p]').forEach(function(h){
 if(h.querySelector('.sx-tscore'))return;var tp=document.querySelector('template.tt-card[data-t="'+h.dataset.p+'"]');if(!tp)return;
 var v=+tp.dataset.low,b=document.createElement('span');b.className='sx-tscore '+(v>=8?'pass':v>=7?'mid':'low');
 b.setAttribute('role','button');b.tabIndex=0;b.title='title: '+tp.dataset.scores;b.textContent='★'+v;
 var mk=h.querySelector(':scope>.sx-marks');if(mk)h.insertBefore(b,mk);else h.appendChild(b);
 tt(h,b,tp);});
 /* a paragraph's own score from the report's Paragraphs: block, where its Flow card gave none (A02) */
 document.querySelectorAll('.sx-board .rv-left h4[data-p]').forEach(function(h){if(h.querySelector('.sx-pscore'))return;
  var tp=document.querySelector('template.tt-pcard[data-t="'+h.dataset.p+'"]');if(!tp)return;var v=+tp.dataset.low,b=document.createElement('span');
  b.className='sx-pscore'+(v<8?' low':'');b.setAttribute('role','button');b.tabIndex=0;b.title=tp.dataset.scores;b.textContent='¶★'+v+'/10';
  (h.querySelector(':scope>.sx-marks')||h).appendChild(b);tt(h,b,tp);});};
function tt(h,b,tp){b.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();var nx=h.nextElementSibling;
  if(nx&&nx.classList.contains('tt-open')&&nx.dataset.k===tp.className){nx.remove();return;}if(nx&&nx.classList.contains('tt-open'))nx.remove();
  var bx=document.createElement('div');bx.className='tt-open';bx.dataset.k=tp.className;bx.innerHTML=tp.innerHTML;h.after(bx);});}
document.addEventListener('DOMContentLoaded',function(){window.ttScore();});
</script>"""
