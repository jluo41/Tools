# Reference: Label Handoff contract

The Label Handoff is the only authority crossing from Label Building to
Label Scanning. It packages an already-frozen human construct; it does not
create, interpret, or improve that construct.

## Canonical location

```text
{project_dir}/handoff/label-v1.yaml
```

The file is immutable after close. Its version is its name and date: for
example `label-v1` and its `created_at` date. A semantic change creates a new
lineage and new handoff rather than rewriting this file. Historical handoffs
remain read-only evidence for the runs that consumed them.

## Required fields

```yaml
schema: subjective-label-handoff/v1
job_id: <one corpus snapshot x one target>
lineage: <policy lineage id>
version: label-v1
created_at: <timestamp>

corpus:
  manifest: <path>
  n_items: <eligible item count>
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
  version: <closed policy version, e.g. G_07>
  manifest: <path>

calibration_gold:
  id: D_cal*
  version: <closed gold version, e.g. D_07>
  manifest: <path>
  n_records: <human-confirmed record count>

sealed_test:
  manifest: <protected-manifest reference>
  n_items: <sealed item count>
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
  inputs: [{path: <path>}]
  previous_receipt: <path or null>

status: valid
invalidated_by: null
```

## Creation gate

The Building side creates the handoff at P2 Freeze, through the Label Handoff
Keeper, only when:

- every cited calibration checkpoint is closed and comparable;
- the configured stopping conjunction passes for the required streak;
- `G*` and `D_cal*` are closed versions whose files exist and parse, with
  counts that match their manifests;
- the Test Custodian confirms protected identifiers and text remained outside
  calibration;
- the human signature names the exact policy, gold, corpus, and lineage.

The handoff carries the protected manifest reference and its sealed item
count, never protected ids or test text.

## Consumption gate

Before any protected release or executor run, the Scanning door:

1. checks every bound artifact: it exists, parses, and matches its count;
2. verifies `status: valid` and no invalidation descendant;
3. freezes its own registry or production manifest against the handoff version;
4. records the access in the Test Custodian or production receipt.

Scanning may not follow `policy/current`; it follows the exact handoff version.

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
