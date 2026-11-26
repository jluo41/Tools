document.head.insertAdjacentHTML('beforeend', "<style>\n.el-on{outline:2px solid var(--accent)!important;outline-offset:1px;background:color-mix(in srgb,var(--accent) 8%,transparent)}\n.el-tag{position:absolute;z-index:41;padding:1px 7px;border-radius:5px 5px 0 0;background:var(--accent);color:var(--bg);\n font:600 11px/18px system-ui,sans-serif;pointer-events:none}\n.el-pop{position:absolute;margin:0;inset:auto;border:1px solid var(--line);border-radius:10px;background:var(--bg);\n color:var(--ink);box-shadow:0 8px 28px rgba(0,0,0,.14);font:13px/1.4 system-ui,-apple-system,sans-serif;padding:6px}\n.el-menu{min-width:200px}.el-menu button{display:block;width:100%;text-align:left;padding:6px 10px;border-radius:6px}\n.el-menu hr{border:0;border-top:1px solid var(--line);margin:4px 2px}\n.el-head{display:flex;align-items:center;gap:8px;padding:4px 8px 6px}\n.el-kind{flex:none;padding:0 7px;border-radius:5px;background:var(--soft);color:var(--accent);font:600 11px/18px system-ui}\n.el-name{font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}\n.el-card{width:min(360px,92vw);padding:8px 8px 10px}.el-card .el-head{padding:2px 4px 8px}\n.el-x{margin-left:auto;padding:0 6px;color:var(--muted)}\n.el-meta{display:grid;gap:2px;padding:0 4px 8px;border-bottom:1px solid var(--line);color:var(--muted);font-size:12px}\n.el-meta code{font-size:11.5px;color:var(--ink)}.el-copy{padding:0 4px;font-size:12px;color:var(--muted)}\n.el-card .im-slot-in{margin:8px 0 0;padding:0 4px;border:0}\n.el-card [data-im-act=check],.el-card [data-im-act=uncheck]{display:none}\n.el-pop button{border:0;background:none;font:inherit;color:inherit;cursor:pointer}.el-menu button:hover{background:var(--soft)}</style>");
window.__elInfo = {"kinds": [["title", "h1", "focus_shell.page_shell"], ["view-button-list", "#rows [data-row]", "focus_jobs.section / job_pane"], ["band", "#body h2", "focus_render.around_work / work_frame"], ["fold", "details.band-sec", "work_frame.section / focus_plan_results.numbered"], ["job-row", "details.job-row", "focus_plan_results.tasks_section"]], "slots": {}, "empty": "", "page": "blueprints/Project-Ladder/work/b17_theme_work"};
document.addEventListener('DOMContentLoaded', function(){
(function(){if(window.__elInfoOn)return;window.__elInfoOn=1;var D=window.__elInfo;
var ONE={path:1,title:1,'view-button-list':1,'left-rail':1};   // one per page: its kind is its address
function slug(t){return (t||'').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'').slice(0,40)||'x';}
function view(){var q=new URLSearchParams(location.search);return slug(q.get('group')||((document.querySelector('.section-views [aria-current]')||{}).textContent)||'page');}
function label(el){var h=el.matches('details')?el.querySelector(':scope>summary'):el.matches('section.fd-sec')?el.querySelector('h3'):el;
 return ((h||el).textContent||'').replace(/\s+/g,' ').replace(/^\d+\s*·\s*/,'').replace(/[☆★]/g,'').trim();}
function tag(){D.kinds.forEach(function(k){document.querySelectorAll(k[1]).forEach(function(el){
 if(el.closest('.el-pop'))return;el.dataset.el=k[0];el.dataset.elBy=k[2];
 var vb=el.closest('[data-view]');   // on a page of bands, the band names the view
 el.dataset.elAddr=ONE[k[0]]?'el.'+k[0]:'el.'+(vb?slug(vb.dataset.view):view())+'.'+k[0]+'.'+slug(label(el));});});}
tag();new MutationObserver(tag).observe(document.body,{childList:true,subtree:true});
function mk(c){var d=document.createElement('div');d.className='el-pop '+c;d.setAttribute('popover','manual');   // closed by us only: a right-button release is not a dismiss
document.body.appendChild(d);return d;}
var menu=mk('el-menu'),card=mk('el-card'),chip=document.createElement('span');chip.className='el-tag';chip.hidden=true;document.body.appendChild(chip);
var cur=null,at={x:0,y:0};
function esc(t){var d=document.createElement('div');d.textContent=t;return d.innerHTML;}
function head(el,x){return '<div class=el-head><span class=el-kind>'+esc(el.dataset.el)+'</span><span class=el-name>'+esc(label(el).slice(0,60))+'</span>'+(x?'<button type=button class=el-x data-el-do=close aria-label=Close>✕</button>':'')+'</div>';}
function on(el){off();cur=el;el.classList.add('el-on');var r=el.getBoundingClientRect();
 chip.textContent=el.dataset.el;chip.style.top=(scrollY+r.top-19)+'px';chip.style.left=(scrollX+r.left)+'px';chip.hidden=false;}
function hide(p){if(p.matches(':popover-open'))p.hidePopover();}
function off(){if(cur)cur.classList.remove('el-on');chip.hidden=true;}
function put(p){p.style.left=Math.min(at.x,scrollX+innerWidth-p.offsetWidth-12)+'px';p.style.top=at.y+'px';}
document.addEventListener('contextmenu',function(e){if(e.shiftKey||card.contains(e.target)||menu.contains(e.target))return;   // shift: the browser's own menu
 var el=e.target.closest&&e.target.closest('[data-el]');if(!el)return;e.preventDefault();
 hide(menu);hide(card);on(el);at={x:e.pageX,y:e.pageY};
 menu.innerHTML=head(el)+'<hr><button type=button data-el-do=info>ℹ️ Info</button><button type=button data-el-do=comment>💬 Comment…</button><button type=button data-el-do=copy>📋 Copy address</button>';
 menu.showPopover();put(menu);});
function open(focus){var el=cur,a=el.dataset.elAddr,slot=D.slots[a]||D.empty.split('ELADDR').join(a);
 card.innerHTML=head(el,1)+'<div class=el-meta><span><code>'+esc(a)+'</code><button type=button class=el-copy data-el-do=copy title="Copy address">📋</button></span><span>drawn by <code>'+esc(el.dataset.elBy)+'</code></span></div>'+slot;
 var s=card.querySelector('[data-im-slot]');if(s)s.hidden=false;card.showPopover();put(card);
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
});
