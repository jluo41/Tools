---
name: haipipe-discovery-inquiry
description: >-
  D1 Folder contract for one Discovery inquiry. It owns folder-kind discovery,
  the four-role article Page Face, the Paper/Source Run Task Face, selected
  plugins, D1 Task workflow, shared Page-workflow handoff, cross-face closure,
  and evidence handoff. Use when resolving,
  scaffolding, checking, or closing one BJTR Discovery Task Page Folder.
metadata:
  version: "0.4.1"
  last_updated: "2026-09-04"
  workflow: haipipe-discovery-workflow
  phase: D1
  folder_kind: discovery
  primary_face: page
  page_ruling: none
  outline:
    mode: grammar
    source: "this SKILL.md"
    shape: "four ordered role headings: Question and boundary, Type payload, Evidence map, Limits and next move; each adds a subject-specific title and owns the same-name Aim group"
---

# /haipipe-discovery-inquiry · D1 owns one evidence question

## Position

D1 is the sole Discovery Folder phase and owns the domain/Task workflow:

```text
SCOPE -> PREPARE? -> ACQUIRE <-> SYNTHESIZE -> CLOSE
```

The stable metadata value `haipipe-discovery-workflow` is its registry identity,
not a second skill to load. The Page Face independently advances through
`haipipe-page-workflow` 00–04. D1 SYNTHESIZE hands Results to that workflow;
it does not write Page artifacts through a private lifecycle. Each admitted
canonical paper or source is one Discovery Level-4 Run. The D1 root uses the
Page CONTENT no-Run route; consumer Pages own any Page-family Runs they need.

At the skill-bank level, `1_search`, `2_review`, and `3_idea` are numbered
capability families analogous to the numbered groups under `haipipe-task`.
They select specialist craft; they do not add D1/D2/D3 phases. Only this skill
under `workflow-phases/` owns the Discovery phase contract.

The canonical Phase × Run declaration, Runs Overview, Human Actions, and Skill
Coverage live in `ref/workflow-table.md`.

## Folder Kind

`folder-kind: discovery` resolves here. The Folder lives at
`discoveries/bNN_<block>/jNN_<job>/tNN_<task>/`, with readable address
`bNN.jNN.tNN`. It has both faces; “Task” names its work altitude and does not
select the empirical `page-type: task` compatibility grammar.

## Input

- One bounded external-world question.
- A canonical `discovery_type` and source/admission boundary.
- Zero or more preserved records or candidate sources.
- For each D1 `ACQUIRE` Run, one resolved canonical Subject and its
  Trigger.

## Page Face

The root same-stem Page writes `folder-kind: discovery` and follows the shared
Opening → optional Diagram → Content → Aims frame. Content has four ordered
roles; the words before the second ` · ` are fixed and the rest is specific to
the inquiry:

```text
1 · Question and boundary · <the exact inquiry and evidence population>
2 · Type payload · <the source map, reading, summary, verdict, landscape, or ideas>
3 · Evidence map · <the claims, Result Cards, cite keys, disagreements, and gaps>
4 · Limits and next move · <what is not established and the next lawful route>
```

Each division opens with a captioned face diagram. A1–A4 repeat the complete
same-name division title after their emoji. Migration may leave Type payload
active and historical evidence mapping explicitly held; it may not claim that
linked legacy files already satisfy Result-backed synthesis.

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
Discovery's own analysis receipts remain the local `runs/` ↔ `results/` pair;
do not copy those Results into `outline/evidence/` or create a second local
Evidence Run merely to repackage a paper.

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
  Page and derived Evidence Bib.
- **REOPEN**: a changed Result, material unresolved Run, or expanded evidence
  population reopens ACQUIRE and the affected Page workflow authority.

## Plugins

- **required**: Folder/Page surface and `haipipe-plugin-outline`; Outline owns
  the Evidence Workspace and derived Discovery aggregate. Each
  Discovery Result owns its one-entry Bib verification receipt in
  `runtime.yaml`.
- **conditional**: Runs presenter when the first Run is admitted; an Outline
  evidence lane only when the Page needs it. Cross-Folder consumers use
  Supporting Run Result pointers, not PageX.
- **compatibility-only**: the legacy Evidence renderer may resolve old routes,
  but it is not a public tab or storage authority.
- **forbidden**: a separate Bibex or reading plugin, a root `<page>/evidence/`
  lane, empty Runs/Results lanes, or a Task Page compatibility grammar layered
  over the Discovery Page Face.

## Gate and Closure

The Page must close through `04 CHECK` before D1 CLOSE may close the Folder's
Task Face. D1 closure requires `paper_runs.py check` to pass, every material
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
  Page phases, Runs Overview, Human Actions, and Skill Coverage.
- `../../haipipe-discovery/SKILL.md` — user door, executor, and compatibility
  verbs.
- `../../haipipe-discovery/ref/page-types.md` — type-specific payload promises.
- `../../haipipe-discovery/ref/paper-run-contract.md` — Level-4 artifacts.
- `../../haipipe-discovery/scripts/paper_runs.py` — deterministic gate.
- `../../../board/page-workflows/haipipe-page-workflow/SKILL.md` — the only
  Page lifecycle and phase router.
- `../../../board/page-plugins/haipipe-plugin-outline/SKILL.md` — Outline and
  Evidence Workspace owner.
- `../../../board/page-plugins/haipipe-plugin-outline/ref/evidence/citations.md`
  — CITE verification and derived Bib authority.
