discover — External Evidence Layer (DESIGN)
=============================================

Status: v1.5.0 (2026-06-20) — single discover entry; durable project
        evidence defaults to one markdown file per discovery.
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
1. Skill interface layer
   /haipipe-discover is the single entry. It runs durable discovery lifecycle
   verbs and routes to search/read/review/idea specialists.

2. Durable artifact layer
   discoveries/<group>/<NN_slug>.md stores external evidence when it belongs
   to a project narrative/probe stack.
```

Do not create a new discovery skill family for project artifacts. The existing
specialists remain the workers; `discoveries/` is just the persistent evidence
package they can write.


Hierarchy
=========

Discover mirrors task's clean grouping, but does not copy task's heavy folder
surface:

```
Task:     task-group      -> task-folder      -> run
Discover: discovery-group -> discovery.md     -> source row
```

Definitions:

```
discovery-group   A directory grouping related outside-evidence questions.
discovery.md      One durable external-world question, stored as one file.
source row        One paper/webpage/report/dataset citation in the Sources
                  section.
```

Folderized heavy mode is opt-in only, for cases with PDFs, HTML snapshots,
annotations, or many per-source extracted notes.

Recommended group hints:

```
L  landscape / narrative-open discovery
P  probe-backed prior art or counterevidence
B  benchmark landscape
C  counterevidence
S  source reads
```

Group letters are organizational hints only. The authoritative type is
`role:` in the discovery markdown frontmatter.


Skill Structure
===============

```
discover/
├── haipipe-discover/          router + durable artifact contract
│   ├── SKILL.md
│   └── ref/
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
│   │   ├── 01_landscape-review.md
│   │   └── 02_novelty-check.md
│   └── P01_rare-phenotype-lift/
│       ├── 01_prior-art.md
│       └── 02_benchmark-landscape.md
├── probes/
├── tasks/
└── narratives/
```

The single orchestration log remains `_haipipe/project.log.jsonl`. Discovery
folders do not keep local event logs.

Folderized legacy packages such as `discoveries/D0619_noisy-labels-prior-art/`
remain readable, but new durable work should default to the group/markdown
hierarchy.


Discovery Lifecycle
===================

Every discovery markdown answers one external-world question:

```
Open     create <NN_slug>.md with frontmatter and empty sections
Search   fill ## Sources with candidate sources + verification state
Read     fill ## Notes with extracted source facts
Review   synthesize notes into claim-relevant findings
Verdict  finalize ## Verdict (ok/inconclusive/blocked)
Post     update parent refs/status and _haipipe/project.log.jsonl
```

File ownership:

```
Open      <NN_slug>.md frontmatter + headings
Search    ## Sources
Read      ## Notes
Review    ## Notes / ## Verdict draft
Verdict   frontmatter status/verdict + ## Verdict
Post      parent refs, project.status.yaml, project.log.jsonl
```

`post` does not judge the research claim. It only makes the discovery verdict
available to its parent narrative or probe.


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
  writes discoveries/<group>/<NN_slug>.md

task
  writes tasks/<id>/

Probe-post
  reads the Verdict section in discoveries/<group>/<NN_slug>.md
  reads tasks/<id>/results/*/metrics.json
  writes probe result + claim verdict
```

`probe` references discoveries; it does not own their search/read/review
process. `discover` writes external evidence; it does not close probe claims.

Narrative may also dispatch discoveries during Narrative-open:

```
Narrative-open
  dispatches L* discovery-groups for landscape and novelty
  writes story.md / claims.md from the discovery verdicts

Probe-open
  dispatches P*/B*/C*/S* discovery-groups for claim-level evidence
  waits for the discovery Verdict section before Probe-post if required
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
- `narratives/` stores story contracts and claim ledgers.
- `_haipipe/project.log.jsonl` is the only orchestration event log.
- `## Sources` in the discovery markdown is the default home for source records.
  Source folders are optional and only for heavy artifacts.


Decision Log
============

2026-06-19  Adopted: discoveries/ as durable external-evidence packages.
            Existing discover specialists remain the capability layer.
            probe can reference discoveries and tasks as sibling evidence
            work before Probe-post judges the claim.
2026-06-20  Adopted: discovery-group/discovery-folder hierarchy. `source` is
            not a mandatory folder; it is usually a record in sources.md.
            `/haipipe-discover` is the single entry for lifecycle + routing.
2026-06-20  Revised: default durable artifact is now one markdown file:
            `discoveries/<group>/<NN_slug>.md`. Folderized packages are legacy
            compatible or opt-in heavy mode only.
