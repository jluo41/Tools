#!/usr/bin/env python3
"""Turn a skill report (.md) into an HTML page with sortable, filterable tables.

    python3 diagnostics/md_to_html.py reports/skill_report_baseline.md
    python3 diagnostics/md_to_html.py reports/skill_report_baseline.md --fragment

The full page is a standalone .html next to the .md. --fragment writes
<name>.fragment.html: no <html>/<head>/<body> wrapper, only the style, the
content and the script, for a host that supplies the document skeleton
(an Artifact publish wraps the page itself).

Covers the Markdown the report uses: headings, paragraphs, blockquotes, lists,
fenced code, tables, **bold**, `code` and [links](url). Every table gets a filter
box (matches any cell) and click-to-sort headers (numbers sort as numbers).
"""

import argparse
import html
import re
from pathlib import Path

STYLE = """
:root{--bg:#fbfbfa;--fg:#1d1d1f;--muted:#6b6b70;--line:#e3e3e0;--head:#f1f1ee;
--accent:#b4441c;--hl:#fff4e5;--hl-line:#f0b46a;--code:#f3f2ef}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#17171a;--fg:#ececee;
--muted:#9a9aa2;--line:#2e2e33;--head:#222227;--accent:#f08a5d;--hl:#2b2218;--hl-line:#8a5a26;--code:#232327}}
:root[data-theme="dark"]{--bg:#17171a;--fg:#ececee;--muted:#9a9aa2;--line:#2e2e33;--head:#222227;
--accent:#f08a5d;--hl:#2b2218;--hl-line:#8a5a26;--code:#232327}
body{background:var(--bg);color:var(--fg);margin:0}
.sr{font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
max-width:1400px;margin:0 auto;padding:24px 16px 64px;color:var(--fg);background:var(--bg)}
.sr h1{font-size:26px;margin:0 0 8px}.sr h2{font-size:20px;margin:32px 0 10px;
border-bottom:1px solid var(--line);padding-bottom:4px}.sr h3{font-size:16px}
.sr code{background:var(--code);padding:1px 5px;border-radius:4px;font-size:13px}
.sr pre{background:var(--code);padding:10px 12px;border-radius:6px;overflow:auto}
.sr pre code{padding:0;background:none}
.sr blockquote{margin:10px 0;padding:8px 14px;background:var(--hl);border-left:4px solid var(--hl-line);
border-radius:4px}.sr blockquote p{margin:4px 0}
.sr a{color:var(--accent)}
.sr .tw{overflow-x:auto;margin:8px 0 4px;border:1px solid var(--line);border-radius:6px}
.sr table{border-collapse:collapse;width:100%;font-size:13px}
.sr th,.sr td{padding:5px 8px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
.sr th{background:var(--head);cursor:pointer;white-space:nowrap;position:sticky;top:0;user-select:none}
.sr th[data-dir="asc"]::after{content:" \\25B2";color:var(--muted)}
.sr th[data-dir="desc"]::after{content:" \\25BC";color:var(--muted)}
.sr td.num{text-align:right;font-variant-numeric:tabular-nums}
.sr .filter{width:100%;max-width:360px;box-sizing:border-box;padding:6px 9px;margin-top:6px;
border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg);font:inherit}
.sr .count{color:var(--muted);font-size:12px;margin-left:8px}
.sr .cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:10px;margin:10px 0 18px}
.sr .card{border:1px solid var(--line);border-radius:8px;padding:10px 12px;background:var(--head)}
.sr .card .v{font-size:22px;font-weight:650;line-height:1.2}.sr .card .k{color:var(--muted);font-size:12.5px;margin-top:2px}
.sr .tw.narrow{display:inline-block;max-width:100%}.sr .tw.narrow table{width:auto}
.sr .toc{position:sticky;top:0;z-index:2;display:flex;flex-wrap:wrap;gap:4px 14px;align-items:center;
padding:8px 0;margin-bottom:8px;background:var(--bg);border-bottom:1px solid var(--line);font-size:13px}
.sr .toc a{text-decoration:none}.sr .toc .sp{flex:1}
.sr .toc button{font:inherit;font-size:12px;padding:3px 9px;border:1px solid var(--line);border-radius:5px;
background:var(--head);color:var(--fg);cursor:pointer}
.sr details{border:1px solid var(--line);border-radius:6px;margin:8px 0;padding:4px 12px}
.sr details[open]{padding-bottom:10px}.sr summary{cursor:pointer;padding:6px 0}
.sr h2{scroll-margin-top:48px}.sr ol li{margin:3px 0}
"""

SCRIPT = """
(function(){
  document.querySelectorAll('.sr .toc button').forEach(function(b){
    b.addEventListener('click',function(){var on=b.getAttribute('data-open')==='1';
      document.querySelectorAll('.sr details').forEach(function(d){d.open=on;});});
  });
  document.querySelectorAll('.sr table').forEach(function(t){
    var wrap=t.parentNode, box=document.createElement('input'), count=document.createElement('span');
    var body0=t.tBodies[0];
    if(wrap.getAttribute('data-small')){sortable(t);return;}
    box.className='filter'; box.placeholder='Filter rows'; count.className='count';
    wrap.parentNode.insertBefore(box,wrap); wrap.parentNode.insertBefore(count,wrap);
    var body=t.tBodies[0], rows=Array.prototype.slice.call(body.rows);
    function show(){var q=box.value.toLowerCase(), n=0;
      rows.forEach(function(r){var on=!q||r.textContent.toLowerCase().indexOf(q)>-1;r.style.display=on?'':'none';n+=on;});
      count.textContent=n+' of '+rows.length+' rows';}
    box.addEventListener('input',show); show();
    sortable(t);
  });
  function sortable(t){
    var body=t.tBodies[0], rows=Array.prototype.slice.call(body.rows);
    Array.prototype.forEach.call(t.tHead.rows[0].cells,function(th,i){
      th.addEventListener('click',function(){
        var dir=th.getAttribute('data-dir')==='asc'?'desc':'asc';
        Array.prototype.forEach.call(t.tHead.rows[0].cells,function(o){o.removeAttribute('data-dir');});
        th.setAttribute('data-dir',dir);
        function key(r){var s=r.cells[i]?r.cells[i].textContent.trim():'',n=parseFloat(s.replace(/,/g,''));
          return (/^-?[\\d,]+(\\.\\d+)?$/.test(s)&&!isNaN(n))?[0,n]:[1,s.toLowerCase()];}
        rows.sort(function(a,b){var x=key(a),y=key(b),c=x[0]-y[0]||(x[1]<y[1]?-1:x[1]>y[1]?1:0);
          return dir==='asc'?c:-c;});
        rows.forEach(function(r){body.appendChild(r);});
      });
    });
  }
})();
"""


def inline(text):
    parts = re.split(r"(`[^`]+`)", text)
    out = []
    for p in parts:
        if p.startswith("`") and p.endswith("`") and len(p) > 1:
            out.append("<code>%s</code>" % html.escape(p[1:-1]))
            continue
        s = html.escape(p)
        s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', s)
        out.append(s)
    return "".join(out)


def split_row(line):
    cells = re.split(r"(?<!\\)\|", line.strip().strip("|"))
    return [c.strip().replace("\\|", "|") for c in cells]


def table(lines):
    head = split_row(lines[0])
    body = [split_row(l) for l in lines[2:]]
    if head and head[0] == "" and len(head) == 2:  # a key-figures table: draw it as cards
        return '<div class="cards">%s</div>' % "".join(
            '<div class="card"><div class="v">%s</div><div class="k">%s</div></div>' % (inline(r[1]), inline(r[0]))
            for r in body if len(r) > 1)
    cls = " narrow" if len(head) <= 4 else ""
    small = ' data-small="1"' if len(body) < 12 else ""
    out = ['<div class="tw%s"%s><table><thead><tr>' % (cls, small)]
    out += ["<th>%s</th>" % inline(h) for h in head]
    out.append("</tr></thead><tbody>")
    for row in body:
        out.append("<tr>")
        for c in row:
            num = re.fullmatch(r"-?[\d,]+(\.\d+)?", c) is not None
            out.append('<td%s>%s</td>' % (' class="num"' if num else "", inline(c)))
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def convert(md):
    lines = md.splitlines()
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            j = i + 1
            while j < len(lines) and not lines[j].startswith("```"):
                j += 1
            out.append("<pre><code>%s</code></pre>" % html.escape("\n".join(lines[i + 1:j])))
            i = j + 1
            continue
        if re.match(r"^\s*</?(details|summary)\b", line):  # collapsible groups pass through
            out.append(line)
            i += 1
            continue
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            n = len(m.group(1))
            anchor = re.sub(r"[^a-z0-9]+", "-", m.group(2).lower()).strip("-")
            out.append('<h%d id="%s">%s</h%d>' % (n, anchor, inline(m.group(2)), n))
            i += 1
            continue
        if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|?$", lines[i + 1]):
            j = i
            while j < len(lines) and lines[j].startswith("|"):
                j += 1
            out.append(table(lines[i:j]))
            i = j
            continue
        if line.startswith(">"):
            j, paras, cur = i, [], []
            while j < len(lines) and lines[j].startswith(">"):
                t = lines[j][1:].strip()
                if t:
                    cur.append(t)
                elif cur:
                    paras.append(" ".join(cur))
                    cur = []
                j += 1
            if cur:
                paras.append(" ".join(cur))
            out.append("<blockquote>%s</blockquote>" % "".join("<p>%s</p>" % inline(p) for p in paras))
            i = j
            continue
        if re.match(r"^\s*([-*]|\d+\.)\s+", line):
            ordered = bool(re.match(r"^\s*\d+\.", line))
            tag = "ol" if ordered else "ul"
            items = []
            while i < len(lines) and re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]):
                items.append(re.sub(r"^\s*([-*]|\d+\.)\s+", "", lines[i]))
                i += 1
            out.append("<%s>%s</%s>" % (tag, "".join("<li>%s</li>" % inline(t) for t in items), tag))
            continue
        if not line.strip():
            i += 1
            continue
        j, para = i, []
        while j < len(lines) and lines[j].strip() and not re.match(r"^(#|\||>|```|\s*([-*]|\d+\.)\s|\s*</?(details|summary))", lines[j]):
            para.append(lines[j].strip())
            j += 1
        out.append("<p>%s</p>" % inline(" ".join(para)))
        i = max(j, i + 1)
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("md", help="the report .md")
    ap.add_argument("--fragment", action="store_true", help="write <name>.fragment.html without the document wrapper")
    ap.add_argument("-o", "--out", help="output path")
    args = ap.parse_args()
    src = Path(args.md)
    md = src.read_text(encoding="utf-8")
    title_m = re.search(r"^#\s+(.*)", md, re.M)
    title = title_m.group(1) if title_m else src.stem
    toc = "".join('<a href="#%s">%s</a>' % (re.sub(r"[^a-z0-9]+", "-", h.lower()).strip("-"), html.escape(h))
                  for h in re.findall(r"^##\s+(.*)", md, re.M))
    nav = ('<nav class="toc">%s<span class="sp"></span><button type="button" data-open="1">Open all</button>'
           '<button type="button" data-open="0">Close all</button></nav>' % toc)
    body = '<div class="sr">%s%s</div>' % (nav, convert(md))
    if args.fragment:
        page = "<title>%s</title>\n<style>%s</style>\n%s\n<script>%s</script>\n" % (html.escape(title), STYLE, body, SCRIPT)
        out = Path(args.out) if args.out else src.with_suffix(".fragment.html")
    else:
        page = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width,initial-scale=1">'
                "<title>%s</title><style>%s</style></head><body>%s<script>%s</script></body></html>\n"
                % (html.escape(title), STYLE, body, SCRIPT))
        out = Path(args.out) if args.out else src.with_suffix(".html")
    out.write_text(page, encoding="utf-8")
    print("wrote %s" % out)


if __name__ == "__main__":
    main()
