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
import html, re, sys
from pathlib import Path

# 状态标签用英文：OPEN / PARTIAL / SETTLED / ON HOLD 是 issue 追踪的通用词，
# 一眼知道什么意思，不像自造的中文缩写要人猜。
ST = {"✅": ("done", "SETTLED"), "🟡": ("wip", "PARTIAL"),
      "🔴": ("todo", "OPEN"), "⏸️": ("hold", "ON HOLD")}
STN = {k.replace("️", ""): v for k, v in ST.items()}
# 段落名用英文（两边都认：新板写英文，老板写中文照样能读）
ALIAS = {"Question": "问题", "Diagram": "图", "Done when": "完成线",
         "Now": "现在什么样", "Why here": "为什么在这块板",
         "Glossary": "名词", "Discussion": "讨论", "Log": "日志",
         "Topic": "主题", "Pipeline": "流水线", "Roster": "清单"}


def sec(d, key):
    """段落取值：先按英文名找，找不到再按中文别名找。"""
    return d.get(key) or d.get(ALIAS.get(key, "\0")) or ""


def stinfo(state):
    """'✅ 已定' / '⏸️ 会上没答完' -> (emoji, css-class, label)"""
    state = (state or "").strip() or "🔴"
    tok = state.split()[0]
    cls, lab = STN.get(tok.replace("️", ""), ("todo", "没做"))
    rest = state[len(tok):].strip()
    return tok, cls, (rest or lab)


def esc(s):
    return html.escape(str(s))


def inline(s):
    s = esc(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img alt="\1" src="\2">', s)
    return s


def body(txt):
    """paragraphs + ``` blocks + comment lanes -> html"""
    out, fence = [], None
    for ln in (txt or "").split("\n"):
        if ln.lstrip().startswith("```"):
            if fence is None:
                fence = []
            else:
                out.append(f'<pre>{esc(chr(10).join(fence))}</pre>')
                fence = None
            continue
        if fence is not None:
            fence.append(ln)
            continue
        # (fenced block accumulates verbatim; flushed on the closing ```)
        if not ln.strip():
            continue
        m = re.match(r"^(\d{6})\s*[·|]\s*(.*)$", ln)          # 260722 · 改了什么
        if m:
            out.append(f'<div class="lg"><span class="d">{m.group(1)}</span>'
                       f'<span>{inline(m.group(2))}</span></div>')
            continue
        m = re.match(r"^\s*[-*]\s*\[([ xX])\]\s*(.*)$", ln)   # - [ ] / - [x]
        if m:
            on = m.group(1).lower() == "x"
            out.append(f'<div class="ck{" on" if on else ""}">'
                       f'<span class="bx">{"☑" if on else "☐"}</span>'
                       f'<span>{inline(m.group(2))}</span></div>')
            continue
        # > JL 「被选中的原句」: 评论    ← 行内评论；引号里那段会在正文里高亮
        m = re.match(r"^(>+)\s*(JL|RA|CC\d*)\s*[「\"]([^」\"]+)[」\"]\s*[:：]\s*(.*)$", ln)
        if m:
            who = m.group(2)
            k = {"JL": "jl", "RA": "ra"}.get(who, "cc")
            out.append(f'<div class="cmt {k}"><b>{esc(who)}</b>'
                       f'<span class="qt">「{inline(m.group(3))}」</span> {inline(m.group(4))}</div>')
            continue
        m = re.match(r"^(>+)\s*(JL|RA|CC\d*)\s*(\[[^\]]+\])?\s*:?\s*(.*)$", ln)
        if m:
            who = m.group(2)
            k = {"JL": "jl", "RA": "ra"}.get(who, "cc")
            out.append(f'<div class="cmt {k}"><b>{esc(who)}</b> {inline(m.group(4))}</div>')
        else:
            out.append(f"<p>{inline(ln)}</p>")
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
    return dict(title=title, spine=f("spine"), close=f("close"),
                theme=sec(bs, "Topic"), pipeline=sec(bs, "Pipeline"))


def parse_q(qid, txt, group="", file=""):
    """one question's text (title line + meta lines + ## sections) -> q dict"""
    lines = txt.split("\n")
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    qt = lines[i].lstrip("# ").strip() if i < len(lines) else qid
    i += 1
    meta = {"state": "🔴", "owner": "", "method": ""}
    while i < len(lines) and not lines[i].startswith("## "):
        m = re.match(r"^(state|owner|method):\s*(.*)$", lines[i].strip())
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
        m = re.match(r"Q([A-Z]*)(\d+)", p.stem)
        if m:
            disk[p.name] = ((m.group(1), int(m.group(2))),
                            "Q" + m.group(1) + m.group(2), p)
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
                warn.append(f"清单里写了 {name}，文件夹里没有这个文件")
    listed = bool(order)
    for name, (key, qid, p) in sorted(disk.items(), key=lambda kv: kv[1][0]):
        if name not in seen:
            if listed:
                warn.append(f"{name} 没写进 board.md 的「## 清单」")
            order.append(("⚠️ 没进清单" if listed else "", p))

    qs = [parse_q(disk[p.name][1], p.read_text(encoding="utf-8"), g, p.name)
          for g, p in order]
    return parse_board(board), qs, warn


def render(meta, qs):
    done = sum(1 for q in qs if q["state"].startswith("✅"))
    n = len(qs)
    bar = "█" * round(done / n * 14) + "░" * (14 - round(done / n * 14)) if n else ""

    def st(q):
        return stinfo(q["state"])

    rows, cur = [], None
    for q in qs:
        if q.get("group") and q["group"] != cur:
            cur = q["group"]
            rows.append(f'<div class="grp">{inline(cur)}</div>')
        rows.append(
            f'<a class="ir {st(q)[1]}" href="#{q["id"]}">'
            f'<span class="s">{st(q)[0]}</span><span class="i">{q["id"]}</span>'
            f'<span class="t">{inline(q["title"])}</span>'
            f'<span class="w">{"🧠 JL" if q["owner"]=="JL" else ("🔧 "+q["owner"] if q["owner"] else "")}</span></a>')
    idx = "\n".join(rows)

    def det(label, inner, open_=False):
        if not inner:
            return ""
        o = " open" if open_ else ""
        return (f'<details class="fold"{o}><summary>{esc(label)}</summary>'
                f'<div class="fb">{inner}</div></details>')

    cards = []
    for i, q in enumerate(qs):
        prv, nxt = (qs[i - 1] if i else None), (qs[i + 1] if i + 1 < n else None)
        nav = ('<div class="nav">'
               + (f'<a href="#{prv["id"]}">← {prv["id"]}</a>' if prv else '<span></span>')
               + f'<a class="all" href="#top">☰ All {n}</a>'
               + (f'<a href="#{nxt["id"]}">{nxt["id"]} →</a>' if nxt else '<span></span>')
               + '</div>')
        tok, cls, lab = st(q)
        who = "🧠 JL 拍板" if q["owner"] == "JL" else ("🔧 " + q["owner"] if q["owner"] else "")
        # 借 html-ppt 的 comparison 版式：一个 Q 的核心就是「现在」和「算做完」的落差，
        # 左右并排时那个落差本身是看得见的；上下堆叠时得读完两段才拼得出来。
        now, goal = sec(q["sec"], "Now"), sec(q["sec"], "Done when")
        boxes = re.findall(r"^\s*[-*]\s*\[([ xX])\]", goal, re.M)
        cnt = (f'<span class="cnt">{sum(1 for b in boxes if b.lower()=="x")}/{len(boxes)}</span>'
               if boxes else "")
        fs = ""
        if now or goal:
            fs += ('<div class="cmp">'
                   f'<div class="col now"><div class="ch">📍 Now</div>{body(now)}</div>'
                   f'<div class="col goal"><div class="ch">🎯 Done when{cnt}</div>{body(goal)}</div>'
                   '</div>')
        why = sec(q["sec"], "Why here")
        if why:
            fs += f'<div class="f"><span class="fl">💡 Why here</span><div>{body(why)}</div></div>'
        disc = sec(q["sec"], "Discussion").strip()
        ndisc = len(re.findall(r"^>+\s*(JL|RA|CC)", disc, re.M))
        folds = det(f"💬 Discussion ({ndisc})",
                    body(disc) if disc else
                    f'<p class="mut">还没有讨论。在 {q["id"]} 那个文件的「## 讨论」下写一行 '
                    f'<code>&gt; JL: …</code></p>')
        folds += det("📖 Glossary", body(sec(q["sec"], "Glossary")))
        log = sec(q["sec"], "Log").strip()
        nlog = len(re.findall(r"^\d{6}\s*[·|]", log, re.M))
        folds += det(f"📜 Log ({nlog})", body(log))
        # 被评论引用过的原句，在正文里高亮出来
        quoted = re.findall(r"^>+\s*(?:JL|RA|CC\d*)\s*[「\"]([^」\"]+)[」\"]\s*[:：]", disc, re.M)
        ask = f'<div class="ask">❓ {inline(sec(q["sec"], "Question"))}</div>'
        dia = (f'<div class="dia">{body(sec(q["sec"], "Diagram"))}</div>'
               if sec(q["sec"], "Diagram") else "")
        for qt in quoted:
            e = esc(qt)
            for tgt in ("ask", "fs"):
                cur = {"ask": ask, "fs": fs}[tgt]
                if e in cur:
                    new = cur.replace(e, f'<mark>{e}</mark>', 1)
                    if tgt == "ask":
                        ask = new
                    else:
                        fs = new
                    break
        cards.append(
            f'<section class="slide q {cls}" id="{q["id"]}"'
            f' data-title="{esc(q["title"])}" data-file="{esc(q.get("file",""))}">'
            f'<div class="qh"><span class="qid">{q["id"]}</span>'
            f'<span class="pill {cls}">{tok} {esc(lab)}</span>'
            f'<span class="mut">{esc(who)}</span>'
            f'<span class="mut">· {inline(q["method"])}</span>'
            f'<span class="src">{esc(q.get("file",""))}</span>'
            f'<a class="top" href="#top">↑ Index</a></div>'
            f'<h2 class="h2"><span class="hid">{q["id"]}</span>{inline(q["title"])}</h2>'
            + ask + dia
            + f'{fs}<div class="folds">{folds}</div>{nav}</section>')

    ctx = ""
    if meta["theme"]:
        ctx += (f'<details class="ctx"><summary>🦴 Topic —— 这块板在干嘛</summary>'
                f'<div class="fb">{body(meta["theme"])}</div></details>')
    if meta["pipeline"]:
        ctx += (f'<details class="ctx"><summary>🔄 Pipeline —— 这些 Q 怎么排</summary>'
                f'<div class="fb">{body(meta["pipeline"])}</div></details>')

    return TPL.format(title=esc(meta["title"]), spine=inline(meta["spine"]),
                      close=inline(meta["close"]), bar=bar, done=done, n=n,
                      ctx=ctx, index=idx, cards="\n".join(cards), js=JS)


JS = r"""
<script>
/* ─────────────────────────────────────────────────────────────
   评论层：纯增强。正文早就是真 HTML，这段脚本只负责「新增评论 + 立刻标出来」。
   剥掉这段，板照样能读，只是不能在页面上加评论。
   评论先存 localStorage（可以一直攒），点「同步进 md」时一次性写回各 Q 文件的
   ## Discussion，格式：  > JL 「被选中的原句」: 评论
   ───────────────────────────────────────────────────────────── */
(function () {
  var KEY = 'board-comments:' + location.pathname;
  var db = [];
  try { db = JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { db = []; }
  var pend = null;

  function mk(tag, id, html) {
    var e = document.createElement(tag); e.id = id; e.innerHTML = html || ''; return e;
  }
  var btn = mk('button', 'cbtn', '\u{1F4AC} 评论');
  var box = mk('div', 'cbox',
    '<div class="qq"></div><textarea placeholder="写点什么…"></textarea>' +
    '<div class="row"><select><option>JL</option><option>RA</option><option>CC</option></select>' +
    '<span style="flex:1"></span><button class="cx">取消</button>' +
    '<button class="ok cs">保存</button></div>');
  var dock = mk('button', 'cdock', '');
  var panel = mk('div', 'cpanel', '');
  var toast = mk('div', 'ctoast', '');
  [btn, box, dock, panel, toast].forEach(function (e) { document.body.appendChild(e); });
  dock.style.display = 'block';

  function save() { localStorage.setItem(KEY, JSON.stringify(db)); paint(); marks(); }
  function say(m) {
    toast.textContent = m; toast.style.display = 'block';
    clearTimeout(toast._t); toast._t = setTimeout(function () {
      toast.style.display = 'none'; }, 2600);
  }

  /* ── 立刻把被评论的句子标出来 ───────────────────────────── */
  function clearMarks() {
    document.querySelectorAll('span.cmk').forEach(function (e) { e.remove(); });
    document.querySelectorAll('mark.pend').forEach(function (m) {
      var p = m.parentNode;
      while (m.firstChild) p.insertBefore(m.firstChild, m);
      p.removeChild(m); p.normalize();
    });
  }
  function wrapAt(node, i, len, idx) {
    var r = document.createRange();
    r.setStart(node, i); r.setEnd(node, i + len);
    var m = document.createElement('mark');
    m.className = 'pend'; m.setAttribute('data-i', idx);
    try { r.surroundContents(m); }
    catch (e) { m.appendChild(r.extractContents()); r.insertNode(m); }
    var s = document.createElement('span');
    s.className = 'cmk'; s.textContent = '\u{1F4AC}'; s.setAttribute('data-i', idx);
    s.title = db[idx].who + '：' + db[idx].text;
    m.parentNode.insertBefore(s, m.nextSibling);
    return true;
  }
  function hit(sec, q, idx) {
    var tries = [q, q.replace(/\s+/g, ' ').trim(), q.replace(/\s+/g, '').slice(0, 18)];
    for (var k = 0; k < tries.length; k++) {
      var probe = tries[k];
      if (!probe || probe.length < 2) continue;
      var w = document.createTreeWalker(sec, NodeFilter.SHOW_TEXT, null);
      var n;
      while ((n = w.nextNode())) {
        if (n.parentNode.closest && n.parentNode.closest('.folds')) continue;
        var i = n.nodeValue.indexOf(probe);
        if (i >= 0) return wrapAt(n, i, probe.length, idx);
      }
    }
    return false;
  }
  function marks() {
    clearMarks();
    db.forEach(function (c, i) {
      var sec = document.getElementById(c.id);
      c.lost = !(sec && hit(sec, c.quote, i));
    });
    document.querySelectorAll('span.cmk').forEach(function (s) {
      s.onclick = function () { panel.style.display = 'block'; flash(+s.getAttribute('data-i')); };
    });
  }
  function flash(i) {
    var el = panel.querySelector('[data-row="' + i + '"]');
    if (!el) return;
    el.scrollIntoView({ block: 'nearest' });
    el.style.background = 'rgba(255,214,0,.25)';
    setTimeout(function () { el.style.background = ''; }, 1200);
  }

  /* ── 选中 → 冒出按钮 ─────────────────────────────────────── */
  document.addEventListener('mouseup', function (ev) {
    if (box.contains(ev.target) || panel.contains(ev.target) || ev.target === btn) return;
    setTimeout(function () {
      var s = window.getSelection();
      var txt = s && String(s).trim();
      if (!txt || txt.length < 2) { btn.style.display = 'none'; return; }
      var node = s.anchorNode;
      node = node.nodeType === 1 ? node : node.parentNode;
      var q = node.closest && node.closest('section.q');
      if (!q) { btn.style.display = 'none'; return; }
      var r = s.getRangeAt(0).getBoundingClientRect();
      pend = { id: q.id, file: q.getAttribute('data-file') || '', quote: txt };
      btn.style.left = (r.left + window.scrollX) + 'px';
      btn.style.top = (r.bottom + window.scrollY + 7) + 'px';
      btn.style.display = 'block';
    }, 0);
  });

  btn.onclick = function () {
    btn.style.display = 'none';
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
    db.push({ id: pend.id, file: pend.file, quote: pend.quote,
              who: box.querySelector('select').value, text: v });
    box.style.display = 'none';
    window.getSelection().removeAllRanges();
    save();
    var last = db[db.length - 1];
    say(last.lost ? '已记下，但没在正文里定位到这句（面板里标了⚠）'
                  : '已记下，右下角 \u{1F4AC} ' + db.length + ' 条待同步');
  };

  /* ── 面板 ────────────────────────────────────────────────── */
  function esc(s) { return s.replace(/[&<>]/g, function (c) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]; }); }
  function line(c) { return '> ' + c.who + ' 「' + c.quote.replace(/\s+/g, ' ').trim() +
                            '」: ' + c.text; }
  function patch() {
    var by = {};
    db.forEach(function (c) { (by[c.file] = by[c.file] || []).push(line(c)); });
    return Object.keys(by).map(function (f) {
      return '### ' + f + '\n' + by[f].join('\n');
    }).join('\n\n');
  }
  function paint() {
    dock.textContent = db.length ? ('\u{1F4AC} ' + db.length + ' 条待同步')
                                 : '\u{1F4AC} 评论';
    dock.className = db.length ? 'has' : '';
    panel.innerHTML =
      '<div class="hd"><b>待同步的评论</b><span style="flex:1"></span>' +
      '<button class="ok sy">同步进 md</button>' +
      '<button class="cp">复制</button></div>' +
      (db.length ? db.map(function (c, i) {
        return '<div class="it" data-row="' + i + '"><div class="q">' + c.id +
               (c.lost ? ' <b style="color:var(--todo)">⚠ 没定位到</b> ' : ' ') +
               '「' + esc(c.quote.slice(0, 40)) + '」</div><b>' + c.who + '</b> ' +
               esc(c.text) + ' <button data-i="' + i +
               '" class="rm" style="padding:2px 8px">删</button></div>';
      }).join('')
        : '<div class="it mut">还没有。在正文里选中一句试试。</div>') +
      '<div class="hint">「同步进 md」会让你选一次这块板的文件夹，' +
      '然后把每条写进对应 Q 文件的 <code>## Discussion</code>。' +
      '写完重新跑 <code>python3 build.py</code>。</div>';
    panel.querySelectorAll('.rm').forEach(function (b) {
      b.onclick = function () { db.splice(+b.getAttribute('data-i'), 1); save(); };
    });
    panel.querySelector('.sy').onclick = sync;
    panel.querySelector('.cp').onclick = function () {
      navigator.clipboard.writeText(patch()).then(function () { say('补丁已复制'); });
    };
  }
  dock.onclick = function () {
    panel.style.display = panel.style.display === 'block' ? 'none' : 'block';
  };

  /* ── 写回 md ─────────────────────────────────────────────── */
  async function sync() {
    if (!db.length) return;
    if (!window.showDirectoryPicker) {
      navigator.clipboard.writeText(patch());
      say('此浏览器不能写文件，补丁已复制');
      return;
    }
    var dir;
    try { dir = await window.showDirectoryPicker({ mode: 'readwrite' }); }
    catch (e) { return; }
    var by = {}, done = 0, bad = [];
    db.forEach(function (c) { (by[c.file] = by[c.file] || []).push(line(c)); });
    for (var f in by) {
      try {
        var fh = await dir.getFileHandle(f);
        var txt = await (await fh.getFile()).text();
        var add = by[f].join('\n');
        if (/^## Discussion[^\n]*$/m.test(txt)) {
          txt = txt.replace(/^## Discussion[^\n]*\n/m, function (m) { return m + add + '\n'; });
        } else if (/\n## Log\b/.test(txt)) {
          txt = txt.replace(/\n## Log\b/, '\n## Discussion\n' + add + '\n\n## Log');
        } else {
          txt = txt.replace(/\s*$/, '') + '\n\n## Discussion\n' + add + '\n';
        }
        var w = await fh.createWritable();
        await w.write(txt); await w.close(); done += by[f].length;
      } catch (e) { bad.push(f + '：' + e.message); }
    }
    if (bad.length) { say('部分写失败 ' + bad.join(' / ')); }
    else { db = []; save(); say('已写回 ' + done + ' 条，重新跑 build.py'); }
  }

  paint(); marks();
})();
</script>
"""

TPL = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
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
.ir{{display:flex;gap:10px;align-items:baseline;padding:9px 13px;border:1px solid var(--line);
 border-left:4px solid var(--mut);border-radius:9px;margin:6px 0;text-decoration:none;
 color:var(--fg);background:var(--card)}}
.ir:hover{{border-color:var(--accent)}}
.ir.todo{{border-left-color:var(--todo)}}.ir.wip{{border-left-color:var(--wip)}}
.ir.done{{border-left-color:var(--done);opacity:.6}}.ir.hold{{border-left-color:var(--hold)}}
.grp{{font-size:12.5px;color:var(--mut);margin:16px 0 2px;padding-left:2px}}
.src{{font:11.5px ui-monospace,Menlo,monospace;color:var(--mut);opacity:.7}}
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
.ask{{font-size:18px;line-height:1.55;padding-left:13px;border-left:3px solid var(--accent);
 margin:0 0 18px}}
.f{{display:flex;gap:12px;margin:11px 0;align-items:flex-start}}
.fl{{flex:0 0 108px;font-size:13px;color:var(--mut);padding-top:2px}}
.f p{{margin:0 0 4px}}

/* 现在 vs 算做完：上下叠，不左右分栏 —— 两边长短不一时并排会空掉半边 */
.cmp{{display:grid;grid-template-columns:1fr;gap:12px;margin:16px 0}}
.col{{border:1px solid var(--line);border-radius:10px;padding:12px 15px;background:var(--bg)}}

/* 勾选清单：md 里写 - [ ] / - [x] */
.ck{{display:flex;gap:9px;align-items:flex-start;margin:5px 0;line-height:1.65}}
.ck .bx{{flex:0 0 auto;color:var(--mut);font-size:15px;line-height:1.6}}
.ck.on{{color:var(--mut)}}
.ck.on .bx{{color:var(--done)}}

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
#cdock{{position:fixed;right:18px;bottom:18px;z-index:42;display:none;
 background:var(--accent);color:#fff;border:none;border-radius:999px;
 padding:10px 17px;font-size:13.5px;cursor:pointer;box-shadow:0 5px 16px rgba(0,0,0,.26)}}
#cpanel{{position:fixed;right:18px;bottom:66px;z-index:42;display:none;width:390px;
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
.lg .d{{flex:0 0 auto;font:11.5px ui-monospace,Menlo,monospace;color:var(--mut)}}

/* ## 图 —— 这一题想干嘛，一张 ascii 图先说清楚 */
.dia{{margin:0 0 18px}}
.dia pre{{margin:0;padding:15px 17px;line-height:1.55}}
.q:target .dia{{margin:0 0 24px}}
.q:target .dia pre{{font-size:13px;line-height:1.6}}
.col.now{{border-left:3px solid var(--wip)}}
.col.goal{{border-left:3px solid var(--done)}}
.ch{{font-size:12.5px;color:var(--mut);margin:0 0 7px;font-weight:600}}
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
.q:target .ask{{font-size:21px;line-height:1.55;border-left:none;padding-left:0;
 color:var(--mut);margin:0 0 26px}}
.q:target .cmp{{gap:22px;margin:0 0 22px}}
.q:target .col{{border:none;border-radius:0;background:none;padding:0 0 0 15px}}
.q:target .col.now{{border-left:2px solid var(--wip)}}
.q:target .col.goal{{border-left:2px solid var(--done)}}
.q:target .ch{{font-size:13px;margin-bottom:9px}}
.q:target .col p{{font-size:16px;line-height:1.75}}
/* 「为什么在这块板」在幻灯片上也排成一栏，跟上面两栏同一个样式，不再是左标签 */
.q:target .f{{display:block;margin:0;border-left:2px solid var(--line);padding-left:15px}}
.q:target .fl{{display:block;flex:none;font-size:13px;margin:0 0 9px;font-weight:600}}
.q:target .f p{{font-size:16px;line-height:1.75;margin:0 0 6px}}
.q:target .folds{{margin-top:auto;padding-top:18px}}
.folds{{margin-top:16px;border-top:1px dashed var(--line);padding-top:8px}}
.fold{{margin:3px 0}}
.fold>summary{{cursor:pointer;color:var(--mut);font-size:14px;list-style:none;padding:4px 0}}
.fold[open]>summary{{color:var(--fg)}}
.fb{{padding:5px 0 8px 16px;font-size:14.5px}}
.cmt{{border-left:3px solid var(--mut);padding:3px 0 3px 10px;margin:5px 0}}
.cmt b{{font-size:11px;letter-spacing:.4px;margin-right:5px}}
.cmt .qt{{background:rgba(217,164,6,.18);border-bottom:1px solid rgba(217,164,6,.55);
 padding:0 2px;border-radius:2px}}
.cmt.jl{{border-color:var(--accent)}}.cmt.jl b{{color:var(--accent)}}
.cmt.ra{{border-color:var(--ra)}}.cmt.ra b{{color:var(--ra)}}
.mut{{color:var(--mut)}}
code{{background:var(--pre);padding:1px 5px;border-radius:4px;font:13px ui-monospace,Menlo,monospace}}
pre{{background:var(--pre);border:1px solid var(--line);border-radius:8px;padding:11px 13px;
 margin:8px 0;overflow-x:auto;font:12.5px/1.6 ui-monospace,Menlo,monospace;white-space:pre}}
img{{max-width:100%;border:1px solid var(--line);border-radius:8px}}
.foot{{margin-top:44px;padding-top:14px;border-top:1px solid var(--line);
 color:var(--mut);font-size:12.5px}}
</style></head><body class="single"><div class="wrap" id="top">

<h1 class="h1">{title}</h1>
<div class="spine"><p><b>🦴 Spine</b> {spine}</p><p><b>🏁 Close when</b> {close}</p></div>
<p class="bar">{bar}  {done}/{n} settled</p>

{ctx}

<h3 class="sec">ALL QUESTIONS<span class="hint">点任意一行 → 只看那一题</span></h3>
<div class="idx">{index}</div>

{cards}

<p class="foot">内容来自同目录的 <code>board.md</code>（全局）和 <code>QX-xxx.md</code>（一题一文件）。
改那些文件，然后重新生成这一页：<code>python3 build.py</code>。<br>这一页是纯静态 HTML，没有任何脚本 ——
双击、VS Code 预览、发给别人，都能正常显示。</p>
</div>{js}</body></html>
"""

if __name__ == "__main__":
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    if src.is_dir():
        meta, qs, warn = parse_dir(src)
        out = src / "board.html"
    elif src.exists():
        meta, qs, warn = parse_file(src.read_text(encoding="utf-8"))
        out = src.with_suffix(".html")
    else:
        sys.exit(f"找不到 {src}")
    out.write_text(render(meta, qs), encoding="utf-8")
    txt = out.read_text(encoding="utf-8")
    # 真正要保的性质不是「没有 script」，而是「关掉 script 页面照样完整」。
    # 评论层是纯增强，所以改成直接验这一条：剥掉所有 <script> 之后，
    # 每个 Q 仍在，正文仍在。
    bare = re.sub(r"<script.*?</script>", "", txt, flags=re.S)
    assert bare.count('class="slide q') == len(qs), "剥掉 JS 后少了 Q"
    plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", bare.split("<body", 1)[1])).strip()
    assert len(plain) > 1200, f"剥掉 JS 后正文只剩 {len(plain)} 字"
    print(f"✅ {out} · {len(qs)} 个 Q · 无 JS 时仍有 {len(plain)} 字正文 · 评论层 {txt.count(chr(60)+'script')} 段")
    for w in warn:
        print(f"⚠️  {w}")
