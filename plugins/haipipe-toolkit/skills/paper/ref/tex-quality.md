Lifecycle TeX Quality Standard
===============================

Every lifecycle .tex (seed, pitch, claims, narrative, display, minimap) is a
**deliverable**, not a fragment or draft. This document defines the quality bar
that all haipipe-paper stage skills must meet at write time and edit time.


Rules
-----

**SELF-CONTAINED** -- every .tex has its own preamble and compiles directly to
a same-name .pdf. No shell wrappers, no \input-fragment indirection.

Minimal preamble:

    \documentclass[11pt]{article}
    \usepackage[margin=1in]{geometry}
    \usepackage{parskip}
    \usepackage{booktabs}
    \usepackage{hyperref}
    \usepackage{xcolor}
    \newcommand{\needprobe}[1]{\textcolor{red}{\textbf{[NEED PROBE]} #1}}
    \title{N-stage: PaperName (Venue)}
    \date{}
    \begin{document}
    \maketitle
    ...
    \end{document}

The \needprobe{} macro marks claims lacking evidence with a visible red flag
in the compiled PDF (see ref/evidence-routing.md). Remove it when the probe
returns a verdict.

**REAL PROSE** -- content is rendered LaTeX prose with \section* headers, not
%% comment blocks. A .tex that compiles to a blank page is a defect.

**SENTENCE-INDEXED** -- every sentence carries %% ---- Pn.Sm ---- tags per
3-write-edit/_shared/sentence-format.md. Paragraph banners use the 3-line
format:

    % =========
    % Para [file-slug.para-slug] Role -- point
    % =========

Pn restarts per file, Sm restarts per paragraph. Tables (tabularx) get a
banner but no per-sentence tags.


Compile Rule
------------

After writing or editing a lifecycle .tex, compile it:

    pdflatex -interaction=nonstopmode -output-directory <stage-dir> <stage.tex>

Run twice when cross-references or citations are present. Then clean aux:

    rm -f <stage-dir>/*.aux <stage-dir>/*.log <stage-dir>/*.out

A stale PDF (tex newer than pdf) is a defect. The skill -- not the user --
is responsible for compiling after every tex mutation.


.gitignore Note
---------------

Lifecycle PDFs are **tracked deliverables**. 0-lifecycle/**/*.pdf is NOT
gitignored. Committing the refreshed PDF after a tex change is expected.


Reference Implementation
-------------------------

The templates in init_paper_layout.py (seed_tex(), pitch_tex(), etc.) already
follow this standard. The same standard applies to skill runtime output -- when
a skill generates or edits a .tex, the result must meet every rule above.
