---
name: haipipe-discovery
description: >-
  External-evidence executor built as Discovery Page Folders. One folder owns
  one typed BJTR Task Page and many numbered Paper Runs; every durable paper or
  source is analyzed through a numbered shell ticket and its exact same-stem
  Result directory containing a Result Card, facts, runtime receipt, and
  one-entry BibTeX. Use to add a paper/link/PDF, find and read literature,
  review a claim or field, check novelty, build an evidence Bib, or answer a
  discovery QA question. Trigger: discover, find paper, add paper, paper run,
  source link, lit review, 找idea, 查新, verdict, landscape, qa,
  /haipipe-discovery.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.8.1"
  last_updated: "2026-09-04"
  # version history: ./CHANGELOG.md
---

# /haipipe-discovery · BJTR Discovery Task Pages + Paper Runs

Single entry for durable external-evidence work. A Discovery `tNN_` Task Page
Folder is one research Topic with BOTH a Page Face and a Task Face. It never references its
consumer upward; consumers link to its public Result Cards, typed records, or QA
digests from their own side.

For durable work, LOAD haipipe-folder and haipipe-page for the two Faces. Load
`haipipe-plugin-outline` for the Page's Outline + Evidence Workspace and its
CITE-item/aggregate-Bib authority. Once the Task Page owns a Paper Run, LOAD `haipipe-run`
for the neutral Level-4 contract. Then LOAD `haipipe-plugin-runs` for its
read-only Run/Result surface. The old `haipipe-plugin-evidence` entry is a
compatibility redirect only; do not treat it as a public plugin or citation
owner. Then read only the relevant Discovery authorities:

~~~text
ref/lifecycle-map.md           hierarchy × lifecycle × type
ref/page-types.md              Discovery article forms and Page/Run boundary
ref/paper-run-contract.md      Level-4 Run/Result/Bib law
ref/discovery-yaml-schema.md   Task manifest + typed records
ref/source-format.md           human source presentation
../board/page-plugins/haipipe-plugin-outline/ref/item-table.md
                                typed Evidence Item and Run-lineage grammar
../board/page-plugins/haipipe-plugin-outline/ref/evidence/citations.md
                                CITE authority and derived Bib aggregation
~~~

## Verbs

~~~text
/haipipe-discovery                              dashboard
/haipipe-discovery <task>                       full Task Page lifecycle
/haipipe-discovery <job|block>                  iterate child Tasks
/haipipe-discovery status [path]                read-only status
/haipipe-discovery open-block <name>             scaffold bNN Block
/haipipe-discovery open-job <block> <name>       scaffold jNN Job
/haipipe-discovery open <job> <type> <question>  scaffold tNN Task Page
/haipipe-discovery scope <task>                  freeze question/type/boundary
/haipipe-discovery prepare <task>                optional reusable instrument
/haipipe-discovery add <task> <trigger>          resolve Trigger; open Run(s)
/haipipe-discovery run <task> [RUNNAME]          execute one/all Paper Runs
/haipipe-discovery acquire <task>                resolve/admit/analyze Subjects
/haipipe-discovery synthesize <task>             promote Results into the Page
/haipipe-discovery check <task>                  validate BJTR + Page + Run/Result
/haipipe-discovery bib <task>                    rebuild derived Evidence Bib
/haipipe-discovery close <task>                  check + reconcile + close
/haipipe-discovery plan|build|execute|report ... compatibility aliases
/haipipe-discovery migrate-bjtr <bank>            dry-run legacy B/J/T migration
/haipipe-discovery migrate-bjtr <bank> --repair-pages  refresh migration Pages
/haipipe-discovery regroup-bjtr <bank>             repair one-Job-per-Block banks
/haipipe-discovery qa "<question>" [task]        question door; fn/qa.md
/haipipe-discovery feedback ...                  fn/feedback.md
/haipipe-discovery digest ...                    fn/digest.md
/haipipe-discovery <specialist> [args]           one-off worker, no folder
~~~

These are user-facing orchestration verbs, not a promise that every verb is a
subcommand of `paper_runs.py`. The deterministic helper currently implements
`check` and `build-bib`; the Discovery creator authors each Subject-specific
ticket from `ref/paper-run-contract.md`, and the `run` verb executes that
ticket. Worker diversity is receipt detail, not a reason to weaken the common
Run/Result contract.

## Model

`folder-kind: discovery` resolves to workflow phase D1 in
`../workflow-phases/haipipe-discovery-inquiry/SKILL.md`. That phase owns both
faces and the cross-face gate; this skill remains the user door and executor.

Three independent dimensions:

~~~text
HIERARCHY       Block -> Job -> Task Page -> Paper/Source Run
WORKFLOW        D1 Inquiry: SCOPE -> PREPARE? -> ACQUIRE <-> SYNTHESIZE -> CLOSE
DISCOVERY TYPE  source-map | source-reading | topic-summary | verdict |
                landscape | ideation variants in ref/page-types.md
~~~

`discoveries/` is the bank, not a Block. Every address-bearing level uses the
same grammar: `<level-letter><NN>_<noun>_<qualifier>`.

~~~text
discoveries/
└── b01_<block_noun>_<qualifier>/      Block: broad Board/program; prefer few
    ├── j01_<job_noun>_<qualifier>/    Job: one inquiry/campaign group
    └── j02_<job_noun>_<qualifier>/    sibling group on the same Board
        └── t01_<task_noun>_<qualifier>/  Task = article-shaped Page Folder
            ├── t01_<task_noun>_<qualifier>.md
            ├── discovery.yaml
            ├── outline/                           Page process + Evidence Workspace
            │   └── evidence/
            │       └── bibex/t01_<...>.bib        derived CITE aggregate
            ├── workflow/                          D1 phase receipts when a pass runs
            ├── scripts/                           optional instrument
            ├── runs/r01_<author><year>_<paper>.sh
            ├── results/r01_<author><year>_<paper>/
            ├── summary.md | verdict.md | landscape.md | ideas.md
            └── QA/
~~~

The path is the address. A Run above is `b01j01t01r01` compact and
`b01.j01.t01.r01` readable. Never write bare `01_`; never infer a missing level
letter from position. Physical prefixes are lowercase; the conceptual level
names are Block, Job, Task, and Run.

Result is not a fifth hierarchy level. A Content division may use many Results,
and one Result may support many divisions.

The Runs plugin is required once a Task Page owns any Paper Run. Discovery uses
its Folder-local dialect, the exact `runs/<RUNNAME>.sh <-> results/<RUNNAME>/`
pair; `scripts/` stays optional and appears only as supporting material. Runs
presents these artifacts but does not own Discovery's D1 workflow. The Outline
plugin owns the Page's Evidence Workspace, CITE verification, and derived Bib;
the compatibility Evidence entrypoint is not an authority, and there is no
separate Bibex plugin.

## Load-bearing Level-4 laws

1. One Run analyzes exactly one resolved canonical Subject, normally one paper.
2. Trigger explains why work started; Subject owns RUNNAME and the authoritative
   Bib. One Trigger may resolve to zero, one, or many Subjects.
3. runs/<RUNNAME>.sh and results/<RUNNAME>/ are an exact 1:1 same-stem pair.
   Opening a Run creates both, with runtime status planned.
4. A complete Result requires <RUNNAME>.md, facts.md, runtime.yaml, and an
   exactly-one-entry <RUNNAME>.bib whose key equals the Card's cite: @Key.
   Runtime must name the Bib source and `mode: verbatim_copy`. Metadata alone
   is not a supplied BibTeX entry and may not be formatted into one.
   `complete` is technical Result completeness; citation verification may
   still be `pending`, but then the Task cannot close as `ok` or
   `inconclusive`.
5. PDF, raw extraction, and captured Trigger text are optional.
6. Internal API, CLI, worker, and skill calls are receipt detail, never Runs.
7. The Task Page Evidence Bib is a deterministic union of completed Result Bibs
   at `outline/evidence/bibex/<task>.bib`. It is derived; correction lands in
   the Result Bib first. Every included Result records its person-verification
   receipt in `runtime.yaml` under `bib.verification`.
8. sources.md and notes.md are legacy/derived indexes, not authority for new
   per-paper work.
9. Every runtime receipt stamps the full readable and compact BJTR address;
   local `rNN` alone is insufficient outside its Task.

Full law: ref/paper-run-contract.md. Never improvise another durable shape.

## Discovery Page Types

~~~text
Search route   source-map · source-reading
Review route   topic-summary · prior-art-verdict · counterevidence-review
               landscape-review · benchmark-landscape
Idea route     ideation · novelty-verdict
~~~

`discovery_type` names what kind of article the root `tNN_<task>.md` promises to
the reader. The Page writes `folder-kind: discovery` and never
`page-type: task`. `discovery_type` is a domain field, not a Board `page-type:` key, Folder level,
phase, or Run. Search/Review/Idea are internal specialist routes derived from
that field:

~~~text
Search -> haipipe-discovery-search
Review -> haipipe-discovery-review
Idea   -> haipipe-discovery-idea
~~~

The root Page is always the human-facing article. `summary.md`, `verdict.md`,
`landscape.md`, and `ideas.md` are optional typed Task-side synthesis records;
they never replace the Page or become Runs. Full grammar and legacy
`type`/`role` normalization: `ref/page-types.md`.

Page-local evidence follows the shared Page contract: use `outline/evidence/`,
especially `outline/evidence/bibex/` and the generated Outline Evidence
Workspace. Discovery Paper/Source Results remain in `results/` and are not
copied into that workspace. The derived aggregate Bib is a projection, not by
itself a typed CITE Evidence Item. Create a typed CITE item only when the
approved Outline explicitly declares that item; then Outline records its
Supporting Run pointer and any required local Page Evidence Item Run. Direct
Result/cite lineage may otherwise support the Page without manufacturing an
item. D1 still owns Topic synthesis and never mints an umbrella Run merely to
repackage a paper.

## Routing

1. Resolve `folder-kind: discovery` through `haipipe-discovery-workflow` D1;
   the empirical Task Page compatibility grammar does not apply.
2. qa, feedback, and digest route to their fn file before other parsing.
3. A lifecycle/run verb operates on a durable `tNN_` Task Page Folder.
4. Existing Task, Job, and Block paths are detected by structure; Task runs the
   lifecycle, while Job/Block iterate their child Tasks.
5. open accepts a `jNN_` parent plus canonical `discovery_type`; legacy
   Search/Review/Idea plus
   role inputs normalize through `ref/page-types.md`.
6. A URL, DOI, PDF path, citation, or pasted source WITH a Task path routes to
   add. The Trigger is resolved before RUNNAME allocation.
7. A bare arXiv/DOI/URL without a Task Page is a one-off lookup unless the user
   asks to keep it. Keeping it requires choosing/opening a Task Page and then add.
8. Specialist or bucket names dispatch one-off work with no folder.
9. Natural language maps to Search (gather), Review (judge/map), or Idea
   (generate/check). Ask only when the type materially changes the output.

## Durable protocol

### 0. Resolve scope

Find the nearest project root containing tasks/, paper/, applications/, or
_haipipe/. Under its `discoveries/` bank, a Block owns Jobs, a Job owns Task
Pages, and a Task contains `discovery.yaml`. Detect existing units by structure,
but every new address must pass the explicit b/j/t/r naming gate.

### 1. Open the BJTR path

Resolve or allocate the next immutable `bNN_`, `jNN_`, and `tNN_` segments.
Each name uses a concrete noun plus distinguishing qualifier. Scaffold the Task
Page's two Faces and only the lanes the workflow needs. The Page filename
equals the Task folder stem. Scaffold the shared `outline/` process records as
the Page is used; create `outline/evidence/` lanes only when the Evidence
Workspace needs them. Do not scaffold empty scripts/, runs/, or results/
merely for symmetry, and never create a root `<task>/evidence/` lane.

A Block is a Board-level evidence program, not a wrapper around one Job. Reuse
an existing Block whenever a new inquiry belongs to the same program. A
single-Job Block is allowed only as a newly opened frontier; once several
related inquiry groups exist, they must be sibling Jobs under one Block rather
than one Block per Job.

### 2. SCOPE

Write discovery.yaml from ref/discovery-yaml-schema.md: full BJTR Task address,
Block/Job/Task ids, `discovery_type`, Page, question, source scope/candidate
rule, optional instrument, and typed record.
No parent, consumer, per-run inventory, or per-run config.

### 3. PREPARE (optional)

When a reusable query, extraction schema, prompt, or synthesis rubric is
needed, write it under scripts/. Otherwise skip PREPARE.

### 4. ACQUIRE · admit Trigger(s)

Classify and resolve each Trigger. Preserve its input/resolved identity in the
runtime receipt. For every admitted canonical Subject:

~~~text
allocate rNN_authorYEAR_slug
write executable runs/<RUNNAME>.sh
write results/<RUNNAME>/runtime.yaml with status: planned
stamp address: bNN.jNN.tNN.rNN and address_compact: bNNjNNtNNrNN
~~~

A Trigger that resolves to zero Subjects opens no Run; return it as unresolved
intake and record it in the project log when durable tracking is needed. If one
Trigger names multiple papers, fan out; never bundle them into one Run.
Before allocating, compare the canonical Subject and frozen intent with existing
runtimes. An unchanged duplicate DOI/URL reuses the existing Run/Result and
opens no new `rNN`; return or log that link without rewriting frozen Run inputs.
A materially changed analysis allocates a new Run with `supersedes:`.

### 5. ACQUIRE · run each admitted Subject

The ticket sets runtime to running, calls the selected workers, then writes its
paired Result only. On success write the Card, facts, one-entry Bib, optional
PDF/raw/trigger, and status complete. After Subject allocation, an analysis,
retrieval, or Bib failure preserves blocked or unresolved plus a reason. Never
claim complete around missing evidence.

### 6. SYNTHESIZE the Discovery type

Derive and dispatch the specialist route from `discovery_type`. Search
owns acquisition craft and materializes admitted candidates as Runs. Review
and Idea consume completed Results; missing evidence routes back to ACQUIRE.
Topic synthesis and idea generation stay authoritative L3 Page work; never
mint an umbrella Run for them.

### 7. CLOSE

Build the derived projection, write the closing report, then run the final
deterministic gate:

~~~bash
python scripts/paper_runs.py build-bib <task> --write
# append/reconcile discovery.yaml report: and Page/Aims state
python scripts/paper_runs.py check <task>
~~~

After SYNTHESIZE has produced the root Task Page and optional typed record,
use `haipipe-plugin-outline/ref/evidence/citations.md` to validate the derived
aggregate under `outline/evidence/bibex/`, append
`discovery.yaml report:`, reconcile its Run counts and canonical `evidence_bib`
path with the inventory, reconcile Page/Aims state, set the truthful terminal
status, and append project log events. The checker reports Result-level
citation-verification counts and rejects a legacy root `<task>/evidence/` lane.
CLOSE cannot report `ok` when a material Run is unresolved, a load-bearing Aim
is held, an aggregated complete Result citation is not person-verified in its
runtime receipt, or the checker fails. If the Outline
declares a typed CITE item, that item must independently pass the Outline CITE
gate. Missing work/gates report `blocked`;
`inconclusive` is reserved for completed admissible evidence with verified
aggregated Result citations that cannot establish the substantive answer.

## Maintenance · migrate or repair a legacy bank

Use `scripts/migrate_bjtr.py <bank> [<bank> ...]` to preview the deterministic
mapping from legacy two-level Discovery folders. The command is dry-run by
default; pass `--write` only after reviewing every destination. One legacy
bank becomes one explicit Board Block; each legacy Group becomes one numbered
`jNN_..._inquiry` Job, and its numbered leaves become sibling `tNN_` Task
Pages. The migrator upgrades
manifests, creates same-stem root Pages, and updates exact textual path
references inside the owning project.

Migration never infers Paper Runs from `sources.md`, `notes.md`, PDFs, or typed
records. Those artifacts remain readable migration inputs until a canonical
Subject is deliberately admitted through `add`. After writing, run
`paper_runs.py check` on every migrated Task Page; any failure leaves the bank
unclosed.
Banks produced by v0.6.1 may be repaired with `scripts/regroup_bjtr.py`; use its
dry run first and give the resulting Board a project-level evidence-program
slug/title. It moves old Block-root indexes into their corresponding Jobs and
rewrites B/J addresses and project-local references without changing Task or
evidence content.
Legacy completion tokens are evidence claims, not formatting. A preserved
`report:` supports only `reported` after structural migration; old `review`,
`ok`, and `inconclusive` do not prove that the new Result-backed evidence map is
closed. Without that receipt, they reopen as `executing`. Use
`migrate_bjtr.py --repair-pages` (dry-run first, then `--write`) to refresh only
Pages carrying the deterministic migration signature; authored Pages are left
untouched. The checker also requires Writing Style, a bounded Opening, a face
diagram per Content division, Content/Aim name agreement, and Page/Aim closure.

## QA question door

Full contract: fn/qa.md. It scans existing QA answers first, then completed
Result Cards, root Pages, and typed records. If existing artifacts answer the question it
writes a digest only. Otherwise it claims one QA ticket and enriches at the
shallowest depth: read existing Results, add Paper Runs to this Task, open a
new Task in the Job, open a Job in the Block, or open a Block. A consumer never
writes Discovery QA files.

## One-off work

One-off searches, readings, reviews, and ideas return inline and write no
durable files. If the user chooses to keep evidence, route through a Task Page's add
verb so the canonical Subject receives a numbered Run, paired Result, and Bib.

## Feedback

Use fn/feedback.md for the skill-feedback inbox and fn/digest.md to harvest a
session. Behavioral preferences live in PREFERENCES.md and are always honored.
