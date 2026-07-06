---
status: open
created: 2026-06-23
context: 2-claims.tex rewrite during JAMANO claims restructuring session
fixed_in: ""
---

When updating any lifecycle stage .tex file (0-lifecycle/0-seed/0-seed.tex, 1-pitch/1-pitch.tex, 2-claims/2-claims.tex, etc.), the agent must compile it to PDF immediately after writing. Lifecycle .tex files are standalone-compilable by design — each has its own \documentclass/\begin{document}/\end{document}. The PDF is the human-readable deliverable; the .tex alone is not "done."

This session: 2-claims.tex was rewritten from 6-claim JAMA NO to 4-claim JAMA flagship structure, but no compile was run. The .tex was left without a corresponding .pdf.

Fix: add a mandatory post-write step to every lifecycle stage skill (haipipe-paper-claims, haipipe-paper-pitch, haipipe-paper-narrative, etc.) and to the paper orchestrator's dispatch logic: after writing or updating any file under 0-lifecycle/, run pdflatex on it and verify the PDF renders. Flag compile errors before reporting success.
