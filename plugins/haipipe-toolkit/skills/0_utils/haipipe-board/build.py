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
EXT = ("md", "py", "html", "css", "js", "json", "yaml", "yml", "sh", "txt", "ipynb")


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
        if det:
            exp = "".join(f"<p>{inline(x)}</p>" for x in det)
            item = (f'<details class="it"><summary class="{name_cls}">{inline(top)}'
                    f'</summary><div class="bd">{exp}</div></details>')
        else:
            item = f'<div class="{name_cls} nod">{inline(top)}</div>'
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

    order, seen, warn, group = [], set(), [], ""
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

    rows, cur = [], None
    for q in qs:
        if q.get("group") and q["group"] != cur:
            cur = q["group"]
            rows.append(f'<div class="grp">{inline(cur)}</div>')
        # 完成度上色：一条没做 = 白，越接近做完越绿（绿色叠加的透明度 = 完成比例）
        fr = frac_done(q)
        pct = round(fr * 100)
        fill = (f' style="--fill:{fr:.3f}"') if fr > 0 else ""
        rows.append(
            f'<a class="ir {st(q)[1]}" href="#{q["id"]}"{fill} title="{pct}% done">'
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
        ask = (f'<div class="ask"><span class="ql">❓ Question</span>'
               f'{body(sec(q["sec"], "Question"))}</div>')
        # 🚧 Boundary（JL 260723 新增，选填）：这题管什么、更要紧的是不管什么。
        # 不写清「不管什么」，读的人会拿别题的期待来读它 —— 零背景最容易在这儿误解。
        bb = body(sec(q["sec"], "Boundary"))
        bnd = f'<div class="bnd">{chead("🚧 Boundary", bb)}{bb}</div>' if bb else ""
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
                      ctx=ctx, index=idx, cards="\n".join(cards), js=JS,
                      boarddir=esc(meta.get("dir", "")))


JS = r"""
<script>
/* ─────────────────────────────────────────────────────────────
   Comment layer — PURE ENHANCEMENT. The prose is already real HTML;
   this script only ADDS "select -> comment -> highlight right away".
   Strip this script block and the board still reads fine (just no commenting).

   Comments live in localStorage until you press "Sync to md", which writes
   them into each Q file's ## Discussion as:   > JL 「quoted sentence」: text
   ───────────────────────────────────────────────────────────── */
(function () {
  var KEY = 'board-comments:' + location.pathname;
  var UK = 'board-users', WK = 'board-user-last';
  var db = [], users = [];
  try { db = JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { db = []; }
  try { users = JSON.parse(localStorage.getItem(UK) || 'null') || ['JL','RA','CC']; }
  catch (e) { users = ['JL','RA','CC']; }
  var pend = null;

  function mk(tag, id, html) {
    var e = document.createElement(tag); e.id = id; e.innerHTML = html || ''; return e;
  }
  var btn = mk('button', 'cbtn', '\u{1F4AC} Comment');
  var box = mk('div', 'cbox',
    '<div class="qq"></div><textarea placeholder="Write a comment…"></textarea>' +
    '<div class="row"><select></select><span style="flex:1"></span>' +
    '<button class="cx">Cancel</button><button class="ok cs">Save</button></div>' +
    '<input class="nu" placeholder="New initials, e.g. ZW — press Enter">');
  var dock = mk('button', 'cdock', '');
  var panel = mk('div', 'cpanel', '');
  var toast = mk('div', 'ctoast', '');
  [btn, box, dock, panel, toast].forEach(function (e) { document.body.appendChild(e); });

  function save() { localStorage.setItem(KEY, JSON.stringify(db)); marks(); paint(); }
  function say(m) {
    toast.textContent = m; toast.style.display = 'block';
    clearTimeout(toast._t);
    toast._t = setTimeout(function () { toast.style.display = 'none'; }, 3000);
  }

  /* ── highlighting ────────────────────────────────────────────
     Two paths, because they have different information:
       NEW comment  -> we still hold the live Range. Wrap THAT. Always exact,
                       even when the selection crosses <code>/<b> boundaries.
       ON RELOAD    -> the Range is gone, so find the quote by text. Search the
                       section's whole text (concatenated across nodes) with a
                       whitespace-tolerant regex, then map the hit back to
                       (node, offset) so the wrap can span several nodes.
     The old version only did indexOf() inside ONE text node — which is why a
     selection crossing any inline tag silently failed to highlight.          */
  function clearMarks() {
    document.querySelectorAll('span.cmk').forEach(function (e) { e.remove(); });
    document.querySelectorAll('mark.pend').forEach(function (m) {
      var par = m.parentNode;
      while (m.firstChild) par.insertBefore(m.firstChild, m);
      par.removeChild(m); par.normalize();
    });
  }
  function badge(mark, idx) {
    var s = document.createElement('span');
    s.className = 'cmk'; s.textContent = '\u{1F4AC}';
    s.setAttribute('data-i', idx);
    s.title = db[idx].who + ': ' + db[idx].text;
    mark.parentNode.insertBefore(s, mark.nextSibling);
  }
  function wrapRange(r, idx) {
    var m = document.createElement('mark');
    m.className = 'pend'; m.setAttribute('data-i', idx);
    try { r.surroundContents(m); }
    catch (e) { m.appendChild(r.extractContents()); r.insertNode(m); }
    if (!m.parentNode) return false;
    badge(m, idx);
    return true;
  }
  function scan(sec) {
    var w = document.createTreeWalker(sec, NodeFilter.SHOW_TEXT, null);
    var n, s = '', map = [];
    while ((n = w.nextNode())) {
      var p = n.parentNode;
      if (p.closest && p.closest('.folds, .qh, .nav, pre')) continue;
      for (var i = 0; i < n.nodeValue.length; i++) map.push([n, i]);
      s += n.nodeValue;
    }
    return { s: s, map: map };
  }
  function rx(q) {
    var parts = q.trim().split(/\s+/).map(function (x) {
      return x.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    });
    return new RegExp(parts.join('[\\s]*'));
  }
  function findAndWrap(sec, quote, idx) {
    var t = scan(sec);
    if (!t.s) return false;
    var m = rx(quote).exec(t.s);
    if (!m) {                                   // last resort: first 12 chars
      var head = quote.trim().slice(0, 12);
      if (head.length < 4) return false;
      m = rx(head).exec(t.s);
      if (!m) return false;
    }
    var a = t.map[m.index], b = t.map[m.index + m[0].length - 1];
    if (!a || !b) return false;
    var r = document.createRange();
    r.setStart(a[0], a[1]); r.setEnd(b[0], b[1] + 1);
    return wrapRange(r, idx);
  }
  function marks() {
    clearMarks();
    db.forEach(function (c, i) {
      var sec = document.getElementById(c.id);
      c.lost = !(sec && findAndWrap(sec, c.quote, i));
    });
    document.querySelectorAll('span.cmk').forEach(function (s) {
      s.onclick = function () {
        panel.style.display = 'block'; flash(+s.getAttribute('data-i'));
      };
    });
  }
  function flash(i) {
    var el = panel.querySelector('[data-row="' + i + '"]');
    if (!el) return;
    el.scrollIntoView({ block: 'nearest' });
    el.style.background = 'rgba(255,214,0,.28)';
    setTimeout(function () { el.style.background = ''; }, 1300);
  }

  /* ── select -> floating button ───────────────────────────── */
  document.addEventListener('mouseup', function (ev) {
    if (box.contains(ev.target) || panel.contains(ev.target) || ev.target === btn) return;
    setTimeout(function () {
      var s = window.getSelection();
      var txt = s && String(s).trim();
      if (!txt || txt.length < 2 || !s.rangeCount) { btn.style.display = 'none'; return; }
      var node = s.anchorNode;
      node = node.nodeType === 1 ? node : node.parentNode;
      var q = node.closest && node.closest('section.q');
      if (!q) { btn.style.display = 'none'; return; }
      var live = s.getRangeAt(0);
      var r = live.getBoundingClientRect();
      pend = { id: q.id, file: q.getAttribute('data-file') || '',
               quote: txt, range: live.cloneRange() };
      btn.style.left = (r.left + window.scrollX) + 'px';
      btn.style.top = (r.bottom + window.scrollY + 7) + 'px';
      btn.style.display = 'block';
    }, 0);
  });

  function fillWho() {
    var sel = box.querySelector('select'), last = localStorage.getItem(WK) || users[0];
    sel.innerHTML = users.map(function (u) {
      return '<option' + (u === last ? ' selected' : '') + '>' + u + '</option>';
    }).join('') + '<option value="__new">+ new person…</option>';
    sel.onchange = function () {
      var nu = box.querySelector('.nu');
      if (sel.value === '__new') { nu.style.display = 'block'; nu.value = ''; nu.focus(); }
      else { nu.style.display = 'none'; localStorage.setItem(WK, sel.value); }
    };
  }
  box.querySelector('.nu').onkeydown = function (ev) {
    if (ev.key !== 'Enter') return;
    ev.preventDefault();
    var v = this.value.trim().toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 4);
    if (!v) return;
    if (users.indexOf(v) < 0) users.push(v);
    localStorage.setItem(UK, JSON.stringify(users));
    localStorage.setItem(WK, v);
    this.style.display = 'none'; fillWho();
  };

  btn.onclick = function () {
    btn.style.display = 'none';
    fillWho(); box.querySelector('.nu').style.display = 'none';
    box.querySelector('.qq').textContent = pend.quote;
    box.querySelector('textarea').value = '';
    box.style.left = btn.style.left; box.style.top = btn.style.top;
    box.style.display = 'block';
    box.querySelector('textarea').focus();
  };
  box.querySelector('.cx').onclick = function () { box.style.display = 'none'; };
  box.querySelector('.cs').onclick = function () {
    var v = box.querySelector('textarea').value.trim();
    if (!v) return;
    var who = box.querySelector('select').value;
    if (who === '__new') who = users[0];
    localStorage.setItem(WK, who);
    var live = pend.range;
    db.push({ id: pend.id, file: pend.file, quote: pend.quote, who: who, text: v });
    var idx = db.length - 1;
    box.style.display = 'none';
    /* wrap the live range FIRST — guaranteed exact, no text search involved */
    var ok = false;
    try { ok = wrapRange(live, idx); } catch (e) { ok = false; }
    window.getSelection().removeAllRanges();
    db[idx].lost = !ok;
    localStorage.setItem(KEY, JSON.stringify(db));
    if (!ok) marks();
    paint();
    /* 这一次点击本身就是用户手势 —— 直接写盘，不用再点 Sync */
    drain(true).then(function (n) {
      if (n) say((ok ? 'Highlighted and ' : 'Saved (not anchored) and ') +
                 'written to ' + pend.file + (srvOK ? ' — reload to see it rendered'
                                                    : ' — rebuild to render it'));
      else say(ok ? 'Highlighted — ' + db.length + ' pending (no folder access yet)'
                  : 'Saved, but could not anchor it (see ⚠ in the panel)');
    });
  };

  /* ── panel ──────────────────────────────────────────────── */
  function esc(s) { return s.replace(/[&<>]/g, function (c) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]; }); }
  function stamp() {
    var d = new Date(), z = function (n) { return (n < 10 ? '0' : '') + n; };
    return String(d.getFullYear()).slice(2) + z(d.getMonth() + 1) + z(d.getDate()) +
           ' ' + z(d.getHours()) + z(d.getMinutes());
  }
  /* md 里一条评论长这样，[ ] 未解决 / [x] 已解决 */
  function line(c) {
    return '- [ ] ' + c.who + ' 「' + c.quote.replace(/\s+/g, ' ').trim() +
           '」 · ' + (c.when || stamp()) + '\n      ' + c.text.replace(/\n/g, '\n      ');
  }
  function patch() {
    var by = {};
    db.forEach(function (c) { (by[c.file] = by[c.file] || []).push(line(c)); });
    return Object.keys(by).map(function (f) {
      return '### ' + f + '\n' + by[f].join('\n');
    }).join('\n\n');
  }
  function paint() {
    // 这个角标只在「真有没写盘的评论」时才出现（JL 260723）。
    // serve.py 跑着的时候 Save 直接落盘，pending 永远是 0 —— 那就不该在右下角常驻碍眼。
    // 它仍是 serve.py 没跑时的兜底入口，所以不是删掉，是平时藏起来。
    dock.style.display = db.length ? 'block' : 'none';
    dock.textContent = db.length ? ('\u{1F4AC} ' + db.length + ' pending')
                                 : '\u{1F4AC} Comment';
    dock.className = db.length ? 'has' : '';
    panel.innerHTML =
      '<div class="hd"><b>Pending comments</b><span style="flex:1"></span>' +
      '<button class="ok sy">Write now</button>' +
      '<button class="cf">Connect folder</button>' +
      '<button class="cp">Copy</button></div>' +
      (db.length ? db.map(function (c, i) {
        return '<div class="it" data-row="' + i + '"><div class="q">' + c.id +
          (c.lost ? ' <span style="color:var(--mut)">· unanchored</span> ' : ' ') +
          '“' + esc(c.quote.slice(0, 40)) + '”</div><b>' + c.who + '</b> ' +
          esc(c.text) + ' <button data-i="' + i +
          '" class="rm" style="padding:2px 8px">del</button></div>';
      }).join('') : '<div class="it mut">Nothing yet. Select a sentence in the text.</div>') +
      '<div class="hint">Comments are written to the <code>.md</code> the moment you save — ' +
      'once you have connected this board’s folder. Anything listed above has NOT been ' +
      'written yet. ' +
      'each comment into its Q file under <code>## Comments</code> as ' +
      '<code>- [ ] WHO 「quote」 · time</code> — flip it to <code>[x]</code> when solved. ' +
      'Re-run <code>python3 build.py</code> afterwards.</div>';
    panel.querySelectorAll('.rm').forEach(function (b) {
      b.onclick = function () { db.splice(+b.getAttribute('data-i'), 1); save(); };
    });
    panel.querySelector('.sy').onclick = sync;
    panel.querySelector('.cf').onclick = async function () {
      dirH = null; await putDir(undefined);
      var d = await ensureDir(true);
      say(d ? 'Folder connected — comments now save straight to the .md' : 'Not connected');
      if (d) drain(false);
    };
    panel.querySelector('.cp').onclick = function () {
      navigator.clipboard.writeText(patch()).then(function () { say('Patch copied'); });
    };
  }
  dock.onclick = function () {
    panel.style.display = panel.style.display === 'block' ? 'none' : 'block';
  };



  /* ── 写盘：优先让服务器写 ───────────────────────────────────
     板文件在服务器上，浏览器在你自己的机器上（Remote-SSH）——
     File System Access 的文件夹选择器只看得到你本机的盘，够不着这些文件。
     所以第一选择是发个 POST 让服务器写（serve.py），它写完顺手重新生成 html。
     只有服务器不支持时，才退回浏览器直接写文件 / 复制补丁。          */
  var srvOK = null;                       // null=没试过, true/false=试过
  async function post(url, payload) {
    payload.path = location.pathname;
    var r = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' },
                               body: JSON.stringify(payload) });
    if (r.status === 404 || r.status === 501) { srvOK = false; return null; }
    srvOK = true;
    return await r.json();
  }
  async function srvComment(c) {
    try {
      var j = await post('/_board/comment',
        { file: c.file, who: c.who, quote: c.quote, text: c.text, when: c.when || stamp() });
      if (!j) return null;
      return j.ok ? true : j.err;
    } catch (e) { srvOK = false; return null; }
  }
  async function srvResolve(file, quote, done) {
    try {
      var j = await post('/_board/resolve', { file: file, quote: quote, done: done });
      if (!j) return null;
      return j.ok ? true : j.err;
    } catch (e) { srvOK = false; return null; }
  }

  /* ── 兜底：浏览器自己写文件（只在服务器不支持时才用到）
     文件夹句柄记在 IndexedDB 里，授权一次，之后每次保存直接写盘 ──
     浏览器规定：第一次挑文件夹必须由用户点击触发，无法自动。
     但句柄可以存下来；之后每次「Save」本身就是一次点击，够格再申请权限，
     所以正常情况下你一个 session 只会看到一次 Allow。                */
  function idb(fn) {
    return new Promise(function (res) {
      var r = indexedDB.open('board-fs', 1);
      r.onupgradeneeded = function () { r.result.createObjectStore('h'); };
      r.onsuccess = function () {
        var db = r.result, tx = db.transaction('h', 'readwrite');
        fn(tx.objectStore('h'), res);
      };
      r.onerror = function () { res(null); };
    });
  }
  function getDir() { return idb(function (s, res) {
    var g = s.get('dir'); g.onsuccess = function () { res(g.result || null); }; }); }
  function putDir(h) { return idb(function (s, res) { s.put(h, 'dir'); res(1); }); }

  var dirH = null;
  async function ensureDir(ask) {
    if (!window.showDirectoryPicker) return null;
    if (!dirH) dirH = await getDir();
    if (dirH) {
      var st = await dirH.queryPermission({ mode: 'readwrite' });
      if (st === 'granted') return dirH;
      if (ask) {
        st = await dirH.requestPermission({ mode: 'readwrite' });
        if (st === 'granted') return dirH;
      }
      return null;
    }
    if (!ask) return null;
    try {
      dirH = await window.showDirectoryPicker({ mode: 'readwrite' });
      await putDir(dirH);
      return dirH;
    } catch (e) { return null; }
  }

  async function edit(dir, file, fn) {
    var fh = await dir.getFileHandle(file);
    var txt = await (await fh.getFile()).text();
    var next = fn(txt);
    if (next === txt) return false;
    var w = await fh.createWritable();
    await w.write(next); await w.close();
    return true;
  }
  function insertComments(txt, add) {
    if (/^## Comments[^\n]*$/m.test(txt))
      return txt.replace(/^## Comments[^\n]*\n/m, function (mm) { return mm + add + '\n'; });
    if (/\n## Log\b/.test(txt))
      return txt.replace(/\n## Log\b/, '\n## Comments\n' + add + '\n\n## Log');
    return txt.replace(/\s*$/, '') + '\n\n## Comments\n' + add + '\n';
  }
  /* 把已经写盘的从待办里剔掉；写不进去的留着，面板里还看得见 */
  async function drain(ask) {
    if (!db.length) return 0;
    if (srvOK !== false) {                       // 先试服务器
      var n = 0, err = null;
      for (var i = 0; i < db.length; i++) {
        var r = await srvComment(db[i]);
        if (r === true) { db[i].written = 1; n++; }
        else if (typeof r === 'string') { err = r; }
        else break;                              // null = 服务器不支持，退出去走老路
      }
      if (n || srvOK) {
        db = db.filter(function (c) { return !c.written; });
        localStorage.setItem(KEY, JSON.stringify(db));
        paint();
        if (err) say(err);
        if (srvOK) return n;
      }
    }
    var dir = await ensureDir(ask);
    if (!dir) return 0;
    var by = {}, done = 0;
    db.forEach(function (c) { (by[c.file] = by[c.file] || []).push(c); });
    for (var f in by) {
      var add = by[f].map(line).join('\n');
      try {
        await edit(dir, f, function (txt) { return insertComments(txt, add); });
        by[f].forEach(function (c) { c.written = 1; });
        done += by[f].length;
      } catch (e) { console.log('[board] ' + f + ': ' + e.message); }
    }
    db = db.filter(function (c) { return !c.written; });
    localStorage.setItem(KEY, JSON.stringify(db));
    paint();
    return done;
  }

  /* ── 页面上直接把一条评论标成已解决 / 重新打开 ───────────── */
  function esc4re(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
  async function toggle(file, quote, to) {
    if (srvOK !== false) {
      var r = await srvResolve(file, quote, to);
      if (r === true) return true;
      if (typeof r === 'string') { say(r); return false; }
    }
    var dir = await ensureDir(true);
    if (!dir) { say('No folder access — press Connect folder in the panel'); return false; }
    var re = new RegExp('^(-\\s*\\[)[ xX](\\]\\s*[A-Z]{1,4}\\d{0,4}\\s*[「"]' +
                        esc4re(quote) + ')', 'm');
    var hit = false;
    await edit(dir, file, function (txt) {
      if (!re.test(txt)) return txt;
      hit = true;
      return txt.replace(re, '$1' + (to ? 'x' : ' ') + '$2');
    });
    return hit;
  }
  // 讨论框：整段写想法 → POST /_board/discuss → 追加进 ## Discussion → 刷新（JL 260723）
  function wireDadd() {
    var last = localStorage.getItem(WK) || users[0];
    document.querySelectorAll('.dadd').forEach(function (box) {
      var ta = box.querySelector('textarea');
      var sel = box.querySelector('select');
      var btn = box.querySelector('.dsave');
      users.forEach(function (u) { sel.appendChild(new Option(u, u)); });
      sel.value = last;
      btn.onclick = async function () {
        var text = ta.value.trim();
        if (!text) { ta.focus(); return; }
        btn.disabled = true; btn.textContent = '…';
        var j = null;
        try {
          j = await post('/_board/discuss',
            { file: box.getAttribute('data-file'), who: sel.value, text: text });
        } catch (e) { j = null; }
        btn.disabled = false; btn.textContent = '➕ Add to discussion';
        if (j === null) {
          say('serve.py is not running — write > ' + sel.value + ': … into ## Discussion in the md yourself');
          return;
        }
        if (j.ok) { localStorage.setItem(WK, sel.value); location.reload(); }
        else say(j.err || 'write failed');
      };
    });
  }

  function wireResolve() {
    document.querySelectorAll('.cms').forEach(function (box) {
      var file = box.getAttribute('data-cfile');
      box.querySelectorAll('.cm').forEach(function (row) {
        if (row.querySelector('.cres')) return;
        var b = document.createElement('button');
        b.className = 'cres';
        var setLbl = function () {
          b.textContent = row.classList.contains('done') ? 'reopen' : 'mark solved';
        };
        setLbl();
        b.onclick = async function () {
          var to = !row.classList.contains('done');
          b.disabled = true;
          var ok = await toggle(file, row.getAttribute('data-quote'), to);
          b.disabled = false;
          if (!ok) { say('Could not find that line in ' + file); return; }
          row.classList.toggle('done', to);
          var s = row.querySelector('.cs:last-of-type');
          if (s) s.textContent = to ? 'solved' : 'open';
          var bx = row.querySelector('.bx'); if (bx) bx.textContent = to ? '☑' : '☐';
          setLbl();
          say('Written to ' + file + (srvOK ? ' — reload to refresh' : ' — rebuild to refresh'));
        };
        row.querySelector('.cmh').appendChild(b);
      });
    });
  }

  /* ── 手动兜底：面板上的按钮 ───────────────────────────── */
  async function sync() {
    if (!db.length) { say('Nothing pending'); return; }
    if (!window.showDirectoryPicker) {
      navigator.clipboard.writeText(patch());
      say('This browser cannot write files — patch copied instead');
      return;
    }
    var n = await drain(true);
    say(n ? ('Wrote ' + n + ' comment(s) — rebuild to see them rendered')
          : 'Could not write. Grant access to the board folder.');
  }


  /* ── 每题一个对话窗（QD1）──────────────────────────────────
     打开它 = 在服务器上起一个 claude_agent_sdk 会话，作用域锁死在这一题：
     只能读这个板文件夹，只能改这一个 Q 文件（服务器端 can_use_tool 把关）。
     session id 由服务器写回 Q 文件头部的 `session:`，所以关掉再开还接得上。 */
  var chat = document.createElement('div');
  chat.id = 'chat';
  chat.innerHTML =
    '<div class="hd"><span class="qid"></span><span class="ti"></span>' +
    '<button class="term" title="Open this question in a real terminal (same session)">⌨</button>' +
    '<button class="x" title="close">×</button></div>' +
    '<div class="bd"></div><div class="tm"></div>' +
    '<div class="acts"></div>' +
    '<div class="tip"></div>' +
    '<div class="cfg">' +
    '<select class="mdl"><option value="opus">Opus 4.8</option>' +
    '<option value="sonnet">Sonnet 5</option><option value="haiku">Haiku 4.5</option></select>' +
    '<select class="eff"><option>low</option><option>medium</option>' +
    '<option selected>high</option><option>xhigh</option><option>max</option></select>' +
    '<select class="scope" title="Permission tier: Scoped = this question only · Full = all tools + skills, like the CLI">' +
    '<option value="scoped">Scoped</option>' +
    '<option value="full" selected>Full · ask</option>' +
    '<option value="bypass">Full · no ask</option></select>' +
    '<span class="cost"></span></div>' +
    '<div class="sid"></div>' +
    '<div class="ft"><textarea rows="1" placeholder="Ask about this question…"></textarea>' +
    '<button class="send">➤</button></div>';
  document.body.appendChild(chat);
  var cq = null;                                    // 当前挂在哪一题
  var MK = 'board-chat-model', EK = 'board-chat-effort', SK = 'board-chat-scope';
  var CHATK = function (id) { return 'board-chat:' + location.pathname + ':' + id; };

  function chatLoad(id) {
    try { return JSON.parse(localStorage.getItem(CHATK(id)) || '[]'); } catch (e) { return []; }
  }
  function chatSave(id, log) { localStorage.setItem(CHATK(id), JSON.stringify(log)); }
  /* 回复是 markdown，得渲染出来 —— 先转义，再只认几种最常用的写法。
     不引第三方库：这一页坚持自带一切，而且要渲染的只是我们自己 agent 的输出。 */
  function mdEsc(s) {
    return s.replace(/[&<>]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]; });
  }
  function mdInline(s) {
    return mdEsc(s)
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      .replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>')
      .replace(/(^|[\s(])\*([^*\s][^*]*)\*/g, '$1<i>$2</i>');
  }
  function md2html(src) {
    var out = [], fence = null, list = null;
    var flush = function () { if (list) { out.push('</' + list + '>'); list = null; } };
    (src || '').split('\n').forEach(function (ln) {
      if (ln.trim().slice(0, 3) === '```') {
        if (fence === null) { flush(); fence = []; }
        else { out.push('<pre>' + mdEsc(fence.join('\n')) + '</pre>'); fence = null; }
        return;
      }
      if (fence !== null) { fence.push(ln); return; }
      if (!ln.trim()) { flush(); return; }
      var h = ln.match(/^(#{1,6})\s+(.*)$/);
      if (h) { flush(); out.push('<div class="mh">' + mdInline(h[2]) + '</div>'); return; }
      var b = ln.match(/^\s*[-*]\s+(.*)$/);
      if (b) {
        if (list !== 'ul') { flush(); out.push('<ul>'); list = 'ul'; }
        out.push('<li>' + mdInline(b[1]) + '</li>'); return;
      }
      var n = ln.match(/^\s*\d+[.)]\s+(.*)$/);
      if (n) {
        if (list !== 'ol') { flush(); out.push('<ol>'); list = 'ol'; }
        out.push('<li>' + mdInline(n[1]) + '</li>'); return;
      }
      if (list) { out.push('<li class="cont">' + mdInline(ln.trim()) + '</li>'); return; }
      out.push('<p>' + mdInline(ln) + '</p>');
    });
    if (fence !== null) out.push('<pre>' + mdEsc(fence.join('\n')) + '</pre>');
    flush();
    return out.join('');
  }
  function bubble(kind, text) {
    var d = document.createElement('div');
    d.className = 'm ' + kind;
    if (kind === 'cc') { d.classList.add('md'); d.innerHTML = md2html(text); }
    else { d.textContent = text; }
    chat.querySelector('.bd').appendChild(d);
    chat.querySelector('.bd').scrollTop = 1e9;
    return d;
  }
  function setBubble(el, text) {
    if (el.classList.contains('md')) el.innerHTML = md2html(text);
    else el.textContent = text;
  }
  /* 思考过程：一个可折叠块。默认展开着让你看它边想，答案一到就自动收起；
     之后随时点标题再展开。跟 CLI 里的 thinking 一个意思，只是这里能折叠。 */
  function thinkBubble() {
    var d = document.createElement('details');
    d.className = 'tk'; d.open = true;
    d.innerHTML = '<summary>💭 Thinking</summary><div class="tk-body"></div>';
    chat.querySelector('.bd').appendChild(d);
    chat.querySelector('.bd').scrollTop = 1e9;
    return d;
  }

  /* 权限提示 —— 行为跟 Claude Code CLI 一致：只读的自动放行，
     会动东西的弹出来问；「总是允许」只在这一轮这一题里有效。 */
  function askUI(ev) {
    var box = document.createElement('div');
    box.className = 'ask';
    box.innerHTML = '<div class="q">Allow this tool?</div>' +
      '<div class="w"><code></code></div>' +
      '<div class="b"><button class="ok y">Allow once</button>' +
      '<button class="a">Always allow</button><button class="n">Deny</button></div>';
    box.querySelector('code').textContent = ev.brief || ev.tool;
    chat.querySelector('.bd').appendChild(box);
    chat.querySelector('.bd').scrollTop = 1e9;
    var send = function (ok, always) {
      box.querySelector('.b').innerHTML =
        '<span class="mut">' + (ok ? (always ? 'Always allowed' : 'Allowed') : 'Denied') + '</span>';
      fetch('/_board/answer', { method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: ev.id, ok: ok, always: always }) })
        .catch(function () {});
    };
    box.querySelector('.y').onclick = function () { send(true, false); };
    box.querySelector('.a').onclick = function () { send(true, true); };
    box.querySelector('.n').onclick = function () { send(false, false); };
  }
  var FIXALL =
    'Work through every unresolved comment in this question\'s ## Comments ' +
    '(the ones starting with `- [ ]`). For each one:\n' +
    '1. Edit this question\'s body the way the comment asks;\n' +
    '2. Flip that line to `- [x]` and reply on an indented line below it with ' +
    '`>> CC<MMDD>: what you did`;\n' +
    '3. Add one line at the TOP of ## Log: `YYMMDD HHMM · what changed`.\n' +
    'If you cannot do one, or disagree, do NOT flip it to [x] — write why underneath.\n' +
    'End with a short summary of what you changed.';

  function openCount(sec) {
    return sec.querySelectorAll('.cm:not(.done)').length;
  }
  function chatActs(sec) {
    var box = chat.querySelector('.acts');
    box.innerHTML = '';
    var add = function (label, fn, primary) {
      var b = document.createElement('button');
      b.className = 'act' + (primary ? ' pri' : '');
      b.textContent = label; b.onclick = fn;
      box.appendChild(b);
    };
    var n = openCount(sec);
    if (n) add('🔧 Handle ' + n + ' open comment' + (n > 1 ? 's' : ''), function () { chatSend(FIXALL); }, true);
    add('📝 What is this question missing?', function () {
      chatSend('Answer only, do not edit any file: which items in this question\'s ' +
               '## Done when are still unchecked, and what is each one blocked on? ' +
               'One per line.');
    });
    add('↻ Reload', function () { location.reload(); });
  }

  async function chatOpen(sec) {
    cq = { id: sec.id, file: sec.getAttribute('data-file') || '',
           title: sec.getAttribute('data-title') || '' };
    chat.querySelector('.qid').textContent = cq.id;
    chat.querySelector('.ti').textContent = cq.title.slice(0, 30);
    var bd = chat.querySelector('.bd'); bd.innerHTML = '';
    var log = chatLoad(cq.id);
    if (!log.length) bubble('sys', 'This chat is attached to ' + cq.file);
    log.forEach(function (m) { bubble(m.k, m.t); });
    chat.querySelector('.tip').textContent = cq.file;
    /* 这一题的 Claude Code session id —— 抽屉和终端用的是同一个 */
    var sid = sec.getAttribute('data-session') || '';
    var sidbox = chat.querySelector('.sid');
    /* session 归档在 cwd（= serve.py 的 --root，现在是 SPACE 根）下的 project 目录，
       所以要 cd 到 root，不是板文件夹 —— cd 错了 --resume 就找不到这个 session。
       root 精确算法：serve.py 在 <root> + location.pathname 处提供文件，
       所以 root = 板文件夹绝对路径 减去 URL 里的那段目录。不靠 .git/pyproject 猜。 */
    var board = document.body.getAttribute('data-board') || '.';
    var urlDir = location.pathname.replace(/\/[^\/]*$/, '');   // 去掉 board.html
    var root = board;
    if (urlDir && board.slice(-urlDir.length) === urlDir) {
      root = board.slice(0, board.length - urlDir.length) || '/';
    }
    if (sid) {
      sidbox.innerHTML = '<code>' + sid + '</code>';
      // 复制的是一整条能直接跑的命令（带注释说明是哪一题），不是光一个 uuid
      var full = '# ' + cq.id + ' · ' + cq.title + '\n'
               + 'cd "' + root + '" && claude --resume ' + sid;
      var cb = document.createElement('button');
      cb.className = 'act'; cb.textContent = '⌨ Copy: claude --resume';
      cb.title = full;
      cb.onclick = function () {
        navigator.clipboard.writeText(full)
          .then(function () { cb.textContent = 'Copied full command'; });
      };
      sidbox.appendChild(cb);
    } else {
      sidbox.innerHTML = '<span class="mut">No session yet — it appears after your first '
        + 'message and is written into the header of ' + cq.file + '</span>';
    }
    chatActs(sec);
    termView(false); disposeTerm();
    chat.classList.add('on'); document.body.classList.add('chaton');

    /* 第一步：先把浏览器里还没写盘的评论同步过去 —— 不然 chat 读不到它们 */
    var mine = db.filter(function (c) { return c.file === cq.file; }).length;
    if (mine) {
      bubble('sys', 'Writing ' + mine + ' new comment' + (mine > 1 ? 's' : '') + ' into ' + cq.file + '…');
      var n = await drain(true);
      bubble('sys', n ? ('Synced ' + n + '. You can now have it work through the comments.')
                      : 'Sync failed — the comments are still pending.');
      if (n) chat.querySelector('.acts').firstChild &&
             chat.querySelector('.acts').replaceChildren();
      if (n) {
        var b = document.createElement('button');
        b.className = 'act pri'; b.textContent = '🔧 Handle the ' + n + ' just-synced comment' + (n > 1 ? 's' : '');
        b.onclick = function () { chatSend(FIXALL); };
        chat.querySelector('.acts').appendChild(b);
        var r = document.createElement('button');
        r.className = 'act'; r.textContent = '↻ Reload';
        r.onclick = function () { location.reload(); };
        chat.querySelector('.acts').appendChild(r);
      }
    }
    chat.querySelector('textarea').focus();
  }
  chat.querySelector('.x').onclick = function () {
    chat.classList.remove('on'); document.body.classList.remove('chaton'); };
  /* 模型 / effort / 权限档 记在本机；默认 Opus 4.8 · high · 完整·问我 */
  (function () {
    var m = chat.querySelector('.mdl'), e = chat.querySelector('.eff'),
        s = chat.querySelector('.scope');
    m.value = localStorage.getItem(MK) || 'opus';
    e.value = localStorage.getItem(EK) || 'high';
    s.value = localStorage.getItem(SK) || 'full';
    m.onchange = function () { localStorage.setItem(MK, m.value); };
    e.onchange = function () { localStorage.setItem(EK, e.value); };
    s.onchange = function () {
      localStorage.setItem(SK, s.value);
      say(s.value === 'scoped' ? 'Scoped: edits only this question, no skills loaded (cheap)'
        : s.value === 'full' ? 'Full: all tools + skills, asks before touching anything else (like the CLI)'
        : 'Full · no ask: everything auto-approved — this endpoint can now run bash with no prompt, be careful');
    };
  })();

  var inflight = null;                    // 正在跑的那一轮：{ctrl, file}
  async function chatStop() {
    if (!inflight) return;
    try {
      await fetch('/_board/stop', { method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: location.pathname, file: inflight.file }) });
      bubble('sys', 'Stop signal sent — it will wrap up at the next message…');
    } catch (e) { /* 服务器都不通了，直接放弃等待 */ }
    inflight.ctrl.abort();                // 浏览器这边立刻不等了
  }
  function chatBusy(on) {
    var btn = chat.querySelector('.send');
    btn.textContent = on ? '⏹' : '➤';
    btn.title = on ? 'Stop this turn' : 'Send';
    btn.classList.toggle('stop', on);
    btn.disabled = false;                 // 忙的时候也能点 —— 那是停止键
    chat.querySelector('textarea').disabled = on;
  }

  async function chatSend(preset) {
    var ta = chat.querySelector('textarea'), btn = chat.querySelector('.send');
    if (inflight) return chatStop();       // 正在跑 → 这一下是「停」
    var msg = (preset || ta.value).trim();
    if (!msg || !cq) return;
    if (!preset) ta.value = '';
    chatBusy(true);
    var log = chatLoad(cq.id);
    bubble('you', msg); log.push({ k: 'you', t: msg }); chatSave(cq.id, log);
    var wait = bubble('sys', '…thinking (click ⏹ again to stop)');
    var ctrl = new AbortController();
    inflight = { ctrl: ctrl, file: cq.file };
    try {
      var r = await fetch('/_board/chat', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        signal: ctrl.signal,
        body: JSON.stringify({ path: location.pathname, file: cq.file, message: msg,
          stream: true,
          model: chat.querySelector('.mdl').value,
          effort: chat.querySelector('.eff').value,
          scope: chat.querySelector('.scope').value })
      });
      /* 服务器一行一条 JSON 地往下发，边收边显示 */
      var rd = r.body.getReader(), dec = new TextDecoder(), buf = '';
      var cur = null, acc = '', j = { ok: true };
      var thinkEl = null, thinkAcc = '';        // 思考过程 → 一个可折叠块
      while (true) {
        var ch = await rd.read();
        if (ch.done) break;
        buf += dec.decode(ch.value, { stream: true });
        var lines = buf.split('\n'); buf = lines.pop();
        for (var i = 0; i < lines.length; i++) {
          if (!lines[i].trim()) continue;
          var ev; try { ev = JSON.parse(lines[i]); } catch (e) { continue; }
          if (ev.t === 'think') {                 // 思考过程 → 折叠块，边想边展开
            wait.remove();
            if (!thinkEl) thinkEl = thinkBubble();
            thinkAcc += ev.text;
            thinkEl.querySelector('.tk-body').textContent = thinkAcc;
            chat.querySelector('.bd').scrollTop = 1e9;
          } else if (ev.t === 'delta') {          // 逐字答案
            wait.remove();
            if (thinkEl && thinkEl.open) thinkEl.open = false;   // 答案一来就收起思考
            if (!cur) cur = bubble('cc', '');
            acc += ev.text;
            setBubble(cur, acc);
            chat.querySelector('.bd').scrollTop = 1e9;
          } else if (ev.t === 'text') {           // 整段（没开逐字时）
            wait.remove();
            if (!cur) cur = bubble('cc', '');
            acc += (acc ? '\n\n' : '') + ev.text;
            setBubble(cur, acc);
            chat.querySelector('.bd').scrollTop = 1e9;
          } else if (ev.t === 'ask') {
            /* 跟 CLI 一样的权限提示：它想动东西，先问你 */
            wait.remove();
            cur = null;                       // 批准之后的输出另起一条气泡
            askUI(ev);
          } else if (ev.t === 'tool') {
            wait.textContent = '…' + ev.name;
          } else if (ev.t === 'done') {
            j = Object.assign({ ok: true }, ev);
            if (ev.text && cur) { acc = ev.text; setBubble(cur, acc); }
          }
        }
      }
      wait.remove();
      var txt = j.ok ? (acc || j.text || '(no text reply — it may have only used tools)')
                     : ('⚠ ' + (j.err || 'failed'));
      if (j.stopped) txt = txt + '\n(you stopped this turn, so it may be unfinished)';
      if (!cur) bubble('cc', txt);
      log.push({ k: 'cc', t: txt }); chatSave(cq.id, log);
      if (j.ok) {
        var bits = [];
        if (j.model) bits.push(j.model.replace('claude-', '') + ' / ' + j.effort);
        if (j.scope) bits.push({scoped:'scoped',full:'full·ask',bypass:'full·no-ask'}[j.scope] || j.scope);
        if (j.usd != null) bits.push('$' + Number(j.usd).toFixed(3));
        if (j.denied && j.denied.length) bits.push('blocked ' + j.denied.length + ' tool call' + (j.denied.length > 1 ? 's' : ''));
        // 只有真的写了盘上文件，才说「已写盘」并给刷新按钮 —— 读一读不该出现
        if (j.wrote) {
          bits.push('written to disk');
          bubble('sys', bits.join(' · '));
          var rb = document.createElement('button');
          rb.className = 'act pri'; rb.textContent = '↻ Reload to see the result';
          rb.onclick = function () { location.reload(); };
          chat.querySelector('.acts').replaceChildren(rb);
        } else if (bits.length) {
          bubble('sys', bits.join(' · '));   // 只报模型/花费，不提写盘、不换按钮
        }
      }
    } catch (e) {
      wait.remove();
      bubble('sys', e.name === 'AbortError'
        ? 'Stopped waiting. The server got the stop signal too.'
        : '⚠ ' + e.message);
    }
    inflight = null; chatBusy(false); ta.focus();
  }
  chat.querySelector('.send').onclick = chatSend;
  chat.querySelector('textarea').addEventListener('keydown', function (ev) {
    if (ev.key === 'Enter' && !ev.shiftKey) { ev.preventDefault(); chatSend(); }
  });

  /* ── ⌨ 真终端：同一个 session 换个窗口 ────────────────────────
     LAW（JL 260723）：一个 session 同时只能有一个窗口。
     抽屉和终端读写的是磁盘上同一个 .jsonl，两边同时开会互相盖或者 fork 出第二段历史。
     所以开终端前服务器先看抽屉在不在用；从终端切回来时要「交回 session」。 */
  var termOn = false;
  function termView(on) {
    termOn = on;
    chat.querySelector('.tm').style.display = on ? 'block' : 'none';
    ['.bd', '.acts', '.cfg', '.sid', '.ft', '.tip'].forEach(function (s) {
      var e = chat.querySelector(s); if (e) e.style.display = on ? 'none' : '';
    });
    var b = chat.querySelector('.term');
    b.textContent = on ? '💬' : '⌨';
    b.title = on ? 'Back to the web chat (hands the session back)' : 'Open this question in a real terminal (same session)';
    if (on && termT) setTimeout(fitTerm, 0);
  }

  /* ── xterm.js 直接画在抽屉里（不再用 iframe，closer to myrlin）──────
     终端后端仍是 serve.py 起的 ttyd；这里我们自己拿 xterm 连它的 WebSocket，
     省掉 iframe 那层（CSP、加载慢、控制不了）。ttyd 的 WS 子协议：
       连接子协议 'tty'；开场发 JSON auth；输入 '0'+data；输出帧首字节 '0'。 */
  var termT = null, termWS = null, xtermP = null;
  function loadXterm() {
    if (xtermP) return xtermP;
    xtermP = new Promise(function (res, rej) {
      var css = document.createElement('link');
      css.rel = 'stylesheet'; css.href = '/_board/asset/xterm.css';
      document.head.appendChild(css);
      var s = document.createElement('script');
      s.src = '/_board/asset/xterm.min.js';
      s.onload = function () { res(window.Terminal); };
      s.onerror = function () { rej(new Error('xterm.js failed to load (is serve.py running?)')); };
      document.head.appendChild(s);
    });
    return xtermP;
  }
  function fitTerm() {
    if (!termT) return;
    var host = chat.querySelector('.tm');
    var w = host.clientWidth, h = host.clientHeight;
    if (w < 40 || h < 40) return;
    var cols = Math.max(20, Math.floor((w - 16) / 8.4));
    var rows = Math.max(6, Math.floor((h - 12) / 17));
    try { termT.resize(cols, rows); } catch (e) {}
  }
  var termKey = null, termRetry = 0, termPing = null, termClosing = false;
  function disposeTerm() {
    termClosing = true;                       // an intentional close never reconnects
    if (termPing) { clearInterval(termPing); termPing = null; }
    try { if (termWS) termWS.close(); } catch (e) {}
    try { if (termT) termT.dispose(); } catch (e) {}
    termWS = null; termT = null; termKey = null; termRetry = 0;
    var host = chat.querySelector('.tm'); if (host) host.innerHTML = '';
  }
  /* smoothness (QD3 260724): the WS is rebuilt on drops, the TERMINAL is not —
     scrollback survives a reconnect; the post-auth resize (SIGWINCH) makes
     claude repaint. Keepalive = a same-size resize op every 30s, so an idle
     relay/proxy never reaps the pipe. */
  function connectWS(key) {
    var proto = location.protocol === 'https:' ? 'wss://' : 'ws://';
    var ws = new WebSocket(proto + location.host + '/_term/' + key + '/ws', ['tty']);
    ws.binaryType = 'arraybuffer';
    termWS = ws;
    window.__wsDbg = { state: 'new', msgs: 0, err: null };
    ws.onopen = function () {
      window.__wsDbg.state = 'open';
      termRetry = 0;
      // the ttyd handshake: auth as one message, size as another (merged = no output)
      ws.send(JSON.stringify({ AuthToken: '' }));
      ws.send(JSON.stringify({ columns: termT.cols || 100, rows: termT.rows || 30 }));
      if (termPing) clearInterval(termPing);
      termPing = setInterval(function () {           // keepalive: same-size resize op
        if (ws.readyState === 1 && termT)
          ws.send('1' + JSON.stringify({ columns: termT.cols, rows: termT.rows }));
      }, 30000);
    };
    ws.onmessage = function (ev) {
      window.__wsDbg.msgs++;
      var d = ev.data;
      if (typeof d === 'string') { if (d.charCodeAt(0) === 48) termT.write(d.slice(1)); return; }
      var b = new Uint8Array(d);
      if (b[0] === 48) termT.write(new TextDecoder().decode(b.subarray(1)));
    };
    ws.onerror = function (e) { window.__wsDbg.err = 'error'; };
    ws.onclose = function (e) {
      window.__wsDbg.state = 'closed:' + (e && e.code);
      if (termPing) { clearInterval(termPing); termPing = null; }
      if (termClosing || !termOn || !termT) return;  // closed on purpose → stay quiet
      if (termRetry >= 6) {
        termT.write('\r\n\x1b[90m[disconnected — click ⌨ twice to reopen]\x1b[0m\r\n');
        return;
      }
      var wait = Math.min(15000, 1000 * Math.pow(2, termRetry));
      termRetry += 1;
      termT.write('\r\n\x1b[90m[connection lost — reconnecting in ' +
                  Math.round(wait / 1000) + 's (' + termRetry + '/6)]\x1b[0m\r\n');
      setTimeout(function () {
        if (!termClosing && termOn && termT && termKey === key) connectWS(key);
      }, wait);
    };
    termT.onData(function (s) { if (ws.readyState === 1) ws.send('0' + s); });
    termT.onResize(function (sz) {
      if (ws.readyState === 1) ws.send('1' + JSON.stringify({ columns: sz.cols, rows: sz.rows }));
    });
  }
  async function mountTerm(key) {
    await loadXterm();
    disposeTerm();
    var host = chat.querySelector('.tm');
    termT = new window.Terminal({
      fontSize: 13, fontFamily: 'Menlo, "SF Mono", ui-monospace, monospace',
      cursorBlink: true, convertEol: false, scrollback: 4000,
      theme: { background: '#0b0d12', foreground: '#e8e8e6', cursor: '#6ea8f0' }
    });
    termT.open(host);
    try { window.__boardTerm = termT; } catch (e) {}   // debug handle, inspect from the console
    fitTerm();
    termClosing = false; termKey = key; termRetry = 0;
    connectWS(key);
    setTimeout(function () { termT && termT.focus(); }, 50);
  }
  window.addEventListener('resize', function () { if (termOn) fitTerm(); });
  // fit when the drawer pane itself changes size, not only the window (debounced)
  (function () {
    var host = chat.querySelector('.tm'), t = null;
    if (window.ResizeObserver && host)
      new ResizeObserver(function () {
        clearTimeout(t); t = setTimeout(function () { if (termOn) fitTerm(); }, 150);
      }).observe(host);
  })();

  async function termRelease(file) {
    disposeTerm();
    if (!file) return;
    try {
      await fetch('/_board/release', { method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: location.pathname, file: file }) });
    } catch (e) { /* 服务器没了也要让界面回得来 */ }
  }
  /* 关整个板页面时，如果抽屉里还开着终端，用 beacon 通知服务器收掉。 */
  window.addEventListener('pagehide', function () {
    if (termOn && cq && cq.file && navigator.sendBeacon) {
      navigator.sendBeacon('/_board/release',
        new Blob([JSON.stringify({ path: location.pathname, file: cq.file })],
                 { type: 'application/json' }));
    }
  });
  async function termOpen(quiet) {
    if (!cq) return false;
    if (!quiet) say('Starting a terminal for this question…');
    try {
      var r = await fetch('/_board/term', { method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: location.pathname, file: cq.file }) });
      var j = await r.json();
      if (!j.ok) { say('⚠ ' + j.err); return false; }
      termView(true);
      await mountTerm(j.key);
      if (!quiet) say(j.reused ? 'Reattached to the terminal already running'
                               : (j.note || 'Terminal ready'));
      return true;
    } catch (e) { say('⚠ ' + e.message); return false; }
  }
  // pre-warm on hover: pull the 480KB xterm.js while the pointer is still on ⌨,
  // so the click feels instant. Assets only — never POST /_board/term here (it takes HOLD).
  chat.querySelector('.term').addEventListener('mouseenter', function () {
    loadXterm().catch(function () {});
  });
  chat.querySelector('.term').onclick = async function () {
    if (!cq) return;
    if (termOn) {                                  // 切回抽屉 = 交回 session
      await termRelease(cq.file);
      termView(false);
      say('Terminal closed, session handed back');
      return;
    }
    await termOpen(false);
  };

  /* ── 面板跟着题走（JL 260723）────────────────────────────────
     换一题 = 换一个 session。抽屉开着的时候，切到哪一题它就跟到哪一题：
     聊天记录换成那一题的，session id 换成那一题的；
     本来在终端模式的话，先把上一题的 session 交回去，再开新那一题的终端。 */
  async function follow() {
    var id = (location.hash || '').slice(1);
    var sec = id && document.getElementById(id);
    if (!sec || !sec.classList.contains('q')) return;
    if (!chat.classList.contains('on')) return;     // 抽屉没开就别多事
    if (cq && cq.id === sec.id) return;             // 还是同一题
    var wasTerm = termOn, oldFile = cq && cq.file;
    if (wasTerm) await termRelease(oldFile);        // 一个 session 一个窗口
    await chatOpen(sec);                            // 重新绑到新题（会重置成聊天视图）
    if (wasTerm) await termOpen(true);              // 本来在终端 → 跟着切过去
    say('Now following ' + sec.id);
  }
  window.addEventListener('hashchange', follow);

  /* 每张卡片的头部挂一个入口 */
  document.querySelectorAll('section.q').forEach(function (sec) {
    var b = document.createElement('button');
    b.className = 'chatbtn'; b.textContent = '\u{1F916} Chat';
    b.onclick = function () {
      // 顺便把 URL 也切到这一题，这样 follow() 和「回目录」都对得上
      if (location.hash !== '#' + sec.id) location.hash = sec.id;
      chatOpen(sec);
    };
    var qh = sec.querySelector('.qh');
    if (qh) qh.appendChild(b);
  });

  /* 右下角悬浮的「💬 Chat」—— 打开当前正在看的这一题的聊天框。
     只在聚焦看某一题时出现（CSS 控制），点它就开这一题的抽屉。 */
  var fab = document.createElement('button');
  fab.id = 'chatfab';
  fab.innerHTML = '\u{1F916} Chat';
  fab.onclick = function () {
    var id = (location.hash || '').slice(1);
    var sec = id && document.getElementById(id);
    if (sec && sec.classList.contains('q')) chatOpen(sec);
  };
  document.body.appendChild(fab);

  marks(); paint(); wireResolve(); wireDadd();
})();

/* ── section「expand / collapse all」──────────────────────────────
   Pure enhancement over native <details>. Strip this block and every
   item is still individually openable; all text stays in the DOM. */
document.addEventListener('click', function (ev) {
  var b = ev.target.closest && ev.target.closest('.secall');
  if (!b) return;
  var sec = b.closest('.col, .f');
  if (!sec) return;
  var open = b.getAttribute('data-open') !== '1';
  sec.querySelectorAll('details.it').forEach(function (d) { d.open = open; });
  b.setAttribute('data-open', open ? '1' : '0');
  var lbl = b.querySelector('.lbl');
  if (lbl) lbl.textContent = open ? 'collapse all' : 'expand all';
});
</script>
"""

TPL = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
/* palette + type follow html-ppt's academic-report; layout is body.single
   (base.css's own no-JS mode) so every section is visible without any script. */
:root{{--bg:#fbfbf9;--fg:#1c1c1c;--mut:#7c7c78;--line:#e4e4df;--card:#fff;--pre:#f4f4f0;
 --accent:#1f5aa8;--ra:#15803d;--todo:#c23b3b;--wip:#b45309;--done:#15803d;--hold:#8a8a8a}}
@media(prefers-color-scheme:dark){{:root{{--bg:#161719;--fg:#e8e8e6;--mut:#9a9a97;
 --line:#2c2e33;--card:#1d1f23;--pre:#111214;--accent:#6ea8f0;--ra:#5fc98a;
 --todo:#e0736e;--wip:#e0a458;--done:#5fc98a}}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);
 font:16px/1.7 -apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif}}
.wrap{{max-width:820px;margin:0 auto;padding:34px 22px 90px}}
.h1{{font-size:26px;line-height:1.35;margin:0 0 10px;font-weight:700}}
.spine{{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--accent);
 border-radius:10px;padding:14px 17px;margin:0 0 14px}}
.spine p{{margin:5px 0}}
.bar{{font:13px ui-monospace,Menlo,monospace;color:var(--mut);margin:0 0 22px}}
details.ctx{{border:1px solid var(--line);border-radius:10px;background:var(--card);
 padding:10px 15px;margin:8px 0}}
details.ctx>summary{{cursor:pointer;font-size:15px;font-weight:600;list-style:none}}
details>summary::-webkit-details-marker{{display:none}}
details>summary::before{{content:"▸ ";color:var(--mut)}}
details[open]>summary::before{{content:"▾ "}}
h3.sec{{font-size:12.5px;letter-spacing:.09em;color:var(--mut);margin:30px 0 10px;font-weight:600}}
h3.sec .hint{{float:right;font-weight:400;letter-spacing:0;text-transform:none}}

/* 默认（#top，没选中任何一题）：只显示目录，不把 10 张卡片全铺出来。
   要一次看全部 / 想 Ctrl-F 全文，点目录旁边的 “show all”（跳到 #all）。 */
body:not(:has(.q:target)):not(:has(#all:target)) .q{{display:none}}
body:has(#all:target) h3.sec .hint{{visibility:hidden}}

/* ── 单题聚焦：纯 CSS，零脚本 ────────────────────────────────
   URL 命中某个 #Qn 时（点目录一行就会），把目录、进度条和其他题全收起来，
   屏幕上只剩这一题。点「☰ 全部」回到 #top，:target 落空，一切复原。
   :has() 是纯选择器，不需要 JS。 */
.nav{{display:none}}
body:has(.q:target) .idx,
body:has(.q:target) .bar,
body:has(.q:target) h3.sec{{display:none}}
body:has(.q:target) .foot,
body:has(.q:target) .q{{display:none}}
/* 必须比上面那条更特指，否则被选中的那题会连自己一起藏掉 */
body:has(.q:target) .q:target{{display:block;margin-top:6px}}
.q:target .nav{{display:flex;gap:10px;align-items:center;margin-top:20px;
 padding-top:13px;border-top:1px solid var(--line)}}
.nav a{{color:var(--accent);text-decoration:none;font-size:14px;
 border:1px solid var(--line);border-radius:8px;padding:6px 13px}}
.nav a:hover{{border-color:var(--accent)}}
.nav .all{{margin:0 auto;color:var(--mut)}}
.q:target .top{{display:none}}
.ir{{position:relative;display:flex;gap:10px;align-items:baseline;padding:9px 13px;
 border:1px solid var(--line);border-left:4px solid var(--mut);border-radius:9px;margin:6px 0;
 text-decoration:none;color:var(--fg);background:var(--card);overflow:hidden;--fill:0}}
/* 完成度上色：白底 → 绿。绿色叠加层的透明度 = 完成比例（--fill 0..1）。
   从左往右填，像进度条，但很淡，不抢正文。 */
.ir::before{{content:"";position:absolute;inset:0;pointer-events:none;
 background:linear-gradient(90deg,
   rgba(21,128,61,calc(var(--fill) * .30)),
   rgba(21,128,61,calc(var(--fill) * .30)) calc(var(--fill) * 100%),
   transparent calc(var(--fill) * 100%))}}
.ir > *{{position:relative;z-index:1}}
.ir:hover{{border-color:var(--accent)}}
h3.sec .hint a{{color:var(--accent);text-decoration:none}}
.ir.todo{{border-left-color:var(--todo)}}.ir.wip{{border-left-color:var(--wip)}}
.ir.done{{border-left-color:var(--done)}}.ir.hold{{border-left-color:var(--hold)}}
/* 索引里的分组标题：放大 + 底下一条线，跟 Q 页里的节标题（.ch）同一套语言（JL 260723） */
.grp{{font-size:16px;font-weight:700;color:var(--fg);letter-spacing:-.01em;
 margin:26px 0 9px;padding:0 0 6px 2px;border-bottom:1px solid var(--line)}}
.grp:first-of-type{{margin-top:8px}}
.src{{font:11.5px ui-monospace,Menlo,monospace;color:var(--mut);opacity:.7;text-decoration:none}}
a.src:hover{{opacity:1;color:var(--accent);text-decoration:underline}}
.ir .i{{font:12px ui-monospace,Menlo,monospace;color:var(--mut);min-width:24px}}
.ir .t{{flex:1}} .ir .w{{font-size:12.5px;color:var(--mut)}}
.slide.q{{border:1px solid var(--line);border-left:4px solid var(--mut);border-radius:12px;
 background:var(--card);padding:20px 22px;margin:18px 0;scroll-margin-top:16px}}
.slide.q.todo{{border-left-color:var(--todo)}}.slide.q.wip{{border-left-color:var(--wip)}}
.slide.q.done{{border-left-color:var(--done)}}.slide.q.hold{{border-left-color:var(--hold)}}
.qh{{display:flex;gap:9px;align-items:center;flex-wrap:wrap;font-size:12.5px;margin-bottom:4px}}
.qid{{font:13px ui-monospace,Menlo,monospace;color:var(--mut)}}
.pill{{padding:2px 10px;border-radius:999px;border:1px solid var(--mut);color:var(--mut)}}
.pill.todo{{border-color:var(--todo);color:var(--todo)}}
.pill.wip{{border-color:var(--wip);color:var(--wip)}}
.pill.done{{border-color:var(--done);color:var(--done)}}
.pill.hold{{border-color:var(--hold);color:var(--hold)}}
.top{{margin-left:auto;color:var(--mut);text-decoration:none;font-size:12px}}
.top:hover{{color:var(--accent)}}
.h2{{font-size:22px;line-height:1.4;margin:4px 0 14px;font-weight:700}}
/* ## Question 现在是「一段话 + 几个要点」：.ask 只是容器，
   第一段当大字领句，要点跟在下面按正常字号（JL 260723 改版） */
.ask{{padding-left:13px;border-left:3px solid var(--accent);margin:0 0 18px}}
.ask p{{margin:0 0 6px}}
.ask>p:first-of-type{{font-size:18px;line-height:1.55;margin:0 0 9px}}
/* 🚧 Boundary：这题管什么 / 不管什么。中性灰边，跟黄(现在)绿(目标)区分开 */
.bnd{{border:1px solid var(--line);border-left:3px solid var(--mut);border-radius:10px;
 padding:12px 15px;background:var(--bg);margin:0 0 16px}}
/* 嵌进来的 excalidraw 画布：一行只放一个分享链接就会变成这个 */
.xcal{{margin:12px 0}}
.xcal iframe{{width:100%;height:440px;border:1px solid var(--line);border-radius:10px;
 background:var(--card);display:block}}
.xcal .xopen{{display:inline-block;margin-top:6px;font-size:12.5px}}
.q:target .xcal iframe{{height:520px}}
/* 📁 Files：这题牵动哪些文件。蓝边（跟 Question 一个色系＝「指向真东西」） */
.fls{{border:1px solid var(--line);border-left:3px solid var(--accent);border-radius:10px;
 padding:12px 15px;background:var(--bg);margin:16px 0 0}}
.fls code{{font-size:12.5px}}
/* Question 段的小标签：跟 📍 Now / 🎯 Done when 一样显示段名，不只剩一个 ❓（JL 260723） */
.ql{{display:block;font-size:12px;font-weight:600;color:var(--accent);
 letter-spacing:.02em;margin:0 0 5px}}
.q:target .ql{{font-size:13px;margin:0 0 8px}}
.f{{margin:16px 0}}
.f p,.fbd p{{margin:0 0 4px}}

/* 现在 vs 算做完：上下叠，不左右分栏 —— 两边长短不一时并排会空掉半边 */
.cmp{{display:grid;grid-template-columns:1fr;gap:12px;margin:16px 0}}
.col{{border:1px solid var(--line);border-radius:10px;padding:12px 15px;background:var(--bg)}}

/* 勾选清单：md 里写 - [ ] / - [x] */
.ck{{display:flex;gap:9px;align-items:flex-start;margin:7px 0;line-height:1.65}}
.ck .ct{{font-weight:600}}
.ck.on .ct{{font-weight:600;opacity:.85}}
.ck .bd{{padding-left:0;margin-top:2px}}
.ck .bx{{flex:0 0 auto;color:var(--mut);font-size:15px;line-height:1.6}}
.ck.on{{color:var(--mut)}}
.ck.on .bx{{color:var(--done)}}

.cmt.cc{{border-color:var(--mut)}}
.cmt.u0{{border-color:#8b5cf6}}.cmt.u0 b{{color:#8b5cf6}}
.cmt.u1{{border-color:#0891b2}}.cmt.u1 b{{color:#0891b2}}
.cmt.u2{{border-color:#c2410c}}.cmt.u2 b{{color:#c2410c}}
.cmt.u3{{border-color:#be185d}}.cmt.u3 b{{color:#be185d}}
mark.pend{{background:rgba(255,214,0,.30);outline:1px dashed rgba(180,83,9,.5)}}
.cmk{{cursor:pointer;font-size:.78em;vertical-align:super;margin-left:2px;opacity:.85}}
.cmk:hover{{opacity:1}}
#cdock.has{{background:var(--wip)}}
#ctoast{{position:fixed;left:50%;transform:translateX(-50%);bottom:26px;z-index:44;
 display:none;background:var(--fg);color:var(--bg);padding:9px 17px;border-radius:9px;
 font-size:13.5px;box-shadow:0 6px 20px rgba(0,0,0,.3)}}
#cbox .nu{{width:100%;margin-top:7px;border:1px solid var(--line);border-radius:7px;
 padding:6px 8px;font:13px inherit;background:var(--bg);color:var(--fg);display:none}}

/* 组标题（整行加粗）：领着下面一串 item 的一句话。🔹 图标 + 略大 + 上间距，
   夹在节标题(.ch, 带下划线) 和 item 名字(.bt, ▸) 中间一层（JL 260723）。 */
.gt{{display:flex;align-items:baseline;gap:7px;font-weight:700;font-size:14.5px;
 color:var(--fg);margin:16px 0 7px;letter-spacing:-.01em}}
.gt .gi{{font-size:.9em;flex:0 0 auto}}
.gt:first-child{{margin-top:2px}}       /* 紧跟节标题的第一句，不留大空档 */
.q:target .gt{{font-size:16.5px;margin:22px 0 9px}}
.q:target .gt:first-child{{margin-top:4px}}

/* 要点式：一个小标题 + 下面的解释（JL 260723）。解释收进 <details>，想看再点开 */
.blt{{margin:11px 0}}
.blt .bt{{font-weight:600;position:relative;padding-left:15px}}
.blt .bt:before{{content:"▸";position:absolute;left:0;color:var(--accent);transition:transform .12s}}
.blt summary.bt{{list-style:none;cursor:pointer}}
.blt summary.bt::-webkit-details-marker{{display:none}}
.blt summary.bt:hover{{color:var(--accent)}}
.blt details.it[open]>summary.bt:before{{content:"▾"}}
.blt .bt.nod:before{{opacity:.45}}          /* 没有解释：▸ 淡一点，示意点不开 */
.blt .bd{{padding-left:15px;margin-top:2px}}
.blt .bd p{{margin:0 0 3px;color:var(--mut)}}
.q:target .blt{{margin:15px 0}}
.q:target .blt .bd p{{font-size:15.5px;line-height:1.7}}

/* 代码块也默认收起（JL 260723）：合着时只是一行 “</> code · N 行”，点开才铺代码。
   带 .it → 跟节标题的 expand-all 一起开合。脚本剥掉后照样点得开，代码一直在 DOM。 */
details.codef{{margin:10px 0}}
details.codef>summary{{list-style:none;cursor:pointer;padding:2px 0;
 font:12px ui-monospace,Menlo,monospace;color:var(--mut)}}
details.codef>summary::-webkit-details-marker{{display:none}}
details.codef>summary:before{{content:"▸ ";color:var(--accent)}}
details.codef[open]>summary:before{{content:"▾ "}}
details.codef>summary:hover{{color:var(--accent)}}
details.codef>pre{{margin:7px 0 0}}

/* 勾选清单里的 item：名字被 ☑/☐ 领着，caret 放在行尾示意可展开 */
.ck .itw{{flex:1;min-width:0}}
.ck summary.ct{{list-style:none;cursor:pointer;position:relative;padding-right:16px}}
.ck summary.ct::-webkit-details-marker{{display:none}}
.ck summary.ct:after{{content:"▸";position:absolute;right:0;top:0;color:var(--accent);font-size:.82em}}
.ck details.it[open]>summary.ct:after{{content:"▾"}}
.ck summary.ct:hover{{color:var(--accent)}}

/* ── 每题一个对话窗（QD1）──────────────────────────────────── */
.chatbtn{{margin-left:6px;border:1px solid var(--line);background:var(--bg);color:var(--mut);
 border-radius:7px;padding:2px 10px;font:11.5px inherit;cursor:pointer}}
.chatbtn:hover{{border-color:var(--accent);color:var(--accent)}}
/* 右侧整条抽屉（照 haichat-inlab 的 drawer）：占满高度，页面往左让位。
   打开它的图标是右下角那个悬浮的 💬 Chat（#chatfab）。 */
#chat{{position:fixed;top:0;right:0;bottom:0;z-index:60;width:min(440px,92vw);
 display:none;flex-direction:column;background:var(--card);
 border-left:1px solid var(--line);box-shadow:-12px 0 34px rgba(0,0,0,.20)}}
#chat.on{{display:flex}}
body.chaton{{padding-right:min(440px,92vw)}}
@media(max-width:820px){{body.chaton{{padding-right:0}}}}

/* 打开聊天框的悬浮图标：右下角，只在看某一题时出现（JL 260723） */
#chatfab{{position:fixed;right:20px;bottom:20px;z-index:55;display:none;
 align-items:center;gap:7px;background:var(--accent);color:#fff;border:none;
 border-radius:999px;padding:11px 18px;font-size:14px;font-weight:600;cursor:pointer;
 box-shadow:0 6px 20px rgba(0,0,0,.28)}}
#chatfab:hover{{filter:brightness(1.06)}}
body:has(.q:target):not(.chaton) #chatfab{{display:inline-flex}}
/* 聚焦看一题时，卡片头里那个小 💬 Chat 让位给悬浮图标；平铺/展开视图里还留着 */
body:has(.q:target) .chatbtn{{display:none}}
#chat .hd{{background:var(--accent);color:#fff;padding:13px 15px;display:flex;
 gap:9px;align-items:center;font-size:14px;font-weight:600;flex:0 0 auto}}
#chat .hd .qid{{background:rgba(255,255,255,.22);border-radius:6px;padding:1px 7px;
 font:11.5px ui-monospace,Menlo,monospace}}
#chat .hd .term{{margin-left:auto;background:rgba(0,0,0,.18);border:none;color:#fff;
 width:28px;height:26px;border-radius:7px;cursor:pointer;font-size:14px;line-height:1}}
#chat .tm{{display:none;flex:1 1 auto;min-height:0;width:100%;background:#0b0d12;
 padding:6px 8px;overflow:hidden}}
#chat .tm .xterm{{height:100%}}
#chat .tm .xterm-viewport{{overflow-y:auto}}
#chat .hd .x{{background:rgba(0,0,0,.18);border:none;color:#fff;
 width:26px;height:26px;border-radius:50%;cursor:pointer;font-size:15px;line-height:1}}
#chat .bd{{padding:14px;flex:1 1 auto;min-height:0;overflow-y:auto;
 display:flex;flex-direction:column;gap:9px;background:var(--bg)}}
#chat .m{{max-width:90%;padding:9px 13px;border-radius:13px;font-size:14px;line-height:1.6;
 white-space:pre-wrap;word-break:break-word}}
#chat .m.you{{align-self:flex-end;background:var(--accent);color:#fff;border-bottom-right-radius:4px}}
#chat .m.cc{{align-self:flex-start;background:var(--pre);color:var(--fg);
 border:1px solid var(--line);border-bottom-left-radius:4px}}
#chat .m.sys{{align-self:center;background:none;color:var(--mut);font-size:12px;padding:2px}}
/* 思考过程折叠块 */
#chat .tk{{align-self:flex-start;max-width:92%;border:1px dashed var(--line);
 border-radius:11px;background:var(--bg);padding:4px 11px;margin:1px 0}}
#chat .tk>summary{{cursor:pointer;color:var(--mut);font-size:12.5px;list-style:none;padding:3px 0}}
#chat .tk>summary::-webkit-details-marker{{display:none}}
#chat .tk>summary::before{{content:"▸ ";color:var(--mut)}}
#chat .tk[open]>summary::before{{content:"▾ "}}
#chat .tk .tk-body{{white-space:pre-wrap;word-break:break-word;color:var(--mut);
 font-size:12.5px;line-height:1.6;padding:4px 0 6px;max-height:280px;overflow-y:auto}}
/* 权限提示，跟 CLI 那个弹窗一个意思 */
#chat .ask{{align-self:stretch;border:1px solid var(--wip);border-radius:11px;
 padding:10px 12px;background:var(--bg)}}
#chat .ask .q{{font-size:13px;font-weight:600;color:var(--wip);margin-bottom:6px}}
#chat .ask .w{{font:12px ui-monospace,Menlo,monospace;color:var(--fg);
 background:var(--pre);border-radius:7px;padding:7px 9px;margin-bottom:9px;
 overflow-x:auto;white-space:pre}}
#chat .ask .b{{display:flex;gap:7px;align-items:center}}
#chat .ask button{{border:1px solid var(--line);background:var(--card);color:var(--fg);
 border-radius:8px;padding:5px 11px;font:12.5px inherit;cursor:pointer}}
#chat .ask button.ok{{background:var(--done);border-color:var(--done);color:#fff}}
#chat .ask button.n{{color:var(--todo);border-color:var(--todo)}}
/* 回复里的 markdown */
#chat .m.md{{white-space:normal}}
#chat .m.md p{{margin:0 0 7px}}
#chat .m.md p:last-child{{margin-bottom:0}}
#chat .m.md .mh{{font-weight:700;margin:9px 0 5px}}
#chat .m.md ul,#chat .m.md ol{{margin:4px 0 7px;padding-left:20px}}
#chat .m.md li{{margin:2px 0}}
#chat .m.md li.cont{{list-style:none;color:var(--mut);margin-left:-6px}}
#chat .m.md pre{{margin:6px 0;padding:9px 11px;font-size:12px;line-height:1.5;
 background:var(--bg);border:1px solid var(--line);border-radius:8px;overflow-x:auto}}
#chat .m.md code{{font-size:12.5px}}
#chat .ft{{display:flex;gap:8px;padding:12px;border-top:1px solid var(--line);
 align-items:flex-end;flex:0 0 auto}}
#chat textarea{{flex:1;border:1px solid var(--line);border-radius:10px;padding:8px 11px;
 font:14px inherit;background:var(--bg);color:var(--fg);resize:none;max-height:110px}}
#chat .send{{background:var(--accent);color:#fff;border:none;border-radius:10px;
 width:38px;height:36px;cursor:pointer;font-size:15px}}
#chat .send:disabled{{opacity:.45;cursor:default}}
#chat .send.stop{{background:var(--todo)}}
#chat .tip{{padding:0 13px 9px;font-size:11.5px;color:var(--mut)}}
#chat .cfg{{display:flex;gap:7px;align-items:center;padding:0 13px 8px;flex:0 0 auto}}
#chat .cfg select{{border:1px solid var(--line);border-radius:7px;padding:4px 7px;
 background:var(--bg);color:var(--fg);font:12px inherit}}
#chat .cfg .cost{{margin-left:auto;font:11.5px ui-monospace,Menlo,monospace;color:var(--mut)}}
#chat .sid{{display:flex;gap:7px;align-items:center;flex-wrap:wrap;padding:0 13px 8px;
 font-size:11.5px;color:var(--mut);flex:0 0 auto}}
#chat .sid code{{font-size:11px}}
#chat .acts{{display:flex;flex-wrap:wrap;gap:6px;padding:10px 14px 4px;flex:0 0 auto}}
#chat .act{{border:1px solid var(--line);background:var(--bg);color:var(--fg);
 border-radius:999px;padding:5px 12px;font:12.5px inherit;cursor:pointer}}
#chat .act:hover{{border-color:var(--accent)}}
#chat .act.pri{{background:var(--accent);color:#fff;border-color:var(--accent)}}

/* ## Comments —— 带状态的行内评论 */
.cm{{border-left:3px solid var(--wip);padding:7px 0 7px 11px;margin:9px 0}}
.cm.done{{border-left-color:var(--done);opacity:.62}}
.cmh{{display:flex;gap:8px;align-items:baseline;flex-wrap:wrap;font-size:13px}}
.cmh .bx{{color:var(--mut)}}
.cm.done .cmh .bx{{color:var(--done)}}
.cmh b{{font-size:11.5px;letter-spacing:.4px}}
.cq{{color:var(--mut);flex:1;min-width:120px}}
.cw{{font:11.5px ui-monospace,Menlo,monospace;color:var(--mut)}}
.cs{{font-size:11px;letter-spacing:.05em;text-transform:uppercase;padding:1px 8px;
 border:1px solid var(--wip);color:var(--wip);border-radius:999px}}
.cm.done .cs{{border-color:var(--done);color:var(--done)}}
.cs.lost{{border-color:var(--todo);color:var(--todo);text-transform:none}}
.cs.unpin{{border-color:var(--line);color:var(--mut);text-transform:none;cursor:help}}
.cmb{{padding-left:22px;margin-top:3px}}
.cmb p{{margin:0 0 4px}}
/* 已解决评论：正文折叠，只留一行 reply 标题 */
.cmb-fold{{padding-left:22px;margin-top:2px}}
.cmb-fold>summary{{cursor:pointer;color:var(--mut);font-size:12px;list-style:none;padding:1px 0}}
.cmb-fold>summary::-webkit-details-marker{{display:none}}
.cmb-fold>summary::before{{content:"▸ ";color:var(--mut)}}
.cmb-fold[open]>summary::before{{content:"▾ "}}
.cmb-fold .cmb{{padding-left:0}}
.cres{{margin-left:6px;border:1px solid var(--line);background:var(--bg);color:var(--mut);border-radius:7px;padding:2px 9px;font:11.5px inherit;cursor:pointer}}
.cres:hover{{border-color:var(--accent);color:var(--accent)}}
.obadge{{background:var(--wip);color:#fff;border-radius:999px;padding:1px 8px;font-size:11.5px}}
mark.solved{{background:rgba(21,128,61,.16);outline:none}}
b.jl{{color:var(--accent)}}b.ra{{color:var(--ra)}}b.cc{{color:var(--mut)}}
b.u0{{color:#8b5cf6}}b.u1{{color:#0891b2}}b.u2{{color:#c2410c}}b.u3{{color:#be185d}}

/* 行内评论：被引用的原句 + 评论里的引文 */
mark{{background:rgba(255,214,0,.34);color:inherit;padding:0 2px;border-radius:3px}}
@media(prefers-color-scheme:dark){{mark{{background:rgba(255,214,0,.22)}}}}
.qt{{color:var(--mut);font-size:.92em;margin-right:5px}}
/* 评论工具条（只有开了 JS 才会出现；关掉 JS 页面一切照旧） */
#cbtn{{position:absolute;z-index:40;display:none;background:var(--accent);color:#fff;
 border:none;border-radius:7px;padding:6px 12px;font-size:13px;cursor:pointer;
 box-shadow:0 3px 10px rgba(0,0,0,.22)}}
#cbox{{position:absolute;z-index:41;display:none;width:330px;background:var(--card);
 border:1px solid var(--line);border-radius:11px;padding:13px;
 box-shadow:0 8px 26px rgba(0,0,0,.24)}}
#cbox .qq{{font-size:12.5px;color:var(--mut);border-left:3px solid var(--accent);
 padding-left:9px;margin-bottom:9px;max-height:66px;overflow:auto}}
#cbox textarea{{width:100%;min-height:66px;border:1px solid var(--line);border-radius:7px;
 padding:8px;font:14px inherit;background:var(--bg);color:var(--fg);resize:vertical}}
#cbox .row{{display:flex;gap:8px;align-items:center;margin-top:9px}}
#cbox select{{border:1px solid var(--line);border-radius:7px;padding:5px 8px;
 background:var(--bg);color:var(--fg);font:13px inherit}}
#cbox button,#cpanel button{{border:1px solid var(--line);border-radius:7px;padding:6px 12px;
 background:var(--bg);color:var(--fg);font:13px inherit;cursor:pointer}}
#cbox .ok,#cpanel .ok{{background:var(--accent);color:#fff;border-color:var(--accent)}}
#cdock{{position:fixed;right:18px;bottom:74px;z-index:42;display:none;
 background:var(--accent);color:#fff;border:none;border-radius:999px;
 padding:10px 17px;font-size:13.5px;cursor:pointer;box-shadow:0 5px 16px rgba(0,0,0,.26)}}
#cpanel{{position:fixed;right:18px;bottom:122px;z-index:42;display:none;width:390px;
 max-height:64vh;overflow:auto;background:var(--card);border:1px solid var(--line);
 border-radius:12px;padding:14px;box-shadow:0 10px 30px rgba(0,0,0,.3)}}
#cpanel .it{{border-top:1px solid var(--line);padding:9px 0;font-size:13.5px}}
#cpanel .it .q{{color:var(--mut);font-size:12px}}
#cpanel .hd{{display:flex;gap:8px;margin-bottom:4px}}
#cpanel .hint{{font-size:12px;color:var(--mut);margin-top:10px;line-height:1.6}}
.cnt{{float:right;font-weight:400;font:12px ui-monospace,Menlo,monospace}}

/* 大标题前面挂编号：QA2 一个 Q 文件的模板 */
.hid{{color:var(--accent);font:.62em ui-monospace,Menlo,monospace;
 vertical-align:.22em;margin-right:11px;letter-spacing:.03em}}

/* ## 日志 —— 这一题一路改过什么 */
.lg{{display:flex;gap:11px;align-items:baseline;margin:4px 0}}
.lg .d{{flex:0 0 96px;white-space:nowrap;font:11.5px ui-monospace,Menlo,monospace;color:var(--mut)}}

/* ## 图 —— 这一题想干嘛，一张 ascii 图先说清楚 */
.dia{{margin:0 0 18px}}
.dia pre{{margin:0;padding:15px 17px;line-height:1.55}}
.q:target .dia{{margin:0 0 24px}}
.q:target .dia pre{{font-size:13px;line-height:1.6}}
.col.now{{border-left:3px solid var(--wip)}}
.col.goal{{border-left:3px solid var(--done)}}
/* 节标题：左标签 + 底下一条线 + 右边 expand-all（JL 260723） */
.ch{{display:flex;align-items:baseline;gap:8px;font-size:12.5px;color:var(--mut);
 margin:0 0 9px;font-weight:600;border-bottom:1px solid var(--line);padding-bottom:5px}}
.ch .chl{{flex:1;min-width:0}}
.ch .cnt{{color:var(--mut);font-weight:600}}
/* expand / collapse all：把这一节所有 item 一起开合。纯增强——脚本剥掉后
   每个 item 仍能单独点开（native <details>），全文一直在 DOM 里。 */
.secall{{flex:0 0 auto;border:1px solid var(--line);background:var(--bg);color:var(--mut);
 border-radius:6px;padding:1px 9px;font:11px inherit;font-weight:500;cursor:pointer;letter-spacing:0}}
.secall:hover{{border-color:var(--accent);color:var(--accent)}}
.q:target .secall{{font-size:12px;padding:2px 11px}}
.col p{{margin:0 0 6px;font-size:15px}}
.col pre{{font-size:11.5px}}

/* ── 聚焦 = 一张幻灯片，不是一个卡片 ─────────────────────────
   照 html-ppt：内容直接铺在页面上，没有边框、圆角、卡片底色把它围住。
   头部压成一条跑马条，剩下的高度全给这一题。 */
body:has(.q:target) .wrap{{max-width:1000px;padding:20px 26px 40px}}
body:has(.q:target) .h1{{font-size:14px;color:var(--mut);font-weight:600;margin:0 0 7px}}
body:has(.q:target) .spine{{border:none;background:none;border-radius:0;
 border-left:2px solid var(--accent);padding:0 0 0 11px;margin:0 0 9px}}
body:has(.q:target) .spine p{{font-size:12.5px;margin:2px 0;color:var(--mut)}}
body:has(.q:target) details.ctx{{border:none;background:none;padding:0;margin:3px 0}}
body:has(.q:target) details.ctx>summary{{font-size:12.5px;color:var(--mut)}}

body:has(.q:target) .q:target{{border:none;border-radius:0;background:none;
 padding:0;margin:26px 0 0;min-height:calc(100vh - 230px);
 scroll-margin-top:280px;display:flex;flex-direction:column}}
.q:target .src,.q:target .top{{display:none}}
.q:target .qh{{margin-bottom:10px}}
.q:target .h2{{font-size:38px;line-height:1.24;letter-spacing:-.01em;margin:0 0 18px}}
.q:target .ask{{border-left:none;padding-left:0;margin:0 0 24px}}
.q:target .ask p{{font-size:16px;line-height:1.75}}
.q:target .ask>p:first-of-type{{font-size:21px;line-height:1.5;color:var(--fg);margin:0 0 13px}}
/* Boundary / Files 聚焦时也去框，只留一道边，跟 Items/Where 一个排法 */
.q:target .bnd{{border:none;border-radius:0;background:none;padding:0 0 0 15px;
 border-left:2px solid var(--mut);margin:0 0 22px}}
.q:target .bnd p{{font-size:16px;line-height:1.75;margin:0 0 6px}}
.q:target .fls{{border:none;border-radius:0;background:none;padding:0 0 0 15px;
 border-left:2px solid var(--accent);margin:22px 0 0}}
.q:target .fls p{{font-size:16px;line-height:1.75;margin:0 0 6px}}
.q:target .cmp{{gap:22px;margin:0 0 22px}}
.q:target .col{{border:none;border-radius:0;background:none;padding:0 0 0 15px}}
.q:target .col.now{{border-left:2px solid var(--wip)}}
.q:target .col.goal{{border-left:2px solid var(--done)}}
.q:target .ch{{font-size:18px;color:var(--fg);margin-bottom:14px;padding-bottom:7px;
 letter-spacing:-.01em}}
.q:target .ch .cnt{{font-size:13px}}
.q:target .col p{{font-size:16px;line-height:1.75}}
/* 「为什么在这块板」在幻灯片上也排成一栏，跟上面两栏同一个样式（.ch 标题 + 线） */
.q:target .f{{display:block;margin:0;border-left:2px solid var(--line);padding-left:15px}}
.q:target .f p,.q:target .fbd p{{font-size:16px;line-height:1.75;margin:0 0 6px}}
.q:target .folds{{margin-top:auto;padding-top:18px}}
.folds{{margin-top:16px;border-top:1px dashed var(--line);padding-top:8px}}
.fold{{margin:3px 0}}
.fold>summary{{cursor:pointer;color:var(--mut);font-size:14px;list-style:none;padding:4px 0}}
.fold[open]>summary{{color:var(--fg)}}
.fb{{padding:5px 0 8px 16px;font-size:14.5px}}
/* 讨论框：整段写想法，追加进 ## Discussion（JL 260723） */
.dadd{{margin-top:11px;border-top:1px dashed var(--line);padding-top:10px}}
.dadd textarea{{width:100%;min-height:60px;border:1px solid var(--line);border-radius:8px;
 padding:8px 10px;font:14px inherit;line-height:1.6;background:var(--bg);color:var(--fg);resize:vertical}}
.dadd .row{{display:flex;gap:8px;align-items:center;margin-top:7px}}
.dadd select{{border:1px solid var(--line);border-radius:7px;padding:4px 9px;font:13px inherit;
 background:var(--bg);color:var(--fg)}}
.dadd .dsave{{margin-left:auto;border:1px solid var(--accent);background:var(--accent);color:#fff;
 border-radius:7px;padding:6px 14px;font:13px inherit;font-weight:600;cursor:pointer}}
.dadd .dsave:hover{{filter:brightness(1.07)}}
.dadd .dsave:disabled{{opacity:.6;cursor:default}}
.cmt{{border-left:3px solid var(--mut);padding:3px 0 3px 10px;margin:5px 0}}
.cmt b{{font-size:11px;letter-spacing:.4px;margin-right:5px}}
.cmt .qt{{background:rgba(217,164,6,.18);border-bottom:1px solid rgba(217,164,6,.55);
 padding:0 2px;border-radius:2px}}
.cmt.jl{{border-color:var(--accent)}}.cmt.jl b{{color:var(--accent)}}
.cmt.ra{{border-color:var(--ra)}}.cmt.ra b{{color:var(--ra)}}
.mut{{color:var(--mut)}}
a.fp{{text-decoration:none;border-bottom:1px dashed var(--accent)}}
a.fp code{{color:var(--accent);cursor:pointer}}
a.fp:hover code{{background:var(--accent);color:var(--bg)}}
code{{background:var(--pre);padding:1px 5px;border-radius:4px;font:13px ui-monospace,Menlo,monospace}}
pre{{background:var(--pre);border:1px solid var(--line);border-radius:8px;padding:11px 13px;
 margin:8px 0;overflow-x:auto;font:12.5px/1.6 ui-monospace,Menlo,monospace;white-space:pre}}
img{{max-width:100%;border:1px solid var(--line);border-radius:8px}}
.foot{{margin-top:44px;padding-top:14px;border-top:1px solid var(--line);
 color:var(--mut);font-size:12.5px}}
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
