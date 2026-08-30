# Reference: project artifacts and write ownership

Every project artifact lives under `{project_dir}/`.
Canonical records are machine-readable and immutable after close.
Human-readable Markdown files are rendered views and never a second source of truth.

## 1. Directory layout

```text
{project_dir}/
├── config.yaml
├── .state.json
├── REPORT.md
├── corpus/
│   ├── manifest.json
│   ├── items.jsonl
│   └── final/
│       ├── D_star.jsonl
│       └── manifest.yaml
├── cache/
│   └── embeddings/
├── policy/
│   ├── current
│   └── versions/
│       └── G_01/
│           ├── manifest.yaml
│           ├── guideline.md
│           ├── boundaries.yaml
│           ├── procedure.yaml
│           ├── uncertainty.yaml
│           ├── casebook.jsonl
│           ├── wrappers/
│           ├── diff.yaml
│           └── regression.jsonl
├── rounds/
│   └── round_01/
│       ├── manifest.yaml
│       ├── candidate_pool.jsonl
│       ├── prelabels/
│       ├── human_batch.jsonl
│       ├── sessions/
│       ├── human_final.jsonl
│       ├── policy_draft/
│       ├── metrics.json
│       ├── coverage.json
│       ├── risk_ledger.jsonl
│       └── checkpoint.json
├── gold/
│   ├── cumulative.jsonl
│   └── cumulative.md
├── handoff/
│   └── label-v1.yaml
├── test/
│   ├── sealed/
│   │   ├── manifest.enc-or-protected
│   │   ├── access_log.jsonl
│   │   └── status.json
│   └── final/
│       ├── human_first.jsonl
│       ├── human_gold.jsonl
│       └── consistency.json
├── evaluation/
│   ├── registry.yaml
│   ├── predictions/
│   ├── baselines/
│   ├── scorecards/
│   └── summary.md
├── production/
│   └── run_01/
│       ├── manifest.yaml
│       ├── preflight.json
│       ├── attempts.jsonl
│       ├── risk_queue.jsonl
│       ├── human_final.jsonl
│       ├── terminal_labels.jsonl
│       └── run_report.md
└── audit/
    └── final_01/
        ├── design.yaml
        ├── sample.jsonl
        ├── human_gold.jsonl
        ├── findings.json
        ├── repairs.jsonl
        ├── provenance_summary.json
        └── report.md
```

## 2. Canonical versus rendered artifacts

Canonical files contain ids, versions, checksums, fields, and event records.
Rendered files summarize them for people.

Required rendered views:

- `REPORT.md`: current state, active gate, latest quality evidence, coverage, risk, and next action;
- `gold/cumulative.md`: compact human-confirmed examples with class, region, reason, and checkpoint;
- policy cheatsheet inside every closed policy version;
- round metrics and policy-diff view;
- final model-scorecard summary;
- production and final-audit reports.

Rendered files may be regenerated and never confer gold or close a state.

## 3. Round package

`candidate_pool.jsonl` contains `C_t` selection evidence.
For Round 1 it may be empty because the random human batch is prepared directly at initialization.

`prelabels/<executor>.jsonl` contains one registered executor's immutable `P_t` rows.
Round 1 may have no prelabels.

`human_batch.jsonl` freezes `B_t` membership, role, stratum, probability, seed, and blind-access state.

`sessions/` stores:

- chat and resume records;
- human-first item events;
- pre-label release events;
- final human events;
- correction, clarification, and concept-revision classification;
- policy proposals and backward-impact candidates.

`checkpoint.json` joins all round checksums and is the only artifact that promotes human gold and a closed policy.

## 4. Human gold

`gold/cumulative.jsonl` contains only human-confirmed final records from closed checkpoints.
It never contains:

- model-unanimous rows without human confirmation;
- model-majority rows;
- classifier or nearest-neighbor inheritance;
- unknown-provenance gallery migrations;
- unresolved items represented as `NONE`.

Each row links to the human event, policy, round, checkpoint, and any later superseding record.

At calibration stopping, the closed cumulative file is frozen by checksum as `D_cal*`.
It remains development gold and is not copied or renamed to completed `D*`.

## 5. Label Handoff

`handoff/label-v1.yaml` is the only authority crossing from Label Building
to Label Scanning. It binds the corpus snapshot, schema, `G*`, `D_cal*`,
sealed-test manifest checksum, stopping evidence, lineage, and human freeze
signature without carrying protected ids or test text. Read
`ref-label-handoff.md` for the complete contract.

The handoff is immutable after close. Scanning binds its exact checksum rather
than following `policy/current`; a semantic change creates a new lineage and
invalidation receipt.

## 6. Annotation policy

Every policy version has one manifest and separate components:

| component | responsibility |
|---|---|
| `guideline.md` | concise trait and class definitions plus evidence and exclusions |
| `boundaries.yaml` | H/L, L/N, H/N, and HLN tests |
| `procedure.yaml` | ordered executor decision procedure |
| `uncertainty.yaml` | confidence, escalation, unresolved, and missing-context rules |
| `casebook.jsonl` | compact canonical centers, counterexamples, and boundaries |
| `wrappers/` | model-specific output and interface instructions |
| `diff.yaml` | semantic, procedural, casebook, wrapper, and editorial changes |
| `regression.jsonl` | affected prior gold and patch outcomes |

`policy/current` points to the latest closed version.
It never points to a draft.

## 7. Sealed test

The sealed manifest exists at initialization and is readable only by the custodian until `G*` freezes.
Its protected identifier storage may be encrypted or isolated by filesystem permissions.

The access log records:

- actor;
- timestamp;
- requested operation;
- authorization source;
- resolved item count;
- success or denial;
- invalidation consequence.

Final human-gold files appear only after authorized release and remain hidden from candidate executors until their predictions close.

## 8. Evaluation

`registry.yaml` freezes:

- candidates and model families;
- seen or held-out role;
- policy and wrapper checksums;
- decoding and repeat rules;
- minimal-instruction baseline;
- metric and selection protocol.

Every prediction is append-only and linked to one run.
Every scorecard links to predictions, `T*` gold, metric code or definition, intervals, costs, and errors.

## 9. Production

The production manifest freezes the selected policy, executor route, thresholds, risk rules, budgets, shard plan, and preflight evidence.
Attempts are append-only and idempotent by item plus run identity.

`terminal_labels.jsonl` contains one reconciled disposition per in-scope item.
It retains human, audited-machine, machine-accepted, accepted-unresolved, excluded, and invalid provenance tiers.

After the final audit and repair gates pass, `corpus/final/D_star.jsonl` materializes the
completed corpus from reconciled terminal rows. Its manifest links the corpus snapshot,
`G*`, `D_cal*`, `T*`, selected scorecard, production run, final audit, provenance counts,
and accepted limitations. Before that close, terminal labels are a completed-corpus
candidate rather than `D*`.

## 10. Final audit

The final audit design freezes its target population, strata, seed, probabilities, blind-human protocol, thresholds, and protected claims.
Findings link each error to production route, policy, executor, class, region, and risk neighborhood.

Repairs are versioned and followed by new evidence.
The final report states provenance shares, weighted error and interval, protected-stratum results, accepted limitations, and any reopened scope.

## 11. Write ownership

| artifact | canonical writer |
|---|---|
| vector cache and indexes | Embedder |
| `C_t` and `B_t` manifests | Candidate Selector |
| executor predictions | registered executor run |
| Session human records | Strong Calibration Agent recording human input |
| closed policy, cumulative gold, checkpoint | Checkpoint Keeper |
| signed Label Handoff | Label Handoff Keeper recording the human freeze signature |
| sealed manifest and access log | Test Custodian |
| final predictions and scorecards | Final Evaluator |
| production attempts and terminal labels | Production Executor plus reconciler |
| final audit and repair receipt | Final Audit Keeper |

## 12. Migration

Before writing v2 artifacts, inventory old gallery, guideline, iteration, validation, and output files.
Classify each old label as human-confirmed, model-only, or unknown from inspectable evidence.

Preserve old files read-only under a migration archive.
Do not rewrite provenance in place and do not infer human confirmation from unanimity, majority, or a high kappa score.
