"""Right-click any element of a focus page: it lights up with its kind on a tab, and a small menu offers Info, Comment
and Copy address; Info and Comment open its card (kind, name, address, what draws it, its comments). Shift+right-click
keeps the browser's own menu (JL 261124: "every element will have that"; "what if we can right click").
On a phone the same menu opens from a long press of about 500 ms (a move, a scroll, a second finger or a pointercancel
cancels it; a press inside an input keeps the browser's text selection), and the card is a bottom panel that stays
above the software keyboard. The page carries no standing button for it.

The kinds are the page parts of hai-ui SKILL.md "Page parts" (band, fold, bar, ...), each found by its CSS
selector, so no writer of a band or a fold changes. An element's address is `el.<view>.<kind>.<name>`, or `el.<kind>`
for a one-per-page part (path, title, view-button-list, left-rail); its comments are item cards (ref/cards.md) written
by the one writer, POST /_board/item-card, into the page's records/.
"""
from __future__ import annotations

import json
from pathlib import Path

from live import item_cards as IC
from live.item_marks import ASSETS as IM_ASSETS, card_slot

# (kind, CSS selector, what draws it): the page parts, innermost last so a fold inside a band wins on hover
KINDS = (
    ("path", ".focus-crumb", "focus_render.crumbs_goal_source"),
    ("title", ".focus-page h1", "focus_shell.page_shell"),
    ("view-button-list", ".section-views", "focus_shell.page_shell (views_bar)"),
    ("band", ".work-section-group>h2, h3.wk-band, h3.pb-group", "focus_render.around_work / work_frame"),
    ("fold", "details.band-sec, section.fd-sec", "work_frame.section / focus_plan_results.numbered"),
    ("job-row", "details.job-row", "focus_plan_results.job_row"),
    ("tree-row", ".fold-row", "focus_tree.fold_tree"),
    ("left-rail", "nav.focus-rail.left", "focus_render.left_rail"),
)
MARK = "ELADDR"                                      # stands for the address in the empty card template


def assets(folder: Path, root: Path) -> str:
    """The ⓘ layer for one page: the card styles and writer script, the kinds, and the comment threads already kept."""
    rel = folder.relative_to(root).as_posix() if folder != root else ""
    try:
        kept = IC.cards(folder)
    except OSError:
        kept = {}
    have = {a: card_slot(a, kept, rel) for a in kept if a.startswith("el.")}
    try:                                             # a Studio type's elements: what each is and why (studio_types)
        from live.studio_types import element_about
        about = element_about(root)
    except Exception:
        about = []
    data = {"kinds": [[k, s, w] for k, s, w in KINDS], "slots": have, "empty": card_slot(MARK, {}, rel),
            "page": rel, "about": about}
    return IM_ASSETS + STYLE + f'<script>window.__elInfo={json.dumps(data)};</script>' + SCRIPT


STYLE = """<style>
.el-on{outline:2px solid var(--accent)!important;outline-offset:1px;background:color-mix(in srgb,var(--accent) 8%,transparent)}
.el-tag{position:absolute;z-index:41;padding:1px 7px;border-radius:5px 5px 0 0;background:var(--accent);color:var(--bg);
 font:600 11px/18px system-ui,sans-serif;pointer-events:none}
.el-pop{position:absolute;margin:0;inset:auto;border:1px solid var(--line);border-radius:10px;background:var(--bg);
 color:var(--ink);box-shadow:0 8px 28px rgba(0,0,0,.14);font:13px/1.4 system-ui,-apple-system,sans-serif;padding:6px}
.el-menu{min-width:200px}.el-menu button{display:block;width:100%;text-align:left;padding:6px 10px;border-radius:6px}
.el-menu hr{border:0;border-top:1px solid var(--line);margin:4px 2px}
.el-head{display:flex;align-items:center;gap:8px;padding:4px 8px 6px}
.el-kind{flex:none;padding:0 7px;border-radius:5px;background:var(--soft);color:var(--accent);font:600 11px/18px system-ui}
.el-name{font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.el-card{width:min(360px,92vw);padding:8px 8px 10px}.el-card .el-head{padding:2px 4px 8px}
.el-x{margin-left:auto;padding:0 6px;color:var(--muted)}
.el-meta{display:grid;gap:2px;padding:0 4px 8px;border-bottom:1px solid var(--line);color:var(--muted);font-size:12px}
.el-meta code{font-size:11.5px;color:var(--ink)}.el-copy{padding:0 4px;font-size:12px;color:var(--muted)}
.el-about{padding:0 8px 6px;max-width:340px}.el-about p{margin:3px 0;font-size:12.5px}.el-about b{display:inline-block;min-width:38px;font-size:11px;color:var(--muted);font-weight:600}
.el-about code{font-size:11.5px}.el-about .el-of{color:var(--muted);font-size:11.5px}
.el-card .im-slot-in{margin:8px 0 0;padding:0 4px;border:0}
.el-card [data-im-act=check],.el-card [data-im-act=uncheck]{display:none}
.el-press,.el-press *{-webkit-user-select:none!important;user-select:none!important;-webkit-touch-callout:none!important}
.el-pop.el-sheet{position:fixed;left:0;right:0;top:auto;bottom:var(--el-kb,0px);width:auto;max-height:calc(var(--el-vh,100vh) - 24px);
 overflow:auto;border-radius:14px 14px 0 0;padding:10px 12px calc(12px + env(safe-area-inset-bottom,0px));box-shadow:0 -8px 28px rgba(0,0,0,.18)}
.el-pop.el-sheet textarea,.el-pop.el-sheet input{font-size:16px}.el-pop.el-sheet .im-slot-in{max-width:none}
</style>"""

SCRIPT = """<script>
(function(){if(window.__elInfoOn)return;window.__elInfoOn=1;var D=window.__elInfo;
var ONE={path:1,title:1,'view-button-list':1,'left-rail':1};   // one per page: its kind is its address
function slug(t){return (t||'').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'').slice(0,40)||'x';}
function view(){var q=new URLSearchParams(location.search);return slug(q.get('group')||((document.querySelector('.section-views [aria-current]')||{}).textContent)||'page');}
function label(el){var h=el.matches('details')?el.querySelector(':scope>summary'):el.matches('section.fd-sec')?el.querySelector('h3'):el;
 return ((h||el).textContent||'').replace(/\\s+/g,' ').replace(/^\\d+\\s*·\\s*/,'').replace(/[☆★]/g,'').trim();}
function tag(){D.kinds.forEach(function(k){document.querySelectorAll(k[1]).forEach(function(el){
 if(el.closest('.el-pop'))return;el.dataset.el=k[0];el.dataset.elBy=k[2];
 var vb=el.closest('[data-view]');   // on a page of bands, the band names the view
 el.dataset.elAddr=ONE[k[0]]?'el.'+k[0]:'el.'+(vb?slug(vb.dataset.view):view())+'.'+k[0]+'.'+slug(label(el));});});
 (D.about||[]).forEach(function(a,i){try{document.querySelectorAll(a.css).forEach(function(el){   // a Studio type's element: named by its type
  if(el.closest('.el-pop')||(a.text&&(el.textContent||'').replace(/\\s+/g,' ').trim()!==a.text))return;
  el.dataset.el=slug(a.name);el.dataset.elAbout=i;el.dataset.elAddr='el.'+view()+'.'+slug(a.name);});}catch(e){}});}
tag();new MutationObserver(tag).observe(document.body,{childList:true,subtree:true});
function mk(c){var d=document.createElement('div');d.className='el-pop '+c;d.setAttribute('popover','manual');   // closed by us only: a right-button release is not a dismiss
document.body.appendChild(d);return d;}
var menu=mk('el-menu'),card=mk('el-card'),chip=document.createElement('span');chip.className='el-tag';chip.hidden=true;document.body.appendChild(chip);
var cur=null,at={x:0,y:0};
function esc(t){var d=document.createElement('div');d.textContent=t;return d.innerHTML;}
function about(el){var a=el.dataset.elAbout!==undefined&&D.about[+el.dataset.elAbout];if(!a)return '';
 return '<div class=el-about>'+(a.what?'<p><b>What</b> '+esc(a.what)+'</p>':'')+(a.why?'<p><b>Why</b> '+esc(a.why)+'</p>':'')+(a.from?'<p><b>From</b> '+esc(a.from).replace(/`([^`]+)`/g,'<code>$1</code>')+'</p>':'')+(a.type?'<p class=el-of>'+esc(a.type)+'</p>':'')+'</div>';}
function head(el,x){var a=el.dataset.elAbout!==undefined&&D.about[+el.dataset.elAbout];
 if(a)return '<div class=el-head><span class=el-kind>element</span><span class=el-name>'+esc(a.name)+'</span>'+(x?'<button type=button class=el-x data-el-do=close aria-label=Close>✕</button>':'')+'</div>';
 return '<div class=el-head><span class=el-kind>'+esc(el.dataset.el)+'</span><span class=el-name>'+esc(label(el).slice(0,60))+'</span>'+(x?'<button type=button class=el-x data-el-do=close aria-label=Close>✕</button>':'')+'</div>';}
function on(el){off();cur=el;el.classList.add('el-on');var r=el.getBoundingClientRect();
 chip.textContent=el.dataset.el;chip.style.top=(scrollY+r.top-19)+'px';chip.style.left=(scrollX+r.left)+'px';chip.hidden=false;}
function hide(p){if(p.matches(':popover-open'))p.hidePopover();}
function off(){if(cur)cur.classList.remove('el-on');chip.hidden=true;}
var touch=false,touchAt=0,press=null,eat=false,ids=new Set(),vv=window.visualViewport;   // touch: this menu came from a long press
function put(p){p.style.left=Math.max(scrollX+4,Math.min(at.x,scrollX+innerWidth-p.offsetWidth-12))+'px';
 p.style.top=(touch?Math.max(scrollY+4,Math.min(at.y,scrollY+innerHeight-p.offsetHeight-12)):at.y)+'px';}
function kb(){if(!vv)return;card.style.setProperty('--el-kb',Math.max(0,innerHeight-vv.height-vv.offsetTop)+'px');   // the keyboard's height:
 card.style.setProperty('--el-vh',vv.height+'px');}                                                            // the panel sits on top of it
if(vv){vv.addEventListener('resize',kb);vv.addEventListener('scroll',kb);}
document.addEventListener('contextmenu',function(e){if(e.shiftKey||card.contains(e.target)||menu.contains(e.target))return;   // shift: the browser's own menu
 if(press){e.preventDefault();fire();return;}                    // a touch browser's own long-press event: one menu, opened now
 if(Date.now()-touchAt<1500){e.preventDefault();return;}         // ... or already opened by the timer: never a second one
 var el=e.target.closest&&e.target.closest('[data-el]');if(!el)return;e.preventDefault();
 touch=false;show(el,e.target,e.pageX,e.pageY);});
function show(el,target,x,y){var e={target:target};
 hide(menu);hide(card);on(el);at={x:x,y:y};
 menu.innerHTML=head(el)+about(el)+'<hr><button type=button data-el-do=info>ℹ️ Info</button><button type=button data-el-do=comment>💬 Comment…</button><button type=button data-el-do=copy>📋 Copy address</button>';
 menu.showPopover();put(menu);
 var own=e.target.closest('[data-path]'),link=el.matches('a[href*="path="]')?el:el.querySelector('a[href*="path="]');
 if(own&&own!==el&&!el.contains(own))own=null;   // its folder: the row clicked inside it, else its own link
 var p=own?own.dataset.path:link&&new URL(link.href,location.href).searchParams.get('path');
 if(p&&!touch){if(/\\.[a-z0-9]{1,5}$/i.test(p))p=p.replace(/\\/[^\\/]*$/,'');   // a file: its folder (a phone's pane is a drawer: it would cover the menu)
  window.dispatchEvent(new CustomEvent('wb:show-files',{detail:p}));}}   // the Files pane folds to it at once
// a phone: press an element for 500 ms. A move, a scroll, a second finger or a pointercancel drops the press; an input keeps its own selection
function drop(){if(!press)return;clearTimeout(press.t);press=null;document.documentElement.classList.remove('el-press');}
function fire(){var p=press;drop();if(!p||!p.el.isConnected)return;touchAt=Date.now();touch=true;eat=true;
 var s=window.getSelection&&getSelection();if(s&&s.removeAllRanges)s.removeAllRanges();
 show(p.el,p.target,p.x+scrollX,p.y+scrollY);}
document.addEventListener('pointerdown',function(e){if(e.pointerType!=='touch')return;eat=false;ids.add(e.pointerId);
 if(ids.size>1){drop();return;}
 if(menu.contains(e.target)||card.contains(e.target)||!e.target.closest)return;
 if(e.target.closest('input,textarea,select,[contenteditable]:not([contenteditable=false])'))return;
 var el=e.target.closest('[data-el]');if(!el)return;
 press={el:el,target:e.target,x:e.clientX,y:e.clientY,t:setTimeout(fire,500)};document.documentElement.classList.add('el-press');},true);
document.addEventListener('pointermove',function(e){if(press&&e.pointerType==='touch'&&Math.hypot(e.clientX-press.x,e.clientY-press.y)>10)drop();},true);
function up(e){if(e.pointerType!=='touch')return;ids.delete(e.pointerId);drop();if(eat)setTimeout(function(){eat=false;},400);}
document.addEventListener('pointerup',up,true);document.addEventListener('pointercancel',up,true);
window.addEventListener('scroll',drop,true);window.addEventListener('blur',drop);
document.addEventListener('click',function(e){if(!eat||menu.contains(e.target)||card.contains(e.target))return;   // the lift after a long press
 eat=false;e.preventDefault();e.stopPropagation();},true);                                                        // is not a click on the element
function open(focus){var el=cur,a=el.dataset.elAddr,slot=D.slots[a]||D.empty.split('ELADDR').join(a);
 card.innerHTML=head(el,1)+about(el)+'<div class=el-meta><span><code>'+esc(a)+'</code><button type=button class=el-copy data-el-do=copy title="Copy address">📋</button></span>'+(el.dataset.elBy?'<span>drawn by <code>'+esc(el.dataset.elBy)+'</code></span>':'')+'</div>'+slot;
 var s=card.querySelector('[data-im-slot]');if(s)s.hidden=false;card.classList.toggle('el-sheet',touch);card.showPopover();
 if(touch){card.style.left=card.style.top='';kb();}else put(card);
 if(focus){var t=card.querySelector('textarea');if(t)t.focus();}}
document.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('[data-el-do]');if(!b||!cur)return;
 var d=b.dataset.elDo;e.preventDefault();hide(menu);
 if(d==='info'||d==='comment')open(d==='comment');
 else if(d==='copy'){navigator.clipboard&&navigator.clipboard.writeText(cur.dataset.elAddr);b.textContent='✓ Copied';}
 else if(d==='close'){hide(card);off();}});
function done(){hide(menu);hide(card);off();}
document.addEventListener('pointerdown',function(e){if(e.button!==0||menu.contains(e.target)||card.contains(e.target))return;   // a left
 if(menu.matches(':popover-open')||card.matches(':popover-open'))done();});                       // press outside closes
document.addEventListener('keydown',function(e){if(e.key!=='Escape'||e.defaultPrevented)return;   // one Esc, one layer:
 if(menu.matches(':popover-open')||card.matches(':popover-open')){e.preventDefault();done();}});      // the pane stays
})();
</script>"""
