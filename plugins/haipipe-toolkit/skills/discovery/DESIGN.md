# Discovery — architecture

Discovery is the durable external-evidence executor. Its article unit is a
`tNN_` Task Page with a Page Face and a Task Face, addressed inside BJTR.

Runtime authority lives in:

~~~text
haipipe-discovery/SKILL.md
haipipe-discovery/ref/lifecycle-map.md
haipipe-discovery/ref/paper-run-contract.md
haipipe-discovery/ref/discovery-yaml-schema.md
haipipe-discovery/ref/bjtr-alignment.md
haipipe-discovery/ref/external-capability-registry.md
~~~

This file explains their relationship; when details differ, those runtime refs
win.

## Numbered skill-family groups

Discovery keeps the same family-level organization used by `haipipe-task`:

~~~text
discovery/
├── haipipe-discovery/                         public door
├── workflow-phases/
│   └── haipipe-discovery-inquiry/             sole D1 phase
├── 1_search/                                  acquisition family
│   ├── haipipe-discovery-search/              family router
│   └── source FIND/READ workers
│       (arxiv, semantic-scholar, exa-search, openalex, gemini-search,
│        alphaxiv, deepxiv, paper-analyzer)
├── 2_review/                                  per-Subject review family
│   ├── haipipe-discovery-review/              family router
│   └── review workers
├── 3_synthesize/                              cross-Result synthesis family
│   └── haipipe-discovery-synthesize/          family router
└── agents/                                    execution roles
~~~

Semantic ideation is a sibling layer, not a Discovery capability family:

~~~text
ideation/haipipe-ideation
  Task Run/Result + Discovery Result/Bib pointers
  -> evidence bundle -> Direction/Idea Cards -> Paper P0 handoff
~~~

The numeric prefixes order and group the skill bank, like `task/1_data`,
`task/2_nn`, and `task/3_end`. They are not executable phase numbers and must
not be renamed to a parallel `routes/` hierarchy. Runtime phase ownership is
declared only under `workflow-phases/`; for Discovery that owner is D1 Inquiry.

The retrofit rule is recorded in `haipipe-discovery/ref/bjtr-alignment.md`:
project work is addressed only as Block -> Job -> Task Page -> Run, while
numbered skill families, D1 cycles, and Page 00-04 remain orthogonal views.
The former Idea family is deleted; it is not a route, migration target, or
compatibility surface.

## Four levels

~~~text
bank        discoveries/
L1 Block    bNN_<noun>_<qualifier>/
L2 Job      jNN_<noun>_<qualifier>/
L3 TaskPage tNN_<noun>_<qualifier>/
L4 Run      runs/rNN_<author><year>_<paper>.sh <-> results/rNN_.../
~~~

L1 is a broad evidence domain; L2 is a self-contained inquiry/campaign; L3 owns
one article question and `discovery_type`; L4 owns one canonical evidence Subject, normally
one paper. Result is the generated projection of Run, not an additional level.

All four levels use `<level-letter><NN>_<noun>_<qualifier>`. Their joined
address is `bNNjNNtNNrNN`; `discoveries/` is a bank and contributes no segment.

## Two Faces

~~~text
Page Face                              Task Face
tNN_<task>.md                         discovery.yaml
outline/                               scripts/ optional
outline/evidence/bibex/tNN_<task>.bib  runs/
(CITE lane owned by Outline)           results/
topic-level synthesis                  runtime receipts
~~~

Configuration is not a Folder kind. Each workflow phase configures the Face it
owns. The manifest plans the Topic; a .sh ticket plans one Paper Run.

## Three orthogonal dimensions

~~~text
Hierarchy   Block -> Job -> Task Page -> Run
Domain      D1 SCOPE -> PREPARE? -> ACQUIRE <-> SYNTHESIZE -> CLOSE
Page        shared 00 CONTEXT -> 01 OUTLINE -> 02 EVIDENCE ->
            03 CONTENT -> 04 CHECK
Page Type   source-map | source-reading | topic-summary | prior-art-verdict |
            counterevidence-review | landscape-review | benchmark-landscape
~~~

The Page Type says what article the root Page is writing. It does not add a
folder level and it does not define a Run. Search, Review, and Synthesize are
the live Discovery specialist routes: Search resolves evidence Subjects,
Review inspects one source/Result at a time, and Synthesize combines accepted
Results into the root article. Semantic ideation consumes Discovery and Task
evidence in `haipipe-ideation` after this workflow; it is not a Discovery
family. Worker/API/CLI calls are runtime detail inside a Run receipt.

## External capability boundary

Reference repositories contribute narrow provider, extraction, lineage, and
verification procedures through
`haipipe-discovery/ref/external-capability-registry.md`. Their outputs are
normalized into Search, Review, or Synthesis packets. They cannot commission a
Run, own a Result Card, write a one-entry Bib, or bypass the shared Page and
Outline gates. This keeps external SaaS-style modules useful without creating
a second Folder model.

## D1 domain-cycle × Run map

~~~text
SCOPE       no Run; writes manifest intent
PREPARE     no Run; scripts/ are supporting instruments
ACQUIRE     paper-analysis | source-analysis × N admitted Subjects
SYNTHESIZE  no Discovery Run; dispatches shared Page workflow
CLOSE       no Run; reconciles the already-CHECKed Page and Task Face

Total R = N admitted canonical Subjects
~~~

Search queries, candidate rows, synthesis passes, and direction generation are not
Runs. A Run begins only after one canonical evidence Subject is admitted.

The canonical table, Runs Overview, Human Actions, and Skill Coverage live at
`workflow-phases/haipipe-discovery-inquiry/ref/workflow-table.md`. There is no
separate Discovery workflow skill; D1 owns the domain workflow and the shared
Page workflow owns Page artifacts. The D1 root uses the permitted no-Run route;
consumer Pages own any Page-family Runs they commission.

The pinned upstream source and compatibility decisions for external workers
live in `haipipe-discovery/ref/external-skill-map.md`. External workers are
read-only scouts; they never bypass the local Subject, Run/Result, or Bib gates.

## Trigger and Subject

~~~text
Trigger -> resolve -> canonical Subject -> numbered Run -> same-stem Result
~~~

A Trigger may be a paper URL, short link, social post, DOI, PDF, citation, or
request. It explains why work started. The canonical Subject owns RUNNAME and
the Bib entry. One Trigger may fan out to many Subjects; one Run never bundles
multiple papers.

## Evidence authority

Each complete Result owns:

~~~text
<RUNNAME>.md
facts.md
runtime.yaml
<RUNNAME>.bib   exactly one authoritative entry
~~~

PDF, raw extraction, and captured Trigger are optional. Result Card cite key
and Bib key are identical. `haipipe-plugin-outline/ref/evidence/citations.md`
owns the deterministic derived union of complete Result Bibs; conflicts
hard-fail. The nested `outline/evidence/supporting-runs/` lane is pointer-only
lineage for Page Evidence Items, not a second Discovery Run inventory.

## Synthesis

Topic Content and Paper Results are many-to-many. A paper may support several
divisions, and a division normally synthesizes several papers. The root Page
is always the human-facing article. Optional `summary.md`, `verdict.md`, and
`landscape.md` are typed Task-side synthesis records, not rival Pages or Runs.
The Page links to Results; it does not copy their entire readouts into a flat
notes ledger.

## Migration boundary

Existing sources.md and notes.md remain readable as migration inputs. They are
not the authority for new evidence. Old prose is not mass-converted: a paper
earns a Result only when canonical identity and authoritative BibTeX can be
verified. An old Idea Page or 3_idea path is rejected rather than redirected;
start a new synthesis Page or use the separate haipipe-ideation skill.
