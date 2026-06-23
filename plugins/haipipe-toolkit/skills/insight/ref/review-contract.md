Insight Review Contract
========================

This contract defines how `insights/` is constructed.

The key decision:

```
task / probe / discover produce material.
narrative / application ask / human review decides what is worth archiving.
insight writes curated cards only.
```

`insights/` is the project-level permanent memory. It is not a task log, probe
log, narrative draft, or application session folder.


Roles
=====

```
Layer / actor        Owns                         Does NOT own
───────────────────  ───────────────────────────  ─────────────────────────────
task                 run artifacts, metrics       permanent KB decisions
probe                verdicts, claims, caveats    permanent KB decisions
discover             literature/source findings   permanent KB decisions
narrative            story gaps, ignite choice    raw evidence computation
application ask      question-driven case plan    external artifact finalization
insight review       review file + card filing    original research judgment
```

The word "review" means: inspect finished material, decide which cards are
worth keeping, write `INSIGHT_REVIEW.yaml`, then apply accepted items into
cards, indices, and graph audit.

User-facing vocabulary:

```text
/haipipe-insight review <folder>      inspect material and write INSIGHT_REVIEW.yaml
/haipipe-insight apply <INSIGHT_REVIEW.yaml>    file accepted cards into insights/
```

`INSIGHT_REVIEW.yaml` is the review checklist: candidates to file, skip, merge,
supersede, or block before permanent cards are written.


Canonical Flow
==============

```
1. Material exists
   - task results are complete
   - probe verdict is judged
   - discover/literature source is resolved
   - narrative has claim slots / gaps

2. Review scans material
   - find unarchived candidates
   - deduplicate against existing cards
   - check card granularity: file / merge / split / skip / blocked
   - decide card layer: D / I / K / W
   - write `INSIGHT_REVIEW.yaml`

3. Apply writes the accepted review items
   - call haipipe-insight-data / information / knowledge / wisdom
   - merge/update/supersede existing cards when new evidence touches the same unit
   - run the matching card reviewer
   - rebuild INDEX files
   - run index-integrity audit

4. Callers cite the cards
   - narrative `claims.md` cites K/W ids
   - application reports cite D/I/K/W ids
   - paper uses K/W plus evidence trail
```


When To Review
===============

Use review after a meaningful boundary, not after every tiny edit.

Good review boundaries:

- after `/haipipe-probe post <probe>` has a judged verdict
- after a paper/application lifecycle needs to backfill claim slots from evidence
- during `/haipipe-application ask` Phase 4
- manually, after several completed tasks/probes need archiving

Bad review boundaries:

- before a task has `results/<run>/`
- before a probe has been judged
- while a narrative is still drafting the claim language
- for raw notes, temporary ideas, or one-line observations too small to keep


INSIGHT_REVIEW.yaml Schema
===================

A review run SHOULD create or emit this shape:

```yaml
review_id: R20260620_film_ood
project: examples/ProjA
scope:
  kind: narrative | application_ask | probe | task | project | manual
  ref: narrative:N01 | app:ask:03 | probe:P.0619_film_ood | task:T.A01.02

candidate_cards:
  - candidate_id: C1
    layer: D
    title: "OOD split error by arm"
    sources: [task:T.A01.02]
    reason: "completed task result not yet archived"
    granularity:
      unit: observation
      decision: file
      rationale: "one reusable metric observation, not a raw seed row"
    action: file

  - candidate_id: C2
    layer: K
    title: "FiLM does not transfer to OOD"
    sources: [probe:P.0619_film_ood]
    refs: [D01, I02]
    reason: "judged probe claim not yet in K_knowledge"
    granularity:
      unit: claim
      decision: file
      rationale: "one scoped belief used by the narrative"
    action: file

  - candidate_id: C3
    layer: W
    title: "Stop treating validation gains as OOD evidence"
    sources: [K03]
    reason: "actionable recommendation implied by new K"
    granularity:
      unit: recommendation
      decision: file
      rationale: "one concrete action with a clear trigger"
    action: file

  - candidate_id: C4
    layer: K
    title: "FiLM improves in-distribution forecasting"
    target: K03
    sources: [probe:P.0701_param_matched]
    reason: "new probe supports the same scoped belief; update evidence trail"
    granularity:
      unit: claim
      decision: merge
      rationale: "same reusable claim as K03, not a new belief"
      merge_target: K03
    change:
      kind: evidence_added
      summary: "adds param-matched support; confidence stays medium due OOD caveat"
      append_change_log: true
    action: merge

skip:
  - source: task:T.A01.01
    reason: "already covered by D02"

review:
  required:
    - card-reviewer-data-agent
    - card-reviewer-knowledge-agent
    - index-integrity-auditor-agent
```

`action` values:

```
file       create a new card
merge      add evidence / refs to an existing card instead of creating a card
update     update metadata / ref_by / status only
supersede  mark an old K/W as superseded by a new card
skip       do not archive; explain why
blocked    material is incomplete or ambiguous
```

Card granularity is governed by `ref/card-granularity.md`. The default is:
one card = one reusable knowledge unit. A candidate that is too fine should be
skipped or merged; a candidate that is too broad should be split before apply.

Card lifecycle is governed by `ref/card-lifecycle.md`. A card's id should stay
stable as long as the same reusable unit is being updated. New evidence usually
produces `merge` or `update`; refuted/wrong-scope cards produce `supersede`.


Source References
=================

Use namespaced external refs and bare internal card ids.

External source refs:

```yaml
task:T.A01.02
probe:P.0619_film_ood
lit:smith2024
discover:Dsc.03
narrative:N01.C2
app:ask:03
```

Internal insight refs:

```yaml
D01
I02
K03
W01
```

Examples:

```yaml
# D card from one task result
sources: [task:T.A01.02]
ref_by: [I01]

# I card from two D cards
sources: [D01, D02]
ref_by: [K01]

# K card from a judged probe, with supporting evidence in body
sources: [probe:P.0619_film_ood]
ref_by: [W01, narrative:N01.C2]

# strategic W across multiple K cards
sources: [K01, K03, K05]
ref_by: []
```


Folder Boundary
===============

`insights/` keeps only source-of-truth card files and derived indices:

```text
insights/
├── INDEX.md
├── views/            optional derived navigation views
├── _reviews/         apply-time review records: <LAYER>_CARD_REVIEW.md + INDEX_AUDIT.md
│                     (underscore = not a card layer; provenance of the gate, kept beside the KB)
├── D_data/
├── I_information/
├── K_knowledge/
├── W_wisdom/
└── okf/              optional derived export
```

The `_reviews/` folder holds the per-layer card-review and index-audit artifacts
produced by the reviewers/auditor during `apply`. They are review provenance, not
source-of-truth cards; the underscore keeps them out of the D/I/K/W card space.

Session plans, logs, and gates belong under `applications/ask/<NN_slug>/`.
Paper/application claim ledgers belong inside their delivery lifecycle folders.
Task/probe execution artifacts stay under `tasks/` and `probes/`.


Review Contract
===============

Review is complete only when:

1. Every filed or materially updated card passes its per-layer card reviewer.
2. `insights/INDEX.md` is rebuilt.
3. `K_knowledge/INDEX.md` and `W_wisdom/INDEX.md` are rebuilt if touched.
4. `index-integrity-auditor-agent` passes or records explicit violations.
5. The caller records the new card ids in its own artifact:
   - narrative: `claims.md`
   - application ask: `report.md` and SESSION_STATE
   - paper/application output: citation/reference list

For `merge`, `update`, or `supersede`, the card's `## Change log` must record
the source and reason for the change.


Non-Goals
=========

Review does not:

- run experiments
- compute new metrics
- judge whether a probe claim is true
- decide a narrative is ready to publish
- write external artifacts

Those happen upstream or downstream. Review only archives.
