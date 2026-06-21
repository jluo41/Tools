Folderized discovery.yaml — Legacy / Heavy Schema
=================================================

What this file is
-----------------

This schema is for legacy or opt-in heavy folderized discovery packages only.
The default durable Discovery artifact is now a single markdown file:

```
examples/<PROJECT>/discoveries/<GROUP_slug>/<NN_slug>.md
```

Use folderized mode only when the discovery must keep PDFs, HTML snapshots,
many per-source notes, or other source artifacts. In that case,
`discovery.yaml` records what question was asked of the outside world and where
the durable evidence files live.

Location:

```
examples/<PROJECT>/discoveries/<GROUP_slug>/<NN_slug>/discovery.yaml
```

Legacy flat locations such as `discoveries/D0619_slug/discovery.yaml` are
readable for compatibility, but new durable discovery work should use a
discovery-group plus discovery-folder.

Sibling files:

```
discovery.yaml   source of truth for this discovery package
status.yaml      current snapshot
site.md          human-readable summary
sources.md       citations, URLs, identifiers, verification flags
notes.md         extracted findings and synthesis
verdict.md       concise answer for the parent probe/narrative
```

No local event log belongs here. Orchestration events go to
`_haipipe/project.log.jsonl`.


Top-Level Fields
----------------

| Field          | Type    | Required | Notes |
|----------------|---------|----------|-------|
| kind           | string  | yes      | always `discovery` |
| id             | string  | yes      | e.g. `D001` or `P01.01` |
| group          | mapping | yes      | discovery-group metadata |
| slug           | string  | yes      | discovery-folder slug |
| title          | string  | yes      | human-readable title |
| status         | enum    | yes      | planned/searching/reading/reviewed/ok/inconclusive/blocked |
| parent         | mapping | opt      | narrative/probe/manual consumer |
| role           | enum    | yes      | how the evidence is used |
| question       | string  | yes      | external-world question |
| sources        | mapping | opt      | search scope and selected source refs |
| expected_outputs | list  | yes      | files expected in this folder |
| verdict        | mapping | yes      | pending/supports/contradicts/inconclusive |
| consumed_by    | list    | opt      | project-relative consumers that have used verdict.md |
| created_at     | string  | yes      | quoted ISO8601 creation time |
| updated_at     | string  | yes      | quoted ISO8601 last update time |


Skeleton
--------

```yaml
kind: discovery
id: P01.01
group:
  id: P01
  slug: robustness-claim
  title: Robustness claim evidence
slug: noisy-labels-prior-art
title: Noisy-label robustness prior art
status: planned
created_at: "2026-06-19T10:00:00-04:00"
updated_at: "2026-06-19T10:00:00-04:00"

parent:
  type: probe
  path: probes/0619_robustness_claim
  role: required_evidence
role: prior_art_check

question: |
  Does prior work already show the same noisy-label robustness mechanism
  claimed by this probe?

sources:
  requested:
    - research-lit
    - semantic-scholar
    - exa
  local_first: true
  verification_required: true

expected_outputs:
  - sources.md
  - notes.md
  - verdict.md

verdict:
  status: pending
  summary: ""
  confidence: unknown
  supports_claim: null
  contradicts_claim: null

consumed_by: []
```


Group Values
------------

`group:` records the discovery-group that owns this folder:

```yaml
group:
  id: L01
  slug: initial-landscape
  title: Initial landscape discovery
```

Recommended group id hints:

```
L  landscape / narrative-open discovery
P  probe-backed prior art or counterevidence
B  benchmark landscape
C  counterevidence
S  source reads
```

Group letters are organizational hints. `role:` remains authoritative.


Parent Values
-------------

`parent:` records who is expected to consume this discovery:

```yaml
parent:
  type: paper | application | probe | manual
  path: paper/PaperX/0-lifecycle/2-claims | applications/ask/001_question | probes/P001_claim | ""
  role: required_evidence | optional_context | delivery_steering
```

Delivery-triggered discoveries usually use `landscape_review`,
`novelty_check`, or `benchmark_landscape`. Probe-triggered discoveries usually
use `prior_art_check`, `counterevidence`, `source_read`, or
`benchmark_landscape`.


Status Values
-------------

```
planned        package exists, work not started
searching      finding sources
reading        reading selected sources
reviewed       synthesis complete, verdict not finalized
ok             verdict.md complete and usable by Probe-post
inconclusive   evidence exists but does not settle the question
blocked        missing access, missing sources, or unresolved ambiguity
```

Do not use `consumed` as the main status. A discovery can be reused by multiple
parents. Keep `status: ok` or `inconclusive` and append consumers to
`consumed_by`.


Role Values
-----------

```
prior_art_check       checks whether the claim already exists
landscape_review      maps known approaches, baselines, datasets, metrics
novelty_check         checks whether the angle is new enough
source_read           deep read of one important source
counterevidence       searches for evidence against the claim
benchmark_landscape   identifies standard eval setups
```


Verdict Contract
----------------

`verdict.md` should be short enough for Probe-post to read directly:

```md
# Verdict

status: supports | contradicts | inconclusive
confidence: high | medium | low

## Answer
One paragraph answering the discovery question.

## Evidence
- Full citation / URL / identifier — one-line finding — VERIFIED or NEEDS-VERIFICATION

## Caveats
- What this discovery did not check.
```

The full citation and verification discipline follows the Review Output
Contract in `haipipe-discover/SKILL.md`.


Source Records
--------------

Sources normally live as records in `sources.md`, not as directories:

```md
# Sources

| id | citation / URL | role | verification |
|----|----------------|------|--------------|
| S001 | <full citation or URL> | adjacent method | VERIFIED |
```

Only create `sources/Sxxx_slug/` when the project must keep heavy source
artifacts such as PDFs, HTML snapshots, or per-source annotation files.
