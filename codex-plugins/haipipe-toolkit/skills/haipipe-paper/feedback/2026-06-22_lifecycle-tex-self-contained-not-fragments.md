---
status: fixed
created: 2026-06-22
context: bootstrapping 0-lifecycle/ for Paper-MegastudyNudgingPreference-IS
fixed_in: "paper ref/tex-quality.md + init_paper_layout.py v2.0.0"
---
When bootstrapping lifecycle layers, the skill wrote the .tex files as fragments (no \documentclass, no \begin{document}) and then created separate *-shell.tex wrappers to compile them. This is wrong. The convention (visible in PhyTraitNudging-IS and SuitableMessageForRx-JAMANO) is that each layer .tex is self-contained: it has its own \documentclass{article}, \begin{document}, \end{document}, and compiles directly to {N}-{name}.pdf. No shell files, no wrapper indirection. The resulting file tree per layer is exactly {N}-{name}.tex + {N}-{name}.pdf.

The lifecycle bootstrap code (or any skill that creates/edits lifecycle layers) must produce self-contained compilable documents, not input-fragments. Compile each layer after writing it.

Fix:
