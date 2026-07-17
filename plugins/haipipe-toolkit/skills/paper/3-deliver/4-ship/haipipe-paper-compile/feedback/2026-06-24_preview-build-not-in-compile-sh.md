---
status: open
created: 2026-06-24
updated: 2026-06-24
occurrences: 1
context: display stage, ProjB Paper-Personality-Opioid-MedJournal (JAMA); rendering the STROBE preview unit display09-strobe-flow
fixed_in: ""
---
"why this is not in the compile.sh? every time I need to agree on it."

The display-unit preview build (a raw `pdflatex` on
`display09-strobe-flow/preview.tex`, run ad-hoc to crop the STROBE vector) is NOT
wired into `compile.sh`, so it triggers a fresh approval prompt on every single
render. JL wants the preview / asset build folded into the paper's build script so
it runs as one approved step, not a per-call raw `pdflatex`.

How to apply (components/compile + display): add the per-unit preview / asset build
to the paper's `1-compile.sh` (or a dedicated `compile.sh` target) so display-asset
rendering goes through the approved build path. Consistent with
[[feedback_use_compile_sh_not_adhoc_pdflatex]] (never raw per-file pdflatex; each
forces an approval prompt).

Fix:
