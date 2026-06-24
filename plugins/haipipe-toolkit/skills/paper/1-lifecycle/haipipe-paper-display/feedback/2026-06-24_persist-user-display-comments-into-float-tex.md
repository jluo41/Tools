---
status: open
created: 2026-06-24
context: display stage, ProjB Paper-Personality2Opioid-MISQ2026
updated: 2026-06-24
occurrences: 2
fixed_in: ""
---
"everytime I add my comments to certain displays, please also add my comments in
the comment format as %{XX}: xxx to the tex and keep them for every[figure], this
will be used as my preference for each figure."

Standing preference: whenever the user comments on a display (figure/table),
PERSIST that comment verbatim as a LaTeX comment `%% {JL}: <comment>`, and KEEP it
across iterations as a per-figure preference / decision log.

CORRECTION (JL, 2026-06-24): the comments go into the lifecycle gallery file
`0-lifecycle/4-display/4-display.tex` (next to that display's `\input`), NOT into
the per-unit `float.tex`. The unit float.tex stays clean (figure + its own header
+ engineering TODOs); 4-display.tex is the single control surface that carries the
human commentary / preference log for the whole display set.

Format: `%% {JL}: <comment>` (aligning the user's stated `%{XX}: xxx` with the repo
convention from feedback_jl_marker_for_audit_notes). One line per comment; never
compress, translate, or drop them.

FIX (proposed): haipipe-paper-display must, after any user comment on a display,
append it as `%% {JL}: ...` near that display's entry in
`0-lifecycle/4-display/4-display.tex` and preserve all prior such lines. ALSO
enforce the gallery requirements JL stated: order to the NARRATIVE flow, meet the
venue display set, and end with a PARKING section for superseded/alternative
displays.

Fix:

## Recurrences
- 2026-06-24 (digest, Display-for-Opioid-JAMA): "no, you should only add the comments to examples/ProjB-PhyTrait-OpioidRx/paper/Paper-Personality-Opioid-MedJournal/0-lifecycle/4-display/4-display.tex in the lifecycle, please mark this down in the skills."
