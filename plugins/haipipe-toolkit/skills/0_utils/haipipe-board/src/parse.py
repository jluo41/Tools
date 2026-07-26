"""md -> data (QB5): board.md, Q files, folder discovery, legacy blocks.
parse_board fills body.LINKS (mutation only — same dict object inline() reads)."""
import re

from .body import LINKS
from .common import page_files, sec
from .stage_contract import contract_status


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
                session=f("session"),   # 整板会话的 id（QD5）——serve.py 记在 board.md 头部
                excalidraw=f("excalidraw"),  # the board's own Excalidraw host, e.g.
                                            # http://127.0.0.1:5610 (self-hosted, QA4a)
                dialect=f("dialect"),       # opt-in: `paper` resolves \citep{} at build time
                paper_root=f("paper-root"),  # where that paper's .bib / 0-displays / 1-probes are
                theme=sec(bs, "Topic"), pipeline=sec(bs, "Pipeline"), dir="")


def parse_doc(d, paths):
    """Pages `doc:` line -> a doc-slide entry (QF2): the listed files render
    directly on one slide, no Q file involved. id = the first file's parent
    folder when it has one (the folder IS the slide's identity:
    `2b-pitch/PITCH_LOG.md` -> `2b-pitch`; also keeps two `README.md`s from
    colliding), else the file's stem. title = the first file's `# ` or setext
    title, else the id."""
    if "/" in paths[0]:
        stem = paths[0].rsplit("/", 2)[-2]
    else:
        stem = paths[0].rsplit("/", 1)[-1]
        stem = stem[:-3] if stem.endswith(".md") else stem
    title = stem
    first = d / paths[0]
    if first.is_file():
        lines = first.read_text(encoding="utf-8").split("\n")
        for i, ln in enumerate(lines):
            if not ln.strip():
                continue
            if ln.startswith("# "):
                title = ln[2:].strip()
            elif (i + 1 < len(lines)
                  and re.match(r"^\s*(=+|-+)\s*$", lines[i + 1])
                  and len(lines[i + 1].strip()) >= 3):
                title = ln.strip()
            break
    return dict(id=stem, title=title, group="", file="", kind="doc",
                files=list(paths), state="", owner="", method="", session="",
                sec={})


def strip_notes(md):
    """Drop `<!-- ... -->` author notes, BEFORE the text is cut into sections.

    `ref/q-template.md` has always told authors a note "is dropped at generation
    either way". It was not: the only strip lived in the Stage Contract path, and
    the template's own notes happen to sit above the first `## `, where nothing
    renders. Written anywhere else a note came out as escaped `&lt;!--` prose
    (found 260726, adding a menu of optional sections to the ＋ button's stub).

    Order matters and cost an attempt to learn: `split_sections` reads any line
    starting `## ` as a heading, including one INSIDE a comment, so a note that
    lists `## Diagram` used to be torn in half and left a phantom section behind.
    Stripping first is what makes such a menu writable at all.

    Fenced blocks are protected, so a figure may still show a comment on purpose,
    and `<!-- haipipe:... -->` is kept because stage_contract reads those markers.
    """
    if "<!--" not in md:
        return md
    parts = re.split(r"(```)", md)
    inside = False
    for i, seg in enumerate(parts):
        if seg == "```":
            inside = not inside
        elif not inside:
            parts[i] = re.sub(r"<!--(?!\s*haipipe:).*?-->", "", seg, flags=re.S)
    return "".join(parts)


def parse_page(qid, txt, group="", file="", kind="question", family=""):
    """One Q/S page (title, meta lines, and ## sections) -> data dict."""
    lines = txt.split("\n")
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    qt = lines[i].lstrip("# ").strip() if i < len(lines) else qid
    i += 1
    meta = {
        "state": "🔴",
        "owner": "",
        "method": "",
        "session": "",
        "requires": "",
        "style_from": "",
        "provides": "",
        "contract_source_hash": "",
    }
    while i < len(lines) and not lines[i].startswith("## "):
        m = re.match(
            r"^(state|owner|method|session|requires|style-from|provides|contract-source-hash):\s*(.*)$",
            lines[i].strip(),
        )
        if m:
            meta[m.group(1).replace("-", "_")] = m.group(2).strip()
        i += 1
    # Author notes are dropped ONCE, here, so every downstream renderer sees clean
    # text. Doing it per-renderer was the old shape and it missed paths: a comment
    # written under ## Question came out as escaped `&lt;!--` prose on the page,
    # while ref/q-template.md had always promised it "is dropped at generation
    # either way" (found 260726). Fenced blocks are protected so a figure may still
    # show one, and `<!-- haipipe:contract:* -->` is kept because stage_contract
    # reads those markers back out of the rendered section.
    body_md = strip_notes("\n".join(lines[i:]))
    return dict(id=qid, title=qt, group=group, file=file, kind=kind, family=family,
                sec=split_sections(body_md), **meta)


def parse_q(qid, txt, group="", file=""):
    """Backward-compatible question parser used by legacy single-file boards."""
    return parse_page(qid, txt, group, file, "question")


def parse_file(md):
    """legacy single-file board: [BOARD] + [Q1] + [Q2] ... blocks"""
    B = split_blocks(md)
    qs = [parse_q(k, B[k]) for k in sorted(
        [k for k in B if re.fullmatch(r"Q\d+", k)], key=lambda x: int(x[1:]))]
    return parse_board(B.get("BOARD", "")), qs, []


def parse_dir(d):
    """house form: board.md + Q<n>-<slug>.md files in one folder tree.

    The Q files ARE the board — binding is by PATH (under the board folder),
    the way 1-probes/ does it, so a question can never desync from its Pages
    entry. board.md's optional `## Pages` only sets ORDER and GROUPING; a file
    on disk that nobody listed is still rendered (under ⚠️), never silently
    dropped. Since QC3 a Q file may sit in a subfolder (its home folder); the
    Pages section keeps listing bare filenames.
    """
    bp = d / "board.md"
    board = re.sub(r"^\[BOARD\]\s*\n", "",
                   bp.read_text(encoding="utf-8") if bp.exists() else "")
    # 文件名前缀就是这题的编号：Q1 / QA1 / QAa1 / Q0s1。组是大写字母（可带一个
    # 小写子组字母，QAa/QAb 这样把一个组一分为二）或「数字+小写」（Q0s 这类
    # 排在字母组之前的前置组），数字是组内序号。
    disk, dupes = {}, []
    for p in page_files(d):
        qm = re.match(r"Q([0-9][a-z]|[A-Z]*[a-z]?)(\d+)([a-z]?)", p.stem)
        full_sm = re.match(
            r"S-(Seed|Work|Venue|Display|Main|Appendix|Submission)-(\d+|[A-Z])(?:-|$)",
            p.stem,
            re.I,
        )
        legacy_sm = re.match(r"(SM|SA|S)(\d+[a-z]?)", p.stem, re.I)
        sm = full_sm or legacy_sm
        if qm or sm:
            if qm:
                key = (0, qm.group(1), int(qm.group(2)), qm.group(3))
                page_id = "Q" + qm.group(1) + qm.group(2) + qm.group(3)
                kind = "question"
                family = ""
            elif full_sm:
                family = full_sm.group(1).lower()
                unit = full_sm.group(2).upper()
                family_order = {
                    "seed": 0,
                    "work": 1,
                    "venue": 2,
                    "display": 3,
                    "main": 4,
                    "appendix": 5,
                    "submission": 6,
                }[family]
                unit_key = (0, int(unit)) if unit.isdigit() else (1, unit)
                key = (1, family_order, *unit_key)
                page_id = f"S-{family.title()}-{unit}"
                kind = "stage"
            else:
                prefix = legacy_sm.group(1).upper()
                order = re.match(r"(\d+)([a-z]?)", legacy_sm.group(2), re.I)
                family = {"S": "stage", "SM": "main", "SA": "appendix"}[prefix]
                family_order = {"stage": 0, "main": 1, "appendix": 2}[family]
                key = (1, family_order, 0, int(order.group(1)), order.group(2))
                page_id = prefix + legacy_sm.group(2)
                kind = "stage"
            if p.name in disk:
                dupes.append(
                    f"{p.name} appears twice "
                    f"({disk[p.name][2].relative_to(d)} and {p.relative_to(d)}); "
                    "keeping the first")
                continue
            disk[p.name] = (key, page_id, p, kind, family)
    pages_txt = sec(split_sections(board), "Pages")
    if not disk and not re.search(r"^doc:", pages_txt, re.M):
        return parse_file(board)        # legacy: everything in one board.md

    order, seen, warn, group, gintro = [], set(), dupes, "", {}
    in_fence = False
    for raw in pages_txt.split("\n"):
        ln = raw.strip()
        if in_fence:                       # 组介绍里的 ``` ascii 图：整段按原样收，不 strip（保住对齐）
            gintro.setdefault(group, []).append(raw)
            if ln.startswith("```"):
                in_fence = False
            continue
        if ln.startswith("### "):
            group = ln[4:].strip()
        elif ln.startswith("doc:"):
            # doc slide（QF2，JL 260724）：这一行列出的源文件直接渲染成一页 ——
            # 没有 Q 文件、没有 state/清单/评论；标题取第一份文件的标题。
            paths = ln[4:].split()
            if paths:
                order.append((group, parse_doc(d, paths)))
        elif ln.endswith(".md"):
            name = ln.lstrip("-*· ").strip()
            if name in disk:
                order.append((group, disk[name][2]))
                seen.add(name)
            else:
                warn.append(f"{name} is listed in Pages but no such file exists")
        elif ln.startswith("```") and group:
            in_fence = True
            gintro.setdefault(group, []).append(raw)
        elif ln and group:
            # Plain lines between a "### " heading and its first .md line are the
            # GROUP INTRO (QC2, JL 260724): line 1 = the sentence that always shows
            # under the header; the rest = the click-to-expand "what / why" body,
            # which MAY include a ``` ascii diagram (JL 260724).
            gintro.setdefault(group, []).append(raw)
    listed = bool(order)
    for name, (key, qid, p, kind, family) in sorted(disk.items(), key=lambda kv: kv[1][0]):
        if name not in seen:
            if listed:
                warn.append(f"{name} is not listed in board.md's ## Pages")
            order.append(("⚠️ Not in Pages" if listed else "", p))

    qs = [p if isinstance(p, dict)
          else parse_page(disk[p.name][1], p.read_text(encoding="utf-8"), g,
                          p.relative_to(d).as_posix(), disk[p.name][3], disk[p.name][4])
          for g, p in order]
    for q, (g, p) in zip(qs, order):
        if isinstance(p, dict):
            q["group"] = g
    by_id = {q["id"].casefold(): q for q in qs if q.get("file")}
    for q in qs:
        status = contract_status(d, q, by_id)
        if status:
            warn.append(status)
    meta = parse_board(board)
    meta["dir"] = str(d.resolve())
    meta["groups"] = {g: ls for g, ls in gintro.items() if ls}
    return meta, qs, warn
