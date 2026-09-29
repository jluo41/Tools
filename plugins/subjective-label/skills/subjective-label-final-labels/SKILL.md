---
name: subjective-label-final-labels
description: >-
  The Delivery › Final labels view skill of the subjective-label family: it
  publishes the audited final label set D* with its provenance shares, after the audit passes or its limit is accepted. Every Run in this view names this skill, and no other view uses it.
  Use for final labels, D*, dstar-materialize, publishing the labeled corpus, or /subjective-label-final-labels.
metadata:
  version: "0.1.0"
  last_updated: "2026-09-29"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /subjective-label-final-labels · Delivery Space › Final labels

This skill owns the Runs of the labeling workbench's Delivery › Final labels
view: every Run card there names it, and no other view uses it (JL 260929:
one skill per view). Load `subjective-label` (the family door),
`subjective-label-workflow` (the Run graph) and `label-scanning` (who decides what) first. Which Run
comes before and after these is in `label-scanning-workflow`.

## Runs in this view

```text
step  run                          state
26    run-dstar-materialize    not built
```

A Run is named `rlNN_<operation>_<target>` on disk and shown as
`run-<operation>-<target>` on the page. Its Ticket is `<Page>/runs/<run>.yaml`
and its Result `<Page>/results/<run>/`, beside `labeling/`.

```text
5 close      on pass or accepted limit, allocate dstar-materialize
             and materialize D* with provenance shares
                                                               → corpus/final/D_star.jsonl + manifest.yaml
                                                               → audit/final_<n>/report.md
```

## Return

Return the Run address or `none`, the files written, and exactly one next
runnable Run or named human gate.
