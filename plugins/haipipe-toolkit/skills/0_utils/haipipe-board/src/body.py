"""The board's body grammar -> html (ref/board-form.md §5): inline marks, link
resolution, topic/explanation bullets, checklists, fences, comment lanes, logs.
BASE (the board folder) is set by the entry point; LINKS is filled by
parse.parse_board from board.md's ## Links. Both live here because inline()
is where paths become hrefs."""
import re

from .common import esc, who_class
from .page_stage import EMBED, embed_block

BASE = None            # 当前这块板的文件夹，build.py 的入口设；用来把路径解析成链接
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
    tok = m.group(1)          # 已经过外层 esc()，别再转义一次（否则 `>` 显示成 &gt;）
    href = resolve(tok)
    if href:
        return f'<a class="fp" href="{esc(href)}"><code>{tok}</code></a>'
    return f"<code>{tok}</code>"


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
# 没写就默认 🔹。build.py 不去猜——图标随内容变，是作者写的，不是机器生成的（QA9 写法规矩）。
# 只认真 emoji 开头：中文、英文、▸(U+25B8) 都不在这些区段，不会误判成图标。
_EMO = ("\U0001F000-\U0001FAFF"      # 大部分 emoji（🔹🎨📍…）
        "\U00002600-\U000027BF"      # 杂项符号 + dingbats（✅⚠⚙…）
        "\U00002B00-\U00002BFF"      # ⭐ 等
        "\U00002190-\U000021FF"      # 箭头
        "\U00002300-\U000023FF")     # ⏰⌛ 等
GT_ICON = re.compile("^([" + _EMO + "]"
                     "[" + _EMO + "️‍\U0001F3FB-\U0001F3FF]*)"
                     r"\s+(.+)$")


LANE = re.compile(r"^>+\s*(Citation|Value|Display|Check|Q-consumer|Link|Source|Note)"
                  r"\s*[:：]\s*(.*)$", re.I)
LANE_ICON = {"citation": "📚", "value": "🔢", "display": "🖼", "check": "⚠️",
             "q-consumer": "🔎", "link": "🔗", "source": "📄", "note": "📝"}


def render_apparatus(lines):
    """一句话的随行装置（QA8，JL 260725）：typed `> Kind:` 行 + `> WHO:` 讨论，
    折叠在它们讨论的那一句下面。返回 (html, 头行数)。"""
    rows, heads = [], 0
    for ln in lines:
        m = LANE.match(ln)
        if m:
            kind = m.group(1).lower()
            lbl = m.group(1)[0].upper() + m.group(1)[1:].lower()
            rows.append(f'<div class="lane"><b>{LANE_ICON.get(kind, "📎")} {esc(lbl)}</b> '
                        f'{inline(m.group(2))}</div>')
            heads += 1
            continue
        m = re.match(r"^(>+)\s*([A-Z]{1,4}\d{0,4})\s*[「\"]([^」\"]+)[」\"]\s*[:：]\s*(.*)$", ln)
        if m:
            rows.append(f'<div class="cmt {who_class(m.group(2))}"><b>{esc(m.group(2))}</b>'
                        f'<span class="qt">「{inline(m.group(3))}」</span> {inline(m.group(4))}</div>')
            heads += 1
            continue
        m = re.match(r"^(>+)\s*([A-Z]{1,4}\d{0,4})\s*(\[[^\]]+\])?\s*[:：]\s*(.*)$", ln)
        if m:
            rows.append(f'<div class="cmt {who_class(m.group(2))}"><b>{esc(m.group(2))}</b> '
                        f'{inline(m.group(4))}</div>')
            heads += 1
            continue
        rows.append(f'<div class="lane-cont">{inline(ln.lstrip(">").strip())}</div>')
    return "".join(rows), heads


def body(txt, fold_code=True, apparatus=True):
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
    ifence = None    # 缩进在 item 下的 ``` 块：收进这个 item 的折叠区（JL 260724）
    last_p, appar = None, {}   # 最近一句正文的 out 下标 → 它收集到的 `>` 装置行（QA8）
    para_head = False          # 上一行是不是 #### 段落标题（决定紧跟的 (…) 是不是它的活儿）

    def flush():
        """把攒着的要点 / 勾选项吐出来。两者共用「小标题 + 缩进解释」这套结构。"""
        nonlocal blt, last_p
        if blt is None:
            return
        last_p = None
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
            parts, lead = [], True
            for x in det:
                if isinstance(x, tuple):   # ("pre", lines): 折叠区里的 ascii 图
                    parts.append(f'<pre class="ip">{esc(chr(10).join(x[1]))}</pre>')
                elif lead:
                    parts.append(f'<p class="ld">{inline(x)}</p>')
                    lead = False
                else:
                    parts.append(f'<p>{inline(x)}</p>')
            exp = "".join(parts)
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
        # 缩进的 ``` 属于当前 item：ascii 收进它的折叠区（JL 260724 QC10）。
        # 顶格的 ``` 照旧 flush 成兄弟块 —— 台面只放标题，图藏在点开之后。
        if ifence is not None:
            if ln.strip().startswith("```"):
                pad = min((len(x) - len(x.lstrip()) for x in ifence if x.strip()),
                          default=0)
                blt[2].append(("pre", [x[pad:] if x.strip() else "" for x in ifence]))
                ifence = None
            else:
                ifence.append(ln)
            continue
        if blt is not None and re.match(r"^\s{2,}```", ln):
            ifence = []
            continue
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
                last_p = None
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
            last_p = None
            blt = ["blt", m.group(1).strip(), [], False]
            continue
        flush()
        if not ln.strip():
            continue
        # 句子随行装置（QA8，JL 260725）：紧跟在一句正文后面的 `>` 行
        # （> Citation: / > Value: / > Check: / > JL: …，可隔空行）收进那一句的
        # 抽屉；句尾挂 ⚑N，点开才现。没有前一句的 `>` 行照旧渲染。
        if apparatus and ln.lstrip().startswith(">") and last_p is not None:
            appar.setdefault(last_p, []).append(ln.strip())
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
            last_p = None
            continue
        m = re.match(r"^\s*[-*]\s*\[([ xX])\]\s*(.*)$", ln)   # - [ ] / - [x]
        if m:
            flush()
            last_p = None
            blt = ["ck", m.group(2), [], m.group(1).lower() == "x"]
            continue
        # ![[path]] / ![[path#Section]]（QF1，JL 260724）：把另一份文件的内容按
        # 【引用】嵌进这一题 —— 生成时现读，零拷贝零漂移。板永远不学源文件的方言：
        # page_stage.render_doc 是通用渲染。嵌不到会就地标红，绝不悄悄空掉。
        m = EMBED.match(ln)
        if m:
            flush()
            out.append(embed_block(m.group(1).strip(), m.group(2)))
            last_p = None
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
            last_p = None
            continue
        # #### = 段落标题（一节里的一个 ¶）。以前被压成 **…**，于是套上了组标题的
        # 🔹，把「一个段落」说成了「领一串 item 的一句话」（JL 260725）。现在它是
        # 自己的层级：没有图标，比组标题小，紧跟其后的整行括号是这一段的活儿。
        m = re.match(r"^#{4,6}\s+(.+?)\s*$", ln)
        if m:
            out.append(f'<div class="ph">{inline(m.group(1))}</div>')
            last_p = None
            para_head = True
            continue
        # 段落标题后面紧跟的整行 (…) 是这一段要干的活：留在页面上（它是扫读用的），
        # 但排成灰斜体，跟正文分开（JL 260725）。只认紧跟标题的那一行。
        if para_head and re.match(r"^\(.+\)\s*$", ln):
            out.append(f'<div class="pj">{inline(ln.strip()[1:-1].strip())}</div>')
            last_p = None
            para_head = False
            continue
        para_head = False
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
            last_p = None
            continue
        # > JL 「被选中的原句」: 评论    ← 行内评论；引号里那段会在正文里高亮
        m = re.match(r"^(>+)\s*([A-Z]{1,4}\d{0,4})\s*[「\"]([^」\"]+)[」\"]\s*[:：]\s*(.*)$", ln)
        if m:
            who = m.group(2)
            k = who_class(who)
            out.append(f'<div class="cmt {k}"><b>{esc(who)}</b>'
                       f'<span class="qt">「{inline(m.group(3))}」</span> {inline(m.group(4))}</div>')
            last_p = None
            continue
        m = re.match(r"^(>+)\s*([A-Z]{1,4}\d{0,4})\s*(\[[^\]]+\])?\s*[:：]\s*(.*)$", ln)
        if m:
            who = m.group(2)
            k = who_class(who)
            out.append(f'<div class="cmt {k}"><b>{esc(who)}</b> {inline(m.group(4))}</div>')
            last_p = None
        else:
            out.append(f"<p>{inline(ln)}</p>")
            last_p = len(out) - 1
    flush()
    # 把收集到的装置行折进各自的句子（native <details>，零脚本不变量成立）
    for idx, lines in appar.items():
        inner, heads = render_apparatus(lines)
        out[idx] = ('<details class="sent"><summary>' + out[idx]
                    + f'<span class="sbadge">⚑ {heads}</span></summary>'
                    f'<div class="sapp">{inner}</div></details>')
    return "\n".join(out)
