"""The draft Task page's stylesheet and script, and the rules it borrows from the shared page."""
from __future__ import annotations

from live.ui_parts import WORD_CSS

CSS = """<style>
/* the box is the heading bar only; the content follows below it, unboxed (JL 261031: "could we put the box just in the
   section? and the content below it we should be outside of the box") */
.fd-sec{margin:0 0 12px}
.fd-sec iframe.fd-draw{display:block;width:100%;height:760px;border:1px solid var(--line,#e5e7eb);border-radius:8px}
.fd-h{font-size:15px;font-weight:600;margin:0;display:flex;align-items:center;gap:8px;border:1px solid var(--line);
 border-radius:8px;background:var(--paper);padding:8px 14px}.fd-h::before{flex:none}
.fd-h>.topic-pop,.fd-h>.fd-verb{margin-left:auto;font-size:12.5px;font-weight:400}
.fd-h .topic-pop a{border:1px solid var(--line);border-radius:6px;padding:2px 10px;text-decoration:none}
.fd-body{margin:10px 0 18px;padding:0 2px;overflow-x:auto}.fd-body[hidden]{display:none}
.fd-body .pm-edit{max-height:85vh;overflow:auto;border:1px solid var(--line);border-radius:6px;padding:8px}   /* the map's own frame */
/* one frame level: what sits inside a section's box draws no second box (hai-ui review 261031) */
.fd-sec .fd-sec>.fd-h{border:0;padding:4px 0;background:none}.fd-body .space-empty{border:0;padding:0;background:none}
.fd-body pre,.fd-body .raw-source{border:0;background:var(--wash)}
@media(max-width:700px){.rv-split.wr-split{grid-template-columns:minmax(0,1fr)}}
.focus-content:has(>.fd-sec,>section>.fd-sec){border:0;padding-left:0;padding-right:0;background:none}
.fd-h[data-fold]{cursor:pointer;user-select:none}.fd-h[data-fold]::before{content:"▾";display:inline-block;width:16px;
 color:var(--muted);font-size:12px}.fd-h[aria-expanded="false"]::before{content:"▸"}.fd-h[data-fold]:hover{color:var(--accent)}
.fd-ask{display:flex;align-items:center;gap:12px;padding:9px 14px;border:1px solid var(--line);border-left:3px solid #b35c00;
 border-radius:6px;margin:0 0 12px;font-size:14px}.fd-ask .n{min-width:170px;font-weight:500;overflow-wrap:anywhere}
.fd-ask .d{flex:1;color:var(--muted);font-size:13px}
/* a phone: each evidence card's rows stack under their sentence, the card's words on a line of their own (r02: the
   cards ran 35 px past the screen, "no ev") */
@media(max-width:600px){.rv-card .rv-rows,.rv-card .rv-rows tbody{display:block;width:100%}
 .rv-card .rv-rows tr{display:flex;flex-wrap:wrap;gap:0 6px;padding:4px 0}
 .rv-card .rv-rows td{display:block;width:auto!important;padding:0!important}.rv-card .rv-rows td:last-child{flex:1 1 100%}}
/* a phone: a bar keeps its arrow, title and word on one row, the title wrapping in place (r02: the arrow sat alone on
   the first line and the word fell to a third) */
@media(max-width:600px){.fd-h{flex-wrap:nowrap!important}.fd-h>.word{white-space:normal!important;text-align:right;max-width:42%}}
@media(max-width:600px){.fd-ask{flex-wrap:wrap;gap:4px 10px}.fd-ask .n{min-width:0;flex:1 1 100%}.fd-ask .d{flex:1 1 100%}
 .fd-row{flex-wrap:wrap;gap:2px 10px}.fd-row .n{min-width:0;flex:1 1 100%}}
.fd-run{margin:0 0 6px}.fd-run textarea{width:100%;min-height:36px;resize:vertical;border:1px solid var(--line);border-radius:5px;
 background:var(--wash);padding:6px 10px;font:13px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:var(--ink)}
.fd-run .fd-bar{display:flex;gap:8px;align-items:center;margin-top:4px}.fd-run .fd-bar small{color:var(--muted);font-size:12px}
.fd-btn{font-size:12px;border:1px solid var(--line);border-radius:5px;padding:3px 10px;background:var(--paper);color:var(--ink);
 cursor:pointer;white-space:nowrap;text-decoration:none}.fd-btn:hover{border-color:var(--accent);text-decoration:none}
.fd-row{display:flex;align-items:center;gap:12px;padding:8px 0;border-bottom:1px solid var(--line);font-size:14px}
.fd-row .n{min-width:170px;font-weight:500;overflow-wrap:anywhere}.fd-row .d{flex:1;color:var(--muted);font-size:13px}
.fd-row .w{font-size:12px;white-space:nowrap}
.fd-you{color:#b35c00;font-weight:600}.fd-ok{color:#2b8a3e}
.section-views a .vw{font-size:11px;margin-left:5px;color:var(--muted)}.section-views a .vw.fd-you{color:#b35c00}
.section-views a .vw.fd-ok{color:#2b8a3e}
.fd-text h3{font-size:12px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.05em;margin:18px 0 4px}
.fd-text p{font-size:16px;line-height:1.7;margin:0 0 10px}
@media(max-width:600px){.fd-body td,.fd-body th{min-width:120px}.fd-body pre{white-space:pre-wrap;overflow-wrap:anywhere}
 .fd-row{flex-wrap:wrap}.fd-row .n{min-width:0}}
</style>""" + WORD_CSS                    # each bar's state word and the waiting line under a closed bar (261106)


JS = """<script>(function(){
 if(window.fdCopy)return;window.fdCopy=1;
 function get(k){try{return localStorage.getItem(k)||'';}catch(e){return '';}}   /* the old page's key: the same notes */
 function put(k,v){try{localStorage.setItem(k,v);}catch(e){}}
 function ready(fn){if(document.readyState!=='loading')fn();else document.addEventListener('DOMContentLoaded',fn);}
 ready(function(){
  document.querySelectorAll('.fd-run textarea[data-key]').forEach(function(t){
   if(!t.value)t.value=get(t.dataset.key);t.addEventListener('input',function(){put(t.dataset.key,t.value);});});
  /* each section folds by its heading (JL 261031: "for the view page's subsection, could they be like collapse as well")
     and starts closed on every page (JL 261104: "默认的话，大家都是合着的"); what you open stays open in this browser */
  var page=new URLSearchParams(location.search),at='fd-fold:'+(page.get('path')||'')+':'+(page.get('section')||'')+':'+(page.get('group')||'');
  var shut={};try{shut=JSON.parse(localStorage.getItem(at)||'{}');}catch(e){}
  document.querySelectorAll('section.fd-sec').forEach(function(sec){
   var h=sec.querySelector(':scope>h3.fd-h');if(!h||h.dataset.fold)return;
   var body=document.createElement('div');body.className='fd-body';
   /* the waiting line stays under the bar, outside the fold, so it shows while the section is closed (261106) */
   for(var n=h.nextSibling,x;n;n=x){x=n.nextSibling;if(!(n.classList&&n.classList.contains('fd-wait')))body.appendChild(n);}
   sec.appendChild(body);
   /* the remembered state keys on the title alone: the state word on the right changes with the work (261106) */
   var c=h.cloneNode(true);c.querySelectorAll('.word').forEach(function(w){w.remove();});
   var key=c.textContent.trim().slice(0,80);h.dataset.fold='1';h.tabIndex=0;h.setAttribute('role','button');
   function set(open){body.hidden=!open;h.setAttribute('aria-expanded',String(open));}
   set(key in shut?!shut[key]:sec.hasAttribute('data-open'));   /* a Section's Text starts open (261106) */
   function flip(){var open=body.hidden;set(open);shut[key]=open?0:1;
    try{localStorage.setItem(at,JSON.stringify(shut));}catch(e){}window.dispatchEvent(new Event('resize'));}
   h.addEventListener('click',function(ev){if(ev.target.closest('a,button'))return;flip();});
   h.addEventListener('keydown',function(ev){if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();flip();}});
  });
 });
 document.addEventListener('click',function(ev){
  var b=ev.target.closest('.fd-copy,.run-copy');if(!b)return;ev.preventDefault();
  var box=b.closest('.fd-run,.run-prompt-box'),notes=box&&box.querySelector('textarea');
  var text=b.dataset.copy||'';if(notes&&notes.value.trim())text+='\\nuser feedback: '+notes.value.trim();
  if(b.dataset.tail)text+='\\n'+b.dataset.tail;
  var was=b.textContent,done=function(){b.textContent='Copied';setTimeout(function(){b.textContent=was;},1400);};
  cp(text,done);
 });
 /* http has no navigator.clipboard: copy through a hidden textarea then (b16 review 261101: "Copied" copied nothing) */
 function cp(text,done){if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(text).then(done,function(){old(text);done();});}else{old(text);done();}}function old(text){var t=document.createElement('textarea');t.value=text;t.setAttribute('readonly','');t.style.position='fixed';t.style.top='-1000px';document.body.appendChild(t);t.select();try{document.execCommand('copy');}catch(e){}document.body.removeChild(t);}
})();</script>"""


# the classes draft_steps' HTML is drawn with that only the old page's stylesheet defines (frame.CSS, frame.WORK_CSS,
# runs_panel.PANEL_CSS, space_views.SPACE_VIEW_CSS): borrowed rule by rule, so their look keeps one owner
BORROW = ("wf-table", ".st{", ".st ", ".st-ok", ".st-warn", ".st-bar", "chip", "stage", "topic-meta", "topic-pop",
          "space-reads", "space-empty", "space-source", "run-prompt", "work-act", "dl-note", "dl-src")


TOKENS = (":root{--ok:light-dark(#24733d,#8bd49a);--warn:light-dark(#996b00,#e4bd62);--miss:light-dark(#c92a2a,#ff8787);"
          "--tab-line:light-dark(#ced4da,#414852);--tab-on:light-dark(#1864ab,#91caff);--tab-wash:light-dark(#e7f5ff,#253749)}"
          ".focus-content table{display:table}")          # focus.css blocks every table, which shrinks a width:100% one


def _rules(css: str) -> list:
    """The top-level rules of a stylesheet (an @media block is left out: the focus page has its own)."""
    out, depth, start = [], 0, 0
    for i, ch in enumerate(css):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                out.append(css[start:i + 1].strip())
                start = i + 1
    return [r for r in out if not r.startswith("@")]


def borrowed_css() -> str:
    from live import frame
    sheets = [frame.CSS, frame.WORK_CSS]
    for mod, name in (("runs_panel", "PANEL_CSS"), ("space_views", "SPACE_VIEW_CSS")):
        try:
            sheets.append(getattr(__import__(f"live.{mod}", fromlist=[name]), name))
        except Exception:
            pass
    keep = [r for css in sheets for r in _rules(css) if "::before" not in r and any(b in r.split("{", 1)[0] + "{" for b in BORROW)]
    return "<style>" + TOKENS + "".join(keep) + "</style>"
