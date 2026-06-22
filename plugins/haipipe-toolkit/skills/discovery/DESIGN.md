discovery — External Evidence Layer (DESIGN)
=============================================

Status: v2.0.0 (2026-06-22) - TWO-AXIS redesign mirroring task. Uniform lifecycle
        Plan -> Build(opt) -> Execute -> Report, crossed with 3 folder types 搜/析/创.
        Skill is haipipe-discovery; discovery = one topic per FOLDER.
Owner:  jluo41
Scope:  external-evidence discovery work and its durable artifact contract inside
        project folders.


Why this layer exists
=====================

`discovery` answers what the outside world already knows. It is not a task
execution stage and it does not judge probe claims by itself.

For a concrete end-to-end project shape, see
`../../blueprints/end-to-end-sandwich-run.md`.

```
discovery   outside-world evidence   sources, notes, verdicts, maps, ideas
task        inside-world execution   code, runs, metrics, reports
probe       claim hub                opens a claim, dispatches discovery + task, closes a verdict
paper/app   delivery (story)         owns the message, lists evidence needs by reference
```


Two Parts
=========

```
1. Skill interface layer
   /haipipe-discovery is the single entry. It runs the durable discovery lifecycle
   (Plan/Build/Execute/Report) and routes to search/read/review/idea bucket workers.

2. Durable artifact layer
   discoveries/<group>/<NN>_<topic>/ stores external evidence when it belongs to a
   project probe or delivery (paper/application) stack.
```

Do not create a new discovery skill family per type. The existing capability
buckets remain the workers; `discoveries/` is just the persistent package they
fill. Workers (4 buckets) and folder types (3) are different axes.


The Two-Axis Model (mirrors task)
=================================

Discovery has the SAME two axes as task: a uniform lifecycle crossed with a
folder type.

```
Axis 1 — LIFECYCLE (uniform; every folder runs it)   Plan -> Build(opt) -> Execute -> Report   (English)
Axis 2 — TYPE      (what kind of folder this is)      搜 · 析 · 创                              (Chinese)

Task = (Plan/Build/Execute/Report) × (data/nn/fit/...)
Discovery = (Plan/Build/Execute/Report) × (搜/析/创)
```

The type axis is named in Chinese single characters and the stage axis in
English so the two can never be confused (the historical mistake was using
search/read/review/idea as BOTH the stages and the types).

One simplification versus task: a task-folder holds MANY runs; a discovery-folder
holds ONE execution per topic — one Plan, one Execute, one Report.

The canonical per-stage / per-type contract lives in ONE place:
`haipipe-discovery/ref/lifecycle-map.md`. Field schema:
`haipipe-discovery/ref/discovery-yaml-schema.md`. Do not restate them here.


Hierarchy
=========

A discovery is one research topic stored as its own folder, the way a task is
one runnable unit stored as its own folder.

```
Task:      tasks/{G}{NN}_group/   ⊃   {NN}_taskname/   -> one runnable unit
Discovery: discoveries/<GROUP>/   ⊃   <NN>_<topic>/    -> one research topic
```

```
discovery-group    A directory grouping related research topics.
discovery-folder   One research topic = one folder. Its IO files (discovery.yaml +
                   sources.md / notes.md / verdict.md|landscape.md|ideas.md +
                   status.yaml / site.md) mirror a task-folder's configs / results /
                   runtime / notebooks.
source row         One paper/webpage/report/dataset citation inside sources.md.
```

Group letters (L/P/B/C/S) are organizational hints only. `type:` and `role:` in
discovery.yaml are authoritative.


The Three Types (Axis 2, IPO: gather -> analyze -> create)
==========================================================

```
字   type      IPO       Execute does                   terminal              consumer
--   -------   -------   ----------------------------   -------------------   ------------------------
搜   source    INPUT     search + read source material  sources.md+notes.md   析 / 创, reusable source base
析   analyze   PROCESS   judge a claim OR map a field   verdict.md / landscape.md   probe (verdict) / paper (landscape)
创   create    OUTPUT    generate candidate claims      ideas.md              probe-open / paper-seed
```

Merge decisions:
- 搜 = search + read merged. They are always bound together (you read what you
  searched), and the digested source set is a reusable, accumulating base — the
  reason task gives `data` its own type instead of folding it into `fit`.
- 析 = judge + synthesize merged. Identical mechanics (read many -> combine ->
  conclude); the only difference is output shape. `role:` picks verdict (判, a
  judgment -> probe) vs landscape (综, a map -> paper). One type, two flavors.
- 创 stays separate: it is divergent (invent new) while 搜/析 are convergent.

```
role -> type -> terminal
搜  source_gather, source_read                       -> sources.md (+ notes.md)
析  prior_art_check, counterevidence, novelty_check    -> verdict.md   (判 -> probe)
析  landscape_review, benchmark_landscape              -> landscape.md (综 -> paper)
创  idea_generation                                    -> ideas.md
```


Skill Structure
===============

```
discovery/
├── CHANGELOG.md               layer-scoped change history
├── haipipe-discovery/          router + durable artifact contract
│   ├── SKILL.md
│   ├── feedback/               skill-feedback inbox (capture, fix later)
│   └── ref/
│       ├── lifecycle-map.md          canonical 2-axis lifecycle + type table
│       └── discovery-yaml-schema.md
├── play/                      plain-language explanation by example
├── 1_search/                  bucket worker: find sources      (used by 搜)
│   ├── arxiv/ semantic-scholar/ exa-search/
├── 2_read/                    bucket worker: read one source   (used by 搜)
│   ├── alphaxiv/ deepxiv/ paper-analyzer/
├── 3_review/                  bucket worker: analyze sources   (used by 析)
│   ├── research-lit/ comm-lit-review/ academic-researcher/
└── 4_idea/                    bucket worker: ideate / validate (used by 创)
    ├── idea-creator/ novelty-check/
```

The 4 buckets are the Execute-stage WORKERS, not folder types: `搜` calls
1_search + 2_read, `析` calls 3_review, `创` calls 4_idea.


Project Folder Contract
=======================

```
examples/<PROJECT>/
├── _haipipe/
│   ├── project.log.jsonl      single append-only orchestration log
│   ├── project.status.yaml
│   └── project.site.md
├── discoveries/
│   ├── L01_initial-landscape/         (parent = paper)
│   │   ├── 01_landscape-review/        (析, landscape_review -> landscape.md)
│   │   └── 02_novelty-check/           (析, novelty_check -> verdict.md)
│   └── P01_rare-phenotype-lift/        (parent = probe)
│       ├── 01_source-base/             (搜 -> sources.md + notes.md)
│       └── 02_prior-art/               (析, prior_art_check -> verdict.md)
├── probes/
├── tasks/
├── insights/
├── paper/
└── applications/
```

The single orchestration log remains `_haipipe/project.log.jsonl`. A
discovery-folder keeps its own `status.yaml` / `site.md` snapshot (like a
task-folder), not an event log.


Discovery Lifecycle (Axis 1)
============================

```
Plan       -> Build (opt)        -> Execute                  -> Report
discovery.yaml  build/ instrument    sources/notes + terminal    report block + status/site
```

`Plan` scaffolds the folder and declares the type; `Build` (optional) authors a
reusable instrument; `Execute` runs the bucket worker for the type and writes the
terminal file; `Report` reports to a human and hands the terminal to the parent.
The canonical per-stage IO lives in `ref/lifecycle-map.md`.

The chain — types compose like task types (`data -> fit -> eval`):

```
搜 folder ─sources/notes→ 析 folder ─landscape.md→ 创 folder
 (reusable source base)    (verdict/landscape)       (ideas)
```

A light effort skips the standalone `搜`: an `析` folder's Execute searches +
reads inline. Build a standalone `搜` when the source base is reused across
several analyses.


How It Combines With Probe
==========================

```
Probe-open
  evidence_plan:
    discoveries:
      - { type: 搜, role: source_gather }      "assemble the source base"
      - { type: 析, role: prior_art_check }    "does this already exist?"  -> verdict.md
    tasks:
      - baseline_eval

Probe-post
  reads discoveries/<group>/<NN>_<topic>/verdict.md   (析, 判)
  reads tasks/<id>/results/*/metrics.json
  writes probe result + claim verdict
```

`probe` references discoveries; it does not own their lifecycle. `discovery`
writes external evidence; it does not close probe claims.

A delivery lifecycle (paper/application) dispatches `析 综` (landscape/benchmark)
and `创` (ideas) during Delivery-open, plus `搜` for a shared source base.


Boundary Rules
==============

- `discoveries/` stores citations, source notes, verdicts, maps, and ideas.
- `discoveries/` does not store code, notebooks, runs, or metrics.
- `tasks/` stores execution artifacts and metrics.
- `probes/` stores claim contracts and verdict sidecars.
- `paper/` and `applications/` own the delivery story and list evidence needs by reference.
- `_haipipe/project.log.jsonl` is the only orchestration event log.
- `sources.md` is the default home for source records; a `sources/` subfolder is
  optional and only for heavy artifacts (PDFs, HTML snapshots).


Decision Log
============

2026-06-19  Adopted: discoveries/ as durable external-evidence packages.
2026-06-20  Adopted: discovery-group/discovery-folder hierarchy.
2026-06-21  Retired: the narrative layer. Parents are now a delivery lifecycle
            (paper/application) for L* and a probe for claim-level evidence.
2026-06-21  A discovery is one research topic = its own FOLDER mirroring a
            task-folder. Skill renamed haipipe-discover -> haipipe-discovery.
2026-06-22  Added: feedback utility verb + feedback/ inbox.
2026-06-22  TWO-AXIS redesign (v2.0.0). The lifecycle is now the uniform task
            lifecycle Plan -> Build(opt) -> Execute -> Report, retiring the
            open/search/read/review/post verb-lifecycle. search/read/review/idea
            are no longer stage verbs; the folder TYPE is one of 3 Chinese-char
            types 搜/析/创. 搜 = search+read merged (reusable source base); 析 =
            judge+synthesize merged (role picks verdict.md vs landscape.md); 创 =
            idea. verdict block renamed to report (report-to-human). The 4
            capability buckets become the Execute-stage workers; per-type
            specialists are NOT created (workers != types). New terminal files
            landscape.md + ideas.md alongside verdict.md. Old folders (role +
            verdict, no type) remain readable; migrate lazily.
