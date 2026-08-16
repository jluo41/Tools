# What SKILL.md must say
state: 🟡 PARTIAL
owner: CC
method: SKILL.md stays as short as possible; details live in the ref/ files

## Opening
What must `SKILL.md` explain, and what detail should it leave to `ref/`?

This file is the first thing every Board session reads, so each extra line has a recurring cost.
Cut too much and a newcomer cannot operate the tools or recover the rules this Board settled.
The split determines whether the manual stays both usable and small as the system grows.
It succeeds when a fresh agent can run the workflow and knows exactly where deeper specifications live.

**Covered elsewhere**: How to **verify it suffices** once written: that is `QF2` (fresh-agent cold read).


## Diagram

```
user types  /haipipe-board
          │
          ▼
      SKILL.md  771 lines (0.124.0, 260806): operations only, spec details never inlined
          ├─ the family: one door, one Page base (haipipe-page), two contract catalogs
          ├─ the shape: what a board looks like (Q + S pages, group intros, embeds)
          ├─ eleven verbs: view · open · add · stage · build · sync · link · close  (offline)
          │                serve · excalidraw · comment                             (live)
          │                plus routed verbs: one-page work goes to haipipe-page,
          │                one-sentence work to haipipe-sentence
          ├─ the metadata head + fixed section order of one Q/S page
          │  (the full page contract lives in board/haipipe-page)
          ├─ three writing rules (no invented terms / purge stale lines / fresh-agent cold read)
          ├─ the four prohibitions
          └─ board ↔ SKILL.md: the graduation mechanism
                │
                ▼  go to ref/ only when detail is needed
        ref/page-template.md          copy to add a Q or S page (renamed from q-template.md 260801)
        ref/board-form.md             full spec: folders · numbering · section↔render §4 · Links §4b · body syntax §5 · generated site §8
        ref/writing-rules.md          how to write plainly + cold-read prompt + convergence criterion
        ref/topic-entry-contract.md   the evidence page: head `route:` key · E<n> divisions · nested probes/ QA-probe records
        ref/board-example.md          a minimal two-question example
        ref/page-lifecycle.workflow.js  the bounded Page RUN controller (producer, build snapshot, independent CHECK, route)
```


## Aims
### The manual's operating answers
- [x] SKILL.md written
      Family · shape · eleven verbs (view/open/add/stage/build/sync/link/close offline, serve/excalidraw/comment live) plus the routed page and sentence verbs · the page head and section order · writing rules · prohibitions · ref/ index.
- [x] Answers "how to open a new board"
      The open section, five steps, including the single place that must stop and ask the user (the Q list needs a nod).
- [x] Answers "how to add a Q to a board"
      Copy `ref/page-template.md` → rename → into the Pages → regenerate.
- [x] Answers "when does a board close"
      Every question at ✅ or ⏸️; `close:` is the closing condition and must be verifiable.

### Staying in sync with the board
- [x] Settles how SKILL.md stays in sync with the board
      The **graduation mechanism** (see ## Law): when a Q reaches ✅, its `## Law` is copied into SKILL.md; unsettled ones never enter.
      Written into SKILL.md as the "board ↔ SKILL.md" section.
      This rule is itself one of the things SKILL.md must state.
- [ ] The live layer (serve/chat/terminal) written as rules
      serve, excalidraw, and comment now carry real action sections in the door.
      Chat and terminal still get pointers only, because QD1/QD2/QD3 are still 🟡.
      When they reach ✅, graduate them in one by one.

### Proven on fresh-agent cold reads
- [x] A fresh agent can open a decent board from it alone
      QF2 ran (260723, GPU-cluster topic): a fresh agent, given only SKILL.md + ref/, opened a valid 5-question board on the first try, verdict YES.
      The single real gap it exposed (how to invoke build.py) is fixed into SKILL.md.
      Re-run 260725 against the shared Q/S skill (4 Q + 1 S), verdict YES again; see the next item for what it cost.
- [x] 📝 The manual describes S pages on the writing side, not only the reading side
      Until 260725 SKILL.md explained how an S page RENDERS but never how to create one: `open` asked "有哪几个 Q", step 4 named files `Q<letter><n>` only, `close` used the words "human-gated / explicitly parked" as if they were states, and nothing said how an S is listed in `## Pages`.
      QF2's re-run had to guess all of it (and guessed right, which is worse: the documents took credit for the agent's judgment).
      Fixed in the same pass: `open` steps 1 and 4 now ask for Q **and** S pages and give both filename shapes plus S's required `## Content`; `close` and the Page section state that both kinds share the same four `state:` values, with ✅ meaning "checkboxes closed" on Q and "human gate passed" on S; `ref/board-form.md` §2 gained the S state mapping and the Pages rule (bare filename, free-text group heading), §3's example gained an S line; `ref/page-template.md`'s consumer record no longer assumes a paper's `1-probes/` tree.
      The build section also names the interpreter split (build/watch on any `python3`, `serve.py` on the venv for the SDK).


## States
**Written, validated by QF2, and kept current through the 0.124.x series; only the live layer's chat and terminal stay pointer-only until the QD group settles.**

- 260731 JL · 🔍 Three fresh reviewers audited the family's contracts: 55 findings
  JL asked whether the Skill pages are up to date and dispatched the review as a fan-out, which is the first real use of the parallel pattern `Agent-2` was built for.
  Three agents took the two SPECs, the routing and index units, and this door skill; they returned 20, 16, and 19 actionable findings, and every one carried file-and-line evidence on both sides.
  All seven mirror pages were already in sync, so nothing was stale in the SENSE the generator can detect; what the reviewers found is drift the generator cannot see, between a contract's words and the code it claims to describe.
  Fixed the same round, each verified against source before the edit: the frontmatter version said 0.73.1 while its own CHANGELOG documented 0.78.0 and its summary was already 0.78.0's text, so the board displayed the wrong version; a blind Question to Opening replacement on 260731 had turned three alias declarations into the tautology "Opening is an alias for Opening" in `SKILL.md`, `ref/board-form.md`, and `ref/page-template.md`, which destroyed the only statement that old pages still parse; ten further `Question` residues were repointed individually across four files; two SPECs carried a version number inside body prose that had already rotted two releases behind their own frontmatter; `haipipe-page` cited §8 for a mapping that lives in §4; and the sentence spec cited `> USER:`, which is the paper family's lane id and appears nowhere in this family's authority.
  Still open, and too large for one round: the door never mentions the `live/` package at all, so four of its five live-layer citations point at `serve.py` where the code no longer is; three sections describe Index elements that 0.78.0 removed; `Skill-<n>` and `Agent-<n>` are missing from its page-kind list while line 45 actively denies that such kinds ship here; and the `page` SPEC still says three page kinds when the code has four.
  Since landed in the 0.124.x door: the `live/` package is documented file by file in its ref index, `cli/skillpage.py`'s `Skill-<n>` and `Agent-<n>` pages are named there, and the page contract now lives in `haipipe-page` (0.21.0) with ten Page Types under `board/page-types/`.

- `SKILL.md`, 771 lines at 0.124.0 (260806)
  Operations only: the family (one door, one Page base, two contract catalogs), the shape (Q + S pages, group intros, embeds), eleven verbs (view / open / add / stage / build / sync / link / close offline, serve / excalidraw / comment live) plus the routed page and sentence verbs, the page head and section order, three writing rules, four prohibitions, the graduation mechanism, a ref/ index.
  Spec and prose details never inlined; it enters the context on every invocation, shorter is better.
  JL's 260731 shrink ruling (Decision Now, option B) has not yet landed as a smaller file: the door has grown past the 581 lines it was ruled on, as the family section, the routed verbs, and the live layer's real action sections moved in.
- `ref/`, six files
  `page-template.md`: the shared Q/S source template (renamed from `q-template.md` on 260801); the page contract it instantiates is owned by `haipipe-page`.
  `board-form.md`, the full spec: folders, numbering, board.md, the section↔render mapping (§4), `## Links` (§4b), body syntax (§5), the generated Board-Webpage (§8), the invariant.
  `writing-rules.md`: hard writing rules + the zero-background review prompt, convergence criterion, and past scores.
  `topic-entry-contract.md`: the evidence page contract from the 260806 redesign (head `route:` key, `### E<n>` divisions, `### E0` queue) and its nested `probes/` QA-probe records.
  `board-example.md`: a minimal two-question example, English since the 260731 language ruling; predates the Q/S merge (no S page, no Content section), so the template, not it, is the authority on shape.
  `page-lifecycle.workflow.js`: the bounded non-linear controller for one Page RUN (producer, build snapshot, independent CHECK, route).
- `CHANGELOG.md`, one entry per body of work, version matching SKILL.md's `version:` line
  Grown from 0.2.0 alongside the board: the Q/S page merge (0.13.0), the Opening and Diagram rulings (0.13.x-0.14.0), the index chatbot (0.15.0), and the QA2 template alignment (0.15.1) are recorded there, up through 0.124.0 (the 260806 evidence-page redesign).
  Its early self-correction stands: the invariant is "strip every script and every page plus all body text remains", asserted on every build.

- 260725 CC · 📝 The S-page instructions caught up with the S-page renderer
  QF2's re-run exposed that every S instruction in the manual was about reading a stage, not writing one, so a newcomer had to invent the Pages listing, the state value, the filename, and the probe pointer.
  All four are now written down (`open` steps 1/4, `close`, the Page section, `ref/board-form.md` §2/§3, `ref/page-template.md`).
  The lesson is general: **the reading contract graduated on its own and left the authoring contract behind**, which is invisible to anyone who already knows both.

Still open: the live layer's chat and terminal graduate in only when the QD questions settle; serve, excalidraw, and comment already carry real action sections.

### Decision Now
These are the calls only JL can make; CC ticks nothing here.
Two of the three below were ruled by JL on 260731, and their ticked rows stay here, attributed, until the work they authorize has fully landed.

- [x] 🗣 Rule the language of the family's own contracts
      DECIDED 260731 by JL: option A, and applied to ALL of them, not only the door ("yes, do it. Apply to all").
      `haipipe-board/SKILL.md` was 342 of 581 lines Chinese (59%) while all five sibling units and both agents were 0%, and the split was chronological rather than principled: the newest sections were wholly English and everything older was Chinese, two of them mixing mid-bullet.
      What made it cost something: 32 normative rules existed ONLY in Chinese, three of them load-bearing, being the skill's one mandatory stop-and-ask gate before scaffolding a board, the whole write-back obligation ("done means written back"), and the rule keeping a listener that carries a real shell on loopback.
      The family's own evidence decided it: `ref/writing-rules.md` and `src/page_board.py`'s `scrub_cjk_comments()` both already cited a JL 260724 English-only ruling, so the door contradicted the rule it shipped.
      Scope of "all": `SKILL.md`, `ref/board-form.md` (65% Chinese), and `ref/board-example.md` (41%); source-code comments are OUT of scope, because `scrub_cjk_comments()` already rules that the source keeps its comments for developers while the OUTPUT stays English.
      The 51 em-dashes in the door were all Chinese doubled dashes, correct punctuation there, so each became different punctuation in the English text rather than surviving as a house-rule break.
      LANDED 260731, all three files: `SKILL.md` 596 lines and 0 Chinese in its body, `ref/board-form.md` 399 lines and 29 sections intact, `ref/board-example.md` 114 lines, and all three are 0 em-dash and 0 hard-wrapped.
      Two categories of Chinese are deliberately KEPT, because they are data the machine matches on rather than prose a reader follows: the two legacy Chinese section aliases still listed inside backticks in `board-form.md` §4, which `ALIAS` still resolves, and the trigger phrases in the door's frontmatter description, which are how a Chinese-speaking user reaches the skill at all.
      A translating agent had removed the trigger phrases; that is a functional regression rather than a style fix, so they were restored on the same precedent as the alias tokens.
      The board felt it immediately: warnings fell from 34 to 13, because the Skill mirror pages stopped carrying Chinese into an English-only board.
- [ ] 📏 Rule whether the board's prose rules bind `SKILL.md` at all
      They do not today: `check.py` scans `page_files()`, so no checker has ever read a single `SKILL.md`, and the one-sentence-per-line, English-only, and no-em-dash rules are board-page rules only.
      Measured: the four SPECs and verbs are already clean at 0 wrapped lines; `haipipe-board/SKILL.md` has 20 and the two agent files have 8 and 3.
      A · extend `check.py` to the family's own `SKILL.md` and `ref/` files, so the rules bind the contracts the same way they bind a page.
      B · keep the rules board-only and treat a skill file as prose whose author decides, which is the status quo.
      C · rule them in but enforce by review rather than by checker, so a reviewer catches what no script looks for.
      → CC recommends A for one sentence per line and no em-dash, because both are cheap to check and every recently written unit already passes; the language half of this is now settled by the row above.
- [x] 🧾 Rule what the door owes now that it is 581 lines
      DECIDED 260731 by JL: option B, move the stale halves into the SPECs that now own them and let the door shrink.
      This page's Law already said "SKILL.md stays minimal, operations only", and the reviewers found the door promising three things it cannot execute: the creator-agent fan-out (unshipped by its own CHANGELOG), authoring a `Skill-<n>` or `Agent-<n>` page (the kinds live in `skillpage.py` and are named nowhere in the door), and writing a `### Decision Now` row (required by the page SPEC and absent here).
      The family was split precisely so the door could stop restating what the SPECs own, and three of those four areas already have a better home.

## Files
- `SKILL.md`
  The deliverable itself.
- `ref/board-form.md` · `ref/writing-rules.md` · `ref/page-template.md` · `ref/topic-entry-contract.md` · `ref/board-example.md` · `ref/page-lifecycle.workflow.js`
  Where the details go; SKILL.md stays minimal because these six catch everything.
- `CHANGELOG.md`
  Version and change record, aligned with SKILL.md's `version:`.

## Law
- Graduation: SKILL.md = the crystallization of the board's settled questions
  This board (`diagram/BoardSkillBoard-260722/`) is the full design record; SKILL.md keeps only the conclusions of `✅ SETTLED` questions.
  When a Q reaches ✅, copy its `## Law` rules into SKILL.md's matching spot. **Unsettled questions (🟡/🔴) never enter the manual**, otherwise ad-hoc choices get written as iron law (QD1's permission rule was hard-coded and overturned exactly that way).
  So SKILL.md always equals the sum of settled rules; before editing it, check whether that question is ✅.
- SKILL.md stays minimal
  Operations only; spec, syntax, and prose details all go to `ref/`.
  It enters the context on every invocation.
- The live layer gets pointers, not rules, for now
  serve.py's comment write-back graduated with QA6 ✅; chat/terminal (the QD group) are still 🟡, so SKILL.md carries only pointers.

## Glossary
`SKILL.md`: the entry file of a Claude Code skill.
When the user types `/haipipe-board`, this is what gets read in. graduation: once a Q settles (✅), moving its settled rules from the board into SKILL.md, where they become instructions people follow.

## Discussion

## Log
- 260806 2131 · [REVISE-CC] swept to the 260806 architecture; the door's current shape corrected from the 0.15.x snapshot (~280 lines, nine actions, four ref/ files) to 0.124.0 reality (771 lines, eleven verbs plus routed page/sentence verbs, six ref/ files incl. topic-entry-contract.md), the QC1a canvas frame linked now that it exists, and the 260731 audit's four open items marked landed
260801 0130 · Reindexed QC1 -> QC1a under the new QC1 skill-family parent (JL 260801)
260731 · JL ruled the language row A and applied it to ALL the family's Chinese files, plus the door row B (shrink by moving stale halves into the SPECs); ref/board-example.md converted, SKILL.md and ref/board-form.md dispatched as a fan-out
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260731 · Fan-out audit of all seven family contracts (3 fresh reviewers, 55 findings): fixed the wrong frontmatter version, three alias tautologies from the Question-to-Opening replacement, ten Question residues, two rotted in-body versions, one wrong section citation, one imported paper lane id; three Decision Now rows opened on language, rule scope, and what the door still owes
260725 1215 · S pages written into the manual's authoring side after QF2's re-run found four gaps (open steps 1/4 · close + Page state values · board-form §2/§3 Pages and state mapping · q-template probe pointer · the python3-vs-venv split); 0.16.0
260725 1140 · Stale numbers purged in the QB alignment pass (JL's go): "128 lines / five actions / CHANGELOG up to 0.2.0" replaced with the 0.15.x reality (~280 lines, nine actions, Q/S page wording); ref/ descriptions updated, board-example.md's pre-merge shape noted
260724 1242 · Translated to English (JL 260724: everything on the board in English); purged the stale "written but not yet verified" lead: QF2 passed on 260723
260723 · Rewritten to the new structure: Question expanded into "one paragraph + bullets", added `## Boundary` and `## Files`; the retired `## Why here` merged into Question
260723 1720 · QF2 acceptance passed → ticked "a fresh agent can open a board"; SKILL.md gains: invoke build.py with its path + slug/default-state/owner conventions
260723 1700 · Graduation mechanism settled (Q ✅ → Law copied into SKILL.md), written into ## Law and SKILL.md's "board ↔ SKILL.md" section;
              graduated the three already-✅ questions along the way: fixed the stale "Sync" wording in the comment section (QA6: Save writes the disk),
              introduced the serve.py action, live layer as provisional pointers only; version 0.2.0 → 0.3.0
260723 1210 · Added the sync and link actions; board↔artifact coupling had never been written down
260723 1210 · board.md gains ## Links; paths in body text become clickable links
260723 1150 · SKILL.md finished (128 lines) + the four ref/ files; CHANGELOG at 0.2.0
260723 1150 · ref/board-example.md replaced (old format); ref/q-template.md gains ## Comments
260723 0919 · Renumbered Q4 → QC1; title compressed; finish line into a checklist
260722 2255 · Opened
260722 2249 · Skill folder moved from skills/board/ to skills/0_utils/haipipe-board/
