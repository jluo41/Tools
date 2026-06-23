---
status: fixed
created: 2026-06-22
context: whole lifecycle flow (every stage skill seed/pitch/claims/narrative/display/minimap); felt on Paper-Personality-Opioid-MedJournal seed re-walk, where the agent rewrote 0-seed.tex but left 0-seed.pdf stale
fixed_in: "paper ref/tex-quality.md + all stage skills v2.0.0"
---
and each lifecycle stage, there is a delievery, everytime, you need to compile the pdf as well. so people can read it.

Distilled ask:
- Every lifecycle stage produces a DELIVERABLE, and that deliverable must be a compiled, readable PDF. After the agent writes/updates a stage .tex, it must compile the stage PDF in the same turn, every time. A .tex the user has to read as source is not a delivery.
- This pairs with [every-stage-must-illuminate-and-elicit-taste]: the readable PDF IS the thing the user reads to internalize the stage. Illuminate = "here is the compiled stage PDF + the taste-bearing choices"; without the fresh PDF there is nothing to read.
- It applies to EVERY stage (seed, pitch, claims, narrative, display, minimap), not just one, and on EVERY edit, not just the first draft. A stale stage PDF (tex newer than pdf) is a defect.

Why this matters:
- The lifecycle .tex files are standalone-compilable for exactly this reason. If the PDF is not refreshed, the user reads stale content or raw LaTeX, defeating internalization.

How (mechanics, already proven on this paper):
- pdflatex is at /Library/TeX/texbin/pdflatex; latexmk also present.
- Per-stage compile: `pdflatex -interaction=nonstopmode -output-directory <stage-dir> <stage.tex>` (twice for hyperref refs), then clean aux (*.aux *.log *.out).
- Full rebuild: `./1-compile.sh` compiles all 0-*.tex + every 0-lifecycle/**.tex + 0-displays/**.tex via a 4-pass pipeline, then cleans aux unless --keep.
- .gitignore is already set to PRESERVE lifecycle/display PDFs (they are tracked deliverables), so committing the refreshed PDF is expected.

Where it touches:
- each stage skill (seed/pitch/claims/narrative/display/minimap): add a final "Compile deliverable" step -> recompile the stage PDF and report its path + size; treat a stale PDF as not-done.
- shared ref (e.g. the ref/stage-illuminate.md proposed in the sibling item): the illuminate step must hand the user a FRESH stage PDF to read.
- haipipe-paper-enter console: could flag any stage whose .tex is newer than its .pdf as "stale deliverable".

Fix:
