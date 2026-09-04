---
name: haipipe-page-draft
description: >-
  Compatibility redirect for the retired DRAFT Page phase. New Page work uses
  haipipe-page-content, whose CONTENT/WRITE cycle includes Draft, Revise,
  Build, and Pre-check. Use only when translating historical instructions or
  receipts that explicitly name DRAFT. Trigger: legacy page draft, old DRAFT
  phase, /haipipe-page-draft.
metadata:
  version: "0.11.0"
  last_updated: "2026-09-04"
---

# /haipipe-page-draft · compatibility redirect

Load and follow `../haipipe-page-content/SKILL.md`.

```text
historical DRAFT phase   → current CONTENT phase
historical draft pass    → current CONTENT / WRITE / Draft movement
new workflow receipt     → phase: CONTENT · cycle: WRITE
```

Do not dispatch a new DRAFT phase or create a DRAFT-specific Run. Preserve old
receipt tokens unchanged for audit; the Page lifecycle auditor owns their
compatibility grammar.
