---
name: subjective-label-handoff
description: >-
  The Delivery › Handoff view skill of the subjective-label family: it
  freezes a stopped Building lineage into the signed Label Handoff, the only crossing to Scanning. Every Run in this view names this skill, and no other view uses it.
  Use for handoff-freeze, Label Handoff, freeze the guideline, G*, D_cal*, or /subjective-label-handoff.
metadata:
  version: "0.1.0"
  last_updated: "2026-09-29"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /subjective-label-handoff · Delivery Space › Handoff

This skill owns the Runs of the labeling workbench's Delivery › Handoff
view: every Run card there names it, and no other view uses it (JL 260929:
one skill per view). Load `subjective-label` (the family door),
`subjective-label-workflow` (the Run graph) and `label-building` (who decides what) first. Which Run
comes before and after these is in `label-building-workflow`.

## Runs in this view

```text
step  Run Type                     state
13    handoff-freeze       not built (no Label Handoff Keeper)
```

A new Run uses `run-labeling-<operation>-<MMDD>-<target>` on disk and
on the page. Older short-named Tickets remain readable. Its Ticket is
`<Page>/runs/<run>.yaml`
and its Result `<Page>/results/<run>/`, beside `labeling/`.

```text
1 commission the `round-close` Route permits `handoff-freeze`
2 verify     Label Handoff Keeper checks G* and D_cal* are complete
3 custody    Test Custodian confirms protected ids never entered a round
4 sign       the human's signature naming exact versions and lineage
5 write      handoff/label-v1.yaml, once, with its receipt block
6 close      validate the Result envelope and return to the family crossing
```

If step 1 fails, the source Run Routes to `round-prepare` or `HOLD` with the
failing predicate named. If
the Keeper or Custodian is absent, `label-building` §Ends at the handoff rules
`HOLD`; this machine stops at step 2 with the frontier preserved.

## Return

Return the Run address or `none`, the files written, and exactly one next
runnable Run or named human gate.
