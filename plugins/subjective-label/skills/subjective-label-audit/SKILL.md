---
name: subjective-label-audit
description: >-
  The Quality › Audit view skill of the subjective-label family: it
  audits the completed labels independently: a frozen probability design, a blind human sample, and the weighted analysis with its route. Every Run in this view names this skill, and no other view uses it.
  Use for final audit, audit-sample, audit-human-gold, audit-analyze, repair, rescan, or /subjective-label-audit.
metadata:
  version: "0.1.0"
  last_updated: "2026-09-29"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /subjective-label-audit · Quality Space › Audit

This skill owns the Runs of the labeling workbench's Quality › Audit
view: every Run card there names it, and no other view uses it (JL 260929:
one skill per view). Load `subjective-label` (the family door),
`subjective-label-workflow` (the Run graph) and `label-scanning` (who decides what) first. Which Run
comes before and after these is in `label-scanning-workflow`.

## Runs in this view

```text
step  Run Type                     state
23    audit-sample         not built
24    audit-human-gold     not built
25    audit-analyze        not built
```

A new Run uses `run-labeling-<operation>-<MMDD>-<target>` on disk and
on the page. Older short-named Tickets remain readable. Its Ticket is
`<Page>/runs/<run>.yaml`
and its Result `<Page>/results/<run>/`, beside `labeling/`.

```text
0 design     freeze the episode commission: population, strata, seed, inclusion probabilities, blind protocol,
             thresholds, protected claims, frozen BEFORE any production label is
             shown to the auditor                              → audit/final_<n>/design.yaml
1 sample     allocate audit-sample; draw under the design       → audit/final_<n>/sample.jsonl
2 gold       allocate audit-human-gold; blind human judgment    → audit/final_<n>/human_gold.jsonl
3 analyze    allocate audit-analyze; weighted error with intervals; failures by route, executor, class,
             region, protected stratum                         → audit/final_<n>/findings.json
             pass · repair · rescan · semantic · limit          → audit/final_<n>/receipt.json
4 repair     declared strata repaired, versioned, then back to design under
             final_<n+1>                                       → audit/final_<n>/repairs.jsonl
```

The repair loop is steps 4 → 0 under a new folder; a receipt is never edited.
`rescan` Routes to a new `scan-preflight` Run with `run_<n+1>`; `semantic`
Routes to `round-prepare` under a new Building lineage. Record invalidation
and affected Runs in the authorized source Run receipt or job control; do not
derive either Route from a compatibility tag.

## Return

Return the Run address or `none`, the files written, and exactly one next
runnable Run or named human gate.
