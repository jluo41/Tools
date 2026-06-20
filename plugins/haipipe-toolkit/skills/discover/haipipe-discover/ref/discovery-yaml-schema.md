discovery.yaml — Schema
=======================

What this file is
-----------------

`discovery.yaml` is the state of one durable external-evidence package. It is
not a task, not a run, and not a probe verdict. It records what question was
asked of the outside world and where the durable evidence files live.

Location:

```
examples/<PROJECT>/discoveries/<DMMDD_slug>/discovery.yaml
```

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
| id             | string  | yes      | e.g. `D0619` |
| slug           | string  | yes      | folder slug |
| title          | string  | yes      | human-readable title |
| status         | enum    | yes      | planned/searching/reading/reviewed/ok/inconclusive/blocked |
| root           | string  | opt      | narrative path if known |
| parent_probe   | string  | opt      | probe path if probe-backed |
| role           | enum    | yes      | how the evidence is used |
| question       | string  | yes      | external-world question |
| sources        | mapping | opt      | search scope and selected source refs |
| expected_outputs | list  | yes      | files expected in this folder |
| verdict        | mapping | yes      | pending/supports/contradicts/inconclusive |
| created_at     | ISO8601 | yes      | creation time |
| updated_at     | ISO8601 | yes      | last update time |


Skeleton
--------

```yaml
kind: discovery
id: D0619
slug: noisy-labels-prior-art
title: Noisy-label robustness prior art
status: planned
created_at: 2026-06-19T10:00:00-04:00
updated_at: 2026-06-19T10:00:00-04:00

root: narratives/01_robustness_story
parent_probe: probes/0619_robustness_claim
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
```


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
