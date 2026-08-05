#!/usr/bin/env python3
"""md2tex.py -- one or more stage pages become LaTeX sections, and a paper.

QC5's central open item was "there is no generator, and that is the real
finding": no `.py` or `.sh` in the family turned a page into a section, so
"generated, one way" was a rule an agent was asked to obey rather than a step
something performed. This is that step.

It is the SIBLING of md2docx.py and reads the same `## Content` by the same
rules, which is the point: Word and LaTeX are two projections of one source, so
they must not disagree about what the source says.

    python3 md2tex.py <S-page.md> [...] --paper-root DIR [-o OUTDIR] [--compile]

WHAT IT READS, and what it drops (QC5's read-and-drop table)
    ###   -> \\section / \\subsection, by the depth of its number
    ####  -> a paragraph boundary; the `(job)` line under it is scaffolding
    prose -> one paragraph per #### block, sentences joined
    \\citep{} \\ref{} kept verbatim: they are already LaTeX
    > lanes DROPPED. In Word they become comments; here they have nowhere to go.

REFUSE TO REGRESS, which QC5 demands by name. Sync runs one way, so a page whose
Content lost a citation would silently empty that section's bibliography. Before
writing over an existing section the generator counts citations in both and
REFUSES if the new one has fewer. Measured 2026-07-27: all nine pages carry real
`\\citep{}` in prose (110 total, 0 plain-text author-year), so the check passes
today. It exists for the day one of them does not.

WHERE IT WRITES. `3-dist/tex/` by default, never `sections/`. JL 2026-07-27:
"3-dist is also the build, and sections are as well." Both are projections, but
`sections/` is the one a human has been hand-carrying, so overwriting it is a
separate, deliberate act (`--into-sections`) rather than a side effect.
"""
import argparse
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from importlib import util as _util           # noqa: E402

_spec = _util.spec_from_file_location("md2docx", os.path.join(HERE, "md2docx.py"))
md2docx = _util.module_from_spec(_spec)
_spec.loader.exec_module(md2docx)             # reuse the SAME reader

CITE = re.compile(r"\\cite[tp]?\*?\{([^}]*)\}")
REF = re.compile(r"\\(?:auto|C|c)?ref\{((?:tab|fig):[^}]*)\}")
LEVEL = ("section", "subsection", "subsubsection")


def strip_number(title):
    """`2.1 Physician Prescribing` -> `Physician Prescribing`.

    LaTeX numbers its own sections; carrying the number in the title too gives
    "2.1 2.1 Physician Prescribing" in the compiled PDF.
    """
    return re.sub(r"^\d+(?:\.\d+)*\s+", "", title).strip()


def build_section(page, displays, report):
    blocks, nfenced = md2docx.parse_page(page)
    if nfenced:
        report.append(f"{os.path.basename(page)}: {nfenced} fenced sketch(es) dropped")
    out, buf, seen = [], [], set()

    def flush():
        if buf:
            out.append(" ".join(buf) + "\n")
            buf.clear()

    for b in blocks:
        if b[0] == "skipped-lane":
            continue
        if b[0] == "pbreak":
            flush()
            continue
        if b[0] == "h":
            flush()
            lvl = LEVEL[min(b[1], 3) - 1]
            out.append("\n\\%s{%s}\n" % (lvl, strip_number(b[2])))
            continue
        buf.append(b[1])
        # A Display named in this sentence is \input right after the paragraph
        # that first mentions it, which is MISQ's stated rule: "embedded in the
        # body of the paper, following the first reference".
        for lab in REF.findall(b[1]):
            unit = displays.by_label.get(lab)
            if unit and unit["unit"] not in seen:
                seen.add(unit["unit"])
                flush()
                out.append("\\input{displays/%s/float}\n" % unit["unit"])
            elif not unit:
                report.append("%s: \\ref{%s} matches no display unit"
                              % (os.path.basename(page), lab))
    flush()
    return "".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page", nargs="+")
    ap.add_argument("--paper-root", required=True)
    ap.add_argument("-o", "--outdir")
    ap.add_argument("--compile", action="store_true",
                    help="run xelatex on the generated master and report pages")
    ap.add_argument("--into-sections", action="store_true",
                    help="write over sections/*.tex. Deliberate, not a default: "
                         "that tree has been hand-carried and sync is one-way.")
    a = ap.parse_args()

    root = os.path.abspath(a.paper_root)
    outdir = a.outdir or os.path.join(root, "3-dist", "tex")
    os.makedirs(outdir, exist_ok=True)
    displays = md2docx.Displays(root)
    report, wrote, total_cites = [], [], 0

    for page in a.page:
        page = os.path.abspath(page)
        body = build_section(page, displays, report)
        n = len(CITE.findall(body))
        total_cites += n
        stem = os.path.splitext(os.path.basename(page))[0]
        dest = os.path.join(outdir, stem + ".tex")

        # REFUSE TO REGRESS (QC5). Compare against whatever this would replace.
        prior = dest if os.path.exists(dest) else None
        if prior:
            had = len(CITE.findall(open(prior, encoding="utf-8").read()))
            if n < had:
                report.append("REFUSED %s: %d citations, the file it replaces has "
                              "%d. Sync is one-way; writing would empty the "
                              "bibliography for that section." % (stem, n, had))
                continue
        with open(dest, "w", encoding="utf-8") as f:
            f.write("%% GENERATED from %s by md2tex.py. Do not hand-edit: sync is\n"
                    "%% one-way and the next run overwrites this file.\n%s"
                    % (os.path.relpath(page, root), body))
        wrote.append((stem, n))

    master = os.path.join(outdir, "paper.tex")
    src = os.path.join(root, "Personality-Opioid-MISQ2026.tex")
    if os.path.exists(src):
        head = open(src, encoding="utf-8").read().split("\\begin{document}")[0]
        with open(master, "w", encoding="utf-8") as f:
            f.write(head + "\\begin{document}\n")
            for stem, _ in wrote:
                f.write("\\input{%s}\n" % stem)
            f.write("\\bibliographystyle{misq}\n"
                    "\\bibliography{Personality-Opioid-MISQ2026}\n"
                    "\\end{document}\n")

    print("✅ %s" % outdir)
    for stem, n in wrote:
        print("   %-34s %3d citations" % (stem + ".tex", n))
    print("   %d section(s) · %d citations total" % (len(wrote), total_cites))

    if a.compile and os.path.exists(master):
        env = dict(os.environ, PATH="/Library/TeX/texbin:" + os.environ.get("PATH", ""),
                   TEXINPUTS=".:%s:" % root, BIBINPUTS=".:%s:" % root,
                   BSTINPUTS=".:%s:" % root)
        for cmd in (["xelatex"], ["bibtex"], ["xelatex"], ["xelatex"]):
            subprocess.run(cmd + (["paper"] if cmd[0] == "bibtex"
                                  else ["-interaction=nonstopmode", "paper.tex"]),
                           cwd=outdir, env=env, capture_output=True, text=True)
        pdf = os.path.join(outdir, "paper.pdf")
        if os.path.exists(pdf):
            info = subprocess.run(["pdfinfo", pdf], env=env,
                                  capture_output=True, text=True).stdout
            pages = next((l.split()[-1] for l in info.split("\n")
                          if l.startswith("Pages")), "?")
            print("   📄 paper.pdf · %s pages   (MISQ ceiling 55, all-inclusive)" % pages)
        else:
            print("   ❌ no PDF; see %s/paper.log" % outdir)

    if report:
        print("⚠️  %d note(s):" % len(report))
        for r in dict.fromkeys(report):
            print("    " + r)


if __name__ == "__main__":
    main()
