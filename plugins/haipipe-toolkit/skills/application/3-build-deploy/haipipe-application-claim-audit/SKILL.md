---
name: haipipe-application-claim-audit
description: "Claim audit for the intervention lifecycle. Verifies that every claim in the intervention's artifacts is traceable to a SETTLED ledger claim in 1-claims.md (whose evidence is a probe section's target: QA file in the task/discovery bank) and that no claim exceeds the evidence scope. Parallel to paper's claim-audit skill. Trigger: claim audit, verify claims, evidence check, /haipipe-application claim-audit."
argument-hint: "[intervention-path]"
allowed-tools: Bash, Read, Grep, Glob, Skill
metadata:
  version: "1.2.1"
  last_updated: "2026-07-14"
  summary: "Claim-evidence audit — traceability + scope check. Paper-alignment sweep: ledger path updated to the 1-claims stage folder. v1.2.0 (probe redesign, Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3 approved JL 2026-07-14): the audit reads 1-probes/PP*.md — each section's target: names the QA file its claim cites — while the claim's STATUS is read from 1-claims.md, its only home (R7: 'verdict'/'verdicted' deleted). v1.2.1: the CHECKLIST itself still asked for 'the PP card backing the claim' and scoped statements against 'the verdict's scope' — both RETIRED. It now checks that the probe SECTION exists, that its `target:` still resolves to a live QA file, and that the statement stays inside the scope the QA file's ## Caveats and the 1-claims.md status line actually support."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-application-claim-audit
========================================

Cross-references the intervention's artifacts against the claim
ledger and KB to catch:

1. **Orphan claims:** artifact says something not in the claim ledger
2. **Overclaims:** artifact states a claim more strongly than evidence supports
3. **Stale citations:** artifact cites a claim whose verdict has been superseded
4. **Missing citations:** factual statement with no ledger/verdict backing


Audit scope
============

```
Reads:
  0-lifecycle/1-claims/1-claims.md   (claim ledger)
  0-artifacts/*.md              (drafted artifacts)
  1-probes/PP*.md               (probe files: each section's target: → the QA file its
                                 claim cites; the STATUS itself lives in 1-claims.md)

Writes:
  0-artifacts/CLAIM_AUDIT.md    (audit report)
```


Audit checklist per artifact
==============================

```
For each factual statement in the artifact body:
  [ ] Statement maps to a claim C## in the ledger
  [ ] Claim C## status is supported or weak (not GAP)
  [ ] If weak: artifact qualifies the statement appropriately
  [ ] The probe SECTION backing the claim exists (`PP<NN> § Q<n>`), its
      `target:` still resolves to a live QA file, and the claim's status in
      1-claims.md is still current
  [ ] Statement does not exceed the SCOPE the evidence supports — read the
      QA file's ## Caveats and the claim's status line in 1-claims.md
      (e.g., the evidence holds "in high-variability patients" but the
       artifact generalizes to "all patients")
```


Risk profile
=============

READ-ONLY on all source files. WRITES one audit report.
