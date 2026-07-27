#!/usr/bin/env python3
"""board folder -> board.html (static content; scripts are optional enhancement).

haipipe-board v0.1.0 — v0-series: never goes to 1.0.0 without JL saying so.

    python3 build.py [board-dir | board.md]

House form (one page, one file):
    <board-dir>/
      board.md        # title / spine: / close: / source: / ## 主题 / ## 流水线
      Q1-<slug>.md    # title / state: / owner: / method: / ## 问题 ...
      S-Seed-0-<slug>.md  # optional named lifecycle page; same grammar + ## Content
      Q2-<slug>.md
      board.html      <- generated
Legacy single-file boards ([BOARD]/[Qn] blocks in one board.md) still build.
Q and S pages may sit in subfolders of the board.

Why static: VS Code's Live Preview webview blocks inline JS, and html-ppt's
base.css hides every `.slide` until runtime.js adds `.is-active`. A JS-built
page therefore renders pure white in the one place the user actually opens it.
So every question is written into the file as a real <section>, collapsibles use
native <details>, and jumping uses plain anchors. Nothing needs JS to be read.

Follows html-ppt conventions where free: `.slide` sections with `data-title`,
`body.single` (base.css's own no-JS escape hatch), `.h1/.h2/.lede/.blt` classes,
academic-report palette. So the same file can later be handed to runtime.js for
presenter mode without rewriting the content.

QB5: this file is a thin entry; the code lives in src/ by topic
(common · parse · body · page_board · page_question · page_stage).
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from src import body as boardbody              # noqa: E402
from src.parse import parse_dir, parse_file    # noqa: E402
from src.page_board import render, scrub_cjk_comments, to_json  # noqa: E402

# Marker SYNTAX a dialect would resolve. Used only to warn when a board writes
# markers and declares no dialect; matching this is not knowing what a paper is.
#
# Code spans are stripped FIRST, and that is the whole precision of the check: a
# board that MEANS a marker writes it in prose, while a board that DISCUSSES the
# syntax quotes it. Measured 2026-07-26 across the four real boards: boardform
# 13 mentions and probe-qa 2, all inside code, none meant.
MARKERISH = re.compile(r"\\cite[pt]?\{|\{VAL:\?|\[Q-[A-Za-z]")
_FENCE = re.compile(r"```.*?```", re.S)
_INLINE = re.compile(r"`[^`\n]*`")


def _meant_markers(text):
    """Markers written as PROSE, with quoted syntax removed."""
    return len(MARKERISH.findall(_INLINE.sub("", _FENCE.sub("", text))))

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--json"]
    as_json = "--json" in sys.argv[1:]
    sys.argv = [sys.argv[0]] + args
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    boardbody.BASE = (target if target.is_dir() else target.parent).resolve()
    if target.is_dir():
        meta, qs, warn = parse_dir(target)
        out = target / "board.html"
    elif target.exists():
        meta, qs, warn = parse_file(target.read_text(encoding="utf-8"))
        out = target.with_suffix(".html")
    else:
        sys.exit(f"not found: {target}")
    # The paper dialect, if this board declares it. Built once, before rendering,
    # so every chip ships resolved and hover works with no script at all.
    #
    # A DIALECT IS DELETABLE (QBc5). The board must not depend on knowing what a
    # paper is, so the import is guarded and a board that does not declare
    # `dialect: paper` never reaches the module at all: delete src/dialect_paper.py
    # and every other board on disk still renders byte-identical.
    boardbody.PAPER = None
    boardbody.EXCAL_HOST = meta.get("excalidraw", "").split("#", 1)[0].strip().rstrip("/")
    if meta.get("dialect", "").split("#", 1)[0].strip():
        try:
            from src import dialect_paper            # noqa: E402
            boardbody.PAPER = dialect_paper.load(boardbody.BASE, meta)
        except ImportError:
            print("⚠️  dialect declared but no dialect module; markers stay plain text")
    else:
        # A board that writes marker SYNTAX and declares no dialect renders it as
        # plain text and silently gets no cross-check. That is the one way this
        # seam fails without saying anything, so say it here.
        #
        # The trigger is the board's own CONTENT, never its folder name: build.py
        # must not learn what a paper is (the dialect stays deletable, QBc5).
        _hits = sum(
            _meant_markers(f.read_text(encoding="utf-8", errors="ignore"))
            for f in sorted(target.glob("**/*.md"))
        ) if target.is_dir() else _meant_markers(target.read_text(encoding="utf-8", errors="ignore"))
        if _hits:
            print(f"⚠️  {_hits} marker(s) found and NO `dialect:` declared, so they render as")
            print("    plain text and nothing cross-checks them. Add to board.md frontmatter:")
            print("        dialect: paper")
            print("        paper-root: ..        # where the .bib, displays/ and 1-probes/ live")
    boardbody.FACE_IDS = {q["id"] for q in qs}
    if as_json:
        print(to_json(meta, qs, warn))
        sys.exit(0)
    out.write_text(scrub_cjk_comments(render(meta, qs)), encoding="utf-8")
    txt = out.read_text(encoding="utf-8")
    # 真正要保的性质不是「没有 script」，而是「关掉 script 页面照样完整」。
    # 评论层是纯增强，所以改成直接验这一条：剥掉所有 <script> 之后，
    # 每个 page 仍在，正文仍在。
    bare = re.sub(r"<script.*?</script>", "", txt, flags=re.S)
    assert bare.count('class="slide q') == len(qs), "a page went missing after stripping JS"
    plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", bare.split("<body", 1)[1])).strip()
    assert len(plain) > 1200, f"only {len(plain)} chars of body left after stripping JS"
    print(f"✅ {out} · {len(qs)} pages · {len(plain)} chars of body survive with JS stripped · {txt.count(chr(60)+'script')} script block(s)")
    for w in warn:
        print(f"⚠️  {w}")
    # A chip can only appear where the board RENDERS text. The manuscript's own
    # .tex is reached only when a page embeds it, so audit it directly and say
    # so out loud rather than let a clean board imply a clean paper.
    if boardbody.PAPER is not None:
        rows = boardbody.PAPER.audit()
        if rows:
            print(f"📄 {len(rows)} unresolved marker(s) in the paper's .tex, "
                  f"which this board does not render:")
            for path, line, kind, why in rows:
                print(f"    {kind:<8} {path}:{line}  {why}")
