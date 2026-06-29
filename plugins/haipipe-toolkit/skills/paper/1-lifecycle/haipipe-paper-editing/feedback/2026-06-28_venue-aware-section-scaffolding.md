---
status: open
created: 2026-06-28
updated: 2026-06-28
occurrences: 1
context: editing scaffold workflow, §7 discussion for MISQ2026
fixed_in: ""
regressed: ""
---

When creating a section scaffold, the editing skill should read the venue style-profile BEFORE drafting the outline structure. Different sections have venue-specific conventions that affect paragraph ordering, subsection titles, and content organization.

In this session, we created a Discussion scaffold with 6 practical-first topics, then discovered from the MISQ style-profile that the canonical order is "Restate contribution first, then IS theory, then practice, then limitations." We had to reorder after the fact.

Proposed workflow for section scaffolding:

1. Read z-structure.md for the section's planned role and paragraph structure
2. Read the venue style-profile (`_venue/playbook-*/style-profile.md`) for section-specific norms (e.g., Discussion ordering, whether to use subsection titles, contribution enumeration conventions)
3. Optionally dispatch a background subagent to survey 3-4 exemplar papers for that specific section type
4. THEN draft the outline with venue-aware ordering
5. Present for user review

The venue-aware step is especially important for Discussion (ordering), Introduction (arc), and Literature Review (stream structure). Methods/Results may be less venue-sensitive.
