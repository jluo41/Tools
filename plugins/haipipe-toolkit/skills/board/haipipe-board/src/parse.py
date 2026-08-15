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
                board_map=f("board-map"),  # optional shared map URL for a static reader
                dialect=f("dialect"),       # opt-in: `paper` resolves \citep{} at build time
                paper_root=f("paper-root"),  # where that paper's .bib / displays / 1-probes are
                theme=sec(bs, "Topic"), pipeline=sec(bs, "Pipeline"),
                structure=sec(bs, "Board Structure"),
                # `## Board Map` is the ASCII map (JL 260730): the map a static
                # host can always draw, and the one whose ids travel. It wins
                # over the `board-map:` canvas URL when both are present.
                map=sec(bs, "Board Map"),
                # `## Related Folders` (QB2/QA0, JL 260731): the folders this
                # board touches, embedded file-by-file into the RELATED FOLDERS
                # index fold at build time.
                related=sec(bs, "Related Folders"), dir="")


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

    `ref/page-template.md` has always told authors a note "is dropped at generation
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
        # route: outward | inward is the evidence-page type key (JL 260806):
        # it sits in the head, right after owner:/method:, and resolves the
        # page to for-literature or for-value where the filename cannot.
        "route": "",
        # page-type: is the OTHER type key. `route:` resolves the two evidence
        # variants; this one names the variant outright, and a plugin surface
        # gates on it (JL 260807), so it has to reach the page dict and the DOM.
        "page_type": "",
        "session": "",
        "requires": "",
        "style_from": "",
        "provides": "",
        "contract_source_hash": "",
    }
    while i < len(lines) and not lines[i].startswith("## "):
        m = re.match(
            r"^(state|owner|method|route|page-type|session|requires|style-from|provides|contract-source-hash):\s*(.*)$",
            lines[i].strip(),
        )
        if m:
            meta[m.group(1).replace("-", "_")] = m.group(2).strip()
        i += 1
    # Author notes are dropped ONCE, here, so every downstream renderer sees clean
    # text. Doing it per-renderer was the old shape and it missed paths: a comment
    # written under ## Question came out as escaped `&lt;!--` prose on the page,
    # while ref/page-template.md had always promised it "is dropped at generation
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
        # A NAMED Q family (JL 260727): `Q-Skill-haipipe-board.md`. Same idea as
        # the named S families, and for the same reason: a skill page is
        # identified by WHAT IT IS, not by a position in a numbered queue.
        # `QS1` would say a skill page is the first of a list; `Q-Skill-<name>`
        # says which skill it is, which is the only thing a reader wants from
        # the id, and it stays greppable across the repo.
        named_qm = re.match(r"Q-([A-Z][A-Za-z]*)-(.+)$", p.stem)
        # A SKILL page is its own kind (JL 260731: "could we just remove Q, from
        # Q-Skill to be Skill ... Like Skill will be a special Page"). It is not a
        # decision, so the `Q` prefix was a lie: a skill page mirrors a shipped
        # unit and closes when that unit ships, never by a checkbox reaching zero.
        # The grammar is the S grammar minus the family, `Skill-<unit>-<slug>`, so
        # the unit orders the roster and the slug still says which skill it is.
        skill_m = re.match(r"Skill-(\d+)-(.+)$", p.stem)
        # A DESIGN page replaced the skill page (JL 260815: "we don't have the
        # page for the Skill anymore. It will be the design"): the same grammar,
        # but the prefix now names what the page DOES — argue the unit's design,
        # settle on a selection, and carry the unit's bytes in its plugins —
        # rather than the dead mirror kind. Skill-* stays parseable for
        # archives and for boards that have not converted.
        design_m = re.match(r"Design-(\d+)-(.+)$", p.stem)
        # An AGENT is not a skill (JL 260731: "we will call it Agent-1 ...
        # Below the skill"): a skill is LOADED into a context, an agent is
        # DISPATCHED into a fresh one. Same grammar, own prefix, sorts after
        # the Skill rows so the roster reads kind by kind.
        agent_m = re.match(r"Agent-(\d+)-(.+)$", p.stem)
        # A MEETING is neither (QC10, JL 260731): a skill is LOADED, an agent is
        # DISPATCHED, a meeting HAPPENED. Same grammar again, its own prefix,
        # and it sorts last so the roster reads kind by kind. It closes when its
        # decisions have been routed onto the pages that own them, never by a
        # checkbox count, which is why it stays outside the settled-question sum.
        meeting_m = re.match(r"Meeting-(\d+)-(.+)$", p.stem)
        full_sm = re.match(
            # The unit is a NUMBER (a manuscript section), a single CAPITAL
            # (an appendix), or a CAPITALISED WORD. The third is for a page that
            # is not a manuscript unit at all: a family's control page, which
            # `board.md` describes as answering "only what no single asset can".
            # Display and Appendix put theirs at unit 0; Main could not, because
            # unit 0 there is the Abstract, so `S-Main-Dash` needed a name
            # (JL 2026-07-27). Added last in the alternation, so a numbered unit
            # still matches first and no existing page re-parses.
            #
            # A number plus a letter plus a TAIL is a VARIANT of that member
            # (JL 2026-07-28): same claim and same job under a different
            # specification, inheriting its parent's letter so that adding one
            # renames nothing. `S-Display-4al2` is `4a` on the binary trait_l2
            # exposure. It leads the alternation because `\d+[a-z]?` would
            # otherwise consume `4a` and then fail the `-|$` that follows,
            # which made such a page silently unparseable rather than rejected.
            r"S-(Open|Seed|Work|Venue|Literature|Value|Display|Main|Appendix|Submission|Round|Label)-"
            # A CAPITAL PLUS DIGITS is a per-unit member of a lettered series
            # (JL 2026-08-02, choosing option A): in Work the letter says the
            # STAGE and the number says the UNIT, so `S-Work-R` is the resources
            # control page and `S-Work-R1` is one resource. It leads `[A-Z]`
            # because that alternative would otherwise consume the `R` of `R1`
            # and then fail the `-|$`, making such a page silently unparseable.
            r"(\d+[a-z][a-z0-9]+|\d+[a-z]?|[A-Z]\d+|[A-Z]|[A-Z][a-z]+)(?:-|$)",
            p.stem,
            re.I,
        )
        legacy_sm = re.match(r"(SM|SA|S)(\d+[a-z]?)", p.stem, re.I)
        sm = full_sm or legacy_sm
        if qm or sm or named_qm or skill_m or agent_m or meeting_m or design_m:
            if design_m:
                family = "design"
                page_id = f"Design-{design_m.group(1)}"
                # design rows sit where skill rows sat: after every lettered group
                key = (0, "￾", int(design_m.group(1)), "")
                kind = "design"
            elif meeting_m:
                family = "meeting"
                page_id = f"Meeting-{meeting_m.group(1)}"
                # sorts after every Skill and Agent row
                key = (0, "\ufffe1", int(meeting_m.group(1)), "")
                kind = "meeting"
            elif skill_m:
                family = "skill"
                page_id = f"Skill-{skill_m.group(1)}"
                # after every lettered group, before the older Q-<Family> rows
                key = (0, "\ufffe", int(skill_m.group(1)), "")
                kind = "skill"
            elif agent_m:
                family = "agent"
                page_id = f"Agent-{agent_m.group(1)}"
                # "\ufffe0" sorts after every Skill row and before "\uffff"
                key = (0, "\ufffe0", int(agent_m.group(1)), "")
                kind = "agent"
            elif named_qm and not qm:
                family = named_qm.group(1).lower()
                page_id = f"Q-{named_qm.group(1)}-{named_qm.group(2)}"
                # after every lettered group, in name order
                key = (0, "\uffff" + family, 0, named_qm.group(2))
                kind = "question"
            elif qm:
                key = (0, qm.group(1), int(qm.group(2)), qm.group(3))
                page_id = "Q" + qm.group(1) + qm.group(2) + qm.group(3)
                kind = "question"
                family = ""
            elif full_sm:
                family = full_sm.group(1).lower()
                # NORMALISE THE UNIT THE WAY THE COMPOSER DOES, and no other way
                # (260803). A bare `.upper()` turned `Dash` into `DASH` and the
                # Display block+member `2a` into `2A`, so every id a person wrote
                # in prose missed the page it names and rendered as a dead
                # same-page fragment. `cli/stage.py resolve_filename()` is the one
                # place a name is MADE; the reader has to agree with it or the two
                # sides disagree about a page that already exists on disk.
                unit = full_sm.group(2)
                if re.fullmatch(r"[A-Za-z]", unit):
                    unit = unit.upper()                      # S-Appendix-C
                elif re.fullmatch(r"[A-Za-z]\d+", unit):
                    unit = unit[0].upper() + unit[1:]        # S-Work-R1
                elif re.fullmatch(r"[A-Za-z][a-z]+", unit):
                    unit = unit[0].upper() + unit[1:].lower()  # S-Main-Dash
                # a number, or a block+member like `4a` / `4al2`, keeps its case
                family_order = {
                    "open": 0,
                    "seed": 0,
                    "work": 1,
                    "venue": 2,
                    "literature": 3,
                    "value": 4,
                    "display": 5,
                    "main": 6,
                    "appendix": 7,
                    "submission": 8,
                    "round": 9,
                    "label": 10,
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
