---
status: open
created: 2026-06-22
context: bootstrapping Paper-PhyTraitNudging-IS lifecycle, pitch generated without title
fixed_in: ""
---
The pitch skill template (haipipe-paper-structure-pitch) does not include a Title section in its canonical backbone. The template jumps straight from \begin{document} to "One-Minute Pitch". The paper title should be the first thing in the pitch -- it is the most basic identifier. When the pitch was generated following the template exactly, the title was omitted and had to be added manually after user flagged it.

Fix: add a \section*{Title} block as the first section in the pitch template, before One-Minute Pitch.
