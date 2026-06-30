---
status: fixed
created: 2026-06-29
updated: 2026-06-29
occurrences: 1
context: editing scaffold workflow, §3 theory session
fixed_in: "v2.1.0 (DRAFT-GATHER-POLISH-CHECK order; venue norm digestion via lesson subagent)"
regressed: ""
---

Two items from the same conversation:

## 1. Per-section layer order is wrong

Current order (v1.3.0): structure → narrative → content → discovery → task → citation → values → sync
Correct order: structure → narrative → display → values → citation → prose → checklist → sync

Why: you can't write prose until you know what displays are there (write around them), what values you have (cite specific numbers), and what citations back each claim. The current order tries to write content too early and then backfill. The correct order is: plan what to say → gather what you need → then write it.

## 2. Section-type venue norms should flow from editing sessions into the venue pack

When we work on a specific section (e.g., MISQ theory), we learn section-type norms (paragraph density, mechanism-derivation structure, citation density, hypothesis placement). These norms should:
- Be captured in the section's _LOG during editing
- Later be digested into _venue/playbook-<venue>/style-profile.md as permanent section-type guidance
- Be organized by section type: misq-intro, misq-theory, misq-results, misq-discussion, nature-intro, jama-intro, etc.
- The editing skill's `lesson` subagent verb should harvest these into the venue pack, not just into memory files
