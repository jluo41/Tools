#!/usr/bin/env python3
"""board folder  ->  board.html   (STATIC. zero <script>. can never render blank.)

haipipe-board v0.1.0 — v0-series: never goes to 1.0.0 without JL saying so.

    python3 build.py [board-dir | board.md]

House form (follows 1-probes/: one question, one file):
    <board-dir>/
      board.md        # title / spine: / close: / source: / ## 主题 / ## 流水线
      Q1-<slug>.md    # title / state: / owner: / method: / ## 问题 ...
      Q2-<slug>.md
      board.html      <- generated
Legacy single-file boards ([BOARD]/[Qn] blocks in one board.md) still build.

Why static: VS Code's Live Preview webview blocks inline JS, and html-ppt's
base.css hides every `.slide` until runtime.js adds `.is-active`. A JS-built
page therefore renders pure white in the one place the user actually opens it.
So every question is written into the file as a real <section>, collapsibles use
native <details>, and jumping uses plain anchors. Nothing needs JS to be read.

Follows html-ppt conventions where free: `.slide` sections with `data-title`,
`body.single` (base.css's own no-JS escape hatch), `.h1/.h2/.lede/.blt` classes,
academic-report palette. So the same file can later be handed to runtime.js for
presenter mode without rewriting the content.
"""
import html, json, re, sys
from pathlib import Path

# 状态标签用英文：OPEN / PARTIAL / SETTLED / ON HOLD 是 issue 追踪的通用词，
# 一眼知道什么意思，不像自造的中文缩写要人猜。
ST = {"✅": ("done", "SETTLED"), "🟡": ("wip", "PARTIAL"),
      "🔴": ("todo", "OPEN"), "⏸️": ("hold", "ON HOLD")}
STN = {k.replace("️", ""): v for k, v in ST.items()}
# 段落名用英文（两边都认：新板写英文，老板写中文照样能读）
# 一个槽位可以有多个段名：规范名 -> [别名…]。中文老名字一直认（老板子不用改就能重新生成），
# 260723 改版又加了两个新名：Done when -> 「Items to Finish」、Now -> 「Where we are」。
ALIAS = {"Question": ["问题"], "Boundary": ["边界"], "Diagram": ["图"],
         "Files": ["文件"],
         "Done when": ["完成线", "Items to Finish"],
         "Now": ["现在什么样", "Where we are"],
         "Why here": ["为什么在这块板"],
         "Glossary": ["名词"], "Discussion": ["讨论"], "Comments": ["评论"],
         "Law": ["规矩"], "Lesson": ["教训"], "Log": ["日志"],
         "Topic": ["主题"], "Pipeline": ["流水线"], "Roster": ["清单"], "Links": ["链接"]}


def sec(d, key):
    """段落取值：先按规范名找，再挨个试别名（中文老名 + 新名）。"""
    if d.get(key):
        return d[key]
    for a in ALIAS.get(key, ()):
        if d.get(a):
            return d[a]
    return ""



CM_HEAD = re.compile(
    r"^-\s*\[([ xX])\]\s*([A-Z]{1,4}\d{0,4})\s*[「\"“]([^」\"”]+)[」\"”]"
    r"\s*(?:·\s*(\d{6}(?:\s+\d{3,4})?))?\s*[:：]?\s*(.*)$")


def parse_comments(txt):
    """## Comments -> [{done, who, quote, when, body[]}]

        - [ ] JL 「被选中的原句」 · 260723 1005
              评论正文，可以好几行
              >> CC0723: 回复接在下面
        - [x] ZW 「另一句」: 一行写完也行     ← [x] = 已解决

    勾选框就是状态：[ ] 没解决 / [x] 已解决。复用已有的语法，不另发明。
    """
    out = []
    for ln in (txt or "").split("\n"):
        m = CM_HEAD.match(ln.strip()) if ln.strip().startswith("-") else None
        if m:
            out.append({"done": m.group(1).lower() == "x", "who": m.group(2),
                        "quote": m.group(3), "when": m.group(4) or "",
                        "body": [m.group(5).strip()] if m.group(5).strip() else []})
        elif out and ln.strip():
            out[-1]["body"].append(ln.strip())
    return out


def render_comments(items):
    if not items:
        return ""
    rows = []
    for c in items:
        cls = "cm done" if c["done"] else "cm"
        when = ""
        if c["when"]:
            d = c["when"][:6]
            when = f'<span class="cw">{d[:2]}-{d[2:4]}-{d[4:]}'
            if len(c["when"]) > 6:
                hm = c["when"][6:].strip().zfill(4)
                when += f' {hm[:2]}:{hm[2:]}'
            when += "</span>"
        reps, main = [], []
        for b in c["body"]:
            (reps if b.startswith(">") else main).append(b)
        body = "".join(f"<p>{inline(x)}</p>" for x in main)
        body += "".join(
            f'<div class="cmt {who_class(re.match(chr(62)+"*.?([A-Z]{1,4})", x).group(1))}">'
            f'{inline(x.lstrip(chr(62)).strip())}</div>'
            if re.match(r">+\s*([A-Z]{1,4})", x) else f"<p>{inline(x)}</p>"
            for x in reps)
        # 已解决的评论：正文折叠起来，台面上只留一行标题（JL 260723：solved 该 collapse，别铺开全文）。
        # 没解决的：正文照常展开，等着你处理。
        if c["done"] and body.strip():
            body_html = (f'<details class="cmb-fold"><summary>reply</summary>'
                         f'<div class="cmb">{body}</div></details>')
        else:
            body_html = f'<div class="cmb">{body}</div>' if body.strip() else ""
        rows.append(
            f'<div class="{cls}" data-quote="{esc(c["quote"])}"'
            f' data-done="{"1" if c["done"] else ""}"><div class="cmh">'
            f'<span class="bx">{"☑" if c["done"] else "☐"}</span>'
            f'<b class="{who_class(c["who"])}">{esc(c["who"])}</b>'
            f'<span class="cq">“{inline(c["quote"])}”</span>{when}'
            + (f'<span class="cs unpin" title="The quoted sentence is not in this '
               'question\'s body — it may have been said in chat, or the original may have '
               'been edited since. No history is kept, so we only say it is not in the body.">'
               '· unanchored</span>' if c.get("lost") else "")
            + f'<span class="cs">{"solved" if c["done"] else "open"}</span></div>'
            f'{body_html}</div>')
    return "\n".join(rows)



LG_HEAD = re.compile(r"^(\d{6})(?:\s+(\d{3,4}))?\s*[·|]\s*(.*)$")


def sort_log(txt):
    """## Log 按时间倒序 —— 最新的在最上面。

    你在 md 里加到哪一行都行，生成时统一排。跨行的条目（缩进的续行）
    跟着它的头一行一起搬。没有时间戳的行原样留在最前面。
    """
    head, ents, cur = [], [], None
    for ln in (txt or "").split("\n"):
        m = LG_HEAD.match(ln.strip())
        if m:
            cur = [(m.group(1), (m.group(2) or "0000").zfill(4)), [ln]]
            ents.append(cur)
        elif cur is not None:
            cur[1].append(ln)
        elif ln.strip():
            head.append(ln)
    ents.sort(key=lambda e: e[0], reverse=True)
    return "\n".join(head + [l for e in ents for l in e[1]])


def stinfo(state):
    """'✅ 已定' / '⏸️ 会上没答完' -> (emoji, css-class, label)"""
    state = (state or "").strip() or "🔴"
    tok = state.split()[0]
    cls, lab = STN.get(tok.replace("️", ""), ("todo", "TODO"))
    rest = state[len(tok):].strip()
    return tok, cls, (rest or lab)


def who_class(who):
    """署名 -> 颜色。JL / RA / CC 固定，其他人按名字分到一个稳定的颜色。"""
    base = re.sub(r"\d+$", "", who).upper()
    if base in ("JL", "RA", "CC"):
        return base.lower()
    return "u" + str(sum(ord(c) for c in base) % 4)


def esc(s):
    return html.escape(str(s))


BASE = None            # 当前这块板的文件夹，main 里设；用来把路径解析成链接
LINKS = {}             # board.md 的 ## Links 声明的： 反引号里的写法 -> 相对路径
EXT = ("md", "py", "html", "css", "js", "json", "yaml", "yml", "sh", "txt", "ipynb",
       "do", "R", "r", "sql", "tex", "bib", "toml", "csv", "tsv", "ps1", "log")


def resolve(token):
    """`反引号里的路径` -> 相对 board.html 的 href，解析不到就返回 None。

    板上讨论的东西（SKILL.md、build.py、另一块板…）和板本身是分开放的，
    光写个路径读者点不动。这里做的事：从板的文件夹往上一路找，
    第一个真实存在的匹配就变成可点的链接。**文件必须真的存在**才链 ——
    否则 `Q*.md`、`- [ ]` 这种也会被误当成路径。
    """
    if not token:
        return None
    if token in LINKS:                      # 板自己声明的，优先，且不做存在性猜测
        return LINKS[token]
    if BASE is None or " " in token:
        return None
    tok = token.rstrip("/")
    if "/" not in tok and tok.rsplit(".", 1)[-1] not in EXT:
        return None
    if any(c in tok for c in "*?<>|"):
        return None
    here = BASE
    for _ in range(8):
        cand = (here / tok)
        if cand.exists():
            try:
                import os
                return os.path.relpath(cand, BASE)
            except ValueError:
                return None
        if (here / ".git").exists() or (here / "pyproject.toml").exists():
            break
        if here.parent == here:
            break
        here = here.parent
    return None


def code_or_link(m):
    tok = m.group(1)
    href = resolve(tok)
    if href:
        return f'<a class="fp" href="{esc(href)}"><code>{esc(tok)}</code></a>'
    return f"<code>{esc(tok)}</code>"


def inline(s):
    s = esc(s)
    s = re.sub(r"`([^`]+)`", code_or_link, s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a class="fp" href="\2">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img alt="\1" src="\2">', s)
    # 裸 URL 自动变链接（放最后）。前面那个 lookbehind 是为了别去动已经躺在
    # href="…" / src="…" 里的地址 —— 否则会把链接再套一层链接。
    s = re.sub(r'(?<![\"\'=])(https?://[^\s<>"\')]+)',
               r'<a class="fp" href="\1" target="_blank" rel="noopener">\1</a>', s)
    return s


STAMP = re.compile(r"^(\d{6})\s+([A-Z]{1,4}\d{0,4})\s*·\s*(.+)$")


def split_stamp(text):
    """item 名字开头的「260722 JL · …」→ (右侧灰印, 真标题)。

    日期和人不该混进标题文字里（JL 260724）。抽出来单独渲染成一个淡印，
    标题只留后半句。没有前缀就原样返回。
    """
    m = STAMP.match(text.strip())
    if not m:
        return "", text
    d = m.group(1)
    stamp = (f'<span class="stmp"><span class="sd">{d[:2]}-{d[2:4]}-{d[4:]}</span>'
             f'<span class="sw {who_class(m.group(2))}">{esc(m.group(2))}</span></span>')
    return stamp, m.group(3)


def flat_rows(txt):
    """把「- 小标题 / 缩进解释」铺成扁平的一行行 <p><b>小标题</b> 解释</p>。

    给 Boundary 这种收进折叠块的短内容用 —— 折叠块里不该再套一层折叠（JL 260724）。
    """
    items, cur = [], None
    for ln in (txt or "").split("\n"):
        m = re.match(r"^[-*]\s+(.+)$", ln)
        if m:
            if cur:
                items.append(cur)
            cur = [m.group(1).strip(), []]
        elif cur is not None and ln.strip():
            cur[1].append(ln.strip())
    if cur:
        items.append(cur)
    rows = []
    for head, exp in items:
        e = " ".join(exp)
        rows.append(f'<p class="brow"><b>{inline(head)}</b>'
                    + (f' {inline(e)}' if e else "") + "</p>")
    return "".join(rows)


def mark_span(html, needle, kls):
    """把 needle（已转义的纯文字）在 html 里对应的那一段包进 <mark>，
    **哪怕这段横跨行内标签**（`代码`→<code>、**粗**→<b>）。

    做法：建一张「可见文字下标 → html 下标」的映射（跳过 <...> 里的东西），
    在可见文字里找 needle，然后在对应的 html 位置插 <mark>…</mark>。
    这样评论选中的句子即使中间夹着 <code> 也能正确描黄 —— 之前 naive 的
    `needle in html` 一遇标签就对不上，评论就「贴不到原文」了（JL 260723）。
    返回 (新 html, 是否命中)。
    """
    idx, intag, i = [], False, 0
    vis = []
    while i < len(html):
        ch = html[i]
        if ch == "<":
            intag = True
        elif ch == ">":
            intag = False
        elif not intag:
            vis.append(ch)
            idx.append(i)
        i += 1
    pos = "".join(vis).find(needle)
    if pos < 0:
        return html, False
    s, e = idx[pos], idx[pos + len(needle) - 1] + 1
    return html[:s] + f"<mark{kls}>" + html[s:e] + "</mark>" + html[e:], True


# 组标题（整行加粗）开头若写了个 emoji，就拿它当记号：**🎨 版式落地** → 🎨。
# 没写就默认 🔹。build.py 不去猜——图标随内容变，是作者写的，不是机器生成的（QA5 写法规矩）。
# 只认真 emoji 开头：中文、英文、▸(U+25B8) 都不在这些区段，不会误判成图标。
_EMO = ("\U0001F000-\U0001FAFF"      # 大部分 emoji（🔹🎨📍…）
        "\U00002600-\U000027BF"      # 杂项符号 + dingbats（✅⚠⚙…）
        "\U00002B00-\U00002BFF"      # ⭐ 等
        "\U00002190-\U000021FF"      # 箭头
        "\U00002300-\U000023FF")     # ⏰⌛ 等
GT_ICON = re.compile("^([" + _EMO + "]"
                     "[" + _EMO + "️‍\U0001F3FB-\U0001F3FF]*)"
                     r"\s+(.+)$")


def body(txt, fold_code=True):
    """paragraphs + ``` blocks + comment lanes + topic/explanation bullets -> html

    要点式排版（JL 260723）：一行 `- 小标题`，下面缩进两格的行是它的解释。
        - 选中就能评论
          光标下冒出「💬 Comment」，点它填字保存。
          保存的瞬间那句话变黄底高亮。
    比一段接一段的散句好扫。`- [ ]` 是勾选清单，不走这条路。

    fold_code=True（默认）：``` 代码块也收进 <details>，默认合着、想看再点开（JL 260723），
    跟节标题的 expand-all 联动。传 False 才铺开（`## Diagram` 那张招牌图就用它）。
    """
    out, fence, blt, lg, flang = [], None, None, None, ""

    def flush():
        """把攒着的要点 / 勾选项吐出来。两者共用「小标题 + 缩进解释」这套结构。"""
        nonlocal blt
        if blt is None:
            return
        kind, top, det, on = blt
        name_cls = "ct" if kind == "ck" else "bt"
        # item = 名字 + 解释。名字永远在台面上；有解释时把它收进 native <details>，
        # 想看再点开 —— 纯 CSS，零脚本（JL 260723）。没解释就是一行光名字。
        # 名字开头的「260722 JL ·」抽成右侧灰印，标题只留后半句（JL 260724）。
        stamp, title = split_stamp(top)
        # 标题开头写个 emoji 就当图标（跟组标题一个规矩，作者写、机器不猜）。
        im = GT_ICON.match(title)
        icon = f'<span class="ti">{im.group(1)}</span>' if im else ""
        if im:
            title = im.group(2).strip()
        if det:
            # 「click the row」，收干净（JL 260724）：台面上只留标题（图标+灰印+caret）；
            #   一句话摘要和长解释【都】藏起来，点这一整行才铺开。
            #   摘要是解释的第一段（.ld，深一档），其余段落淡一档，展开后一眼分层。
            head = (f'<div class="{name_cls} nof">{icon}'
                    f'<span class="ttl">{inline(title)}</span>'
                    f'{stamp}<span class="cv"></span></div>')
            exp = "".join(
                f'<p class="ld">{inline(x)}</p>' if i == 0 else f'<p>{inline(x)}</p>'
                for i, x in enumerate(det))
            item = (f'<details class="it row"><summary>{head}</summary>'
                    f'<div class="bd">{exp}</div></details>')
        else:
            item = (f'<div class="{name_cls} nod">{icon}'
                    f'<span class="ttl">{inline(title)}</span>{stamp}</div>')
        if kind == "ck":
            out.append(f'<div class="ck{" on" if on else ""}">'
                       f'<span class="bx">{"☑" if on else "☐"}</span>'
                       f'<div class="itw">{item}</div></div>')
        else:
            out.append(f'<div class="blt">{item}</div>')
        blt = None

    for ln in (txt or "").split("\n"):
        if ln.lstrip().startswith("```"):
            flush()
            if fence is None:
                fence = []
                flang = ln.lstrip()[3:].strip()
            else:
                code = esc(chr(10).join(fence))
                if fold_code:
                    lab = ('&lt;/&gt; code'
                           + (f' · {esc(flang)}' if flang else '')
                           + f' · {len(fence)} lines')
                    out.append(f'<details class="it codef"><summary class="cs">{lab}'
                               f'</summary><pre>{code}</pre></details>')
                else:
                    out.append(f'<pre>{code}</pre>')
                fence = None
            continue
        if fence is not None:
            fence.append(ln)
            continue
        # (fenced block accumulates verbatim; flushed on the closing ```)
        if blt is not None and re.match(r"^\s{2,}\S", ln):
            blt[2].append(ln.strip())
            continue
        if lg is not None and re.match(r"^\s{2,}\S", ln):   # Log 条目的续行
            out[lg] = out[lg].replace("</span></div>",
                                      " " + inline(ln.strip()) + "</span></div>")
            continue
        lg = None
        m = re.match(r"^[-*]\s+(?!\[[ xX]\])(.+)$", ln)
        if m:
            flush()
            blt = ["blt", m.group(1).strip(), [], False]
            continue
        flush()
        if not ln.strip():
            continue
        # 260723 0940 · 改了什么      （时间可省，省了就只显示日期）
        m = re.match(r"^(\d{6})(?:\s+(\d{3,4}))?\s*[·|]\s*(.*)$", ln)
        if m:
            d, hm = m.group(1), m.group(2)
            stamp = f"{d[:2]}-{d[2:4]}-{d[4:]}"
            if hm:
                hm = hm.zfill(4)
                stamp += f" {hm[:2]}:{hm[2:]}"
            out.append(f'<div class="lg"><span class="d">{stamp}</span>'
                       f'<span>{inline(m.group(3))}</span></div>')
            lg = len(out) - 1
            continue
        m = re.match(r"^\s*[-*]\s*\[([ xX])\]\s*(.*)$", ln)   # - [ ] / - [x]
        if m:
            flush()
            blt = ["ck", m.group(2), [], m.group(1).lower() == "x"]
            continue
        # 一行只放一个 excalidraw 分享链接 → 嵌成一块可交互画布，底下再给一条链接。
        # 为什么敢嵌：excalidraw.com 没有 X-Frame-Options / frame-ancestors（实测）。
        # 为什么还要那条链接：断网 / iframe 被拦时，画布是空的，链接仍然点得开 —— 不靠 iframe 才读得到。
        m = re.match(r"^\s*(https?://(?:app\.)?excalidraw\.com/\S+)\s*$", ln)
        if m:
            u = esc(m.group(1))
            out.append(f'<div class="xcal"><iframe src="{u}" loading="lazy" '
                       f'referrerpolicy="no-referrer"></iframe>'
                       f'<a class="fp xopen" href="{u}" target="_blank" rel="noopener">'
                       f'↗ Open in Excalidraw</a></div>')
            continue
        # 整行加粗 = 组标题：领着下面一串 item 的一句话。图标 + 略大 + 上间距，
        # 夹在节标题(.ch)和 item 名字(.bt)中间一层，把层级拉开（JL 260723）。
        # 只认「整行都在 **…** 里」的（内部不含 **），混排的加粗照旧走 <p>。
        # 图标随内容变：加粗开头写个 emoji 就用它（GT_ICON），没写用默认 🔹。
        m = re.match(r"^\*\*((?:(?!\*\*).)+)\*\*\s*$", ln)
        if m:
            inner = m.group(1).strip()
            im = GT_ICON.match(inner)
            icon, txt = (im.group(1), im.group(2).strip()) if im else ("🔹", inner)
            out.append(f'<div class="gt"><span class="gi">{icon}</span>{inline(txt)}</div>')
            continue
        # > JL 「被选中的原句」: 评论    ← 行内评论；引号里那段会在正文里高亮
        m = re.match(r"^(>+)\s*([A-Z]{1,4}\d{0,4})\s*[「\"]([^」\"]+)[」\"]\s*[:：]\s*(.*)$", ln)
        if m:
            who = m.group(2)
            k = who_class(who)
            out.append(f'<div class="cmt {k}"><b>{esc(who)}</b>'
                       f'<span class="qt">「{inline(m.group(3))}」</span> {inline(m.group(4))}</div>')
            continue
        m = re.match(r"^(>+)\s*([A-Z]{1,4}\d{0,4})\s*(\[[^\]]+\])?\s*[:：]\s*(.*)$", ln)
        if m:
            who = m.group(2)
            k = who_class(who)
            out.append(f'<div class="cmt {k}"><b>{esc(who)}</b> {inline(m.group(4))}</div>')
        else:
            out.append(f"<p>{inline(ln)}</p>")
    flush()
    return "\n".join(out)


def split_blocks(src):
    out, cur, buf = {}, None, []
    for ln in src.split("\n"):
        m = re.match(r"^\[([^\]]+)\]\s*$", ln)
        if m:
            if cur:
                out[cur] = "\n".join(buf).strip()
            cur, buf = m.group(1), []
        else:
            buf.append(ln)
    if cur:
        out[cur] = "\n".join(buf).strip()
    return out


def split_sections(txt):
    """split on `## ` headings — but NEVER inside a ``` fence, or a template
    block that shows what `## 问题` looks like would tear its own file apart."""
    out, cur, buf, fence = {}, None, [], False
    for ln in txt.split("\n"):
        if ln.lstrip().startswith("```"):
            fence = not fence
        if ln.startswith("## ") and not fence:
            if cur:
                out[cur] = "\n".join(buf).strip()
            cur, buf = ln[3:].strip(), []
        else:
            buf.append(ln)
    if cur:
        out[cur] = "\n".join(buf).strip()
    return out


def parse_board(board):
    """board-level text (no [Qn] blocks) -> meta dict"""
    def f(k):
        m = re.search(rf"^{k}:\s*(.*)$", board, re.M)
        return m.group(1).strip() if m else ""

    bs = split_sections(board)
    title = next((l[2:].strip() for l in board.split("\n") if l.startswith("# ")), "board")
    LINKS.clear()
    for ln in sec(bs, "Links").split("\n"):
        parts = ln.strip().split(None, 1)
        if len(parts) == 2 and not ln.startswith("#"):
            LINKS[parts[0]] = parts[1].strip()
    return dict(title=title, spine=f("spine"), close=f("close"),
                theme=sec(bs, "Topic"), pipeline=sec(bs, "Pipeline"), dir="")


def parse_q(qid, txt, group="", file=""):
    """one question's text (title line + meta lines + ## sections) -> q dict"""
    lines = txt.split("\n")
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    qt = lines[i].lstrip("# ").strip() if i < len(lines) else qid
    i += 1
    meta = {"state": "🔴", "owner": "", "method": "", "session": ""}
    while i < len(lines) and not lines[i].startswith("## "):
        m = re.match(r"^(state|owner|method|session):\s*(.*)$", lines[i].strip())
        if m:
            meta[m.group(1)] = m.group(2).strip()
        i += 1
    return dict(id=qid, title=qt, group=group, file=file,
                sec=split_sections("\n".join(lines[i:])), **meta)


def parse_file(md):
    """legacy single-file board: [BOARD] + [Q1] + [Q2] ... blocks"""
    B = split_blocks(md)
    qs = [parse_q(k, B[k]) for k in sorted(
        [k for k in B if re.fullmatch(r"Q\d+", k)], key=lambda x: int(x[1:]))]
    return parse_board(B.get("BOARD", "")), qs, []


def parse_dir(d):
    """house form: board.md + Q<n>-<slug>.md files in one folder.

    The Q files ARE the board — binding is by PATH (same folder), the way
    1-probes/ does it, so a question can never desync from its roster entry.
    board.md's optional `## 清单` only sets ORDER and GROUPING; a file on disk
    that nobody listed is still rendered (under ⚠️), never silently dropped.
    """
    bp = d / "board.md"
    board = re.sub(r"^\[BOARD\]\s*\n", "",
                   bp.read_text(encoding="utf-8") if bp.exists() else "")
    # 文件名前缀就是这题的编号：Q1 / QA1 / QB3。字母是组，数字是组内序号。
    disk = {}
    for p in d.glob("Q*.md"):
        m = re.match(r"Q([A-Z]*)(\d+)([a-z]?)", p.stem)
        if m:
            disk[p.name] = ((m.group(1), int(m.group(2)), m.group(3)),
                            "Q" + m.group(1) + m.group(2) + m.group(3), p)
    if not disk:                        # legacy: everything in one board.md
        return parse_file(board)

    order, seen, warn, group, gintro = [], set(), [], "", {}
    for ln in sec(split_sections(board), "Roster").split("\n"):
        ln = ln.strip()
        if ln.startswith("### "):
            group = ln[4:].strip()
        elif ln.endswith(".md"):
            name = ln.lstrip("-*· ").strip()
            if name in disk:
                order.append((group, disk[name][2]))
                seen.add(name)
            else:
                warn.append(f"{name} is listed in the Roster but no such file exists")
        elif ln and group:
            # Plain lines between a "### " heading and its first .md line are the
            # GROUP INTRO (QC2, JL 260724): line 1 = the sentence that always shows
            # under the header; the rest = the click-to-expand "what / why" body.
            gintro.setdefault(group, []).append(ln)
    listed = bool(order)
    for name, (key, qid, p) in sorted(disk.items(), key=lambda kv: kv[1][0]):
        if name not in seen:
            if listed:
                warn.append(f"{name} is not listed in board.md's ## Roster")
            order.append(("⚠️ Not in Roster" if listed else "", p))

    qs = [parse_q(disk[p.name][1], p.read_text(encoding="utf-8"), g, p.name)
          for g, p in order]
    meta = parse_board(board)
    meta["dir"] = str(d.resolve())
    meta["groups"] = {g: ls for g, ls in gintro.items() if ls}
    return meta, qs, warn


def render(meta, qs):
    done = sum(1 for q in qs if q["state"].startswith("✅"))
    n = len(qs)
    bar = "█" * round(done / n * 14) + "░" * (14 - round(done / n * 14)) if n else ""

    def st(q):
        return stinfo(q["state"])

    open_cm = {q["id"]: sum(1 for c in parse_comments(sec(q["sec"], "Comments"))
                            if not c["done"]) for q in qs}

    def frac_done(q):
        """完成度 0..1：Done when 勾了几条。✅ 一律满格，⏸️ 当作定了也满格。"""
        s = q["state"]
        if s.startswith("✅") or s.startswith("⏸"):
            return 1.0
        boxes = re.findall(r"^\s*[-*]\s*\[([ xX])\]", sec(q["sec"], "Done when"), re.M)
        if not boxes:
            return 0.0
        return sum(1 for b in boxes if b.lower() == "x") / len(boxes)

    ginfo = meta.get("groups") or {}
    rows, cur = [], None
    for q in qs:
        if q.get("group") and q["group"] != cur:
            cur = q["group"]
            rows.append(f'<div class="grp" data-g="{esc(cur)}">'
                        f'<span class="gt">{inline(cur)}</span></div>')
            # Group intro (QC2): one sentence always visible; if more lines follow,
            # they open on click via a native <details>. No script involved, so the
            # strip-scripts invariant is untouched.
            gi = ginfo.get(cur)
            if gi and len(gi) > 1:
                gib = "<br>".join(inline(x) for x in gi[1:])
                rows.append(f'<details class="gi"><summary>{inline(gi[0])}</summary>'
                            f'<div class="gib">{gib}</div></details>')
            elif gi:
                rows.append(f'<div class="gi one">{inline(gi[0])}</div>')
        # 完成度上色：一条没做 = 白，越接近做完越绿（绿色叠加的透明度 = 完成比例）
        fr = frac_done(q)
        pct = round(fr * 100)
        fill = (f' style="--fill:{fr:.3f}"') if fr > 0 else ""
        df = f' data-f="{esc(q["file"])}"' if q.get("file") else ""
        rows.append(
            f'<a class="ir {st(q)[1]}" href="#{q["id"]}"{fill}{df} title="{pct}% done">'
            f'<span class="s">{st(q)[0]}</span><span class="i">{q["id"]}</span>'
            f'<span class="t">{inline(q["title"])}</span>'
            + (f'<span class="obadge">💬 {open_cm[q["id"]]}</span>' if open_cm[q["id"]] else "")
            + f'<span class="w">{"🧠 JL" if q["owner"]=="JL" else ("🔧 "+q["owner"] if q["owner"] else "")}</span></a>')
    idx = "\n".join(rows)

    def det(label, inner, open_=False):
        if not inner:
            return ""
        o = " open" if open_ else ""
        return (f'<details class="fold"{o}><summary>{esc(label)}</summary>'
                f'<div class="fb">{inner}</div></details>')

    def chead(label, inner):
        """一个节标题：左边标签、底下一条线（CSS 画）、右边一个「expand all」。
        只有这一节真有可折叠的 item（body 里出现 class="it"）才挂那个按钮 ——
        没东西可开合就不放。纯增强：脚本剥掉后每个 item 仍能单独点开。"""
        tog = ('<button class="secall" type="button" title="expand / collapse all">'
               '<span class="lbl">expand all</span></button>'
               if '<details class="it' in inner else '')
        return f'<div class="ch"><span class="chl">{label}</span>{tog}</div>'

    cards = []
    for i, q in enumerate(qs):
        prv, nxt = (qs[i - 1] if i else None), (qs[i + 1] if i + 1 < n else None)
        nav = ('<div class="nav">'
               + (f'<a href="#{prv["id"]}">← {prv["id"]}</a>' if prv else '<span></span>')
               + f'<a class="all" href="#top">☰ Index</a>'
               + (f'<a href="#{nxt["id"]}">{nxt["id"]} →</a>' if nxt else '<span></span>')
               + '</div>')
        tok, cls, lab = st(q)
        who = "🧠 JL decides" if q["owner"] == "JL" else ("🔧 " + q["owner"] if q["owner"] else "")
        # 顺序（JL 260723 改版）：先「什么算做完」，再「现在到哪了」。
        # 原来 Now 在上，零背景的人先撞上一堵实现细节，还没搞懂目标就淹了 ——
        # 先给意图（目标），再给状态（进度）。
        now, goal = sec(q["sec"], "Now"), sec(q["sec"], "Done when")
        boxes = re.findall(r"^\s*[-*]\s*\[([ xX])\]", goal, re.M)
        cnt = (f'<span class="cnt">{sum(1 for b in boxes if b.lower()=="x")}/{len(boxes)}</span>'
               if boxes else "")
        fs = ""
        if now or goal:
            nb, gb = body(now), body(goal)
            fs += ('<div class="cmp">'
                   f'<div class="col goal">{chead(f"🎯 Items to Finish{cnt}", gb)}{gb}</div>'
                   f'<div class="col now">{chead("📍 Where we are", nb)}{nb}</div>'
                   '</div>')
        # 「Why here」不再单独占台面：它该讲的（为什么难 / 不定会怎样）并进 ## Question
        # 的要点里，光读第一节就 orient。老板子里还写着这段的，收进底部折叠区，内容不丢。
        why = sec(q["sec"], "Why here")
        disc = sec(q["sec"], "Discussion").strip()
        cms = parse_comments(sec(q["sec"], "Comments"))

        # 先高亮，再渲染评论 —— 这样每条评论知道自己有没有锚上，
        # 锚不上的当场标出来（原文改过之后引文就对不上了，不能让它悄悄失效）。
        # ## Question 是「一段话 + 几个要点」（JL 260723 改版）：走 body() 才吃得下要点。
        # 第一段是大字领句（CSS 挑 p:first-of-type），要点跟在下面 —— 光这一节就该让
        # 零背景的人明白：在问什么、为什么难、不定会怎样（原 Why here 的活并进来了）。
        # ## Question（JL 260724）：领句本身可点，点这一整行才铺开隐藏块。
        # 隐藏块里带小标题、readable：Why this matters（解释）+ 🚧 Boundary（管/不管）。
        # 问句里的 **粗体** 要正常内联流动 —— 所以文字包进一个 .qt span，别让 flex 拆散它。
        # Boundary 收进【同一个】折叠块，不再单占一节；里头用扁平行，不套第二层折叠。
        q_md = sec(q["sec"], "Question").strip()
        _parts = re.split(r"\n\s*\n", q_md, 1)
        qlead = inline(_parts[0].replace("\n", " ").strip())
        qrest = _parts[1].strip() if len(_parts) > 1 else ""
        btxt = sec(q["sec"], "Boundary").strip()
        inner = ""
        if qrest:
            inner += f'<div class="fh">Why this matters</div>{body(qrest)}'
        if btxt:
            inner += f'<div class="fh">🚧 Boundary</div>{flat_rows(btxt)}'
        if inner:
            qblock = (f'<details class="it row qd"><summary>'
                      f'<p class="qlead"><span class="qt">{qlead}</span>'
                      f'<span class="cv"></span></p></summary>'
                      f'<div class="bd qbd">{inner}</div></details>')
        else:
            qblock = f'<p class="qlead"><span class="qt">{qlead}</span></p>'
        ask = (f'<div class="ask"><span class="ql">❓ Question</span>{qblock}</div>')
        bnd = ""   # Boundary 现在收在 ask 的折叠块里，不再单独上台面
        # 📁 Files（JL 260723 新增，选填）：这题牵动哪些文件。读懂之后知道去哪儿动手；
        # 反过来改了哪个文件，也知道该回写哪一题。路径写反引号里，board.md 的
        # ## Links 声明过的会自动变成可点链接。
        flb = body(sec(q["sec"], "Files"))
        fls = f'<div class="fls">{chead("📁 Files", flb)}{flb}</div>' if flb else ""
        dia = (f'<div class="dia">{body(sec(q["sec"], "Diagram"), fold_code=False)}</div>'
               if sec(q["sec"], "Diagram") else "")

        def _norm(s):
            # 剥掉标签、把连续空白压成一个 —— 拿来判「这句到底在不在页面上」
            return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()

        # 卡片上所有可见文字的「纯文本」快照，用来判 lost（不含标签、空白已归一）
        card_plain = _norm(ask + " " + bnd + " " + fs + " " + fls + " " + dia)

        def hl(quote, solved):
            # 锚点为什么老丢，两个原因都堵上（JL 260723 问）：
            #   ① 扫描范围太窄：以前只扫 ask+fs，选中「## Diagram」里的字就被冤枉。→ 现在也扫 dia。
            #   ② 引文横跨行内标记：`代码`→<code>、**粗**→<b>。用 mark_span 跨标签描黄，
            #      不再是 naive 的 e in html（那个一遇标签就贴不到原文）。
            #   兜底：连跨标签都找不到（空白差异等），退一步用纯文本判「在不在」——
            #        在就不算 lost（只是这一条没描黄）。
            nonlocal ask, bnd, fs, fls, dia
            e = esc(quote)
            kls = ' class="solved"' if solved else ''
            for name in ("ask", "bnd", "fs", "fls", "dia"):
                cur = {"ask": ask, "bnd": bnd, "fs": fs, "fls": fls, "dia": dia}[name]
                new, ok = mark_span(cur, e, kls)
                if ok:
                    if name == "ask":
                        ask = new
                    elif name == "bnd":
                        bnd = new
                    elif name == "fs":
                        fs = new
                    elif name == "fls":
                        fls = new
                    else:
                        dia = new
                    return True
            nq = _norm(e)
            return bool(nq) and nq in card_plain

        for c in cms:
            c["lost"] = not hl(c["quote"], c["done"])
        for x in re.findall(r"^>+\s*[A-Z]{1,4}\d{0,4}\s*[「\"]([^」\"]+)[」\"]\s*[:：]",
                            disc, re.M):
            hl(x, False)

        ndisc = len(re.findall(r"^>+\s*[A-Z]{1,4}\d{0,4}\s*[「\"：:]", disc, re.M))
        # 讨论里加个「整段写想法」的框（要 serve.py 跑着）：写完 → 追加进 ## Discussion。
        # 不钉在某句话上，就是自由讨论；serve.py 没跑时按钮会提示改走手写（JL 260723）。
        dadd = (f'<div class="dadd" data-file="{esc(q.get("file",""))}">'
                f'<textarea placeholder="Write a thought into the discussion…"></textarea>'
                f'<div class="row"><select></select>'
                f'<button class="dsave" type="button">➕ Add to discussion</button></div></div>')
        folds = det(f"💬 Discussion ({ndisc})",
                    (body(disc) if disc else
                     f'<p class="mut">No discussion yet — add a line under '
                     f'<code>## Discussion</code> in {q["file"]}: '
                     f'<code>&gt; JL: …</code></p>')
                    + dadd)
        nopen = sum(1 for c in cms if not c["done"])
        nlost = sum(1 for c in cms if c["lost"])
        if cms:
            lab = f"💬 Comments ({nopen} open / {len(cms)})"
            if nlost:
                lab += f" · {nlost} unanchored"      # 引文不在正文里；不喊「丢了」（分不清是聊天话还是真被改）
            folds += det(lab, f'<div class="cms" data-cfile="{esc(q.get("file",""))}">'
                         + render_comments(cms) + '</div>', open_=nopen > 0)
        # Why here 不再上台面（它的活并进 ## Question 的要点）；老板子里还写着的收进折叠区
        folds += det("💡 Why here", body(why))
        folds += det("⚖️ Law", body(sec(q["sec"], "Law")))
        folds += det("🧠 Lesson", body(sec(q["sec"], "Lesson")))
        folds += det("📖 Glossary", body(sec(q["sec"], "Glossary")))
        log = sort_log(sec(q["sec"], "Log").strip())
        nlog = len(re.findall(r"^\d{6}(?:\s+\d{3,4})?\s*[·|]", log, re.M))
        folds += det(f"📜 Log ({nlog})", body(log))
        cards.append(
            f'<section class="slide q {cls}" id="{q["id"]}"'
            f' data-title="{esc(q["title"])}" data-file="{esc(q.get("file",""))}"'
            f' data-session="{esc(q.get("session",""))}">'
            f'<div class="qh"><span class="qid">{q["id"]}</span>'
            f'<span class="pill {cls}">{tok} {esc(lab)}</span>'
            f'<span class="mut">{esc(who)}</span>'
            f'<span class="mut">· {inline(q["method"])}</span>'
            + (f'<span class="obadge">💬 {nopen}</span>' if nopen else "")
            # 文件名做成链接：点它直接看这一题的原始 markdown（serve.py 把它当纯文本发）
            + f'<a class="src" href="{esc(q.get("file",""))}" target="_blank"'
            f' title="Open this question\'s raw markdown">📄 {esc(q.get("file",""))}</a>'
            f'<a class="top" href="#top">↑ Index</a></div>'
            # id 后面那个空格是真字符（不是 CSS margin）——复制这行标题时
            # 才不会粘成 QA4Single…，而是 QA4 Single…（JL 260723）
            f'<h2 class="h2"><span class="hid">{q["id"]} </span>{inline(q["title"])}</h2>'
            + ask + bnd + dia
            + f'{fs}{fls}<div class="folds">{folds}</div>{nav}</section>')

    ctx = ""
    if meta["theme"]:
        ctx += (f'<details class="ctx"><summary>🦴 Topic — what this board is about</summary>'
                f'<div class="fb">{body(meta["theme"])}</div></details>')
    if meta["pipeline"]:
        ctx += (f'<details class="ctx"><summary>🔄 Pipeline — how these Qs are ordered</summary>'
                f'<div class="fb">{body(meta["pipeline"])}</div></details>')

    return TPL.format(title=esc(meta["title"]), spine=inline(meta["spine"]),
                      close=inline(meta["close"]), bar=bar, done=done, n=n,
                      ctx=ctx, index=idx, cards="\n".join(cards), js=JS, css=CSS,
                      boarddir=esc(meta.get("dir", "")))


# ── page assets (QB4, JL 260724: build.py was one 2,500-line file) ─────────
# The page's JS and CSS live in assets/ as REAL .js/.css files — editable,
# lintable, node --check-able. build.py INLINES them at build time, so the
# output stays ONE self-contained board.html and the offline invariant holds.
HERE = Path(__file__).resolve().parent
JS = ("\n<script>\n"
      + (HERE / "assets" / "board.js").read_text(encoding="utf-8").rstrip("\n")
      + "\n</script>\n")
CSS = (HERE / "assets" / "board.css").read_text(encoding="utf-8").rstrip("\n")

TPL = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
{css}
</style></head><body class="single" data-board="{boarddir}"><div class="wrap" id="top">

<h1 class="h1">{title}</h1>
<div class="spine"><p><b>🦴 Spine</b> {spine}</p><p><b>🏁 Close when</b> {close}</p></div>
<p class="bar">{bar}  {done}/{n} settled</p>

{ctx}

<h3 class="sec" id="qlist">ALL QUESTIONS<span class="hint">click a row → open it · <a href="#all">show all</a></span></h3>
<div class="idx">{index}</div>

<span id="all"></span>
{cards}

<p class="foot">Content comes from <code>board.md</code> (board-level) and <code>QX-xxx.md</code>
(one per question) in this folder. Edit those, then rebuild:
<code>python3 build.py</code>.<br>Every question is real HTML — the page reads fine
with JavaScript off; the script only adds commenting.</p>
</div>{js}</body></html>
"""

_CJK = re.compile(r"[一-鿿]")


def scrub_cjk_comments(txt):
    """Drop CSS/JS comments that contain CJK from the EMITTED page (the source
    keeps its comments for developers; the output stays fully English — JL 260724).
    Only comments are touched: /*…*/ blocks, and //-to-EOL tails whose line prefix
    has balanced quotes (so a // inside a string is never mistaken for a comment)."""
    txt = re.sub(r"/\*.*?\*/", lambda m: "" if _CJK.search(m.group(0)) else m.group(0),
                 txt, flags=re.S)
    def line(ln):
        i = ln.find("//")
        while i != -1:
            pre = ln[:i]
            if pre.count("'") % 2 == 0 and pre.count('"') % 2 == 0 and pre.count("`") % 2 == 0:
                return pre.rstrip() if _CJK.search(ln[i:]) else ln
            i = ln.find("//", i + 1)
        return ln
    return "\n".join(line(l) if _CJK.search(l) else l for l in txt.split("\n"))


def to_json(meta, qs, warn):
    """`build.py <dir> --json` — the parser as a service (QE3: one grammar,
    two render paths). Emits the same data the HTML is built from, plus the
    derived numbers the index shows, so JSON and HTML cannot disagree."""
    def q_json(q):
        boxes = re.findall(r"^\s*[-*]\s*\[([ xX])\]", sec(q["sec"], "Done when"), re.M)
        cms = parse_comments(sec(q["sec"], "Comments"))
        tok, cls, lab = stinfo(q["state"])
        return dict(id=q["id"], title=q["title"], group=q["group"], file=q["file"],
                    state=q["state"], state_token=tok, state_label=lab,
                    owner=q["owner"], method=q["method"], session=q["session"],
                    done=sum(1 for b in boxes if b.lower() == "x"), total=len(boxes),
                    comments_open=sum(1 for c in cms if not c["done"]),
                    comments_total=len(cms),
                    sections={k: v for k, v in q["sec"].items()})
    return json.dumps({"meta": meta, "questions": [q_json(q) for q in qs],
                       "warnings": warn}, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--json"]
    as_json = "--json" in sys.argv[1:]
    sys.argv = [sys.argv[0]] + args
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    BASE = (src if src.is_dir() else src.parent).resolve()
    if src.is_dir():
        meta, qs, warn = parse_dir(src)
        out = src / "board.html"
    elif src.exists():
        meta, qs, warn = parse_file(src.read_text(encoding="utf-8"))
        out = src.with_suffix(".html")
    else:
        sys.exit(f"not found: {src}")
    if as_json:
        print(to_json(meta, qs, warn))
        sys.exit(0)
    out.write_text(scrub_cjk_comments(render(meta, qs)), encoding="utf-8")
    txt = out.read_text(encoding="utf-8")
    # 真正要保的性质不是「没有 script」，而是「关掉 script 页面照样完整」。
    # 评论层是纯增强，所以改成直接验这一条：剥掉所有 <script> 之后，
    # 每个 Q 仍在，正文仍在。
    bare = re.sub(r"<script.*?</script>", "", txt, flags=re.S)
    assert bare.count('class="slide q') == len(qs), "a Q went missing after stripping JS"
    plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", bare.split("<body", 1)[1])).strip()
    assert len(plain) > 1200, f"only {len(plain)} chars of body left after stripping JS"
    print(f"✅ {out} · {len(qs)} questions · {len(plain)} chars of body survive with JS stripped · {txt.count(chr(60)+'script')} script block(s)")
    for w in warn:
        print(f"⚠️  {w}")
