---
name: haipipe-plugin-probe
description: >-
  Compatibility redirect for the retired Page-local Probe plugin and probe/
  lane. New Page evidence is a typed Evidence Item managed by Outline through
  SHAPE, SURVEY, LAND, and EMBED. Trigger: old probe plugin, probe card,
  evidence probe, /haipipe-plugin-probe.
metadata:
  version: "1.0.0"
  last_updated: "2026-09-03"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-plugin-probe · compatibility redirect

The Page-local Probe plugin and `probe/` storage lane are retired. Do not
register a Probe tab, create `<page>/probe/`, or create
`<page>/outline/evidence/probe/`.

For current work, load:

```text
haipipe-page-outline    SHAPE the typed Evidence Item; SURVEY its Run graph
haipipe-page-evidence   LAND one accepted local Result; EMBED its Page meaning
haipipe-plugin-outline  present Shape, evidence, paths, and feedback together
```

Use `VALUE`, `CITE`, or `DISPLAY` Evidence Items. Their zero-to-many supporting
Execution/Discovery Runs are pointers under
`outline/evidence/supporting-runs/`; actual local Runs and Results remain in
sibling `runs/` and `results/` folders.

Legacy Probe artifacts may be read as migration input, but they are never a
current authority and must not be copied into a new Probe folder.
