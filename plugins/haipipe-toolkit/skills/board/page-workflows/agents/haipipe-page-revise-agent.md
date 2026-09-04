---
name: haipipe-page-revise-agent
description: "Compatibility identity for historical REVISE or COMPILE receipts. New Page production dispatches haipipe-page-content-agent and records phase CONTENT, cycle WRITE. Trigger only when auditing or translating an old REVISE/COMPILE receipt."
tools:
  - Read
  - Skill
model: inherit
metadata:
  version: "0.2.0"
  last_updated: "2026-09-04"
  summary: "Historical REVISE/COMPILE agent redirect; new work belongs to CONTENT."
  changelog: "./CHANGELOG.md"
---

# REVISE producer · compatibility only

Do not dispatch this agent for new work. Load
`../haipipe-page-content/SKILL.md` and use `haipipe-page-content-agent`.
Preserve this name only when reading an immutable historical receipt whose
phase is REVISE or COMPILE.
