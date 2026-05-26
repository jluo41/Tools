Data contract schema — data/contract.yaml
==========================================

The project's hand-written declaration of what data it needs to
operate. Lives at `<PROJECT_ROOT>/data/contract.yaml`. Read at the
start of every ask session; never modified by the orchestrator.

Two generated companions sit next to it (never hand-edited):

```
data/available.md   what the active subject store has at the active cut
data/gaps.md        what's missing + which analyses block (required)
                                       or trim (optional)
```

Both regenerated at Phase 1 step A1 of every ask session.


Why a contract layer?
======================

The project (analytical hub) is reusable across subjects. The
contract declares the project's data requirements once; each subject
store carries the actual data plus a manifest declaring which streams
and cuts exist for THAT subject. The orchestrator diffs the two at
session init.

Without a contract, every ask session re-invents ad-hoc stream
checks (see ask SKILL.md history of bug #11 / #17 patches in
Phase 1 step B). The contract collapses those into one resolution
pass with a single source of truth.


Schema
=======

```yaml
project: Subject*-Profile           # project name pattern (informational)
schema_version: 1

# Streams the project REQUIRES to run at all.
# Missing required stream  -> ask session HARD BLOCKs at Phase 1 step A1.
required:
  - stream: cgm
    min_window_days: 30             # subject must cover >= this span
    min_density_per_day: 200        # readings/day floor
    notes: "5-min CGM, expected 288/day; floor 200 tolerates sensor gaps"

# Streams the project CAN USE if available.
# Missing optional stream  -> matching task_batch entries are trimmed.
optional:
  - stream: diet
    enables: [meal-response-analysis, postprandial-cv]
  - stream: medication
    enables: [med-response-analysis]
  - stream: activity
    enables: [activity-response, daily-context-rhythm]

# How this project treats new data cuts on the subject side.
# See subject-side manifest.yaml `cuts:` for the producer side.
# Cadence (monthly, quarterly, event-driven, ...) is the subject's
# concern, NOT the project's; this field declares DISCIPLINE only.
cut_discipline: latest              # snapshot | latest | pinned
pinned_cut: null                    # required iff cut_discipline=pinned
                                    # opaque tag, e.g. "v2026-04", "release-3"
```


Generated companions
======================

`data/available.md` (regenerated each session):

```
Active subject: Subject-26
Active cut:     2026-05  (through 2026-05-31)

Required:
  cgm           present   61,283 rows, 344 days, density 178/day
                          (below 200/day floor -- see gaps.md)

Optional:
  diet          absent
  medication    absent
  activity      absent
```

`data/gaps.md` (regenerated each session):

```
Required gaps (BLOCK):
  cgm density 178/day < required 200/day
    -> session BLOCKED until contract relaxed OR denser subject picked

Optional gaps (TRIM):
  diet absent       -> trim: meal-response-analysis, postprandial-cv
  medication absent -> trim: med-response-analysis
  activity absent   -> trim: activity-response, daily-context-rhythm
```


Resolution rules (ask Phase 1 step A1)
=======================================

```
1. Read <PROJECT_ROOT>/data/contract.yaml
   - Missing       -> scaffold a default contract from a kind-specific
                      template (ask default: cgm required; rest optional);
                      surface a one-line notice to the user
   - Schema-invalid -> HARD BLOCK and surface to user

2. Read <subject_store>/manifest.yaml
   - cuts[]   -> pick active cut per the contract's cut_discipline:
                   latest    -> last entry in cuts[]
                   pinned    -> the contract's pinned_cut tag
                   snapshot  -> the cut recorded in the project's first
                                session (frozen for the project's life)
                 `--cut <tag>` on the ask command overrides all three
                 for the current session only (SESSION_STATE.notes
                 records the override)
   - streams: -> presence map for the chosen cut

3. Diff required vs available
   - Any required stream missing OR below floor -> HARD BLOCK
   - Write data/available.md + data/gaps.md (atomic; .tmp + mv)
   - Pin SESSION_STATE.data_cut       = <active cut tag>
   - Pin SESSION_STATE.contract_path  = data/contract.yaml

4. For each optional stream that is absent: trim plan.task_batch
   entries whose `enables` tag matches the missing stream.
   Record trimmed task ids in SESSION_STATE.trimmed_by_contract[].
```


Per-subject overrides
======================

A subject can override the project contract by writing:

```
<PROJECT_ROOT>/data/contract.local.yaml
```

Only thresholds (`min_window_days`, `min_density_per_day`) may be
relaxed locally. The required stream list cannot be subtracted.
The local file is merged into the effective contract at step A1;
its presence is noted in `data/available.md`.


Cross-references
=================

```
<subject_store>/manifest.yaml                producer side: streams + cuts
haipipe-application/SKILL.md                 "Data contract layer"
haipipe-application-ask/SKILL.md             Phase 1 step A1
haipipe-application/ref/session-state-schema.md
                                             SESSION_STATE.data_cut,
                                             SESSION_STATE.contract_path
```
