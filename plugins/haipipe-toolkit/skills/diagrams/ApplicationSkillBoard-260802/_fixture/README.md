# Validation fixture: one Application, two boards

Synthetic. Every number below is invented for structure testing and describes no real cohort, patient, or campaign. Do not cite a value from this tree.

It exercises the full route once, end to end:

```text
🔎 SmsClickR4-InsightBoard          🎨 YoungMaleRefill-DesignBoard
   M00-meta      page-type: meta       A00-brief    page-type: brief
   I01-who-clicks  scope: application  D01-young-male-refill  page-type: design
        │                                     │
        └──────── PageX ─────────────────────▶  R1 accepted · R2 accepted
                                                R3 unaccepted, on purpose
```

What it proves: both head pages resolve, an Insight Page reaches a Design Handoff, a Design Page borrows that handoff across boards by relative path, acceptance sits on divisions rather than the page, and an unaccepted division beside accepted ones is a legal state.

Replaced the retired `0-lifecycle/1a-descriptions/…` ladder fixture on 260820.
