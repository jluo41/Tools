---
name: subjective-label-guideline
description: >-
  The Labeling › Guideline view skill of the subjective-label family: it
  writes the guideline versions: a first guideline candidate and, after each round, the next guideline drafted from the human's accepted judgments. Every Run in this view names this skill, and no other view uses it.
  Use for guideline, guideline-seed, guideline-learn, policy_draft, a guideline patch, backward impact, or /subjective-label-guideline.
metadata:
  version: "0.1.0"
  last_updated: "2026-09-29"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /subjective-label-guideline · Labeling Space › Guideline

This skill owns the Runs of the labeling workbench's Labeling › Guideline
view: every Run card there names it, and no other view uses it (JL 260929:
one skill per view). Load `subjective-label` (the family door),
`subjective-label-workflow` (the Run graph) and `label-building` (who decides what) first. Which Run
comes before and after these is in `label-building-workflow`.

## Runs in this view

```text
step  Run Type                     state
 6    guideline-seed       not built · G_00 itself comes from corpus-contract
10    guideline-learn      not built
```

A new Run uses `run-labeling-<operation>-<MMDD>-<target>` on disk and
on the page. Older short-named Tickets remain readable. Its Ticket is
`<Page>/runs/<run>.yaml`
and its Result `<Page>/results/<run>/`, beside `labeling/`.

`guideline-seed` (not built yet) revises the inspectable policy, only when
separately commissioned; the first guideline `G_00` is written by
`corpus-contract`, so this Run is never a prerequisite.

After any item is judged, a change to a label's meaning is no longer a
`definition-discussion`: it is a guideline patch here.

### LEARN

1. From accepted human evidence, draft the smallest general patch into
   `policy_draft/`, typed semantic / procedural / casebook / wrapper / editorial.
2. Compute backward impact: every prior gold row the patch would flip, into
   `policy_draft/regression.jsonl`.
3. Present each substantive patch with its impact for the human's ruling.
4. Close `guideline-learn` after every substantive patch has a human ruling.

## Return

Return the Run address or `none`, the files written, and exactly one next
runnable Run or named human gate.
