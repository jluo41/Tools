---
name: haipipe-labeling-final-labels
description: >-
  The Delivery › Final labels view skill of the labeling theme: it
  publishes the audited final label set D* with its provenance shares, after the audit passes or its limit is accepted. Every Run in this view names this skill, and no other view uses it.
  Use for final labels, D*, dstar-materialize, publishing the labeled corpus, or /haipipe-labeling-final-labels.
metadata:
  version: "0.1.0"
  last_updated: "2026-09-29"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-labeling-final-labels · Delivery Space › Final labels

This skill owns the Runs of the labeling workbench's Delivery › Final labels
view: every Run card there names it, and no other view uses it (JL 260929:
one skill per view). Load `haipipe-labeling` (the family door),
`haipipe-labeling-workflow` (the Run graph) and `haipipe-labeling-scanning` (who decides what) first. Which Run
comes before and after these is in `haipipe-labeling-scanning`.

## Runs in this view

```text
step  Run Type                     state
26    dstar-materialize    not built
```

A new Run uses `run-labeling-<operation>-<MMDD>-<target>` on disk and
on the page. Older short-named Tickets remain readable. Its Ticket is
`<Page>/runs/<run>.yaml`
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
