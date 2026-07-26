"""One question -> one <section class="slide q"> card (QB5: the card chunk of
the old render(), moved verbatim). page_stage.py owns embedded source content;
this file owns the q-template anatomy on stage."""
import re

from .body import (body, flat_rows, inline, mark_span, parse_comments,
                   render_comments, sort_log)
from .common import esc, sec, stinfo

STAGE_LABELS = {
    "seed": "SEED PAGE",
    "work": "WORK PAGE",
    "venue": "VENUE PAGE",
    "display": "DISPLAY PAGE",
    "main": "MAIN SECTION",
    "appendix": "APPENDIX",
    "submission": "SUBMISSION PAGE",
}


def det(label, inner, open_=False):
    if not inner:
        return ""
    o = " open" if open_ else ""
    return (f'<details class="fold"{o}><summary>{esc(label)}</summary>'
            f'<div class="fb">{inner}</div></details>')


def chead(label, inner, tag="div"):
    """一个节标题：左边标签、底下一条线（CSS 画）、右边一个「expand all」。
    只有这一节真有可折叠的 item（body 里出现 class="it"）才挂那个按钮 ——
    没东西可开合就不放。纯增强：脚本剥掉后每个 item 仍能单独点开。
    tag="summary" 时它就是所在 <details> 的开合把手（见 sect()）。"""
    tog = ('<button class="secall" type="button" title="expand / collapse all">'
           '<span class="lbl">expand all</span></button>'
           if '<details class="it' in inner else '')
    return f'<{tag} class="ch"><span class="chl">{label}</span>{tog}</{tag}>'


def sect(label, inner, cls="", open_=True):
    """A whole page section that folds from its own heading (JL 260725), by the
    same native-details mechanism Diagram already uses. Shut, the section keeps
    its text in the DOM, so the zero-script invariant, Ctrl-F, and the section
    ⧉ copy button all keep working."""
    if not inner:
        return ""
    o = " open" if open_ else ""
    return (f'<details class="sect {cls}"{o}>'
            f'{chead(label, inner, tag="summary")}{inner}</details>')


def parse_content_sections(txt):
    """Split direct ### headings without treating headings inside fences as sections."""
    sections = []
    title, buf, fence = "", [], False
    for ln in txt.split("\n"):
        if ln.lstrip().startswith("```"):
            fence = not fence
        if ln.startswith("### ") and not fence:
            if title or any(x.strip() for x in buf):
                sections.append((title, "\n".join(buf).strip()))
            title, buf = ln[4:].strip(), []
        else:
            buf.append(ln)
    if title or any(x.strip() for x in buf):
        sections.append((title, "\n".join(buf).strip()))
    return sections


def render_subsections(sections, open_first=True, flat=False):
    """Render named markdown chunks as native disclosure rows.

    flat=True drops the disclosure entirely and emits a plain `.fh` heading plus
    its body. Opening uses it (JL 260725: "I don't want to have >"): behind the
    lead question everything is simply shown, the way Boundary already was, so no
    second layer of ▸ rows hides the stage style, venue section, or writing style."""
    out = []
    for i, (heading, md) in enumerate(sections):
        # #### 不再压成 **…**（那会套上组标题的 🔹）；body() 现在自己渲染段落标题。
        rendered = body(md)
        if heading and flat:
            out.append(f'<div class="fh">{inline(heading)}</div>'
                       f'<div class="cbody flat">{rendered}</div>')
        elif heading:
            out.append(
                f'<details class="csec"{" open" if (open_first and i == 0) else ""}>'
                f'<summary>{inline(heading)}</summary><div class="cbody">{rendered}</div>'
                '</details>')
        elif rendered:
            out.append(f'<div class="cbody prelude">{rendered}</div>')
    return "".join(out)


def face_name(q):
    """"S Main 7 · Results" -> "Main 7 Results": the face's own name, for labels."""
    return re.sub(r"\s+", " ", re.sub(r"^[QS]\s+", "", q.get("title", ""))
                  .replace("·", " ")).strip()


def render_content(sections, q=None):
    """Render a face's remaining named Content subsections.

    On S pages the heading NAMES the stage ("Content · Main 7 Results") instead of
    counting subsections (JL 260725): an S page's Content is the stage's own
    substance, so the label should say which substance, not how many boxes.
    Q pages keep the count, where it is a scanning aid rather than an identity."""
    if not sections:
        return ""
    inner = render_subsections(sections)
    name = face_name(q) if q else ""
    n = len(sections)
    lab = (f"📚 Content · {esc(name)}" if name
           else f"📚 Content · {n} section" + ("s" if n != 1 else ""))
    return sect(lab, inner, cls="content")


def render_contract(sections):
    """Stage Contract renders INSIDE Opening (JL 260725), never its own section.

    It is shown outright behind the lead question, so Required Inputs, Writing
    Style and the venue section are read rather than hunted for. Its heading is a
    plain word like every other heading in that drawer (JL 260725: the drawer had
    two iconed headings and five bare ones, which is what read as inconsistent)."""
    if not sections:
        return ""
    return ('<div class="fh">Stage Contract</div>'
            + render_subsections(sections, flat=True))


def render_question(q, prv, nxt):
    nav = ('<div class="nav">'
           + (f'<a href="#{prv["id"]}">← {prv["id"]}</a>' if prv else '<span></span>')
           + f'<a class="all" href="#top">☰ Index</a>'
           + (f'<a href="#{nxt["id"]}">{nxt["id"]} →</a>' if nxt else '<span></span>')
           + '</div>')
    tok, cls, lab = stinfo(q["state"])
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
               + sect(f"🎯 Items to Finish{cnt}", gb, cls="col goal")
               + sect("📍 Where we are", nb, cls="col now")
               + '</div>')
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
    # 隐藏块只带 Boundary；Question 的解释落到随后可见的 Content 里，让页面真正按
    # Opening -> Content -> Items -> Where 阅读。
    # 问句里的 **粗体** 要正常内联流动 —— 所以文字包进一个 .qt span，别让 flex 拆散它。
    # Boundary 收进【同一个】折叠块，不再单占一节；里头用扁平行，不套第二层折叠。
    q_md = sec(q["sec"], "Question").strip()
    _parts = re.split(r"\n\s*\n", q_md, maxsplit=1)
    qlead = inline(_parts[0].replace("\n", " ").strip())
    qrest = _parts[1].strip() if len(_parts) > 1 else ""
    content_sections = parse_content_sections(sec(q["sec"], "Content"))
    contract_md = re.sub(r"<!--.*?-->", "", sec(q["sec"], "Stage Contract"), flags=re.S)
    contract_sections = parse_content_sections(contract_md)
    stage_record = ""
    is_stage = q.get("kind") == "stage"
    if is_stage:
        for i, (heading, md) in enumerate(content_sections):
            if re.sub(r"\s+", " ", heading).strip().casefold() == "stage record":
                stage_record = md
                del content_sections[i]
                break
    opening_sections = []
    if is_stage:
        if qrest:
            opening_sections.append(("Why this matters", qrest))
        if stage_record:
            opening_sections.append(("Stage Record", stage_record))
    elif qrest:
        content_sections.insert(0, ("Why this matters", qrest))
    # Stage Contract joins Opening's collapsed rows (JL 260725: "within the
    # Opening, not a separate section"), after Why this matters / Stage Record.
    btxt = sec(q["sec"], "Boundary").strip()
    inner = ""
    if btxt:
        inner += f'<div class="fh">Boundary</div>{flat_rows(btxt)}'
    # 抽屉里全是平的：Boundary 一直就是这样，Why this matters / Stage Record /
    # Stage Contract 现在跟它一致（JL 260725：「I don't want to have >」，以及
    # 「why other information are gone」—— 它们没丢，是被第二层 ▸ 关起来了）。
    inner += render_subsections(opening_sections, flat=True)
    if is_stage:
        inner += render_contract(contract_sections)
    # Opening 本身不折（JL 260725：「no > in the Opening, it will always be there」）：
    # 🧭 Opening 这一行和领句永远在台面上。可点的是【领句】—— 点开它，Boundary、
    # Why this matters、Stage Record、Stage Contract 全在这一个抽屉里，用来解释这句问句。
    # 中间那版把折叠挂在 🧭 Opening 上，于是节名本身成了一个只写着「Opening」的 ▸ 行，
    # 读者看不出里头有 Boundary —— 正是 260724 那条 Law 要防的（fold 生效且不可见）。
    # 领句的排版跟原版一模一样：<summary> 里仍然是那个 <p class="qlead">，
    # 所以 `.q p` 的 serif 和 `.ask>p:first-of-type` 的字号都照旧命中（JL 260725：
    # 「I want the original font size and font type」—— 把 class 挪到 summary 上就丢了这两条）。
    lead_p = (f'<p class="qlead"><span class="qt">{qlead}</span>'
              f'<span class="cv"></span></p>')
    opening_head = '<div class="ch opening-head"><span class="chl">🧭 Opening</span></div>'
    qblock = (
        f'<details class="it row qd"><summary>{lead_p}</summary>'
        f'<div class="bd qbd">{inner}</div></details>'
        if inner else
        f'<p class="qlead"><span class="qt">{qlead}</span></p>'
    )
    ask = f'<div class="ask">{opening_head}{qblock}</div>'
    bnd = ""   # Boundary 现在收在 ask 的折叠块里，不再单独上台面
    # 📁 Files（JL 260723 新增，选填）：这题牵动哪些文件。读懂之后知道去哪儿动手；
    # 反过来改了哪个文件，也知道该回写哪一题。路径写反引号里，board.md 的
    # ## Links 声明过的会自动变成可点链接。
    flb = body(sec(q["sec"], "Files"))
    fls = sect("📁 Files", flb, cls="fls")
    dia_txt = sec(q["sec"], "Diagram")
    dia = (
        '<details class="diagram-section">'
        '<summary class="ch"><span class="chl">🖼 Diagram</span></summary>'
        f'<div class="dia">{body(dia_txt, fold_code=False)}</div>'
        '</details>'
        if dia_txt else ""
    )
    content = render_content(content_sections, q if is_stage else None)

    def _norm(s):
        # 剥掉标签、把连续空白压成一个 —— 拿来判「这句到底在不在页面上」
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()

    # 卡片上所有可见文字的「纯文本」快照，用来判 lost（不含标签、空白已归一）
    # Stage Contract 的文字已经嵌在 ask 里，扫 ask 就覆盖它。
    card_plain = _norm(
        ask + " " + bnd + " " + content + " " + fs + " " + fls + " " + dia
    )

    def hl(quote, solved):
        # 锚点为什么老丢，两个原因都堵上（JL 260723 问）：
        #   ① 扫描范围太窄：以前只扫 ask+fs，选中「## Diagram」里的字就被冤枉。→ 现在也扫 dia。
        #   ② 引文横跨行内标记：`代码`→<code>、**粗**→<b>。用 mark_span 跨标签描黄，
        #      不再是 naive 的 e in html（那个一遇标签就贴不到原文）。
        #   兜底：连跨标签都找不到（空白差异等），退一步用纯文本判「在不在」——
        #        在就不算 lost（只是这一条没描黄）。
        nonlocal ask, bnd, content, fs, fls, dia
        e = esc(quote)
        kls = ' class="solved"' if solved else ''
        for name in ("ask", "bnd", "content", "fs", "fls", "dia"):
            cur = {"ask": ask, "bnd": bnd, "content": content,
                   "fs": fs, "fls": fls, "dia": dia}[name]
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
                elif name == "dia":
                    dia = new
                else:
                    content = new
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
                (body(disc, apparatus=False) if disc else
                 f'<p class="mut">No discussion yet — add a line under '
                 f'<code>## Discussion</code> in {q["file"]}: '
                 f'<code>&gt; JL: …</code></p>')
                + dadd)
    nopen = sum(1 for c in cms if not c["done"])
    nlost = sum(1 for c in cms if c["lost"])
    if cms:
        # cm_lab, NOT lab: the old single-function render() reused `lab` here and
        # clobbered the state label, so any question WITH comments wore the
        # comments count in its state pill. Caught by QB5's byte-identical gate.
        cm_lab = f"💬 Comments ({nopen} open / {len(cms)})"
        if nlost:
            cm_lab += f" · {nlost} unanchored"    # 引文不在正文里；不喊「丢了」（分不清是聊天话还是真被改）
        folds += det(cm_lab, f'<div class="cms" data-cfile="{esc(q.get("file",""))}">'
                     + render_comments(cms) + '</div>', open_=nopen > 0)
    # Why here 不再上台面（它的活并进 ## Question 的要点）；老板子里还写着的收进折叠区
    folds += det("💡 Why here", body(why, apparatus=False))
    folds += det("⚖️ Law", body(sec(q["sec"], "Law"), apparatus=False))
    folds += det("🧠 Lesson", body(sec(q["sec"], "Lesson"), apparatus=False))
    folds += det("📖 Glossary", body(sec(q["sec"], "Glossary"), apparatus=False))
    log = sort_log(sec(q["sec"], "Log").strip())
    nlog = len(re.findall(r"^\d{6}(?:\s+\d{3,4})?\s*[·|]", log, re.M))
    folds += det(f"📜 Log ({nlog})", body(log, apparatus=False))
    return (
        f'<section class="slide q {cls}" id="{q["id"]}"'
        f' data-title="{esc(q["title"])}" data-file="{esc(q.get("file",""))}"'
        f' data-session="{esc(q.get("session",""))}">'
        f'<div class="qh"><span class="qid">{q["id"]}</span>'
        f'<span class="pill {cls}">{tok} {esc(lab)}</span>'
        f'<span class="mut">{esc(who)}</span>'
        f'<span class="mut">· {inline(q["method"])}</span>'
        + (
            f'<span class="kind">'
            f'{esc(STAGE_LABELS.get(q.get("family"), "STAGE"))}</span>'
            if q.get("kind") == "stage" else ""
        )
        + (f'<span class="obadge">💬 {nopen}</span>' if nopen else "")
        # 文件名做成链接：点它直接看这一题的原始 markdown（serve.py 把它当纯文本发）
        + f'<a class="src" href="{esc(q.get("file",""))}" target="_blank"'
        f' title="Open this question\'s raw markdown">📄 {esc(q.get("file",""))}</a>'
        f'<a class="top" href="#top">↑ Index</a></div>'
        # id 后面那个空格是真字符（不是 CSS margin）——复制这行标题时
        # 才不会粘成 QA4Single…，而是 QA4 Single…（JL 260723）
        f'<h2 class="h2"><span class="hid">{q["id"]} </span>{inline(q["title"])}</h2>'
        + f'<div class="opening">{ask}{bnd}</div>' + dia + content
        + f'{fs}{fls}<div class="folds">{folds}</div>{nav}</section>')
