---
name: haipipe-discovery
description: >-
  External-evidence executor built as Discovery Task Page Folders. One folder
  owns one research Topic and many numbered Paper Runs; every durable paper or
  source is analyzed through a numbered shell ticket and its exact same-stem
  Result directory containing a Result Card, facts, runtime receipt, and
  one-entry BibTeX. Use to add a paper/link/PDF, find and read literature,
  review a claim or field, check novelty, build an evidence Bib, or answer a
  discovery QA question. Trigger: discover, find paper, add paper, paper run,
  source link, lit review, 找idea, 查新, verdict, landscape, qa,
  /haipipe-discovery.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.4.2"
  last_updated: "2026-09-01"
  # version history: ./CHANGELOG.md
---

# /haipipe-discovery · Discovery Topic Page + Paper Runs

Single entry for durable external-evidence work. A Discovery Folder is one
research Topic with BOTH a Page Face and a Task Face. It never references its
consumer upward; consumers link to its public Result Cards, terminals, or QA
digests from their own side.

For durable work, LOAD haipipe-folder and haipipe-page for the two Faces. Once
the Topic owns a Paper Run, LOAD `haipipe-plugin-runs` for its Run/Result
surface. Then read only the relevant Discovery authorities:

~~~text
ref/lifecycle-map.md           hierarchy × lifecycle × type
ref/paper-run-contract.md      Level-4 Run/Result/Bib law
ref/discovery-yaml-schema.md   Topic Task manifest + terminals
ref/source-format.md           human source presentation
~~~

## Verbs

~~~text
/haipipe-discovery                              dashboard
/haipipe-discovery <topic>                      full Topic lifecycle
/haipipe-discovery <group>                      summarize child Topics
/haipipe-discovery status [path]                read-only status
/haipipe-discovery open <type> <question>       scaffold Topic Page Folder
/haipipe-discovery open-group <slug>            ensure Drop/group directory
/haipipe-discovery plan <topic>                  write/update discovery.yaml
/haipipe-discovery build <topic>                 optional reusable instrument
/haipipe-discovery add <topic> <trigger>         resolve Trigger; open Run(s)
/haipipe-discovery run <topic> [RUNNAME]         execute one/all Paper Runs
/haipipe-discovery execute <topic>               type-level Execute
/haipipe-discovery check <topic>                 validate Run/Result spine
/haipipe-discovery bib <topic>                   rebuild derived Evidence Bib
/haipipe-discovery report <topic>                check + bib + synthesize Report
/haipipe-discovery qa "<question>" [topic]       question door; fn/qa.md
/haipipe-discovery feedback ...                  fn/feedback.md
/haipipe-discovery digest ...                    fn/digest.md
/haipipe-discovery <specialist> [args]           one-off worker, no folder
~~~

## Model

Three independent dimensions:

~~~text
HIERARCHY   Block -> Drop -> Discovery Task Page Folder -> Paper Run
LIFECYCLE   Plan -> Build(optional) -> Execute -> Report
TYPE        Search | Review | Idea
~~~

The Page Face communicates the Topic. The Task Face executes it:

~~~text
<topic>/
├── <topic>.md                         Page Face
├── discovery.yaml                     Task Face manifest
├── outline/                           optional
├── evidence/bibex/<topic>.bib         DERIVED from completed Results
├── scripts/                           optional reusable instrument
├── runs/<RUNNAME>.sh                  authored Level-4 ticket
├── results/<RUNNAME>/                 same Level-4 unit, generated projection
├── verdict.md | landscape.md | ideas.md
└── QA/                                optional readable digests
~~~

Result is not a fifth hierarchy level. A Content division may use many Results,
and one Result may support many divisions.

The Runs plugin is required once a Topic owns any Paper Run. Discovery uses its
Folder-local dialect, the exact `runs/<RUNNAME>.sh <-> results/<RUNNAME>/`
pair; `scripts/` stays optional and appears only as supporting material. Runs
presents these artifacts but does not own Discovery's
Plan/Build/Execute/Report lifecycle.

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
5. PDF, raw extraction, and captured Trigger text are optional.
6. Internal API, CLI, worker, and skill calls are receipt detail, never Runs.
7. The Topic Evidence Bib is a deterministic union of completed Result Bibs.
   It is derived; correction lands in the Result Bib first.
8. sources.md and notes.md are legacy/derived indexes, not authority for new
   per-paper work.

Full law: ref/paper-run-contract.md. Never improvise another durable shape.

## Types

~~~text
Search   find candidates -> resolve -> admit Paper Runs -> Page source map
Review   synthesize completed Results -> verdict.md or landscape.md
Idea     generate at Topic level; novelty papers still become Paper Runs
~~~

Search/Review/Idea select type-level behavior; they are not lifecycle phases.
Their specialists own Execute:

~~~text
Search -> haipipe-discovery-search
Review -> haipipe-discovery-review
Idea   -> haipipe-discovery-idea
~~~

## Routing

1. qa, feedback, and digest route to their fn file before other parsing.
2. A lifecycle/run verb operates on a durable Topic Folder.
3. An existing Topic path runs the requested stage or full lifecycle.
4. open accepts Search, Review, or Idea.
5. A URL, DOI, PDF path, citation, or pasted source WITH a Topic path routes to
   add. The Trigger is resolved before RUNNAME allocation.
6. A bare arXiv/DOI/URL without a Topic is a one-off lookup unless the user asks
   to keep it. Keeping it requires choosing/opening a Topic and then add.
7. Specialist or bucket names dispatch one-off work with no folder.
8. Natural language maps to Search (gather), Review (judge/map), or Idea
   (generate/check). Ask only when the type materially changes the output.

## Durable protocol

### 0. Resolve scope

Find the nearest project root containing tasks/, paper/, applications/, or
_haipipe/. A Topic Folder contains discovery.yaml. A group contains Topic
children. Never write a durable package into an ambiguous project.

### 1. Open the Topic

Allocate the next immutable group/topic numbers. Scaffold the two Faces,
discovery.yaml, and only the lanes the selected workflow needs. Do not scaffold
empty scripts/, runs/, or results/ merely for symmetry.

### 2. Plan

Write discovery.yaml from ref/discovery-yaml-schema.md: type, role, Page,
question, source scope/candidate rule, optional instrument, and topic terminal.
No parent, consumer, per-run inventory, or per-run config.

### 3. Build (optional)

When a reusable query, extraction schema, prompt, or synthesis rubric is
needed, write it under scripts/. Otherwise skip Build.

### 4. Add Trigger(s)

Classify and resolve each Trigger. Preserve its input/resolved identity in the
runtime receipt. For every admitted canonical Subject:

~~~text
allocate rNN_authorYEAR_slug
write executable runs/<RUNNAME>.sh
write results/<RUNNAME>/runtime.yaml with status: planned
~~~

An unresolved Trigger gets a truthful receipt and cannot enter Evidence. If one
Trigger names multiple papers, fan out; never bundle them into one Run.

### 5. Run

The ticket sets runtime to running, calls the selected workers, then writes its
paired Result only. On success write the Card, facts, one-entry Bib, optional
PDF/raw/trigger, and status complete. On failure preserve blocked or unresolved
plus a reason. Never claim complete around missing evidence.

### 6. Execute the type

Dispatch the type specialist. Search materializes candidates as Runs. Review
and novelty work consume completed Results and add missing evidence as new
Runs. Idea generation itself stays Topic-level Page work.

### 7. Report

Run both deterministic gates:

~~~bash
python scripts/paper_runs.py check <topic>
python scripts/paper_runs.py build-bib <topic> --write
~~~

Then synthesize the root Page and type terminal, append discovery.yaml report:,
set status ok/inconclusive/blocked, and append project log events. Report cannot
be ok when a material Run is unresolved or the checker fails.

## QA question door

Full contract: fn/qa.md. It scans existing QA answers first, then completed
Result Cards and topic terminals. If existing artifacts answer the question it
writes a digest only. Otherwise it claims one QA ticket and enriches at the
shallowest depth: read existing Results, add Paper Runs to this Topic, open a
new Topic, or open a new group. A consumer never writes Discovery QA files.

## One-off work

One-off searches, readings, reviews, and ideas return inline and write no
durable files. If the user chooses to keep evidence, route through a Topic's add
verb so the canonical Subject receives a numbered Run, paired Result, and Bib.

## Feedback

Use fn/feedback.md for the skill-feedback inbox and fn/digest.md to harvest a
session. Behavioral preferences live in PREFERENCES.md and are always honored.
