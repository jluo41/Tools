"""The insight Board page's stylesheet and scripts, as the strings insightboard.py puts into the page."""

_CSS = """
:root{--bg:#fff;--fg:#1c1c1c;--mut:#6f6f6b;--line:#e3e3e6;--soft:#f4f5f7;--acc:#3e5c84;--acc-soft:#e6edf5;--ok:#3a7d44;--ok-soft:#e5f1e7;--warn:#b3541e;--warn-soft:#f8ebe1;--bad:#8a3b3b;--bad-soft:#f5e6e6;--human:#6b4fa0;--human-soft:#ede8f6;--tab-line:#ced4da;--tab-on:#1864ab;--tab-wash:#e7f5ff}
@media(prefers-color-scheme:dark){:root{--bg:#161719;--fg:#e8e8e6;--mut:#a0a09c;--line:#2c2e33;--soft:#212429;--acc:#8aa7cc;--acc-soft:#22304a;--ok:#7dbb87;--ok-soft:#1f3324;--warn:#e0955a;--warn-soft:#3a2a1c;--bad:#d98b8b;--bad-soft:#3a2323;--human:#b39ddb;--human-soft:#2c2540;--tab-line:#414852;--tab-on:#91caff;--tab-wash:#253749}}
*{box-sizing:border-box}body{margin:0;padding:16px;background:var(--bg);color:var(--fg);font:16px/1.55 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
main{max-width:1600px}h1{font-size:18px;margin:0 0 2px}h2{font-size:17px;margin:0 0 6px}h3{font-size:15px;margin:14px 0 6px}p{margin:4px 0}
.mut{color:var(--mut);font-size:13px}code,.mono{font:13px ui-monospace,Menlo,monospace}a{color:var(--acc)}
.spaces{display:flex;gap:6px;margin:12px 0 8px;flex-wrap:wrap}.space{font:400 16px system-ui,sans-serif;border:1px solid var(--tab-line);border-radius:6px;padding:6px 14px;cursor:pointer;background:var(--bg);color:var(--fg)}.space.on{border-color:var(--tab-on);color:var(--tab-on);background:var(--tab-wash)}
.pane{display:none}.pane.on{display:block}.split{display:flex;align-items:flex-start;gap:14px}
.shell{flex:1 1 auto;border:1px solid var(--line);border-radius:10px;padding:12px 16px 16px;min-width:0;overflow-x:auto}
.wtabs{display:flex;gap:6px;flex-wrap:wrap;padding:0 0 10px;margin:0 0 12px;border-bottom:1px solid var(--line)}.wtab{font:400 16px system-ui,sans-serif;border:1px solid var(--tab-line);border-radius:6px;padding:5px 12px;cursor:pointer;background:transparent;color:var(--fg)}.wtab.on{border-color:var(--tab-on);color:var(--tab-on);background:var(--tab-wash)}
.view{display:none}.view.on{display:block}.lead{margin:0 0 12px;color:var(--mut);font-size:14px}.note{border:1px dashed var(--line);border-radius:8px;padding:10px 12px;color:var(--mut);font-size:14px}
table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}td,th{padding:7px 9px;border:1px solid var(--line);text-align:left;vertical-align:top}th{background:var(--soft);color:var(--mut);font-size:12px;font-weight:650}td.num{text-align:right;font-family:ui-monospace,Menlo,monospace;font-size:13px}.scroll{overflow-x:auto}
.inputs td:first-child{background:var(--soft);color:var(--mut);width:160px}.inputs td{overflow-wrap:anywhere}
.pill{display:inline-block;border:1px solid var(--line);border-radius:999px;padding:1px 8px;font-size:12px;color:var(--mut);white-space:nowrap}.pill.ok{color:var(--ok);border-color:var(--ok);background:var(--ok-soft)}.pill.warn{color:var(--warn);border-color:var(--warn);background:var(--warn-soft)}.pill.bad{color:var(--bad);border-color:var(--bad);background:var(--bad-soft)}.pill.acc{color:var(--acc);border-color:var(--acc);background:var(--acc-soft)}.pill.human{color:var(--human);border-color:var(--human);background:var(--human-soft)}
/* the segments are the Insight Space's Views: the View-tab look (.wtabs/.wtab) */.parts{display:flex;gap:6px;flex-wrap:wrap;padding:0 0 10px;margin:0 0 12px;border-bottom:1px solid var(--line)}.part{font:400 16px system-ui,sans-serif;border:1px solid var(--tab-line);border-radius:6px;padding:5px 12px;cursor:pointer;background:transparent;color:var(--fg)}.part.on{border-color:var(--tab-on);color:var(--tab-on);background:var(--tab-wash)}
.hl{display:none;min-width:760px}.hl.on{display:block}.hl-head{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;padding:6px 10px;border-bottom:1px solid var(--line);color:var(--mut);font-size:13px}
details.lvl{border-bottom:1px solid var(--line)}details.lvl>summary{cursor:pointer;padding:9px 10px;font-weight:650;background:var(--soft)}details.lvl>summary .mut{font-weight:400;margin-left:6px}
.hl-row{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;padding:10px 10px;border-top:1px solid var(--line);cursor:pointer}.hl-row:hover{background:var(--soft)}.hl-row.on{background:var(--acc-soft)}.hl-row.dim .hl-l{opacity:.6}
.hl-l,.hl-r,.hl-p{min-width:0}.hl-r,.hl-p{border-left:1px solid var(--line);padding-left:14px}
.rp-head{margin:0;font-weight:600}.rp-head a{color:inherit}.rp-text{margin:3px 0 0;font-size:14.5px}.rp-label{margin:0}.rp-title{margin:4px 0 0;font-weight:600}.rp-title a{color:inherit}.rp-tags{margin:3px 0 0;color:var(--mut);font-size:12.5px}
.q-top{display:flex;align-items:center;gap:8px;flex-wrap:wrap}.q-title{margin:4px 0 0}.wk-title{margin:4px 0 0}.q-name{font-size:15px}
.lvl-src{float:right;font-weight:400;font-size:13px}
details.q-more{margin-top:4px;font-size:13.5px}details.q-more>summary{cursor:pointer;color:var(--acc);list-style:none}details.q-more>summary::before{content:'› '}details.q-more[open]>summary::before{content:'⌄ '}
.q-more dl{margin:4px 0 0}.wk-needs{margin:2px 0 6px;padding-left:18px;font-size:13.5px}.wk-needs li{margin:2px 0}.wk-needs li.gap{color:#c0392b}.wk-bind{color:var(--mut)}.q-needs{margin:2px 0 0;padding-left:18px}.q-needs li{margin:2px 0}.q-more dt{color:var(--mut);font-size:12.5px;margin-top:6px}.q-more dd{margin:1px 0 0}.step{white-space:nowrap}.kind{display:inline-block;font:650 12px -apple-system,sans-serif;color:var(--acc);border:1px solid var(--acc);border-radius:999px;padding:0 8px;margin-right:4px}.q-text{margin-top:3px}.q-sub,.wk-sub{display:block;color:var(--mut);font-size:13px;margin-top:2px}
.wk-none{color:var(--mut);font-size:14px;margin:0}.wk-page{margin:4px 0}details.wk>summary{cursor:pointer;list-style:none}details.wk>summary::-webkit-details-marker{display:none}details.wk>summary::before{content:'› ';color:var(--mut)}details.wk[open]>summary::before{content:'⌄ '}
.bj{padding:4px 0 2px 14px;font-size:13.5px}.bj-b{margin-top:4px}.bj-j{margin-left:16px}.bj-tr{margin-left:32px}.bj-tr.bj-flat{margin-left:16px}.bj-tr>summary{cursor:pointer;list-style:none}.bj-tr>summary::-webkit-details-marker{display:none}.bj-runs{margin-left:18px}.bj-run{display:block;text-decoration:none;color:inherit;padding:1px 0;overflow-wrap:anywhere}.bj-run:hover{color:var(--acc)}.idtag{font:13px ui-monospace,Menlo,monospace;color:var(--mut)}
.rp{flex:0 0 clamp(260px,28vw,420px);border:1px solid var(--line);border-radius:10px;background:var(--soft);padding:12px;position:sticky;top:8px;min-width:0;max-height:calc(100vh - 16px);overflow:auto}
.rp-head{display:flex;align-items:center;gap:8px;margin-bottom:8px}.rp-fold{border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg);cursor:pointer;padding:0 7px;font-size:13px}
.rp.folded{flex-basis:42px;padding:10px 6px;cursor:pointer;overflow:hidden}.rp.folded .rp-body,.rp.folded .rp-for{display:none}.rp.folded .rp-head{writing-mode:vertical-rl;margin:0}.rp-types{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px}
.rp-type{font:500 13px -apple-system,sans-serif;border:1px solid var(--line);border-radius:8px;padding:5px 10px;cursor:pointer;background:var(--bg);color:var(--fg)}.rp-type.on{border-color:var(--acc);color:var(--acc);background:var(--acc-soft)}.rp-n{color:var(--mut);margin-left:3px}
.rp-kind{background:var(--bg);border:1px solid var(--line);border-radius:8px;padding:10px 12px}.rp-skill{font-size:13px;color:var(--ok)}.rp-ph{display:flex;justify-content:space-between;align-items:center;font-weight:600;font-size:14px;margin-top:6px}
.rp-copy{font:500 12px -apple-system,sans-serif;border:1px solid var(--line);border-radius:6px;padding:2px 8px;cursor:pointer;background:var(--bg);color:var(--fg)}.rp-prompt pre{white-space:pre-wrap;font:12.5px/1.5 ui-monospace,Menlo,monospace;background:var(--soft);padding:8px;border-radius:6px;margin:6px 0}
.rp-runs{list-style:none;margin:8px 0 0;padding:0;max-height:420px;overflow:auto;font-size:13.5px}.rp-runs li{padding:3px 0;border-top:1px solid var(--line)}.rp-empty{color:var(--mut);font-size:13px}
.gates{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));border:1px solid var(--line);border-radius:8px;overflow:hidden}.gate{padding:8px 9px;border-right:1px solid var(--line);font-size:13px;min-width:0;overflow-wrap:anywhere}.gate:last-child{border-right:0}.gate .k{font:650 13px ui-monospace,Menlo,monospace}.gate .n{display:block;color:var(--mut)}.gate.passed{box-shadow:inset 0 3px 0 var(--ok)}.gate.held{box-shadow:inset 0 3px 0 var(--human)}.gate.refused{box-shadow:inset 0 3px 0 var(--bad)}.gate.pending,.gate.skipped{color:var(--mut)}.gate .who{display:block;margin-top:3px}
.counts{margin:0 0 12px;padding-left:18px}.form{display:grid;gap:12px}.field textarea{width:100%;min-height:64px;border:1px solid var(--line);border-radius:7px;padding:8px;font:15px -apple-system,sans-serif;background:var(--bg);color:var(--fg)}
.btn{border:1px solid var(--acc);border-radius:8px;padding:8px 13px;background:var(--acc);color:#fff;font:650 14px -apple-system,sans-serif;cursor:pointer}.actions{display:flex;gap:10px;align-items:center}.status{font-size:13px;color:var(--mut)}
.pop-bg{position:fixed;inset:0;background:rgba(0,0,0,.35);display:flex;align-items:center;justify-content:center;z-index:50}.pop-bg[hidden]{display:none}.pop-box{width:min(1100px,94vw);height:88vh;background:var(--bg);border-radius:12px;display:flex;flex-direction:column;overflow:hidden}
.pop-bar{display:flex;align-items:center;gap:12px;padding:8px 14px;border-bottom:1px solid var(--line)}.pop-title{font-weight:650;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.pop-x{border:0;background:transparent;font-size:20px;cursor:pointer;color:var(--fg)}.pop-frame{flex:1;border:0;width:100%}
@media(max-width:820px){.gates{grid-template-columns:repeat(4,1fr)}}
.mlib{max-width:1100px}.mviews{display:flex;gap:6px;flex-wrap:wrap;margin:0 0 12px}.mviews button{font:600 12.5px -apple-system,sans-serif;border:1px solid var(--line);border-radius:14px;padding:3px 11px;background:transparent;color:var(--mut);cursor:pointer}
.mviews button.on{color:var(--fg);border-color:var(--acc);background:var(--soft)}.mview{display:none}.mview.on{display:block}
.st-bar{display:flex;gap:14px;align-items:baseline;justify-content:space-between;margin:0 0 8px}.st-bar a{white-space:nowrap}
.mlib .mview[data-mview=studio]{max-width:none}.st-frame{display:block;width:100%;height:calc(100vh - 260px);min-height:560px;border:1px solid var(--line);border-radius:8px;background:#fff}
article.mdoc{font-size:14.5px}article.mdoc h1{font-size:17px;margin:4px 0 6px}article.mdoc h2{font-size:18px;margin:30px 0 8px}article.mdoc h3{font-size:15px;margin:18px 0 6px}article.mdoc p{margin:6px 0;line-height:1.55}
pre.theory{margin:8px 0;padding:10px 12px;background:var(--soft);border-radius:6px;font:12px/1.5 ui-monospace,Menlo,monospace;overflow-x:auto}
table.mdt{width:100%;border-collapse:collapse;margin:6px 0 14px;font-size:13.5px}table.mdt th,table.mdt td{padding:5px 8px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}table.mdt td:first-child{font-weight:600;white-space:nowrap}
.mlib .rp-head{display:block;font:700 12px -apple-system,sans-serif;text-transform:uppercase;letter-spacing:.04em;color:var(--mut);margin:0 0 2px}
.mlib .rp-tools{margin:2px 0 8px}.mlib .rp-only{font:600 12.5px -apple-system,sans-serif;border:1px solid var(--acc);color:var(--acc);background:transparent;border-radius:14px;padding:3px 11px;cursor:pointer}.mlib .rp-only[aria-pressed=true]{background:var(--acc);color:#fff}
.rp-list.only-pdf .rp-card:not(.has-pdf),.rp-list.only-pdf .rp-band:not(.has-pdf),.rp-list.only-pdf details.rp-more>summary{display:none}
details.rp-venues{margin:0 0 10px}details.rp-more{margin:2px 0 4px}details.rp-more>summary{font-size:12.5px;color:var(--mut);padding:2px 0;cursor:pointer}details.rp-venues>summary{font-size:12.5px;color:var(--acc);cursor:pointer}details.rp-venues>div{margin-top:4px;line-height:1.6}
.lw-k{font:700 11.5px -apple-system,sans-serif;text-transform:uppercase;letter-spacing:.04em;color:var(--acc);margin:14px 0 6px}.lw-kn{font-weight:500;text-transform:none;letter-spacing:0;opacity:.85;margin-left:6px}
.rp-group{border:1px solid var(--line);border-radius:10px;overflow:hidden;margin:0 0 4px}.rp-card+.rp-card{border-top:1px solid var(--line)}
.rp-card>summary{list-style:none;cursor:pointer;display:grid;grid-template-columns:1em minmax(0,1fr);gap:6px;align-items:baseline;padding:10px 14px}
.rp-card>summary::-webkit-details-marker{display:none}.rp-card>summary:hover,.rp-card[open]>summary{background:var(--soft)}
.bjt-chev{color:var(--mut);display:inline-block;width:1em;text-align:center;transition:transform .12s ease}.rp-card[open]>summary .bjt-chev,details.mcard[open]>summary .bjt-chev{transform:rotate(90deg)}
.lw-sum{min-width:0}.mlib .rp-title{margin:0;font-weight:600;font-size:14.5px;line-height:1.4;color:var(--fg)}
.rp-sub{display:flex;justify-content:space-between;align-items:baseline;gap:12px;margin-top:2px;font-size:13px;color:var(--mut)}
.rp-marks{display:flex;gap:10px;flex:none}.rp-utd{font:700 10.5px -apple-system,sans-serif;color:#9c6500;border:1px solid #e3c27a;border-radius:4px;padding:0 4px;letter-spacing:.03em}.rp-pdf{font:700 10.5px -apple-system,sans-serif;color:#fff;background:var(--acc);border-radius:4px;padding:1px 5px;letter-spacing:.03em}
.rp-q{color:var(--acc);font-weight:600}.rp-q.rp-evidence{color:var(--ok)}.rp-q.rp-classic{color:var(--mut)}
.mlib .rp-body{padding:6px 14px 14px calc(14px + 1em + 6px)}.rp-why{font-size:14.5px;line-height:1.55;margin:4px 0 6px}
.rp-acts{display:flex;gap:6px 16px;flex-wrap:wrap;font-size:13.5px;margin:0 0 6px}.rp-nopdf{font-size:13.5px;margin-top:8px}
details.rp-absd>summary{font-size:13px;color:var(--mut);cursor:pointer}details.rp-absd>p{font-size:13.5px;line-height:1.55;margin:4px 0 6px}
.rp-frame{display:block;width:100%;height:82vh;border:1px solid var(--line);border-radius:8px;background:#fff;margin-top:8px}
.mcards{margin:8px 0 16px}.mc-fam{font-size:13px;margin:14px 0 6px;padding:5px 10px;background:var(--soft);border-radius:6px}
details.mcard{border:1px solid var(--line);border-radius:10px;margin:0 0 8px;background:var(--bg)}
details.mcard>summary{color:var(--fg);list-style:none;cursor:pointer;display:grid;grid-template-columns:1em minmax(0,1fr);gap:6px;align-items:baseline;padding:11px 14px}
details.mcard>summary::-webkit-details-marker{display:none}details.mcard>summary:hover,details.mcard[open]>summary{background:var(--soft)}
details.mcard.future{border-style:dashed;border-color:var(--acc)}
.mc-top{display:flex;align-items:baseline;gap:8px}.mnum{color:var(--mut);font-weight:500}.mc-name{font-weight:650;font-size:15px}
.mc-status{margin-left:auto;font:600 11.5px -apple-system,sans-serif;white-space:nowrap}.mc-status.ok{color:var(--ok)}.mc-status.gap{color:var(--warn)}.mc-status.future{color:var(--acc)}
.mc-move{margin:2px 0 6px;font-size:14px;line-height:1.45}
.mc-io,.mc-from,.mc-tests,.mc-papers{font-size:12.5px;line-height:1.7}.mc-io .arrow{color:var(--mut);margin:0 6px}
.lbl{display:inline-block;min-width:7.2em;margin-right:4px;color:var(--mut);font-size:11px;text-transform:uppercase;letter-spacing:.03em}
.mc-body{padding:4px 14px 14px calc(14px + 1em + 6px)}
.mc-cols{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:14px;margin:6px 0 10px}
@media(max-width:900px){.mc-cols{grid-template-columns:minmax(0,1fr)}}
.mc-col{border:1px solid var(--line);border-radius:8px;padding:10px 12px}.mc-col.ai{border-color:var(--acc);background:var(--soft)}
.mc-h{font:700 11.5px -apple-system,sans-serif;text-transform:uppercase;letter-spacing:.04em;color:var(--mut);margin:0 0 6px}.mc-col.ai .mc-h{color:var(--acc)}
.mc-col dl{margin:0}.mc-col dt{font-weight:650;font-size:12.5px;margin:6px 0 1px}.mc-col dd{margin:0;font-size:13px;line-height:1.5}
.mc-col .line{margin:0 0 3px}.mc-tests .when{margin:0 4px 0 14px}.mc-tests .lbl+.when{margin-left:0}
.mlib .pcard{border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin:0 0 16px;background:var(--soft)}.ptitle{font-size:17px;font-weight:600}.psub{color:var(--mut);margin:2px 0 8px}.ptiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px}.ptile{border:1px solid var(--line);border-radius:8px;padding:8px 10px;background:var(--bg)}.ptile b{display:block;font-size:22px;font-weight:600}.ptile span{color:var(--mut);font-size:13px}.pact{border:1px solid var(--line);border-radius:8px;padding:10px 12px;margin:0 0 8px}.pchips{margin-top:6px}.pchips .chip{font-size:13px;padding:1px 8px}.pquote{font-size:17px;margin:0 0 6px}.pq{border:1px solid var(--line);border-radius:8px;margin:0 0 8px;background:var(--bg)}.pq>summary{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 10px;padding:9px 12px;cursor:pointer;list-style:none}.pq>summary::-webkit-details-marker{display:none}.pq[open]>summary{border-bottom:1px solid var(--line)}.pqid{font:600 13px ui-monospace,Menlo,monospace;color:var(--acc)}.pqname{font-weight:600}.pqq{color:var(--mut);flex:1 1 220px}.pqtags{display:flex;flex-wrap:wrap;gap:2px}.pqbody{padding:10px 12px}.pqbody p{margin:0 0 8px}.pretired{margin-top:12px}.pretired>summary{cursor:pointer;color:var(--mut)}.chip{display:inline-block;border:1px solid var(--line);border-radius:10px;padding:0 7px;margin:1px 3px 2px 0;font-size:12px;white-space:nowrap}
a.pchip{display:inline-block;border:1px solid var(--line);border-radius:10px;padding:0 7px;margin:1px 3px 2px 0;font-size:12px;white-space:nowrap;background:var(--bg);text-decoration:none}
a.pchip:hover{border-color:var(--acc)}a.pchip .rp-pdf{margin-left:5px;font-size:9.5px;padding:0 4px}
.tcode{font:700 11px ui-monospace,Menlo,monospace;color:var(--acc);border:1px solid var(--acc);border-radius:4px;padding:0 3px;cursor:help}
.when{display:inline-block;color:var(--mut);font-size:11px;text-transform:uppercase;letter-spacing:.03em}
a.cite{white-space:nowrap}a.cite .rp-pdf{margin-left:3px;font-size:9px;padding:0 3px}.ours{color:var(--mut);font-style:italic}
details.msec{border:1px solid var(--tab-line);border-radius:8px;margin:0 0 12px;background:var(--bg)}details.msec>summary{padding:14px 16px;cursor:pointer}details.msec>summary strong{color:var(--tab-on);font-size:18px;font-weight:500}.msec-body{padding:0 16px 14px}details.draw{border:1px solid var(--line);border-radius:8px;margin:0 0 10px;overflow:hidden}details.draw>summary{cursor:pointer;padding:10px 14px;font-weight:650;background:var(--soft)}details.draw[open]>summary{border-bottom:1px solid var(--line)}details.draw>.st-bar{padding:8px 12px 0}details.draw>.st-frame{border:0;border-radius:0;border-top:1px solid var(--line)}
@media(max-width:600px){body{padding:12px}.spaces{flex-wrap:nowrap;overflow-x:auto}.shell{padding:10px}}
"""

_POP = ('<div class=pop-bg hidden><div class=pop-box><div class=pop-bar><span class=pop-title></span>'
        '<a class=pop-new target=_blank rel=noopener>Open in its own tab ↗</a>'
        '<button type=button class=pop-x aria-label=Close>×</button></div><iframe class=pop-frame></iframe></div></div>')

_JS = """<script>(function(){
var body=document.body;
function setUrl(k,v){try{var u=new URL(location.href);u.searchParams.set(k,v);history.replaceState({},'',u)}catch(e){}}
var sp=[].slice.call(document.querySelectorAll('.space')),pn=[].slice.call(document.querySelectorAll('.pane'));
function space(s,w){if(!document.querySelector('.pane[data-space="'+s+'"]'))s='insight';body.dataset.space=s;sp.forEach(function(b){b.classList.toggle('on',b.dataset.space===s)});pn.forEach(function(p){p.classList.toggle('on',p.dataset.space===s)});if(w)setUrl('space',s)}
sp.forEach(function(b){b.onclick=function(){space(b.dataset.space,true)}});
document.querySelectorAll('.shell').forEach(function(sh){var tabs=[].slice.call(sh.querySelectorAll('.wtab'));function sync(){var on=sh.querySelector('.wtab.on');sh.querySelectorAll('.view').forEach(function(v){v.classList.toggle('on',!!on&&v.dataset.view===on.dataset.view)})}tabs.forEach(function(t){t.onclick=function(){tabs.forEach(function(x){x.classList.toggle('on',x===t)});sync();setUrl('view',t.dataset.view)}});sync()});
try{var vw=new URL(location.href).searchParams.get('view');if(vw)document.querySelectorAll('.pane[data-space="'+body.dataset.space+'"] .wtab[data-view="'+vw+'"]').forEach(function(t){t.click()})}catch(e){}
function part(p,w){document.querySelectorAll('.part').forEach(function(b){b.classList.toggle('on',b.dataset.part===p)});document.querySelectorAll('.hl').forEach(function(t){t.classList.toggle('on',t.dataset.part===p)});if(w)setUrl('p',p)}
document.querySelectorAll('.part').forEach(function(b){b.onclick=function(){part(b.dataset.part,true)}});
var hs=document.querySelector('.hls');if(hs)part(hs.dataset.on,false);
function label(){var r=document.querySelector('.hl-row[data-key="'+body.dataset.sel+'"]');return r?r.dataset.label:''}
function pick(key){body.dataset.sel=key;var lab=label(),k=key.split(':');
 document.querySelectorAll('.hl-row').forEach(function(r){r.classList.toggle('on',r.dataset.key===key)});
 document.querySelectorAll('.rp:not([data-space=scope]) .rp-for').forEach(function(s){s.textContent=lab?'· '+lab:''});
 document.querySelectorAll('.rp-runs li').forEach(function(li){var ks=(li.dataset.keys||'').split(' ');li.hidden=!!key&&ks.indexOf(key)<0});
 document.querySelectorAll('.rp').forEach(function(rp){var best=null;rp.querySelectorAll('.rp-kind').forEach(function(kd){var shown=[].slice.call(kd.querySelectorAll('.rp-runs li')).filter(function(li){return !li.hidden}).length;kd.querySelector('.rp-empty').hidden=shown>0;var t=rp.querySelector('.rp-type[data-k="'+kd.dataset.k+'"]');t.querySelector('.rp-n').textContent=shown;if(shown&&best===null)best=t});
  var on=rp.querySelector('.rp-type.on');if(best&&on&&on.querySelector('.rp-n').textContent==='0')showType(rp,best)});
 document.querySelectorAll('.rp-prompt pre').forEach(function(pre){pre.textContent=pre.dataset.base.replace(/\\{question\\}/g,k[1]||'<question>').replace(/\\{partition\\}/g,k[0]||'<segment>')});
 var any=false;document.querySelectorAll('.gateset').forEach(function(g){g.hidden=g.dataset.key!==key;any=any||!g.hidden});document.querySelectorAll('.gate-none').forEach(function(n){n.hidden=any});
 if(k.length===2){setUrl('q',k[1]);setUrl('p',k[0])}}
document.querySelectorAll('.hl-row').forEach(function(r){r.addEventListener('click',function(ev){if(ev.target.closest('a,summary'))return;pick(r.dataset.key===body.dataset.sel?'':r.dataset.key)})});
function store(k,v){try{if(v===undefined)return localStorage.getItem(k);localStorage.setItem(k,v)}catch(e){return null}}
document.querySelectorAll('.rp').forEach(function(rp){var key='insight-runs-open:'+rp.dataset.space,fb=rp.querySelector('.rp-fold');
 function setFold(on){rp.classList.toggle('folded',on);fb.textContent=on?'◂':'▸';store(key,on?'0':'1')}
 fb.addEventListener('click',function(ev){ev.stopPropagation();setFold(!rp.classList.contains('folded'))});
 rp.addEventListener('click',function(ev){if(rp.classList.contains('folded'))setFold(false)});
 if(store(key)==='1')setFold(false)});
function showType(rp,t){rp.querySelectorAll('.rp-type').forEach(function(x){x.classList.toggle('on',x===t)});rp.querySelectorAll('.rp-kind').forEach(function(k){k.hidden=k.dataset.k!==t.dataset.k})}
document.querySelectorAll('.rp').forEach(function(rp){rp.querySelectorAll('.rp-type').forEach(function(t){t.onclick=function(){showType(rp,t)}})});
document.querySelectorAll('.rp-copy').forEach(function(b){b.onclick=function(){var t=b.closest('.rp-prompt').querySelector('pre').textContent;try{navigator.clipboard.writeText(t).then(function(){b.textContent='Copied'},function(){b.textContent='Select it'})}catch(e){b.textContent='Select it'}}});
var bg=document.querySelector('.pop-bg');
document.addEventListener('click',function(ev){var a=ev.target.closest&&ev.target.closest('a.pop');if(a&&bg&&!(ev.metaKey||ev.ctrlKey)){ev.preventDefault();bg.querySelector('.pop-title').textContent=a.dataset.pop||a.textContent;bg.querySelector('.pop-new').href=a.href;bg.querySelector('.pop-frame').src=a.href;bg.hidden=false;return}
 if(bg&&!bg.hidden&&(ev.target===bg||(ev.target.closest&&ev.target.closest('.pop-x')))){bg.hidden=true;bg.querySelector('.pop-frame').src='about:blank'}},true);
document.addEventListener('keydown',function(ev){if(ev.key==='Escape'&&bg&&!bg.hidden){bg.hidden=true;bg.querySelector('.pop-frame').src='about:blank'}});
var f=document.getElementById('askform');if(f){f.onsubmit=function(ev){ev.preventDefault();var q=document.getElementById('ask-text').value.replace(/\\s+/g,' ').trim();if(!q)return;
var cmd='/hai-insight application '+f.dataset.root+' question "'+q.replace(/"/g,"'")+'"';document.getElementById('ask-cmd').textContent=cmd;document.getElementById('ask-out').hidden=false;
var st=document.getElementById('ask-status');if(navigator.clipboard){navigator.clipboard.writeText(cmd).then(function(){st.textContent='copied'},function(){st.textContent='select and copy the line below'})}else{st.textContent='select and copy the line below'}}}
function mview(box,k,w){box.querySelectorAll('.mviews button').forEach(function(x){x.classList.toggle('on',x.dataset.mview===k)});box.querySelectorAll('.mview').forEach(function(v){v.classList.toggle('on',v.dataset.mview===k)});box.querySelectorAll('.mview.on iframe.st-frame[data-src]').forEach(function(f){if(!f.getAttribute('src'))f.setAttribute('src',f.dataset.src)});if(w)setUrl('mview',k)}
document.querySelectorAll('.mlib').forEach(function(box){box.querySelectorAll('.mviews button').forEach(function(b){b.onclick=function(){mview(box,b.dataset.mview,true)}})});
document.addEventListener('toggle',function(e){var d=e.target;if(!(d.matches&&d.matches('details.msec')&&d.open))return;d.querySelectorAll('iframe.st-frame[data-src]').forEach(function(f){if(!f.getAttribute('src'))f.setAttribute('src',f.dataset.src)})},true);   // a fold's canvas loads when it opens
try{var mv=new URL(location.href).searchParams.get('mview');if(mv)document.querySelectorAll('.mlib').forEach(function(box){if(box.querySelector('.mview[data-mview="'+mv+'"]'))mview(box,mv,false)})}catch(e){}
document.addEventListener('toggle',function(ev){var w=ev.target;if(!(w.matches&&w.matches('details.rp-card')))return;var f=w.open&&w.querySelector('iframe[data-pdf]');if(f&&!f.getAttribute('src'))f.setAttribute('src',f.dataset.pdf)},true);
function toPaper(id){var c=document.getElementById(id);if(!c)return;var box=c.closest('.mlib');if(box)mview(box,'papers',true);var f=c.closest('details.rp-more');if(f)f.open=true;c.open=true;c.scrollIntoView({block:'start'})}
document.querySelectorAll('a.to-paper').forEach(function(a){a.onclick=function(e){e.preventDefault();toPaper(a.getAttribute('href').slice(1))}});
document.querySelectorAll('.rp-only').forEach(function(b){b.onclick=function(){var l=b.closest('.rp-list'),on=!l.classList.contains('only-pdf');l.classList.toggle('only-pdf',on);b.setAttribute('aria-pressed',on);if(on)l.querySelectorAll('details.rp-more').forEach(function(d){d.open=true})}});
space(body.dataset.space,false);pick(body.dataset.sel||'');
})();</script>"""


# Question Book › RoadMap Draw: a row's canvas loads when it opens, view only; Edit drawing reloads it with the pen
# and Finish editing gives the pen back (a generated drawing has no Edit). Open rows are remembered for this board
# in the browser tab.
_STUDIO_JS = """<script>(function(){
var list=document.querySelector('.draw-list');if(!list)return;
var key='insight-draw-open:'+list.dataset.studio,editing=null,saved={};
try{saved=JSON.parse(sessionStorage.getItem(key)||'{}')}catch(e){}
function remember(){try{var o={};list.querySelectorAll('details.draw').forEach(function(d){o[d.dataset.board]=d.open});sessionStorage.setItem(key,JSON.stringify(o))}catch(e){}}
function load(r){var f=r.querySelector('iframe');if(r.open&&f&&!f.getAttribute('src'))f.setAttribute('src',f.dataset.src)}
function stop(){if(!editing)return;var f=editing.querySelector('iframe');f.setAttribute('src',f.dataset.src);editing.querySelector('.draw-edit').textContent='Edit drawing';editing=null}
list.querySelectorAll('details.draw').forEach(function(r){
 if(Object.prototype.hasOwnProperty.call(saved,r.dataset.board))r.open=!!saved[r.dataset.board];
 r.addEventListener('toggle',function(){load(r);remember()});
 var b=r.querySelector('.draw-edit');if(b)b.onclick=function(){if(editing===r){stop();return}stop();editing=r;r.open=true;
  r.querySelector('iframe').setAttribute('src',r.querySelector('iframe').dataset.src+'&edit=1');b.textContent='Finish editing'};
 load(r)});
})();</script>"""
