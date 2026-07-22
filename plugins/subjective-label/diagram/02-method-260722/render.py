#!/usr/bin/env python3
"""board.md -> board.html — single-page dashboard render.

The .md is the ONLY source of truth. This script is one-way and idempotent:
edit board.md, re-run, board.html is replaced. Never hand-edit board.html.

    python3 render.py            # board.md -> board.html

Handles the board dialect only: `## §slug · title` sections, a meta line,
the four fields, ``` text blocks, > comment lanes, **bold**, `code`.
"""
import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
SRC = HERE / "board.md"
OUT = HERE / "board.html"

# ---------------------------------------------------------------- inline

def inline(s: str) -> str:
    s = html.escape(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img alt="\1" src="\2">', s)
    return s


def lane(line: str):
    """A comment line -> (who, text) or None."""
    m = re.match(r"^(>+)\s*(JL|RA|CC\d*)\s*(\[#[^\]]+\])?\s*:?\s*(.*)$", line)
    if not m:
        return None
    who = m.group(2)
    anchor = m.group(3) or ""
    return who, inline((anchor + " " if anchor else "") + m.group(4))


# ---------------------------------------------------------------- badges

BADGE = [
    ("🧠", "decide", r"🧠"),
    ("🔧", "build", r"🔧"),
]


def meta_badges(meta: str) -> str:
    """Split the section meta line into pill spans."""
    out = []
    for part in [p.strip() for p in meta.split("·") if p.strip()]:
        cls = "pill"
        if "🧠" in part:
            cls += " decide"
        elif "🔧" in part:
            cls += " build"
        elif "⛔" in part or "⏳" in part:
            cls += " block"
        elif "✅" in part:
            cls += " done"
        elif "🟠" in part:
            cls += " open"
        out.append(f'<span class="{cls}">{inline(part)}</span>')
    return "".join(out)


# ---------------------------------------------------------------- parse

def render(md: str) -> str:
    lines = md.split("\n")
    body, i, in_pre = [], 0, False
    sections = []           # (slug, title) for the jump nav

    while i < len(lines):
        ln = lines[i]

        if ln.startswith("```"):
            body.append("</pre>" if in_pre else '<pre class="ascii">')
            in_pre = not in_pre
            i += 1
            continue
        if in_pre:
            body.append(html.escape(ln))
            i += 1
            continue

        if ln.startswith("# "):
            body.append(f"<h1>{inline(ln[2:])}</h1>")
        elif re.match(r"^## .*〔#[\w-]+〕\s*$", ln):
            m = re.match(r"^## (.*?)\s*〔#([\w-]+)〕\s*$", ln)
            title, slug = m.group(1), m.group(2)
            sections.append((slug, title))
            # the meta line is the next non-blank line if it is bold-led
            meta = ""
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and lines[j].lstrip().startswith("**"):
                meta = lines[j]
                i = j
            body.append(
                f'<section class="card" id="{slug}">'
                f'<h2>{inline(title)} <a class="slug" href="#{slug}">#{slug}</a></h2>'
                f'<div class="meta">{meta_badges(meta)}</div>'
                f'<button class="copy" data-slug="{slug}">💬 复制评论模板</button>'
            )
        elif ln.startswith("## "):
            body.append(f"<h2 class=\"plain\">{inline(ln[3:])}</h2>")
        elif ln.startswith("---"):
            body.append("<hr>")
        elif (c := lane(ln)) is not None:
            who, txt = c
            k = "jl" if who == "JL" else ("ra" if who == "RA" else "cc")
            body.append(f'<div class="cmt {k}"><b>{who}</b> {txt}</div>')
        elif ln.lstrip().startswith("- "):
            body.append(f'<div class="field">{inline(ln.lstrip()[2:])}</div>')
        elif ln.strip():
            body.append(f"<p>{inline(ln)}</p>")
        i += 1

    # close any open card before the next h1/h2-plain — simpler: close all at end
    html_body = "\n".join(body)
    html_body = re.sub(r'(?=<section class="card")', "</section>", html_body, count=0)
    # naive: one section closes when the next starts; add trailing close
    html_body = html_body.replace('</section><section class="card"', '</section>\n<section class="card"')
    if '<section class="card"' in html_body:
        html_body += "\n</section>"

    nav = " · ".join(f'<a href="#{s}">§{s}</a>' for s, _ in sections)
    return PAGE.replace("{{BODY}}", html_body).replace("{{NAV}}", nav)


PAGE = """<!doctype html>
<meta charset="utf-8">
<title>board — subjective-label</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{
  --bg:#fbfbf9; --fg:#1c1c1c; --mut:#6b6b6b; --line:#e2e2dd; --card:#fff;
  --pre:#f5f5f1; --jl:#1f5aa8; --ra:#15803d; --cc:#8a8a8a; --warn:#b45309;
}
@media (prefers-color-scheme:dark){:root{
  --bg:#16171a; --fg:#e8e8e6; --mut:#9a9a97; --line:#2c2e33; --card:#1d1f23;
  --pre:#111214; --jl:#6ea8f0; --ra:#5fc98a; --cc:#8a8a8a; --warn:#e0a458;
}}
:root[data-theme=dark]{
  --bg:#16171a; --fg:#e8e8e6; --mut:#9a9a97; --line:#2c2e33; --card:#1d1f23;
  --pre:#111214; --jl:#6ea8f0; --ra:#5fc98a; --cc:#8a8a8a; --warn:#e0a458;
}
:root[data-theme=light]{
  --bg:#fbfbf9; --fg:#1c1c1c; --mut:#6b6b6b; --line:#e2e2dd; --card:#fff;
  --pre:#f5f5f1; --jl:#1f5aa8; --ra:#15803d; --cc:#8a8a8a; --warn:#b45309;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
  font:15px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC",
  "Hiragino Sans GB","Microsoft YaHei",sans-serif;}
main{max-width:920px;margin:0 auto;padding:32px 20px 80px}
h1{font-size:25px;line-height:1.35;margin:0 0 6px}
h2{font-size:18px;margin:0 0 10px}
h2.plain{margin:34px 0 12px;padding-top:14px;border-top:1px solid var(--line)}
hr{border:0;border-top:1px solid var(--line);margin:26px 0}
p{margin:8px 0}
code{background:var(--pre);padding:1px 5px;border-radius:4px;
  font:13px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace}
pre.ascii{background:var(--pre);border:1px solid var(--line);border-radius:8px;
  padding:14px 16px;overflow-x:auto;
  font:12.5px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;margin:12px 0}
img{max-width:100%;border:1px solid var(--line);border-radius:8px}
nav{position:sticky;top:0;background:var(--bg);border-bottom:1px solid var(--line);
  padding:10px 0;margin-bottom:18px;font-size:13px;z-index:5}
nav a{color:var(--mut);text-decoration:none;margin-right:2px}
nav a:hover{color:var(--jl)}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;
  padding:18px 20px;margin:18px 0;position:relative}
.card h2 .slug{color:var(--mut);text-decoration:none;font:13px ui-monospace,monospace}
.card h2 .slug:hover{color:var(--jl)}
.meta{margin:-2px 0 12px;display:flex;flex-wrap:wrap;gap:6px}
.pill{font-size:12px;padding:2px 9px;border-radius:999px;
  border:1px solid var(--line);background:var(--pre);color:var(--mut)}
.pill.decide{border-color:var(--jl);color:var(--jl)}
.pill.build{border-color:var(--ra);color:var(--ra)}
.pill.block{border-color:var(--warn);color:var(--warn)}
.pill.open{border-color:var(--warn);color:var(--warn)}
.pill.done{border-color:var(--ra);color:var(--ra)}
.field{margin:9px 0;padding-left:2px}
.cmt{border-left:3px solid var(--cc);padding:5px 0 5px 11px;margin:7px 0;
  background:transparent;font-size:14px}
.cmt b{font-size:12px;letter-spacing:.4px;margin-right:6px}
.cmt.jl{border-color:var(--jl)} .cmt.jl b{color:var(--jl)}
.cmt.ra{border-color:var(--ra)} .cmt.ra b{color:var(--ra)}
.cmt.cc{border-color:var(--cc)} .cmt.cc b{color:var(--cc)}
.copy{position:absolute;top:16px;right:16px;font-size:12px;cursor:pointer;
  background:var(--pre);border:1px solid var(--line);color:var(--mut);
  border-radius:7px;padding:4px 10px}
.copy:hover{color:var(--jl);border-color:var(--jl)}
.note{color:var(--mut);font-size:12.5px;margin-top:40px;text-align:center}
</style>
<main>
<nav>{{NAV}}</nav>
{{BODY}}
<p class="note">generated from <code>board.md</code> · 不要手改这个文件 ·
<code>python3 render.py</code> 重新生成</p>
</main>
<script>
document.querySelectorAll('.copy').forEach(b=>b.onclick=()=>{
  const t=`> JL [#${b.dataset.slug}]: `;
  navigator.clipboard.writeText(t);
  b.textContent='✅ 已复制，粘进 board.md';
  setTimeout(()=>b.textContent='💬 复制评论模板',1800);
});
</script>
"""

# ================================================================ deck
# board.md -> deck.html : ONE SLIDE PER TOPIC, html-ppt academic-report style.
# Same single source. Regenerate whenever board.md changes.

DECK = HERE / "deck.html"
ASSETS = "../../../html-ppt/skills/html-ppt/assets"


def _blt(items):
    return '<ul class="blt">' + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>"


def _pre(block):
    return '<pre class="ascii">' + html.escape("\n".join(block)) + "</pre>"


def deck(md: str) -> str:
    lines = md.split("\n")
    slides = []

    # ---- collect the pieces we need -------------------------------------
    title = next((l[2:] for l in lines if l.startswith("# ")), "board")
    deliver = [l.lstrip("> ").strip() for l in lines
               if l.startswith("> ") and "交付物" in l or
               (l.startswith("> ") and l.lstrip("> ").startswith(("autonomy", "B03")))]

    pres, cur, inpre = [], [], False
    for l in lines:
        if l.startswith("```"):
            if inpre:
                pres.append(cur)
                cur = []
            inpre = not inpre
        elif inpre:
            cur.append(l)

    def pick(*keys):
        """First fenced block containing every key. Content-matched, so adding
        or reordering blocks in board.md never shifts the deck."""
        for b in pres:
            t = "\n".join(b)
            if all(k in t for k in keys):
                return b
        return None

    def add(name, h2, block, foot=""):
        if block is None:
            return
        slides.append((name, f'<h2 class="h2">{h2}</h2>' + _pre(block)
                       + (f'<p class="fnote">{foot}</p>' if foot else "")))

    # ---- 1 cover ---------------------------------------------------------
    dash = pick("📊", "题 ·")
    slides.append((
        "Cover",
        f'<h1 class="h1">{inline(title.replace("📋 ", ""))}</h1>'
        f'<p class="lede mt-s">{inline(" ".join(deliver))}</p>'
        + (_pre(dash) if dash else "")
    ))

    # ---- 2 the storyline --------------------------------------------------
    add("七步总览", "这七步现在的实现情况", pick("第 1 步", "第 7 步"))

    # ---- 3 the engine pipeline, and where the 6 topics pin ----------------
    add("几何图", "你在会上画的那张几何图", pick("clean case", "hard case"))

    # ---- 4 built but never run --------------------------------------------
    add("四个问题", "会上留下、到今天还没答的 4 个问题", pick("Q1", "Q4"),
        "commit 1eb432f6 · 2026-07-21 23:28 · +1616 行 · 6 个 lib 自测全绿 · "
        "note-update Part 12: “NOT yet done = real runs”")

    # ---- 5 F1-F8 ----------------------------------------------------------
    add("三层验证", "每改一版规则，要分三层考", pick("样例内", "泛化"))

    # ---- 6 盘面数字 --------------------------------------------------------
    add("锚点采样", "第 4 步：60 条怎么长到 140 条", pick("7 个锚点"))

    # ---- 6..n one slide per topic -----------------------------------------
    act = ""
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("# 🎬") or ln.startswith("# 🧹"):
            act = ln[2:].strip()
        if re.match(r"^## .*〔#[\w-]+〕\s*$", ln):
            m = re.match(r"^## (.*?)\s*〔#([\w-]+)〕\s*$", ln)
            stitle, slug = m.group(1), m.group(2)
            meta, why, fields = "", "", []
            j = i + 1
            while j < len(lines) and not lines[j].startswith(("## ", "# ", "---")):
                s = lines[j]
                if s.lstrip().startswith("**") and not meta:
                    meta = s
                elif s.startswith("> **为什么"):
                    why = re.sub(r"^>\s*", "", s)
                elif s.startswith(">") and why:
                    why += " " + re.sub(r"^>\s*", "", s).strip()
                elif s.lstrip().startswith("- "):
                    f = s.lstrip()[2:]
                    k = j + 1
                    while k < len(lines) and lines[k].startswith("  ") \
                            and not lines[k].lstrip().startswith("- "):
                        f += " " + lines[k].strip()
                        k += 1
                    fields.append(f)
                    j = k - 1
                j += 1
            pills = " · ".join(p.strip() for p in meta.replace("**", "").split("·") if p.strip())
            slides.append((
                slug,
                f'<p class="act">{inline(act)}</p>'
                f'<h2 class="h2">{inline(stitle)}</h2>'
                f'<p class="lede mt-s">{inline(pills)}</p>'
                + (f'<p class="fnote">{inline(why)}</p>' if why else "")
                + _blt(fields)
            ))
            i = j
            continue
        i += 1

    # ---- last: 现在等谁 ----------------------------------------------------
    slides.append((
        "等谁",
        '<h2 class="h2">现在卡在哪里</h2>'
        + _pre([
            "🧠 等 JL 决断 2 条 —— 落了它们，RA 6 条全部解锁",
            "   §license-scope   电池选谁      ⛔ 挡着 §license-run   (~3d)",
            "   §objective-wire  选择目标      ⛔ 挡着 §physician-rerun (~2d)",
            "",
            "🔧 RA 现在能立刻开工的 2 条",
            "   §probe-lexicon   词表自动生成  ~1d",
            "   §b02-collision   编号理干净    ~0.5d",
            "",
            "💡 已停放到下一块板：S9 全量应用 · 第二标注者执行 ·",
            "   老设计图订正 · plugin CHANGELOG",
        ])
    ))

    body = "\n".join(
        f'<section class="slide" data-title="{html.escape(t)}">\n{c}\n</section>'
        for t, c in slides
    )
    return DECK_PAGE.replace("{{TITLE}}", html.escape(title)) \
                    .replace("{{A}}", ASSETS).replace("{{BODY}}", body) \
                    .replace("{{N}}", str(len(slides)))


DECK_PAGE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{TITLE}}</title>
<link rel="stylesheet" href="{{A}}/fonts.css">
<link rel="stylesheet" href="{{A}}/base.css">
<link rel="stylesheet" id="theme-link" href="{{A}}/themes/academic-report.css">
<link rel="stylesheet" href="{{A}}/academic-report-extras.css">
<style>
  /* academic-report forces Times on `.slide *` with !important — ASCII
     diagrams MUST stay monospace or every box collapses. Out-specify it. */
  .slide pre.ascii, .slide pre.ascii *{
    font-family:ui-monospace,SFMono-Regular,Menlo,"DejaVu Sans Mono",monospace !important;
    font-size:11.5px;line-height:1.45}
  .slide pre.ascii{background:var(--surface-2);border:1px solid #d4d4d0;
    border-radius:2px;padding:12px 14px;overflow:auto;margin:12px 0;
    white-space:pre;flex:0 1 auto}
  /* `.kicker` is display:none in this theme (house rule: no kicker).
     The act label is content, not chrome — give it its own visible class. */
  .act{color:#8a8a8a;font-size:15px;margin:0 0 4px}
  .fnote{color:#6b6b6b;font-size:15px;margin:8px 0 2px}
  .lede{color:var(--accent)}
</style>
</head>
<body class="tpl-academic-report">
<div class="deck">
{{BODY}}
</div>
<script src="{{A}}/runtime.js"></script>
</body>
</html>
"""

if __name__ == "__main__":
    if not SRC.exists():
        sys.exit(f"missing {SRC}")
    src = SRC.read_text(encoding="utf-8")
    OUT.write_text(render(src), encoding="utf-8")
    DECK.write_text(deck(src), encoding="utf-8")
    n = deck(src).count('<section class="slide"')
    print(f"{SRC.name} -> {OUT.name} (dashboard) + {DECK.name} ({n} slides)")
