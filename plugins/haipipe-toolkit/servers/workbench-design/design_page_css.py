"""The Design page's stylesheet.

Split out of design_page.py; design_page.py re-exports every name here."""


# ------------------------------------------------------------------ render --

_CSS = """
:root{--fg:#1c1c1c;--mut:#6f6f6b;--line:#e4e4e7;--bg:#fff;--acc:#3e5c84;--bad:#b3541e;--ok:#3a7d44;--soft:#f5f6f8;--acc-soft:#e6edf5}
@media(prefers-color-scheme:dark){:root{--fg:#e8e8e6;--mut:#9a9a97;--line:#2c2e33;--bg:#161719;--acc:#7d9cc4;--bad:#e0955a;--ok:#7dbb87;--soft:#20242a;--acc-soft:#22304a}}
*{box-sizing:border-box}body{margin:0;padding:16px 18px;background:var(--bg);color:var(--fg);font:14px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:1100px}
h1{font-size:18px;margin:0 0 2px;font-weight:700}h2{font-size:14px;margin:18px 0 6px;font-weight:650}
.mut{color:var(--mut);font-size:12.5px}.bad{color:var(--bad)}.ok{color:var(--ok)}
/* the header's band of facts, one line, as every workbench draws it */
.dataset{margin:10px 0 4px;padding:8px 14px;border:1px solid var(--acc);border-radius:10px;background:var(--acc-soft);color:var(--acc);font-size:14px}
/* a View tab, the same look as a Space tab */
.views{display:flex;gap:6px;flex-wrap:wrap;padding:0 0 10px;margin:0 0 12px;border-bottom:1px solid var(--line)}
.views button{font:400 16px system-ui,sans-serif;padding:6px 14px;border:1px solid #ced4da;border-radius:6px;background:#fff;color:#1e1e1e;cursor:pointer}
.views button.on{background:#e7f5ff;color:#1864ab;border-color:#1864ab}.view{display:none}.view.on{display:block}
@media(prefers-color-scheme:dark){.views button{background:#191c21;color:#edf0f4;border-color:#414852}
.views button.on{background:#253749;color:#91caff;border-color:#91caff}}
/* one tab style for every workbench, the Guide's: a Space tab is a filled pill when on */
.tabs{display:flex;gap:6px;margin:12px 0 8px;flex-wrap:wrap}
.tabs button{font:400 16px system-ui,sans-serif;padding:6px 14px;border:1px solid #ced4da;border-radius:6px;cursor:pointer;background:#fff;color:#1e1e1e}
.tabs button.on{background:#e7f5ff;color:#1864ab;border-color:#1864ab}
@media(prefers-color-scheme:dark){.tabs button{background:#191c21;color:#edf0f4;border-color:#414852}
.tabs button.on{background:#253749;color:#91caff;border-color:#91caff}}
.pane{display:none}.pane.on{display:block}
table{border-collapse:collapse;width:100%;margin:4px 0 8px}td,th{padding:6px 8px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
th{color:var(--mut);font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.03em}
code{font:12px ui-monospace,Menlo,monospace;word-break:break-word}a{color:var(--acc);text-decoration:none}a:hover{text-decoration:underline}
details{margin:2px 0}summary{cursor:pointer;color:var(--acc);font-size:12.5px}
ul.rules{margin:2px 0 0 16px;padding:0}ul.rules li{margin:1px 0}
.item{border-top:2px solid var(--line);padding:12px 0 14px;margin:0}.item.sel{background:var(--soft);margin:0 -10px;padding:12px 10px 14px}
.item .head{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;align-items:baseline}
.item .head b{font-size:15px}
pre.text{margin:8px 0;padding:10px 12px;background:var(--soft);border-left:3px solid var(--acc);font:15px/1.45 -apple-system,sans-serif;white-space:pre-wrap;word-break:break-word}
table.kv{margin:6px 0}table.kv th{width:88px;text-transform:none;letter-spacing:0;font-size:12px;color:var(--mut);border-bottom:0;padding:3px 8px 3px 0}
table.kv td{border-bottom:0;padding:3px 0}
.card{border:1px solid var(--line);border-radius:6px;padding:10px 12px;margin:8px 0}
.card .head{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
.act{margin-top:8px;display:flex;gap:6px;flex-wrap:wrap;align-items:center}
table.designs td.who{width:230px}.design{white-space:pre-wrap;word-break:break-word;font-size:14.5px}
details.decide{margin-top:8px}details.decide .act{margin-top:6px}
.act input,.act textarea,.form input,.form textarea,.form select{font:13px -apple-system,sans-serif;border:1px solid var(--line);border-radius:4px;padding:4px 6px;background:var(--bg);color:var(--fg)}
.act input.name{width:90px}.act input.words{width:min(420px,100%)}
button.do{font:600 12.5px -apple-system,sans-serif;border:1px solid var(--acc);border-radius:4px;padding:4px 10px;background:var(--bg);color:var(--acc);cursor:pointer}
button.do:hover{background:var(--soft)}button.do.bad{border-color:var(--bad);color:var(--bad)}
.msg{font-size:12.5px;margin-top:4px}.msg.bad{color:var(--bad)}.msg.ok{color:var(--ok)}
.form{display:grid;grid-template-columns:110px 1fr;gap:6px 10px;max-width:760px;margin:6px 0}
.form label{color:var(--mut);font-size:12px;padding-top:5px}
.form textarea{min-height:56px}.form .full{grid-column:1/3}
.empty{color:var(--mut);padding:10px 0}
.pair{display:flex;gap:22px;align-items:flex-start}.pair .pic{flex:0 0 260px;min-width:0}.pair .facts{flex:1;min-width:0}
.pair.text .pic{flex:0 0 min(300px,38%)}.pair.text pre.text{margin-top:4px}.pair .facts table.kv{margin-top:0}
.phone{border:1px solid var(--line);border-radius:18px;padding:12px 12px 16px;margin:8px 0 4px;background:var(--bg);max-width:280px}
.phone .from{font-size:11px;color:var(--mut);text-align:center;margin-bottom:10px}
.bubble{background:var(--soft);border-radius:16px 16px 16px 4px;padding:8px 11px;font:14.5px/1.42 -apple-system,sans-serif;white-space:pre-wrap;word-break:break-word}
.bubble .link{color:var(--acc);text-decoration:underline}
.item{padding:0}.item.sel{margin:0;padding:0;background:none}
.item.sel>details>summary{box-shadow:inset 3px 0 0 var(--acc)}
.foldbar{margin:6px 0 2px;text-align:right}
details.itemfold.cardrow>summary{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;height:auto;min-height:34px;align-items:center;padding:9px 4px;font-size:13px}
details.itemfold.cardrow>summary::before{display:none}details.itemfold.cardrow>summary>span{min-width:0;display:flex;flex-direction:column;gap:2px;overflow:hidden}
details.itemfold.cardrow>summary .c1 b{max-width:none;white-space:normal}
details.itemfold.cardrow>summary .c1 .line>b:first-child::before{content:"▸ ";color:var(--mut)}
details.itemfold.cardrow[open]>summary .c1 .line>b:first-child::before{content:"▾ "}
details.itemfold.cardrow .peek{white-space:normal;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}
details.itemfold.cardrow .move{display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
details.itemfold.cardrow .sup,details.itemfold.cardrow .wrong{font-size:12.5px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.cardgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;padding:6px 4px 14px;align-items:start}
.cardgrid>.col{min-width:0}
h4.colh{margin:12px 0 4px;font:650 11px -apple-system,sans-serif;letter-spacing:.05em;text-transform:uppercase;color:var(--mut)}
.cardgrid>.col>h4.colh:first-child{margin-top:2px}
details.sub{border:1px solid var(--line);border-radius:8px;margin:8px 0;padding:6px 10px}
details.sub>summary{font-size:13px;color:var(--fg);font-weight:600}
details.sub[open]>summary{margin-bottom:6px}ul.notes{margin:0;padding-left:18px;font-size:13px;line-height:1.5}ul.notes li{margin:3px 0}
/* three columns left to right at every width; a narrow screen only tightens the gaps */
@media(max-width:860px){.cardgrid{gap:8px}.cardgrid>.col.pic{position:static}.cardgrid>.col{overflow-wrap:anywhere}}
details.runsfold{margin:6px 0 8px}details.runsfold>summary{font-size:12px;color:var(--mut);font-weight:400}
details.runsfold[open]>summary{margin-bottom:4px}
details.itemfold.cardrow .line{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
ul.runs{list-style:none;margin:0;padding:0}ul.runs li{padding:6px 0;border-bottom:1px dashed var(--line)}
ul.runs li:last-child{border-bottom:0}
ul.runs .rl{display:flex;gap:10px;flex-wrap:wrap;align-items:baseline;font-size:13px}ul.runs .rid{font-size:11px;color:var(--mut)}
ul.runs .said{font-size:12.5px;color:var(--mut);font-style:italic;margin:2px 0}ul.runs li.old{opacity:.6}
.chain{margin:2px 0 8px}.chain .node,.node.limit{padding:3px 0}.chain .step{font-size:11px;color:var(--mut);margin:1px 0 1px 4px}
.node .rid{font:650 12px ui-monospace,Menlo,monospace;margin-right:6px}.node .says{font-size:13px;line-height:1.45}
.node .pg{font-size:12px;color:var(--mut);margin-left:0}.also{font-size:12px;color:var(--mut);margin:2px 0 4px;line-height:1.45}
.cardgrid table.elems{display:table;table-layout:fixed;overflow:visible;width:100%;border-collapse:collapse;font-size:13px;margin:2px 0 6px}
table.elems th{text-align:left;font-size:11px;color:var(--mut);font-weight:600;border-bottom:1px solid var(--line);padding:3px 4px}
table.elems td{vertical-align:top;padding:4px;border-bottom:1px dashed var(--line);line-height:1.4;overflow-wrap:anywhere}
table.elems th:last-child,table.elems td.elsup{width:34%}
table.elems .ids{display:block;font-size:11.5px;color:var(--mut)}.el-new{color:var(--bad);font-weight:600}s.el-gone{color:var(--mut)}
.elmatrix{margin:8px 0 12px}.elmatrix>summary{font-weight:600;color:var(--fg)}
.elscroll{overflow-x:auto}table.elmat{border-collapse:collapse;font-size:12.5px;margin:6px 0;width:100%}
table.elmat th,table.elmat td{border-bottom:1px solid var(--line);padding:4px 6px;text-align:left;vertical-align:top}
table.elmat th{font-size:11px;color:var(--mut);font-weight:600;white-space:nowrap}
table.elmat td.el-same{color:var(--mut);text-align:center}table.elmat td.el-changed{color:var(--bad);font-weight:600}
table.elmat td.el-removed{color:var(--mut)}table.elmat td.el-missing{color:var(--mut);text-align:center}
table.elmat tr.elcount td{color:var(--mut);font-size:11.5px}
.el-from{font-weight:600}.el-from.requirements{color:var(--acc)}
.el-from.internal{color:var(--ok)}.el-from.external{color:#7048e8}
.el-from.intuition{color:var(--bad)}.el-how{color:var(--mut)}
.task .tl{display:flex;gap:10px;margin:2px 0}.task .tl>.mut{flex:0 0 130px}
span.link{font:600 12px ui-monospace,Menlo,monospace;color:var(--acc);background:color-mix(in srgb,var(--acc) 10%,transparent);border-radius:4px;padding:0 3px}
.cardhead{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;padding:4px;color:var(--mut);font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.03em;border-bottom:1px solid var(--line)}
.task{border:1px solid var(--acc);border-radius:8px;background:var(--soft);padding:10px 14px;margin:6px 0 12px;line-height:1.55}
.taskhead{font-weight:650;color:var(--acc);font-size:15px}
details.inner{margin:8px 0 0}
@media(max-width:860px){details.itemfold.cardrow>summary,.cardhead{gap:8px}details.itemfold.cardrow>summary>span{overflow-wrap:anywhere}}
details.itemfold>summary{list-style:none;display:flex;gap:12px;align-items:center;height:46px;cursor:pointer;color:var(--fg);font-size:14px;overflow:hidden}
details.itemfold>summary::-webkit-details-marker{display:none}details.itemfold>summary::before{content:"▸";color:var(--mut);flex:0 0 10px}
details.itemfold[open]>summary::before{content:"▾"}details.itemfold>summary:hover{background:var(--soft)}
details.itemfold>summary b{flex:0 1 auto;max-width:42%;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.peek{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;color:var(--mut);font-size:13px}
.st{flex:0 0 auto;white-space:nowrap}
table.grid{width:100%;border:1px solid var(--line);border-radius:9px;border-collapse:separate;border-spacing:0;overflow:hidden;margin:4px 0 12px}
table.grid th{background:var(--soft);padding:7px 10px;border-bottom:1px solid var(--line);border-right:1px solid var(--line)}
table.grid td{padding:7px 10px;border-bottom:1px solid var(--line);border-right:1px solid var(--line);vertical-align:top}
table.grid th:last-child,table.grid td:last-child{border-right:0}table.grid tr:last-child td{border-bottom:0}
table.input td.key{width:170px;font-weight:600}table.input td.src{width:170px;font-size:12px;color:var(--mut)}
h3{font-size:13px;margin:18px 0 2px;font-weight:650}
.itembody{height:560px;overflow:auto;padding:2px 8px 14px 0;border-top:1px dashed var(--line)}
.itembody .pair .pic{position:sticky;top:6px;max-height:540px;overflow:auto}
table.explain{border:1px solid var(--line);border-radius:10px;border-collapse:separate;border-spacing:0;overflow:hidden;margin:6px 0 0}
table.explain th{width:160px;background:var(--soft);font-size:11px;font-weight:650;letter-spacing:.05em;text-transform:uppercase;color:var(--mut);padding:12px 14px;border-bottom:1px solid var(--line);border-right:1px solid var(--line);vertical-align:top}
table.explain td{padding:10px 14px;border-bottom:1px solid var(--line);vertical-align:top;line-height:1.5}
table.explain tr:last-child th,table.explain tr:last-child td{border-bottom:0}
table.explain td>.mut:first-child{margin-bottom:4px}@media(max-width:720px){table.explain th{width:110px;padding:10px}}
.explain p.goal{margin:0 0 2px;font-size:14.5px;line-height:1.5}
ol.flow{list-style:none;margin:0;padding:0}ol.flow li.lv{display:flex;gap:10px;align-items:baseline}
ol.flow .lvname{flex:0 0 96px;font-size:11.5px;color:var(--mut)}
ol.flow .nodes{flex:1;min-width:0}ol.flow .node{display:block;margin:1px 0;line-height:1.4}
ol.flow li.down{padding-left:118px;color:var(--mut);font-size:12px;line-height:1.2}ol.flow li.me .lvname{color:var(--acc);font-weight:600}
.betl{display:flex;gap:10px;margin:2px 0;line-height:1.45}.betl .k{flex:0 0 64px;font-size:12px;font-weight:600}
ul.checks{list-style:none;margin:0;padding:0}ul.checks li{margin:2px 0;padding-left:20px;text-indent:-20px;line-height:1.4}
ul.checks .g{display:inline-block;width:20px;text-indent:0;font-weight:700}
@media(max-width:720px){.pair{display:block}.itembody .pair .pic{position:static;max-height:none}
main table:not(.explain){display:block;max-width:100%;overflow-x:auto}
main table:not(.explain) code{white-space:nowrap;word-break:normal}
.peek{display:none}
details.itemfold>summary b{max-width:none;flex:1 1 auto}}
img.shot{display:block;width:250px;max-width:100%;height:auto;margin:8px 0 4px;border:1px solid var(--line);border-radius:18px;background:#fff}
pre.src{margin:6px 0;padding:8px 10px;background:var(--soft);font:11.5px/1.4 ui-monospace,Menlo,monospace;white-space:pre-wrap;word-break:break-word;max-height:360px;overflow:auto}
.gallery{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:20px 18px;margin:10px 0}
details.retired{margin-top:18px}.gallery figure{margin:0}.gallery img.shot{width:100%;margin:0 0 6px}
.gallery figcaption{font-size:13px;line-height:1.35}
@media(max-width:640px){body{padding:12px}td,th{padding:5px 6px}.form{grid-template-columns:1fr}.form .full{grid-column:1}}
"""
