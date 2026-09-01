# Discovery Lifecycle Map (v3 — Topic Page + Paper Runs)

A Discovery Folder is one durable research Topic with BOTH a Page Face and a
Task Face. It is a sibling of a task-folder, not a flat citation note. This file
is the canonical authority for the lifecycle/type cross; Level-4 mechanics live
only in `paper-run-contract.md`.

## Three independent dimensions

```text
HIERARCHY   Block -> Drop -> Discovery Task Page Folder -> Paper Run
LIFECYCLE   Plan -> Build(optional) -> Execute -> Report
TYPE        Search | Review | Idea
```

Hierarchy says WHERE the unit lives. Lifecycle says WHEN work happens. Type
says WHAT topic-level terminal is produced. Never use phase names as folder
levels or worker calls as Paper Runs.

## Hierarchy

```text
discoveries/                         Block
└── <GROUP>/                         Drop
    └── <NN_topic>/                  Discovery Task Page Folder: one topic
        ├── runs/<RUNNAME>.sh        Paper Run: authored projection
        └── results/<RUNNAME>/       same Paper Run: generated projection
```

One Topic Folder holds MANY numbered Paper Runs. Each Run owns exactly one
canonical paper/source subject and has an exact same-stem Result. Result is not
a fifth hierarchy level. Full contract: `paper-run-contract.md`.

## The two Faces

```text
Page Face                              Task Face
---------                              ---------
<topic>.md                             discovery.yaml
outline/                               scripts/ (optional instrument)
evidence/bibex/<topic>.bib             runs/
topic-level synthesis                  results/
```

The Faces work on the same Topic. The Page synthesizes many Results; the Task
Face plans and executes them. `discovery.yaml` is the Task manifest, not the
whole folder or the only file that matters.

## Lifecycle ownership

| Phase | Meaning | Writes |
|---|---|---|
| **Plan** | declare type, role, topic question, scope, terminal, and candidate selection rule | `discovery.yaml`; Page opening when needed |
| **Build** *(optional)* | author reusable search/extraction/synthesis instruments | `scripts/`; never an empty scaffold |
| **Execute** | resolve triggers; create one `.sh`/Result pair per selected Subject; run paper analyses | `runs/`, `results/`, topic terminal draft |
| **Report** | validate Runs, rebuild aggregate Bib, synthesize outcome/confidence/caveats | `<topic>.md`, type terminal, `evidence/bibex/`, `discovery.yaml report:` |

Low-level calls to arXiv, Crossref, a CLI, an API, or another skill are recorded
inside a Paper Run receipt. They are not Level-4 Runs themselves.

## Types and terminals

The exact type/role table lives in `discovery-yaml-schema.md`.

- **Search** finds candidates and admits selected canonical Subjects as Paper
  Runs. Its topic terminal is a readable source map/index derived from Results.
- **Review** reads completed Paper Results and writes a verdict or landscape.
  Missing evidence creates another Paper Run; it is not pasted into one
  monolithic notes file.
- **Idea** writes ranked ideas or a novelty verdict. Idea generation itself is
  topic-level Page work, not a fake Paper Run. Every paper used for novelty
  evidence still earns its own Paper Run.

The chain remains:

```text
Search Topic Results -> Review Topic synthesis -> Idea Topic synthesis
```

Folders may reference another Topic's terminal from their own side. A
Discovery Folder remains probe-unaware and never tracks its consumers.

## Trigger resolution

```text
URL / DOI / PDF / citation / request
    -> classify Trigger
    -> resolve zero, one, or many canonical Subjects
    -> allocate one Run per Subject
```

The Trigger is provenance. The Subject owns RUNNAME and the authoritative Bib.
An unresolved Trigger writes a truthful `status: unresolved` receipt and never
enters the Page Evidence Bib.

## Agents

- **creator** drafts the topic plan, creates paired Run tickets/receipts,
  executes them, then synthesizes the Page.
- **reviewer** audits search coverage, Run/Result bijection, Subject identity,
  one-entry Bibs, claim anchors, and topic-level scope.

Citation verification is the highest-value Discovery gate. The deterministic
checker and Bib builder run before Report can claim `status: ok`.

## Command routing

```text
/haipipe-discovery                         -> dashboard
/haipipe-discovery open <type> <question> -> scaffold Topic Page Folder
/haipipe-discovery plan <topic>           -> write/update Task manifest
/haipipe-discovery build <topic>          -> author optional instrument
/haipipe-discovery add <topic> <trigger>  -> resolve trigger; scaffold Paper Run(s)
/haipipe-discovery run <topic> [RUNNAME]  -> execute one/all Paper Runs
/haipipe-discovery execute <topic>        -> type-level Execute (includes pending Runs)
/haipipe-discovery report <topic>         -> check, aggregate Bib, synthesize Report
/haipipe-discovery <topic>                -> run full lifecycle
/haipipe-discovery <specialist> [args]    -> one-off worker, no durable folder
```

`add` is intake; `run` is Level-4 execution; `execute` is the Topic lifecycle
phase. These names deliberately separate hierarchy from workflow.
