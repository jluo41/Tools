# Compile Pipelines

`make-diff.sh` calls `${COMPILER_HINT:-pdflatex}` four times (1 + bibtex +
2 more passes) to settle cross-references. The compiler is auto-detected
from preamble cues in `detect-paper-class.sh`:

| Trigger in master.tex                          | Compiler  |
|------------------------------------------------|-----------|
| `\usepackage{fontspec}` / `unicode-math`       | `xelatex` |
| `\usepackage{luacode}` / `\directlua`          | `lualatex`|
| neither                                        | `pdflatex`|

Override per diff via `1-diff/<sub>/config.sh`:
```
COMPILER_HINT="lualatex"
```

## When the auto-pick is wrong

- **fontspec for unicode but no xelatex/lualatex flag**: most modern ACM
  acmart papers use fontspec but compile with pdflatex via the `nonacm`
  fallback. Force `COMPILER_HINT=pdflatex` if needed.
- **biblatex/biber instead of bibtex**: detect via `\usepackage{biblatex}`.
  Currently `make-diff.sh` always runs `bibtex` — if your paper uses
  biber, change the script's bibtex line or run biber manually after the
  first pdflatex pass and skip the script's bibtex step.
- **latexmk wrappers**: `make-diff.sh` doesn't use latexmk because it
  conflicts with `clean_aux_files()` patterns from sibling skills (e.g.,
  `paper-compile`). If you prefer latexmk, run it manually inside
  `1-diff/<sub>/` after the script writes `<main>-DIFF.tex`.

## Bibliography styles

The script copies `*.bib` and `*.bst` from `new/` to the diff subdir before
compiling. If the paper uses a custom .bst that's outside the new/ tree
(e.g., system-installed), bibtex will still find it via TeX's path
resolution.

## Multi-master papers

If your paper has multiple master tex files (e.g., `0-MainPaper.tex` +
`0-MainPaper-EC.tex` for an electronic companion), `make-diff.sh` only
diffs ONE master. To diff both:

```bash
make-diff.sh <baseline> <tag> 0-MainPaper.tex
make-diff.sh <baseline> <tag>-ec 0-MainPaper-EC.tex
```

Each call writes to a distinct `vs-<tag>-<sha>/` subdir.
