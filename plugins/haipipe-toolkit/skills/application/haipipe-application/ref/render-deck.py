#!/usr/bin/env python3
"""
render-deck.py
==============

Convert a DIKW-spine report.md (per ../ref/report-template.md) into an
html-ppt slide deck. One source -> two artifacts: keep report.md /
report.html as scrolling reference; emit deck/index.html for
stakeholder presentation.

Usage
-----
    render-deck.py <report.md> [--theme=academic-paper] [--out=<dir>]

Defaults
--------
  --theme  academic-paper
  --out    <report-md-parent>/deck/

Output
------
  <out>/index.html               the deck
  <out>/assets/{fonts,base,animations}.css
  <out>/assets/runtime.js
  <out>/assets/themes/<theme>.css

Conventions read from report.md
-------------------------------
  * Each '# H1' line opens a top-level section. We auto-bucket:
        "Application: ask ..."           -> cover slide
        "Answer (TL;DR)"                 -> hero/lede slide
        "D · Data" / "I · Information"   -> section divider, then
                                            one slide per '## H2' within
        "K · Knowledge" / "W · Wisdom"   -> single placeholder slide
        "Did we answer..."               -> checklist slide
        "Provenance"                     -> appendix slide
  * Optional hint comments inside a block tune the converter:
        <!-- slide-break -->         force a new slide
        <!-- supplementary -->       this content belongs in a follow-on slide
        <!-- layout: hero|grid|table|callout|image -->   override layout pick
"""

from __future__ import annotations
import argparse
import base64
import mimetypes
import re
import shutil
import subprocess
import sys
from pathlib import Path

HTML_PPT_SKILL_ROOT = Path(
    "/home/jluo41/WellDoc-SPACE/Tools/plugins/html-ppt/skills/html-ppt"
)
ASSETS_TO_COPY = [
    "assets/fonts.css",
    "assets/base.css",
    "assets/animations/animations.css",
    "assets/runtime.js",
]
DEFAULT_THEME = "academic-paper"


# --------------------------------------------------------------------------- #
#  Markdown -> HTML (per slide chunk) via pandoc
# --------------------------------------------------------------------------- #

def md_to_html(md: str) -> str:
    """Convert a markdown chunk to inline HTML via pandoc (no wrapper)."""
    if not md.strip():
        return ""
    proc = subprocess.run(
        ["pandoc", "-f", "markdown", "-t", "html"],
        input=md,
        capture_output=True,
        text=True,
        check=True,
    )
    return proc.stdout.strip()


# --------------------------------------------------------------------------- #
#  Parse report.md into a list of slides
# --------------------------------------------------------------------------- #

LAYER_HEADERS = {
    "D · Data": "D",
    "I · Information": "I",
    "K · Knowledge": "K",
    "W · Wisdom": "W",
}


def normalize_headers(md: str) -> str:
    """Convert setext-style headers (===, ---) to ATX (#, ##) for uniform parsing."""
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        nxt_s = nxt.strip()
        if ln.strip() and nxt_s and set(nxt_s) == {"="} and len(nxt_s) >= 3:
            out.append(f"# {ln.strip()}")
            i += 2
        elif (ln.strip() and nxt_s and set(nxt_s) == {"-"}
              and len(nxt_s) >= 3 and not ln.lstrip().startswith(("|", "-", "*"))):
            out.append(f"## {ln.strip()}")
            i += 2
        else:
            out.append(ln)
            i += 1
    return "\n".join(out)


def parse_slides(report_md: str, report_path: Path) -> list[dict]:
    """Return [{title, kicker, body_md, layout, notes}, ...]."""
    report_md = normalize_headers(report_md)
    lines = report_md.splitlines()

    # ---- 1. Split into H1 sections -----------------------------------------
    sections: list[tuple[str, list[str]]] = []
    cur_title, cur_body = None, []
    for ln in lines:
        m = re.match(r"^# (.+?)\s*$", ln)
        if m and not ln.startswith("##"):
            if cur_title is not None or cur_body:
                sections.append((cur_title or "", cur_body))
            cur_title, cur_body = m.group(1).strip(), []
        else:
            cur_body.append(ln)
    if cur_title is not None or cur_body:
        sections.append((cur_title or "", cur_body))

    # ---- 2. Bucket each section to slides ----------------------------------
    slides: list[dict] = []

    for title, body_lines in sections:
        body = "\n".join(body_lines).strip()
        if not title and not body:
            continue

        # cover
        if title.startswith("Application:"):
            slides.append(dict(
                title="Cover", kicker="ask · session",
                heading=title, body_md=body, layout="cover",
            ))
            continue

        # TL;DR hero
        if title.startswith("Answer"):
            slides.append(dict(
                title="TL;DR", kicker="Bottom line",
                heading=title, body_md=body, layout="hero",
            ))
            continue

        # D / I / K / W layer sections — each H2 within = one slide
        layer = next((v for k, v in LAYER_HEADERS.items() if title.startswith(k)), None)
        if layer:
            # Section divider slide
            slides.append(dict(
                title=f"Section {layer}", kicker=f"{layer} layer",
                heading=title, body_md="", layout="divider",
            ))
            # Per-H2 block
            h2_blocks = split_h2_blocks(body_lines)
            if not h2_blocks:
                # empty layer placeholder
                slides.append(dict(
                    title=f"{layer} (empty)", kicker=f"{layer} layer",
                    heading=f"{layer} · (no cards filed)",
                    body_md=body, layout="callout",
                ))
            else:
                for h2_title, h2_body in h2_blocks:
                    layout = pick_block_layout(h2_body)
                    slides.append(dict(
                        title=f"{layer}: {h2_title[:30]}",
                        kicker=f"{layer} card",
                        heading=h2_title,
                        body_md=h2_body,
                        layout=layout,
                    ))
            continue

        # "Did we answer..." checklist
        if title.startswith("Did we answer"):
            slides.append(dict(
                title="Did we answer?", kicker="Verdict",
                heading=title, body_md=body, layout="checklist",
            ))
            continue

        # Provenance / appendix
        if title.startswith("Provenance"):
            slides.append(dict(
                title="Provenance", kicker="Appendix",
                heading=title, body_md=body, layout="appendix",
            ))
            continue

        # Fallback
        slides.append(dict(
            title=title[:30], kicker="",
            heading=title, body_md=body, layout="text",
        ))

    # ---- 3. Apply <!-- slide-break --> hint --------------------------------
    expanded = []
    for s in slides:
        parts = re.split(r"<!--\s*slide-break\s*-->", s["body_md"])
        if len(parts) == 1:
            expanded.append(s)
        else:
            for i, p in enumerate(parts):
                ns = dict(s)
                ns["body_md"] = p.strip()
                if i > 0:
                    ns["kicker"] = (s["kicker"] or "") + " (cont.)"
                expanded.append(ns)
    return expanded


def split_h2_blocks(body_lines: list[str]) -> list[tuple[str, str]]:
    """Within a layer section, split body on '## H2' lines."""
    blocks: list[tuple[str, list[str]]] = []
    cur_t, cur_b = None, []
    for ln in body_lines:
        m = re.match(r"^## (.+?)\s*$", ln)
        if m:
            if cur_t is not None:
                blocks.append((cur_t, cur_b))
            cur_t, cur_b = m.group(1).strip(), []
        else:
            if cur_t is None:
                # body before any H2 = skip (it's the layer's intro / placeholder)
                continue
            cur_b.append(ln)
    if cur_t is not None:
        blocks.append((cur_t, cur_b))
    return [(t, "\n".join(b).strip()) for t, b in blocks]


def pick_block_layout(body_md: str) -> str:
    """Choose a slide layout based on block content shape."""
    # explicit override
    m = re.search(r"<!--\s*layout:\s*(\w+)\s*-->", body_md)
    if m:
        return m.group(1)
    if "![" in body_md:
        return "image"
    if body_md.count("|") > 10:   # lots of table pipes
        return "table"
    return "text"


# --------------------------------------------------------------------------- #
#  Render slides -> deck HTML
# --------------------------------------------------------------------------- #

DECK_TEMPLATE_EXTERNAL = """<!DOCTYPE html>
<html lang="en" data-theme="{theme}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="assets/fonts.css">
<link rel="stylesheet" href="assets/base.css">
<link rel="stylesheet" id="theme-link" href="assets/themes/{theme}.css">
<link rel="stylesheet" href="assets/animations.css">
{slide_styles}
</head>
<body data-themes="academic-paper,minimal-white,editorial-serif,swiss-grid,corporate-clean">
<div class="deck">
{slides_html}
</div>
<script src="assets/runtime.js"></script>
</body>
</html>
"""

DECK_TEMPLATE_EMBED = """<!DOCTYPE html>
<html lang="en" data-theme="{theme}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
/* ===== fonts.css ===== */
{fonts_css}
/* ===== base.css ===== */
{base_css}
/* ===== theme: {theme} ===== */
{theme_css}
/* ===== animations.css ===== */
{animations_css}
</style>
{slide_styles}
</head>
<body data-themes="academic-paper,minimal-white,editorial-serif,swiss-grid,corporate-clean">
<div class="deck">
{slides_html}
</div>
<script>
{runtime_js}
</script>
</body>
</html>
"""

SLIDE_STYLES = """<style>
  /* tighten dense tables for slide consumption */
  .slide table { font-size: 0.78em; border-collapse: collapse; margin: 0.5em 0; }
  .slide table th, .slide table td { padding: 4px 10px; border-bottom: 1px solid var(--border, #ddd); text-align: left; }
  .slide table thead { border-bottom: 2px solid var(--border, #ccc); }
  .slide pre { font-size: 0.72em; line-height: 1.35; overflow-x: auto; max-height: 60vh; }
  .slide img { max-width: 100%; max-height: 65vh; display: block; margin: 0.5em auto; }
  .slide .kicker { text-transform: uppercase; letter-spacing: 0.12em; font-size: 0.78em; color: var(--dim, #777); }
  .slide h2 { margin: 0.25em 0 0.4em 0; }
  .slide.cover { display: flex; flex-direction: column; justify-content: center; }
  .slide.hero  { display: flex; flex-direction: column; justify-content: center; }
  .slide.divider { display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; }
  .slide.divider h2 { font-size: 3em; }
</style>"""


def render_slide(slide: dict, idx: int, total: int, report_dir: Path,
                 embed: bool) -> str:
    """Wrap one parsed slide as html-ppt <section class="slide">."""
    layout = slide["layout"]
    classes = f"slide {layout}"
    kicker = slide.get("kicker", "")
    heading = slide.get("heading", "")
    body_md = slide.get("body_md", "")

    if embed:
        # base64 each ![](relative-path) directly in the markdown so pandoc
        # passes the data-URI through; image becomes part of the html.
        def embed_img(match: re.Match) -> str:
            prefix, path, suffix = match.group(1), match.group(2), match.group(3)
            # resolve path relative to report.md (the source)
            full = (report_dir / path).resolve()
            if not full.exists():
                return match.group(0)
            mime, _ = mimetypes.guess_type(str(full))
            mime = mime or "application/octet-stream"
            data = base64.b64encode(full.read_bytes()).decode("ascii")
            return f"{prefix}data:{mime};base64,{data}{suffix}"
        body_md = re.sub(
            r'(!\[[^\]]*\]\()(?!https?://|/|data:)([^)]+)(\))',
            embed_img, body_md,
        )
    else:
        # rewrite image paths from report-relative to deck-relative
        # report.md lives at <session_root>/report.md
        # deck lives at  <session_root>/deck/index.html
        # so we need to prepend "../" to relative image paths in <img src="...">
        body_md = re.sub(
            r'(!\[[^\]]*\]\()(?!https?://|/|data:)([^)]+)(\))',
            r'\1../\2\3',
            body_md,
        )

    body_html = md_to_html(body_md) if body_md else ""

    kicker_html = f'<p class="kicker">{kicker}</p>' if kicker else ""
    heading_html = f"<h2>{heading}</h2>" if heading else ""
    footer = (
        f'<div class="deck-footer" style="position:absolute;bottom:1em;right:1.5em;'
        f'font-size:0.7em;color:var(--dim,#888)">{idx} / {total}</div>'
    )

    return (
        f'<section class="{classes}" data-title="{slide["title"]}">'
        f"{kicker_html}{heading_html}{body_html}{footer}"
        f"</section>"
    )


def build_deck(slides: list[dict], report_path: Path, theme: str, title: str,
               embed: bool) -> str:
    parts = [
        render_slide(s, i + 1, len(slides), report_path.parent, embed)
        for i, s in enumerate(slides)
    ]
    if embed:
        # inline all asset files
        def read_asset(rel: str) -> str:
            return (HTML_PPT_SKILL_ROOT / rel).read_text()
        theme_css = (HTML_PPT_SKILL_ROOT / "assets" / "themes"
                     / f"{theme}.css").read_text()
        return DECK_TEMPLATE_EMBED.format(
            theme=theme,
            title=title,
            fonts_css=read_asset("assets/fonts.css"),
            base_css=read_asset("assets/base.css"),
            theme_css=theme_css,
            animations_css=read_asset("assets/animations/animations.css"),
            runtime_js=read_asset("assets/runtime.js"),
            slide_styles=SLIDE_STYLES,
            slides_html="\n\n".join(parts),
        )
    else:
        return DECK_TEMPLATE_EXTERNAL.format(
            theme=theme,
            title=title,
            slide_styles=SLIDE_STYLES,
            slides_html="\n\n".join(parts),
        )


# --------------------------------------------------------------------------- #
#  Asset copying (self-contained deck)
# --------------------------------------------------------------------------- #

def copy_assets(out_dir: Path, theme: str) -> None:
    assets_dst = out_dir / "assets"
    (assets_dst / "themes").mkdir(parents=True, exist_ok=True)
    for rel in ASSETS_TO_COPY:
        src = HTML_PPT_SKILL_ROOT / rel
        # animations.css lives under assets/animations/ on disk; flatten to assets/
        dst = assets_dst / Path(rel).name
        shutil.copy2(src, dst)
    theme_src = HTML_PPT_SKILL_ROOT / "assets" / "themes" / f"{theme}.css"
    if not theme_src.exists():
        sys.exit(f"theme not found: {theme} (looked at {theme_src})")
    shutil.copy2(theme_src, assets_dst / "themes" / f"{theme}.css")


# --------------------------------------------------------------------------- #
#  Main
# --------------------------------------------------------------------------- #

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("report", type=Path)
    ap.add_argument("--theme", default=DEFAULT_THEME)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument(
        "--embed", action="store_true",
        help="Emit a single self-contained .html (inline CSS+JS, base64 image). "
             "Works via file:// in any browser, no server needed.",
    )
    args = ap.parse_args()

    if not args.report.exists():
        sys.exit(f"report not found: {args.report}")

    # in --embed mode: emit a single .html next to report.md
    # otherwise: emit deck/index.html + deck/assets/
    if args.embed:
        out_file = args.out or (args.report.parent / "deck-embed.html")
        out_dir = out_file.parent
    else:
        out_dir = args.out or (args.report.parent / "deck")
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / "index.html"

    md = args.report.read_text()
    # normalize image paths in --embed mode: resolve relative to report.md
    slides = parse_slides(md, args.report)

    # derive deck title from first H1 (after normalization for setext headers)
    md_normed = normalize_headers(md)
    title_match = re.search(r"^# (.+?)\s*$", md_normed, re.MULTILINE)
    title = title_match.group(1) if title_match else "Report deck"

    if not args.embed:
        copy_assets(out_dir, args.theme)
    deck_html = build_deck(slides, args.report, args.theme, title, args.embed)
    out_file.write_text(deck_html)

    size_kb = out_file.stat().st_size / 1024
    print(f"Rendered {len(slides)} slides")
    print(f"Theme:   {args.theme}")
    print(f"Mode:    {'embed (self-contained .html)' if args.embed else 'external assets (deck/ folder)'}")
    print(f"Output:  {out_file}  ({size_kb:.0f} KB)")
    if args.embed:
        print(f"Open:    file://{out_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
