---
status: fixed
created: 2026-06-22
context: bootstrapping Paper-SMSandTiming-IS and Paper-AdaptiveFollowUp-IS lifecycle via haipipe-paper-folder and manual creation. Reference implementation Paper-SuitableMessageForRx-JAMANO.
fixed_in: "paper ref/tex-quality.md + init_paper_layout.py v2.0.0"
---
When bootstrapping lifecycle stages for two new papers (Paper-SMSandTiming-IS and Paper-AdaptiveFollowUp-IS), the generated 0-lifecycle/ tex files were written entirely as %% comment blocks — no \documentclass, no \begin{document}, no rendered prose, no compilable PDF output. This violates three established conventions visible in Paper-SuitableMessageForRx-JAMANO:

1. SELF-CONTAINED COMPILABLE: every lifecycle .tex has \documentclass[11pt]{article}, \usepackage[margin=1in]{geometry}, \usepackage{parskip}, \begin{document}...\end{document} and compiles directly to a same-name .pdf. See existing feedback: 2026-06-22_lifecycle-tex-self-contained-not-fragments.md.

2. REAL PROSE, NOT COMMENTS: content is rendered LaTeX prose, not %% comment blocks. The JAMANO pitch has \section*{Hook}, \section*{Surprise}, \section*{Implication} etc. with actual sentences. The AdaptiveFollowUp pitch has the same content but buried in %% comments that produce a blank PDF.

3. SENTENCE-INDEXED: every sentence carries %% ---- Pn.Sm ---- tags per 3-write-edit/_shared/sentence-format.md. The JAMANO lifecycle files follow this. The new papers' files do not. See existing feedback: 2026-06-22_lifecycle-tex-sentence-format.md.

The JAMANO reference shows the correct pattern per stage:
- 0-seed: \section*{Parent Project}, \section*{Prospectus Question}, \section*{Tentative Claim Shape}, \section*{Current Evidence Status}, \section*{Open Evidence Needs}, \section*{Promotion Gate}, \section*{Kill Criteria} — all rendered prose with Pn.Sm tags.
- 1-pitch: \section*{One-Minute Pitch}, \section*{Hook}, \section*{Surprise}, \section*{Implication}, \section*{Audience and Venue Fit}, \section*{Why Believe}, \section*{Still Fragile}, \section*{Next Evidence Move} — all rendered prose.
- 2-claims: overview table (\begin{tabular}) + per-claim paragraphs with \textbf{CXX} [\supported|\weak|\gap] + evidence + caveat + route.
- 3-narrative: \subsection*{Problem Statement}, \subsection*{Core Claim}, \subsection*{Method}, \subsection*{5-Act Story Arc}, \subsection*{Claim--Evidence Matrix}, \subsection*{Figure Inventory}, \subsection*{Limitations}.

Root cause: haipipe-paper-folder skill's lifecycle generator (and any manual lifecycle creation) does not enforce the JAMANO template. The fix should be in the generator code (scripts/init_paper_layout.py) AND in the stage skills (haipipe-paper-structure-{seed,pitch,claims,narrative}) so they never produce comment-only or fragment tex.

Affected papers: Paper-SMSandTiming-IS (all 6 lifecycle stages), Paper-AdaptiveFollowUp-IS (seed + pitch).

Fix:
