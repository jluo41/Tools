# Reference: human-grounded agent architecture

This reference defines roles, access, write authority, and call order for the revised subjective-label system.
One human is the semantic authority.
Models create evidence and execution artifacts but do not substitute for that authority.

## 1. Family topology

```text
subjective-label umbrella
├── 🏗 label-building
│   ├── Human semantic authority ↔ Strong calibration agent
│   ├── Embedder · Candidate selector · Weak executors
│   ├── Comparison auditor · Guideline optimizer · Checkpoint keeper
│   └── Test custodian (reservation only) · Label Handoff keeper
│
├──────────── signed Label Handoff ────────────▶
│
└── 🔍 label-scanning
    ├── Test custodian (authorized release)
    ├── Final evaluator
    ├── Production executor + terminal reconciler
    └── Final audit keeper

subjective-label-workflow sits above both sides and owns the phase numbers,
gates, and the crossing; label-building-workflow and label-scanning-workflow
order the steps inside each side; the doors own the law.
```

The sibling doors have different questions and write authority. Building asks
whether the construct matches the human and ends at the handoff. Scanning asks
whether that frozen construct was executed reliably and ends at audited `D*`.
The strong calibration agent remains the only conversational door for semantic
and blind-human judgments; this does not grant it semantic or canonical-write
authority.

## 2. Authority matrix

| role | may read | may write | may propose | may decide | forbidden |
|---|---|---|---|---|---|
| human semantic authority | item, prior closed policy, post-lock comparison | human-first and final decisions through the keeper | label, region, reason, rule wording | class, region, semantic patch, concept revision, stop signoff, risk acceptance | viewing weak predictions before first-pass lock |
| strong calibration agent | allowed Session context | chat and proposal records | contrast questions, rules, regressions, impacts | interaction order only | creating gold, accepting semantic patches, revealing sealed outputs early |
| embedder | corpus text and embedding config | vector cache, index, clusters, distances | none | none | semantic label decisions |
| candidate selector | eligible ids, scores, gold anchors, sealed committee signatures | `C_t` and `B_t` manifests | quotas and sampling plan | selection under approved config | writing class or region gold |
| weak executor | closed policy, wrapper, assigned item | its own prediction record | predicted class, region, confidence, reason | none | seeing peer outputs or human answer before run close |
| comparison auditor | sealed predictions and human records after release | comparison, disagreement, consensus-failure, and error-taxonomy records | error category and affected strata | none | final label or policy acceptance |
| guideline optimizer | accepted human evidence and model error records | policy patch proposal and regression plan | smallest general patch | none | accepting its own patch |
| checkpoint keeper | full round package and human evidence | closed checkpoint, `D_t`, closed `G_t` | HOLD or close recommendation | artifact validity only | inventing human evidence or semantic acceptance |
| test custodian | sealed manifest and authorized freeze state | access log and test release | invalidation warning | access authorization from contract | exposing test text during calibration |
| final evaluator | frozen `G*`, registered wrappers, `T*` gold after lock | frozen predictions and scorecards | eligible executor set | metric computation only | changing scored systems or test gold |
| production executor | frozen production manifest and corpus remainder | attempts, predictions, risk queue | route disposition | automatic acceptance under frozen rule only | waiving risk thresholds or writing human gold |
| final audit keeper | production terminal records and audit frame | audit sample, findings, repairs, receipt | pass, expand, repair, or reopen recommendation | statistical acceptance under frozen rule | changing semantic policy silently |

## 3. Human interaction protocol

Every calibration item follows this access order:

```text
item text + prior closed policy
        ↓
human-first record
        ↓ immutable lock
release weak-model comparison
        ↓
clarification and contrast
        ↓
final human decision
        ↓
policy proposal and checkpoint evidence
```

The strong agent must not hint at vote direction, confidence, region, or model rationale before the lock.
Selection reason may be hidden when it reveals model predictions.

## 4. Weak-executor committee

The former persona panel becomes a committee of independent executors.
Personas may still be used as experimental wrappers, but persona majority is not a semantic authority.

Committee requirements:

- same closed core policy;
- independently registered wrappers;
- no peer output access;
- fixed schema and run settings;
- prediction, optional region, confidence, concise structured reason, and provenance;
- immutable seal before human batch finalization.

Consensus is one sampling stratum.
Every later human batch includes a stratified random consensus audit.

## 5. Building call graph

Round 1:

```text
umbrella → label-building Contract → Test Custodian reserve → embedder
         → random sampler → strong calibration agent → checkpoint keeper
```

Round 2 onward:

```text
umbrella → label-building Round
→ candidate selector
   → embedder
   → optional classifier or region scorer
→ weak executors in parallel
→ comparison auditor for signatures
→ candidate selector for B_t composition
→ strong calibration agent and human
→ guideline optimizer
→ checkpoint keeper
```

After the stopping conjunction and human signoff pass:

```text
label-building freeze (P2)
→ Label Handoff keeper rehashes G* + D_cal* + custody
→ records the signed immutable Label Handoff
→ subjective-label-workflow tests G2
```

## 6. Final evaluation call graph

```text
umbrella → label-scanning Test
→ verify valid Label Handoff
→ test custodian releases T* text
→ strong calibration agent records blind human gold
→ test custodian locks gold
→ final evaluator runs registered executors and baselines
→ final evaluator writes scorecards
```

The evaluator remains read-only over `G*`, wrappers, test gold, and candidate registry.

## 7. Production and audit call graph

```text
umbrella → label-scanning Scan
→ production-policy selection from frozen scorecards and handoff
→ preflight
→ production executor
→ human risk review through strong calibration agent
→ terminal reconciler
→ final audit keeper
→ repair or complete
```

The production and audit roles must not silently revise `G*`.
A semantic failure returns the project to calibration and follows final-test invalidation rules.

## 8. Canonical write authorities

| artifact family | sole canonical writer |
|---|---|
| embeddings and vector indexes | Embedder |
| candidate and human-batch manifests | Candidate selector |
| one executor's predictions | that executor's registered run |
| human-first and final Session records | strong agent recording inspectable human input |
| cumulative human gold and closed policy | Checkpoint Keeper |
| signed Label Handoff | Label Handoff Keeper recording the human freeze signature |
| sealed manifest and access log | Test Custodian |
| final predictions and scorecards | Final Evaluator |
| production attempts and terminal labels | Production Executor plus reconciler |
| final audit and repair receipt | Final Audit Keeper |

Rendered Markdown views are generated from canonical records and have no independent authority.

## 9. Failure and HOLD behavior

An agent stops with an explicit HOLD when:

- required human evidence is absent;
- the sealed-access rule would be violated;
- artifact checksum or parent version mismatches;
- a required engine capability has not shipped;
- a metric lacks a valid population or denominator;
- a policy change would invalidate a final claim;
- high-severity risk lacks an owner.

The HOLD names the missing evidence, affected artifact, current safe state, and next authorized actor.

## 10. Retired assumptions

The canonical architecture forbids:

- persona or model majority as gold;
- unanimous committee cases bypassing probability audit;
- Category D auto-resolution into cumulative gold;
- public-dataset kappa as the project stop rule;
- model-model agreement as correctness;
- embedding or classifier confidence as semantic authority;
- one agent predicting, adjudicating, writing gold, and approving its own checkpoint.
