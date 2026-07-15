---
name: haipipe-application-claim-audit
description: "Claim audit for the intervention lifecycle. Verifies that every claim in the intervention's artifacts is traceable to an adopted A entry (A -> C -> anchor) and that no claim exceeds the evidence scope. Parallel to paper's claim-audit skill. Trigger: claim audit, verify claims, evidence check, /haipipe-application claim-audit."
argument-hint: "[intervention-path]"
allowed-tools: Bash, Read, Grep, Glob, Skill
metadata:
  version: "1.1.0"
  last_updated: "2026-07-06"
  summary: "Claim-evidence audit — traceability + scope check. Paper-alignment sweep: ledger path updated to the 1c-claims stage folder (ladder restage 2026-07-09)."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-application-claim-audit
========================================

Cross-references the intervention's artifacts against the claim
ledger and KB to catch:

1. **Orphan claims:** artifact says something not in the claim ledger
2. **Overclaims:** artifact states a claim more strongly than evidence supports
3. **Stale citations:** artifact cites a K/W entry that has been superseded
4. **Missing citations:** factual statement with no K/W backing


Audit scope
============

```
Reads:
  0-lifecycle/1d-advice/1d-advice.md  (design advice -- the A<-C chain)
  0-lifecycle/1c-claims/1c-claims.md          (claim ledger)
  0-artifacts/*.md              (drafted artifacts)
  insights/K_knowledge/*.md     (K entries, when cited)
  insights/W_wisdom/*.md        (W entries, when cited)

Writes:
  0-artifacts/CLAIM_AUDIT.md    (audit report)
```

Trace chain: every artifact move -> the `A<n>` it executes -> the `C<n>` each A derives from -> the claim's anchor. A break anywhere in artifact -> adopted A -> C -> anchor is a finding.


Audit checklist per artifact
==============================

```
For each factual statement in the artifact body:
  [ ] Statement maps to a claim C## in the ledger
  [ ] Claim C## status is supported or weak (not GAP)
  [ ] If weak: artifact qualifies the statement appropriately
  [ ] Cited K/W entry exists and is active (not superseded)
  [ ] Statement does not exceed the K entry's scope
      (e.g., K says "in high-variability patients" but artifact
       generalizes to "all patients")
```


Risk profile
=============

READ-ONLY on all source files. WRITES one audit report.
