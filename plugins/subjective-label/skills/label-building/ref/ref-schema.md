# Reference: subjective-label record schemas

This reference defines the machine-readable records shared by the router, subskills, agents, and later engine implementation.
Examples are illustrative JSON and YAML shapes, not a claim that every current library already writes them.

## 1. Semantic fields

Every completed human annotation keeps four independent fields:

```json
{
  "class_label": "high | low | none",
  "diagnostic_region": "H | L | N | HL | LN | HN | HLN",
  "uncertainty": {"level": "low | medium | high", "reason": "..."},
  "rationale": {"evidence": ["..."], "rejected_label": "...", "reason": "..."}
}
```

Rules:

- `class_label` is the final outcome field.
- `diagnostic_region` records why the case is typical or boundary-informative.
- `uncertainty` records procedural doubt.
- `rationale` records decisive evidence and the strongest rejected alternative.
- `none` means absent trait evidence and never substitutes for uncertainty or unresolved status.

## 2. Base item identity

Every record that refers to corpus content includes or resolves:

```json
{
  "item_id": "stable-id",
  "corpus_version": "sha256:...",
  "text_hash": "sha256:...",
  "source_metadata": {},
  "population_status": "eligible | excluded | invalid"
}
```

Raw text may live in one canonical corpus table rather than being copied into every artifact.
Sealed-test records use protected handles until authorized text resolution.

## 3. Candidate-pool record

`C_t` is selection evidence and contains no gold field:

```json
{
  "round_id": "round-02",
  "item_id": "r123",
  "source_pool": "H | L | N | HL | LN | HN | HLN | novelty | random",
  "scores": {"region": {}, "margin": 0.0, "novelty": 0.0},
  "ranker": {"name": "...", "version": "..."},
  "selection_reason": "...",
  "seed": 0,
  "inclusion_probability": null
}
```

Predicted region and similarity are typed scores, not human annotation fields.

## 4. Sealed pre-label record

Each weak executor writes one independent `P_t` row:

```json
{
  "round_id": "round-02",
  "item_id": "r123",
  "policy_version": "G_1",
  "policy_checksum": "sha256:...",
  "executor": {"name": "...", "version": "...", "family": "..."},
  "wrapper_checksum": "sha256:...",
  "run_id": "...",
  "prediction": "high | low | none",
  "predicted_region": "HN",
  "confidence": 0.62,
  "structured_reason": {
    "evidence": ["..."],
    "applied_rule": "rule-id",
    "rejected_label": "none",
    "uncertainty_reason": "..."
  },
  "seal_checksum": "sha256:...",
  "status": "success | failed"
}
```

Structured reasons are concise audit fields, not hidden chain-of-thought.
Failed outputs remain failed and are never imputed from committee consensus.

## 5. Human-batch manifest

Every `B_t` row preserves why it enters human review:

```json
{
  "round_id": "round-02",
  "item_id": "r123",
  "primary_role": "audit | challenge | coverage | carryover",
  "source_pool": "disagreement | mismatch | novelty | consensus",
  "stratum": {"predicted_class": "high", "predicted_region": "HN", "confidence_band": "mid"},
  "selection_probability": 0.12,
  "seed": 0,
  "batch_manifest_checksum": "sha256:...",
  "blind_access_state": "sealed"
}
```

Membership freezes before the Human-AI Session.

## 6. Human-first and final records

The blind initial judgment and the final human decision are separate immutable events:

```json
{
  "item_id": "r123",
  "round_id": "round-02",
  "human_id": "JL",
  "policy_version": "G_1",
  "first_pass": {
    "timestamp": "...",
    "class_label": "none",
    "diagnostic_region": "HN",
    "uncertainty": {"level": "medium", "reason": "..."},
    "rationale": {"evidence": ["..."], "rejected_label": "high", "reason": "..."},
    "prelabels_visible": false,
    "checksum": "sha256:..."
  },
  "final": {
    "timestamp": "...",
    "class_label": "high",
    "diagnostic_region": "HN",
    "uncertainty": {"level": "low", "reason": "..."},
    "rationale": {"evidence": ["..."], "rejected_label": "none", "reason": "..."},
    "change_type": "none | correction | clarification | concept_revision"
  },
  "prelabel_comparison": {},
  "backward_impact_ids": []
}
```

An unresolved item uses a workflow disposition:

```json
{"terminal_disposition":"unresolved","reason":"missing_context","owner":"JL","use_limitation":"exclude_from_training"}
```

It does not invent a fourth class.

## 7. Annotation-policy version

```yaml
policy_id: G_2
parent: G_1
status: draft | closed | final
components:
  core_guideline: guideline.md
  boundary_rules: boundaries.yaml
  decision_procedure: procedure.yaml
  uncertainty_policy: uncertainty.yaml
  casebook: casebook.jsonl
  wrappers: wrappers/
diff:
  semantic: []
  procedural: []
  casebook: []
  wrapper: []
  editorial: []
accepted_by: JL
checkpoint_id: checkpoint-02
checksum: sha256:...
```

Closed and final policy versions are immutable.

## 8. Checkpoint record

```json
{
  "checkpoint_id": "checkpoint-02",
  "round_id": "round-02",
  "parents": {"prior_policy": "G_1", "prior_gold": "D_1"},
  "artifacts": {"candidate_pool": "sha256:...", "prelabels": [], "human_batch": "sha256:...", "human_final": "sha256:..."},
  "closed_policy": "G_2",
  "cumulative_gold": "D_2",
  "metrics": "metrics-02",
  "coverage": "coverage-02",
  "risk_ledger": "risk-02",
  "human_evidence": "...",
  "status": "closed"
}
```

The checkpoint is the only event that closes a round and promotes `G_t` plus `D_t` for future use.
At an accepted calibration stop, the final closed `D_t` checksum is additionally named
`D_cal*`. This is frozen human calibration gold, not completed corpus `D*`.

## 9. Test and scorecard records

The sealed manifest stores population, sampling design, seed, protected identifiers, inclusion probabilities, custodian, access log, and invalidation state.
Final human-gold rows use the human schema after `G*` freezes.

Every executor scorecard stores:

- executor, model family, seen or held-out status;
- `G*`, wrapper, decoding, seeds, and run count;
- `T*` manifest and human-gold checksums;
- per-item predictions;
- absolute, class, region, uncertainty, stability, cost, and latency results;
- minimal-instruction baseline and guideline uplift;
- confidence intervals and failure strata.

## 10. Production and provenance

One terminal production row per item:

```json
{
  "item_id": "r999",
  "terminal_disposition": "labeled | unresolved | excluded | invalid",
  "class_label": "low",
  "diagnostic_region": null,
  "provenance_tier": "human_confirmed | audited_machine | machine_accepted | accepted_unresolved | excluded | invalid",
  "policy_version": "G*",
  "executor": {"name": "...", "version": "..."},
  "wrapper_checksum": "sha256:...",
  "route": "single | ensemble | classifier | human",
  "confidence": 0.88,
  "run_id": "production-01",
  "audit_stratum": "...",
  "audit_report": "audit-01"
}
```

Production attempts remain append-only.
One reconciler selects the terminal row and records why retries or alternate routes were rejected.

Completed `D*` is created only after reconciliation and final-audit acceptance. Its
manifest records corpus checksum, terminal-row checksum and count, `G*`, `D_cal*`, `T*`,
selected executor scorecard, production run, audit and repair ids, provenance totals,
limitations, and close timestamp. A pre-audit terminal file must not identify itself as
`D*`.

## 11. Migration rules

Old records are classified as `human_confirmed`, `model_only`, or `unknown` from inspectable evidence.
Only `human_confirmed` rows may enter cumulative gold automatically.
Model-unanimous, panel-majority, and unknown rows remain non-gold evidence until reviewed by the human.
