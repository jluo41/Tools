#!/usr/bin/env python3
"""md2docx.py -- one accepted Board Page's ## Content becomes a .docx whose apparatus
rides in anchored Word comments.

QC6's ruling, executed. The carrier is a native Word comment with
`w:author="haipipe"`, which is what keeps machine provenance separable from a
coauthor's own markup and is what makes the backport ruling mechanical.

Standard library only, on purpose: pandoc cannot WRITE Word comments at all,
so the obvious tool cannot carry this exporter's central feature.

Nothing here formats a citation or recomputes a number. Every resolved thing
is read from a file the family already generates:
    .board-refs.bbl                 the in-text label AND the reference list,
                                    produced by the paper's own .bst
    displays/<unit>/float.tex       the \\label and the unit's kind
    displays/<unit>/assets/         table-body.tex or figure.png

Usage:  md2docx.py <page.md> [-o out.docx] [--paper-root DIR]
"""
import argparse, os, re, struct, sys, zipfile
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

# The parts sit beside this file, and it may be loaded by path, so its folder goes on the import path first.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import md2docx_docx  # noqa: E402

# The parts of this module live in their own files; every name still answers here.
from md2docx_layout import (  # noqa: F401
    ABSTRACT_DIVISIONS, ABSTRACT_LABELS, BODY_IN, BODY_TW, DISCUSSION_LANES, DRW, EMU_IN, EVIDENCE_LANES, LANES,
    NUMTOK, OFF, PKG, SECTION_KIND, SKIP_DIVISIONS, UNNUMBERED_OK, W, WORKING_LANES, _TW, abstract_label,
    col_widths, is_abstract_page, is_manuscript_heading, text_tw,
)
from md2docx_inputs import (  # noqa: F401
    Bbl, DIFF, DPI, Displays, KEYEQ, SUPER, _braced, compact_lane, detex, rasterize,
)
from md2docx_page import (  # noqa: F401
    _KEEP, _TEX_SYMBOLS, _tex_math, _unwrap, content_format, latex_content_to_markdown, parse_page, tex_inline_md,
)
from md2docx_inline import (  # noqa: F401
    Inline, Numbering,
)
from md2docx_tables import (  # noqa: F401
    _alignment_columns, _braced_arg, _command_args, _environment_body, _split_table_rows, parse_table_body,
    split_cells,
)
from md2docx_docx import (  # noqa: F401
    AUTHOR, Docx, STYLES, _initials, png_size,
)


# --------------------------------------------------------------- driver

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page", nargs="+",
                    help="one accepted Board Page, or several in reader order "
                         "for a composed document. Several is not a convenience: float "
                         "numbering, the reference list and heading numbers are "
                         "DOCUMENT-level facts, so only one walk over all pages "
                         "in order can get them right (QC6's section-only rows).")
    ap.add_argument("-o", "--out")
    ap.add_argument("--paper-root")
    ap.add_argument("--document-title",
                    help="optional full-document title emitted before Content; "
                         "Board passes the page's canonical H1")
    ap.add_argument("--author", default=AUTHOR,
                    help='comment author. Default "haipipe" keeps QC6\'s '
                         'partition in the author field; pass a person\'s name '
                         'when the markup should read as theirs. ASK first.')
    ap.add_argument("--join-paragraphs", action="store_true",
                    help="join the sentences of each #### block into ONE Word "
                         "paragraph. The .md is one sentence per line, which is "
                         "right for review and wrong for a manuscript: unjoined, "
                         "a 6-sentence paragraph becomes 6 double-spaced Word "
                         "paragraphs, reads as a list, and inflates the page "
                         "count. Use it for the COMBINED document; leave it off "
                         "for per-section review files, where a sentence per "
                         "paragraph is the point.")
    ap.add_argument("--keep-fences", action="store_true",
                    help="render ``` blocks as monospaced Word blocks instead "
                         "of dropping them; the Board exporter uses this for "
                         "prompt/specification Pages")
    ap.add_argument("--no-displays", action="store_true",
                    help="skip embedding tables and figures")
    ap.add_argument("--display-root",
                    help="an EXTRA folder of display units (each subfolder a "
                         "unit with float.tex), scanned beside the paper's "
                         "displays/: a board page's <page>/display/ workbench")
    ap.add_argument("--lanes", default="Citation",
                    help="which EVIDENCE lanes become comments, comma-separated: "
                         "Citation, Value, Display. Default Citation only. All "
                         "three are evidence and all three are true, but five "
                         "comments landed on one sentence of §1 and three of them "
                         "were Display audits several hundred characters long "
                         "(JL 2026-07-28): a display's state is a BOARD concern, "
                         "and the coauthor reading the .docx is checking the "
                         "sentence. Pass Citation,Value,Display to get them back.")
    a = ap.parse_args()
    lanes = tuple(x.strip() for x in a.lanes.split(",") if x.strip())
    bad = [x for x in lanes if x not in EVIDENCE_LANES]
    if bad:
        raise SystemExit("--lanes: %s is not an evidence lane; pick from %s"
                         % (", ".join(bad), ", ".join(EVIDENCE_LANES)))
    globals()['AUTHOR'] = a.author
    md2docx_docx.AUTHOR = a.author          # Docx reads the comment author from its own module

    pages = [os.path.abspath(x) for x in a.page]
    root = os.path.abspath(a.paper_root) if a.paper_root else \
        os.path.dirname(pages[0])
    stem = (os.path.splitext(os.path.basename(pages[0]))[0] if len(pages) == 1
            else "combined")
    out = a.out or os.path.join(root, "word", stem + ".docx")
    os.makedirs(os.path.dirname(out), exist_ok=True)

    report, num = [], Numbering()
    # STALENESS IS COMPUTED, NEVER DECLARED (QC3's law, applied here).
    # Compared MTIMES first and that was wrong: an editor save with no content
    # change makes the .bib newer than the cache, so the warning fired forever
    # (measured 2026-07-27, .bib touched 7s after a fresh regeneration). What
    # actually matters is whether the cache RENDERS every key the .bib DECLARES,
    # which is exact, cheap, and immune to a touch. It also names the keys.
    bbl_path = os.path.join(root, ".board-refs.bbl")
    bib = next((os.path.join(root, f) for f in sorted(os.listdir(root))
                if f.endswith(".bib")), None)
    if bib and os.path.exists(bbl_path):
        declared = set(re.findall(r"^@\w+\s*\{\s*([^,\s]+)\s*,",
                                 open(bib, encoding="utf-8", errors="replace").read(), re.M))
        rendered = set(re.findall(r"\\bibitem\[[^\]]*\]\{([^}]+)\}",
                                 open(bbl_path, encoding="utf-8", errors="replace").read()))
        gap = sorted(declared - rendered)
        if gap:
            report.append((
                "stale-bibliography",
                f".board-refs.bbl renders {len(rendered)} of the .bib's "
                f"{len(declared)} keys. {len(gap)} declared key(s) are absent, so "
                f"citing any of them prints a bare key: "
                f"{', '.join(gap[:6])}{' …' if len(gap) > 6 else ''}. "
                f"Regenerate: python3 <haipipe-draft>/cli/refs.py <paper-root>"))
    bbl = Bbl(bbl_path)
    disp = Displays(root, extra_root=a.display_root)
    inline = Inline(bbl, disp, num, report)
    d = Docx()
    if a.document_title:
        d.title(a.document_title)

    placed, npara, skipped, held = set(), 0, {}, {}
    parsed = [(page, parse_page(page, keep_fences=a.keep_fences)) for page in pages]
    # A display's number is the order of its first citation in a SENTENCE, across all
    # pages, the order LaTeX prints the floats in. Read ahead, so a caption or note that
    # names a later table already gives it the number the body will (S-MISQ-Main-5-
    # Results 260928: a caption's \ref numbered and placed the pooled table early).
    prose_cited = set()
    for _page, (blocks, _nfenced) in parsed:
        for b in blocks:
            if b[0] == "p":
                for m in Inline.REF.finditer(b[1]):
                    rec = disp.by_label.get(m.group(1))
                    if rec:
                        num.assign(rec)
                        prose_cited.add(rec["unit"])
    for page, (blocks, nfenced) in parsed:
        if nfenced and not a.keep_fences:
            report.append(("fenced-sketch-skipped",
                           f"{os.path.basename(page)}: {nfenced} ``` block(s) in "
                           f"## Content are ASCII sketches, not prose, and were "
                           f"NOT exported. Each is usually a display unit that "
                           f"has not been built."))
        buf = []          # [(rendered_sentence, lanes)] awaiting a paragraph flush

        def flush():
            """Emit the buffered sentences as ONE Word paragraph.

            Each lane keeps the WINDOW of its own sentence inside the joined
            text, so a comment still anchors on the number in the sentence that
            owed it rather than on the first match in the paragraph."""
            if not buf:
                return
            parts, lanes, pos = [], [], 0
            for sent, sl in buf:
                lo = pos
                parts.append(sent)
                pos += len(sent) + 1                      # +1 for the joining space
                hi = pos
                lanes += [(k, v, lo, hi) for k, v in sl]
            d.para_with_comments(" ".join(parts), lanes)
            buf.clear()

        def place_due(final=False):
            """The displays this paragraph cited, after the whole paragraph, in citation
            order: a float never splits a paragraph (S-MISQ-Main-5-Results, 260928; the
            LaTeX export follows the same rule)."""
            flush()
            due = [u for u in inline.prose_refs if u not in placed]
            if final:                                  # cited only in a caption or note
                due += [u for u in num.given if u not in placed and u not in prose_cited and u not in due]
            for unit in due:
                n = num.given[unit]
                rec = disp.by_unit[unit]
                if rec["kind"] == "table":
                    parsed = parse_table_body(rec["body"])
                    if parsed:
                        rows, align = parsed
                        d.table(rows, align=align,
                                caption="Table %d. %s" % (
                                    n, inline.caption(rec["caption"]) or unit))
                        if rec.get("note"):
                            d.para(inline.caption(rec["note"]), style="TableNote")
                    else:
                        report.append(("no-table-body", f"{unit} has no parsable table-body.tex"))
                    placed.add(unit)
                else:
                    img = rec["image"] or (
                        # Cache beside the derived Word projection. A temp build
                        # never writes into a Paper runtime.
                        rasterize(rec["pdf"],
                                  os.path.join(os.path.dirname(out), ".media"),
                                  report) if rec.get("pdf") else None)
                    if img:
                        d.image(img, caption="Figure %d. %s" % (
                            n, inline.caption(rec["caption"]) or unit))
                    else:
                        report.append(("no-image",
                                       f"{unit} has neither figure.png nor a "
                                       f"rasterizable figure.pdf"))
                    placed.add(unit)

        label = None      # a structured abstract's label, owed to the next paragraph
        for b in blocks:
            if b[0] == "skipped-lane":
                skipped[b[1]] = skipped.get(b[1], 0) + 1
                continue
            if b[0] == "label":
                label = b[1]
                continue
            if b[0] == "pbreak":
                if not a.no_displays:
                    place_due()
                flush()
                continue
            if b[0] == "fence":
                if not a.no_displays:
                    place_due()
                flush()
                d.code("\n".join(b[1]))
                continue
            if b[0] == "table":
                flush()
                d.table([[(re.sub(r"[`*]", "", c), i == 0, 1) for c in row]   # header row bold
                         for i, row in enumerate(b[1])])
                continue
            if b[0] == "h":
                if not a.no_displays:
                    place_due()
                flush()
                d.heading(b[1], b[2])
                label = None
                continue
            npara += 1
            rendered, auto = inline.render(b[1])
            if label:
                rendered, label = "**%s** %s" % (label, rendered), None
            sl = auto + [(k, v) for k, v in b[3]]
            for k, _v in sl:
                if k not in lanes:
                    held[k] = held.get(k, 0) + 1
            sl = [(k, v) for k, v in sl if k in lanes]
            if a.join_paragraphs:
                buf.append((rendered, sl))
            else:
                d.para_with_comments(rendered, sl)
            # its displays wait for the paragraph's end (a blank line, a heading, a fence)
        if not a.no_displays:
            place_due(final=True)
        flush()

    if inline.cited:
        d.heading(1, "References")
        # one list for the WHOLE document, alphabetical, in MISQ's Reference
        # style: single-spaced with a left hanging indent.
        for k in sorted(inline.cited, key=lambda k: bbl.intext.get(k, k).lower()):
            d.para(bbl.body.get(k, f"[{k}: not in .board-refs.bbl]"),
                   style="Reference")

    d.save(out)

    print(f"✅ {out}")
    print(f"   {len(pages)} page(s) · {npara} paragraphs · "
          f"{d.cid} anchored comments · {len(num.given)} displays placed · "
          f"{len(inline.cited)} references")
    print("   comment lanes: " + ", ".join(lanes)
          + (" · held back by --lanes: "
             + " · ".join(f"{k} {v}" for k, v in sorted(held.items())) if held else ""))
    if skipped:
        print("   working lanes NOT exported (they stay on the board): "
              + " · ".join(f"{k} {v}" for k, v in sorted(skipped.items())))
    if report:
        print(f"⚠️  {len(report)} thing(s) the export could not resolve:")
        seen = set()
        for kind, msg in report:
            if (kind, msg) in seen:
                continue
            seen.add((kind, msg))
            print(f"    {kind:18s} {msg}")


if __name__ == "__main__":
    main()
