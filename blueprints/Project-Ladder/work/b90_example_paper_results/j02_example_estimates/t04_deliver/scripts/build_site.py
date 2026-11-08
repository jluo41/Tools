"""Placeholder worker: a small static explorer page over the main Task's values, for the work theme's example Block.

Reads the main Task's returned values.csv (t01_example_main, Run r01_example_main) and writes into RESULT_DIR (set by
the Run's ticket) index.html, one self-contained page (no network, no outside script) whose box filters the table, and
headline.txt. Every number is made up. The page carries no build time, so the same values build the same page.
"""
from __future__ import annotations

import csv
import html
import json
import os
from pathlib import Path

VALUES = Path("t01_example_main/runs/r01_example_main/result/values.csv")   # from the Job folder

PAGE = """<!doctype html>
<html lang=en><head><meta charset=utf-8><meta name=viewport content="width=device-width, initial-scale=1">
<title>Example estimates explorer</title>
<style>
:root{--bg:#ffffff;--fg:#1e1e1e;--mut:#5c636a;--line:#ced4da;--wash:#f1f3f5;--acc:#1864ab}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#16181b;--fg:#e9ecef;--mut:#a5abb1;--line:#3a3f45;--wash:#23272b;--acc:#74c0fc}}
:root[data-theme="dark"]{--bg:#16181b;--fg:#e9ecef;--mut:#a5abb1;--line:#3a3f45;--wash:#23272b;--acc:#74c0fc}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:760px;margin:0 auto;padding:20px 16px 40px}
h1{font-size:20px;margin:0 0 4px}.mut{color:var(--mut)}
.lead{border:1px solid var(--line);border-radius:8px;padding:12px 14px;margin:14px 0;background:var(--wash)}
.lead b{font-size:22px;color:var(--acc)}
input{width:100%;box-sizing:border-box;padding:8px 10px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg);font:inherit}
table{width:100%;border-collapse:collapse;margin-top:10px;font-size:14px}
th,td{text-align:left;padding:6px 8px;border-bottom:1px solid var(--line);vertical-align:top}
th{background:var(--wash);font-weight:600}td.num{font-variant-numeric:tabular-nums;white-space:nowrap}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:13px}
</style></head><body><main>
<h1>Example estimates explorer</h1>
<p class=mut>Placeholder: every number here is made up. Read from the main Task's values.csv (__N__ values).</p>
<div class=lead>The main association is <b>__LEAD__</b> points.</div>
<label for=q class=mut>Find a value by its key, unit or text</label>
<input id=q type=search placeholder="main, sample, points..." autocomplete=off>
<table><thead><tr><th>Key</th><th>Value</th><th>Unit</th><th>As printed</th></tr></thead><tbody id=rows></tbody></table>
<p id=none class=mut hidden>No value matches.</p>
</main><script>
var ROWS = __ROWS__;
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;","\\"":"&quot;"}[c]})}
function draw(){var q=document.getElementById("q").value.trim().toLowerCase(),out=[];
ROWS.forEach(function(r){var t=(r.key+" "+r.unit+" "+r.text).toLowerCase();if(!q||t.indexOf(q)>=0)out.push(
"<tr><td><code>"+esc(r.key)+"</code></td><td class=num>"+esc(r.value)+"</td><td>"+esc(r.unit)+"</td><td>"+esc(r.text)+"</td></tr>")});
document.getElementById("rows").innerHTML=out.join("");document.getElementById("none").hidden=out.length>0}
document.getElementById("q").addEventListener("input",draw);draw();
</script></body></html>
"""


def main() -> None:
    res = Path(os.environ["RESULT_DIR"])
    job = Path(__file__).resolve().parents[2]
    with (job / VALUES).open(encoding="utf-8") as f:
        rows = [{k: r[k] for k in ("key", "value", "unit", "text")} for r in csv.DictReader(f)]
    lead = next(r for r in rows if r["key"] == "main.b")
    page = (PAGE.replace("__N__", str(len(rows)))
                .replace("__LEAD__", html.escape(lead["text"] or lead["value"]))
                .replace("__ROWS__", json.dumps(rows, ensure_ascii=False).replace("</", "<\\/")))
    (res / "index.html").write_text(page, encoding="utf-8")
    (res / "headline.txt").write_text(f"an explorer page over {len(rows)} values; it leads with the main association\n",
                                      encoding="utf-8")


if __name__ == "__main__":
    main()
