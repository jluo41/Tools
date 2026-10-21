"""Revise view: one box per paragraph, pre-filled with its current Draft, edit in place.

JL 260922: "我想让每一个 paragraph 是一个方框，然后你把现在的 draft（也就是更新后的
draft）copy 过去 … 这样我就可以在上面改了." So each paragraph is one text box
holding its Draft sentences. JL 261020 took the frame and the row under it away ("i don't
like the box, could you remove it?"; "We might don't need this as well"): the box reads as plain text, a thin
line at its left while you type, and it saves when you leave it (or Cmd+Enter); Esc puts back what it held. The Draft a
reader sees in Reading view is the Draft field of each Outline Bullet, so on
Save the box goes back to the paragraph's Bullets: since JL 261020 the box shows each sentence a row ("we want to
make it each sentence a row"), and a Save cuts it into sentences and gives each Bullet the run of sentences, in
order, that reads most like what it held ("more easier and free style"; `_text_to_bullets`); nothing is dropped.
Since JL 261020 ("could we make each sentences to be auto generate the sentence id as well?") each row shows its
sentence id and carries its Bullet, so a Save knows which sentence each row is (`_rows_to_bullets`); a row the person
makes is a new Bullet with the id before it plus the next free letter (S2 → S2a), its point in `## 1 · Structure`
and its sentence in `## 3 · Draft`; no Bullet is ever renumbered. "+ paragraph" (`add_paragraph`, JL: "How could I
add a new paragraph?") puts an empty paragraph after one, which opens on one empty row. Nothing else in the Outline
moves.

Every Save writes the changed Draft fields back into the selected Outline
Markdown under the page lock, guarded by the Bullet and Draft tokens the page was
rendered with. Records only at the two ends (JL 260928): the first Save on a
paragraph opens its Revise run, `run-revise-<c1-p2>` (one ticket in
`runs/`, which keeps the paragraph's text before the Save as its Before); later
Saves change only the Draft (a Why note is kept in that ticket). `page.py
close-run` writes the Before / After ledger into the run's pass `runs/<run>/passes/` when the person
says close (haipipe-draft-writing (ref/revise.md)). The Runs panel lists the run under Revise edits.

Nothing here touches Page Content; `page.py adopt` copies the Drafts into it when the person asks.
"""
from __future__ import annotations

import datetime as dt
import difflib
import html
import json
import re
from pathlib import Path

import tempfile

from src.outline_version import plan_dir, latest_outline, record_path, version_tag
from src.run_folders import find_ticket, ticket_dir, ticket_rel, working_dir, write_card
from src.plan_shape import iter_plan_bullets, render_bullet
from src.plan_layout import (SCRATCH_TARGET, _assemble, _sections, from_canonical, is_sectioned,
                             overview_lines, set_overview, to_canonical)
from src.run_lifecycle import find_open, open_run
from live.outline_preview import (bullet_token, draft_path, page_lock, read_drafts,
                                  reader_prose, record_token, write_drafts)

_ADDRESS_RE = re.compile(r"^C\d+\.P\d+$")
_BULLET_RE = re.compile(r"^C\d+\.P\d+\.B\d+$")
MAX_TEXT = 40000


def _e(value) -> str:
    return html.escape(str(value), quote=True)


def _now() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M")


_REALIZES_RE = re.compile(r"(?m)^([^\n]*?)<!--\s*realizes:\s*(C\d+\.P\d+\.[BS]\d+)\s*-->\s*$")


def page_realizations(page_src: Path) -> dict[str, str]:
    """Bullet address -> the Page Content sentence(s) that realize it.

    The same reading the Table and Reading views fall back to when an Outline
    Bullet has no Draft field: the box starts from these sentences, and they
    are the ledger's Before when a Save writes the first Draft over them.
    """
    try:
        text = page_src.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}
    found: dict[str, list[str]] = {}
    for match in _REALIZES_RE.finditer(text):
        address = re.sub(r"\.S(\d+)$", r".B\1", match.group(2))
        prose = reader_prose(match.group(1)).strip()
        if prose:
            found.setdefault(address, []).append(prose)
    return {address: " ".join(lines) for address, lines in found.items()}


def _effective(records: dict, realized: dict, address: str) -> str:
    draft = " ".join(((records.get(address) or {}).get("text", "")).split())
    return draft or " ".join(realized.get(address, "").split())


_PROTECT_RE = re.compile(r"\b(?:e\.g\.|i\.e\.|et al\.|cf\.|vs\.|Dr\.|Mr\.|Ms\.|Prof\.|Fig\.|Eq\.|No\.|St\.|Jr\.|Inc\.|Ltd\.|[A-Z]\.)", re.I)
# a sentence may also open on a ⟦pending⟧ or ⟦check⟧ mark, or on a LaTeX command (JL 261020: a mark alone is its own
# sentence, and must stay its own point when the paragraph is saved as prose)
_END_RE = re.compile(r"[.!?]['\"”’)\]⟧]*\s+(?=[\"“'(\[A-Z0-9⟦\\])|[。！？]['\"”’)\]]*\s*")


def split_sentences(text: str) -> list[str]:
    """One sentence per line for the box (JL: "each sentence separated with a new line").

    Abbreviations, initials, decimals and citation braces are protected so a
    split lands only after a real sentence end. A wrong split is harmless: on
    Save the lines of one point are joined back with spaces.
    """
    text = " ".join(text.split())
    if not text:
        return []
    guarded = re.sub(r"(?<=\d)\.(?=\d)", "\u0000", text)
    guarded = _PROTECT_RE.sub(lambda m: m.group(0).replace(".", "\u0000"), guarded)
    guarded = re.sub(r"\{[^}]*\}", lambda m: m.group(0).replace(".", "\u0000").replace(" ", "\u0001"), guarded)
    parts, start = [], 0
    for match in _END_RE.finditer(guarded):
        parts.append(guarded[start:match.end()])
        start = match.end()
    parts.append(guarded[start:])
    cleaned = [p.replace("\u0000", ".").replace("\u0001", " ").strip() for p in parts]
    return [p for p in cleaned if p]


def box_text(texts: list[str]) -> str:
    """The box: each sentence a row (JL 261020: "we want to make it each sentence a row"), with no blank lines; a Save
    matches the rows back to the points by likeness (`_text_to_bullets`), so the editing stays free ("more easier and
    free style")."""
    return "\n".join(s for t in texts if t and t.strip() for s in split_sentences(t))


_SID_RE = re.compile(r"^(S\d+[a-z]?(?:\s*(?:-|–|to)\s*S\d+[a-z]?)?)\s*·")


def sentence_id(head: str) -> str:
    """A Bullet's sentence id, `S2` or `S2a`, from its head (`S2 · [Role] point`); empty on a plan without them."""
    match = _SID_RE.match(head or "")
    return match.group(1) if match else ""


def screen_rows(bullets: list[dict]) -> list[dict]:
    """The rows the editor shows: each sentence of each Bullet a row, `b` its Bullet, `s` its sentence id on the
    Bullet's first row (JL 261020: "could we make each sentences to be auto generate the sentence id as well?").
    `bullets` carry address, bullet_id, sid and text."""
    rows = []
    for bullet in bullets:
        for k, sentence in enumerate(split_sentences(bullet.get("text") or "")):
            rows.append({"b": bullet["address"], "text": sentence,
                         "s": (bullet.get("sid") or bullet.get("bullet_id") or "") if k == 0 else ""})
    return rows


# ---------------------------------------------------------------- rendering

def revise_rows_html(paragraph: str, display_paragraph: str, rows: list[dict], *,
                     read_only: bool = False, path_q: str = "", file_q: str = "") -> str:
    """One form per paragraph: its sentences a row each, each row labelled with its sentence id.

    `rows` carry address, bullet_id, sid, text, bullet_token and record_token for
    every Bullet of the paragraph, in plan order (none for a paragraph just added).
    Each row names its Bullet (`data-b`) so a Save maps rows back; the Bullet list
    rides along as data to detect a page rendered before someone else's edit.
    """
    # A paragraph with no points yet (just added) still opens on one empty row to type into (JL 261020: "How could I
    # add a new paragraph?"); its first Save makes its first Bullets.
    text = box_text([row["text"] for row in rows])
    bullets = json.dumps([{"address": r["address"], "bullet": r["bullet_token"], "record": r["record_token"]}
                          for r in rows], separators=(",", ":"))
    disabled = " disabled" if read_only else ""
    box = ('<textarea name="text" class="revise-box" data-bullets="%s" aria-label="Draft of %s" spellcheck="false" '
           'hidden%s>%s</textarea>'
           % (_e(bullets), _e(display_paragraph), disabled, _e(text)))
    # what the person types in: one row per sentence, a long one wrapping inside its row (JL 261020: "howto make this
    # each sentence a row?"; a one-line row ran off the edge), each row labelled with its sentence id. The textarea
    # above stays the text a Save compares.
    shown = screen_rows(rows)
    box += ('<div class="revise-rows%s" contenteditable="%s" role="textbox" aria-multiline="true" aria-label="Draft of %s" '
            'spellcheck="false">%s</div>'
            % ("" if shown else " blank", "false" if read_only else "true", _e(display_paragraph),
               "".join('<div data-b="%s" data-s="%s">%s</div>' % (_e(r["b"]), _e(r["s"]), _e(r["text"]))
                       for r in shown) or "<div><br></div>"))
    # no Why, Reset or Save row (JL 261020: "We might don't need this as well"): a box saves when you leave it
    actions = ('<div class="revise-actions"><span class="mut">read-only host</span></div>' if read_only else
               '<div class="revise-actions"><span class="revise-status" role="status" aria-live="polite"></span>'
               '<button type="button" class="revise-add" data-revise-add>+ paragraph</button></div>')
    return (
        '<form class="revise-form" data-paragraph="%s" data-display="%s" data-path="%s" '
        'data-file="%s" data-points="%d" autocomplete="off">%s%s</form>'
        % (_e(paragraph), _e(display_paragraph), _e(path_q), _e(file_q), len(rows), box, actions)
    )


def assets_html(read_only: bool = False) -> str:
    """CSS always; the Save script only where a Save exists (read-only hosts get none)."""
    css, _, script = _ASSETS.partition('</style>')
    return css + '</style>' + ('' if read_only else script)


_ASSETS = r'''<style>
.paragraph-revise{display:none}
.draft-lens[data-draft-mode="revise"] .paragraph-bullets,.draft-lens[data-draft-mode="revise"] .paragraph-reading{display:none}
.draft-lens[data-draft-mode="revise"] .paragraph-revise{display:block}
.draft-lens[data-draft-mode="revise"] details.paragraph-group>summary{cursor:pointer}
.draft-lens[data-draft-mode="revise"] .paragraph-group{margin-bottom:22px}
.revise-run-note{display:none;margin:-5px 0 12px;padding:7px 10px;border-left:2px solid var(--acc);color:var(--mut);font-size:12px;line-height:1.5}
.draft-lens[data-draft-mode="revise"] .revise-run-note{display:block}
.revise-form{display:block;padding:4px 0 2px}
.revise-box{box-sizing:border-box;width:100%;max-width:none;white-space:pre;overflow-x:auto;min-height:2em;resize:none;border:0;border-radius:0;background:transparent;color:var(--fg);padding:2px 0 2px 12px;font:15px/1.7 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;field-sizing:content}
.revise-box:hover{box-shadow:inset 2px 0 0 var(--line)}
.revise-box:focus{outline:none;box-shadow:inset 2px 0 0 var(--acc)}
.revise-box.changed{box-shadow:inset 3px 0 0 var(--acc)}
.revise-box:disabled{background:transparent}
.revise-box[hidden]{display:none!important}
.revise-rows{box-sizing:border-box;width:100%;max-width:100ch;padding:2px 0 2px 12px;color:var(--fg);outline:none;font:15px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;white-space:normal;overflow-wrap:anywhere}
.revise-rows>div{padding-left:46px;text-indent:-46px;margin:0 0 4px}
.revise-rows>div::before{content:attr(data-s);display:inline-block;width:46px;text-indent:0;color:var(--mut);font:11.5px/1 ui-monospace,Menlo,monospace}
.revise-rows>div:not([data-b])::before{content:"new";color:var(--acc)}
.revise-rows.blank>div::before{content:""}
.revise-rows.blank{position:relative}
.revise-rows.blank::after{content:"Type the first sentence; one sentence a row";position:absolute;left:58px;top:2px;color:var(--mut);pointer-events:none}
.revise-add{margin-left:auto;font:12px system-ui,sans-serif;border:0;background:none;color:var(--mut);cursor:pointer;padding:2px 0;opacity:.55}
.revise-add:hover,.revise-add:focus-visible{opacity:1;color:var(--acc)}
.revise-add:disabled{cursor:default}
.revise-rows:hover{box-shadow:inset 2px 0 0 var(--line)}
.revise-rows:focus{box-shadow:inset 2px 0 0 var(--acc)}
.revise-rows.changed{box-shadow:inset 3px 0 0 var(--acc)}
.revise-actions{display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding:2px 0 0 12px}
.revise-status:empty{display:none}
.revise-why{flex:1 1 12em;min-width:0;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg);padding:4px 8px;font:12.5px system-ui,sans-serif}
.revise-save,.revise-reset{font:600 12px/1.4 system-ui,sans-serif;border:1px solid var(--line);border-radius:6px;padding:4px 10px;cursor:pointer;background:var(--card);color:var(--fg)}
.revise-save{border-color:var(--acc);color:var(--acc)}
.revise-save:disabled,.revise-reset:disabled{opacity:.5;cursor:default}
.revise-status{font:12px system-ui,sans-serif;color:var(--mut)}
.revise-status.err{color:var(--warn)}
.revise-empty{color:var(--mut);font-size:12.5px;padding:6px 0}
@media (max-width:700px){.revise-box{font-size:15px;padding:2px 0 2px 10px}}
</style><script>
(function(){
 if(window.__draftRevise)return; window.__draftRevise=true;
 var known=new WeakSet();   /* the rows the page drew; a row the browser makes (Enter, paste) is a new sentence */
 function box(form){return form.querySelector('.revise-box');}
 function rowsOf(form){return form.querySelector('.revise-rows');}
 function clean(s){return s.replace(/ /g,' ').replace(/\s+/g,' ').trim();}
 /* the rows a person typed, one sentence a row: the text a Save compares (the hidden textarea keeps it) */
 function read(el){return el.innerText.split('\n').map(clean).filter(Boolean).join('\n');}
 /* each row with the Bullet it was drawn from; a new row names none, and the Save gives it the next free id */
 function rows(el){var out=[];Array.prototype.forEach.call(el.childNodes,function(n){
   var own=n.nodeType===1&&(known.has(n)||!el._ready)?(n.getAttribute('data-b')||''):'';
   (n.nodeType===1?n.innerText:(n.textContent||'')).split('\n').map(clean).filter(Boolean)
    .forEach(function(t,k){out.push({b:k?'':own,text:t});});});return out;}
 function adopt(el){Array.prototype.forEach.call(el.children,function(d){known.add(d);});}
 function ready(form){var el=rowsOf(form);if(el&&!el._ready){adopt(el);form._html=el.innerHTML;el._ready=true;}}
 function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
 function paint(form,list){var el=rowsOf(form);if(!el)return;
  el.innerHTML=list.length?list.map(function(r){return '<div data-b="'+esc(r.b)+'" data-s="'+esc(r.s||'')+'">'+esc(r.text)+'</div>';}).join(''):'<div><br></div>';
  el.classList.toggle('blank',!list.length);adopt(el);el._ready=true;form._html=el.innerHTML;}
 function restore(form){var el=rowsOf(form);if(!el||form._html==null)return;el.innerHTML=form._html;adopt(el);el.classList.toggle('blank',!read(el));}
 /* the caret back on the same row after a repaint, at its end */
 function rowAt(el){var s=window.getSelection();var n=s&&s.anchorNode;while(n&&n.parentNode!==el)n=n.parentNode;return n?Array.prototype.indexOf.call(el.childNodes,n):-1;}
 function caret(el,i){var d=el.children[Math.min(i,el.children.length-1)];if(!d)return;var r=document.createRange();r.selectNodeContents(d);r.collapse(false);var s=window.getSelection();s.removeAllRanges();s.addRange(r);}
 function dirty(form){var b=box(form);return b&&b.value.trim()!==b.defaultValue.trim();}
 function mark(form){var d=dirty(form);var b=box(form);if(b)b.classList.toggle('changed',d);var el=rowsOf(form);if(el)el.classList.toggle('changed',d);return d;}
 function status(form,text,err){var s=form.querySelector('.revise-status');if(!s)return;s.textContent=text;s.classList.toggle('err',!!err);}
 function where(form){var params=new URLSearchParams(location.search);return{path:form.dataset.path||params.get('path')||'',file:form.dataset.file||params.get('file')||''};}
 function payload(form){var b=box(form),el=rowsOf(form),at=where(form);var body={action:'revise',path:at.path,file:at.file,paragraph:form.dataset.paragraph,display:form.dataset.display||'',why:'',text:b.value,bullets:JSON.parse(b.dataset.bullets||'[]')};if(el)body.rows=rows(el);return body;}
 function reflect(change){var line=document.querySelector('.reading-line[data-point="'+change.address+'"] .reading-copy');if(line)line.textContent=change.text||'Not drafted';var id='bullet-'+change.address.replace(/\./g,'-');var row=document.getElementById(id);var copy=row?row.querySelector('.preview-copy'):null;if(copy)copy.textContent=change.text||'Not drafted';}
 try{document.execCommand('defaultParagraphSeparator',false,'div');}catch(err){}   /* Enter starts a new row */
 document.addEventListener('focusin',function(e){var el=e.target.closest&&e.target.closest('.revise-rows');if(el)ready(el.closest('form.revise-form'));});
 document.addEventListener('input',function(e){var form=e.target.closest&&e.target.closest('form.revise-form');if(!form)return;
  var el=e.target.closest('.revise-rows');
  if(el){Array.prototype.forEach.call(el.children,function(d){if(!known.has(d)){d.removeAttribute('data-b');d.removeAttribute('data-s');}});
   box(form).value=read(el);el.classList.toggle('blank',!box(form).value);}
  if(el||e.target.classList.contains('revise-box'))mark(form);});
 document.addEventListener('paste',function(e){var el=e.target.closest&&e.target.closest('.revise-rows');if(!el)return;   /* plain text only */
  e.preventDefault();document.execCommand('insertText',false,(e.clipboardData||window.clipboardData).getData('text/plain'));});
 document.addEventListener('keydown',function(e){var t=e.target.closest&&e.target.closest('.revise-box,.revise-rows');if(!t)return;var form=t.closest('form.revise-form');
  if((e.metaKey||e.ctrlKey)&&e.key==='Enter'){e.preventDefault();form.requestSubmit();}
  else if(e.key==='Escape'){var b=box(form);b.value=b.defaultValue;restore(form);mark(form);status(form,'');t.blur();}});
 document.addEventListener('focusout',function(e){var t=e.target.closest&&e.target.closest('.revise-box,.revise-rows');if(!t)return;var form=t.closest('form.revise-form');if(dirty(form))form.requestSubmit();});
 document.addEventListener('submit',function(e){
  var form=e.target.closest&&e.target.closest('form.revise-form');if(!form)return;e.preventDefault();
  if(!dirty(form)){status(form,'');return;}
  var body=payload(form);status(form,'Saving…');
  form._pending=fetch('/_board/draft',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})
   .then(function(r){return r.json().then(function(j){if(!r.ok||!j.ok)throw new Error(j.err||'Unable to save');return j;});})
   .then(function(j){var b=box(form),el=rowsOf(form);var typed=b.value!==body.text;
     b.defaultValue=j.text;b.dataset.bullets=JSON.stringify(j.bullets||[]);(j.changed||[]).forEach(reflect);
     /* repaint with each row's id, new rows included, unless the person typed on while it saved */
     if(el&&!typed){var focused=document.activeElement===el,at=focused?rowAt(el):-1;b.value=j.text;paint(form,j.rows||[]);if(focused)caret(el,at);}
     mark(form);var n=(j.changed||[]).length;status(form,n?'Saved · '+n+' sentence'+(n===1?'':'s'):'Nothing changed.');})
   .catch(function(err){status(form,String(err.message||err),true);mark(form);})
   .then(function(){form._pending=null;});
 });
 /* + paragraph: an empty paragraph after this one, opened on one empty row */
 document.addEventListener('click',function(e){var add=e.target.closest&&e.target.closest('[data-revise-add]');if(!add)return;
  var form=add.closest('form.revise-form'),at=where(form);add.disabled=true;status(form,'Adding a paragraph…');
  var waits=Array.prototype.map.call(document.querySelectorAll('form.revise-form'),function(f){return f._pending;}).filter(Boolean);
  Promise.all(waits).then(function(){return fetch('/_board/draft',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({action:'add-paragraph',path:at.path,file:at.file,after:form.dataset.paragraph})});})
   .then(function(r){return r.json().then(function(j){if(!r.ok||!j.ok)throw new Error(j.err||'Unable to add a paragraph');return j;});})
   .then(function(j){location.hash='group-'+j.paragraph.replace(/[^A-Za-z0-9_-]/g,'-');location.reload();})
   .catch(function(err){add.disabled=false;status(form,String(err.message||err),true);});});
 window.addEventListener('beforeunload',function(e){if(Array.prototype.some.call(document.querySelectorAll('form.revise-form'),dirty)){e.preventDefault();e.returnValue='';}});
 document.querySelectorAll('form.revise-form').forEach(mark);
})();
</script>'''


# ------------------------------------------------------------------- saving

def _clean_line(value: str, address: str) -> str:
    text = " ".join(value.split())
    if "<!--" in text or text.startswith(("> Comment ", "## ", "- ")):
        raise ValueError("%s: Draft accepts prose, not hidden address records" % address)
    return text


def _card(number: int, address: str, before: str, after: str, why: str) -> str:
    kind = "first draft" if not before else "deletion" if not after else "wording"
    return (
        "##### R%02d · %s\n\n"
        "###### Target\n%s\n\n"
        "###### Before\n%s\n\n"
        "###### After\n%s\n\n"
        "###### Why\n%s\n\n"
        "###### Decision\naccept\n\n"
        "###### Preference status\nedited directly by the person in Draft Space → Revise\n"
        % (number, kind, address, before or "(no draft)", after or "(removed)", why)
    )


def _write_ledger(page_src: Path, run_id: str, existing: bool, target: str, display: str,
                  plan: Path, changes: list[dict], why: str) -> dict:
    base = page_src.parent
    runs = ticket_dir(base, run_id)                 # the run's own folder (0.125)
    runs.mkdir(parents=True, exist_ok=True)
    if not (runs / (run_id + ".md")).is_file():     # the ticket first: it makes the folder a run
        (runs / (run_id + ".md")).write_text("---\nfamily: page\nrun: %s\n---\n" % run_id, encoding="utf-8")
        existing = False
    result = working_dir(base, run_id)              # its open pass, or results/<run>/ (older)
    rel = result.relative_to(base).as_posix()
    version_file = result / "v001.md"
    text = version_file.read_text(encoding="utf-8", errors="replace") if existing and version_file.is_file() else ""
    step_number = len(re.findall(r"(?m)^## Step s\d+", text)) + 1
    card_start = len(re.findall(r"(?m)^##### R\d+ ·", text)) + 1
    step = "s%03d" % step_number
    stamp = _now()
    why = why or "Edited directly in Draft Space → Revise."
    cards = "".join(_card(card_start + i, c["address"], c["before"], c["after"], why)
                    for i, c in enumerate(changes))
    block = (
        "## Step %s\n\n"
        "### Human feedback\n"
        "Direct edit of %s in Draft Space → Revise · %s.\n\n"
        "### Saved result\n\n"
        "#### Inputs\n"
        "- Before: %s · Draft fields as rendered (the Page's own sentence where no Draft existed)\n"
        "- After: the same file after this Save\n"
        "- Target: %s (%s)\n\n"
        "#### Summary\n"
        "%d sentence%s changed in %s.\n\n"
        "#### Track changes\n\n%s"
        % (step, display, stamp, plan.parent.name + "/" + plan.name, target, display,
           len(changes), "s"[:len(changes) != 1], display, cards)
    )
    if not text:
        text = ("Run: %s\nVersion: v001\nState: open\nTarget: %s\n\n" % (run_id, target)) + block
    else:
        text = text.rstrip("\n") + "\n\n" + block
    version_file.write_text(text.rstrip("\n") + "\n", encoding="utf-8")
    if not existing or "operation:" not in (runs / (run_id + ".md")).read_text(encoding="utf-8"):
        (runs / (run_id + ".md")).write_text(
            "---\n"
            "family: page\noperation: interactive-writing\ninteraction: human-revise\n"
            "mode: revise\ntarget_scope: paragraph\ntarget: %s\nrun: %s\n"
            "ticket: %s\nresult: %s\n"
            "---\n\n# %s\n\n"
            "- Purpose: the person revises the Draft of %s in place; every Save appends one Step "
            "with a change ledger.\n"
            "- Close rule: the person closes the Run when the paragraph reads right; the accepted "
            "Drafts stay in the Outline for the writing Run to adopt.\n"
            % (target, run_id, ticket_rel(base, run_id), rel, run_id, display), encoding="utf-8")
        if runs.name == run_id:
            write_card(base, run_id, type="revise", target=target, skill="haipipe-draft-writing",
                       status="running", writes=[], feeds=[])
    total = len(re.findall(r"(?m)^##### R\d+ ·", text))
    summary = "%d change%s over %d Step%s" % (total, "s"[:total != 1], step_number, "s"[:step_number != 1])
    (result / "working.md").write_text(
        "# %s · Revise\n\n- State: open.\n- Target: paragraph %s (%s).\n- Summary: %s.\n"
        "- Latest: %s · %d sentence%s.\n"
        % (run_id, target, display, summary, step, len(changes), "s"[:len(changes) != 1]),
        encoding="utf-8")
    (result / "runtime.yaml").write_text(
        "run: %s\nfamily: page\noperation: interactive-writing\ninteraction: human-revise\n"
        "mode: revise\ntarget_scope: paragraph\ntarget: %s\n"
        "ticket: %s\nresult: %s\nstatus: running\nversion: v001\nstep: %s\n"
        "version_file: %s/v001.md\nsummary: %s\n"
        % (run_id, target, ticket_rel(base, run_id), rel, step, rel, summary), encoding="utf-8")
    return {"run": run_id, "step": step, "summary": summary,
            "result": str(result.relative_to(base))}


def _words(text: str) -> list[str]:
    """A sentence's words for matching: lower case, the punctuation at either end of each word taken off."""
    return [w for w in (x.strip(".,;:!?()[]\"'“”‘’") for x in text.lower().split()) if w]


def _text_to_bullets(text: str, addresses: list[str], before: list[str]) -> dict[str, str]:
    """The paragraph as typed → its Bullets, by likeness: the text is cut into sentences, and each Bullet takes the
    run of sentences, in order, that reads most like the sentence it held before (word overlap). Every sentence
    lands somewhere and the order never changes: a sentence typed in between joins the neighbour it fits best, a
    deleted one leaves its Bullet empty, and with nothing to match (a first draft) Bullet k takes sentence k and the
    last takes the rest. A row ends a sentence (a line typed without its full stop stays its own sentence); blank
    lines carry no meaning."""
    sents = [s for line in text.splitlines() for s in split_sentences(line)]     # a row ends a sentence too
    n, m = len(addresses), len(sents)
    if not m:
        return {a: "" for a in addresses}
    old = [_words(b) for b in before] + [[]] * (n - len(before))

    def score(i: int, k: int, j: int) -> int:
        if k == j:
            return 0
        got = _words(" ".join(sents[k:j]))
        like = difflib.SequenceMatcher(None, old[i], got).ratio() if old[i] and got else 0.0
        # a filled Bullet gains a little, an earlier one a little more (with nothing to match, fill from B1);
        # a long run costs a little
        return round(like * 1000) + 20 + (n - i) - (j - k - 1)

    worst = -10 ** 9
    best = [[worst] * (m + 1) for _ in range(n + 1)]
    cut = [[0] * (m + 1) for _ in range(n + 1)]
    best[0][0] = 0
    for i in range(1, n + 1):
        for j in range(m + 1):
            for k in range(j + 1):
                if best[i - 1][k] == worst:
                    continue
                total = best[i - 1][k] + score(i - 1, k, j)
                if total > best[i][j]:
                    best[i][j], cut[i][j] = total, k
    mapped, j = {}, m
    for i in range(n, 0, -1):
        k = cut[i][j]
        mapped[addresses[i - 1]] = " ".join(sents[k:j])
        j = k
    return mapped


def _like(a: str, b: str) -> float:
    wa, wb = _words(a), _words(b)
    return difflib.SequenceMatcher(None, wa, wb).ratio() if wa and wb else 0.0


def _rows_to_bullets(rows: list[dict], addresses: list[str], before: list[str]) -> tuple[dict, list]:
    """The rows as typed, each naming the Bullet it was drawn from (`b`, empty on a new row) → (the paragraph's
    Bullets: their new text, [(the Bullet a run of new sentences follows, or None for the paragraph's start,
    [sentence, ...])]).

    A row keeps its Bullet, so typing inside a row edits that sentence; a row the person made (Enter, paste) is a new
    sentence (JL 261020: "auto generate the sentence id"). Inside a row, the sentences that read like the Bullet's own
    keep it and a sentence typed before or after them is new. A new sentence word for word a sentence of a Bullet no
    row names is that Bullet (two rows joined, a row retyped); an empty planned point takes the next new sentence
    before any new Bullet is made. Bullets never change order: a row naming one out of order is new."""
    index = {a: i for i, a in enumerate(addresses)}
    named = {str(r.get("b") or "") for r in rows} & set(addresses)
    olds = [split_sentences(b) for b in before]
    groups: list[list] = []          # [address or None, [sentences]] in the order typed
    last = -1

    def put(address, sentence):
        if address is not None and groups and groups[-1][0] == address:
            groups[-1][1].append(sentence)
        else:
            groups.append([address, [sentence]])

    def loose(sentence, upto):
        nonlocal last
        start = last if last >= 0 and groups and groups[-1][0] == addresses[last] else last + 1
        for k in range(start, upto):
            if addresses[k] not in named and any(" ".join(_words(o)) == " ".join(_words(sentence)) for o in olds[k]):
                put(addresses[k], sentence)
                last = k
                return
        put(None, sentence)

    for row in rows:
        sents = split_sentences(" ".join(str(row.get("text") or "").split()))
        if not sents:
            continue
        i = index.get(str(row.get("b") or ""), -1)
        if i >= 0 and (i < last or (i == last and not (groups and groups[-1][0] == addresses[i]))):
            i = -1
        if i < 0:
            for sentence in sents:
                loose(sentence, len(addresses))
            continue
        keep = [k for k, s in enumerate(sents) if any(_like(s, o) >= 0.5 for o in olds[i])]
        first, end = (keep[0], keep[-1] + 1) if len(sents) > 1 and keep else (0, len(sents))
        for sentence in sents[:first]:
            loose(sentence, i)
        for sentence in sents[first:end]:
            put(addresses[i], sentence)
        last = i
        for sentence in sents[end:]:
            loose(sentence, len(addresses))

    mapped = {a: "" for a in addresses}
    inserts, waiting, placed = [], [], -1

    def flush(upto):
        free = [k for k in range(placed + 1, upto) if not before[k].strip()]
        for k, sentence in zip(free, waiting):
            mapped[addresses[k]] = sentence
        rest = waiting[len(free):]
        if rest:
            after = free[-1] if free else placed
            inserts.append((addresses[after] if after >= 0 else None, list(rest)))
        waiting.clear()

    for address, sents in groups:
        if address is None:
            waiting.extend(sents)
            continue
        flush(index[address])
        mapped[address] = " ".join(sents)
        placed = index[address]
    flush(len(addresses))
    return mapped, inserts


def _point(sentence: str, words: int = 8) -> str:
    """The plan point of a sentence typed in Revise: its first words, for the person to rename."""
    text = re.sub(r"\\cite\w*\*?(?:\[[^\]]*\])*\{[^}]*\}", "", sentence)
    ws = reader_prose(text).split()
    return "[Added] " + " ".join(ws[:words]).rstrip(".,;:") + (" …" if len(ws) > words else "")


def _new_ids(plan_text: str, paragraph: str, inserts: list) -> list:
    """Give each new sentence its Bullet number (the paragraph's highest + 1, never renumbering) and its sentence id:
    the id before it with the next free letter (S2 → S2a, then S2b), page-wide; none on a plan that has none."""
    blocks = list(iter_plan_bullets(plan_text))
    sids = [sentence_id(b["head"]) for b in blocks]
    taken = {s for s in sids if s}
    order = [m.group(1) for m in re.finditer(r"(?m)^### (C\d+\.P\d+)\b", to_canonical(plan_text))]
    earlier = set(order[:order.index(paragraph)]) if paragraph in order else set()
    numbers = [int(b["bullet"][1:]) for b in blocks if b["paragraph"] == paragraph]
    next_b = max(numbers, default=0) + 1
    out = []
    for after, sentences in inserts:
        if after:
            at = next(k for k, b in enumerate(blocks) if b["address"] == after)
            prior = [s for s in sids[:at + 1] if s]
        else:
            prior = [s for b, s in zip(blocks, sids) if s and b["paragraph"] in earlier]
        base = int(re.findall(r"S(\d+)", prior[-1])[-1]) if prior else 0
        made = []
        for sentence in sentences:
            sid = ""
            if taken:
                letter = next(c for c in "abcdefghijklmnopqrstuvwxyz" if "S%d%s" % (base, c) not in taken)
                sid = "S%d%s" % (base, letter)
                taken.add(sid)
            made.append({"address": "%s.B%d" % (paragraph, next_b), "number": next_b, "sid": sid, "text": sentence})
            next_b += 1
        out.append((after, made))
    return out


def _insert_bullets(plan: Path, paragraph: str, inserts: list) -> None:
    """Write the new Bullets into the plan, each run right after the Bullet it follows (None: before the paragraph's
    first): its point in `## 1 · Structure`, its sentence in `## 3 · Draft`."""
    raw = plan.read_text(encoding="utf-8", errors="replace")
    lines = to_canonical(raw).split("\n")
    head, spans, i = None, {}, 0
    while i < len(lines):
        line = lines[i]
        heading = re.match(r"^### (C\d+\.P\d+)\b", line)
        if heading or (line.startswith("## ") and head is not None):
            if head is not None:
                break
            if heading and heading.group(1) == paragraph:
                head = i
            i += 1
            continue
        bullet = re.match(r"^- (?:\[[ xX]\]\s*)?(?:B|S)(\d+)\s*·", line)
        if head is not None and bullet:
            j = i + 1
            while j < len(lines) and lines[j].startswith("  ") and not re.match(r"^- ", lines[j]):
                j += 1
            spans["%s.B%s" % (paragraph, bullet.group(1))] = (i, j)
            i = j
            continue
        i += 1
    if head is None:
        raise ValueError("%s is not in the plan; reload" % paragraph)
    placed = []
    for after, made in inserts:
        block = []
        for bullet in made:
            block += render_bullet("- B%d · " % bullet["number"], bullet["sid"] + " · " if bullet["sid"] else "",
                                   _point(bullet["text"]), [], bullet["text"], "")
        placed.append((spans[after][1] if after else head + 1, block))
    for at, block in sorted(placed, key=lambda x: -x[0]):
        lines[at:at] = block
    _atomic(plan, from_canonical(raw, "\n".join(lines)))


def _atomic(plan: Path, text: str) -> None:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=plan.parent, prefix=".outline-", delete=False) as tmp:
        tmp.write(text)
        temporary = Path(tmp.name)
    temporary.replace(plan)


def add_paragraph(page_src: Path, payload: dict, *, read_only: bool = False) -> tuple[dict | None, str | None]:
    """An empty paragraph right after `after`, in the same section (JL 261020: "How could I add a new paragraph?").

    Its address takes the page's highest paragraph number + 1, so no paragraph, Run or Evidence record is renumbered
    (the views number paragraphs by position). Its heading goes into the three sections and the Structure Overview;
    the Revise view opens it on one empty row, and Structure renames it."""
    if read_only:
        return None, "This host is read-only; paragraphs cannot be added"
    after = str(payload.get("after") or "").strip()
    if not _ADDRESS_RE.match(after):
        return None, "after must be a C<n>.P<m> address"
    title = "New paragraph"
    with page_lock(page_src):
        plan = latest_outline(plan_dir(page_src.parent), page_src.stem)
        if plan is None or not plan.is_file():
            return None, "No Outline Markdown exists for this Page"
        if plan.is_symlink() or plan.parent.is_symlink():
            return None, "Outline source must be a local Markdown file"
        raw = plan.read_text(encoding="utf-8", errors="replace")
        lines = to_canonical(raw).split("\n")
        heads = [(k, m.group(1)) for k, line in enumerate(lines) if (m := re.match(r"^### (C\d+\.P\d+)\b", line))]
        at = next((k for k, address in heads if address == after), None)
        if at is None:
            return None, "%s is not in the plan; reload" % after
        new = "%s.P%d" % (after.split(".")[0], max(int(a.split(".P")[1]) for _k, a in heads) + 1)
        heading = "### %s · %s" % (new, title)
        end = next((k for k in range(at + 1, len(lines)) if lines[k].startswith(("### ", "## "))), len(lines))
        while end > at + 1 and not lines[end - 1].strip():
            end -= 1
        lines[end:end] = ["", heading]
        text = from_canonical(raw, "\n".join(lines))
        if is_sectioned(text):
            entries = overview_lines(text)
            k = next((n for n, e in enumerate(entries) if re.match(r"^- %s\b" % re.escape(after), e)), None)
            if k is not None:
                k += 1
                while k < len(entries) and entries[k].strip().startswith("→"):
                    k += 1
                entries[k:k] = ["- %s · %s" % (new, title)]
                text = set_overview(text, entries)
            header, sections, order, tail = _sections(text)
            if "scratch" in sections:
                body = sections["scratch"][1]
                k = next((n for n, line in enumerate(body)
                          if (m := SCRATCH_TARGET.match(line)) and m.group(1) == after), None)
                if k is not None:
                    stop = next((n for n in range(k + 1, len(body)) if body[n].startswith("### ")), len(body))
                    while stop > k + 1 and not body[stop - 1].strip():
                        stop -= 1
                    body[stop:stop] = ["", heading]
                    text = _assemble(header, sections, order, tail)
        _atomic(plan, text)
        log = record_path(plan_dir(page_src.parent), page_src.stem, "log")
        if log.is_file():
            with log.open("a", encoding="utf-8") as fh:
                fh.write("\n### %s · Paragraph added in Draft Space\n- **Headings**: %s after %s\n"
                         % (dt.datetime.now().strftime("%y%m%d %H%M"), new, after))
    return {"paragraph": new, "after": after, "outline": str(plan)}, None


def _display_name(run_id: str) -> str:
    """The name people read, as the Runs panel shows it."""
    try:
        from live.runs_panel import display_name
    except ImportError:
        return run_id
    return display_name(run_id)


def _note_why(folder: Path, run_id: str, paragraph: str, why: str) -> None:
    """Keep the person's reason in the open run's own ticket (not in results/ or the log)."""
    ticket = find_ticket(folder, run_id) or folder / "runs" / (run_id + ".md")
    if ticket.is_file():
        text = ticket.read_text(encoding="utf-8")
        if "\n## Why\n" not in text:
            text = text.rstrip("\n") + "\n\n## Why\n"
        ticket.write_text(text.rstrip("\n") + "\n- %s: %s\n" % (paragraph, why), encoding="utf-8")


def _screen(blocks: dict, paragraph: str, fresh: dict, realized: dict) -> tuple[list[str], list[dict]]:
    """-> (the paragraph's Bullet addresses in plan order, the rows the editor shows)."""
    addresses = [a for a in blocks if a.startswith(paragraph + ".")]
    return addresses, screen_rows([{"address": a, "bullet_id": blocks[a]["bullet"], "sid": sentence_id(blocks[a]["head"]),
                                    "text": _effective(fresh, realized, a)} for a in addresses])


def _id_clash(text: str) -> str:
    """Why a save must wait, or "": a sentence in `## 3 · Draft` whose id differs from its point's (the same B) in
    `## 1 · Structure`. A save writes every §3 id from §1 by B, so a §1 whose B numbers were shifted would silently
    relabel the text (t01, 261020: a point put in after S2 took B3, and the save made S3 into S2a)."""
    if not is_sectioned(text):
        return ""
    ids, part, para = {"1": {}, "3": {}}, None, None
    for line in text.splitlines():
        m = re.match(r"^## (\d+)\s*·", line)
        h = re.match(r"^### (C\d+\.P\d+)\b", line)
        b = re.match(r"^- B(\d+) · (S\d+[a-z]*) · ", line)
        if m:
            part = m.group(1)
        elif h:
            para = h.group(1)
        elif b and para and part in ids:
            ids[part][(para, b.group(1))] = b.group(2)
    for (para, n), sid in ids["3"].items():
        planned = ids["1"].get((para, n))
        if planned and planned != sid:
            return ("Not saved: %s.B%s is %s in the plan but %s in the text; the plan's B numbers shifted, "
                    "fix them first" % (para, n, planned, sid))
    return ""


def save_revise(page_src: Path, payload: dict, *, read_only: bool = False) -> tuple[dict | None, str | None]:
    """Map the typed rows onto the paragraph's Bullets, add a Bullet per new sentence, save, extend the Revise Run.

    `rows` ([{b, text}], each row naming the Bullet it was drawn from) is what the editor sends; without it the
    `text` alone is matched to the Bullets by likeness and no Bullet is added."""
    if read_only:
        return None, "This host is read-only; Revise saves are disabled"
    paragraph = str(payload.get("paragraph") or "").strip()
    if not _ADDRESS_RE.match(paragraph):
        return None, "paragraph must be a C<n>.P<m> address"
    text = payload.get("text")
    if not isinstance(text, str) or len(text) > MAX_TEXT:
        return None, "text must be a string of at most 40,000 characters"
    rows = payload.get("rows")
    if rows is not None and not (isinstance(rows, list) and all(
            isinstance(r, dict) and isinstance(r.get("text", ""), str) and isinstance(r.get("b", ""), str)
            for r in rows) and sum(len(r.get("text", "")) for r in rows) <= MAX_TEXT):
        return None, "rows must list the typed rows, each {b, text}, at most 40,000 characters"
    listed = payload.get("bullets")
    if not isinstance(listed, list) or not all(isinstance(b, dict) for b in listed) or (not listed and rows is None):
        return None, "bullets must list the paragraph's Bullets as rendered"
    why = str(payload.get("why") or "").strip()
    if len(why) > 500 or "<!--" in why:
        return None, "why must be one short line"
    addresses = [str(b.get("address") or "").strip() for b in listed]
    if not all(_BULLET_RE.match(a) and a.startswith(paragraph + ".") for a in addresses):
        return None, "every listed Bullet must sit inside %s" % paragraph
    with page_lock(page_src):
        plan = latest_outline(plan_dir(page_src.parent), page_src.stem)
        if plan is None or not plan.is_file():
            return None, "No Outline Markdown exists for this Page"
        if plan.is_symlink() or plan.parent.is_symlink():
            return None, "Outline source must be a local Markdown file"
        plan_text = plan.read_text(encoding="utf-8", errors="replace")
        clash = _id_clash(plan_text)
        if clash:
            return None, clash
        blocks = {b["address"]: b for b in iter_plan_bullets(plan_text)}
        current = [a for a in blocks if a.startswith(paragraph + ".")]
        if current != addresses:
            return None, "%s's points changed since this page was opened; reload before saving" % paragraph
        if not addresses and not re.search(r"(?m)^### %s\b" % re.escape(paragraph), to_canonical(plan_text)):
            return None, "%s is not in the plan; reload" % paragraph
        records = read_drafts(page_src)
        realized = page_realizations(page_src)
        for item in listed:
            address = str(item.get("address"))
            if str(item.get("bullet") or "") != bullet_token(blocks[address]):
                return None, "Point %s changed; reload and review before saving" % address
            if str(item.get("record") or "") != record_token(records.get(address)):
                return None, "Draft %s changed in another editor; reload before saving" % address
        before = [_effective(records, realized, a) for a in addresses]
        try:
            if rows is None:
                mapped, inserts = _text_to_bullets(text, addresses, before), []
            else:
                mapped, inserts = _rows_to_bullets(rows, addresses, before)
            mapped = {a: _clean_line(t, a) for a, t in mapped.items()}
            inserts = [(after, [_clean_line(s, paragraph) for s in sentences]) for after, sentences in inserts]
        except ValueError as exc:
            return None, str(exc)
        changed = []
        for address, old in zip(addresses, before):
            if old == mapped[address]:
                continue
            changed.append({"address": address, "before": old, "after": mapped[address]})
        if not changed and not inserts:
            fresh = read_drafts(page_src)
            shown = _screen(blocks, paragraph, fresh, realized)[1]
            return {"paragraph": paragraph, "changed": [], "run": "", "step": "",
                    "text": "\n".join(r["text"] for r in shown), "rows": shown,
                    "bullets": [{"address": a, "bullet": bullet_token(blocks[a]),
                                 "record": record_token(fresh.get(a))} for a in addresses],
                    "message": "nothing changed"}, None
        # The paragraph as it reads before this Save: a new Revise run keeps it as its Before.
        before_text = "\n".join("%s · %s" % (a, b or "") for a, b in zip(addresses, before))
        if changed:
            for item in changed:
                records[item["address"]] = {**records.get(item["address"], {}),
                                            "plan": version_tag(plan),
                                            "text": item["after"]}
            write_drafts(page_src, records)
        if inserts:
            made = _new_ids(plan.read_text(encoding="utf-8", errors="replace"), paragraph, inserts)
            try:
                _insert_bullets(plan, paragraph, made)
            except ValueError as exc:
                return None, str(exc)
            changed += [{"address": b["address"], "before": "", "after": b["text"]} for _a, bs in made for b in bs]
        fresh = read_drafts(page_src)
        blocks = {b["address"]: b for b in iter_plan_bullets(plan.read_text(encoding="utf-8", errors="replace"))}
        addresses, shown = _screen(blocks, paragraph, fresh, realized)
        # Records only at the two ends (JL 260928): the first Save opens the run (its ticket
        # keeps the Before); later Saves change only the Draft; close-run writes the run's pass.
        run_id = find_open(page_src.parent, "revise", paragraph)
        if not run_id:
            run_id = open_run(page_src, "revise", target=paragraph, goal=why,
                              by="person · Draft Space › Revise", before=before_text)["run"]
        elif why:
            _note_why(page_src.parent, run_id, paragraph, why)
    return {
        "paragraph": paragraph,
        "run": run_id, "name": run_id, "step": "", "summary": "",
        "result": "", "outline": str(draft_path(page_src)),
        "version": version_tag(plan),
        "text": "\n".join(r["text"] for r in shown), "rows": shown,
        "bullets": [{"address": a, "bullet": bullet_token(blocks[a]), "record": record_token(fresh.get(a))}
                    for a in addresses],
        "changed": [{"address": c["address"], "text": c["after"]} for c in changed],
    }, None
