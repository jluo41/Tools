"""The 📃 Page document template: the whole HTML, CSS and JS shell that
outline.render fills with str.format (moved verbatim from outline.py).
"""
_PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>
:root{{--bg:#ffffff;--fg:#1c1c1c;--mut:#7c7c78;--line:#e4e4e7;--card:#fff;
 --warn:#b3541e;--ok:#3a7d44;--acc:#3e5c84}}
@media(prefers-color-scheme:dark){{:root{{--bg:#161719;--fg:#e8e8e6;
 --mut:#9a9a97;--line:#2c2e33;--card:#1d1f23;--warn:#e0955a;--ok:#7dbb87;
 --acc:#7d9cc4}}}}
body{{margin:0;padding:16px;background:var(--bg);color:var(--fg);
 font:15px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}
h1{{font-size:17px;margin:0 0 2px}} .mut{{color:var(--mut);font-size:13px}}
/* Three calm workspaces replace the old process-record strip. */
.spaces,.subchips{{display:flex;gap:5px;margin:10px 0 6px;flex-wrap:wrap}}
.subchips{{display:none;margin:0 0 10px;padding-left:2px}}
.subchips.show{{display:flex}}
.space,.chip{{font:600 11.5px -apple-system,sans-serif;border:1px solid var(--line);
 border-radius:8px;padding:3px 9px;cursor:pointer;background:var(--card);
 color:var(--fg);white-space:nowrap;flex:0 0 auto}}
.space.on,.chip.on{{border-color:var(--acc);color:var(--acc)}}
.subchips .chip{{font-weight:500;color:var(--mut);background:transparent}}
.subchips .chip.on{{color:var(--acc);background:var(--card)}}
.ok{{color:var(--ok);font-weight:600}} .warn{{color:var(--warn);font-weight:600}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:10px;
 padding:10px 14px;margin:0 0 10px}}
.card h2{{font-size:15px;margin:0 0 4px;display:flex;gap:8px;
 align-items:baseline}}
.card h2 .tally{{margin-left:auto;flex:none;font:600 11px ui-monospace,
 Menlo,monospace;color:var(--mut)}}
.card h2 .tally.all{{color:var(--ok)}}
.lead{{font-size:14.5px;margin:6px 0 0;color:var(--fg)}}
.tally{{display:flex;flex-wrap:wrap;gap:10px;align-items:center;
 margin:10px 0 6px;font-size:12px}}
.tally b{{font-weight:600}}
.bar{{display:inline-block;width:84px;height:7px;border-radius:4px;
 background:var(--line);overflow:hidden}}
.bar i{{display:block;height:100%;background:var(--ok)}}
.left{{color:var(--fg)}} .wait{{color:var(--warn);font-weight:600}}
details{{margin:4px 0 0}}
summary{{cursor:pointer;font:600 12px -apple-system,sans-serif;
 color:var(--mut);text-transform:uppercase;letter-spacing:.03em;
 padding:3px 0;list-style:none}}
summary::-webkit-details-marker{{display:none}}
summary:before{{content:"▸ ";color:var(--mut)}}
details[open]>summary:before{{content:"▾ "}}
summary:hover{{color:var(--acc)}}
.brief{{color:var(--mut);font-size:13.5px;margin:0 0 8px;
 padding-bottom:8px;border-bottom:1px solid var(--line)}}
.sub{{font:600 12.5px -apple-system,sans-serif;color:var(--mut);
 text-transform:uppercase;margin:8px 0 2px}}
.row{{display:flex;gap:8px;padding:2px 0;font-size:14px;line-height:1.55;
 align-items:baseline}}
.row .t{{flex:none}} .row .x{{flex:1;min-width:0}}
.idtag{{flex:none;font:500 12px ui-monospace,Menlo,monospace;color:var(--mut)}}
/* A TAG, not a pill. As a rounded 14px pill on its own flex column it wrapped
   its own label onto two lines and pushed the sentence into half the pane
   (JL 260817, screenshot). Small, nowrap, inline at the end of the sentence. */
.evchip,.evtag{{display:inline;white-space:nowrap;
 font:12px/1.45 ui-monospace,Menlo,monospace;
 border:1px solid color-mix(in srgb,currentColor 26%,transparent);
 background:color-mix(in srgb,currentColor 8%,transparent);
 border-radius:4px;padding:0 4px;color:inherit;vertical-align:1px}}
.evchip{{cursor:pointer}} a.evchip{{text-decoration:none}}
.evtag{{border-style:dashed}}
/* A bullet with hidden detail is a details element: the row shows only the
   terse head + chips, and clicking unfolds the Answered:/Drawn: text (JL 260819:
   "点击之后能看到这个 bullet point 稍微详细一点、但又非常 concise 的解释…
   像 figure 之类的，其实完全可以放到 hidden text 里面"). Native, script-free,
   like the popovers. */
/* HARD RESET: the board shell injects this card into a page that styles its
   own drawers' summary/row classes (big, bold, accent-coloured — JL 260819
   screenshot: one folded bullet rendered like a section heading). Restate
   every typography and layout property so no host rule survives cascade. */
details.brow{{margin:0;padding:0;border:0;background:none}}
details.brow>summary{{list-style:none!important;cursor:pointer;display:flex;
 gap:8px;padding:2px 0;margin:0;border:0;background:none;font-size:14px;
 line-height:1.55;align-items:baseline;font-weight:400;color:var(--fg);
 text-transform:none;letter-spacing:normal;font-family:inherit}}
details.brow>summary .x{{flex:1;min-width:0;font-size:14px;font-weight:400;
 color:var(--fg);text-transform:none;letter-spacing:normal}}
details.brow>summary .addr{{font:500 11.5px ui-monospace,Menlo,monospace;
 color:var(--mut);flex:none;min-width:76px;text-align:left;
 text-transform:none}}
/* the paragraph row is a LEVEL, not another bullet (JL 260819: "hard to
   distinguish with the bullet point"): a thin rule above and a heavier,
   slightly spaced label make the structure visible at a skim. */
/* JL picked the ACCENT BAR (260819, from four previews): a short colored
   bar juts into the left gutter beside the paragraph label, dark text,
   and the bullets stay flush — the bar alone carries the hierarchy. */
.prow{{margin-top:10px;position:relative;margin-left:-9px;
 padding-left:9px}}
/* a short tick, not a full-height bar (JL 260819: "this one is too long"):
   0.85em tall, vertically centered on the label line. */
.prow::before{{content:"";position:absolute;left:0;top:50%;
 transform:translateY(-50%);width:3px;height:.85em;
 background:var(--acc);border-radius:2px}}
.prow .mut{{font-weight:650;font-size:13.5px;color:var(--fg);
 letter-spacing:.01em}}
.paragraph-group{{margin:18px 0 24px;border:0;border-radius:0;background:var(--card)}}
details.paragraph-group>summary{{list-style:none!important;display:flex;gap:8px;
 align-items:baseline;cursor:pointer;padding:7px 9px;margin:0;background:var(--card);
 border:0;font-size:13.5px;line-height:1.45;font-weight:650;color:var(--fg);text-transform:none;letter-spacing:normal}}
details.paragraph-group>summary::-webkit-details-marker{{display:none!important}}
details.paragraph-group>summary::before{{content:"▸";color:var(--acc);flex:none;width:10px}}
details.paragraph-group[open]>summary::before{{content:"▾"}}
details.paragraph-group>summary:hover{{background:color-mix(in srgb,var(--acc) 7%,var(--card))}}
.paragraph-group .prow{{margin:0;padding:0;border:0;background:none}}
.paragraph-group .prow::before{{display:none}}
/* Paragraph headers do not share the bullet address gutter.  The global
   `.addr` rule reserves a wide bullet column so Cx.Px.Bx rows stay aligned;
   applying that same width to the paragraph summary creates an artificial
   gap between `C1.P1` and its title (JL 260914 screenshot). */
details.paragraph-group>summary .addr{{min-width:0;margin-right:0}}
.paragraph-bullets{{padding:0;border-top:1px solid var(--line)}}
.point-group{{padding:0;border-bottom:1px solid var(--line);display:grid;grid-template-columns:minmax(0,1fr) minmax(0,3fr);gap:0}}
.point-plan,.point-preview{{min-width:0;overflow-wrap:anywhere}}
.point-plan{{padding:12px 14px 12px 0}}
.point-preview{{padding:12px 0 12px 16px;border-left:1px solid var(--line)}}
.preview-columns{{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,3fr);gap:0;font:500 12px/1.5 system-ui,sans-serif;color:var(--mut);padding:8px 0;border-bottom:1px solid var(--line)}}
.preview-columns>span:last-child{{padding-left:16px}}
.point-preview>.preview-copy{{font:16px/1.65 Georgia,serif;color:var(--fg);text-transform:none;letter-spacing:normal;padding:0;white-space:pre-wrap;min-height:44px;display:block}}
.resolved-evidence{{display:inline;margin:0 1px;vertical-align:baseline}}
.resolved-evidence>summary{{display:inline;cursor:pointer;list-style:none;color:var(--fg);font:inherit}}
.resolved-evidence>summary::-webkit-details-marker{{display:none}}
.resolved-evidence>summary:after{{content:"⌄";color:var(--mut);font:11px system-ui,sans-serif;margin-left:2px}}
.resolved-evidence[open]>summary:after{{content:"⌃"}}
.resolved-evidence-detail{{display:block;margin:3px 0 5px;padding:4px 7px;border:1px solid var(--line);border-radius:5px;background:var(--card);font:11px/1.45 system-ui,sans-serif;color:var(--mut);white-space:normal}}
.resolved-evidence-detail code{{color:var(--fg);font:10.5px ui-monospace,Menlo,monospace;overflow-wrap:anywhere}}
.missing-evidence-token{{color:var(--warn);font:13px ui-monospace,Menlo,monospace}}
.preview-placeholder{{color:var(--mut);font:13px/1.55 system-ui,sans-serif}}
.preview-stale{{font:12px/1.5 system-ui,sans-serif;color:var(--warn);margin-bottom:6px}}
.page-details{{margin:2px 0 8px}}
.page-details>summary,.plan-details>summary{{font:12px/1.6 system-ui,sans-serif;text-transform:none;letter-spacing:normal}}
.plan-card{{border:0;border-radius:0;padding:0}}
.plan-details{{margin:8px 0}}
.division-title{{font-size:14px;margin:14px 0 8px}}
@media(max-width:560px){{body{{padding:12px}}.point-plan{{padding:10px 9px 10px 0}}.point-preview{{padding:10px 0 10px 10px}}.preview-columns>span:last-child{{padding-left:10px}}.point-head{{font-size:13px!important}}.point-preview>.preview-copy{{font-size:14px;line-height:1.65}}.spaces{{gap:4px}}.spaces .space{{font-size:11px;padding:4px 6px}}}}
.point-group:last-child{{border-bottom:0}}
.point-head{{display:block;font-size:14px;line-height:1.55}}
.point-address{{font:500 10.5px ui-monospace,Menlo,monospace;color:var(--mut);margin-right:5px;
 text-decoration:none;border-radius:3px}}
.point-address:hover,.point-address:focus-visible{{color:var(--acc);outline:2px solid var(--acc);
 outline-offset:2px}}
.point-label{{font:650 12px -apple-system,sans-serif;color:var(--acc);margin-right:6px}}
.point-statement{{color:var(--fg)}}
/* Evidence is part of the Bullet's reading contract, but the full item still
   lives in Evidence Space. Keep only a compact, read-only route here and let
   it follow the waypoint naturally. A source-free `none` decision has no
   visible marker; its meaning remains in the authored Markdown and the row's
   data attributes. */
.point-evidence{{display:inline;margin-left:6px;font:12px/1.45 ui-monospace,Menlo,monospace;
 color:var(--mut)}}
.point-evidence .evchip,.point-evidence .evtag{{display:inline;margin-left:4px}}
.point-evidence .evchip:first-child,.point-evidence .evtag:first-child{{margin-left:0}}
.point-notes{{margin:3px 0 0 1.2em;padding:0 0 0 1em;color:var(--mut);font-size:12.5px;line-height:1.5}}
.point-notes li{{padding-left:2px}}
.point-transition{{margin:6px 0 0 1.2em;color:var(--acc);font-size:12.5px;line-height:1.45}}
.point-transition span{{color:var(--mut)}}
/* the host shell draws its drawer triangle with ::before, which ::marker
   rules never touch — kill every pseudo that could carry a glyph */
details.brow>summary::before{{content:none!important;display:none!important}}
details.brow>summary::after{{content:none!important}}
details.brow>summary::-webkit-details-marker{{display:none!important}}
details.brow>summary::marker{{content:""!important;display:none!important}}
details.brow>summary:hover{{background:color-mix(in srgb,var(--fg) 5%,transparent)}}
.bdetail{{margin:1px 0 7px 3.6em;color:var(--mut);font-size:13px;
 line-height:1.5;max-width:62em}}
.evchip:hover,.evchip:focus-visible{{background:color-mix(in srgb,currentColor 18%,transparent);
 border-color:color-mix(in srgb,currentColor 45%,transparent)}}
.chipcard{{margin:auto;max-width:min(44em,calc(100vw - 2rem));padding:8px 11px;
 max-height:min(46vh,20em);overflow:auto;border:1px solid var(--line);
 border-left-width:3px;border-radius:8px;background:var(--card);color:var(--fg);
 font:14px/1.6 -apple-system,BlinkMacSystemFont,sans-serif;
 box-shadow:0 6px 20px rgba(0,0,0,.18)}}
@supports selector(:popover-open){{.chipcard:not(:popover-open){{display:none}}}}
.chipcard::backdrop{{background:rgba(0,0,0,.12)}}
.chipcard.ok{{border-left-color:var(--ok)}}
.chipcard.warn{{border-left-color:var(--warn)}}
.chipcard.mut{{border-left-color:var(--mut)}}
.cch{{display:flex;gap:7px;align-items:baseline;flex-wrap:wrap;
 padding-bottom:4px;margin-bottom:5px;border-bottom:1px solid var(--line)}}
.cch b{{font:600 12px ui-monospace,Menlo,monospace;word-break:break-all}}
.cck{{font:10px ui-monospace,Menlo,monospace;color:var(--mut);
 letter-spacing:.04em;text-transform:uppercase}}
.ccb p{{margin:0}}
/* THE FIGURE, in the panel the chip opens. A display unit whose mark opens a
   panel holding only its claim sends the reader out of the tab to see the one
   thing the mark is about (JL 260818). Bounded so the plan stays skimmable:
   the panel is evidence, never the page. */
.evfig{{display:block;width:100%;max-height:32vh;margin:0 0 7px;
 border:1px solid var(--line);border-radius:5px;background:#fff;
 object-fit:contain}}
object.evfig{{height:32vh}}
@supports (position-area:block-end){{
 .chipcard{{position:fixed;inset:auto;margin:0;
  position-area:block-end span-inline-end;
  position-try-fallbacks:flip-block,flip-inline}}}}
.ev>summary::-webkit-details-marker{{display:none}}
.ev>summary:hover{{text-decoration:underline dotted}}
.evbody{{margin:3px 0 5px 62px;padding:7px 10px;border-left:2px solid var(--line);color:var(--fg);font-size:13.5px;background:var(--card)}}
.sep{{opacity:.45;padding:0 2px}}
.addr{{font:500 11.5px ui-monospace,Menlo,monospace;color:var(--mut);flex:none;min-width:76px;text-align:left}} /* 76px fits C14.P2.B4; one shared column, so paragraph and bullet titles start at the same x (JL 260819: aligned) */
/* The SECTION address is LEFT aligned, and the bullet addresses stay right.
   A right-aligned gutter ends `C3` and `P1.B1` at the same x, so the two
   character section id sits FURTHER RIGHT than the five character bullet id
   beneath it and the hierarchy reads backwards (JL 260818, screenshot). */
.addr.sec{{text-align:left;min-width:0;margin-right:8px}}
.bundles{{margin:7px 0 8px;padding:5px 8px;border:1px solid var(--line);
 border-radius:7px;background:color-mix(in srgb,var(--acc) 3%,var(--card))}}
.bundles>summary{{font-size:10px}}
.planmeta{{margin:2px 0 7px;color:var(--mut);font-size:12.5px;line-height:1.45}}
.cyclebar{{display:flex;align-items:center;gap:13px;flex-wrap:wrap;margin:2px 0 7px;
 font:500 11px ui-monospace,Menlo,monospace;color:var(--mut)}}
.cyclebar span{{white-space:nowrap}}.cyclebar b{{font-weight:500;margin-right:3px}}
.cyclebar .done{{color:var(--ok)}}.cyclebar .current{{color:var(--fg);font-weight:700;
 background:color-mix(in srgb,var(--acc) 12%,var(--card));border-radius:5px;padding:0 5px}}
.bundle-row{{display:flex;gap:7px;align-items:baseline;padding:2px 0;
 font-size:11px;line-height:1.35;border-top:1px solid var(--line)}}
.bundle-row:first-of-type{{border-top:0}}
.bundle-kind{{flex:none;font:500 10px ui-monospace,Menlo,monospace;
 color:var(--mut);text-transform:uppercase}}
.bundle-items{{flex:1;min-width:0;color:var(--fg);overflow-wrap:anywhere}}
.bundle-state{{flex:none;font:500 10px ui-monospace,Menlo,monospace}}
.now{{display:inline-block;font:600 10px -apple-system,sans-serif;
 text-transform:uppercase;letter-spacing:.04em;color:var(--acc);
 margin-right:6px;vertical-align:1px}}
.row .badge{{flex:none;font:500 11px ui-monospace,Menlo,monospace;
 color:var(--acc);border:1px solid var(--line);border-radius:6px;
 padding:0 6px;cursor:pointer;text-decoration:none}}
.st{{color:var(--mut);font-size:12px;margin:0 0 4px 2px;padding-left:10px;
 border-left:2px solid var(--line)}}
.err{{color:var(--warn);font-size:12px}}
/* the sibling-file records, one shape for every kind (0.18.0) */
.rmeta{{margin:0 0 6px;font:11.5px ui-monospace,Menlo,monospace}}
.rec{{padding:8px 0 6px;border-top:1px solid var(--line)}}
.rec:first-of-type{{border-top:0;padding-top:2px}}
.rh{{display:flex;gap:8px;align-items:baseline;flex-wrap:wrap}}
.rid{{flex:none;font:600 11px ui-monospace,Menlo,monospace;color:var(--acc);
 border:1px solid var(--line);border-radius:6px;padding:0 6px;white-space:nowrap}}
.rt{{flex:1;min-width:12em;font-size:14.5px;font-weight:600;line-height:1.4}}
.pill{{flex:none;font:600 10.5px -apple-system,sans-serif;text-transform:uppercase;
 letter-spacing:.04em;border-radius:999px;padding:1px 8px;border:1px solid currentColor;
 max-width:16em;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.pill.ok{{color:var(--ok)}} .pill.warn{{color:var(--warn)}}
.pill.mut{{color:var(--mut)}} .pill.acc{{color:var(--acc)}}
.rrows{{margin-top:3px}}
.rr{{display:grid;grid-template-columns:5.4em 1fr;gap:6px;font-size:13.5px;
 line-height:1.5;padding:1px 0}}
.rr b{{font:600 11px -apple-system,sans-serif;color:var(--mut);text-transform:uppercase;
 letter-spacing:.04em;padding-top:3px}}
.rq{{margin:3px 0 0 5.8em;padding-left:9px;border-left:2px solid var(--line);
 color:var(--mut);font-size:12.5px;line-height:1.5}}
.rd{{margin:3px 0 0 5.8em}} .rd>summary{{font-size:11.5px;color:var(--mut);
 cursor:pointer;list-style:none}}
.rd>summary::-webkit-details-marker{{display:none}}
.rd>summary::before{{content:"▸ "}} .rd[open]>summary::before{{content:"▾ "}}
.rdb{{margin:3px 0 0;padding-left:9px;border-left:2px solid var(--line);color:var(--mut);
 font-size:13px;line-height:1.5;overflow-wrap:anywhere}}
.rec>.rdb{{margin-left:5.8em}}
.rgrp{{margin:12px 0 4px;font:600 12px -apple-system,sans-serif;color:var(--mut);
 text-transform:uppercase;letter-spacing:.05em}}
.rpre{{color:var(--mut);font-size:13px;margin:2px 0;line-height:1.5}}
/* Feedback is a decision surface, not a source-file dump. Keep the reviewer's
   ask and each requested change visible; fold order, gate, provenance and
   routing so all metadata does not compete at the same visual weight. */
.fbsummary{{display:flex;gap:12px;flex-wrap:wrap;margin:1px 0 12px;
 color:var(--mut);font:600 11.5px ui-monospace,Menlo,monospace}}
.fbsummary b{{color:var(--fg);font-weight:650}}
.fbgroup{{display:flex;gap:8px;align-items:baseline;margin:12px 0 4px}}
.fbgroup .rid{{border:0;padding:0;color:var(--acc)}}
.fbgtitle{{font-size:14px;font-weight:650}}
.fbask{{margin:7px 0 6px;padding:8px 11px;border-left:3px solid var(--acc);
 border-radius:0 7px 7px 0;background:color-mix(in srgb,var(--acc) 5%,var(--card));
 font-size:14px;line-height:1.55}}
.fbask b,.fbwork b{{font:650 10.5px -apple-system,sans-serif;color:var(--acc);
 text-transform:uppercase;letter-spacing:.05em;margin-right:7px}}
.fbsource{{color:var(--mut);font-size:12.5px;line-height:1.45;margin:1px 0 5px}}
.fbcontext{{margin:2px 0 9px}} .fbcontext>summary{{font-size:11px}}
.fbcontext .rdb{{margin-left:0}}
.fbmsg{{margin:6px 0 3px;font-size:14px;line-height:1.55;color:var(--fg)}}
.fbwork{{margin:3px 0;color:var(--mut);font-size:13px;line-height:1.5}}
.fbaux{{display:grid;grid-template-columns:4.8em 1fr;gap:5px;
 padding:1px 0;font-size:12.5px;line-height:1.5}}
.fbaux b{{font:600 10px -apple-system,sans-serif;color:var(--mut);
 text-transform:uppercase;letter-spacing:.04em;padding-top:3px}}
.fbroute{{margin:3px 0;padding-left:9px;border-left:2px solid var(--line);
 color:var(--mut);font-size:12.5px;line-height:1.5}}
.rec.record-focus,.point-group.record-focus{{outline:2px solid var(--acc);outline-offset:4px;border-radius:9px;
 scroll-margin-top:12px}}
.lens .card pre{{white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px}}
.workspace-frame{{display:block;width:100%;height:calc(100vh - 150px);
 min-height:180px;border:1px solid var(--line);border-radius:10px;background:var(--card)}}
{structure_css}
{runs_css}
{space_css}
.source-map{{display:flex;gap:10px;flex-wrap:wrap;margin:4px 0 10px;color:var(--mut);
 font:11px/1.45 ui-monospace,Menlo,monospace}}
.source-map code{{font-size:11px;color:var(--fg)}}
.source-details{{margin:4px 0 10px}}
.source-details>summary{{display:inline-block;cursor:pointer;color:var(--mut);
 font:12px/1.5 system-ui,sans-serif}}
.source-details[open]>summary{{color:var(--fg)}}
.source-details .source-map{{margin:4px 0 0}}
.draft-mode-switcher{{display:flex;align-items:center;gap:5px;margin:2px 0 12px}}
.draft-mode-label{{font:600 10px/1.5 system-ui,sans-serif;color:var(--mut);
 text-transform:uppercase;letter-spacing:.05em;margin-right:2px}}
.draft-mode-tab{{font:600 11.5px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
 border:1px solid var(--line);border-radius:7px;padding:3px 9px;cursor:pointer;
 background:var(--card);color:var(--mut)}}
.draft-mode-tab.on{{border-color:var(--acc);color:var(--acc)}}
.scratch-run-note{{display:none;margin:-5px 0 12px;padding:7px 10px;border-left:2px solid var(--acc);
 color:var(--mut);font-size:12px;line-height:1.5}}
.draft-lens[data-draft-mode="scratch"] .scratch-run-note{{display:block}}
.scratch-run-note b{{color:var(--fg)}}
.scratch-run-meta{{display:none;color:var(--mut);font:10.5px/1.3 ui-monospace,Menlo,monospace}}
.draft-lens[data-draft-mode="scratch"] .scratch-run-meta{{display:inline}}
.paragraph-reading{{display:none}}
.reading-line{{display:grid;grid-template-columns:2.6em minmax(0,1fr);gap:10px;
 padding:8px 0;border-bottom:1px solid var(--line);align-items:start}}
.reading-line:last-child{{border-bottom:0}}
.reading-address{{padding-top:3px;font:500 11px/1.5 ui-monospace,Menlo,monospace;
 color:var(--mut)}}
.reading-copy{{max-width:78ch;font:16px/1.7 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
 color:var(--fg);overflow-wrap:anywhere}}
.reading-copy .resolved-evidence-detail{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}}
.draft-lens[data-draft-mode="reading"] .paragraph-bullets{{display:none}}
.draft-lens[data-draft-mode="reading"] .paragraph-reading{{display:block}}
.draft-lens[data-draft-mode="reading"] details.paragraph-group>summary{{cursor:pointer}}
.draft-lens[data-draft-mode="reading"] details.paragraph-group>summary::before{{content:"▸";color:var(--acc);flex:none;width:10px}}
.draft-lens[data-draft-mode="reading"] details.paragraph-group[open]>summary::before{{content:"▾"}}
.draft-lens[data-draft-mode="reading"] details.paragraph-group>summary:hover{{background:color-mix(in srgb,var(--acc) 7%,var(--card))}}
.draft-lens[data-draft-mode="reading"] .paragraph-group{{margin-bottom:28px}}
@media (max-width:700px){{
 .reading-line{{grid-template-columns:2.3em minmax(0,1fr);gap:7px;padding:7px 0}}
 .reading-copy{{font-size:15px;line-height:1.65}}
}}
.lens{{display:none}} .lens.show{{display:block}}
code{{font:12px ui-monospace,Menlo,monospace}}
</style></head><body>
<h1>📃 {title}</h1>
{board_link}
{band}
<div class=spaces>
 <button class="space on" data-space=bullet data-default=div>Draft</button>
 <button class=space data-space=evidence data-default=evidence>Evidence</button>
 <button class=space data-space=delivery data-default=delivery>Delivery</button>
</div>
<div class="lens show draft-lens space-split" id=lens-div data-draft-mode={draft_mode}>
 <div class=space-main>
 <div class=draft-mode-switcher role=group aria-label="Draft view" title="{draft_reads}">
  <button type=button class="draft-mode-tab{table_on}" data-draft-mode=table>Table</button>
  <button type=button class="draft-mode-tab{reading_on}" data-draft-mode=reading>Reading</button>
  <button type=button class="draft-mode-tab{scratch_on}" data-draft-mode=scratch>Scratch</button>
  <button type=button class="draft-mode-tab{roadmap_on}" data-draft-mode=roadmap>RoadMap Draw</button>
  <button type=button class="draft-mode-tab{revise_on}" data-draft-mode=revise>Revise</button>
 </div>
 <div class=draft-structure>{structure}</div>
 {by_div}
 <div class=draft-roadmap>{roadmap}</div>
 </div>
 {runs_draft}
</div>
<div class="lens space-split" id=lens-evidence><div class=space-main>{evidence_space}</div>{runs_evidence}</div>
<div class=lens id=lens-run><iframe class=workspace-frame
 title="Run Space" data-src="{run_url}"></iframe></div>
<div class="lens space-split" id=lens-delivery><div class=space-main>{delivery_space}</div>{runs_delivery}</div>
<script>
var SPACE_FOR={{div:'bullet',evidence:'evidence',run:'run',delivery:'delivery',workspace:'evidence'}};
var params=new URLSearchParams(location.search), requested=params.get('lens')||'',
    requestedSeg=params.get('seg')||'',
    requestedFocus=params.get('focus')||'', requestedRun=params.get('run')||'',
    requestedDraftMode=['scratch','reading','roadmap','revise'].indexOf(params.get('view'))>=0?params.get('view'):'table';
/* v4 keeps old workspace URLs readable while exposing four plain spaces. */
if(requested==='prog')requested='div';
if(requested==='workspace')requested=(requestedSeg==='runs'||requestedRun)?'run':'evidence';
if(!requested&&(requestedSeg||requestedFocus||requestedRun))
  requested=(requestedSeg==='runs'||requestedRun)?'run':'evidence';
function workspaceSource(frame,name){{
  var src=frame.dataset.src||'';
  if(name==='evidence'&&requestedSeg&&requestedSeg!=='runs')
    src+=(src.indexOf('?')<0?'?':'&')+'seg='+encodeURIComponent(requestedSeg);
  if(requestedFocus)src+=(src.indexOf('?')<0?'?':'&')+'focus='
                         +encodeURIComponent(requestedFocus);
  if(requestedRun)src+=(src.indexOf('?')<0?'?':'&')+'run='
                       +encodeURIComponent(requestedRun);
  return src;
}}
function showLens(c){{
    document.querySelectorAll('.lens-chip').forEach(function(x){{
      x.classList.remove('on');}});
    document.querySelectorAll('.lens').forEach(function(x){{
      x.classList.remove('show');}});
    if(c)c.classList.add('on');
    var lens=document.getElementById('lens-'+c.dataset.lens);
    lens.classList.add('show');
    if(c.dataset.lens==='evidence'||c.dataset.lens==='run'||c.dataset.lens==='delivery'){{
      var frame=lens.querySelector('iframe.workspace-frame'),src=workspaceSource(frame,c.dataset.lens);
      if(src)frame.setAttribute('src',src);
    }} else {{
      var nested=lens.querySelector('iframe');
      if(nested && !nested.getAttribute('src') && nested.dataset.src)
        nested.setAttribute('src',nested.dataset.src);
    }}
}}
function activateLens(name){{
  var space=SPACE_FOR[name]||'bullet';
  document.querySelectorAll('.space').forEach(function(x){{
    x.classList.toggle('on',x.dataset.space===space);}});
  document.querySelectorAll('.subchips').forEach(function(x){{
    x.classList.toggle('show',x.dataset.subspace===space);}});
  var chip=document.querySelector('.lens-chip[data-lens="'+name+'"]');
  if(chip)showLens(chip);
  else{{
    var lens=document.getElementById('lens-'+name);
    if(lens){{document.querySelectorAll('.lens').forEach(function(x){{x.classList.remove('show');}});
      lens.classList.add('show');
      if(name==='evidence'||name==='run'||name==='delivery'){{
        var frame=lens.querySelector('iframe.workspace-frame'),src=workspaceSource(frame,name);
        if(src)frame.setAttribute('src',src);
      }}
    }}
  }}
  document.dispatchEvent(new CustomEvent('lens-shown',{{detail:{{name:name,focus:requestedFocus}}}}));
}}
document.querySelectorAll('.lens-chip').forEach(function(c){{
  c.addEventListener('click',function(){{activateLens(c.dataset.lens);}});
}});
document.querySelectorAll('.space').forEach(function(c){{
  c.addEventListener('click',function(){{activateLens(c.dataset.default);}});
}});
function activateDraftMode(mode,writeUrl){{
  mode=['scratch','reading','roadmap','revise'].indexOf(mode)>=0?mode:'table';
  var lens=document.getElementById('lens-div');
  if(lens)lens.setAttribute('data-draft-mode',mode);
  /* RoadMap Draw loads its canvas the first time it shows */
  if(mode==='roadmap')document.querySelectorAll('#lens-div iframe.page-roadmap-frame').forEach(function(f){{
    if(!f.getAttribute('src')&&f.dataset.src)f.setAttribute('src',f.dataset.src);
  }});
  document.querySelectorAll('.draft-mode-tab').forEach(function(x){{
    x.classList.toggle('on',x.dataset.draftMode===mode);
  }});
  if(mode==='scratch')document.querySelectorAll('#lens-div details.paragraph-group').forEach(function(x){{
    x.open=true;
  }});
  if(mode==='reading'||mode==='revise')document.querySelectorAll('#lens-div details.paragraph-group').forEach(function(x){{
    x.open=true;
  }});
  if(writeUrl!==false)try{{
    var u=new URL(location.href);
    if(mode!=='table')u.searchParams.set('view',mode);
    else u.searchParams.delete('view');
    history.replaceState(null,'',u.href);
  }}catch(e){{}}
}}
document.querySelectorAll('.draft-mode-tab').forEach(function(c){{
  c.addEventListener('click',function(){{activateDraftMode(c.dataset.draftMode,true);}});
}});
document.querySelectorAll('a.badge').forEach(function(a){{
  a.addEventListener('click',function(ev){{
    ev.preventDefault();
    activateLens('div');
    var el=document.getElementById(a.getAttribute('href').slice(1));
    if(el)el.scrollIntoView({{behavior:'smooth'}});
  }});
}});
function focusRecord(id){{
  /* A bullet permalink is a table address. Switch back before focusing so the
     target is visible even when the reader arrived in immersive mode. Section
     and paragraph focus belong to the current Draft mode and must not switch
     it back to Table. */
  var isBullet=/^C\\d+\\.P\\d+\\.B\\d+[a-z]*$/.test(id);
  if(isBullet)activateDraftMode('table',false);
  /* Bullet URLs keep the authored C.P.B address readable.  The DOM id uses a
     prefixed, CSS-safe form so it cannot collide with another record kind. */
  var domId=isBullet?'bullet-'+id.replace(/\\./g,'-'):id;
  var target=document.getElementById(domId);
  if(!target){{
    var points=document.querySelectorAll('[data-display-point]');
    for(var i=0;i<points.length;i++){{
      if(points[i].getAttribute('data-display-point')===id){{target=points[i];break;}}
    }}
  }}
  if(!target)return;
  var owner=target.parentElement;
  while(owner){{if(owner.tagName==='DETAILS')owner.open=true;owner=owner.parentElement;}}
  document.querySelectorAll('.record-focus').forEach(function(x){{
    x.classList.remove('record-focus');}});
  target.classList.add('record-focus');
  target.setAttribute('tabindex','-1');
  target.focus({{preventScroll:true}});
  target.scrollIntoView({{block:'center'}});
}}
/* Draft links open either the Evidence or Run Space in place. */
document.addEventListener('click',function(ev){{
  var a=ev.target.closest?ev.target.closest('a[data-outline-focus]'):null;
  if(!a||ev.button!==0||ev.metaKey||ev.ctrlKey||ev.shiftKey||ev.altKey)return;
  ev.preventDefault();
  requested=a.getAttribute('data-outline-lens')||'evidence';
  requestedSeg=a.getAttribute('data-outline-seg')||'';
  requestedFocus=a.getAttribute('data-outline-focus')||'';
  requestedRun=a.getAttribute('data-outline-run')||'';
  if(requested==='workspace')requested=(requestedSeg==='runs'||requestedRun)?'run':'evidence';
  if(requestedRun)requested='run';
  activateLens(requested);
  if(requestedFocus&&requested==='div')focusRecord(requestedFocus);
  try{{
    var u=new URL(location.href);
    u.searchParams.set('lens',requested);
    ['seg','focus','run'].forEach(function(k){{u.searchParams.delete(k);}});
    if(requestedSeg)u.searchParams.set('seg',requestedSeg);
    if(requestedFocus)u.searchParams.set('focus',requestedFocus);
    if(requestedRun)u.searchParams.set('run',requestedRun);
    history.replaceState(null,'',u.href);
  }}catch(e){{}}
}});
if(requested)activateLens(requested);
activateDraftMode(requestedDraftMode,false);
if(requestedFocus&&requested==='div')setTimeout(function(){{
  focusRecord(requestedFocus);}},0);
</script>
<script>{runs_js}</script>
<script>{space_js}</script>
</body></html>"""
