discovery — External Evidence Layer (DESIGN)
=============================================

Status: v1.7.0 (2026-06-21) - discovery = one research topic per FOLDER (mirrors
        task-folder); IO files sources/notes/verdict; narrative parent retired.
Owner:  jluo41
Scope:  search/read/review/idea discovery work and its durable artifact
        contract inside project folders.


Why this layer exists
=====================

`discovery` answers what the outside world already knows. It is not a
task execution stage and it does not judge probe claims by itself.

For a concrete end-to-end project shape, see
`../../blueprints/end-to-end-sandwich-run.md`.

```
discovery   outside-world evidence   sources, notes, prior art, novelty, verdicts
task        inside-world execution   code, runs, metrics, reports
probe       claim hub                opens a claim, dispatches discovery + task, closes a verdict
paper/app   delivery (story)         owns the message, lists evidence needs by reference
```


Two Parts
=========

`discovery` has two separate responsibilities:

```
1. Skill interface layer
   /haipipe-discover is the single entry. It runs durable discovery lifecycle
   verbs and routes to search/read/review/idea specialists.

2. Durable artifact layer
   discoveries/<group>/<NN>_<topic>/ stores external evidence when it belongs
   to a project probe or delivery (paper/application) stack.
```

Do not create a new discovery skill family for project artifacts. The existing
specialists remain the workers; `discoveries/` is just the persistent evidence
package they can write.


Hierarchy
=========

Discovery mirrors task: a discovery is one research topic stored as its own
folder, the way a task is one runnable unit stored as its own folder.

```
Task:      tasks/{G}{NN}_group/   -> {NN}_taskname/   -> one runnable unit
Discovery: discoveries/<GROUP>/   -> <NN>_<topic>/    -> one research topic
```

Definitions:

```
discovery-group    A directory grouping related research topics.
discovery-folder   One research topic = one folder. Its IO files (discovery.yaml
                   + sources.md / notes.md / verdict.md + status.yaml / site.md)
                   mirror a task-folder's configs / results / runtime / notebooks.
source row         One paper/webpage/report/dataset citation inside sources.md.
```

Heavy source artifacts (PDFs, HTML snapshots, per-source annotations) go in an
optional sources/ subfolder inside the discovery-folder.

Recommended group hints:

```
L  landscape / delivery-open discovery
P  probe-backed prior art or counterevidence
B  benchmark landscape
C  counterevidence
S  source reads
```

Group letters are organizational hints only. The authoritative type is
`role:` in discovery.yaml.


Skill Structure
===============

```
discovery/
├── CHANGELOG.md               layer-scoped change history
├── haipipe-discover/          router + durable artifact contract
│   ├── SKILL.md
│   └── ref/
│       ├── lifecycle-map.md          canonical verb lifecycle table
│       └── discovery-yaml-schema.md
├── play/                      plain-language explanation by example
│   └── README.md
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
│   ├── L01_initial-landscape/
│   │   ├── 01_landscape-review/
│   │   └── 02_novelty-check/
│   └── P01_rare-phenotype-lift/
│       ├── 01_prior-art/
│       └── 02_benchmark-landscape/
├── probes/
├── tasks/
├── insights/
├── paper/
└── applications/
```

The single orchestration log remains `_haipipe/project.log.jsonl`. A
discovery-folder keeps its own `status.yaml` / `site.md` snapshot (like a
task-folder), not an event log.


Discovery Lifecycle
===================

A discovery-folder's IO files are filled by the lifecycle, the way a
task-folder's results are filled by its runs:

```
open    ->  search    ->  read     ->  review (or idea)  ->  post
discovery.yaml  sources.md   notes.md     verdict.md          parent link
```

The canonical per-stage contract (skill, files_in, files_out) lives in ONE
place: `haipipe-discover/ref/lifecycle-map.md`. Do not restate it here. `open`
scaffolds the folder, the work stages fill its IO files, and `post` makes the
verdict available to the parent delivery lifecycle (paper/application) or probe
without judging the claim.


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

discovery
  writes discoveries/<group>/<NN>_<topic>/ (sources.md, notes.md, verdict.md)

task
  writes tasks/<id>/

Probe-post
  reads discoveries/<group>/<NN>_<topic>/verdict.md
  reads tasks/<id>/results/*/metrics.json
  writes probe result + claim verdict
```

`probe` references discoveries; it does not own their search/read/review
process. `discovery` writes external evidence; it does not close probe claims.

A delivery lifecycle may also dispatch discoveries during Delivery-open:

```
Delivery-open (paper / application)
  dispatches L* discovery-groups for landscape and novelty
  writes the deliverable's story/claims from the discovery verdicts

Probe-open
  dispatches P*/B*/C*/S* discovery-groups for claim-level evidence
  waits for the discovery's verdict.md before Probe-post if required
```


Discovery Types
===============

Use `role:` in discovery frontmatter to identify how the output should be
consumed:

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
- `paper/` and `applications/` own the delivery story and list evidence needs by reference.
- `_haipipe/project.log.jsonl` is the only orchestration event log.
- `sources.md` in the discovery-folder is the default home for source records.
  A `sources/` subfolder is optional and only for heavy artifacts.


Decision Log
============

2026-06-19  Adopted: discoveries/ as durable external-evidence packages.
            Existing discovery specialists remain the capability layer.
            probe can reference discoveries and tasks as sibling evidence
            work before Probe-post judges the claim.
2026-06-20  Adopted: discovery-group/discovery-folder hierarchy. `source` is
            not a mandatory folder; it is usually a record in sources.md.
            `/haipipe-discover` is the single entry for lifecycle + routing.
2026-06-20  Revised: default durable artifact is now one markdown file:
            `discoveries/<group>/<NN_slug>.md`. Folderized packages are legacy
            compatible or opt-in heavy mode only.
2026-06-21  Retired: the narrative layer. A discovery now has two parents only:
            a delivery lifecycle (paper/application) for L* landscape/novelty,
            and a probe for claim-level evidence. Story-side dispatch moved from
            Narrative-open to Delivery-open.
2026-06-21  Added: ref/lifecycle-map.md as the canonical verb lifecycle table
            (Status/Open/Search/Read/Review/Verdict/Post). SKILL.md and this
            file now point to it instead of restating the per-verb columns.
2026-06-21  Renamed: folder discover/ -> discovery/ so the layer concept reads
            as a noun, matching discoveries/ and the task/probe/insight siblings.
            Skill name: stays haipipe-discover.
2026-06-21  Reverted the v1.5 single-file default. A discovery is one research
            topic = its own FOLDER (discovery.yaml + sources.md/notes.md/verdict.md
            + status.yaml/site.md), mirroring a task-folder; sources/notes/verdict
            are its results. The dry-run fixture and blueprint already used folders;
            the single-file default never landed. lifecycle-map.md recast as
            open -> search -> read -> review/idea -> post, each stage filling one
            IO file.
