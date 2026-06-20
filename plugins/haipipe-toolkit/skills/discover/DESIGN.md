discover — External Evidence Layer (DESIGN)
=============================================

Status: v1.3.0 (2026-06-19) — discovery skills stay as capability routers;
        durable project evidence lives in `discoveries/`.
Owner:  jluo41
Scope:  search/read/review/idea discovery work and its durable artifact
        contract inside project folders.


Why this layer exists
=====================

`discover` answers what the outside world already knows. It is not a
task execution stage and it does not judge probe claims by itself.

For a concrete end-to-end project shape, see
`../../blueprints/end-to-end-sandwich-run.md`.

```
discover    outside-world evidence   sources, notes, prior art, novelty
task        inside-world execution   code, runs, metrics, audits
probe       claim judgment           combines discovery + task evidence
narrative   story judgment           decides which probe verdicts fill gaps
```


Two Parts
=========

`discover` has two separate responsibilities:

```
1. Skill capability layer
   /haipipe-discover routes to search/read/review/idea specialists.

2. Durable artifact layer
   discoveries/<id>/ stores external evidence when it belongs to a project
   narrative/probe stack.
```

Do not create a new discovery skill family for project artifacts. The existing
specialists remain the workers; `discoveries/` is just the persistent evidence
package they can write.


Skill Structure
===============

```
discover/
├── haipipe-discover/          router + durable artifact contract
│   ├── SKILL.md
│   └── ref/
│       └── discovery-yaml-schema.md
├── 1_search/                  find sources
│   ├── arxiv/
│   ├── semantic-scholar/
│   └── exa-search/
├── 2_read/                    read one source
│   ├── alphaxiv/
│   ├── deepxiv/
│   └── paper-analyzer/
├── 3_review/                  synthesize many sources
│   ├── research-lit/
│   ├── comm-lit-review/
│   └── academic-researcher/
└── 4_idea/                    generate/check ideas
    ├── idea-creator/
    └── novelty-check/
```


Project Folder Contract
=======================

When discovery output should be tracked by a project, write a durable package:

```
examples/<PROJECT>/
├── _haipipe/
│   ├── project.log.jsonl      single append-only orchestration log
│   ├── project.status.yaml
│   └── project.site.md
├── discoveries/
│   ├── D0619_noisy-labels-prior-art/
│   │   ├── discovery.yaml
│   │   ├── status.yaml
│   │   ├── site.md
│   │   ├── sources.md
│   │   ├── notes.md
│   │   └── verdict.md
│   └── 2026-archive/
├── probes/
├── tasks/
└── narratives/
```

The single orchestration log remains `_haipipe/project.log.jsonl`. Discovery
folders do not keep local event logs.


How It Combines With Probe
==========================

Probe-open may dispatch either or both evidence types:

```
Probe-open
  evidence_plan:
    discoveries:
      - prior_art_check
      - novelty_check
    tasks:
      - baseline_eval
      - treatment_eval

discover
  writes discoveries/<id>/

task
  writes tasks/<id>/

Probe-post
  reads discoveries/<id>/verdict.md
  reads tasks/<id>/results/*/metrics.json
  writes probe result + claim verdict
```

`probe` references discoveries; it does not own their search/read/review
process. `discover` writes external evidence; it does not close probe claims.


Discovery Types
===============

Use `role:` in `discovery.yaml` to identify how the output should be consumed:

```
prior_art_check       Does this already exist?
landscape_review      What are the known approaches and baselines?
novelty_check         Is the proposed angle new enough?
source_read           What does one key paper/source actually say?
counterevidence       What evidence argues against the claim?
benchmark_landscape   What datasets/metrics/baselines are standard?
```


Boundary Rules
==============

- `discoveries/` stores citations, source notes, synthesis, and verdicts.
- `discoveries/` does not store code, notebooks, runs, or metrics.
- `tasks/` stores execution artifacts and metrics.
- `probes/` stores claim contracts and verdict sidecars.
- `narratives/` stores story contracts and claim ledgers.
- `_haipipe/project.log.jsonl` is the only orchestration event log.


Decision Log
============

2026-06-19  Adopted: discoveries/ as durable external-evidence packages.
            Existing discover specialists remain the capability layer.
            probe can reference discoveries and tasks as sibling evidence
            work before Probe-post judges the claim.
