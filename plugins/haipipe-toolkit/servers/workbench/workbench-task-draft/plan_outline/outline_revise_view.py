"""Revise view, the screen half: one paragraph's rows form and the view's CSS and Save script.

Moved out of outline_revise.py (the 600-line rule); outline_revise re-exports every name here.
"""
from __future__ import annotations

import html
import json

from live.outline_revise_text import box_text, screen_rows


def _e(value) -> str:
    return html.escape(str(value), quote=True)


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

