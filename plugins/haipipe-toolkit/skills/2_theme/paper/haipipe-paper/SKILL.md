---
name: haipipe-paper
description: "The one door for a paper on the ladder: a paper Board, one version Job per send, one Task per Section, Abstract or letter; routes to the Story, Ideation, Venue, Section, comments and assembly owners. Use for paper setup (paper_ladder.py), bringing an older paper folder onto the latest layout (paper_ladder.py audit, update), where a paper stands (checklist.md, paper_check.py, its sNN-paper-checklist topic), the delivery and its requirements, drafting, or reviews. Trigger: paper, paper Board, version, send, update the paper folder, paper checklist, delivery requirements, /haipipe-paper."
metadata:
  version: "1.20.1"
  last_updated: "2026-11-01"
  summary: "Paper owns the journey and composition; the shared Page owns each Paper Page's lifecycle and release."
---

# /haipipe-paper · compose a paper from evidence-bearing Pages


> ⛔ **Generated files: never modify them directly; change the code that writes them (or its source), then rerun it** (hard rule, JL 260928; AGENTS.md rule 6). For a paper that is its `delivery/` folder and every Page's `delivery/<lane>/`: fix the Page or the build code, then rebuild.
>
> ⛔ **No sha256 or other content hashes** (hard rule, JL 260928; AGENTS.md rule 9). A version is its number and date; staleness is file time or `git diff`. Never write, check or pin a hash.

`haipipe-paper` is the Paper-family router. It does not implement the Page
workflow and it does not replace the specialist Page Type contracts.

## 🧭 Four layers: plan, explore, evidence, writing (JL 261031; b16-s01-paper-tree-concept)

**One paper Block links many discovery Blocks (external information) and work Blocks (internal information), deposits them into its evidence Jobs, and writes them into papers in its writing Jobs** (JL 261031).

```text
plan       the paper Board          the idea, the story, the venue, data flow, paper flow, related work (its sNN topics)
explore    internal: work Blocks    datasets and regressions on raw data
           external: discovery      papers and sources, each read by a Run
evidence   j02_evidence_value       the printed numbers, one Task per group   ← internal Results
           j03_evidence_cite        the citations, one Task per claim group   ← external, verified CITE Results
           j01_evidence_display     figures and tables (t01-t19 main, t51-t59 appendix), drawn from internal Results
writing    j11_writing_v<MMDD>_<desk>, j12_writing_…   one Job per send: its Sections quote the evidence
```

The evidence is independent of the writing and of the venue (JL 261031: "evdience might identipatnet to the paper
writing and the venue"), so its Jobs sit beside the writing Jobs, never inside one: a resend reuses them as they are;
a venue's style is applied when the paper is built. An evidence Task reads returned, aggregated Results only, never
raw data, so the paper folder stays safe to share; computing stays in work. `paper_ladder.py evidence <board>` makes
the three evidence Jobs; `version` and `next` number the writing Jobs from j11. An older `jNN_v<MMDD>_<desk>` version
still reads.

## ✅ Where a paper stands: `checklist.md`

JL 261031: "here we should also try to add the checklist.md, so everytime, the haipipe-paper we can have the things like check the progress"; JL 261101: "what is the final checklist we should have? what is the delivery, and what is the delivery requirements"; "make the checklist to be a sNN as well". [`checklist.md`](checklist.md) lists what a paper needs, from its question to the send: ⓪ Layout L1-L5, ① Plan P1-P8, ② Explore E1-E3, ③ Evidence V1-V5, ④ Writing W1-W5, ⑤ Delivery D1-D9. `scripts/paper_check.py <Paper-Board>` ticks every line a file can prove (✅ done, ⏳ under way, ⬜ not yet, 🙋 waits on a person). Run it whenever someone asks where a paper stands, and answer from its lines.

```text
paper_check.py <Board>            print the checklist; change nothing
paper_check.py <Board> --write    also tick it into sNN-paper-checklist/ below its GENERATED line
```

**The checklist is a topic.** Each paper Board keeps it as `sNN-paper-checklist/` (s05 when free, the concept band): the face's head (Decided, Open) is the person's; below its GENERATED line is `paper_check.py --write`'s, rerun, never edited.

**The delivery and its requirements (⑤).** One send hands over the manuscript (PDF and Word), the supplement when the venue takes one, the cover letter, the venue's own files (its author kit) and the receipt, `delivery/<writing Job>/build-manifest.json`. Each D line names where its rule lives and never copies it: haipipe-paper-assemble's Required outputs (D1-D3), `venues/<venue>/call.md` (D4: words, desk rules, the venue's own build profile), AGENTS.md § Papers (D5: no process text), haipipe-paper-evidence (D6), `ref/submission-readiness.md` (D7 the build's blockers, D8 the human reading pass), haipipe-delivery (D9: only a person writes `sent` in `delivery/delivery.md`).

## 🔄 Bring an older paper folder up to date: `audit` and `update`

JL 261101: "the /haipipe-paper need to have the update, so you can update the existing paper folder to the latest version". `paper_ladder.py audit <Board>` prints the ⓪ Layout lines; `paper_ladder.py update <Board> [--date MMDD]` prints, as a dry run, the steps that fix each failing line; `--apply` does them, in order, and stops at the first that fails:

```text
L1 old Pages (A1-Story/, B*-/)     carry_over/migrate_paper.py, topics_paper.py, then sweep_names.py
L2 undated versions, S-… Sections  carry_over/rename_tasks.py --date MMDD
L3 jNN_v<MMDD>_<desk>/             renamed jNN_writing_v<MMDD>_<desk>/ (from j11; a number of 11 or more kept), its face,
                                   its delivery/<job>/ folder and build inputs too, the whole name swept
V1 missing evidence Jobs           paper_ladder.py evidence
L4 no checklist topic              sNN-paper-checklist/ (haipipe-studio new_topic.py --over-limit), then paper_check.py --write
L5 faces the views read            🙋 not mechanical: haipipe-paper-story (T, D tables), haipipe-paper-plan (-drawing.yaml)
```

Every carry-over step keeps its own rollback; nothing is committed. Update also removes an empty leftover `A1-Story/`
or `studio/` folder. Each step's title names the step, never a count.

**Undo, newest first.** `paper_ladder.py rollback <Board>` undoes the evidence Jobs step; then `paper_ladder.py update
<Board> --rollback` undoes the renames and sweeps, from the record `.ladder-undo/update-N/`. To undo the checklist
topic, delete its `sNN-paper-checklist/` folder. Run update in the paper's own session (one session per Project), dry run first, and show the person the dry run before `--apply`. A subagent, or any session that does not own the paper, stops at the dry run and reports it.

## 🪜 The ladder: Board · version · Task · Run

A paper is one Board; each send to a venue is a writing Job (a version); each Section, the
Abstract and each letter is a Page Task in that version; every Run is
`run-<type>-<target>` (b16 Q01, Q04, Q05). The contract is
[`ref/paper-ladder.md`](ref/paper-ladder.md); `scripts/paper_ladder.py` makes
each level (`board`, `version`, `next`, `spaces`, `task`, `run`, `rollback`).
Route a request by the level it names:

| Level | Folder | Its owners |
|---|---|---|
| Board | `Paper-<Slug>/`: face, its topics `sNN-<topic>/` beside the Jobs (no `studio/` folder), `reports/`, `runs/`, `venues/`, `related/`, `delivery/` | Story and Ideation (studio topics and Board Questions), Venue, Related through Discovery |
| evidence | `j01_evidence_display/`, `j02_evidence_value/`, `j03_evidence_cite/`: one Task per display, value group or claim group | haipipe-paper-evidence (rules), haipipe-display (drawing) |
| version (writing) | `j11_writing_v<MMDD>_<desk>/` (older `jNN_v<MMDD>_<desk>/`): face with `## Narrative` and `## Questions`, its Tasks; output in Block `delivery/<version>/` | the Section release (G3), comments reports, assembly and send (G4, G5) |
| Task | `t00_abstract` · `t0N_` Main · `t2N_` Appendix · `t3N_` letters | `haipipe-paper-draft` over haipipe-draft's seven steps (below) |
| Run | `runs/run-<type>-<target>/` (its `run.yaml`, ticket and `passes/`, as `haipipe-run` has it); a Section's are the Page engine's | the run cards, `haipipe-paper-workflow/ref/run-cards.md` |

Use two orders for two different jobs. First route the family request:

```text
haipipe-paper
  → haipipe-paper-workflow, when the question is the journey or a gate
  → resolve the concrete Page and its Page Type
```

When creating or updating a concrete Page, use the Page router's order:

```text
haipipe-draft
  → haipipe-draft-workflow
  → current Run Workflow / Run Spec owner
  → haipipe-paper-workflow (Folder-owning workflow)
  → the exact Page Type: haipipe-paper-ideation · haipipe-paper-story ·
    haipipe-paper-draft · haipipe-paper-comments, or haipipe-paper-venue
  → Run Spec references / the Story's Section row and style policy
  → haipipe-run + selected workers, only where Runs exist
  → paper/haipipe-paper/ref/page-integration.md and ref/run-naming.md when a
    Paper-local Run or Page release is planned
```

For CONTEXT, OUTLINE, and EVIDENCE, the exact material contracts are
`workbench-task-draft/ref/...` files. The Page surface already installs the
shared Outline presenter; it is not a final execution dependency.

Read [`ref/page-integration.md`](ref/page-integration.md) for the Paper-specific
consequences of the shared Page contract. This router owns no second Page
lifecycle, Page Run namespace, Evidence Workspace, or Page release protocol.

`haipipe-paper-assemble` is a separate complete-paper verb after routing; it has its own bounded compile Spec in the Paper Workflow.

### A Section, step by step (b32 s41, on screen 2026-10-20)

A Section Task is a draft Task (`task-type: draft`), worked in haipipe-draft's seven steps. Its Work shows the five
middle steps as views (1 Plan to 5 Revise; Display only when the Section calls or makes a display); Studio and
Delivery are the top row's. The paper adds its own owner to four of the steps:

| Step (tab) | In a paper | Owner |
|---|---|---|
| 🎨 Studio | the Board's topics that name the Section (its story s02, its plan s04 rows) | haipipe-studio · haipipe-paper-story · haipipe-paper-plan |
| 📐 1 · Plan | §1 from the Section's contract (the face's reader-question … transition-out, from the version's `## Narrative` row); your Scratch, a note per paragraph; the venue's SUB-* rows beside the Requirement | haipipe-draft-logic · haipipe-paper-draft |
| ✍️ 2 · Write | `## 3 · Draft` from §1 and its Scratch, the desk's sentence and word limits; you type in its boxes too | haipipe-paper-draft · haipipe-draft-writing |
| 🔎 3 · Evidence | `evidence/cards.yaml` under the paper's rules (CITE from verified Results, one number everywhere); the prompt is `/haipipe-paper-evidence <task>` | haipipe-paper-evidence |
| 🖼 4 · Display | the Section's Tables and Figures, `display/Display<n>-<slug>/`, numbered for the paper (`label: Table 1`) and within the venue's limit | haipipe-display · haipipe-paper-evidence |
| 🔁 5 · Revise | Revise cards, then comments' Review Items routed to the Section | haipipe-draft-writing · haipipe-paper-comments |
| 📤 Delivery | the Section's lanes in `delivery/jNN_<version>/<tNN>/`; ◆ ready for the build | haipipe-delivery · haipipe-paper-assemble |

The version's Work shows each Section as one row with its five step words (Plan, Write, Evidence, Display, Revise;
`focus_draft.WORK`), each saying its state (done, next, sign, asked, send, optional, pass k, later) and opening that
step (`paper_version.section_row`).

## Paper Workflow and content owners

A Paper Workflow is the `paper-runs` layer: a list of bounded owner-native
Runs. Read
`haipipe-paper-workflow/ref/run-workflow.md` for Specs, dependencies and G0–G5;
Page containers, status reads and gate records do not allocate Runs.

| Owner | Paper responsibility |
|---|---|
| Ideation | the idea pool as `s01-ideation/` and Questions (group ideation); `haipipe-paper-ideation` |
| Related work | the closest work: `s10-related-work-map/` maps it beside ours, `s11`-`s19` read one type each; `haipipe-paper-related` |
| Story | each telling as `sNN-story-<desk>-<idea>/` in the Board folder, its research questions as Board Questions with reports, the Narrative; `haipipe-paper-story` |
| Plan | after the story: `s03-paper-dataflow/` (how the data becomes each answer) and `s04-paper-workflow/` (the Sections, displays and dates to the send); `haipipe-paper-plan` |
| Venue | shared evidence-backed desk contract; `haipipe-paper-venue` |
| Section (draft) | one Section, the Abstract or a letter, a draft Task: its plan and sentences in `draft/`; `haipipe-paper-draft` (was haipipe-paper-section) |
| Evidence | what backs each Section (`evidence/`, `display/`) and one ledger per version: citations, one number per result, displays; `haipipe-paper-evidence` |
| Comments | one batch of comments (a review, a meeting, a coauthor pass) and its answers; `haipipe-paper-comments` |

Use native receipts to report the current owner, accepted Result/version,
pending dependency and next human decision. Retargeting keeps Story identity,
binds the selected Venue and changes only the new writing Job's `## Narrative`. Read the
exact PageType contract for its content rules; this router does not restate it.

`/haipipe-paper status` is a read-only rollup, not a Page Type or lifecycle.

## 🃏 Evidence and Page boundary

Paper Pages use the shared Page Face, Page Run, Evidence Item and Page CHECK
contracts. `haipipe-draft` and `haipipe-draft-workflow` own the lifecycle;
`workbench-task-draft` presents typed CITE, VALUE and DISPLAY Results. Load
[`ref/page-integration.md`](ref/page-integration.md) for the Paper-specific
ownership, release, source/projection and Run boundaries, and
[`ref/run-naming.md`](ref/run-naming.md) for Paper context and identities.

Supporting Task/Discovery Runs retain their native owners. A Page-local Result
is the evidence authority for the Page; assembly may copy accepted artifacts
but never becomes a wording or evidence source.

For visual displays, load `haipipe-display`; its concept-first gate owns
composition references, editable reconstruction and candidate promotion.

**The paper Board holds the evidence; work and discovery Blocks create it** (JL 261022: "for /haipipe-paper, we should
have a paper block and a work block to provide the displays and E-work, right?"; JL 261031, the four layers above).
Work Blocks `work/bNN_.../` hold the Runs that make every number and every underlying table on raw data; the paper
Board's evidence Jobs deposit them: `j01_evidence_display` (one Task per display, each picture or table drawn by its
own Run from returned, aggregated Results), `j02_evidence_value`, `j03_evidence_cite`. Until 261031 the display Job sat
in the work Block (`j21_paper_displays`, `j21_<venue>_displays`); an older Project keeps it there until it is moved. The display Job opens with a **display plan** the authors agree before anything is
drawn (JL 261023: "this should be a plan, proposed to the author to think about how to draw them"): one row per
display with its number, title, the one question it answers, its layout (rows, columns or axes), its source Runs
and its open choices, written from the team's own record (meeting notes, slides) in the Job face. The Sections write
their numbers only after the drawn displays pass review and are accepted, so a sentence never describes a table
that is still changing. A paper display unit only frames that Run's picture (question, caption, legend, number,
size, review); no paper folder runs analysis or plotting code. The version face (or `board.md`) names the Block in a
`work-block:` line. The rules are haipipe-paper-evidence's rule 3.

## 🚪 Routing

Resolve the paper root and target Page before changing anything.

| User intent | Route |
|---|---|
| brainstorm, novelty-check, compare or select ideas | `haipipe-ideation` and only its relevant specialist; use `haipipe-paper-ideation` when a Paper Page projection is involved |
| create, refresh, read or check the Paper Idea portfolio Page | `haipipe-draft` + `haipipe-draft-workflow` + `haipipe-paper-ideation`; load the semantic owner for sync/handoff |
| ask where a paper is in the journey, or test a gate | `haipipe-paper-workflow` |
| draft or review the whole paper, its research roadmaps or section narrative | `haipipe-paper-story` |
| plan the data flow or the paper flow (s03, s04): which Run feeds which question, which Section answers it, the displays, the dates to the send | `haipipe-paper-plan` |
| release work, inspect execution progress, accept a receipt, or release a Section | `haipipe-paper-workflow` plus the exact Discovery/Task/Section owner; use Story for the resulting paper meaning |
| inspect or record a target venue | `haipipe-paper-venue` (shared reference library) |
| write or revise one manuscript/appendix unit | `haipipe-paper-draft`, one step at a time (A Section, step by step) |
| check a Section's or a version's evidence, citations, numbers or displays | `haipipe-paper-evidence` |
| give each Section Page its own session, or message the Section sessions | `/haipipe-paper sessions`: [`ref/section-sessions.md`](ref/section-sessions.md) and `scripts/create_section_sessions.py` |
| take in or answer one batch of comments (review, meeting, coauthor, advisor) | `haipipe-paper-comments` |
| check paper or one family's status | `/haipipe-paper status` (command, not a Page Type) |
| run one Page through its lifecycle | `haipipe-draft-workflow` |
| compile or export one Page | `workbench-task-draft`, using its LaTeX or Word lane |
| assemble the paper | `haipipe-paper-assemble` from the Section Pages' own `delivery/latex/` outputs and accepted bindings |
| respond to reviewers | `haipipe-paper-comments`: a comments report in the version that answers it, its Review Items routed to the Sections |
| start a paper, a version, a Section or a Run | `scripts/paper_ladder.py` (`board`, `version`, `next`, `task`, `run`) |
| bring an older paper folder onto the latest layout | `scripts/paper_ladder.py audit`, `update [--date MMDD] [--apply]` |
| where a paper stands, and its delivery | `checklist.md`, `scripts/paper_check.py <Board> [--write]`, the Board's `sNN-paper-checklist/` |

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
                                       Section (one for the Appendix), once the
                                       writing Job's ## Narrative fixes them
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
| a concrete Page | `haipipe-draft` + `haipipe-draft-workflow` + its exact Paper PageType |
| Page outline/evidence material | the relevant `workbench-task-draft/ref/...` contract; presenter already installed |
| one Page export | `workbench-task-draft` and the selected format reference |
| a display Evidence Item | `haipipe-display` and the chosen worker, through the Page RE Result contract |
| Paper board presentation | `workbench-paper`; `haipipe-draft` owns rendering/checking |

### What the person sees · the Paper Workbench

A person who names a Workbench tab means its owner below. The link and the
screen's own rules are in `workbench-paper`.

| Level › Space › view | What it shows | Owner skill |
|---|---|---|
| Studio › Related (folded under the topics, the Board's) | `related/related.md`, one row per item, grouped by its subfolder (meetings · papers · files · emails) and then its `group` cell, opening on its file; by question in Report › Related Papers | `haipipe-related` · `haipipe-paper` · `haipipe-discovery` |
| Studio (top row, the Board's) | the Board's `sNN-<topic>/` folders, one drawing each, with Tags and Stage | the base frame (`haipipe-studio`) |
| Delivery (top row, the Board's) | `delivery/jNN_<version>/`, one per version; from a version, its part | `haipipe-paper-assemble` · `haipipe-delivery` |
| Board › Report · Work (focus page, `layout=focus`) | seven views, A Idea · B Story (the venues inside, `venues/<venue>/call.md`) · C Data flow · D Paper flow · E Support blocks · F Evidence · G Writing; Report reads RESULTS first, Work PROCESS first | `haipipe-paper-ideation` · `haipipe-paper-story` · `haipipe-paper-venue` · `haipipe-paper-plan` · `haipipe-paper-evidence` · `haipipe-paper` (`paper_ladder.py`) |
| Board › Description › Scope · Venue · Resources (frame layout only; on the focus page the venues sit in B Story) | the face; `venues/<venue>/`; resources | `haipipe-paper` · `haipipe-paper-venue` |
| Board › Audience Report › Ideation · Narrative · High-level logic + Low-level work · Related Questions · Related Papers (frame layout) | the ideation Questions; the story; each research question as Question │ Work │ Report; the reviewer and reader questions; the related papers by question | `haipipe-paper-ideation` · `haipipe-paper-story` · `haipipe-report` |
| version › Description › Version · Venue rules (frame layout) | the version face; the venue's call | `haipipe-paper` · `haipipe-paper-venue` |
| version › Work › Draft-Main · Draft-Appendix · Display-Main · Display-Appendix · Values · Citations | each Section a row with its five step words, each opening that step; the evidence Jobs' Tasks | `haipipe-paper-draft` over `haipipe-draft`'s steps · `haipipe-paper-evidence` |
| version › Audience Report › Questions · Draft-Main · Draft-Appendix · Comments · Cover letter (frame layout) | the standing J1-J5 and the version's Questions; each Section as Question │ Work │ Report; the Review Items of its comments reports; the letter, paragraph by paragraph | `haipipe-paper-comments` · `haipipe-paper-assemble` |
| Section › Work › 1 Plan · 2 Write · 3 Evidence · 4 Display · 5 Revise | each step, Operation (Input, Sign, Prompt) over Result; the SUB-* rows in 1 Plan; Display only when the Section has one | `haipipe-draft` (the seven steps) · `haipipe-paper-draft` · `haipipe-paper-evidence` |
| Section › Report · Description · Delivery | the steps' Results, Table, Questions, Comments; the reader contract; ◆ ready for the build | `haipipe-paper-draft` · `haipipe-paper-comments` |
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
not maintain a second naming or migration contract. In short: the evidence Jobs are `j01_evidence_display/`, `j02_evidence_value/`, `j03_evidence_cite/`; a version is a
writing Job `j11_writing_v<MMDD>_<desk>/` (older: `jNN_v<MMDD>_<desk>/`) and its
Tasks are named by series, `t00_abstract` · `t0N_` Main · `t2N_` Appendix · `t3N_` letters; a comments
batch is a report of type comments, `reports/qNN_<kind>-<MMDD>/` (`scripts/carry_over/rename_tasks.py` renames an older
version once).

## 🧑‍💻 Section sessions

Once the compile order in the writing Job face's `## Narrative` fixes the Sections, `/haipipe-paper sessions`
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
DRAFT build. Contract: `haipipe-draft-workflow/ref/interactive-writing-run.md` §🔖.

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
the Section's row in its writing Job face's `## Narrative`, accepted evidence/display Results, current Page CHECK versions,
assembly manifest and G4 status. Keep DRAFT, blocked, deferred and human-owned
decisions explicit. A discussion or planning handoff does not create a Run,
release a Section or close G4. Use the owning Page, Workflow, Assembly, Venue
and submission references for detailed checks.

## 📂 Family boundary

See [`../README.md`](../README.md) for the family index. This door owns Paper
routing and composition; Page, Workflow, Run, Evidence, Display, Board, Venue
and Assembly owners retain their own contracts.
