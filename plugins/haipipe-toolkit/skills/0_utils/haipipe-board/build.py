#!/usr/bin/env python3
"""board folder -> board.html (static content; scripts are optional enhancement).

haipipe-board v0.1.0 — v0-series: never goes to 1.0.0 without JL saying so.

    python3 build.py [board-dir | board.md]

House form (one face, one file):
    <board-dir>/
      board.md        # title / spine: / close: / source: / ## 主题 / ## 流水线
      Q1-<slug>.md    # title / state: / owner: / method: / ## 问题 ...
      S0-<slug>.md    # optional lifecycle stage; same grammar + ## Content
      Q2-<slug>.md
      board.html      <- generated
Legacy single-file boards ([BOARD]/[Qn] blocks in one board.md) still build.
Q and S faces may sit in subfolders of the board.

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
    if as_json:
        print(to_json(meta, qs, warn))
        sys.exit(0)
    out.write_text(scrub_cjk_comments(render(meta, qs)), encoding="utf-8")
    txt = out.read_text(encoding="utf-8")
    # 真正要保的性质不是「没有 script」，而是「关掉 script 页面照样完整」。
    # 评论层是纯增强，所以改成直接验这一条：剥掉所有 <script> 之后，
    # 每个 face 仍在，正文仍在。
    bare = re.sub(r"<script.*?</script>", "", txt, flags=re.S)
    assert bare.count('class="slide q') == len(qs), "a face went missing after stripping JS"
    plain = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", bare.split("<body", 1)[1])).strip()
    assert len(plain) > 1200, f"only {len(plain)} chars of body left after stripping JS"
    print(f"✅ {out} · {len(qs)} faces · {len(plain)} chars of body survive with JS stripped · {txt.count(chr(60)+'script')} script block(s)")
    for w in warn:
        print(f"⚠️  {w}")
