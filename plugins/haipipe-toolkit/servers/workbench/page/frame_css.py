"""The frame's stylesheet."""

from __future__ import annotations

from live.frame_runs import RUN_CSS


# ── the page ────────────────────────────────────────────────────────────────────────────────────
CSS = """
:root{--bg:#fff;--fg:#1c1c1c;--mut:#6f6f6b;--line:#e3e3e6;--acc:#3e5c84;--acc-soft:#e6edf5;--card:#fff;--ok:#24733d;--warn:#996b00;--miss:#c92a2a;--tab-line:#ced4da;--tab-on:#1864ab;--tab-wash:#e7f5ff;--wash:#f6f6f7;--grp-fixed-bg:#e9ecef;--grp-fixed-line:#868e96;--grp-sug-bg:#fff4e6;--grp-sug-line:#f08c00}
@media(prefers-color-scheme:dark){:root{--bg:#161719;--fg:#e8e8e6;--mut:#a0a09c;--line:#2c2e33;--acc:#8aa7cc;--acc-soft:#22304a;--card:#161719;--ok:#8bd49a;--warn:#e4bd62;--miss:#ff8787;--tab-line:#414852;--tab-on:#91caff;--tab-wash:#253749;--wash:#1d1f22;--grp-fixed-bg:#2b2f34;--grp-fixed-line:#868e96;--grp-sug-bg:#3b2a12;--grp-sug-line:#d9822b}}
*{box-sizing:border-box}body{margin:0;padding:16px;background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
main{max-width:1600px}h1{font-size:18px;margin:0 0 2px}
/* the level row is the page index, the title under it the page's own title, wide gaps (b03 s32-D13, JL 261008) */
nav.levels{margin:0;padding-bottom:12px;border-bottom:1px solid var(--line)}
/* a faint line between the Spaces row and the view row, as light as the one under the index (JL 261008) */
nav.subs{border-top:1px solid var(--line);padding-top:10px;margin-top:10px}
header.page-title h1{font-size:26px;margin:22px 0 18px;line-height:1.25}header.page-title .lv{color:var(--mut);font-weight:400}h2{font-size:16px;margin:0 0 6px}a{color:var(--acc)}.mut{color:var(--mut);font-size:13px}
.row{display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin:8px 0}
.tab{display:inline-block;padding:4px 12px;border:1px solid var(--line);border-radius:999px;color:var(--fg);text-decoration:none;font-size:14px;background:var(--card)}
.tab.on{border-color:var(--acc);color:var(--acc);font-weight:600}.tab.opt{border-style:dashed}
.levels select{font:inherit;font-size:14px;padding:3px 8px;border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--fg);field-sizing:content;max-width:min(56ch,100%);text-overflow:ellipsis}
.levels select.on{border-color:var(--acc);color:var(--acc);font-weight:600}
.levels select:disabled{opacity:.45;cursor:default}
/* top tabs: the Insight and Design board pages' buttons (b03 s32-element-ui, picked D · E, JL 261007):
   16px, 6px corners, a grey border, the open one washed blue; the third row keeps its own until picked */
.levels .tab,.spaces .tab,.levels select{font:400 16px system-ui,sans-serif;padding:6px 14px;border:1px solid var(--tab-line);
 border-radius:6px;background:var(--bg);color:var(--fg)}
.levels select{padding:6px 10px}
.levels .lvl{display:inline-flex}.levels .lvl .tab{border-radius:6px 0 0 6px}
.levels .lvl select{border-radius:0 6px 6px 0;border-left:0;padding:6px 10px;appearance:none;-webkit-appearance:none;cursor:pointer}
.levels .tab.on,.spaces .tab.on,.levels select.on{border-color:var(--tab-on);color:var(--tab-on);background:var(--tab-wash);font-weight:400}
.levels .tab:hover,.spaces .tab:hover{border-color:var(--tab-on)}
.spaces .tab.opt{border-style:solid}   /* an optional Space looks like any other (JL 261007) */
.bar{display:inline-block;width:1px;height:22px;background:var(--fg);margin:0 6px}
.page-view{display:block;width:100%;height:calc(100vh - 260px);min-height:560px;border:1px solid var(--line);border-radius:8px;background:var(--bg)}
/* the view row (third row): the Page workbench's view buttons (b03 s32-element-ui, picked E, JL 261007; not the
   small pills): 16px, 6px corners, padding 5px 12px, the open one washed blue */
.subs .tab,.studio-filters .tab{font:400 16px system-ui,sans-serif;padding:5px 12px;border:1px solid var(--tab-line);border-radius:6px;
 background:transparent;color:var(--fg)}
.subs .tab.on,.studio-filters .tab.on{border-color:var(--tab-on);color:var(--tab-on);background:var(--tab-wash);font-weight:400}
.subs .tab:hover,.studio-filters .tab:hover{border-color:var(--tab-on)}
.studio-filters{margin:0 0 12px;position:sticky;top:8px;z-index:2;padding:4px 0;background:var(--bg)}.studio-filters button{cursor:pointer}.tag-count{font-size:12px;opacity:.7;margin-left:4px}
.studio-filters .drop-ready{outline:2px dashed var(--tab-on);outline-offset:3px;background:var(--tab-wash)}
.studio-drag{cursor:grab;flex:none;user-select:none;touch-action:none;color:var(--mut);padding:0 4px}
.studio-drag:active{cursor:grabbing}.topic.dragging{opacity:.55}
.studio-drag-preview{position:fixed;z-index:9999;pointer-events:none;padding:8px 12px;border:1px solid var(--tab-on);border-radius:8px;background:var(--bg);color:var(--fg);box-shadow:0 3px 14px #0002;font:600 14px system-ui,sans-serif;max-width:340px}
.studio-current{font:400 12px system-ui,sans-serif;white-space:nowrap;border:1px solid var(--tab-line);border-radius:6px;padding:3px 7px;background:var(--bg);color:var(--fg);cursor:pointer}
.studio-current[aria-pressed=true]{color:var(--tab-on);border-color:var(--tab-on);background:var(--tab-wash)}
/* groups you make and delete (b10 s02-D16): × beside a group deletes it, + Group makes one, × on a topic's chip takes it out */
.studio-filters.row{gap:8px;padding-top:8px}
.studio-filters .bar{background:var(--line);height:20px;margin:0 2px}
/* the × is a small corner badge that shows only under the mouse (JL 261010), so the row keeps even gaps */
.grp{position:relative;display:inline-flex}
.grp-emoji{margin-right:6px;font-size:15px}
.grp>.tab{touch-action:none;user-select:none}.studio-filters.sorting,.studio-filters.sorting .tab{cursor:grabbing}
.grp.moving>.tab{opacity:.6;border-style:dashed;border-color:var(--tab-on)}.grp.moving .grp-x{display:none}
.studio-filters .grp-x{position:absolute;top:-7px;right:-7px;width:18px;height:18px;padding:0;border:1px solid var(--tab-line);
 border-radius:50%;background:var(--bg);color:var(--mut);font:400 12px/16px system-ui,sans-serif;text-align:center;
 opacity:0;pointer-events:none;transition:opacity .12s}
.grp:hover .grp-x,.grp:focus-within .grp-x{opacity:1;pointer-events:auto}
.studio-filters .grp-x:hover{background:var(--warn);border-color:var(--warn);color:#fff}
.studio-filters .tab.grp-fixed:not(.on),.grp-key.grp-fixed{background:var(--grp-fixed-bg);border-color:var(--grp-fixed-line)}
.studio-filters .tab.grp-suggested:not(.on),.grp-key.grp-suggested{background:var(--grp-sug-bg);border-color:var(--grp-sug-line)}
.grp-key{border:1px solid;border-radius:4px;padding:0 5px;color:var(--fg)}
.grp-new{font:400 14px system-ui,sans-serif;border:1px dashed var(--line);border-radius:6px;padding:6px 12px;background:transparent;color:var(--mut)}
.grp-new:hover{border-color:var(--tab-on);border-style:solid;color:var(--tab-on);background:var(--tab-wash)}
.grp-form{display:inline-flex;gap:6px;align-items:center}.grp-form[hidden],.grp-new[hidden]{display:none}
.grp-form input{font:400 15px system-ui,sans-serif;border:1px solid var(--tab-on);border-radius:6px;padding:5px 10px;width:160px;background:var(--bg);color:var(--fg);outline:none}
.grp-ok,.grp-cancel{font:400 13px system-ui,sans-serif;border:1px solid var(--tab-line);border-radius:6px;padding:4px 10px;background:var(--bg);color:var(--fg);cursor:pointer}
.grp-ok{border-color:var(--tab-on);color:var(--tab-on)}
.topic-tags .chip{position:relative}
.tag-x{position:absolute;top:-6px;right:-6px;width:14px;height:14px;padding:0;border:1px solid var(--line);border-radius:50%;
 background:var(--bg);color:var(--mut);font:400 10px/12px system-ui,sans-serif;text-align:center;cursor:pointer;
 opacity:0;pointer-events:none;transition:opacity .12s}
.chip:hover>.tag-x,.chip:focus-within>.tag-x{opacity:1;pointer-events:auto}
.tag-x:hover{background:var(--warn);border-color:var(--warn);color:#fff}
.studio-source{font-size:13px;color:var(--mut);display:flex;align-items:center;gap:8px;margin-bottom:8px}
.studio-source select{font:400 13px system-ui,sans-serif;border:1px solid var(--tab-line);border-radius:6px;padding:4px 8px;background:var(--bg);color:var(--fg)}
.studio-help,.studio-empty,.studio-status{font-size:13px;margin:8px 0 12px}.studio-status:empty{display:none}
.studio-topics .topic-pop{margin-left:auto}
.studio-topics .topic>summary{flex-wrap:nowrap;align-items:center;gap:10px}
.studio-topics .topic>summary>b{flex:0 1 auto;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.studio-topics .topic-tags{flex:0 1 auto;min-width:0;overflow:hidden;flex-wrap:nowrap}.studio-topics .topic-tags .chip{font-size:11px;white-space:nowrap}
.studio-topics .topic-pop,.studio-topics .topic>summary>.stage{flex:0 0 auto}
.studio-topics .studio-current{opacity:0;transition:opacity .15s}.studio-topics .topic:hover .studio-current,.studio-topics .studio-current:focus,.studio-topics .studio-current[aria-pressed=true]{opacity:1}
.studio-topics .topic>summary>.stage{font-size:0;gap:0;padding:5px 7px}
.topic[hidden]{display:none}.topic-tags{display:inline-flex;gap:6px;flex-wrap:wrap}.topic-tags .chip{font-size:12px;color:var(--mut);border-color:var(--line)}
.wf-table{border-collapse:collapse;width:100%;font-size:14px}.wf-table th,.wf-table td{text-align:left;padding:5px 8px;border-bottom:1px solid var(--line);vertical-align:top}
.wf-table th{font-weight:600;color:var(--mut);font-size:12.5px}
.topic{border:1px solid var(--line);border-radius:10px;background:var(--card);margin:0 0 8px;overflow:hidden}
.topic>summary{display:flex;flex-wrap:wrap;gap:8px 12px;align-items:baseline;cursor:pointer;padding:9px 14px;list-style:none}
.stage{--st:#868e96;--st-bg:#f1f3f5;display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:600;letter-spacing:.02em;padding:2px 10px 2px 8px;border:1px solid var(--st);border-radius:999px;white-space:nowrap;color:var(--st);background:var(--st-bg)}
.stage-explore{--st:#2b8a3e;--st-bg:#ebfbee}.stage-shaping{--st:#7048e8;--st-bg:#f3f0ff}.stage-agreed{--st:#1971c2;--st-bg:#e7f5ff}.stage-closed{--st:#495057;--st-bg:#f1f3f5}
@media(prefers-color-scheme:dark){.stage{--st-bg:transparent}.stage-explore{--st:#8ce99a}.stage-shaping{--st:#b197fc}.stage-agreed{--st:#74c0fc}.stage-closed{--st:#adb5bd}}
.stage-steps{display:inline-flex;gap:2px}.stage-steps b{width:7px;height:7px;border-radius:2px;border:1px solid var(--st);opacity:.55}.stage-steps b.on{background:var(--st);opacity:1}
.stage-none{color:var(--mut);border-style:dashed;font-weight:400}
.topic>summary::-webkit-details-marker{display:none}.topic>summary::before{content:"▸";color:var(--mut)}
.topic[open]>summary::before{content:"▾"}.topic[open]>summary{border-bottom:1px solid var(--line)}
.studio-related{border:1px solid var(--line);border-radius:10px;background:var(--card);margin:16px 0 8px;overflow:hidden}
.related-in .topic>summary{flex-wrap:nowrap}.related-in .topic>summary>.related-head{flex:1 1 auto;min-width:0}.related-in .topic>summary b{font-weight:600}.related-in .topic-pop{margin-left:auto;flex:0 0 auto;max-width:34%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.related-img{display:block;max-width:100%;border-top:1px solid var(--line)}
.studio-related>summary{display:flex;gap:10px;align-items:baseline;cursor:pointer;padding:9px 14px;list-style:none}
.studio-related>summary::-webkit-details-marker{display:none}.studio-related>summary::before{content:"▸";color:var(--mut)}
.studio-related[open]>summary::before{content:"▾"}.studio-related[open]>summary{border-bottom:1px solid var(--line)}
.studio-related>.related-in{padding:6px 14px 12px}.related-meta{color:var(--mut);font-size:13px}
/* a Delivery item's versions, newest first, one pane each (JL 261014) */
.dv-vers{margin:8px 12px 6px;gap:4px}.dv-vers .tab{font-size:13px;padding:2px 10px;cursor:pointer}.dv-vers .tab[aria-pressed=true]{border-color:var(--tab-on);color:var(--tab-on);background:var(--tab-wash)}.dv-files{margin:2px 12px 8px}
.tl-wrap{--tl-time:92px;--tl-dot:28px;--tl-cell:60px;--tl-gcell:100px}.tl-wrap [hidden]{display:none!important}
.tl-levels{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin:4px 0 14px}.tl-help{font-size:12px;color:var(--mut);margin-left:8px}
.tl-levels button{font:inherit;font-size:13px;border:1px solid var(--tab-line);border-radius:6px;padding:2px 10px;background:var(--bg);color:var(--fg);cursor:pointer}
.tl-levels button[aria-pressed=true]{border-color:var(--tab-on);color:var(--tab-on);background:var(--tab-wash)}
.tl-kd{display:inline-block;width:9px;height:9px;border-radius:2px;margin:0 6px 0 2px;flex:0 0 auto}.tl-legend-k .tl-kd{margin-left:10px}
.k-decided{background:var(--ok)}.k-session{background:var(--acc)}.k-drawing{background:var(--warn)}
.tl-wrap[data-level=days]:not(.picking) .tl-list,.tl-wrap[data-level=days] .tl-legend-k,.tl-wrap:not([data-level=days]) .tl-map,
.tl-wrap:not([data-level=days]) .tl-legend-b,.tl-wrap[data-level=topics] .tl-items{display:none}
.tl-map{position:relative;overflow-x:auto;padding:0 0 26px;--tl-head:28px}.tl-map[data-cols=topics]{--tl-head:var(--tl-slant,28px)}
.tl-map::before{content:"";position:absolute;left:calc(var(--tl-time) + var(--tl-dot) / 2 - 1px);top:calc(var(--tl-head) + 12px);bottom:9px;border-left:2px solid var(--fg)}
.tl-map::after{content:"";position:absolute;left:calc(var(--tl-time) + var(--tl-dot) / 2 - 6px);bottom:0;border:6px solid transparent;border-top:10px solid var(--fg);border-bottom:0}
.tl-mhead,.tl-mrow{display:flex;align-items:center;min-width:max-content}.tl-mhead{height:var(--tl-head)}
.tl-mhead>span:first-child,.tl-mrow>time{flex:0 0 var(--tl-time);text-align:right;font-size:13px;font-weight:600;white-space:nowrap}
.tl-mhead>span:nth-child(2),.tl-dot{flex:0 0 var(--tl-dot);display:flex;justify-content:center;position:relative;z-index:1}
.tl-dot::before{content:"";width:10px;height:10px;border-radius:50%;background:var(--fg);box-shadow:0 0 0 3px var(--card)}
.tl-col,.tl-cell{flex:0 0 var(--tl-cell);display:flex;align-items:center;justify-content:center;position:relative}
.tl-col{font-size:12px;color:var(--mut);text-decoration:none;align-self:stretch}.tl-col:hover{color:var(--tab-on)}
.tl-col>b{position:absolute;left:0;right:0;bottom:4px;text-align:center;font-size:14px;font-weight:700;color:var(--fg)}
.tl-col>span{position:absolute;left:50%;bottom:28px;transform-origin:0 100%;transform:rotate(-45deg);white-space:nowrap}
.tl-col:hover>b,.tl-col.on>b{color:var(--tab-on)}
.tl-mrow{height:38px;border-radius:8px}.tl-mrow:hover{background:var(--wash)}
.tl-cell{height:38px}.tl-cell::before{content:"";position:absolute;left:50%;top:0;bottom:0;border-left:1px solid var(--line)}
.tl-b{position:relative;display:block;width:var(--s);height:var(--s);border-radius:50%;background:var(--acc);opacity:.8;
 box-shadow:0 0 0 2px var(--card);transition:transform .12s,opacity .12s}.tl-b:hover{transform:scale(1.2);opacity:1}
.tl-bar,.tl-bar-h{flex:0 0 170px;margin-left:14px;display:flex;align-items:center;gap:8px}.tl-bar-h{font-size:11px;color:var(--mut);align-self:flex-end;padding-bottom:4px}
.tl-track{flex:0 0 120px;height:8px;border-radius:4px;background:var(--wash);overflow:hidden}.tl-track i{display:block;height:100%;background:var(--mut);opacity:.6}
.tl-bar b{font-size:12px;font-weight:600;color:var(--mut)}
.tl-axis{list-style:none;margin:0;padding:0 0 26px;position:relative}
.tl-axis::before{content:"";position:absolute;left:111px;top:6px;bottom:9px;border-left:2px solid var(--fg)}
.tl-axis::after{content:"";position:absolute;left:106px;bottom:0;border:6px solid transparent;border-top:10px solid var(--fg);border-bottom:0}
.tl-day{position:relative;display:grid;grid-template-columns:92px minmax(0,1fr);column-gap:40px;padding:0 0 14px}
.tl-day::after{content:"";position:absolute;left:107px;top:5px;width:10px;height:10px;border-radius:50%;background:var(--fg);box-shadow:0 0 0 3px var(--card)}
.tl-day>time{text-align:right;font-size:13px;font-weight:600;white-space:nowrap;line-height:20px}
.tl-topic{display:grid;grid-template-columns:minmax(160px,280px) minmax(0,1fr);column-gap:12px;align-items:center;line-height:20px;padding:1px 0}
.tl-name{font-size:13px;color:var(--fg);text-decoration:none;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tl-name b{font-weight:600;margin-right:6px}.tl-name span{color:var(--mut)}.tl-name:hover span{color:var(--tab-on)}
.tl-meter{display:flex;align-items:center;gap:8px}.tl-stack{display:flex;flex:0 0 auto;height:8px;border-radius:4px;overflow:hidden}.tl-n{font-size:12px;color:var(--mut)}
.tl-items{grid-column:1/-1;list-style:none;margin:3px 0 8px 3px;padding:0 0 0 12px;border-left:2px solid var(--line);display:grid;gap:2px}
.tl-items li{display:flex;align-items:center;font-size:12.5px;color:var(--mut);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tl-items li>span,.tl-items li>a{overflow:hidden;text-overflow:ellipsis}.tl-items li>a{margin-right:6px}.tl-items li b{color:var(--fg);font-weight:600;margin-right:6px}
.tl-mrow.tl-quiet,.tl-quiet .tl-cell,.tl-quiet .tl-gcell{height:20px}.tl-quiet>time{font-weight:400;font-size:12px;color:var(--mut)}
.tl-quiet .tl-bar,.tl-quiet .tl-b,.tl-quiet .tl-gb{visibility:hidden}
.tl-quiet .tl-dot::before,.tl-day.tl-quiet::after{width:6px;height:6px;border:2px solid var(--mut);background:var(--card)}
.tl-day.tl-quiet{padding-bottom:6px}.tl-day.tl-quiet>time{line-height:20px}
.tl-groups{display:flex;flex-wrap:wrap;gap:4px;align-items:center;margin:-6px 0 12px;font-size:12px;color:var(--mut)}
.tl-groups:empty{display:none}.tl-groups>span{margin-right:4px}
.tl-groups button{font:inherit;font-size:12px;border:1px solid var(--tab-line);border-radius:6px;padding:1px 8px;background:var(--bg);color:var(--fg);cursor:pointer}
.tl-groups button[aria-pressed=true]{border-color:var(--tab-on);color:var(--tab-on);background:var(--tab-wash)}.tl-groups button:hover{border-color:var(--tab-on)}
.tl-groups button i{font-style:normal;opacity:.7;margin-left:4px}
.fd-root{margin:2px 0 8px;font:12px ui-monospace,monospace;color:var(--mut)}
.fd-tree,.fd-tree ul{list-style:none;margin:0;padding:0}.fd-tree ul{margin-left:11px;padding-left:12px;border-left:1px solid var(--line)}
.fd-row{display:flex;align-items:baseline;gap:10px;min-width:0;padding:2px 6px;border-radius:5px;font-size:13.5px;line-height:21px}
.fd-row:hover{background:var(--wash)}.studio-folder summary.fd-row{cursor:pointer;list-style:none}
.studio-folder summary.fd-row::-webkit-details-marker{display:none}
.fd-dir>details>summary .fd-name::before{content:"📁 "}.fd-dir>details[open]>summary .fd-name::before{content:"📂 "}
.fd-name{font-weight:600;white-space:nowrap}.fd-i{flex:0 0 auto;margin-right:-4px}
.fd-file a{color:var(--fg);text-decoration:none;white-space:nowrap}.fd-file a:hover{color:var(--tab-on);text-decoration:underline}
.fd-n,.fd-when{flex:0 0 auto;font-size:12px;color:var(--mut)}
.fd-more button{font:inherit;font-size:12px;margin:4px 6px;border:1px solid var(--tab-line);border-radius:6px;padding:1px 9px;background:var(--bg);color:var(--fg);cursor:pointer}
.fd-word{font-size:12.5px;color:var(--mut);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
.tl-map[data-cols=groups] .tl-col,.tl-map[data-cols=groups] .tl-cell,.tl-map[data-cols=topics] .tl-gcol,.tl-map[data-cols=topics] .tl-gcell{display:none}
.tl-gcol,.tl-gcell{flex:0 0 var(--tl-gcell);position:relative}.tl-gcell{height:38px;display:flex;align-items:center;justify-content:center}
.tl-gcell::before{content:"";position:absolute;left:50%;top:0;bottom:0;border-left:1px solid var(--line)}
.tl-gcol{font:inherit;font-size:11px;color:var(--mut);background:none;border:0;cursor:pointer;align-self:flex-end;padding:0 4px 4px;
 white-space:nowrap;overflow:hidden;text-overflow:ellipsis;text-align:center}.tl-gcol:hover{color:var(--tab-on)}
.tl-gb{position:relative;display:block;width:var(--s);height:var(--s);border-radius:50%;background:var(--acc);opacity:.8;border:0;padding:0;
 cursor:pointer;box-shadow:0 0 0 2px var(--card);transition:transform .12s,opacity .12s}.tl-gb:hover{transform:scale(1.2);opacity:1}
.tl-cols{display:inline-flex;gap:4px;align-items:center;font-size:12px;color:var(--mut);margin-left:8px}
.tl-levels .tl-cols button{font-size:12px;padding:1px 8px}
.tl-wrap[data-level=days].picking .tl-off,.tl-wrap:not(.picking) .tl-picked,.tl-wrap:not([data-level=days]) .tl-picked{display:none}
.tl-col{cursor:pointer}.tl-col.on{color:var(--tab-on);font-weight:700}.tl-cell.on .tl-b{background:var(--tab-on);opacity:1}
.tl-wrap.picking .tl-cell:not(.on) .tl-b{opacity:.3}
.tl-picked{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:2px 0 12px;font-size:13px}
.tl-picked button{font:inherit;font-size:12px;border:1px solid var(--tab-line);border-radius:6px;padding:1px 8px;background:var(--bg);color:var(--fg);cursor:pointer}
@media(max-width:700px){.tl-wrap{--tl-time:62px}.tl-day{grid-template-columns:62px minmax(0,1fr);column-gap:30px}
 .tl-axis::before{left:76px}.tl-axis::after{left:71px}.tl-day::after{left:72px}.tl-topic{grid-template-columns:minmax(0,1fr) 120px}}
.topic-meta{color:var(--mut);font-size:13px;flex:1}.topic-pop a{text-decoration:none;font-size:15px}
.topic .none{margin:10px 14px}.topic-pop{display:flex;gap:10px;align-items:baseline;font-size:13px}
.chip{display:inline-block;padding:0 8px;margin-right:4px;border:1px solid var(--acc);border-radius:999px;color:var(--acc);font-size:12px;text-decoration:none}
.st-bar{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;padding:8px 14px}
.st-map{overflow-x:auto;padding:10px 14px 16px;border-top:1px solid var(--line)}
.st-side{display:inline-flex;border:1px solid var(--line);border-radius:6px;overflow:hidden}.st-side button{font:500 12.5px -apple-system,sans-serif;border:0;padding:1px 9px;cursor:pointer;background:var(--bg);color:var(--mut)}.st-side button+button{border-left:1px solid var(--line)}.st-side button[aria-pressed=true]{background:var(--tab-wash,var(--line));color:var(--tab-on,var(--fg))}.st-side button:disabled{cursor:default;opacity:.45}.draw-edit[hidden],.side-link[hidden]{display:none}
.draw-edit{font:500 12.5px -apple-system,sans-serif;border:1px solid var(--line);border-radius:6px;padding:1px 9px;cursor:pointer;background:var(--bg);color:var(--fg)}
.studio-parts{margin:10px 14px 16px}.studio-parts>details.topic{margin:0 0 8px}.studio-transcripts{margin:16px 14px}.studio-transcripts>h3{font-size:17px;margin:0 0 12px}.studio-transcript-note,.studio-transcript-links{margin:12px 14px;font-size:14px;line-height:1.5}.studio-transcript-note{color:var(--mut)}
.st-frame{display:block;width:100%;height:calc(100vh - 240px);min-height:520px;border:0;border-top:1px solid var(--line);background:#fff}
.add{margin:6px 2px 0}
.st-ok{color:var(--ok)}.st-warn{color:var(--warn)}
.dl-frame{display:block;width:100%;height:560px;border:0;border-top:1px solid var(--line);background:#fff}
.dl-note{padding:0 14px 10px;margin:0}.dl-src{max-height:420px;overflow:auto;margin:0 14px 12px}
.topic.missing{border:1px dashed var(--miss);background:transparent}.topic.missing>summary b{color:var(--mut)}
.q-row{display:grid;grid-template-columns:1.1fr 1fr 1.3fr;border:1px solid var(--line);border-radius:10px;margin:0 0 8px;background:var(--card)}
.q-row.q-two{grid-template-columns:1fr 1.7fr}.q-work{font-size:13.5px;margin:6px 0 8px}
.q-row>div{padding:10px 12px;min-width:0}.q-row>div+div{border-left:1px solid var(--line)}
.q-head-row{border:0;background:transparent;margin:0;color:var(--mut);font-size:12.5px}.q-head-row>div{padding:2px 12px}.q-head-row>div+div{border-left:0}
/* level rows as the old Insight board drew them (b11, JL 261008): flush grey rows split by thin lines, a ▶
   marker, a small link on the right; the q-rows inside flush, like one table. A theme opts in by the classes. */
.dikw{border-top:1px solid var(--line);margin:4px 0 12px}
.dikw>.topic{border:0;border-bottom:1px solid var(--line);border-radius:0;margin:0;background:var(--wash)}
.dikw>.topic>summary{padding:8px 12px}.dikw>.topic>summary::before{content:"▶";color:var(--fg);font-size:11px}
.dikw>.topic[open]>summary::before{content:"▼"}.dikw .topic-meta{flex:1;font-size:13px}.dikw .lv-link{font-size:12.5px}
/* a report read as one document (insight's Overall Report, JL 261012): one column at a reader's measure */
.report-doc{max-width:1180px;margin:4px 0 24px;font-size:15.5px;line-height:1.6}.report-doc>:not(.rep-glance){max-width:820px}.report-doc h2{font-size:24px;margin:2px 0 4px}
.report-doc>p.mut{margin:0 0 4px}.report-doc .rep-glance-head{margin:14px 0 6px;font-weight:700;font-size:17px}
.report-doc .rep-glance{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin:0 0 20px}@media(max-width:1000px){.report-doc .rep-glance{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:600px){.report-doc .rep-glance{grid-template-columns:1fr}}
.rep-glance a{display:block;border:1px solid var(--line);border-radius:8px;padding:8px 10px;color:inherit;text-decoration:none;background:var(--card)}
.rep-glance a:hover{border-color:var(--acc)}.rep-glance span{display:block;font-size:12.5px;color:var(--mut)}
.rep-glance b{display:block;font-size:14px;line-height:1.35;margin:2px 0 6px}.rep-glance img{display:block;width:100%;background:#fff;border-radius:4px}
.report-doc .rep-fig{margin:12px 0 14px;max-width:720px}.report-doc .rep-fig figcaption{font-weight:700;font-size:16px;margin:0 0 6px}
.report-doc .rep-fig img{display:block;width:100%;border:1px solid var(--line);border-radius:8px;background:#fff}.report-doc .rep-fig p{margin:4px 0 0;font-size:13px}
.report-doc section{border-top:1px solid var(--line);padding:16px 0 4px}.report-doc section h3{font-size:19px;margin:0 0 2px}
.report-doc .rep-ask{color:var(--mut);font-style:italic;margin:0 0 10px}.report-doc .rep-lead{font-weight:600;margin:0 0 4px}
.report-doc ol,.report-doc ul{padding-left:24px}.report-doc li{margin:0 0 7px}.report-doc h4{font-size:15.5px;margin:12px 0 4px}
.report-doc details{margin:4px 0 8px}.report-doc details>summary{cursor:pointer;color:var(--acc);font-size:14px}
.q-table{padding:8px 0 12px;background:var(--bg)}.q-table>p.mut{margin:0 12px 6px;font-size:13px}
.q-table>.q-row{border-radius:0;margin:0;border-bottom-width:0}.q-table>.q-row:last-child{border-bottom-width:1px}
.q-head{margin:0}.kind{color:var(--mut);font-size:12.5px;font-weight:600}
.q-top{display:flex;align-items:center;gap:6px}
.q-label{display:inline-block;border:1px solid var(--tab-on);color:var(--tab-on);border-radius:999px;padding:0 8px;font:600 11.5px/1.6 system-ui,sans-serif}
.q-dot{display:inline-block;width:12px;height:12px;border-radius:50%;border:1px solid var(--tab-line);background:var(--bg)}
.q-dot.partial{background:#fcc419;border-color:#f59f00}.q-dot.answered{background:#40c057;border-color:#2f9e44}
.q-slug{margin:6px 0 2px!important;font-weight:700}.q-text{margin:0 0 4px!important}
.q-more summary{cursor:pointer;color:var(--acc);font-size:13px;list-style:none}.q-more summary::-webkit-details-marker{display:none}
.q-more p{font-size:13px}.q-row p{margin:0 0 4px}
.q-group{margin:22px 0 6px;font-size:16px}.from{margin:8px 0 0!important;font-size:12px;color:var(--mut)}.from-list{margin:2px 0 0;padding-left:16px;font-size:13px}
.q-w{font-size:13.5px}.rp-title{font-weight:600}.rp-title a{color:inherit}.rp-text{font-size:14px}
.rp-thumb{display:block;margin:6px 0}.rp-thumb img{display:block;width:100%;max-height:200px;object-fit:contain;object-position:left top;border:1px dashed var(--line);border-radius:6px;background:#fff}
.rp-live{cursor:zoom-in;margin:6px 0 2px}.rp-live.on{cursor:auto}
.rp-draw{display:block;width:100%;height:300px;border:1px dashed var(--line);border-radius:6px;background:#fff}
.rp-full{font-size:12.5px;margin:0 0 4px!important}
.rp-tags{color:var(--mut);font-size:12.5px}
#frame-pop{width:min(1300px,95vw);height:90vh;max-width:95vw;max-height:90vh;padding:0;border:0;border-radius:12px;background:var(--bg);color:var(--fg);overflow:hidden}
#frame-pop::backdrop{background:rgba(0,0,0,.35)}#frame-pop[open]{display:flex;flex-direction:column}
.pop-bar{display:flex;align-items:center;gap:12px;padding:8px 14px;border-bottom:1px solid var(--line)}
.pop-title{font-weight:650;flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.pop-x{border:0;background:transparent;font-size:20px;cursor:pointer;color:var(--fg)}.pop-frame{flex:1;border:0;width:100%;background:#fff}
@media(max-width:600px){body{padding:12px}.row{flex-wrap:nowrap;overflow-x:auto}.q-row,.q-row.q-two{grid-template-columns:1fr}.q-row>div+div{border-left:0;border-top:1px solid var(--line)}.q-head-row{display:none}}
"""
CSS += RUN_CSS                                  # the Runs cards, shared with SPACE Home (JL 261019)
