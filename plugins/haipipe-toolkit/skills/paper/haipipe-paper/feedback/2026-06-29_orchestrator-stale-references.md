---
status: fixed
created: 2026-06-29
updated: 2026-06-29
occurrences: 1
context: skill architecture redesign
fixed_in: "2026-06-29: updated all stale folder/skill/lifecycle references in orchestrator SKILL.md"
regressed: ""
---

The haipipe-paper orchestrator SKILL.md still references old folder names and skill names that were changed in this session:
- 3-write-edit → 2-section-edit
- 4-build-submit → 3-build-submit
- 5-respond → 4-respond
- 6-present → 5-present
- haipipe-paper-editing → haipipe-paper-section-edit (merged)
- haipipe-paper-edit → haipipe-paper-section-edit (merged)
- write-edit → section-edit (in stage strip, STATUS.md)
- seed→pitch→claims → seed→claims→pitch (lifecycle reorder)
- write/ → polish/ (layer worker folder)

The orchestrator SKILL.md, keyword maps, routing logic, and specialist list need a pass to update all stale references to the new names.
