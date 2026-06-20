# 0-sections/ : section files for {{PAPER_SLUG}}

Modular body of the manuscript. Naming grammar and file roles: `Tools/plugins/haipipe-toolkit/skills/paper/2-build/_shared/paper-folder-anatomy.md` and `3-edit/_shared/tex-file-anatomy.md`.

## Main sections

{{MAIN_SECTION_LIST}}

## Supplementary blocks (SI, separate document)

{{SI_SECTION_LIST}}

## Rules

- Driver (`../0-{{PAPER_SLUG}}.tex`) owns every `\section{}`; wrappers hold only `\input` lines; leaves hold the prose.
- Filenames are structural addresses: `NN[-MM]_<slug>.tex`, contiguous, no gaps. Close gaps in the same pass as any delete/merge.
- Every paragraph carries a stable-id banner (`% Para [<slug>.<point>] ...`); never renumber ids.
