#!/usr/bin/env python3
"""Render a paper's real bibliography, once, into a cache the board can read.

    python3 refs.py <paper-root>

WHY THIS IS A SEPARATE COMMAND AND NOT PART OF THE BUILD.
`QBc5` rules that a dialect module holds grammar and resolution and never
writes. Running BibTeX writes. It also needs a TeX installation, takes seconds,
and would make `build.py` fail on a machine that has no LaTeX. So the split is:
this script WRITES the cache when a human asks, and `dialect_paper.py` only ever
READS it. Delete the cache and the panels fall back to the one-line summary and
the raw bibtex entry, exactly as before.

WHY BIBTEX AND NOT A FORMATTER OF OUR OWN.
The paper declares `\\bibliographystyle{misq}` and ships `misq.bst`. Any
reference we formatted ourselves would be a plausible-looking approximation of
the one the manuscript will actually print, which is the same class of error
this whole apparatus exists to catch. Running the paper's own `.bst` gives the
real string. A synthesized `.aux` citing every key is enough; no full LaTeX
compile happens and nothing in the paper is touched.
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CACHE = ".board-refs.bbl"


def build(root):
    root = Path(root).resolve()
    bibs = sorted(root.glob("*.bib"))
    if not bibs:
        sys.exit(f"no .bib in {root}")
    if not shutil.which("bibtex"):
        sys.exit("bibtex is not installed; panels will keep the raw entry")
    bib = bibs[0]
    keys = re.findall(r"^@\w+\s*\{\s*([^,\s]+)\s*,",
                      bib.read_text(encoding="utf-8", errors="replace"), re.M)
    style = "plainnat"
    for tex in root.glob("*.tex"):
        m = re.search(r"\\bibliographystyle\{([^}]*)\}",
                      tex.read_text(encoding="utf-8", errors="replace"))
        if m:
            style = m.group(1)
            break
    with tempfile.TemporaryDirectory() as tmp:
        aux = Path(tmp) / "refs.aux"
        aux.write_text("".join(f"\\citation{{{k}}}\n" for k in keys)
                       + f"\\bibstyle{{{style}}}\n\\bibdata{{{bib.stem}}}\n",
                       encoding="utf-8")
        env = {"BIBINPUTS": f"{root}:", "BSTINPUTS": f"{root}:", "PATH": "/usr/bin:/bin:/Library/TeX/texbin"}
        r = subprocess.run(["bibtex", "refs"], cwd=tmp, env=env,
                           capture_output=True, text=True)
        out = Path(tmp) / "refs.bbl"
        if not out.is_file():
            sys.exit(f"bibtex produced no .bbl\n{r.stdout[-1500:]}")
        dest = root / CACHE
        dest.write_text(out.read_text(encoding="utf-8", errors="replace"),
                        encoding="utf-8")
        n = out.read_text(encoding="utf-8", errors="replace").count("\\bibitem")
        warn = len(re.findall(r"^Warning--", r.stdout, re.M))
        print(f"✅ {dest}")
        print(f"   {n} references rendered by {style}.bst from {bib.name}"
              f" · {warn} bibtex warning(s)")
        print("   the board reads this on its next build; delete it and panels "
              "fall back to the raw entry")


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else ".")
