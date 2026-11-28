"""The Evidence view's stylesheet."""
from __future__ import annotations


_CSS = """
:root{--bg:#ffffff;--fg:#1c1d1f;--mut:#71727a;--line:#e4e4e7;--card:#f7f7f8;
 --acc:#3b6ea5;--ok:#287443;--warn:#a95b12}
@media(prefers-color-scheme:dark){:root{--bg:#161719;--fg:#e8e8e6;--mut:#9a9a97;
 --line:#2c2e33;--card:#1d1f23;--acc:#7aa7d8;--ok:#74b68a;--warn:#e0a05c}}
body{margin:0;background:var(--bg);color:var(--fg);
 font:15px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
header{padding:12px 16px 7px}
.embedded header{display:none}.embedded nav{top:0;padding-top:6px;padding-bottom:6px}
.source-map{margin:8px 16px 6px;color:var(--mut);font:11px/1.45 ui-monospace,Menlo,monospace}
.source-map code{color:var(--fg);font-size:11px}
h1{font-size:16px;margin:0}
.mut{color:var(--mut);font-size:12.5px}.lead{margin:2px 0 0;color:var(--mut);font-size:13px}
nav{display:flex;gap:6px;overflow-x:auto;padding:8px 16px;border-bottom:1px solid var(--line);
 position:sticky;top:0;background:var(--bg);z-index:1}
nav button{border:1px solid var(--line);background:var(--card);color:var(--fg);
 border-radius:6px;padding:4px 10px;font-size:13px;cursor:pointer;white-space:nowrap;flex:none}
nav button.on{border-color:var(--acc);color:var(--acc);font-weight:600}
#items,#runs{padding:12px 16px 20px;max-width:none}
#items pre,#runs pre{background:var(--card);padding:8px 10px;border-radius:6px;
 overflow-x:auto;font:12.5px ui-monospace,Menlo,monospace}
#items code,#runs code{font:12.5px ui-monospace,Menlo,monospace;background:var(--card);
 padding:0 3px;border-radius:4px}
#items h2{font-size:15px;margin:14px 0 4px}
#items h3{font-size:13.5px;margin:12px 0 3px}
#items .run-focus,#runs .run-focus{outline:2px solid var(--acc);outline-offset:4px;border-radius:9px;scroll-margin-top:64px}
#items ul{margin:4px 0;padding-left:22px}
.evsummary{display:flex;align-items:center;gap:6px;flex-wrap:wrap;margin:0 0 12px}
.evsummary span{font-size:11.5px;color:var(--mut);border:1px solid var(--line);border-radius:999px;padding:1px 7px}
.evsummary .cycle{color:var(--acc);border-color:var(--acc);font-weight:650}.evsummary .approved{color:var(--ok);border-color:var(--ok)}
.evcard{border:1px solid var(--line);border-radius:9px;margin:9px 0;background:var(--bg);overflow:hidden}
.evrow.conflict{color:var(--warn,#9a6700)}.evrow.conflict pre{white-space:pre-wrap;overflow-wrap:anywhere;max-width:100%}
.evhead{display:flex;align-items:baseline;gap:7px;flex-wrap:wrap;padding:9px 10px 7px}
.evid{font:650 11px ui-monospace,Menlo,monospace;color:var(--acc);border:1px solid var(--line);border-radius:5px;padding:0 5px;white-space:nowrap}
.evtitle{font-weight:650;line-height:1.4;flex:1;min-width:10em}.evaddr{color:var(--mut);font-size:12px;white-space:nowrap}
.evpills{display:flex;gap:5px;align-items:center}.evpill{font:650 10.5px -apple-system,sans-serif;text-transform:uppercase;letter-spacing:.035em;border-radius:999px;padding:1px 7px;border:1px solid currentColor;white-space:nowrap}
.evpill.specified{color:var(--warn)}.evpill.ready{color:var(--ok)}.evpill.type{color:var(--acc)}
.evrows{border-top:1px solid var(--line);padding:5px 10px 7px}.evrow{display:grid;grid-template-columns:5.8em minmax(0,1fr);gap:7px;padding:3px 0;font-size:13px;line-height:1.48}
.evrow b{font:600 10.5px -apple-system,sans-serif;color:var(--mut);text-transform:uppercase;letter-spacing:.025em}.evrow span{overflow-wrap:anywhere}
.runs{display:flex;gap:4px;flex-wrap:wrap}.runchip{display:inline-flex;align-items:baseline;gap:3px;border:1px solid var(--line);border-radius:5px;padding:1px 5px;font-size:11.5px;line-height:1.4}.runchip .runfam{font:750 9px ui-monospace,Menlo,monospace;color:var(--mut)}.runchip .runfam.discovery{color:#7055a5}.runchip .runfam.execution{color:var(--acc)}.runchip .runfam.paper{color:#356b5d}.runchip .runact{color:var(--mut);font:600 10px ui-monospace,Menlo,monospace}.runchip code{background:none!important;padding:0!important}
.evcard details{border-top:1px solid var(--line);padding:5px 10px 7px;color:var(--mut);font-size:12.5px}.evcard summary{cursor:pointer;color:var(--mut)}.evdetail{margin-top:5px}.evdetail b{display:inline-block;min-width:6.5em;color:var(--mut);font-size:10.5px;text-transform:uppercase;letter-spacing:.025em}
.runmap-card{border:1px solid var(--line);border-radius:9px;margin:8px 0;background:var(--bg);overflow:hidden}
.runmap-head{display:grid;grid-template-columns:auto auto minmax(8em,1fr) auto;align-items:center;gap:7px;padding:8px 10px 6px}
.runmap-eid,.runmap-addr{font:650 11px ui-monospace,Menlo,monospace;white-space:nowrap}.runmap-eid{color:var(--acc)}.runmap-addr{color:var(--mut)}
.runmap-title{font-weight:650;line-height:1.35;min-width:0}.runmap-type{font:650 9.5px -apple-system,sans-serif;color:var(--acc);border:1px solid var(--acc);border-radius:999px;padding:0 6px;letter-spacing:.03em}
.runmap-line{display:grid;grid-template-columns:5.4em minmax(0,1fr);gap:7px;align-items:start;border-top:1px solid var(--line);padding:7px 10px}
.runmap-label{font:600 10px -apple-system,sans-serif;color:var(--mut);text-transform:uppercase;letter-spacing:.035em;padding-top:3px}
.lineage-list{display:flex;flex-wrap:wrap;gap:5px;min-width:0}.lineage-chip{appearance:none;display:inline-flex;align-items:center;gap:5px;max-width:100%;border:1px solid var(--line);border-radius:999px;padding:2px 7px;color:var(--fg);text-decoration:none;background:var(--card);font:11px/1.35 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;cursor:pointer}.lineage-chip:hover,.lineage-chip:focus-visible{border-color:var(--acc);outline:none}
.lineage-chip:before{content:'';width:6px;height:6px;border-radius:50%;background:var(--mut);flex:none}.lineage-chip.ready:before{background:var(--ok)}.lineage-chip.warn:before{background:var(--warn)}.lineage-chip.planned:before{background:var(--mut)}.lineage-chip code{background:none!important;padding:0!important;font-size:11.5px!important;color:inherit}.lineage-chip small{color:var(--mut);font-size:9.5px;white-space:nowrap}
.run-popover{width:min(560px,calc(100vw - 28px));max-height:calc(100dvh - 24px);overflow:auto;overscroll-behavior:contain;-webkit-overflow-scrolling:touch;box-sizing:border-box;border:1px solid var(--line);border-radius:12px;padding:0;background:var(--bg);color:var(--fg);box-shadow:0 18px 55px rgba(0,0,0,.22)}.run-popover::backdrop{background:rgba(0,0,0,.22)}
html.no-popover .run-popover{display:none}html.no-popover .run-popover[data-fallback-open="1"]{display:block;position:fixed;z-index:1000;top:10vh;left:50%;transform:translateX(-50%);max-height:80vh;overflow:auto}
.run-popover-head{position:sticky;top:0;z-index:1;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:10px;align-items:start;padding:13px 14px 10px;border-bottom:1px solid var(--line);background:var(--bg)}.run-popover-title{display:flex;align-items:baseline;gap:8px;flex-wrap:wrap}.run-popover-title code{font-size:14px!important;background:none!important;padding:0!important}.run-availability{font:650 10px -apple-system,sans-serif;text-transform:uppercase;letter-spacing:.04em;color:var(--mut)}.run-close{appearance:none;border:0;background:transparent;color:var(--mut);font-size:20px;line-height:1;cursor:pointer;padding:2px 5px;border-radius:6px}.run-close:hover{background:var(--card);color:var(--fg)}
.run-popover-body{padding:10px 14px 14px}.run-fact{display:grid;grid-template-columns:6.7em minmax(0,1fr);gap:8px;padding:5px 0;font-size:12.5px;line-height:1.5}.run-fact b{font:650 10px -apple-system,sans-serif;text-transform:uppercase;letter-spacing:.035em;color:var(--mut);padding-top:3px}.run-fact span{overflow-wrap:anywhere}.run-fact.primary{padding-top:0;padding-bottom:9px}.run-fact.primary span{color:var(--fg)}.run-popover-path{display:grid;grid-template-columns:6.7em minmax(0,1fr);gap:8px;padding:6px 0;border-top:1px solid var(--line);font-size:12px}.run-popover-path b{font:650 10px -apple-system,sans-serif;text-transform:uppercase;letter-spacing:.035em;color:var(--mut);padding-top:2px}.run-popover-path code{display:block;background:none!important;padding:0!important;white-space:normal;overflow-wrap:anywhere;word-break:break-word;color:var(--fg);user-select:text}.run-popover-path .missing{color:var(--mut)}
.runmap-local{display:flex;align-items:center;flex-wrap:wrap;gap:6px;border-top:1px solid var(--line);padding:4px 10px;color:var(--mut);font-size:11.5px;overflow-wrap:anywhere}.runmap-local b{font-size:9.5px;text-transform:uppercase;letter-spacing:.035em}.runmap-card details{border-top:1px solid var(--line);padding:4px 10px 6px;color:var(--mut);font-size:11.5px}.runmap-card summary{cursor:pointer;font-size:11px}.run-detail{display:grid;grid-template-columns:9.5em minmax(0,1fr);gap:6px;padding:4px 0}.run-detail>code{background:none!important;padding:0!important;color:var(--fg)}.run-detail-links{display:grid;gap:3px;min-width:0}.run-path{display:grid;grid-template-columns:3.5em minmax(0,1fr);gap:6px;align-items:start;color:var(--fg);text-decoration:none;min-width:0}.run-path b{font-size:10px;text-transform:uppercase;color:var(--mut)}.run-path code{background:none!important;padding:0!important;white-space:normal;overflow-wrap:anywhere;word-break:break-word}.run-detail .missing{color:var(--mut)}
.related-summary{display:flex;gap:6px;flex-wrap:wrap;margin:0 0 10px}.related-summary span{border:1px solid var(--line);border-radius:999px;padding:1px 7px;color:var(--mut);font-size:11.5px}.related-summary .all{color:var(--acc);border-color:var(--acc);font-weight:650}.related-evidence-group{margin:14px 0 18px}.related-group-head{display:flex;align-items:baseline;gap:7px;flex-wrap:wrap;margin:0 0 6px;padding:0 2px}.related-group-head .evid{background:var(--card)}.related-group-title{font-weight:650}.related-group-count{color:var(--mut);font-size:11.5px}
.related-run-card{border:1px solid var(--line);border-radius:9px;margin:8px 0;background:var(--bg);overflow:hidden}.related-run-head{display:flex;align-items:baseline;gap:7px;flex-wrap:wrap;padding:9px 10px 7px}.related-run-layer{font:650 9.5px -apple-system,sans-serif;text-transform:uppercase;letter-spacing:.04em;color:var(--acc);border:1px solid var(--acc);border-radius:999px;padding:0 6px}.related-run-head code{font-size:12.5px!important;background:none!important;padding:0!important}.related-run-head .run-availability{margin-left:auto}.related-run-action{font:650 10px -apple-system,sans-serif;text-transform:uppercase;letter-spacing:.04em;color:var(--warn)}.related-run-head .run-availability b,.related-run-action b{font:600 8px -apple-system,sans-serif;letter-spacing:.04em;color:var(--mut);margin-right:4px}
.related-run-body{border-top:1px solid var(--line);padding:6px 10px}.related-run-body .run-fact{padding:4px 0}.related-evidence-list{display:flex;gap:5px;flex-wrap:wrap}.related-evidence{appearance:none;border:1px solid var(--line);background:var(--card);color:var(--acc);border-radius:5px;padding:1px 6px;font:650 10.5px ui-monospace,Menlo,monospace;cursor:pointer}.related-evidence:hover,.related-evidence:focus-visible{border-color:var(--acc);outline:none}.related-run-card details{border-top:1px solid var(--line);padding:5px 10px 7px;color:var(--mut);font-size:11.5px}.related-run-card summary{cursor:pointer}.related-run-card .run-popover-path:first-child{border-top:0}
@media(max-width:560px){#items,#runs{padding:10px 10px 18px}.runmap-head{grid-template-columns:auto minmax(0,1fr) auto}.runmap-addr{display:none}.runmap-line{grid-template-columns:1fr}.runmap-label{padding:0}.lineage-list{gap:4px}.run-detail{grid-template-columns:1fr;gap:1px}.run-path{grid-template-columns:3.2em minmax(0,1fr)}.related-run-head .run-availability{width:100%;margin-left:0}}
.ghost{color:var(--mut);padding:24px 0;font-size:13.5px}
#seg{display:none;border:0;width:100%;height:calc(100vh - 92px)}
.evidence-list{padding:10px 16px 22px;max-width:980px;margin:0 auto}
.evidence-overview{display:flex;gap:6px;flex-wrap:wrap;margin:0 0 11px}
.evidence-overview span,.evidence-overview a{border:1px solid var(--line);border-radius:999px;padding:2px 8px;
 color:var(--mut);font-size:11.5px}.evidence-overview a{display:inline-block;text-decoration:none}
.evidence-overview a:hover,.evidence-overview a:focus-visible{border-color:var(--acc);color:var(--acc);outline:none}
.evidence-overview a.active{border-color:var(--acc);color:var(--acc);font-weight:650}
.evidence-overview .total{color:var(--fg);font-weight:650}
.source-details{margin:0 0 14px;color:var(--mut);font-size:11.5px}
.source-details summary{display:inline-block;cursor:pointer}.source-details summary:hover{color:var(--fg)}
.source-details .source-body{margin-top:5px;padding:6px 8px;border:1px solid var(--line);
 border-radius:6px;overflow-wrap:anywhere}.source-details code{font-size:11px;color:var(--fg)}
.evidence-type-section{margin:18px 0 22px}.evidence-type-head{display:flex;align-items:baseline;
 gap:7px;margin:0 0 7px;padding:0 2px}.evidence-type-title{font-size:15px;margin:0}
.evidence-type-count{color:var(--mut);font-size:11.5px}.evidence-type-hint{margin-left:auto;
 color:var(--mut);font-size:11.5px}.evidence-cards{display:grid;gap:7px}
.evidence-card{border:1px solid var(--line);border-radius:9px;background:var(--bg);overflow:hidden;
 scroll-margin-top:14px}.evidence-card:hover{border-color:#b8c4d2}
.evidence-migration-blocker{margin:0 0 12px;padding:8px 10px;border:1px solid var(--warn);
 border-left:3px solid var(--warn);border-radius:7px;color:var(--warn);font-size:12px}
.evidence-migration-blocker code{color:inherit}
.evidence-card>summary{list-style:none;cursor:pointer}.evidence-card>summary::-webkit-details-marker{display:none}
.evidence-summary{display:flex;align-items:flex-start;gap:7px;padding:9px 10px;min-width:0;
 box-sizing:border-box}.evidence-summary-main{flex:1;min-width:0;display:grid;gap:3px}
.evidence-summary-line{display:flex;align-items:baseline;gap:7px;min-width:0;flex-wrap:wrap}
.evidence-chevron{flex:none;color:var(--mut);font-size:18px;
 line-height:1;transition:transform .12s ease}.evidence-card[open] .evidence-chevron{transform:rotate(90deg)}
.evidence-card[open]{border-color:var(--acc)}.evidence-label{font-weight:650;overflow-wrap:anywhere}
.evidence-kind{color:var(--acc);font:650 9.5px -apple-system,sans-serif;text-transform:uppercase;
 letter-spacing:.035em;border:1px solid var(--acc);border-radius:999px;padding:0 6px;white-space:nowrap}
.evidence-title{color:var(--mut);font-size:12.5px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.evidence-bullet{display:block;color:var(--mut);font-size:11px;white-space:nowrap;padding-left:2px}
.evidence-summary code{background:none;padding:0}
.evidence-status{flex:none;margin-left:auto;align-self:center;font-weight:650;font-size:13px}
.evidence-status.complete,.evidence-status.ready,
.evidence-status.folded,.evidence-status.accepted{color:var(--ok)}
.evidence-status.specified,.evidence-status.planned{color:var(--warn)}
.evidence-summary{display:grid;grid-template-columns:1.1em auto minmax(0,1fr) auto auto;align-items:center;gap:7px;padding:9px 10px;min-width:0;
 box-sizing:border-box}.evidence-summary-main{grid-column:3;min-width:0;display:grid;gap:0}
.evidence-summary-line{display:flex;align-items:baseline;gap:7px;min-width:0;overflow:hidden}
.evidence-chevron{grid-column:1;grid-row:1;color:var(--mut);font-size:18px;
 line-height:1;transition:transform .12s ease}.evidence-card[open] .evidence-chevron{transform:rotate(90deg)}
.evidence-card[open]{border-color:var(--acc)}.evidence-label{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-weight:650}
.evidence-kind{grid-column:2;grid-row:1;color:var(--acc);font:650 9.5px -apple-system,sans-serif;text-transform:uppercase;
 letter-spacing:.035em;border:1px solid var(--acc);border-radius:999px;padding:0 6px;white-space:nowrap}
.evidence-title{color:var(--mut);font-size:12.5px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.evidence-bullet{grid-column:4;grid-row:1;justify-self:end;display:block;color:var(--mut);font-size:11px;white-space:nowrap;padding-left:2px}
.evidence-summary code{background:none;padding:0}
.evidence-status{grid-column:5;grid-row:1;flex:none;align-self:center;font-weight:650;font-size:13px;white-space:nowrap}
.evidence-status.complete,.evidence-status.ready,
.evidence-status.folded,.evidence-status.accepted{color:var(--ok)}
.evidence-status.specified,.evidence-status.planned,.evidence-status.needs-review,.evidence-status.partial{color:var(--warn)}
.evidence-detail{border-top:1px solid var(--line);padding:0 11px 10px}.evidence-detail-row{display:grid;
 grid-template-columns:8.5em minmax(0,1fr);gap:8px;padding:3px 0;font-size:12.5px;line-height:1.45}
.evidence-prompt-actions{display:flex;justify-content:flex-end;margin:7px 0}
.evidence-detail-label{color:var(--mut);font:650 10px -apple-system,sans-serif;text-transform:uppercase;
 letter-spacing:.035em;padding-top:2px}.evidence-detail-value{min-width:0;overflow-wrap:anywhere}
.evidence-detail-value code{font-size:11.5px;background:none;padding:0;overflow-wrap:anywhere;word-break:break-word}
.evidence-preview{margin:0 0 8px;padding:9px 0 0;border:0;border-radius:0;background:transparent}
.evidence-preview-label{margin:0 0 5px;color:var(--mut);font:650 9.5px -apple-system,sans-serif;
 text-transform:uppercase;letter-spacing:.05em}.evidence-preview-subhead{margin:8px 0 4px;color:var(--mut);font:650 9.5px -apple-system,sans-serif;
 text-transform:uppercase;letter-spacing:.05em}.evidence-preview-copy{margin:4px 0 0;font-size:12.5px;line-height:1.48}
.evidence-preview-copy p{margin:4px 0}.evidence-preview-media{min-width:0}.evidence-preview-image{display:block;width:100%;max-height:250px;object-fit:contain;
 border:1px solid var(--line);border-radius:5px;background:var(--bg)}
.evidence-preview-pdf{display:block;width:100%;height:min(34vh,260px);min-height:180px;border:1px solid var(--line);
 border-radius:5px;background:var(--bg)}.evidence-preview-link{font-size:11.5px;color:var(--acc)}
.evidence-preview-link{display:inline-block;margin-top:5px;text-decoration:none}.evidence-preview-link:hover{text-decoration:underline}
.evidence-preview-empty{color:var(--mut);font-size:12.5px}.evidence-preview-hero{font-size:24px;line-height:1.15;
 font-weight:700;color:var(--fg);letter-spacing:-.02em}.evidence-preview-hero small{font-size:12px;font-weight:500;
 color:var(--mut);letter-spacing:0}.evidence-preview-facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(8em,1fr));
 gap:0 18px;margin-top:7px}.evidence-preview-fact{padding:6px 0;border:0;border-bottom:1px solid var(--line);border-radius:0;background:transparent}
.evidence-preview-fact b{display:block;color:var(--mut);font:650 9.5px -apple-system,sans-serif;text-transform:uppercase;
 letter-spacing:.03em}.evidence-preview-fact span{display:block;margin-top:1px;font-size:12px;overflow-wrap:anywhere}
.evidence-preview-table{width:100%;border-collapse:collapse;font-size:11.5px;background:transparent}
.evidence-preview-table th,.evidence-preview-table td{padding:5px 6px 5px 0;border:0;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
.evidence-preview-table th{color:var(--mut);font-size:10px;text-transform:uppercase;letter-spacing:.025em;font-weight:650}
.evidence-preview-table tbody tr:last-child td{border-bottom:0}.evidence-preview-table-wrap{overflow:auto;max-height:360px;border:0;border-radius:0}
.evidence-preview-source{padding:6px 0;border-top:1px solid var(--line)}.evidence-preview-source:first-child{border-top:0;padding-top:0}
.evidence-preview-source-head{display:flex;gap:6px;align-items:baseline;flex-wrap:wrap;font-size:12px}
.evidence-preview-source-head b{font-weight:650}.evidence-preview-source-head code{color:var(--mut);font-size:10.5px;background:none;padding:0}
.evidence-preview-source p{margin:3px 0 0;font-size:12.5px;line-height:1.45}
.evidence-card.run-focus{outline:2px solid var(--acc);outline-offset:3px}
.evidence-actions{display:flex;gap:12px;flex-wrap:wrap;margin:2px 0 7px}
.evidence-action{display:inline-block;border:0;border-bottom:1px solid var(--line);border-radius:0;padding:2px 0;
 color:var(--mut);font-size:11px;text-decoration:none;background:transparent}
.evidence-action:hover,.evidence-action:focus-visible{border-color:var(--acc);color:var(--acc);outline:none}
.evidence-trace{margin-top:7px;border-top:1px solid var(--line);padding-top:5px;color:var(--mut);font-size:12px}
.evidence-trace>summary{cursor:pointer;list-style:none;font-size:11px}.evidence-trace>summary::-webkit-details-marker{display:none}
.evidence-trace>summary:before{content:'+';display:inline-block;width:1em;color:var(--acc);font-weight:700}
.evidence-trace[open]>summary:before{content:'-'} .evidence-trace-body{margin-top:4px}
.evidence-label-list{display:grid;gap:0}.evidence-label-binding{border:0;border-bottom:1px solid var(--line);
 border-radius:0;padding:5px 0;background:transparent}.evidence-label-binding>summary{cursor:pointer;
 list-style:none;display:flex;gap:7px;align-items:baseline;flex-wrap:wrap}.evidence-label-binding>summary::-webkit-details-marker{display:none}
.evidence-label-visible{font-weight:650;color:var(--fg)}.evidence-label-token{color:var(--acc);font:11px ui-monospace,Menlo,monospace;
 overflow-wrap:anywhere}.evidence-label-state{color:var(--mut);font-size:10.5px;text-transform:uppercase;letter-spacing:.03em}
.evidence-label-meta{margin-top:4px;color:var(--mut);font-size:11.5px;line-height:1.45}.evidence-label-meta code{color:var(--fg)}
.evidence-label-summary{display:flex;align-items:center;gap:5px;flex-wrap:wrap;margin:0 0 8px;padding:5px 0;border:0;border-bottom:1px solid var(--line);border-radius:0;background:transparent}.evidence-label-summary-title{color:var(--mut);font:650 10px -apple-system,sans-serif;text-transform:uppercase;letter-spacing:.04em}.evidence-label-chip{display:inline-flex;align-items:baseline;gap:4px;padding:2px 0;border:0;border-radius:0;background:transparent;font-size:11.5px;max-width:100%;overflow:hidden}.evidence-label-chip b{color:var(--acc);font-size:9.5px;letter-spacing:.03em}.evidence-label-chip span{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
@media(max-width:620px){.evidence-list{padding:6px 10px 16px}.evidence-type-hint{display:none}
 .evidence-summary{grid-template-columns:1.1em auto auto 1fr;gap:6px;padding:8px 9px}
 .evidence-summary .evidence-title{grid-column:2 / -1;white-space:normal;overflow:visible}
 .evidence-summary .evidence-bullet{grid-column:2 / 4}.evidence-summary .evidence-status{justify-self:end}
 .evidence-summary{grid-template-columns:1.1em auto minmax(0,1fr) auto;gap:6px;padding:8px 9px}
 .evidence-summary-main{grid-column:3;grid-row:1}
 .evidence-bullet{grid-column:3;grid-row:2;justify-self:start}.evidence-status{grid-column:4;grid-row:1 / span 2;justify-self:end}
 .evidence-detail-row{grid-template-columns:1fr;gap:1px}.evidence-detail-label{padding-top:2px}}
"""
