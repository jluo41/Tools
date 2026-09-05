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
├── register.md                       the seven regions × open / covered / risky
├── gates/
│   ├── p0-contract/receipt.json       immutable P0 import/checksum receipt
│   └── g0/receipt.json                human meaning confirmation + G0 binding
├── runs/
│   └── rNN_labeling-<operation>_<target>.yaml      authored Run Ticket
├── results/
│   └── rNN_labeling-<operation>_<target>/
│       ├── runtime.yaml              lifecycle and attempt trail
│       └── result.yaml               safe pointers to canonical domain Results
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
│       ├── G_00/                     the Contract's seed guideline
│       └── G_01/
│           ├── manifest.yaml
│           ├── guideline.md
│           ├── boundaries.yaml
│           ├── procedure.yaml
│           ├── uncertainty.yaml
│           ├── casebook.jsonl
│           ├── wrappers/
│           ├── diff.yaml
│           ├── regression.jsonl
│           ├── cheatsheet.md         rendered: one screen of class rules + seven region tests
│           └── gallery.md            rendered: 2-3 real items per region from D_t, with the reason
├── rounds/
│   └── round_01/                     one ROUND UNIT (§3)
│       ├── card.md                   the wager · first file · proposed → released → landed
│       ├── README.md                 id · lineage · serves · state · closed:
│       ├── manifest.yaml             the compiled batch (the unit's spec)
│       ├── evidence.md               what the round may read, by checksum
│       ├── prospect.md               the forecast, written before judging
│       ├── candidate_pool.jsonl
│       ├── prelabels/
│       ├── human_batch.jsonl
│       ├── sessions/
│       ├── human_final.jsonl
│       ├── policy_draft/
│       ├── metrics.json
│       ├── coverage.json
│       ├── risk_ledger.jsonl
│       ├── checkpoint.json           the close · the only artifact that promotes gold and policy
│       └── view/                     rendered, regenerable, never authority
│           ├── judgments.md          item · sealed guess · first · final · change type
│           ├── rules.md              diff G_(t-1) → G_t + backward impact on prior gold
│           └── result.md             prospect vs actual · one line per gate · the route
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
│       ├── consistency.json
│       └── lock.json                 T* locked; SCORE may start
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
        ├── receipt.json              the G6 receipt: route, and on pass the D* checksum
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

## 2a. Labeling Run dialect

The project root is one Level-3 Labeling job. Every allocated Level-4 Run uses
one generic envelope:

```text
runs/<RUNNAME>.yaml
results/<RUNNAME>/runtime.yaml
results/<RUNNAME>/result.yaml
```

The envelope points to the canonical artifacts already owned by P0-P5; it does
not copy them or become semantic authority. The 25 operation kinds include
bounded P0 construction, P1 calibration work, P2 handoff, P3 prediction and
scoring, P4 shards and review, and P5 audit and materialization. Round, Test,
Scan, and Audit are grouping episodes, not extra Runs. Item events, tool calls,
and retries under unchanged frozen inputs stay inside the relevant operation.
Read `ref-run.md` for allocation, count law, completion gates, and presentation.

The `gates/` receipts are phase authority, not Run envelopes.  In particular,
the Board Labeling surface must call the canonical status evaluator whenever a
P0 or G0 receipt exists; it may show a compatibility file-presence view only
for historical lanes that have no canonical receipt yet.

## 3. Calibration Round episode

A round is one grouping folder: proposed as a card, realized by the independent
operations `label-building-workflow` orders, closed by a checkpoint, and cited
by the Job Page's `§2 · Rounds` division by id. A proposed Card is planning and
has no `round-prepare` Run until a person releases it.

### card.md · the wager, the folder's first file

```markdown
# round_03 · <slug>
state: proposed | released | landed
gap: HL, LN                    register cells targeted · round 1 writes `random`
arms: challenge 40 · audit 20  challenge = adaptively selected · audit = probability arm
seed: 20260830
expects: <one sentence: what disagreement or rule the batch should force>
released: <person> <YYMMDD>    written by a person only
landed: checkpoint-03          written at CLOSE
```

While `state: proposed` the folder holds `card.md` and nothing else. A killed
card keeps its folder forever with the reason inside.

### README.md · identity

```markdown
unit: round_03
lineage: <policy lineage id>
policy_in: G_02 · policy_out: G_03
serves: <Job Page id> · §2 Rounds
state: open | judged | closed@checkpoint-03
closed: <keeper> <YYMMDD> · route: another round | freeze | HOLD
```

### The compiled and bound files

`manifest.yaml` freezes `B_t` membership, role, stratum, inclusion probability,
seed, and blind-access state; it is compiled from the contract's quotas and the
prior checkpoint's coverage, never invented. `evidence.md` lists, by checksum,
what the round read: `G_(t-1)`, `D_(t-1)`, the candidate pool, the custody
status; a sealed-test id in it voids the round. `prospect.md` states the
expected disagreement per targeted cell, the rule the evidence should force,
and the audit-arm metric it should move, before the first item is shown.

### The canonical event files

`candidate_pool.jsonl` contains `C_t` selection evidence (empty in round 1).
`prelabels/<executor>.jsonl` holds one executor's immutable sealed rows (none in
round 1). `sessions/` is append-only: show, first, lock, reveal, final events
per item, plus policy proposals and backward-impact candidates. `human_final.jsonl`
is the per-item final decision with its change type. `checkpoint.json` joins
every checksum and is the only artifact that promotes human gold and a closed
policy.

### view/ · rendered, never authority

`judgments.md` (one row per item: sealed guess, first, final, change type),
`rules.md` (the `G_(t-1) → G_t` diff with every prior gold row it flipped),
`result.md` (prospect vs actual, one line per gate, the route). They are
regenerated from the canonical files; a view that disagrees with
`checkpoint.json` loses.

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
| `cheatsheet.md` | rendered: one screen of class rules and the seven region tests, what the Job Page's §1 quotes |
| `gallery.md` | rendered: two or three real items per region from `D_t`, each with the human's reason |

`policy/current` points to the latest closed version.
It never points to a draft.

## 6a. Register

`register.md` is the Building side's scoreboard: one row per diagnostic region
(H, L, N, HL, LN, HN, HLN), each `open`, `covered`, or `risky`, with the round
card currently targeting it and the checkpoint that last settled it.

```markdown
| cell | state | confirmed items | open card | last settled |
|---|---|---|---|---|
| HL | open | 4 | round_03 | checkpoint-02 |
```

A round card names the cells it targets; CLOSE settles them. The register is
written only by the Checkpoint Keeper at CLOSE (and by Contract at scaffold, all
cells `open`). What an open cell means for Freeze is `label-building` §The
register's law, not restated here.

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

`registry.yaml` is the single definition of what P3 freezes (the ORDER skill
points here; `ref-config.md` §4 gives the per-candidate entry schema):

- the bound Label Handoff checksum;
- candidates and model families, each with seen or held-out role;
- policy and wrapper checksums;
- decoding and repeat rules;
- the minimal-instruction baseline;
- metrics, quality floors, and the selection rule.

Every candidate prediction is the canonical Result of one independently
addressed `executor-predict` Run in the Test episode.
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
| executor predictions | registered executor through one `executor-predict` Run |
| Session human records | Strong Calibration Agent recording human input |
| closed policy, cumulative gold, checkpoint | Checkpoint Keeper |
| round card `released:` | a person |
| `register.md` | Checkpoint Keeper (Contract scaffolds it) |
| `view/`, `cheatsheet.md`, `gallery.md`, `README.md` | rendered by the Keeper at close; regenerable |
| signed Label Handoff | Label Handoff Keeper recording the human freeze signature |
| sealed manifest and access log | Test Custodian |
| `evaluation/registry.yaml` | Final Evaluator, frozen before release; the Test Custodian refuses release without it |
| final predictions and scorecards | Final Evaluator |
| production attempts and terminal labels | Production Executor plus reconciler |
| final audit and repair receipt | Final Audit Keeper |

## 12. Migration

Before writing v2 artifacts, inventory old gallery, guideline, iteration, validation, and output files.
Classify each old label as human-confirmed, model-only, or unknown from inspectable evidence.

Preserve old files read-only under a migration archive.
Do not rewrite provenance in place and do not infer human confirmation from unanimity, majority, or a high kappa score.
