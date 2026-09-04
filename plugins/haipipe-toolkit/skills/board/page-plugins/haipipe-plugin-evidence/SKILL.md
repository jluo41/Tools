---
name: haipipe-plugin-evidence
description: >-
  Compatibility redirect for the retired standalone Evidence plugin. Evidence
  Items, supporting-run lineage, citations, values, displays, and their
  detailed workspace now belong to haipipe-plugin-outline. Trigger: old
  evidence plugin, evidence tab, /haipipe-plugin-evidence.
metadata:
  version: "0.6.1"
  last_updated: "2026-09-04"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-plugin-evidence · compatibility redirect

The standalone Evidence plugin is retired. Do not register an `Evidence` tab,
do not create `<page>/evidence/`, and do not maintain a second evidence
workspace.

Load `haipipe-plugin-outline` instead. It owns:

```text
MAIN PAGE              one compact read-only Outline Table
OUTLINE PLUGIN         detailed Shape + Evidence Workspace + process materials
outline/               plan, requirements, feedback, discussion, item ledger, log
outline/evidence/      citations, displays, supporting-run lineage, materials
```

The old engine route `/_board/evidence` remains an internal compatibility
renderer used by the Outline plugin's Evidence Workspace. Its existence does
not make it a public plugin or a storage authority.

Use these current contracts:

```text
haipipe-plugin-outline/ref/evidence/citations.md
haipipe-plugin-outline/ref/evidence/values.md
haipipe-plugin-outline/ref/evidence/displays.md
haipipe-plugin-outline/ref/evidence/pagex.md   # legacy migration reference only
```

Actual Page-local execution remains outside Outline at `<page>/runs/` and
`<page>/results/`; the nested `outline/evidence/supporting-runs/` lane stores
only generated Evidence Item lineage and pointers.
