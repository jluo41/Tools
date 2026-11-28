---
name: hai-paper
description: "The router for the Paper family (manuscript and grant Boards): a paper Board, one version Job per send, one Task per Section. Use for paper setup, updating an older paper folder or the submission portal. Trigger: paper, paper Board, grant proposal, submission portal, writing lab, /hai-paper."
metadata:
  version: "1.41.0"
  last_updated: "2026-11-24"
  summary: "Paper owns the journey and composition; the shared Page owns each Paper Page's lifecycle and release."
---

# /hai-paper · compose a paper from evidence-bearing Pages


> ⛔ **Generated files: never modify them directly; change the code that writes them (or its source), then rerun it** (hard rule, JL 260928; the SPACE's AGENTS.md § Working rules). For a paper that is its `delivery/` folder and every Page's `delivery/<lane>/`: fix the Page or the build code, then rebuild.
>
> ⛔ **No sha256 or other content hashes** (hard rule, JL 260928; the SPACE's AGENTS.md § Working rules). A version is its number and date; staleness is file time or `git diff`. Never write, check or pin a hash. The two exceptions, decided 2026-11-15: hai-insight's receipt `tables_sha256` (rerun compare) and hai-design's `method-sha` and inputs `manifest.yaml` sha256 (the Job fence); nothing else pins a hash.
>
> ⛔ **Must-check before JL sees it** (hard rule, JL 261115: "make them into the skills of /hai-paper, and ask them to be must check them"). [`ref/must-check.md`](ref/must-check.md) holds every paper rule JL has already given, each with its check. Before JL sees a Section, before a Section closes and before a send, run its gate: `auto` rules by script, `read` rules by a fresh reviewer that did not write the text; fix a failure or name its id and reason. A correction JL gives, directly or relayed by another session, changes that file in the same change as the fix; a rule already there means its check was too weak, so strengthen the check.

`hai-paper` is the Paper-family router. It does not implement the Page
workflow and it does not replace the specialist Page Type contracts.

## From an Idea Job

New research portfolios live in an Idea Block, `paper/Idea-<Slug>/` beside the Paper and Grant Boards (JL 261124:
"No more ideation theme"): one direction, one Job per idea, evaluation Tasks within it. `hai-ideation` owns the scientific Card,
assessments and human selection. This router creates/binds the linked Paper
from the selected handoff; it keeps the source Job and its history in place.
Normally each selected Job has its own Paper Block. Paper Jobs still mean
versions/evidence/submission work, not candidate ideas.

Read [the source adapter](../hai-paper-ideation/ref/idea-job-source.md)
for reciprocal links and repeat-safe binding. An explicit early Paper request
may precede selection, but an unbound sync packet alone does not create one.
Legacy Paper-local portfolios remain readable without migration.

## Paper types and shared content

Paper is the theme family. The manuscript-oriented Paper Board and Grant Board
are types within it. Grant uses the same planning, evidence, writing-version,
review and assembly contracts, with the funding call supplying its application
requirements. Do not create a separate Grant theme or parallel lifecycle.

Grant shares Idea, Story and Data + Paper Plan, including Related in both Idea
and Story and Story by Section in both Story and Displays. Funding opportunity,
specific aims, research approach, team, budget and submission requirements extend
that shared structure. For Grant, Venues means the funding program or call;
Paper flow means the application narrative and sections. Keep preliminary
findings distinct from proposed future outcomes.

| Content | Semantic owner | Workbench placement |
|---|---|---|
| Candidate idea and its theory | hai-ideation owns the source Job; [hai-paper-ideation](../hai-paper-ideation/SKILL.md) owns its Paper projection | Idea |
| Related-work positioning | [hai-paper-related](../hai-paper-related/SKILL.md); records remain owned by hai-related | Related in Idea and Story |
| Chosen argument and Section Narrative | [hai-paper-story](../hai-paper-story/SKILL.md) | Story; the same Story by Section also appears in Displays |
| Data flow, application/paper flow and display plan | [hai-paper-plan](../hai-paper-plan/SKILL.md) | Data + Paper Plan; Displays |
| Target requirements | [hai-paper-venue](../hai-paper-venue/SKILL.md) | Venues; Grant design also has Opportunity |
| Returned values, citations and display evidence | [hai-paper-evidence](../hai-paper-evidence/SKILL.md) | Evidence and Displays |
| Section drafts and assembled outputs | [hai-paper-draft](../hai-paper-draft/SKILL.md), [hai-paper-assemble](../hai-paper-assemble/SKILL.md) | Writing and Delivery |
| Reading and rendering these records | [workbench-paper](../workbench-paper/SKILL.md) | Shared Paper frame |

**A grant Board is `Grant-<Slug>/`** (JL 261112: "It should not be a Paper-xxx, it should be Grant-xxxx"). It sits
in the Project's `paper/` beside the Paper Boards. `paper_ladder.py board <paper/>Grant-<Slug>` writes its face
with `board-kind: grant-board` and `use-case: Initial application`; `version`, `task`, `evidence`, `submission` and
`paper_check.py` then work on it as on a Paper Board. The code that finds a paper Board by its name accepts both
prefixes (hai-draft `common.py`, hai-project `ladder.py`, the workbench `address_links.py`, the evidence
scripts). First example: `<examples world>/Project-<Name>/paper/Grant-<Slug>/` (an LOI).

**Implementation boundary:** the Grant scaffold is implemented; there is no Grant renderer of its own (the
workbench shows a grant Board with the paper views) and no grant-specific Section template or submission adapter
yet. A Grant Section Task uses the manuscript Section template; the call's content items live in
`venues/<call>/call.md`. A matrix entry does not by itself authorize migrating an existing grant folder or
submitting an application.

## 🧭 Four layers: plan, explore, evidence, writing (JL 261031; b16-s01-paper-tree-concept)

**One paper Block links many discovery Blocks (external information) and work Blocks (internal information), deposits them into its evidence Jobs, and writes them into papers in its writing Jobs** (JL 261031).

```text
plan       the paper Board          the idea, the story, the venue, data flow, paper flow, related work (its sNN topics)
explore    internal: work Blocks    datasets and regressions on raw data
           external: discovery      papers and sources, each read by a Run
evidence   j02_evidence_value       the printed numbers, one Task per group   ← internal Results
           j03_evidence_cite        the citations, one Task per claim group   ← external, verified CITE Results
           j01_evidence_display     figures and tables (tNN_display-<letter>-<slug>), drawn from internal Results
writing    j11_writing_v<MMDD>_<desk>, j12_writing_…   one Job per send: its Sections quote the evidence
submission j21_submission_v<MMDD>_<desk>   one per send (face `for: <writing Job>`): t01_cover-letter, the walk of
           the venue's portal (every step and field), and the portal fill page to review and paste
```

The evidence is independent of the writing and of the venue (JL 261031: "evdience might identipatnet to the paper
writing and the venue"), so its Jobs sit beside the writing Jobs, never inside one: a resend reuses them as they are;
a venue's style is applied when the paper is built. An evidence Task reads returned, aggregated Results only, never
raw data, so the paper folder stays safe to share; computing stays in work. `paper_ladder.py evidence <board>` makes
the three evidence Jobs; `version` and `next` number the writing Jobs from j11. An older `jNN_v<MMDD>_<desk>` version
still reads.

## ✅ Where a paper stands: `checklist.md`

JL 261031: "here we should also try to add the checklist.md, so everytime, the hai-paper we can have the things like check the progress"; JL 261101: "what is the final checklist we should have? what is the delivery, and what is the delivery requirements"; "make the checklist to be a sNN as well". [`checklist.md`](checklist.md) lists what a paper needs, from its question to the send: ⓪ Layout L1-L6, ① Plan P1-P9, ② Explore E1-E3, ③ Evidence V1-V11, ④ Writing W1-W7, ⑤ Delivery D1-D11. `scripts/paper_check.py <Paper-Board>` ticks every line a file can prove (✅ done, ⏳ under way, ⬜ not yet, 🙋 waits on a person). Run it whenever someone asks where a paper stands, and answer from its lines.

```text
paper_check.py <Board>            print the checklist; change nothing
paper_check.py <Board> --write    also tick it into sNN-paper-checklist/ below its GENERATED line
```

**The checklist is a topic.** Each paper Board keeps it as `sNN-paper-checklist/` (s05 when free, the concept band): the face's head (Decided, Open) is the person's; below its GENERATED line is `paper_check.py --write`'s, rerun, never edited.

**The delivery and its requirements (⑤).** One send hands over the manuscript (PDF and Word), the supplement when the venue takes one, the cover letter, the venue's own files (its author kit) and the receipt, `delivery/<writing Job>/build-manifest.json`. Each D line names where its rule lives and never copies it: hai-paper-assemble's Required outputs (D1-D3), `venues/<venue>/call.md` (D4: words, desk rules, the venue's own build profile), AGENTS.md § Papers (D5: no process text), hai-paper-evidence (D6), hai-paper-assemble's portal packet (D8: `delivery/<writing Job>/portal/`, the files uploaded to the venue's portal as they are, one row per slot in `portal.md`), § The submission Job below (D9: the portal fill page), `ref/submission-readiness.md` (D7 the build's blockers, D10 the human reading pass), hai-delivery (D11: only a person writes `sent` in `delivery/delivery.md`).

**What goes into the portal: `delivery/<writing Job>/portal/`** (JL 261102: "here we might want to say the final delivery content that are ready to submit directly in the portal"). paper-build.toml `[portal]` lists each upload slot the venue's portal asks for (manuscript, supplement, one file per figure, cover letter, source ZIP, forms) and the built file that fills it; the build copies them into `portal/` and writes `portal/portal.md` with each slot's state (✅ ready, 🔶 built, not approved, ❗ stale, ⬜ missing). Upload exactly those files; list the slots that have no file yet too, so a missing form shows. The cover letter is a letter Task, built by the cover letter lane (`[coverletter]`, its `task =` naming the Task), never a Word file kept by hand.

**The submission Job: the portal, reviewed before anyone submits** (JL 261102: "you should have a new job to go through the whole portal and then create a delviery of html, and prefill the values for us"; "pelae don't submit, I just want to review the content"). Each send has one `j21_submission_v<MMDD>_<desk>/` (face `for: <writing Job>`): `t01_cover-letter` (the letter's words), `t02_portal-walk` (a Run that reads every step of the venue's portal draft, read only, into `portal-fields.yaml`: each field, its options, what the draft holds) and `t03_portal-fill` (`portal-values.yaml`, each field's value as text, a packet file, or `from_tex:` a built Section, then a Run writes `delivery/<submission Job>/portal-fill.html`: one card per field with a Copy button and its state, ✅ already in the draft, ✏️ paste, 📎 upload, 🙋 a person decides, ❗ the portal and the manuscript disagree). The paper workbench shows it as the assembled paper's tab "The submission portal". An agent never types into the portal, never ticks a declaration and never presses Submit: a person pastes and a person submits.

**It is shipped: a paper's Job holds only its values** (JL 261103: "you should also prepare the submission portal materials as well, like the cover letter, what content to fill in the submission portal"). No paper writes its own generator.

```text
paper_ladder.py submission <Board> --date MMDD [--for <writing Job>] [--desk <desk>] [--venue <venues folder>] [--dry-run]
    makes j21_submission_v<MMDD>_<desk>/: face, t01_cover-letter, t02_portal-walk, t03_portal-fill, starter yaml, tickets;
    seeds each field's `says` from venues/<venue>/call.md, each upload from the writing Job's [portal], title and words
    from the build; `rollback` undoes it
scripts/portal_fill.py <submission Job>     what t03's ticket runs: portal-fields.yaml + portal-values.yaml + the build
    → delivery/<submission Job>/portal-fill.html, and the Run's result/ receipt
```

A paper keeps `t02`'s walk and `t03_portal-fill/portal-values.yaml`, nothing else; `src/gen_portal_fill.py` in an older Job is retired by pointing its ticket at `portal_fill.py` (the page comes out the same). A value is `value:`, `file:` (under `delivery/<writing Job>/`), `from_tex:` (a built Section's Task), `ask:`, `disagree: true`, `check:` and `note:`; the full list is the script's docstring. A file not built yet shows ⬜ no file yet, a sixth state, never ✏️ or 📎.

**❗ comes from what the build records, never a guess.** `check: title|words|tables|figures|references` compares the value, and the portal's `now`, with the build (the title as `declared_title` reads it, `build-manifest.json` for the counts); a packet file the build calls stale is ❗ too. What only a reading can show (an account's old email) is `disagree: true` with a `note:`. With no build the card says "Not checked".

**The walk stays a person-started Run.** `t02_portal-walk/runs/r01_read_portal/` starts as a seeded starter, marked STARTER, so D9 stays ⏳ until a real walk replaces it: a person logs in and opens the draft; an agent then reads each step, read only, into `result/portal-fields.yaml`, as its ticket says. Neither script logs in, opens a browser or reaches the network. The letter's words stay in the writing Job's `t31_cover-letter` when it has one (`t01_cover-letter` then only points there with `words-in:`); otherwise they live in `t01_cover-letter`, which the build finds by the Job's `for:` line.

## 🔄 Bring an older paper folder up to date: `audit` and `update`

JL 261101: "the /hai-paper need to have the update, so you can update the existing paper folder to the latest version". `paper_ladder.py audit <Board>` prints the ⓪ Layout lines; `paper_ladder.py update <Board> [--date MMDD]` prints, as a dry run, the steps that fix each failing line; `--apply` does them, in order, and stops at the first that fails:

```text
L1 old Pages (A1-Story/, B*-/)     carry_over/migrate_paper.py, topics_paper.py, then sweep_names.py
L2 undated versions, S-… Sections  carry_over/rename_tasks.py --date MMDD
L3 jNN_v<MMDD>_<desk>/             renamed jNN_writing_v<MMDD>_<desk>/ (from j11; a number of 11 or more kept), its face,
                                   its delivery/<job>/ folder and build inputs too, the whole name swept
V1 missing evidence Jobs           paper_ladder.py evidence
L4 no checklist topic              sNN-paper-checklist/ (hai-studio new_topic.py --over-limit), then paper_check.py --write
L5 faces the views read            🙋 not mechanical: hai-paper-story (T, D tables, §8 Section Narrative, its #### Story arc
                                   and claims; the per-Section rows on the version's ## Narrative), hai-paper-plan
                                   (-drawing.yaml)
L6 a page face with no use-case:   writes the matrices' word under the H1: Board, Job, Task (🙋 when none fits)
```

**L5, the story the views read (JL 261109).** Report › Story and › Displays show Story by Section: first the whole
paper's Story arc (§8 `#### Story arc`), then a tab per Section, its part of the arc (the per-Section table, first header
`Section`, in the newest writing version's `## Narrative`; an older Board's §8 table is still read first), its claims
last. L5 asks for both; `hai-paper-story` writes them. `version` writes the table's header and `task` adds the new
Section's row with `<placeholders>`, which count as unwritten until a person or hai-paper-story fills them.

**Two layers, one source each (JL 261111).** The Story's Section Narrative holds what every version shares: title, story,
explanation, the claims C1..Cn with their numbers, and no per-Section rows. A new version face's `## Narrative` holds
that venue's layout only: claims to displays, display Runs, one row per Section, the compile order; it points at the
Story's Section Narrative (`tells:`) and copies no claim. `version` scaffolds that section, the person signs it with `page.py
sign-narrative <version> --quote "…"` (hai-draft § The Plan gate) before any Section's `page.py sign`, and the
whole-paper structure is the version Job's Report › Structure view (workbench-paper), never a Task. Planned for
`audit` (L5, not yet in `paper_ladder.py`): flag a version face whose `## Narrative` copies claim propositions, and a
Story Section Narrative that still holds a per-Section table.

**L6, every page says its use (JL 261108, 261109).** Each Board, Job and Task page shows its type and use case under
its title. The workbench never guesses a use: it shows the face's `use-case:` line, or the one use a type has in
the b16 matrices, and nothing when a type has several. So the face says it. `update` writes it from what the face
and folder already declare, never from nothing:

```text
Board      board-kind: grant-board → Initial application; else Manuscript development
Job        version: responds-to: → Feedback revision, else Manuscript drafting (from: alone is no sign)
           evidence: Figure and table preparation · Printed-value verification · Citation verification
           submission: Submission package preparation
Task       draft: responds-to: → Reviewer response; section_kind abstract|summary → Abstract or summary;
                  letter → Cover letter drafting; else Manuscript section
           display: type:, label: or display: (then the name) says figure or table → Figure|Table preparation
           value: …value-tables → Source table inspection; t99_ → Whole-paper value audit; else Printed-value verification
           citation: t99_ → Whole-paper citation audit; else Claim-group citation check
           submission: letter → Reference the version letter; portal-walk → Portal field survey; portal-fill → Portal preparation
```

A page that fits none (a `j51_insight_demo` Job, a display Task that says neither figure nor table) gets no guess:
L6 shows 🙋 and a person writes its line. A line already there is kept; when you add `responds-to:` later, change
`use-case:` too. Every scaffold (`board`, `version`, `next`, `task`, `evidence`, `submission`) stamps the faces it
makes by the same rule (`paper_check.stamp_use_case`), so L6 only fails on older Boards. The words are the Use Cases
of b16 `delivery/page-spec/block-views.md`, `job-views.md`, `task-views.md`; change them in both places.

Every carry-over step keeps its own rollback; nothing is committed. Update also removes an empty leftover `A1-Story/`
or `studio/` folder. Each step's title names the step, never a count.

**Undo, newest first.** `paper_ladder.py rollback <Board>` undoes the evidence Jobs step; then `paper_ladder.py update
<Board> --rollback` undoes the renames and sweeps, from the record `.ladder-undo/update-N/`. To undo the checklist
topic, delete its `sNN-paper-checklist/` folder. Run update in the paper's own session (one session per Project), dry run first, and show the person the dry run before `--apply`. A subagent, or any session that does not own the paper, stops at the dry run and reports it.

## 📄 The final draft in the Writing view

**Before anyone reads the assembled paper:** the whole build goes through `hai-paper-assemble` § The final read, a coauthor's or an author's read alike (JL 261104).

JL 261103: "where is the cover letter?"; "please update /hai-paper about this for the final draft writing view". The
Writing view's **The assembled paper** lists every document of the send, side by side: the paper (LaTeX and Word), the
supplement, the combined copy, and the cover letter. So a send needs, in the writing Job's `paper-build.toml`:

```text
[coverletter]   task = the t31 letter Task · journal · article_type · addressee · signatory · authors · affiliation · email
[outputs]       cover_letter_pdf · cover_letter_docx
t31 words       the body only: the build adds the date, the addressee, "Dear …" and the signature
t05_back-matter the statements (corresponding author, contributions, conflicts, funding, data sharing, AI use); in compile
                order, with [profile.latex] acknowledgments = false; not counted in the venue's words
[portal]        each upload slot (hai-paper-assemble § The portal packet)
```

A letter Task exported on its own still shows there, from its `word/` folder, but D3 stays ⏳ until the build makes it.

The Writing view also shows two Board files when they exist, each as its own section (JL 261110): `revision-plan.md`
first, "🗺️ Revision plan" (the round's steps as ⬜/✅ lines, each keeping its own mark, no tally), and `writing-patterns.md`
last, "🚫 Writing patterns to avoid" (the co-authors' patterns, `### N.` each; hai-paper-draft § Co-authors'
patterns). Both are authored files on the Board, so a private paper's words never enter Tools.

## 🪜 The ladder: Board · version · Task · Run

A paper is one Board; each send to a venue is a writing Job (a version); each Section, the
Abstract and each letter is a Page Task in that version; every Run is
`run-<type>-<target>` (b16 Q01, Q04, Q05). The contract is
[`ref/paper-ladder.md`](ref/paper-ladder.md); `scripts/paper_ladder.py` makes
each level (`board`, `version`, `next`, `spaces`, `task`, `run`, `rollback`).
Route a request by the level it names:

| Level | Folder | Its owners |
|---|---|---|
| Board | `Paper-<Slug>/` (a grant: `Grant-<Slug>/`): face, its topics `sNN-<topic>/` beside the Jobs (no `studio/` folder), `reports/`, `runs/`, `venues/`, `related/`, `delivery/` | Story and Ideation (studio topics and Board Questions), Venue, Related through Discovery |
| evidence | `j01_evidence_display/`, `j02_evidence_value/`, `j03_evidence_cite/`: one Task per display, value group or claim group | hai-paper-evidence (rules), hai-display (drawing) |
| version (writing) | `j11_writing_v<MMDD>_<desk>/` (older `jNN_v<MMDD>_<desk>/`): face with `## Narrative` (the layout, signed by `sign-narrative`; its Report › Structure view) and `## Questions`, its Tasks; output in Block `delivery/<version>/` | the Section release (G3), comments reports, assembly and send (G4, G5) |
| Task | `t00_abstract` · `t0N_` Main · `t2N_` Appendix · `t3N_` letters | `hai-paper-draft` over hai-draft's seven steps (below) |
| Run | `runs/run-<type>-<target>/` (its `run.yaml`, ticket and `passes/`, as `hai-run` has it); a Section's are the Page engine's | the run cards, `hai-paper-workflow/ref/run-cards.md` |

Use two orders for two different jobs. First route the family request:

```text
hai-paper
  → hai-paper-workflow, when the question is the journey or a gate
  → resolve the concrete Page and its Page Type
```

When creating or updating a concrete Page, use the Page router's order:

```text
hai-draft
  → hai-draft-workflow
  → current Run Workflow / Run Spec owner
  → hai-paper-workflow (Folder-owning workflow)
  → the exact Page Type: hai-paper-ideation · hai-paper-story ·
    hai-paper-draft · hai-paper-comments, or hai-paper-venue
  → Run Spec references / the Story's Section row and style policy
  → hai-run + selected workers, only where Runs exist
  → paper/hai-paper/ref/page-integration.md and ref/run-naming.md when a
    Paper-local Run or Page release is planned
```

For CONTEXT, OUTLINE, and EVIDENCE, the exact material contracts are
`workbench-task-draft/ref/...` files. The Page surface already installs the
shared Outline presenter; it is not a final execution dependency.

Read [`ref/page-integration.md`](ref/page-integration.md) for the Paper-specific
consequences of the shared Page contract. This router owns no second Page
lifecycle, Page Run namespace, Evidence Workspace, or Page release protocol.

`hai-paper-assemble` is a separate complete-paper verb after routing; it has its own bounded compile Spec in the Paper Workflow.

### A Section, step by step (b32 s41, on screen 2026-10-20)

A Section Task is a draft Task (`task-type: draft`), worked in hai-draft's seven steps. Its Report shows the five
middle steps as views (Work is retired, JL 261111; workbench-paper) (1 Plan to 5 Revise; Display only when the Section calls or makes a display); Studio and
Delivery are the top row's. The paper adds its own owner to four of the steps:

| Step (tab) | In a paper | Owner |
|---|---|---|
| 🎨 Studio | the Board's topics that name the Section (its story s02, its plan s04 rows) | hai-studio · hai-paper-story · hai-paper-plan |
| 📐 1 · Plan | §1 from the Section's contract (the face's reader-question … transition-out, from the version's `## Narrative` row); your Scratch, a note per paragraph; the venue's SUB-* rows beside the Requirement | hai-draft-logic · hai-paper-draft |
| ✍️ 2 · Write | `## 3 · Draft` from §1 and its Scratch, the desk's sentence and word limits; you type in its boxes too | hai-paper-draft · hai-draft-writing |
| 🔎 3 · Evidence | `evidence/cards.yaml` under the paper's rules (CITE from verified Results, one number everywhere); the prompt is `/hai-paper-evidence <task>` | hai-paper-evidence |
| 🖼 4 · Display | the Tables and Figures the Section cites, each the Board's display Task that names it in `cited-in:` (its one home, JL 261113; an older Board: a Section-side `display/Display<n>-<slug>/` or `results/` payload, still read), numbered for the paper (`label: Table 1`) and within the venue's limit | hai-display · hai-paper-evidence |
| 🔁 5 · Revise | Revise cards, then comments' Review Items routed to the Section | hai-draft-writing · hai-paper-comments |
| 📤 Delivery | the Section's lanes in `delivery/jNN_<version>/<tNN>/`; ◆ ready for the build | hai-delivery · hai-paper-assemble |

The version's Report shows each Section as one row with its five step words (Plan, Write, Evidence, Display, Revise;
`focus_draft.WORK`), each saying its state (done, next, sign, asked, send, optional, pass k, later) and opening that
step (`paper_version.section_row`).

## Paper Workflow and content owners

A Paper Workflow is the `paper-runs` layer: a list of bounded owner-native
Runs. Read
`hai-paper-workflow/ref/run-workflow.md` for Specs, dependencies and G0–G5;
Page containers, status reads and gate records do not allocate Runs.

| Owner | Paper responsibility |
|---|---|
| Ideation | source Idea Job projected as `s01-ideation/`; legacy Paper-local pools remain readable; `hai-paper-ideation` |
| Related work | the closest work: `s10-related-work-map/` maps it beside ours, `s11`-`s19` read one type each; `hai-paper-related` |
| Story | each telling as `sNN-story-<desk>-<idea>/` in the Board folder, its research questions as Board Questions with reports, the Narrative; `hai-paper-story` |
| Plan | after the story: `s03-paper-dataflow/` (how the data becomes each answer), `s04-paper-workflow/` (the Sections and dates to the send) and `s06-paper-displays/` (each display and its Run, checked against the venue's display rules); `hai-paper-plan` |
| Venue | shared evidence-backed desk contract; `hai-paper-venue` |
| Section (draft) | one Section, the Abstract or a letter, a draft Task: its plan and sentences in `draft/`; `hai-paper-draft` (was hai-paper-section) |
| Evidence | what backs each Section (`evidence/`; its displays are the Board's display Tasks) and one ledger per version: citations, one number per result, displays; `hai-paper-evidence` |
| Comments | one batch of comments (a review, a meeting, a coauthor pass) and its answers; `hai-paper-comments` |

Use native receipts to report the current owner, accepted Result/version,
pending dependency and next human decision. Retargeting keeps Story identity,
binds the selected Venue and changes only the new writing Job's `## Narrative`. Read the
exact PageType contract for its content rules; this router does not restate it.

`/hai-paper status` is a read-only rollup, not a Page Type or lifecycle.

## 🃏 Evidence and Page boundary

Paper Pages use the shared Page Face, Page Run, Evidence Item and Page CHECK
contracts. `hai-draft` and `hai-draft-workflow` own the lifecycle;
`workbench-task-draft` presents typed CITE, VALUE and DISPLAY Results. Load
[`ref/page-integration.md`](ref/page-integration.md) for the Paper-specific
ownership, release, source/projection and Run boundaries, and
[`ref/run-naming.md`](ref/run-naming.md) for Paper context and identities.

Supporting Task/Discovery Runs retain their native owners. A Page-local Result
is the evidence authority for the Page; assembly may copy accepted artifacts
but never becomes a wording or evidence source.

For visual displays, load `hai-display`; its concept-first gate owns
composition references, editable reconstruction and candidate promotion.

**The paper Board holds the evidence; work and discovery Blocks create it** (JL 261022: "for /hai-paper, we should
have a paper block and a work block to provide the displays and E-work, right?"; JL 261031, the four layers above).
Work Blocks `work/bNN_.../` hold the Runs that make every number and every underlying table on raw data; the paper
Board's evidence Jobs deposit them: `j01_evidence_display` (one Task per display, each picture or table drawn by its
own Run from the value Job's copies of returned, aggregated Results: values first, then displays, JL 261110),
`j02_evidence_value`, `j03_evidence_cite`. Until 261031 the display Job sat
in the work Block (`j21_paper_displays`, `j21_<venue>_displays`); an older Project keeps it there until it is moved. The displays start from a **display plan**, the `s06-paper-displays` Studio topic (hai-paper-plan), which the authors agree before anything is
drawn (JL 261023: "this should be a plan, proposed to the author to think about how to draw them"): one row per
display with its number, title, the one question it answers, its layout (rows, columns or axes), its source Runs
and its open choices, written from the team's own record (meeting notes, slides) in that topic's face (older Boards: the plan sits in the display Job face). The Sections write
their numbers only after the drawn displays pass review and are accepted, so a sentence never describes a table
that is still changing. The display Task holds the display whole (question, caption, legend, number,
size, review; JL 261113); its Run only draws from returned, aggregated Results, and no paper folder runs analysis on raw data. The version face (or `board.md`) names the Block in a
`work-block:` line. The rules are hai-paper-evidence's rule 3.

## 🚪 Routing

Resolve the paper root and target Page before changing anything.

| User intent | Route |
|---|---|
| brainstorm, novelty-check, compare or select ideas | `hai-ideation` and only its relevant specialist; use `hai-paper-ideation` when a Paper Page projection is involved |
| create, refresh, read or check the Paper Idea portfolio Page | `hai-draft` + `hai-draft-workflow` + `hai-paper-ideation`; load the semantic owner for sync/handoff |
| ask where a paper is in the journey, or test a gate | `hai-paper-workflow` |
| draft or review the whole paper, its research roadmaps or section narrative | `hai-paper-story` |
| plan the data flow or the paper flow (s03, s04): which Run feeds which question, which Section answers it, the displays, the dates to the send | `hai-paper-plan` |
| release work, inspect execution progress, accept a receipt, or release a Section | `hai-paper-workflow` plus the exact Discovery/Task/Section owner; use Story for the resulting paper meaning |
| inspect or record a target venue | `hai-paper-venue` (shared reference library) |
| write or revise one manuscript/appendix unit | `hai-paper-draft`, one step at a time (A Section, step by step) |
| check a Section's or a version's evidence, citations, numbers or displays | `hai-paper-evidence` |
| give each Section Page its own session, or message the Section sessions | `/hai-paper sessions`: [`ref/section-sessions.md`](ref/section-sessions.md) and `scripts/create_section_sessions.py` |
| start the paper writing lab: VS Code windows (draft page above, Claude session below), the Board session (board.md `board-session:`) first, plus a Codex thread per Section | `/hai-paper lab`: [`ref/writing-lab.md`](ref/writing-lab.md) and `scripts/open_writing_lab.py` |
| take in or answer one batch of comments (review, meeting, coauthor, advisor) | `hai-paper-comments` |
| check paper or one family's status | `/hai-paper status` (command, not a Page Type) |
| run one Page through its lifecycle | `hai-draft-workflow` |
| compile or export one Page | `workbench-task-draft`, using its LaTeX or Word lane |
| assemble the paper | `hai-paper-assemble` from the Section Pages' own `delivery/latex/` outputs and accepted bindings |
| respond to reviewers | `hai-paper-comments`: a review Job on the Board (`jNN_review_<kind>_v<MMDD>/`, `for:` the version), its Review Items routed to the Sections |
| start a paper, a version, a Section or a Run | `scripts/paper_ladder.py` (`board`, `version`, `next`, `task`, `run`) |
| bring an older paper folder onto the latest layout | `scripts/paper_ladder.py audit`, `update [--date MMDD] [--apply]` |
| prepare a send's portal: the cover letter, what to paste into each field | § The submission Job: `scripts/paper_ladder.py submission`, then `scripts/portal_fill.py` |
| where a paper stands, and its delivery | `checklist.md`, `scripts/paper_check.py <Board> [--write]`, the Board's `sNN-paper-checklist/` |
| run the must-check gate on a Section or a version | `scripts/must_check.py <task or version-job> [--json]` (it runs `scripts/scope_guard.py <task>` and the evidence scripts, then names the reading agents to dispatch) |

### Paper verbs

```text
/hai-paper ideate <direction|idea-id> [controller-label]
/hai-paper enter [paper]
/hai-paper status [paper] [section|evidence|citation|display]
/hai-paper journey [paper]         read the journey position · test the gates ·
                                       never advances anything
/hai-paper story [paper] [controller-label]
/hai-paper venue <target> [controller-label]
/hai-paper section <section-id> [controller-label]
/hai-paper sessions [paper]        a named Claude session + Codex thread per
                                       Section (one for the Appendix), once the
                                       writing Job's ## Narrative fixes them
/hai-paper lab [paper]             the writing lab: VS Code windows, the Board session
                                       (board-session:) first, then each Section's
                                       draft page on top and its Claude session below;
                                       creates missing Claude sessions and a Codex thread
                                       per Section (Codex app), paired
/hai-paper comments <new|id>
/hai-paper assemble [paper]        runs anytime · a build made while gate G4
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
| idea generation, testing, selection | `hai-ideation` → its generate/test/select skill and requested specialist |
| external sources, review, synthesis | `hai-discovery` → selected Discovery capability |
| computation, experiments, reusable execution | `hai-task` → selected Task worker |
| native Run identities and closure | `hai-run`, when commissioning/resuming a Run |
| a concrete Page | `hai-draft` + `hai-draft-workflow` + its exact Paper PageType |
| Page outline/evidence material | the relevant `workbench-task-draft/ref/...` contract; presenter already installed |
| one Page export | `workbench-task-draft` and the selected format reference |
| a display Evidence Item | `hai-display` and the chosen worker, through the Page RE Result contract |
| Paper board presentation | `workbench-paper`; `hai-draft` owns rendering/checking |

### What the person sees · the Paper Workbench

A person who names a Workbench tab means its owner below. The link and the
screen's own rules are in `workbench-paper`.

| Level › Space › view | What it shows | Owner skill |
|---|---|---|
| Studio › Related (folded under the topics, the Board's) | `related/related.md`, one row per item, grouped by its subfolder (meetings · papers · files · emails) and then its `group` cell, opening on its file; by question in Report › Related Papers | `hai-related` · `hai-paper` · `hai-discovery` |
| Studio (top row, the Board's) | the Board's `sNN-<topic>/` folders, one drawing each, with Tags and Stage | the base frame (`hai-studio`) |
| Delivery (top row, the Board's) | `delivery/jNN_<version>/`, one per version; from a version, its part | `hai-paper-assemble` · `hai-delivery` |
| Board › Report (focus page, `layout=focus`) | seven views: Idea, Story (including venues, `venues/<venue>/call.md`), Data + Paper Plan, Support blocks, Evidence, Displays and Writing; each has Review Content followed by Around the Work. Legacy Board Work routes redirect to Report. | `hai-paper-ideation` · `hai-paper-story` · `hai-paper-venue` · `hai-paper-plan` · `hai-paper-evidence` · `hai-paper` (`paper_ladder.py`) |
| Board › Description › Scope · Venue · Resources (frame layout only; on the focus page the venues sit in Story) | the face; `venues/<venue>/`; resources | `hai-paper` · `hai-paper-venue` |
| Board › Audience Report › Ideation · Narrative · High-level logic + Low-level work · Related Questions · Related Papers (frame layout) | the ideation Questions; the story; each research question as Question │ Work │ Report; the reviewer and reader questions; the related papers by question | `hai-paper-ideation` · `hai-paper-story` · `hai-report` |
| version › Description › Version · Venue rules (frame layout) | the version face; the venue's call | `hai-paper` · `hai-paper-venue` |
| version › Report (Work is retired) › Draft-Main · Draft-Appendix · Display-Main · Display-Appendix · Values · Citations | each Section a row with its five step words, each opening that step; the evidence Jobs' Tasks | `hai-paper-draft` over `hai-draft`'s steps · `hai-paper-evidence` |
| version › Audience Report › Questions · Draft-Main · Draft-Appendix · Comments · Cover letter (frame layout) | the standing J1-J5 and the version's Questions; each Section as Question │ Work │ Report; the Review Items of its comments reports; the letter, paragraph by paragraph | `hai-paper-comments` · `hai-paper-assemble` |
| Section › Report (Work is retired) › 1 Plan · 2 Write · 3 Evidence · 4 Display · 5 Revise | each step, Operation (Input, Sign, Prompt) over Result; the SUB-* rows in 1 Plan; Display only when the Section has one | `hai-draft` (the seven steps) · `hai-paper-draft` · `hai-paper-evidence` |
| Section › Report · Description · Delivery | the steps' Results, Table, Questions, Comments; the reader contract; ◆ ready for the build | `hai-paper-draft` · `hai-paper-comments` |
| any level › Runs | that level's own Runs, by run type | the run cards (`hai-paper-workflow`) |

Load only what the request uses. Reuse an already loaded owner; do not recurse
between the Paper router, Page router and domain adapter. Insight and Design
remain independent families, referenced through their own Results/contracts.

## 📐 Story boundary

`hai-paper-story` owns each telling's meaning (its studio topic and Board
Questions), the read-through test and the selected telling. Each Section binds
its row in its version face's `## Narrative` through `story-row:`. Read
`hai-paper-story/ref/integration.md` for the compile-order interface;
planning a Section does not instantiate its Page, authorize execution or imply
approval.

## 📂 Paper structure

Read [`ref/paper-ladder.md`](ref/paper-ladder.md) for the folder layout,
group and Section naming, compile-order markers, Task boundary, delivery law
and migration rules. The Paper router only resolves the structure owner; it does
not maintain a second naming or migration contract. In short: the evidence Jobs are `j01_evidence_display/`, `j02_evidence_value/`, `j03_evidence_cite/`; a version is a
writing Job `j11_writing_v<MMDD>_<desk>/` (older: `jNN_v<MMDD>_<desk>/`) and its
Tasks are named by series, `t00_abstract` · `t0N_` Main · `t2N_` Appendix · `t3N_` letters; a comments
batch is a review Job on the Board, `jNN_review_<kind>_v<MMDD>/` (an older Board: `reports/qNN_<kind>-<MMDD>/` in the version; `scripts/carry_over/rename_tasks.py` renames an older
version once).

## 🧑‍💻 Section sessions

Once the compile order in the writing Job face's `## Narrative` fixes the Sections, `/hai-paper sessions`
gives each Main Section Page, and the Appendix group as one unit, a named Claude
session and a named Codex thread (`<Short>-<unit>`, `<Short>-<unit>-Codex`),
pairs them, records both ids in the page header (`session:`, `codex-session:`),
and stops the Claude session after its first turn (a read-only look, then the default review round) so `/resume` can open
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
`hai-paper-assemble` reads only what those lanes export, and it takes a
Section's approval from its newest draft version: while a Run works on a new,
unapproved version, the build lists that Section as not ready and prints only
its numbered placeholder, unless `paper-build.toml` sets
`draft_includes_unready = true`, which prints the Section's last export in a
DRAFT build. Contract: `hai-draft-workflow/ref/interactive-writing-run.md` §🔖.

## 📦 Assembly and delivery

`hai-paper-assemble` owns source-driven complete-paper builds. It reads
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

G4 also needs the evidence chain to hold: `hai-paper-evidence/scripts/chain_check.py <Board>` exits 0
(run as the value Job's `t99_paper_value_check`). Work computes, the value Run copies and gives ids, displays and
Sections read pinned ids only; a failing line blocks the send (hai-paper-evidence, The chain).

## 🧱 Current architecture boundary

The former S01–S10 stage contracts, stage resolver, S-page creator, S03/S04
topic-entry tooling, stage-specific craft, and their helper scripts are outside
the current Paper runtime. This door does not load them.

A telling's seed (identity, pitch, stakes) and its roadmaps live in its studio
topic, alongside the shared Section Narrative (§8: title, story, claims). Its
research questions live in Board Questions with reports. Each writing version's
`## Narrative` holds its layout (Section rows, claims to displays, compile order),
pointing at the Story's Section Narrative and copying no claim;
execution, Section, compile and comments records stay with their native owners. The router reads no retired child
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
