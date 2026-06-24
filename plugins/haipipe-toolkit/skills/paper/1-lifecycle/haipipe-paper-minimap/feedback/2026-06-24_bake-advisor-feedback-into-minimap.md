---
status: open
created: 2026-06-24
updated: 2026-06-24
occurrences: 1
context: minimap stage, ProjB Paper-Personality2Opioid-MISQ2026
fixed_in: ""
regressed: ""
---
"you should also bake professor's feedback below the narrative thread as well, trying to solve their comments."

The minimap should THREAD advisor/reviewer feedback (e.g. Prof. Agarwal's comments, carried as `\fb{}` lines in `3-narrative.tex`) below the relevant per-paragraph narrative note (`\nnote`), each rendered with a status [resolved / addressing / open] and a one-line "how we resolve it." This makes the minimap show not just the spine but how it ANSWERS known reviewer comments, beat by beat.

How to apply: add a `\pfb{status}{comment}{resolution}` convention (maroon, placed directly below the `\nnote` it concerns), map each advisor comment from `3-narrative.tex`'s `\fb` lines to the beat it concerns, and roll up any still-open ones into the Write-Time Reconciliations.

Fix:
