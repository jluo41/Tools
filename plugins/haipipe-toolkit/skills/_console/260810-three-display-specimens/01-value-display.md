# DV-01 · Coefficient stability across regression specifications

specimen: illustrative only
origin: value
evidence: bound
visual: candidate
narrative: claim-linked
paper: not-requested
probe: V2-E1
paper_eligibility: direct-adopt

## Purpose

Can one table show whether the estimated association survives the specification choices that a
claim depends on?
This Value Display exists so the analyst and Narrative can judge the result before deciding whether
a paper reader needs to see it.

## Display

**Candidate regression table**: illustrative estimates used only to test the display anatomy.

| Specification | Estimate | 95% CI | Controls | Fixed effects | N |
|---|---:|---:|---|---|---:|
| M1 · unadjusted | 0.18 | [0.11, 0.25] | no | no | 8,420 |
| M2 · patient adjusted | 0.15 | [0.08, 0.22] | patient | no | 8,420 |
| M3 · organization adjusted | 0.13 | [0.06, 0.20] | patient + organization | no | 8,420 |
| M4 · preferred | 0.12 | [0.05, 0.19] | full | organization + year | 8,420 |

## Reading

Five-second takeaway: the estimate shrinks after adjustment but does not change direction, and the
preferred interval remains above zero.
The table supports an association claim only.
It does not establish causality, mechanism, or generalization beyond the analyzed cohort.

## Provenance

| Printed element | Source required in a real unit | Status in this specimen |
|---|---|---|
| estimates and intervals | exact Value binding and run path | illustrative |
| specification labels | model configuration | illustrative |
| sample size | cohort artifact and exclusions | illustrative |
| preferred-model designation | predeclared analysis rule or dated decision | illustrative |

No number from this specimen may be used substantively.

## Claim interface

claim: C1
role: candidate punchline
permission: association only
boundary: cohort and specification dependent

## Paper eligibility

decision: `direct-adopt`

This table can be adopted unchanged if its real version resolves every provenance row, uses labels a
target reader understands, and Narrative selects C1 as a paper claim.
Paper adoption may add a caption, label, acceptance record, and placement.
It may not create a second independently edited copy of the estimates.
