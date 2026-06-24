---
status: open
created: 2026-06-24
updated: 2026-06-24
occurrences: 1
context: minimap stage, ProjB Paper-Personality2Opioid-MISQ2026
fixed_in: ""
regressed: ""
---
"the supplement is too limited. we should have more, please check what we have in 0-sections." + "try to sync with supplement."

The minimap's Supplement section must SYNC with the paper's actual supplementary
material, not be a thin generic list. Read the existing `0-sections` appendices
(here A-F: LLM prompts/rubric, LLM validation, variable construction, IV details,
robustness tables, extended lit + Big Five) and any `0-Supplementary-*.tex` master,
and enumerate the real eAppendix items, each mapped to the main beat it supports.
Keep the minimap eAppendix and the real supplement IN SYNC (re-read when either
changes), so the minimap is an honest map of what the SI will contain.

How to apply: at minimap build, glob `0-sections/{A..Z}*.tex` and any
`0-Supplementary-*.tex`, derive the eAppendix list from what exists, and flag a
`\wt` when a planned SI item has no draft yet (or a draft has no minimap slot).

Fix:
