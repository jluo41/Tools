# Reference: Labeling Run dialect

Read this file whenever planning, allocating, resuming, counting, presenting,
or auditing Runs inside one subjective-label job. Load `haipipe-run` first for
the neutral Level-4 contract. This file defines only the Labeling domain's
operation catalog, physical resolver, completion gates, and count law.

## 1. Identity: Run Type, Run Spec, Run, episode, gate

Keep four things distinct:

```text
operation kind   Labeling Run Type for independently closable work
Run Spec         one planned bounded commission in a Workflow Definition
Run              one allocated instance of a Run Spec for one target
episode          domain grouping such as round_03 or production_01; not a Run
gate event       a named human/Keeper authorization; normally evidence on a Run
```

One job is one corpus snapshot × one target construct × one identified human
semantic authority. It is the Level-3 work object, not a Run. `Round`, `Test`,
`Scan`, and `Audit` are episodes that group Run Specs, Instances, and domain
artifacts; do not add them to the Run count. A Workflow is the list of
Run Specs and their dependency/Route graph; its runtime is the allocated native
Run Instances and their receipts. P0-P5 are compatibility capability tags on
Labeling records only. They do not own Specs, Runs, gates, Routes, or lifecycle
state. Retain serialized `phase` fields when a reader expects them, but do not
use them as routing or allocation authority.

Mint a Run only when all neutral criteria hold: one frozen target, one authored
Ticket, one durable Result, and a disk-testable terminal state. Chat turns,
item judgments, API/model calls, retries under unchanged inputs, workflow
router invocations, and a person's bare `agree`, `release`, `stop`, or `sign`
event are not separate Runs.

A human-work operation may still be a Run. For example, `human-calibration`
commissions one bounded batch and returns a complete human-final record. The
person's individual judgments remain events inside that Run; only the named
person may write them.

## 2. One envelope, domain artifacts stay authoritative

Use one job-wide, monotonic `rlNN` address (`rl` = Run of Labeling). Never
renumber or infer it from a domain ordinal such as `round_03`. The prefix is
the native family identity, so the stem does not repeat `labeling-`:

```text
rl01_corpus-contract_job-v1
rl02_discovery-search_trait-definition
rl03_embedding-build_all-minilm-l6-v2
rl04_round-prepare_round-01
```

Every allocated Run has one control envelope:

```text
runs/<RUNNAME>.yaml                    authored Ticket; the only execution door
results/<RUNNAME>/runtime.yaml         lifecycle and attempt trail
results/<RUNNAME>/result.yaml          terminal safe receipt and artifact pointers
```

The envelope does not copy or replace canonical Labeling artifacts. The Ticket
binds its Run Spec commission, such as a released Card or frozen registry. The
Result records paths, checksums, counts, and the operation gate over the domain
artifacts listed below. Protected ids, raw item text, private judgments,
credentials, and model secrets never enter the envelope.

Use these required Ticket fields. A `phase` field may remain in a
legacy/current dialect record as a compatibility capability tag; it is never a
Run Spec identity or gate/Route authority:

```yaml
run: rl14_executor-predict_test-v1-executor-a
family: labeling
domain: subjective-label
phase: P3                          # compatibility capability tag only
operation: executor-predict
episode: test_01
target: {executor: executor-a, test: test-v1}
commission: {path: evaluation/registry.yaml, sha256: <hex>}
inputs: []
worker: {kind: api, name: <declared worker>}
acceptance: <named operation gate below>
supersedes: null
```

Create the runtime receipt with `status: planned` before work starts. A Result
envelope with missing canonical outputs is truthful non-success, never `Done`.
Existing `rNN_labeling-*` envelopes remain readable migration history. Never
rename or alias them; every newly allocated Labeling Run uses `rlNN`.

## 3. The 25 Labeling operation kinds

The table names each Labeling Run Type and its minimum canonical Result. A
Result envelope may bind more files required by the Run Spec's entry/exit
gates. Its P0-P5 value is compatibility metadata, not Workflow ownership.

| capability tag (compatibility only) | Run Type / operation | cardinality | bounded target | minimum canonical Result |
|---|---|---:|---|---|
| P0 | `corpus-contract` | 1 | one imported, fenced job snapshot | `gates/p0-contract/receipt.json` |
| P0 | `discovery-search` | D | one bounded external-evidence query | `discovery/search_<n>/result.json` |
| P0 | `guideline-seed` | G (optional) | one initial policy candidate per commissioned Run | `policy/versions/G_00/manifest.yaml` |
| P0 | `test-reserve` | T (optional) | one sealed-test reservation frame per commissioned Run | `test/sealed/status.json` |
| P0 | `embedding-build` | E (optional) | one corpus × embedder version per commissioned Run | `cache/embeddings/<version>/manifest.json` |
| P1 | `round-prepare` | N | one released Card | frozen `manifest.yaml`, batch, evidence, and prospect |
| P1 | `weak-prelabel` | ΣW_r | one round × weak executor | `rounds/round_<t>/prelabels/<executor>.jsonl` |
| P1 | `human-calibration` | N | one frozen human batch | complete `human_final.jsonl` plus Session events |
| P1 | `guideline-learn` | N | one round's accepted human evidence | ruled `policy_draft/` plus regression record |
| P1 | `round-measure` | N | one closed judgment set | `metrics.json`, `coverage.json`, risk ledger |
| P1 | `round-close` | N | one measured round | `checkpoint.json` and promoted G_t/D_t pointers |
| P2 | `handoff-freeze` | 1 | one stopped Building lineage | `handoff/label-v1.yaml` |
| P3 | `test-gold-lock` | 1 | one released sealed test | `test/final/lock.json` plus T* pointers |
| P3 | `executor-predict` | K | one registered executor × T* | `evaluation/predictions/<executor>.jsonl` or baseline equivalent |
| P3 | `executor-score` | K | one closed prediction Result × T* | `evaluation/scorecards/<executor>.json` |
| P3 | `executor-select` | 1 | one frozen registry and complete scorecard set | `evaluation/summary.md` |
| P4 | `scan-preflight` | 1 | one frozen production manifest | `production/run_<n>/preflight.json` |
| P4 | `scan-shard` | S | one manifest × corpus shard | declared shard attempts receipt |
| P4 | `risk-route` | 1 | one complete shard Result set | `production/run_<n>/risk_queue.jsonl` |
| P4 | `human-review` | 1 | one frozen risk queue, including an empty queue | `production/run_<n>/human_final.jsonl` |
| P4 | `reconcile` | 1 | one reviewed production episode | terminal labels and `run_report.md` |
| P5 | `audit-sample` | 1 | one frozen probability-audit design | `audit/final_<n>/sample.jsonl` |
| P5 | `audit-human-gold` | 1 | one blind audit sample | `audit/final_<n>/human_gold.jsonl` |
| P5 | `audit-analyze` | 1 | one audit sample with human gold | findings and `receipt.json` |
| P5 | `dstar-materialize` | 1 | one passing or accepted-limit audit | `corpus/final/D_star.jsonl` and manifest |

`D` is the number of bounded discovery queries, `N` the number of calibration
rounds, `W_r` the number of weak executors in round `r`, `K` the number of
qualification candidates including the baseline, and `S` the number of
production shards.

The expected happy-path instance count is:

```text
planned Runs = D + G + T + E + sum(W_r) + 5N + 2K + S + 12
```

`G`, `T`, and `E` may each be zero when that independent Run Type is not
commissioned. For `D=2`, `G=T=E=1`, `N=3`, `W=[0,2,2]`, `K=3`, and `S=1`, the planned
count is `43`. This is a plan, not an inventory claim. The actual count is the number of
allocated Run envelopes with a valid runtime receipt. Repairs, rescans,
semantic reopens, materially changed inputs, and superseding candidates add
Runs. Retries under an unchanged Ticket add attempts to the same Run.

Use `engine/run_catalog.py plan` for deterministic count and instance planning.

## 4. Allocation and dependency law

Allocate only at the last responsible moment, after the operation's commission
and authoritative inputs freeze. Preserve this dependency order:

```text
P0 (compat)  corpus-contract → G0 entry predicate → released Card → round-prepare
             discovery-search, guideline-seed, and test-reserve are separately
             commissioned Specs under their owner contracts; they are not a
             prerequisite chain for one another when initial contract artifacts
             suffice. embedding-build is separately commissioned after P0
             integrity passes and is not gated on G0.
P1 (compat)  released Card → prepare → weak-prelabel* → human-calibration
    → guideline-learn → round-measure → round-close
P2 (compat)  stopped checkpoints → handoff-freeze
P3 (compat)  frozen registry → test-gold-lock → executor-predict* → executor-score*
    → executor-select
P4 (compat)  frozen manifest → scan-preflight → scan-shard* → risk-route
    → human-review → reconcile
P5 (compat)  frozen design → audit-sample → audit-human-gold → audit-analyze
    → dstar-materialize
```

Parallelize only the starred Runs after their common prerequisite closes.
Never let an executor prediction see T* before `test-gold-lock` completes, and
never score an executor while its prediction Run remains open. These are
Run Spec dependencies and source-Run exit predicates; P0-P5 do not define the
dependency graph.

Human gates authorize or block the relevant Run Spec transition. Attach their
evidence to the owning Run Result/receipt, or to a named `resource_controls`
when the control changes job authority without an independently commissioned
Run. Never make a gate a Run solely to count it:

```text
meaning confirmation  validates the transition to round-prepare after a valid
                      corpus-contract Result; pending confirmation is not HOLD
Card release          commissions round-prepare after G0 passes
item/rule decisions   occur inside human-calibration/guideline-learn
stop signoff          permits handoff-freeze allocation
freeze signature      occurs inside handoff-freeze before promotion
test/audit gold       occur only inside their named human Runs
limitation acceptance permits dstar-materialize on an accepted-limit route
```

No model may synthesize a missing human event.

## 5. Completion and promotion

Mark each Run `complete` only when its declared canonical Result exists,
rehashes, and passes its operation-specific assertions. In addition:

- `round-close` alone promotes G_t/D_t and records the next route;
- `handoff-freeze` alone may write the immutable crossing after G2 and the
  exact human signature pass;
- `executor-select` applies the preregistered rule and selects at most one
  qualified route;
- `reconcile` proves one terminal disposition per in-scope item but produces
  only a candidate corpus;
- `audit-analyze` records pass, repair, rescan, semantic, or accepted-limit;
- `dstar-materialize` alone promotes the audited candidate into D*.

Completion does not imply promotion. Keep Result, gate receipt, and promotion
as separate facts in `result.yaml`.

## 6. Inventory and safe presentation

Enumerate the union of `runs/*.yaml` and `results/*/runtime.yaml`. Report an
orphan Ticket, orphan runtime, missing `result.yaml`, duplicate `run:`, path
mismatch, or invalid terminal gate explicitly. Count one row per allocated
logical Run, never per episode, capability tag, domain artifact, item, chat,
API call, or attempt. Put active and recovery-needed rows first.

`haipipe-plugin-labeling` owns operation. `haipipe-plugin-runs` presents the
same envelopes read-only and may group them by compatibility tag or episode. Show only safe
targets, checksums, counts, status, and Result pointers. Never add a second
approve, reveal, freeze, final, or run control.

If the allocator, worker, Keeper, or verifier required by an operation does
not exist in the implementation, return `HOLD` at the preserved Run frontier.
Do not backfill historical domain artifacts as Runs without authored Tickets
and truthful runtime receipts.
