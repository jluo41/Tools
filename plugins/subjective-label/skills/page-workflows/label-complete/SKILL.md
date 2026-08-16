---
name: label-complete
description: "Complete a subjective-labeling corpus after sealed evaluation by freezing a validated production policy, running preflight and idempotent labeling, routing risky items to humans or unresolved status, reconciling one terminal disposition per item, and performing a probability-based final audit with provenance. Use for /label-complete, production labeling, or corpus completion."
---

# Complete the corpus

Apply only a production route that passed the sealed evaluation for the intended claims.
Finish with one accountable disposition per corpus item and a human-audited quality
statement.

## Read first

Read:

- `../../../ref/ref-contract.md`
- `../../../ref/ref-schema.md`
- `../../../ref/ref-stages.md`
- `../../../ref/ref-assets.md`
- `../../../ref/ref-architecture.md`
- `../../../ref/ref-cascade.md`
- `../../../ref/ref-output-style.md`

## Preconditions

Require valid `G*`, `D_cal*`, and `T*`; closed scorecards; a candidate that passes all
required quality floors; and a declared remaining in-scope corpus. Otherwise stop with
`HOLD` or select human-only completion explicitly.

## Protocol

1. **Freeze production manifest.** Record corpus scope, policy and executor checksums,
   full routing rule, thresholds, abstention, risk queue, human capacity, budget, shard
   plan, retries, provenance tiers, and final-audit design.
2. **Run preflight.** Use a frozen probability sample to estimate route shares, risk
   queue size, quality linked to `T*`, cost, latency, and capacity. Do not change
   thresholds without creating a new manifest and preserving the old result.
3. **Execute idempotently.** Write every attempt append-only with item, run, policy,
   executor, wrapper, input checksum, output, reason codes, confidence, and timestamps.
   Resume failed shards without overwriting prior attempts.
4. **Apply risk routing.** Escalate declared disagreement, boundary, novelty, coverage,
   policy-mismatch, protected-stratum, duplicate-conflict, and drift conditions. Keep
   over-capacity or unresolvable items unresolved; never relabel them as `NONE`.
5. **Record human review.** Human judgments override machine outputs semantically and
   retain links to both attempts. Production review does not silently mutate `G*`; a
   material policy issue opens a new calibration/versioning decision.
6. **Reconcile terminals.** Create exactly one terminal disposition for every in-scope
   item: human-confirmed, audited-machine, machine-accepted, accepted-unresolved,
   excluded, or invalid. Report missing and duplicate terminal ids as hard failures.
7. **Run final probability audit.** Freeze sampling strata, seed, probabilities, blind
   human protocol, thresholds, and claims. Estimate weighted errors and intervals,
   inspect protected strata and route-specific failures, and document repairs.
8. **Close or reopen.** Create completed `D*` only when completeness, provenance,
   quality, and risk gates pass. Otherwise repair, re-audit, narrow claims, or reopen
   calibration with explicit versions.

## Result

Return total scope; terminal count; labels and dispositions by provenance; unresolved,
excluded, and invalid counts; route shares; human-review load; cost and latency; final
audit estimate and intervals; repairs; protected claims; limitations; and artifact paths.

Embeddings, classifier confidence, and LM consensus are permitted only inside the exact
validated route. If the production runner, reconciler, audit sampler, or provenance
writer is absent, emit `HOLD`; do not fall back to legacy k-NN inheritance or panel
majority.
