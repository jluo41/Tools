# Reference: Label Handoff contract

The Label Handoff is the only authority crossing from Label Building to
Label Scanning. It packages an already-frozen human construct; it does not
create, interpret, or improve that construct.

## Canonical location

```text
{project_dir}/handoff/label-v1.yaml
```

The file is immutable after close. A semantic change creates a new lineage and
new handoff rather than rewriting this file. Historical handoffs remain
read-only evidence for the runs that consumed them.

## Required fields

```yaml
schema: subjective-label-handoff/v1
job_id: <one corpus snapshot x one target>
lineage: <policy lineage id>
created_at: <timestamp>

corpus:
  manifest: <path>
  checksum: <sha256>
  target_population: <declared population>

semantic_authority:
  id: <identified human>
  freeze_signature: <inspectable signed record>

schema_contract:
  labels: [high, low, none]
  regions: [H, L, N, HL, LN, HN, HLN]
  uncertainty_separate: true
  unresolved_is_not_none: true

policy:
  id: G*
  manifest: <path>
  checksum: <sha256>

calibration_gold:
  id: D_cal*
  manifest: <path>
  checksum: <sha256>

sealed_test:
  manifest: <protected-manifest reference>
  manifest_checksum: <sha256>
  custody_status: reserved-and-unexposed
  protected_ids_in_handoff: false

stopping:
  checkpoints: [<comparable checkpoint ids>]
  quality: pass
  stability: pass
  coverage: pass
  risk: pass
  human_signoff: pass

receipt:
  inputs: {<path>: <sha256>}
  output_checksum: <sha256 excluding this field>
  previous_receipt: <sha256 or null>

status: valid
invalidated_by: null
```

## Creation gate

The Building door may create the handoff, as its P2 Freeze phase, only when:

- every cited calibration checkpoint is closed and comparable;
- the configured stopping conjunction passes for the required streak;
- `G*` and `D_cal*` are immutable and rehash cleanly;
- the Test Custodian confirms protected identifiers and text remained outside
  calibration;
- the human signature names the exact policy, gold, corpus, and lineage.

The handoff carries the protected manifest checksum, never protected ids or
test text.

## Consumption gate

Before any protected release or executor run, the Scanning door:

1. rehashes every bound artifact;
2. verifies `status: valid` and no invalidation descendant;
3. freezes its own registry or production manifest against the handoff checksum;
4. records the access in the Test Custodian or production receipt.

Scanning may not follow `policy/current`; it follows the exact handoff checksum.

## Invalidation

Any semantic, wrapper, threshold, executor-selection, routing, or test-access
change invalidates the claims whose frozen system it changes. Preserve the old
handoff and append an invalidation receipt naming:

- changed component and reason;
- affected scorecards, production runs, audits, and claims;
- whether the consumed test became development evidence;
- required new lineage, handoff, test, scorecard, scan, or audit.

An editorial-only policy change may remain in lineage only when a deterministic
diff proves no executor-visible or human-visible instruction changed.

## Forbidden crossings

- policy drafts or open-round output presented as `G*`;
- model consensus presented as human gold;
- protected ids or text copied into the handoff;
- Scanning editing Building artifacts;
- Building writing scorecards or production claims;
- a handoff regenerated in place after downstream use;
- a completed-corpus claim without the bound final audit receipt.
