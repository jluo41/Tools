---
name: haipipe-page-draft-agent
description: "Compatibility identity for historical DRAFT receipts. New Page production dispatches haipipe-page-content-agent and records phase CONTENT, cycle WRITE. Trigger only when auditing or translating an old DRAFT receipt."
tools:
  - Read
  - Skill
model: inherit
metadata:
  version: "0.2.0"
  last_updated: "2026-09-04"
  summary: "Historical DRAFT agent redirect; new work belongs to CONTENT."
  changelog: "./CHANGELOG.md"
---

# DRAFT producer · compatibility only

Do not dispatch this agent for new work. Load
`../haipipe-page-content/SKILL.md` and use `haipipe-page-content-agent`.
Preserve this name only when reading an immutable historical receipt whose
phase is DRAFT.
