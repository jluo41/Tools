---
status: fixed
created: 2026-06-29
updated: 2026-06-29
occurrences: 1
context: skill architecture redesign
fixed_in: "v2.0.0 of seed/pitch/claims/narrative skills"
regressed: ""
---

Paper-level argument documents (seed, pitch, claims, narrative) should be markdown + _LOG only, no .tex compilation. Only the display stage compiles to .tex + PDF.

Rule: if you need to SEE it rendered, .tex. If you need to READ it, .md.

Fix: applied to haipipe-paper-seed, -pitch, -claims, -narrative SKILL.md descriptions (all bumped to v2.0.0). Display unchanged (keeps .tex + PDF).
