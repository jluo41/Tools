---
name: haipipe-discovery-inquiry
description: >-
  Discovery Folder contract for one inquiry. It owns folder-kind discovery,
  the four-role article Page Face, the Paper/Source Run Task Face, selected
  workbenches, Discovery controller routing, shared Page-workflow handoff, cross-face closure,
  and evidence handoff. Use when resolving,
  scaffolding, checking, or closing one BJTR Discovery Task Page Folder.
metadata:
  version: "0.7.1"
  last_updated: "2026-09-22"
  workflow: haipipe-discovery-inquiry
  phase: D1 # compatibility selector for the Discovery controller contract; not a Run identity
  folder_kind: discovery
  primary_face: page
  page_ruling: none
  outline:
    mode: grammar
    source: "this SKILL.md"
    shape: "four ordered role headings: Question and boundary, Type payload, Evidence map, Limits and next move; each adds a subject-specific title and owns the same-name Aim group"
---

# /haipipe-discovery-inquiry · Discovery owner contract and Run Workflow

## Position

D1 is the retained Discovery controller label. Its lifecycle vocabulary names
internal routing Steps, not Workflow units:

```text
SCOPE -> PREPARE? -> ACQUIRE <-> SYNTHESIZE -> CLOSE
```

This skill is the Discovery Folder owner and Run Workflow definition; there is
no second Discovery workflow skill to load. A live Workflow is a list of
selected owner-native Run Instances and their dependency/route graph. This
contract defines the available Run Specs; its Runtime lists the selected
Discovery source Runs and, when commissioned, the separately owned Page Runs.
SCOPE, PREPARE, ACQUIRE, SYNTHESIZE, and CLOSE are controller Steps that route
between those Runs and their gates; they are not Run identities or additional
workflow units. The Page Face independently advances through
`haipipe-page-workflow` 00–04. D1 SYNTHESIZE hands Results to that workflow;
it does not write Page artifacts through a private lifecycle. Each admitted
canonical paper or source is one Discovery Level-4 Run. The D1 root uses the
direct Result/cite route for its evidence objects, but it does not bypass the
Page's human-interaction contract: when Page interaction is selected, the Page
workflow owns `rp00_mermaid-structure` first and `rpNN_pNN[-pNN]` thereafter.
Those Page Runs are not D1 Runs and never enter the Discovery inventory.

At the skill-bank level, `haipipe-discovery-search`, `haipipe-discovery-review`,
and `haipipe-discovery-synthesize` are the three live capability skills at the
family root; `1_search/` and `2_review/` hold only the vendored originals they
may call. Search resolves candidates, Review inspects one source/Result, and
Synthesize combines accepted Results into the Page. These skills do not add
D1/D2/D3 phases or Runs. This controller sits at the family root too (the former
`workflow-phases/` path is retired) and owns the Discovery Run Specs and
controller routing policy.

The canonical Run Specs, controller-Step routing, Runs Overview, Human Actions,
and Skill Coverage live in `ref/workflow-table.md`.

The retrofit of earlier 0/1/2/3 or 1/2/3/4 descriptions is authoritative in
`../haipipe-discovery/ref/bjtr-alignment.md`: D1 names controller Steps,
while the project address remains Block -> Job -> Task Page -> Run.

## Board formation

The D1 controller forms the Board as the BJTR path is opened. Block is Board,
Job is Group, Task is Page Folder, and Run is an execution record. Discovery
owns the source tree; `haipipe-board` owns the generated projection. On
`open-block`, `open-job`, and `open`, call
`../haipipe-discovery/scripts/board_sync.py <block>` so `board.md` and its
managed Job span remain current. After a Run batch, Page `04 CHECK`, and before
D1 CLOSE, call it with `--build --check --strict`. The helper never writes
individual Task rows or Run content into `board.md`; the direct `jNN_/tNN_`
tree supplies membership and order.

## Folder Kind

`folder-kind: discovery` resolves here. The Folder lives at
`discoveries/bNN_<block>/jNN_<job>/tNN_<task>/`, with readable address
`bNN.jNN.tNN`. It has both faces; “Task” names its work altitude and does not
select the empirical `page-type: task` compatibility grammar.

## Input

- One bounded external-world question.
- A canonical `discovery_type` and source/admission boundary. Before broad
  retrieval, freeze a question-specific candidate rule at SCOPE, including the
  topical inclusion/exclusion test and coverage/stopping boundary. If that
  rule is missing or too vague to apply, return to SCOPE or hold for resolution
  before opening Runs; retrieval ranks and citation counts are not substitutes.
- Zero or more preserved records or candidate sources.
- For each D1 `ACQUIRE` Run, one resolved canonical Subject and its
  Trigger.

## Page Face

The root same-stem Page writes `folder-kind: discovery` and follows the shared
Opening → generated Outline → Content → Aims frame. Content has four ordered
roles; the words before the second ` · ` are fixed and the rest is specific to
the inquiry. A face diagram belongs inside each Content division; there is no
top-level `## Diagram` or authored `## Outline` section:

```text
1 · Question and boundary · <the exact inquiry and evidence population>
  2 · Type payload · <the source map, source reading, summary, verdict, or landscape>
3 · Evidence map · <the claims, Result Cards, cite keys, disagreements, and gaps>
4 · Limits and next move · <what is not established and the next lawful route>
```

Each division opens with a captioned face diagram. A1–A4 repeat the complete
same-name division title after their emoji. Migration may leave Type payload
active and historical evidence mapping explicitly held; it may not claim that
linked legacy files already satisfy Result-backed synthesis.

The shared Outline workbench owns the plan, candidate preview, requirement records,
feedback, and nested Evidence Workspace. Discovery does not put writing rules
in a `## Writing Style` section. `outline/<stem>-logic.mmd` is the derived Page
structure reviewed by `rp00_mermaid-structure`; paragraph Page Runs begin at
`rp01` only after that structure and the Page-global `P01..PN` order close.

## Task Face

`discovery.yaml` owns intent, lifecycle status, and the closing report. SCOPE
bounds the question; PREPARE optionally creates a reusable instrument;
ACQUIRE admits and analyzes canonical Subjects; SYNTHESIZE dispatches the
shared Page workflow and may write an optional Task-side typed record; CLOSE
updates only the Task report/status after the Page has passed CHECK.

The Page process folder is shared with every Page: `outline/` holds planning
material and, when the inquiry needs citation material, `outline/evidence/`
holds the derived Bib. The D1 root Page uses direct Result/Card/cite lineage
and does not create a local typed Evidence Item for its own Results.
Discovery's own analysis receipts remain the local `rNN` subset of the shared
`runs/` ↔ `results/` lanes. Page-owned `rpNN` records may coexist in those
folders, but are not Discovery inventory and are validated by the Page
workflow. Do not copy Discovery Results into `outline/evidence/` or create a
second local Evidence Run merely to repackage a paper.

### Run Profile

- **ALLOWED**: `paper-analysis`, `source-analysis`.
- **TARGET**: one canonical paper, dataset, report, webpage, media item, or
  other source Subject.
- **TICKET**: executable `runs/rNN_<author-or-source><year>_<slug>.sh`.
- **INPUTS**: Trigger provenance, resolved Subject identity, question, and
  admission rationale.
- **WORKER**: the selected research/source-analysis skill.
- **RESULT**: same-stem Result Card, `facts.md`, `runtime.yaml`, optional PDF,
  and one authoritative one-entry Bib.
- **COMMISSION**: only D1 `ACQUIRE` may allocate a Discovery Run.
- **ACCEPT**: identity, pairing, provenance, facts, cite key, and status pass
  `paper_runs.py check`.
- **PROMOTION**: completed Results may be synthesized many-to-many into the
  Page and derived Evidence Bib; Page-owned writing interaction is promoted
  only through the shared Page release barrier.
- **REOPEN**: a changed Result, material unresolved Run, or expanded evidence
  population reopens ACQUIRE and the affected Page workflow authority.

## Workbenches

- **required**: Folder/Page surface and `haipipe-workbench-page`; Outline owns
  the Evidence Workspace and derived Discovery aggregate. Each
  Discovery Result owns its one-entry Bib verification receipt in
  `runtime.yaml`.
- **conditional**: Runs presenter when the first Run is admitted; an Outline
  evidence lane only when the Page needs it. Cross-Folder consumers use
  Supporting Run Result pointers, not PageX.
- **compatibility-only**: the legacy Evidence renderer may resolve old routes,
  but it is not a public tab or storage authority.
- **forbidden**: a separate Bibex or reading workbench, a root `<page>/evidence/`
  lane, empty Runs/Results lanes, or a Task Page compatibility grammar layered
  over the Discovery Page Face.

### Page Run boundary

The `runs/` ↔ `results/` pair in a Discovery Task Folder is reserved for
`paper-analysis` and `source-analysis` `rNN` Runs. The Page-facing `rpNN` lane
is owned by `haipipe-page-workflow` and may be shown by the Runs presenter, but
it is not copied into the Discovery `runs/` inventory and does not change
`R_discovery = N_admitted`. D1 SYNTHESIZE may request or resume Page-owned
interaction; it may not mint `division-writing`, a per-division Discovery Run,
or an umbrella synthesis Run.

## Gate and Closure

The Page must close through `04 CHECK` before D1 CLOSE may close the Folder's
Task Face. The Page release barrier must be satisfied before CONTENT adoption:
`rp00_mermaid-structure`, every selected paragraph Page Run, and every required
Task Result must be complete and bound. D1 closure requires `paper_runs.py check` to pass, every material
admitted Run is resolved or explicitly held, the Page answers its question at
the promised `discovery_type`, and Page state agrees with `discovery.yaml`.
`report:` supports `reported`; `ok` additionally requires the Result-backed
Evidence map, the Outline CITE aggregate, and all load-bearing Page Aims
to be met. Non-load-bearing limitations may remain recorded, but a held
load-bearing Aim forbids `ok`. Every complete Result entering the aggregate
must also carry the
Result-runtime person judgment `bib.verification: verified` before CLOSE may
claim an epistemic `status: ok` or `status: inconclusive` outcome.
Missing operational work or citation-verification debt yields `blocked`;
`inconclusive` is reserved for completed admissible evidence that cannot
establish the substantive answer. Neither receipt may claim `ok`.

## Handoff

Consumers receive the root Page, exact Result/Card links, cite keys, the
derived `outline/evidence/bibex/<task>.bib`, disagreements, and unresolved
limits. A consumer never treats a legacy source index as a Result receipt.

## Files

- `ref/workflow-table.md` — canonical Discovery specialization of the shared
  Page Workflow Steps, Runs Overview, Human Actions, and Skill Coverage.
- `../haipipe-discovery/ref/board-sync.md` — Block-as-Board source shape and
  lifecycle checkpoints.
- `../haipipe-discovery/ref/bjtr-alignment.md` — numbered-family retrofit and
  BJTR crosswalk.
- `../haipipe-discovery/SKILL.md` — user door, executor, and compatibility
  verbs.
- `../haipipe-discovery/ref/page-types.md` — type-specific payload promises.
- `../haipipe-discovery/ref/paper-run-contract.md` — Level-4 artifacts.
- `../haipipe-discovery/scripts/paper_runs.py` — deterministic gate.
- `../../page/haipipe-page-workflow/SKILL.md` — the only
  Page lifecycle and phase router.
- `../../page/haipipe-workbench-page/SKILL.md` — Outline and
  Evidence Workspace owner.
- `../../page/haipipe-workbench-page/ref/evidence/citations.md`
  — CITE verification and derived Bib authority.
