---
name: haipipe-paper
description: >-
  The one door for planning, writing, and revising a paper on the ladder: a
  paper Board, one version Job per send, one Page Task per Section, Abstract or
  letter, and their run-<type>-<target> Runs. Routes by level to the Story,
  Ideation, Venue, Section, comments and assembly owners; the shared Page
  lifecycle runs each Task, and Discovery and Task owners execute the external
  work. Use for paper setup (paper_ladder.py), status, drafting, a Claude and
  Codex session per Section, complete-paper assembly, or comments and reviews.
metadata:
  version: "1.11.1"
  last_updated: "2026-10-09"
  summary: "Paper owns the journey and composition; the shared Page owns each Paper Page's lifecycle and release."
---

# /haipipe-paper · compose a paper from evidence-bearing Pages

> ⛔ **Generated files: never modify them directly; change the code that writes them (or its source), then rerun it** (hard rule, JL 260928; AGENTS.md rule 6). For a paper that is its `delivery/` folder and every Page's `delivery/<lane>/`: fix the Page or the build code, then rebuild.
>
> ⛔ **No sha256 or other content hashes** (hard rule, JL 260928; AGENTS.md rule 9). A version is its number and date; staleness is file time or `git diff`. Never write, check or pin a hash.

`haipipe-paper` is the Paper-family router. It does not implement the Page
workflow and it does not replace the specialist Page Type contracts.

## 🪜 The ladder: Board · version · Task · Run

A paper is one Board; each send to a venue is a version Job; each Section, the
Abstract and each letter is a Page Task in that version; every Run is
`run-<type>-<target>` (b16 Q01, Q04, Q05). The contract is
[`ref/paper-ladder.md`](ref/paper-ladder.md); `scripts/paper_ladder.py` makes
each level (`board`, `version`, `next`, `spaces`, `task`, `run`, `rollback`).
Route a request by the level it names:

| Level | Folder | Its owners |
|---|---|---|
| Board | `Paper-<Slug>/`: face, `studio/`, `reports/`, `runs/`, `venues/`, `related/` | Story and Ideation (studio topics and Board Questions), Venue, Related through Discovery |
| version | `jNN_v<MMDD>_<desk>/`: face with `## Narrative` and `## Questions`, its Tasks, `delivery/` | the Section release (G3), comments reports, assembly and send (G4, G5) |
| Task | `t00_abstract` · `t0N_` Main · `t2N_` Appendix · `t3N_` letters | `haipipe-paper-section` over the shared Page workflow |
| Run | `runs/run-<type>-<target>/` (its `run.yaml`, ticket and `passes/`, as `haipipe-run` has it); a Section's are the Page engine's | the run cards, `haipipe-paper-workflow/ref/run-cards.md` |

Use two orders for two different jobs. First route the family request:

```text
haipipe-paper
  → haipipe-paper-workflow, when the question is the journey or a gate
  → resolve the concrete Page and its Page Type
```

When creating or updating a concrete Page, use the Page router's order:

```text
haipipe-page
  → haipipe-page-workflow
  → current Run Workflow / Run Spec owner
  → haipipe-paper-workflow (Folder-owning workflow)
  → the exact Page Type: haipipe-paper-ideation · haipipe-paper-story ·
    haipipe-paper-section · haipipe-paper-comments, or haipipe-paper-venue
  → Run Spec references / the Story's Section row and style policy
  → haipipe-run + selected workers, only where Runs exist
  → paper/haipipe-paper/ref/page-integration.md and ref/run-naming.md when a
    Paper-local Run or Page release is planned
```

For CONTEXT, OUTLINE, and EVIDENCE, the exact material contracts are
`workbench-page/ref/...` files. The Page surface already installs the
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
| Ideation | the idea pool as `studio/s01-ideation/` and Questions (group ideation); `haipipe-paper-ideation` |
| Story | each telling as `studio/sNN-story-<telling>/`, its research questions as Board Questions with reports, the Narrative; `haipipe-paper-story` |
| Venue | shared evidence-backed desk contract; `haipipe-paper-venue` |
| Section | reader-ordered manuscript unit and its wording/evidence; `haipipe-paper-section` |
| Comments | one batch of comments (a review, a meeting, a coauthor pass) and its answers; `haipipe-paper-comments` |

Use native receipts to report the current owner, accepted Result/version,
pending dependency and next human decision. Retargeting keeps Story identity,
binds the selected Venue and changes only the candidate telling in §8. Read the
exact PageType contract for its content rules; this router does not restate it.

`/haipipe-paper status` is a read-only rollup, not a Page Type or lifecycle.

## 🃏 Evidence and Page boundary

Paper Pages use the shared Page Face, Page Run, Evidence Item and Page CHECK
contracts. `haipipe-page` and `haipipe-page-workflow` own the lifecycle;
`workbench-page` presents typed CITE, VALUE and DISPLAY Results. Load
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
| give each Section Page its own session, or message the Section sessions | `/haipipe-paper sessions`: [`ref/section-sessions.md`](ref/section-sessions.md) and `scripts/create_section_sessions.py` |
| take in or answer one batch of comments (review, meeting, coauthor, advisor) | `haipipe-paper-comments` |
| check paper or one family's status | `/haipipe-paper status` (command, not a Page Type) |
| run one Page through its lifecycle | `haipipe-page-workflow` |
| compile or export one Page | `workbench-page`, using its LaTeX or Word lane |
| assemble the paper | `haipipe-paper-assemble` from the Section Pages' own `delivery/latex/` outputs and accepted bindings |
| respond to reviewers | `haipipe-paper-comments`: a comments report in the version that answers it, its Review Items routed to the Sections |
| start a paper, a version, a Section or a Run | `scripts/paper_ladder.py` (`board`, `version`, `next`, `task`, `run`) |

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
/haipipe-paper sessions [paper]        a named Claude session + Codex thread per
                                       Section (one for the Appendix), once §8
                                       fixes the Sections
/haipipe-paper comments <new|id>
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
| Page outline/evidence material | the relevant `workbench-page/ref/...` contract; presenter already installed |
| one Page export | `workbench-page` and the selected format reference |
| a display Evidence Item | `haipipe-display` and the chosen worker, through the Page RE Result contract |
| Paper board presentation | `workbench-paper`; `haipipe-page` owns rendering/checking |

### What the person sees · the Paper Workbench

A person who names a Workbench tab means its owner below. The link and the
screen's own rules are in `workbench-paper`.

| Level › Space › view | What it shows | Owner skill |
|---|---|---|
| Board › Description › Scope · Venue · Resources · Related | the face; `venues/<venue>/`; resources; one card per related item, opening on its deep read's drawing | `haipipe-paper` · `haipipe-paper-venue` · `haipipe-discovery` |
| Board › Idea Studio | the `studio/` topics, one drawing each | the base frame (`excalidraw-report`) |
| Board › Audience Report › Ideation | the ideation Questions and their `studio/s01-ideation/` work | `haipipe-paper-ideation` |
| Board › Audience Report › Narrative | what the story says, how it is drawn, how it is told, whether it attracts an editor, a reviewer, the public | `haipipe-paper-story` |
| Board › Audience Report › High-level logic + Low-level work | each research question: Question │ Work │ Report | `haipipe-paper-story`; the work in `haipipe-task`, `haipipe-discovery` |
| Board › Audience Report › Related Questions | the reviewer, coauthor, editor and reader questions | `haipipe-question` |
| Board › Work Details | the versions (and grants, slides) | `haipipe-paper` (`paper_ladder.py`) |
| version › Description › Version · Venue rules | the version face; the venue's call | `haipipe-paper` · `haipipe-paper-venue` |
| version › Audience Report › Questions · Draft-Main · Draft-Appendix | the standing J1–J5 and the version's Questions; each Section as Question │ Work │ Report, the rendered draft beside its drawing | `haipipe-question` · `haipipe-paper-story` (Narrative review, G3 release) |
| version › Audience Report › Comments · Cover letter | the Review Items of its comments reports; the letter, paragraph by paragraph | `haipipe-paper-comments` · `haipipe-paper-assemble` |
| version › Work Details › Main · Appendix · Letters | its Tasks | `haipipe-paper-section` |
| version › Delivery | one card per kind: manuscript, letters, checks, sent | `haipipe-paper-assemble` |
| Section › every Space | the Page Task's views, plus the reader contract, Requirement, Comments and "ready for the build" | `haipipe-paper-section` over the Page skills |
| any level › Runs | that level's own Runs, by run type | the run cards (`haipipe-paper-workflow`) |

Load only what the request uses. Reuse an already loaded owner; do not recurse
between the Paper router, Page router and domain adapter. Insight and Design
remain independent families, referenced through their own Results/contracts.

## 📐 Story boundary

`haipipe-paper-story` owns each telling's meaning (its studio topic and Board
Questions), the read-through test and the selected telling. Each Section binds
its row in its version face's `## Narrative` through `story-row:`. Read
`haipipe-paper-story/ref/integration.md` for the compile-order interface;
planning a Section does not instantiate its Page, authorize execution or imply
approval.

## 📂 Paper structure

Read [`ref/paper-ladder.md`](ref/paper-ladder.md) for the folder layout,
group and Section naming, compile-order markers, Task boundary, delivery law
and migration rules. The Paper router only resolves the structure owner; it does
not maintain a second naming or migration contract. In short: a version is `jNN_v<MMDD>_<desk>/` and its
Tasks are named by series, `t00_abstract` · `t0N_` Main · `t2N_` Appendix · `t3N_` letters; a comments
batch is a report of type comments, `reports/qNN_<kind>-<MMDD>/` (`scripts/carry_over/rename_tasks.py` renames an older
version once).

## 🧑‍💻 Section sessions

Once the Story's §8 compile order fixes the Sections, `/haipipe-paper sessions`
gives each Main Section Page, and the Appendix group as one unit, a named Claude
session and a named Codex thread (`<Short>-<unit>`, `<Short>-<unit>-Codex`),
pairs them, records both ids in the page header (`session:`, `codex-session:`),
and stops the Claude session after a read-only first turn so `/resume` can open
it. Plan first (no `--apply`), then create. Read
[`ref/section-sessions.md`](ref/section-sessions.md) for units, the scope rules
each session starts with, and how to message a session afterwards.

**A Section Run has two bookends (JL 260928).** In a Section session the author
says when a writing Run starts and when it is over. In between, only the
Section's Draft file changes: no log line, receipt, `results/` write, Page
Content or delivery. Rulings routed from another session go into the Draft the
same way. At the close the session writes the Run's records and one log entry
at once. When the author asks, it then adopts the Draft into Page Content and
runs the Section's delivery lanes: web page, then LaTeX, then Word.
`haipipe-paper-assemble` reads only what those lanes export, and it takes a
Section's approval from its newest draft version: while a Run works on a new,
unapproved version, the build lists that Section as not ready and prints only
its numbered placeholder, unless `paper-build.toml` sets
`draft_includes_unready = true`, which prints the Section's last export in a
DRAFT build. Contract: `haipipe-page-workflow/ref/interactive-writing-run.md` §🔖.

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

A telling's seed (identity, pitch, stakes) and its roadmaps live in its studio
topic, its research questions in Board Questions with reports, and its Section
Narrative in each version face's `## Narrative`; the corresponding execution,
Section, compile and comments records stay with their native owners. The router reads no retired child
Page, compatibility alias, or fallback source.

## ✅ Completion checks

Before reporting Paper work complete, identify the active Page owner, Run Spec,
Story §8 row, accepted evidence/display Results, current Page CHECK versions,
assembly manifest and G4 status. Keep DRAFT, blocked, deferred and human-owned
decisions explicit. A discussion or planning handoff does not create a Run,
release a Section or close G4. Use the owning Page, Workflow, Assembly, Venue
and submission references for detailed checks.

## 📂 Family boundary

See [`../README.md`](../README.md) for the family index. This door owns Paper
routing and composition; Page, Workflow, Run, Evidence, Display, Board, Venue
and Assembly owners retain their own contracts.
