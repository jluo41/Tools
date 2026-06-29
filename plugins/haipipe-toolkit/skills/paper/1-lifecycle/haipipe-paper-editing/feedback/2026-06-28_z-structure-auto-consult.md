---
status: open
created: 2026-06-28
updated: 2026-06-28
occurrences: 1
context: editing scaffold workflow, §7 discussion + z-structure sync
fixed_in: ""
regressed: ""
---

When creating a new section scaffold, the editing skill should auto-consult z-structure.md (the paper-level architecture index) for that section's planned role, paragraph count, and cross-section dependencies. When the scaffold is finalized, auto-update z-structure.md to reflect the settled structure.

In this session, we manually checked z-structure.md for §7's plan, then manually updated it after reordering. Both steps should be part of the scaffold creation workflow.

The z-structure auto-sync memory (feedback_z_structure_auto_sync.md) already says "when any section scaffold in 5-editing/ is created or restructured, also update z-structure/z-structure.md." The editing skill should encode this as a workflow step, not rely on the agent remembering a memory.
