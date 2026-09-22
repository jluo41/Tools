"""Outline's minimal, Result-first Evidence Space.

The live surface is grouped by Evidence type and reads only
``results/*/result.yaml``. Each item is a collapsed, read-only summary whose
details distinguish the Evidence Label, Evidence Item, Evidence Run, and
Supporting Runs. Retired Outline Evidence files are never an input or
fallback; their presence is reported as a migration blocker. This module
presents only and never executes a Run.
"""
from __future__ import annotations

import base64
import csv
import html
import io
import json
import mimetypes
import pathlib
import re
import sys
from urllib.parse import quote

from src.common import evidence_run_dirs
from src.evidence_labels import parse_result_labels
from src.item_table import (readable_global_run, readable_paper_route,
                            readable_task, wall_label)

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


def _md_lite(text: str, heading_prefix: str = "") -> str:
    """Enough markdown for the generated evidence snapshot: headings,
    bullets, fences, bold, inline code. Never trusted with raw HTML."""
    out, in_pre, in_ul = [], False, False
    for raw in text.split("\n"):
        line = html.escape(raw, quote=False)
        if raw.strip().startswith("```"):
            if in_ul: out.append("</ul>"); in_ul = False
            out.append("<pre>" if not in_pre else "</pre>")
            in_pre = not in_pre
            continue
        if in_pre:
            out.append(line)
            continue
        line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
        line = re.sub(r"`([^`]+)`", r"<code>\1</code>", line)

        def link(match):
            label, href = match.group(1), html.unescape(match.group(2))
            # The binding map writes only repo-relative Run/Result links;
            # permit ordinary web links too, but never let a markdown field
            # inject a script/data URL into the live Board surface.
            if not (href.startswith(("../", "./", "/", "https://", "http://"))):
                return label
            return ('<a href="%s" target="_blank" rel="noopener">%s</a>' %
                    (html.escape(href, quote=True), label))

        line = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, line)
        s = raw.lstrip()
        heading_attr = ""
        if heading_prefix and s.startswith(("## ", "### ")):
            heading = s.lstrip("# ").split(" ·", 1)[0].strip()
            safe = re.sub(r"[^A-Za-z0-9_-]+", "-", heading).strip("-")
            if safe:
                heading_attr = ' id="%s"' % html.escape(
                    heading_prefix + safe, quote=True
                )
        if s.startswith("### "):
            if in_ul: out.append("</ul>"); in_ul = False
            out.append("<h3%s>%s</h3>" % (heading_attr, line.lstrip()[4:]))
        elif s.startswith("## "):
            if in_ul: out.append("</ul>"); in_ul = False
            out.append("<h2%s>%s</h2>" % (heading_attr, line.lstrip()[3:]))
        elif s.startswith("- "):
            if not in_ul: out.append("<ul>"); in_ul = True
            out.append("<li>%s</li>" % line.lstrip()[2:])
        elif not s:
            if in_ul: out.append("</ul>"); in_ul = False
        else:
            out.append("<p>%s</p>" % line)
    if in_ul: out.append("</ul>")
    if in_pre: out.append("</pre>")
    return "\n".join(out)


_ITEM_HEADING = re.compile(r"^###\s+([^·]+?)\s*·\s*(.*)$")
_FIELD = re.compile(r"^-\s+\*\*([^*]+?)\*\*\s*:\s*(.*)$")


def _inline_lite(text: str) -> str:
    """Safe inline rendering for the compact Evidence Item cards."""
    line = html.escape(text.strip(), quote=False)
    line = re.sub(r"`([^`]+)`", r"<code>\1</code>", line)
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)


def _evidence_snapshot(text: str) -> tuple[str, list[dict[str, object]]]:
    """Read the generated snapshot without leaking its file mechanics into UI.

    The snapshot remains the durable generated audit.  This reader keeps its
    item headings and labelled rows, while omitting its file title, regeneration
    command, and sentinel lines; they explain the file, not the Evidence view.
    """
    plan, records, current = "", [], None
    for raw in text.splitlines():
        line, stripped = raw.rstrip(), raw.strip()
        if not stripped or line.startswith("# ---") or stripped.startswith((
                "# ", "page:", "kind:", "EVIDENCE STATUS", "regenerate:", "GENERATED")):
            continue
        if stripped.startswith("plan:"):
            plan = stripped[len("plan:"):].strip()
            continue
        match = _ITEM_HEADING.match(line)
        if match:
            rest = match.group(2).split(" · ", 1)
            current = {"id": match.group(1).strip(), "address": rest[0].strip(),
                       "title": rest[1].strip() if len(rest) > 1 else rest[0].strip(),
                       "fields": {}}
            records.append(current)
            continue
        match = _FIELD.match(stripped)
        if match and current is not None:
            current["fields"][match.group(1).strip().lower()] = match.group(2).strip()
    # A stale snapshot can repeat an item at several Bullet targets. Keep one
    # addressable card per immutable identity, but expose every conflicting
    # source record instead of silently choosing a ready contract.
    unique = {}
    for record in records:
        item_id = str(record["id"])
        if item_id not in unique:
            unique[item_id] = record
        else:
            unique[item_id].setdefault("duplicate_records", []).append(record)
    return plan, list(unique.values())


def _plan_chips(plan: str) -> str:
    """Keep only the current, reader-relevant plan facts in the top summary."""
    if not plan:
        return ""
    chips = []
    version = re.search(r"\bv(\d+)\b", plan)
    cycle = re.search(r"\bcycle:\s*([A-Za-z]+)", plan)
    items = re.search(r"\bitems\s+(\d+)", plan)
    decided = re.search(r"\bdecided\s+(\d+/\d+)", plan)
    approved = re.search(r"\bapproved:\s*([^·]+)", plan)
    if version:
        chips.append("<span>plan v%s</span>" % version.group(1))
    if cycle:
        chips.append("<span class=cycle>%s</span>" % html.escape(cycle.group(1)))
    if items:
        chips.append("<span>%s items</span>" % items.group(1))
    if decided:
        chips.append("<span>%s decided</span>" % decided.group(1))
    if approved and "✅" in approved.group(1):
        chips.append("<span class=approved>approved</span>")
    for kind, count in re.findall(r"\b(VALUE|CITE|DISPLAY)\s+(\d+)", plan):
        chips.append("<span>%s %s</span>" % (html.escape(kind), count))
    return '<div class=evsummary>%s</div>' % "".join(chips) if chips else ""


def _run_chips(value: str, evidence_id: str, context: dict[str, str]) -> str:
    """Show compact family, action, and dotted address without inventing rNN."""
    chips = []
    for raw in value.split(";"):
        parts = [part.strip() for part in raw.split(" · ") if part.strip()]
        if not parts:
            continue
        address = parts[-1]
        readable = readable_global_run(address) or readable_task(address) or address
        family, action = (parts[0] if len(parts) > 2 else ""), (parts[1] if len(parts) > 2 else "")
        key = family.lower()
        marker = "D" if key.startswith("discovery") else "X" if key.startswith("execution") else ""
        short_action = "new" if action.startswith("new-") else action.replace("-", "")
        survey_action = short_action or "unresolved"
        availability = "Planned" if survey_action == "new" else "Paths unresolved"
        next_action = "Rerun" if survey_action == "rerun" else "Allocate and run"
        state_class = "warn" if survey_action == "rerun" else "planned"
        chip_action = "rerun" if "rerun" in next_action.lower() else "plan"
        run = {"address": readable, "run": "", "result": "", "runtime": "",
               "availability": availability, "next_action": next_action,
               "chip_action": chip_action, "class": state_class}
        run = _with_evidence_context(run, context, local=False)
        chip = _lineage_chip(run, "run-detail-%s-fallback-%d" % (
            evidence_id, len(chips) + 1
        ))
        chips.append('<span class=runchip><b class="runfam %s">%s</b>%s</span>' % (
            html.escape(key, quote=True), marker, chip))
    return '<div class=runs>%s</div>' % "".join(chips) if chips else "—"


def _local_run_chip(value: str, evidence_id: str, context: dict[str, str]) -> str:
    """Show a Paper-Board-local Run as ``P jNN.tNN.rNN action``."""
    left, _arrow, _result = value.partition("→")
    parts = [part.strip() for part in left.split("·")]
    if len(parts) < 4 or [part.lower() for part in parts[:2]] != ["page", "evidence item"]:
        return _inline_lite(value)
    action, address = parts[2], parts[3]
    readable = readable_paper_route(address) or address
    run = {"address": "P " + readable, "run": "", "result": "", "runtime": "",
           "availability": "Planned", "next_action": "Allocate and run",
           "chip_action": "plan", "class": "planned"}
    run = _with_evidence_context(run, context, local=True)
    return _lineage_chip(
        run, "run-detail-%s-local-fallback" % evidence_id, local=True
    )


def _item_card(record: dict[str, object], binding: dict[str, object] | None = None) -> str:
    """Render one Evidence Item with every Run item grouped inside it."""
    fields = record["fields"]
    duplicates = record.get("duplicate_records", [])
    status = "conflicting records" if duplicates else str(fields.get("status", "open"))
    status_class = "ready" if any(word in status.lower() for word in ("ready", "accepted", "landed")) else "specified"
    type_ = str(fields.get("type", ""))
    evidence_id = str(record["id"])
    compact_id = wall_label(
        evidence_id, type_, str(record["title"]), str(fields.get("label", ""))
    )
    run_context = {
        "title": str(record["title"]),
        "type": type_,
        "need": str(fields.get("need", "")),
        "expected": str(fields.get("expected", "")),
        "acceptance": str(fields.get("acceptance", "")),
        "local_input": str(fields.get("local input", "")),
    }
    rows = []
    if duplicates:
        conflicting = [{key: value for key, value in record.items()
                        if key != "duplicate_records"}, *duplicates]
        rows.append(
            '<div class="evrow conflict" role="alert"><b>Duplicate identity</b>'
            '<span>This Evidence ID has %d source records. Resolve its target '
            'and contract in SHAPE before treating it as ready.'
            '<details><summary>Conflicting source records</summary><pre>%s</pre>'
            '</details></span></div>' % (
                len(conflicting), html.escape(json.dumps(conflicting, ensure_ascii=False, indent=2))
            )
        )
    for label, key in (("Needed", "expected"), ("Ready when", "acceptance")):
        value = str(fields.get(key, ""))
        if value:
            rows.append('<div class=evrow><b>%s</b><span>%s</span></div>' %
                        (label, _inline_lite(value)))

    run_details = []
    if binding is not None:
        supporting_runs = [
            _with_evidence_context(_run_binding(str(raw)), run_context, local=False)
            for raw in binding.get("supporting", [])
            if str(raw).strip() not in ("", "—", "-", "[]")
        ]
        supporting_html = "".join(
            _lineage_chip(run, "run-detail-%s-support-%d" % (evidence_id, index))
            for index, run in enumerate(supporting_runs, 1)
        ) or "—"
        run_details.extend(_run_detail(run) for run in supporting_runs)
        rows.append('<div class=evrow><b>Supporting runs</b><span class=lineage-list>%s</span></div>' %
                    supporting_html)

        local_raw = str(binding.get("local_run", ""))
        local_has_address = bool(re.match(r"^P\s+j\d+\.t\d+\.r\d+\b", local_raw))
        local_unallocated = (
            not local_has_address and (
                not local_raw
                or "not declared" in local_raw.lower()
                or "run not allocated" in local_raw.lower()
                or "ticket not allocated" in local_raw.lower()
                or local_raw.strip().lower() in (
                    "not allocated", "not surveyed yet", "not declared", "—", "-"
                )
            )
        )
        if local_unallocated:
            local_html = "not allocated"
        else:
            local = _with_evidence_context(
                _run_binding(local_raw), run_context, local=True
            )
            local_html = _lineage_chip(
                local, "run-detail-%s-local" % evidence_id, local=True
            )
            run_details.append(_run_detail(local))
        rows.append('<div class=evrow><b>Local run</b><span>%s</span></div>' % local_html)

        local_result = str(binding.get("local_result", ""))
        if not local_result or "not allocated" in local_result.lower():
            local_result = str(fields.get("has", "local Result not ready"))
        rows.append('<div class=evrow><b>Result</b><span>%s</span></div>' %
                    _inline_lite(local_result))
    else:
        supporting = str(fields.get("supporting runs", ""))
        if supporting:
            rows.append('<div class=evrow><b>Supporting runs</b><span>%s</span></div>' %
                        _run_chips(supporting, evidence_id, run_context))
        local_run = str(fields.get("local run", ""))
        if local_run:
            local_label = "not allocated" if local_run.startswith(("—", "-")) else local_run
            rows.append('<div class=evrow><b>Local run</b><span>%s</span></div>' %
                        _local_run_chip(local_label, evidence_id, run_context))
        has = str(fields.get("has", ""))
        if has:
            rows.append('<div class=evrow><b>Result</b><span>%s</span></div>' %
                        _inline_lite(has))

    paths_html = "".join(detail for detail in run_details if detail)
    paths = ('<details><summary>Run &amp; Result paths</summary>%s</details>' % paths_html
             if paths_html else "")
    details = []
    for label, key in (("Local input", "local input"),
                       ("Verified", "verified"), ("Decision", "decide")):
        value = str(fields.get(key, ""))
        if value:
            details.append('<div class=evdetail><b>%s</b><span>%s</span></div>' %
                           (label, _inline_lite(value)))
    detail_html = ('<details><summary>survey details</summary>%s</details>' % "".join(details)) if details else ""
    pills = '<span class="evpill %s">%s</span>' % (status_class, _inline_lite(status))
    if type_:
        pills += '<span class="evpill type">%s</span>' % _inline_lite(type_)
    return ('<article class=evcard id="run-%s" data-evidence-id="%s"><div class=evhead>'
            '<code class=evid title="%s">%s</code>'
            '<span class=evaddr>%s</span><span class=evtitle>%s</span><span class=evpills>%s</span>'
            '</div><div class=evrows>%s</div>%s%s</article>') % (
                html.escape(evidence_id, quote=True), html.escape(evidence_id, quote=True),
                html.escape(evidence_id, quote=True), html.escape(compact_id),
                _inline_lite(str(record["address"])), _inline_lite(str(record["title"])),
                pills, "".join(rows), paths, detail_html)


def _evidence_cards(text: str, run_text: str = "") -> str:
    plan, records = _evidence_snapshot(text)
    if not records:
        return _md_lite(text)
    bindings = {
        str(record["id"]): record for record in _run_binding_snapshot(run_text)
    } if run_text else {}
    return _plan_chips(plan) + "".join(
        _item_card(record, bindings.get(str(record["id"]))) for record in records
    )


_RUN_BINDING_HEADING = re.compile(
    r"^##\s+([^·]+?)\s*·\s*([^·]+?)(?:\s*·\s*(.*))?$"
)
_MARKDOWN_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")


def _safe_run_href(href: str) -> str:
    href = html.unescape(href.strip())
    if href.startswith(("../", "./", "/", "https://", "http://")):
        return href
    return ""


def _run_binding_snapshot(text: str) -> list[dict[str, object]]:
    """Parse the generated pointer map into compact Evidence Item records."""
    records, current, supporting = [], None, False
    for raw in text.splitlines():
        match = _RUN_BINDING_HEADING.match(raw.strip())
        if match:
            current = {
                "id": match.group(1).strip(),
                "address": match.group(2).strip(),
                "title": (match.group(3) or "").strip(),
                "supporting": [],
                "local_run": "",
                "local_result": "",
            }
            records.append(current)
            supporting = False
            continue
        if current is None:
            continue
        stripped = raw.strip()
        if stripped == "- **Supporting Runs**:":
            supporting = True
        elif raw.startswith("  - ") and supporting:
            current["supporting"].append(stripped[2:].strip())
        elif stripped.startswith("- **Local Run**:"):
            current["local_run"] = stripped.split(":", 1)[1].strip()
            supporting = False
        elif stripped.startswith("- **Local Result**:"):
            current["local_result"] = stripped.split(":", 1)[1].strip()
            supporting = False
    return records


def _run_binding(raw: str) -> dict[str, object]:
    """Read one Run pointer; accept legacy Ticket/Receipt labels silently."""
    text = raw.strip()
    first_link = _MARKDOWN_LINK.match(text)
    first_code = re.match(r"`([^`]+)`", text)
    if first_link:
        address, run_href = first_link.group(1), _safe_run_href(first_link.group(2))
        tail = text[first_link.end():].strip().lstrip("·").strip()
    elif first_code:
        address, run_href = first_code.group(1), ""
        tail = text[first_code.end():].strip().lstrip("·").strip()
    else:
        address, _sep, tail = text.partition(" · ")
        run_href = ""
    links = {
        label.lower(): _safe_run_href(href)
        for label, href in _MARKDOWN_LINK.findall(tail)
    }
    parts = [
        _MARKDOWN_LINK.sub(lambda match: match.group(1), part).strip()
        for part in tail.split(" · ") if part.strip()
    ]
    run_path = links.get("run", "") or links.get("ticket", "") or run_href
    result_path = links.get("result", "")
    lowered = " · ".join(parts).lower()
    explicitly_unallocated = (
        "run not allocated" in lowered
        or "ticket not allocated" in lowered
        or "not allocated" in address.lower()
    )
    if run_path and result_path:
        availability = "Run + Result"
    elif run_path:
        availability = "Run exists · Result missing"
    elif explicitly_unallocated or any(
        token in lowered for token in ("newrun", "new-run", " · new ·")
    ):
        availability = "Planned"
    else:
        availability = "Paths unresolved"

    if "rerun" in lowered:
        next_action = "Rerun" if run_path else "Resolve path, then rerun"
    elif result_path:
        next_action = "Reuse Result"
    elif run_path:
        next_action = "Run"
    elif availability == "Planned":
        next_action = "Allocate and run"
    else:
        next_action = "Resolve path"

    if result_path:
        state_class = "ready"
    elif "rerun" in lowered or run_path or availability == "Paths unresolved":
        state_class = "warn"
    else:
        state_class = "planned"
    if "rerun" in next_action.lower():
        chip_action = "rerun"
    elif next_action == "Reuse Result":
        chip_action = "reuse"
    elif availability == "Planned":
        chip_action = "plan"
    elif next_action == "Run":
        chip_action = "run"
    else:
        chip_action = "resolve"
    return {
        "address": address.strip(),
        "href": run_path,
        "run": run_path,
        "result": result_path,
        "runtime": links.get("runtime", "") or links.get("receipt", ""),
        "availability": availability,
        "next_action": next_action,
        "chip_action": chip_action,
        "class": state_class,
        "title": " · ".join([address.strip()] + parts),
    }


def _human_run_name(path: str) -> str:
    """Turn a Ticket filename into a short reader-facing purpose phrase."""
    stem = pathlib.PurePosixPath(path).stem
    stem = re.sub(r"^r\d+[_-]?", "", stem, flags=re.IGNORECASE)
    stem = re.sub(r"[_-]+", " ", stem)
    stem = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", stem)
    return re.sub(r"\s+", " ", stem).strip()


def _survey_sentence(note: str, address: str) -> str:
    """Pick the authored SURVEY sentence about one Supporting Run, if any."""
    if not note:
        return ""
    compact = re.sub(r"[^A-Za-z0-9]", "", address).lower()
    for sentence in re.split(r"(?<=[.!?])\s+", note.strip()):
        if compact and compact in re.sub(r"[^A-Za-z0-9]", "", sentence).lower():
            return sentence.strip()
    return ""


def _with_evidence_context(
    run: dict[str, object], context: dict[str, str], *, local: bool
) -> dict[str, object]:
    """Attach a useful purpose/plan without creating another stored authority."""
    enriched = dict(run)
    title = context.get("title", "this Evidence Item")
    expected = context.get("expected", "").strip()
    payload = expected.split("·", 1)[-1].strip() if expected else "the required evidence"
    if run.get("run"):
        ticket_name = _human_run_name(str(run["run"]))
        description = "%s; supports “%s”." % (
            ticket_name or "Existing Supporting Run", title
        )
        description_label = "Purpose"
    elif local:
        description = "Produce the page-local %s Result for “%s”: %s." % (
            context.get("type", "evidence") or "evidence", title, payload
        )
        description_label = "Plan"
    else:
        description = "Design a Supporting Run for “%s” to provide %s." % (
            title, payload
        )
        description_label = "Plan"
    note = context.get("local_input", "").strip()
    enriched["description"] = description
    enriched["description_label"] = description_label
    enriched["survey_note"] = note if local else _survey_sentence(
        note, str(run.get("address", ""))
    )
    return enriched


def _run_popover(run: dict[str, object], popover_id: str) -> str:
    """Render one calm Run detail card with non-navigating path text."""
    facts = [
        '<div class="run-fact primary"><b>%s</b><span>%s</span></div>' % (
            html.escape(str(run.get("description_label", "Purpose"))),
            html.escape(str(run.get("description", "Surveyed Run for this Evidence Item."))),
        )
    ]
    if run.get("survey_note"):
        facts.append('<div class=run-fact><b>Survey note</b><span>%s</span></div>' %
                     html.escape(str(run["survey_note"])))
    facts.extend([
        '<div class=run-fact><b>Availability</b><span>%s</span></div>' %
        html.escape(str(run["availability"])),
        '<div class=run-fact><b>Next action</b><span>%s</span></div>' %
        html.escape(str(run["next_action"])),
    ])
    paths = []
    path_rows = [("Run", "run"), ("Result", "result")]
    if run.get("runtime"):
        path_rows.append(("Runtime", "runtime"))
    for label, key in path_rows:
        href = str(run[key])
        if href:
            # Raw scripts and receipts are commonly served as downloads. The
            # Run chip already opens this detail, so paths remain selectable
            # text rather than becoming a second navigation door.
            value = '<code class=repo-path>%s</code>' % html.escape(href)
        else:
            value = '<span class=missing>%s</span>' % (
                "not allocated" if str(run["class"]) == "planned" else "not available"
            )
        paths.append('<div class=run-popover-path><b>%s</b>%s</div>' % (label, value))
    return ('<div id="%s" popover class=run-popover><div class=run-popover-head>'
            '<div class=run-popover-title><code>%s</code><span class=run-availability>%s</span></div>'
            '<button type=button class=run-close popovertarget="%s" '
            'popovertargetaction=hide aria-label="Close Run detail">×</button></div>'
            '<div class=run-popover-body>%s%s</div></div>') % (
                html.escape(popover_id, quote=True), html.escape(str(run["address"])),
                html.escape(str(run["availability"])), html.escape(popover_id, quote=True),
                "".join(facts), "".join(paths))


def _lineage_chip(run: dict[str, object], popover_id: str, *, local: bool = False) -> str:
    """Open Run detail in place instead of sending a chip to a raw script."""
    return ('<button type=button class="lineage-chip %s" popovertarget="%s" '
            'data-run-address="%s" data-run-kind="%s" title="Inspect %s">'
            '<code>%s</code><small>%s</small>'
            '</button>%s' % (
                html.escape(str(run["class"]), quote=True),
                html.escape(popover_id, quote=True),
                html.escape(str(run["address"]), quote=True),
                "local" if local else "supporting",
                html.escape(str(run["address"]), quote=True),
                html.escape(str(run["address"])), html.escape(str(run["chip_action"])),
                _run_popover(run, popover_id)))


def _run_detail(run: dict[str, object]) -> str:
    if not run["run"] and not run["result"] and not run.get("runtime"):
        return ""
    links = []
    path_rows = [("Run", "run"), ("Result", "result")]
    if run.get("runtime"):
        path_rows.append(("Runtime", "runtime"))
    for label, key in path_rows:
        href = str(run[key])
        if href:
            links.append('<span class=run-path><b>%s</b><code>%s</code></span>' %
                         (label, html.escape(href)))
        elif label == "Result":
            links.append('<span class="run-path missing"><b>Result</b>'
                         '<span>not available</span></span>')
    return ('<div class=run-detail><code>%s</code><span class=run-detail-links>%s</span></div>' %
            (html.escape(str(run["address"])), "".join(links)))


def _run_binding_card(record: dict[str, object]) -> str:
    evidence_id = str(record["id"])
    identity = re.match(r"^(E\d+)(?:-([A-Z]+))?(?:-(.*))?$", evidence_id)
    short_id = identity.group(1) if identity else evidence_id
    type_ = identity.group(2) if identity and identity.group(2) else ""
    slug = identity.group(3) if identity and identity.group(3) else ""
    short_title = slug.replace("-", " ") if slug else str(record["title"])
    run_context = {
        "title": str(record["title"]) or short_title,
        "type": type_,
        "need": "",
        "expected": "",
        "acceptance": "",
        "local_input": "",
    }
    runs = [
        _with_evidence_context(_run_binding(str(raw)), run_context, local=False)
        for raw in record["supporting"]
        if str(raw).strip() not in ("", "—", "-", "[]")
    ]
    chips = "".join(
        _lineage_chip(run, "run-detail-%s-support-%d" % (evidence_id, index))
        for index, run in enumerate(runs, 1)
    ) or "—"
    details = "".join(_run_detail(run) for run in runs)

    local_run, local_result = str(record["local_run"]), str(record["local_result"])
    local_has_address = bool(re.match(r"^P\s+j\d+\.t\d+\.r\d+\b", local_run))
    local_unallocated = (
        not local_has_address and (
            not local_run
            or "not declared" in local_run.lower()
            or "run not allocated" in local_run.lower()
            or "ticket not allocated" in local_run.lower()
            or local_run.strip().lower() in (
                "not allocated", "not surveyed yet", "not declared", "—", "-"
            )
        )
    )
    if local_unallocated:
        local_html = "<span>not allocated</span>"
    elif local_run:
        local = _with_evidence_context(
            _run_binding(local_run), run_context, local=True
        )
        local_html = _lineage_chip(
            local, "run-detail-%s-local" % evidence_id, local=True
        )
        details += _run_detail(local)
        if not local_result or "not allocated" in local_result.lower():
            local_html += "<span>no result</span>"
        else:
            local_html += "<span>Result · %s</span>" % html.escape(local_result)
    else:
        local_html = "<span>—</span>"
    detail_html = ('<details><summary>Run &amp; Result paths</summary>%s</details>' % details) if details else ""
    type_html = '<span class=runmap-type>%s</span>' % html.escape(type_) if type_ else ""
    return ('<article class=runmap-card id="run-%s"><div class=runmap-head title="%s">'
            '<code class=runmap-eid>%s</code><code class=runmap-addr>%s</code>'
            '<span class=runmap-title>%s</span>%s</div>'
            '<div class=runmap-line><span class=runmap-label>Supporting</span>'
            '<div class=lineage-list>%s</div></div>'
            '<div class=runmap-local><b>Local</b>%s</div>%s</article>') % (
                html.escape(evidence_id, quote=True), html.escape(str(record["title"]), quote=True),
                html.escape(short_id), html.escape(str(record["address"])),
                html.escape(short_title), type_html, chips, local_html, detail_html)


def _run_binding_cards(text: str) -> str:
    records = _run_binding_snapshot(text)
    if not records:
        return _md_lite(text, heading_prefix="run-")
    return "".join(_run_binding_card(record) for record in records)


def _run_key(address: str, *, local: bool) -> str:
    """Return a stable identity key without conflating Paper and global Runs."""
    compact = re.sub(r"[^A-Za-z0-9]", "", address).lower()
    return ("local:" if local else "supporting:") + compact


def _record_context(record: dict[str, object]) -> dict[str, str]:
    fields = record.get("fields", {})
    return {
        "title": str(record.get("title", "")),
        "type": str(fields.get("type", "")),
        "need": str(fields.get("need", "")),
        "expected": str(fields.get("expected", "")),
        "acceptance": str(fields.get("acceptance", "")),
        "local_input": str(fields.get("local input", "")),
    }


def _support_family(fields: dict[str, object], address: str) -> str:
    wanted = re.sub(r"[^A-Za-z0-9]", "", address).lower()
    for raw in str(fields.get("supporting runs", "")).split(";"):
        parts = [part.strip() for part in raw.split(" · ") if part.strip()]
        if len(parts) >= 3 and re.sub(r"[^A-Za-z0-9]", "", parts[-1]).lower() == wanted:
            return parts[0]
    return "Supporting"


def _authored_support(raw: str, context: dict[str, str]) -> tuple[dict[str, object], str] | None:
    """Build an honest planned/unresolved pointer when the derived map is absent."""
    parts = [part.strip() for part in raw.split(" · ") if part.strip()]
    if len(parts) < 3:
        return None
    family, action, address = parts[0], parts[1].lower(), parts[-1]
    readable = readable_global_run(address) or readable_task(address) or address
    planned = action.startswith("new-")
    next_action = (
        "Rerun" if action == "rerun" else
        "Reuse Result" if action == "reuse" else
        "Run" if action == "registered" else
        "Allocate and run" if planned else "Resolve path"
    )
    run = {
        "address": readable, "run": "", "result": "", "runtime": "",
        "availability": "Planned" if planned else "Paths unresolved",
        "next_action": next_action,
        "chip_action": "plan" if planned else action,
        "class": "planned" if planned else "warn",
    }
    return _with_evidence_context(run, context, local=False), family


def _related_runs(evidence_text: str, run_text: str) -> list[dict[str, object]]:
    """Reverse the item-centric binding map into unique Run-centric records."""
    _plan, evidence_records = _evidence_snapshot(evidence_text)
    bindings = {
        str(record["id"]): record for record in _run_binding_snapshot(run_text)
    }
    related: dict[str, dict[str, object]] = {}

    def add(run: dict[str, object], record: dict[str, object], *, local: bool,
            family: str) -> None:
        key = _run_key(str(run.get("address", "")), local=local)
        if key.endswith(":"):
            return
        entry = related.setdefault(key, {
            **run, "local": local, "family": family, "evidence": [],
        })
        fields = record.get("fields", {})
        item_id = str(record["id"])
        compact = wall_label(
            item_id, str(fields.get("type", "")), str(record.get("title", "")),
            str(fields.get("label", "")),
        )
        if not any(ref["id"] == item_id for ref in entry["evidence"]):
            entry["evidence"].append({
                "id": item_id, "label": compact,
                "title": str(record.get("title", "")),
            })

    for record in evidence_records:
        item_id = str(record["id"])
        fields = record.get("fields", {})
        context = _record_context(record)
        binding = bindings.get(item_id)
        if binding:
            for raw in binding.get("supporting", []):
                if str(raw).strip() in ("", "—", "-", "[]"):
                    continue
                run = _with_evidence_context(_run_binding(str(raw)), context, local=False)
                add(run, record, local=False,
                    family=_support_family(fields, str(run["address"])))
            local_raw = str(binding.get("local_run", "")).strip()
            if local_raw and local_raw.lower() not in (
                "—", "-", "not allocated", "not surveyed yet", "not declared"
            ) and "not declared" not in local_raw.lower():
                local = _with_evidence_context(_run_binding(local_raw), context, local=True)
                add(local, record, local=True, family="Page")
        else:
            for raw in str(fields.get("supporting runs", "")).split(";"):
                authored = _authored_support(raw.strip(), context)
                if authored:
                    add(authored[0], record, local=False, family=authored[1])
            local_raw = str(fields.get("local run", "")).strip()
            match = re.search(r"(pj\d+t\d+r\d+)", local_raw, re.IGNORECASE)
            if match:
                readable = "P " + (readable_paper_route(match.group(1)) or match.group(1))
                local = _with_evidence_context({
                    "address": readable, "run": "", "result": "", "runtime": "",
                    "availability": "Planned", "next_action": "Allocate and run",
                    "chip_action": "plan", "class": "planned",
                }, context, local=True)
                add(local, record, local=True, family="Page")
    return sorted(
        related.values(),
        key=lambda run: (bool(run["local"]), str(run["address"]).lower()),
    )


def _related_run_card(run: dict[str, object], evidence_ref: dict[str, str]) -> str:
    refs = [evidence_ref]
    if run.get("run"):
        purpose = _human_run_name(str(run["run"])) or "Existing Run"
        purpose = "%s; supports “%s”." % (purpose, evidence_ref["title"])
        purpose_label = "Purpose"
    else:
        purpose = str(run.get("description", "Planned evidence Run."))
        purpose_label = "Plan"
    ref_html = "".join(
        '<button type=button class=related-evidence data-evidence-target="run-%s" '
        'title="%s">%s</button>' % (
            html.escape(str(ref["id"]), quote=True),
            html.escape(str(ref["title"]), quote=True),
            html.escape(str(ref["label"])),
        ) for ref in refs
    )
    path_rows = []
    for label, key in (("Run", "run"), ("Result", "result"), ("Runtime", "runtime")):
        path = str(run.get(key, ""))
        value = ('<code class=repo-path>%s</code>' % html.escape(path)) if path else (
            '<span class=missing>%s</span>' % (
                "not allocated" if run.get("availability") == "Planned" else "not available"
            )
        )
        path_rows.append('<div class=run-popover-path><b>%s</b>%s</div>' % (label, value))
    safe_id = re.sub(r"[^A-Za-z0-9_-]+", "-", "%s-%s" % (
        evidence_ref["id"], _run_key(str(run["address"]), local=bool(run["local"]))
    )).strip("-")
    layer = "Local · Page" if run["local"] else "Supporting · %s" % run["family"]
    return ('<article class=related-run-card id="related-run-%s" '
            'data-evidence-id="%s" data-run-address="%s" data-run-kind="%s">'
            '<div class=related-run-head><span class=related-run-layer>%s</span>'
            '<code>%s</code><span class=run-availability><b>Availability</b>%s</span>'
            '<span class=related-run-action><b>Next</b>%s</span></div>'
            '<div class=related-run-body>'
            '<div class="run-fact primary"><b>%s</b><span>%s</span></div>'
            '<div class=run-fact><b>Evidence Items</b><span class=related-evidence-list>%s</span></div>'
            '</div><details><summary>Run &amp; Result paths</summary>%s</details></article>') % (
                html.escape(safe_id, quote=True),
                html.escape(str(evidence_ref["id"]), quote=True),
                html.escape(str(run["address"]), quote=True),
                "local" if run["local"] else "supporting",
                html.escape(layer),
                html.escape(str(run["address"])), html.escape(str(run["availability"])),
                html.escape(str(run["next_action"])), purpose_label,
                html.escape(purpose), ref_html, "".join(path_rows),
            )


def _related_run_cards(evidence_text: str, run_text: str) -> tuple[str, int]:
    runs = _related_runs(evidence_text, run_text)
    if not runs:
        return ('<div class=ghost>No Supporting or Local Runs are mapped to these '
                'Evidence Items yet.</div>', 0)
    _plan, records = _evidence_snapshot(evidence_text)
    groups, mapping_count = [], 0
    for record in records:
        item_id = str(record["id"])
        fields = record.get("fields", {})
        compact = wall_label(
            item_id, str(fields.get("type", "")), str(record.get("title", "")),
            str(fields.get("label", "")),
        )
        evidence_ref = {
            "id": item_id, "label": compact,
            "title": str(record.get("title", "")),
        }
        item_runs = [
            run for run in runs
            if any(str(ref["id"]) == item_id for ref in run["evidence"])
        ]
        if not item_runs:
            continue
        mapping_count += len(item_runs)
        groups.append(
            '<section class=related-evidence-group><div class=related-group-head>'
            '<button type=button class="evid related-evidence" data-evidence-target="run-%s">%s</button>'
            '<span class=related-group-title>%s</span><span class=related-group-count>%d Run%s</span>'
            '</div>%s</section>' % (
                html.escape(item_id, quote=True), html.escape(compact),
                html.escape(str(record.get("title", ""))), len(item_runs),
                "" if len(item_runs) == 1 else "s",
                "".join(_related_run_card(run, evidence_ref) for run in item_runs),
            )
        )
    summary = ('<div class=related-summary><span class=all>%d Run mappings</span>'
               '<span>%d unique Runs</span><span>%d Evidences</span></div>') % (
                   mapping_count, len(runs), len(groups)
               )
    return summary + "".join(groups), mapping_count


def _legacy_render(page_src: pathlib.Path, path_q: str, file_q: str) -> str:
    stem = page_src.stem
    folded = page_src.parent.name == stem
    folder = page_src.parent if folded else None
    ev = (folder / "outline" / f"{stem}-evidence.md") if folder else \
         (page_src.parent / "outline" / f"{stem}-evidence.md")
    page_home = folder or page_src.parent
    runmap = next((d / f"{stem}-run-bindings.md"
                   for d in evidence_run_dirs(page_home)
                   if (d / f"{stem}-run-bindings.md").is_file()), None)
    run_text = runmap.read_text(encoding="utf-8") if runmap else ""
    evidence_text = ev.read_text(encoding="utf-8") if ev.exists() else ""
    if evidence_text:
        body = _evidence_cards(evidence_text, run_text)
    else:
        body = ("<div class=ghost>No evidence snapshot yet: "
                "<code>cli/evidence-status.py</code> (or an OUTLINE pass) "
                "writes <code>outline/%s-evidence.md</code>.</div>" % html.escape(stem))
    runs_body, related_run_count = _related_run_cards(evidence_text, run_text)
    _plan, evidence_records = _evidence_snapshot(evidence_text)
    counts = {kind: 0 for kind in ("CITE", "VALUE", "DISPLAY")}
    for record in evidence_records:
        kind = str(record.get("fields", {}).get("type", "")).upper()
        if kind in counts:
            counts[kind] += 1
    ctx = json.dumps({"path": path_q, "file": file_q, "stem": stem,
                      "folded": folded})
    return f"""<!doctype html><meta charset=utf-8>
<title>🧭 Outline · Evidence Space · {html.escape(stem)}</title>
<style>{_CSS}</style>
<header><h1>Evidence Space · {html.escape(stem)}</h1>
<p class=lead>what each bullet needs, what supports it, and what is ready</p></header>
<nav>
<button class=on data-seg=items>🧾 Evidences · {len(evidence_records)}</button>
<button data-seg=runs>⚙️ Runs · {related_run_count}</button>
<button data-seg=bibex>📚 Citations · {counts['CITE']}</button>
<button data-seg=value>🧮 Values · {counts['VALUE']}</button>
<button data-seg=display>🖼 Displays · {counts['DISPLAY']}</button>
</nav>
<div id=items>{body}</div>
<div id=runs style="display:none">{runs_body}</div>
<iframe id=seg></iframe>
<script>
(function () {{
  'use strict';
  var CTX = {ctx};
  function savedUrl(plugin, ext) {{
    var p = decodeURIComponent(CTX.path || '');
    var cut = p.lastIndexOf('/board/');
    var base = cut >= 0 ? p.slice(0, cut)
             : (/\\.md$/.test(p) ? p.slice(0, p.lastIndexOf('/')) : '');
    if (!base) return '';
    var m = (CTX.file || '').match(/^(.*)\\/([^\\/]+)\\/\\2\\.md$/);
    if (m) return base + '/' + m[1] + '/' + m[2] + '/outline/evidence/' + plugin + '/' + m[2] + (ext || '-view.html');
    return base + '/outline/evidence/' + plugin + '/' + CTX.stem + (ext || '-view.html');
  }}
  var LANES = {{
    bibex:   {{ext: '-bib.html',  route: 'bibex'}},
    display: {{ext: '-view.html', route: 'display'}},
    value:   {{live: '/_board/value?path=' + encodeURIComponent(CTX.path)
                    + '&file=' + encodeURIComponent(CTX.file)}}
  }};
  var frame = document.getElementById('seg'),
      staticSegs = {{items: document.getElementById('items'),
                    runs: document.getElementById('runs')}};
  function show(id, btn) {{
    var all = document.querySelectorAll('nav button');
    for (var i = 0; i < all.length; i++) all[i].className = '';
    btn.className = 'on';
    if (staticSegs[id]) {{
      frame.style.display = 'none';
      Object.keys(staticSegs).forEach(function (key) {{ staticSegs[key].style.display = key === id ? 'block' : 'none'; }});
      return;
    }}
    Object.keys(staticSegs).forEach(function (key) {{ staticSegs[key].style.display = 'none'; }});
    frame.style.display = 'block';
    var lane = LANES[id];
    if (lane.live) {{ frame.src = lane.live; return; }}
    var url = savedUrl(id, lane.ext);
    fetch(url, {{method: 'HEAD'}}).then(function (r) {{
      if (r.ok) {{ frame.src = url + '?embed'; return; }}
      /* not built yet: press the lane's own pen, then load what it names */
      fetch('/_board/' + lane.route, {{
        method: 'POST', headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{path: CTX.path, file: CTX.file}})
      }}).then(function (r2) {{ return r2.json(); }})
        .then(function (j) {{
          if (j.ok && j.url) frame.src = j.url + '?embed';
          else frame.srcdoc = '<p style="font:13px sans-serif;color:#888;padding:20px">⚠ ' +
                              ((j && j.err) || 'the ' + id + ' view failed') + '</p>';
        }});
    }});
  }}
  var btns = document.querySelectorAll('nav button');
  for (var i = 0; i < btns.length; i++) {{
    (function (b) {{
      b.addEventListener('click', function () {{ show(b.getAttribute('data-seg'), b); }});
    }})(btns[i]);
  }}
  var evidenceLinks = document.querySelectorAll('[data-evidence-target]');
  for (var j = 0; j < evidenceLinks.length; j++) {{
    evidenceLinks[j].addEventListener('click', function () {{
      var itemsButton = document.querySelector('nav button[data-seg="items"]');
      show('items', itemsButton);
      var target = document.getElementById(this.getAttribute('data-evidence-target'));
      if (!target) return;
      target.classList.add('run-focus');
      target.setAttribute('tabindex', '-1');
      target.focus({{preventScroll: true}});
      target.scrollIntoView({{block: 'start', behavior: 'smooth'}});
    }});
  }}
  /* Safari versions without the Popover API still need the Run inspector.
     Keep native popovers where available and use one small, explicit fallback
     for both a tap and an automatic deep-link open. */
  var hasPopover = typeof HTMLElement !== 'undefined'
                && typeof HTMLElement.prototype.showPopover === 'function';
  if (!hasPopover) document.documentElement.classList.add('no-popover');
  function openRunPanel(panel) {{
    if (!panel) return;
    if (hasPopover) {{
      try {{ panel.showPopover(); return; }} catch (e) {{
        hasPopover = false;
        document.documentElement.classList.add('no-popover');
      }}
    }}
    panel.setAttribute('data-fallback-open', '1');
  }}
  function closeRunPanel(panel) {{
    if (!panel) return;
    if (hasPopover && typeof panel.hidePopover === 'function') {{
      try {{ panel.hidePopover(); return; }} catch (e) {{}}
    }}
    panel.removeAttribute('data-fallback-open');
  }}
  var runButtons = document.querySelectorAll('.lineage-chip[popovertarget]');
  for (var rb = 0; rb < runButtons.length; rb++) {{
    runButtons[rb].addEventListener('click', function (event) {{
      event.preventDefault();
      var owner = this.closest('[data-evidence-id]');
      var matched = focusRelatedRun(
        this.getAttribute('data-run-address') || '',
        this.getAttribute('data-run-kind') === 'local',
        owner ? owner.getAttribute('data-evidence-id') || '' : ''
      );
      if (!matched)
        openRunPanel(document.getElementById(this.getAttribute('popovertarget')));
    }});
  }}
  var closeButtons = document.querySelectorAll('.run-close[popovertarget]');
  for (var cb = 0; cb < closeButtons.length; cb++) {{
    closeButtons[cb].addEventListener('click', function (event) {{
      event.preventDefault();
      event.stopPropagation();
      closeRunPanel(document.getElementById(this.getAttribute('popovertarget')));
    }});
  }}
  document.addEventListener('keydown', function (event) {{
    if (hasPopover || event.key !== 'Escape') return;
    var open = document.querySelector('.run-popover[data-fallback-open="1"]');
    if (open) closeRunPanel(open);
  }});
  var params = new URLSearchParams(location.search),
      requestedSeg = params.get('seg') || '',
      requestedFocus = params.get('focus') || '',
      requestedRun = params.get('run') || '';
  if (params.get('embed') === '1') document.documentElement.classList.add('embedded');
  /* Old Outline links remain valid after By bullet and Run links merge. */
  if (requestedSeg === 'runlinks' || requestedSeg === 'bybullet') requestedSeg = 'items';
  if (requestedSeg) {{
    var requestedButton = document.querySelector('nav button[data-seg="' +
                                                   requestedSeg + '"]');
    if (requestedButton) show(requestedSeg, requestedButton);
  }}
  function runKey(value, local) {{
    var text = (value || '').trim();
    var match;
    if (local) {{
      match = text.match(/^P?\\s*\\.?j(\\d+)\\.?t(\\d+)\\.?r(\\d+)$/i);
      if (match) return 'j' + match[1] + '.t' + match[2] + '.r' + match[3];
    }}
    match = text.match(/^b(\\d+)\\.?j(\\d+)\\.?t(\\d+)(?:\\.?r(\\d+))?$/i);
    if (match) return 'b' + match[1] + '.j' + match[2] + '.t' + match[3]
                      + (match[4] ? '.r' + match[4] : '');
    return text.toLowerCase();
  }}
  function focusRelatedRun(address, local, evidenceId) {{
    var runsButton = document.querySelector('nav button[data-seg="runs"]');
    if (runsButton) show('runs', runsButton);
    var cards = document.querySelectorAll('#runs .related-run-card[data-run-address]');
    var target = null;
    for (var i = 0; i < cards.length; i++) {{
      var cardLocal = cards[i].getAttribute('data-run-kind') === 'local';
      if (local !== null && cardLocal !== local) continue;
      if (evidenceId && cards[i].getAttribute('data-evidence-id') !== evidenceId) continue;
      if (runKey(cards[i].getAttribute('data-run-address') || '', cardLocal) !== runKey(address, cardLocal)) continue;
      target = cards[i];
      break;
    }}
    if (!target) return false;
    document.querySelectorAll('.run-focus').forEach(function (x) {{
      x.classList.remove('run-focus');}});
    target.classList.add('run-focus');
    target.setAttribute('tabindex', '-1');
    target.focus({{preventScroll: true}});
    target.scrollIntoView({{block: 'start', behavior: 'instant'}});
    return true;
  }}
  if (requestedFocus) {{
    setTimeout(function () {{
      if (requestedRun) {{
        var evidenceId = requestedFocus.replace(/^run-/, '');
        /* A local Task Run also has a b/j/t/r address. Resolve its layer
           from the mapped card, never from the spelling of its namespace. */
        if (focusRelatedRun(requestedRun, null, evidenceId)) return;
      }}
      var target = document.getElementById(requestedFocus);
      if (target) {{
        target.classList.add('run-focus');
        target.setAttribute('tabindex', '-1');
        target.focus({{preventScroll: true}});
        target.scrollIntoView({{block: 'start'}});
        if (requestedRun) {{
          var buttons = target.querySelectorAll('[data-run-address]');
          for (var i = 0; i < buttons.length; i++) {{
            var address = buttons[i].getAttribute('data-run-address') || '';
            var local = buttons[i].getAttribute('data-run-kind') === 'local';
            if (runKey(address, local) !== runKey(requestedRun, local)) continue;
            var panel = document.getElementById(buttons[i].getAttribute('popovertarget'));
            openRunPanel(panel);
            buttons[i].focus();
            break;
          }}
        }}
      }}
    }}, 0);
  }}
}})();
</script>"""


_RESULT_ITEM = re.compile(
    r"^E\d+-(?:VALUE|TABLE|CITE|DISPLAY)-[a-z0-9]+(?:-[a-z0-9]+)*$", re.I
)


def _top_field(text: str, name: str) -> str:
    match = re.search(rf"(?mi)^{re.escape(name)}:\s*([^#\n]+)", text)
    return match.group(1).strip().strip("'\"") if match else ""


def _result_document(text: str) -> dict[str, object]:
    """Parse a Result envelope without treating its payload as trusted HTML."""
    try:
        value = json.loads(text)
    except (TypeError, ValueError):
        try:
            import yaml
        except ImportError:
            # The Board supervisor may launch system Python while the
            # workspace's .venv owns the optional YAML dependency.
            yaml = None
            anchors = [pathlib.Path.cwd(), *pathlib.Path(__file__).resolve().parents]
            for anchor in anchors:
                venv_lib = anchor / ".venv" / "lib"
                for site in sorted(venv_lib.glob("python*/site-packages")):
                    if not site.is_dir():
                        continue
                    sys.path.insert(0, str(site))
                    try:
                        import yaml
                        break
                    except ImportError:
                        sys.path.pop(0)
                if yaml is not None:
                    break
            if yaml is None:
                return {}
        try:
            value = yaml.safe_load(text)
        except yaml.YAMLError:
            return {}
    return value if isinstance(value, dict) else {}


def _document_text(document: dict[str, object], key: str, text: str) -> str:
    value = document.get(key)
    if isinstance(value, (str, int, float, bool)):
        return str(value).strip()
    return _top_field(text, key)


def _supporting_run_ids(document: dict[str, object], text: str) -> list[str]:
    """Return only owner-native Supporting Run ids for the compact card."""
    values = document.get("supporting_results")
    found = []
    if isinstance(values, list):
        for value in values:
            if isinstance(value, dict) and value.get("run"):
                found.append(str(value["run"]).strip())
            elif isinstance(value, str) and value.strip():
                found.append(value.strip())
    if found:
        return found
    return [value.strip() for value in re.findall(
        r"(?m)^\s*-\s+run:\s*([^#\n]+)", text
    ) if value.strip()]


def _result_records(page_home: pathlib.Path) -> list[dict[str, object]]:
    """Read the current Evidence surface exclusively from Run Results."""
    records: dict[str, dict[str, object]] = {}
    order: list[str] = []

    result_root = page_home / "results"
    if result_root.is_dir() and not result_root.is_symlink():
        from src.evidence_selection import selected_for_home
        for manifest in selected_for_home(page_home):
            if manifest.is_symlink():
                continue
            try:
                manifest.resolve().relative_to(result_root.resolve())
                text = manifest.read_text(encoding="utf-8", errors="replace")
            except (OSError, ValueError):
                continue
            document = _result_document(text)
            item_id = _document_text(document, "item", text)
            if not _RESULT_ITEM.fullmatch(item_id):
                continue
            kind = (_document_text(document, "type", text)
                    or item_id.split("-", 2)[1].upper())
            status = _document_text(document, "status", text) or "ready"
            owner_run = _document_text(document, "run", text)
            page_run = _document_text(document, "page_run", text)
            run_id = page_run or owner_run or manifest.parent.name
            bullet = _document_text(document, "bullet", text)
            title = _document_text(document, "title", text)
            label = _document_text(document, "label", text)
            expected = _document_text(document, "expected", text)
            acceptance = _document_text(document, "acceptance", text)
            run_status = ""
            runtime_receipt = manifest.parent / "runtime.yaml"
            if runtime_receipt.is_file():
                try:
                    run_status = _top_field(runtime_receipt.read_text(
                        encoding="utf-8", errors="replace"), "status")
                except OSError:
                    run_status = ""
            labels = parse_result_labels(text)
            for result_label in labels:
                result_label.update({
                    "item": item_id,
                    "page_run": page_run,
                    "run": owner_run,
                    "result": manifest.relative_to(page_home).as_posix(),
                    "provenance": _document_text(document, "provenance", text),
                })
            supporting = _supporting_run_ids(document, text)
            record = records.get(item_id)
            if record is None:
                slug = item_id.split("-", 2)[-1].replace("-", " ")
                record = {"id": item_id, "address": bullet, "title": title or label or slug,
                          "fields": {}}
                records[item_id] = record
                order.append(item_id)
            elif bullet:
                record["address"] = bullet
            if title:
                record["title"] = title
            fields = dict(record.get("fields", {}))
            fields.update({
                "type": kind.upper(),
                "status": status.lower(),
                "run": run_id,
                "run status": run_status,
                "page_run": page_run,
                "owner run": owner_run if page_run and owner_run != page_run else "",
                "bullet": bullet,
                "label": label,
                "expected": expected,
                "acceptance": acceptance,
                "result": manifest.relative_to(page_home).as_posix(),
                "supporting runs": "; ".join(value.strip() for value in supporting),
                "labels": labels,
                "display_kind": (_document_text(document, "display_kind", text)
                                  or (str(document.get("payload", {}).get("display_kind", ""))
                                      if isinstance(document.get("payload"), dict) else "")),
            })
            record["fields"] = fields
            record["result_document"] = document
            record["result_file"] = manifest

    return [records[item_id] for item_id in order]


def _evidence_inventory(page_src: pathlib.Path,
                        records: list[dict[str, object]]) -> list[dict[str, object]]:
    """Combine selected Results with eligible, not-yet-resulted ledger items.

    The Evidence Space remains read-only. Ledger-only entries are explicitly
    marked as planned/specified and never receive a fabricated Run or Result.
    """
    from src.item_table import read_items
    try:
        ledger = read_items(page_src)
    except (OSError, ValueError):
        ledger = {}
    try:
        from live.runs import local_runs
        run_rows = local_runs(page_src)
    except (OSError, ValueError):
        run_rows = []

    runs_by_item: dict[str, list[dict[str, object]]] = {}
    for row in run_rows:
        for item_id in row.get("refs", []):
            runs_by_item.setdefault(str(item_id), []).append(row)

    result_ids = {str(record.get("id", "")).strip() for record in records}
    projected = list(records)
    for record in projected:
        item_id = str(record.get("id", "")).strip()
        item = ledger.get(item_id, {})
        fields = record.setdefault("fields", {})
        fields.update({
            "item expected": str(item.get("expected", "")).strip(),
            "item acceptance": str(item.get("acceptance", "")).strip(),
            "local input": str(item.get("local_input", "")).strip(),
            "ledger local run": str(item.get("local_run", "")).strip(),
            "ledger run action": str(item.get("action", "")).strip(),
            "ledger run route": str(item.get("address", "")).strip(),
            "ledger result binding": str(item.get("result", "")).strip(),
            "decision": str(item.get("decision", "")).strip(),
            "supporting runs valid": bool(item.get("supports_valid")),
            "local run registered": bool(item.get("runs_registered")),
            "supporting runs": (str(item.get("supporting_runs", "")).strip()
                                 or str(fields.get("supporting runs", "")).strip()),
        })
        matched = runs_by_item.get(item_id, [])
        fields["matching page runs"] = "; ".join(
            "%s · %s" % (row.get("run_id", "unknown"), row.get("status", "unknown"))
            for row in matched
        )
        current_run = str(fields.get("run", "")).strip()
        exact = next((row for row in matched
                      if str(row.get("run_id", "")).strip() == current_run), None)
        if exact:
            fields["run status"] = str(exact.get("status", "unknown"))

    for item_id, item in ledger.items():
        if item_id in result_ids or item.get("type") not in {"VALUE", "CITE", "DISPLAY"}:
            continue
        if item.get("decision") in {"defer", "drop"}:
            continue
        target = str(item.get("target", "")).strip()
        if not target:
            continue
        decision = str(item.get("decision", "")).strip()
        if decision == "make" and item.get("planned"):
            status = "planned"
        elif decision == "make":
            status = "blocked"
        else:
            status = "specified"
        matched = runs_by_item.get(item_id, [])
        fields = {
            "type": str(item.get("type", "")).upper(),
            "status": status,
            "item expected": str(item.get("expected", "")).strip(),
            "item acceptance": str(item.get("acceptance", "")).strip(),
            "local input": str(item.get("local_input", "")).strip(),
            "ledger local run": str(item.get("local_run", "")).strip(),
            "ledger run action": str(item.get("action", "")).strip(),
            "ledger run route": str(item.get("address", "")).strip(),
            "ledger result binding": str(item.get("result", "")).strip(),
            "decision": decision,
            "supporting runs valid": bool(item.get("supports_valid")),
            "local run registered": bool(item.get("runs_registered")),
            "supporting runs": str(item.get("supporting_runs", "")).strip(),
            "matching page runs": "; ".join(
                "%s · %s" % (row.get("run_id", "unknown"), row.get("status", "unknown"))
                for row in matched
            ),
            "run": "; ".join(str(row.get("run_id", "unknown")) for row in matched),
            "run status": "; ".join(str(row.get("status", "unknown")) for row in matched),
            "result": "",
            "no selected result": True,
            "display_kind": "",
        }
        projected.append({
            "id": item_id,
            "address": target,
            "title": str(item.get("name", "")).strip() or item_id,
            "fields": fields,
        })
    return projected


def _evidence_blockers(fields: dict[str, object]) -> list[str]:
    """Name ledger gates that are visibly absent; never infer acceptance."""
    blockers = []
    for key, label in (("item expected", "item Expected contract"),
                       ("item acceptance", "item Acceptance checks"),
                       ("local input", "frozen Local Input")):
        if not str(fields.get(key, "")).strip():
            blockers.append(label + " not recorded")
    if not str(fields.get("decision", "")).strip():
        blockers.append("human Decide choice not recorded")
    if not str(fields.get("ledger local run", "")).strip():
        blockers.append("one local Page RE declaration not recorded")
    elif (not str(fields.get("ledger run action", "")).strip()
          or not str(fields.get("ledger run route", "")).strip()):
        blockers.append("typed Local Run action/route is incomplete")
    if not str(fields.get("supporting runs", "")).strip():
        blockers.append("Supporting Runs not recorded; confirm [] when none are needed")
    elif not fields.get("supporting runs valid") or not fields.get("local run registered"):
        blockers.append("Supporting Run and Local Run declarations are not fully registered")
    return blockers


def _evidence_type(record: dict[str, object]) -> str:
    fields = record.get("fields", {})
    kind = str(fields.get("type", "")).strip().upper()
    if kind == "TABLE":
        return "DISPLAY"
    return kind if kind in {"DISPLAY", "CITE", "VALUE"} else "OTHER"


def _status_parts(record: dict[str, object]) -> tuple[str, str]:
    fields = record.get("fields", {})
    raw = str(fields.get("status", "specified")).strip()
    status = raw.lstrip("📝🔗🟢📌✅⚠️⏸✖⛔ ").lower() or "specified"
    status = {
        "ready_for_human_verification": "Needs review",
        "ready_for_review": "Needs review",
        "ready_for_human_review": "Needs review",
        "in_progress": "In progress",
        "not_started": "Planned",
    }.get(status, status.replace("_", " ").capitalize())
    token = re.sub(r"[^a-z0-9_-]", "-", status.lower())
    return status, token


def _detail_row(label: str, value: str, *, code: bool = False) -> str:
    if not value:
        return ""
    rendered = "<code>%s</code>" % html.escape(value) if code else html.escape(value)
    return ('<div class=evidence-detail-row><span class=evidence-detail-label>%s</span>'
            '<span class=evidence-detail-value>%s</span></div>' %
            (html.escape(label), rendered))


def _evidence_run_contract(kind: str) -> dict[str, str]:
    """Reader-facing Run facts for an Evidence Result card, not a new spec."""
    label = {"VALUE": "Value", "CITE": "Citation", "DISPLAY": "Display"}.get(kind, "Evidence")
    work = {
        "VALUE": "Make one focal value Result for this Evidence Item.",
        "CITE": "Make one focal citation/source-bundle Result for this Evidence Item.",
        "DISPLAY": "Make one focal figure, table, algorithm, or other declared display Result for this Evidence Item.",
    }.get(kind, "Make one typed Result for this Evidence Item.")
    worker = ("haipipe-plugin-outline owns VALUE/CITE/DISPLAY payload rules; use only the exact owner-native "
              "Supporting Run worker(s) selected during SURVEY.")
    if kind == "DISPLAY":
        worker += " DISPLAY also uses the haipipe-display front door and the renderer Skill selected for its declared display kind."
    return {
        "name": label,
        "work": work,
        "owner": "haipipe-page-workflow → haipipe-page-evidence",
        "workers": worker,
        "actor": "agent / system / hybrid; any declared human verification remains a human decision",
        "prerequisites": ("Fresh Page Context; accepted Shape and Survey contracts; this item's typed Expected/Acceptance; "
                          "one frozen Local Input and its declared Supporting Runs; human verification when required."),
    }


def _evidence_copy_prompt(record: dict[str, object], page_src: pathlib.Path,
                          root: pathlib.Path, board_path: str, page_path: str,
                          status: str) -> str:
    """Compose a copy-only request for the exact Evidence Item on this card."""
    kind = _evidence_type(record)
    contract = _evidence_run_contract(kind)
    fields = record.get("fields", {})
    item_id = str(record.get("id", "")).strip()
    label = str(fields.get("label", record.get("title", ""))).strip()
    target = str(record.get("address", fields.get("target", ""))).strip()
    run_id = str(fields.get("run", "") or fields.get("local run", "")).strip()
    run_status = str(fields.get("run status", "")).strip() or "not recorded"
    owner_run = str(fields.get("owner run", "")).strip()
    support = str(fields.get("supporting runs", "")).strip() or "none recorded"
    matching_runs = str(fields.get("matching page runs", "")).strip()
    if not matching_runs and run_id:
        matching_runs = "%s · %s" % (run_id, run_status)
    matching_runs = matching_runs or "none recorded"
    blockers = _evidence_blockers(fields)
    no_result = bool(fields.get("no selected result"))
    decision = str(fields.get("decision", "")).strip() or "not recorded"
    item_expected = str(fields.get("item expected", "")).strip() or "not recorded"
    item_acceptance = str(fields.get("item acceptance", "")).strip() or "not recorded"
    local_input = str(fields.get("local input", "")).strip() or "not recorded"
    local_action = str(fields.get("ledger run action", "")).strip() or "not recorded"
    local_route = str(fields.get("ledger run route", "")).strip() or "not recorded"
    result_binding = str(fields.get("ledger result binding", "")).strip() or "not recorded"
    try:
        folder = page_src.parent.relative_to(root).as_posix()
    except ValueError:
        folder = page_src.parent.name
    if folder in {"", "."}:
        folder = page_src.parent.name
    board = board_path.strip()
    if board in {"", "/"}:
        board = "Standalone Page (no Board)"
    if no_result and decision != "make":
        next_action = ("Resolve the required human Decide choice and the SHAPE/SURVEY gates first. Do not allocate or run "
                       "an Evidence Run while this item is only specified.")
    elif no_result and blockers:
        next_action = ("Report these ledger blockers and ask the owner to complete SHAPE/SURVEY before any allocation: "
                       + "; ".join(blockers) + ". Do not invent a Run or treat a planned route as an allocated Run.")
    elif no_result and "; " in matching_runs:
        next_action = ("Several Page Runs map to this item. Compare their Tickets, receipts, targets, and Results, then "
                       "ask which unique lineage to resume; do not select one by ordering.")
    elif no_result and matching_runs != "none recorded":
        next_action = ("Resume only the one recorded matching Page RE after checking its Ticket, receipt, and the current "
                       "owner gates. Do not allocate a second lineage.")
    elif no_result:
        next_action = ("The human has selected make and the ledger prerequisites are present. Recheck accepted Shape/Survey "
                       "contracts, then the owner may allocate the next typed RE if no matching Run now exists.")
    elif status.lower() in {"ready", "complete", "completed", "accepted", "resolved"}:
        next_action = ("Reuse the recorded ready Result and let the Page Evidence owner decide whether EMBED is next. "
                       "Do not create a new Evidence Run unless the owner identifies a new attempt or goal.")
    elif status.lower() in {"needs review", "in progress", "planned", "specified"}:
        next_action = ("Inspect the named item, its current Run/Result, and required human verification. Resume only the "
                       "unique matching Run when its owner contract permits; otherwise name the blocker and hold.")
    else:
        next_action = ("Reconcile this item against the current Run/Result and its Acceptance. The owner must decide "
                       "whether to resume, hold, or commission a new attempt; do not silently replace a Result.")
    lines = [
        "Use haipipe-page-workflow and haipipe-page-evidence for this one typed Page Evidence item.",
        "Board: " + board,
        "Folder: " + folder,
        "Page: " + page_src.stem,
        "Page source: " + (page_path.strip() or page_src.name),
        "Evidence Item: " + item_id + (" · " + label if label else ""),
        "Target: " + (target or "not recorded"),
        "Run Type: Page.evidence-item · " + contract["name"],
        "Run identity: " + {"VALUE": "re-value-NN_<slug>", "CITE": "re-cite-NN_<slug>",
                            "DISPLAY": "re-display-NN_<slug>"}.get(kind, "owner-native Evidence identity"),
        "Bounded work: " + contract["work"],
        "Owner Skill(s): " + contract["owner"],
        "Worker Skill(s): " + contract["workers"],
        "Actor: " + contract["actor"],
        "Prerequisites: " + contract["prerequisites"],
        "Item Expected: " + item_expected,
        "Item Acceptance: " + item_acceptance,
        "Local Input declaration: " + local_input,
        "Ledger Local Run: " + local_action + " · " + local_route,
        "Ledger Result binding: " + result_binding,
        "Decision: " + decision,
        "Current matching Page Run/status: " + matching_runs,
        "Current Result status: " + ("no selected Result" if no_result else status),
        "Supporting Run references: " + support,
        "Owner-native worker Run: " + (owner_run or "none recorded"),
        "Next permitted action: " + next_action,
        "Space affordance: Shown here · read-only; Copy prompt to chat. This copy action is inert until pasted and sent.",
        "Re-read the current Page, selected Outline, Evidence Item ledger, matching Run ticket/receipt, and selected Result before acting. This prompt contains item metadata only: never copy protected payloads or raw rows into chat; use their owner-governed paths.",
    ]
    display_kind = str(fields.get("display_kind", "")).strip()
    if kind == "DISPLAY" and display_kind:
        lines.insert(lines.index("Actor: " + contract["actor"]),
                     "Declared display kind: " + display_kind + "; select its renderer Skill through the Outline owner contract.")
    return "\n".join(lines)


def _copy_prompt_button(prompt: str) -> str:
    label = "Copy prompt to chat"
    return ('<button type="button" class="run-prompt-copy" aria-label="%s" title="%s" '
            'data-run-prompt="%s">⧉ %s</button>' % (
                html.escape(label, quote=True), html.escape(label, quote=True),
                html.escape(prompt, quote=True), html.escape(label)))


def _label_details(labels: object) -> str:
    """Render resolved values with their original token in disclosure.

    The visible value is intentionally short. Opening the row exposes the
    authored token, target path, Evidence Item, Page RE, and Result path so a
    resolved number never loses its evidence identity.
    """
    if not isinstance(labels, list):
        return ""
    rows = []
    for raw in labels:
        if not isinstance(raw, dict):
            continue
        token = str(raw.get("token", "")).strip()
        reference = str(raw.get("reference") or raw.get("key") or token).strip()
        if not token:
            continue
        display = str(raw.get("display", "")).strip()
        status = str(raw.get("status", "unresolved")).strip().lower()
        visible = display if display and status not in {"pending", "unresolved", "missing"} else token
        meta = [
            ("kind", raw.get("kind", "")),
            ("reference", reference),
            ("target", raw.get("target", "")),
            ("item", raw.get("item", "")),
            ("evidence run", raw.get("page_run", "")),
            ("owner run", raw.get("run", "")),
            ("result", raw.get("result", "")),
            ("provenance", raw.get("provenance", "")),
        ]
        meta_html = "".join(
            '<span><b>%s</b> <code>%s</code></span> '
            % (html.escape(key), html.escape(str(value)))
            for key, value in meta if str(value).strip()
        )
        rows.append(
            '<details class=evidence-label-binding><summary>'
            '<span class=evidence-label-visible>%s</span>'
            '<code class=evidence-label-token>%s</code>'
            '<span class=evidence-label-state>%s</span></summary>'
            '<div class=evidence-label-meta>%s</div></details>'
            % (html.escape(visible), html.escape(token), html.escape(status), meta_html)
        )
    return '<div class=evidence-label-list>%s</div>' % "".join(rows) if rows else ""


_PREVIEW_IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".svg"}

def _label_summary(labels: object) -> str:
    """Render the small, reader-facing V/C/D index for an open card."""
    if not isinstance(labels, list):
        return ""
    chips = []
    for raw in labels:
        if not isinstance(raw, dict):
            continue
        token = str(raw.get("token") or raw.get("reference") or raw.get("key") or "").strip()
        if not token:
            continue
        kind = str(raw.get("kind", "")).strip().upper() or "LABEL"
        display = str(raw.get("display", "")).strip()
        status = str(raw.get("status", "unresolved")).strip().lower()
        visible = display if display and status not in {"pending", "unresolved", "missing"} else token
        chips.append(
            '<span class=evidence-label-chip title="%s"><b>%s</b><span>%s</span></span>'
            % (html.escape(token, quote=True), html.escape(kind), html.escape(visible)),
        )
    if not chips:
        return ""
    return '<div class=evidence-label-summary><span class=evidence-label-summary-title>Labels</span>%s</div>' % "".join(chips)
_PREVIEW_PATH_KEYS = {
    "artifact", "artifacts", "asset", "assets", "figure", "image", "preview",
    "preview_path", "table", "file", "path",
}
_PREVIEW_COPY_KEYS = {
    "reader_takeaway", "caption_claim", "summary", "interpretation",
    "aggregate_values", "outcome",
}
_PREVIEW_SUFFIX_ORDER = {
    ".png": 0, ".jpg": 0, ".jpeg": 0, ".webp": 0, ".svg": 1,
    ".pdf": 2, ".csv": 3, ".tsv": 3, ".md": 4,
}


def _payload(document: dict[str, object]) -> object:
    value = document.get("payload")
    return value if value is not None else {}


def _preview_scalar(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return f"{value:,}"
    if isinstance(value, float):
        return str(value)
    if isinstance(value, str):
        return value
    if isinstance(value, list) and all(
        isinstance(item, (str, int, float, bool)) for item in value
    ):
        return ", ".join(_preview_scalar(item) for item in value)
    return ""


def _find_preview_scalar(value: object, keys: set[str], *, path: tuple[str, ...] = (),
                         depth: int = 0) -> tuple[str, str]:
    """Find one useful scalar in a shallow Result payload tree."""
    if depth > 3:
        return "", ""
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key).lower() in keys:
                text = _preview_scalar(child)
                if text:
                    return " · ".join((*path, str(key))), text
        for key, child in value.items():
            if isinstance(child, (dict, list)):
                found = _find_preview_scalar(
                    child, keys, path=(*path, str(key)), depth=depth + 1
                )
                if found[1]:
                    return found
    elif isinstance(value, list):
        for index, child in enumerate(value[:8]):
            found = _find_preview_scalar(
                child, keys, path=(*path, str(index + 1)), depth=depth + 1
            )
            if found[1]:
                return found
    return "", ""


def _preview_label(value: str) -> str:
    return re.sub(r"[_-]+", " ", value).strip().title()
def _value_preview_label(value: str) -> str:
    "Use reader-facing terms for the few Value fields that need context."
    if value.startswith("Historical Cell · "):
        result = value.split(" · ", 1)[1]
        return "Reported Result · " + ("SE" if result == "Se" else result)
    if value == "Replacement Gate":
        return "Gate"
    return value

def _value_preview_rows(value: object, *, prefix: str = "", skip: set[str] | None = None, rows: list[tuple[str, str]] | None = None, limit: int = 40) -> list[tuple[str, str]]:
    """Flatten scalar VALUE payload fields into reader-facing table rows."""
    if rows is None:
        rows = []
    if len(rows) >= limit or not isinstance(value, dict):
        return rows
    skip = {item.lower() for item in (skip or set())}
    for key, child in value.items():
        key_text = str(key)
        if key_text.lower() in skip:
            continue
        label = _preview_label(key_text)
        if prefix:
            label = "%s · %s" % (prefix, label)
        label = _value_preview_label(label)
        if isinstance(child, dict):
            _value_preview_rows(child, prefix=label, skip=skip, rows=rows, limit=limit)
        else:
            text = _preview_scalar(child)
            if not text and child is not None and isinstance(child, (list, tuple)):
                text = json.dumps(child, ensure_ascii=False, default=str)
            if text:
                rows.append((label, text))
        if len(rows) >= limit:
            break
    return rows
def _value_preview_table(payload: object) -> str:
    if not isinstance(payload, dict):
        return ""
    skip = (_PREVIEW_COPY_KEYS - {"outcome"}) | {
        "boundary", "artifact", "artifacts", "preview", "sources"
    }
    rows = _value_preview_rows(payload, skip=skip)
    if not rows:
        return ""
    body = "".join(
        "<tr><th>%s</th><td>%s</td></tr>" %
        (html.escape(label), html.escape(text))
        for label, text in rows
    )
    return ('<div class=evidence-preview-table-wrap><table class="evidence-preview-table evidence-preview-value-table">'
            '<thead><tr><th>Field</th><th>Value</th></tr></thead><tbody>%s</tbody></table></div>' % body)


def _preview_facts(payload: object, *, skip: set[str] | None = None,
                   limit: int = 8, prefix: str = "") -> str:
    if not isinstance(payload, dict):
        return ""
    skip = {item.lower() for item in (skip or set())}
    rows = []
    for key, value in payload.items():
        if str(key).lower() in skip:
            continue
        text = _preview_scalar(value)
        if not text:
            continue
        label = _preview_label(str(key))
        if prefix:
            label = "%s · %s" % (_preview_label(prefix), label)
        rows.append(
            '<div class=evidence-preview-fact><b>%s</b><span>%s</span></div>' %
            (html.escape(label), html.escape(text))
        )
        if len(rows) >= limit:
            break
    return '<div class=evidence-preview-facts>%s</div>' % "".join(rows) if rows else ""


def _preview_table(rows: object, *, limit: int = 8) -> str:
    if not isinstance(rows, list) or not rows or not all(
        isinstance(row, dict) for row in rows[:limit]
    ):
        return ""
    selected = [row for row in rows[:limit] if isinstance(row, dict)]
    columns = []
    for row in selected:
        for key in row:
            if str(key) not in columns:
                columns.append(str(key))
    columns = columns[:8]
    if not columns:
        return ""
    head = "".join(
        "<th>%s</th>" % html.escape(_preview_label(key)) for key in columns
    )
    body = []
    for row in selected:
        cells = []
        for key in columns:
            value = _preview_scalar(row.get(key, ""))
            if not value and row.get(key) is not None:
                value = json.dumps(row.get(key), ensure_ascii=False, default=str)
            cells.append("<td>%s</td>" % html.escape(value))
        body.append("<tr>%s</tr>" % "".join(cells))
    return ('<div class=evidence-preview-table-wrap><table class=evidence-preview-table>'
            '<thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>') % (
                head, "".join(body)
            )


def _payload_table(payload: object) -> str:
    if isinstance(payload, list):
        return _preview_table(payload)
    if not isinstance(payload, dict):
        return ""
    for key in ("rows", "table", "data", "ladder", "comparisons"):
        table = _preview_table(payload.get(key))
        if table:
            return table
    return ""


def _preview_texts(document: dict[str, object], payload: object) -> list[str]:
    keys = ("reader_takeaway", "caption_claim", "summary", "interpretation",
            "aggregate_values")
    values = []
    for source in (payload, document):
        if not isinstance(source, dict):
            continue
        for key in keys:
            text = _preview_scalar(source.get(key))
            if text and text not in values:
                values.append(text)
    return values


def _preview_path_hints(payload: object) -> tuple[str, list[str]]:
    """Return a unit directory and explicit browser-preview artifact hints."""
    if not isinstance(payload, dict):
        return "", []
    unit = _preview_scalar(payload.get("unit"))
    hints: list[str] = []

    def collect(value: object, key: str = "") -> None:
        if isinstance(value, str):
            if value.strip():
                hints.append(value.strip())
            return
        if isinstance(value, list):
            for item in value:
                collect(item, key)
            return
        if isinstance(value, dict):
            for child_key, child_value in value.items():
                if str(child_key).lower() in _PREVIEW_PATH_KEYS:
                    collect(child_value, str(child_key))

    for key, value in payload.items():
        if str(key).lower() in _PREVIEW_PATH_KEYS:
            collect(value, str(key))
    return unit, hints


def _safe_preview_file(candidate: pathlib.Path, page_home: pathlib.Path) -> pathlib.Path | None:
    try:
        if candidate.is_symlink() or not candidate.is_file():
            return None
        resolved = candidate.resolve()
        root = page_home.resolve()
        relative = resolved.relative_to(root)
        # Hidden lanes must not become a back door into the reader. An explicit
        # archive is readable only when an active Result names its artifact;
        # it is not consulted as a legacy Evidence source.
        if any(part.startswith(".") for part in relative.parts):
            return None
        if len(relative.parts) >= 2 and relative.parts[:2] == ("outline", "evidence"):
            return None
        return resolved
    except (OSError, RuntimeError, ValueError):
        return None


def _preview_artifact(record: dict[str, object], page_home: pathlib.Path) -> pathlib.Path | None:
    document = record.get("result_document", {})
    if not isinstance(document, dict):
        return None
    payload = _payload(document)
    unit, hints = _preview_path_hints(payload)
    result_file = record.get("result_file")
    result_dir = result_file.parent if isinstance(result_file, pathlib.Path) else page_home / "results"
    bases = [result_dir, page_home]
    if unit:
        unit_path = pathlib.Path(unit)
        bases.insert(0, unit_path if unit_path.is_absolute() else page_home / unit_path)
        bases.insert(1, unit_path if unit_path.is_absolute() else result_dir / unit_path)
    candidates = []
    for hint in hints:
        raw = hint.split("#", 1)[0].strip().strip("'\"")
        if not raw or "://" in raw or raw.startswith("data:"):
            continue
        path = pathlib.Path(raw)
        if path.is_absolute():
            candidates.append(path)
        else:
            candidates.extend(base / path for base in bases)
    if unit:
        for base in bases[:2]:
            candidates.extend(base / name for name in (
                "preview.png", "figure.png", "table.png", "preview.svg",
                "figure.svg", "preview.pdf", "figure.pdf", "table.pdf",
            ))
    seen = set()
    valid = []
    for candidate in candidates:
        key = str(candidate)
        if key in seen:
            continue
        seen.add(key)
        found = _safe_preview_file(candidate, page_home)
        if found and found.suffix.lower() in _PREVIEW_SUFFIX_ORDER:
            valid.append(found)
    return min(valid, key=lambda path: _PREVIEW_SUFFIX_ORDER[path.suffix.lower()]) if valid else None


def _render_delimited(path: pathlib.Path) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")[:512 * 1024]
        reader = csv.reader(io.StringIO(text), delimiter="\t" if path.suffix.lower() == ".tsv" else ",")
        parsed = []
        for index, row in enumerate(reader):
            parsed.append(row)
            if index >= 8:
                break
    except (OSError, csv.Error):
        return ""
    if not parsed:
        return ""
    columns = [value or "Column %d" % (index + 1)
               for index, value in enumerate(parsed[0][:8])]
    rows = [dict(zip(columns, row[:8])) for row in parsed[1:8]]
    return _preview_table(rows)


def _preview_asset_data(path: pathlib.Path) -> str:
    """Inline a small approved preview because ``results/`` is not public static."""
    if path.suffix.lower() not in _PREVIEW_IMAGE_SUFFIXES | {".pdf"}:
        return ""
    try:
        if path.stat().st_size > 12 * 1024 * 1024:
            return ""
        mime = mimetypes.guess_type(str(path))[0]
        if not mime:
            return ""
        encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    except OSError:
        return ""
    return "data:%s;base64,%s" % (mime, encoded)


def _render_preview_artifact(path: pathlib.Path, data_url: str) -> str:
    suffix = path.suffix.lower()
    if not data_url and suffix not in {".csv", ".tsv", ".md"}:
        return ""
    open_link = ('<a class=evidence-preview-link href="%s" target="_blank" rel="noopener">'
                 'Open full preview</a>' % html.escape(data_url, quote=True)) if data_url else ""
    if suffix in _PREVIEW_IMAGE_SUFFIXES:
        return ('<div class=evidence-preview-media><img class=evidence-preview-image '
                'src="%s" alt="Evidence display preview" loading="lazy">%s</div>' %
                (html.escape(data_url, quote=True), open_link))
    if suffix == ".pdf":
        return ('<div class=evidence-preview-media><object class=evidence-preview-pdf '
                'data="%s" type="application/pdf">%s</object>%s</div>' %
                (html.escape(data_url, quote=True), open_link, open_link))
    if suffix in {".csv", ".tsv"}:
        return _render_delimited(path)
    if suffix == ".md":
        try:
            return '<div class=evidence-preview-copy>%s</div>' % _md_lite(
                path.read_text(encoding="utf-8", errors="replace")[:12000]
            )
        except OSError:
            return ""
    return ""


def _result_preview(record: dict[str, object], page_home: pathlib.Path,
                    root: pathlib.Path | None) -> str:
    """Render substantive Result content, never the envelope metadata."""
    fields = record.get("fields", {})
    if fields.get("no selected result"):
        return ('<section class=evidence-preview><div class=evidence-preview-label>Result</div>'
                '<div class=evidence-preview-empty>No Result selected · %s</div></section>' %
                html.escape(str(fields.get("status", "specified"))))
    document = record.get("result_document", {})
    if not isinstance(document, dict):
        document = {}
    payload = _payload(document)
    kind = _evidence_type(record)
    content = []
    artifact = _preview_artifact(record, page_home)
    if artifact:
        rendered = _render_preview_artifact(artifact, _preview_asset_data(artifact))
        if rendered:
            content.append(rendered)

    if kind == "VALUE":
        boundary = _preview_scalar(payload.get("boundary")) if isinstance(payload, dict) else ""
        if boundary:
            content.append('<div class=evidence-preview-copy><p><b>Boundary</b> %s</p></div>' %
                           html.escape(boundary))
        table = _value_preview_table(payload)
        if table:
            content.append(table)
    elif kind == "CITE" and isinstance(payload, dict):
        sources = payload.get("sources")
        if isinstance(sources, list):
            source_cards = []
            for source in sources[:6]:
                if not isinstance(source, dict):
                    continue
                cite = _preview_scalar(source.get("cite"))
                identity = _preview_scalar(source.get("identity"))
                claim = _preview_scalar(source.get("claim"))
                head = " · ".join(value for value in (cite, identity) if value)
                source_cards.append(
                    '<article class=evidence-preview-source><div class=evidence-preview-source-head>'
                    '<b>%s</b><code>%s</code></div><p>%s</p></article>' %
                    (html.escape(head or "Source"), html.escape(identity), html.escape(claim))
                )
            if source_cards:
                content.append("".join(source_cards))
    elif kind == "DISPLAY":
        # A Display is a reader artifact. Keep its preview PDF/image as the
        # only visual preview; payload metadata stays in Traceability.
        content.append(_preview_facts(
            payload,
            skip={"unit", "artifact", "artifacts", "preview", "table", "data", "rows", "values"}
            | _PREVIEW_COPY_KEYS,
        ))
        content.append(_preview_facts(
            payload, skip={"unit", "artifact", "artifacts", "preview"} | _PREVIEW_COPY_KEYS
        ))
    else:
        table = _payload_table(payload)
        if table:
            content.append(table)
        content.append(_preview_facts(payload, skip=_PREVIEW_COPY_KEYS))

    texts = _preview_texts(document, payload)
    if texts:
        content.append('<div class=evidence-preview-copy>%s</div>' % "".join(
            "<p>%s</p>" % html.escape(text) for text in texts[:3]
        ))
    content = [part for part in content if part]
    if not content:
        status = str(record.get("fields", {}).get("status", "not ready"))
        content.append('<div class=evidence-preview-empty>Result content is not available yet · %s</div>' %
                       html.escape(status))
    return '<section class=evidence-preview><div class=evidence-preview-label>Preview</div>%s</section>' % "".join(content)


def _workspace_actions(path_q: str, file_q: str, run_id: str = "") -> str:
    if not path_q and not file_q:
        return ""
    path = quote(path_q or "", safe="")
    file = quote(file_q or "", safe="")
    runs_href = "/_board/runs?path=%s&file=%s" % (path, file)
    if run_id:
        runs_href += "&space=evidence&run=%s" % quote(run_id, safe="")
    folder_href = "/_board/folderstat?path=%s&file=%s" % (path, file)
    return ('<div class=evidence-actions aria-label="Evidence navigation">'
            '<a class=evidence-action href="%s" target="_blank" rel="noopener">Run Space</a>'
            '<a class=evidence-action href="%s" target="_blank" rel="noopener">'
            'Browse Run + Result folders</a></div>' %
            (html.escape(runs_href, quote=True), html.escape(folder_href, quote=True)))


def _evidence_sections(records: list[dict[str, object]],
                       page_home: pathlib.Path | None = None,
                       root: pathlib.Path | None = None,
                       path_q: str = "", file_q: str = "",
                       page_src: pathlib.Path | None = None) -> str:
    """Render compact typed sections with collapsed, progressive-disclosure cards."""
    if not records:
        return '<div class=ghost>No current Evidence Item or Result.</div>'

    if page_home is None:
        for record in records:
            result_file = record.get("result_file")
            if isinstance(result_file, pathlib.Path):
                page_home = result_file.parent.parent.parent
                break
    page_home = page_home or pathlib.Path.cwd()
    root = root or page_home

    groups: dict[str, list[dict[str, object]]] = {
        "DISPLAY": [], "CITE": [], "VALUE": [], "OTHER": [],
    }
    for record in records:
        groups[_evidence_type(record)].append(record)

    headings = {
        "DISPLAY": ("Displays", "figures · tables · algorithms"),
        "CITE": ("Citations", "verified source claims"),
        "VALUE": ("Values", "scalars · intervals · comparisons"),
        "OTHER": ("Other", "migration items"),
    }
    sections = []
    for kind in ("DISPLAY", "CITE", "VALUE", "OTHER"):
        items = groups[kind]
        if not items:
            continue
        title, hint = headings[kind]
        cards = []
        for record in items:
            item_id = str(record.get("id", "")).strip()
            fields = record.get("fields", {})
            status, status_token = _status_parts(record)
            title_text = str(record.get("title", "")).strip()
            label = str(fields.get("label", "")).strip()
            if not label:
                label = title_text or item_id.split("-", 2)[-1].replace("-", " ")
            address = str(record.get("address", fields.get("target", ""))).strip()
            run_id = str(fields.get("run", "") or fields.get("local run", "")).strip()
            result_path = str(fields.get("result", "")).strip()
            result_note = str(fields.get("has", "")).strip()
            supporting = str(fields.get("supporting runs", "")).strip()
            focus = "run-" + re.sub(r"[^A-Za-z0-9_-]", "-", item_id)
            safe_kind = html.escape(kind, quote=True)
            safe_item = html.escape(item_id, quote=True)
            display_title = title_text if title_text and title_text.lower() != label.lower() else ""
            label_html = _label_details(fields.get("labels", []))
            label_summary = _label_summary(fields.get("labels", []))
            copy_prompt = (_copy_prompt_button(_evidence_copy_prompt(
                record, page_src, root, path_q, file_q, status))
                if (page_src is not None and kind in {"VALUE", "CITE", "DISPLAY"}
                    and str(record.get("address", fields.get("target", ""))).strip()
                    and not (fields.get("no selected result")
                             and str(fields.get("decision", "")).strip() in {"drop", "defer"})) else "")
            contract = _evidence_run_contract(kind) if kind in {"VALUE", "CITE", "DISPLAY"} else None
            run_pattern = {
                "VALUE": "re-value-NN_<slug>",
                "CITE": "re-cite-NN_<slug>",
                "DISPLAY": "re-display-NN_<slug>",
            }.get(kind, "")
            contract_details = ""
            if contract:
                matching = str(fields.get("matching page runs", "")).strip()
                if not matching:
                    matching = ("%s · %s" % (run_id, str(fields.get("run status", "")).strip() or "status not recorded")
                                if run_id else "none recorded")
                matching += " · Result status: " + ("no selected Result" if fields.get("no selected result") else status)
                contract_rows = "".join((
                    _detail_row("Run Type", "Page.evidence-item · " + contract["name"]),
                    _detail_row("Run identity", run_pattern, code=True),
                    _detail_row("Bounded work", contract["work"]),
                    _detail_row("Owner Skill", contract["owner"]),
                    _detail_row("Worker Skill(s)", contract["workers"]),
                    _detail_row("Actor", contract["actor"]),
                    _detail_row("Prerequisites", contract["prerequisites"]),
                    _detail_row("Space affordance", "Shown here · read-only"),
                    _detail_row("Matching Run / status", matching),
                ))
                contract_details = (
                    '<details class=evidence-trace><summary>%s Run · Run Type and ownership</summary>'
                    '<div class=evidence-trace-body>%s</div></details>' % (
                        html.escape(contract["name"]), contract_rows))
            trace = "".join((
                ('<div class=evidence-detail-row><span class=evidence-detail-label>'
                 'Evidence Labels</span><span class=evidence-detail-value>%s</span></div>'
                 % label_html) if label_html else "",
                _detail_row("Evidence Label", label),
                _detail_row("Evidence Item", item_id, code=True),
                _detail_row("Type", kind),
                _detail_row("Bullet", address, code=True),
                _detail_row("Status", status),
                _detail_row("Evidence Run", run_id or "not allocated", code=bool(run_id)),
                _detail_row("Owner Run", str(fields.get("owner run", "")).strip(), code=True),
                _detail_row("Supporting Runs", supporting or "none"),
                _detail_row("Result", result_path or (result_note or "not ready"), code=bool(result_path)),
                _detail_row("Item Expected", str(fields.get("item expected", "")).strip()),
                _detail_row("Item Acceptance", str(fields.get("item acceptance", "")).strip()),
                _detail_row("Local Input", str(fields.get("local input", "")).strip()),
                _detail_row("Ledger Local Run", str(fields.get("ledger local run", "")).strip()),
                _detail_row("Ledger Run action", str(fields.get("ledger run action", "")).strip()),
                _detail_row("Ledger Run route", str(fields.get("ledger run route", "")).strip(), code=True),
                _detail_row("Ledger Result binding", str(fields.get("ledger result binding", "")).strip(), code=True),
                _detail_row("Decision", str(fields.get("decision", "")).strip()),
                _detail_row("Expected", str(fields.get("expected", "")).strip()),
                _detail_row("Acceptance", str(fields.get("acceptance", "")).strip()),
            ))
            detail = "".join((
                label_summary,
                contract_details,
                _result_preview(record, page_home, root),
                '<div class=evidence-prompt-actions>%s</div>' % copy_prompt if copy_prompt else "",
                _workspace_actions(path_q, file_q, run_id),
                '<details class=evidence-trace><summary>Traceability</summary>'
                '<div class=evidence-trace-body>%s</div></details>' % trace,
            ))
            cards.append(
                '<details class=evidence-card id="%s" data-evidence-id="%s" data-evidence-type="%s">'
                '<summary class=evidence-summary><span class=evidence-chevron aria-hidden=true>›</span>'
                '<span class=evidence-kind>%s</span>'
                '<span class=evidence-summary-main><span class=evidence-summary-line>'
                '<span class=evidence-label>%s</span><span class=evidence-title>%s</span></span></span>'
                '<code class=evidence-bullet>%s</code>'
                '<span class="evidence-status %s">%s</span></summary>'
                '<div class=evidence-detail>%s</div></details>' % (
                    html.escape(focus, quote=True), safe_item, safe_kind,
                    safe_kind, html.escape(label), html.escape(display_title),
                    html.escape(address or "—"), html.escape(status_token, quote=True),
                    html.escape(status), detail,
                )
            )
        sections.append(
            '<section id="evidence-%s" class=evidence-type-section data-evidence-type="%s">'
            '<header class=evidence-type-head><h2 class=evidence-type-title>%s</h2>'
            '<span class=evidence-type-count>%d</span><span class=evidence-type-hint>%s</span></header>'
            '<div class=evidence-cards>%s</div></section>' % (
                html.escape(kind, quote=True), html.escape(kind, quote=True),
                html.escape(title), len(items),
                html.escape(hint), "".join(cards)
            )
        )
    return "".join(sections)


def _minimal_table(records: list[dict[str, object]]) -> str:
    """Compatibility name retained for callers of the former flat renderer."""
    return _evidence_sections(records)


def _retired_evidence_paths(page_home: pathlib.Path) -> list[str]:
    """Return only the presence of retired Evidence paths, never their content."""
    outline = page_home / "outline"
    found = []
    if outline.is_dir():
        found.extend(sorted(
            path.relative_to(page_home).as_posix()
            for path in outline.glob("*-evidence.md")
            if path.is_file() or path.is_symlink()
        ))
        retired_folder = outline / "evidence"
        if retired_folder.exists() or retired_folder.is_symlink():
            found.append(retired_folder.relative_to(page_home).as_posix())
    return found


def _migration_notice(page_home: pathlib.Path) -> str:
    paths = _retired_evidence_paths(page_home)
    if not paths:
        return ""
    listed = ", ".join("<code>%s</code>" % html.escape(path) for path in paths[:3])
    extra = " and %d more" % (len(paths) - 3) if len(paths) > 3 else ""
    return (
        '<div class=evidence-migration-blocker><strong>v4 migration required.</strong> '
        'Retired Evidence paths are ignored: %s%s. Move them to '
        '<code>_archive/legacy-outline-evidence/</code> before accepting this Page as v4.</div>'
        % (listed, extra)
    )


def render(page_src: pathlib.Path, path_q: str, file_q: str,
           root: pathlib.Path | None = None) -> str:
    """Render the v4 Evidence Space as typed, Result-first disclosure cards."""
    from live.outline_prompts import assets_html as prompt_assets_html

    page_home = page_src.parent
    records = _evidence_inventory(page_src, _result_records(page_home))
    body = _evidence_sections(records, page_home=page_home, root=root or page_home,
                               path_q=path_q, file_q=file_q, page_src=page_src)
    migration_notice = _migration_notice(page_home)
    counts = {kind: sum(1 for record in records if _evidence_type(record) == kind)
              for kind in ("DISPLAY", "CITE", "VALUE")}
    overview = (
        '<a class=total href="#evidence-items">%d Evidence Items</a>' % len(records) +
        '<a href="#evidence-DISPLAY">%d Displays</a>' % counts["DISPLAY"] +
        '<a href="#evidence-CITE">%d Citations</a>' % counts["CITE"] +
        '<a href="#evidence-VALUE">%d Values</a>' % counts["VALUE"]
    )
    return f"""<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>Evidence Space · {html.escape(page_src.stem)}</title><style>{_CSS}</style>
<body class=embedded>{prompt_assets_html()}<header><h1>Evidence Space</h1></header>
<div id=evidence-items class=evidence-list><div class=evidence-overview>{overview}</div>{migration_notice}
<details class=source-details><summary>Sources</summary><div class=source-body>Result <code>results/**/result.yaml</code>.</div></details>
{body}</div>
<script>
(function(){{var links=document.querySelectorAll('.evidence-overview a'),sections=document.querySelectorAll('.evidence-type-section'),source=document.querySelector('.source-details');
function applyFilter(){{var match=location.hash.match(/^#evidence-(DISPLAY|CITE|VALUE)$/),kind=match?match[1]:"";
sections.forEach(function(section){{section.hidden=!!kind && section.dataset.evidenceType!==kind;}});
if(source)source.hidden=!!kind;
links.forEach(function(link){{var active=!!kind && link.getAttribute('href')==="#evidence-"+kind;link.classList.toggle('active',active);}});
}}
window.addEventListener('hashchange',applyFilter);applyFilter();}})();
(function(){{var q=new URLSearchParams(location.search),id=q.get('focus');if(!id)return;
var row=document.getElementById(id);if(row){{row.open=true;row.classList.add('run-focus');row.scrollIntoView({{block:'center'}});}}}})();
</script>
</body>"""


class EvidenceTabMixin:
    """Current read-only Result-first route for Outline's Evidence Space."""

    # ---- GET/HEAD /_board/evidence?path=…&file=… ------------------------
    def evidence_tab_view(self, head_only=False):
        from urllib.parse import parse_qs, urlparse
        q = parse_qs(urlparse(self.path).query)
        path_q = (q.get("path") or [""])[0]
        file_q = (q.get("file") or [""])[0]
        got = self.target({"path": path_q, "file": file_q})
        if got[0] is None:
            return self.reply(400, {"ok": False, "err": got[1]})
        body = render(got[0], path_q, file_q, root=got[1]).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    # ---- POST /_board/evidence — the shell's write() twin, writes nothing
    def plug_evidence(self, p):
        from urllib.parse import quote
        got = self.target(p)
        if got[0] is None:
            return None, got[1]
        return {"url": "/_board/evidence?path=%s&file=%s"
                % (quote(p.get("path") or ""), quote(p.get("file") or ""))}, None
