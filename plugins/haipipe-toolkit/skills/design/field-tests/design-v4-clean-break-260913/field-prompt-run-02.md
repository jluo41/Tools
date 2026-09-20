LOAD `haipipe:haipipe-design`, `haipipe:haipipe-design-workflow`, and
`haipipe:haipipe-design-unit` from the installed Physician-SPACE skills.

REAL TARGET, BOARD-LEVEL SLICE ONLY (read-only):
`/Users/jluo41/Desktop/DrFirst-SPACE/examples-5-design/Project-Application-SMSDesign/applications/B00_DesignBoard-R2Messages-260821`

1. Stamp START with `date`.
2. Inspect `board.md` plus directory names only far enough to decide whether the
   Board routes into current Design v4. Stop before reading candidate content as
   soon as one decisive unsupported Design marker is found.
3. Report Design and Design-Page frontiers separately.
4. Apply the shipped clean-break vocabulary exactly. Do not call an unsupported
   object history, migration material, a read-only input, or a compatibility
   surface.
5. State the Page and Design Run namespaces a fresh current Folder would use.
6. Keep a numbered FRICTION LOG only for unclear, wrong, contradictory, or
   missing instructions in the loaded skills. Target defects belong in status,
   not in this log. If no skill friction exists, write `None`.
7. Make no writes, migration, external-provider call, or upstream dispatch.
8. Stamp END with `date` and STOP after one bounded next action.
