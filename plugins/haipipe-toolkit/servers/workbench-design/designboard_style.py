"""The DesignBoard page's style and its theory script (split from designboard.py, which re-exports every name
here)."""
from __future__ import annotations




_CSS = """
:root{--fg:#1c1c1c;--mut:#6f6f6b;--line:#e4e4e7;--bg:#fff;--acc:#3e5c84;--bad:#b3541e;--ok:#3a7d44;--soft:#f5f6f8;--ext:#7a4f9a;--acc-soft:#e6edf5}
@media(prefers-color-scheme:dark){:root{--fg:#e8e8e6;--mut:#9a9a97;--line:#2c2e33;--bg:#161719;--acc:#7d9cc4;--bad:#e0955a;--ok:#7dbb87;--soft:#20242a;--ext:#b896d6;--acc-soft:#22304a}}
*{box-sizing:border-box}body{margin:0;padding:16px 18px;background:var(--bg);color:var(--fg);font:14px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:1100px}
h1{font-size:18px;margin:0 0 2px;font-weight:700}h2{font-size:14px;margin:18px 0 6px;font-weight:650}
.mut{color:var(--mut);font-size:12.5px}.bad{color:var(--bad)}.ok{color:var(--ok)}
/* one tab style for every workbench, the Guide's: a Space tab is a filled pill when on */
.tabs{display:flex;gap:6px;margin:12px 0 8px;flex-wrap:wrap}
.tabs button{font:400 16px system-ui,sans-serif;padding:6px 14px;border:1px solid #ced4da;border-radius:6px;cursor:pointer;background:#fff;color:#1e1e1e}
.tabs button.on{background:#e7f5ff;color:#1864ab;border-color:#1864ab}
@media(prefers-color-scheme:dark){.tabs button{background:#191c21;color:#edf0f4;border-color:#414852}
.tabs button.on{background:#253749;color:#91caff;border-color:#91caff}}
/* the board header, as the Insight board draws it */
.dataset{margin:10px 0 4px;padding:8px 14px;border:1px solid var(--acc);border-radius:10px;background:var(--acc-soft,#e6edf5);color:var(--acc);font-size:14px}
.pane{display:none}.pane.on{display:block}
table{border-collapse:collapse;width:100%;margin:4px 0 8px}td,th{padding:6px 8px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
th{color:var(--mut);font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.03em}
code{font:12px ui-monospace,Menlo,monospace;word-break:break-word}a{color:var(--acc);text-decoration:none}a:hover{text-decoration:underline}
tr.me td{background:var(--soft)}
.card{border:1px solid var(--line);border-radius:6px;padding:10px 12px;margin:8px 0}
.card .head{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
pre.text{margin:8px 0;padding:10px 12px;background:var(--soft);border-left:3px solid var(--acc);font:15px/1.45 -apple-system,sans-serif;white-space:pre-wrap;word-break:break-word}
table.designs td.who{width:230px}.design{white-space:pre-wrap;word-break:break-word;font-size:14.5px}
img.shot{display:block;width:100%;height:auto;margin:0 0 6px;border:1px solid var(--line);border-radius:18px;background:#fff}
.gallery{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:20px 18px;margin:10px 0}
.gallery figure{margin:0}.gallery figcaption{font-size:13px;line-height:1.35}
button.do{font:600 12.5px -apple-system,sans-serif;border:1px solid var(--acc);border-radius:4px;padding:3px 9px;background:var(--bg);color:var(--acc);cursor:pointer}
.msg{font-size:12.5px}.msg.bad{color:var(--bad)}.msg.ok{color:var(--ok)}
.empty{color:var(--mut);padding:10px 0}
details{margin:2px 0}summary{cursor:pointer;color:var(--acc);font-size:12.5px}
.form{display:grid;grid-template-columns:110px 1fr;gap:6px 10px;max-width:760px;margin:6px 0}
.form label{color:var(--mut);font-size:12px;padding-top:5px}
.form input,.form textarea,.form select{font:13px -apple-system,sans-serif;border:1px solid var(--line);border-radius:4px;padding:4px 6px;background:var(--bg);color:var(--fg)}
.form textarea{min-height:72px}.form .full{grid-column:1/3}
details.taskblock{border:1px solid var(--line);border-radius:6px;padding:8px 12px;margin:8px 0}
details.taskblock>summary{font-size:14px;color:var(--fg)}
.task{border:1px solid var(--acc);border-radius:8px;background:var(--soft);padding:8px 12px;margin:10px 0}
article.theory{max-width:980px}article.theory h1{font-size:16px;margin:8px 0 6px}article.theory h2{margin:22px 0 6px}
article.theory p{margin:6px 0;line-height:1.55}pre.theory{margin:8px 0;padding:10px 12px;background:var(--soft);border-radius:6px;font:12px/1.5 ui-monospace,Menlo,monospace;overflow-x:auto}
/* the Method page: a part (A · …) above its sub-sections (A1 · …) (Paper session, 261003) */
article.theory h2{font-size:18px;margin:28px 0 8px;padding-top:12px;border-top:1px solid var(--line)}
article.theory h3{font-size:14.5px;margin:18px 0 6px;font-weight:650}
details.draw-fold,details.sec-fold{margin:4px 0 12px;border:1px solid #dee2e6;border-radius:8px}
details.sec-fold>summary{padding:14px 16px;cursor:pointer}details.sec-fold>summary strong{color:#1864ab;font-size:18px;font-weight:500}
.sec-body{padding:0 18px 14px}.sec-body>h3:first-child{margin-top:4px}
@media(prefers-color-scheme:dark){details.sec-fold{border-color:#414852}
details.sec-fold>summary strong{color:#91caff}}
details.draw-fold>summary{padding:14px 16px;cursor:pointer}details.draw-fold>summary strong{color:#1864ab;font-size:18px;font-weight:500}
details.draw-fold>summary span{display:block;color:var(--mut);font-size:14px;margin-top:3px;margin-left:18px}.draw-body{padding:0 12px 12px}
@media(prefers-color-scheme:dark){details.draw-fold{border-color:#414852}details.draw-fold>summary strong{color:#91caff}}
details.ref-fold{margin:22px 0 0;border-top:1px solid var(--line);padding-top:10px}
details.ref-fold>summary{cursor:pointer;font-weight:650;font-size:15px}
ul.fam-methods{margin:4px 0 10px;padding-left:18px}ul.fam-methods li{margin:3px 0}
.steps{display:flex;gap:6px;flex-wrap:wrap;margin:6px 0 12px}
.steps button{font:400 14px system-ui,sans-serif;padding:4px 12px;border:1px solid #ced4da;border-radius:14px;background:#fff;color:#1e1e1e;cursor:pointer}
.steps button.on{background:#f1f3f5;border-color:#495057;font-weight:600}
.step{display:none}.step.on{display:block}.step-card{border:1px solid #dee2e6;border-radius:8px;padding:2px 14px;margin:0 0 12px;background:#f8f9fa}
details.packet{border:1px solid #dee2e6;border-radius:8px;margin:0 0 10px}
details.packet>summary{padding:8px 12px;cursor:pointer}.packet-body{padding:0 14px 8px;max-height:520px;overflow:auto}
table.msgs td:first-child{white-space:nowrap}table.msgs td.msg-text{font-family:ui-monospace,Menlo,monospace;font-size:13px;width:52%}
@media(prefers-color-scheme:dark){.steps button{background:#191c21;color:#edf0f4;border-color:#414852}
.steps button.on{background:#253749}.step-card,details.packet{border-color:#414852;background:transparent}}
/* a View (sub-Space) tab, the same look as a Space tab */
.views{display:flex;gap:6px;flex-wrap:wrap;padding:0 0 10px;margin:0 0 12px;border-bottom:1px solid var(--line)}
.views button{font:400 16px system-ui,sans-serif;padding:6px 14px;border:1px solid #ced4da;border-radius:6px;background:#fff;color:#1e1e1e;cursor:pointer}
.views button.on{background:#e7f5ff;color:#1864ab;border-color:#1864ab}
@media(prefers-color-scheme:dark){.views button{background:#191c21;color:#edf0f4;border-color:#414852}
.views button.on{background:#253749;color:#91caff;border-color:#91caff}}
.view{display:none}.view.on{display:block}
.rp-head{font:700 12px -apple-system,sans-serif;text-transform:uppercase;letter-spacing:.04em;color:var(--mut);margin:0 0 2px}
details.rp-venues{margin:0 0 10px}details.rp-more{margin:2px 0 4px}
details.rp-more>summary{font-size:12.5px;color:var(--mut);padding:2px 0}
details.rp-more[open]>summary{margin-bottom:4px}details.rp-venues>div{margin-top:4px;line-height:1.6}
.lw-k{font:700 11.5px -apple-system,sans-serif;text-transform:uppercase;letter-spacing:.04em;color:var(--acc);margin:14px 0 6px}
.lw-kn{font-weight:500;text-transform:none;letter-spacing:0;opacity:.85;margin-left:6px}
.rp-group{border:1px solid var(--line);border-radius:10px;overflow:hidden;margin:0 0 4px}
.rp-card+.rp-card{border-top:1px solid var(--line)}
.rp-card>summary{list-style:none;cursor:pointer;display:grid;grid-template-columns:1em minmax(0,1fr);gap:6px;align-items:baseline;padding:10px 14px}
.rp-card>summary::-webkit-details-marker{display:none}.rp-card>summary:hover,.rp-card[open]>summary{background:var(--soft)}
.bjt-chev{color:var(--mut);display:inline-block;width:1em;text-align:center;transition:transform .12s ease}
.rp-card[open]>summary .bjt-chev{transform:rotate(90deg)}
.lw-sum{min-width:0}.rp-title{font-weight:600;font-size:14.5px;line-height:1.4;color:var(--fg)}
.rp-sub{display:flex;justify-content:space-between;align-items:baseline;gap:12px;margin-top:2px;font-size:13px;color:var(--mut)}
.rp-marks{display:flex;gap:10px;flex:none}.rp-utd{font:700 10.5px -apple-system,sans-serif;color:#9c6500;border:1px solid #e3c27a;border-radius:4px;padding:0 4px;letter-spacing:.03em}
.rp-q{color:var(--acc);font-weight:600}.rp-q.rp-evidence{color:var(--ok)}
.rp-q.rp-classic{color:var(--mut)}
.rp-body{padding:6px 14px 14px calc(14px + 1em + 6px)}.rp-why{font-size:14.5px;line-height:1.55;margin:4px 0 6px}
.rp-acts{display:flex;gap:6px 16px;flex-wrap:wrap;font-size:13.5px;margin:0 0 6px}.rp-nopdf{font-size:13.5px;margin-top:8px}
details.rp-absd>summary{font-size:13px;color:var(--mut);cursor:pointer}details.rp-absd>p{font-size:13.5px;line-height:1.55;margin:4px 0 6px}
.st-bar{display:flex;justify-content:space-between;gap:12px;align-items:baseline;margin:0 0 6px;font-size:13px}
.st-frame{display:block;width:100%;height:calc(100vh - 210px);min-height:560px;border:1px solid var(--line);border-radius:8px;background:#fff}
.rp-frame{display:block;width:100%;height:82vh;border:1px solid var(--line);border-radius:8px;background:#fff;margin-top:8px}
table.mdt{display:table;width:100%;border-collapse:collapse;margin:6px 0 14px;font-size:13.5px}
table.mdt td:first-child{font-weight:600;white-space:nowrap}
.mcards{margin:8px 0 16px}.mc-fam{font-size:13px;margin:14px 0 6px;padding:5px 10px;background:var(--soft);border-radius:6px}
details.mcard{border:1px solid var(--line);border-radius:10px;margin:0 0 8px;background:var(--bg)}
details.mcard>summary{color:var(--fg);list-style:none;cursor:pointer;display:grid;grid-template-columns:1em minmax(0,1fr);gap:6px;align-items:baseline;padding:11px 14px}
details.mcard>summary::-webkit-details-marker{display:none}details.mcard>summary:hover,details.mcard[open]>summary{background:var(--soft)}
details.mcard[open]>summary .bjt-chev{transform:rotate(90deg)}
.mc-top{display:flex;align-items:baseline;gap:8px}.mnum{color:var(--mut);font-weight:500}.mc-name{font-weight:650;font-size:15px}
.mc-status{margin-left:auto;font:600 11.5px -apple-system,sans-serif;white-space:nowrap}
.mc-status.ok{color:var(--ok)}.mc-status.gap{color:var(--bad)}
.mc-status.future{color:var(--acc)}
details.mcard.future{border-style:dashed;border-color:var(--acc)}
.mc-move{margin:2px 0 6px;font-size:14px;line-height:1.45}
.mc-io,.mc-from,.mc-tests,.mc-papers{font-size:12.5px;line-height:1.7}.mc-io .arrow{color:var(--mut);margin:0 6px}
.lbl{display:inline-block;min-width:7.2em;margin-right:4px;color:var(--mut);font-size:11px;text-transform:uppercase;letter-spacing:.03em}
.mc-io .lbl+.chip{margin-left:0}.mc-from .src{white-space:normal}
/* the three inputs a design reads: its requirements, internal insights, external insights */
.chip.in-req{border-color:var(--acc);color:var(--acc)}.chip.in-int{border-color:var(--ok);color:var(--ok)}
.chip.in-ext{border-color:var(--ext);color:var(--ext)}
.mc-body{padding:4px 14px 14px calc(14px + 1em + 6px)}
.mc-cols{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:14px;margin:6px 0 10px}
@media(max-width:900px){.mc-cols{grid-template-columns:minmax(0,1fr)}}
.mc-col{border:1px solid var(--line);border-radius:8px;padding:10px 12px}.mc-col.ai{border-color:var(--acc);background:var(--soft)}
.mc-h{font:700 11.5px -apple-system,sans-serif;text-transform:uppercase;letter-spacing:.04em;color:var(--mut);margin:0 0 6px}
.mc-col.ai .mc-h{color:var(--acc)}
.mc-col dl{margin:0}.mc-col dt{font-weight:650;font-size:12.5px;margin:6px 0 1px}.mc-col dd{margin:0;font-size:13px;line-height:1.5}
.mc-col .line{margin:0 0 3px}.mc-tests .when{margin:0 4px 0 14px}.mc-tests .lbl+.when{margin-left:0}
.chip{display:inline-block;border:1px solid var(--line);border-radius:10px;padding:0 7px;margin:1px 3px 2px 0;font-size:12px;white-space:nowrap}
a.pchip{display:inline-block;border:1px solid var(--line);border-radius:10px;padding:0 7px;margin:1px 3px 2px 0;font-size:12px;white-space:nowrap;background:var(--bg)}
a.pchip:hover{border-color:var(--acc);text-decoration:none}a.pchip .rp-pdf{margin-left:5px;font-size:9.5px;padding:0 4px}
.tcode{font:700 11px ui-monospace,Menlo,monospace;color:var(--acc);border:1px solid var(--acc);border-radius:4px;padding:0 3px;cursor:help}
.when{display:inline-block;color:var(--mut);font-size:11px;text-transform:uppercase;letter-spacing:.03em}
a.cite{white-space:nowrap}a.cite .rp-pdf{margin-left:3px;font-size:9px;padding:0 3px}.ours{color:var(--mut);font-style:italic}
.rp-pdf{font:700 10.5px -apple-system,sans-serif;color:#fff;background:var(--acc);border-radius:4px;padding:1px 5px;letter-spacing:.03em}
.rp-tools{margin:2px 0 8px}.rp-only{font:600 12.5px -apple-system,sans-serif;border:1px solid var(--acc);color:var(--acc);background:transparent;border-radius:14px;padding:3px 11px;cursor:pointer}
.rp-only[aria-pressed=true]{background:var(--acc);color:#fff}
.rp-list.only-pdf .rp-card:not(.has-pdf),.rp-list.only-pdf .rp-band:not(.has-pdf),.rp-list.only-pdf details.rp-more>summary{display:none}
@media(max-width:640px){body{padding:12px}td,th{padding:5px 6px}.form{grid-template-columns:1fr}.form .full{grid-column:1}}
@media(max-width:720px){main table{display:block;max-width:100%;overflow-x:auto}main table code{white-space:nowrap;word-break:normal}}
"""


# Theory › Design theory · Design methods · Methods studio · Papers: one view at a time, a
# paper's PDF loaded only when its card opens, a cited paper opening its card. Guide ›
# Methods frames the same page (render_theory_embed), so both use this one script.
_THEORY_JS = (
    # a Space's views (Theory: Design theory · Design methods · Papers): one shown at a time, kept in the URL
    "function loadFrames(pane){pane.querySelectorAll('.view.on iframe.st-frame[data-src]').forEach(function(f){"
    "if(f.closest('details:not([open])'))return;"          # a closed card's canvas loads when it opens
    "if(!f.getAttribute('src'))f.setAttribute('src',f.dataset.src)})}"
    "document.querySelectorAll('.pane').forEach(loadFrames);"
    "document.querySelectorAll('.views button').forEach(function(b){b.onclick=function(){"
    "var pane=b.closest('.pane');pane.querySelectorAll('.views button').forEach(function(x){x.classList.toggle('on',x===b)});"
    "pane.querySelectorAll('.view').forEach(function(v){v.classList.toggle('on',v.dataset.view===b.dataset.view)});"
    "loadFrames(pane);"
    "var u=new URL(location.href);u.searchParams.set('view',b.dataset.view);history.replaceState({},'',u)}});"
    # a paper's PDF loads only when its card opens; toggle does not bubble, so listen in capture
    "document.addEventListener('toggle',function(ev){var d=ev.target;if(d.matches&&d.matches('details.draw-fold')&&d.open)"
    "d.querySelectorAll('iframe.st-frame[data-src]').forEach(function(f){if(!f.getAttribute('src'))f.setAttribute('src',f.dataset.src)})},true);"
    "document.addEventListener('toggle',function(ev){var w=ev.target;if(!(w.matches&&w.matches('details.rp-card')))return;"
    "var f=w.open&&w.querySelector('iframe[data-pdf]');if(f&&!f.getAttribute('src'))f.setAttribute('src',f.dataset.pdf)},true);"
    # a paper named in the Design methods table opens its card in the Papers view
    "function toPaper(id){var c=document.getElementById(id);if(!c)return;var b=document.querySelector('.views button[data-view=papers]');"
    "if(b&&!b.classList.contains('on'))b.click();var f=c.closest('details.rp-more');if(f)f.open=true;c.open=true;"
    "c.scrollIntoView({block:'start'});history.replaceState({},'',location.pathname+location.search+'#'+id)}"
    "document.querySelectorAll('a.to-paper').forEach(function(a){a.onclick=function(e){e.preventDefault();"
    "toPaper(a.getAttribute('href').slice(1))}});"
    "if(location.hash.indexOf('#paper-')===0)toPaper(location.hash.slice(1));"
    # "Show only the papers with a PDF": hide the rest, and open the folds so every PDF card shows
    "document.querySelectorAll('.rp-only').forEach(function(b){b.onclick=function(){var l=b.closest('.rp-list'),"
    "on=!l.classList.contains('only-pdf');l.classList.toggle('only-pdf',on);b.setAttribute('aria-pressed',on);"
    "if(on)l.querySelectorAll('details.rp-more').forEach(function(d){d.open=true})}});"
)


# the theory page sits inside Guide: a pinch over it must not zoom the tab (guide-mount.js says why)
_NO_PINCH = ("<script>addEventListener('wheel',function(e){if(e.ctrlKey)e.preventDefault()},{passive:false});"
             "['gesturestart','gesturechange','gestureend'].forEach(function(t){addEventListener(t,function(e){e.preventDefault()},{passive:false})})</script>")
