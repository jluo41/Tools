---
status: open
created: 2026-07-01
updated: 2026-07-01
occurrences: 1
context: §1 introduction status strip
fixed_in: ""
regressed: ""
---

The section-level status strip must use the actual layer NAMES, not just index numbers (L1, L2, etc.). The user cannot tell what L1-L8 mean without memorizing the mapping. Use the real names from the layer table.

Before (bad):
```
§1:     L1 ✅  L2 ✅  L3 ✅  │  L4 --  L5 --  L6 ✅  │  L7 🚀  │  L8 ⬜
        ───DRAFT──────────  ───GATHER──────────────  ──POLISH─  ──CHECK──
```

After (good):
```
§1:     paper-structure ✅  section-structure ✅  narrative ✅  │  display --  values --  citation ✅  │  prose 🚀  │  checklist ⬜
        ──────────DRAFT──────────────────────────  ──────────GATHER──────────────────────  ──POLISH──  ───CHECK───
```
