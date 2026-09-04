---
name: haipipe-page-revise
description: >-
  Compatibility redirect for the retired REVISE and COMPILE Page phases. New
  Page work uses haipipe-page-content, whose CONTENT/WRITE cycle includes
  Draft, Revise, Build, and Pre-check. Use only when translating historical
  instructions or receipts that explicitly name REVISE or COMPILE. Trigger:
  legacy page revise, old REVISE phase, old COMPILE phase,
  /haipipe-page-revise.
metadata:
  version: "0.6.0"
  last_updated: "2026-09-04"
---

# /haipipe-page-revise · compatibility redirect

Load and follow `../haipipe-page-content/SKILL.md`.

```text
historical REVISE phase    → current CONTENT phase
historical COMPILE phase   → current CONTENT / WRITE / Build movement
historical revise pass     → current CONTENT / WRITE / Revise movement
new workflow receipt       → phase: CONTENT · cycle: WRITE
```

Do not dispatch new REVISE or COMPILE phases. Preserve old receipt tokens
unchanged for audit; the Page lifecycle auditor owns their compatibility
grammar.
