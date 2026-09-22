---
name: haipipe-paper
description: >-
  The one door for planning, writing, and revising a paper as a graph of Board
  Pages. Routes Ideation, Story, Section and Round Pages through the shared
  Page lifecycle; Discovery and Task owners execute the external work lane.
  Use for paper setup, status, drafting, complete-paper assembly, compiling,
  or review rounds.
metadata:
  version: "1.3.0"
  last_updated: "2026-09-21"
  summary: "Paper owns the journey and composition; the shared Page owns each Paper Page's lifecycle and release."
---

# /haipipe-paper · compose a paper from evidence-bearing Pages

`haipipe-paper` is the Paper-family router. It does not implement the Page
workflow and it does not replace the specialist Page Type contracts.

Use two orders for two different jobs. First route the family request:

```text
haipipe-paper
  → haipipe-paper-workflow, when the question is the journey or a gate
  → resolve the concrete Page and its Page Type
```

When creating or updating a concrete Page, use the Page router's canonical order:

```text
haipipe-page
  → haipipe-page-workflow
  → current Run Workflow / Run Spec owner
  → haipipe-paper-workflow (Folder-owning workflow)
  → the exact Page Type: haipipe-paper-ideation · haipipe-paper-story ·
    haipipe-paper-section · haipipe-paper-round, or haipipe-paper-venue
  → Run Spec references / the Story's Section row and style policy
  → haipipe-run + selected workers, only where Runs exist
  → paper/haipipe-paper/ref/page-integration.md and ref/run-naming.md when a
    Paper-local Run or Page release is planned
```

For CONTEXT, OUTLINE, and EVIDENCE, the exact material contracts are
`haipipe-workbench-page/ref/...` files. The Page surface already installs the
shared Outline presenter; it is not a final execution dependency.

Read [`ref/page-integration.md`](ref/page-integration.md) for the Paper-specific
consequences of the shared Page contract. This router owns no second Page
lifecycle, Page Run namespace, Evidence Workspace, or Page release protocol.

`haipipe-paper-assemble` is a separate complete-paper verb after routing; it has its own bounded compile Spec in the Paper Workflow.

## Paper Workflow and content owners

A Paper Workflow is the `paper-runs` layer: a list of bounded owner-native
Runs. Read
`haipipe-paper-workflow/ref/run-workflow.md` for Specs, dependencies and G0–G5;
Page containers, status reads and gate records do not allocate Runs.

| Owner | Paper responsibility |
|---|---|
| Ideation | semantic idea cards and the I3 handoff; `haipipe-paper-ideation` projects it |
| Story | prospective C1–C8 blueprint and selected telling; `haipipe-paper-story` |
| Venue | shared evidence-backed desk contract; `haipipe-paper-venue` |
| Section | reader-ordered manuscript unit and its wording/evidence; `haipipe-paper-section` |
| Round | one feedback batch and checked response; `haipipe-paper-round` |

Use native receipts to report the current owner, accepted Result/version,
pending dependency and next human decision. Retargeting keeps Story identity,
binds the selected Venue and changes only the candidate telling in C8. Read the
exact PageType contract for its content rules; this router does not restate it.

`/haipipe-paper status` is a read-only rollup, not a Page Type or lifecycle.

## 🃏 Evidence and Page boundary

Paper Pages use the shared Page Face, Page Run, Evidence Item and Page CHECK
contracts. `haipipe-page` and `haipipe-page-workflow` own the lifecycle;
`haipipe-workbench-page` presents typed CITE, VALUE and DISPLAY Results. Load
[`ref/page-integration.md`](ref/page-integration.md) for the Paper-specific
ownership, release, source/projection and Run boundaries, and
[`ref/run-naming.md`](ref/run-naming.md) for Paper context and identities.

Supporting Task/Discovery Runs retain their native owners. A Page-local Result
is the evidence authority for the Page; assembly may copy accepted artifacts
but never becomes a wording or evidence source.

For visual displays, load `haipipe-display`; its concept-first gate owns
composition references, editable reconstruction and candidate promotion.

## 🚪 Routing

Resolve the paper root and target Page before changing anything.

| User intent | Route |
|---|---|
| brainstorm, novelty-check, compare or select ideas | `haipipe-ideation` and only its relevant specialist; use `haipipe-paper-ideation` when a Paper Page projection is involved |
| create, refresh, read or check the Paper Idea portfolio Page | `haipipe-page` + `haipipe-page-workflow` + `haipipe-paper-ideation`; load the semantic owner for sync/handoff |
| ask where a paper is in the journey, or test a gate | `haipipe-paper-workflow` |
| draft or review the whole paper, its research roadmaps or section narrative | `haipipe-paper-story` |
| release work, inspect execution progress, accept a receipt, or release a Section | `haipipe-paper-workflow` plus the exact Discovery/Task/Section owner; use Story for the resulting paper meaning |
| inspect or record a target venue | `haipipe-paper-venue` (shared reference library) |
| write or revise one manuscript/appendix unit | `haipipe-paper-section` |
| triage or answer one feedback/review cycle | `haipipe-paper-round` |
| check paper or one family's status | `/haipipe-paper status` (command, not a Page Type) |
| run one Page through its lifecycle | `haipipe-page-workflow` |
| compile or export one Page | `haipipe-workbench-page`, using its LaTeX or Word lane |
| assemble the paper | `haipipe-paper-assemble` from the Section Pages' own `delivery/latex/` outputs and accepted bindings |
| respond to reviewers | a Round Page plus the affected Story rows and Sections |

### Paper verbs

```text
/haipipe-paper ideate <direction|idea-id> [controller-label]
/haipipe-paper enter [paper]
/haipipe-paper status [paper] [section|evidence|citation|display]
/haipipe-paper journey [paper]         read the journey position · test the gates ·
                                       never advances anything
/haipipe-paper story [paper] [controller-label]
/haipipe-paper venue <target> [controller-label]
/haipipe-paper section <section-id> [controller-label]
/haipipe-paper round <new|id>
/haipipe-paper assemble [paper]        runs anytime · a build made while gate G4
                                       fails is watermarked DRAFT in its receipt
```

`[controller-label]` is an optional Page dispatch hint (CONTEXT…CHECK), not a
Workflow unit. Existing callers using the old positional argument remain
readable as this hint; the receipt and native owner decide the action.
When a concrete Page is named, resolve its owner before choosing work. Omit the
hint to resume from its latest receipt.

### Shared skills, loaded when needed

| Need | Owner to load |
|---|---|
| idea generation, testing, selection | `haipipe-ideation` → its generate/test/select skill and requested specialist |
| external sources, review, synthesis | `haipipe-discovery` → selected Discovery capability |
| computation, experiments, reusable execution | `haipipe-task` → selected Task worker |
| native Run identities and closure | `haipipe-run`, when commissioning/resuming a Run |
| a concrete Page | `haipipe-page` + `haipipe-page-workflow` + its exact Paper PageType |
| Page outline/evidence material | the relevant `haipipe-workbench-page/ref/...` contract; presenter already installed |
| one Page export | `haipipe-workbench-page` and the selected format reference |
| a display Evidence Item | `haipipe-display` and the chosen worker, through the Page RE Result contract |
| Paper board presentation | `haipipe-workbench-paper`; `haipipe-board` owns rendering/checking |

Load only what the request uses. Reuse an already loaded owner; do not recurse
between the Paper router, Page router and domain adapter. Insight and Design
remain independent families, referenced through their own Results/contracts.

## 📐 Story boundary

`haipipe-paper-story` owns C1–C8 meaning, the read-through test and the selected
telling. Each Section binds one current C8 row through `story-row:`. Read
`haipipe-paper-story/ref/integration.md` for the compile-order interface;
planning a Section does not instantiate its Page, authorize execution or imply
approval.

## 📂 Paper structure

Read [`ref/paper-structure.md`](ref/paper-structure.md) for the folder layout,
group and Section naming, compile-order markers, Task boundary, delivery law
and migration rules. The Paper router only resolves the structure owner; it does
not maintain a second naming or migration contract.

## 📦 Assembly and delivery

`haipipe-paper-assemble` owns source-driven complete-paper builds. It reads
Section-owned LaTeX fragments, accepted bindings and `paper-build.toml`, then
regenerates `delivery/`. Generated DOCX/PDF files are projections, never inputs.
Assembly may run before G4, but the manifest stays `DRAFT` until the Section
CHECK and Paper readiness gates are closed. Load the assembly skill for its
engine, profile and receipt contract.

## 🚦 Submission-readiness gate (G4 · before submission)

Run the gate defined in [`ref/submission-readiness.md`](ref/submission-readiness.md)
after assembly: freeze evidence, check the story and reporting, apply the
21-point `SUB-*` overlay, verify venue files, and complete the independent human
pass. A clean render is necessary but never sufficient. The build remains
`DRAFT` while hard blockers or required human decisions are open.

## 🧱 Current architecture boundary

The former S01–S10 stage contracts, stage resolver, S-page creator, S03/S04
topic-entry tooling, stage-specific craft, and their helper scripts are outside
the current Paper runtime. This door does not load them.

The current Paper graph has one Story prospective blueprint. Its C1–C5 Seed
content, C6 Discovery Roadmap, C7 Task Roadmap, and C8 Section Narrative remain
substantive Story content; the corresponding execution, Section, Compile, and
Round records stay with their native owners. The router reads no retired child
Page, compatibility alias, or fallback source.

## ✅ Completion checks

Before reporting Paper work complete, identify the active Page owner, Run Spec,
Story/C8 row, accepted evidence/display Results, current Page CHECK versions,
assembly manifest and G4 status. Keep DRAFT, blocked, deferred and human-owned
decisions explicit. A discussion or planning handoff does not create a Run,
release a Section or close G4. Use the owning Page, Workflow, Assembly, Venue
and submission references for detailed checks.

## 📂 Family boundary

See [`../README.md`](../README.md) for the family index. This door owns Paper
routing and composition; Page, Workflow, Run, Evidence, Display, Board, Venue
and Assembly owners retain their own contracts.
